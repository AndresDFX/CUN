# -*- coding: utf-8 -*-
"""Modelo de evaluación y ventanas de los 5 cursos CUN — **tablas explícitas**.

FUENTE DE VERDAD: el **libro de calificaciones de cada aula en CDigital**, auditado el
2026-08-10 (ver «AUDITORIA CDigital 2026-08-10.md» §2). Cada ítem de ``ACA_COMPONENTES``
existe en el gradebook del aula con ESE nombre (``code``), ESE tipo de actividad
(``kind``: cuestionario / tarea / foro) y ESE peso (``weight``) dentro de su corte.

Aquí **NO se recalcula nada**: no hay reparto por pesos, ni «snap» al día de clase, ni
derivación desde recepción/cierre. Las ventanas viven en tablas escritas a mano
(``VENTANAS`` y ``VENTANAS_POR_GRUPO``) y solo se cambian editando esas tablas.

Lo que esto corrige del modelo anterior (que sí calculaba):
  · Existen **quices y parciales** y pesan mucho (Parcial 1 = 24%): antes no existían.
  · En pregrado hay **una sola «ACA Final»** (Tarea) en el tercer corte. No hay
    ACA 1 / ACA 2 / ACA 3 como tres entregables.
  · **Autoevaluación y coevaluación existen en los 5 cursos**, no solo en Proyecto I;
    la **coevaluación es un FORO** (se participa), no un cuestionario.
  · TG3 **no** es «corte único 100% (EV05/EXAM)»: son tres cortes 30/30/40.
  · Queda anulada la regla «cada ACA toma el 100% de su corte».
  · En Proyecto I el primer corte es un **Quiz** (25%), no la ACA de formulación.

Criterio con que el Docente fijó las ventanas (2026-08-10, no recalcular):
  1. La **fecha máxima de recepción de TRABAJOS** limita la **ACA Final** (documento),
     porque es un entregable documental.
  2. Los **quices y parciales** son cuestionarios: pueden correr hasta el cierre de
     notas y se ubican **en día de clase** (la ventana abre en la sesión anterior).
  3. La **Sesión 01 es de encuadre** y no evalúa: ningún ítem cierra ahí.
  4. **Auto y coevaluación** van entre la última semana y el **cierre de notas**.
  5. **Proyecto I** usa las fechas OFICIALES de Coordinación (cronograma AFI): no se tocan.
  6. **TG3 varía por grupo**: 54450 recibe/cierra una semana antes que 54466 y 54467.

Uso:
  from fechas_entrega_aca import entregas_curso, fmt_entrega, blocks_para_slide
  python config/cursos/fechas_entrega_aca.py   # imprime la tabla de los 5 cursos
"""
from __future__ import annotations

import re
from dataclasses import dataclass, replace
from datetime import date, timedelta
from typing import Any

from carga_academica import curso, fmt_dmy, fmt_dmy_largo, load_carga

DIAS = ("lun", "mar", "mié", "jue", "vie", "sáb", "dom")

# Tipos de actividad tal como están creados (o deben crearse) en Moodle/CDigital.
KIND_CUESTIONARIO = "cuestionario"
KIND_TAREA = "tarea"
KIND_FORO = "foro"
KIND_LABEL = {
    KIND_CUESTIONARIO: "Cuestionario",
    KIND_TAREA: "Tarea",
    KIND_FORO: "Foro",
}

# Instrumentos individuales de cierre: se *diligencian* / se *participa*, no se
# entrega documento. Existen en los CINCO cursos (auditoría 2026-08-10).
IDS_INSTRUMENTO_CIERRE = ("auto", "coev")

# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGO DE ÍTEMS — copia fiel del libro de calificaciones de cada aula.
#   id      → identificador estable que usan builds / hitos / enunciados
#   code    → nombre EXACTO del ítem en Moodle
#   label   → etiqueta corta para slides y tablas
#   weight  → peso real sobre 100 (suma 100 por curso; verificado al final)
#   kind    → cuestionario | tarea | foro (tipo de actividad en el aula)
#   corte   → 1 | 2 | 3
ACA_COMPONENTES: dict[str, list[dict[str, Any]]] = {
    # PROYECTO I 54ES4 (ESP329) — estructura propia 25 / 25 / 50.
    "proyecto1": [
        {"id": "quiz", "code": "Quiz", "label": "Quiz",
         "weight": 25, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "aca1", "code": "ACA 1", "label": "ACA 1",
         "weight": 25, "kind": KIND_TAREA, "corte": 2},
        {"id": "aca_final", "code": "ACA FINAL", "label": "ACA FINAL",
         "weight": 42, "kind": KIND_TAREA, "corte": 3},
        {"id": "auto", "code": "Autoevaluación", "label": "Autoevaluación",
         "weight": 4, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "coev", "code": "Coevaluación", "label": "Coevaluación",
         "weight": 4, "kind": KIND_FORO, "corte": 3},
    ],
    # INVESTIGACIÓN 53339 — pregrado 30 / 30 / 40.
    "investigacion": [
        {"id": "quiz1", "code": "Quiz 1", "label": "Quiz 1",
         "weight": 6, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "parcial1", "code": "Parcial 1", "label": "Parcial 1",
         "weight": 24, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "quiz2", "code": "Quiz 2", "label": "Quiz 2",
         "weight": 9, "kind": KIND_CUESTIONARIO, "corte": 2},
        {"id": "parcial2", "code": "Parcial 2", "label": "Parcial 2",
         "weight": 21, "kind": KIND_CUESTIONARIO, "corte": 2},
        {"id": "aca_final", "code": "ACA Final", "label": "ACA Final",
         "weight": 32.8, "kind": KIND_TAREA, "corte": 3},
        {"id": "quiz3", "code": "Quiz 3", "label": "Quiz 3",
         "weight": 4, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "auto", "code": "Autoevaluación", "label": "Autoevaluación",
         "weight": 1.6, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "coev", "code": "Coevaluación", "label": "Coevaluación",
         "weight": 1.6, "kind": KIND_FORO, "corte": 3},
    ],
    # CREATIVIDAD 54408 — pregrado 30 / 30 / 40 (mismos pesos que Investigación).
    "creatividad": [
        {"id": "quiz1", "code": "Quiz 1", "label": "Quiz 1",
         "weight": 6, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "parcial1", "code": "Parcial 1", "label": "Parcial 1",
         "weight": 24, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "quiz2", "code": "Quiz 2", "label": "Quiz 2",
         "weight": 9, "kind": KIND_CUESTIONARIO, "corte": 2},
        {"id": "parcial2", "code": "Parcial 2", "label": "Parcial 2",
         "weight": 21, "kind": KIND_CUESTIONARIO, "corte": 2},
        {"id": "aca_final", "code": "ACA Final", "label": "ACA Final",
         "weight": 32.8, "kind": KIND_TAREA, "corte": 3},
        {"id": "quiz3", "code": "Quiz 3", "label": "Quiz 3",
         "weight": 4, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "auto", "code": "Autoevaluación", "label": "Autoevaluación",
         "weight": 1.6, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "coev", "code": "Coevaluación", "label": "Coevaluación",
         "weight": 1.6, "kind": KIND_FORO, "corte": 3},
    ],
    # TG2 54448 — pregrado 30 / 30 / 40 (confirmado en el aula, ya no «orientativo»).
    "tg2": [
        {"id": "quiz1", "code": "Quiz 1", "label": "Quiz 1",
         "weight": 6, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "parcial1", "code": "Parcial 1", "label": "Parcial 1",
         "weight": 24, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "quiz2", "code": "Quiz 2", "label": "Quiz 2",
         "weight": 9, "kind": KIND_CUESTIONARIO, "corte": 2},
        {"id": "parcial2", "code": "Parcial 2", "label": "Parcial 2",
         "weight": 21, "kind": KIND_CUESTIONARIO, "corte": 2},
        {"id": "aca_final", "code": "ACA Final", "label": "ACA Final",
         "weight": 32.8, "kind": KIND_TAREA, "corte": 3},
        {"id": "quiz3", "code": "Quiz 3", "label": "Quiz 3",
         "weight": 4, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "auto", "code": "Autoevaluación", "label": "Autoevaluación",
         "weight": 1.6, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "coev", "code": "Coevaluación", "label": "Coevaluación",
         "weight": 1.6, "kind": KIND_FORO, "corte": 3},
    ],
    # TG3 54450 / 54466 / 54467 — igual estructura, pero ACA Final 32% y
    # auto/coevaluación 2% cada una (así está en las tres aulas).
    "tg3": [
        {"id": "quiz1", "code": "Quiz 1", "label": "Quiz 1",
         "weight": 6, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "parcial1", "code": "Parcial 1", "label": "Parcial 1",
         "weight": 24, "kind": KIND_CUESTIONARIO, "corte": 1},
        {"id": "quiz2", "code": "Quiz 2", "label": "Quiz 2",
         "weight": 9, "kind": KIND_CUESTIONARIO, "corte": 2},
        {"id": "parcial2", "code": "Parcial 2", "label": "Parcial 2",
         "weight": 21, "kind": KIND_CUESTIONARIO, "corte": 2},
        {"id": "aca_final", "code": "ACA Final", "label": "ACA Final",
         "weight": 32, "kind": KIND_TAREA, "corte": 3},
        {"id": "quiz3", "code": "Quiz 3", "label": "Quiz 3",
         "weight": 4, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "auto", "code": "Autoevaluación", "label": "Autoevaluación",
         "weight": 2, "kind": KIND_CUESTIONARIO, "corte": 3},
        {"id": "coev", "code": "Coevaluación", "label": "Coevaluación",
         "weight": 2, "kind": KIND_FORO, "corte": 3},
    ],
}

# Peso declarado de cada corte en el aula (se verifica contra la suma de sus ítems).
PESOS_CORTE: dict[str, dict[int, float]] = {
    "proyecto1": {1: 25, 2: 25, 3: 50},
    "investigacion": {1: 30, 2: 30, 3: 40},
    "creatividad": {1: 30, 2: 30, 3: 40},
    "tg2": {1: 30, 2: 30, 3: 40},
    "tg3": {1: 30, 2: 30, 3: 40},
}

REGLA_RESUMEN = (
    "Estructura, tipo de actividad y pesos = libro de calificaciones del aula en CDigital "
    "(auditoría 2026-08-10). Las ventanas son tablas explícitas de "
    "config/cursos/fechas_entrega_aca.py: no se recalculan por pesos."
)

# ─────────────────────────────────────────────────────────────────────────────
# PROYECTO I — fechas OFICIALES de Coordinación (cronograma AFI). NO se tocan.
#
# Las fija la Coordinación de Gestión del Conocimiento en
# `Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf`. El mapeo contra el aula
# (auditoría 2026-08-10) es: 1.ª ventana → **Quiz** (25%, corte 1), 2.ª → **ACA 1**
# (25%, corte 2), 3.ª → **ACA FINAL** (42%, corte 3).
REGLA_OFICIAL_P1 = (
    "Fechas OFICIALES de Coordinación (Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf) "
    "sobre la estructura real del aula en CDigital: Quiz 25% (corte 1) · ACA 1 25% (corte 2) · "
    "ACA FINAL 42% + autoevaluación 4% + coevaluación 4% (corte 3). "
    "Cierre y registro de todas las notas: 22/11/2026."
)

REGLA_VENTANAS_DOCENTE = (
    "Ventanas fijadas por el Docente (2026-08-10) sobre la estructura real del aula en "
    "CDigital: los quices y parciales son cuestionarios y cierran en día de clase (la "
    "Sesión 01 es de encuadre y no evalúa); la ACA Final es una tarea y cierra en la fecha "
    "máxima de recepción de trabajos; auto y coevaluación van de la última semana al cierre "
    "de notas."
)

# ─────────────────────────────────────────────────────────────────────────────
# VENTANAS — tabla explícita por curso: id → (apertura, cierre, límite de nota docente)
# El comentario de cada línea dice en qué sesión cae el cierre.
VENTANAS: dict[str, dict[str, tuple[date, date, date]]] = {
    # PROYECTO I 54ES4 · recepción 14/11 · cierre de notas 22/11 (fechas de Coordinación)
    "proyecto1": {
        "quiz":      (date(2026, 8, 3), date(2026, 8, 30), date(2026, 9, 7)),
        "aca1":      (date(2026, 9, 7), date(2026, 10, 4), date(2026, 10, 12)),
        "aca_final": (date(2026, 10, 12), date(2026, 11, 8), date(2026, 11, 16)),
        "coev":      (date(2026, 11, 9), date(2026, 11, 15), date(2026, 11, 22)),
        "auto":      (date(2026, 11, 16), date(2026, 11, 22), date(2026, 11, 22)),
    },
    # CREATIVIDAD 54408 · mié · recepción 19/09 · cierre de notas 27/09
    "creatividad": {
        "quiz1":     (date(2026, 8, 12), date(2026, 8, 19), date(2026, 8, 26)),   # cierra S02
        "parcial1":  (date(2026, 8, 20), date(2026, 8, 26), date(2026, 9, 2)),    # cierra S03
        "quiz2":     (date(2026, 8, 27), date(2026, 9, 2), date(2026, 9, 9)),     # cierra S04
        "parcial2":  (date(2026, 9, 3), date(2026, 9, 9), date(2026, 9, 16)),     # cierra S05
        "quiz3":     (date(2026, 9, 10), date(2026, 9, 16), date(2026, 9, 23)),   # cierra S06
        "aca_final": (date(2026, 8, 12), date(2026, 9, 19), date(2026, 9, 27)),   # recepción
        "auto":      (date(2026, 9, 23), date(2026, 9, 27), date(2026, 9, 27)),
        "coev":      (date(2026, 9, 23), date(2026, 9, 27), date(2026, 9, 27)),
    },
    # INVESTIGACIÓN 53339 · jue · recepción 12/09 · cierre de notas 20/09
    "investigacion": {
        "quiz1":     (date(2026, 8, 13), date(2026, 8, 20), date(2026, 8, 27)),   # cierra S02
        "parcial1":  (date(2026, 8, 21), date(2026, 8, 27), date(2026, 9, 3)),    # cierra S03
        "quiz2":     (date(2026, 8, 28), date(2026, 9, 3), date(2026, 9, 10)),    # cierra S04
        "parcial2":  (date(2026, 9, 4), date(2026, 9, 10), date(2026, 9, 17)),    # cierra S05
        "aca_final": (date(2026, 8, 13), date(2026, 9, 12), date(2026, 9, 20)),   # recepción
        # Excepción a REGLA_VENTANAS_DOCENTE: el Quiz 3 NO cierra en día de clase.
        # La última sesión (S06, 17/09) cae DESPUÉS de la recepción del 12/09, así que
        # dejarlo en la S06 lo ponía a cerrar después del entregable final del corte.
        # Decisión del Docente (10/08/2026): todo el corte 3 cierra el 12/09 y la S06
        # queda como socialización y cierre, sin evaluación.
        "quiz3":     (date(2026, 9, 11), date(2026, 9, 12), date(2026, 9, 20)),   # con la ACA Final
        "auto":      (date(2026, 9, 17), date(2026, 9, 20), date(2026, 9, 20)),
        "coev":      (date(2026, 9, 17), date(2026, 9, 20), date(2026, 9, 20)),
    },
    # TG2 54448 · lun · recepción 14/11 · cierre de notas 22/11
    "tg2": {
        "quiz1":     (date(2026, 8, 24), date(2026, 8, 31), date(2026, 9, 7)),    # cierra S03
        "parcial1":  (date(2026, 9, 7), date(2026, 9, 14), date(2026, 9, 21)),    # cierra S05
        "quiz2":     (date(2026, 9, 21), date(2026, 9, 28), date(2026, 10, 5)),   # cierra S07
        "parcial2":  (date(2026, 9, 29), date(2026, 10, 5), date(2026, 10, 19)),  # cierra S08
        "quiz3":     (date(2026, 10, 19), date(2026, 10, 26), date(2026, 11, 9)),  # cierra S10
        "aca_final": (date(2026, 8, 10), date(2026, 11, 14), date(2026, 11, 22)),  # recepción
        "auto":      (date(2026, 11, 9), date(2026, 11, 22), date(2026, 11, 22)),
        "coev":      (date(2026, 11, 9), date(2026, 11, 22), date(2026, 11, 22)),
    },
    # TG3 · mar · quices y parciales IGUALES en los tres grupos.
    # ACA Final / auto / coevaluación varían por grupo → VENTANAS_POR_GRUPO.
    "tg3": {
        "quiz1":    (date(2026, 8, 18), date(2026, 8, 25), date(2026, 9, 1)),     # cierra S03
        "parcial1": (date(2026, 9, 8), date(2026, 9, 15), date(2026, 9, 22)),     # cierra S06
        "quiz2":    (date(2026, 9, 22), date(2026, 9, 29), date(2026, 10, 6)),    # cierra S08
        "parcial2": (date(2026, 10, 6), date(2026, 10, 13), date(2026, 10, 20)),  # cierra S10
        "quiz3":    (date(2026, 10, 20), date(2026, 10, 27), date(2026, 11, 3)),  # cierra S12
    },
}

# Overrides por grupo (mismo formato). TG3: 54450 recibe el 07/11 y cierra notas el
# 15/11; 54466 y 54467 reciben el 14/11 y cierran el 22/11.
#
# Auto y coevaluación cierran en la ÚLTIMA CLASE del grupo, no en el cierre de notas
# (decisión del Docente, 10/08/2026). Antes cerraban el mismo día del cierre
# institucional —y en domingo—, así que la coevaluación, que es un FORO y se valora a
# mano, no tenía ni un día para calificarse y registrarse. Cerrar en día de clase deja
# 5 días de margen y permite recordarlo en vivo. 54450 termina en la S14 (10/11) porque
# su curso cierra el 15/11; 54466 y 54467 llegan a la S15 (17/11).
VENTANAS_POR_GRUPO: dict[str, dict[str, dict[str, tuple[date, date, date]]]] = {
    "tg3": {
        "54450": {
            "aca_final": (date(2026, 8, 11), date(2026, 11, 7), date(2026, 11, 15)),
            "auto":      (date(2026, 11, 3), date(2026, 11, 10), date(2026, 11, 15)),   # S14
            "coev":      (date(2026, 11, 3), date(2026, 11, 10), date(2026, 11, 15)),   # S14
        },
        "54466": {
            "aca_final": (date(2026, 8, 11), date(2026, 11, 14), date(2026, 11, 22)),
            "auto":      (date(2026, 11, 10), date(2026, 11, 17), date(2026, 11, 22)),  # S15
            "coev":      (date(2026, 11, 10), date(2026, 11, 17), date(2026, 11, 22)),  # S15
        },
        "54467": {
            "aca_final": (date(2026, 8, 11), date(2026, 11, 14), date(2026, 11, 22)),
            "auto":      (date(2026, 11, 10), date(2026, 11, 17), date(2026, 11, 22)),  # S15
            "coev":      (date(2026, 11, 10), date(2026, 11, 17), date(2026, 11, 22)),  # S15
        },
    },
}

# Grupo cuyas fechas se usan cuando no se pide uno explícito (el mayoritario).
GRUPO_REFERENCIA = {"tg3": "54466"}

# De qué tabla salió cada curso (para la columna «Regla» y los textos al estudiante).
REGLA_POR_CURSO = {
    "proyecto1": REGLA_OFICIAL_P1,
    "creatividad": REGLA_VENTANAS_DOCENTE,
    "investigacion": REGLA_VENTANAS_DOCENTE,
    "tg2": REGLA_VENTANAS_DOCENTE,
    "tg3": REGLA_VENTANAS_DOCENTE,
}


# ─────────────────────────────────────────────────────────────────────────────
# Modelo
# ─────────────────────────────────────────────────────────────────────────────
def fmt_peso(weight: float) -> str:
    """`32.8 → '32,8%'` · `6 → '6%'` (coma decimal, como el material en español)."""
    s = f"{float(weight):.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",") + "%"


@dataclass(frozen=True)
class EntregaAca:
    """Un ítem del libro de calificaciones + su ventana."""

    id: str
    code: str
    label: str
    weight: float
    kind: str            # cuestionario | tarea | foro
    corte: int           # 1 | 2 | 3
    apertura: date
    entrega: date        # cierre del ítem en CDigital
    nota_docente: date | None
    grupo: str | None = None
    regla: str = REGLA_RESUMEN

    @property
    def weight_pct(self) -> str:
        return fmt_peso(self.weight)

    @property
    def tipo_label(self) -> str:
        return KIND_LABEL[self.kind]

    @property
    def es_instrumento_cierre(self) -> bool:
        """Autoevaluación / coevaluación: se diligencian o se participa, no se entregan."""
        return self.id in IDS_INSTRUMENTO_CIERRE

    @property
    def es_documento(self) -> bool:
        """Tarea = entregable documental (la ACA Final y las ACAs de Proyecto I)."""
        return self.kind == KIND_TAREA


def componentes_curso(key: str) -> list[dict[str, Any]]:
    """Catálogo de ítems del curso (orden del libro de calificaciones)."""
    return ACA_COMPONENTES[key]


def componente(key: str, item_id: str) -> dict[str, Any]:
    for c in ACA_COMPONENTES[key]:
        if c["id"] == item_id:
            return c
    raise KeyError(f"{key}/{item_id}")


def cortes_curso(key: str) -> list[int]:
    return sorted({int(c["corte"]) for c in ACA_COMPONENTES[key]})


def peso_corte(key: str, corte: int) -> float:
    return round(sum(float(c["weight"]) for c in ACA_COMPONENTES[key]
                     if int(c["corte"]) == corte), 6)


def desglose_corte_texto(key: str) -> str:
    """«Corte 1 30% = Quiz 1 6% + Parcial 1 24% · …» — para notas de slides y CSV."""
    partes = []
    for corte in cortes_curso(key):
        items = [c for c in ACA_COMPONENTES[key] if int(c["corte"]) == corte]
        detalle = " + ".join(f"{c['code']} {fmt_peso(c['weight'])}" for c in items)
        partes.append(f"Corte {corte} {fmt_peso(peso_corte(key, corte))} = {detalle}")
    return " · ".join(partes)


def _grupo_referencia(key: str) -> str | None:
    porg = VENTANAS_POR_GRUPO.get(key) or {}
    if not porg:
        return None
    return GRUPO_REFERENCIA.get(key) or sorted(porg)[0]


def _ventanas(key: str, grupo: str | None = None) -> dict[str, tuple[date, date, date]]:
    """Ventanas del curso, con el override del grupo aplicado si existe."""
    tabla = dict(VENTANAS[key])
    porg = VENTANAS_POR_GRUPO.get(key) or {}
    if porg:
        g = grupo if grupo in porg else _grupo_referencia(key)
        tabla.update(porg[g])
    return tabla


def entregas_para_grupo(key: str, grupo: str | None = None) -> list[EntregaAca]:
    """Ítems del curso (y grupo, si sus ventanas varían — TG3), en orden de gradebook."""
    tabla = _ventanas(key, grupo)
    regla = REGLA_POR_CURSO.get(key, REGLA_RESUMEN)
    porg = VENTANAS_POR_GRUPO.get(key) or {}
    etiqueta_grupo = grupo if (grupo and grupo in porg) else None
    out: list[EntregaAca] = []
    for c in ACA_COMPONENTES[key]:
        ap, cierre, nota = tabla[c["id"]]
        out.append(
            EntregaAca(
                id=c["id"],
                code=c["code"],
                label=c["label"],
                weight=float(c["weight"]),
                kind=c["kind"],
                corte=int(c["corte"]),
                apertura=ap,
                entrega=cierre,
                nota_docente=nota,
                grupo=etiqueta_grupo,
                regla=regla,
            )
        )
    return out


def entregas_curso(key: str) -> list[EntregaAca] | dict[str, list[EntregaAca]]:
    """Cursos con ventanas por grupo (TG3) → dict por grupo; el resto → lista."""
    c = curso(key)
    groups = list(c.get("groups") or [])
    if (VENTANAS_POR_GRUPO.get(key) or {}) and len(groups) > 1:
        return {g: entregas_para_grupo(key, g) for g in groups}
    return entregas_para_grupo(key)


def entrega_por_id(key: str, item_id: str, grupo: str | None = None) -> EntregaAca:
    """Un ítem por id. Sin ``grupo`` en cursos multi-ventana → grupo de referencia."""
    data = entregas_curso(key)
    if isinstance(data, dict):
        g = grupo or _grupo_referencia(key) or sorted(data)[0]
        items = data[g]
    else:
        items = data
    for e in items:
        if e.id == item_id:
            return e
    raise KeyError(f"{key}/{item_id}")


def fmt_entrega(d: date, *, largo: bool = True) -> str:
    return fmt_dmy_largo(d) if largo else fmt_dmy(d)


def _regla_sin_grupo(regla: str) -> str:
    """Quita el sufijo « Grupo NNNNN.» cuando el texto ya nombra varios grupos."""
    return re.sub(r"\s*Grupo\s+\S+\.\s*$", "", regla or "").strip()


def _sufijo_grupo(grupo: str | None) -> str:
    """« · Grupo 54450» / « · Grupos 54450 / 54466 / 54467» / «» (todos por igual)."""
    if not grupo:
        return ""
    etiqueta = "Grupos" if "/" in grupo else "Grupo"
    return f" · {etiqueta} {grupo}"


def texto_fecha_enunciado(e: EntregaAca, weekday: int) -> str:
    """Bloque markdown de fecha para el enunciado / instructivo del estudiante.

    El texto depende del **tipo real de actividad** en CDigital: una tarea se
    *entrega*, un cuestionario se *cierra*, un foro se *participa*. El paréntesis del
    día no afirma «día de clase» a ciegas: las ventanas de Proyecto I cierran en
    domingo (fechas de Coordinación) y su día de clase es lunes.
    """
    dia = DIAS[weekday]
    dia_real = DIAS[e.entrega.weekday()]
    g = _sufijo_grupo(e.grupo)
    if e.entrega.weekday() == weekday:
        parentesis = f"{dia_real} · día de clase"
    else:
        parentesis = (
            f"{dia_real} · fecha de cierre institucional; "
            f"el día de clase del curso es {dia}"
        )
    if e.es_instrumento_cierre:
        verbo = "participar en el foro" if e.kind == KIND_FORO else "diligenciarla"
        return (
            f"**Ventana para {verbo} (CDigital){g}:** {fmt_dmy(e.apertura)} – "
            f"{fmt_dmy(e.entrega)} (cierra **{fmt_dmy_largo(e.entrega)}**).\n\n"
            f"**Tipo en el aula:** {e.tipo_label} · **{e.weight_pct}** de la nota "
            f"(corte {e.corte}).\n\n"
            f"> {e.regla}"
        )
    if e.kind == KIND_CUESTIONARIO:
        return (
            f"**Cierre del cuestionario (CDigital){g}:** **{fmt_dmy_largo(e.entrega)}** "
            f"({parentesis}).\n\n"
            f"**Ventana:** apertura {fmt_dmy(e.apertura)} – cierre {fmt_dmy(e.entrega)} · "
            f"**{e.weight_pct}** de la nota (corte {e.corte}).\n\n"
            f"> {e.regla}"
        )
    return (
        f"**Fecha de entrega (CDigital){g}:** **{fmt_dmy_largo(e.entrega)}** "
        f"({parentesis}).\n\n"
        f"**Ventana:** apertura {fmt_dmy(e.apertura)} – cierre {fmt_dmy(e.entrega)} · "
        f"**{e.weight_pct}** de la nota (corte {e.corte}).\n\n"
        f"> {e.regla}"
    )


def texto_fecha_curso(key: str, item_id: str) -> str:
    """Texto de fecha para enunciado (TG3: lista por grupo si las ventanas divergen)."""
    c = curso(key)
    weekday = int(c["horario"]["weekday"])
    data = entregas_curso(key)
    if isinstance(data, dict):
        by_date: dict[date, list[str]] = {}
        sample: dict[date, EntregaAca] = {}
        for g, items in data.items():
            for e in items:
                if e.id != item_id:
                    continue
                by_date.setdefault(e.entrega, []).append(g)
                sample[e.entrega] = e
        if not by_date:
            raise KeyError(f"{key}/{item_id}")
        if len(by_date) == 1:
            # Misma fecha para todos los grupos: NO nominar a uno solo (un estudiante
            # de otro grupo concluiría que no le aplica).
            e = next(iter(sample.values()))
            todos = " / ".join(sorted(data.keys()))
            if len(data) > 1:
                e = replace(e, grupo=todos, regla=_regla_sin_grupo(e.regla))
            return texto_fecha_enunciado(e, weekday)
        _e0 = sample[sorted(by_date)[0]]
        titulo = (
            "**Ventanas (CDigital) según grupo:**"
            if _e0.es_instrumento_cierre
            else "**Fechas de cierre (CDigital) según grupo:**"
        )
        lines = [titulo, ""]
        for d in sorted(by_date):
            gs = " / ".join(sorted(by_date[d]))
            e = sample[d]
            lines.append(
                f"- **Grupos {gs}:** **{fmt_dmy_largo(d)}** "
                f"(ventana {fmt_dmy(e.apertura)} – {fmt_dmy(e.entrega)})"
            )
        lines.append("")
        lines.append(
            f"**Tipo en el aula:** {_e0.tipo_label} · **{_e0.weight_pct}** de la nota "
            f"(corte {_e0.corte}) · **Día de clase:** {DIAS[weekday]}."
        )
        lines.append("")
        lines.append(f"> {_regla_sin_grupo(_e0.regla)}")
        return "\n".join(lines)
    e = entrega_por_id(key, item_id)
    return texto_fecha_enunciado(e, weekday)


def blocks_para_slide(
    key: str,
    grupo: str | None = None,
    *,
    por_corte: bool = True,
) -> list[dict]:
    """Bloques ``{label, start, end, pct}`` para ``fechas_inicio_fin_slide``.

    Por defecto **una tarjeta por corte** (3 tarjetas): con 8 ítems por curso la
    slide de cronograma queda ilegible. ``por_corte=False`` devuelve ítem por ítem.
    """
    items = entregas_para_grupo(key, grupo)
    if not por_corte:
        return [
            {"label": e.label, "start": e.apertura, "end": e.entrega, "pct": e.weight_pct}
            for e in items
        ]
    blocks: list[dict] = []
    prev_fin: date | None = None
    for corte in cortes_curso(key):
        del_corte = [e for e in items if e.corte == corte]
        ini = min(e.apertura for e in del_corte)
        fin = max(e.entrega for e in del_corte)
        # La ACA Final abre el primer día del curso (es el producto acumulativo del
        # periodo), así que su apertura NO sirve como inicio del tercer corte: haría
        # que las tarjetas se solaparan. El inicio de la tarjeta se recorta al día
        # siguiente del cierre del corte anterior; la ventana completa del ítem sigue
        # publicada en su enunciado y en `resumen_tabla_markdown`.
        if prev_fin is not None and ini <= prev_fin:
            ini = prev_fin + timedelta(days=1)
        blocks.append(
            {
                "label": f"Corte {corte}",
                "start": ini,
                "end": fin,
                "pct": fmt_peso(peso_corte(key, corte)),
            }
        )
        prev_fin = fin
    return blocks


def blocks_tg3_slide() -> list[dict]:
    """TG3 en Presentación del Curso: grupo de referencia (54466 = mismo que 54467)."""
    return blocks_para_slide("tg3", _grupo_referencia("tg3"))


def regla_corta(e: EntregaAca) -> str:
    """Etiqueta breve del ORIGEN de la fecha (columna «Regla» de las tablas)."""
    r = e.regla or ""
    if r.startswith("Fechas OFICIALES de Coordinación"):
        return "oficial Coordinación (cronograma AFI)"
    if r.startswith("Ventanas fijadas por el Docente"):
        return "ventana docente (2026-08-10)"
    return "libro de calificaciones CDigital"


def resumen_tabla_markdown(key: str, *, con_nota: bool = True) -> str:
    """Tabla markdown del modelo de evaluación del curso (Manual del Docente / LEEME).

    Una fila por ítem del libro de calificaciones. En cursos con ventanas por grupo
    (TG3) las filas se compactan: solo se desglosa el ítem cuyas fechas divergen.
    """
    data = entregas_curso(key)
    lines = [
        "| Ítem | Tipo | Corte | Peso | Apertura | Cierre | Nota docente |",
        "| :--- | :--- | :---: | ---: | :--- | :--- | :--- |",
    ]
    reglas: list[str] = []

    def _fila(e: EntregaAca, etiqueta: str) -> str:
        return (
            f"| **{e.code}**{etiqueta} | {e.tipo_label} | {e.corte} | {e.weight_pct} | "
            f"{fmt_dmy(e.apertura)} | {fmt_dmy(e.entrega)} | "
            f"{fmt_dmy(e.nota_docente) if e.nota_docente else '—'} |"
        )

    if isinstance(data, dict):
        grupos = sorted(data)
        for comp in ACA_COMPONENTES[key]:
            por_firma: dict[tuple, list[str]] = {}
            muestra: dict[tuple, EntregaAca] = {}
            for g in grupos:
                e = next(x for x in data[g] if x.id == comp["id"])
                firma = (e.apertura, e.entrega, e.nota_docente)
                por_firma.setdefault(firma, []).append(g)
                muestra[firma] = e
            unico = len(por_firma) == 1
            for firma, gs in por_firma.items():
                e = muestra[firma]
                lines.append(_fila(e, "" if unico else f" ({' / '.join(gs)})"))
                if e.regla not in reglas:
                    reglas.append(e.regla)
    else:
        for e in data:
            lines.append(_fila(e, ""))
            if e.regla not in reglas:
                reglas.append(e.regla)

    lines.append("")
    lines.append(f"**Cortes:** {desglose_corte_texto(key)}.")
    if con_nota and reglas:
        lines.append("")
        for r in reglas:
            lines.append(f"> {r}")
    return "\n".join(lines)


def hitos_aca_rows(
    key: str,
    grupo: str | None = None,
    *,
    esencial: bool = True,
) -> list[tuple[str, date, str]]:
    """Filas (label, date, note) para el CSV de hitos docentes.

    Con ``esencial=True`` (default): solo deadlines — cierre del ítem y límite de
    nota; en auto/coevaluación, habilitar + cierre. Sin aperturas de tareas/quices.
    Las filas salen ordenadas por fecha.
    """
    items = entregas_para_grupo(key, grupo)
    rows: list[tuple[str, date, str]] = []
    for e in items:
        etiqueta = f"{e.tipo_label} · {e.weight_pct} · corte {e.corte}"
        if e.es_instrumento_cierre:
            verbo = "Habilitar el foro" if e.kind == KIND_FORO else "Habilitar la actividad"
            rows.append(
                (
                    f"{e.code} — ventana",
                    e.apertura,
                    f"{e.code} ({etiqueta}) · ventana {fmt_dmy(e.apertura)}–"
                    f"{fmt_dmy(e.entrega)}. {verbo} en CDigital.",
                )
            )
            rows.append((f"{e.code} — cierre", e.entrega, f"Cierre {e.code} ({etiqueta})."))
        else:
            if not esencial:
                rows.append(
                    (
                        f"{e.code} — apertura",
                        e.apertura,
                        f"Apertura {e.code} ({etiqueta}). Configurar en CDigital "
                        f"({e.tipo_label.lower()} + rúbrica o banco de preguntas).",
                    )
                )
            cierre_nota = (
                f"Cierre {e.code} ({etiqueta})."
                if e.es_documento
                else (
                    f"Cierre {e.code} ({etiqueta}). El ítem ya está en el libro de "
                    "calificaciones; verificar que la actividad exista en el aula."
                )
            )
            rows.append((f"{e.code} — cierre", e.entrega, cierre_nota))
        if e.nota_docente:
            rows.append(
                (
                    f"{e.code} — límite nota docente",
                    e.nota_docente,
                    f"Fecha límite de ingreso de la nota de {e.code} ({etiqueta}).",
                )
            )
    rows.sort(key=lambda r: r[1])
    return rows


def as_json_dict() -> dict:
    """Snapshot serializable de todo el modelo (docs / depuración)."""
    load_carga()
    out: dict[str, Any] = {"regla": REGLA_RESUMEN, "fuente": "CDigital · auditoría 2026-08-10",
                           "cursos": {}}

    def _item(e: EntregaAca) -> dict:
        return {
            "id": e.id,
            "code": e.code,
            "tipo": e.kind,
            "corte": e.corte,
            "weight": e.weight,
            "apertura": e.apertura.isoformat(),
            "entrega": e.entrega.isoformat(),
            "nota_docente": e.nota_docente.isoformat() if e.nota_docente else None,
        }

    for key in ACA_COMPONENTES:
        data = entregas_curso(key)
        if isinstance(data, dict):
            out["cursos"][key] = {g: [_item(e) for e in items] for g, items in data.items()}
        else:
            out["cursos"][key] = [_item(e) for e in data]
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Verificación del catálogo (corre al importar: los pesos deben sumar 100)
# ─────────────────────────────────────────────────────────────────────────────
def verificar_catalogo() -> None:
    """Falla ruidosamente si el modelo deja de ser coherente con el aula."""
    for key, comps in ACA_COMPONENTES.items():
        ids = [c["id"] for c in comps]
        if len(set(ids)) != len(ids):
            raise ValueError(f"{key}: ids repetidos en ACA_COMPONENTES → {ids}")
        total = round(sum(float(c["weight"]) for c in comps), 6)
        if total != 100.0:
            raise ValueError(
                f"{key}: los pesos suman {total} y deben sumar 100 "
                "(libro de calificaciones CDigital)"
            )
        for c in comps:
            if c["kind"] not in KIND_LABEL:
                raise ValueError(f"{key}/{c['id']}: kind desconocido {c['kind']!r}")
            if int(c["corte"]) not in (1, 2, 3):
                raise ValueError(f"{key}/{c['id']}: corte inválido {c['corte']!r}")
        for corte, peso in PESOS_CORTE[key].items():
            real = peso_corte(key, corte)
            if round(real, 6) != round(float(peso), 6):
                raise ValueError(
                    f"{key}: corte {corte} suma {real} pero el aula declara {peso}"
                )
        grupos: list[str | None] = list(VENTANAS_POR_GRUPO.get(key) or {}) or [None]
        for g in grupos:
            tabla = _ventanas(key, g)
            faltan = [i for i in ids if i not in tabla]
            if faltan:
                raise ValueError(f"{key} (grupo {g}): sin ventana para {faltan}")
            for i in ids:
                ap, cierre, nota = tabla[i]
                if not (ap <= cierre <= nota):
                    raise ValueError(
                        f"{key}/{i} (grupo {g}): ventana incoherente "
                        f"{ap} → {cierre} → nota {nota}"
                    )


verificar_catalogo()


def main() -> None:
    import json

    print(REGLA_RESUMEN)
    print()
    for key in ACA_COMPONENTES:
        c = curso(key)
        print(f"=== {key} · {c['titulo_corto']} ===")
        print(
            f"inicio={c['inicio']} recepcion={c['recepcion']} cierre={c['cierre']} "
            f"weekday={DIAS[c['horario']['weekday']]}"
        )
        print(resumen_tabla_markdown(key))
        print()
    print(json.dumps(as_json_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
