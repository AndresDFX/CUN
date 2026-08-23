# -*- coding: utf-8 -*-
"""Catálogo de sesiones por asignatura CUN (fuente: Syllabus / Manual / calendario).
   Usado por presentación del curso y build_sesion_material.py (Sesion NN).

   Horarios / bloques / grupos 2026: ver `carga_academica_2026.json` (fuente editable).
   Links AFI: `config/universidades/cun.json` → sección `links_afi` (fuente de verdad).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]

try:
    from carga_academica import docente as _docente_pair, curso as _carga_curso, course_dir as _course_dir
    DOCENTE, DOCENTE_CORREO = _docente_pair()
except Exception:  # pragma: no cover — fallback si el JSON no está
    DOCENTE = "Julian Andres Castaño"
    DOCENTE_CORREO = "julian_castanoe@cun.edu.co"
    _carga_curso = None  # type: ignore
    _course_dir = None  # type: ignore

# Perfil proyectado del docente (slide genérico «Docente», sin nombre propio en pantalla).
# Fuente única: la usan build_all_course_presentations.py y build_sesion_material.py.
DOCENTE_CREDS = [
    "Ingeniero de Sistemas",
    "Candidato a MSc en Inteligencia Artificial",
    "Líder Técnico",
    "Speaker Tecnológico",
]


def _abs_folder(key: str, rel_fallback: str) -> str:
    """Ruta absoluta de la asignatura: prioriza `carga_academica_2026.json` → folder."""
    if _course_dir is not None:
        try:
            return str(_course_dir(key))
        except Exception:
            pass
    return str((_ROOT / rel_fallback.replace("\\", "/")).resolve())

_CUN_JSON = Path(__file__).resolve().parent.parent / "universidades" / "cun.json"
_CUN_CACHE: dict | None = None
_FALLBACK_LINKS_AFI = {
    "formulario_asistencia_tutorias_estudiante": "https://forms.gle/oZ8xCYiUo3KEWr1d9",
    "formulario_registro_sesiones_docente": "https://forms.gle/6t6BXqQ2Kwmivpct8",
    "formulario_acuerdo_pedagogico": "https://forms.gle/EPHb7tbrEJTC6ey77",
    "formulario_informe_cierre": (
        "https://docs.google.com/forms/d/e/1FAIpQLSej5yUK3b0p617XhccE7GZrm2C4ra3lk-hzfPTx43uJM_xAmg/viewform"
    ),
    "coanfitrion_meet": "investigacion_especializaciones@cun.edu.co",
}


def load_cun_profile(force: bool = False) -> dict:
    """Perfil institución `config/universidades/cun.json`."""
    global _CUN_CACHE
    if _CUN_CACHE is not None and not force:
        return _CUN_CACHE
    with open(_CUN_JSON, encoding="utf-8") as f:
        _CUN_CACHE = json.load(f)
    return _CUN_CACHE


def links_afi() -> dict:
    """Formularios AFI desde cun.json → `links_afi` (fuente editable)."""
    try:
        data = load_cun_profile().get("links_afi") or {}
        out = dict(_FALLBACK_LINKS_AFI)
        out.update({k: v for k, v in data.items() if not str(k).startswith("_") and isinstance(v, str)})
        return out
    except Exception:  # pragma: no cover
        return dict(_FALLBACK_LINKS_AFI)


_AFI = links_afi()
# Claves canónicas: config/universidades/cun.json → links_afi.*
LINK_TUTORIAS = _AFI["formulario_asistencia_tutorias_estudiante"]
LINK_REGISTRO_DOCENTE_AFI = _AFI["formulario_registro_sesiones_docente"]
LINK_ACUERDO_PEDAGOGICO = _AFI["formulario_acuerdo_pedagogico"]
LINK_INFORME_CIERRE = _AFI["formulario_informe_cierre"]
COANFITRION_MEET_AFI = _AFI["coanfitrion_meet"]

# Solo Proyecto I (AFI · especialización): tutorías por grupo = cita en la semana (no espontáneas).
# NO inventar esta consigna en TG2/TG3 (ni Creatividad/Investigación) salvo que el syllabus lo diga.
MSG_TUTORIAS_POR_GRUPO = (
    "Las tutorías por grupo se acuerdan en la semana con el Docente "
    "(no hay atención espontánea sin cita)."
)
# Alias histórico: solo P1. No incluir tg2/tg3.
CURSOS_CON_TUTORIAS_POR_GRUPO = frozenset({"proyecto1"})
CURSOS_PROYECTO = CURSOS_CON_TUTORIAS_POR_GRUPO  # compat: builds antiguos

# ── Agenda de asesoría del Docente ────────────────────────────────────────────
# OJO, no confundir con LINK_TUTORIAS: aquel es el **formulario de asistencia AFI** que el
# estudiante de Proyecto I diligencia DESPUÉS de una tutoría, y sale de `cun.json`. Este es otro
# asunto y va antes: el estudiante **reserva** un espacio en el calendario del Docente. Por eso
# vive aquí, junto a los datos del Docente, y no en el bloque AFI: no es de la especialización,
# es de la persona, y sirve igual en pregrado.
LINK_AGENDA_ASESORIA = "https://calendar.app.google/1xkHJosUTHdLemvB7"

# Qué cursos lo anuncian, y por qué cada uno:
#   · proyecto1 — su Syllabus lo pide con todas las letras: «tutorías de proyecto»,
#     «acompañamiento metodológico», «Acompañamiento Directo».
#   · tg2 y tg3 — producto de investigación individual que se sustenta ante jurados designados
#     por la Dirección del Programa; el Syllabus reserva horas «Tutorial con Docente».
# Creatividad e Investigación quedan FUERA a propósito: en sus dos Syllabus la casilla
# «Proyectos tutorados» está **sin marcar** (☐), así que anunciar asesoría ahí sería inventarla.
# Si un Syllabus nuevo la marca, se añade aquí y el correo lo recoge solo.
CURSOS_CON_ASESORIA = frozenset({"proyecto1", "tg2", "tg3"})

MSG_AGENDA_ASESORIA = (
    "Si necesitas asesoría sobre tu trabajo, puedes reservar un espacio en mi calendario "
    "cuando te sirva: {enlace} — elige el horario que te quede bien y queda agendado."
)


def _horario_carga(key: str, default: str) -> str:
    if _carga_curso is None:
        return default
    try:
        h = _carga_curso(key)["horario"]
        return h.get("texto_corto") or h["texto"]
    except Exception:
        return default

# Un solo Meet por curso (serie completa).
# Fuente única del enlace real: carga_academica_2026.json → cursos.<key>.meet
# (cadena vacía = el docente aún no creó la sala ⇒ se muestra el placeholder).
# NO hardcodear la URL en los builds: usar `meet_url(course_key, titulo)`.
def meet_placeholder(curso_corto: str) -> str:
    return f"[URL Meet — mismo enlace toda la serie · {curso_corto}]"


def meet_url(course_key: str, curso_corto: str | None = None) -> str:
    """Enlace de Meet de la serie: el real si está en config, si no el placeholder.

    `curso_corto` solo se usa para redactar el placeholder (nombre visible del curso).
    """
    url = ""
    if _carga_curso is not None:
        try:
            url = (_carga_curso(course_key).get("meet") or "").strip()
        except Exception:
            url = ""
    if url:
        return url
    corto = curso_corto or (COURSES.get(course_key, {}).get("titulo") or course_key)
    return meet_placeholder(corto)


# Aula del curso en CDigital (Moodle institucional, https://cdigital.cun.edu.co/).
# Fuente única del enlace real: carga_academica_2026.json → cursos.<key>.cdigital y, cuando
# el curso tiene un aula POR GRUPO, cursos.<key>.grupos.<grupo>.cdigital
# (cadena vacía = aún no se tiene el enlace del aula ⇒ se muestra el placeholder).
# NO hardcodear la URL en los builds: usar `cdigital_url(course_key, grupo)`.
#
# UN AULA POR GRUPO — el caso de TG3 (corregido 2026-08-11)
#   TG3 comparte una sola serie de encuentros pero tiene TRES aulas distintas: 54450 → 112321,
#   54466 → 116387, 54467 → 129270. Antes esta función ignoraba el grupo y devolvía siempre la
#   del curso (la de 54450), así que los correos de bienvenida de 54466 y 54467 mandaban a los
#   estudiantes al aula equivocada — donde no están matriculados y no verían ni sus notas ni
#   sus entregas. Pasa el grupo siempre que lo tengas.
CDIGITAL_PLACEHOLDER = "[URL CDigital — campus del curso pendiente]"


def cdigital_url(course_key: str, grupo: str | None = None) -> str:
    """Enlace del aula en CDigital. Con `grupo`, la del grupo si el curso tiene una por grupo."""
    url = ""
    if _carga_curso is not None:
        try:
            c = _carga_curso(course_key)
            if grupo:
                url = (((c.get("grupos") or {}).get(str(grupo)) or {}).get("cdigital") or "").strip()
            if not url:
                url = (c.get("cdigital") or "").strip()
        except Exception:
            url = ""
    return url or CDIGITAL_PLACEHOLDER


def cdigital_urls_por_grupo(course_key: str) -> dict[str, str]:
    """`{grupo: url}` cuando el curso tiene un aula por grupo; `{}` si comparte una sola.

    Lo necesita todo lo que se comparte a la vez con varios grupos —el LEEME del estudiante
    de `Clases/`, por ejemplo— donde no se puede enseñar una sola aula sin equivocarse con dos
    tercios del curso.
    """
    if _carga_curso is None:
        return {}
    try:
        c = _carga_curso(course_key)
    except Exception:
        return {}
    aulas = {
        str(g): (m.get("cdigital") or "").strip()
        for g, m in (c.get("grupos") or {}).items()
        if (m.get("cdigital") or "").strip()
    }
    return aulas if len(set(aulas.values())) > 1 else {}


def cdigital_frase(course_key: str) -> str:
    """Cómo se nombra el aula en material que se proyecta a **todos** los grupos a la vez.

    Existe porque las decks de sesión traían la URL escrita a mano en el JSON de cada sesión —53
    bloques— y esa copia se quedó con el placeholder, así que el estudiante veía proyectado
    «[URL CDigital — campus del curso pendiente]» aunque el aula sí estuviera registrada.

    En TG3 devuelve una frase, no una URL: son **tres** aulas para una sola serie de encuentros,
    y cualquier URL única sería la equivocada para dos tercios del curso.
    """
    if cdigital_urls_por_grupo(course_key):
        return "el aula de **su grupo** en CDigital"
    url = cdigital_url(course_key)
    return url if url != CDIGITAL_PLACEHOLDER else "el aula del curso en **CDigital**"


# Convención carpetas (raíz de asignatura, GENÉRICO — sin código de grupo):
#   Clases/Presentacion del Curso - ....pptx
#   Clases/Sesion 01 - <Nombre del tema>/Presentacion.pptx  ← numerada + tema
#   Docente/Guiones/Sesion 01 - <Nombre del tema>.md        ← numerado + tema (solo .md)
#   Docente/Guiones/Capturas/
# PPTX de sesión: SIN bio/correo del docente (eso solo en Presentación del Curso).
#
# REGLA · TÍTULOS DE SESIÓN SIN FECHAS (obligatoria, verificada al importar):
#   El `titulo` nombra el TEMA, nunca una fecha ni una ventana («… (hasta 22 nov)»).
#   La fecha sale siempre del modelo: `fecha` de esta misma sesión para el día del
#   encuentro y `config/cursos/fechas_entrega_aca.py` para aperturas, cierres y
#   límites de nota. Un título con fecha se congela en el nombre de la carpeta
#   `Clases/Sesion NN - <tema>/` y del guion `.md`, y sigue mintiendo aunque el
#   modelo cambie (fue el caso de TG3 S15: anunciaba el 22/11 y la ACA Final cerraba
#   el 14/11 en 54466/54467 y el 07/11 en 54450). Si necesita matizar, use `detalle`.
#   La verifica `_verificar_titulos_sin_fecha()` al final de este módulo.

COURSES = {
    "proyecto1": {
        "key": "proyecto1",
        "folder": _abs_folder("proyecto1", "Especializacion/Proyecto I"),
        "titulo": "PROYECTO I",
        "titulo_largo": "Proyecto I — Especialización en Inteligencia Artificial",
        "codigo": "ESP329",
        "horario": _horario_carga("proyecto1", "Lunes, 8:00 pm – 10:00 pm"),
        "duracion_min": 120,  # 60 contenido + 60 tutoría
        "contenido_min": 60,
        "fuente": (
            "Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx "
            "(fuente primaria) · Instructivo/Cronograma AFI 26ES4 (operativa) · Manual del Docente"
        ),
        "nota_syllabus": (
            "Temario curricular = 7 unidades didácticas del ESP329. "
            "Las 11 sesiones semanales del calendario AFI desarrollan esas unidades."
        ),
        # `bloque` = el ítem del aula al que apunta el tramo de sesiones, con el NOMBRE
        # EXACTO del libro de calificaciones de CDigital (ver `fechas_entrega_aca.py` →
        # ACA_COMPONENTES["proyecto1"]): Quiz (25%, corte 1) · ACA 1 (25%, corte 2) ·
        # ACA FINAL (42%, corte 3). El esquema viejo «ACA 1 / ACA 2 / ACA 3 / Puente»
        # del ESP329 se retiró el 2026-08-11: colisionaba con los nombres del aula y
        # hacía creer al estudiante que había perdido un ítem que apenas se le abría.
        "sesiones": [
            {"n": 1, "fecha": "10/08/2026",
             "titulo": "Presentación del curso · docente · estudiantes · ACAs", "bloque": "Encuadre",
             "unidad_esp329": "—",
             "presentacion": True,
             "unidad_diferida": "ESP329 U1 (Fundamentos y enfoque de investigación) → lectura autónoma; se retoma al abrir la Sesión 02.",
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes y de las ACAs (peso, fechas, formato APA). No se dicta tema."},
            {"n": 2, "fecha": "24/08/2026",
             "titulo": "Problema y pregunta de investigación", "bloque": "Quiz",
             "unidad_esp329": "U2",
             "detalle": "ESP329 U2 · Delimitación del problema · pregunta viable · líneas IA del programa."},
            {"n": 3, "fecha": "31/08/2026",
             "titulo": "Objetivos, justificación, alcances y limitaciones", "bloque": "Quiz",
             "unidad_esp329": "U3",
             "detalle": "ESP329 U3 · Objetivo general/específicos · justificación · alcances/limitaciones · el Quiz (cuestionario, corte 1) cerró el domingo anterior: la última sincrónica antes de su cierre fue la Sesión 02."},
            {"n": 4, "fecha": "07/09/2026",
             "titulo": "Retroalimentación del Quiz · Antecedentes de investigación", "bloque": "ACA 1",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Retro del Quiz (cuestionario del corte 1) · hoy ABRE la ACA 1 (tarea, corte 2) · antecedentes (mín. 6 nacionales/internacionales)."},
            {"n": 5, "fecha": "14/09/2026",
             "titulo": "Marco teórico", "bloque": "ACA 1",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Bases teóricas alineadas a pregunta y variables/categorías."},
            {"n": 6, "fecha": "21/09/2026",
             "titulo": "Marco conceptual y marco contextual", "bloque": "ACA 1",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Definiciones operativas y contexto de aplicación."},
            {"n": 7, "fecha": "28/09/2026",
             "titulo": "Marco legal · citación APA 7", "bloque": "ACA 1",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Marco legal si aplica · citación/referencias · última sincrónica antes del cierre de la ACA 1."},
            {"n": 8, "fecha": "05/10/2026",
             "titulo": "Diseño metodológico: paradigma, enfoque y alcance", "bloque": "ACA FINAL",
             "unidad_esp329": "U5",
             "detalle": "ESP329 U5 · Adelantar metodología antes de los festivos del tramo de la ACA FINAL."},
            {"n": 9, "fecha": "19/10/2026",
             "titulo": "Devolución de la ACA 1 · población, muestra e instrumentos propuestos",
             "bloque": "ACA FINAL",
             "unidad_esp329": "U5",
             "detalle": "ESP329 U5 · Primeros 20 min: devolución de la ACA 1 con la rúbrica en pantalla (qué se corrige antes de la ACA FINAL, que exige trazabilidad de esas correcciones) · luego población/muestra e instrumentos PROPUESTOS (no aplicados en Proyecto I)."},
            {"n": 10, "fecha": "26/10/2026",
             "titulo": "Planeación, viabilidad e integración del anteproyecto", "bloque": "ACA FINAL",
             "unidad_esp329": "U6–U7",
             "detalle": "ESP329 U6–U7 · Cronograma, presupuesto e integración · última sincrónica antes del cierre de la ACA FINAL."},
            {"n": 11, "fecha": "09/11/2026",
             "titulo": "Integración y evaluación · coevaluación y autoevaluación", "bloque": "Cierre",
             "unidad_esp329": "U7",
             "detalle": "ESP329 U7 · Coherencia final · coevaluación/autoevaluación · última sesión sincrónica."}
        ],
    },
    "investigacion": {
        "key": "investigacion",
        "folder": _abs_folder("investigacion", "Pregrado/Investigacion en ciencia y tecnologia"),
        "titulo": "INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA",
        "titulo_largo": "Investigación Ciencia y Tecnología — Escuela de Ingenierías",
        "codigo": "EI005",
        "horario": _horario_carga("investigacion", "Jueves, 5:00 pm – 6:00 pm"),
        "duracion_min": 60,
        "contenido_min": 60,
        "fuente": "Syllabus SIAC EI005_PRES",
        "nota_syllabus": (
            "Numeración del Syllabus salta N° 3 y 9. Periodo corto 26P03: el rango institucional "
            "tiene 7 jueves calendario (06/08–17/09), pero el inicio operativo del semestre es el "
            "10/08, así que se dictan **6** (13/08–17/09) y el periodo cierra el 20/09. "
            "TEMARIO ADELANTADO (2026-08-11): la ACA Final (el artículo) califica marco teórico y "
            "revisión de literatura y cierra el 12/09, así que **U8** (bases de datos CUN y gestores "
            "de citas) pasa a la **Sesión 04** y **U10–U12** (posturas teóricas · marco teórico y "
            "revisión) a la **Sesión 05**. Ninguna unidad se elimina: es un reorden, no un recorte. "
            "La Sesión 06 (17/09) queda como socialización del artículo y cierre, sin evaluación."
        ),
        "unidades_syllabus": [
            "U1 Presentación del Syllabus y producto final (artículo)",
            "U2 Fundamentos del método científico",
            "U4 MinCiencias · 6 líneas de Ingeniería",
            "U5 Prueba parcial · 1.er avance del artículo",
            "U6 Identificación de problemas y pregunta",
            "U7 Formulación del planteamiento del problema",
            "U8 Bases de datos CUN + gestores de citas",
            "U10–12 Posturas teóricas · marco teórico y revisión de literatura",
        ],
        "sesiones": [
            {"n": 1, "fecha": "13/08/2026", "titulo": "Presentación del curso · docente · estudiantes · ACAs", "bloque": "Encuadre",
             "presentacion": True,
             "unidad_diferida": "U1–U2 (Syllabus y producto final · fundamentos del método científico) → lectura autónoma; se retoma al abrir la Sesión 02.",
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes y de las ACAs (peso, fechas, formato). No se dicta tema."},
            {"n": 2, "fecha": "20/08/2026", "titulo": "MinCiencias · 6 líneas de Ingeniería · elección de línea", "bloque": "U4",
             "detalle": "IoT, Big Data, IA, cloud/FinTech, aplicaciones, telemática."},
            {"n": 3, "fecha": "27/08/2026", "titulo": "Prueba parcial · 1.er avance del artículo", "bloque": "U5",
             "detalle": "Talleres/sustentaciones · tipos de conocimiento y fuentes."},
            {"n": 4, "fecha": "03/09/2026", "titulo": "Problema y pregunta · bases de datos y gestores de citas", "bloque": "U6+U8",
             "detalle": "U6+U8 en un solo encuentro: espina de pescado, árbol de problemas y método 3D hasta la pregunta · Scholar, SciELO, Redalyc y biblioteca CUN · operadores de búsqueda y citación APA 7 con ZoteroBib. U8 se adelanta porque la ACA Final la califica y cierra antes de la Sesión 06."},
            {"n": 5, "fecha": "10/09/2026", "titulo": "Planteamiento del problema · marco teórico y revisión de literatura", "bloque": "U7+U10–12",
             "detalle": "U7+U10–U12 en un solo encuentro: estado actual, evidencias, causas y vacío hasta cerrar en la pregunta · constructos, posturas teóricas, fichas de lectura y primera página de marco. Última sincrónica antes del cierre de la ACA Final y del Quiz 3."},
            {"n": 6, "fecha": "17/09/2026", "titulo": "Socialización del artículo y cierre del curso", "bloque": "Cierre",
             "detalle": "Cierre sin evaluación nueva: la ACA Final y el Quiz 3 ya cerraron. Ronda de socialización del artículo, retroalimentación entre pares, ruta hacia semillero y trabajo de grado, y diligenciamiento de autoevaluación y coevaluación, que abren este día en CDigital."}
        ],
    },
    "creatividad": {
        "key": "creatividad",
        "folder": _abs_folder("creatividad", "Pregrado/Creatividad y pensamiento innovador"),
        "titulo": "CREATIVIDAD Y PENSAMIENTO INNOVADOR",
        "titulo_largo": "Creatividad y Pensamiento Innovador — Escuela de Ingenierías",
        "codigo": "EI004",
        "horario": _horario_carga("creatividad", "Miércoles, 5:00 pm – 6:00 pm"),
        "duracion_min": 60,
        "contenido_min": 60,
        "fuente": "Syllabus SIAC EI004_VIR",
        "nota_syllabus": (
            "TEMARIO ADELANTADO (2026-08-11): la ACA Final califica «Ecosistema: entidades de apoyo» "
            "(**U8**) y cierra el 19/09, cuatro días antes de la Sesión 07, donde U8 se dictaba. "
            "**U7** (vigilancia tecnológica) pasa a la **Sesión 05** —junto con U6, que ya vivía ahí— "
            "y **U8** a la **Sesión 06**; la Sesión 07 queda como taller de consolidación y "
            "sustentación. Ninguna unidad se elimina: es un reorden, no un recorte. U1–U2 siguen en "
            "lectura autónoma desde la Sesión 01."
        ),
        "sesiones": [
            {"n": 1, "fecha": "12/08/2026", "titulo": "Presentación del curso · docente · estudiantes · ACAs", "bloque": "Encuadre",
             "presentacion": True,
             "unidad_diferida": "U1–U2 (Propuesta de Innovación · creatividad e inteligencia emocional) → lectura autónoma; se retoma al abrir la Sesión 02.",
             # Documento publicado aparte del deck, en la carpeta de la sesión y como recurso del
             # aula. Su consigna le dice al estudiante que NO entra en el Quiz 1; sí entra desde
             # el Parcial 1, y el banco de ese parcial ya lo evalúa. `excluido_de` mantiene las dos
             # guías diciendo lo mismo que la consigna, sin que haya que recordarlo a mano.
             "material_estudio": [
                 {"nombre": "Material de estudio U2 — Bloqueadores y ensanchadores de la creatividad",
                  "detalle": "bloqueadores perceptivos, emocionales y culturales · ensanchadores · "
                             "la inteligencia emocional como insumo de la creatividad · autodiagnóstico",
                  "excluido_de": ["Quiz 1"]},
             ],
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes y de las ACAs (peso, fechas, formato). No se dicta tema."},
            {"n": 2, "fecha": "19/08/2026", "titulo": "Creatividad/innovación en I+D · Design Thinking y técnicas", "bloque": "U3",
             "detalle": "Pensamiento divergente/convergente · ideación."},
            {"n": 3, "fecha": "26/08/2026", "titulo": "Gestión de la innovación (Manual de Oslo / OCDE)", "bloque": "U4",
             "detalle": "Métodos en producto, proceso, organización, marketing, social."},
            {"n": 4, "fecha": "02/09/2026", "titulo": "Tipos de innovación", "bloque": "U5",
             "detalle": "Cuadro comparativo · mejoras en contextos socio-económicos."},
            {"n": 5, "fecha": "09/09/2026", "titulo": "Validación de la propuesta · vigilancia tecnológica", "bloque": "U6–U7",
             "detalle": "U6+U7 en un solo encuentro: FODA, Canvas y MVP · prueba del supuesto más riesgoso con criterio fijado antes · tablero de vigilancia (Scholar/Patents) que termina en una decisión. U7 se adelanta porque la ACA Final la califica."},
            {"n": 6, "fecha": "16/09/2026", "titulo": "Innovación local–internacional · entidades de apoyo", "bloque": "U8",
             "detalle": "U8 adelantada una sesión: escalas local–regional–nacional–internacional, tipos de impacto, mapa de entidades reales con un pedido concreto y guion del pitch de 60 s. Última sincrónica antes del cierre de la ACA Final, que califica ecosistema y pitch."},
            {"n": 7, "fecha": "23/09/2026", "titulo": "Taller de consolidación y sustentación de la propuesta", "bloque": "Cierre",
             "detalle": "Cierre sin evaluación nueva: la ACA Final y el Quiz 3 ya cerraron. Sustentación cruzada con el pitch de 60 s, revisión de coherencia del paquete consolidado y diligenciamiento de autoevaluación y coevaluación, que abren este día en CDigital."}
        ],
    },
    "tg2": {
        "key": "tg2",
        "folder": _abs_folder("tg2", "Pregrado/Trabajo de grado 2"),
        "titulo": "TRABAJO DE GRADO 2",
        "titulo_largo": "Trabajo de Grado 2 — Modelos de Innovación (Ing. Sistemas)",
        "codigo": "94453",
        "horario": _horario_carga("tg2", "Lunes, 5:00 pm – 6:00 pm"),
        "duracion_min": 60,
        "contenido_min": 60,
        "fuente": "Syllabus SIAC oficial (entregado el 22/08/2026) · Manual del Docente",
        "nota_syllabus": "Syllabus recibido el 22/08/2026: «TRABJO DE GRADO II INGENIERIA DE SISTEMAS.docx», sin código SIAC en el nombre. 6 unidades didácticas.",
        "sesiones": [
            # EXCEPCIÓN puntual: esta sesión se corrió del lunes 10/08 al viernes 14/08 porque
            # la clase del lunes no se pudo dar (decisión del Docente, 11/08/2026). Es la ÚNICA
            # sesión de TG2 que no cae en lunes; de la S02 en adelante el curso sigue su horario
            # normal, lunes 5:00–6:00 pm. No cambiar el `weekday` del curso por esto.
            {"n": 1, "fecha": "14/08/2026", "titulo": "Presentación del curso · docente · estudiantes · ACAs", "bloque": "Encuadre",
             "presentacion": True,
             "reprogramada": "Del lunes 10/08 al viernes 14/08: la sesión del lunes no se pudo dar. Misma hora (5:00–6:00 pm). La Sesión 02 vuelve al lunes.",
             "unidad_diferida": "Delimitación / reformulación del tema → lectura autónoma; se retoma al abrir la Sesión 02. (El acuerdo pedagógico se firma en esta sesión de encuadre.)",
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes y de las ACAs (peso, fechas, formato APA) + acuerdo pedagógico. No se dicta tema. Sesión reprogramada al viernes 14/08; la Sesión 02 vuelve al lunes."},
            {"n": 2, "fecha": "24/08/2026", "titulo": "Pregunta, objetivos y título provisional", "bloque": "Orientativo",
             "detalle": "17/08 es clase autónoma (festivo)."},
            {"n": 3, "fecha": "31/08/2026", "titulo": "Estructura del documento de avance", "bloque": "Orientativo",
             "detalle": "Plantilla APA CUN. El esqueleto es el mismo para cualquier modalidad de grado."},
            {"n": 4, "fecha": "07/09/2026", "titulo": "Antecedentes y referentes (Fase I)", "bloque": "Orientativo",
             "detalle": "Búsqueda en bases CUN."},
            {"n": 5, "fecha": "14/09/2026", "titulo": "Marco teórico — avance", "bloque": "Orientativo",
             "detalle": "Variables y bases teóricas."},
            {"n": 6, "fecha": "21/09/2026", "titulo": "Marco conceptual y contextual", "bloque": "Orientativo",
             "detalle": "Definiciones operativas."},
            {"n": 7, "fecha": "28/09/2026", "titulo": "Diseño metodológico (propuesto)", "bloque": "Orientativo",
             "detalle": "Enfoque, tipo, alcance."},
            {"n": 8, "fecha": "05/10/2026", "titulo": "Instrumentos y plan de análisis (propuestos)", "bloque": "Orientativo",
             "detalle": "12/10 clase autónoma (festivo)."},
            {"n": 9, "fecha": "19/10/2026", "titulo": "Integración del avance · correcciones", "bloque": "Orientativo",
             "detalle": "Documento consolidado."},
            {"n": 10, "fecha": "26/10/2026", "titulo": "Socialización de avances", "bloque": "Orientativo",
             "detalle": "Retroalimentación entre pares/docente."},
            {"n": 11, "fecha": "09/11/2026", "titulo": "Cierre del avance · preparación para TG3", "bloque": "Orientativo",
             "detalle": "02/11 y 16/11 clases autónomas (festivos)."}
        ],
    },
    "tg3": {
        "key": "tg3",
        "folder": _abs_folder("tg3", "Pregrado/Trabajo de grado 3"),
        "titulo": "TRABAJO DE GRADO 3",
        "titulo_largo": "Trabajo de Grado 3 — Modelos de Innovación (Ing. Sistemas)",
        "codigo": "94532",
        "horario": _horario_carga("tg3", "Martes, 5:00 pm – 6:00 pm"),
        "duracion_min": 60,
        "contenido_min": 60,
        "fuente": "Syllabus SIAC 94532 (14 unidades)",
        "nota_syllabus": None,
        "sesiones": [
            {"n": 1, "fecha": "11/08/2026", "titulo": "Presentación del curso · docente · estudiantes · ACAs", "bloque": "Encuadre",
             "presentacion": True,
             "unidad_diferida": "U1–U2 (Casos de éxito · retomar proyecto · contexto y planteamiento) → lectura autónoma; se retoma al abrir la Sesión 02. (El acuerdo pedagógico se firma en esta sesión de encuadre.)",
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes y de las ACAs (peso, fechas, formato APA) + acuerdo pedagógico. No se dicta tema."},
            {"n": 2, "fecha": "18/08/2026", "titulo": "Formulación de pregunta, objetivos y título", "bloque": "U3",
             "detalle": "Variables en la pregunta-problema."},
            {"n": 3, "fecha": "25/08/2026", "titulo": "Estructura del documento · taller de introducción", "bloque": "U4",
             "detalle": "Contexto, problema, pregunta y objetivos. Mismo esqueleto para cualquier modalidad."},
            {"n": 4, "fecha": "01/09/2026", "titulo": "Fase I de referentes de investigación", "bloque": "U5",
             "detalle": "Diálogo colaborativo."},
            {"n": 5, "fecha": "08/09/2026", "titulo": "Diseño de instrumento · desarrollo metodológico", "bloque": "U6",
             "detalle": "Prototipado / obra-creación."},
            {"n": 6, "fecha": "15/09/2026", "titulo": "Comunidades de práctica y co-creación", "bloque": "U7",
             "detalle": "Socialización de problemas y propuestas."},
            {"n": 7, "fecha": "22/09/2026", "titulo": "Experiencia creativa · análisis de datos", "bloque": "U8",
             "detalle": "Socialización del avance."},
            {"n": 8, "fecha": "29/09/2026", "titulo": "Fase III de referentes · cierre del marco teórico", "bloque": "U9",
             "detalle": "Cuerpo del documento (revisión literaria)."},
            {"n": 9, "fecha": "06/10/2026", "titulo": "Resultados, discusión y relación con referentes", "bloque": "U10",
             "detalle": "Hallazgos vs. literatura."},
            {"n": 10, "fecha": "13/10/2026", "titulo": "Resumen, palabras clave UNESCO, conclusiones y referencias", "bloque": "U11",
             "detalle": "Culminación del documento."},
            {"n": 11, "fecha": "20/10/2026", "titulo": "Póster · evidencias · verificación antiplagio", "bloque": "U12",
             "detalle": "Alistamiento para sustentación."},
            {"n": 12, "fecha": "27/10/2026", "titulo": "Sustentación ante jurados", "bloque": "U13",
             "detalle": "Defensa oral del proyecto."},
            {"n": 13, "fecha": "03/11/2026", "titulo": "Entregables para repositorio institucional", "bloque": "U14",
             "detalle": "Cierre formal del trabajo de grado (Syllabus U1–U14 completo)."},
            {"n": 14, "fecha": "10/11/2026", "titulo": "Ajustes finales · seguimiento post-sustentación", "bloque": "Buffer",
             "detalle": "Fecha calendario extra tras U14. Grupo 54450: última martes antes del cierre 15/11 (recepción 07/11)."},
            {"n": 15, "fecha": "17/11/2026", "titulo": "Cierre administrativo · recepción de entregables", "bloque": "Buffer",
             "detalle": "Solo grupos 54466/54467 (26V04): cae después de la recepción de su ACA Final y antes del cierre de notas. El 54450 NO tiene esta fecha: su periodo ya cerró. Las fechas exactas se leen en CDigital."}
        ],
    },
}


# ---------------------------------------------------------------------------
# Regla «títulos de sesión sin fechas» — se verifica al importar el módulo
# ---------------------------------------------------------------------------
# El título viaja al nombre de la carpeta `Clases/Sesion NN - <tema>/` y del guion
# `.md`: una fecha escrita ahí sobrevive a cualquier cambio del calendario y le
# queda mintiendo al estudiante. Las fechas se leen del modelo (`fecha` de la
# sesión · `config/cursos/fechas_entrega_aca.py`), nunca del título.
_MES_ABREV = r"ene|feb|mar|abr|may|jun|jul|ago|sep|sept|oct|nov|dic"
_MES_LARGO = (
    r"enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
    r"septiembre|setiembre|octubre|noviembre|diciembre"
)
_RE_FECHA_EN_TITULO = re.compile(
    r"\d{1,2}\s*/\s*\d{1,2}"                                  # 22/11 · 22/11/2026
    rf"|\b\d{{1,2}}\s*(?:de\s+)?(?:{_MES_ABREV}|{_MES_LARGO})\b"  # 22 nov · 22 de noviembre
    rf"|\b(?:{_MES_ABREV}|{_MES_LARGO})\.?\s+\d{{1,2}}\b",        # nov 22 · noviembre 22
    re.IGNORECASE,
)


def titulos_con_fecha() -> list[str]:
    """Sesiones cuyo `titulo` trae una fecha. Debe devolver SIEMPRE lista vacía."""
    malos: list[str] = []
    for key, c in COURSES.items():
        for s in c.get("sesiones") or []:
            titulo = s.get("titulo") or ""
            if _RE_FECHA_EN_TITULO.search(titulo):
                malos.append(f"{key} S{int(s.get('n', 0)):02d}: «{titulo}»")
    return malos


def _verificar_titulos_sin_fecha() -> None:
    malos = titulos_con_fecha()
    if malos:
        raise ValueError(
            "Título de sesión con fecha (la fecha sale del modelo, no del título; "
            "si hay que matizar, va en `detalle`): " + " · ".join(malos)
        )


_verificar_titulos_sin_fecha()


# ---------------------------------------------------------------------------
# Subject de Calendar (encuentros CSV/ICS) — patrón único los 5 cursos
# ---------------------------------------------------------------------------
# Formato canónico (CSV/ICS encuentros · los 5 cursos):
#   {periodo} - {grupos} - {Asignatura corta} - Sesion NN
#   Varios grupos: 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 03
# Sin nombre largo del tema (el tema va en Description).
# Festivo Pregrado (clase autónoma) — mismo patrón + sufijo:
#   {periodo} - {grupos} - {Asignatura} - Sesion NN (autónoma)
#
# POR QUÉ EL PERIODO VA DE PRIMERO (2026-08-11, decisión del Docente):
#   El nombre del evento es la clave de búsqueda de la carpeta única de grabaciones
#   («periodo - grupo - asignatura - sesion»). Esa carpeta acumula TODOS los periodos,
#   así que sin el prefijo, dentro de un mismo año hay varios «54448 - Trabajo de
#   Grado 2 - Sesion 01» indistinguibles. El periodo NO es una constante del build:
#   se deriva de los MISMOS grupos que entran en el Subject (carga_academica_2026.json
#   → cursos.<key>.grupos.<grupo>.periodo), porque TG3 corre los tres grupos en una
#   sola serie con dos periodos (54450 = 26P04 · 54466/54467 = 26V04) y porque el
#   calendario recorta grupos ya cerrados en las últimas fechas.
# ---------------------------------------------------------------------------

def titulo_para_calendar(course_key: str) -> str:
    """Nombre corto amigable para Subject (antes del guión tipográfico del título largo)."""
    c = COURSES.get(course_key) or {}
    tl = (c.get("titulo_largo") or c.get("titulo") or course_key).strip()
    for sep in (" — ", " – ", " - "):
        if sep in tl:
            return tl.split(sep, 1)[0].strip()
    return tl


def groups_subject_label(groups: list[str]) -> str:
    """Códigos de grupo(s) en Subject: '54ES4' o '54450/54466/54467'."""
    gs = [str(g).strip() for g in groups if str(g).strip()]
    if not gs:
        return "—"
    return "/".join(gs)


# Avisos ya emitidos (course_key, grupos sin periodo): `subject_encuentro` se llama una vez
# por sesión, y sin memoria el mismo aviso saldría 11–15 veces por curso.
_PERIODO_AVISADO: set[tuple[str, str]] = set()


def periodo_de_grupo(course_key: str, grupo: str) -> str:
    """Periodo del grupo (26ES4 · 26V04 · 26P03 · 26P04) desde `carga_academica_2026.json`.

    Cadena vacía si no está el JSON, el curso, el grupo o el campo `periodo`.
    """
    if _carga_curso is None:
        return ""
    try:
        grupos = _carga_curso(course_key).get("grupos") or {}
        return str((grupos.get(str(grupo).strip()) or {}).get("periodo") or "").strip()
    except Exception:
        return ""


def periodos_subject_label(course_key: str, groups: list[str]) -> str:
    """Periodo(s) en Subject: '26V04' o '26P04/26V04' — de los MISMOS grupos del Subject.

    Sin repetir y en el orden en que llegan los grupos (el mismo que usa
    `groups_subject_label`, para que las dos etiquetas se lean en paralelo).
    Si algún grupo no trae periodo devuelve '' (Subject sin prefijo) y avisa por
    consola: un Subject a medias —unos eventos con periodo y otros sin él— rompe la
    búsqueda de grabaciones más que no ponerlo.
    """
    gs = [str(g).strip() for g in groups if str(g).strip()]
    if not gs:
        return ""
    periodos: list[str] = []
    faltantes: list[str] = []
    for g in gs:
        p = periodo_de_grupo(course_key, g)
        if not p:
            faltantes.append(g)
        elif p not in periodos:
            periodos.append(p)
    if faltantes:
        clave = (course_key, "/".join(faltantes))
        if clave not in _PERIODO_AVISADO:
            _PERIODO_AVISADO.add(clave)
            print(
                f"[sesiones_cun] AVISO: sin `periodo` para {course_key} → grupo(s) "
                f"{clave[1]} en carga_academica_2026.json "
                "(cursos.<key>.grupos.<grupo>.periodo). El Subject de esos encuentros "
                "sale SIN prefijo de periodo y no se podrá buscar en la carpeta de "
                "grabaciones con «periodo - grupo - asignatura - sesion».",
                file=sys.stderr,
            )
        return ""
    return "/".join(periodos)


def subject_encuentro(
    course_key: str,
    groups: list[str],
    *,
    n: int | None = None,
    titulo_sesion: str | None = None,
    autonoma: bool = False,
    festivo_nombre: str | None = None,
) -> str:
    """Arma el Subject corto de un evento de encuentro (sincrónico o autónomo).

    Patrón: ``{periodo} - {grupos} - {Asignatura} - Sesion NN`` (sin tema largo).
    El periodo sale de los mismos `groups` (ver `periodos_subject_label`); si falta,
    el Subject cae al patrón anterior ``{grupos} - {Asignatura} - …`` y se avisa.
    ``titulo_sesion`` se ignora en el Subject (queda en Description del evento).
    Festivo sin entrada en catálogo:
    ``{periodo} - {grupos} - {Asignatura} - Clase autonoma (…)``.
    Día festivo con sesión de catálogo: mismo patrón Sesion NN + `` (autónoma)``.
    """
    curso = titulo_para_calendar(course_key)
    g_lbl = groups_subject_label(groups)
    p_lbl = periodos_subject_label(course_key, groups)
    pref = f"{p_lbl} - " if p_lbl else ""
    # titulo_sesion: aceptado por compatibilidad; no va en el Subject corto.
    _ = (titulo_sesion or "").strip()
    if n is not None:
        core = f"{pref}{g_lbl} - {curso} - Sesion {int(n):02d}"
    elif autonoma:
        fest = f" ({festivo_nombre})" if festivo_nombre else ""
        core = f"{pref}{g_lbl} - {curso} - Clase autonoma{fest}"
    else:
        core = f"{pref}{g_lbl} - {curso} - Encuentro"
    # Solo la rama `Sesion NN` necesita el sufijo: la rama `Clase autonoma (Festivo)` ya
    # dice que es autónoma, y añadirlo otra vez daba «Clase autonoma (Asunción…) (autónoma)».
    if autonoma and n is not None and not core.rstrip().endswith("(autónoma)"):
        core = f"{core} (autónoma)"
    return core


def tema_por_fecha(course_key: str) -> dict[str, dict]:
    """Mapa dd/mm/YYYY → sesión de este catálogo."""
    course = COURSES.get(course_key) or {}
    out: dict[str, dict] = {}
    for s in course.get("sesiones") or []:
        f = s.get("fecha")
        if f:
            out[f] = s
    return out
