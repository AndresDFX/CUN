# -*- coding: utf-8 -*-
"""Actualiza las Presentaciones del Curso de las 5 asignaturas CUN
   (tutor genérico «Docente» + listado de sesiones en 1 slide + marca CUN).

   Metadatos de semestre (bloque, horario, grupos solo en portada, fechas):
   `config/cursos/carga_academica_2026.json` → builds de Proyecto I y Pregrado.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))
from cun_slides_engine import *
from sesiones_cun import (
    COURSES, DOCENTE_CORREO, DOCENTE_CREDS, LINK_TUTORIAS,
    MSG_TUTORIAS_POR_GRUPO, meet_url,
)
from carga_academica import bold_var, cover_meta_lines, curso as carga_curso

# Placeholder de respaldo: los usos por curso deben llamar a
from sesiones_cun import cdigital_url, CDIGITAL_PLACEHOLDER  # noqa: E402
# `cdigital_url(<clave del curso>)`, que devuelve la URL real del aula si existe
# en carga_academica_2026.json (auditadas el 2026-08-10) y el placeholder si no.
URL_CDIGITAL = CDIGITAL_PLACEHOLDER
# La plantilla NO se enlaza por URL pública: viaja DENTRO de la carpeta que recibe el
# estudiante. Ruta relativa a `Clases/` (misma convención que APA_REL en
# build_acas_estudiantes.py). Decisión del docente 2026-08-10.
RUTA_PLANTILLA_APA = "Recursos/Plantilla_APA_CUN_Proyecto de grado.docx"


def build_proyecto1(course):
    """Deck compacto de respaldo. El deck rico canónico es build_cun_proyecto1.py."""
    out = os.path.join(course["folder"], "Clases", "Presentacion del Curso - Proyecto I.pptx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    set_footer("")
    prs = new_prs()
    meta = cover_meta_lines(
        "proyecto1",
        horario_suffix="",
        extra=[f"**Tutorías (registro):** {LINK_TUTORIAS}"],
    )
    # Portada compacta: periodo/horario/grupo ya vienen con negrita de oferta.
    course_cover(prs, "PROYECTO I", "Especialización en IA · ESP329", meta)
    tutor_slide(prs, "Docente", DOCENTE_CREDS, DOCENTE_CORREO, idx=2)
    content_slide(prs, "¿QUÉ ES PROYECTO I?", [
        "Formular un **anteproyecto** viable y metodológicamente sólido.",
        "Nada se recolecta ni se aplica (eso es Proyecto II).",
        "El Docente es el garante metodológico del proceso.",
    ], idx=3)
    content_slide(prs, "LÍNEAS DE INVESTIGACIÓN", [
        ("**Uso y adaptación de IA para entornos productivos**", 0),
        ("**Implementación de IA en la educación**", 0),
    ], idx=4)
    table_content(prs, "METODOLOGÍA DEL ENCUENTRO (2 H)",
        ["Bloque", "Horario", "Qué ocurre"],
        [["Contenido", "8:00–9:00 pm", "Concepto de la semana + modelación"],
         ["Tutoría", "9:00–10:00 pm", "Acompañamiento con el Docente"]],
        note=f"{MSG_TUTORIAS_POR_GRUPO} En CADA tutoría registra asistencia: {LINK_TUTORIAS}", idx=5)
    link_callout_slide(prs, "REGISTRO OBLIGATORIO DE TUTORÍAS",
        "Diligencia TU formulario en cada tutoría:", LINK_TUTORIAS,
        notes=[
            MSG_TUTORIAS_POR_GRUPO,
            "Distinto del registro del Docente. Sin esto, tu asistencia puede no acreditarse.",
        ], idx=6)
    _n_cont = contenido_sesiones_slide(prs, course["sesiones"], idx=7)
    _i = 7 + _n_cont
    table_content(prs, "QUÉ ENTREGA CADA ACA",
        ["ACA", "Contenido"],
        [["ACA1 25%", "Problema, pregunta, objetivos, justificación, alcances"],
         ["ACA2 25%", "Correcciones + marco referencial (antecedentes ≥6)"],
         ["ACA3 42%", "Metodología propuesta + cronograma + presupuesto = anteproyecto final"]],
        idx=_i)
    _i += 1
    content_slide(prs, "RECURSOS Y PLANTILLAS", [
        f"**Contacto del Docente:** {DOCENTE_CORREO}",
        f"**CDigital (campus del curso):** {bold_var(cdigital_url('proyecto1'))}",
        f"**Tutorías:** @@{LINK_TUTORIAS}@@",
        MSG_TUTORIAS_POR_GRUPO,
        f"**Meet:** {bold_var(meet_url('proyecto1', 'Proyecto I'))}",
        f"**Plantilla APA CUN:** `{RUTA_PLANTILLA_APA}` (viene en tu carpeta del curso)",
        f"**Plantilla APA CUN (en tu carpeta):** `{RUTA_PLANTILLA_APA}`",
        "**Enunciados ACA:** `Clases/Recursos/ACAs/`",
    ], idx=_i)
    _p1_h = carga_curso("proyecto1")["horario"]
    _p1_h_txt = _p1_h.get("texto_corto") or _p1_h["texto"]
    closing_slide(prs, "¡Empezamos!", [
        f"Nos vemos en el primer encuentro sincrónico: {bold_var(_p1_h_txt)}.",
        "El Docente — garante metodológico de tu anteproyecto.",
        MSG_TUTORIAS_POR_GRUPO,
        f"Tutorías → {LINK_TUTORIAS}",
    ], "PROYECTO I · ESP329")
    prs.save(out)
    print("OK", out, "slides", len(prs.slides))


def build_pregrado(course, filename):
    """Deck compacto de respaldo. El deck rico canónico es build_pregrado_cursos.py."""
    out = os.path.join(course["folder"], "Clases", filename)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    key = course.get("key")
    if key in ("investigacion", "creatividad", "tg2", "tg3"):
        set_footer("")
    prs = new_prs()
    if key in ("investigacion", "creatividad", "tg2", "tg3"):
        meta = cover_meta_lines(key, extra=[f"**Fuente de temas:** {course['fuente']}"])
    else:
        meta = [
            f"**Código:** {course['codigo']}",
            f"**Horario:** {course['horario']}",
            f"**Contacto del Docente:** {DOCENTE_CORREO}",
            f"**Fuente de temas:** {course['fuente']}",
        ]
    if course.get("nota_syllabus"):
        meta.append(f"⚠️ {course['nota_syllabus']}")
    course_cover(prs, course["titulo"], course["titulo_largo"], meta)
    tutor_slide(prs, "Docente", DOCENTE_CREDS, DOCENTE_CORREO, idx=2)
    content_slide(prs, "PROPÓSITO DEL CURSO", [
        f"Asignatura: **{course['titulo_largo']}**.",
        f"Temario tomado de: {course['fuente']}.",
        "Enfoque teórico-práctico con trabajo autónomo entre sesiones.",
        # La actividad de la clase autónoma vive en el **Drive de clases** (la carpeta
        # `Clases/` que comparte el Docente), en la carpeta de esa sesión. CDigital sigue
        # siendo donde se ENTREGA y donde están las notas: no mezclar los dos roles.
        "Si el día de clase es festivo colombiano → **clase autónoma** "
        "(actividad en el **Drive de clases**, en la carpeta de esa sesión).",
    ], idx=3)
    _n_cont = contenido_sesiones_slide(prs, course["sesiones"], idx=4)
    _i = 4 + _n_cont
    content_slide(prs, "RECURSOS", [
        f"**Contacto del Docente:** {DOCENTE_CORREO}",
        f"**CDigital (campus del curso):** {bold_var(cdigital_url(key))}",
        f"**Meet:** {bold_var(meet_url(course['key'], course['titulo']))}",
        f"**Plantilla APA CUN:** `{RUTA_PLANTILLA_APA}` (viene en tu carpeta del curso)",
        f"**Plantilla APA CUN (en tu carpeta):** `{RUTA_PLANTILLA_APA}`",
    ], idx=_i)
    closing_slide(prs, "¡Empezamos!", [
        "Nos vemos en el primer encuentro sincrónico.",
        f"Horario semanal: {bold_var(course['horario'])}",
        f"Contacto del Docente: {DOCENTE_CORREO}",
    ], course["titulo"])
    prs.save(out)
    print("OK", out, "slides", len(prs.slides))


def main():
    """Regenera presentaciones: Proyecto I (deck rico) + Pregrado vía build_pregrado_cursos
    (incluye horario confirmado en portada, calendarios CSV/ICS e Informacion.txt).
    """
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.check_call([sys.executable, os.path.join(here, "build_cun_proyecto1.py")])
    subprocess.check_call([sys.executable, os.path.join(here, "build_pregrado_cursos.py")])
    subprocess.check_call([sys.executable, os.path.join(here, "build_calendar_proyecto1_54es4.py")])


if __name__ == "__main__":
    main()
