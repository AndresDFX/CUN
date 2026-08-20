# -*- coding: utf-8 -*-
"""Abre el vocabulario del entregable en Trabajo de Grado 2 y 3.

EL PROBLEMA
    El material de TG2/TG3 hablaba de «el artículo» como si fuera la única modalidad de
    trabajo de grado posible. El Syllabus 94532 pide **dos** cosas —un documento escrito
    (cuya forma por defecto es el artículo resultado de investigación, ≥ 4.000 palabras y
    ≥ 50 referencias) y un **producto** que evidencie desempeño profesional—, y el material
    había colapsado las dos en una sola. Un estudiante que trae un proyecto aplicado, un
    prototipo, una sistematización o un emprendimiento no se veía representado en ninguna
    diapositiva.

LA CORRECCIÓN
    El entregable se nombra **«el documento»**. El esqueleto (introducción → referentes →
    metodología → resultados → discusión → conclusiones) es el mismo para cualquier
    modalidad: cambia el peso de las secciones y qué cuenta como «resultado», no la
    estructura ni los mínimos. El *artículo resultado de investigación* se sigue nombrando,
    pero como la **forma por defecto**, no como la única.

LOS TRES SENTIDOS DE «ARTÍCULO» — por qué esto no es un sed
    (A) el entregable del estudiante        → se abre    («el artículo» → «el documento»)
    (B) un paper publicado que se lee/cita  → SE CONSERVA (Scholar, SciELO, «artículo
        semilla», la lectura obligatoria de Arias Castrillón / Itriago y Zerpa, «no
        encontré artículos», «artículos de revistas académicas»…)
    (C) la palabra como TEMA de la frase    → SE CONSERVA («artículo es la forma por
        defecto, no la única», «este esqueleto no es «el del artículo»», «hablaba de «el
        artículo» como si fuera la única forma»). Son los bloques escritos a mano después
        de la primera barrida; abrirlos produce tautologías.
    Un reemplazo ciego rompe (B): dejaría a la Sesión 04 de TG2 buscando «documentos de
    revistas académicas» en Google Académico. Y rompe (C): dejaría la §1.1 de los manuales
    diciendo «el documento no es la única salida». Por eso las líneas de (B) y (C) se
    saltan enteras, y dentro de las que sí se procesan las `FRASES_INTACTAS` se
    **enmascaran** antes de aplicar las reglas y se restauran después.

    El script es **idempotente**: correrlo hoy reporta 0 cambios. Si vuelve a reportar
    cambios, mírelos uno por uno con `--ver` antes de confirmar — lo más probable es que
    sean prosa nueva del sentido (C) que falta proteger, no material por abrir.

FUERA DE ALCANCE (a propósito) — y quién sí se ocupa
    Los bancos de preguntas de `Docente/Cuestionarios/` **no** se tocan con este script. Sí
    hubo que abrirlos, porque citan literalmente las diapositivas, pero no con estas reglas:
    en un banco «el artículo» significa casi siempre la **lectura obligatoria** (Arias
    Castrillón, Itriago y Zerpa) y es el sujeto de la pregunta calificada («según el
    artículo»). Aplicar `REGLAS` ahí convierte 126 renglones en preguntas distintas y falsas.
    Los bancos los abre `sincronizar_bancos_con_decks.py`, con reglas ancladas a contexto
    explícito y una autoprueba de frases reales. Ya está aplicado (88 renglones, 9 archivos).

Uso:
    python config/cursos/abrir_modalidades_tg.py            # simula (no escribe)
    python config/cursos/abrir_modalidades_tg.py --confirmar
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# (B) Marcadores de «artículo = paper publicado». Una línea que empareje con
#     cualquiera de estos se deja intacta.
# ---------------------------------------------------------------------------
MARCADORES_PAPER = [
    r"art[ií]culo semilla",
    r"as[ií] sea un art[ií]culo famoso",
    r"art[ií]culos? de revistas",
    r"no encontr[ée]",
    r"no se encontraron art",
    r"A(?:bre|bra) un art[ií]culo",
    r"cita ese art",
    r"usaron ese art",
    r"referencias del propio art",
    r"resumen del art[ií]culo",
    r"Cito un art",
    r"Copi[ée] el m[ée]todo",
    r"frase perfecta en un art",
    r"cu[áa]ntos art[ií]culos",
    r"ley[óo] los art[ií]culos",
    r"(?:dos|tres|los)\s+\*{0,2}art[ií]culos",
    r"intitle:",
    r"citado por",
    r"art[ií]culo clave est[áa] detr[áa]s",
    r"aparece un art[ií]culo de 20",
    r"Ese art[ií]culo no le quita",
    r"no se lee el art[ií]culo completo",
    r"de un buen art[ií]culo salen",
    r"mejor art[ií]culo",
    r"bola de nieve",
    r"art[ií]culo se parece a su problema",
    r"art[ií]culo sobrevivi[óo]",
    r"art[ií]culo (?:muy )?citado",
    r"art[ií]culo sobre automatizaci[óo]n industrial",
    r"art[ií]culo que haya medido",
    r"metodolog[ií]a de un art[ií]culo",
    r"art[ií]culo escrito para investigacion",
    r"ficha del articulo",
    r"acceso abierto",
    r"acceso libre",
    r"publicable",
    r"Arias Castrill[óo]n",
    r"Itriago",
    r"un art[ií]culo de su [áa]rea",
    r"de un art[ií]culo salen otros",
    # Lectura autónoma de TG2: «El articulo distingue cuatro cosas…» es el paper de
    # Arias Castrillón, no el entregable. La línea no nombra al autor, así que se
    # protege por la frase.
    r"distingue cuatro cosas",
]
RE_PAPER = re.compile("|".join(MARCADORES_PAPER), re.IGNORECASE)

# ── Sentido (C): la línea HABLA DE la cuestión de la modalidad ────────────────────────
# Son los bloques escritos a mano *después* de la barrida (§1.1 de los dos manuales, el
# guion de la S01 y S03 de TG3, los bullets de los decks) que dicen justamente «artículo
# es la forma por defecto, no la única» o «esto no es el esqueleto del artículo». Ahí la
# palabra «artículo» ES el tema de la frase: sustituirla por «documento» produce
# tautologías —«el documento no es la única salida», «no es "el del documento", es el del
# trabajo de grado»—. Se saltan enteras, como las del sentido (B).
MARCADORES_MODALIDAD = [
    r"no es la (única|unica) (salida|modalidad)",
    r"forma por defecto",
    r"no es «el del art[ií]culo»",
    r"«el del art[ií]culo»",
    r"cualquier modalidad de grado",
    r"esta misma estructura sirve para cualqui",
    r"y no «del art[ií]culo»",
    r"no es «el del",
    r"«modalidad» ni «monograf[ií]a»",
    r"lista oficial de (opciones|modalidades)",
    # «hablaba de «el artículo» como si fuera la única forma»: describe el defecto que esta
    # misma barrida corrigió. Abrirlo lo deja diciendo que el problema era «el documento».
    r"como si fuera la [úu]nica",
    # «el de la S03 se llamaba «Estructura del documento / artículo de avance»»: cita un
    # nombre viejo a propósito, para explicar por qué la carpeta se renombró.
    r"se llamaba «",
]
RE_MODALIDAD = re.compile("|".join(MARCADORES_MODALIDAD), re.IGNORECASE)

# Frases que se conservan textuales aunque la línea sí se procese: la forma por
# defecto que nombra el Syllabus, y las citas textuales del Syllabus.
FRASES_INTACTAS = [
    "artículo resultado de investigación",
    "artículo derivado de un proceso de investigación-creación",
    "Artículo resultado de investigación",
]

# ---------------------------------------------------------------------------
# Reglas, en orden. Las multipalabra van primero.
# ---------------------------------------------------------------------------
REGLAS: list[tuple[str, str]] = [
    # --- títulos y rótulos de sesión -------------------------------------
    (r"Estructura del documento / art[ií]culo de avance", "Estructura del documento de avance"),
    (r"Estructura del documento art[ií]culo de avance", "Estructura del documento de avance"),
    (r"Estructura del art[ií]culo/documento", "Estructura del documento"),
    (r"Estructura del art[ií]culo", "Estructura del documento"),
    (r"estructura del art[ií]culo", "estructura del documento"),
    (r"Anatom[ií]a del art[ií]culo", "Anatomía del documento"),
    (r"anatom[ií]a del art[ií]culo", "anatomía del documento"),
    (r"Culminaci[óo]n formal del art[ií]culo", "Culminación formal del documento"),
    (r"Culminaci[óo]n del art[ií]culo", "Culminación del documento"),
    (r"Cierre del art[ií]culo", "Cierre del documento"),
    (r"cierre del art[ií]culo", "cierre del documento"),
    (r"escribir el art[ií]culo", "escribir el documento"),
    (r"Escribir el art[ií]culo", "Escribir el documento"),
    (r"proyecto/art[ií]culo", "proyecto/documento"),
    (r"art[ií]culo / proyecto de investigaci[óo]n", "documento de grado (artículo o proyecto)"),
    (r"art[ií]culo/sustentaci[óo]n", "documento/sustentación"),
    # --- genéricas --------------------------------------------------------
    (r"\bdel art[ií]culo\b", "del documento"),
    (r"\bDel art[ií]culo\b", "Del documento"),
    (r"\bal art[ií]culo\b", "al documento"),
    (r"\bAl art[ií]culo\b", "Al documento"),
    (r"\bel art[ií]culo\b", "el documento"),
    (r"\bEl art[ií]culo\b", "El documento"),
    (r"\bun art[ií]culo\b", "un documento"),
    (r"\bUn art[ií]culo\b", "Un documento"),
    (r"\bsu art[ií]culo\b", "su documento"),
    (r"\bSu art[ií]culo\b", "Su documento"),
    (r"\bmi art[ií]culo\b", "mi documento"),
    (r"\btu art[ií]culo\b", "tu documento"),
    (r"\bese art[ií]culo\b", "ese documento"),
    (r"\beste art[ií]culo\b", "este documento"),
    (r"\bEste art[ií]culo\b", "Este documento"),
    (r"\blos art[ií]culos\b", "los documentos"),
    (r"\bLos art[ií]culos\b", "Los documentos"),
    (r"\bart[ií]culos\b", "documentos"),
    (r"\bArt[ií]culos\b", "Documentos"),
    (r"\bart[ií]culo\b", "documento"),
    (r"\bArt[ií]culo\b", "Documento"),
    # --- ajustes de estilo tras el reemplazo ------------------------------
    # «este artículo se pregunta» es la frase modelo que el estudiante copia en su
    # introducción; «este trabajo se pregunta» es lo idiomático y sirve a cualquier
    # modalidad. «este documento se pregunta» suena a formulario.
    (r"este documento se pregunta", "este trabajo se pregunta"),
    (r"Un documento de resultados de investigaci[óo]n", "El documento de trabajo de grado"),
    # --- limpieza de colisiones ------------------------------------------
    (r"el mismo documento del documento", "el mismo documento"),
    (r"documento del documento", "documento"),
    (r"el documento, único documento que se sube", "el documento, lo único que se sube"),
    (r"documento de grado \(artículo o proyecto\) de investigación", "documento de grado (artículo o proyecto)"),
]
REGLAS_C = [(re.compile(p), r) for p, r in REGLAS]

# ---------------------------------------------------------------------------
# Qué se procesa. `rango` = (desde, hasta) 1-indexado inclusivo; None = todo.
# ---------------------------------------------------------------------------
OBJETIVOS: list[tuple[str, tuple[int, int] | None]] = [
    # generadores compartidos: SOLO el tramo de TG2/TG3
    ("config/slides/_regen_guiones_pregrado.py", (1141, 3939)),
    # decks
    *[(f"config/slides/content/cun_tg3_s{n:02d}.json", None) for n in range(1, 16)],
    ("config/slides/content/cun_tg2_s01.json", None),
    # documentos escritos a mano
    ("Pregrado/Trabajo de grado 2/Manual del Docente - Trabajo de Grado 2.md", None),
    ("Pregrado/Trabajo de grado 3/Manual del Docente - Trabajo de Grado 3.md", None),
    ("Pregrado/Trabajo de grado 2/HERRAMIENTAS_EXAMLAB.md", None),
    ("Pregrado/Trabajo de grado 3/HERRAMIENTAS_EXAMLAB.md", None),
    ("Pregrado/Trabajo de grado 2/Clases/Sesion 01 - Presentación del curso · docente · estudiantes · ACAs/Lectura autonoma - Sesion 01.txt", None),
    ("Pregrado/Trabajo de grado 3/Clases/Sesion 01 - Presentación del curso · docente · estudiantes · ACAs/Lectura autonoma - Sesion 01.txt", None),
]

RE_ART = re.compile(r"art[ií]culos?\b", re.IGNORECASE)


def procesar_linea(linea: str) -> str:
    """Aplica las reglas a una línea, salvo que sea del sentido (B) o (C)."""
    if not RE_ART.search(linea):
        return linea
    if RE_PAPER.search(linea) or RE_MODALIDAD.search(linea):
        return linea
    # Enmascara las frases que se conservan textuales.
    marcas: list[str] = []
    for frase in FRASES_INTACTAS:
        if frase in linea:
            token = f"\x00{len(marcas)}\x00"
            marcas.append(frase)
            linea = linea.replace(frase, token)
    for rx, rep in REGLAS_C:
        linea = rx.sub(rep, linea)
    for i, frase in enumerate(marcas):
        linea = linea.replace(f"\x00{i}\x00", frase)
    return linea


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--confirmar", action="store_true", help="escribe los archivos")
    ap.add_argument("--ver", action="store_true", help="muestra cada línea cambiada")
    args = ap.parse_args(argv)

    total_cambios = 0
    total_omitidas = 0
    total_intactas = 0
    for rel, rango in OBJETIVOS:
        p = RAIZ / rel
        if not p.exists():
            print(f"  !! no existe: {rel}", file=sys.stderr)
            continue
        original = p.read_text(encoding="utf-8")
        lineas = original.split("\n")
        desde, hasta = rango if rango else (1, len(lineas))
        cambios = 0
        omitidas = 0
        intactas = 0
        for i in range(desde - 1, min(hasta, len(lineas))):
            vieja = lineas[i]
            if not RE_ART.search(vieja):
                continue
            if RE_PAPER.search(vieja):
                omitidas += 1
                continue
            if RE_MODALIDAD.search(vieja):
                intactas += 1
                continue
            nueva = procesar_linea(vieja)
            if nueva != vieja:
                lineas[i] = nueva
                cambios += 1
                if args.ver:
                    print(f"    {i+1}- {vieja.strip()[:150]}")
                    print(f"    {i+1}+ {nueva.strip()[:150]}")
        if cambios:
            nuevo = "\n".join(lineas)
            if args.confirmar:
                p.write_text(nuevo, encoding="utf-8")
        estado = "escrito" if (cambios and args.confirmar) else ("simulado" if cambios else "sin cambios")
        residuo = len([1 for i, l in enumerate(lineas)
                       if RE_ART.search(l) and (desde - 1) <= i < min(hasta, len(lineas))])
        print(f"  {cambios:4} cambios · {omitidas:3} paper · {intactas:3} sobre la modalidad · "
              f"{residuo:3} líneas con «artículo» tras el paso  [{estado}]  {rel}")
        total_cambios += cambios
        total_omitidas += omitidas
        total_intactas += intactas

    print(f"\nTOTAL: {total_cambios} líneas cambiadas · {total_omitidas} intactas por ser paper "
          f"publicado (sentido B) · {total_intactas} intactas por hablar de la modalidad (sentido C)")
    if not args.confirmar:
        print("Simulación. Nada escrito. Añada --confirmar para aplicar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
