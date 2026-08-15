# 26ET2-G-013 — Diseño de una estrategia de Optimización e Implementación de Tecnologías Digitales en la Tesorería de las Cooperativas Financieras de la ciudad de Bogotá

**Sustentación:** miércoles 19 de agosto de 2026 · 7:00 p. m. – 7:20 p. m. · **Mi rol:** Jurado 2
**Integrante:** Eliana Vianeth Gaitán Garzón (eliana.gaitang@cun.edu.co) — **trabajo individual, una sola autora** (p. 1)
**Directora:** María Fernanda Rivera Sanclemente, Ph. D. (p. 2) — es también la moderadora de la sesión
**Línea:** Transformación Digital e Innovación Organizacional (según el cronograma de la Dirección; la portada del documento no declara línea de profundización, pp. 1-2)
**Documentos leídos:**
- `ACA 3 Proyecto Grupo 13.pdf` — **85 páginas** (pp. 77-85 son anexos escaneados sin texto seleccionable). Es la única versión del trabajo en la carpeta. Todas las citas «(p. N)» de esta ficha son de este archivo salvo que se indique «(diap. N)».
- `presentacion_G13.pdf` — **16 diapositivas**.

---

## 1. Resumen para leer en 5 minutos

**Problema.** Las cooperativas financieras de Bogotá operan la tesorería con procesos manuales, formatos físicos y plataformas desactualizadas; el documento reporta tiempos de respuesta de 5 a 8 días frente a 3 a 5 de la banca, hasta 12% de incidencias mensuales en conciliación manual y hasta 65% de la jornada del equipo financiero dedicada a tareas repetitivas (p. 15). La pregunta es cómo una estrategia de transformación digital basada en tecnologías de vanguardia puede optimizar el ecosistema de tesorería y fortalecer la gestión financiera de esas cooperativas (p. 15).

**Método.** Investigación aplicada, descriptivo-propositiva, con **estudio de caso único** en una cooperativa de ahorro y crédito de Bogotá cuya identidad se declara reservada (pp. 31, 35). El proceso se organiza en cuatro fases —planificación, actuación, observación, reflexión— (pp. 35-37) y el plan anuncia **6 participantes**: 2 directivos, 3 funcionarios de tesorería y 1 responsable de tecnología, con entrevistas semiestructuradas, observación no participante y revisión documental (pp. 33, 36). Los instrumentos efectivamente descritos son observación y **una encuesta Likert de 15 ítems en cuatro dimensiones** (pp. 39-40, 74-76).

**Resultados.** Todo el capítulo 9 se sostiene en la encuesta, con **muestra n = 10** (6 auxiliares y 4 analistas, p. 45): 100% coincide en que la carga manual genera reprocesos y retrasos (p. 50); 100% considera que el Core Financiero no está preparado para integrarse vía API o Host-to-Host (p. 52); 60% dice que los procesos de conciliación no están documentados (p. 46); 50% reconoce brechas en su propia competencia digital (p. 59). No hay resultados de entrevistas ni de observación en ninguna página del capítulo (buscado en pp. 45-68).

**Producto.** El **MACM (Middleware Autónomo de Conciliación Monetaria)**: middleware no invasivo que concilia sin tocar el Core, con arquitectura de datos por capas, modelo lógico de siete entidades, proceso ETL, seguridad y trazabilidad (pp. 63-64), y un flujo de intercambio por archivos CSV/Excel porque **no fue posible conectarse al Core** por restricciones de confidencialidad (p. 64). Se muestran un panel semáforo con 94,2% de conciliación autónoma, 12 casos por auditar y 0 riesgos (imagen, p. 62), una tabla de algoritmos de KPI (p. 67) y un plan de adopción con mentorías cruzadas y microlearning de un minuto (pp. 67-68). También propone un modelo propio, **METD-TES**, de seis fases (pp. 43-44).

**Lo que hay que preguntar.** Las limitaciones dicen que el alcance «no es de contemplar la ejecución ni prueba directa de las herramientas propuestas» (p. 19), pero el objetivo específico 3 promete un prototipo funcional validado con pruebas funcionales e indicadores (p. 16). Las conclusiones (pp. 69-70) no mencionan ni el prototipo ni las pruebas.

## 2. Coherencia título → objetivo → resultados

Título (p. 1), objetivo general (p. 16) y pregunta de investigación (p. 15) **sí dicen lo mismo**: *diseñar* una estrategia para optimizar la tesorería de las cooperativas financieras de Bogotá. El verbo «diseñar» es honesto y fija un techo bajo y alcanzable: no obliga a implementar. El problema es que los objetivos específicos **suben ese techo** —el 3 pide «desarrollar un prototipo funcional… validar su funcionamiento mediante pruebas funcionales y la evaluación de indicadores operativos» (p. 16)— y la sección de limitaciones lo vuelve a bajar (p. 19). El documento fija tres alturas distintas para el mismo trabajo. **Acreditados sin reservas: 2 de 4.**

| Objetivo específico (p. 16) | ¿Se cumplió? | Evidencia (p. N) | Qué falta |
|---|---|---|---|
| **1. Diagnosticar** el estado actual de los procesos de tesorería, actividades críticas y limitaciones | **Sí** | Encuesta de 15 ítems analizada ítem por ítem (pp. 46-61); caracterización de la muestra (p. 45); instrumento completo (pp. 74-76); **nueve páginas de encuestas diligenciadas escaneadas** (pp. 77-85) | El diagnóstico prometía entrevistas a directivos y a TI y observación directa (pp. 33, 36): no hay una sola línea de resultados de esas técnicas (pp. 45-68). Tampoco se reporta el nivel de madurez en el DMM de Gartner, que era la fase 2 del método (p. 33) y un indicador declarado (p. 33) |
| **2. Diseñar** la arquitectura funcional y el modelo de integración del MACM | **Sí** | Cinco componentes de la arquitectura de datos, modelo lógico de siete entidades, ETL, calidad, seguridad, trazabilidad y despliegue (pp. 63-64); tabla de entidades y campos (imagen, p. 63); flujo Core → CSV → motor MACM → dashboard (imagen, p. 65); justificación del escenario sin API (pp. 65-66) | Es la sección más sólida del trabajo. Falta la matriz de evaluación tecnológica que se anuncia como entregable en la p. 42: no aparece en el documento |
| **3. Desarrollar un prototipo funcional** en entorno de simulación con datos anonimizados y **validarlo con pruebas funcionales e indicadores operativos** | **No acreditado** | Lo único que existe es el panel semáforo con 94,2% / 12 casos / 0 riesgos (imagen, p. 62) y la tabla de fórmulas de KPI (imagen, p. 67) | No hay informe de pruebas (prometido en la p. 42), ni número de registros procesados, ni el archivo de datos simulados, ni repositorio, ni URL, ni una captura del sistema operando sobre esos datos. La p. 64 confirma que solo se «reprodujo el comportamiento esperado». Las conclusiones (pp. 69-70) no lo mencionan |
| **4. Diseñar** un plan de capacitación, adopción y **evaluación de usuarios** | **Parcial** | Mentorías cruzadas peer-to-peer con «líderes de adopción digital» y microlearning embebido de un minuto (pp. 67-68); diapositiva 15 con dos fases | El plan tiene dos tácticas, no un plan: sin cronograma, sin responsables, sin costos y —lo que el objetivo pide expresamente— **sin instrumento de evaluación de usuarios**. La p. 43 anuncia manual de usuario, registro de capacitación e informe de resultados como entregables: ninguno está en el documento |

## 3. Fortalezas verificables

1. **Hay trabajo de campo real y está anexado.** Nueve páginas escaneadas de encuestas diligenciadas a mano (pp. 77-85), con encabezado «Datos generales» en las pp. 77, 80 y 83. En un cohorte donde varios diagnósticos son de fuente secundaria, tener el papel firmado pesa.
2. **El diagnóstico manda sobre el diseño, y se puede rastrear.** El MACM se justifica ítem por ítem contra la encuesta: el middleware por archivos existe porque el 100% dijo que el Core no integra vía API (p. 52 → p. 61); la interfaz «zero-training» existe porque el 50% declaró brechas de competencia digital (p. 59 → pp. 61-62); las mentorías cruzadas existen porque el 40% percibió falta de programas de actualización (p. 60 → p. 67). Esa cadena es exactamente lo que la rúbrica llama coherencia metodológica.
3. **La restricción técnica está bien resuelta y bien argumentada.** Ante un Core sin API, en lugar de fingir integración se diseña una capa no invasiva por archivos estructurados con carpetas seguras, SFTP y procesos programados (pp. 65-66). Es una decisión de arquitectura defendible en una cooperativa real.
4. **La arquitectura de datos está descrita con nivel de especialización, no de folleto:** entidades, diccionario de datos con tipo, longitud, obligatoriedad y regla de validación, reglas de calidad (duplicados, nulos, integridad referencial), cifrado en tránsito y en reposo, segregación de funciones y ambientes de pruebas y producción (pp. 63-64).
5. **Reconoce el límite de gobierno del producto:** dice explícitamente que la validación de cumplimiento normativo «deberá realizarse por las áreas jurídica, de riesgos y de cumplimiento de la cooperativa» (p. 61). Es la frase de alguien que entiende el sector.
6. **Uso de IA declarado en las figuras**, no escondido: «Elaboración propia, diseño ayuda de la IA» (p. 39), «Diseño de la IA» (p. 44) y «gráfica elaboración de la IA» al pie de cada gráfica del capítulo 9 (pp. 46-60).

## 4. Debilidades y huecos (con página)

1. **El documento se contradice sobre qué se hizo.** P. 19: el alcance «no es de contemplar la ejecución ni prueba directa de las herramientas propuestas, limitándose el estudio al diseño teórico y metodológico». P. 37: «Esta fase no implica la implementación de la propuesta dentro de la organización». Pero las pp. 41-43 narran en pasado, como ejecutadas, la configuración de herramientas, la integración de bases de datos, las pruebas funcionales, la corrección de incidencias, la capacitación a los colaboradores y la medición de indicadores antes/después. Leyendo el trabajo no se puede saber qué ocurrió de verdad.
2. **El método declarado y el método aplicado son distintos.** Se anuncian entrevistas semiestructuradas a 2 directivos, 3 funcionarios de tesorería y 1 responsable de TI (p. 33), observación no participante y revisión documental (p. 36), con triangulación (p. 38). El capítulo de resultados es 100% encuesta Likert con n = 10 auxiliares y analistas (p. 45). La triangulación anunciada no se ejecutó y el nivel directivo y el de TI —los que iban a dar la visión estratégica y tecnológica— no aparecen en ningún resultado.
3. **La caracterización de la muestra no cuadra con el anexo.** La p. 45 afirma que los 10 participantes tienen antigüedad «entre 1 y 4 años» (frecuencia 10), categoría que **no existe** en el instrumento, cuyas opciones son «Menos de 1 año / 1-3 / 4-6 / Más de 6» (p. 74). Y en dos de las tres encuestas diligenciadas la casilla marcada es «Menos de 1 año» (pp. 80 y 83). Además, las áreas manuscritas son Control Operativo (p. 77), Contabilidad (p. 80) y Cartera (p. 83): ninguna es Tesorería.
4. **Del prototipo no hay evidencia, hay una maqueta.** El panel de la p. 62 muestra 94,2% de conciliación autónoma y 12 casos por auditar sin decir sobre qué conjunto de datos se obtuvieron esas cifras, cuántos registros se procesaron ni con qué criterio se consideró exitosa la conciliación. La p. 62 lo dice en futuro: «se incorporará una descripción formal de la arquitectura de datos».
5. **El anonimato declarado no se sostiene.** Las pp. 31 y 35 prometen confidencialidad institucional y anonimato, pero la p. 26 aporta la personería jurídica número 3207 del 26 de noviembre de 1957 y la Resolución 1214 del 12 de julio de 2002, y la p. 27 nombra el convenio con Finagro para la línea Agro y con el FNG para la línea de crédito Fincoeducar. Con esos tres datos la entidad es identificable. Y en la p. 83 quedó legible el nombre manuscrito de la persona que respondió la encuesta.
6. **La presentación no muestra el trabajo empírico.** En 16 diapositivas no hay ni una con los resultados de la encuesta. El diagnóstico expuesto (diap. 3 a 6) es el de fuentes secundarias: 12%, 65%, 42%, 35%, 28%, los mismos números de las pp. 14-15. La diapositiva 11 repite el plan de las 6 entrevistas que no se reportan. La diapositiva 16 se titula «RESULTADOS ESPERADOS» y muestra 25% de eficiencia, que en la p. 15 es una proyección de McKinsey, no un resultado del proyecto.
7. **La diapositiva 13 afirma un dato que el documento no tiene:** «40% — Nivel de madurez IV AUTO» en el DMM de Gartner. El documento presenta el DMM como referente aplicable (p. 23) y anuncia ubicar el nivel (p. 33), pero nunca lo asigna (buscado en pp. 45-70).
8. **Conclusiones sin cierre de dos objetivos y sin limitaciones.** Las pp. 69-70 cierran el diagnóstico, la evaluación de tecnologías y la propuesta, pero no el prototipo ni las pruebas ni la evaluación de usuarios; y no hay sección de limitaciones ni de trabajo futuro al final del documento (las limitaciones están solo en la p. 19, redactadas como anteproyecto).
9. **APA 7.ª: citas del texto que no están en la lista de referencias** (pp. 71-73): Westerman et al. 2014 (pp. 21, 29), McKinsey & Company 2020 (pp. 15, 21), Orozco & Mejía 2022 (p. 22), Gartner 2018 (p. 23), BID 2022 (p. 22), Parviainen et al. 2017 (p. 22), ISO 2018 (p. 22) y Van Horne & Wachowicz 2010 (pp. 17, 29). La lista, además, trae tres entradas que no son referencias sino notas —«Robles (2012): definición prospectiva…», «Pérez y Pérez (2016): planificación como herramienta…», «Rankia (s. f.)» sin URL— y repite Hernández/Sampieri 2014 tres veces (pp. 71-72). Se cita «Yin (2018)» en la p. 31 y «Yin (2011)» en la p. 34 para la misma obra.
10. **Restos de plantilla y de herramientas** (se anotan como dato sobre el cuidado del documento; **no se preguntan en sala**): la p. 2 dice «PROYECTO I» y la p. 1 «PROYECTO II»; la declaración de originalidad de la p. 9 dice «programa de Especialización en **Analítica de Datos**», usa «Declaramos… he escrito» en un trabajo individual y está firmada el **1 de agosto de 2025** cuando la portada dice agosto de 2026; en la p. 26 quedó incrustado el marcador **«[turn0search0]»**, que es la huella de una herramienta de búsqueda automática; la tabla de contenido sitúa las referencias en la p. 65 y están en la p. 71, y su «Lista de Imágenes» declara 3 imágenes cuando el documento tiene alrededor de treinta figuras; el modelo propio se llama «METD-TES» en la p. 43 y «MEDS TES» en la tabla de contenido (p. 6); la sigla MACM se expande como «Sistema de Automatización y Control de Tesorería» en el objetivo 2 (p. 16) y como «Middleware Autónomo de Conciliación Monetaria» en la propuesta (p. 63); el instrumento «en blanco» del anexo llega con el cargo ya diligenciado, «Analista de Cartera / cartera» (p. 74); y no hay cronograma, presupuesto ni reporte de similitud en ninguna de las 85 páginas (buscados «Turnitin», «similitud», «presupuesto», «cronograma»: solo la mención genérica de la p. 35).

## 5. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. Qué evidencia cierra el objetivo específico 3 — el prototipo y sus pruebas.**
> «Su tercer objetivo específico, en la página 16, es desarrollar un prototipo funcional del MACM en un entorno de simulación y validarlo con pruebas funcionales e indicadores. El panel de la página 62 reporta 94,2% de conciliación autónoma y 12 casos por auditar: ¿sobre cuántos registros y sobre qué archivo de datos simulados se calculó ese 94,2%, y dónde está el informe de pruebas que usted anuncia como entregable en la página 42?»

- **Por qué:** es el único objetivo que exige un producto verificable y el documento no trae informe de pruebas, ni volumen de datos, ni repositorio, ni captura del sistema procesando el archivo; la p. 64 dice que solo se «reprodujo el comportamiento esperado» y las conclusiones (pp. 69-70) no lo mencionan.
- **Qué la resuelve:** muestra el prototipo corriendo —aunque sea una hoja con macros o un script— cargando un CSV de N registros y produciendo la conciliación; da el número de registros, cuántos cuadraron y cómo se definió el 94,2%; o dice con franqueza que el panel es una maqueta de la interfaz propuesta y que la cifra es ilustrativa, y entonces el objetivo se reformula como diseño.
- **Qué la agrava:** que el 94,2% no venga de ninguna corrida y se presente como resultado; o «lo tengo en el computador de la oficina y no puedo mostrarlo».

**2. Quién respondió y cuántos: la encuesta contra el plan de entrevistas.**
> «La metodología, en la página 33, anuncia seis participantes: dos directivos, tres funcionarios de tesorería y un responsable de TI, con entrevistas semiestructuradas; los resultados de la página 45 reportan una encuesta con n igual a 10, seis auxiliares y cuatro analistas; y el anexo trae tres encuestas diligenciadas de Control Operativo, Contabilidad y Cartera. ¿Cuántas encuestas se aplicaron finalmente, a qué áreas, y qué pasó con las entrevistas a directivos y a TI?»

- **Por qué:** todo el capítulo 9 y toda la justificación del MACM se apoyan en porcentajes sobre 10 respuestas; el documento no reporta ni una línea de las entrevistas, la observación o la triangulación que anuncia (pp. 33, 36, 38), y el anexo (pp. 77-85) documenta tres formularios, no diez.
- **Qué la resuelve:** explica que el diseño migró de entrevistas a encuesta censal del equipo, sustenta las 10 respuestas —aunque solo tres se hayan escaneado— y reconoce que la metodología quedó sin actualizar. Cualquier respuesta que ordene el dato real es buena respuesta.
- **Qué la agrava:** insistir en que se hicieron las seis entrevistas sin poder decir a quién ni mostrar nada; o no distinguir entre lo que planeó y lo que aplicó.

**3. De una cooperativa a «las cooperativas financieras de Bogotá».**
> «El título y el objetivo general hablan de las cooperativas financieras de la ciudad de Bogotá, pero el diseño es un estudio de caso único en una sola cooperativa, con diez encuestas de un área. ¿Qué parte de su estrategia es transferible a otra cooperativa de Bogotá y qué parte solo funciona en la entidad que estudió?»

- **Por qué:** la p. 31 declara caso único y la p. 35 una sola unidad de análisis, mientras el título (p. 1), el objetivo (p. 16) y el resumen (p. 7) están escritos en plural sectorial. El documento afirma que los resultados «pueden ser extrapolados y adaptados a otras organizaciones con características similares» (p. 31) sin decir a cuáles ni con qué criterio.
- **Qué la resuelve:** nombra la condición que hace transferible el MACM —una cooperativa con Core sin API y conciliación manual— y reconoce que el diagnóstico es de esa entidad; o propone acotar el título al caso. Es la pregunta que le permite lucirse: sabe del sector.
- **Qué la agrava:** «sirve para todas las cooperativas del país» sin criterio; o defender la generalización con el n = 10.

### Banco de reserva

4. **El 40% de madurez de la diapositiva 13.** «Su diapositiva 13 ubica la organización en 40% de madurez, nivel IV del DMM de Gartner. El documento presenta el DMM como referente (p. 23) y anuncia ubicar el nivel (p. 33), pero no lo reporta. ¿Con qué instrumento y con qué escala llegó a ese 40%?»
5. **Alcance contra procedimiento.** «La página 19 dice que el alcance no contempla la ejecución ni la prueba directa de las herramientas, y la página 37 que no hay implementación; las páginas 41 a 43 narran en pasado la configuración, las pruebas, la capacitación y la medición de indicadores. ¿Qué de eso ocurrió realmente en la cooperativa?»
6. **Confidencialidad.** «Su metodología promete anonimato institucional (pp. 31 y 35), pero la página 26 trae la personería jurídica y la resolución de autorización, y la página 27 los convenios con Finagro y el FNG. ¿Cómo se manejó la autorización de la entidad y el consentimiento de las personas que respondieron, teniendo en cuenta que en la página 83 quedó un nombre manuscrito?»
7. **El plan del objetivo 4.** «El objetivo 4 incluye evaluación de usuarios. ¿Con qué instrumento se evaluaría la adopción, y en qué plazo, más allá de las mentorías cruzadas y el microlearning de las páginas 67 y 68?»
8. **METD-TES.** «Propone el modelo METD-TES de seis fases como aporte propio (pp. 43-44). ¿En qué se diferencia de las cuatro fases metodológicas que ya usó, y en qué parte del trabajo lo aplicó?»
9. **Viabilidad.** «No hay presupuesto ni cronograma en el documento. Si mañana la cooperativa aprueba el MACM, ¿cuánto cuesta y en cuánto tiempo se pone en producción?»

## 6. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si expone la diapositiva 16 «Resultados esperados» como si fueran resultados obtenidos** → «El 25% de eficiencia y el 60% de tiempo reasignado, ¿son medición de su prototipo o la proyección de McKinsey que cita en la página 15?»
- **Si no muestra el sistema funcionando** (ni video, ni captura, ni corrida en vivo) → pasar directo a la pregunta 1, sin preámbulo, y pedir el número de registros procesados.
- **Si muestra el sistema funcionando** → «¿Qué pasa cuando el archivo del banco trae una transacción duplicada o una fecha inválida? La página 63 dice que hay reglas de calidad: muéstreme el registro que el sistema rechaza.»
- **Si afirma que aplicó entrevistas a directivos y a TI** → «¿Cuántas, en qué fechas, y qué hallazgo del capítulo 9 sale de ellas y no de la encuesta?»
- **Si dice n = 10 en la exposición** → «El anexo trae tres formularios diligenciados (pp. 77-85). ¿Dónde están los otros siete?»
- **Si presenta el 94,2% como logro del proyecto** → pedir el denominador: cuántos movimientos, de qué periodo, de qué archivo.
- **Si declara que el MACM ya está en operación en la cooperativa** → «Entonces la limitación de la página 19 y la afirmación de la página 37 hay que corregirlas; ¿desde cuándo opera y quién lo usa hoy?»
- **Si se le acaba el tiempo y salta los resultados** → preguntar únicamente por el objetivo 3 (pregunta 1). Es el que decide la nota.
- **Si el discurso queda en generalidades sobre transformación digital** → aterrizar: «Explíqueme el paso de conciliación: llega el CSV del banco, ¿con qué campos cruza la transacción y qué tolerancia usa en valor y en fecha?» (la tabla de entidades de la p. 63 le da con qué responder).
- **Si lee las diapositivas** → dejar constancia en «claridad» y pedir que explique el diagrama de la p. 65 sin mirar la pantalla.
- **Si es la única expositora y domina el tema** → registrarlo a favor: en un trabajo individual, todo el dominio y toda la defensa recaen en ella; no hay a quién repartirle la pregunta difícil, y eso merece reconocerse.

## 7. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

**Dominio del tema.** Es su fortaleza probable: conoce la operación de tesorería cooperativa, la regulación de la Supersolidaria y el problema del Core sin API (pp. 26-30, 65-66). Para 4,6+ necesito que explique el flujo de conciliación con sus campos y sus reglas sin leer la diapositiva.

**Claridad.** La presentación es visualmente ordenada pero está construida sobre el diagnóstico de fuentes secundarias; si en 12 minutos no aparece su propia evidencia (la encuesta y el MACM corriendo), la claridad se queda en 3,6–4,0 por desbalance entre contexto y resultados.

**Coherencia del documento.** Es el criterio más débil y el que sostengo con página: alcance contra procedimiento (p. 19 vs. pp. 41-43), método declarado contra método aplicado (p. 33 vs. p. 45), caracterización de la muestra contra el anexo (p. 45 vs. pp. 74, 80, 83), objetivo 3 sin sección de resultados (p. 16 vs. pp. 61-68), y restos de plantilla en la portada y en la declaración de originalidad (pp. 2, 9). Con esto, este criterio no pasa de **3,4–3,8** por sí solo, aunque la trazabilidad diagnóstico → diseño (fortaleza 2) lo sostiene por encima del mínimo.

**Capacidad de defensa.** Aquí puede recuperar mucho. Si responde las tres preguntas reconociendo lo que quedó desactualizado en el documento y demostrando el prototipo, sube a 4,4–4,6. Si esquiva o afirma en sala cosas que el documento no soporta, baja a 3,2–3,5.

**Umbrales, en concreto:**
- **4,6 o más:** muestra el prototipo procesando datos simulados con volumen declarado **y** aclara con precisión qué se aplicó (encuesta) frente a qué se planeó (entrevistas). Sin lo primero, no hay 4,6.
- **4,0–4,4:** no hay prototipo demostrable, pero explica el diseño del MACM con dominio técnico, ordena el dato de la muestra y acota honestamente el alcance a la cooperativa estudiada.
- **3,6–4,0 (mi expectativa a priori):** defiende bien el diagnóstico y el diseño, deja sin resolver la evidencia del prototipo y las contradicciones del documento quedan en pie.
- **3,0–3,5:** sostiene en sala que implementó, capacitó y midió indicadores en la cooperativa sin poder mostrar nada de eso, o no distingue entre lo planeado y lo ejecutado.
- **Por debajo de 3,0:** solo si no puede explicar su propio instrumento ni el funcionamiento del MACM. Nada de lo leído lo anticipa.

**Distinción meritoria:** no la propondría. La coherencia documental exige antes una revisión de fondo, y una nota de 3,4 en ese criterio la bloquea de todos modos.

## 8. Observaciones administrativas (no académicas)

1. **Trabajo individual.** Una sola autora (p. 1). Es admisible —el tope es 3 estudiantes— y hay que tenerlo presente al calibrar: el volumen entregado y la carga de la sustentación son de una persona.
2. **Portada inconsistente:** p. 1 «PROYECTO II», p. 2 «PROYECTO I». Para el metodólogo.
3. **Declaración de originalidad con el programa equivocado:** dice «Especialización en Analítica de Datos» en un trabajo de la Especialización en Transformación Digital, y está fechada el 1 de agosto de **2025** (p. 9). Conviene que se corrija antes de radicar el documento final; es un dato de forma, no una falta de integridad.
4. **Sin reporte de similitud.** No hay Turnitin ni porcentaje declarado en las 85 páginas. Es requisito de la rúbrica de integridad (15%) y le corresponde al metodólogo, no al jurado.
5. **Marcador de herramienta automática en el cuerpo del texto:** «[turn0search0]» (p. 26). No se acusa nada: se reporta como resto sin depurar y se sugiere que la Dirección pida la depuración del párrafo, junto con la referencia que falta ahí.
6. **Protección de datos.** El anexo escaneado deja visible el nombre manuscrito de una persona encuestada (p. 83) y el cuerpo del documento aporta datos que identifican a la cooperativa (personería jurídica y resolución, p. 26; convenios y líneas de crédito, p. 27), en contra del anonimato declarado (pp. 31, 35). Es asunto de la Dirección con la estudiante antes de cualquier publicación o repositorio.
7. **Sin cronograma ni presupuesto.** No existen como secciones (tabla de contenido, pp. 5-6). Pesa 15% en la rúbrica del metodólogo; se registra aquí solo para que quede constancia.
8. **Para plantear al director antes de la sala:** la agenda da 20 minutos para tres evaluadores. Si la Dirección va a preguntar por el diagnóstico y el Jurado 1 por la propuesta, yo tomo el objetivo 3 (evidencia del prototipo) y la muestra, para no repetir preguntas.
