# -*- coding: utf-8 -*-
"""Convierte un .md a .docx con identidad CUN — reutiliza el mismo motor que usan los
generadores de material de curso (`config/slides/guion_md_a_docx.py`), para que las
propuestas de investigación y los artículos salgan con la misma marca que todo lo demás
en este repositorio.

Uso:
  python Investigacion/build_documento.py "Propuestas 2026/Propuesta 1 - Titulo.md"
  python Investigacion/build_documento.py "Propuestas 2026/Propuesta 1 - Titulo.md" \
      --subtitulo "Convocatoria interna CUN 2026 (Fase II) · Anteproyecto"
"""
from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "config", "slides"))
sys.path.insert(0, os.path.join(_HERE, "..", "config", "cursos"))

from guion_md_a_docx import convert  # noqa: E402


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("md", help="Ruta al .md de entrada")
    ap.add_argument("--subtitulo", default=None, help="Subtítulo bajo el título del documento")
    ap.add_argument("--footer", default=None, help="Texto del pie de página")
    ap.add_argument("--out", default=None, help="Ruta del .docx de salida (por defecto, mismo nombre)")
    args = ap.parse_args(argv)

    md_path = os.path.abspath(args.md)
    out_path = args.out or (os.path.splitext(md_path)[0] + ".docx")
    convert(md_path, out_path, brand=True, subtitle=args.subtitulo, footer=args.footer)
    print("OK", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
