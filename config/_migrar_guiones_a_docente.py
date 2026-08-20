# -*- coding: utf-8 -*-
"""Reescribe las referencias a la carpeta de guiones tras moverla dentro de `Docente/`.

    <Asignatura>/Guiones/…   ->   <Asignatura>/Docente/Guiones/…

Contexto: los guiones docentes son material **solo del Docente** —igual que los bancos de preguntas,
que se movieron a `Docente/Cuestionarios/` el 18/08/2026—, así que viven en la misma carpeta. Los 198
archivos se movieron con `git mv` el 19/08/2026; esto pone al día lo que los nombraba por ruta.

    python config/_migrar_guiones_a_docente.py            # en seco: enseña qué cambiaría
    python config/_migrar_guiones_a_docente.py --aplicar   # escribe

Dos cosas que NO toca, a propósito:

* **FESNA.** `alinear_narracion.py`, `build_daw_capturas.py`, `shots_desarrollo_moviles_1.py` y
  `capturar_pantallas_examlab.cjs` apuntan a `Empleo/FESNA/Cursos/…`, otro Drive con su propia
  estructura (allí los guiones cuelgan de `Clases/Version vigente …/Guiones/`). Reescribirlos rompería
  rutas que aquí no se pueden verificar.
* **`_Archivo obsoleto 2026-08-09/`.** Es una foto congelada de cómo estaba el curso ese día; su
  `Guiones/` se queda donde está porque su valor es justamente no haber cambiado.

Es idempotente, y hubo que trabajarlo: la primera versión solo guardaba `(?<!Docente)` en las rutas de
texto, así que una segunda corrida en seco pedía convertir `/ "Docente" / "Guiones"` en
`/ "Docente" / "Docente" / "Guiones"` en 8 archivos de código. Ahora cada patrón lleva su guardia, y un
`Guiones/` a secas —el de un árbol de carpetas o el del `LEEME` que ya vive dentro de `Docente/`— se
deja quieto porque ahí ya es la ruta correcta. Corriéndolo hoy sobre el repositorio migrado: 0 archivos.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EXT = {".md", ".py", ".json", ".mdc", ".txt", ".csv", ".cjs", ".js", ".yml", ".yaml"}
FUERA = {
    # Él mismo: sus patrones y su docstring nombran las dos rutas, la vieja y la nueva.
    "config/_migrar_guiones_a_docente.py",
    "config/slides/alinear_narracion.py",
    "config/slides/build_daw_capturas.py",
    "config/slides/shots_desarrollo_moviles_1.py",
    "config/capturar_pantallas_examlab.cjs",
}

# Ruta con prefijo: «X/Guiones» o «X\Guiones» — se respeta el separador que ya traía.
RE_RUTA = re.compile(r"(?<!Docente)([/\\])Guiones(?!\w)")
# Mención relativa que arranca en «Guiones/»: `Guiones/Capturas/`, Guiones/Sesion 01 - ….md
RE_RELATIVA = re.compile(r"(?<![\w/\\])Guiones([/\\])")
# Construcción de rutas en Python: `X / "Guiones"` y `os.path.join(x, "Guiones")`. El grupo opcional
# es el guardia de idempotencia: si «Docente» ya viene delante, se deja como está.
RE_PATHLIB = re.compile(r'("Docente"\s*)?/\s*"Guiones"')
RE_JOIN = re.compile(r'(,\s*"Docente")?,\s*"Guiones"')
# Línea de árbol de carpetas o de glosario: solo sangría, comillas o viñeta antes de «Guiones/».
RE_ARBOL = re.compile(r"^[\s`|+\\/*-]*Guiones[/\\]")


def reescribir(texto: str, rel: str = "") -> str:
    t = RE_RUTA.sub(lambda m: f"{m.group(1)}Docente{m.group(1)}Guiones", texto)
    t = RE_PATHLIB.sub(lambda m: m.group(0) if m.group(1) else '/ "Docente" / "Guiones"', t)
    t = RE_JOIN.sub(lambda m: m.group(0) if m.group(1) else ', "Docente", "Guiones"', t)
    # «Guiones/» a secas es ambiguo: dentro de un archivo que ya vive en `Docente/`, o dibujado en un
    # árbol de carpetas donde `Docente/` es la línea de arriba, ya es la ruta correcta y prefijarlo la
    # rompe. Solo se toca cuando hay texto real antes en la línea y el archivo está fuera de `Docente/`.
    if "/Docente/" not in f"/{rel}":
        t = "\n".join(
            ln if RE_ARBOL.match(ln) else RE_RELATIVA.sub(lambda m: f"Docente{m.group(1)}Guiones{m.group(1)}", ln)
            for ln in t.split("\n")
        )
    return t


def candidatos():
    for f in sorted(RAIZ.rglob("*")):
        rel = str(f.relative_to(RAIZ)).replace("\\", "/")
        if not f.is_file() or f.suffix.lower() not in EXT:
            continue
        if (rel.startswith(".git/") or "__pycache__" in rel
                or "_Archivo obsoleto" in rel or rel in FUERA):
            continue
        yield f, rel


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    aplicar = "--aplicar" in sys.argv
    tocados = lineas = 0
    for f, rel in candidatos():
        try:
            antes = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "Guiones" not in antes:
            continue
        despues = reescribir(antes, rel)
        if despues == antes:
            continue
        tocados += 1
        n = sum(1 for a, b in zip(antes.splitlines(), despues.splitlines()) if a != b)
        lineas += n
        print(f"\n-- {rel}  ({n} lineas)")
        for a, b in zip(antes.splitlines(), despues.splitlines()):
            if a != b:
                print(f"   - {a.strip()[:140]}")
                print(f"   + {b.strip()[:140]}")
        if aplicar:
            f.write_text(despues, encoding="utf-8")
    print(f"\n{'APLICADO' if aplicar else 'EN SECO'}: {tocados} archivos, {lineas} lineas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
