# -*- coding: utf-8 -*-
"""Builder GENÉRICO de la presentación de una sesión GCP (UGPP/UMNG) desde un JSON.
Reutiliza gcp_slides_engine (identidad de la plantilla oficial + mejoras). Un JSON por sesión:
  { "kicker","titulo","subtitulo","footer",
    "slides":[ {"type":"content","title","sub","bullets":[...]} |
               {"type":"code","title","sub","code":[...],"nota"} ],
    "cierre":{"mensaje","lineas":[...]} }
Cada bullet es un string o [texto, nivel].  Marcado: **negrita**, @@dorado@@, `codigo`.
Uso: python build_gcp_deck.py <ruta.json> <ruta_salida.pptx>
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gcp_slides_engine import *


def _bullets(items):
    out = []
    for b in items or []:
        if isinstance(b, (list, tuple)):
            out.append((b[0], int(b[1])))
        else:
            out.append(b)
    return out


def build_deck(spec, out_path):
    set_footer(spec.get("footer", ""))
    prs = new_prs()
    cover(prs, spec.get("kicker", ""), spec["titulo"], spec.get("subtitulo"),
          spec.get("meta", "UGPP · Universidad Militar Nueva Granada"))
    idx = 2
    for sl in spec.get("slides", []):
        t = sl.get("type", "content")
        if t == "code":
            code_slide(prs, sl["title"], sl.get("code", []), nota=sl.get("nota"), sub=sl.get("sub"), idx=idx)
        elif t in ("step", "shot", "pantallazo"):
            step_slide(prs, sl["title"], _bullets(sl.get("bullets", sl.get("items", []))),
                       sl.get("image", ""), sub=sl.get("sub"), size=sl.get("size", 15), idx=idx)
        elif t == "table":
            table_content(prs, sl["title"], sl["headers"], sl["rows"], nota=sl.get("nota"),
                          col_w=sl.get("col_w"), sub=sl.get("sub"), idx=idx)
        else:
            content_slide(prs, sl["title"], _bullets(sl.get("bullets")), sub=sl.get("sub"),
                          size=sl.get("size", 16), idx=idx)
        idx += 1
    c = spec.get("cierre")
    if c:
        closing(prs, c.get("mensaje", "¡Gracias!"), c.get("lineas"))
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    prs.save(out_path)
    print("OK", out_path)


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    build_deck(spec, sys.argv[2])
