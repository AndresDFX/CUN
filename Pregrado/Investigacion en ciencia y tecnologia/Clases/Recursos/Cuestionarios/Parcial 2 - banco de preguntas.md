# Parcial 2 — banco de preguntas · INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA (EI005)

Gemelo legible del archivo `Parcial 2 - banco de preguntas (Moodle XML).xml`. **El maestro es el XML**: si algo se corrige, se corrige allá y se refleja aquí. En cada edición del curso el banco se reimporta; no se reescribe.

| Dato | Valor |
| :--- | :--- |
| Ítem del aula | **Parcial 2** · Cuestionario · **21 %** de la nota (corte 2) |
| Aula CDigital | `111070` — <https://cdigital.cun.edu.co/course/view.php?id=111070> |
| Ventana | apertura 04/09/2026 · cierre 10/09/2026 · nota docente 17/09/2026 |
| Categoría en el banco | `$course$/Parcial 2 - Investigacion S01-S04` (sin número de grupo: el banco sirve para varias aulas) |
| Formato | 10 preguntas de selección única, 4 opciones, retroalimentación por opción |
| Validado con | `python config/moodle/cdigital.py importar "…" --curso 111070 --simular` → «10 preguntas» · «validación local: sin problemas» (última corrida: 15/08/2026, tras la revisión cruzada de los cinco bancos del curso) |

## Alcance (lo fija el Manual del Docente, no este documento)

**Entra** —es acumulativo—:

- **Lectura autónoma de la Sesión 01** (U1–U2: producto final del curso y fundamentos del método científico). Lectura obligatoria: Casares-Salazar, R., González-Herrera, R. A. y Quintal-Franco, C. A. (2019). *Cómo organizar eficientemente un documento científico*. Ingeniería, 23(1), 21-35.
- **Sesión 02** (20/08) — MinCiencias · SNCTI · 6 líneas de Ingeniería · elección de línea.
- **Sesión 03** (27/08) — primer avance: título, introducción en tres párrafos, tipos de conocimiento, tipos de fuente.
- **Sesión 04** (03/09) — problema y pregunta (espina de pescado, árbol de problemas, método 3D); bases de datos, operadores de búsqueda, filtro de fuentes y citación en APA 7 con ZoteroBib.

**No entra:** la **Sesión 05** (10/09), que se dicta el mismo día en que cierra el cuestionario. Queda fuera todo su vocabulario: planteamiento del problema y su estructura de embudo, sus seis componentes, constructos, posturas teóricas, fichas de lectura, matriz de fuentes y la revisión de literatura como método de trabajo. Ese temario entra en el **Quiz 3**.

> Fuente del recorte — *Manual del Docente*, tabla «Los cuestionarios»: «**Parcial 2** (21%) | Añade la **S04** (problema, causas, pregunta, bases de datos, APA 7). | Que diferencie deseo de producto y problema de investigación, y que sepa buscar y citar.» Y la guía del estudiante: «Lo que NO entra: la Sesión 05 (10/09/2026 …) se dicta el mismo día en que cierra el cuestionario, así que su tema queda fuera».

**Reparto de las 10 preguntas:** Sesión 04 → **9** · Sesión 03 → **1**. La lectura obligatoria de la Sesión 01 respalda además la pregunta de citas y referencias (INV-P2-05), junto con el deck de la S04.

El peso cae donde el Manual lo pone: la S04 es la sesión que este ítem añade y es donde está lo que el Manual manda revisar aquí —diferenciar deseo de producto y problema de investigación, y saber buscar y citar—. Lo de las Sesiones 01 y 02 ya se evaluó en los ítems del corte 1 y en el Quiz 2, y vuelve en el Quiz 3.

Las 10 son de **tema**; ninguna pregunta por pesos, fechas, créditos, canal de entrega, reglas de IA ni mecánica del cuestionario. **Preguntas de administración del curso: 0.**

---

## INV-P2-01 · Problema de investigación frente a deseo de producto — Sesión 04

**Enunciado.** Un compañero le pide revisar el arranque de su documento. De las cuatro formulaciones que escribió, ¿cuál corresponde a un **problema de investigación** según el criterio de la Sesión 04?

- ✅ Las fallas de los equipos del laboratorio se anotan en un cuaderno y no se sabe cuánto tardan en atenderse ni cuántas prácticas quedan incompletas.
- ❌ El programa necesita una aplicación móvil que permita reportar en línea las fallas… → deseo de producto.
- ❌ El mantenimiento predictivo de equipos de laboratorio con inteligencia artificial en las universidades colombianas… → tema, no problema.
- ❌ A los estudiantes de la franja de la noche les molesta que los equipos se dañen tan seguido… → molestia sin consecuencias verificables.

**Cita literal de la fuente** (`config/slides/content/cun_investigacion_s04.json`, slide «Qué es (y qué no es) un problema de investigación»):

> «**Es** un hecho que se puede **observar, describir o medir** en un lugar y un tiempo concretos. Tiene **afectados**: alguien pierde algo (tiempo, dinero, calidad, oportunidades). […] **No es** la ausencia de su solución favorita. **No es** un tema ("la inteligencia artificial" es un tema, no un problema). **No es** una molestia personal sin consecuencias verificables. […] Prueba de control: pregúntese **"¿qué duele hoy, si mi solución nunca existiera?"**. La respuesta es su problema.»

*Por qué así:* los tres distractores no comparten plantilla sintáctica —evitan el «falta / no existe / hay que» que delataría la clave— y cada uno encarna uno de los tres «No es» de la slide.

---

## INV-P2-02 · Espina de pescado con todas las causas en una sola familia — Sesión 04

**Enunciado.** Usted dibuja la espina de pescado de su problema y, al terminar, las siete causas quedaron colgadas de la familia **tecnología**: personas, proceso y entorno están vacías. ¿Qué indica eso?

- ✅ Que todavía no abrió el problema: repitió su hipótesis inicial. Se esperan al menos tres familias con una causa concreta cada una.
- ❌ Que el problema es técnico y concentrar las causas demuestra foco.
- ❌ Que la herramienta no sirve y conviene cambiarla por el método 3D.
- ❌ Que faltan causas en las otras familias, aunque sean adjetivos generales.

**Cita literal** (deck S04, slide «Espina de pescado: abrir familias de causas»):

> «Regla práctica: **mínimo tres familias con al menos una causa cada una**. Si todo le cabe en una sola familia, no ha abierto el problema: ha repetido su hipótesis.»

Y, en la misma slide: «En cada espina se cuelgan **causas concretas**, no adjetivos: "faltan tutores" es vago; "un tutor por cada 45 estudiantes" es una causa.» — es lo que hace fallar al cuarto distractor.

---

## INV-P2-03 · Reformular una pregunta que se responde con sí o no — Sesión 04

**Enunciado.** Su pregunta dice: «¿Existe deserción en el programa de Ingeniería?». ¿Cuál reformulación la vuelve investigable?

- ✅ ¿Qué factores académicos anteceden la deserción en los dos primeros semestres del programa de Ingeniería de la sede X?
- ❌ ¿Es la deserción… tan grave como en el resto de los programas del país? → sigue siendo sí/no.
- ❌ ¿Cómo diseñar un tablero que muestre las cifras de deserción? → pregunta de diseño.
- ❌ ¿Cuál es la mejor estrategia para reducir la deserción…? → «mejor» sin criterio.

**Cita literal** (deck S04, tabla «Preguntas mal formuladas y su reformulación»):

> «"¿Existe deserción en el programa?" — Sí/no; además ya se sabe la respuesta — "¿Qué factores académicos anteceden la deserción en los dos primeros semestres del programa X?"»
>
> Nota de la tabla: «Patrón de la corrección: **agregar actor y lugar**, y cambiar el verbo de apertura por *qué*, *cómo* o *en qué medida*.»

Complementa la tabla «Anatomía de una pregunta investigable» (clara · delimitada · viable · relevante · abierta), de la misma sesión.

---

## INV-P2-04 · Operador que cubre dos términos equivalentes — Sesión 04

**Enunciado.** Su pregunta usa «correo malicioso», pero la literatura lo llama «phishing», y quiere que una sola búsqueda recupere los dos términos. ¿Qué operador usa y cómo se escribe?

- ✅ OR, que amplía porque sirve cualquiera de los dos: `phishing OR "correo malicioso"`.
- ❌ AND: exige que aparezcan ambos, así que reduce.
- ❌ Comillas: piden la frase exacta en ese orden.
- ❌ Signo menos: excluye el término.

**Cita literal** (deck S04, tabla «Operadores de búsqueda que ahorran horas»):

> «**OR** — Amplía: sirve cualquiera de los dos (útil para sinónimos) — `phishing OR "correo malicioso"`»
>
> «**AND** — Exige que aparezcan **ambos** términos»; «**Comillas** — Busca la **frase exacta**, en ese orden»; «**Signo menos** — **Excluye** un término que le ensucia los resultados».

*Por qué así:* los cuatro distractores son operadores reales de la misma tabla, atribuidos a la función equivocada. Quien no estudió reconoce el operador pero no su efecto.

---

## INV-P2-05 · Cita en el texto y referencia final al parafrasear — Sesión 04

**Enunciado.** Usted parafrasea, con sus propias palabras, una idea de un artículo que abrió y leyó. ¿Cómo debe quedar eso en su documento?

- ✅ Cita (Apellido, año) en el cuerpo del texto **y** ficha completa bajo «Referencias», en orden alfabético.
- ❌ Solo la ficha final: al reescribir con sus palabras ya no hace falta marcar la fuente.
- ❌ Solo la cita en el texto: la ficha completa se reserva para las citas textuales.
- ❌ El enlace pegado en el párrafo, sin listado final.

**Citas literales.** Deck S04, slide «Paso a paso: citar en APA 7 con ZoteroBib»:

> «**6.** *Copy to clipboard* y pegue en su documento, bajo **Referencias**, en **orden alfabético**. **7.** En el cuerpo del texto cite **(Apellido, año)**; para cita textual agregue la página: **(Apellido, año, p. 12)**.»
>
> Nota de la misma slide: «Cada referencia del listado debe estar citada en el texto, y cada cita del texto debe estar en el listado.»

Lectura obligatoria (Casares-Salazar et al., 2019, «Las referencias»):

> «Es una práctica de la investigación citar las fuentes de información ajenas al autor del trabajo en el caso de los enunciados que no son del conocimiento común. De lo contrario, se trataría de un plagio, y esto es una falta grave de ética. Esto incluye enunciados o conceptos copiados textualmente, o bien que sean parafraseados, así como datos obtenidos de otras fuentes.»

---

## INV-P2-06 · Clasificar una afirmación por tipo de conocimiento — Sesión 03

**Enunciado.** En su documento un compañero escribe: «el registro de la mesa de ayuda documenta 47 incidentes de conexión durante marzo, con la hora y la duración de cada uno». Según la tabla de tipos de conocimiento de la Sesión 03, ¿qué tipo de conocimiento es y qué puede hacer con él?

- ✅ Científico: hay medición y evidencia documentada que otra persona puede verificar, de modo que sí sirve para sostener el artículo.
- ❌ Empírico: aunque el registro exista, sigue siendo una observación hecha dentro de la propia institución… → el criterio no es de quién es el escenario observado.
- ❌ Cotidiano: recoge la experiencia de quienes usan el servicio a diario… → un registro con 47 casos fechados no es una impresión personal.
- ❌ Científico, pero solo si ese registro llega a publicarse en una revista… → añade una condición que la tabla no pone.

**Cita literal** (`cun_investigacion_s03.json`, tabla «Tipos de conocimiento (esto suele caer en el parcial)»):

> «**Científico** — Con método, medición y evidencia documentada — ¿Se verifica? Sí, por otros — "La bitácora registra 12 caídas en un mes" — ¿Sostiene el artículo? Sí»
>
> Nota de la tabla: «La diferencia entre empírico y científico no es la verdad: es que el científico **se puede verificar y repetir** porque quedó registrado el cómo.»

*Por qué así:* dos opciones dicen «científico» y se separan por una condición inventada (estar publicado), así que reconocer la etiqueta no alcanza. El escenario —un registro con hora y duración por incidente— es **distinto** del que usa el Quiz 2 en INV-Q2-07 («llevo un año y siempre se cae la red a las 3 p. m.»), que es el caso empírico de la misma tabla. El estudiante no ve dos veces la misma pregunta: ve las dos filas contrarias de la tabla, en dos cortes distintos, y la nota que las separa es lo que se evalúa.

---

## INV-P2-07 · Árbol de problemas: distinguir una causa de un efecto — Sesión 04

**Enunciado.** Está armando el árbol de problemas de su caso y tiene dos hechos anotados: «los equipos del laboratorio tienen ocho años» y «los grupos deben repetir la práctica en otra franja». Según la Sesión 04, ¿dónde va cada uno y con qué pregunta se decide?

- ✅ La antigüedad de los equipos es causa y va en las raíces; repetir la práctica es efecto y va en las ramas. Lo deciden «¿por qué ocurre?» y «¿qué provoca esto?».
- ❌ Al revés: la antigüedad es el efecto de las ramas y repetir la práctica es la causa de las raíces. → invierte el árbol.
- ❌ Los dos son causas y van juntos en las raíces, porque ambos son hechos observables y verificables. → ser observable no convierte un hecho en causa.
- ❌ Ninguno entra en el árbol: en raíces y ramas solo se escriben cifras. → restricción que la sesión no pone.

**Citas literales** (deck S04). Slide del árbol de problemas:

> «**Raíces** = causas. Se llega a ellas preguntando **"¿por qué ocurre?"** · **Tronco** = el problema central, en una sola frase. · **Ramas** = efectos. Se llega a ellos preguntando **"¿qué provoca esto?"**»

Y en los errores frecuentes de la misma sesión:

> «**Confundir causas con efectos.** Dos preguntas distintas las separan: *¿por qué ocurre?* señala una **causa**; *¿qué provoca esto?* señala un **efecto**. En el árbol: causas abajo, efectos arriba.»

*Por qué así:* el distractor invertido es el error que la propia sesión nombra como frecuente, así que la pregunta discrimina justo donde el material advierte. La clave no es la más larga: las cuatro opciones quedan entre 24 y 30 palabras.

---

## INV-P2-08 · Los tres movimientos del método 3D — Sesión 04

**Enunciado.** Su tema quedó demasiado grande y la Sesión 04 propone el método **3D** para bajarlo a escala. ¿En qué consisten sus tres movimientos?

- ✅ Describir qué pasa exactamente sin adjetivos, dimensionar cuánto, a cuántos y cada cuánto, y decidir qué parte puede estudiar este periodo.
- ❌ Diagnosticar el estado actual, diseñar la solución y desplegarla para comprobar si el problema quedó resuelto. → ciclo de proyecto, y vuelve a poner la solución en el centro.
- ❌ Definir el tema en una frase, dibujar el diagrama de causas y documentar las fuentes que va a citar. → mezcla tres tareas del taller y las llama 3D.
- ❌ Delimitar por área de conocimiento, por año de publicación y por país. → confunde acotar el problema con filtrar la búsqueda.

**Cita literal** (deck S04, slide del método 3D):

> «**Método 3D** — para temas demasiado grandes, tres movimientos: **Describir:** ¿qué pasa exactamente? Escríbalo sin adjetivos, como si narrara una escena. **Dimensionar:** ¿cuánto, a cuántos, cada cuánto, desde cuándo? Aquí entran las cifras. **Decidir:** de todo lo anterior, ¿qué parte puedo estudiar **este periodo** con las fuentes que tengo?»

Y en la slide siguiente: «El 3D es el mejor antídoto contra la pregunta planetaria: obliga a bajar a escala.»

*Por qué así:* los tres distractores son ternas de verbos con D que suenan igual de plausibles (diagnosticar-diseñar-desplegar es el reflejo del ingeniero), de modo que recordar la letra inicial no basta: hay que saber qué hace cada movimiento.

---

## INV-P2-09 · Buscador académico, base de datos y gestor de citas — Sesión 04

**Enunciado.** Un compañero afirma que da igual entrar por Google Académico, por SciELO o por ZoteroBib, «porque los tres sirven para encontrar artículos». Según la Sesión 04, ¿qué hay que corregirle?

- ✅ Que Google Académico es un buscador amplio que mezcla calidades, SciELO es una base de datos con texto completo y ZoteroBib no busca nada: arma la referencia.
- ❌ Que solo cambia la cobertura: los tres buscan, pero indexan cantidades distintas de títulos. → acepta la premisa falsa.
- ❌ Que el orden importa: primero ZoteroBib, que reúne las bases suscritas, y después Google Académico. → le atribuye a ZoteroBib el papel de la biblioteca CUN.
- ❌ Que tiene razón, aunque conviene instalar Zotero de escritorio. → la sesión pide expresamente lo contrario.

**Citas literales** (deck S04). Slide «Tres nombres que hay que separar desde ya»:

> «**Buscador académico** (Google Académico): rastrea muchísimo, pero mezcla calidades. **Base de datos** (SciELO, Redalyc, las suscritas por la CUN): colecciones curadas, con texto completo. **Gestor de citas** (ZoteroBib): no busca nada; **arma la referencia** en el formato correcto.»

Y la tabla comparativa de la misma sesión:

> «ZoteroBib (zbib.org) — Generador de citas en línea — APA 7 al instante, sin instalar ni registrarse — No guarda su biblioteca: copie lo que genere.»

*Por qué así:* la confusión entre las tres herramientas es la que hace perder más tiempo en el taller. La pregunta es de vocabulario técnico de la S04 y no de formato de la cita: ninguna opción pide reconocer la puntuación de una referencia APA.

---

## INV-P2-10 · El filtro de 60 segundos: en qué orden se lee — Sesión 04

**Enunciado.** Tiene ocho resultados de búsqueda abiertos y poco tiempo para decidir con cuáles se queda. Según el **filtro de 60 segundos** de la Sesión 04, ¿en qué orden recorre cada documento y qué límite tiene esa lectura rápida?

- ✅ Título, resumen, conclusiones y método; y si solo leyó el resumen, no puede citar el interior del artículo.
- ❌ Título, introducción y bibliografía; y con el resumen ya puede citar cualquier parte del artículo. → invierte la advertencia de la sesión.
- ❌ En el orden en que está escrito —método, resultados, discusión y conclusiones—. → gasta el minuto en lo más denso.
- ❌ Primero el número de veces que aparece en «citado por»; si supera a los demás, no hace falta abrirlo. → «citado por» no reemplaza la lectura.

**Cita literal** (deck S04, «El filtro de 60 segundos: ¿me quedo con esta fuente?»):

> «Truco de lectura rápida, en este orden: **título → resumen → conclusiones → método**. Con eso decide en un minuto si vale la pena leer el artículo completo. Y una advertencia de honestidad: **si solo leyó el resumen, no cite el interior del artículo**.»

*Por qué así:* cierra el banco con la operación que el estudiante repite más veces durante la semana. Dos distractores ofrecen atajos para no leer —el resumen y el contador de citas—, que son los dos atajos reales que se toman en el taller.

---

## Notas para el Docente

1. **El caso modelado del curso se reutiliza a propósito.** El laboratorio de redes, la bitácora y la retroalimentación tardía aparecen en los decks de la S03, S04 y S05; el banco usa variantes de ese mismo caso para que el estudiante reconozca el terreno y el examen mida el concepto, no la lectura de un contexto nuevo. Ninguna variante requiere la S05.
2. **Vocabulario de la S05 excluido a mano.** Se revisó que ninguna opción nombre embudo, seis componentes del planteamiento, constructos, posturas teóricas, fichas de lectura ni matriz de fuentes. La palabra «discusión» aparece una sola vez, en un distractor de INV-P2-10 que enumera el orden de imprenta de un artículo (método, resultados, discusión, conclusiones): eso es el formato IMRyD de la lectura obligatoria de la S01, que sí está publicado dentro de la ventana. La palabra «vacío» ya no aparece en ninguna pregunta de este banco.
3. **Solape con el Quiz 2, resuelto.** El Quiz 2 (cerrado el 03/09) cubre hasta la S03, así que el riesgo real era repetir ítem entre cortes. Aquí solo una pregunta es de la S03 —tipos de conocimiento, que el propio deck marca como «esto suele caer en el parcial»— y usa **la fila contraria** de la tabla: el Quiz 2 pregunta por el caso empírico («llevo un año y siempre se cae la red a las 3 p. m.») y este banco por el caso científico (registro de la mesa de ayuda con 47 incidentes fechados). Enunciado, clave y opciones son distintos. Ninguna otra pregunta de este banco comparte caso con otro banco del curso.
4. **Tipos de fuente (primaria / secundaria / terciaria) quedó fuera a propósito.** Está en el alcance —es S03— pero es lo que el Manual asigna al Quiz 2 («que sepa qué va en un avance y qué es una fuente confiable»), y allí se evalúa (INV-Q2-08). En la S04 el mismo criterio reaparece como «filtro de 60 segundos», y esa es la forma en que sí entra aquí (INV-P2-10). Si usted quiere subir a 12 preguntas, los primeros temas a agregar son el checklist de las cinco cosas que se revisan antes de descargar una fuente y la conversión de la pregunta en términos de búsqueda.
5. **Desajuste con lo que el ítem promete.** El Manual dice que el Parcial 2 revisa «que diferencie deseo de producto y problema de investigación, y que sepa buscar y citar». El banco cubre las tres cosas (INV-P2-01, INV-P2-04, INV-P2-05), pero conviene saber que **la mitad del alcance del ítem es material que el estudiante vio una sola vez y a las carreras**: la S04 es sesión doble con Quiz 2 encima (20 min de contenido para dos unidades) y el propio Manual advierte que «el deck completo es el material de estudio de la semana; en clase se proyecta lo priorizado». Si el grupo rinde mal en las preguntas de búsqueda y citación, la causa probable es esa y no el banco.
6. **Sin preguntas de administración del curso.** No hay ítems sobre pesos, ventanas, créditos, canal de entrega, plantilla, reglas de IA ni mecánica del cuestionario. No se usó la excepción de las dos preguntas de método del curso: el deck de la S04 solo tenía material temático de sobra.
7. **Nueve de diez son de la S04, y eso es deliberado.** El banco anterior repartía las preguntas entre las cuatro sesiones del alcance acumulado y terminaba repitiendo, con otras palabras, preguntas que el estudiante ya había respondido en el Quiz 1, el Parcial 1 y el Quiz 2 (metodología, resultados frente a discusión, el caso de las dos líneas de Ingeniería). Se concentró el peso en la sesión que este ítem añade, que es además donde el Manual pone el aprendizaje a verificar. **Consecuencia que conviene tener presente:** si un estudiante no asistió a la S04, este parcial le va a resultar muy duro, y el material de recuperación es el deck completo de esa sesión. Si usted prefiere repartir, la vía sin repetir es cambiar INV-P2-08 o INV-P2-09 por preguntas de la S02 con casos nuevos —no con el de «seguridad informática», que ya vive en INV-P1-10—.
8. **Al crear la actividad en CDigital.** El aula ya trae seis cuestionarios abiertos con slots aleatorios: importar el banco no basta, hay que **sustituir los slots** por las 10 preguntas de esta categoría. La ruta es `quiz-sustituir` del mismo script, y sin `--confirmar` solo simula.
