# -*- coding: utf-8 -*-
"""¿El taller que el Docente lee en voz alta es el que el estudiante tiene proyectado?

El guion narra el taller a mano —«En `S07_...`: (1) armen…, (2) escriban…»— mientras la deck lo
saca de `talleres.py`. Son dos copias del mismo contenido, y lo que importa no es que la prosa
coincida, sino que no se **contradigan** en lo verificable: el nombre del archivo y el producto.
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "cursos"))
import talleres as T  # noqa: E402
from sesiones_cun import COURSES  # noqa: E402

malos, abreviados, sin_guion = [], [], []

for curso, c in sorted(COURSES.items()):
    guiones = os.path.join(c["folder"], "Docente", "Guiones")
    for (k, n), e in sorted(T.TALLERES.items()):
        if k != curso:
            continue
        cand = glob.glob(os.path.join(guiones, "Sesion %02d - *.md" % n))
        if not cand:
            sin_guion.append("%s s%02d" % (curso, n))
            continue
        txt = open(cand[0], encoding="utf-8").read()
        ref = "%s s%02d" % (curso, n)

        # 1. ¿nombra OTRO archivo de sesión? Eso sería contradicción, no abreviación.
        otros = {a for a in re.findall(r"S\d\d_[A-Za-z0-9]+_Apellidos?", txt)
                 if a != e["archivo"] and a.startswith("S%02d_" % n)}
        if otros:
            malos.append("%s: el guion nombra %s; la deck, %s" % (ref, sorted(otros), e["archivo"]))
        elif e["archivo"] not in txt:
            malos.append("%s: el guion no nombra el archivo %s" % (ref, e["archivo"]))

        # 2. ¿cuántos pasos de la deck reconoce el guion? (por su verbo inicial)
        vistos = 0
        for p in e["pasos"]:
            clave = re.sub(r"\*\*", "", p).strip().split()[0].lower().rstrip(",.:")
            if len(clave) > 4 and clave in txt.lower():
                vistos += 1
        if vistos < len(e["pasos"]):
            abreviados.append("%s: el guion refleja %d de %d pasos"
                              % (ref, vistos, len(e["pasos"])))

print("CONTRADICCIONES (archivo distinto o ausente): %d" % len(malos))
for m in malos:
    print("   ✗ " + m)
print("\nABREVIACIONES (el guion resume, no contradice): %d de %d talleres"
      % (len(abreviados), len(T.TALLERES)))
for a in abreviados[:8]:
    print("   · " + a)
if len(abreviados) > 8:
    print("   · … y %d más" % (len(abreviados) - 8))
if sin_guion:
    print("\nSIN GUION LOCALIZADO: %s" % ", ".join(sin_guion))
sys.exit(1 if malos else 0)
