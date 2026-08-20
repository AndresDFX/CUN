# 26ET2-G-003 — Análisis y modernización del archivo municipal de la Secretaría de Gobierno de San Francisco, Putumayo, para mejorar la eficiencia documental en la vigencia 2024

**Sustentación:** martes 18 de agosto de 2026 · 6:40 p. m. – 7:00 p. m. · **Mi rol:** Jurado 2
**Integrantes:** José Javier Galvis Noguera (jose.galvisn@cun.edu.co), Eliana Naranjo Cortés (correo cruzado en el cronograma, ver §9), Cristian David Forero Álvarez (correo cruzado en el cronograma, ver §9), Gloria Nahtaly Florez Susa (gloria.florezs@cun.edu.co)
**Línea:** Gestión y Tecnología
**Directora / moderadora:** María Fernanda Rivera Sanclemente · **Jurado 1:** Hayder Alejandro Romero Sierra
**Documentos leídos:** `ACA_No_3_Proyecto_Final_VF.pdf` (169 páginas — única versión en la carpeta del grupo) y `presentación - Proyecto 2.pptx` (10 diapositivas)

---

## 1. Resumen para leer en 5 minutos

El proyecto interviene el archivo de la Secretaría de Gobierno de San Francisco (Putumayo). El objeto de estudio es el fondo documental de la vigencia fiscal **2024**, mientras que el desarrollo técnico y la redacción se ejecutaron en **2026** (p. 14) — el propio documento advierte ese desfase.

**Problema.** Gestión documental manual, sin inventario formal, sin SGDEA, con deterioro por humedad y sin trazabilidad; tiempos de localización de un expediente **entre 45 y 90 minutos** (p. 79, Tabla 3 —la cifra **no** está en las pp. 17-18, que solo hablan de «demoras recurrentes»—; se repite en pp. 85 y 92).

**Método.** Enfoque mixto declarado (p. 71), bajo modelo de investigación-acción (p. 23: la p. 71 no usa esa expresión). Instrumentos: FUID regulado por el Acuerdo 042 de 2002 y adaptado con corte a 2024 (p. 77), **matriz de diagnóstico de 20 aspectos en 6 dimensiones** calificados de 1 a 5 (p. 72), y **4 encuestas/entrevistas semiestructuradas** a funcionarios, aplicadas el 24 de junio de 2026 (pp. 72, 76-79, 141, 167). Se declara consentimiento informado (Ley 1581 de 2012) para entrevistas y fotografías (p. 72).

**Resultado del diagnóstico (objetivo 1).** Promedio general **1,9/5**: 9 ítems críticos, 8 deficientes, 1 aceptable y 2 en cumplimiento; el 85 % exige intervención (p. 81). Por dimensión: trazabilidad y seguridad 1,33; tecnología y cumplimiento normativo 1,67; organización 1,75; conservación física 3,25, la única sobre el umbral (p. 82). El FUID se aplicó **sobre una muestra, no censal**, y corresponde al «diseño y aplicación piloto del instrumento» (pp. 78, 86, 130).

**Producto (objetivos 2 y 3).** Prototipo **SGDEA**: Flask 3.0.3 + PostgreSQL 16 en dos contenedores Docker, ejecutado en el **portátil personal de un integrante**, consumido en `http://localhost:5000` (pp. 89-91). Diseño archivístico serio: DCF de tres niveles, DRS por serie, modelo entidad-relación de 14 entidades y modelo lógico con PK/FK y restricciones (pp. 88, 97-100). Seguridad: RBAC con **6 perfiles** y matriz de permisos (pp. 93-94), auditoría append-only (pp. 100 y 109; el término no aparece en las pp. 93-94).

**Honestidad del alcance.** La **Tabla 14 (pp. 104-105)** clasifica cada capacidad en implementado / representado en el prototipo / diseñado / proyectado: *implementado y probado* → Flask-PostgreSQL, radicación con consecutivo (SGDEA-2026-000128), búsqueda con filtros, clasificación TRD, RBAC de 6 perfiles y persistencia por volumen; *solo representado* → cifrado AES-256 (Restic), hash SHA-256, OCR (Tesseract) y MinIO; *proyectado* → TLS, MFA, pruebas de usabilidad y seguridad e **implementación institucional**. Seis casos de prueba CP-01 a CP-06, todos «aprobados», uno con observación (pp. 109-110).

**Lo proyectado, no medido.** Reducción de tiempos a <5 minutos, metas de la tabla de impacto y la mejora por dimensión son **proyecciones**, y el documento lo dice (pp. 24, 92, 113-114). Cierra con 28 semanas de cronograma de implementación (p. 96), conclusiones (pp. 133-134) y recomendaciones por dimensión (pp. 135-136).

---

## 2. Coherencia título → objetivo → resultados

**Título** («análisis y modernización… para mejorar la eficiencia documental») y **objetivo general** («**Modernizar** el archivo municipal… en 2024», p. 20) prometen un verbo de implementación. Lo que existe y está evidenciado es un **diagnóstico + un prototipo verificado en laboratorio**, con la implementación institucional explícitamente aplazada (p. 105). El techo real del trabajo es *diagnosticar y diseñar/prototipar*, no *modernizar*. La pregunta de investigación (p. 19) pregunta «cómo la implementación… moderniza… y mejora la eficiencia», algo que el propio documento no responde con datos, sino con proyecciones (pp. 92, 113).

| Objetivo específico (p. 20) | ¿Se cumplió? | Evidencia (p.) | Qué falta |
|---|---|---|---|
| 1. Gestionar el archivo mediante diagnóstico e **inventario** de 2024 según AGN | **Sí, en la parte de diagnóstico; parcial en inventario** | Matriz de 20 aspectos y promedio 1,9/5 (pp. 79-84); FUID adaptado (pp. 77-78); autoevaluación de cumplimiento (p. 86) | El inventario **no es censal** y **nunca se cuantifica**: no hay número de expedientes, folios ni metros lineales (pp. 78, 86, 130). La Tabla 2 muestra los *campos* del FUID, no datos |
| 2. Desarrollar plataforma piloto con DCF y DRS | **Sí, como prueba de concepto** | Arquitectura (p. 87), DCF/DRS (p. 88), figuras C-1 a C-7 del prototipo (pp. 106-109), CP-01 a CP-04 (pp. 109-110) | Corre en equipo personal, no en la entidad (pp. 89-91); OCR y MinIO solo «representados» (p. 105); alertas del DRS y control de versiones **diseñados, no implementados** (p. 105) |
| 3. Establecer requisitos de seguridad y acceso, perfiles y protocolos | **Sí en diseño; parcial en implementación** | RBAC de 6 perfiles y matriz (pp. 93-94), protocolos (Tabla 6, p. 94), CP-05 y CP-06 (p. 110) | Cifrado AES-256 y hash SHA-256 **representados, no integrados** (p. 105); auditoría «Implementado (parcial)… falta IP y resultado» (p. 104, no la 105); MFA proyectado |
| 4. **Verificar** el funcionamiento «en un entorno institucional controlado» frente a la normativa | **No en el entorno institucional** | Se declara cumplido en entorno de simulación Docker (p. 132); pruebas de persistencia (pp. 120-121) | La verificación fue en laboratorio local; «pruebas de usabilidad y de seguridad: **pendientes de ejecución**» e «implementación institucional: **proyectada**» (p. 105). El apartado de verificación institucional está redactado en futuro (p. 112) |

**Nudo de la incoherencia:** el capítulo de alcance afirma en pasado hechos que el resto del documento desmiente. P. 27: «Se **desplegó** la aplicación de prueba de forma piloto en la Secretaría de Gobierno», «Se **digitalizaron** selectivamente documentos prioritarios» y (p. 27-28) «Se **realizaron** sesiones de capacitación». No hay evidencia de ninguna de las tres: la implementación institucional está proyectada (p. 105), no se reporta ni una página digitalizada frente a la meta de «al menos 200 páginas» (p. 24) y las entrevistas preguntan a los funcionarios si *estarían dispuestos a recibir capacitación* (pp. 146, 153, 160 y 166), lo que sitúa la capacitación después del trabajo de campo.

---

## 3. Fortalezas verificables

1. **La Tabla 14 (pp. 104-105) es lo mejor del trabajo.** Clasificar cada funcionalidad en implementado / representado / diseñado / proyectado, y decir explícitamente «para no atribuir a la solución funciones que aún no operan en producción» (p. 104), es una honestidad técnica poco común en este nivel. Vale la pena reconocérselo en voz alta.
2. **Diagnóstico con línea base defendible.** 20 aspectos, 6 dimensiones, escala 1-5, promedios por dimensión y tres gráficas de lectura distinta (barras, distribución y radar) (pp. 79-85). El 1,9/5 se puede rastrear ítem por ítem hasta la Tabla 3.
3. **Diseño archivístico bien anclado.** El DCF traduce el CCD y el DRS automatiza la TRD, con la decisión de eliminación reservada al humano (p. 88); los principios archivísticos se mapean uno a uno contra la plataforma (Tabla 4, p. 89).
4. **Ingeniería de datos por encima del promedio.** Modelo E-R de 14 entidades en 4 dominios, tablas puente para las relaciones muchos-a-muchos del RBAC, modelo lógico con tipos, UNIQUE, NOT NULL y reglas ON DELETE/ON UPDATE, y auditoría append-only (pp. 97-100, 109).
5. **Prueba de resiliencia real.** `docker compose down` / `up` con persistencia por volumen `db_data` verificada (CP-01, p. 109; pp. 120-121). Es una prueba pequeña, pero es una prueba, no una promesa.
6. **Decisión de infraestructura justificada por contexto.** Simulación local con recursos modestos como paso previo a la nube MinTIC, con la conectividad del municipio como argumento (pp. 89-90, 128-130, 135).
7. **Consideración de datos personales.** Consentimiento informado para entrevistas y fotografías, y uso académico declarado (p. 72).

---

## 4. OBSERVACIONES DEL DOCUMENTO — debilidades y huecos (con página)

1. **El verbo del objetivo general excede el producto.** «Modernizar… en 2024» frente a un prototipo no desplegado (pp. 20, 105). No es un problema de esfuerzo, es de formulación: el trabajo entrega diagnóstico y diseño/prototipo.
2. **Afirmaciones en pasado sin respaldo** (p. 27): despliegue piloto en la entidad, digitalización de documentos prioritarios y sesiones de capacitación. Ninguna tiene evidencia y las tres se contradicen con la p. 105 y con las entrevistas (pp. 146, 153, 160 y 166).
3. **La muestra nunca se cuantifica.** «Muestra representativa» literal en pp. 78, 86 y 130 —y «la muestra documental fue representativa» en la p. 71— sin número de expedientes, folios ni metros lineales, y sin criterio de selección. Las cadenas «metros lineales» y «folio» aparecen **una sola vez** en las 169 páginas: en la p. 71, como lo que el enfoque cuantitativo «requiere medir». Con el alcance de estudio de caso una muestra pequeña es perfectamente aceptable; lo que no es aceptable es no decir cuál fue. Lo que el mazo proyecta en su lugar —«muestra de tipo censal»— está en la §5 (punto 3).
4. **El enfoque mixto queda a medias.** La p. 71 justifica lo cuantitativo por «cuantificar tiempos exactos de respuesta **antes y después** de la implementación»; no hay medición posterior: todos los valores de mejora son metas o proyecciones (pp. 24, 92, 113-114).
5. **Quién calificó la matriz no está claro.** La p. 72 dice que la calificación «fue asignada por el equipo investigador a partir de la observación directa»; la Tabla 3 se titula «Calificación de resultados de **la encuesta** diagnóstica» y su nota dice «se realizó una calificación de cada una de las preguntas realizadas en la encuesta» (pp. 79-80). Como el 1,9/5 es la base empírica de todo el trabajo, la ambigüedad pesa.
6. **La misma matriz se describe con 3 dimensiones (p. 72) y con 6 (p. 79).** El mazo toma partido por la versión de 6 (§5, punto 11).
7. **Dato del parque tecnológico contradictorio:** Tabla 3, «Recursos tecnológicos: 3 — Dos computadores disponibles» (p. 80) frente a «según el diagnóstico del ACA 1: ocho equipos de escritorio con Windows» (p. 90).
8. **Restos de plantilla y evidencias vacías en el protocolo de pruebas.** CP-01 dice en el campo Evidencia: «**Insertar aquí la captura correspondiente**»; CP-02, CP-03, CP-04 y CP-06 tienen el campo Evidencia en blanco (pp. 109-110).
9. **Bibliografía con marcadores «por verificar» sobre fuentes que sí se citan en el cuerpo.** «Zapata, C. A., & Castrillón. (2020). [Título… por verificar]. [Datos de publicación por verificar]» (p. 140), citada como respaldo en pp. 15, 18 y 42; y «DANE (2024). [Título del informe estadístico — por verificar]» (p. 138), citada en pp. 14, 17, 18, 21 y 22. La entrada de Jaramillo Sánchez (2024) queda truncada sin datos de publicación (p. 139).
10. **Citas del texto sin entrada en la bibliografía:** «Contraloría General de la República, 2024» (pp. 14, 17, 18, 21), «AGN, 2024» y «MinTIC, 2024» no aparecen en la lista de referencias (pp. 137-140); además el texto cita «CCSDS, 2012» (p. 67) y la lista registra CCSDS 2024 (p. 138), y la misma obra PREMIS (Data Dictionary 3.0) queda duplicada en dos entradas —«Library of Congress. (2015)» y «PREMIS Editorial Committee. (2015)»— (pp. 139-140). *No* se les puede reprochar ISO 27001: las dos entradas de la p. 139 son ediciones distintas de la norma (2013 y 2022), lo cual es legítimo.
11. **No hay apartado de limitaciones del estudio.** La sección 5 **del documento** se titula «Alcances y Limitaciones» pero solo contiene alcance y delimitaciones (pp. 23-32). Faltan las limitaciones de los resultados (una sola dependencia, 4 informantes, prototipo en laboratorio, ausencia de medición post).
12. **La delimitación institucional se contradice:** dentro de «No incluye» aparece «Archivo municipal correspondiente al término 2024» (p. 29), que es justamente el objeto del proyecto.
13. **No se declara similitud (Turnitin) ni uso de herramientas de IA generativa;** tampoco hay presupuesto ni costeo del despliegue, pese a las 28 semanas de cronograma (p. 96) y a las recomendaciones de nube y deshumidificación (pp. 135-136).
14. **Conclusiones más fuertes que la evidencia:** «la integración de registros de auditoría inmutables y el diseño de cifrado AES-256 resolvieron la obligación de trazabilidad y confidencialidad… **blindando jurídicamente** a la Secretaría» (p. 134), cuando el cifrado no está integrado (p. 105) y la auditoría es parcial (p. 104). Las diapositivas 7 y 10 repiten la afirmación y la endurecen: §5, puntos 1 y 2.
15. **Redacción del planteamiento con citas incrustadas como frases sueltas** (pp. 15, 17, 18, 21-22): párrafos que terminan en un listado de autores y años sin verbo, y referencias completas insertadas dentro del cuerpo del texto (p. 15, p. 19).

---

## 5. OBSERVACIONES DE LAS DIAPOSITIVAS — qué proyectan y en qué se separan del documento

**Mazo:** `presentación - Proyecto 2.pptx` — **10 diapositivas** (1 portada · 2 problema y pregunta · 3 objetivos · 4 metodología y muestra · 5 fases · 6 diagnóstico por dimensiones · 7 propuesta de solución · 8 impacto proyectado · 9 el video del prototipo · 10 conclusiones)

Diez diapositivas contra 169 páginas, y el saldo es el inverso al de los demás grupos de la jornada: **el mazo no proyecta lo mejor que tiene el trabajo y sí proyecta lo único que el documento se cuidó de no afirmar.** La Tabla 14 —la que separa implementado, representado, diseñado y proyectado— no aparece en ninguna diapositiva; el cifrado operando, que esa misma tabla niega, aparece en dos. El documento se corrige a sí mismo y el mazo lo deshace.

1. **«Cifrado de grado militar (AES-256)» (diapositiva 7) es una frase que no existe en las 169 páginas.** Busqué «grado militar» en el documento completo: cero apariciones. Y la diapositiva 10 la sube de nivel al pasarla a pasado verificado: «se verificó… integridad con cifrado AES-256». La Tabla 14 (p. 105) lo deja en «representado en prototipo — integración real proyectada». Es la contradicción más citable entre los dos entregables y es la pregunta prioritaria 1.
2. **La diapositiva 10 mete tres afirmaciones en una sola frase y solo la primera se sostiene entera.** «Se verificó el Control de Acceso (RBAC) con 6 perfiles definidos, trazabilidad de auditoría e integridad con cifrado AES-256»: los 6 perfiles sí están (p. 94, aunque las pp. 26 y 30 digan tres → reserva 4); la auditoría está «Implementado (parcial)… falta IP y resultado» (p. 104); el cifrado está solo representado (p. 105). Conviene desarmarla afirmación por afirmación y no en bloque: reconocer que la primera es verdadera da autoridad para las otras dos.
3. **«Muestra de tipo censal» (diapositiva 4)**, exactamente lo contrario de lo que el documento afirma tres veces (pp. 78, 86 y 130). La línea, además, se contradice sola: «Acervo documental total de la vigencia 2024. Muestra de tipo censal y muestra poblacional de 4 funcionarios clave» —censo y muestra en el mismo renglón—. Es el punto de entrada de la pregunta 3.
4. **El mazo pierde el mejor dato del diagnóstico.** La diapositiva 2 resume el problema en «Los tiempos de búsqueda son muy largos» y **no proyecta la línea base de 45 a 90 minutos** que el documento repite tres veces (Tabla 3, p. 79; pp. 85 y 92). Sin esa cifra en pantalla, el «más del 50 %» de la diapositiva 8 se queda sin referencia visible: quien solo vea el mazo no sabe 50 % de qué.
5. **La diapositiva 6 es fiel a la p. 82, y lo verifiqué valor por valor.** Organización 1.8, Conservación Física 3.25 «Aceptable», Trazabilidad 1.33, Tecnología 1.67, Seguridad de la Información 1.33 y Cumplimiento Normativo 1.67; el 85 % de brechas y el reparto 9 / 8 / 1 / 2 coinciden con la p. 81. **Aquí no hay hallazgo que perseguir**, y conviene saberlo para no gastar turno: la tabla del mazo está bien. Dos lunares de forma, que van al bloque de ortografía y no a la sala: proyecta 1.8 donde la p. 82 calcula 1,75, y rotula el mismo 1.67 como «Crítico» en tecnología y como «Deficiente» en cumplimiento normativo.
6. **La diapositiva 2 se contradice con la 6 en el titular.** Encabeza el problema con «Deterioro Físico Crítico», mientras su propia diapositiva 6 pone conservación física en 3.25 «Aceptable» —la única dimensión sobre el umbral—. El titular sí tiene respaldo, pero de un solo ítem: «Condiciones ambientales: 1 — Crítico» (Tabla 3, p. 80). Es el mismo nudo de la reserva 9 —la deshumidificación justificada con un 1/5 que la p. 82 no sostiene—, ahora también en pantalla.
7. **La diapositiva 8 es honesta en el adjetivo y se pasa en el sustantivo.** «Reducción **proyectada** de más del 50 %» dice «proyectada», que es exactamente lo que corresponde (pp. 92, 113-114); pero introduce una **tercera** meta para el mismo indicador, junto al «≥ 40 %» de la p. 24 y el «menos de cinco minutos» de la p. 92 (reserva 6). En la misma diapositiva, «Trazabilidad total» no tiene con qué sostenerse: la auditoría está parcial (p. 104).
8. **La diapositiva 5 es más prudente que la 3, justo donde el trabajo falla.** La 3 copia los objetivos textuales de la p. 20, con el OE4 «en un entorno institucional controlado»; la 5 describe la Fase 4 como «Pruebas en entorno controlado», sin «institucional». La versión de la 5 es la que corresponde a lo que se hizo. Si en sala usan la fórmula de la 5, es una concesión y hay que registrarla como tal.
9. **La diapositiva 9 es solo un rótulo y un video.** Todo su contenido es «Plataforma SGDEA Piloto» y «VER VIDEO». El video **está incrustado en el archivo** (`ppt/media/media1.mp4`, 47,6 MB: de ahí salen los ~52 MB del `.pptx`), así que **no depende de internet** y no hay que temer que no cargue. El riesgo es de tiempo: es la única vista del producto en las diez diapositivas, y son cuatro integrantes en 20 minutos. Las dos condicionales del inicio de la §7 cubren que corra y que no corra.
10. **Un dato del mazo que el documento entierra:** la diapositiva 10 afirma la inoperancia de TRD y CCD «desde 2019», y eso **sí** está respaldado (Tabla 3: TRD «No actualizado desde 2019»; el cuerpo habla de instrumentos «inoperantes desde 2019»). Es una precisión que el documento no destaca y el mazo sí. Vale reconocérsela en voz alta.
11. **Lo que no aparece en ninguna de las diez diapositivas:** que el prototipo corre en el portátil personal de un integrante, en `localhost:5000` (pp. 89-91); la Tabla 14 y sus cuatro estados; las limitaciones del estudio; el presupuesto; el cronograma de 28 semanas (p. 96); y la declaración de similitud o de uso de IA. Las omisiones no son simétricas: **ocultan el techo real del producto y a la vez la honestidad que lo salvaba.** Lo que sí resuelve el mazo es la contradicción interna de la matriz: la diapositiva 4 dice «Matriz Diagnóstica: evaluar deterioro en 6 dimensiones», la versión de la p. 79 y no las tres de la p. 72.

### Qué mirar en pantalla mientras exponen

- Si alguien lee en voz alta «cifrado de grado militar» o «se verificó la integridad con AES-256», anotar la diapositiva y el minuto: es la premisa literal de la pregunta 1 y ya no admite matiz.
- Si la diapositiva 4 pasa rápido, retener la frase «muestra de tipo censal» tal cual: es la premisa de la pregunta 3 y en la respuesta pueden intentar reformularla.
- Si en algún momento proyectan un número de expedientes, folios o metros lineales —en el video, en una tabla, en un pie de diapositiva—, la pregunta 3 queda contestada y el turno se pasa a la reserva 7.
- En el video de la diapositiva 9: si aparece un módulo de respaldos o de copias, mirar si se **ejecuta** algo o solo se ve la pantalla. Ese medio segundo decide la respuesta a la pregunta 1.
- Si el video muestra la pantalla de auditoría, mirar si las columnas incluyen IP y resultado (la p. 104 dice que faltan).
- Vigilar si dicen «entorno controlado» o «entorno institucional controlado»: la diferencia entre las diapositivas 5 y 3 es la diferencia entre el OE4 cumplido y el OE4 aplazado.
- Contar cuántos integrantes hablan y en qué diapositivas. Diez diapositivas y un video se reparten mal entre cuatro personas; ese reparto es lo que sostiene la condicional de la §7 sobre quién no habló.

---

## 6. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. ¿Existe hoy un respaldo cifrado, sí o no? (documento contra diapositivas 7 y 10).**
> «La diapositiva 10 concluye que se verificó la integridad con cifrado AES-256, y su página 134 sostiene que el diseño de ese cifrado resolvió la obligación de confidencialidad de la Ley 1581, blindando jurídicamente a la Secretaría. Su Tabla 14, en la página 105, lo deja como representado en prototipo, con integración real proyectada. Una sola cosa: ¿existe hoy un respaldo del prototipo efectivamente cifrado, sí o no? Si es diseño y no operación, dígalo con esas palabras.»

- **Sale de:** de las **diapositivas**, y por eso va primero: la 7 escribe «cifrado de grado militar (AES-256)» —frase que no aparece en ninguna de las 169 páginas— y la 10 la pasa a pasado verificado. Del **documento** sale la refutación exacta: la Tabla 14 (p. 105) lo deja en «representado en prototipo». La contradicción no la construyo yo, la traen ellos entre sus dos entregables, y por eso no hay forma de tumbar la premisa.
- **Por qué:** es la única contradicción que toca a la vez resultados y cumplimiento normativo, y la acaban de afirmar en voz alta. Diapositiva 7: «Implementación de… cifrado de grado militar (AES-256)»; diapositiva 10: «se verificó… integridad con cifrado AES-256». Su Tabla 14 (p. 105) deja ese cifrado con Restic en «Representado en prototipo — integración real proyectada», y la p. 134 convierte el **diseño** en cumplimiento («blindando jurídicamente a la Secretaría»). Pide un artefacto binario, no una opinión: el guion de la exposición afirma lo contrario, así que no la responde. Refuerzos si objetan: p. 104 (auditoría «Implementado (parcial)… falta IP y resultado») y p. 80 (Ley 1581 calificada 1/5).
- **Qué la resuelve:** que digan sin rodeos «el cifrado está diseñado y representado, no operando» y remitan a la p. 105; sube más si distinguen ellos mismos los estados de la Tabla 14 y reconocen que las diapositivas 7 y 10 y la conclusión de la p. 134 deben corregirse. Resolución completa: mostrar en pantalla un repositorio Restic real con un snapshot cifrado del volumen `db_data`.
- **Qué la agrava:** sostener que el cifrado opera sin poder mostrarlo; usar «AES-256 diseñado» y «AES-256 implementado» como sinónimos; o defender el «blindaje jurídico» de la p. 134 con la auditoría implementada solo parcialmente (p. 104) y la Ley 1581 en 1 sobre 5 en su propio diagnóstico (p. 80).

**2. La capacitación de la p. 27: fecha y asistente.**
> «Su página 27 afirma en pasado que se realizaron sesiones de capacitación para el personal de la Secretaría, y enumera diez temas. Pero sus cuatro entrevistas, aplicadas el 24 de junio de 2026, todavía preguntan si el funcionario estaría dispuesto a recibir capacitación. Una sola cosa: ¿qué fecha tuvo esa capacitación y quién asistió? Si quedó planeada y no dictada, dígalo y lo registramos así.»

- **Sale de:** solo del **documento**, y es la única de las tres que el mazo no puede ni apoyar ni desmentir: **ninguna de las diez diapositivas menciona la capacitación**. La afirmación en pasado está en la p. 27 y su desmentido en las cuatro entrevistas (pp. 146, 153, 160 y 166). Consecuencia práctica: si no la nombran en la exposición, la pregunta sigue viva igual; y si la nombran, se les pide la fecha en el mismo turno, sin esperar.
- **Por qué:** es el punto donde el documento afirma como ejecutado lo que en otras cuatro páginas está en el futuro, y decide si el objetivo 4 se cumplió en la Secretaría o en un entorno de simulación. La premisa es literal y no se puede tumbar: 5.5.7 «Se realizaron sesiones de capacitación para el personal de la Secretaría de Gobierno» (p. 27) con los diez temas listados en la p. 28, frente al ítem F1 de las cuatro entrevistas del 24/06/2026 —«¿Estaría dispuesto a recibir capacitación…?»— en pp. 146, 153, 160 y 166 (fecha en pp. 141 y 167). Contraste: p. 105 («Implementación institucional — Proyectado a fase posterior») y p. 96 (verificación e implementación institucional en las semanas 23 a 26).
- **Qué la resuelve:** una fecha concreta y un asistente identificable —mejor, el acta o el registro de asistencia—; o la admisión limpia de que el apartado 5.5 describe acciones previstas del alcance y debió redactarse en futuro, remitiendo a la p. 105 y al cronograma de la p. 96 como estado real.
- **Qué la agrava:** insistir en el pasado sin poder dar fecha ni asistente; hacer pasar la sesión de entrevistas del 24 de junio por la capacitación; o afirmar que el sistema ya opera en la Secretaría, contra su p. 105 y contra la p. 132, que declara el objetivo 4 cumplido «en un entorno de simulación controlado».

**3. La cifra que la metodología prometió (objetivo 1).**
> «Su página 71 define el enfoque cuantitativo por medir volúmenes documentales en metros lineales y cantidad de folios, y presenta el FUID como el instrumento para cuantificar la muestra. En las 169 páginas, metros lineales y folios no vuelven a aparecer. ¿Cuántos expedientes, folios o metros lineales cubrió la muestra representativa de las páginas 78 y 86? Denos el número; si no se cuantificó, dígalo con esas palabras.»

- **Sale de:** de las dos piezas, y en direcciones opuestas. Del **documento**, el vacío: la p. 71 fija la unidad de medida —metros lineales y folios— y esas dos cadenas no vuelven a aparecer en 169 páginas. De las **diapositivas**, la sobreafirmación: la 4 dice «muestra de tipo censal», que es más de lo que el propio documento reclama tres veces (pp. 78, 86 y 130). El mazo, además, borra la única cifra fuerte del diagnóstico: la diapositiva 2 no proyecta los 45 a 90 minutos (§5, punto 4).
- **Por qué:** el objetivo 1 y todo el enfoque mixto se apoyan en esa muestra, y el propio diseño fijó la unidad de medida y el instrumento para medirla (p. 71: FUID «para cuantificar la muestra»). Refuerzo verificado: las cadenas «metros lineales» y «folio» aparecen **una sola vez** en las 169 páginas, en la p. 71 —ni la Tabla 2 del FUID tiene campo de folios—. No se les reprocha el tamaño; se les pide la cifra que su metodología prometió. Pide un número, así que no admite relato, y la exposición no lo da: la diapositiva 4 dice «Muestra de tipo censal», contra las pp. 78, 86 y 130.
- **Qué la resuelve:** cualquier cifra defendible con su origen —expedientes inventariados en el FUID piloto, folios, metros lineales o número de registros cargados— y la corrección expresa de la diapositiva 4, que debe decir muestra piloto y no censal. También la resuelve, con menos nota pero con honestidad, decir «no se cuantificó» y señalar que la p. 78 ya lo declara «diseño y aplicación piloto del instrumento».
- **Qué la agrava:** repetir «muestra representativa» sin un solo número; sostener el «censal» de la diapositiva 4 contra sus pp. 78, 86 y 130; o seguir llamando «línea base cuantificable» (pp. 86, 130 y 133) a un diagnóstico que no reporta ninguna cantidad de acervo.

### Lo que se leyó en la sala el 18/08 — para cotejar con la hoja escrita a mano

1. «Su Tabla 14 distingue con mucho cuidado lo implementado y probado de lo que está solo representado en la interfaz, y ubica el cifrado AES-256 y el hash SHA-256 en el segundo grupo. La diapositiva 10 concluye, en cambio, que se verificó la integridad con cifrado AES-256. ¿Me pueden precisar qué quedó implementado y probado en el prototipo y qué está representado a nivel de interfaz?»
2. «El documento precisa tres veces que el FUID se aplicó sobre una muestra y no sobre el censo de la vigencia 2024, mientras la diapositiva 4 dice muestra de tipo censal. ¿Cuántos expedientes o cuántos folios quedaron efectivamente inventariados, y con qué criterio se escogieron?»
3. «Su cuarto objetivo es verificar el prototipo en un entorno institucional controlado. La verificación documentada se hizo sobre un portátil personal, en localhost, y la implementación institucional aparece como proyectada. ¿Algún funcionario de la Secretaría usó el prototipo, y con qué datos: expedientes reales de 2024 o datos de prueba?»

### Banco de reserva (por si el tiempo estira o el director cede turno)

Los números no se cambian: la §7 cita estas reservas por número (`reserva 4`, `reserva 7`). Lo que sigue es el mismo banco, separado según de dónde salga la evidencia.

#### Del documento

4. **Perfiles del RBAC, ¿tres o seis?** La p. 30 define tres —Administrador (acceso completo), Archivista (registro y consulta) y Consultor (solo lectura)—, igual que la p. 26; la p. 94 habla de «los seis perfiles definidos» y la nota de la Tabla 14 afirma que el texto y el prototipo «quedan así alineados» (p. 105). ¿Cuál es el número?
5. **Sobre cuántos registros corrió CP-03.** Su verificación por `psql` confirma «los cuatro registros documentales» en la base (p. 121); CP-03 y CP-04 prueban la búsqueda por múltiples criterios (p. 110). Con cuatro expedientes, ¿qué discrimina la prueba de filtros?
7. **Autoría del 1,9/5:** ¿salió de la observación directa del equipo o de las respuestas de los cuatro entrevistados? La p. 72 dice que «la calificación fue asignada por el equipo investigador a partir de la observación directa», y la Tabla 3 se titula «Calificación de resultados de la encuesta diagnóstica» (pp. 79-80).
8. **El noveno ítem crítico, ¿en qué dimensión está?** La p. 83 dice que «los 9 ítems críticos… aparecen en cinco de las seis dimensiones», pero solo enumera ocho: falta «Condiciones ambientales — 1 — Crítico» (p. 80), que es conservación física, la sexta dimensión, tal como la propia p. 82 reconoce.
9. **Deshumidificación:** se justifica con «la calificación crítica (1/5) en conservación» (p. 135), pero la p. 82 dice que conservación física, con 3,25, es la única dimensión que supera el umbral. ¿Cuál de las dos cifras manda, y cuánto cuesta esa recomendación?
10. **Parque tecnológico para el despliegue que recomiendan:** ¿los «dos computadores disponibles» de la Tabla 3 (p. 80) o los «ocho equipos de escritorio con Windows» que la p. 90 atribuye al diagnóstico del ACA 1, entregable que no está en este documento?
11. **Evidencia de CP-01:** remite a un «Anexo — prototipo de backend» con la nota «Insertar aquí la captura correspondiente» (p. 109), y el trabajo solo tiene cinco anexos: cuatro entrevistas y el registro fotográfico (índice, p. 6). ¿La evidencia real de la persistencia son las Figuras 9 a 11 (pp. 120-121)?
12. **Cadena de custodia:** su modelo lógico declara `ip` y `resultado` en `registro_auditoria`, append-only y con NOT NULL (pp. 99-100), pero la Tabla 14 anota que en el prototipo «falta IP y resultado» (p. 104). ¿Qué acredita entonces el «blindaje jurídico» frente a la Ley 1581 que afirma la p. 134?
13. **Versiones declaradas del entorno:** la p. 90 registra Docker Compose v5.3.0 y Docker Desktop 29.6.1; ¿pueden confirmar esos números frente a la salida real de `docker compose version`?

#### De las diapositivas

6. **Tres metas distintas para el mismo indicador:** «≥ 40% de mejora» en la tabla de impacto (p. 24), «menos de cinco minutos» (p. 92) y «más del 50%» en la diapositiva 8. ¿Cuál es la meta oficial y de qué medición sale?
14. **«Deterioro Físico Crítico» (diapositiva 2) contra «3.25 — Aceptable» (diapositiva 6).** Las dos afirmaciones son suyas y son de la misma exposición. ¿Cuál describe el estado del acervo? Si la respuesta es «lo crítico son las condiciones ambientales» —que es el único ítem en 1/5 (Tabla 3, p. 80)—, está bien dicha; y entonces la p. 135 debería decir eso, y no «la calificación crítica (1/5) en conservación».
15. **La línea base que el mazo no proyecta.** ¿Por qué los 45 a 90 minutos de la Tabla 3 (p. 79), repetidos en las pp. 85 y 92, no aparecen en ninguna diapositiva? Es la cifra que le da sentido al «más del 50 %» de la diapositiva 8.
16. **«Entorno controlado» (diapositiva 5) o «entorno institucional controlado» (diapositiva 3 y OE4, p. 20):** ¿cuál de las dos redacciones describe lo que efectivamente se verificó?

---

## 7. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si el video de la diapositiva 9 no corre o no lo alcanzan a mostrar** → pedir que describan, sin video, el flujo completo de un documento: quién lo radica, cómo se le asigna serie, quién puede verlo y qué queda en la auditoría. Si describen el flujo con soltura, el video sobraba.
- **Si el video muestra el prototipo funcionando** → preguntar por una pantalla específica: «en el módulo de respaldos que acabo de ver, ¿ese respaldo cifrado se ejecuta o es la vista de la función proyectada?» (p. 105 dice que es la segunda opción).
- **Si dicen que el sistema «está implementado en la Alcaldía»** → pedir la fecha, el equipo donde quedó instalado y quién lo administra hoy; contrastar con p. 105.
- **Si presentan la reducción de 45-90 minutos a menos de 5 como resultado obtenido** → preguntar con qué medición: cuántas búsquedas, con qué expedientes, quién cronometró (p. 92 la declara «meta proyectada»).
- **Si afirman que capacitaron al personal** → preguntar cuántos funcionarios, cuándo, qué contenidos y si hay acta o lista de asistencia (p. 27 lo afirma; pp. 146, 153, 160 y 166 sugieren que la capacitación seguía siendo una expectativa).
- **Si dicen «muestra censal» en la exposición** → pedirles que conciliar esa afirmación con las pp. 78, 86 y 130 de su propio documento; darles la salida honesta: «¿fue una muestra o el censo?».
- **Si el diagnóstico se presenta como el resultado principal y el prototipo queda de adorno** → pedir que expliquen qué decisión de diseño del SGDEA salió directamente de un hallazgo del diagnóstico; el documento tiene la respuesta buena (los cuatro hallazgos críticos que originan el RBAC, p. 95).
- **Si no mencionan una sola limitación** → preguntar directamente cuáles son los tres límites del trabajo y qué no se puede concluir de él; es el hueco de la sección 5 **del documento** (pp. 23-32).
- **Si solo habla uno o dos integrantes** → pedir explícitamente a quien no habló que explique su parte: al que sostenga la parte archivística, cómo se construyó el DCF de tres niveles (p. 88); al de la parte técnica, cómo se probó la persistencia (CP-01, p. 109). Son cuatro integrantes: conviene oír al menos a tres.
- **Si atribuyen a la plataforma el «blindaje jurídico» de la Secretaría (p. 134)** → preguntar qué obligación normativa concreta queda cubierta hoy y cuál solo quedará cubierta cuando se implemente, en particular frente a la Ley 1581 de 2012, que el propio diagnóstico calificó en 1/5 (p. 80) y cuyo protocolo se recomienda redactar (p. 136).
- **Si el director ya preguntó por la muestra o por el estado del prototipo** → conservar la pregunta 2 (fecha y asistente de la capacitación) y usar el tiempo en la reserva 7 (autoría del 1,9/5) o en la reserva 4 (¿tres o seis perfiles del RBAC?).
- **Si se pasan de tiempo y saltan resultados** → ir directo al objetivo 4: «¿qué se verificó, dónde y con quién?».

---

## 8. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

Criterios: **dominio del tema · claridad · coherencia del documento · capacidad de defensa.**

- **Para 4,6 o más** necesito: (a) que sostengan en vivo la distinción de la Tabla 14 sin inflar el producto, corrigiendo ellos mismos la diapositiva del AES-256; (b) una cifra concreta de la muestra del FUID con su criterio de selección; (c) que reconozcan sin evasivas que la verificación fue de laboratorio y que la implementación institucional está pendiente; y (d) que hablen al menos tres de los cuatro integrantes con dominio de su parte. Sin (a) no hay 4,6.
- **4,0 – 4,4** si: explican bien el diagnóstico y el prototipo, pero no cuantifican la muestra o dejan sin conciliar la contradicción documento/presentación sobre el cifrado o sobre lo censal. Es el escenario más probable dado el estado de los dos entregables. *Recordatorio institucional: una nota de 4,4 en un solo criterio bloquea la meritoria del grupo.*
- **3,6 – 3,9** si: defienden como resultados obtenidos las cifras que su propio documento declara proyectadas (pp. 24, 92, 113), o si sostienen el despliegue y la capacitación de la p. 27 sin poder describirlos.
- **3,0 – 3,5** si: solo lee diapositivas quien expone, no puede explicar cómo funciona el prototipo por dentro (DCF, DRS, RBAC, persistencia) y responde a las tres preguntas con generalidades.
- **Por debajo de 3,0** solo si aparece algo que hoy no tengo indicio de que exista: que no puedan mostrar ni describir el prototipo, o que la evidencia presentada no corresponda al trabajo.

**Encuadre justo:** es una especialización profesionalizante. No corresponde exigir muestra estadísticamente representativa, validación externa de la matriz de diagnóstico ni despliegue en producción. Sí corresponde exigir que el título y el objetivo general se ajusten a lo entregado, que la muestra se declare, y que la presentación no afirme más que el documento. La Tabla 14 muestra que este grupo sabe hacer exactamente eso; la presentación es donde se les fue de las manos.

---

### 8.1 Formulario oficial del jurado — 5 criterios en escala 1–5

> **Instrumento distinto de los cuatro criterios de arriba.** Son las cinco preguntas del formulario que la Dirección le pide al jurado, cada una con opciones **1 2 3 4 5**. **Ninguna califica la sustentación oral:** las cinco se responden con el documento, así que van precargadas con la página que las sostiene y en sala solo se confirman.
>
> Lectura de la escala, fijada de antemano: **5** sobresaliente, sin reparos de fondo · **4** sólido, con reparos menores y declarados · **3** aceptable, con un reparo de fondo que el documento no resuelve · **2** deficiente: hay material, pero se contradice o no sostiene lo que afirma · **1** sin base verificable en el documento.
>
> ⚠️ **Este 1–5 no es la nota del acta.** La nota que se reporta sale de los cuatro criterios y de los umbrales de esta §8. La casilla del formulario la marca el jurado humano; esto es una propuesta con página.

**1. Planteamiento de la problemática y formulación de objetivos** — propuesto **3** / 5

> Claridad, pertinencia y delimitación del problema de investigación, así como la coherencia y precisión de los objetivos propuestos, verificando su alineación con el propósito del estudio y su viabilidad investigativa.

El problema está bien delimitado y es real —archivo municipal, FUID del Acuerdo 042 de 2002, vigencia 2024— y los objetivos son claros. El reparo de fondo está en el alcance: la **p. 27 afirma en pasado** un despliegue piloto, jornadas de digitalización y sesiones de capacitación de las que no hay una sola evidencia en el resto de las 169 páginas, y el OE4 promete verificar «en un entorno institucional controlado» algo que se verificó en un portátil personal, en localhost:5000 (pp. 89-91).

**2. Marco teórico y referentes conceptuales** — propuesto **2** / 5

> Solidez del sustento teórico del proyecto, la pertinencia y actualidad de las fuentes consultadas, y la capacidad de articular conceptos, enfoques y antecedentes que fundamenten adecuadamente la investigación.

El anclaje normativo es correcto y pertinente (Acuerdo 042 de 2002, AGN). Lo que impide más de un 2 es material y no interpretable: la bibliografía llega al documento final con **marcadores «[por verificar]»** (pp. 138-140) y hay citas del cuerpo que no existen en la lista (Contraloría 2024, AGN 2024, MinTIC 2024). Un referente que el propio documento marca como no verificado no puede fundamentar nada.

**3. Metodología, muestra y coherencia del diseño** — propuesto **2** / 5

> Correspondencia entre el enfoque metodológico, el tipo de estudio, las técnicas e instrumentos de recolección de información y la definición de la muestra, garantizando la coherencia interna del diseño investigativo.

Hay trabajo de campo real: matriz de 20 aspectos en 6 dimensiones con escala 1-5 y cuatro entrevistas fechadas el 24/06/2026. Pero **la muestra nunca se cuantifica** en las 169 páginas y el documento declara tres veces que no es censal (pp. 78, 86, 130), mientras la diapositiva 4 dice «muestra de tipo censal». Un diseño cuyo número de unidades analizadas no aparece en ninguna página, y cuyo propio mazo lo contradice, no acredita coherencia interna. Tampoco hay sección de limitaciones.

**4. Resultados y conclusiones** — propuesto **3** / 5

> Calidad en la presentación, interpretación y análisis de los resultados obtenidos, así como la consistencia y pertinencia de las conclusiones en relación con los objetivos, la problemática y el marco teórico del estudio.

El diagnóstico está bien construido y es la parte fuerte: 1,9/5 global (p. 81) desagregado en trazabilidad 1,33, tecnología 1,67, organización 1,75 y conservación 3,25 (p. 82). Y la **Tabla 14 (pp. 104-105) es lo mejor de todo el cohorte en honestidad de reporte**: clasifica cada componente como implementado, representado, diseñado o proyectado. Lo que lo frena en 3 es que las diapositivas 7 y 10 concluyen «cifrado de grado militar (AES-256)» sobre un componente que esa misma Tabla 14 marca como solo representado en la interfaz: el documento se corrige y el mazo lo deshace.

**5. Pertinencia disciplinar y articulación con la especialización** — propuesto **4** / 5

> Grado de alineación del proyecto con el campo disciplinar y los énfasis de la especialización cursada, así como su aporte potencial al desarrollo académico, profesional o investigativo del área.

Gestión documental electrónica en una alcaldía, con SGDEA, DCF de tres niveles, DRS, modelo ER de 14 entidades, RBAC de 6 perfiles y auditoría append-only (pp. 89-91): es transformación digital del sector público con necesidad documentada. No llega a 5 porque nada de eso salió del portátil.

**Suma propuesta: 14 / 25.**

**Qué subiría una casilla en sala:** El **criterio 4 pasa a 4** si sostienen en sala la distinción de su propia Tabla 14 —qué quedó implementado y probado frente a qué está representado— en vez de defender la diapositiva 10 (pregunta prioritaria 1). El **criterio 3 pasa a 3** si dan una cifra de expedientes o folios inventariados y el criterio con que se escogieron (pregunta 2).

**Qué la bajaría:** El **criterio 1 baja a 2** si defienden como ejecutado el despliegue de la p. 27. Ojo con el tiempo: son cuatro integrantes en 20 minutos, y si solo exponen sin responder, el que se resiente es el criterio 3, no estos cinco.

## 9. Observaciones administrativas (no académicas)

1. **Equipo de 4 integrantes.** El tope en Proyecto I/II de especialización es de 3. Es una observación para la Dirección del Programa, **no** un criterio para bajar la nota. Consecuencia práctica en sala: con 20 minutos y cuatro personas, conviene pedir de entrada que expongan máximo dos y responder preguntas los cuatro.
2. **Correos cruzados en el cronograma.** A Eliana Naranjo Cortés le figura el correo de Cristian Forero y a Cristian David Forero Álvarez el de Eliana Naranjo. Reportar a la Dirección para que no se envíe la retroalimentación a la persona equivocada.
3. **Firmante ausente en un anexo.** La declaración de originalidad (p. 12) lleva los cuatro nombres, pero el cierre del instrumento de entrevistas (p. 167) firma como «Equipo de investigación» solo a tres. No es un hallazgo académico; sí es la razón práctica para pedir que hable más de un integrante.
4. **Sin declaración de similitud (Turnitin) ni de uso de IA generativa** en las 169 páginas. Si el programa lo exige en la entrega final, es un pendiente de forma que se resuelve con el metodólogo, no en la sala.
5. **Logística de la presentación.** El `.pptx` pesa ~52 MB y la diapositiva 9 depende de un video («VER VIDEO»). Vale avisar al grupo antes de las 6:40 p. m. de que pruebe reproducción y audio; si el video falla, se les va la mitad del tiempo.
6. **Forma y ortografía** (bloque breve, no se pregunta en sala): «SECRETARIA» sin tilde en el título del trabajo y de la diapositiva 1; el nombre de una integrante aparece como «Nahtaly» en el cronograma y «Nathaly» en el documento; «Grafica 8» sin tilde y **dos gráficas numeradas 8** (pp. 98 y 113); en la p. 76 el texto remite a «(Tabla 2)» cuando la tabla que sigue, titulada en la p. 77, es la Tabla 1; la diapositiva 6 reporta una dimensión en 1,8 mientras la p. 82 la calcula en 1,75; y quedan restos de plantilla en la diapositiva 1 (notas «Usar máximo 5-6 líneas por diapositiva») y en el campo de evidencia de CP-01 (p. 109).

---

*Ficha preparada por Julian Andrés Castaño Espinosa (Jurado 2) el 15 de agosto de 2026. Todas las afirmaciones sobre el proyecto están referidas a la página del documento del grupo; las páginas 27, 78, 86, 90 y 105 se reverificaron una a una antes de cerrar la ficha.*
