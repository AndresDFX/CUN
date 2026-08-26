/**
 * CAMBIAR LINK DE MEET EN EVENTOS EXISTENTES
 *
 * Busca eventos por título y les cambia el link de Meet a uno fijo que configures.
 *
 * CÓMO FUNCIONA:
 * Google Calendar NO permite cambiar el link de Meet de un evento existente. Este script:
 * 1. Busca eventos por título
 * 2. Guarda sus datos (fecha, hora, participantes, descripción)
 * 3. Los ELIMINA
 * 4. Los RECREA con el nuevo link de Meet que configures
 *
 * CONFIGURACIÓN:
 * - CONFIG_CURSOS: por cada curso, el fragmento del título y el nuevo link de Meet
 * - FECHA_DESDE / FECHA_HASTA: rango opcional para limitar la búsqueda
 * - SIMULAR: true/false (como siempre, simular primero)
 *
 * PASOS:
 * 1. https://script.google.com con tu cuenta
 * 2. Nuevo proyecto -> pega TODO este archivo -> guarda
 * 3. Edita CONFIG_CURSOS: por cada curso, el título y el link de Meet
 * 4. Ejecuta verificarEventos() (solo lectura) -> lee el registro
 * 5. Si cuadra: pon SIMULAR = false, guarda, ejecuta cambiarLinkMeet()
 *
 * ⚠️  IMPORTANTE: Los eventos se eliminan y recrean. Las notificaciones se reenvían.
 */

// ═══════════════════════ CONFIGURACIÓN ═════════════════════════════════

// Pre-configurado con los 5 cursos de la CUN
var CONFIG_CURSOS = [
  {
    tituloContiene: "Proyecto I",  // fragmento del título del evento
    nuevoLinkMeet: ""  // <- pega aquí el link de Meet (ej: https://meet.google.com/abc-defg-hij)
  },
  {
    tituloContiene: "Trabajo de Grado 2",
    nuevoLinkMeet: ""
  },
  {
    tituloContiene: "Trabajo de Grado 3",
    nuevoLinkMeet: ""
  },
  {
    tituloContiene: "Creatividad y Pensamiento Innovador",
    nuevoLinkMeet: ""
  },
  {
    tituloContiene: "Investigación Ciencia y Tecnología",
    nuevoLinkMeet: ""
  }
];

// MODO SIMULACIÓN: con true nada escribe, solo dice qué haría. Ponlo en false cuando
// verificarEventos() te cuadre.
var SIMULAR = true;

// CALENDARIO: tu correo (usa el calendario principal) o el ID de un calendario compartido.
var CALENDARIO_ID = 'primary';

// RANGO DE FECHAS (opcional): limita la búsqueda a eventos entre estas fechas.
// Formato: 'YYYY-MM-DD'. Si están vacías, busca en todo el calendario.
var FECHA_DESDE = '';  // ej: '2026-08-01'
var FECHA_HASTA = '';  // ej: '2026-12-31'

var TIMEZONE = 'America/Bogota';

// ══════════════════════════════ LÓGICA ══════════════════════════════════

function _calendarioPorId_(id) {
  if (id === 'primary' || id === '') {
    return CalendarApp.getDefaultCalendar();
  }
  try {
    return CalendarApp.getCalendarById(id);
  } catch (e) {
    return null;
  }
}

function _rangoDeFechas_() {
  var desde = null, hasta = null;

  if (FECHA_DESDE && FECHA_DESDE.trim() !== '') {
    desde = new Date(FECHA_DESDE + ' 00:00:00');
  }

  if (FECHA_HASTA && FECHA_HASTA.trim() !== '') {
    hasta = new Date(FECHA_HASTA + ' 23:59:59');
  }

  return { desde: desde, hasta: hasta };
}

function _buscarEventos_(calendar, titulo, rango) {
  var eventos = [];
  var busqueda;

  if (rango.desde && rango.hasta) {
    busqueda = calendar.getEvents(rango.desde, rango.hasta);
  } else if (rango.desde) {
    var futuro = new Date(rango.desde);
    futuro.setFullYear(futuro.getFullYear() + 2);
    busqueda = calendar.getEvents(rango.desde, futuro);
  } else if (rango.hasta) {
    var pasado = new Date(rango.hasta);
    pasado.setFullYear(pasado.getFullYear() - 2);
    busqueda = calendar.getEvents(pasado, rango.hasta);
  } else {
    var ahora = new Date();
    var pasado = new Date(ahora);
    pasado.setFullYear(pasado.getFullYear() - 2);
    var futuro = new Date(ahora);
    futuro.setFullYear(futuro.getFullYear() + 2);
    busqueda = calendar.getEvents(pasado, futuro);
  }

  for (var i = 0; i < busqueda.length; i++) {
    var evt = busqueda[i];
    var tituloEvt = evt.getTitle();
    if (tituloEvt.toLowerCase().indexOf(titulo.toLowerCase()) >= 0) {
      eventos.push(evt);
    }
  }

  return eventos;
}

function _participantesActuales_(evento) {
  var invitados = evento.getGuestList();
  var correos = [];
  for (var i = 0; i < invitados.length; i++) {
    correos.push(invitados[i].getEmail());
  }
  return correos;
}

function _datosEvento_(evento) {
  return {
    titulo: evento.getTitle(),
    inicio: evento.getStartTime(),
    fin: evento.getEndTime(),
    descripcion: evento.getDescription(),
    ubicacion: evento.getLocation(),
    participantes: _participantesActuales_(evento)
  };
}

// ── funciones principales ────────────────────────────────────────────────

function verificarEventos() {
  Logger.log('═════════ VERIFICAR EVENTOS ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var calendar = _calendarioPorId_(CALENDARIO_ID);
  if (!calendar) {
    Logger.log('❌ No se pudo abrir el calendario: ' + CALENDARIO_ID);
    return;
  }
  Logger.log('✓ Calendario: ' + calendar.getName());
  Logger.log('');

  var rango = _rangoDeFechas_();
  if (rango.desde || rango.hasta) {
    Logger.log('Rango de fechas:');
    if (rango.desde) Logger.log('  Desde: ' + rango.desde.toLocaleDateString());
    if (rango.hasta) Logger.log('  Hasta: ' + rango.hasta.toLocaleDateString());
    Logger.log('');
  }

  var totalEventos = 0;

  for (var i = 0; i < CONFIG_CURSOS.length; i++) {
    var cfg = CONFIG_CURSOS[i];
    Logger.log('▸ [' + cfg.tituloContiene + ']');

    if (!cfg.nuevoLinkMeet || cfg.nuevoLinkMeet.trim() === '') {
      Logger.log('  ⚠️  Sin link de Meet configurado, se omite');
      Logger.log('');
      continue;
    }

    var eventos = _buscarEventos_(calendar, cfg.tituloContiene, rango);
    Logger.log('  Eventos encontrados: ' + eventos.length);
    Logger.log('  Nuevo link de Meet: ' + cfg.nuevoLinkMeet);

    if (eventos.length === 0) {
      Logger.log('  ⚠️  No se encontraron eventos con ese título');
      Logger.log('');
      continue;
    }

    totalEventos += eventos.length;

    for (var j = 0; j < eventos.length && j < 5; j++) {
      var evt = eventos[j];
      Logger.log('');
      Logger.log('  [' + (j + 1) + '] ' + evt.getTitle());
      Logger.log('      Fecha: ' + evt.getStartTime().toLocaleString());
      Logger.log('      Participantes: ' + _participantesActuales_(evt).length);
    }

    if (eventos.length > 5) {
      Logger.log('');
      Logger.log('  ... y ' + (eventos.length - 5) + ' eventos más');
    }

    Logger.log('');
  }

  Logger.log('─────────────────────────────────────');
  Logger.log('Total: ' + totalEventos + ' eventos a actualizar');
  Logger.log('');
  Logger.log('⚠️  IMPORTANTE: Los eventos se ELIMINAN y RECREAN con el nuevo link.');
  Logger.log('    Las invitaciones se reenvían a los participantes.');
  Logger.log('');
  Logger.log('Si cuadra: pon SIMULAR = false y ejecuta cambiarLinkMeet().');
}

function cambiarLinkMeet() {
  Logger.log('═════════ CAMBIAR LINK DE MEET ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var calendar = _calendarioPorId_(CALENDARIO_ID);
  if (!calendar) {
    Logger.log('❌ No se pudo abrir el calendario: ' + CALENDARIO_ID);
    return;
  }

  var rango = _rangoDeFechas_();
  var totalCambiados = 0, totalErrores = 0;

  for (var i = 0; i < CONFIG_CURSOS.length; i++) {
    var cfg = CONFIG_CURSOS[i];

    if (!cfg.nuevoLinkMeet || cfg.nuevoLinkMeet.trim() === '') {
      continue;
    }

    var eventos = _buscarEventos_(calendar, cfg.tituloContiene, rango);

    Logger.log('▸ [' + cfg.tituloContiene + '] - ' + eventos.length + ' eventos');

    for (var j = 0; j < eventos.length; j++) {
      var evt = eventos[j];
      var datos = _datosEvento_(evt);

      try {
        if (SIMULAR) {
          Logger.log('  ✓ SIMULAR: ' + datos.titulo);
          Logger.log('      Fecha: ' + datos.inicio.toLocaleString());
        } else {
          // Eliminar evento viejo
          evt.deleteEvent();

          // Recrear con el nuevo link de Meet
          var descripcionNueva = datos.descripcion;
          if (descripcionNueva.indexOf('meet.google.com') < 0) {
            descripcionNueva += '\n\nEnlace de Meet: ' + cfg.nuevoLinkMeet;
          }

          var nuevoEvento = calendar.createEvent(datos.titulo, datos.inicio, datos.fin, {
            description: descripcionNueva,
            location: cfg.nuevoLinkMeet
          });

          // Agregar participantes
          for (var k = 0; k < datos.participantes.length; k++) {
            nuevoEvento.addGuest(datos.participantes[k]);
          }

          Logger.log('  ✓ ACTUALIZADO: ' + datos.titulo);
          Logger.log('      Nuevo ID: ' + nuevoEvento.getId());
        }
        totalCambiados++;
      } catch (e) {
        Logger.log('  ❌ ERROR al actualizar ' + datos.titulo + ': ' + e.toString());
        totalErrores++;
      }
    }

    Logger.log('');
  }

  Logger.log('─────────────────────────────────────');
  Logger.log('Resumen: ' + totalCambiados + ' eventos actualizados, ' + totalErrores + ' errores');

  if (!SIMULAR) {
    Logger.log('');
    Logger.log('✓ Los eventos tienen el nuevo link de Meet.');
    Logger.log('  NOTA: Los IDs de los eventos cambiaron (se recrearon).');
  }
}