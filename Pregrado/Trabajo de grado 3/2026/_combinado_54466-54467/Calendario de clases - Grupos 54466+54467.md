# Calendario — Trabajo de Grado 3 — Modelos de Innovación (Ing. Sistemas)
**Grupos 54466 / 54467** · Horario: **Martes, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela).
> CSV/ICS **sin invitados** estudiantes. Description corta; Location vacío hasta Meet real.

| # | Fecha | Tipo | Subject (Calendar) | Evaluación (aula CDigital) |
|---|---|---|---|---|
| 1 | 11/08/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 01 | — |
| 2 | 18/08/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 02 | — |
| 3 | 25/08/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 03 | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 4 | 01/09/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 04 | — |
| 5 | 08/09/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 05 | — |
| 6 | 15/09/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 06 | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 7 | 22/09/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 07 | — |
| 8 | 29/09/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 08 | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 9 | 06/10/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 09 | — |
| 10 | 13/10/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 10 | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 11 | 20/10/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 11 | — |
| 12 | 27/10/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 12 | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |
| 13 | 03/11/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 13 | — |
| 14 | 10/11/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 14 | — |
| 15 | 17/11/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 15 | — |

## Fechas institucionales
- **54466** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**
- **54467** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**
- Cierre considerado en este archivo Calendar: **22/11/2026**
- Eventos generados: **15**
- Archivos: `Encuentros TRABAJO DE GRADO 3 - Grupos 54466+54467 - Importar a Calendar.csv` / `Encuentros TRABAJO DE GRADO 3 - Grupos 54466+54467 - Importar a Calendar.ics`

## Cómo importar (sin invitados · description corta)
1. Google Calendar → Configuración → Importar → `.ics` o `.csv`.
2. **No incluye estudiantes** (Pregrado no lleva Guests/ATTENDEE).
3. Location vacío: tras importar, añade Meet (mismo enlace en toda la serie) y publícalo en CDigital.
4. Subject corto: grupos - asignatura - Sesion NN. Description = una línea con el tema.
5. Placeholder Meet de referencia (no va en el ICS): [URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 3].

## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem

Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/slides/build_pregrado_cursos.py --calendar-only`.

| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |
| :--- | :--- | :---: | ---: | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 25/08/2026 | **S03** — Estructura del artículo · taller de introducción |
| **Parcial 1** | Cuestionario | 1 | 24% | 15/09/2026 | **S06** — Comunidades de práctica y co-creación |
| **Quiz 2** | Cuestionario | 2 | 9% | 29/09/2026 | **S08** — Fase III de referentes · cierre del marco teórico |
| **Parcial 2** | Cuestionario | 2 | 21% | 13/10/2026 | **S10** — Resumen, palabras clave UNESCO, conclusiones y referencias |
| **ACA Final** | Tarea | 3 | 32% | 14/11/2026 | — (no cae en día de clase: es la fecha máxima de recepción de trabajos) |
| **Quiz 3** | Cuestionario | 3 | 4% | 27/10/2026 | **S12** — Sustentación ante jurados |
| **Autoevaluación** | Cuestionario | 3 | 2% | 22/11/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |
| **Coevaluación** | Foro | 3 | 2% | 22/11/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32% + Quiz 3 4% + Autoevaluación 2% + Coevaluación 2%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
