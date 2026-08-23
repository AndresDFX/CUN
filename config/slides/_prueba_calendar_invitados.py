# -*- coding: utf-8 -*-
r"""
Ejecuta las órdenes `verificarInvitados()` / `agregarInvitados()` de los `.gs` de encuentros en
Node, con las globales de Apps Script simuladas, y comprueba que se portan como dice su runbook.

Por qué existe: esos `.gs` son archivos **generados** que se pegan en los servidores de Google y
escriben en el calendario de un curso con 51, 50 o 112 estudiantes invitados. Un fallo ahí no se
queda en la consola: manda correos, o deja media clase sin invitación. Aquí se prueba sin cuenta,
sin red y sin tocar ningún calendario: se le da un calendario de mentira construido a partir de las
propias `SESIONES` del archivo y se mira qué hace.

Cubre lo que de verdad se puede romper:
  1. camino feliz — a quién le falta invitación, y añadirlo
  2. UN patch por encuentro, no uno por invitado (51 invitados = 1 llamada, no 51)
  3. no se pierde el «Sí asisto» de quien ya estaba
  4. idempotencia — si no falta nadie, no se toca nada
  5. el id del Meet en sus tres formas (URL, código con guiones, código pelado)
  6. encuentros renombrados a mano y tutorías fuera de SESIONES: se hallan por el Meet
  7. un encuentro con OTRA sala no se toca
  8. `NUEVOS` — solo esos correos; basura y el propio correo del Docente abortan
  9. bajas: se informan, nunca se quitan
 10. sala de otro curso: avisa antes de invitar al roster equivocado
 11. sin el servicio avanzado: invita de a uno y lo dice
 12. TG3 — la última sesión lleva el roster de dos grupos, no de tres

    python config/slides/_prueba_calendar_invitados.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
P1 = REPO / "Especializacion/Proyecto I/2026/54ES4/PRINCIPAL - Crear encuentros con invitados.gs"
TG3 = (REPO / "Pregrado/Trabajo de grado 3/2026/_combinado_todos"
            / "PRINCIPAL - Crear encuentros con invitados (3 grupos).gs")
MEET_P1 = "https://meet.google.com/omk-woqk-vsj"

# ── globales de Apps Script, simuladas ───────────────────────────────────────
HARNESS = r"""
var PRUEBA = JSON.parse(process.argv[2]);
var _log = [], _eventos = [], _patches = [], _addGuest = [], _props = {};

var Logger = {log: function (t) { _log.push(String(t)); }};
var PropertiesService = {
  getScriptProperties: function () {
    return {
      getProperty: function (k) { return _props[k] || null; },
      setProperty: function (k, v) { _props[k] = v; },
      deleteProperty: function (k) { delete _props[k]; }
    };
  }
};
// America/Bogota es UTC-5 todo el año: no hay horario de verano que enredar.
var Utilities = {
  parseDate: function (s) { return new Date(String(s).replace(' ', 'T') + '-05:00'); },
  formatDate: function (d) {
    return new Date(d.getTime() - 5 * 36e5).toISOString().substring(0, 10);
  },
  sleep: function () {}
};

var Calendar = {
  Events: {
    list: function () { return {items: _eventos.slice(0)}; },
    get: function (calId, id) {
      for (var i = 0; i < _eventos.length; i++) if (_eventos[i].id === id) return _eventos[i];
      return null;
    },
    patch: function (recurso, calId, id, opciones) {
      _patches.push({id: id, recurso: recurso, opciones: opciones || {}});
      for (var i = 0; i < _eventos.length; i++) {
        if (_eventos[i].id === id && recurso.attendees) _eventos[i].attendees = recurso.attendees;
      }
      return _eventos[0];
    }
  }
};
if (!PRUEBA.api) { Calendar = undefined; }

function _comoApp_(e) {
  return {
    getTitle: function () { return e.summary; },
    getLocation: function () { return e.location || ''; },
    getDescription: function () { return e.description || ''; },
    getStartTime: function () { return new Date(e.start.dateTime); },
    getId: function () { return e.id + '@google.com'; },
    getGuestList: function () {
      return (e.attendees || []).map(function (a) {
        return {getEmail: function () { return a.email; }};
      });
    },
    addGuest: function (correo) {
      _addGuest.push({id: e.id, correo: correo});
      e.attendees = (e.attendees || []).concat([{email: correo}]);
    }
  };
}
var CalendarApp = {
  getDefaultCalendar: function () {
    return {
      getName: function () { return 'julian_castanoe@cun.edu.co'; },
      getId: function () { return 'julian_castanoe@cun.edu.co'; },
      getEvents: function (desde, hasta, opt) {
        return _eventos.filter(function (e) {
          var t = new Date(e.start.dateTime).getTime();
          if (t < desde.getTime() || t > hasta.getTime()) return false;
          if (opt && opt.search) return String(e.summary).indexOf(opt.search) >= 0;
          return true;
        }).map(_comoApp_);
      }
    };
  }
};
"""

# El calendario de mentira se siembra a partir de las SESIONES del propio .gs: así la prueba no
# repite las fechas ni el roster, y sirve igual para los cinco cursos.
COLA = r"""
MEET_ID = PRUEBA.meetId || '';
NUEVOS = PRUEBA.nuevos || [];
SEND_INVITES = !!PRUEBA.sendInvites;

(function sembrar() {
  var cuantos = PRUEBA.creados == null ? SESIONES.length : PRUEBA.creados;
  for (var i = 0; i < cuantos; i++) {
    var s = SESIONES[i];
    var roster = _invitados(s.grupos);
    var faltan = PRUEBA.faltanN == null ? 0 : PRUEBA.faltanN;
    var hasta = PRUEBA.sinNadie ? 0 : Math.max(0, roster.length - faltan);
    var att = [];
    for (var j = 0; j < hasta; j++) {
      att.push({email: roster[j], responseStatus: j === 0 ? 'accepted' : 'needsAction'});
    }
    if (PRUEBA.sobrante) att.push({email: PRUEBA.sobrante, responseStatus: 'accepted'});
    _eventos.push({
      id: 'ev' + (i + 1),
      summary: (PRUEBA.renombrar && i === 0) ? 'Clase movida (la renombré a mano)' : s.subject,
      start: {dateTime: s.start + '-05:00'},
      location: PRUEBA.salaEnEventos == null ? MEET_URL : PRUEBA.salaEnEventos,
      description: '',
      attendees: att
    });
  }
  (PRUEBA.extra || []).forEach(function (e, k) {
    _eventos.push({id: 'x' + (k + 1), summary: e.titulo, start: {dateTime: e.start},
                   location: e.sala || '', description: e.descripcion || '', attendees: []});
  });
})();

var salida = {ok: true, error: null};
try {
  if (PRUEBA.accion === 'agregar') agregarInvitados(); else verificarInvitados();
} catch (e) {
  salida.ok = false;
  salida.error = String(e && e.message ? e.message : e);
}
salida.log = _log;
salida.patches = _patches;
salida.addGuest = _addGuest;
salida.eventos = _eventos;
console.log(JSON.stringify(salida));
"""


def correr(gs: Path, accion: str = "verificar", **prueba) -> dict:
    prueba.setdefault("api", True)
    prueba["accion"] = accion
    with tempfile.TemporaryDirectory() as tmp:
        js = Path(tmp) / "prueba.js"
        js.write_text(HARNESS + "\n" + gs.read_text(encoding="utf-8") + "\n" + COLA,
                      encoding="utf-8")
        r = subprocess.run(["node", str(js), json.dumps(prueba, ensure_ascii=False)],
                           capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            raise SystemExit(f"node falló:\n{r.stderr[:2000]}")
        return json.loads(r.stdout.strip().splitlines()[-1])


def faltan_por_evento(r: dict) -> list[int]:
    return [int(m) for m in re.findall(r"faltan=(\d+)", "\n".join(r["log"]))]


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_calendar_encuentros as B  # noqa: PLC0415  (aquí, no arriba: es para el cotejo)

    for f in (P1, TG3):
        if not f.is_file():
            raise SystemExit(f"No está {f.name}. Corre build_calendar_encuentros.py primero.")
        # Probar un .gs viejo da un verde que no vale nada: lo primero es que el archivo en disco
        # sea el que emite el builder de hoy. (Pasó de verdad: edité el cuerpo JS, no regeneré, y
        # la prueba falló señalando la lógica en vez del olvido.)
        if B.GS_FUNCIONES.strip() not in f.read_text(encoding="utf-8"):
            raise SystemExit(
                f"«{f.name}» está DESACTUALIZADO respecto a build_calendar_encuentros.py.\n"
                "Corre primero:  python config/slides/build_calendar_encuentros.py")

    fallos: list[str] = []

    def check(nombre: str, cond: bool, detalle: str = "") -> None:
        print(("  OK   " if cond else "  FALLA ") + nombre + ("" if cond else f"  → {detalle}"))
        if not cond:
            fallos.append(nombre)

    # ── 1. camino feliz: faltan 2 por encuentro ──────────────────────────────
    r = correr(P1, "verificar", faltanN=2)
    log = "\n".join(r["log"])
    check("1. verificarInvitados() ve los 11 encuentros y los 2 que faltan en cada uno",
          r["ok"] and faltan_por_evento(r) == [2] * 11, r.get("error") or log[-400:])
    check("1b. cuenta invitaciones y personas distintas",
          "Invitaciones que faltan: 22" in log and "personas distintas: 2" in log, log[-500:])
    check("1c. verificar NO escribe nada", not r["patches"] and not r["addGuest"],
          f"{len(r['patches'])} patches, {len(r['addGuest'])} addGuest")
    check("1d. remite a agregarInvitados()", "ejecuta agregarInvitados()" in log, log[-200:])

    r = correr(P1, "agregar", faltanN=2)
    log = "\n".join(r["log"])
    check("2. agregarInvitados() añade las 22 invitaciones",
          r["ok"] and "Añadidos: 22 invitaciones en 11 encuentros" in log,
          r.get("error") or log[-400:])
    check("2b. UN patch por encuentro, no uno por invitado", len(r["patches"]) == 11,
          str(len(r["patches"])))
    check("2c. sin el servicio avanzado no habría hecho falta addGuest", not r["addGuest"],
          str(len(r["addGuest"])))
    if r["patches"]:
        att = r["patches"][0]["recurso"]["attendees"]
        aceptado = [a for a in att if a.get("responseStatus") == "accepted"]
        check("3. conserva el «Sí asisto» de quien ya estaba", len(aceptado) == 1 and len(att) == 51,
              f"{len(att)} asistentes, {len(aceptado)} aceptados")
        check("3b. sendUpdates=none con SEND_INVITES=false",
              r["patches"][0]["opciones"].get("sendUpdates") == "none",
              json.dumps(r["patches"][0]["opciones"]))

    r = correr(P1, "agregar", faltanN=2, sendInvites=True)
    check("3c. sendUpdates=all con SEND_INVITES=true",
          r["patches"] and r["patches"][0]["opciones"].get("sendUpdates") == "all",
          json.dumps(r["patches"][0]["opciones"]) if r["patches"] else "sin patches")

    # ── 4. idempotencia ─────────────────────────────────────────────────────
    r = correr(P1, "agregar", faltanN=0)
    log = "\n".join(r["log"])
    check("4. si no falta nadie no toca nada",
          r["ok"] and not r["patches"] and "No falta nadie" in log, r.get("error") or log[-300:])

    # ── 5. el id del Meet, en sus tres formas ───────────────────────────────
    formas = {"URL completa": MEET_P1, "código con guiones": "omk-woqk-vsj",
              "código pelado": "omkwoqkvsj"}
    for nombre, valor in formas.items():
        r = correr(P1, "verificar", faltanN=1, meetId=valor)
        log = "\n".join(r["log"])
        check(f"5. MEET_ID como {nombre}: misma sala, mismos 11 encuentros",
              r["ok"] and "SALA      : omkwoqkvsj" in log and faltan_por_evento(r) == [1] * 11,
              r.get("error") or log[:400])

    r = correr(P1, "verificar", faltanN=1, meetId="pega aquí el meet")
    check("5b. MEET_ID que no es un Meet: aborta y enseña el formato",
          not r["ok"] and "meet.google.com/abc-defg-hij" in (r["error"] or ""),
          (r.get("error") or "")[:200])

    # ── 6. renombrado a mano + tutoría fuera de SESIONES ────────────────────
    r = correr(P1, "verificar", faltanN=2, renombrar=True, meetId=MEET_P1)
    log = "\n".join(r["log"])
    check("6. el encuentro renombrado a mano se halla por el Meet",
          r["ok"] and "Clase movida (la renombré a mano)" in log and
          "[FUERA DE SESIONES · lo hallé por el Meet]" in log, r.get("error") or log[:600])
    check("6b. y avisa de que esa sesión no aparece por título",
          "sin crear todavía: 1" in log, log[-500:])

    r = correr(P1, "verificar", faltanN=0, meetId=MEET_P1, extra=[
        {"titulo": "Tutoría de anteproyecto", "start": "2026-09-02T20:00:00-05:00",
         "sala": MEET_P1},
    ])
    log = "\n".join(r["log"])
    check("6c. una tutoría con la misma sala también entra, marcada",
          r["ok"] and "Tutoría de anteproyecto" in log and
          "[FUERA DE SESIONES · lo hallé por el Meet]" in log, r.get("error") or log[:600])

    # ── 7. otra sala: ni se mira ────────────────────────────────────────────
    r = correr(P1, "agregar", faltanN=0, extra=[
        {"titulo": "Junta de la Escuela", "start": "2026-09-02T15:00:00-05:00",
         "sala": "https://meet.google.com/zzz-zzzz-zzz"},
    ])
    log = "\n".join(r["log"])
    check("7. un evento con otra sala y otro título no se toca",
          r["ok"] and "Junta de la Escuela" not in log and not r["patches"],
          r.get("error") or log[-300:])

    # ── 8. NUEVOS ───────────────────────────────────────────────────────────
    r = correr(P1, "agregar", faltanN=2, nuevos=["tarde.matriculado@cun.edu.co"])
    log = "\n".join(r["log"])
    check("8. NUEVOS: solo ese correo, en los 11 encuentros",
          r["ok"] and "Añadidos: 11 invitaciones en 11 encuentros" in log and
          "solo los 1 correos de NUEVOS" in log, r.get("error") or log[-400:])
    if r["patches"]:
        nuevos_en_patch = [a["email"] for a in r["patches"][0]["recurso"]["attendees"]
                           if a["email"] == "tarde.matriculado@cun.edu.co"]
        check("8b. y los 49 que ya estaban siguen ahí",
              len(r["patches"][0]["recurso"]["attendees"]) == 50 and len(nuevos_en_patch) == 1,
              str(len(r["patches"][0]["recurso"]["attendees"])))

    r = correr(P1, "agregar", faltanN=2, nuevos=["esto no es un correo"])
    check("8c. NUEVOS con basura: aborta sin invitar a nadie",
          not r["ok"] and "no son un correo" in (r["error"] or "") and not r["patches"],
          (r.get("error") or "")[:200])

    r = correr(P1, "agregar", faltanN=2, nuevos=["julian_castanoe@cun.edu.co"])
    check("8d. NUEVOS solo con tu correo: aborta en vez de invitar al roster entero",
          not r["ok"] and "organizador" in (r["error"] or "") and not r["patches"],
          (r.get("error") or "")[:200])

    # ── 9. bajas ────────────────────────────────────────────────────────────
    r = correr(P1, "agregar", faltanN=1, sobrante="se.retiro@cun.edu.co")
    log = "\n".join(r["log"])
    check("9. una baja se informa, no se quita",
          r["ok"] and "ya NO están en el roster: 1" in log and "se.retiro@cun.edu.co" in log,
          r.get("error") or log[-500:])
    if r["patches"]:
        sigue = any(a["email"] == "se.retiro@cun.edu.co"
                    for a in r["patches"][0]["recurso"]["attendees"])
        check("9b. y sigue invitada después del patch", sigue,
              json.dumps(r["patches"][0]["recurso"]["attendees"])[:200])

    # ── 10. sala de otro curso ──────────────────────────────────────────────
    r = correr(P1, "verificar", faltanN=1, meetId="abc-defg-hij")
    log = "\n".join(r["log"])
    check("10. sala que no es la del curso: avisa antes de invitar al roster equivocado",
          r["ok"] and "NO es la de PROYECTO I" in log and "PÁRATE AQUÍ" in log,
          r.get("error") or log[:600])

    # ── 11. sin servicio avanzado ───────────────────────────────────────────
    r = correr(P1, "agregar", faltanN=2, api=False)
    log = "\n".join(r["log"])
    check("11. sin el servicio avanzado invita de a uno con CalendarApp",
          r["ok"] and len(r["addGuest"]) == 22 and not r["patches"],
          r.get("error") or f"{len(r['addGuest'])} addGuest, {len(r['patches'])} patches")
    check("11b. y avisa de que no puede elegir si se les notifica",
          "NO puedo elegir si se les notifica" in log, log[:600])

    # ── 12. sesiones sin crear · calendario vacío ───────────────────────────
    r = correr(P1, "verificar", faltanN=1, creados=9)
    log = "\n".join(r["log"])
    check("12. las sesiones que aún no existen se cuentan aparte",
          r["ok"] and "Encuentros hallados: 9 de 11" in log and "sin crear todavía: 2" in log,
          r.get("error") or log[-400:])

    r = correr(P1, "verificar", creados=0)
    log = "\n".join(r["log"])
    check("12b. calendario vacío: remite a crearEncuentros(), no revienta",
          r["ok"] and "crearEncuentros()" in log and not r["patches"],
          r.get("error") or log[-300:])

    # ── 13. TG3: el roster de la última sesión es de dos grupos ─────────────
    r = correr(TG3, "verificar", sinNadie=True)
    log = "\n".join(r["log"])
    cuentas = faltan_por_evento(r)
    check("13. TG3: la última sesión lleva menos invitados que las demás",
          r["ok"] and len(cuentas) == 15 and cuentas[-1] < cuentas[0],
          r.get("error") or f"{cuentas}")
    check("13b. TG3: las 14 primeras llevan los 112 de los tres grupos",
          cuentas[:14] == [112] * 14, str(cuentas[:14]))

    print(f"\n{len(fallos)} fallos")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
