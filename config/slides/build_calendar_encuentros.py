# -*- coding: utf-8 -*-
"""Genera el Apps Script de encuentros CON invitados Y CON Meet para Creatividad,
Investigación, TG2 y TG3 — más el runbook (`LEEME - Crear los eventos de Calendar.md`).

Por qué existe: Google Calendar **descarta los invitados** al importar `.ics`/`.csv`, así que
la única vía que sí crea la sección Invitados es un script de Apps Script con CalendarApp.
Hasta ahora solo Proyecto I tenía el suyo (`build_calendar_proyecto1_54es4.py`); esto lo
generaliza a los otros cuatro cursos.

MEET AUTOGESTIONADO (2026-08-11)
    `CalendarApp` no adjunta videoconferencia, así que hasta ahora el `.gs` solo dejaba el
    enlace en Ubicación — y cuatro de los cinco cursos ni siquiera tenían sala: el material
    salía con el marcador de posición de `meet_url()`. Ahora el propio `.gs` **crea la sala**
    usando el servicio avanzado de Calendar (`Calendar.Events.patch` + `createRequest`) en el
    PRIMER evento de la serie, y **reutiliza ese mismo enlace** en los demás pasando
    `conferenceId` + `conferenceSolution` + `entryPoints` **sin** `createRequest` — que es
    como Calendar copia el Meet al duplicar un evento (patrón ya probado en producción en
    `Especializacion/Proyecto I/2026/54ES4/NO USAR - Actualizar Meet en encuentros (mismo
    enlace).gs`, hoy obsoleto: ver MEET_POR_SESION más abajo).
    Un solo enlace para toda la serie, con chip nativo, sin trabajo manual.

    Orden de preferencia de la sala, para no crear nunca dos:
      1. `MEET_URL` (viene de `carga_academica_2026.json → cursos.<key>.meet`).
      2. La que este mismo script guardó en `ScriptProperties[PROP_MEET]`.
      3. La que ya tenga un evento de la serie (si se crearon en una corrida previa).
      4. Crear una nueva — y entonces imprime dónde pegarla para que el correo de bienvenida
         y el LEEME del estudiante dejen de mostrar el marcador de posición.
    Sin servicio avanzado el script NO se rompe: crea los eventos igual y avisa cómo activarlo.

TG3 = UNA SOLA SERIE para los tres grupos
    54450, 54466 y 54467 comparten horario (martes 5–6 pm) y **un solo enlace de Meet**
    (decisión del docente). Por eso se genera un único `.gs` en `2026/_combinado_todos/`
    que invita a los tres rosters juntos. Ojo con el cierre: 54450 termina el 15/11 y los
    otros dos el 22/11, así que a la ÚLTIMA sesión (posterior al cierre de 54450) solo se
    invita a 54466/54467. El script lo marca por evento.

NOMBRES DE ARCHIVO — flujo principal vs. respaldo
    El `.gs` se llama `PRINCIPAL - Crear encuentros con invitados.gs` y los `.ics`/`.csv` de
    los MISMOS encuentros (que emite `build_pregrado_cursos.py`) llevan el prefijo
    `RESPALDO sin invitados - `. El nombre del archivo es lo primero que ve el docente: sin
    esa marca, importar el `.ics` que está al lado deja la serie con cero estudiantes.

ROSTER — de dónde salen los correos
    De `<Curso>/2026/<grupo>/`, en el primer archivo que encuentre con correos:
    `.ods`, `.xlsx`, `.csv` o `.txt` (cualquier nombre; se extraen por expresión regular).
    Si un grupo no tiene roster, ese curso se **omite con aviso** (no se inventan invitados).

Uso:
  python config/slides/build_calendar_encuentros.py            # todos los que tengan roster
  python config/slides/build_calendar_encuentros.py tg2        # uno solo

Orden recomendado: primero `build_pregrado_cursos.py --calendar-only` (renombra los
respaldos) y después este, para que el LEEME liste los archivos con su nombre definitivo.
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
from carga_academica import (  # noqa: E402
    _parse_date as _pdate,
    curso as carga_curso,
    fmt_dmy as _fmt_dmy,
)

EMAIL_RX = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# LOS CINCO cursos, Proyecto I incluido (2026-08-11). Antes quedaba fuera «porque tenía su
# propio builder», y el resultado fue que el único curso que ya empezó era el único sin el
# rótulo PRINCIPAL/RESPALDO, sin Meet autogestionado y con un runbook de 114 palabras frente
# a las ~1.400 de los otros cuatro. `build_calendar_proyecto1_54es4.py` sigue existiendo para
# lo que sí es suyo (CSV/ICS de respaldo, coanfitrión AFI, tutorías); el `.gs` y el runbook
# salen de aquí, para los cinco por igual.
CURSOS = ("proyecto1", "creatividad", "investigacion", "tg2", "tg3")
TG3_GRUPOS = ("54450", "54466", "54467")
TG3_CIERRE_CORTO = "54450"  # cierra 15/11; no asiste a la última sesión de la serie

GS_NAME = "PRINCIPAL - Crear encuentros con invitados.gs"
GS_NAME_TG3 = "PRINCIPAL - Crear encuentros con invitados (3 grupos).gs"
LEEME_NAME = "LEEME - Crear los eventos de Calendar.md"
# Nombres que usaron versiones anteriores de este build; se borran al regenerar para que
# no queden dos .gs con el mismo contenido y distinto nombre en la carpeta del docente.
GS_LEGACY = ("Crear encuentros con invitados.gs", "Crear encuentros con invitados (3 grupos).gs")

DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")


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


# Cuerpo JS invariable del script: todo lo que cambia por curso viaja en las variables de
# configuración que emite `_gs_texto`. Se mantiene FUERA de la f-string a propósito —
# doblar un centenar de llaves de JavaScript para meterlas en una f-string es exactamente
# de donde salen los errores tontos.
GS_FUNCIONES = r"""
// ═════════════════════════════ PÚBLICAS ══════════════════════════════════════

/**
 * SOLO LECTURA. Dice exactamente qué va a pasar —con los eventos y con el Meet—
 * sin crear, modificar ni borrar nada. Ejecuta SIEMPRE esto primero.
 */
function verificar() {
  var cal = CalendarApp.getDefaultCalendar();
  Logger.log('CURSO     : ' + CURSO + '  (clave interna: ' + CURSO_KEY + ')');
  Logger.log('CALENDARIO: ' + cal.getName() + '  (' + cal.getId() + ')');
  Logger.log('SESIONES  : ' + SESIONES.length + '  ·  invitados distintos: ' +
             _todosLosInvitados_().length);
  Logger.log('Servicio avanzado «Google Calendar API»: ' +
             (_apiCalendar_() ? 'ACTIVADO' : 'NO ACTIVADO'));
  Logger.log('--- sesiones ---------------------------------------------------');
  var existen = 0;
  SESIONES.forEach(function (s) {
    var ya = _buscarEvento_(cal, s);
    if (ya) existen++;
    Logger.log(s.start.substring(0, 10) + '  ' + s.subject +
               '  invitados=' + _invitados(s.grupos).length +
               ' [' + s.grupos.join(', ') + ']' +
               (ya ? '   <- YA EXISTE (no se duplica)' : ''));
  });
  Logger.log('--- Meet -------------------------------------------------------');
  var guardado = _salaGuardada_();
  // Solo se rastrean los eventos si no hay respuesta más barata: son N consultas a la API.
  var enEvento = (!_meetConfigurado_() && !guardado && _apiCalendar_())
    ? _meetDeLaSerieExistente_(cal) : '';
  if (_meetConfigurado_()) {
    Logger.log('Ya hay sala en el material: ' + MEET_URL);
    Logger.log('Se REUTILIZA en las ' + SESIONES.length + ' sesiones. No se crea ninguna otra.');
  } else if (guardado) {
    Logger.log('Este script ya creó la sala ' + guardado + ' en una ejecución anterior.');
    Logger.log('Se REUTILIZA. No se crea ninguna otra.');
    Logger.log('Si todavía no la has pegado en el material, hazlo:');
    Logger.log('  config/cursos/carga_academica_2026.json -> cursos.' + CURSO_KEY + '.meet');
  } else if (enEvento) {
    Logger.log('Los encuentros ya existentes tienen la sala ' + enEvento + '.');
    Logger.log('Se REUTILIZA esa misma. No se crea ninguna otra.');
  } else if (_apiCalendar_()) {
    Logger.log('Todavía NO hay sala. crearEncuentros() creará UNA sola, la pondrá en las ' +
               SESIONES.length + ' sesiones');
    Logger.log('y la imprimirá aquí para que la pegues en:');
    Logger.log('  config/cursos/carga_academica_2026.json -> cursos.' + CURSO_KEY + '.meet');
  } else {
    Logger.log('NO habrá videoconferencia: falta el servicio avanzado y el material no trae');
    Logger.log('enlace. Actívalo en el editor: Servicios (+) -> «Google Calendar API» -> Añadir.');
    Logger.log('Sin él los eventos se crean igual (con invitados), pero sin Meet.');
  }
  Logger.log('----------------------------------------------------------------');
  Logger.log(existen === SESIONES.length
    ? 'Los ' + existen + ' encuentros ya están creados: crearEncuentros() solo tocará el Meet.'
    : 'Si esto cuadra, ejecuta crearEncuentros().');
  Logger.log('¿Matrícula nueva en encuentros que ya existen? -> verificarInvitados().');
}

/**
 * Crea los encuentros con invitados y deja la MISMA sala de Meet en todos.
 * Es idempotente: reejecutarlo no duplica eventos ni crea una segunda sala.
 */
function crearEncuentros() {
  var cal = CalendarApp.getDefaultCalendar();
  var eventos = [], creados = 0, existentes = 0;

  SESIONES.forEach(function (s) {
    var ya = _buscarEvento_(cal, s);
    if (ya) { existentes++; eventos.push(ya); return; }
    eventos.push(cal.createEvent(s.subject, _fecha(s.start), _fecha(s.end), {
      description: s.description + '\nCDigital: ' + CDIGITAL,
      guests: _invitados(s.grupos).join(','),
      sendInvites: SEND_INVITES
    }));
    creados++;
  });
  Logger.log('Encuentros: creados=' + creados + ' · ya existían=' + existentes +
             ' · sendInvites=' + SEND_INVITES);

  // ── Meet ───────────────────────────────────────────────────────────────────
  var nativos = 0, soloEnlace = 0, url;

  if (MEET_POR_SESION) {
    // Una sala por encuentro. Se crea SOLO en el que no tenga ya la suya: así reejecutar esto no
    // le cambia el enlace a nadie, que es lo que invalidaría las invitaciones ya enviadas.
    var conSala = 0, nuevas = 0, sinSala = 0;
    eventos.forEach(function (ev, i) {
      var suya = _apiCalendar_() ? _meetNativo_(_idApi_(ev)) : '';
      if (!suya && _meetId_(ev.getLocation())) suya = ev.getLocation();
      if (suya) {
        conSala++;
      } else {
        suya = _crearSala_(ev, 's' + (i + 1));
        if (suya) { nuevas++; } else { sinSala++; return; }
      }
      if (_aplicarMeet_(ev, suya)) nativos++; else soloEnlace++;
    });
    Logger.log('Meet POR SESIÓN -> ya tenían=' + conSala + ' · creadas=' + nuevas +
               ' · sin sala=' + sinSala);
    Logger.log('  chip nativo en ' + nativos + ' · solo enlace en ' + soloEnlace +
               (_apiCalendar_() ? '' : '  (activa «Google Calendar API» para el chip)'));
    Logger.log(sinSala ? 'Quedaron ' + sinSala + ' encuentros sin sala: reintenta en un minuto.'
                       : 'Listo. Cada encuentro tiene su propio enlace.');
    return;
  }

  url = _salaDeLaSerie_(cal, eventos[0]);
  if (!url) {
    Logger.log('Los encuentros quedaron creados, pero SIN enlace de Meet.');
    Logger.log('Activa el servicio avanzado («Google Calendar API») y vuelve a ejecutar');
    Logger.log('crearEncuentros(): no duplica nada, solo añade la sala.');
    return;
  }
  eventos.forEach(function (ev) { if (_aplicarMeet_(ev, url)) nativos++; else soloEnlace++; });
  Logger.log('Meet ' + url + ' -> chip nativo en ' + nativos + ' · solo enlace en ' + soloEnlace +
             (_apiCalendar_() ? '' : '  (activa «Google Calendar API» para el chip)'));
  Logger.log(nativos
    ? 'Listo. Abre un evento en Calendar: debe tener Invitados y «Unirse con Google Meet».'
    : 'Listo. Abre un evento: tiene Invitados y el enlace en Ubicación, pero sin chip nativo.');
}

// ═══════ AÑADIR INVITADOS A ENCUENTROS QUE YA EXISTEN ════════════════════════
//
// Para cuando la serie ya está en el calendario y llega matrícula nueva. Estas dos órdenes
// NO crean eventos, NO quitan a nadie y NO tocan el Meet: solo suman los invitados que
// falten. El Meet es el asidero para encontrar los encuentros (ver MEET_ID arriba).

/**
 * SOLO LECTURA. Dice, encuentro por encuentro, a quién le falta la invitación y quién está
 * invitado sin estar en el roster. No escribe nada. Ejecuta SIEMPRE esto primero.
 */
function verificarInvitados() { _correrInvitados_('verificar'); }

/**
 * Añade a los encuentros que YA existen los invitados que les falten. Idempotente: si no
 * falta nadie no hace nada, y volver a ejecutarlo no invita a nadie dos veces.
 */
function agregarInvitados() { _correrInvitados_('agregar'); }

/**
 * SOLO LECTURA. Encuentro por encuentro, compara el Meet DE VERDAD del evento —el del chip— con
 * el enlace que anuncia su descripción, y dice cuáles no coinciden.
 *
 * Hace falta porque los encuentros creados cuando la serie compartía sala arrastran una línea
 * «Meet (mismo enlace toda la serie): …» que apunta a la sala vieja, mientras el chip del evento
 * lleva ya la suya. Quien lea la descripción entra a otra sala, y no tiene forma de saberlo.
 */
function verificarEnlaceEnDescripcion() { _correrDescripcion_('verificar'); }

/** Reescribe esa línea con el Meet real de cada encuentro. No toca nada más de la descripción. */
function arreglarEnlaceEnDescripcion() { _correrDescripcion_('arreglar'); }

function _correrDescripcion_(modo) {
  var cal = CalendarApp.getDefaultCalendar();
  var revisados = 0, malos = 0, arreglados = 0, sinChip = 0;
  Logger.log('MODO: ' + modo + (modo === 'verificar' ? '  (no escribe nada)' : '  (ESCRIBE)'));

  SESIONES.forEach(function (s) {
    var ev = _buscarEvento_(cal, s);
    if (!ev) { Logger.log('  (no esta) ' + s.subject); return; }
    revisados++;

    var real = _apiCalendar_() ? _meetNativo_(_idApi_(ev)) : '';
    if (!real && _meetId_(ev.getLocation())) real = ev.getLocation();
    if (!real) { sinChip++; Logger.log('  SIN MEET  ' + ev.getTitle()); return; }

    // La descripción se recorre por líneas y no con una expresión regular multilínea: es más fácil
    // de leer, y sobre todo no toca ni una línea más que la del enlace.
    var lineas = (ev.getDescription() || '').split('\n');
    var idx = -1, anunciado = '';
    for (var i = 0; i < lineas.length; i++) {
      var m = lineas[i].match(/Meet[^:]*:\s*(https:\/\/meet\.google\.com\/[a-z-]+)/i);
      if (m) { idx = i; anunciado = m[1]; break; }
    }
    if (anunciado && _meetId_(anunciado) === _meetId_(real)) return;   // coincide: nada que hacer

    malos++;
    Logger.log('  DISTINTO  ' + ev.getTitle());
    Logger.log('     chip del evento : ' + real);
    Logger.log('     dice la descrip.: ' + (anunciado || '(no anuncia ninguno)'));
    if (modo !== 'arreglar') return;

    if (idx >= 0) lineas[idx] = 'Meet de esta sesion: ' + real;
    else lineas.push('Meet de esta sesion: ' + real);
    try { ev.setDescription(lineas.join('\n')); arreglados++; }
    catch (e) { Logger.log('     no se pudo escribir: ' + e); }
  });

  Logger.log('');
  Logger.log('Encuentros revisados=' + revisados + ' · con enlace distinto=' + malos +
             ' · sin Meet=' + sinChip + (modo === 'arreglar' ? ' · corregidos=' + arreglados : ''));
  if (malos && modo !== 'arreglar') {
    Logger.log('Para corregirlos: arreglarEnlaceEnDescripcion(). Solo toca esa linea.');
  }
}

function _correrInvitados_(modo) {
  _INICIO_ = Date.now();
  var cal = CalendarApp.getDefaultCalendar();
  var sala = _salaObjetivo_(cal);
  var explicitos = _correosLimpios_(NUEVOS);
  if (NUEVOS && NUEVOS.length && !explicitos.length) {
    // Si no, «NUEVOS = ['<tu correo>']» acabaría invitando al roster entero sin decirlo.
    throw new Error('NUEVOS solo trae tu propio correo: tú eres el organizador, no un ' +
      'invitado. Déjalo vacío ([]) si lo que quieres es añadir el roster completo.');
  }

  Logger.log('CURSO     : ' + CURSO + '  (clave interna: ' + CURSO_KEY + ')');
  Logger.log('CALENDARIO: ' + cal.getName() + '  (' + cal.getId() + ')');
  Logger.log('SALA      : ' + (sala.id ? sala.id + '   <- ' + sala.origen
    : '(ninguna conocida: busco solo por el título de las sesiones)'));
  Logger.log('A INVITAR : ' + (explicitos.length
    ? 'solo los ' + explicitos.length + ' correos de NUEVOS'
    : 'el roster de este archivo (' + _todosLosInvitados_().length + ' correos)'));
  Logger.log('Servicio avanzado «Google Calendar API»: ' +
             (_apiCalendar_() ? 'ACTIVADO' : 'NO ACTIVADO'));
  if (!_apiCalendar_()) {
    Logger.log('  Sin él invito de a uno y NO puedo elegir si se les notifica: Google les');
    Logger.log('  manda la invitación. Actívalo (Servicios + -> «Google Calendar API») para');
    Logger.log('  que SEND_INVITES = ' + SEND_INVITES + ' mande de verdad.');
  }
  if (!MEET_POR_SESION && sala.id && _meetConfigurado_() && sala.id !== _meetId_(MEET_URL)) {
    Logger.log('');
    Logger.log('  !! OJO: esa sala NO es la de ' + CURSO + ' (' + MEET_URL + ').');
    Logger.log('  !! Si te equivocaste de curso al copiar el id, PÁRATE AQUÍ: este archivo');
    Logger.log('  !! invitaría al roster de ' + CURSO + ' a los encuentros de otro curso.');
    Logger.log('');
  }

  var objetivos = _objetivosInvitados_(cal, sala.id);
  if (!objetivos.length) {
    Logger.log('No encontré NINGÚN encuentro de esta serie en el calendario.');
    Logger.log('Si todavía no los has creado, eso lo hace crearEncuentros(). Si los creaste');
    Logger.log('con otro nombre, pon el id de la sala en MEET_ID y vuelve a ejecutar.');
    return;
  }

  var faltantes = 0, sobrantes = {}, distintos = {};
  Logger.log('--- encuentros ya creados --------------------------------------');
  objetivos.forEach(function (o) {
    var deben = explicitos.length ? explicitos : _correosDeSesion_(o);
    var ya = {};
    o.asistentes.forEach(function (a) {
      if (a && a.email) ya[String(a.email).toLowerCase()] = true;
    });
    o.faltan = deben.filter(function (e) { return !ya[e.toLowerCase()]; });
    faltantes += o.faltan.length;
    o.faltan.forEach(function (e) { distintos[e.toLowerCase()] = true; });
    // «Sobran» = invitados que el roster ya no tiene (bajas). Solo se informa: para quitar a
    // alguien hay que abrir el evento, que es una decisión con consecuencias para esa persona.
    if (!explicitos.length) {
      var esperado = {};
      deben.forEach(function (e) { esperado[e.toLowerCase()] = true; });
      o.asistentes.forEach(function (a) {
        var e = a && a.email ? String(a.email).toLowerCase() : '';
        if (e && !esperado[e] && e !== String(DOCENTE).toLowerCase()) sobrantes[e] = true;
      });
    }
    Logger.log(o.dia + '  ' + o.titulo +
               (o.porMeet ? '   [FUERA DE SESIONES · lo hallé por el Meet]' : '') +
               '  invitados=' + o.asistentes.length + '  faltan=' + o.faltan.length +
               (o.faltan.length ? '  -> ' + _resumirLista_(o.faltan) : ''));
  });

  var hallados = {};
  objetivos.forEach(function (o) { if (o.sesion) hallados[o.sesion.subject] = true; });
  var sinCrear = SESIONES.filter(function (s) { return !hallados[s.subject]; });

  Logger.log('--- resumen ----------------------------------------------------');
  Logger.log('Encuentros hallados: ' + objetivos.length + ' de ' + SESIONES.length +
             ' sesiones' + (sinCrear.length ? '  ·  sin crear todavía: ' + sinCrear.length +
             ' (eso es crearEncuentros())' : ''));
  Logger.log('Invitaciones que faltan: ' + faltantes + '  ·  personas distintas: ' +
             _cuantas_(distintos));
  var basura = _cuantas_(sobrantes);
  if (basura) {
    Logger.log('Invitados que ya NO están en el roster: ' + basura + ' -> ' +
               _resumirLista_(_claves_(sobrantes)));
    Logger.log('  (posibles bajas. NO se quita a nadie: eso se hace a mano en el evento.)');
  }

  if (modo !== 'agregar') {
    Logger.log('----------------------------------------------------------------');
    Logger.log(faltantes ? 'Si esto cuadra, ejecuta agregarInvitados().'
                         : 'No falta nadie: no hay nada que ejecutar.');
    return;
  }
  if (!faltantes) { Logger.log('No falta nadie: no toco nada.'); return; }

  var sumados = 0, tocados = 0, cortado = false;
  Logger.log('--- añadiendo -------------------------------------------------');
  for (var i = 0; i < objetivos.length; i++) {
    var o = objetivos[i];
    if (!o.faltan.length) continue;
    if (_sinTiempo_()) { cortado = true; break; }
    var n = _agregarA_(o, o.faltan);
    if (n) { sumados += n; tocados++; Logger.log('  +' + n + '  ' + o.dia + '  ' + o.titulo); }
  }
  Logger.log('Añadidos: ' + sumados + ' invitaciones en ' + tocados + ' encuentros · ' +
             'sendInvites=' + SEND_INVITES);
  if (cortado) {
    Logger.log('CORTADO por el límite de 6 minutos de Apps Script. Vuelve a ejecutar');
    Logger.log('agregarInvitados(): continúa por donde se quedó y no repite a nadie.');
  } else {
    Logger.log('Listo. Abre un encuentro en Calendar y cuenta los invitados.');
  }
}

/**
 * Deshacer: borra SOLO los eventos cuyo título coincide exactamente con los de SESIONES.
 * Si ya notificaste a los estudiantes (SEND_INVITES = true), recibirán la cancelación.
 * NO olvida la sala de Meet: para eso está olvidarSalaMeet().
 */
function borrarEncuentros() {
  var cal = CalendarApp.getDefaultCalendar();
  var titulos = {};
  SESIONES.forEach(function (s) { titulos[s.subject] = true; });
  var desde = _fecha(SESIONES[0].start);
  var hasta = _fecha(SESIONES[SESIONES.length - 1].end);
  var n = 0;
  cal.getEvents(desde, new Date(hasta.getTime() + 36e5)).forEach(function (ev) {
    if (titulos[ev.getTitle()]) { ev.deleteEvent(); n++; }
  });
  Logger.log('Eliminados=' + n + '. La sala de Meet sigue guardada (olvidarSalaMeet() la suelta).');
}

/**
 * Deshacer (Meet): olvida la sala que este script creó, para que la próxima ejecución
 * genere otra. Úsalo solo si la sala quedó mal; la sala vieja NO se borra de Google.
 */
function olvidarSalaMeet() {
  var props = PropertiesService.getScriptProperties();
  var antes = props.getProperty(PROP_MEET) || '(ninguna)';
  props.deleteProperty(PROP_MEET);
  Logger.log('Olvidada: ' + antes);
  Logger.log('Ojo: si los eventos ya existen, siguen apuntando a esa sala. Para cambiarla,');
  Logger.log('ejecuta borrarEncuentros() y después crearEncuentros().');
}

// ═════════════════════════════ INTERNAS ══════════════════════════════════════

/** ¿Está añadido el servicio avanzado «Google Calendar API»? */
function _apiCalendar_() {
  try { return typeof Calendar !== 'undefined' && !!Calendar.Events; }
  catch (e) { return false; }
}

/** ¿MEET_URL trae una sala de verdad o el marcador de posición del builder? */
function _meetConfigurado_() {
  return typeof MEET_URL === 'string' && MEET_URL.indexOf('https://meet.google.com/') === 0;
}

function _salaGuardada_() {
  return (PropertiesService.getScriptProperties().getProperty(PROP_MEET) || '').trim();
}

/** Id que entiende la API avanzada, a partir del id de CalendarApp. */
function _idApi_(evento) { return evento.getId().split('@')[0]; }

/** Evento ya existente para esa sesión (mismo título, mismo día), o null. */
/** Clave de comparación: minúsculas y espacios normalizados. */
function _claveTitulo_(t) {
  return String(t == null ? '' : t).replace(/\s+/g, ' ').trim().toLowerCase();
}

/**
 * ¿El título de este evento es el de esta sesión?
 *
 * NO se compara con `===`, y eso es lo que estaba roto. Los encuentros del calendario pueden
 * llevar el prefijo del periodo o no llevarlo: «26ES4 - 54ES4 - Proyecto I - Sesion 06» y
 * «54ES4 - Proyecto I - Sesion 06» son el mismo encuentro, y con la comparación exacta el guion
 * no reconocía ninguno. Las consecuencias eran las dos peores posibles: `verificarInvitados()`
 * decía «no encontré NINGÚN encuentro» con los once delante, y `crearEncuentros()` los daba por
 * inexistentes y creaba once duplicados encima.
 *
 * Se compara por el FINAL, que es donde está lo que distingue —grupo, curso y número de sesión—,
 * y exigiendo que el corte caiga en un separador para no casar a media palabra.
 */
function _mismoTitulo_(tituloEvento, subject) {
  var a = _claveTitulo_(tituloEvento), b = _claveTitulo_(subject);
  if (!a || !b) return false;
  if (a === b) return true;
  var largo = a.length > b.length ? a : b, corto = a.length > b.length ? b : a;
  if (largo.slice(-corto.length) !== corto) return false;
  if (!/[\s\-]$/.test(largo.slice(0, largo.length - corto.length))) return false;
  // El trozo corto tiene que seguir identificando al curso, no solo a la sesión: sin esto, un
  // evento ajeno llamado «Sesion 06» a la misma hora casaría, porque también es un final válido.
  // Se exige que conserve al menos un separador, es decir grupo y curso además del número.
  return corto.indexOf(' - ') >= 0;
}

/** La sesión a la que corresponde un título, o null. */
function _sesionDeTitulo_(titulo) {
  for (var i = 0; i < SESIONES.length; i++) {
    if (_mismoTitulo_(titulo, SESIONES[i].subject)) return SESIONES[i];
  }
  return null;
}

function _buscarEvento_(cal, s) {
  // Sin la opción `search`: buscaba el título completo, con el prefijo del periodo incluido, y por
  // eso no devolvía el evento que en el calendario se llama sin él. La ventana ya es estrecha.
  var hallados = cal.getEvents(_fecha(s.start), _fecha(s.end))
    .filter(function (ev) { return _mismoTitulo_(ev.getTitle(), s.subject); });
  return hallados.length ? hallados[0] : null;
}

/** URL de vídeo dentro de un conferenceData, o '' si no hay. */
function _uriDeConferencia_(conf) {
  if (!conf || !conf.entryPoints) return '';
  for (var i = 0; i < conf.entryPoints.length; i++) {
    if (conf.entryPoints[i].entryPointType === 'video') return conf.entryPoints[i].uri || '';
  }
  return '';
}

/** Enlace de Meet nativo que ya tiene un evento, o '' si no tiene. */
function _meetNativo_(id) {
  if (!_apiCalendar_()) return '';
  try {
    var ev = Calendar.Events.get('primary', id, { conferenceDataVersion: 1 });
    return _uriDeConferencia_(ev && ev.conferenceData);
  } catch (e) { return ''; }
}

/** Meet que ya tenga cualquier encuentro de la serie (de una corrida anterior). */
function _meetDeLaSerieExistente_(cal) {
  for (var i = 0; i < SESIONES.length; i++) {
    var ev = _buscarEvento_(cal, SESIONES[i]);
    if (ev) {
      var u = _meetNativo_(_idApi_(ev));
      if (u) return u;
    }
  }
  return '';
}

/**
 * conferenceData reutilizable a partir de una URL de Meet ya conocida.
 * SIN createRequest: así es como Calendar copia el Meet al duplicar un evento, y por eso
 * los N encuentros acaban con el MISMO enlace en vez de con N salas distintas.
 */
function _conferenciaDesdeUrl_(url) {
  var id = String(url).replace(/^https?:\/\/meet\.google\.com\//, '');
  return {
    conferenceId: id,
    signature: null,
    conferenceSolution: { key: { type: 'hangoutsMeet' }, name: 'Google Meet' },
    entryPoints: [{ entryPointType: 'video', uri: url, label: id }]
  };
}

/**
 * La sala de TODA la serie. Orden de preferencia, pensado para no crear nunca una segunda:
 *   1) MEET_URL del material   2) la que guardé antes   3) la que ya tiene un evento
 *   4) crear una nueva sobre `semilla`.
 * Devuelve '' si no hay forma (sin servicio avanzado y sin enlace en el material).
 */
function _salaDeLaSerie_(cal, semilla) {
  if (_meetConfigurado_()) return MEET_URL;

  var guardado = _salaGuardada_();
  if (guardado) { Logger.log('Reutilizo la sala que creé antes: ' + guardado); return guardado; }

  if (!_apiCalendar_()) return '';

  var enEvento = _meetDeLaSerieExistente_(cal);
  if (enEvento) {
    PropertiesService.getScriptProperties().setProperty(PROP_MEET, enEvento);
    Logger.log('Reutilizo la sala que ya tenían los encuentros: ' + enEvento);
    return enEvento;
  }
  if (!semilla) return '';

  var url = _crearSala_(semilla);
  if (!url) return '';
  PropertiesService.getScriptProperties().setProperty(PROP_MEET, url);
  Logger.log('');
  Logger.log('  +--------------------------------------------------------------');
  Logger.log('  | SALA DE MEET CREADA: ' + url);
  Logger.log('  | Es la de las ' + SESIONES.length + ' sesiones. Cópiala y pégala en el material:');
  Logger.log('  |   config/cursos/carga_academica_2026.json -> cursos.' + CURSO_KEY + '.meet');
  Logger.log('  | Y reconstruye: así el correo de bienvenida, el LEEME del estudiante y el');
  Logger.log('  | calendario del curso dejan de mostrar el marcador de posición.');
  Logger.log('  +--------------------------------------------------------------');
  Logger.log('');
  return url;
}

/** Crea UNA sala de Meet sobre `evento` y devuelve su URL ('' si no se pudo). */
function _crearSala_(evento, sufijo) {
  var id = _idApi_(evento);
  try {
    var res = Calendar.Events.patch({
      conferenceData: {
        createRequest: {
          // Determinista a propósito: si se repite el requestId, Google NO crea otra sala. Por eso
          // el sufijo por sesión es imprescindible cuando cada encuentro lleva la suya: sin él,
          // Google devolvería la MISMA sala once veces y el cambio no se notaría.
          requestId: REQUEST_ID + (sufijo ? '-' + sufijo : ''),
          conferenceSolutionKey: { type: 'hangoutsMeet' }
        }
      }
    }, 'primary', id, { conferenceDataVersion: 1, sendUpdates: 'none' });

    var url = _uriDeConferencia_(res && res.conferenceData);
    // Google crea la sala de forma asíncrona: la primera respuesta puede venir «pending».
    for (var i = 0; !url && i < 10; i++) {
      Utilities.sleep(1500);
      url = _meetNativo_(id);
    }
    if (!url) {
      Logger.log('AVISO: Google aceptó la petición pero todavía no devuelve el enlace.');
      Logger.log('Espera un minuto y vuelve a ejecutar crearEncuentros() (no duplica nada).');
    }
    return url;
  } catch (e) {
    Logger.log('AVISO: no se pudo crear la sala de Meet: ' + e);
    Logger.log('Los encuentros quedan creados igual; revisa el servicio avanzado y reintenta.');
    return '';
  }
}

/**
 * Deja `url` en un evento: Ubicación + línea en la descripción (que es lo que se ve en el
 * correo) y, si hay servicio avanzado, el chip nativo «Unirse con Google Meet».
 * Devuelve true si quedó el chip nativo.
 */
function _aplicarMeet_(evento, url) {
  try {
    if (evento.getLocation() !== url) evento.setLocation(url);
    var d = evento.getDescription() || '';
    if (d.indexOf(url) < 0) {
      evento.setDescription((d ? d + '\n' : '') + (MEET_POR_SESION ? 'Meet de esta sesión: '
                                          : 'Meet (mismo enlace toda la serie): ') + url);
    }
  } catch (e) {
    Logger.log('AVISO: no pude escribir el enlace en «' + evento.getTitle() + '»: ' + e);
  }
  if (!_apiCalendar_()) return false;
  try {
    var id = _idApi_(evento);
    if (_meetNativo_(id) === url) return true;   // ya está bien: no lo toques
    Calendar.Events.patch({ conferenceData: _conferenciaDesdeUrl_(url) }, 'primary', id, {
      conferenceDataVersion: 1,
      sendUpdates: SEND_INVITES ? 'all' : 'none'
    });
    return _meetNativo_(id) === url;
  } catch (e) {
    Logger.log('AVISO: sin chip nativo en «' + evento.getTitle() + '»: ' + e);
    return false;
  }
}

// ── internas de verificarInvitados() / agregarInvitados() ────────────────────

var _INICIO_ = 0;

/** Quedan menos de minuto y medio del tope de 6 min de Apps Script. */
function _sinTiempo_() { return !!_INICIO_ && (Date.now() - _INICIO_) > 270000; }

/**
 * Código de una sala de Meet, sin guiones y en minúsculas, para poder comparar.
 * Acepta la URL completa (aunque venga dentro de un texto más largo), el código con
 * guiones o el código pelado. Devuelve '' si ahí no hay ninguna sala.
 */
function _meetId_(x) {
  var s = String(x == null ? '' : x).trim().toLowerCase();
  var url = s.match(/meet\.google\.com\/([a-z0-9\-]+)/);
  if (url) return url[1].replace(/-/g, '');
  if (/^[a-z0-9]{2,}-[a-z0-9]{2,}-[a-z0-9]{2,}$/.test(s)) return s.replace(/-/g, '');
  if (/^[a-z0-9]{8,}$/.test(s)) return s;
  return '';
}

/**
 * La sala que identifica la serie, y de dónde salió. Orden: lo que pusiste en MEET_ID >
 * el material > la que creó este script > la que ya tienen los encuentros.
 */
function _salaObjetivo_(cal) {
  var puesto = String(MEET_ID == null ? '' : MEET_ID).trim();
  if (puesto) {
    var id = _meetId_(puesto);
    if (!id) {
      throw new Error('MEET_ID = «' + puesto + '» no parece un Meet. Pon la URL completa ' +
        '(https://meet.google.com/abc-defg-hij) o solo el código (abc-defg-hij).');
    }
    return { id: id, origen: 'MEET_ID, que pusiste arriba' };
  }
  // Con una sala por sesión no hay «la sala de la serie»: el ancla es el título. Devolver aquí
  // MEET_URL haría que el aviso de más abajo gritara, en cada encuentro, que la sala no es la del
  // curso — que es justo lo que pasaba.
  if (MEET_POR_SESION) return { id: '', origen: '' };
  if (_meetConfigurado_()) return { id: _meetId_(MEET_URL), origen: 'MEET_URL del material' };
  var guardado = _salaGuardada_();
  if (guardado) return { id: _meetId_(guardado), origen: 'la sala que creó este script' };
  var enEvento = _apiCalendar_() ? _meetDeLaSerieExistente_(cal) : '';
  if (enEvento) return { id: _meetId_(enEvento), origen: 'la sala que ya tienen los encuentros' };
  return { id: '', origen: '' };
}

/** Sala de un evento de la API avanzada: chip nativo, si no Ubicación, si no descripción. */
function _meetIdDeEventoApi_(ev) {
  return _meetId_(_uriDeConferencia_(ev.conferenceData)) ||
         _meetId_(ev.location) || _meetId_(ev.description);
}

/** Todos los eventos del periodo del curso. Una sola consulta (más las páginas que haga falta). */
function _eventosDelPeriodo_() {
  var desde = _fecha(SESIONES[0].start);
  var hasta = new Date(_fecha(SESIONES[SESIONES.length - 1].end).getTime() + 36e5);
  var items = [], token = '';
  do {
    var opt = {
      timeMin: desde.toISOString(), timeMax: hasta.toISOString(),
      singleEvents: true, maxResults: 2500, orderBy: 'startTime'
    };
    if (token) opt.pageToken = token;
    var r = Calendar.Events.list('primary', opt);
    items = items.concat(r.items || []);
    token = (r && r.nextPageToken) || '';
  } while (token);
  return items;
}

/**
 * Encuentros YA creados a los que hay que revisarles los invitados. Entra un evento si:
 *   - su título es uno de SESIONES —la vía normal—, o
 *   - usa la sala buscada: eso es lo que compra el Meet como asidero, y alcanza los eventos
 *     que renombraste a mano o las tutorías que no están en SESIONES (van marcadas).
 * Con el servicio avanzado los invitados vienen en la misma consulta; sin él se leen con
 * CalendarApp, que también ve la Ubicación y la descripción.
 */
function _objetivosInvitados_(cal, idSala) {
  var porTitulo = {};
  SESIONES.forEach(function (s) { porTitulo[s.subject] = s; });
  var out = [];

  if (_apiCalendar_()) {
    _eventosDelPeriodo_().forEach(function (ev) {
      if (ev.status === 'cancelled') return;
      var s = porTitulo[ev.summary] || _sesionDeTitulo_(ev.summary);
      var porMeet = !!idSala && _meetIdDeEventoApi_(ev) === idSala;
      if (!s && !porMeet) return;
      out.push({
        apiId: ev.id, evApp: null,
        titulo: ev.summary || '(sin título)',
        dia: String((ev.start && (ev.start.dateTime || ev.start.date)) || '').substring(0, 10),
        sesion: s, porMeet: porMeet && !s, faltan: [],
        asistentes: ev.attendees ? ev.attendees.slice(0) : []
      });
    });
  } else {
    var desde = _fecha(SESIONES[0].start);
    var hasta = new Date(_fecha(SESIONES[SESIONES.length - 1].end).getTime() + 36e5);
    cal.getEvents(desde, hasta).forEach(function (ev) {
      var s = porTitulo[ev.getTitle()] || _sesionDeTitulo_(ev.getTitle());
      var porMeet = !!idSala && (_meetId_(ev.getLocation()) === idSala ||
                                 _meetId_(ev.getDescription()) === idSala);
      if (!s && !porMeet) return;
      out.push({
        apiId: null, evApp: ev,
        titulo: ev.getTitle(),
        dia: Utilities.formatDate(ev.getStartTime(), TIMEZONE, 'yyyy-MM-dd'),
        sesion: s, porMeet: porMeet && !s, faltan: [],
        asistentes: ev.getGuestList().map(function (g) { return { email: g.getEmail() }; })
      });
    });
  }
  out.sort(function (a, b) { return a.dia < b.dia ? -1 : (a.dia > b.dia ? 1 : 0); });
  return out;
}

/** Quiénes deberían estar invitados a este encuentro. */
function _correosDeSesion_(o) {
  // Un evento fuera de SESIONES no declara grupos: se le invita a todo el roster, que en los
  // cursos de un solo grupo es lo mismo. Va marcado en el registro para que lo veas antes.
  return o.sesion ? _invitados(o.sesion.grupos) : _todosLosInvitados_();
}

/** Añade `correos` a un encuentro. Devuelve cuántos entraron. */
function _agregarA_(o, correos) {
  if (o.apiId) {
    // Un solo patch por evento con la lista completa: los que ya estaban van tal cual, así no
    // se pierde su respuesta («Sí asisto»), y 51 invitados cuestan una llamada, no 51.
    var lista = o.asistentes.slice(0);
    correos.forEach(function (e) { lista.push({ email: e }); });
    try {
      Calendar.Events.patch({ attendees: lista }, 'primary', o.apiId,
                            { sendUpdates: SEND_INVITES ? 'all' : 'none' });
      o.asistentes = lista;
      return correos.length;
    } catch (err) {
      Logger.log('AVISO: no pude invitar en «' + o.titulo + '»: ' + err);
      return 0;
    }
  }
  var n = 0;
  correos.forEach(function (e) {
    try { o.evApp.addGuest(e); n++; }
    catch (err) { Logger.log('AVISO: ' + e + ' no entró en «' + o.titulo + '»: ' + err); }
  });
  return n;
}

/** Correos de NUEVOS, validados. Revienta si hay algo que no es un correo (mejor que invitar mal). */
function _correosLimpios_(lista) {
  var out = [], vistos = {}, malos = [];
  (lista || []).forEach(function (x) {
    var e = String(x == null ? '' : x).trim();
    if (!e) return;
    if (!/^[^\s@,;]+@[^\s@,;]+\.[^\s@,;]+$/.test(e)) { malos.push(e); return; }
    var k = e.toLowerCase();
    if (k === String(DOCENTE).toLowerCase()) return;   // el organizador no es invitado
    if (!vistos[k]) { vistos[k] = true; out.push(e); }
  });
  if (malos.length) {
    throw new Error('NUEVOS tiene ' + malos.length + ' entrada(s) que no son un correo: ' +
      malos.join(', ') + '. Corrígelas y vuelve a ejecutar.');
  }
  return out;
}

function _resumirLista_(a) {
  return a.length <= 4 ? a.join(', ')
    : a.slice(0, 4).join(', ') + ' … y ' + (a.length - 4) + ' más';
}

function _claves_(o) { var k = []; for (var x in o) k.push(x); return k; }
function _cuantas_(o) { return _claves_(o).length; }

function _invitados(grupos) {
  var out = [], vistos = {};
  grupos.forEach(function (g) {
    (INVITADOS[g] || []).forEach(function (e) {
      if (!vistos[e]) { vistos[e] = true; out.push(e); }
    });
  });
  return out;
}

function _todosLosInvitados_() {
  var claves = [];
  for (var g in INVITADOS) claves.push(g);
  return _invitados(claves);
}

function _fecha(iso) {
  return Utilities.parseDate(iso.replace('T', ' '), TIMEZONE, 'yyyy-MM-dd HH:mm:ss');
}
"""


def _gs_texto(course_key: str, grupos_titulo: list[str], solo_ultima: list[str] | None,
              rosters: dict[str, list[str]], total: int) -> str:
    c = COURSES[course_key]
    ses = c["sesiones"]
    ini_iso = datetime.strptime(ses[0]["fecha"], "%d/%m/%Y").date().isoformat()

    invitados_js = ",\n".join(
        f"  {_js(g)}: [\n" + ",\n".join(f"    {_js(e)}" for e in rosters[g]) + "\n  ]"
        for g in grupos_titulo
    )

    nota_tg3 = ""
    if course_key == "tg3":
        nota_tg3 = (
            " * TG3 — UNA SOLA SERIE para los tres grupos: comparten horario y una sola sala de\n"
            " * Meet (por eso hay un único .gs y no tres). A la ÚLTIMA sesión no se invita a\n"
            f" * {TG3_CIERRE_CORTO}: su curso cierra antes.\n"
            " *\n"
        )

    cabecera = f"""/**
 * {c['titulo']} — Crear los encuentros en Calendar CON invitados y CON Meet.
 *
 * Google Calendar DESCARTA los invitados al importar .ics/.csv. Este script usa
 * CalendarApp y sí crea la sección Invitados. Los .ics/.csv que están al lado (los que
 * empiezan por «RESPALDO») son solo un respaldo de fechas: NO los importes salvo que
 * renuncies a los invitados.
 *
{nota_tg3} * MEET — el script se encarga solo. Crea UNA sala en el primer encuentro y pone ESE MISMO
 * enlace en todos los demás (chip nativo «Unirse con Google Meet»). Si el material ya trae
 * sala, la reutiliza y no crea ninguna otra. Reejecutarlo no duplica ni eventos ni salas.
 * Necesita el servicio avanzado de Calendar; si no está, crea los eventos igual (con
 * invitados) y avisa cómo activarlo.
 *
 * PASOS  (detalle completo en «{LEEME_NAME}», misma carpeta)
 * 1. https://script.google.com con la cuenta CUN ({DOCENTE_CORREO}).
 * 2. Nuevo proyecto -> pega TODO este archivo -> guarda.
 * 3. Editor -> Servicios (+) -> «Google Calendar API» -> Añadir.
 * 4. Ejecuta `verificar()` (SOLO LECTURA) y lee el registro.
 * 5. Si cuadra, ejecuta `crearEncuentros()`.
 * 6. Copia la URL de Meet que imprime -> carga_academica_2026.json -> cursos.{course_key}.meet
 * 7. Añade el coanfitrión de Meet a mano (eso no lo puede hacer la API).
 *
 * MATRÍCULA NUEVA, con los encuentros YA creados: `verificarInvitados()` (solo lectura) y
 * después `agregarInvitados()`. Añade a quien le falte en TODOS los encuentros de la serie;
 * no crea eventos, no quita a nadie y no toca el Meet. Los encuentros se localizan por el
 * título y —si pones `MEET_ID`— por la sala, que los alcanza incluso renombrados.
 *
 * Deshacer: `borrarEncuentros()` (eventos) · `olvidarSalaMeet()` (sala guardada).
 * Quitar un invitado NO lo hace este script: se abre el evento en Calendar.
 *
 * Regenerar este .gs: python config/slides/build_calendar_encuentros.py {course_key}
 */

// ───────────────────────────── CONFIGURACIÓN ─────────────────────────────────
var SEND_INVITES = false;  // true solo cuando quieras notificar a los estudiantes
var TIMEZONE = 'America/Bogota';
var CURSO = {_js(c['titulo'])};
var CURSO_KEY = {_js(course_key)};
// Sala real -> se reutiliza. Marcador de posición -> el script crea UNA y te dice dónde pegarla.
var MEET_URL = {_js(meet_url(course_key))};
var CDIGITAL = {_js(cdigital_url(course_key))};
// Dónde recuerda el script la sala que creó, para no crear una segunda al reejecutar.
var PROP_MEET = {_js('MEET_URL_' + course_key)};
// UNA SALA POR SESIÓN, que es como se trabaja desde el 31/08/2026.
// Antes toda la serie compartía un enlace y resultó problemático, así que ahora cada encuentro
// tiene el suyo. Con `true`:
//   · `crearEncuentros()` le crea a cada sesión su propia sala (requestId distinto por sesión);
//   · `verificarInvitados()` y `agregarInvitados()` buscan los encuentros **por su título** y no
//     por la sala, que ya no identifica a la serie;
//   · nada vuelve a escribir un mismo enlace en varios eventos.
// Ponlo en `false` solo si un curso concreto vuelve al enlace único, y entonces MEET_URL manda.
var MEET_POR_SESION = true;

// Determinista: Google ignora un createRequest con un requestId ya usado, así que ni
// borrando ScriptProperties se acaba con dos salas para la misma serie.
var REQUEST_ID = {_js(f'cun-{course_key}-{ini_iso}')};
var DOCENTE = {_js(DOCENTE_CORREO)};  // organizador: nunca se añade como invitado

// ── AÑADIR INVITADOS A ENCUENTROS YA CREADOS ─────────────────────────────────
// Para matrícula que llega después de crear la serie. Órdenes:
//   verificarInvitados()  (solo lectura)   ->   agregarInvitados()
// Caso normal: NO toques ninguna de las dos líneas de abajo. El archivo ya trae el roster
// al día (lo regenera el build desde el listado de CDigital) y añade a quien le falte.
var MEET_ID = '';  // Id o URL de la sala, p. ej. 'abc-defg-hij'. Vacío -> la de este curso.
                   // Sirve para encontrar los encuentros aunque los hayas renombrado a mano,
                   // y para alcanzar tutorías que no están en SESIONES.
var NUEVOS = [];   // Solo estos correos, p. ej. ['nuevo.estudiante@cun.edu.co'].
                   // Vacío -> todo el roster de INVITADOS (se añade el que falte).

// Roster por grupo ({total} invitados distintos en total).
var INVITADOS = {{
{invitados_js}
}};

var SESIONES = [
{_sesiones_js(course_key, grupos_titulo, solo_ultima)}
];
"""
    return cabecera + GS_FUNCIONES


# ── runbook (LEEME) ──────────────────────────────────────────────────────────
def _fecha_larga(ddmmyyyy: str) -> str:
    d = datetime.strptime(ddmmyyyy, "%d/%m/%Y").date()
    return f"{d.strftime('%d/%m/%Y')} ({DIAS[d.weekday()]})"


def _sync_fechas_txt(course_key: str, grupo_dir: Path) -> None:
    """Refresca las líneas de fecha de `Fechas.txt` e `Informacion.txt` desde la carga académica.

    Estos dos archivos vienen del portal y nadie los sincronizaba salvo en Proyecto I, que tiene
    su propio `_sync_txt_grupo()`. Resultado: Creatividad e Investigación anunciaban «Fecha de
    inicio: 03/08/2026» cuando la carga académica dice 10/08 en los cinco cursos. Solo se
    reescribe la línea de dato, nunca el texto explicativo, así que es idempotente.
    """
    if course_key == "proyecto1":
        return  # tiene su propio sync, más rico (incluye la línea del enlace de Meet)
    try:
        c = carga_curso(course_key)
        campos = {
            "Fecha de inicio:": _fmt_dmy(_pdate(c["inicio"])),
            "Fecha máxima para recepción de trabajos:": _fmt_dmy(_pdate(c["recepcion"])),
            "Recepción de trabajos:": _fmt_dmy(_pdate(c["recepcion"])),
            "Fecha de cierre:": _fmt_dmy(_pdate(c["cierre"])),
        }
    except Exception:
        return
    for nombre in ("Fechas.txt", "Informacion.txt"):
        path = grupo_dir / nombre
        if not path.is_file():
            continue
        out, tocado = [], False
        for linea in path.read_text(encoding="utf-8").split("\n"):
            limpio = linea.strip()
            for clave, valor in campos.items():
                if limpio.startswith(clave):
                    resto = limpio[len(clave):].strip()
                    cola = " " + resto[resto.index("("):] if "(" in resto else ""
                    nueva = f"{clave} {valor}{cola}"
                    tocado = tocado or nueva != linea
                    linea = nueva
                    break
            out.append(linea)
        if tocado:
            path.write_text("\n".join(out), encoding="utf-8")
            print(f"   sync {nombre} ({grupo_dir.name})")


ROSTER_NAME = "Correos estudiantes (invitados Calendar).txt"


def _escribir_roster_txt(course_key: str, dest_dir: Path, etiqueta: str, correos: list[str]) -> None:
    """Lista de correos del grupo, en UNA línea separada por comas y SIN espacios.

    El formato lo pidió el Docente (11/08/2026) y no es capricho: es el único que Google
    acepta de una pegada al añadir miembros a un grupo de Chat o de Grupos. Con un correo
    por línea —como estaba— hay que pegarlos de a uno, y son entre 20 y 112.

    Antes solo Proyecto I regeneraba este archivo (desde su propio builder); los otros
    cuatro se quedaron congelados desde que se crearon. Ahora lo escribe este build, que
    ya calcula el roster de los cinco cursos desde `Listado estudiantes (CDigital).csv`.
    """
    if not dest_dir.is_dir():
        return
    titulo = COURSES[course_key]["titulo"]
    cuerpo = ",".join(correos)
    (dest_dir / ROSTER_NAME).write_text(
        f"Correos de los estudiantes · {titulo} · grupo {etiqueta} · {len(correos)} invitados.\n"
        "\n"
        "PARA CREAR EL GRUPO DE GOOGLE (Chat o Grupos): copia la última línea ENTERA y pégala\n"
        "en «Añadir miembros». Va separada por comas y sin espacios, que es como Google la\n"
        "acepta de una sola vez.\n"
        "\n"
        "El Docente no está en la lista: es el organizador, no un invitado.\n"
        "Para los eventos de Calendar NO uses esto ni el .ics: usa el «PRINCIPAL - Crear\n"
        "encuentros con invitados.gs», que ya lleva estos mismos correos dentro.\n"
        "\n"
        f"{cuerpo}\n",
        encoding="utf-8",
    )


def _inventario(out_dir: Path, gs_name: str) -> list[str]:
    """Filas de la tabla «qué hay en esta carpeta», clasificadas por rol."""
    filas = []
    for f in sorted(out_dir.iterdir()):
        if not f.is_file():
            continue
        n = f.name
        if n == gs_name:
            rol = "**FLUJO PRINCIPAL.** El único que crea los eventos con invitados y con Meet."
        elif n == LEEME_NAME:
            rol = "Este archivo."
        elif n.startswith("RESPALDO"):
            rol = ("⚠️ **Respaldo de fechas. NO importar** salvo emergencia: Google descarta los "
                   "invitados al importar `.ics`/`.csv`.")
        elif n.startswith("Encuentros") and n.lower().endswith((".ics", ".csv")):
            rol = ("⚠️ **Respaldo de fechas sin invitados**, con el nombre antiguo. No importar; "
                   "se renombra al correr `build_pregrado_cursos.py --calendar-only`.")
        elif n.startswith("Entregas y hitos"):
            rol = ("Cierres de ACA y hitos del docente. Este **sí** se importa a Calendar: son "
                   "recordatorios tuyos, sin invitados.")
        elif n.startswith("Calendario de clases"):
            rol = "Referencia: el cronograma en tabla. No se importa: se lee."
        elif n.startswith("Correos estudiantes"):
            rol = "Roster en texto plano — de aquí sacó el `.gs` la lista de invitados."
        elif n.startswith("Listado estudiantes (CDigital)"):
            rol = "Matrícula descargada de CDigital (fuente del roster)."
        elif n.startswith("Listado estudiantes"):
            # El .ods que subió el docente se quedó en 40 estudiantes cuando el aula ya tenía
            # 50 (auditoría 2026-08-10). Decirle «fuente del roster» invitaría a fiarse de él.
            rol = ("Carga original del docente, anterior a la auditoría del aula. Se conserva como "
                   "histórico: el roster vigente es el `(CDigital)`.")
        elif n.startswith("NO USAR - Actualizar Meet") or n.startswith("Actualizar Meet"):
            # Renombrado con el prefijo «NO USAR - » el 31/08/2026: desde que cada sesión tiene su
            # propio Meet, ponerles a todas el mismo es destructivo, y el nombre del archivo es lo
            # primero que ve el docente.
            rol = ("⛔ **NO EJECUTAR.** Pone el MISMO enlace en todos los encuentros, y desde el "
                   "31/08/2026 cada sesión tiene el suyo: correrlo machacaría los enlaces que los "
                   "estudiantes ya tienen en su Calendar. Se conserva solo por si algún curso "
                   "vuelve al enlace único.")
        elif n.startswith("Correo de bienvenida"):
            rol = "Correo para enviar a los estudiantes el primer día."
        elif n in ("Informacion.txt", "Fechas.txt"):
            rol = "Datos de la oferta del grupo (portal)."
        else:
            rol = "—"
        filas.append(f"| `{n}` | {rol} |")
    return filas


def _leeme_texto(course_key: str, grupos_titulo: list[str], rosters: dict[str, list[str]],
                 total: int, out_dir: Path, gs_name: str, solo_ultima: list[str] | None) -> str:
    c = COURSES[course_key]
    ses = c["sesiones"]
    hora_ini, hora_fin = _horas(course_key)
    dia = DIAS[datetime.strptime(ses[0]["fecha"], "%d/%m/%Y").date().weekday()]
    tg3 = course_key == "tg3"
    meet = meet_url(course_key)
    meet_real = meet.startswith("https://meet.google.com/")

    if tg3:
        quienes = "los tres grupos (" + ", ".join(grupos_titulo) + ")"
        detalle = " · " + " + ".join(f"{g}: {len(rosters[g])}" for g in grupos_titulo)
    else:
        quienes = f"los {total} estudiantes del grupo {grupos_titulo[0]}"
        detalle = ""

    L: list[str] = [
        f"# Crear los eventos de Calendar — {c['titulo']}",
        "",
        f"**{'Grupos' if tg3 else 'Grupo'} {', '.join(grupos_titulo)}** · {dia} "
        f"{hora_ini}–{hora_fin} · **{len(ses)} encuentros** · "
        f"**{total} estudiantes invitados**{detalle}",
        "",
        "> **Archivo generado — no editar a mano.** Regenerar: "
        f"`python config/slides/build_calendar_encuentros.py {course_key}`",
        "",
        "## Qué vas a conseguir",
        "",
        f"Los **{len(ses)} encuentros** del periodo ({ses[0]['fecha']} → {ses[-1]['fecha']}) en tu "
        f"Google Calendar, cada uno con **{quienes}** en la sección *Invitados* y con **el mismo "
        "enlace de Google Meet** en todos. Unos cinco minutos. No hay que crear la sala a mano: "
        "la crea el propio script.",
        "",
        "## ⚠️ Lo primero: no importes el `.ics`",
        "",
        "Google Calendar **descarta la lista de invitados** al importar `.ics` y `.csv`. No es un "
        "defecto de estos archivos: es cómo Google trata esos formatos. Si importas el `.ics` de "
        f"esta carpeta te quedan los {len(ses)} eventos **con cero de los {total} estudiantes**, y "
        "encima ya no puedes usar el script sin borrarlos antes.",
        "",
        "> **Si ya creaste los encuentros y lo que buscas es meter matrícula nueva**, no repitas "
        "nada de esto: salta a "
        # Ancla con los acentos tal cual: es la que genera GitHub, y en el texto plano —que es como
        # se lee este archivo la mayoría de las veces— un %C3%AD a media frase no dice nada.
        "[Llega matrícula nueva](#llega-matrícula-nueva-y-los-encuentros-ya-están-creados). "
        "Son dos órdenes, `verificarInvitados()` y `agregarInvitados()`, y no tocan lo que ya está.",
        "",
        "Por eso el respaldo se llama `RESPALDO sin invitados - …` y el script `PRINCIPAL - …`. "
        "El respaldo está solo por si algún día necesitas las fechas en un calendario que no sea "
        "Google. **El flujo bueno es el `.gs`.**",
        "",
    ]
    if tg3:
        L += [
            "En TG3 hay una trampa extra: esto es **una sola serie para los tres grupos**. Antes "
            "convivían carpetas `_combinado_54466-54467/` y `_combinado_todos_hasta_15-11/` "
            "con versiones alternativas de los mismos encuentros; se eliminaron precisamente "
            "porque importar dos de ellas creaba los eventos por duplicado. Lo único que crea "
            "encuentros de TG3 es el `.gs` de esta carpeta.",
            "",
        ]

    L += [
        "## Qué hay en esta carpeta",
        "",
        "| Archivo | Para qué sirve |",
        "|---|---|",
        *_inventario(out_dir, gs_name),
        "",
    ]
    if tg3:
        L += [
            "El `Entregas y hitos docentes - Importar a Calendar.csv`, el roster y el correo de "
            f"bienvenida de cada grupo están en `2026/{grupos_titulo[0]}/`, "
            f"`2026/{grupos_titulo[1]}/` y `2026/{grupos_titulo[2]}/`: los cierres de ACA **no** "
            "son iguales en los tres.",
            "",
        ]

    L += [
        "## Paso a paso",
        "",
        "### 1. Abre Apps Script con la cuenta CUN",
        "",
        f"**https://script.google.com** con **{DOCENTE_CORREO}**. Si entras con otra cuenta, los "
        f"eventos se crean en el calendario equivocado. **Nuevo proyecto** → borra el "
        f"`function myFunction()` que trae de fábrica → pega **todo** el contenido de "
        f"`{gs_name}` → guarda. Ponle al proyecto un nombre reconocible "
        f"(p. ej. «Encuentros {c['titulo'].capitalize()} 2026»).",
        "",
        "### 2. Activa el servicio avanzado de Calendar (30 segundos)",
        "",
        "Es lo que le permite al script **crear la sala de Meet**. Sin esto los eventos se crean "
        "igual y con invitados, pero sin videoconferencia.",
        "",
        "1. En el panel izquierdo del editor, junto a **Servicios**, pulsa **+**.",
        "2. Busca **Google Calendar API** en la lista.",
        "3. Deja el identificador que propone (`Calendar`) y la versión **v3**.",
        "4. **Añadir**. Debe quedar «Calendar» listado bajo *Servicios*.",
        "",
        "### 3. Ejecuta `verificar()` — siempre, antes que nada",
        "",
        "Elige la función **`verificar`** en la barra superior y pulsa **Ejecutar**.",
        "",
        "La primera vez Google pide permisos: **Revisar permisos** → tu cuenta CUN → «Google no "
        "ha verificado esta aplicación» → **Configuración avanzada** → **Ir a (nombre del "
        "proyecto)** → **Permitir**. Es tu propio script; el aviso sale porque no está publicado.",
        "",
        "`verificar()` **no crea, no modifica y no borra nada**. Solo escribe en el registro "
        "(*Ver → Registro de ejecución*):",
        "",
        "- en qué calendario va a trabajar — comprueba que es el tuyo de CUN;",
        f"- las **{len(ses)} sesiones**, con fecha, título del evento y cuántos invitados lleva "
        "cada una;",
        "- si alguna **ya existe** (entonces no se duplicará);",
        "- si el servicio avanzado está activado;",
        "- **qué va a pasar con el Meet**: si reutiliza una sala existente o si va a crear una.",
        "",
        "Si algo no cuadra —calendario equivocado, invitados a cero, fechas raras— párate aquí: "
        "todavía no has tocado nada.",
        "",
        "### 4. Ejecuta `crearEncuentros()`",
        "",
        f"Crea los **{len(ses)} eventos** con sus invitados y después pone la misma sala de Meet "
        "en todos. Tarda un poco: la creación de la sala es asíncrona y el script espera a que "
        "Google devuelva el enlace.",
        "",
        "- **`SEND_INVITES = false`** (primera línea de configuración del `.gs`): los estudiantes "
        "**no** reciben correo todavía. Los eventos les aparecen en el calendario, pero sin "
        "notificación. Déjalo así mientras revisas; ponlo en `true` y vuelve a ejecutar solo "
        "cuando quieras avisarles.",
        "- **Es idempotente:** volver a ejecutarlo no duplica eventos (los reconoce por título y "
        "fecha) ni crea una segunda sala (la recuerda en las propiedades del proyecto).",
        "",
        "### 5. Lleva la URL de Meet al material",
        "",
    ]
    if meet_real:
        L += [
            f"Este curso **ya tiene sala**: {meet}. El script la reutiliza y no crea otra. "
            "Nada que hacer en este paso.",
            "",
        ]
    else:
        L += [
            "El registro te va a mostrar un recuadro así:",
            "",
            "```",
            "  +--------------------------------------------------------------",
            "  | SALA DE MEET CREADA: https://meet.google.com/xxx-xxxx-xxx",
            f"  | Es la de las {len(ses)} sesiones. Cópiala y pégala en el material:",
            f"  |   config/cursos/carga_academica_2026.json -> cursos.{course_key}.meet",
            "  +--------------------------------------------------------------",
            "```",
            "",
            "**Hazlo.** Abre `config/cursos/carga_academica_2026.json`, busca "
            f'`"{course_key}"` y pon esa URL en su campo `"meet"` (hoy está vacío). Después '
            "regenera el material:",
            "",
            "```",
            "python config/slides/build_pregrado_cursos.py --calendar-only",
            "python config/slides/build_correo_bienvenida.py",
            f"python config/slides/build_calendar_encuentros.py {course_key}",
            "```",
            "",
            "Mientras ese campo siga vacío, el **correo de bienvenida**, el **LEEME del "
            "estudiante** y el calendario del curso muestran el marcador de posición "
            "`[URL Meet — mismo enlace toda la serie · …]` en vez del enlace de verdad. Es el "
            "único paso manual que queda.",
            "",
        ]

    L += [
        "### 6. Remate a mano (lo que la API no puede hacer)",
        "",
        "- **Coanfitrión de Meet:** ábrelo en Calendar y añádelo desde la ficha del evento.",
        f"- Publica el enlace en el aula de CDigital: {cdigital_url(course_key)}",
        "",
        "## Llega matrícula nueva y los encuentros ya están creados",
        "",
        "Pasa cada semestre: alguien se matricula tarde, o el aula tenía menos estudiantes que "
        f"hoy. No hay que borrar ni rehacer los **{len(ses)} encuentros** ni tocar el Meet. Hay dos "
        "órdenes nuevas para esto:",
        "",
        "| Ejecuta | Qué hace | Escribe algo |",
        "|---|---|---|",
        "| **`verificarInvitados`** | encuentro por encuentro: a quién le falta invitación y quién "
        "está invitado sin estar en el roster | **no** |",
        "| **`agregarInvitados`** | añade solo los que faltan | sí |",
        "",
        "Nunca **quitan** a nadie, no crean eventos y no tocan la sala de Meet. Y son "
        "idempotentes: si no falta nadie, no hacen nada.",
        "",
        "### Vía normal — que entre toda la matrícula de hoy",
        "",
        "1. Descarga otra vez el listado del aula y sobrescribe "
        f"`2026/{grupos_titulo[0]}/Listado estudiantes (CDigital).csv`"
        + (" (y el de los otros dos grupos)." if tg3 else "."),
        f"2. `python config/slides/build_calendar_encuentros.py {course_key}` — el `.gs` sale con el "
        "roster nuevo dentro.",
        f"3. Pega el `{gs_name}` actualizado en el proyecto de Apps Script (reemplaza el que había).",
        "4. **`verificarInvitados`** → lee el registro → **`agregarInvitados`**.",
        "",
        "### Vía corta — un solo estudiante",
        "",
        "Si es una persona y no quieres regenerar nada, pon su correo arriba del `.gs`:",
        "",
        "```js",
        "var NUEVOS = ['nombre.apellido@cun.edu.co'];",
        "```",
        "",
        "y ejecuta **`verificarInvitados`** → **`agregarInvitados`**. Con `NUEVOS` puesto, esos son "
        "los **únicos** correos que se añaden; el roster del archivo se ignora. Déjalo en `[]` para "
        "volver a la vía normal.",
        "",
        "### Para qué sirve pasarle el id del Meet",
        "",
        "Los encuentros se localizan por el **título**. Si renombraste alguno a mano —o quieres "
        "alcanzar una **tutoría** que creaste aparte con la misma sala—, el título ya no cuadra y "
        "por ahí no se encuentran. El asidero que sí aguanta es la **sala de Meet**, porque es la "
        "misma en toda la serie:",
        "",
        "```js",
        "var MEET_ID = 'abc-defg-hij';   // o la URL completa; sale de la barra del navegador",
        "```",
        "",
        "Con eso entran también los eventos que no están en la lista de sesiones, y el registro los "
        "marca `[FUERA DE SESIONES · lo hallé por el Meet]` para que los veas **antes** de "
        "confirmar. Vacío (lo normal), el script usa la sala de este curso"
        + (f" ({meet})." if meet_real else " en cuanto exista."),
        "",
        "> Si el id que pegas **no** es el de este curso, el registro te lo grita antes de escribir "
        "nada: pegar por error el Meet de otra asignatura invitaría a este roster a los encuentros "
        "de la otra.",
        "",
        "### Dos cosas que conviene saber",
        "",
        "- **¿Les llega correo?** Manda `SEND_INVITES`, igual que al crear. En `false` el encuentro "
        "les aparece en el calendario sin notificación. Para el que se matricula tarde normalmente "
        "**sí** quieres avisarle: ponlo en `true` antes de `agregarInvitados` — pero ojo, entonces "
        "el aviso les llega **a todos** los invitados del evento, no solo al nuevo (Google no "
        "distingue).",
        "- **Las bajas no se quitan solas.** Si alguien ya no está en el roster, el registro lo "
        "lista como «invitados que ya NO están en el roster» y ahí se queda: quitar a una persona "
        "de un evento se hace a mano, abriendo el encuentro en Calendar.",
        "",
        "## Si algo sale mal",
        "",
        "| Lo que ves | Qué pasa y qué haces |",
        "|---|---|",
        "| `verificar()` dice **NO ACTIVADO** | Te saltaste el paso 2. Actívalo y repite. Los "
        "eventos se crearían igual, pero sin Meet. |",
        "| Dice «creará UNA sala nueva» y **no querías** | Ya existía sala: pégala primero en "
        f"`carga_academica_2026.json → cursos.{course_key}.meet`, regenera el `.gs` y vuelve a "
        "`verificar()`. |",
        "| «Google aceptó la petición pero todavía no devuelve el enlace» | La sala tarda en "
        "aparecer. Espera un minuto y ejecuta `crearEncuentros()` otra vez: no duplica nada. |",
        "| Invitados = **0** en `verificar()` | No se leyó el roster. Revisa "
        "`Correos estudiantes (invitados Calendar).txt` en la carpeta del grupo y regenera el "
        "`.gs`. |",
        "| Eventos duplicados | Se crearon dos veces con títulos distintos, o se importó el "
        "`.ics`. `borrarEncuentros()` limpia los del script; el resto, a mano. |",
        "| «Se ha excedido el tiempo máximo de ejecución» | Vuelve a ejecutar "
        "`crearEncuentros()`: continúa donde se quedó. |",
        "| `verificarInvitados()` dice **«No encontré NINGÚN encuentro»** | O no los has creado "
        "(`crearEncuentros()`), o los renombraste: pon la sala en `MEET_ID`. |",
        "| `agregarInvitados()` dice **CORTADO por el límite de 6 minutos** | Vuelve a ejecutarlo: "
        "sigue por donde se quedó y no invita a nadie dos veces. |",
        "| `MEET_ID = «…» no parece un Meet` | Pega la URL completa o solo el código de tres "
        "bloques (`abc-defg-hij`). |",
        "| `NUEVOS tiene N entrada(s) que no son un correo` | Coma o espacio de más al pegar la "
        "lista. Corrige y repite: no invitó a nadie. |",
        "",
        "## Cómo deshacer",
        "",
        f"- **`borrarEncuentros()`** — borra solo los eventos cuyo título coincide exactamente con "
        f"los {len(ses)} de esta serie. No toca nada más de tu calendario. Si ya habías puesto "
        "`SEND_INVITES = true`, los estudiantes reciben la cancelación.",
        "- **`olvidarSalaMeet()`** — hace que el script olvide la sala que creó, para que la "
        "siguiente ejecución genere otra. La sala vieja no se borra de Google, y los eventos ya "
        "creados siguen apuntando a ella.",
        "- **Rehacer desde cero:** `borrarEncuentros()` → `olvidarSalaMeet()` → "
        "`crearEncuentros()`.",
        "- **`agregarInvitados()` no se deshace en bloque.** Añadir invitados no tiene marcha atrás "
        "automática: se quitan a mano en el evento. Por eso `verificarInvitados()` existe y por eso "
        "se ejecuta primero.",
        "",
    ]

    if tg3 and solo_ultima:
        ult = ses[-1]
        L += [
            "## Dos cosas propias de TG3",
            "",
            f"1. **La última sesión no es para todos.** S{int(ult['n']):02d}, "
            f"{_fecha_larga(ult['fecha'])}, invita solo a **{', '.join(solo_ultima)}**: el grupo "
            f"**{TG3_CIERRE_CORTO}** cierra el 15/11 y ese día ya no tiene clase. El `.gs` lo hace "
            "solo; se ve en `verificar()`, en la línea de esa fecha.",
            f"2. **Una sola sala de Meet para los tres grupos.** Es una sola serie, no tres. No "
            "crees salas por grupo ni ejecutes el script tres veces.",
            "",
        ]

    L += [
        "## Las sesiones que se van a crear",
        "",
        "| # | Fecha | Tema | Invitados |",
        "|---|---|---|---|",
    ]
    for i, s in enumerate(ses):
        grupos_s = solo_ultima if (solo_ultima and i == len(ses) - 1) else grupos_titulo
        n_inv = len({e for g in grupos_s for e in rosters[g]})
        L.append(f"| {int(s['n']):02d} | {_fecha_larga(s['fecha'])} | {s['titulo']} | {n_inv} |")

    L += [
        "",
        "Fechas y temas salen de `config/cursos/sesiones_cun.py`; el roster, de los listados de "
        "`2026/<grupo>/`; el enlace de Meet y el aula, de "
        "`config/cursos/carga_academica_2026.json`. Si cambia cualquiera de los tres, regenera "
        f"este `.gs` con `python config/slides/build_calendar_encuentros.py {course_key}`.",
    ]
    return "\n".join(L) + "\n"


# ── orquestación por curso ───────────────────────────────────────────────────
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

    # Invitados DISTINTOS: un estudiante repetido en dos grupos de TG3 no cuenta dos veces.
    total = len({e for g in grupos_titulo for e in rosters[g]})
    gs_name = GS_NAME_TG3 if combinado else GS_NAME

    dest = out_dir / gs_name
    dest.write_text(_gs_texto(course_key, grupos_titulo, solo_ultima, rosters, total),
                    encoding="utf-8")
    # El .gs cambió de nombre (ahora dice PRINCIPAL): fuera la copia con el nombre viejo, o
    # el docente acaba con dos scripts casi idénticos sin saber cuál abrir.
    for viejo in GS_LEGACY:
        p = out_dir / viejo
        if viejo != gs_name and p.exists():
            try:
                p.unlink()
            except OSError:
                pass

    leeme = out_dir / LEEME_NAME
    leeme.write_text(
        _leeme_texto(course_key, grupos_titulo, rosters, total, out_dir, gs_name, solo_ultima),
        encoding="utf-8",
    )

    for g in grupos_titulo:
        _sync_fechas_txt(course_key, base / g)
        _escribir_roster_txt(course_key, base / g, g, rosters[g])
    if combinado:
        # TG3 va en una sola serie: además de la lista por grupo, la de los tres juntos,
        # que es la que sirve para el grupo de Google Chat de la clase.
        todos = sorted({e for g in grupos_titulo for e in rosters[g]})
        _escribir_roster_txt(course_key, out_dir, "+".join(grupos_titulo), todos)

    raiz = Path(c["folder"]).parents[1]
    estado_meet = ("Meet ya en config" if meet_url(course_key).startswith("https://")
                   else "Meet lo crea el .gs")
    print(f"OK {course_key}: {dest.relative_to(raiz)} · {len(c['sesiones'])} sesiones · "
          f"{total} invitados · {estado_meet}"
          f"{' · serie única para ' + '/'.join(grupos_titulo) if combinado else ''}")
    print(f"   runbook: {leeme.relative_to(raiz)}")
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
