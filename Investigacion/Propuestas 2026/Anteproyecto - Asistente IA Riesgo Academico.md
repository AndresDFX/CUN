# Prototipo de asistente conversacional con recuperación aumentada (RAG) para la detección temprana de riesgo académico en un programa de la CUN: construcción, validación retrospectiva y salvaguardas de uso

Anteproyecto en el **Formato de Estructuración y Presentación de Propuestas de Investigación
INV-FO03 (Anexo 2)** · Convocatoria interna CUN 2026 — Desarrollo de Grupos Temáticos de
Investigación (Fase II).

**Fecha de diligenciamiento:** día 15 · mes 08 · año 2026.

---

## Pendientes previos a la radicación (nota administrativa — no es un campo del INV-FO03)

Este apartado existe para el uso interno del investigador principal y **debe retirarse al trasladar
el contenido al formato oficial**. No sustituye ni modifica ningún campo del INV-FO03.

1. **CvLAC registrado, sin producción registrada — pendiente de confirmación, no incumplimiento.** El
   numeral 5.1 de los Términos de Referencia exige "mantener el aplicativo CvLAC debidamente
   actualizado". El investigador principal **sí tiene CvLAC registrado**; lo que no tiene aún es
   producción cargada en él, porque esta sería su primera propuesta de investigación en la
   institución. Un registro al día que refleja cero producción está, en sentido literal, actualizado:
   **no hay incumplimiento que declarar**. Pero si "debidamente actualizado" admite una lectura más
   exigente no es algo que le corresponda decidir al proponente, así que la consulta queda planteada
   en `Correo a la DNI - consultas previas a la radicacion.md` y conviene tener la respuesta antes de
   radicar. Con independencia de cómo se lea, sin producción previa esta propuesta no puede apoyarse
   en la trayectoria del investigador y debe sostenerse por la calidad de lo propuesto — que es
   exactamente donde está escrita.
2. **Contrato de tiempo completo — cumplido.** El investigador principal tiene vinculación activa
   con contrato de tiempo completo; ese requisito del numeral 5.1 está satisfecho.
3. **Descarga horaria y ausencia de pendientes de convocatorias anteriores.** Ambos requisitos del
   numeral 5.1 dependen de aprobación y verificación de la DNI; no se dan por resueltos aquí.
4. **Cronograma de la convocatoria — sin fechas calendario.** Las fechas del numeral 9 de los
   Términos de Referencia (cierre 20/03/2026, correcciones 31/03/2026, comité de ética 03/04/2026,
   acta de inicio 10/04/2026) ya transcurrieron. Por esa razón el cronograma de este anteproyecto se
   formula en **semanas relativas (Semana 1 a Semana 12)** contadas desde la firma del acta de
   inicio, y **no se inventan fechas calendario**. El anclaje a calendario queda pendiente de la
   respuesta de la DNI.
5. **Autorización de acceso a los datos académicos — requisito habilitante y riesgo principal del
   proyecto.** Esta propuesta no puede ejecutarse sin autorización expresa para consultar, en un
   periodo académico **ya cerrado** y de un solo programa, los registros de calificaciones parciales,
   asistencia y actividad en el aula virtual. Debe gestionarse con la dirección del programa, con
   Registro y Control Académico y con el área responsable de la plataforma de aula virtual, y debe
   definirse por escrito el rol del investigador frente a esos datos (acceso a un extracto
   seudonimizado bajo responsabilidad institucional, no cesión de la base). **Este documento no
   supone esa autorización concedida.** La contingencia declarada en el alcance —construir y evaluar
   el prototipo sobre un conjunto sintético calibrado con estadísticos agregados— mantiene vivos los
   productos técnicos pero **degrada el valor de la validación retrospectiva**, y si hay que activarla
   debe informarse a la DNI porque cambia el objeto de la evaluación.
6. **Aval del Comité de Ética de la Investigación Institucional — habilitante.** El proyecto trata
   datos personales de estudiantes y aplica instrumentos a docentes y estudiantes voluntarios.
   Ninguna extracción de datos ni actividad con participantes puede iniciar antes del aval del Comité
   y de la aprobación del consentimiento informado por parte de este.
7. **Tratamiento de datos personales y servicios de terceros — decisión de diseño por confirmar.**
   La Ley Estatutaria 1581 de 2012 obliga a autorización, finalidad e información previa del titular.
   Por eso el diseño mantiene los identificadores y los datos crudos **dentro de la infraestructura
   que la institución autorice** y expone al modelo de lenguaje únicamente indicadores derivados y
   seudonimizados. Queda por confirmar con la institución: (a) si es admisible usar un servicio de
   modelo de lenguaje alojado por un tercero incluso con datos seudonimizados, o si debe operarse
   exclusivamente con un modelo de pesos abiertos en infraestructura controlada; y (b) que los
   términos del proveedor que se contrate permitan **desactivar el uso de los datos enviados para
   entrenamiento de modelos**. Si (a) se resuelve por la vía restrictiva, el diseño ya la contempla
   como configuración principal y el impacto es de costo de cómputo, no de alcance.
8. **Disponibilidad real de la traza de actividad del aula virtual — no verificada.** El diseño
   supone que la plataforma expone registros de actividad utilizables (accesos, entregas, tiempo en
   recursos) para el grupo piloto. Esa disponibilidad no ha sido verificada por el proponente. Si no
   existe o no es exportable, el conjunto de variables se reduce a calificaciones y asistencia; la
   propuesta sigue siendo ejecutable, pero **el poder de anticipación esperado disminuye** y así
   deberá reportarse. Verificar antes de radicar.
9. **Rubros de talento humano y de cómputo — no verificados contra la tabla del numeral 6.** La
   tabla de rubros financiables y no financiables del numeral 6 de los Términos de Referencia **está
   incrustada como imagen en el PDF y no se puede extraer ni leer**, de modo que no fue posible
   verificar dos rubros de este presupuesto: (a) la **bonificación del auxiliar de investigación de
   semillero**, $900.000, equivalente al **23,4 %** del presupuesto solicitado; y (b) los
   **servicios de cómputo y de API de modelo de lenguaje**, $1.000.000, equivalentes al **26,0 %**.
   En conjunto, **49,4 % del presupuesto está pendiente de verificación** contra un documento que no
   se puede leer. Debe confirmarse con la DNI la financiabilidad de ambos rubros antes de radicar; si
   alguno no lo es, la reasignación es viable pero cambia el diseño (el auxiliar es el segundo
   anotador del conjunto de validación y su ausencia elimina la medida de fiabilidad).
10. **Vinculación a un grupo de investigación CUN — por definir.** El Parágrafo 3 del numeral 5.1
    prioriza la financiación de propuestas que contemplen la participación de un docente investigador
    perteneciente a un grupo de investigación CUN. La adscripción del investigador principal a un
    grupo y la vinculación de su CvLAC al GrupLAC correspondiente están consultadas a la DNI y **no
    se dan por resueltas** en la ficha de identificación.
11. **Número de propuestas por investigador principal — no está limitado en el documento.** Los
    Términos de Referencia **no fijan un máximo** de propuestas por investigador principal: el
    Parágrafo 1 del numeral 5.1 establece un **mínimo** ("deberán presentarse, en todos los casos, de
    manera individual o en coautoría, con una propuesta nueva") y el numeral 8 fija el techo de
    financiación "por propuesta aprobada". Radicar este anteproyecto junto con los demás que el
    investigador estructura en esta misma convocatoria **no contraviene ningún numeral escrito**, pero
    conviene confirmarlo con la DNI: la descarga horaria del mismo numeral 5.1 está condicionada al
    "número de plazas de investigación disponibles", y varios proyectos de 12 semanas en paralelo
    compiten por las mismas horas del mismo docente. **Esta consulta todavía no está incluida en el
    correo a la DNI:** el borrador vigente de `Correo a la DNI - consultas previas a la radicacion.md`
    plantea únicamente el cronograma y el alcance del requisito de CvLAC/GrupLAC. Debe agregarse a ese
    correo —junto con la del pendiente 9 sobre rubros financiables— antes de radicar.
12. **Inconsistencia en los criterios de evaluación del numeral 11.** La tabla del numeral 11 asigna
    Elementos preliminares 2 / Impacto, viabilidad y retorno 28 / Calidad de la propuesta 50 /
    Resultados y productos 20 = 100, mientras el texto explicativo inmediatamente debajo asigna
    Elementos preliminares 20 / Calidad de la propuesta 60 / Resultados y productos 20 = 100 sin
    desglosar "impacto, viabilidad y retorno". Es una inconsistencia del propio documento
    institucional y **no se resuelve aquí**. Este anteproyecto está escrito para el criterio más
    exigente bajo cualquiera de las dos lecturas: la **calidad de la propuesta**.
13. **Verificación de metadatos bibliográficos — no ejecutada.** Las 30 entradas de la lista de
    referencias corresponden a obras que el investigador principal identifica como existentes y
    reconocibles en su campo, pero **los metadatos de cada entrada —volumen, número, artículo, rango
    de páginas, año y DOI— no fueron contrastados uno por uno contra el registro del editor**. Por eso
    algunas entradas se dejan deliberadamente sin número de artículo o sin rango de páginas en lugar de
    completarlas con un dato no verificado ([5], [12], [20], [22] y el año de la versión vigente del
    modelo de medición de Minciencias). El contraste de los 30 registros contra la fuente del editor y
    la incorporación de DOI quedan como tarea previa a la radicación; el apartado "Lista de
    referencias" declara este mismo alcance y **no afirma ninguna verificación que no se haya hecho**.

---

## Identificación de la propuesta

| Campo | Contenido |
|---|---|
| **Título de la propuesta** | Prototipo de asistente conversacional con recuperación aumentada (RAG) para la detección temprana de riesgo académico en un programa de la CUN: construcción, validación retrospectiva y salvaguardas de uso |
| **Investigador principal** | Julian Andrés Castaño Erazo |
| **Co-investigador(es)** | No aplica (propuesta individual). Se vincula un estudiante de semillero como auxiliar de investigación y **segundo anotador** del conjunto de validación, sin rol de co-investigador. |
| **Correo electrónico** | julian_castanoe@cun.edu.co |
| **Programa académico / Área transversal** | Ingeniería de Sistemas y Especialización en Inteligencia Artificial (desarrollo y evaluación). El programa piloto sobre el que se construye el conjunto de datos se acuerda con la dirección de programa; la opción prevista es Ingeniería de Sistemas, por ser el programa de adscripción del investigador principal. |
| **Sede** | Bogotá — sede de adscripción del investigador principal |
| **Escuela** | Escuela de Ingenierías |
| **Fechas de implementación** | Fecha de inicio: a partir de la firma del acta de inicio (por confirmar con la DNI). Fecha de finalización: 12 semanas después del acta de inicio. |
| **Tiempo total en meses** | 3 meses (12 semanas) |
| **Lugar de ejecución de la propuesta** | Sede Bogotá, modalidad de trabajo virtual. El desarrollo y el tratamiento de datos se realizan en la infraestructura de cómputo que la institución autorice; los talleres y las sesiones de evaluación con docentes-tutores y estudiantes voluntarios se realizan en línea. |
| **Grupo de investigación** | **Por definir.** La adscripción del investigador principal a un grupo de investigación CUN y la vinculación de su CvLAC al GrupLAC correspondiente son una de las consultas abiertas a la DNI (ver pendiente 10). No se declara un grupo que no esté confirmado. |
| **Grupo Temático** | Grupo Temático 1 — Línea de Gestión y Tecnologías |
| **Eje Dinamizador** | Inteligencia Artificial y Tecnologías Emergentes |
| **Presupuesto solicitado** | $3.850.000 COP (por debajo del techo de $5.000.000 del numeral 8; desglose y justificación en el apartado de presupuesto) |

---

## Elementos preliminares

Marque la opción según corresponda. Cuantos más elementos incorpore la propuesta, mayor puntaje
puede obtener.

| Elemento a considerar | Cumple | Precisión |
|---|---|---|
| ¿La propuesta contempla la creación o vinculación de experiencias de Semilleros? | **Sí** | Un estudiante de semillero de Ingeniería de Sistemas se vincula como auxiliar de investigación con plan de trabajo, entrenamiento y certificación. No es apoyo accesorio: es el **segundo anotador independiente** del conjunto de validación —lo que hace posible reportar fiabilidad entre anotadores— y participa en la construcción del canal de datos y en la documentación de la arquitectura. |
| ¿Los resultados esperados implican a más de un programa académico? | **Parcialmente** | El desarrollo se realiza desde Ingeniería de Sistemas y la Especialización en Inteligencia Artificial, y el panel de docentes-tutores que evalúa la utilidad de las recomendaciones se convoca en al menos dos programas de la Escuela de Ingenierías. Pero el **conjunto de datos y la validación retrospectiva se limitan a un solo programa piloto**, de modo que los resultados de desempeño describen ese programa y no varios; lo transferible es la arquitectura y el protocolo de datos, no las métricas. |
| ¿Los resultados esperados implican a más de una sede regional? | **Parcialmente** | El programa piloto opera en modalidad virtual y su matrícula suele integrar estudiantes de distintas regionales; la distribución real del grupo se reportará como dato descriptivo. No se despliega el prototipo en otra sede ni se replica la validación fuera de la sede Bogotá dentro de las 12 semanas, por lo que **no se afirma un impacto multi-sede verificado**. |
| ¿Los resultados esperados implican a las diversas modalidades de formación (virtual, distancia y presencial)? | **Parcialmente** | El conjunto de variables se apoya en la traza de actividad del aula virtual, que existe en las modalidades **virtual y a distancia**; en la modalidad **presencial** esa traza es marginal o inexistente y el modelo quedaría reducido a calificaciones y asistencia. El alcance de esta propuesta no cubre la modalidad presencial y no se afirma que la cubra: se documenta explícitamente qué variables faltarían para adaptarlo. |
| ¿La propuesta contempla la articulación efectiva con comunidades vinculadas a la sociedad civil? | **No** | El proyecto se ejecuta íntegramente sobre procesos y datos internos de la institución; no interviene comunidades externas. |
| ¿La propuesta contempla la articulación efectiva con actores del sector externo (empresas, ONG, entidades)? | **No** | La relación con proveedores de servicios de cómputo o de modelos de lenguaje es una compra de servicio, no una articulación investigativa, y no se declara como tal. |
| ¿La propuesta contempla la articulación efectiva con organizaciones de carácter internacional? | **No** | No aplica en el alcance de 12 semanas. |
| ¿La propuesta contempla incluir mecanismos de financiación externa? | **No** | La ejecución se financia con $3.850.000 de la convocatoria. El prototipo, la validación retrospectiva y la arquitectura documentada se conciben como antecedente verificable para una postulación externa posterior (ventana Minciencias o convocatorias de permanencia estudiantil), pero **no se declara financiación externa comprometida**, porque no la hay. |

---

## Tipo de propuesta

Marque con una X.

| Tipo | Marca |
|---|---|
| Investigación | |
| Productiva | |
| Innovación | |
| Pedagógica | |
| Proyección Social | |
| **Desarrollo de Software** | **X** |
| Obra Creación | |
| Otro | |

**Justificación de la selección.** El entregable central es un **artefacto de software que hoy no
existe y que esta propuesta construye**: un canal determinista que calcula indicadores de riesgo a
partir de los registros académicos del programa piloto y una capa conversacional con recuperación
aumentada (RAG) que redacta explicaciones y recomendaciones ancladas a documentos institucionales
verificables. Ese artefacto es el objeto del trabajo, consume el grueso del esfuerzo y es lo que se
somete a validación; describirlo de otro modo desalinearía el tipo de propuesta respecto del
presupuesto y del cronograma.

**Por qué no las otras siete.** No se marca **Investigación** a secas porque el propósito no es
producir conocimiento desvinculado de un artefacto: sin el prototipo construido no hay nada que
evaluar. No se marca **Innovación** porque, a diferencia de otra propuesta que el investigador
estructura en esta convocatoria —donde el sistema ya existe y lo que se produce es su evaluación—,
aquí el software se construye desde cero dentro del proyecto, y "Desarrollo de Software" describe eso
con más precisión. No se marca **Pedagógica** porque no se propone una intervención de aula, un
rediseño curricular ni una estrategia didáctica, y porque el estudio **no mide aprendizaje ni
permanencia efectiva** (exclusión declarada en el alcance). No se marca **Productiva** porque no hay
un bien o servicio destinado a un mercado dentro de este alcance. No se marca **Proyección Social**
porque no se articulan organizaciones de la sociedad civil ni del sector empresarial. No se marca
**Obra Creación** porque el producto no es una obra artística. Y no se marca **Otro** porque una de
las categorías previstas describe el trabajo sin forzarla.

**Precisión necesaria sobre el tipo.** "Desarrollo de Software" no significa aquí entregar un sistema
en producción integrado a los sistemas académicos de la CUN: el entregable es un **prototipo
funcional evaluado en un piloto retrospectivo**, con su arquitectura documentada y sus salvaguardas.
El paso a producción exige integración, gobierno de datos y soporte que exceden 12 semanas y
$3.850.000, y queda fuera del alcance de forma explícita.

---

## Resumen

*(Máximo 200 palabras. Conteo real verificado con `wc -w` sobre el texto extraído: **199 palabras**.)*

La CUN enfrenta pérdida de asignaturas, rezago y deserción; las alertas de permanencia dependen de
revisiones manuales que llegan con el corte de notas, cuando el margen de intervención ya se estrechó.
Esta propuesta construye y evalúa un prototipo de asistente conversacional para detectar tempranamente
el riesgo académico en un programa piloto. El diseño separa dos capas: un canal determinista que
calcula indicadores de riesgo —calificaciones parciales, asistencia y actividad en el aula virtual—
con código auditable, y una capa de generación aumentada por recuperación (RAG) que redacta la
explicación y la recomendación anclándolas al Syllabus vigente, al reglamento estudiantil y a las
rutas de apoyo institucionales. Así se acota la alucinación: el modelo no calcula el riesgo ni escribe
cifras, las explica. La evaluación es retrospectiva, sobre un periodo cerrado, con datos
seudonimizados y sin emitir alertas sobre estudiantes identificados: se contrastan sensibilidad,
precisión y semanas de anticipación frente a la práctica actual de corte de notas, se audita la
atribución de cada afirmación a su fuente, se examina el sesgo entre subgrupos y se valora su utilidad
con docentes-tutores. Se entregan el prototipo, su arquitectura documentada, el protocolo de datos y
una lista de salvaguardas de adopción.

---

## Relación general de la propuesta con los ejes temáticos dinamizadores

Seleccione (marque con una X) el eje dinamizador en el que se inscribe su propuesta:

| Grupo Temático | Eje dinamizador | Marca |
|---|---|---|
| 1 — Gestión y Tecnologías | Desarrollo de Tecnologías Educativas | |
| 1 — Gestión y Tecnologías | Tecnologías de la Información y la Comunicación e Internet de las Cosas (IoT) | |
| 1 — Gestión y Tecnologías | **Inteligencia Artificial y Tecnologías Emergentes** | **X** |
| 2 — Innovación Pedagógica | Docente Avatar y Telepresencia | |
| 2 — Innovación Pedagógica | Pedagogías de la Comunicación y el Diseño, Desarrollo de Industrias Creativas y Culturales | |
| 2 — Innovación Pedagógica | Educación Entretenida | |
| 3 — Responsabilidad Social | Energías alternativas, Transición Energética y sostenibilidad ambiental | |
| 3 — Responsabilidad Social | Construcción de Paz y Responsabilidad Social | |
| 3 — Responsabilidad Social | Industrias 5.0, Big Data, ciberseguridad y manejo de datos | |
| **Escenario de interacción con otra área o función sustantiva de la CUN** | Bienestar y permanencia estudiantil (destinatario del prototipo y validador de la definición operativa de riesgo) y gestión académica (dirección de programa y Registro y Control como custodios de las fuentes de datos) | **X** |

**Justificación de la elección — un solo eje.** Se marca **un único eje dinamizador**, "Inteligencia
Artificial y Tecnologías Emergentes", porque el objeto del proyecto es el diseño de un sistema de
inteligencia artificial aplicado a una función sustantiva institucional, y esa es la descripción
literal del eje. La decisión se toma descartando explícitamente los dos que podrían disputarla.
**No se marca "Desarrollo de Tecnologías Educativas"** porque el artefacto no produce material de
enseñanza ni media el proceso de aprendizaje: opera sobre registros administrativos y académicos para
apoyar una decisión de acompañamiento; llamarlo tecnología educativa desdibujaría lo que hace.
**No se marca "Industrias 5.0, Big Data, ciberseguridad y manejo de datos"** porque el volumen de
datos de un programa piloto en un periodo no es "big data" en ningún sentido técnico —son miles de
registros, no millones— y porque el componente de protección de datos, aunque central en el diseño,
es una salvaguarda del proyecto y no su objeto de investigación. Marcar tres ejes para "sumar" sería
exactamente el tipo de imprecisión que el criterio de calidad castiga.

Se marca además el **escenario de interacción con otra función sustantiva**, y no de forma retórica:
la definición operativa de "riesgo académico" que el prototipo calcula **no la fija el investigador**,
la valida el área de bienestar y permanencia en el primer objetivo específico, porque quien conoce las
rutas de intervención y sus umbrales de utilidad es esa área. Un sistema que detecta riesgo según un
criterio que el área responsable no reconoce no tiene destinatario.

**Vinculación del eje transversal de herramientas de IA.** El eje transversal del numeral 3 pide
vincular herramientas de IA "en la construcción y la proyección de resultados". Aquí se cumple en tres
planos distinguibles, y conviene separarlos para no confundir el objeto con el instrumento. Primero,
**la IA es el artefacto construido**: un modelo de lenguaje operado en arquitectura de recuperación
aumentada es el corazón del prototipo, y un clasificador interpretable —no una red profunda— produce
la señal de riesgo. Segundo, **la IA es objeto de auditoría**: el proyecto no solo usa el modelo, mide
si sus afirmaciones son atribuibles a una fuente recuperada y si su señal se comporta de forma
comparable entre subgrupos de estudiantes; es decir, produce evidencia sobre la herramienta, no solo
con la herramienta. Tercero, **la IA se usa como asistencia en la construcción del proyecto**:
asistentes de IA generativa apoyan la escritura de código, la depuración de la búsqueda bibliográfica
y la codificación preliminar de las respuestas abiertas de los instrumentos, en todos los casos con
verificación humana declarada y registrada en una bitácora de uso. Los tres planos se detallan en
"Aplicación de herramientas IA".

---

## Impacto, viabilidad y retorno de la propuesta de investigación

### Impacto de la investigación

| Dimensión | Contenido |
|---|---|
| **Fortalecimiento institucional** | La institución obtiene cuatro activos que hoy no tiene documentados: (a) una **definición operativa de riesgo académico** acordada con el área de permanencia y calculable a partir de fuentes que la institución ya posee, en lugar de un criterio implícito que varía por docente; (b) un **prototipo funcional** que convierte esa definición en una señal semanal y en una explicación trazable a documento institucional; (c) evidencia medida —no supuesta— de **cuántas semanas antes** que la práctica actual de corte de notas puede emitirse una alerta útil, y a qué costo de falsos positivos; y (d) un **protocolo de tratamiento de datos y una lista de salvaguardas** (seudonimización, no decisión automatizada, revisión de sesgo, declaración de uso de IA) que sirven de base para cualquier iniciativa institucional de analítica académica, no solo para esta. El cuarto activo es el que sobrevive incluso si el prototipo rinde mal. |
| **Pertinencia académica y alineación institucional** | La permanencia estudiantil es una función sustantiva de la institución y un indicador vigilado por el sistema de aseguramiento de la calidad; un instrumento que la apoye con evidencia interna es pertinente por sí mismo. La propuesta se inscribe en el eje de Inteligencia Artificial y Tecnologías Emergentes y en las capacidades reales de la Escuela de Ingenierías: el investigador principal es ingeniero de sistemas y docente de la Especialización en Inteligencia Artificial, de modo que el desarrollo se ejecuta con competencias existentes y no contratadas. El proyecto además retroalimenta la docencia: la arquitectura, las métricas y el análisis de sesgo son material de aula inmediatamente reutilizable en las asignaturas de IA y de formación investigativa. |
| **Plan de evaluación de impacto** | El impacto se evalúa con seis indicadores medibles **dentro de las 12 semanas**, todos con fuente de verificación y todos declarados antes de ejecutar. (1) **Cobertura del conjunto de datos:** 100 % de los estudiantes del grupo piloto del periodo cerrado con vector de indicadores completo, y porcentaje de valores faltantes reportado por variable. (2) **Anticipación:** número de semanas de diferencia entre la primera alerta del prototipo y el momento en que la práctica actual (corte de notas) habría identificado el mismo caso; se reporta la mediana y el rango, no un promedio único. (3) **Desempeño de detección:** sensibilidad, precisión, valor predictivo negativo y área bajo la curva ROC del clasificador frente al desenlace conocido del periodo, reportados junto a la **prevalencia observada** del desenlace —sin la cual esas cuatro cifras no son interpretables—, con intervalos de confianza y con la **línea base explícita** (la regla de corte de notas vigente); el criterio de éxito es superar la línea base, no alcanzar una cifra absoluta. (4) **Verificabilidad de las recomendaciones:** porcentaje de afirmaciones factuales del texto generado que un revisor humano puede atribuir a un fragmento recuperado (meta declarada como hipótesis: ≥ 95 %), sobre una muestra de 100 respuestas generadas, con doble anotación en el 30 %. (5) **Equidad de la señal:** diferencia en tasa de falsos positivos entre subgrupos definidos por las variables que la institución autorice (modalidad, jornada, rango de edad, sede de matrícula), reportada con su n; si alguna variable no está disponible, se declara como no evaluada en lugar de omitirse. (6) **Utilidad percibida:** puntaje de utilidad y de intención de uso de docentes-tutores (mínimo 6 participantes) sobre la explicación generada frente a un puntaje numérico sin explicación, en comparación pareada. |

**Advertencia deliberada sobre lo que este proyecto no puede demostrar.** No se afirma —ni se
promete— que el prototipo reduzca la deserción o mejore la permanencia. Establecer ese efecto exige un
diseño longitudinal con grupo de comparación, intervención real sobre estudiantes y al menos un
semestre de seguimiento; prometerlo en 12 semanas sería insostenible y, si se aceptara, quedaría como
un compromiso incumplible frente a la DNI. Lo que este proyecto puede demostrar es **si la señal
existe, con cuánta antelación, con qué error y si su explicación es verificable**, que es la condición
previa de cualquier estudio de efecto posterior.

### Viabilidad y retorno de investigación

| Dimensión | Contenido |
|---|---|
| **Contribución a procesos de optimización interna (tiempos y recursos)** | Hoy la identificación de estudiantes en riesgo consume tiempo docente y del área de permanencia en revisión manual de planillas, y ese tiempo se gasta después del corte de notas, cuando la intervención tiene menos margen. El prototipo automatiza el cálculo de la señal y la redacción del primer borrador de explicación, dos tareas repetitivas y de bajo valor discrecional, y deja a la persona la decisión y el contacto. El retorno se plantea como **hipótesis de trabajo, no como hecho**: el proyecto mide el tiempo que hoy toma revisar un grupo manualmente (autorreportado por docentes-tutores) y el tiempo de revisión de la salida del prototipo (registrado prospectivamente en la evaluación de utilidad), y reporta la comparación con su naturaleza distinta declarada. Si el resultado es que la revisión de la salida consume lo que el cálculo ahorra, ese hallazgo también es útil: evita adoptar un ahorro aparente. |
| **Potencial de transferencia tecnológica** | Alto y con costo marginal bajo, por dos decisiones de diseño. Primera, la **separación de capas**: el canal de indicadores es código propio y portable, y la capa de recuperación se alimenta de documentos institucionales que cada programa ya tiene, de modo que replicar el prototipo en otro programa es cambiar el extracto de datos y el corpus documental, no reescribir el sistema. Segunda, la **preferencia por componentes de pesos abiertos y librerías sin licenciamiento** (modelo de lenguaje open-weight, orquestador y base vectorial de código abierto), que evita atar la institución a un proveedor. Los activos transferibles son el prototipo con su código, la arquitectura de referencia, el protocolo de tratamiento de datos y la lista de salvaguardas. La transferencia a producción, en cambio, **no se promete dentro del proyecto**: requiere integración con los sistemas académicos, gobierno de datos y soporte, y queda planteada como fase siguiente. |
| **Alineación con tendencias de mercado e IA** | La analítica de aprendizaje y los sistemas de alerta temprana son un segmento consolidado de la tecnología educativa, y la incorporación de modelos generativos como capa explicativa sobre modelos predictivos es una tendencia reciente y todavía poco evaluada en instituciones de habla hispana. El vacío de mercado que esta propuesta ocupa no es predecir —eso lo hacen productos comerciales— sino **explicar de forma verificable y anclada a la normativa de la propia institución**, que es justamente lo que un producto genérico no puede hacer. Existe además una tendencia regulatoria que refuerza el diseño: la exigencia de explicabilidad y de no decisión automatizada sobre personas. Un prototipo que nace con revisión humana obligatoria y trazabilidad a fuente está alineado con ella; uno que emita puntajes opacos tendría que rehacerse. |

**Viabilidad técnica.** Los componentes están disponibles y son maduros: un modelo de lenguaje de
pesos abiertos servido en infraestructura controlada, un orquestador de recuperación, una base
vectorial ligera y un clasificador interpretable de la familia de la regresión logística y los árboles
de decisión. No se propone entrenar un modelo desde cero, no se propone ajuste fino de un modelo de
lenguaje y no se propone arquitectura novedosa: el aporte está en la integración, en el anclaje
institucional y en la evaluación, no en la invención de un método. El investigador principal reúne el
perfil (ingeniero de sistemas, docente de la Especialización en Inteligencia Artificial) y el proyecto
no depende de contratar competencias externas.

**Viabilidad económica.** El presupuesto solicitado es de **$3.850.000**, el 77 % del techo de
$5.000.000 del numeral 8. No se solicita hardware de servidor —se usa cómputo en la nube por tres
meses, o infraestructura institucional si está disponible, lo que reduciría el monto—, no se solicitan
desplazamientos y no hay licencias propietarias en la ruta crítica. Dos rubros, que suman el 49,4 %
del total, **no pudieron verificarse contra la tabla de rubros financiables del numeral 6 porque esa
tabla está incrustada como imagen en el PDF y no es legible**; el pendiente 9 lo declara con el detalle
y el porcentaje expuesto.

**Viabilidad operativa y el riesgo que la condiciona.** El alcance está acotado a un programa, un
periodo ya cerrado, datos existentes y 12 semanas, sin captura nueva de información. El riesgo
dominante no es técnico sino **de acceso a los datos**: si la autorización institucional no llega en
las primeras dos semanas, la ruta principal se detiene. Por eso se declara desde ahora la ruta de
contingencia —construir y evaluar el prototipo sobre un conjunto de datos sintético calibrado con
estadísticos agregados que la institución sí pueda entregar—, que conserva el prototipo, la
arquitectura, el protocolo y las salvaguardas, pero **convierte la validación retrospectiva en una
prueba de funcionamiento sin valor predictivo real**. Es una degradación seria y se nombra como tal,
no se disimula: la propuesta con valor pleno es la que accede a los datos reales.

### Aplicación de herramientas IA

| Herramienta IA | Cómo se proyecta utilizarla y qué impactos puede generar |
|---|---|
| **Modelo de lenguaje de pesos abiertos servido en infraestructura controlada** — configuración principal: **Llama 3.1 8B Instruct** (Meta) servido con **Ollama** o **vLLM** | Es el generador de la capa conversacional: redacta la explicación de la alerta y la recomendación de ruta de apoyo, **exclusivamente a partir de los fragmentos recuperados** y de los indicadores que le entrega el canal determinista. Se elige un modelo de pesos abiertos como configuración principal por una razón de protección de datos, no de costo: permite que ningún dato de estudiante —ni seudonimizado— salga de la infraestructura que la institución autorice. Impacto: hace posible el proyecto bajo un criterio restrictivo de tratamiento de datos, y hace replicable el prototipo sin dependencia de proveedor. La versión exacta del modelo se fija al inicio de la ejecución y se registra, porque el desempeño no es comparable entre versiones. |
| **Servicio comercial de modelo de lenguaje como contraste** — **GPT-4o mini** (OpenAI) o **Claude** (Anthropic), vía API | Se usa **solo como línea de comparación de calidad de redacción y de fidelidad a la fuente**, y **solo sobre casos sintéticos o completamente desidentificados**, nunca sobre datos de estudiantes reales. Impacto: permite reportar cuánto se pierde (o no) al operar con un modelo local, dato que la institución necesita para decidir la configuración de un eventual despliegue. Si el pendiente 7 se resuelve prohibiendo servicios de terceros incluso con datos desidentificados, este contraste se elimina y así se reporta. |
| **Orquestación de recuperación aumentada** — **LangChain** o **LlamaIndex**, base vectorial **FAISS** o **Chroma**, incrustaciones multilingües de la familia **sentence-transformers** | Construyen el índice sobre el corpus documental institucional (Syllabus vigente del programa piloto, reglamento estudiantil en lo pertinente a evaluación y permanencia, rutas y servicios de apoyo, calendario académico) y recuperan los fragmentos que sostienen cada afirmación de la respuesta. Impacto: es el mecanismo concreto por el cual una recomendación queda **trazable a un documento institucional citable** en lugar de ser una opinión del modelo; sin esta capa, el asistente sería un generador de consejos genéricos. |
| **Clasificador interpretable de riesgo** — **scikit-learn**: regresión logística regularizada y árbol de decisión de profundidad limitada, con **pandas** para la ingeniería de variables | Producen la señal de riesgo a partir de calificaciones parciales, asistencia y actividad en el aula virtual. Se eligen modelos interpretables por construcción —coeficientes y reglas legibles— en lugar de un modelo de mayor capacidad y menor transparencia, porque la explicación que el asistente entrega debe corresponder a lo que el modelo realmente usó. Impacto: la explicación no es una narrativa plausible construida a posteriori, sino la lectura de un modelo auditable. |
| **Instrumentación de evaluación del componente RAG** — anotación humana con apoyo de **Ragas** u equivalente | Se calculan indicadores de fidelidad a la fuente y de pertinencia de los fragmentos recuperados. Se declara la limitación: estas métricas se calculan con un modelo de lenguaje como juez, de modo que **no se aceptan como evidencia por sí solas**; el indicador que se reporta como resultado es el de anotación humana sobre 100 respuestas, con doble anotación del 30 % y fiabilidad reportada. Impacto: evita el circuito cerrado de usar un modelo para certificar a otro modelo. |
| **Asistentes de IA generativa en la construcción del proyecto** — **Claude** (Anthropic) y **ChatGPT** (OpenAI) | Apoyo en la escritura y depuración de código del prototipo, en la depuración de la búsqueda bibliográfica con verificación manual de cada fuente, y en la codificación preliminar de las respuestas abiertas de los instrumentos, con codificación humana de contraste y reporte de acuerdo. Impacto: acorta el tiempo de desarrollo y de análisis sin delegar la validación. Todos estos usos quedan registrados en una bitácora de uso de IA y declarados en la lista de referencias. |

**Lo que la IA no hará en este proyecto, por diseño.** El modelo de lenguaje **no calcula el riesgo**
—eso lo hace código auditable—, **no escribe datos duros** —fechas, notas, pesos de evaluación y
umbrales los inserta el canal determinista a partir de la fuente institucional—, **no decide** sobre
la situación académica de ningún estudiante, y **no se dirige a estudiantes identificados durante el
piloto**: toda salida del prototipo pasa por revisión humana antes de considerarse utilizable. Estas
cuatro exclusiones no son una precaución retórica; son las que permiten distinguir, en los resultados,
un error de modelado de un error de configuración, y las que hacen presentable el proyecto ante el
Comité de Ética.

---

## Antecedentes generales de la propuesta

### Antecedentes teóricos y de investigación consultados

El estudio del abandono en educación superior tiene un marco de referencia estable desde el modelo de
integración académica y social de Tinto [1], que explica la decisión de abandonar no como un evento
súbito sino como el resultado de una trayectoria de desvinculación progresiva. Ese punto de partida
importa para esta propuesta por una consecuencia operativa: si el abandono es un proceso, deja rastros
observables antes de consumarse, y el problema deja de ser predecir un destino para convertirse en
**detectar el proceso mientras ocurre**. En Colombia, el seguimiento sistemático de esas trayectorias
se institucionalizó con el sistema de información del Ministerio de Educación Nacional para la
prevención de la deserción (SPADIES) [2], que provee el marco conceptual y los indicadores con los que
el país mide el fenómeno; este proyecto no reemplaza ese marco: opera dentro del periodo académico, en
la escala de la asignatura y de la semana, que es la escala en la que un docente-tutor puede actuar y
que un reporte nacional agregado no cubre.

La instrumentación de esa idea es el campo de la analítica de aprendizaje, cuya constitución como
disciplina sistematiza Siemens [3], y su expresión más citada como sistema de alerta temprana es
Course Signals, descrito por Arnold y Pistilli [4]: un semáforo por estudiante calculado a partir de
desempeño, esfuerzo, historia académica y características, con la particularidad —relevante aquí— de
que el valor del sistema no estaba en el color del semáforo sino en el mensaje que el docente enviaba
a partir de él. Del lado técnico, la revisión de Prenkaj *et al.* [5] sistematiza los enfoques de
aprendizaje automático para predicción de abandono en cursos en línea y documenta un patrón
consistente: las variables de comportamiento y de interacción con la plataforma aportan poder
predictivo temprano que las calificaciones, por definición tardías, no pueden aportar. Aulck *et al.*
[6] muestran que con datos administrativos ordinarios —los que una institución ya tiene— se obtienen
modelos útiles sin instrumentación adicional, lo que es exactamente la premisa de viabilidad de esta
propuesta. Y Kizilcec y Halawa [7] documentan brechas de abandono y de logro en entornos con
componente virtual, evidencia pertinente para un programa de modalidad virtual como el del piloto y
para la exigencia de examinar el comportamiento de la señal por subgrupos.

Sobre el uso de inteligencia artificial en educación superior, la revisión sistemática de
Zawacki-Richter *et al.* [8] agrupa el campo en cuatro dominios —perfilado y predicción, evaluación,
sistemas adaptativos y sistemas tutores— y advierte que la discusión pedagógica y ética suele quedar
en segundo plano frente a la técnica. Esta propuesta se ubica en el primero de esos dominios pero
incorpora deliberadamente la advertencia: la mitad de sus indicadores de impacto son de
verificabilidad, equidad y utilidad, no de exactitud.

La novedad técnica que hace posible el componente conversacional es la generación aumentada por
recuperación introducida por Lewis *et al.* [9]: en lugar de confiar en el conocimiento paramétrico del
modelo, se recuperan fragmentos de un corpus documental y se condiciona la generación a ellos. Esa
elección arquitectónica responde directamente a dos riesgos documentados. El primero es la alucinación,
revisada exhaustivamente por Ji *et al.* [10] como contenido fluido pero infiel a la fuente o no
verificable; en un mensaje que un estudiante recibirá como palabra institucional, una recomendación
inventada —un plazo que no existe, un servicio que no se presta— es un daño concreto. El segundo es el
sesgo: Mehrabi *et al.* [11] sistematizan sus fuentes en datos y algoritmos, Baker y Hawn [12] lo
tratan específicamente en educación y muestran que los modelos educativos pueden rendir de forma
desigual entre grupos incluso cuando su desempeño global es bueno, y Gardner *et al.* [13] aportan un
procedimiento concreto —análisis por segmentos— para auditarlo en modelos de estudiantes. De ahí sale
un indicador obligatorio de este proyecto, no un apartado de buenas intenciones.

Dos decisiones de diseño más se apoyan en la literatura. La primera es usar un modelo **interpretable
por construcción** en lugar de un modelo opaco con explicación posterior, siguiendo el argumento de
Rudin [14] para decisiones de alto impacto: en un dominio donde la explicación es el producto, una
explicación aproximada de un modelo opaco es un riesgo, no una solución. La segunda es la gobernanza:
la Ley Estatutaria 1581 de 2012 [15] fija en Colombia las obligaciones de autorización, finalidad y
seguridad en el tratamiento de datos personales, y a ellas se suman las exigencias convergentes de la
orientación de la UNESCO sobre IA generativa en educación e investigación [16] y de la política
nacional de transformación digital e inteligencia artificial [17] —control humano de las decisiones,
protección de datos y transparencia—. En esta propuesta se traducen en obligaciones verificables:
revisión humana previa a cualquier contacto, datos crudos y seudonimización dentro de la
infraestructura que la institución autorice, y trazabilidad de cada afirmación generada a su fuente.

**El vacío que ocupa esta propuesta.** Existe abundante literatura sobre predicción de abandono y
abundante literatura sobre modelos generativos en educación, pero muy poca que **integre las dos capas
y evalúe la integración**: sistemas que predicen sin explicar de forma verificable, o asistentes
conversacionales que explican sin estar anclados a la situación académica real y a la normativa de la
institución. La contribución de este proyecto no es un algoritmo nuevo: es la evaluación de una
arquitectura que separa el cálculo del riesgo (determinista y auditable) de su comunicación
(generativa y anclada a documento), medida en un caso institucional real y en español, con las métricas
de verificabilidad y de equidad que esa integración exige.

### Antecedentes en la CUN

No se identificaron proyectos CUN documentados que hayan construido y evaluado un sistema de detección
temprana de riesgo académico con modelos de lenguaje. Y una precisión que conviene hacer por delante:
**este anteproyecto no dispone de cifras institucionales de deserción, pérdida de asignaturas o
cobertura de alertas de la CUN, y no las inventa.** La línea base cuantitativa se establece en el
primer objetivo específico, con las fuentes que la institución autorice; cualquier cifra que apareciera
aquí sin ese respaldo sería una afirmación sin verificación y debilitaría el resto del documento.

Sí existen tres antecedentes institucionales pertinentes y verificables. El primero es que la
institución ya opera los insumos que el prototipo necesita: hay Syllabus institucional por asignatura,
libro de calificaciones con ítems y pesos, registro de asistencia y un aula virtual con traza de
actividad; el proyecto no propone crear fuentes de datos, propone usar las existentes. El segundo es
normativo y está en esta misma convocatoria: el numeral 11.1 de los Términos de Referencia establece
que las propuestas serán evaluadas "por Inteligencia Artificial, en primer lugar", lo que evidencia
que la institución ya incorpora estas herramientas en procesos de decisión académica y hace más
pertinente —no menos— que exista dentro de la CUN evidencia propia sobre cómo auditarlas. El tercero es
el propio proponente: en esta misma convocatoria el investigador estructura otras propuestas sobre
aplicación de IA a funciones institucionales, independientes de esta en objeto, método y presupuesto,
y con las que esta no comparte productos comprometidos ni duplica ningún rubro de este presupuesto.

### Punto de partida real del proyecto

Por transparencia, y a diferencia de otra de las propuestas del mismo investigador, aquí **no hay
artefacto preexistente**: el prototipo no existe y se construye íntegramente dentro del proyecto. Eso
tiene una consecuencia que conviene declarar en vez de dejar que la descubra el evaluador: el riesgo de
ejecución es mayor que en un estudio sobre algo ya construido. Se controla con tres decisiones. (a) El
alcance del software es deliberadamente pequeño: un canal de datos, un clasificador interpretable, un
índice documental y una interfaz conversacional mínima; nada de integración con sistemas en producción,
nada de autenticación institucional, nada de despliegue multiusuario. (b) Se usan componentes maduros y
disponibles, sin entrenamiento de modelos desde cero ni ajuste fino. (c) El primer entregable de valor
—la definición operativa de riesgo validada con el área de permanencia y el conjunto de datos
inventariado— se produce en las primeras semanas y **conserva valor institucional incluso si el
prototipo rindiera por debajo de lo esperado**.

## Planteamiento del problema de investigación

Cuando un estudiante de un programa virtual deja de entrar al aula, deja de entregar y empieza a perder
evaluaciones parciales, la institución casi siempre lo sabe: la información está en sus sistemas. El
problema es **cuándo** lo sabe y **quién** lo sabe. En la práctica corriente, el dato se vuelve visible
en el corte de notas, cuando el estudiante ya perdió una parte del curso y el margen de recuperación
—académico, administrativo y motivacional— se ha estrechado. Antes de ese corte, la señal existe pero
está dispersa en tres lugares que nadie cruza sistemáticamente: la planilla de calificaciones, el
registro de asistencia y la traza de actividad del aula virtual. Cruzarlos a mano, semana a semana, para
todos los grupos de un programa, es un trabajo que ninguna carga docente ordinaria absorbe. El
resultado no es negligencia: es una capacidad de revisión estructuralmente inferior al volumen que
habría que revisar.

De ahí se derivan tres carencias concretas, y las tres tienen que ver con información, no con voluntad.
La primera es de **oportunidad**: la alerta llega tarde porque se apoya en la variable más tardía de
todas, la calificación consolidada, cuando la literatura muestra que las variables de comportamiento
—accesos, entregas, participación— se mueven antes [5]. La segunda es de **cobertura**: la revisión
manual privilegia los casos evidentes y deja fuera a los estudiantes que se desvinculan sin llamar la
atención, que es precisamente el patrón de desvinculación progresiva que describe Tinto [1] y el que un
entorno virtual facilita [7]. La tercera es de **accionabilidad**: incluso cuando la alerta se produce,
suele consistir en un nombre y un número. Un puntaje de riesgo no le dice al estudiante qué hacer, ni
al docente-tutor por qué ese estudiante y no otro, ni a cuál de las rutas de apoyo institucionales
remitirlo. Lo que convierte una alerta en una intervención es una explicación con contexto normativo y
curricular, y eso hoy lo escribe una persona, caso por caso, o no se escribe.

La tentación inmediata es resolverlo con las herramientas disponibles hoy: un modelo predictivo
comercial, o un asistente conversacional de propósito general al que se le pida "redactar
recomendaciones para estudiantes en riesgo". Ambos caminos fallan de forma predecible, y por razones
documentadas. Un modelo predictivo genérico produce un puntaje sin contexto institucional, no conoce el
Syllabus de la asignatura ni el reglamento ni las rutas de apoyo de la CUN, y si es opaco su
explicación posterior es una aproximación —el argumento de Rudin contra usar modelos de caja negra en
decisiones de alto impacto [14]—. Un asistente generativo sin anclaje documental produce texto fluido y
puede inventar plazos, servicios o normas que no existen: es el fenómeno de la infidelidad a la fuente
[10], y en un mensaje que el estudiante lee como voz institucional el error no es un detalle de calidad,
es una desinformación con consecuencias. A esos dos riesgos se suma un tercero, el **sesgo**: un modelo
entrenado sobre desenlaces históricos puede rendir peor para determinados grupos de estudiantes sin
que el desempeño global lo revele [12], y un sistema que concentra falsos positivos en un subgrupo
convierte el acompañamiento en estigmatización. Auditar eso requiere análisis por segmentos [13], que
casi nunca se hace.

Hay, finalmente, un problema de **gobernanza** que no puede quedar implícito. Un sistema que clasifica
a personas por su riesgo de fracaso académico trata datos personales sensibles en su efecto práctico,
y toca directamente la exigencia de control humano sobre decisiones que afectan a individuos y la
protección de datos que impone la Ley Estatutaria 1581 de 2012 [15] y que las orientaciones
internacionales sobre IA en educación reiteran [16], [17]. La pregunta institucional no es solo si el
sistema acierta: es también quién ve la alerta, qué se le dice al estudiante, quién decide, qué se
registra y qué garantiza que la alerta no se convierta en una etiqueta. Sin esas respuestas escritas
antes de construir, un prototipo técnicamente correcto es institucionalmente inadoptable.

En síntesis, el problema no es la ausencia de datos ni la ausencia de tecnología: es que los datos que
la institución ya tiene no se convierten, a tiempo y de forma verificable, en una explicación
accionable para la persona que puede actuar. Y no existe, dentro de la CUN, evidencia propia que
permita decidir si una arquitectura que separe el cálculo auditable del riesgo de su comunicación
generativa anclada a documento institucional funciona, con cuánta antelación, con qué error y con qué
garantías.

## Formulación del problema de investigación

**Pregunta central:** ¿en qué medida un prototipo de asistente conversacional que calcula el riesgo
académico con un modelo interpretable sobre datos institucionales existentes y comunica sus resultados
mediante generación aumentada por recuperación anclada a documentos de la CUN permite detectar el
riesgo académico antes que la práctica actual de corte de notas, con qué error, con qué verificabilidad
de sus explicaciones, con qué comportamiento entre subgrupos de estudiantes y bajo qué condiciones de
gobernanza resultaría adoptable?

Preguntas derivadas, una por objetivo específico:

1. ¿Qué variables disponibles en las fuentes institucionales del programa piloto —calificaciones
   parciales, asistencia y actividad en el aula virtual— componen una definición operativa de riesgo
   académico que el área de permanencia reconozca como útil, y cuál es la práctica de referencia contra
   la que debe compararse cualquier alerta anticipada?
2. ¿Es posible construir un prototipo que calcule esa señal con un modelo interpretable y genere, para
   cada caso, una explicación y una recomendación cuyas afirmaciones sean atribuibles a un fragmento
   recuperado de documento institucional, sin que el modelo de lenguaje escriba datos duros ni decida?
3. ¿Qué desempeño de detección, qué anticipación en semanas, qué verificabilidad, qué diferencias entre
   subgrupos y qué utilidad percibida por docentes-tutores alcanza el prototipo en una validación
   retrospectiva, y qué salvaguardas mínimas exigiría su adopción institucional?

## Justificación

**Para la institución.** La permanencia estudiantil se gestiona con la información que llega a tiempo,
y hoy la que llega a tiempo no se está usando. Esta propuesta no pide a la institución que confíe en
una promesa: entrega un prototipo funcional y, sobre todo, **la medida de cuánto sirve** —cuántas
semanas de anticipación, a qué costo de falsos positivos, con qué comportamiento entre subgrupos—, que
es la información que una decisión de inversión necesita y que ningún proveedor externo puede aportar
sobre los datos de la CUN. El costo es bajo ($3.850.000, el 77 % del techo) y no compromete
infraestructura permanente. Y hay un retorno que no depende del desempeño del prototipo: el protocolo
de tratamiento de datos, la definición operativa de riesgo acordada con el área de permanencia y la
lista de salvaguardas quedan como activos institucionales aun si las métricas resultan modestas.

**Para el estudiante, que es el destinatario final.** El valor no está en ser clasificado antes, sino
en recibir antes una indicación concreta y correcta: qué evaluación está pendiente, qué peso tiene en
la nota final, qué plazo aplica según el reglamento y a qué servicio de apoyo puede acudir. Esa es la
diferencia entre una alerta y una intervención, y es la razón de que la capa generativa esté anclada a
documento en lugar de generar texto libre: un consejo genérico no ayuda, y un consejo inventado
perjudica. La propuesta incorpora además, desde el diseño y no como cláusula, la protección del
estudiante: seudonimización, ninguna decisión automatizada, revisión humana obligatoria y —durante el
piloto— **ninguna alerta emitida sobre estudiantes identificados**.

**Para la práctica docente y la gestión académica.** El docente-tutor recibe un insumo redactado y
trazable en lugar de una planilla que debe interpretar. Si la evaluación muestra que esa explicación no
le resulta más útil que un puntaje, el proyecto lo reportará: la utilidad percibida es un indicador
declarado, con su condición de refutación, no un supuesto.

**Desde el rol profesional del investigador.** Como docente de la Especialización en Inteligencia
Artificial, el investigador enseña a evaluar sistemas de IA con métricas, líneas base y auditoría de
sesgo, no con entusiasmo. Construir un sistema de alto impacto sobre personas y someterlo al mismo
examen que exige en clase —línea base explícita, intervalos de confianza, análisis por subgrupos,
verificabilidad de la salida generada y publicación de las condiciones de refutación— es la aplicación
consistente de ese criterio y produce material de aula directamente reutilizable en las asignaturas de
IA y de formación investigativa.

**Por qué ahora y por qué en este instrumento.** Los componentes técnicos son maduros y de bajo costo;
los datos ya existen; y la decisión institucional que está pendiente —si vale la pena invertir en
analítica de permanencia y con qué garantías— se toma mejor con evidencia interna que con una
demostración comercial. Doce semanas y $3.850.000 no alcanzan para un despliegue, pero alcanzan
exactamente para lo que falta: un prototipo evaluado y las reglas de su uso.

## Alcance de la propuesta

**Inicio y fin.** El proyecto inicia con la gestión de la autorización de datos y la validación de la
definición operativa de riesgo con el área de permanencia (Semana 1) y termina con la entrega del
prototipo funcional, la arquitectura documentada, el informe de validación retrospectiva, el protocolo
de tratamiento de datos y la lista de salvaguardas (Semana 12).

**Lo que queda dentro.**

1. **Un solo programa académico y un solo periodo académico ya cerrado**, con los estudiantes que
   estuvieron matriculados en ese periodo, sobre datos **ya existentes** en los sistemas
   institucionales. No hay captura nueva de información sobre estudiantes.
2. **Tres familias de variables**: calificaciones parciales y su peso en el libro de calificaciones,
   asistencia registrada y actividad en el aula virtual (accesos, entregas, oportunidad de entrega).
3. **Un clasificador interpretable** (regresión logística regularizada y árbol de decisión de
   profundidad limitada) y una **línea base explícita**: la regla de corte de notas que representa la
   práctica actual. Toda métrica se reporta contra esa línea base.
4. **Una capa conversacional con recuperación aumentada** sobre un corpus documental institucional
   acotado: Syllabus vigente del programa piloto, apartados del reglamento estudiantil relativos a
   evaluación y permanencia, catálogo de rutas y servicios de apoyo, y calendario académico.
5. **Validación retrospectiva** contra los desenlaces conocidos del periodo (pérdida de asignatura,
   retiro, aprobación), con reporte de sensibilidad, precisión, valor predictivo negativo, área bajo la
   curva ROC, **prevalencia observada del desenlace**, semanas de anticipación e intervalos de
   confianza.
6. **Auditoría de la capa generativa**: anotación humana de la atribución a fuente de las afirmaciones
   factuales en 100 respuestas generadas, con doble anotación del 30 % y fiabilidad reportada.
7. **Análisis de equidad por segmentos** con las variables que la institución autorice.
8. **Evaluación de utilidad con docentes-tutores** (mínimo 6) sobre casos reales seudonimizados de un
   periodo cerrado, en comparación pareada contra un puntaje sin explicación, y **prueba de usabilidad
   con estudiantes voluntarios (mínimo 10) sobre perfiles sintéticos**, no sobre su propia situación.
9. **Protocolo de tratamiento de datos y lista de salvaguardas** de gobernanza: seudonimización, no
   decisión automatizada, revisión humana previa, declaración de uso de IA, registro de trazabilidad y
   procedimiento de rectificación.

**Lo que queda fuera, de forma explícita.**

- **(a) No se mide reducción de la deserción ni mejora de la permanencia.** Establecer ese efecto exige
  intervención real, grupo de comparación y seguimiento de al menos un semestre. Este proyecto mide la
  calidad de la señal y de su explicación, que es la condición previa, no el efecto.
- **(b) No se emiten alertas sobre estudiantes identificados durante el piloto** y no se contacta a
  ningún estudiante a partir de una salida del prototipo. La evaluación es retrospectiva sobre un
  periodo cerrado; la usabilidad con estudiantes se hace sobre perfiles sintéticos. Esta exclusión es
  una decisión ética, no una limitación de recursos: un prototipo sin validar no debe decirle a una
  persona real que va a fracasar.
- **(c) No se integra con los sistemas académicos en producción** ni en tiempo real. No hay
  autenticación institucional, no hay despliegue multiusuario y no hay puesta en operación. El
  entregable es un prototipo evaluado, no un servicio.
- **(d) No se despliega en más de un programa ni en más de una sede.** Lo transferible es la
  arquitectura y el protocolo; las métricas describen el programa piloto.
- **(e) No se cubre la modalidad presencial.** Sin traza de actividad en aula virtual, el conjunto de
  variables cambia y el desempeño no sería comparable; se documenta qué faltaría para adaptarlo.
- **(f) No se entrena un modelo de lenguaje desde cero ni se hace ajuste fino**, y no se compara el
  desempeño de modelos de lenguaje entre sí como objeto de estudio: el único contraste entre modelos es
  instrumental y sobre datos desidentificados o sintéticos.
- **(g) No se recogen datos socioeconómicos, psicológicos ni de salud** de los estudiantes, aunque la
  literatura los asocia al abandono. Quedan fuera porque su tratamiento exige un marco de protección
  mayor y porque el proyecto se limita, por diseño, a lo que la institución ya registra con finalidad
  académica.
- **(h) No se produce material de enseñanza ni se interviene el diseño curricular.**

**Supuestos.** La institución autoriza el acceso a un extracto seudonimizado de los registros del
periodo cerrado (pendiente 5); el Comité de Ética avala el proyecto y los instrumentos (pendiente 6);
la plataforma de aula virtual expone traza de actividad exportable (pendiente 8); el área de
permanencia dispone de tiempo para validar la definición operativa de riesgo en las primeras semanas; y
la descarga horaria aprobada permite dedicar el tiempo previsto.

**Ruta de contingencia declarada.** Si la autorización de datos no se obtiene en las dos primeras
semanas, el proyecto continúa sobre un **conjunto de datos sintético calibrado con estadísticos
agregados** que la institución pueda entregar sin exponer registros individuales. Se conservan el
prototipo, la arquitectura, el protocolo y las salvaguardas; se conserva la auditoría de la capa
generativa, que no depende de datos reales; y **se pierde la validez de la validación retrospectiva**,
que pasa a reportarse como prueba de funcionamiento sin valor predictivo. La activación de esta ruta se
informa a la DNI porque cambia el objeto de la evaluación.

---

## Objetivo general de la propuesta

Construir y evaluar retrospectivamente un prototipo de asistente conversacional para la detección
temprana de riesgo académico en un programa piloto de la CUN, que calcule la señal de riesgo con un
modelo interpretable sobre datos institucionales existentes y comunique sus resultados mediante
generación aumentada por recuperación anclada a documentos institucionales, determinando su
anticipación frente a la práctica actual, su error, la verificabilidad de sus explicaciones y su
comportamiento entre subgrupos, y formulando las salvaguardas de gobernanza para su eventual adopción,
en un plazo de 12 semanas.

## Objetivos específicos de la propuesta

1. **Caracterizar** las variables de riesgo académico disponibles en las fuentes institucionales del
   programa piloto —calificaciones parciales y su peso, asistencia y actividad en el aula virtual—,
   **constituir** el conjunto de datos seudonimizado de un periodo académico cerrado y **acordar** con
   el área de bienestar y permanencia la definición operativa de riesgo y la línea base de comparación
   (la regla de corte de notas vigente), durante las semanas 1 a 4 de ejecución.
2. **Desarrollar** el prototipo del asistente en dos capas verificables —un canal determinista que
   calcula la señal de riesgo con un modelo interpretable y una capa de generación aumentada por
   recuperación que produce la explicación y la recomendación atribuibles a fragmentos del corpus
   documental institucional—, con su arquitectura documentada y su protocolo de tratamiento de datos,
   entre las semanas 3 y 9 de ejecución.
3. **Evaluar** el prototipo en validación retrospectiva —desempeño de detección y semanas de
   anticipación frente a la línea base, verificabilidad de las afirmaciones generadas por anotación
   humana con fiabilidad reportada, y diferencias de error entre subgrupos— y **valorar** su utilidad
   con docentes-tutores y su usabilidad con estudiantes voluntarios sobre perfiles sintéticos, para
   **formular** la lista de salvaguardas y la guía de adopción institucional, entre las semanas 7 y 12
   de ejecución.

*El cumplimiento conjunto de los tres objetivos específicos constituye el objetivo general:* el OE1
produce la definición y los datos sin los cuales no hay nada que calcular; el OE2 produce el artefacto
que el objetivo general nombra; y el OE3 produce las cuatro medidas (anticipación, error,
verificabilidad, equidad) y las salvaguardas que el objetivo general exige. Ninguno es prescindible y
ninguno duplica a otro.

## Hipótesis

El tipo de propuesta es "Desarrollo de Software" y su núcleo es la construcción de un artefacto, de
modo que buena parte del trabajo no es contrastable en sentido estricto: un prototipo se construye o no
se construye. Pero su **componente de evaluación sí admite proposiciones falsables**, y declararlas por
adelantado —con su condición de refutación— es lo que impide que la evaluación termine describiendo
solo lo que favorece al autor del prototipo. Se declaran cuatro, más una que deliberadamente no se
formula.

- **H1 (anticipación y desempeño de detección).** Con los datos disponibles hasta un punto de corte
  intermedio del periodo académico —fijado en el OE1 y anterior al primer corte de notas—, el
  clasificador interpretable identifica los casos que terminaron en pérdida de asignatura o retiro con
  **mayor sensibilidad que la línea base** (la regla de corte de notas vigente) **sin degradar la
  precisión por debajo del valor de esa línea base**, y con una anticipación mediana de al menos **tres
  semanas**. *Se refuta* si la sensibilidad no supera la de la línea base, si la ganancia en
  sensibilidad se obtiene a costa de una caída de precisión que multiplique los falsos positivos por
  encima de la capacidad de atención declarada por el área de permanencia, o si la anticipación mediana
  es menor a tres semanas. **Los umbrales absolutos no se fijan aquí a propósito:** dependen de la
  prevalencia real del desenlace, que solo se conoce al constituir el conjunto de datos en el OE1. Lo
  que sí queda fijado por adelantado es la **regla de decisión** —superar la línea base en sensibilidad
  a precisión no inferior— y el compromiso de registrar los umbrales concretos en un acta previa a la
  evaluación, para que no puedan ajustarse después de ver los resultados.
- **H2 (verificabilidad de la capa generativa).** Al menos el **95 %** de las afirmaciones factuales
  contenidas en las explicaciones y recomendaciones generadas es atribuible por un anotador humano a un
  fragmento recuperado del corpus documental institucional o a un indicador entregado por el canal
  determinista. *Se refuta* si la proporción atribuible queda por debajo de ese umbral en la muestra de
  100 respuestas anotadas. Se declara además una expectativa **más fuerte y más fácil de refutar** sobre
  los datos duros: la tasa de error en fechas, notas, pesos de evaluación y umbrales debe ser **cero**,
  porque esos valores no los escribe el modelo de lenguaje sino el canal determinista; **un solo error
  de dato duro refuta la premisa arquitectónica del prototipo** y obliga a reportarlo como defecto de
  diseño, no como imprecisión del modelo.
- **H3 (equidad de la señal).** La diferencia en tasa de falsos positivos entre los subgrupos definidos
  por las variables que la institución autorice (modalidad, jornada, rango de edad, sede de matrícula)
  no supera **10 puntos porcentuales**. *Se refuta* si alguna comparación entre subgrupos con n
  suficiente supera ese margen; en ese caso el hallazgo se reporta como resultado principal y no como
  nota al pie, y el prototipo se declara **no adoptable en su configuración evaluada** hasta corregirlo.
  Esta hipótesis es **condicional a la disponibilidad de las variables**: si la institución no autoriza
  alguna, se declara como no evaluada, con el nombre de la variable faltante, en lugar de omitir la
  comparación en silencio.
- **H4 (utilidad de la explicación frente al puntaje).** En comparación pareada, los docentes-tutores
  valoran la explicación generada como más accionable que un puntaje de riesgo sin explicación, con una
  diferencia estadísticamente detectable en la muestra disponible. *Se refuta* si no hay diferencia o
  si la diferencia favorece al puntaje solo. Se declara desde ahora que con seis a diez participantes
  el estudio **no tiene potencia** para estimar la magnitud del efecto: un resultado sin diferencias se
  reportará como ausencia de evidencia, no como prueba de equivalencia.

**La hipótesis que no se formula, y por qué.** No se formula ninguna hipótesis sobre **reducción de la
deserción, mejora de la permanencia o efecto en el aprendizaje**. No es una omisión: es que este diseño
no puede contrastarla —no hay intervención, no hay grupo de comparación y no hay seguimiento
longitudinal— y formularla sería comprometer ante la DNI un resultado que el proyecto no puede entregar.
Esa hipótesis corresponde a un estudio posterior, para el cual este proyecto produce precisamente lo
que le falta: el instrumento validado, la línea base y las salvaguardas.

---

## Marco teórico

*(Extensión requerida: 1.500 a 2.000 palabras. Conteo real verificado con `wc -w` sobre el cuerpo de
texto extraído de esta sección, sin contar los subtítulos de apartado ni esta nota: **1.958
palabras**.)*

### El abandono como proceso y la analítica de aprendizaje como instrumento

Tinto [1] describe el abandono como el desenlace de un proceso de desvinculación académica y social,
no como una decisión súbita atribuible a un rasgo del estudiante. De ahí la consecuencia que ordena
todo el diseño: un proceso deja rastros observables antes de consumarse, de modo que la unidad de
análisis es la **trayectoria** —el comportamiento semana a semana dentro del periodo— y no el
estudiante como caso estático. Se busca detectar la pendiente, no el punto.

Ese desplazamiento choca con una limitación de escala. El sistema de información para la prevención
de la deserción [2] mide el fenómeno por cohortes y periodos: es el marco del diagnóstico agregado,
pero su resolución no es la de la semana ni la de la asignatura, que es donde un docente-tutor puede
intervenir. El vacío es de instrumentación en la escala operativa, y es el que ocupa esta propuesta.

La disciplina que se ocupa de esa escala es la analítica de aprendizaje, que Siemens [3] define en
torno a la medición y el análisis de datos de los entornos de aprendizaje para comprender y
**optimizar** el proceso, con el énfasis en la acción como rasgo constitutivo. Su realización más
citada como alerta temprana es Course Signals, de Arnold y Pistilli [4], y su aporte aquí está en
dos lecturas. El valor del sistema no residía en el color del semáforo sino en el **mensaje** que el
docente enviaba a partir de él: la comunicación no es el envoltorio del cálculo, es parte del
artefacto. Y sus estimaciones de retención provienen de diseños observacionales sin asignación
controlada, que no autorizan inferencia causal fuerte; de ahí que este proyecto no prometa efectos
sobre la permanencia.

### Predicción de riesgo con datos administrativos: lo establecido y lo que no se puede comparar

La revisión de Prenkaj *et al.* [5] organiza los enfoques de aprendizaje automático para predicción
de abandono en cursos en línea y deja dos resultados. El primero, sustantivo: las variables de
interacción con la plataforma aportan capacidad de anticipación que las calificaciones consolidadas,
tardías por definición, no pueden aportar; de ahí que el conjunto de variables integre la traza del
aula virtual y no solo la planilla. El segundo, metodológico: las definiciones de "abandono", los
horizontes de predicción y las particiones varían de estudio a estudio, de modo que las cifras
absolutas de sensibilidad o de área bajo la curva **no son comparables entre trabajos**. Ahí está la
justificación de no fijar umbrales absolutos por adelantado y de evaluar contra una **línea base
interna** —la regla de corte de notas vigente— medida sobre los mismos datos y con la misma
definición de desenlace.

Aulck *et al.* [6] muestran que datos administrativos ordinarios sostienen modelos de utilidad
práctica sin instrumentación adicional: es la premisa de viabilidad de este proyecto. Kizilcec y
Halawa [7] documentan brechas sistemáticas de abandono y de logro en entornos con componente
virtual; en un programa de modalidad virtual eso convierte el análisis por subgrupos en obligación
del diseño. Y la revisión de Zawacki-Richter *et al.* [8] sitúa el conjunto: el campo de la
inteligencia artificial en educación superior está dominado por el perfilado y la predicción,
mientras la discusión pedagógica y ética se trata con superficialidad; esta propuesta se ubica en
ese dominio pero invierte la proporción, porque tres de sus seis indicadores de impacto miden
verificabilidad, equidad y utilidad, no exactitud.

### Cómo se mide bien un detector de eventos poco frecuentes

El desenlace que se intenta anticipar es minoritario: la mayoría de los estudiantes no pierde la
asignatura ni se retira. En ese régimen de clases desbalanceadas la exactitud global es engañosa —un
clasificador que niegue todo riesgo la maximiza— y el área bajo la curva ROC tampoco es inocua.
Davis y Goadrich [18] establecen la relación formal entre el espacio ROC y el de
precisión-exhaustividad: la dominancia de una curva se conserva, pero la magnitud de las diferencias
no, de modo que dos modelos con ROC casi idénticas pueden diferir decisivamente en precisión cuando
la clase positiva es rara. Saito y Rehmsmeier [19] cuantifican ese efecto: la tasa de falsos
positivos se diluye en un número grande de negativos y oculta el volumen de alertas incorrectas que
alguien tendría que atender. De ahí que las métricas se reporten en conjunto —sensibilidad,
precisión, valor predictivo negativo, área bajo la curva ROC y prevalencia observada— y contra la
línea base.

El punto de operación tampoco es una decisión libre del modelador: elegir el umbral es elegir la
razón entre falsos positivos y falsos negativos que la institución asume, y esa razón depende de la
capacidad de atención del área de permanencia —una alerta que nadie puede atender no es una alerta—;
por eso se fija con el área responsable y se registra en acta previa, lo que impide ajustarlo
después de ver los resultados. Rudin [14] añade el criterio de familia de modelos: en decisiones de
alto impacto sobre personas debe preferirse uno interpretable por construcción antes que uno opaco
con explicación posterior, que aproxima al modelo pero no es el modelo. El argumento pesa aquí
porque la explicación **es el producto** que el docente-tutor recibe. De ahí la restricción a
regresión logística regularizada y árboles de profundidad limitada. La **anticipación en semanas**,
por último, carece de definición canónica, así que se define operativamente y se reporta con mediana
y rango.

### De la equidad como principio a la equidad como indicador

Que un modelo funcione en promedio no implica que funcione igual para todos. Mehrabi *et al.* [11]
sistematizan las fuentes de sesgo en datos y algoritmos y las nociones de equidad disponibles; Baker
y Hawn [12] trasladan el problema al terreno educativo, documentan que los modelos de estudiantes
pueden rendir de manera desigual entre grupos aun cuando el desempeño agregado es satisfactorio, y
advierten sobre los grupos cuyo sesgo no puede examinarse porque la variable que los define no está
registrada. Gardner, Brooks y Baker [13] aportan el procedimiento: el análisis por segmentos, que
recalcula las métricas de error sobre particiones definidas por atributos del estudiante en lugar de
conformarse con el agregado; es el que este proyecto adopta como indicador obligatorio.

Queda decidir *qué* diferencia se mide, y la elección no puede ser neutral. Hardt *et al.* [20]
formalizan criterios definidos sobre tasas de error condicionadas al desenlace real y muestran que
distintos criterios de equidad resultan mutuamente incompatibles salvo en casos degenerados: hay que
elegir uno y justificarlo. La asimetría de daños orienta la decisión. Un falso negativo deja a un
estudiante en riesgo sin acompañamiento, lo que reproduce la situación actual; un falso positivo
introduce un daño nuevo —la sospecha institucional sobre quien no la merecía— y su concentración en
un subgrupo convierte el acompañamiento en estigmatización. Por eso el indicador declarado es la
**diferencia en tasa de falsos positivos entre subgrupos**, con margen máximo de diez puntos
porcentuales, sin renunciar a reportar la sensibilidad por subgrupo.

### La capa de comunicación: anclaje documental, infidelidad a la fuente y su evaluación

El segundo componente del prototipo no predice: explica. La arquitectura que lo hace posible es la
generación aumentada por recuperación de Lewis *et al.* [9], que combina la memoria paramétrica del
modelo de lenguaje con una memoria no paramétrica consultable y condiciona la generación a los
fragmentos recuperados. Se adopta por responsabilidad institucional, no por desempeño lingüístico:
una recomendación sobre la situación académica de un estudiante debe poder rastrearse a un documento
de la institución —el Syllabus vigente, el reglamento estudiantil, las rutas de apoyo— y no al
conocimiento paramétrico de un modelo entrenado sobre la web.

El requisito se entiende a la luz del fallo que contiene. Ji *et al.* [10] revisan la alucinación en
generación de lenguaje natural —contenido fluido pero infiel a la fuente o no verificable— y
rastrean sus causas en los datos y en un objetivo de entrenamiento que premia la plausibilidad, no
la fidelidad. En un mensaje que se lee como voz institucional, un plazo inexistente no es un defecto
de estilo: es desinformación con consecuencias administrativas. De aquí la restricción
arquitectónica más fuerte del prototipo: el modelo no calcula la señal y **no escribe datos duros**
—fechas, notas, pesos, umbrales—, que inserta el canal determinista desde la fuente institucional.
Esa restricción convierte una propiedad difusa ("el modelo no alucina") en una hipótesis refutable
con un solo contraejemplo.

Su evaluación, en cambio, es un problema abierto. Gao *et al.* [21] describen la arquitectura en
tres etapas —indexación, recuperación y generación— y muestran que los fallos se distribuyen entre
ellas: el sistema puede recuperar el fragmento equivocado o, teniendo el correcto, generar una
afirmación que no se sigue de él. Como una auditoría que no distinga ambos casos no permite
corregir, la anotación registra por separado la pertinencia del fragmento y la atribución de la
afirmación a él. Existen además marcos automáticos —Es *et al.* [22] proponen métricas de fidelidad
y pertinencia sin referencia humana— útiles como instrumentación, pero emplean un modelo de lenguaje
como juez y comparten familia de fallos con el sistema evaluado: sirven para iterar, no como
evidencia.

### Evidencia producida por personas: fiabilidad entre anotadores y aceptación

La anotación de cien respuestas con una pauta es un análisis de contenido y hereda sus exigencias.
Krippendorff [23] establece que su validez depende de una unidad de análisis definida, de un esquema
de codificación con anclas explícitas fijadas antes de codificar y, de manera insustituible, del
reporte del acuerdo entre codificadores independientes: sin fiabilidad demostrada, los resultados
describen al codificador y no al material. Landis y Koch [24] aportan los rangos con los que se
interpreta la magnitud de ese acuerdo. Aquí la exigencia responde a un conflicto de interés
declarado —quien construye el prototipo es también quien lo evalúa—: de ahí el estudiante de
semillero como **segundo anotador independiente**, la doble anotación del 30 % de la muestra y la
fijación de la pauta antes de ver las respuestas.

La utilidad del artefacto tampoco se deduce de sus métricas. El modelo unificado de aceptación y uso
de tecnología de Venkatesh *et al.* [25] identifica cuatro determinantes de la intención de uso
—expectativa de desempeño, expectativa de esfuerzo, influencia social y condiciones facilitadoras—
de los que se derivan los ítems del instrumento aplicado a los docentes-tutores; la pregunta
pertinente no es solo si la explicación es correcta, sino en qué condiciones alguien distinto de su
autor la incorporaría a su trabajo. De ahí el contraste pareado contra un puntaje sin explicación
—la forma en que hoy se presenta la información— y la advertencia de potencia de H4: con seis a diez
participantes solo se detectarían diferencias grandes.

### Gobernanza: lo que la norma le exige al diseño, no al informe final

El último cuerpo normativo no es un anexo de cumplimiento: determina la arquitectura. La Ley
Estatutaria 1581 de 2012 [15] fija los principios de finalidad, autorización previa, seguridad y
circulación restringida en el tratamiento de datos personales; aplicados a un sistema que clasifica
estudiantes por su riesgo de fracaso, implican que los datos crudos y la tabla de correspondencia de
la seudonimización permanezcan en la infraestructura que la institución autorice, que el modelo de
lenguaje reciba solo indicadores derivados y que exista un procedimiento de rectificación. La
orientación de la UNESCO sobre inteligencia artificial generativa en educación e investigación [16]
añade el control humano de las decisiones y la verificación de contenidos, y la política nacional de
transformación digital e inteligencia artificial [17] inscribe esas exigencias en el marco
colombiano de ética y confianza. Traducidas al prototipo producen tres reglas verificables:
**ninguna decisión automatizada**, revisión humana previa a cualquier salida utilizable y
trazabilidad de cada afirmación a su fuente.

**Síntesis: del marco a la metodología.** El estado del conocimiento no deja libres estas
decisiones, las obliga: la unidad de análisis es la trayectoria semanal [1], [2]; las métricas se
reportan con su prevalencia y contra una línea base interna [18], [19]; el modelo es interpretable
por construcción [14]; la equidad se declara de antemano como diferencia de falsos positivos entre
subgrupos [12], [13], [20]; y la arquitectura separa el cálculo de la comunicación, con evidencia
humana de atribución a fuente [10], [23], [24]. La metodología que sigue ejecuta estas obligaciones.

---

## Metodología

### Enfoque y tipo de investigación

**Enfoque:** mixto convergente [26], con predominio cuantitativo en la validación retrospectiva del
detector y en la auditoría de la capa generativa, y componente cualitativo en la valoración de
utilidad y de condiciones de adopción. Los dos ramales se recogen en paralelo y se integran al final
en una matriz de triangulación por pregunta de investigación, no se anidan uno dentro del otro.

**Tipo de investigación:** aplicada, de **desarrollo tecnológico** y **evaluativa**. El artefacto se
construye dentro del proyecto (de ahí el tipo de propuesta "Desarrollo de Software") y el objeto de
medición es el artefacto mismo, no una población de estudiantes: los estudiantes del periodo cerrado
aportan los registros sobre los que el artefacto se evalúa, no son sujetos de una intervención.

**Rótulo del diseño, con precisión deliberada.** El documento evita el término "cuasiexperimental",
que no describe nada de lo que aquí se hace. El diseño tiene tres componentes con rótulos distintos y
no intercambiables:

1. **Validación retrospectiva del detector — diseño no experimental, ex post facto, de caso único
   institucional.** No hay intervención, no hay grupos de sujetos y no hay asignación de ninguna
   clase: se reconstruye la trayectoria semanal de los estudiantes de un periodo **ya cerrado** y se
   comparan **dos reglas de decisión aplicadas a los mismos casos** —el clasificador interpretable y
   la línea base de corte de notas— contra un desenlace ya ocurrido y conocido. La comparación es
   **pareada por caso**, lo que elimina la confusión entre grupos porque no hay dos grupos. Llamarlo
   cuasiexperimental sería inventar una manipulación que no existe.
2. **Evaluación de utilidad con docentes-tutores — diseño intrasujeto de medidas repetidas
   (*crossover*) con orden de presentación aleatorizado.** Cada docente-tutor valora **ambas**
   condiciones —caso presentado como puntaje de riesgo sin explicación y caso presentado con la
   explicación generada y trazable—, sobre pares de casos equiparados en nivel de riesgo. Se
   aleatoriza, por participante, el orden de las condiciones y la asignación de qué caso del par se
   presenta en cada condición; el propósito es controlar el efecto de orden y de aprendizaje. **Hay
   aleatorización, luego no es cuasiexperimental**: es un diseño experimental intrasujeto de muestra
   pequeña, y así se nombra. Lo que no es, es un experimento sobre estudiantes ni un estudio de
   efecto sobre la permanencia.
3. **Prueba de usabilidad con estudiantes voluntarios — diseño descriptivo sobre perfiles
   sintéticos.** No hay condición de comparación ni aleatorización: se registran cumplimiento de
   tareas, comprensión de la explicación y observaciones abiertas. Es descriptivo y se reporta como
   tal.

**Unidades de análisis.** Son tres y conviene distinguirlas porque cada una tiene su propio tamaño y
su propia métrica. (a) La **unidad estudiante-semana**: el vector de indicadores de un estudiante
matriculado en el programa piloto en una semana del periodo cerrado. Es la unidad del detector, y la
que hace posible medir anticipación: el mismo estudiante aporta una observación por semana. (b) La
**respuesta generada**: el texto completo de explicación y recomendación producido por el prototipo
para un caso, que es la unidad de la auditoría de la capa generativa; dentro de ella, la unidad de
codificación es la **afirmación factual individual**, no el párrafo. (c) La **persona
participante** —docente-tutor o estudiante voluntario— en los componentes de utilidad y usabilidad.

**Poblaciones, muestras y su justificación.**

- **Datos académicos:** tratamiento **censal**, no muestral. Se incluyen todos los estudiantes
  matriculados en el programa piloto en el periodo cerrado autorizado, con todas sus semanas
  registradas. No se muestrea porque el conjunto es pequeño (miles de filas estudiante-semana, no
  millones) y porque muestrear reduciría el número de casos positivos, que es el recurso escaso.
- **Prevalencia observada:** se reporta como dato de primer orden, no como nota metodológica. La
  proporción de casos que terminaron en pérdida de asignatura o retiro condiciona la lectura de todas
  las demás métricas [18], [19] y es la razón por la cual las metas absolutas de sensibilidad y
  precisión no se fijan antes de conocerla (H1).
- **Respuestas generadas:** muestra de **100 respuestas** con **muestreo estratificado** por nivel de
  señal (casos señalados de riesgo alto, señalados de riesgo moderado y no señalados) y por tipo de
  recomendación, para que la auditoría no se concentre en los casos fáciles. **30 respuestas (30 %)**
  reciben **doble anotación independiente** por el auxiliar de investigación de semillero.
- **Docentes-tutores:** mínimo **6**, muestreo intencional por criterio (ejercer tutoría o
  acompañamiento académico en la Escuela de Ingenierías, estar adscritos a **al menos dos programas
  académicos** de la Escuela —condición que sostiene la respuesta "Parcialmente" del segundo elemento
  preliminar— y no haber participado en el desarrollo del prototipo) y voluntario. Se declara desde
  ahora que este tamaño no da potencia para estimar magnitudes de efecto (H4).
- **Estudiantes voluntarios:** mínimo **10**, convocatoria abierta y voluntaria, **sin que ninguno
  vea su propia situación académica**: trabajan sobre perfiles sintéticos. No se convoca a
  estudiantes de asignaturas a cargo del investigador principal, para no reproducir la asimetría de
  poder entre docente y estudiante en la solicitud de participación.

### Instrumentos

| # | Instrumento | Contenido y uso |
|---|---|---|
| I1 | **Ficha de inventario de fuentes y variables** | Por cada fuente institucional (libro de calificaciones, registro de asistencia, traza del aula virtual): campos disponibles, granularidad temporal, formato de exportación, cobertura del periodo y **porcentaje de valores faltantes por variable**. Es el instrumento que convierte el pendiente 8 —disponibilidad no verificada de la traza de actividad— en un dato reportado en lugar de un supuesto. |
| I2 | **Acta de definición operativa de riesgo, línea base y punto de operación** | Instrumento y producto a la vez. Se diligencia en taller con el área de bienestar y permanencia y registra, **antes de ver resultados**: (a) la definición operativa de riesgo académico y el desenlace que cuenta como positivo (pérdida de asignatura, retiro); (b) la formulación exacta de la **línea base** —la regla de corte de notas vigente, reconstruible sobre los mismos datos—; (c) la **capacidad semanal de atención** declarada por el área, en número de casos que puede contactar; (d) el **umbral y el punto de operación** del clasificador derivado de esa capacidad; y (e) el punto de corte intermedio del periodo en que se evalúa la anticipación. El acta se firma y se fecha; **los umbrales no pueden modificarse después de conocer los resultados**, y cualquier cambio exige un anexo fechado que explique la razón. |
| I3 | **Diccionario de datos y protocolo de seudonimización** | Definición de cada variable derivada, su fórmula, su ventana temporal y su tratamiento de faltantes; procedimiento de seudonimización, ubicación de la tabla de correspondencia dentro de la infraestructura autorizada, control de accesos y procedimiento de rectificación y de destrucción al cierre. |
| I4 | **Protocolo de validación retrospectiva** | Fijado antes de ejecutar. Métricas de reporte conjunto: **sensibilidad, precisión, valor predictivo negativo, área bajo la curva ROC y prevalencia observada**, más curva de precisión-exhaustividad [18], [19]; particiones (validación cruzada estratificada por caso, **con separación por estudiante** para que las semanas de un mismo estudiante no queden repartidas entre entrenamiento y prueba); intervalos de confianza por **bootstrap** de casos [27]; y la definición operativa de **anticipación en semanas** (ver abajo). Incluye la regla de decisión de H1 y la lista de análisis que se reportarán aunque el resultado sea desfavorable. |
| I5 | **Pauta de anotación de atribución a fuente — dos códigos separados** | Instrumento central de la auditoría de la capa generativa, **congelado antes de ver las respuestas**. Por cada afirmación factual de cada respuesta se registran **dos códigos independientes**, no uno: **C-P (pertinencia del fragmento recuperado)** —si el fragmento que el sistema recuperó es pertinente para sustentar esa afirmación— y **C-A (atribución de la afirmación al fragmento)** —si la afirmación se sigue efectivamente del fragmento recuperado o del indicador entregado por el canal determinista—. La separación es exigencia del propio marco: los fallos de un sistema de recuperación aumentada se distribuyen entre la recuperación y la generación, y una auditoría que los sume en un solo código no permite corregir ninguno de los dos [21]. Un tercer registro, dicotómico, cuenta los **errores de dato duro** (fecha, nota, peso de evaluación, umbral), cuya tasa esperada es cero por construcción arquitectónica. La pauta incluye anclas con ejemplos y contraejemplos, y la definición de qué cuenta como "afirmación factual". |
| I6 | **Instrumento de utilidad y aceptación para docentes-tutores** | Tres bloques. (a) **Comparación pareada** entre el caso con explicación trazable y el caso con puntaje sin explicación, con escala de accionabilidad y elección forzada de cuál usaría. (b) **Ítems Likert 1–5 derivados de los cuatro determinantes de UTAUT [25]** —expectativa de desempeño, expectativa de esfuerzo, influencia social y condiciones facilitadoras—, con al menos tres ítems por determinante, más ítems de confianza en la trazabilidad y de alcance de la revisión que consideran necesaria antes de contactar a un estudiante. (c) **Preguntas abiertas** sobre riesgos percibidos, condiciones de adopción y límites que no cruzarían. |
| I7 | **Guion de prueba de usabilidad con estudiantes voluntarios** | Cuatro tareas sobre **perfiles sintéticos**: identificar qué evaluación está pendiente, decir qué peso tiene en la nota, decir cuál es el plazo aplicable según el reglamento y decir a qué servicio de apoyo acudiría. Se registran cumplimiento, tiempo, errores de interpretación y una escala de claridad percibida, más preguntas abiertas sobre el tono del mensaje. Mide si la explicación se entiende, no si el estudiante está en riesgo. |
| I8 | **Formato de consentimiento informado** | Dos versiones (docentes-tutores y estudiantes voluntarios): propósito, carácter voluntario, tratamiento anonimizado, ausencia de incidencia en evaluación laboral o académica, derecho de retiro en cualquier momento, tiempo de conservación y contacto del investigador. Sujeto a aprobación del Comité de Ética (pendiente 6). |
| I9 | **Lista de verificación de salvaguardas de gobernanza** | Instrumento y producto: seudonimización efectiva, ausencia de decisión automatizada, revisión humana previa a toda salida utilizable, trazabilidad de cada afirmación a fuente, análisis de equidad ejecutado y reportado, declaración de uso de IA, procedimiento de rectificación y regla de conservación y destrucción de datos. |

**Definición operativa de "anticipación en semanas".** No existe una definición canónica, de modo que
se fija aquí y no se cambia después. Para cada caso que terminó en desenlace positivo y fue detectado
por ambas reglas, la anticipación es la **diferencia, en número de semanas, entre la primera semana
del periodo en que el prototipo señala el caso y la semana en que la línea base lo habría señalado**.
Se reporta con **mediana y rango**, no con promedio único, porque la distribución es asimétrica y
acotada por el calendario del periodo. Los casos detectados por el prototipo y **no** detectados por
la línea base se reportan **aparte y por conteo**, no como una anticipación de valor infinito; los
casos detectados por la línea base antes que por el prototipo se reportan con anticipación negativa y
no se excluyen. Esta última precisión importa: excluirlos inflaría el resultado.

### Cómo se alcanza cada objetivo específico

**Objetivo específico 1 — Caracterizar las variables, constituir el conjunto de datos seudonimizado y
acordar la definición operativa de riesgo y la línea base (actividades 1 a 4, semanas 1 a 4).**

- *Gestión habilitante:* radicación de la solicitud de acceso a datos ante la dirección de programa,
  Registro y Control Académico y el área responsable del aula virtual, y radicación del proyecto y de
  los instrumentos ante el Comité de Ética. En la solicitud se define por escrito el rol del
  investigador frente a los datos: acceso a un **extracto seudonimizado bajo responsabilidad
  institucional**, no cesión de la base. Es la actividad 1 y condiciona todo lo demás.
- *Caracterización de fuentes:* diligenciamiento de I1 sobre las tres fuentes, con verificación
  efectiva de la exportabilidad de la traza del aula virtual —el punto no verificado del pendiente
  8—. El resultado se reporta tal como salga: si la traza no es exportable, el conjunto de variables
  se reduce a calificaciones y asistencia y se declara la reducción, con su efecto esperado sobre la
  anticipación.
- *Definición operativa y línea base:* taller de trabajo con el área de bienestar y permanencia
  estudiantil, del que sale el acta I2. Tres decisiones se toman **ahí y no después**: qué cuenta como
  desenlace positivo, cómo se formula la línea base de corte de notas sobre los mismos datos, y qué
  capacidad semanal de atención tiene el área —dato que fija el punto de operación del clasificador,
  porque una alerta que nadie puede atender no es una alerta—. Sin esta actividad el proyecto tendría
  un umbral elegido por conveniencia del modelador.
- *Constitución del conjunto de datos:* construcción de la tabla estudiante-semana con seudonimización
  aplicada en origen, diccionario de datos (I3), reporte de faltantes por variable y **cálculo de la
  prevalencia observada del desenlace**. Se documenta la trazabilidad del proceso con código
  reproducible.
- *Análisis:* descriptivo. Distribución de cada indicador por semana, correlación con el desenlace,
  prevalencia y cobertura.
- *Criterio de logro:* acta I2 firmada, I1 diligenciada para las tres fuentes, conjunto de datos
  constituido con cobertura del 100 % de los estudiantes del grupo piloto y prevalencia reportada.
- *Regla de contingencia, con fecha límite:* si al **cierre de la semana 2** no hay autorización de
  acceso, se activa la ruta declarada en el alcance —conjunto sintético calibrado con estadísticos
  agregados— y se informa a la DNI. La activación no cambia las actividades ni el cronograma, pero sí
  cambia lo que la validación del OE3 puede afirmar, y así se reporta en el informe.

**Objetivo específico 2 — Desarrollar el prototipo en dos capas verificables, con su arquitectura y
su protocolo de datos (actividades 5 a 9, semanas 3 a 9).**

- *Canal determinista de indicadores (actividad 5):* implementación en Python con pandas de la
  ingeniería de variables semanales definida en I3 —notas parciales ponderadas por el peso real del
  libro de calificaciones, asistencia acumulada y su tendencia, accesos y entregas con su oportunidad—.
  Se acompaña de **pruebas unitarias sobre casos de control construidos a mano**, con el resultado
  esperado calculado manualmente: es el mecanismo por el cual se puede afirmar que los datos duros son
  correctos por construcción y no por confianza.
- *Clasificador interpretable (actividad 6):* entrenamiento de **regresión logística regularizada** y
  **árbol de decisión de profundidad limitada** [14], con validación cruzada estratificada y
  **separación por estudiante** entre particiones. Selección del punto de operación en el umbral
  registrado en el acta I2, no en el que maximiza una métrica. Se reportan los coeficientes y las
  reglas, porque la explicación que el asistente entrega debe corresponder a lo que el modelo usó.
- *Corpus documental e índice (actividad 7):* recolección y versionado del Syllabus vigente del
  programa piloto, de los apartados del reglamento estudiantil relativos a evaluación y permanencia,
  del catálogo de rutas y servicios de apoyo y del calendario académico; segmentación, generación de
  incrustaciones multilingües e indexación vectorial. Cada fragmento conserva su **ficha de
  procedencia** (documento, versión, apartado), sin la cual la trazabilidad sería una afirmación
  vacía.
- *Capa de generación aumentada por recuperación (actividad 8):* implementación de la recuperación y
  de las plantillas de generación bajo la restricción arquitectónica declarada: el modelo de lenguaje
  redacta a partir de los fragmentos recuperados y de los indicadores recibidos, y **los datos duros
  los inserta el canal determinista**, no el modelo [10]. Interfaz conversacional mínima, sin
  autenticación institucional ni despliegue multiusuario. Se ejecuta un ciclo interno de iteración con
  instrumentación automática de fidelidad y pertinencia (Ragas o equivalente [22]) usada
  **exclusivamente para iterar**: por emplear un modelo de lenguaje como juez y compartir familia de
  fallos con el sistema evaluado, **no se reporta como evidencia** en ningún resultado.
- *Documentación (actividad 9):* arquitectura de referencia (componentes, flujos, decisiones y
  alternativas descartadas), protocolo de tratamiento de datos (I3) y bitácora de uso de IA en el
  desarrollo.
- *Criterio de logro:* prototipo ejecutable de extremo a extremo que, dado un caso del conjunto de
  datos, produce señal, explicación, recomendación y **lista de fragmentos citados**; pruebas
  unitarias del canal en verde; arquitectura y protocolo entregados.

**Objetivo específico 3 — Evaluar el prototipo, valorar su utilidad y usabilidad, y formular las
salvaguardas (actividades 10 a 14, semanas 7 a 12).**

- *Validación retrospectiva del detector (actividad 10):* aplicación del protocolo I4. Se reportan
  **conjuntamente sensibilidad, precisión, valor predictivo negativo, área bajo la curva ROC y
  prevalencia observada**, con curva de precisión-exhaustividad y con intervalos de confianza por
  bootstrap de casos [27], **siempre junto a la línea base** medida sobre los mismos datos y con la
  misma definición de desenlace. Se calcula la **anticipación en semanas** con la definición operativa
  fijada arriba, reportada con mediana y rango.
- *Análisis de equidad por segmentos (actividad 11):* siguiendo el procedimiento de análisis por
  segmentos [13], se recalculan las métricas de error sobre los subgrupos que la institución autorice
  (modalidad, jornada, rango de edad, sede de matrícula). El indicador declarado es la **diferencia en
  tasa de falsos positivos entre subgrupos**, con margen máximo de diez puntos porcentuales (H3). La
  elección del criterio se justifica por **asimetría de daños** —un falso positivo introduce sospecha
  institucional sobre quien no la merecía, y su concentración en un subgrupo convierte el
  acompañamiento en estigmatización— y se sostiene sabiendo que los criterios de equidad son
  **mutuamente incompatibles** salvo en casos degenerados [20]: se elige uno, se justifica y se
  declara qué queda sin controlar. Se reporta además la sensibilidad por subgrupo. Todo subgrupo con
  **n insuficiente** se reporta de forma descriptiva y con su n, sin prueba de hipótesis; toda variable
  no autorizada se declara **como no evaluada, con su nombre** [12].
- *Auditoría de la capa generativa (actividad 12):* generación de las 100 respuestas de la muestra
  estratificada; **congelamiento de la pauta I5 antes de verlas**; anotación por el investigador de
  las 100 y **doble anotación independiente de 30 (30 %)** por el auxiliar de semillero, previo
  entrenamiento sobre las anclas con un piloto de 10 respuestas ajenas a la muestra. Los dos códigos
  —pertinencia del fragmento (C-P) y atribución de la afirmación (C-A)— se analizan por separado y se
  cruzan en una matriz de dos por dos, que es la que permite distinguir un fallo de recuperación de un
  fallo de generación [21]. Fiabilidad entre anotadores con **κ de Cohen por código y α de
  Krippendorff** [23], interpretada con los rangos de referencia de Landis y Koch [24]; se reportan
  los desacuerdos, no solo el coeficiente. La tasa de **error de dato duro** se reporta como conteo
  absoluto: un solo error refuta la premisa arquitectónica (H2) y se reporta como defecto de diseño.
- *Utilidad y usabilidad (actividad 13):* aplicación de I6 a los docentes-tutores en el diseño
  intrasujeto con orden aleatorizado descrito arriba, y de I7 a los estudiantes voluntarios sobre
  perfiles sintéticos. Consentimiento informado (I8) previo en ambos casos.
- *Análisis de los componentes con personas e integración (actividades 13 y 14):* cuantitativo, prueba de **Wilcoxon para pares** sobre la
  comparación pareada de accionabilidad y prueba binomial sobre la elección forzada, con tamaño de
  efecto, n e **intervalos por bootstrap** [27] y con la advertencia de potencia de H4 declarada en el
  propio reporte; descriptivos por determinante de UTAUT [25]. Cualitativo, **análisis temático en seis
  fases** [28] de las respuestas abiertas y de las observaciones de usabilidad, con libro de códigos,
  codificación preliminar asistida por modelo de lenguaje **verificada íntegramente por codificación
  humana** y reporte del acuerdo entre ambas. Integración convergente [26] de los cinco ramales
  —desempeño, anticipación, verificabilidad, equidad y utilidad— en una matriz de triangulación por
  pregunta de investigación.
- *Formulación de salvaguardas (actividad 14):* la lista I9 y la guía de adopción se redactan **a
  partir de los riesgos que la evaluación haya evidenciado**, no de una plantilla previa; si el
  análisis de equidad refuta H3, la guía declara el prototipo **no adoptable en su configuración
  evaluada** y especifica qué habría que corregir.
- *Criterio de logro:* informe de validación con las cinco métricas y la anticipación reportadas
  contra la línea base; análisis de equidad ejecutado y reportado (o declarado no evaluable, con la
  variable faltante nombrada); 100 respuestas anotadas, 30 con doble anotación y fiabilidad reportada;
  ≥ 6 docentes-tutores y ≥ 10 estudiantes participantes; lista de salvaguardas y guía de adopción
  entregadas y socializadas.

### Salvaguardas metodológicas frente al conflicto de interés

Quien construye el prototipo es quien lo evalúa, y ese conflicto no se resuelve declarándolo: se
controla con procedimientos verificables. Se adoptan seis. (1) La **definición operativa de riesgo, la
línea base, el umbral y el punto de operación se fijan con el área de permanencia y se registran en
acta fechada (I2) antes de ejecutar cualquier evaluación**, de modo que no puedan ajustarse a
posteriori para favorecer al detector. (2) La **pauta de anotación (I5) se congela antes de ver las
respuestas** que se van a anotar. (3) El **30 % de la muestra se anota por un segundo anotador
independiente** y se reporta la fiabilidad con sus desacuerdos; el auxiliar de semillero existe en el
presupuesto por esta razón metodológica, no como apoyo accesorio. (4) La **línea base se reconstruye y
se reporta con el mismo detalle que el modelo propio**, incluida su propia matriz de confusión: sin
línea base bien medida, cualquier ventaja es un artefacto. (5) Las **métricas crudas por caso y por
subgrupo, la matriz de dos por dos de la anotación y el código del canal determinista se entregan como
anexo del informe**, para que un tercero pueda recalcular. (6) Los **resultados desfavorables se
reportan con el mismo detalle que los favorables**, y las condiciones de refutación quedaron escritas
por adelantado en el apartado de hipótesis.

### Limitaciones declaradas

**Primera — validez externa de las métricas.** Un solo programa y un solo periodo: las cifras de
desempeño describen ese caso y no la institución. Lo transferible es la arquitectura, el protocolo de
datos y los instrumentos, no los números; y las cifras absolutas tampoco son comparables con la
literatura, porque las definiciones de desenlace y los horizontes de predicción varían entre
estudios [5].

**Segunda — no se mide efecto sobre la permanencia.** El diseño no tiene intervención, grupo de
comparación ni seguimiento longitudinal, de modo que **ninguna conclusión sobre deserción o
permanencia es admisible** a partir de estos datos. Se mide la calidad de la señal y de su
explicación, que es la condición previa.

**Tercera — dependencia de un habilitante externo.** El acceso a los datos no está concedido
(pendiente 5). Si se activa la ruta de contingencia, el prototipo, la arquitectura, el protocolo, las
salvaguardas y la auditoría de la capa generativa se conservan, pero la validación retrospectiva pasa
a ser **prueba de funcionamiento sin valor predictivo**, y el análisis de equidad sobre datos
sintéticos **no sería evidencia de equidad** y así se declararía.

**Cuarta — evento poco frecuente y subgrupos pequeños.** Con prevalencia baja, los intervalos de
confianza son anchos y las estimaciones por subgrupo pueden ser inestables. Se mitiga con bootstrap
[27], con reporte obligatorio del n de cada subgrupo y con la regla, fijada por adelantado, de no
aplicar pruebas de hipótesis a subgrupos con n insuficiente.

**Quinta — potencia y autoselección en los componentes con personas.** Seis a diez participantes solo
permiten detectar diferencias grandes: una ausencia de diferencias se reportará como **ausencia de
evidencia, no como prueba de equivalencia** (H4). La participación voluntaria sesga hacia docentes
interesados en IA; se documenta el perfil de los participantes y las respuestas escépticas se reportan
sin agregarlas.

**Sexta — los sesgos que no se pueden examinar.** Solo pueden auditarse los subgrupos que la
institución registra y autoriza. Los grupos definidos por variables no registradas quedan fuera del
análisis de equidad, y esa imposibilidad se declara con el nombre de la variable ausente en lugar de
presentarse como equidad verificada [12].

**Séptima — el prototipo no queda en operación.** No hay integración con sistemas en producción; el
desempeño medido es el de un prototipo sobre datos históricos, y el comportamiento en operación real
—con datos que llegan incompletos y a destiempo— **no queda establecido** por este estudio.

---

## Resultados y productos de la propuesta

Los productos se clasifican en las tipologías del modelo de medición de Minciencias [29]. Cada uno se
atribuye al objetivo específico **cuyas actividades lo producen**, con el número de esas actividades a
la vista. Los dos productos que dependen de actividades de más de un objetivo se declaran
**transversales** —uno a dos objetivos y otro a los tres— y no se asignan a uno solo por comodidad de
la tabla: atribuir a un único objetivo un producto que otro objetivo también produce rompería
precisamente el amarre que esta sección debe demostrar.

| Tipología Minciencias [29] | Producto entregable | Objetivo específico (actividades) | Indicador de verificación | Tiempo de impacto en la comunidad académica |
|---|---|---|---|---|
| **IV. Desarrollo tecnológico e innovación** | **Prototipo funcional del asistente en dos capas**: canal determinista de indicadores con clasificador interpretable, capa de generación aumentada por recuperación sobre el corpus institucional e interfaz conversacional mínima. Entregado como repositorio versionado y ejecutable. | **OE2** (actividades 5, 6, 7, 8) | Prototipo que, dado un caso del conjunto de datos, produce señal de riesgo, explicación, recomendación y **lista de fragmentos citados con su procedencia**; pruebas unitarias del canal determinista en verde; demostración registrada de extremo a extremo. | Inmediato como demostrador para la dirección de programa y el área de permanencia; base técnica de un eventual despliegue posterior. |
| **IV. Desarrollo tecnológico e innovación** | **Arquitectura de referencia documentada y protocolo de tratamiento de datos**: componentes, flujos, decisiones de diseño y alternativas descartadas; seudonimización, custodia de la tabla de correspondencia, control de accesos, rectificación y destrucción. | **OE2** (actividad 9) | Documento de arquitectura con diagrama de componentes y mapa de dependencias entre documento institucional y salida generada, más protocolo de datos entregado y consistente con el aval del Comité de Ética. | Inmediato y reutilizable por cualquier iniciativa institucional de analítica académica, con independencia de este prototipo. |
| **IV. Desarrollo tecnológico e innovación** | **Definición operativa de riesgo académico acordada, con su línea base, y conjunto de datos seudonimizado documentado** (tabla estudiante-semana, diccionario de datos, faltantes por variable y prevalencia observada). | **OE1** (actividades 2, 3, 4) | Acta I2 firmada por el área de bienestar y permanencia; conjunto de datos con cobertura del 100 % del grupo piloto del periodo cerrado y diccionario completo; prevalencia reportada. | Inmediato para el área de permanencia; es el activo que **conserva valor institucional incluso si el prototipo rinde por debajo de lo esperado**. |
| **I. Generación de nuevo conocimiento** | **Informe de validación retrospectiva y manuscrito de resultados** (artículo o ponencia): desempeño frente a la línea base con las cinco métricas y la prevalencia, anticipación en semanas con mediana y rango, verificabilidad de la capa generativa con fiabilidad entre anotadores, y análisis de equidad por subgrupos, **incluidas las hipótesis refutadas**. | **OE3** (actividades 10, 11, 12, 13, 14) | Manuscrito entregado a la DNI con datos, análisis, anexo de métricas crudas por caso y subgrupo, matriz de anotación y declaración de uso de IA. | A partir de la semana 12 y en la ventana de observación de la siguiente convocatoria Minciencias. |
| **I. Generación de nuevo conocimiento** | **Protocolo de auditoría de atribución a fuente para asistentes con recuperación aumentada**: pauta de anotación con los dos códigos separados (pertinencia del fragmento y atribución de la afirmación), anclas, definición de unidad de codificación y procedimiento de fiabilidad. Es un instrumento reutilizable, no un apartado del informe. | **OE3** (actividad 12) | Pauta congelada con acta de fecha anterior a la generación de la muestra; α de Krippendorff y κ por código reportados con su interpretación [24]; matriz de dos por dos publicada. | A partir de la semana 11; aplicable por cualquier programa que evalúe un asistente anclado a documento, dentro o fuera de la CUN. |
| **II. Formación de recurso humano en CTeI** | **Vinculación certificada de un estudiante de semillero** como auxiliar de investigación: participa en la construcción del canal de datos y en la documentación de la arquitectura, y actúa como **segundo anotador independiente** del conjunto de validación, con entrenamiento, plan de trabajo, bitácora y coautoría del anexo de fiabilidad. | **Transversal a OE2 y OE3** (actividades 5, 9, 12 y 14: la certificación se emite en la actividad 14) | Certificación emitida por la institución, bitácora de trabajo entregada y 30 respuestas anotadas de forma independiente con su reporte de fiabilidad. | Durante la ejecución y de forma diferida en su trabajo de grado y hoja de vida académica. |
| **III. Apropiación social del conocimiento** | **Guía de adopción institucional y lista de verificación de salvaguardas** (seudonimización, no decisión automatizada, revisión humana previa, trazabilidad a fuente, análisis de equidad, declaración de uso de IA, rectificación y destrucción de datos), socializada en un taller interno con el área de permanencia, la dirección de programa y docentes-tutores. | **Transversal a OE1, OE2 y OE3** (actividades 3, 9 y 14): la restricción de capacidad de atención y el punto de operación vienen del acta de la actividad 3, las salvaguardas de datos vienen del protocolo de la actividad 9 y las salvaguardas de uso salen de los hallazgos de la actividad 14 | Guía y lista entregadas; taller realizado con acta de socialización y ≥ 10 asistentes; constancia de entrega al área de bienestar y permanencia. | Inmediato para los asistentes; base de un eventual lineamiento institucional de analítica de permanencia. |

**Por qué se comprometen las cuatro tipologías y por qué no más productos.** Las cuatro salen del
diseño sin forzarlas: el prototipo, la arquitectura y el conjunto de datos documentado son desarrollo
tecnológico; el informe de validación y el protocolo de auditoría son conocimiento nuevo —el segundo lo
es con independencia de cómo rinda el prototipo—; el auxiliar de semillero es una **necesidad
metodológica** antes que un añadido, porque sin segundo anotador no hay fiabilidad que reportar; y la
guía con las salvaguardas solo tiene sentido si se socializa con quien tendría que aplicarla. **No se
compromete** un producto de divulgación pública de la ciencia distinto del manuscrito, porque en 12
semanas sería el mismo contenido con otro rótulo; **no se compromete** software en producción,
consistente con la exclusión (c) del alcance; y **no se compromete** ningún producto que dependa de
demostrar efecto sobre la permanencia, consistente con la exclusión (a).

**Dos productos con condición explícita.** El informe de validación se entrega en cualquier escenario,
pero si se activó la ruta de contingencia declara en su título y en su resumen que la validación se
realizó sobre datos sintéticos y **no constituye evidencia predictiva**. Y la guía de adopción se
entrega también en cualquier escenario, pero puede concluir que el prototipo **no es adoptable en su
configuración evaluada**: ese resultado cumple el producto, no lo incumple.

---

## Presupuesto detallado

| Rubro | Descripción | Cantidad | Valor unitario (COP) | Valor total (COP) |
|---|---|---|---|---|
| Talento humano | Auxiliar de investigación de semillero: entrenamiento en la pauta de anotación, doble anotación independiente de 30 respuestas, apoyo en el canal de datos y en la documentación (bonificación por 3 meses) | 1 | 900.000 | 900.000 |
| Servicios de cómputo | Instancia de cómputo con GPU en la nube para servir el modelo de lenguaje de pesos abiertos y ejecutar la indexación vectorial (3 meses) | 3 | 250.000 | 750.000 |
| Servicios digitales | Créditos de API de modelo de lenguaje comercial, para el contraste de calidad sobre casos sintéticos o desidentificados y para la instrumentación automática de la iteración del componente RAG | 1 | 250.000 | 250.000 |
| Servicios digitales | Almacenamiento cifrado y respaldo versionado del conjunto de datos seudonimizado, del corpus documental y de los resultados (3 meses) | 3 | 60.000 | 180.000 |
| Software | Licencia académica de herramienta de anotación y análisis cualitativo asistido por computador (3 meses), para la pauta de atribución a fuente y el libro de códigos | 1 | 300.000 | 300.000 |
| Servicios digitales | Transcripción automática con revisión manual de las sesiones de evaluación de utilidad y de usabilidad | 1 | 150.000 | 150.000 |
| Divulgación | Inscripción a evento académico nacional para la ponencia de resultados | 1 | 450.000 | 450.000 |
| Divulgación | Revisión editorial y ajuste del manuscrito a las normas de la revista o evento de destino | 1 | 300.000 | 300.000 |
| Materiales | Papelería, impresión de consentimientos informados, formatos de anotación y guías del taller | 1 | 120.000 | 120.000 |
| Logística | Talleres: definición operativa de riesgo con el área de permanencia y socialización de la guía de adopción (2 sesiones) | 2 | 110.000 | 220.000 |
| Imprevistos | Contingencia sobre el subtotal (6,35 %) | 1 | 230.000 | 230.000 |
| **TOTAL** | | | | **3.850.000** |

**Verificación aritmética, línea por línea.** 1 × 900.000 = 900.000 · 3 × 250.000 = 750.000 ·
1 × 250.000 = 250.000 · 3 × 60.000 = 180.000 · 1 × 300.000 = 300.000 · 1 × 150.000 = 150.000 ·
1 × 450.000 = 450.000 · 1 × 300.000 = 300.000 · 1 × 120.000 = 120.000 · 2 × 110.000 = 220.000 ·
1 × 230.000 = 230.000. Subtotal sin imprevistos: 900.000 + 750.000 + 250.000 + 180.000 + 300.000 +
150.000 + 450.000 + 300.000 + 120.000 + 220.000 = **3.620.000**. Imprevistos: 230.000, equivalentes al
**6,35 %** de ese subtotal. **Total: 3.620.000 + 230.000 = 3.850.000 COP**, idéntico al monto
declarado en la ficha de identificación y equivalente al **77,0 %** del techo de $5.000.000 del
numeral 8.

**Los dos rubros no verificados y el porcentaje en riesgo — remite al pendiente 9.** La tabla de rubros
financiables y no financiables del numeral 6 de los Términos de Referencia **está incrustada como
imagen en el PDF y no se puede extraer ni leer**, de modo que dos rubros de este presupuesto no
pudieron contrastarse con ella: (a) el **talento humano** —bonificación del auxiliar de semillero—,
$900.000, equivalentes al **23,4 %** del total; y (b) los **servicios de cómputo y de API de modelo de
lenguaje**, $750.000 + $250.000 = $1.000.000, equivalentes al **26,0 %**. En conjunto, **$1.900.000, el
49,4 % del presupuesto solicitado, queda pendiente de verificación** contra un documento ilegible. Debe
confirmarse con la DNI antes de radicar.

**Qué pasa si alguno no es financiable, dicho sin eufemismos.** Si el talento humano no lo es, el
proyecto pierde al **segundo anotador independiente** y con él la medida de fiabilidad entre
anotadores; la auditoría de la capa generativa quedaría con un solo anotador, que además es el
constructor del prototipo, lo que **debilita el control de conflicto de interés número (3)** y
obligaría a reportar la verificabilidad sin coeficiente de acuerdo y a declararlo como limitación
añadida. La alternativa —anotación cruzada voluntaria por un docente de la Escuela— se gestionaría, pero
no puede comprometerse aquí. Si los servicios de cómputo no lo son, la ruta es operar el modelo de
pesos abiertos en infraestructura institucional si existe capacidad disponible; el alcance no cambia,
pero la ejecución quedaría sujeta a la disponibilidad de esa infraestructura, que tampoco está
confirmada. Ninguna de las dos contingencias se presenta como resuelta.

**Por qué no se solicita el techo.** El proyecto no requiere hardware propio, no requiere
desplazamientos intersedes y no requiere licencias propietarias en su ruta crítica: se solicita el
77,0 % del techo porque es lo que el diseño consume. Completar hasta $5.000.000 exigiría partidas de
relleno —equipos que no se usarían, viáticos sin trayecto o incentivos económicos a participantes, que
además introducirían un problema de coerción sobre estudiantes y docentes—, y eso deterioraría la
coherencia entre alcance, método y presupuesto. Si la DNI privilegiara la ejecución del monto completo,
la ampliación defendible sería **replicar la validación retrospectiva en un segundo programa piloto**,
con el costo de coordinación, extracción de datos y segundo panel de docentes-tutores que ello implica;
se presenta como alternativa, no como solicitud, y aumentaría el alcance declarado.

*Nota:* la adquisición de servicios e insumos queda sujeta a la revisión y aval de la Vicerrectoría de
Gestión, la Vicerrectoría de Innovación, Investigación y Emprendimiento y el Comité de Ética de la
Investigación Institucional, según el numeral 6 de los Términos de Referencia.

---

## Lista de referencias

Norma de citación: **IEEE**, por corresponder a una propuesta de la **Escuela de Ingenierías**. Las
**30 fuentes** están citadas en el cuerpo del documento —las 25 primeras en el marco teórico, y las
cinco últimas en metodología ([26], [27], [28]), en resultados y productos ([29]) y en aspectos
éticos ([30])— y todas las citas del cuerpo aparecen en esta lista.

**Convención de numeración.** Las entradas están numeradas en **orden de primera aparición** según el
orden de secciones del INV-FO03, que es el orden en que están escritas aquí. Esta lista ocupa su
posición oficial —sección 16, **después** de "Resultados y productos de la propuesta" (sección 15) y
**antes** de "Aspectos éticos" (sección 17)—, de modo que las secciones que la preceden son las que
introducen las últimas entradas: Metodología (sección 14) aporta [26], [27] y [28] y Resultados y
productos (sección 15) aporta [29]; [30] aparece por primera vez en Aspectos éticos, que va
inmediatamente después.

[1] V. Tinto, *Leaving College: Rethinking the Causes and Cures of Student Attrition*, 2a ed.
Chicago, IL, EE. UU.: University of Chicago Press, 1993.

[2] Ministerio de Educación Nacional de Colombia, *Sistema para la Prevención de la Deserción de la
Educación Superior (SPADIES)*. Bogotá, Colombia: MEN. (Sistema de información institucional para el
seguimiento y la prevención de la deserción en educación superior.)

[3] G. Siemens, "Learning analytics: The emergence of a discipline," *American Behavioral
Scientist*, vol. 57, no. 10, pp. 1380–1400, 2013.

[4] K. E. Arnold y M. D. Pistilli, "Course Signals at Purdue: Using learning analytics to increase
student success," en *Proc. 2nd International Conference on Learning Analytics and Knowledge (LAK
'12)*, Vancouver, Canadá, 2012, pp. 267–270.

[5] B. Prenkaj, P. Velardi, G. Stilo, D. Distante, y S. Faralli, "A survey of machine learning
approaches for student dropout prediction in online courses," *ACM Computing Surveys*, vol. 53, no.
3, 2020.

[6] L. Aulck, N. Velagapudi, J. Blumenstock, y J. West, "Predicting student dropout in higher
education," *arXiv preprint* arXiv:1606.06364, 2016.

[7] R. F. Kizilcec y S. Halawa, "Attrition and achievement gaps in online learning," en *Proc. 2nd
ACM Conference on Learning at Scale (L@S '15)*, Vancouver, Canadá, 2015, pp. 57–66.

[8] O. Zawacki-Richter, V. I. Marín, M. Bond, y F. Gouverneur, "Systematic review of research on
artificial intelligence applications in higher education – where are the educators?," *International
Journal of Educational Technology in Higher Education*, vol. 16, art. 39, 2019.

[9] P. Lewis *et al.*, "Retrieval-augmented generation for knowledge-intensive NLP tasks," en
*Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, 2020, pp. 9459–9474.

[10] Z. Ji *et al.*, "Survey of hallucination in natural language generation," *ACM Computing
Surveys*, vol. 55, no. 12, art. 248, dic. 2023.

[11] N. Mehrabi, F. Morstatter, N. Saxena, K. Lerman, y A. Galstyan, "A survey on bias and fairness
in machine learning," *ACM Computing Surveys*, vol. 54, no. 6, art. 115, jul. 2021.

[12] R. S. Baker y A. Hawn, "Algorithmic bias in education," *International Journal of Artificial
Intelligence in Education*, vol. 32, 2022.

[13] J. Gardner, C. Brooks, y R. Baker, "Evaluating the fairness of predictive student models
through slicing analysis," en *Proc. 9th International Conference on Learning Analytics and
Knowledge (LAK '19)*, Tempe, AZ, EE. UU., 2019, pp. 225–234.

[14] C. Rudin, "Stop explaining black box machine learning models for high stakes decisions and use
interpretable models instead," *Nature Machine Intelligence*, vol. 1, no. 5, pp. 206–215, may. 2019.

[15] Congreso de la República de Colombia, *Ley Estatutaria 1581 de 2012, por la cual se dictan
disposiciones generales para la protección de datos personales*. Bogotá, Colombia, oct. 2012.

[16] UNESCO, *Guidance for Generative AI in Education and Research*. París, Francia: UNESCO, 2023.

[17] Departamento Nacional de Planeación, *Documento CONPES 3975 de 2019: Política Nacional para la
Transformación Digital e Inteligencia Artificial*. Bogotá, Colombia: DNP, 2019.

[18] J. Davis y M. Goadrich, "The relationship between Precision-Recall and ROC curves," en *Proc.
23rd International Conference on Machine Learning (ICML '06)*, Pittsburgh, PA, EE. UU., 2006, pp.
233–240.

[19] T. Saito y M. Rehmsmeier, "The precision-recall plot is more informative than the ROC plot when
evaluating binary classifiers on imbalanced datasets," *PLoS ONE*, vol. 10, no. 3, art. e0118432,
mar. 2015.

[20] M. Hardt, E. Price, y N. Srebro, "Equality of opportunity in supervised learning," en *Advances
in Neural Information Processing Systems (NeurIPS)*, vol. 29, 2016.

[21] Y. Gao *et al.*, "Retrieval-augmented generation for large language models: A survey," *arXiv
preprint* arXiv:2312.10997, 2023.

[22] S. Es, J. James, L. Espinosa-Anke, y S. Schockaert, "RAGAS: Automated evaluation of retrieval
augmented generation," en *Proc. 18th Conference of the European Chapter of the Association for
Computational Linguistics (EACL): System Demonstrations*, 2024.

[23] K. Krippendorff, *Content Analysis: An Introduction to Its Methodology*, 4a ed. Thousand Oaks,
CA, EE. UU.: SAGE Publications, 2018.

[24] J. R. Landis y G. G. Koch, "The measurement of observer agreement for categorical data,"
*Biometrics*, vol. 33, no. 1, pp. 159–174, mar. 1977.

[25] V. Venkatesh, M. G. Morris, G. B. Davis, y F. D. Davis, "User acceptance of information
technology: Toward a unified view," *MIS Quarterly*, vol. 27, no. 3, pp. 425–478, sep. 2003.

[26] J. W. Creswell y V. L. Plano Clark, *Designing and Conducting Mixed Methods Research*, 3a ed.
Thousand Oaks, CA, EE. UU.: SAGE Publications, 2018.

[27] B. Efron y R. J. Tibshirani, *An Introduction to the Bootstrap*. Nueva York, NY, EE. UU.:
Chapman & Hall/CRC, 1993.

[28] V. Braun y V. Clarke, "Using thematic analysis in psychology," *Qualitative Research in
Psychology*, vol. 3, no. 2, pp. 77–101, 2006.

[29] Ministerio de Ciencia, Tecnología e Innovación (Minciencias), *Modelo de Medición de Grupos de
Investigación, Desarrollo Tecnológico o de Innovación y de Reconocimiento de Investigadores del
Sistema Nacional de Ciencia, Tecnología e Innovación*. Bogotá, Colombia: Minciencias. (Se cita la
tipología de productos; el año de la versión vigente se fija al radicar, y por eso no se declara
aquí un número de convocatoria que no ha sido verificado.)

[30] Congreso de la República de Colombia, *Ley 23 de 1982, sobre derechos de autor*. Bogotá,
Colombia, ene. 1982.

**Declaración de uso de herramientas de IA en la elaboración de este anteproyecto.** En la
construcción de este documento se emplearon asistentes de IA generativa —**Claude** (Anthropic) y
**ChatGPT** (OpenAI)— para cuatro tareas: apoyo en la identificación y depuración de los referentes
teóricos del campo, estructuración y redacción de borradores de los apartados, conteo y verificación
automática de la extensión de las secciones sujetas a límite de palabras, y verificación de
consistencia interna entre citas del cuerpo y entradas de esta lista, y entre objetivos específicos,
productos, actividades y cronograma. Toda decisión de contenido, alcance, presupuesto y método fue
adoptada y revisada por el investigador principal.

**Alcance real de la verificación bibliográfica — declarado como pendiente, no como cumplido.** Las
30 entradas de esta lista corresponden a obras que el investigador principal identifica como
existentes y reconocibles en su campo, y su selección privilegió deliberadamente obras seminales y
revisiones consolidadas frente a resultados puntuales de baja circulación. Sin embargo, **en esta
versión del documento los metadatos de cada entrada —volumen, número, artículo, rango de páginas,
año y DOI— no fueron contrastados uno por uno contra el registro del editor**, y por esa razón
algunas entradas se dejan sin número de artículo o sin rango de páginas en lugar de completarlas con
un dato no verificado —así ocurre con [5], [12], [20], [22] y con el año de la versión vigente del
modelo de medición de Minciencias—. La revisión de los 30 registros contra la fuente del editor, la incorporación
de DOI y la consulta del texto completo por parte del investigador principal quedan registradas como
**pendiente 13 previo a la radicación**, en los mismos términos en que el apartado de pendientes
declara los demás requisitos sin confirmar. No se declara aquí ninguna verificación que no se haya
realizado.

**Uso de IA durante la ejecución.** Los tres planos de uso previstos —la IA como artefacto
construido, la IA como objeto de auditoría y la IA como asistencia de desarrollo y análisis— están
detallados en el apartado "Aplicación de herramientas IA". Durante la ejecución, todo uso de
asistentes generativos queda registrado en la bitácora de trazabilidad de uso de IA, con revisión
humana obligatoria de cada artefacto generado y con la restricción, ya declarada, de no exponer
datos de estudiantes a servicios de terceros.

---

## Aspectos éticos

| Aspecto ético | Argumentación |
|---|---|
| **a) Posible impacto sobre poblaciones sujeto de estudio o intervenida** | Hay que distinguir dos conjuntos de personas, porque su exposición es distinta. **Los estudiantes del periodo cerrado** no son participantes: aportan registros que la institución ya posee, tratados de forma seudonimizada, sin contacto, sin intervención y **sin que se emita ninguna alerta sobre ellos** —exclusión (b) del alcance—. El riesgo que les concierne no es de procedimiento sino de **clasificación**: un sistema que ordena personas por su probabilidad de fracaso puede, si se usa mal, convertir una alerta en una etiqueta. Contra eso operan cuatro medidas de diseño, no de intención: ninguna decisión automatizada, revisión humana previa a cualquier salida utilizable, prohibición de dirigirse a estudiantes identificados durante el piloto y **medición obligatoria de la equidad de la señal** (H3), cuya refutación declara el prototipo no adoptable. Se declara además el riesgo de **estigmatización diferencial**: si los falsos positivos se concentran en un subgrupo, el daño no es estadístico sino social, y por eso el indicador elegido es la diferencia de tasa de falsos positivos y no una métrica agregada. **Los participantes voluntarios** son docentes-tutores y estudiantes: los primeros enfrentan un riesgo laboral —sus respuestas podrían leerse como juicio sobre un colega o sobre su propia práctica—, mitigado con convocatoria sin intermediación de jefaturas, reporte agregado y anonimizado y declaración expresa de no incidencia en evaluación de desempeño; los segundos enfrentan una asimetría de poder frente al docente que solicita su participación, mitigada porque **no se convoca a estudiantes de asignaturas a cargo del investigador principal**, porque trabajan sobre **perfiles sintéticos y nunca sobre su propia situación** y porque no se ofrecen incentivos económicos, precisamente para no inducir la participación. No se interviene poblaciones vulnerables ni se realizan procedimientos sobre personas. |
| **b) Adecuado uso y manejo de la información, incluyendo consentimiento informado cuando sea necesario** | Este proyecto trata **datos personales de estudiantes** y se sujeta íntegramente a la Ley Estatutaria 1581 de 2012 [15]. **Base del tratamiento:** los datos se recogieron con finalidad académica dentro de la relación institucional; su uso para esta investigación **requiere autorización institucional expresa y aval del Comité de Ética** (pendientes 5 y 6), y este documento **no supone concedida ninguna de las dos**. Ninguna extracción de datos inicia antes de ambas. **Minimización:** solo tres familias de variables —calificaciones parciales y sus pesos, asistencia y traza de actividad—; se excluyen expresamente datos socioeconómicos, psicológicos y de salud (exclusión (g) del alcance). **Seudonimización en origen:** los identificadores se sustituyen por códigos antes de que los datos lleguen al análisis; la tabla de correspondencia y los datos crudos permanecen en la infraestructura que la institución autorice, bajo su responsabilidad, con control de accesos registrado. **Circulación restringida:** al modelo de lenguaje se le exponen **únicamente indicadores derivados y seudonimizados**, nunca la base ni identificadores; el uso de un servicio de terceros incluso con datos seudonimizados está sujeto a confirmación institucional (pendiente 7) y la configuración principal es un modelo de pesos abiertos en infraestructura controlada, precisamente para no depender de esa confirmación. Al proveedor que se contrate se le exige poder **desactivar el uso de los datos enviados para entrenamiento**. **Consentimiento informado escrito** (instrumento I8, sujeto a aprobación del Comité) para los docentes-tutores y los estudiantes voluntarios, con propósito, voluntariedad, tratamiento anonimizado, grabación cuando aplique, conservación, derecho de retiro sin consecuencia y contacto del investigador. **Rectificación y destrucción:** existe procedimiento de rectificación documentado en el protocolo I3, y el conjunto seudonimizado y las grabaciones se destruyen al cierre del proyecto, con constancia. **Publicación:** resultados agregados; los anexos de métricas se publican por caso seudonimizado y por subgrupo con su n, y se suprime todo subgrupo cuyo tamaño permita reidentificar a una persona. |
| **c) Respeto por el ambiente circundante, trato digno a seres humanos y otros seres sintientes** | **No se experimenta con animales ni con otros seres sintientes: ese componente no aplica**, y se declara expresamente en lugar de omitirse. El trato digno a los participantes humanos se concreta en voluntariedad, tiempos acotados y respetados (sesión de evaluación de utilidad de menos de 60 minutos, prueba de usabilidad de menos de 30), lenguaje no evaluativo en los instrumentos, derecho a no responder cualquier ítem y ausencia de cualquier consecuencia académica o laboral derivada de participar o de negarse. Hay una exigencia adicional de trato digno propia de este proyecto: **el tono de los mensajes generados**. Un texto que le dice a alguien que probablemente va a fracasar puede ser correcto y humillante a la vez, de modo que la pauta de generación prohíbe atribuir el riesgo a rasgos de la persona, obliga a referirse a hechos y plazos verificables y a nombrar siempre una ruta de apoyo; la prueba de usabilidad (I7) incluye ítems abiertos sobre el tono precisamente para detectar esto con estudiantes, sobre perfiles sintéticos. Respecto del ambiente: el proyecto no consume materiales físicos relevantes ni genera residuos electrónicos —no se compra hardware—, pero sí tiene una huella que conviene no ocultar, el **consumo energético del cómputo con modelos de lenguaje**. Se mitiga por diseño: los datos duros los resuelve código determinista y no el modelo, lo que evita generaciones repetidas; se usa un modelo pequeño (8B) en lugar de uno de frontera; la muestra de auditoría es de 100 respuestas y no de miles; y no se entrena ni se ajusta finamente ningún modelo. La modalidad virtual del estudio elimina desplazamientos. |
| **d) Garantía de respeto a los criterios básicos de propiedad intelectual y derechos de autor** | Cuatro planos. **Corpus documental institucional:** el índice de recuperación se construye sobre documentos **de la propia CUN** —Syllabus vigente del programa piloto, reglamento estudiantil, catálogo de rutas de apoyo, calendario académico—, usados dentro de la institución y para una finalidad institucional, con **ficha de procedencia por fragmento** (documento, versión, apartado); no se indexan obras de terceros con licencia restrictiva ni material comercial, y las citas en las respuestas generadas remiten al documento y apartado exactos, lo que es atribución y no reproducción encubierta. **Componentes de software:** se emplean componentes de código abierto y modelos de pesos abiertos respetando sus licencias, que se inventarían en la documentación de arquitectura con su licencia declarada; el uso de servicios comerciales de modelo de lenguaje se rige por los términos del proveedor, incluida la desactivación del uso de datos para entrenamiento. **Autoría de lo producido:** conforme a la Ley 23 de 1982 [30], la autoría corresponde a la persona natural que crea la obra en su forma de expresión; el código, la arquitectura, los instrumentos, el informe y la guía se atribuyen al **investigador principal**, con declaración explícita de la contribución del **auxiliar de investigación de semillero** —coautoría del anexo de fiabilidad—, y **en ningún caso al proveedor del modelo de lenguaje**, que no es autor ni coautor. El uso de asistentes de IA en el desarrollo y en el análisis se declara en la bitácora de trazabilidad y en la declaración incorporada a este documento, en aplicación del mismo principio de simetría que se exige al estudiante. **Cesión y crédito:** los productos —prototipo, arquitectura, protocolo de datos, conjunto de datos documentado, protocolo de auditoría, informe, manuscrito, guía y lista de salvaguardas— se ceden a la institución conforme a la carta de cesión de derechos del Anexo 1, con reconocimiento de la autoría del investigador principal y del auxiliar. El **conjunto de datos seudonimizado no se cede ni se publica como dato abierto**: contiene información derivada de datos personales y su custodia es institucional; lo que se publica es el diccionario, el código que lo construye y las métricas agregadas. |

---

## Estructura de objetivos y actividades

**Nota sobre las fechas.** Las columnas de inicio y fin se expresan en **semanas relativas contadas
desde la firma del acta de inicio**, porque las fechas del cronograma institucional (numeral 9 de los
Términos de Referencia) ya transcurrieron y no se han confirmado nuevas; el anclaje a calendario queda
pendiente de la respuesta de la DNI (pendiente 4). La numeración de actividades es **consecutiva a
través de los tres objetivos específicos (1 a 14)**, no se reinicia en cada objetivo, y es la misma que
referencia el cronograma.

### Objetivo específico 1

Caracterizar las variables de riesgo disponibles, constituir el conjunto de datos seudonimizado del
periodo cerrado y acordar con el área de bienestar y permanencia la definición operativa de riesgo y la
línea base de comparación (semanas 1 a 4).

| # | Actividad | Resultado esperado | Indicador de cumplimiento | Medio de verificación | Inicio | Fin |
|---|---|---|---|---|---|---|
| 1 | Gestión de la autorización institucional de acceso a los datos y del aval del Comité de Ética, con definición escrita del rol del investigador frente a los datos y de los instrumentos a aplicar | Habilitantes gestionados y ruta de datos definida por escrito, o activación documentada de la contingencia | 1 solicitud de acceso radicada ante dirección de programa, Registro y Control y área de aula virtual, y 1 radicación ante el Comité de Ética; decisión sobre contingencia tomada al cierre de S2 | Radicados con fecha, respuesta institucional y acta de decisión sobre la ruta | Semana 1 | Semana 3 |
| 2 | Caracterización de fuentes y variables (I1): campos, granularidad, exportabilidad y faltantes, con verificación efectiva de la traza de actividad del aula virtual | Inventario de variables disponible y disponibilidad real de la traza verificada (pendiente 8 resuelto con dato) | Ficha I1 diligenciada para las 3 fuentes, con porcentaje de faltantes reportado por variable | Ficha de inventario y reporte de exportación de prueba | Semana 1 | Semana 3 |
| 3 | Taller con el área de bienestar y permanencia: definición operativa de riesgo, formulación de la línea base de corte de notas, capacidad semanal de atención, umbral y punto de operación, y punto de corte intermedio de evaluación | Acta de definición operativa, línea base y punto de operación firmada **antes** de cualquier evaluación | 1 acta I2 firmada y fechada, con los cinco elementos registrados | Acta I2 firmada y lista de asistencia del taller | Semana 2 | Semana 4 |
| 4 | Constitución del conjunto de datos seudonimizado estudiante-semana con código reproducible, diccionario de datos y protocolo de seudonimización (I3); cálculo de la prevalencia observada del desenlace | Conjunto de datos auditable y caracterizado, con prevalencia conocida | Cobertura del 100 % de los estudiantes del grupo piloto del periodo cerrado, diccionario completo y prevalencia observada reportada | Conjunto de datos versionado, diccionario, script de construcción y reporte descriptivo | Semana 2 | Semana 4 |

### Objetivo específico 2

Desarrollar el prototipo del asistente en dos capas verificables —canal determinista con clasificador
interpretable y capa de generación aumentada por recuperación anclada al corpus institucional—, con su
arquitectura documentada y su protocolo de tratamiento de datos (semanas 3 a 9).

| # | Actividad | Resultado esperado | Indicador de cumplimiento | Medio de verificación | Inicio | Fin |
|---|---|---|---|---|---|---|
| 5 | Implementación del canal determinista de indicadores semanales (ingeniería de variables definida en I3) con pruebas unitarias sobre casos de control calculados a mano, con participación del auxiliar de investigación de semillero | Canal de indicadores auditable y verificado, no solo funcional | 100 % de los indicadores del diccionario implementados y batería de pruebas unitarias en verde sobre los casos de control | Repositorio versionado, suite de pruebas y reporte de ejecución | Semana 3 | Semana 6 |
| 6 | Entrenamiento y calibración del clasificador interpretable (regresión logística regularizada y árbol de profundidad limitada) con validación cruzada estratificada y separación por estudiante; fijación del punto de operación del acta I2 | Modelo interpretable calibrado en el punto de operación acordado, con coeficientes y reglas legibles | Ambas familias entrenadas y comparadas, punto de operación coincidente con el acta I2 y coeficientes/reglas documentados | Cuadernos de análisis, reporte de validación cruzada y anexo de coeficientes | Semana 5 | Semana 7 |
| 7 | Conformación y versionado del corpus documental institucional (Syllabus vigente, reglamento estudiantil, rutas de apoyo, calendario), segmentación, incrustaciones e indexación vectorial con ficha de procedencia por fragmento | Índice documental trazable, con procedencia verificable fragmento a fragmento | 4 tipos de documento indexados y 100 % de los fragmentos con ficha de procedencia (documento, versión, apartado) | Índice vectorial versionado y tabla de procedencia de fragmentos | Semana 4 | Semana 7 |
| 8 | Implementación de la capa de generación aumentada por recuperación y de las plantillas, con inserción determinista de datos duros, e interfaz conversacional mínima; ciclo interno de iteración con instrumentación automática | Prototipo funcional de extremo a extremo que explica y cita, sin escribir datos duros | Prototipo que, dado un caso, entrega señal, explicación, recomendación y lista de fragmentos citados; ciclo de iteración documentado con la instrumentación declarada como no evidencia | Demostración registrada, repositorio y bitácora de iteración | Semana 6 | Semana 9 |
| 9 | Documentación de la arquitectura de referencia (componentes, flujos, decisiones y alternativas descartadas), del protocolo de tratamiento de datos y del inventario de licencias de componentes, con participación del auxiliar de semillero en el levantamiento de la documentación | Arquitectura y protocolo entregables y replicables | 1 documento de arquitectura con diagrama y mapa de dependencias, 1 protocolo de datos y 1 inventario de licencias | Documentos versionados y bitácora de uso de IA en el desarrollo | Semana 6 | Semana 9 |

### Objetivo específico 3

Evaluar el prototipo en validación retrospectiva —desempeño, anticipación, verificabilidad y equidad—,
valorar su utilidad con docentes-tutores y su usabilidad con estudiantes voluntarios sobre perfiles
sintéticos, y formular la lista de salvaguardas y la guía de adopción (semanas 7 a 12).

| # | Actividad | Resultado esperado | Indicador de cumplimiento | Medio de verificación | Inicio | Fin |
|---|---|---|---|---|---|---|
| 10 | Validación retrospectiva del detector contra la línea base (protocolo I4): sensibilidad, precisión, valor predictivo negativo, área bajo la curva ROC y prevalencia observada, con curva de precisión-exhaustividad e intervalos por bootstrap; cálculo de la anticipación en semanas | Desempeño y anticipación medidos frente a la práctica actual, no frente a una cifra ideal | Las 5 métricas y la prevalencia reportadas para prototipo y línea base sobre los mismos datos, con intervalos de confianza; anticipación reportada con mediana y rango | Reporte de validación, anexo de métricas crudas por caso y matrices de confusión de ambas reglas | Semana 7 | Semana 10 |
| 11 | Análisis de equidad por segmentos: diferencia en tasa de falsos positivos entre subgrupos autorizados, con su n, y sensibilidad por subgrupo; declaración nominal de las variables no disponibles | Comportamiento de la señal entre subgrupos establecido o declarado no evaluable, sin silencios | Diferencia de tasa de falsos positivos calculada para todos los subgrupos con n suficiente y toda variable no autorizada declarada por su nombre | Anexo de métricas por subgrupo con n y reporte de equidad | Semana 9 | Semana 11 |
| 12 | Auditoría de la capa generativa: congelamiento de la pauta I5 antes de generar la muestra, generación estratificada de 100 respuestas, entrenamiento del segundo anotador con piloto de 10, anotación de las 100 con los dos códigos separados y doble anotación de 30; fiabilidad y conteo de errores de dato duro | Verificabilidad medida con evidencia humana y fiabilidad reportada, con los fallos de recuperación distinguidos de los de generación | Pauta congelada con acta anterior a la generación; 100 respuestas anotadas, 30 con doble anotación; α de Krippendorff y κ por código reportados con su interpretación; conteo absoluto de errores de dato duro | Acta de congelamiento, base de anotación, matriz de dos por dos, reporte de fiabilidad y de desacuerdos | Semana 8 | Semana 11 |
| 13 | Evaluación de utilidad con ≥ 6 docentes-tutores (I6, diseño intrasujeto con orden aleatorizado y comparación pareada contra puntaje sin explicación) y prueba de usabilidad con ≥ 10 estudiantes voluntarios sobre perfiles sintéticos (I7), con consentimiento informado previo | Utilidad y usabilidad valoradas por terceros, no por el autor del prototipo | ≥ 6 docentes-tutores adscritos a ≥ 2 programas de la Escuela de Ingenierías y ≥ 10 estudiantes participantes, con consentimiento registrado y las dos condiciones aplicadas a cada docente | Consentimientos, bases de respuestas anonimizadas, registro de aleatorización y reporte descriptivo | Semana 9 | Semana 11 |
| 14 | Análisis integrado y triangulación de los cinco ramales; redacción del informe de validación, del manuscrito, de la guía de adopción y de la lista de salvaguardas (I9); socialización, entrega a la DNI y certificación del auxiliar de semillero | Productos comprometidos entregados, socializados y con sus condiciones de uso declaradas | 1 informe de validación, 1 manuscrito, 1 guía de adopción, 1 lista de salvaguardas, 1 taller de socialización con ≥ 10 asistentes y 1 certificación de semillero | Matriz de triangulación, documentos radicados, acta de socialización y certificación emitida | Semana 10 | Semana 12 |

---

## Cronograma de actividades

El cronograma se estructura por **número de actividad** de la estructura de objetivos y actividades (1 a
14). Se expresa en **semanas relativas (S1 a S12)** contadas desde la firma del acta de inicio, por las
razones ya señaladas: el cronograma institucional publicado en los Términos de Referencia corresponde a
fechas ya transcurridas y el anclaje a calendario queda pendiente de confirmación de la DNI. La duración
total es de **12 semanas (3 meses)**, consistente con la orientación del numeral 7 de priorizar
productos entregables en aproximadamente tres meses.

| Actividad # | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | S11 | S12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | X | X | X | | | | | | | | | |
| 2 | X | X | X | | | | | | | | | |
| 3 | | X | X | X | | | | | | | | |
| 4 | | X | X | X | | | | | | | | |
| 5 | | | X | X | X | X | | | | | | |
| 6 | | | | | X | X | X | | | | | |
| 7 | | | | X | X | X | X | | | | | |
| 8 | | | | | | X | X | X | X | | | |
| 9 | | | | | | X | X | X | X | | | |
| 10 | | | | | | | X | X | X | X | | |
| 11 | | | | | | | | | X | X | X | |
| 12 | | | | | | | | X | X | X | X | |
| 13 | | | | | | | | | X | X | X | |
| 14 | | | | | | | | | | X | X | X |

**Correspondencia con los objetivos específicos:** OE1 → actividades 1 a 4 (**S1–S4**); OE2 →
actividades 5 a 9 (**S3–S9**); OE3 → actividades 10 a 14 (**S7–S12**). Las tres ventanas coinciden
exactamente con las declaradas en los objetivos específicos y en el alcance.

**Por qué los traslapes son necesarios y no cosméticos.** La actividad 5 empieza en S3, dentro de la
ventana del OE1, porque el canal determinista se implementa contra el diccionario de datos y no contra
la base final: se puede construir y probar con casos de control mientras el conjunto se consolida. La
actividad 7 —corpus documental e índice— empieza en S4 y **no depende en absoluto del acceso a los datos
académicos**, de modo que avanza aunque la autorización se demore; junto con las actividades 5 y 9, que
tampoco requieren la base real, forma el frente de trabajo que puede sostenerse mientras el habilitante
está pendiente, y es la razón por la cual un retraso de la autorización no detiene el proyecto entero.
La actividad que sí queda bloqueada es la 6, y de ahí que el hito de decisión se sitúe en S2 y no más
tarde. La actividad 6 no puede empezar antes de S5
porque exige el conjunto de datos (actividad 4, fin S4) y el punto de operación del acta I2 (actividad
3, fin S4): ese orden es una salvaguarda, no una preferencia de planeación. La actividad 10 arranca en
S7, en cuanto el clasificador está calibrado (actividad 6, fin S7), y no espera a que la capa generativa
esté terminada, porque el desempeño del detector es independiente de ella. La actividad 12 arranca en S8
sobre las primeras respuestas ya generables del prototipo (actividad 8, en curso desde S6) y se extiende
a S11 porque la anotación de 100 respuestas con dos códigos y doble anotación del 30 % es trabajo
humano, no un lote de cómputo. Y la actividad 11 se coloca en S9–S11, después de la validación global
(actividad 10), porque el análisis por subgrupos recalcula sobre las mismas predicciones ya producidas y
adelantarlo no ahorraría tiempo.

**Hito de decisión declarado.** Al cierre de **S2** se decide si el proyecto continúa por la ruta
principal —datos reales autorizados— o activa la ruta de contingencia con conjunto sintético calibrado.
La decisión se registra en acta y se informa a la DNI si se activa la contingencia. El cronograma no
cambia en ninguno de los dos escenarios; lo que cambia es el valor probatorio de las actividades 10 y
11, y así se reporta en el informe.

---

## Control de cambios

Última fila del INV-FO03. Se diligencia con la versión que efectivamente se radica.

| Fecha | Versión | Descripción del cambio |
|---|---|---|
| 15/08/2026 | 1.0 | Versión inicial del anteproyecto, estructurada sobre el formato INV-FO03 (Anexo 2) y auditada contra los Términos de Referencia 2026 (Fase II). Cronograma en semanas relativas S1–S12 por vencimiento del cronograma del numeral 9. |
| Por definir | 1.1 | Reservada para el anclaje del cronograma a fechas calendario y el cierre de los pendientes 1 a 13, una vez la DNI responda las consultas radicadas. |
