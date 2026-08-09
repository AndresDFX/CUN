# -*- coding: utf-8 -*-
"""Variantes de CSV para probar si Google Calendar importa invitados (P1 · 54ES4).

Contexto: la documentación oficial de Google es explícita —
«When you import an event, guests and conference data for that event are not
imported» (https://support.google.com/calendar/answer/37118) — y la lista de
encabezados soportados no incluye ninguna columna de invitados.

Estas variantes existen para que el docente lo verifique en su propia cuenta CUN
(Workspace) en 2 minutos, descartando de paso problemas de formato (BOM,
separador, formato de fecha/hora, nombre de columna).

Genera en `2026/54ES4/pruebas_csv/`:
  A  control: 9 columnas oficiales, UTF-8 sin BOM  → debe importar bien, sin invitados
  B  A + columna `Guests`                          → hipótesis «columna Guests»
  C  encabezados del export CSV de Outlook (EN)    → hipótesis «Required Attendees»
  D  sinónimos (`Attendees`/`Guests`/`Invitees`)   → hipótesis «el nombre importa»

También genera `Crear encuentros desde CSV en Sheets.gs`: flujo que SÍ mete
invitados usando el CSV B como fuente (CSV → Google Sheets → Apps Script).

Requiere haber corrido antes:
    python config/slides/build_calendar_proyecto1_54es4.py
(que produce `encuentros_p1_calendar_data.json` con roster y sesiones).

Uso:
    python config/slides/build_pruebas_csv_invitados_p1.py
"""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

# Raíz del workspace derivada del propio archivo. Antes estaba hardcodeada como
# «G:\\Mi unidad\\...» y rompía cuando Google Drive monta la unidad en inglés
# («G:\\My Drive»). Corregido 2026-08-09.
_WS = Path(__file__).resolve().parents[2]


GRUPO = Path(
    _WS / "Especializacion" / "Proyecto I" / "2026" / "54ES4"
)
DATA = GRUPO / "encuentros_p1_calendar_data.json"
OUT = GRUPO / "pruebas_csv"

# Google documenta la hora como «10:00 AM»; Outlook exporta «10:00:00 AM».
HORA_GOOGLE = ("8:00 PM", "10:00 PM")
HORA_OUTLOOK = ("8:00:00 PM", "10:00:00 PM")

DOCENTE_CORREO = "julian_castanoe@cun.edu.co"

HEADERS_OFICIAL = [
    "Subject", "Start Date", "Start Time", "End Date", "End Time",
    "All Day Event", "Description", "Location", "Private",
]

# Encabezados tal como los emite el export CSV de Outlook en inglés.
HEADERS_OUTLOOK = [
    "Subject", "Start Date", "Start Time", "End Date", "End Time",
    "All day event", "Reminder on/off", "Reminder Date", "Reminder Time",
    "Meeting Organizer", "Required Attendees", "Optional Attendees",
    "Meeting Resources", "Billing Information", "Categories", "Description",
    "Location", "Mileage", "Priority", "Private", "Sensitivity",
    "Show time as",
]

if not DATA.is_file():
    raise FileNotFoundError(
        f"Falta {DATA.name}. Corre primero: "
        "python config/slides/build_calendar_proyecto1_54es4.py"
    )

data = json.loads(DATA.read_text(encoding="utf-8"))
guests: list[str] = data["guests"]
guests_csv = ", ".join(guests)
eventos = data["events"]
OUT.mkdir(parents=True, exist_ok=True)


def _fecha(iso: str) -> str:
    """MM/DD/YYYY — formato que documenta Google (locale en-US)."""
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%m/%d/%Y")


def _desc(texto: str) -> str:
    """Description en una línea (los saltos rompen filas CSV en algunos parsers)."""
    return texto.replace("\n", " | ")


def escribir(nombre: str, headers: list[str], filas: list[dict], bom: bool) -> Path:
    ruta = OUT / nombre
    enc = "utf-8-sig" if bom else "utf-8"
    with ruta.open("w", newline="", encoding=enc) as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)
    return ruta


def fila_base(ev: dict, horas: tuple[str, str]) -> dict:
    return {
        "Subject": ev["subject"],
        "Start Date": _fecha(ev["fecha"]),
        "Start Time": horas[0],
        "End Date": _fecha(ev["fecha"]),
        "End Time": horas[1],
        "Description": _desc(ev["description"]),
        "Location": "",
        "Private": "False",
    }


filas_a, filas_b, filas_c, filas_d = [], [], [], []
for ev in eventos:
    base = fila_base(ev, HORA_GOOGLE)

    filas_a.append({**base, "All Day Event": "False"})
    filas_b.append({**base, "All Day Event": "False", "Guests": guests_csv})
    filas_d.append({
        **base,
        "All Day Event": "False",
        "Guests": guests_csv,
        "Attendees": guests_csv,
        "Invitees": guests_csv,
    })

    out = fila_base(ev, HORA_OUTLOOK)
    out.update({
        "All day event": "False",
        "Reminder on/off": "False",
        "Reminder Date": "",
        "Reminder Time": "",
        "Meeting Organizer": DOCENTE_CORREO,
        "Required Attendees": "; ".join(guests),
        "Optional Attendees": "",
        "Meeting Resources": "",
        "Billing Information": "",
        "Categories": "",
        "Mileage": "",
        "Priority": "Normal",
        "Sensitivity": "Normal",
        "Show time as": "2",
    })
    filas_c.append(out)

generados = [
    escribir(
        "A - Control oficial 9 columnas (sin invitados).csv",
        HEADERS_OFICIAL, filas_a, bom=False,
    ),
    escribir(
        "B - Oficial + columna Guests.csv",
        HEADERS_OFICIAL + ["Guests"], filas_b, bom=False,
    ),
    escribir(
        "C - Estilo Outlook (Required Attendees).csv",
        HEADERS_OUTLOOK, filas_c, bom=False,
    ),
    escribir(
        "D - Sinonimos Attendees Guests Invitees.csv",
        HEADERS_OFICIAL + ["Guests", "Attendees", "Invitees"], filas_d, bom=False,
    ),
]

# ---------------------------------------------------------------------------
# Flujo «con el CSV» que sí mete invitados: CSV B → Google Sheets → Apps Script
# ---------------------------------------------------------------------------
gs = f'''/**
 * Proyecto I · 54ES4 — Crear encuentros CON invitados leyendo el CSV desde Sheets.
 *
 * Para quien quiera seguir trabajando "con el CSV": el archivo
 * «B - Oficial + columna Guests.csv» se sube a Google Sheets y este script
 * recorre las filas y crea los eventos añadiendo la columna Guests como
 * invitados reales (la importación nativa de Calendar la ignora).
 *
 * Pasos:
 * 1. drive.google.com → Nuevo → Subir «B - Oficial + columna Guests.csv».
 * 2. Clic derecho en el archivo → Abrir con → Hojas de cálculo de Google.
 * 3. Extensiones → Apps Script → pega TODO este archivo → Guardar.
 * 4. Revisa SEND_INVITES (false = crea sin notificar a nadie).
 * 5. Ejecuta crearEncuentrosDesdeHoja() → Autorizar → permitir Calendar.
 * 6. Abre un evento en Calendar: debe verse la sección Invitados.
 *
 * Regenerar: python config/slides/build_pruebas_csv_invitados_p1.py
 */
var SEND_INVITES = false; // true solo cuando quieras enviar el correo de invitación
var TIMEZONE = 'America/Bogota';

function crearEncuentrosDesdeHoja() {{
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var filas = hoja.getDataRange().getDisplayValues();
  var head = filas[0].map(function (h) {{ return String(h).trim(); }});
  var col = {{}};
  head.forEach(function (h, i) {{ col[h] = i; }});

  ['Subject', 'Start Date', 'Start Time', 'End Time', 'Guests'].forEach(function (c) {{
    if (col[c] === undefined) throw new Error('Falta la columna: ' + c);
  }});

  var cal = CalendarApp.getDefaultCalendar();
  var creados = 0;
  var omitidos = 0;

  for (var i = 1; i < filas.length; i++) {{
    var f = filas[i];
    var subject = f[col['Subject']];
    if (!subject) continue;

    var inicio = _fecha(f[col['Start Date']], f[col['Start Time']]);
    var finDia = f[col['End Date']] || f[col['Start Date']];
    var fin = _fecha(finDia, f[col['End Time']]);

    var yaExiste = cal.getEvents(inicio, fin, {{ search: subject }}).some(function (ev) {{
      return ev.getTitle() === subject;
    }});
    if (yaExiste) {{ omitidos++; continue; }}

    cal.createEvent(subject, inicio, fin, {{
      description: f[col['Description']] || '',
      location: f[col['Location']] || '',
      guests: String(f[col['Guests']] || '').split(',').map(function (e) {{
        return e.trim();
      }}).filter(String).join(','),
      sendInvites: SEND_INVITES
    }});
    creados++;
  }}

  Logger.log('Creados=' + creados + ' omitidos=' + omitidos +
             ' sendInvites=' + SEND_INVITES);
}}

/** «08/10/2026» + «8:00 PM» → Date en America/Bogota. */
function _fecha(fechaMDY, hora12) {{
  var p = String(fechaMDY).split('/');
  var iso = p[2] + '-' + _pad(p[0]) + '-' + _pad(p[1]);
  var h = String(hora12).trim().toUpperCase().match(/^(\\d{{1,2}}):(\\d{{2}})(?::(\\d{{2}}))?\\s*(AM|PM)$/);
  if (!h) throw new Error('Hora no reconocida: ' + hora12);
  var hh = parseInt(h[1], 10) % 12;
  if (h[4] === 'PM') hh += 12;
  var hms = _pad(hh) + ':' + h[2] + ':' + (h[3] || '00');
  return Utilities.parseDate(iso + ' ' + hms, TIMEZONE, 'yyyy-MM-dd HH:mm:ss');
}}

function _pad(v) {{
  v = String(v);
  return v.length < 2 ? '0' + v : v;
}}
'''

gs_path = GRUPO / "Crear encuentros desde CSV en Sheets.gs"
gs_path.write_text(gs, encoding="utf-8")

print(f"OK carpeta={OUT}")
for p in generados:
    print(f"  - {p.name}")
print(f"OK script Sheets={gs_path.name}")
print(f"sesiones={len(eventos)} invitados/evento={len(guests)} BOM=no separador=coma")
