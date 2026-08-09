# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(__file__).with_name("carga_academica_2026.json")
data = json.loads(p.read_text(encoding="utf-8"))
n = 0
for c in data["cursos"].values():
    if c.get("inicio") == "2026-08-03":
        c["inicio"] = "2026-08-10"
        n += 1
    for g in c.get("grupos", {}).values():
        if g.get("inicio") == "2026-08-03":
            g["inicio"] = "2026-08-10"
            n += 1
notas = data.setdefault("notas", [])
extra = [
    "Inicio operativo del semestre 2026 (pedido docente / clase AFI 10/08): 2026-08-10 en todos los cursos.",
    "Fechas de entrega ACA: cálculo regenerable en config/cursos/fechas_entrega_aca.py (no hardcodear en enunciados).",
]
for e in extra:
    if e not in notas:
        # insert before last "Edita este archivo..." if present
        if notas and notas[-1].startswith("Edita este archivo"):
            notas.insert(-1, e)
        else:
            notas.append(e)
data["actualizado"] = "2026-08-07"
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("inicios actualizados:", n)
