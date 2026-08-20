# -*- coding: utf-8 -*-
r"""Mantiene las 3 preguntas de cada grupo idénticas en los tres sitios donde viven.

EL PROBLEMA
    Las tres preguntas que el Jurado 2 lee en voz alta están escritas tres veces: en la §5 de
    `1 - Ficha de preparacion.md`, en la §C de `2 - Hoja de respuestas.md` y en el bloque de la
    agenda de `00 - Indice y agenda de sustentaciones.md`. En sala se lee la de la hoja; la ficha
    es la que se preparó; el índice es lo que se repasa antes del turno. Si las tres no dicen
    exactamente lo mismo, se lee en voz alta una versión distinta de la que se preparó, y la
    respuesta se anota contra una pregunta que no se hizo.

LA FUENTE ES LA FICHA
    Manda la §6 de la ficha, el bloque «### 🎯 Las 3 que sí voy a preguntar». La hoja y el índice
    se rellenan desde ahí. Los rótulos de la hoja («**Pregunta 2 — El techo que fija su propia
    restricción**») y las notas `>` del índice NO se tocan: son del jurado, no del dato.

EL MARCADO ES DISTINTO EN CADA FICHA, A PROPÓSITO
    Unas fichas escriben la pregunta como `**1. …**`, otras como `**1) «…»**` y otras como cita en
    bloque `> «…»`. Se redactaron en tandas distintas y no merece la pena uniformarlas: lo que
    tiene que coincidir es la FRASE, no su tipografía. Por eso la comparación normaliza —quita
    negritas, comillas angulares y la numeración— y solo entonces exige igualdad carácter por
    carácter.

    Un bloque de pregunta se cierra en su `»`; si no viene entrecomillada, en el renglón vacío o en
    el primer bullet de comentario. Sin la regla del `»`, la tercera pregunta se come las notas `>`
    que van detrás y el script reporta una desincronía que no existe.

QUÉ NO TOCA
    La §8 y §8.1 de la ficha, y la §D y §E de la hoja: esos son la rúbrica y el formulario oficial,
    y los escribe `formulario_jurado.py` / `formulario_en_fichas.py`. El «### Banco de reserva» y el
    bloque «### Lo que se leyó en la sala» tampoco: son texto del jurado.

Uso:
    python config/evaluaciones/preguntas_en_tres_sitios.py                  # simula
    python config/evaluaciones/preguntas_en_tres_sitios.py --ver            # y las imprime
    python config/evaluaciones/preguntas_en_tres_sitios.py --confirmar
    python config/evaluaciones/preguntas_en_tres_sitios.py --confirmar --docx   # y rehace los .docx
    python config/evaluaciones/preguntas_en_tres_sitios.py --grupos G-004,G-007
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHAS = os.path.join(RAIZ, "Especializacion", "Evaluaciones", "2026-2", "Fichas de evaluacion")
INDICE = os.path.join(FICHAS, "00 - Indice y agenda de sustentaciones.md")

# El nombre de la carpeta empieza por el orden de sustentación, así que el orden alfabético del
# explorador es el orden de la sesión y basta con listar el directorio.
RE_CARPETA = re.compile(r"^(\d{2}) - (G-\d{3}) - ")

MAX_PALABRAS = 90  # techo de los 40 segundos de lectura en voz alta


def carpetas() -> list[tuple[str, str]]:
    """[(código, carpeta)] en orden de sustentación."""
    out = []
    for d in sorted(os.listdir(FICHAS)):
        m = RE_CARPETA.match(d)
        if m and os.path.isdir(os.path.join(FICHAS, d)):
            out.append((m.group(2), d))
    return out


# ---------------------------------------------------------------------------
# Lectura: sacar la FRASE, ignorando el marcado
# ---------------------------------------------------------------------------
INICIO = re.compile(r"^(?:\*\*\d[.)]\s|>\s*«|\s*\d\.\s*«)")

# Ficha y hoja se escribieron en tandas distintas y difieren en tipografía sin decir nada distinto:
# comillas rectas contra tipográficas, una cursiva `*así*`, un espacio duro antes del `%`. Ninguna de
# las tres se oye al leer en voz alta, así que se normalizan antes de comparar. Lo que tiene que
# coincidir es la FRASE QUE SE DICE; exigir el mismo byte reporta desincronías que no existen y, peor,
# invita a reescribir un archivo que estaba bien.
TIPOGRAFIA = str.maketrans({
    "“": '"', "”": '"',          # “ ”
    "‘": "'", "’": "'",          # ‘ ’
    " ": " ", " ": " ", " ": " ",  # espacios duro, fino duro y fino
})


def norm(s: str) -> str:
    s = s.replace("**", "").replace("«", "").replace("»", "").translate(TIPOGRAFIA)
    s = re.sub(r"^\s*>?\s*\d[.)]\s*", "", s)
    s = re.sub(r"\*(?!\s)([^*\n]+?)(?<!\s)\*", r"\1", s)  # cursiva de una sola línea
    s = re.sub(r"(\d)\s+%", r"\1%", s)                     # «87 %» y «87%» se oyen igual
    return re.sub(r"\s+", " ", re.sub(r"^\s*>\s*", "", s)).strip()


def region(txt: str, ini: str, fin: str) -> str:
    m = re.search(ini + r"(.*?)(?=" + fin + r"|\Z)", txt, re.S | re.M)
    return m.group(1) if m else ""


def preguntas(reg: str) -> list[str]:
    """La cita manda sobre el rótulo: cuando una ficha pone titular en negrita Y la cita entre
    comillas, la que se lee en voz alta es la cita."""
    bloques: list[str] = []
    buf: str | None = None
    for l in reg.split("\n"):
        if buf is None and INICIO.match(l):
            buf = l
        elif buf is not None:
            if not l.strip() or l.lstrip().startswith(("- ", "#", ">")):
                bloques.append(buf)
                buf = l if INICIO.match(l) else None
            else:
                buf += " " + l
        if buf is not None and buf.rstrip().endswith("»"):
            bloques.append(buf)
            buf = None
    if buf:
        bloques.append(buf)
    citas = [norm(b) for b in bloques if "«" in b and len(norm(b)) > 60]
    rotulos = [norm(b) for b in bloques if "«" not in b and len(norm(b)) > 60]
    return citas or rotulos


def de_ficha(carpeta: str) -> list[str]:
    p = os.path.join(FICHAS, carpeta, "1 - Ficha de preparacion.md")
    with open(p, encoding="utf-8") as fh:
        # Termina en el PRIMER `###` que siga: puede ser «Banco de reserva» o «Lo que se leyó en
        # la sala», que se añadió después y si no se corta aquí entra como cuarta pregunta.
        return preguntas(region(fh.read(), r"Las 3 que s[íi] voy a preguntar", r"^###\s"))


def de_hoja(carpeta: str) -> list[str]:
    p = os.path.join(FICHAS, carpeta, "2 - Hoja de respuestas.md")
    with open(p, encoding="utf-8") as fh:
        return preguntas(region(fh.read(), r"^##\s*C\s*[·.]", r"^##\s*D\s*[·.]"))


def de_indice(txt: str, codigo: str) -> list[str]:
    return preguntas(region(txt, rf"^####[^\n]*{codigo}[^\n]*$", r"^#{2,6}\s"))


# ---------------------------------------------------------------------------
# Escritura: sustituir la frase dejando el marcado como está
# ---------------------------------------------------------------------------
def reescribir_citas(texto: str, ini: str, fin: str, nuevas: list[str]) -> tuple[str, int]:
    """Cambia el contenido de cada `«…»` de una sola línea dentro de la región, en orden."""
    m = re.search(ini + r"(.*?)(?=" + fin + r"|\Z)", texto, re.S | re.M)
    if not m:
        return texto, 0
    reg, i, cambios = m.group(1), [0], 0
    lineas = reg.split("\n")
    for n, l in enumerate(lineas):
        if not INICIO.match(l) or "«" not in l or not l.rstrip().endswith("»"):
            continue
        if i[0] >= len(nuevas):
            break
        if norm(l) != nuevas[i[0]]:
            lineas[n] = re.sub(r"«.*»", "«" + nuevas[i[0]].replace("\\", "\\\\") + "»", l)
            cambios += 1
        i[0] += 1
    if not cambios:
        return texto, 0
    return texto[: m.start(1)] + "\n".join(lineas) + texto[m.end(1):], cambios


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--confirmar", action="store_true", help="escribe los archivos")
    ap.add_argument("--simular", action="store_true", help="no escribe nada (por defecto)")
    ap.add_argument("--ver", action="store_true", help="imprime las tres preguntas de cada grupo")
    ap.add_argument("--docx", action="store_true", help="con --confirmar, rehace los .docx tocados")
    ap.add_argument("--grupos", default="", help="solo estos códigos, separados por coma")
    args = ap.parse_args(argv)

    filtro = {c.strip().upper() for c in args.grupos.split(",") if c.strip()}
    with open(INDICE, encoding="utf-8") as fh:
        indice = fh.read()
    indice_nuevo = indice

    fallos, tocados, largas = 0, [], []
    for codigo, carpeta in carpetas():
        if filtro and codigo not in filtro:
            continue
        f_q, h_q = de_ficha(carpeta), de_hoja(carpeta)
        i_q = de_indice(indice_nuevo, codigo)

        if len(f_q) != 3:
            print(f"  ⛔ {codigo}: la §6 de la ficha da {len(f_q)} preguntas, no 3. No se toca nada.")
            fallos += 1
            continue

        for n, q in enumerate(f_q, 1):
            if len(q.split()) > MAX_PALABRAS:
                largas.append(f"{codigo} · {n} · {len(q.split())} palabras")

        acciones = []
        # la hoja
        ruta_h = os.path.join(FICHAS, carpeta, "2 - Hoja de respuestas.md")
        if h_q != f_q:
            with open(ruta_h, encoding="utf-8") as fh:
                t = fh.read()
            t2, n = reescribir_citas(t, r"^##\s*C\s*[·.]", r"^##\s*D\s*[·.]", f_q)
            if n and args.confirmar:
                with open(ruta_h, "w", encoding="utf-8") as fh:
                    fh.write(t2)
            if n:
                acciones.append(f"hoja §C: {n}")
                tocados.append((carpeta, "2 - Hoja de respuestas"))
            else:
                fallos += 1
                acciones.append("⛔ hoja §C distinta y no pude sustituirla (marcado inesperado)")

        # el índice
        if i_q != f_q:
            t2, n = reescribir_citas(indice_nuevo, rf"^####[^\n]*{codigo}[^\n]*$", r"^#{2,6}\s", f_q)
            if n:
                indice_nuevo = t2
                acciones.append(f"índice: {n}")
            else:
                fallos += 1
                acciones.append(f"⛔ el bloque del índice de {codigo} no tiene 3 citas sustituibles")

        estado = " · ".join(acciones) if acciones else "="
        print(f"  {'⛔' if '⛔' in estado else ('~' if acciones else '✓')} {codigo}  {estado}")
        if args.ver:
            for n, q in enumerate(f_q, 1):
                print(f"        {n}. [{len(q.split()):>2} pal] {q}")

    if indice_nuevo != indice and args.confirmar:
        with open(INDICE, "w", encoding="utf-8") as fh:
            fh.write(indice_nuevo)
        tocados.append(("", "00 - Indice y agenda de sustentaciones"))

    if largas:
        print(f"\n  ⚠️  {len(largas)} preguntas pasan de {MAX_PALABRAS} palabras (no caben en 40 s):")
        for l in largas:
            print(f"      {l}")

    if args.docx and args.confirmar and tocados:
        sys.path.insert(0, os.path.join(RAIZ, "config", "slides"))
        import guion_md_a_docx

        print()
        for carpeta, nombre in dict.fromkeys(tocados):
            md = os.path.join(FICHAS, carpeta, nombre + ".md")
            guion_md_a_docx.convert(md, os.path.splitext(md)[0] + ".docx", brand=True)
            print(f"  docx {nombre}  {carpeta or '(índice)'}")

    grupos_tocados = len({c for c, _ in tocados if c})
    if fallos:
        print(f"\n⛔ {fallos} problemas")
    elif grupos_tocados or indice_nuevo != indice:
        print(f"\n{'✓ sincronizados' if args.confirmar else '~ hay que sincronizar'}: "
              f"{grupos_tocados} grupos" + (" y el índice" if indice_nuevo != indice else ""))
    else:
        print("\n✓ las preguntas ya coinciden en los tres sitios. Nada que hacer.")
    if not args.confirmar:
        print("Simulación. Nada escrito. Añada --confirmar para aplicar (y --docx para rehacer los .docx).")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
