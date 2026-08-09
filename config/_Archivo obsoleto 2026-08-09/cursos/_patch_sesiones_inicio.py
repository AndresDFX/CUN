# -*- coding: utf-8 -*-
"""Ajusta fechas de sesión < 2026-08-10: elimina encuentros previos al inicio operativo."""
from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

START = date(2026, 8, 10)
PATH = Path(__file__).with_name("sesiones_cun.py")
text = PATH.read_text(encoding="utf-8")

# Solo tocamos el bloque de fechas en sesiones; reescritura puntual P1 + pregrado.
# P1: fusionar 03/08 en 10/08 como Sesión 1; desplazar títulos de las que quedan.


def parse_d(s: str) -> date:
    return datetime.strptime(s, "%d/%m/%Y").date()


# --- Proyecto I: reemplazo explícito del catálogo de fechas ---
old_p1 = '''        "sesiones": [
            {"n": 1, "fecha": "03/08/2026",
             "titulo": "Presentación del curso y fundamentos de investigación", "bloque": "ACA 1",
             "unidad_esp329": "U1",
             "detalle": "ESP329 U1 · Encuadre P-I→P-II · enfoques/ética · acuerdos · tutorías · rompehielos QR/Padlet."},
            {"n": 2, "fecha": "10/08/2026",
             "titulo": "Problema y pregunta de investigación", "bloque": "ACA 1",
             "unidad_esp329": "U2",
             "detalle": "ESP329 U2 · Delimitación del problema · pregunta viable · líneas IA del programa."},
            {"n": 3, "fecha": "24/08/2026",
             "titulo": "Objetivos, justificación, alcances y limitaciones", "bloque": "ACA 1",
             "unidad_esp329": "U3",
             "detalle": "ESP329 U3 · Objetivo general/específicos · justificación · alcances/limitaciones · cierre ACA1 30/08."},
            {"n": 4, "fecha": "07/09/2026",
             "titulo": "Retroalimentación ACA1 · Antecedentes de investigación", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Retro ACA1 · antecedentes (mín. 6 nacionales/internacionales)."},
            {"n": 5, "fecha": "14/09/2026",
             "titulo": "Marco teórico", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Bases teóricas alineadas a pregunta y variables/categorías."},
            {"n": 6, "fecha": "21/09/2026",
             "titulo": "Marco conceptual y marco contextual", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Definiciones operativas y contexto de aplicación."},
            {"n": 7, "fecha": "28/09/2026",
             "titulo": "Marco legal · citación APA 7", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Marco legal si aplica · citación/referencias · cierre ACA2 04/10."},
            {"n": 8, "fecha": "05/10/2026",
             "titulo": "Diseño metodológico: paradigma, enfoque y alcance", "bloque": "Puente",
             "unidad_esp329": "U5",
             "detalle": "ESP329 U5 · Adelantar metodología antes de festivos de ACA3."},
            {"n": 9, "fecha": "19/10/2026",
             "titulo": "Población/muestra, técnicas e instrumentos (propuestos)", "bloque": "ACA 3",
             "unidad_esp329": "U5",
             "detalle": "ESP329 U5 · Instrumentos PROPUESTOS (no aplicados en Proyecto I)."},
            {"n": 10, "fecha": "26/10/2026",
             "titulo": "Planeación, viabilidad e integración del anteproyecto", "bloque": "ACA 3",
             "unidad_esp329": "U6–U7",
             "detalle": "ESP329 U6–U7 · Cronograma, presupuesto e integración · cierre ACA3 08/11."},
            {"n": 11, "fecha": "09/11/2026",
             "titulo": "Integración y evaluación · coevaluación y autoevaluación", "bloque": "Cierre",
             "unidad_esp329": "U7",
             "detalle": "ESP329 U7 · Coherencia final · coevaluación/autoevaluación · última sesión sincrónica."},
        ],'''

new_p1 = '''        "sesiones": [
            {"n": 1, "fecha": "10/08/2026",
             "titulo": "Presentación del curso y fundamentos de investigación", "bloque": "ACA 1",
             "unidad_esp329": "U1",
             "detalle": "ESP329 U1 · Encuadre P-I→P-II · enfoques/ética · acuerdos · tutorías · rompehielos QR/Padlet."},
            {"n": 2, "fecha": "24/08/2026",
             "titulo": "Problema y pregunta de investigación", "bloque": "ACA 1",
             "unidad_esp329": "U2",
             "detalle": "ESP329 U2 · Delimitación del problema · pregunta viable · líneas IA del programa."},
            {"n": 3, "fecha": "31/08/2026",
             "titulo": "Objetivos, justificación, alcances y limitaciones", "bloque": "ACA 1",
             "unidad_esp329": "U3",
             "detalle": "ESP329 U3 · Objetivo general/específicos · justificación · alcances/limitaciones · cierre ACA1 31/08."},
            {"n": 4, "fecha": "07/09/2026",
             "titulo": "Retroalimentación ACA1 · Antecedentes de investigación", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Retro ACA1 · antecedentes (mín. 6 nacionales/internacionales)."},
            {"n": 5, "fecha": "14/09/2026",
             "titulo": "Marco teórico", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Bases teóricas alineadas a pregunta y variables/categorías."},
            {"n": 6, "fecha": "21/09/2026",
             "titulo": "Marco conceptual y marco contextual", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Definiciones operativas y contexto de aplicación."},
            {"n": 7, "fecha": "28/09/2026",
             "titulo": "Marco legal · citación APA 7", "bloque": "ACA 2",
             "unidad_esp329": "U4",
             "detalle": "ESP329 U4 · Marco legal si aplica · citación/referencias · cierre ACA2 28/09."},
            {"n": 8, "fecha": "05/10/2026",
             "titulo": "Diseño metodológico: paradigma, enfoque y alcance", "bloque": "Puente",
             "unidad_esp329": "U5",
             "detalle": "ESP329 U5 · Adelantar metodología antes de festivos de ACA3."},
            {"n": 9, "fecha": "19/10/2026",
             "titulo": "Población/muestra, técnicas e instrumentos (propuestos)", "bloque": "ACA 3",
             "unidad_esp329": "U5",
             "detalle": "ESP329 U5 · Instrumentos PROPUESTOS (no aplicados en Proyecto I)."},
            {"n": 10, "fecha": "26/10/2026",
             "titulo": "Planeación, viabilidad e integración del anteproyecto", "bloque": "ACA 3",
             "unidad_esp329": "U6–U7",
             "detalle": "ESP329 U6–U7 · Cronograma, presupuesto e integración · cierre ACA3 09/11."},
            {"n": 11, "fecha": "09/11/2026",
             "titulo": "Integración y evaluación · coevaluación y autoevaluación", "bloque": "Cierre",
             "unidad_esp329": "U7",
             "detalle": "ESP329 U7 · Coherencia final · coevaluación/autoevaluación · última sesión sincrónica."},
        ],'''

if old_p1 not in text:
    raise SystemExit("Bloque P1 no encontrado — revisar sesiones_cun.py")
text = text.replace(old_p1, new_p1)

# Pregrado: cualquier "fecha": "DD/MM/YYYY" anterior a START → se deja y luego
# un post-proceso renumerará eliminando n con fecha < START dentro de cada curso.
# Más seguro: reemplazos puntuales de primeras fechas conocidas.

repls = {
    # investigacion: quitar 06/08 → primera queda 13/08 como n1 (renumerar abajo)
    '"fecha": "06/08/2026"': '"fecha": "DROP"',
    '"fecha": "05/08/2026"': '"fecha": "DROP"',
    '"fecha": "03/08/2026"': '"fecha": "DROP"',
    '"fecha": "04/08/2026"': '"fecha": "DROP"',
}
for a, b in repls.items():
    text = text.replace(a, b)

# Renumber sessions per course block: parse loosely
# After DROP markers, rebuild n sequentially for each "sesiones": [ ... ]

def renumber_sesiones_block(block: str) -> str:
    # Remove objects with fecha DROP
    parts = re.split(r'(\{\s*"n":\s*\d+,)', block)
    # Simpler: find each session dict
    sessions = list(re.finditer(
        r'\{\s*"n":\s*\d+,\s*"fecha":\s*"([^"]+)",.*?\},?',
        block,
        flags=re.S,
    ))
    if not sessions:
        return block
    kept = []
    for m in sessions:
        if m.group(1) == "DROP":
            continue
        kept.append(m.group(0).rstrip().rstrip(","))
    if not kept:
        return block
    new_items = []
    for i, raw in enumerate(kept, 1):
        raw2 = re.sub(r'"n":\s*\d+', f'"n": {i}', raw, count=1)
        new_items.append("            " + raw2.strip())
    inner = ",\n".join(new_items)
    return re.sub(
        r'"sesiones":\s*\[.*?\]',
        f'"sesiones": [\n{inner}\n        ]',
        block,
        count=1,
        flags=re.S,
    )


# Split by course keys roughly — apply renumber to each sesiones array in file
def renumber_all(src: str) -> str:
    out = []
    pos = 0
    for m in re.finditer(r'"sesiones":\s*\[', src):
        start = m.start()
        # find matching ]
        i = m.end() - 1
        depth = 0
        while i < len(src):
            if src[i] == "[":
                depth += 1
            elif src[i] == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
            i += 1
        else:
            continue
        out.append(src[pos:start])
        block = src[start:end]
        # Only renumber if DROP present
        if "DROP" in block:
            out.append(renumber_sesiones_block('"sesiones": ' + block.split('"sesiones":', 1)[1] if False else block))
            # renumber_sesiones_block expects full '"sesiones": [...]'
            rebuilt = renumber_sesiones_block(block if block.startswith('"sesiones"') else '"sesiones": ' + src[m.end()-1:end])
            # Fix: pass exact slice
            rebuilt = renumber_sesiones_block(src[start:end])
            out[-1] = src[pos:start]  # already appended
            out.append(rebuilt)
        else:
            out.append(src[start:end])
        pos = end
    out.append(src[pos:])
    return "".join(out)


# Cleaner renumber implementation
def renumber_file(src: str) -> str:
    pattern = re.compile(r'"sesiones":\s*\[(.*?)\]', re.S)

    def repl(m):
        body = m.group(1)
        items = re.findall(r'\{[^{}]*\}', body, flags=re.S)
        kept = []
        for it in items:
            fm = re.search(r'"fecha":\s*"([^"]+)"', it)
            if not fm or fm.group(1) == "DROP":
                continue
            kept.append(it)
        if not kept:
            return m.group(0)
        lines = []
        for i, it in enumerate(kept, 1):
            it2 = re.sub(r'"n":\s*\d+', f'"n": {i}', it, count=1)
            lines.append("            " + it2.strip())
        return '"sesiones": [\n' + ",\n".join(lines) + "\n        ]"

    return pattern.sub(repl, src)


text = renumber_file(text)
PATH.write_text(text, encoding="utf-8")
print("OK sesiones_cun.py actualizado (inicio >= 10/08)")
