# Herramientas de ExamLab — Creatividad y Pensamiento Innovador (CUN · Pregrado · 26V04)

| Campo | Valor |
|---|---|
| Asignatura | Creatividad y Pensamiento Innovador — Escuela de Ingenierías |
| Código | **EI004** (SIAC) · área oferente C-EMP |
| Grupo | **54408** · **50 inscritos / cupo 50** |
| Periodo | **26V04 · Primer bloque** · 10/08/2026 → 27/09/2026 |
| Modalidad | **Virtual** · Google Meet · 7 encuentros sincrónicos, miércoles 5:00–6:00 pm (arranque real 5:10) |
| Créditos | 2 · 32 h docente + **64 h autónomas** |
| Docente | Julian Andrés Castaño · `julian_castanoe@cun.edu.co` |
| Evaluación | Art. 52 — Corte 1 30% · Corte 2 30% · Corte 3 40%. Autoevaluación/coevaluación **no aplican** |
| Fecha del documento | 2026-08-08 |
| Estado | **Borrador para decisión docente** |

---

> ### Alcance de este documento
>
> Esto es un análisis de **HERRAMIENTAS**, no de entregas.
>
> **La entrega oficial y la nota siguen viviendo en CDigital.** Nada de lo que sigue la sustituye, la duplica ni la mueve. Los porcentajes 30/30/40 del Art. 52, la nomenclatura `CRE_ACAN_Apellido` y las tres ventanas de ACA (19/08, 02/09, 16/09) quedan exactamente donde están.
>
> Lo que se analiza es lo otro: **con qué trabajan el estudiante y el docente durante la sesión y entre sesiones.** El lienzo donde se idea, el foro donde se pregunta el jueves, el asistente que responde a las 11 pm, el material que el estudiante realmente recibe, la señal de quién no arrancó. Cuando una herramienta de ExamLab necesita "existir" en la nota, el puente es registrar la actividad como **externa** con el enlace a CDigital — el archivo se sube allá, acá solo queda la nota y la observación para que el semáforo de riesgo y el consolidado del corte tengan de qué agarrarse.
>
> Marcas usadas: **[INFERIDO]** = deducción mía, no está en el material ni verificado en el código. Todo lo demás está verificado contra el repositorio de ExamLab o contra el material del curso.

---

## 1. Resumen ejecutivo

### Veredicto: **viable y con alto valor — pero el valor NO está donde uno esperaría.**

El cuello de botella real de este curso no es evaluar. Es que **hay 50 estudiantes, 50 minutos efectivos de clase, y 20 minutos de taller cuyo producto es el insumo obligatorio de la sesión siguiente** — y el docente hoy solo puede leer 3 de esas 50 fichas ("3 personas leen", "4 voluntarios pitchean"). Todo lo demás se pierde en silencio hasta que llega el ACA.

ExamLab resuelve **bien** tres cosas de ese cuello de botella y las resuelve hoy, sin desarrollo:

1. **Que el estudiante reciba la consigna real.** Los PPTX de las sesiones 02–07 son plantilla genérica; el contenido está en `Guiones/`, que el estudiante no recibe. El módulo de Contenidos + Tablero cierra ese hueco, con un detalle que cambia el esfuerzo: **genera el paquete completo por clase con IA** (presentación, guía docente, taller práctico, ejercicio con solución, examen con clave y rúbrica), y lo emite ya separado en material de docente vs. material de estudiante.
2. **Que el docente lea las 50 fichas, no 3.** El constructor de formularios (`encuesta mixta`) convierte la ficha de 6 campos en 6 campos reales, y el docente los lee **agrupados por campo con el nombre del autor** — las 50 respuestas al campo "usuario concreto", una debajo de otra.
3. **Que el estudiante tenga a quién preguntarle entre miércoles y miércoles.** El Tutor IA lee el texto real del material —PDF, DOCX, PPTX incluyendo las notas del orador, XLSX— y su prompt está sembrado explícitamente para **no resolverle el ejercicio**. El criterio de calidad que hoy vive en la tabla de acompañamiento del guion (*"¿Quién la usaría mañana a las 8 am y qué le duele hoy?"*) alcanza a los 50 y no solo a quien preguntó dentro de los 18 minutos.

Y falla **honestamente** en dos: no tiene ninguna plantilla de ideación de este dominio (SCAMPER, Canvas, FODA, mapa de utilidad, espina, árbol de problemas — el catálogo de 44 figuras de la pizarra es 100% ingeniería de software y redes), y **no guarda versiones**: la propuesta de innovación de la sesión 7 pisa la de la sesión 1, así que el "hilo conductor único" del curso no tiene dónde verse como hilo.

La contra-noticia buena: la brecha de plantillas es **menos grave de lo que parece**, porque el tipo de pregunta `diagrama` le da a cada estudiante su propio lienzo persistido y calificable, y el motor de diagramas incluye **mapa mental, matriz 2×2 y mapa de experiencia**. No hay botón de plantilla para ellos —el docente pega el código base una vez— pero existen.

### Tabla necesidad → herramienta → estado

Las 13 necesidades genéricas del análisis del curso (§4 del material):

| # | Necesidad del curso | Herramienta de ExamLab | Estado |
|---:|---|---|---|
| 1 | Lienzo de ideación compartido, sin login | Pregunta tipo **`diagrama`** en taller (un lienzo por estudiante, persistido y calificable) + **pizarra de sesión compartida** para modelar en vivo | **Con workaround** — sin plantillas del dominio |
| 2 | Contenedor único del artefacto acumulativo, con historial | **Proyecto con N slots** (una sección por sesión, con rúbrica y nota por slot) | **Con workaround** — no hay versiones |
| 3 | Plantillas por campos, llenables y revisables de un vistazo | **Encuesta mixta** (`poll_type='mixed'`) + `PollQuestionsEditor` | **Lista** — pero no lleva nota |
| 4 | Ver quién no arrancó, por sesión | **Alerta temprana** + **progreso de material** + **diagnóstico del curso** | **Lista** — hay que abrirla, no avisa sola |
| 5 | Banco autocorregible de vocabulario conceptual | **Reto en vivo** + taller `cerrada`/`cerrada_multi` + **Banco de preguntas** | **Lista** |
| 6 | Discusión asíncrona | **Foros** (por sesión, con ventana, hilo fijado y respuesta oficial) | **Lista** |
| 7 | Votación en vivo con resultado visible | **Encuestas** `single`/`multiple` + Reto en vivo | **Lista** |
| 8 | Material organizado por sesión, acceso directo | **Contenidos + Tablero** (allowlist de archivos por sesión) | **Lista** |
| 9 | Cronómetro proyectable con consigna y criterio | — | **No existe** |
| 10 | Asistente acotado al material del curso | **Tutor IA** por curso | **Lista** |
| 11 | Pitch grabado + coevaluación de pares | Proyecto con **video de sustentación** + factor | **Parcial** — coevaluación no existe |
| 12 | Señal de si el estudiante abrió el material | **Progreso de material** (`abriste N de M archivos`) | **Lista** |
| 13 | Calendario unificado que llegue al estudiante | **Sync Google / Microsoft 365** con invitados + **.ics suscribible** | **Lista** |

Y las necesidades que el syllabus exige pero el material no planifica:

| Exigencia del syllabus | Herramienta | Estado |
|---|---|---|
| Prueba estándar tipo SABER PRO por corte | Taller `cerrada`/`cerrada_multi` (sin proctoring) desde el Banco de preguntas | **Lista** |
| Rúbrica por actividad | `expected_rubric` como **tabla markdown en el enunciado** (se renderiza formateada) | **Con workaround** — la rúbrica no es dato, es texto |
| Mapa de utilidad / bloqueadores–ensanchadores (U2, sin sesión asignada) | `diagrama` mermaid **`quadrantChart`** (matriz 2×2 nativa) | **Con workaround** |
| Material en segundo idioma | Contenidos con IA acepta `language` en el generador | **Lista** |
| Clase autónoma por festivo | **Sesión tipo `autonoma`** — notifica y emaila sola a la hora de inicio; el estudiante marca revisado | **Lista** |

---

## 2. Mapa sesión por sesión

Esta es la sección que importa. Formato: qué pasa en la sesión según el guion → con qué herramienta concreta → qué queda en manos del docente.

**Presupuesto real por sesión: 50 minutos** (5:10 a 6:00). Regla que atraviesa todo el mapa y que recomiendo respetar: **máximo una herramienta nueva por sesión.** Con 50 estudiantes de pregrado conectados por Meet, cada herramienta que se estrena cuesta entre 4 y 8 minutos de "no me carga" — y esos minutos salen del taller, que es lo único que produce el insumo de la sesión siguiente. **[INFERIDO]** — es criterio mío, no está medido.

---

### Semana 0 — antes del 12/08 (montaje)

Nada de esto es sincrónico, pero condiciona las 7 sesiones.

| Qué | Herramienta | Detalle |
|---|---|---|
| Crear las 50 cuentas | **Importación por CSV** | Columnas: `full_name, institutional_email, personal_email, password, roles, student_code, course_name, …`. Con `course_name` quedan matriculados en el mismo paso y sale el correo de bienvenida automático. Clave temporal fija `Temporal#123` + cambio forzado al primer inicio. **No hay lista de estudiantes en el material del curso** — hay que pedirla al portal |
| Cargar el cronograma de 7 encuentros | **Generador de sesiones** o **importación CSV de 8 columnas** | El CSV lleva `session_date, title, start_time, end_time, meeting_url, cut_name, recording_url, session_type`. El generador conoce los festivos de Colombia (Ley Emiliani + Pascua calculada) y ofrece política `incluir / saltar / mover` |
| Regla "festivo → clase autónoma, no cancelación" | **`session_type = autonoma`** | Se marca **en la misma columna del CSV**. Un proceso automático detecta la hora de inicio de la sesión autónoma y **notifica + envía correo** a los matriculados; el estudiante "asiste" marcando el material como revisado. **[INFERIDO]** — no verifiqué si algún miércoles del 12/08 al 23/09 cae festivo; el Manual declara la regla, así que dejo la pieza lista |
| Subir el material | **Contenidos** | Se puede seleccionar **la carpeta `Clases/` completa**. Tope 25 MB por archivo, 100 MB por lote |
| Configurar 30/30/40 | **Cortes del curso** | Tres cortes con sus fechas y pesos; dentro de cada uno, cuánto pesan talleres, exámenes, proyectos y asistencia. La tabla del Syllabus venía truncada (`CORTE 1 = 30% / EV 01 / 9,0%`). **Decidido 2026-08-10:** cada ACA evalúa el **100% de su corte** (ACA 1 = Corte 1 30% · ACA 2 = Corte 2 30% · ACA 3 = Corte 3 40%); no se subdivide en varios EV. |
| Escala 0,1–5,0 y nota de aprobación | **Configuración de la institución** | La escala y la nota mínima se configuran a nivel institución. **La nota de aprobación no está en el material del curso** — confirmar con CDigital |
| Sincronizar el calendario | **Google / Microsoft 365** | El docente conecta su cuenta una vez; el sistema crea los eventos **con los 50 como invitados** y genera el enlace de Meet. Esto cierra el defecto textual del material (*"los CSV/ICS de Pregrado no incluyen invitados/estudiantes"*): hoy el estudiante nunca recibe la invitación |
| Sembrar el Tutor IA | **Prompts de IA → override del curso** | Pegar en el prompt del curso las 4 respuestas típicas de la tabla de acompañamiento del guion S01 y el criterio *"si alguien externo entiende el dolor sin pedir aclaración, sirve"* |
| Cargar el Banco de preguntas | **Banco de preguntas** | Los errores conceptuales que los guiones ya enumeran literalmente: *"innovación = tecnología nueva"*, *"es de todos los tipos" sin priorizar*, *"MVP = fase 2 del software grande"*, *"mi innovación es radical" como adorno*, Canvas con frases genéricas. Etiquetados por sesión |

**El movimiento de mayor retorno de toda la semana 0** es generar el paquete por clase con IA para las sesiones 02–07. El generador produce cinco piezas por clase (presentación, guía docente, taller práctico, ejercicio con solución, examen con clave y rúbrica), acepta instrucciones libres del docente, duración e idioma, y **emite los archivos con la convención de nombres que el filtro de "solo docente" ya reconoce** — o sea, el material nace separado sin renombrar nada. Costo: revisar 6 paquetes generados, que no es poco, pero es órdenes de magnitud menos que redactar 6 PPTX. Consume cuota de IA.

---

### Sesión 01 — 12/08 · Introducción · Propuesta de Innovación · creatividad e inteligencia emocional

**Lo que pide el guion:** post-it en Padlet con expectativa + tema (~7 min); **18 min** llenando la ficha problema–oportunidad de 6 campos; 3 estudiantes leen usuario+problema en 30 s. Entregable `S01_FichaProblema_Apellido`.

| Momento | Herramienta | Cómo |
|---|---|---|
| Rompehielos (7 min) | **Encuesta mixta** | 2 campos: "tu expectativa del curso" y "el tema o problema que te interesa". El nombre ya lo trae el sistema. Reemplaza el Padlet — que hoy es **el mismo enlace compartido entre los 5 cursos del docente**, así que las respuestas se mezclan |
| Ficha de 6 campos (18 min) | **Encuesta mixta**, 6 campos `obligatorios` con tope de caracteres | Título · usuario concreto · problema (3–5 líneas) · evidencia observable · tipo Oslo tentativo · valor esperado. El docente después la lee **campo por campo con el nombre del autor**: las 50 respuestas a "usuario concreto" juntas, que es exactamente lo que hoy no puede hacer |
| Las 3 lecturas en voz alta | **Se mantienen** | La encuesta no las reemplaza; las hace innecesarias como muestreo, no como momento de clase |
| Cierre | **Tablero del curso** | El estudiante ve el material de la sesión; el guion docente queda cargado pero **destildado del allowlist** de esa sesión, así que no lo ve |
| Anuncio | **Tutor IA + Foro de la sesión 01** | Se anuncian los dos el día 1. El foro con ventana 12/08 → 18/08 |

**Lo que no cubre:** la inteligencia emocional, los bloqueadores/ensanchadores y el mapa de utilidad son la Unidad 2 del syllabus, el ACA 1 los exige, y **ninguna de las 5 fases del guion S01 les asigna tiempo**. Ver sesión 02 para dónde meterlos.

**Advertencia de arranque:** esta es la sesión donde 50 personas entran por primera vez, cambian la clave temporal y descubren la plataforma. Si además se estrena el Reto en vivo, no queda taller. **Recomiendo cero Reto en la sesión 01.**

---

### Sesión 02 — 19/08 · Design Thinking y técnicas · *(vence ACA 1)*

**Lo que pide el guion:** **22 min** — redactar 1 *How Might We*, listar **mínimo 8 ideas**, elegir 1–2 justificando con 3 criterios, boceto de 1 min. 3 comparten el HMW.

| Momento | Herramienta | Cómo |
|---|---|---|
| Las 8 ideas | **Taller con pregunta tipo `diagrama`** → mermaid `mindmap` | **Este es el hallazgo más útil del análisis para esta sesión.** El tipo `diagrama` se renderiza dentro de la pantalla del estudiante: cada uno tiene **su propio lienzo**, la respuesta se guarda, y lleva rúbrica y puntaje como cualquier otra pregunta. Un mapa mental con 8 ramas es exactamente el instrumento. En modo grupo, un lienzo por grupo |
| El *How Might We* + los 3 criterios | Misma pregunta o pregunta `abierta` aparte | Con la rúbrica escrita como **tabla markdown en el enunciado** — el enunciado se renderiza formateado mientras el estudiante responde, así que la tabla de criterios se ve como tabla |
| El mapa de utilidad (U2, huérfano) | **`diagrama`** → mermaid `quadrantChart` | Matriz 2×2 nativa. Cierra el instrumento de la Unidad 2 que el material tiene como archivo suelto (`s02_mapa_utilidad_modelo.html`) sin sesión que lo acoja. El ACA 1 lo exige |
| El boceto de 1 min | **Mensajería 1-a-1 o el hilo del foro** | **Brecha:** no se puede subir una imagen como respuesta de taller. Los compañeros del mismo curso **sí** pueden mensajearse entre ellos con adjuntos, y el docente también. Es un rodeo |
| SCAMPER | **Sin plantilla** | El catálogo de 44 figuras de la pizarra no la tiene. Se dicta como lista de verbos y el estudiante la aplica en el mapa mental. Ver §6 |
| ACA 1 vence hoy | **Actividad externa** | Registrar en ExamLab un taller `externo` con el enlace a CDigital, para que la nota entre al corte y al semáforo |

---

### Sesión 03 — 26/08 · Gestión de la innovación (Manual de Oslo)

**Lo que pide el guion:** clasificar 3 mini-casos **respondiendo en el chat de Meet**; **20 min** llenando la ficha Oslo (tipo dominante + secundario, novedad, valor, **2 actividades de gestión con responsable y fecha**, riesgo #1). 3 lecturas rápidas.

| Momento | Herramienta | Cómo |
|---|---|---|
| Los 3 mini-casos | **Encuesta `single`** ×3, resultado visible al instante | Reemplaza el "pidan en el chat" de manera exacta: con 50 personas el chat de Meet no da lectura agregada; la encuesta muestra la distribución en 20 segundos y el docente enseña sobre el error mayoritario, no sobre el que alcanzó a leer |
| Ficha Oslo (20 min) | **Encuesta mixta** de 7 campos | Los dos campos de "actividad de gestión con responsable y fecha" son campos obligatorios, así que el sistema no deja cerrar sin ellos — hoy es lo primero que la gente deja en blanco |
| Cierre + repaso | **Reto en vivo**, 6 preguntas de 20 s | Sobre los errores del banco: *"innovación = tecnología nueva"*, *"es de todos los tipos"*. Si el tiempo no da, va como taller autocorregible para la semana |
| Retroalimentación del ACA 1 | **Hilo de retroalimentación** sobre la actividad externa | Anclado a la actividad, no en un correo suelto |

---

### Sesión 04 — 02/09 · Tipos de innovación · *(vence ACA 2)*

**Lo que pide el guion:** **21 min** — matriz comparativa tipo elegido vs. alternativo, **mínimo 5 criterios** + conclusión en 4 líneas.

| Momento | Herramienta | Cómo |
|---|---|---|
| La matriz de 5 criterios | **Encuesta mixta con 5 campos** (uno por criterio) + 1 campo de conclusión | **Aquí ExamLab no tiene lo que el curso pide.** No existe un tipo de pregunta tabular: no hay grilla filas × columnas. El formulario de 5 campos es lo más cerca, y tiene la ventaja de que el docente lee "criterio 3" de los 50 juntos. Lo que se pierde es que el estudiante vea su matriz como matriz |
| Alternativa visual | **`diagrama`** → mermaid `quadrantChart` | Incremental ↔ radical en un eje, y el criterio que el docente elija en el otro. Es la lectura que el guion busca (*"contexto socio-económico"*) mejor que una tabla |
| Repaso | **Reto en vivo** | *"mi innovación es radical" como adorno* es el error del banco que corresponde a esta sesión |
| ACA 2 vence hoy | **Actividad externa** + hilo de retroalimentación | Igual que el ACA 1 |

---

### Sesión 05 — 09/09 · Análisis de negocios · validación de la propuesta

**Lo que pide el guion:** **22 min** — FODA en 6 bullets; Canvas mínimo (propuesta de valor, segmento, canales, actividades); MVP en 5 líneas; **1 prueba de validación con criterio numérico u observable**.

| Momento | Herramienta | Cómo |
|---|---|---|
| FODA | **`diagrama`** → `quadrantChart` | Los 4 cuadrantes son nativos del motor de diagramas. **No hay plantilla FODA** en el catálogo de figuras: el docente pega el código base una vez y el estudiante lo llena |
| Canvas mínimo (4 bloques) | **Encuesta mixta con 4 campos** o taller `abierta` ×4 | **No hay plantilla de Business Model Canvas.** Con 4 bloques el formulario es honesto; con los 9 completos sería un formulario de 9 campos, que ya es incómodo. Como el guion pide el Canvas **mínimo**, los 4 campos alcanzan |
| MVP en 5 líneas | Campo `abierto` con tope de caracteres | El tope obliga a las 5 líneas |
| La prueba de validación | Campo obligatorio, con la rúbrica del criterio numérico en el enunciado | Es el campo que hoy más se llena con generalidades |
| Repaso | **Reto en vivo** | *"MVP = fase 2 del software grande"*, Canvas con frases genéricas |

**Trabajo autónomo S05→S06:** el guion pide **ejecutar la prueba de validación con usuarios reales**. Ahí el **Foro** de la semana y el **Tutor IA** son las dos piezas que sostienen a un estudiante de pregrado que nunca entrevistó a nadie.

---

### Sesión 06 — 16/09 · Vigilancia tecnológica · *(vence ACA 3)*

**Lo que pide el guion:** **22 min** — tablero de vigilancia con **mínimo 3 fichas de señal** (título, fuente + fecha + enlace, hallazgo en 2 líneas, implicación, nivel de confianza); ≥1 señal debe forzar un ajuste. 2 comparten la implicación.

| Momento | Herramienta | Cómo |
|---|---|---|
| Las 3 fichas de 5 campos | **Taller con 3 preguntas `abierta`**, cada una con la plantilla de 5 campos escrita como tabla markdown en el enunciado | 15 campos en un formulario es demasiado. Con 3 preguntas abiertas y la plantilla en el enunciado, la IA califica las 3 contra la rúbrica y el estudiante ve la estructura formateada |
| El ajuste forzado por una señal | Cuarta pregunta `abierta` | Es el criterio de aprobación del taller |
| Las fuentes con fecha y enlace | — | **Brecha real, ver §6.** No hay gestor de referencias ni ayuda de citación. El estudiante pega la URL a mano y nadie valida el formato |
| El ciclo observar→analizar→comunicar→usar | **`diagrama`** → flowchart | Modelado en vivo por el docente en la pizarra de sesión |
| ACA 3 vence hoy | **Actividad externa** | Es el 40% del curso: si no queda registrado acá, el semáforo de riesgo queda ciego para el corte más pesado |

---

### Sesión 07 — 23/09 · Innovación local–internacional · entidades de apoyo · cierre

**Lo que pide el guion:** **23 min** — mapa de **mínimo 3 entidades reales** con el pedido concreto; escribir guion de pitch de 60 s; **ensayo en parejas**; **4 voluntarios pitchean cronometrados**.

| Momento | Herramienta | Cómo |
|---|---|---|
| Mapa de 3 entidades | **`diagrama`** → mermaid `mindmap` o flowchart | Universidad / sector productivo / Estado / redes como ramas, con el pedido concreto en cada hoja |
| Ensayo en parejas | **Mensajería 1-a-1 entre compañeros** | Dos matriculados del mismo curso pueden escribirse, **con adjuntos**. Sirve para intercambiar el guion antes de ensayarlo |
| Los 4 voluntarios | **Se mantienen en vivo** | |
| **Los otros 46 pitches** | **Proyecto con video de sustentación** | Este es el cierre honesto del curso: el estudiante graba su pitch de 60 s, pega el enlace (o sube el archivo), y el docente registra el **factor de sustentación** y las notas cuando puede. La nota final del proyecto es `nota de entrega × factor`. Con importación masiva de sustentaciones por CSV, para no abrir 50 diálogos |
| Coevaluación entre pares | **Foro, un hilo por estudiante** | **Brecha, ver §6.** Funciona como conversación; no hay pauta, ni asignación de quién revisa a quién, ni nota |
| Cierre y consolidado | **Informes** | Plantilla con las notas por corte, exportable a `.docx` e imprimible a PDF |
| Restricción del guion | *"no prometa cupos ni financiaciones"* | Se mantiene tal cual; ninguna herramienta la toca |

---

### Transversal a las 7 sesiones

| Qué | Herramienta | Cadencia |
|---|---|---|
| **Prueba tipo SABER PRO por corte** (exigida por el syllabus, inexistente en el material) | **Taller `cerrada` / `cerrada_multi`** desde el Banco de preguntas, **sin proctoring**, con varios intentos | Tres, uno al cierre de cada corte |
| **Quién no arrancó** | **Alerta temprana** (Estadísticas) + progreso de material | Revisar el lunes antes de cada sesión |
| **Dudas de la semana** | **Foro** con ventana por sesión, hilo de la consigna **fijado arriba** y el criterio del docente marcado como **respuesta oficial** | 7 foros, uno por sesión |
| **Recordatorio de ACA** | **Mensaje programado** con difusión al curso | Escrito una vez en la semana 0, programado para el domingo anterior a 19/08, 02/09 y 16/09 |
| **Acompañamiento entre clases** | **Tutor IA** | Permanente |

**Ninguna sesión queda sin herramienta.** Las tres que quedan a medias — la matriz de 5 criterios de la S04, el Canvas de la S05 y las fuentes citadas de la S06 — están señaladas arriba y desarrolladas en §5 y §6.

---

## 3. Herramientas que sirven YA, sin desarrollo

### 3.1 Contenidos + Tablero — el material que el estudiante sí recibe

Sube archivos (`.pdf .pptx .docx .xlsx .md .txt .csv` + imágenes + `.zip`), **carpeta completa de una vez**, 25 MB por archivo y 100 MB por lote. El tablero asigna contenido a una sesión concreta, y dentro de la sesión el docente **destilda archivo por archivo** qué ve el estudiante (allowlist explícito). Visor sin descargar: PDF en línea, imágenes con zoom y anotaciones, `.md` con editor, `.pptx` con anotaciones por diapositiva.

Además hay un filtro automático por nombre de archivo: cualquier archivo cuyo nombre contenga `GUIA_DOCENTE`, `SOLUCION`, `EXAMEN` o `TEACHER_GUIDE` **nunca se le muestra al estudiante**.

**Y genera con IA el paquete por clase.** Cinco piezas configurables (presentación · guía docente · taller práctico · ejercicio con solución · examen con clave y rúbrica), con etiquetas `teórico`/`práctico`/`examen`, número de clases, duración, idioma e instrucciones libres del docente. Los prompts de generación **se pueden sobrescribir por curso**. El material generado sale ya con la convención de nombres que activa el filtro de solo-docente.

**Aplicación directa:** el defecto #1 del material de este curso (*"los PPTX de las sesiones 02–07 son plantilla genérica; cero contenido temático; todo el contenido real vive en el guion, que el estudiante no recibe"*).

**Dos reglas operativas:**
- Guion **asignado a una sesión** → destildarlo del allowlist. No hace falta renombrarlo.
- Guion como **material general del curso** → sí hay que renombrarlo a `GUIA_DOCENTE_*`, porque el material general no pasa por el allowlist, solo por el filtro de nombre.

**Límites:** "nueva versión" es reemplazo, no historial — no hay versionado en ningún flujo de contenidos. Y borrar un contenido no borra los archivos del almacenamiento.

### 3.2 Tutor IA del curso

Un chat por (estudiante, curso), permanente. **Lee el texto real del material, no los títulos:** extrae de `.md`/`.txt`, notebooks, y de los binarios de Office descomprimiéndolos y leyendo su XML interno — de los `.pptx` saca **también las notas del orador**, que es donde suele estar la explicación docente real. Y **lee PDF** con extracción de texto. El estudiante puede **referenciar un archivo con `#`** y ese archivo se prioriza en el contexto.

El prompt sembrado dice, textualmente: *"Tu rol es acompañar al estudiante en el aprendizaje del material del docente, **NO resolverle los ejercicios**"*, con reglas explícitas de "no regalas soluciones", rechazo a "escribir su trabajo final por él" y honestidad académica. Tiene conciencia de la fecha (zona horaria de Bogotá), así que responde bien a "¿cuántos días me quedan para el ACA?".

**Es síncrono por diseño** — responde en vivo, a las 11 pm de un domingo, independientemente de cómo esté configurado el modo de procesamiento del resto de la IA.

**Aplicación:** la necesidad #10 del curso. El criterio de la tabla de acompañamiento del guion S01 se pega en el prompt del curso y alcanza a los 50.

**Límites:** consume cuota por mensaje. Un PDF **escaneado** (imagen sin capa de texto) devuelve vacío. Hay tope de contexto (unos 6.000 caracteres por documento, 22.000 en total): con mucho material, lo último se trunca.

### 3.3 Encuesta mixta — el constructor de formularios

Preguntas `abierta` (texto libre con tope de caracteres) y `cerrada` (opción única), cada una marcable como **obligatoria**. El estudiante las llena con guardado automático por campo, ve el contador de caracteres y el asterisco de obligatorio, y no puede cerrar sin completar las obligatorias.

**Lo que la hace la pieza clave de este curso:** el docente lee los resultados **agrupados por campo, con el nombre del autor** — las respuestas cerradas como barras de conteo con los votantes, y las abiertas como lista de textos con autor. Eso es literalmente "leer 50 fichas de un vistazo, campo por campo", que es la necesidad #3.

**Aplicación:** ficha problema–oportunidad (6 campos), ficha Oslo (7), Canvas mínimo (4), rompehielos (2), matriz de criterios (5).

**Límite grande, hay que decirlo:** **no lleva nota.** No entra al consolidado del corte, ni al semáforo de riesgo, ni tiene rúbrica ni calificación con IA. Es un instrumento de trabajo de clase, no de evaluación. Cuando la ficha deba pesar, va como **taller** con preguntas `abierta` (ver §5.1).

### 3.4 Foros

N foros por curso, cada uno con **ventana de apertura y cierre** y **asociable a una sesión**. Los estudiantes abren hilos y responden; hay votos a favor. El docente puede **fijar un hilo arriba**, **bloquearlo** y **marcar una respuesta como oficial** (que sube al primer lugar y marca el hilo como resuelto). El estado "abierto" está sincronizado entre la pantalla y la base, así que nunca ofrece un botón que la base vaya a rechazar.

Y las tablas markdown escritas por un estudiante **sí se renderizan como tabla** en el foro.

**Aplicación:** la necesidad #6, que en este curso **no existe en absoluto** (cero artefactos de discusión asíncrona en los 63 archivos). Un foro por sesión, abierto desde el miércoles de la clase hasta el martes siguiente. En pregrado virtual esto vale doble: el que no habla en Meet frente a 50 sí escribe.

**Y un uso que el material no anticipa:** fijar el hilo con la consigna del taller arriba del foro, y marcar el criterio de calidad del docente como **respuesta oficial**. El criterio queda anclado, visible y sin IA de por medio.

**Límites:** el foro **no se califica** (sin rúbrica, sin nota, sin conteo de participación hacia el consolidado) y **no admite adjuntos**. Un estudiante no puede crear el foro contenedor, solo hilos.

### 3.5 Encuestas en vivo y Reto en vivo

**Encuestas `single`/`multiple`:** voto de un clic, resultados visibles siempre / al cerrar / nunca, permitir cambiar respuesta, cierre automático cuando todos respondan, asociables a una sesión, con enlace compartible que lleva directo a la encuesta.

**Reto en vivo:** quiz con PIN, 4 formas y colores, tiempo y puntos por pregunta, selección múltiple, ranking **acumulado por curso a través de todos los juegos**, y puntaje que premia la rapidez. **Se puede entrar sin iniciar sesión**, escaneando el QR: pide el correo institucional y valida que esté matriculado.

**Aplicación:** la necesidad #7 (sustituye el "pidan en el chat" de la S03 y el muestreo de voluntarios) y la #5 (el vocabulario conceptual, con el banco de errores que los guiones ya enumeran).

**Límites que hay que conocer antes de la clase:**
- **No entran jugadores después de que arranca.** Con 50 personas conectándose por Meet, hay que dar margen de lobby generoso.
- Debe ser el **correo institucional** exacto del perfil. Si el estudiante escribe el personal, lo rechaza.
- El cronómetro se ancla al reloj del dispositivo: **un teléfono con la hora adelantada ve las preguntas ya vencidas.** Es la causa a sospechar cuando "a un estudiante no le cargan las preguntas".
- Generar el Reto **desde el material del curso** está implementado en el servidor pero **no tiene pantalla**: hoy el docente escribe los temas a mano.

### 3.6 Alerta temprana, progreso de material y diagnóstico del curso

**Alerta temprana:** cada estudiante acumula motivos discretos y verificables — inasistencia, actividades reprobadas, no entregadas, promedio bajo — y el nivel sale de cuántos se cruzaron: 0 sin riesgo, 1 en observación, **2 o más en riesgo**. Hacen falta **dos señales independientes** para el rojo, justamente para que un taller difícil no pinte medio curso. Tres reglas de justicia en la asistencia: llegar tarde cuenta como que asistió; una ausencia justificada sale del denominador; y solo cuentan las sesiones donde el estudiante tiene registro. Solo lista a quienes requieren atención.

**Progreso de material:** registra qué archivos abrió o descargó cada estudiante y muestra **"abriste N de M archivos"** y **"seguías en: …"**.

**Diagnóstico del curso:** matriz estudiante × actividad con cinco estados de celda (sin entregar · entregado sin calificar · calificado · error de IA · sin sustentación).

**Aplicación:** la necesidad #4 y la #12. Entre el 12/08 y el 19/08 hay una sola clase; la primera señal real de abandono hoy es el ACA 1, y con 50 inscritos de pregrado eso llega tarde.

**Dos límites que cambian el hábito:**
1. **No avisa solo.** El docente tiene que **abrir Estadísticas**. No hay notificación automática ni historial del nivel. Es un hábito semanal, no una alerta que llega.
2. El universo de actividades se deriva de las entregas existentes: una actividad que **nadie** entregó no cuenta como "no entregada". Aceptable, porque en ese caso el faltante no distingue a nadie.

### 3.7 Calendario con invitación al estudiante

El docente conecta su cuenta de Google **o Microsoft 365** y sincroniza las sesiones: el sistema crea los eventos **con los matriculados como invitados**, envía las actualizaciones y **genera el enlace de Meet**, guardándolo en la sesión. Del lado del estudiante hay además una URL `.ics` suscribible con token privado, que incluye talleres, proyectos y sesiones.

**Aplicación:** el defecto textual del material — *"los CSV/ICS de Pregrado no incluyen invitados/estudiantes"*. Hoy el estudiante **nunca recibe la invitación**, y "no sabía que era hoy" es causa real de no-entrega en pregrado.

**Límite:** requiere autorización del docente con su cuenta institucional. **Si la CUN restringe aplicaciones de terceros en Workspace o 365, esto no conecta** — es lo primero a probar, porque si falla hay que replanear la comunicación de fechas.

### 3.8 Sesiones, asistencia y clases autónomas

Matriz sesiones × estudiantes. Cada sesión lleva fecha, título, hora, duración, enlace de reunión, enlace de grabación, corte, contenido asignado y su subconjunto de archivos. Autoservicio de asistencia con **QR rotativo** proyectable (código de 6 dígitos que cambia cada minuto por defecto, con período de gracia), contador de presentes en vivo, y también un camino para marcar sin haber iniciado sesión.

**Modalidad `autonoma`:** un proceso automático detecta la hora de inicio y **notifica y envía correo** a los matriculados; el estudiante marca el material como revisado y queda como presente.

**Aplicación:** la regla *"Festivo en día de clase → clase autónoma, no cancelación"* del Manual, que hoy no tiene actividad preparada.

**Límite que sí importa acá:** la pantalla de asistencia **solo ofrece "presente" y "ausente"**. Los estados *tarde* y *justificado* existen en el motor y **cambian el cálculo** (tarde cuenta como asistió; justificado sale del denominador de Alerta temprana), pero **el docente no tiene dónde ponerlos**. Con 7 encuentros, faltar a uno es el 14% del curso sincrónico: la ausencia justificada sin registrar empuja a alguien al semáforo rojo sin motivo.

### 3.9 Banco de preguntas, talleres y proyectos

**Banco de preguntas:** preguntas reutilizables por curso con tema, dificultad (1–5), etiquetas y puntaje sugerido. Se importan a un taller, a un proyecto o **a un Reto en vivo**; los tipos que no aplican al destino se filtran solos. **12 tipos**; para este curso sirven `abierta`, `cerrada`, `cerrada_multi` y `diagrama`.

**Talleres:** N preguntas con rúbrica y puntaje, fecha límite, instrucciones, **enlace externo**, modo grupo, número de intentos, peso hacia el corte, y videos introductorios con bloqueo de avance. Corrección con IA por pregunta o completa, con retroalimentación, estimación de si la respuesta la escribió una IA, y detección de copia entre compañeros.

**Proyectos:** N "archivos esperados", cada uno con su tipo y rúbrica. **Sustentación como factor multiplicativo**: `nota final = nota de entrega × factor (0 a 1)`. Video de sustentación (enlace o archivo subido) e importación masiva de sustentaciones por CSV. Grupos con arrastrar y soltar; la entrega es compartida y al calificar se notifica a cada integrante.

**Aplicación:** los talleres como práctica formativa autocorregible y como ensayo con rúbrica antes de la entrega oficial; el proyecto como el **contenedor del artefacto acumulativo** y como el **pitch grabado asíncrono** de la S07.

### 3.10 Notas externas y consolidado

`ExternalGradesEditor` lista a los 50 matriculados con columnas **Nota + Observación** por estudiante, para actividades que ocurrieron fuera de la plataforma. Los cortes se configuran con peso propio y cuatro bolsas internas (talleres, exámenes, proyectos, asistencia), y la asistencia de un corte se deriva por fechas de sesión.

**Aplicación:** **este es el puente correcto para los tres ACA.** El archivo se sube a CDigital; en ExamLab queda el enlace, la nota y la observación por estudiante. Con eso, y solo con eso, funcionan Alerta temprana, el consolidado y los informes.

**Límite:** una actividad sin nota **cuenta como 0** con su peso original, no se reescala. Es deliberado (refleja "lo que debe y no entregó es nota perdida hasta que aparezca"), pero sorprende a quien espera un promedio parcial.

---

## 4. Lo que necesita workaround — con el workaround exacto y su costo

### 4.1 La ficha estructurada que además lleve nota

**Problema:** la encuesta mixta lee 50 fichas campo por campo, pero no califica. El taller califica con rúbrica e IA, pero sus respuestas se ven como texto plano y el docente vuelve a leer 50 textos sueltos.

**Workaround:** decidir por sesión cuál de las dos importa.
- **Sesiones 01, 03, 05** (fichas de trabajo, insumo de la siguiente): **encuesta mixta**. Lo que se necesita es leerlas rápido, no ponerles nota.
- **Sesiones 02, 04, 06** (lo que va a los ACA): **taller** con una pregunta `abierta` por campo y la rúbrica escrita como **tabla markdown en el enunciado** — el enunciado se renderiza formateado mientras el estudiante responde, así que ve la tabla de criterios antes de escribir.

**Costo:** el docente arma dos veces el mismo instrumento (una como formulario, otra como taller). Con las 7 fichas del curso, son ~7 duplicaciones. Y sigue sin haber una grilla: 5 criterios son 5 preguntas, no 5 columnas.

### 4.2 Las plantillas de ideación que el material pide por nombre

**Problema:** el catálogo de figuras de la pizarra tiene **44 items en 6 categorías**, todas de ingeniería de software y redes (UML, diagrama de flujo, entidad–relación, estructuras de datos, arquitectura de nube, topología). **No hay post-it, ni mapa mental, ni FODA, ni Business Model Canvas, ni SCAMPER, ni espina de pescado, ni árbol de problemas, ni mapa de utilidad.**

**Workaround, en dos niveles:**

**Nivel 1 — el que funciona bien.** Usar la pregunta tipo `diagrama` con el motor de diagramas, que **sí incluye mapa mental, matriz 2×2, mapa de experiencia, línea de tiempo y tablero kanban**. Cubre: las 8 ideas (mapa mental), el mapa de utilidad y el FODA (matriz 2×2), el ciclo de vigilancia (flujo) y el mapa de entidades (mapa mental). El docente pega el código base una vez en el enunciado y el estudiante lo edita.
*Costo:* preparar 5 fragmentos de código base, una vez. No hay botón de plantilla — los 7 botones que existen son de ingeniería. **[INFERIDO]** — verifiqué que el motor incluye esos tipos de diagrama y que no hay lista blanca que los bloquee, pero **no ejecuté un render** para confirmarlo visualmente. **Probar uno antes de la sesión 02.**

**Nivel 2 — para lo que no tiene equivalente (Canvas de 9 bloques, SCAMPER).** Formulario de campos (§3.3) o, si se quiere el lienzo visual, el docente dibuja la plantilla en una pizarra y la duplica.
*Costo y límite duro:* **el estudiante no puede editar pizarras propias hoy.** No es una restricción de la base de datos —la base sí lo permitiría— sino que la pantalla del estudiante es de solo lectura y la ruta de creación es solo del docente. El único lienzo que los estudiantes editan es la **pizarra de la sesión**, y es **una sola escena para toda la clase**: sirve para modelar en vivo con participación, no para que 50 personas ideen en paralelo.

### 4.3 El artefacto acumulativo (la Propuesta de Innovación)

**Problema:** el hilo conductor del curso es un documento que crece 7 semanas. ExamLab guarda **una entrega por actividad, sobrescrita** — la versión de la sesión 7 pisa la de la sesión 1. No hay historial.

**Workaround:** modelar la propuesta como **un proyecto con 7 slots**, uno por sesión. Cada slot tiene su propia rúbrica, su propia nota y su propio hilo de retroalimentación. Eso da el "semáforo por sección" que el curso pide, y la vista de diagnóstico muestra la matriz estudiante × slot con cinco estados.

**Costo:** no es historial de versiones — es historial de **secciones**. Si el estudiante reescribe la sección 1 en la semana 6 (que es exactamente lo que el guion S01→S02 pide: *"mejorar el problema con una observación real"*), la versión anterior desaparece. **No se puede verificar si incorporó la retroalimentación**, solo ver el resultado final.

### 4.4 Coevaluación y ensayo entre pares

**Problema:** no existe evaluación entre pares. Un estudiante no puede ver la entrega de otro.

**Workaround en dos piezas:**
- **Ensayo en parejas (S07):** dos matriculados del mismo curso **sí pueden mensajearse entre ellos, con adjuntos**. Se intercambian el guion del pitch por mensajería.
- **Comentarios de pares:** un hilo de foro por estudiante donde los compañeros comentan.

**Costo:** sin pauta, sin asignación automática de quién revisa a quién, sin registro de que la revisión ocurrió, sin nota. Y el foro no admite adjuntos, así que el trabajo hay que pegarlo como texto. **Atenuante:** este curso declara que autoevaluación y coevaluación **no aplican** con peso propio, así que la ausencia bloquea la actividad formativa, no la nota.

### 4.5 La rúbrica que el syllabus exige

**Problema:** el syllabus dice *"las actividades contarán con su respectiva rúbrica"* y el curso tiene **cero rúbricas** (los ACA traen listas de verificación de 5 ítems sin ponderación). En ExamLab la rúbrica es **una cadena de texto**, no un dato: no hay criterios como filas, ni niveles, ni puntaje por celda, ni suma automática, ni reutilización entre actividades.

**Workaround:** escribir la rúbrica como **tabla markdown** (criterios × niveles) y ponerla en **dos lugares**:
1. En el **enunciado** de la pregunta → el estudiante la ve formateada **antes** de responder.
2. En el campo de **rúbrica esperada** → alimenta la calificación con IA, y el estudiante la ve formateada en la revisión **después** de calificar.

**Costo:** la rúbrica se escribe dos veces por actividad y no se puede consultar en conjunto ni reutilizar entre actividades. Pero los cinco instrumentos del curso ya están definidos campo por campo en los guiones — **eso ya es la rúbrica, solo hay que pegarla**.

### 4.6 Registrar los ACA sin duplicar la entrega

**Workaround (es la práctica correcta, no un parche):** por cada ACA, crear en ExamLab un taller marcado como **externo** con el enlace a CDigital, y cargar las notas con el editor de notas externas (nota + observación por estudiante).

**Costo:** cargar 50 notas × 3 ACA. Con `is_external` la pantalla esconde todo lo que no aplica, así que es una tabla de 50 filas con dos columnas. **Sin esto, Alerta temprana y el consolidado quedan ciegos** — y el ACA 3 es el 40% del curso.

### 4.7 Asistencia justificada

**Problema:** la pantalla solo ofrece presente/ausente. El motor sí entiende *justificado* (lo saca del denominador de riesgo).

**Workaround:** marcar **presente** y anotar la justificación en la observación de la actividad del corte, o llevarla fuera de la plataforma.
**Costo:** con 7 encuentros, marcar ausente a alguien con excusa válida lo empuja al semáforo rojo. Marcar presente falsea el registro de asistencia. **No hay salida limpia.** Recomiendo marcar presente y dejar constancia por otra vía. **[INFERIDO]** — es criterio mío.

---

## 5. Brechas reales

Sin maquillar. Estas cinco no se tapan con otra pieza.

| # | Brecha | Impacto en este curso | Qué se pierde exactamente |
|---:|---|---|---|
| 1 | **No hay tipo de pregunta tabular (grilla filas × columnas)** | **Alto** | La matriz comparativa de ≥5 criterios (S04) y el tablero de vigilancia con 3 fichas × 5 campos (S06) son el instrumento central de dos sesiones. Se pueden pedir como formulario de campos o como texto con plantilla en el enunciado, pero el estudiante nunca ve su matriz como matriz, y no hay validación de "esta celda quedó vacía" |
| 2 | **La rúbrica no es dato** | **Alto** | El syllabus la exige por actividad. Se escribe como tabla markdown en dos lugares (§4.5) y funciona visualmente, pero no hay criterios, ni niveles, ni puntaje por celda, ni suma, ni reutilización, ni consulta agregada |
| 3 | **No hay plantillas de ideación de este dominio** | **Medio-alto** | El material pide SCAMPER, Business Model Canvas, FODA y mapa de utilidad **por nombre**. El motor de diagramas cubre mapa mental y matriz 2×2 (que resuelve mapa de utilidad y FODA); Canvas y SCAMPER quedan sin plantilla visual. Y **el estudiante no puede crear pizarras propias** — es limitación de pantalla, no de base |
| 4 | **No hay versiones de un trabajo largo** | **Medio-alto** | La Propuesta de Innovación es un documento que crece 7 semanas y es *"el hilo conductor único"* del curso. La plataforma guarda su última versión. El ciclo del guion (*"mejorar el problema con una observación real"*) no se puede verificar |
| 5 | **No hay gestor de referencias ni ayuda de citación** | **Medio** | La ficha de señal de la S06 pide **fuente + fecha + enlace** y el ACA 3 pide fuentes trazables. El estudiante pega URLs a mano; nadie valida formato, nadie detecta duplicados, no hay biblioteca personal. Y el syllabus exige plantilla APA CUN |
| 6 | **No hay coevaluación / revisión por pares** | **Medio** | S07 pide ensayo en parejas y el pitch es criterio del ACA 3. Sucedáneo: mensajería entre compañeros + hilo de foro, sin pauta ni nota (§4.4) |
| 7 | **No hay cronómetro de actividad proyectable** | **Bajo-medio** | Cada guion es un reloj (18/22/21/22/22/23 min) y cada taller tiene un criterio explícito que hoy solo se dice en voz alta. Se resuelve con cualquier temporizador compartido en pantalla |
| 8 | **No hay canal de clase donde los 50 se vean entre sí** | **Bajo-medio** | La difusión llega a 50 conversaciones privadas. La discusión colectiva vive en el Foro, que sí funciona para eso |
| 9 | **Sin adjuntos en el foro; sin subir imagen como respuesta de taller** | **Bajo-medio** | El "boceto de 1 minuto" de la S02 no tiene dónde ir dentro del taller. Rodeo: mensajería (sí admite adjuntos) |
| 10 | **La biblioteca de videos no reproduce ni recuerda la posición** | **Bajo** | Abre en pestaña nueva. El bloqueo de avance existe solo atado a un taller o proyecto |
| 11 | **Alerta temprana no notifica** | **Bajo, pero es hábito** | Hay que abrir Estadísticas cada semana. Si el docente no adquiere el hábito, la herramienta no existe |

**Lo que NO es brecha, aunque se pareciera:** que la entrega oficial esté en CDigital. Eso es el diseño, no una carencia. El puente de actividad externa (§4.6) lo resuelve sin duplicar nada.

---

## 6. Riesgos — con el agravante de pregrado

Este curso no es un posgrado. 50 estudiantes de nivel tecnológico, virtual, con **una hora semanal** y menos autonomía. Eso cambia el peso de casi todos los riesgos.

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **La sesión 01 se consume en soporte técnico** (50 personas creando cuenta, cambiando clave temporal, encontrando el curso) | **Alto** | Crear las cuentas y matricular **la semana 0**; el correo de bienvenida sale solo. En la S01 no estrenar nada más que el formulario. Dejar el Reto en vivo para la S03 |
| **Dos plataformas → "¿dónde entrego?"** | **Alto** | Regla explícita en la S01 y repetida en cada ACA: **CDigital recibe la entrega; ExamLab es donde se trabaja.** Toda actividad de ACA en ExamLab va como **externa con el enlace a CDigital** — el botón lleva allá |
| **La mayoría entra por celular** | **Alto** | Verificar en móvil: formulario de 6 campos, foro y Reto en vivo. El QR de asistencia requiere compartir pantalla en Meet; el código de 6 dígitos dictado en voz alta es el camino real |
| **50 minutos no alcanzan** | **Alto** | Máximo **una herramienta nueva por sesión**. Si algo se desborda, lo primero que se sacrifica es el repaso, nunca el taller |
| **El Reto en vivo se cae en clase** (no entran después del lobby · correo institucional exacto · reloj del dispositivo adelantado) | **Medio-alto** | Lobby largo y anunciado. Recordar "correo `@cun.edu.co`". Si a alguien no le cargan las preguntas, es el reloj del teléfono. Plan B inmediato: la misma pregunta como encuesta `single` |
| **El estudiante usa el Tutor IA para que le escriba la ficha** | **Medio-alto** | El prompt sembrado lo rechaza explícitamente y es socrático por diseño, pero **no es infalible**. Reforzar con el detector de texto generado por IA en los talleres, entendiéndolo como **señal para conversar, no como prueba** |
| **La IA está en modo diferido y no responde en clase** | **Medio-alto** | El modo de procesamiento es un interruptor de la institución, no del docente. **Verificarlo antes de la S01.** En modo diferido, la generación de contenidos y la calificación se encolan; el Tutor IA sí responde igual |
| **La autorización del calendario institucional falla** | **Medio** | Probarlo en la semana 0. Si la CUN bloquea aplicaciones de terceros, el plan B es la URL `.ics` suscribible del estudiante + mensajes programados con las fechas |
| **El docente no adquiere el hábito de abrir Alerta temprana** | **Medio** | Es la herramienta que más valor tiene y la que más fácil se olvida, porque no avisa. Anclarla a un momento fijo: lunes, antes de preparar el miércoles |
| **Las tres URL bloqueantes del curso siguen pendientes** (CDigital, Meet, plantilla APA) | **Medio** | No es un riesgo de ExamLab, pero lo hereda: sin la URL de CDigital, las actividades externas no tienen adónde apuntar |
| **Contenido generado con IA con errores conceptuales** | **Medio** | Revisar los 6 paquetes antes de publicarlos. El curso enseña a distinguir innovación de tecnología: un material generado que confunda eso es peor que un PPTX genérico |
| **Cuota de IA agotada** | **Medio** | El Tutor IA consume por mensaje y 50 estudiantes en semana de ACA generan picos. Hay lista de claves de respaldo con rotación automática — verificar que esté configurada |
| ~~El desglose EV del syllabus está truncado~~ — **resuelto 2026-08-10** | — | **Decidido 2026-08-10:** cada ACA evalúa el **100% de su corte** (ACA 1 = Corte 1 30% · ACA 2 = Corte 2 30% · ACA 3 = Corte 3 40%); no se subdivide en varios EV. Cambiarlo a mitad de bloque recalcularía todas las notas: no tocar |
| **Ausencia justificada sin dónde registrarse** | **Bajo-medio** | Con 7 encuentros, un ausente justificado se va al rojo. Marcar presente y dejar constancia por otra vía (§4.7) |
| **Sobrecarga: 13 herramientas para 7 sesiones** | **Alto, y es el riesgo real** | Ver §7. La recomendación es empezar con **cinco**, no con trece |

---

## 7. Decisión recomendada y checklist

### Decisión

**Adoptar ExamLab como el espacio de TRABAJO del curso, con cinco herramientas en el primer bloque, no trece.**

El curso dura 7 semanas. Estrenar todo el catálogo garantiza que ninguna pieza se use bien. El conjunto mínimo que resuelve el cuello de botella real es:

1. **Contenidos + Tablero** — que el estudiante reciba la consigna real, no el PPTX genérico.
2. **Encuesta mixta** — que las 7 fichas se llenen estructuradas y el docente lea las 50, no 3.
3. **Foro por sesión** — el espacio asíncrono que hoy no existe en ningún archivo del curso.
4. **Tutor IA** — el acompañamiento de las 64 horas autónomas.
5. **Actividades externas + Alerta temprana** — los tres ACA registrados, para que el semáforo vea algo.

**Segundo anillo, si el primero funciona** (a partir de la S03): Reto en vivo, pregunta tipo `diagrama` para la ideación, y el proyecto con video de sustentación para el pitch de la S07.

**No adoptar en este bloque:** certificados (los emite la institución), exámenes con supervisión remota (fricción sin retorno formativo en un virtual de pregrado por celular), pizarras standalone (el estudiante no las puede crear) y todo el módulo de código.

**Lo que ExamLab no va a hacer y hay que asumir:** la grilla de la matriz comparativa, la rúbrica como dato, la plantilla de Canvas y el historial de versiones de la propuesta. Esas cuatro se trabajan con los rodeos de §4, sabiendo que son rodeos.

### Checklist priorizado

**Bloqueantes — antes del 12/08**

- [ ] Conseguir el listado de los 50 estudiantes (no está en el material del curso) y armar el CSV de importación.
- [ ] Confirmar las tres URL pendientes: **CDigital**, **Google Meet** y plantilla APA pública.
- [ ] Verificar que el **modo de procesamiento de IA** esté en inmediato (si está en diferido, la generación de contenidos se encola).
- [ ] Configurar los cortes con **una ACA por corte** (30/30/40), sin subdividir en EV — decidido 2026-08-10.
- [ ] Confirmar la **nota de aprobación** y la escala institucional.
- [ ] Importar el cronograma de 7 encuentros con la columna de modalidad de sesión.
- [ ] Probar la autorización del calendario institucional. Si falla, plan B con `.ics` + mensajes programados.

**Alto valor — semana 0**

- [ ] Subir la carpeta `Clases/` completa a Contenidos.
- [ ] Asignar el material a cada sesión y **destildar los guiones del allowlist** (o renombrarlos a `GUIA_DOCENTE_*` si van como material general).
- [ ] Generar con IA el paquete por clase para las sesiones **02 a 07** y **revisarlo pieza por pieza**.
- [ ] Sembrar el override del prompt del Tutor IA con la tabla de acompañamiento del guion S01.
- [ ] Crear los **7 foros**, uno por sesión, con su ventana.
- [ ] Armar las **7 fichas como formularios** (empezar por la de la S01, 6 campos obligatorios).
- [ ] Programar los tres recordatorios de ACA (domingos anteriores al 19/08, 02/09 y 16/09).

**Segundo anillo — después de la sesión 02**

- [ ] Cargar el Banco de preguntas con los errores conceptuales que los guiones ya enumeran.
- [ ] **Probar un render de mapa mental y de matriz 2×2** en una pregunta tipo `diagrama` antes de usarla en clase (§4.2, nivel 1 — está inferido, no verificado visualmente).
- [ ] Preparar los 5 fragmentos de código base de diagrama (mapa mental, matriz 2×2, flujo del ciclo de vigilancia, mapa de entidades).
- [ ] Armar el Reto en vivo de la S03 con 6 preguntas.
- [ ] Escribir las rúbricas como tabla markdown para los tres instrumentos que van a los ACA.
- [ ] Crear el proyecto de pitch de la S07 con video de sustentación.

**Hábito semanal — todo el bloque**

- [ ] **Lunes:** abrir Alerta temprana y el progreso de material antes de preparar el miércoles.
- [ ] **Miércoles después de clase:** abrir el foro de la sesión y fijar el hilo de la consigna.
- [ ] **Tras cada ACA:** cargar las 50 notas + observación en la actividad externa.

**Cierre**

- [ ] Generar el informe consolidado del bloque.
- [ ] Anotar qué herramienta se usó, cuál no, y por qué — para el bloque siguiente.

---

## 8. Fuentes

### Material del curso

| Recurso | Ubicación |
|---|---|
| Identificación, grupo, periodo, modalidad | `2026/54408/Informacion.txt` |
| Syllabus SIAC (8 unidades, sistema de evaluación truncado) | `CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS EI004_VIR.docx` |
| Manual del docente (regla de festivos, hilo conductor) | `Manual del Docente - Creatividad y Pensamiento Innovador.md` |
| Calendario de los 7 encuentros | `Calendario de clases (oficial).md` |
| Guiones de las 7 sesiones (fases al minuto, talleres, criterios) | `Guiones/Sesion 0N - ….md` |
| Enunciados de los 3 ACA | `Clases/Recursos/ACAs/` |
| Presentación del curso (cortes 30/30/40, acuerdos) | `Presentacion del Curso….pptx` |
| Instrumento huérfano de la Unidad 2 | `Guiones/Capturas/Sesion 02/s02_mapa_utilidad_modelo.html` |
| Índice de material para estudiantes | `LEEME - Material para estudiantes.docx` |
| Fechas e hitos | `Entregas y hitos docentes - Importar a Calendar.csv` |

### Plataforma

Inventario de módulos verificado contra el repositorio de ExamLab (catálogo de módulos, rutas, migraciones y funciones de servidor), con una verificación adversarial posterior que corrigió nueve afirmaciones del inventario inicial. Las correcciones que cambian conclusiones de este documento:

| Corrección aplicada | Efecto en este documento |
|---|---|
| El Tutor IA **sí** lee PDF (además de XLSX y las notas del orador de PPTX) | §3.2 — la pieza más fuerte del análisis no queda inutilizada por material en PDF |
| El CSV de sesiones tiene **8 columnas** e incluye la modalidad de sesión | §2 semana 0 — las clases autónomas se marcan en el mismo import, no una por una |
| Los foros **sí** tienen hilo fijado, bloqueo y respuesta oficial | §3.4 — el criterio del docente queda anclado sin depender de la IA |
| Contenidos **genera** el paquete por clase con IA, ya separado docente/estudiante | §3.1 — cambia el esfuerzo de cerrar el hueco de los PPTX genéricos |
| El allowlist por archivo de la sesión existe (no hay que renombrar los guiones asignados) | §3.1 — dos reglas operativas distintas según dónde viva el guion |
| La pregunta tipo `diagrama` da **un lienzo por estudiante**, persistido y calificable | §4.2 — la brecha de "50 ideando en paralelo" no es tal |
| El motor de diagramas incluye mapa mental, matriz 2×2 y mapa de experiencia | §4.2 — mapa de utilidad y FODA tienen soporte nativo. **Sin verificación visual** |
| La **encuesta mixta** es un constructor de formularios y el docente lee por campo con autor | §3.3 — resuelve la necesidad #3, que el inventario daba por inexistente |
| Compañeros del mismo curso pueden mensajearse **con adjuntos** | §4.4 — el ensayo en parejas de la S07 tiene camino |
| La rúbrica escrita como tabla markdown **sí** se renderiza formateada al estudiante | §4.5 — el rodeo pasa de imposible a viable |
| El estudiante **podría** crear pizarras propias (la base lo permite; falta la pantalla) | §5 brecha 3 — es limitación de interfaz, no de arquitectura |

---

*Documento interno de plan de curso. No distribuir a estudiantes. La entrega oficial y la nota del curso viven en CDigital; nada de lo aquí descrito la sustituye.*
