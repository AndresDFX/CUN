# 26ET2-G-001 — Sistema de Información Agropecuario Integral con Módulo Pecuario y Chatbots, aplicado a la Finca El Paraíso (Anzoátegui, Tolima)

**Sustentación:** martes 18 de agosto de 2026 · 6:00 p. m. – 6:20 p. m. (primer grupo de la jornada) · **Mi rol:** Jurado 2
**Integrantes:** Diomedes Igua Hernández (diomedes.igua@cun.edu.co), Adolfo Escobar Buelvas (adolfoescobar@cun.edu.co), Jorge Carlos Polo Muñoz (jorge.polo@cun.edu.co)
**Línea:** Liderazgo y Adaptación con Tecnologías Emergentes
**Documentos leídos:** `Sistema de información agropecuario integral.pdf` (273 páginas, versión única en la carpeta), `Sistema de información agropecuario integral.pptx` (17 diapositivas)

> Nota de lectura: la carpeta del grupo tiene un solo documento de trabajo de grado, sin versiones alternas. Varias diapositivas (8, 9, 10, 11, 12, 13, 16) son imágenes sin texto extraíble; cuando esta ficha dice que algo «no aparece en la presentación» se refiere al texto extraíble y hay que confirmarlo en sala.

---

## 1. Resumen para leer en 5 minutos

**El problema.** La gestión pecuaria de pequeños productores depende de registros manuales con alta probabilidad de error, carece de trazabilidad en alimentación, reproducción y sanidad, desconoce los costos reales de producción y enfrenta barreras de conectividad y alfabetización digital (p. 32). El escenario es la Finca El Paraíso, vereda Fonda Colombia, municipio de Anzoátegui, Tolima (p. 40).

**Qué hicieron.** Es la Fase II de un producto que ya existía: extiende el Mínimo Producto Viable agrícola «TuFinca», construido en la Especialización en Gestión TIC (p. 40), agregándole dos cosas: un módulo pecuario (inventario animal, reproducción, sanidad, alimentación y costos) y un chatbot conversacional embebido en la plataforma mediante un componente WebChat (p. 22). El stack declarado es Blazor Server, ASP.NET Core Web API, Entity Framework Core y Microsoft SQL Server (p. 171), desplegado en Azure App Service con la API como servicio independiente (pp. 192-193).

**Con qué método.** Estudio descriptivo y aplicado, enfoque mixto (p. 65), Scrum con 14 sprints de dos semanas entre diciembre de 2025 y junio de 2026 (p. 45). Participantes: seis operarios pecuarios, muestreo no probabilístico intencional que corresponde a la totalidad de la población pecuaria de la finca (pp. 67-68). Instrumentos: revisión documental de la Fase I, entrevista semiestructurada y observación directa (p. 71). Nivel de madurez declarado TRL 5-6, sin pretensión de despliegue comercial (p. 42). Plantean H₀ y H₁ formales (p. 34) y las contrastan con estadística descriptiva (p. 66).

**Qué obtuvieron.** Los cuatro objetivos específicos tienen sección de resultados que los cierra. El OE4 es una evaluación comparativa de tres condiciones —manual, aplicación web y chatbot— con medidas repetidas, tres iteraciones por participante y caso (pp. 196-197): reducciones de tiempo de 63,5 % a 90,6 % con la aplicación y de 66,8 % a 94,9 % con el chatbot (p. 209); registros completos de 72,2 % a 97,8 % (aplicación) y 95,6 % (chatbot); tasa de errores de 18,9 % a 3,3 % y 4,4 %; disponibilidad del historial de 66,7 % a 100 % (p. 210). El chatbot alcanzó 93,3 % de exactitud sobre 60 consultas, 5,8 segundos de respuesta promedio, 8,3 % de reformulación y satisfacción de 4,5/5 (p. 211). Los conteos crudos están publicados (65/90, 88/90, 47/60, 56/60 — p. 213), lo que permite verificar los porcentajes.

**Qué entregan.** Sistema desplegado y funcionando en Azure, con acta de certificación y entrega del sistema a la unidad productiva (p. 218, Anexo 8). El documento califica sus propios hallazgos como «mejoras descriptivas» y advierte que no constituyen demostración poblacional (p. 238).

---

## 2. Coherencia título → objetivo → resultados

**Título → objetivo general → pregunta.** Los tres dicen lo mismo: el título anuncia sistema integral + módulo pecuario + chatbots aplicado a la Finca El Paraíso; el objetivo general dice «Desarrollar un sistema de información agropecuario integral, a partir del mínimo producto viable (TuFinca) existente, incorporando un módulo pecuario y una herramienta conversacional basada en chatbot… en la Finca El Paraíso» (p. 35); y la pregunta de investigación pregunta si esa implementación mejora la eficiencia operativa y la trazabilidad en esa finca (p. 34). El verbo «desarrollar» del objetivo general fija el techo del trabajo, y el trabajo llega hasta ahí: desarrolla, despliega y mide. **No hay objetivo huérfano, que es el hueco más frecuente en esta rúbrica.**

Única fricción de redacción: el título dice «Chatbots» en plural y el objetivo general transcrito por la Dirección dice «herramientas conversacionales basadas en chatbots», mientras el documento entrega **un** chatbot con **un** canal (WebChat) y declara WhatsApp y otras plataformas de mensajería como trabajo futuro (p. 22). Está declarado de frente, no es un ocultamiento, pero un jurado que solo lea el título puede llegar esperando varios canales.

| Objetivo específico (p. 35) | ¿Se cumplió? | Evidencia | Qué falta / qué preguntar |
|---|---|---|---|
| **OE1.** Diseñar el módulo pecuario para gestionar inventario animal, reproducción, sanidad, alimentación y costos | **Sí, y por encima del verbo.** El objetivo dice «diseñar»; entregan implementado y en operación | Arquitectura multicapa y modelo de datos en 3FN con el animal como núcleo (pp. 118-136); seis componentes funcionales con pantallas, formularios y servicios REST (pp. 138-157); dashboard consolidado con indicadores financieros (pp. 158-164) | Nada sustantivo. El verbo del objetivo quedó por debajo de lo entregado |
| **OE2.** Diseñar la arquitectura funcional del chatbot: flujos de interacción, tipos de usuario y lógica de comunicación | **Sí** | Arquitectura de cinco capas descrita capa por capa (pp. 168-171); tres tipos de usuario con operaciones autorizadas, reutilizando el modelo de autenticación de TuFinca (p. 172); flujo general de siete etapas (pp. 174-176); tabla de intenciones conversacionales (p. 177) | **La capa 2, el «motor conversacional», es la única que no tiene tecnología nombrada** (Tabla 18, p. 171). Todas las demás sí: Blazor, ASP.NET Core, EF Core, SQL Server → pregunta prioritaria 2 |
| **OE3.** Integrar el chatbot mediante servicios REST y procesamiento de lenguaje natural | **Sí** | Arquitectura de integración (pp. 183-184); WebChat embebido en la interfaz (pp. 185-187); incidencias de configuración de endpoints declaradas y corregidas —honestidad técnica poco frecuente— (p. 188); despliegue en Azure App Service verificado (pp. 191-194) | El chatbot ejecuta consultas y registros según Tabla 21 (p. 177) y Tabla 26 (p. 209), pero las capturas de validación mostradas son de consulta (pp. 189-190). Vale confirmar el registro escrito por voz/texto en el demo |
| **OE4.** Evaluar la eficiencia operativa y la trazabilidad **antes y después** de la implementación, con indicadores y análisis comparativos | **Sí en ejecución; con una salvedad de diseño en el «antes»** | Diseño de evaluación completo (pp. 195-203), 20 indicadores codificados (p. 202), umbrales fijados *antes* de aplicar el instrumento (pp. 199-200), resultados con conteos crudos (pp. 209-213), contraste de hipótesis (pp. 237-238) | El objetivo dice «antes y después», pero el diseño es de **medidas repetidas concurrentes** con los mismos seis operarios que ya conocían el sistema (pp. 196-197), y el documento reconoce que la finca no es ajena a la transformación digital porque participó en las fases previas (p. 238). El «antes» es una condición reconstruida, no una línea base histórica → pregunta prioritaria 1 |

---

## 3. Fortalezas verificables

1. **Los cuatro objetivos cierran, y el cuarto es el que casi nadie ejecuta.** El «evaluar» que en la mayoría de los trabajos queda como promesa aquí tiene diseño, instrumento, umbrales previos, resultados y contraste de hipótesis (pp. 195-213, 237-238).
2. **Los umbrales de interpretación se fijaron antes de medir y se declaran como locales, no normativos** (p. 199: «Los umbrales adoptados no corresponden a estándares poblacionales ni a valores normativos de aplicación general»). Es exactamente la precaución que se le pide a un trabajo profesionalizante.
3. **Publican los conteos crudos, no solo los porcentajes** (Tabla 30, p. 213: 65/90, 88/90, 86/90, 12/18, 47/60, 56/60). Recalculados, los porcentajes cuadran: 65/90 = 72,2 %; 88/90 = 97,8 %; 17/90 = 18,9 %; 56/60 = 93,3 %. Es la firma de una medición que de verdad ocurrió.
4. **Honestidad sostenida sobre los límites.** Declaran muestra de 6, sesgo por participación voluntaria, estudio de caso único y periodo corto (p. 45); llaman a sus propios hallazgos «mejoras descriptivas» (p. 238); y advierten que la validación en una unidad productiva con seis participantes es «insuficiente para generalizar» (p. 244). Incluso reconocen que su indicador de trazabilidad todavía no cubre auditoría completa (p. 232).
5. **El producto existe y hay evidencia de entrega.** Despliegue en Azure App Service documentado (pp. 192-194) y acta de certificación y entrega firmada con la unidad productiva (p. 218).
6. **Continuidad declarada con la Fase I sin apropiársela.** Citan el MPV previo como antecedente (p. 64, referencia en p. 254) y aclaran que la validación de esta fase usó instrumentos nuevos diseñados específicamente para ella (p. 64).
7. **Arquitectura defendible por decisión, no por moda.** El chatbot no persiste datos ni administra permisos: consume los mismos servicios REST y el mismo modelo de autorización de la aplicación (pp. 170, 172). Eso garantiza una sola fuente de verdad y es la decisión técnicamente correcta.

---

## 4. Debilidades y huecos (con página)

1. **El «antes» del OE4 es reconstruido, no histórico.** El objetivo promete medir «antes y después de la implementación» (p. 35) y la Tabla 23 registra «Manual como condición previa» (p. 197), pero el diseño es de medidas repetidas donde «cada participante realizó los mismos casos de uso bajo las condiciones aplicables» y tres iteraciones por caso (p. 196). Mitigan con casos equivalentes no idénticos y alternancia del orden (p. 196), pero el efecto de expectativa sobre la condición manual no se controla y de ahí salen las cifras titulares de 63-95 %.
2. **El motor conversacional no tiene tecnología nombrada en 273 páginas.** La Tabla 18 lo describe funcionalmente (p. 171) y el mismo párrafo afirma que la solución «se apoya exclusivamente» en Blazor Server, ASP.NET Core Web API, EF Core y SQL Server, sin componentes externos (p. 171). No aparece ningún servicio de NLU ni modelo de lenguaje en el documento (buscado en pp. 165-194 y en referencias, pp. 250-255: OpenAI 2021 e IBM Watson 2021 figuran solo como bibliografía, nunca como tecnología implementada). Sin esto, el 93,3 % de exactitud no es interpretable: cambia de significado según si las intenciones se resuelven por reglas cerradas o por un modelo.
3. **No hay presupuesto ni costeo en todo el documento.** La palabra «presupuesto» no aparece en las 273 páginas (búsqueda insensible a mayúsculas sobre el documento completo). Al mismo tiempo se reconoce que «la sostenibilidad post-proyecto dependerá de recursos para hosting, mantenimiento y soporte» (p. 46) y se recomienda a la finca adoptar TuFinca como sistema oficial y poner fecha de finalización a los registros en papel (p. 245). Más agudo todavía: el marco conceptual justifica la nube porque da «escalabilidad y respaldos automáticos sin requerir inversión en servidores físicos» (p. 56), sin mencionar el costo recurrente que sustituye a esa inversión. El riesgo operativo queda enunciado y sin cuantificar.
4. **No hay URL de acceso, repositorio ni credenciales de demostración.** El sistema está en Azure (pp. 191-194) pero un tercero no puede verificarlo con el documento en la mano. La evidencia es fotográfica.
5. **Hipótesis formal sin herramienta inferencial.** Se plantean H₀ y H₁ (p. 34) y el tratamiento estadístico declarado es solo descriptivo: frecuencias, porcentajes y medidas de tendencia central (p. 66). El contraste se resuelve comparando contra umbrales operativos propios (pp. 237-238). El documento es honesto al llamarlo «respaldada… dentro del alcance», pero el aparato de hipótesis nula queda sobredimensionado para lo que el diseño permite.
6. **El indicador de trazabilidad no incluye trazabilidad de auditoría.** Reportan 98,9 % de eventos asociados correctamente (p. 210) y en la discusión reconocen que aún falta «el registro automático del usuario responsable, la fecha y hora de las operaciones, el historial de modificaciones» (p. 232). Es honesto, pero la palabra «trazabilidad» está haciendo dos trabajos distintos.
7. **Denominadores del OE4 sin derivación explícita.** De seis participantes por tres iteraciones salen 18 ejecuciones por tarea y cinco tareas evaluadas (pp. 196, 209), pero las bases reportadas son 90 registros, 90 eventos, 60 tareas, 18 consultas y 60 consultas del chatbot (p. 213), sin explicar cómo se compone cada una.
8. **Referencias listadas que nunca se citan en el cuerpo,** aparentemente arrastradas de la fase agrícola o de otro proyecto: ASOHOFRUCOL (picos de cosecha de mango en el Tequendama), Uniminuto «Ruta innovadora del mango», QGIS Development Team, World Bank GIS Lab (PostGIS), MQTT v5.0, Bahga y Madisetti (IoT), Ander-Egg y Yin (2018). Todas aparecen solo en pp. 250-255; ninguna se cita en el texto (QGIS solo figura en la lista de abreviaturas, p. 21).
9. **No hay reporte de similitud.** No se menciona Turnitin ni índice de similitud en ninguna página (buscado en preliminares pp. 26-27 y en anexos pp. 256-270). Es tarea del metodólogo, pero conviene saberlo antes de la sala.
10. **El consentimiento informado se afirma pero no se anexa.** La p. 69 declara que todos los participantes firmaron consentimiento; los anexos van del 1 al 8 (pp. 256-270) y ninguno lo contiene.

---

## 5. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**Pregunta 1 — La línea base**

> «¿Los tiempos del procedimiento manual que reportan en la Tabla 26 se midieron antes de implementar el sistema, o los mismos seis operarios reprodujeron el método manual en la misma jornada de pruebas, cuando ya conocían TuFinca?»

- **Por qué se pregunta:** el OE4 promete evaluar «antes y después de la implementación» (p. 35) y la Tabla 23 clasifica lo manual como «condición previa» (p. 197), pero el diseño descrito es de medidas repetidas simultáneas sobre casos equivalentes (p. 196). De esa comparación salen todas las cifras titulares del trabajo: 63,5 %–90,6 % y 66,8 %–94,9 % (p. 209).
- **Qué la resuelve:** que reconozcan sin rodeos que la condición manual se reprodujo en el mismo periodo, expliquen que por eso alternaron el orden de aplicación entre participantes y usaron casos equivalentes no idénticos (p. 196), y digan qué efecto esperan que eso tenga sobre las cifras. Suma mucho si mencionan que la propia p. 238 ya advierte que la finca venía de la Fase I y que en una finca sin digitalización previa el efecto podría ser mayor.
- **Qué la agrava:** afirmar que existió una medición histórica previa a la implementación sin poder decir cuándo se tomó ni en qué anexo está; o defender las cifras como si fueran un antes-después real.

**Pregunta 2 — Qué es exactamente el motor conversacional**

> «El documento nombra la tecnología de todas las capas —Blazor Server, ASP.NET Core, Entity Framework, SQL Server— menos la del motor conversacional, del que solo dice qué hace: ¿con qué se implementó concretamente la interpretación de intenciones y la extracción de entidades?»

- **Por qué se pregunta:** la Tabla 18 (p. 171) describe el motor conversacional funcionalmente, y el párrafo siguiente afirma que la solución «se apoya exclusivamente» en el stack .NET, sin componentes externos (p. 171). Ningún servicio de NLU ni modelo de lenguaje aparece en el documento. Esto decide cómo se lee el 93,3 % de exactitud sobre 60 consultas (p. 211): con intenciones cerradas y consultas escritas por el propio equipo, ese número mide cobertura de reglas; con lenguaje abierto, mide comprensión.
- **Qué la resuelve:** nombrar el componente y explicar cómo se resuelven intención y entidades; y decir quién redactó las 60 consultas de prueba y si los seis operarios las formularon con sus propias palabras. Si es una implementación propia por reglas, decirlo con claridad es una **buena** respuesta: es coherente con TRL 5-6 y con lo que declararon en p. 171.
- **Qué la agrava:** responder «usa inteligencia artificial» o «procesamiento de lenguaje natural» sin nombrar nada concreto; o descubrir en el intercambio que las 60 consultas de prueba las escribió el mismo equipo que definió las intenciones y eso no está declarado.

**Pregunta 3 — Quién sostiene el producto entregado**

> «El sistema quedó desplegado en Azure y ustedes le recomiendan a la finca dejar los registros en papel en una fecha definida: ¿quién paga y administra ese hosting a partir de hoy, y el sistema sigue en línea?»

- **Por qué se pregunta:** el documento declara la «entrega formal de la solución desarrollada a la unidad productiva» (p. 215) y adjunta el acta de certificación y entrega como Figura 93 / Anexo 8 (p. 218) —es una imagen, así que desde el texto no puedo confirmar quién la firma—, la recomendación 11.1 pide consolidar TuFinca como sistema oficial y definir una fecha de finalización de los registros físicos (p. 245), y la limitación tecnológica reconoce que la sostenibilidad «dependerá de recursos para hosting, mantenimiento y soporte» (p. 46). En 273 páginas no aparece la palabra «presupuesto», y la nube se justifica por no requerir «inversión en servidores físicos» (p. 56) sin nombrar el costo recurrente que la reemplaza. Se le pidió a una unidad productiva real que abandone su respaldo en papel sin un plan de costos.
- **Qué la resuelve:** una respuesta concreta —quién es el responsable técnico, con qué cuenta, con qué costo mensual aproximado, y qué pasa si nadie paga—; o reconocer con franqueza que el plan de sostenibilidad es el vacío del trabajo y que la recomendación de eliminar el papel debe condicionarse a resolverlo. Cualquiera de las dos es una respuesta de nivel.
- **Qué la agrava:** decir que «la finca puede asumirlo» sin cifra; o no saber si el despliegue está arriba hoy, tres días antes de sustentar.

### Banco de reserva

- **Trazabilidad, ¿de qué tipo?** «Reportan 98,9 % de eventos asociados correctamente (p. 210) y en la discusión reconocen que falta el registro automático de usuario responsable, fecha-hora e historial de modificaciones (p. 232): ¿qué mide entonces su indicador de trazabilidad y qué le falta para servir en una auditoría sanitaria?»
- **Hipótesis y estadística.** «¿Por qué plantear una hipótesis nula formal (p. 34) si el tratamiento estadístico declarado es solo descriptivo (p. 66) y el contraste se resuelve contra umbrales propios (pp. 237-238)?»
- **Denominadores.** «Con seis participantes y tres iteraciones salen 18 ejecuciones por tarea: ¿cómo se componen entonces las bases de 90 registros, 60 tareas y 18 consultas de la Tabla 30 (p. 213)?»
- **Registro por chatbot.** «La Tabla 26 reporta tiempos de registro por chatbot (p. 209) y las capturas de validación que muestran son de consulta (pp. 189-190): ¿pueden registrar una vacunación por el WebChat ahora mismo?»
- **Conectividad.** «La conectividad irregular es su primera limitación tecnológica (p. 46) y el modo offline queda como trabajo futuro (p. 244): ¿cómo se comportó la conectividad durante las jornadas de medición y cuántas ejecuciones descartaron por fallas técnicas, que dicen haber registrado por separado (p. 196)?»
- **Relación con la unidad de estudio.** «¿Cuál es su relación con la Finca El Paraíso y cómo se aseguraron de que los seis operarios pudieran declinar participar?» El documento declara sesgo por participación voluntaria (p. 45) pero no declara la posición de los investigadores frente a la finca (buscado en 7.3 Participantes, pp. 67-68, y en Agradecimientos, p. 5). No es un reproche: el acceso a una unidad productiva real es un activo del trabajo, solo debería estar declarado.
- **Escalabilidad afirmada.** «Sostienen que la arquitectura permite escalar a otras fincas del Tolima (p. 43): ¿qué haría falta para instalarla en una segunda finca la semana entrante, y lo probaron?»

---

## 6. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si el demo de la diapositiva 12 no ocurre o falla** → «¿El sistema está en línea en este momento? Si no, ¿desde cuándo no lo está?» (el despliegue documentado está en pp. 192-194). Esto convierte la pregunta 3 en la prioritaria.
- **Si el demo sí corre y funciona** → dejar caer la pregunta 2 sobre el motor y pedir una consulta improvisada: «formúlele al chatbot una consulta con otras palabras, como la diría un operario». Es la verificación más limpia de si hay comprensión de lenguaje o coincidencia de patrones. Hacerlo con respeto y con una sola frase.
- **Si presentan las reducciones de 63-95 % como impacto del proyecto sin matizar** → pregunta 1, directa.
- **Si ya explicaron bien la línea base y la alternancia de condiciones** → soltar pregunta 1 y usar el tiempo en la reserva de trazabilidad-auditoría, que es más fina.
- **Si dicen «inteligencia artificial» o «IA» en la exposición sin nombrar tecnología** → pregunta 2, y añadir: «¿el modelo corre en su infraestructura o llama a un servicio externo?».
- **Si se pasan del tiempo y saltan el OE4** → ir directo a los resultados: «en una frase, ¿cuál fue el resultado del objetivo 4 y qué tan lejos está de ser generalizable?».
- **Si no declaran la muestra de seis participantes ni el carácter de caso único** → pedirlo explícitamente. Está bien defendido en el documento (pp. 45, 67-68, 244) y no declararlo en sala sería perder gratis un punto de honestidad que ya tienen ganado.
- **Si solo habla uno de los tres integrantes** → pedir nominalmente a otro que explique una parte técnica concreta: la arquitectura de integración del chatbot (pp. 183-184) o el diseño de la evaluación comparativa (pp. 196-197). Es la vía legítima para verificar dominio individual.
- **Si atribuyen a Diomedes Igua toda la parte técnica** → recordar que es coautor del MPV de la Fase I (referencia p. 254) y preguntar a los otros dos qué construyeron ellos en esta fase. Con tono neutro: es una pregunta de reparto de trabajo, no de sospecha.
- **Si anuncian WhatsApp como si estuviera hecho** → «la p. 22 lo declara como trabajo futuro: ¿está implementado o es la proyección de la arquitectura?».
- **Si afirman que el sistema «reduce costos» de la finca** → pedir la cifra. El documento no tiene costeo ni presupuesto en ninguna página.

---

## 7. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

Recordar el marco: la nota final es 75 % metodólogo + 25 % jurados; mi voto es la mitad de ese 25 %. Un 5,0 es una propuesta de laureada y exige que **ambos** jurados la pidan; la meritoria (4,6–4,99) se bloquea si cualquier nota individual baja de 4,5.

**Punto de partida.** El documento sostiene una nota alta por sí solo: cuatro de cuatro objetivos con resultados, medición real con conteos crudos verificables, umbrales fijados antes de medir y limitaciones honestas. Para un nivel profesionalizante esto está por encima de lo esperado. Lo que se juega el martes es si el dominio del tema acompaña al documento.

| Criterio | Para 4,6+ necesito ver | Si falta |
|---|---|---|
| **Dominio del tema** | Que nombren y expliquen el motor conversacional sin evasivas, y que sepan cuál es el límite de validez de sus propias cifras del OE4 | Si responden con etiquetas («IA», «PLN») sin sustancia, o si defienden el 63-95 % como impacto poblacional, este criterio cae a 4,0–4,4 |
| **Claridad** | Que en 12 minutos quepan el problema, el método, la muestra de seis, el resultado y el límite; que el demo se entienda sin que nadie lea la pantalla en voz alta | Si el demo consume el tiempo y los resultados quedan en un minuto atropellado, 4,0–4,4 |
| **Coherencia del documento** | Ya está: título, objetivo, pregunta y los cuatro objetivos cierran (pp. 34-35, 195-213). Lo verificado en la ficha lo sostiene | Solo bajaría si en sala contradicen lo escrito, sobre todo sobre la línea base del OE4 |
| **Capacidad de defensa** | Que ante la pregunta de la línea base y la del hosting **reconozcan el límite y lo argumenten**, en vez de defenderlo. Que responda más de uno de los tres | Si esquivan las dos, o si solo uno domina el trabajo, 4,0–4,4 |

**Escenarios concretos.**
- **4,6–4,8:** demo funcionando, motor conversacional nombrado con precisión, y la línea base reconocida como condición reconstruida y no como antes-después histórico. Es el escenario más probable dado el documento.
- **5,0 (laureada, solo si el Jurado 1 coincide):** todo lo anterior, más una respuesta sólida y cuantificada sobre sostenibilidad y hosting, más que los tres integrantes demuestren dominio de partes distintas. Exigente pero no imposible con este documento.
- **4,0–4,4:** el motor conversacional queda sin nombrar, o defienden las cifras como impacto generalizable, o solo uno sabe defender el trabajo. Advertencia: **poner 4,4 bloquea la meritoria del grupo**, así que si voy ahí necesito la página exacta que lo sustente, y aquí las páginas están en las secciones 4 y 5 de esta ficha.
- **Por debajo de 3,6:** no lo veo posible con este documento salvo un derrumbe total en sala.

---

## 8. Observaciones administrativas (no académicas)

- **Equipo de tres integrantes:** cumple el máximo de 3 en Proyecto I/II de especialización. Sin observación.
- **Correos:** los tres correos institucionales del cronograma están bien formados. Nótese que el de Adolfo Escobar Buelvas es `adolfoescobar@cun.edu.co`, sin punto separador, a diferencia del patrón de sus compañeros; conviene confirmarlo si hay que notificarles algo.
- **Sin reporte de similitud.** No hay mención de Turnitin ni de índice de similitud en el documento (buscado en preliminares pp. 26-27 y anexos pp. 256-270). Verificarlo con el metodólogo o la Dirección antes de la sala; no es criterio de jurado, pero pesa 15 % en la rúbrica del ACA 3.
- **Consentimiento informado afirmado sin anexo.** La p. 69 declara consentimiento firmado por todos los participantes; los anexos 1 a 8 (pp. 256-270) no lo incluyen. Observación para la Dirección, no pregunta pública: hay menores de edad ausentes y datos de operarios de por medio.
- **Referencias no citadas, aparente arrastre de la Fase I.** Al menos nueve entradas de pp. 250-255 no se citan en el cuerpo, varias del dominio agrícola/mango/GIS que no corresponde a esta fase (ASOHOFRUCOL 2012 y 2017, Uniminuto 2021 y 2022, QGIS, World Bank GIS Lab, MQTT, Bahga y Madisetti, Ander-Egg, Yin). Reportar al metodólogo como ajuste de APA 7, no bajar nota de jurado por esto.
- **Este grupo abre la jornada** (6:00 p. m., martes 18). El primer grupo suele pagar los problemas de conexión y de compartir pantalla de toda la sala. Si el demo de la diapositiva 12 se cae por causas de la plataforma y no del proyecto, no cargárselo a ellos: pasar a la pregunta 3 y evaluar el producto por la evidencia documental (pp. 192-194, 218).

### Erratas y forma (bloque breve, no se pregunta en sala)

- **Dato inconsistente entre tablas:** «Tareas completadas correctamente» con la aplicación aparece como 98,8 % en la Tabla 27 (p. 210) y en la Tabla 29 (p. 212), pero el conteo crudo de la Tabla 30 es 59/60 = 98,3 % (p. 213) y la narrativa de la discusión dice 98,3 % (p. 232). La variación de +20,0 p. p. reportada también corresponde a 98,3. El 98,8 es errata de transcripción; el dato bueno es 98,3 %.
- Mejora del chatbot en registros completos: +23,3 p. p. en la Tabla 27 (p. 210) frente a 23,4 p. p. en la narrativa (p. 231). Redondeo.
- La diapositiva 1 conserva en sus notas el texto guía de la plantilla («Notas Importantes: Usar máximo 5-6 líneas por diapositiva…») y las diapositivas 14 y 15 repiten casi las mismas notas de conclusiones. Limpieza pendiente, sin efecto en la nota.
- «El proyecto se ejecutó durante un periodo aproximado de siete (7) meses» (p. 45) y, cuatro párrafos después, «aunque se cuenta con seis meses» en las limitaciones metodológicas (p. 45).
- Las declaraciones de originalidad y de exoneración están firmadas «en Bogotá, Cundinamarca» (pp. 26-27); Bogotá es Distrito Capital. Texto de plantilla.
- Las figuras 6 y 7 del contexto productivo municipal son de 2011-2013 (pp. 43-44); el documento explica de frente por qué usa datos de esa vigencia (limitada disponibilidad de datos públicos actualizados, p. 44). Bien resuelto, no es un hueco.
