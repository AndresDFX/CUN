# 26ET2-G-003 — Análisis y modernización del archivo municipal de la Secretaría de Gobierno de San Francisco, Putumayo, para mejorar la eficiencia documental en la vigencia 2024

**Sustentación:** martes 18 de agosto de 2026 · 6:40 p. m. – 7:00 p. m. · **Mi rol:** Jurado 2
**Integrantes:** José Javier Galvis Noguera (jose.galvisn@cun.edu.co), Eliana Naranjo Cortés (correo cruzado en el cronograma, ver §8), Cristian David Forero Álvarez (correo cruzado en el cronograma, ver §8), Gloria Nahtaly Florez Susa (gloria.florezs@cun.edu.co)
**Línea:** Gestión y Tecnología
**Directora / moderadora:** María Fernanda Rivera Sanclemente · **Jurado 1:** Hayder Alejandro Romero Sierra
**Documentos leídos:** `ACA_No_3_Proyecto_Final_VF.pdf` (169 páginas — única versión en la carpeta del grupo) y `presentación - Proyecto 2.pptx` (10 diapositivas)

---

## 1. Resumen para leer en 5 minutos

El proyecto interviene el archivo de la Secretaría de Gobierno de San Francisco (Putumayo). El objeto de estudio es el fondo documental de la vigencia fiscal **2024**, mientras que el desarrollo técnico y la redacción se ejecutaron en **2026** (p. 14) — el propio documento advierte ese desfase.

**Problema.** Gestión documental manual, sin inventario formal, sin SGDEA, con deterioro por humedad y sin trazabilidad; tiempos de localización de un expediente **entre 45 y 90 minutos** (pp. 17-18, 80).

**Método.** Enfoque mixto declarado, bajo modelo de investigación-acción (pp. 71, 23). Instrumentos: FUID del Acuerdo 042 de 2002, **matriz de diagnóstico de 20 aspectos en 6 dimensiones** calificados de 1 a 5, y **4 encuestas/entrevistas semiestructuradas** a funcionarios, aplicadas el 24 de junio de 2026 (pp. 72, 76-79, 141, 167). Se declara consentimiento informado (Ley 1581 de 2012) para entrevistas y fotografías (p. 72).

**Resultado del diagnóstico (objetivo 1).** Promedio general **1,9/5**: 9 ítems críticos, 8 deficientes, 1 aceptable y 2 en cumplimiento; el 85 % exige intervención (p. 81). Por dimensión: trazabilidad y seguridad 1,33; tecnología y cumplimiento normativo 1,67; organización 1,75; conservación física 3,25, la única sobre el umbral (p. 82). El FUID se aplicó **sobre una muestra, no censal**, y corresponde al «diseño y aplicación piloto del instrumento» (pp. 78, 86, 130).

**Producto (objetivos 2 y 3).** Prototipo **SGDEA**: Flask 3.0.3 + PostgreSQL 16 en dos contenedores Docker, ejecutado en el **portátil personal de un integrante**, consumido en `http://localhost:5000` (pp. 89-91). Diseño archivístico serio: DCF de tres niveles, DRS por serie, modelo entidad-relación de 14 entidades y modelo lógico con PK/FK y restricciones (pp. 88, 97-100). Seguridad: RBAC con **6 perfiles** y matriz de permisos, auditoría append-only (pp. 93-94, 105-110).

**Honestidad del alcance.** La **Tabla 14 (pp. 104-105)** clasifica cada capacidad en implementado / representado en el prototipo / diseñado / proyectado: *implementado y probado* → Flask-PostgreSQL, radicación con consecutivo (SGDEA-2026-000128), búsqueda con filtros, clasificación TRD, RBAC de 6 perfiles y persistencia por volumen; *solo representado* → cifrado AES-256 (Restic), hash SHA-256, OCR (Tesseract) y MinIO; *proyectado* → TLS, MFA, pruebas de usabilidad y seguridad e **implementación institucional**. Seis casos de prueba CP-01 a CP-06, todos «aprobados», uno con observación (pp. 109-110).

**Lo proyectado, no medido.** Reducción de tiempos a <5 minutos, metas de la tabla de impacto y la mejora por dimensión son **proyecciones**, y el documento lo dice (pp. 24, 92, 113-114). Cierra con 28 semanas de cronograma de implementación (p. 96), conclusiones (pp. 133-134) y recomendaciones por dimensión (pp. 135-136).

---

## 2. Coherencia título → objetivo → resultados

**Título** («análisis y modernización… para mejorar la eficiencia documental») y **objetivo general** («**Modernizar** el archivo municipal… en 2024», p. 20) prometen un verbo de implementación. Lo que existe y está evidenciado es un **diagnóstico + un prototipo verificado en laboratorio**, con la implementación institucional explícitamente aplazada (p. 105). El techo real del trabajo es *diagnosticar y diseñar/prototipar*, no *modernizar*. La pregunta de investigación (p. 19) pregunta «cómo la implementación… moderniza… y mejora la eficiencia», algo que el propio documento no responde con datos, sino con proyecciones (pp. 92, 113).

| Objetivo específico (p. 20) | ¿Se cumplió? | Evidencia (p.) | Qué falta |
|---|---|---|---|
| 1. Gestionar el archivo mediante diagnóstico e **inventario** de 2024 según AGN | **Sí, en la parte de diagnóstico; parcial en inventario** | Matriz de 20 aspectos y promedio 1,9/5 (pp. 79-84); FUID adaptado (pp. 77-78); autoevaluación de cumplimiento (p. 86) | El inventario **no es censal** y **nunca se cuantifica**: no hay número de expedientes, folios ni metros lineales (pp. 78, 86, 130). La Tabla 2 muestra los *campos* del FUID, no datos |
| 2. Desarrollar plataforma piloto con DCF y DRS | **Sí, como prueba de concepto** | Arquitectura (p. 87), DCF/DRS (p. 88), figuras C-1 a C-7 del prototipo (pp. 106-109), CP-01 a CP-04 (pp. 109-110) | Corre en equipo personal, no en la entidad (pp. 89-91); OCR y MinIO solo «representados» (p. 105); alertas del DRS y control de versiones **diseñados, no implementados** (p. 105) |
| 3. Establecer requisitos de seguridad y acceso, perfiles y protocolos | **Sí en diseño; parcial en implementación** | RBAC de 6 perfiles y matriz (pp. 93-94), protocolos (p. 94), CP-05 y CP-06 (p. 110) | Cifrado AES-256 y hash SHA-256 **representados, no integrados**; auditoría «implementada parcial: falta IP y resultado» (pp. 104-105); MFA proyectado |
| 4. **Verificar** el funcionamiento «en un entorno institucional controlado» frente a la normativa | **No en el entorno institucional** | Se declara cumplido en entorno de simulación Docker (p. 132); pruebas de persistencia (pp. 120-121) | La verificación fue en laboratorio local; «pruebas de usabilidad y de seguridad: **pendientes de ejecución**» e «implementación institucional: **proyectada**» (p. 105). El apartado de verificación institucional está redactado en futuro (p. 112) |

**Nudo de la incoherencia:** el capítulo de alcance afirma en pasado hechos que el resto del documento desmiente. P. 27: «Se **desplegó** la aplicación de prueba de forma piloto en la Secretaría de Gobierno», «Se **digitalizaron** selectivamente documentos prioritarios» y (p. 27-28) «Se **realizaron** sesiones de capacitación». No hay evidencia de ninguna de las tres: la implementación institucional está proyectada (p. 105), no se reporta ni una página digitalizada frente a la meta de «al menos 200 páginas» (p. 24) y las entrevistas preguntan a los funcionarios si *estarían dispuestos a recibir capacitación* (pp. 146, 153, 166), lo que sitúa la capacitación después del trabajo de campo.

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

## 4. Debilidades y huecos (con página)

1. **El verbo del objetivo general excede el producto.** «Modernizar… en 2024» frente a un prototipo no desplegado (pp. 20, 105). No es un problema de esfuerzo, es de formulación: el trabajo entrega diagnóstico y diseño/prototipo.
2. **Afirmaciones en pasado sin respaldo** (p. 27): despliegue piloto en la entidad, digitalización de documentos prioritarios y sesiones de capacitación. Ninguna tiene evidencia y las tres se contradicen con la p. 105 y con las entrevistas (pp. 146, 153, 166).
3. **La muestra nunca se cuantifica.** «Muestra representativa» (pp. 71, 78, 86, 130) sin número de expedientes, folios ni metros lineales, y sin criterio de selección. Con el alcance de estudio de caso una muestra pequeña es perfectamente aceptable; lo que no es aceptable es no decir cuál fue.
4. **La presentación dice «muestra de tipo censal» (diapositiva 4)**, exactamente lo contrario de lo que el documento afirma tres veces (pp. 78, 86, 130).
5. **La presentación sobreafirma la seguridad.** Diapositiva 7: «Implementación de… cifrado de grado militar (AES-256)»; diapositiva 10: «se verificó… integridad con cifrado AES-256». La Tabla 14 dice «representado en prototipo; integración real proyectada» y «verificación real pendiente» (p. 105). Es la contradicción más citable entre los dos entregables.
6. **El enfoque mixto queda a medias.** La p. 71 justifica lo cuantitativo por «cuantificar tiempos exactos de respuesta **antes y después** de la implementación»; no hay medición posterior: todos los valores de mejora son metas o proyecciones (pp. 24, 92, 113-114).
7. **Quién calificó la matriz no está claro.** La p. 72 dice que la calificación «fue asignada por el equipo investigador a partir de la observación directa»; la Tabla 3 se titula «Calificación de resultados de **la encuesta** diagnóstica» y su nota dice «se realizó una calificación de cada una de las preguntas realizadas en la encuesta» (pp. 79-80). Como el 1,9/5 es la base empírica de todo el trabajo, la ambigüedad pesa.
8. **La misma matriz se describe con 3 dimensiones (p. 72) y con 6 (p. 79).**
9. **Dato del parque tecnológico contradictorio:** Tabla 3, «Recursos tecnológicos: 3 — Dos computadores disponibles» (p. 80) frente a «según el diagnóstico del ACA 1: ocho equipos de escritorio con Windows» (p. 90).
10. **Restos de plantilla y evidencias vacías en el protocolo de pruebas.** CP-01 dice en el campo Evidencia: «**Insertar aquí la captura correspondiente**»; CP-02, CP-03, CP-04 y CP-06 tienen el campo Evidencia en blanco (pp. 109-110).
11. **Bibliografía con marcadores «por verificar» sobre fuentes que sí se citan en el cuerpo.** «Zapata, C. A., & Castrillón. (2020). [Título… por verificar]. [Datos de publicación por verificar]» (p. 140), citada como respaldo en pp. 15, 18 y 42; y «DANE (2024). [Título del informe estadístico — por verificar]» (p. 138), citada en pp. 14, 17, 18, 21 y 22. La entrada de Jaramillo Sánchez (2024) queda truncada sin datos de publicación (p. 139).
12. **Citas del texto sin entrada en la bibliografía:** «Contraloría General de la República, 2024» (pp. 14, 17, 18, 21), «AGN, 2024» y «MinTIC, 2024» no aparecen en la lista de referencias (pp. 137-140); además el texto cita «CCSDS, 2012» (p. 67) y la lista registra CCSDS 2024 (p. 138), y hay dos entradas duplicadas de PREMIS y dos de ISO 27001 (pp. 139-140).
13. **No hay apartado de limitaciones del estudio.** La sección 5 se titula «Alcances y Limitaciones» pero solo contiene alcance y delimitaciones (pp. 23-32). Faltan las limitaciones de los resultados (una sola dependencia, 4 informantes, prototipo en laboratorio, ausencia de medición post).
14. **La delimitación institucional se contradice:** dentro de «No incluye» aparece «Archivo municipal correspondiente al término 2024» (p. 29), que es justamente el objeto del proyecto.
15. **No se declara similitud (Turnitin) ni uso de herramientas de IA generativa;** tampoco hay presupuesto ni costeo del despliegue, pese a las 28 semanas de cronograma (p. 96) y a las recomendaciones de nube y deshumidificación (pp. 135-136).
16. **Conclusiones más fuertes que la evidencia:** «la integración de registros de auditoría inmutables y el diseño de cifrado AES-256 resolvieron la obligación de trazabilidad y confidencialidad… **blindando jurídicamente** a la Secretaría» (p. 134), cuando el cifrado no está integrado (p. 105) y la auditoría es parcial (p. 104).
17. **Redacción del planteamiento con citas incrustadas como frases sueltas** (pp. 15, 17, 18, 21-22): párrafos que terminan en un listado de autores y años sin verbo, y referencias completas insertadas dentro del cuerpo del texto (p. 15, p. 19).

---

## 5. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. Estado real del producto (el cierre de la brecha documento-presentación).**
> «Su Tabla 14 distingue con mucho cuidado lo implementado y probado de lo que está solo representado en la interfaz, y ubica el cifrado AES-256 y el hash SHA-256 en el segundo grupo. La diapositiva 10 concluye, en cambio, que se verificó la integridad con cifrado AES-256. ¿Me pueden precisar qué quedó implementado y probado en el prototipo y qué está representado a nivel de interfaz?»

- **Por qué:** Tabla 14, pp. 104-105 («Representado en prototipo… integración real proyectada», «verificación real pendiente») frente a la diapositiva 10 y a la diapositiva 7 («Implementación de… cifrado de grado militar»).
- **Qué la resuelve:** que repitan su propia clasificación sin titubear —comunicación Flask-PostgreSQL, radicación con consecutivo, búsqueda con filtros, clasificación TRD, RBAC de 6 perfiles y persistencia por volumen están probados; cifrado, hash, OCR y MinIO están representados— y que reconozcan que la diapositiva se pasó de afirmación. Eso demuestra dominio y honestidad a la vez.
- **Qué la agrava:** sostener que el cifrado está funcionando, o responder «sí, está implementado porque está diseñado». Confundir diseño con implementación en el criterio de seguridad es lo que el documento evitó y la presentación deshizo.

**2. Tamaño y naturaleza de la muestra (objetivo 1).**
> «El documento precisa tres veces que el FUID se aplicó sobre una muestra y no sobre el censo de la vigencia 2024, mientras la diapositiva 4 dice muestra de tipo censal. ¿Cuántos expedientes o cuántos folios quedaron efectivamente inventariados, y con qué criterio se escogieron?»

- **Por qué:** pp. 78, 86 y 130 declaran expresamente que no es censal y que la Tabla 2 es el diseño y aplicación piloto del instrumento; la diapositiva 4 afirma lo contrario. En ninguna página se da la cifra.
- **Qué la resuelve:** una cifra concreta (número de expedientes, carpetas o folios) con el criterio de selección —frecuencia de consulta, riesgo de deterioro, valor legal, como anuncia la p. 27— y el reconocimiento de que «censal» en la diapositiva es un error de la diapositiva. A este nivel, una muestra pequeña bien delimitada es suficiente.
- **Qué la agrava:** no tener el número, o defender que fue censal contradiciendo su propio documento.

**3. Objetivo 4: verificación en entorno institucional.**
> «Su cuarto objetivo es verificar el prototipo en un entorno institucional controlado. La verificación documentada se hizo sobre un portátil personal, en localhost, y la implementación institucional aparece como proyectada. ¿Algún funcionario de la Secretaría usó el prototipo, y con qué datos: expedientes reales de 2024 o datos de prueba?»

- **Por qué:** objetivo 4 (p. 20) frente a pp. 89-91 (simulación en equipo personal, `http://localhost:5000`), p. 105 («implementación institucional: proyectada a fase posterior»; «pruebas de usabilidad y de seguridad: pendientes de ejecución») y p. 112, redactada en futuro. La p. 27, en cambio, afirma que se desplegó el piloto y se capacitó al personal.
- **Qué la resuelve:** decir con claridad que la verificación fue técnica y en laboratorio, que la validación con usuarios queda pendiente, y explicar qué datos cargaron (los radicados que aparecen —SF-2024-0004, SGDEA-2026-000128— parecen de prueba). Si además hubo alguna sesión con funcionarios, describirla: cuántos, cuándo, qué hicieron.
- **Qué la agrava:** sostener el despliegue institucional y la capacitación de la p. 27 sin acta, lista de asistencia, captura o correo que lo respalde. Si dicen que cargaron expedientes reales, aparece de inmediato la pregunta de Ley 1581 y tratamiento de datos en un equipo personal.

### Banco de reserva (por si el tiempo estira o el director cede turno)

4. **Autoría de la calificación 1,9/5:** ¿la asignó el equipo por observación directa (p. 72) o se derivó de las respuestas de los cuatro funcionarios (Tabla 3 y su nota, pp. 79-80)? ¿Y la matriz tiene 3 dimensiones o 6 (pp. 72 vs. 79)?
5. **Parque tecnológico:** ¿dos computadores (p. 80) u ocho equipos de escritorio (p. 90)? De ello depende la viabilidad del despliegue que recomiendan.
6. **Enfoque mixto:** la p. 71 lo justifica por medir tiempos «antes y después»; ¿existe alguna medición posterior, o todo el «después» es proyección (pp. 24, 92, 113)?
7. **Digitalización:** la meta era al menos 200 páginas (p. 24) y la p. 27 afirma que se digitalizó selectivamente; ¿cuántas páginas se digitalizaron y dónde están?
8. **Evidencias de las pruebas:** CP-01 conserva la instrucción «Insertar aquí la captura correspondiente» y CP-02, 03, 04 y 06 tienen el campo Evidencia vacío (pp. 109-110). ¿Existen esas capturas?
9. **Bibliografía:** ¿cuál es la fuente de Zapata y Castrillón (2020), citada en pp. 15, 18 y 42 y registrada como «por verificar» (p. 140)? Igual para el informe del DANE 2024 (p. 138) y para Contraloría 2024, que no tiene entrada.
10. **Sostenibilidad:** con dos computadores, sin área de TI y sin presupuesto en el documento, ¿quién administra el SGDEA, hace los respaldos y responde por el 3-2-1 que recomiendan (p. 136)?
11. **Alertas del DRS:** están «diseñadas, no implementadas» (p. 105) y son el corazón de la retención documental. ¿Qué faltó para ejecutar la regla de disposición?
12. **Delimitación contradictoria:** ¿por qué el «No incluye» excluye el archivo de la vigencia 2024 (p. 29), que es el objeto del proyecto?
13. **Versiones declaradas del entorno:** la p. 90 registra Docker Compose v5.3.0; ¿pueden confirmar el número de versión frente a la salida real de `docker compose version`?

---

## 6. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si el video de la diapositiva 9 no corre o no lo alcanzan a mostrar** → pedir que describan, sin video, el flujo completo de un documento: quién lo radica, cómo se le asigna serie, quién puede verlo y qué queda en la auditoría. Si describen el flujo con soltura, el video sobraba.
- **Si el video muestra el prototipo funcionando** → preguntar por una pantalla específica: «en el módulo de respaldos que acabo de ver, ¿ese respaldo cifrado se ejecuta o es la vista de la función proyectada?» (p. 105 dice que es la segunda opción).
- **Si dicen que el sistema «está implementado en la Alcaldía»** → pedir la fecha, el equipo donde quedó instalado y quién lo administra hoy; contrastar con p. 105.
- **Si presentan la reducción de 45-90 minutos a menos de 5 como resultado obtenido** → preguntar con qué medición: cuántas búsquedas, con qué expedientes, quién cronometró (p. 92 la declara «meta proyectada»).
- **Si afirman que capacitaron al personal** → preguntar cuántos funcionarios, cuándo, qué contenidos y si hay acta o lista de asistencia (p. 27 lo afirma; pp. 146, 153, 166 sugieren que la capacitación seguía siendo una expectativa).
- **Si dicen «muestra censal» en la exposición** → pedirles que conciliar esa afirmación con las pp. 78, 86 y 130 de su propio documento; darles la salida honesta: «¿fue una muestra o el censo?».
- **Si el diagnóstico se presenta como el resultado principal y el prototipo queda de adorno** → pedir que expliquen qué decisión de diseño del SGDEA salió directamente de un hallazgo del diagnóstico; el documento tiene la respuesta buena (los cuatro hallazgos críticos que originan el RBAC, p. 95).
- **Si no mencionan una sola limitación** → preguntar directamente cuáles son los tres límites del trabajo y qué no se puede concluir de él; es el hueco de la sección 5 (pp. 23-32).
- **Si solo habla uno o dos integrantes** → pedir explícitamente a quien no habló que explique su parte: al que sostenga la parte archivística, cómo se construyó el DCF de tres niveles (p. 88); al de la parte técnica, cómo se probó la persistencia (CP-01, p. 109). Son cuatro integrantes: conviene oír al menos a tres.
- **Si atribuyen a la plataforma el «blindaje jurídico» de la Secretaría (p. 134)** → preguntar qué obligación normativa concreta queda cubierta hoy y cuál solo quedará cubierta cuando se implemente, en particular frente a la Ley 1581 de 2012, que el propio diagnóstico calificó en 1/5 (p. 80) y cuyo protocolo se recomienda redactar (p. 136).
- **Si el director ya preguntó por la muestra o por el estado del prototipo** → soltar mi pregunta 2 o 1 y usar el tiempo en la reserva 4 (quién calificó el 1,9/5) o en la reserva 9 (bibliografía «por verificar»).
- **Si se pasan de tiempo y saltan resultados** → ir directo al objetivo 4: «¿qué se verificó, dónde y con quién?».

---

## 7. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

Criterios: **dominio del tema · claridad · coherencia del documento · capacidad de defensa.**

- **Para 4,6 o más** necesito: (a) que sostengan en vivo la distinción de la Tabla 14 sin inflar el producto, corrigiendo ellos mismos la diapositiva del AES-256; (b) una cifra concreta de la muestra del FUID con su criterio de selección; (c) que reconozcan sin evasivas que la verificación fue de laboratorio y que la implementación institucional está pendiente; y (d) que hablen al menos tres de los cuatro integrantes con dominio de su parte. Sin (a) no hay 4,6.
- **4,0 – 4,4** si: explican bien el diagnóstico y el prototipo, pero no cuantifican la muestra o dejan sin conciliar la contradicción documento/presentación sobre el cifrado o sobre lo censal. Es el escenario más probable dado el estado de los dos entregables. *Recordatorio institucional: una nota de 4,4 en un solo criterio bloquea la meritoria del grupo.*
- **3,6 – 3,9** si: defienden como resultados obtenidos las cifras que su propio documento declara proyectadas (pp. 24, 92, 113), o si sostienen el despliegue y la capacitación de la p. 27 sin poder describirlos.
- **3,0 – 3,5** si: solo lee diapositivas quien expone, no puede explicar cómo funciona el prototipo por dentro (DCF, DRS, RBAC, persistencia) y responde a las tres preguntas con generalidades.
- **Por debajo de 3,0** solo si aparece algo que hoy no tengo indicio de que exista: que no puedan mostrar ni describir el prototipo, o que la evidencia presentada no corresponda al trabajo.

**Encuadre justo:** es una especialización profesionalizante. No corresponde exigir muestra estadísticamente representativa, validación externa de la matriz de diagnóstico ni despliegue en producción. Sí corresponde exigir que el título y el objetivo general se ajusten a lo entregado, que la muestra se declare, y que la presentación no afirme más que el documento. La Tabla 14 muestra que este grupo sabe hacer exactamente eso; la presentación es donde se les fue de las manos.

---

## 8. Observaciones administrativas (no académicas)

1. **Equipo de 4 integrantes.** El tope en Proyecto I/II de especialización es de 3. Es una observación para la Dirección del Programa, **no** un criterio para bajar la nota. Consecuencia práctica en sala: con 20 minutos y cuatro personas, conviene pedir de entrada que expongan máximo dos y responder preguntas los cuatro.
2. **Correos cruzados en el cronograma.** A Eliana Naranjo Cortés le figura el correo de Cristian Forero y a Cristian David Forero Álvarez el de Eliana Naranjo. Reportar a la Dirección para que no se envíe la retroalimentación a la persona equivocada.
3. **Firmante ausente en un anexo.** La declaración de originalidad (p. 12) lleva los cuatro nombres, pero el cierre del instrumento de entrevistas (p. 167) firma como «Equipo de investigación» solo a tres. No es un hallazgo académico; sí es la razón práctica para pedir que hable más de un integrante.
4. **Sin declaración de similitud (Turnitin) ni de uso de IA generativa** en las 169 páginas. Si el programa lo exige en la entrega final, es un pendiente de forma que se resuelve con el metodólogo, no en la sala.
5. **Logística de la presentación.** El `.pptx` pesa ~52 MB y la diapositiva 9 depende de un video («VER VIDEO»). Vale avisar al grupo antes de las 6:40 p. m. de que pruebe reproducción y audio; si el video falla, se les va la mitad del tiempo.
6. **Forma y ortografía** (bloque breve, no se pregunta en sala): «SECRETARIA» sin tilde en el título del trabajo y de la diapositiva 1; el nombre de una integrante aparece como «Nahtaly» en el cronograma y «Nathaly» en el documento; «Grafica 8» sin tilde y **dos gráficas numeradas 8** (pp. 98 y 113); en la p. 76 el texto remite a «(Tabla 2)» cuando la tabla que sigue, titulada en la p. 77, es la Tabla 1; la diapositiva 6 reporta una dimensión en 1,8 mientras la p. 82 la calcula en 1,75; y quedan restos de plantilla en la diapositiva 1 (notas «Usar máximo 5-6 líneas por diapositiva») y en el campo de evidencia de CP-01 (p. 109).

---

*Ficha preparada por Julian Andrés Castaño Espinosa (Jurado 2) el 15 de agosto de 2026. Todas las afirmaciones sobre el proyecto están referidas a la página del documento del grupo; las páginas 27, 78, 86, 90 y 105 se reverificaron una a una antes de cerrar la ficha.*
