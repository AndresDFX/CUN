# -*- coding: utf-8 -*-
"""Presentaciones + calendarios de las 4 asignaturas de Pregrado (CUN).

Reglas:
- Presentación del Curso en <Asignatura>/Clases/: grupo(s) solo en portada;
  tutor_slide genérico («Docente» + perfil + correo); CONTENIDO en UNA slide
  (Sesión N — tema; helper contenido_sesiones_slide); recursos/cierre sin grupo ni nombre propio.
- Si el día de clase cae en festivo colombiano → la sesión queda como CLASE AUTÓNOMA
  (sigue en el calendario, marcada; no se cancela).
- Eventos de Calendar (encuentros): Subject corto =
  `{grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo; sin tema largo).
  Fuente de fechas/temas (Description): `sesiones_cun.py`.
- Horarios confirmados por el docente:
    TG2  → lunes 5:00–6:00 pm
    TG3  → martes 5:00–6:00 pm
    Creatividad → miércoles 5:00–6:00 pm
    Investigación → jueves 5:00–6:00 pm
"""
from __future__ import annotations

import csv
import os
import sys
from datetime import date, timedelta
import datetime as _dt
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))
from cun_slides_engine import *  # noqa: F401,F403
from sesiones_cun import (  # noqa: E402
    COURSES as SESIONES_COURSES,
    subject_encuentro,
    tema_por_fecha as _tema_por_fecha_catalogo,
)
from carga_academica import (  # noqa: E402
    bold_var,
    cover_meta_lines,
    docente as _docente_pair,
    footer_inicio_efectivo,
    pregrado_build_dict,
)
from fechas_entrega_aca import blocks_para_slide, blocks_tg3_slide  # noqa: E402

# Ruta derivada del propio archivo (config/slides/ → ../../Pregrado). Antes estaba
# hardcodeada como «G:\Mi unidad\…», que rompe cuando Google Drive monta la unidad
# en inglés («G:\My Drive») — corregido 2026-08-09.
ROOT = Path(__file__).resolve().parents[2] / "Pregrado"
D = date
DOCENTE, DOCENTE_CORREO = _docente_pair()
from sesiones_cun import DOCENTE_CREDS  # noqa: E402  (fuente única del perfil proyectado)
URL_PLANTILLA_APA = "[URL Drive/Moodle de la Plantilla APA CUN — pendiente]"
URL_CDIGITAL = "[URL CDigital — campus del curso pendiente]"
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


def tema_por_fecha(course_key: str) -> dict[str, dict]:
    """Mapa dd/mm/YYYY → sesión de sesiones_cun (si existe)."""
    return _tema_por_fecha_catalogo(course_key)


def _meet_ph(titulo_corto: str) -> str:
    return f"[URL Meet — mismo enlace toda la serie · {titulo_corto}]"


def add_eval_scope_pregrado(prs, idx: int, regimen: str) -> int:
    """Bloque claro: evaluación por cortes Art. 52; auto/coeval con % propio no aplica.

    Distingue de la autoevaluación institucional SIAC (calidad de programas).
    """
    content_slide(
        prs,
        "ALCANCE DE LA EVALUACIÓN",
        [
            regimen,
            "Autoevaluación y coevaluación **con porcentaje propio** (modelo AFI Proyecto I: "
            "4% + 4% según ESP329): **no aplican** en esta asignatura según el syllabus SIAC / Art. 52.",
            "No confundir con la autoevaluación **institucional** SIAC (calidad de programas en "
            "acreditacion.cun.edu.co): esa no es una nota del curso.",
            "Entregas, rúbricas EV y publicación de notas: solo por **CDigital**.",
            "Si Coordinación publica un instrumento formativo sin peso propio, se anuncia en el aula; "
            "no inventamos % fuera del syllabus.",
        ],
        idx=idx,
        size=13,
    )
    return idx + 1


def recursos_items(titulo_corto: str, *extra: str) -> list[str]:
    """Bullets de la slide RECURSOS (links concretos + placeholders claros).

    Placeholders de oferta (CDigital / Meet) en negrita. Sin nombre propio del docente.
    """
    items = [
        f"**Contacto del Docente:** {DOCENTE_CORREO}",
        f"**CDigital (campus del curso):** {bold_var(URL_CDIGITAL)}",
        f"**Google Meet (mismo enlace toda la serie):** {bold_var(_meet_ph(titulo_corto))}",
        "**Plantilla APA CUN – Proyecto de Grado** (archivo local): "
        "`Cursos/Plantilla_APA_CUN_Proyecto de grado.docx`.",
        f"**URL pública Plantilla APA:** {URL_PLANTILLA_APA}",
        "**Enunciados ACA / cortes (estudiantes):** `Clases/Recursos/ACAs/`.",
    ]
    items.extend(extra)
    return items


def add_tutor(prs, idx: int = 2):
    tutor_slide(prs, "Docente", DOCENTE_CREDS, DOCENTE_CORREO, idx=idx)


def add_icebreaker(prs, idx: int = 3, consignas=None):
    """Rompehielos con QR (Presentación del Curso · los 5 cursos)."""
    icebreaker_qr_slide(prs, idx=idx, consignas=consignas)

# Festivos Colombia 2026 relevantes al periodo ago–nov (incl. trasladados a lunes)
FESTIVOS_2026 = {
    D(2026, 8, 7): "Batalla de Boyacá",
    D(2026, 8, 17): "Asunción de la Virgen",
    D(2026, 10, 12): "Día de la Raza",
    D(2026, 11, 2): "Todos los Santos",
    D(2026, 11, 16): "Independencia de Cartagena",
}


def weekday_dates(start: date, end: date, weekday: int) -> list[date]:
    """weekday: 0=lun … 6=dom. Incluye start/end si coinciden."""
    d = start
    while d.weekday() != weekday:
        d += timedelta(days=1)
        if d > end:
            return []
    out = []
    while d <= end:
        out.append(d)
        d += timedelta(days=7)
    return out


def is_festivo(d: date) -> bool:
    return d in FESTIVOS_2026


def groups_label(groups: list[str], for_filename: bool = False) -> str:
    if for_filename:
        if len(groups) == 1:
            return f"Grupo {groups[0]}"
        return "Grupos " + "+".join(groups)
    if len(groups) == 1:
        return f"Grupo {groups[0]}"
    return "Grupos " + " / ".join(groups)


# ---------------------------------------------------------------------------
# Definición de cursos (fuente editable: config/cursos/carga_academica_2026.json)
# ---------------------------------------------------------------------------
COURSES = {
    key: pregrado_build_dict(key)
    for key in ("investigacion", "creatividad", "tg2", "tg3")
}


def ensure_dirs(course_dir: Path):
    (course_dir / "Clases").mkdir(parents=True, exist_ok=True)
    (course_dir / "Guiones" / "Capturas").mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Presentaciones
# ---------------------------------------------------------------------------
def build_investigacion(out: Path):
    set_footer(footer_inicio_efectivo("investigacion"))
    prs = new_prs()
    course_cover(
        prs, "INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA",
        "Escuela de Ingenierías · Código EI005 · 2 créditos",
        cover_meta_lines(
            "investigacion",
            extra=["**Regla de festivo:** si el jueves es festivo → **clase autónoma**."],
        ),
    )
    add_tutor(prs, idx=2)
    add_icebreaker(prs, idx=3, consignas=[
        f"**Escanea o abre:** {PADLET_PRESENTACION_URL}",
        "Post-it: **nombre** + **expectativa del curso** + **idea de tema** para el artículo (1 frase).",
        "Tablero oficial: **Padlet** (mismo enlace en los 5 cursos).",
        "Ahora (~7 min). Leemos juntos 3–4 notas (sin juzgar).",
    ])
    content_slide(prs, "¿QUÉ ES ESTA ASIGNATURA?", [
        "Aplicar el **método científico** a una temática de tu entorno (empresarial o vivencial).",
        "Se enmarca en las **6 líneas estratégicas de Ingeniería** (IoT, Big Data, IA, servicios/cloud-FinTech, aplicaciones, telemática).",
        "Producto esperado: avance hacia un **artículo / proyecto de investigación** (ABP).",
        "32 h con docente + 64 h de trabajo autónomo y colaborativo.",
    ], idx=4)
    content_slide(prs, "COMPETENCIAS (SYLLABUS)", [
        "**Saber:** desarrollar el tema acorde a líneas del programa e identificar el diseño de investigación.",
        "**Hacer:** usar fuentes confiables con redacción científica; organizar el desarrollo teórico-metodológico.",
        "**Ser:** respetar derechos de autor en la escritura del proceso.",
    ], idx=5)
    _n_cont = contenido_sesiones_slide(
        prs, SESIONES_COURSES["investigacion"]["sesiones"], idx=6,
    )
    _i = 6 + _n_cont
    blocks = blocks_para_slide("investigacion")
    _inv_h = COURSES["investigacion"]["horario_corto"]
    fechas_inicio_fin_slide(
        prs, "EVALUACIÓN — CORTES (ART. 52)",
        blocks,
        note="Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%. Enunciados: Clases/Recursos/ACAs/. Fechas = día de clase (jue). Confirma desglose EV en CDigital.",
        sub=f"Periodo {bold_var('26P03')} · inicio {bold_var('10/08/2026')} · cierre {bold_var('20/09/2026')}",
        idx=_i,
    )
    _i += 1
    _i = add_eval_scope_pregrado(
        prs, _i,
        "**Régimen:** Art. 52 del Reglamento Estudiantil · **Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%** "
        "(desglose EV: confirmar en CDigital / syllabus SIAC EI005).",
    )
    box_note_slide(prs, "ACUERDOS DEL CURSO", [
        ("info", f"Encuentro sincrónico: {bold_var(_inv_h)} por Google Meet. El enlace se publica en el aula virtual."),
        ("aclaracion", "Si el día de clase es festivo colombiano, la sesión NO se cancela: se cursa como **clase autónoma** (material/actividad en el CDigital)."),
        ("advertencia", "El producto final se construye desde la semana 1 — no es una entrega sorpresa al cierre."),
    ], idx=_i)
    _i += 1
    content_slide(prs, "RECURSOS", recursos_items(
        "Investigación C&T",
        "**Bases de datos:** biblioteca CUN (EBSCO, SciELO, Redalyc, Latindex) + citas en la nube (ZoteroBib / Google Docs).",
        "**Entregas y notas oficiales:** solo por CDigital del curso.",
    ), idx=_i)
    closing_slide(prs, "¡Empezamos!", [
        f"Nos vemos en el primer encuentro sincrónico: {bold_var(_inv_h)}.",
        "Trae una idea de tema ligado a tu entorno o a una línea de Ingeniería.",
    ], "EI005 · Investigación, Ciencia y Tecnología")
    prs.save(str(out))
    print("OK PPTX", out, "slides", len(prs.slides))


def build_creatividad(out: Path):
    set_footer(footer_inicio_efectivo("creatividad"))
    prs = new_prs()
    course_cover(
        prs, "CREATIVIDAD Y PENSAMIENTO INNOVADOR",
        "Escuela de Ingenierías · Código EI004 · 2 créditos",
        cover_meta_lines(
            "creatividad",
            extra=[
                "**Área oferente:** Unidad de Emprendimiento e Innovación (C-EMP)",
                "**Regla de festivo:** si el miércoles es festivo → **clase autónoma**.",
            ],
        ),
    )
    add_tutor(prs, idx=2)
    add_icebreaker(prs, idx=3, consignas=[
        f"**Escanea o abre:** {PADLET_PRESENTACION_URL}",
        "Post-it: **nombre** + **expectativa del curso** + **tema/problema** de interés (1 frase).",
        "Tablero oficial: **Padlet** (mismo enlace en los 5 cursos).",
        "Ahora (~7 min). Leemos juntos 3–4 notas (sin juzgar).",
    ])
    content_slide(prs, "¿QUÉ ES ESTA ASIGNATURA?", [
        "Identificar tus habilidades de **creatividad e innovación** y aplicarlas a mejorar una realidad observada (producto, proceso u organización).",
        "Hilo conductor: una **Propuesta de Innovación** anunciada desde la semana 1.",
        "32 h con docente + 64 h de trabajo autónomo y colaborativo.",
    ], idx=4)
    _n_cont = contenido_sesiones_slide(
        prs, SESIONES_COURSES["creatividad"]["sesiones"], idx=5,
    )
    _i = 5 + _n_cont
    blocks = blocks_para_slide("creatividad")
    _cre_h = COURSES["creatividad"]["horario_corto"]
    fechas_inicio_fin_slide(
        prs, "EVALUACIÓN — CORTES (ART. 52)",
        blocks,
        note="Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%. Enunciados: Clases/Recursos/ACAs/. Fechas = día de clase (mié).",
        sub=f"Periodo {bold_var('26V04')} · inicio {bold_var('10/08/2026')} · cierre {bold_var('27/09/2026')}",
        idx=_i,
    )
    _i += 1
    _i = add_eval_scope_pregrado(
        prs, _i,
        "**Régimen:** Art. 52 del Reglamento Estudiantil · **Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%** "
        "(desglose EV: confirmar en CDigital / syllabus SIAC EI004).",
    )
    box_note_slide(prs, "ACUERDOS DEL CURSO", [
        ("info", f"Encuentro sincrónico: {bold_var(_cre_h)} por Google Meet."),
        ("aclaracion", "Festivo en día de clase = **clase autónoma** (actividad en el CDigital), no cancelación."),
        ("advertencia", "La Propuesta de Innovación se explica desde el día 1 y se valida/sustenta hacia la unidad 6."),
    ], idx=_i)
    _i += 1
    content_slide(prs, "RECURSOS", recursos_items(
        "Creatividad",
        "**Herramientas típicas:** Design Thinking, Canvas, Journey Map, MVP, vigilancia tecnológica.",
        "**Entregas y notas oficiales:** solo por CDigital del curso.",
    ), idx=_i)
    closing_slide(prs, "¡Empezamos!", [
        f"Nos vemos en el primer encuentro sincrónico: {bold_var(_cre_h)}.",
        "Piensa desde ya en un problema real que quieras mejorar con innovación.",
    ], "EI004 · Creatividad y Pensamiento Innovador")
    prs.save(str(out))
    print("OK PPTX", out, "slides", len(prs.slides))


def build_tg2(out: Path):
    set_footer(footer_inicio_efectivo("tg2"))
    prs = new_prs()
    course_cover(
        prs, "TRABAJO DE GRADO 2",
        "Modelos de Innovación — Ingeniería de Sistemas · Código 94453 · 2 créditos",
        cover_meta_lines(
            "tg2",
            extra=[
                "**Regla de festivo:** si el lunes es festivo → **clase autónoma**.",
                "⚠️ Syllabus SIAC pendiente — contenido orientativo.",
            ],
        ),
    )
    add_tutor(prs, idx=2)
    add_icebreaker(prs, idx=3, consignas=[
        f"**Escanea o abre:** {PADLET_PRESENTACION_URL}",
        "Post-it: **nombre** + **estado actual** del proyecto (1 frase) + expectativa de TG2.",
        "Tablero oficial: **Padlet** (mismo enlace en los 5 cursos).",
        "Ahora (~7 min). Leemos juntos 3–4 notas (sin juzgar).",
    ])
    content_slide(prs, "¿QUÉ ES TRABAJO DE GRADO 2?", [
        "Espacio de **opción de grado** (pregrado): avance consolidado del proyecto/artículo antes de la culminación en Trabajo de Grado 3.",
        "No se rige por el instructivo AFI de Especializaciones (Proyecto I/II).",
        "Enfoque: formulación y desarrollo metodológico del trabajo, con acompañamiento semanal de 1 hora.",
        "Formato de referencia: **Plantilla APA CUN – Proyecto de Grado**.",
    ], idx=4)
    content_slide(prs, "ENFOQUE DEL PERIODO (A CONFIRMAR CON EL SYLLABUS)", [
        "Retomar / delimitar el proyecto proveniente de semestres anteriores.",
        "Consolidar planteamiento, pregunta, objetivos y marco referencial.",
        "Avanzar el diseño metodológico (aún con énfasis en lo propuesto / documentado).",
        "Dejar el documento listo para la fase de culminación y sustentación en Trabajo de Grado 3.",
    ], idx=5)
    _n_cont = contenido_sesiones_slide(
        prs, SESIONES_COURSES["tg2"]["sesiones"], idx=6,
    )
    _i = 6 + _n_cont
    blocks = blocks_para_slide("tg2")
    _tg2_h = COURSES["tg2"]["horario_corto"]
    fechas_inicio_fin_slide(
        prs, "EVALUACIÓN (ART. 52) — ORIENTATIVA",
        blocks,
        note=(
            "*Pesos típicos Art. 52 (30/30/40). CONFIRMAR en Syllabus/CDigital. "
            "Enunciados: Clases/Recursos/ACAs/. Fechas = día de clase (lun). "
            f"Recepción máx.: {bold_var('14/11/2026')}."
        ),
        sub=f"Inicio {bold_var('10/08/2026')} · cierre {bold_var('22/11/2026')}",
        idx=_i,
    )
    _i += 1
    _i = add_eval_scope_pregrado(
        prs, _i,
        "**Régimen:** Art. 52 · pesos orientativos **30% / 30% / 40%** hasta cargar Syllabus SIAC de TG2 "
        "(confirmar en CDigital).",
    )
    box_note_slide(prs, "ACUERDOS DEL CURSO", [
        ("info", f"Encuentro sincrónico: {bold_var(_tg2_h)} por Google Meet. El Meet es el mismo enlace para toda la serie."),
        ("aclaracion", "Lunes festivo = **clase autónoma** (guía/actividad en el CDigital), no se pierde el hilo del proyecto."),
        ("advertencia", "Hasta cargar el Syllabus SIAC, cualquier detalle de rubrica/pesos se verifica en el aula virtual."),
    ], idx=_i)
    _i += 1
    content_slide(prs, "RECURSOS", recursos_items(
        "Trabajo de Grado 2",
        "**Siguiente eslabón:** Trabajo de Grado 3 (sustentación ante jurados + repositorio).",
        "**Entregas y notas oficiales:** solo por CDigital del curso.",
    ), idx=_i)
    closing_slide(prs, "¡Empezamos!", [
        f"Nos vemos en el primer encuentro sincrónico: {bold_var(_tg2_h)}.",
        "Llega con el estado actual de tu proyecto (aunque esté incompleto).",
    ], "94453 · Trabajo de Grado 2")
    prs.save(str(out))
    print("OK PPTX", out, "slides", len(prs.slides))


def build_tg3(out: Path):
    set_footer(footer_inicio_efectivo("tg3"))
    prs = new_prs()
    course_cover(
        prs, "TRABAJO DE GRADO 3",
        "Modelos de Innovación — Ingeniería de Sistemas · Código 94532 · 2 créditos",
        cover_meta_lines(
            "tg3",
            extra=["**Regla de festivo:** si el martes es festivo → **clase autónoma**."],
        ),
    )
    add_tutor(prs, idx=2)
    add_icebreaker(prs, idx=3, consignas=[
        f"**Escanea o abre:** {PADLET_PRESENTACION_URL}",
        "Post-it: **nombre** + **tema del artículo** (1 frase) + expectativa del semestre.",
        "Tablero oficial: **Padlet** (mismo enlace en los 5 cursos).",
        "Ahora (~7 min). Leemos juntos 3–4 notas (sin juzgar).",
    ])
    content_slide(prs, "¿QUÉ ES TRABAJO DE GRADO 3?", [
        "Culminación de la **opción de grado**: artículo resultado de investigación (o obra-creación) + sustentación.",
        "Prerrequisito: Opción de grado II.",
        "Artículo con revisión rigurosa (≥ 50 referencias; extensión no inferior a 4.000 palabras, según Syllabus).",
        "32 h con docente + 64 h de trabajo autónomo.",
    ], idx=4)
    _n_cont = contenido_sesiones_slide(
        prs, SESIONES_COURSES["tg3"]["sesiones"], idx=5,
    )
    _i = 5 + _n_cont
    blocks = blocks_tg3_slide()
    _tg3_h = COURSES["tg3"]["horario_corto"]
    fechas_inicio_fin_slide(
        prs, "EVALUACIÓN — CORTE ÚNICO 100%",
        blocks,
        note=(
            "EV05 50% + EXAM 50%. Enunciados: Clases/Recursos/ACAs/. "
            f"Cierre grupos 54466/54467: {bold_var('22/11/2026')}; "
            f"grupo 54450: {bold_var('15/11/2026')} (EXAM anticipado)."
        ),
        sub=f"Art. 52 · inicio {bold_var('10/08/2026')} · día de clase mar",
        idx=_i,
    )
    _i += 1
    _i = add_eval_scope_pregrado(
        prs, _i,
        "**Régimen:** Art. 52 · **corte único 100%** = EV05 (proceso) **50%** + EXAM (sustentación) **50%** "
        "(syllabus SIAC TG3).",
    )
    box_note_slide(prs, "ACUERDOS DEL CURSO", [
        (
            "info",
            f"Encuentro: {bold_var(_tg3_h)}. El Meet es el mismo enlace para toda la serie.",
        ),
        ("aclaracion", "Martes festivo = **clase autónoma** (avance guiado en el CDigital)."),
        ("advertencia", "Antes de la sustentación: verificación antiplagio (unidad 12) y póster listo."),
    ], idx=_i)
    _i += 1
    content_slide(prs, "RECURSOS", recursos_items(
        "Trabajo de Grado 3",
        "**Repositorio:** carga institucional del trabajo de grado al finalizar la sustentación.",
        "**Entregas y notas oficiales:** solo por CDigital del curso.",
    ), idx=_i)
    closing_slide(prs, "¡Empezamos!", [
        f"Nos vemos en el primer encuentro sincrónico: {bold_var(_tg3_h)}.",
        "Objetivo del periodo: artículo listo + sustentación ante jurados.",
    ], "94532 · Trabajo de Grado 3")
    prs.save(str(out))
    print("OK PPTX", out, "slides", len(prs.slides))


# ---------------------------------------------------------------------------
# Calendarios
# ---------------------------------------------------------------------------
def ics_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def write_calendar_files(course_key: str, course: dict, groups_for_event: list[str], out_dir: Path, end: date):
    """Genera CSV + ICS + markdown para un conjunto de grupos que comparten horario.
    Pregrado: sin Guests/ATTENDEE. Festivo = clase autónoma (sigue en calendar).
    Subject: `{grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    sessions = weekday_dates(course["inicio"], end, course["weekday"])
    temas = tema_por_fecha(course_key)
    g_lbl = groups_label(groups_for_event)
    g_file = groups_label(groups_for_event, for_filename=True)
    meet = _meet_ph(course["titulo_corto"])

    rows = []
    ics_events = []
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    h0, h1 = course["hora_ics"]

    cal_md_rows = []
    for i, d in enumerate(sessions, 1):
        auto = is_festivo(d)
        fest_name = FESTIVOS_2026.get(d, "")
        fecha_txt = d.strftime("%d/%m/%Y")
        ses = temas.get(fecha_txt)

        # n/tema = catálogo sesiones_cun (alineado a carpetas Sesion NN).
        # Festivo sin entrada en catálogo → Clase autónoma (…) (autónoma).
        if ses:
            n_ses = int(ses["n"])
            titulo_ses = ses["titulo"]
            tema_txt = f"Sesión {n_ses:02d} — {titulo_ses}"
            subject = subject_encuentro(
                course_key, groups_for_event,
                n=n_ses, titulo_sesion=titulo_ses,
                autonoma=auto, festivo_nombre=fest_name or None,
            )
        elif auto:
            tema_txt = f"Clase autónoma — continuar avance (festivo: {fest_name})"
            subject = subject_encuentro(
                course_key, groups_for_event,
                autonoma=True, festivo_nombre=fest_name,
            )
        else:
            tema_txt = "Encuentro sincrónico (ver Manual / Syllabus)"
            subject = subject_encuentro(course_key, groups_for_event)

        # Description corta (2–4 líneas). Location vacío sin Meet real.
        if auto:
            if ses:
                desc = (
                    f"Sesión {int(ses['n']):02d} — {ses['titulo']} (autónoma)\n"
                    f"Festivo: {fest_name}. Actividad en CDigital."
                )
            else:
                desc = (
                    f"Clase autónoma — {fest_name}\n"
                    "Actividad en CDigital."
                )
            location = ""
            tipo = f"Autónoma ({fest_name})"
        else:
            if ses:
                desc = f"Sesión {int(ses['n']):02d} — {ses['titulo']}"
            else:
                desc = tema_txt
            location = ""
            tipo = "Sincrónica"

        rows.append({
            "Subject": subject,
            "Start Date": d.strftime("%m/%d/%Y"),
            "Start Time": course["hora_ini"],
            "End Date": d.strftime("%m/%d/%Y"),
            "End Time": course["hora_fin"],
            "All Day Event": "False",
            "Description": desc.replace("\n", " | "),
            "Location": location,
            "Private": "False",
        })
        cal_md_rows.append((i, d, tipo, tema_txt, subject))

        uid = f"cun-pregrado-{course_key}-{'-'.join(groups_for_event)}-{d.isoformat()}@cun.edu.co"
        ics_events += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{stamp}",
            f"DTSTART;TZID=America/Bogota:{d.strftime('%Y%m%d')}T{h0}",
            f"DTEND;TZID=America/Bogota:{d.strftime('%Y%m%d')}T{h1}",
            f"SUMMARY:{ics_escape(subject)}",
            f"DESCRIPTION:{ics_escape(desc)}",
        ]
        if location:
            ics_events.append(f"LOCATION:{ics_escape(location)}")
        ics_events += [
            "STATUS:CONFIRMED",
            "END:VEVENT",
        ]

    stem = f"Encuentros {course['titulo_corto']} - {g_file}"
    csv_path = out_dir / f"{stem} - Importar a Calendar.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
            "Subject", "Start Date", "Start Time", "End Date", "End Time",
            "All Day Event", "Description", "Location", "Private",
        ])
        w.writeheader()
        w.writerows(rows)

    ics_path = out_dir / f"{stem} - Importar a Calendar.ics"
    ics_path.write_text(
        "\r\n".join([
            "BEGIN:VCALENDAR", "VERSION:2.0",
            "PRODID:-//CUN//Pregrado Encuentros//ES",
            "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
            *ics_events, "END:VCALENDAR",
        ]) + "\r\n",
        encoding="utf-8",
    )

    # Calendario markdown
    lines = [
        f"# Calendario — {course['titulo_largo']}",
        f"**{g_lbl}** · Horario: **{course['horario_txt']}**",
        "",
        "> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` "
        "(fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo.",
        "> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela).",
        "> CSV/ICS **sin invitados** estudiantes. Description corta; Location vacío hasta Meet real.",
        "",
        "| # | Fecha | Tipo | Subject (Calendar) |",
        "|---|---|---|---|",
    ]
    for i, d, tipo, tema_txt, subject in cal_md_rows:
        lines.append(
            f"| {i} | {d.strftime('%d/%m/%Y')} ({DIAS[d.weekday()]}) | {tipo} | {subject} |"
        )
    # Fechas institucionales del/los grupos de este archivo
    meta_bits = []
    for g in groups_for_event:
        m = course["group_meta"].get(g, {})
        if m:
            meta_bits.append(
                f"- **{g}** ({m.get('periodo', '—')}): inicio {m['inicio'].strftime('%d/%m/%Y')} · "
                f"recepción {m['recepcion'].strftime('%d/%m/%Y')} · cierre **{m['cierre'].strftime('%d/%m/%Y')}**"
            )
    lines += [
        "",
        "## Fechas institucionales",
        *meta_bits,
        f"- Cierre considerado en este archivo Calendar: **{end.strftime('%d/%m/%Y')}**",
        f"- Eventos generados: **{len(sessions)}**",
        f"- Archivos: `{csv_path.name}` / `{ics_path.name}`",
        "",
        "## Cómo importar (sin invitados · description corta)",
        "1. Google Calendar → Configuración → Importar → `.ics` o `.csv`.",
        "2. **No incluye estudiantes** (Pregrado no lleva Guests/ATTENDEE).",
        "3. Location vacío: tras importar, añade Meet (mismo enlace en toda la serie) y publícalo en CDigital.",
        "4. Subject corto: grupos - asignatura - Sesion NN. Description = una línea con el tema.",
        f"5. Placeholder Meet de referencia (no va en el ICS): {meet}.",
        "",
        f"Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`",
    ]
    (out_dir / f"Calendario de clases - {g_file}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Limpia duplicado antiguo con raya tipográfica
    legacy = out_dir / f"Calendario de clases — {g_file}.md"
    if legacy.exists() and legacy.resolve() != (out_dir / f"Calendario de clases - {g_file}.md").resolve():
        try:
            legacy.unlink()
        except OSError:
            pass
    print(f"OK CAL {course_key} {g_lbl}: {len(sessions)} sesiones -> {out_dir}")


def write_calendario_curso(course_key: str, course: dict, course_dir: Path):
    """Calendario oficial en raíz del curso, con mapeo tema↔fecha del Syllabus."""
    end = max(m["cierre"] for m in course["group_meta"].values())
    sessions = weekday_dates(course["inicio"], end, course["weekday"])
    temas = tema_por_fecha(course_key)
    syllabus = SESIONES_COURSES.get(course_key, {})
    n_temas = len(syllabus.get("sesiones") or [])
    lines = [
        f"# Calendario de clases (oficial) — {course['titulo_largo']}",
        f"Plantilla del curso · Horario: **{course['horario_txt']}**",
        f"Grupos de este periodo: **{', '.join(course['groups'])}**",
        f"Docente: **{DOCENTE}** · {DOCENTE_CORREO}",
        "",
        "> Si el día de clase es **festivo colombiano**, la sesión se considera **clase autónoma** (actividad en CDigital).",
        "> Los CSV/ICS de Pregrado **no** incluyen invitados/estudiantes.",
        "> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo). Fuente: `sesiones_cun.py`.",
        "",
    ]
    # Nota de cierres distintos (TG3)
    cierres = {(g, m["cierre"].strftime("%d/%m/%Y"), m["periodo"]) for g, m in course["group_meta"].items()}
    if len({c[1] for c in cierres}) > 1:
        lines.append("## Cierres por grupo (fuente oficial)")
        for g, m in course["group_meta"].items():
            lines.append(
                f"- **{g}** ({m['periodo']}): inicio {m['inicio'].strftime('%d/%m/%Y')} · "
                f"recepción {m['recepcion'].strftime('%d/%m/%Y')} · cierre **{m['cierre'].strftime('%d/%m/%Y')}**"
            )
        lines.append("")
        lines.append(
            f"> Esta plantilla lista fechas hasta el cierre más largo (**{end.strftime('%d/%m/%Y')}**). "
            "Cada carpeta `2026/<grupo>/` recorta al cierre de ese grupo."
        )
        lines.append("")

    if syllabus.get("nota_syllabus"):
        lines += [f"> **Nota Syllabus:** {syllabus['nota_syllabus']}", ""]

    lines += [
        f"**Eventos en plantilla (hasta {end.strftime('%d/%m/%Y')}):** {len(sessions)} · "
        f"**Entradas en catálogo de temas:** {n_temas}",
        "",
        "| # | Fecha | Tipo | Tema (Syllabus / plan) |",
        "|---|---|---|---|",
    ]
    for i, d in enumerate(sessions, 1):
        fecha_txt = d.strftime("%d/%m/%Y")
        ses = temas.get(fecha_txt)
        if is_festivo(d):
            tipo = f"Autónoma ({FESTIVOS_2026[d]})"
            tema_txt = (
                f"{ses.get('bloque', '')}: {ses['titulo']}".strip(": ")
                if ses else f"Clase autónoma — continuar avance (festivo: {FESTIVOS_2026[d]})"
            )
        else:
            tipo = "Sincrónica"
            tema_txt = (
                f"{ses.get('bloque', '')}: {ses['titulo']}".strip(": ")
                if ses else "Encuentro sincrónico (ver Manual / Syllabus)"
            )
        lines.append(f"| {i} | {fecha_txt} ({DIAS[d.weekday()]}) | {tipo} | {tema_txt} |")

    if syllabus.get("unidades_syllabus"):
        lines += ["", "## Unidades del Syllabus (completas — no se eliminan)", ""]
        for u in syllabus["unidades_syllabus"]:
            lines.append(f"- {u}")

    lines += [
        "",
        "Los CSV/ICS con el/los códigos de grupo en el título del evento viven en `2026/<grupo>/` "
        "(y, si varios grupos comparten horario y cierre, también puede generarse un archivo combinado).",
    ]
    (course_dir / "Calendario de clases (oficial).md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_informacion(course: dict):
    for g, meta in course["group_meta"].items():
        path = ROOT / course["folder"] / "2026" / g / "Informacion.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        bloque = meta.get("bloque") or course.get("bloque_portada") or "—"
        id_grupo = meta.get("id_grupo")
        id_ln = f"Id_grupo (portal): {id_grupo}\n" if id_grupo else ""
        cap = meta.get("capacidad")
        insc = meta.get("inscritos")
        cupo_ln = ""
        if cap is not None or insc is not None:
            cupo_ln = f"Cupo / inscritos: {cap if cap is not None else '—'} / {insc if insc is not None else '—'}\n"
        dep = course.get("dependencia") or ""
        dep_ln = f"Dependencia: {dep}\n" if dep else ""
        jornada = course.get("jornada") or ""
        jornada_ln = f"Jornada: {jornada}\n" if jornada else ""
        unidad = course.get("unidad") or {}
        unidad_ln = ""
        if unidad:
            unidad_ln = f"Unidad: {unidad.get('cod', '')} — {unidad.get('nom', '')}\n"
        text = (
            "Asignaciones de pregrado\n\n"
            f"Periodo: {meta['periodo']}\n"
            f"Grupo: {g}\n"
            f"{id_ln}"
            f"Asignatura: {course['titulo_largo']}\n"
            f"Código: {course.get('codigo_corto') or course['codigo']}\n"
            f"{unidad_ln}"
            "Modalidad: VIRTUAL\n"
            f"Bloque: {bloque}\n"
            f"{jornada_ln}"
            f"{dep_ln}"
            f"Horario definido: {course['horario_txt']}\n"
            f"Sede: {course.get('sede_entrega', 'Virtual')}\n"
            f"Aula: {course.get('aula', 'Aula virtual - Google Meet')}\n"
            f"Fecha de inicio: {meta['inicio'].strftime('%d/%m/%Y')}\n"
            f"Fecha máxima para recepción de trabajos: {meta['recepcion'].strftime('%d/%m/%Y')}\n"
            f"Fecha de cierre: {meta['cierre'].strftime('%d/%m/%Y')}\n"
            f"Créditos / horas: {course['creditos']}\n"
            f"{cupo_ln}"
            "\n"
            "Regla: si la fecha de clase cae en festivo colombiano, la sesión se cursa como clase autónoma.\n"
            "Fuente de grupos/bloque: config/cursos/carga_academica_2026.json\n"
            "Ver calendario e importación a Calendar en esta carpeta.\n"
        )
        path.write_text(text, encoding="utf-8")


def write_all_calendars():
    """CSV/ICS de encuentros + calendarios oficiales md (sin PPTX)."""
    for key, course in COURSES.items():
        course_dir = ROOT / course["folder"]
        ensure_dirs(course_dir)
        write_calendario_curso(key, course, course_dir)

        for g, meta in course["group_meta"].items():
            write_calendar_files(key, course, [g], course_dir / "2026" / g, meta["cierre"])

        if key == "tg3":
            write_calendar_files(
                key, course, ["54466", "54467"],
                course_dir / "2026" / "_combinado_54466-54467",
                D(2026, 11, 22),
            )
            write_calendar_files(
                key, course, ["54450", "54466", "54467"],
                course_dir / "2026" / "_combinado_todos_hasta_15-11",
                D(2026, 11, 15),
            )


def main(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(description="Presentaciones + calendarios Pregrado CUN")
    parser.add_argument(
        "--calendar-only",
        action="store_true",
        help="Solo regenera CSV/ICS de encuentros y calendarios md (no PPTX ni Informacion.txt)",
    )
    args = parser.parse_args(argv)

    if args.calendar_only:
        write_all_calendars()
        print("DONE (calendar-only)")
        return

    builders = {
        "investigacion": build_investigacion,
        "creatividad": build_creatividad,
        "tg2": build_tg2,
        "tg3": build_tg3,
    }

    for key, course in COURSES.items():
        course_dir = ROOT / course["folder"]
        ensure_dirs(course_dir)
        safe_names = {
            "investigacion": "Presentacion del Curso - Investigacion Ciencia y Tecnologia.pptx",
            "creatividad": "Presentacion del Curso - Creatividad y Pensamiento Innovador.pptx",
            "tg2": "Presentacion del Curso - Trabajo de Grado 2.pptx",
            "tg3": "Presentacion del Curso - Trabajo de Grado 3.pptx",
        }
        pptx = course_dir / "Clases" / safe_names[key]
        builders[key](pptx)
        update_informacion(course)

    write_all_calendars()
    print("DONE")


if __name__ == "__main__":
    main()
