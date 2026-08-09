# -*- coding: utf-8 -*-
"""Temporal: verificar paths tras limpieza. Borrar al terminar."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "config" / "cursos"))
from carga_academica import load_carga  # noqa: E402
from sesiones_cun import COURSES  # noqa: E402

carga = load_carga()
print("=== carga_academica folders ===")
for key, c in carga["cursos"].items():
    p = ROOT / c["folder"]
    print(f"{key}: {c['folder']} -> exists={p.is_dir()}")
    for g in c["grupos"]:
        gdir = p / "2026" / g
        print(f"  2026/{g}: exists={gdir.is_dir()}")
    pptx = list((p / "Clases").glob("Presentacion del Curso*.pptx")) if (p / "Clases").exists() else []
    print(f"  Presentaciones: {[x.name for x in pptx]}")
    leeme = p / "Clases" / "LEEME - Material para estudiantes.docx"
    print(f"  LEEME: {leeme.exists()}")
    guiones = list((p / "Guiones").glob("Sesion *.md")) if (p / "Guiones").exists() else []
    print(f"  Guiones .md: {len(guiones)} · sesiones COURSES={len(COURSES[key]['sesiones'])}")

orphans = []
for d in (ROOT / "Pregrado").rglob("Sesion 01*"):
    if d.is_dir() and ("trabajo final" in d.name or "producto final" in d.name):
        orphans.append(str(d.relative_to(ROOT)))
print("orphans:", orphans or "none")

p1_clases = ROOT / "Especializacion" / "Proyecto I" / "Clases"
print("nuevo pptx:", list(p1_clases.glob("*nuevo*")))
print(
    "canonical pptx:",
    (p1_clases / "Presentacion del Curso - Proyecto I.pptx").exists(),
)
print(
    "sesion07 inv:",
    (
        ROOT
        / "Pregrado"
        / "Investigacion en ciencia y tecnologia"
        / "Guiones"
        / "Capturas"
        / "Sesion 07"
    ).exists(),
)
print(
    "md in Clases:",
    [str(p.relative_to(ROOT)) for p in (ROOT).rglob("Clases/**/*.md")],
)
print(
    "docx in Guiones:",
    [str(p.relative_to(ROOT)) for p in (ROOT).rglob("Guiones/**/*.docx")],
)
print(
    "correo in Clases:",
    [str(p.relative_to(ROOT)) for p in (ROOT).rglob("Clases/**/*bienvenida*")],
)
