# Calendario de clases (oficial) — Proyecto I — Especialización en Inteligencia Artificial
Plantilla del curso · Horario: **Lunes, 8:00 pm – 10:00 pm (2 horas)** · franja AFI oficial **19:00–22:00 h** (duración exigida 1 h 30 min – 2 h)
Grupos de este periodo: **54ES4** · Periodo **26ES4** · Código **ESP329**
Docente: **Julian Andres Castaño** · julian_castanoe@cun.edu.co

> **Archivo generado — no editar a mano.** Regenerar: `python config/slides/build_pregrado_cursos.py --calendar-only` (o `--proyecto1-only`). Fuentes: oferta y horario en `config/cursos/carga_academica_2026.json`; sesiones y temas en `config/cursos/sesiones_cun.py`; ítems, tipos, pesos y ventanas en `config/cursos/fechas_entrega_aca.py`.
> **Horario ✓ instructivo AFI:** el encuentro (20:00–22:00 h) cae dentro de la franja oficial **19:00–22:00 h** y cumple la duración exigida (1 h 30 min – 2 h); coincide además con la sugerencia del propio portal (20:00–22:00 h).
> **Regla de festivo (AFI — distinta de pregrado):** En lunes festivo **no se hace encuentro sincrónico** (Instructivo de encuentros sincrónicos de Especializaciones, §3). Opción principal: **clase pregrabada** disponible en CDigital; opción excepcional: **reprogramar**, solo por coincidencia con festivo y avisando con anticipación. Por eso el catálogo **no numera** los días de clase festivos: aparecen en la tabla de sesiones sin número, y **no** generan evento en el CSV/ICS.
> **Subject Calendar:** `{periodo} - {grupos} - {Asignatura} - Sesion NN` (fuente: `sesiones_cun.py`; el periodo va delante porque el nombre del evento es la clave de búsqueda en la carpeta de grabaciones). El CSV/ICS del grupo —con invitados, coanfitrión y el enlace único de Meet de la serie— lo genera `python config/slides/build_calendar_proyecto1_54es4.py`, **no** este build.
> **CDigital (aula del curso):** https://cdigital.cun.edu.co/course/view.php?id=130378 · **Google Meet (mismo enlace toda la serie):** https://meet.google.com/omk-woqk-vsj
> **Nota Syllabus:** Temario curricular = 7 unidades didácticas del ESP329. Las 11 sesiones semanales del calendario AFI desarrollan esas unidades.

## El encuentro de 2 horas: ~60 min de contenido + 60 min de tutoría

- **Contenido nuevo por sesión: ~60 min.** El guion docente de cada sesión trae solo ese bloque (teoría + modelación); no hay que preparar 120 min de material.
- **Los otros 60 min son tutoría/taller en vivo** con los equipos: revisión de avances y dudas puntuales. Es acompañamiento flexible, no material nuevo.
- Las tutorías por grupo se acuerdan en la semana con el Docente (no hay atención espontánea sin cita).
- **Asistencia a tutorías (formulario del estudiante):** https://forms.gle/oZ8xCYiUo3KEWr1d9

## Evaluación — ventanas OFICIALES de Coordinación

**Régimen:** **Nota única 100%** (ESP329 · Art. 41 §3 del Reglamento Estudiantil), registrada en el aula en **tres cortes 25% / 25% / 50%**. Fuente de las ventanas: `config/cursos/fechas_entrega_aca.py` → `VENTANAS["proyecto1"]`; fuente de los nombres, tipos y pesos: libro de calificaciones del aula en CDigital (auditoría 2026-08-10).

| Ítem en el aula (CDigital) | Tipo | Corte (peso) | Peso del ítem | Apertura | Cierre | Límite de nota | Última sincrónica antes del cierre |
| :--- | :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| **Quiz** | Cuestionario | 1 (25%) | **25%** | lun 03/08/2026 | dom 30/08/2026 | 07/09/2026 | **S02** (24/08) — Problema y pregunta de investigación |
| **ACA 1** | Tarea | 2 (25%) | **25%** | lun 07/09/2026 | dom 04/10/2026 | 12/10/2026 | **S07** (28/09) — Marco legal · citación APA 7 |
| **ACA FINAL** | Tarea | 3 (50%) | **42%** | lun 12/10/2026 | dom 08/11/2026 | 16/11/2026 | **S10** (26/10) — Planeación, viabilidad e integración del anteproyecto |
| **Autoevaluación** | Cuestionario | 3 (50%) | **4%** | lun 16/11/2026 | dom 22/11/2026 | 22/11/2026 | **S11** (09/11) — Integración y evaluación · coevaluación y autoevaluación |
| **Coevaluación** | Foro | 3 (50%) | **4%** | lun 09/11/2026 | dom 15/11/2026 | 22/11/2026 | **S11** (09/11) — Integración y evaluación · coevaluación y autoevaluación |

**Cortes:** Corte 1 25% = Quiz 25% · Corte 2 25% = ACA 1 25% · Corte 3 50% = ACA FINAL 42% + Autoevaluación 4% + Coevaluación 4%.

> **Ningún ítem cierra en día de clase:** las ventanas de Coordinación cierran en **domingo** y el día de clase es **lunes**. Por eso la última columna marca la última sesión sincrónica útil antes de cada cierre, en vez de «la sesión en que cae».
> A diferencia de pregrado, Proyecto I **no tiene quices ni parciales adicionales**: en todo el periodo hay **1 cuestionario evaluativo** (Quiz) y **2 tareas** (ACA 1, ACA FINAL); el resto del corte 3 son los instrumentos individuales de cierre (**autoevaluación** cuestionario, **coevaluación** foro).
> **Ventanas que abren antes del inicio del periodo:** **Quiz** (03/08/2026), contra un inicio de clases el 10/08/2026. Son las fechas de Coordinación; en la práctica el ítem se presenta y se trabaja desde la primera clase.
> Fechas OFICIALES de Coordinación (Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf) sobre la estructura real del aula en CDigital: Quiz 25% (corte 1) · ACA 1 25% (corte 2) · ACA FINAL 42% + autoevaluación 4% + coevaluación 4% (corte 3). Cierre y registro de todas las notas: 22/11/2026.
> **No te guíes por los recordatorios de Moodle** para el cierre: pueden estar desactualizados. La fecha válida es la de Coordinación (columna «Límite de nota» y cierre del periodo en «Fechas institucionales»).

## Cuántas clases caben dentro de cada ventana

Cruce de las ventanas de Coordinación con los festivos colombianos y con el catálogo de sesiones. **Día de clase: lunes.** La **sesión de encuadre no dicta tema**, así que no cuenta como clase de contenido para el ítem cuya ventana la incluye.

| Ítem | Ventana | Días de clase en la ventana (dentro del periodo) | Perdidos por festivo | Sesiones sincrónicas | Cuáles |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **Quiz** ⚠️ | 03/08 – 30/08 | 3 | 17/08 (Asunción de la Virgen) | **2** | S01 (10/08, encuadre — no dicta tema) · S02 (24/08) |
| **ACA 1** | 07/09 – 04/10 | 4 | — | **4** | S04 (07/09) · S05 (14/09) · S06 (21/09) · S07 (28/09) |
| **ACA FINAL** ⚠️ | 12/10 – 08/11 | 4 | 12/10 (Día de la Raza) · 02/11 (Todos los Santos) | **2** | S09 (19/10) · S10 (26/10) |
| **Autoevaluación** | 16/11 – 22/11 | 1 | 16/11 (Independencia de Cartagena) | **0** | — |
| **Coevaluación** | 09/11 – 15/11 | 1 | — | **1** | S11 (09/11) |

> ⚠️ **Quiz** (25% · corte 1) se juega en solo **1 sesión de contenido** (la sesión de encuadre que cae en su ventana no dicta tema): de los 3 días de clase de su ventana, 1 cae en festivo — 17/08 (Asunción de la Virgen). Refuerza con **tutorías por grupo** en esas semanas. No dejes ese tramo dependiendo solo de las sesiones sincrónicas.
> ⚠️ **ACA FINAL** (42% · corte 3) se juega en solo **2 sesiones de contenido**: de los 4 días de clase de su ventana, 2 caen en festivo — 12/10 (Día de la Raza) · 02/11 (Todos los Santos). Adelanta contenido en la sesión anterior a la ventana (**S08**, 05/10). Refuerza con **tutorías por grupo** en esas semanas. No dejes ese tramo dependiendo solo de las sesiones sincrónicas.

## Días de clase SIN encuentro (festivos colombianos 2026)

| Fecha | Festivo | Qué toca de la evaluación |
| :--- | :--- | :--- |
| 17/08/2026 (lun) | Asunción de la Virgen (trasladado del sáb. 15/08) | ventana de **Quiz** |
| 12/10/2026 (lun) | Día de la Raza | **abre ACA FINAL** · límite de nota de **ACA 1** |
| 02/11/2026 (lun) | Todos los Santos (trasladado del dom. 01/11) | ventana de **ACA FINAL** |
| 16/11/2026 (lun) | Independencia de Cartagena (trasladado del mié. 11/11) | **abre Autoevaluación** · límite de nota de **ACA FINAL** |

> En lunes festivo **no se hace encuentro sincrónico** (Instructivo de encuentros sincrónicos de Especializaciones, §3). Opción principal: **clase pregrabada** disponible en CDigital; opción excepcional: **reprogramar**, solo por coincidencia con festivo y avisando con anticipación.

## Las sesiones de clase (lunes) — alineadas a ESP329

**Fuente:** Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx (fuente primaria) · Instructivo/Cronograma AFI 26ES4 (operativa) · Manual del Docente

**Sesión** = numeración del catálogo, la que usan el guion, el `.pptx` y el Subject de Calendar. Las filas sin número son días de clase festivos: **no hay encuentro y no hay evento en Calendar**. La columna **Evaluación** dice qué ventana abre ese lunes, cuál cierra durante esa semana (en domingo) y si esa es la última clase antes de un cierre.

| Sesión | Fecha | Tipo | Bloque | Unidad ESP329 | Contenido | Evaluación (aula CDigital) |
|---|---|---|---|---|---|---|
| **01** | 10/08/2026 (lun) | Sincrónica | Encuadre | — | Encuadre: presentación del curso, del Docente, de los estudiantes (Padlet) y de las ACAs (peso, fechas, formato APA). No se dicta tema. | — |
| — | (misma semana) | ⚠️ Lectura autónoma | Encuadre | — | ESP329 U1 (Fundamentos y enfoque de investigación) → lectura autónoma; se retoma al abrir la Sesión 02. | — |
| — | 17/08/2026 (lun) | Sin sincrónico (Asunción de la Virgen) | — | — | **No hay encuentro** (festivo). Clase **pregrabada** en CDigital / trabajo autónomo; el avance del anteproyecto no se detiene. | — |
| **02** | 24/08/2026 (lun) | Sincrónica | Quiz | U2 | ESP329 U2 · Delimitación del problema · pregunta viable · líneas IA del programa. | **Cierra Quiz** dom 30/08 (cuestionario · 25%) — esta es la última clase antes del cierre |
| **03** | 31/08/2026 (lun) | Sincrónica | Quiz | U3 | ESP329 U3 · Objetivo general/específicos · justificación · alcances/limitaciones · el Quiz (cuestionario, corte 1) cerró el domingo anterior: la última sincrónica antes de su cierre fue la Sesión 02. | **Calificando Quiz** (límite de nota 07/09): sesión de retroalimentación |
| **04** | 07/09/2026 (lun) | Sincrónica | ACA 1 | U4 | ESP329 U4 · Retro del Quiz (cuestionario del corte 1) · hoy ABRE la ACA 1 (tarea, corte 2) · antecedentes (mín. 6 nacionales/internacionales). | **Abre ACA 1** (tarea · 25% · corte 2) · **Hoy vence el límite de nota de Quiz** |
| **05** | 14/09/2026 (lun) | Sincrónica | ACA 1 | U4 | ESP329 U4 · Bases teóricas alineadas a pregunta y variables/categorías. | — |
| **06** | 21/09/2026 (lun) | Sincrónica | ACA 1 | U4 | ESP329 U4 · Definiciones operativas y contexto de aplicación. | — |
| **07** | 28/09/2026 (lun) | Sincrónica | ACA 1 | U4 | ESP329 U4 · Marco legal si aplica · citación/referencias · última sincrónica antes del cierre de la ACA 1. | **Cierra ACA 1** dom 04/10 (tarea · 25%) — esta es la última clase antes del cierre |
| **08** | 05/10/2026 (lun) | Sincrónica | ACA FINAL | U5 | ESP329 U5 · Adelantar metodología antes de los festivos del tramo de la ACA FINAL. | **Calificando ACA 1** (límite de nota 12/10): sesión de retroalimentación |
| — | 12/10/2026 (lun) | Sin sincrónico (Día de la Raza) | — | — | **No hay encuentro** (festivo). Clase **pregrabada** en CDigital / trabajo autónomo; el avance del anteproyecto no se detiene. | **Abre ACA FINAL** (tarea · 42% · corte 3) · **Hoy vence el límite de nota de ACA 1** |
| **09** | 19/10/2026 (lun) | Sincrónica | ACA FINAL | U5 | ESP329 U5 · Primeros 20 min: devolución de la ACA 1 con la rúbrica en pantalla (qué se corrige antes de la ACA FINAL, que exige trazabilidad de esas correcciones) · luego población/muestra e instrumentos PROPUESTOS (no aplicados en Proyecto I). | — |
| **10** | 26/10/2026 (lun) | Sincrónica | ACA FINAL | U6–U7 | ESP329 U6–U7 · Cronograma, presupuesto e integración · última sincrónica antes del cierre de la ACA FINAL. | **Última sincrónica antes del cierre de ACA FINAL** (dom 08/11) |
| — | 02/11/2026 (lun) | Sin sincrónico (Todos los Santos) | — | — | **No hay encuentro** (festivo). Clase **pregrabada** en CDigital / trabajo autónomo; el avance del anteproyecto no se detiene. | **Cierra ACA FINAL** dom 08/11 (tarea · 42%) |
| **11** | 09/11/2026 (lun) | Sincrónica | Cierre | U7 | ESP329 U7 · Coherencia final · coevaluación/autoevaluación · última sesión sincrónica. | **Abre Coevaluación** (foro · 4% · corte 3) · **Cierra Coevaluación** dom 15/11 (foro · 4%) — esta es la última clase antes del cierre · **Última sincrónica antes del cierre de Autoevaluación** (dom 22/11) · **Calificando ACA FINAL** (límite de nota 16/11): sesión de retroalimentación |
| — | 16/11/2026 (lun) | Sin sincrónico (Independencia de Cartagena) | — | — | **No hay encuentro** (festivo). Clase **pregrabada** en CDigital / trabajo autónomo; el avance del anteproyecto no se detiene. | **Abre Autoevaluación** (cuestionario · 4% · corte 3) · **Cierra Autoevaluación** dom 22/11 (cuestionario · 4%) · **Hoy vence el límite de nota de ACA FINAL** |

> La actividad **«Conformación de equipos»** tiene que quedar habilitada en CDigital desde el encuadre: sin ella **no hay entrega grupal** (Instructivo AFI). Los equipos se arman en la hora de tutoría de la Sesión 01.

**Total: 11 sesiones sincrónicas** = los 11 días de clase no festivos del periodo (10/08 → 09/11). Entre 10/08/2026 y 22/11/2026 hay **15** días de clase; menos los **4** festivos (17/08, 12/10, 02/11, 16/11) quedan **11**. No sobra ni falta ninguno.

## Fechas institucionales
- Inicio del periodo: **10/08/2026**
- Fecha máxima de recepción de trabajos (informativa, portal): **14/11/2026**
- **Cierre oficial y registro de notas: 22/11/2026** (domingo) — única fecha válida
- Última sesión sincrónica del periodo: **09/11/2026** (S11)
- Informe Final de Curso: dentro de los **3 días hábiles siguientes** al cierre.

## Registro obligatorio de cada sesión y tutoría (dentro de 24 h)
Formulario exclusivo del Docente titular (**NO compartir con estudiantes**): **Registro de Sesiones Sincrónicas y Tutorías Especialización:** https://forms.gle/6t6BXqQ2Kwmivpct8

## Ver también
- `Manual del Docente - PROYECTO I.md` (raíz del curso): guía completa — cómo preparar la sesión, qué le entregas a la universidad, qué te entregan los estudiantes.
- `2026/54ES4/`: roster, CSV/ICS de encuentros con invitados, Apps Script, hitos docentes y correo de bienvenida.
- Enunciados e instructivos para el estudiante: `Clases/Recursos/ACAs/` (`python config/slides/build_acas_estudiantes.py proyecto1`).
