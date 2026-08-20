# -*- coding: utf-8 -*-
"""Capturas reales (Chrome headless) para guías docentes prácticas CUN.

Uso:
  python config/slides/capture_herramientas_practicas.py
  python config/slides/capture_herramientas_practicas.py --only creatividad_s01
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Raíz del workspace derivada del propio archivo. Antes estaba hardcodeada como
# «G:\\Mi unidad\\...» y rompía cuando Google Drive monta la unidad en inglés
# («G:\\My Drive»). Corregido 2026-08-09.
_WS = Path(__file__).resolve().parents[2]


ROOT = (_WS)
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

CREAT = ROOT / "Pregrado" / "Creatividad y pensamiento innovador"
INV = ROOT / "Pregrado" / "Investigacion en ciencia y tecnologia"
P1 = ROOT / "Especializacion" / "Proyecto I"
TG2 = ROOT / "Pregrado" / "Trabajo de grado 2"
TG3 = ROOT / "Pregrado" / "Trabajo de grado 3"

# (grupo, id_archivo, url, espera_extra_s)
SHOTS = [
    # Creatividad S01 — taller ficha + pizarra
    # (El Padlet salió de aquí el 2026-08-11: con 50 estudiantes el rompehielos es el juego de
    #  Slido, y Slido no se puede capturar sin evento creado. Cuando exista, añadir su URL.)
    ("creatividad_s01", "s01_excalidraw_pizarra", "https://excalidraw.com/", 4),
    ("creatividad_s01", "s01_google_docs_inicio", "https://docs.google.com/document/u/0/?tgif=d", 4),
    ("creatividad_s01", "s01_google_forms_plantilla", "https://docs.google.com/forms/u/0/", 3),
    ("creatividad_s01", "s01_miro_design_thinking", "https://miro.com/templates/design-thinking/", 4),
    ("creatividad_s01", "s01_canva_whiteboard", "https://www.canva.com/es_es/pizarra-online/", 4),
    # Creatividad S02 — mapa utilidad / empatía
    ("creatividad_s02", "s02_excalidraw_mapa", "https://excalidraw.com/", 3),
    ("creatividad_s02", "s02_miro_empathy_map", "https://miro.com/templates/empathy-map/", 4),
    # Creatividad S03/S06 (para matriz y futuros)
    ("creatividad_tools", "dt_ideo_designkit", "https://www.designkit.org/methods", 4),
    ("creatividad_tools", "bmc_canvanizer", "https://canvanizer.com/new/business-model-canvas", 4),
    ("creatividad_tools", "strategyzer_bmc", "https://www.strategyzer.com/library/the-business-model-canvas", 4),
    # Investigación S01 — tablero encuadre (ÚNICO curso que conserva el muro: 20 estudiantes)
    ("investigacion_s01", "inv_s01_padlet", "https://padlet.com/andres_dfx/cun-wruz81hmf9k06gd7", 4),
    # Investigación S06 — Scholar + gestores + bases abiertas (periodo corto)
    ("investigacion_s06", "inv_google_scholar", "https://scholar.google.com/", 3),
    ("investigacion_s06", "inv_scholar_busqueda", "https://scholar.google.com/scholar?q=innovaci%C3%B3n+ingenier%C3%ADa+software+Colombia", 4),
    ("investigacion_s06", "inv_zoterobib", "https://zbib.org/", 4),
    ("investigacion_s06", "inv_scielo", "https://scielo.org/es/", 3),
    ("investigacion_s06", "inv_redalyc", "https://www.redalyc.org/", 3),
    ("investigacion_s06", "inv_google_docs", "https://docs.google.com/document/u/0/?tgif=d", 3),
    # Proyecto I — formulario tutorías + APA + ZoteroBib (sin Padlet: 50 estudiantes → Slido)
    ("proyecto1_s01", "p1_form_tutorias_estudiante", "https://forms.gle/oZ8xCYiUo3KEWr1d9", 5),
    ("proyecto1_s01", "p1_zoterobib", "https://zbib.org/", 3),
    ("proyecto1_s01", "p1_apa_style", "https://apastyle.apa.org/style-grammar-guidelines/citations", 4),
    ("proyecto1_s01", "p1_cun_home", "https://cun.edu.co/", 3),
    # TG — escritura / antiplagio público (sin Padlet: TG2 son 50 y TG3 112 → Slido)
    ("tg_tools", "tg_scholar", "https://scholar.google.com/", 2),
    ("tg_tools", "tg_zoterobib", "https://zbib.org/", 4),
]


def out_dirs(group: str) -> list[Path]:
    """Destinos canónicos: solo `Docente/Guiones/Capturas/` (no Clases/ — carpetas de estudiantes)."""
    mapping = {
        "creatividad_s01": [
            CREAT / "Docente" / "Guiones" / "Capturas" / "Sesion 01",
        ],
        "creatividad_s02": [
            CREAT / "Docente" / "Guiones" / "Capturas" / "Sesion 02",
        ],
        "creatividad_tools": [
            CREAT / "Docente" / "Guiones" / "Capturas" / "Herramientas",
        ],
        "investigacion_s01": [
            INV / "Docente" / "Guiones" / "Capturas" / "Sesion 01",
        ],
        "investigacion_s06": [
            INV / "Docente" / "Guiones" / "Capturas" / "Sesion 06",
        ],
        "proyecto1_s01": [
            P1 / "Docente" / "Guiones" / "Capturas" / "Sesion 01",
        ],
        "tg_tools": [
            TG2 / "Docente" / "Guiones" / "Capturas" / "Herramientas",
            TG3 / "Docente" / "Guiones" / "Capturas" / "Herramientas",
            TG2 / "Docente" / "Guiones" / "Capturas" / "Sesion 01",
            TG3 / "Docente" / "Guiones" / "Capturas" / "Sesion 01",
        ],
    }
    return mapping[group]


def mirror_flat(primary: Path, group: str) -> None:
    """Copia plana en Docente/Guiones/Capturas/ para referenciar desde guiones .md (matriz)."""
    flat_roots = {
        "creatividad_s01": CREAT / "Docente" / "Guiones" / "Capturas",
        "creatividad_s02": CREAT / "Docente" / "Guiones" / "Capturas",
        "creatividad_tools": CREAT / "Docente" / "Guiones" / "Capturas",
        "investigacion_s01": INV / "Docente" / "Guiones" / "Capturas",
        "investigacion_s06": INV / "Docente" / "Guiones" / "Capturas",
        "proyecto1_s01": P1 / "Docente" / "Guiones" / "Capturas",
        "tg_tools": TG2 / "Docente" / "Guiones" / "Capturas",
    }
    root = flat_roots.get(group)
    if not root or not primary.exists():
        return
    root.mkdir(parents=True, exist_ok=True)
    dest = root / primary.name
    if dest.resolve() != primary.resolve():
        shutil.copy2(primary, dest)


def capture(url: str, dest: Path, wait: float = 3.0) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".tmp.png")
    if tmp.exists():
        tmp.unlink()
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1440,900",
        f"--screenshot={tmp}",
        "--virtual-time-budget=8000",
        url,
    ]
    try:
        subprocess.run(cmd, check=False, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        print("TIMEOUT", url)
        return False
    time.sleep(wait * 0.1)
    if not tmp.exists() or tmp.stat().st_size < 2000:
        print("FAIL", dest.name, url)
        if tmp.exists():
            tmp.unlink()
        return False
    if dest.exists():
        dest.unlink()
    tmp.replace(dest)
    print("OK", dest, f"({dest.stat().st_size // 1024} KB)")
    return True


def render_ficha_html(path: Path) -> None:
    """Ficha modelo local (HTML) para pantallazo de modelación en vivo."""
    path.parent.mkdir(parents=True, exist_ok=True)
    html = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"/>
<title>Ficha problema–oportunidad · Creatividad CUN</title>
<style>
  body{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#0C2340;color:#122}
  .wrap{max-width:980px;margin:28px auto;background:#fff;border-radius:12px;overflow:hidden;
        box-shadow:0 12px 40px rgba(0,0,0,.35)}
  header{background:#007433;color:#fff;padding:18px 28px}
  header h1{margin:0;font-size:22px}
  header p{margin:6px 0 0;opacity:.9;font-size:13px}
  main{padding:22px 28px 28px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  .field{border:1.5px solid #d7e3da;border-radius:8px;padding:12px 14px;background:#f7fbf8}
  .field.full{grid-column:1/-1}
  .lbl{font-size:11px;font-weight:700;color:#007433;text-transform:uppercase;letter-spacing:.04em}
  .val{margin-top:6px;font-size:15px;line-height:1.35}
  .tag{display:inline-block;background:#91DC00;color:#0C2340;font-weight:700;
       padding:3px 10px;border-radius:999px;font-size:12px}
  footer{padding:10px 28px 18px;font-size:12px;color:#567;background:#f2f5f3}
</style></head>
<body><div class="wrap">
<header>
  <h1>Ficha problema–oportunidad (modelo en vivo)</h1>
  <p>Creatividad y Pensamiento Innovador · Sesión 01 · Ejemplo: turnos de laboratorio</p>
</header>
<main>
  <div class="grid">
    <div class="field"><div class="lbl">1. Título tentativo</div>
      <div class="val">Reserva visible de laboratorios de Ingeniería</div></div>
    <div class="field"><div class="lbl">5. Tipo de innovación (tentativo)</div>
      <div class="val"><span class="tag">Proceso</span> + posible producto (módulo de reserva)</div></div>
    <div class="field full"><div class="lbl">2. Usuario concreto</div>
      <div class="val">Estudiantes de Ingeniería que reservan laboratorios para prácticas de circuitos / redes (turno mañana y noche).</div></div>
    <div class="field full"><div class="lbl">3. Problema (3–5 líneas)</div>
      <div class="val">Llegan al laboratorio y el equipo ya está ocupado o no hay rastro de quién lo pidió. Pierden entre 40 y 60 minutos por sesión y terminan improvisando en aulas sin el kit correcto.</div></div>
    <div class="field"><div class="lbl">4. Evidencia / síntoma observable</div>
      <div class="val">Colas en puerta del lab; planillas en Excel desactualizadas; quejas en el grupo de WhatsApp del curso.</div></div>
    <div class="field"><div class="lbl">6. Valor esperado (1 frase)</div>
      <div class="val">Que el estudiante sepa con 24 h de anticipación si el puesto está disponible y quién lo tiene asignado.</div></div>
  </div>
</main>
<footer>Modelo docente · CUN — no es la solución final; es el marco del problema.</footer>
</div></body></html>
"""
    path.write_text(html, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="Filtrar por grupo (ej. creatividad_s01)")
    args = ap.parse_args()
    if not CHROME.exists():
        print("Chrome no encontrado:", CHROME)
        return 1

    # Ficha HTML modelo
    ficha = CREAT / "Docente" / "Guiones" / "Capturas" / "Sesion 01" / "s01_ficha_modelo.html"
    render_ficha_html(ficha)
    if not args.only or args.only == "creatividad_s01":
        src = CREAT / "Docente" / "Guiones" / "Capturas" / "Sesion 01" / "s01_ficha_modelo.png"
        capture(ficha.as_uri(), src, 1)
        if src.exists():
            mirror_flat(src, "creatividad_s01")

    ok = 0
    fail = 0
    failed_urls: list[str] = []
    for group, fid, url, wait in SHOTS:
        if args.only and group != args.only:
            continue
        dirs = out_dirs(group)
        primary = dirs[0] / f"{fid}.png"
        if capture(url, primary, wait):
            ok += 1
            for d in dirs[1:]:
                d.mkdir(parents=True, exist_ok=True)
                (d / f"{fid}.png").write_bytes(primary.read_bytes())
            mirror_flat(primary, group)
        else:
            fail += 1
            failed_urls.append(f"{fid} <- {url}")
    print(f"\nListo: {ok} OK · {fail} FAIL")
    if failed_urls:
        print("FALLIDOS (usar home usable o captura manual en clase):")
        for line in failed_urls:
            print(" -", line.encode("ascii", "replace").decode("ascii"))
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
