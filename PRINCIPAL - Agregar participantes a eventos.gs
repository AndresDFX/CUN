/**
 * AGREGAR PARTICIPANTES A EVENTOS DE CALENDAR
 *
 * Busca eventos en tu Calendar por título y agrega una lista de correos como invitados.
 * Útil para agregar estudiantes a todas las sesiones de un curso, o agregar observadores/tutores.
 *
 * CONFIGURACIÓN
 * 1. CONFIG_EVENTOS: por cada curso, el fragmento del título y la lista de correos a agregar
 * 2. FECHA_DESDE / FECHA_HASTA: rango de fechas para limitar la búsqueda (opcional)
 * 3. CALENDARIO_ID: tu correo (por defecto) o el ID de un calendario compartido
 *
 * PASOS
 * 1. https://script.google.com con tu cuenta
 * 2. Nuevo proyecto -> pega TODO este archivo -> guarda
 * 3. Edita CONFIG_EVENTOS: por cada curso, el fragmento del título y los correos
 * 4. Ejecuta verificarEventos() (solo lectura) -> lee el registro
 * 5. Si cuadra: pon SIMULAR = false, guarda, ejecuta agregarParticipantes()
 *
 * Deshacer: quitarParticipantes() (los quita de todos los eventos)
 */

// ═══════════════════════ CONFIGURACIÓN ═════════════════════════════════

var CONFIG_EVENTOS = [
  {
    tituloContiene: "Trabajo de grado 3",  // fragmento del título del evento
    participantes: [
      // <- pega aquí los correos, uno por línea
      // "estudiante1@cun.edu.co",
      // "estudiante2@cun.edu.co",
    ]
  },
  {
    tituloContiene: "Trabajo de grado 2",
    participantes: [
      // "estudiante3@cun.edu.co",
    ]
  },
  {
    tituloContiene: "Proyecto I",
    participantes: [
      // "estudiante4@cun.edu.co",
    ]
  }
];

// MODO SIMULACIÓN: con true nada escribe, solo dice qué haría. Ponlo en false cuando
// verificarEventos() te cuadre.
var SIMULAR = true;

// CALENDARIO: tu correo (usa el calendario principal) o el ID de un calendario compartido.
// Déjalo en 'primary' para usar tu calendario por defecto.
var CALENDARIO_ID = 'primary';

// RANGO DE FECHAS (opcional): limita la búsqueda a eventos entre estas fechas.
// Formato: 'YYYY-MM-DD'. Si están vacías, busca en todo el calendario.
var FECHA_DESDE = '';  // ej: '2026-08-01'
var FECHA_HASTA = '';  // ej: '2026-12-31'

// Zona horaria para interpretar las fechas
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
    // desde una fecha hacia el futuro (próximos 2 años)
    var futuro = new Date(rango.desde);
    futuro.setFullYear(futuro.getFullYear() + 2);
    busqueda = calendar.getEvents(rango.desde, futuro);
  } else if (rango.hasta) {
    // desde hace 2 años hasta una fecha
    var pasado = new Date(rango.hasta);
    pasado.setFullYear(pasado.getFullYear() - 2);
    busqueda = calendar.getEvents(pasado, rango.hasta);
  } else {
    // sin rango: últimos 2 años + próximos 2 años
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

function _faltanAgregar_(actuales, nuevos) {
  var faltan = [];
  for (var i = 0; i < nuevos.length; i++) {
    var correo = nuevos[i].toLowerCase();
    var yaEsta = false;
    for (var j = 0; j < actuales.length; j++) {
      if (actuales[j].toLowerCase() === correo) {
        yaEsta = true;
        break;
      }
    }
    if (!yaEsta) {
      faltan.push(nuevos[i]);
    }
  }
  return faltan;
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

  var totalEventos = 0, totalParticipantes = 0;

  for (var i = 0; i < CONFIG_EVENTOS.length; i++) {
    var cfg = CONFIG_EVENTOS[i];
    Logger.log('▸ [' + cfg.tituloContiene + ']');

    if (!cfg.participantes || cfg.participantes.length === 0) {
      Logger.log('  ⚠️  Sin participantes configurados, se omite');
      Logger.log('');
      continue;
    }

    var eventos = _buscarEventos_(calendar, cfg.tituloContiene, rango);
    Logger.log('  Eventos encontrados: ' + eventos.length);

    if (eventos.length === 0) {
      Logger.log('  ⚠️  No se encontraron eventos con ese título');
      Logger.log('');
      continue;
    }

    totalEventos += eventos.length;

    for (var j = 0; j < eventos.length; j++) {
      var evt = eventos[j];
      var actuales = _participantesActuales_(evt);
      var faltan = _faltanAgregar_(actuales, cfg.participantes);

      Logger.log('');
      Logger.log('  [' + (j + 1) + '] ' + evt.getTitle());
      Logger.log('      Fecha: ' + evt.getStartTime().toLocaleString());
      Logger.log('      Participantes actuales: ' + actuales.length);
      Logger.log('      A agregar: ' + faltan.length);

      if (faltan.length > 0) {
        for (var k = 0; k < faltan.length; k++) {
          Logger.log('        + ' + faltan[k]);
        }
        totalParticipantes += faltan.length;
      } else {
        Logger.log('        (todos ya están invitados)');
      }
    }

    Logger.log('');
  }

  Logger.log('─────────────────────────────────────');
  Logger.log('Total: ' + totalEventos + ' eventos, ' + totalParticipantes + ' invitaciones a agregar');
  Logger.log('');
  Logger.log('Si cuadra: pon SIMULAR = false y ejecuta agregarParticipantes().');
}

function agregarParticipantes() {
  Logger.log('═════════ AGREGAR PARTICIPANTES ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var calendar = _calendarioPorId_(CALENDARIO_ID);
  if (!calendar) {
    Logger.log('❌ No se pudo abrir el calendario: ' + CALENDARIO_ID);
    return;
  }

  var rango = _rangoDeFechas_();
  var totalAgregados = 0, totalEventos = 0;

  for (var i = 0; i < CONFIG_EVENTOS.length; i++) {
    var cfg = CONFIG_EVENTOS[i];

    if (!cfg.participantes || cfg.participantes.length === 0) {
      continue;
    }

    var eventos = _buscarEventos_(calendar, cfg.tituloContiene, rango);

    for (var j = 0; j < eventos.length; j++) {
      var evt = eventos[j];
      var actuales = _participantesActuales_(evt);
      var faltan = _faltanAgregar_(actuales, cfg.participantes);

      if (faltan.length === 0) {
        continue;
      }

      totalEventos++;

      Logger.log('[' + cfg.tituloContiene + '] ' + evt.getTitle());
      Logger.log('  Fecha: ' + evt.getStartTime().toLocaleString());

      for (var k = 0; k < faltan.length; k++) {
        try {
          if (SIMULAR) {
            Logger.log('  ✓ SIMULAR: agregar ' + faltan[k]);
          } else {
            evt.addGuest(faltan[k]);
            Logger.log('  ✓ AGREGADO: ' + faltan[k]);
          }
          totalAgregados++;
        } catch (e) {
          Logger.log('  ❌ ERROR al agregar ' + faltan[k] + ': ' + e.toString());
        }
      }

      Logger.log('');
    }
  }

  Logger.log('─────────────────────────────────────');
  Logger.log('Resumen: ' + totalAgregados + ' participantes agregados en ' + totalEventos + ' eventos');
}

function quitarParticipantes() {
  Logger.log('═════════ QUITAR PARTICIPANTES ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var calendar = _calendarioPorId_(CALENDARIO_ID);
  if (!calendar) {
    Logger.log('❌ No se pudo abrir el calendario: ' + CALENDARIO_ID);
    return;
  }

  var rango = _rangoDeFechas_();
  var totalQuitados = 0, totalEventos = 0;

  for (var i = 0; i < CONFIG_EVENTOS.length; i++) {
    var cfg = CONFIG_EVENTOS[i];

    if (!cfg.participantes || cfg.participantes.length === 0) {
      continue;
    }

    var eventos = _buscarEventos_(calendar, cfg.tituloContiene, rango);

    for (var j = 0; j < eventos.length; j++) {
      var evt = eventos[j];
      var actuales = _participantesActuales_(evt);
      var aQuitar = [];

      // verificar cuáles de los configurados están presentes
      for (var k = 0; k < cfg.participantes.length; k++) {
        var correo = cfg.participantes[k].toLowerCase();
        for (var m = 0; m < actuales.length; m++) {
          if (actuales[m].toLowerCase() === correo) {
            aQuitar.push(cfg.participantes[k]);
            break;
          }
        }
      }

      if (aQuitar.length === 0) {
        continue;
      }

      totalEventos++;

      Logger.log('[' + cfg.tituloContiene + '] ' + evt.getTitle());
      Logger.log('  Fecha: ' + evt.getStartTime().toLocaleString());

      for (var n = 0; n < aQuitar.length; n++) {
        try {
          if (SIMULAR) {
            Logger.log('  ✓ SIMULAR: quitar ' + aQuitar[n]);
          } else {
            evt.removeGuest(aQuitar[n]);
            Logger.log('  ✓ QUITADO: ' + aQuitar[n]);
          }
          totalQuitados++;
        } catch (e) {
          Logger.log('  ❌ ERROR al quitar ' + aQuitar[n] + ': ' + e.toString());
        }
      }

      Logger.log('');
    }
  }

  Logger.log('─────────────────────────────────────');
  Logger.log('Resumen: ' + totalQuitados + ' participantes quitados de ' + totalEventos + ' eventos');
}