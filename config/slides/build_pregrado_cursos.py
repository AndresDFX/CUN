# -*- coding: utf-8 -*-
"""Presentaciones + calendarios de las 4 asignaturas de Pregrado (CUN)
   + «Calendario de clases (oficial)» de PROYECTO I (Especialización · AFI).

Por qué Proyecto I vive aquí y no en su propio archivo: el motor del calendario
oficial (catálogo de sesiones ↔ fechas, festivos, ventanas del libro de
calificaciones, tabla de evaluación) está completo en este módulo y en ninguna otra
parte. Duplicarlo para un quinto curso garantizaba que las dos copias se
desincronizaran — que es exactamente lo que pasó mientras ese archivo se mantuvo a
mano. Proyecto I **no** entra en `COURSES`: sus PPTX (`build_cun_proyecto1.py`), su
CSV/ICS con invitados y su `Informacion.txt` (`build_calendar_proyecto1_54es4.py`) ya
tienen dueño, y meterlo en `COURSES` los sobrescribiría. Entra por `COURSE_P1` y por
`write_calendario_proyecto1()`, que aplican sus reglas propias (ver §PROYECTO I).

Reglas:
- Presentación del Curso en <Asignatura>/Clases/: grupo(s) solo en portada;
  tutor_slide genérico («Docente» + perfil + correo); CONTENIDO en UNA slide
  (Sesión N — tema; helper contenido_sesiones_slide); recursos/cierre sin grupo ni nombre propio.
- Si el día de clase cae en festivo colombiano → la sesión queda como CLASE AUTÓNOMA
  (sigue en el calendario, marcada; no se cancela). El material y la actividad de esa
  clase quedan en la carpeta de la sesión dentro del **Drive de clases** (`Clases/`),
  no en CDigital: CDigital es donde se ENTREGA y donde están las NOTAS.
- Eventos de Calendar (encuentros): Subject corto =
  `{periodo} - {grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo; sin
  tema largo). El periodo va delante porque el nombre del evento es la clave de
  búsqueda en la carpeta única de grabaciones, que acumula todos los periodos.
  Fuente de fechas/temas (Description): `sesiones_cun.py`.
- Horarios confirmados por el docente:
    TG2  → lunes 5:00–6:00 pm
    TG3  → martes 5:00–6:00 pm
    Creatividad → miércoles 5:00–6:00 pm
    Investigación → jueves 5:00–6:00 pm
    Proyecto I → lunes 8:00–10:00 pm (Especialización · franja AFI 19:00–22:00 h)

§PROYECTO I — en qué se aparta de pregrado (por eso tiene su propio writer):
- Festivo: el Instructivo AFI dice que en lunes festivo **NO hay sincrónico** (clase
  pregrabada en CDigital), no «clase autónoma que sigue en el calendario». Su catálogo
  de sesiones salta los lunes festivos y no los numera.
- Evaluación 25 / 25 / 50 (no 30/30/40) y sobre nota única Art. 41 §3, no Art. 52.
- Ningún ítem cierra en día de clase: las ventanas de Coordinación cierran en domingo y
  la clase es lunes. La columna útil no es «en qué sesión cae» sino «última sincrónica
  antes del cierre».
- Encuentro de 2 h = ~1 h de contenido + 1 h de tutoría por grupo (AFI).
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
    clases_url,
    course_dir as _course_dir,
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
from sesiones_cun import (  # noqa: E402  (AFI · solo los usa el calendario de Proyecto I)
    CURSOS_CON_TUTORIAS_POR_GRUPO,
    LINK_REGISTRO_DOCENTE_AFI,
    LINK_TUTORIAS,
    MSG_TUTORIAS_POR_GRUPO,
)
# La plantilla NO se enlaza por URL pública: viaja DENTRO de la carpeta que recibe el
# estudiante. Ruta relativa a `Clases/` (misma convención que APA_REL en
# build_acas_estudiantes.py). Decisión del docente 2026-08-10.
RUTA_PLANTILLA_APA = "Recursos/Plantilla_APA_CUN_Proyecto de grado.docx"
# Placeholder de respaldo: los usos por curso deben llamar a
# `cdigital_url(<clave del curso>)`, que devuelve la URL real del aula si existe
# en carga_academica_2026.json (auditadas el 2026-08-10) y el placeholder si no.
URL_CDIGITAL = CDIGITAL_PLACEHOLDER
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
DIAS_LARGO = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

# ---------------------------------------------------------------------------
# CLASE AUTÓNOMA (festivo en día de clase) — dónde vive el material
# ---------------------------------------------------------------------------
# Decisión del docente (2026-08-11): el material y la actividad de la clase autónoma
# quedan en la **carpeta de esa sesión dentro del Drive de clases** —la carpeta
# `Clases/` que el Docente comparte, la misma que describe el LEEME del estudiante—,
# **no** en CDigital. Antes todo el material decía «actividad en el CDigital».
# Los dos roles no se mezclan: el Drive tiene el MATERIAL; CDigital sigue siendo donde
# se ENTREGA y donde están las NOTAS. Enlace de la carpeta: `clases_url(<clave>)`
# (carga_academica_2026.json → cursos.<key>.clases; vacío ⇒ marcador de posición).
CARPETA_SESION_DRIVE = "`Clases/Sesion NN - …/`"
AVISO_AUTONOMA_DRIVE = (
    "la actividad y el material quedan en la **carpeta de esa sesión en el Drive de "
    f"clases** ({CARPETA_SESION_DRIVE}); la entrega y la nota siguen en **CDigital**"
)

# Flujo principal vs. respaldo. Los nombres se importan de su dueño (el builder del .gs)
# para que no haya dos verdades sobre cómo se llama el archivo que el docente debe abrir.
from build_calendar_encuentros import (  # noqa: E402
    GS_NAME as GS_PRINCIPAL,
    GS_NAME_TG3 as GS_PRINCIPAL_TG3,
    LEEME_NAME as LEEME_ENCUENTROS,
)
# Prefijo de los .ics/.csv de encuentros. Existen solo como respaldo de fechas: Google
# Calendar DESCARTA los invitados al importarlos, así que un docente que importe el que
# está al lado del .gs se queda con la serie vacía de estudiantes. El aviso va en el
# nombre del archivo porque es lo primero (y a veces lo único) que se lee.
RESPALDO_PREFIJO = "RESPALDO sin invitados - "


def _borrar_legacy(out_dir: Path, nombres: list[str], conservar: set[str] | None = None) -> None:
    """Retira archivos con nombres de versiones anteriores del build.

    Un archivo generado que cambia de nombre no desaparece solo: se queda al lado del
    nuevo, con contenido plausible y desactualizado. En esta carpeta eso significa que el
    docente puede importar el que no es.
    """
    conservar = conservar or set()
    for n in nombres:
        if n in conservar:
            continue
        p = out_dir / n
        if p.is_file():
            try:
                p.unlink()
            except OSError:
                pass


# Carpetas de TG3 que este build emitía antes del 2026-08-11 y que ya no debe emitir:
# eran juegos alternativos de los MISMOS encuentros (dos grupos, o los tres pero cortados
# el 15/11), sobrantes de planes previos a la decisión del docente de «un solo enlace para
# los tres grupos». Con cuatro juegos conviviendo, importar el que no es duplicaba eventos.
COMBINADOS_OBSOLETOS_TG3 = ("_combinado_54466-54467", "_combinado_todos_hasta_15-11")


def _retirar_combinados_obsoletos(base_2026: Path) -> None:
    """Borra las carpetas `_combinado_*` obsoletas de TG3, si siguen ahí.

    Solo retira archivos generados por este mismo build (md/csv/ics de encuentros). Si
    queda algo que no reconoce, deja la carpeta y lo avisa en vez de borrar a ciegas.
    """
    for nombre in COMBINADOS_OBSOLETOS_TG3:
        carpeta = base_2026 / nombre
        if not carpeta.is_dir():
            continue
        for f in sorted(carpeta.iterdir()):
            if f.is_file() and f.suffix.lower() in {".md", ".csv", ".ics"}:
                try:
                    f.unlink()
                except OSError:
                    pass
        restos = list(carpeta.iterdir())
        if restos:
            print(f"AVISO: {carpeta} no se pudo retirar; quedan "
                  f"{', '.join(r.name for r in restos)}")
            continue
        try:
            carpeta.rmdir()
            print(f"OK RETIRADA carpeta obsoleta -> {carpeta}")
        except OSError as e:
            print(f"AVISO: no se pudo borrar {carpeta}: {e}")


def plural(n: int, singular: str, plural_: str) -> str:
    """`1 sesión` / `2 sesiones` — sin «(s)» en el material del docente."""
    return f"{n} {singular if n == 1 else plural_}"


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
        # Carpeta `Clases/` compartida en Drive: material de cada sesión y, cuando el día
        # de clase es festivo, la actividad de la clase autónoma.
        f"**Material de clases (Drive):** {bold_var(clases_url(course_key, titulo_corto))} — "
        "aquí está el material de cada sesión, incluida la de una **clase autónoma**.",
        f"**Plantilla APA CUN – Proyecto de Grado** (viene en tu carpeta del curso): "
        f"`{RUTA_PLANTILLA_APA}`.",
        f"**Plantilla APA CUN (en tu carpeta):** `{RUTA_PLANTILLA_APA}`",
        "**Enunciados ACA / cortes (estudiantes):** `Clases/Recursos/ACAs/`.",
    ]
    items.extend(extra)
    return items


def add_tutor(prs, idx: int = 2):
    tutor_slide(prs, "Docente", DOCENTE_CREDS, DOCENTE_CORREO, idx=idx)


def add_icebreaker(prs, course_key: str, idx: int = 3, *, pide: str | None = None):
    """Rompehielos «Preséntate» de la Presentación del Curso (los 5 cursos).

    La FORMA no se elige aquí: `icebreaker_qr_slide` cuenta la matrícula real del curso
    (roster de CDigital) y sirve el muro de Padlet en los grupos de hasta
    `ICEBREAKER_MAX_MURO` estudiantes; por encima sirve el juego **«Dos verdades y una
    mentira» en Slido** (quiz de 3 rondas sobre el Docente + Q&A), que con 50 —o con los
    112 de TG3— es lo único que cabe en la hora: un muro de 50 notas no lo lee nadie y
    una ronda de presentaciones se come la clase. De este lado viaja solo lo que sí
    cambia entre cursos: `pide`, lo que se le pide al estudiante además del nombre (lo
    usa el modo muro; en el juego, el que se presenta es el Docente).

    Las frases de las tres rondas y **cuál es la mentira** no viven en ninguna deck: son
    material del Docente, en `<Asignatura>/2026/<grupo>/Rompehielos Slido - Sesion 01.md`
    (`python config/slides/build_rompehielos_slido.py`).
    """
    icebreaker_qr_slide(prs, idx=idx, course_key=course_key, pide=pide)

# Festivos Colombia 2026 relevantes al periodo ago–nov (incl. trasladados a lunes)
FESTIVOS_2026 = {
    D(2026, 8, 7): "Batalla de Boyacá",
    D(2026, 8, 17): "Asunción de la Virgen",
    D(2026, 10, 12): "Día de la Raza",
    D(2026, 11, 2): "Todos los Santos",
    D(2026, 11, 16): "Independencia de Cartagena",
}


# Festivos que caen en lunes por la Ley Emiliani: fecha real de la efeméride. Va aparte
# de FESTIVOS_2026 para no alterar el texto ya publicado en los 4 calendarios de pregrado
# (que solo nombran el festivo); lo usa la tabla de festivos de Proyecto I.
FESTIVOS_TRASLADO_2026 = {
    D(2026, 8, 17): D(2026, 8, 15),
    D(2026, 11, 2): D(2026, 11, 1),
    D(2026, 11, 16): D(2026, 11, 11),
}


def nombre_festivo(d: date, *, con_traslado: bool = False) -> str:
    """«Todos los Santos» / «Todos los Santos (trasladado del dom. 01/11)»."""
    nombre = FESTIVOS_2026[d]
    orig = FESTIVOS_TRASLADO_2026.get(d) if con_traslado else None
    if not orig:
        return nombre
    return f"{nombre} (trasladado del {DIAS[orig.weekday()]}. {orig.strftime('%d/%m')})"


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


def fechas_de_clase(course_key: str, inicio: date, fin: date, weekday: int) -> list[date]:
    """Días con evento: los del catálogo de sesiones MÁS los festivos del día de clase.

    Antes se recorría solo la rejilla semanal (`weekday_dates`) y las sesiones se cruzaban
    por fecha. Eso se rompe en cuanto una sesión se reprograma a otro día de la semana: la
    sesión desaparece del CSV/ICS y el hueco que deja en la rejilla sale como «Encuentro»
    genérico. Pasó al mover la Sesión 01 de TG2 del lunes 10/08 al viernes 14/08.

    La rejilla se sigue usando **solo** para detectar los festivos, que sí generan su
    «clase autónoma» aunque no tengan sesión en el catálogo. En los cursos sin
    reprogramaciones el resultado es idéntico al anterior.
    """
    fechas = {d for d in weekday_dates(inicio, fin, weekday) if is_festivo(d)}
    for s in SESIONES_COURSES[course_key]["sesiones"]:
        d = _dt.datetime.strptime(s["fecha"], "%d/%m/%Y").date()
        if inicio <= d <= fin:
            fechas.add(d)
    return sorted(fechas)


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

# ---------------------------------------------------------------------------
# PROYECTO I (Especialización · AFI) — solo «Calendario de clases (oficial).md».
# Deliberadamente FUERA de COURSES: `write_all_calendars()` y `main()` iteran ese
# dict para escribir CSV/ICS por grupo, PPTX e Informacion.txt, y los tres ya los
# genera otro build para Proyecto I (ver docstring). Meterlo ahí borraría el CSV/ICS
# con invitados + coanfitrión + Meet de la serie que produce
# build_calendar_proyecto1_54es4.py.
# ---------------------------------------------------------------------------
P1_KEY = "proyecto1"
COURSE_P1 = pregrado_build_dict(P1_KEY)

# Franja horaria oficial de encuentros sincrónicos de Especializaciones
# (Instructivo_encuentros_sincronicos_Especializaciones_AFI.pdf). El horario concreto
# del curso sale de carga_academica_2026.json; esto es el marco que debe cumplir.
FRANJA_AFI = "19:00–22:00 h"
DURACION_AFI = "1 h 30 min – 2 h"
# El propio portal sugiere 20:00–22:00 h para esta oferta; el horario confirmado coincide.
SUGERENCIA_PORTAL_AFI = "20:00–22:00 h"

# Instructivo AFI §3: el lunes festivo NO se convierte en «clase autónoma» como en
# pregrado — no hay sincrónico y se deja clase pregrabada.
REGLA_FESTIVO_AFI = (
    "En lunes festivo **no se hace encuentro sincrónico** (Instructivo de encuentros "
    "sincrónicos de Especializaciones, §3). Opción principal: **clase pregrabada** "
    "disponible en CDigital; opción excepcional: **reprogramar**, solo por coincidencia "
    "con festivo y avisando con anticipación."
)

# ESP329 cita el Art. 41 §3 (nota única); el aula la reparte en tres cortes.
REGIMEN_P1 = (
    "**Nota única 100%** (ESP329 · Art. 41 §3 del Reglamento Estudiantil), registrada en "
    "el aula en **tres cortes 25% / 25% / 50%**"
)

# Manual del Docente P1 §Informe Final de Curso (mismo plazo en el Checklist de cierre).
PLAZO_INFORME_FINAL = "3 días hábiles"

# Requisito del Instructivo AFI (Especializacion/0. General/01_Instructivos_AFI_Proyecto_I_II/):
# la entrega de las ACAs es grupal y Moodle no la habilita sin esta actividad.
NOTA_EQUIPOS_AFI = (
    "La actividad **«Conformación de equipos»** tiene que quedar habilitada en CDigital "
    "desde el encuadre: sin ella **no hay entrega grupal** (Instructivo AFI). Los equipos "
    "se arman en la hora de tutoría de la Sesión 01."
)


def ensure_dirs(course_dir: Path):
    (course_dir / "Clases").mkdir(parents=True, exist_ok=True)
    (course_dir / "Docente" / "Guiones" / "Capturas").mkdir(parents=True, exist_ok=True)


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
    add_icebreaker(
        prs, "investigacion", idx=3,
        pide="**expectativa del curso** + una **idea de tema** para el artículo (1 frase)",
    )
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
        ("aclaracion", "Si el día de clase es festivo colombiano, la sesión NO se cancela: se cursa "
                       f"como **clase autónoma** y {AVISO_AUTONOMA_DRIVE}."),
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
    add_icebreaker(
        prs, "creatividad", idx=3,
        pide="**expectativa del curso** + un **tema o problema** que te interese (1 frase)",
    )
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
        ("aclaracion", "Festivo en día de clase = **clase autónoma**, no cancelación: "
                       f"{AVISO_AUTONOMA_DRIVE}."),
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
    add_icebreaker(
        prs, "tg2", idx=3,
        pide="el **estado actual** de tu proyecto (1 frase) + tu **expectativa de TG2**",
    )
    content_slide(prs, "¿QUÉ ES TRABAJO DE GRADO 2?", [
        "Espacio de **opción de grado** (pregrado): avance consolidado del **documento** de grado antes de la culminación en Trabajo de Grado 3.",
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
        "tomados del libro de calificaciones del aula. El Syllabus SIAC de TG2 (recibido el 22/08/2026) "
        "declara CORTE ÚNICO = 100 %; **manda el aula**.",
        course_key="tg2",
    )
    box_note_slide(prs, "ACUERDOS DEL CURSO", [
        ("info", f"Encuentro sincrónico: {bold_var(_tg2_h)} por Google Meet. El Meet es el mismo enlace para toda la serie."),
        ("aclaracion", "Lunes festivo = **clase autónoma**, no se pierde el hilo del proyecto: "
                       f"{AVISO_AUTONOMA_DRIVE}."),
        ("advertencia", "El Syllabus dice corte único y el aula dice 30/30/40: cualquier detalle de rubrica o peso se verifica en el aula virtual, que es la que manda."),
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
    add_icebreaker(
        prs, "tg3", idx=3,
        pide="el **tema de tu trabajo de grado** (1 frase) + tu **expectativa del semestre**",
    )
    content_slide(prs, "¿QUÉ ES TRABAJO DE GRADO 3?", [
        "Culminación de la **opción de grado**: **documento** de grado + **producto** + sustentación.",
        "Prerrequisito: Opción de grado II.",
        "El documento —por defecto, **artículo resultado de investigación**— con revisión rigurosa (≥ 50 referencias; extensión no inferior a 4.000 palabras, según Syllabus).",
        "Otras modalidades (proyecto aplicado, prototipo, sistematización) cumplen los **mismos mínimos**: cambia el peso de las secciones, no el esqueleto.",
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
        ("aclaracion", "Martes festivo = **clase autónoma**: el avance guiado queda en la **carpeta "
                       f"de esa sesión en el Drive de clases** ({CARPETA_SESION_DRIVE}); la entrega "
                       "y la nota siguen en **CDigital**."),
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
        "Objetivo del periodo: documento listo + sustentación ante jurados.",
    ], "94532 · Trabajo de Grado 3")
    prs.save(str(out))
    print("OK PPTX", out, "slides", len(prs.slides))


# ---------------------------------------------------------------------------
# Calendarios
# ---------------------------------------------------------------------------
def ics_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def write_calendar_files(course_key: str, course: dict, groups_for_event: list[str],
                         out_dir: Path, end: date, *, con_ics: bool = True,
                         grupos_evento: list[str] | None = None):
    """Genera CSV + ICS + markdown para un conjunto de grupos que comparten horario.
    Pregrado: sin Guests/ATTENDEE. Festivo = clase autónoma (sigue en calendar; su
    material va a la carpeta de la sesión en el Drive de clases, no a CDigital).
    Subject: `{periodo} - {grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo).

    `con_ics=False` escribe **solo** el markdown de referencia del grupo. Es lo que se hace
    con los tres grupos de TG3: sus encuentros son UNA sola serie (`2026/_combinado_todos/`),
    así que un `.ics` por grupo no es un respaldo — es un tercer juego de los mismos eventos
    que, importado, los triplica.

    En un archivo multi-grupo cada sesión invita solo a los grupos **cuyo cierre no ha
    pasado** (54450 de TG3 cierra el 15/11 y los otros dos el 22/11). Así el Subject del
    respaldo dice lo mismo que el `.gs` de la serie, evento por evento.

    `grupos_evento` son los grupos que salen en el **Subject**, cuando no coinciden con los
    del archivo: el calendario de 54450 lista los eventos de la serie de los tres, porque son
    los que va a ver en Calendar. Si se pusiera solo «54450», la tabla anunciaría un título
    de evento que no existe.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    sessions = fechas_de_clase(course_key, course["inicio"], end, course["weekday"])
    temas = tema_por_fecha(course_key)
    g_lbl = groups_label(groups_for_event)
    g_file = groups_label(groups_for_event, for_filename=True)
    meet = _meet(course_key, course["titulo_corto"])

    en_subject = grupos_evento or groups_for_event

    def grupos_de(d: date) -> list[str]:
        """Grupos vivos en esa fecha (solo importa cuando la serie cubre varios)."""
        if len(en_subject) == 1:
            return en_subject
        vivos = [g for g in en_subject if d <= course["group_meta"][g]["cierre"]]
        return vivos or en_subject

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
        grupos_d = grupos_de(d)

        # n/tema = catálogo sesiones_cun (alineado a carpetas Sesion NN).
        # Festivo sin entrada en catálogo → Clase autónoma (…) (autónoma).
        if ses:
            n_ses = int(ses["n"])
            titulo_ses = ses["titulo"]
            tema_txt = f"Sesión {n_ses:02d} — {titulo_ses}"
            subject = subject_encuentro(
                course_key, grupos_d,
                n=n_ses, titulo_sesion=titulo_ses,
                autonoma=auto, festivo_nombre=fest_name or None,
            )
        elif auto:
            tema_txt = f"Clase autónoma — continuar avance (festivo: {fest_name})"
            subject = subject_encuentro(
                course_key, grupos_d,
                autonoma=True, festivo_nombre=fest_name,
            )
        else:
            tema_txt = "Encuentro sincrónico (ver Manual / Syllabus)"
            subject = subject_encuentro(course_key, grupos_d)

        # Description corta (2–4 líneas). Location vacío sin Meet real.
        if auto:
            # El material de la clase autónoma vive en la carpeta de la sesión del Drive
            # de clases; CDigital es donde se entrega y donde salen las notas.
            if ses:
                desc = (
                    f"Sesión {int(ses['n']):02d} — {ses['titulo']} (autónoma)\n"
                    f"Festivo: {fest_name}. Actividad en la carpeta de la sesión "
                    "(Drive de clases); la entrega va por CDigital."
                )
            else:
                desc = (
                    f"Clase autónoma — {fest_name}\n"
                    "Actividad en la carpeta de la sesión (Drive de clases); "
                    "la entrega va por CDigital."
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

    # El nombre del archivo es lo primero que ve el docente: sin la marca «RESPALDO», el
    # .ics que está al lado del .gs invita a importarlo — y Google descarta los invitados.
    stem = f"{RESPALDO_PREFIJO}Encuentros {course['titulo_corto']} - {g_file}"
    csv_path = out_dir / f"{stem}.csv"
    ics_path = out_dir / f"{stem}.ics"

    # Drive puede dejar la carpeta del grupo sin crear (ya pasó 2 veces): sin este mkdir el
    # build revienta a mitad, después de haber escrito los PPTX.
    out_dir.mkdir(parents=True, exist_ok=True)
    _borrar_legacy(out_dir, [
        # Nombres anteriores (sin la marca RESPALDO). Se retiran siempre, también cuando
        # `con_ics=False`: en TG3 son justo los que duplicaban la serie del .gs.
        f"Encuentros {course['titulo_corto']} - {g_file} - Importar a Calendar.csv",
        f"Encuentros {course['titulo_corto']} - {g_file} - Importar a Calendar.ics",
    ])
    if not con_ics:
        _borrar_legacy(out_dir, [csv_path.name, ics_path.name])

    if con_ics:
        with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
                "Subject", "Start Date", "Start Time", "End Date", "End Time",
                "All Day Event", "Description", "Location", "Private",
            ])
            w.writeheader()
            w.writerows(rows)

        ics_path.write_text(
            "\r\n".join([
                "BEGIN:VCALENDAR", "VERSION:2.0",
                "PRODID:-//CUN//Pregrado Encuentros//ES",
                "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
                f"X-WR-CALNAME:{course['titulo_corto']} {g_lbl} Encuentros (respaldo)",
                "X-WR-TIMEZONE:America/Bogota",
                *VTIMEZONE_BOGOTA,
                *ics_events, "END:VCALENDAR",
            ]) + "\r\n",
            encoding="utf-8",
        )

    # Calendario markdown
    gs_nombre = GS_PRINCIPAL_TG3 if course_key == "tg3" else GS_PRINCIPAL
    lines = [
        f"# Calendario — {course['titulo_largo']}",
        f"**{g_lbl}** · Horario: **{course['horario_txt']}**",
        "",
        "> **Este archivo es de consulta: no crea eventos.** Los encuentros se crean con "
        f"`{gs_nombre}` (Apps Script), que es lo único que añade a los estudiantes como "
        "invitados y pone el Meet. Paso a paso en "
        f"`{LEEME_ENCUENTROS}`.",
        "> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` "
        "(fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo. "
        "El periodo va delante porque el nombre del evento es la clave de búsqueda en la carpeta "
        "de grabaciones, que acumula todos los periodos.",
        "> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa "
        "como **clase autónoma** (no se cancela): la actividad queda en la carpeta de esa sesión "
        "en el **Drive de clases**, y la entrega y la nota siguen en **CDigital**.",
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
        f"- Sesiones del periodo: **{len(sessions)}**",
        "",
        "## Cómo se crean estos eventos",
    ]
    if con_ics:
        lines += [
            f"1. **Flujo principal:** `{gs_nombre}` en esta misma carpeta → Apps Script → "
            f"`verificar()` y luego `crearEncuentros()`. Es lo único que añade a los "
            "estudiantes como **invitados** y deja el **mismo enlace de Meet** en toda la serie. "
            f"Instrucciones: `{LEEME_ENCUENTROS}`.",
            f"2. **Respaldo (`{csv_path.name}` / `{ics_path.name}`):** ⚠️ Google Calendar "
            "**descarta los invitados** al importar `.ics`/`.csv`. Estos archivos solo llevan "
            "fechas y títulos; úsalos si necesitas el cronograma en un calendario que no sea "
            "Google, no para crear la serie del curso.",
            f"3. Enlace de Meet: {meet}. No va dentro del respaldo; lo pone el `.gs`.",
        ]
    else:
        lines += [
            f"Con `{gs_nombre}`, que está en `2026/_combinado_todos/`. Los tres grupos de TG3 "
            "son **una sola serie** (mismo horario, misma sala de Meet), así que hay un único "
            f"script y un único juego de eventos. Instrucciones: "
            f"`2026/_combinado_todos/{LEEME_ENCUENTROS}`.",
            "",
            "⚠️ Este grupo **no tiene** `.ics`/`.csv` de encuentros propio, y es a propósito: "
            "importar el de cada grupo crearía los mismos eventos tres veces. El respaldo de "
            "fechas de la serie está también en `_combinado_todos/`.",
            "",
            "Lo que sí se importa desde esta carpeta es "
            "`Entregas y hitos docentes - Importar a Calendar.csv`: son recordatorios tuyos, "
            "sin invitados, y los cierres de ACA **no** coinciden entre los tres grupos.",
        ]
    lines += [
        "",
        *tabla_eval_calendario(course_key, groups_for_event),
        "",
        "Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`",
    ]
    (out_dir / f"Calendario de clases - {g_file}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Limpia duplicado antiguo con raya tipográfica
    _borrar_legacy(out_dir, [f"Calendario de clases — {g_file}.md"],
                   conservar={f"Calendario de clases - {g_file}.md"})
    print(f"OK CAL {course_key} {g_lbl}: {len(sessions)} sesiones"
          f"{'' if con_ics else ' (solo md: la serie es única)'} -> {out_dir}")


def write_calendario_curso(course_key: str, course: dict, course_dir: Path):
    """Calendario oficial en raíz del curso, con mapeo tema↔fecha del Syllabus."""
    end = max(m["cierre"] for m in course["group_meta"].values())
    sessions = fechas_de_clase(course_key, course["inicio"], end, course["weekday"])
    temas = tema_por_fecha(course_key)
    syllabus = SESIONES_COURSES.get(course_key, {})
    n_temas = len(syllabus.get("sesiones") or [])
    lines = [
        f"# Calendario de clases (oficial) — {course['titulo_largo']}",
        f"Plantilla del curso · Horario: **{course['horario_txt']}**",
        f"Grupos de este periodo: **{', '.join(course['groups'])}**",
        f"Docente: **{DOCENTE}** · {DOCENTE_CORREO}",
        "",
        "> Si el día de clase es **festivo colombiano**, la sesión se considera **clase autónoma**: "
        "la actividad queda en la carpeta de esa sesión del **Drive de clases** "
        f"({CARPETA_SESION_DRIVE}), y la entrega y la nota siguen en **CDigital**.",
        "> Los CSV/ICS de Pregrado **no** incluyen invitados/estudiantes.",
        "> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` "
        "(+ ` (autónoma)` si festivo). Fuente: `sesiones_cun.py`.",
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

    if course_key == "tg3":
        donde = ("`2026/_combinado_todos/` — los tres grupos son **una sola serie** (mismo "
                 "horario y misma sala de Meet), así que hay un único script y un único juego "
                 "de eventos para 54450, 54466 y 54467")
    else:
        donde = f"`2026/{course['groups'][0]}/`"
    lines += [
        "",
        "## Cómo llegan estos encuentros a Calendar",
        "",
        f"Con `{GS_PRINCIPAL_TG3 if course_key == 'tg3' else GS_PRINCIPAL}`, en {donde}. Es un "
        "Apps Script y es lo único que añade a los estudiantes como **invitados** y deja el "
        f"**mismo enlace de Meet** en toda la serie. Paso a paso: `{LEEME_ENCUENTROS}`, en esa "
        "misma carpeta.",
        "",
        "⚠️ Los `.ics`/`.csv` que hay junto al script llevan el prefijo "
        f"`{RESPALDO_PREFIJO.strip(' -')}` porque **Google Calendar descarta los invitados** al "
        "importarlos: sirven como respaldo de fechas, no para crear la serie del curso.",
    ]
    (course_dir / "Calendario de clases (oficial).md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# PROYECTO I (Especialización · AFI) — calendario oficial
# ---------------------------------------------------------------------------
def sesiones_catalogo(course_key: str) -> list[tuple[date, dict]]:
    """`(fecha, sesión)` del catálogo `sesiones_cun`, ordenadas por fecha."""
    out = [
        (_dt.datetime.strptime(s["fecha"], "%d/%m/%Y").date(), s)
        for s in (SESIONES_COURSES[course_key].get("sesiones") or [])
    ]
    out.sort(key=lambda t: t[0])
    return out


def ultima_sincronica(sesiones: list[tuple[date, dict]], hasta: date):
    """Última sesión sincrónica en o antes de `hasta` (None si no hay ninguna).

    En Proyecto I ningún ítem cierra en día de clase —las ventanas de Coordinación
    cierran en domingo y la clase es lunes—, así que la pregunta útil no es «en qué
    sesión cae» sino «cuál fue la última clase para hablar de esto».
    """
    previas = [t for t in sesiones if t[0] <= hasta]
    return previas[-1] if previas else None


def sesion_ref(par: tuple[date, dict] | None) -> str:
    if not par:
        return "— (sin sesión previa: la ventana abre antes del inicio del curso)"
    d, ses = par
    return f"**S{int(ses['n']):02d}** ({d.strftime('%d/%m')}) — {ses['titulo']}"


def lunes_del_periodo(course: dict) -> list[date]:
    """Todos los días de clase del periodo, festivos incluidos (para la tabla)."""
    fin = max(m["cierre"] for m in course["group_meta"].values())
    return weekday_dates(course["inicio"], fin, course["weekday"])


def cobertura_item(e, lunes: list[date], sesiones: list[tuple[date, dict]]) -> dict:
    """Cuántos días de clase y cuántas sesiones sincrónicas caen dentro de una ventana."""
    en_ventana = [d for d in lunes if e.apertura <= d <= e.entrega]
    festivos = [d for d in en_ventana if is_festivo(d)]
    ses = [t for t in sesiones if e.apertura <= t[0] <= e.entrega]
    anteriores = [t for t in sesiones if t[0] < e.apertura]
    return {
        "lunes": en_ventana,
        "festivos": festivos,
        "sesiones": ses,
        "previa": anteriores[-1] if anteriores else None,
    }


def marcas_eval_p1(items, sesiones: list[tuple[date, dict]], d: date,
                   es_sesion: bool) -> list[str]:
    """Qué pasa con la evaluación en la semana que arranca el lunes `d`.

    La columna «Evaluación» de pregrado marca el ítem que cierra ESE día; en Proyecto I
    eso dejaría la columna vacía en las 15 filas. Aquí se marca lo que sí ocurre: qué
    ventana abre ese lunes, qué ventana cierra durante esa semana (en domingo) y si esa
    es la última clase antes de un cierre.
    """
    fin_semana = d + timedelta(days=6)
    marcas: list[str] = []
    for e in items:
        if e.apertura == d:
            marcas.append(
                f"**Abre {e.code}** ({e.tipo_label.lower()} · {e.weight_pct} · corte {e.corte})"
            )
    for e in items:
        if not (d <= e.entrega <= fin_semana):
            continue
        u = ultima_sincronica(sesiones, e.entrega)
        cola = " — esta es la última clase antes del cierre" if (es_sesion and u and u[0] == d) else ""
        marcas.append(
            f"**Cierra {e.code}** {DIAS[e.entrega.weekday()]} "
            f"{e.entrega.strftime('%d/%m')} ({e.tipo_label.lower()} · {e.weight_pct}){cola}"
        )
    if es_sesion:
        for e in items:
            if d <= e.entrega <= fin_semana:
                continue  # ya lo dice la marca «Cierra …»
            u = ultima_sincronica(sesiones, e.entrega)
            if u and u[0] == d:
                marcas.append(
                    f"**Última sincrónica antes del cierre de {e.code}** "
                    f"({DIAS[e.entrega.weekday()]} {e.entrega.strftime('%d/%m')})"
                )
    # Entre el cierre del ítem y el límite de nota el Docente está calificando: la clase
    # de esa franja es la de la retroalimentación (S03 y S04 con el Quiz, S11 con la
    # ACA FINAL). Sin esta marca la fila quedaría en «—» y parecería una semana muerta.
    for e in items:
        if not e.nota_docente:
            continue
        if d == e.nota_docente:
            marcas.append(f"**Hoy vence el límite de nota de {e.code}**")
        elif es_sesion and e.entrega < d < e.nota_docente:
            marcas.append(
                f"**Calificando {e.code}** (límite de nota "
                f"{e.nota_docente.strftime('%d/%m')}): sesión de retroalimentación"
            )
    return marcas


def tabla_eval_p1(course_key: str, sesiones: list[tuple[date, dict]]) -> list[str]:
    """Bloque «Evaluación» de Proyecto I: ventanas oficiales de Coordinación.

    Todo sale de `fechas_entrega_aca.VENTANAS['proyecto1']` y de `ACA_COMPONENTES`
    (nombre exacto del ítem en el aula, tipo de actividad, peso, corte). Aquí no se
    escribe a mano ninguna fecha, ningún peso y ningún nombre de ítem.
    """
    items = entregas_para_grupo(course_key)
    cuest = [e for e in items if e.kind == "cuestionario" and not e.es_instrumento_cierre]
    tareas = [e for e in items if e.es_documento]
    lines = [
        "## Evaluación — ventanas OFICIALES de Coordinación",
        "",
        f"**Régimen:** {REGIMEN_P1}. Fuente de las ventanas: "
        "`config/cursos/fechas_entrega_aca.py` → `VENTANAS[\"proyecto1\"]`; fuente de los "
        "nombres, tipos y pesos: libro de calificaciones del aula en CDigital "
        "(auditoría 2026-08-10).",
        "",
        "| Ítem en el aula (CDigital) | Tipo | Corte (peso) | Peso del ítem | Apertura | "
        "Cierre | Límite de nota | Última sincrónica antes del cierre |",
        "| :--- | :--- | :---: | ---: | :--- | :--- | :--- | :--- |",
    ]
    for e in items:
        lines.append(
            f"| **{e.code}** | {e.tipo_label} | {e.corte} "
            f"({fmt_peso(peso_corte(course_key, e.corte))}) | **{e.weight_pct}** | "
            f"{DIAS[e.apertura.weekday()]} {fmt_entrega(e.apertura, largo=False)} | "
            f"{DIAS[e.entrega.weekday()]} {fmt_entrega(e.entrega, largo=False)} | "
            f"{fmt_entrega(e.nota_docente, largo=False) if e.nota_docente else '—'} | "
            f"{sesion_ref(ultima_sincronica(sesiones, e.entrega))} |"
        )
    en_dia_clase = [e for e in items if e.entrega.weekday() == COURSE_P1["weekday"]]
    lines += [
        "",
        f"**Cortes:** {desglose_corte_texto(course_key)}.",
        "",
    ]
    if not en_dia_clase:
        dias_cierre = sorted({DIAS_LARGO[e.entrega.weekday()] for e in items})
        lines.append(
            "> **Ningún ítem cierra en día de clase:** las ventanas de Coordinación "
            f"cierran en **{' / '.join(dias_cierre)}** y el día de clase es "
            f"**{DIAS_LARGO[COURSE_P1['weekday']]}**. Por eso la última columna marca la "
            "última sesión sincrónica útil antes de cada cierre, en vez de «la sesión en "
            "que cae»."
        )
    lines.append(
        "> A diferencia de pregrado, Proyecto I **no tiene quices ni parciales "
        "adicionales**: en todo el periodo hay "
        f"**{plural(len(cuest), 'cuestionario evaluativo', 'cuestionarios evaluativos')}** "
        f"({', '.join(e.code for e in cuest) or '—'}) y "
        f"**{plural(len(tareas), 'tarea', 'tareas')}** "
        f"({', '.join(e.code for e in tareas) or '—'}); el resto del corte 3 son los "
        "instrumentos individuales de cierre (**autoevaluación** cuestionario, "
        "**coevaluación** foro)."
    )
    previas = [e for e in items if e.apertura < COURSE_P1["inicio"]]
    if previas:
        lines.append(
            "> **Ventanas que abren antes del inicio del periodo:** "
            + " · ".join(
                f"**{e.code}** ({fmt_entrega(e.apertura, largo=False)})" for e in previas
            )
            + f", contra un inicio de clases el "
            f"{COURSE_P1['inicio'].strftime('%d/%m/%Y')}. Son las fechas de Coordinación; "
            "en la práctica el ítem se presenta y se trabaja desde la primera clase."
        )
    lines.append(f"> {items[0].regla}")
    lines.append(
        "> **No te guíes por los recordatorios de Moodle** para el cierre: pueden estar "
        "desactualizados. La fecha válida es la de Coordinación (columna «Límite de nota» "
        "y cierre del periodo en «Fechas institucionales»)."
    )
    return lines


def tabla_cobertura_p1(course_key: str, lunes: list[date],
                       sesiones: list[tuple[date, dict]]) -> list[str]:
    """Cuántas clases quedan realmente dentro de la ventana de cada ítem.

    Es la sección que en la versión a mano era la «🔴 ALERTA PENDIENTE: ACA 3 solo tiene
    2 lunes». Ahora se calcula: si mañana cambia un festivo o una ventana, la alerta se
    recalcula sola en vez de quedarse afirmando algo que ya no es cierto.
    """
    items = entregas_para_grupo(course_key)
    lines = [
        "## Cuántas clases caben dentro de cada ventana",
        "",
        "Cruce de las ventanas de Coordinación con los festivos colombianos y con el "
        f"catálogo de sesiones. **Día de clase: {DIAS_LARGO[COURSE_P1['weekday']]}.** La "
        "**sesión de encuadre no dicta tema**, así que no cuenta como clase de contenido "
        "para el ítem cuya ventana la incluye.",
        "",
        "| Ítem | Ventana | Días de clase en la ventana (dentro del periodo) | "
        "Perdidos por festivo | Sesiones sincrónicas | Cuáles |",
        "| :--- | :--- | :---: | :--- | :---: | :--- |",
    ]
    alertas: list[str] = []
    for e in items:
        c = cobertura_item(e, lunes, sesiones)
        fest = " · ".join(
            f"{d.strftime('%d/%m')} ({FESTIVOS_2026[d]})" for d in c["festivos"]
        ) or "—"
        cuales = " · ".join(
            f"S{int(s['n']):02d} ({d.strftime('%d/%m')}"
            + (", encuadre — no dicta tema)" if s.get("presentacion") else ")")
            for d, s in c["sesiones"]
        ) or "—"
        # La sesión de encuadre no dicta tema (regla de los 5 cursos), así que no cuenta
        # como clase de contenido para el ítem cuya ventana la incluye.
        contenido = [t for t in c["sesiones"] if not t[1].get("presentacion")]
        marca = " ⚠️" if (c["festivos"] and len(contenido) <= 2
                          and not e.es_instrumento_cierre) else ""
        lines.append(
            f"| **{e.code}**{marca} | {e.apertura.strftime('%d/%m')} – "
            f"{e.entrega.strftime('%d/%m')} | {len(c['lunes'])} | {fest} | "
            f"**{len(c['sesiones'])}** | {cuales} |"
        )
        if marca:
            encuadre = (
                " (la sesión de encuadre que cae en su ventana no dicta tema)"
                if len(contenido) != len(c["sesiones"]) else ""
            )
            previa = (
                " Adelanta contenido en la sesión anterior a la ventana "
                f"(**S{int(c['previa'][1]['n']):02d}**, {c['previa'][0].strftime('%d/%m')})."
                if c["previa"] else ""
            )
            refuerzo = (
                " Refuerza con **tutorías por grupo** en esas semanas."
                if course_key in CURSOS_CON_TUTORIAS_POR_GRUPO else ""
            )
            alertas.append(
                f"> ⚠️ **{e.code}** ({e.weight_pct} · corte {e.corte}) se juega en solo "
                f"**{plural(len(contenido), 'sesión de contenido', 'sesiones de contenido')}"
                f"**{encuadre}: de los "
                f"{plural(len(c['lunes']), 'día de clase', 'días de clase')} de su ventana, "
                f"{plural(len(c['festivos']), 'cae', 'caen')} en festivo — {fest}."
                f"{previa}{refuerzo} No dejes ese tramo dependiendo solo de las sesiones "
                "sincrónicas."
            )
    if alertas:
        lines += ["", *alertas]
    return lines


def tabla_festivos_p1(course_key: str, lunes: list[date]) -> list[str]:
    """Los días de clase que caen en festivo y qué ventana tocan."""
    items = entregas_para_grupo(course_key)
    lines = [
        f"## Días de clase SIN encuentro (festivos colombianos {COURSE_P1['inicio'].year})",
        "",
        "| Fecha | Festivo | Qué toca de la evaluación |",
        "| :--- | :--- | :--- |",
    ]
    for d in lunes:
        if not is_festivo(d):
            continue
        partes = []
        for e in items:
            if e.apertura == d:
                partes.append(f"**abre {e.code}**")
            elif e.apertura < d <= e.entrega:
                partes.append(f"ventana de **{e.code}**")
        for e in items:
            if e.nota_docente == d:
                partes.append(f"límite de nota de **{e.code}**")
        lines.append(
            f"| {d.strftime('%d/%m/%Y')} ({DIAS[d.weekday()]}) | "
            f"{nombre_festivo(d, con_traslado=True)} | {' · '.join(partes) or '—'} |"
        )
    lines += ["", f"> {REGLA_FESTIVO_AFI}"]
    return lines


def write_calendario_proyecto1(course: dict, course_dir: Path) -> None:
    """«Calendario de clases (oficial).md» de Proyecto I — 100% generado.

    Hasta 2026-08-11 este archivo era el único de los cinco cursos que se mantenía a
    mano, y por eso conservaba títulos de sesión viejos y la nomenclatura muerta
    ACA 1 / ACA 2 / ACA 3 (que hacía leer «la ACA 1 cerró el 30/08» cuando lo que cierra
    el 30/08 es el **Quiz**). Todo lo que aquí se escribe sale del modelo:
      · oferta, horario y fechas institucionales → carga_academica_2026.json
      · sesiones, temas y unidades ESP329        → sesiones_cun.py
      · ítems, tipos, pesos y ventanas           → fechas_entrega_aca.py
    """
    key = course["key"]
    sesiones = sesiones_catalogo(key)
    lunes = lunes_del_periodo(course)
    items = entregas_para_grupo(key)
    syllabus = SESIONES_COURSES.get(key, {})
    meta = course["group_meta"][course["groups"][0]]
    fin = max(m["cierre"] for m in course["group_meta"].values())
    festivos = [d for d in lunes if is_festivo(d)]
    dia_clase = DIAS_LARGO[course["weekday"]]
    # `hora_ics` es HHMMSS 24 h (misma fuente que el ICS): así la comprobación contra la
    # franja AFI usa el mismo dato que se importa a Calendar, no un texto paralelo.
    hhmm_ini, hhmm_fin = (f"{h[:2]}:{h[2:4]}" for h in course["hora_ics"])

    lines = [
        f"# Calendario de clases (oficial) — {course['titulo_largo']}",
        f"Plantilla del curso · Horario: **{course['horario_txt']}** · "
        f"franja AFI oficial **{FRANJA_AFI}** (duración exigida {DURACION_AFI})",
        f"Grupos de este periodo: **{', '.join(course['groups'])}** · "
        f"Periodo **{meta['periodo']}** · Código **{course['codigo']}**",
        f"Docente: **{DOCENTE}** · {DOCENTE_CORREO}",
        "",
        "> **Archivo generado — no editar a mano.** Regenerar: "
        "`python config/slides/build_pregrado_cursos.py --calendar-only` "
        "(o `--proyecto1-only`). "
        "Fuentes: oferta y horario en `config/cursos/carga_academica_2026.json`; "
        "sesiones y temas en `config/cursos/sesiones_cun.py`; ítems, tipos, pesos y "
        "ventanas en `config/cursos/fechas_entrega_aca.py`.",
        f"> **Horario ✓ instructivo AFI:** el encuentro ({hhmm_ini}–{hhmm_fin} h) cae "
        f"dentro de la franja oficial **{FRANJA_AFI}** y cumple la duración exigida "
        f"({DURACION_AFI}); coincide además con la sugerencia del propio portal "
        f"({SUGERENCIA_PORTAL_AFI}).",
        f"> **Regla de festivo (AFI — distinta de pregrado):** {REGLA_FESTIVO_AFI} "
        "Por eso el catálogo **no numera** los días de clase festivos: aparecen en la "
        "tabla de sesiones sin número, y **no** generan evento en el CSV/ICS.",
        "> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` (fuente: "
        "`sesiones_cun.py`; el periodo va delante porque el nombre del evento es la clave de "
        "búsqueda en la carpeta de grabaciones). El CSV/ICS del grupo —con invitados, coanfitrión y el enlace "
        "único de Meet de la serie— lo genera "
        "`python config/slides/build_calendar_proyecto1_54es4.py`, **no** este build.",
        f"> **CDigital (aula del curso):** {cdigital_url(key)} · "
        f"**Google Meet (mismo enlace toda la serie):** {_meet(key, course['titulo_corto'])}",
    ]
    if syllabus.get("nota_syllabus"):
        lines.append(f"> **Nota Syllabus:** {syllabus['nota_syllabus']}")
    lines.append("")

    # ── El encuentro de 2 h: contenido + tutoría ────────────────────────────
    dur = syllabus.get("duracion_min")
    cont = syllabus.get("contenido_min")
    if dur and cont and dur > cont:
        lines += [
            f"## El encuentro de {dur // 60} horas: ~{cont} min de contenido + "
            f"{dur - cont} min de tutoría",
            "",
            f"- **Contenido nuevo por sesión: ~{cont} min.** El guion docente de cada "
            "sesión trae solo ese bloque (teoría + modelación); no hay que preparar "
            f"{dur} min de material.",
            f"- **Los otros {dur - cont} min son tutoría/taller en vivo** con los equipos: "
            "revisión de avances y dudas puntuales. Es acompañamiento flexible, no "
            "material nuevo.",
        ]
        if key in CURSOS_CON_TUTORIAS_POR_GRUPO:
            lines.append(f"- {MSG_TUTORIAS_POR_GRUPO}")
            lines.append(
                f"- **Asistencia a tutorías (formulario del estudiante):** {LINK_TUTORIAS}"
            )
        lines.append("")

    # ── Evaluación (ventanas oficiales) ─────────────────────────────────────
    lines += tabla_eval_p1(key, sesiones)
    lines.append("")

    # ── Cobertura de cada ventana + alertas calculadas ──────────────────────
    lines += tabla_cobertura_p1(key, lunes, sesiones)
    lines.append("")

    # ── Festivos ────────────────────────────────────────────────────────────
    lines += tabla_festivos_p1(key, lunes)
    lines.append("")

    # ── Sesiones ────────────────────────────────────────────────────────────
    temas = {d: s for d, s in sesiones}
    lines += [
        f"## Las sesiones de clase ({dia_clase}) — alineadas a {course['codigo']}",
        "",
        f"**Fuente:** {syllabus.get('fuente', '—')}",
        "",
        f"**Sesión** = numeración del catálogo, la que usan el guion, el `.pptx` y el "
        f"Subject de Calendar. Las filas sin número son días de clase festivos: **no hay "
        f"encuentro y no hay evento en Calendar**. La columna **Evaluación** dice qué "
        f"ventana abre ese {dia_clase}, cuál cierra durante esa semana (en domingo) y si "
        f"esa es la última clase antes de un cierre.",
        "",
        "| Sesión | Fecha | Tipo | Bloque | Unidad "
        f"{course['codigo']} | Contenido | Evaluación (aula CDigital) |",
        "|---|---|---|---|---|---|---|",
    ]
    for d in lunes:
        ses = temas.get(d)
        fecha_txt = f"{d.strftime('%d/%m/%Y')} ({DIAS[d.weekday()]})"
        if ses:
            n_ses = f"**{int(ses['n']):02d}**"
            tipo = "Sincrónica"
            bloque = ses.get("bloque") or "—"
            unidad = ses.get("unidad_esp329") or "—"
            contenido = ses.get("detalle") or ses["titulo"]
        elif is_festivo(d):
            n_ses = "—"
            tipo = f"Sin sincrónico ({FESTIVOS_2026[d]})"
            bloque = unidad = "—"
            contenido = (
                "**No hay encuentro** (festivo). Clase **pregrabada** en CDigital / "
                "trabajo autónomo; el avance del anteproyecto no se detiene."
            )
        else:
            n_ses = "—"
            tipo = "Sin sesión en el catálogo"
            bloque = unidad = "—"
            contenido = "Revisar `sesiones_cun.py`: este día de clase no tiene sesión."
        ev = " · ".join(marcas_eval_p1(items, sesiones, d, bool(ses))) or "—"
        lines.append(
            f"| {n_ses} | {fecha_txt} | {tipo} | {bloque} | {unidad} | {contenido} | {ev} |"
        )
        if ses and ses.get("unidad_diferida"):
            lines.append(
                f"| — | (misma semana) | ⚠️ Lectura autónoma | {ses.get('bloque') or '—'} "
                f"| — | {ses['unidad_diferida']} | — |"
            )

    lines += [
        "",
        f"> {NOTA_EQUIPOS_AFI}",
        "",
        f"**Total: {len(sesiones)} sesiones sincrónicas** = los {len(sesiones)} días de "
        f"clase no festivos del periodo ({sesiones[0][0].strftime('%d/%m')} → "
        f"{sesiones[-1][0].strftime('%d/%m')}). Entre "
        f"{course['inicio'].strftime('%d/%m/%Y')} y {fin.strftime('%d/%m/%Y')} hay "
        f"**{len(lunes)}** días de clase; menos los **{len(festivos)}** festivos "
        f"({', '.join(d.strftime('%d/%m') for d in festivos)}) quedan "
        f"**{len(lunes) - len(festivos)}**. No sobra ni falta ninguno.",
        "",
        "## Fechas institucionales",
        f"- Inicio del periodo: **{meta['inicio'].strftime('%d/%m/%Y')}**",
        f"- Fecha máxima de recepción de trabajos (informativa, portal): "
        f"**{meta['recepcion'].strftime('%d/%m/%Y')}**",
        f"- **Cierre oficial y registro de notas: {meta['cierre'].strftime('%d/%m/%Y')}** "
        f"({DIAS_LARGO[meta['cierre'].weekday()]}) — única fecha válida",
        f"- Última sesión sincrónica del periodo: "
        f"**{sesiones[-1][0].strftime('%d/%m/%Y')}** (S{int(sesiones[-1][1]['n']):02d})",
    ]
    if course.get("creditos"):
        lines.append(f"- Créditos / horas: {course['creditos']}")
    lines += [
        f"- Informe Final de Curso: dentro de los **{PLAZO_INFORME_FINAL} siguientes** "
        "al cierre.",
        "",
        "## Registro obligatorio de cada sesión y tutoría (dentro de 24 h)",
        "Formulario exclusivo del Docente titular (**NO compartir con estudiantes**): "
        f"**Registro de Sesiones Sincrónicas y Tutorías Especialización:** "
        f"{LINK_REGISTRO_DOCENTE_AFI}",
        "",
        "## Ver también",
        "- `Manual del Docente - PROYECTO I.md` (raíz del curso): guía completa — cómo "
        "preparar la sesión, qué le entregas a la universidad, qué te entregan los "
        "estudiantes.",
        f"- `2026/{course['groups'][0]}/`: roster, CSV/ICS de encuentros con invitados, "
        "Apps Script, hitos docentes y correo de bienvenida.",
        "- Enunciados e instructivos para el estudiante: `Clases/Recursos/ACAs/` "
        "(`python config/slides/build_acas_estudiantes.py proyecto1`).",
    ]
    (course_dir / "Calendario de clases (oficial).md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"OK CAL {key} {course['groups'][0]}: {len(sesiones)} sesiones / "
        f"{len(lunes)} días de clase -> {course_dir}"
    )


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
            "Regla: si la fecha de clase cae en festivo colombiano, la sesión se cursa como clase\n"
            "autónoma: el material queda en la carpeta de esa sesión en el Drive de clases\n"
            "(Clases/Sesion NN - …/) y la entrega y la nota siguen en CDigital.\n"
            "Fuente de grupos/bloque: config/cursos/carga_academica_2026.json\n"
            "Ver calendario e importación a Calendar en esta carpeta.\n"
        )
        path.write_text(text, encoding="utf-8")


def write_all_calendars():
    """CSV/ICS de encuentros + calendarios oficiales md (sin PPTX).

    Incluye el «Calendario de clases (oficial)» de Proyecto I. De ese curso se genera
    **solo** ese archivo: su CSV/ICS con invitados es de `build_calendar_proyecto1_54es4.py`.
    """
    p1_dir = _course_dir(P1_KEY)
    ensure_dirs(p1_dir)
    write_calendario_proyecto1(COURSE_P1, p1_dir)

    for key, course in COURSES.items():
        course_dir = ROOT / course["folder"]
        ensure_dirs(course_dir)
        write_calendario_curso(key, course, course_dir)

        # TG3: los tres grupos son UNA sola serie (mismo horario, misma sala de Meet), así
        # que sus encuentros viven en `_combinado_todos/` y punto. Por grupo se escribe solo
        # el markdown de referencia —cada uno tiene su propio cierre y su propio libro de
        # calificaciones—, nunca un .ics: importar los tres crearía los eventos por
        # triplicado. Hasta el 2026-08-11 este build emitía además `_combinado_54466-54467/`
        # y `_combinado_todos_hasta_15-11/`, restos de planes anteriores a la decisión del
        # docente; eran dos juegos más de los mismos encuentros y se retiraron.
        for g, meta in course["group_meta"].items():
            write_calendar_files(
                key, course, [g], course_dir / "2026" / g, meta["cierre"],
                con_ics=(key != "tg3"),
                # En TG3 el evento real lleva los tres códigos: es una sola serie.
                grupos_evento=(list(course["group_meta"].keys()) if key == "tg3" else None),
            )

        if key == "tg3":
            write_calendar_files(
                key, course, list(course["group_meta"].keys()),
                course_dir / "2026" / "_combinado_todos",
                max(m["cierre"] for m in course["group_meta"].values()),
            )
            _retirar_combinados_obsoletos(course_dir / "2026")


def main(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(
        description="Presentaciones + calendarios Pregrado CUN "
                    "(+ calendario oficial de Proyecto I)"
    )
    parser.add_argument(
        "--calendar-only",
        action="store_true",
        help="Solo regenera CSV/ICS de encuentros y calendarios md (no PPTX ni Informacion.txt)",
    )
    parser.add_argument(
        "--proyecto1-only",
        action="store_true",
        help="Solo regenera «Calendario de clases (oficial).md» de Proyecto I",
    )
    args = parser.parse_args(argv)

    if args.proyecto1_only:
        p1_dir = _course_dir(P1_KEY)
        ensure_dirs(p1_dir)
        write_calendario_proyecto1(COURSE_P1, p1_dir)
        print("DONE (proyecto1-only)")
        return

    if args.calendar_only:
        write_all_calendars()
        print("DONE (calendar-only)")
        return

    # Los PPTX y el Informacion.txt de Proyecto I NO se generan aquí:
    # build_cun_proyecto1.py y build_calendar_proyecto1_54es4.py son sus dueños.
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
