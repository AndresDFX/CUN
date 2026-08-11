# -*- coding: utf-8 -*-
"""Genera el CSV y el ICS de respaldo de los encuentros de Proyecto I (grupo 54ES4).

Subject: «{periodo} - {grupos} - {Asignatura} - Sesion NN» (helper `subject_encuentro`).
El periodo va delante para que la carpeta de grabaciones, que acumula periodos, no mezcle
dos «Sesion 01» del mismo grupo de años distintos.
Description: 2–4 líneas (sin políticas ni placeholders largos).
Location: enlace único de Meet de la serie, leído de
`carga_academica_2026.json → cursos.proyecto1.meet` (vacío ⇒ sin sala todavía).

Invitados en Google Calendar: la importación .ics/.csv **no** mete Guests (limitación de
Google). Por eso lo que sale de aquí es SOLO respaldo de fechas, y va rotulado
`RESPALDO sin invitados - …`.

El flujo que sí funciona —el `.gs` con invitados y Meet, y su runbook— lo genera
`build_calendar_encuentros.py`, que desde el 2026-08-11 cubre los CINCO cursos. Antes
Proyecto I se generaba aquí y era el único sin rótulo PRINCIPAL/RESPALDO, sin Meet
autogestionado y con un runbook de 114 palabras.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# Raíz del workspace derivada del propio archivo. Antes estaba hardcodeada como
# «G:\\Mi unidad\\...» y rompía cuando Google Drive monta la unidad en inglés
# («G:\\My Drive»). Corregido 2026-08-09.
_WS = Path(__file__).resolve().parents[2]


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))
from sesiones_cun import (  # noqa: E402
    COANFITRION_MEET_AFI,
    COURSES,
    DOCENTE,
    DOCENTE_CORREO,
    LINK_TUTORIAS,
    subject_encuentro,
)
from carga_academica import (  # noqa: E402
    _parse_date as _pdate,
    curso as _carga_curso,
    fmt_dmy as _fmt_dmy,
)

GRUPO = Path(
    _WS / "Especializacion" / "Proyecto I" / "2026" / "54ES4"
)
GROUPS = ["54ES4"]
COURSE_KEY = "proyecto1"
# Enlace ÚNICO de Meet para toda la serie del periodo. FUENTE ÚNICA:
# carga_academica_2026.json → cursos.proyecto1.meet (así el mismo enlace llega también a la
# Presentación del Curso, al LEEME, a los guiones y al CSV de hitos). Si el periodo aún no
# tiene sala, el campo queda "" y el material vuelve a mostrar placeholder (no inventar URL).
LOCATION = (_carga_curso(COURSE_KEY).get("meet") or "").strip()


# Colombia no tiene horario de verano: un solo componente STANDARD en UTC-5.
# RFC 5545 exige VTIMEZONE cuando los eventos usan `TZID=`; sin él, algunos clientes
# (no Google) desplazan la hora del encuentro.
VTIMEZONE_BOGOTA = [
    "BEGIN:VTIMEZONE",
    "TZID:America/Bogota",
    "BEGIN:STANDARD",
    "DTSTART:19930404T000000",
    "TZOFFSETFROM:-0500",
    "TZOFFSETTO:-0500",
    "TZNAME:-05",
    "END:STANDARD",
    "END:VTIMEZONE",
]


def _cn_from_email(em: str) -> str:
    local = em.split("@", 1)[0]
    return " ".join(p.capitalize() for p in re.split(r"[._+\-]+", local) if p)


def _desc(n: int, tema: str, coord: str) -> str:
    """Description mínima (2–4 líneas)."""
    return (
        f"Sesión {n:02d} — {tema}\n"
        f"Form tutorías: {LINK_TUTORIAS}\n"
        f"Coanfitrión: {coord}"
    )


def ics_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _js_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def load_roster_emails(ods: Path) -> list[str]:
    """Correos del grupo. Prioriza el roster extraído de CDigital sobre el .ods histórico.

    El `.ods` que subió el docente se quedó en 40 estudiantes; la matrícula real en el aula
    (auditada el 2026-08-10) es de 50. Se lee el primer archivo disponible en la carpeta del
    grupo por orden de confianza y, si hay varios, se toma el que más correos aporte.
    """
    carpeta = ods.parent
    candidatos = [
        carpeta / "Correos estudiantes (invitados Calendar).txt",
        carpeta / "Listado estudiantes (CDigital).csv",
        ods,
    ]
    mejor: list[str] = []
    for f in candidatos:
        if not f.is_file():
            continue
        try:
            if f.suffix.lower() in {".ods", ".xlsx"}:
                with zipfile.ZipFile(f) as z:
                    data = " ".join(
                        z.read(n).decode("utf-8", "replace")
                        for n in z.namelist() if n.endswith(".xml")
                    )
            else:
                data = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        hallados = sorted(set(re.findall(
            r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", data)))
        if len(hallados) > len(mejor):
            mejor = hallados
    if not mejor:
        raise FileNotFoundError(
            f"No se encontró roster con correos en {carpeta}. "
            "Debe existir «Correos estudiantes (invitados Calendar).txt» "
            "o «Listado estudiantes.ods»."
        )
    return mejor


def build_calendar_payload(grupo: Path | None = None) -> dict:
    """Datos de encuentros + invitados (en memoria; no escribe JSON en disco)."""
    grupo = grupo or GRUPO
    emails = load_roster_emails(grupo / "Listado estudiantes.ods")
    coord = COANFITRION_MEET_AFI
    guests = emails + ([coord] if coord not in emails else [])
    catalog = COURSES[COURSE_KEY]["sesiones"]
    events = []
    for ses in catalog:
        d = datetime.strptime(ses["fecha"], "%d/%m/%Y").date()
        n = int(ses["n"])
        tema = ses["titulo"]
        subject = subject_encuentro(
            COURSE_KEY, GROUPS, n=n, titulo_sesion=tema, autonoma=False,
        )
        desc = _desc(n, tema, coord)
        events.append({
            "n": n,
            "fecha": d.isoformat(),
            "subject": subject,
            "description": desc,
            "start": f"{d.isoformat()}T20:00:00",
            "end": f"{d.isoformat()}T22:00:00",
            "timezone": "America/Bogota",
            "date": d,
            "tema": tema,
        })
    return {
        "course": "proyecto1",
        "group": "54ES4",
        "calendar_id": "primary",
        "timezone": "America/Bogota",
        "location": LOCATION,
        "emails": emails,
        "guests": guests,
        "coanfitrion": coord,
        "send_updates": "none",
        "events": events,
    }


def _sync_txt_grupo() -> None:
    """Refresca los datos volátiles de `Fechas.txt` e `Informacion.txt` desde config.

    Estos dos archivos no tenían generador: quedaron con «Fecha de inicio: 03/08/2026» y
    con el Meet en placeholder mucho después de que la config dijera otra cosa. Aquí solo
    se reescriben las líneas de dato (no el texto explicativo), así que es idempotente.
    """
    c = _carga_curso(COURSE_KEY)
    campos = {
        "Fecha de inicio:": _fmt_dmy(_pdate(c["inicio"])),
        "Fecha máxima para recepción de trabajos:": _fmt_dmy(_pdate(c["recepcion"])),
        "Recepción de trabajos:": _fmt_dmy(_pdate(c["recepcion"])),
        "Fecha de cierre:": _fmt_dmy(_pdate(c["cierre"])),
    }
    for nombre in ("Fechas.txt", "Informacion.txt"):
        path = GRUPO / nombre
        if not path.is_file():
            continue
        out = []
        for linea in path.read_text(encoding="utf-8").split("\n"):
            limpio = linea.strip()
            for clave, valor in campos.items():
                if limpio.startswith(clave):
                    resto = limpio[len(clave):].strip()
                    cola = ""
                    if "(" in resto:
                        cola = " " + resto[resto.index("("):]
                    linea = f"{clave} {valor}{cola}"
                    break
            else:
                if limpio.startswith("- Un solo enlace para toda la serie:"):
                    linea = (
                        "  - Un solo enlace para toda la serie: "
                        + (LOCATION or "[URL Meet — pendiente]")
                    )
            out.append(linea)
        path.write_text("\n".join(out), encoding="utf-8")
        print("OK sync", path.name)


# _write_apps_script() y _write_leeme() vivían aquí. Retirados el 2026-08-11: el `.gs` y
# el runbook de Proyecto I los emite ahora `build_calendar_encuentros.py`, el mismo que los
# de los otros cuatro cursos. Dejarlos habría significado dos generadores compitiendo por
# el mismo archivo, que es justo como Proyecto I se quedó atrás.


def main() -> None:
    grupo = GRUPO
    payload = build_calendar_payload(grupo)
    emails = payload["emails"]
    guests = payload["guests"]
    coord = payload["coanfitrion"]
    events = payload["events"]
    guests_csv = ", ".join(guests)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    rows_out = []
    ics_events: list[str] = []
    for ev in events:
        d = ev["date"]
        rows_out.append({
            "Subject": ev["subject"],
            "Start Date": d.strftime("%m/%d/%Y"),
            "Start Time": "8:00 PM",
            "End Date": d.strftime("%m/%d/%Y"),
            "End Time": "10:00 PM",
            "All Day Event": "False",
            "Description": ev["description"].replace("\n", " | "),
            "Location": LOCATION,
            "Private": "False",
            "Guests": guests_csv,
        })
        uid = f"proyecto1-encuentro-{d.isoformat()}@cun.edu.co"
        ics_events += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{stamp}",
            f"DTSTART;TZID=America/Bogota:{d.strftime('%Y%m%d')}T200000",
            f"DTEND;TZID=America/Bogota:{d.strftime('%Y%m%d')}T220000",
            f"SUMMARY:{ics_escape(ev['subject'])}",
            f"DESCRIPTION:{ics_escape(ev['description'])}",
        ]
        if LOCATION:
            ics_events.append(f"LOCATION:{ics_escape(LOCATION)}")
        ics_events += [
            f"ORGANIZER;CN={ics_escape(DOCENTE)}:mailto:{DOCENTE_CORREO}",
            "STATUS:CONFIRMED",
            "SEQUENCE:0",
        ]
        for em in guests:
            cn = ics_escape(_cn_from_email(em))
            ics_events.append(
                f"ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;"
                f"PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN={cn}:mailto:{em}"
            )
        ics_events.append("END:VEVENT")

    csv_path = grupo / "RESPALDO sin invitados - Encuentros Proyecto I - Grupo 54ES4.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)

    mails_path = grupo / "Correos estudiantes (invitados Calendar).txt"
    mails_path.write_text(
        "Correos invitados (estudiantes 54ES4). El coanfitrión se añade aparte en el script.\n"
        "NO uses import CSV/ICS para invitados: Google Calendar descarta Guests/ATTENDEE.\n"
        "Flujo correcto: ejecutar «PRINCIPAL - Crear encuentros con invitados.gs» (Apps Script).\n"
        f"Coanfitrión: {coord}\n\n"
        + "\n".join(emails) + "\n",
        encoding="utf-8",
    )

    ics_path = grupo / "RESPALDO sin invitados - Encuentros Proyecto I - Grupo 54ES4.ics"
    ics_path.write_text(
        "\r\n".join([
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//CUN//Proyecto I Encuentros//ES",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:Proyecto I 54ES4 Encuentros",
            "X-WR-TIMEZONE:America/Bogota",
            *VTIMEZONE_BOGOTA,
            *ics_events,
            "END:VCALENDAR",
        ]) + "\r\n",
        encoding="utf-8",
    )

    _sync_txt_grupo()

    # El `.gs` y el runbook de Proyecto I salen de `build_calendar_encuentros.py`, igual que
    # los de los otros cuatro cursos (2026-08-11). Antes se emitían aquí, y por eso Proyecto I
    # —el único curso que ya empezó— era el único sin rótulo PRINCIPAL/RESPALDO, sin Meet
    # autogestionado y con un runbook de 114 palabras. Se borran los que dejó este build.
    for viejo in ("Crear encuentros con invitados.gs",
                  "LEEME - Importar encuentros a Calendar.md"):
        p = grupo / viejo
        if p.is_file():
            p.unlink()
            print(f"RM {viejo}  (ahora lo genera build_calendar_encuentros.py)")

    print(
        f"OK CSV={csv_path.name} ICS={ics_path.name} "
        f"estudiantes={len(emails)} invitados/evento={len(guests)} "
        f"sesiones={len(events)} subject0={rows_out[0]['Subject']!r}"
    )


if __name__ == "__main__":
    main()
