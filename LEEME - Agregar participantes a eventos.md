# Agregar participantes a eventos de Calendar — Guía de uso

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