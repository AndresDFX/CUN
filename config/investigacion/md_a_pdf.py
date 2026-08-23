# -*- coding: utf-8 -*-
"""Markdown -> PDF con reportlab. Existe porque SciELO Preprints solo acepta PDF y esta máquina
no tiene ni Word ni LibreOffice (comprobado), así que no hay ruta docx -> pdf.

No pretende ser un maquetador: pretende producir un PDF legible y completo, que es lo que pide un
servidor de preprints. Respeta encabezados, párrafos, listas, citas en bloque, tablas y código.
"""
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

BASE = getSampleStyleSheet()
E = {
    "h1": ParagraphStyle("h1", parent=BASE["Heading1"], fontSize=15, leading=19, spaceBefore=16,
                         spaceAfter=8, textColor=colors.HexColor("#1a1a1a")),
    "h2": ParagraphStyle("h2", parent=BASE["Heading2"], fontSize=12.5, leading=16, spaceBefore=12,
                         spaceAfter=6),
    "h3": ParagraphStyle("h3", parent=BASE["Heading3"], fontSize=11, leading=14, spaceBefore=10,
                         spaceAfter=4),
    "p": ParagraphStyle("p", parent=BASE["BodyText"], fontSize=10, leading=14.5,
                        alignment=TA_JUSTIFY, spaceAfter=6),
    "cita": ParagraphStyle("cita", parent=BASE["BodyText"], fontSize=9.5, leading=13,
                           leftIndent=14, textColor=colors.HexColor("#444444"), spaceAfter=6),
    "li": ParagraphStyle("li", parent=BASE["BodyText"], fontSize=10, leading=14,
                         leftIndent=14, bulletIndent=4, spaceAfter=3),
    "ref": ParagraphStyle("ref", parent=BASE["BodyText"], fontSize=9, leading=12.5,
                          leftIndent=18, firstLineIndent=-18, spaceAfter=4),
    "titulo": ParagraphStyle("titulo", parent=BASE["Title"], fontSize=17, leading=21, spaceAfter=14),
    "centro": ParagraphStyle("centro", parent=BASE["BodyText"], fontSize=10, leading=14,
                             alignment=TA_CENTER, spaceAfter=4),
}


def _equilibrar(t: str) -> str:
    """Reanida las etiquetas cruzadas en vez de reventar.

    El manuscrito trae marcado cruzado de verdad —`**texto *bootstrap**`—, que es Markdown
    malformado pero se lee bien en cualquier visor. reportlab, en cambio, exige XML válido y aborta
    el documento entero. Aquí se recorre la secuencia de etiquetas con una pila: cuando llega un
    cierre que no es el de arriba, se cierran las intermedias y se reabren después. El texto queda
    igual; solo cambia dónde empiezan y acaban las negritas.
    """
    salida, pila = [], []
    for trozo in re.split(r"(</?(?:b|i)>)", t):
        m = re.fullmatch(r"</?(b|i)>", trozo or "")
        if not m:
            salida.append(trozo)
            continue
        etq, cierre = m.group(1), trozo.startswith("</")
        if not cierre:
            pila.append(etq)
            salida.append(trozo)
        elif etq in pila:
            reabrir = []
            while pila and pila[-1] != etq:            # cierra lo que estorba…
                x = pila.pop()
                salida.append("</%s>" % x)
                reabrir.append(x)
            pila.pop()
            salida.append("</%s>" % etq)
            for x in reversed(reabrir):                # …y lo devuelve a su sitio
                pila.append(x)
                salida.append("<%s>" % x)
    while pila:                                        # nunca dejar una etiqueta abierta
        salida.append("</%s>" % pila.pop())
    return "".join(salida)


def enriquecer(t: str) -> str:
    """Markdown en línea -> etiquetas de reportlab. El escapado va PRIMERO, o se come el marcado."""
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    t = _equilibrar(t)
    t = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', t)
    t = re.sub(r"\[(.+?)\]\((https?://[^)]+)\)", r'<link href="\2" color="#1155cc">\1</link>', t)
    return t


def tabla(filas: list[list[str]]):
    if not filas:
        return None
    ancho = (A4[0] - 4 * cm) / max(1, len(filas[0]))
    datos = [[Paragraph(enriquecer(c), ParagraphStyle("celda", parent=E["p"], fontSize=8,
                                                      leading=10.5, spaceAfter=0)) for c in f]
             for f in filas]
    t = Table(datos, colWidths=[ancho] * len(filas[0]), repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def construir(md: str) -> list:
    flujo, buffer_tabla, en_ref = [], [], False
    lineas = md.splitlines()
    i = 0
    while i < len(lineas):
        ln = lineas[i].rstrip()

        if re.match(r"^\s*\|", ln):
            celdas = [c.strip() for c in ln.strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in celdas):
                buffer_tabla.append(celdas)
            i += 1
            continue
        if buffer_tabla:
            t = tabla(buffer_tabla)
            if t:
                flujo += [Spacer(1, 4), t, Spacer(1, 8)]
            buffer_tabla = []

        if not ln.strip():
            i += 1
            continue
        if re.fullmatch(r"\s*(-{3,}|\*{3,}|_{3,})\s*", ln):
            flujo.append(Spacer(1, 10))
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            nivel, txt = len(m.group(1)), m.group(2).strip()
            en_ref = bool(re.match(r"referencias|bibliograf", txt, re.I))
            if nivel == 1 and not flujo:
                flujo.append(Paragraph(enriquecer(txt), E["titulo"]))
            else:
                flujo.append(Paragraph(enriquecer(txt), E["h1" if nivel <= 1 else
                                                         ("h2" if nivel == 2 else "h3")]))
            i += 1
            continue

        if ln.lstrip().startswith(">"):
            flujo.append(Paragraph(enriquecer(re.sub(r"^\s*>\s?", "", ln)), E["cita"]))
            i += 1
            continue

        m = re.match(r"^\s*([-*+]|\d+[.)])\s+(.*)$", ln)
        if m:
            vinieta = "•" if not m.group(1)[0].isdigit() else m.group(1)
            flujo.append(Paragraph(enriquecer(m.group(2)), E["li"], bulletText=vinieta))
            i += 1
            continue

        # párrafo: junta líneas hasta el siguiente corte
        parrafo = [ln]
        while i + 1 < len(lineas) and lineas[i + 1].strip() and \
                not re.match(r"^\s*(#|\||>|[-*+]\s|\d+[.)]\s|-{3,})", lineas[i + 1]):
            i += 1
            parrafo.append(lineas[i].strip())
        flujo.append(Paragraph(enriquecer(" ".join(parrafo)), E["ref"] if en_ref else E["p"]))
        i += 1

    if buffer_tabla:
        t = tabla(buffer_tabla)
        if t:
            flujo.append(t)
    return flujo


def main() -> int:
    if len(sys.argv) < 3:
        print("uso: md_a_pdf.py <entrada.md> <salida.pdf>")
        return 2
    origen, destino = Path(sys.argv[1]), Path(sys.argv[2])
    doc = SimpleDocTemplate(str(destino), pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm,
                            title=origen.stem, author="")

    def pie(canvas, _doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#777777"))
        canvas.drawCentredString(A4[0] / 2, 1.2 * cm, str(canvas.getPageNumber()))
        canvas.restoreState()

    doc.build(construir(origen.read_text(encoding="utf-8")),
              onFirstPage=pie, onLaterPages=pie)
    print("Escrito %s (%.0f KB, %d páginas)" % (destino, destino.stat().st_size / 1024, doc.page))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
