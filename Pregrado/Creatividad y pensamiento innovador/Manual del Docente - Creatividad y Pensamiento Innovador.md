# Manual del Docente — CREATIVIDAD Y PENSAMIENTO INNOVADOR (Escuela de Ingenierías)
**Plantilla genérica.** Código SIAC de carpeta: **EI004** · Área oferente: **C-EMP** · 2 créditos · 32 h docente + 64 h autónomas.
Fuente: syllabus `CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS EI004_VIR.docx` (en esta carpeta).

> No es AFI / Proyecto I-II. Evaluación por cortes (Art. 52).

**Léelo entero antes de la Sesión 01.** Está escrito para alguien que nunca ha dictado esta asignatura: dice qué se hace en cada encuentro, qué hay que dejar montado en el aula la primera semana, qué se le entrega a la Universidad y qué entregan los estudiantes. Lo específico del grupo de este periodo vive un nivel abajo, en `2026/54408/`.

## 0. Lo mínimo para entrar a la primera clase

| Dato | Valor | De dónde sale |
|---|---|---|
| Grupo · periodo | **54408** · **26V04** · PRIMER BLOQUE (id portal 801143) | `config/cursos/carga_academica_2026.json` |
| Estudiantes | **50 inscritos / cupo 50** | ídem (`grupos.54408`) |
| Encuentro sincrónico | **Miércoles, 5:00–6:00 pm — 60 minutos**, virtual (Google Meet) | ídem (`horario`) |
| Número de encuentros | **7** (12/08 → 23/09 de 2026) | `config/cursos/sesiones_cun.py` |
| Aula en CDigital | https://cdigital.cun.edu.co/course/view.php?id=115463 | `carga_academica_2026.json` → `cursos.creatividad.cdigital` |
| Enlace de Meet | **Todavía no existe**: el material muestra el marcador `[URL Meet — …]`. Lo crea el script de Calendar (§8) | `cursos.creatividad.meet` está vacío |
| Inicio del periodo | **10/08/2026** (institucional) | `carga_academica_2026.json` |
| Recepción máx. de trabajos | **19/09/2026** — ⚠️ **no es fecha institucional** (ver abajo) | ídem |
| Cierre / registro de notas | **27/09/2026** (institucional) | ídem |
| Docente | Julian Andres Castaño · `julian_castanoe@cun.edu.co` | ídem |

**Cinco cosas que se equivocan siempre en este curso:**

1. **La clase dura UNA hora, no dos.** Si vienes de Proyecto I (2 h), recalibra: aquí no hay segunda hora de tutoría. Los guiones ya están cronometrados a 60 minutos exactos, con los minutos de cada fase, y la Sesión 01 trae además una tabla de ampliación por si el grupo va rápido.
2. **Hay quices y parciales, y pesan más que todo lo demás junto.** El **Parcial 1 solo vale 24%**. El único entregable documental del curso es la **ACA Final** (32,8%). Los quices y parciales **no se suben**: son cuestionarios que se resuelven en el aula, y su documento en `Clases/Recursos/ACAs/` es la *guía de qué entra*, no el examen.
3. **Los ítems existen en el libro de calificaciones, pero las actividades no están creadas.** Ver el ítem en el gradebook no significa que el estudiante pueda responder nada. Hay que crear el cuestionario y su banco de preguntas antes de cada ventana (§8.2).
4. **La Sesión 01 es de encuadre: no dicta tema.** Es deliberado y está en el guion. El contenido curricular arranca en la Sesión 02.
5. **La «fecha de recepción» (19/09) no es institucional.** Solo el **inicio (10/08)** y el **cierre/registro de notas (27/09)** lo son. El 19/09 se derivó como ~8 días antes del cierre para tener margen de calificación, y así está escrito en los enunciados del estudiante y en los eventos de Calendar. Es movible si Coordinación pide otra cosa: si la mueves, cámbiala en `config/cursos/carga_academica_2026.json` y regenera (§11), no la corrijas a mano en ocho documentos.

## 📁 Estructura
- **`Clases/Presentacion del Curso - ….pptx`** + **`Clases/Sesion NN - <tema>/Presentacion.pptx`** · docente **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`
- **`Guiones/Sesion NN - <tema>.md`** (solo Markdown; no hay `.docx`) + `Capturas/`
- **`Calendario de clases (oficial).md`** · festivo = autónoma · mapeo tema↔fecha
- **`2026/<grupo>/`** — Informacion + CSV/ICS (**sin invitados**; Meet placeholder único por serie)
- **`Clases/Recursos/ACAs/`** — un documento para el estudiante **por ítem real del aula** (guía de cada quiz y parcial, enunciado de la ACA Final, instructivos de auto y coevaluación) + `Plantilla_APA_CUN_Proyecto de grado.docx`.
- **`HERRAMIENTAS_EXAMLAB.md`** (raíz del curso) — análisis de herramientas de apoyo. Es un **borrador para decisión del Docente**, no material obligatorio ni parte de la nota; su recuadro de corrección del 2026-08-10 ya está alineado con la estructura real del aula.

**Horario confirmado:** miércoles, **5:00–6:00 pm** (60 minutos).
**Festivo en día de clase → clase autónoma** (la actividad queda en el **Drive de clases**). *En este periodo ningún miércoles de los siete cae en festivo, así que las siete sesiones son sincrónicas.*

## 1. Propósito
Que el estudiante identifique habilidades de creatividad e innovación y formule una **Propuesta de Innovación** (hilo conductor desde la semana 1).

Traducido a lo que verás en clase: **no es un curso sobre innovación, es un curso donde cada estudiante escribe su propia propuesta**, sobre un problema real y un usuario concreto, y la va armando por partes. Cada sesión produce una pieza del documento (ideación → tipo de innovación → validación → vigilancia → ecosistema y pitch) y todas esas piezas terminan en un solo entregable: la **ACA Final**. Tu rol es de acompañamiento y criterio, no de experto temático del problema que cada uno eligió: la pregunta que más rinde durante todo el semestre es *«¿quién lo usaría mañana a las 8 am y qué le duele hoy?»*.

## 2. Unidades de conocimiento (syllabus)

> **La Sesión 01 (12/08/2026) es de ENCUADRE: no se dicta tema.** Se presenta el curso, el Docente, los estudiantes y las ACAs. U1–U2 (Propuesta de Innovación · creatividad e inteligencia emocional) → lectura autónoma; se retoma al abrir la Sesión 02. El contenido curricular arranca en la **Sesión 02**.

| # | Temática | Dónde se dicta |
|---|---|---|
| 1 | Introducción · syllabus · trabajo final | S01 (encuadre) → lectura autónoma |
| 2 | Inteligencia emocional, creatividad e innovación | lectura autónoma; se retoma al abrir S02 |
| 3 | Conceptos en I+D · Design Thinking y técnicas | **S02** |
| 4 | Gestión de la innovación (Manual de Oslo / OCDE) | **S03** |
| 5 | Tipos de innovación | **S04** |
| 6 | Análisis de negocios · validación / sustentación | **S05** (sesión doble) |
| 7 | Vigilancia tecnológica | **S05** (sesión doble) |
| 8 | Innovación local–internacional · entidades de apoyo | **S06** (adelantada) |

### El temario está ADELANTADO — lo que recuerdes de la versión anterior es falso

Cambio del **2026-08-11**, registrado en `config/cursos/sesiones_cun.py` (campo `nota_syllabus`): la **ACA Final califica el «ecosistema: entidades de apoyo» (U8)** y cierra el **19/09**, cuatro días **antes** de la Sesión 07, que era donde U8 se dictaba. Se corrigió así:

- **U7 (vigilancia tecnológica) baja a la Sesión 05**, junto con U6, que ya vivía ahí → **la S05 es una sesión doble** y su guion lo dice desde la primera fase.
- **U8 sube a la Sesión 06**, que queda como **la última sincrónica antes del cierre de la ACA Final**. No es sesión de refuerzo: de ahí salen dos puntos calificados de la consigna (entidades de apoyo y pitch).
- **La Sesión 07 queda como taller de consolidación y sustentación**, después del cierre de la ACA Final y del Quiz 3: **no introduce contenido evaluable nuevo**.

Ninguna unidad se eliminó: es un reorden, no un recorte. Si algún documento tuyo todavía dice que la vigilancia tecnológica va en la S06 o que U8 va en la S07, está desactualizado.

### Dos avisos sobre el Syllabus SIAC de esta asignatura

Está en esta carpeta (`CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS EI004_VIR.docx`) y su tabla de unidades es la de arriba. Dos cosas que conviene saber antes de citarlo:

1. **El cuerpo del documento es el de Ciencias Administrativas.** Adentro dice «*…PARA LA ESCUELA DE CIENCIAS ADMINISTRATIVAS*» y **`CÓDIGO SÍAC: AE003`**, aunque el archivo y la oferta sean **EI004** de la Escuela de Ingenierías. Es el mismo temario reutilizado. Los ejemplos que te pide dar los adaptas a ingeniería (así están escritos los guiones); si necesitas citar el código formalmente, usa **EI004**, que es el de la carga académica, y ten presente esta discrepancia por si Coordinación pregunta.
2. **Su «sistema de evaluación» no sirve para configurar el aula.** El Syllabus solo trae filas `EV 01 · 9.0% · «Talleres, Quices, Proyecto»` bajo cortes 30/30/40. Lo que manda es el libro de calificaciones (§3): la auditoría del **2026-08-10** encontró **8 ítems reales** y ese es el desglose que se registra. El Syllabus sí manda en lo curricular (unidades, competencias, bibliografía) y ahí es donde debes apoyarte.

## 3. Evaluación — estructura REAL del aula (CDigital)

**Fuente:** libro de calificaciones del aula en CDigital (auditoría 2026-08-10), cargado en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py creatividad`.

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

- **Producto documental del curso:** la **Propuesta de Innovación**, hilo conductor desde la Sesión 02. Es lo que se entrega como **ACA Final** (tarea) en el tercer corte.
- **Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem del aula** (guía de cada quiz y parcial, enunciado de la ACA Final, instructivo de auto y coevaluación). Regenerar: `python config/slides/build_acas_estudiantes.py creatividad`.

Ventanas (apertura · cierre · límite de nota) y en qué sesión cae cada cuestionario: «Fechas de entrega ACA / cortes» más abajo y `Calendario de clases (oficial).md` → «Evaluación en el aula».

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py creatividad`.

| Ítem | Tipo | Corte | Peso | Apertura | Cierre | Nota docente |
| :--- | :--- | :---: | ---: | :--- | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 12/08/2026 | 19/08/2026 | 26/08/2026 |
| **Parcial 1** | Cuestionario | 1 | 24% | 20/08/2026 | 26/08/2026 | 02/09/2026 |
| **Quiz 2** | Cuestionario | 2 | 9% | 27/08/2026 | 02/09/2026 | 09/09/2026 |
| **Parcial 2** | Cuestionario | 2 | 21% | 03/09/2026 | 09/09/2026 | 16/09/2026 |
| **ACA Final** | Tarea | 3 | 32,8% | 12/08/2026 | 19/09/2026 | 27/09/2026 |
| **Quiz 3** | Cuestionario | 3 | 4% | 10/09/2026 | 16/09/2026 | 23/09/2026 |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 23/09/2026 | 27/09/2026 | 27/09/2026 |
| **Coevaluación** | Foro | 3 | 1,6% | 23/09/2026 | 27/09/2026 | 27/09/2026 |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Ventanas fijadas por el Docente (2026-08-10) sobre la estructura real del aula en CDigital: los quices y parciales son cuestionarios y cierran en día de clase (la Sesión 01 es de encuadre y no evalúa); la ACA Final es una tarea y cierra en la fecha máxima de recepción de trabajos; auto y coevaluación van de la última semana al cierre de notas.

## 4. Grupo actual (2026)
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`).

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 54408 | 26V04 | PRIMER BLOQUE | 10/08/2026 | 19/09/2026 | 27/09/2026 |

**50 inscritos sobre un cupo de 50** — el grupo está lleno, y eso condiciona el diseño de la clase: en 60 minutos no alcanzas a escuchar a 50 personas. Los guiones ya asumen ese número (se leen 3–4 aportes en voz alta, no 50) y por eso el trabajo fino se recoge por CDigital, no en el Meet.

> **Sobre el 10/08:** el `Fechas.txt` del portal que quedó en `2026/54408/` dice **03/08/2026** como inicio. El inicio operativo de todos los cursos de este semestre se fijó en **10/08/2026** y esa es la fecha que usa la carga académica y todo el material generado. La primera clase, en cualquier caso, es el **miércoles 12/08/2026**.

## 5. Cómo guiar cada sesión

### 5.1 La hora: qué cabe y qué no

El encuentro es de **60 minutos** y los guiones están cronometrados fase por fase hasta sumar exactamente esa hora. La forma de la clase, salvo la primera y la última, es siempre la misma:

| Momento | Duración típica | Qué haces |
|---|---|---|
| Antes del encuentro | — | Publica el material de la semana en CDigital y **verifica que la actividad del cuestionario del día exista y esté configurada** (intentos, tiempo límite, retroalimentación diferida). El checklist «antes de clase» está al final de cada guion. |
| Encuadre y puente | ~5–6 min | Retomas lo de la semana pasada y anuncias qué se produce hoy. |
| Bloque de contenido | ~18–20 min | Explicación + **modelación en vivo** (el guion trae el ejemplo ya resuelto: úsalo, es lo que evita la clase abstracta). |
| Taller del estudiante | ~9–17 min | Ellos producen la pieza de la semana; tú acompañas con la tabla de acompañamiento del guion. |
| **Cuestionario en clase** | **10–22 min según el ítem** | El quiz o parcial del día se **aplica dentro del encuentro** y cierra ese mismo día. |
| Cierre y trabajo autónomo | ~6–8 min | Tres ideas del día, nombre del archivo a subir y anuncio del tema siguiente. |

Dos reglas de oro que están escritas en los guiones y conviene no negociar: **el tiempo del cuestionario no es tiempo adicional** (las demás fases ya vienen recortadas para que la hora siga sumando 60), y **lo que no alcance no se elimina: se convierte en trabajo autónomo y se anuncia como tal en CDigital**.

Durante los minutos del cuestionario tu trabajo es mirar el chat del Meet y **anotar quién reporta falla técnica, con nombre y hora**: esa nota es la evidencia si después hay reclamación. No empieces a calificar ahí.

**No hay tutorías formales en este curso.** Los formularios de registro de sesiones y de asistencia a tutorías que verás en el material de Proyecto I son de **AFI / especializaciones** y **no aplican a pregrado** (`Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`). Acompañamiento aquí = los últimos minutos del encuentro, el foro del aula y el correo institucional.

### 5.2 Sesión por sesión

Siete encuentros, todos miércoles 5:00–6:00 pm. Guion en `Guiones/Sesion NN - <tema>.md`; deck del estudiante en `Clases/Sesion NN - <tema>/Presentacion.pptx` (el guion indica, fase por fase, en qué slide vas).

| # | Fecha | Qué pasa realmente en el encuentro | Cierra ese día |
|---|---|---|---|
| **01** | 12/08 | **Encuadre, no tema.** Ocho fases: bienvenida, quién es el Docente, rompehielos en **Slido** —«dos verdades y una mentira» sobre ti, tres rondas, 8 minutos, con premio—, recorrido del curso y su producto, cómo se evalúa, integridad e IA, herramientas y acuerdos, encargo autónomo. Con 50 estudiantes un muro de post-its no lo lee nadie; el juego va **antes** de los porcentajes y de paso te presenta. Guion del montaje en `2026/54408/Rompehielos Slido - Sesion 01.md`. | — (abren Quiz 1 y ACA Final) |
| **02** | 19/08 | **Design Thinking, divergencia/convergencia y ideación.** Modelas un *How Might We* y SCAMPER en vivo; ellos producen su HMW + banco de ideas + boceto. Es la sesión donde cada estudiante elige la semilla de su propuesta. | **Quiz 1** (12 min) |
| **03** | 26/08 | **Gestión de la innovación con el Manual de Oslo.** Clasificas tres casos en vivo (producto, proceso, organización, marketing, social) y ellos tipifican el suyo con las dos condiciones de Oslo: novedad **e** implementación. | **Parcial 1** (22 min) |
| **04** | 02/09 | **Tipos de innovación en serio: de clasificar a argumentar.** Incremental vs. radical y prueba de realidad en contexto socioeconómico; ellos arman la matriz comparativa de su propuesta con criterios, no con gusto. | **Quiz 2** (15 min) |
| **05** | 09/09 | **Sesión DOBLE (U6 + U7).** Por dentro: FODA, Canvas y MVP, con el supuesto más riesgoso y un criterio de éxito fijado *antes* de probar. Por fuera: vigilancia tecnológica en Scholar y Google Patents, con una ficha de señal de cinco campos que termina en una decisión. La primera fase del guion explica al grupo por qué hoy va doble. | **Parcial 2** (22 min) |
| **06** | 16/09 | **Ecosistema y pitch — la última sincrónica antes del cierre de la ACA Final.** Escalas local→internacional, tipos de impacto, mapa de entidades reales con un pedido concreto y el guion del pitch de 60 segundos. **Materia calificada, no repaso**: son dos puntos de la consigna de la ACA Final. | **Quiz 3** (10 min) |
| **07** | 23/09 | **Taller de cierre, sin contenido evaluable nuevo** (la ACA Final y el Quiz 3 ya cerraron). Sustentación cruzada de 3 minutos por persona con cinco preguntas fijas, retroalimentación entre pares, revisión de costuras del documento y **diligenciamiento en clase de autoevaluación y coevaluación**, que abren ese día. | Abren **Autoevaluación** y **Coevaluación** |

### 5.3 Qué se espera del estudiante entre sesiones

El Syllabus declara **32 h con docente y 64 h autónomas**, pero la oferta real de este periodo son **7 encuentros de una hora**: 7 h sincrónicas contra 64 autónomas. Es decir, **el 90 % del trabajo del estudiante ocurre sin ti**, no dos tercios. Planea en consecuencia: lo que no quepa en los 60 minutos no se recorta, se convierte en trabajo autónomo con entregable. Cada guion cierra anunciando un archivo con nombre fijo que se sube a CDigital, y ese archivo es la pieza que la sesión siguiente da por hecha:

| Sesión | Lo que sube el estudiante | Para qué sirve |
|---|---|---|
| 01 | Participación en el rompehielos de Slido + lectura autónoma U1–U2 + su problema en tres líneas + documento de trabajo creado con la plantilla APA | Insumo de la S02 (`Ficha_problema_oportunidad.docx` y `Ejemplo_ficha_modelo.html` están en la carpeta de la S01) |
| 02 | `S02_Ideacion_Apellido` (HMW + banco de ideas + boceto) | Semilla de la propuesta |
| 03 | `S03_FichaOslo_Apellido` | Tipo de innovación justificado |
| 04 | `S04_MatrizTipos_Apellido` | Argumentación del tipo y del grado |
| 05 | `S05_ValidacionVigilancia_Apellido` | FODA + Canvas + MVP + ficha de señal |
| 06 | `S06_EcosistemaPitch_Apellido` | Mapa de entidades + guion del pitch |
| 07 | — (sustentación en vivo; auto y coevaluación en el aula) | Cierre |

**Estos avances son formativos: no están en el libro de calificaciones.** Su función es que la ACA Final no se escriba la noche del 18 de septiembre. Dilo así en la Sesión 01, porque es la frase que más deserción de entrega evita: *el documento es acumulativo; llegar a la entrega final sin los avances es la forma más común de perderla*.

### 5.4 Dónde están tu guion y tu deck

- **Guion (interno, solo Markdown):** `Guiones/Sesion NN - <tema>.md`. Trae fundamento teórico para estudiar antes, guion literal para leer casi textual, minutos por fase, tabla de acompañamiento del taller, preguntas trampa frecuentes, checklist antes de clase y checklist después de clase. Están escritos para que **un docente sin trayectoria en innovación pueda dictar la hora completa**.
- **Deck del estudiante:** `Clases/Sesion NN - <tema>/Presentacion.pptx`. Sin bio del docente (esa va solo en `Clases/Presentacion del Curso - ….pptx`).
- **Capturas de apoyo:** `Guiones/Capturas/`.
- **Regenerar guiones:** `python "Pregrado/Creatividad y pensamiento innovador/Guiones/_regen_guiones_creatividad.py"` o `python config/slides/build_sesion_material.py creatividad all --guion-only`.

## 6. Qué le entregas tú a la Universidad

### Durante el periodo

| Qué | Cuándo | Dónde |
|---|---|---|
| Alistamiento completo del aula (bienvenida, syllabus, cortes, actividades y espacios de entrega) | **Semana 1** | CDigital · aula 115463 |
| **Crear** las actividades de los cuestionarios (Quiz 1/2/3, Parcial 1/2) con su banco de preguntas | Antes de que ABRA cada ventana, no de que cierre — la del Quiz 1 abre el **12/08**, el día de la Sesión 01 | CDigital |
| Nota + retroalimentación de **Quiz 1** | Antes del **26/08/2026** | Gradebook |
| Nota + retroalimentación de **Parcial 1** | Antes del **02/09/2026** | Gradebook |
| Nota + retroalimentación de **Quiz 2** | Antes del **09/09/2026** | Gradebook |
| Nota + retroalimentación de **Parcial 2** | Antes del **16/09/2026** | Gradebook |
| Nota + retroalimentación de **Quiz 3** | Antes del **23/09/2026** | Gradebook |
| Habilitar **Autoevaluación** (cuestionario) y **Coevaluación** (foro) | Ventana **23/09 → 27/09/2026** | CDigital |
| Clase autónoma publicada si un miércoles cayera en festivo | Según calendario | CDigital (este periodo no aplica) |

### Al cierre del periodo

| Qué | Plazo | Nota |
|---|---|---|
| **ACA Final** recibida | **19/09/2026** (recepción máx. de trabajos — fecha operativa, ver §0) | CDigital |
| **ACA Final** calificada con retroalimentación | Antes del **27/09/2026** | Gradebook |
| **Todas** las notas de los tres cortes registradas | **27/09/2026** (cierre del grupo) | Gradebook |
| Respaldo de evidencias (entregas, foros, calificaciones) | Antes del cierre de acceso al aula | Local / Drive propio |

### Lo que NO está confirmado (no lo inventes)

`Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md` marca como **pendiente de confirmar con Coordinación / Escuela** cuatro cosas de pregrado, y así están marcados también los eventos del CSV de hitos:

1. **Acuerdo pedagógico**: si hay formulario propio de pregrado o basta con socializar el Syllabus en CDigital.
2. **Canal oficial de cargue/cierre de notas**: si es solo el gradebook de CDigital o también un portal académico.
3. **Informe de cierre de pregrado**: si existe formato.
4. **Plazo post-cierre** para correcciones y descarga de evidencias.

⚠️ **Los formularios de AFI (registro de sesiones del docente, asistencia a tutorías del estudiante, acuerdo pedagógico e informe de cierre de Proyecto I/II) NO aplican a este curso.** Diligenciarlos «por si acaso» ensucia el registro de otra dependencia. Pregunta a Coordinación antes.

## 7. Qué te entregan los estudiantes

Ocho ítems en el libro de calificaciones. **Solo uno es un documento.** Todos los enunciados y guías del estudiante están en `Clases/Recursos/ACAs/` y se regeneran con `python config/slides/build_acas_estudiantes.py creatividad`.

### Los cuestionarios: Quiz 1/2/3 y Parcial 1/2 — no se suben

Se resuelven **en CDigital, dentro del encuentro**, y la nota queda al enviar. No hay archivo, no hay plantilla APA. El documento `… - guia del cuestionario.docx` es **la guía de qué entra**, no el examen: le dice al estudiante qué sesiones ya se dictaron cuando su ventana cierra, y le recuerda que el recorte exacto, el número de preguntas y el tiempo los publica el Docente en la actividad del aula.

**El temario de cada uno es acumulativo y su regla es «no se pregunta lo que todavía no se ha visto»:**

| Ítem | Cierra | Qué entra | Qué NO entra |
|---|---|---|---|
| **Quiz 1** (6%) | 19/08 | Solo la **lectura autónoma U1–U2** de la S01 y lo que hayas publicado en CDigital. Ninguna sesión de tema cae antes de este cierre | La S02, que se dicta ese mismo día |
| **Parcial 1** (24%) | 26/08 | + **S02** (Design Thinking, HMW, ideación) | La S03, que se dicta ese día |
| **Quiz 2** (9%) | 02/09 | + **S03** (Oslo, gestión de la innovación) | La S04 |
| **Parcial 2** (21%) | 09/09 | + **S04** (tipos, incremental/radical) | La S05 |
| **Quiz 3** (4%) | 16/09 | + **S05** (FODA/Canvas/MVP y vigilancia tecnológica) | La S06 — pero **sí es materia de la ACA Final** |

**Criterio al redactar las preguntas:** el Parcial 1 (24%) y el Parcial 2 (21%) son los dos ítems que deciden el 45% del curso; el Syllabus pide **prueba tipo estándar ICFES–SABER PRO al finalizar cada corte** (Art. 47–48 del Reglamento), así que redáctalos como preguntas de aplicación con caso corto, no de definición memorística. Los quices (6/9/4%) son de verificación rápida y se pueden resolver en 10–15 minutos.

### ACA Final — Propuesta de Innovación (tarea, 32,8%, cierra 19/09, nota máx. 27/09)

El único entregable documental del curso. Documento consolidado de **8–12 páginas** + **pitch de 1 página**, nombre sugerido `CRE_ACAFinal_Apellido`, formato con la plantilla APA CUN. Enunciado del estudiante: `Clases/Recursos/ACAs/ACA Final (32,8%) - Propuesta de Innovacion.docx`.

**Qué debe contener** (así está en la consigna, y es lo que se revisa):

1. Problema–oportunidad: usuario concreto, dolor y **evidencia observable**.
2. Propuesta de valor y tipo(s) de innovación **justificados con el Manual de Oslo**.
3. Validación: FODA + Canvas (BMC) + **MVP definido y verificable**.
4. Vigilancia tecnológica: tendencias, referentes o patentes, **con fuentes citadas**.
5. Ecosistema: entidades de apoyo pertinentes (locales, nacionales o internacionales).
6. Siguiente paso realista.
7. Pitch de 1 página.
8. Referencias de todo lo citado.

**Criterio de calificación** (checklist del propio enunciado, para que la retroalimentación sea la misma que ellos leyeron): usuario y problema concretos, no genéricos · tipo de innovación bien justificado con Oslo · FODA y Canvas coherentes con **ese** problema · MVP claro y verificable · vigilancia con fuentes · entidades identificadas · pitch claro, presentación cuidada e integridad académica.

Lo que más se cae, en orden: propuestas sin usuario («los estudiantes en general»), Canvas copiado de plantilla sin relación con el problema, MVP que en realidad es el producto completo, y vigilancia tecnológica que es una lista de links sin decisión.

### Autoevaluación (cuestionario, 1,6%) y Coevaluación (foro, 1,6%) — 23/09 → 27/09

**No son ACAs y no se sube documento.** La autoevaluación es un **cuestionario individual** sobre la propia trayectoria en el periodo; la coevaluación es un **foro**: se participa publicando un aporte que valora el trabajo y los aportes de los compañeros. Cada estudiante hace las dos: hacer una no cuenta como la otra, y nadie las diligencia por otro. Se abren en la Sesión 07 y se reservan ~4 minutos de clase para cada una, precisamente porque son las que más gente olvida. Tú las habilitas, verificas participación y registras la nota antes del 27/09. Instructivos: `Autoevaluacion individual (1,6%) - instructivo.docx` y `Coevaluacion individual (1,6%) - instructivo.docx`.

## 8. Configuración técnica — semana 1

### 8.1 El aula en CDigital

**https://cdigital.cun.edu.co/course/view.php?id=115463** — es el aula del grupo 54408 y el único canal oficial de entregas y notas (Drive, correo o WhatsApp no sustituyen). Deja publicados en la primera semana: anuncio de bienvenida, Syllabus, régimen de cortes 30/30/40 con el desglose por ítem, los enunciados de `Clases/Recursos/ACAs/`, la plantilla APA y el espacio de entrega del Corte 1.

### 8.2 Crear las actividades (lo más urgente)

Los **ocho ítems ya existen** en el libro de calificaciones, pero **cinco de ellos no tienen actividad asociada**: Quiz 1, Parcial 1, Quiz 2, Parcial 2 y Quiz 3 son, hoy, solo una casilla de nota. Hay que crear cada cuestionario con su banco de preguntas y configurar intentos, tiempo límite y retroalimentación diferida. **El primero vence el 19/08**, en la Sesión 02, así que esto es trabajo de la semana 1, no de la semana 2. Verifica también que la **coevaluación esté creada como FORO** (no como cuestionario ni como tarea) y que la suma de pesos dé 30 + 30 + 40 = 100.

### 8.3 Grupos

**No hay trabajo por equipos en este curso.** La Propuesta de Innovación es individual y los ocho ítems son individuales, así que **no configures grupos ni «elección de grupo»** en CDigital: eso es de Proyecto I. Si autorizas alguna pareja por excepción, es decisión tuya y debe quedar dicha en la Sesión 01, no improvisada en septiembre.

### 8.4 Encuentro sincrónico y eventos de Calendar

El enlace de Meet **todavía no existe**: el campo `cursos.creatividad.meet` de `carga_academica_2026.json` está vacío y por eso el correo de bienvenida, los guiones y el calendario muestran el marcador `[URL Meet — mismo enlace toda la serie · …]`. Los siete eventos, con los **50 estudiantes como invitados** y **una sola sala de Meet para toda la serie**, se crean con el Apps Script de la carpeta del grupo.

➡️ **Sigue el runbook, no improvises:** `Pregrado/Creatividad y pensamiento innovador/2026/54408/LEEME - Crear los eventos de Calendar.md`

Trae el paso a paso completo (activar el servicio avanzado de Calendar, `verificar()` antes de crear nada, `crearEncuentros()`, qué hacer si algo falla y cómo deshacer). Aquí solo se repite lo que más caro cuesta ignorar:

- ⚠️ **No importes el `.ics` ni el `.csv` de encuentros.** Google Calendar **descarta la lista de invitados** al importar esos formatos: quedarías con 7 eventos y 0 invitados, y ya no podrías usar el script sin borrarlos antes. Por eso se llaman `RESPALDO sin invitados - …`. El flujo bueno es `PRINCIPAL - Crear encuentros con invitados.gs`.
- **Sí se importa**, en cambio, `Entregas y hitos docentes - Importar a Calendar.csv`: son recordatorios tuyos (cierres y límites de nota), sin invitados.
- Al terminar, el script te muestra la URL de la sala: **pégala en `config/cursos/carga_academica_2026.json` → `cursos.creatividad.meet`** y regenera el material (§11). Es el único paso manual que queda, y mientras no lo hagas todo el material sigue mostrando el marcador.
- Lo que la API no puede hacer y toca a mano: **coanfitrión** del Meet y **publicar el enlace en el aula**.

## 9. Integridad académica y uso de IA

Se socializa en la fase 6 de la Sesión 01 (slides 12–13) y el guion trae el texto literal. Lo esencial:

- **Todo lo que no sea propio se cita en APA 7**: texto, datos, imágenes, código y también las ideas parafraseadas. Cuenta como plagio copiar sin fuente, parafrasear sin citar, traducir un texto ajeno y presentarlo como propio, o entregar trabajo de otra persona.
- **El plagio no se arregla entre docente y estudiante**: sigue el conducto del **Reglamento Estudiantil de la CUN** (https://cun.edu.co/somos-la-cun/normatividad/). Un porcentaje alto de similitud no es plagio automático: exige tu análisis cualitativo y debido proceso.
- **La IA generativa no está prohibida: está regulada.** Tres reglas que anuncias el primer día: (1) **declararla** en una nota al final del documento —qué herramienta, para qué, y qué hizo el estudiante con la salida—; declararlo no baja la nota, ocultarlo sí es falta; (2) **verificar toda cita** que produzca, porque las referencias inventadas son el error número uno; (3) la IA **no puede hacer lo que este curso evalúa** — no observa a un usuario real, no elige el problema y no defiende un criterio. Un texto impecable sobre un problema que nadie miró se cae en la primera pregunta de la sustentación de la Sesión 07, y esa sesión existe también para eso.

## 10. Checklist accionable

**Antes de la Sesión 01 (12/08)**
- [ ] Aula 115463 abierta, con anuncio de bienvenida, Syllabus y régimen de cortes publicados.
- [ ] Eventos de Calendar creados con el `.gs` según el runbook de `2026/54408/`, y la URL de Meet pegada en `carga_academica_2026.json` + material regenerado.
- [ ] **Quiz 1** (6%) y **ACA Final** (32,8%) **habilitados**: su ventana abre este día.
- [ ] Enunciados de `Clases/Recursos/ACAs/` y plantilla APA publicados en el aula.
- [ ] Evento de Slido creado, con el quiz de las tres rondas y **la mentira marcada** en `2026/54408/Rompehielos Slido - Sesion 01.md`; código listo para pegar en el chat del Meet
- [ ] Decidida tu respuesta a las tres preguntas que siempre salen: trabajo en pareja, uso de IA y entregas tarde.
- [ ] Canal con Coordinación abierto para lo pendiente de §6 (acuerdo pedagógico, cargue de notas, informe de cierre).

**Antes de cada sesión con cuestionario (S02–S06)**
- [ ] La **actividad** del cuestionario del día está creada en CDigital (no solo el ítem del gradebook), con intentos, tiempo límite y retroalimentación diferida.
- [ ] Guion leído y deck de la sesión abierto; capturas de apoyo listas.
- [ ] Espacio de entrega del avance de la semana (`SNN_…`) publicado.
- [ ] Durante el cuestionario: registrar en nota aparte quién reporta falla técnica, con nombre y hora.

**Antes de cada cierre de nota**
- [ ] Quiz 1 → 26/08 · Parcial 1 → 02/09 · Quiz 2 → 09/09 · Parcial 2 → 16/09 · Quiz 3 → 23/09 · ACA Final, Autoevaluación y Coevaluación → 27/09.
- [ ] La retroalimentación usa el mismo checklist que leyó el estudiante en su enunciado.

**Semana del cierre de la ACA Final (14–19/09)**
- [ ] En la Sesión 06 (16/09) anunciado en voz alta que la ACA Final cierra antes del próximo encuentro.
- [ ] Verificado que los archivos subidos abren (un PDF corrupto cuenta como no entregado).

**Sesión 07 y cierre (23–27/09)**
- [ ] **Autoevaluación** (cuestionario) y **Coevaluación** (foro) habilitadas el 23/09 y diligenciadas en clase.
- [ ] Los tres cortes suman 30 + 30 + 40 en el gradebook, sin ítems vacíos.
- [ ] Todas las notas registradas el **27/09/2026**.
- [ ] Evidencias respaldadas antes de perder el acceso al aula.
- [ ] Estudiantes informados de dónde ver la nota definitiva y de la ventana de revisión.

## 11. Fuentes y cómo regenerar

Nada de lo numérico de este manual se escribe a mano. Si cambia un dato, cámbialo en su fuente y regenera.

| Dato | Fuente única | Comando |
|---|---|---|
| Ítems, tipos, pesos y ventanas | `config/cursos/fechas_entrega_aca.py` | `python config/cursos/sync_manuales_fechas.py creatividad` (reescribe **solo** «## 3. Evaluación…» y «## Fechas de entrega ACA…» de este archivo) |
| Sesiones, títulos, detalles y orden del temario | `config/cursos/sesiones_cun.py` | `python config/slides/build_pregrado_cursos.py --calendar-only` (calendario) · `python config/slides/build_sesion_material.py creatividad all` (decks + guiones) |
| Grupo, horario, fechas de oferta, aula y Meet | `config/cursos/carga_academica_2026.json` | `python config/slides/build_all_course_presentations.py` |
| Enunciados y guías del estudiante | derivados de los dos primeros | `python config/slides/build_acas_estudiantes.py creatividad` |
| Serie de encuentros y roster | `2026/54408/` | `python config/slides/build_calendar_encuentros.py creatividad` |
| Hitos del docente en Calendar | derivados | `python config/slides/build_hitos_docentes_calendar.py` |

> ⚠️ **Este archivo es parcialmente generado.** `sync_manuales_fechas.py` reescribe los bloques **«## 3. Evaluación — estructura REAL del aula (CDigital)»** y **«## Fechas de entrega ACA / cortes»** completos, hasta el siguiente encabezado `## `. **No escribas nada tuyo dentro de esos dos bloques: se pierde en la siguiente regeneración.** Todo lo demás de este manual es contenido curado a mano y sobrevive.

**Otros documentos que cruzan con este:**
- `Calendario de clases (oficial).md` (raíz del curso) — mapeo sesión ↔ fecha ↔ ítem que cierra ese día.
- `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md` — ciclo inicio/desarrollo/cierre de pregrado y qué sigue pendiente con Coordinación.
- `Pregrado/Checklist de cierre de curso a satisfaccion.md` — verificables de cierre, útil también para directivos.
- `AUDITORIA CDigital 2026-08-10.md` (raíz del workspace) §2 — la auditoría del libro de calificaciones que manda sobre el Syllabus.
- `HERRAMIENTAS_EXAMLAB.md` (raíz del curso) — opcional, decisión del Docente.
