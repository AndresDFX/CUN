/**
 * Proyecto I · 54ES4 — Crear encuentros CON invitados leyendo el CSV desde Sheets.
 *
 * Para quien quiera seguir trabajando "con el CSV": el archivo
 * «B - Oficial + columna Guests.csv» se sube a Google Sheets y este script
 * recorre las filas y crea los eventos añadiendo la columna Guests como
 * invitados reales (la importación nativa de Calendar la ignora).
 *
 * Pasos:
 * 1. drive.google.com → Nuevo → Subir «B - Oficial + columna Guests.csv».
 * 2. Clic derecho en el archivo → Abrir con → Hojas de cálculo de Google.
 * 3. Extensiones → Apps Script → pega TODO este archivo → Guardar.
 * 4. Revisa SEND_INVITES (false = crea sin notificar a nadie).
 * 5. Ejecuta crearEncuentrosDesdeHoja() → Autorizar → permitir Calendar.
 * 6. Abre un evento en Calendar: debe verse la sección Invitados.
 *
 * Regenerar: python config/slides/build_pruebas_csv_invitados_p1.py
 */
var SEND_INVITES = false; // true solo cuando quieras enviar el correo de invitación
var TIMEZONE = 'America/Bogota';

function crearEncuentrosDesdeHoja() {
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var filas = hoja.getDataRange().getDisplayValues();
  var head = filas[0].map(function (h) { return String(h).trim(); });
  var col = {};
  head.forEach(function (h, i) { col[h] = i; });

  ['Subject', 'Start Date', 'Start Time', 'End Time', 'Guests'].forEach(function (c) {
    if (col[c] === undefined) throw new Error('Falta la columna: ' + c);
  });

  var cal = CalendarApp.getDefaultCalendar();
  var creados = 0;
  var omitidos = 0;

  for (var i = 1; i < filas.length; i++) {
    var f = filas[i];
    var subject = f[col['Subject']];
    if (!subject) continue;

    var inicio = _fecha(f[col['Start Date']], f[col['Start Time']]);
    var finDia = f[col['End Date']] || f[col['Start Date']];
    var fin = _fecha(finDia, f[col['End Time']]);

    var yaExiste = cal.getEvents(inicio, fin, { search: subject }).some(function (ev) {
      return ev.getTitle() === subject;
    });
    if (yaExiste) { omitidos++; continue; }

    cal.createEvent(subject, inicio, fin, {
      description: f[col['Description']] || '',
      location: f[col['Location']] || '',
      guests: String(f[col['Guests']] || '').split(',').map(function (e) {
        return e.trim();
      }).filter(String).join(','),
      sendInvites: SEND_INVITES
    });
    creados++;
  }

  Logger.log('Creados=' + creados + ' omitidos=' + omitidos +
             ' sendInvites=' + SEND_INVITES);
}

/** «08/10/2026» + «8:00 PM» → Date en America/Bogota. */
function _fecha(fechaMDY, hora12) {
  var p = String(fechaMDY).split('/');
  var iso = p[2] + '-' + _pad(p[0]) + '-' + _pad(p[1]);
  var h = String(hora12).trim().toUpperCase().match(/^(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)$/);
  if (!h) throw new Error('Hora no reconocida: ' + hora12);
  var hh = parseInt(h[1], 10) % 12;
  if (h[4] === 'PM') hh += 12;
  var hms = _pad(hh) + ':' + h[2] + ':' + (h[3] || '00');
  return Utilities.parseDate(iso + ' ' + hms, TIMEZONE, 'yyyy-MM-dd HH:mm:ss');
}

function _pad(v) {
  v = String(v);
  return v.length < 2 ? '0' + v : v;
}
