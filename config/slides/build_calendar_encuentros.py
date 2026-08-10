# -*- coding: utf-8 -*-
"""Genera el Apps Script de encuentros CON invitados para Creatividad, Investigación, TG2 y TG3.

Por qué existe: Google Calendar **descarta los invitados** al importar `.ics`/`.csv`, así que
la única vía que sí crea la sección Invitados es un script de Apps Script con CalendarApp.
Hasta ahora solo Proyecto I tenía el suyo (`build_calendar_proyecto1_54es4.py`); esto lo
generaliza a los otros cuatro cursos.

TG3 = UNA SOLA SERIE para los tres grupos
    54450, 54466 y 54467 comparten horario (martes 5–6 pm) y **un solo enlace de Meet**
    (decisión del docente). Por eso se genera un único `.gs` en `2026/_combinado_todos/`
    que invita a los tres rosters juntos. Ojo con el cierre: 54450 termina el 15/11 y los
    otros dos el 22/11, así que a la ÚLTIMA sesión (posterior al cierre de 54450) solo se
    invita a 54466/54467. El script lo marca por evento.

ROSTER — de dónde salen los correos
    De `<Curso>/2026/<grupo>/`, en el primer archivo que encuentre con correos:
    `.ods`, `.xlsx`, `.csv` o `.txt` (cualquier nombre; se extraen por expresión regular).
    Si un grupo no tiene roster, ese curso se **omite con aviso** (no se inventan invitados).

Uso:
  python config/slides/build_calendar_encuentros.py            # todos los que tengan roster
  python config/slides/build_calendar_encuentros.py tg2        # uno solo
"""
from __future__ import annotations

import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))

from sesiones_cun import (  # noqa: E402
    COURSES,
    DOCENTE_CORREO,
    cdigital_url,
    meet_url,
    subject_encuentro,
)
from carga_academica import curso as carga_curso  # noqa: E402

EMAIL_RX = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# Proyecto I tiene su propio builder (incluye coanfitrión AFI y su propio flujo).
CURSOS = ("creatividad", "investigacion", "tg2", "tg3")
TG3_GRUPOS = ("54450", "54466", "54467")
TG3_CIERRE_CORTO = "54450"  # cierra 15/11; no asiste a la última sesión de la serie


# ── roster ───────────────────────────────────────────────────────────────────
def _emails_de_archivo(f: Path) -> list[str]:
    try:
        if f.suffix.lower() in {".ods", ".xlsx"}:
            with zipfile.ZipFile(f) as z:
                blob = " ".join(
                    z.read(n).decode("utf-8", "replace")
                    for n in z.namelist()
                    if n.endswith(".xml")
                )
        else:
            blob = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    return EMAIL_RX.findall(blob)


def roster(grupo_dir: Path) -> list[str]:
    """Correos del grupo, deduplicados y ordenados. Lista vacía si no hay roster."""
    if not grupo_dir.is_dir():
        return []
    encontrados: list[str] = []
    for f in sorted(grupo_dir.iterdir()):
        if f.is_file() and f.suffix.lower() in {".ods", ".xlsx", ".csv", ".txt"}:
            encontrados += _emails_de_archivo(f)
    # Descarta el correo del propio docente: él es el organizador, no invitado.
    return sorted({e for e in encontrados if e.lower() != DOCENTE_CORREO.lower()})


# ── emisión del .gs ──────────────────────────────────────────────────────────
def _js(s: str) -> str:
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"


def _horas(course_key: str) -> tuple[str, str]:
    """('17:00','18:00') a partir de `hora_ics` de carga_academica ('170000','180000')."""
    ics = carga_curso(course_key)["horario"]["hora_ics"]
    return f"{ics[0][:2]}:{ics[0][2:4]}", f"{ics[1][:2]}:{ics[1][2:4]}"


def _sesiones_js(course_key: str, grupos: list[str], solo_ultima: list[str] | None) -> str:
    ini, fin = _horas(course_key)
    filas = []
    ses = COURSES[course_key]["sesiones"]
    for i, s in enumerate(ses):
        d = datetime.strptime(s["fecha"], "%d/%m/%Y").date()
        ultima = i == len(ses) - 1
        invitados = solo_ultima if (ultima and solo_ultima) else grupos
        n = int(s["n"])
        filas.append(
            "  {\n"
            f"    subject: {_js(subject_encuentro(course_key, invitados, n=n))},\n"
            f"    description: {_js(f'Sesión {n:02d} — ' + s['titulo'])},\n"
            f"    start: '{d.isoformat()}T{ini}:00',\n"
            f"    end: '{d.isoformat()}T{fin}:00',\n"
            f"    grupos: [{', '.join(_js(g) for g in invitados)}]\n"
            "  }"
        )
    return ",\n".join(filas)


def build_curso(course_key: str) -> str | None:
    c = COURSES[course_key]
    base = Path(c["folder"]) / "2026"
    combinado = course_key == "tg3"
    grupos = list(TG3_GRUPOS) if combinado else [
        p.name for p in sorted(base.iterdir()) if p.is_dir() and not p.name.startswith("_")
    ]

    rosters = {g: roster(base / g) for g in grupos}
    faltan = [g for g, e in rosters.items() if not e]
    if faltan:
        print(f"SKIP {course_key}: sin roster en {', '.join(faltan)} "
              f"(pon el listado en 2026/<grupo>/ y vuelve a correr)")
        return None

    if combinado:
        out_dir = base / "_combinado_todos"
        grupos_titulo = list(TG3_GRUPOS)
        solo_ultima = [g for g in TG3_GRUPOS if g != TG3_CIERRE_CORTO]
    else:
        out_dir = base / grupos[0]
        grupos_titulo = grupos
        solo_ultima = None
    out_dir.mkdir(parents=True, exist_ok=True)

    invitados_js = ",\n".join(
        f"  {_js(g)}: [\n" + ",\n".join(f"    {_js(e)}" for e in rosters[g]) + "\n  ]"
        for g in grupos_titulo
    )
    total = sum(len(rosters[g]) for g in grupos_titulo)

    nota_tg3 = ""
    if combinado:
        nota_tg3 = (
            " *\n"
            " * TG3 — UNA SOLA SERIE para los tres grupos: comparten horario y **un solo enlace de\n"
            f" * Meet**. A la ÚLTIMA sesión no se invita a {TG3_CIERRE_CORTO} (su curso cierra antes).\n"
        )

    gs = f"""/**
 * {c['titulo']} — Crear encuentros CON invitados en Google Calendar.
 *
 * Google Calendar DESCARTA los invitados al importar .ics/.csv. Este script usa
 * CalendarApp y sí añade la sección Invitados.
 *{nota_tg3} *
 * PASOS
 * 1. https://script.google.com con la cuenta CUN ({DOCENTE_CORREO}).
 * 2. Nuevo proyecto → pega TODO este archivo → guarda.
 * 3. Ejecuta `verificar()` (SOLO LECTURA) y revisa el registro.
 * 4. Si todo cuadra, ejecuta `crearEncuentros()`.
 * 5. Añade el coanfitrión de Meet a mano (eso no lo puede hacer la API).
 *
 * MEET: CalendarApp no adjunta videoconferencia. El enlace va en Ubicación y en la
 * descripción (clicable y visible en el correo). Para el chip nativo «Unirse con
 * Google Meet», usa después el script «Actualizar Meet en encuentros (mismo enlace).gs».
 *
 * Regenerar este .gs: python config/slides/build_calendar_encuentros.py {course_key}
 */
var SEND_INVITES = false;  // true solo cuando quieras notificar a los estudiantes
var TIMEZONE = 'America/Bogota';
var MEET_URL = {_js(meet_url(course_key))};
var CDIGITAL = {_js(cdigital_url(course_key))};

// Roster por grupo ({total} invitados en total).
var INVITADOS = {{
{invitados_js}
}};

var SESIONES = [
{_sesiones_js(course_key, grupos_titulo, solo_ultima)}
];

function crearEncuentros() {{
  var cal = CalendarApp.getDefaultCalendar();
  var creados = 0, omitidos = 0;
  SESIONES.forEach(function (s) {{
    var ini = _fecha(s.start), fin = _fecha(s.end);
    var ya = cal.getEvents(ini, fin, {{ search: s.subject }}).some(function (ev) {{
      return ev.getTitle() === s.subject;
    }});
    if (ya) {{ omitidos++; return; }}
    cal.createEvent(s.subject, ini, fin, {{
      description: s.description + '\\nMeet: ' + MEET_URL + '\\nCDigital: ' + CDIGITAL,
      location: MEET_URL,
      guests: _invitados(s.grupos).join(','),
      sendInvites: SEND_INVITES
    }});
    creados++;
  }});
  Logger.log('Listo. Creados=' + creados + ' omitidos(ya existían)=' + omitidos +
             ' sendInvites=' + SEND_INVITES);
}}

/** SOLO LECTURA: qué haría el script, sin crear nada. */
function verificar() {{
  Logger.log('Sesiones: ' + SESIONES.length + ' · Meet: ' + MEET_URL);
  SESIONES.forEach(function (s) {{
    var n = _invitados(s.grupos).length;
    Logger.log(s.start.substring(0, 10) + '  ' + s.subject + '  invitados=' + n +
               ' [' + s.grupos.join(', ') + ']');
  }});
  Logger.log('Si esto cuadra, ejecuta crearEncuentros().');
}}

/** Borra solo los eventos creados por este script. */
function borrarEncuentros() {{
  var cal = CalendarApp.getDefaultCalendar();
  var titulos = {{}};
  SESIONES.forEach(function (s) {{ titulos[s.subject] = true; }});
  var desde = _fecha(SESIONES[0].start);
  var hasta = _fecha(SESIONES[SESIONES.length - 1].end);
  var n = 0;
  cal.getEvents(desde, new Date(hasta.getTime() + 36e5)).forEach(function (ev) {{
    if (titulos[ev.getTitle()]) {{ ev.deleteEvent(); n++; }}
  }});
  Logger.log('Eliminados=' + n);
}}

function _invitados(grupos) {{
  var out = [], vistos = {{}};
  grupos.forEach(function (g) {{
    (INVITADOS[g] || []).forEach(function (e) {{
      if (!vistos[e]) {{ vistos[e] = true; out.push(e); }}
    }});
  }});
  return out;
}}

function _fecha(iso) {{
  return Utilities.parseDate(iso.replace('T', ' '), TIMEZONE, 'yyyy-MM-dd HH:mm:ss');
}}
"""
    nombre = f"Crear encuentros con invitados{' (3 grupos)' if combinado else ''}.gs"
    dest = out_dir / nombre
    dest.write_text(gs, encoding="utf-8")
    print(f"OK {course_key}: {dest.relative_to(Path(COURSES[course_key]['folder']).parents[1])} "
          f"· {len(COURSES[course_key]['sesiones'])} sesiones · {total} invitados"
          f"{' · serie única para ' + '/'.join(grupos_titulo) if combinado else ''}")
    return str(dest)


def main(argv: list[str]) -> int:
    keys = [a for a in argv if a in CURSOS] or list(CURSOS)
    hechos = [k for k in keys if build_curso(k)]
    print(f"\nGenerados: {len(hechos)}/{len(keys)}")
    if len(hechos) < len(keys):
        print("Los omitidos necesitan el listado de estudiantes en 2026/<grupo>/ "
              "(.ods, .xlsx, .csv o .txt con los correos).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
