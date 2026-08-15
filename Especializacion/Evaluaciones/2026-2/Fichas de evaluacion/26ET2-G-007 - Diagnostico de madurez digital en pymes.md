# 26ET2-G-007 — Diseño de un Modelo de Diagnóstico Estratégico Para Evaluar la Transformación Digital en las Pymes de Bogotá Orientado al Fortalecimiento de su Competitividad

**Sustentación:** martes 18 de agosto de 2026 · 8:00 p.m. – 8:20 p.m. · **Mi rol:** Jurado 2
**Integrantes:** Sonia Patricia Salamanca Avella (sonia.salamanca@cun.edu.co), Jhon Castro Oviedo (jhon.castro@cun.edu.co) — en la portada figura como «Jhon Jairo Castro Oviedo» (p. 1)
**Línea:** Ingeniería y Tecnología (según el cronograma de la Dirección)
**Dirección del proyecto:** Ing. María Fernanda Rivera Sanclemente (p. 2), quien además modera la sesión
**Documentos leídos:** `Proyecto Grado II_Grupo 7.pdf` (94 páginas) y `Tarea_1_Presentacion_Proyecto_2_Grupo_ 7_2.pdf` (19 diapositivas). Hay una sola versión de cada uno en la carpeta del grupo; el título correcto es el de la portada del trabajo (p. 1), no el del cronograma.

---

## 1. Resumen para leer en 5 minutos

Problema: las pymes de Bogotá adoptan tecnología de forma «aislada y reactiva, sin una articulación coherente dentro de una visión estratégica integral», y no existen modelos diagnósticos accesibles y contextualizados para medir su madurez digital (p. 14). La pregunta de investigación es doble: cuál es el nivel de transformación digital de las pymes de Bogotá y cómo estructurar un modelo de diagnóstico que identifique brechas (p. 15).

Qué hicieron. Estudio declarado descriptivo-propositivo (p. 31), de investigación aplicada con enfoque cuantitativo y cualitativo (pp. 32-33), sobre 30 pymes de Bogotá tomadas del banco de elegibles de la convocatoria «MiPymes Innovadoras» de la SDDE/ATENEA/Universidad Distrital (p. 33). Las 30 empresas están nombradas con razón social y localidad (p. 44), en 10 localidades (p. 84). El instrumento es un formulario en Forms de 11 preguntas —localidad más 10 dimensiones: nube, automatización, datos, canales digitales, cultura digital, ciberseguridad, colaboración, innovación, capacitación y estrategia de TD— con escala ordinal tipo Likert (pp. 34-35). La regla de calificación declarada es 0-3 puntos por pregunta, máximo 30, convertido a porcentaje, con cuatro niveles: Inicial, En Desarrollo, Avanzado y Líder Digital (pp. 36-37), y un informe de recomendaciones por nivel (p. 38). No se calculó Alfa de Cronbach ni otra medida de confiabilidad, y el documento lo dice (p. 38).

Qué obtuvieron. Respuestas individuales de las 30 empresas ítem por ítem (p. 46) y puntajes por dimensión con promedio y nivel por empresa (p. 47). Promedio de madurez 2,54 sobre 4 y nivel predominante «Avanzado» (p. 81); índice de madurez ponderado 71% (p. 78). Las dimensiones más rezagadas son canales digitales (2,07) y automatización (2,40) (p. 82). Segmentan las empresas en tres ecosistemas —Tech y nativos digitales ~40%, Servicios/Creativas/Salud ~33%, Manufactura/Comercio ~27%— con riesgos, prioridad de intervención y acción recomendada por segmento (pp. 50-52) e informe individual por empresa (pp. 85-87).

Qué producto entregan. Un prototipo de aplicación web con arquitectura React + Node/Express + MySQL (pp. 58, 74), módulos de cuestionario, cálculo, dashboard, reportes y seguridad (p. 59), modelo entidad-relación (p. 75), capturas de versión escritorio y móvil (pp. 69-73) y una matriz de pruebas funcionales (pp. 61-62). El propio documento califica el objetivo 3 como «cumplido parcialmente» por falta de evidencia visual y técnica completa (p. 89).

## 2. Coherencia título → objetivo → resultados

Título (p. 1), objetivo general (p. 16) y pregunta de investigación (p. 15) dicen lo mismo: **diseñar** un modelo de diagnóstico, soportado en una aplicación web. El verbo es «diseñar», no «implementar» ni «evaluar el impacto»: el techo del trabajo está bien puesto y el alcance lo respeta explícitamente («el proyecto se limita a diagnosticar... no incluye implementación ni seguimiento», p. 19).

| Objetivo específico (p. 16) | ¿Se cumplió? | Evidencia (p. N) | Qué falta |
|---|---|---|---|
| 1. Identificar las dimensiones clave de madurez digital para pymes de Bogotá, basadas en modelos reconocidos | Sí | Instrumento de 10 dimensiones (pp. 34-35); alineación argumentada con el DMM de Gartner (p. 37); cierre del objetivo con «10 dimensiones evaluadas — Cumplido» (p. 88) | Trazabilidad dimensión ↔ modelo de referencia: ellos mismos la registran como brecha, «documentar explícitamente la referencia metodológica usada para sustentar cada dimensión» (p. 88). Además el listado de dimensiones cambia entre el resumen (5: estrategia, procesos, tecnología, cultura, talento, p. 9), el alcance (6, con seguridad y datos/innovación, p. 19) y el instrumento (10, p. 34) |
| 2. Diseñar el modelo integrando dimensiones de TD con métricas de competitividad | Sí en la parte de madurez; **no** en la parte de competitividad | Regla de puntaje y niveles (pp. 36-37); recomendaciones por nivel (p. 38); clasificación por ecosistemas y tabla de impacto/prioridad (pp. 50-52); tabla de cierre «Cumplido» (p. 88) | Las «métricas de competitividad» no quedan definidas: el índice de competitividad digital se usa por empresa (p. 83) y en el mismo cierre del objetivo se recomienda «incluir un índice de competitividad digital basado en automatización, datos, innovación, canales digitales y nube» (p. 88), es decir, se propone a futuro lo que ya se reportó. Escala y número de niveles no unificados (0-3 y 4 niveles en pp. 36-37; 1-4 y niveles Inicial/Básico/Intermedio/Avanzado en p. 47; 3 segmentos en p. 76; 5 niveles de Gartner en p. 23) — conflicto que su propia matriz de pruebas registra (p. 61) |
| 3. Desarrollar la aplicación web prototipo (registro, autoevaluación en tiempo real, reportes personalizados) | Parcialmente, **y así lo declaran** | Arquitectura (p. 58), módulos (p. 59), esquema y modelo ER de base de datos (pp. 60, 63-64, 75), capturas del prototipo (pp. 54-57 y 69-73), matriz de casos de prueba (pp. 61-62) | «Cumplido parcialmente… falta evidencia visual/técnica completa de la aplicación web» (p. 89); «la lógica existe en formulario, tablas y dashboard, pero falta documentación técnica» (p. 81). Las columnas «Resultado real / Evidencia / Estado» de la matriz se describen como *uso recomendado* y el estado admite «No ejecutado» (p. 62): no hay reporte de ejecución de pruebas. El documento no declara URL de despliegue ni repositorio de código (buscado en las 94 páginas con `--buscar "repositorio,GitHub,URL"`) |
| 4. Analizar la relación entre madurez digital y competitividad con herramientas estadísticas y formular recomendaciones | **No verificable con lo entregado**; las recomendaciones sí están | Tabla de 30 empresas con nivel, puntaje TD e índice de competitividad (p. 83); tabla de brechas por dimensión (p. 82); recomendaciones priorizadas por dimensión y por frente estratégico (pp. 77, 81); cierre «Cumplido con oportunidad de profundización» (p. 89) | El coeficiente no aparece: «La correlación Pearson de **001** evidencia una relación positiva alta» (p. 84), «La correlación con el promedio de madurez digital es **001**» (p. 53), «Correlación TD vs índice competitividad digital: **001**» (p. 89) y lo mismo en la diapositiva 16. Los promedios se reportan como «**003** / 4» (pp. 53, 84) y las brechas como «**002**» (p. 80): son referencias rotas de hoja de cálculo. La sección titulada «d) Correlación de Spearman o Pearson» (p. 83) no contiene ningún estadístico, solo el listado de empresas |

**El nudo de coherencia.** En la p. 78 la «competitividad esperada» se **asigna** a partir del nivel de madurez (Avanzado → Alta, Intermedio → Media-alta, Inicial-Intermedio → Media), y en la p. 85 se declara que «el riesgo, ecosistema y prioridad se asignan según el nivel de madurez digital de cada empresa». Con eso, la conclusión «una mayor madurez digital se asocia con mayor competitividad esperada» (p. 79, y diapositiva 15) se deduce de la asignación y no de los datos. El documento reconoce a medias el problema: «la relación es estadística, pero debe complementarse con indicadores reales de productividad, ventas o clientes» (p. 84).

## 3. Fortalezas verificables

1. **Datos primarios reales y expuestos.** 30 empresas con razón social y localidad (p. 44), respuestas individuales ítem por ítem (p. 46) y puntajes por dimensión (p. 47). No es un trabajo de escritorio: hay trabajo de campo y se puede auditar.
2. **Los cuatro objetivos están rotulados en el cuerpo del trabajo** (pp. 44, 49, 53, 73) y cerrados en una tabla de resultados objetivo por objetivo (pp. 88-89). Es una estructura que facilita la lectura del jurado y es poco frecuente.
3. **Honestidad sobre los límites, y con detalle.** Muestra piloto no generalizable, sesgo de selección por voluntariedad, autodeclaración con deseabilidad social, estadística básica sin modelamiento predictivo, restricción geográfica y temporal (pp. 20-21); el prototipo «no constituye una solución escalable ni contempla soporte técnico posterior» (p. 21).
4. **Autocrítica técnica documentada.** La matriz de pruebas registra sus propias ambigüedades: escala 0-3 frente a tablas 1-4, cuatro niveles globales frente a una segmentación de tres, y «la evidencia de funcionamiento del prototipo es parcial» (p. 61). Detectar eso es criterio de ingeniería.
5. **Autoevaluación no complaciente:** califican el objetivo 3 como «cumplido parcialmente» y el 4 «con oportunidad de profundización» (p. 89), en vez de declarar todo cumplido.
6. **Producto con arquitectura definida, no una idea.** Frontend React/Vite, backend Node/Express, MySQL, servicios transversales de seguridad y monitoreo (pp. 58, 74), entidades del modelo ER enumeradas (p. 75) y capturas de las versiones escritorio y móvil (pp. 69-73).
7. **Anclaje normativo colombiano correcto y pertinente:** CONPES 3975, Estrategia Nacional de Transformación Digital 2030, PND 2022-2026, NTC 5854 (pp. 21-23), con referencias que sí aparecen en la lista final (pp. 93-94).

## 4. Debilidades y huecos (con página)

1. **El resultado central del objetivo 4 no tiene número.** «La correlación Pearson de 001» (p. 84); también en pp. 53 y 89 y en la **diapositiva 16**, que es la que se va a proyectar. Igual ocurre con «003 / 4» para los promedios (pp. 53, 84) y «002» para las brechas (p. 80).
2. **Dos clasificaciones incompatibles de las mismas 30 empresas.** 12 avanzado / 10 intermedio / 8 inicial-intermedio (pp. 46, 48, 52, 76, 78, 79, 85 y diapositivas 14-15) frente a 13 avanzado / 1 intermedio / 6 básico / 10 inicial (p. 80), que es lo que arroja la tabla de puntajes de la p. 47. Peor: la tabla de «validación de funcionamiento» de la p. 79 certifica «OK» la distribución 12/10/8 en la página inmediatamente anterior a la que la contradice.
3. **El índice de competitividad digital no está definido.** Se reporta por empresa con dos decimales (p. 83) sin fórmula, sin ítems y sin fuente; el instrumento (p. 34) no pregunta nada de competitividad; la única aproximación conceptual es «la competitividad se evalúa por eficiencia operativa, innovación y posicionamiento de mercado» (p. 25), que nunca se operacionaliza.
4. **Circularidad en el hallazgo principal**, ya explicada: competitividad esperada, riesgo, ecosistema y prioridad se asignan desde el nivel de madurez (pp. 78, 85) y luego se concluye que madurez y competitividad se asocian (pp. 79, 90).
5. **Escala y niveles sin unificar** (pp. 23, 36, 37, 47, 76). Es la ambigüedad que su propia matriz manda resolver «antes de ejecutar casos de cálculo» (p. 61) y que no se resolvió.
6. **La «validación del instrumento» prometida en el alcance** —«el proyecto incluye la construcción (diseño) y validación de un instrumento de medición» (p. 19)— se resuelve como correspondencia conceptual con el DMM de Gartner (p. 37). No hay panel de expertos ni confiabilidad, y el documento lo admite (p. 38). Para una especialización profesionalizante eso es aceptable; lo que no cuadra es prometer «validación» en el alcance.
7. **Enfoque mixto declarado sin componente cualitativo ejecutado.** Se declara cuantitativo y cualitativo (pp. 32-33), pero las entrevistas semiestructuradas quedan en condicional: «en caso de que se requiera información adicional se aplicarán…» (p. 76).
8. **Tiempos verbales en futuro dentro de secciones de resultados:** «se aplicará una encuesta vía forms» (p. 49), «los datos obtenidos se contrastarán», «se formularán lineamientos» (p. 73), «se generará un informe detallado» (p. 75). El trabajo de campo se lee como propuesta justo donde debería leerse como ejecución.
9. **No hay reporte de ejecución de pruebas del prototipo** (pp. 61-62), ni URL ni repositorio en las 94 páginas. La evidencia visual existe (pp. 54-57, 69-73), pero una de las capturas de «pantallas del prototipo» es código fuente de una barra de navegación (p. 57), no una pantalla en uso.
10. **La muestra responde a otra pregunta que la formulada.** La pregunta es por el nivel de TD de las pymes de Bogotá (p. 15); las 30 empresas vienen del banco de elegibles de «MiPymes Innovadoras» (p. 33) y ~40% son nativas digitales (p. 50), lo que explica que casi la mitad salga «avanzada» (p. 47) y choca con el punto de partida del resumen —«las pymes de Bogotá enfrentan un nivel bajo de madurez» (p. 9)—. El sesgo está declarado (p. 20) pero no se usa al concluir (p. 90).
11. **Faltan piezas de la última entrega:** no hay cronograma, presupuesto, anexos ni reporte de similitud en el PDF (94 páginas, buscados con `--buscar`); «presupuesto» solo aparece como recomendación para las empresas (p. 77).

## 5. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. El coeficiente que falta.**
> «En la tabla 13 de la página 84, y también en su diapositiva 16, la correlación entre madurez digital y competitividad aparece como “001”. ¿Cuál es el coeficiente que obtuvieron, con qué prueba lo calcularon —Pearson o Spearman— y sobre qué par de variables?»

- *Por qué:* p. 84 («la correlación Pearson de 001 evidencia una relación positiva alta»), p. 53 y p. 89 con el mismo «001», y la diapositiva 16. Es el resultado que cierra el objetivo 4.
- *Qué la resuelve:* dan el coeficiente concreto, dicen n = 30, identifican el «001» como una referencia rota de la hoja de cálculo y explican cómo se calculó.
- *Qué la agrava:* afirman que «es alta» sin poder dar el número, confunden Pearson con Spearman, o no saben de dónde salió el 001.

**2. De dónde sale la competitividad.**
> «El índice de competitividad digital que reportan empresa por empresa en la tabla 12 de la página 83, ¿con qué ítems y con qué fórmula se calcula, si el cuestionario de la página 34 solo pregunta por dimensiones de madurez digital?»

- *Por qué:* p. 83 (índice por empresa, con decimales), p. 34 (el instrumento no tiene ítems de competitividad), p. 78 (la «competitividad esperada» se asigna desde el nivel de madurez), p. 88 (recomiendan «incluir un índice de competitividad digital basado en automatización, datos, innovación, canales digitales y nube» *después* de haberlo usado).
- *Qué la resuelve:* muestran la fórmula, aunque sea un proxy construido con un subconjunto de las mismas dimensiones, y reconocen que en ese caso la correlación alta es esperable por construcción y no evidencia causal.
- *Qué la agrava:* sostienen que es una medida independiente de competitividad (ventas, productividad, clientes) sin poder decir de qué fuente salieron esos datos.

**3. Cuál de las dos clasificaciones entrega el modelo.**
> «En la página 79 su tabla de validación certifica “OK” la distribución de 12 avanzado, 10 intermedio y 8 inicial-intermedio; en la página 80, la tabla 10 reporta 13 avanzado, 1 intermedio, 6 básico y 10 inicial para las mismas 30 empresas. ¿Cuál de las dos clasifica el modelo que entregan, y con qué escala: 0 a 3 o 1 a 4?»

- *Por qué:* p. 79 (Tabla 9), p. 80 (Tabla 10), p. 47 (los puntajes 1-4 que producen 13/1/6/10), p. 36 (regla declarada 0-3, máximo 30 puntos), p. 61 (su matriz de pruebas ya señala el conflicto de escalas y de número de niveles).
- *Qué la resuelve:* identifican la tabla de la p. 47 como la clasificación del modelo, explican que 12/10/8 corresponde a la segmentación por ecosistema y prioridad de intervención y no al nivel de madurez, y dicen qué regla quedó programada en el aplicativo.
- *Qué la agrava:* defienden las dos cifras como equivalentes, o responden «eso lo calcula la herramienta» sin poder describir la regla.

### Banco de reserva

- **Alcance vs. validación.** «El alcance promete “construcción (diseño) y validación de un instrumento de medición” (p. 19) y en la página 38 ustedes escriben que no se calculó Alfa de Cronbach. ¿Qué entienden por validación en este trabajo y por qué es suficiente para el uso que le dan?»
- **Muestra y respuesta a la pregunta.** «Las 30 empresas vienen del banco de elegibles de “MiPymes Innovadoras” (p. 33) y cerca del 40% son nativas digitales (p. 50). ¿Cómo se lee entonces que casi la mitad salga en nivel avanzado, frente al punto de partida del resumen, que dice que las pymes de Bogotá tienen madurez baja (p. 9)?»
- **Pruebas del prototipo.** «La matriz de las páginas 61 y 62 define los casos y la guía de registro, pero las columnas de resultado y estado aparecen como “uso recomendado” y admiten “No ejecutado”. ¿Cuántos casos se ejecutaron y con qué resultado?»
- **Existencia del producto.** «El documento no declara URL de despliegue ni repositorio. ¿Dónde está corriendo hoy el aplicativo y quién puede entrar a usarlo?»
- **Enfoque mixto.** «La metodología declara enfoque cuantitativo y cualitativo (pp. 32-33) y las entrevistas semiestructuradas quedan condicionadas a “si se requiere información adicional” (p. 76). ¿Se hicieron entrevistas? Si no, ¿por qué se mantiene el componente cualitativo?»
- **Qué ve el empresario.** «El marco adopta los cinco niveles del DMM de Gartner (p. 23), la calificación del instrumento define cuatro (p. 37) y el modelo de intervención define tres (p. 76). ¿Cuál de los tres ve el empresario al terminar su autoevaluación?»
- **Datos de terceros.** «El trabajo publica la razón social de las 30 empresas junto con su nivel de madurez y sus debilidades de ciberseguridad (pp. 44, 83, 85). ¿Con qué autorización de las empresas se publica eso con nombre propio?»
- **Título vs. instrumento.** «El título dice “evaluar la transformación digital” y el instrumento mide madurez digital autodeclarada (p. 34). ¿Qué diría que su modelo no mide?»
- **Valor de las recomendaciones.** «Las recomendaciones de la página 38 son las mismas para todas las empresas de un mismo nivel. ¿En qué se diferencia eso de un informe genérico, y dónde entra el ecosistema o sector de cada empresa?»

## 6. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si mostraron el aplicativo funcionando en vivo** → pedir un caso de frontera: «hagan una autoevaluación que caiga en 24 % o 25 %, o en 74 % o 75 %, y muéstrenme qué nivel arroja» (su propia matriz marca esas fronteras como riesgo, p. 61).
- **Si NO lo mostraron funcionando y solo pasaron capturas** → «¿está desplegado? ¿Qué parte del flujo —registro, autoevaluación, cálculo, dashboard, reporte personalizado— está implementada y qué parte es diseño?» (p. 89 lo declara cumplido parcialmente).
- **Si dijeron un coeficiente en voz alta** (p. ej. «0,95») → pedir n, prueba usada y si las dos variables son independientes entre sí; si el índice de competitividad sale de los mismos ítems de madurez, el valor alto era inevitable.
- **Si dijeron «validamos el instrumento con expertos»** → cuántos expertos, con qué perfil, con qué método (interjueces, V de Aiken) y qué ítems se modificaron después. En el documento solo hay correspondencia conceptual con Gartner (p. 37).
- **Si presentaron la distribución 12/10/8 (diapositivas 14-15) sin mencionar la tabla 10** → ir directo a la p. 80 y preguntar por la diferencia; es la pregunta 3 tal cual.
- **Si generalizan las conclusiones a «las pymes de Bogotá»** → devolverles su propia limitación de la p. 20 (evidencia preliminar, sesgo de selección) y pedirles que reformulen el alcance de la conclusión en voz alta.
- **Si se pasaron del tiempo y saltaron los resultados del objetivo 4** → usar solo la pregunta 1, que es la más corta y la más discriminante.
- **Si habló solo uno de los dos** → pedirle explícitamente al otro que explique una de dos cosas, según quién habló: la regla de cálculo del puntaje y del nivel (pp. 36-37) o la arquitectura y el modelo de datos (pp. 58, 75).
- **Si mencionan entrevistas, visitas o acompañamiento a las empresas que no están en el documento** → cuántas, cuándo y dónde quedó el registro; en el documento están en condicional (p. 76).
- **Si afirman que el aplicativo ya lo usan empresas reales** → cuántas se registraron por sí mismas en el aplicativo, frente a las 30 respuestas que se recogieron por Forms (p. 45).
- **Si aparece en pantalla el «001» o el «003/4»** (diapositiva 16) → no señalar el error en público como tal; preguntar directamente por el valor, que es la pregunta 1, y dejar la nota de forma para la retroalimentación escrita.

## 7. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

Criterios: **dominio del tema · claridad · coherencia del documento · capacidad de defensa.**

- **Para 4,6 o más** necesito ver cuatro cosas: (a) el coeficiente de correlación con su prueba y su n; (b) la fórmula del índice de competitividad, aunque sea un proxy, dicho como proxy; (c) una explicación clara de por qué hay dos distribuciones y cuál rige el modelo; (d) el aplicativo calculando un caso en vivo. Con eso el documento se lee como un informe sólido con erratas de edición y no con huecos de fondo, y la nota alta es defendible.
- **4,0–4,4** si defienden bien el instrumento, el trabajo de campo con 30 empresas y el prototipo, pero el objetivo 4 sigue sin número y la contradicción entre 12/10/8 y 13/1/6/10 no se resuelve en sala. **Este es el escenario más probable a partir del documento.** Tener presente que un 4,4 mío bloquea la meritoria del grupo, así que si aclaran (a) y (c) hay que subir.
- **3,6–3,9** si además no distinguen madurez de competitividad —es decir, si defienden la circularidad como si fuera un hallazgo— o si el prototipo solo existe en capturas y no pueden decir qué está implementado.
- **3,0–3,5** si leen las diapositivas, no pueden explicar la regla de cálculo del puntaje y el nivel, o atribuyen los resultados a «lo que arrojó la herramienta» sin poder describir la regla.
- **Por debajo de 3,0** solo ante un problema de integridad: que los datos no soporten lo afirmado o que no puedan explicar de dónde salieron los 30 registros. Nada en el documento apunta hoy en esa dirección.
- **Calibración:** es una especialización profesionalizante. No pesa contra ellos la falta de muestra representativa, de validación externa del instrumento ni de aporte teórico original —todo eso está declarado como limitación en las pp. 20-21—. Lo que sí pesa es que el resultado que cierra el objetivo 4 no tenga cifra y que el mismo dato se reporte de dos maneras.

## 8. Observaciones administrativas (no académicas)

- **El título del cronograma trae tres erratas** («Diesño», «diagmnostico», «formtalecimiendo»). El título correcto es el de la portada (p. 1). Conviene pasárselo al moderador antes de leerlo en público.
- **El objetivo general del cronograma está abreviado y cambia el objeto:** dice «evaluar madurez digital», mientras el del documento dice «evaluar la transformación digital y su relación con la competitividad… soportado en una aplicación web» (p. 16).
- **Nombre de un integrante:** el cronograma dice «Jhon Castro Oviedo»; la portada, «Jhon Jairo Castro Oviedo» (p. 1). Equipo de 2, dentro del máximo de 3.
- **Tres fechas distintas en los preliminares:** portada «junio de 2026» (p. 1), declaración de originalidad firmada el 28 de febrero de 2026 (p. 11) y declaración de exoneración el 20 de febrero de 2026 (p. 12).
- **No hay reporte de similitud, cronograma, presupuesto ni anexos** en el PDF de 94 páginas (buscado con `--buscar`). Si la Dirección los exige para la entrega final, es un pendiente administrativo del metodólogo, no una nota de jurado.
- **Datos de terceros:** las 30 empresas aparecen con razón social junto a su nivel de madurez y sus debilidades de ciberseguridad (pp. 44, 83, 85). Vale la pena que la Dirección verifique si hay autorización de tratamiento de datos; es un asunto institucional y no debe mezclarse con la calificación.
- **Forma (bloque breve, no se pregunta en sala):** dos secciones numeradas «1» en la tabla de contenido —Introducción p. 13 y Planteamiento del problema p. 14— (p. 5); «Figura 7» repetida (pp. 45 y 46); «Figura 10» repetida (pp. 48 y 53); no aparecen las figuras 18 y 21; «Modelo Entidad - ERP» donde debe decir ER (p. 75); tres figuras distintas tituladas casi igual como diagrama de base de datos (pp. 60, 63, 64).
- **Presentación:** la diapositiva 6 dice, en el mismo cuadro, «la validación se limita a pruebas piloto con al menos 20 PYMES bogotanas» y «la validación piloto (30 empresas)»; el documento dice «al menos 30» (p. 20). Corregir antes de proyectar. El archivo conserva el nombre de entrega de aula (`Tarea_1_Presentacion_Proyecto_2_Grupo_ 7_2.pdf`).
- **La directora del proyecto (p. 2) es también la moderadora de la sesión.** Es lo previsto en este esquema; se anota solo para tenerlo presente al ponderar el 25% de jurados.
