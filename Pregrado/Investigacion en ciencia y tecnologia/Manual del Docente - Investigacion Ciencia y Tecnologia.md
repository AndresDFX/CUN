# Manual del Docente — INVESTIGACIÓN CIENCIA Y TECNOLOGÍA (Escuela de Ingenierías)
**Plantilla genérica** (sin código de grupo en el material de raíz). Código SIAC: **EI005** · 2 créditos · 32 h docente + 64 h autónomas.
Fuente: syllabus `INVESTIGACION CIENCIA Y TECNOLOGIA PARA ESCUELA DE INGENIERIAS EI005_PRES.docx` (en esta carpeta).

> Nota: aunque el área que oferta es "Formación Investigativa", **este NO es Proyecto I/II** — es asignatura regular de escuela con evaluación por cortes (Art. 52). El instructivo AFI no aplica.

## 📁 Estructura
- **`Clases/Presentacion del Curso - Investigacion Ciencia y Tecnologia.pptx`** — horario jue 5–6 pm · docente **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`.
- **`Clases/Sesion NN - <tema>/Presentacion.pptx`** — presentación del estudiante (sin bio docente).
- **`Guiones/Sesion NN - <tema>.md`** (solo Markdown; no hay `.docx`) — guion docente + `Capturas/`.
- **`Calendario de clases (oficial).md`** — festivo = clase autónoma · mapeo tema↔fecha.
- **`2026/<grupo>/`** — Informacion + CSV/ICS Calendar (**sin invitados estudiantes**; Meet placeholder único por serie).

**Horario confirmado:** jueves, **5:00–6:00 pm** (Google Meet).
**Regla de festivo (Pregrado):** si el día de clase es festivo colombiano → **clase autónoma** (actividad en CDigital), no cancelación.

## 1. Propósito
Aplicar el **método científico** a una temática del entorno del estudiante, dentro de las **6 líneas estratégicas de Ingeniería** (IoT, Big Data, IA, servicios cloud/FinTech, aplicaciones, telemática).

## 2. Unidades de conocimiento (syllabus)

> **La Sesión 01 (13/08/2026) es de ENCUADRE: no se dicta tema.** Se presenta el curso, el Docente, los estudiantes (Padlet) y las ACAs. U1–U2 (Syllabus y producto final · fundamentos del método científico) → lectura autónoma; se retoma al abrir la Sesión 02. El contenido curricular arranca en la **Sesión 02**.

| # | Temática |
|---|---|
| 1 | Presentación del syllabus y del producto final (artículo de nuevo conocimiento) |
| 2 | Fundamentos del método científico y sus etapas |
| 4 | MinCiencias · 6 líneas · elección de línea temática |
| 5 | Prueba escrita parcial · 1.er avance del artículo |
| 6 | Identificación de problemas y pregunta de investigación |
| 7 | Formulación del planteamiento del problema |
| 8 | Bases de datos CUN + gestores web (ZoteroBib / similares) |
| 10–12 | Posturas teóricas · 2.ª parcial · marco teórico / literatura |

> El syllabus salta N° 3 y 9; respeta la numeración oficial.

## 3. Evaluación — estructura REAL del aula (CDigital)

**Fuente:** libro de calificaciones del aula en CDigital (auditoría 2026-08-10), cargado en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py investigacion`.

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
- **Los quices y parciales existen y pesan.** El **Parcial 1 vale 24%** por sí solo. Ya tienen guía para el estudiante en `Clases/Recursos/ACAs/` (`Quiz N (…) - guia del cuestionario.docx` · `Parcial N (…) - guia del cuestionario.docx`), pero en el aula **existen solo como ítem del libro de calificaciones**: falta **crear la actividad** (cuestionario + banco de preguntas) antes de su ventana.

### Notas de este curso

- **Producto documental del curso:** avance del **artículo / proyecto de investigación** (formato `Plantilla_APA_CUN_Proyecto de grado.docx`). Es lo que se entrega como **ACA Final** (tarea) en el tercer corte.
- **Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem del aula** (guía de cada quiz y parcial, enunciado de la ACA Final, instructivo de auto y coevaluación). Regenerar: `python config/slides/build_acas_estudiantes.py investigacion`.
- La **prueba escrita parcial** que el Syllabus pide en U5 y U11–12 ya tiene dónde vivir: son los **Parcial 1 y Parcial 2** del aula (24% y 21%).

Ventanas (apertura · cierre · límite de nota) y en qué sesión cae cada cuestionario: «Fechas de entrega ACA / cortes» más abajo y `Calendario de clases (oficial).md` → «Evaluación en el aula».

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py investigacion`.

| Ítem | Tipo | Corte | Peso | Apertura | Cierre | Nota docente |
| :--- | :--- | :---: | ---: | :--- | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 13/08/2026 | 20/08/2026 | 27/08/2026 |
| **Parcial 1** | Cuestionario | 1 | 24% | 21/08/2026 | 27/08/2026 | 03/09/2026 |
| **Quiz 2** | Cuestionario | 2 | 9% | 28/08/2026 | 03/09/2026 | 10/09/2026 |
| **Parcial 2** | Cuestionario | 2 | 21% | 04/09/2026 | 10/09/2026 | 17/09/2026 |
| **ACA Final** | Tarea | 3 | 32,8% | 13/08/2026 | 12/09/2026 | 20/09/2026 |
| **Quiz 3** | Cuestionario | 3 | 4% | 11/09/2026 | 12/09/2026 | 20/09/2026 |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 17/09/2026 | 20/09/2026 | 20/09/2026 |
| **Coevaluación** | Foro | 3 | 1,6% | 17/09/2026 | 20/09/2026 | 20/09/2026 |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Ventanas fijadas por el Docente (2026-08-10) sobre la estructura real del aula en CDigital: los quices y parciales son cuestionarios y cierran en día de clase (la Sesión 01 es de encuadre y no evalúa); la ACA Final es una tarea y cierra en la fecha máxima de recepción de trabajos; auto y coevaluación van de la última semana al cierre de notas.

## 4. Grupo actual (2026)
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`).

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 53339 | 26P03 | SEGUNDO BLOQUE | 10/08/2026 | 12/09/2026 | 20/09/2026 |
