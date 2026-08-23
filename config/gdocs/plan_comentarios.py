# -*- coding: utf-8 -*-
r"""
Preparar los comentarios de un documento de estudiante, para publicarlos con Apps Script.

Esta es la mitad que corre en este computador. No toca Google: **no hay credenciales, ni token, ni
proyecto en Google Cloud**. Trabaja sobre la copia que el Docente descargó del documento compartido
(*Archivo → Descargar → Microsoft Word*), y su salida es un `Plan.gs` que se pega en el proyecto de
Apps Script para publicar de verdad. La otra mitad es
`PRINCIPAL - Comentar documentos de estudiantes.gs`.

POR QUÉ LA CITA Y NO EL NÚMERO DE PÁRRAFO
-----------------------------------------
El `.docx` descargado y el documento vivo **no numeran igual** los párrafos: la exportación junta y
parte cosas, y el estudiante sigue editando. Si el comentario viajara con «párrafo 12», acabaría
citando la frase equivocada delante del estudiante. Así que cada comentario viaja con la **cita
literal**, y el Apps Script la busca en el documento vivo antes de publicar: si no la encuentra,
avisa y no inventa. El número de párrafo lo calcula allá, sobre el documento real.

Por eso `_norm()` tiene que ser **idéntica** aquí y en el `.gs`: es la misma comparación hecha dos
veces, y si divergen el aviso sale cuando ya no sirve.

DÓNDE VA EL TRABAJO DEL ESTUDIANTE
----------------------------------
En `_Revisiones/`, que está **ignorada por git** (ver su LEEME). Es material crudo con nombres
propios: se sincroniza a Drive, pero al historial no entra — el mismo criterio que dejó fuera
`3 - Transcripcion.md`.

USO
---
    # 1. Volcar el documento numerado y ver los criterios con que se va a comentar
    python config/gdocs/plan_comentarios.py leer "_Revisiones/ACA1 - Perez.docx" \
        --curso proyecto1 --aca aca1

    # 2. (yo redacto el plan.json)  3. validarlo y emitir el Plan.gs
    python config/gdocs/plan_comentarios.py generar "_Revisiones/ACA1 - Perez.plan.json"

`generar` **no** escribe el `Plan.gs` si algo no cuadra: un criterio que no esté en la guía, un
comentario sin texto, o una cita que no aparezca en el documento.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import criterios_aca as CA  # noqa: E402

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

# Tipografía que Word y Google Docs intercambian a su gusto. Tiene que coincidir carácter por
# carácter con la tabla del `.gs`.
EQUIVALENCIAS = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
    "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-",
    " ": " ", " ": " ", " ": " ", "​": "",
    "…": "...",
}


def norm(s: str) -> str:
    """Normaliza para COMPARAR. Nunca para mostrar: la cita se publica tal como está en el documento."""
    s = unicodedata.normalize("NFC", s)
    for a, b in EQUIVALENCIAS.items():
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def parrafos_docx(ruta: Path) -> list[dict]:
    """Aplana el .docx a párrafos numerados, arrastrando el último encabezado como sección.

    Recorre también las celdas de las tablas: en un anteproyecto el cronograma y el presupuesto van
    en tabla, y son justo dos de los criterios del ACA Final.
    """
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    doc = Document(str(ruta))
    salida: list[dict] = []
    seccion = ""

    def agregar(p) -> None:
        nonlocal seccion
        txt = p.text.strip()
        if not txt:
            return
        estilo = (p.style.name or "") if p.style is not None else ""
        if re.match(r"^(Heading|Título|Titulo|Subtitle)", estilo, re.I):
            seccion = txt
        salida.append({"n": len(salida) + 1, "seccion": seccion, "estilo": estilo, "texto": txt})

    def recorrer(padre) -> None:
        cuerpo = padre.element.body if hasattr(padre.element, "body") else padre._tc
        for hijo in cuerpo.iterchildren():
            if hijo.tag.endswith("}p"):
                agregar(Paragraph(hijo, padre))
            elif hijo.tag.endswith("}tbl"):
                for fila in Table(hijo, padre).rows:
                    for celda in fila.cells:
                        for p in celda.paragraphs:
                            agregar(p)

    recorrer(doc)
    return salida


def leer(ruta: Path, curso: str, aca: str) -> int:
    guia, items = CA.criterios(curso, aca)
    ps = parrafos_docx(ruta)
    print(f"Documento : {ruta.name}")
    print(f"Guía      : {guia}")
    print(f"Párrafos  : {len(ps)}\n")
    print("─── criterios con los que se comenta ───")
    for i, c in enumerate(items, 1):
        print(f"  {i}. {c}")
    print("\n─── documento ───")
    for p in ps:
        sec = f"({p['seccion'][:38]}) " if p["seccion"] else ""
        print(f"[{p['n']:>3}] {sec}{p['texto']}")
    return 0


def generar(ruta_plan: Path) -> int:
    plan = json.loads(ruta_plan.read_text(encoding="utf-8"))
    for campo in ("docId", "curso", "aca", "documento", "comentarios"):
        if not plan.get(campo):
            raise SystemExit(f"El plan no tiene «{campo}».")

    guia, items = CA.criterios(plan["curso"], plan["aca"])
    doc = (ruta_plan.parent / plan["documento"]).resolve()
    if not doc.is_file():
        doc = Path(plan["documento"]).resolve()
    if not doc.is_file():
        raise SystemExit(f"No está el documento descargado: {plan['documento']}")

    ps = parrafos_docx(doc)
    entero = norm(" ".join(p["texto"] for p in ps))
    validos = {norm(c): c for c in items}

    problemas: list[str] = []
    for i, c in enumerate(plan["comentarios"], 1):
        crit, cita, texto = c.get("criterio", ""), c.get("cita", ""), c.get("texto", "")
        if norm(crit) not in validos:
            problemas.append(
                f"#{i}: el criterio «{crit}» no está en la guía. La guía dice:\n      "
                + "\n      ".join(items)
            )
        if not texto.strip():
            problemas.append(f"#{i} «{crit}»: sin `texto`; un comentario vacío no se publica.")
        if not cita.strip():
            problemas.append(f"#{i} «{crit}»: sin `cita`; sin ella el comentario no dice de qué frase habla.")
        elif norm(cita) not in entero:
            problemas.append(
                f"#{i} «{crit}»: la cita NO aparece en el documento.\n"
                f"      cita: «{cita[:90]}…»"
            )

    if problemas:
        print(f"NO se generó el Plan.gs — {len(problemas)} problema(s):\n")
        for p in problemas:
            print("  ✗ " + p)
        return 1

    salida = ruta_plan.with_name(ruta_plan.stem.replace(".plan", "") + " - Plan.gs")
    cuerpo = {
        "docId": plan["docId"],
        "titulo": plan.get("titulo") or doc.stem,
        "curso": plan["curso"],
        "aca": plan["aca"],
        "guia": guia,
        "comentarios": [
            {"criterio": validos[norm(c["criterio"])], "cita": c["cita"].strip(),
             "texto": c["texto"].strip()}
            for c in plan["comentarios"]
        ],
    }
    salida.write_text(
        "// Plan de comentarios — generado por config/gdocs/plan_comentarios.py\n"
        "// Pégalo como el archivo «Plan.gs» del proyecto «CUN - Comentarios» y ejecuta simular().\n"
        f"// Documento: {cuerpo['titulo']}\n"
        f"// Guía     : {guia}\n"
        f"// Criterios comentados: {len(cuerpo['comentarios'])} de {len(items)}\n\n"
        "// Ponlo en true SOLO después de leer la salida de simular().\n"
        "var CONFIRMAR = false;\n\n"
        "var PLAN = " + json.dumps(cuerpo, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"OK  {len(cuerpo['comentarios'])} comentarios · las {len(cuerpo['comentarios'])} citas "
          f"aparecen en el documento · criterios de «{guia}»")
    print(f"    {salida}")
    print("    Pégalo como «Plan.gs» en Apps Script y ejecuta simular().")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("leer", help="Volcar el .docx numerado + los criterios del ACA")
    p.add_argument("docx")
    p.add_argument("--curso", required=True, choices=sorted(CA.CURSOS))
    p.add_argument("--aca", required=True)

    p = sub.add_parser("generar", help="Validar el plan.json y emitir el Plan.gs")
    p.add_argument("plan")

    a = ap.parse_args()
    if a.cmd == "leer":
        return leer(Path(a.docx), a.curso, a.aca)
    return generar(Path(a.plan))


if __name__ == "__main__":
    raise SystemExit(main())
