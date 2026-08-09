# -*- coding: utf-8 -*-
"""One-shot: reescribe cabecera/main de _regen_guiones_creatividad.py."""
from __future__ import annotations

import re
from pathlib import Path

path = Path(
    r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\Pregrado"
    r"\Creatividad y pensamiento innovador\Guiones\_regen_guiones_creatividad.py"
)
text = path.read_text(encoding="utf-8")

new_header = '''# -*- coding: utf-8 -*-
"""Regenera guiones docentes de Creatividad (EI004) — solo .md, 60 min, con pantallazos.

Alineado a config/cursos/sesiones_cun.py (7 sesiones del periodo).
Sesión 01 = modelo de calidad; se omite al regenerar si ya existe (salvo --force-s01).
"""
from __future__ import annotations
import os, sys, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "config", "slides"))
CURSOS = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "config", "cursos"))
sys.path.insert(0, SLIDES)
sys.path.insert(0, CURSOS)

from sesiones_cun import COURSES, meet_placeholder  # noqa: E402
from cun_slides_engine import PADLET_PRESENTACION_URL  # noqa: E402

MEET = meet_placeholder(COURSES["creatividad"]["titulo"])


def topic_filename(titulo: str, max_len: int = 70) -> str:
    s = re.sub(r'[<>:"/\\\\|?*]', "", titulo.strip())
    s = re.sub(r"\\s+", " ", s).strip(" .")
    return (s[:max_len] or "Tema").rstrip()


def sesiones_meta():
    """(n, label_archivo, titulo, detalle) desde sesiones_cun."""
    out = []
    for s in COURSES["creatividad"]["sesiones"]:
        n = s["n"]
        titulo = s["titulo"]
        label = f"Sesion {n:02d} - {topic_filename(titulo)}"
        out.append((n, label, titulo, s.get("detalle", "")))
    return out


SESIONES = sesiones_meta()


def shot(rel_path: str, caption: str, tip: str) -> str:
    return (
        f"\\n![{caption}](Capturas/{rel_path})\\n\\n"
        f"> **En pantalla:** {tip}\\n"
    )


# Pantallazos por sesión canónica (n)
SHOTS = {
    1: {
        "demo": [
            ("Sesion 01/s01_padlet.png", "Padlet — Preséntate",
             f"Presentación del Curso → PRESÉNTATE. URL: {PADLET_PRESENTACION_URL}. ~7 min."),
            ("Sesion 01/s01_ficha_modelo.png", "Ficha problema–oportunidad (modelo)",
             "Proyectar la ficha modelo; llenar campos en vivo (usuario, dolor, tipo tentativo)."),
        ],
        "taller": [
            ("Sesion 01/s01_excalidraw_pizarra.png", "Excalidraw — pizarra",
             "Abrir https://excalidraw.com/ sin cuenta; boceto del problema si ayuda."),
            ("Sesion 01/s01_google_docs_inicio.png", "Google Docs — entrega",
             "Estudiante redacta/pega la ficha y sube a CDigital."),
        ],
    },
    2: {
        "demo": [
            ("Sesion 01/s01_miro_design_thinking.png", "Miro — Design Thinking (plantilla free)",
             "Mostrar etapas DT; plan B: Excalidraw si Miro pide login."),
            ("s01_excalidraw_pizarra.png", "Excalidraw — HMW + banco de ideas",
             "Escribir 1 How Might We y 10 ideas en voz alta."),
        ],
        "taller": [
            ("Herramientas/dt_ideo_designkit.png", "IDEO Design Kit (referencia)",
             "Solo si carga bien; si no, continuar en Excalidraw/Miro free."),
        ],
    },
    3: {
        "demo": [
            ("s01_google_docs_inicio.png", "Docs — tabla Oslo",
             "Clasificar 3 casos en producto/proceso/organización/marketing/social."),
        ],
        "taller": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — ficha Oslo de su propuesta",
             "Tipo dominante + secundario + 1 justificación."),
        ],
    },
    4: {
        "demo": [
            ("s01_google_docs_inicio.png", "Docs — matriz tipos de innovación",
             "Filas = tipos Oslo; columnas = ejemplo / su propuesta."),
        ],
        "taller": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — cuadro comparativo",
             "Mejora socio-económica vs. tipo elegido."),
        ],
    },
    5: {
        "demo": [
            ("Herramientas/bmc_canvanizer.png", "Canvanizer — Business Model Canvas",
             "Abrir https://canvanizer.com/new/business-model-canvas; llenar 3 bloques clave en vivo."),
            ("Herramientas/strategyzer_bmc.png", "Strategyzer BMC (referencia visual)",
             "Solo referencia; el trabajo se hace en Canvanizer/Excalidraw/Docs."),
        ],
        "taller": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — FODA + MVP",
             "FODA 4 cuadrantes + hipótesis de MVP en 5 líneas."),
            ("s01_google_docs_inicio.png", "Docs — consolidar Canvas/MVP",
             "Pegar captura o texto del Canvas y subir a CDigital."),
        ],
    },
    6: {
        "demo": [
            ("s01_google_docs_inicio.png", "Docs — matriz de vigilancia",
             "Columnas: señal / fuente / implicación para mi propuesta."),
        ],
        "taller": [
            ("s01_google_docs_inicio.png", "Scholar en otra pestaña + matriz",
             "Abrir https://scholar.google.com/; anotar 3 señales tecnológicas."),
        ],
    },
    7: {
        "demo": [
            ("s01_google_docs_inicio.png", "Docs — mapa de entidades de apoyo",
             "Mínimo 3 entidades reales (nombre correcto) + pedido concreto."),
        ],
        "taller": [
            ("s01_excalidraw_pizarra.png", "Pitch 60 s — guion",
             "Ensayar con cronómetro; 4 voluntarios. Canva free opcional para 1 slide."),
        ],
    },
}


def inject_shots(md: str, n: int) -> str:
    cfg = SHOTS.get(n) or {}
    demo = "".join(shot(*t) for t in cfg.get("demo", []))
    taller = "".join(shot(*t) for t in cfg.get("taller", []))
    if demo and "#### 3️⃣" in md:
        md = md.replace("#### 3️⃣", demo + "\\n#### 3️⃣", 1)
    elif demo:
        md = md + "\\n\\n### Pantallazos (demo)\\n" + demo
    if taller and "#### 4️⃣" in md:
        md = md.replace("#### 4️⃣", taller + "\\n#### 4️⃣", 1)
    elif taller:
        md = md + "\\n\\n### Pantallazos (taller)\\n" + taller
    if "Pantallazos de esta sesión" not in md and "Pantallazos en `Guiones/Capturas/`" not in md:
        md = md.replace(
            "✅ **Checklist del docente antes de clase**",
            "✅ **Checklist del docente antes de clase**\\n- [ ] Pantallazos en `Guiones/Capturas/` abiertos",
            1,
        )
    return md

'''

idx = text.find("def header(")
if idx < 0:
    raise SystemExit("header not found")
m_builders = re.search(r"^BUILDERS = \{", text, re.M)
if not m_builders:
    raise SystemExit("BUILDERS not found")

body = text[idx : m_builders.start()]
body = body.replace(
    "Próxima: *Inteligencia emocional, creatividad e innovación*",
    "Próxima: *Creatividad/innovación en I+D · Design Thinking*",
)
body = body.replace(
    "traer a la Sesión 02 **3 bloqueadores personales** que les impiden crear.",
    "traer a la próxima **3 bloqueadores personales** o 1 evidencia de empatía.",
)
body = body.replace("sin listar las 8 unidades", "sin listar todas las unidades")
body = body.replace(
    "los veremos a fondo en las sesiones 4 y 5",
    "los veremos a fondo en las siguientes sesiones (Oslo / tipos)",
)

new_tail = '''
# Builders originales (1..8). Mapa canónico 7 sesiones: 1→1, 2→3, 3→4, 4→5, 5→6, 6→7, 7→8
BUILDERS_LEGACY = {
    1: guion_01,
    2: guion_02,
    3: guion_03,
    4: guion_04,
    5: guion_05,
    6: guion_06,
    7: guion_07,
    8: guion_08,
}

CANON_TO_LEGACY = {1: 1, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}


def _fix_session_numbers(md: str, n: int) -> str:
    md = re.sub(r"Sesión \\*\\*\\d{2}\\*\\*", f"Sesión **{n:02d}**", md)
    md = re.sub(r"Sesión \\d{2}\\b", f"Sesión {n:02d}", md)
    md = re.sub(r"Fin del Guión — Sesión \\d{2}", f"Fin del Guión — Sesión {n:02d}", md)
    md = re.sub(r"ciclo de 8 encuentros", "ciclo de encuentros del Syllabus EI004", md)
    return md


def main(argv=None):
    """Escribe solo .md (guiones docentes = Markdown; sin .docx).

    Sesión 01 = modelo: no se sobrescribe si ya existe (evitar degradar).
    Para forzar S01: ``--force-s01``. Si S01 no existe, se genera siempre.
    """
    argv = list(argv or sys.argv[1:])
    force_s01 = "--force-s01" in argv
    argv = [a for a in argv if a != "--force-s01"]
    only_n = int(argv[0]) if argv and argv[0].isdigit() else None

    metas = sesiones_meta()
    keep = {f"{m[1]}.md" for m in metas}
    for name in os.listdir(ROOT):
        if name.startswith("Sesion ") and name.endswith(".md") and name not in keep:
            try:
                os.remove(os.path.join(ROOT, name))
                print("DEL", name)
            except OSError:
                pass

    for meta in metas:
        n, label, titulo, detalle = meta
        if only_n is not None and n != only_n:
            continue
        md_path = os.path.join(ROOT, f"{label}.md")
        if n == 1 and not force_s01 and os.path.isfile(md_path):
            print("SKIP S01 (modelo en disco; use --force-s01 para sobrescribir)")
            continue
        legacy_n = CANON_TO_LEGACY[n]
        builder = BUILDERS_LEGACY[legacy_n]
        text_md = builder((n, label, titulo, detalle))
        text_md = _fix_session_numbers(text_md, n)
        text_md = inject_shots(text_md, n)
        if n == 1 and "Rompehielos Padlet" not in text_md:
            text_md = text_md.replace(
                "- **Meet (serie del curso):**",
                (
                    f"> **Rompehielos Padlet:** slide PRESÉNTATE de la Presentación del Curso. "
                    f"URL: {PADLET_PRESENTACION_URL}\\n\\n- **Meet (serie del curso):**"
                ),
                1,
            )
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(text_md)
        print("MD", md_path)


if __name__ == "__main__":
    main()
'''

final = new_header + body + new_tail
# The new_header was written with \\n in shot() which in the .py file should be \n inside strings.
# In the triple-quoted new_header above, we used \\n which becomes \n in the written file - good for f-strings.

path.write_text(final, encoding="utf-8")
print("OK", path)
print("lines", len(final.splitlines()))

# smoke import
import importlib.util
spec = importlib.util.spec_from_file_location("cre_regen", path)
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    print("import OK, sesiones", len(mod.SESIONES))
except Exception as e:
    print("IMPORT FAIL", type(e), e)
    raise
