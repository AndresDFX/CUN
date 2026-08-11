# Calendario de clases (oficial) — Trabajo de Grado 3 — Modelos de Innovación (Ing. Sistemas)
Plantilla del curso · Horario: **Martes, 5:00 pm – 6:00 pm (1 hora sincrónica)**
Grupos de este periodo: **54450, 54466, 54467**
Docente: **Julian Andres Castaño** · julian_castanoe@cun.edu.co

> Si el día de clase es **festivo colombiano**, la sesión se considera **clase autónoma**: la actividad queda en la carpeta de esa sesión del **Drive de clases** (`Clases/Sesion NN - …/`), y la entrega y la nota siguen en **CDigital**.
> Los CSV/ICS de Pregrado **no** incluyen invitados/estudiantes.
> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo). Fuente: `sesiones_cun.py`.

## Cierres por grupo (fuente oficial)
- **54450** (26P04): inicio 10/08/2026 · recepción 07/11/2026 · cierre **15/11/2026**
- **54466** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**
- **54467** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**

> Esta plantilla lista fechas hasta el cierre más largo (**22/11/2026**). Cada carpeta `2026/<grupo>/` recorta al cierre de ese grupo.

**Eventos en plantilla (hasta 22/11/2026):** 15 · **Entradas en catálogo de temas:** 15

> **Evento** = fila del CSV/ICS (incluye las clases autónomas por festivo). **Sesión** = numeración del catálogo, la que usan el guion, el `.pptx` y el Subject de Calendar. En cursos con festivos los dos números NO coinciden.
> La columna **Evaluación (aula CDigital)** marca qué ítem del libro de calificaciones cierra ese día (quices y parciales son cuestionarios y cierran en día de clase). Detalle completo en «Evaluación en el aula» al final de este archivo.

| Evento | Sesión | Fecha | Tipo | Tema (Syllabus / plan) | Evaluación (aula CDigital) |
|---|---|---|---|---|---|
| 1 | **01** | 11/08/2026 (mar) | Sincrónica | Encuadre: Presentación del curso · docente · estudiantes · ACAs | — |
| — | — | (misma semana) | ⚠️ Lectura autónoma | U1–U2 (Casos de éxito · retomar proyecto · contexto y planteamiento) → lectura autónoma; se retoma al abrir la Sesión 02. (El acuerdo pedagógico se firma en esta sesión de encuadre.) | — |
| 2 | **02** | 18/08/2026 (mar) | Sincrónica | U3: Formulación de pregunta, objetivos y título | — |
| 3 | **03** | 25/08/2026 (mar) | Sincrónica | U4: Estructura del artículo · taller de introducción | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 4 | **04** | 01/09/2026 (mar) | Sincrónica | U5: Fase I de referentes de investigación | — |
| 5 | **05** | 08/09/2026 (mar) | Sincrónica | U6: Diseño de instrumento · desarrollo metodológico | — |
| 6 | **06** | 15/09/2026 (mar) | Sincrónica | U7: Comunidades de práctica y co-creación | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 7 | **07** | 22/09/2026 (mar) | Sincrónica | U8: Experiencia creativa · análisis de datos | — |
| 8 | **08** | 29/09/2026 (mar) | Sincrónica | U9: Fase III de referentes · cierre del marco teórico | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 9 | **09** | 06/10/2026 (mar) | Sincrónica | U10: Resultados, discusión y relación con referentes | — |
| 10 | **10** | 13/10/2026 (mar) | Sincrónica | U11: Resumen, palabras clave UNESCO, conclusiones y referencias | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 11 | **11** | 20/10/2026 (mar) | Sincrónica | U12: Póster · evidencias · verificación antiplagio | — |
| 12 | **12** | 27/10/2026 (mar) | Sincrónica | U13: Sustentación ante jurados | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |
| 13 | **13** | 03/11/2026 (mar) | Sincrónica | U14: Entregables para repositorio institucional | — |
| 14 | **14** | 10/11/2026 (mar) | Sincrónica | Buffer: Ajustes finales · seguimiento post-sustentación | **Cierra la ventana de Autoevaluación** (cuestionario · 2% · corte 3) · **Cierra la ventana de Coevaluación** (foro · 2% · corte 3) |
| 15 | **15** | 17/11/2026 (mar) | Sincrónica | Buffer: Cierre administrativo · recepción de entregables | — |

## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem

Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/slides/build_pregrado_cursos.py --calendar-only`.

| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |
| :--- | :--- | :---: | ---: | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 25/08/2026 | **S03** — Estructura del artículo · taller de introducción |
| **Parcial 1** | Cuestionario | 1 | 24% | 15/09/2026 | **S06** — Comunidades de práctica y co-creación |
| **Quiz 2** | Cuestionario | 2 | 9% | 29/09/2026 | **S08** — Fase III de referentes · cierre del marco teórico |
| **Parcial 2** | Cuestionario | 2 | 21% | 13/10/2026 | **S10** — Resumen, palabras clave UNESCO, conclusiones y referencias |
| **ACA Final** | Tarea | 3 | 32% | 07/11/2026 | — (no cae en día de clase: es la fecha máxima de recepción de trabajos) |
| **Quiz 3** | Cuestionario | 3 | 4% | 27/10/2026 | **S12** — Sustentación ante jurados |
| **Autoevaluación** | Cuestionario | 3 | 2% | 10/11/2026 | **S14** — Ajustes finales · seguimiento post-sustentación |
| **Coevaluación** | Foro | 3 | 2% | 10/11/2026 | **S14** — Ajustes finales · seguimiento post-sustentación |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32% + Quiz 3 4% + Autoevaluación 2% + Coevaluación 2%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

## Cómo llegan estos encuentros a Calendar

Con `PRINCIPAL - Crear encuentros con invitados (3 grupos).gs`, en `2026/_combinado_todos/` — los tres grupos son **una sola serie** (mismo horario y misma sala de Meet), así que hay un único script y un único juego de eventos para 54450, 54466 y 54467. Es un Apps Script y es lo único que añade a los estudiantes como **invitados** y deja el **mismo enlace de Meet** en toda la serie. Paso a paso: `LEEME - Crear los eventos de Calendar.md`, en esa misma carpeta.

⚠️ Los `.ics`/`.csv` que hay junto al script llevan el prefijo `RESPALDO sin invitados` porque **Google Calendar descarta los invitados** al importarlos: sirven como respaldo de fechas, no para crear la serie del curso.
