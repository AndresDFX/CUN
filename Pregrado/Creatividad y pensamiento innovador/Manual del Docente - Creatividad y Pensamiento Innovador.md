# Manual del Docente — CREATIVIDAD Y PENSAMIENTO INNOVADOR (Escuela de Ingenierías)
**Plantilla genérica.** Código SIAC de carpeta: **EI004** · Área oferente: **C-EMP** · 2 créditos · 32 h docente + 64 h autónomas.
Fuente: syllabus `CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS EI004_VIR.docx` (en esta carpeta).

> No es AFI / Proyecto I-II. Evaluación por cortes (Art. 52).

## 📁 Estructura
- **`Clases/Presentacion del Curso - ….pptx`** + **`Clases/Sesion NN - <tema>/Presentacion.pptx`** · docente **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`
- **`Guiones/Sesion NN - <tema>.md`** (solo Markdown; no hay `.docx`) + `Capturas/`
- **`Calendario de clases (oficial).md`** · festivo = autónoma · mapeo tema↔fecha
- **`2026/<grupo>/`** — Informacion + CSV/ICS (**sin invitados**; Meet placeholder único por serie)

**Horario confirmado:** miércoles, **5:00–6:00 pm**.
**Festivo en día de clase → clase autónoma** (CDigital).

## 1. Propósito
Que el estudiante identifique habilidades de creatividad e innovación y formule una **Propuesta de Innovación** (hilo conductor desde la semana 1).

## 2. Unidades de conocimiento (syllabus)

> **La Sesión 01 (12/08/2026) es de ENCUADRE: no se dicta tema.** Se presenta el curso, el Docente, los estudiantes (Padlet) y las ACAs. U1–U2 (Propuesta de Innovación · creatividad e inteligencia emocional) → lectura autónoma; se retoma al abrir la Sesión 02. El contenido curricular arranca en la **Sesión 02**.

| # | Temática |
|---|---|
| 1 | Introducción · syllabus · trabajo final |
| 2 | Inteligencia emocional, creatividad e innovación |
| 3 | Conceptos en I+D · Design Thinking y técnicas |
| 4 | Gestión de la innovación (Manual de Oslo / OCDE) |
| 5 | Tipos de innovación |
| 6 | Análisis de negocios · validación / sustentación |
| 7 | Vigilancia tecnológica |
| 8 | Innovación local–internacional · entidades de apoyo |

## 3. Evaluación — estructura REAL del aula (CDigital)

**Fuente:** libro de calificaciones del aula en CDigital (auditoría 2026-08-10), cargado en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py creatividad`.

Régimen: **Art. 52 · tres cortes** — **Corte 1 = 30%** · **Corte 2 = 30%** · **Corte 3 = 40%**. Configúralo así en CDigital: estos son los ítems que **ya existen** en el libro de calificaciones, con este tipo de actividad y este peso.

| Corte | Ítem en el aula | Tipo de actividad | Peso |
| :---: | :--- | :--- | ---: |
| **1** (30%) | **Quiz 1** | Cuestionario | 6% |
|  | **Parcial 1** | Cuestionario | 24% |
| **2** (30%) | **Quiz 2** | Cuestionario | 9% |
|  | **Parcial 2** | Cuestionario | 21% |
| **3** (40%) | **ACA Final** | Tarea | 32,8% |
|  | **Quiz 3** | Cuestionario | 4% |
|  | **Autoevaluación** | Cuestionario | 1,6% |
|  | **Coevaluación** | Foro | 1,6% |

### Qué desmiente esto del material anterior

- **No hay tres ACAs.** El aula tiene **una sola «ACA Final»** (tarea) en el tercer corte. Los antiguos enunciados ACA 1 / ACA 2 / ACA 3 no correspondían a tres ítems del libro de calificaciones; ya se rehicieron como **un documento por ítem real** (2026-08-10).
- **Queda anulada la regla «cada ACA evalúa el 100% de su corte»** (decisión del 2026-08-10, derogada el mismo día por la auditoría): el desglose real existe y está en la tabla de arriba.
- **Autoevaluación y coevaluación SÍ hacen parte de la nota de este curso** — no son exclusivas de Proyecto I. La **coevaluación es un FORO** (se participa, no se entrega documento) y la **autoevaluación un cuestionario**.
- **Los quices y parciales existen y pesan.** El **Parcial 1 vale 24%** por sí solo. Ya tienen guía para el estudiante en `Clases/Recursos/ACAs/` (`Quiz N (…) - guía del cuestionario.docx` · `Parcial N (…) - guía del cuestionario.docx`), pero en el aula **existen solo como ítem del libro de calificaciones**: falta **crear la actividad** (cuestionario + banco de preguntas) antes de su ventana.

### Notas de este curso

- **Producto documental del curso:** la **Propuesta de Innovación**, hilo conductor desde la Sesión 02. Es lo que se entrega como **ACA Final** (tarea) en el tercer corte.
- **Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem del aula** (guía de cada quiz y parcial, enunciado de la ACA Final, instructivo de auto y coevaluación). Regenerar: `python config/slides/build_acas_estudiantes.py creatividad`.

Ventanas (apertura · cierre · límite de nota) y en qué sesión cae cada cuestionario: «Fechas de entrega ACA / cortes» más abajo y `Calendario de clases (oficial).md` → «Evaluación en el aula».

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py creatividad`.

| Ítem | Tipo | Corte | Peso | Apertura | Cierre | Nota docente |
| :--- | :--- | :---: | ---: | :--- | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 12/08/2026 | 19/08/2026 | 26/08/2026 |
| **Parcial 1** | Cuestionario | 1 | 24% | 20/08/2026 | 26/08/2026 | 02/09/2026 |
| **Quiz 2** | Cuestionario | 2 | 9% | 27/08/2026 | 02/09/2026 | 09/09/2026 |
| **Parcial 2** | Cuestionario | 2 | 21% | 03/09/2026 | 09/09/2026 | 16/09/2026 |
| **ACA Final** | Tarea | 3 | 32,8% | 12/08/2026 | 19/09/2026 | 27/09/2026 |
| **Quiz 3** | Cuestionario | 3 | 4% | 10/09/2026 | 16/09/2026 | 23/09/2026 |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 23/09/2026 | 27/09/2026 | 27/09/2026 |
| **Coevaluación** | Foro | 3 | 1,6% | 23/09/2026 | 27/09/2026 | 27/09/2026 |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Ventanas fijadas por el Docente (2026-08-10) sobre la estructura real del aula en CDigital: los quices y parciales son cuestionarios y cierran en día de clase (la Sesión 01 es de encuadre y no evalúa); la ACA Final es una tarea y cierra en la fecha máxima de recepción de trabajos; auto y coevaluación van de la última semana al cierre de notas.

## 4. Grupo actual (2026)
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`).

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 54408 | 26V04 | PRIMER BLOQUE | 10/08/2026 | 19/09/2026 | 27/09/2026 |
