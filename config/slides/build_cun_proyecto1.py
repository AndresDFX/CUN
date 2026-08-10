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
from fechas_entrega_aca import blocks_para_slide, entrega_por_id, fmt_entrega

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
URL_PLANTILLA_ACA = "Clases/Recursos/ACAs/ (enunciados ACA 1–3 · autoevaluación · coevaluación)"
# Enlace real si existe en carga_academica_2026.json → cursos.proyecto1.meet; si no, placeholder.
URL_MEET = meet_url("proyecto1", "Proyecto I")
# URL real del aula desde carga_academica_2026.json → cursos.<key>.cdigital
# (auditada en CDigital el 2026-08-10). Si falta, `cdigital_url` da el placeholder.
URL_CDIGITAL = cdigital_url("proyecto1")
FUENTE_ESP329 = "Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx"

set_footer("")
prs = new_prs()

# ---------- 1. PORTADA (único slide con grupo) ----------
_p1_raw = cover_meta_lines("proyecto1", horario_suffix=" (2 horas)")
_p1_meta = [
    _p1_raw[0],
    "**Programa:** Especialización en Inteligencia Artificial",
    "**Código SIAC:** ESP329 · Virtual · 2 créditos · Nota única",
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
        "ACA 1, 2 y 3 son **avances acumulativos del mismo producto** (no tareas aisladas).",
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

# ---------- EVALUACIÓN ESP329 ----------
table_content(
    prs, "EVALUACIÓN — NOTA ÚNICA (ESP329 / Art. 41)",
    ["Componente", "%", "Qué valora"],
    [
        ["ACA 1", "25%", "Avance: problema, pregunta, objetivos, justificación…"],
        ["ACA 2", "25%", "Avance: marco referencial (antecedentes, teórico, etc.)"],
        ["ACA 3 (anteproyecto)", "42%", "Producto consolidado + metodología + planeación"],
        ["Autoevaluación", "4%", "Individual (cierre)"],
        ["Coevaluación", "4%", "Individual (cierre)"],
    ],
    note="Seguimiento formativo de un producto único y acumulativo. Si ACA 3 evidencia correcciones y resultados, el docente puede ajustar favorablemente ACA 1/2 con trazabilidad en CDigital.",
    idx=_i, fs_body=12, col_w=[3.2, 1.0, 6.7],
)
_i += 1

# ---------- AUTO / COEVALUACIÓN (solo P1 AFI) ----------
content_slide(
    prs,
    "AUTOEVALUACIÓN Y COEVALUACIÓN — CÓMO FUNCIONAN",
    [
        "**Aplican solo en Proyecto I** (ESP329 · Art. 41 · cronograma AFI). **No** en Proyecto II ni en pregrado Art. 52.",
        "**Autoevaluación (4%):** tú valoras tu proceso, aportes al equipo y logro del anteproyecto. Individual y honesta.",
        "**Coevaluación (4%):** valoras el trabajo colaborativo / aportes de pares de tu equipo (respeto + criterio académico).",
        "**Dónde:** actividad individual en **CDigital**. Instructivos en tu carpeta: `Recursos/ACAs/`.",
        # Ventanas leídas del CRONOGRAMA OFICIAL (fechas_entrega_aca.CRONOGRAMA_OFICIAL_P1);
        # antes estaban escritas a mano y se habían desfasado un día (10–16/11 · 17–22/11).
        f"**Cuándo (26ES4):** coevaluación "
        f"{bold_var(fmt_entrega(entrega_por_id('proyecto1', 'coev').apertura, largo=False) + '–' + fmt_entrega(entrega_por_id('proyecto1', 'coev').entrega, largo=False))} · "
        f"autoevaluación "
        f"{bold_var(fmt_entrega(entrega_por_id('proyecto1', 'auto').apertura, largo=False) + '–' + fmt_entrega(entrega_por_id('proyecto1', 'auto').entrega, largo=False))} "
        f"(cierre notas {bold_var('22/11/2026')}).",
        "**Quién califica:** el estudiante diligencia el instrumento; el Docente habilita la ventana, verifica y registra la nota en el gradebook.",
        "**Evidencia:** completar la actividad en la ventana. No sustituye ACA 3 (anteproyecto).",
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
         "ACA 3 (42%) solo tiene 2 lunes sincrónicos (19/10 y 26/10). Apóyate en tutorías adicionales "
         f"acordadas en la semana con el Docente y registra cada una en el formulario."),
        ("info", MSG_TUTORIAS_POR_GRUPO),
        ("aclaracion",
         "ESP329 / AFI: en Proyecto I se **diseña** la metodología (instrumentos propuestos); "
         "la aplicación y recolección son de Proyecto II."),
    ],
    idx=_i,
)
_i += 1

# ---------- QUÉ ENTREGA CADA ACA (cruce ESP329 unidades + AFI) ----------
table_content(
    prs, "QUÉ ENTREGA CADA EQUIPO EN CADA ACA",
    ["ACA", "Contenido (unidades ESP329)"],
    [
        ["ACA 1 (25%)", "U2–U3 (+alcances): problema, pregunta, objetivos, justificación, alcances/limitaciones."],
        ["ACA 2 (25%)", "U4: correcciones ACA1 + marco referencial (antecedentes, teórico, conceptual, contextual, legal)."],
        ["ACA 3 (42%)", "U5–U7: correcciones + metodología + cronograma/presupuesto + anteproyecto FINAL integrado."],
    ],
    note="Equipos máx. 3 (AFI). Formato: Plantilla APA CUN – Proyecto de Grado (APA 7). Criterios: coherencia, pertinencia, rigor, fuentes, escritura, integridad y viabilidad (ESP329).",
    idx=_i,
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
        f"**Enunciados ACA (estudiantes):** `{URL_PLANTILLA_ACA}`",
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
