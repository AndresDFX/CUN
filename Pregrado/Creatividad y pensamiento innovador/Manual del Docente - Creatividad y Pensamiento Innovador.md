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

## 3. Evaluación (Art. 52)
**Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%.** Cada ACA evalúa el **100% de su corte** (ACA 1 = Corte 1 · ACA 2 = Corte 2 · ACA 3 = Corte 3), **sin subdividir en varios EV** — decidido 2026-08-10. Configúralo así en CDigital.
**Enunciados estudiantes:** `Clases/Recursos/ACAs/` (ACA 1–3 = Cortes 1–3 · Propuesta de Innovación). Regen: `python config/slides/build_acas_estudiantes.py creatividad`.

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py creatividad`.

| Componente | Entrega | Apertura | Nota docente | Regla |
| :--- | :--- | :--- | :--- | :--- |
| **ACA 1** | 26/08/2026 | 12/08/2026 | 02/09/2026 | ventana docente (2026-08-10) |
| **ACA 2** | 09/09/2026 | 27/08/2026 | 16/09/2026 | ventana docente (2026-08-10) |
| **ACA 3** | 16/09/2026 | 10/09/2026 | 23/09/2026 | ventana docente (2026-08-10) |

> Ventanas fijadas por el Docente (2026-08-10) para que cada ACA tenga clases de contenido cursadas antes de su cierre — la Sesión 01 es de encuadre y no dicta tema. Respetan la fecha de recepción institucional del curso.

## 4. Grupo actual (2026)
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`).

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 54408 | 26V04 | PRIMER BLOQUE | 10/08/2026 | 19/09/2026 | 27/09/2026 |
