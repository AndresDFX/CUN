# Parcial 1 — banco de preguntas

**Curso:** TRABAJO DE GRADO 2 · Modelos de Innovación (Ingeniería de Sistemas) · código 94453 · grupo 54448
**Aula CDigital:** 129268
**Ítem:** Parcial 1 — **24% de la nota del curso**, Corte 1
**Ventana:** 07/09/2026 (se abre y se anuncia en la Sesión 04) → 14/09/2026 (se resuelve en clase, Sesión 05, en unos 22 minutos)
**Formato:** 10 preguntas de selección única, 4 opciones, con retroalimentación por opción. Tiempo estimado de resolución: ~15 minutos.
**Categoría en el banco:** `Parcial 1 - TG2 S01-S04`
**Archivo gemelo:** `Parcial 1 - banco de preguntas (Moodle XML).xml`
**Validación:** `python config/moodle/cdigital.py importar "…/Parcial 1 - banco de preguntas (Moodle XML).xml" --curso 129268 --simular` → **10 preguntas · validación local: sin problemas**. El aula no se tocó.

Este documento es el gemelo legible del XML: sirve para revisar el banco sin abrir Moodle, para sustentar cada clave con la **cita literal** de donde salió, y para atender reclamos.

---

## 0. Alcance: qué entra y qué no

El alcance lo fija el **Manual del Docente** (§6.1: «Acumula S02–S04: formulación, estructura del documento y antecedentes») y lo completa la **guía del estudiante** (`Parcial 1 (24%) - guia del cuestionario.docx`), que añade la lectura autónoma obligatoria de la Sesión 01 al temario. Este banco evalúa la unión de las dos: la lectura y las Sesiones 02, 03 y 04.

| Fuente en el alcance | Qué aporta al parcial | Preguntas |
|---|---|---|
| **Lectura autónoma S01** — Arias Castrillón (2020), *Plantear y formular un problema de investigación* | Los cuatro criterios que debe contener un problema de investigación | 01 |
| **Sesión 02** — Del tema a la pregunta: objetivos que se pueden evaluar | Pregunta investigable, anatomía de la pregunta, verbos observables, objetivo general | 02, 03 |
| **Sesión 03** — La estructura del documento de avance | Introducción en embudo, qué va en cada sección, metodología en tiempo propuesto, outline | 04, 05, 06 |
| **Sesión 04** — Antecedentes: buscar, leer y citar sin plagiar | Qué cuenta como antecedente, el bloque de antecedentes, la ficha de cinco campos, el párrafo puente | 07, 08, 09, 10 |

**Regla de oro cumplida.** La Sesión 05 (marco teórico) se dicta **el mismo día en que cierra la ventana**, y el parcial se resuelve dentro de esa clase. Por eso ninguna pregunta necesita la Sesión 05 ni las posteriores, y **ninguna opción usa su vocabulario**: no aparecen «constructo», «variable operacionalizada», «marco conceptual», «marco contextual», «enfoque cuantitativo/cualitativo» como categoría a escoger, «instrumento», «plan de análisis», «triangulación» ni «matriz de consistencia». El ítem 08 sí pide distinguir el bloque de antecedentes de otras piezas del marco referencial, pero **las opciones describen contenidos** (la teoría de fondo, una definición operativa, el escenario del proyecto) **sin usar las etiquetas** «marco teórico / conceptual / contextual»; esas etiquetas aparecen únicamente en la retroalimentación general, que se muestra después de cerrar. La distinción que exige el ítem se enseñó el 07/09, en la tabla de la Sesión 04, dentro de la ventana.

**Regla del Docente cumplida — «temas, no asignatura».** Las **10 preguntas son de contenido académico**. Ninguna pregunta por pesos, cortes, fechas, créditos, horas, canal de entrega, nombre de plantilla, reglas de integridad, uso de IA, acuerdos de convivencia ni mecánica del cuestionario. **La excepción de hasta 2 preguntas de método del curso NO se usó** y no hacía falta: el alcance tiene cuatro fuentes temáticas cargadas de contenido.

---

## 1. Tabla resumen

| # | Nombre en el banco | Fuente | Subtema | Respuesta correcta (resumida) | seg |
|---|---|---|---|---|---|
| 01 | TG2-P1-01 Los cuatro criterios aplicados a un planteamiento | Lectura S01 | Los 4 criterios del problema | Faltan la espacio-temporal y la de los sujetos | 100 |
| 02 | TG2-P1-02 Una pregunta que ya trae la solución decidida | S02 | Pregunta investigable | La solución ya está decidida; no hay problema que investigar | 90 |
| 03 | TG2-P1-03 El objetivo general como espejo de la pregunta | S02 | Objetivo general | «Evaluar el efecto de un modelo… en la mesa de ayuda de X» | 110 |
| 04 | TG2-P1-04 La introducción como embudo de tres párrafos | S03 | Introducción | Contexto → problema → propósito | 80 |
| 05 | TG2-P1-05 Cómo se escribe la metodología del avance | S03 | Tiempo verbal del método | «Se propone aplicar una encuesta a los analistas…» | 90 |
| 06 | TG2-P1-06 Viñetas del outline: afirmación, no etiqueta | S03 | Outline | «La mesa de ayuda recibe los tickets por tres canales…» | 85 |
| 07 | TG2-P1-07 Qué tienen en común las fuentes que sí cuentan | S04 | Qué cuenta como antecedente | Dicen qué método usaron y qué encontraron | 90 |
| 08 | TG2-P1-08 Qué va en el bloque de antecedentes | S04 | Antecedentes ≠ teoría | Un estudio de 2022 que clasificó tickets y reporta su hallazgo | 95 |
| 09 | TG2-P1-09 La línea «me aporta» de la ficha | S04 | Ficha de antecedente | «Me aporta el criterio de coincidencia con el analista…» | 90 |
| 10 | TG2-P1-10 El párrafo puente y el vacío | S04 | Párrafo puente | Coinciden en… · difieren en… · ninguno abordó… | 75 |

**Total estimado: 905 segundos ≈ 15 minutos.** Cabe con holgura en los ~22 minutos que el Manual reserva para aplicarlo en la Sesión 05.

---

## 2. Las 10 preguntas completas

### 01 · TG2-P1-01 Los cuatro criterios aplicados a un planteamiento

**Enunciado.** Un compañero le muestra su planteamiento: describe con detalle qué ocurre con la clasificación de tickets y argumenta con cifras por qué eso constituye un problema, pero no dice en qué área ni en qué periodo trabajará, ni con quiénes lo hará. Según los cuatro criterios de la lectura autónoma obligatoria de la Sesión 01 (Arias Castrillón, 2020), ¿cuáles son las dos descripciones que le faltan?

- ✅ **La descripción espacio-temporal y la descripción de los sujetos de investigación.** → *Falta situar dónde y cuándo se investigará —y justificar por qué ahí y no en otro lugar— y describir la población con la que se va a trabajar. Son los criterios 3 y 4.*
- ❌ La descripción del fenómeno y la descripción del desequilibrio. → *Son justamente las dos que el planteamiento ya tiene: contar qué ocurre es el fenómeno; argumentar con cifras por qué es un problema es el desequilibrio.*
- ❌ La descripción del desequilibrio y la descripción de los sujetos de investigación. → *Acierta con los sujetos, pero el desequilibrio ya está resuelto por las cifras. Lo que falta con ellos es el dónde y el cuándo.*
- ❌ La descripción del fenómeno y la descripción espacio-temporal. → *Acierta con la espacio-temporal, pero el fenómeno ya está descrito en el planteamiento.*

**Cita literal** (Arias Castrillón, 2020, p. 309): «3. Descripción espaciotemporal: implica una descripción del espacio y el tiempo en que se va a realizar la investigación. Justificar por qué en ese lugar geográfico y no en otro, cuáles son las características de ese lugar que hacen que el problema sea importante de investigar. De igual manera el tiempo, situar históricamente el problema a investigar […] 4. Descripción de los sujetos de investigación: describir la población con la que se va a trabajar. Cuáles son las características de estas personas y por qué se hace la investigación con ellos y no con otras personas. […] Estas descripciones nos van a permitir delimitar claramente el objeto de investigación y construir la pregunta de investigación».

**Apoyo** (misma lectura, p. 308, criterios 1 y 2, los que el caso sí cumple): «1. Una descripción del fenómeno: […] ¿qué es lo que sucede en el fragmento de realidad que se propone investigar? 2. Una descripción del desequilibrio: es decir, ese problema ¿por qué es un problema? […] Aquí es común el uso de cifras estadísticas de informes oficiales sobre el problema en cuestión».

**Blindaje.** Las cuatro opciones son combinaciones de dos criterios, con la misma longitud y la misma sintaxis, así que la forma no delata nada: hay que entender los cuatro para descartar tres. Es un ítem de aplicación, no de memoria; el trabajo está en leer el caso y ver qué falta.

---

### 02 · TG2-P1-02 Una pregunta que ya trae la solución decidida

**Enunciado.** Un compañero llega con esta pregunta de investigación: «¿Cómo implementar Python en la empresa X para agilizar el registro de incidentes?». Según los criterios de la Sesión 02, ¿cuál es el defecto de fondo de esa pregunta?

- ✅ **Que la solución ya está decidida: justifica una herramienta escogida en vez de indagar un problema.**
- ❌ Que se contesta con un sí o con un no, así que incumple la exigencia de ser abierta. → *Empieza por «cómo»: sí es abierta. Los arranques que se agotan en sí o no son «¿es…?», «¿sirve…?», «¿debería…?».*
- ❌ Que el contexto es imposible de abarcar y habría que reducirlo a una organización identificable. → *El contexto ya está acotado a la empresa X; ese defecto es el de «¿cómo mejorar los procesos de las empresas colombianas?».*
- ❌ Que es una consulta de buscador: la respuesta ya está publicada en la documentación del lenguaje. → *Ese es el defecto de «¿qué es el aprendizaje automático?», que se responde leyendo.*

**Cita literal** (Presentación S02): «**No es** el título, ni el objetivo, ni la solución que usted ya decidió aplicar. · Si la pregunta ya nombra la solución ("¿cómo implementar Python para…?"), no está investigando: está justificando lo que ya escogió.»

**Apoyo** (S02, tabla «Preguntas que no sirven y su versión investigable»): «¿Cómo implementar Python en la empresa? — La solución ya está decidida; no hay problema — **¿Cómo** afecta la clasificación manual de tickets la carga de trabajo del analista de soporte de X?»

**Blindaje.** Los tres distractores son los otros tres defectos de la misma tabla (sí/no, contexto inabarcable, consulta de buscador). Cada uno es un error real y frecuente, y la retroalimentación explica por qué no aplica *a este caso*: se corrige la confusión, no solo se descarta la opción.

---

### 03 · TG2-P1-03 El objetivo general como espejo de la pregunta

**Enunciado.** Su pregunta quedó así: «¿En qué medida un modelo de clasificación supervisada reduce el tiempo de clasificación de tickets en la mesa de ayuda de la empresa X?». Según la Sesión 02, ¿cuál de estos objetivos generales está bien formulado para esa pregunta?

- ✅ **Evaluar el efecto de un modelo de clasificación supervisada sobre el tiempo de clasificación de tickets en la mesa de ayuda de la empresa X.**
- ❌ Diseñar e implementar un modelo de clasificación supervisada que reduzca el tiempo de clasificación de tickets en la mesa de ayuda de la empresa X. → *Dos verbos, dos proyectos; y da por probado lo que la pregunta quiere establecer.*
- ❌ Comparar el tiempo de clasificación de tickets con y sin el modelo de clasificación supervisada en la mesa de ayuda de la empresa X. → *Es un objetivo específico, el paso de contrastar, no el propósito completo.*
- ❌ Conocer el funcionamiento de los modelos de clasificación supervisada aplicados al manejo de tickets en las mesas de ayuda. → *Verbo que nadie puede verificar, y además se sale del contexto de la pregunta.*

**Cita literal** (Presentación S02): «Fórmula: **verbo observable + qué + sobre qué o en quién + en qué contexto**. · "**Evaluar** el efecto de un modelo de clasificación supervisada sobre el tiempo de clasificación de tickets en la mesa de ayuda de la empresa X." · **Regla del espejo**: la pregunta y el general dicen lo mismo —uno en interrogación, el otro en propósito—. · **Un solo verbo** en el general. "Evaluar y diseñar" son dos proyectos, no uno.»

**Apoyo 1** (S02, tabla de verbos): «Conocer — Nadie puede verificar cuánto conoció usted — Identificar · caracterizar», con la nota «si no puede decir **con qué evidencia** demostraría que cumplió el verbo, el verbo está mal escogido».
**Apoyo 2** (S03, outline modelado): «**Objetivos** — general: evaluar el efecto del modelo · específicos: caracterizar el flujo, diseñar el modelo, **comparar tiempos**» — de ahí que «comparar tiempos» sea específico y no general.

**Blindaje.** Es el ítem más largo y el más discriminante del banco: cada distractor encarna un error distinto (dos verbos / confundir específico con general / verbo no medible) y los cuatro tienen longitud comparable, con la clave en segundo lugar de extensión.

---

### 04 · TG2-P1-04 La introducción como embudo de tres párrafos

**Enunciado.** Según la Sesión 03, la introducción del documento de avance es un embudo de tres párrafos. ¿En qué orden van esos párrafos?

- ✅ **Contexto, problema y propósito: el escenario real con un dato verificable, qué está fallando y a quién le duele, y qué propone el proyecto.**
- ❌ Problema, contexto y propósito. → *Invierte los dos primeros movimientos: la falla se enuncia sin haber situado el escenario.*
- ❌ Propósito, contexto y problema. → *Arranca por la solución, así que el problema queda puesto para justificar una decisión ya tomada.*
- ❌ Recorrido histórico, contexto y propósito. → *Es el arranque que la sesión prohíbe de forma expresa, y además desaparece el párrafo del problema.*

**Cita literal** (Presentación S03): «**Párrafo 1 — contexto:** el escenario real donde vive el problema, con un dato verificable. · **Párrafo 2 — problema:** qué está fallando y a quién le duele. · **Párrafo 3 — propósito:** qué se propone hacer el proyecto y para qué sirve. · El embudo va de lo general a **su** caso, en tres párrafos, no en tres páginas. · Prohibido el arranque histórico universal: la introducción no empieza en la prehistoria, empieza en el contexto del problema.»

**Apoyo** (S03, tabla «Sección por sección»): «Introducción — Contexto → problema → propósito, en ese orden — Error típico: arrancar "desde la antigüedad, el ser humano…"».

**Blindaje.** Los tres distractores son permutaciones plausibles y cada opción incluye la glosa de sus movimientos, de modo que no se puede acertar por longitud. El cuarto recoge el error real más común del curso.

---

### 05 · TG2-P1-05 Cómo se escribe la metodología del avance

**Enunciado.** En la sección de diseño metodológico de su documento de avance, ¿cuál de estas frases está bien escrita según la Sesión 03?

- ✅ **«Se propone aplicar una encuesta a los analistas del área de soporte de la empresa X.»**
- ❌ «Se aplicó una encuesta a 30 analistas del área de soporte de la empresa X.» → *Pasado: da por ejecutado un trabajo de campo que pertenece al semestre siguiente.*
- ❌ «Se propone aplicar una encuesta cuyos resultados muestran una reducción del tiempo de clasificación.» → *Empieza bien y mete un hallazgo dentro de la frase.*
- ❌ «Se concluye que el modelo propuesto es más eficiente que la clasificación manual de tickets.» → *Es una conclusión: responde «¿qué encontré?».*

**Cita literal** (Presentación S03): «En este curso **todavía no hay resultados**: el trabajo de campo pertenece al semestre siguiente. · Por eso la metodología se escribe en **propuesto**: "se propone", "se aplicará", "se seleccionará". · Si en la sección de método aparece un porcentaje, un hallazgo o una conclusión, algo está fuera de lugar. · Frase de control: si la oración responde "¿qué encontré?", no va en método. Si responde "¿qué voy a hacer?", sí va.»

**Apoyo** (S03, tabla «Tiempo verbal: cómo se escribe cada cosa en el avance»): «"Se aplicó una encuesta a 30 analistas." → "Se propone aplicar una encuesta a los analistas del área de soporte." · "Los resultados muestran una reducción del 40 %." → "Se espera comparar el tiempo de clasificación con y sin el modelo propuesto." · "Se concluye que el modelo es eficiente." → "El avance concluye con el diseño del modelo; su evaluación empírica queda planteada."»

**Blindaje.** El tercer distractor **también empieza por «Se propone»**, así que la clave no se detecta mirando el verbo inicial: hay que leer la frase completa. Se evitó a propósito el ejemplo «se observó que los tickets de red demoran más», porque el mismo deck admite **datos de contexto ya publicados y citados**, lo que abriría una segunda lectura defendible.

---

### 06 · TG2-P1-06 Viñetas del outline: afirmación, no etiqueta

**Enunciado.** La Sesión 03 pide que cada viñeta del outline sea una afirmación y no una etiqueta. ¿Cuál de estas viñetas del planteamiento cumple ese criterio?

- ✅ **La mesa de ayuda recibe los tickets por tres canales distintos y sin categoría previa.**
- ❌ Contexto del problema y su importancia para el área de soporte de la empresa. → *Etiqueta: nombra el tema del párrafo pero no dice nada del caso.*
- ❌ Aquí se explicará por qué la clasificación manual afecta el trabajo del analista. → *Promesa: anuncia lo que se dirá en vez de decirlo.*
- ❌ Planteamiento del problema, pendiente de redactar cuando aparezcan las fuentes. → *Rótulo con un pendiente.*

**Cita literal** (Presentación S03): «**Outline** = cada sección del documento con **3 a 5 viñetas** de lo que irá adentro. Nada de párrafos todavía. […] Cada viñeta debe ser una **afirmación**, no una etiqueta. · Mal: "contexto". Bien: "la mesa de ayuda recibe tickets por tres canales distintos y sin categoría previa".»

**Apoyo** (S03, autoevaluación): «Cada sección tiene entre 3 y 5 viñetas, y cada viñeta afirma algo (no es una etiqueta)». Y sobre el cuarto distractor: «Marque con color las secciones que hoy están **vacías**: ese color es su lista de tareas de las próximas semanas» — marcar el vacío es válido, pero no reemplaza la viñeta que afirma.

**Blindaje.** Los tres distractores tienen longitud parecida a la clave y son de **tipos distintos** (etiqueta, promesa, pendiente), no variaciones del mismo molde. El cuarto es el más sutil, porque describe una práctica que sí existe en la sesión, pero para otra cosa.

---

### 07 · TG2-P1-07 Qué tienen en común las fuentes que sí cuentan

**Enunciado.** La Sesión 04 acepta como antecedentes los artículos de revistas académicas, las tesis y trabajos de grado, las ponencias de congresos y los informes técnicos de entidades reconocidas. ¿Qué tienen en común todas ellas, y que en cambio le falta a un blog o a un video de opinión?

- ✅ **Que dicen qué método usaron y qué encontraron, de modo que su resultado se puede verificar.**
- ❌ Que se consiguen en las bases de datos de la biblioteca CUN, y no en un buscador abierto. → *Confunde el lugar de búsqueda con la calidad de la fuente; la sesión también manda a Google Académico, SciELO y Redalyc.*
- ❌ Que se publicaron en los últimos cinco años, requisito que ninguna fuente puede incumplir. → *Convierte en regla absoluta una recomendación que admite excepción para los trabajos fundacionales.*
- ❌ Que estudian exactamente el mismo problema del proyecto, en el mismo tipo de organización. → *Endurece el criterio: basta parecerse en al menos una de tres cosas.*

**Cita literal** (Presentación S04): «**Sí cuentan:** artículos de revistas académicas, tesis y trabajos de grado, ponencias de congresos, informes técnicos de entidades reconocidas. · Todos tienen algo en común: dicen **qué método usaron** y **qué encontraron**. · **No cuentan como antecedente:** blogs, videos de opinión, páginas comerciales de productos, ni respuestas de un asistente de inteligencia artificial. · Un texto sin método verificable no es un estudio previo; es una opinión.»

**Apoyo** (misma diapositiva): «**Ventana temporal recomendada: últimos 5 años**, salvo que sea un trabajo fundacional del área. · Un antecedente debe **parecerse a su proyecto** en al menos una de tres cosas: el problema, el método o el tipo de organización. · Si no se parece en ninguna, es lectura interesante, pero no es antecedente suyo.»

**Blindaje.** Los tres distractores son criterios **verdaderos de la sesión pero mal usados**: uno cambia el lugar por la calidad, otro vuelve absoluta una recomendación, el tercero endurece el parecido hasta dejar el bloque vacío. Es la confusión que el Docente verá en las fichas entregadas: descartar fuentes buenas por la fecha y aceptar blogs recientes.

---

### 08 · TG2-P1-08 Qué va en el bloque de antecedentes

**Enunciado.** Está armando el bloque de **antecedentes** del marco referencial. De acuerdo con la Sesión 04, ¿cuál de estos contenidos corresponde a ese bloque?

- ✅ **Un estudio de 2022 que clasificó tickets de soporte con aprendizaje automático y reporta qué encontró.**
- ❌ La explicación de qué es la clasificación supervisada y cómo funciona como modelo de fondo. → *Es la teoría con la que se entiende el fenómeno, no un precedente.*
- ❌ La definición de «tiempo de atención» como los minutos entre la apertura y el cierre del ticket. → *Es una definición operativa de un término del proyecto.*
- ❌ La descripción del área de soporte de la empresa X como escenario real y acotado del proyecto. → *Responde «¿dónde ocurre esto exactamente?»: sitúa el trabajo, no muestra qué se hizo antes.*

**Cita literal** (Presentación S04, tabla «Las tres piezas del marco referencial no son lo mismo»): «Antecedentes — Estudios previos parecidos al suyo — ¿Quién ya hizo algo así y qué halló? — Un estudio que clasificó tickets con aprendizaje automático en 2022». Nota de la misma tabla: «Hoy solo se trabaja la primera fila. Confundir antecedentes con teoría es el error que más devoluciones genera en esta sección».

**Nota de alcance.** Las **opciones no nombran** «marco teórico», «marco conceptual» ni «marco contextual»: describen contenidos, porque esas piezas se desarrollan en la Sesión 05 y siguientes, fuera de la ventana. Las etiquetas solo aparecen en la retroalimentación general, que se publica al cerrar. La distinción que el ítem exige está en la tabla proyectada el 07/09, dentro de la ventana.

**Blindaje.** Los tres distractores son las otras tres filas de la tabla, redactadas como contenido concreto del mismo caso de los tickets y con longitudes equivalentes. Solo una opción reporta un estudio con hallazgo.

---

### 09 · TG2-P1-09 La línea «me aporta» de la ficha

**Enunciado.** La ficha de antecedente de la Sesión 04 tiene cinco campos y el último es «Aporte a mi proyecto». ¿Cuál de estas líneas cumple lo que ese campo exige?

- ✅ **Me aporta el criterio de «coincidencia con el analista» para medir el acierto, que puedo adaptar a mi caso.**
- ❌ Me aporta una referencia muy importante y actualizada, que respalda todo mi marco referencial. → *Es la fórmula vaga que la sesión descarta: equivale a «me sirve de referencia».*
- ❌ Me aporta el resumen del artículo, que copié tal cual para no alterar lo que quisieron decir los autores. → *La ficha se escribe con palabras propias, y este campo no recoge lo que dijeron los autores.*
- ❌ Me aporta el año y el nombre de la revista, datos que necesito para completar la referencia en APA 7. → *Repite el primer campo de la ficha.*

**Cita literal** (Presentación S04): «**Aporte a mi proyecto** — ¿Para qué me sirve a mí? — Una línea, obligatoria. […] Sin la última línea la ficha es decorativa: se convierte en una lista de lecturas, no en un argumento. Empiécela siempre con "Me aporta…".»

**Apoyo** (S04, ejemplo modelado): «**Me aporta:** el criterio de "coincidencia con el analista" como forma de medir el acierto, que puedo adaptar a mi caso; y la advertencia de que las categorías poco frecuentes necesitan tratamiento aparte. · Note que **nada** está copiado del resumen original: todo está reescrito con palabras propias. · Note también que el aporte es **específico**: no dice "me sirve de referencia", dice qué se lleva.»

**Blindaje.** Las cuatro opciones empiezan igual, por «Me aporta», así que el molde no delata la clave: la diferencia está en el contenido. El segundo distractor es literalmente el antiejemplo de la sesión; el tercero y el cuarto llenan el campo equivocado de la ficha.

---

### 10 · TG2-P1-10 El párrafo puente y el vacío

**Enunciado.** Después de las cuatro fichas, la Sesión 04 pide un **párrafo puente** que convierta la lista en argumento. ¿Cuál es su fórmula de tres movimientos?

- ✅ **Coinciden en…, difieren en… y ninguno abordó…, que es el vacío que el proyecto viene a llenar.**
- ❌ Coinciden en…, difieren en… y por eso conviene…, que anuncia la solución técnica que se construirá. → *Cambia el vacío por el anuncio de la solución.*
- ❌ Resumen de cada estudio en orden cronológico y cierre con el más reciente. → *Ordenar por fecha no crea argumento: sigue siendo un catálogo.*
- ❌ Objetivo, método y hallazgo de cada estudio, uno tras otro, para que el lector compare por su cuenta. → *Eso es lo que ya hacen las fichas.*

**Cita literal** (Presentación S04, diapositiva «El párrafo puente: lo que convierte la lista en argumento»): «Cuatro fichas pegadas una tras otra son un catálogo. El **párrafo puente** las **vuelve un razonamiento**. · Fórmula de tres movimientos: **coinciden en… · difieren en… · ninguno abordó…** · El tercer movimiento —el vacío— es la razón de ser de todo el bloque de antecedentes.»

**Apoyo** (S04, criterio de éxito del trabajo autónomo): «el párrafo puente nombra explícitamente el vacío que llena su proyecto». Y en la autoevaluación: «El párrafo puente tiene los tres movimientos y termina nombrando el vacío».

**Blindaje.** El primer distractor conserva los dos primeros movimientos y cambia solo el tercero, que es justo donde está el aprendizaje; los otros dos son las dos formas de catálogo que el párrafo puente viene a reemplazar. Es la pregunta más corta del banco a propósito: cierra el cuestionario con el concepto que más se usa en la entrega de la Sesión 04.

---

## 3. Reparto y decisiones de composición

**Por fuente:** 1 de la lectura autónoma (01) + 2 de la Sesión 02 (02, 03) + 3 de la Sesión 03 (04, 05, 06) + 4 de la Sesión 04 (07, 08, 09, 10).

**Por qué el peso está atrás.** El Quiz 1 (6%, ventana 24/08 → 31/08) ya evalúa la lectura autónoma y la Sesión 02: su banco gemelo dedica cuatro preguntas a la lectura y seis a la S02. Las Sesiones 03 y 04 son el **material nuevo desde ese cierre** y son las dos que sostienen el entregable del corte. Por eso el Parcial 1 conserva la lectura y la S02 solo como prerrequisitos aplicados —una y dos preguntas— y carga siete de diez en S03 y S04. El ítem sigue siendo acumulativo, como promete el Manual, pero sin repetir el quiz. Ver §6, punto 7, para el traslape residual.

**Tipo de tarea cognitiva:** 7 de las 10 son **casos cortos de aplicación** —hay que juzgar un planteamiento, una pregunta, un objetivo, una frase de método, una viñeta, un contenido o una línea de ficha— y 3 piden reconocer una regla o una fórmula (04, 07, 10). Ninguna se responde con una definición memorizada.

**Blindaje general.** En las 10 preguntas: una sola opción defendible; los tres distractores nunca comparten plantilla sintáctica entre sí, salvo donde el paralelismo es deliberado (ítems 01 y 09, en los que el molde común impide que la forma delate la clave); longitudes comparables y la clave nunca es la opción más larga; ninguna opción del tipo «todas las anteriores» o «ninguna de las anteriores»; cada distractor es un error real, observado o anunciado en el material, y su retroalimentación explica **por qué** falla, no solo que falla.

**Vocabulario.** Español de Colombia, trato de **usted**, sin anglicismos innecesarios («aprendizaje automático», no *machine learning*, salvo donde el deck lo escribe así). Se dice **Syllabus**, nunca «sílabo» —aunque en este banco no hace falta nombrarlo, porque no se pregunta administración—.

---

## 4. Lo que este banco NO cubre

**Por la regla de oro (fuera de la ventana).** Nada de la Sesión 05 (marco teórico, teorías que sostienen el fenómeno) ni de la Sesión 06 y siguientes (marco conceptual y contextual, diseño metodológico, población y muestra, instrumentos, plan de análisis, integración del documento, socialización). El parcial se resuelve **dentro** de la Sesión 05, antes o después de dictarla; en cualquiera de los dos casos el estudiante no puede quedar evaluado sobre lo que apenas está viendo. Ese material es el alcance del Parcial 2.

**Reservas de contenido en alcance, no usadas** (sirven para renovar el banco en la próxima edición o para reemplazar un ítem que traslape con el Quiz 1):

- S02 (**fila agotada: el banco del Quiz 1 ya usa las cuatro, así que no sirven para reemplazar un ítem de este parcial**): el título provisional y el tope de 21 palabras (`TG2-Q1-06`); el **test del subrayado** (`TG2-Q1-02`); los tres específicos con el orden caracterizar → diseñar → comparar (`TG2-Q1-04`); los verbos no medibles y sus reemplazos (`TG2-Q1-03`). Quedan libres, dentro de S02, la tabla «preguntas que no sirven y su versión investigable» —usada en el Quiz 2 y el Parcial 2— y el cierre de la sesión con las tres piezas de salida.
- S03: la tabla **sección por sección** completa (qué va y qué no en cada sección); la prueba de ubicación («si una idea puede ir en dos secciones, está mal redactada»); los datos de contexto citados que sí pueden aparecer en el método; estimar párrafos por sección.
- S04: la **ventana de cinco años** y su excepción fundacional; el mínimo de una fuente nacional o local y una internacional; la **lectura estratégica** en tres pasos (resumen → conclusiones → método) y la bola de nieve; cómo se arma una consulta (3 a 5 palabras clave, comillas, filtro de años, traducción al inglés); qué hacer si la búsqueda trae cero o demasiados resultados.
- Lectura S01: los tres tipos de razonamiento (inductivo, deductivo, abductivo). Se dejó fuera a propósito porque la guía de la lectura pide leer esa parte «como contexto, sin atascarse», y evaluarla sería más exigente que lo prometido.

**Por la regla del Docente (temas, no asignatura).** No se pregunta nada de: pesos, cortes o composición de la nota; fechas, ventanas o plazos; créditos y horas; canal de entrega, plantilla o nombre del archivo; reglas de integridad académica y uso de IA; acuerdos de convivencia; qué traer a la próxima sesión; herramientas del curso o mecánica del cuestionario. Todo eso está en el Manual y en la guía del estudiante: se administra, no se evalúa.

---

## 5. Notas de aplicación en CDigital

- Importar el XML en **Banco de preguntas → Importar → formato Moodle XML**. Crea la categoría `Parcial 1 - TG2 S01-S04` dentro del curso 129268. El nombre de la categoría **no lleva el número de grupo**: el mismo banco sirve si el aula se replica en otra edición.
- Comando de validación usado (no toca el aula): `export PYTHONUTF8=1 && python config/moodle/cdigital.py importar "Pregrado/Trabajo de grado 2/Clases/Recursos/Cuestionarios/Parcial 1 - banco de preguntas (Moodle XML).xml" --curso 129268 --simular` → *10 preguntas · validación local: sin problemas*.
- Configuración sugerida del cuestionario: **1 intento**, orden de preguntas aleatorio, respuestas mezcladas (ya viene activado por pregunta con `shuffleanswers`), calificación 10 puntos que el aula pondera al 24%, **retroalimentación después de cerrar el cuestionario** para que las claves no circulen durante la ventana, y tiempo límite de **20 minutos** (el banco se resuelve en ~15).
- La ventana debe abrir el **07/09/2026** (Sesión 04, se anuncia en el cierre de la clase con nombre y peso) y cerrar el **14/09/2026** (Sesión 05, se aplica en clase en ~22 minutos). El Manual, §5.4: quien falta ese día pierde el ítem.
- **Publique en la descripción de la actividad** los parámetros que la guía del estudiante deja explícitamente en manos del Docente: intentos, tiempo límite, cantidad y tipo de preguntas, material permitido y si se puede retomar un intento interrumpido.

---

## 6. Desajustes encontrados en el material (para revisión del Docente)

1. **TG2 no tiene Syllabus SIAC en el repositorio** (Manual, Aviso 2), así que **no hay unidades oficiales que nombrar**. Por eso la categoría del banco se identifica por sesiones (`Parcial 1 - TG2 S01-S04`) y no por unidades como en los otros cursos (`Quiz 1 - Creatividad U1-U2`). Cuando aparezca el `.docx` SIAC hay que revisar si conviene renombrar la categoría por unidades.
2. **El Manual y la guía del estudiante no dicen exactamente lo mismo sobre el alcance.** El Manual §6.1 dice «Acumula **S02–S04**»; la guía añade, con razón, la **lectura autónoma de la S01** («Su unidad quedó como lectura autónoma y se retomó al abrir la Sesión 02, así que también hace parte del temario»). Este banco siguió la guía, que es el documento que el estudiante tiene en la mano, y de ahí sale la pregunta 01. Vale la pena unificar la redacción del Manual.
3. **La tabla de la Sesión 04 se titula «Las tres piezas del marco referencial no son lo mismo» pero tiene cuatro filas** (antecedentes, marco teórico, marco conceptual, marco contextual). El conteo cuadra con la tabla de la Sesión 03, donde el marco referencial se describe como «antecedentes + marco teórico + conceptual y contextual» (conceptual y contextual como una sola pieza), pero visto en pantalla el título contradice lo que se ve debajo. **Ninguna pregunta de este banco depende del número de piezas** —el ítem 08 pide reconocer contenidos, no contarlos—, precisamente por eso. Recomendación: cambiar el título a «Las piezas del marco referencial no son lo mismo».
4. **El deck de la Sesión 04 pide «cuatro fichas» y su nota dice «al menos una fuente nacional o local y al menos una internacional»**, mientras la fila de la Sesión 04 en el Manual (§5.3) dice «fichas con ≥ 1 fuente nacional y ≥ 1 internacional» sin fijar el número de fichas. No es contradicción, pero si el Docente quiere preguntar por el mínimo del entregable en una edición futura, conviene que las dos fuentes digan «cuatro fichas» de forma explícita.
5. **Los decks de las Sesiones 02, 03 y 04 traen el marcador `[URL CDigital — campus del curso pendiente]`** en la diapositiva de trabajo autónomo. No afecta a este banco (no se pregunta canal de entrega), pero el estudiante lo ve proyectado. Vale reemplazarlo por `https://cdigital.cun.edu.co/course/view.php?id=129268`.
6. **El aula 129268 ya tiene 54 preguntas guardadas** en la categoría «Preguntas guardadas del contexto Cuestionario: Autoevaluación» (visto en la simulación de importación). El Manual dice que los cinco cuestionarios existen «solo como línea del gradebook», así que ese contexto viene de un cuestionario de plantilla del aula. **Antes de aplicar el Parcial 1 hay que verificar que el cuestionario que se cree apunte a la categoría nueva** y no herede slots aleatorios de esa categoría de plantilla.
7. **Traslape con el banco del Quiz 1: ya corregido en lo grueso, pero conviene una última mirada antes de publicar.** El banco del Quiz 1 (`Quiz 1 - banco de preguntas (Moodle XML).xml`, misma carpeta) se escribió en paralelo y cubre la lectura autónoma y la Sesión 02, que también entran en el Parcial 1 porque este es acumulativo. Al detectarlo se rehízo este banco: la lectura bajó a una sola pregunta y el peso se movió a S03 y S04. Queda un traslape de **tema, no de pregunta**, en dos puntos: el Quiz 1 pregunta por los cuatro criterios y por el contenido de la descripción del desequilibrio, y aquí el ítem 01 pide aplicar esos mismos cuatro criterios a un caso; el Quiz 1 también trabaja el objetivo general, y aquí lo hace el ítem 03. Son tareas distintas (nombrar frente a aplicar) y median dos semanas, lo cual es legítimo en un parcial acumulativo; pero si el Docente prefiere cero repetición, los reemplazos deben salir de las reservas de **S03 y S04** de la §4, nunca de la fila de S02: esa fila está agotada por el Quiz 1 (el test del subrayado es `TG2-Q1-02`, los tres específicos son `TG2-Q1-04`, la regla del espejo es `TG2-Q1-05`, el tope de 21 palabras es `TG2-Q1-06` y los verbos no medibles son `TG2-Q1-03`). Sirven, en cambio, la **prueba de ubicación** o la **tabla sección por sección** de S03 para el ítem 03, y la **lectura estratégica en tres pasos** o la **ventana de cinco años con su excepción** de S04 para el ítem 01.
