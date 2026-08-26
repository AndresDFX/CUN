# -*- coding: utf-8 -*-
"""Genera la V2 del Apps Script de creación de eventos en Calendar — con link único de Meet por sesión.

PROBLEMA QUE RESUELVE:
Cuando creas eventos recurrentes o copias eventos en Calendar, Google Meet reutiliza el MISMO
link para todas las sesiones. Esto genera confusión: los estudiantes entran al Meet de la sesión
1 cuando quieren ir a la sesión 5.

SOLUCIÓN:
Esta v2 crea eventos INDIVIDUALES (no recurrentes), cada uno con su propia conferencia de Meet.
Cada sesión tiene un link único.

Uso:
  python config/calendar/build_apps_script_crear_eventos_v2.py

Escribe:
  - PRINCIPAL - Crear eventos con link unico (v2).gs
  - LEEME - Crear eventos con link unico (v2).md
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GS_NAME = "PRINCIPAL - Crear eventos con link unico (v2).gs"
LEEME_NAME = "LEEME - Crear eventos con link unico (v2).md"

# ── el .gs ─────────────────────────────────────────────────────────────
GS_CONTENT = """/**
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
    descripcion: "Clase sincrónica de Proyecto I\\n\\nEspecialización en Inteligencia Artificial\\nCUN - 26ES4",
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
    descripcion: "Clase sincrónica de Trabajo de Grado 2\\n\\nIngeniería de Sistemas - Modelos de Innovación\\nCUN - 26V04",
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
    descripcion: "Clase sincrónica de Trabajo de Grado 3\\n\\nIngeniería de Sistemas - Modelos de Innovación\\nCUN - 26V04",
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
    descripcion: "Clase sincrónica de Creatividad y Pensamiento Innovador\\n\\nEscuela de Ingenierías\\nCUN - 26P03",
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
    descripcion: "Clase sincrónica de Investigación Ciencia y Tecnología\\n\\nEscuela de Ingenierías\\nCUN - 26P03",
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
""".strip()

# ── el LEEME ───────────────────────────────────────────────────────────
LEEME_CONTENT = """# Crear eventos en Calendar con link único de Meet — Guía de uso v2

**Versión 2 — con link único de Meet por sesión**

Este Apps Script crea eventos individuales en Google Calendar, cada uno con su propia
conferencia de Meet. NO crea eventos recurrentes.

## Problema que resuelve

Cuando creas eventos recurrentes o copias eventos en Calendar, Google Meet reutiliza el MISMO
link para todas las sesiones. Esto genera confusión: los estudiantes entran al Meet de la sesión
1 cuando quieren ir a la sesión 5.

**Esta v2 crea eventos INDIVIDUALES** para que cada sesión tenga su propio link de Meet.

## Diferencia con la v1

| | v1 | v2 |
|:--|:--|:--|
| **Eventos** | Serie recurrente (un solo evento) | Eventos individuales (uno por sesión) |
| **Link de Meet** | EL MISMO para todas las sesiones | Link ÚNICO por sesión |
| **Generación** | Se regenera desde Python | Se edita directo en Apps Script |
| **Config** | Inyecta correos desde JSON | Correos editables en el .gs |

## Configuración pre-cargada

El script viene **pre-configurado con los 5 cursos de la CUN** (26ES4 / 26P03 / 26V04):
1. Proyecto I (Especialización IA) — Lunes 8:00 pm - 10:00 pm
2. Trabajo de Grado 2 — Lunes 5:00 pm - 6:00 pm
3. Trabajo de Grado 3 — Martes 5:00 pm - 6:00 pm
4. Creatividad y Pensamiento Innovador — Miércoles 5:00 pm - 6:00 pm
5. Investigación Ciencia y Tecnología — Jueves 5:00 pm - 6:00 pm

Solo tienes que agregar los correos de los estudiantes y ajustar fechas/números de sesión.

## Pasos de instalación

### 1. Abre Apps Script

Ve a [script.google.com](https://script.google.com) con tu cuenta (la que organizará las clases).

### 2. Crea un proyecto nuevo

- Nuevo proyecto
- Pega TODO el contenido de `PRINCIPAL - Crear eventos con link unico (v2).gs`
- Guarda

### 3. Edita `CONFIG_CURSOS`

Por cada curso, ajusta:

```javascript
{
  titulo: "26ES4 - 54ES4 - Proyecto I - Sesión",  // prefijo (se agrega el número)
  fechaInicio: "2026-08-11",  // fecha de la primera sesión
  numSesiones: 15,  // cuántas sesiones crear
  diaSemana: 1,  // 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes
  horaInicio: "20:00",  // HH:MM formato 24h
  horaFin: "22:00",
  participantes: [
    "estudiante1@cun.edu.co",  // <- agrega aquí los correos
    "estudiante2@cun.edu.co",
  ]
}
```

### 4. (Opcional) Configura festivos

Si hay días festivos que quieres saltar:

```javascript
var FECHAS_FESTIVAS = [
  "2026-08-17",  // ejemplo
  "2026-10-12",
];
```

Si una sesión cae en una fecha festiva, se salta a la siguiente semana.

### 5. Verifica (solo lectura)

Ejecuta `verificarEventos()`:
- Botón ▶️ arriba, elige `verificarEventos`
- La primera vez pedirá permisos
- Lee TODO el registro: te dice cuántos eventos va a crear y en qué fechas

### 6. Ejecuta una vez a mano

Si el paso anterior cuadra:
1. Cambia `SIMULAR = true` por `SIMULAR = false`
2. Guarda
3. Ejecuta `crearEventos()` UNA vez
4. Lee el registro: debe decir "✓ CREADO:" por cada evento

## Funciones disponibles

| Función | Qué hace |
|:--|:--|
| `verificarEventos()` | Solo lectura. Dice qué haría sin crear nada. |
| `crearEventos()` | Crea los eventos (respeta `SIMULAR`). |
| `eliminarEventos()` | Elimina TODOS los eventos creados por este script. |

## Importante sobre los links de Meet

**Cada evento tiene su propio link de Meet.** Los estudiantes NO pueden usar un link fijo para
todo el curso — deben usar el link del evento de ESA sesión.

**Cómo compartir los links:**
- Opción 1: Los estudiantes abren el evento en su Calendar y hacen clic en el link de Meet
- Opción 2: Copias el link de Meet de cada evento y lo pegas en el chat/aula
- Opción 3: Usas un link fijo para todo el curso (creas una sala permanente en meet.google.com)
  y lo agregas manualmente a cada evento

## Agregar un curso nuevo

1. Abre el proyecto en Apps Script
2. Edita `CONFIG_CURSOS`: agrega una entrada más
3. Guarda
4. Ejecuta `verificarEventos()` para comprobar
5. Si cuadra: `SIMULAR = false` → `crearEventos()`

**No hace falta regenerar nada**: editas directo en Apps Script.

## Cambiar fechas o número de sesiones

Igual: editas `CONFIG_CURSOS` en Apps Script, cambias `fechaInicio` o `numSesiones`, y vuelves a
ejecutar `crearEventos()`.

**NOTA:** Si ya creaste eventos y quieres cambiar algo, primero ejecuta `eliminarEventos()` para
borrar los anteriores, y luego `crearEventos()` con la nueva config.

## Deshacer

Si te equivocaste:
1. Ejecuta `eliminarEventos()`
2. Lee el registro: debe decir "✓ ELIMINADO:" por cada evento
3. Los eventos se borran de Calendar y el registro se limpia

## Limitaciones

- **Notificaciones:** Google envía correo de invitación a cada participante. No se puede silenciar.
- **Link único vs link fijo:** Si prefieres un link fijo para todo el curso, crea una sala
  permanente en meet.google.com y agrégala manualmente a cada evento.
- **Eventos ya existentes:** Este script NO modifica eventos existentes. Solo crea nuevos.

## Calendario compartido

Si quieres crear los eventos en un calendario compartido (no en tu calendario principal):

1. Abre el calendario en Google Calendar
2. Configuración → nombre del calendario → "Integrar calendario" → copia el ID
3. Pega el ID en `CALENDARIO_ID`:
   ```javascript
   var CALENDARIO_ID = 'abc123@group.calendar.google.com';
   ```

Por defecto usa `'primary'` (tu calendario principal).

## Dónde están los archivos

- Generador: `config/calendar/build_apps_script_crear_eventos_v2.py`
- .gs generado: `PRINCIPAL - Crear eventos con link unico (v2).gs`
- Este LEEME: `LEEME - Crear eventos con link unico (v2).md`

Regenerar:
```bash
python config/calendar/build_apps_script_crear_eventos_v2.py
```

## Versión y autoría

**v2 — 26/08/2026**
Con link único de Meet por sesión. Pre-configurado con los 5 cursos de la CUN.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
""".strip()


def main():
    gs_path = ROOT / GS_NAME
    leeme_path = ROOT / LEEME_NAME

    print(f"Escribiendo {GS_NAME}...")
    gs_path.write_text(GS_CONTENT, encoding="utf-8")

    print(f"Escribiendo {LEEME_NAME}...")
    leeme_path.write_text(LEEME_CONTENT, encoding="utf-8")

    print()
    print(f"OK {GS_NAME}  ({len(GS_CONTENT):,} bytes)")
    print(f"OK {LEEME_NAME}  ({len(LEEME_CONTENT):,} bytes)")
    print()
    print("Próximos pasos:")
    print("1. Abre script.google.com con tu cuenta")
    print(f"2. Nuevo proyecto -> pega el contenido de '{GS_NAME}'")
    print("3. Edita CONFIG_CURSOS: ya viene con los 5 cursos de la CUN, solo agrega correos")
    print("4. Ejecuta verificarEventos() -> si cuadra, SIMULAR=false -> crearEventos()")
    print()
    print("IMPORTANTE: Cada sesion tendra su propio link de Meet (no reutiliza el mismo)")


if __name__ == "__main__":
    main()
