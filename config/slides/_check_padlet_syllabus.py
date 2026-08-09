# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path
from pptx import Presentation

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos")
url = "https://padlet.com/andres_dfx/cun-wruz81hmf9k06gd7"
paths = sorted(
    set(list(root.rglob("Presentacion del Curso*.pptx")) + list(root.rglob("Sesion 01*/Presentacion.pptx"))),
    key=lambda p: str(p),
)
for p in paths:
    if "Temas" in str(p):
        continue
    prs = Presentation(str(p))
    blob = []
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                blob.append(sh.text_frame.text)
    text = "\n".join(blob)
    has_pad = url in text
    sil_hits = re.findall(r"[Ss][íi]labo|SÍLABO", text, flags=re.IGNORECASE)
    clear = "Clear posts" in text or "3 padlets" in text
    idea = "IdeaBoardz" in text
    status = "OK" if has_pad and not sil_hits and not clear and not idea else "CHK"
    print(
        f"{status} pad={has_pad} sil={sil_hits[:3]!r} clear={clear} idea={idea} | {p.relative_to(root)}"
    )
