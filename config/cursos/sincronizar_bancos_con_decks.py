# -*- coding: utf-8 -*-
r"""Sincroniza los bancos de preguntas de TG2/TG3 con el vocabulario que ya tienen los decks.

EL PROBLEMA QUE RESUELVE
    `abrir_modalidades_tg.py` abrió el entregable en los decks y los manuales: «el artículo»
    pasó a ser «el documento». Los bancos de preguntas quedaron fuera de esa barrida a
    propósito. Pero los bancos **citan literalmente** las diapositivas —«Cita literal (deck
    de la Sesión 03)», «la tabla "Anatomía del artículo" de la misma sesión»— y esas citas
    quedaron mintiendo: dicen citar una diapositiva que ya no dice eso. Un estudiante que
    reclame con el deck en la mano tiene razón.

POR QUÉ NO SE REUSA EL MOTOR DE LOS DECKS
    Porque en los bancos «el artículo» significa casi siempre **la lectura obligatoria**
    (Arias Castrillón en TG2, Itriago y Zerpa en TG3), y ahí es el sujeto de la frase:

        «¿Qué exige exactamente esa descripción, según el artículo?»
        «Correcta. El artículo pide describir el espacio y el tiempo…»

    El motor genérico propone 126 líneas y convierte esas en «según el documento» — que en
    TG2/TG3 ya significa *el entregable del propio estudiante*. La pregunta calificada se
    vuelve otra pregunta, y falsa. Se probó en seco: no se aplica aquí.

CÓMO DISTINGUE UN SENTIDO DEL OTRO
    Por **contexto explícito, enumerado a mano**. Cada regla nombra las palabras que rodean
    a «artículo» y solo sustituye **esa palabra**; todo lo demás se conserva por
    retrorreferencia. No hay ninguna regla que dispare con «el artículo» a secas, que es
    justo como el banco nombra la lectura obligatoria. Añadir una rompería preguntas.

    Sustituir solo la palabra resuelve además dos cosas que una regla de frase completa no
    puede: el `.md` **parte las citas largas en dos renglones** («…y el artículo se le↵vuelve
    inmanejable») y el XML **mete etiquetas HTML dentro de la frase** («el cuerpo</strong>
    del artículo»). El separador `SEP` admite espacios, un salto de línea, `**` y etiquetas,
    y sale intacto porque nunca se reescribe.

    Y hay una autoprueba: `CENTINELAS_B` son frases reales de los bancos donde «artículo» es
    el paper que se lee, y ninguna regla puede tocarlas; `CENTINELAS_A` son frases reales del
    entregable, y todas tienen que cambiar. Si una regla se rompe o se pasa de lista, el
    script no corre.

LOS GEMELOS — y por qué no basta con leer el `.md`
    Cada banco es un `.md` legible y un `(Moodle XML).xml` que es el que se importa. Los dos
    están escritos a mano, y **se parafrasean**: no son el mismo texto. El Quiz 2 de TG3 dice
    el mismo distractor de dos formas —«con el artículo más avanzado» en una celda de tabla
    del `.md`, «cuando el artículo **esté** más avanzado» en prosa en el XML— y hay
    generalfeedbacks que solo existen en el XML («ni el mapa de lo que sigue en el
    artículo»). Una regla calcada del `.md` deja el XML a medias, que es el archivo que Moodle
    lee. Las reglas se aplican a los dos y se afinan mirando los dos.

    Lo que garantiza que no quedó nada sin abrir no es el recuento de cambios —una variante de
    mayúsculas o una paráfrasis se escapan sin ruido— sino `--residuo`, que lista cada
    «artículo» que sobrevive para confirmar a ojo que todos son el paper. Corra `--residuo`
    siempre, y léalo entero: es la única red que atrapa lo que las reglas no imaginaron.

LA PUERTA HACIA FUERA — esto escribe el repositorio, no CUN Digital
    Reimportar un banco vivo destruye los intentos en curso. Ventanas 2026-2:

        TG3 Quiz 1    18/08 → 25/08   ← ABIERTO. No reimportar hasta el 26/08.
        TG2 Quiz 1    24/08 → 31/08   ← reimportar ANTES del 24/08.
        TG3 Quiz 2    22/09 → 29/09       TG2 Quiz 2    21/09 → 28/09
        TG3 Parcial 1 08/09 → 15/09       TG2 Parcial 1 07/09 → 14/09
        TG3 Parcial 2 06/10 → 13/10       TG2 Parcial 2 29/09 → 05/10
        TG3 Quiz 3    20/10 → 27/10       TG2 Quiz 3    19/10 → 26/10

Uso:
    python config/cursos/sincronizar_bancos_con_decks.py             # simula
    python config/cursos/sincronizar_bancos_con_decks.py --ver       # simula y muestra el diff
    python config/cursos/sincronizar_bancos_con_decks.py --residuo   # qué «artículo» se queda
    python config/cursos/sincronizar_bancos_con_decks.py --confirmar
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(AQUI))

from abrir_modalidades_tg import RE_ART, RE_PAPER  # noqa: E402  (la red de seguridad)

CURSOS = ("Trabajo de grado 2", "Trabajo de grado 3")

# Separador tolerante: espacios, UN salto de línea (no un párrafo en blanco), los asteriscos
# de negrita del `.md` y las etiquetas inline del XML. Sale intacto porque va en un grupo.
SEP = r"(?:[^\S\n]|\n(?![^\S\n]*\n)|</?[a-z]+>|\*\*|·)+"
ART = r"[Aa]rt[ií]culo"

# ---------------------------------------------------------------------------
# Los contextos. Cada patrón captura TODO menos la palabra, y la palabra se sustituye
# conservando su mayúscula inicial. El orden no importa: los contextos no se solapan.
# ---------------------------------------------------------------------------
def _ctx(*, antes: str | None = None, despues: str | None = None) -> str:
    """Envuelve cada lado en `(?:…)`: sin eso la alternancia se come al separador."""
    if antes and despues:
        return rf"(\b(?:{antes}){SEP}){ART}({SEP}(?:{despues}))"
    if antes:
        return rf"(\b(?:{antes}){SEP}){ART}"
    return rf"{ART}({SEP}(?:{despues}))"


# Partes del entregable: «<sustantivo> del artículo». Ninguno de estos sustantivos precede
# nunca a la lectura obligatoria en estos bancos — a esa el banco la nombra «el artículo»,
# «del artículo» o «el resumen del artículo», sin una parte que la anteceda.
PARTES = (r"secci[óo]n(?:es)?|cuerpo|orden|[íi]ndice|prop[óo]sito|cierre|anatom[íi]a"
          r"|estructura|culminaci[óo]n formal|t[íi]tulo|resultados|metodolog[íi]a"
          r"|conclusi[óo]n|referencias en APA|ninguna parte")

CONTEXTOS: list[str] = [
    _ctx(antes=rf"(?:{PARTES}){SEP}del"),
    # ── posesivos y determinantes que apuntan al estudiante ────────────────────────────
    # «su artículo» es siempre el del estudiante: el banco nunca dice «su artículo» de
    # Itriago ni de Arias Castrillón, los nombra por apellido.
    _ctx(antes=r"su"),
    _ctx(antes=rf"entra{SEP}a{SEP}su|entra{SEP}al|en{SEP}todo{SEP}el"),
    _ctx(antes=rf"(?:escribir[áa]?|escribe|redactar[áa]?){SEP}el"),
    _ctx(antes=rf"(?:reportar{SEP}en{SEP}el|cierra{SEP}el)"),
    # «el mapa de lo que sigue en el artículo»: es la introducción del estudiante anunciando
    # su propio documento. La lectura obligatoria nunca se nombra así.
    _ctx(antes=rf"lo{SEP}que{SEP}sigue{SEP}en{SEP}el"),
    # ── frases hechas de los decks ─────────────────────────────────────────────────────
    _ctx(despues=r"en miniatura"),
    _ctx(despues=r"se le"),
    _ctx(despues=rf"se{SEP}vuelve{SEP}encontrable"),
    # El `esté` opcional es el gemelo XML del Quiz 2: el `.md` lo dice en una celda de tabla
    # («con el artículo más avanzado») y el XML en prosa («cuando el artículo esté más
    # avanzado»). Un paper publicado no se pone «más avanzado»; el entregable sí.
    _ctx(despues=rf"(?:est[ée]{SEP})?m[áa]s{SEP}avanzado"),
    _ctx(despues=r"completo"),        # «leer el artículo completo»
    _ctx(antes=r"en este", despues=r"se hablar"),
]
# IGNORECASE por el prefijo («Estructura» y «estructura» son el mismo rótulo). No afecta a la
# palabra sustituida: `_sustituir` decide la mayúscula leyendo lo que emparejó de verdad.
CONTEXTOS_C = [re.compile(p, re.IGNORECASE) for p in CONTEXTOS]

# El título de la S03 de TG2 pierde una palabra, así que no le sirve el motor de arriba.
# Una sola regla para las dos cajas: el `.md` lo rotula en mayúscula y la descripción de
# categoría del XML en minúscula, y con solo la mayúscula el gemelo XML se quedaba atrás.
RE_TITULO_TG2 = re.compile(rf"(structura del documento){SEP}/{SEP}{ART}({SEP}de{SEP}avance)")


def _sustituir(m: re.Match) -> str:
    """Reemplaza solo la palabra, conservando separadores y mayúscula inicial."""
    palabra = m.group(0)
    inicial = re.search(ART, palabra).group(0)[0]
    nueva = "Documento" if inicial.isupper() else "documento"
    grupos = [g for g in m.groups() if g is not None]
    if len(grupos) == 2:
        return grupos[0] + nueva + grupos[1]
    # Un solo grupo: puede ser el prefijo o el sufijo.
    return grupos[0] + nueva if palabra.startswith(grupos[0]) else nueva + grupos[0]


def procesar(texto: str) -> str:
    texto = RE_TITULO_TG2.sub(lambda m: m.group(1) + m.group(2), texto)
    for rx in CONTEXTOS_C:
        texto = rx.sub(_sustituir, texto)
    return texto


# ---------------------------------------------------------------------------
# Autoprueba. Frases reales de los bancos. Sin esto, una regla puede pasarse de lista
# meses después y no se notaría hasta que un estudiante reclame.
# ---------------------------------------------------------------------------
CENTINELAS_B = [  # «artículo» = el paper que se lee. NINGUNA puede cambiar.
    "¿Qué exige exactamente esa descripción, según el artículo?",
    "Correcta. El artículo pide describir el espacio y el tiempo en que se va a realizar",
    "Son los cuatro criterios del artículo, y el resultado de aplicarlos es una pregunta",
    "El artículo insiste en esa distinción: el formato es condición necesaria",
    "No dice qué se lleva, así que cualquier artículo del mundo cabría en esa línea.",
    "Me aporta el resumen del artículo, que copié tal cual",
    "Si no la toca, **no entra, así sea un artículo famoso**.",
    "Usted encontró un artículo muy citado, con autor, año y DOI.",
    "El artículo de Itriago y Zerpa alterna «condiciones» y «restricciones»",
    "La tabla resumen del artículo (p. 50) la ubica igual",
    "el artículo habla de «datos, metas, restricciones y operaciones»",
    "son vocabulario del artículo obligatorio que el estudiante ya leyó",
    "El artículo todavía tiene material sin usar en ninguno de los dos bancos",
    "el artículo enuncia el cuarto componente como «condiciones» en la p. 41",
    "Sí cuentan: artículos de revistas académicas, tesis y trabajos de grado",
    'Lo que **no** es limitación: "tuve poco tiempo", "no encontré artículos"',
    "sirve para encontrar más fuentes a partir de un artículo semilla",
    "son las cuatro distinciones reales del artículo, en el orden correcto",
    "La pregunta 01 sale del **artículo**, no de la presentación de encuadre.",
    "El artículo ejemplifica con drogadicción",
    "Que un artículo sea muy citado no lo vuelve pertinente para su pregunta",
    "las cuatro nociones que el artículo distingue al comienzo",
]
CENTINELAS_A = [  # «artículo» = el entregable. TODAS tienen que cambiar.
    "cada objetivo específico se convierte después en una sección del artículo",
    "Al buscar con Ctrl+F cada apellido en el cuerpo del artículo",
    "ese anexo <strong>no está referenciado desde el cuerpo</strong> del artículo",
    "va a escribir 7 secciones y el artículo se le vuelve inmanejable",
    "Está redactando la sección de **Resultados** de su artículo.",
    "| **Sesión 03** (25/08) — Estructura del artículo · taller de introducción",
    "el tema de la Sesión 03 (estructura del documento / artículo de avance sobre la plantilla",
    "| 03 | 31/08 | Estructura del documento / artículo de avance | **Sí** |",
    "El póster no es el artículo en miniatura",
    "como en «en este artículo se hablará de…»",
    "por eso el artículo se vuelve encontrable en repositorios",
    "la tabla «Anatomía del artículo» de la misma sesión",
    "esa fuente no entra a su artículo",
    "Una fuente citada una sola vez en todo el artículo",
    "el jurado quiera leer el artículo completo",
    "se resuelve más adelante, con el artículo más avanzado",
    "en la sección de Metodología del artículo. El jurado las busca.",
    "ya aparecen en el título del artículo",
    "una cifra sin punto de comparación no puede aparecer en ninguna parte del artículo",
    "ese es también el orden en que se escribirá el artículo",
    # la cita partida en dos renglones por el ancho del `.md`
    "va a escribir 7 secciones y el artículo se le\nvuelve inmanejable",
    # las dos frases que solo existen —o solo se redactan así— en el gemelo XML
    "ni el mapa de lo que sigue en el artículo",
    "se resuelve más adelante, cuando el artículo esté más avanzado",
]


def autoprueba() -> list[str]:
    fallos = []
    for frase in CENTINELAS_B:
        if procesar(frase) != frase:
            fallos.append(f"  ⛔ tocó una frase del paper: {frase[:78]}")
    for frase in CENTINELAS_A:
        if procesar(frase) == frase:
            fallos.append(f"  ⛔ no abrió una frase del entregable: {frase[:78]}")
    return fallos


# ---------------------------------------------------------------------------
def bancos() -> list[Path]:
    out: list[Path] = []
    for curso in CURSOS:
        base = RAIZ / "Pregrado" / curso / "Docente" / "Cuestionarios"
        out += sorted(base.glob("*.md")) + sorted(base.glob("*.xml"))
    return out


def texto_decks() -> str:
    """Todo el texto de los decks de TG2/TG3 y del generador de guiones, normalizado."""
    trozos = []
    for f in sorted((RAIZ / "config" / "slides" / "content").glob("cun_tg*.json")):
        trozos.append(json.dumps(json.load(open(f, encoding="utf-8")), ensure_ascii=False))
    trozos.append((RAIZ / "config" / "slides" / "_regen_guiones_pregrado.py").read_text(encoding="utf-8"))
    t = re.sub(r"<[^>]+>", " ", "\n".join(trozos))
    return re.sub(r"\s+", " ", t.replace("**", "")).lower()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--confirmar", action="store_true", help="escribe los archivos")
    ap.add_argument("--ver", action="store_true", help="muestra cada tramo, antes y después")
    ap.add_argument("--simular", action="store_true", help="no escribe nada (por defecto)")
    ap.add_argument("--residuo", action="store_true",
                    help="lista cada «artículo» que queda, para confirmar a ojo que es paper")
    args = ap.parse_args(argv)

    fallos = autoprueba()
    if fallos:
        print(f"AUTOPRUEBA · {len(fallos)} fallos. No se toca nada.", file=sys.stderr)
        print("\n".join(fallos), file=sys.stderr)
        return 1
    print(f"Autoprueba: {len(CENTINELAS_B)} frases del paper intactas · "
          f"{len(CENTINELAS_A)} frases del entregable abiertas ✓\n")

    total = 0
    tocados: dict[str, int] = {}
    residuos: list[tuple[str, int, str]] = []

    for ruta in bancos():
        original = ruta.read_text(encoding="utf-8")
        nuevo = procesar(original)

        # Red de seguridad: cada frase que RE_PAPER reconoce como paper publicado tiene que
        # seguir apareciendo, literal y las mismas veces. Se cuenta sobre todo el texto y no
        # por línea porque hay renglones con los dos sentidos: la descripción de categoría
        # del Parcial 1 de TG3 nombra el «artículo de Itriago y Zerpa (2011)» —que se queda—
        # y la «estructura del artículo» —que se abre— en el mismo renglón.
        perdidas = []
        for frase in {m.group(0) for m in RE_PAPER.finditer(original)}:
            if nuevo.count(frase) < original.count(frase):
                perdidas.append(frase)
        if perdidas:
            print(f"  ⛔ ABORTA · {ruta.name}: se perderían {perdidas}", file=sys.stderr)
            return 1

        cambios = 0
        if nuevo != original:
            viejas, nuevas = original.split("\n"), nuevo.split("\n")
            for i, (a, b) in enumerate(zip(viejas, nuevas)):
                if a == b:
                    continue
                cambios += 1
                if args.ver:
                    print(f"  {ruta.name} L{i+1}")
                    print(f"    - {a.strip()[:150]}")
                    print(f"    + {b.strip()[:150]}")
            if args.confirmar:
                ruta.write_text(nuevo, encoding="utf-8")
            clave = f"{ruta.parent.parent.parent.name} · {ruta.name.split(' - banco')[0]}"
            tocados[clave] = tocados.get(clave, 0) + cambios

        for i, l in enumerate(nuevo.split("\n")):
            for m in RE_ART.finditer(l):
                ini, fin = max(0, m.start() - 55), min(len(l), m.end() + 55)
                residuos.append((f"{ruta.parent.parent.parent.name[-1]} {ruta.name[:30]}",
                                 i + 1, l[ini:fin].strip()))

        residuo = sum(1 for l in nuevo.split("\n") if RE_ART.search(l))
        estado = "escrito" if (cambios and args.confirmar) else ("simulado" if cambios else "=")
        print(f"  {cambios:3} renglones · {residuo:3} con «artículo» tras el paso "
              f"[{estado:9}] {ruta.parent.parent.parent.name} / {ruta.name}")
        total += cambios

    if args.residuo:
        print(f"\nRESIDUO · {len(residuos)} «artículo» que se quedan. Todos deberían ser el "
              f"paper que se lee, no el entregable:")
        for arch, n, ctx in residuos:
            print(f"  {arch:34} L{n:<4} …{ctx}…")

    print(f"\nTOTAL: {total} renglones en {len(tocados)} archivos")
    print("\nCuestionarios que quedan desincronizados con CUN Digital hasta reimportar el banco:")
    for k, v in sorted(tocados.items()):
        print(f"  · {k}  ({v} renglones)")
    print("\n  ⚠️  TG3 Quiz 1 está ABIERTO (18/08 → 25/08). Reimportar el 26/08 o después.")
    print("  ⚠️  TG2 Quiz 1 abre el 24/08. Reimportar ANTES de esa fecha.")
    if not args.confirmar:
        print("\nSimulación. Nada escrito. Añada --confirmar para aplicar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
