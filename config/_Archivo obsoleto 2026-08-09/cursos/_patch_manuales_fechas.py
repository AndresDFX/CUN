# -*- coding: utf-8 -*-
"""Actualiza fechas de inicio/ACA en Manuales del Docente (los 5)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fechas_entrega_aca import entregas_curso, fmt_dmy, resumen_tabla_markdown
from carga_academica import curso, load_carga

load_carga(force=True)

MANUALS = {
    "proyecto1": ROOT / "Especializacion/PROYECTO I/Manual del Docente - PROYECTO I.md",
    "creatividad": ROOT / "Pregrado/CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS/Manual del Docente - Creatividad y Pensamiento Innovador.md",
    "investigacion": ROOT / "Pregrado/INVESTIGACION CIENCIA Y TECNOLOGIA PARA ESCUELA DE INGENIERIAS/Manual del Docente - Investigacion Ciencia y Tecnologia.md",
    "tg2": ROOT / "Pregrado/TRABAJO DE GRADO 2 - MODELOS DE INNOVACION INGENIERIA DE SISTEMAS/Manual del Docente - Trabajo de Grado 2.md",
    "tg3": ROOT / "Pregrado/TRABAJO DE GRADO 3 - MODELOS DE INNOVACION INGENIERIA DE SISTEMAS/Manual del Docente - Trabajo de Grado 3.md",
}


def patch_inicio_table(text: str) -> str:
    # 03/08/2026 → 10/08/2026 en tablas de oferta
    return text.replace("03/08/2026", "10/08/2026")


def patch_p1(text: str) -> str:
    data = {e.id: e for e in entregas_curso("proyecto1")}
    a1, a2, a3 = data["aca1"], data["aca2"], data["aca3"]
    co, au = data["coev"], data["auto"]
    text = re.sub(
        r"### ACA 1 — Formulación del problema \(25%, cierra [^)]+\)",
        f"### ACA 1 — Formulación del problema (25%, cierra {fmt_dmy(a1.entrega)}, "
        f"nota máx. {fmt_dmy(a1.nota_docente)})",
        text,
    )
    text = re.sub(
        r"### ACA 2 — Fundamentación referencial \(25%, cierra [^)]+\)",
        f"### ACA 2 — Fundamentación referencial (25%, cierra {fmt_dmy(a2.entrega)}, "
        f"nota máx. {fmt_dmy(a2.nota_docente)})",
        text,
    )
    text = re.sub(
        r"### ACA 3 — Diseño metodológico y anteproyecto FINAL \(42%, cierra [^)]+\)",
        f"### ACA 3 — Diseño metodológico y anteproyecto FINAL (42%, cierra {fmt_dmy(a3.entrega)}, "
        f"nota máx. {fmt_dmy(a3.nota_docente)})",
        text,
    )
    text = re.sub(
        r"ACA1 calificada con retro antes del [^;]+; ACA2 antes del [^;]+; ACA3 antes del [^\.]+",
        f"ACA1 calificada con retro antes del {fmt_dmy(a1.nota_docente)}; "
        f"ACA2 antes del {fmt_dmy(a2.nota_docente)}; ACA3 antes del {fmt_dmy(a3.nota_docente)}",
        text,
    )
    text = re.sub(
        r"Antes de la \"fecha límite para ingreso de nota\" de cada una \([^)]+\)",
        f'Antes de la "fecha límite para ingreso de nota" de cada una '
        f"({fmt_dmy(a1.nota_docente)}, {fmt_dmy(a2.nota_docente)}, {fmt_dmy(a3.nota_docente)})",
        text,
    )
    # Bloque resumen fechas
    marker = "\n## Fechas de entrega ACA (calculadas)\n"
    block = (
        marker
        + "\nFuente: `config/cursos/fechas_entrega_aca.py` (inicio operativo **10/08/2026**).\n\n"
        + resumen_tabla_markdown("proyecto1")
        + f"\n\n- Coevaluación: {fmt_dmy(co.apertura)} – {fmt_dmy(co.entrega)}\n"
        + f"- Autoevaluación: {fmt_dmy(au.apertura)} – {fmt_dmy(au.entrega)}\n"
    )
    if marker in text:
        # replace until next ##
        text = re.sub(
            r"\n## Fechas de entrega ACA \(calculadas\)\n.*?(?=\n## |\Z)",
            block + "\n",
            text,
            flags=re.S,
        )
    else:
        # insert before PARTE 3 or at end of evaluación section
        if "## PARTE 3" in text:
            text = text.replace("## PARTE 3", block + "\n## PARTE 3")
        else:
            text += "\n" + block
    return text


def patch_pregrado(key: str, text: str) -> str:
    marker = "\n## Fechas de entrega ACA / cortes (calculadas)\n"
    block = (
        marker
        + "\nFuente: `config/cursos/fechas_entrega_aca.py` (inicio **10/08/2026**).\n\n"
        + resumen_tabla_markdown(key)
        + "\n"
    )
    if marker.strip() in text or "Fechas de entrega ACA / cortes" in text:
        text = re.sub(
            r"\n## Fechas de entrega ACA / cortes \(calculadas\)\n.*?(?=\n## |\Z)",
            block + "\n",
            text,
            flags=re.S,
        )
    else:
        # after enunciados estudiantes line
        if "**Enunciados" in text:
            lines = text.splitlines()
            out = []
            inserted = False
            for ln in lines:
                out.append(ln)
                if (not inserted) and "Enunciados" in ln and "ACAs" in ln:
                    out.append(block)
                    inserted = True
            text = "\n".join(out)
            if not text.endswith("\n"):
                text += "\n"
        else:
            text += "\n" + block
    return text


for key, path in MANUALS.items():
    if not path.is_file():
        print("SKIP missing", path)
        continue
    t = path.read_text(encoding="utf-8")
    t = patch_inicio_table(t)
    if key == "proyecto1":
        t = patch_p1(t)
    else:
        t = patch_pregrado(key, t)
    path.write_text(t, encoding="utf-8")
    print("OK", path.relative_to(ROOT))

# Calendario oficial P1 — actualizar tabla de cronograma ACA
cal = ROOT / "Especializacion/PROYECTO I/Calendario de clases (oficial).md"
if cal.is_file():
    data = {e.id: e for e in entregas_curso("proyecto1")}
    c = curso("proyecto1")
    note = (
        "\n\n## Fechas de entrega ACA (regenerables · inicio 10/08/2026)\n\n"
        "Cálculo: `config/cursos/fechas_entrega_aca.py` sobre carga académica "
        f"(recepción {c['recepcion']}, cierre {c['cierre']}).\n\n"
        + resumen_tabla_markdown("proyecto1")
        + "\n\n> La tabla histórica del cronograma AFI (inicio 03/08) queda sustituida "
        "operativamente por estas fechas al mover el inicio a **10/08/2026**.\n"
    )
    t = cal.read_text(encoding="utf-8")
    if "## Fechas de entrega ACA (regenerables" in t:
        t = re.sub(
            r"\n## Fechas de entrega ACA \(regenerables.*",
            note.rstrip() + "\n",
            t,
            flags=re.S,
        )
    else:
        t = t.rstrip() + note
    # Inicio del periodo
    t = t.replace("Inicio del periodo: **03/08/2026**", "Inicio del periodo: **10/08/2026**")
    cal.write_text(t, encoding="utf-8")
    print("OK", cal.relative_to(ROOT))
