/**
 * TRABAJO DE GRADO 2 — Crear encuentros CON invitados en Google Calendar.
 *
 * Google Calendar DESCARTA los invitados al importar .ics/.csv. Este script usa
 * CalendarApp y sí añade la sección Invitados.
 * *
 * PASOS
 * 1. https://script.google.com con la cuenta CUN (julian_castanoe@cun.edu.co).
 * 2. Nuevo proyecto → pega TODO este archivo → guarda.
 * 3. Ejecuta `verificar()` (SOLO LECTURA) y revisa el registro.
 * 4. Si todo cuadra, ejecuta `crearEncuentros()`.
 * 5. Añade el coanfitrión de Meet a mano (eso no lo puede hacer la API).
 *
 * MEET: CalendarApp no adjunta videoconferencia. El enlace va en Ubicación y en la
 * descripción (clicable y visible en el correo). Para el chip nativo «Unirse con
 * Google Meet», usa después el script «Actualizar Meet en encuentros (mismo enlace).gs».
 *
 * Regenerar este .gs: python config/slides/build_calendar_encuentros.py tg2
 */
var SEND_INVITES = false;  // true solo cuando quieras notificar a los estudiantes
var TIMEZONE = 'America/Bogota';
var MEET_URL = '[URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 2]';
var CDIGITAL = 'https://cdigital.cun.edu.co/course/view.php?id=129268';

// Roster por grupo (50 invitados en total).
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
    subject: '54448 - Trabajo de Grado 2 - Sesion 01',
    description: 'Sesión 01 — Presentación del curso · docente · estudiantes · ACAs',
    start: '2026-08-10T17:00:00',
    end: '2026-08-10T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 02',
    description: 'Sesión 02 — Pregunta, objetivos y título provisional',
    start: '2026-08-24T17:00:00',
    end: '2026-08-24T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 03',
    description: 'Sesión 03 — Estructura del documento / artículo de avance',
    start: '2026-08-31T17:00:00',
    end: '2026-08-31T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 04',
    description: 'Sesión 04 — Antecedentes y referentes (Fase I)',
    start: '2026-09-07T17:00:00',
    end: '2026-09-07T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 05',
    description: 'Sesión 05 — Marco teórico — avance',
    start: '2026-09-14T17:00:00',
    end: '2026-09-14T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 06',
    description: 'Sesión 06 — Marco conceptual y contextual',
    start: '2026-09-21T17:00:00',
    end: '2026-09-21T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 07',
    description: 'Sesión 07 — Diseño metodológico (propuesto)',
    start: '2026-09-28T17:00:00',
    end: '2026-09-28T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 08',
    description: 'Sesión 08 — Instrumentos y plan de análisis (propuestos)',
    start: '2026-10-05T17:00:00',
    end: '2026-10-05T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 09',
    description: 'Sesión 09 — Integración del avance · correcciones',
    start: '2026-10-19T17:00:00',
    end: '2026-10-19T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 10',
    description: 'Sesión 10 — Socialización de avances',
    start: '2026-10-26T17:00:00',
    end: '2026-10-26T18:00:00',
    grupos: ['54448']
  },
  {
    subject: '54448 - Trabajo de Grado 2 - Sesion 11',
    description: 'Sesión 11 — Cierre del avance · preparación para TG3',
    start: '2026-11-09T17:00:00',
    end: '2026-11-09T18:00:00',
    grupos: ['54448']
  }
];

function crearEncuentros() {
  var cal = CalendarApp.getDefaultCalendar();
  var creados = 0, omitidos = 0;
  SESIONES.forEach(function (s) {
    var ini = _fecha(s.start), fin = _fecha(s.end);
    var ya = cal.getEvents(ini, fin, { search: s.subject }).some(function (ev) {
      return ev.getTitle() === s.subject;
    });
    if (ya) { omitidos++; return; }
    cal.createEvent(s.subject, ini, fin, {
      description: s.description + '\nMeet: ' + MEET_URL + '\nCDigital: ' + CDIGITAL,
      location: MEET_URL,
      guests: _invitados(s.grupos).join(','),
      sendInvites: SEND_INVITES
    });
    creados++;
  });
  Logger.log('Listo. Creados=' + creados + ' omitidos(ya existían)=' + omitidos +
             ' sendInvites=' + SEND_INVITES);
}

/** SOLO LECTURA: qué haría el script, sin crear nada. */
function verificar() {
  Logger.log('Sesiones: ' + SESIONES.length + ' · Meet: ' + MEET_URL);
  SESIONES.forEach(function (s) {
    var n = _invitados(s.grupos).length;
    Logger.log(s.start.substring(0, 10) + '  ' + s.subject + '  invitados=' + n +
               ' [' + s.grupos.join(', ') + ']');
  });
  Logger.log('Si esto cuadra, ejecuta crearEncuentros().');
}

/** Borra solo los eventos creados por este script. */
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
  Logger.log('Eliminados=' + n);
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

function _fecha(iso) {
  return Utilities.parseDate(iso.replace('T', ' '), TIMEZONE, 'yyyy-MM-dd HH:mm:ss');
}
