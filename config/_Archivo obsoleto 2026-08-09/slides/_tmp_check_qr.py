# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\config\slides\assets\qr_presentacion_estudiantes.png")
print("exists", p.exists(), "size", p.stat().st_size if p.exists() else 0)
try:
    from pyzbar.pyzbar import decode
    from PIL import Image
    data = decode(Image.open(p))
    print("pyzbar", [(d.data, d.type) for d in data])
except Exception as e:
    print("pyzbar fail", type(e).__name__, e)
