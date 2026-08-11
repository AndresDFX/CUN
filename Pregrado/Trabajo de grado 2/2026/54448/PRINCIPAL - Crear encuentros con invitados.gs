/**
 * TRABAJO DE GRADO 2 — Crear los encuentros en Calendar CON invitados y CON Meet.
 *
 * Google Calendar DESCARTA los invitados al importar .ics/.csv. Este script usa
 * CalendarApp y sí crea la sección Invitados. Los .ics/.csv que están al lado (los que
 * empiezan por «RESPALDO») son solo un respaldo de fechas: NO los importes salvo que
 * renuncies a los invitados.
 *
 * MEET — el script se encarga solo. Crea UNA sala en el primer encuentro y pone ESE MISMO
 * enlace en todos los demás (chip nativo «Unirse con Google Meet»). Si el material ya trae
 * sala, la reutiliza y no crea ninguna otra. Reejecutarlo no duplica ni eventos ni salas.
 * Necesita el servicio avanzado de Calendar; si no está, crea los eventos igual (con
 * invitados) y avisa cómo activarlo.
 *
 * PASOS  (detalle completo en «LEEME - Crear los eventos de Calendar.md», misma carpeta)
 * 1. https://script.google.com con la cuenta CUN (julian_castanoe@cun.edu.co).
 * 2. Nuevo proyecto -> pega TODO este archivo -> guarda.
 * 3. Editor -> Servicios (+) -> «Google Calendar API» -> Añadir.
 * 4. Ejecuta `verificar()` (SOLO LECTURA) y lee el registro.
 * 5. Si cuadra, ejecuta `crearEncuentros()`.
 * 6. Copia la URL de Meet que imprime -> carga_academica_2026.json -> cursos.tg2.meet
 * 7. Añade el coanfitrión de Meet a mano (eso no lo puede hacer la API).
 *
 * Deshacer: `borrarEncuentros()` (eventos) · `olvidarSalaMeet()` (sala guardada).
 *
 * Regenerar este .gs: python config/slides/build_calendar_encuentros.py tg2
 */

// ───────────────────────────── CONFIGURACIÓN ─────────────────────────────────
var SEND_INVITES = false;  // true solo cuando quieras notificar a los estudiantes
var TIMEZONE = 'America/Bogota';
var CURSO = 'TRABAJO DE GRADO 2';
var CURSO_KEY = 'tg2';
// Sala real -> se reutiliza. Marcador de posición -> el script crea UNA y te dice dónde pegarla.
var MEET_URL = '[URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 2]';
var CDIGITAL = 'https://cdigital.cun.edu.co/course/view.php?id=129268';
// Dónde recuerda el script la sala que creó, para no crear una segunda al reejecutar.
var PROP_MEET = 'MEET_URL_tg2';
// Determinista: Google ignora un createRequest con un requestId ya usado, así que ni
// borrando ScriptProperties se acaba con dos salas para la misma serie.
var REQUEST_ID = 'cun-tg2-2026-08-14';

// Roster por grupo (50 invitados distintos en total).
var INVITADOS = {
  '54448': [
    'andres.gonzalezppa@cun.edu.co',
    'andres.pulidol@cun.edu.co',
    'anggie.quintana@cun.edu.co',
    'brayan.marinb@cun.edu.co',
    'brayan.polania@cun.edu.co',
    'carol.huertass@cun.edu.co',
    'christian.cruzc@cun.edu.co',
    'daimer.ospina@cun.edu.co',
    'diego.pabong@cun.edu.co',
    'diego.ramirezm@cun.edu.co',
    'eduin.rodriguez@cun.edu.co',
    'edwin.devia@cun.edu.co',
    'elkin.benavides@cun.edu.co',
    'erika.hernandezt@cun.edu.co',
    'farid.martinezh@cun.edu.co',
    'gabriel.velandia@cun.edu.co',
    'geiver.ochoa@cun.edu.co',
    'hermes.franco@cun.edu.co',
    'huber.puentes@cun.edu.co',
    'jaider.reyes@cun.edu.co',
    'javier.martinezgu@cun.edu.co',
    'jean.arizac@cun.edu.co',
    'jesus.campo@cun.edu.co',
    'jesus.ortizc@cun.edu.co',
    'jhohan.yusunguaira@cun.edu.co',
    'jhossel.galan@cun.edu.co',
    'jose.carlosama@cun.edu.co',
    'juan.esteban@cun.edu.co',
    'juan.pardoddi@cun.edu.co',
    'julian.novoab@cun.edu.co',
    'karol.hernandezddi@cun.edu.co',
    'kessica.montealegre@cun.edu.co',
    'kevin.campoa@cun.edu.co',
    'lug.rodriguez@cun.edu.co',
    'luis.lopeza@cun.edu.co',
    'luis.rozos@cun.edu.co',
    'luisa.castanedav@cun.edu.co',
    'luisa.lopezg@cun.edu.co',
    'mario.menjura@cun.edu.co',
    'mateo.obregozo@cun.edu.co',
    'maycol.valbuena@cun.edu.co',
    'michael.godoy@cun.edu.co',
    'nelson.sanchezcca@cun.edu.co',
    'ricardo.arevalo@cun.edu.co',
    'robinson.coca@cun.edu.co',
    'rolando.villamil@cun.edu.co',
    'sebastian.bernals@cun.edu.co',
    'thomas.guerrero@cun.edu.co',
    'yeiner.navarro@cun.edu.co',
    'yessica.carrascal@cun.edu.co'
  ]
};

var SESIONES = [
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 01',
    description: 'Sesión 01 — Presentación del curso · docente · estudiantes · ACAs',
    start: '2026-08-14T17:00:00',
    end: '2026-08-14T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 02',
    description: 'Sesión 02 — Pregunta, objetivos y título provisional',
    start: '2026-08-24T17:00:00',
    end: '2026-08-24T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 03',
    description: 'Sesión 03 — Estructura del documento / artículo de avance',
    start: '2026-08-31T17:00:00',
    end: '2026-08-31T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 04',
    description: 'Sesión 04 — Antecedentes y referentes (Fase I)',
    start: '2026-09-07T17:00:00',
    end: '2026-09-07T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 05',
    description: 'Sesión 05 — Marco teórico — avance',
    start: '2026-09-14T17:00:00',
    end: '2026-09-14T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 06',
    description: 'Sesión 06 — Marco conceptual y contextual',
    start: '2026-09-21T17:00:00',
    end: '2026-09-21T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 07',
    description: 'Sesión 07 — Diseño metodológico (propuesto)',
    start: '2026-09-28T17:00:00',
    end: '2026-09-28T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 08',
    description: 'Sesión 08 — Instrumentos y plan de análisis (propuestos)',
    start: '2026-10-05T17:00:00',
    end: '2026-10-05T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 09',
    description: 'Sesión 09 — Integración del avance · correcciones',
    start: '2026-10-19T17:00:00',
    end: '2026-10-19T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 10',
    description: 'Sesión 10 — Socialización de avances',
    start: '2026-10-26T17:00:00',
    end: '2026-10-26T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '26V04 - 54448 - Trabajo de Grado 2 - Sesion 11',
    description: 'Sesión 11 — Cierre del avance · preparación para TG3',
    start: '2026-11-09T17:00:00',
    end: '2026-11-09T18:00:00',
    grupos: ['54448']
  }
];

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

  // ── Meet: UNA sala para toda la serie ──────────────────────────────────────
  var url = _salaDeLaSerie_(cal, eventos[0]);
  if (!url) {
    Logger.log('Los encuentros quedaron creados, pero SIN enlace de Meet.');
    Logger.log('Activa el servicio avanzado («Google Calendar API») y vuelve a ejecutar');
    Logger.log('crearEncuentros(): no duplica nada, solo añade la sala.');
    return;
  }
  var nativos = 0, soloEnlace = 0;
  eventos.forEach(function (ev) { if (_aplicarMeet_(ev, url)) nativos++; else soloEnlace++; });
  Logger.log('Meet ' + url + ' -> chip nativo en ' + nativos + ' · solo enlace en ' + soloEnlace +
             (_apiCalendar_() ? '' : '  (activa «Google Calendar API» para el chip)'));
  Logger.log(nativos
    ? 'Listo. Abre un evento en Calendar: debe tener Invitados y «Unirse con Google Meet».'
    : 'Listo. Abre un evento: tiene Invitados y el enlace en Ubicación, pero sin chip nativo.');
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
function _buscarEvento_(cal, s) {
  var hallados = cal.getEvents(_fecha(s.start), _fecha(s.end), { search: s.subject })
    .filter(function (ev) { return ev.getTitle() === s.subject; });
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
function _crearSala_(evento) {
  var id = _idApi_(evento);
  try {
    var res = Calendar.Events.patch({
      conferenceData: {
        createRequest: {
          // Determinista a propósito: si se repite el requestId, Google NO crea otra sala.
          requestId: REQUEST_ID,
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
      evento.setDescription((d ? d + '\n' : '') + 'Meet (mismo enlace toda la serie): ' + url);
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
