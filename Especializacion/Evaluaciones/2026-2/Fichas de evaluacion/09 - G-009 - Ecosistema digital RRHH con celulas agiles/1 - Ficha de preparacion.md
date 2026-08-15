# 26ET2-G-009 — Transformación digital en la gestión de Recursos Humanos de una empresa del sector retail en Colombia, región Bogotá Sur: Diseño de un ecosistema digital mediante células ágiles para la optimización de procesos

**Sustentación:** martes 18 de agosto de 2026 · 8:40 p.m. – 9:00 p.m. (**último turno del día**) · **Mi rol:** Jurado 2
**Integrantes:** Yulieth Paola Rodríguez Roqueme (yulieth.rodriguezro@cun.edu.co), Loren Jasbleydi Prieto Cuenca (loren.prieto@cun.edu.co)
**Línea:** el cronograma de la Dirección la registra como «Arquitectura y estrategias para la transformación digital en las organizaciones»; la portada del trabajo declara «Gestión y Tecnología» (p. 1) y la segunda página la deja en blanco (p. 2). Discrepancia administrativa, ver §8.
**Documentos leídos:**
- `PROYECTO DE GRADO - YULIETH RODRIGUEZ - LOREN PRIETO.pdf` — **126 páginas** (trabajo de grado; única versión en la carpeta, sin sufijo de versión).
- `Sustentación Proyecto de grado- Loren Prieto - Yulieth Rodriguez.pdf` — **23 diapositivas** (presentación).
- Ruta: `G:\.shortcut-targets-by-id\17gSfmud5pWNib9sS2Y2KadGlqkJPJEZ1\26ET2-G-009\`

> **Convención de citas.** `(p. N)` = página del trabajo de grado de 126 páginas. `(dp. N)` = diapositiva de la presentación. Cuando algo no está, la ficha dice dónde se buscó y con qué término. Nada de lo que aquí se afirma sobre el proyecto viene de mi cabeza.

---

## 1. Resumen para leer en 5 minutos

**Problema.** Los procesos de talento humano de una empresa de retail de Bogotá Sur —más de 1.600 colaboradores— se tramitan con sistemas fragmentados, procedimientos manuales y seguimiento por múltiples canales, lo que rompe la trazabilidad y genera reprocesos (pp. 18-20). El documento afirma que los procesos operaban «en un 70 % de forma manual» (p. 45), **sin citar la fuente de ese porcentaje**.

**Qué se propusieron.** *Diseñar* un ecosistema digital para RR. HH. mediante células ágiles, orientado a optimizar procesos internos, fortalecer la autogestión y mejorar la experiencia del colaborador (p. 22). Cuatro objetivos específicos: caracterizar los procesos optimizables, estructurar un modelo de células ágiles, definir la arquitectura funcional y proponer un tablero de indicadores (p. 22). Pregunta de investigación coherente con lo anterior (p. 21).

**Cómo.** Enfoque mixto secuencial explicativo CUANT→cual, paradigma pragmático (p. 44); alcance exploratorio-descriptivo y aplicado (p. 46). Encuesta de 22 ítems Likert en cuatro dimensiones a **150 colaboradores** («muestreo estratificado probabilístico», p. 45) y **25 entrevistas semiestructuradas** (muestreo intencional tipo *snowball*, p. 45), más revisión documental y observación (pp. 56-58). Instrumentos validados por juicio de expertos (p. 54; Anexo 5, pp. 125-126). Tres fases en seis meses (pp. 47-48).

**Qué obtuvieron.** Eficiencia de procesos: promedio 3,2/5, con gestión documental 3,05 y tiempos de respuesta 3,07 como los más bajos (pp. 59-60). Acceso rápido a la información 2,85 y adecuación de las herramientas 2,96, marcadas «oportunidad crítica» (pp. 61-62). Alta aceptación del cambio: continuar la transformación digital 4,13 (p. 62) y «las metodologías ágiles pueden mejorar RR. HH.» 4,27 (p. 67). En entrevistas, *seguimiento de vinculaciones* aparece en el 52 % y *gestión documental* en el 36 % (p. 74). Con una matriz de priorización se eligió vinculaciones como eje (pp. 75-76), y se levantaron los procesos AS IS (p. 79) y TO BE (p. 80).

**Producto entregado.** Arquitectura funcional de seis módulos sobre Power Apps + SharePoint (p. 81); modelo de células ágiles con roles, sprint de dos semanas, backlog de siete historias, cuatro ceremonias y criterios de aceptación y de evaluación por célula (pp. 83-88); cuatro interfaces (principal, vinculaciones, seguimiento, tablero) (pp. 89-91); y dieciséis indicadores caracterizados con fórmula, fuente, frecuencia, responsable y meta (Tabla 14, pp. 93-97).

**Techo del trabajo, declarado por ellas mismas.** No hubo implementación ni piloto: los datos del tablero «tienen un propósito ilustrativo y no provienen de una implementación operativa» (p. 97) y los efectos «deberán verificarse mediante una implementación piloto» (pp. 78, 104). La presentación lo rotula igual: «Con datos simulados» (dp. 19).

## 2. Coherencia título → objetivo → resultados

El verbo del objetivo general es **«Diseñar»** (p. 22) y lo entregado es un diseño (pp. 103-104): **el techo declarado y el techo alcanzado coinciden**, que es lo primero que hay que reconocerle a este trabajo. El título añade «para la optimización de procesos» y el objetivo añade «fortalecer la autogestión y mejorar la experiencia del colaborador»: son *propósitos*, no resultados medidos, y el documento lo admite (pp. 78, 104).

| Objetivo específico | ¿Se cumplió? | Evidencia (p. N) | Qué falta |
|---|---|---|---|
| **1. Caracterizar** los procesos de RR. HH. susceptibles de optimización, con énfasis en seguimiento de vinculaciones y gestión colaborativa | **Sí** | Encuesta por dimensiones (pp. 59-67); 25 entrevistas categorizadas (pp. 69-74); matriz de priorización (pp. 75-76); proceso AS IS (p. 79) | Es un diagnóstico **de percepción**. No hay ni un valor duro de línea base (tiempo real de vinculación, número de reprocesos), y el «70 % manual» (p. 45) y la «rotación superior al 30 %» (p. 24) van sin fuente |
| **2. Estructurar** el modelo de células ágiles (roles, ciclos, articulación) | **Sí, en el nivel de diseño** | Roles (p. 83), sprint de dos semanas (p. 84), backlog de siete historias (pp. 84-85), ceremonias (p. 85), criterios de aceptación (p. 86) y de evaluación por célula (p. 87) | **Ambigüedad de fondo:** la p. 48 lista entre las **actividades de la fase 2** —fechada «Meses 3–4: mayo-junio 2026», ya transcurrida (p. 47)— la «Conformación de cuatro células ágiles (5–7 miembros… sprints quincenales)», mientras la p. 88 dice que los criterios de evaluación son guía «para una futura implementación». El documento **no declara** si esas células llegaron a conformarse: hay que preguntarlo |
| **3. Definir** la arquitectura funcional (vinculación, administración de personal, calidad de vida) | **Sí, parcialmente** | Arquitectura de seis módulos (p. 81); TO BE (p. 80); interfaces principal, vinculaciones y seguimiento (pp. 89-90) | Novedades de nómina, **portal de autogestión** —que las pp. 81 y 89 llaman «portal del colaborador»—, calidad de vida y códigos QR son cajas de la Figura 9 (p. 81) y accesos de la interfaz principal (Figura 11, p. 89), y nómina, calidad de vida y QR sí tienen indicadores caracterizados en la Tabla 14 (pp. 94-95); lo que **no** existe es una pantalla propia ni una especificación funcional de cada módulo: las Figuras 12 a 14 (pp. 89-91) solo desarrollan vinculaciones y el tablero. Calidad de vida queda además en prioridad «Baja» en el backlog (p. 85). No hay modelo de datos ni listas de SharePoint documentadas |
| **4. Proponer** el tablero conceptual de indicadores | **Sí** | Figura 14 (p. 91) y Tabla 14 con dieciséis indicadores (pp. 93-97) | La columna «Línea base» dice **«Diagnóstico inicial» en los dieciséis indicadores** (pp. 93-97), pero el diagnóstico no produjo ningún valor numérico de esos indicadores (pp. 59-74). Un tablero sin línea base no puede demostrar mejora |

## 3. Fortalezas verificables

1. **No sobreprometen.** El documento distingue explícitamente diseño de implementación en tres lugares distintos (pp. 78, 97, 104) y la presentación lo repite (dp. 19-20). En un periodo donde varios grupos hablan de «resultados» sin haber medido nada, esto es una virtud y hay que decirlo en la sala.
2. **Los cuatro objetivos específicos tienen producto localizable por página** (pp. 75-76, 83-88, 81 y 89-90, 93-97). No hay objetivo huérfano ni un «evaluar» final sin ejecutar.
3. **Trabajo de campo real y triangulado:** 150 encuestas + 25 entrevistas + revisión documental + observación, con el contraste entre lo cuantitativo y lo cualitativo hecho de forma explícita (pp. 73, 77).
4. **La priorización está argumentada, no elegida por gusto:** matriz de impacto/frecuencia/prioridad (pp. 75-76) y el backlog respeta ese orden (pp. 84-85).
5. **Los dieciséis indicadores están operacionalizados** con fórmula, fuente de datos, frecuencia, responsable, meta, unidad, sentido esperado y regla de interpretación (pp. 93-97). Es más de lo que suele traer un tablero «conceptual».
6. **Limitaciones honestas y suficientes:** dependencia tecnológica, acceso restringido a datos reales, resistencia al cambio, licencias, tiempo insuficiente para validar a largo plazo y no generalización más allá del caso (pp. 26-27).
7. **Cronograma y presupuesto reales**, con rubros, cantidades y total de $10.944.230 (Anexos 1 y 2, pp. 113-115).
8. **Instrumentos anexos y auditables:** encuesta (Anexo 3, p. 116 y ss.), guía de entrevista (Anexo 4, pp. 123-124) y descripción de la validación (Anexo 5, pp. 125-126).

## 4. Debilidades y huecos (con página)

1. **Diseño o ejecución de las células, sin resolver.** p. 48 («Conformación de cuatro células ágiles… sprints quincenales») contra pp. 87-88 y 104 («eventual/futura implementación»). Es el hueco más importante del documento porque afecta al objetivo 2 completo.
2. **Línea base inexistente pero declarada.** «Diagnóstico inicial» en las dieciséis filas de la Tabla 14 (pp. 93-97) sin un solo número; el diagnóstico solo produjo promedios Likert (pp. 59-67) y frecuencias de categorías (p. 73). Sumado al «70 % manual» sin fuente (p. 45), el punto de partida del proyecto no es verificable.
3. **Muestreo declarado por encima de lo hecho.** Se afirma «muestreo estratificado probabilístico» (pp. 45, 49) sin marco de muestreo, sin cálculo de tamaño, sin nivel de confianza ni error; y los estratos anunciados (nivel jerárquico y antigüedad, p. 45) no son los reportados (área y antigüedad, pp. 99-101). A nivel de especialización no se exige representatividad estadística, pero sí que lo declarado coincida con lo hecho.
4. **Plan de análisis incumplido en un detalle:** la p. 44 anuncia «promedios, medianas y frecuencias» y los resultados solo traen promedios y porcentajes (pp. 59-67). No hay ninguna mediana.
5. **Capítulo 10 «Resultados y discusión» anuncia lo que no contiene.** La p. 98 promete resultados por dimensión e integración de entrevistas y observación, pero el capítulo solo trae «10.1 Caracterización de la muestra» (pp. 99-102): los resultados ya estaban en el capítulo 9 (pp. 58-97). Duplicación estructural.
6. **Cuatro módulos anunciados y sin desarrollo propio** (nómina, portal de autogestión/«portal del colaborador», calidad de vida, QR): la p. 17 los enuncia, la Figura 9 los dibuja como cajas de la arquitectura (p. 81) y la interfaz principal los ofrece como accesos (p. 89); tres de ellos —nómina, calidad de vida y QR— sí tienen indicadores caracterizados en la Tabla 14 (pp. 94-95). Pero ninguno tiene pantalla propia ni especificación funcional: las Figuras 12 a 14 (pp. 89-91) solo desarrollan vinculaciones y el tablero. La autogestión es, además, uno de los tres propósitos del objetivo general (p. 22).
7. **Cero menciones de ética y autorización.** Búsqueda en las 126 páginas de «consentimiento», «confidencialidad», «ética», «anonimato» y «habeas»: **ningún resultado**. No hay carta de aval de la empresa entre los anexos (pp. 113-126) y la organización se mantiene sin nombre (p. 45) sin explicar que sea por confidencialidad. Son 175 participantes reales.
8. **Ninguna referencia a similitud o Turnitin** en el documento (búsqueda de «Turnitin» y «similitud»: sin resultados). No es un hallazgo contra el grupo: es un dato que le corresponde al metodólogo (ver §8).
9. **Anexo 5 sin sustancia verificable:** describe el juicio de expertos y sus cuatro aspectos evaluados, pero no dice **cuántos** expertos, **quiénes** ni incluye los formatos diligenciados (pp. 125-126).
10. **Lista de referencias con dos series alfabéticas y restos de plantilla.** Una serie en pp. 107-111 y otra, con otro formato, en pp. 111-112. Duplicados exactos: Pérez 2024a/b/c y Páez-Gabriunas 2021a/b (p. 109), Rojas Gallardo repetido (pp. 110-111). Dos citas del texto que no están en la lista: Méndez-Gutiérrez et al. (2023) y Pastuña (2025), ambas en la p. 15. Y entradas sin relación alguna con el proyecto: la norma IEEE 802.15.4 (2006), el software SPSS 27 —que la metodología nunca usa, el análisis fue en Google Forms y estadística descriptiva (p. 56)—, Rioja (2008) sobre judicialización de la salud y personas sordas, y Ramírez & Guzmán sobre sistemas participativos de garantía agrarios (pp. 111-112). Son ejemplos típicos de una plantilla APA que no se depuró.
11. **Discrepancia documento vs. presentación en la muestra:** la dp. 7 afirma «150 colaboradores (20 de RR. HH. y 130 operativos)»; la Tabla 15 (p. 99) reporta Recursos Humanos 15 (10,0 %), Operaciones 70, Logística 35, Comercial 25 y Otro 5.
12. **Lo que la presentación decidió no mostrar:** ni un solo promedio de la encuesta (dp. 10 resume las cuatro dimensiones en prosa), ni la matriz de priorización con sus valores (dp. 11 la muestra sin cifras), ni las limitaciones desarrolladas (dp. 5 las lista en cinco viñetas). En cambio la dp. 13 introduce **Power Automate**, que en el documento no aparece como componente de la arquitectura (la p. 81 nombra Power Apps y SharePoint; Power Automate solo sale en antecedentes y referencias, pp. 33-34 y 108-110).

**Forma y ortografía (bloque breve, no se pregunta en sala).** «Elboración propia» (p. 84); «TECONOLOGICOS» (p. 115); falta un «se» en «Como parte de la propuesta diseñaron las interfaces» (p. 16); encabezado fusionado «8.3 Población y muestra Componente cuantitativo:» (p. 45); numeración del marco inconsistente —el índice lista «7 Tecnologías habilitadoras» y «7.3 Marco conceptual» mientras el marco teórico es 6.2 y arranca en 6.2.2 (pp. 4-5)—; referencias cruzadas erradas: la p. 99 remite a la «Tabla 16» para mostrar la Tabla 15, la p. 101 remite a la «Tabla 17» para la Tabla 16, y la figura de antigüedad se numera «Figura 10» (p. 101) cuando la Figura 10 es el modelo de células ágiles (p. 82).

## 5. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. Las cuatro células ágiles: ¿se conformaron o se diseñaron?**
> «En el diseño metodológico, la fase 2 registra como actividad la conformación de cuatro células ágiles de cinco a siete miembros, con Scrum/Kanban y sprints quincenales (p. 48); pero al cerrar el capítulo el modelo se plantea como guía para una futura implementación (p. 88). ¿Esas cuatro células se conformaron con personas de la empresa y alcanzaron a correr algún sprint, o el segundo objetivo se cerró en el nivel de diseño?»

- **Por qué se pregunta:** es la única contradicción interna que cambia el alcance real del trabajo (p. 48 vs. pp. 87-88 y 104), y afecta a un objetivo específico completo.
- **Qué la resuelve:** cualquiera de las dos respuestas dicha con claridad. Si se conformaron: nombrar quiénes ocuparon los roles de la Tabla 8 (p. 83), cuántos sprints y qué entregable salió. Si no: decir que la redacción de la p. 48 quedó en clave de plan y que el objetivo 2 es diseño, que es lo que el resto del documento sostiene.
- **Qué la agrava:** afirmar que las células «ya operan» sin poder nombrar una ceremonia realizada ni un entregable de sprint; o cambiar de versión a mitad de la respuesta.

**2. La línea base de los indicadores: un número, no una etiqueta.**
> «En la Tabla 14 los dieciséis indicadores llevan como línea base la palabra "Diagnóstico inicial" (pp. 93-97). Denme un número: ¿cuánto es hoy el tiempo promedio de cubrimiento de una vacante en esa empresa, y de dónde sale ese dato?»

- **Por qué se pregunta:** sin valor de partida, el tablero no puede demostrar mejora, y el documento sostiene en el diagnóstico que el 70 % de los procesos era manual (p. 45) sin decir de dónde viene esa cifra.
- **Qué la resuelve:** dar el valor y su fuente (los registros internos revisados en la fase 1, p. 56), **o** reconocer con precisión que la línea base queda pendiente porque el diagnóstico fue de percepción y que el primer paso del piloto es medirla.
- **Qué la agrava:** repetir «diagnóstico inicial» como si fuera una cifra, o improvisar un número que no está en el documento.

**3. El estado real del artefacto que se ve en las figuras.**
> «Las figuras 11 a 14 muestran interfaces del ecosistema (pp. 89-91) y ustedes aclaran que los datos del tablero son ilustrativos (p. 97). ¿Esas pantallas son aplicaciones construidas en Power Apps que se pueden abrir en un entorno, o son maquetas del diseño funcional? Y si están construidas, ¿sobre qué listas de SharePoint corren?»

- **Por qué se pregunta:** el objetivo es diseñar, así que una maqueta es perfectamente legítima; lo que no es legítimo es la ambigüedad. La palabra «diseñaron las interfaces» (p. 16) admite las dos lecturas.
- **Qué la resuelve:** nombrar el entorno (tenant educativo, licencia, app en modo de prueba) y ofrecer abrirla, **o** decir sin rodeos «son maquetas de la arquitectura funcional».
- **Qué la agrava:** decir «está implementado y funcionando», porque contradice las pp. 97 y 104 y obliga a la pregunta siguiente: entonces por qué no hay medición.

### Banco de reserva

- **R1 (autogestión).** El objetivo general promete «fortalecer la autogestión» (p. 22) y el portal aparece como módulo de la arquitectura (pp. 17, 81) y como acceso de la pantalla principal (p. 89), pero no tiene interfaz propia ni especificación funcional (las Figuras 12 a 14, pp. 89-91, desarrollan vinculaciones y el tablero). ¿Qué parte concreta del diseño responde a esa promesa?
- **R2 (muestreo).** ¿Cómo se construyeron los estratos y cómo se seleccionó a los 150 dentro de cada uno, si lo declarado son nivel jerárquico y antigüedad (p. 45) y lo reportado es área y antigüedad (pp. 99-101)?
- **R3 (composición de la muestra).** La diapositiva 7 dice 20 personas de RR. HH.; la Tabla 15 (p. 99) dice 15. ¿Cuál es la cifra correcta?
- **R4 (autorización y datos).** ¿Con qué autorización de la empresa se aplicaron los instrumentos a 175 personas y cómo se protegió su identidad? (No hay ninguna mención de consentimiento ni de confidencialidad en las 126 páginas ni en los anexos).
- **R5 (jueces expertos).** ¿Cuántos expertos participaron en la validación y de qué perfil? El Anexo 5 (pp. 125-126) no lo dice.
- **R6 (herramienta de análisis).** ¿Con qué se procesaron las 150 respuestas? La metodología menciona Google Forms y estadística descriptiva (p. 56), y el plan anunciaba medianas que no aparecen (p. 44).
- **R7 (sostenibilidad).** El presupuesto asume licencias Power Apps educativas sin costo (p. 115) y las limitaciones advierten el costo de licencias (p. 26). Al salir del entorno académico, ¿qué licenciamiento necesitaría la empresa para los módulos priorizados?
- **R8 (solo si sobra tiempo).** El backlog deja calidad de vida en prioridad «Baja» (p. 85) aunque es uno de los tres procesos del objetivo 3 (p. 22). ¿Se sostiene ese objetivo o se recortó de hecho?

## 6. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si no dicen en voz alta que el trabajo terminó en diseño y no en implementación** → hacer la pregunta 3 tal cual, sin preámbulo.
- **Si dicen «implementamos» o «está en producción»** → pedir el entorno o la captura en vivo y contrastar con las pp. 97 y 104, donde el propio documento dice lo contrario. Preguntarlo como aclaración, no como acusación: puede ser un desliz de lenguaje.
- **Si presentan el tablero sin decir que los datos son simulados** (la dp. 19 sí lo rotula) → preguntar de dónde salen esos números.
- **Si atribuyen mejoras cuantificadas** («se redujeron los tiempos», «bajaron los reprocesos») → pedir cuándo se midió y contra qué línea base, y recordar las pp. 78 y 104.
- **Si solo habla una de las dos** → pedirle explícitamente a la otra que explique el modelo de células ágiles —roles y ceremonias, pp. 83-85— o la construcción de los indicadores (pp. 93-97). Es la vía legítima para verificar dominio individual.
- **Si se saltan la fase 1 por tiempo** → preguntar por la matriz de priorización (pp. 75-76): vinculaciones y gestión documental quedaron ambas en prioridad «Alta», ¿por qué el eje fue vinculaciones?
- **Si mencionan Power Automate** (dp. 13) → preguntar qué flujos automatizados quedaron especificados, porque en el documento la automatización aparece como criterio de la arquitectura (p. 81) y no como flujo diseñado.
- **Si afirman que las células ya operan en la empresa** → pregunta 1 en su versión dura: acta, tablero de sprint o nombres de los roles cubiertos.
- **Si no mencionan ninguna limitación** → pedirles que digan las dos que ellas mismas escribieron (pp. 26-27) y cuál pesaría más en una implementación real.
- **Si el día va retrasado y les quedan menos de 12 minutos** → renunciar a la pregunta 2 y quedarse con la 1 y la 3, que son las que definen el alcance real del trabajo.

## 7. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

**Punto de partida antes de oírlas: 4,0–4,4.** Es un documento coherente, con campo real, con producto localizable y honesto sobre sus límites; lo que lo frena no es el nivel de exigencia de maestría, es que el punto de partida del proyecto no es verificable (línea base ausente, pp. 93-97) y que hay una contradicción interna sobre la ejecución del objetivo 2 (p. 48 vs. p. 88).

| Criterio | Para 4,6+ necesito ver | Si falta, estamos en |
|---|---|---|
| **Dominio del tema** | Que resuelvan la pregunta 1 sin ambigüedad y que expliquen por qué un diseño con línea base pendiente sigue siendo un aporte; que sepan de memoria sus propios números (3,2 de eficiencia, 2,85 de acceso a la información, 52 % de vinculaciones) | 4,0–4,4 si dependen del documento para recordar sus datos |
| **Claridad** | Exposición que separe explícitamente diagnóstico → diseño → lo que queda para el piloto, sin leer las diapositivas | 3,6–4,0 si leen las láminas o si el tablero se presenta como si fuera operativo |
| **Coherencia del documento** | Que la respuesta sostenga lo que el documento dice, y que la contradicción de la p. 48 se explique como redacción y no como hecho | 4,0–4,4 tal como está: la cadena título→objetivo→resultados sí cierra (pp. 22, 103-104), pero la línea base declarada y no existente, el capítulo 10 duplicado y las referencias con restos de plantilla (pp. 111-112) impiden el 4,6 |
| **Capacidad de defensa** | Que **ambas** respondan, que acepten un límite sin defenderlo de más y que ofrezcan cómo lo medirían en el piloto | 3,0–3,5 si sostienen impactos que no midieron o si solo una de las dos puede defender el trabajo |

**Fronteras que dejo escritas antes de entrar, para no improvisarlas:**
- **5,0 (laureada) no está sobre la mesa** en este trabajo: la lista de referencias arrastra entradas ajenas al proyecto (pp. 111-112) y dieciséis indicadores se declaran con una línea base que no existe (pp. 93-97). Eso basta para que no sea un trabajo impecable, por bien que sustenten.
- **4,6–4,99 (meritoria) es alcanzable** solo si contestan las tres preguntas y ambas demuestran dominio: sería premiar la honestidad metodológica y la operacionalización de los indicadores, que son sus dos mejores activos.
- **Por debajo de 3,0** solo si afirman resultados de impacto que el documento niega (pp. 97, 104) o si no pueden explicar su propio instrumento.

## 8. Observaciones administrativas (no académicas)

1. **Línea de profundización discrepante.** Cronograma de la Dirección: «Arquitectura y estrategias para la transformación digital en las organizaciones». Portada del trabajo: «Gestión y Tecnología» (p. 1). Página 2: en blanco. **Confirmar con la Dirección con cuál queda el acta** antes de firmar.
2. **Equipo de dos integrantes:** cumple el máximo de tres de Proyecto II. Sin observación.
3. **La directora del trabajo es María Fernanda Rivera Sanclemente** (p. 2), la misma directora/moderadora de la sesión. Es lo habitual en el programa; solo conviene tenerlo presente al leer el 75 % del metodólogo frente al 25 % de jurados.
4. **No hay informe de similitud ni declaración de uso de IA generativa** en las 126 páginas. Pedírselo al metodólogo o a la Dirección, **no** al grupo en la sala.
5. **No hay carta de aval o autorización de la empresa** entre los anexos (pp. 113-126), pese a un trabajo de campo con 175 participantes. Si la Dirección la exige para trabajos de campo, falta el documento.
6. **Anexo 3:** el instrumento se entrega como enlace a Google Forms en modo `preview` (p. 116) y las pp. 117-122 son imágenes sin texto extraíble. Si alguien quiere auditar la encuesta, quizá necesite sesión activa.
7. **Cronograma del Anexo 1** (p. 113): cubre noviembre, diciembre, mayo, junio, julio y agosto, con cuatro meses sin actividad entre diciembre y mayo, mientras la p. 47 declara «seis meses con hitos mensuales» y fecha la fase 2 en «Meses 3–4: mayo-junio 2026». Dato para el metodólogo, no para la sala.
8. **Turno de riesgo:** son el último grupo del martes (8:40–9:00 p.m.), detrás de ocho grupos. Si el día acumula retraso, ir con las preguntas 1 y 3 solamente.
9. **Correos institucionales de las dos integrantes correctos** en el cronograma (dominio `@cun.edu.co`). Sin observación.
