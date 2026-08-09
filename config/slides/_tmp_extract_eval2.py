# -*- coding: utf-8 -*-
"""Dump full evaluation table cells without collapsing duplicates poorly."""
from docx import Document
from pathlib import Path

files = {
    "INV": Path(
        r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\Pregrado"
        r"\INVESTIGACION CIENCIA Y TECNOLOGIA PARA ESCUELA DE INGENIERIAS"
        r"\INVESTIGACION CIENCIA Y TECNOLOGIA PARA ESCUELA DE INGENIERIAS EI005_PRES.docx"
    ),
    "CRE": Path(
        r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\Pregrado"
        r"\CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS"
        r"\CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS EI004_VIR.docx"
    ),
}

out = Path(r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\config\slides\_tmp_eval_extract")

for key, path in files.items():
    doc = Document(str(path))
    lines = [f"=== {key} full tables near evaluacion ==="]
    for ti, table in enumerate(doc.tables):
        blob = " ".join(c.text for row in table.rows for c in row.cells).lower()
        if "corte" not in blob and "sistema de evalu" not in blob and "mecanismos" not in blob:
            continue
        lines.append(f"\n## TABLE {ti} rows={len(table.rows)} cols={len(table.columns)}")
        for ri, row in enumerate(table.rows):
            cells = []
            for ci, cell in enumerate(row.cells):
                t = " ".join(cell.text.split())
                cells.append(f"[{ci}]{t}")
            # dedupe consecutive identical merged cells for readability
            shown = []
            prev = None
            for c in cells:
                if c != prev:
                    shown.append(c)
                    prev = c
            lines.append(f"R{ri}: " + " || ".join(shown))
    (out / f"{key}_eval_full.txt").write_text("\n".join(lines), encoding="utf-8")
    print("OK", key)
