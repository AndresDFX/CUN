# -*- coding: utf-8 -*-
r"""Lleva el FORMULARIO OFICIAL DEL JURADO (5 criterios, escala 1-5) a los dos archivos
que el jurado sí abre: la **ficha de preparación** y la **hoja de respuestas**.

POR QUÉ EXISTE
    `formulario_jurado.py` escribió el formulario, con casilla propuesta y página que la
    sostiene, en los 13 `4 - Evaluacion.md`. Pero ese archivo es el **último** de la secuencia:
    se llena DESPUÉS de la sala y no tiene `.docx`. Los dos que de verdad se usan son:

      1 - Ficha de preparacion.(md|docx)   se LEE antes de entrar  → aquí va el precargado
                                            con su sustento, para poder defender la casilla
      2 - Hoja de respuestas.(md|docx)     se TIENE delante en sala → aquí va la escala
                                            `1 2 3 4 5` para rodear, criterio por criterio

    Sin este paso el formulario existía en el repositorio pero no en la mano del jurado.

LOS CINCO CRITERIOS Y SU DESCRIPCIÓN
    Son los del formulario que la Dirección le pide al jurado, cada uno con opciones
    **1 2 3 4 5**. La descripción de cada criterio va literal en `DESCRIPCIONES`; es la que
    define qué se está calificando y por eso se imprime completa en la ficha.

    Ninguno de los cinco califica la sustentación oral: los cinco se responden con el
    documento, así que las casillas vienen **precargadas** y en sala solo se confirman o se
    corrigen. Eso es lo que hace rendir los ~3 minutos que le tocan al Jurado 2.

    ⚠️ El 1-5 de este formulario **no** es la nota 0,1-5,0 del acta. La escala interna del
    jurado (dominio · claridad · coherencia · defensa) y los umbrales de la §8 de la ficha
    siguen mandando sobre la nota que se reporta.

FUENTE ÚNICA
    Las casillas y sus sustentos NO se reescriben aquí: se importan de `formulario_jurado.DATOS`.
    Si una casilla cambia, se cambia allí y se vuelve a correr este script. G-011 no tiene
    documento, así que en vez de un número lleva el protocolo de los dos escenarios.

Uso:
    python config/evaluaciones/formulario_en_fichas.py --simular    # no escribe nada
    python config/evaluaciones/formulario_en_fichas.py --confirmar  # md + docx de los 13
    python config/evaluaciones/formulario_en_fichas.py --confirmar --sin-docx
"""
from __future__ import annotations

import argparse
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "config", "slides"))

from formulario_jurado import CRITERIOS, DATOS, FICHAS, ORDEN  # noqa: E402

# Descripción literal de cada criterio, tal como la trae el formulario de la Dirección.
DESCRIPCIONES = [
    "Claridad, pertinencia y delimitación del problema de investigación, así como la coherencia "
    "y precisión de los objetivos propuestos, verificando su alineación con el propósito del "
    "estudio y su viabilidad investigativa.",
    "Solidez del sustento teórico del proyecto, la pertinencia y actualidad de las fuentes "
    "consultadas, y la capacidad de articular conceptos, enfoques y antecedentes que fundamenten "
    "adecuadamente la investigación.",
    "Correspondencia entre el enfoque metodológico, el tipo de estudio, las técnicas e "
    "instrumentos de recolección de información y la definición de la muestra, garantizando la "
    "coherencia interna del diseño investigativo.",
    "Calidad en la presentación, interpretación y análisis de los resultados obtenidos, así como "
    "la consistencia y pertinencia de las conclusiones en relación con los objetivos, la "
    "problemática y el marco teórico del estudio.",
    "Grado de alineación del proyecto con el campo disciplinar y los énfasis de la especialización "
    "cursada, así como su aporte potencial al desarrollo académico, profesional o investigativo "
    "del área.",
]

# Nombre corto para la hoja de sala, donde el espacio manda.
CORTOS = [
    "Problemática y objetivos",
    "Marco teórico y referentes",
    "Metodología, muestra y diseño",
    "Resultados y conclusiones",
    "Pertinencia disciplinar",
]

# Los dos escenarios de G-011 (sin documento). Copiados de la tabla de
# `formulario_jurado.BLOQUE_SIN_DOCUMENTO`, §3.2 — si allí cambian, aquí también, y la
# comprobación de abajo avisa si las sumas dejan de cuadrar con lo que dice esa tabla.
SIN_DOC_CON_ORDEN = (3, 2, 2, 2, 3)   # suma 12 / 25
SIN_DOC_SIN_CERRAR = (2, 1, 1, 1, 2)  # suma  7 / 25
assert sum(SIN_DOC_CON_ORDEN) == 12 and sum(SIN_DOC_SIN_CERRAR) == 7
assert max(SIN_DOC_CON_ORDEN) <= 3, "sin documento, ningún criterio pasa de 3"

LECTURA_ESCALA = (
    "**5** sobresaliente, sin reparos de fondo · **4** sólido, con reparos menores y declarados · "
    "**3** aceptable, con un reparo de fondo que el documento no resuelve · **2** deficiente: hay "
    "material, pero se contradice o no sostiene lo que afirma · **1** sin base verificable en el "
    "documento."
)

# ---------------------------------------------------------------------------
# Bloque para «1 - Ficha de preparacion.md» — se LEE antes de la sala
# ---------------------------------------------------------------------------

ANCLA_FICHA = "### 8.1 Formulario oficial del jurado"
CORTE_FICHA = "\n## 9. Observaciones administrativas"


def bloque_ficha(codigo: str, datos: dict) -> str:
    p = [
        f"{ANCLA_FICHA} — 5 criterios en escala 1–5\n\n",
        "> **Instrumento distinto de los cuatro criterios de arriba.** Son las cinco preguntas del "
        "formulario que la Dirección le pide al jurado, cada una con opciones **1 2 3 4 5**. "
        "**Ninguna califica la sustentación oral:** las cinco se responden con el documento, así "
        "que van precargadas con la página que las sostiene y en sala solo se confirman.\n>\n",
        f"> Lectura de la escala, fijada de antemano: {LECTURA_ESCALA}\n>\n",
        "> ⚠️ **Este 1–5 no es la nota del acta.** La nota que se reporta sale de los cuatro "
        "criterios y de los umbrales de esta §8. La casilla del formulario la marca el jurado "
        "humano; esto es una propuesta con página.\n\n",
    ]

    if datos.get("sin_documento"):
        p.append(
            "**No hay base documental para responderlo.** Este grupo no entregó trabajo de grado "
            "ni presentación a la carpeta de jurados (cero archivos, verificado el 15/08/2026), y "
            "los cinco criterios se responden con el documento. **No se inventa un número.** El "
            "formulario es de opción obligatoria, así que en sala hay que marcar algo: estas son "
            "las dos únicas lecturas sostenibles, y **ningún criterio pasa de 3 sin documento**, "
            "porque por encima de 3 la escala afirma calidad verificable.\n\n"
        )
        p.append("| # | Criterio | Si expone con orden y cierra sus objetivos | Si no cierra los objetivos |\n")
        p.append("|:-:|---|:-:|:-:|\n")
        for i, (crit, a, b) in enumerate(
            zip(CRITERIOS, SIN_DOC_CON_ORDEN, SIN_DOC_SIN_CERRAR), start=1
        ):
            p.append(f"| {i} | {crit} | **{a}** | **{b}** |\n")
        p.append("| | **Suma** | **12 / 25** | **7 / 25** |\n")
        p.append(
            "\n**En los dos escenarios, dejar escrito en el formulario y en el acta:** «respondido "
            "únicamente sobre la exposición oral; el grupo no entregó trabajo de grado ni "
            "presentación a la carpeta de jurados (verificado el 15/08/2026)». Sin esa constancia, "
            "un 2 parece un juicio sobre el trabajo cuando es la consecuencia de que no haya "
            "trabajo que leer.\n"
        )
        p.append("\n**Detalle completo y qué preguntarle a la Dirección:** `4 - Evaluacion.md`, §3.\n")
        return "".join(p)

    if datos.get("nota_cita"):
        p.append("> 📄 " + datos["nota_cita"] + "\n\n")

    respuestas = datos["respuestas"]
    suma = sum(v for v, _ in respuestas)

    for i, (valor, sustento) in enumerate(respuestas, start=1):
        p.append(f"**{i}. {CRITERIOS[i - 1]}** — propuesto **{valor}** / 5\n\n")
        # Cita en bloque, no cursiva con `*…*`: `guion_md_a_docx.add_inline` solo entiende
        # `**negrita**` y `` `código` ``, y dejaría los asteriscos a la vista en el .docx. El
        # bloque `>` sí sale en gris y cursiva, que es justo lo que distingue la redacción
        # oficial del criterio de mi propio análisis.
        p.append(f"> {DESCRIPCIONES[i - 1]}\n\n")
        p.append(f"{sustento}\n\n")

    p.append(f"**Suma propuesta: {suma} / 25.**\n\n")
    p.append(f"**Qué subiría una casilla en sala:** {datos['sube']}\n\n")
    p.append(f"**Qué la bajaría:** {datos['baja']}\n")
    return "".join(p)


# ---------------------------------------------------------------------------
# Bloque para «2 - Hoja de respuestas.md» — se TIENE delante en sala
# ---------------------------------------------------------------------------

ANCLA_HOJA = "## E · FORMULARIO OFICIAL DEL JURADO"
ESCALA = "1   ·   2   ·   3   ·   4   ·   5"


def bloque_hoja(codigo: str, datos: dict) -> str:
    """Sección E, al final de la hoja: es lo último que se llena y va a la Dirección."""
    p = [
        f"{ANCLA_HOJA} — 5 criterios, escala 1–5\n\n",
        "Instrumento **distinto** de los cuatro criterios de la §D: aquellos dan la **nota del "
        "acta**, estos cinco van al formulario de la Dirección y **no son notas**. Las cinco se "
        "responden con el documento, así que vienen **precargadas** desde la §8.1 de la ficha, "
        "que trae la página que sostiene cada casilla. En sala solo se confirma; si la "
        "sustentación cambia una, se tacha y se rodea otra.\n\n",
    ]

    if datos.get("sin_documento"):
        p.append(
            "⚠️ **Este grupo no entregó documento ni presentación** (cero archivos, verificado el "
            "15/08/2026). Los cinco criterios se responden con el escrito, así que **ninguno pasa "
            "de 3**: por encima de 3 la escala afirma calidad verificable, y aquí no hay qué "
            "verificar. Marcar por lo que se escuche y dejar la constancia de abajo.\n\n"
        )
        for i, (corto, a, b) in enumerate(
            zip(CORTOS, SIN_DOC_CON_ORDEN, SIN_DOC_SIN_CERRAR), start=1
        ):
            p.append(
                f"**{i}. {corto}** — rodear:   {ESCALA}   →   "
                f"con orden y objetivos cerrados **{a}**; si no, **{b}**\n\n"
            )
        p.append(
            "**Suma:  ______ / 25**   ·   escenarios de referencia: **12 / 25** si expone con "
            "orden y cierra sus objetivos, **7 / 25** si no los cierra.\n\n"
        )
        p.append(
            "**Constancia obligatoria en el formulario y en el acta, copiar tal cual:** "
            "«respondido únicamente sobre la exposición oral; el grupo no entregó trabajo de grado "
            "ni presentación a la carpeta de jurados (verificado el 15/08/2026)». Sin esa frase, "
            "un 2 se lee como juicio sobre el trabajo, y el hallazgo es que no hay trabajo que "
            "leer.\n"
        )
        return "".join(p)

    respuestas = datos["respuestas"]
    suma = sum(v for v, _ in respuestas)
    for i, (valor, _sustento) in enumerate(respuestas, start=1):
        p.append(
            f"**{i}. {CORTOS[i - 1]}** — rodear:   {ESCALA}   →   precargado **{valor}**\n\n"
        )
    p.append(f"**Suma:  ______ / 25**   ·   precargada: **{suma} / 25**\n\n")
    # La razón va en la MISMA línea del rótulo: una línea de solo guiones bajos es una regla
    # horizontal en markdown y el renderer a .docx la descarta.
    p.append(
        "**Si cambio una casilla, la razón en una línea** (la §8.1 trae el sustento del "
        "precargado):   ______________________________________________________\n"
    )
    return "".join(p)


# ---------------------------------------------------------------------------
# Inyección
# ---------------------------------------------------------------------------

def _inyectar(ruta: str, ancla: str, corte: str, nuevo: str) -> tuple[str | None, str]:
    """Devuelve (texto nuevo o None si no cambia, mensaje)."""
    with open(ruta, encoding="utf-8") as fh:
        original = fh.read()
    if corte not in original:
        return None, f"no encontré el corte «{corte.strip()[:40]}»"
    fin = original.index(corte)
    if ancla in original:
        ini = original.index(ancla)
        if ini > fin:
            return None, "el ancla quedó después del corte: revisar a mano"
        salida = original[:ini] + nuevo + original[fin:]
        accion = "reemplazado"
    else:
        salida = original[:fin] + "\n" + nuevo + original[fin:]
        accion = "insertado"
    if salida == original:
        return None, "sin cambios"
    return salida, accion


def _anexar(ruta: str, ancla: str, nuevo: str) -> tuple[str | None, str]:
    """Igual que `_inyectar`, pero la sección va al FINAL: se reemplaza la cola."""
    with open(ruta, encoding="utf-8") as fh:
        original = fh.read()
    if ancla in original:
        salida = original[: original.index(ancla)].rstrip("\n") + "\n\n" + nuevo
        accion = "reemplazada"
    else:
        salida = original.rstrip("\n") + "\n\n" + nuevo
        accion = "añadida"
    if salida == original:
        return None, "sin cambios"
    return salida, accion


def procesar(codigo: str, datos: dict, simular: bool) -> list[str]:
    carpeta = os.path.join(FICHAS, datos["carpeta"])
    msgs = []

    ficha = os.path.join(carpeta, "1 - Ficha de preparacion.md")
    if not os.path.exists(ficha):
        msgs.append(f"  ⛔ {codigo}: falta {os.path.basename(ficha)}")
    else:
        salida, accion = _inyectar(ficha, ANCLA_FICHA, CORTE_FICHA, bloque_ficha(codigo, datos))
        if salida and not simular:
            with open(ficha, "w", encoding="utf-8") as fh:
                fh.write(salida)
        msgs.append(f"  {'✓' if salida else '='} {codigo} ficha  · §8.1 {accion}")

    hoja = os.path.join(carpeta, "2 - Hoja de respuestas.md")
    if not os.path.exists(hoja):
        msgs.append(f"  ⛔ {codigo}: falta {os.path.basename(hoja)}")
    else:
        salida, accion = _anexar(hoja, ANCLA_HOJA, bloque_hoja(codigo, datos))
        if salida and not simular:
            with open(hoja, "w", encoding="utf-8") as fh:
                fh.write(salida)
        msgs.append(f"  {'✓' if salida else '='} {codigo} hoja   · §E {accion}")
    return msgs


def rehacer_docx(datos: dict) -> list[str]:
    import guion_md_a_docx

    out = []
    carpeta = os.path.join(FICHAS, datos["carpeta"])
    for nombre in ("1 - Ficha de preparacion", "2 - Hoja de respuestas"):
        md = os.path.join(carpeta, nombre + ".md")
        if not os.path.exists(md):
            continue
        docx = os.path.join(carpeta, nombre + ".docx")
        guion_md_a_docx.convert(md, docx, brand=True)
        out.append(f"    docx {nombre}")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--simular", action="store_true", help="no escribe nada (por defecto)")
    ap.add_argument("--confirmar", action="store_true", help="escribe los archivos")
    ap.add_argument("--sin-docx", action="store_true", help="solo .md, no rehace .docx")
    args = ap.parse_args(argv)
    simular = not args.confirmar

    print(f"{'SIMULACIÓN' if simular else 'ESCRITURA'} · {len(ORDEN)} grupos\n")
    for codigo in ORDEN:
        datos = DATOS[codigo]
        for m in procesar(codigo, datos, simular):
            print(m)
        if args.confirmar and not args.sin_docx:
            for m in rehacer_docx(datos):
                print(m)

    if simular:
        print("\nNada escrito. Añada --confirmar para aplicar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
