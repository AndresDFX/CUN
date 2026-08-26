# -*- coding: utf-8 -*-
"""Genera el Apps Script para cambiar el link de Meet de eventos existentes.

PROBLEMA:
Los eventos ya están creados pero tienen links de Meet diferentes (uno por sesión), o tienen
un link viejo. Quieres cambiarlos a UN link fijo por curso.

LIMITACIÓN DE GOOGLE CALENDAR:
No se puede cambiar el link de Meet de un evento existente directamente. La única forma es:
1. Eliminar los eventos viejos
2. Recrearlos con el nuevo link de Meet

Este script hace eso: busca eventos por título, guarda sus datos (fecha, hora, participantes),
los elimina y los recrea con el link de Meet que configures.

Uso:
  python config/calendar/build_apps_script_cambiar_link_meet.py

Escribe:
  - PRINCIPAL - Cambiar link de Meet en eventos.gs
  - LEEME - Cambiar link de Meet en eventos.md
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GS_NAME = "PRINCIPAL - Cambiar link de Meet en eventos.gs"
LEEME_NAME = "LEEME - Cambiar link de Meet en eventos.md"

# ── el .gs ─────────────────────────────────────────────────────────────
GS_CONTENT = """/**
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
            descripcionNueva += '\\n\\nEnlace de Meet: ' + cfg.nuevoLinkMeet;
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
""".strip()

# ── el LEEME ───────────────────────────────────────────────────────────
LEEME_CONTENT = """# Cambiar link de Meet en eventos existentes — Guía de uso

Este Apps Script cambia el link de Meet de eventos que ya están creados en Google Calendar.

## Problema que resuelve

Los eventos ya están creados pero:
- Tienen links de Meet diferentes (uno por sesión)
- Tienen un link viejo que quieres cambiar
- Quieres usar UN link fijo para todo el curso

## Cómo funciona

**Limitación de Google Calendar:** No se puede cambiar el link de Meet de un evento existente
directamente.

**Solución:** Este script:
1. Busca eventos por título
2. Guarda sus datos (fecha, hora, participantes, descripción)
3. Los ELIMINA
4. Los RECREA con el nuevo link de Meet que configures

Los participantes reciben una nueva invitación (Google lo hace automáticamente).

## Configuración pre-cargada

El script viene pre-configurado con los 5 cursos de la CUN:
1. Proyecto I
2. Trabajo de Grado 2
3. Trabajo de Grado 3
4. Creatividad y Pensamiento Innovador
5. Investigación Ciencia y Tecnología

Solo tienes que agregar el link de Meet que quieres usar para cada curso.

## Pasos de instalación

### 1. Abre Apps Script

Ve a [script.google.com](https://script.google.com) con tu cuenta (la que tiene los eventos).

### 2. Crea un proyecto nuevo

- Nuevo proyecto
- Pega TODO el contenido de `PRINCIPAL - Cambiar link de Meet en eventos.gs`
- Guarda

### 3. Edita `CONFIG_CURSOS`

Por cada curso, pega el link de Meet:

```javascript
{
  tituloContiene: "Trabajo de Grado 3",  // fragmento del título
  nuevoLinkMeet: "https://meet.google.com/abc-defg-hij"  // <- link fijo
}
```

**Cómo obtener el link de Meet:**
- Opción 1: Usa el link de un evento existente (si hay uno que quieres reutilizar)
- Opción 2: Crea una sala permanente en [meet.google.com](https://meet.google.com) → "Nueva reunión" → copia el link

### 4. (Opcional) Configura el rango de fechas

Si solo quieres cambiar eventos de un periodo específico:

```javascript
var FECHA_DESDE = '2026-08-01';
var FECHA_HASTA = '2026-12-31';
```

Si los dejas vacíos, cambia TODOS los eventos que encuentre (últimos 2 años + próximos 2 años).

### 5. Verifica (solo lectura)

Ejecuta `verificarEventos()`:
- Botón ▶️ arriba, elige `verificarEventos`
- La primera vez pedirá permisos
- Lee TODO el registro: te dice cuántos eventos encontró y cuál es el nuevo link

### 6. Ejecuta una vez a mano

**⚠️ IMPORTANTE: Los eventos se eliminan y recrean. Las invitaciones se reenvían.**

Si el paso anterior cuadra:
1. Cambia `SIMULAR = true` por `SIMULAR = false`
2. Guarda
3. Ejecuta `cambiarLinkMeet()` UNA vez
4. Lee el registro: debe decir "✓ ACTUALIZADO:" por cada evento

## Funciones disponibles

| Función | Qué hace |
|:--|:--|
| `verificarEventos()` | Solo lectura. Dice qué haría sin cambiar nada. |
| `cambiarLinkMeet()` | Cambia el link (respeta `SIMULAR`). |

## Ejemplo: Cambiar el link de TG3

```javascript
var CONFIG_CURSOS = [
  {
    tituloContiene: "Trabajo de Grado 3",
    nuevoLinkMeet: "https://meet.google.com/xyz-abcd-efg"
  }
];

var SIMULAR = false;  // <- cambiar a false después de verificar
var FECHA_DESDE = '2026-08-01';
var FECHA_HASTA = '2026-12-31';
```

Ejecutas `cambiarLinkMeet()` → TODOS los eventos de TG3 entre esas fechas se recrean con el
nuevo link.

## Importante

### Los eventos se recrean
- Los IDs de los eventos cambian
- Los participantes reciben una nueva invitación por correo
- Si tenían respuestas (Sí/No/Tal vez), se pierden

### El link viejo sigue funcionando
- Si alguien guardó el link viejo, todavía funciona
- Pero NO lleva al evento nuevo — lleva a una sala vacía

### Notificaciones
- Google envía correo a cada participante diciendo que el evento cambió
- No se puede silenciar

## Cambiar el link de un solo curso

Edita `CONFIG_CURSOS` y deja el `nuevoLinkMeet` de los otros cursos en `""` (vacío). El script
solo procesa los que tienen link configurado.

## Deshacer

**No hay forma de deshacer automáticamente** porque los eventos se eliminan. Si te equivocaste:
1. Vuelve a ejecutar el script con el link que querías
2. O recrea los eventos manualmente

Por eso es importante **simular primero** y leer el registro completo.

## Calendario compartido

Si los eventos están en un calendario compartido:

1. Abre el calendario en Google Calendar
2. Configuración → nombre del calendario → "Integrar calendario" → copia el ID
3. Pega el ID en `CALENDARIO_ID`:
   ```javascript
   var CALENDARIO_ID = 'abc123@group.calendar.google.com';
   ```

Por defecto usa `'primary'` (tu calendario principal).

## Dónde están los archivos

- Generador: `config/calendar/build_apps_script_cambiar_link_meet.py`
- .gs generado: `PRINCIPAL - Cambiar link de Meet en eventos.gs`
- Este LEEME: `LEEME - Cambiar link de Meet en eventos.md`

Regenerar:
```bash
python config/calendar/build_apps_script_cambiar_link_meet.py
```

## Versión y autoría

**v1 — 26/08/2026**
Para cambiar el link de Meet de eventos existentes. Pre-configurado con los 5 cursos de la CUN.

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
    print("Proximos pasos:")
    print("1. Abre script.google.com con tu cuenta")
    print(f"2. Nuevo proyecto -> pega el contenido de '{GS_NAME}'")
    print("3. Edita CONFIG_CURSOS: por cada curso, pega el nuevo link de Meet")
    print("4. Ejecuta verificarEventos() -> si cuadra, SIMULAR=false -> cambiarLinkMeet()")
    print()
    print("IMPORTANTE: Los eventos se ELIMINAN y RECREAN con el nuevo link")


if __name__ == "__main__":
    main()
