# -*- coding: utf-8 -*-
"""Reescribe el bloque «Fechas de entrega ACA» de los Manuales del Docente de PREGRADO.

Por qué existe: los cuatro manuales de pregrado tenían la tabla **congelada** con el
reparto por pesos que se abandonó el 2026-08-10. Ningún build vivo los regeneraba
(el único consumidor de `resumen_tabla_markdown` era un script archivado que ya ni
siquiera corre: apuntaba a nombres de carpeta inexistentes), así que Creatividad e
Investigación anunciaban al docente fechas **7 días antes** de las que ya estaban en
los enunciados del estudiante.

Qué hace: sustituye el bloque que empieza en `## Fechas de entrega ACA` y termina en
el siguiente encabezado `## `, con la tabla en vivo de `fechas_entrega_aca` (columna
«Regla» derivada de `EntregaAca.regla`, no hardcodeada).

Uso:
    python config/cursos/sync_manuales_fechas.py            # los 4 de pregrado
    python config/cursos/sync_manuales_fechas.py creatividad

Proyecto I NO se toca aquí: su manual lleva una tabla propia con % y corte, curada a
mano contra el cronograma oficial de Coordinación.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from carga_academica import workspace_root  # noqa: E402
from fechas_entrega_aca import resumen_tabla_markdown  # noqa: E402

MANUALES = {
    "creatividad": "Pregrado/Creatividad y pensamiento innovador/"
                   "Manual del Docente - Creatividad y Pensamiento Innovador.md",
    "investigacion": "Pregrado/Investigacion en ciencia y tecnologia/"
                     "Manual del Docente - Investigacion Ciencia y Tecnologia.md",
    "tg2": "Pregrado/Trabajo de grado 2/Manual del Docente - Trabajo de Grado 2.md",
    "tg3": "Pregrado/Trabajo de grado 3/Manual del Docente - Trabajo de Grado 3.md",
}

HEADING = "## Fechas de entrega ACA / cortes"


def bloque(key: str) -> str:
    return (
        f"{HEADING}\n"
        "\n"
        "Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — "
        f"regenerar con `python config/cursos/sync_manuales_fechas.py {key}`.\n"
        "\n"
        f"{resumen_tabla_markdown(key)}\n"
        "\n"
    )


def sync(key: str) -> bool:
    path = workspace_root() / MANUALES[key]
    text = io.open(path, encoding="utf-8").read()
    pat = re.compile(r"^## Fechas de entrega ACA.*?(?=^## )", re.S | re.M)
    if not pat.search(text):
        print(f"AVISO {path.name}: no encontré el bloque de fechas — sin cambios")
        return False
    nuevo = pat.sub(lambda _m: bloque(key), text, count=1)
    if nuevo == text:
        print(f"OK {path.name} (ya estaba al día)")
        return False
    io.open(path, "w", encoding="utf-8", newline="").write(nuevo)
    print(f"OK {path.name} — tabla de fechas actualizada")
    return True


def main(argv: list[str] | None = None) -> None:
    argv = list(argv if argv is not None else sys.argv[1:])
    keys = [a for a in argv if a in MANUALES] or list(MANUALES)
    for k in keys:
        sync(k)


if __name__ == "__main__":
    main()
