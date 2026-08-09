# -*- coding: utf-8 -*-
"""Genera CSV mínimo de hitos docentes (entregas / trámites) para Google Calendar.

Salida: <curso>/2026/<grupo>/Entregas y hitos docentes - Importar a Calendar.csv
        + copia en raíz del curso (mismo nombre).

Solo lo esencial: deadlines ACA (+ auto/coeval P1), Acuerdo/informe AFI,
recepción/cierre. NO incluye encuentros semanales (viven en Encuentros…csv/ics).
NO satura con aperturas ACA ni recordatorios AFI quincenales.
"""
from __future__ import annotations

import csv
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "config" / "cursos"))
from carga_academica import load_carga  # type: ignore
from fechas_entrega_aca import hitos_aca_rows  # type: ignore
from sesiones_cun import (  # type: ignore
    COANFITRION_MEET_AFI,
    LINK_ACUERDO_PEDAGOGICO,
    LINK_INFORME_CIERRE,
    LINK_REGISTRO_DOCENTE_AFI,
    LINK_TUTORIAS,
)

OUT_NAME = "Entregas y hitos docentes - Importar a Calendar.csv"

MEET_PH = "[URL Meet — mismo enlace toda la serie · {curso}]"
CDIGITAL_PH = "[URL CDigital — campus del curso pendiente]"

HEADERS = [
    "Subject",
    "Start Date",
    "Start Time",
    "End Date",
    "End Time",
    "All Day Event",
    "Description",
    "Location",
    "Private",
]


def md(d: date) -> str:
    return d.strftime("%m/%d/%Y")


def row(subject: str, d: date, description: str, location: str = "") -> dict:
    return {
        "Subject": subject,
        "Start Date": md(d),
        "Start Time": "",
        "End Date": md(d),
        "End Time": "",
        "All Day Event": "True",
        "Description": description.replace("\n", " "),
        "Location": location,
        "Private": "False",
    }


def monday_on_or_after(d: date) -> date:
    return d + timedelta(days=(7 - d.weekday()) % 7)


def mid_period_monday(inicio: date, cierre: date) -> date:
    """Un solo lunes a mitad del periodo (recordatorio AFI, no serie quincenal)."""
    mid = inicio + (cierre - inicio) / 2
    return monday_on_or_after(mid)


def build_esp_rows(curso_titulo: str, grupo: str, g: dict) -> list[dict]:
    inicio = date.fromisoformat(g["inicio"])
    recepcion = date.fromisoformat(g["recepcion"])
    cierre = date.fromisoformat(g["cierre"])
    meet = MEET_PH.format(curso=curso_titulo)
    tag = f"{curso_titulo} · {grupo}"
    rows: list[dict] = []

    # 1) Inicio consolidado: Acuerdo + Meet/grabación + 10/08 + links AFI
    rows.append(
        row(
            f"[HITOS] {tag} — Inicio · Acuerdo · Meet/grabación AFI",
            inicio,
            "Inicio del periodo. Socializar y diligenciar Acuerdo Pedagógico "
            f"(distinto del Informe de cierre): {LINK_ACUERDO_PEDAGOGICO}. "
            f"Configurar Meet: coanfitrión OBLIGATORIO {COANFITRION_MEET_AFI}; "
            "habilitar grabación; invitar SOLO ese correo + estudiantes inscritos; "
            "programar toda la serie. "
            "Lunes 10/08/2026: clase P1 debe realizarse y grabarse (Coordinación AFI). "
            f"Registro docente cada sesión/tutoría <24h + link grabación: {LINK_REGISTRO_DOCENTE_AFI}. "
            f"Tutorías estudiante: {LINK_TUTORIAS}. "
            f"Meet: {meet} · CDigital: {CDIGITAL_PH}. "
            "Encuentros semanales: importar CSV/ICS Encuentros… (no este archivo).",
            meet,
        )
    )

    # 2) Deadlines ACA + auto/coeval (sin aperturas)
    for label, d, note in hitos_aca_rows("proyecto1", grupo, esencial=True):
        rows.append(
            row(
                f"[HITOS] {tag} — {label}",
                d,
                f"{note} CDigital: {CDIGITAL_PH}",
                CDIGITAL_PH,
            )
        )

    # 3) Un solo recordatorio AFI a mitad de periodo (no uno por sesión ni quincenal)
    mid = mid_period_monday(inicio, cierre)
    if mid != inicio and mid < cierre:
        rows.append(
            row(
                f"[HITOS] {tag} — Recordatorio registro sesiones AFI (mitad periodo)",
                mid,
                "Práctica continua: registrar CADA sesión/tutoría dentro de 24h "
                f"(solo docente) con enlace de grabación: {LINK_REGISTRO_DOCENTE_AFI}. "
                f"Tutorías estudiante: {LINK_TUTORIAS}. "
                "No hay un evento por clase aquí — el checklist post-clase está en cada guión.",
            )
        )

    # 4) Recepción / cierre / informe
    rows.append(
        row(
            f"[HITOS] {tag} — Recepción máxima de trabajos",
            recepcion,
            f"Fecha máxima de recepción de trabajos (portal/carga académica). "
            f"CDigital: {CDIGITAL_PH}",
            CDIGITAL_PH,
        )
    )
    rows.append(
        row(
            f"[HITOS] {tag} — Cierre de notas",
            cierre,
            "Cierre oficial y registro de TODAS las calificaciones en CDigital. "
            f"Fecha válida Coordinación AFI. CDigital: {CDIGITAL_PH}",
            CDIGITAL_PH,
        )
    )
    informe = cierre + timedelta(days=3)
    while informe.weekday() >= 5:
        informe += timedelta(days=1)
    rows.append(
        row(
            f"[HITOS] {tag} — Informe de cierre Proyecto I/II",
            informe,
            "Informe Final de Curso (plazo orientativo: 3 días hábiles tras cierre). "
            f"Form Informe de cierre: {LINK_INFORME_CIERRE} · "
            f"Acuerdo Pedagógico (inicio, otro form): {LINK_ACUERDO_PEDAGOGICO}",
        )
    )
    return rows


def build_pregrado_rows(curso_titulo: str, grupo: str, g: dict) -> list[dict]:
    inicio = date.fromisoformat(g["inicio"])
    recepcion = date.fromisoformat(g["recepcion"])
    cierre = date.fromisoformat(g["cierre"])
    meet = MEET_PH.format(curso=curso_titulo)
    tag = f"{curso_titulo} · {grupo}"
    rows: list[dict] = []

    rows.append(
        row(
            f"[HITOS] {tag} — Inicio / Syllabus (acuerdo: confirmar)",
            inicio,
            "Inicio del periodo pregrado. Socializar Syllabus y reglas del curso. "
            "Acuerdo pedagógico: PENDIENTE CONFIRMAR canal/formulario con Coordinación "
            "(NO asumir el form AFI de Proyecto I/II). "
            f"Meet: {meet} · CDigital: {CDIGITAL_PH} · "
            "Eval. orientativa Art. 52: Corte1 30% · Corte2 30% · Corte3 40% (confirmar EV en CDigital). "
            "Encuentros semanales: importar CSV/ICS Encuentros… (no este archivo).",
            meet,
        )
    )

    course_key = g.get("_course_key")
    if course_key:
        for label, d, note in hitos_aca_rows(course_key, grupo, esencial=True):
            rows.append(
                row(
                    f"[HITOS] {tag} — {label}",
                    d,
                    f"{note} CDigital: {CDIGITAL_PH}",
                    CDIGITAL_PH,
                )
            )
    else:
        rows.append(
            row(
                f"[HITOS] {tag} — Corte / entregable final · recepción",
                recepcion,
                "Fecha máxima de recepción de trabajos (carga académica). "
                f"CDigital: {CDIGITAL_PH}",
                CDIGITAL_PH,
            )
        )

    rows.append(
        row(
            f"[HITOS] {tag} — Cierre de notas / evidencias (confirmar)",
            cierre,
            "Cierre del grupo según carga académica. "
            "PENDIENTE CONFIRMAR con Coordinación: canal oficial de cargue/cierre de notas "
            "(CDigital vs portal académico) y si hay informe de cierre de pregrado. "
            "Respaldar evidencias (entregas, calificaciones, foros). "
            "NO usar el form de Informe de cierre AFI (Proyecto I/II) salvo indicación explícita. "
            f"CDigital: {CDIGITAL_PH}",
            CDIGITAL_PH,
        )
    )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"OK {path.relative_to(ROOT)} ({len(rows)} eventos)")


def dedupe(rows: list[dict]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []
    for r in rows:
        k = (r["Subject"], r["Start Date"])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def main() -> None:
    carga = load_carga()
    written: list[str] = []
    for key, curso in carga["cursos"].items():
        folder = ROOT / curso["folder"]
        titulo = curso["titulo_corto"]
        nivel = curso["nivel"]
        grupos = list(curso["grupos"].items())
        combined: list[dict] = []
        for grupo, g in grupos:
            g = dict(g)
            g["_course_key"] = key
            if nivel == "especializacion":
                rows = build_esp_rows(titulo, grupo, g)
            else:
                rows = build_pregrado_rows(titulo, grupo, g)
            deduped = dedupe(rows)
            combined.extend(deduped)
            dest_grupo = folder / "2026" / grupo / OUT_NAME
            write_csv(dest_grupo, deduped)
            written.append(str(dest_grupo.relative_to(ROOT)))
            if len(grupos) > 1:
                dest_raiz_g = folder / f"Entregas y hitos docentes - Grupo {grupo} - Importar a Calendar.csv"
                write_csv(dest_raiz_g, deduped)
                written.append(str(dest_raiz_g.relative_to(ROOT)))
        write_csv(folder / OUT_NAME, dedupe(combined))
        written.append(str((folder / OUT_NAME).relative_to(ROOT)))
    print(f"\nTotal archivos: {len(written)}")


if __name__ == "__main__":
    main()
