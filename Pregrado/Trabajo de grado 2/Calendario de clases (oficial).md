# Calendario de clases (oficial) — Trabajo de Grado 2 — Modelos de Innovación (Ing. Sistemas)
Plantilla del curso · Horario: **Lunes, 5:00 pm – 6:00 pm (1 hora sincrónica)**
Grupos de este periodo: **54448**
Docente: **Julian Andres Castaño** · julian_castanoe@cun.edu.co

> Si el día de clase es **festivo colombiano**, la sesión se considera **clase autónoma**: la actividad queda en la carpeta de esa sesión del **Drive de clases** (`Clases/Sesion NN - …/`), y la entrega y la nota siguen en **CDigital**.
> Los CSV/ICS de Pregrado **no** incluyen invitados/estudiantes.
> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` (+ ` (autónoma)` si festivo). Fuente: `sesiones_cun.py`.

> **Nota Syllabus:** FALTA SYLLABUS OFICIAL. Temario orientativo — confirmar en Moodle/portal.

**Eventos en plantilla (hasta 22/11/2026):** 15 · **Entradas en catálogo de temas:** 11

> **Evento** = fila del CSV/ICS (incluye las clases autónomas por festivo). **Sesión** = numeración del catálogo, la que usan el guion, el `.pptx` y el Subject de Calendar. En cursos con festivos los dos números NO coinciden.
> La columna **Evaluación (aula CDigital)** marca qué ítem del libro de calificaciones cierra ese día (quices y parciales son cuestionarios y cierran en día de clase). Detalle completo en «Evaluación en el aula» al final de este archivo.

| Evento | Sesión | Fecha | Tipo | Tema (Syllabus / plan) | Evaluación (aula CDigital) |
|---|---|---|---|---|---|
| 1 | **01** | 14/08/2026 (vie) | Sincrónica | Encuadre: Presentación del curso · docente · estudiantes · ACAs | — |
| — | — | (misma semana) | ⚠️ Lectura autónoma | Delimitación / reformulación del tema → lectura autónoma; se retoma al abrir la Sesión 02. (El acuerdo pedagógico se firma en esta sesión de encuadre.) | — |
| 2 | — | 17/08/2026 (lun) | Autónoma (Asunción de la Virgen) | Clase autónoma — continuar avance (festivo: Asunción de la Virgen) | — |
| 3 | **02** | 24/08/2026 (lun) | Sincrónica | Orientativo: Pregunta, objetivos y título provisional | — |
| 4 | **03** | 31/08/2026 (lun) | Sincrónica | Orientativo: Estructura del documento de avance | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 5 | **04** | 07/09/2026 (lun) | Sincrónica | Orientativo: Antecedentes y referentes (Fase I) | — |
| 6 | **05** | 14/09/2026 (lun) | Sincrónica | Orientativo: Marco teórico — avance | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 7 | **06** | 21/09/2026 (lun) | Sincrónica | Orientativo: Marco conceptual y contextual | — |
| 8 | **07** | 28/09/2026 (lun) | Sincrónica | Orientativo: Diseño metodológico (propuesto) | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 9 | **08** | 05/10/2026 (lun) | Sincrónica | Orientativo: Instrumentos y plan de análisis (propuestos) | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 10 | — | 12/10/2026 (lun) | Autónoma (Día de la Raza) | Clase autónoma — continuar avance (festivo: Día de la Raza) | — |
| 11 | **09** | 19/10/2026 (lun) | Sincrónica | Orientativo: Integración del avance · correcciones | — |
| 12 | **10** | 26/10/2026 (lun) | Sincrónica | Orientativo: Socialización de avances | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |
| 13 | — | 02/11/2026 (lun) | Autónoma (Todos los Santos) | Clase autónoma — continuar avance (festivo: Todos los Santos) | — |
| 14 | **11** | 09/11/2026 (lun) | Sincrónica | Orientativo: Cierre del avance · preparación para TG3 | — |
| 15 | — | 16/11/2026 (lun) | Autónoma (Independencia de Cartagena) | Clase autónoma — continuar avance (festivo: Independencia de Cartagena) | — |

## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem

Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/slides/build_pregrado_cursos.py --calendar-only`.

| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |
| :--- | :--- | :---: | ---: | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 31/08/2026 | **S03** — Estructura del documento de avance |
| **Parcial 1** | Cuestionario | 1 | 24% | 14/09/2026 | **S05** — Marco teórico — avance |
| **Quiz 2** | Cuestionario | 2 | 9% | 28/09/2026 | **S07** — Diseño metodológico (propuesto) |
| **Parcial 2** | Cuestionario | 2 | 21% | 05/10/2026 | **S08** — Instrumentos y plan de análisis (propuestos) |
| **ACA Final** | Tarea | 3 | 32,8% | 14/11/2026 | — (no cae en día de clase: es la fecha máxima de recepción de trabajos) |
| **Quiz 3** | Cuestionario | 3 | 4% | 26/10/2026 | **S10** — Socialización de avances |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 22/11/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |
| **Coevaluación** | Foro | 3 | 1,6% | 22/11/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

## Cómo llegan estos encuentros a Calendar

Con `PRINCIPAL - Crear encuentros con invitados.gs`, en `2026/54448/`. Es un Apps Script y es lo único que añade a los estudiantes como **invitados** y deja el **mismo enlace de Meet** en toda la serie. Paso a paso: `LEEME - Crear los eventos de Calendar.md`, en esa misma carpeta.

⚠️ Los `.ics`/`.csv` que hay junto al script llevan el prefijo `RESPALDO sin invitados` porque **Google Calendar descarta los invitados** al importarlos: sirven como respaldo de fechas, no para crear la serie del curso.
