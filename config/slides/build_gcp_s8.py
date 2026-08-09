# -*- coding: utf-8 -*-
"""Sesión 8 · GCP (UGPP/UMNG) — PRESENTACIÓN ÚNICA de clase (se proyecta).
Teoría con un CONCEPTO antes de cada tema (+ ejemplo). Los ejemplos usan el dataset de
práctica `capacitacion` (datos 'sabor UGPP' que se generan con crear_datos_practica.sql).
La práctica paso a paso va en la 'Guía del estudiante'; el cómo conducir + FAQ en la 'Guía del docente'."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gcp_slides_engine import *

BASE = r"C:\Users\Andre\Downloads\Google Cloud\Sesiones\Sesion 8"
os.makedirs(BASE, exist_ok=True)


def build():
    set_footer("S8 · Refuerzo de SQL")
    prs = new_prs()
    cover(prs, "SESIÓN 8", "Refuerzo de SQL en BigQuery",
          "Presentación de clase", "UGPP · Universidad Militar Nueva Granada")

    content_slide(prs, "¿Qué es BigQuery?", [
        "Es el **almacén de datos analítico** de Google Cloud: guarda **millones de filas** y las consulta en segundos.",
        "Piensa en **una hoja de cálculo gigante en la nube**, pensada para analizar, no para digitar.",
        "Le preguntamos con **SQL** y devuelve **tablas de resultados**.",
        "@@Hoy repasamos 3 preguntas clave sobre nuestros datos: elegir, resumir y cruzar.@@",
    ], sub="Concepto — antes de practicar", idx=2)

    content_slide(prs, "¿Qué es SQL y una consulta?", [
        "**SQL** = la forma estándar de **preguntarle a los datos**.",
        "Una consulta básica tiene tres partes:",
        ("**SELECT** — qué columnas quiero ver.", 1),
        ("**FROM** — de qué tabla las tomo (p. ej. `capacitacion.denuncias`).", 1),
        ("**WHERE** — qué filas me interesan (filtro).", 1),
        "Es como en Excel: elegir columnas, filtrar filas y ordenar — pero sobre datos enormes.",
    ], sub="Concepto", idx=3)

    content_slide(prs, "Tema 1 · SELECT — elegir y filtrar", [
        "**SELECT** elige columnas; **WHERE** filtra; **ORDER BY** ordena; **LIMIT** recorta.",
        "Responde: *“¿las 10 denuncias de mayor valor?”*, *“¿las denuncias de Bogotá?”*.",
        "Es el punto de partida de todo análisis: **ver y acotar** los datos.",
    ], sub="Concepto teórico", idx=4)

    code_slide(prs, "SELECT — ejemplo", [
        "SELECT denuncia_id, fecha, ciudad, estado, valor_presunto",
        "FROM capacitacion.denuncias",
        "ORDER BY valor_presunto DESC",
        "LIMIT 10;",
    ], nota="Las 10 denuncias de mayor valor presunto. En la práctica cada quien lo ejecuta en su cuenta.", idx=5)

    content_slide(prs, "Tema 2 · Agregación y GROUP BY — resumir", [
        "Las **funciones** resumen muchas filas: **SUM** (total), **AVG** (promedio), **COUNT** (cantidad).",
        "**GROUP BY** agrupa por una columna y aplica esas funciones **por grupo**.",
        "Es la idea de una **tabla dinámica de Excel**: “denuncias y valor **por** ciudad”.",
        "@@Regla clave: toda columna del SELECT que no sea función va en el GROUP BY.@@",
    ], sub="Concepto teórico", idx=6)

    code_slide(prs, "GROUP BY — ejemplo", [
        "SELECT ciudad,",
        "  COUNT(*) AS denuncias,",
        "  SUM(valor_presunto) AS valor_total",
        "FROM capacitacion.denuncias",
        "GROUP BY ciudad",
        "ORDER BY denuncias DESC;",
    ], nota="Una fila por ciudad, con su conteo y valor total.", idx=7)

    content_slide(prs, "Tema 3 · JOIN — cruzar tablas", [
        "Los datos viven en varias tablas: las **denuncias** en una, los **aportantes** en otra…",
        "**JOIN** las une por una **columna común** (una llave), p. ej. `aportante_id`.",
        "Así respondemos preguntas que mezclan dos fuentes: *“¿denuncias por sector del aportante?”*.",
        ("**INNER JOIN**: solo lo que coincide. **LEFT JOIN**: todo lo de la izquierda + lo que empate.", 1),
    ], sub="Concepto teórico", idx=8)

    code_slide(prs, "JOIN — ejemplo", [
        "SELECT a.sector, COUNT(*) AS denuncias, SUM(d.valor_presunto) AS valor_total",
        "FROM capacitacion.denuncias  AS d",
        "JOIN capacitacion.aportantes AS a  ON d.aportante_id = a.aportante_id",
        "GROUP BY a.sector",
        "ORDER BY valor_total DESC;",
    ], nota="Cruza cada denuncia con su aportante para totalizar por sector económico.", idx=9)

    content_slide(prs, "Ahora sí: a la práctica 🛠️", [
        "Abran la **Guía del estudiante** (documento) y síganla **en su propia cuenta**.",
        "Entorno: **tu proyecto** + **BigQuery Sandbox** (gratis, sin tarjeta).",
        "Harán: crear proyecto → abrir BigQuery → **crear los datos** (un script) → **SELECT**, **GROUP BY**, **JOIN**.",
        "Y al final, **cada quien resuelve el caso de SU área** con los mismos datos:",
        ("Denuncias · Cartera de administradoras · Comunicaciones (persuasivo) · Cruces (gestión de datos).", 1),
        "📤 **Evidencia:** cada consulta con su resultado (pantallazo).",
    ], sub="La guía los lleva de la mano", idx=10)

    closing(prs, "De preguntar datos… ¡a analizarlos!",
            ["Próxima sesión: cargar y cruzar TUS propios archivos (Excel/CSV/Sheets)."])
    out = os.path.join(BASE, "Presentacion S8 - Refuerzo de SQL en BigQuery.pptx")
    prs.save(out); print("OK", out)


if __name__ == "__main__":
    build()
