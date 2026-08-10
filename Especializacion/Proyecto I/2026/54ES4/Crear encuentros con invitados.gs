/**
 * Proyecto I · 54ES4 — Crear encuentros CON invitados en Google Calendar.
 *
 * Google Calendar al IMPORTAR .ics/.csv DESCARTA los invitados (ATTENDEE/Guests).
 * Este script usa CalendarApp y SÍ añade la sección Invitados.
 *
 * Pasos:
 * 1. Abre https://script.google.com con tu cuenta CUN (julian_castanoe@cun.edu.co).
 * 2. Nuevo proyecto → pega TODO este archivo → guarda.
 * 3. Revisa SEND_INVITES (false = crea sin notificar; true = envía correo).
 * 4. Ejecuta createEncuentrosP1() → autoriza Calendar cuando lo pida.
 * 5. En Calendar: abre un evento → debe verse Invitados (roster + coanfitrión).
 * 6. Asigna el coanfitrión de Meet a mano (eso NO lo puede hacer la API).
 *
 * SOBRE EL ENLACE DE MEET
 * CalendarApp NO adjunta videoconferencia: si se añade Meet evento por evento desde la
 * interfaz, Google crea un enlace DISTINTO en cada uno. Por eso este script escribe el
 * MISMO enlace de la serie en Location y en la descripción de los 11 encuentros.
 * Para además tener el chip nativo «Unirse con Google Meet», ejecuta después
 * `Actualizar Meet en encuentros (mismo enlace).gs` (usa el servicio avanzado de Calendar).
 *
 * Regenerar este .gs: python config/slides/build_calendar_proyecto1_54es4.py
 */
var SEND_INVITES = false; // true solo cuando quieras notificar a todos
var TIMEZONE = 'America/Bogota';
var LOCATION = "https://meet.google.com/omk-woqk-vsj"; // enlace único de Meet para toda la serie

var GUESTS = [
  "aide.moreno@cun.edu.co",
  "alejandro.munozd@cun.edu.co",
  "andres.abrilt@cun.edu.co",
  "andres.lopezhe@cun.edu.co",
  "angela.castilloro@cun.edu.co",
  "anternol.bedoya@cun.edu.co",
  "baldwin.foschini@cun.edu.co",
  "bayron.carranza@cun.edu.co",
  "bonny.galindosa@cun.edu.co",
  "camilo.rodriguezay@cun.edu.co",
  "carlos.nunezf@cun.edu.co",
  "carlos.palta@cun.edu.co",
  "christiam.fischer@cun.edu.co",
  "cielo.angulo@cun.edu.co",
  "clara.vieco@cun.edu.co",
  "cristhian.cortesm@cun.edu.co",
  "daimer.cardona@cun.edu.co",
  "david.paezd@cun.edu.co",
  "diana.bonillaa@cun.edu.co",
  "diego.leonz@cun.edu.co",
  "elva.tenganan@cun.edu.co",
  "fabian.rincong@cun.edu.co",
  "harold.villamilo@cun.edu.co",
  "hernan.gomezs@cun.edu.co",
  "investigacion_especializaciones@cun.edu.co",
  "jaime.cortesg@cun.edu.co",
  "jair.vargasa@cun.edu.co",
  "jhon.guerrerom@cun.edu.co",
  "jhonatan.diazc@cun.edu.co",
  "jhonny.roseroc@cun.edu.co",
  "johann.gonzalez@cun.edu.co",
  "juan.guerrerotu@cun.edu.co",
  "juan.salcedoo@cun.edu.co",
  "juan.sandovala@cun.edu.co",
  "juan.vargassi@cun.edu.co",
  "julian_castanoe@cun.edu.co",
  "julio.rodriguezca@cun.edu.co",
  "karen.ospinal@cun.edu.co",
  "kevin.diazch@cun.edu.co",
  "leidy.henaor@cun.edu.co",
  "libardo.cabarcas@cun.edu.co",
  "luis.ospinad@cun.edu.co",
  "mayra.bernate@cun.edu.co",
  "michel.ortizr@cun.edu.co",
  "miguel.gutierrezca@cun.edu.co",
  "miguel.sierrari@cun.edu.co",
  "natalia.sepulvedar@cun.edu.co",
  "oscar.hernandezbo@cun.edu.co",
  "over.cometa@cun.edu.co",
  "santiago.bahamon@cun.edu.co",
  "sebastian.castanos@cun.edu.co",
  "william_marinch@cun.edu.co"
];

var SESSIONS = [
  {
    subject: "54ES4 - Proyecto I - Sesion 01",
    description: "Sesión 01 — Presentación del curso · docente · estudiantes · ACAs\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-08-10T20:00:00",
    end: "2026-08-10T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 02",
    description: "Sesión 02 — Problema y pregunta de investigación\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-08-24T20:00:00",
    end: "2026-08-24T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 03",
    description: "Sesión 03 — Objetivos, justificación, alcances y limitaciones\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-08-31T20:00:00",
    end: "2026-08-31T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 04",
    description: "Sesión 04 — Retroalimentación ACA1 · Antecedentes de investigación\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-09-07T20:00:00",
    end: "2026-09-07T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 05",
    description: "Sesión 05 — Marco teórico\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-09-14T20:00:00",
    end: "2026-09-14T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 06",
    description: "Sesión 06 — Marco conceptual y marco contextual\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-09-21T20:00:00",
    end: "2026-09-21T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 07",
    description: "Sesión 07 — Marco legal · citación APA 7\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-09-28T20:00:00",
    end: "2026-09-28T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 08",
    description: "Sesión 08 — Diseño metodológico: paradigma, enfoque y alcance\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-10-05T20:00:00",
    end: "2026-10-05T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 09",
    description: "Sesión 09 — Población/muestra, técnicas e instrumentos (propuestos)\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-10-19T20:00:00",
    end: "2026-10-19T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 10",
    description: "Sesión 10 — Planeación, viabilidad e integración del anteproyecto\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-10-26T20:00:00",
    end: "2026-10-26T22:00:00"
  },
  {
    subject: "54ES4 - Proyecto I - Sesion 11",
    description: "Sesión 11 — Integración y evaluación · coevaluación y autoevaluación\nForm tutorías: https://forms.gle/oZ8xCYiUo3KEWr1d9\nCoanfitrión: investigacion_especializaciones@cun.edu.co",
    start: "2026-11-09T20:00:00",
    end: "2026-11-09T22:00:00"
  }
];

function createEncuentrosP1() {
  var cal = CalendarApp.getDefaultCalendar();
  var guestsCsv = GUESTS.join(',');
  var created = 0;
  var skipped = 0;

  SESSIONS.forEach(function (s) {
    var start = _parseLocal(s.start);
    var end = _parseLocal(s.end);
    var existing = cal.getEvents(start, end, { search: s.subject });
    var already = existing.some(function (ev) {
      return ev.getTitle() === s.subject;
    });
    if (already) {
      skipped++;
      return;
    }
    var options = {
      description: s.description,
      location: LOCATION,
      guests: guestsCsv,
      sendInvites: SEND_INVITES
    };
    cal.createEvent(s.subject, start, end, options);
    created++;
  });

  Logger.log(
    'Listo. Creados=' + created + ' omitidos(ya existían)=' + skipped +
    ' invitados/evento=' + GUESTS.length + ' sendInvites=' + SEND_INVITES
  );
}

/** Borra solo eventos cuyo título empieza por «54ES4 - Proyecto I - Sesion». */
function deleteEncuentrosP1Generados() {
  var cal = CalendarApp.getDefaultCalendar();
  var from = _parseLocal(SESSIONS[0].start);
  var to = _parseLocal(SESSIONS[SESSIONS.length - 1].end);
  to = new Date(to.getTime() + 60 * 60 * 1000);
  var events = cal.getEvents(from, to);
  var n = 0;
  events.forEach(function (ev) {
    var t = ev.getTitle() || '';
    if (t.indexOf('54ES4 - Proyecto I - Sesion') === 0) {
      ev.deleteEvent();
      n++;
    }
  });
  Logger.log('Eliminados=' + n);
}

function _parseLocal(isoLocal) {
  // isoLocal: YYYY-MM-DDTHH:MM:SS → America/Bogota
  return Utilities.parseDate(
    isoLocal.replace('T', ' '),
    TIMEZONE,
    'yyyy-MM-dd HH:mm:ss'
  );
}
