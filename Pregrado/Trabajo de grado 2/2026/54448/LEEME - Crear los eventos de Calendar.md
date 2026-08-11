# Crear los eventos de Calendar — TRABAJO DE GRADO 2

**Grupo 54448** · viernes 17:00–18:00 · **11 encuentros** · **50 estudiantes invitados**

> **Archivo generado — no editar a mano.** Regenerar: `python config/slides/build_calendar_encuentros.py tg2`

## Qué vas a conseguir

Los **11 encuentros** del periodo (14/08/2026 → 09/11/2026) en tu Google Calendar, cada uno con **los 50 estudiantes del grupo 54448** en la sección *Invitados* y con **el mismo enlace de Google Meet** en todos. Unos cinco minutos. No hay que crear la sala a mano: la crea el propio script.

## ⚠️ Lo primero: no importes el `.ics`

Google Calendar **descarta la lista de invitados** al importar `.ics` y `.csv`. No es un defecto de estos archivos: es cómo Google trata esos formatos. Si importas el `.ics` de esta carpeta te quedan los 11 eventos **con cero de los 50 estudiantes**, y encima ya no puedes usar el script sin borrarlos antes.

Por eso el respaldo se llama `RESPALDO sin invitados - …` y el script `PRINCIPAL - …`. El respaldo está solo por si algún día necesitas las fechas en un calendario que no sea Google. **El flujo bueno es el `.gs`.**

## Qué hay en esta carpeta

| Archivo | Para qué sirve |
|---|---|
| `Calendario de clases - Grupo 54448.md` | Referencia: el cronograma en tabla. No se importa: se lee. |
| `Correo de bienvenida.docx` | Correo para enviar a los estudiantes el primer día. |
| `Correos estudiantes (invitados Calendar).txt` | Roster en texto plano — de aquí sacó el `.gs` la lista de invitados. |
| `Entregas y hitos docentes - Importar a Calendar.csv` | Cierres de ACA y hitos del docente. Este **sí** se importa a Calendar: son recordatorios tuyos, sin invitados. |
| `Informacion.txt` | Datos de la oferta del grupo (portal). |
| `LEEME - Crear los eventos de Calendar.md` | Este archivo. |
| `Listado estudiantes (CDigital).csv` | Matrícula descargada de CDigital (fuente del roster). |
| `PRINCIPAL - Crear encuentros con invitados.gs` | **FLUJO PRINCIPAL.** El único que crea los eventos con invitados y con Meet. |
| `RESPALDO sin invitados - Encuentros TRABAJO DE GRADO 2 - Grupo 54448.csv` | ⚠️ **Respaldo de fechas. NO importar** salvo emergencia: Google descarta los invitados al importar `.ics`/`.csv`. |
| `RESPALDO sin invitados - Encuentros TRABAJO DE GRADO 2 - Grupo 54448.ics` | ⚠️ **Respaldo de fechas. NO importar** salvo emergencia: Google descarta los invitados al importar `.ics`/`.csv`. |
| `Rompehielos Slido - Sesion 01.md` | — |

## Paso a paso

### 1. Abre Apps Script con la cuenta CUN

**https://script.google.com** con **julian_castanoe@cun.edu.co**. Si entras con otra cuenta, los eventos se crean en el calendario equivocado. **Nuevo proyecto** → borra el `function myFunction()` que trae de fábrica → pega **todo** el contenido de `PRINCIPAL - Crear encuentros con invitados.gs` → guarda. Ponle al proyecto un nombre reconocible (p. ej. «Encuentros Trabajo de grado 2 2026»).

### 2. Activa el servicio avanzado de Calendar (30 segundos)

Es lo que le permite al script **crear la sala de Meet**. Sin esto los eventos se crean igual y con invitados, pero sin videoconferencia.

1. En el panel izquierdo del editor, junto a **Servicios**, pulsa **+**.
2. Busca **Google Calendar API** en la lista.
3. Deja el identificador que propone (`Calendar`) y la versión **v3**.
4. **Añadir**. Debe quedar «Calendar» listado bajo *Servicios*.

### 3. Ejecuta `verificar()` — siempre, antes que nada

Elige la función **`verificar`** en la barra superior y pulsa **Ejecutar**.

La primera vez Google pide permisos: **Revisar permisos** → tu cuenta CUN → «Google no ha verificado esta aplicación» → **Configuración avanzada** → **Ir a (nombre del proyecto)** → **Permitir**. Es tu propio script; el aviso sale porque no está publicado.

`verificar()` **no crea, no modifica y no borra nada**. Solo escribe en el registro (*Ver → Registro de ejecución*):

- en qué calendario va a trabajar — comprueba que es el tuyo de CUN;
- las **11 sesiones**, con fecha, título del evento y cuántos invitados lleva cada una;
- si alguna **ya existe** (entonces no se duplicará);
- si el servicio avanzado está activado;
- **qué va a pasar con el Meet**: si reutiliza una sala existente o si va a crear una.

Si algo no cuadra —calendario equivocado, invitados a cero, fechas raras— párate aquí: todavía no has tocado nada.

### 4. Ejecuta `crearEncuentros()`

Crea los **11 eventos** con sus invitados y después pone la misma sala de Meet en todos. Tarda un poco: la creación de la sala es asíncrona y el script espera a que Google devuelva el enlace.

- **`SEND_INVITES = false`** (primera línea de configuración del `.gs`): los estudiantes **no** reciben correo todavía. Los eventos les aparecen en el calendario, pero sin notificación. Déjalo así mientras revisas; ponlo en `true` y vuelve a ejecutar solo cuando quieras avisarles.
- **Es idempotente:** volver a ejecutarlo no duplica eventos (los reconoce por título y fecha) ni crea una segunda sala (la recuerda en las propiedades del proyecto).

### 5. Lleva la URL de Meet al material

El registro te va a mostrar un recuadro así:

```
  +--------------------------------------------------------------
  | SALA DE MEET CREADA: https://meet.google.com/xxx-xxxx-xxx
  | Es la de las 11 sesiones. Cópiala y pégala en el material:
  |   config/cursos/carga_academica_2026.json -> cursos.tg2.meet
  +--------------------------------------------------------------
```

**Hazlo.** Abre `config/cursos/carga_academica_2026.json`, busca `"tg2"` y pon esa URL en su campo `"meet"` (hoy está vacío). Después regenera el material:

```
python config/slides/build_pregrado_cursos.py --calendar-only
python config/slides/build_correo_bienvenida.py
python config/slides/build_calendar_encuentros.py tg2
```

Mientras ese campo siga vacío, el **correo de bienvenida**, el **LEEME del estudiante** y el calendario del curso muestran el marcador de posición `[URL Meet — mismo enlace toda la serie · …]` en vez del enlace de verdad. Es el único paso manual que queda.

### 6. Remate a mano (lo que la API no puede hacer)

- **Coanfitrión de Meet:** ábrelo en Calendar y añádelo desde la ficha del evento.
- Publica el enlace en el aula de CDigital: https://cdigital.cun.edu.co/course/view.php?id=129268

## Si algo sale mal

| Lo que ves | Qué pasa y qué haces |
|---|---|
| `verificar()` dice **NO ACTIVADO** | Te saltaste el paso 2. Actívalo y repite. Los eventos se crearían igual, pero sin Meet. |
| Dice «creará UNA sala nueva» y **no querías** | Ya existía sala: pégala primero en `carga_academica_2026.json → cursos.tg2.meet`, regenera el `.gs` y vuelve a `verificar()`. |
| «Google aceptó la petición pero todavía no devuelve el enlace» | La sala tarda en aparecer. Espera un minuto y ejecuta `crearEncuentros()` otra vez: no duplica nada. |
| Invitados = **0** en `verificar()` | No se leyó el roster. Revisa `Correos estudiantes (invitados Calendar).txt` en la carpeta del grupo y regenera el `.gs`. |
| Eventos duplicados | Se crearon dos veces con títulos distintos, o se importó el `.ics`. `borrarEncuentros()` limpia los del script; el resto, a mano. |
| «Se ha excedido el tiempo máximo de ejecución» | Vuelve a ejecutar `crearEncuentros()`: continúa donde se quedó. |

## Cómo deshacer

- **`borrarEncuentros()`** — borra solo los eventos cuyo título coincide exactamente con los 11 de esta serie. No toca nada más de tu calendario. Si ya habías puesto `SEND_INVITES = true`, los estudiantes reciben la cancelación.
- **`olvidarSalaMeet()`** — hace que el script olvide la sala que creó, para que la siguiente ejecución genere otra. La sala vieja no se borra de Google, y los eventos ya creados siguen apuntando a ella.
- **Rehacer desde cero:** `borrarEncuentros()` → `olvidarSalaMeet()` → `crearEncuentros()`.

## Las sesiones que se van a crear

| # | Fecha | Tema | Invitados |
|---|---|---|---|
| 01 | 14/08/2026 (viernes) | Presentación del curso · docente · estudiantes · ACAs | 50 |
| 02 | 24/08/2026 (lunes) | Pregunta, objetivos y título provisional | 50 |
| 03 | 31/08/2026 (lunes) | Estructura del documento / artículo de avance | 50 |
| 04 | 07/09/2026 (lunes) | Antecedentes y referentes (Fase I) | 50 |
| 05 | 14/09/2026 (lunes) | Marco teórico — avance | 50 |
| 06 | 21/09/2026 (lunes) | Marco conceptual y contextual | 50 |
| 07 | 28/09/2026 (lunes) | Diseño metodológico (propuesto) | 50 |
| 08 | 05/10/2026 (lunes) | Instrumentos y plan de análisis (propuestos) | 50 |
| 09 | 19/10/2026 (lunes) | Integración del avance · correcciones | 50 |
| 10 | 26/10/2026 (lunes) | Socialización de avances | 50 |
| 11 | 09/11/2026 (lunes) | Cierre del avance · preparación para TG3 | 50 |

Fechas y temas salen de `config/cursos/sesiones_cun.py`; el roster, de los listados de `2026/<grupo>/`; el enlace de Meet y el aula, de `config/cursos/carga_academica_2026.json`. Si cambia cualquiera de los tres, regenera este `.gs` con `python config/slides/build_calendar_encuentros.py tg2`.
