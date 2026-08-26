# Cambiar link de Meet en eventos existentes — Guía de uso

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