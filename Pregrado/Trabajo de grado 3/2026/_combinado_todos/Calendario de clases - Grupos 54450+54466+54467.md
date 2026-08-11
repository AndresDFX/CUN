# Calendario — Trabajo de Grado 3 — Modelos de Innovación (Ing. Sistemas)
**Grupos 54450 / 54466 / 54467** · Horario: **Martes, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Este archivo es de consulta: no crea eventos.** Los encuentros se crean con `PRINCIPAL - Crear encuentros con invitados (3 grupos).gs` (Apps Script), que es lo único que añade a los estudiantes como invitados y pone el Meet. Paso a paso en `LEEME - Crear los eventos de Calendar.md`.
> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo. El periodo va delante porque el nombre del evento es la clave de búsqueda en la carpeta de grabaciones, que acumula todos los periodos.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela): la actividad queda en la carpeta de esa sesión en el **Drive de clases**, y la entrega y la nota siguen en **CDigital**.

| # | Fecha | Tipo | Subject (Calendar) | Evaluación (aula CDigital) |
|---|---|---|---|---|
| 1 | 11/08/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 01 | — |
| 2 | 18/08/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 02 | — |
| 3 | 25/08/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 03 | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 4 | 01/09/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 04 | — |
| 5 | 08/09/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 05 | — |
| 6 | 15/09/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 06 | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 7 | 22/09/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 07 | — |
| 8 | 29/09/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 08 | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 9 | 06/10/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 09 | — |
| 10 | 13/10/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 10 | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 11 | 20/10/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 11 | — |
| 12 | 27/10/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 12 | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |
| 13 | 03/11/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 13 | — |
| 14 | 10/11/2026 (mar) | Sincrónica | 26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 14 | **Cierra la ventana de Autoevaluación** (cuestionario · 2% · corte 3) · **Cierra la ventana de Coevaluación** (foro · 2% · corte 3) |
| 15 | 17/11/2026 (mar) | Sincrónica | 26V04 - 54466/54467 - Trabajo de Grado 3 - Sesion 15 | — |

## Fechas institucionales
- **54450** (26P04): inicio 10/08/2026 · recepción 07/11/2026 · cierre **15/11/2026**
- **54466** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**
- **54467** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**
- Cierre considerado en este archivo Calendar: **22/11/2026**
- Sesiones del periodo: **15**

## Cómo se crean estos eventos
1. **Flujo principal:** `PRINCIPAL - Crear encuentros con invitados (3 grupos).gs` en esta misma carpeta → Apps Script → `verificar()` y luego `crearEncuentros()`. Es lo único que añade a los estudiantes como **invitados** y deja el **mismo enlace de Meet** en toda la serie. Instrucciones: `LEEME - Crear los eventos de Calendar.md`.
2. **Respaldo (`RESPALDO sin invitados - Encuentros TRABAJO DE GRADO 3 - Grupos 54450+54466+54467.csv` / `RESPALDO sin invitados - Encuentros TRABAJO DE GRADO 3 - Grupos 54450+54466+54467.ics`):** ⚠️ Google Calendar **descarta los invitados** al importar `.ics`/`.csv`. Estos archivos solo llevan fechas y títulos; úsalos si necesitas el cronograma en un calendario que no sea Google, no para crear la serie del curso.
3. Enlace de Meet: [URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 3]. No va dentro del respaldo; lo pone el `.gs`.

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

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
