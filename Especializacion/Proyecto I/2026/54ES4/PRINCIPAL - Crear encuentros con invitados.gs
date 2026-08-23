/**
 * PROYECTO I — Crear los encuentros en Calendar CON invitados y CON Meet.
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
 * 6. Copia la URL de Meet que imprime -> carga_academica_2026.json -> cursos.proyecto1.meet
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
 * Regenerar este .gs: python config/slides/build_calendar_encuentros.py proyecto1
 */

// ───────────────────────────── CONFIGURACIÓN ─────────────────────────────────
var SEND_INVITES = false;  // true solo cuando quieras notificar a los estudiantes
var TIMEZONE = 'America/Bogota';
var CURSO = 'PROYECTO I';
var CURSO_KEY = 'proyecto1';
// Sala real -> se reutiliza. Marcador de posición -> el script crea UNA y te dice dónde pegarla.
var MEET_URL = 'https://meet.google.com/omk-woqk-vsj';
var CDIGITAL = 'https://cdigital.cun.edu.co/course/view.php?id=130378';
// Dónde recuerda el script la sala que creó, para no crear una segunda al reejecutar.
var PROP_MEET = 'MEET_URL_proyecto1';
// Determinista: Google ignora un createRequest con un requestId ya usado, así que ni
// borrando ScriptProperties se acaba con dos salas para la misma serie.
var REQUEST_ID = 'cun-proyecto1-2026-08-10';
var DOCENTE = 'julian_castanoe@cun.edu.co';  // organizador: nunca se añade como invitado

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

// Roster por grupo (51 invitados distintos en total).
var INVITADOS = {
  '54ES4': [
    'aide.moreno@cun.edu.co',
    'alejandro.munozd@cun.edu.co',
    'andres.abrilt@cun.edu.co',
    'andres.lopezhe@cun.edu.co',
    'angela.castilloro@cun.edu.co',
    'anternol.bedoya@cun.edu.co',
    'baldwin.foschini@cun.edu.co',
    'bayron.carranza@cun.edu.co',
    'bonny.galindosa@cun.edu.co',
    'camilo.rodriguezay@cun.edu.co',
    'carlos.nunezf@cun.edu.co',
    'carlos.palta@cun.edu.co',
    'christiam.fischer@cun.edu.co',
    'cielo.angulo@cun.edu.co',
    'clara.vieco@cun.edu.co',
    'cristhian.cortesm@cun.edu.co',
    'daimer.cardona@cun.edu.co',
    'david.paezd@cun.edu.co',
    'diana.bonillaa@cun.edu.co',
    'diego.leonz@cun.edu.co',
    'elva.tenganan@cun.edu.co',
    'fabian.rincong@cun.edu.co',
    'harold.villamilo@cun.edu.co',
    'hernan.gomezs@cun.edu.co',
    'investigacion_especializaciones@cun.edu.co',
    'jaime.cortesg@cun.edu.co',
    'jair.vargasa@cun.edu.co',
    'jhon.guerrerom@cun.edu.co',
    'jhonatan.diazc@cun.edu.co',
    'jhonny.roseroc@cun.edu.co',
    'johann.gonzalez@cun.edu.co',
    'juan.guerrerotu@cun.edu.co',
    'juan.salcedoo@cun.edu.co',
    'juan.sandovala@cun.edu.co',
    'juan.vargassi@cun.edu.co',
    'julio.rodriguezca@cun.edu.co',
    'karen.ospinal@cun.edu.co',
    'kevin.diazch@cun.edu.co',
    'leidy.henaor@cun.edu.co',
    'libardo.cabarcas@cun.edu.co',
    'luis.ospinad@cun.edu.co',
    'mayra.bernate@cun.edu.co',
    'michel.ortizr@cun.edu.co',
    'miguel.gutierrezca@cun.edu.co',
    'miguel.sierrari@cun.edu.co',
    'natalia.sepulvedar@cun.edu.co',
    'oscar.hernandezbo@cun.edu.co',
    'over.cometa@cun.edu.co',
    'santiago.bahamon@cun.edu.co',
    'sebastian.castanos@cun.edu.co',
    'william_marinch@cun.edu.co'
  ]
};

var SESIONES = [
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 01',
    description: 'Sesión 01 — Presentación del curso · docente · estudiantes · ACAs',
    start: '2026-08-10T20:00:00',
    end: '2026-08-10T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 02',
    description: 'Sesión 02 — Problema y pregunta de investigación',
    start: '2026-08-24T20:00:00',
    end: '2026-08-24T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 03',
    description: 'Sesión 03 — Objetivos, justificación, alcances y limitaciones',
    start: '2026-08-31T20:00:00',
    end: '2026-08-31T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 04',
    description: 'Sesión 04 — Retroalimentación del Quiz · Antecedentes de investigación',
    start: '2026-09-07T20:00:00',
    end: '2026-09-07T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 05',
    description: 'Sesión 05 — Marco teórico',
    start: '2026-09-14T20:00:00',
    end: '2026-09-14T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 06',
    description: 'Sesión 06 — Marco conceptual y marco contextual',
    start: '2026-09-21T20:00:00',
    end: '2026-09-21T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 07',
    description: 'Sesión 07 — Marco legal · citación APA 7',
    start: '2026-09-28T20:00:00',
    end: '2026-09-28T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 08',
    description: 'Sesión 08 — Diseño metodológico: paradigma, enfoque y alcance',
    start: '2026-10-05T20:00:00',
    end: '2026-10-05T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 09',
    description: 'Sesión 09 — Devolución de la ACA 1 · población, muestra e instrumentos propuestos',
    start: '2026-10-19T20:00:00',
    end: '2026-10-19T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 10',
    description: 'Sesión 10 — Planeación, viabilidad e integración del anteproyecto',
    start: '2026-10-26T20:00:00',
    end: '2026-10-26T22:00:00',
    grupos: ['54ES4']
  },
  {
    subject: '26ES4 - 54ES4 - Proyecto I - Sesion 11',
    description: 'Sesión 11 — Integración y evaluación · coevaluación y autoevaluación',
    start: '2026-11-09T20:00:00',
    end: '2026-11-09T22:00:00',
    grupos: ['54ES4']
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
  if (sala.id && _meetConfigurado_() && sala.id !== _meetId_(MEET_URL)) {
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
      var s = porTitulo[ev.summary] || null;
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
      var s = porTitulo[ev.getTitle()] || null;
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
