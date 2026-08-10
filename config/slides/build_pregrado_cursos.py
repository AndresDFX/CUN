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
    meet_url as _meet_url,
    subject_encuentro,
    tema_por_fecha as _tema_por_fecha_catalogo,
)
from carga_academica import (  # noqa: E402
    bold_var,
    cover_meta_lines,
    docente as _docente_pair,
    pregrado_build_dict,
)
from fechas_entrega_aca import (  # noqa: E402
    VENTANAS_POR_GRUPO, blocks_para_slide, blocks_tg3_slide, componentes_curso,
    desglose_corte_texto, entrega_por_id, entregas_para_grupo, fmt_entrega,
    fmt_peso, peso_corte,
)

# Ruta derivada del propio archivo (config/slides/ → ../../Pregrado). Antes estaba
# hardcodeada como «G:\Mi unidad\…», que rompe cuando Google Drive monta la unidad
# en inglés («G:\My Drive») — corregido 2026-08-09.
ROOT = Path(__file__).resolve().parents[2] / "Pregrado"
D = date
DOCENTE, DOCENTE_CORREO = _docente_pair()
from sesiones_cun import DOCENTE_CREDS  # noqa: E402  (fuente única del perfil proyectado)
from sesiones_cun import cdigital_url, CDIGITAL_PLACEHOLDER  # noqa: E402
# La plantilla NO se enlaza por URL pública: viaja DENTRO de la carpeta que recibe el
# estudiante. Ruta relativa a `Clases/` (misma convención que APA_REL en
# build_acas_estudiantes.py). Decisión del docente 2026-08-10.
RUTA_PLANTILLA_APA = "Recursos/Plantilla_APA_CUN_Proyecto de grado.docx"
# Placeholder de respaldo: los usos por curso deben llamar a
# `cdigital_url(<clave del curso>)`, que devuelve la URL real del aula si existe
# en carga_academica_2026.json (auditadas el 2026-08-10) y el placeholder si no.
URL_CDIGITAL = CDIGITAL_PLACEHOLDER
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


# Colombia no tiene horario de verano: un solo componente STANDARD en UTC-5.
# RFC 5545 exige VTIMEZONE cuando los eventos usan `TZID=`; sin él, algunos clientes
# (no Google) desplazan la hora del encuentro.
VTIMEZONE_BOGOTA = [
    "BEGIN:VTIMEZONE",
    "TZID:America/Bogota",
    "BEGIN:STANDARD",
    "DTSTART:19930404T000000",
    "TZOFFSETFROM:-0500",
    "TZOFFSETTO:-0500",
    "TZNAME:-05",
    "END:STANDARD",
    "END:VTIMEZONE",
]


def tema_por_fecha(course_key: str) -> dict[str, dict]:
    """Mapa dd/mm/YYYY → sesión de sesiones_cun (si existe)."""
    return _tema_por_fecha_catalogo(course_key)


def _meet(course_key: str, titulo_corto: str) -> str:
    """Enlace real del Meet (carga_academica_2026.json → cursos.<key>.meet) o placeholder."""
    return _meet_url(course_key, titulo_corto)


def add_eval_scope_pregrado(prs, idx: int, regimen: str, course_key: str | None = None) -> int:
    """Alcance de la evaluación con la estructura REAL del aula (CDigital).

    Antes esta slide afirmaba que la autoevaluación y la coevaluación «no aplican» en
    pregrado (se apoyaba en el instructivo AFI). La auditoría del libro de
    calificaciones (2026-08-10) mostró que **existen en los cinco cursos**: la
    autoevaluación es un cuestionario y la coevaluación es un **foro**, cada una con su
    peso dentro del tercer corte. El desglose se lee del modelo, no se escribe a mano.
    """
    bullets = [regimen]
    if course_key:
        items = {e.id: e for e in entregas_para_grupo(course_key)}
        auto, coev = items.get("auto"), items.get("coev")
        # El desglose ítem por ítem ya va en la tabla «CÓMO SE CALIFICA» (slide anterior):
        # aquí solo se recuerda dónde está, para no repetir 200 caracteres de porcentajes.
        bullets.append(
            "**Cada corte se compone de ítems concretos del aula** — nombre exacto, tipo de "
            "actividad, peso y cierre: en la tabla «CÓMO SE CALIFICA» de esta presentación."
        )
        if auto and coev:
            bullets.append(
                f"**Autoevaluación ({auto.weight_pct}, cuestionario)** y "
                f"**coevaluación ({coev.weight_pct}, foro)** **sí hacen parte** de la nota "
                "de este curso: van en el tercer corte y se diligencian/participan en el aula."
            )
        bullets.append(
            "Los **quices y parciales** son cuestionarios en CDigital y cierran en día de clase; "
            "la **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción."
        )
    bullets.extend([
        "No confundir con la autoevaluación **institucional** SIAC (calidad de programas en "
        "acreditacion.cun.edu.co): esa no es una nota del curso.",
        "Entregas, rúbricas y publicación de notas: solo por **CDigital**.",
        "Si un peso o una ventana del aula no coincide con este material, **manda el aula**: "
        "se corrige aquí y se avisa en clase.",
    ])
    content_slide(prs, "ALCANCE DE LA EVALUACIÓN", bullets, idx=idx, size=13)
    return idx + 1


def nota_cortes_slide(course_key: str, grupo: str | None = None, extra: str = "") -> str:
    """Nota de la slide de cronograma, leída del modelo (no escrita a mano).

    Las tarjetas de la slide son por CORTE (con 8 ítems por curso no caben); esta nota
    es la que dice qué ítems hay dentro de cada corte y cuándo cierra el documento.
    """
    items = {e.id: e for e in entregas_para_grupo(course_key, grupo)}
    af = items["aca_final"]
    dia = DIAS[COURSES[course_key]["weekday"]]
    txt = (
        f"{desglose_corte_texto(course_key)} — libro de calificaciones de **CDigital**. "
        f"Quices y parciales: **cuestionarios** que cierran en día de clase ({dia}). "
        f"**ACA Final** (tarea/documento) cierra {bold_var(fmt_entrega(af.entrega, largo=False))}. "
        "Enunciados: Clases/Recursos/ACAs/."
    )
    return f"{txt} {extra}".strip()


def items_aula_rows(course_key: str, groups: list[str] | None = None) -> list[list[str]]:
    """Filas de la tabla de evaluación: **un ítem del libro de calificaciones por fila**.

    Nombre exacto del ítem en CDigital, tipo de actividad, corte (con el peso del corte),
    peso del ítem y fecha de cierre. Todo sale de `fechas_entrega_aca` (auditoría
    2026-08-10): en esta slide no se escribe a mano ningún peso ni ninguna fecha.

    En cursos cuyas ventanas varían por grupo (TG3) la columna «Cierre» desglosa
    `fecha (grupos)` **solo** en los ítems cuya fecha difiere; si los tres grupos
    coinciden se muestra una sola fecha (nombrar a un grupo haría pensar a los otros
    dos que no les aplica).
    """
    gs = list(groups or [])
    if (VENTANAS_POR_GRUPO.get(course_key) or {}) and len(gs) > 1:
        data = {g: entregas_para_grupo(course_key, g) for g in gs}
    else:
        data = {None: entregas_para_grupo(course_key)}
    rows: list[list[str]] = []
    for comp in componentes_curso(course_key):
        por_fecha: dict[date, list[str]] = {}
        muestra: dict[date, object] = {}
        for g, items in data.items():
            e = next(x for x in items if x.id == comp["id"])
            por_fecha.setdefault(e.entrega, []).append(g)
            muestra[e.entrega] = e
        if len(por_fecha) == 1:
            cierre = fmt_entrega(next(iter(por_fecha)), largo=False)
        else:
            cierre = " · ".join(
                f"{fmt_entrega(d, largo=False)} ({'/'.join(sorted(x for x in por_fecha[d] if x))})"
                for d in sorted(por_fecha)
            )
        e = muestra[sorted(por_fecha)[0]]
        rows.append([
            f"**{e.code}**",
            e.tipo_label,
            f"{e.corte} ({fmt_peso(peso_corte(course_key, e.corte))})",
            f"**{e.weight_pct}**",
            cierre,
        ])
    return rows


def tabla_items_aula_slide(prs, course_key: str, idx: int) -> int:
    """Slide-tabla «CÓMO SE CALIFICA»: los tres cortes con sus ítems reales del aula.

    La slide de tarjetas (`fechas_inicio_fin_slide`) muestra el periodo de cada corte;
    esta muestra **de qué está hecho** cada corte: quices, parciales, ACA Final,
    autoevaluación y coevaluación, con tipo de actividad, peso y cierre. Es la slide que
    el estudiante necesita para encontrar el ítem en el libro de calificaciones.

    La ficha de origen y la suma van en el **subtítulo**, no en la nota al pie: con 8
    ítems la tabla llega hasta 6,9" y el pie de `table_content` (fijo en 6,65") le
    quedaría encima. Lo que decía esa nota —qué se sube, qué se resuelve, qué es foro—
    lo dice la slide siguiente («ALCANCE DE LA EVALUACIÓN»).
    """
    groups = list(COURSES[course_key]["groups"])
    rows = items_aula_rows(course_key, groups)
    items = entregas_para_grupo(course_key)
    total = fmt_peso(sum(e.weight for e in items))
    docs = [e.code for e in items if e.es_documento]
    sub = (
        "**Libro de calificaciones del aula** (CDigital) · cortes "
        f"{' / '.join(fmt_peso(peso_corte(course_key, c)) for c in (1, 2, 3))} · "
        f"los pesos suman **{total}**"
    )
    note = None
    if len(rows) <= 6:   # con más filas la tabla ocupa el sitio de la nota al pie
        note = (
            f"Se **sube** documento únicamente en **{', '.join(docs)}** (tarea); los "
            "**cuestionarios se resuelven en el aula** y la **coevaluación es un foro**."
        )
    table_content(
        prs, "CÓMO SE CALIFICA — LOS ÍTEMS DEL AULA (CDIGITAL)",
        ["Ítem en CDigital", "Tipo", "Corte (peso)", "Peso del ítem", "Cierre"],
        rows,
        sub=sub,
        note=note,
        col_w=[2.3, 1.5, 1.5, 1.4, 4.6], idx=idx, fs_body=11,
    )
    return idx + 1


def eval_por_fecha(course_key: str, groups: list[str] | None = None) -> dict[str, list[str]]:
    """`dd/mm/YYYY` → ítems del libro de calificaciones que **cierran** ese día.

    Sirve para marcar en el «Calendario de clases (oficial)» en qué sesión cae cada
    quiz y cada parcial: son cuestionarios de CDigital y cierran en día de clase, así
    que el docente necesita verlos junto al tema de la sesión, no en otra tabla.

    En cursos con ventanas por grupo (TG3) la etiqueta nombra los grupos **solo** si la
    fecha difiere entre ellos; si coincide, se deja sin sufijo (nombrar a uno haría
    pensar a los otros que no les aplica).
    """
    porg = VENTANAS_POR_GRUPO.get(course_key) or {}
    gs = list(groups or [])
    if porg and len(gs) > 1:
        data = {g: entregas_para_grupo(course_key, g) for g in gs}
    else:
        data = {(gs[0] if len(gs) == 1 else None): entregas_para_grupo(
            course_key, gs[0] if len(gs) == 1 else None)}
    out: dict[str, list[str]] = {}
    for comp in componentes_curso(course_key):
        por_fecha: dict[date, list[str]] = {}
        muestra: dict[date, object] = {}
        for g, items in data.items():
            e = next(x for x in items if x.id == comp["id"])
            por_fecha.setdefault(e.entrega, []).append(g)
            muestra[e.entrega] = e
        unico = len(por_fecha) == 1
        for d, gg in por_fecha.items():
            e = muestra[d]
            etiquetas = sorted(x for x in gg if x)
            sufijo = "" if (unico or not etiquetas) else f" · grupos {' / '.join(etiquetas)}"
            verbo = "Cierra" if not e.es_instrumento_cierre else "Cierra la ventana de"
            out.setdefault(d.strftime("%d/%m/%Y"), []).append(
                f"**{verbo} {e.code}** ({e.tipo_label.lower()} · {e.weight_pct} · "
                f"corte {e.corte}){sufijo}"
            )
    return out


def tabla_eval_calendario(course_key: str, groups: list[str] | None = None) -> list[str]:
    """Bloque markdown «Evaluación en el aula»: ítem → cierre → sesión en que cae.

    Se genera desde `fechas_entrega_aca` (libro de calificaciones de CDigital); ninguna
    fecha ni peso se escribe a mano aquí.
    """
    temas = tema_por_fecha(course_key)
    porg = VENTANAS_POR_GRUPO.get(course_key) or {}
    gs = list(groups or [])
    if porg and len(gs) > 1:
        data = {g: entregas_para_grupo(course_key, g) for g in gs}
    else:
        data = {(gs[0] if len(gs) == 1 else None): entregas_para_grupo(
            course_key, gs[0] if len(gs) == 1 else None)}
    lines = [
        "## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem",
        "",
        "Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en "
        "`config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con "
        "`python config/slides/build_pregrado_cursos.py --calendar-only`.",
        "",
        "| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |",
        "| :--- | :--- | :---: | ---: | :--- | :--- |",
    ]
    for comp in componentes_curso(course_key):
        por_fecha: dict[date, list[str]] = {}
        muestra: dict[date, object] = {}
        for g, items in data.items():
            e = next(x for x in items if x.id == comp["id"])
            por_fecha.setdefault(e.entrega, []).append(g)
            muestra[e.entrega] = e
        unico = len(por_fecha) == 1
        for d in sorted(por_fecha):
            e = muestra[d]
            etiquetas = sorted(x for x in por_fecha[d] if x)
            sufijo = "" if (unico or not etiquetas) else f" ({' / '.join(etiquetas)})"
            fecha_txt = d.strftime("%d/%m/%Y")
            ses = temas.get(fecha_txt)
            if ses and ses.get("n"):
                donde = f"**S{int(ses['n']):02d}** — {ses['titulo']}"
            elif e.es_documento:
                donde = "— (no cae en día de clase: es la fecha máxima de recepción de trabajos)"
            else:
                donde = "— (no cae en día de clase: ventana hasta el cierre de notas)"
            lines.append(
                f"| **{e.code}**{sufijo} | {e.tipo_label} | {e.corte} | {e.weight_pct} | "
                f"{fecha_txt} | {donde} |"
            )
    lines += [
        "",
        f"**Cortes:** {desglose_corte_texto(course_key)}.",
        "",
        "> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana "
        "abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la "
        "fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y "
        "**coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 "
        "es de encuadre y no evalúa.**",
    ]
    return lines


def recursos_items(course_key: str, titulo_corto: str, *extra: str) -> list[str]:
    """Bullets de la slide RECURSOS (links concretos + placeholders claros).

    Placeholders de oferta (CDigital / Meet) en negrita. Sin nombre propio del docente.
    """
    items = [
        f"**Contacto del Docente:** {DOCENTE_CORREO}",
        f"**CDigital (campus del curso):** {bold_var(cdigital_url(course_key))}",
        f"**Google Meet (mismo enlace toda la serie):** {bold_var(_meet(course_key, titulo_corto))}",
        f"**Plantilla APA CUN – Proyecto de Grado** (viene en tu carpeta del curso): "
        f"`{RUTA_PLANTILLA_APA}`.",
        f"**Plantilla APA CUN (en tu carpeta):** `{RUTA_PLANTILLA_APA}`",
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
    set_footer("")
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
        note=nota_cortes_slide("investigacion"),
        sub=f"Periodo {bold_var('26P03')} · inicio {bold_var('10/08/2026')} · cierre {bold_var('20/09/2026')}",
        idx=_i,
    )
    _i += 1
    _i = tabla_items_aula_slide(prs, "investigacion", _i)
    _i = add_eval_scope_pregrado(
        prs, _i,
        "**Régimen:** Art. 52 del Reglamento Estudiantil · "
        "**Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%**.",
        course_key="investigacion",
    )
    box_note_slide(prs, "ACUERDOS DEL CURSO", [
        ("info", f"Encuentro sincrónico: {bold_var(_inv_h)} por Google Meet. El enlace se publica en el aula virtual."),
        ("aclaracion", "Si el día de clase es festivo colombiano, la sesión NO se cancela: se cursa como **clase autónoma** (material/actividad en el CDigital)."),
        ("advertencia", "El producto final se construye desde la semana 1 — no es una entrega sorpresa al cierre."),
    ], idx=_i)
    _i += 1
    content_slide(prs, "RECURSOS", recursos_items(
        "investigacion",
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
    set_footer("")
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
        note=nota_cortes_slide("creatividad"),
        sub=f"Periodo {bold_var('26V04')} · inicio {bold_var('10/08/2026')} · cierre {bold_var('27/09/2026')}",
        idx=_i,
    )
    _i += 1
    _i = tabla_items_aula_slide(prs, "creatividad", _i)
    _i = add_eval_scope_pregrado(
        prs, _i,
        "**Régimen:** Art. 52 del Reglamento Estudiantil · "
        "**Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%**.",
        course_key="creatividad",
    )
    box_note_slide(prs, "ACUERDOS DEL CURSO", [
        ("info", f"Encuentro sincrónico: {bold_var(_cre_h)} por Google Meet."),
        ("aclaracion", "Festivo en día de clase = **clase autónoma** (actividad en el CDigital), no cancelación."),
        ("advertencia", "La Propuesta de Innovación se explica desde el día 1 y se valida/sustenta hacia la unidad 6."),
    ], idx=_i)
    _i += 1
    content_slide(prs, "RECURSOS", recursos_items(
        "creatividad",
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
    set_footer("")
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
        # Los pesos ya NO son orientativos: están en el libro de calificaciones del aula
        # (auditoría 2026-08-10). Lo que sigue ausente es el Syllabus SIAC de TG2.
        prs, "EVALUACIÓN — CORTES (ART. 52)",
        blocks,
        note=nota_cortes_slide("tg2", extra=f"Recepción máx. de trabajos: {bold_var('14/11/2026')}."),
        sub=f"Inicio {bold_var('10/08/2026')} · cierre {bold_var('22/11/2026')}",
        idx=_i,
    )
    _i += 1
    _i = tabla_items_aula_slide(prs, "tg2", _i)
    _i = add_eval_scope_pregrado(
        prs, _i,
        "**Régimen:** Art. 52 · **Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%**, "
        "tomados del libro de calificaciones del aula (sigue sin cargarse el Syllabus SIAC de TG2).",
        course_key="tg2",
    )
    box_note_slide(prs, "ACUERDOS DEL CURSO", [
        ("info", f"Encuentro sincrónico: {bold_var(_tg2_h)} por Google Meet. El Meet es el mismo enlace para toda la serie."),
        ("aclaracion", "Lunes festivo = **clase autónoma** (guía/actividad en el CDigital), no se pierde el hilo del proyecto."),
        ("advertencia", "Hasta cargar el Syllabus SIAC, cualquier detalle de rubrica/pesos se verifica en el aula virtual."),
    ], idx=_i)
    _i += 1
    content_slide(prs, "RECURSOS", recursos_items(
        "tg2",
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
    set_footer("")
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
        # TG3 NO es «corte único 100% EV05/EXAM» como decía su Syllabus: el aula tiene
        # tres cortes 30/30/40 (auditoría CDigital 2026-08-10).
        # `blocks_tg3_slide()` trae las ventanas del grupo de referencia (54466 = 54467).
        # La ACA Final difiere por grupo, así que la nota la desglosa explícitamente:
        # 15/11 y 22/11 son cierres de NOTAS, no fechas de entrega.
        prs, "EVALUACIÓN — TRES CORTES (ART. 52)",
        blocks,
        note=nota_cortes_slide(
            "tg3", "54466",
            extra=(
                "**ACA Final por grupo** — 54450: "
                f"{bold_var(fmt_entrega(entrega_por_id('tg3', 'aca_final', '54450').entrega, largo=False))} · "
                "54466 y 54467: "
                f"{bold_var(fmt_entrega(entrega_por_id('tg3', 'aca_final', '54466').entrega, largo=False))}. "
                f"(El cierre de notas es posterior: 54450 {bold_var('15/11/2026')}, "
                f"54466/54467 {bold_var('22/11/2026')}.)"
            ),
        ),
        sub=f"Art. 52 · inicio {bold_var('10/08/2026')} · día de clase mar",
        idx=_i,
    )
    _i += 1
    # TG3: la columna «Cierre» de esta tabla desglosa por grupo los tres ítems cuyas
    # ventanas difieren (ACA Final, autoevaluación y coevaluación en 54450); el cierre
    # de notas por grupo ya lo dice la nota de la slide de cortes.
    _i = tabla_items_aula_slide(prs, "tg3", _i)
    _i = add_eval_scope_pregrado(
        prs, _i,
        "**Régimen:** Art. 52 · **tres cortes 30% / 30% / 40%** según el libro de "
        "calificaciones del aula (el Syllabus SIAC 94532 declaraba «corte único 100%»: "
        "manda el aula).",
        course_key="tg3",
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
        "tg3",
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
    meet = _meet(course_key, course["titulo_corto"])

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
    # Drive puede dejar la carpeta del grupo sin crear (ya pasó 2 veces): sin este mkdir el
    # build revienta a mitad, después de haber escrito los PPTX.
    out_dir.mkdir(parents=True, exist_ok=True)
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
            f"X-WR-CALNAME:{course['titulo_corto']} {g_lbl} Encuentros",
            "X-WR-TIMEZONE:America/Bogota",
            *VTIMEZONE_BOGOTA,
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
        "| # | Fecha | Tipo | Subject (Calendar) | Evaluación (aula CDigital) |",
        "|---|---|---|---|---|",
    ]
    evals = eval_por_fecha(course_key, groups_for_event)
    for i, d, tipo, tema_txt, subject in cal_md_rows:
        ev_txt = " · ".join(evals.get(d.strftime("%d/%m/%Y"), [])) or "—"
        lines.append(
            f"| {i} | {d.strftime('%d/%m/%Y')} ({DIAS[d.weekday()]}) | {tipo} | {subject} "
            f"| {ev_txt} |"
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
        *tabla_eval_calendario(course_key, groups_for_event),
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
        "> **Evento** = fila del CSV/ICS (incluye las clases autónomas por festivo). "
        "**Sesión** = numeración del catálogo, la que usan el guion, el `.pptx` y el Subject "
        "de Calendar. En cursos con festivos los dos números NO coinciden.",
        "> La columna **Evaluación (aula CDigital)** marca qué ítem del libro de "
        "calificaciones cierra ese día (quices y parciales son cuestionarios y cierran en día "
        "de clase). Detalle completo en «Evaluación en el aula» al final de este archivo.",
        "",
        "| Evento | Sesión | Fecha | Tipo | Tema (Syllabus / plan) | Evaluación (aula CDigital) |",
        "|---|---|---|---|---|---|",
    ]
    evals = eval_por_fecha(course_key, course["groups"])
    for i, d in enumerate(sessions, 1):
        fecha_txt = d.strftime("%d/%m/%Y")
        ses = temas.get(fecha_txt)
        n_ses = f"**{ses['n']:02d}**" if ses and ses.get("n") else "—"
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
        ev_txt = " · ".join(evals.get(fecha_txt, [])) or "—"
        lines.append(
            f"| {i} | {n_ses} | {fecha_txt} ({DIAS[d.weekday()]}) | {tipo} | {tema_txt} "
            f"| {ev_txt} |"
        )
        # La unidad que pasó a lectura autónoma vive en el catálogo y solo la documentaba
        # Proyecto I; sin esta fila el calendario deja «desaparecidas» U1–U2.
        if ses and ses.get("unidad_diferida"):
            lines.append(
                f"| — | — | (misma semana) | ⚠️ Lectura autónoma | {ses['unidad_diferida']} | — |"
            )

    # Los ítems que NO cierran en día de clase (ACA Final, auto y coevaluación) no
    # aparecerían en la tabla de sesiones: van completos en el bloque de evaluación.
    lines += ["", *tabla_eval_calendario(course_key, course["groups"])]

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
