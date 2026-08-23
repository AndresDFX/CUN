# -*- coding: utf-8 -*-
"""
Los criterios de evaluación de cada ACA, leídos de la guía que el estudiante ya tiene.

Fuente única: los `.docx` de `<curso>/Clases/Recursos/ACAs/`, que genera
`config/slides/build_acas_estudiantes.py`. Se comenta contra el checklist **que se le entregó al
estudiante**, no contra una rúbrica paralela; si el criterio cambia, cambia en un solo sitio y el
comentario lo sigue.

Lo usan las dos mitades del proceso de comentar documentos:
`plan_comentarios.py` (aquí, para redactar) y `build_apps_script_comentarios.py`
(que los incrusta en el `.gs` para que Google valide el plan antes de publicar).
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]

# Carpeta de cada curso. Las claves son las de `config/cursos/fechas_entrega_aca.py`.
CURSOS = {
    "proyecto1": "Especializacion/Proyecto I",
    "creatividad": "Pregrado/Creatividad y pensamiento innovador",
    "investigacion": "Pregrado/Investigacion en ciencia y tecnologia",
    "tg2": "Pregrado/Trabajo de grado 2",
    "tg3": "Pregrado/Trabajo de grado 3",
}


def guias(curso: str) -> list[Path]:
    """Las guías de ACA del curso. Solo las ACA: los quices se responden en el aula, no se comentan."""
    raiz = REPO / CURSOS[curso] / "Clases" / "Recursos" / "ACAs"
    return sorted(Path(p) for p in glob.glob(str(raiz / "ACA*.docx")))


def slug(guia: Path) -> str:
    """«ACA 1 (25%) - Formulacion…» → `aca1` · «ACA FINAL (42%) - …» → `acafinal`."""
    cabeza = guia.stem.split("(")[0]
    return re.sub(r"[^a-z0-9]", "", cabeza.lower())


def checklist(guia: Path) -> list[str]:
    """El checklist de la sección «Criterios de evaluación» de esa guía.

    Los ítems se reconocen por el `[ ]` con que los escribe el generador. La sección termina en el
    siguiente encabezado numerado («6. Herramientas…»), no al primer párrafo suelto: entre los ítems
    puede haber una línea de aclaración.
    """
    from docx import Document

    parrafos = [p.text.strip() for p in Document(str(guia)).paragraphs]
    dentro = False
    items: list[str] = []
    for t in parrafos:
        if re.search(r"Criterios de evaluaci", t, re.I):
            dentro = True
            continue
        if not dentro:
            continue
        if t.startswith("[ ]") or t.startswith("[x]"):
            items.append(t[3:].strip())
        elif items and re.match(r"^\d+\.\s+\S", t):
            break
    return items


def criterios(curso: str, aca: str) -> tuple[str, list[str]]:
    """(nombre de la guía, criterios) del ACA pedido. Aborta diciendo qué hay si no coincide."""
    pedido = re.sub(r"[^a-z0-9]", "", aca.lower())
    for g in guias(curso):
        if slug(g) == pedido:
            return g.stem, checklist(g)
    hay = ", ".join(f"{slug(g)}" for g in guias(curso)) or "(ninguna)"
    raise SystemExit(
        f"«{aca}» no existe en {curso}. Disponibles: {hay}\n"
        "Recuerda: pregrado tiene UNA sola tarea documental (ACA Final); Especialización dos."
    )


def todos() -> dict[str, dict[str, dict]]:
    """Todo el mapa curso → aca → {guia, criterios}. Lo incrusta el generador del Apps Script."""
    salida: dict[str, dict[str, dict]] = {}
    for curso in sorted(CURSOS):
        for g in guias(curso):
            items = checklist(g)
            if items:
                salida.setdefault(curso, {})[slug(g)] = {"guia": g.stem, "criterios": items}
    return salida


if __name__ == "__main__":
    total = 0
    for curso, acas in todos().items():
        for s, d in acas.items():
            print(f"{curso:<14} {s:<9} {len(d['criterios']):>2} criterios   {d['guia']}")
            total += len(d["criterios"])
    print(f"\n{total} criterios en total")
