# -*- coding: utf-8 -*-
"""Genera la Presentación del Curso — PROYECTO I (CUN).
   Fuente primaria: Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx
   Cruce AFI (instructivo/cronograma) solo donde no contradiga el ESP329.
   Material proyectado: «el Docente» (sin nombre propio); grupo(s) solo en portada.
   Salida: .../Clases/Presentacion del Curso - Proyecto I.pptx
"""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))
from cun_slides_engine import *
from sesiones_cun import COURSES, DOCENTE_CORREO, LINK_TUTORIAS, MSG_TUTORIAS_POR_GRUPO, meet_url
from carga_academica import bold_var, cover_meta_lines, curso as carga_curso
from fechas_entrega_aca import (
    blocks_para_slide,
    entrega_por_id,
    entregas_para_grupo,
    fmt_entrega,
    fmt_peso,
    peso_corte,
)
# Catálogo de los .docx que viven en `Clases/Recursos/ACAs/`: mismo módulo que los
# escribe, así que los nombres que cita esta presentación son los del disco.
from build_acas_estudiantes import documentos_for as acas_documentos_for

OUT_DIR = os.path.join(COURSES["proyecto1"]["folder"], "Clases")
from sesiones_cun import cdigital_url, CDIGITAL_PLACEHOLDER  # noqa: E402
OUT = os.path.join(OUT_DIR, "Presentacion del Curso - Proyecto I.pptx")
os.makedirs(OUT_DIR, exist_ok=True)

D = datetime.date
DOCENTE_CREDENCIALES = [
    "Ingeniero de Sistemas",
    "Candidato a MSc en Inteligencia Artificial",
    "Líder Técnico",
    "Speaker Tecnológico",
]
LINK_TUTORIAS_ESTUDIANTE = LINK_TUTORIAS
# La plantilla NO se enlaza por URL pública: viaja DENTRO de la carpeta que recibe el
# estudiante. Ruta relativa a `Clases/` (misma convención que APA_REL en
# build_acas_estudiantes.py). Decisión del docente 2026-08-10.
RUTA_PLANTILLA_APA = "Recursos/Plantilla_APA_CUN_Proyecto de grado.docx"
# Carpeta de enunciados que viaja con el estudiante. NO se enumeran aquí «ACA 1 – 3»:
# esos documentos dejaron de existir cuando los enunciados se renombraron por ítem del
# aula. Los nombres se citan con `doc_aca()`, que los lee del catálogo.
RUTA_ACAS_ESTUDIANTE = "Clases/Recursos/ACAs/"
# Enlace real si existe en carga_academica_2026.json → cursos.proyecto1.meet; si no, placeholder.
URL_MEET = meet_url("proyecto1", "Proyecto I")
# URL real del aula desde carga_academica_2026.json → cursos.<key>.cdigital
# (auditada en CDigital el 2026-08-10). Si falta, `cdigital_url` da el placeholder.
URL_CDIGITAL = cdigital_url("proyecto1")
FUENTE_ESP329 = "Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx"

# ---------- Documentos REALES de `Clases/Recursos/ACAs/` ----------
# Cada enunciado se llama como su ítem del libro de calificaciones:
# `<ítem> (<peso>) - <qué es>.docx`. Ni un nombre se escribe a mano aquí:
# `build_acas_estudiantes` los deriva del MISMO catálogo (fechas_entrega_aca: código del
# ítem + peso) con el que escribe los .docx, así que la slide y la carpeta del estudiante
# no pueden volver a desincronizarse. Antes esta presentación mandaba a buscar «ACA 1 /
# ACA 2 / ACA 3» —documentos que ya no existen— y, peor, anunciaba como guía del Quiz
# (cierra 30/08) el documento del segundo corte.
_P1_DOCS = {d["item"]: d for d in acas_documentos_for("proyecto1")}


def doc_aca(item_id, corto=False):
    """Nombre del documento de `Recursos/ACAs/` que prepara el ítem, tal cual en disco.

    Sin la extensión. Con ``corto=True`` devuelve solo el prefijo por el que el
    estudiante lo reconoce en la carpeta («Quiz (25%)», «ACA FINAL (42%)»): es el mismo
    archivo, sin la cola descriptiva.
    """
    nombre = _P1_DOCS[item_id]["filename"].removesuffix(".docx")
    return nombre.split(" - ")[0] if corto else nombre


set_footer("")
prs = new_prs()

# ---------- 1. PORTADA (único slide con grupo) ----------
_p1_raw = cover_meta_lines("proyecto1", horario_suffix=" (2 horas)")
_p1_meta = [
    _p1_raw[0],
    "**Programa:** Especialización en Inteligencia Artificial",
    # El aula compone la nota en tres cortes (auditoría CDigital 2026-08-10): decirlo aquí
    # evita la contradicción con la tabla de evaluación, que ya no es de «nota única».
    "**Código SIAC:** ESP329 · Virtual · 2 créditos · "
    + " / ".join(fmt_peso(peso_corte("proyecto1", c)) for c in (1, 2, 3))
    + " en tres cortes",
    f"**Fuente curricular:** {FUENTE_ESP329}",
    *_p1_raw[1:],
]
course_cover(
    prs,
    "PROYECTO I",
    "Especialización en Inteligencia Artificial · Código ESP329",
    _p1_meta,
)

# ---------- 2. DOCENTE (genérico · sin nombre propio) ----------
tutor_slide(prs, "Docente", DOCENTE_CREDENCIALES, DOCENTE_CORREO, idx=2)

# ---------- 3. ROMPEHIELOS + QR ----------
icebreaker_qr_slide(
    prs,
    idx=3,
    consignas=[
        f"**Escanea o abre:** {PADLET_PRESENTACION_URL}",
        "Post-it: **nombre** + **expectativa del curso** + **tema tentativo** de investigación (1 frase).",
        "Tablero oficial: **Padlet** (mismo enlace en los 5 cursos).",
        "Ahora (~7 min). Leemos juntos 3–4 notas (sin juzgar).",
    ],
)

# ---------- 4. PROPÓSITO (ESP329 · Justificación + macrocompetencia) ----------
content_slide(
    prs, "¿QUÉ ES PROYECTO I? (ESP329)",
    [
        "Inicia la ruta de trabajo de grado: delimitar una situación problemática y convertirla en un **anteproyecto** coherente, viable y éticamente fundamentado.",
        "Macrocompetencia: **formula un anteproyecto** pertinente para la especialización (problema, antecedentes, objetivos y ruta metodológica viable).",
        "Producto final: **anteproyecto completo**, base para Proyecto II (o equivalente).",
        ("En este espacio **no se recolecta ni se aplica** trabajo de campo — eso corresponde a Proyecto II, tras el aval metodológico.", 1),
        "El Docente acompaña como **garante metodológico** (orientación, revisión y coherencia del anteproyecto).",
    ],
    idx=4,
)

# ---------- 5. RESULTADOS DE APRENDIZAJE (ESP329) ----------
content_slide(
    prs, "RESULTADOS DE APRENDIZAJE (ESP329)",
    [
        "Analiza críticamente información académica y profesional relevante.",
        "Formula problemas, preguntas y objetivos investigables.",
        "Sustenta las decisiones teóricas y metodológicas del anteproyecto.",
        "Integra los componentes del proyecto en un documento académico coherente.",
        "Aplica integridad académica, propiedad intelectual y uso responsable de fuentes e IA.",
    ],
    idx=5,
)

# ---------- 6. LÍNEAS (programa IA + marco institucional ESP329) ----------
content_slide(
    prs, "LÍNEAS DE INVESTIGACIÓN",
    [
        "Todo anteproyecto de la Especialización en IA se enmarca en una línea de **programa**:",
        ("**Uso y adaptación de IA para entornos productivos**", 1),
        ("**Implementación de IA en la educación**", 1),
        "Según ESP329, los proyectos también dialogan con líneas **institucionales** (Gestión y Tecnologías · Innovación Pedagógica · Responsabilidad Social) cuando sea pertinente.",
        "Si tu tema no encaja, **el Docente** te orienta a reformularlo.",
    ],
    idx=6,
)

# ---------- 7. ESTRUCTURA TEMÁTICA ESP329 (7 unidades) ----------
table_content(
    prs, "ESTRUCTURA TEMÁTICA ESP329 — 7 UNIDADES",
    ["U", "Unidad didáctica", "Producto esperado"],
    [
        ["1", "Fundamentos y enfoque de investigación", "Enfoque y tipo de investigación justificados"],
        ["2", "Problema y pregunta de investigación", "Problema delimitado y pregunta viable"],
        ["3", "Objetivos y justificación", "Objetivos y justificación articulados"],
        ["4", "Construcción del marco referencial", "Marco pertinente, actualizado y sustentado"],
        ["5", "Diseño metodológico", "Metodología coherente (instrumentos propuestos)"],
        ["6", "Planeación y viabilidad del proyecto", "Plan de trabajo viable"],
        ["7", "Integración y evaluación del anteproyecto", "Anteproyecto completo listo para P-II"],
    ],
    note=f"Fuente primaria: {FUENTE_ESP329}. Las sesiones semanales desarrollan estas unidades (ver calendario).",
    idx=7, fs_body=11, col_w=[0.6, 4.2, 6.1],
)

# ---------- 8. ESTRATEGIA DIDÁCTICA (ESP329) ----------
content_slide(
    prs, "ESTRATEGIA DIDÁCTICA (ESP329)",
    [
        "**Aprendizaje basado en proyectos** + acompañamiento tutorial.",
        "Sesiones sincrónicas: orientaciones metodológicas, ejemplos, discusión y talleres aplicados al anteproyecto.",
        "Trabajo autónomo: búsqueda/lectura crítica, escritura progresiva, revisión entre pares e incorporación de retro.",
        "Los tres cortes trabajan **un mismo producto acumulativo** (no tareas aisladas): el "
        "corte 1 lo comprueba un **Quiz** en el aula y los cortes 2 y 3 se **suben** como "
        "**ACA 1** y **ACA FINAL**.",
        "Mediación: encuentros sincrónicos, tutorías, recursos en **CDigital** y atención asincrónica.",
        MSG_TUTORIAS_POR_GRUPO,
        "IA generativa: apoyo permitido solo con supervisión humana, verificación, declaración transparente y protección de datos.",
    ],
    idx=8,
)

# ---------- 9. METODOLOGÍA DEL ENCUENTRO (operativa · AFI / horario docente) ----------
table_content(
    prs, "ENCUENTRO SEMANAL (2 HORAS)",
    ["Bloque", "Horario", "Qué ocurre"],
    [
        ["Contenido nuevo", "8:00 – 9:00 pm", "Orientación metodológica de la unidad, modelación, dudas."],
        ["Tutoría / taller", "9:00 – 10:00 pm", "Trabajo en equipos con acompañamiento del Docente."],
    ],
    note=(
        f"ESP329: 32 h acompañamiento directo + 64 h autónomo (2 créditos). Todo el encuentro se graba. "
        f"{MSG_TUTORIAS_POR_GRUPO} Registra cada tutoría (slide siguiente)."
    ),
    idx=9,
)

# ---------- 10. LINK TUTORÍAS ----------
link_callout_slide(
    prs,
    "REGISTRO OBLIGATORIO DE TUTORÍAS",
    "En CADA tutoría (del encuentro o adicional) diligencia TU formulario:",
    LINK_TUTORIAS_ESTUDIANTE,
    notes=[
        MSG_TUTORIAS_POR_GRUPO,
        "⚠️ Sin este registro, tu asistencia a tutorías puede no quedar acreditada.",
        "Formulario del ESTUDIANTE (distinto del registro del Docente). Ambos son obligatorios.",
    ],
    idx=10,
)

# ---------- 11. CONTENIDO (sesiones · UNA sola slide) ----------
_ses = COURSES["proyecto1"]["sesiones"]
_n_cont = contenido_sesiones_slide(prs, _ses, idx=11)
_i = 11 + _n_cont  # siguiente idx libre

# ---------- EVALUACIÓN ESP329 — ítems REALES del aula ----------
# La tabla se genera desde `fechas_entrega_aca` (libro de calificaciones de CDigital,
# auditoría 2026-08-10): ni un peso escrito a mano. El aula NO nombra los componentes
# «ACA 1 / 2 / 3»: el primer corte es un **Quiz** (cuestionario), el segundo la **ACA 1**
# (tarea) y el tercero la **ACA FINAL** + autoevaluación (cuestionario) + coevaluación
# (foro). El documento de `Recursos/ACAs/` que prepara cada ítem se declara en la fila
# con su nombre REAL —vía `doc_aca()`, no escrito a mano—, porque el enunciado ya se
# renombró por ítem del aula y los viejos «ACA 1 / 2 / 3» ya no están en la carpeta.
QUE_VALORA_P1 = {
    "quiz": "Comprobación individual en CDigital de las sesiones 02–03: problema, "
            "pregunta, objetivos y justificación. Guía escrita: "
            f"`{doc_aca('quiz', corto=True)}`.",
    "aca1": "Documento del equipo: correcciones + marco referencial — antecedentes, "
            "teórico, conceptual, contextual y legal. Enunciado: "
            f"`{doc_aca('aca1', corto=True)}`.",
    "aca_final": "Anteproyecto completo e integrado: metodología, instrumentos "
                 "propuestos, cronograma, presupuesto y viabilidad. Enunciado: "
                 f"`{doc_aca('aca_final', corto=True)}`.",
    "auto": "Tu valoración de tu propio proceso y de tu aporte al equipo (individual). "
            f"Instructivo: `{doc_aca('auto', corto=True)}`.",
    "coev": "Valoración de los aportes de tus pares del equipo: se participa en el foro. "
            f"Instructivo: `{doc_aca('coev', corto=True)}`.",
}
_p1_items = entregas_para_grupo("proyecto1")
table_content(
    prs, "EVALUACIÓN — LOS TRES CORTES EN EL AULA (ESP329 / Art. 41)",
    ["Ítem en CDigital", "Tipo", "Corte (peso)", "Peso", "Qué valora"],
    [
        [
            f"**{e.code}**",
            e.tipo_label,
            f"{e.corte} ({fmt_peso(peso_corte('proyecto1', e.corte))})",
            f"**{e.weight_pct}**",
            QUE_VALORA_P1[e.id],
        ]
        for e in _p1_items
    ],
    note=(
        f"Estructura, tipo de actividad y pesos = **libro de calificaciones del aula**; "
        f"suman {bold_var(fmt_peso(sum(e.weight for e in _p1_items)))}. ESP329 declara nota "
        f"única: el aula la compone en **tres cortes "
        f"({' / '.join(fmt_peso(peso_corte('proyecto1', c)) for c in (1, 2, 3))})**. "
        "Producto único y acumulativo: si el anteproyecto final evidencia correcciones y "
        "resultados, el Docente puede ajustar favorablemente los avances previos, con "
        "trazabilidad en CDigital."
    ),
    idx=_i, fs_body=11, col_w=[2.1, 1.4, 1.5, 1.0, 5.9],
)
_i += 1

# ---------- AUTO / COEVALUACIÓN ----------
# Ya NO se presentan como exclusivas de Proyecto I: la auditoría del libro de
# calificaciones (2026-08-10) las encontró en los CINCO cursos. Lo propio de Proyecto I
# es el peso (4% + 4% según ESP329 / Art. 41), no la existencia del instrumento.
content_slide(
    prs,
    "AUTOEVALUACIÓN Y COEVALUACIÓN — CÓMO FUNCIONAN",
    [
        # Pesos leídos del libro de calificaciones (antes estaban escritos a mano).
        f"**En Proyecto I pesan {entrega_por_id('proyecto1', 'auto').weight_pct} + "
        f"{entrega_por_id('proyecto1', 'coev').weight_pct}** (ESP329 · Art. 41 · cronograma AFI), "
        "dentro del tercer corte. Existen también en los demás cursos del Docente, con otro peso: "
        "lo que cambia es el porcentaje, no el instrumento.",
        f"**Autoevaluación ({entrega_por_id('proyecto1', 'auto').weight_pct}):** tú valoras tu proceso, aportes al equipo y logro del anteproyecto. Individual y honesta. En el aula es un **cuestionario**.",
        f"**Coevaluación ({entrega_por_id('proyecto1', 'coev').weight_pct}):** valoras el trabajo colaborativo / aportes de pares de tu equipo (respeto + criterio académico). En el aula es un **foro**: se participa, no se sube archivo.",
        "**Dónde:** actividades individuales en **CDigital**. Instructivos en tu carpeta: `Recursos/ACAs/`.",
        # Ventanas leídas del CRONOGRAMA OFICIAL (fechas_entrega_aca.VENTANAS["proyecto1"]);
        # antes estaban escritas a mano y se habían desfasado un día (10–16/11 · 17–22/11).
        f"**Cuándo (26ES4):** coevaluación "
        f"{bold_var(fmt_entrega(entrega_por_id('proyecto1', 'coev').apertura, largo=False) + '–' + fmt_entrega(entrega_por_id('proyecto1', 'coev').entrega, largo=False))} · "
        f"autoevaluación "
        f"{bold_var(fmt_entrega(entrega_por_id('proyecto1', 'auto').apertura, largo=False) + '–' + fmt_entrega(entrega_por_id('proyecto1', 'auto').entrega, largo=False))} "
        f"(cierre notas {bold_var('22/11/2026')}).",
        "**Quién califica:** el estudiante diligencia el instrumento; el Docente habilita la ventana, verifica y registra la nota en el gradebook.",
        "**Evidencia:** completar la actividad en la ventana. No sustituye el anteproyecto final (**ACA FINAL** en el aula).",
    ],
    idx=_i,
    size=13,
)
_i += 1

box_note_slide(
    prs,
    "ROLES — AUTO / COEVALUACIÓN",
    [
        (
            "info",
            "Estudiante: espera la habilitación en CDigital → diligencia individual → respeta plazos. "
            "Si eres de equipo, la coevaluación mira aportes reales del trabajo conjunto.",
        ),
        (
            "aclaracion",
            "Docente: configurar/habilitar actividades individuales en las ventanas oficiales; "
            "calificar/registrar antes del cierre de notas; conservar evidencia en el aula.",
        ),
        (
            "advertencia",
            "No confundir con la «autoevaluación» institucional SIAC (calidad de programas en "
            "acreditacion.cun.edu.co): esa no es una nota del curso.",
        ),
    ],
    idx=_i,
)
_i += 1

# ---------- CRONOGRAMA INICIO / CIERRE (fechas_entrega_aca · inicio 10/08) ----------
blocks = blocks_para_slide("proyecto1")
festivos = [
    (D(2026, 8, 17), "Asunción de la Virgen"),
    (D(2026, 10, 12), "Día de la Raza"),
    (D(2026, 11, 2), "Todos los Santos"),
    (D(2026, 11, 16), "Indep. de Cartagena"),
]
fechas_inicio_fin_slide(
    prs, "CRONOGRAMA — VENTANAS DE ENTREGA (AFI 26ES4)",
    blocks, holiday_marks=festivos,
    note=f"📌 Tutorías → {LINK_TUTORIAS_ESTUDIANTE}",
    sub=f"Periodo {bold_var('26ES4')} · cierre y registro de notas: {bold_var('22/11/2026')}",
    idx=_i,
)
_i += 1

# ---------- AVISO ACA3 ----------
box_note_slide(
    prs, "AVISO IMPORTANTE",
    [
        ("advertencia",
         f"La **ACA FINAL** ({entrega_por_id('proyecto1', 'aca_final').weight_pct}, el anteproyecto "
         "integrado) solo tiene 2 lunes sincrónicos (19/10 y 26/10). Apóyate en tutorías adicionales "
         "acordadas en la semana con el Docente y registra cada una en el formulario."),
        ("info", MSG_TUTORIAS_POR_GRUPO),
        ("aclaracion",
         "ESP329 / AFI: en Proyecto I se **diseña** la metodología (instrumentos propuestos); "
         "la aplicación y recolección son de Proyecto II."),
    ],
    idx=_i,
)
_i += 1

# ---------- QUÉ SE PREPARA EN CADA CORTE (cruce ESP329 unidades + ítem del aula) ----------
# Conviven TRES nomenclaturas y el estudiante tropieza con las tres: el **Syllabus
# ESP329** numera tres ACAs (1 / 2 / 3), el **aula** califica Quiz · ACA 1 · ACA FINAL,
# y los **documentos** de `Recursos/ACAs/` se titulan como el ítem del aula. La tabla
# publica el puente completo para que nadie busque en el gradebook un ítem que no existe
# ni en su carpeta un archivo que ya no se llama así. Ojo: la «ACA 1» del Syllabus NO es
# el archivo «ACA 1» de la carpeta —esa es la del segundo corte—; por eso la tercera
# columna sale de `doc_aca()` (catálogo) y no de un nombre escrito a mano.
_p1_puente = [
    ("quiz", "ACA 1", "U2–U3 (+alcances): problema, pregunta, objetivos, justificación, "
                      "alcances/limitaciones. Se comprueba en el **Quiz** del aula."),
    ("aca1", "ACA 2", "U4: correcciones + marco referencial (antecedentes, teórico, "
                      "conceptual, contextual, legal). Se **sube** como ACA 1 del aula."),
    ("aca_final", "ACA 3", "U5–U7: correcciones + metodología + cronograma/presupuesto + "
                           "anteproyecto FINAL integrado. Se **sube** como ACA FINAL."),
]
table_content(
    prs, "QUÉ SE PREPARA EN CADA CORTE (Y CÓMO SE LLAMA EN CADA SITIO)",
    ["En el Syllabus ESP329", "Ítem del aula (CDigital)",
     "Documento en Recursos/ACAs/", "Contenido (unidades ESP329)"],
    [
        [
            f"**{doc}**",
            f"**{entrega_por_id('proyecto1', item_id).code}** "
            f"({entrega_por_id('proyecto1', item_id).tipo_label.lower()} · "
            f"{entrega_por_id('proyecto1', item_id).weight_pct})",
            f"`{doc_aca(item_id)}.docx`",
            texto,
        ]
        for item_id, doc, texto in _p1_puente
    ],
    note=(
        "Tres nombres para lo mismo: el Syllabus numera las ACAs, el aula califica "
        "**Quiz · ACA 1 · ACA FINAL** y tu carpeta titula cada documento como su ítem. "
        "Busca siempre por el nombre de la tercera columna. Equipos máx. 3 (AFI). "
        "Formato: Plantilla APA CUN – Proyecto de Grado (APA 7). Criterios: coherencia, "
        "pertinencia, rigor, fuentes, escritura, integridad y viabilidad (ESP329)."
    ),
    idx=_i, fs_body=11, col_w=[1.5, 1.9, 3.4, 5.1],
)
_i += 1

# ---------- RECURSOS ----------
content_slide(
    prs, "RECURSOS, PLANTILLAS Y ENLACES",
    [
        f"**Contacto del Docente:** {DOCENTE_CORREO}",
        f"**CDigital (campus del curso):** {bold_var(URL_CDIGITAL)}",
        f"**Registro de tutorías (obligatorio):** @@{LINK_TUTORIAS_ESTUDIANTE}@@",
        MSG_TUTORIAS_POR_GRUPO,
        f"**Google Meet (mismo enlace toda la serie):** {bold_var(URL_MEET)}",
        f"**Plantilla APA CUN – Proyecto de Grado** (viene en tu carpeta del curso): "
        f"`{RUTA_PLANTILLA_APA}`.",
        f"**Plantilla APA CUN (en tu carpeta):** `{RUTA_PLANTILLA_APA}`",
        f"**Enunciados y guías:** `{RUTA_ACAS_ESTUDIANTE}` — un documento por ítem del "
        "aula, con su nombre y su peso.",
        "**Biblioteca Virtual CUN + bases:** Google Scholar, Redalyc, SciELO, Dialnet · citas: ZoteroBib / Google Docs.",
        f"**Syllabus fuente:** `{FUENTE_ESP329}` · Entregas oficiales solo por CDigital.",
    ],
    idx=_i,
)

# ---------- CIERRE ----------
_p1_h = carga_curso("proyecto1")["horario"]
_p1_h_txt = _p1_h.get("texto_corto") or _p1_h["texto"]
closing_slide(
    prs,
    "¡Empezamos!",
    [
        f"Nos vemos en el primer encuentro sincrónico: {bold_var(_p1_h_txt)}.",
        "El Docente — garante metodológico de tu anteproyecto.",
        MSG_TUTORIAS_POR_GRUPO,
        f"Tutorías: regístrate siempre en {LINK_TUTORIAS_ESTUDIANTE}",
    ],
    "PROYECTO I · ESP329",
)

prs.save(OUT)
print("OK ->", OUT, "| slides:", len(prs.slides))
