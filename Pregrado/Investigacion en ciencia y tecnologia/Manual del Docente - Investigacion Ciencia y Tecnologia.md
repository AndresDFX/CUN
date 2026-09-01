# Manual del Docente — INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA (Escuela de Ingenierías)

**Léelo ANTES de entrar a la primera clase.** Código SIAC **EI005** · 2 créditos · **32 h con docente + 64 h autónomas** · nivel Profesional · tipología Teórico-Práctica.
Docente: **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`.

Este manual es **genérico del curso**; lo específico de la oferta de este periodo vive en `2026/<grupo>/` (hoy: `2026/53339/`). Es asignatura **regular de pregrado** con evaluación por cortes (Art. 52): aunque el área que la oferta es «Formación Investigativa», **no es Proyecto I/II** y **el instructivo AFI no aplica** — sus formularios y sus rúbricas son de Especialización.

**Fuentes cruzadas (no inventar fuera de ellas):**

1. **Syllabus SIAC (fuente curricular primaria):** `INVESTIGACION CIENCIA Y TECNOLOGIA PARA ESCUELA DE INGENIERIAS EI005_PRES.docx`, en esta misma carpeta — descripción, propósito, competencias, tabla de **unidades de conocimiento**, metodología, bibliografía, sistema de evaluación.
2. **Libro de calificaciones del aula** (auditoría CDigital del 2026-08-10), cargado en `config/cursos/fechas_entrega_aca.py` — ítems reales, tipo de actividad, pesos y ventanas. **Donde el aula y el Syllabus se contradigan, manda el aula.**
3. **Catálogo de sesiones:** `config/cursos/sesiones_cun.py` → `COURSES["investigacion"]` — títulos, fechas, detalle y duración de cada encuentro.
4. **Carga académica:** `config/cursos/carga_academica_2026.json` — grupo, bloque, periodo, horario, inicio/recepción/cierre, enlace del aula.
5. `Calendario de clases (oficial).md` (esta carpeta) — cruce sesión ↔ fecha ↔ ítem que cierra ese día.
6. `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md` — ciclo inicio/desarrollo/cierre de pregrado y lo que sigue pendiente de confirmar con Coordinación.
7. `Pregrado/Checklist de cierre de curso a satisfaccion.md` — verificables de cierre (útiles también para directivos).
8. `2026/53339/LEEME - Crear los eventos de Calendar.md` — runbook de los encuentros en Google Calendar.
9. `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` — formato del producto documental.
10. `HERRAMIENTAS_EXAMLAB.md` (esta carpeta) — análisis de herramientas de apoyo; **no** define entregas ni notas.

## 📁 Estructura de carpetas (`Clases/` = estudiante · `Docente/Guiones/` = docente)

- **`Clases/Presentacion del Curso - Investigacion Ciencia y Tecnologia.pptx`** — encuadre del semestre: docente, horario, evaluación, contacto.
- **`Clases/Sesion NN - <tema>/Presentacion.pptx`** — deck de la sesión (sin bio del docente). Algunas carpetas traen además las lecturas de esa semana (p. ej. la Sesión 01 lleva dos PDF de acceso abierto y un `Lectura autonoma - Sesion 01.txt` con la consigna).
- **`Docente/Guiones/Sesion NN - <tema>.md`** — guion docente, minuto a minuto, para leer casi literal (**solo Markdown**, no hay `.docx`) + `Docente/Guiones/Capturas/`.
- **`Clases/Recursos/ACAs/`** — **un documento por ítem real del aula**: guía de cada quiz y de cada parcial, enunciado de la ACA Final e instructivos de auto y coevaluación.
- **`Calendario de clases (oficial).md`** — mapeo tema ↔ fecha ↔ evaluación.
- **`2026/<grupo>/`** — roster, correo de bienvenida, CSV de hitos docentes y el script de Calendar.

Regenerar material (no editar los generados a mano): guiones y decks de sesión `python config/slides/build_sesion_material.py investigacion all` · enunciados del estudiante `python config/slides/build_acas_estudiantes.py investigacion` · calendario `python config/slides/build_pregrado_cursos.py --calendar-only` · evaluación y fechas de **este** manual `python config/cursos/sync_manuales_fechas.py investigacion`.

## ✅ Lo confirmado · 🔴 lo que tienes que resolver tú

- **Horario: jueves 5:00–6:00 pm. Una hora, no dos.** El encuentro completo son **60 minutos** (`carga_academica_2026.json` → `horario`; `sesiones_cun.py` → `duracion_min: 60`). No hay segundo bloque de tutoría como en Proyecto I: todo lo que quieras hacer cabe en esa hora o se va a trabajo autónomo.
- **Periodo corto: 6 encuentros** (13/08 · 20/08 · 27/08 · 03/09 · 10/09 · 17/09 de 2026). **6 horas sincrónicas contra 64 horas autónomas**: el 90 % del trabajo del estudiante ocurre sin ti. No hay semana de recuperación.
- **Ningún jueves de este periodo cae en festivo**, así que las 6 sesiones son sincrónicas (el calendario generado no marca ninguna «autónoma»). Si un periodo futuro sí lo trae: **festivo = clase autónoma en CDigital, nunca cancelación**.
- 🔴 **Los quices y los parciales existen solo como ítem del libro de calificaciones: falta crear la actividad** (cuestionario + banco de preguntas) antes de cada ventana. El primero abre el **13/08** y cierra el **20/08**. Es lo más urgente del curso.
- 🔴 **El enlace de Google Meet está vacío** en `carga_academica_2026.json` (`"meet": ""`), por eso todo el material muestra el marcador `[URL Meet — mismo enlace toda la serie · INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA]`. Créalo, pégalo en el JSON y regenera.
- 🔴 **Pendientes con Coordinación** (no los inventes): canal del acuerdo pedagógico de pregrado, canal oficial de cargue/cierre de notas, si existe informe de cierre de pregrado y qué plazo hay para respaldar evidencias. Están listados en `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`.
- ⚠️ **El Syllabus marca la metodología como «Presencial ☑»** y la oferta de este grupo es **VIRTUAL** por Google Meet. Es una inconsistencia del documento SIAC, no un error del montaje; queda registrada en `HERRAMIENTAS_EXAMLAB.md` §7-R14.

## 1. Propósito

Aplicar el **método científico** a una temática del entorno del estudiante —laboral o vivencial— dentro de las **6 líneas estratégicas de Ingeniería**: IoT, Big Data, Inteligencia Artificial, servicios de ingeniería (cloud/FinTech), uso de aplicaciones y telemática.

El Syllabus lo desarrolla en cuatro ideas que conviene tener presentes al calificar:

- La metodología de referencia es **ABP**: se parte de una problemática real del entorno del estudiante y se propone una solución que responda a la pregunta de investigación.
- El resultado de aprendizaje esperado es **un proyecto de investigación** construido con bases de datos especializadas, enmarcado en los lineamientos de **MinCiencias** y de la institución.
- El producto final es **un artículo de nuevo conocimiento**, inédito, con la perspectiva propia del estudiante.
- **Ojo con esto:** el Syllabus (U1) dice que ese artículo «se entrega al docente, quien, **en calidad de coautor**, continuará con su proceso de sometimiento a publicación». Es una expectativa institucional del documento, no un trámite montado en el aula ni una tarea de este periodo. Si piensas ejercerla, acuérdalo explícitamente con el estudiante y consulta con Coordinación antes de prometer nada.

**Tu rol es el de garante metodológico**, no el de experto temático de los 20 proyectos: lo que calificas es que el problema esté argumentado, la pregunta sea viable y las fuentes sostengan lo que el estudiante afirma.

## 2. Unidades de conocimiento (Syllabus SIAC)

> **La Sesión 01 (13/08/2026) es de ENCUADRE: no se dicta tema.** Se presenta el curso, el Docente, los estudiantes (Padlet) y las ACAs. **U1–U2** quedan como **lectura autónoma** de esa semana y se retoman al abrir la Sesión 02. El contenido curricular arranca en la **Sesión 02**.

| N° | Temática (Syllabus) | Dónde se dicta |
|---|---|---|
| 1 | Presentación del Syllabus y del producto final (artículo de nuevo conocimiento) | Lectura autónoma S01 → se retoma en S02 |
| 2 | Fundamentos del método científico y sus etapas | Lectura autónoma S01 → se retoma en S02 |
| 4 | MinCiencias · SNCTI · 6 líneas de Ingeniería · elección de línea | **Sesión 02** |
| 5 | Prueba escrita parcial · 1.er avance del artículo | **Sesión 03** |
| 6 | Identificación de problemas y causas · pregunta de investigación (espina de pescado, árbol de problemas, método 3D) | **Sesión 04** |
| 7 | Formulación del planteamiento del problema (estado actual, evidencias, causas, soluciones) | **Sesión 05** |
| 8 | Bases de datos CUN (EBSCO, SciELO, Redalyc, Latindex) + gestores de citas | **Sesión 04** *(adelantada)* |
| 10–12 | Posturas teóricas · marco teórico · revisión de literatura | **Sesión 05** *(adelantadas)* |

> La numeración oficial **salta el N° 3 y el N° 9**: no es un error de transcripción, respétala.

**⚠️ El temario se adelantó (2026-08-11) — lo que recuerdes del orden anterior ya no aplica.** La **ACA Final** califica marco teórico y revisión de literatura y **cierra el 12/09**, antes de la última clase. Para que nada evaluable llegue tarde, **U8** pasó a la Sesión 04 y **U10–U12** a la Sesión 05. Ninguna unidad se eliminó: es un reorden. Consecuencias: hay **dos sesiones dobles** (S04 y S05) y la **Sesión 06 queda como taller de cierre sin contenido evaluable nuevo**. La fuente vigente de títulos y detalles es `sesiones_cun.py`.

**Metodología que pide el Syllabus:** núcleos problémicos integradores, plan de aula concertado en el acuerdo pedagógico, ABP, apoyo en segundo idioma, metodología BANG y **pruebas estándar tipo ICFES-SABER PRO al finalizar cada corte** (arts. 47 y 48 del Reglamento Estudiantil). Esa última línea es justamente lo que en el aula son los **parciales**: cuestionarios de selección, no ensayos. Metodologías complementarias marcadas en el documento: **clase magistral** y **seminario-taller**.

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
| **Quiz 1** | Cuestionario | 1 | 6% | 20/08/2026 | 27/08/2026 | 27/08/2026 |
| **Parcial 1** | Cuestionario | 1 | 24% | 21/08/2026 | 28/08/2026 | 03/09/2026 |
| **Quiz 2** | Cuestionario | 2 | 9% | 28/08/2026 | 06/09/2026 | 13/09/2026 |
| **Parcial 2** | Cuestionario | 2 | 21% | 06/09/2026 | 13/09/2026 | 20/09/2026 |
| **ACA Final** | Tarea | 3 | 32,8% | 13/08/2026 | 12/09/2026 | 20/09/2026 |
| **Quiz 3** | Cuestionario | 3 | 4% | 11/09/2026 | 12/09/2026 | 20/09/2026 |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 13/09/2026 | 20/09/2026 | 20/09/2026 |
| **Coevaluación** | Foro | 3 | 1,6% | 13/09/2026 | 20/09/2026 | 20/09/2026 |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Ventanas fijadas por el Docente (2026-08-10) sobre la estructura real del aula en CDigital: los quices y parciales son cuestionarios y cierran en día de clase (la Sesión 01 es de encuadre y no evalúa); la ACA Final es una tarea y cierra en la fecha máxima de recepción de trabajos; auto y coevaluación van de la última semana al cierre de notas.

## 4. Grupo actual (2026)

Fuente editable: `config/cursos/carga_academica_2026.json` (Excel origen: `Carga academica 2026.xlsx`).

| Grupo | Id_grupo | Periodo | Bloque | Inicio | Recepción | Cierre | Cupo / inscritos |
|---|---|---|---|---|---|---|---|
| 53339 | 795383 | 26P03 | SEGUNDO BLOQUE | 10/08/2026 | 12/09/2026 | 20/09/2026 | 50 / **20** |

**Aula en CDigital:** <https://cdigital.cun.edu.co/course/view.php?id=111070> · Modalidad **Virtual** (Google Meet) · Unidad **FINVV — Formación Investigativa Virtual** · Dependencia Formación Investigativa · Regional Bogotá.

> **Cuidado con la palabra «recepción».** Solo el **inicio (10/08/2026)** y el **cierre / registro de notas (20/09/2026)** son fechas institucionales de la carga académica. La **recepción del 12/09/2026 no viene en el Excel**: se derivó como fecha operativa a unos 8 días del cierre para dejar margen de calificación, y así está anotado en `carga_academica_2026.json`. Anúnciala a los estudiantes como **la fecha en que cierra la entrega en el aula** —que es lo que la vuelve real— y no como una fecha oficial de la Universidad; si algún periodo necesita moverla, se puede.

## 5. Cómo guiar cada sesión

### 5.1 La hora: cómo se reparte de verdad

Son **60 minutos y no hay bloque de tutoría**. Esta es la estructura REAL, contada en los seis guiones (todos suman 60 min exactos):

| Fase | S01 | S02 | S03 | S04 | S05 | S06 | Qué haces |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Encuadre | 10 | 6 | 8 | 6 | 6 | 6 | Retomas lo pendiente y pones en pantalla los avances de ellos. |
| Contenido y modelación | 24 | 22 | 14 | 20 | 16 | 16 | Explicas con el deck, modelas con un ejemplo y lo bajas a **su** tema. |
| **Taller** | 18 | 12 | 8 | 11 | 8 | **22** | Ellos producen, tú circulas. Es la fase que primero se sacrifica y la que más rinde: no la sueltes sin pelear. |
| Evaluación en clase | — | 12 | 22 | 15 | 22 | 8 | Solo en las sesiones que cierran un ítem. **No es tiempo adicional**: el guion ya recortó las otras fases. |
| Cierre y anuncio | 8 | 8 | 8 | 8 | 8 | 8 | Qué abre y qué cierra en CDigital, y qué traer. El guion trae la frase literal. |

Lo que se ve en la tabla: **cuando cae un parcial, el contenido baja a la mitad**. La S03 y la S05 tienen 22 minutos de cuestionario y solo 14 y 16 de explicación. No es un defecto del plan: es la consecuencia de meter cinco cuestionarios en seis encuentros de una hora. Prepara esas dos sesiones sabiendo que vas a explicar poco y que el peso cae en la lectura previa.

Antes de la sesión, publica en CDigital el material y la lectura: en aula invertida esto no es opcional. Después, califica dentro de la ventana de «nota docente» y publica retroalimentación.

Cada guion trae el minuto a minuto y el texto casi literal; el estándar del proyecto es que cubran **toda** la hora (`config/universidades/cun.json` → `pedagogia`).

### 5.2 Dónde están el guion y el deck

Los dos comparten el mismo nombre de sesión:

- **Guion (docente):** `Docente/Guiones/Sesion NN - <título>.md`
- **Deck (estudiante):** `Clases/Sesion NN - <título>/Presentacion.pptx`

Además, el **encuadre del semestre** tiene su propio deck: `Clases/Presentacion del Curso - Investigacion Ciencia y Tecnologia.pptx`.

**La penúltima slide de todos los decks de sesión es `RUTA DE ENTREGABLES DEL CURSO`, y no se edita.** La escribe `config/slides/ruta_entregables.py` con los ítems del libro de calificaciones, su tipo, su peso y —en **número de sesión, nunca en fecha**— el punto del curso en que cierra cada uno, más una línea de qué tiene que tener listo el estudiante. Te sirve para cerrar la clase en treinta segundos («esto es lo que viene»); y como no hay fechas escritas, cuando el próximo periodo mueva el calendario se recoloca sola sin reeditar deck alguno. La **fecha** exacta de cada ventana sigue viviendo solo en el enunciado del ACA y en CDigital, que es lo que manda.

### 5.3 Sesión por sesión

| # | Fecha | Título de la sesión (usa este nombre exacto para el guion y la carpeta del deck) | Qué haces tú en el encuentro | Qué se espera del estudiante | Deck |
|:-:|---|---|---|---|:-:|
| **01** | 13/08 | Presentación del curso · docente · estudiantes · ACAs | **Encuadre: no dictas tema.** Presentas curso, docente y evaluación con los nombres reales del aula; rompehielos en Padlet; anuncias que **Quiz 1 y ACA Final abren hoy**. | Se presenta en el Padlet y sale con la lectura autónoma asignada (U1–U2) y su tema tentativo por escribir. | 21 slides |
| **02** | 20/08 | MinCiencias · 6 líneas de Ingeniería · elección de línea | Retomas U1–U2 con las dudas de la lectura, explicas el SNCTI y las 6 líneas, y **haces que cada quien elija línea hoy**. Aplicas el **Quiz 1** (~12 min). | Llega con dos dudas escritas y su **tema tentativo** (actor + fenómeno + contexto) subido a CDigital; sale con línea elegida. | 19 slides |
| **03** | 27/08 | Prueba parcial · 1.er avance del artículo | Bajas la ansiedad del primer avance: qué es y qué no es, título, introducción en tres párrafos, tipos de conocimiento y fuentes. Aplicas el **Parcial 1** (~22 min, el 24%). | Trae el primer avance: portada, introducción breve, problema tentativo y fuentes iniciales. | 22 slides |
| **04** | 03/09 | Problema y pregunta · bases de datos y gestores de citas | **Sesión doble (U6 + U8).** Espina de pescado, árbol de problemas y método 3D hasta la pregunta; luego Scholar, SciELO, Redalyc y biblioteca CUN, operadores de búsqueda y APA 7 con ZoteroBib. Aplicas el **Quiz 2** (~15 min). | Sale con **una pregunta de investigación escrita** y con su primera búsqueda hecha con operadores. | 31 slides |
| **05** | 10/09 | Planteamiento del problema · marco teórico y revisión de literatura | **Sesión doble (U7 + U10–12) y última clase con contenido evaluable.** Estado actual, evidencias, causas y vacío; constructos, posturas teóricas, fichas de lectura y primera página de marco. Aplicas el **Parcial 2** (~22 min). **Aquí anuncias que ACA Final y Quiz 3 cierran antes del próximo encuentro.** | Sale con el planteamiento redactado y la matriz de fuentes empezada; le quedan dos días para consolidar la entrega. | 35 slides |
| **06** | 17/09 | Socialización del artículo y cierre del curso | **Taller de cierre, sin evaluación nueva:** la ACA Final y el Quiz 3 ya cerraron. Ronda de socialización, retroalimentación entre pares, ruta hacia semillero y trabajo de grado. Abres **autoevaluación** (cuestionario) y **coevaluación** (foro) y los haces diligenciar en clase (~8 min). | Presenta su artículo al grupo, comenta el de un compañero y deja diligenciados los dos instrumentos de cierre. | 21 slides |

### 5.4 Las dos sesiones dobles: cómo no perder la hora

S04 y S05 llevan **dos unidades cada una y además un cuestionario**. Los decks dan para dos horas y la hora no crece. La regla que ya aplican los guiones —y que conviene decir en voz alta al empezar— es esta: **el deck completo es el material de estudio de la semana; en clase se proyecta lo priorizado y las slides que no alcanzan se anuncian por su nombre** como recorrido guiado de trabajo autónomo. Es la única forma honesta de cerrar el temario adelantado sin dejar al estudiante sin el material.

### 5.5 La Sesión 06 llega después de la recepción

El 17/09 es posterior al cierre de la ACA Final (12/09) y del Quiz 3 (12/09). **No sirve para presionar entregas ni para dictar algo que se vaya a evaluar**: sirve para devolver, socializar y cerrar bien. Trátala como lo que es y no como una clase de contenido perdida.

## 6. Qué le entregas tú a la Universidad

### Durante el periodo

| Qué | Cuándo | Dónde |
|---|---|---|
| Alistamiento completo del aula (bienvenida, Syllabus, cortes, enlace de Meet, material de la S01) | **Semana 1**, antes del 13/08/2026 | CDigital |
| Socializar la evaluación Art. 52 con **los nombres reales del aula** (no «las tres ACAs») | Sesión 01 · 13/08/2026 | Encuentro + CDigital |
| **Crear la actividad** de cada cuestionario (no basta el ítem del libro de calificaciones) | Antes de su apertura: Quiz 1 → 13/08 · Parcial 1 → 21/08 · Quiz 2 → 28/08 · Parcial 2 → 04/09 · Quiz 3 → 11/09 | CDigital |
| Abrir la **tarea** ACA Final | 13/08/2026 (queda abierta todo el periodo) | CDigital |
| Calificar con retroalimentación cualitativa **y** cuantitativa | Quiz 1 → 27/08 · Parcial 1 → 03/09 · Quiz 2 → 10/09 · Parcial 2 → 17/09 · ACA Final, Quiz 3, Auto y Coev → 20/09 | Libro de calificaciones de CDigital |
| Habilitar **Autoevaluación** (cuestionario) y **Coevaluación** (foro) | Ventana 17/09 → 20/09/2026 | CDigital |
| Acuerdo pedagógico de inicio | Semana 1 | 🔴 **Canal por confirmar con Coordinación.** No uses el formulario AFI de Proyecto I/II. |
| Mantener las evidencias en el aula (Drive y correo **no** sustituyen a CDigital) | Continuo | CDigital |

> Esta tabla **no la regenera ningún script**: si cambian las ventanas en `fechas_entrega_aca.py`, corre `sync_manuales_fechas.py` y después actualiza esta tabla a mano.

### Al cierre (20/09/2026)

| Qué | Plazo | Nota |
|---|---|---|
| **Todas las calificaciones registradas**, los 8 ítems | **domingo 20/09/2026** — fecha de cierre del grupo en la carga académica | Es la fecha institucional dura del periodo |
| Comunicar notas definitivas y ventana de revisión | Antes del cierre | Reglamento Estudiantil vigente |
| **Descarga y respaldo de evidencias** (entregas, foros, calificaciones) | Antes del cierre del aula | Una vez cerrada, puedes perder el acceso |
| Informe / formato de cierre de pregrado | 🔴 **Por confirmar** | Puede que no exista para pregrado; **no** uses el formulario de informe final de AFI |
| Cierre formal de notas en el sistema que indique la Escuela | 🔴 **Por confirmar** si el canal es solo CDigital o también el portal académico | — |

### Lo que NO tienes que hacer en este curso

- **No hay formulario de registro de sesiones ni de asistencia a tutorías.** Esos son de AFI/Especializaciones (Proyecto I y II) y no aplican a pregrado.
- **No hay tutorías obligatorias por grupo** ni horas de acompañamiento comprometidas fuera del encuentro.
- **No hay que configurar equipos de trabajo en el aula.** A diferencia de Proyecto I, aquí el producto es **individual** (el propio enunciado sugiere nombrar el archivo `INV_ACAFinal_Apellido`). No crees grupos ni actividad de «elección de grupo»: la entrega es de cada estudiante.

## 7. Qué te entregan los estudiantes

Ocho ítems, y **solo uno es un documento**. Los cuestionarios se resuelven dentro del aula: no se sube archivo, no usan plantilla APA y su documento en `Clases/Recursos/ACAs/` es **la guía de qué entra**, no el examen.

### Los cuestionarios (Quiz 1/2/3 y Parcial 1/2)

Cada guía le dice al estudiante exactamente qué sesiones entran, con la regla «lo que se dicta el mismo día del cierre **no** entra». Ese es el recorte que tu banco de preguntas debe respetar:

| Ítem | Qué entra | Qué revisas |
|---|---|---|
| **Quiz 1** (6%) | Solo la **lectura autónoma de la S01** (U1–U2) y lo publicado en CDigital. Ninguna sesión de tema cerró todavía. | Que reconozca el producto del curso y las etapas del método científico. Es diagnóstico: sirve para ver quién arrancó. |
| **Parcial 1** (24%) | Añade la **S02** (MinCiencias, SNCTI, 6 líneas). | Que distinga las 6 líneas y ubique su tema en una. Es el ítem más pesado del corte 1: prepáralo con tiempo. |
| **Quiz 2** (9%) | Añade la **S03** (primer avance: título, introducción, tipos de conocimiento y fuentes). | Que sepa qué va en un avance y qué es una fuente confiable. |
| **Parcial 2** (21%) | Añade la **S04** (problema, causas, pregunta, bases de datos, APA 7). | Que diferencie deseo de producto y problema de investigación, y que sepa buscar y citar. |
| **Quiz 3** (4%) | Añade la **S05** (planteamiento, posturas teóricas, marco). | Cierre conceptual. **Cae fuera de día de clase (12/09)**: nadie se lo va a recordar, avísalo en la S05. |

> El número de preguntas, el tiempo y los intentos los defines tú al crear la actividad; lo que diga CDigital es lo que aplica. Las guías ya le advierten eso al estudiante.

### ACA Final — Artículo de nuevo conocimiento (tarea · 32,8% · cierra 12/09/2026)

Único entregable documental del curso. Es acumulativo: se construye entre las Sesiones 02 y 05. Debe contener título y autoría, introducción con la línea de Ingeniería elegida, problema y pregunta con evidencias y causas, objetivos si su ruta los exige, marco teórico / revisión de literatura en progreso con **matriz de fuentes** (autor, año, aporte, relación con la pregunta) y referencias en APA 7. Formato: plantilla APA CUN, 10–15 páginas acumuladas, entrega solo por CDigital.

**Criterios con los que se califica** (los mismos del enunciado del estudiante, para que no haya sorpresa):

1. Línea de Ingeniería explícita y pertinente.
2. Problema argumentado con evidencias, no una opinión.
3. Pregunta clara y **viable en un periodo de seis semanas**.
4. Fuentes confiables y matriz de fuentes completa.
5. Marco/revisión **alineado a la pregunta**, no un listado desconectado.
6. Citas y referencias APA 7 · integridad académica.
7. Mejoras frente a los avances previos.

El criterio 7 es el que hace que valga la pena la retroalimentación de los cortes 1 y 2: si el estudiante no ve devolución, no hay nada que incorporar.

### Autoevaluación (cuestionario · 1,6%) y Coevaluación (foro · 1,6%) — ventana 17/09 → 20/09

**No son ACAs.** La autoevaluación la diligencia cada quien sobre su propia trayectoria; la coevaluación es un **foro**: el estudiante publica su aporte valorando el trabajo y los aportes de sus compañeros. Si no publica, no participó. No hay archivo, no hay plantilla, no hay vocero. Tú las habilitas, verificas cumplimiento y registras la nota antes del 20/09. Se diligencian en la Sesión 06, en clase.

### Formato de entrega (para lo documental)

Plantilla `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` (o equivalente en Google Docs) · **APA 7** en citas y referencias · entrega **solo por CDigital** · herramientas gratuitas y en la nube (Google Docs/Word Online, Scholar, SciELO, Redalyc, biblioteca virtual CUN, ZoteroBib `https://zbib.org/`): no se exige software de escritorio de pago.

## 8. Configuración técnica — hazlo tú en la semana 1

### 8.1 El aula de CDigital

Aula del curso: **<https://cdigital.cun.edu.co/course/view.php?id=111070>** (fuente: `carga_academica_2026.json` → `cursos.investigacion.cdigital`). Es el enlace que ya aparece impreso en los ocho enunciados del estudiante, así que **no lo cambies sin regenerarlos**.

Antes del 13/08 el aula debe tener: mensaje de bienvenida, Syllabus, el deck de la Presentación del Curso, el enlace de Meet publicado, el material y las lecturas de la Sesión 01, y los 8 enunciados de `Clases/Recursos/ACAs/`. Y, sobre todo, **la actividad de Quiz 1 creada** —no solo su ítem en el libro de calificaciones—, porque abre ese mismo día.

Verifica también que la suma de pesos del libro de calificaciones dé **30 + 30 + 40 = 100** y que cada ítem tenga el **tipo correcto**: la coevaluación tiene que ser **foro**, no cuestionario.

### 8.2 Grupos

**No aplica.** El producto de este curso es individual. Deja el aula sin modo de grupo y no crees actividad de elección de grupo: si la creas, la entrega individual empieza a pedir pertenencia a un grupo y se te bloquean estudiantes.

### 8.3 Encuentro sincrónico (Google Meet)

Un **único enlace de Meet para toda la serie** de 6 encuentros, jueves 5:00–6:00 pm. Créalo desde tu cuenta institucional, publícalo en CDigital y en Avisos, y **pégalo en `config/cursos/carga_academica_2026.json` → `cursos.investigacion.meet`**: mientras esté vacío, todo el material generado seguirá mostrando el marcador `[URL Meet — …]`. Después de pegarlo, regenera el material que lo cita. Graba los encuentros: es la evidencia de que la sesión se dictó y el respaldo para quien no pudo conectarse (el curso es virtual y son solo seis clases).

> **Coanfitrión:** la regla de asignar a `investigacion_especializaciones@cun.edu.co` como coanfitrión obligatorio es del instructivo **AFI de Especializaciones** y no aplica a este curso. No lo agregues por analogía.

### 8.4 Los eventos en Google Calendar

**No los crees a mano y no importes el `.ics`.** Google Calendar descarta la lista de invitados al importar `.ics`/`.csv`, así que los 20 estudiantes se perderían. El flujo correcto es el Apps Script `PRINCIPAL - Crear encuentros con invitados.gs`, que crea los 6 eventos con invitados y con la misma sala de Meet, y es idempotente.

**Paso a paso completo (no lo dupliques aquí, síguelo allá):**
`Pregrado/Investigacion en ciencia y tecnologia/2026/53339/LEEME - Crear los eventos de Calendar.md`

En esa misma carpeta está `Entregas y hitos docentes - Importar a Calendar.csv`, que **sí** se importa: son tus recordatorios de cierres y límites de nota, sin invitados. Regenerar: `python config/slides/build_calendar_encuentros.py investigacion` y `python config/slides/build_hitos_docentes_calendar.py`.

### 8.5 Rompehielos

Tablero Padlet del curso: <https://padlet.com/andres_dfx/cun-wruz81hmf9k06gd7>. Es **el mismo tablero y el mismo momento** que el de la Presentación del Curso —la Sesión 01 *es* la sesión de presentación—, no dos rompehielos distintos.

## 9. Integridad académica

- El Syllabus lo pone como elemento de competencia del **SER**: «reconoce y mantiene la escritura de su proceso de investigación bajo parámetros del respeto de los derechos de autor». Es criterio de calificación de la ACA Final, no una recomendación.
- **Toda cita, en APA 7**, con lista de referencias al final. La matriz de fuentes es justamente la herramienta que hace visible de dónde salió cada afirmación: úsala para detectar el marco teórico copiado.
- **No hay un umbral de similitud institucional confirmado para pregrado.** El ≤10 % que circula viene del instructivo de rúbricas de **Proyecto I/II (AFI)** y no se puede extrapolar aquí. Si usas un detector, trátalo como insumo cualitativo: un porcentaje alto **no** es plagio automático, exige tu análisis y debido proceso según el Reglamento Estudiantil (<https://cun.edu.co/somos-la-cun/normatividad/>).
- **Texto generado por IA:** el producto debe ser inédito y con la perspectiva del estudiante (Syllabus). El punto de control práctico es la **Sesión 06**: quien socializa su artículo y no puede explicar su propia pregunta ni sus fuentes, deja evidencia por sí solo.
- En los cuestionarios, la integridad se juega en el diseño: banco de preguntas amplio, orden aleatorio y tiempo ajustado. Con 20 estudiantes es perfectamente manejable.

## 10. Checklists accionables

### Antes de la Sesión 01 (13/08/2026)

- [ ] Enlace de Meet creado, publicado en CDigital y **pegado en `carga_academica_2026.json`**.
- [ ] Eventos de Calendar creados con el `.gs` (runbook: `2026/53339/LEEME - Crear los eventos de Calendar.md`) y CSV de hitos docentes importado.
- [ ] Aula alistada: bienvenida, Syllabus, decks, lecturas de la S01 y los 8 enunciados de `Clases/Recursos/ACAs/`.
- [ ] **Quiz 1 creado como actividad** con su banco de preguntas (abre el 13/08, cierra el 20/08).
- [ ] **ACA Final creada como tarea** y abierta (13/08).
- [ ] Libro de calificaciones verificado: 8 ítems, tipos correctos (coevaluación = **foro**), 30 + 30 + 40 = 100.
- [ ] Guion de la Sesión 01 leído completo; Padlet abierto y probado.
- [ ] Acuerdo pedagógico: canal consultado con Coordinación.

### Antes de cada cuestionario

- [ ] Actividad creada en CDigital, con ventana, tiempo, intentos y aleatorización definidos.
- [ ] Preguntas **dentro del recorte** que declara su guía (nada de la sesión que se dicta ese mismo día).
- [ ] Minutos de aplicación reservados en el plan de clase (ya vienen en el guion).
- [ ] Anuncio hecho en la sesión anterior, con las palabras del guion.
- [ ] Nota y retroalimentación cargadas antes de su fecha límite.

### Antes del cierre de la ACA Final (12/09/2026)

- [ ] En la **S05 (10/09)** anunciado que la ACA Final **y** el Quiz 3 cierran antes del próximo encuentro.
- [ ] Retroalimentación de los cortes 1 y 2 publicada — si no, el criterio «mejoras frente a los avances previos» no es evaluable.
- [ ] Revisado quién no ha subido nada y contactado; con 20 estudiantes se puede hacer uno por uno.
- [ ] **Quiz 3 creado** (abre el 11/09, cierra el 12/09).

### Antes del cierre del periodo (20/09/2026)

- [ ] Autoevaluación (cuestionario) y coevaluación (foro) habilitadas el 17/09 y diligenciadas en la Sesión 06.
- [ ] **Los 8 ítems calificados** con retroalimentación en el libro de calificaciones.
- [ ] Notas definitivas y ventana de revisión comunicadas a los estudiantes.
- [ ] Evidencias descargadas y respaldadas **antes** de perder acceso al aula.
- [ ] Confirmado con Coordinación si hay informe de cierre de pregrado y por qué canal se cierran las notas.
