# -*- coding: utf-8 -*-
"""Reemplaza el taller escrito a mano de cada JSON de sesión por el marcador `{"type": "taller"}`.

Es la migración de una sola vez que pasa los 45 talleres de estar escritos dentro de
`content/cun_<curso>_s<NN>.json` a salir de la fuente única `talleres.py`. El marcador conserva
**la posición exacta** que el taller tenía en la sesión, así que el orden de las slides no cambia.

    python config/slides/aplicar_talleres.py              # simulación (no escribe nada)
    python config/slides/aplicar_talleres.py --confirmar  # escribe los JSON

Es idempotente: correrlo de nuevo no encuentra nada que cambiar. Antes de escribir comprueba que
`talleres.py` tenga entrada para cada taller que va a reemplazar; si falta una, no toca ese archivo
—perder el texto sin tener con qué sustituirlo sería el único daño irreversible aquí—.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import talleres  # noqa: E402

ES_TALLER = re.compile(r"^\s*taller\b", re.IGNORECASE)
MARCADOR = {"type": "taller"}


def _clave(nombre: str) -> tuple[str, int] | None:
    m = re.search(r"^cun_(.+)_s(\d\d)\.json$", nombre)
    return (m.group(1), int(m.group(2))) if m else None


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    confirmar = "--confirmar" in argv

    avisos = talleres.verificar()
    if avisos:
        print("talleres.py no cumple su propio contrato; no se migra nada:")
        for a in avisos:
            print("   ⚠ " + a)
        return 1

    cambiados = ya_estaban = sin_taller = 0
    problemas: list[str] = []

    for ruta in sorted(glob.glob(os.path.join(_HERE, "content", "cun_*_s*.json"))):
        nombre = os.path.basename(ruta)
        clave = _clave(nombre)
        if not clave:
            continue
        with open(ruta, encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, list):
            continue

        idx_marcador = [i for i, b in enumerate(data)
                        if isinstance(b, dict) and (b.get("type") or "").lower() == "taller"]
        idx_manual = [i for i, b in enumerate(data)
                      if isinstance(b, dict) and ES_TALLER.match(str(b.get("title", "")))]

        if idx_marcador and not idx_manual:
            ya_estaban += 1
            continue
        if not idx_manual:
            sin_taller += 1
            continue
        if not talleres.tiene(*clave):
            problemas.append("%s: tiene taller escrito a mano pero talleres.py no tiene entrada "
                             "para (%s, s%02d). No se toca." % (nombre, clave[0], clave[1]))
            continue

        nuevo = list(data)
        for i in reversed(idx_manual):
            nuevo[i] = dict(MARCADOR)
        # Solo el primero queda como marcador; si hubiera más de uno (nunca ha pasado), los
        # sobrantes se eliminan para no duplicar el taller en la deck.
        if len(idx_manual) > 1:
            for i in reversed(idx_manual[1:]):
                del nuevo[i]

        titulo = str(data[idx_manual[0]].get("title", ""))
        vinetas = len(data[idx_manual[0]].get("bullets") or [])
        desborde = " ⟵ desbordaba a «(cont.)»" if vinetas > 9 else ""
        print("   %-26s pos %2d · %2d viñetas%s\n%s%s"
              % (nombre, idx_manual[0], vinetas, desborde, " " * 30, titulo))

        if confirmar:
            with open(ruta, "w", encoding="utf-8") as fh:
                json.dump(nuevo, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
        cambiados += 1

    print("\n%s   %d con taller a migrar · %d ya con marcador · %d sin taller"
          % ("ESCRITO" if confirmar else "SIMULACIÓN", cambiados, ya_estaban, sin_taller))
    for p in problemas:
        print("   ⚠ " + p)
    if not confirmar and cambiados:
        print("   → repita con --confirmar para escribir los JSON")
    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
