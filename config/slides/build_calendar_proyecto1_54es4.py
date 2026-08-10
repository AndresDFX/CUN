# -*- coding: utf-8 -*-
"""Genera CSV + ICS + Apps Script de encuentros Proyecto I (grupo 54ES4).

Subject corto: «54ES4 - Proyecto I - Sesion NN» (helper subject_encuentro).
Description: 2–4 líneas (sin políticas ni placeholders largos).
Location: vacío mientras no haya Meet real.

Invitados en Google Calendar: la importación .ics/.csv **no** mete Guests
(limitación de Google). Flujo que sí funciona → Apps Script generado aquí
(`Crear encuentros con invitados.gs`) o Calendar API
(`create_encuentros_p1_calendar_api.py`).
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

GRUPO = Path(
    _WS / "Especializacion" / "Proyecto I" / "2026" / "54ES4"
)
GROUPS = ["54ES4"]
COURSE_KEY = "proyecto1"
# Enlace ÚNICO de Meet para toda la serie del periodo (lo confirmó el docente 2026-08-10).
# Va en Location de los eventos y en el .gs; si algún periodo aún no tiene sala, se deja "" y
# el material vuelve a mostrar placeholder (no inventar una URL).
LOCATION = "https://meet.google.com/omk-woqk-vsj"


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
    if not ods.is_file():
        raise FileNotFoundError(
            f"No se encontró el roster ODS en {ods}. "
            "Debe vivir en Especializacion/Proyecto I/2026/54ES4/."
        )
    with zipfile.ZipFile(ods) as z:
        data = z.read("content.xml").decode("utf-8", errors="replace")
    return sorted(set(re.findall(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", data)))


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


def _write_apps_script(gs_path: Path, guests: list[str], events: list[dict]) -> None:
    guests_js = ",\n  ".join(_js_str(e) for e in guests)
    sessions_js_parts = []
    for ev in events:
        sessions_js_parts.append(
            "  {\n"
            f"    subject: {_js_str(ev['subject'])},\n"
            f"    description: {_js_str(ev['description'])},\n"
            f"    start: {_js_str(ev['start'])},\n"
            f"    end: {_js_str(ev['end'])}\n"
            "  }"
        )
    sessions_js = ",\n".join(sessions_js_parts)
    gs_path.write_text(
        f"""/**
 * Proyecto I · 54ES4 — Crear encuentros CON invitados en Google Calendar.
 *
 * Google Calendar al IMPORTAR .ics/.csv DESCARTA los invitados (ATTENDEE/Guests).
 * Este script usa CalendarApp y SÍ añade la sección Invitados.
 *
 * Pasos:
 * 1. Abre https://script.google.com con tu cuenta CUN ({DOCENTE_CORREO}).
 * 2. Nuevo proyecto → pega TODO este archivo → guarda.
 * 3. Revisa SEND_INVITES (false = crea sin notificar; true = envía correo).
 * 4. Ejecuta createEncuentrosP1() → autoriza Calendar cuando lo pida.
 * 5. En Calendar: abre un evento → debe verse Invitados (roster + coanfitrión).
 * 6. Asigna el coanfitrión de Meet a mano (eso NO lo puede hacer la API).
 *
 * SOBRE EL ENLACE DE MEET
 * CalendarApp NO adjunta videoconferencia: si se añade Meet evento por evento desde la
 * interfaz, Google crea un enlace DISTINTO en cada uno. Por eso este script escribe el
 * MISMO enlace de la serie en Location y en la descripción de los 11 encuentros.
 * Para además tener el chip nativo «Unirse con Google Meet», ejecuta después
 * `Actualizar Meet en encuentros (mismo enlace).gs` (usa el servicio avanzado de Calendar).
 *
 * Regenerar este .gs: python config/slides/build_calendar_proyecto1_54es4.py
 */
var SEND_INVITES = false; // true solo cuando quieras notificar a todos
var TIMEZONE = 'America/Bogota';
var LOCATION = {_js_str(LOCATION)}; // enlace único de Meet para toda la serie

var GUESTS = [
  {guests_js}
];

var SESSIONS = [
{sessions_js}
];

function createEncuentrosP1() {{
  var cal = CalendarApp.getDefaultCalendar();
  var guestsCsv = GUESTS.join(',');
  var created = 0;
  var skipped = 0;

  SESSIONS.forEach(function (s) {{
    var start = _parseLocal(s.start);
    var end = _parseLocal(s.end);
    var existing = cal.getEvents(start, end, {{ search: s.subject }});
    var already = existing.some(function (ev) {{
      return ev.getTitle() === s.subject;
    }});
    if (already) {{
      skipped++;
      return;
    }}
    var options = {{
      description: s.description,
      location: LOCATION,
      guests: guestsCsv,
      sendInvites: SEND_INVITES
    }};
    cal.createEvent(s.subject, start, end, options);
    created++;
  }});

  Logger.log(
    'Listo. Creados=' + created + ' omitidos(ya existían)=' + skipped +
    ' invitados/evento=' + GUESTS.length + ' sendInvites=' + SEND_INVITES
  );
}}

/** Borra solo eventos cuyo título empieza por «54ES4 - Proyecto I - Sesion». */
function deleteEncuentrosP1Generados() {{
  var cal = CalendarApp.getDefaultCalendar();
  var from = _parseLocal(SESSIONS[0].start);
  var to = _parseLocal(SESSIONS[SESSIONS.length - 1].end);
  to = new Date(to.getTime() + 60 * 60 * 1000);
  var events = cal.getEvents(from, to);
  var n = 0;
  events.forEach(function (ev) {{
    var t = ev.getTitle() || '';
    if (t.indexOf('54ES4 - Proyecto I - Sesion') === 0) {{
      ev.deleteEvent();
      n++;
    }}
  }});
  Logger.log('Eliminados=' + n);
}}

function _parseLocal(isoLocal) {{
  // isoLocal: YYYY-MM-DDTHH:MM:SS → America/Bogota
  return Utilities.parseDate(
    isoLocal.replace('T', ' '),
    TIMEZONE,
    'yyyy-MM-dd HH:mm:ss'
  );
}}
""",
        encoding="utf-8",
    )


def _write_leeme(path: Path) -> None:
    path.write_text(
        """# Proyecto I · 54ES4 · Calendar (mínimo)

## Qué hay aquí
- `Listado estudiantes.ods` — roster (fuente)
- `Correos estudiantes (invitados Calendar).txt` — lista plana
- `Crear encuentros con invitados.gs` — **flujo principal** (sí mete invitados)
- `Encuentros Proyecto I - Importar a Calendar.csv` / `.ics` — fechas/respaldo (Google **no** importa invitados)
- `Entregas y hitos docentes - Importar a Calendar.csv` — deadlines ACA / hitos AFI
- `Correo de bienvenida.docx` · `Informacion.txt` — oferta del grupo

## Qué hacer
1. **Encuentros con invitados:** script.google.com → pegar `Crear encuentros con invitados.gs` → `createEncuentrosP1` (`SEND_INVITES=false` al inicio).
2. **Hitos docentes:** Calendar → Importar el CSV de entregas (sin invitados).
3. Regenerar CSV/ICS/.gs/correos: `python config/slides/build_calendar_proyecto1_54es4.py`
""",
        encoding="utf-8",
    )


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

    csv_path = grupo / "Encuentros Proyecto I - Importar a Calendar.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)

    mails_path = grupo / "Correos estudiantes (invitados Calendar).txt"
    mails_path.write_text(
        "Correos invitados (estudiantes 54ES4). El coanfitrión se añade aparte en el script.\n"
        "NO uses import CSV/ICS para invitados: Google Calendar descarta Guests/ATTENDEE.\n"
        "Flujo correcto: ejecutar Crear encuentros con invitados.gs (Apps Script).\n"
        f"Coanfitrión: {coord}\n\n"
        + "\n".join(emails) + "\n",
        encoding="utf-8",
    )

    ics_path = grupo / "Encuentros Proyecto I - Importar a Calendar.ics"
    ics_path.write_text(
        "\r\n".join([
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//CUN//Proyecto I Encuentros//ES",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:Proyecto I 54ES4 Encuentros",
            "X-WR-TIMEZONE:America/Bogota",
            *ics_events,
            "END:VCALENDAR",
        ]) + "\r\n",
        encoding="utf-8",
    )

    gs_path = grupo / "Crear encuentros con invitados.gs"
    _write_apps_script(gs_path, guests, events)

    leeme_path = grupo / "LEEME - Importar encuentros a Calendar.md"
    _write_leeme(leeme_path)

    # No generar JSON auxiliar ni pruebas_csv/ (ruido; el .gs ya es self-contained).
    print(
        f"OK CSV={csv_path.name} ICS={ics_path.name} GS={gs_path.name} "
        f"estudiantes={len(emails)} invitados/evento={len(guests)} "
        f"sesiones={len(events)} subject0={rows_out[0]['Subject']!r}"
    )


if __name__ == "__main__":
    main()
