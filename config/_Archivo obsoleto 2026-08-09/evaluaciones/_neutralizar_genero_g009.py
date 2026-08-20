# -*- coding: utf-8 -*-
"""G-009: quitar el femenino que salía de los nombres, no del documento.

POR QUÉ
    El trabajo de G-009 nunca dice «autoras» ni «las estudiantes»: su presupuesto (p. 115) los
    nombra «Estudiante 1», «Estudiante 2» y «Estudiantes». El femenino de la ficha salía de los
    nombres de pila, que no es una fuente. Y «la estudiante», en singular, además contradice al
    propio documento, que registra **dos**.

    Ninguna de estas frases es una de las tres preguntas de la §5, así que la sincronía
    ficha↔hoja↔índice no se toca. Las dos que sí viven en dos sitios —el condicional de §6 de la
    ficha y su casilla en la §B de la hoja— se cambian con el mismo texto.

Uso:
    python config/evaluaciones/_neutralizar_genero_g009.py            # simula
    python config/evaluaciones/_neutralizar_genero_g009.py --confirmar
"""
from __future__ import annotations

import argparse
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARP = os.path.join(RAIZ, "Especializacion", "Evaluaciones", "2026-2", "Fichas de evaluacion",
                    "09 - G-009 - Ecosistema digital RRHH con celulas agiles")

# (archivo, viejo, nuevo, cuántas veces tiene que aparecer)
CAMBIOS = [
    ("1 - Ficha de preparacion.md",
     "**Techo del trabajo, declarado por ellas mismas.**",
     "**Techo del trabajo, declarado por el propio documento.**", 1),
    ("1 - Ficha de preparacion.md",
     "al acceso restringido de la estudiante a la información de la empresa",
     "al acceso restringido del equipo a la información de la empresa", 1),
    ("1 - Ficha de preparacion.md",
     "al acceso restringido de la estudiante a los datos de la empresa",
     "al acceso restringido del equipo a los datos de la empresa", 1),
    ("1 - Ficha de preparacion.md",
     "y referida al acceso restringido de la estudiante.",
     "y referida al acceso restringido del equipo.", 1),
    ("1 - Ficha de preparacion.md",
     "decir que el especialista low-code «son ellas mismas», con un presupuesto de dos "
     "estudiantes (p. 115)",
     "decir que el papel de especialista low-code lo cubre el propio equipo, cuando el "
     "presupuesto solo paga a dos estudiantes (p. 115)", 1),
    # Este par vive en los dos archivos y tiene que quedar con el mismo texto.
    ("1 - Ficha de preparacion.md",
     "pedirles que digan las dos que ellas mismas escribieron (pp. 26-27)",
     "pedirles que digan las dos que escribieron (pp. 26-27)", 1),
    ("2 - Hoja de respuestas.md",
     "pedirles que digan las dos que ellas mismas escribieron (pp. 26-27)",
     "pedirles que digan las dos que escribieron (pp. 26-27)", 1),
]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--confirmar", action="store_true", help="escribe los archivos")
    args = ap.parse_args(argv)

    textos = {}
    for arch in {c[0] for c in CAMBIOS}:
        textos[arch] = open(os.path.join(CARP, arch), encoding="utf-8").read()

    # Se cuenta TODO antes de escribir NADA: si una sola cuenta no cuadra, no se toca el disco.
    problemas = []
    for arch, viejo, nuevo, esperadas in CAMBIOS:
        n = textos[arch].count(viejo)
        marca = "✓" if n == esperadas else "⛔"
        print(f"  {marca} {arch[0]}  {n}/{esperadas}  {viejo[:66]}…")
        if n != esperadas:
            problemas.append(f"{arch}: «{viejo[:50]}…» aparece {n} veces, se esperaban {esperadas}")

    if problemas:
        print("\n⛔ no se escribe nada:")
        for p in problemas:
            print(f"   {p}")
        return 1

    for arch, viejo, nuevo, _ in CAMBIOS:
        textos[arch] = textos[arch].replace(viejo, nuevo)

    if args.confirmar:
        for arch, t in textos.items():
            with open(os.path.join(CARP, arch), "w", encoding="utf-8") as fh:
                fh.write(t)
        print(f"\n✓ {len(CAMBIOS)} sustituciones escritas en {len(textos)} archivos.")
    else:
        print(f"\n~ {len(CAMBIOS)} sustituciones listas. Simulación: nada escrito. "
              f"Añada --confirmar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
