# -*- coding: utf-8 -*-
"""Consolida en Clases/ lo que se comparte con estudiantes (los 5 cursos).

- Genera enunciados ACA en Clases/Recursos/ACAs/ (.docx)
- Copia Plantilla APA a Clases/Recursos/
- Escribe Clases/LEEME - Material para estudiantes.docx (nunca .md en Clases/)
  · el rompehielos del LEEME se deriva del tamaño del grupo (ver `rompehielos()`):
    muro Padlet hasta 20 estudiantes, juego en Slido por encima.
- Regenera Correo de bienvenida en rutas docentes (`2026/<grupo>/`; nunca en Clases/)
- (Creatividad) ficha taller S01 en carpeta de sesión como .docx

Uso: python config/slides/sync_clases_estudiantes.py
"""
from __future__ import annotations

import csv
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))

from sesiones_cun import (
    COURSES,
    CURSOS_CON_TUTORIAS_POR_GRUPO,
    DOCENTE_CORREO,
    LINK_TUTORIAS,
    MSG_TUTORIAS_POR_GRUPO,
    meet_url,
    subject_encuentro,
)
from cun_slides_engine import (
    ICEBREAKER_MAX_MURO,
    PADLET_PRESENTACION_URL,
    slido_url,
)
from guion_md_a_docx import convert as md_to_docx
from build_acas_estudiantes import build_course as build_acas, catalog_for_leeme
from build_correo_bienvenida import build_course as build_correo, CORREO_NAME
from carga_academica import GRABACIONES_URL, course_dir, curso as carga_curso
from sesiones_cun import cdigital_url, cdigital_urls_por_grupo, CDIGITAL_PLACEHOLDER  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
APA_SRC = os.path.join(ROOT, "Plantilla_APA_CUN_Proyecto de grado.docx")
APA_NAME = "Plantilla_APA_CUN_Proyecto de grado.docx"
# Placeholder de respaldo: los usos por curso deben llamar a
# `cdigital_url(<clave del curso>)`, que devuelve la URL real del aula si existe
# en carga_academica_2026.json (auditadas el 2026-08-10) y el placeholder si no.
URL_CDIGITAL = CDIGITAL_PLACEHOLDER

LEEME_NAME = "LEEME - Material para estudiantes.docx"
FICHA_CREATIVIDAD_NAME = "Ficha_problema_oportunidad.docx"

# --- Rompehielos: la herramienta la decide el TAMAÑO del grupo ----------------
# Decisión del Docente (2026-08-11). Un muro colaborativo solo sirve mientras las
# notas se puedan leer TODAS en la clase: con 50 matriculados —o los 112 de TG3 en
# una sola serie— nadie alcanza a ser visto y el muro se vuelve ruido. Por eso el
# modo NO se escribe curso por curso: se deriva de la matrícula real (listados
# exportados de CDigital, `<Asignatura>/2026/<grupo>/Listado estudiantes (CDigital).csv`).
#   hasta ICEBREAKER_MAX_MURO estudiantes → muro Padlet (hoy solo Investigación: 20)
#   por encima                            → juego en **Slido** (Proyecto I,
#                                            Creatividad, TG2 y TG3)
# El umbral es el mismo de siempre y vive en `cun_slides_engine` (una sola casa: si
# cambia allá, cambia aquí). Por qué Slido: el plan gratis (Basic) da 100
# participantes por evento, 3 encuestas, 1 quiz con tabla de posiciones y Q&A
# ilimitado — Mentimeter corta en 50 participantes AL MES y no alcanza ni para un
# curso de 50. En los cursos grandes el rompehielos deja de ser «cada quien se
# presenta» (que no cabe en la hora) y pasa a ser un juego de 8 minutos con premio:
# «dos verdades y una mentira» sobre el Docente.
#
# OJO — lo que este LEEME NO puede decir: las frases de las rondas y **cuál es la
# mentira**. Eso es material del Docente y vive en
# `<Asignatura>/2026/<grupo>/Rompehielos Slido - Sesion 01.md`
# (`config/slides/build_rompehielos_slido.py`), fuera de `Clases/`.
LISTADO_CSV = "Listado estudiantes (CDigital).csv"


def matriculados(key: str) -> int | None:
    """Estudiantes del curso: filas con rol «Estudiante» en los listados de CDigital.

    Suma **todos** los grupos del curso porque comparten una sola serie de
    encuentros (TG3 dicta 54450 + 54466 + 54467 en la misma clase). Devuelve
    `None` si no hay ningún listado exportado, es decir, si no hay con qué decidir.
    """
    raiz = course_dir(key)
    total = 0
    listados = 0
    for grupo in carga_curso(key).get("groups") or []:
        ruta = raiz / "2026" / str(grupo) / LISTADO_CSV
        if not ruta.is_file():
            continue
        listados += 1
        with open(ruta, encoding="utf-8-sig", newline="") as fh:
            total += sum(
                1
                for fila in csv.DictReader(fh)
                if (fila.get("rol") or "").strip().lower() == "estudiante"
            )
    return total if listados else None


def rompehielos(key: str) -> dict:
    """Modo y textos del rompehielos de este curso, según cuánta gente hay matriculada.

    Nada de lo que sale de aquí puede adelantar las frases del juego ni cuál es la
    mentira: esto es material del estudiante.
    """
    n = matriculados(key)
    corto = carga_curso(key)["titulo_corto"]
    if n is not None and n <= ICEBREAKER_MAX_MURO:
        return {
            "modo": "muro",
            "n": n,
            "recurso": "**Padlet** (rompehielos / Preséntate)",
            "url": PADLET_PRESENTACION_URL,
            "corto": "rompehielos en el muro de Padlet",
            "nombre": "El muro de Padlet",
            "cierre": (
                "**El muro de Padlet** es para presentarte / mapear expectativas; no "
                "sustituye la entrega en CDigital."
            ),
            "como": (
                "El **Padlet** es el muro donde te presentas en la Sesión 01: una nota por "
                "persona (nombre, expectativa y tema de interés). El grupo es pequeño, así que "
                "las leemos **todas** en clase."
            ),
        }
    # Sin listado tampoco se asume grupo pequeño: el muro es justo lo que se rompe
    # con volumen, y el juego funciona igual de bien con 20 que con 112.
    cuantos = f"{n} matriculados" if n is not None else "un grupo grande"
    url = slido_url(key, corto)
    # Mientras el evento no exista, la tabla muestra el marcador de posición: no tiene
    # sentido mandar al estudiante a «el enlace de arriba». El código del chat siempre
    # sirve, con enlace o sin él, y es la vía real por la que entra la mayoría.
    tambien_enlace = (
        " (también puedes usar el enlace de la tabla de arriba)"
        if url.lower().startswith("http") else ""
    )
    return {
        "modo": "slido",
        "n": n,
        "recurso": "**Slido** (rompehielos de la Sesión 01 · juego con premio)",
        "url": url,
        "corto": "el juego de presentación en Slido",
        "nombre": "El juego de Slido",
        "cierre": (
            "**El juego de Slido** es el rompehielos de la Sesión 01: sirve para conocernos "
            "y **no da nota** ni sustituye ninguna entrega de CDigital."
        ),
        "como": (
            "El rompehielos de la **Sesión 01** es un juego de **8 minutos** en **Slido**: "
            "«**dos verdades y una mentira**» sobre el Docente. En cada ronda ves tres frases "
            "suyas y eliges la que **no** es cierta; acertar es 1 entre 3, así que no hay que "
            "saber nada para ganar. **Cómo entras:** abres **slido.com** y escribes el "
            "**código del evento**, que el Docente pega en el **chat del Meet** al empezar"
            f"{tambien_enlace}. No hay que instalar nada "
            "ni crear cuenta. Al final sale la **tabla de posiciones** y los **tres primeros** "
            f"juegan la ronda final con sus propias frases. Hay **premio**. Con {cuantos} no "
            "alcanzamos a presentarnos uno por uno, y así igual nos conocemos. Si te la "
            "pierdes, el evento queda **abierto 48 horas**: puedes jugar aunque ya no entres "
            "en la tabla. Las **preguntas** de toda la sesión también van por el **Q&A** de "
            "ese mismo Slido."
        ),
    }

PRESENTACION_CURSO = {
    "proyecto1": "Presentacion del Curso - Proyecto I.pptx",
    "investigacion": "Presentacion del Curso - Investigacion Ciencia y Tecnologia.pptx",
    "creatividad": "Presentacion del Curso - Creatividad y Pensamiento Innovador.pptx",
    "tg2": "Presentacion del Curso - Trabajo de Grado 2.pptx",
    "tg3": "Presentacion del Curso - Trabajo de Grado 3.pptx",
}

FICHA_CREATIVIDAD_S01 = """# Ficha problema–oportunidad (Sesión 01)

**Curso:** Creatividad y Pensamiento Innovador  
**Entregable:** sube a CDigital como `S01_FichaProblema_Apellido`  
**Preferible:** Google Docs / Word Online (no se exige Office de escritorio).

Completa los 6 campos:

1. **Título tentativo:**

2. **Usuario concreto:** (quién sufre el problema; no “la gente”)

3. **Problema (3–5 líneas):**

4. **Evidencia o síntoma observable:**

5. **Tipo de innovación tentativo:** (producto / proceso / organización / marketing / social)

6. **Valor esperado (1 frase):**

---

**Criterio de éxito:** si alguien externo entiende el usuario + el dolor + el contexto sin pedirte aclaración, la ficha sirve.
"""


def write_md_as_docx(
    md_text: str,
    docx_path: str,
    *,
    subtitle: str | None = None,
    footer: str | None = None,
) -> None:
    """Genera .docx con marca CUN (sin dejar .md en Clases/)."""
    fd, tmp = tempfile.mkstemp(suffix=".md", prefix="clases_est_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(md_text)
        md_to_docx(tmp, docx_path, brand=True, subtitle=subtitle, footer=footer)
    finally:
        if os.path.isfile(tmp):
            os.remove(tmp)


def remove_if_exists(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)
        print("RM", path)


def leeme_md(key: str) -> str:
    c = COURSES[key]
    cc = carga_curso(key)
    pptx_curso = PRESENTACION_CURSO[key]
    meet = meet_url(key, c["titulo"])
    rh = rompehielos(key)
    # Nombre real del evento de la Sesión 01: es la clave con la que el estudiante
    # busca la grabación dentro de la carpeta única de Drive.
    evento_s01 = subject_encuentro(key, list(cc.get("groups") or []), n=1)
    es_pregrado = cc.get("nivel") != "especializacion"
    # TG3 comparte esta carpeta `Clases/` entre sus TRES grupos, y cada grupo tiene su
    # PROPIA aula en CDigital (54450 → 112321, 54466 → 116387, 54467 → 129270). Enseñar una
    # sola mandaría a dos tercios del curso a un aula donde no están matriculados.
    _aulas = cdigital_urls_por_grupo(key)
    aula_txt = (
        " · ".join(f"**{g}**: {u}" for g, u in sorted(_aulas.items())) + " — busca la de tu grupo"
        if _aulas else cdigital_url(key)
    )
    aca_rows = catalog_for_leeme(key)
    # La tabla lista los **ítems reales del libro de calificaciones** (auditoría
    # CDigital 10/08/2026), no solo las tareas: en pregrado 5 de los 8 ítems son
    # cuestionarios (quices y parciales) y antes no aparecían en ningún lado.
    aca_table = "\n".join(
        f"| **{r['code']}** — {r['title']} | {r['corte']} | {r['tipo']} · **{r['weight']}** "
        f"| **{r['fecha']}** | `{r['rel']}` |"
        for r in aca_rows
    )
    # Auto/coevaluación: existen en los 5 cursos (no solo Proyecto I). NO son ACAs
    # — van aparte y rotuladas como instrumentos individuales de cierre.
    instrumentos = [r for r in aca_rows if r["kind"] == "instrumento"]
    documental = [r for r in aca_rows if r["kind"] == "aca"]
    instrumentos_bloque = ""
    arbol_instrumentos = ""
    if instrumentos:
        pesos = " / ".join(dict.fromkeys(r["weight"] for r in instrumentos))
        arbol_instrumentos = (
            f"\n      Autoevaluacion / Coevaluacion individual ({pesos}) - instructivo.docx"
            "   ← no son ACAs"
        )
        lineas = "\n".join(
            f"- **{r['code']}** ({r['weight']}) — se diligencia hasta el **{r['fecha']}** · "
            f"instructivo: `{r['rel']}`"
            for r in instrumentos
        )
        instrumentos_bloque = (
            "\n### Autoevaluación y coevaluación — **no son ACAs**\n\n"
            "Al cierre del curso hay además dos **instrumentos individuales**: no se entrega documento "
            "ni se usa la plantilla APA. **Cada estudiante los diligencia** (tipo formulario) en **CDigital**, "
            "dentro de su ventana. **No sustituyen "
            + (f"la {documental[-1]['code']}" if documental else "el entregable del corte 3")
            + "**; si no los diligencias, ese porcentaje queda en cero.\n\n"
            f"{lineas}\n"
        )
    # Clase autónoma por festivo: el material de esa sesión vive en ESTA carpeta de
    # Drive (no en CDigital, que sigue siendo el sitio de la entrega y de las notas).
    festivo_item = ""
    if es_pregrado:
        festivo_item = (
            "\n4. **Si un día de clase cae festivo**, la sesión **no se cancela**: es "
            "**clase autónoma** y la actividad de ese día queda en la carpeta "
            "`Sesion NN - …/` de esta misma carpeta compartida, junto al material de "
            "la sesión. La **entrega**, como siempre, en **CDigital**."
        )
    tutorias_bloque = ""
    # Solo Proyecto I (AFI). No inventar esta sección en TG2/TG3.
    if key in CURSOS_CON_TUTORIAS_POR_GRUPO:
        tutorias_bloque = (
            "\n---\n\n"
            "## Tutorías por grupo\n\n"
            f"{MSG_TUTORIAS_POR_GRUPO}\n\n"
            "En Proyecto I, la 2.ª hora del encuentro semanal es tutoría/taller en vivo; "
            "las revisiones adicionales por equipo también se acuerdan en la semana. "
            f"Cuando asistas a tutoría, registra asistencia en: {LINK_TUTORIAS}.\n"
        )
    return f"""# Material para estudiantes — {c["titulo"]}

Esta carpeta **`Clases/`** es lo único que el Docente comparte contigo para la asignatura.
Guiones, manuales y calendarios con datos internos **no** van aquí.

**Contacto del Docente:** {DOCENTE_CORREO}

---

## Empieza por aquí

1. Este **LEEME** — mapa de la carpeta y listado de ACAs.
2. **Presentación del Curso** — encuadre, el Docente, {rh["corto"]} y acuerdos.
3. **`Sesion 01 - …/`** — además del deck, trae la **lectura autónoma** de la semana en PDF y el archivo `Lectura autonoma - Sesion 01.txt` con la cita, el enlace y **qué traer a la Sesión 02**. La Sesión 01 es de **encuadre**: no se dicta tema, el contenido arranca en la Sesión 02.
4. **`Recursos/ACAs/`** — enunciados de las entregas evaluadas.

La **bienvenida del curso** (grupo, horario y contacto) la recibes por **correo electrónico** del Docente; no forma parte de esta carpeta compartida.

---

## Enlaces del curso

| Recurso | Enlace / ubicación |
| :--- | :--- |
| {rh["recurso"]} | {rh["url"]} |
| **Google Meet** (mismo enlace toda la serie) | {meet} |
| **CDigital** (campus del curso: entregas y notas) | {aula_txt} |
| **Grabaciones de las clases** (Drive) | {GRABACIONES_URL} |
| **Plantilla APA CUN** | `Recursos/{APA_NAME}` (ábrela en Google Docs / Word Online) |

{rh["como"]}

La carpeta de **grabaciones** es **una sola para todos los cursos y todos los periodos**: dentro se busca por el **nombre del encuentro**, con la forma «periodo - grupo - asignatura - sesión». En este curso, la Sesión 01 se llama **«{evento_s01}»**.

{tutorias_bloque}
---

## Lo que se evalúa (los ítems de CDigital, uno por uno)

Esta tabla es **el libro de calificaciones de tu aula**: cada fila es un ítem que existe en **CDigital** y tiene su propio documento en **`Recursos/ACAs/`**. Los cuestionarios (quices y parciales) **se resuelven en el aula, no se sube archivo**; su documento es la **guía** que te dice qué entra. Las tareas sí se suben. Léelo antes de cada fecha: las notas oficiales solo salen de CDigital.

| Ítem del aula | Corte | Tipo · peso | Cierre | Documento |
| :--- | :---: | :--- | :--- | :--- |
{aca_table}
{instrumentos_bloque}
---

## Cómo está organizada esta carpeta

```text
Clases/
  LEEME - Material para estudiantes.docx   ← este archivo
  {pptx_curso}
  Recursos/
    {APA_NAME}
    ACAs/
      Quiz / Parcial N (peso) - guia del cuestionario.docx   ← qué entra; se resuelve en el aula
      ACA … (peso) - ….docx                                  ← tarea: esto sí se sube{arbol_instrumentos}
  Sesion 01 - …/
    Presentacion.pptx
    Lectura autonoma - Sesion 01.txt       ← qué leer, para cuándo y dónde está
    Lectura … .pdf                          ← la(s) lectura(s), en acceso abierto
    (fichas / capturas de apoyo si aplica)
  Sesion 02 - …/
  …
```

1. **Presentación del Curso** — bienvenida, el Docente, {rh["corto"]} (slide Preséntate), contenido, recursos y acuerdos. La **Sesión 01** de encuadre usa este deck para el Preséntate.
2. **`Sesion NN - <tema>/`** — diapositivas de esa clase (`Presentacion.pptx`) y, si hay, plantillas o capturas de apoyo para el taller. En **`Sesion 01 - …/`** están además la **lectura autónoma** (PDF de acceso abierto) y el `.txt` que dice qué leer, cuánto tarda y qué traer a la Sesión 02: **no hay que buscarla en ningún otro lado**.
3. **`Recursos/`** — plantilla APA + carpeta **`ACAs/`** con los enunciados. No busques estos archivos fuera de `Clases/`.{festivo_item}

---

## Entregas

- Las entregas y notas oficiales van por **CDigital** (cuando esté el enlace del campus).
- Usa la plantilla APA de `Recursos/` cuando el entregable sea documental.
- Sigue el enunciado de `Recursos/ACAs/` correspondiente a cada corte/ACA.
- {rh["cierre"]}

---

*Si falta un enlace (Meet, CDigital o el rompehielos), el Docente lo publicará en el canal del curso; el del rompehielos, además, lo pega en el **chat del Meet** al empezar la Sesión 01.*
"""


def sync_course(key: str) -> None:
    c = COURSES[key]
    clases = os.path.join(c["folder"], "Clases")
    recursos = os.path.join(clases, "Recursos")
    os.makedirs(recursos, exist_ok=True)

    # Enunciados ACA (docx) en Recursos/ACAs/
    build_acas(key)

    # Correo de bienvenida: solo rutas docentes (2026/<grupo>/); limpia si quedó en Clases/
    build_correo(key)
    remove_if_exists(os.path.join(clases, CORREO_NAME))

    cc = carga_curso(key)
    brand_sub = f"Material para estudiantes · {cc['titulo_corto']}"
    brand_foot = f"CUN · {cc['titulo_corto']} · Clases/ · Vigilada Mineducación"
    leeme_docx = os.path.join(clases, LEEME_NAME)
    write_md_as_docx(leeme_md(key), leeme_docx, subtitle=brand_sub, footer=brand_foot)
    print("OK LEEME", leeme_docx)
    remove_if_exists(os.path.join(clases, "LEEME - Material para estudiantes.md"))

    if not os.path.isfile(APA_SRC):
        raise FileNotFoundError(APA_SRC)
    apa_dst = os.path.join(recursos, APA_NAME)
    shutil.copy2(APA_SRC, apa_dst)
    print("OK APA", apa_dst)

    if key == "creatividad":
        s01 = None
        for name in os.listdir(clases):
            if name.startswith("Sesion 01"):
                s01 = os.path.join(clases, name)
                break
        if s01:
            ficha_docx = os.path.join(s01, FICHA_CREATIVIDAD_NAME)
            write_md_as_docx(
                FICHA_CREATIVIDAD_S01,
                ficha_docx,
                subtitle=f"Ficha de taller · {cc['titulo_corto']}",
                footer=brand_foot,
            )
            print("OK ficha", ficha_docx)
            remove_if_exists(os.path.join(s01, "Ficha_problema_oportunidad.md"))
            # Ejemplo modelo (referencia visual) — opcional si existe en Guiones/Capturas
            modelo_src = os.path.join(
                c["folder"], "Guiones", "Capturas", "Sesion 01", "s01_ficha_modelo.html"
            )
            if os.path.isfile(modelo_src):
                modelo_dst = os.path.join(s01, "Ejemplo_ficha_modelo.html")
                shutil.copy2(modelo_src, modelo_dst)
                print("OK ejemplo ficha", modelo_dst)


def main():
    for key in ("proyecto1", "investigacion", "creatividad", "tg2", "tg3"):
        sync_course(key)
    print("Listo: Clases/ sincronizado en los 5 cursos (material estudiante = .docx).")


if __name__ == "__main__":
    main()
