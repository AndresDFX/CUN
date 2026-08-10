# Calendario — Investigación Ciencia y Tecnología — Escuela de Ingenierías
**Grupo 53339** · Horario: **Jueves, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela).
> CSV/ICS **sin invitados** estudiantes. Description corta; Location vacío hasta Meet real.

| # | Fecha | Tipo | Subject (Calendar) | Evaluación (aula CDigital) |
|---|---|---|---|---|
| 1 | 13/08/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 01 | — |
| 2 | 20/08/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 02 | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 3 | 27/08/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 03 | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 4 | 03/09/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 04 | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 5 | 10/09/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 05 | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 6 | 17/09/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 06 | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |

## Fechas institucionales
- **53339** (26P03): inicio 10/08/2026 · recepción 12/09/2026 · cierre **20/09/2026**
- Cierre considerado en este archivo Calendar: **20/09/2026**
- Eventos generados: **6**
- Archivos: `Encuentros INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA - Grupo 53339 - Importar a Calendar.csv` / `Encuentros INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA - Grupo 53339 - Importar a Calendar.ics`

## Cómo importar (sin invitados · description corta)
1. Google Calendar → Configuración → Importar → `.ics` o `.csv`.
2. **No incluye estudiantes** (Pregrado no lleva Guests/ATTENDEE).
3. Location vacío: tras importar, añade Meet (mismo enlace en toda la serie) y publícalo en CDigital.
4. Subject corto: grupos - asignatura - Sesion NN. Description = una línea con el tema.
5. Placeholder Meet de referencia (no va en el ICS): [URL Meet — mismo enlace toda la serie · INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA].

## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem

Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/slides/build_pregrado_cursos.py --calendar-only`.

| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |
| :--- | :--- | :---: | ---: | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 20/08/2026 | **S02** — MinCiencias · 6 líneas de Ingeniería · elección de línea |
| **Parcial 1** | Cuestionario | 1 | 24% | 27/08/2026 | **S03** — Prueba parcial · 1.er avance del artículo |
| **Quiz 2** | Cuestionario | 2 | 9% | 03/09/2026 | **S04** — Identificación de problemas y pregunta de investigación |
| **Parcial 2** | Cuestionario | 2 | 21% | 10/09/2026 | **S05** — Formulación del planteamiento del problema |
| **ACA Final** | Tarea | 3 | 32,8% | 12/09/2026 | — (no cae en día de clase: es la fecha máxima de recepción de trabajos) |
| **Quiz 3** | Cuestionario | 3 | 4% | 17/09/2026 | **S06** — Bases de datos CUN · gestores · marco teórico y revisión (U8+U10–12) |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 20/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |
| **Coevaluación** | Foro | 3 | 1,6% | 20/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
