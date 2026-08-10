# Calendario de clases (oficial) — Creatividad y Pensamiento Innovador — Escuela de Ingenierías
Plantilla del curso · Horario: **Miércoles, 5:00 pm – 6:00 pm (1 hora sincrónica)**
Grupos de este periodo: **54408**
Docente: **Julian Andres Castaño** · julian_castanoe@cun.edu.co

> Si el día de clase es **festivo colombiano**, la sesión se considera **clase autónoma** (actividad en CDigital).
> Los CSV/ICS de Pregrado **no** incluyen invitados/estudiantes.
> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo). Fuente: `sesiones_cun.py`.

**Eventos en plantilla (hasta 27/09/2026):** 7 · **Entradas en catálogo de temas:** 7

> **Evento** = fila del CSV/ICS (incluye las clases autónomas por festivo). **Sesión** = numeración del catálogo, la que usan el guion, el `.pptx` y el Subject de Calendar. En cursos con festivos los dos números NO coinciden.
> La columna **Evaluación (aula CDigital)** marca qué ítem del libro de calificaciones cierra ese día (quices y parciales son cuestionarios y cierran en día de clase). Detalle completo en «Evaluación en el aula» al final de este archivo.

| Evento | Sesión | Fecha | Tipo | Tema (Syllabus / plan) | Evaluación (aula CDigital) |
|---|---|---|---|---|---|
| 1 | **01** | 12/08/2026 (mié) | Sincrónica | Encuadre: Presentación del curso · docente · estudiantes · ACAs | — |
| — | — | (misma semana) | ⚠️ Lectura autónoma | U1–U2 (Propuesta de Innovación · creatividad e inteligencia emocional) → lectura autónoma; se retoma al abrir la Sesión 02. | — |
| 2 | **02** | 19/08/2026 (mié) | Sincrónica | U3: Creatividad/innovación en I+D · Design Thinking y técnicas | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 3 | **03** | 26/08/2026 (mié) | Sincrónica | U4: Gestión de la innovación (Manual de Oslo / OCDE) | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 4 | **04** | 02/09/2026 (mié) | Sincrónica | U5: Tipos de innovación | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 5 | **05** | 09/09/2026 (mié) | Sincrónica | U6: Análisis de negocios · validación de la propuesta | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 6 | **06** | 16/09/2026 (mié) | Sincrónica | U7: Vigilancia tecnológica | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |
| 7 | **07** | 23/09/2026 (mié) | Sincrónica | U8: Innovación local–internacional · entidades de apoyo | — |

## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem

Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/slides/build_pregrado_cursos.py --calendar-only`.

| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |
| :--- | :--- | :---: | ---: | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 19/08/2026 | **S02** — Creatividad/innovación en I+D · Design Thinking y técnicas |
| **Parcial 1** | Cuestionario | 1 | 24% | 26/08/2026 | **S03** — Gestión de la innovación (Manual de Oslo / OCDE) |
| **Quiz 2** | Cuestionario | 2 | 9% | 02/09/2026 | **S04** — Tipos de innovación |
| **Parcial 2** | Cuestionario | 2 | 21% | 09/09/2026 | **S05** — Análisis de negocios · validación de la propuesta |
| **ACA Final** | Tarea | 3 | 32,8% | 19/09/2026 | — (no cae en día de clase: es la fecha máxima de recepción de trabajos) |
| **Quiz 3** | Cuestionario | 3 | 4% | 16/09/2026 | **S06** — Vigilancia tecnológica |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 27/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |
| **Coevaluación** | Foro | 3 | 1,6% | 27/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

Los CSV/ICS con el/los códigos de grupo en el título del evento viven en `2026/<grupo>/` (y, si varios grupos comparten horario y cierre, también puede generarse un archivo combinado).
