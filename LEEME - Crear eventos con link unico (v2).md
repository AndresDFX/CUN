# Crear eventos en Calendar con link único de Meet — Guía de uso v2

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