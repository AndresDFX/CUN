# Herramientas de ExamLab — TRABAJO DE GRADO 2 (94453 · 54448 · 26V04)

| Campo | Valor |
|---|---|
| Curso | Trabajo de Grado 2 — Modelos de Innovación (Ing. Sistemas) · **94453** |
| Programa / unidad | Ingeniería de Sistemas · **OPCGV — Opciones de Grado Virtual** |
| Grupo / periodo | **54448** / **26V04** · BLOQUE ÚNICO |
| Docente | Julian Andres Castaño · `julian_castanoe@cun.edu.co` |
| Modalidad / horario | Virtual (Google Meet) · **lunes 5:00–6:00 pm** (1 hora sincrónica) |
| Estudiantes | **50 / 50** (cupo lleno) — cada uno con **un proyecto individual distinto** |
| Encuentros | **15** = 11 sincrónicas + **4 autónomas** (17/08, 12/10, 02/11, 16/11) |
| Fechas clave | Inicio 10/08/2026 · recepción máx. 14/11/2026 · cierre **22/11/2026** |
| Plataforma oficial CUN | **CDigital (Moodle)** — no negociable |
| Herramienta evaluada | **ExamLab** (`examlab.lovable.app`) |
| Evaluación | Art. 52 — **tres cortes 30 / 30 / 40** · Corte 1 = Quiz 1 6% + **Parcial 1 24%** · Corte 2 = Quiz 2 9% + **Parcial 2 21%** · Corte 3 = **ACA Final 32,8%** + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6% (**foro**) |
| Fecha | 2026-08-08 · **revisado 2026-08-10** contra el aula |
| Estado | **Borrador para aprobación docente** |

> ## ⚠️ Corrección del 2026-08-10 — los pesos ya no están «sin confirmar»
>
> Este análisis se escribió el 08/08 cuando la evaluación de TG2 era una reconstrucción por analogía con TG3, a la espera del Syllabus SIAC. El **10/08 se auditó el libro de calificaciones del aula** (`AUDITORIA CDigital 2026-08-10.md` §2): **la estructura está ahí, completa**. Donde el cuerpo diga lo contrario, manda este recuadro:
>
> | Lo que decía este documento | Lo que hay en el aula |
> |---|---|
> | «Pesos 30/30/40 **sin confirmar** — **bloqueante**, no crear cortes hasta tener el SIAC (R4)» | **Confirmados y desglosados.** Ya no hay bloqueo: el SIAC solo falta para el **temario** |
> | «Tres ACAs, una por corte, entregadas el 07/09 · 05/10 · 09/11» | **8 ítems.** Quiz 1 6% → **31/08** (S03) · **Parcial 1 24%** → **14/09** (S05) · Quiz 2 9% → **28/09** (S07) · **Parcial 2 21%** → **05/10** (S08) · Quiz 3 4% → **26/10** (S10) · **ACA Final 32,8%** (tarea) → **14/11** (recepción) · Autoevaluación 1,6% y Coevaluación 1,6% → 09–22/11 |
> | «Autoevaluación y coevaluación **con peso propio no aplican** aquí» | **Sí aplican** (1,6% cada una). La **coevaluación es un FORO de CDigital**: la nota se cumple allá, y lo que falta en ExamLab es solo la capa formativa |
>
> **Lo que esto cambia:**
> - **R4 deja de ser bloqueante.** Los cortes se pueden crear hoy, con los 8 ítems reales.
> - **Aparece la tarea más urgente del curso, que este documento no contemplaba:** redactar **Quiz 1–3 y Parcial 1–2** (64% de la nota). En el aula existen como ítem del libro de calificaciones **sin actividad ni preguntas**; el primero cierra el **31/08**. El **Banco de preguntas** de ExamLab es el insumo natural — la nota oficial sigue siendo la del cuestionario de CDigital.
> - **R3 se atenúa:** con cinco cuestionarios entre agosto y octubre, el estudiante ya no queda «reprobado hasta noviembre» a la espera de un único entregable.

---

> ### Alcance de este documento: HERRAMIENTAS, no entregas
>
> Este documento evalúa **con qué trabajan el estudiante y el docente** en la sesión y entre sesiones:
> material por sesión, asistente sobre el material, foro, encuesta en vivo, lienzo de diagramas,
> calendario, seguimiento de avance, banco de preguntas.
>
> **No** analiza dónde se sube el archivo final ni los porcentajes de la nota. **La entrega oficial, la
> aplicación de los cuestionarios y el registro de notas siguen en CDigital, sin excepción** — así lo
> declaran los enunciados ACA, el `LEEME` del estudiante y el Manual del Docente. Nada de lo que sigue
> mueve eso.
>
> Todo lo marcado *(inferido)* es reconstrucción propia, no está en el material del curso.

---

## 1. Resumen ejecutivo

**Veredicto: viable y de alto valor, con alcance acotado — como capa de material y acompañamiento, nunca como segunda entrega.**

Tres hechos, y el primero no es sobre ExamLab:

1. **El curso tiene un hueco documentado de material, no de plataforma de entrega.** Los 11 PPTX que el
   estudiante recibe son **plantilla interpolada**: el slide "ACTIVIDAD / TALLER" dice lo mismo en las 11
   sesiones (*"Aplica el concepto de hoy a tu propio proyecto… Entregable: según indique el Docente"*).
   Las consignas reales —*"4 fichas mínimas + párrafo puente"*, *"matriz de gaps + dueños"*— viven **solo
   en `Guiones/`, que el `LEEME` dice explícitamente que no se comparte**. El estudiante de pregrado que
   faltó, o que no tomó nota en el minuto 32, no tiene de dónde recuperar qué debía producir. Ese hueco
   lo cierra una herramienta de material, no una de evaluación.

2. **El 27% de los encuentros está vacío.** Las 4 clases autónomas (17/08, 12/10, 02/11, 16/11) solo
   dicen *"continuar avance"*: sin guion, sin consigna, sin entregable. ExamLab tiene el contenedor exacto
   —`session_type = 'autonoma'`, que notifica y emaila solo al llegar la fecha y deja al alumno marcar el
   material como revisado— pero **el contenedor no escribe la consigna**. Eso sigue siendo trabajo docente.

3. **Lo que ExamLab aporta aquí es aritmética, no funcionalidad.** 50 estudiantes × 50 proyectos
   distintos × **1 hora semanal**. La sesión 10 pide pitch de 3 min por estudiante: **50 × 3 = 150 minutos
   en una sesión de 60**. Es imposible en vivo. Y el acompañamiento individual de 50 proyectos en 60
   minutos semanales tampoco existe. Las piezas que mueven la aguja son las que convierten trabajo
   sincrónico imposible en asíncrono posible.

**La restricción que define el alcance:** todo lo que el estudiante ya entrega en CDigital **no se
espeja** en ExamLab. Pedirle a 50 estudiantes de pregrado que hagan el taller en ExamLab *y* lo suban a
CDigital es doble trabajo, y en pregrado el resultado de eso no es "lo hacen dos veces": es que lo hacen
mal una vez. ExamLab entra **solo donde no duplica**.

### Necesidad → herramienta → estado

Las 11 necesidades son las declaradas en el análisis del curso, más la de las clases autónomas.

| # | Necesidad del curso | Herramienta de ExamLab | Estado |
|---|---|---|---|
| 1 | Material por sesión **con la consigna adentro** | Contenidos + Tablero + subconjunto de archivos por sesión | **Lista** |
| 2 | Discusión asíncrona anclada a la sesión | Foros con ventana, hilo fijado y **respuesta oficial** | **Lista** |
| 3 | Ver quién se queda, **por sección del documento** | Proyecto con 1 slot por sección + diagnóstico del curso + alerta temprana | **Con workaround** |
| 4 | Lienzo para diagramar, que **quede como evidencia** | Pregunta tipo `diagrama` (mermaid, por estudiante) + pizarra de sesión | **Lista** |
| 5 | Socializar avances + feedback de pares asíncrono | Video de sustentación + foro (1 hilo por estudiante) | **Con workaround** |
| 6 | Pulso rápido del grupo en vivo | Encuesta de opción única/múltiple + Reto en vivo | **Lista** |
| 7 | Asistente sobre el material **y el borrador propio** | Tutor IA por curso (lee `.docx`, `.pptx`, `.pdf`, `.xlsx`) | **Lista** |
| 8 | Demostración asíncrona reutilizable (grabaciones) | Videos + `recording_url` por sesión | **Lista** |
| 9 | Verificación autocorregible de errores recurrentes | Reto en vivo + taller cerrado con reintentos + banco de preguntas | **Lista** |
| 10 | Calendario que el **estudiante** reciba | Sincronía Google/M365 con invitados + `.ics` suscribible del alumno | **Lista** |
| 11 | Saber si abrió el material | Progreso de material ("abriste N de M") + "Seguías en…" | **Lista** |
| 12 | **Las 4 clases autónomas vacías** | `session_type = 'autonoma'` + notificación automática + foro con ventana | **Lista (el contenedor)** |
| — | Gestor de referencias y ayuda de citación APA | — | **No existe** |
| — | Rúbrica como **dato** (criterios × niveles × puntaje) | — | **No existe** |
| — | Revisión por pares con rúbrica y registro *(la **coevaluación con nota** del curso —1,6%— **sí existe**, pero es un **foro de CDigital**)* | — | **No existe en ExamLab** |
| — | Historial de versiones del avance, que se construye acumulativamente S01→S11 | — | **No existe** |
| — | Que el **estudiante** cree una encuesta (sesión 08) | — | **No existe (bloqueado en RLS)** |
| — | Cronómetro proyectable con consigna y criterio a la vista | — | **No existe** |

**Recomendación:** adoptar **siete piezas no duplicativas** (material por sesión, tutor IA, foros, sesión
autónoma, encuesta de pulso, diagrama, calendario) + el registro docente de notas con observación. **No
espejar** los 11 entregables de sesión. El modelado del documento APA como proyecto de N slots (§5.1) es
la pieza de mayor valor pedagógico y la única que pide una decisión de diseño real.

---

## 2. Lo que condiciona todo: 50 estudiantes, 1 hora, 50 proyectos

Esto no es contexto de color; es lo que decide qué herramienta tiene sentido.

| Hecho | Consecuencia directa |
|---|---|
| **1 hora sincrónica semanal** (la mitad de un posgrado típico) | La fase "Taller aplicado" son **20 min**. Lo que no cabe ahí, o es asíncrono o no ocurre |
| **50 estudiantes, 50 proyectos individuales distintos** | No hay "el ejercicio de la clase". Toda ayuda es 1-a-1, y 50 × 1-a-1 no cabe en 60 min |
| **Pregrado, no posgrado** | Menos autonomía: *"no sabía que era hoy"* y *"no encontré la consigna"* son causas reales de no-entrega |
| **4 de 15 encuentros son autónomos y están vacíos** | El 27% del curso depende de que el estudiante se autoorganice sin consigna |
| **Estructura idéntica en las 11 sesiones** (6+14+12+20+8) | La modelación en vivo son 12 min × 11 = **132 minutos** de demo repetible, grabables una vez |
| **Falta el syllabus SIAC oficial** | Falta el **temario**. Los **pesos ya no son un problema**: salen del libro de calificaciones del aula (auditoría 2026-08-10) y se pueden configurar hoy |

Dos cifras que aparecen solas al hacer la cuenta y que el material no resuelve:

- **Sesión 10 no cabe.** 50 pitches de 3 min = 150 min en una sesión de 60. El guion solo prevé
  *"cronómetro en pantalla"*. O se vuelve asíncrona, o alcanza para ~15 estudiantes.
- **550 evidencias de sesión.** 11 entregables × 50 estudiantes, más 3 ACAs, contra 1 hora semanal. Sin
  un tablero que diga a quién buscar, el primer momento en que el docente ve el atraso es la nota del corte.

---

## 3. Mapa sesión por sesión

Los 15 encuentros. Ninguno queda vacío; donde no hay herramienta, lo digo.

**Convención:** *Formativo* = ejercicio en ExamLab con nota **no ponderada** (peso 0), que **no reemplaza**
el archivo que va a CDigital. *Registro* = el docente digita nota + observación, el estudiante no hace nada
en ExamLab.

### Antes de la sesión 01 (semana de montaje)

Alta de los 50 por CSV · subir `Clases/` completa · asignar material a cada sesión · publicar el Tutor IA ·
importar las 15 sesiones (con las 4 autónomas marcadas) · crear los 11 foros · programar las difusiones de
las 3 ventanas ACA. Detalle en §8.

### Las 11 sesiones sincrónicas

| # | Fecha | Tema y taller (20 min) | Herramienta concreta de ExamLab |
|---:|---|---|---|
| **01** | 10/08 | Acuerdo pedagógico · delimitación. **Taller:** matriz de estado (secciones listas / a medias / inexistentes) + 3 compromisos. Rompehielos en Padlet | **Encuesta `mixed`** que reemplaza a Padlet y al Doc de estado: 1 campo cerrado por sección del APA (Planteamiento · Objetivos · Marco · Metodología → *listo / a medias / inexistente*) + 1 abierto para los 3 compromisos. El docente la lee **agrupada por campo y con el nombre del autor** → tiene el semáforo de los 50 en la misma clase. Ventaja sobre Padlet: queda por curso (hoy el Padlet es **el mismo enlace en los 5 cursos** del docente) y los nombres se resuelven |
| **02** | 24/08 | Pregunta, objetivos y título ≤21 palabras. **Taller:** bloque pregunta + general + 3 específicos + título | **Taller formativo** con 4 preguntas abiertas + **rúbrica escrita como tabla markdown en el enunciado** (el estudiante la ve *antes* de responder) + calificación IA formativa + hilo de retro por pieza. **Reto en vivo** de 6–8 preguntas cerradas sobre el error nombrado en el guion: verbos *"conocer / entender"* en objetivos |
| **03** | 31/08 | Estructura del documento / artículo de avance. **Taller:** outline con bullets por sección | **Pregunta `diagrama`** (mermaid `mindmap`): el mapa de secciones del APA queda **persistido por estudiante, calificable y consultable después** — hoy se dibuja en Excalidraw suelto y se pierde. Contenidos: la `Plantilla_APA_CUN` asignada a esta sesión alimenta al Tutor IA |
| **04** | 07/09 | Antecedentes y referentes (Fase I). **Taller:** 4 fichas + párrafo puente. *(el **Quiz 1**, 6%, cerró el 31/08 en la S03; el **Parcial 1**, 24%, cierra el 14/09 en la S05)* | **Taller formativo**: 1 pregunta abierta por ficha (autor · año · aporte · relación con mi pregunta) con la rúbrica de la ficha en el enunciado, + hilo de retro por ficha. **Registro del Quiz 1** como ítem externo (nota + observación) y **repaso del Parcial 1**, que es el ítem más pesado del primer corte. **Brecha:** la citación APA sigue en ZoteroBib, fuera de ExamLab (§6.1) |
| **05** | 14/09 | Marco teórico — avance. **Taller:** mapa de constructos + 1–2 páginas | **Pregunta `diagrama`** (mermaid `mindmap` o `flowchart`) = el mapa de constructos, exactamente lo que pide el guion. **Tutor IA** para la duda típica de esta semana: *"¿esto es marco teórico o conceptual?"* — respondida a las 11 pm del domingo, no 7 días después |
| **06** | 21/09 | Marco conceptual y contextual. **Taller:** tabla de términos + 1 página contextual | **Encuesta `mixed`** para la tabla de términos (término · definición operativa · fuente), o **foro** — con el dato fino de que **en el foro una tabla markdown sí renderiza como tabla**, mientras que en la respuesta de un taller sale en texto plano (§6.2). Error a atajar: *"contexto = país entero"* |
| **07** | 28/09 | Diseño metodológico (propuesto). **Taller:** ficha metodológica (matriz pregunta–método) | **Encuesta `mixed`** con la ficha como formulario de campos fijos (enfoque · tipo · alcance · población · técnica · instrumento). Es el caso de mayor valor de esta pieza: el docente ve **los 50 enfoques agrupados por campo**, no 50 textos. Alternativa para la matriz: `diagrama` tipo `quadrantChart` |
| **08** | 05/10 | Instrumentos y plan de análisis. **Taller:** bosquejo de instrumento (10 ítems o guía de 8 preguntas). **cierra el Parcial 2 (21%)** | **Brecha explícita: el estudiante NO puede crear una encuesta en ExamLab** — la RLS lo bloquea (§6.5). Workaround: el **docente** construye una encuesta `mixed` de demostración —que es *literalmente* el instrumento que se está enseñando a diseñar— y los 50 la responden para ver cómo se comporta; el bosquejo propio va como pregunta abierta. **Registro del Parcial 2** (21%) como ítem externo |
| **09** | 19/10 | Integración del avance · correcciones. **Taller:** matriz de gaps + dueños ("semáforo por sección") | **Proyecto con 1 slot por sección del APA** (§5.1): cada sección tiene rúbrica, nota y **hilo de retro propio**, y el **diagnóstico del curso** da la matriz estudiante × sección con 5 estados de celda. Es la técnica que el guion ya usa en clase, convertida en tablero |
| **10** | 26/10 | Socialización de avances. **Pitch 3 min + 3 comentarios de pares** | **La sesión no cabe** (150 min en 60). Se vuelve asíncrona: el alumno graba 3 min y el enlace va en `defense_video_url`; **un hilo de foro por estudiante** donde 3 pares comentan. En vivo se hace una muestra de ~10, repartida con una **encuesta `slot`**. **Brecha:** no hay asignación automática de revisores, ni rúbrica de par, ni nota de par — el docente lista a mano quién comenta a quién (§6.3) |
| **11** | 09/11 | Cierre del avance · preparación para TG3. **Taller:** pendientes TG3 + versión limpia. *(la **ACA Final**, 32,8%, cierra el **14/11** — recepción máx.; auto y coevaluación 09–22/11)* | **Última sincrónica antes de la ACA Final**: recordarla, y explicar que la **coevaluación es un foro** de CDigital. **Banco de preguntas** de sustentación etiquetado por sección, que se hereda a TG3. Export del consolidado de notas → digitación en CDigital. **Alerta temprana** final: a quién hay que buscar antes del cierre del 22/11 |

### Las 4 clases autónomas (hoy vacías)

Estas 4 son el 27% de los encuentros y hoy solo dicen *"continuar avance"*. ExamLab aporta el **contenedor
y el recordatorio**; la consigna la sigue escribiendo el docente.

| Fecha | Festivo | Ubicación en el hilo | Herramienta + qué falta |
|---|---|---|---|
| **17/08** | Asunción | Entre S01 (estado) y S02 (pregunta/objetivos) | Sesión marcada `autonoma`: al llegar la fecha **notifica y emaila sola** a los 50, y el alumno marca el material como revisado (queda como asistencia). Material asignado + **foro con ventana 17/08–23/08**. *Falta la consigna* — sugerida *(inferido)*: subir el borrador de pregunta al foro y comentar 1 de un compañero |
| **12/10** | Día de la Raza | Justo después del **Parcial 2** (05/10), antes de S09 (integración) | Ídem. Ventana de foro 12/10–18/10. *Falta la consigna* — sugerida *(inferido)*: leer la retro del Parcial 2 y publicar los 3 gaps propios, que es el insumo del taller de S09 |
| **02/11** | Todos los Santos | Entre S10 (socialización) y S11 (cierre) | Ídem. Ventana 02/11–08/11. *Falta la consigna* — sugerida *(inferido)*: incorporar los comentarios de pares recibidos en S10 y publicar qué cambió |
| **16/11** | Indep. Cartagena | Después de S11 y de la recepción máx. (14/11) | Es la semana de cierre: **nota de la ACA Final** y ventanas de auto/coevaluación abiertas hasta el 22/11. Uso realista: **registro y cierre docente**, no actividad nueva. Difusión programada con el estado de notas antes del cierre del 22/11 |

> **Nota honesta:** marcar las 4 como `autonoma` se hace **en el mismo CSV de importación** del cronograma
> (la columna `session_type` viaja en la plantilla), no una por una. Pero eso resuelve la *logística*, no el
> *contenido*: las 4 consignas siguen sin existir en el material y son la brecha pedagógica más grande del
> curso — mayor que cualquier brecha de herramienta de este documento.

---

## 4. Herramientas que sirven YA, sin desarrollo

Las siete piezas no duplicativas, más el registro docente. Ninguna pide que el estudiante haga dos veces
lo mismo.

| # | Herramienta | Qué hace exactamente | Por qué aquí |
|---|---|---|---|
| 1 | **Contenidos + Tablero** | Sube **carpetas completas** (`.pdf .pptx .docx .xlsx .md .txt .csv` + imágenes; 25 MB/archivo, 100 MB/lote). Asigna material **a una sesión concreta** y permite **destildar archivo por archivo** cuál ve el alumno. Visor inline de PDF e imágenes | Cierra el hueco #1 del curso: la `Clases/` entera entra tal cual, y la consigna real de cada sesión (hoy solo en `Guiones/`) se publica como un `.md` corto por sesión |
| 2 | **Tutor IA por curso** | Chat persistente por alumno que lee el **texto real** del material: `.docx`, `.pptx` (**incluidas las notas del orador**), `.pdf` y `.xlsx`. El alumno **referencia archivos con `#`** y esos se priorizan. Prompt sembrado explícitamente socrático: *"acompañar… **NO resolverle los ejercicios**"*. Es **síncrono** — responde en vivo | La pieza de mayor apalancamiento: 50 proyectos, 6 días de cada 7 en solitario. Lee la `Plantilla_APA_CUN` y los 3 ACAs, así que responde *"¿esto va en marco teórico o conceptual?"* con el documento real del curso, no en genérico |
| 3 | **Foros** | N foros por curso, con **ventana de apertura/cierre**, **sesión asociada**, hilos **fijados**, hilos cerrados y **respuesta oficial** del docente (que sube al tope). Alumno matriculado abre hilos y responde. Renderiza markdown, **tablas incluidas** | En los 4 cursos del docente el foro **no existe hoy** — es el canal asíncrono que con 1 hora semanal no es un extra, es donde ocurre el acompañamiento. En pregrado vale doble: el que no habla en Meet frente a 50 sí escribe |
| 4 | **Sesiones + tipo `autonoma`** | Importación por CSV de las 15 filas (fecha, título, hora, enlace de Meet, corte, grabación, **tipo**). El tipo `autonoma` **notifica y emaila solo** al llegar la fecha, y el alumno marca el material como revisado → cuenta como asistencia. Generador de cronograma que **conoce los festivos de Colombia** | Es el contenedor exacto de la regla *"festivo en lunes → clase autónoma, no cancelación"*, repetida en el Manual y el Calendario. Y el generador evita el error de cuentas: 15 lunes, 4 festivos |
| 5 | **Encuestas** | **Opción única/múltiple** para el pulso en vivo (resultados con nombres). **`mixed`** = formulario de campos (abiertos y cerrados, con obligatorio y tope de caracteres) que el alumno llena campo por campo y el docente lee **agrupado por campo, con autor**. **`slot`** tipo Doodle con reserva de cupo atómica | El pulso en vivo hoy es *"1 pregunta a 2 estudiantes"* = 2 de 50. Y `mixed` es lo que convierte las fichas y matrices del curso (S01, S06, S07) en algo legible de un vistazo |
| 6 | **Pregunta `diagrama`** | Editor mermaid **dentro del taller del estudiante**: cada alumno produce su diagrama, se guarda con su entrega, lleva rúbrica y puntaje. Verificado: **sin whitelist de tipo**, y mermaid 11.15 trae `mindmap`, `quadrantChart`, `journey` y `timeline` además de los de ingeniería | Soporta 4 talleres del curso: mapa de secciones (S03), mapa de constructos (S05), matriz pregunta–método (S07) y semáforo por sección (S09). Hoy se dibuja en Excalidraw suelto y **se pierde al cerrar la pestaña** |
| 7 | **Calendario** | El docente conecta Google **o Microsoft 365** y sincroniza las sesiones **con los 50 como invitados** (`sendUpdates=all`), generando el enlace de Meet. El alumno además se suscribe a un `.ics` privado con sesiones y actividades | Cierra un defecto textual del material: *"Los CSV/ICS de Pregrado **no** incluyen invitados/estudiantes"*. Hoy el estudiante **nunca recibe la invitación** |
| 8 | **Registro de notas + observación** | Editor de actividades externas: grilla de los 50 con **Nota + Observación** por estudiante. Alimenta cortes, alerta temprana, informes y actas | Los ítems del aula (5 cuestionarios + ACA Final) se aplican/entregan en CDigital y se **registran** aquí: costo cero para el estudiante, y habilita el semáforo y el consolidado |
| 9 | **Alerta temprana** | Semáforo por estudiante con motivos discretos (inasistencia · reprobadas · no entregadas · promedio bajo). Rojo solo con **2 señales independientes**. Justificado sale del denominador; tarde cuenta como asistió | Los 550 entregables contra 1 hora semanal. Se mira **antes** de la clase para decidir a quién buscar. *Advertencia:* hay que **abrir Estadísticas** — no llega como alerta |
| 10 | **Progreso de material + videos** | "Abriste N de M archivos" y "Seguías en…". Biblioteca de videos por curso | Distingue *"no entendió"* de *"no abrió nada"*. Y los **12 min × 11 sesiones** de modelación en vivo, grabados una vez, vuelven al taller |

**Lectura:** el solapamiento real no es la evaluación —esa vive en CDigital— sino el **andamiaje del
semestre**: material, canal asíncrono, agenda y semáforo. Es justo lo que el material del curso enumera
como faltante en su §4.

---

## 5. Lo que requiere workaround (y qué se paga)

### 5.1 Semáforo por sección → modelar el documento APA como proyecto de N slots

Es la decisión de diseño más importante de este documento, y la de mayor valor.

| | |
|---|---|
| **Cómo** | Un **proyecto** llamado *"Avance TG2"* con un slot por sección de la plantilla: Planteamiento · Pregunta · Objetivos · Justificación · Antecedentes · Marco teórico · Marco conceptual/contextual · Metodología. Cada slot tiene su **rúbrica**, su **nota** y su **hilo de retroalimentación** propios |
| **Qué se gana** | El *"semáforo por sección"* que la S09 ya usa como técnica de clase, y la *"matriz de estado: listas / a medias / inexistentes"* de la S01, dejan de ser un ejercicio de papel y pasan a ser un tablero real. El **diagnóstico del curso** da la matriz estudiante × sección con 5 estados de celda. Y la retro queda **anclada a la sección que hay que corregir**, no en un correo |
| **Qué se paga** | El estudiante tiene que **pegar el texto de cada sección** en ExamLab además de subir el `.docx` a CDigital. Para 50 estudiantes de pregrado, eso es duplicación y **es el punto donde este plan puede fracasar** |
| **Cómo se evita pagarlo** | **No pedir el texto completo.** Cada slot recibe **un párrafo de estado**, no la sección: *"¿en qué va esta sección y qué te falta?"* (3–5 líneas). Eso conserva el semáforo, la rúbrica y el hilo de retro, y baja el costo del estudiante a ~10 minutos por corte. El documento completo sigue **solo** en CDigital |
| **Alternativa más barata** | Saltarse el proyecto y usar solo la **encuesta `mixed` de la S01** (1 campo cerrado por sección) repetida en S05 y S09. Da el semáforo del grupo, pero **no lleva nota, no entra al consolidado ni a la alerta temprana**, y no tiene hilo de retro por sección |

> **Recomendación:** empezar por la alternativa barata (encuesta `mixed` en S01) y decidir en la S05 si el
> proyecto de slots vale el costo. Si en la S01 la encuesta la responden menos de 35 de 50, el proyecto de
> slots tampoco va a funcionar. *(Umbral inferido; no está en el material.)*

### 5.2 Rúbrica → tabla markdown en el enunciado

No existe rúbrica como dato (§6.4). Pero hay un camino verificado que la mayoría no ve: **el enunciado de
la pregunta se renderiza como markdown en el momento de responder**, y ese renderizador soporta **tablas**.

Entonces una rúbrica de criterios × niveles se escribe como tabla markdown **dentro del enunciado**, y el
estudiante **la ve formateada antes de entregar**. Es la primera vez que este curso tendría rúbrica
visible: hoy no hay ninguna en toda la carpeta (los ACAs traen *checklist* de 5 ítems, no rúbrica con
niveles).

**Lo que se paga:** no hay cálculo por criterio, no se reutiliza entre actividades y no se puede consultar
de forma agregada. Es una rúbrica que se lee, no que se opera.

**Complemento:** el criterio de calidad que hoy vive en la *tabla de acompañamiento* del guion —las
respuestas típicas del docente a *"si el estudiante… usted responde…"*— se pega en el **override del prompt
del Tutor IA por curso**. Así ese criterio alcanza a los 50, y no solo a quien preguntó en los 20 minutos.

### 5.3 Sesión 10 → pitch grabado + foro de pares

| | |
|---|---|
| **Cómo** | El alumno graba 3 min (celular o Meet) y el enlace va en el campo de video de sustentación. Se abre **un hilo de foro por estudiante**; el docente publica la lista de quién comenta a quién (3 pares por alumno) y **fija** la pauta de comentario como hilo destacado |
| **Qué se gana** | 150 minutos imposibles se vuelven asíncronos. Y la clase de 60 min queda libre para una muestra de ~10 pitches en vivo, repartida con una encuesta `slot` |
| **Qué se paga** | **No hay asignación automática de revisores, ni rúbrica de par, ni nota de par, ni registro de que la revisión ocurrió.** El docente arma la lista a mano y verifica leyendo el foro. Para 50 estudiantes son 150 comentarios a supervisar |
| **Mitigación** | Pauta de comentario **fijada** en el foro (3 preguntas fijas), y revisión por muestreo, no exhaustiva |

### 5.4 Las 4 clases autónomas → contenedor listo, consigna pendiente

El contenedor está completo (notificación automática, material asignado, foro con ventana, asistencia
autodeclarada). Lo que **no** aporta ninguna herramienta es la consigna: hoy las 4 dicen *"continuar
avance"*. **Costo: 4 consignas cortas que el docente debe escribir antes del 17/08.** Sugerencias en §3.

### 5.5 Reemplazar Padlet por encuesta `mixed`

El Padlet actual es *"el mismo enlace en los 5 cursos"* del docente, así que los 50 de TG2 comparten muro
con los otros cursos. La encuesta `mixed` queda por curso, resuelve los nombres y el docente la lee
agrupada por campo.

**Qué se paga:** Padlet no pide cuenta; ExamLab sí (§7 R6). Para la sesión 01 —la primera vez que los 50
entran— eso es fricción justo en el peor momento. **Mitigación:** dejar el Padlet para el rompehielos de la
S01 y usar la encuesta `mixed` desde la S02, cuando las cuentas ya estén activas.

---

## 6. Brechas reales

Sin maquillar. Cada una con lo que sí se puede hacer y lo que no.

### 6.1 Gestor de referencias y ayuda de citación APA — **no existe**

Cero. No hay biblioteca de referencias por estudiante, ni importación de DOI/BibTeX/RIS, ni formateo de
cita, ni detección de duplicados. Lo único parecido es un campo de texto libre *"Bibliografía sugerida"* en
el panel del Admin, que es del Syllabus institucional.

**Impacto en este curso:** alto y directo. La S04 pide 4 fichas de antecedentes y la **ACA Final** (32,8%) exige el marco referencial completo e integrado. **ZoteroBib sigue siendo obligatorio y externo**, tal como está
hoy en la *Guía práctica de herramientas de escritura y citación*. ExamLab no lo reemplaza ni lo mejora.

### 6.2 Rúbrica como dato — **no existe**

La rúbrica es una **columna de texto libre** cuyo único consumidor es el prompt de la IA. No hay criterios
como filas, ni niveles, ni puntaje por celda, ni suma, ni reutilización entre actividades.

**Matiz que sí ayuda:** el estudiante **sí ve** la rúbrica renderizada (con tablas) — pero *después* de
calificar. Para verla *antes*, va en el enunciado (§5.2).

### 6.3 Coevaluación / revisión por pares — **no existe**

Cero código y cero tablas. Y es estructural: **un estudiante no puede leer la entrega de otro** (la RLS lo
impide por diseño). No hay tabla de asignación de revisores, ni de comentario de par, ni de nota de par.

**Impacto:** la S10 pide *"3 comentarios de pares con criterio"*. El sustituto es el foro (§5.3): funciona
como actividad, no como instrumento. **Corregido 2026-08-10:** el curso **sí tiene coevaluación con peso
propio (1,6%)**, y en el aula es un **foro de CDigital** — la nota se cumple allá; lo que falta acá es la
actividad formativa.

### 6.4 Historial de versiones del documento — **no existe**

Una entrega por actividad, **sobrescrita**. No hay tabla de versiones ni de hitos. Si el avance se modelara
como una sola actividad reentregable, la V2 pisaría la V1, su retro y su feedback.

**Impacto:** la **ACA Final** integra todo el avance del periodo y exige incorporar la retroalimentación de los
anteriores. **No hay forma de ver si se incorporó.** Workaround: una entidad por versión (una actividad
por corte) en los tres cortes — se conservan las tres notas y las tres retros, se pierde el diff.

### 6.5 Que el estudiante cree una encuesta — **no existe, y está bloqueado en la base**

La escritura de encuestas exige ser docente del curso o Admin. Un matriculado no pasa. No hay flag ni "modo
borrador del alumno": **requiere migración**.

**Impacto:** es exactamente el ejercicio de la **S08** (*"bosquejo de instrumento: 10 ítems o guía de 8
preguntas"*). Lo irónico es que la herramienta que el estudiante necesitaría —el constructor de formularios
`mixed`— existe y está completa, pero solo del lado docente. Workaround en §3, S08.

### 6.6 Similitud en prosa — **existe, pero no sirve para este curso**

Compara **solo entre entregas del mismo curso** (sin internet, sin corpus externo), con dos topes que
rompen el caso: **máximo 30 entregas** por comparación —y aquí hay **50 inscritos**— y **3.000 caracteres**
por texto, o sea ~500 palabras de un avance que tiene páginas. Además el criterio del modelo está calibrado
para código (nombres de variables, literales), no para paráfrasis ni estructura argumentativa.

**Regla operativa:** **no presentarla como antiplagio.** El antiplagio institucional es el de CDigital/CUN,
y la propia *Guía práctica* del curso ya advierte: *"no invente servicios externos de pago"*.

**Lo que sí funciona sobre prosa** y conviene no confundir: la estimación de **texto generado por IA**, que
sí usa marcadores de prosa. Es una señal para conversar, no una prueba.

### 6.7 Cronómetro de actividad proyectable — **no existe**

Cada guion es un reloj (6+14+12+**20**+8) y cada taller tiene un criterio de éxito explícito. No hay un
cronómetro proyectable que muestre a la vez el tiempo restante, la consigna y el criterio. Los únicos
temporizadores son los de examen, Reto en vivo y check-in de asistencia. Se resuelve con un cronómetro
externo compartiendo pantalla.

### 6.8 Menores, pero conviene saberlos

| Brecha | Efecto |
|---|---|
| Asistencia sin *tarde* / *justificado* en la interfaz | El motor de notas y la alerta temprana **sí** los usan (justificado sale del denominador), pero el docente solo puede marcar presente/ausente. Con 11 sincrónicas, faltar a una es el 9% |
| Generar el Reto en vivo **desde el material del curso** | Implementado en el servidor, **sin pantalla que lo pida**. El docente escribe los temas a mano |
| Videos sin reproductor ni posición | La biblioteca abre en pestaña nueva; no hay "reanudar donde ibas" |
| La encuesta `slot` no lleva la hora real del cupo | Manda invitación de calendario a cada estudiante, pero anclada al **cierre de la encuesta**, no a la franja elegida |
| Portafolio / bitácora del estudiante | No existe. El paquete acumulativo de los 3 ACAs no tiene contenedor propio |

---

## 7. Riesgos

Ponderados para **pregrado**: menos autonomía, más estudiantes por hora, y una plataforma más que aprender.

| # | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| **R1** | **Cuarta plataforma para 50 estudiantes de pregrado.** Ya usan CDigital, Meet, Google Docs y Padlet | **Alto** | Alcance mínimo **no duplicativo** (§1). Presentarla como *"donde está el material y donde preguntás"*, no como "otra plataforma de entrega". Si en la S03 menos de 35 de 50 entraron, retirar todo salvo material y tutor |
| **R2** | **Doble trabajo:** hacer el taller en ExamLab **y** subirlo a CDigital | **Alto** | **No espejar los 11 entregables.** Donde ExamLab pida texto (§5.1), pedir un **párrafo de estado**, nunca la sección completa |
| **R3** | **Un ítem sin nota cuenta como 0** con su peso original. La **ACA Final** (32,8%) no cierra hasta el 14/11 | **Medio** *(bajó de Alto el 2026-08-10: con cinco cuestionarios calificados entre agosto y octubre, el estudiante ya no se ve reprobado hasta noviembre)* | Los formativos van con **peso 0**. Explicarlo en la S01. Registrar cada ítem apenas se califica, no al final |
| ~~**R4**~~ | ~~Falta el syllabus SIAC; los pesos 30/30/40 son reconstrucción~~ → **cerrado 2026-08-10** | — | El libro de calificaciones del aula trae la estructura completa (8 ítems con su peso y su ventana). **Ya no bloquea:** los cortes se crean hoy. Del SIAC sigue faltando solo el **temario** |
| **R5** | Los estudiantes entienden que el avance se entrega en ExamLab | **Alto** | Slide explícita en la S01: *"la entrega oficial es y sigue siendo CDigital"*. No crear en ExamLab ningún ítem que parezca recibir el archivo final |
| **R6** | **Fricción de alta:** 50 cuentas, clave temporal y cambio forzado en el primer ingreso | Medio-alto | Importar los 50 por CSV **antes** del 10/08 (el correo de bienvenida sale solo). Dejar el Padlet para el rompehielos de la S01 y estrenar ExamLab en la S02 (§5.5) |
| **R7** | El Tutor IA **le escribe el trabajo** al estudiante | Medio-alto en pregrado | El prompt sembrado ya es anti-atajo (*"NO resolverle los ejercicios"*). Reforzarlo con el override por curso y alinearlo con el checklist de integridad académica de los ACAs. Decirlo en voz alta en la S01 |
| **R8** | La IA califica prosa académica con criterio calibrado para código | Medio | Override del prompt de pregunta de taller **antes** de la S02, con el criterio del curso (coherencia, pertinencia, rigor, calidad de fuentes, escritura académica). Y decir en clase que **esa nota no cuenta** |
| **R9** | Se confunde la similitud de ExamLab con el antiplagio institucional | Medio | **No lo es** (§6.6). No usarla como evidencia |
| **R10** | **Reto en vivo:** no entran jugadores después de que arranca, y un dispositivo con la hora adelantada ve las preguntas vencidas | Medio | Dar margen de lobby largo. Si a un estudiante "no le cargan las preguntas", sospechar el reloj de su equipo antes que la red |
| **R11** | La encuesta `mixed` **no produce nota** ni entra al consolidado | Medio | Es diagnóstico, no evaluación. No prometerle al estudiante que "cuenta" |
| **R12** | El OAuth de calendario puede estar restringido por la CUN en Workspace/365 | Medio | **Probarlo primero**: es lo primero a verificar del montaje. Si no conecta, el `.ics` del alumno sigue funcionando |
| **R13** | **Las 4 autónomas siguen sin consigna.** La herramienta da el contenedor, no el contenido | **Alto** (es el 27% de los encuentros) | Escribir las 4 consignas antes del 17/08. Es trabajo docente que ninguna herramienta sustituye |
| **R14** | Doble fuente de verdad de notas (ExamLab vs CDigital) | Medio | **CDigital manda.** Registrar en ExamLab y exportar hacia CDigital, nunca al revés |
| **R15** | La alerta temprana **no notifica**: hay que abrir Estadísticas | Bajo-medio | Volverlo hábito semanal, el lunes antes de la clase, junto con el progreso de material |

---

## 8. Decisión recomendada y checklist

### Decisión

1. **Adoptar ExamLab como capa de material y acompañamiento**, con alcance explícito: material por sesión,
   tutor IA, foros, sesiones autónomas, encuestas de pulso, diagramas, calendario y registro de notas.
2. **La entrega oficial y las notas siguen en CDigital.** Sin excepción, sin piloto.
3. **No espejar los 11 entregables de sesión.** ExamLab entra solo donde no duplica trabajo del estudiante.
4. Los **3 ACAs** se modelan como actividades **externas** (nota + observación); el estudiante no hace nada
   en ExamLab por ellos.
5. Los ejercicios formativos van con **peso 0** y se retiran sin costo si la adopción es baja.
6. **Las 4 clases autónomas** se marcan como tales en el CSV y se les escribe consigna + foro con ventana.
7. El **proyecto de N slots** (§5.1) se decide en la S05, no antes, y con párrafo de estado — no con la
   sección completa.
8. **No** presentar la similitud de ExamLab como antiplagio institucional.

### Checklist priorizado

**Bloqueante — antes de configurar nada**

- [ ] Docente aprueba este documento (veredicto + alcance de las 7 piezas).
- [x] ~~Conseguir el syllabus SIAC para confirmar pesos y fechas~~ → **resuelto 2026-08-10**: salen del aula. Crear los **tres cortes 30/30/40** con los 8 ítems (Quiz 1 6% + Parcial 1 24% · Quiz 2 9% + Parcial 2 21% · ACA Final 32,8% + Quiz 3 4% + auto 1,6% + coev 1,6%).
- [ ] **Redactar el Quiz 1 antes del 31/08 y el Parcial 1 antes del 14/09** en el Banco de preguntas: en el aula existen como ítem del libro de calificaciones, sin actividad ni preguntas.
- [ ] Verificar que el OAuth de calendario conecta con la cuenta institucional (R12).
- [ ] Confirmar que hay clave de IA configurada y modo **síncrono** — si está en asíncrono, el tutor y la generación no responden en clase.

**Montaje — antes del 10/08**

- [ ] Crear el curso `Trabajo de Grado 2 — 94453 — 54448 (26V04)`; confirmar escala 0–5 y aprobatoria 3.
- [ ] Importar los **50 estudiantes** por CSV con `course_name` (matrícula + correo de bienvenida en un paso).
- [ ] Importar el **CSV de 15 sesiones** con `meeting_url`, `cut_name` y `session_type` — las 4 autónomas marcadas de una vez.
- [ ] Subir la carpeta `Clases/` completa y asignar el material a cada sesión.
- [ ] Subir `Plantilla_APA_CUN_Proyecto de grado.docx` y los 3 enunciados ACA — **esto es lo que alimenta al Tutor IA**.
- [ ] Renombrar o **destildar** los 11 guiones docentes para que no queden visibles al estudiante.
- [ ] **Escribir y publicar las 11 consignas de taller** (hoy solo están en `Guiones/`) como un `.md` corto por sesión. *Es el mayor valor individual de todo el montaje.*
- [ ] **Escribir las 4 consignas de clase autónoma** (R13).
- [ ] Crear los 11 foros (uno por sesión) + 4 foros con ventana para las autónomas.
- [ ] Sincronizar el calendario con los 50 como invitados.
- [ ] Programar las difusiones de las 3 ventanas ACA (una sola sesión de trabajo).

**Verificación — antes de la S01**

- [ ] Probar el Tutor IA: *"¿qué debe llevar el marco conceptual según la plantilla del curso?"*. Si responde solo con el título, el material **no se indexó** — revisar que los archivos estén asignados.
- [ ] Escribir el override del prompt del tutor con el criterio del curso (R7, R8).
- [ ] Preparar la slide *"la entrega oficial es CDigital"* (R5).

**Durante el semestre**

- [ ] S01: encuesta `mixed` de matriz de estado. Contar cuántos de 50 responden → decide R1.
- [ ] S02: Reto en vivo de verbos de objetivo + rúbrica en el enunciado.
- [ ] S05: **decidir** si va el proyecto de N slots (§5.1).
- [ ] Cada lunes antes de clase: revisar alerta temprana + progreso de material (R15).
- [ ] Por ítem del aula (Quiz 1–3, Parcial 1–2, ACA Final): registrar nota + observación → exportar → digitar en CDigital (R14).
- [ ] S10: abrir los 50 hilos de pitch y publicar la asignación de pares (§5.3).
- [ ] Antes del 22/11: generar el consolidado y **descargar la evidencia**.

**Fuera de alcance de este periodo** *(inferido — registrar para decidir después)*

- [ ] Revisión por pares con rúbrica y registro en ExamLab (§6.3) — requiere desarrollo. *(La coevaluación con nota del curso se cumple en el **foro de CDigital**, 1,6%.)*
- [ ] Que el estudiante cree encuestas (§6.5) — requiere migración.
- [ ] Rúbrica como dato (§6.2) y historial de versiones (§6.4).

---

## 9. Fuentes

### Material del curso

| Recurso | Ruta |
|---|---|
| Manual del Docente | `Trabajo de grado 2/Manual del Docente - Trabajo de Grado 2.md` |
| Calendario oficial (15 eventos) | `Trabajo de grado 2/Calendario de clases (oficial).md` |
| Información del grupo | `2026/54448/Informacion.txt` (50/50 inscritos · 94453 · 26V04) |
| Guiones docentes (11) | `Guiones/Sesion NN - <tema>.md` — consignas de taller y tabla de acompañamiento |
| Guía de citación | `Guiones/Guía práctica - Herramientas de escritura y citación.md` |
| Material del estudiante | `Clases/LEEME…docx` · `Presentacion del Curso…pptx` · 11 × `Sesion NN/Presentacion.pptx` |
| Enunciados ACA (3) | `Clases/Recursos/ACAs/ACA {1,2,3}…docx` |
| Plantilla institucional | `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` |
| Hitos a Calendar | `Entregas y hitos docentes - Importar a Calendar.csv` |
| **Syllabus SIAC** | **No está en la carpeta** — declarado faltante en 4 archivos distintos |

### Verificación de capacidades en el código de ExamLab

| Afirmación | Evidencia |
|---|---|
| Tutor IA extrae texto de `.pdf`, `.docx`, `.pptx` (con notas del orador) y `.xlsx` | `supabase/functions/tutor-chat/index.ts:119-136,151-178,202-237` |
| Contenidos: extensiones y topes; subida de carpeta | `src/modules/contents/UploadExternalContentDialog.tsx:97` |
| Subconjunto de archivos visible por sesión | `supabase/migrations/20260920000000_session_content_file_paths.sql:9-14` · `src/routes/app.student.courses.tsx:712-714` |
| Filtro de material solo-docente por nombre de archivo | `src/modules/contents/contents-extract.ts:96-113` |
| Foros: ventana, hilo fijado, hilo cerrado, respuesta oficial | `supabase/migrations/20260520100000_forum.sql:191,208-211,258` · `app.forum.$courseId.$forumId.$threadId.tsx:139,253,648` |
| Markdown con tablas en texto escrito por el estudiante (foro) | `src/shared/components/MarkdownInline.tsx:15,46-57` · `app.forum.$courseId.$forumId.$threadId.tsx:577,634` |
| Enunciado renderizado como markdown al responder | `src/modules/workshops/WorkshopQuestions.tsx:2923` · `src/routes/app.student.take.$examId.tsx:2321` |
| CSV de sesiones: 8 columnas, incluye `session_type` | `src/modules/sessions/csv.ts:31,38-47` |
| Sesión autónoma: notificación automática + asistencia autodeclarada | `supabase/migrations/20261490000000_notify_autonomous_sessions.sql` |
| Generador de sesiones con festivos de Colombia | `src/modules/schedules/co-holidays.ts` · `src/modules/contents/session-plan.ts` |
| Encuesta `mixed`: constructor de campos, obligatorio, tope de caracteres | `supabase/migrations/20260984000000_poll_questions_mixed.sql:26-53` · `src/modules/polls/PollQuestionsEditor.tsx` |
| Resultados de `mixed` agrupados por campo, con autor | `src/routes/app.teacher.polls.tsx:3439-3446,3463` |
| Estudiante llena campo por campo (autosave por pregunta) | `src/routes/app.student.polls.tsx:330,903,1040` |
| Pregunta `diagrama` en el taller del **estudiante** | `src/modules/workshops/WorkshopQuestions.tsx:3034` (dentro de `StudentWorkshopTaker`, l. 1273) · `app.student.take.$examId.tsx:2433` |
| mermaid sin whitelist de tipo de diagrama | `src/modules/code/DiagramEditor.tsx:152-158` (solo `securityLevel:"strict"`) |
| mermaid 11.15.0 incluye `mindmap`, `quadrantChart`, `journey`, `timeline` | `node_modules/mermaid/dist/chunks/mermaid.core/` — verificado |
| Plantillas del editor: 7, todas de ingeniería | `src/modules/code/DiagramEditor.tsx:8-89` |
| Calendario: Google **y** Microsoft 365, invitados + Meet automático | `src/routes/app.teacher.calendar.tsx:393` · `supabase/functions/calendar/index.ts:646-688` |
| `.ics` suscribible del estudiante | `supabase/functions/student-calendar-ics/index.ts` |
| Notas externas con observación | `src/modules/grading/ExternalGradesEditor.tsx` |
| Ítem sin nota cuenta 0 con su peso | `src/modules/grading/grade.ts:70-76` |
| Alerta temprana: motivos discretos, 2 señales para rojo | `src/shared/lib/early-alert.ts:37,107,127` |
| Diagnóstico del curso: matriz estudiante × actividad, 5 estados | `src/modules/courses/diagnostic.ts:55-61,112-140` |
| Proyecto: slot con rúbrica, nota y feedback propios | `supabase/migrations/20260428000000_projects.sql:19-28,70-80` |
| Video de sustentación | `supabase/migrations/20260941000000_project_defense_video.sql` |
| Progreso de material (conteo, no porcentaje) | `supabase/migrations/20261590000000_content_file_progress.sql` |
| Prompt del Tutor IA (socrático, anti-atajo) | `supabase/migrations/20260923000000_tutor_chat_seed_prompt.sql` |
| Rúbrica es texto libre (único consumidor: el prompt) | `20260428000000_projects.sql:25` · `src/modules/ai/grade-submission.ts:36` |
| Similitud: solo entre pares del curso · tope 30 entregas y 3.000 caracteres | `supabase/functions/detect-plagiarism/index.ts:41-45` |
| Prompt de similitud calibrado para código | `supabase/migrations/20260508160000_ai_prompts_plagio_y_ia.sql:37-58` |
| Coevaluación / revisión por pares: inexistente | Búsqueda `coevaluac\|peer_review\|peer_assess` → único hit: plantilla de informe docente |
| Estudiante no puede crear encuestas | `20260932000000_polls_admin_tenant_scoping.sql:109-120` · `20260984000000…sql:86-95` |
| Sin gestor de referencias ni APA | Búsqueda `zotero\|mendeley\|bibtex\|citation\|apa7` → 0 hits funcionales |
| Sin historial de versiones de entrega | Búsqueda `milestone\|hito\|entrega parcial` → 1 hit, y es un comentario |
| Asistencia: solo presente/ausente en la interfaz | `src/routes/app.teacher.attendance.tsx:194-210` |
| Generar Reto desde el material: sin pantalla | `supabase/functions/ai-generate-questions/index.ts:980-990` vs. 0 llamadas desde `src/` |

---

*Documento interno Plan de curso · alcance: TG2 · 54448 · 26V04 · no distribuir a estudiantes.*
*La entrega oficial y el registro de notas de Trabajo de Grado 2 se realizan exclusivamente en CDigital.*
