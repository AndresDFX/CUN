# Plan de viabilidad — ExamLab (PROYECTO I · ESP329 · 54ES4 · 26ES4)

| Campo | Valor |
|---|---|
| Curso | PROYECTO I (**ESP329**) |
| Programa | Especialización en Inteligencia Artificial |
| Grupo / Periodo | **54ES4** / **26ES4** |
| Docente | Julian Andres Castaño · `julian_castanoe@cun.edu.co` |
| Modalidad / Horario | Virtual (Google Meet) · **lunes 8:00–10:00 pm** (2 h) |
| Estudiantes | **40** (→ ~14 equipos de ≤3) |
| Plataforma oficial CUN | **CDigital (Moodle)** — no negociable |
| Herramienta evaluada | **ExamLab** (`examlab.lovable.app`) |
| Fecha | 2026-08-08 (fechas ACA actualizadas 2026-08-09) |
| Estado | **Borrador para aprobación docente** |

> **Nota 2026-08-09:** las fechas de Quiz/ACA 1/ACA FINAL/coevaluación/autoevaluación de este plan se actualizaron para usar la **Cronograma OFICIAL de Coordinación** (`Calendario de clases (oficial).md`, raíz de Proyecto I), la misma fuente ya adoptada en el Manual del Docente. Esto **resuelve el §11(a)** de este documento, que quedaba abierto — ver el cierre de esa sección más abajo. Las fechas de sesión (10/08, 24/08, 31/08…) no cambiaron.

> **Nota 2026-08-11 · nombres de los ítems.** Este plan se escribió con la numeración del Syllabus ESP329 (ACA 1 / ACA 2 / ACA 3). La auditoría del aula (2026-08-10) mostró que **CDigital los llama distinto**, y ese es el nombre que usan hoy el gradebook, el `Calendario de clases (oficial).md` y los enunciados del estudiante. Todo el documento quedó reescrito con los nombres del aula: **Quiz** (cuestionario, 25%, corte 1 — era «ACA 1») · **ACA 1** (tarea, 25%, corte 2 — era «ACA 2») · **ACA FINAL** (tarea, 42%, corte 3 — era «ACA 3»). Ojo con la trampa que dejaba la numeración vieja: **lo que cierra el 30/08 es el Quiz**, no la ACA 1, que cierra el **04/10**.

---

## 1. Resumen ejecutivo

**Veredicto: viable condicionado — SOLO como complemento de CDigital, nunca como reemplazo.**

Hay dos razones, y la primera es institucional, no técnica:

1. **CUN exige la entrega en CDigital.** Los 5 enunciados de ACA lo dicen en la misma línea de cabecera: *"Entrega oficial: solo por CDigital"*. El Manual del Docente (L95, L151-156) pone ahí las entregas, el gradebook y el registro de notas, y fija el cierre único el **22/11/2026**. Ninguna decisión sobre ExamLab puede mover eso.
2. **ExamLab no puede recibir el entregable de este curso.** Verificado en código, en tres capas: no existe un tipo de pregunta "subir documento" (los 12 tipos vigentes son texto, código, consola, GUI, SQL y diagrama); los únicos `<input type="file">` para el estudiante aceptan `.zip` o extensiones de código; y el calificador IA **rechaza activamente** archivos no-código dentro del ZIP (`ai-grade-submission/index.ts:1626-1639`). El entregable documental (**ACA 1** y **ACA FINAL**) en **Plantilla APA CUN** — Times New Roman 12, márgenes 3 cm, espaciado 1,5, portada, paginación — no entra a ExamLab como entrega.

Sumado a eso: **la coevaluación (4%) y la autoevaluación (4%) no existen en ExamLab.** No es un tema de configuración; **no hay ninguna tabla en la que un `user_id` califique a otro**, y la RLS lo impide por diseño (un estudiante no puede leer la entrega de un compañero). Se registran como nota, no se diligencian.

**Lo que sí queda, y es más de lo que parece:** ExamLab calza *exactamente* con el andamiaje ESP329 — pesos 25/25/42/4/4 sobre escala 0–5 con aprobatoria 3 **sin reconfigurar nada**; equipos con entrega compartida que replican la regla de Moodle *"solo un integrante sube"*; **notas externas con observación** (que es literalmente lo que el Manual L92 pide: *"retro cualitativa y cuantitativa"*); **hilo de retroalimentación por sección con adjuntos de cualquier tipo** (25 MB — aquí sí entra el `.docx` anotado); y un **Tutor IA que lee el contenido real** de la plantilla APA y de los 5 enunciados.

| Criterio | Resultado |
|---|---|
| Recibir el ACA en plantilla APA (`.docx`/`.pdf`) | **No** — bloqueado en 3 capas del código |
| Registrar nota + retro cualitativa de cada ACA | **Sí** (actividades externas, hoy, sin desarrollo) |
| Pesos ESP329 25/25/42/4/4 en 3 cortes | **Sí, exacto** (suman 100; escala 0–5 y aprobatoria 3 por defecto) |
| Equipos de ≤3 con una entrega y una nota | **Sí** (`group_required`); el tope de 3 **no lo valida el sistema** |
| Coevaluación 4% como instrumento | **No existe** — solo se registra el número |
| Autoevaluación 4% como instrumento | **No existe** — solo se registra el número |
| Rúbrica estructurada con criterios ponderados | **No existe** — `expected_rubric` es texto libre |
| Similitud tipo Turnitin (≤10% depurada) | **No** — solo compara entre entregas del curso, y **trunca a 3.000 caracteres** |
| Retro por sección + `.docx` anotado de vuelta | **Sí** (hilo de feedback por pregunta, adjuntos sin filtro de MIME) |
| Tutoría asincrónica sobre el material real | **Sí** (Tutor IA extrae texto de `.docx`/`.pptx`) |
| Integración / sincronía de notas con CDigital | **No existe** — sin LTI, sin API. Puente manual (export XLSX/CSV) |

**Recomendación:** adoptar ExamLab como **capa de seguimiento y retroalimentación** del curso (notas consolidadas, retro por sección, tutor IA, evidencia de sesiones, difusión programada) y **dejar en CDigital las 5 entregas oficiales, la coevaluación y la autoevaluación**. No pilotear la entrega de documentos en ExamLab en 26ES4.

---

## 2. La restricción que define el veredicto

Esto no es una preferencia del docente; está escrito en el material que los estudiantes ya recibieron.

| Fuente | Texto |
|---|---|
| Los 5 enunciados ACA (cabecera idéntica) | *"Entrega oficial: solo por CDigital"* |
| Manual L151-156 | Plantilla institucional obligatoria · APA 7 · portada con todos los integrantes · **"Solo un integrante sube"** |
| Manual L95, L103 | Gradebook y registro de notas en CDigital · **"Todas las notas en Moodle a más tardar el 22/11/2026"** |
| Manual L160-168 | Configuración obligatoria de grupos **en Moodle** en semana 1, con la advertencia *"No cambies esta configuración después de recibir entregas"* |
| Manual L98 | Coevaluación y autoevaluación se **habilitan en CDigital** |

**Consecuencia directa:** cualquier cosa que ExamLab haga es *adicional*. Si ExamLab y CDigital discrepan en una nota, **CDigital manda**. Y como el registro oficial vive allá, ExamLab introduce un riesgo real de **doble fuente de verdad** que hay que administrar explícitamente (ver §10, riesgo R1).

> ⚠️ Dato operativo del Manual que juega **a favor** de ExamLab: *"una vez cerrada el aula, NO se puede volver a entrar"* (L102, descarga de evidencias antes del cierre). ExamLab sirve como **archivo permanente** de notas, retro y evidencia de sesiones después del 22/11 — algo que CDigital no le deja al docente.

---

## 3. Los tres bloqueos (verificados en código, no supuestos)

### 3.1 No se puede entregar un documento

| Capa | Evidencia |
|---|---|
| Tipos de pregunta | CHECK vigente: `abierta, cerrada, cerrada_multi, codigo, diagrama, java_gui, python_gui, codigo_zip, red_consola, red_gui, so_consola, bd_sql`. **No hay `documento` ni `archivo`.** |
| UI de entrega | Los únicos `<input type="file">` del estudiante aceptan `.zip` o `LANG_TO_EXT[langKey]` (extensiones de código), con whitelist que **rechaza el submit** |
| Calificador IA | `cleanedAllowed = … Array.from(CODE_EXT)` — 60+ extensiones de código, **sin `docx`, sin `pdf`** |
| Tabla que serviría | `project_submission_attachments` existe en DB con **0 referencias en `src/`** — no hay UI que escriba ni lea ahí |

**Hallazgo de bajo costo, para el registro:** el bucket `workshop-files` **ya admite** `application/pdf` y `…wordprocessingml.document` en su `allowed_mime_types`. El bloqueo es **100% de UI**, no de Storage ni de RLS. Habilitar un tipo de pregunta "documento" sería sobre todo UI + un tipo en 4 CHECK constraints. *No se propone hacerlo en este periodo* (ver §6).

### 3.2 No existe la coevaluación

Búsqueda exhaustiva (`coevaluac|peer_review|peer_grade|evaluator|grader_id`) sobre todo `src/` y `supabase/`: **cero resultados funcionales**. Los hits son clases CSS `peer-*` de Tailwind y el comentario `// peer-to-peer plagiarism`.

Lo más parecido y en qué falla:
- **Grupos** dan el universo (equipos de ≤3), pero la nota es **compartida**, no diferenciada por par.
- **Encuestas `mixed`** permiten preguntas abiertas y cerradas por estudiante, pero `poll_question_responses` **no tiene ninguna columna de puntaje**. Una encuesta no produce nota y no está conectada a los cortes.
- **`defense_factor`** de proyectos es un multiplicador 0..1 que pone **el docente**, no un par.

### 3.3 No existe la autoevaluación

Mismo resultado. El único hit de `autoevaluac` en todo el repositorio es una **plantilla de reporte para el docente** (*"Reporte los resultados de su autoevaluación del desarrollo del curso"*) — es la autoevaluación *del docente sobre su propio curso*, se imprime en PDF y no produce nota ni tiene participación del estudiante. **No es el instrumento del 4%.**

---

## 4. Lo que se puede hacer HOY, sin desarrollo y sin workaround

| # | Capacidad | Encaje ESP329 |
|---|---|---|
| 1 | **Pesos y cortes** (`grade_cuts` + peso por ítem como % de la nota final) | 25 + 25 + 42 + 4 + 4 = **100**. Corte I / II / III = 25 / 25 / 50, igual que el Calendario oficial |
| 2 | **Escala 0–5, aprobatoria 3** (`grade_scale_max` default 5, `passing_grade` default 3) | Coincide con la escala CUN (0,1–2,9 Insuficiente / 3,0–3,5 Aceptable / 3,6–4,5 Buen desempeño / 4,6–5,0 Excelente) **sin tocar nada** |
| 3 | **Actividades externas + editor de notas** (`is_external` + `ExternalGradesEditor`) | Grilla de los 40 matriculados con **Nota + Observación**. Cubre el Manual L92 (*retro cualitativa y cuantitativa*) para los 5 componentes |
| 4 | **Equipos con entrega y nota compartida** (`group_required`) | Replica *"Requerir pertenecer a grupo: Sí"* + *"Requerir que todos entreguen: No"* del Manual L165. Al calificar, notifica **a cada miembro** |
| 5 | **Hilo de retroalimentación con adjuntos** (`feedback_threads` + bucket `feedback-attachments`) | Un hilo **por pregunta**, docente y estudiante pueden escribir y adjuntar. `<input type="file">` **sin atributo `accept`** y bucket con `allowed_mime_types = NULL` → **el `.docx` anotado pasa**. 25 MB/archivo, 8 archivos/comentario |
| 6 | **Tutor IA que lee el material** (`tutor-chat` + `material-extract`) | Extrae texto real de `.docx`/`.pptx` (fflate + `docxXmlToText`), lo cachea, y el estudiante referencia archivos con `#`. Responde sobre la plantilla APA y los enunciados ACA |
| 7 | **Contenidos con `.pdf`/`.pptx`/`.docx`** | Las 11 `Presentacion.pptx`, la Plantilla APA y los 5 enunciados se cargan tal cual y se asignan por sesión. PDF e imágenes tienen **visor inline**; `.docx`/`.pptx` solo descarga |
| 8 | **Sesiones por CSV con `recording_url`** (8 columnas: `session_date, title, start_time, end_time, meeting_url, cut_name, recording_url, session_type`) | Las 11 sesiones se importan de un golpe, con el Meet reutilizable y **el enlace de grabación por sesión** — la evidencia que el Manual L94 exige en <24 h |
| 9 | **Difusión programada** (`scheduled_messages` + pg_cron) | Los recordatorios de las 5 ventanas se programan **de una vez en agosto**. Por difusión: 1 notificación + **1 solo correo con los 40 en BCC** (ningún alumno ve la lista) + réplica al inbox |
| 10 | **Foros con ventana `opens_at`/`closes_at`** | Discusión por unidad (U1–U7) y el rompehielos, con ventanas por fecha |
| 11 | **Export de notas a CSV y XLSX** desde el gradebook | El puente manual hacia CDigital para el cierre del 22/11 |
| 12 | **Informes y actas a DOCX real** (`html-to-docx`: membrete en `word/header1.xml`, tablas, imágenes) | Documento consolidado del curso + respaldo de evidencia **antes** de que CDigital cierre |

**Lectura:** el solapamiento real entre ExamLab y este curso es el **andamiaje**, no la evaluación. Y el andamiaje calza sorprendentemente bien: los pesos y la escala no requieren *ninguna* reconfiguración.

---

## 5. Lo que requiere workaround (y qué se paga por él)

### 5.1 Coevaluación 4% y autoevaluación 4% → recolectar fuera, registrar dentro

| | |
|---|---|
| **Cómo** | Se diligencian **en CDigital** (como manda el Manual L98). En ExamLab se crean dos talleres `is_external` ("Coevaluación" 4% y "Autoevaluación" 4%) y se digitan las 40 notas con su observación |
| **Qué se gana** | Los dos componentes aparecen en el consolidado y el Corte III suma 50 correctamente |
| **Qué se paga** | **Doble digitación** de 80 notas (40 + 40). El estudiante no diligencia nada en ExamLab |
| **Alternativa descartada** | Encuesta `mixed` en ExamLab para recolectar los juicios: técnicamente posible, pero las respuestas **no producen nota** y habría que transcribirlas igual. Añade una tercera plataforma sin quitar la digitación. **No recomendada** |

> ⚠️ El propio material CUN deja sin documentar **cómo se deriva el 4% de las respuestas** (el texto solo dice que el docente *"verifica y registra"*, y los checklists de los enunciados son de **cumplimiento**, no de desempeño graduado). Mientras eso no esté definido, el workaround es fiel al documento: se registra un número que el docente decide. *(Observación, no propuesta.)*

### 5.2 Retro por sección del ACA → talleres con una pregunta `abierta` por sección

`feedback_threads` es único por `(parent_kind, question_id, submission_id)` → **un hilo por pregunta**. Si el ACA se modela con una pregunta `abierta` por sección de la plantilla (Planteamiento · Pregunta · Objetivo general · Objetivos específicos · Justificación · Alcances y limitaciones · Referencias), cada sección tiene su propio hilo con adjuntos.

**Pero esto implica que el estudiante pegue texto en ExamLab además de entregar en CDigital.** Para 40 estudiantes y 6–10 páginas por ACA, es doble trabajo con pérdida de formato (portada, paginación, tablas, APA — justo lo que la plantilla exige).

**Recomendación acotada:** NO espejar el ACA completo. Usar preguntas `abierta` **solo en las piezas cortas y de mayor apalancamiento**, donde el texto es un párrafo y no una sección:

| Pieza | Por qué ahí | Sesión |
|---|---|---|
| **Título del anteproyecto** (≤21 palabras, tono afirmativo, alineado al objetivo general) | Regla verificable y objetiva; error caro si llega mal a la ACA FINAL | 02–03 |
| **Pregunta de investigación** | Es el eje de coherencia de todo el Quiz | 02 |
| **Objetivo general** | Un párrafo; la IA detecta desalineación con la pregunta | 03 |

Tres piezas cortas, calificación IA formativa (nota **no** ponderada), hilo de feedback, y — dato verificado — **el texto de una pregunta `abierta` NO se trunca** al calificar con IA (los límites de 200.000 / 50.000 caracteres están en la rama de ZIP de código, no en la de texto). Cabe además bajo el cap de similitud de 3.000 caracteres, así que la detección entre equipos **sí funciona** en estas piezas.

### 5.3 Rúbrica ESP329 → prosa en `expected_rubric` + override del prompt por curso

No existe tabla de rúbrica: `expected_rubric` es una columna **TEXT libre** y `workshops.rubric JSONB` solo se copia al duplicar cursos (no hay UI de criterios). Los 5–6 criterios ponderados de cada ACA van como **texto**, no como datos: sin cálculo por criterio y sin vista de rúbrica para el estudiante.

Mitigación real: el use case `workshop_question` de `ai_prompts` acepta un **override por curso editable por el docente**, que gana sobre el global. Ahí se escribe el criterio ESP329 textual (Manual L199: *coherencia, pertinencia, rigor metodológico, calidad de fuentes, escritura académica, integridad y viabilidad*) en lugar del default, que está calibrado para código. **Solo se persiste el system prompt** — la rúbrica, la respuesta y el puntaje los inyecta el código, así que no hay riesgo de romper el contrato.

### 5.4 Tope de 3 integrantes → lo enforza el docente, no el sistema

`group_size_max` existe (default **5**) pero **sin UI, sin validación y sin trigger**: un equipo de 6 se crea sin error. **Por qué no muerde en este curso:** `self_signup` no está expuesto en la UI, así que **el docente es el único que puede crear y poblar grupos** (drag & drop). El tope de 3 lo controla su propia mano. El único trigger existente impide estar en >1 grupo del mismo taller, que sí es útil.

**Detalle a no olvidar:** con `group_required`, un estudiante **sin grupo queda bloqueado** para entregar. Los 40 deben quedar en un grupo, incluidos los que trabajen solos — exactamente la misma regla que el Manual L74 fija para Moodle (*"Estudiante individual → igual necesita un grupo propio"*). Con 40 estudiantes: **13 equipos de 3 + 1 individual**, o 12 de 3 + 2 de 2. *(Reparto inferido; los equipos reales no están documentados en ningún archivo del curso.)*

### 5.5 Trazabilidad de versiones Quiz → ACA 1 → ACA FINAL

Asimetría verificada: **los exámenes guardan historial** (cada intento es una fila nueva en `submissions`, con `retry_mode ∈ last|average|highest`); **talleres y proyectos NO** — es *una sola fila que se UPDATEa*, con un `attempt_count` explícito y **sin `retry_mode`**. Si un ACA se modelara como un taller reentregable, la reentrega **sobrescribiría** el texto anterior, su `ai_feedback` y el `teacher_feedback` — justo la trazabilidad que ACA 1 y ACA FINAL exigen.

**Workaround:** **tres entidades separadas** (Quiz, ACA 1, ACA FINAL) en tres cortes distintos, que es lo que el Calendario oficial ya llama Corte I/II/III. Se pierde el diff automático entre versiones, pero se conservan las tres notas y las tres retros. El ajuste que autoriza el Manual (*"si la **ACA FINAL** evidencia que el estudiante incorporó correcciones…, el docente puede ajustar favorablemente el **Quiz** y la **ACA 1**"*) se aplica editando la nota del ítem viejo — y el cambio queda con su observación.

---

## 6. Lo que requeriría desarrollo nuevo (fuera de alcance para 26ES4)

Se documenta para decidir en otro periodo, no para este.

| Necesidad | Alcance estimado *(inferido)* | Nota |
|---|---|---|
| Tipo de pregunta **"documento"** (`.docx`/`.pdf` como entrega) | Medio-bajo: UI de entrega + tipo en 4 CHECK constraints + rama de lectura | **Storage y RLS ya lo permiten** (`workshop-files` acepta PDF/DOCX). El bloqueo es de UI |
| **Coevaluación** entre pares | Alto: tabla nueva (`grader_id` → `graded_id`), RLS que abra lectura acotada entre miembros del mismo grupo, agregación a nota, UI | Es la brecha más estructural: hoy la RLS **impide** que un estudiante vea la entrega de otro |
| **Autoevaluación** como instrumento calificable | Medio: formulario por estudiante + derivación de nota + ítem ponderado | Podría compartir infraestructura con la anterior |
| **Rúbrica estructurada** (criterios ponderados, vista para el estudiante) | Medio-alto: tabla de criterios + cálculo + UI docente y estudiante + integración con el prompt de IA | Habilitaría los 5–6 criterios reales de cada ACA como datos |
| Ampliar el cap de similitud en texto largo | **Trivial**: `MAX_CHARS_PER_TEXT = 3000` es una constante de una línea en `detect-plagiarism/index.ts:43` | No convierte la herramienta en Turnitin (sigue sin corpus web) |
| Validación APA / conteo de antecedentes / verificación de DOI | Alto, y sin precedente en el repo | **No existe nada.** Turnitin no está integrado |
| Sincronía de notas con CDigital (LTI o API) | Alto y dependiente de CUN | Hoy el puente es export XLSX + digitación |

---

## 7. Reparto propuesto de responsabilidades

| Función | CDigital (oficial) | ExamLab (complemento) |
|---|---|---|
| Entrega de **ACA 1** / **ACA FINAL** (plantilla APA) | ✅ **Única** | ❌ Imposible |
| Coevaluación y autoevaluación (diligenciar) | ✅ **Única** | ❌ No existe |
| Registro oficial de notas (cierre 22/11) | ✅ **Fuente de verdad** | Espejo de seguimiento |
| Retro cualitativa por ACA | ✅ Requerida por AFI | ✅ **Observación por estudiante** + hilo con adjuntos |
| Devolver el ACA **anotado** al equipo | Posible | ✅ **Mejor**: hilo por sección, adjunto de cualquier tipo, 25 MB |
| Tutoría asincrónica sobre el material | — | ✅ **Tutor IA** sobre la plantilla APA y los 5 enunciados |
| Consolidado de pesos y cortes | ✅ Gradebook Moodle | ✅ **Cálculo automático** 25/25/42/4/4 sobre 0–5 |
| Evidencia de sesiones + grabación | Avisos | ✅ `recording_url` por sesión (evidencia AFI <24 h) |
| Recordatorios de ventanas ACA | Avisos manuales | ✅ **Programados en agosto**, 1 correo con BCC |
| Feedback formativo antes de entregar | — | ✅ IA sobre título / pregunta / objetivo general |
| Archivo permanente post-cierre | ❌ *"no se puede volver a entrar"* | ✅ **Queda todo** |
| Registro AFI (`forms.gle/6t6BX…`) e Informe Final | ✅ Google Forms | ❌ No lo reemplaza (sí produce el consolidado en DOCX) |

---

## 8. Configuración concreta del curso en ExamLab

### 8.1 Curso y escala

| Campo | Valor | Nota |
|---|---|---|
| Nombre | `Proyecto I — ESP329 — 54ES4 (26ES4)` | |
| `grade_scale_max` | **5** | default, no tocar |
| `passing_grade` | **3** | default; coincide con "Aceptable 3,0–3,5" |
| Matrícula | 40 estudiantes (`@cun.edu.co`) | El listado ODS y los 40 correos del Calendar cruzan exacto |

### 8.2 Cortes y pesos (suman 100)

| Corte | `weight` | Rango de fechas | `workshop_weight` | `attendance_weight` | Ítems |
|---|---:|---|---:|---:|---|
| **Corte I** | 25 | 10/08 – 30/08 | 25 | **0** | Quiz (25) |
| **Corte II** | 25 | 31/08 – 04/10 | 25 | **0** | ACA 1 (25) |
| **Corte III** | 50 | 05/10 – 22/11 | 50 | **0** | ACA FINAL (42) · Coevaluación (4) · Autoevaluación (4) |

> **`attendance_weight` = 0 en los tres cortes.** ESP329 no pondera asistencia. Si se pone >0, la suma de buckets deja de cuadrar con `cut.weight` y el consolidado se desvía.
>
> Rangos actualizados 2026-08-09 a la Cronograma OFICIAL (cierres 30/08 · 04/10 · 22/11). Los rangos reparten las 11 sesiones **2 / 5 / 4** (Corte I: 10/08, 24/08 · Corte II: 31/08, 07/09, 14/09, 21/09, 28/09 · Corte III: 05/10, 19/10, 26/10, 09/11) — cambió de 3/4/4 porque la sesión del 31/08 ahora cae **después** del nuevo cierre del Quiz (30/08), no en el mismo día. La pertenencia de una sesión a un corte **se deriva por `session_date` entre `cut.start_date` y `cut.end_date`**, no por FK: un corte mal fechado desplaza sesiones de corte.

### 8.3 Los 5 ítems

Los cinco como **talleres** (no proyectos): los talleres soportan `is_external`, grupos y — si más adelante se usan preguntas `abierta` — la detección de similitud sí funciona en talleres, mientras que para proyectos compara el *resumen que escribió la IA*, no el texto del alumno.

| Ítem | Tipo | `is_external` | `group_mode` | Peso | Cierre |
|---|---|---|---|---:|---|
| Quiz — Formulación del problema | Taller | ✅ | `group_required` | 25 | 30/08/2026 |
| ACA 1 — Fundamentación referencial | Taller | ✅ | `group_required` | 25 | 04/10/2026 |
| ACA FINAL — Anteproyecto integrado | Taller | ✅ | `group_required` | 42 | 08/11/2026 |
| Coevaluación | Taller | ✅ | `individual` | 4 | 15/11/2026 |
| Autoevaluación | Taller | ✅ | `individual` | 4 | 22/11/2026 |

> Fechas de cierre = Cronograma OFICIAL (actualizado 2026-08-09). Fechas límite de nota docente: Quiz 07/09 · ACA 1 12/10 · ACA FINAL 16/11 · coev./autoev. 22/11 (ver §8.5 y §9).

> Al ser `is_external`, se ocultan duración, navegación, proctoring y preguntas: el docente solo transcribe **Nota + Observación**.
>
> ⚠️ **La nota se ingresa en la escala del curso (0–5), no en `max_score` del ítem.** Está documentado en el código el bug que esto evita: *"Mantener max_score=100 acá producía que un '5' se interpretara como 5/100=0,25 al consolidar el corte."*

### 8.4 Talleres formativos NO ponderados (opcional, §5.2)

| Taller | Preguntas | Peso | Uso |
|---|---|---:|---|
| Borrador — Título, pregunta y objetivo | 3 × `abierta` | **0** | IA formativa + hilo por sección + similitud entre equipos |

Requiere: override del prompt `workshop_question` con el criterio ESP329, y decir en clase que **la nota que devuelve la IA no cuenta**.

### 8.5 Grupos, sesiones y difusión

- **Grupos:** crear los ~14 equipos por drag & drop en las semanas 2–3 (la misma ventana que el Manual L72 fija para Moodle). **Ningún estudiante sin grupo**, o queda bloqueado. Mantener el mismo reparto que en Moodle para que las notas sean comparables.
- **Sesiones:** un CSV de 11 filas con `session_date, title, start_time=20:00, end_time=22:00, meeting_url` (el Meet reutilizable), `cut_name` y `recording_url` (se llena después de cada clase, <24 h).
- **Contenidos:** subir las 11 `Presentacion.pptx`, `Plantilla_APA_CUN_Proyecto de grado.docx` y los 5 enunciados ACA; asignarlos a su sesión. Esto es lo que **alimenta al Tutor IA**.
- **Difusión programada (una sola sesión de trabajo en agosto):**

| Programar para | Mensaje |
|---|---|
| 24/08 | El **Quiz** (cuestionario, 25%) cierra el **30/08** · se resuelve en CDigital dentro de la ventana, no se sube documento |
| 28/09 | La **ACA 1** (tarea, 25%) cierra el **04/10** · plantilla APA · un solo integrante sube en CDigital · mínimo 6 antecedentes nacionales e internacionales |
| 26/10 | La **ACA FINAL** (tarea, 42%) cierra el **08/11** · anteproyecto **completo e integrado**, no un fragmento |
| 09/11 | **Coevaluación abierta** en CDigital (09/11–15/11) |
| 16/11 | **Autoevaluación abierta** en CDigital (16/11–22/11) · cierre de notas 22/11 |

---

## 9. Encaje por sesión

| # | Fecha | Tema | Uso de ExamLab |
|---:|---|---|---|
| 01 | 10/08 | Presentación y fundamentos | Alta de los 40 · subir contenidos · publicar Tutor IA · programar las 5 difusiones |
| 02 | 24/08 | Problema y pregunta | Cerrar equipos · **taller formativo**: pregunta de investigación · última clase antes del cierre del Quiz (30/08) |
| 03 | 31/08 | Objetivos, justificación, alcances | **Taller formativo**: objetivo general y título (≤21 palabras) · el **Quiz** ya cerró ayer (30/08) |
| 04 | 07/09 | Retroalimentación del **Quiz** · Antecedentes | **Registrar el Quiz** (nota + observación, límite hoy) · devolver el `.docx` anotado por el hilo de feedback |
| 05 | 14/09 | Marco teórico | Foro U4 · tutor IA para citación |
| 06 | 21/09 | Marco conceptual y contextual | Foro U4 |
| 07 | 28/09 | Marco legal · APA 7 | Última clase antes del cierre de la **ACA 1** (04/10) · tutor IA sobre los 22 pares cita↔referencia legal de la plantilla |
| 08 | 05/10 | Diseño metodológico (puente) | la **ACA 1** ya cerró ayer (04/10) · adelantar metodología (solo 2 lunes sincrónicos quedan para la ACA FINAL) |
| 09 | 19/10 | Población, técnicas e instrumentos | Encuesta `slot` para tutorías por equipo (ver nota abajo) |
| 10 | 26/10 | Planeación, viabilidad, integración | Tutorías por equipo · última clase antes del cierre de la ACA FINAL (08/11) |
| 11 | 09/11 | Integración · coev y autoev | la **ACA FINAL** ya cerró ayer (08/11) · hoy abre la ventana de **Coevaluación** (09/11–15/11) · explicar las dos ventanas |
| — | 12/10 | *(festivo — nota límite ACA 1)* | **Registrar ACA 1** (nota + observación, límite hoy) |
| — | 15/11 | *(cierre ventana coevaluación)* | Cierra la ventana de diligenciamiento de Coevaluación |
| — | 16/11 | *(festivo)* | **Registrar ACA FINAL** (nota límite hoy) · hoy abre la ventana de **Autoevaluación** (16/11–22/11) |
| — | 22/11 | Cierre | Registrar coev + autoev (nota límite hoy) · **exportar XLSX** → digitar en CDigital · generar consolidado DOCX |
| — | 25/11 | Post-cierre | Informe Final (Google Form) · ExamLab queda como archivo |

**Sobre tutorías (sesiones 09–10):** no existe módulo de agendamiento. El sustituto es la **encuesta tipo `slot`** (Doodle), con claim atómico de cupo y generador `fechas × ventana × paso`. **Dos limitaciones que hay que aceptar:** (a) el evento de calendario que genera **ignora la franja elegida** — lo ancla al cierre de la encuesta para todos, porque los labels de slot no llevan el año y parsearlos es ambiguo (limitación documentada en el propio código); (b) es **por curso, no por equipo**. Sirve para repartir cupos; el evento real sigue en Google Calendar.

**Festivos sin sincrónico:** 17/08, 12/10, 02/11, 16/11 → clase pregrabada en CDigital (Manual L181).

---

## 10. Riesgos

| # | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| **R1** | **Doble fuente de verdad de notas** (ExamLab vs CDigital) | **Alto** | Declarar por escrito que **CDigital es la oficial**. Digitar en ExamLab primero y exportar XLSX → CDigital en un solo movimiento por corte. Nunca al revés |
| **R2** | **Ítems sin nota cuentan como 0** con su peso original (no se reescalan) | **Alto** | Con la ACA FINAL al 42% cerrando el 08/11, todo estudiante verá una nota reprobatoria hasta noviembre. Opciones: explicarlo en la sesión 01, o desactivar el módulo de notas para el rol Estudiante — **ojo: `module_visibility` es por institución y rol, no por curso**, así que afectaría a todos los cursos del tenant *(inferido)* |
| **R3** | ~~Los **tres juegos de fechas ACA** no concuerdan~~ — **resuelto 2026-08-09** (ver §11) | — | Se adoptó la Cronograma OFICIAL en el Manual, el Calendario y este plan. Si se retoma este plan más adelante, verificar que ningún documento quedó con las fechas viejas (31/08 · 28/09 · 09/11) |
| **R4** | Estudiantes entienden que el ACA se entrega en ExamLab | **Alto** | Slide explícita en sesión 01: *"la entrega oficial es y sigue siendo CDigital"*. No crear en ExamLab ningún ítem que parezca recibir archivos |
| **R5** | **Doble digitación** de 5 × 40 = 200 notas (más coev/autoev) | Medio | Aceptado por diseño. Usar el editor de notas externas (grilla de 40 filas, una pasada por ítem) |
| **R6** | La IA formativa califica prosa académica con criterio calibrado para código | Medio | Override del prompt `workshop_question` por curso **antes** de la sesión 02. Y decir en clase que esa nota **no cuenta** |
| **R7** | Se confunde la similitud de ExamLab con el ≤10% depurada de Turnitin | Medio | **No lo es**: compara solo entre entregas del curso, sin corpus web, y **trunca a 3.000 caracteres**. No usarla como evidencia de plagio; el Manual L204-205 ya exige *análisis cualitativo con debido proceso* |
| **R8** | Un equipo queda con >3 integrantes | Bajo | `group_size_max` no se valida, pero `self_signup` no está expuesto → **solo el docente crea grupos**. Verificar al cerrar la semana 3 |
| **R9** | Estudiante sin grupo queda bloqueado (`group_required`) | Bajo | Los 40 en un grupo, incluidos los individuales — misma regla que Moodle |
| **R10** | Adjunto de retro >25 MB o >8 archivos | Bajo | Comprimir el `.docx` anotado o partirlo en dos comentarios |
| **R11** | El acta / consolidado **recalcula con datos vivos**, no congela notas | Bajo-medio | Documentado en el propio código. Generar el DOCX **después** del cierre del 22/11 y guardarlo como archivo, no regenerarlo |
| **R12** | Tercera plataforma → más carga para 40 estudiantes | Medio | Mantener el alcance mínimo: los talleres formativos son **opcionales** y solo sobre 3 piezas cortas. Si en la sesión 03 la adopción es baja, retirarlos sin costo |

---

## 11. Pendientes a resolver ANTES de configurar (bloqueantes)

Estos dos no los resuelve este plan: están sin documentar en el material del curso.

**(a) Cuál juego de fechas ACA es el vinculante — ✅ RESUELTO 2026-08-09.** Coexistían tres juegos, y el propio Manual se contradecía internamente (L98 decía *"09-15/11 coevaluación; 16-22/11 autoevaluación"*, la tabla calculada decía *"10/11–16/11 … 17/11–22/11"*):

| Componente | Manual (antes, encabezados ACA) | Manual (antes, tabla calculada) | Calendario oficial AFI — **adoptado** |
|---|---|---|---|
| Quiz cierre / nota | 31/08 · 07/09 | 31/08 · 07/09 | **30/08 · 07/09** |
| ACA 1 cierre / nota | 28/09 · 05/10 | 28/09 · 05/10 | **04/10 · 12/10** |
| ACA FINAL cierre / nota | 09/11 · 16/11 | 09/11 · 16/11 | **08/11 · 16/11** |
| Coevaluación cierre / nota | — · 22/11 | 16/11 · 22/11 | **15/11 · 22/11** (ventana 09/11–15/11) |
| Autoevaluación cierre / nota | — · 22/11 | 22/11 · 22/11 | **22/11 · 22/11** (ventana 16/11–22/11) |

**Decisión (docente, 2026-08-09):** se adoptó el juego de la **Cronograma OFICIAL AFI** (Coordinación de Gestión del Conocimiento) — no el de los enunciados ACA que este plan recomendaba originalmente. El Manual del Docente y el Calendario oficial ya se corrigieron para usar estas fechas, y este documento (§8.2, §8.3, §8.5, §9) se actualizó para que coincida. ~~**Pendiente real:** los 5 enunciados en `Clases/Recursos/ACAs/*.docx` siguen con las fechas viejas (31/08, 28/09, 09/11).~~ → **Cerrado el 2026-08-10, reverificado extrayendo los `.docx` el 2026-08-11:** los cinco se regeneraron con los nombres del aula y las ventanas oficiales — `Quiz (25%) - guia del cuestionario.docx` 03/08→**30/08** · `ACA 1 (25%) - Formulacion del problema y fundamentacion referencial.docx` 07/09→**04/10** · `ACA FINAL (42%) - Anteproyecto integrado.docx` 12/10→**08/11** · coevaluación 09/11→**15/11** · autoevaluación 16/11→**22/11**. **No hay nada que comunicarle al curso por este motivo.** Lo único no ambiguo en todas las fuentes, antes y después: **cierre y registro de todas las notas = domingo 22/11/2026**.

**(b) Por qué el inicio es 03/08 en `Informacion.txt` pero la Sesión 01 es el 10/08** en el CSV, el `.ics` y el Apps Script. El Manual además fija como hito de Coordinación: *"Lunes 10/08/2026: la clase de Proyecto I debe realizarse y grabarse"*. **Recomendación:** usar **10/08** como `start_date` del Corte I (es la primera sesión real y el hito verificable). *(Recomendación, no resolución.)*

**(c) Composición de los equipos.** Ningún archivo del curso los lista. Debe fijarse en Moodle primero y **replicarse idéntico** en ExamLab, o las notas grupales no serán comparables entre las dos plataformas.

---

## 12. Decisión recomendada y siguientes pasos

### Decisión

1. **Aprobar ExamLab como complemento**, con alcance explícito: notas consolidadas, retroalimentación, tutor IA, evidencia de sesiones y difusión programada.
2. **Las 5 entregas oficiales, la coevaluación y la autoevaluación se quedan en CDigital.** Sin excepción, sin piloto.
3. **CDigital es la fuente de verdad de las notas.** ExamLab es espejo de seguimiento y archivo permanente.
4. Modelar los 5 componentes como **talleres `is_external`** con pesos 25/25/42/4/4 en tres cortes de 25/25/50 y `attendance_weight = 0`.
5. Los **talleres formativos con IA son opcionales** y limitados a tres piezas cortas (título, pregunta, objetivo general). Se retiran sin costo si la adopción es baja.
6. **No** pilotear entrega de documentos en ExamLab en 26ES4. Se registra en §6 para otro periodo.
7. **No** presentar la detección de similitud de ExamLab como equivalente a Turnitin.

### Siguientes pasos (checklist)

- [ ] Docente aprueba este plan (veredicto + alcance de complemento).
- [x] **§11(a) resuelto 2026-08-09:** se adoptó el juego de fechas de la Cronograma OFICIAL AFI (ver tabla en §11a). Pendiente real: comunicar a los estudiantes si se quiere alinear las fechas de los 5 enunciados ACA (siguen con las fechas viejas).
- [x] **§11(b) resuelto:** 10/08 es el inicio real del Corte I (ya usado en todo este plan y en el Manual/Calendario).
- [ ] Configurar en Moodle lo obligatorio de semana 1 (grupos visibles, forzar modo grupo, `Equipo@` de 3, "Elección de grupo") — **esto va primero**.
- [ ] Crear el curso en ExamLab · verificar que `grade_scale_max=5` y `passing_grade=3` quedaron por defecto.
- [ ] Crear los 3 cortes con los pesos y rangos de §8.2 · confirmar `attendance_weight = 0`.
- [ ] Crear los 5 talleres `is_external` con sus pesos y `group_mode` de §8.3.
- [ ] Importar los 40 estudiantes · replicar **los mismos equipos** de Moodle (§11c) · verificar ninguno sin grupo.
- [ ] Importar el CSV de las 11 sesiones con `meeting_url` y `cut_name`.
- [ ] Subir contenidos (11 PPTX + plantilla APA + 5 enunciados) y asignarlos por sesión.
- [ ] Verificar que el **Tutor IA responde sobre la plantilla APA** (prueba: *"¿cómo cito material legal en APA 7?"*). Si responde solo con el título, el material no se indexó.
- [ ] Programar las 5 difusiones de §8.5 **antes del 24/08**.
- [ ] Escribir el override del prompt `workshop_question` con el criterio ESP329 (solo si se usan los talleres formativos).
- [ ] Sesión 01: slide explícita *"la entrega oficial es CDigital"* + explicar que un ítem sin nota se ve como 0 (R2).
- [ ] Por corte: registrar notas + observación en ExamLab → exportar XLSX → digitar en CDigital.
- [ ] Antes del 22/11: generar el consolidado DOCX y **descargar toda la evidencia de CDigital** (*"una vez cerrada el aula, NO se puede volver a entrar"*).
- [ ] Post-cierre: evaluar si vale desarrollar el tipo de pregunta "documento" para el próximo periodo (§6).

---

## 13. Fuentes

### Material del curso

| Recurso | Ruta |
|---|---|
| Manual del Docente | `Especializacion/Proyecto I/Manual del Docente - PROYECTO I.md` |
| Calendario oficial | `Especializacion/Proyecto I/Calendario de clases (oficial).md` |
| Enunciados ACA (5) | `Proyecto I/Clases/Recursos/ACAs/ACA {1,2,3}…docx`, `ACA {Auto,Co}evaluacion.docx` |
| Plantilla institucional | `Proyecto I/Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` |
| Info del grupo · roster | `2026/54ES4/Informacion.txt` · `Listado estudiantes.ods` · `Correos estudiantes (invitados Calendar).txt` |
| Calendario y hitos | `Encuentros Proyecto I - Importar a Calendar.csv` · `Entregas y hitos docentes - Importar a Calendar.csv` · `Crear encuentros con invitados.gs` |
| Material del estudiante | `Proyecto I/Clases/LEEME - Material para estudiantes.docx` · `Presentacion del Curso - Proyecto I.pptx` · 11 × `Sesion NN/Presentacion.pptx` |
| Rúbricas (**no leído**) | `Instructivo_Docentes_Proyecto_I_II_Especializaciones_Rubricas_Unificado.pdf` (Anexo 2) |

### Código de ExamLab (verificación de capacidades y brechas)

| Afirmación | Evidencia |
|---|---|
| No hay tipo de pregunta "documento" | CHECK en `supabase/migrations/20261600000000_bd_sql_support.sql:64` |
| La entrega solo acepta ZIP / código | `src/modules/projects/ProjectFiles.tsx:3253,3323-3358` · `src/modules/workshops/WorkshopQuestions.tsx:3069,3156` |
| El grader rechaza no-código | `supabase/functions/ai-grade-submission/index.ts:1498-1556,1626-1639` |
| Tabla de adjuntos de entrega, muerta | `project_submission_attachments` — 0 referencias en `src/` |
| Notas externas con observación | `supabase/migrations/20260505200000_external_activities.sql` · `src/modules/grading/ExternalGradesEditor.tsx:39,104-292` |
| Nota en escala del curso, no `max_score` | Comentario en `20260505200000…sql:47-54` |
| Pesos como % de la nota final · `score=null` cuenta 0 | `20260507100001_weights_as_percent_of_final.sql` · `src/modules/grading/grade.ts:70-76` |
| Escala 5 / aprobatoria 3 por defecto | `supabase/migrations/20260419123846…sql:4,7` |
| Asistencia → corte por `session_date` | Regla documentada en `CLAUDE.md` (modelo de pesos/cortes) |
| Grupos: modos y entrega compartida | `20260507150000_workshop_groups.sql:54-58` · `20260516010000_group_required_mode.sql:4-13` |
| `group_size_max` sin validación · `self_signup` no expuesto | `20260516010000…sql:11-13` |
| Hilo de feedback por pregunta | `20260503210000_feedback_threads.sql:6-16,110-122` |
| Adjuntos sin filtro de MIME · 25 MB · 8 archivos | `20260517100000_feedback_attachments.sql:87-97` · `src/modules/grading/FeedbackThread.tsx:839-846` · `feedback-attachments.ts:16,21` |
| Tutor IA extrae texto de `.docx`/`.pptx` | `supabase/functions/tutor-chat/index.ts` · `src/modules/contents/material-extract.ts:43-45` |
| Contenidos: extensiones aceptadas | `src/modules/contents/UploadExternalContentDialog.tsx:97-121` |
| Visor inline solo PDF e imágenes | `src/modules/contents/media-files.ts` · `MediaViewerDialog.tsx` |
| Sesiones: 8 columnas del CSV | `src/modules/sessions/csv.ts:31-44` |
| Similitud: aplica a texto · caps | `supabase/functions/detect-plagiarism/index.ts:15-20,42-45,297,332-349` |
| Rúbrica es texto libre | `20260428000000_projects.sql:25` · `20260419060000…sql:82` |
| Prompts por curso (override) | `20260508100000_ai_prompts.sql` · `20261300000000…sql:33-40` |
| Historial de intentos solo en exámenes | `20260501025625:2-3` · comentario en `20260607010000:53-54` |
| Coevaluación / autoevaluación inexistentes | Búsqueda `coevaluac\|autoevaluac\|peer_review\|grader_id\|evaluator` → único hit funcional: `20260609000000_seed_diagnostico_seguimiento_template.sql:9,32,141` (reporte del docente) |
| Encuestas no producen nota | `20260720000000_polls.sql:12-15,26-29,44` · `20260984000000_poll_questions_mixed.sql:26-53` |
| Slot de tutorías: evento ignora la franja | `20260943000000_poll_calendar_events.sql:19-26` |
| Acta recalcula con datos vivos | `src/modules/reports/ActasManager.tsx:12-17` |
| Export DOCX con membrete | `src/modules/reports/html-to-docx.ts` · `docx-import.ts` |
| Sin política de entrega tardía | Búsqueda `allow_late\|late_submission` → 0 hits |
| Sin integración LTI / Moodle | Sin referencias en `src/` ni `supabase/` |

---

*Documento interno Plan de curso · alcance: 26ES4 / 54ES4 · no distribuir a estudiantes. Las entregas oficiales de PROYECTO I se realizan exclusivamente en CDigital.*
