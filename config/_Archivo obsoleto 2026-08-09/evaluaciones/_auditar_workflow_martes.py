# -*- coding: utf-8 -*-
"""Comprobación de una sola vez: qué escribieron de verdad los 9 agentes del martes.

Verifica lo que les di como VETADO:
  · que la §5 conserve, bajo «Lo que se leyó en la sala el 18/08», las 3 preguntas viejas
  · que ninguna cédula haya entrado a la carpeta
  · que la §7/§7.1 de la ficha y la §D/§E de la hoja no las tocara el workflow
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHAS = os.path.join(RAIZ, "Especializacion", "Evaluaciones", "2026-2", "Fichas de evaluacion")
MARTES = [f"G-{n:03d}" for n in range(1, 10)]
RE_CARPETA = re.compile(r"^(\d{2}) - (G-\d{3}) - ")

# Una cédula colombiana son 7-10 dígitos seguidos, con o sin puntos de miles. Un folio, un
# porcentaje y un número de tabla nunca llegan a siete.
RE_CEDULA = re.compile(r"(?<!\d)(?:\d{1,3}\.){2,3}\d{3}(?!\d)|(?<![\d.,])\d{7,10}(?![\d.,])")


def carpetas():
    out = {}
    for d in sorted(os.listdir(FICHAS)):
        m = RE_CARPETA.match(d)
        if m and os.path.isdir(os.path.join(FICHAS, d)):
            out[m.group(2)] = d
    return out


def region(txt, ini, fin):
    m = re.search(ini + r"(.*?)(?=" + fin + r"|\Z)", txt, re.S | re.M)
    return m.group(1) if m else ""


def head(rel):
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=RAIZ,
                       capture_output=True)
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


print("1) EL BLOQUE DE LO QUE SE LEYÓ EN LA SALA EL 18/08")
faltan = []
for cod in MARTES:
    carp = carpetas()[cod]
    p = os.path.join(FICHAS, carp, "1 - Ficha de preparacion.md")
    txt = open(p, encoding="utf-8").read()
    reg = region(txt, r"^###[^\n]*se ley[óo] en la sala", r"^#{2,3}\s")
    citas = [l for l in reg.split("\n") if "«" in l and len(l) > 60]
    marca = "✓" if len(citas) == 3 else "⛔"
    if len(citas) != 3:
        faltan.append(cod)
    print(f"   {marca} {cod}  {len(citas)} preguntas viejas conservadas")

print("\n2) CÉDULAS EN LA CARPETA (7-10 dígitos seguidos)")
sospechas = []
for raiz, _, files in os.walk(FICHAS):
    for f in files:
        if not f.endswith((".md", ".txt")):
            continue
        p = os.path.join(raiz, f)
        for n, l in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            for m in RE_CEDULA.finditer(l):
                sospechas.append((os.path.relpath(p, FICHAS), n, m.group(0), l.strip()[:90]))
print(f"   {len(sospechas)} coincidencias:")
for rel, n, v, ctx in sospechas:
    print(f"     {v:>13}  {rel} L{n}  …{ctx}…")

print("\n3) ¿TOCÓ EL WORKFLOW LA §7/§7.1 DE LA FICHA O LA §D/§E DE LA HOJA?")
print("   (se compara con HEAD; si un tramo cambió en los 13 grupos por igual es del")
print("    formulario del segmento anterior, no de los 9 agentes)")
ZONAS = [
    ("1 - Ficha de preparacion.md", r"^##\s*7\s*[·.]", r"\Z"),
    ("2 - Hoja de respuestas.md", r"^##\s*D\s*[·.]", r"\Z"),
]
for archivo, ini, fin in ZONAS:
    print(f"\n   {archivo}")
    for cod, carp in carpetas().items():
        rel = f"Especializacion/Evaluaciones/2026-2/Fichas de evaluacion/{carp}/{archivo}"
        antes = head(rel)
        if antes is None:
            print(f"     ?? {cod}  no está en HEAD")
            continue
        ahora = open(os.path.join(FICHAS, carp, archivo), encoding="utf-8").read()
        a, b = region(antes, ini, fin), region(ahora, ini, fin)
        dia = "martes" if cod in MARTES else "miérc."
        print(f"     {'=' if a == b else '≠'}  {cod} ({dia})  "
              f"{len(a)} → {len(b)} caracteres")

print()
print("⛔ faltan bloques en: " + ", ".join(faltan) if faltan
      else "✓ los 9 conservan las 3 preguntas que se leyeron el 18/08")
