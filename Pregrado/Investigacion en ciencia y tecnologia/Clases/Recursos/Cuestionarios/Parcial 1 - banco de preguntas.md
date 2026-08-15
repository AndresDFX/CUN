# Parcial 1 (24%) · Banco de preguntas — Investigación, Ciencia y Tecnología

**Curso:** INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA PARA LA ESCUELA DE INGENIERÍAS · SIAC **EI005** · CUN · 2026
**Aula:** CDigital (curso **111070**) · **Docente:** Julián Andrés Castaño Erazo
**Ítem:** Parcial 1 · Cuestionario · **24% de la nota del curso** · **Corte 1**
**Ventana:** 21/08/2026 a 27/08/2026 · se aplica **dentro del encuentro de la Sesión 03**, en unos **22 minutos**
**Formato:** selección única, 4 opciones, retroalimentación por opción. Es el ítem más pesado del corte 1, así que aquí sí se usa el formato tipo ICFES/SABER PRO: **seis de las diez preguntas son casos cortos** de aplicación (02, 03, 04, 06 y 08, y en parte 10), no reconocimiento de definiciones.

**Archivo importable:** `Parcial 1 - banco de preguntas (Moodle XML).xml` (categoría `$course$/Parcial 1 - Investigacion U1-U4`).
**Validado:** `python config/moodle/cdigital.py importar "…" --curso 111070 --simular` → *10 preguntas · validación local: sin problemas*. Última corrida: 15/08/2026, tras la revisión cruzada de los cinco bancos del curso. El aula no se tocó.

---

## 1. El alcance, y de dónde sale

El alcance lo fija el **Manual del Docente** (§7, tabla «Qué entra / qué revisas») y lo repite palabra por palabra la guía del estudiante `Clases/Recursos/ACAs/Parcial 1 (24%) - guia del cuestionario.docx`.

| Entra | No entra |
|---|---|
| **Lectura autónoma de la Sesión 01** — U1 (presentación del Syllabus y producto final: el artículo de nuevo conocimiento) y **U2** (fundamentos del método científico y sus etapas), con su **lectura obligatoria** de 15 páginas. | **Sesión 03** (27/08) — se dicta el mismo día en que cierra el cuestionario. Regla del Manual: «lo que se dicta el mismo día del cierre **no** entra». |
| **Sesión 02** (20/08) — U4: MinCiencias, el Sistema Nacional de CTeI, las **6 líneas de Ingeniería** del programa y la elección de línea. | **Sesión 04, 05 y 06** — nada de su vocabulario aparece, ni siquiera como distractor. |

Cita literal del Manual (§7): «**Parcial 1** (24%) | Añade la **S02** (MinCiencias, SNCTI, 6 líneas). | Que distinga las 6 líneas y ubique su tema en una. Es el ítem más pesado del corte 1: prepáralo con tiempo.»
Cita literal de la guía del estudiante: «Lo que NO entra: la Sesión 03 (27/08/2026 — Prueba parcial · 1.er avance del artículo) se dicta el mismo día en que cierra el cuestionario, así que su tema queda fuera: no se te pregunta algo que todavía no has visto en clase.»

> **La numeración de unidades del Syllabus salta el N° 3 y el N° 9.** Por eso el nombre de la categoría, `Parcial 1 - Investigacion U1-U4`, cubre exactamente U1, U2 y U4 — no hay una U3 que quedara dentro por error.

### Vocabulario que quedó prohibido (y no aparece ni en las opciones)

De la **S03**: tipos de conocimiento (cotidiano / empírico / científico), tipos de fuente (primaria, secundaria, terciaria), la fórmula del título de esa sesión, la introducción en tres párrafos, ZoteroBib.
De la **S04**: espina de pescado, árbol de problemas, método 3D, formulación de la pregunta de investigación, EBSCO, SciELO, Redalyc, Latindex, operadores de búsqueda, APA 7.
De la **S05**: planteamiento del problema, posturas teóricas, matriz de fuentes, revisión de literatura.

Dos matices, para que nadie los lea como fuga:

- **«Marco teórico» y «antecedentes» sí aparecen** (INV-P1-06 y INV-P1-10). No son de la S05: la **S02** los nombra literalmente al explicar que la línea condiciona el artículo («Cambia el marco teórico (qué conceptos hay que definir). Cambian los antecedentes (qué autores son referencia obligada)»), y la **lectura obligatoria** dedica un apartado al marco teórico o conceptual. No se pregunta *cómo escribirlo* —eso es S05—, se pregunta que la línea lo determina.
- **«Estado del arte» aparece una vez, en un distractor de INV-P1-05**, y sale de la **lectura obligatoria** publicada el 13/08, dentro de la ventana («Dicho vacío se puede identificar al elaborar el estado del arte»). No hace falta la S05 para descartarlo: basta saber qué partes tiene la Discusión.
- **Las cinco preguntas de la lectura obligatoria son las cinco secciones que ningún otro banco del curso toca**: palabras clave, autores, conclusiones, metodología aplicada y las tres partes de la Discusión. Las etapas del método, IMRyD, el vacío, el resumen, la introducción, el título y la frontera Resultados/Discusión se evalúan en el Quiz 1, que es el ítem diagnóstico de esa misma lectura; repetirlas aquí habría hecho que el estudiante viera dos veces la misma pregunta.

### Fuentes usadas, con su ruta

1. `Manual del Docente - Investigacion Ciencia y Tecnologia.md` — alcance, ventana y peso.
2. `Clases/Recursos/ACAs/Parcial 1 (24%) - guia del cuestionario.docx` — el recorte prometido al estudiante.
3. `config/slides/content/cun_investigacion_s01.json` y `…_s02.json` — los dos decks en alcance.
4. `Clases/Sesion 01 - …/Lectura autonoma - Sesion 01.txt` — la consigna de la lectura.
5. `Clases/Sesion 01 - …/Lectura autonoma - Organizar un documento cientifico (Casares 2019).pdf` — **lectura obligatoria**. Casares-Salazar, R., González-Herrera, R. A. y Quintal-Franco, C. A. (2019). Cómo organizar eficientemente un documento científico. *Ingeniería*, 23(1), 21-35. Acceso abierto, CC BY-NC 4.0.
6. `INVESTIGACION CIENCIA Y TECNOLOGIA PARA ESCUELA DE INGENIERIAS EI005_PRES.docx` — Syllabus SIAC, tabla «Unidades de conocimiento» (se usó para fijar el alcance de U1, U2 y U4; ninguna pregunta de este banco se responde con él, porque las cuatro etapas del método se preguntan en el Quiz 1).
7. `Guiones/Sesion 02 - ….md` — guion docente, para confirmar qué se dijo en voz alta sobre MinCiencias y el SNCTI.

**No se usó** la lectura *complementaria* (Cienfuegos 2019, «Reflexiones en torno al método científico y sus etapas»), porque la consigna la marca como **opcional**: ninguna pregunta la necesita.

---

## 2. Reparto: 10 de 10 son de tema

| # | Nombre | Unidad | Fuente | Tipo | Seg. |
|---|--------|--------|--------|------|------|
| 1 | INV-P1-01 Para qué sirven las palabras clave | U1-U2 | Lectura obligatoria | Concepto / para qué sirve | 70 |
| 2 | INV-P1-02 Quiénes entran en la lista de autores | U1-U2 | Lectura obligatoria | **Caso corto** | 90 |
| 3 | INV-P1-03 Qué va y qué no va en las conclusiones | U1-U2 | Lectura obligatoria | **Caso corto** | 85 |
| 4 | INV-P1-04 Para qué sirve la sección de metodología | U1-U2 | Lectura obligatoria | **Caso corto** | 90 |
| 5 | INV-P1-05 Las tres partes de la Discusión | U1-U2 | Lectura obligatoria | Taxonomía / orden | 80 |
| 6 | INV-P1-06 «Mi tema no cabe en ninguna línea» | U4 | Deck S02 | **Caso corto** | 75 |
| 7 | INV-P1-07 Qué es MinCiencias y para qué le sirve al artículo | U4 | Deck S02 + guion S02 | Concepto / qué NO es | 70 |
| 8 | INV-P1-08 Ubicar un caso en una de las 6 líneas | U4 | Deck S02 | **Caso corto** | 85 |
| 9 | INV-P1-09 Los tres criterios para elegir la línea | U4 | Deck S02 | Criterios técnicos | 80 |
| 10 | INV-P1-10 Consecuencia de elegir una línea u otra | U4 | Deck S02 | Aplicación | 80 |

**Total estimado: 805 segundos ≈ 13 minutos.** Caben con holgura en los **22 minutos** que el guion de la Sesión 03 reserva para la evaluación, con margen para entrar al aula, leer las instrucciones y enviar el intento. Si el Docente prefiere un intento más corto, aplicar el banco con selección aleatoria de 6 ítems (3 de la lectura autónoma y 3 de la S02) da unos 8 minutos.

**Reparto por origen: 5 preguntas de la lectura autónoma (U1-U2) y 5 de la Sesión 02 (U4).**
**Preguntas de administración del curso: 0.** No se pregunta por pesos, porcentajes, cortes, fechas, ventanas, créditos, horas, canal de entrega, plantilla, integridad académica, reglas de uso de IA ni acuerdos de convivencia. **No se usó la excepción de las 2 preguntas de método del curso**: la lectura obligatoria dio cinco preguntas de tema por sí sola, así que no hizo falta.

---

## 3. Las 10 preguntas completas

### INV-P1-01 · Para qué sirven las palabras clave
*U1-U2 · Las palabras clave y la indexación · 70 s*

**Enunciado:** Ya tiene escrito el título de su artículo y ahora debe elegir las **palabras clave**. Según la lectura obligatoria de la Sesión 01, ¿para qué sirven y qué conviene evitar al elegirlas?

- **✅ Sirven para la indexación en las bases de datos y son las que usan los lectores al buscar en línea; por eso no conviene que sean las mismas palabras del título.**
  *Correcta. Son el mecanismo por el que otro investigador encuentra su trabajo, así que repetir las palabras del título desperdicia la mitad de las entradas posibles de búsqueda.*
- ❌ Sirven para resumir el contenido a quien no leerá el artículo completo, así que conviene repetir las palabras del título para reforzar el tema del trabajo.
  *Error: quien no lee el artículo completo lee el resumen, no las palabras clave. Y la lectura pide justo lo contrario de repetir el título, para ampliar las posibilidades de búsqueda.*
- ❌ Sirven para anunciar las secciones que contiene el documento, de modo que se toman de los encabezados de la estructura IMRyD del propio artículo.
  *Error: confunde palabras clave con índice. No describen la estructura del documento, sino su contenido temático, y su destino es el buscador de la base de datos.*
- ❌ Sirven para declarar el área de conocimiento a la que se adscribe el trabajo, y por eso las fija la revista y no el autor del artículo.
  *Error: las elige el autor, y son una lista corta de palabras relevantes de su trabajo. No son una clasificación temática impuesta por la revista.*

**Cita literal (Casares-Salazar et al., 2019, Las palabras clave):** «Las palabras clave son una lista corta de palabras relevantes del trabajo. Sirven para la indexación en las bases de datos, por lo que son usadas por los lectores en el momento de hacer búsquedas en línea. Por lo tanto, no conviene que sean las mismas palabras del título, a fin de ampliar las posibilidades de búsqueda.»

*Nota de diseño: las cuatro opciones comparten la plantilla «Sirven para… + consecuencia práctica», así que la clave no se delata por forma. Es también la pregunta que conecta con la Sesión 04: quien entiende que las palabras clave son términos de búsqueda entiende después por qué el vocabulario decide lo que encuentra en Google Académico.*

---

### INV-P1-02 · Quiénes entran en la lista de autores
*U1-U2 · Caso corto · Autoría, orden de firma y reconocimientos · 90 s*

**Enunciado:** Tres personas intervinieron en su trabajo: la primera concibió la investigación y redactó el manuscrito, la segunda ejecutó las mediciones, y la tercera solo facilitó el laboratorio y revisó la ortografía del texto. Según la lectura obligatoria de la Sesión 01, ¿cómo queda la lista de autores?

- **✅ Las dos primeras son autoras, colocadas en orden de importancia con relación a los experimentos, y la tercera se menciona en la sección de reconocimientos.**
  *Correcta. Concebir la investigación y ejecutar las mediciones son contribuciones de autoría; prestar el laboratorio y corregir la ortografía se reconocen, pero no dan firma.*
- ❌ Las tres son autoras y se ordenan alfabéticamente por apellido, porque las tres participaron de alguna forma en la realización del trabajo.
  *Error doble: incluir a quien tuvo una contribución mínima es la falta ética que la lectura llama autoría injustificada, y el orden no es alfabético sino de importancia con relación a los experimentos.*
- ❌ Las tres son autoras y encabeza la lista quien facilitó el laboratorio, por ser quien aportó los recursos y la afiliación institucional del trabajo.
  *Error: el primer autor es por lo general quien más contribuyó al desarrollo de la investigación y a la redacción del manuscrito. Quien aportó recursos o instalaciones va en los reconocimientos.*
- ❌ Solo la primera es autora, y las otras dos se citan en la sección de referencias junto con las fuentes que se consultaron durante el trabajo.
  *Error: deja fuera a quien ejecutó los experimentos, que sí es contribución de autoría, y confunde reconocimientos con referencias. En las referencias van las fuentes citadas, no las personas que colaboraron.*

**Cita literal (Casares-Salazar et al., 2019, Los autores):** «La lista de autores debe incluir solamente a aquellos que contribuyeron a la concepción general de la investigación, a la ejecución de los experimentos o a la interpretación de los resultados. Cuando se incluye como autores a personas cuyas contribuciones fueron mínimas o nulas se incurre en una falta ética conocida como autoría injustificada (Mari-Mutt, s.f.). Todas las personas que de alguna forma participaron en la investigación pero que no son autores pueden y deben mencionarse en la sección de reconocimientos. Los autores deben colocarse en orden de importancia con relación a los experimentos. El primer autor es por lo general la persona que más contribuyó al desarrollo de la investigación y a la redacción del manuscrito.»

*Nota de diseño: el caso da tres contribuciones bien diferenciadas —concebir y redactar, ejecutar, facilitar y corregir— para que la decisión se tome con el criterio de la lectura y no por intuición sobre jerarquías. La autoría es materia de tema, no de administración del curso: se pregunta qué dice la fuente sobre la firma de un artículo, no qué exige el aula.*

---

### INV-P1-03 · Qué va y qué no va en las conclusiones
*U1-U2 · Caso corto · Las conclusiones no traen hallazgos nuevos · 85 s*

**Enunciado:** Al cerrar su artículo usted escribe, en la sección de **Conclusiones**, un dato de campo que no había aparecido en ninguna sección anterior, y vuelve a explicar en detalle por qué su medición es válida. Según la lectura obligatoria de la Sesión 01, ¿cuál es el error?

- **✅ Que las conclusiones enuncian los principales resultados sin justificarlos de nuevo y sin presentar hallazgos nuevos: cada una se basa en material ya presentado.**
  *Correcta. Un hallazgo que aparece por primera vez en las conclusiones llega sin metodología que lo sostenga, y volver a justificar la medición repite trabajo ya hecho en secciones anteriores.*
- ❌ Que las conclusiones no deben mencionar resultados, porque los resultados ya tienen su propia sección dentro de la estructura del documento.
  *Error: sí los enuncian. La sección presenta brevemente los principales resultados de la investigación; lo que no hace es volver a justificarlos ni añadir hallazgos que nadie vio antes.*
- ❌ Que las conclusiones deben ordenarse de la menos importante a la más importante, para dejar el punto fuerte en la última línea del artículo.
  *Error: invierte la recomendación de la lectura, que pide iniciar con las conclusiones más importantes y seguir con las demás. Y ese no es el defecto del párrafo descrito.*
- ❌ Que las conclusiones deben ir siempre unidas a las recomendaciones en un solo apartado, porque separadas pierden fuerza ante el lector.
  *Error: las recomendaciones son una sección opcional que puede ir junto con las conclusiones, no una obligación. Combinar secciones depende de los lineamientos de la revista, y no arregla el problema real.*

**Cita literal (Casares-Salazar et al., 2019, Las conclusiones):** «En esta sección se enuncian los principales resultados de la investigación sin justificarlos de nuevo y sin presentar nuevos hallazgos. Cada conclusión debe presentarse brevemente y estar basada en el material que ha sido presentado previamente en el documento. Conviene enfatizar lo que es importante y significativo, así como cualquier autocrítica. Se recomienda iniciar con las conclusiones más importantes y seguir con las demás (Silyn-Roberts, 2013).»

*Por qué importa para el curso: el criterio 2 de la ACA Final es «problema argumentado con evidencias, no una opinión». Una conclusión que estrena un dato es una afirmación sin evidencia presentada, que es exactamente lo que ese criterio castiga.*

---

### INV-P1-04 · Para qué sirve la sección de metodología
*U1-U2 · Caso corto · La reproductibilidad como propósito de la sección · 90 s*

**Enunciado:** Un compañero escribe completa su sección de metodología así: «Se recogieron datos de los usuarios y se procesaron con herramientas estadísticas». Según la lectura obligatoria de la Sesión 01, ¿por qué esa redacción no cumple el propósito de la sección?

- **✅ Porque no da el detalle suficiente para que otro investigador competente repita el trabajo ni para que el lector juzgue la validez de los resultados.**
  *Correcta. Ese es el propósito declarado de la sección, y la frase no lo cumple: no dice qué datos, de cuántos usuarios, cómo se obtuvieron ni qué método estadístico se usó, de modo que nadie podría reproducir el trabajo.*
- ❌ Porque está escrita en estilo impersonal; la metodología debe ir en primera persona para dejar clara la responsabilidad de quien ejecutó cada paso.
  *Error: el estilo impersonal es precisamente lo que la lectura recomienda («mantener el estilo impersonal propio de la redacción científica: se midió, se realizó una prueba»). El problema de la frase es la falta de detalle, no el «se recogieron».*
- ❌ Porque menciona los datos, que pertenecen a la sección de resultados; la metodología describe solo los materiales y los equipos empleados.
  *Error: la lectura pide expresamente describir en la metodología «los datos con los que se trabajará», cómo se obtuvieron y cualquier detalle que permita repetir el estudio. Lo que va en resultados son los hallazgos, no la descripción de los datos de partida.*
- ❌ Porque toda metodología debe abrir con las hipótesis y los objetivos del estudio, que son los que justifican los métodos que se eligieron.
  *Error: las preguntas de investigación, las hipótesis y los objetivos se formulan en la introducción, según la lectura. Repetirlos al abrir la metodología no arreglaría el defecto real, que es que el procedimiento no se puede reproducir.*

**Cita literal (Casares-Salazar et al., 2019, La metodología):** «El objetivo de la metodología consiste en describir los procedimientos experimentales con suficiente detalle como para que otro investigador competente pueda repetir el trabajo, permitiendo a la vez que el lector juzgue la validez de los resultados».
**Respaldo del distractor «primera persona»** (Comentarios finales): «3) mantener el estilo impersonal propio de la redacción científica (e.g. se midió, se realizó una prueba, etc.)».
**Respaldo del distractor «los datos son de resultados»** (La metodología): «En esta sección también se deberán describir los datos con los que se trabajará, e.g. la composición de la muestra o los datos de campo, cómo se obtuvieron y cualquier otro detalle que permita su repetición en condiciones similares».

---

### INV-P1-05 · Las tres partes de la Discusión
*U1-U2 · Los tres componentes de la Discusión, en su orden · 80 s*

**Enunciado:** La lectura obligatoria de la Sesión 01 afirma que la sección de **Discusión** consta básicamente de tres partes o componentes. ¿Cuáles son, y en qué orden?

- **✅ Explicar los resultados frente a las preguntas, hipótesis u objetivos; contrastarlos con los trabajos ya publicados; e interpretar el significado de cada conclusión.**
  *Correcta. Ese es el recorrido de la Discusión: se responde si se cumplieron las hipótesis, se confronta con lo que hallaron otros autores y se explica para qué sirvió el trabajo, con sus limitaciones.*
- ❌ Resumir de nuevo los datos obtenidos, agradecer a las personas e instituciones que colaboraron y enunciar las recomendaciones para investigaciones futuras.
  *Error: reúne tres secciones distintas del documento. Los agradecimientos son los reconocimientos y las recomendaciones son una sección opcional aparte; ninguno de los dos es una parte de la Discusión.*
- ❌ Describir los materiales y los procedimientos empleados, presentar los datos ya procesados y compararlos con la hipótesis que se formuló al inicio.
  *Error: las dos primeras son la metodología y los resultados. La Discusión no describe procedimientos ni vuelve a presentar los datos: parte de resultados ya expuestos para explicarlos.*
- ❌ Repetir el contenido de la introducción, ampliar el estado del arte con las fuentes que faltaron y anunciar la siguiente investigación del grupo.
  *Error: el estado del arte y el contexto van en la introducción, y los trabajos con los que se compara «se habrían citado en la introducción». La Discusión los retoma para confrontar, no para ampliar la revisión.*

**Cita literal (Casares-Salazar et al., 2019, La discusión):** «La sección de Discusión consta básicamente de tres partes o componentes: 1) En la primera parte se deben explicar los resultados confrontándolos con las preguntas de investigación, hipótesis u objetivos (…) 2) En la segunda parte se discute cómo concuerdan (o no) los resultados e interpretaciones con los trabajos anteriormente publicados (Day, 2005), tanto los que están a favor como en contra, explicando las posibles razones de las discrepancias (…) 3) En la tercera parte se explica o interpreta el significado de cada conclusión previamente deducida (…) Se debe dejar en claro las limitaciones del estudio y la forma como estas pudieron afectar las conclusiones.»

*Nota de diseño: las cuatro opciones enumeran tres movimientos con la misma plantilla y longitud parecida, así que la clave no es la más completa. Cada distractor está armado con partes reales de otras secciones del documento —reconocimientos, recomendaciones, metodología, resultados, introducción—, que es el error que de verdad comete quien no distingue las secciones.*

---

### INV-P1-06 · «Mi tema no cabe en ninguna línea»
*U4 · Caso corto · El mito que bloquea la elección de línea · 75 s*

**Enunciado:** Un compañero sostiene que su tema **no cabe en ninguna** de las seis líneas de Ingeniería del programa. Según la Sesión 02, ¿qué corresponde responderle?

- **✅ Que casi siempre cabe: hay que preguntarse qué duele en el tema —los datos, la red, el software, el dispositivo o el servicio en la nube—.**
  *Correcta. Las seis líneas son un menú de ángulos, no de temas: casi cualquier tema cabe en varias, y el ángulo se descubre identificando qué es lo que falla en el caso.*
- ❌ Que puede avanzar sin línea mientras el tema sea pertinente, y declararla al final del periodo cuando ya tenga escrito el marco teórico.
  *Error: es el mito de la línea como requisito administrativo. La línea define el vocabulario y los referentes desde el primer día; cambiarla o dejarla para el final obliga a reescribir el marco teórico completo.*
- ❌ Que debe proponer una línea nueva ante MinCiencias, porque el listado de seis del programa solo recoge las líneas de mayor demanda del país.
  *Error: MinCiencias no es una ventanilla donde se registran temas ni líneas nuevas por estudiante. Es el ministerio que organiza el conocimiento por áreas y líneas: un mapa de comunidades, no una lista de temas permitidos.*
- ❌ Que conviene tomar la línea más popular del momento, porque es la que le va a ofrecer la mayor cantidad de literatura disponible.
  *Error: la sesión desactiva ese mito de entrada («la moda no le entrega fuentes»). Lo que importa no es el volumen global de publicaciones de la línea, sino que haya artículos usables del ángulo concreto que él quiere trabajar.*

**Cita literal (Presentación de la Sesión 02, «Cuatro mitos que hay que desactivar hoy»):** «"Mi tema no cabe en ninguna línea." Casi siempre cabe. Pregúntese qué duele en su tema: ¿los **datos**, la **red**, el **software**, el **dispositivo** o el **servicio en la nube**? Esa respuesta ya es la línea.» · «Léala como un menú de ángulos, no de temas: casi cualquier tema cabe en varias líneas, pero se trabaja desde una.»

*Nota de diseño: los tres distractores son los otros tres mitos de la misma slide (avanzar sin línea, la línea como trámite, elegir por moda), así que no hay opciones absurdas: las cuatro son cosas que los estudiantes dicen de verdad. La pregunta no repite el trío «afinidad / viabilidad / pertinencia» de INV-P1-09: aquí se pregunta el desbloqueo, allí los criterios.*

---

### INV-P1-07 · Qué es MinCiencias y para qué le sirve al artículo
*U4 · MinCiencias y el Sistema Nacional de CTeI · 70 s*

**Enunciado:** De acuerdo con la Sesión 02, ¿qué es MinCiencias y en qué le sirve concretamente a la escritura de su artículo?

- **✅ El Ministerio de Ciencia, Tecnología e Innovación: coordina el Sistema Nacional de CTeI y organiza el conocimiento en áreas y líneas, y esa línea define su vocabulario, sus autores y sus revistas.**
  *Correcta. La sesión lo resume así: MinCiencias organiza el conocimiento por áreas y líneas, y la línea «define el vocabulario que usará, los autores que citará y las revistas donde buscará».*
- ❌ Un catálogo oficial de los temas de investigación autorizados en el país: si su tema no figura en ese catálogo, hay que reemplazarlo por uno que sí aparezca.
  *Error: es exactamente lo que la sesión niega («No es una lista de temas permitidos; es un mapa de comunidades de conocimiento»). No autoriza temas: agrupa comunidades que investigan con un mismo lenguaje.*
- ❌ Un requisito de trámite del artículo: se menciona en la portada y en las referencias para acreditar que el proyecto cumple la normativa nacional de investigación.
  *Error: la sesión lo descarta con esas palabras («No es un requisito de trámite que se llena y se olvida») y la lista de mitos insiste en que la línea no es administrativa, porque condiciona el contenido del texto.*
- ❌ El repositorio nacional en el que se consultan a texto completo las tesis y los artículos publicados por las universidades colombianas.
  *Error: confunde el ministerio con una base de datos de consulta. MinCiencias coordina el Sistema Nacional de CTeI y orienta convocatorias, financiación y categorización de grupos; no es el lugar donde se descargan los textos.*

**Cita literal (Presentación de la Sesión 02):** «MinCiencias = Ministerio de Ciencia, Tecnología e Innovación de Colombia. Coordina el **Sistema Nacional de CTeI**: la red de grupos, semilleros, universidades y centros que produce investigación en el país. Su función clave para usted: **organiza el conocimiento por áreas y líneas** (…) Lo que MinCiencias **NO** es: No es un requisito de trámite que se llena y se olvida. No es una lista de temas permitidos; es un mapa de **comunidades de conocimiento**. Traducción práctica: la línea define **el vocabulario que usará, los autores que citará y las revistas donde buscará**.»

---

### INV-P1-08 · Ubicar un caso en una de las 6 líneas
*U4 · Caso corto · Las 6 líneas de Ingeniería del programa · 85 s*

**Enunciado:** Usted quiere estudiar los riesgos de **disponibilidad y seguridad** que aparecen cuando la institución deja de alojar la plataforma de notas en su propio servidor y la traslada a un proveedor externo que la aloja y la opera. De las seis líneas de Ingeniería del programa, ¿en cuál se ubica ese ángulo?

- **✅ Cloud / FinTech: servicios en la nube y servicios financieros digitales, con vocabulario de SaaS, migración y disponibilidad.**
  *Correcta. Lo que duele en el caso es el servicio alojado en un tercero, y el vocabulario que la sesión asigna a esta línea es justamente migración y disponibilidad.*
- ❌ Telemática: redes, protocolos y comunicaciones, con vocabulario de latencia, ancho de banda y topología.
  *Error atractivo: la palabra «disponibilidad» hace pensar en la red. Pero el objeto de estudio no es el enlace que transporta el servicio, sino el servicio alojado en un tercero; si el ángulo fuera telemático, mediría latencia o pérdida de paquetes.*
- ❌ Aplicaciones: desarrollo de software y experiencia de uso, con vocabulario de usabilidad, requisitos y prototipo.
  *Error: se queda en que el objeto es «una plataforma» y la trata como software por construir. Aquí no se estudia cómo se usa ni cómo se desarrolla la plataforma, sino los riesgos de trasladar su alojamiento y su operación a un tercero.*
- ❌ Big Data: analítica de grandes volúmenes de datos ya existentes, con vocabulario de dataset, ETL y minería de datos.
  *Error: se engancha con la palabra «notas» y supone que hay datos por analizar. En el caso no se analiza ningún volumen de datos: se estudia el traslado y la operación de un servicio.*

**Cita literal (Presentación de la Sesión 02, tabla «Las 6 líneas de Ingeniería del programa»):** «**Cloud / FinTech** | Servicios en la nube y servicios financieros digitales | SaaS, migración, disponibilidad, pasarela de pago | ¿Qué riesgos de seguridad tiene migrar los pagos a la nube?» · «**Telemática** | Redes, protocolos y comunicaciones | latencia, ancho de banda, pérdida de paquetes, topología» · «**Aplicaciones** | Desarrollo de software y experiencia de uso | usabilidad, requisitos, prototipo, accesibilidad» · «**Big Data** | Analítica de grandes volúmenes de datos ya existentes | dataset, ETL, minería de datos, dashboard».
**Criterio de desempate que la sesión le da al estudiante:** «Pregúntese qué duele en su tema: ¿los **datos**, la **red**, el **software**, el **dispositivo** o el **servicio en la nube**? Esa respuesta ya es la línea.»

*Nota de diseño: el caso no reusa ninguna de las «preguntas de ejemplo» del deck (no se habla de pagos ni de pasarelas), para que no se responda por coincidencia literal sino aplicando el criterio. Las tres líneas no ofrecidas —IoT e IA— se dejaron fuera a propósito: ninguna es plausible aquí, y ofrecerlas habría bajado la dificultad al eliminarlas de un vistazo.*

---

### INV-P1-09 · Los tres criterios para elegir la línea
*U4 · Criterios técnicos de la elección de línea · 80 s*

**Enunciado:** La Sesión 02 fija **tres criterios** para elegir la línea de investigación, cada uno con su pregunta de control. ¿Cuáles son?

- **✅ Afinidad (¿la línea conserva lo que me interesa del tema?), viabilidad de fuentes (¿hay hoy al menos dos artículos usables de este ángulo?) y pertinencia local (¿le sirve a algo de mi entorno?).**
  *Correcta. Son los tres criterios de la tabla, con sus preguntas de control: afinidad con el tema, existencia real de fuentes usables hoy y utilidad en el propio entorno.*
- ❌ Novedad (¿la línea está de moda y se habla mucho de ella?), disponibilidad de herramientas (¿tengo instalado el software que hace falta?) y aval del Docente (¿aprueba la línea que elegí?).
  *Error: reúne tres criterios que la sesión descarta. El primero es el mito que abre la lista («la moda no le entrega fuentes»), y la elección de línea la hace y la justifica el estudiante: no se decide por el visto bueno del Docente.*
- ❌ Afinidad (¿me interesa la línea que voy a trabajar?), dificultad técnica (¿puedo con el nivel matemático que exige?) y cantidad total de resultados que devuelve el buscador.
  *Error: acierta con la afinidad y falla en los otros dos. La sesión no evalúa dificultad técnica, y sobre el buscador es explícita: se anota «cuántos resultados usables» hay por línea, no cuántos resultados totales.*
- ❌ Pertinencia local (¿sirve en mi entorno inmediato?), tamaño de la muestra (¿tengo suficientes casos para observar?) y presupuesto disponible (¿puedo pagar el acceso a los datos?).
  *Error: acierta con la pertinencia local y sustituye los otros dos por criterios de ejecución posterior. Además contradice el enfoque del curso: las herramientas y las fuentes que se piden son gratuitas y en el navegador, así que el presupuesto no es criterio de elección.*

**Cita literal (Presentación de la Sesión 02, tabla «Los tres criterios para elegir su línea»):** «**Afinidad** | ¿Esta línea conserva lo que a mí me interesa del tema, o lo desvía? | Tiene que forzar el tema para que quepa» · «**Viabilidad de fuentes** | ¿Encuentro hoy, en Google Académico, al menos 2 artículos usables de este ángulo? | Busca 10 minutos y no aparece nada pertinente» · «**Pertinencia local** | ¿Le sirve a algo de mi entorno: mi sede, mi empresa, mi barrio, mi práctica? | Solo tiene sentido en un país o una escala que no puede observar».
**Respaldo del distractor «resultados totales»** (Paso a paso): «**6.** Anote en la tabla **cuántos resultados usables** halló por línea (no cuántos resultados totales).»

*Nota de diseño: dos de los tres distractores conservan un criterio verdadero (afinidad en uno, pertinencia local en el otro), así que no se puede descartar leyendo la primera palabra. Los tres distractores se alargaron hasta igualar la clave —las cuatro opciones quedan entre 31 y 34 palabras, con tres criterios y su pregunta entre paréntesis— para que la longitud no delate nada.*

---

### INV-P1-10 · Consecuencia de elegir una línea u otra
*U4 · La línea decide el ángulo, y el ángulo decide todo lo demás · 80 s*

**Enunciado:** En la Sesión 02, dos estudiantes escriben el mismo tema tentativo, «seguridad informática»: el primero lo trabaja desde **Inteligencia Artificial** y el segundo desde **Telemática**. ¿Qué consecuencia tiene esa decisión para el artículo de cada uno?

- **✅ Cambian los conceptos por definir, los autores de referencia y la evidencia exigible: terminan con dos bibliografías que casi no se cruzan y dos artículos distintos.**
  *Correcta. Es la conclusión que la sesión pide anotar: la línea decide el ángulo y el ángulo decide todo lo demás, así que el mismo tema produce dos artículos distintos.*
- ❌ Cambia el enfoque de la redacción, pero los conceptos y los autores de referencia son los mismos porque el tema de fondo no cambió.
  *Error: reduce la línea a un asunto de estilo. Si el tema se aborda desde IA se hablará de clasificadores, entrenamiento y falsos positivos; desde telemática, de segmentación, firewall y tráfico anómalo. Son literaturas distintas, no la misma redactada de otro modo.*
- ❌ Ninguna consecuencia de fondo, siempre que los dos citen en el mismo formato: la línea afecta el registro del proyecto, no el contenido del texto.
  *Error: es el mito que la sesión desactiva expresamente. La línea no es un requisito administrativo; define el vocabulario y los referentes, y cambiarla a mitad del periodo obliga a reescribir el marco teórico completo.*
- ❌ Cambia la evidencia que cada uno debe recoger, pero no las fuentes: la literatura sobre seguridad informática es común a las dos líneas.
  *Error: concede la mitad. La sesión muestra que el primero busca «phishing detection, classifier, dataset» y el segundo «firewall, segmentación de red, latencia»: precisamente por eso las bibliografías casi no se cruzan.*

**Cita literal (Presentación de la Sesión 02):** «Caso concreto: dos estudiantes escriben "seguridad informática". El primero la trabaja como **Inteligencia Artificial** → busca *phishing detection*, *classifier*, *dataset*. El segundo la trabaja como **Telemática** → busca *firewall*, *segmentación de red*, *latencia*. Mismo tema, **dos bibliografías que casi no se cruzan** y dos artículos distintos.» · «Conclusión que hay que anotar: **la línea decide el ángulo, y el ángulo decide todo lo demás**. Efecto sobre el artículo: Cambia el **marco teórico** (qué conceptos hay que definir). Cambian los **antecedentes** (qué autores son referencia obligada). Cambia la **evidencia** que le van a exigir (un log de red no sirve para argumentar un modelo de IA).»

---

## 4. Cómo se cuidó la calidad de los distractores

- **Ninguna opción usa vocabulario de la Sesión 03 o posterior.** Se revisó el deck de la S03 slide por slide y su terminología (tipos de conocimiento, tipos de fuente, ZoteroBib) quedó fuera incluso de los distractores.
- **La clave nunca es la opción más larga.** En 01, 05, 08 y 09 las cuatro opciones comparten plantilla y extensión; en 02, 03, 04, 06, 07 y 10 la diferencia máxima de longitud entre la clave y el distractor más largo está por debajo de una línea, y en 03, 06 y 07 el distractor es **más** largo que la clave.
- **Los 3 distractores nunca comparten una plantilla que deje la clave como la opción impar.** Donde hay plantilla (01, 05, 08, 09) la comparten las cuatro opciones.
- **Cada distractor es un error de comprensión documentado, y su feedback cita la línea de la fuente que lo refuta**: la autoría injustificada y el orden de firma en 02, el orden de las conclusiones en 03, el estilo impersonal en 04, los reconocimientos y las recomendaciones en 05, los otros tres mitos de la slide en 06, «no es lista de temas permitidos» en 07, «resultados usables, no totales» en 09.
- **Sin «todas las anteriores» ni «ninguna de las anteriores».**
- **Una sola respuesta defendible.** Los enunciados se acotaron donde había riesgo: en 02 se detalla exactamente qué hizo cada una de las tres personas, para que la autoría no dependa de suposiciones; en 03 se describen los dos defectos del párrafo (dato inédito y justificación repetida) y la clave los cubre a los dos; en 04 se aclara que esa frase es la sección *completa* (si fuera un fragmento, la falta de detalle no sería demostrable); en 08 se dice que el proveedor externo *aloja y opera* la plataforma, para cerrar la lectura telemática.
- **Ninguna pregunta repite otra del curso.** Se comparó este banco contra los otros cuatro (Quiz 1, Quiz 2, Parcial 2 y Quiz 3) enunciado por enunciado, caso por caso y opción por opción. Las cinco preguntas de la lectura obligatoria que estaban repetidas con el Quiz 1 —etapas del método, IMRyD, el vacío, la frontera Resultados/Discusión y los criterios del título— se sustituyeron por cinco secciones que ningún otro banco toca: palabras clave, autores, conclusiones, la Discusión y su metodología aplicada. El caso de «seguridad informática desde IA o desde Telemática» quedó **solo** en INV-P1-10; ya no aparece en el Parcial 2 ni en el Quiz 2.

## 5. Desajustes encontrados en el material — para revisión del Docente

1. **La Sesión 03 le anuncia al estudiante un parcial que no coincide con el alcance del Parcial 1.** El deck `cun_investigacion_s03.json` trae una slide titulada «Qué evalúa la prueba parcial» que promete: «Diferenciar los tres tipos de conocimiento», «Clasificar una fuente como primaria, secundaria o terciaria», «Reconocer las partes de un artículo y qué va en cada una», «Detectar si una pregunta es investigable» e «Identificar el vacío dentro de una introducción de ejemplo». De esos cinco puntos, **solo dos están en el alcance del Parcial 1** (las partes del artículo y el vacío, que vienen de la lectura obligatoria). Los tipos de conocimiento y los tipos de fuente son contenido de esa misma Sesión 03 —que el Manual y la guía excluyen porque se dicta el día del cierre— y «si una pregunta es investigable» es de la Sesión 04. **Riesgo concreto:** si el Docente proyecta esa slide antes de aplicar el cuestionario, el estudiante espera preguntas que este banco no trae y puede reclamar. Dos salidas: (a) al proyectarla, decir en voz alta que esa lista corresponde al **Parcial 2**, o (b) editar la slide para que diga «qué evalúan las pruebas del curso» y separar lo del Parcial 1. **No se movió nada** del deck: está fuera de la carpeta `Cuestionarios/` de este encargo.
2. **El deck de la S03 y la lectura obligatoria dan dos versiones del título, compatibles pero no idénticas.** La lectura pide «hasta 12 palabras, o hasta 20 como máximo» y prohíbe empezar con artículo; el deck de la S03 pide «máximo 20 palabras» con la fórmula «actor + fenómeno + contexto» y no menciona el artículo inicial. No se contradicen —los dos ejemplos «fuertes» del deck empiezan por sustantivo, no por artículo—, pero conviene decirlo cuando se dicte la S03 para que nadie crea que cambió la regla. **Este banco ya no pregunta por el título:** la pregunta de título de la lectura obligatoria vive en el Quiz 1 (INV-Q1-04) y la de la fórmula del curso en el Quiz 2 (INV-Q2-10), así que el estudiante nunca ve las dos versiones dentro del mismo ítem.
3. **El Manual dice que la Sesión 02 cubre «MinCiencias · SNCTI», pero el deck no desarrolla el SNCTI más allá de nombrarlo.** El deck dice «Coordina el Sistema Nacional de CTeI: la red de grupos, semilleros, universidades y centros», y ahí termina. El Syllabus, en cambio, pide en la subtemática de U3-U4 «indagar sobre los actores del SNCTI (…) así mismo sobre los **8 focos estratégicos propuestos por la Misión de Sabios**» y explorar convocatorias, becas y movilidad. **Nada de eso está en el deck ni en el guion**, así que no se pudo preguntar: el banco solo llega hasta lo que la presentación efectivamente dice. Si el Docente quiere que los 8 focos de la Misión de Sabios sean evaluables, hay que agregarlos primero a la S02 (y el Parcial 1 ya cerró para esta edición, así que sería para el Parcial 2 o para la próxima).
4. **La lectura complementaria (Cienfuegos 2019) es la que desarrolla las etapas del método científico, y es opcional.** La única fuente en alcance que enumera las cuatro etapas de U2 es el **Syllabus**, no un deck ni la lectura obligatoria: los decks de S01 y S02 no traen ninguna slide sobre el método científico y sus etapas. **Este banco ya no depende de eso:** la pregunta de las etapas se retiró del Parcial 1 porque repetía la del Quiz 1 (INV-Q1-01), así que las diez preguntas de aquí se responden con el PDF de la lectura obligatoria y con el deck de la S02. La observación sigue viva **para el Quiz 1**: si el Docente quiere blindar esa pregunta, lo mejor es publicar en CDigital una nota de media página con las cuatro etapas textuales de U2 (o marcar la lectura de Cienfuegos como obligatoria en lugar de complementaria).
5. **Menor, sin efecto en el banco:** el nombre de la categoría se escribió sin tilde (`Parcial 1 - Investigacion U1-U4`) a propósito. El propio `cdigital.py` advierte que la consola de Windows es cp1252, y las órdenes que reciben el nombre de la categoría lo exigen **exacto** (`borrar-categoria`, `quiz-sustituir`): sin tilde no hay forma de que se rompa al teclearlo.

## 6. Siguiente paso en el aula (lo hace el Docente)

El aula 111070 **ya trae cuestionarios con slots aleatorios** apuntando a categorías viejas («Preguntas guardadas del contexto Cuestionario: Autoevaluación», etc.): importar el banco no basta.

```bash
export PYTHONUTF8=1
# 1) importar de verdad (sin --simular) — crea la categoría y sube las 10 preguntas
python config/moodle/cdigital.py importar "Pregrado/Investigacion en ciencia y tecnologia/Clases/Recursos/Cuestionarios/Parcial 1 - banco de preguntas (Moodle XML).xml" --curso 111070
# 2) ver qué cmid tiene la actividad Parcial 1 y de qué categoría saca sus slots
python config/moodle/cdigital.py curso 111070
python config/moodle/cdigital.py quiz <cmid del Parcial 1>
# 3) sustituir los slots por la categoría nueva (primero sin --confirmar: simula)
python config/moodle/cdigital.py quiz-sustituir <cmid> --categoria <catid,contextid de Parcial 1 - Investigacion U1-U4>
```

Este banco es el **maestro del repositorio**: en cada edición del curso se reimporta, no se reescribe.
