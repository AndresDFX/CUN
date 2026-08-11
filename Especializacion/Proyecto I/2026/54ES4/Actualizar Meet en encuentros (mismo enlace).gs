/**
 * Proyecto I · 54ES4 — Poner el MISMO enlace de Meet en los 11 encuentros ya creados.
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * POR QUÉ HACE FALTA ESTE SCRIPT
 * `CalendarApp.createEvent()` (el que usó «Crear encuentros con invitados.gs»)
 * NO adjunta videoconferencia. Si después se añade Meet evento por evento desde
 * la interfaz de Calendar, Google genera un enlace DISTINTO en cada uno.
 * Este script deja los 11 encuentros apuntando a una sola sala.
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * ANTES DE EJECUTAR (2 minutos)
 * 1. https://script.google.com con la cuenta CUN (julian_castanoe@cun.edu.co).
 * 2. Abre el proyecto donde pegaste «Crear encuentros con invitados.gs»
 *    (o crea uno nuevo) y pega ESTE archivo como un .gs aparte.
 * 3. ⚠️ Activa el servicio avanzado de Calendar (necesario para el botón nativo
 *    «Unirse con Google Meet»):
 *       Panel izquierdo → Servicios (+) → «Google Calendar API» → Añadir.
 *    Si NO lo activas, el script sigue funcionando en modo compatible: deja el
 *    enlace en Ubicación y en la descripción (clicable), pero sin el chip de Meet.
 * 4. Ejecuta primero `verificarMeetP1()` → es de SOLO LECTURA, no cambia nada.
 * 5. Revisa el log (Ver → Registro) y, si todo cuadra, ejecuta `actualizarMeetP1()`.
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * NOTIFICACIONES
 * `NOTIFICAR = false` por defecto: los 40 estudiantes NO reciben correo por este
 * cambio. Ponlo en true solo si quieres avisarles del enlace definitivo (mandaría
 * una actualización por evento).
 */

// ───────────────────────────── CONFIGURACIÓN ─────────────────────────────────
var MEET_URL = 'https://meet.google.com/omk-woqk-vsj'; // enlace único de toda la serie
// Fragmento que identifica a los encuentros de la serie. Se busca CONTENIDO, no prefijo:
// el subject lleva ahora el periodo delante («26ES4 - 54ES4 - Proyecto I - Sesion 01»), y un
// match anclado al inicio dejaba de encontrar los eventos — el script quedaba mudo y parecía
// que no había nada que actualizar. Corregido 2026-08-11.
var MARCA = '54ES4 - Proyecto I - Sesion';             // aparece en el título del encuentro
var DESDE = '2026-08-01';                              // ventana de búsqueda
var HASTA = '2026-11-30';
var NOTIFICAR = false;    // true = avisa a los invitados de cada cambio
var TIMEZONE = 'America/Bogota';

// Línea que se garantiza en la descripción (además de Ubicación).
var LINEA_MEET = 'Meet (mismo enlace toda la serie): ' + MEET_URL;

// ─────────────────────────────── PÚBLICAS ────────────────────────────────────

/** SOLO LECTURA. Muestra cómo está cada encuentro hoy. Ejecuta esto primero. */
function verificarMeetP1() {
  var eventos = _encuentros_();
  if (!eventos.length) {
    Logger.log('No se encontró ningún evento cuyo título contenga "' + MARCA + '".');
    Logger.log('Revisa MARCA / DESDE / HASTA, o que estés en la cuenta correcta.');
    return;
  }
  Logger.log('Encontrados ' + eventos.length + ' encuentros. Servicio avanzado: ' +
             (_apiDisponible_() ? 'ACTIVO (botón nativo de Meet)' : 'NO activo (modo compatible)'));
  Logger.log('---');
  eventos.forEach(function (ev) {
    var loc = ev.getLocation() || '';
    var desc = ev.getDescription() || '';
    var nativo = _meetNativo_(ev.getId());
    Logger.log(
      Utilities.formatDate(ev.getStartTime(), TIMEZONE, 'dd/MM HH:mm') + '  ' +
      ev.getTitle() +
      '\n    Meet nativo : ' + (nativo || '—') +
      '\n    Ubicación   : ' + (loc || '—') +
      '\n    En descrip. : ' + (desc.indexOf(MEET_URL) >= 0 ? 'sí' : 'no')
    );
  });
  Logger.log('---');
  Logger.log('Si esto se ve bien, ejecuta actualizarMeetP1().');
}

/** Pone MEET_URL en los 11 encuentros: conferencia nativa (si se puede) + Ubicación + descripción. */
function actualizarMeetP1() {
  var eventos = _encuentros_();
  if (!eventos.length) {
    Logger.log('Nada que actualizar: no se encontraron encuentros. Ejecuta verificarMeetP1().');
    return;
  }
  var api = _apiDisponible_();
  var nativos = 0, basicos = 0, errores = 0;

  eventos.forEach(function (ev) {
    var titulo = ev.getTitle();
    try {
      // 1) Ubicación + descripción (funciona siempre, y es lo que se ve en el correo).
      if (ev.getLocation() !== MEET_URL) ev.setLocation(MEET_URL);
      var desc = ev.getDescription() || '';
      if (desc.indexOf(MEET_URL) < 0) {
        ev.setDescription((desc ? desc + '\n' : '') + LINEA_MEET);
      }
      // 2) Conferencia nativa (botón «Unirse con Google Meet»), si hay servicio avanzado.
      if (api && _adjuntarMeet_(ev.getId())) nativos++;
      else basicos++;
    } catch (e) {
      errores++;
      Logger.log('ERROR en "' + titulo + '": ' + e);
    }
  });

  Logger.log('Listo. Encuentros procesados: ' + eventos.length);
  Logger.log('  con Meet nativo   : ' + nativos);
  Logger.log('  solo enlace       : ' + basicos + (api ? '' : '  (activa Google Calendar API para el chip nativo)'));
  Logger.log('  errores           : ' + errores);
  Logger.log('Notificación a invitados: ' + (NOTIFICAR ? 'SÍ enviada' : 'no (NOTIFICAR = false)'));
  Logger.log('Verifica con verificarMeetP1().');
}

/** Quita el enlace de Ubicación y descripción (por si hay que revertir). No toca la conferencia nativa. */
function revertirEnlaceP1() {
  var n = 0;
  _encuentros_().forEach(function (ev) {
    if (ev.getLocation() === MEET_URL) { ev.setLocation(''); n++; }
    var d = ev.getDescription() || '';
    if (d.indexOf(LINEA_MEET) >= 0) {
      ev.setDescription(d.replace('\n' + LINEA_MEET, '').replace(LINEA_MEET, '').trim());
    }
  });
  Logger.log('Revertidos: ' + n);
}

// ─────────────────────────────── INTERNAS ────────────────────────────────────

function _encuentros_() {
  var cal = CalendarApp.getDefaultCalendar();
  var desde = _fecha_(DESDE), hasta = _fecha_(HASTA);
  return cal.getEvents(desde, hasta)
    .filter(function (ev) { return (ev.getTitle() || '').indexOf(MARCA) !== -1; })
    .sort(function (a, b) { return a.getStartTime() - b.getStartTime(); });
}

function _fecha_(iso) {
  return Utilities.parseDate(iso + ' 00:00:00', TIMEZONE, 'yyyy-MM-dd HH:mm:ss');
}

/** ¿Está añadido el servicio avanzado «Google Calendar API»? */
function _apiDisponible_() {
  try { return typeof Calendar !== 'undefined' && !!Calendar.Events; }
  catch (e) { return false; }
}

/** Código de sala a partir de la URL: omk-woqk-vsj */
function _codigoMeet_() {
  var m = MEET_URL.match(/meet\.google\.com\/([a-z0-9-]+)/i);
  return m ? m[1] : MEET_URL;
}

/** Devuelve el enlace de Meet nativo del evento, o '' si no tiene. */
function _meetNativo_(eventId) {
  if (!_apiDisponible_()) return '';
  try {
    var id = eventId.split('@')[0];
    var ev = Calendar.Events.get('primary', id, { conferenceDataVersion: 1 });
    if (ev && ev.conferenceData && ev.conferenceData.entryPoints) {
      for (var i = 0; i < ev.conferenceData.entryPoints.length; i++) {
        if (ev.conferenceData.entryPoints[i].entryPointType === 'video') {
          return ev.conferenceData.entryPoints[i].uri;
        }
      }
    }
    return '';
  } catch (e) { return ''; }
}

/**
 * Adjunta la MISMA sala de Meet al evento (chip nativo «Unirse con Google Meet»).
 * Reutiliza una conferencia existente pasando entryPoints + conferenceSolution
 * sin createRequest — que es como Calendar copia el Meet al duplicar un evento.
 */
function _adjuntarMeet_(eventId) {
  try {
    var id = eventId.split('@')[0];
    var actual = _meetNativo_(eventId);
    if (actual === MEET_URL) return true; // ya está bien, no lo toques

    var codigo = _codigoMeet_();
    var recurso = {
      conferenceData: {
        conferenceId: codigo,
        signature: null,
        conferenceSolution: {
          key: { type: 'hangoutsMeet' },
          name: 'Google Meet'
        },
        entryPoints: [{
          entryPointType: 'video',
          uri: MEET_URL,
          label: MEET_URL.replace('https://', '')
        }]
      }
    };
    Calendar.Events.patch(recurso, 'primary', id, {
      conferenceDataVersion: 1,
      sendUpdates: NOTIFICAR ? 'all' : 'none'
    });
    return _meetNativo_(eventId) === MEET_URL;
  } catch (e) {
    Logger.log('  (sin conferencia nativa: ' + e + ')');
    return false;
  }
}
