# -*- coding: utf-8 -*-
"""Catálogo de sesiones por asignatura CUN (fuente: Syllabus / Manual / calendario).
   Usado por presentación del curso y build_sesion_material.py (Sesion NN).

   Horarios / bloques / grupos 2026: ver `carga_academica_2026.json` (fuente editable).
   Links AFI: `config/universidades/cun.json` → sección `links_afi` (fuente de verdad).
"""
from __future__ import annotations

import json
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


def _horario_carga(key: str, default: str) -> str:
    if _carga_curso is None:
        return default
    try:
        h = _carga_curso(key)["horario"]
        return h.get("texto_corto") or h["texto"]
    except Exception:
        return default

# Un solo Meet por curso (serie completa). Sustituir el placeholder cuando exista el enlace real.
def meet_placeholder(curso_corto: str) -> str:
    return f"[URL Meet — mismo enlace toda la serie · {curso_corto}]"


# Convención carpetas (raíz de asignatura, GENÉRICO — sin código de grupo):
#   Clases/Presentacion del Curso - ....pptx
#   Clases/Sesion 01 - <Nombre del tema>/Presentacion.pptx  ← numerada + tema
#   Guiones/Sesion 01 - <Nombre del tema>.md                ← numerado + tema (solo .md)
#   Guiones/Capturas/
# PPTX de sesión: SIN bio/correo del docente (eso solo en Presentación del Curso).

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
        "sesiones": [
            {"n": 1, "fecha": "10/08/2026",
             "titulo": "Presentación del curso · docente · estudiantes · ACAs", "bloque": "Encuadre",
             "unidad_esp329": "—",
             "presentacion": True,
             "unidad_diferida": "ESP329 U1 (Fundamentos y enfoque de investigación) → lectura autónoma; se retoma al abrir la Sesión 02.",
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes (Padlet) y de las ACAs (peso, fechas, formato APA). No se dicta tema."},
            {"n": 2, "fecha": "24/08/2026",
             "titulo": "Problema y pregunta de investigación", "bloque": "ACA 1",
             "unidad_esp329": "U2",
             "detalle": "ESP329 U2 · Delimitación del problema · pregunta viable · líneas IA del programa."},
            {"n": 3, "fecha": "31/08/2026",
             "titulo": "Objetivos, justificación, alcances y limitaciones", "bloque": "ACA 1",
             "unidad_esp329": "U3",
             "detalle": "ESP329 U3 · Objetivo general/específicos · justificación · alcances/limitaciones · ACA1 ya cerró (dom 30/08); la última sincrónica antes del cierre es la Sesión 02."},
            {"n": 4, "fecha": "07/09/2026",
             "titulo": "Retroalimentación ACA1 · Antecedentes de investigación", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Retro ACA1 · antecedentes (mín. 6 nacionales/internacionales)."},
            {"n": 5, "fecha": "14/09/2026",
             "titulo": "Marco teórico", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Bases teóricas alineadas a pregunta y variables/categorías."},
            {"n": 6, "fecha": "21/09/2026",
             "titulo": "Marco conceptual y marco contextual", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Definiciones operativas y contexto de aplicación."},
            {"n": 7, "fecha": "28/09/2026",
             "titulo": "Marco legal · citación APA 7", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Marco legal si aplica · citación/referencias · última sincrónica antes del cierre de ACA2 (dom 04/10)."},
            {"n": 8, "fecha": "05/10/2026",
             "titulo": "Diseño metodológico: paradigma, enfoque y alcance", "bloque": "Puente",
             "unidad_esp329": "U5",
             "detalle": "ESP329 U5 · Adelantar metodología antes de festivos de ACA3."},
            {"n": 9, "fecha": "19/10/2026",
             "titulo": "Población/muestra, técnicas e instrumentos (propuestos)", "bloque": "ACA 3",
             "unidad_esp329": "U5",
             "detalle": "ESP329 U5 · Instrumentos PROPUESTOS (no aplicados en Proyecto I)."},
            {"n": 10, "fecha": "26/10/2026",
             "titulo": "Planeación, viabilidad e integración del anteproyecto", "bloque": "ACA 3",
             "unidad_esp329": "U6–U7",
             "detalle": "ESP329 U6–U7 · Cronograma, presupuesto e integración · última sincrónica antes del cierre de ACA3 (dom 08/11)."},
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
            "Numeración del Syllabus salta N° 3 y 9. Periodo corto 26P03 = 7 jueves (03/08–20/09): "
            "las unidades U8 + U10–U12 se combinan en la fecha del 17/09 (no se eliminan del Syllabus)."
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
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes (Padlet) y de las ACAs (peso, fechas, formato). No se dicta tema."},
            {"n": 2, "fecha": "20/08/2026", "titulo": "MinCiencias · 6 líneas de Ingeniería · elección de línea", "bloque": "U4",
             "detalle": "IoT, Big Data, IA, cloud/FinTech, aplicaciones, telemática."},
            {"n": 3, "fecha": "27/08/2026", "titulo": "Prueba parcial · 1.er avance del artículo", "bloque": "U5",
             "detalle": "Talleres/sustentaciones · tipos de conocimiento y fuentes."},
            {"n": 4, "fecha": "03/09/2026", "titulo": "Identificación de problemas y pregunta de investigación", "bloque": "U6",
             "detalle": "Espina de pescado, árbol de problemas, método 3D."},
            {"n": 5, "fecha": "10/09/2026", "titulo": "Formulación del planteamiento del problema", "bloque": "U7",
             "detalle": "Estado actual, evidencias, causas, posibles soluciones. Recepción máx. trabajos: 12/09."},
            {"n": 6, "fecha": "17/09/2026", "titulo": "Bases de datos CUN · gestores · marco teórico y revisión (U8+U10–12)", "bloque": "U8+U10–12",
             "detalle": "COMBINACIÓN por periodo corto: U8 + U10–U12 en un solo encuentro. Scholar + biblioteca CUN + ZoteroBib (web) + avance de revisión en Google Docs."}
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
        "nota_syllabus": None,
        "sesiones": [
            {"n": 1, "fecha": "12/08/2026", "titulo": "Presentación del curso · docente · estudiantes · ACAs", "bloque": "Encuadre",
             "presentacion": True,
             "unidad_diferida": "U1–U2 (Propuesta de Innovación · creatividad e inteligencia emocional) → lectura autónoma; se retoma al abrir la Sesión 02.",
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes (Padlet) y de las ACAs (peso, fechas, formato). No se dicta tema."},
            {"n": 2, "fecha": "19/08/2026", "titulo": "Creatividad/innovación en I+D · Design Thinking y técnicas", "bloque": "U3",
             "detalle": "Pensamiento divergente/convergente · ideación."},
            {"n": 3, "fecha": "26/08/2026", "titulo": "Gestión de la innovación (Manual de Oslo / OCDE)", "bloque": "U4",
             "detalle": "Métodos en producto, proceso, organización, marketing, social."},
            {"n": 4, "fecha": "02/09/2026", "titulo": "Tipos de innovación", "bloque": "U5",
             "detalle": "Cuadro comparativo · mejoras en contextos socio-económicos."},
            {"n": 5, "fecha": "09/09/2026", "titulo": "Análisis de negocios · validación de la propuesta", "bloque": "U6",
             "detalle": "FODA, Canvas, MVP · sustentación de propuesta."},
            {"n": 6, "fecha": "16/09/2026", "titulo": "Vigilancia tecnológica", "bloque": "U7",
             "detalle": "Datos estratégicos sobre tecnologías y tendencias."},
            {"n": 7, "fecha": "23/09/2026", "titulo": "Innovación local–internacional · entidades de apoyo", "bloque": "U8",
             "detalle": "Cierre del curso · impactos y programas de apoyo."}
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
        "fuente": "Manual del Docente (⚠️ sin Syllabus SIAC) · analogía con TG3",
        "nota_syllabus": "FALTA SYLLABUS OFICIAL. Temario orientativo — confirmar en Moodle/portal.",
        "sesiones": [
            {"n": 1, "fecha": "10/08/2026", "titulo": "Presentación del curso · docente · estudiantes · ACAs", "bloque": "Encuadre",
             "presentacion": True,
             "unidad_diferida": "Delimitación / reformulación del tema → lectura autónoma; se retoma al abrir la Sesión 02. (El acuerdo pedagógico se firma en esta sesión de encuadre.)",
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes (Padlet) y de las ACAs (peso, fechas, formato APA) + acuerdo pedagógico. No se dicta tema."},
            {"n": 2, "fecha": "24/08/2026", "titulo": "Pregunta, objetivos y título provisional", "bloque": "Orientativo",
             "detalle": "17/08 es clase autónoma (festivo)."},
            {"n": 3, "fecha": "31/08/2026", "titulo": "Estructura del documento / artículo de avance", "bloque": "Orientativo",
             "detalle": "Plantilla APA CUN."},
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
             "detalle": "Encuadre: presentación del curso, del Docente, de los estudiantes (Padlet) y de las ACAs (peso, fechas, formato APA) + acuerdo pedagógico. No se dicta tema."},
            {"n": 2, "fecha": "18/08/2026", "titulo": "Formulación de pregunta, objetivos y título", "bloque": "U3",
             "detalle": "Variables en la pregunta-problema."},
            {"n": 3, "fecha": "25/08/2026", "titulo": "Estructura del artículo · taller de introducción", "bloque": "U4",
             "detalle": "Contexto, problema, pregunta y objetivos."},
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
             "detalle": "Culminación del artículo."},
            {"n": 11, "fecha": "20/10/2026", "titulo": "Póster · evidencias · verificación antiplagio", "bloque": "U12",
             "detalle": "Alistamiento para sustentación."},
            {"n": 12, "fecha": "27/10/2026", "titulo": "Sustentación ante jurados", "bloque": "U13",
             "detalle": "Defensa oral del proyecto."},
            {"n": 13, "fecha": "03/11/2026", "titulo": "Entregables para repositorio institucional", "bloque": "U14",
             "detalle": "Cierre formal del trabajo de grado (Syllabus U1–U14 completo)."},
            {"n": 14, "fecha": "10/11/2026", "titulo": "Ajustes finales · seguimiento post-sustentación", "bloque": "Buffer",
             "detalle": "Fecha calendario extra tras U14. Grupo 54450: última martes antes del cierre 15/11 (recepción 07/11)."},
            {"n": 15, "fecha": "17/11/2026", "titulo": "Cierre administrativo · recepción (hasta 22 nov)", "bloque": "Buffer",
             "detalle": "Solo grupos 54466/54467 (26V04, cierre 22/11). El 54450 NO tiene esta fecha."}
        ],
    },
}


# ---------------------------------------------------------------------------
# Subject de Calendar (encuentros CSV/ICS) — patrón único los 5 cursos
# ---------------------------------------------------------------------------
# Formato canónico (CSV/ICS encuentros · los 5 cursos):
#   {grupos} - {Asignatura corta} - Sesion NN
#   Varios grupos: 54450/54466/54467 - Trabajo de Grado 3 - Sesion 03
# Sin nombre largo del tema (el tema va en Description).
# Festivo Pregrado (clase autónoma) — mismo patrón + sufijo:
#   {grupos} - {Asignatura} - Sesion NN (autónoma)
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

    Patrón: ``{grupos} - {Asignatura} - Sesion NN`` (sin tema largo).
    ``titulo_sesion`` se ignora en el Subject (queda en Description del evento).
    Festivo sin entrada en catálogo: ``{grupos} - {Asignatura} - Clase autonoma (…) (autónoma)``.
    Día festivo con sesión de catálogo: mismo patrón Sesion NN + `` (autónoma)``.
    """
    curso = titulo_para_calendar(course_key)
    g_lbl = groups_subject_label(groups)
    # titulo_sesion: aceptado por compatibilidad; no va en el Subject corto.
    _ = (titulo_sesion or "").strip()
    if n is not None:
        core = f"{g_lbl} - {curso} - Sesion {int(n):02d}"
    elif autonoma:
        fest = f" ({festivo_nombre})" if festivo_nombre else ""
        core = f"{g_lbl} - {curso} - Clase autonoma{fest}"
    else:
        core = f"{g_lbl} - {curso} - Encuentro"
    if autonoma and not core.rstrip().endswith("(autónoma)"):
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
