# Crear los eventos de Calendar — PROYECTO I

**Grupo 54ES4** · lunes 20:00–22:00 · **11 encuentros** · **51 estudiantes invitados**

> **Archivo generado — no editar a mano.** Regenerar: `python config/slides/build_calendar_encuentros.py proyecto1`

## Qué vas a conseguir

Los **11 encuentros** del periodo (10/08/2026 → 09/11/2026) en tu Google Calendar, cada uno con **los 51 estudiantes del grupo 54ES4** en la sección *Invitados* y con **el mismo enlace de Google Meet** en todos. Unos cinco minutos. No hay que crear la sala a mano: la crea el propio script.

## ⚠️ Lo primero: no importes el `.ics`

Google Calendar **descarta la lista de invitados** al importar `.ics` y `.csv`. No es un defecto de estos archivos: es cómo Google trata esos formatos. Si importas el `.ics` de esta carpeta te quedan los 11 eventos **con cero de los 51 estudiantes**, y encima ya no puedes usar el script sin borrarlos antes.

> **Si ya creaste los encuentros y lo que buscas es meter matrícula nueva**, no repitas nada de esto: salta a [Llega matrícula nueva](#llega-matrícula-nueva-y-los-encuentros-ya-están-creados). Son dos órdenes, `verificarInvitados()` y `agregarInvitados()`, y no tocan lo que ya está.

Por eso el respaldo se llama `RESPALDO sin invitados - …` y el script `PRINCIPAL - …`. El respaldo está solo por si algún día necesitas las fechas en un calendario que no sea Google. **El flujo bueno es el `.gs`.**

## Qué hay en esta carpeta

| Archivo | Para qué sirve |
|---|---|
| `Actualizar Meet en encuentros (mismo enlace).gs` | Solo si ya habías creado los encuentros ANTES y quieres ponerles el chip nativo de Meet sin borrarlos. Si creas los eventos con el flujo principal, no hace falta. |
| `Correo de bienvenida.docx` | Correo para enviar a los estudiantes el primer día. |
| `Correos estudiantes (invitados Calendar).txt` | Roster en texto plano — de aquí sacó el `.gs` la lista de invitados. |
| `desktop.ini` | — |
| `Entregas y hitos docentes - Importar a Calendar.csv` | Cierres de ACA y hitos del docente. Este **sí** se importa a Calendar: son recordatorios tuyos, sin invitados. |
| `Fechas.txt` | Datos de la oferta del grupo (portal). |
| `Informacion.txt` | Datos de la oferta del grupo (portal). |
| `LEEME - Crear los eventos de Calendar.md` | Este archivo. |
| `Listado estudiantes (CDigital).csv` | Matrícula descargada de CDigital (fuente del roster). |
| `Listado estudiantes.ods` | Carga original del docente, anterior a la auditoría del aula. Se conserva como histórico: el roster vigente es el `(CDigital)`. |
| `PRINCIPAL - Crear encuentros con invitados.gs` | **FLUJO PRINCIPAL.** El único que crea los eventos con invitados y con Meet. |
| `RESPALDO sin invitados - Encuentros Proyecto I - Grupo 54ES4.csv` | ⚠️ **Respaldo de fechas. NO importar** salvo emergencia: Google descarta los invitados al importar `.ics`/`.csv`. |
| `RESPALDO sin invitados - Encuentros Proyecto I - Grupo 54ES4.ics` | ⚠️ **Respaldo de fechas. NO importar** salvo emergencia: Google descarta los invitados al importar `.ics`/`.csv`. |
| `Rompehielos Slido - Sesion 01.md` | — |

## Paso a paso

### 1. Abre Apps Script con la cuenta CUN

**https://script.google.com** con **julian_castanoe@cun.edu.co**. Si entras con otra cuenta, los eventos se crean en el calendario equivocado. **Nuevo proyecto** → borra el `function myFunction()` que trae de fábrica → pega **todo** el contenido de `PRINCIPAL - Crear encuentros con invitados.gs` → guarda. Ponle al proyecto un nombre reconocible (p. ej. «Encuentros Proyecto i 2026»).

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

Este curso **ya tiene sala**: https://meet.google.com/omk-woqk-vsj. El script la reutiliza y no crea otra. Nada que hacer en este paso.

### 6. Remate a mano (lo que la API no puede hacer)

- **Coanfitrión de Meet:** ábrelo en Calendar y añádelo desde la ficha del evento.
- Publica el enlace en el aula de CDigital: https://cdigital.cun.edu.co/course/view.php?id=130378

## Llega matrícula nueva y los encuentros ya están creados

Pasa cada semestre: alguien se matricula tarde, o el aula tenía menos estudiantes que hoy. No hay que borrar ni rehacer los **11 encuentros** ni tocar el Meet. Hay dos órdenes nuevas para esto:

| Ejecuta | Qué hace | Escribe algo |
|---|---|---|
| **`verificarInvitados`** | encuentro por encuentro: a quién le falta invitación y quién está invitado sin estar en el roster | **no** |
| **`agregarInvitados`** | añade solo los que faltan | sí |

Nunca **quitan** a nadie, no crean eventos y no tocan la sala de Meet. Y son idempotentes: si no falta nadie, no hacen nada.

### Vía normal — que entre toda la matrícula de hoy

1. Descarga otra vez el listado del aula y sobrescribe `2026/54ES4/Listado estudiantes (CDigital).csv`.
2. `python config/slides/build_calendar_encuentros.py proyecto1` — el `.gs` sale con el roster nuevo dentro.
3. Pega el `PRINCIPAL - Crear encuentros con invitados.gs` actualizado en el proyecto de Apps Script (reemplaza el que había).
4. **`verificarInvitados`** → lee el registro → **`agregarInvitados`**.

### Vía corta — un solo estudiante

Si es una persona y no quieres regenerar nada, pon su correo arriba del `.gs`:

```js
var NUEVOS = ['nombre.apellido@cun.edu.co'];
```

y ejecuta **`verificarInvitados`** → **`agregarInvitados`**. Con `NUEVOS` puesto, esos son los **únicos** correos que se añaden; el roster del archivo se ignora. Déjalo en `[]` para volver a la vía normal.

### Para qué sirve pasarle el id del Meet

Los encuentros se localizan por el **título**. Si renombraste alguno a mano —o quieres alcanzar una **tutoría** que creaste aparte con la misma sala—, el título ya no cuadra y por ahí no se encuentran. El asidero que sí aguanta es la **sala de Meet**, porque es la misma en toda la serie:

```js
var MEET_ID = 'abc-defg-hij';   // o la URL completa; sale de la barra del navegador
```

Con eso entran también los eventos que no están en la lista de sesiones, y el registro los marca `[FUERA DE SESIONES · lo hallé por el Meet]` para que los veas **antes** de confirmar. Vacío (lo normal), el script usa la sala de este curso (https://meet.google.com/omk-woqk-vsj).

> Si el id que pegas **no** es el de este curso, el registro te lo grita antes de escribir nada: pegar por error el Meet de otra asignatura invitaría a este roster a los encuentros de la otra.

### Dos cosas que conviene saber

- **¿Les llega correo?** Manda `SEND_INVITES`, igual que al crear. En `false` el encuentro les aparece en el calendario sin notificación. Para el que se matricula tarde normalmente **sí** quieres avisarle: ponlo en `true` antes de `agregarInvitados` — pero ojo, entonces el aviso les llega **a todos** los invitados del evento, no solo al nuevo (Google no distingue).
- **Las bajas no se quitan solas.** Si alguien ya no está en el roster, el registro lo lista como «invitados que ya NO están en el roster» y ahí se queda: quitar a una persona de un evento se hace a mano, abriendo el encuentro en Calendar.

## Si algo sale mal

| Lo que ves | Qué pasa y qué haces |
|---|---|
| `verificar()` dice **NO ACTIVADO** | Te saltaste el paso 2. Actívalo y repite. Los eventos se crearían igual, pero sin Meet. |
| Dice «creará UNA sala nueva» y **no querías** | Ya existía sala: pégala primero en `carga_academica_2026.json → cursos.proyecto1.meet`, regenera el `.gs` y vuelve a `verificar()`. |
| «Google aceptó la petición pero todavía no devuelve el enlace» | La sala tarda en aparecer. Espera un minuto y ejecuta `crearEncuentros()` otra vez: no duplica nada. |
| Invitados = **0** en `verificar()` | No se leyó el roster. Revisa `Correos estudiantes (invitados Calendar).txt` en la carpeta del grupo y regenera el `.gs`. |
| Eventos duplicados | Se crearon dos veces con títulos distintos, o se importó el `.ics`. `borrarEncuentros()` limpia los del script; el resto, a mano. |
| «Se ha excedido el tiempo máximo de ejecución» | Vuelve a ejecutar `crearEncuentros()`: continúa donde se quedó. |
| `verificarInvitados()` dice **«No encontré NINGÚN encuentro»** | O no los has creado (`crearEncuentros()`), o los renombraste: pon la sala en `MEET_ID`. |
| `agregarInvitados()` dice **CORTADO por el límite de 6 minutos** | Vuelve a ejecutarlo: sigue por donde se quedó y no invita a nadie dos veces. |
| `MEET_ID = «…» no parece un Meet` | Pega la URL completa o solo el código de tres bloques (`abc-defg-hij`). |
| `NUEVOS tiene N entrada(s) que no son un correo` | Coma o espacio de más al pegar la lista. Corrige y repite: no invitó a nadie. |

## Cómo deshacer

- **`borrarEncuentros()`** — borra solo los eventos cuyo título coincide exactamente con los 11 de esta serie. No toca nada más de tu calendario. Si ya habías puesto `SEND_INVITES = true`, los estudiantes reciben la cancelación.
- **`olvidarSalaMeet()`** — hace que el script olvide la sala que creó, para que la siguiente ejecución genere otra. La sala vieja no se borra de Google, y los eventos ya creados siguen apuntando a ella.
- **Rehacer desde cero:** `borrarEncuentros()` → `olvidarSalaMeet()` → `crearEncuentros()`.
- **`agregarInvitados()` no se deshace en bloque.** Añadir invitados no tiene marcha atrás automática: se quitan a mano en el evento. Por eso `verificarInvitados()` existe y por eso se ejecuta primero.

## Las sesiones que se van a crear

| # | Fecha | Tema | Invitados |
|---|---|---|---|
| 01 | 10/08/2026 (lunes) | Presentación del curso · docente · estudiantes · ACAs | 51 |
| 02 | 24/08/2026 (lunes) | Problema y pregunta de investigación | 51 |
| 03 | 31/08/2026 (lunes) | Objetivos, justificación, alcances y limitaciones | 51 |
| 04 | 07/09/2026 (lunes) | Retroalimentación del Quiz · Antecedentes de investigación | 51 |
| 05 | 14/09/2026 (lunes) | Marco teórico | 51 |
| 06 | 21/09/2026 (lunes) | Marco conceptual y marco contextual | 51 |
| 07 | 28/09/2026 (lunes) | Marco legal · citación APA 7 | 51 |
| 08 | 05/10/2026 (lunes) | Diseño metodológico: paradigma, enfoque y alcance | 51 |
| 09 | 19/10/2026 (lunes) | Devolución de la ACA 1 · población, muestra e instrumentos propuestos | 51 |
| 10 | 26/10/2026 (lunes) | Planeación, viabilidad e integración del anteproyecto | 51 |
| 11 | 09/11/2026 (lunes) | Integración y evaluación · coevaluación y autoevaluación | 51 |

Fechas y temas salen de `config/cursos/sesiones_cun.py`; el roster, de los listados de `2026/<grupo>/`; el enlace de Meet y el aula, de `config/cursos/carga_academica_2026.json`. Si cambia cualquiera de los tres, regenera este `.gs` con `python config/slides/build_calendar_encuentros.py proyecto1`.
