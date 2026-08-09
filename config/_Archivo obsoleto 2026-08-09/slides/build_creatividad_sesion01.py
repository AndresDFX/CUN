# -*- coding: utf-8 -*-
"""Genera Presentacion.pptx de Sesión 01 — Creatividad y Pensamiento Innovador.

Solo el tema de la clase + nº Sesión 01.
Sin fechas de periodo, sin mapa completo del curso, sin bio/correo del docente.
"""
from __future__ import annotations
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))
from cun_slides_engine import (
    new_prs, course_cover, content_slide, table_content,
    box_note_slide, closing_slide, set_footer,
)
from carga_academica import footer_inicio_efectivo
from sesiones_cun import COURSES


def _out_path() -> str:
    """Ruta canónica = carpeta Sesion 01 de `sesiones_cun` (mismo criterio que build_sesion_material)."""
    from build_sesion_material import session_folder_name

    course = COURSES["creatividad"]
    ses = next(s for s in course["sesiones"] if s["n"] == 1)
    label = session_folder_name(ses["n"], ses["titulo"])
    ses_dir = os.path.join(course["folder"], "Clases", label)
    os.makedirs(ses_dir, exist_ok=True)
    return os.path.join(ses_dir, "Presentacion.pptx")


def build():
    set_footer(footer_inicio_efectivo("creatividad"))
    prs = new_prs()
    tema = next(s["titulo"] for s in COURSES["creatividad"]["sesiones"] if s["n"] == 1)

    # 1 Portada
    course_cover(
        prs,
        "SESIÓN 01 — Introducción",
        "Propuesta de Innovación (trabajo final)",
        [
            "**Sesión 01**",
            f"**Tema:** {tema}",
            "**Asignatura:** Creatividad y Pensamiento Innovador — Escuela de Ingenierías",
            "**Producto de hoy:** Ficha problema–oportunidad (insumo #1)",
        ],
    )

    # 2 Objetivos
    content_slide(prs, "OBJETIVOS DE HOY", [
        "**Distinguir** creatividad de innovación con ejemplos de Ingeniería.",
        "**Anunciar** el hilo conductor: **Propuesta de Innovación** (se construye desde hoy).",
        "**Redactar** en clase una ficha: problema + usuario + tipo tentativo.",
        "**Salir** con tarea autónoma clara para la Sesión 02.",
    ], idx=2)

    # 3 Enfoque (sin logística de semestre)
    box_note_slide(prs, "ENFOQUE DE HOY", [
        ("info", "Hoy no entregamos la propuesta completa: entregamos el **insumo #1** (ficha de problema)."),
        ("aclaracion", "Cada unidad alimentará el **mismo** documento — no son talleres isla."),
        ("advertencia", "Sin problema claro no hay propuesta defendible."),
    ], idx=3)

    # Padlet / Preséntate: solo en Presentación del Curso (Sesión 01 = encuadre).
    # 4 Creatividad vs innovación
    table_content(
        prs, "CREATIVIDAD ≠ INNOVACIÓN",
        ["", "Creatividad", "Innovación"],
        [
            ["Pregunta", "¿Se me ocurre algo nuevo?", "¿Lo pongo en marcha y genera valor?"],
            ["Evidencia", "Idea, boceto, lluvia de ideas", "Prototipo usado / proceso cambiado / adopción"],
            ["Riesgo", "Quedarse en “idea genial”", "No verificar si alguien lo necesita"],
        ],
        sub="Primera idea madre del curso",
        note="Sin implementación y sin valor → hay idea, **no** hay innovación.",
        idx=4, fs_body=13,
    )

    # 5 Analogía
    content_slide(prs, "ANALOGÍA DE LA RECETA", [
        "**Creatividad** = inventar la receta (la idea puede quedarse en un post-it).",
        "**Innovación** = cocinarla, servirla y que alguien la **pida de nuevo**.",
        "En Ingeniería abunda “tengo una app…” y falta “alguien la usó y le cambió el dolor”.",
        "Este curso apunta a lo segundo: **valor en uso**, no solo ingenio.",
    ], idx=5)

    # 6 Trabajo final día 1 (sin mapa U1–U8)
    content_slide(prs, "EL TRABAJO FINAL DESDE EL DÍA 1", [
        "Entregable conductor: **Propuesta de Innovación**.",
        "Hoy: **ficha de problema** (usuario + dolor + tipo tentativo + valor esperado).",
        "Si el problema queda claro ahora, el resto del curso tiene hacia dónde empujar.",
        "Tipos Oslo (producto, proceso, organización, marketing, social): hoy solo **tentativo**.",
    ], idx=6)

    # 7 Oslo preview
    table_content(
        prs, "TIPOS DE INNOVACIÓN (vista previa · Oslo / OCDE)",
        ["Tipo", "Pregunta guía", "Ejemplo en Ingeniería"],
        [
            ["Producto", "¿Qué nuevo bien/servicio?", "Módulo/app con valor de uso"],
            ["Proceso", "¿Cómo entrego distinto?", "Automatizar pruebas / despliegues"],
            ["Organización", "¿Cómo nos coordinamos?", "Nuevo flujo de roles en un equipo"],
            ["Marketing", "¿Cómo llego/posiciono?", "Nuevo canal de adopción"],
            ["Social", "¿Qué impacto comunitario?", "Solución con bien público medible"],
        ],
        sub="Hoy solo eligen un tipo tentativo — se profundiza más adelante",
        note="Innovación ≠ gadget. Puede ser proceso u organización sin hardware nuevo.",
        idx=7, fs_body=12,
    )

    # 8 Ejemplo modelado
    content_slide(prs, "EJEMPLO MODELADO — Ficha de problema", [
        "**Título tentativo:** Reserva clara de laboratorio de Ingeniería.",
        "**Usuario:** estudiantes que reservan equipos de laboratorio.",
        "**Problema:** llegan y el equipo está ocupado / sin rastro de quién lo pidió; pierden 40–60 min.",
        "**Evidencia / síntoma:** tiempo perdido, frustración, subuso de equipos.",
        "**Tipo tentativo:** proceso (flujo) + posible producto (módulo de reserva).",
        "**Valor esperado:** menos tiempo muerto y mejor uso de recursos.",
        "Ojo: esto es el **marco del problema**, aún no la solución final.",
    ], idx=8, size=15)

    # 9 Taller
    content_slide(prs, "TALLER — Ficha problema–oportunidad (18 min)", [
        "Completen en clase estos **6 campos**:",
        "1. Título tentativo · 2. Usuario concreto · 3. Problema (3–5 líneas)",
        "4. Evidencia o síntoma observable · 5. Tipo de innovación tentativo",
        "6. Una frase de **valor esperado**",
        "**Criterio de éxito:** si alguien externo entiende el dolor sin pedir aclaración, sirve.",
        "Al final: **3 personas** leen solo usuario + problema (30 s c/u).",
    ], idx=9, size=15)

    # 10 Autónomo (sin fechas de calendario)
    content_slide(prs, "PARA CONTINUAR — trabajo autónomo", [
        "Suban la ficha a CDigital: `S01_FichaProblema_Apellido`.",
        "Mejoren el problema con **una observación real** (dato, foto o frase de un usuario).",
        "Traigan a la Sesión 02 una lista de **3 bloqueadores personales** que les impiden crear.",
    ], idx=10)

    # 11 Cierre
    closing_slide(
        prs, "Cierre — Sesión 01",
        [
            "Creatividad genera · Innovación implementa con valor",
            "Hilo: Propuesta de Innovación (insumo #1 = ficha de hoy)",
            "Próxima: Inteligencia emocional, creatividad e innovación",
        ],
        accent="Mismo Meet · mismo horario semanal",
    )

    out = _out_path()
    prs.save(out)
    print("OK", out, "slides", len(prs.slides))


if __name__ == "__main__":
    build()
