/**
 * TRABAJO DE GRADO 3 — Crear encuentros CON invitados en Google Calendar.
 *
 * Google Calendar DESCARTA los invitados al importar .ics/.csv. Este script usa
 * CalendarApp y sí añade la sección Invitados.
 * *
 * TG3 — UNA SOLA SERIE para los tres grupos: comparten horario y **un solo enlace de
 * Meet**. A la ÚLTIMA sesión no se invita a 54450 (su curso cierra antes).
 *
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
 * Regenerar este .gs: python config/slides/build_calendar_encuentros.py tg3
 */
var SEND_INVITES = false;  // true solo cuando quieras notificar a los estudiantes
var TIMEZONE = 'America/Bogota';
var MEET_URL = '[URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 3]';
var CDIGITAL = 'https://cdigital.cun.edu.co/course/view.php?id=112321';

// Roster por grupo (112 invitados en total).
var INVITADOS = {
  '54450': [
    'angie.calderonrru@cun.edu.co',
    'carlos.velezf@cun.edu.co',
    'cristian.castroddu@cun.edu.co',
    'daniel.henaou@cun.edu.co',
    'jenny.bacca@cun.edu.co',
    'jesus.gonzalezrro@cun.edu.co',
    'joseph.arias@cun.edu.co',
    'juan.osorno@cun.edu.co',
    'juan.pedrazabba@cun.edu.co',
    'manuel.vargasb@cun.edu.co',
    'sebastian.cadenas@cun.edu.co',
    'sebastian.orjuelag@cun.edu.co',
    'wilson.sanchezy@cun.edu.co'
  ],
  '54466': [
    'alicia.medina@cun.edu.co',
    'anderson.rativa@cun.edu.co',
    'anderson.sanchezg@cun.edu.co',
    'andres.carmonao@cun.edu.co',
    'angel.fonseca@cun.edu.co',
    'arley.zea@cun.edu.co',
    'brayan.polo@cun.edu.co',
    'brayan.rivasb@cun.edu.co',
    'cristian.cardenasgon@cun.edu.co',
    'cristian.rinconv@cun.edu.co',
    'cristian.sierram@cun.edu.co',
    'daniela.mendezg@cun.edu.co',
    'edelsy.carreno@cun.edu.co',
    'fabio.salamanca@cun.edu.co',
    'gioseph.escobar@cun.edu.co',
    'harold.hurtadoc@cun.edu.co',
    'ivan.rubiano@cun.edu.co',
    'jaime.valle@cun.edu.co',
    'jazmin.bejarano@cun.edu.co',
    'jhon.alexanderv@cun.edu.co',
    'johan.munozd@cun.edu.co',
    'jose.calchon@cun.edu.co',
    'jose.frailec@cun.edu.co',
    'juan.claros@cun.edu.co',
    'juanm.gomez@cun.edu.co',
    'julian.rojast@cun.edu.co',
    'kevin.trullo@cun.edu.co',
    'kevin.villart@cun.edu.co',
    'kevin_sanchez@cun.edu.co',
    'laura.beltrant@cun.edu.co',
    'leidy.mendezgal@cun.edu.co',
    'lina.angarita@cun.edu.co',
    'luis.avilagon@cun.edu.co',
    'luis.ospinocab@cun.edu.co',
    'luisa.villacorte@cun.edu.co',
    'luz.bustosm@cun.edu.co',
    'maria.torresvar@cun.edu.co',
    'maria.urream@cun.edu.co',
    'mariana.correag@cun.edu.co',
    'omar.cardenasa@cun.edu.co',
    'oscar.diazbed@cun.edu.co',
    'ricardo.alvarezm@cun.edu.co',
    'ricardo.capera@cun.edu.co',
    'ricardo.montoya@cun.edu.co',
    'samy.arias@cun.edu.co',
    'victor.badillo@cun.edu.co',
    'yerson.leguizamon@cun.edu.co',
    'yon.villa@cun.edu.co',
    'yuri.artunduaga@cun.edu.co'
  ],
  '54467': [
    'alejandro.munozl@cun.edu.co',
    'andres.cardenasd@cun.edu.co',
    'andres.rodriguezgon@cun.edu.co',
    'anyi.gomezv@cun.edu.co',
    'arnold.roncanciop@cun.edu.co',
    'brayan.merchanv@cun.edu.co',
    'brayan.pianda@cun.edu.co',
    'carlos.marquezs@cun.edu.co',
    'cristiam.lopezb@cun.edu.co',
    'cristian.apontel@cun.edu.co',
    'cristian.perillaa@cun.edu.co',
    'cristian.quinteroa@cun.edu.co',
    'daniel.ramirezf@cun.edu.co',
    'daniel.vidales@cun.edu.co',
    'derly.delgadillo@cun.edu.co',
    'diego.reyescue@cun.edu.co',
    'diego.rojasc@cun.edu.co',
    'eimi.salazar@cun.edu.co',
    'enrique.galeano@cun.edu.co',
    'freddy.escobard@cun.edu.co',
    'jeferson.sanchezf@cun.edu.co',
    'jefferson.gonzalezy@cun.edu.co',
    'jency.avila@cun.edu.co',
    'jesus.sanchezd@cun.edu.co',
    'jhon.lozano@cun.edu.co',
    'jhonathan.echeverri@cun.edu.co',
    'johanna.garay@cun.edu.co',
    'jorge.bobadilla@cun.edu.co',
    'jose.carmonam@cun.edu.co',
    'jose.sarmientoper@cun.edu.co',
    'juan.gamezd@cun.edu.co',
    'juan.garavitos@cun.edu.co',
    'juan.higuita@cun.edu.co',
    'juan.morenoccocor@cun.edu.co',
    'juan.rivasmar@cun.edu.co',
    'julian.aguirree@cun.edu.co',
    'karina.arjona@cun.edu.co',
    'laura.bernalrrorom@cun.edu.co',
    'liz.ortiz@cun.edu.co',
    'lubin.reyes@cun.edu.co',
    'luis.cabrerarod@cun.edu.co',
    'marisol.agudelo@cun.edu.co',
    'monica.lozanos@cun.edu.co',
    'nadyesda.santamaria@cun.edu.co',
    'neider.berrio@cun.edu.co',
    'santiago.noscue@cun.edu.co',
    'santiago.urregor@cun.edu.co',
    'sergio.albarracin@cun.edu.co',
    'wilfrido.corbacho@cun.edu.co',
    'wilson.calderon@cun.edu.co'
  ]
};

var SESIONES = [
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 01',
    description: 'Sesión 01 — Presentación del curso · docente · estudiantes · ACAs',
    start: '2026-08-11T17:00:00',
    end: '2026-08-11T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 02',
    description: 'Sesión 02 — Formulación de pregunta, objetivos y título',
    start: '2026-08-18T17:00:00',
    end: '2026-08-18T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 03',
    description: 'Sesión 03 — Estructura del artículo · taller de introducción',
    start: '2026-08-25T17:00:00',
    end: '2026-08-25T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 04',
    description: 'Sesión 04 — Fase I de referentes de investigación',
    start: '2026-09-01T17:00:00',
    end: '2026-09-01T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 05',
    description: 'Sesión 05 — Diseño de instrumento · desarrollo metodológico',
    start: '2026-09-08T17:00:00',
    end: '2026-09-08T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 06',
    description: 'Sesión 06 — Comunidades de práctica y co-creación',
    start: '2026-09-15T17:00:00',
    end: '2026-09-15T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 07',
    description: 'Sesión 07 — Experiencia creativa · análisis de datos',
    start: '2026-09-22T17:00:00',
    end: '2026-09-22T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 08',
    description: 'Sesión 08 — Fase III de referentes · cierre del marco teórico',
    start: '2026-09-29T17:00:00',
    end: '2026-09-29T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 09',
    description: 'Sesión 09 — Resultados, discusión y relación con referentes',
    start: '2026-10-06T17:00:00',
    end: '2026-10-06T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 10',
    description: 'Sesión 10 — Resumen, palabras clave UNESCO, conclusiones y referencias',
    start: '2026-10-13T17:00:00',
    end: '2026-10-13T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 11',
    description: 'Sesión 11 — Póster · evidencias · verificación antiplagio',
    start: '2026-10-20T17:00:00',
    end: '2026-10-20T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 12',
    description: 'Sesión 12 — Sustentación ante jurados',
    start: '2026-10-27T17:00:00',
    end: '2026-10-27T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 13',
    description: 'Sesión 13 — Entregables para repositorio institucional',
    start: '2026-11-03T17:00:00',
    end: '2026-11-03T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54450/54466/54467 - Trabajo de Grado 3 - Sesion 14',
    description: 'Sesión 14 — Ajustes finales · seguimiento post-sustentación',
    start: '2026-11-10T17:00:00',
    end: '2026-11-10T18:00:00',
    grupos: ['54450', '54466', '54467']
  },
  {
    subject: '54466/54467 - Trabajo de Grado 3 - Sesion 15',
    description: 'Sesión 15 — Cierre administrativo · recepción (hasta 22 nov)',
    start: '2026-11-17T17:00:00',
    end: '2026-11-17T18:00:00',
    grupos: ['54466', '54467']
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
