/**
 * CREAR EVENTOS EN CALENDAR — V2 CON LINK ÚNICO DE MEET POR SESIÓN
 *
 * Crea eventos individuales en Google Calendar, cada uno con su propia conferencia de Meet.
 * NO crea eventos recurrentes — cada sesión es un evento independiente con link único.
 *
 * PROBLEMA QUE RESUELVE:
 * Cuando creas eventos recurrentes, Google Meet reutiliza el MISMO link para todas las
 * sesiones. Esta v2 crea eventos individuales para que cada sesión tenga su propio link.
 *
 * CONFIGURACIÓN:
 * - CONFIG_CURSOS: por cada curso, el título, fecha inicio, número de sesiones, día de la
 *   semana, hora inicio/fin y lista de participantes
 * - CALENDARIO_ID: tu correo (por defecto) o el ID de un calendario compartido
 * - SIMULAR: true/false (como siempre, simular primero)
 *
 * PASOS:
 * 1. https://script.google.com con tu cuenta
 * 2. Nuevo proyecto -> pega TODO este archivo -> guarda
 * 3. Edita CONFIG_CURSOS: por cada curso, los datos y los correos
 * 4. Ejecuta verificarEventos() (solo lectura) -> lee el registro
 * 5. Si cuadra: pon SIMULAR = false, guarda, ejecuta crearEventos()
 *
 * Deshacer: eliminarEventos() (elimina TODOS los eventos creados por este script)
 */

// ═══════════════════════ CONFIGURACIÓN ═════════════════════════════════

// Pre-configurado con los 5 cursos de la CUN (26ES4 / 26P03 / 26V04)
var CONFIG_CURSOS = [
  {
    titulo: "26ES4 - 54ES4 - Proyecto I - Sesión",  // prefijo del título (se agrega el número de sesión)
    fechaInicio: "2026-08-11",  // fecha de la primera sesión (YYYY-MM-DD)
    numSesiones: 15,  // cuántas sesiones crear
    diaSemana: 1,  // 0=Domingo, 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes, 6=Sábado
    horaInicio: "20:00",  // HH:MM formato 24h
    horaFin: "22:00",
    timezone: "America/Bogota",
    descripcion: "Clase sincrónica de Proyecto I\n\nEspecialización en Inteligencia Artificial\nCUN - 26ES4",
    participantes: [
      // <- pega aquí los correos de los estudiantes, uno por línea
      // "estudiante1@cun.edu.co",
      // "estudiante2@cun.edu.co",
    ]
  },
  {
    titulo: "26V04 - 54448 - Trabajo de Grado 2 - Sesión",
    fechaInicio: "2026-08-12",
    numSesiones: 15,
    diaSemana: 1,  // Lunes
    horaInicio: "17:00",
    horaFin: "18:00",
    timezone: "America/Bogota",
    descripcion: "Clase sincrónica de Trabajo de Grado 2\n\nIngeniería de Sistemas - Modelos de Innovación\nCUN - 26V04",
    participantes: []
  },
  {
    titulo: "26V04 - 54443 - Trabajo de Grado 3 - Sesión",
    fechaInicio: "2026-08-13",
    numSesiones: 15,
    diaSemana: 2,  // Martes
    horaInicio: "17:00",
    horaFin: "18:00",
    timezone: "America/Bogota",
    descripcion: "Clase sincrónica de Trabajo de Grado 3\n\nIngeniería de Sistemas - Modelos de Innovación\nCUN - 26V04",
    participantes: []
  },
  {
    titulo: "26P03 - 53339 - Creatividad y Pensamiento Innovador - Sesión",
    fechaInicio: "2026-08-13",
    numSesiones: 6,
    diaSemana: 2,  // Miércoles (ajustar al día real)
    horaInicio: "17:00",
    horaFin: "18:00",
    timezone: "America/Bogota",
    descripcion: "Clase sincrónica de Creatividad y Pensamiento Innovador\n\nEscuela de Ingenierías\nCUN - 26P03",
    participantes: []
  },
  {
    titulo: "26P03 - 53339 - Investigación Ciencia y Tecnología - Sesión",
    fechaInicio: "2026-08-14",
    numSesiones: 6,
    diaSemana: 3,  // Jueves
    horaInicio: "17:00",
    horaFin: "18:00",
    timezone: "America/Bogota",
    descripcion: "Clase sincrónica de Investigación Ciencia y Tecnología\n\nEscuela de Ingenierías\nCUN - 26P03",
    participantes: []
  }
];

// MODO SIMULACIÓN: con true nada escribe, solo dice qué haría. Ponlo en false cuando
// verificarEventos() te cuadre.
var SIMULAR = true;

// CALENDARIO: tu correo (usa el calendario principal) o el ID de un calendario compartido.
// Déjalo en 'primary' para usar tu calendario por defecto.
var CALENDARIO_ID = 'primary';

// DÍAS FESTIVOS o SESIONES A SALTAR (opcional): fechas en formato YYYY-MM-DD que se deben omitir.
// Si una sesión cae en una de estas fechas, se salta a la siguiente semana.
var FECHAS_FESTIVAS = [
  // "2026-08-17",  // ejemplo: día festivo
];

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

function _esFestivo_(fecha) {
  var fechaStr = Utilities.formatDate(fecha, 'America/Bogota', 'yyyy-MM-dd');
  for (var i = 0; i < FECHAS_FESTIVAS.length; i++) {
    if (FECHAS_FESTIVAS[i] === fechaStr) {
      return true;
    }
  }
  return false;
}

function _siguienteFecha_(fechaBase, diaSemana, timezone) {
  // Calcula la siguiente fecha que coincida con el día de la semana especificado
  var fecha = new Date(fechaBase);
  var diaActual = fecha.getDay();

  if (diaActual === diaSemana) {
    // Si ya es el día correcto, avanzar 7 días
    fecha.setDate(fecha.getDate() + 7);
  } else {
    // Calcular días hasta el próximo día de la semana
    var diasHasta = (diaSemana - diaActual + 7) % 7;
    if (diasHasta === 0) diasHasta = 7;
    fecha.setDate(fecha.getDate() + diasHasta);
  }

  // Saltar festivos
  while (_esFestivo_(fecha)) {
    fecha.setDate(fecha.getDate() + 7);
  }

  return fecha;
}

function _prop_(k) {
  return 'EVENTOS_V2_' + k;
}

function _leerEventosCreados_() {
  var ps = PropertiesService.getScriptProperties();
  var raw = ps.getProperty(_prop_('EVENTOS'));
  return raw ? JSON.parse(raw) : [];
}

function _escribirEventosCreados_(arr) {
  PropertiesService.getScriptProperties().setProperty(_prop_('EVENTOS'), JSON.stringify(arr));
}

function _registrarEvento_(eventId, titulo, fecha) {
  var eventos = _leerEventosCreados_();
  eventos.push({
    eventId: eventId,
    titulo: titulo,
    fecha: fecha.toISOString(),
    cuando: new Date().toISOString()
  });
  _escribirEventosCreados_(eventos);
}

// ── funciones principales ────────────────────────────────────────────────

function verificarEventos() {
  Logger.log('═════════ VERIFICAR EVENTOS (v2) ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var calendar = _calendarioPorId_(CALENDARIO_ID);
  if (!calendar) {
    Logger.log('❌ No se pudo abrir el calendario: ' + CALENDARIO_ID);
    return;
  }
  Logger.log('✓ Calendario: ' + calendar.getName());
  Logger.log('');

  var totalEventos = 0;

  for (var i = 0; i < CONFIG_CURSOS.length; i++) {
    var cfg = CONFIG_CURSOS[i];
    Logger.log('▸ [' + cfg.titulo + ']');
    Logger.log('  Fecha inicio: ' + cfg.fechaInicio);
    Logger.log('  Sesiones: ' + cfg.numSesiones);
    Logger.log('  Día: ' + _nombreDia_(cfg.diaSemana) + ', ' + cfg.horaInicio + ' - ' + cfg.horaFin);
    Logger.log('  Participantes: ' + (cfg.participantes ? cfg.participantes.length : 0));
    Logger.log('');

    var fechaBase = new Date(cfg.fechaInicio + ' 00:00:00');

    for (var j = 0; j < cfg.numSesiones; j++) {
      var numSesion = j + 1;
      var fechaEvento;

      if (j === 0) {
        fechaEvento = fechaBase;
      } else {
        fechaEvento = _siguienteFecha_(fechaEvento, cfg.diaSemana, cfg.timezone);
      }

      var tituloCompleto = cfg.titulo + ' ' + String(numSesion).padStart(2, '0');
      var fechaFormato = Utilities.formatDate(fechaEvento, cfg.timezone, 'yyyy-MM-dd (EEE)');

      Logger.log('  [' + numSesion + '] ' + tituloCompleto);
      Logger.log('      ' + fechaFormato + ' · ' + cfg.horaInicio + ' - ' + cfg.horaFin);

      totalEventos++;
    }

    Logger.log('');
  }

  Logger.log('─────────────────────────────────────');
  Logger.log('Total: ' + totalEventos + ' eventos a crear');
  Logger.log('');
  Logger.log('Si cuadra: pon SIMULAR = false y ejecuta crearEventos().');
}

function crearEventos() {
  Logger.log('═════════ CREAR EVENTOS (v2) ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var calendar = _calendarioPorId_(CALENDARIO_ID);
  if (!calendar) {
    Logger.log('❌ No se pudo abrir el calendario: ' + CALENDARIO_ID);
    return;
  }

  var totalCreados = 0, totalErrores = 0;

  for (var i = 0; i < CONFIG_CURSOS.length; i++) {
    var cfg = CONFIG_CURSOS[i];
    Logger.log('▸ Creando eventos para: ' + cfg.titulo);

    var fechaBase = new Date(cfg.fechaInicio + ' 00:00:00');

    for (var j = 0; j < cfg.numSesiones; j++) {
      var numSesion = j + 1;
      var fechaEvento;

      if (j === 0) {
        fechaEvento = fechaBase;
      } else {
        fechaEvento = _siguienteFecha_(fechaEvento, cfg.diaSemana, cfg.timezone);
      }

      var tituloCompleto = cfg.titulo + ' ' + String(numSesion).padStart(2, '0');

      // Construir fecha/hora de inicio y fin
      var horaIniParts = cfg.horaInicio.split(':');
      var horaFinParts = cfg.horaFin.split(':');

      var inicio = new Date(fechaEvento);
      inicio.setHours(parseInt(horaIniParts[0], 10));
      inicio.setMinutes(parseInt(horaIniParts[1], 10));
      inicio.setSeconds(0);

      var fin = new Date(fechaEvento);
      fin.setHours(parseInt(horaFinParts[0], 10));
      fin.setMinutes(parseInt(horaFinParts[1], 10));
      fin.setSeconds(0);

      try {
        if (SIMULAR) {
          Logger.log('  ✓ SIMULAR: [' + numSesion + '] ' + tituloCompleto);
          Logger.log('      ' + Utilities.formatDate(inicio, cfg.timezone, 'yyyy-MM-dd HH:mm'));
        } else {
          // Crear evento individual
          var evento = calendar.createEvent(tituloCompleto, inicio, fin, {
            description: cfg.descripcion || '',
            location: 'Google Meet (link único por sesión)'
          });

          // Agregar conferencia de Meet (cada evento tendrá su propio link)
          evento.addConferenceData();

          // Agregar participantes
          if (cfg.participantes && cfg.participantes.length > 0) {
            for (var k = 0; k < cfg.participantes.length; k++) {
              evento.addGuest(cfg.participantes[k]);
            }
          }

          _registrarEvento_(evento.getId(), tituloCompleto, inicio);
          Logger.log('  ✓ CREADO: [' + numSesion + '] ' + tituloCompleto);
        }
        totalCreados++;
      } catch (e) {
        Logger.log('  ❌ ERROR al crear sesión ' + numSesion + ': ' + e.toString());
        totalErrores++;
      }
    }

    Logger.log('');
  }

  Logger.log('─────────────────────────────────────');
  Logger.log('Resumen: ' + totalCreados + ' eventos creados, ' + totalErrores + ' errores');

  if (!SIMULAR) {
    Logger.log('');
    Logger.log('⚠️  IMPORTANTE: Cada evento tiene su propio link de Meet.');
    Logger.log('    Los estudiantes deben usar el link del evento de ESA sesión,');
    Logger.log('    no un link fijo para todo el curso.');
  }
}

function eliminarEventos() {
  Logger.log('═════════ ELIMINAR EVENTOS ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var eventos = _leerEventosCreados_();
  if (eventos.length === 0) {
    Logger.log('No hay eventos registrados para eliminar.');
    return;
  }

  var calendar = _calendarioPorId_(CALENDARIO_ID);
  if (!calendar) {
    Logger.log('❌ No se pudo abrir el calendario: ' + CALENDARIO_ID);
    return;
  }

  Logger.log('Eliminando ' + eventos.length + ' eventos...');
  var ok = 0, fallo = 0;

  for (var i = eventos.length - 1; i >= 0; i--) {
    var evt = eventos[i];
    try {
      if (SIMULAR) {
        Logger.log('  ✓ SIMULAR: eliminar ' + evt.titulo);
      } else {
        var evento = calendar.getEventById(evt.eventId);
        if (evento) {
          evento.deleteEvent();
          Logger.log('  ✓ ELIMINADO: ' + evt.titulo);
        } else {
          Logger.log('  ⚠️  No encontrado: ' + evt.titulo);
        }
      }
      ok++;
    } catch (e) {
      Logger.log('  ❌ ERROR al eliminar ' + evt.titulo + ': ' + e.toString());
      fallo++;
    }
  }

  Logger.log('');
  Logger.log('Resumen: ' + ok + ' eventos eliminados, ' + fallo + ' fallos');

  if (!SIMULAR && ok > 0) {
    Logger.log('Borrando el registro...');
    _escribirEventosCreados_([]);
  }
}

function _nombreDia_(dia) {
  var nombres = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
  return nombres[dia] || '?';
}