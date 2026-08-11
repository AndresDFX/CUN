# -*- coding: utf-8 -*-
"""Genera material por SESIÓN numerada: PPTX estudiante + guion docente (.md únicamente).

Convención (obligatoria):
  Clases/
    Presentacion del Curso - ….pptx
    Sesion 01 - <Nombre del tema>/
      Presentacion.pptx          ← SOLO el tema de esa clase (sin fechas ni mapa del curso)
    Sesion 02 - <Nombre del tema>/
      ...
  Guiones/
    Sesion 01 - <Nombre del tema>.md   ← solo Markdown (interno docente; sin .docx)
    Capturas/

Contenido RICO por sesión (opcional, recomendado):
  - `config/slides/content/cun_<curso>_s<NN>.json` (curso ∈ proyecto1|investigacion|
    creatividad|tg2|tg3 · NN con cero: s03). Lista de bloques bullets/table/boxes —
    esquema y render en `cun_contenido_sesion.py`; validar con:
        python cun_contenido_sesion.py <curso> <NN>
  - Si el JSON existe: la deck = portada + bloques del JSON + cierre.
  - Si NO existe: deck genérica de 7 slides de siempre (fallback intacto).
  - Sesión 01 (encuadre): el contenido rico se intercala DESPUÉS de la slide
    «CÓMO SE EVALÚA» y ANTES de «PARA LA PRÓXIMA SESIÓN» (ver `S01_CONTENIDO_TRAS`).

Estándar PPTX de sesión:
  - Número de sesión discreto (p. ej. «Sesión 01») + tema puntual.
  - SIN fechas de periodo/referencia, SIN mapa completo del curso, SIN bio del docente.
  - Logística de semestre (fechas, grupos, evaluación) → Presentación del Curso.

Estándar guion:
  - Tema de la sesión, fundamento, plan minuto a minuto, práctica, entregable de ESA clase.
  - Referencia slides de ESA Presentacion.pptx (no el temario entero).
  - Solo formato `.md` (no se genera .docx de guiones).
  - Proyecto I (AFI): cierre con checklist post-clase — registro docente AFI (<24h)
    + recordatorio formulario de asistencia del estudiante en tutoría.
    URLs desde config/universidades/cun.json → links_afi (vía sesiones_cun).
  - Guiones ricos (minuto a minuto): regeneradores propios — no sobrescribir aquí:
      proyecto1 → Especializacion/Proyecto I/Guiones/_regen_guiones_proyecto1.py
      creatividad → Pregrado/.../Guiones/_regen_guiones_creatividad.py
      investigacion/tg2/tg3 → config/slides/_regen_guiones_pregrado.py

Uso:
  python build_sesion_material.py proyecto1 1
  python build_sesion_material.py investigacion 1
  python build_sesion_material.py all 1
  python build_sesion_material.py proyecto1 all
  python build_sesion_material.py all all
  python build_sesion_material.py proyecto1 all --guion-only   # solo .md (sin PPTX)
"""
from __future__ import annotations
import os, sys, re, textwrap, shutil

# Consola de Windows en cp1252: sin esto, imprimir la ayuda (que trae «←») aborta.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))
from cun_slides_engine import *
import cun_contenido_sesion as contenido
from sesiones_cun import (
    COURSES,
    DOCENTE,
    DOCENTE_CORREO,
    DOCENTE_CREDS,
    LINK_TUTORIAS,
    MSG_TUTORIAS_POR_GRUPO,
    LINK_REGISTRO_DOCENTE_AFI,
    meet_url,
)
from guion_slides import deck_path, tabla_slides_md, titulos_pptx  # noqa: E402
from fechas_entrega_aca import (  # noqa: E402
    entregas_para_grupo,
    fmt_peso,
    peso_corte,
)

SLIDES_DIR = os.path.dirname(os.path.abspath(__file__))

# Guiones minuto-a-minuto viven en regeneradores propios (no sobrescribir aquí).
RICH_GUION_COURSES = {"creatividad", "proyecto1", "investigacion", "tg2", "tg3"}

# Contenido RICO por sesión: config/slides/content/cun_<curso>_s<NN>.json
# (esquema y render → cun_contenido_sesion.py). Si el JSON no existe, la deck
# se genera exactamente igual que antes (fallback genérico intacto).
# En la Sesión 01 (encuadre) el contenido rico se inserta DESPUÉS de la slide
# «CÓMO SE EVALÚA» y ANTES de «PARA LA PRÓXIMA SESIÓN»; este flag elige el punto exacto:
#   "acas"     → justo después de la tabla de evaluación (por defecto; valor histórico)
#   "acuerdos" → después de ACUERDOS DE TRABAJO (cierra el encuadre y luego el tema)
S01_CONTENIDO_TRAS = "acas"


def topic_filename(titulo: str, max_len: int = 70) -> str:
    """Nombre limpio a partir del tema (sin número de sesión)."""
    s = titulo.strip()
    s = re.sub(r'[<>:"/\\|?*]', "", s)
    s = re.sub(r"\s+", " ", s).strip(" .")
    return (s[:max_len] or "Tema").rstrip()


def session_folder_name(n: int, titulo: str) -> str:
    return f"Sesion {n:02d} - {topic_filename(titulo)}"


# --- Fundamentos teóricos ricos para el primer tema de cada curso ---
FUNDAMENTOS_S1 = {
    "proyecto1": textwrap.dedent("""\
        ### 1. Qué es (y qué NO es) un anteproyecto
        Un **anteproyecto de investigación** es el documento que demuestra que una pregunta
        de investigación es **viable, coherente y metodológicamente defendible** antes de
        recolectar datos. En la CUN (AFI / Especializaciones), Proyecto I culmina en ese
        anteproyecto; Proyecto II es la ejecución (aplicación de instrumentos, análisis, etc.).

        | Concepto | Proyecto I | Proyecto II |
        |---|---|---|
        | Producto | Anteproyecto aprobado | Investigación ejecutada / resultados |
        | Instrumentos | Solo **propuestos** | Aplicados |
        | Campo / encuestados | No | Sí (con aval) |
        | Rol docente | Garante metodológico | Acompañamiento de ejecución |

        **Error frecuente:** querer “ya encuestar” en la semana 2. Respuesta del docente:
        “En Proyecto I diseñamos; en Proyecto II aplicamos, tras el aval.”

        ### 2. El docente como garante metodológico
        No eres el experto temático de cada IA aplicada que proponga el equipo. Tu rol es
        verificar coherencia pregunta–objetivos–marco–método, viabilidad y formato APA CUN.
        Si el tema no entra en las líneas oficiales de IA, orientas a reformularlo.

        ### 3. Estructura del encuentro de 2 horas
        - **60 min contenido:** concepto + modelación + dudas comunes.
        - **60 min tutoría:** trabajo por equipos; el estudiante debe registrar asistencia en
          {link}. {msg}
        """).format(link=LINK_TUTORIAS, msg=MSG_TUTORIAS_POR_GRUPO),

    "investigacion": textwrap.dedent("""\
        ### 1. Método científico (versión operativa para Ingeniería)
        El método científico es un ciclo: **problema → datos → procesamiento → interpretación**.
        En esta asignatura el producto esperado es un **artículo / proyecto de investigación**
        enmarcado en las 6 líneas de Ingeniería (IoT, Big Data, IA, cloud/FinTech, apps, telemática).

        | Etapa | Pregunta guía | Entregable típico del estudiante |
        |---|---|---|
        | Problema | ¿Qué no funciona / qué no sabemos? | Planteamiento + pregunta |
        | Datos | ¿Con qué evidencia? | Fuentes / bases CUN |
        | Procesamiento | ¿Cómo se organiza? | ZoteroBib + Google Docs + matriz de lectura |
        | Interpretación | ¿Qué significa? | Discusión / avance de artículo |

        ### 2. Acuerdo pedagógico del primer encuentro
        Presenta competencias, evaluación por cortes (30/30/40 Art. 52) y el producto final
        desde el día 1. Evita que el artículo “aparezca” al final como sorpresa.
        """),

    "creatividad": textwrap.dedent("""\
        ### 1. Creatividad vs. innovación (para no confundirlos en clase)
        **Creatividad** = generar ideas nuevas. **Innovación** = llevar una idea a cabo con
        valor (producto, proceso, organización, marketing o social). El trabajo final del curso
        es una **Propuesta de Innovación**, anunciada desde el primer encuentro.

        | Tipo (Manual de Oslo) | Ejemplo en Ingeniería |
        |---|---|
        | Producto | Nuevo módulo/software con valor de uso |
        | Proceso | Automatizar un flujo de pruebas |
        | Organización | Cambiar roles/flujo de un equipo Dev |
        | Marketing | Nuevo canal de adopción de una app |
        | Social | Solución con impacto comunitario |

        ### 2. Por qué anunciar el trabajo final el día 1
        Cada unidad (IE, Design Thinking, vigilancia, etc.) debe alimentar la misma propuesta.
        Si no lo anuncias, el estudiante trata cada taller como isla.
        """),

    "tg2": textwrap.dedent("""\
        ### 1. Lugar de TG2 en la ruta de opción de grado
        ⚠️ **Sin Syllabus SIAC cargado.** Usa este marco orientativo y confírmalo en CDigital.

        Trabajo de Grado 2 es la fase de **avance consolidado** del documento/proyecto antes
        de la culminación y sustentación (TG3). El estudiante no “empieza de cero”: retoma
        semestres previos y deja un avance defendible.

        | Fase | Enfoque típico |
        |---|---|
        | TG2 | Problema, marco, método propuesto, avance integrado |
        | TG3 | Artículo completo, póster, antiplagio, sustentación, repositorio |

        ### 2. Tu rol en el primer encuentro
        Diagnosticar el estado real del proyecto de cada estudiante/equipo y fijar el
        acuerdo pedagógico del encuentro (festivo = **clase autónoma**: la actividad
        queda en la carpeta de esa sesión del **Drive de clases**, y lo que se entregue
        sigue yendo a CDigital).
        """),

    "tg3": textwrap.dedent("""\
        ### 1. Qué exige el Syllabus 94532
        Culminar la opción de grado con un **artículo resultado de investigación**
        (revisión rigurosa; el Syllabus indica ≥50 referencias y extensión no inferior a
        4.000 palabras) + **sustentación ante jurados** + carga a repositorio.

        | Entregable | Momento del Syllabus |
        |---|---|
        | Artículo completo | Unidades 4–11 |
        | Póster + antiplagio | Unidad 12 |
        | Sustentación | Unidad 13 |
        | Repositorio | Unidad 14 |

        ### 2. Primer encuentro: casos de éxito y acuerdo
        Modela con casos de investigación/obra-creación qué se espera al final.
        Deja claros el producto de hoy y el hilo hacia artículo + sustentación.
        """),
}


def _paths(course, ses):
    root = course["folder"]
    label = session_folder_name(ses["n"], ses["titulo"])
    ses_dir = os.path.join(root, "Clases", label)
    guiones = os.path.join(root, "Guiones")
    os.makedirs(ses_dir, exist_ok=True)
    os.makedirs(os.path.join(guiones, "Capturas"), exist_ok=True)
    pptx = os.path.join(ses_dir, "Presentacion.pptx")
    md = os.path.join(guiones, f"{label}.md")
    return pptx, md, label, ses_dir


# Qué se le pide al estudiante en el rompehielos de la Presentación del Curso
# (= Sesión 01; no se duplica en la deck de sesión).
ROMPEHIELOS_PROMPTS = {
    "proyecto1": "expectativa del curso + **tema tentativo** de investigación (1 frase)",
    "investigacion": "expectativa del curso + **idea de tema** para el artículo (1 frase)",
    "tg2": "**estado actual** del proyecto (1 frase) + expectativa de TG2",
    "tg3": "**tema del artículo** (1 frase) + expectativa del semestre",
    "creatividad": "expectativa del curso + **tema/problema** de interés",
}

# --- Rompehielos según el TAMAÑO del grupo -----------------------------------------
# La forma del rompehielos NO se elige aquí: la decide `cun_slides_engine` a partir de la
# matrícula real (roster de CDigital) — muro de Padlet hasta ICEBREAKER_MAX_MURO
# estudiantes, formulario de Google + encuestas y Q&A de Meet por encima. De ahí salen
# `usa_padlet()` y `formulario_presentacion_url()`, que este módulo solo consume.
# Hoy: Investigación 53339 = 20 (muro) · Proyecto I 54ES4 = 50 · Creatividad 54408 = 50 ·
# TG2 54448 = 50 · TG3 (54450 + 54466 + 54467) = 112 en una sola serie (formulario).


# Qué hace el estudiante con cada ítem, según su TIPO real de actividad en el aula.
# (auditoría CDigital 2026-08-10: quices y parciales son cuestionarios, la ACA Final
# es una tarea y la coevaluación es un FORO — no se sube archivo).
_QUE_HACES = {
    "auto": "La diligencias tú mismo en el aula (cuestionario individual).",
    "coev": "Participas en el foro valorando el trabajo de tus pares.",
    "cuestionario": "Lo resuelves en CDigital dentro de su ventana. No se sube archivo.",
    "tarea": "Subes el documento (plantilla APA CUN) al espacio de la tarea.",
}


def _evaluacion_rows(course_key):
    """Filas de la slide «CÓMO SE EVALÚA» de la Sesión 01 → ``(rows, note)``.

    Una fila por ítem del **libro de calificaciones del aula**: quices, parciales,
    ACA Final, autoevaluación y coevaluación, con el tipo de actividad y el peso
    REALES. Todo se lee de `config/cursos/fechas_entrega_aca.py` (auditoría CDigital
    2026-08-10): aquí no se escribe ningún peso a mano.

    Reemplaza a la vieja tabla «LAS ACAs», que mostraba tres entregables inexistentes
    (en pregrado el aula tiene una sola ACA Final) y dejaba fuera los quices y
    parciales, que son la mayor parte de la nota (Parcial 1 = 24%).

    Sin fechas: la ventana vive en el enunciado (`Clases/Recursos/ACAs/`) y en la
    Presentación del Curso, para no arrastrar aquí una fecha que quede vieja.
    """
    try:
        items = entregas_para_grupo(course_key)
    except Exception:
        return [], None, None
    rows = []
    for e in items:
        rows.append([
            f"**{e.code}**",
            e.tipo_label,
            f"{e.corte} ({fmt_peso(peso_corte(course_key, e.corte))})",
            f"**{e.weight_pct}**",
            _QUE_HACES.get(e.id) or _QUE_HACES[e.kind],
        ])
    total = fmt_peso(sum(e.weight for e in items))
    docs = [e.code for e in items if e.es_documento]
    docs_txt = " y ".join(", ".join(docs).rsplit(", ", 1)) if docs else "—"
    # `sub` (bajo el título) en vez de nota al pie: con 8 ítems la tabla baja hasta 6,9"
    # y el pie de `table_content` (fijo en 6,65") le quedaría encima.
    sub = (
        f"Evaluación y notas: solo en **CDigital** · los pesos suman **{total}** · "
        "fechas: enunciados y Presentación del Curso"
    )
    note = None
    if len(rows) <= 6:
        note = (
            f"Se **sube** documento únicamente en **{docs_txt}**; los cuestionarios se "
            "**resuelven** en el aula y la **coevaluación es un foro**. Enunciados y "
            "ventanas: `Clases/Recursos/ACAs/`."
        )
    return rows, sub, note


def build_pptx_presentacion(course, ses, pptx):
    """Sesión 01 = ENCUADRE. Presentación del curso, del Docente, de los estudiantes
    (Padlet) y de **cómo se evalúa** (ítems reales del aula). **No se dicta tema** —
    el tema empieza en la Sesión 02.
    """
    n = ses["n"]
    label = f"Sesión {n:02d}"
    key = course["key"]
    set_footer("")
    prs = new_prs()
    course_cover(
        prs,
        f"{label.upper()} — PRESENTACIÓN DEL CURSO",
        course["titulo_largo"],
        [
            f"**{label}** · Sesión de encuadre",
            "**Hoy:** el curso · el Docente · ustedes · cómo se evalúa",
            f"**Asignatura:** {course['titulo']}",
        ],
    )
    # Contenido rico opcional de la Sesión 01 (JSON): se intercala entre el encuadre
    # y «PARA LA PRÓXIMA SESIÓN»; sin JSON, la numeración queda idéntica (2…7).
    bloques = contenido.load(key, n)
    idx = 2
    content_slide(prs, "AGENDA DE HOY", [
        "**El curso:** de qué se trata, cómo trabajamos y qué se llevan al final.",
        "**El Docente:** quién los acompaña y cómo contactarlo.",
        "**Ustedes:** nos presentamos en el tablero colaborativo.",
        "**Cómo se evalúa:** qué ítems tiene el aula, cuánto pesa cada uno y qué se hace con él.",
        "**Acuerdos** de trabajo y el primer encargo autónomo.",
    ], sub="Sesión de encuadre — hoy no vemos tema; el contenido arranca en la Sesión 02.", idx=idx)
    idx += 1
    tutor_slide(prs, "Docente", DOCENTE_CREDS, DOCENTE_CORREO, idx=idx)
    idx += 1
    # Muro o formulario lo decide el motor con la matrícula real: aquí solo se dice de
    # qué curso es y qué se le pide al estudiante además del nombre.
    icebreaker_qr_slide(
        prs, idx=idx, course_key=key,
        pide=ROMPEHIELOS_PROMPTS.get(key, "expectativa + tema de interés"),
    )
    idx += 1
    # CÓMO SE EVALÚA: los ítems REALES del libro de calificaciones del aula (quices,
    # parciales, ACA Final, auto y coevaluación) con su tipo y su peso, leídos del
    # modelo. Antes esta slide se llamaba «LAS ACAs» y listaba tres entregables que el
    # aula no tiene (auditoría CDigital 2026-08-10).
    rows, sub, note = _evaluacion_rows(key)
    if rows:
        table_content(
            prs, "CÓMO SE EVALÚA — LOS ÍTEMS DEL AULA",
            ["Ítem en CDigital", "Tipo", "Corte (peso)", "Peso", "Qué haces con él"], rows,
            sub=sub,
            note=note,
            col_w=[2.0, 1.3, 1.3, 0.9, 6.4], idx=idx, fs_body=11,
        )
    else:
        content_slide(prs, "CÓMO SE EVALÚA — LOS ÍTEMS DEL AULA", [
            "Estructura, tipo de actividad y pesos: **libro de calificaciones del aula**.",
            "Enunciados y fechas: `Clases/Recursos/ACAs/` y la Presentación del Curso.",
        ], idx=idx)
    idx += 1
    if bloques and S01_CONTENIDO_TRAS == "acas":
        idx = contenido.render(prs, bloques, start_idx=idx)
    acuerdos = [
        ("info", "**Entrega oficial: CDigital.** Lo que no esté ahí, no está entregado."),
        ("aclaracion", "Traer el avance **escrito** a cada encuentro: se trabaja sobre lo que ya existe."),
        ("advertencia", "Integridad académica: citar siempre en **APA 7**. El plagio tiene debido proceso."),
    ]
    if key == "proyecto1":
        acuerdos.insert(1, ("aclaracion", MSG_TUTORIAS_POR_GRUPO))
    box_note_slide(prs, "ACUERDOS DE TRABAJO", acuerdos, idx=idx)
    idx += 1
    if bloques and S01_CONTENIDO_TRAS != "acas":
        idx = contenido.render(prs, bloques, start_idx=idx)
    diferida = ses.get("unidad_diferida")
    proximos = [
        "Revisar la **Presentación del Curso** completa (fechas, evaluación, contenido de todas las sesiones).",
        "Abrir los enunciados de `Clases/Recursos/ACAs/`: son la guía escrita de lo que evalúa cada corte.",
    ]
    if diferida:
        proximos.insert(0, f"**Lectura autónoma:** {diferida.split('→')[0].strip()} — la retomamos al abrir la Sesión 02.")
    content_slide(prs, "PARA LA PRÓXIMA SESIÓN", proximos, idx=idx)
    closing_slide(prs, f"Cierre — {label}", [
        "Ya sabemos qué haremos, cómo se evalúa y quién es quién.",
        "**Sesión 02:** arranca el contenido del curso.",
    ], course["titulo"])
    prs.save(pptx)
    return len(prs.slides)


def _cover_sesion(prs, course, ses, label):
    """Portada estándar de deck de sesión (misma para contenido rico y genérico)."""
    titulo = ses["titulo"]
    return course_cover(
        prs,
        f"{label.upper()} — {titulo.upper() if len(titulo) < 45 else titulo}",
        course["titulo_largo"],
        [
            f"**{label}**",
            f"**Tema:** {titulo}",
            f"**Asignatura:** {course['titulo']}",
        ],
    )


def build_pptx(course, ses, pptx):
    """PPTX estudiante: solo tema de la sesión + nº Sesión NN.
    Sin fechas, sin mapa del curso, sin bio/correo del docente.

    Si existe `config/slides/content/cun_<curso>_s<NN>.json`, la deck se arma con ese
    contenido rico (portada + bloques del JSON + cierre). Si no existe, se conserva
    exactamente el deck genérico de 7 slides de siempre.
    """
    if ses.get("presentacion"):
        return build_pptx_presentacion(course, ses, pptx)
    n = ses["n"]
    titulo = ses["titulo"]
    label = f"Sesión {n:02d}"
    set_footer("")

    bloques = contenido.load(course["key"], n)
    if bloques:
        prs = new_prs()
        _cover_sesion(prs, course, ses, label)
        contenido.render(prs, bloques, start_idx=2)
        closing_slide(prs, f"Cierre — {label}", [
            f"{label}: {titulo}",
            "Siguiente encuentro: continúa el hilo del mismo entregable.",
        ], course["titulo"])
        prs.save(pptx)
        return len(prs.slides)

    prs = new_prs()
    _cover_sesion(prs, course, ses, label)
    content_slide(prs, "OBJETIVOS", [
        f"Comprender: **{titulo}**.",
        ses.get("detalle", "Desarrollar la subtemática del Syllabus / Manual."),
        "Aplicar lo visto en un taller / avance concreto del entregable del curso.",
        "Salir con dudas concretas y un avance observable.",
    ], idx=2)
    content_slide(prs, "CONTENIDO CLAVE", [
        f"**Tema:** {titulo}",
        f"**Detalle:** {ses.get('detalle', '')}",
        "Explicación + ejemplo modelado + práctica guiada.",
        "Trabajo autónomo: avance del entregable según la unidad / ACA correspondiente.",
    ], idx=3)
    if course["key"] == "proyecto1":
        box_note_slide(prs, "RECUERDA", [
            ("info", MSG_TUTORIAS_POR_GRUPO),
            ("advertencia", f"Registra tu asistencia a tutorías: {LINK_TUTORIAS}"),
            ("aclaracion", "En Proyecto I los instrumentos se proponen, no se aplican."),
        ], idx=4)
    else:
        box_note_slide(prs, "ENFOQUE DE HOY", [
            ("info", f"Todo el encuentro gira en torno a: **{titulo}**."),
            ("aclaracion", "El avance de hoy alimenta el mismo entregable del curso (no un taller aislado)."),
        ], idx=4)

    next_idx = 5
    # Padlet / Preséntate vive solo en Presentación del Curso (= Sesión 01 de encuadre).
    # No duplicar el rompehielos en esta deck de sesión.

    content_slide(prs, "ACTIVIDAD / TALLER", [
        "Aplica el concepto de hoy a **tu propio proyecto / propuesta / avance**.",
        "**Criterio de éxito:** sales con un borrador o evidencia parcial alineada al tema.",
        "**Entregable:** avance en CDigital / plantilla APA según indique el Docente. "
        "Enunciado ACA completo: `Clases/Recursos/ACAs/` (no duplicar aquí).",
    ], idx=next_idx)
    next_idx += 1
    content_slide(prs, "PARA CONTINUAR", [
        "Completa el avance encargado hoy.",
        "Lleva dudas concretas (el párrafo o sección puntual, no “no entendí nada”).",
        "Revisa la plantilla APA CUN si tu entregable es documental.",
    ], idx=next_idx)
    closing_slide(prs, f"Cierre — {label}", [
        f"{label}: {titulo}",
        "Siguiente encuentro: continúa el hilo del mismo entregable.",
    ], course["titulo"])
    prs.save(pptx)
    return len(prs.slides)


def build_guion_md(course, ses, label: str) -> str:
    """Guion enfocado en ESTA sesión (sin mapa del curso ni logística de semestre)."""
    n = ses["n"]
    dur = course["contenido_min"]
    titulo = ses["titulo"]
    meet = meet_url(course["key"], course["titulo"])
    fund = FUNDAMENTOS_S1.get(course["key"], "") if n == 1 else textwrap.dedent(f"""\
        ### Concepto central
        Desarrolla con profundidad el tema **{titulo}**, tal como aparece en la fuente
        ({course['fuente']}). Explica el *qué*, el *por qué* y el *cómo* con al menos un ejemplo
        del contexto de Ingeniería / IA / innovación según la asignatura.

        | Qué debe dominar el docente antes de clase | Para qué le sirve en el aula |
        |---|---|
        | Definición operativa del tema | Explicarlo en 5 minutos claros |
        | 2–3 errores frecuentes del estudiante | Corregir en tutoría/taller |
        | Criterio de calidad del avance de hoy | Retroalimentar con evidencia |

        ### Errores frecuentes
        1. Quedarse en definiciones sin conectar al entregable del estudiante.
        2. Avanzar contenido nuevo sin verificar el estado del avance previo.
        3. Cerrar la clase sin tarea observable para la siguiente sesión.
        """)

    is_s01_encuadre = n == 1 and course["key"] in ROMPEHIELOS_PROMPTS
    board_prompt = ROMPEHIELOS_PROMPTS.get(course["key"], "expectativa + tema de interés")
    act_slide = 5
    cont_slide = 6
    close_slide = 7

    if course["key"] == "proyecto1":
        plan = f"""
| Fase | Min | Qué dice / hace el docente | Slide |
|---|---|---|---|
| Encuadre | 8 | Bienvenida, objetivos, Meet; recuerda tutorías ({LINK_TUTORIAS}). | 1–2 |
| Exposición | 25 | Explica el tema con diapositivas; modela 1 ejemplo en vivo. | 3–4 |
| Taller | 20 | Equipos aplican el concepto a su anteproyecto; circula y pregunta. | {act_slide} |
| Cierre contenido | 7 | Resume 3 ideas clave + tarea hasta la próxima. | {cont_slide}–{close_slide} |
| Tutoría (2ª hora) | 60 | Revisión por equipo; recuerda formulario estudiante ({LINK_TUTORIAS}). Tras clase: registro docente AFI <24h. | — |
"""
    else:
        plan = f"""
| Fase | Min | Qué dice / hace el docente | Slide |
|---|---|---|---|
| Encuadre | 5 | Objetivos de hoy + puente breve al tema (sin repasar el mapa del curso). | 1–2 |
| Exposición–diálogo | {max(15, dur // 3)} | Desarrolla el tema con ejemplo; pregunta a 2–3 estudiantes. | 3–4 |
| Taller práctico | {max(15, dur // 3)} | Ejercicio aplicado al proyecto/propuesta del estudiante. | {act_slide} |
| Retro + cierre | {max(8, dur // 6)} | Criterio de éxito + tarea concreta para la próxima. | {cont_slide}–{close_slide} |
"""

    warn = f"\n> ⚠️ {course['nota_syllabus']}\n" if course.get("nota_syllabus") else ""
    rel_pptx = f"Clases/{label}/Presentacion.pptx"

    # Tabla del deck REAL si ya existe en disco; si no, la plantilla como último recurso.
    _tabla_real = tabla_slides_md(
        titulos_pptx(deck_path(course["folder"], label)), encabezado=""
    )
    slides_table = (_tabla_real or "").strip() or f"""| Slide | Título | Cuándo |
| :---: | :--- | :--- |
| **1** | Portada — {n:02d} | Apertura |
| **2** | OBJETIVOS | Encuadre |
| **3** | CONTENIDO CLAVE | Exposición |
| **4** | {"RECUERDA" if course["key"] == "proyecto1" else "ENFOQUE DE HOY"} | Anclaje del tema |
| **5** | ACTIVIDAD / TALLER | Consigna práctica |
| **6** | PARA CONTINUAR | Trabajo autónomo |
| **7** | Cierre | Despedida |"""

    board_block = ""
    rompehielos_check = ""
    if is_s01_encuadre and usa_padlet(course["key"]):
        board_block = f"""
### Rompehielos Padlet — en Presentación del Curso (no se repite aquí)
La **Sesión 01 es la de presentación del curso**. El rompehielos “Preséntate” (QR + Padlet) se hace con la **Presentación del Curso** (slide PRESÉNTATE — ROMPEHIELOS), no como un segundo momento en esta deck.
1. Abrir `Clases/Presentacion del Curso - ….pptx` → slide **Preséntate**.
2. URL oficial: **{PADLET_PRESENTACION_URL}**
3. Consigna: post-it con nombre + {board_prompt}.
4. ~7 min; leer 3–4 notas. Luego continuar con **esta** `Presentacion.pptx` de Sesión 01 (fundamentos / taller).

> El muro sigue aquí porque este grupo tiene **20 estudiantes**: 20 notas se leen enteras en pantalla. En los cursos de más de 20 el rompehielos es un **formulario**, no un muro.
"""
        rompehielos_check = (
            f"- [ ] Abrí la **Presentación del Curso** (slide Preséntate / Padlet): {PADLET_PRESENTACION_URL}\n"
        )
    elif is_s01_encuadre:
        _form = formulario_presentacion_url(course["key"])
        # TG3 son 112 en UNA sola serie (54450 + 54466 + 54467): la regla del grupo grande
        # se vuelve tajante, porque una ronda de presentaciones se come la hora entera.
        _nota_tg3 = (
            "\n> **En TG3 (112 estudiantes en una sola serie) NO se presentan todos:** "
            "treinta segundos por persona son casi una hora. Se leen **5 o 6** respuestas "
            "—una por grupo (54450 · 54466 · 54467), dos del estado mayoritario y una que "
            "se pueda conectar con otra— y el resto se ve en la pantalla de resumen. "
            "Ninguna respuesta delicada se lee en público: eso va por mensaje privado.\n"
            if course["key"] == "tg3" else ""
        )
        board_block = f"""
### Rompehielos — formulario del curso (en Presentación del Curso, no se repite aquí)
La **Sesión 01 es la de presentación del curso**. Con este grupo —**más de 20 estudiantes**— el rompehielos **no es un muro**: es un **formulario de Google** que se responde en cuatro minutos, más las **encuestas** y el **Q&A** que ya trae Meet para la parte en vivo. Un muro con 50 notas nadie lo lee entero y el efecto se pierde: la gente escribe y no se siente vista.
1. Abrir `Clases/Presentacion del Curso - ….pptx` → slide **Preséntate**.
2. Enlace del formulario: **{_form}** — se **pega en el chat del Meet**, dos veces: al abrir la fase y otra vez al minuto 3. No dependa del QR: con estos grupos la mitad entra desde el computador.
3. Consigna: nombre + {board_prompt}. **4 minutos**, y el tiempo se dice en voz alta.
4. Mientras responden, lance una **encuesta de Meet** de una sola pregunta cerrada y proyecte el resultado: eso da la foto del grupo sin leer cincuenta respuestas.
5. Cierre leyendo **5 o 6 respuestas** escogidas (variedad, no las cinco primeras que llegaron) y proyectando la pestaña **Respuestas → Resumen** del formulario: ahí quedan todas a la vista.
6. Deje el **Q&A de Meet** abierto todo el encuentro y responda al final las preguntas más votadas.
7. La hoja de respuestas **no se bota**: sirve todo el periodo para sacar ejemplos, armar equipos y ver quién nunca respondió.
{_nota_tg3}"""
        rompehielos_check = (
            f"- [ ] **Formulario Preséntate** probado y el enlace listo para el chat: {_form}\n"
            "- [ ] **Encuesta de Meet** ya redactada (una pregunta) y **Q&A** activado en la sala\n"
            "- [ ] La slide PRESÉNTATE de la Presentación del Curso ya muestra el **formulario** (si le quedó el QR viejo del Padlet, regenere la deck; en clase, el enlace del chat es el que manda)\n"
        )

    post_clase_block = _post_clase_proyecto1() if course["key"] == "proyecto1" else ""

    return f"""### GUIÓN DOCENTE — Sesión {n:02d}: {titulo}

> **Uso:** guion de esta clase. Enfoque: tema, fundamento, minuto a minuto, práctica y entregable de **hoy**.
> Logística de semestre (fechas, grupos, evaluación global) → Presentación del Curso / Manual.
> **Duración bloque de contenido:** ≈ {dur} min.
> **PPTX:** `{rel_pptx}` (referencia solo estas slides).

📌 **De esta sesión**
- **Sesión:** **{n:02d}** · **Tema:** {titulo}
- **Detalle:** {ses.get('detalle', '')}
- **PPTX estudiante:** `{rel_pptx}`
- **Meet (serie del curso):** {meet}
{warn}
🗺️ **Slides de esta presentación** (no es el mapa del curso)

{slides_table}

🎯 **Objetivos**
* Que el estudiante comprenda el alcance del tema **{titulo}**.
* Que produzca un avance observable alineado a este tema (borrador / matriz / sección).
* Que deje claras las dudas para tutoría o el siguiente encuentro.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

{fund}
{board_block}
---

🧭 **Plan de Clase por Fases** (contenido ≈ {dur} min)
{plan}

**Script de apertura (ejemplo):**
> “Buenas tardes. Sesión {n:02d}: *{titulo}*. Al terminar deben salir con un avance
> concreto de su entregable. Si algo no queda claro, anótenlo: lo resolvemos en el taller.”

**Script de cierre (ejemplo):**
> “Tres ideas clave de hoy: (1)… (2)… (3)…. Para continuar: …. Dudas por el canal del curso.”

---

🧩 **Actividad práctica / taller**
1. Aplica el concepto de hoy a **tu propio** proyecto / propuesta / anteproyecto.
2. **Criterio de éxito:** evidencia parcial escrita o diagrama listo para retroalimentar.
3. **Entregable:** avance en CDigital / plantilla APA CUN según corresponda. Ver enunciado ACA en `Clases/Recursos/ACAs/` (no duplicar el texto largo aquí).

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el fundamento teórico de arriba
- [ ] Tengo la presentación `{rel_pptx}`
{rompehielos_check}- [ ] Publiqué el material de la sesión en `Clases/{label}/` (**Drive de clases**) · CDigital queda para la **entrega** y las **notas**
- [ ] {"Recordé el link de tutorías " + LINK_TUTORIAS if course["key"] == "proyecto1" else "Preparé el ejemplo/modelación del tema de hoy"}
- [ ] Meet listo: {meet}
{post_clase_block}
"""


def _post_clase_proyecto1() -> str:
    """Checklist de cierre AFI: registro docente + recordatorio asistencia estudiante."""
    return f"""
---

📋 **Checklist post-clase / seguimiento AFI**
- [ ] **Seguimiento docente — diligenciar formulario** de *Registro de Sesiones Sincrónicas y Tutorías Especialización* **dentro de 24h**, con el link de grabación: {LINK_REGISTRO_DOCENTE_AFI} *(uso exclusivo docente AFI — no compartir con estudiantes)*
- [ ] En tutoría: recordé a los estudiantes su formulario de asistencia: {LINK_TUTORIAS}
"""


def _run_rich_guion_regen(course_key: str, only_n: int | None = None) -> None:
    """Invoca regeneradores minuto-a-minuto (solo .md)."""
    import importlib.util
    import subprocess

    if course_key == "proyecto1":
        script = os.path.join(
            COURSES["proyecto1"]["folder"], "Guiones", "_regen_guiones_proyecto1.py"
        )
    elif course_key == "creatividad":
        script = os.path.join(
            COURSES["creatividad"]["folder"], "Guiones", "_regen_guiones_creatividad.py"
        )
    elif course_key in {"investigacion", "tg2", "tg3"}:
        script = os.path.join(SLIDES_DIR, "_regen_guiones_pregrado.py")
    else:
        return
    if not os.path.isfile(script):
        print("WARN regenerador ausente:", script)
        return
    args = [sys.executable, script]
    if course_key in {"investigacion", "tg2", "tg3"}:
        args.append(course_key)
        if only_n is not None:
            args.append(str(only_n))
    elif only_n is not None:
        args.append(str(only_n))
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print("WARN regen:", r.stderr or r.stdout)
    else:
        if r.stdout:
            print(r.stdout.rstrip())


def _cleanup_legacy_temas(course):
    """Elimina Clases/Temas/ tras migrar a Sesion NN."""
    temas = os.path.join(course["folder"], "Clases", "Temas")
    if os.path.isdir(temas):
        shutil.rmtree(temas, ignore_errors=True)
        print("REMOVED", temas)


def _cleanup_legacy_guiones(course, keep_labels: set[str]):
    """Quita guiones obsoletos; elimina cualquier .docx residual bajo Guiones/."""
    guiones = os.path.join(course["folder"], "Guiones")
    if not os.path.isdir(guiones):
        return
    for name in os.listdir(guiones):
        if name == "Capturas" or name.startswith("_"):
            continue
        path = os.path.join(guiones, name)
        if not os.path.isfile(path):
            continue
        stem, ext = os.path.splitext(name)
        if ext.lower() == ".docx":
            os.remove(path)
            print("REMOVED docx residual", path)
            continue
        if ext.lower() != ".md":
            continue
        if stem in keep_labels:
            continue
        if re.match(r"^Sesion \d{2} - ", stem):
            if stem not in keep_labels:
                os.remove(path)
                print("REMOVED stale", path)
            continue
        # Conservar guías/anexos que no son guiones de sesión (p. ej. «Guía práctica…»)
        if stem.lower().startswith("guía") or stem.lower().startswith("guia"):
            continue
        os.remove(path)
        print("REMOVED legacy", path)


def generate_one(course_key: str, n: int, *, guion_only: bool = False):
    course = COURSES[course_key]
    ses = next((s for s in course["sesiones"] if s["n"] == n), None)
    if not ses:
        print(f"SKIP {course_key} sesión {n}: no existe")
        return
    pptx, md, label, _ses_dir = _paths(course, ses)
    # Sesión 01 = encuadre en los 5 cursos (build_pptx → build_pptx_presentacion).
    # El antiguo builder rico de tema de Creatividad S01 quedó obsoleto (archivado 2026-08-09).
    nslides = 0
    if not guion_only:
        nslides = build_pptx(course, ses, pptx)
    if course_key in RICH_GUION_COURSES:
        # Los regeneradores escriben todos los .md del curso; se invocan en generate_course.
        print(f"OK {course_key} · {label}: pptx({nslides}) · guion = regenerador propio (.md)")
        return
    text = build_guion_md(course, ses, label)
    with open(md, "w", encoding="utf-8") as f:
        f.write(text)
    if guion_only:
        print(f"OK {course_key} · {label}: md (guion-only)")
    else:
        print(f"OK {course_key} · {label}: pptx({nslides}) + md")


def generate_course(course_key: str, only_n: int | None = None, *, guion_only: bool = False):
    course = COURSES[course_key]
    keep = set()
    targets = course["sesiones"] if only_n is None else [s for s in course["sesiones"] if s["n"] == only_n]
    for s in targets:
        generate_one(course_key, s["n"], guion_only=guion_only)
        keep.add(session_folder_name(s["n"], s["titulo"]))
    if course_key in RICH_GUION_COURSES:
        _run_rich_guion_regen(course_key, only_n)
    if only_n is None:
        keep = {session_folder_name(s["n"], s["titulo"]) for s in course["sesiones"]}
        _cleanup_legacy_guiones(course, keep)
        if not guion_only:
            _cleanup_legacy_temas(course)
            clases = os.path.join(course["folder"], "Clases")
            if os.path.isdir(clases):
                for name in os.listdir(clases):
                    path = os.path.join(clases, name)
                    if os.path.isdir(path) and re.match(r"^Sesion \d{2} - ", name) and name not in keep:
                        shutil.rmtree(path, ignore_errors=True)
                        print("REMOVED orphan session dir", path)


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return
    args = list(argv[1:])
    guion_only = "--guion-only" in args
    if guion_only:
        args = [a for a in args if a != "--guion-only"]
    if len(args) < 2:
        print(__doc__)
        return
    course_arg, ses_arg = args[0], args[1]
    keys = list(COURSES) if course_arg == "all" else [course_arg]
    for key in keys:
        if key not in COURSES:
            print("Curso desconocido:", key)
            continue
        if ses_arg == "all":
            generate_course(key, None, guion_only=guion_only)
        else:
            generate_course(key, int(ses_arg), guion_only=guion_only)


if __name__ == "__main__":
    main(sys.argv)
