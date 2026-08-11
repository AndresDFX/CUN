# Calendario — Trabajo de Grado 2 — Modelos de Innovación (Ing. Sistemas)
**Grupo 54448** · Horario: **Lunes, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Este archivo es de consulta: no crea eventos.** Los encuentros se crean con `PRINCIPAL - Crear encuentros con invitados.gs` (Apps Script), que es lo único que añade a los estudiantes como invitados y pone el Meet. Paso a paso en `LEEME - Crear los eventos de Calendar.md`.
> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo. El periodo va delante porque el nombre del evento es la clave de búsqueda en la carpeta de grabaciones, que acumula todos los periodos.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela): la actividad queda en la carpeta de esa sesión en el **Drive de clases**, y la entrega y la nota siguen en **CDigital**.

| # | Fecha | Tipo | Subject (Calendar) | Evaluación (aula CDigital) |
|---|---|---|---|---|
| 1 | 14/08/2026 (vie) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 01 | — |
| 2 | 17/08/2026 (lun) | Autónoma (Asunción de la Virgen) | 26V04 - 54448 - Trabajo de Grado 2 - Clase autonoma (Asunción de la Virgen) | — |
| 3 | 24/08/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 02 | — |
| 4 | 31/08/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 03 | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 5 | 07/09/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 04 | — |
| 6 | 14/09/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 05 | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 7 | 21/09/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 06 | — |
| 8 | 28/09/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 07 | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 9 | 05/10/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 08 | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 10 | 12/10/2026 (lun) | Autónoma (Día de la Raza) | 26V04 - 54448 - Trabajo de Grado 2 - Clase autonoma (Día de la Raza) | — |
| 11 | 19/10/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 09 | — |
| 12 | 26/10/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 10 | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |
| 13 | 02/11/2026 (lun) | Autónoma (Todos los Santos) | 26V04 - 54448 - Trabajo de Grado 2 - Clase autonoma (Todos los Santos) | — |
| 14 | 09/11/2026 (lun) | Sincrónica | 26V04 - 54448 - Trabajo de Grado 2 - Sesion 11 | — |
| 15 | 16/11/2026 (lun) | Autónoma (Independencia de Cartagena) | 26V04 - 54448 - Trabajo de Grado 2 - Clase autonoma (Independencia de Cartagena) | — |

## Fechas institucionales
- **54448** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**
- Cierre considerado en este archivo Calendar: **22/11/2026**
- Sesiones del periodo: **15**

## Cómo se crean estos eventos
1. **Flujo principal:** `PRINCIPAL - Crear encuentros con invitados.gs` en esta misma carpeta → Apps Script → `verificar()` y luego `crearEncuentros()`. Es lo único que añade a los estudiantes como **invitados** y deja el **mismo enlace de Meet** en toda la serie. Instrucciones: `LEEME - Crear los eventos de Calendar.md`.
2. **Respaldo (`RESPALDO sin invitados - Encuentros TRABAJO DE GRADO 2 - Grupo 54448.csv` / `RESPALDO sin invitados - Encuentros TRABAJO DE GRADO 2 - Grupo 54448.ics`):** ⚠️ Google Calendar **descarta los invitados** al importar `.ics`/`.csv`. Estos archivos solo llevan fechas y títulos; úsalos si necesitas el cronograma en un calendario que no sea Google, no para crear la serie del curso.
3. Enlace de Meet: [URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 2]. No va dentro del respaldo; lo pone el `.gs`.

## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem

Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/slides/build_pregrado_cursos.py --calendar-only`.

| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |
| :--- | :--- | :---: | ---: | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 31/08/2026 | **S03** — Estructura del documento / artículo de avance |
| **Parcial 1** | Cuestionario | 1 | 24% | 14/09/2026 | **S05** — Marco teórico — avance |
| **Quiz 2** | Cuestionario | 2 | 9% | 28/09/2026 | **S07** — Diseño metodológico (propuesto) |
| **Parcial 2** | Cuestionario | 2 | 21% | 05/10/2026 | **S08** — Instrumentos y plan de análisis (propuestos) |
| **ACA Final** | Tarea | 3 | 32,8% | 14/11/2026 | — (no cae en día de clase: es la fecha máxima de recepción de trabajos) |
| **Quiz 3** | Cuestionario | 3 | 4% | 26/10/2026 | **S10** — Socialización de avances |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 22/11/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |
| **Coevaluación** | Foro | 3 | 1,6% | 22/11/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
