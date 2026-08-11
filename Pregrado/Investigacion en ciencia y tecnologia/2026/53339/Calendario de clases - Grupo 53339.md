# Calendario — Investigación Ciencia y Tecnología — Escuela de Ingenierías
**Grupo 53339** · Horario: **Jueves, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Este archivo es de consulta: no crea eventos.** Los encuentros se crean con `PRINCIPAL - Crear encuentros con invitados.gs` (Apps Script), que es lo único que añade a los estudiantes como invitados y pone el Meet. Paso a paso en `LEEME - Crear los eventos de Calendar.md`.
> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo. El periodo va delante porque el nombre del evento es la clave de búsqueda en la carpeta de grabaciones, que acumula todos los periodos.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela): la actividad queda en la carpeta de esa sesión en el **Drive de clases**, y la entrega y la nota siguen en **CDigital**.

| # | Fecha | Tipo | Subject (Calendar) | Evaluación (aula CDigital) |
|---|---|---|---|---|
| 1 | 13/08/2026 (jue) | Sincrónica | 26P03 - 53339 - Investigación Ciencia y Tecnología - Sesion 01 | — |
| 2 | 20/08/2026 (jue) | Sincrónica | 26P03 - 53339 - Investigación Ciencia y Tecnología - Sesion 02 | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 3 | 27/08/2026 (jue) | Sincrónica | 26P03 - 53339 - Investigación Ciencia y Tecnología - Sesion 03 | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 4 | 03/09/2026 (jue) | Sincrónica | 26P03 - 53339 - Investigación Ciencia y Tecnología - Sesion 04 | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 5 | 10/09/2026 (jue) | Sincrónica | 26P03 - 53339 - Investigación Ciencia y Tecnología - Sesion 05 | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 6 | 17/09/2026 (jue) | Sincrónica | 26P03 - 53339 - Investigación Ciencia y Tecnología - Sesion 06 | — |

## Fechas institucionales
- **53339** (26P03): inicio 10/08/2026 · recepción 12/09/2026 · cierre **20/09/2026**
- Cierre considerado en este archivo Calendar: **20/09/2026**
- Sesiones del periodo: **6**

## Cómo se crean estos eventos
1. **Flujo principal:** `PRINCIPAL - Crear encuentros con invitados.gs` en esta misma carpeta → Apps Script → `verificar()` y luego `crearEncuentros()`. Es lo único que añade a los estudiantes como **invitados** y deja el **mismo enlace de Meet** en toda la serie. Instrucciones: `LEEME - Crear los eventos de Calendar.md`.
2. **Respaldo (`RESPALDO sin invitados - Encuentros INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA - Grupo 53339.csv` / `RESPALDO sin invitados - Encuentros INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA - Grupo 53339.ics`):** ⚠️ Google Calendar **descarta los invitados** al importar `.ics`/`.csv`. Estos archivos solo llevan fechas y títulos; úsalos si necesitas el cronograma en un calendario que no sea Google, no para crear la serie del curso.
3. Enlace de Meet: [URL Meet — mismo enlace toda la serie · INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA]. No va dentro del respaldo; lo pone el `.gs`.

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

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
