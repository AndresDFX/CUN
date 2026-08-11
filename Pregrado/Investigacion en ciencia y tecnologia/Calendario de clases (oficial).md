# Calendario de clases (oficial) — Investigación Ciencia y Tecnología — Escuela de Ingenierías
Plantilla del curso · Horario: **Jueves, 5:00 pm – 6:00 pm (1 hora sincrónica)**
Grupos de este periodo: **53339**
Docente: **Julian Andres Castaño** · julian_castanoe@cun.edu.co

> Si el día de clase es **festivo colombiano**, la sesión se considera **clase autónoma**: la actividad queda en la carpeta de esa sesión del **Drive de clases** (`Clases/Sesion NN - …/`), y la entrega y la nota siguen en **CDigital**.
> Los CSV/ICS de Pregrado **no** incluyen invitados/estudiantes.
> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo). Fuente: `sesiones_cun.py`.

> **Nota Syllabus:** Numeración del Syllabus salta N° 3 y 9. Periodo corto 26P03: el rango institucional tiene 7 jueves calendario (06/08–17/09), pero el inicio operativo del semestre es el 10/08, así que se dictan **6** (13/08–17/09) y el periodo cierra el 20/09. TEMARIO ADELANTADO (2026-08-11): la ACA Final (el artículo) califica marco teórico y revisión de literatura y cierra el 12/09, así que **U8** (bases de datos CUN y gestores de citas) pasa a la **Sesión 04** y **U10–U12** (posturas teóricas · marco teórico y revisión) a la **Sesión 05**. Ninguna unidad se elimina: es un reorden, no un recorte. La Sesión 06 (17/09) queda como socialización del artículo y cierre, sin evaluación.

**Eventos en plantilla (hasta 20/09/2026):** 6 · **Entradas en catálogo de temas:** 6

> **Evento** = fila del CSV/ICS (incluye las clases autónomas por festivo). **Sesión** = numeración del catálogo, la que usan el guion, el `.pptx` y el Subject de Calendar. En cursos con festivos los dos números NO coinciden.
> La columna **Evaluación (aula CDigital)** marca qué ítem del libro de calificaciones cierra ese día (quices y parciales son cuestionarios y cierran en día de clase). Detalle completo en «Evaluación en el aula» al final de este archivo.

| Evento | Sesión | Fecha | Tipo | Tema (Syllabus / plan) | Evaluación (aula CDigital) |
|---|---|---|---|---|---|
| 1 | **01** | 13/08/2026 (jue) | Sincrónica | Encuadre: Presentación del curso · docente · estudiantes · ACAs | — |
| — | — | (misma semana) | ⚠️ Lectura autónoma | U1–U2 (Syllabus y producto final · fundamentos del método científico) → lectura autónoma; se retoma al abrir la Sesión 02. | — |
| 2 | **02** | 20/08/2026 (jue) | Sincrónica | U4: MinCiencias · 6 líneas de Ingeniería · elección de línea | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 3 | **03** | 27/08/2026 (jue) | Sincrónica | U5: Prueba parcial · 1.er avance del artículo | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 4 | **04** | 03/09/2026 (jue) | Sincrónica | U6+U8: Problema y pregunta · bases de datos y gestores de citas | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 5 | **05** | 10/09/2026 (jue) | Sincrónica | U7+U10–12: Planteamiento del problema · marco teórico y revisión de literatura | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 6 | **06** | 17/09/2026 (jue) | Sincrónica | Cierre: Socialización del artículo y cierre del curso | — |

## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem

Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/slides/build_pregrado_cursos.py --calendar-only`.

| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |
| :--- | :--- | :---: | ---: | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 20/08/2026 | **S02** — MinCiencias · 6 líneas de Ingeniería · elección de línea |
| **Parcial 1** | Cuestionario | 1 | 24% | 27/08/2026 | **S03** — Prueba parcial · 1.er avance del artículo |
| **Quiz 2** | Cuestionario | 2 | 9% | 03/09/2026 | **S04** — Problema y pregunta · bases de datos y gestores de citas |
| **Parcial 2** | Cuestionario | 2 | 21% | 10/09/2026 | **S05** — Planteamiento del problema · marco teórico y revisión de literatura |
| **ACA Final** | Tarea | 3 | 32,8% | 12/09/2026 | — (no cae en día de clase: es la fecha máxima de recepción de trabajos) |
| **Quiz 3** | Cuestionario | 3 | 4% | 12/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 20/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |
| **Coevaluación** | Foro | 3 | 1,6% | 20/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

## Unidades del Syllabus (completas — no se eliminan)

- U1 Presentación del Syllabus y producto final (artículo)
- U2 Fundamentos del método científico
- U4 MinCiencias · 6 líneas de Ingeniería
- U5 Prueba parcial · 1.er avance del artículo
- U6 Identificación de problemas y pregunta
- U7 Formulación del planteamiento del problema
- U8 Bases de datos CUN + gestores de citas
- U10–12 Posturas teóricas · marco teórico y revisión de literatura

## Cómo llegan estos encuentros a Calendar

Con `PRINCIPAL - Crear encuentros con invitados.gs`, en `2026/53339/`. Es un Apps Script y es lo único que añade a los estudiantes como **invitados** y deja el **mismo enlace de Meet** en toda la serie. Paso a paso: `LEEME - Crear los eventos de Calendar.md`, en esa misma carpeta.

⚠️ Los `.ics`/`.csv` que hay junto al script llevan el prefijo `RESPALDO sin invitados` porque **Google Calendar descarta los invitados** al importarlos: sirven como respaldo de fechas, no para crear la serie del curso.
