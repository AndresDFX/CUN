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

## 3. Evaluación (Art. 52)
**Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%.** Cada ACA evalúa el **100% de su corte** (ACA 1 = Corte 1 · ACA 2 = Corte 2 · ACA 3 = Corte 3), **sin subdividir en varios EV** — decidido 2026-08-10. Configúralo así en CDigital.
Producto: avance de **proyecto/artículo de investigación**. Formato de referencia: `Plantilla_APA_CUN_Proyecto de grado.docx`.
**Enunciados estudiantes:** `Clases/Recursos/ACAs/` (ACA 1–3 = Cortes). Regen: `python config/slides/build_acas_estudiantes.py investigacion`.

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py investigacion`.

| Componente | Entrega | Apertura | Nota docente | Regla |
| :--- | :--- | :--- | :--- | :--- |
| **ACA 1** | 27/08/2026 | 13/08/2026 | 03/09/2026 | ventana docente (2026-08-10) |
| **ACA 2** | 03/09/2026 | 28/08/2026 | 10/09/2026 | ventana docente (2026-08-10) |
| **ACA 3** | 10/09/2026 | 04/09/2026 | 17/09/2026 | ventana docente (2026-08-10) |

> Ventanas fijadas por el Docente (2026-08-10) para que cada ACA tenga clases de contenido cursadas antes de su cierre — la Sesión 01 es de encuadre y no dicta tema. Respetan la fecha de recepción institucional del curso.

## 4. Grupo actual (2026)
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`).

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 53339 | 26P03 | SEGUNDO BLOQUE | 10/08/2026 | 12/09/2026 | 20/09/2026 |
