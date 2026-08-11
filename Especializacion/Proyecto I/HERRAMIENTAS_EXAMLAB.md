# Mapa de herramientas — ExamLab (PROYECTO I · ESP329 · 54ES4 · 26ES4)

> ⚠️ **Base desactualizada (2026-08-11).** Este análisis se escribió cuando el rompehielos de la
> Sesión 01 era un muro de Padlet en los cinco cursos. Ya no: con **más de 20 estudiantes** es el
> juego «dos verdades y una mentira» en **Slido** (Proyecto I, Creatividad, TG2 y TG3), y el muro
> solo sobrevive en **Investigación**, que tiene 20. Donde el texto proponga sustituir el Padlet,
> léase «sustituir el rompehielos actual»; el diagnóstico de fondo sigue valiendo.

| Campo | Valor |
|---|---|
| Curso | PROYECTO I (**ESP329**) — Metodología de investigación / anteproyecto |
| Programa | Especialización en Inteligencia Artificial |
| Grupo / Periodo | **54ES4** / **26ES4** |
| Docente | Julian Andres Castaño · `julian_castanoe@cun.edu.co` |
| Modalidad / Horario | Virtual (Google Meet) · **lunes 8:00–10:00 pm** (60 min contenido + 60 min tutoría) |
| Estudiantes | **40** adultos que trabajan → ~14 equipos de ≤3 |
| Plataforma oficial CUN | **CDigital (Moodle)** — no negociable |
| Herramienta evaluada | **ExamLab** (`examlab.lovable.app`) |
| Eje de este documento | **HERRAMIENTAS** (con qué se dicta y se acompaña) |
| Evaluación (aula CDigital) | Nota única Art. 41, operada en **3 cortes 25 / 25 / 50**: **Quiz** 25% (cuestionario) · **ACA 1** 25% (tarea) · **ACA FINAL** 42% (tarea) + **Autoevaluación** 4% (cuestionario) + **Coevaluación** 4% (**foro**) |
| Fecha | 2026-08-08 · **revisado 2026-08-10** contra el aula |
| Estado | **Borrador para aprobación docente** |

> ### ⚠️ Nota del 2026-08-10 — cómo se llaman las cosas en el aula
>
> La auditoría del libro de calificaciones (`AUDITORIA CDigital 2026-08-10.md` §2) mostró que **el aula nombra los ítems distinto** de como los numeraba el Syllabus ESP329: la ACA 1 del ESP329 es el ítem **«Quiz»** (cuestionario, 25%, corte 1), la ACA 2 es la **«ACA 1»** del aula (tarea, 25%, corte 2) y la ACA 3 es la **«ACA FINAL»** (tarea, 42%, corte 3). La **coevaluación es un FORO** (se participa) y la **autoevaluación un cuestionario**. **Los pesos y las fechas no cambiaron** (siguen las de Coordinación); lo que cambia es a qué ítem se le entra la nota.
>
> **Actualización 2026-08-11:** este documento ya está reescrito con los **nombres del aula** — igual que el `PLAN_VIABILIDAD_EXAMLAB.md`, el Manual, el `Calendario de clases (oficial).md` y los enunciados del estudiante. Cuidado con la trampa que dejaba la numeración vieja: **lo que cierra el 30/08 es el Quiz**; la **ACA 1** del aula cierra el **04/10**. Las referencias entre comillas invertidas del tipo `` `ACA 2:18` `` son **citas a los enunciados anteriores al 2026-08-10** (archivo y número de línea de entonces) y se conservan tal cual como rastro de dónde salió cada requisito.
>
> Segunda corrección: auto y coevaluación **no son exclusivas de Proyecto I** — existen también en los 4 cursos de pregrado, con peso menor. Y las ventanas oficiales son **coevaluación 09–15/11** y **autoevaluación 16–22/11** (este documento traía 10–16/11 y 17–22/11).

> **Este documento COMPLEMENTA, no reemplaza, a [`./PLAN_VIABILIDAD_EXAMLAB.md`](./PLAN_VIABILIDAD_EXAMLAB.md).**
> Ese plan analizó el curso por el eje de las **ENTREGAS** y concluyó *"viable condicionado — ExamLab como complemento de CDigital, nunca como reemplazo"*. Esa conclusión se mantiene íntegra y **no se re-discute acá**: la entrega oficial del **Quiz**, la **ACA 1** y la **ACA FINAL**, más la coevaluación y la autoevaluación, siguen en CDigital.
> Lo que este documento responde es otra pregunta: **¿qué herramientas de ExamLab le sirven al docente para DICTAR y ACOMPAÑAR este curso, sesión por sesión?** Herramienta = algo con lo que el estudiante o el docente *trabaja* durante la sesión o entre sesiones (tutor de IA, pizarra, foro, encuesta en vivo, material por sesión, calendario, seguimiento). Dónde se sube el `.docx` final y cuánto pesa en la nota **queda fuera de alcance** — eso ya está resuelto en el documento hermano.

---

## 1. Resumen ejecutivo

**Veredicto sobre el eje herramientas: adopción recomendada, con alcance acotado a 7 herramientas y 3 brechas declaradas.**

Por el eje de entregas, ExamLab quedó como "complemento de contabilidad" (notas + retro + evidencia). Por el eje de herramientas el resultado es **mejor de lo esperado y por razones distintas**: el curso tiene un problema estructural de acompañamiento —60 minutos de contenido, 60 de tutoría, ~14 equipos, y **el 42% de la nota concentrado en un tramo con solo 2 lunes sincrónicos** (`Manual:27`, `Calendario:11-12`)— y ExamLab tiene exactamente las piezas que atacan eso: sesiones autónomas con notificación por correo, material anclado a la fecha, un tutor de IA que lee el material real del docente, un foro con ventanas y un agendador de cupos.

Tres precisiones que definen el alcance, y las tres son honestas:

1. **La herramienta con mayor palanca es el Tutor IA**, y no por ser IA: porque **extrae el texto real** de los `.docx` y `.pptx` del docente y responde citándolos. Los 11 guiones contienen los criterios que hoy solo existen en la cabeza del docente (verbos vetados, la frontera antecedente ≠ marco teórico, "empezar por la solución no es un problema"). Subidos como material + un override de prompt por curso, eso pasa a estar disponible a las 11 pm, que es cuando este perfil de estudiante escribe.
2. **La única necesidad de herramienta que el material del curso nombra explícitamente ya está adentro**: el guion de la S05 pide *"Mapa en Excalidraw/tldraw: Pregunta al centro → constructos → autores clave"*. ExamLab trae Excalidraw como pizarra de sesión, compartida en vivo y persistida contra esa sesión.
3. **Una sesión completa se queda sin herramienta: la S09.** Su actividad central es que el estudiante *bosqueje un instrumento* (10–15 ítems + tabla de alineación ítems↔objetivos). ExamLab tiene un constructor de cuestionarios excelente… y tres candados que impiden que un estudiante cree uno. Se dice explícito en §3 y §6; no se maquilla.

### Necesidad → herramienta → estado

| # | Necesidad del curso | Herramienta ExamLab | Estado |
|---|---|---|---|
| 1 | Material de la semana publicado **antes** del encuentro (aula invertida, `Manual:50`) | Contenidos + asignación a sesión | ✅ **Lista** |
| 2 | Sustituto asincrónico de las sesiones que no existen (4 lunes festivos + tramo de la ACA FINAL) | **Sesión `autonoma`** (notifica por correo a la hora fijada + el alumno marca "material revisado" y queda asistencia) | ✅ **Lista** |
| 3 | Grabación de las 2 h ligada a su sesión (evidencia AFI <24 h, `Manual:96`) | `recording_url` + **sync automático desde Google Calendar cada 6 h** | ✅ **Lista** |
| 4 | Calendario único con sesiones, festivos y ventanas | Generador de sesiones con **festivos de Colombia calculados** + suscripción `.ics` del estudiante | ✅ **Lista** |
| 5 | Tutoría asincrónica 24/7 sobre el material real del curso | **Tutor IA** + override del prompt `tutor_chat` por curso | ✅ **Lista** |
| 6 | Modelar en vivo y que el ejemplo **no se pierda** con la sesión | **Pizarra de sesión** (Excalidraw) + modo compartido en vivo | ✅ **Lista** |
| 7 | Chequeo de comprensión con resultado visible en el momento | **Encuesta `single`** lanzada desde la sesión (`results_visible = always`) | ✅ **Lista** |
| 8 | Publicar el avance de cada equipo y que los demás lo lean/comenten | **Foro** por curso, con ventana `opens_at`/`closes_at` | ✅ **Lista** |
| 9 | Drill de citación APA reutilizable entre cohortes | **Banco de preguntas** por curso (+ taller autocalificado o Reto en vivo) | ✅ **Lista** |
| 10 | Iterar el avance después de la retro, sin acción manual del docente | `max_attempts` del taller (1 → 5) | ✅ **Lista** (el default institucional es **1**) |
| 11 | Probar el curso tal como lo ve un estudiante | `/app/teacher/students` → **"Ver como"** (impersonación acotada a sus cursos) | ✅ **Lista** |
| 12 | Agendar tutorías por equipo con cupo (`ACA 1:47`: *"no hay atención espontánea sin cita"*) | **Encuesta `slot`** (tipo Doodle, con claim atómico de cupo) | ⚠️ **Workaround** (la hora vive en el texto del cupo; **al publicar NO manda correo**; sin export) |
| 13 | Captura estructurada por campos (fichas de S01, S06, S08, S10) | **Encuesta `mixed`** (abierta + cerrada, multi-pregunta) | ⚠️ **Workaround** (solo 2 tipos; sin export CSV; preguntas inmutables tras la 1.ª respuesta; **las abiertas solo las ve el docente**) |
| 14 | Auto-chequeo contra los criterios reales del ACA, antes de entregar | Taller **peso 0** con `abierta` + `expected_rubric` + calificación IA | ⚠️ **Workaround** (el alumno **pega texto**; la IA no lee `.docx` ni `.pdf`) |
| 15 | Detección temprana de quién no trae nada | **Alerta temprana** (semáforo por estudiante) | ⚠️ **Workaround** (arranca **ciega**: requiere los ACA creados como `is_external` con `due_date`) |
| 16 | Devolver el `.docx` anotado al equipo | **Mensaje 1-a-1 con adjunto** (25 MB, 8 archivos, sin filtro de tipo) | ⚠️ **Workaround** (1-a-1 ⇒ **3 mensajes por equipo**) |
| 17 | Lista de verificación que el estudiante marca y el docente ve consolidada | Encuesta `mixed` con `cerrada` sí/no por criterio | ⚠️ **Workaround** (el `.md` publicado **no** es marcable) |
| 18 | Muro colaborativo con entrada por QR **sin cuenta** (rompehielos S01) | — | ❌ **No existe** → mantener Padlet en S01 |
| 19 | Señal real de que el estudiante abrió el material | `content_file_progress` (la base **sí** lo registra) | ❌ **Sin pantalla docente** → usar la sesión autónoma como señal autodeclarada |
| 20 | Canal por equipo / bitácora del *"acuerdo observable"* (`Guiones/*:97`) | — | ❌ **No existe** (el chat de grupo está en la base, **sin interfaz**) |
| 21 | Registro de correcciones con estado pendiente → atendido (`ACA 2:18`) | — | ❌ **No existe** |
| 22 | Gestor de referencias · verificación APA 7 · comprobación de DOI | — | ❌ **No existe** (0 rastros en todo el producto) |
| 23 | Que el **estudiante** diseñe y aplique su propio instrumento (S09) | — | ❌ **No existe** (3 candados independientes) |

**Recomendación:** adoptar las 11 herramientas del bloque ✅ como base del curso, aceptar los 6 workarounds del bloque ⚠️ con su costo escrito, y **declararle al estudiante en la S01 las 5 brechas del bloque ❌**, para que nadie las busque. No pilotear nada que exija que el estudiante cree encuestas, marque checklists o gestione referencias dentro de ExamLab.

---

## 2. Cómo leer el mapa de sesiones

Tres convenciones, para que la sección 3 se lea rápido:

- **Fechas.** Se usa el mapeo de sesiones ya fijado en §9 del plan de entregas (inicio 10/08/2026). Las discrepancias de fechas entre el Cronograma de Coordinación y los enunciados ACA **están abiertas y son bloqueantes**, pero se resuelven allá (§11a de ese documento), no acá.
- **Origen de la actividad.** Las 11 `Presentacion.pptx` **no contienen las actividades**: sus slides 4, 5 y 6 son idénticas en todas las sesiones y la slide 5 remite a `Clases/Recursos/ACAs/`. Todo lo que aparece como actividad sale de `Guiones/Sesion NN - ….md` y de los enunciados ACA. Lo marcado *(inferido)* es lectura mía, no texto del curso.
- **Marco fijo de las 11.** Encuentro de 2 h = **60 min de contenido + 60 min de tutoría en vivo por equipos**; aula invertida; grabación completa; equipos de máx. 3; el estudiante registra su asistencia a tutoría en un formulario externo; **en Proyecto I los instrumentos se proponen, no se aplican**. Eso no se repite en cada fila.

---

## 3. Mapa sesión por sesión (01 → 11)

### Sesión 01 · 10/08 — Presentación del curso · docente · estudiantes · ACAs

**Tema.** **Sesión de encuadre: no dicta contenido curricular.** Se presenta el curso, el Docente, los estudiantes y los tres ítems calificables del aula (**Quiz · ACA 1 · ACA FINAL**), más acuerdos de trabajo: frontera Proyecto I → Proyecto II; el docente como **garante metodológico**, no experto temático; las 2 líneas oficiales de IA del programa; ética mínima del día 1; estructura 60+60. La ESP329 U1 (fundamentos y enfoque de investigación) va como **lectura autónoma** y se retoma al abrir la Sesión 02.

**Actividad.** Rompehielos en muro con QR (~7 min): un aporte con expectativa + **tema tentativo en una frase**. Taller de 18 min: **ficha de encuadre** (integrantes ≤3, línea oficial, tema en una frase, contexto, una duda metodológica). Tutoría por equipos. Registrar asistencia como evidencia.

**Herramienta.**

| Pieza de la sesión | Herramienta | Nota operativa |
|---|---|---|
| Rompehielos con efecto espejo | **Padlet (fuera de ExamLab)** + en paralelo un **foro** "Preséntate y di tu tema", un hilo por persona | ⚠️ **No usar la pizarra compartida ese día.** No tiene QR, exige estar logueado y matriculado, y ese lunes los 40 recién reciben credenciales temporales con un diálogo de cambio de contraseña **bloqueante**. 40 primeros logins en 7 minutos por Meet no ocurre. El foro sí da el efecto espejo, pero asíncrono durante la semana |
| Ficha de encuadre (5 campos) | **Encuesta `mixed`**: 1 `cerrada` (las 2 líneas oficiales de IA) + 4 `abierta` | ⚠️ Las respuestas abiertas **solo las ve el docente y el propio autor** — sirve como captura, no como muro |
| Material del curso | **Contenidos**: presentación del curso, plantilla APA, los 5 enunciados del aula como *material general del curso* | Convertir a **PDF** lo que se quiera leer inline: `.docx` y `.pptx` subidos son **descarga pura** |
| Calendario del semestre | **Generador de sesiones con festivos de Colombia** (ya corrido antes de la S01) + el alumno se suscribe al **`.ics`** | Hace visible el día 1 el choque de la **ACA FINAL** con 12/10 y 02/11 |
| Orientación en la plataforma | **Tour guiado del rol Estudiante** (~15 pasos, ya construido) + **⌘K** | ⚠️ El tour **no se dispara en pantallas <768 px**: quien entre por celular no lo verá nunca |
| Asistencia | **Check-in por QR**, variante **pública sin login** (el alumno pone correo + contraseña y queda registrado) | Exige estar **matriculado**: hacerlo después de la matrícula, no antes |
| Equipos | Editor de grupos por **drag & drop** en el taller del primer corte | El auto-registro (`self_signup`) **no está expuesto**: los ~14 equipos los arma el docente a mano |

---

### Sesión 02 · 24/08 — Problema y pregunta de investigación

**Tema.** Tema ≠ problema ≠ pregunta; criterios de calidad de la pregunta; **tabla de pares débil vs fuerte**; las 5 preguntas de delimitación; errores típicos (empezar por la solución, pregunta sí/no, tema fuera de línea).

**Actividad.** Modelación en vivo (12 min): síntoma → contexto → pregunta delimitada → *qué NO es la pregunta*. Taller de 18 min: 8–12 líneas + pregunta en una frase. Micro-exposición cruzada: **3 equipos leen su pregunta en 20 segundos**. Autónomo: 3 referencias exploratorias.

**Herramienta.**

| Pieza | Herramienta | Nota |
|---|---|---|
| *"¿esto es tema, problema o pregunta?"* con resultado en vivo | **Encuesta `single`** lanzada desde la sesión, `results_visible = always` (histograma en tiempo real) | 3 ítems = **3 encuestas** (una pregunta por encuesta). Hoy ese diagnóstico es una pregunta oral a dos personas |
| Modelación en vivo | **Pizarra de sesión** — familia *Diagrama de flujo* (Proceso · Decisión · Inicio/Fin) + puntero láser | La escena queda anclada a la sesión; el alumno la ve después si se activa "Pizarra compartida" |
| Que las 14 preguntas se lean y se comenten (no solo 3) | **Foro** "Nuestra pregunta", **un hilo por equipo** | Resuelve el cuello real: 20 segundos alcanzan para 3 de 14 equipos |
| Banco de pares débil/fuerte | **Contenido `.md`** publicado (se lee inline en la app) | Hoy esos pares viven **solo** en el guion del docente; el estudiante nunca los ve |
| Dudas de medianoche | **Tutor IA** | Con el override del prompt, ya sabe distinguir problema de solución |

---

### Sesión 03 · 31/08 — Objetivos, justificación, alcances y limitaciones

**Tema.** Objetivo general vs específicos; **verbos permitidos** (analizar, caracterizar, diseñar, contrastar, proponer) vs **vetados** (conocer, aprender, interesarse); justificación como argumento de pertinencia, no autobiografía; alcance = promesa / limitación = honestidad; **coherencia del hilo completo**, que es lo que evalúa ACA1.

**Actividad.** Actualizar la pregunta si cambió. Modelación: 1 general + 3 específicos. Taller de 20 min: objetivo general, 3 específicos, justificación de ½–1 página, alcances y limitaciones. Empaquetar contra los 6 criterios del checklist de `ACA 1`.

**Herramienta.**

| Pieza | Herramienta | Nota |
|---|---|---|
| Que los 6 criterios del **Quiz** estén **donde se redacta** | **Taller formativo peso 0** con 3 preguntas `abierta` (pregunta de investigación · objetivo general · 3 específicos) y en cada `expected_rubric` los criterios reales + los verbos vetados → **la IA devuelve observaciones en ~10 s** | ⚠️ El alumno **pega el texto** (la IA no lee `.docx`). Acotarlo a ~15 líneas, no al ACA completo. **Requiere** que la IA esté en modo inmediato (§7, R5) |
| Iterar tras la observación | **`max_attempts` = 4** en ese taller | El default institucional es **1**: sin subirlo, el alumno entrega una vez y queda bloqueado, y el docente tendría que reabrir 40 entregas a mano |
| Referencia de verbos aceptados/vetados | **Contenido `.md`** | Consultable en el momento de redactar |
| Aviso de la ventana de entrega (no dicho al aire en el cierre de clase) | **Mensaje programado** en agosto para todo el semestre | El recordatorio automático de vencimiento existe, pero tiene **dedup permanente**: si se mueve la fecha, **no hay segundo aviso** |
| Vista "pregunta \| objetivo general \| específicos" lado a lado | **No existe como vista** | Sustituto: las 3 respuestas del taller quedan una debajo de otra en la pantalla de calificación. Es lo más cerca que se llega |
| Muestrario de ejemplos bien resueltos | **Contenido `.md`** generado con IA y publicado | Hoy se modela en pantalla y se evapora con la sesión |

---

### Sesión 04 · 07/09 — Retroalimentación del Quiz · Antecedentes de investigación

**Tema.** Criterios con los que el docente leyó el **Quiz**, devolviendo **2–3 hallazgos accionables sin reescribir el texto**; qué es un antecedente y qué no (y **tampoco es marco teórico todavía**); meta de **mínimo 6, nacionales e internacionales**; estructura de la ficha (autor, año, propósito, método, hallazgo y **relación explícita con SU pregunta**); error frecuente: **"decoración bibliográfica"**.

**Actividad.** Recibir retro y trabajar correcciones en paralelo, con trazabilidad visible exigida en la **ACA 1**. Ver 1 ficha modelo llenada en pantalla. Taller de 20 min: buscar al menos 2 antecedentes hoy. Autónomo: completar 6.

**Herramienta.**

| Pieza | Herramienta | Nota |
|---|---|---|
| Nota + retro cualitativa del **Quiz** | **Notas de actividades externas** (grilla de los 40 con **Nota + Observación**) | Es literalmente lo que pide `Manual:95` (*retro cualitativa y cuantitativa*) |
| Devolver el **`.docx` anotado** al equipo | **Mensaje 1-a-1 con adjunto** (25 MB, hasta 8 archivos, **sin filtro de tipo**) | ⚠️ **No hay chat de equipo** (existe en la base, sin interfaz) ⇒ **3 mensajes por equipo, ~40 en total**. El mensaje queda **inmutable una vez leído**, lo que sí lo vuelve evidencia |
| Ficha modelo llenada en vivo | **Pizarra de sesión** — la caja de 3 zonas de *UML·Clase* / *DB·Tabla* sirve como ficha (autor+año / método / hallazgo) | El catálogo de 44 figuras no fue diseñado para metodología: de 6 familias, solo *Diagrama de flujo* y *Entidad–Relación* se reutilizan |
| Matriz de antecedentes del equipo | **Foro** — un hilo por equipo, **una respuesta por ficha**, con enlace/DOI | ⚠️ **No teclear la matriz como tabla markdown de 6×6**: un posgrado que redacta en Word no lo hace. La matriz vive en Drive; al foro va el **enlace + el hallazgo y su vínculo con la pregunta en prosa**. Solo el foro renderiza markdown; la vista de calificación de taller **no** |
| Contador "n de 6" | **No existe** | Sustituto: cuenta de respuestas en el hilo del equipo. Es el único entregable del curso con un número duro y ExamLab no lo lleva |
| Frontera antecedente ≠ marco teórico a las 11 pm | **Tutor IA** con la frontera escrita en el override | La fija **este curso**, no una regla general: por eso el override importa más que el modelo |

---

### Sesión 05 · 14/09 — Marco teórico

**Tema.** Antecedentes (qué se investigó) vs marco teórico (con qué lentes se explica); hilo pregunta → conceptos → autores → contexto; **profundidad sobre acumulación** (*"2–4 constructos bien hilados > 15 citas decorativas"*); teoría que no se usa después en el método.

**Actividad.** El docente **modela un mapa de constructos** — *"Mapa en Excalidraw/tldraw: Pregunta al centro → constructos → autores clave"* (texto literal del guion). Taller de 20 min: (1) su mapa, (2) 1–2 páginas del primer apartado. Tutoría: mostrar lo escrito, una pregunta de coherencia, **un acuerdo observable** para la próxima.

**Herramienta.** Es la sesión donde el encaje es **exacto**, porque el guion nombra la herramienta.

| Pieza | Herramienta | Nota |
|---|---|---|
| Mapa de constructos, modelado y luego construido por cada equipo | **Pizarra de sesión con "Pizarra compartida" activada** — Excalidraw, los alumnos matriculados **editan la misma escena en vivo** | Familia *Entidad–Relación* como nodos de mapa conceptual (constructo = entidad, relación = rombo etiquetado, atributo = óvalo). ⚠️ **Última escritura gana**, sin fusión: con muchos dibujando a la vez hay ~1,5 s de ping-pong. Mitigación práctica: asignar una zona del lienzo por equipo. Tope de 5 MB por escena |
| Que el mapa **quede** y no se pierda | La escena se persiste contra la sesión + **viewport persistente** por hoja | Es exactamente lo que hoy no pasa: la app externa no deja el resultado asociado al curso |
| Dejar el párrafo puntual **antes** de la tutoría | **Foro** con `closes_at` la noche anterior al encuentro | Hoy el vehículo es el chat de la videollamada, que no persiste. Así el docente llega habiéndolo leído |
| "Este constructo no se usará en el método" | **Tutor IA** (el estudiante le pega su borrador) | Es uno de los dos errores que el guion declara; hoy solo se detecta si el docente alcanza a leer el texto en los 8–12 min de tutoría |
| Bitácora del *"acuerdo observable"* | **No existe** | El campo por (alumno, sesión) existe en la base pero **no tiene casilla en la interfaz**: solo entra por importación CSV. Ver §6 |

---

### Sesión 06 · 21/09 — Marco conceptual y marco contextual

**Tema.** Marco conceptual = **definiciones operativas** (cómo se entenderá cada término *en este estudio*); marco contextual = dónde ocurre (organización, proceso, territorio, restricciones), con la prohibición explícita del contexto genérico.

**Actividad.** El docente arma en pantalla una **tabla de 4 columnas**: `Término | Definición teórica | Definición operativa | Por qué importa a la pregunta`. Taller de 22 min: completarla con **4–6 términos** + 1 página de contexto. Criterio de éxito: *"términos operativos no ambiguos"*.

**Herramienta.**

| Pieza | Herramienta | Nota |
|---|---|---|
| La tabla de 4 columnas como **datos**, no como prosa | **Encuesta `mixed`**: 4 preguntas `abierta` por término (o una por columna) | El valor real: el docente lee **la columna "definición operativa" de los 14 equipos de un golpe** y detecta las ambiguas — que es literalmente el criterio de evaluación. ⚠️ **Las preguntas se vuelven inmutables** apenas llega la primera respuesta: diseñar la ficha bien la primera vez. ⚠️ **Sin export**: para analizar fuera hay que transcribir |
| Lectura cruzada entre equipos sobre las definiciones | **Foro** | La revisión de pares es el mecanismo más económico contra "ambiguo", y hoy no existe: la única revisión posible son los 8–12 min de tutoría |
| Mapa del contexto (organización / proceso / restricciones) | **Pizarra de sesión** | Se explica peor en prosa que en dibujo |
| Glosario que se reusa en S08 y S09 | **No existe** como entidad | Las definiciones quedan dentro de la encuesta; se re-escriben en la metodología. Costo aceptado |

---

### Sesión 07 · 28/09 — Marco legal · citación APA 7

**Tema.** Marco legal *si aplica* (y si no, declararlo honestamente, sin inventar leyes); APA 7 en lo que más se rompe (cita en texto vs referencia, DOI/URL, **copiar bibliografía sin citar en el cuerpo**); herramientas de citación en nube. Cierra el bloque referencial.

**Actividad.** **"Clínica APA"** (14 min): *"Corrijan en vivo 3 errores típicos que yo pego en el chat"*. Taller de 20 min: limpiar referencias y verificar que **toda cita del cuerpo esté en la lista y viceversa**. Criterio: *"0 citas huérfanas evidentes"*.

**Herramienta.** Es la necesidad **peor servida** del curso hoy: los 3 errores se pegan en el chat de Meet, no queda registro, no se sabe **quién** acertó, y el ejercicio se rearma cada cohorte.

| Pieza | Herramienta | Nota |
|---|---|---|
| Clínica APA con respuesta individual y corrección automática | **Banco de preguntas del curso**: 8–10 ítems `cerrada` (generables con IA) → servidos como **taller autocalificado peso 0** | **Recomendado sobre el Reto en vivo** para este perfil: el juego exige sostener Meet + el cronómetro en el mismo dispositivo y hay un fallo conocido por reloj del celular desfasado. El taller asíncrono conserva lo que importa (diagnóstico por estudiante + reuso entre cohortes) y pierde solo el show. El Reto en vivo queda como opción si el docente lo quiere |
| Que el banco **sobreviva al semestre** | El banco vive **por curso** y se importa a otros formatos | Convierte 14 minutos de clase en un activo permanente. ⚠️ La IA genera bien `cerrada`; **`cerrada_multi` llega sin opciones** y todo llega con puntaje 1 |
| Checklist de cierre referencial | **Contenido `.md`** publicado + una **`mixed` con las casillas como `cerrada` sí/no** | El `.md` **no es marcable**: un `- [ ]` se ve como casilla pero nadie puede tildarla y no se persiste. Lo consolidable es la encuesta |
| Enlaces de trabajo (Scholar, SciELO, Redalyc, biblioteca CUN, generador de citas) | **Contenido `.md`** como material general del curso | Hoy viven enterrados dentro del enunciado `ACA 2`, no al alcance de la mano |
| Detectar citas huérfanas en el propio texto | **Tutor IA** sobre un fragmento pegado | El criterio es mecánico y verificable, así que la revisión automática reemplaza trabajo repetitivo casi sin pérdida. ⚠️ **No verifica que la fuente exista ni que el DOI sea real** — ver §6 |

---

### Sesión 08 · 05/10 — Diseño metodológico: paradigma, enfoque y alcance

**Tema.** Enfoque (cuantitativo / cualitativo / mixto) que *"debe conversar con la pregunta"*; alcance (exploratorio / descriptivo / correlacional / explicativo); diseño como esbozo para Proyecto II; la **"coherencia de oro"** (pregunta cuantitativa con encuesta de escalas ≠ enfoque cualitativo de entrevistas). Es **sesión puente** antes del tramo con 2 lunes.

**Actividad.** Modelación de la matriz `Pregunta | Enfoque | Alcance | Técnica tentativa | Por qué coherente`. Taller de 20 min: completarla para su proyecto, con **justificación explícita de coherencia**.

**Herramienta.** El mejor encaje de la familia de encuestas, porque dos de los cuatro campos son **listas cerradas**.

| Pieza | Herramienta | Nota |
|---|---|---|
| La matriz metodológica | **Encuesta `mixed`**: `cerrada` para enfoque (3 valores) · `cerrada` para alcance (4 valores) · `abierta` para técnica · `abierta` para la justificación | La incoherencia "cualitativo + escalas" **se ve escaneando dos columnas**; hundida en un párrafo de un adjunto, no |
| Sondeo antes de soltar el taller | **Encuesta `single`** *"¿tu estudio es cuantitativo, cualitativo o mixto?"* | El docente ve la distribución del grupo en 30 segundos y decide si re-explica, en vez de descubrir el error una semana después leyendo fichas |
| Guardrail **"propuesto, NO aplicado"** | Una `cerrada` obligatoria dentro de la misma `mixed`: *"¿aplicaste el instrumento a alguien?"* sí/no | Es la restricción más repetida del curso (`ACA 1:33`, `ACA 3:27,31`) y hoy solo se controla verbalmente |
| Cadena de coherencia como diagrama | **Pizarra de sesión**, familia *Diagrama de flujo* | La cadena es literalmente cajas con flechas |
| Interrogar la cadena pregunta↔enfoque↔alcance↔técnica | **Tutor IA** con la "coherencia de oro" escrita en el override | Es una regla verificable, no una opinión |

---

### Sesión 09 · 19/10 — Devolución de la ACA 1 · población, muestra e instrumentos propuestos

> ### ⚠️ Esta es la sesión que se queda SIN herramienta para su actividad central.

**Tema.** Población vs muestra; criterios de inclusión/exclusión; técnicas e instrumentos **propuestos** (encuesta, entrevista, rúbrica de observación, análisis de logs) con propósito, estructura, validez tentativa y plan de análisis; alineación ítems ↔ objetivos ↔ categorías. Regla de oro: **se proponen, no se aplican**.

**Actividad.** Taller de 20 min: **bosquejar el instrumento** — 10–15 ítems o guía de 8 preguntas — **+ un párrafo de plan de análisis**, con la tabla de alineación ítem ↔ objetivo.

**Por qué no hay herramienta.** La actividad cae en **dos brechas simultáneas**:

1. ExamLab tiene un constructor de cuestionarios multi-pregunta completo y bien hecho… pero **el estudiante no puede crear uno**. Hay tres candados independientes: la seguridad de la tabla de encuestas exige ser docente del curso, la de las preguntas también, y la ruta del constructor está restringida al rol Docente. No es configuración: es diseño del producto.
2. **No existe un tipo "tabla / matriz"** que el estudiante llene. Los 12 tipos de pregunta del producto son texto, código, consola, GUI, SQL y diagrama. La tabla de alineación ítem↔objetivo no tiene dónde vivir.

**Fallbacks, con su costo real:**

| Fallback | Qué se gana | Qué se paga |
|---|---|---|
| **(a) Foro** — el bosquejo del instrumento pegado como texto (o tabla markdown) en un hilo por equipo + lectura cruzada | Queda registro, hay revisión de pares, el docente lo lee antes de la tutoría | Se teclea a mano; nada valida columnas; no exporta; no es el acto de *diseñar* un instrumento |
| **(b) El docente transcribe la encuesta de un equipo piloto** a una `mixed` real y la lanza al curso | El instrumento se **prueba con población real**, que es lo que un curso de investigación quiere | No escala: **14 equipos = 14 encuestas transcritas**. Y el diseñador **nunca recupera los datos**: un estudiante solo ve su propia respuesta, y **no hay export en ningún formato** — alguien transcribe a mano desde la pantalla de resultados |

**Recomendación:** usar **(a)** como norma y reservar **(b)** para **un solo equipo piloto**, como demostración en clase. El instrumento real se diseña en Word o en un formulario externo. **Decirlo explícito en la sesión**, para que nadie lo busque dentro de ExamLab.

**Lo que sí queda para la S09:** el guardrail "propuesto / no aplicado" (encuesta `cerrada` obligatoria); el agendamiento de tutorías (§ abajo); el material de la sesión; el Tutor IA; y la Alerta temprana como lista de a quién buscar esa semana.

**Además, en esta sesión y la siguiente — agendamiento de tutorías.** La regla institucional es *"no hay atención espontánea sin cita"* (repetida en `ACA 1:47` y `ACA 3:41`). La herramienta es la **encuesta `slot`**: el docente publica fechas + una ventana horaria + paso + cupo, y el sistema genera los cupos; la reserva es **atómica** (dos personas no se pisan) y el docente puede **mover** a alguien de cupo o **asignar automáticamente** a quien no reservó. Tres límites que hay que aceptar: la hora vive en el **texto del cupo** (el evento de calendario que se genera queda anclado al cierre de la encuesta, igual para todos); **al publicar la encuesta NO se manda correo** (solo campana in-app) ⇒ acompañarla de un mensaje de difusión; y no hay export.

---

### Sesión 10 · 26/10 — Planeación, viabilidad e integración del anteproyecto

**Tema.** Cronograma realista con fases hasta Proyecto II; recursos; riesgos; **viabilidad ≠ optimismo**; la **ACA FINAL** exige el documento **completo**, no un fragmento nuevo; cadena de coherencia final.

**Actividad.** Taller de 20 min: **matriz de coherencia** — filas = secciones del anteproyecto; columnas = ¿existe? ¿alineado? ¿falta? — **+ lista de gaps con dueño**. Criterio: *"gaps priorizados con responsable"*.

**Herramienta.**

| Pieza | Herramienta | Nota |
|---|---|---|
| Matriz de coherencia por secciones | **Encuesta `mixed`**: una `cerrada` por sección con 3 valores (existe / alineado / falta) + una `abierta` "gaps priorizados con responsable" | Convierte la matriz en algo escaneable para los 14 equipos. Es la mejor aproximación disponible; **la matriz como grilla no existe** |
| Lista de pendientes con dueño, que sobreviva entre sesiones | **No existe** módulo de tareas | Vive dentro de la respuesta abierta. El campo de nota por (alumno, sesión) existe en la base pero **no tiene casilla en la interfaz** |
| Ver quién viene en blanco **antes** de la sesión | **Alerta temprana** (semáforo por estudiante, con el motivo escrito) | ⚠️ Requiere que los ACA existan como items `is_external` con `due_date` — si no, el semáforo **nunca pasa de ámbar** y no dice nada (§5.4) |
| Cadena de coherencia como diagrama | **Pizarra de sesión** | Hoy el guion la dicta hablada |
| Cronograma / presupuesto | **Fuera de ExamLab** (Drive) | No hay planificador de hitos. No inflarlo |

---

### Sesión 11 · 09/11 — Integración y evaluación · coevaluación y autoevaluación

**Tema.** Lectura de cierre (*"¿el documento cuenta una sola historia?"*); checklist de integración; coevaluación **formativa** entre pares con rúbrica breve de 4 criterios; puente a Proyecto II. **Es la última sesión sincrónica** — después no hay más encuentros hasta el 22/11.

**Actividad.** Taller de 20 min: **intercambian 1 sección con otro equipo** → **3 comentarios accionables** → ajustes. Entregable: *"lista de verificación firmada por el equipo + ajustes"*. Fuera de sesión: **coevaluación (09–15/11, foro)** y **autoevaluación (16–22/11, cuestionario)**, individuales, en CDigital — fechas oficiales de Coordinación.

**Herramienta.**

| Pieza | Herramienta | Nota |
|---|---|---|
| Lecturas cruzadas entre equipos | **Foro** "Lecturas cruzadas": un hilo por equipo con su sección; el equipo asignado responde con los 3 comentarios | Es lo que la estrategia didáctica del syllabus exige (*"la revisión entre pares"*) y hoy **no tiene ningún soporte**. Queda evidencia de que ocurrió. ⚠️ **El foro no admite adjuntos**: se pega el texto o se enlaza a Drive |
| Checklist de integración "firmada por el equipo" | **Encuesta `mixed`** con las 8 casillas como `cerrada` sí/no | Lo único consolidable. El `.md` de referencia acompaña, pero no se marca |
| Repaso de cierre sobre la checklist | **Banco de preguntas** → taller peso 0 (o Reto en vivo) | Convierte 12 min de monólogo en diagnóstico |
| Coevaluación y autoevaluación como **instrumento** | **No existe en ExamLab** — se diligencian en CDigital | Ya resuelto en el plan de entregas §3.2 y §3.3. Lo que ExamLab aporta acá es el **mensaje programado** con la apertura de cada ventana |
| Acompañamiento del último tramo (10 → 22/11, sin sincrónico) | **Foro con `closes_at = 22/11`** | Es el **único** canal de acompañamiento de esas dos semanas |
| Registro de lo que queda para Proyecto II | **Contenido `.md`** o un hilo fijado del foro | Artefacto de traspaso, no de nota |

---

### Las sesiones que NO existen: 4 lunes festivos

`17/08` · `12/10` · `02/11` · `16/11`. El instructivo **exige** clase pregrabada en lunes festivo, y los dos festivos de octubre/noviembre caen dentro del tramo de la **ACA FINAL**, que vale 42%.

**Herramienta: sesión `autonoma`.** Es el mecanismo más completo de todo el producto para este caso y no requiere nada especial:

1. Se crea la sesión en la fecha del festivo, marcada como autónoma, con el **material asignado** y la **grabación** en su enlace.
2. Al llegar la fecha/hora, un proceso automático **notifica a cada matriculado por campana, notificación push y CORREO**.
3. El estudiante pulsa **"material revisado"** y queda una fila de asistencia.

Dos límites a conocer: es **autodeclarado** (un click marca presente sin abrir un archivo — sirve como compromiso, no como evidencia, y **no debe alimentar nota**); y el botón vive en la vista de Asistencia, **no en el tablero del curso**, así que hay que decirle al alumno dónde está.

---

## 4. Herramientas que sirven YA, sin desarrollo

| # | Herramienta | Cómo se usa en ESP329 |
|---|---|---|
| 1 | **Contenidos + asignación por sesión** | Un paquete por sesión (o uno del curso repartido con subconjuntos de archivos). Las 11 presentaciones + plantilla APA + los 5 enunciados. Convertir a **PDF** lo que se quiera leer inline. Un archivo cuyo nombre empiece por `GUIA_DOCENTE_` o `SOLUCION_` queda **invisible al estudiante** por dos capas — útil, y a la vez una trampa: *"Guía docente de citación"* desaparecería sin aviso |
| 2 | **Sesión `autonoma`** | Los 4 festivos + las semanas de la **ACA FINAL**. Notificación automática por correo + registro de asistencia autodeclarado |
| 3 | **Generador de sesiones con festivos de Colombia** | Las 11 sesiones en una pasada, con los 4 festivos marcados por nombre y política omitir / mover / dejar-como-autónoma. Hace visible el choque de la **ACA FINAL** el día 1 |
| 4 | **`recording_url` + sync automático de Google Calendar** | Cada 6 h rellena el enlace de grabación de la sesión desde el evento de Google. El docente lo copia al formulario AFI de 24 h desde la fila; el alumno lo encuentra colgado de su sesión meses después. ⚠️ Solo Google trae grabación |
| 5 | **Calendario `.ics` del estudiante** | Suscripción única: las 11 sesiones + las ventanas de los ACA aparecen en el calendario del teléfono. Es la mitigación práctica de la discrepancia de fechas |
| 6 | **Tutor IA con override de prompt por curso** | Sube los guiones y los ACA; escribe en el override las fronteras del curso (verbos vetados, antecedente ≠ marco teórico, título ≤21 palabras, las 2 líneas oficiales, "los instrumentos se proponen"). El estudiante escribe `#` para referenciar un archivo concreto y garantizar que entra al contexto |
| 7 | **Pizarra de sesión (Excalidraw) + modo compartido** | La necesidad nombrada por el propio guion (S05). También S02, S06, S08, S10. Puntero láser, viewport persistente, pegado de imágenes |
| 8 | **Foro con ventana `opens_at`/`closes_at`** | El caballo de batalla asíncrono: publicar la pregunta del equipo, lecturas cruzadas, matriz de antecedentes por enlace, el párrafo antes de la tutoría, el tramo sin sincrónico hasta el 22/11. Respuesta **oficial** + hilo **fijado** para dejar el material de referencia |
| 9 | **Encuestas `single` en vivo** | Chequeo de comprensión con histograma en tiempo real (S02, S08, S11) |
| 10 | **Encuesta `slot` (Doodle)** | Agendamiento de tutorías con cupo y reserva atómica; mover a un alumno de franja; asignar automáticamente a los que no reservaron |
| 11 | **Check-in por QR, variante pública sin login** | Reemplaza el formulario externo de asistencia a tutoría, y el dato queda **dentro del curso** alimentando el % y la Alerta temprana |
| 12 | **Banco de preguntas del curso** | La clínica APA y el repaso de cierre, reutilizables entre cohortes e importables a otros formatos |
| 13 | **`max_attempts` por taller (1 → 10)** | Iteración **self-service**: el siguiente intento se habilita cuando el anterior fue calificado. Es la diferencia entre iterar y hacer 70 reaperturas manuales |
| 14 | **Mensajes programados** | Los avisos de las 5 ventanas se cargan de una sentada en agosto; el envío revalida permisos en el momento |
| 15 | **`/app/teacher/students` → "Ver como"** | El docente entra como uno de sus 40 y verifica qué material ve, qué sesiones ve y cómo le responde el tutor con su override. **Corrige un supuesto extendido**: no hace falta una segunda cuenta. Ahí mismo puede **resetear contraseñas** de sus estudiantes sin pasar por el Admin |
| 16 | **Tours guiados de Docente y Estudiante** | Onboarding ya construido (~24 y ~15 pasos). ⚠️ **No se disparan bajo 768 px** |
| 17 | **⌘K (buscador)** | Mitigación del sidebar largo mientras no se apaguen módulos |
| 18 | **Registro de acciones (`/app/teacher/audit-logs`)** | Único rastro consultable de lo que se hizo (difusiones, reaperturas) |

---

## 5. Lo que requiere workaround (y qué se paga)

### 5.1 Retro del ACA con el `.docx` anotado → mensaje 1-a-1 con adjunto

**Cómo.** La nota y la observación cualitativa van en el editor de notas externas. El **`.docx` anotado** se manda como adjunto por Mensajes (25 MB, hasta 8 archivos, sin filtro de tipo).
**Qué se gana.** Un registro escrito, **inmutable una vez leído**, de las 2–3 observaciones accionables — hoy eso se dice en voz alta en la tutoría y se pierde.
**Qué se paga.** **No hay chat de equipo.** La infraestructura está en la base de datos pero **no tiene interfaz**: el diálogo "Nueva conversación" abre 1-a-1 y no hay forma de crear un grupo. Con 14 equipos son **~40 mensajes** por ronda de retro (uno por estudiante), o 14 si se le manda solo al vocero.
**Alternativa descartada.** El hilo de retroalimentación por sección es más rico (ida y vuelta, adjuntos de ambos lados, estado abierto/cerrado), **pero no existe hasta que el estudiante pulsa Entregar** — no hay fila de borrador. Como el ACA se entrega en CDigital, ese hilo solo aparece si el equipo usa el taller formativo de peso 0. Ahí sí conviene usarlo.

### 5.2 Fichas y matrices estructuradas → encuesta `mixed`

**Cómo.** Cada ficha del curso (encuadre S01, tabla de términos S06, matriz metodológica S08, matriz de coherencia S10, checklist S11) se modela como una encuesta multi-pregunta: `cerrada` donde el valor es una lista finita, `abierta` donde es redacción.
**Qué se gana.** Lo que un documento adjunto no da: **leer una columna de los 14 equipos de un golpe**. Ese es el criterio de evaluación real en S06 y S08.
**Qué se paga.** Cuatro cosas: solo hay 2 tipos de pregunta (**no hay multi-selección, no hay escala/Likert, no hay campos condicionales**, así que el "formulario donde la respuesta anterior condiciona la siguiente" no se puede armar); **las preguntas se vuelven inmutables** apenas llega la primera respuesta; **no hay export en ningún formato** (analizar fuera = transcribir a mano); y **las respuestas abiertas solo las ven el docente y el propio autor**, por lo que una `mixed` **nunca es un muro colaborativo**.

### 5.3 Auto-chequeo con criterios reales → taller peso 0 con `abierta` + rúbrica

**Cómo.** Un taller sin peso ("Chequeo de coherencia") con 3–4 preguntas `abierta` y, en cada `expected_rubric`, los criterios reales del enunciado ACA más las reglas del guion. El estudiante lo envía y recibe observaciones en ~10 s; corrige; **después** entrega en CDigital.
**Qué se gana.** Que los 6 criterios —que hoy viven en un `.docx` de enunciado que se lee una vez— aparezcan **donde se redacta**.
**Qué se paga.** **El estudiante pega texto**: la calificación IA no lee `.docx` ni `.pdf`. Para un curso cuyo producto es un documento en Word, eso define el diseño: **fragmentos cortos** (pregunta + objetivos, ~15 líneas), nunca "pegá tu anteproyecto". Y hay un detalle incómodo: el markdown de la respuesta **no se renderiza ni siquiera para su propio autor** — se ve en tipografía monoespaciada. Nada de pedir tablas ahí.
**Además:** subir `max_attempts` a 4 en ese taller, o el alumno entrega una vez y queda bloqueado.

### 5.4 Alerta temprana → encender el semáforo con los ACA como items externos

**Cómo.** Crear los **5 ítems del aula** como actividades externas con su `due_date`: **Quiz** (ESP329: ACA 1) · **ACA 1** (ESP329: ACA 2) · **ACA FINAL** (ESP329: ACA 3) · **Coevaluación** (foro) · **Autoevaluación**.
**Qué se gana.** Tres cosas de golpe: el semáforo deja de estar ciego y lista a quién buscar esta semana con el motivo escrito; los recordatorios automáticos de ventana se activan; y las ventanas aparecen en el `.ics` del estudiante.
**Qué se paga y hay que hacerlo bien.** El semáforo deriva las actividades **de las entregas existentes**: sin items, solo puede encenderse la inasistencia y —como hace falta cruzar **dos** motivos para el rojo— **nunca pasa de ámbar**. Y el motor es **por estudiante, no por equipo**: con un solo envío grupal, los otros 2 integrantes figuran como "no entregó". ⚠️ **Crear esos items con peso 0** si solo se usan para seguimiento: un item con peso y sin nota **cuenta como 0 con su peso completo** y hunde el consolidado.

### 5.5 Anotar sobre las diapositivas → exportar las slides a imagen

**Cómo.** La función "Presentar y anotar" proyecta las diapositivas y deja rayarlas encima con Excalidraw, persistiendo la anotación por diapositiva.
**Qué se paga.** **Solo funciona con presentaciones generadas por la IA del módulo o con imágenes.** Un `.pptx` **subido** y un **PDF** no producen diapositivas anotables: hay que **exportar cada slide a PNG** y subir las imágenes. Y hay un límite mayor: **el estudiante no ve las anotaciones en ninguna pantalla** — la base lo permite, la interfaz no lo pide. Lo modelado se conserva **para el docente**, no se le entrega al alumno.
**Recomendación:** para las 11 sesiones, usar la **pizarra de sesión** (que sí ve el alumno si se comparte) y dejar "Presentar y anotar" como recurso del docente.

### 5.6 Señal de consumo del material → sesión autónoma, no el registro real

**Cómo.** La base **sí** registra qué archivo abrió o descargó cada alumno, y la seguridad ya se lo permite leer al docente del curso. Pero **no hay pantalla**: hoy solo se consulta por consulta directa a la base.
**Sustituto usable:** la sesión autónoma con su "material revisado" (autodeclarado). Es un compromiso registrado, no evidencia de lectura.

---

## 6. Brechas reales de herramienta (lo que NO existe)

Sin maquillaje. Ninguna de estas tiene configuración que la resuelva.

| # | Brecha | Impacto en ESP329 | Lo más cercano, y por qué no alcanza |
|---|---|---|---|
| **G1** | **El estudiante no puede diseñar un instrumento** | **Bloquea la actividad central de la S09** | El constructor existe y es bueno, pero tres candados independientes lo reservan al docente. Fallback: foro (texto) o transcripción por el docente, que no escala a 14 equipos y **no le devuelve los datos al diseñador** |
| **G2** | **Gestor de referencias bibliográficas** | El curso exige **mínimo 6 antecedentes** con ficha y vínculo a la pregunta, acumulados durante 3 meses | **No existe nada**: sin entidad "fuente", sin CRUD, sin generación de cita, sin integración con Scholar/SciELO/Redalyc/DOI. La "libreta" natural sería la conversación del Tutor IA, pero es **una sola por curso, sin título**, cada apunte cuesta una llamada al modelo, y el único botón de gestión **la borra entera** |
| **G3** | **Verificación de citación APA 7** | Es media sesión (S07) y criterio de los tres ACA | **No existe**, y el Tutor IA **no verifica**: es chat sin herramientas ni acceso a la web, así que reformatea *de memoria*. Para APA 7 eso es exactamente el error a evitar: una referencia bien formateada e inexistente |
| **G4** | **Registro de correcciones con estado** (pendiente → atendido) | Es criterio **calificable dos veces** (`ACA 2:18`, `ACA 3:18`) y habilita el ajuste favorable retroactivo de `Manual:189` | La observación y el mensaje son **texto sin ciclo de vida**. Nada permite marcar "atendido" ni ver el diff. Además **no hay historial de versiones en ningún flujo**: "nueva versión" = reemplazar |
| **G5** | **Canal por equipo** y bitácora del *"acuerdo observable"* | Los 11 guiones cierran la tutoría con *"un acuerdo observable para la próxima"* — y hoy vive en la memoria del docente | El chat de grupo **está en la base de datos y no tiene interfaz**. El campo de nota por (alumno, sesión) existe y **no tiene casilla**: solo entra por importación CSV. Sustituto: un foro por equipo, o N conversaciones 1-a-1 |
| **G6** | **Tabla / matriz como tipo de dato** | S04 (antecedentes), S06 (términos), S09 (alineación), S10 (coherencia) | Los 12 tipos de pregunta son texto, código, consola, GUI, SQL y diagrama. La tabla markdown **solo se renderiza en el foro** — ni en la vista del docente ni en la del propio alumno |
| **G7** | **Checklist marcable** | Entregable literal de la S11 (*"lista de verificación firmada por el equipo"*) | El markdown publicado no admite casillas. Workaround: encuesta con `cerrada` sí/no |
| **G8** | **Coevaluación y autoevaluación como instrumento** | 8% de la nota | Ya documentado en el plan de entregas (§3.2, §3.3). No hay ninguna tabla donde un estudiante califique a otro, y la seguridad lo impide por diseño |
| **G9** | **Vista docente del consumo de material** | Aula invertida sin señal (`Manual:50`) | El dato **se está grabando** y la seguridad ya lo permite: falta la pantalla. Es "falta la interfaz", no "falta el modelo de datos" |
| **G10** | **Panel de avance por EQUIPO** | Todo el curso es por equipos de ≤3 | Todo el seguimiento (semáforo, informes, editor de notas externas) es **por estudiante**. No hay variable de equipo en las plantillas de informe |

---

## 7. Riesgos

Incluye el perfil: **posgrado virtual, 40 adultos que trabajan, clase de lunes 8–10 pm**.

| # | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| **R1** | **Adopción de una segunda plataforma sin efecto en la nota.** Todo depende de que 40 adultos entren voluntariamente a un sitio que no califica | **Alto** | Definir **qué se hace SOLO en ExamLab** para que entrar no sea opcional: la grabación de la sesión, el material, el foro de lecturas cruzadas y la reserva de tutoría. Si en la semana 3 la tasa de entrada es baja, **retirar los talleres formativos** (son opcionales y salen sin costo) y quedarse con material + grabación + tutorías |
| **R2** | **El docente NO puede crear las cuentas.** La importación de usuarios es Admin/SuperAdmin | **Alto** (bloquea la S01) | **Paso 0 con owner y fecha**: el Admin importa las 40 identidades desde CSV **antes** del 10/08. El docente sí puede **matricular** usuarios existentes y **resetear contraseñas** desde `/app/teacher/students` |
| **R3** | **Primer login con contraseña temporal + diálogo de cambio bloqueante**, y el tour **no se dispara en celular** | **Alto en la S01** | No hacer nada crítico el primer día. Mandar credenciales por correo la semana previa, y en la S01 solo mostrar dónde está el material. Advertir que el recorrido guiado **requiere computador** |
| **R4** | **Mobile.** Pizarra, matrices y el juego en vivo son inviables en celular; el Reto en vivo además compite con Meet por la pantalla | Medio | Declarar en la S01 **qué es "de computador"** (pizarra, talleres, matrices) y **qué sirve en celular** (leer material, marcar sesión autónoma, check-in, foro, encuestas, tutor) |
| **R5** | **La IA está en modo diferido por defecto**: cada acción se encola y la drena un proceso **cada hora**. Si el docente prepara la clínica APA 20 minutos antes de clase, las preguntas **no existen** cuando entra al aula | **Alto** | Decidir con el Admin **antes** de arrancar: modo inmediato para esta institución, o un código de IA inmediata a la mano. **El Tutor IA es la excepción**: siempre responde en vivo |
| **R6** | **Seis ajustes que el docente necesita y solo puede tocar el Admin — y son por INSTITUCIÓN, no por curso**: modo de la IA, intentos por defecto, antelación de recordatorios, umbrales del semáforo, tipos de correo activos, módulos visibles | Medio-alto | Tabla explícita "ajuste → quién lo hace → a quién más afecta" antes de configurar. Si el tenant es compartido con otros docentes, **no** apagar módulos ni mover umbrales |
| **R7** | **La aritmética de la tutoría no cierra.** 14 equipos × 8–12 min = **2–3 h/semana** contra las ~5 h declaradas (`Manual:54`) y, con adultos que trabajan, **todos van a querer las mismas franjas nocturnas**: con cupo 1 y ventana diurna se llenan 3 cupos y quedan 11 equipos sin cita | **Alto** | Publicar franjas **fuera del horario laboral**, aceptar **tutoría quincenal por equipo** y usar la asignación automática de los que no reservaron. La 2.ª hora del encuentro sigue siendo el canal principal |
| **R8** | **Correo.** Media docena de piezas dependen de él: los tipos de correo se pueden apagar por institución; el recordatorio de vencimiento tiene **deduplicación permanente** (mover una fecha **no** genera segundo aviso); **la publicación de una encuesta NO manda correo**; y hay antecedente de rebotes por buzón lleno | Medio | Prueba de correo a 3 direcciones institucionales antes de la semana 1. Tratar la **campana in-app** como canal de respaldo. Acompañar cada encuesta de tutoría con un mensaje de difusión |
| **R9** | **El material asignado a una sesión solo notifica si CAMBIA el paquete.** Si se van agregando archivos a un paquete ya asignado, **nadie se entera** | Medio | En un curso de aula invertida donde el material crece semana a semana, es el fallo silencioso más probable. Acompañar cada publicación con un mensaje, o asignar un paquete por sesión |
| **R10** | **Datos personales, en un curso que enseña protección de datos y uso declarado de IA** | Medio | Tres reglas: (a) **no subir grabaciones de tutoría** a la biblioteca de videos — ese almacenamiento es de lectura abierta por URL, no control de acceso: dejar el enlace de Meet/Drive con permisos; (b) el Tutor IA envía el material y el texto del alumno a un proveedor externo **y el docente puede leer las conversaciones**: decirlo en la S01 en una línea; (c) encuadre de qué se guarda, dónde y quién lo ve |
| **R11** | **Los guiones docentes son visibles al estudiante si se suben tal cual.** El filtro de "solo docente" es **por nombre de archivo**, y `Sesion 01 - ….md` **no lo activa**: el tutor le citaría al alumno los errores frecuentes y las respuestas modeladas | Medio | Renombrar a `GUIA_DOCENTE_Sesion01.md` antes de subir. Verificar con "Ver como" (§4.15) que el alumno no los ve |
| **R12** | **Salida al cierre.** Un curso marcado como finalizado **oculta su material al estudiante por defecto**; lo eliminado se **purga a los 30 días**; y **no hay "descargar todo"** en Contenidos | Medio | Definir quién exporta qué y cuándo, y **qué se le promete al estudiante** sobre el acceso post-cierre. Combina con el punto ya escrito en el plan de entregas: ExamLab es el archivo permanente **si** se conserva abierto |
| **R13** | **El Tutor IA con 40 estudiantes consume cuota real** (es síncrono, sin cola ni tope) | Medio | Verificar con el Admin que la institución tenga la lista de claves de respaldo cargada. El cupo de material del tutor es limitado: enseñar a usar `#` para referenciar un archivo no es cosmético |
| **R14** | **El sidebar tiene ~22 ítems planos**, la mayoría irrelevantes acá (Exámenes, Certificados, Cola de IA, Papelera) | Bajo-medio | Apagarlos es **por institución y rol, y lo hace el Admin**: solo vale si el tenant es dedicado. Si no, mitigar con **⌘K** y con el tour |

> Los riesgos ya escritos en el plan de entregas (doble fuente de verdad de notas, items sin nota que cuentan 0, la similitud confundida con Turnitin, la doble digitación) **no se repiten acá**. Siguen vigentes.

---

## 8. Decisión recomendada y siguientes pasos

### Decisión

1. **Adoptar ExamLab como capa de HERRAMIENTAS del curso**, con este alcance y no más: material por sesión, sesiones autónomas para los festivos, grabaciones ancladas, calendario, Tutor IA, pizarra, foro, encuestas y agendamiento de tutorías.
2. **La S09 se declara sin herramienta** para su actividad central. El instrumento se bosqueja en el foro y se diseña fuera. **Decirlo en clase**, no dejar que lo busquen.
3. **Padlet se queda en la S01.** ExamLab arranca de verdad en la S02, cuando los 40 ya tienen credenciales funcionando.
4. **La clínica APA se hace como taller asíncrono autocalificado**, no como juego en vivo. El Reto en vivo queda disponible si el docente lo quiere.
5. **Nada que exija pegar el anteproyecto completo dentro de ExamLab.** Los talleres formativos se acotan a fragmentos de ~15 líneas.
6. **Ningún artefacto del curso se teclea como tabla markdown.** Las matrices viven en Drive; al foro va el enlace y el análisis en prosa.
7. **Los talleres formativos con IA son opcionales** y se retiran sin costo si la adopción de la semana 3 es baja.
8. **No** presentar el Tutor IA como verificador de citas. Es un asistente de criterio, no de existencia de fuentes (G3).

### Checklist priorizado

**Bloque 0 — Antes del 10/08 (bloqueante; requiere al Admin de la institución)**

- [ ] Docente aprueba este documento (alcance + la S09 declarada sin herramienta).
- [ ] **Admin:** importar las 40 cuentas desde CSV y matricularlas al curso *(el docente no puede hacerlo)*.
- [ ] **Admin:** poner la IA en **modo inmediato** para esta institución, o entregar códigos de IA inmediata *(sin esto, R5 muerde en la primera clase)*.
- [ ] **Admin:** subir el default de intentos de taller de **1 a 4** *(o el docente lo ajusta ítem por ítem)*.
- [ ] **Admin:** verificar que los tipos de correo relevantes están activos (inicio de sesión autónoma, bienvenida al curso, vencimientos) y hacer una prueba a 3 direcciones `@cun.edu.co`.
- [ ] Decidir si el curso va en un tenant dedicado (habilita apagar módulos y ajustar umbrales sin afectar a otros docentes).

**Bloque 1 — Armado del curso (docente, semana previa)**

- [ ] Generar las **11 sesiones** con el generador + política de festivos; marcar `17/08`, `12/10`, `02/11` y `16/11` como **autónomas**.
- [ ] Conectar **Google Calendar** para que Meet, la invitación a los 40 y el enlace de grabación se sincronicen solos.
- [ ] Subir el material: 11 presentaciones + plantilla APA + los 5 enunciados. **Convertir a PDF** lo que deba leerse inline. **Renombrar** los guiones a `GUIA_DOCENTE_*` antes de subir (R11).
- [ ] Asignar el material a cada sesión (y el general del curso, aparte).
- [ ] Escribir el **override del prompt del Tutor IA** para este curso: verbos vetados, antecedente ≠ marco teórico, título ≤21 palabras, las 2 líneas oficiales, "los instrumentos se proponen, no se aplican".
- [ ] **Verificar con "Ver como"** un estudiante: qué material ve, qué NO ve, y que el tutor responde citando la plantilla APA. *(Si responde solo con el título, el material no se indexó o el curso ancla es otro.)*
- [ ] Crear los ACA como items **externos con `due_date` y peso 0** — enciende el semáforo, los recordatorios y el `.ics` (§5.4).
- [ ] Programar los **5 avisos de ventana** de una sola vez.
- [ ] Publicar el **`.md` de referencia**: verbos aceptados/vetados, pares débil/fuerte, checklist de cierre referencial, enlaces de bases académicas.

**Bloque 2 — Durante el curso**

- [ ] S01: matricular → check-in QR → decir en una línea qué se guarda y quién lo ve (R10) → **Padlet** para el rompehielos.
- [ ] S02: crear el foro "Nuestra pregunta" (un hilo por equipo) + la encuesta de 3 ítems.
- [ ] S03: taller formativo peso 0 con los 6 criterios en la rúbrica y `max_attempts = 4`.
- [ ] S04: registrar el **Quiz** (nota + observación) y mandar el `.docx` anotado por mensaje con adjunto.
- [ ] S05: activar **"Pizarra compartida"** en la sesión y asignar una zona del lienzo por equipo.
- [ ] S07: armar el **banco de 8–10 ítems** de citación → servirlo como taller autocalificado.
- [ ] S09–S10: publicar la encuesta `slot` de tutorías **con franjas nocturnas** y acompañarla de un mensaje de difusión *(la encuesta sola no manda correo, R8)*.
- [ ] S11: foro "Lecturas cruzadas" + checklist como encuesta + foro de acompañamiento con cierre el 22/11.

**Bloque 3 — Cierre**

- [ ] Antes del 22/11: descargar el material y las evidencias *(no hay "descargar todo": es archivo por archivo, R12)*.
- [ ] Decidir qué pasa con el curso después del cierre y **qué se le promete al estudiante** sobre el acceso.
- [ ] Evaluar para el próximo periodo, en este orden de costo/beneficio: **(1)** pantalla docente del consumo de material *(el dato ya existe)*; **(2)** casilla de nota por sesión para la bitácora del acuerdo; **(3)** interfaz del chat de equipo *(la base ya está)*; **(4)** hora real por franja de tutoría.

---

## 9. Fuentes

### Material del curso *(verificado en disco)*

| Recurso | Ruta |
|---|---|
| Documento hermano (eje entregas) | `Especializacion/Proyecto I/PLAN_VIABILIDAD_EXAMLAB.md` |
| Manual del Docente | `Especializacion/Proyecto I/Manual del Docente - PROYECTO I.md` |
| Calendario oficial | `Especializacion/Proyecto I/Calendario de clases (oficial).md` |
| Guiones de las 11 sesiones *(donde vive la actividad real)* | `Proyecto I/Guiones/Sesion 01..11 - ….md` |
| Enunciados ACA (5) | `Proyecto I/Clases/Recursos/ACAs/ACA {1,2,3}….docx` · `ACA {Auto,Co}evaluacion.docx` |
| Presentaciones de sesión *(plantilla: sin actividades, slides 4-5-6 idénticas)* | `Proyecto I/Clases/Sesion NN - …/Presentacion.pptx` |
| Syllabus ESP329 (7 unidades + estrategia didáctica) | `Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx` |
| Rúbricas detalladas — **no leídas** | `Instructivo_Docentes_Proyecto_I_II_Especializaciones_Rubricas_Unificado.pdf` (Anexo 2, externo) |
| Plan de referencia de formato | `UNIAJ/…/Plan curso/2026-2/PLAN_VIABILIDAD_FLOCI_2026-2.md` |

### Verificación de capacidades de ExamLab

Todas las afirmaciones sobre lo que ExamLab hace, no hace o hace a medias fueron verificadas contra el código del producto en `C:/Projects/Personal/examlab` (rutas de la aplicación, migraciones de base de datos y funciones de servidor), no contra su documentación. Los inventarios de origen cubrieron cuatro familias —material y contenido, inteligencia artificial, colaboración y clase en vivo, seguimiento y gestión— más dos barridos de brechas, y pasaron por una verificación adversarial que corrigió ocho afirmaciones. Las correcciones que sobreviven y que este documento incorpora:

| Corrección aplicada | Consecuencia acá |
|---|---|
| El **chat de grupo no tiene interfaz** (existe solo en la base de datos) | La retro por equipo son N mensajes 1-a-1 (§5.1, G5) |
| **Publicar una encuesta NO manda correo** (solo campana) | El agendamiento de tutorías necesita un mensaje de difusión (R8) |
| El Tutor IA tiene **una sola conversación por curso**, sin título, y el único botón la borra entera | No sirve como libreta de fuentes (G2) |
| El estudiante **no crea foros** y su hilo exige el foro **abierto**… pero **editar su propio hilo no** | El foro depende de que el docente lo cree; una vez creado, el hilo se itera aunque cierre |
| Los talleres tienen **`max_attempts` propio con interfaz** (default 1, hasta 10) | Iteración self-service en vez de 70 reaperturas manuales (§4.13) |
| El markdown de la respuesta **no se renderiza ni para su autor** | Nada de tablas en talleres; la tabla solo vive en el foro (§5.3, G6) |
| Las respuestas abiertas de una encuesta **solo las ve el docente y el autor**; sin export | La `mixed` no es muro y no da dataset (§5.2, S09) |
| `/app/teacher/students` permite **"Ver como"** y resetear contraseñas | El docente **sí** puede probar su propio override sin una segunda cuenta (§4.15) |

---

*Documento interno Plan de curso · alcance: 26ES4 / 54ES4 · eje HERRAMIENTAS · complementa `PLAN_VIABILIDAD_EXAMLAB.md`, no lo sustituye. No distribuir a estudiantes. Las entregas oficiales de PROYECTO I se realizan exclusivamente en CDigital.*
