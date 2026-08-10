/**
 * CREATIVIDAD Y PENSAMIENTO INNOVADOR — Crear encuentros CON invitados en Google Calendar.
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
 * Regenerar este .gs: python config/slides/build_calendar_encuentros.py creatividad
 */
var SEND_INVITES = false;  // true solo cuando quieras notificar a los estudiantes
var TIMEZONE = 'America/Bogota';
var MEET_URL = '[URL Meet — mismo enlace toda la serie · CREATIVIDAD Y PENSAMIENTO INNOVADOR]';
var CDIGITAL = 'https://cdigital.cun.edu.co/course/view.php?id=115463';

// Roster por grupo (50 invitados en total).
var INVITADOS = {
  '54408': [
    'alessandra.cendales@cun.edu.co',
    'alessandra.garzon@cun.edu.co',
    'andres.cortesber@cun.edu.co',
    'andres.mirandam@cun.edu.co',
    'angie.sanchezggogon@cun.edu.co',
    'aslhey.roblesc@cun.edu.co',
    'brandon.zarate@cun.edu.co',
    'cesar.churta@cun.edu.co',
    'cristian.losadan@cun.edu.co',
    'david.chingate@cun.edu.co',
    'dayana.cifuentes@cun.edu.co',
    'diego.quirogag@cun.edu.co',
    'dulis.duran@cun.edu.co',
    'edisson.casaneda@cun.edu.co',
    'erika.villada@cun.edu.co',
    'esteify.suarez@cun.edu.co',
    'francy.ostos@cun.edu.co',
    'jair.espana@cun.edu.co',
    'jinneth.ortizp@cun.edu.co',
    'johan.ramirezp@cun.edu.co',
    'juan.garavitog@cun.edu.co',
    'juan.jarabac@cun.edu.co',
    'juan.jimenezc@cun.edu.co',
    'juan.martinezaau@cun.edu.co',
    'juan.martinezffi@cun.edu.co',
    'juan.moralesdde@cun.edu.co',
    'juan.vargass@cun.edu.co',
    'juan.vivasg@cun.edu.co',
    'julieth.osoriom@cun.edu.co',
    'karen.bernale@cun.edu.co',
    'karen.prietom@cun.edu.co',
    'katherine.quitina@cun.edu.co',
    'kimberly.orozco@cun.edu.co',
    'laura.ballenh@cun.edu.co',
    'laura.yayad@cun.edu.co',
    'leidy.usma@cun.edu.co',
    'lior.rodriguez@cun.edu.co',
    'maria.barriosy@cun.edu.co',
    'maria.toroo@cun.edu.co',
    'miguel.palacios@cun.edu.co',
    'miguel.torrentes@cun.edu.co',
    'mike.marichal@cun.edu.co',
    'omar.espinel@cun.edu.co',
    'omar.popayan@cun.edu.co',
    'paula.rodriguezbel@cun.edu.co',
    'raul.diaz@cun.edu.co',
    'tomas.ballesteros@cun.edu.co',
    'viviana.ortizal@cun.edu.co',
    'yeimy.aguilara@cun.edu.co',
    'yesica.manrique@cun.edu.co'
  ]
};

var SESIONES = [
  {
    subject: '54408 - Creatividad y Pensamiento Innovador - Sesion 01',
    description: 'Sesión 01 — Presentación del curso · docente · estudiantes · ACAs',
    start: '2026-08-12T17:00:00',
    end: '2026-08-12T18:00:00',
    grupos: ['54408']
  },
  {
    subject: '54408 - Creatividad y Pensamiento Innovador - Sesion 02',
    description: 'Sesión 02 — Creatividad/innovación en I+D · Design Thinking y técnicas',
    start: '2026-08-19T17:00:00',
    end: '2026-08-19T18:00:00',
    grupos: ['54408']
  },
  {
    subject: '54408 - Creatividad y Pensamiento Innovador - Sesion 03',
    description: 'Sesión 03 — Gestión de la innovación (Manual de Oslo / OCDE)',
    start: '2026-08-26T17:00:00',
    end: '2026-08-26T18:00:00',
    grupos: ['54408']
  },
  {
    subject: '54408 - Creatividad y Pensamiento Innovador - Sesion 04',
    description: 'Sesión 04 — Tipos de innovación',
    start: '2026-09-02T17:00:00',
    end: '2026-09-02T18:00:00',
    grupos: ['54408']
  },
  {
    subject: '54408 - Creatividad y Pensamiento Innovador - Sesion 05',
    description: 'Sesión 05 — Análisis de negocios · validación de la propuesta',
    start: '2026-09-09T17:00:00',
    end: '2026-09-09T18:00:00',
    grupos: ['54408']
  },
  {
    subject: '54408 - Creatividad y Pensamiento Innovador - Sesion 06',
    description: 'Sesión 06 — Vigilancia tecnológica',
    start: '2026-09-16T17:00:00',
    end: '2026-09-16T18:00:00',
    grupos: ['54408']
  },
  {
    subject: '54408 - Creatividad y Pensamiento Innovador - Sesion 07',
    description: 'Sesión 07 — Innovación local–internacional · entidades de apoyo',
    start: '2026-09-23T17:00:00',
    end: '2026-09-23T18:00:00',
    grupos: ['54408']
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
