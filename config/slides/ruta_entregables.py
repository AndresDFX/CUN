# -*- coding: utf-8 -*-
"""Diapositiva final de cada sesión: la RUTA DE ENTREGABLES del curso, **sin fechas**.

Se añade como última slide de contenido de **todas** las decks de sesión (justo antes del
cierre) para que el estudiante tenga siempre delante qué se le va a pedir y en qué punto
del curso. Responde a un pedido explícito: recordar los entregables y pendientes «de forma
genérica, para que en siguientes versiones del curso se aplique igual».

De ahí las dos reglas que gobiernan este archivo:

1. **Ninguna fecha.** Lo temporal se dice en número de sesión: «cierra en la semana de la
   Sesión 05». La ventana exacta vive en el enunciado (`Clases/Recursos/ACAs/`) y en
   CDigital, que es lo único que califica. Una fecha aquí quedaría vieja en el siguiente
   dictado y habría que reeditar 50 decks.
2. **Nada se escribe a mano dos veces.** El código del ítem, su tipo, su peso y su corte
   salen de `fechas_entrega_aca.py`; el número de sesión se **calcula** cruzando la fecha
   de cierre del ítem con el calendario de `sesiones_cun.py`. Cambia el calendario del
   próximo periodo y la ruta se recoloca sola. Lo único redactado a mano es la frase de
   «qué debes tener listo», y va anclada al `code` del ítem (ver `QUE_TENER_LISTO`).

    python config/slides/ruta_entregables.py          # imprime la ruta de los 5 cursos
    python config/slides/ruta_entregables.py --verificar
"""
from __future__ import annotations

import os
import sys
from datetime import date, datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.join(os.path.dirname(_HERE), "cursos")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fechas_entrega_aca import entregas_para_grupo  # noqa: E402
from sesiones_cun import COURSES  # noqa: E402

# ---------------------------------------------------------------------------
# Lo único redactado a mano: qué tiene que tener listo el estudiante para cada ítem.
#
# Anclado al `code` del ítem, no a su posición: si el libro de calificaciones del aula
# cambia de ítems, `verificar()` lo grita en el build en vez de imprimir la frase de otro
# entregable bajo el encabezado correcto (el mismo defecto que ya cazó `FOCOS_SESION` en
# `build_acas_estudiantes.py`).
#
# Redactadas contra el enunciado real de cada ítem —`Clases/Recursos/ACAs/*.docx`— y
# verificadas una por una el 19/08/2026: sin fechas, sin URL, sin número de grupo y sin
# requisitos que el enunciado no pida.
#
# Tampoco llevan número de sesión dentro de la frase. El primer borrador de Trabajo de
# grado 3 decía «Estudia las Sesiones 02 a 05»: cierto hoy y falso en cuanto el temario se
# reordene, que es exactamente lo que esta slide no puede permitirse. El alcance exacto de
# cada cuestionario ya lo calcula `build_acas_estudiantes._sesiones_evaluables()` y sale
# impreso en el enunciado del ítem; aquí va solo el contenido.
# ---------------------------------------------------------------------------
QUE_TENER_LISTO: dict[str, dict[str, str]] = {
    "proyecto1": {
        "Quiz": "Estudia **problema y pregunta** de investigación; resuélvelo dentro de su ventana.",
        "ACA 1": "Sube en **plantilla APA** problema, pregunta, objetivos, mínimo 6 antecedentes y los marcos.",
        "ACA FINAL": "Sube el anteproyecto integrado con las **correcciones** de la ACA 1, metodología y viabilidad.",
        "Autoevaluación": "Diligénciala tú, dentro de su ventana, según tu **participación real**.",
        "Coevaluación": "**Publica** tu propio aporte y valora hechos del trabajo del equipo, con respeto.",
    },
    "investigacion": {
        "Quiz 1": "Ten claras las **etapas del método** y qué es un artículo de nuevo conocimiento.",
        "Parcial 1": "Ten memorizadas las **6 líneas** de MinCiencias y en cuál se ubica tu tema, y por qué.",
        "Quiz 2": "Distingue **tipos de fuente** y qué la hace confiable: quién firma, dónde y de cuándo es.",
        "Parcial 2": "Domina problema, pregunta y objetivo, búsqueda con operadores y citas en **APA 7**.",
        "ACA Final": "Sube el **artículo consolidado**: problema, pregunta, marco, matriz de fuentes y APA 7.",
        "Quiz 3": "Ten claras las partes del **planteamiento** y qué es una revisión de literatura articulada.",
        "Autoevaluación": "Diligénciala tú, según tu **participación real** en el periodo.",
        "Coevaluación": "**Publica tu aporte**: valora con respeto hechos del trabajo del equipo, no personas.",
    },
    "creatividad": {
        "Quiz 1": "Ten leída la unidad del encuadre: **Propuesta de Innovación** e inteligencia emocional.",
        "Parcial 1": "Domina **Design Thinking**, dos técnicas de ideación, bloqueadores y ensanchadores.",
        "Quiz 2": "Suma el **Manual de Oslo**: qué cuenta como innovación y cómo se gestiona; el curso acumula.",
        "Parcial 2": "Tipifica tu innovación (producto, proceso, organización, marketing, social) y **justifícala**.",
        "ACA Final": "Sube la **propuesta consolidada**: problema, tipo Oslo, FODA, Canvas, MVP, vigilancia y pitch.",
        "Quiz 3": "Ten claros **FODA, Canvas y MVP** (verificable) y para qué sirve la vigilancia tecnológica.",
        "Autoevaluación": "Diligénciala tú, y solo tú, **con honestidad** sobre tu participación real.",
        "Coevaluación": "**Publica** tu aporte: valora hechos del trabajo en equipo, no a las personas.",
    },
    "tg2": {
        "Quiz 1": "Ten formulados **pregunta, objetivos y título** provisional.",
        "Parcial 1": "Repasa **estructura APA CUN** y antecedentes Fase I, más pregunta, objetivos y título.",
        "Quiz 2": "Distingue **marco teórico, conceptual y contextual** y cómo se articulan con tu pregunta.",
        "Parcial 2": "Repasa los tres marcos y el **diseño metodológico**: enfoque, tipo, alcance y diseño.",
        "Quiz 3": "Ten claros **instrumentos y plan de análisis** propuestos y la integración del avance.",
        "ACA Final": "Sube el **avance consolidado** en plantilla APA CUN, integrado y listo para TG3.",
        "Autoevaluación": "Diligénciala tú, de forma **individual**, valorando tu participación real.",
        "Coevaluación": "**Publica** tu aporte: valora hechos del trabajo del equipo, nunca a las personas.",
    },
    "tg3": {
        "Quiz 1": "Repasa **pregunta, objetivos y título** y las variables de la pregunta-problema.",
        "Parcial 1": "Estudia la **introducción**, los referentes Fase I y el instrumento ya diseñado.",
        "Quiz 2": "Estudia **comunidades de práctica**, co-creación y análisis de datos.",
        "Parcial 2": "Estudia el cierre del **marco teórico**, los resultados y la discusión.",
        "Quiz 3": "Ten claros **resumen**, palabras clave UNESCO, póster y verificación antiplagio.",
        "ACA Final": "Sube el **documento final** en plantilla APA CUN: mínimo 4.000 palabras y 50 referencias.",
        "Autoevaluación": "Diligénciala **tú**, dentro de su ventana, sobre tu participación real.",
        "Coevaluación": "**Publica** tu aporte dentro de la ventana: un borrador sin enviar no cuenta.",
    },
}

# Frase de reserva cuando un ítem nuevo todavía no tiene redacción propia. No inventa nada:
# dice lo único que es cierto de todos los ítems de su tipo.
_POR_TIPO = {
    "cuestionario": "Resuélvelo **en CDigital** dentro de su ventana; no se sube archivo.",
    "tarea": "Sube el documento en la **plantilla APA CUN** al espacio de la tarea.",
    "foro": "Participa en el **foro** valorando el trabajo de tus compañeros.",
}

ESTADO_CERRADO = "ya cerró"
ESTADO_ACTUAL = "cierra esta semana"
ESTADO_PENDIENTE = "pendiente"


def _fecha(s: dict) -> date:
    return datetime.strptime(s["fecha"], "%d/%m/%Y").date()


def _sesiones(course_key: str) -> list[dict]:
    return sorted(COURSES[course_key]["sesiones"], key=_fecha)


def ancla(course_key: str, cierre: date) -> int | None:
    """Número de la última sesión sincrónica que ocurre **antes o el día** del cierre.

    Es el ancla temporal de la ruta: en vez de «cierra el 27/09», la slide dice «cierra en
    la semana de la Sesión 05». Devuelve ``None`` si el ítem cierra antes de la primera
    sesión (no debería pasar; `verificar()` lo reporta).
    """
    previas = [s["n"] for s in _sesiones(course_key) if _fecha(s) <= cierre]
    return previas[-1] if previas else None


def ruta(course_key: str) -> list[dict]:
    """Los entregables del curso ordenados por el punto del curso en que cierran."""
    items = []
    for e in entregas_para_grupo(course_key):
        items.append({
            "id": e.id,
            "code": e.code,
            "tipo": e.tipo_label,
            "kind": e.kind,
            "peso": e.weight_pct,
            "corte": e.corte,
            "ancla": ancla(course_key, e.entrega),
            "que": (QUE_TENER_LISTO.get(course_key, {}).get(e.code)
                    or _POR_TIPO.get(e.kind, "")),
        })
    items.sort(key=lambda i: (i["ancla"] or 99, i["corte"], i["code"]))
    return items


def _estado(anclaje: int | None, n_actual: int) -> str:
    if anclaje is None or anclaje < n_actual:
        return ESTADO_CERRADO
    return ESTADO_ACTUAL if anclaje == n_actual else ESTADO_PENDIENTE


def filas(course_key: str, n_actual: int) -> list[list[str]]:
    """Filas de la tabla: (punto del curso + estado, ítem + tipo + peso, qué tener listo).

    El **tipo** va en la tabla, no dentro de la frase: es lo que distingue «resolver un
    cuestionario en el aula» de «subir un documento» o «publicar en un foro», sale derivado
    del libro de calificaciones y así ninguna frase tiene que gastar caracteres en repetirlo.
    """
    out = []
    for it in ruta(course_key):
        punto = f"Sesión {it['ancla']:02d}" if it["ancla"] else "antes de empezar"
        out.append([
            f"**{punto}** · {_estado(it['ancla'], n_actual)}",
            f"**{it['code']}** · {it['tipo']} · {it['peso']}",
            it["que"],
        ])
    return out


TITULO = "RUTA DE ENTREGABLES DEL CURSO"
SUB = ("Sin fechas a propósito: aquí va **en qué punto del curso** cierra cada ítem · "
       "la ventana exacta la fija CDigital")
NOTE = ("Esta misma tabla va al final de todas las sesiones. La **fecha** de cada ventana "
        "está en el enunciado del ítem (`Clases/Recursos/ACAs/`) y en el aula: si el aula y "
        "cualquier otro material se contradicen, **manda el aula**.")
_COL_W = [2.9, 2.9, 6.1]


def slide(prs, course_key: str, n_actual: int, idx: int | None = None):
    """Añade la slide de ruta a `prs`. Import perezoso del motor para no acoplar el CLI."""
    from cun_slides_engine import table_content
    return table_content(
        prs,
        TITULO,
        ["Cierra en la semana de…", "Entregable", "Qué debes tener listo"],
        filas(course_key, n_actual),
        sub=SUB,
        note=NOTE,
        col_w=_COL_W,
        idx=idx,
        fs_body=11,
    )


def verificar() -> list[str]:
    """Avisos para el build: ítems sin frase propia, frases huérfanas y anclas imposibles."""
    avisos: list[str] = []
    for key in COURSES:
        codes = set()
        for it in ruta(key):
            codes.add(it["code"])
            if it["code"] not in QUE_TENER_LISTO.get(key, {}):
                avisos.append(
                    f"{key}: «{it['code']}» no tiene frase en QUE_TENER_LISTO; se usó la "
                    f"genérica de tipo «{it['kind']}». Redáctala contra su enunciado."
                )
            if it["ancla"] is None:
                avisos.append(
                    f"{key}: «{it['code']}» cierra antes de la primera sesión del "
                    "calendario. Revisa la ventana en fechas_entrega_aca.py."
                )
        for code in QUE_TENER_LISTO.get(key, {}):
            if code not in codes:
                avisos.append(
                    f"HUÉRFANA — {key}: hay frase para «{code}» y ese ítem ya no está en el "
                    "libro de calificaciones. Bórrala o corrige el code."
                )
    return avisos


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    for key, c in COURSES.items():
        n = len(_sesiones(key))
        print(f"\n===== {c['titulo']}  ({n} sesiones)")
        for fila in filas(key, n_actual=1):
            print("   " + " | ".join(f.replace("**", "") for f in fila))
    avisos = verificar()
    print(f"\n{len(avisos)} avisos")
    for a in avisos:
        print("   ⚠ " + a)
    return 1 if ("--verificar" in argv and avisos) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
