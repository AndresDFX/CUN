# Parcial 1 (24%) · Banco de preguntas — Trabajo de Grado 3

**Curso:** TRABAJO DE GRADO 3 — Modelos de Innovación (Ing. Sistemas) · código SIAC **94532** · grupos **54450 / 54466 / 54467** · CUN · 2026
**Aulas:** son **tres** (54450 → CDigital 112321 · 54466 → 116387 · 54467 → 129270). Este banco se importa en las tres; la categoría no lleva número de grupo a propósito.
**Docente:** Julián Andrés Castaño
**Ítem:** Parcial 1 · Cuestionario · **24% de la nota del curso** · **Corte 1** (30% = Quiz 1 6% + Parcial 1 24%)
**Ventana:** 08/09/2026 (abre en la Sesión 05) a 15/09/2026 (cierra en la Sesión 06) · se resuelve **dentro del encuentro**, en los **22 minutos** que el Manual reserva ese día (la sesión más recortada del semestre)
**Formato:** selección única, 4 opciones, retroalimentación por opción. Mezcla de ítems conceptuales y **casos cortos de aplicación** (5 de los 10 ponen al estudiante frente a una pregunta, un párrafo, una fila de matriz o un ítem de instrumento y le piden decidir).

**Archivo importable:** `Parcial 1 - banco de preguntas (Moodle XML).xml` (categoría `$course$/Parcial 1 - TG3 S01-S05`).
**Validado** con `python config/moodle/cdigital.py importar … --curso 112321 --simular`: **10 preguntas · validación local: sin problemas** · el aula quedó intacta.

---

## 0. Alcance: qué entra y qué no

El alcance no lo decide este banco. Lo fija el **Manual del Docente TG3**, §Parte 3, tabla de los cinco cuestionarios: *«**Parcial 1** (24%) — Hasta **S05** (nuevo desde Quiz 1: S03–S05). Estructura del artículo, referentes fase I, diseño metodológico e instrumento. El ítem más pesado del curso después de la ACA Final»*, con sus dos reglas duras: *«**El alcance es acumulativo:** entran todas las sesiones ya dictadas cuando el cuestionario cierra (…). La lectura autónoma de la S01 (U1–U2) también cuenta»* y *«**El tema del mismo día NO entra**»*.

Lo confirma la guía del estudiante (`Clases/Recursos/ACAs/Parcial 1 (24%) - guia del cuestionario.docx`): *«Lo que NO entra: la Sesión 06 (15/09/2026 — Comunidades de práctica y co-creación) se dicta el mismo día en que cierra el cuestionario, así que su tema queda fuera: no se te pregunta algo que todavía no has visto en clase. Ese tema entra en Quiz 2.»*

**Sí entra:**

| Fuente en alcance | Qué aporta al banco | Preguntas |
|---|---|---|
| **Lectura autónoma obligatoria de la Sesión 01** — Itriago C., M. y Zerpa, C. E. (2011). *El planteamiento del problema en el proyecto de investigación en ingeniería*. Revista de la Facultad de Ingeniería UCV, 26(3), 39–54. PDF en la carpeta de la Sesión 01 | El problema como **estructura** de cuatro partes: en qué momento entran las **operaciones** y qué las distingue de los otros tres componentes | 01 |
| **Sesión 02** (18/08) — Formulación de pregunta, objetivos y título · deck `config/slides/content/cun_tg3_s02.json` | Del objetivo general a los **específicos**: cuántos, con qué verbos y en qué **orden** (cada específico es después una sección del artículo) | 02 |
| **Sesión 03** (25/08) — Estructura del artículo · taller de introducción · deck `cun_tg3_s03.json` | Anatomía IMRyD sección por sección, la regla mental *por qué / cómo / qué encontré / qué significa*, la introducción como embudo de seis tramos | 03, 04 |
| **Sesión 04** (01/09) — Fase I de referentes · deck `cun_tg3_s04.json` | Antecedentes frente a marco teórico y estado del arte, los cinco criterios del buen referente, la ficha de cuatro campos, el mapa de diálogo | 05, 06, 07 |
| **Sesión 05** (08/09) — Diseño de instrumento · desarrollo metodológico · deck `cun_tg3_s05.json` | Matriz de consistencia y su orden de llenado, técnica frente a instrumento, la regla dura del ítem que responde a un objetivo | 08, 09, 10 |

**La Sesión 01 no aporta encuadre, aporta su lectura.** La Sesión 01 es de encuadre y no dictó tema (*«Hoy no se dicta tema»*, Manual §1.2); U1–U2 quedaron como lectura autónoma obligatoria y se retomaron al abrir la Sesión 02 (`Lectura autonoma - Sesion 01.txt`). La pregunta 01 sale del **artículo**, no de la presentación de encuadre. Se agotó esa lectura antes de considerar cualquier otra cosa, y de hecho da mucho más de una pregunta: el reparto del banco privilegió los decks porque el encargo del Docente pide preguntas *«más de temas que aparezcan en la presentación»*, y porque la lectura es territorio natural del **Quiz 1** (alcance hasta S02), que se aplica tres semanas antes.

**No entra (regla de oro):** nada de la Sesión 06 en adelante. Ninguna pregunta la necesita y **ninguna opción usa su vocabulario**:

- **S06** — no aparecen «comunidades de práctica», «co-creación», «socializar entre pares», «bitácora de retroalimentación de pares» ni el nombre de Wenger (que el deck de la S04 sí menciona de paso, como ejemplo de teoría fundacional; aquí se omitió igual, por prudencia).
- **S07** — no aparecen «análisis de datos», «tabla de hallazgos», «experiencia creativa» ni «codificación por categorías» como tarea del estudiante.
- **S08** — no aparece «Fase III», ni «cierre del marco teórico», ni «huecos del marco».
- **S09** — no aparecen «relación explícita con los referentes» ni la escritura de resultados y discusión como sección propia. **Ojo:** la pregunta 03 sí nombra *Resultados* y *Discusión*, pero solo como **casillas del esqueleto**, que es exactamente como las presenta la tabla de anatomía de la **propia Sesión 03**; no se pregunta cómo se escriben, que es lo de la S09.
- **S10** — no aparecen «resumen», «palabras clave», «tesauro UNESCO», «conclusiones» ni «referencias» como tarea.
- **S11 a S13** — no aparecen «póster», «evidencias», «antiplagio», «similitud», «sustentación», «jurados» ni «repositorio institucional».

**Tampoco entra la administración del curso.** Por encargo expreso del Docente (*«más de temas que aparezcan en la presentación, no tanto de la asignatura»*), este banco **no pregunta** pesos, porcentajes ni composición de cortes; fechas ni ventanas; créditos ni horas; canal de entrega, nombre de la plantilla o extensión del entregable; reglas de integridad o de uso de IA; acuerdos de convivencia; ni mecánica del cuestionario. **Las 10 preguntas son de tema.** **No se usó la excepción** de las 2 preguntas de método del curso: no hacía falta, el alcance tiene cinco fuentes temáticas y cuatro de ellas son decks completos.

Un detalle deliberado: el mínimo de **50 referencias** y las **4.000 palabras** del Syllabus aparecen en los decks, pero aquí **no se preguntan**. Son requisitos del producto, no conceptos: preguntar la cifra sería preguntar por la asignatura. Lo que sí se evalúa es el criterio detrás de la cifra — *«cantidad sin pertinencia no cuenta»* — y eso está en la pregunta 06.

---

## 1. Tabla resumen

| # | Nombre | Fuente | Subtema | Respuesta correcta | Seg. |
|---|--------|--------|---------|--------------------|------|
| 1 | TG3-P1-01 El componente que pone en marcha el trabajo de ingeniería | Lectura S01 | Datos · metas · restricciones · operaciones | Las operaciones: las acciones para ir de los datos a la meta | 95 |
| 2 | TG3-P1-02 El orden en que van los objetivos específicos | S02 | Objetivos específicos: cuántos, qué verbos, qué orden | El orden: describir → diseñar → comparar, o sea 2, 3, 1 | 85 |
| 3 | TG3-P1-03 Un párrafo que responde dos preguntas a la vez | S03 | La regla mental de las cuatro palabras | Partirlo: el dato a Resultados, el contraste a Discusión | 100 |
| 4 | TG3-P1-04 El tramo del vacío en el embudo de la introducción | S03 | Los seis tramos del embudo | Qué no se ha estudiado ni resuelto todavía | 90 |
| 5 | TG3-P1-05 Qué pregunta responde la Fase I de referentes | S04 | Antecedentes ≠ marco teórico ≠ estado del arte | ¿Quién más ha estudiado esto y qué encontró? | 75 |
| 6 | TG3-P1-06 El campo de la ficha que decide si la fuente entra | S04 | La ficha de cuatro campos · aporte declarable | Se descarta: sin aporte declarable, no entra al artículo | 95 |
| 7 | TG3-P1-07 Mapa de diálogo: el autor que aporta método | S04 | Confirman · contradicen · extienden · aportan método | Interesa cómo midió; se copia la lógica, no el texto | 85 |
| 8 | TG3-P1-08 El orden en que se llena la matriz de consistencia | S05 | Las cinco columnas y por qué se leen de izquierda a derecha | Objetivo → variable → técnica → instrumento → análisis | 100 |
| 9 | TG3-P1-09 Técnica e instrumento no son la misma cosa | S05 | Forma de acercarse al dato vs. objeto que lo captura | Técnica «entrevista» · instrumento «guía de 8 preguntas» | 90 |
| 10 | TG3-P1-10 El ítem huérfano del instrumento | S05 | La regla dura: cada ítem responde a un objetivo | Se borra: entra porque un objetivo lo necesita | 85 |

**Total estimado: 900 segundos = 15 minutos.** Cabe en los **22 minutos** que el Manual reserva dentro de la Sesión 06 (§1.1), con margen para entrar al aula, leer las instrucciones y enviar el intento. Si se quiere un intento más corto, aplicar el banco con selección aleatoria de 6 ítems (1 de lectura + 1 de S02/S03 + 2 de S04 + 2 de S05) da unos 9 minutos.

**Aleatorización:** el Manual (§Parte 5) pide aleatorizar orden de preguntas y de respuestas, porque los 112 estudiantes de los tres grupos resuelven en la misma hora y en la misma sala. El XML ya trae `<shuffleanswers>true</shuffleanswers>` en las 10 preguntas; el orden de preguntas se activa en la actividad de CDigital.

---

## 2. Las 10 preguntas completas

### TG3-P1-01 · El componente que pone en marcha el trabajo de ingeniería
*Lectura autónoma S01 · El problema como estructura de cuatro partes · caso corto · 95 s*

**Enunciado:** Un estudiante ya identificó, en la situación que quiere investigar, la información de partida, el lugar al que quiere llegar y los factores que condicionan qué solución sería viable. Según la lectura autónoma obligatoria de la Sesión 01, ¿qué componente de la **estructura del problema** le falta todavía y qué contiene?

| | Opción | |
|---|---|---|
| ✅ | Las operaciones: las acciones específicas que hay que realizar para ir de los datos a la meta, considerando las restricciones que la situación impone. | **Clave** |
| ✗ | Las restricciones: los factores de la situación que ponen condicionantes para alcanzar la meta y deciden cuál solución resulta admisible y cuál no lo es. | Ya están en el enunciado |
| ✗ | Los antecedentes: la revisión de lo que otros autores ya publicaron sobre la misma situación problemática, que el texto cuenta como cuarto componente. | Alimentan los **datos**, no son componente |
| ✗ | La hipótesis: la respuesta anticipada al problema, que según el texto debe quedar formulada antes de empezar a redactar el planteamiento. | No está en el modelo de la lectura |

> **Cita literal de la fuente** (Itriago y Zerpa, 2011, p. 42 — PDF en `Clases/Sesion 01 - …/`):
> «una vez que se han considerado los tres factores anteriores (datos, metas y restricciones) **es cuando el trabajo en Ingeniería comienza**: se requiere generar las **Operaciones** necesarias para dar con la solución más eficiente y económica; en otras palabras, el componente "operaciones" se refiere a **las acciones específicas que deben realizarse para ir de los datos a la meta, considerando las restricciones que la situación impone**.»
>
> El enunciado describe los otros tres componentes con las definiciones del mismo artículo, sin nombrarlos: «**Dato** es todo aquel componente de un problema que aporta información acerca de en qué consiste la situación»; «**Meta** es el componente de un problema que expresa de forma explícita o implícita, dónde se quiere llegar; el lugar deseado»; y de las restricciones, «factores (…) que tienden a poner condicionantes para alcanzar la meta; es decir, condicionan el tipo de solución que se puede aportar». El distractor de los antecedentes también sale del texto, pero de otro lugar: «Esta información puede estar referida a los **antecedentes** de la situación-problema» — es decir, son insumo de los datos, no un quinto componente.

**Por qué funciona:** el estudiante que memorizó la lista de cuatro palabras no basta: el enunciado le da tres de los cuatro **descritos, no nombrados**, así que tiene que reconocerlos para saber cuál sobra. Los dos distractores fuertes son las restricciones (que están en el enunciado, disfrazadas) y los antecedentes (que sí aparecen en la lectura, pero como insumo). Los cuatro textos de opción tienen longitud pareja y ninguno es más completo que la clave.

**Nota de no solapamiento:** esta pregunta **no repite** TG3-Q1-01 (que pide la lista completa de los cuatro componentes) ni TG3-Q1-03 (que pide la definición de las restricciones). Aquí las restricciones son **distractor**, no clave, y lo evaluado es en qué momento del proceso entran las operaciones.

---

### TG3-P1-02 · El orden en que van los objetivos específicos
*Sesión 02 · Objetivos específicos: cuántos, qué verbos, qué orden · caso corto · 85 s*

**Enunciado:** Un estudiante presenta sus tres objetivos específicos en este orden: (1) *comparar* los tiempos de despliegue antes y después de la automatización; (2) *caracterizar* el proceso actual del equipo; (3) *diseñar* la automatización de las pruebas. Según la Sesión 02, ¿qué está mal y cómo se corrige?

| | Opción | |
|---|---|---|
| ✅ | El orden: van en secuencia lógica —primero describir lo que hay, luego diseñar o intervenir y al final comparar—, así que quedan 2, 3, 1. | **Clave** |
| ✗ | Nada: como los tres se derivan de la pregunta y cada uno usa un verbo operable y verificable, el orden en que se enumeran no cambia nada de lo que se escribe. | El orden fija el orden del artículo |
| ✗ | El número: tres objetivos específicos dejan el proyecto corto y la sesión pide entre cinco y siete, para que cada variable de la pregunta tenga el suyo. | La sesión pide «tres o cuatro» |
| ✗ | Los verbos: comparar, caracterizar y diseñar ocurren dentro de la cabeza del estudiante y nadie puede verificarlos, así que hay que cambiarlos por conocer, entender y profundizar en. | Está invertido: esos son los verbos desterrados |

> **Cita literal de la fuente** (deck de la Sesión 02, `cun_tg3_s02.json`, slide «Del objetivo general a los específicos»):
> «Los objetivos específicos son los **pasos** para lograr el general: **tres o cuatro, ni más ni menos**. **Regla de oro de esta sesión: cada objetivo específico se convierte después en una sección del artículo.** (…) Los específicos se ordenan **en secuencia lógica: primero describir lo que hay, luego diseñar o intervenir, al final comparar o evaluar**.»
> El ejemplo modelado de la misma sesión los presenta justo en ese orden: «Específico 1: **Caracterizar**… Específico 2: **Diseñar**… Específico 3: **Comparar**…».
> El cuarto distractor invierte la tabla de la slide siguiente de la misma sesión, «Verbos: los que hunden el proyecto y los que lo sostienen»: *caracterizar*, *comparar* y *diseñar* están los tres en la columna **«Verbo operable (úselo)»**, mientras que *conocer* y *entender* están en la de verbo débil porque «**ocurre dentro de su cabeza: nadie puede verificarlo**» y *profundizar en* porque «**no tiene punto de llegada: nunca se sabe si se cumplió**».

**Por qué funciona:** el caso trae **un solo** defecto y los otros dos atributos que el estudiante podría atacar —el número y los verbos— están deliberadamente correctos, así que los distractores 3 y 4 son falsables contra el enunciado. El distractor «Nada» es el más tentador para quien recuerda que los objetivos se derivan de la pregunta pero no recuerda la regla de oro que conecta cada específico con una sección del artículo. Ningún texto de opción es más corto que la clave.

**Nota de no solapamiento:** esta pregunta **no repite** TG3-Q1-07, que usa el mismo tema de la S02 pero evalúa las cuatro piezas de la **pregunta** de investigación (conector, variable que se mueve, variable que se observa, actor y contexto). Aquí no se evalúa la pregunta, sino los **objetivos específicos**: cuántos, con qué verbos y en qué orden.

---

### TG3-P1-03 · Un párrafo que responde dos preguntas a la vez
*Sesión 03 · La regla mental de las cuatro palabras · caso corto · 100 s*

**Enunciado:** Usted escribió este párrafo: *«El tiempo promedio de despliegue bajó de 42 a 15 minutos, lo cual coincide con lo que reporta Ramírez (2022) y sugiere que la manualidad era el cuello de botella del proceso»*. Según la regla mental de la Sesión 03, ¿qué hay que hacer con él?

| | Opción | |
|---|---|---|
| ✅ | Partirlo: el dato medido se queda en Resultados, en tono neutral, y el contraste con el autor pasa a Discusión. | **Clave** |
| ✗ | Dejarlo completo en Resultados: el hallazgo y su explicación son la misma cosa y separarlos fragmenta la lectura. | Interpretar es lo que NO va en Resultados |
| ✗ | Dejarlo completo en Discusión: desde el momento en que cita a un autor, el párrafo dejó de ser un resultado. | La cita no decide la sección |
| ✗ | Subirlo a la introducción: allí se anuncia el hallazgo principal para que el lector sepa a qué atenerse. | La introducción responde «por qué» |

> **Cita literal de la fuente** (deck de la Sesión 03, `cun_tg3_s03.json`, slide «La regla mental que evita el 90% de las mezclas»):
> «**Resultados = qué encontré.** Los datos y hallazgos, sin adjetivos ni juicios. **Discusión = qué significa.** Qué implican esos hallazgos frente a lo que dicen otros autores. (…) **Si un párrafo responde dos preguntas a la vez, pártalo en dos y mande cada mitad a su sección.**»
> La tabla «Anatomía del artículo» de la misma sesión lo confirma en las dos filas relevantes: «Resultados | Qué se encontró, en tono **neutral** | **Interpretar y opinar aquí**» (columna de «Qué NO va») y «Discusión | Qué significa, en diálogo con los autores | Repetir los resultados con otras palabras».
> El cuarto distractor viene del ejemplo de mezcla clásica de la propia sesión: «"Se aplicó una encuesta de 10 ítems a los usuarios y se evidenció que el 70% desconoce el proceso", escrito **en la introducción**. (…) En la introducción no debía ir ninguna de las dos.»

**Nota de alcance:** esta pregunta nombra *Resultados* y *Discusión*, pero solo como **casillas del esqueleto**, tal como las presenta la tabla de anatomía de la Sesión 03. **No** se pregunta cómo se escribe una discusión, que es el tema de la Sesión 09 y por tanto fuera de alcance. El párrafo del enunciado lo da el enunciado: el estudiante no tiene que producirlo.

---

### TG3-P1-04 · El tramo del vacío en el embudo de la introducción
*Sesión 03 · Los seis tramos del embudo · 90 s*

**Enunciado:** La Sesión 03 presenta la introducción como un embudo con seis tramos: contexto, problema, **vacío**, pregunta, objetivos y propósito. ¿Qué tiene que decir el tramo del **vacío**?

| | Opción | |
|---|---|---|
| ✅ | Qué no se ha estudiado ni resuelto todavía: el hueco donde entra su trabajo, anunciado con giros como «sin embargo». | **Clave** |
| ✗ | Las limitaciones del propio estudio y los datos que no se lograron conseguir, declarados desde el principio. | Los límites van en Conclusiones |
| ✗ | Los conceptos que todavía no se han definido, para anunciar que el marco teórico se encargará de definirlos. | «Vacío» no es pendiente de redacción |
| ✗ | Qué encontrará el lector en las páginas siguientes, sección por sección, para que sepa cómo está organizado. | Es el **propósito**, el sexto tramo |

> **Cita literal de la fuente** (deck de la Sesión 03, slide «La introducción es un embudo: de lo ancho a lo estrecho»):
> «**3. Vacío** — qué no se ha estudiado o resuelto todavía. **Es el hueco donde entra su trabajo.** Se enuncia con giros como "sin embargo", "no obstante", "aún no se ha documentado".»
> Ejemplo modelado de la misma sesión, párrafo 2: «En el área de TI de la organización estudiada, cada despliegue exige seis pasos manuales y toma en promedio 42 minutos. **No obstante, no existe un registro que documente el efecto de esa manualidad sobre los errores en producción.**»
> Los distractores salen de casillas vecinas del mismo material: «Conclusiones | Responder la pregunta, **límites y trabajo futuro**» (tabla de anatomía) y «**6. Propósito del artículo (lo estrecho)** — qué encontrará el lector en las siguientes páginas».

**Por qué funciona:** el distractor más fuerte es el del propósito, porque también pertenece al embudo. Distinguirlos exige haber entendido que el embudo va de lo ancho a lo estrecho y que el vacío está **antes** de la pregunta, no después de los objetivos.

---

### TG3-P1-05 · Qué pregunta responde la Fase I de referentes
*Sesión 04 · Antecedentes ≠ marco teórico ≠ estado del arte · 75 s*

**Enunciado:** La Sesión 04 separa tres cosas que suelen confundirse: los antecedentes o referentes, el marco teórico y el estado del arte. La **Fase I de referentes** que se trabajó ese día responde a una pregunta concreta. ¿A cuál?

| | Opción | |
|---|---|---|
| ✅ | ¿Quién más ha estudiado este problema y qué encontró? | **Clave** |
| ✗ | ¿Qué conceptos y teorías sostienen mi pregunta? | Es el **marco teórico** |
| ✗ | ¿Qué es lo más reciente y avanzado que existe hoy sobre el tema? | Es el **estado del arte** |
| ✗ | ¿Qué hueco deja la literatura y cómo lo llena mi propuesta? | Es el **vacío** de la introducción |

> **Cita literal de la fuente** (deck de la Sesión 04, `cun_tg3_s04.json`, tabla «Tres palabras que todo el mundo confunde»):
> «**Antecedentes / referentes** | ¿Quién más lo ha estudiado y qué encontró? | **Hoy — Fase I** | "Ramírez (2022) midió el efecto de automatizar pruebas en 3 equipos ágiles"»
> «**Marco teórico** | ¿Qué conceptos y teorías sostienen mi pregunta? | Se cierra más adelante en el curso»
> «**Estado del arte** | ¿Qué es lo más reciente y avanzado del tema? | Se alimenta durante todo el proceso»
> Nota de la misma tabla: «Hoy **NO** estamos construyendo el marco teórico. Estamos levantando el **mapa de quién ya caminó por aquí**.»

**Nota de alcance:** las etiquetas «marco teórico» y «estado del arte» aparecen en las opciones, pero **sí están dentro del alcance**: son las columnas de esta misma tabla de la Sesión 04 (y «marco teórico» está también en la anatomía de la S03). Lo que no entra es el **cierre** del marco teórico, que es la Sesión 08, y de eso no se pregunta nada.

---

### TG3-P1-06 · El campo de la ficha que decide si la fuente entra
*Sesión 04 · La ficha de cuatro campos · caso corto · 95 s*

**Enunciado:** Usted encontró un artículo muy citado, con autor, año y DOI. Lo leyó, escribió con sus palabras la idea principal y copió una cita textual con su página. Sin embargo, no logra escribir en una línea qué le aporta a **su** proyecto. Según el criterio de la Sesión 04, ¿qué hace con esa fuente?

| | Opción | |
|---|---|---|
| ✅ | La descarta en el momento: si no puede declarar el aporte a su proyecto, esa fuente no entra al artículo. | **Clave** |
| ✗ | La incluye igual: tener autor, año y DOI ya la hace trazable, y una fuente más nunca sobra en la lista. | Confunde trazabilidad con pertinencia |
| ✗ | Deja ese campo en blanco y lo completa más adelante, cuando ya se vea qué autores le sirven de verdad. | La ficha no admite campos en blanco |
| ✗ | Sustituye ese campo por el número de veces que la fuente ha sido citada, que es una medida más objetiva. | El «citado por» sirve para buscar, no para justificar |

> **Cita literal de la fuente** (deck de la Sesión 04, nota de la tabla «La ficha de lectura: el ladrillo de todo lo que viene»):
> «Nadie cita bien lo que no leyó. **Si usted no logra escribir la última fila de la ficha, esa fuente no entra a su artículo.**»
> Slide «Qué hace que una fuente sea un buen referente»: «**Aporte declarable:** usted puede escribir en una línea qué le aporta a **su** proyecto. **Si no puede escribir esa línea, la fuente sobra.**» · «**Pertinencia:** toca alguna de las variables de su pregunta. Si no la toca, **no entra, así sea un artículo famoso**.» · «Cantidad sin pertinencia no cuenta: 50 referencias de relleno pesan menos que 30 bien elegidas.»
> Nota del taller de la misma sesión: «Si una fuente no le deja escribir la cuarta fila de la ficha, **descártela en el momento** y busque otra. Descartar temprano es ganar tiempo.»

**Por qué funciona:** el enunciado da por resueltos los tres primeros campos **y** la lectura real de la fuente, de modo que la única cosa que falla es la cuarta fila. Sin ese cuidado, «vuelva a leerla» o «reescriba la idea con sus palabras» serían segundas respuestas defendibles.

---

### TG3-P1-07 · Mapa de diálogo: el autor que aporta método
*Sesión 04 · Las cuatro posturas del mapa · 85 s*

**Enunciado:** En el **mapa de diálogo** de la Sesión 04 los autores se agrupan por lo que hacen entre ellos. ¿Qué caracteriza a un autor que se clasifica como «**aporta método**»?

| | Opción | |
|---|---|---|
| ✅ | Que lo aprovechable no es su hallazgo sino cómo midió: de él se copia la lógica del instrumento, no el texto. | **Clave** |
| ✗ | Que su hallazgo coincide con el que usted espera encontrar, de modo que los dos se citan juntos en un paréntesis. | Es «**confirman**» |
| ✗ | Que lleva más lejos el hallazgo de otro autor o lo aplica a un contexto nuevo, más parecido al suyo. | Es «**extienden**» |
| ✗ | Que encuentra lo contrario de lo que reportan los demás, lo cual abre una tensión que vale la pena discutir. | Es «**contradicen**» |

> **Cita literal de la fuente** (deck de la Sesión 04, slide «El mapa de diálogo: los autores no se apilan, se ponen a conversar»):
> «**Confirman** — coinciden en el mismo hallazgo. Se citan juntos: (Ramírez, 2022; Pérez, 2021).» · «**Contradicen** — encuentran lo contrario. Es su mejor material: ahí hay una tensión que discutir.» · «**Extienden** — uno lleva más lejos lo del otro, o lo aplica a un contexto nuevo.» · «**Aportan método** — no le interesa su resultado, sino cómo midieron. Sirven para su metodología.»
> Tabla «Mapa de diálogo — ejemplo con cuatro autores»: «**Aportan método** | Pérez (2021) | Usó bitácora de despliegues durante 8 semanas | Copio la **lógica** del instrumento, no el texto».

**Por qué funciona:** las cuatro opciones son las cuatro posturas del mapa, descritas con las palabras de la sesión. No hay opción absurda: quien no estudió tiene cuatro descripciones igualmente razonables y ninguna pista sintáctica.

---

### TG3-P1-08 · El orden en que se llena la matriz de consistencia
*Sesión 05 · Las cinco columnas · 100 s*

**Enunciado:** La Sesión 05 insiste en un orden para llenar la **matriz de consistencia** y advierte que invertirlo es el error más caro del trabajo de grado. ¿Cuál es ese orden, y qué pasa si se empieza por el otro extremo?

| | Opción | |
|---|---|---|
| ✅ | Objetivo específico → variable → técnica → instrumento → análisis: empezar por el instrumento produce encuestas que no miden lo que se preguntó. | **Clave** |
| ✗ | Instrumento → variable → objetivo específico → técnica → análisis: conviene partir de lo que de verdad se puede aplicar en el tiempo disponible. | Es el orden que la sesión prohíbe |
| ✗ | Variable → objetivo específico → análisis → técnica → instrumento: primero se fija qué se va a medir y después para qué sirve medirlo. | La variable se **extrae** del objetivo |
| ✗ | Análisis → instrumento → técnica → variable → objetivo específico: se parte del tipo de tabla o gráfico que se quiere presentar. | El análisis es la última columna |

> **Cita literal de la fuente** (deck de la Sesión 05, `cun_tg3_s05.json`, slide «Cómo se construye la matriz: el orden importa»):
> «**No empiece por el instrumento.** Casi todo el mundo lo hace y por eso termina con encuestas que no miden nada. **Paso 1 — Copie sus objetivos específicos** en la primera columna (…) **Paso 2 — Extraiga la variable** que hay en cada objetivo (…) **Paso 3 — Elija la técnica** (…) **Paso 4 — Nombre el instrumento** concreto (…) **Paso 5 — Declare el análisis**».
> Nota de la tabla «La matriz de consistencia, fila por fila»: «Léala de izquierda a derecha: **qué quiero lograr → qué observo → cómo lo capturo → con qué herramienta → cómo lo interpreto**. Si una fila se corta a medio camino, ahí está el problema.»
> Y la regla de apertura de la sesión: «**el método no se elige, se deriva** de la pregunta y de los objetivos».
> El segundo distractor cita el error frecuente que la sesión desmonta: «"Elegí encuesta porque es lo más fácil." — El método se deriva de la pregunta y los objetivos, no de la comodidad.»

**Por qué funciona:** las cuatro opciones comparten la misma plantilla (una secuencia de cinco columnas + una justificación), así que la clave no es la opción impar. Adivinar exige recordar la secuencia, no detectar el formato distinto.

---

### TG3-P1-09 · Técnica e instrumento no son la misma cosa
*Sesión 05 · Forma de acercarse al dato vs. objeto que lo captura · caso corto · 90 s*

**Enunciado:** Un compañero le muestra una fila de su matriz de consistencia en la que la columna **técnica** dice «entrevista» y la columna **instrumento** también dice «entrevista». Según la Sesión 05, ¿qué está mal y cómo se arregla?

| | Opción | |
|---|---|---|
| ✅ | La técnica es la forma de acercarse al dato y el instrumento el objeto que lo captura: hay que nombrarlo concreto, «guía de entrevista de 8 preguntas». | **Clave** |
| ✗ | No está mal: cuando el acercamiento al dato es cualitativo, técnica e instrumento coinciden y basta con nombrarlos una vez. | La sesión no admite esa excepción |
| ✗ | Está mal el orden de las columnas: el instrumento va antes que la técnica, porque primero se elige la herramienta concreta y después la forma de aplicarla. | El problema no es el orden |
| ✗ | Lo que falta es el análisis: mientras la fila no diga cómo se interpretan los datos, distinguir técnica de instrumento es secundario. | El análisis es otra columna |

> **Cita literal de la fuente** (deck de la Sesión 05, slide «Cómo se construye la matriz: el orden importa»):
> «**Paso 3 — Elija la técnica**: observación, encuesta, entrevista, medición, prototipado, análisis documental. **La técnica es la forma de acercarse al dato; el instrumento es el objeto con el que lo captura.** **Paso 4 — Nombre el instrumento** concreto: "cuestionario de 10 ítems", "**guía de entrevista de 8 preguntas**", "bitácora de despliegues", "rúbrica del prototipo".»
> Checklist de autoevaluación de la misma sesión: «**Matriz:** ¿hay una fila por cada objetivo específico? ¿todas las celdas están llenas? **¿la técnica y el instrumento son cosas distintas y no la misma repetida?**»
> Tabla «Qué instrumento para qué necesidad»: «**Guía de entrevista** | Explicaciones y matices de pocas personas | **6 a 8 preguntas abiertas** | Convertirla en un interrogatorio cerrado».

**Por qué funciona:** el caso es el que el checklist de la sesión pregunta literalmente, así que el estudiante que usó el checklist lo reconoce de inmediato. El distractor del «orden» es tentador porque menciona una regla verdadera de la sesión (no empezar por el instrumento) aplicada al problema equivocado.

---

### TG3-P1-10 · El ítem huérfano del instrumento
*Sesión 05 · La regla dura: cada ítem responde a un objetivo · caso corto · 85 s*

**Enunciado:** Su bitácora de despliegues ya tiene tres campos, cada uno anotado con el objetivo al que responde. Se le ocurre agregar un cuarto: *«¿Le gusta trabajar en equipo?»*, porque le parece interesante. Según la **regla dura** de la Sesión 05, ¿qué se hace con ese ítem?

| | Opción | |
|---|---|---|
| ✅ | Se borra: ningún ítem entra porque suene interesante, sino porque un objetivo lo necesita. | **Clave** |
| ✗ | Se conserva al final del instrumento como campo de contexto: aporta información sobre el clima del equipo. | La excusa habitual del ítem huérfano |
| ✗ | Se conserva y se le asigna el objetivo más cercano, para que ninguna celda de la matriz quede vacía. | Falsifica la consistencia |
| ✗ | Se reformula como pregunta abierta, porque un ítem sin objetivo funciona mejor si no fuerza una escala. | Cambiar el formato no resuelve el fondo |

> **Cita literal de la fuente** (deck de la Sesión 05, slide «El instrumento: cada ítem responde a un objetivo»):
> «**Regla dura:** por cada pregunta o criterio de su instrumento, pregúntese **"¿a qué objetivo responde?"**. **Si no responde a ninguno, se borra. Sin discusión, sin lástima.**»
> Slide «Ejemplo modelado — de una fila de la matriz a los ítems»: «**Y ahora el ítem huérfano:** "¿Le gusta trabajar en equipo?". ¿A qué objetivo responde? A **ninguno**. Se borra. Así de simple. **Ese es el estándar:** ningún ítem entra porque "suena interesante"; entra porque un objetivo lo necesita.»
> Criterio de éxito del taller: «**No queda ningún ítem huérfano**: todos tienen anotado al frente el objetivo que responden.»

**Por qué funciona:** el ítem del enunciado es **el mismo** que el docente descarta en pantalla durante la modelación de la sesión, así que quien estuvo en clase lo reconoce. Los tres distractores son las tres racionalizaciones reales con las que los estudiantes salvan ítems huérfanos: llamarlo «de contexto», forzarle un objetivo o cambiarle el formato.

---

## 3. Notas para el Docente

1. **Cabe con holgura.** 15 minutos estimados contra los 22 reservados en la Sesión 06. Es el margen más ajustado de los cinco cuestionarios del curso porque la S06 es «la sesión más recortada» (Manual §1.2), así que conviene abrir el aula puntual y no gastar los primeros minutos en avisos.
2. **Un solo banco, tres aulas.** La categoría es `Parcial 1 - TG3 S01-S05`, sin número de grupo: se importa igual en 112321, 116387 y 129270. Recuerde el aviso del Manual §4.1: los documentos de `Recursos/ACAs/` imprimen como aula oficial la 112321 (54450), así que el estudiante del 54466 o del 54467 que haga clic en la guía aterriza en un aula ajena. Eso no afecta al banco, pero sí a la guía de estudio que el estudiante lee antes.
3. **Sustituya los slots.** Las aulas CUN traen los cuestionarios con slots aleatorios que sacan preguntas de su propia categoría: importar el banco no basta. Después de importar hay que sustituir los slots para que el cuestionario sirva estas 10 preguntas (`config/moodle/cdigital.py`, subcomandos `actividad` / `sustituir_slots`).
4. **Desajuste que vale registrar.** La guía del estudiante (`Parcial 1 (24%) - guia del cuestionario.docx`, §5) enumera lo que hay que estudiar por sesión y en la S04 dice: *«Ten claro qué es un referente (Fase I) y cómo se elige: pertinencia, vigencia y relación con tu pregunta»*. El deck de la S04 tiene **cinco** criterios, no tres: pertinencia, trazabilidad, vigencia, verificabilidad y aporte declarable. El banco usa los del deck (que es la fuente de autoridad 2) y las preguntas 06 y 05 se apoyan en pertinencia, trazabilidad y aporte declarable. Si quiere alinear la guía, hay que agregarle trazabilidad y verificabilidad; si no, ningún estudiante queda en desventaja, porque la guía manda estudiar el deck de cada sesión.
5. **Reparto acordado con el Quiz 1 (auditoría del 15/08/2026).** El Quiz 1 ya existe y comparte dos fuentes con este banco: la lectura de la S01 y el deck de la S02. Una revisión adversarial encontró que las preguntas 01 y 02 originales de este Parcial repetían casi literalmente TG3-Q1-03 (definición de las restricciones) y TG3-Q1-07 (la pieza que le falta a una pregunta de investigación), de modo que un estudiante habría visto el mismo ítem dos veces con tres semanas de diferencia. Se reescribieron las dos de **este** banco —no las del Quiz 1, que se aplica primero y funciona como diagnóstico— y se movieron a subtemas que el Quiz 1 no toca: el momento en que entran las **operaciones** (P1-01) y el **orden** de los objetivos específicos (P1-02). El reparto vigente es: **Quiz 1** se queda con los cuatro componentes en lista, la definición de restricciones, las interrogantes-guía y las cuatro piezas de la pregunta; **Parcial 1** se queda con las operaciones y con los objetivos específicos. El artículo todavía tiene material sin usar en ninguno de los dos bancos —las **tres partes** del texto de problema-solución (antecedentes y situación actual · problematización · aproximación al propósito) y las dos tablas de autorrevisión— por si hay que sustituir alguna pregunta más adelante.
6. **Vocabulario vigilado.** Ninguna opción nombra co-creación, comunidades de práctica, hallazgos, tesauro UNESCO, póster, antiplagio, sustentación ni repositorio. La única concesión es nombrar *Resultados* y *Discusión* como casillas del esqueleto en la pregunta 03, lo cual está publicado desde la Sesión 03 (tabla de anatomía) y por tanto dentro de la ventana.
7. **Sin excepción administrativa.** El encargo permite hasta 2 preguntas de método del curso cuando el alcance no tiene material temático. Aquí no se usó: hay cuatro decks completos y una lectura obligatoria. Las 10 son de tema.
8. **Retroalimentación.** El `<generalfeedback>` de cada pregunta trae la cita literal de la fuente, así que el estudiante que revise su intento después del cierre encuentra dónde estaba escrito. Eso cubre la exigencia de «calificación con retroalimentación» antes del 22/09 (Manual, Parte 2) sin trabajo adicional por estudiante.
