# Calendario — Trabajo de Grado 3 — Modelos de Innovación (Ing. Sistemas)
**Grupo 54467** · Horario: **Martes, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Este archivo es de consulta: no crea eventos.** Los encuentros se crean con `PRINCIPAL - Crear encuentros con invitados (3 grupos).gs` (Apps Script), que es lo único que añade a los estudiantes como invitados y pone el Meet. Paso a paso en `LEEME - Crear los eventos de Calendar.md`.
> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela).

| # | Fecha | Tipo | Subject (Calendar) | Evaluación (aula CDigital) |
|---|---|---|---|---|
| 1 | 11/08/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 01 | — |
| 2 | 18/08/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 02 | — |
| 3 | 25/08/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 03 | **Cierra Quiz 1** (cuestionario · 6% · corte 1) |
| 4 | 01/09/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 04 | — |
| 5 | 08/09/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 05 | — |
| 6 | 15/09/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 06 | **Cierra Parcial 1** (cuestionario · 24% · corte 1) |
| 7 | 22/09/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 07 | — |
| 8 | 29/09/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 08 | **Cierra Quiz 2** (cuestionario · 9% · corte 2) |
| 9 | 06/10/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 09 | — |
| 10 | 13/10/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 10 | **Cierra Parcial 2** (cuestionario · 21% · corte 2) |
| 11 | 20/10/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 11 | — |
| 12 | 27/10/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 12 | **Cierra Quiz 3** (cuestionario · 4% · corte 3) |
| 13 | 03/11/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 13 | — |
| 14 | 10/11/2026 (mar) | Sincrónica | 54450/54466/54467 - Trabajo de Grado 3 - Sesion 14 | — |
| 15 | 17/11/2026 (mar) | Sincrónica | 54466/54467 - Trabajo de Grado 3 - Sesion 15 | **Cierra la ventana de Autoevaluación** (cuestionario · 2% · corte 3) · **Cierra la ventana de Coevaluación** (foro · 2% · corte 3) |

## Fechas institucionales
- **54467** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**
- Cierre considerado en este archivo Calendar: **22/11/2026**
- Sesiones del periodo: **15**

## Cómo se crean estos eventos
Con `PRINCIPAL - Crear encuentros con invitados (3 grupos).gs`, que está en `2026/_combinado_todos/`. Los tres grupos de TG3 son **una sola serie** (mismo horario, misma sala de Meet), así que hay un único script y un único juego de eventos. Instrucciones: `2026/_combinado_todos/LEEME - Crear los eventos de Calendar.md`.

⚠️ Este grupo **no tiene** `.ics`/`.csv` de encuentros propio, y es a propósito: importar el de cada grupo crearía los mismos eventos tres veces. El respaldo de fechas de la serie está también en `_combinado_todos/`.

Lo que sí se importa desde esta carpeta es `Entregas y hitos docentes - Importar a Calendar.csv`: son recordatorios tuyos, sin invitados, y los cierres de ACA **no** coinciden entre los tres grupos.

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
| **Autoevaluación** | Cuestionario | 3 | 2% | 17/11/2026 | **S15** — Cierre administrativo · recepción de entregables |
| **Coevaluación** | Foro | 3 | 2% | 17/11/2026 | **S15** — Cierre administrativo · recepción de entregables |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32% + Quiz 3 4% + Autoevaluación 2% + Coevaluación 2%.

> Los **quices y parciales** son cuestionarios: caen en día de clase y su ventana abre en la sesión anterior. La **ACA Final** es una tarea (documento) y cierra en la fecha máxima de recepción de trabajos. **Autoevaluación** (cuestionario) y **coevaluación** (foro) van de la última semana al cierre de notas. La **Sesión 01 es de encuadre y no evalúa.**

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
