# Manual del Docente — TRABAJO DE GRADO 3 (Modelos de Innovación, Ingeniería de Sistemas)
**Plantilla genérica.** Código SIAC: **94532** · 32 h docente + 64 h autónomas · Opción de grado III.
Fuente: `TRABAJO DE GRADO 3-MDI_INGENIERIA DE SISTEMAS_94532_PRES_VIR.docx` (en esta carpeta).

> **NO** se rige por el instructivo AFI de Proyecto I/II.

## 📁 Estructura
- **`Clases/`** — presentación del curso (15 sesiones = encuadre + U3–U14 + 2 buffers) + **`Sesion NN - <tema>/Presentacion.pptx`** · docente **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`
- **`Guiones/`** — `Sesion NN - <tema>.md` (solo Markdown; no hay `.docx`) + `Capturas/`
- **`Calendario…`** · festivo = autónoma · 54450 cierra 15/11; 54466/54467 hasta 22/11
- **`2026/<grupo>/`** — roster, correo de bienvenida, hitos docentes y el calendario del grupo (cada grupo tiene su propio cierre)
- **`2026/_combinado_todos/`** — los encuentros: los tres grupos son **una sola serie** (mismo horario, **una sola sala de Meet**). `PRINCIPAL - Crear encuentros con invitados (3 grupos).gs` los crea **con invitados y con Meet**; el `.gs` crea la sala solo. Paso a paso en `LEEME - Crear los eventos de Calendar.md`. Los `.ics`/`.csv` marcados `RESPALDO sin invitados` son respaldo de fechas: Google **descarta los invitados** al importarlos

**Horario confirmado:** martes, **5:00–6:00 pm**.
**Festivo en martes → clase autónoma.**

## 1. Qué es
Culminación del trabajo de grado: **artículo** (≥ 50 referencias; ≥ 4.000 palabras según syllabus) + **sustentación ante jurados** + carga a repositorio.
Prerrequisito: Opción de grado II.

## 2. Unidades de conocimiento del Syllabus (14 **unidades**, no sesiones)

> **La Sesión 01 (11/08/2026) es de ENCUADRE: no se dicta tema.** Se presenta el curso, el Docente, los estudiantes (Padlet) y las ACAs. U1–U2 (Casos de éxito · retomar proyecto · contexto y planteamiento) → lectura autónoma; se retoma al abrir la Sesión 02. (El acuerdo pedagógico se firma en esta sesión de encuadre.) El contenido curricular arranca en la **Sesión 02**.

> ⚠️ La columna **U#** es la numeración del Syllabus. **U1–U2 se cursan como lectura autónoma de la Sesión 01**, así que a partir de ahí **sesión = unidad − 1**: leer esta tabla como si fueran sesiones es lo que producía el error «sustentación = Sesión 13».

| U# (Syllabus) | Sesión real | Temática |
|---|---|---|
| U1–U2 | **S01** (lectura autónoma) | Casos de éxito · retomar proyecto · contexto y planteamiento |
| U3–U4 | S02–S03 | Pregunta/objetivos · estructura del artículo · introducción |
| U5–U6 | S04–S05 | Referentes I · diseño metodológico / instrumento |
| U7–U8 | S06–S07 | Comunidades de práctica · co-creación · análisis de datos |
| U9–U10 | S08–S09 | Cierre marco teórico · resultados y discusión |
| U11–U12 | S10–S11 | Resumen/UNESCO · póster · antiplagio |
| U13–U14 | **S12–S13** | Sustentación ante jurados · repositorio institucional |
| — | S14–S15 | Buffer de calendario (el grupo 54450 no tiene la S15) |

## 3. Evaluación — estructura REAL del aula (CDigital)

**Fuente:** libro de calificaciones del aula en CDigital (auditoría 2026-08-10), cargado en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py tg3`.

Régimen: **Art. 52 · tres cortes** — **Corte 1 = 30%** · **Corte 2 = 30%** · **Corte 3 = 40%**. Configúralo así en CDigital: estos son los ítems que **ya existen** en el libro de calificaciones, con este tipo de actividad y este peso.

| Corte | Ítem en el aula | Tipo de actividad | Peso |
| :---: | :--- | :--- | ---: |
| **1** (30%) | **Quiz 1** | Cuestionario | 6% |
|  | **Parcial 1** | Cuestionario | 24% |
| **2** (30%) | **Quiz 2** | Cuestionario | 9% |
|  | **Parcial 2** | Cuestionario | 21% |
| **3** (40%) | **ACA Final** | Tarea | 32% |
|  | **Quiz 3** | Cuestionario | 4% |
|  | **Autoevaluación** | Cuestionario | 2% |
|  | **Coevaluación** | Foro | 2% |

### Qué desmiente esto del material anterior

- **No hay tres ACAs.** El aula tiene **una sola «ACA Final»** (tarea) en el tercer corte. Los antiguos enunciados ACA 1 / ACA 2 / ACA 3 no correspondían a tres ítems del libro de calificaciones; ya se rehicieron como **un documento por ítem real** (2026-08-10).
- **Queda anulada la regla «cada ACA evalúa el 100% de su corte»** (decisión del 2026-08-10, derogada el mismo día por la auditoría): el desglose real existe y está en la tabla de arriba.
- **Autoevaluación y coevaluación SÍ hacen parte de la nota de este curso** — no son exclusivas de Proyecto I. La **coevaluación es un FORO** (se participa, no se entrega documento) y la **autoevaluación un cuestionario**.
- **Los quices y parciales existen y pesan.** El **Parcial 1 vale 24%** por sí solo. Ya tienen guía para el estudiante en `Clases/Recursos/ACAs/` (`Quiz N (…) - guia del cuestionario.docx` · `Parcial N (…) - guia del cuestionario.docx`), pero en el aula **existen solo como ítem del libro de calificaciones**: falta **crear la actividad** (cuestionario + banco de preguntas) antes de su ventana.
- **TG3 no es «corte único = 100%».** El Syllabus 94532 decía corte único con **EV05 50% + EXAM 50%**; el aula tiene **tres cortes 30/30/40** y ni EV05 ni EXAM existen como ítems. Manda el aula.

### Notas de este curso

- **Producto documental del curso:** el **artículo** (≥ 50 referencias, ≥ 4.000 palabras) + sustentación ante jurados + carga a repositorio. Se entrega como **ACA Final** (tarea) en el tercer corte.
- **Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem del aula**. Los antiguos «ACA 1 (EV05)» y «ACA 2 (EXAM)» se refundieron en el enunciado de la **ACA Final**, que es el único entregable documental del aula.
- La **sustentación ante jurados** sigue siendo obligatoria (Sesión 12) y se califica dentro de la **ACA Final**: en el aula no existe un ítem «EXAM» separado.

Ventanas (apertura · cierre · límite de nota) y en qué sesión cae cada cuestionario: «Fechas de entrega ACA / cortes» más abajo y `Calendario de clases (oficial).md` → «Evaluación en el aula».

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py tg3`.

| Ítem | Tipo | Corte | Peso | Apertura | Cierre | Nota docente |
| :--- | :--- | :---: | ---: | :--- | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 18/08/2026 | 25/08/2026 | 01/09/2026 |
| **Parcial 1** | Cuestionario | 1 | 24% | 08/09/2026 | 15/09/2026 | 22/09/2026 |
| **Quiz 2** | Cuestionario | 2 | 9% | 22/09/2026 | 29/09/2026 | 06/10/2026 |
| **Parcial 2** | Cuestionario | 2 | 21% | 06/10/2026 | 13/10/2026 | 20/10/2026 |
| **ACA Final** (54450) | Tarea | 3 | 32% | 11/08/2026 | 07/11/2026 | 15/11/2026 |
| **ACA Final** (54466 / 54467) | Tarea | 3 | 32% | 11/08/2026 | 14/11/2026 | 22/11/2026 |
| **Quiz 3** | Cuestionario | 3 | 4% | 20/10/2026 | 27/10/2026 | 03/11/2026 |
| **Autoevaluación** (54450) | Cuestionario | 3 | 2% | 03/11/2026 | 10/11/2026 | 15/11/2026 |
| **Autoevaluación** (54466 / 54467) | Cuestionario | 3 | 2% | 10/11/2026 | 17/11/2026 | 22/11/2026 |
| **Coevaluación** (54450) | Foro | 3 | 2% | 03/11/2026 | 10/11/2026 | 15/11/2026 |
| **Coevaluación** (54466 / 54467) | Foro | 3 | 2% | 10/11/2026 | 17/11/2026 | 22/11/2026 |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32% + Quiz 3 4% + Autoevaluación 2% + Coevaluación 2%.

> Ventanas fijadas por el Docente (2026-08-10) sobre la estructura real del aula en CDigital: los quices y parciales son cuestionarios y cierran en día de clase (la Sesión 01 es de encuadre y no evalúa); la ACA Final es una tarea y cierra en la fecha máxima de recepción de trabajos; auto y coevaluación van de la última semana al cierre de notas.

## 4. Grupos 2026
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`).

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 54450 | 26P04 | BLOQUE UNICO | 10/08/2026 | 07/11/2026 | 15/11/2026 |
| 54466 | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | 22/11/2026 |
| 54467 | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | 22/11/2026 |
