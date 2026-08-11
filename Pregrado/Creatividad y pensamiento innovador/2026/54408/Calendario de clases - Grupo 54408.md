# Calendario — Creatividad y Pensamiento Innovador — Escuela de Ingenierías
**Grupo 54408** · Horario: **Miércoles, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Este archivo es de consulta: no crea eventos.** Los encuentros se crean con `PRINCIPAL - Crear encuentros con invitados.gs` (Apps Script), que es lo único que añade a los estudiantes como invitados y pone el Meet. Paso a paso en `LEEME - Crear los eventos de Calendar.md`.
> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela).

| # | Fecha | Tipo | Subject (Calendar) | Evaluación (aula CDigital) |
|---|---|---|---|---|
| 1 | 12/08/2026 (mié) | Sincrónica | 54408 - Creatividad y Pensamiento Innovador - Sesion 01 | — |
| 2 | 19/08/2026 (mié) | Sincrónica | 54408 - Creatividad y Pensamiento Innovador - Sesion 02 | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 3 | 26/08/2026 (mié) | Sincrónica | 54408 - Creatividad y Pensamiento Innovador - Sesion 03 | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 4 | 02/09/2026 (mié) | Sincrónica | 54408 - Creatividad y Pensamiento Innovador - Sesion 04 | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 5 | 09/09/2026 (mié) | Sincrónica | 54408 - Creatividad y Pensamiento Innovador - Sesion 05 | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 6 | 16/09/2026 (mié) | Sincrónica | 54408 - Creatividad y Pensamiento Innovador - Sesion 06 | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |
| 7 | 23/09/2026 (mié) | Sincrónica | 54408 - Creatividad y Pensamiento Innovador - Sesion 07 | — |

## Fechas institucionales
- **54408** (26V04): inicio 10/08/2026 · recepción 19/09/2026 · cierre **27/09/2026**
- Cierre considerado en este archivo Calendar: **27/09/2026**
- Sesiones del periodo: **7**

## Cómo se crean estos eventos
1. **Flujo principal:** `PRINCIPAL - Crear encuentros con invitados.gs` en esta misma carpeta → Apps Script → `verificar()` y luego `crearEncuentros()`. Es lo único que añade a los estudiantes como **invitados** y deja el **mismo enlace de Meet** en toda la serie. Instrucciones: `LEEME - Crear los eventos de Calendar.md`.
2. **Respaldo (`RESPALDO sin invitados - Encuentros CREATIVIDAD Y PENSAMIENTO INNOVADOR - Grupo 54408.csv` / `RESPALDO sin invitados - Encuentros CREATIVIDAD Y PENSAMIENTO INNOVADOR - Grupo 54408.ics`):** ⚠️ Google Calendar **descarta los invitados** al importar `.ics`/`.csv`. Estos archivos solo llevan fechas y títulos; úsalos si necesitas el cronograma en un calendario que no sea Google, no para crear la serie del curso.
3. Enlace de Meet: [URL Meet — mismo enlace toda la serie · CREATIVIDAD Y PENSAMIENTO INNOVADOR]. No va dentro del respaldo; lo pone el `.gs`.

## Evaluación en el aula (CDigital) — en qué sesión cae cada ítem

Fuente: libro de calificaciones de cada aula (auditoría 2026-08-10), en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/slides/build_pregrado_cursos.py --calendar-only`.

| Ítem | Tipo | Corte | Peso | Cierre | Sesión en que cae |
| :--- | :--- | :---: | ---: | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 19/08/2026 | **S02** — Creatividad/innovación en I+D · Design Thinking y técnicas |
| **Parcial 1** | Cuestionario | 1 | 24% | 26/08/2026 | **S03** — Gestión de la innovación (Manual de Oslo / OCDE) |
| **Quiz 2** | Cuestionario | 2 | 9% | 02/09/2026 | **S04** — Tipos de innovación |
| **Parcial 2** | Cuestionario | 2 | 21% | 09/09/2026 | **S05** — Validación de la propuesta · vigilancia tecnológica |
| **ACA Final** | Tarea | 3 | 32,8% | 19/09/2026 | — (no cae en día de clase: es la fecha máxima de recepción de trabajos) |
| **Quiz 3** | Cuestionario | 3 | 4% | 16/09/2026 | **S06** — Innovación local–internacional · entidades de apoyo |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 27/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |
| **Coevaluación** | Foro | 3 | 1,6% | 27/09/2026 | — (no cae en día de clase: ventana hasta el cierre de notas) |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
