# -*- coding: utf-8 -*-
"""Cliente de **CDigital** — el Moodle de la CUN (https://cdigital.cun.edu.co).

Sirve para poner contenido evaluativo en las aulas sin hacerlo a mano: importa bancos de
preguntas en Moodle XML y crea las actividades de cuestionario **ocultas**, para que el docente
las revise y las active cuando quiera.

POR QUÉ ASÍ
-----------
Moodle no expone la autoría de preguntas por servicios web: `mod_quiz_*` sirve para *resolver*
cuestionarios, no para crearlos, y no existe un `core_question_create`. El camino real es el mismo
que usa la interfaz: subir el archivo al área de borradores y enviar el formulario de importación.
Eso es lo que hace este módulo, con `requests` y sin navegador.

CREDENCIALES
------------
Se leen de ``%LOCALAPPDATA%\\cdigital-cun\\credenciales.json``, **fuera de este repositorio**, que
está en git y sincronizado a Google Drive. Nunca escribas usuario ni clave en un archivo de aquí.
Formato del archivo::

    {"url": "https://cdigital.cun.edu.co", "usuario": "...", "clave": "..."}

USO
---
    python config/moodle/cdigital.py estado
    python config/moodle/cdigital.py curso 115463
    python config/moodle/cdigital.py importar "ruta/al/banco.xml" --curso 115463 --simular
    python config/moodle/cdigital.py importar "ruta/al/banco.xml" --curso 115463
    python config/moodle/cdigital.py preguntas --curso 115463
    python config/moodle/cdigital.py quiz 6745720
    python config/moodle/cdigital.py quiz-sustituir 6745720 --categoria 4976278,8271261
    python config/moodle/cdigital.py quiz-sustituir 6745720 --categoria 4976278,8271261 --confirmar
    python config/moodle/cdigital.py subir-recurso "Material U2.docx" --curso 115463 --seccion 2
    python config/moodle/cdigital.py subir-recurso "Material U2.docx" --curso 115463 --confirmar
    python config/moodle/cdigital.py ocultar 6745720
    python config/moodle/cdigital.py mostrar 6745720

``--simular`` valida el XML y muestra qué haría, sin tocar el aula. **Úsalo siempre primero**: estos
cursos tienen estudiantes matriculados. `quiz-sustituir` y `subir-recurso` sin `--confirmar` tampoco
tocan nada.

ALISTAMIENTO DEL AULA
---------------------
Así se llama el proceso completo: dejar el material y las evaluaciones **puestos en CDigital pero
ocultos**, listos para que el Docente los revise a mano y los active. Por eso `subir-recurso` crea
el recurso oculto salvo que se pida `--visible`, y por eso `quiz-sustituir` deja el cuestionario
oculto si algo falla: es preferible invisible que roto.

LAS AULAS VIENEN CON CUESTIONARIOS DE PLANTILLA
-----------------------------------------------
Cada aula de la CUN se crea desde una plantilla (`plantilla_cero` / `PEE26042019`) que ya trae
**seis cuestionarios visibles y abiertos** —Quiz 1, Parcial 1, Quiz 2, Parcial 2, Autoevaluación,
Quiz 3— y **cada uno ya tiene 10 slots aleatorios** que sacan preguntas de su propia categoría
«Por defecto en <nombre del quiz>», heredada de la plantilla. Importar el banco NO cambia eso:
la importación deja las preguntas en una categoría del **contexto del curso**, y los slots siguen
apuntando al **contexto del módulo**. Hay que sustituir los slots — eso hace `quiz-sustituir`.
"""
from __future__ import annotations

import argparse
import html
import io
import json
import os
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET

import requests

# La consola de Windows es cp1252 y los nombres de las preguntas llevan tildes, flechas y «·».
# Sin esto, un simple print revienta con UnicodeEncodeError a mitad de un informe.
# `reconfigure` y no envolver en TextIOWrapper: envolver dos veces cierra el buffer de quien
# ya lo hubiera envuelto (un script que importe este módulo).
for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

ARCHIVO_CRED = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
                            "cdigital-cun", "credenciales.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36")
REPO_SUBIDA = 5  # id del repositorio "Subir un archivo" en esta instalación


# =============================================================================================
# Sesión
# =============================================================================================
class CDigital:
    def __init__(self) -> None:
        if not os.path.isfile(ARCHIVO_CRED):
            raise SystemExit(
                f"No hay credenciales en {ARCHIVO_CRED}\n"
                'Crea el archivo con {"url": "...", "usuario": "...", "clave": "..."}.\n'
                "No lo pongas dentro del repositorio: está en git y sincronizado a Drive."
            )
        cred = json.load(open(ARCHIVO_CRED, encoding="utf-8"))
        self.base = cred["url"].rstrip("/")
        self._cred = cred
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.sesskey: str | None = None
        self.uid: str | None = None

    def entrar(self) -> None:
        r = self.s.get(f"{self.base}/login/index.php", timeout=60)
        tok = re.search(r'name="logintoken"\s+value="([^"]+)"', r.text)
        datos = {"username": self._cred["usuario"], "password": self._cred["clave"]}
        if tok:
            datos["logintoken"] = tok.group(1)
        r = self.s.post(f"{self.base}/login/index.php", data=datos, timeout=60)
        m = re.search(r'"sesskey":"([^"]+)"', r.text)
        if not m:
            raise SystemExit("Inicio de sesión fallido: no apareció el sesskey. "
                             "Revisa usuario y clave (¿la rotaron?).")
        self.sesskey = m.group(1)
        u = re.search(r'"userId":(\d+)', r.text)
        self.uid = u.group(1) if u else None
        self.nombre = self._nombre_visible()

    def _nombre_visible(self) -> str:
        """El nombre no está en el HTML del panel; se lee del perfil."""
        try:
            h = self.get("/user/profile.php").text
        except requests.RequestException:
            return "(no pude leer el perfil)"
        for pat in (r'<h1[^>]*>\s*([^<]{3,80})\s*</h1>', r"<title>\s*([^<:]{3,80})"):
            m = re.search(pat, h)
            if m and m.group(1).strip():
                return html.unescape(m.group(1)).strip()
        return "(nombre no visible)"

    def get(self, ruta: str, **kw):
        return self.s.get(self.base + ruta if ruta.startswith("/") else ruta, timeout=90, **kw)

    def post(self, ruta: str, datos: dict, **kw):
        return self.s.post(self.base + ruta if ruta.startswith("/") else ruta,
                           data=datos, timeout=90, **kw)

    def ws(self, methodname: str, args: dict):
        """Llama un servicio web AJAX de Moodle, como lo hace la propia interfaz.

        Hace falta porque las páginas de curso de Moodle 4.5 **no traen el contenido de los temas
        en el HTML**: sólo la sección «General» viene servida, y el resto lo pinta el navegador con
        este servicio. Raspar `/course/view.php` reporta de menos: es como se llegó a creer que un
        aula con seis cuestionarios no tenía ninguno.
        """
        r = self.s.post(f"{self.base}/lib/ajax/service.php?sesskey={self.sesskey}&info={methodname}",
                        json=[{"index": 0, "methodname": methodname, "args": args}], timeout=90)
        cuerpo = r.json()[0]
        if cuerpo.get("error"):
            raise SystemExit(f"El servicio {methodname} falló: {cuerpo.get('exception') or cuerpo}")
        datos = cuerpo.get("data")
        return json.loads(datos) if isinstance(datos, str) else datos

    def estado_curso(self, curso: int) -> dict:
        """Estado real del aula: todas las secciones y módulos, incluidos los ocultos."""
        return self.ws("core_courseformat_get_state", {"courseid": curso})


# =============================================================================================
# Validación local del Moodle XML — antes de tocar el aula
# =============================================================================================
def validar_xml(ruta: str) -> dict:
    """Revisa el XML como lo revisaría Moodle, pero en local. Devuelve el informe."""
    if not os.path.isfile(ruta):
        raise SystemExit(f"No existe el archivo: {ruta}")
    try:
        arbol = ET.parse(ruta)
    except ET.ParseError as e:
        raise SystemExit(f"El XML no es válido: {e}")
    raiz = arbol.getroot()
    if raiz.tag != "quiz":
        raise SystemExit(f"La raíz debería ser <quiz> y es <{raiz.tag}>.")

    informe = {"archivo": ruta, "categoria": None, "preguntas": [], "problemas": []}
    for q in raiz.findall("question"):
        tipo = q.get("type")
        if tipo == "category":
            nodo = q.find("category/text")
            informe["categoria"] = nodo.text.strip() if nodo is not None and nodo.text else None
            continue
        nombre_nodo = q.find("name/text")
        nombre = (nombre_nodo.text or "").strip() if nombre_nodo is not None else "(sin nombre)"
        ficha = {"tipo": tipo, "nombre": nombre}
        if tipo == "multichoice":
            respuestas = q.findall("answer")
            correctas = [a for a in respuestas if _fraccion(a) > 0]
            ficha["opciones"] = len(respuestas)
            ficha["correctas"] = len(correctas)
            ficha["suma_fracciones"] = round(sum(_fraccion(a) for a in correctas), 4)
            single = (q.findtext("single") or "").strip().lower()
            ficha["single"] = single
            if len(respuestas) < 2:
                informe["problemas"].append(f"«{nombre}»: tiene {len(respuestas)} opciones.")
            if single == "true" and len(correctas) != 1:
                informe["problemas"].append(
                    f"«{nombre}»: single=true pero hay {len(correctas)} opciones con puntaje > 0.")
            if correctas and abs(ficha["suma_fracciones"] - 100) > 0.05 and single == "true":
                informe["problemas"].append(
                    f"«{nombre}»: la opción correcta suma {ficha['suma_fracciones']} y debería ser 100.")
            sin_texto = [i for i, a in enumerate(respuestas, 1)
                         if not (a.findtext("text") or "").strip()]
            if sin_texto:
                informe["problemas"].append(f"«{nombre}»: opciones vacías en {sin_texto}.")
        informe["preguntas"].append(ficha)

    if informe["categoria"] is None:
        informe["problemas"].append(
            "No hay <question type=\"category\">: las preguntas caerían en la categoría que se "
            "elija en el formulario, no en una propia.")
    if not informe["preguntas"]:
        informe["problemas"].append("El archivo no contiene ninguna pregunta.")
    return informe


def _fraccion(nodo_answer) -> float:
    try:
        return float(nodo_answer.get("fraction") or 0)
    except ValueError:
        return 0.0


# =============================================================================================
# Importación
# =============================================================================================
def _inputs(h: str) -> dict:
    """name -> value de todos los <input> ocultos y de texto.

    No se puede buscar 'name="x" value="y"' con una expresión posicional: Moodle intercala
    atributos (`newfile` lleva `id="id_newfile"` en medio) y a veces invierte el orden.
    """
    campos: dict[str, str] = {}
    for m in re.finditer(r"<input\b[^>]*>", h):
        tag = m.group(0)
        n = re.search(r'\bname="([^"]+)"', tag)
        if not n or n.group(1) in campos:
            continue
        t = re.search(r'\btype="([^"]+)"', tag)
        if t and t.group(1) not in ("hidden", "text"):
            continue
        v = re.search(r'\bvalue="([^"]*)"', tag)
        campos[n.group(1)] = html.unescape(v.group(1)) if v else ""
    return campos


def _campos_import(h: str) -> dict:
    """Extrae del formulario los valores que cambian en cada carga de página."""
    campos = _inputs(h)
    faltan = [k for k in ("sesskey", "context", "newfile") if not campos.get(k)]
    if faltan:
        raise SystemExit(
            f"El formulario de importación no trajo: {', '.join(faltan)}.\n"
            "O la sesión no tiene permiso de edición en este aula, o Moodle cambió de versión.")

    cats = [(v, html.unescape(t).strip()) for v, t in
            re.findall(r'<option[^>]*value="(\d+,\d+)"[^>]*>([^<]{0,120})', h)]
    autor = next((a for a in re.findall(r'"author":"([^"]*)"', h) if a.strip()), "")
    return {
        "sesskey": campos["sesskey"],
        "context": campos["context"],
        "itemid": campos["newfile"],
        "author": html.unescape(autor.encode().decode("unicode_escape")
                               if "\\u" in autor else autor),
        "categorias": cats,
    }


def importar(cd: CDigital, ruta_xml: str, curso: int, categoria: str | None,
             simular: bool) -> int:
    inf = validar_xml(ruta_xml)
    print(f"XML: {os.path.basename(ruta_xml)}")
    print(f"   categoría declarada en el archivo: {inf['categoria'] or '(ninguna)'}")
    print(f"   preguntas: {len(inf['preguntas'])}")
    for p in inf["preguntas"]:
        extra = (f"{p.get('correctas')}/{p.get('opciones')} correctas, single={p.get('single')}"
                 if p["tipo"] == "multichoice" else "")
        print(f"      - [{p['tipo']}] {p['nombre'][:60]}  {extra}")
    if inf["problemas"]:
        print("\n   PROBLEMAS ENCONTRADOS:")
        for x in inf["problemas"]:
            print(f"      · {x}")
        print("\n   No se importa nada con problemas pendientes. Corrige el XML y repite.")
        return 1
    print("   validación local: sin problemas.")

    url = f"/question/bank/importquestions/import.php?courseid={curso}"
    h = cd.get(url).text
    campos = _campos_import(h)
    print(f"\nAula {curso} · contexto {campos['context']} · borrador {campos['itemid']}")
    print("   categorías existentes en el banco:")
    for v, t in campos["categorias"]:
        print(f"      {v}  {t[:70]}")

    destino = categoria or (campos["categorias"][0][0] if campos["categorias"] else None)
    if not destino:
        raise SystemExit("El formulario no ofreció ninguna categoría de destino.")
    usa_del_archivo = bool(inf["categoria"])
    print(f"\n   categoría del formulario: {destino}")
    print(f"   'obtener categoría del archivo': {'SÍ' if usa_del_archivo else 'no'}"
          + (f" → se creará/usará «{inf['categoria']}»" if usa_del_archivo else ""))

    if simular:
        print("\n--simular: no se subió nada. El aula queda intacta.")
        print("Repite sin --simular para importar de verdad.")
        return 0

    # 1) subir el archivo al área de borradores
    with open(ruta_xml, "rb") as f:
        r = cd.s.post(
            f"{cd.base}/repository/repository_ajax.php?action=upload",
            data={
                "sesskey": campos["sesskey"], "repo_id": str(REPO_SUBIDA),
                "itemid": campos["itemid"], "savepath": "/",
                "title": os.path.basename(ruta_xml), "author": campos["author"],
                "license": "unknown", "overwrite": "1", "ctx_id": campos["context"],
            },
            files={"repo_upload_file": (os.path.basename(ruta_xml), f, "text/xml")},
            timeout=180,
        )
    try:
        respuesta = r.json()
    except ValueError:
        print("La subida no devolvió JSON:", r.status_code, r.text[:400])
        return 1
    if respuesta.get("error"):
        print("Error al subir el archivo:", respuesta["error"])
        return 1
    print(f"\n   archivo subido al borrador: {respuesta.get('file') or respuesta.get('url') or respuesta}")

    # 2) enviar el formulario de importación
    datos = {
        "sesskey": campos["sesskey"],
        "courseid": str(curso),
        "context": campos["context"],
        "_qf__qbank_importquestions_form_question_import_form": "1",
        "format": "xml",
        "category": destino,
        "matchgrades": "error",
        "stoponerror": "1",
        "newfile": campos["itemid"],
        "submitbutton": "Importar",
    }
    if usa_del_archivo:
        datos["catfromfile"] = "1"
        datos["contextfromfile"] = "1"
    r = cd.s.post(f"{cd.base}/question/bank/importquestions/import.php", data=datos, timeout=300)
    texto = re.sub(r"<[^>]+>", " ", r.text)
    texto = html.unescape(re.sub(r"\s+", " ", texto))

    print(f"\n   respuesta de la importación: HTTP {r.status_code}")
    for pat in [r"[Ii]mportando\s+\d+\s+preguntas?[^.]{0,80}",
                r"\d+\s+preguntas?\s+import\w+[^.]{0,60}",
                r"[Ee]rror[^.]{0,200}", r"no se encontr[^.]{0,120}",
                r"[Ff]allo[^.]{0,150}"]:
        for m in list(re.finditer(pat, texto))[:4]:
            print("      ", m.group(0).strip()[:200])
    exito = re.search(r"[Ii]mportando\s+(\d+)", texto)
    if exito:
        print(f"\n   IMPORTADAS: {exito.group(1)} preguntas.")
    else:
        print("\n   No pude confirmar el conteo en la respuesta. Verifica con:")
        print(f"      python config/moodle/cdigital.py preguntas --curso {curso}")
    return 0


# =============================================================================================
# Deshacer — para poder reintentar una importación sin dejar duplicados
# =============================================================================================
def borrar_categoria(cd: CDigital, curso: int, nombre: str, confirmar: bool) -> int:
    """Borra una categoría del banco **y las preguntas que contenga**, por nombre exacto.

    Moodle no deja borrar una categoría con preguntas dentro: exige moverlas a otra. Así que
    primero se borran las preguntas una por una y después la categoría, ya vacía.
    """
    h = cd.get(f"/question/bank/managecategories/category.php?courseid={curso}").text
    # cada categoría aparece más de una vez en el HTML (árbol + menú de acciones): hay que
    # deduplicar, o una categoría legítima parecería ambigua
    encontradas = list(dict.fromkeys(
        re.findall(r'data-categoryid="(\d+)"[^>]*data-contextid="(\d+)"'
                   r'[^>]*data-categoryname="([^"]*)"', h)))
    objetivo = list(dict.fromkeys(
        (c, x) for c, x, n in encontradas if html.unescape(n).strip() == nombre))
    if not objetivo:
        print(f"No hay ninguna categoría llamada exactamente «{nombre}» en el aula {curso}.")
        print("Categorías presentes:")
        for c, x, n in encontradas:
            print(f"   {c},{x}  {html.unescape(n)}")
        return 1
    if len(objetivo) > 1:
        print(f"Hay {len(objetivo)} categorías con ese nombre. Aclara cuál antes de borrar.")
        return 1
    cat, ctx = objetivo[0]

    listado = cd.get(f"/question/edit.php?courseid={curso}&cat={cat},{ctx}").text
    qids = sorted(set(re.findall(r'name="q(\d+)"', listado)))
    print(f"Categoría «{nombre}» (id {cat}) con {len(qids)} preguntas.")
    if not confirmar:
        print("Esto BORRA las preguntas y la categoría. Repite con --confirmar si es lo que quieres.")
        return 0

    sesskey = re.search(r'"sesskey":"([^"]+)"', listado).group(1)
    ret = urllib.parse.quote(f"/question/edit.php?courseid={curso}&cat={cat},{ctx}", safe="")
    for q in qids:
        pg = cd.get(f"/question/bank/deletequestion/delete.php?deleteselected={q}&q{q}=1"
                    f"&sesskey={sesskey}&courseid={curso}&returnurl={ret}").text
        # 'confirm' es un hash que calcula Moodle, no un 1; hay que devolverlo tal cual
        campos = _inputs(_form(pg, r'action="[^"]*deletequestion/delete\.php"'))
        campos["deletequestions"] = "Sí"
        cd.s.post(f"{cd.base}/question/bank/deletequestion/delete.php", data=campos, timeout=90)
    quedan = re.findall(r'name="q(\d+)"',
                        cd.get(f"/question/edit.php?courseid={curso}&cat={cat},{ctx}").text)
    print(f"   preguntas borradas: {len(qids) - len(set(quedan))} · quedan {len(set(quedan))}")

    h = cd.get(f"/question/bank/managecategories/category.php?courseid={curso}").text
    sesskey = re.search(r'"sesskey":"([^"]+)"', h).group(1)
    cd.get(f"/question/bank/managecategories/category.php?courseid={curso}"
           f"&sesskey={sesskey}&delete={cat}")
    final = cd.get(f"/question/bank/managecategories/category.php?courseid={curso}").text
    sigue = f'data-categoryid="{cat}"' in final
    print(f"   categoría: {'SIGUE AHÍ (bórrala a mano)' if sigue else 'borrada'}")
    return 1 if sigue else 0


def _form(h: str, patron_action: str) -> str:
    m = re.search(r"<form[^>]*" + patron_action + r".*?</form>", h, re.S)
    return m.group(0) if m else h


# =============================================================================================
# Inspección
# =============================================================================================
def ver_curso(cd: CDigital, curso: int) -> int:
    """Todo lo que hay en el aula, tema por tema, con lo que está oculto marcado.

    Lee el servicio de estado, no el HTML: ver `CDigital.ws`.
    """
    h = cd.get(f"/course/view.php?id={curso}").text
    t = re.search(r"<title>([^<]+)</title>", h)
    print("Aula:", html.unescape(t.group(1)).strip() if t else "?")
    ctx = re.search(r'"contextid":(\d+)', h)
    print("contextid:", ctx.group(1) if ctx else "?")

    est = cd.estado_curso(curso)
    cms = {str(c["id"]): c for c in est.get("cm", [])}
    secciones = est.get("section", [])
    total = 0
    for sec in secciones:
        ids = [str(x) for x in (sec.get("cmlist") or [])]
        if not ids:
            continue
        oculta = "" if sec.get("visible", True) else "   [SECCIÓN OCULTA]"
        print(f"\n{sec.get('title') or sec.get('name') or 'Tema ?'}{oculta}")
        for cmid in ids:
            c = cms.get(cmid, {})
            marca = "" if c.get("visible", True) else "  [OCULTO]"
            if c.get("stealth"):
                marca += "  [disponible pero no mostrado]"
            print(f"   {str(c.get('module', '?')):12s} cmid={cmid:>9s}  "
                  f"{html.unescape(str(c.get('name', '?')))[:60]}{marca}")
            total += 1

    quices = [c for c in cms.values() if c.get("module") == "quiz"]
    print(f"\nActividades: {total}   ·   Cuestionarios: {len(quices)}")
    for c in quices:
        print(f"   quiz cmid={str(c['id']):>9s}  {html.unescape(str(c.get('name', '?')))[:55]:55s}"
              f"  visible={c.get('visible')}")
    if quices:
        print("\nOJO: los cuestionarios que trae la plantilla del aula tienen slots ALEATORIOS sobre\n"
              "     su propia categoría «Por defecto en …». Míralos con:  cdigital.py quiz <cmid>")
    return 0


def _texto(h: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


def leer_quiz(cd: CDigital, cmid: int) -> dict:
    """Radiografía de un cuestionario: sus slots en orden, con nombre, puntaje y si son aleatorios."""
    h = cd.get(f"/mod/quiz/edit.php?cmid={cmid}").text
    trozos = re.split(r'id="slot-(\d+)"', h)
    slots, vistos = [], set()
    for i in range(1, len(trozos) - 1, 2):
        sid, cuerpo = trozos[i], trozos[i + 1][:4000]
        if sid in vistos:
            continue
        vistos.add(sid)
        nom = re.search(r'<span class="questionname">\s*(?:<[^>]+>\s*)*([^<]{2,140})', cuerpo)
        marca = re.search(r"instancemaxmark[^>]*>\s*([\d.,]+)", cuerpo)
        # de qué categoría saca sus preguntas un slot aleatorio
        cat = re.search(r"question/edit\.php\?cmid=\d+&(?:amp;)?cat=(\d+)(?:%2C|,)(\d+)", cuerpo)
        slots.append({
            "id": sid,
            "nombre": html.unescape(nom.group(1)).strip() if nom else "?",
            "aleatorio": "aleatoria basada en" in cuerpo,
            "marca": marca.group(1) if marca else "?",
            "categoria": f"{cat.group(1)},{cat.group(2)}" if cat else "",
        })
    plano = _texto(h)
    tot = re.search(r"Puntuaci[oó]n total:\s*([\d.,]+)", plano)
    sk = re.search(r'"sesskey":"([^"]+)"', h)
    qz = re.search(r'"quizid"\s*:\s*"?(\d+)', h)
    cur = re.search(r'"courseid"\s*:\s*"?(\d+)', h)
    return {"cmid": cmid, "slots": slots, "html": h,
            "total": tot.group(1) if tot else "?",
            "sesskey": sk.group(1) if sk else cd.sesskey,
            "quizid": qz.group(1) if qz else None,
            "curso": cur.group(1) if cur else None}


def _ajustes_quiz(cd: CDigital, cmid: int) -> dict:
    """Fechas, límite, intentos y nota máxima, leídos del formulario de ajustes."""
    h = cd.get(f"/course/modedit.php?update={cmid}").text

    def campo(nombre: str) -> str:
        # los nombres de Moodle llevan corchetes (timeopen[day]): hay que escaparlos
        e = re.escape(nombre)
        m = re.search(rf'<select[^>]*name="{e}"[^>]*>(.*?)</select>', h, re.S)
        if m:
            s = (re.search(r'<option[^>]*selected[^>]*?value="([^"]*)"[^>]*>([^<]*)', m.group(1))
                 or re.search(r'<option[^>]*value="([^"]*)"[^>]*selected[^>]*>([^<]*)', m.group(1)))
            return html.unescape(s.group(2)).strip() if s else "?"
        m = re.search(rf'<input[^>]*name="{e}"[^>]*>', h)
        if m:
            if 'type="checkbox"' in m.group(0):
                return "sí" if "checked" in m.group(0) else "no"
            v = re.search(r'value="([^"]*)"', m.group(0))
            return html.unescape(v.group(1)) if v else ""
        return "?"

    def fecha(p: str) -> str:
        if campo(p + "[enabled]") == "no":
            return "(desactivada)"
        return (f"{campo(p+'[day]')}/{campo(p+'[month]')}/{campo(p+'[year]')} "
                f"{campo(p+'[hour]')}:{campo(p+'[minute]')}")

    lim = ("(sin límite)" if campo("timelimit[enabled]") == "no"
           else f"{campo('timelimit[number]')} {campo('timelimit[timeunit]')}")
    return {"abre": fecha("timeopen"), "cierra": fecha("timeclose"), "limite": lim,
            "intentos_permitidos": campo("attempts"), "metodo": campo("grademethod"),
            "nota_maxima": campo("grade"), "por_pagina": campo("questionsperpage")}


def _intentos(cd: CDigital, cmid: int) -> int:
    """Cuántos intentos de estudiantes hay. -1 si no se pudo contar: entonces NO se toca nada."""
    plano = _texto(cd.get(f"/mod/quiz/report.php?id={cmid}&mode=overview").text)
    m = re.search(r"Intentos:\s*(\d+)", plano)
    return int(m.group(1)) if m else -1


def preguntas_de_categoria(cd: CDigital, curso: int, categoria: str) -> list[tuple[str, str]]:
    """(id, nombre) de las preguntas de una categoría 'catid,contextid', en el orden que las lista."""
    cat = categoria.replace(",", "%2C")
    h = cd.get(f"/question/edit.php?courseid={curso}&cat={cat}&qperpage=500").text
    # El nombre no está en un <span class="questionname"> como en la página del quiz: en el banco
    # es un campo editable en línea, y trae el id y el nombre juntos en sus atributos.
    salida, vistos = [], set()
    for m in re.finditer(r'data-itemtype="questionname"[^>]*?data-itemid="(\d+)"'
                         r'[^>]*?data-value="([^"]*)"', h):
        if m.group(1) in vistos:
            continue
        vistos.add(m.group(1))
        salida.append((m.group(1), html.unescape(m.group(2)).strip()))
    if not salida:  # por si el tema cambia el markup del editable
        for qid in dict.fromkeys(re.findall(r'name="q(\d+)"', h)):
            salida.append((qid, "?"))
    return salida


def ver_quiz(cd: CDigital, cmid: int) -> int:
    q = leer_quiz(cd, cmid)
    a = _ajustes_quiz(cd, cmid)
    print(f"Cuestionario cmid={cmid}  (quizid={q['quizid']}, curso={q['curso']})")
    print(f"   abre {a['abre']}  ·  cierra {a['cierra']}  ·  límite {a['limite']}")
    print(f"   intentos permitidos {a['intentos_permitidos']}  ·  {a['metodo']}  ·  "
          f"nota máxima {a['nota_maxima']}  ·  {a['por_pagina']} preguntas por página")
    print(f"   intentos YA hechos por estudiantes: {_intentos(cd, cmid)}")
    print(f"\n   {len(q['slots'])} slots  ·  puntuación total {q['total']}")
    for n, s in enumerate(q["slots"], 1):
        tipo = "ALEATORIA" if s["aleatorio"] else "concreta "
        extra = f"  cat={s['categoria']}" if s["categoria"] else ""
        print(f"      {n:2d}. slot {s['id']:>9s}  {tipo}  {s['marca']:>5s}  "
              f"{s['nombre'][:58]}{extra}")
    if any(s["aleatorio"] for s in q["slots"]):
        print("\n   Estos slots NO sirven las preguntas importadas: sacan al azar de la categoría de\n"
              "   plantilla que indica 'cat='. Para que sirvan las tuyas: cdigital.py quiz-sustituir")
    return 0


# =============================================================================================
# Sustituir los slots de un cuestionario
# =============================================================================================
def sustituir_slots(cd: CDigital, cmid: int, categoria: str | None, preguntas: str | None,
                    confirmar: bool, por_pagina: int = 2, dejar_oculto: bool = False) -> int:
    """Deja el cuestionario sirviendo EXACTAMENTE las preguntas indicadas, en ese orden.

    Cómo, y por qué así:
      · `editrandom.php` (reapuntar el filtro de un slot aleatorio) **ya no existe** en Moodle 4.5:
        devuelve 404. No se puede arreglar un slot aleatorio; hay que reemplazarlo.
      · `edit.php?remove=N` tampoco actúa por GET: el botón «Borrar» lleva `data-action="delete"` y
        lo intercepta el JavaScript, que hace POST a `/mod/quiz/edit_rest.php`. Ése es el endpoint.
      · Primero AÑADE y después BORRA, para que el cuestionario nunca quede sin preguntas.
      · Si hay un solo intento de estudiante, aborta: no se recompone un examen ya respondido.

    Sirve igual para un cuestionario **vacío** (0 slots): la fase de borrado no hace nada. Cinco de
    las siete aulas están así — el cuestionario existe, visible y abierto, pero sin ni una pregunta.

    Con `dejar_oculto=True` no se restaura la visibilidad al terminar: es el modo del **alistamiento
    del aula**, que deja todo puesto pero invisible hasta que el Docente lo revise.
    """
    q = leer_quiz(cd, cmid)
    curso = int(q["curso"])
    if categoria:
        lista = preguntas_de_categoria(cd, curso, categoria)
    elif preguntas:
        lista = [(x.strip(), "?") for x in preguntas.split(",") if x.strip()]
    else:
        raise SystemExit("Indica --categoria 'catid,contextid' o --preguntas 'id,id,...'.")
    if not lista:
        raise SystemExit("Esa categoría no tiene preguntas: nada que poner.")

    print(f"Cuestionario cmid={cmid} (quizid={q['quizid']}) del aula {curso}")
    print(f"   ahora: {len(q['slots'])} slots "
          f"({sum(1 for s in q['slots'] if s['aleatorio'])} aleatorios), total {q['total']}")
    print(f"   quedará con estas {len(lista)} preguntas, en este orden:")
    for n, (qid, nom) in enumerate(lista, 1):
        print(f"      {n:2d}. id={qid:>9s}  {nom[:66]}")

    hechos = _intentos(cd, cmid)
    print(f"\n   intentos de estudiantes: {hechos}")
    if hechos != 0:
        raise SystemExit("   ABORTA: hay intentos, o no pude contarlos. No se toca un examen con notas.")
    if not confirmar:
        print("\n   (simulación: no se tocó nada. Añade --confirmar para aplicar.)")
        return 0

    viejos = [s["id"] for s in q["slots"]]
    est = cd.estado_curso(curso)
    cm = next((c for c in est.get("cm", []) if str(c["id"]) == str(cmid)), {})
    visible_original = bool(cm.get("visible", True))

    def rest(**datos):
        d = {"sesskey": leer_quiz(cd, cmid)["sesskey"], "courseid": curso, "quizid": q["quizid"]}
        d.update(datos)
        r = cd.post("/mod/quiz/edit_rest.php", d)
        try:
            return r.json()
        except ValueError:
            return {"respuesta_no_json": r.text[:200]}

    # Mientras se opera, el cuestionario se oculta: hay estudiantes matriculados y durante unos
    # segundos tendría el doble de preguntas.
    if visible_original:
        cd.get(f"/course/mod.php?sesskey={cd.sesskey}&hide={cmid}")
        print("\n   cuestionario ocultado mientras se opera")

    fallo = None
    try:
        print(f"\n1. añadir {len(lista)} preguntas")
        for n, (qid, _nom) in enumerate(lista, 1):
            antes = len(leer_quiz(cd, cmid)["slots"])
            cd.get(f"/mod/quiz/edit.php?cmid={cmid}&sesskey={cd.sesskey}"
                   f"&addquestion={qid}&addonpage=0")
            ahora = len(leer_quiz(cd, cmid)["slots"])
            print(f"   +{qid} ({n:2d}/{len(lista)})  slots {antes} -> {ahora}")
            if ahora != antes + 1:
                raise RuntimeError(f"añadir la pregunta {qid} no creó un slot")
            time.sleep(0.25)

        print(f"\n2. borrar los {len(viejos)} slots anteriores")
        for n, sid in enumerate(viejos, 1):
            antes = len(leer_quiz(cd, cmid)["slots"])
            resp = rest(**{"class": "resource", "action": "DELETE", "id": sid})
            ahora = len(leer_quiz(cd, cmid)["slots"])
            print(f"   -slot {sid} ({n:2d}/{len(viejos)})  slots {antes} -> {ahora}  {resp}")
            if ahora != antes - 1:
                raise RuntimeError(f"borrar el slot {sid} no redujo el número de slots")
            time.sleep(0.25)

        if por_pagina:
            print(f"\n3. repaginar a {por_pagina} preguntas por página")
            for pos, s in enumerate(leer_quiz(cd, cmid)["slots"], 1):
                if pos == 1:
                    continue
                # value=2 abre página nueva antes de este slot; value=1 lo deja en la misma
                quiere = 2 if (pos - 1) % por_pagina == 0 else 1
                rest(**{"class": "resource", "field": "updatepagebreak", "id": s["id"],
                        "value": quiere})
                time.sleep(0.2)

        print("\n4. verificación")
        fin = leer_quiz(cd, cmid)
        problemas = []
        if len(fin["slots"]) != len(lista):
            problemas.append(f"{len(fin['slots'])} slots, esperaba {len(lista)}")
        if any(s["aleatorio"] for s in fin["slots"]):
            problemas.append("quedan slots aleatorios")
        esperadas = [n for _i, n in lista]
        if categoria and [s["nombre"] for s in fin["slots"]] != esperadas:
            problemas.append("los nombres o el orden no coinciden")
        for n, s in enumerate(fin["slots"], 1):
            print(f"      {n:2d}. slot {s['id']:>9s}  {s['marca']:>5s}  {s['nombre'][:62]}")
        print(f"      puntuación total: {fin['total']}")
        if problemas:
            raise RuntimeError(" · ".join(problemas))
        print("   OK")
    except Exception as exc:  # noqa: BLE001
        fallo = exc
        print(f"\n   !!! FALLO: {type(exc).__name__}: {exc}")
        print("   El cuestionario queda OCULTO a propósito: es preferible invisible que roto.")

    if not fallo and visible_original and not dejar_oculto:
        cd.get(f"/course/mod.php?sesskey={cd.sesskey}&show={cmid}")
        est = cd.estado_curso(curso)
        cm = next((c for c in est.get("cm", []) if str(c["id"]) == str(cmid)), {})
        print(f"\n   cuestionario visible otra vez: {cm.get('visible')}")
        print(f"   intentos tras la operación: {_intentos(cd, cmid)}  (debe seguir en 0)")
    elif not fallo and dejar_oculto:
        est = cd.estado_curso(curso)
        cm = next((c for c in est.get("cm", []) if str(c["id"]) == str(cmid)), {})
        print(f"\n   se queda OCULTO por --dejar-oculto: visible={cm.get('visible')}")
        print(f"   (estaba {'visible' if visible_original else 'oculto'} antes; "
              f"actívalo tú con: mostrar {cmid})")
        print(f"   intentos tras la operación: {_intentos(cd, cmid)}  (debe seguir en 0)")
    return 1 if fallo else 0


# =============================================================================================
# Reordenar los slots de un cuestionario
# =============================================================================================
def nombres_del_xml(ruta: str) -> list[str]:
    """Los nombres de las preguntas del banco maestro, en el orden en que están escritas."""
    raiz = ET.parse(ruta).getroot()
    return [(q.findtext("name/text") or "").strip() for q in raiz.findall("question")
            if q.get("type") != "category"]


def reordenar_slots(cd: CDigital, cmid: int, nombres: list[str], confirmar: bool,
                    por_pagina: int = 2, dejar_oculto: bool = False) -> int:
    """Pone los slots que YA tiene el cuestionario en el orden indicado. No añade ni borra.

    Por qué hace falta una función aparte de `sustituir_slots`: para reordenar no sirve volver a
    sustituir. `sustituir_slots` añade antes de borrar —así el cuestionario nunca queda vacío—, pero
    **Moodle no añade dos veces la misma pregunta al mismo cuestionario**: el GET a `addquestion`
    responde 200 y no crea slot, así que la comprobación «añadir no creó un slot» aborta, con razón.
    El orden se cambia con el endpoint que usa el arrastrar-y-soltar de la página:

        POST /mod/quiz/edit_rest.php   class=resource  field=move  id=<slotid>
                                       sectionId=<id del li.section>  previousid=<slot que queda
                                       delante, se omite si va primero>  page=<número de página>

    Para que `page` no sea una adivinanza, primero se **aplana todo a una página** (`updatepagebreak`
    value=1), se mueve, y al final se repagina a `por_pagina`. Y se mueve por selección: para cada
    posición, si no está ya la pregunta que toca, se trae su slot detrás del anterior y se comprueba
    releyendo. Un movimiento no puede perder preguntas —el peor caso es un orden raro, que se
    arregla con más movimientos—, pero igual aborta si hay intentos: un examen respondido no se
    recompone, y cambiar el orden de las preguntas de un intento ya hecho sería justo eso.
    """
    q = leer_quiz(cd, cmid)
    curso = int(q["curso"])
    actuales = [s["nombre"] for s in q["slots"]]
    seccion = re.search(r'id="section-(\d+)"', q["html"])

    print(f"Cuestionario cmid={cmid} (quizid={q['quizid']}) del aula {curso}")
    print(f"   ahora ({len(actuales)} slots)          quedará")
    for n in range(max(len(actuales), len(nombres))):
        a = actuales[n] if n < len(actuales) else ""
        b = nombres[n] if n < len(nombres) else ""
        print(f"   {n+1:2d}. {a[:44]:44s}  {'=' if a == b else '->'}  {b[:44]}")

    if sorted(actuales) != sorted(nombres):
        sobran = sorted(set(actuales) - set(nombres))
        faltan = sorted(set(nombres) - set(actuales))
        print("\n   ABORTA: no son las mismas preguntas, así que esto no es un reordenamiento.")
        if sobran:
            print(f"   en el cuestionario y no en la lista: {sobran}")
        if faltan:
            print(f"   en la lista y no en el cuestionario: {faltan}")
        print("   Para cambiar QUÉ preguntas sirve, usa quiz-sustituir.")
        return 1
    if not seccion:
        print("\n   ABORTA: no encuentro el id de la sección en la página de edición.")
        return 1
    if actuales == nombres:
        print("\n   Ya están en ese orden: no hay nada que hacer.")
        return 0

    hechos = _intentos(cd, cmid)
    print(f"\n   intentos de estudiantes: {hechos}")
    if hechos != 0:
        raise SystemExit("   ABORTA: hay intentos, o no pude contarlos. No se toca un examen con notas.")
    if not confirmar:
        print("\n   (simulación: no se tocó nada. Añade --confirmar para aplicar.)")
        return 0

    est = cd.estado_curso(curso)
    cm = next((c for c in est.get("cm", []) if str(c["id"]) == str(cmid)), {})
    visible_original = bool(cm.get("visible", True))

    def rest(**datos):
        d = {"sesskey": leer_quiz(cd, cmid)["sesskey"], "courseid": curso, "quizid": q["quizid"]}
        d.update(datos)
        r = cd.post("/mod/quiz/edit_rest.php", d)
        try:
            return r.json()
        except ValueError:
            return {"respuesta_no_json": r.text[:200]}

    if visible_original:
        cd.get(f"/course/mod.php?sesskey={cd.sesskey}&hide={cmid}")
        print("\n   cuestionario ocultado mientras se opera")

    fallo = None
    try:
        print("\n1. aplanar a una sola página (para que 'page' no sea una adivinanza)")
        for pos, s in enumerate(leer_quiz(cd, cmid)["slots"], 1):
            if pos > 1:
                rest(**{"class": "resource", "field": "updatepagebreak", "id": s["id"], "value": 1})
                time.sleep(0.2)

        print("\n2. mover cada pregunta a su sitio")
        movimientos = 0
        for i, quiere in enumerate(nombres):
            slots = leer_quiz(cd, cmid)["slots"]
            if slots[i]["nombre"] == quiere:
                print(f"   {i+1:2d}. ya está: {quiere[:56]}")
                continue
            suyo = next((s for s in slots if s["nombre"] == quiere), None)
            if not suyo:
                raise RuntimeError(f"la pregunta «{quiere}» ya no está en el cuestionario")
            datos = {"class": "resource", "field": "move", "id": suyo["id"],
                     "sectionId": seccion.group(1), "page": 1}
            if i > 0:
                datos["previousid"] = slots[i - 1]["id"]
            resp = rest(**datos)
            movimientos += 1
            despues = leer_quiz(cd, cmid)["slots"]
            print(f"   {i+1:2d}. slot {suyo['id']} -> posición {i+1}  {quiere[:44]}  {resp}")
            if despues[i]["nombre"] != quiere:
                raise RuntimeError(f"el movimiento no dejó «{quiere}» en la posición {i+1}: "
                                   f"quedó «{despues[i]['nombre']}»")
            if len(despues) != len(nombres):
                raise RuntimeError(f"el movimiento cambió el número de slots: {len(despues)}")
            time.sleep(0.25)
        print(f"   {movimientos} movimientos")

        if por_pagina:
            print(f"\n3. repaginar a {por_pagina} preguntas por página")
            for pos, s in enumerate(leer_quiz(cd, cmid)["slots"], 1):
                if pos == 1:
                    continue
                quiere_salto = 2 if (pos - 1) % por_pagina == 0 else 1
                rest(**{"class": "resource", "field": "updatepagebreak", "id": s["id"],
                        "value": quiere_salto})
                time.sleep(0.2)

        print("\n4. verificación")
        fin = leer_quiz(cd, cmid)
        problemas = []
        if [s["nombre"] for s in fin["slots"]] != nombres:
            problemas.append("los nombres o el orden no coinciden con lo pedido")
        if any(s["aleatorio"] for s in fin["slots"]):
            problemas.append("quedan slots aleatorios")
        if str(fin["total"]) != str(q["total"]):
            problemas.append(f"la puntuación total cambió: {q['total']} -> {fin['total']}")
        for n, s in enumerate(fin["slots"], 1):
            print(f"      {n:2d}. slot {s['id']:>9s}  {s['marca']:>5s}  {s['nombre'][:62]}")
        print(f"      puntuación total: {fin['total']}")
        if problemas:
            raise RuntimeError(" · ".join(problemas))
        print("   OK")
    except Exception as exc:  # noqa: BLE001
        fallo = exc
        print(f"\n   !!! FALLO: {type(exc).__name__}: {exc}")
        print("   El cuestionario queda OCULTO a propósito: es preferible invisible que roto.")

    if not fallo and visible_original and not dejar_oculto:
        cd.get(f"/course/mod.php?sesskey={cd.sesskey}&show={cmid}")
    est = cd.estado_curso(curso)
    cm = next((c for c in est.get("cm", []) if str(c["id"]) == str(cmid)), {})
    print(f"\n   visible={cm.get('visible')}  (estaba "
          f"{'visible' if visible_original else 'oculto'} antes)")
    if cm.get("visible") is False:
        print(f"   sigue OCULTO: actívalo tú con  mostrar {cmid}")
    print(f"   intentos tras la operación: {_intentos(cd, cmid)}  (debe seguir en 0)")
    return 1 if fallo else 0


# =============================================================================================
# Material de estudio — publicarlo como recurso de archivo, oculto
# =============================================================================================
MIME = {".pdf": "application/pdf", ".docx": "application/vnd.openxmlformats-officedocument"
                                            ".wordprocessingml.document",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".md": "text/markdown", ".txt": "text/plain", ".zip": "application/zip"}


def subir_recurso(cd: CDigital, curso: int, ruta: str, seccion: int, nombre: str | None,
                  intro: str, visible: bool, confirmar: bool) -> int:
    """Crea un `mod_resource` (Archivo) en el aula con el documento indicado.

    Por defecto **oculto**: el alistamiento del aula deja el material puesto pero invisible, para
    que el Docente lo revise y lo active cuando quiera. `--visible` invierte eso a propósito.

    El paso que no es evidente: `availabilityconditionsjson` es un ``<textarea>`` **vacío** en el
    HTML servido, que rellena el JavaScript de Moodle. `_inputs()` sólo lee ``<input>``, así que
    nunca lo ve, y `modedit.php` responde **HTTP 404** con «Invalid JSON from
    availabilityconditionsjson» si no llega. Hay que mandarlo a mano.
    """
    if not os.path.exists(ruta):
        print(f"No existe el archivo: {ruta}")
        return 1
    titulo = nombre or os.path.splitext(os.path.basename(ruta))[0]
    ext = os.path.splitext(ruta)[1].lower()
    tam = os.path.getsize(ruta)

    print(f"Aula {curso} · sección {seccion}")
    print(f"   archivo:  {os.path.basename(ruta)}  ({tam:,} bytes)")
    print(f"   nombre:   {titulo}")
    print(f"   visible:  {'SÍ' if visible else 'NO (oculto para los estudiantes)'}")
    if not confirmar:
        print("\n   Simulación: no se ha creado nada. Añade --confirmar para crearlo.")
        return 0

    url = (f"/course/modedit.php?add=resource&type=&course={curso}"
           f"&section={seccion}&return=0&sr=0")
    campos = _inputs(cd.get(url).text)
    faltan = [k for k in ("sesskey", "context", "files", "course") if not campos.get(k)]
    if faltan:
        print(f"El formulario de «Archivo» no trajo: {', '.join(faltan)}. "
              "¿La sesión tiene permiso de edición en este aula?")
        return 1

    with open(ruta, "rb") as f:
        r = cd.s.post(
            f"{cd.base}/repository/repository_ajax.php?action=upload",
            data={"sesskey": campos["sesskey"], "repo_id": str(REPO_SUBIDA),
                  "itemid": campos["files"], "savepath": "/",
                  "title": os.path.basename(ruta), "author": cd.nombre,
                  "license": "unknown", "overwrite": "1", "ctx_id": campos["context"]},
            files={"repo_upload_file": (os.path.basename(ruta), f,
                                        MIME.get(ext, "application/octet-stream"))},
            timeout=600)
    try:
        subida = r.json()
    except ValueError:
        print("La subida no devolvió JSON:", r.status_code, r.text[:300])
        return 1
    if subida.get("error"):
        print("Error al subir el archivo:", subida["error"])
        return 1
    print(f"\n   1. subido al borrador: {subida.get('file') or subida.get('id')}")

    datos = dict(campos)
    datos.update({
        "name": titulo,
        "introeditor[text]": f"<p>{html.escape(intro)}</p>" if intro else "",
        "introeditor[format]": "1",
        "printintro": "1",
        "display": "0",                 # 0 automático · 1 incrustar · 4 forzar descarga · 5 abrir
        "visible": "1" if visible else "0",
        # Sin esto, modedit.php responde 404: el textarea viene vacío en el HTML.
        "availabilityconditionsjson": '{"op":"&","c":[],"showc":[]}',
        "submitbutton2": "Guardar cambios y regresar al curso",
    })
    r = cd.s.post(f"{cd.base}/course/modedit.php", data=datos, timeout=300)
    print(f"   2. modedit: HTTP {r.status_code}")
    if r.status_code != 200:
        texto = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text)))
        for m in list(re.finditer(r"(?:[Ee]rror|[Ii]nvalid|no v[áa]lido)[^.]{0,180}", texto))[:3]:
            print("      ", m.group(0).strip()[:200])
        return 1

    est = cd.estado_curso(curso)
    creados = [c for c in est.get("cm", []) if str(c.get("name", "")).strip() == titulo]
    if not creados:
        print("   !!! El POST salió bien pero el recurso no aparece en el aula. Revísalo a mano.")
        return 1
    for c in creados:
        print(f"\n   3. creado: cmid {c['id']}  visible={c.get('visible')}  stealth={c.get('stealth')}")
        if bool(c.get("visible")) != visible:
            print(f"   !!! La visibilidad no quedó como se pidió. Corrígela con: "
                  f"{'mostrar' if visible else 'ocultar'} {c['id']}")
            return 1
    if len(creados) > 1:
        print(f"   Aviso: hay {len(creados)} actividades con ese nombre exacto en el aula.")
    print(f"\n   URL: {cd.base}/mod/resource/view.php?id={creados[0]['id']}")
    return 0


_TRANSLITERA = str.maketrans({
    "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n", "ü": "u",
    "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ñ": "N", "Ü": "U",
    "·": "-", "–": "-", "—": "-", "’": "'", "‘": "'", "“": '"', "”": '"', "…": "..."})


def nombre_archivo(titulo: str, ext: str, largo: int = 120) -> str:
    """Nombre de archivo que Moodle no va a reescribir a nuestras espaldas.

    Importa porque la verificación final compara los nombres que pedimos contra los que aparecen
    en la carpeta: si Moodle transformara acentos o «·», la comprobación daría un falso fallo.
    """
    base = titulo.translate(_TRANSLITERA)
    base = re.sub(r"[^A-Za-z0-9 ()\[\].,'+&%_-]+", " ", base)
    base = re.sub(r"\s+", " ", base).strip(" .-")
    return f"{base[:largo].strip(' .-')}{ext}"


def subir_carpeta(cd: CDigital, curso: int, archivos: list[tuple[str, str | None]], seccion: int,
                  nombre: str, intro: str, visible: bool, confirmar: bool) -> int:
    """Crea un `mod_folder` (Carpeta) con VARIOS archivos dentro, oculto por defecto.

    `archivos` es una lista de `(ruta, título)`; el título es cómo se llamará el archivo dentro de
    la carpeta (sin extensión), y con `None` se usa el nombre que ya tiene en el disco.

    Por qué una Carpeta y no un «Archivo» por documento: el material de un curso son entre 19 y 27
    documentos. Como actividades sueltas serían 27 líneas en la página del aula —y 27 cosas que
    revisar y activar una por una—; en cuatro carpetas son cuatro. Los estudiantes ven la lista de
    archivos igual, y pueden descargarla completa.

    Mismo camino que `subir_recurso`: todas las subidas van al MISMO borrador (`files`), y hay que
    mandar `availabilityconditionsjson` a mano porque es un `<textarea>` vacío que rellena el
    JavaScript de Moodle y `modedit.php` responde 404 si no llega.
    """
    plan: list[tuple[str, str]] = []
    for ruta, titulo in archivos:
        if not os.path.exists(ruta):
            print(f"No existe el archivo: {ruta}")
            return 1
        ext = os.path.splitext(ruta)[1].lower()
        destino = nombre_archivo(titulo, ext) if titulo else nombre_archivo(
            os.path.splitext(os.path.basename(ruta))[0], ext)
        plan.append((ruta, destino))

    repetidos = {d for _r, d in plan if [x for _y, x in plan].count(d) > 1}
    if repetidos:
        print("Dos archivos distintos acabarían con el mismo nombre dentro de la carpeta, y el "
              f"segundo pisaría al primero: {sorted(repetidos)}")
        return 1

    tam = sum(os.path.getsize(r) for r, _d in plan)
    print(f"Aula {curso} · sección {seccion} · carpeta «{nombre}»")
    print(f"   {len(plan)} archivos · {tam:,} bytes")
    print(f"   visible:  {'SÍ' if visible else 'NO (oculta para los estudiantes)'}")
    for _r, d in plan:
        print(f"      · {d}")
    if not confirmar:
        print("\n   Simulación: no se ha creado nada. Añade --confirmar para crearla.")
        return 0

    url = (f"/course/modedit.php?add=folder&type=&course={curso}"
           f"&section={seccion}&return=0&sr=0")
    campos = _inputs(cd.get(url).text)
    faltan = [k for k in ("sesskey", "context", "files", "course") if not campos.get(k)]
    if faltan:
        print(f"El formulario de «Carpeta» no trajo: {', '.join(faltan)}. "
              "¿La sesión tiene permiso de edición en este aula?")
        return 1

    guardados: list[str] = []
    for n, (ruta, destino) in enumerate(plan, 1):
        ext = os.path.splitext(ruta)[1].lower()
        with open(ruta, "rb") as f:
            r = cd.s.post(
                f"{cd.base}/repository/repository_ajax.php?action=upload",
                data={"sesskey": campos["sesskey"], "repo_id": str(REPO_SUBIDA),
                      "itemid": campos["files"], "savepath": "/",
                      "title": destino, "author": cd.nombre,
                      "license": "unknown", "overwrite": "1", "ctx_id": campos["context"]},
                files={"repo_upload_file": (destino, f,
                                            MIME.get(ext, "application/octet-stream"))},
                timeout=600)
        try:
            subida = r.json()
        except ValueError:
            print(f"   !!! La subida de «{destino}» no devolvió JSON: {r.status_code} "
                  f"{r.text[:200]}")
            return 1
        if subida.get("error"):
            print(f"   !!! Error al subir «{destino}»: {subida['error']}")
            return 1
        real = subida.get("file") or destino
        guardados.append(real)
        aviso = "" if real == destino else f"   (Moodle lo renombró: pedí «{destino}»)"
        print(f"   {n:2d}/{len(plan)} {real}{aviso}")

    datos = dict(campos)
    datos.update({
        "name": nombre,
        "introeditor[text]": f"<p>{html.escape(intro)}</p>" if intro else "",
        "introeditor[format]": "1",
        "showdescription": "1" if intro else "0",
        "display": "0",                 # 0 mostrar en página aparte · 1 incrustar en el aula
        "showexpanded": "1",
        "showdownloadfolder": "1",      # que el estudiante pueda bajarse la carpeta completa
        "visible": "1" if visible else "0",
        "availabilityconditionsjson": '{"op":"&","c":[],"showc":[]}',
        "submitbutton2": "Guardar cambios y regresar al curso",
    })
    r = cd.s.post(f"{cd.base}/course/modedit.php", data=datos, timeout=600)
    print(f"\n   modedit: HTTP {r.status_code}")
    if r.status_code != 200:
        texto = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text)))
        for m in list(re.finditer(r"(?:[Ee]rror|[Ii]nvalid|no v[áa]lido)[^.]{0,180}", texto))[:3]:
            print("      ", m.group(0).strip()[:200])
        return 1

    est = cd.estado_curso(curso)
    creados = [c for c in est.get("cm", []) if str(c.get("name", "")).strip() == nombre]
    if not creados:
        print("   !!! El POST salió bien pero la carpeta no aparece en el aula. Revísala a mano.")
        return 1
    cm = creados[-1]
    print(f"   creada: cmid {cm['id']}  visible={cm.get('visible')}")
    if len(creados) > 1:
        print(f"   Aviso: hay {len(creados)} actividades con ese nombre exacto en el aula.")
    if bool(cm.get("visible")) != visible:
        print(f"   !!! La visibilidad no quedó como se pidió. Corrígela con: "
              f"{'mostrar' if visible else 'ocultar'} {cm['id']}")
        return 1

    # Que el POST responda 200 no garantiza que los archivos hayan quedado dentro: se comprueba
    # que cada nombre aparezca en la vista de la carpeta.
    vista = cd.get(f"/mod/folder/view.php?id={cm['id']}").text
    ausentes = [g for g in guardados if html.escape(g) not in vista and g not in vista]
    print(f"   contenido verificado: {len(guardados) - len(ausentes)}/{len(guardados)} archivos")
    if ausentes:
        print(f"   !!! No aparecen en la carpeta: {ausentes}")
        return 1
    print(f"\n   URL: {cd.base}/mod/folder/view.php?id={cm['id']}")
    return 0


def visibilidad(cd: CDigital, cmid: int, mostrar: bool) -> int:
    """Oculta o muestra una actividad. Es un GET a `/course/mod.php`, pero hay que verificarlo."""
    accion = "show" if mostrar else "hide"
    cd.get(f"/course/mod.php?sesskey={cd.sesskey}&{accion}={cmid}")

    # mod.php no dice de qué curso era el módulo: se saca de la página de la actividad.
    h = cd.get(f"/course/modedit.php?update={cmid}&return=0&sr=0").text
    m = re.search(r'name="course"[^>]*value="(\d+)"', h) or re.search(r'[?&]id=(\d+)', h)
    if not m:
        print(f"No pude averiguar de qué aula es el cmid {cmid}; la acción se envió pero no la verifico.")
        return 1
    curso = int(m.group(1))
    cm = next((c for c in cd.estado_curso(curso).get("cm", []) if str(c["id"]) == str(cmid)), None)
    if not cm:
        print(f"El cmid {cmid} no aparece en el aula {curso}.")
        return 1
    print(f"Aula {curso} · «{cm.get('name')}» (cmid {cmid})")
    print(f"   visible = {cm.get('visible')}   stealth = {cm.get('stealth')}")
    if bool(cm.get("visible")) != mostrar:
        print(f"   !!! Pedí {accion} y no quedó así. Puede ser que el aula esté en modo de "
              "«disponible pero no visible» o que falte permiso.")
        return 1
    print("   OK")
    return 0


def ver_preguntas(cd: CDigital, curso: int) -> int:
    h = cd.get(f"/question/bank/importquestions/import.php?courseid={curso}").text
    campos = _campos_import(h)
    print(f"Categorías del banco de preguntas del aula {curso} (contexto {campos['context']}):")
    for v, t in campos["categorias"]:
        print(f"   {v}  {t}")
    print("\n(El número entre paréntesis es la cantidad de preguntas de cada categoría.)")
    return 0


# =============================================================================================
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Cliente de CDigital (Moodle CUN).",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("estado", help="Iniciar sesión y decir con qué cuenta se entró")

    p = sub.add_parser("curso", help="Listar actividades del aula")
    p.add_argument("id", type=int)

    p = sub.add_parser("importar", help="Importar un banco de preguntas en Moodle XML")
    p.add_argument("xml")
    p.add_argument("--curso", type=int, required=True)
    p.add_argument("--categoria", default=None,
                   help="'catid,contextid' de destino; por defecto la primera del formulario")
    p.add_argument("--simular", action="store_true",
                   help="Validar y mostrar qué haría, SIN tocar el aula")

    p = sub.add_parser("preguntas", help="Listar las categorías del banco de preguntas")
    p.add_argument("--curso", type=int, required=True)

    p = sub.add_parser("borrar-categoria",
                       help="Deshacer una importación: borra una categoría y sus preguntas")
    p.add_argument("nombre", help="Nombre EXACTO de la categoría")
    p.add_argument("--curso", type=int, required=True)
    p.add_argument("--confirmar", action="store_true", help="Sin esto solo informa")

    p = sub.add_parser("quiz", help="Radiografía de un cuestionario: slots, fechas, intentos")
    p.add_argument("cmid", type=int)

    p = sub.add_parser("quiz-sustituir",
                       help="Que un cuestionario sirva las preguntas indicadas (no las de plantilla)")
    p.add_argument("cmid", type=int)
    p.add_argument("--categoria", default=None, help="'catid,contextid' del banco a servir")
    p.add_argument("--preguntas", default=None, help="ids de pregunta separados por comas, en orden")
    p.add_argument("--por-pagina", type=int, default=2, help="preguntas por página (0 = no repaginar)")
    p.add_argument("--dejar-oculto", action="store_true",
                   help="No restaurar la visibilidad al terminar (modo alistamiento del aula)")
    p.add_argument("--confirmar", action="store_true", help="Sin esto solo simula")

    p = sub.add_parser("quiz-ordenar",
                       help="Reordenar los slots que YA tiene, al orden del .xml maestro")
    p.add_argument("cmid", type=int)
    p.add_argument("--xml", required=True, help="Banco maestro: manda el orden en que está escrito")
    p.add_argument("--por-pagina", type=int, default=2, help="preguntas por página (0 = no repaginar)")
    p.add_argument("--dejar-oculto", action="store_true",
                   help="No restaurar la visibilidad al terminar (modo alistamiento del aula)")
    p.add_argument("--confirmar", action="store_true", help="Sin esto solo simula")

    p = sub.add_parser("subir-recurso",
                       help="Publicar un documento como actividad «Archivo», oculta por defecto")
    p.add_argument("archivo")
    p.add_argument("--curso", type=int, required=True)
    p.add_argument("--seccion", type=int, default=1, help="Tema del aula (0 = General)")
    p.add_argument("--nombre", default=None, help="Nombre en el aula; por defecto, el del archivo")
    p.add_argument("--intro", default="", help="Descripción breve que ve el estudiante")
    p.add_argument("--visible", action="store_true",
                   help="Crearlo VISIBLE. Sin esto queda oculto, que es lo que quiere el alistamiento")
    p.add_argument("--confirmar", action="store_true", help="Sin esto solo simula")

    p = sub.add_parser("subir-carpeta",
                       help="Publicar varios documentos como una «Carpeta», oculta por defecto")
    p.add_argument("archivos", nargs="+")
    p.add_argument("--curso", type=int, required=True)
    p.add_argument("--nombre", required=True, help="Nombre de la carpeta en el aula")
    p.add_argument("--seccion", type=int, default=0, help="Tema del aula (0 = General)")
    p.add_argument("--intro", default="", help="Descripción breve que ve el estudiante")
    p.add_argument("--visible", action="store_true",
                   help="Crearla VISIBLE. Sin esto queda oculta, que es lo que quiere el alistamiento")
    p.add_argument("--confirmar", action="store_true", help="Sin esto solo simula")

    p = sub.add_parser("ocultar", help="Ocultar una actividad a los estudiantes")
    p.add_argument("cmid", type=int)

    p = sub.add_parser("mostrar", help="Hacer visible una actividad")
    p.add_argument("cmid", type=int)

    args = ap.parse_args(argv)

    # 'importar --simular' valida el XML aunque no haya sesión, pero igual necesita el formulario
    cd = CDigital()
    cd.entrar()
    print(f"Sesión iniciada como: {cd.nombre}  (userId {cd.uid})\n")

    if args.cmd == "estado":
        return 0
    if args.cmd == "curso":
        return ver_curso(cd, args.id)
    if args.cmd == "preguntas":
        return ver_preguntas(cd, args.curso)
    if args.cmd == "importar":
        return importar(cd, os.path.abspath(args.xml), args.curso, args.categoria, args.simular)
    if args.cmd == "borrar-categoria":
        return borrar_categoria(cd, args.curso, args.nombre, args.confirmar)
    if args.cmd == "quiz":
        return ver_quiz(cd, args.cmid)
    if args.cmd == "quiz-sustituir":
        return sustituir_slots(cd, args.cmid, args.categoria, args.preguntas,
                               args.confirmar, args.por_pagina, args.dejar_oculto)
    if args.cmd == "quiz-ordenar":
        return reordenar_slots(cd, args.cmid, nombres_del_xml(os.path.abspath(args.xml)),
                               args.confirmar, args.por_pagina, args.dejar_oculto)
    if args.cmd == "subir-recurso":
        return subir_recurso(cd, args.curso, os.path.abspath(args.archivo), args.seccion,
                             args.nombre, args.intro, args.visible, args.confirmar)
    if args.cmd == "subir-carpeta":
        return subir_carpeta(cd, args.curso, [(os.path.abspath(a), None) for a in args.archivos],
                             args.seccion, args.nombre, args.intro, args.visible, args.confirmar)
    if args.cmd == "ocultar":
        return visibilidad(cd, args.cmid, mostrar=False)
    if args.cmd == "mostrar":
        return visibilidad(cd, args.cmid, mostrar=True)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
