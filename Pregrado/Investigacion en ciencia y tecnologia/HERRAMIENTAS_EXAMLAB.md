# Herramientas de ExamLab — Investigación, Ciencia y Tecnología (EI005 · Grupo 53339 · 26P03)

| Campo | Valor |
|---|---|
| Curso | Investigación, Ciencia y Tecnología — Escuela de Ingenierías |
| Código SIAC | **EI005** · Unidad FINVV (Formación Investigativa Virtual) |
| Grupo | **53339** (único del periodo) · cupo 50 / **20 inscritos** |
| Créditos | 2 · **32 h con docente + 64 h autónomas** |
| Nivel | **Profesional (pregrado)** · Teórico-Práctico |
| Periodo | **26P03** · segundo bloque · inicio 10/08/2026 · cierre 20/09/2026 |
| Modalidad | **Virtual** (Google Meet) — ⚠️ el syllabus marca `Presencial ☑`; ver §7-R14 |
| Encuentros | **6 sincrónicos**, jueves **5:00–6:00 pm** (13/08 · 20/08 · 27/08 · 03/09 · 10/09 · 17/09) |
| Docente | Julian Andres Castaño · `julian_castanoe@cun.edu.co` |
| Fecha del documento | 2026-08-08 |
| Estado | **Borrador para decisión docente** |

---

> ### Este documento es sobre HERRAMIENTAS, no sobre entregas
>
> **La entrega oficial y la publicación de notas siguen en CDigital, sin excepción.** Lo dicen los tres ACAs (*"Entrega oficial: solo por CDigital"*), el `LEEME` y la slide 8 del deck de encuadre. Nada de lo que aparece abajo la sustituye, la duplica ni la compite.
>
> Lo que sí se discute acá es **con qué trabaja el estudiante o el docente en la sesión y entre sesiones**: dónde vive el material, dónde se dibuja el árbol de problemas, dónde queda la duda del jueves a las 9 pm, con qué se practica el vocabulario del método científico, y cómo se ve —antes del ACA 1— quién todavía no arrancó.
>
> Los porcentajes 30/30/40 del Art. 52 se mencionan **solo** cuando definen dónde poner el peso del acompañamiento. No se propone mover ni un punto.

---

## 1. Resumen ejecutivo

### Veredicto: **viable con alcance recortado y arranque por fases.**

Tres hechos condicionan todo lo demás, y ninguno es de la plataforma:

1. **Quedan 5 días hasta la primera sesión** (hoy 08/08; S01 el jueves 13/08). No hay margen para montar todo.
2. **El curso es 6 h sincrónicas contra 64 h autónomas.** El 91% del tiempo del estudiante ocurre sin docente, y hoy ese tramo no tiene ninguna herramienta: ni foro, ni asistente, ni forma de ver quién se descolgó. Ahí es donde ExamLab aporta casi todo su valor.
3. **El ACA 1 (30%) vence el 20/08**, o sea la semana 2. Lo que no esté listo antes del 13/08 no alcanza a influir en el primer corte.

Con 20 inscritos —el grupo más pequeño de los cuatro cursos— casi todo lo que en un curso de 111 sería inviable acá es manejable. La restricción real es el calendario del docente, no la escala.

### Necesidad → herramienta → estado

Las 11 necesidades del análisis del corpus, más tres que aparecieron al cruzarlo con el inventario:

| # | Necesidad | Herramienta de ExamLab | Estado |
|---|---|---|---|
| 1 | Material organizado por sesión, con la consigna real (no la slide plantilla) | Contenidos + Tablero del curso (`content_file_paths` por sesión) | **Lista** |
| 2 | Asistente sobre el material del curso para las 64 h autónomas | Tutor IA por curso + override del prompt | **Lista** |
| 3 | Ejercicios autocorregibles (la "prueba parcial" que el syllabus exige y no existe) | Banco de preguntas → Taller `cerrada`/`cerrada_multi` + Reto en vivo | **Lista** |
| 4 | Discusión asíncrona anclada a la sesión | Foros (por sesión, con hilo fijado + respuesta oficial) | **Lista** |
| 5 | Ver quién se está quedando, semana a semana | Alerta temprana + progreso de material + diagnóstico del curso | **Lista** (hay que abrirlo, no llega solo) |
| 6 | Pulso rápido en vivo durante el encuentro | Encuesta `single`/`multiple` + Reto en vivo | **Lista** |
| 7 | Ideación / presentación colectiva de arranque (el Padlet de la S01) | Encuesta `mixed` (formulario multi-campo con autor) | **Lista** |
| 8 | Calendario que el estudiante vea como agenda | Sync Google/M365 con invitados + `.ics` suscribible del alumno | **Lista** |
| 9 | Registrar presencia en un encuentro remoto de 1 h | Check-in con código rotativo (o marcar a mano: son 20) | **Lista** (sin `tarde`/`justificado` en el UI) |
| 10 | Las 26 h de docencia que el bloque no entrega sincrónicamente | Sesiones tipo `autonoma` (notifican solas y registran revisión) | **Lista** |
| 11 | Lienzo de diagramación: espina de pescado y árbol de problemas (S04) | Pizarra de sesión (docente) + pregunta `diagrama` (estudiante) | **Con workaround** — ver §5.1 |
| 12 | Matriz estructurada (síntoma/evidencia/consecuencia; matriz de fuentes) | Encuesta `mixed` con un campo por columna, o tabla markdown en el foro | **Con workaround** — ver §5.2 |
| 13 | Rúbrica visible por criterios y niveles | Tabla markdown en el enunciado (`MarkdownInline` la renderiza) | **Con workaround** — ver §5.3 |
| 14 | Gestor de referencias / ayuda de citación APA (ACA 3: matriz de fuentes) | — | **No existe** — §6.1 |
| 15 | Historial de versiones del documento acumulativo (ACA 1→2→3) | — | **No existe** — §6.2 |
| 16 | Similitud entre entregas de prosa | Detector de plagio (cabe por escala, pero el prompt es de código) | **Con workaround caro** — §6.3 |

**Recomendación:** montar el **núcleo de 4 piezas** antes del 13/08 (curso + 20 cuentas + material por sesión + check-in), encender **Tutor IA y foros** en la semana 1, y dejar el banco de preguntas para la S03 —que es justo donde el syllabus pide la prueba parcial que no existe—. Todo lo demás, fuera de este bloque.

---

## 2. Lo que ya está resuelto en el curso y no hay que tocar

Para no proponer sobre lo que ya funciona:

- Los 6 guiones docentes están completos, con reloj al minuto y estructura idéntica: **Encuadre (6–12) → Exposición (12–16) → Modelación en pantalla (10–12) → Taller (16–22) → Cierre (8) = 60 min exactos.** Este documento no propone cambiar esa estructura; propone qué herramienta ocupa cada fase.
- Los 3 ACAs existen con consigna, entregable, checklist y fecha.
- Hay manual del docente, calendario oficial, calendario por grupo, CSV/ICS y correo de bienvenida.

Y los cuatro defectos del material que sí condicionan las decisiones de abajo:

| Defecto (del análisis del corpus) | Consecuencia para la herramienta |
|---|---|
| §6.1 — Las slides 4, 5 y 6 son **textualmente idénticas** en las 6 sesiones; la consigna real vive solo en `Guiones/`, que no se comparte | El estudiante que revisa la presentación después de clase **no recupera la consigna**. Es la necesidad #1 |
| §6.2 — La **prueba parcial no existe** como artefacto, aunque el syllabus la exige en U5 y U11–12 y la metodología la pide por corte con estándar ICFES-SABER PRO | La S03 tiene un hueco de contenido, no solo de herramienta. Es la necesidad #3 |
| §6.3 — No hay rúbricas: 5 casillas binarias por ACA, y la tabla EV del syllabus está **truncada en el origen** (llega hasta `CORTE 1 / EV 01 / 9.0%`) | Cualquier configuración de pesos en ExamLab exige decidir antes el desglose. Ver §8-checklist |
| §6.9 — No hay material para las clases autónomas ni para las ~26 h que el bloque corto no entrega | Es la necesidad #10, y tiene una herramienta específica y poco obvia (§4.6) |

---

## 3. Mapa sesión por sesión

La sección más importante. Una fila por fase del guion. **Ninguna sesión queda vacía**; donde no hay herramienta limpia, lo digo con esas palabras.

Convención: **[L]** lista sin trabajo previo · **[W]** con workaround (§5) · **[X]** no hay herramienta.

---

### Sesión 01 — 13/08 (jue) — U1–U2: Presentación del Syllabus · fundamentos del método científico

| Fase (min) | Actividad del guion | Herramienta | |
|---|---|---|---|
| Encuadre (12) | Rompehielos con post-its: nombre + expectativa + idea de tema | **Encuesta `mixed`** con 2 campos abiertos ("¿qué esperas del curso?", "¿sobre qué te gustaría investigar?"). El nombre lo pone el perfil. El docente ve las 20 respuestas **agrupadas por campo y con autor** | **[L]** |
| Exposición (16) | Ciencia vs. tecnología vs. investigación; etapas del método | **Contenidos**: la PPTX de la sesión, subida al tablero y asignada a la S01 | **[L]** |
| Modelación (12) | Modelar en pantalla las etapas del método | **Pizarra de sesión** (Excalidraw), proyectada por Meet. Queda guardada y el alumno la consulta después | **[L]** |
| Taller (16) | Ficha: tema tentativo + por qué importa + 1 fuente exploratoria → `S01_TemaTentativo_Apellido` | **Encuesta `mixed`** de 3 campos (uno por dato). Si se quiere que lleve nota, **Taller** con 3 preguntas `abierta` + rúbrica | **[L]** |
| Cierre (8) | 2–3 estudiantes comparten 30 s | Sin herramienta — es conversación en Meet | — |
| Asistencia | — | **Check-in** con código de 6 dígitos por el chat de Meet, o marcar a mano (son 20) | **[L]** |
| Entre clases | *"Completa el avance encargado hoy"* | **Foro de la S01**, con la consigna real como **hilo fijado** | **[L]** |

**Lo que hay que resolver acá y no es de plataforma:** el Padlet actual comparte el mismo enlace entre los 5 cursos del docente. La encuesta `mixed` queda por curso, con autor resuelto y sin enlace público.

---

### Sesión 02 — 20/08 (jue) — U4: MinCiencias · 6 líneas de Ingeniería · elección de línea

| Fase (min) | Actividad del guion | Herramienta | |
|---|---|---|---|
| Encuadre (10) | Verificar avance previo | **Progreso de material** ("abriste N de M archivos") + **Alerta temprana**, revisados el miércoles | **[L]** |
| Exposición (16) | SNCTI, 8 focos de la Misión de Sabios, convocatorias/becas/movilidad | Contenidos (PPTX + enlaces MinCiencias como material de la sesión) | **[L]** |
| Modelación (10) | Navegar el portal de MinCiencias | Compartir pantalla en Meet. *(Opcional post-bloque: grabarlo y subirlo a la biblioteca de videos)* | **[L]** |
| Exposición | Las 6 líneas: IoT, Big Data, IA, servicios de ingeniería, uso de aplicaciones, telemática | **Encuesta `single`** con las 6 líneas → el docente ve **en vivo** cómo se reparten los 20. Eso decide dónde pone el acompañamiento las siguientes 4 semanas | **[L]** |
| Taller (20) | Línea elegida + párrafo de justificación + 2 referentes con APA tentativa → `S02_LineaInvestigacion_Apellido` | **Encuesta `mixed`**: 1 pregunta `cerrada` (la línea) + 2 `abierta` (justificación, referentes) | **[L]** |
| Repaso | — | **Reto en vivo**: 6 preguntas de 20 s sobre el método científico (S01). Reemplaza el *"1 pregunta a 2 estudiantes"* que hoy deja sin señal a 18 de 20 | **[L]** |
| Hito | **Cierra ACA 1 (30%)** | Registrar como actividad `is_external` con el enlace a CDigital → entra al gradebook y a Alerta temprana **sin duplicar la entrega** | **[L]** |

---

### Sesión 03 — 27/08 (jue) — U5: Prueba parcial · 1.er avance del artículo

**Es la sesión con el hueco más grande del curso, y no es un hueco de herramienta: la prueba no existe.** El syllabus la exige dos veces (U5 y U11–12) y la metodología la pide por corte bajo estándar ICFES-SABER PRO; en los 44 archivos de la carpeta no hay ni un quiz, ni un banco, ni una prueba redactada.

| Fase (min) | Actividad del guion | Herramienta | |
|---|---|---|---|
| Encuadre (10) | Recoger el estado del avance | Alerta temprana + entregas de la S01/S02 | **[L]** |
| Exposición (14) | Tipos de conocimiento, fuentes de información, caracterización del problema | Contenidos | **[L]** |
| Modelación (12) | Estructura mínima del avance: título, intro de 3 párrafos (contexto → vacío → propósito), pregunta, 3 referencias | Pizarra de sesión | **[L]** |
| **Prueba parcial** | *No existe en el material* | **Banco de preguntas → Taller** con preguntas `cerrada`/`cerrada_multi`, **sin proctoring** y con varios intentos. Contenido: etapas del método, tipos de conocimiento, distinguir problema de solución, reconocer una fuente confiable, reconocer una cita APA correcta | **[L]** — el instrumento hay que escribirlo (§8) |
| Taller (22) | Borrador del 1.er avance en plantilla APA → `S03_Avance1_Apellido` | La redacción va en Google Docs / Word Online (plantilla APA, restricción del curso). ExamLab aporta: **rúbrica visible** en el enunciado (§5.3) + **Tutor IA** para las preguntas de las 64 h | **[W]** |
| Hito | **Fecha límite de nota del ACA 1** | **Hilo de retroalimentación** sobre el ítem externo del ACA 1: la observación queda anclada a lo que hay que corregir, y no en un correo | **[L]** |

> ⚠️ **Nudo de calendario que el material ya tiene y la herramienta no arregla:** el ACA 2 obliga a *"incorporar retroalimentación del Corte 1"*, pero la fecha límite de nota del ACA 1 es el **mismo 27/08** en que cierra el ACA 2. La retroalimentación tiene que salir antes de esa fecha o el requisito es imposible. Es una decisión del docente, no una función que falte.

---

### Sesión 04 — 03/09 (jue) — U6: Identificación de problemas y pregunta de investigación

**La sesión que más pide herramienta, y la que tiene la brecha más específica del curso.** El entregable pide literalmente *"diagrama (espina o árbol)"*, y el guion manda *"Abrir Excalidraw (sin cuenta) o dibujar la espina en Docs"*.

| Fase (min) | Actividad del guion | Herramienta | |
|---|---|---|---|
| Encuadre (10) | Verificar el avance | Alerta temprana | **[L]** |
| Exposición (14) | Espina de pescado, árbol de problemas, método de las 3D; preguntas cerradas/abiertas/compuestas; fuentes oficiales confiables | Contenidos | **[L]** |
| **Modelación (12)** | El docente dibuja la espina en vivo | **Pizarra de sesión** (Excalidraw embebido, sin cuenta ni instalación → cumple la restricción "solo gratis + nube"). **El catálogo de 44 figuras no trae espina ni árbol**: el docente dibuja la plantilla **una vez** con rectángulo + línea + texto, y la **duplica** para cada uso | **[W]** — §5.1 |
| **Taller (20)** | 8–12 líneas de problema + pregunta en una frase + **diagrama** → `S04_ProblemaPregunta_Apellido` | **Taller con pregunta tipo `diagrama`**: cada estudiante tiene su propio lienzo, persistido, con rúbrica y puntaje, calificable. Para el **árbol de problemas** el editor soporta jerarquías; la **espina de pescado** no tiene forma nativa | **[W]** — §5.1 |
| Cierre (8) | 2–3 comparten | — | — |
| Entre clases | — | Foro de la S04: los diagramas se comentan entre pares | **[L]** |

> **Honestidad sobre este punto:** una espina de pescado **por estudiante, dentro de ExamLab, sin fricción** no tiene camino limpio hoy. Los tres caminos posibles y su costo están en §5.1. El árbol de problemas sí lo tiene.

---

### Sesión 05 — 10/09 (jue) — U7: Formulación del planteamiento del problema

| Fase (min) | Actividad del guion | Herramienta | |
|---|---|---|---|
| Encuadre (10) | Recoger el diagrama de la S04 | Entregas del taller de la S04 (visibles con nota y feedback) | **[L]** |
| Exposición (14) | ¿Estado actual? ¿evidencias visibles? ¿causas/implicaciones? ¿qué hacer? ¿posibles soluciones? | Contenidos | **[L]** |
| **Modelación (12)** | **Tabla síntoma / evidencia / consecuencia** antes de pasar a prosa | Dos caminos: **(a)** encuesta `mixed` con 3 campos —el docente lee las 20 en columna—; **(b)** el estudiante pega la tabla en markdown en un **hilo del foro**, donde **sí se renderiza como tabla real** con bordes | **[W]** — §5.2 |
| Taller (22) | Planteamiento de 1–1.5 páginas → `S05_Planteamiento_Apellido` | Google Docs (plantilla APA) + **Tutor IA** con el criterio del guion cargado + rúbrica visible | **[W]** |
| Hito | **Cierra ACA 3 (40%)** | Actividad `is_external` con enlace a CDigital | **[L]** |

> ⚠️ **Ojo con el camino (b):** una respuesta de taller se muestra en texto plano monoespaciado —los pipes de la tabla salen crudos—. En el **foro** sí renderiza como tabla. Si la tabla se quiere ver formateada, va al foro; si se quiere que lleve nota, va al taller y se lee cruda.

---

### Sesión 06 — 17/09 (jue) — U8 + U10–12: Bases de datos CUN · gestores · marco teórico y revisión

Es la sesión más cargada (cuatro unidades comprimidas en una hora) y la única **sin nombre de archivo de entrega** en su guion.

| Fase (min) | Actividad del guion | Herramienta | |
|---|---|---|---|
| Encuadre (10) | Estado del planteamiento | Alerta temprana | **[L]** |
| Exposición (16) | EBSCO, SciELO, Redalyc, Latindex; gestores (Mendeley, RefWorks, ZoteroBib); posturas teóricas; 3D | Contenidos | **[L]** |
| **Modelación (12)** | Buscar en las bases CUN → exportar a ZoteroBib → pegar en Docs | Compartir pantalla. **Alto valor si se graba una vez** y se sube a la biblioteca de videos: el flujo se repite en los 4 cursos del docente y come 12 min cada vez | **[L]** |
| **Taller (22)** | **5 fichas de lectura** + 1 página de marco/revisión | **Taller con 5 preguntas `abierta`** (una ficha por pregunta), cada una con la estructura pedida en el enunciado (autor · año · aporte · relación con tu pregunta) y su rúbrica. La IA califica ficha por ficha. **Es el mejor encaje del módulo de talleres en todo el curso** | **[L]** |
| Cierre (8) | — | Definir y comunicar el nombre del archivo que falta: `S06_FichasMarco_Apellido` (⚠️ inferido por analogía con S01–S05) | — |

> **Brecha específica de esta sesión:** ExamLab **no tiene gestor de referencias ni ayuda de citación APA**. Las 5 fichas se recogen como texto; nada valida el formato APA, nada detecta duplicados, nada importa un DOI. Es la brecha §6.1 y afecta también al ACA 3.

---

### Las 26 h que el bloque no entrega — sesiones autónomas

El syllabus pide **32 h con docente**; el bloque real entrega **6 h** (6 encuentros × 1 h). Las 26 restantes no están asignadas en ningún archivo del corpus.

**Herramienta:** las sesiones de tipo **`autonoma`**. Cuando llega su fecha y hora, el sistema **notifica y envía correo** a los 20 matriculados por sí solo; el estudiante marca el material como revisado y eso registra su asistencia a esa sesión.

**Propuesta concreta:** 6 sesiones autónomas, una por semana entre jueves y jueves, con el material de la semana asignado y el foro correspondiente. Se importan **en el mismo CSV del cronograma** (la plantilla incluye la columna `session_type`), no una por una.

> **Nota de calendario:** los 6 jueves del curso (13/08 – 17/09) **no caen en festivo colombiano** —los festivos por Ley Emiliani se trasladan al lunes—. La regla *"jueves festivo → clase autónoma"* que el material repite cuatro veces **no se activa en este periodo**. La sesión `autonoma` sirve acá para otra cosa: dar contenedor formal a las horas que faltan.
>
> ⚠️ **Límite honesto:** la asistencia de una sesión autónoma es **autodeclarada** — el estudiante afirma que revisó. No hay verificación de lectura real. Sirve como registro y como recordatorio automático, no como evidencia de estudio.

---

## 4. Herramientas que sirven YA, sin desarrollo

Las seis que más pesan en este curso, en orden de valor.

### 4.1 Contenidos + Tablero del curso — cierra el defecto #1

Se sube la carpeta `Clases/` **completa** (acepta selección de carpeta y sube en lote), y el tablero asigna el material a cada una de las 6 sesiones. Formatos aceptados: `.pdf .pptx .docx .xlsx .md .txt .csv` + imágenes + `.zip`, hasta 25 MB por archivo. Visor inline sin descargar: el PDF se ve en la página, el `.pptx` con anotaciones por slide, el `.md` con editor.

**Lo que resuelve:** el defecto §6.1. La consigna real de cada taller —que hoy vive solo en `Guiones/`— se sube como un `.md` corto por sesión y el estudiante la recupera cuando revisa después de clase.

**Cómo separar lo del docente de lo del estudiante:**
- Los guiones **asignados a una sesión** se destildan del subconjunto visible (el docente elige archivo por archivo qué ve el alumno en esa sesión). No hay que renombrar nada.
- Los guiones subidos como **material general del curso** sí se filtran por nombre: un archivo que empiece por `GUIA_DOCENTE_` (o contenga `SOLUCION`, `EXAMEN`) nunca se le muestra al estudiante. Los guiones tal como se llaman hoy (`Sesion 01 - ….md`) **serían visibles**: hay que renombrarlos o asignarlos a la sesión y destildarlos.

**Extra que conviene conocer:** el módulo no solo sube — **genera con IA el paquete por clase** (presentación, guía docente, taller práctico, ejercicio con solución, examen con clave y rúbrica), con los prompts editables por curso. El material que genera **nace ya separado docente/estudiante** con la convención de nombres correcta. Es la vía más rápida para producir el instrumento que falta en la S03.

### 4.2 Tutor IA por curso — la pieza para las 64 h autónomas

Un chat por estudiante y por curso que **lee el texto real del material**, no los títulos: extrae `.pdf` (incluida la capa de texto), `.docx`, `.pptx` —**incluidas las notas del orador**, que suelen tener la explicación docente real de cada slide—, `.xlsx` y texto plano. El estudiante referencia un archivo escribiendo `#` y ese archivo se prioriza en el contexto. Responde **en vivo**, a las 11 pm de un domingo.

El prompt sembrado es explícitamente socrático y anti-atajo: *"acompañar al estudiante en el aprendizaje del material del docente, **NO resolverle los ejercicios**"*, con reglas de "no regalas soluciones" y "honestidad académica". Y el docente puede **sobreescribirlo para este curso**.

**Cómo se usa acá:** los guiones traen el criterio de calidad que el estudiante no ve —qué distingue una pregunta de investigación viable de una que no lo es, qué es un planteamiento y qué es ya una solución—. Ese criterio se pega en el override del prompt del curso, y entonces alcanza a los 20 en las 64 h autónomas, no solo a quien preguntó en los 16 min del taller.

**Límite real:** un PDF **escaneado** (sin capa de texto) es invisible. Y el material se trunca alrededor de 22.000 caracteres en total por consulta: si se sube todo el corpus, el tutor deja de ver lo último.

### 4.3 Banco de preguntas → taller autocorregible y Reto en vivo

Preguntas reutilizables por curso, con tema, dificultad, etiquetas y puntaje sugerido. Se importan a un taller, a un examen **o a un Reto en vivo**, y se pueden generar con IA desde temas o cargar por CSV.

**Cubre el hueco §6.2.** El vocabulario que el material identifica como error recurrente —etapas del método, tipos de conocimiento, pregunta cerrada/abierta/compuesta, distinguir problema de solución, reconocer fuente confiable, reconocer cita APA correcta— se escribe **una vez**, se etiqueta por unidad, y alimenta: el Reto en vivo del 20/08, la prueba de la S03 y la práctica de las 64 h.

**Sobre el Reto en vivo (Kahoot):** quiz con PIN, 4 colores, tiempo por pregunta y puntaje por velocidad, con **ranking acumulado del curso** entre semanas. El estudiante puede entrar **sin loguearse**, escaneando el QR e ingresando su correo institucional. Dos advertencias operativas: **nadie entra después de que arranca** (hay que dar margen en el lobby, sobre todo por Meet), y el correo debe ser el **institucional exacto**, no el personal.

> ⚠️ **Recomendación fuerte:** si se usa un examen para la prueba parcial, usarlo **sin proctoring**. La maquinaria de vigilancia (pantalla completa, advertencias, bloqueo de navegación) existe, pero en un pregrado 100% virtual, por Meet, con estudiantes en celular, es fricción que no compra nada formativo.

### 4.4 Foros — hoy no existen en el curso, en ninguna forma

El docente crea N foros por curso, cada uno con **ventana de apertura/cierre** y **sesión asociada**. Los estudiantes abren hilos y responden. Y —dato que cambia el uso— el docente puede **fijar un hilo arriba**, **cerrarlo** y **marcar una respuesta como oficial**, que queda destacada en primer lugar.

**Cómo se usa acá:** un foro por sesión, asociado a esa sesión, abierto desde el día de la clase hasta el día antes de la siguiente. La consigna real del taller va como **hilo fijado**; el criterio de calidad del guion va como **respuesta oficial**. Eso cubre el cierre que el material pide —*"lleva dudas concretas: el párrafo puntual, no 'no entendí nada'"*— con la forma exacta: la duda queda pegada a la sesión que la origina.

En pregrado esto vale doble: el estudiante que no habla en Meet frente a 20 compañeros sí escribe.

**Límites:** el foro **no se califica** (no hay rúbrica ni conteo de participación hacia el gradebook) y **no acepta adjuntos** — solo texto (que sí renderiza markdown con tablas).

### 4.5 Alerta temprana + progreso de material — la señal antes del ACA 1

Cada estudiante acumula **motivos** discretos y verificables: inasistencia, actividades reprobadas, no entregadas, promedio bajo. 0 motivos = sin riesgo, 1 = en observación, **2 o más = en riesgo**. Que hagan falta dos señales independientes para el rojo es deliberado: evita que un instrumento duro pinte medio curso. Solo lista a quienes requieren atención.

Tres reglas de justicia en la asistencia que conviene conocer: **tarde cuenta como que asistió**; **justificado sale del denominador**; y solo cuentan las sesiones donde el estudiante tiene registro (sin registros, "no hay dato", no "0% de asistencia").

En paralelo, el **progreso de material** dice *"abriste N de M archivos"* y la card del curso muestra *"Seguías en: …"*.

**Cómo se usa acá:** hay **6 hitos observables antes del primer 30%** (`S01_…` a `S06_…`), y un error listado en los 6 guiones: *"Avanzar contenido sin verificar el estado del avance previo"*. Revisar Alerta temprana **el miércoles antes de cada jueves** es la rutina que convierte esos hitos en acción. Con 6 semanas, detectar en el ACA 1 que alguien no arrancó ya es tarde.

**Límite importante:** **no llega sola.** No hay notificación automática ni persistencia del nivel de riesgo — el docente tiene que abrir el módulo de estadísticas. Es un hábito semanal, no una alerta.

### 4.6 Sesiones, asistencia y calendario

- **Generador de sesiones**: fecha de inicio + días de la semana + N sesiones → previsualización editable fila por fila, con los **festivos colombianos** ya calculados (Ley Emiliani y Pascua incluidas) y política de incluir / saltar / mover.
- **Import CSV de 8 columnas** (`session_date, title, start_time, end_time, meeting_url, cut_name, recording_url, session_type`) — las sesiones autónomas del §3 se marcan **en el mismo import**.
- **Check-in autónomo** con QR y código de 6 dígitos rotativo. Por Meet, el camino real es dictar/pegar el código en el chat. Con 20 estudiantes, marcar a mano también es viable.
- **Calendario**: el docente conecta Google **o Microsoft 365** y sincroniza las 6 sesiones **con los 20 estudiantes como invitados** (`sendUpdates=all`), generando el link de Meet. El estudiante además se suscribe a una URL `.ics` privada con sesiones y fechas de actividades.

**Cómo se usa acá:** cierra el defecto textual del material —*"Los CSV/ICS de Pregrado **no** incluyen invitados/estudiantes"*—. Hoy las fechas solo aparecen en la slide 7, vista una vez en la semana 1. En pregrado, *"no sabía que era hoy"* es causa real de no-entrega.

---

## 5. Lo que necesita workaround — con el costo exacto

### 5.1 Espina de pescado y árbol de problemas (Sesión 04)

**La situación real.** El lienzo existe y es Excalidraw completo, sin cuenta ni instalación. Lo que no existe es la **plantilla**: el catálogo trae **44 figuras en 6 categorías**, todas de ingeniería de software y redes (UML, diagrama de flujo, entidad-relación, estructuras de datos, arquitectura AWS, topología de redes). **No hay espina de pescado, ni árbol de problemas, ni post-it, ni mapa mental, ni FODA.**

**Tres caminos, con su costo:**

| Camino | Qué se obtiene | Costo | Recomendación |
|---|---|---|---|
| **A — Pizarra de sesión, docente** | El docente dibuja la espina **una vez** con rectángulo + línea + texto y **duplica la pizarra** para cada uso. Sirve para la fase de Modelación (12 min) | ~20 min de preparación, una sola vez | **Sí, para la modelación** |
| **B — Pregunta tipo `diagrama` en un taller** | **Un lienzo por estudiante**, persistido, con rúbrica y puntaje, calificable por IA. El editor renderiza jerarquías, así que el **árbol de problemas** sale bien | Escribir el enunciado + un ejemplo de estructura | **Sí, para el árbol** |
| **C — Excalidraw suelto + subir la imagen** | Lo que hacen hoy. La espina sale como el estudiante quiera | Cero preparación, pero el dibujo queda fuera de la plataforma y no se puede calificar con rúbrica | Solo si A y B no alcanzan |

**Lo que NO funciona:** la pizarra de sesión **compartida** (donde los estudiantes coeditan) es **una sola escena para toda la clase**, con último-que-escribe-gana. Con 20 personas dibujando en paralelo durante los 20 min del taller, es caos. No usarla para eso.

> ⚠️ **Marcado como inferido:** que el editor de diagramas renderice mapas mentales y matrices 2×2 se dedujo de que no filtra el tipo de diagrama y de que las librerías correspondientes están instaladas — **no se probó un render real**. Antes de comprometer la S04 con el camino B, hacer una prueba de 5 minutos con un árbol de ejemplo.

**Recomendación para la S04:** camino A para la modelación (docente) + camino B **solo para el árbol de problemas** en el taller. Para la espina, dejar el camino C explícito en la consigna: *"dibújala en Excalidraw y sube la imagen"*.

### 5.2 Matriz estructurada (S05 y ACA 3)

**Lo que falta:** no hay un tipo de pregunta tabular. El estudiante no puede llenar una grilla de N filas × M columnas.

**Lo que sí hay, y alcanza para el caso concreto:**

| Necesidad | Workaround | Costo |
|---|---|---|
| **Tabla síntoma / evidencia / consecuencia** (S05, modelación) | **Encuesta `mixed`** con 3 preguntas abiertas, una por columna. El docente lee **todas las respuestas de una columna juntas, con autor**. Una ficha de 3 campos son 3 preguntas | Armar la encuesta: 10 min. **No lleva nota ni entra al gradebook** |
| **Matriz de fuentes** del ACA 3 (autor, año, aporte, relación con tu pregunta) | **Taller con una pregunta `abierta` por fuente**, con la estructura pedida en el enunciado. 5 fuentes = 5 preguntas, cada una con rúbrica y calificable | Escribir el enunciado una vez. Sí lleva nota |
| **Tabla que el estudiante quiere que se vea como tabla** | Pegarla en **markdown en un hilo del foro** → renderiza con bordes | Cero, pero fuera del gradebook |

**Lo que NO funciona:** pedir la tabla markdown dentro de una respuesta de taller. Ahí se muestra en texto plano monoespaciado y salen los pipes crudos.

### 5.3 Rúbrica visible por criterios y niveles

**Lo que falta:** la rúbrica es un campo de texto libre. No hay criterios como filas, ni niveles con puntaje por celda, ni suma automática, ni reutilización entre actividades.

**El workaround, que es más barato de lo que parece:** escribir la rúbrica como **tabla markdown dentro del enunciado de la pregunta**. El enunciado se renderiza con soporte de tablas **en el momento en que el estudiante responde**, así que ve la rúbrica formateada **antes de entregar**.

```markdown
| Criterio | Insuficiente (0) | Aceptable (1) | Sólido (2) |
|---|---|---|---|
| Pregunta de investigación | No es pregunta o es un tema | Es pregunta pero muy amplia | Delimitada, con población y variable |
| Evidencia del problema | Solo opinión | Menciona una fuente | Cita fuente oficial con año |
| Formulación | Mezcla problema y solución | Separa parcialmente | Describe el problema sin proponer la solución |
```

**Costo:** escribirla una vez por actividad. **Lo que se gana además:** ese mismo texto es lo que la IA usa como criterio al calificar, así que la rúbrica que el estudiante lee y la que la máquina aplica son **literalmente la misma cadena** — no pueden divergir.

**Lo que sigue faltando:** no se puede consultar "cuántos fallaron el criterio 2", ni reutilizar la rúbrica entre las 6 sesiones sin copiar y pegar.

### 5.4 Registrar los 3 ACAs sin duplicar la entrega

**Situación:** los ACAs se entregan y califican en CDigital. Pero si no existen en ExamLab, Alerta temprana no los ve y el gradebook queda incompleto.

**Workaround:** crear cada ACA como actividad **externa** con el enlace a CDigital y registrar la nota en el editor de notas externas (columna Nota + columna **Observación** por estudiante). Configurar los cortes 30 / 30 / 40.

**Costo:** transcribir 20 notas tres veces = ~15 min por corte. **Lo que se gana:** los tres ACAs alimentan Alerta temprana, el gradebook y los informes, y sobre el ítem externo se puede colgar el **hilo de retroalimentación** que el ACA 2 exige.

⚠️ **Antes de configurar los cortes hay que decidir el desglose EV**, que en el syllabus está truncado en el origen (llega hasta `CORTE 1 / EV 01 / 9.0%`). Los propios ACAs lo admiten: *"Desglose EV exacto: confirmar en CDigital"*.

---

## 6. Brechas reales — sin maquillar

### 6.1 Gestor de referencias y ayuda de citación APA — **no existe**

No hay nada: ni biblioteca de referencias por estudiante, ni importación de DOI/BibTeX/RIS, ni formateo de cita, ni detección de duplicados, ni validación de formato APA. Lo único parecido es un campo de texto libre "Bibliografía sugerida" en el panel del Admin, que es una sola cadena por asignatura del Syllabus institucional.

**Impacto directo en este curso:** el ACA 3 (40%) pide una **matriz de fuentes** (autor, año, aporte, relación con tu pregunta); la S03 pide 3 referencias APA; la S06 pide 5 fichas de lectura y enseña gestores. **Ninguna de esas cosas tiene apoyo en la plataforma.** Se recogen como texto y se revisan a ojo.

**Qué se hace mientras tanto:** seguir con ZoteroBib (zbib.org), que ya está en la lista de herramientas permitidas del curso, y usar el taller de 5 preguntas `abierta` de la S06 como contenedor con rúbrica.

### 6.2 Historial de versiones del documento acumulativo — **no existe**

Los 3 ACAs son **el mismo documento creciendo** (4–7 → 6–10 → 10–15 páginas) con obligación explícita de incorporar la retroalimentación previa. La plataforma guarda **una entrega por actividad, sobrescrita**: la versión 2 pisa la versión 1. No hay forma de comparar, ni de verificar que la retroalimentación se incorporó.

**Lo más cercano, y su límite:** un proyecto se puede modelar como N secciones, cada una con su rúbrica, su nota y su hilo de feedback. Eso da un **semáforo por sección** —que es justo la técnica que el material ya usa— pero sigue guardando una sola versión de cada sección.

**Decisión sugerida para este bloque:** no montarlo. Es la pieza más grande de las que faltan y el bloque dura 6 semanas. Con 20 estudiantes, el seguimiento por sección se puede llevar en el editor de notas externas (columna Observación) sin construir nada.

### 6.3 Similitud entre entregas de prosa — **existe, pero está calibrado para código**

El comparador es **estudiante contra estudiante dentro de la misma actividad** — no busca en internet ni compara contra otros semestres. Dos cosas a saber:

- **La escala sí alcanza acá.** El comparador deja de ser exhaustivo por encima de 30 entregas; con 20 inscritos, este es el único de los cuatro cursos que **entra completo**.
- **Pero el criterio es de código.** El prompt busca nombres de variables idénticos, literales de cadena, valores hard-coded. **No busca paráfrasis, sinonimización, reordenamiento de oraciones ni estructura argumentativa** — que es exactamente cómo se copia un planteamiento del problema. Además trunca cada respuesta alrededor de 3.000 caracteres (≈500 palabras), y un planteamiento de 1–1.5 páginas se corta.

**Workaround posible:** el prompt de detección de plagio **es editable** y admite override por curso. Reescribirlo con marcadores de prosa (estructura argumentativa compartida, mismas fuentes en el mismo orden, transiciones idénticas) lo vuelve útil. ⚠️ **Verificar primero** que ese caso de uso esté expuesto en el panel del docente y no solo en el del Admin.

**Lo que sí funciona tal cual sobre prosa:** la estimación de **texto generado por IA** (prosa demasiado pulida, estructura genérica, ausencia de voz personal). Es una **señal para abrir una conversación, no una prueba**, y conviene decirlo así en clase antes de usarla.

### 6.4 Brechas menores, para que no sorprendan

| Brecha | Consecuencia acá |
|---|---|
| No hay revisión por pares con rúbrica ni asignación de revisores | El material de este curso no la pide con fuerza (los 9 entregables son individuales). Se puede aproximar con un hilo de foro por estudiante, sin pauta ni nota |
| La asistencia solo ofrece **presente** y **ausente** en el UI, aunque el motor entiende `tarde` y `justificado` | Con 6 encuentros, faltar a uno es el 17% del curso sincrónico. Una ausencia justificada no se puede registrar como tal |
| La biblioteca de videos **no reproduce** (abre en pestaña nueva) y no guarda la posición | Si se graba la demo de EBSCO/ZoteroBib, el estudiante la ve en YouTube/Drive, no dentro de la plataforma |
| No hay cronómetro de actividad proyectable con la consigna y el criterio visibles | Cada guion es un reloj (16–22 min de taller). Hoy la consigna se dice en voz alta |
| No hay chat de grupo ni canal de clase donde los 20 se vean entre sí | La difusión llega a cada uno por separado. Para discusión entre pares, el módulo es Foros |
| No hay portafolio ni bitácora del estudiante | Los 9 entregables quedan sueltos por actividad, sin vista agregada de "todo mi trabajo del bloque" |
| No hay generación del Reto en vivo **desde el material del curso** en la interfaz | El docente escribe los temas a mano al generar preguntas con IA |

---

## 7. Riesgos — con el pregrado como condición, no como detalle

Este es un curso de **pregrado, virtual, de 6 semanas, con 6 horas sincrónicas y 20 estudiantes que están viendo investigación por primera vez**. La diferencia con un posgrado no es de contenido: es que **la autonomía no se puede presuponer**. El material está diseñado como si sí (*"parta hoy con un mínimo viable; el autónomo completa"*), y esa es la tensión de fondo de todos los riesgos de abajo.

| # | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| **R1** | **Solo quedan 5 días hasta la S01** (hoy 08/08 · S01 el 13/08) y el ACA 1 vence el 20/08 | **Alto** | Montar únicamente la **Fase 0** de §8. Todo lo demás entra en marcha, después del 13/08 |
| **R2** | **Fatiga de herramientas**: CDigital + Meet + Google Docs + plantilla APA + ZoteroBib + Excalidraw + **ExamLab**. Siete superficies para seis encuentros | **Alto** | Presentar ExamLab como **una sola cosa**: *"acá está el material de cada sesión y acá se preguntan las dudas"*. No mencionar módulos que no se van a usar. Nunca pedir la misma cosa en dos lugares |
| **R3** | **Doble entrega**: si ExamLab pide entregar lo que ya va a CDigital, el estudiante entrega donde le califican y el resto queda vacío | **Alto** | Regla explícita desde la S01: **lo que vale nota va a CDigital; lo de ExamLab es práctica y borrador**. Los ACAs se registran como actividad **externa con enlace**, nunca como entrega |
| **R4** | **El estudiante de pregrado no entra por iniciativa propia.** Sin una razón semanal, la plataforma queda muerta en la semana 3 | **Alto** | Un motivo por semana, dicho en clase: el foro de la sesión (con el hilo fijado), el material del jueves siguiente, y el Reto en vivo que ya se anunció |
| **R5** | **Login inicial**: 20 personas con contraseña temporal y cambio forzado, coordinadas por Meet, en una sesión de 60 min | **Medio** | Enviar cuentas **48 h antes** de la S01 con el correo de bienvenida automático. Reservar 5 min del encuadre de la S01 para los rezagados, no 20 |
| **R6** | **Las URLs de CDigital y Meet están pendientes** en todo el material (`[URL CDigital — pendiente]`) | **Medio** | Bloquea el correo de bienvenida y el campo `meeting_url` de las sesiones. Conseguirlas es **prerrequisito** de la Fase 0 |
| **R7** | **La IA depende de configuración institucional**: una clave de proveedor activa y el modo de procesamiento. Si está en modo diferido, la generación con IA se encola en vez de responder en clase | **Medio** | Verificar **antes** del 13/08. El Tutor IA responde siempre en vivo; lo que se encola es la generación de contenido y preguntas — hacerla fuera de clase |
| **R8** | **Un PDF escaneado es invisible al Tutor IA.** Si el material clave del curso llega como imagen, el tutor responde sin él | **Medio** | Revisar los PDFs del corpus: si al seleccionar texto no se selecciona nada, no tiene capa de texto. Subir en su lugar el `.docx`/`.pptx` original |
| **R9** | **La espina de pescado no tiene camino limpio** por estudiante dentro de la plataforma (§5.1) | **Medio** | Probar el editor de diagramas con un árbol de ejemplo **antes del 03/09**. Si no convence, dejar la espina en Excalidraw suelto y decirlo en la consigna |
| **R10** | **El ACA 3 pide matriz de fuentes y no hay gestor de referencias** (§6.1) | **Medio** | Seguir con ZoteroBib. Recoger la matriz como taller de 5 preguntas `abierta` con rúbrica |
| **R11** | **La retroalimentación del ACA 1 vence el mismo día que cierra el ACA 2** (27/08), y el ACA 2 obliga a incorporarla | **Medio** | Adelantar la retroalimentación del ACA 1 a la semana del 24/08, o ajustar el requisito. Es decisión docente, no de herramienta |
| **R12** | **Reto en vivo:** nadie entra después de que arranca, el correo debe ser el institucional exacto, y un dispositivo con la hora desfasada ve las preguntas ya vencidas | **Bajo** | Dar 2 min de lobby. Anunciar "usá tu correo `@cun.edu.co`". Si a alguien "no le cargan las preguntas", revisar la hora de su teléfono |
| **R13** | **El OAuth de calendario puede estar bloqueado** por la política de la CUN para apps de terceros | **Bajo** | Probarlo primero. Si no conecta, el estudiante se suscribe a la URL `.ics` (no requiere permisos institucionales) |
| **R14** | **Contradicción documental de modalidad**: el syllabus marca `Presencial ☑` y el archivo se llama `_PRES`, pero la asignación del grupo dice **Virtual** | **Bajo** | Operativamente se resuelve marcando las 6 sesiones como `virtual` con el enlace de Meet. La contradicción del syllabus **no la arregla ninguna herramienta** y conviene reportarla |
| **R15** | **Alerta temprana no notifica**: hay que abrirla | **Bajo** | Ponerlo en la agenda: miércoles antes de cada jueves, 5 minutos |

---

## 8. Decisión recomendada y checklist

### Decisión

1. **Adoptar ExamLab con alcance recortado**, como capa de **material + acompañamiento + práctica**. La entrega y la nota siguen íntegramente en CDigital.
2. **Montar solo la Fase 0 antes del 13/08.** Lo que no quepa en 5 días entra en marcha o no entra.
3. **Prioridad al tramo autónomo**, no al sincrónico. Las 6 h de Meet ya funcionan con los guiones; las 64 h autónomas hoy no tienen nada.
4. **No montar este bloque**: seguimiento por secciones del documento, videos grabados de EBSCO/ZoteroBib, certificados, revisión por pares. Se evalúan para el próximo periodo con más margen.
5. **Un solo lugar por cosa.** Si algo está en CDigital, no se pide en ExamLab. Si algo está en ExamLab, no se manda además por correo.

### Checklist priorizado

**Fase 0 — antes del jueves 13/08 (bloqueante)**

- [ ] Conseguir la **URL de CDigital** y el **enlace de Meet** (bloquean R6 y el correo de bienvenida).
- [ ] Verificar con el Admin: clave de IA activa y **modo de procesamiento** (R7).
- [ ] Crear el curso `Investigación, Ciencia y Tecnología — 53339` con escala **0,1–5,0** y nota de aprobación institucional.
- [ ] Importar los **20 estudiantes por CSV** con `course_name` (matricula + correo de bienvenida en un solo paso). Contraseña temporal fija + cambio forzado.
- [ ] Generar las **6 sesiones** (jueves, 17:00–18:00, desde 13/08), marcadas como `virtual` con el enlace de Meet. Verificar que ningún jueves cae festivo — no debería.
- [ ] Subir la carpeta **`Clases/` completa** y asignar el material a cada sesión.
- [ ] **Guiones**: renombrarlos a `GUIA_DOCENTE_Sesion_NN.md` o asignarlos a la sesión y **destildarlos** del subconjunto visible al estudiante. Comprobar entrando con una cuenta de prueba.
- [ ] Subir la **consigna real de la S01** como `.md` corto visible al estudiante (cierra el defecto §6.1 para la primera sesión).
- [ ] Armar la **encuesta `mixed` del rompehileos** (expectativa + idea de tema).

**Fase 1 — semanas 1 y 2 (hasta el 27/08)**

- [ ] **Override del prompt del Tutor IA** para este curso: pegar el criterio de calidad de los guiones (qué hace viable una pregunta de investigación, qué separa problema de solución).
- [ ] Crear **un foro por sesión**, con ventana de la semana, hilo fijado con la consigna y el criterio como respuesta oficial.
- [ ] Configurar los **cortes 30 / 30 / 40** — ⚠️ antes hay que decidir el desglose EV, truncado en el syllabus.
- [ ] Registrar **ACA 1, 2 y 3** como actividades **externas** con enlace a CDigital.
- [ ] Sincronizar el **calendario** con los 20 como invitados; si el OAuth no conecta, publicar la URL `.ics`.
- [ ] Subir las consignas `.md` de las sesiones 02 a 06.
- [ ] Crear las **6 sesiones autónomas** semanales (importables en el mismo CSV, columna `session_type`).
- [ ] Rutina: **abrir Alerta temprana cada miércoles**, 5 minutos.

**Fase 2 — semanas 3 a 6**

- [ ] **Banco de preguntas** con el vocabulario del método científico → arma la prueba de la S03 que hoy no existe (§6.2 del corpus).
- [ ] **Reto en vivo** de repaso para la S02 (6 preguntas, 20 s).
- [ ] **Taller sin proctoring** con varios intentos para la S03, como práctica de las 64 h.
- [ ] **Probar el editor de diagramas** con un árbol de problemas antes del 03/09 (R9). Decidir camino B o C.
- [ ] Preparar la **pizarra plantilla** de espina de pescado y duplicarla.
- [ ] **Taller de 5 fichas** con rúbrica para la S06.
- [ ] Definir y comunicar el nombre de archivo faltante de la S06 (⚠️ inferido: `S06_FichasMarco_Apellido`).
- [ ] Si se va a usar detección de similitud: **reescribir el prompt de plagio** con marcadores de prosa (§6.3) y verificar que el caso de uso esté disponible para el docente.

**Cierre del bloque**

- [ ] Exportar el gradebook y contrastarlo con CDigital antes del 20/09.
- [ ] Registrar qué se usó y qué no, para decidir el alcance del próximo periodo.

---

## 9. Fuentes

### Material del curso (44 archivos, todos revisados)

| Documento | Aporte a este análisis |
|---|---|
| `INVESTIGACION CIENCIA Y TECNOLOGIA … EI005_PRES.docx` (18 tablas) | Identificación, créditos, unidades, metodología, sistema de evaluación (truncado), medios y ayudas |
| `2026/53339/Informacion.txt` | Grupo, cupo/inscritos, modalidad virtual, fechas del periodo |
| `Calendario de clases (oficial).md` | Las 6 sesiones, la regla de festivo, la nota de compresión U8+U10–12 |
| `2026/53339/Calendario de clases - Grupo 53339.md` · `Entregas y hitos…csv` | Hitos, y la nota de que los CSV/ICS **no** incluyen estudiantes |
| `Manual del Docente - Investigacion Ciencia y Tecnologia.md` | Fechas de cierre y de límite de nota por ACA |
| `Guiones/Sesion 01–06 ….md` | Estructura de 60 min, actividades por fase, nombres de entregable, tabla de remediación |
| `Clases/Sesion 01–06 …/Presentacion.pptx` (6) · `Presentacion del Curso….pptx` | Contenido visible al estudiante; evidencia de las slides idénticas |
| `Clases/Recursos/ACAs/ACA 1, 2, 3 ….docx` | Consignas, checklists, restricción "solo gratis + nube", "entrega oficial: solo por CDigital" |
| `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` | Formato obligatorio (y su origen de posgrado) |
| `Clases/LEEME - Material para estudiantes.docx` | Qué se comparte y qué no; el Padlet compartido entre 5 cursos |

### Verificación de la plataforma

- Inventario de herramientas verificado contra el catálogo de módulos, rutas, componentes y migraciones del repositorio de ExamLab.
- Informe de brechas verificado con búsquedas exhaustivas sobre el código fuente y las migraciones.
- **Verificación adversarial** que corrigió el inventario y el informe de brechas. Correcciones aplicadas en este documento, con prioridad sobre las fuentes anteriores:
  - El Tutor IA **sí** extrae `.pdf`, `.xlsx` y las notas del orador de `.pptx` (§4.2).
  - El CSV de sesiones tiene **8 columnas** e incluye `session_type` (§4.6).
  - Los foros **sí** tienen hilo fijado, cierre y respuesta oficial (§4.4).
  - Contenidos **genera** el paquete por clase con IA, no solo lo aloja (§4.1).
  - Existe **toggle por archivo** para el material asignado a una sesión (§4.1).
  - Existe **constructor de formularios** multi-campo con lectura agrupada por campo y autor (§5.2).
  - El tipo de pregunta `diagrama` **da un lienzo por estudiante**, persistido y calificable (§5.1).
  - El enunciado y la rúbrica se renderizan con soporte de **tablas markdown** (§5.3).
  - La reserva de un cupo **sí** genera invitación de calendario (con la hora de cierre, no la del cupo).

### Marcas de este documento

- ⚠️ señala **inferencias** y **contradicciones del material de origen**, no hechos verificados.
- Los tres puntos explícitamente inferidos son: el nombre de archivo faltante de la S06, el comportamiento del editor de diagramas con árboles y mapas (no probado con un render real), y la propuesta de 6 sesiones autónomas semanales como contenedor de las 26 h no asignadas.

---

*Documento interno de plan de curso · Investigación, Ciencia y Tecnología (EI005 · 53339 · 26P03) · no distribuir a estudiantes.*
