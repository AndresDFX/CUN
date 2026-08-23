# -*- coding: utf-8 -*-
"""Puerta previa al depósito: ¿el PDF LLEVA DENTRO lo que SciELO va a buscar?

Por qué existe: SciELO analiza el PDF y exige encontrar en el texto, con encabezado propio, la
declaración de conflicto de intereses, la de disponibilidad de datos, la de uso de Inteligencia
Artificial y el ORCID en formato de enlace. Una remisión del tipo «declarado en la sección 3.12»
NO cuenta: el analizador no la detecta y el envío se atasca. Esto se comprueba ANTES de abrir el
navegador, no después de pelearse con el formulario.

Uso:  python config/investigacion/preflight_pdf.py <archivo.pdf> [más.pdf ...]
Sale con código 1 si a algún PDF le falta una de las cuatro familias de frases.
"""
import re
import sys
from pathlib import Path

from pypdf import PdfReader

ORCID = "orcid.org/0009-0003-6598-432X"

# Cada familia se da por cumplida con que aparezca UNA de sus variantes: los manuscritos van en
# español o en inglés, y algunos repiten el rótulo en los dos idiomas dentro del mismo párrafo.
FAMILIAS = [
    ("Conflicto de intereses", ["Conflict of interest", "Conflicto de intereses",
                                "Conflito de interesses"]),
    ("Disponibilidad de datos", ["Data Availability", "Disponibilidad de datos",
                                 "Disponibilidade de dados"]),
    ("Uso de IA", ["Artificial Intelligence", "Inteligencia Artificial",
                   "Inteligência Artificial"]),
    ("ORCID como enlace", [ORCID]),
]


def texto(ruta: Path) -> tuple[str, int]:
    lector = PdfReader(str(ruta))
    crudo = "\n".join(p.extract_text() or "" for p in lector.pages)
    return re.sub(r"\s+", " ", crudo), len(lector.pages)


def revisar(ruta: Path) -> bool:
    t, paginas = texto(ruta)
    bajo = t.lower()
    print("\n%s  (%d páginas, %d caracteres de texto extraído)" % (ruta.name, paginas, len(t)))
    ok = True
    for etiqueta, variantes in FAMILIAS:
        halladas = [v for v in variantes if v.lower() in bajo]
        if halladas:
            print("  SI  %-26s %s" % (etiqueta, ", ".join(halladas)))
        else:
            print("  NO  %-26s falta: %s" % (etiqueta, " | ".join(variantes)))
            ok = False
    # Fugas típicas de un manuscrito que no está listo para viajar.
    for fuga in ("[PENDIENTE", "eliminar antes del sometimiento"):
        if fuga.lower() in bajo:
            print("  NO  FUGA INTERNA            el PDF contiene «%s»" % fuga)
            ok = False
    print("  ->  %s" % ("LISTO para depositar" if ok else "NO subir: corregir el .md y regenerar"))
    return ok


def main(args):
    if not args:
        print("uso: preflight_pdf.py <archivo.pdf> [más.pdf ...]")
        return 2
    return 0 if all([revisar(Path(a)) for a in args]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
