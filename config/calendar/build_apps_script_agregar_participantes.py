# -*- coding: utf-8 -*-
"""Genera el Apps Script para agregar participantes a eventos de Calendar de un curso.

El script busca eventos de Calendar por título (ej: contiene "Trabajo de grado 3") y agrega
una lista de correos como invitados a TODOS los eventos que coincidan. Sirve para:
- Agregar estudiantes nuevos a todas las sesiones de un curso
- Agregar observadores, tutores o jurados
- Corregir cuando faltaron invitados en la creación inicial

Uso:
  python config/calendar/build_apps_script_agregar_participantes.py

Escribe:
  - PRINCIPAL - Agregar participantes a eventos.gs
  - LEEME - Agregar participantes a eventos.md
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GS_NAME = "PRINCIPAL - Agregar participantes a eventos.gs"
LEEME_NAME = "LEEME - Agregar participantes a eventos.md"

# ── el .gs ─────────────────────────────────────────────────────────────
GS_CONTENT = """/**
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
""".strip()

# ── el LEEME ───────────────────────────────────────────────────────────
LEEME_CONTENT = """# Agregar participantes a eventos de Calendar — Guía de uso

Este Apps Script busca eventos en tu Google Calendar por título y agrega una lista de correos
como invitados a TODOS los eventos que coincidan.

## Para qué sirve

- Agregar estudiantes nuevos a todas las sesiones de un curso
- Agregar observadores, tutores o jurados a eventos ya creados
- Corregir cuando faltaron invitados en la creación inicial de eventos
- Agregar participantes a múltiples cursos a la vez

## Cómo funciona

1. Buscas eventos por fragmento del título (ej: "Trabajo de grado 3")
2. Defines una lista de correos a agregar
3. El script agrega esos correos como invitados a TODOS los eventos que coincidan
4. Si un correo ya está invitado, no lo duplica

## Pasos de instalación

### 1. Abre Apps Script

Ve a [script.google.com](https://script.google.com) con tu cuenta (la que tiene los eventos).

### 2. Crea un proyecto nuevo

- Nuevo proyecto
- Pega TODO el contenido de `PRINCIPAL - Agregar participantes a eventos.gs`
- Guarda (le pone nombre automáticamente)

### 3. Edita `CONFIG_EVENTOS`

Al principio del archivo (línea ~30) hay un arreglo. Por cada curso:

```javascript
{
  tituloContiene: "Trabajo de grado 3",  // <- fragmento del título del evento
  participantes: [
    "estudiante1@cun.edu.co",  // <- correos, uno por línea
    "estudiante2@cun.edu.co",
    "estudiante3@cun.edu.co"
  ]
}
```

**Cómo obtener los correos:**
- Si están en una hoja de cálculo: copia la columna y pégala aquí con comillas y comas
- Si están en un archivo de texto: un correo por línea, con comillas y comas

### 4. (Opcional) Configura el rango de fechas

Si solo quieres agregar participantes a eventos de un periodo específico:

```javascript
var FECHA_DESDE = '2026-08-01';  // eventos desde esta fecha
var FECHA_HASTA = '2026-12-31';  // hasta esta fecha
```

Si los dejas vacíos, busca en todo el calendario (últimos 2 años + próximos 2 años).

### 5. Verifica (solo lectura)

Ejecuta la función `verificarEventos()`:
- Botón ▶️ arriba, elige `verificarEventos`
- La primera vez pedirá permisos (Autorizar → elige tu cuenta → Avanzado → Ir a [nombre])
- Lee TODO el registro: te dice cuántos eventos encontró y cuántos participantes va a agregar

### 6. Ejecuta una vez a mano

Si el paso anterior cuadra:
1. Cambia `SIMULAR = true` por `SIMULAR = false` (línea ~53)
2. Guarda
3. Ejecuta `agregarParticipantes()` UNA vez
4. Lee el registro: debe decir "✓ AGREGADO:" por cada correo

## Funciones disponibles

| Función | Qué hace |
|:--|:--|
| `verificarEventos()` | Solo lectura. Dice qué haría sin agregar nada. |
| `agregarParticipantes()` | Agrega los participantes (respeta `SIMULAR`). |
| `quitarParticipantes()` | Quita los participantes configurados de todos los eventos. |

## Cómo agregar estudiantes de otro curso

1. Abre el proyecto en Apps Script
2. Edita `CONFIG_EVENTOS`: agrega una entrada más
3. Guarda
4. Ejecuta `verificarEventos()` para comprobar
5. Si cuadra: `SIMULAR = false` → `agregarParticipantes()`

**No hace falta regenerar nada**: editas directo en Apps Script.

## Ejemplo: Agregar 3 estudiantes a TG3

```javascript
var CONFIG_EVENTOS = [
  {
    tituloContiene: "Trabajo de grado 3",
    participantes: [
      "maria.lopez@cun.edu.co",
      "juan.perez@cun.edu.co",
      "ana.garcia@cun.edu.co"
    ]
  }
];

var SIMULAR = false;  // <- cambiar a false después de verificar
var FECHA_DESDE = '2026-08-01';
var FECHA_HASTA = '2026-12-31';
```

Ejecutas `agregarParticipantes()` → los 3 correos se agregan a TODOS los eventos de TG3 entre
esas fechas.

## Deshacer

Si te equivocaste y quieres quitar los participantes:

1. Deja `CONFIG_EVENTOS` como está (con los correos que quieres quitar)
2. Pon `SIMULAR = false`
3. Ejecuta `quitarParticipantes()`

Quita los correos configurados de todos los eventos donde estén presentes.

## Limitaciones

- **Eventos recurrentes:** cada ocurrencia se trata por separado. Si quieres agregar a TODAS las
  ocurrencias de una serie, tendrás muchas entradas en el log.
- **Permisos de Calendar:** si usas un calendario compartido, asegúrate de tener permisos para
  modificar eventos.
- **Notificaciones:** Google envía correo de invitación a cada participante agregado. No hay forma
  de silenciar eso desde Apps Script.

## Calendario compartido

Si los eventos están en un calendario compartido (no en tu calendario principal):

1. Abre el calendario en Google Calendar
2. Configuración → nombre del calendario → "Integrar calendario" → copia el ID del calendario
3. Pega el ID en `CALENDARIO_ID`:
   ```javascript
   var CALENDARIO_ID = 'abc123@group.calendar.google.com';
   ```

Por defecto usa `'primary'` (tu calendario principal).

## Dónde están los archivos

- Generador: `config/calendar/build_apps_script_agregar_participantes.py`
- .gs generado: `PRINCIPAL - Agregar participantes a eventos.gs`
- Este LEEME: `LEEME - Agregar participantes a eventos.md`

Regenerar:
```bash
python config/calendar/build_apps_script_agregar_participantes.py
```

## Versión y autoría

**v1 — 26/08/2026**
Script parametrizable para agregar participantes a eventos de Calendar.

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
    print("3. Edita CONFIG_EVENTOS: por cada curso, el título y los correos a agregar")
    print("4. Ejecuta verificarEventos() -> si cuadra, SIMULAR=false -> agregarParticipantes()")


if __name__ == "__main__":
    main()
