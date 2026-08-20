# -*- coding: utf-8 -*-
"""Antes de migrar: ¿el taller nuevo dice todo lo concreto que decía el viejo?

Un refactor de texto puede perder una instrucción sin que nada falle. Esto respalda los 45
talleres tal como están hoy en los JSON y compara **lo verificable** —nombre de archivo,
herramientas, cifras y palabras técnicas— entre la versión vieja y la que produce `talleres.py`.
No compara prosa: compara lo que el estudiante podría echar en falta.
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import talleres as T  # noqa: E402

ES_TALLER = re.compile(r"^\s*taller\b", re.IGNORECASE)
RESPALDO = os.path.join(os.environ.get("TEMP", "/tmp"), "talleres_originales.json")

# Lo que sí importa que sobreviva: herramientas, formatos y nombres propios de técnicas.
TERMINOS = [
    "excalidraw", "canvanizer", "zoterobib", "zbib", "scholar", "académico", "scielo", "redalyc",
    "canva", "google doc", "google slides", "patents", "unesco", "tesauro", "apa 7", "pdf",
    "scamper", "hmw", "foda", "canvas", "mvp", "oslo", "imrad", "ctrl+f", "ctrl + f",
    "sangría francesa", "incógnito", "cdigital", "drive", "plantilla apa cun",
]

orig = {}
for ruta in sorted(glob.glob(os.path.join(_HERE, "content", "cun_*_s*.json"))):
    m = re.search(r"^cun_(.+)_s(\d\d)\.json$", os.path.basename(ruta))
    if not m:
        continue
    data = json.load(open(ruta, encoding="utf-8"))
    if not isinstance(data, list):
        continue
    for b in data:
        if isinstance(b, dict) and ES_TALLER.match(str(b.get("title", ""))):
            orig["%s|%s" % (m.group(1), int(m.group(2)))] = b

with open(RESPALDO, "w", encoding="utf-8") as fh:
    json.dump(orig, fh, ensure_ascii=False, indent=2)
print("respaldo de %d talleres originales → %s\n" % (len(orig), RESPALDO))


def texto(blocks):
    out = []
    for b in blocks:
        out += [str(b.get("title") or ""), str(b.get("sub") or ""), str(b.get("note") or "")]
        out += [str(x) for x in (b.get("bullets") or [])]
    return " ".join(out).lower()


faltan_terminos = faltan_archivo = 0
for k, viejo in sorted(orig.items()):
    curso, n = k.split("|")[0], int(k.split("|")[1])
    nuevo = T.bloques(curso, n)
    tv, tn = texto([viejo]), texto(nuevo)
    ref = "%s s%02d" % (curso, n)

    perdidos = [t for t in TERMINOS if t in tv and t not in tn]
    if perdidos:
        faltan_terminos += 1
        print("%-16s pierde: %s" % (ref, ", ".join(perdidos)))

    arch = re.findall(r"s\d\d_[a-z0-9]+_apellidos?", tv)
    if arch and arch[0] not in tn:
        faltan_archivo += 1
        print("%-16s el nombre de archivo «%s» no aparece en el nuevo" % (ref, arch[0]))

print("\n%d talleres · %d con término perdido · %d con archivo perdido"
      % (len(orig), faltan_terminos, faltan_archivo))
