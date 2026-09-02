# -*- coding: utf-8 -*-
r"""
Publicar comentarios anclados en el documento de un estudiante, manejando Google Docs como lo harías tú.

QUÉ HACE Y POR QUÉ ASÍ
----------------------
El Docente recibe un documento compartido y quiere dejar comentarios **anclados a la frase** de la que
hablan. Por API eso no se puede: la API de Docs no crea sugerencias, y las anclas que fija un programa
las dibuja Google como comentarios *sueltos*, sin frase (ver `VIABILIDAD_COMENTARIOS_GOOGLE_DOCS.md`).
Además, comentar un archivo ajeno exigiría el alcance amplio `drive`, porque **no existe un alcance de
solo comentar**.

Así que aquí no se llama a ninguna API: se usa la sesión del navegador del Docente y se repite la
secuencia de teclas que él haría. Google Docs dibuja el texto en un lienzo, no en el DOM, así que
seleccionar con el ratón no es viable; la única vía es el teclado:

    Ctrl+F  →  escribir la cita  →  Enter  →  Escape   (la selección queda sobre la coincidencia)
    Ctrl+Alt+M  →  escribir el comentario  →  Ctrl+Enter

Comprobado el 22/08/2026 sobre un anteproyecto real: el comentario queda anclado **exactamente** a la
cita, ni un carácter de más. La comprobación no es visual: se exporta el documento a `.docx` y se leen
`word/comments.xml` y los `w:commentRangeStart/End`, que dicen qué texto quedó anclado de verdad.

TRES REGLAS QUE IMPONE EL MECANISMO
-----------------------------------
Buscar con Ctrl+F no es lo mismo que recorrer el documento por programa, y de ahí salen tres
validaciones que la ruta de Apps Script no necesitaba:

1. **La cita cabe en un párrafo.** Ctrl+F no cruza saltos de párrafo. Una cita a caballo entre dos
   nunca se encuentra, y el comentario se quedaría sin publicar.
2. **La cita es única.** Ctrl+F va a la primera coincidencia. Si la frase aparece dos veces, el
   comentario aparecería delante del estudiante señalando la frase equivocada.
3. **La cita se escribe, letra por letra.** Cuanto más larga, más lenta y más frágil; cuanto más
   corta, más fácil que se repita. Se exige un mínimo y se avisa del máximo.

EL LENGUAJE DE LOS COMENTARIOS
------------------------------
Lo lee un estudiante, no un comité. Se habla del **contenido y de la estructura del documento**: qué
dice esta parte, qué le falta, cómo encaja con las demás. El criterio de la guía va en el plan como
trazabilidad —para saber de dónde salió cada comentario— pero **no se publica**: nadie escribe
«Criterio "Problema argumentado con evidencias" — párrafo 12» a un estudiante. `revisar_lenguaje()`
rechaza esas aperturas de oficio.

ÓRDENES, EN EL ORDEN EN QUE SE USAN
-----------------------------------
    leer      descarga el documento vivo y lo vuelca numerado, con los criterios del ACA
    simular   valida el plan contra el documento y dice qué se publicaría   ← SIEMPRE primero
    ensayar   publica de verdad, pero en una COPIA en tu Drive; nadie se entera
    comentar  publica en el documento del estudiante          (exige --confirmar)
    deshacer  borra los comentarios de la última publicación (por el recibo que dejó)

`ensayar` existe porque `simular` no puede mentir pero tampoco puede probarlo: comprueba el plan, no
el documento vivo. El ensayo sí publica, y el Docente lo ve con sus ojos antes de tocar el trabajo
del estudiante.

DÓNDE VA EL TRABAJO DEL ESTUDIANTE
----------------------------------
En `_Revisiones/`, **ignorada por git** (ver su LEEME). Material crudo con nombres propios: se
sincroniza a Drive, al historial no entra. Mismo criterio que dejó fuera `3 - Transcripcion.md`.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import criterios_aca as CA  # noqa: E402
import plan_comentarios as PC  # noqa: E402
import sesion_google as SG  # noqa: E402
import syllabus_curso as SY  # noqa: E402

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
REVISIONES = REPO / "_Revisiones"

# Límites de la cita. El mínimo evita coincidencias por casualidad; el máximo, teclear un párrafo
# entero en la caja de búsqueda (lento y sin ninguna ventaja: con anclar la frase basta).
CITA_MIN = 20
CITA_MAX = 180

# Aperturas de oficio: si un comentario empieza así, no está hablándole a una persona.
# El de la izquierda es el patrón; el de la derecha, qué hacer en su lugar.
LENGUAJE_DE_OFICIO = [
    (r"^\s*criterio\b", "no cites el criterio: di qué le falta a esta parte del documento"),
    (r"^\s*(no\s+)?cumple\b", "no dictamines: explica qué habría que cambiar"),
    (r"^\s*seg[uú]n\s+(el|la)\s+(criterio|r[uú]brica|gu[ií]a)", "habla del documento, no de la rúbrica"),
    (r"^\s*de\s+acuerdo\s+(con|a)\s+(el|la|los)\s+(criterio|r[uú]brica)", "habla del documento, no de la rúbrica"),
    (r"^\s*se\s+evidencia\b", "escribe en directo: «aquí falta…», «esta parte dice…»"),
    (r"^\s*el\s+estudiante\b", "háblale a esa persona, no de esa persona"),
    (r"^\s*p[aá]rrafo\s+\d", "el ancla ya señala la frase; no hace falta numerarla"),
    (r"\b(insuficiente|satisfactorio|sobresaliente)\b", "esas son bandas de nota, no observaciones"),
]


# ─────────────────────────────── el documento vivo ───────────────────────────────

def doc_id(x: str) -> str:
    """Acepta el enlace que te compartieron, o el id pelado. Es lo que el Docente tiene a mano."""
    m = re.search(r"/document/d/([\w-]{20,})", x)
    if m:
        return m.group(1)
    x = x.strip()
    if re.fullmatch(r"[\w-]{20,}", x):
        return x
    raise SystemExit(f"«{x}» no parece un enlace ni un id de Google Docs.")


def descargar(ctx, doc: str, destino: Path) -> Path:
    """Baja el documento **vivo** como .docx con la sesión del navegador. Sin descargas a mano."""
    r = ctx.request.get(f"https://docs.google.com/document/d/{doc}/export?format=docx", timeout=120000)
    if r.status != 200:
        raise SystemExit(
            f"La descarga devolvió HTTP {r.status}. Suele ser una de dos: la sesión caducó o ese\n"
            f"documento no está compartido contigo.\n"
            f"Comprueba con:  python config/gdocs/sesion_google.py estado --doc {doc}"
        )
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(r.body())
    return destino


def texto_como_lo_busca_ctrl_f(ruta: Path) -> list[str]:
    """Los trozos de texto que el editor PINTA, párrafo por párrafo. No es lo mismo que `parrafos_docx`.

    `parrafos_docx` recorre el `.docx` con python-docx y solo mira párrafos y tablas; la **tabla de
    contenido** que exporta Google va envuelta en un `w:sdt` y se la salta. Ctrl+F sí la ve, y esto
    costó un comentario mal puesto: la cita «Interpretación Técnica de Hallazgos» parecía única, pero
    en el documento vivo está dos veces —en el índice y en el encabezado— y la búsqueda fue al índice.

    Así que para contar apariciones se lee el XML en crudo y se saca todo `w:t`, que es exactamente lo
    que el lector ve. Se corta en cada fin de párrafo para no casar citas que cruzan un salto, que
    Ctrl+F tampoco cruza.
    """
    import zipfile

    xml = zipfile.ZipFile(ruta).read("word/document.xml").decode("utf-8", "replace")
    trozos = []
    for bloque in xml.replace("</w:p>", "</w:p>\x00").split("\x00"):
        t = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", bloque, re.S))
        if t.strip():
            trozos.append(html.unescape(t))
    return trozos


def titulo_de(pg, doc: str) -> str:
    """El título tal como lo ve el estudiante. Sirve para nombrar la copia local y el recibo."""
    try:
        return re.sub(r"\s*-\s*Documentos de Google\s*$", "", pg.title()).strip()
    except Exception:
        return doc


def _sanear(nombre: str) -> str:
    """Nombre de archivo válido en Windows, sin perder de vista de quién es el documento.

    Se le quita el `.docx` final si ya lo trae: los documentos que el estudiante **subió** a Drive
    conservan la extensión en el título, y sin esto el archivo local acabaría en `.docx.docx`.
    """
    nombre = re.sub(r"\.(docx?|pdf|odt)$", "", nombre.strip(), flags=re.I)
    return re.sub(r"[<>:\"/\\|?*]", "-", nombre).strip()[:110] or "documento"


# ─────────────────────────────── validar el plan ───────────────────────────────

def revisar_lenguaje(texto: str) -> list[str]:
    """Los reparos de estilo de UN comentario. Lista vacía = suena a persona hablándole a otra."""
    reparos = []
    for patron, consejo in LENGUAJE_DE_OFICIO:
        if re.search(patron, texto, re.I):
            reparos.append(consejo)
    return reparos


def validar(plan: dict, ps: list[dict], visibles: list[str], items: list[str]) -> tuple[list[str], list[str]]:
    """`(problemas, avisos)`. Con un solo problema no se publica nada; los avisos no detienen.

    Dos vistas del mismo documento, y cada una sirve para una cosa: `ps` numera los párrafos y sabe en
    qué sección va cada uno —eso es lo que se le muestra al Docente—, y `visibles` es lo que Ctrl+F
    va a encontrar de verdad, que es lo que decide si la cita sirve.
    """
    problemas: list[str] = []
    avisos: list[str] = []

    validos = {PC.norm(c): c for c in items}
    # Se busca por párrafo, no en el documento entero: es la regla 1 del encabezado.
    normalizados = [PC.norm(t) for t in visibles]

    for i, c in enumerate(plan.get("comentarios") or [], 1):
        crit = (c.get("criterio") or "").strip()
        cita = (c.get("cita") or "").strip()
        texto = (c.get("texto") or "").strip()
        etq = f"#{i}"

        if not crit:
            problemas.append(f"{etq}: sin `criterio`; sin él no se sabe de dónde salió el comentario.")
        elif PC.norm(crit) not in validos:
            problemas.append(
                f"{etq}: el criterio «{crit}» no está en la guía. La guía dice:\n      "
                + "\n      ".join(items))

        if not texto:
            problemas.append(f"{etq}: sin `texto`; un comentario vacío no se publica.")
        else:
            for r in revisar_lenguaje(texto):
                problemas.append(f"{etq}: lenguaje de oficio — {r}\n      «{texto[:80]}…»")
            if len(texto) < 40:
                avisos.append(f"{etq}: el comentario tiene {len(texto)} caracteres; costará entenderlo solo.")

        if not cita:
            problemas.append(f"{etq}: sin `cita`; sin ella el comentario no dice de qué frase habla.")
            continue

        n = PC.norm(cita)
        if len(n) < CITA_MIN:
            problemas.append(
                f"{etq}: la cita tiene {len(n)} caracteres (mínimo {CITA_MIN}). Tan corta se repite\n"
                f"      en el documento y el comentario acabaría en otra frase: «{cita}»")
        if len(n) > CITA_MAX:
            avisos.append(f"{etq}: la cita tiene {len(n)} caracteres; con anclar la frase basta.")

        veces = sum(1 for t in normalizados if n in t)
        # Ctrl+F busca LITERAL: no perdona un espacio doble ni una comilla curva cambiada. La
        # comparación normalizada sirve para explicarle el problema a quien redactó el plan, pero la
        # que decide si el comentario se va a poder publicar es esta.
        literal = sum(1 for t in visibles if cita in t)
        # Y esto es solo para enseñárselo al Docente: en qué párrafo y sección cae.
        donde = [p["n"] for p in ps if n in PC.norm(p["texto"])]

        if veces and not literal:
            problemas.append(
                f"{etq}: la cita está en el documento pero NO letra por letra, y Ctrl+F busca literal:\n"
                f"      no se publicaría. Cópiala tal cual la imprime `leer` (suele ser un espacio\n"
                f"      doble o una comilla curva). cita: «{cita[:70]}…»")
        if not veces:
            suelta = n in PC.norm(" ".join(visibles))
            problemas.append(
                f"{etq}: la cita NO está en ningún párrafo" + (
                    " —cruza un salto de párrafo, y Ctrl+F no cruza saltos: recórtala a una sola frase."
                    if suelta else ". Revisa si el estudiante ya la editó.")
                + f"\n      cita: «{cita[:90]}…»")
        elif veces > 1:
            problemas.append(
                f"{etq}: la cita aparece {veces} veces en el documento"
                + (f" (párrafos {', '.join(map(str, donde))})" if len(donde) > 1 else
                   " —la otra suele ser la tabla de contenido, que Ctrl+F también busca—")
                + ".\n      Ctrl+F iría a la primera y el comentario señalaría el sitio equivocado:\n"
                f"      alárgala hasta que sea única, o cita una frase del cuerpo en vez del encabezado.\n"
                f"      cita: «{cita[:70]}…»")
        elif donde:
            c["_parrafo"] = donde[0]
            c["_seccion"] = ps[donde[0] - 1]["seccion"]

    if not plan.get("comentarios"):
        problemas.append("El plan no tiene comentarios.")
    return problemas, avisos


def leer_plan(ruta: Path) -> dict:
    plan = json.loads(ruta.read_text(encoding="utf-8"))
    for campo in ("curso", "aca", "comentarios"):
        if not plan.get(campo):
            raise SystemExit(f"El plan no tiene «{campo}».")
    return plan


# ─────────────────────────────── publicar ───────────────────────────────

def _abrir_doc(pg, doc: str) -> None:
    pg.goto(f"https://docs.google.com/document/d/{doc}/edit",
            wait_until="domcontentloaded", timeout=120000)
    # El lienzo tarda en pintar; sin esta espera el primer Ctrl+F se pierde.
    pg.wait_for_timeout(9000)


def _foco_al_cuerpo(pg) -> None:
    """Devuelve el foco al texto. Tras publicar, el cursor se queda en la barra de comentarios.

    Se hace clic en el lienzo, que mueve el cursor pero **no escribe nada**; Ctrl+F da la vuelta al
    documento, así que da igual dónde quede el cursor.
    """
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(400)
    for sel in (".kix-canvas-tile-content", ".kix-appview-editor", ".kix-page-paginated"):
        try:
            pg.locator(sel).first.click(timeout=4000)
            pg.wait_for_timeout(600)
            return
        except Exception:
            continue


def _seleccionar(pg, cita: str) -> None:
    """Ctrl+F → cita → Enter → Escape. Al cerrar el buscador la selección queda en la coincidencia."""
    pg.keyboard.press("Control+f")
    pg.wait_for_timeout(1200)
    pg.keyboard.type(cita, delay=6)
    pg.wait_for_timeout(1600)
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(1200)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(1200)


def _comentar(pg, texto: str) -> None:
    pg.keyboard.press("Control+Alt+m")
    pg.wait_for_timeout(2600)
    pg.keyboard.type(texto, delay=5)
    pg.wait_for_timeout(900)
    pg.keyboard.press("Control+Enter")
    pg.wait_for_timeout(3000)


def comentarios_publicados(ctx, doc: str) -> list[dict]:
    """Lo que hay AHORA en el documento, leído del .docx exportado: `[{texto, ancla}]`.

    Es la única comprobación que no se cree a sí misma: no mira la pantalla, mira el archivo.
    """
    import io
    import zipfile

    r = ctx.request.get(f"https://docs.google.com/document/d/{doc}/export?format=docx", timeout=120000)
    if r.status != 200:
        return []
    z = zipfile.ZipFile(io.BytesIO(r.body()))
    nombres = z.namelist()
    if "word/comments.xml" not in nombres:
        return []

    def plano(x: str) -> str:
        """Texto legible de un trozo de XML.

        `unescape` va DESPUÉS de quitar las etiquetas, igual que en `hilos_publicados`: al revés, un
        «&lt;b&gt;» del texto del estudiante se convertiría en `<b>` y la siguiente pasada se lo
        comería como si fuera etiqueta.

        Sin este `unescape` la comprobación del ancla daba **falso fallo** en cuanto la cita llevaba
        un `<`, un `>` o un `&`: el 02/09/2026 un comentario anclado a un diagrama de flechas
        —«[Control 100% Manual] ──> […]»— se reportó como «quedó anclado a otra cosa» porque el
        `.docx` devuelve `──&gt;`. El ancla era correcta. Un falso fallo es peor que ninguno: manda
        a mirar a mano un problema que no existe, y a la tercera vez ya nadie mira.
        """
        return html.unescape(" ".join(re.sub(r"<[^>]+>", " ", x).split()))

    xml = z.read("word/comments.xml").decode("utf-8", "replace")
    cuerpo = z.read("word/document.xml").decode("utf-8", "replace")

    # El id del comentario une las dos mitades: el texto está en comments.xml y el ancla, en el cuerpo.
    anclas: dict[str, str] = {}
    for m in re.finditer(r'<w:commentRangeStart[^>]*w:id="(\d+)"[^>]*/>(.*?)<w:commentRangeEnd[^>]*w:id="\1"',
                         cuerpo, re.S):
        anclas[m.group(1)] = plano(m.group(2))

    salida = []
    for m in re.finditer(r'<w:comment\b[^>]*w:id="(\d+)"[^>]*>(.*?)</w:comment>', xml, re.S):
        salida.append({"id": m.group(1), "texto": plano(m.group(2)), "ancla": anclas.get(m.group(1), "")})
    return salida


def hilos_publicados(ctx, doc: str) -> list[dict]:
    """Los comentarios AGRUPADOS EN HILOS, con autor, fecha y si están resueltos.

    Para qué: cuando el estudiante contesta, su respuesta entra en el mismo hilo. Sin agrupar no
    se distingue «le dije once cosas» de «me contestó cuatro».

    Cómo se agrupa, y por qué así. Google exporta cada mensaje —el original y cada respuesta— como
    un `<w:comment>` propio, y **no** rellena `w15:paraIdParent`, que es donde Word guardaría de
    quién cuelga cada respuesta (comprobado: los `commentEx` salen solo con `paraId` y `done`). Lo
    único que comparten los mensajes de un mismo hilo es el **tramo anclado**: sus
    `commentRangeStart`/`End` cubren exactamente el mismo texto. Así que el hilo se reconstruye por
    la posición del ancla en el cuerpo, no por un identificador de padre que aquí no viene.

    `resuelto` sale de `w15:done` en `commentsExtended.xml`; si esa parte no está, queda en None y
    se dice «no consta», que no es lo mismo que «sin resolver».
    """
    import io
    import zipfile

    r = ctx.request.get(f"https://docs.google.com/document/d/{doc}/export?format=docx", timeout=120000)
    if r.status != 200:
        return []
    z = zipfile.ZipFile(io.BytesIO(r.body()))
    if "word/comments.xml" not in z.namelist():
        return []

    def plano(x: str) -> str:
        # `unescape` va DESPUÉS de quitar las etiquetas: al revés, un «&lt;b&gt;» del texto del
        # estudiante se convertiría en una etiqueta y la siguiente pasada se lo comería.
        return html.unescape(" ".join(re.sub(r"<[^>]+>", " ", x).split()))

    xml = z.read("word/comments.xml").decode("utf-8", "replace")
    cuerpo = z.read("word/document.xml").decode("utf-8", "replace")

    # Tramo anclado y posición, por id. La posición ordena los hilos como se leen en el documento.
    tramo: dict[str, tuple[int, str]] = {}
    for m in re.finditer(r'<w:commentRangeStart[^>]*w:id="(\d+)"[^>]*/>(.*?)<w:commentRangeEnd[^>]*w:id="\1"',
                         cuerpo, re.S):
        tramo[m.group(1)] = (m.start(), plano(m.group(2)))

    # ¿Resuelto? Va por paraId, que es el del párrafo del mensaje dentro de comments.xml.
    hecho: dict[str, bool] = {}
    if "word/commentsExtended.xml" in z.namelist():
        ext = z.read("word/commentsExtended.xml").decode("utf-8", "replace")
        for m in re.finditer(r'<w15:commentEx[^>]*w15:paraId="([0-9A-Fa-f]+)"[^>]*>', ext):
            hecho[m.group(1).upper()] = 'w15:done="1"' in m.group(0)

    mensajes = []
    for m in re.finditer(r'<w:comment\b([^>]*)w:id="(\d+)"([^>]*)>(.*?)</w:comment>', xml, re.S):
        cab, cid, cuerpo_c = m.group(1) + m.group(3), m.group(2), m.group(4)
        autor = (re.search(r'w:author="([^"]*)"', cab) or [None, ""])[1]
        fecha = (re.search(r'w:date="([^"]*)"', cab) or [None, ""])[1]
        pid = (re.search(r'w14:paraId="([0-9A-Fa-f]+)"', cuerpo_c) or [None, ""])[1].upper()
        pos, ancla = tramo.get(cid, (10 ** 9, ""))
        mensajes.append({"id": cid, "autor": autor, "fecha": fecha[:16].replace("T", " "),
                         "texto": plano(cuerpo_c), "ancla": ancla, "_pos": pos,
                         "resuelto": hecho.get(pid)})

    hilos: dict[tuple, dict] = {}
    for x in sorted(mensajes, key=lambda y: (y["_pos"], int(y["id"]))):
        clave = (x["_pos"], x["ancla"])
        h = hilos.setdefault(clave, {"ancla": x["ancla"], "pos": x["_pos"], "mensajes": []})
        h["mensajes"].append({k: v for k, v in x.items() if k != "_pos"})
    return [hilos[k] for k in sorted(hilos)]


def publicar(pg, ctx, doc: str, plan: dict) -> tuple[list[dict], list[str]]:
    """Publica los comentarios uno a uno y comprueba el resultado contra el documento exportado."""
    antes = {c["texto"] for c in comentarios_publicados(ctx, doc)}
    _abrir_doc(pg, doc)
    fallos: list[str] = []

    for i, c in enumerate(plan["comentarios"], 1):
        cita, texto = c["cita"].strip(), c["texto"].strip()
        print(f"  [{i}/{len(plan['comentarios'])}] «{cita[:58]}…»", flush=True)
        try:
            if i > 1:
                _foco_al_cuerpo(pg)
            _seleccionar(pg, cita)
            _comentar(pg, texto)
        except Exception as e:
            fallos.append(f"#{i}: {str(e).splitlines()[0][:120]}")

    ahora = comentarios_publicados(ctx, doc)
    nuevos = [c for c in ahora if c["texto"] not in antes]

    # Que el comentario exista no basta: tiene que haber quedado anclado a SU cita, y **exactamente**
    # a ella. Pedir que el ancla «contenga» la cita no sirve: así se colaba un comentario que Ctrl+F
    # había puesto sobre la entrada de la tabla de contenido, cuyo texto también contiene la cita.
    for i, c in enumerate(plan["comentarios"], 1):
        esperado = PC.norm(c["texto"].strip())
        igual = [n for n in nuevos if PC.norm(n["texto"]) == esperado]
        if not igual:
            fallos.append(f"#{i}: no quedó publicado («{c['texto'][:60]}…»)")
        elif PC.norm(igual[0]["ancla"]) != PC.norm(c["cita"].strip()):
            fallos.append(
                f"#{i}: quedó anclado a otra cosa.\n      esperaba: «{c['cita'][:70]}…»"
                f"\n      quedó en: «{igual[0]['ancla'][:70]}…»")
    return nuevos, fallos


def copiar(pg, doc: str) -> str:
    """Hace una copia del documento en el Drive del Docente y devuelve su id. Para `ensayar`."""
    pg.goto(f"https://docs.google.com/document/d/{doc}/copy",
            wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(3500)
    # Hay que pedir el BOTÓN por su rol: el diálogo repite «hacer una copia» en la pregunta, y un
    # selector por texto acaba pulsando el párrafo, que no hace nada.
    try:
        pg.get_by_role("button", name=re.compile("copia|copy", re.I)).first.click(timeout=10000)
    except Exception as e:
        raise SystemExit(f"No pude pulsar «Hacer una copia»: {str(e).splitlines()[0][:110]}")
    for _ in range(30):
        pg.wait_for_timeout(2000)
        for cand in pg.context.pages:
            m = re.search(r"/document/d/([\w-]+)", cand.url)
            if m and m.group(1) != doc:
                return m.group(1)
    raise SystemExit("La copia no llegó a abrirse. Vuelve a intentarlo.")


# El panel de comentarios, tal como es de verdad (comprobado sobre el DOM el 22/08/2026). Nada de
# esto se adivina: `div[role='article']` y `.docos-docoview-tesla-conflict-parent`, que es lo que uno
# esperaría, **no existen** en Google Docs y el clic se queda esperando hasta que expira.
HILO = "div[role='listitem'].docos-anchoreddocoview"
DESPLEGABLE = ".docos-docomenu-dropdown"          # el «Más opciones» de cada hilo
VISIBLE = ".goog-menuitem:visible, [role='menuitem']:visible"
BORRAR_EXACTO = re.compile(r"^(eliminar|borrar|delete)$", re.I)


def borrar(pg, doc: str, comentarios: list[dict]) -> tuple[int, list[tuple[str, str]]]:
    """Borra los comentarios de `comentarios` (`{"cita","texto"}`). `(borrados, [(texto, motivo)])`.

    El camino no es el que parece. Lo natural sería buscar el hilo en el panel y desplazarse hasta
    él, y **eso no funciona**: el hilo se posiciona a la altura de su ancla, que en un documento de
    44 páginas está a `y≈45000`, y `scroll_into_view_if_needed` expira en la mayoría de los hilos
    porque el panel es una capa superpuesta sin desplazamiento propio. Probado: así se borran tres de
    once y los otros ocho fallan todos con el mismo mensaje.

    Lo que sí funciona es **llegar por el documento**, con el mismo Ctrl+F con el que se publica: al
    seleccionar la cita, el editor se desplaza hasta ahí y el hilo de ese trozo queda en pantalla y
    activo. Por eso el recibo guarda la cita además del texto.

    Y se recarga entre borrado y borrado, que son diez segundos por comentario: al borrar un hilo el
    panel reposiciona los demás y los localizadores vivos apuntan a huecos. Deshacer es una operación
    rara —el camino normal es `ensayar` y luego publicar—, así que prefiero tardar dos minutos a
    dejar el trabajo a medias.

    El otro detalle, que no se ve en el código si no se dice: tanto el menú como la confirmación se
    acotan a lo **visible**, y la confirmación además al diálogo. En el DOM hay varios «Eliminar»
    escondidos (los menús de la barra, para empezar), y al clicar uno de esos el diálogo se cierra
    sin borrar nada: parece que funcionó y no funcionó.
    """
    borrados, fallos = 0, []
    for i, c in enumerate(comentarios):
        t, cita = c["texto"], (c.get("cita") or "").strip()
        corto = t.strip()[:60]
        try:
            if i:
                _abrir_doc(pg, doc)
            if cita:                       # trae el hilo a la pantalla y lo deja activo
                _foco_al_cuerpo(pg)
                _seleccionar(pg, cita)
                pg.wait_for_timeout(1200)
            hilo = pg.locator(HILO).filter(has_text=corto).first
            if not hilo.count():
                fallos.append((t, "no está en el panel"))
                continue
            hilo.click(timeout=8000)      # activa el hilo: sin esto el menú no tiene caja
            pg.wait_for_timeout(1200)
            drop = hilo.locator(DESPLEGABLE).first
            drop.click(timeout=8000)
            pg.wait_for_timeout(1200)
            pg.locator(VISIBLE).filter(has_text=BORRAR_EXACTO).first.click(timeout=8000)
            pg.wait_for_timeout(1500)
            try:  # No todas las versiones piden confirmación; si la piden, es un role=dialog.
                pg.get_by_role("dialog").locator("[role='button']:visible, button:visible").filter(
                    has_text=BORRAR_EXACTO).last.click(timeout=6000)
            except Exception:
                pass
            pg.wait_for_timeout(2500)
            borrados += 1
        except Exception as e:
            fallos.append((t, str(e).splitlines()[0][:90]))
    return borrados, fallos


# ─────────────────────────────── el recibo ───────────────────────────────

def ruta_recibo(doc: str) -> Path:
    return REVISIONES / f"{doc}.publicados.json"


def guardar_recibo(doc: str, plan: dict, nuevos: list[dict], titulo: str) -> Path:
    """Deja constancia de lo publicado, para poder deshacerlo sin marcar los comentarios.

    El comentario no lleva ninguna seña de que lo escribió un programa —el estudiante lee prosa, no
    etiquetas—, así que `deshacer` necesita saber de fuera qué se escribió.
    """
    r = ruta_recibo(doc)
    r.parent.mkdir(parents=True, exist_ok=True)
    r.write_text(json.dumps({
        "docId": doc, "titulo": titulo, "curso": plan["curso"], "aca": plan["aca"],
        "comentarios": [{"cita": c["cita"], "texto": c["texto"]} for c in plan["comentarios"]],
        "publicados": nuevos,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return r


# ─────────────────────────────── órdenes ───────────────────────────────

def orden_leer(a) -> int:
    doc = doc_id(a.doc)
    guia, items = CA.criterios(a.curso, a.aca)
    p, ctx, pg = SG.abrir(headless=True)
    try:
        if not SG.sesion_viva(pg, doc_id=doc):
            raise SystemExit(f"No hay acceso a {doc}. Corre:  python config/gdocs/sesion_google.py login")
        titulo = titulo_de(pg, doc)
        destino = descargar(ctx, doc, REVISIONES / f"{_sanear(titulo)}.docx")
    finally:
        SG.cerrar(p, ctx)

    ps = PC.parrafos_docx(destino)
    print(f"Documento : {titulo}")
    print(f"            https://docs.google.com/document/d/{doc}/edit")
    print(f"Copia     : {destino.relative_to(REPO)}   (no entra en git)")
    print(f"Guía      : {guia}")
    print(f"Párrafos  : {len(ps)}\n")
    # El Syllabus y los criterios responden a dos preguntas distintas y las dos hacen falta: la guía
    # dice qué se le pidió en esta entrega, el Syllabus qué enseña la asignatura. Ver `syllabus_curso`.
    print("─── la asignatura, según su Syllabus ───")
    for linea in SY.resumen(a.curso):
        print("  " + linea)
    print("\n─── criterios con los que se comenta ───")
    for i, c in enumerate(items, 1):
        print(f"  {i}. {c}")
    print("\n─── documento ───")
    for x in ps:
        sec = f"({x['seccion'][:38]}) " if x["seccion"] else ""
        print(f"[{x['n']:>3}] {sec}{x['texto']}")
    return 0


def _preparar(a) -> tuple[str, dict, list[dict], str, list[str]]:
    """Lo común a simular/ensayar/comentar: bajar el documento vivo y validar el plan contra él."""
    doc = doc_id(a.doc)
    plan = leer_plan(Path(a.plan))
    if plan.get("docId") and doc_id(plan["docId"]) != doc:
        raise SystemExit(
            f"El plan es de otro documento.\n  plan: {doc_id(plan['docId'])}\n  pedido: {doc}")
    guia, items = CA.criterios(plan["curso"], plan["aca"])

    p, ctx, pg = SG.abrir(headless=True)
    try:
        if not SG.sesion_viva(pg, doc_id=doc):
            raise SystemExit(f"No hay acceso a {doc}. Corre:  python config/gdocs/sesion_google.py login")
        titulo = titulo_de(pg, doc)
        # Se valida contra el documento VIVO, no contra lo que se bajó ayer: el estudiante sigue
        # editando, y una cita que ya borró no se puede comentar.
        destino = descargar(ctx, doc, REVISIONES / f"{_sanear(titulo)}.docx")
    finally:
        SG.cerrar(p, ctx)

    ps = PC.parrafos_docx(destino)
    problemas, avisos = validar(plan, ps, texto_como_lo_busca_ctrl_f(destino), items)
    return doc, plan, ps, titulo, [guia, problemas, avisos]


def orden_simular(a) -> int:
    doc, plan, ps, titulo, (guia, problemas, avisos) = _preparar(a)
    print(f"Documento : {titulo}   ({len(ps)} párrafos)")
    print(f"Curso     : {plan['curso']} · {guia}")
    print(f"Plan      : {len(plan['comentarios'])} comentarios\n")

    for i, c in enumerate(plan["comentarios"], 1):
        sec = c.get("_seccion") or "?"
        par = c.get("_parrafo")
        print(f"─── {i}. {sec[:60]}" + (f"  ·  párrafo {par}" if par else ""))
        print(f"    ancla   : «{c.get('cita', '')[:100]}»")
        print(f"    comenta : {c.get('texto', '')}")
        print(f"    (criterio, no se publica: {c.get('criterio', '')})\n")

    for x in avisos:
        print("  ~ " + x)
    if problemas:
        print(f"\nNO se publica nada — {len(problemas)} problema(s):\n")
        for x in problemas:
            print("  ✗ " + x)
        return 1
    print(f"\nOK  el plan cuadra con el documento: {len(plan['comentarios'])} citas, todas únicas y "
          f"dentro de un párrafo.")
    print("    Ahora ensáyalo en una copia:")
    print(f'    python config/gdocs/comentar_docs.py ensayar --doc {doc} --plan "{a.plan}"')
    return 0


def orden_ensayar(a) -> int:
    doc, plan, ps, titulo, (guia, problemas, avisos) = _preparar(a)
    if problemas:
        print(f"NO se ensaya — el plan tiene {len(problemas)} problema(s). Corre `simular` y arréglalos.")
        for x in problemas:
            print("  ✗ " + x)
        return 1

    p, ctx, pg = SG.abrir(headless=a.headless)
    try:
        print(f"Copiando «{titulo}» a tu Drive…")
        copia = copiar(pg, doc)
        print(f"Copia: https://docs.google.com/document/d/{copia}/edit\n")
        print(f"Publicando {len(plan['comentarios'])} comentarios EN LA COPIA:")
        nuevos, fallos = publicar(pg, ctx, copia, plan)
    finally:
        SG.cerrar(p, ctx)

    print(f"\n{len(nuevos)} comentarios en la copia.")
    for c in nuevos:
        print(f"  · «{c['ancla'][:60]}…»  →  {c['texto'][:70]}")
    if fallos:
        print(f"\n{len(fallos)} fallo(s):")
        for x in fallos:
            print("  ✗ " + x)
        return 1
    print(f"\nOK  ensayo limpio. Ábrelo, léelo con tus ojos, y si te convence:")
    print(f'    python config/gdocs/comentar_docs.py comentar --doc {doc} --plan "{a.plan}" --confirmar')
    print(f"    La copia es tuya y puedes mandarla a la papelera:")
    print(f"    https://docs.google.com/document/d/{copia}/edit")
    return 0


def orden_comentar(a) -> int:
    doc, plan, ps, titulo, (guia, problemas, avisos) = _preparar(a)
    if problemas:
        print(f"NO se publica nada — {len(problemas)} problema(s). Corre `simular`.")
        for x in problemas:
            print("  ✗ " + x)
        return 1
    if not a.confirmar:
        print(f"Esto publicaría {len(plan['comentarios'])} comentarios en «{titulo}», que el "
              f"estudiante ve al instante.")
        print("Falta --confirmar. Antes, si no lo has hecho:  ensayar")
        return 1

    p, ctx, pg = SG.abrir(headless=a.headless)
    try:
        print(f"Publicando en «{titulo}» — el documento del estudiante:")
        nuevos, fallos = publicar(pg, ctx, doc, plan)
    finally:
        SG.cerrar(p, ctx)

    recibo = guardar_recibo(doc, plan, nuevos, titulo)
    print(f"\n{len(nuevos)} comentarios publicados y comprobados en el documento exportado.")
    for c in nuevos:
        print(f"  · «{c['ancla'][:60]}…»  →  {c['texto'][:70]}")
    print(f"\nRecibo: {recibo.relative_to(REPO)}")
    if fallos:
        print(f"\n{len(fallos)} fallo(s) — revisa el documento a mano:")
        for x in fallos:
            print("  ✗ " + x)
        return 1
    print(f"Si algo no te gusta:  python config/gdocs/comentar_docs.py deshacer --doc {doc}")
    return 0


def orden_deshacer(a) -> int:
    doc = doc_id(a.doc)
    r = ruta_recibo(doc)
    if not r.is_file():
        raise SystemExit(
            f"No hay recibo de {doc} en {r.parent.relative_to(REPO)}.\n"
            "Sin él no sé cuáles comentarios escribí yo y cuáles son de otra persona: bórralos a mano.")
    recibo = json.loads(r.read_text(encoding="utf-8"))
    cs = recibo["comentarios"]
    textos = [c["texto"] for c in cs]
    print(f"Documento : {recibo.get('titulo', doc)}")
    print(f"Borraría  : {len(textos)} comentarios\n")
    for t in textos:
        print(f"  · {t[:90]}")
    if not a.confirmar:
        print("\nFalta --confirmar.")
        return 1

    p, ctx, pg = SG.abrir(headless=a.headless)
    try:
        _abrir_doc(pg, doc)
        borrados, fallos = borrar(pg, doc, cs)
        quedan = {PC.norm(c["texto"]) for c in comentarios_publicados(ctx, doc)}
    finally:
        SG.cerrar(p, ctx)

    # Manda la exportación, no la cuenta de clics. Un fallo cuyo comentario ya no está no es un
    # fallo —el hilo pudo borrarse antes, a mano— y sacarlo por pantalla solo asusta.
    sobrevivientes = [t for t in textos if PC.norm(t) in quedan]
    motivos = {t: m for t, m in fallos if PC.norm(t) in quedan}
    print(f"\n{borrados} borrados de {len(textos)}.")
    if sobrevivientes:
        print(f"{len(sobrevivientes)} siguen ahí — bórralos a mano:")
        for t in sobrevivientes:
            print("  ✗ " + t[:90] + (f"\n      {motivos[t]}" if t in motivos else ""))
        return 1
    if fallos:
        print(f"({len(fallos)} no estaban en el panel; ya no estaban en el documento.)")
    r.unlink()
    print("OK  no queda ninguno, y borré el recibo.")
    return 0


def orden_conversacion(a) -> int:
    """Lee lo que hay en el documento y, sobre todo, **qué contestó el estudiante**.

    No publica, no borra, no abre ventana: solo exporta y lee. Es la vuelta que faltaba —hasta
    ahora el proceso sabía hablar pero no escuchar—, y sirve igual para ver qué feedback trae ya un
    documento antes de añadir el propio.
    """
    doc = doc_id(a.doc)
    p, ctx, pg = SG.abrir(headless=True)
    try:
        hilos = hilos_publicados(ctx, doc)
    finally:
        SG.cerrar(p, ctx)

    if not hilos:
        print(f"El documento {doc} no tiene ningún comentario.")
        return 0

    # Cuáles escribí yo: manda el recibo, que es lo único que lo sabe con certeza. Si no hay,
    # se cae al nombre del autor, que en las exportaciones de plantilla sale como «Autor».
    rec = ruta_recibo(doc)
    mios = set()
    if rec.is_file():
        try:
            mios = {PC.norm(c["texto"]) for c in json.loads(rec.read_text(encoding="utf-8"))["comentarios"]}
        except Exception:
            pass

    autores: dict[str, int] = {}
    for h in hilos:
        for m in h["mensajes"]:
            autores[m["autor"] or "(sin autor)"] = autores.get(m["autor"] or "(sin autor)", 0) + 1

    n_msg = sum(len(h["mensajes"]) for h in hilos)
    print(f"Documento : {doc}")
    print(f"Hilos     : {len(hilos)}   ·   mensajes: {n_msg}")
    print("Autores   : " + " · ".join(f"{k} ({v})" for k, v in sorted(autores.items(), key=lambda x: -x[1])))
    if rec.is_file():
        print(f"Recibo    : {rec.name} — {len(mios)} comentarios míos registrados")
    else:
        print("Recibo    : no hay, así que «mío» se deduce del autor y puede fallar")
    print()

    con_respuesta = []
    for i, h in enumerate(hilos, 1):
        marca = {True: "resuelto", False: "sin resolver", None: "no consta"}[h["mensajes"][0]["resuelto"]]
        print(f"─── hilo {i}  ·  {marca}")
        print(f"    ancla : «{(h['ancla'] or '(sin ancla)')[:96]}»")
        for j, m in enumerate(h["mensajes"]):
            quien = "TÚ" if (PC.norm(m["texto"]) in mios) else (m["autor"] or "?")
            flecha = "   " if j == 0 else "  ↳"
            print(f"{flecha} [{quien} · {m['fecha']}] {m['texto'][:150]}")
        # Hay respuesta cuando el hilo tiene más de un mensaje y el último no es mío.
        if len(h["mensajes"]) > 1 and PC.norm(h["mensajes"][-1]["texto"]) not in mios:
            con_respuesta.append(i)
        print()

    if mios:
        sin_contestar = [i for i, h in enumerate(hilos, 1)
                         if any(PC.norm(m["texto"]) in mios for m in h["mensajes"])
                         and i not in con_respuesta]
        print(f"Te contestó en {len(con_respuesta)} hilo(s): {con_respuesta or '—'}")
        print(f"Siguen sin respuesta: {len(sin_contestar)} de los tuyos")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Comentar el documento de un estudiante como lo harías tú, con el navegador.",
        epilog="Orden de uso:  leer → (redactar el plan) → simular → ensayar → comentar --confirmar",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def comunes(p, plan=True, confirmar=False):
        p.add_argument("--doc", required=True, help="el enlace que te compartieron, o el id")
        if plan:
            p.add_argument("--plan", required=True, help="el .json con los comentarios")
        p.add_argument("--headless", action="store_true",
                       help="sin ventana; Docs es una aplicación de lienzo y va mejor con ventana")
        if confirmar:
            p.add_argument("--confirmar", action="store_true")

    p = sub.add_parser("leer", help="bajar el documento vivo y volcarlo numerado con los criterios")
    p.add_argument("--doc", required=True)
    p.add_argument("--curso", required=True, choices=sorted(CA.CURSOS))
    p.add_argument("--aca", required=True, help="aca1 · acafinal (pregrado solo tiene acafinal)")

    comunes(sub.add_parser("simular", help="validar el plan contra el documento vivo. SIEMPRE primero"))
    comunes(sub.add_parser("ensayar", help="publicar de verdad, pero en una copia en tu Drive"))
    comunes(sub.add_parser("comentar", help="publicar en el documento del estudiante"), confirmar=True)

    p = sub.add_parser("deshacer", help="borrar los comentarios de la última publicación")
    comunes(p, plan=False, confirmar=True)

    p = sub.add_parser("conversacion", help="leer los hilos y ver qué contestó el estudiante")
    p.add_argument("--doc", required=True, help="el enlace que te compartieron, o el id")

    a = ap.parse_args()
    return {"leer": orden_leer, "simular": orden_simular, "ensayar": orden_ensayar,
            "comentar": orden_comentar, "deshacer": orden_deshacer,
            "conversacion": orden_conversacion}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
