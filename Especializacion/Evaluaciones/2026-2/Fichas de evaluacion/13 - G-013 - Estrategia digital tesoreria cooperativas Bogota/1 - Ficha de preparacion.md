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

## 4. OBSERVACIONES DEL DOCUMENTO — debilidades y huecos (con página)

1. **El documento se contradice sobre qué se hizo.** P. 19: el alcance «no es de contemplar la ejecución ni prueba directa de las herramientas propuestas, limitándose el estudio al diseño teórico y metodológico». P. 37: «Esta fase no implica la implementación de la propuesta dentro de la organización». Pero las pp. 41-43 narran en pasado, como ejecutadas, la configuración de herramientas, la integración de bases de datos, las pruebas funcionales, la corrección de incidencias, la capacitación a los colaboradores y la medición de indicadores antes/después. Leyendo el trabajo no se puede saber qué ocurrió de verdad.
2. **El método declarado y el método aplicado son distintos.** Se anuncian entrevistas semiestructuradas a 2 directivos, 3 funcionarios de tesorería y 1 responsable de TI (p. 33), observación no participante y revisión documental (p. 36), con triangulación (p. 38). El capítulo de resultados es 100% encuesta Likert con n = 10 auxiliares y analistas (p. 45). La triangulación anunciada no se ejecutó y el nivel directivo y el de TI —los que iban a dar la visión estratégica y tecnológica— no aparecen en ningún resultado.
3. **La caracterización de la muestra no cuadra con el anexo.** La p. 45 afirma que los 10 participantes tienen antigüedad «entre 1 y 4 años» (frecuencia 10), categoría que **no existe** en el instrumento, cuyas opciones son «Menos de 1 año / 1-3 / 4-6 / Más de 6» (p. 74). Y en dos de las tres encuestas diligenciadas la casilla marcada es «Menos de 1 año» (pp. 80 y 83). Además, las áreas manuscritas son Control Operativo (p. 77), Contabilidad (p. 80) y Cartera (p. 83): ninguna es Tesorería.
4. **Del prototipo no hay evidencia, hay una maqueta.** El panel de la p. 62 muestra 94,2% de conciliación autónoma y 12 casos por auditar sin decir sobre qué conjunto de datos se obtuvieron esas cifras, cuántos registros se procesaron ni con qué criterio se consideró exitosa la conciliación. La p. 62 lo dice en futuro: «se incorporará una descripción formal de la arquitectura de datos».
5. **El anonimato declarado no se sostiene.** Las pp. 31 y 35 prometen confidencialidad institucional y anonimato, pero la p. 26 aporta la personería jurídica número 3207 del 26 de noviembre de 1957 y la Resolución 1214 del 12 de julio de 2002, y la p. 27 nombra el convenio con Finagro para la línea Agro y con el FNG para la línea de crédito Fincoeducar. Con esos tres datos la entidad es identificable. Y en la p. 83 quedó legible el nombre manuscrito de la persona que respondió la encuesta.
6. **Conclusiones sin cierre de dos objetivos y sin limitaciones.** Las pp. 69-70 cierran el diagnóstico, la evaluación de tecnologías y la propuesta, pero no el prototipo ni las pruebas ni la evaluación de usuarios; y no hay sección de limitaciones ni de trabajo futuro al final del documento (las limitaciones están solo en la p. 19, redactadas como anteproyecto).
7. **APA 7.ª: citas del texto que no están en la lista de referencias** (pp. 71-73): Westerman et al. 2014 (pp. 21, 29), McKinsey & Company 2020 (pp. 15, 21), Orozco & Mejía 2022 (p. 22), Gartner 2018 (p. 23), BID 2022 (p. 22), Parviainen et al. 2017 (p. 22), ISO 2018 (p. 22) y Van Horne & Wachowicz 2010 (pp. 17, 29). La lista, además, trae tres entradas que no son referencias sino notas —«Robles (2012): definición prospectiva…», «Pérez y Pérez (2016): planificación como herramienta…», «Rankia (s. f.)» sin URL— y repite Hernández/Sampieri 2014 tres veces (pp. 71-72). Se cita «Yin (2018)» en la p. 31 y «Yin (2011)» en la p. 34 para la misma obra.
8. **Restos de plantilla y de herramientas** (se anotan como dato sobre el cuidado del documento; **no se preguntan en sala**): la p. 2 dice «PROYECTO I» y la p. 1 «PROYECTO II»; la declaración de originalidad de la p. 9 dice «programa de Especialización en **Analítica de Datos**», usa «Declaramos… he escrito» en un trabajo individual y está firmada el **1 de agosto de 2025** cuando la portada dice agosto de 2026; en la p. 26 quedó incrustado el marcador **«[turn0search0]»**, que es la huella de una herramienta de búsqueda automática; la tabla de contenido sitúa las referencias en la p. 65 y están en la p. 71, y su «Lista de Imágenes» declara 3 imágenes cuando el documento tiene alrededor de treinta figuras; el modelo propio se llama «METD-TES» en la p. 43 y «MEDS TES» en la tabla de contenido (p. 6); la sigla MACM se expande como «Sistema de Automatización y Control de Tesorería» en el objetivo 2 (p. 16) y como «Middleware Autónomo de Conciliación Monetaria» en la propuesta (p. 63); el instrumento «en blanco» del anexo llega con el cargo ya diligenciado, «Analista de Cartera / cartera» (p. 74); y no hay cronograma, presupuesto ni reporte de similitud en ninguna de las 85 páginas (buscados «Turnitin», «similitud», «presupuesto», «cronograma»: solo la mención genérica de la p. 35).

## 5. OBSERVACIONES DE LAS DIAPOSITIVAS — qué proyectan y en qué se separan del documento

**Mazo:** `presentacion_G13.pdf` — **16 diapositivas**, tituladas en pantalla «PLAN ESTRATÉGICO DIGITAL» (diap. 1). Se citan **(diap. N)**; las páginas siguen siendo del trabajo de 85 páginas. Las preguntas que nacen de aquí están en la §6, en el banco de reserva, bajo **«De las diapositivas»**.

1. **El propio mazo dice «simulación» donde el documento dice «reprodujo el comportamiento esperado».** La diapositiva 9 lista como tercera meta: «Validación de Modelo — Prototipo funcional validado mediante **simulación de datos** y análisis de indicadores». Es la frase más útil de toda la presentación: sostiene la rama «cifra ilustrativa» de la pregunta 1 con su propio material. Si la leen en voz alta, la pregunta se cierra ahí mismo y sin fricción.
2. **Ninguna de las 16 diapositivas trae el trabajo empírico.** El diagnóstico proyectado (diap. 2 a 6) es el de fuentes secundarias —12 %, 65 %, 42 %, 35 %, 28 %, los mismos números de las pp. 14-15—; **no hay ni una diapositiva con la encuesta de los diez participantes** (los 100 % y 50 % de las pp. 52-59) ni con el panel del 94,2 % (p. 62). La diapositiva 16 se titula **«RESULTADOS ESPERADOS»** y muestra 25 % de eficiencia, 60 % de tiempo reasignado y 100 % de transparencia: el 25 % es la proyección de McKinsey de la p. 15, no una medición del proyecto.
3. **La diapositiva 13 afirma un dato que no está en las 85 páginas:** «40 % · NIVEL DE MADUREZ IV AUTO», DMM de Gartner. El documento presenta el DMM como referente aplicable (p. 23) y anuncia ubicar el nivel (p. 33), pero nunca lo asigna (buscado en pp. 45-70). Es el único número del mazo que no tiene origen documental.
4. **La diapositiva 11 presenta como aplicadas las seis entrevistas que ningún resultado reporta** —«Entrevistas a 2 directivos, 3 funcionarios de tesorería y 1 responsable TI, asegurando una visión estratégica, operativa y tecnológica»—, cuando el capítulo de resultados es 100 % encuesta Likert con n = 10 (p. 45). Y en la misma diapositiva dice **«CASO ESTUDIO ÚNICO»**: la respuesta a la pregunta 3 está escrita en su propio mazo, mientras el título del trabajo va en plural sectorial.
5. **La diapositiva 3 proyecta una comparación que el documento no trae:** «TIEMPOS DE RESPUESTA (DÍAS) — 5-8 cooperativas / 3-5 banca tradicional», sin fuente en pantalla y sin equivalente en el trabajo (buscado en pp. 14-15). Si la proyecta, la fuente es pregunta legítima.
6. **Lo que el mazo pone en pantalla contra el anonimato que promete el documento.** La diapositiva 14 nombra el convenio con **Finagro** y la línea **Fincoeducar** con el FNG: los mismos dos datos que en las pp. 26-27 vuelven identificable a la entidad (ítem 5 de la §4). No es reparo académico —es lo que conviene **no** leer en voz alta en una sala grabada, ni repetir yo al preguntar.
7. **El mazo se titula distinto del trabajo, y con errata:** «Optimización de flujos financieros y modernización de infraestructuras para el sector **de cooperativo** financiero» (diap. 1). No se pregunta: se anota con el resto de la forma (§9).

### Qué mirar en pantalla mientras exponen

- **Diap. 9** — si dicen «validado mediante simulación», marcarlo: es media respuesta a la pregunta 1 dada por ellos.
- **Diap. 13** — si aparece el 40 %, es el momento exacto de la pregunta de reserva del mazo.
- **Diap. 16** — si el 25 % / 60 % / 100 % se presenta como logro y no como expectativa, el condicional ya está escrito en la §7.
- **Diap. 10 y 15** — MACM y plan de adopción son **diseño**: no esperar demo. Si aparece una captura del sistema procesando un archivo, eso sí es nuevo respecto del documento: anotar cuántos movimientos muestra.
- **Lo que no va a estar:** la encuesta y el 94,2 %. Si en 12 minutos no aparece su propia evidencia, es justo el desbalance contexto/resultados que la §8 castiga en claridad.

---

## 6. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. Resultado medido o cifra ilustrativa — el 94,2 % del objetivo específico 3.**
> «La página 64 dice que se “reprodujo el comportamiento esperado”. Para el acta necesito saber cuál de las dos cosas es el 94,2 % del panel de la imagen inferior de la página 62: ¿un resultado medido sobre un archivo de movimientos, o una cifra ilustrativa de la maqueta de interfaz? Si es lo primero, cuántos movimientos traía el archivo.»

- **Sale de:** documento p. 62 (imagen **inferior**) y p. 64 · y del mazo, **diap. 9**, que llama a la validación «simulación de datos».
- **Por qué:** es el único objetivo que exige un producto verificable (p. 16) y el documento no trae informe de pruebas, ni volumen de datos, ni repositorio, ni captura del sistema procesando el archivo; las conclusiones (pp. 69-70) no lo mencionan. Plantearla como una disyuntiva de dos ramas —medición o ilustración— cierra la salida «lo trabajamos en la fase siguiente», porque las dos ramas son respuestas admisibles y solo una exige un número. **Localizador:** es la imagen **inferior** de la p. 62; la superior es la banda de fases FASE 01-04, y confundirlas en voz alta le regala el punto.
- **Qué la resuelve:** decir «medido» y dar el número de movimientos; o decir «ilustrativa» con franqueza, con lo cual el objetivo se reformula como diseño y el reconocimiento suma. Hay una comprobación aritmética a mano: si el 94,2 % y los 12 casos por auditar salen de la misma corrida, el archivo tenía del orden de 12 ÷ (1 − 0,942) ≈ 207 movimientos; si la cifra que dice se aleja mucho de ahí, conviene pedirle que la cuadre.
- **Qué la agrava:** que el 94,2 % no venga de ninguna corrida y se presente como resultado; o «lo tengo en el computador de la oficina y no puedo mostrarlo».

**2. Cuántos de los diez son de Tesorería.**
> «La página 45 caracteriza los diez encuestados y las tres encuestas escaneadas del anexo traen escritas a mano las áreas Control operativo, CONTABILIDAD y Cartera. De esos diez encuestados, ¿cuántos pertenecen al área de Tesorería? Dígame el número.»

- **Sale de:** documento p. 45 y anexos pp. 77, 80 y 83. **En el mazo no hay ninguna diapositiva de la encuesta**: nada en pantalla la respalda ni la contradice, así que hay que citar el folio.
- **Por qué:** todo el capítulo 9 y toda la justificación del MACM se apoyan en porcentajes sobre esas diez respuestas, y el trabajo es sobre la **tesorería**: si ninguno de los encuestados es de Tesorería, el diagnóstico describe otra cosa. Las tres únicas áreas verificables son las manuscritas del anexo (pp. 77, 80 y 83) y ninguna es Tesorería. Pedir un número —y solo uno— es lo que impide que la respuesta se vaya al relato del muestreo.
- **Qué la resuelve:** el número, y de dónde sale. Si es cero o uno, reconocerlo y explicar por qué el equipo de conciliación está en Contabilidad y Cartera es una respuesta sólida, no una concesión: en una cooperativa mediana la operación de tesorería la ejecutan esas áreas.
- **Qué la agrava:** responder con el n = 10 sin desagregar; o afirmar que los diez son de Tesorería cuando el anexo dice otra cosa en las tres hojas legibles.

**3. Cuántas cooperativas de Bogotá.**
> «El título de la portada y el objetivo general de la página 16 hablan de las cooperativas financieras de la ciudad de Bogotá. ¿En cuántas cooperativas de Bogotá aplicó usted el instrumento? Dígame el número.»

- **Sale de:** portada y p. 16 (plural sectorial) contra p. 31 (caso único) · y **diap. 11**, que dice «CASO ESTUDIO ÚNICO» en pantalla.
- **Por qué:** la p. 31 declara caso único y la p. 35 una sola unidad de análisis, mientras el título (p. 1), el objetivo (p. 16) y el resumen (p. 7) están escritos en plural sectorial; el documento afirma además que los resultados «pueden ser extrapolados y adaptados a otras organizaciones con características similares» (p. 31) sin decir a cuáles ni con qué criterio. La respuesta es «en una», la sabe, y decirla en voz alta es lo que abre la conversación sobre transferibilidad sin que el jurado tenga que acusar de nada. **El título está en la portada, no en la p. 16:** citarlos por separado.
- **Qué la resuelve:** decir «en una» y, sin que se lo pidan, nombrar la condición que hace transferible el MACM —una cooperativa con Core sin API y conciliación manual— o proponer acotar el título al caso. Es la pregunta que le permite lucirse: sabe del sector.
- **Qué la agrava:** «sirve para todas las cooperativas del país» sin criterio; o defender la generalización con el n = 10.

### Banco de reserva

#### Del documento

4. **El informe de pruebas.** «La página 42 anuncia un informe de pruebas como entregable del objetivo 3. ¿Dónde quedó ese informe?»
5. **La antigüedad de la muestra.** «La página 45 dice que los diez tienen antigüedad “entre 1 y 4 años”, una categoría que no existe en su propio instrumento, cuyas opciones son “Menos de 1 año / 1-3 / 4-6 / Más de 6” (p. 74); y en dos de las tres encuestas escaneadas lo marcado es “Menos de 1 año” (pp. 80 y 83). ¿De dónde sale esa categoría?» *(La encuesta con «1-3 años» no contradice nada: la pinza son las dos de «Menos de 1 año».)*
7. **Alcance contra procedimiento.** «La página 19 dice que el alcance no contempla la ejecución ni la prueba directa de las herramientas, y la página 37 que no hay implementación; las páginas 41 a 43 narran en pasado la configuración, las pruebas, la capacitación y la medición de indicadores. ¿Qué de eso ocurrió realmente en la cooperativa?»
8. **Confidencialidad.** «Su metodología promete anonimato institucional (pp. 31 y 35), pero la página 26 trae la personería jurídica y la resolución de autorización, y la página 27 los convenios con Finagro y el FNG. ¿Cómo se manejó la autorización de la entidad y el consentimiento de las personas que respondieron, teniendo en cuenta que en la página 83 quedó un nombre manuscrito?»
9. **El plan del objetivo 4.** «El objetivo 4 incluye evaluación de usuarios. ¿Con qué instrumento se evaluaría la adopción, y en qué plazo, más allá de las mentorías cruzadas y el microlearning de las páginas 67 y 68?»
10. **METD-TES.** «Propone el modelo METD-TES de seis fases como aporte propio (pp. 43-44). ¿En qué se diferencia de las cuatro fases metodológicas que ya usó, y en qué parte del trabajo lo aplicó?»
11. **Viabilidad.** «No hay presupuesto ni cronograma en el documento. Si mañana la cooperativa aprueba el MACM, ¿cuánto cuesta y en cuánto tiempo se pone en producción?»

#### De las diapositivas

Estas tres solo se hacen **si la diapositiva sale en pantalla**. Los números de reserva no se reordenaron —la hoja de respuestas los cita— así que van fuera de secuencia a propósito.

6. **El 40 % de madurez de la diapositiva 13.** «Su diapositiva 13 ubica la organización en 40% de madurez, nivel IV del DMM de Gartner. El documento presenta el DMM como referente (p. 23) y anuncia ubicar el nivel (p. 33), pero no lo reporta. ¿Con qué instrumento y con qué escala llegó a ese 40 %?»
6-bis. **Los 5-8 días de la diapositiva 3.** «Su diapositiva 3 compara los tiempos de respuesta de las cooperativas, 5 a 8 días, con los de la banca tradicional, 3 a 5. ¿De dónde salen esas dos cifras?» *(No están en el documento; buscado en pp. 14-15.)*
6-ter. **Las seis entrevistas de la diapositiva 11.** «Su diapositiva 11 presenta entrevistas a dos directivos, tres funcionarios de tesorería y un responsable de TI. ¿Se realizaron esas seis entrevistas y dónde quedaron sus resultados?» *(El capítulo de resultados es solo la encuesta de diez, p. 45. Es la versión suave del hueco: se pregunta por el paradero, no por la omisión.)*

## 7. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si expone la diapositiva 16 «Resultados esperados» como si fueran resultados obtenidos** → «El 25% de eficiencia y el 60% de tiempo reasignado, ¿son medición de su prototipo o la proyección de McKinsey que cita en la página 15?»
- **Si no muestra el sistema funcionando** (ni video, ni captura, ni corrida en vivo) → pasar directo a la pregunta 1, sin preámbulo, y pedir el número de movimientos del archivo.
- **Si contesta «ilustrativa» en la pregunta 1** → no insistir: es la respuesta honesta y sube. Pasar a la reserva 4, el informe de pruebas anunciado en la p. 42, solo si sobra tiempo.
- **Si muestra el sistema funcionando** → «¿Qué pasa cuando el archivo del banco trae una transacción duplicada o una fecha inválida? La página 63 dice que hay reglas de calidad: muéstreme el registro que el sistema rechaza.»
- **Si afirma que aplicó entrevistas a directivos y a TI** → «¿Cuántas, en qué fechas, y qué hallazgo del capítulo 9 sale de ellas y no de la encuesta?»
- **Si dice n = 10 en la exposición** → «El anexo trae tres formularios diligenciados (pp. 77-85). ¿Dónde están los otros siete?»
- **Si presenta el 94,2% como logro del proyecto** → pedir el denominador: cuántos movimientos, de qué periodo, de qué archivo. Si da una cifra, cuadrarla contra los 12 casos por auditar: 12 ÷ (1 − 0,942) ≈ 207 movimientos.
- **Si dice que los diez encuestados son de Tesorería** → «en las tres encuestas escaneadas que se pueden leer, las áreas manuscritas son Control operativo, Contabilidad y Cartera: ¿de dónde sale la clasificación de la página 45?».
- **Si contesta «en una» a la pregunta 3** → dejarla lucirse: «nómbreme las tres condiciones que otra cooperativa de Bogotá tendría que cumplir para que el MACM le sirva tal como está».
- **Si declara que el MACM ya está en operación en la cooperativa** → «Entonces la limitación de la página 19 y la afirmación de la página 37 hay que corregirlas; ¿desde cuándo opera y quién lo usa hoy?»
- **Si se le acaba el tiempo y salta los resultados** → preguntar únicamente por el objetivo 3 (pregunta 1). Es el que decide la nota.
- **Si el discurso queda en generalidades sobre transformación digital** → aterrizar: «Explíqueme el paso de conciliación: llega el CSV del banco, ¿con qué campos cruza la transacción y qué tolerancia usa en valor y en fecha?» (la tabla de entidades de la p. 63 le da con qué responder).
- **Si lee las diapositivas** → dejar constancia en «claridad» y pedir que explique el diagrama de la p. 65 sin mirar la pantalla.
- **Si expone sin equipo y domina el tema** → registrarlo a favor: en un trabajo individual, todo el dominio y toda la defensa recaen en una sola persona; no hay a quién repartirle la pregunta difícil, y eso merece reconocerse.

## 8. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

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

### 8.1 Formulario oficial del jurado — 5 criterios en escala 1–5

> **Instrumento distinto de los cuatro criterios de arriba.** Son las cinco preguntas del formulario que la Dirección le pide al jurado, cada una con opciones **1 2 3 4 5**. **Ninguna califica la sustentación oral:** las cinco se responden con el documento, así que van precargadas con la página que las sostiene y en sala solo se confirman.
>
> Lectura de la escala, fijada de antemano: **5** sobresaliente, sin reparos de fondo · **4** sólido, con reparos menores y declarados · **3** aceptable, con un reparo de fondo que el documento no resuelve · **2** deficiente: hay material, pero se contradice o no sostiene lo que afirma · **1** sin base verificable en el documento.
>
> ⚠️ **Este 1–5 no es la nota del acta.** La nota que se reporta sale de los cuatro criterios y de los umbrales de esta §8. La casilla del formulario la marca el jurado humano; esto es una propuesta con página.

**1. Planteamiento de la problemática y formulación de objetivos** — propuesto **3** / 5

> Claridad, pertinencia y delimitación del problema de investigación, así como la coherencia y precisión de los objetivos propuestos, verificando su alineación con el propósito del estudio y su viabilidad investigativa.

Título (p. 1), objetivo general (p. 16) y pregunta (p. 15) sí dicen lo mismo, y el verbo **«diseñar»** fija un techo honesto y alcanzable. El reparo de fondo es que el documento fija **tres alturas distintas para el mismo trabajo**: el objetivo específico 3 promete un prototipo funcional validado con pruebas e indicadores (p. 16), las limitaciones dicen que el alcance «no contempla la ejecución ni prueba directa de las herramientas» (p. 19) y la p. 37 que no hay implementación. A eso se suma que el título habla en plural sectorial —las cooperativas de Bogotá— sobre un estudio de caso único (pp. 31, 35).

**2. Marco teórico y referentes conceptuales** — propuesto **2** / 5

> Solidez del sustento teórico del proyecto, la pertinencia y actualidad de las fuentes consultadas, y la capacidad de articular conceptos, enfoques y antecedentes que fundamenten adecuadamente la investigación.

El referente de sector es correcto (regulación de la Supersolidaria, pp. 26-30) y el DMM de Gartner se presenta como marco aplicable (p. 23). Pero la lista de referencias (pp. 71-73) no sostiene el cuerpo: **ocho citas del texto no están en la lista** —Westerman et al. 2014, McKinsey 2020, Orozco & Mejía 2022, Gartner 2018, BID 2022, Parviainen et al. 2017, ISO 2018, Van Horne & Wachowicz 2010—, tres «referencias» son notas y no referencias, Hernández/Sampieri 2014 se repite tres veces y la misma obra de Yin se cita como 2018 (p. 31) y como 2011 (p. 34).

**3. Metodología, muestra y coherencia del diseño** — propuesto **2** / 5

> Correspondencia entre el enfoque metodológico, el tipo de estudio, las técnicas e instrumentos de recolección de información y la definición de la muestra, garantizando la coherencia interna del diseño investigativo.

Hay trabajo de campo real y anexado —instrumento completo (pp. 74-76) y nueve páginas de encuestas diligenciadas a mano (pp. 77-85)—, lo que en este cohorte pesa. Pero el método declarado y el aplicado son distintos y no se puede reconstruir cuál rigió: se anuncian **seis participantes con entrevistas semiestructuradas** —dos directivos, tres de tesorería, uno de TI—, observación no participante y triangulación (pp. 33, 36, 38), y el capítulo de resultados es **100 % encuesta Likert con n = 10** (p. 45), sin una línea de entrevistas ni de observación. La caracterización tampoco cuadra con el anexo: la p. 45 dice antigüedad «entre 1 y 4 años», una categoría **que no existe en el instrumento** (p. 74), y en dos de las tres encuestas escaneadas lo marcado es «Menos de 1 año» (pp. 80, 83); las áreas manuscritas son Control Operativo, Contabilidad y Cartera —**ninguna es Tesorería**—.

**4. Resultados y conclusiones** — propuesto **2** / 5

> Calidad en la presentación, interpretación y análisis de los resultados obtenidos, así como la consistencia y pertinencia de las conclusiones en relación con los objetivos, la problemática y el marco teórico del estudio.

El análisis del diagnóstico está hecho ítem por ítem y **la trazabilidad diagnóstico → diseño se puede rastrear**: el middleware por archivos existe porque el 100 % dijo que el Core no integra por API (p. 52 → p. 61), la interfaz «zero-training» porque el 50 % declaró brechas digitales (p. 59 → pp. 61-62). Lo que impide más de 2: del **objetivo 3 no hay resultado** —solo un panel semáforo con 94,2 %, 12 casos y 0 riesgos (p. 62) sin decir sobre cuántos registros ni qué archivo, y la p. 64 admite que solo se «reprodujo el comportamiento esperado»—; las **conclusiones (pp. 69-70) no cierran ni el prototipo, ni las pruebas, ni la evaluación de usuarios**, y no hay sección de limitaciones al final; la diapositiva 13 afirma un 40 % de madurez nivel IV del DMM que no está en ninguna de las 85 páginas; y la diapositiva 16 titula «resultados esperados» una proyección de McKinsey (p. 15).

**5. Pertinencia disciplinar y articulación con la especialización** — propuesto **4** / 5

> Grado de alineación del proyecto con el campo disciplinar y los énfasis de la especialización cursada, así como su aporte potencial al desarrollo académico, profesional o investigativo del área.

Tesorería cooperativa con middleware de conciliación no invasivo, arquitectura de datos por capas, modelo lógico de siete entidades, ETL, seguridad y trazabilidad (pp. 63-64): encaja de lleno en «Transformación Digital e Innovación Organizacional», y la solución al Core sin API por archivos estructurados con SFTP es una decisión defendible en una cooperativa real (pp. 65-66). Suma que reconozca el límite de gobierno —la validación normativa corresponde a jurídica, riesgos y cumplimiento (p. 61)—. No llega a 5 porque el producto no pasó de la maqueta.

**Suma propuesta: 13 / 25.**

**Qué subiría una casilla en sala:** El **criterio 4 pasa a 3** si muestra el prototipo procesando un archivo con número de registros declarado, o si dice con franqueza que el panel es una maqueta y el 94,2 % es ilustrativo (pregunta prioritaria 1) — reconocerlo sube, no baja. El **criterio 3 pasa a 3** si ordena el dato de la muestra: cuántas encuestas, a qué áreas y qué pasó con las entrevistas (pregunta 2). El **criterio 1 pasa a 4** si acota honestamente el alcance a la cooperativa estudiada y nombra la condición que hace transferible el MACM (pregunta 3).

**Qué la bajaría:** El **criterio 4 baja a 1** si presenta el 94,2 % o el 25 % de McKinsey como medición de su prototipo. El **criterio 1 baja a 2** si sostiene que implementó, capacitó y midió indicadores en la cooperativa sin poder mostrar nada. Es trabajo individual y cierra la jornada: todo el dominio y toda la defensa recaen en una persona, y eso se reconoce a favor.

## 9. Observaciones administrativas (no académicas)

1. **Trabajo individual.** Una sola autora (p. 1). Es admisible —el tope es 3 estudiantes— y hay que tenerlo presente al calibrar: el volumen entregado y la carga de la sustentación son de una persona.
2. **Portada inconsistente:** p. 1 «PROYECTO II», p. 2 «PROYECTO I». Para el metodólogo.
3. **Declaración de originalidad con el programa equivocado:** dice «Especialización en Analítica de Datos» en un trabajo de la Especialización en Transformación Digital, y está fechada el 1 de agosto de **2025** (p. 9). Conviene que se corrija antes de radicar el documento final; es un dato de forma, no una falta de integridad.
4. **Sin reporte de similitud.** No hay Turnitin ni porcentaje declarado en las 85 páginas. Es requisito de la rúbrica de integridad (15%) y le corresponde al metodólogo, no al jurado.
5. **Marcador de herramienta automática en el cuerpo del texto:** «[turn0search0]» (p. 26). No se acusa nada: se reporta como resto sin depurar y se sugiere que la Dirección pida la depuración del párrafo, junto con la referencia que falta ahí.
6. **Protección de datos.** El anexo escaneado deja visible el nombre manuscrito de una persona encuestada (p. 83) y el cuerpo del documento aporta datos que identifican a la cooperativa (personería jurídica y resolución, p. 26; convenios y líneas de crédito, p. 27), en contra del anonimato declarado (pp. 31, 35). Es asunto de la Dirección con la estudiante antes de cualquier publicación o repositorio.
7. **Sin cronograma ni presupuesto.** No existen como secciones (tabla de contenido, pp. 5-6). Pesa 15% en la rúbrica del metodólogo; se registra aquí solo para que quede constancia.
8. **Para plantear al director antes de la sala:** la agenda da 20 minutos para tres evaluadores. Si la Dirección va a preguntar por el diagnóstico y el Jurado 1 por la propuesta, yo tomo el objetivo 3 (evidencia del prototipo) y la muestra, para no repetir preguntas.
