/**
 * INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA — Crear encuentros CON invitados en Google Calendar.
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
 * Regenerar este .gs: python config/slides/build_calendar_encuentros.py investigacion
 */
var SEND_INVITES = false;  // true solo cuando quieras notificar a los estudiantes
var TIMEZONE = 'America/Bogota';
var MEET_URL = '[URL Meet — mismo enlace toda la serie · INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA]';
var CDIGITAL = 'https://cdigital.cun.edu.co/course/view.php?id=111070';

// Roster por grupo (20 invitados en total).
var INVITADOS = {
  '53339': [
    'andrea.castelblanco@cun.edu.co',
    'andres.sanabriav@cun.edu.co',
    'cristian.vergaraa@cun.edu.co',
    'damaris.ordones@cun.edu.co',
    'david.losada@cun.edu.co',
    'diana.guerreroa@cun.edu.co',
    'elfar.moreno@cun.edu.co',
    'hernan.berrio@cun.edu.co',
    'jasmin.albino@cun.edu.co',
    'jhonny.duarteo@cun.edu.co',
    'johan.buitragog@cun.edu.co',
    'johan.correat@cun.edu.co',
    'jorge.bustamante@cun.edu.co',
    'jorge.gambin@cun.edu.co',
    'jorge.jaramilloo@cun.edu.co',
    'jorge.trilleras@cun.edu.co',
    'jose.rojasppepenpena@cun.edu.co',
    'karen.contrerasr@cun.edu.co',
    'liberney.ardila@cun.edu.co',
    'maria.acostappo@cun.edu.co'
  ]
};

var SESIONES = [
  {
    subject: '53339 - Investigación Ciencia y Tecnología - Sesion 01',
    description: 'Sesión 01 — Presentación del curso · docente · estudiantes · ACAs',
    start: '2026-08-13T17:00:00',
    end: '2026-08-13T18:00:00',
    grupos: ['53339']
  },
  {
    subject: '53339 - Investigación Ciencia y Tecnología - Sesion 02',
    description: 'Sesión 02 — MinCiencias · 6 líneas de Ingeniería · elección de línea',
    start: '2026-08-20T17:00:00',
    end: '2026-08-20T18:00:00',
    grupos: ['53339']
  },
  {
    subject: '53339 - Investigación Ciencia y Tecnología - Sesion 03',
    description: 'Sesión 03 — Prueba parcial · 1.er avance del artículo',
    start: '2026-08-27T17:00:00',
    end: '2026-08-27T18:00:00',
    grupos: ['53339']
  },
  {
    subject: '53339 - Investigación Ciencia y Tecnología - Sesion 04',
    description: 'Sesión 04 — Identificación de problemas y pregunta de investigación',
    start: '2026-09-03T17:00:00',
    end: '2026-09-03T18:00:00',
    grupos: ['53339']
  },
  {
    subject: '53339 - Investigación Ciencia y Tecnología - Sesion 05',
    description: 'Sesión 05 — Formulación del planteamiento del problema',
    start: '2026-09-10T17:00:00',
    end: '2026-09-10T18:00:00',
    grupos: ['53339']
  },
  {
    subject: '53339 - Investigación Ciencia y Tecnología - Sesion 06',
    description: 'Sesión 06 — Bases de datos CUN · gestores · marco teórico y revisión (U8+U10–12)',
    start: '2026-09-17T17:00:00',
    end: '2026-09-17T18:00:00',
    grupos: ['53339']
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
