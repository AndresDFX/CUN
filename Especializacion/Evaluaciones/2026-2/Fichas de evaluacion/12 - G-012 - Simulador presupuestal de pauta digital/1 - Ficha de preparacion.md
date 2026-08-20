# 26ET2-G-012 — Diseño de un prototipo de simulación para optimizar la asignación de recursos en campañas de marketing digital mediante la evaluación de escenarios en plataformas de Social Media

**Sustentación:** miércoles 19 de agosto de 2026 · 6:40 p.m. – 7:00 p.m. (segunda sesión del panel, 6:00–7:20 p.m.) · **Mi rol:** Jurado 2
**Integrantes:** Anderson Iván Ortiz Cifuentes (anderson.ortizc@cun.edu.co), Lida Vannesa Acosta Varela (lida.acosta@cun.edu.co), Jonathan Orlando Cifuentes Aldana (jonathan.cifuentesa@cun.edu.co), Carol Alejandra Parada Zárate (carol.parada@cun.edu.co)
**Línea:** Mejoramiento de procesos organizacionales
**Panel:** María Fernanda Rivera Sanclemente (directora/moderadora) · Hayder Alejandro Romero Sierra (Jurado 1) · Julián Andrés Castaño Espinosa (Jurado 2)
**Documentos leídos:**
- `Proyecto_de_grado_II_Validacion_y_Desarrollo_del_producto-1 Final.pdf` — 71 páginas (única versión en la carpeta; portada fechada junio de 2026, p. 1)
- `Presentación Final 25ET1 - Proyecto-Seminario II - Grupo 12.pptx.pdf` — 19 diapositivas

---

## 1. Resumen para leer en 5 minutos

El proyecto parte de un diagnóstico sectorial, no de una empresa cliente: las áreas de marketing tienen datos pero planifican con supuestos deterministas, y medir qué canal funciona mejor es cada vez más difícil (p. 14, con Gartner 2022, IAB & PwC 2024 y WARC 2024). La pregunta de investigación es cómo el diseño de un simulador puede optimizar la asignación presupuestal en campañas de marketing digital evaluando escenarios de incertidumbre en Meta, TikTok y YouTube (p. 15).

El producto entregado es un prototipo en Google Colab que parametriza presupuesto, distribución por plataforma, modelo de compra (CPC, CPM, CPV), tarifa, CTR, tasa de visualización, frecuencia objetivo, audiencia máxima e incertidumbre, corre simulación Monte Carlo, evalúa distribuciones candidatas y exporta a Excel (pp. 46-47). El modelo está formalizado con ecuaciones, distribuciones, función objetivo y restricciones (Tabla 7, p. 45): la tarifa se perturba con un factor lognormal, CTR y tasa de visualización con normales acotadas, el alcance se limita por audiencia máxima, la función objetivo es `w* = arg max E[Z(w)]` con `Σw_p = 1` y `w_p ≥ 0,05`, y los candidatos se generan con Dirichlet (5.000 distribuciones). La reproducibilidad se apoya en semilla fija SEED = 42 (p. 44).

El insumo empírico es una encuesta estructurada en Google Forms a 50 participantes, 45 registros válidos tras depuración, muestreo no probabilístico por conveniencia (p. 32); las 10 preguntas están transcritas en el Anexo 4 (p. 65) y los resultados en el Anexo 5 (pp. 67-69). Los hallazgos se amarran a decisiones de diseño en una tabla de trazabilidad explícita (Tabla 6, p. 44).

Los resultados son de validación interna controlada: batería de 10 pruebas funcionales, todas «Cumple», con evidencia numérica y mensajes de error (Tabla 8, pp. 51-52); tres escenarios conservador/probable/optimista (Tabla 9, p. 52); comparación del escenario ingresado 40/30/30 contra el recomendado 5,31 % / 88,77 % / 5,92 %, que sube el promedio de clics de 6.902 a 10.441 (+51,28 %) con presupuesto de $10.000.000 (Tabla 10, p. 53); sensibilidad univariada (Tabla 11, p. 54) y convergencia Monte Carlo (Tabla 12, p. 55).

El documento es explícito en lo que no demuestra: la validación es interna, no prueba superioridad en campañas reales, no se operacionalizó la variable «reducción de incertidumbre» (pp. 56-58) y no hubo pruebas con usuarios distintos a los desarrolladores (Anexo 7, p. 71).

*(≈390 palabras)*

---

## 2. Coherencia título → objetivo → resultados

Título, pregunta (p. 15) y objetivo general (p. 16) dicen lo mismo: el verbo techo es **diseñar** un prototipo. El trabajo no solo diseñó: desarrolló y evaluó internamente. No hay inflación de verbo, que es el problema habitual; el riesgo aquí es el inverso, la presentación promete más de lo que el documento sostiene (ver §5).

| Objetivo específico (p. 16) | ¿Se cumplió? | Evidencia | Qué falta |
|---|---|---|---|
| 1. Identificar y justificar las variables de planificación que servirán de parámetros | **Sí** | Tabla 2 de variables (pp. 33-34); Tabla 6 de trazabilidad encuesta → decisión de diseño (p. 44); Anexo 5 con los porcentajes (pp. 67-69) | La encuesta justifica *cuáles* variables, no *qué valores*: las tarifas y métricas siguen siendo «supuestos académicos de referencia» (nota, p. 45) |
| 2. Diseñar el modelo lógico y las fórmulas con escenarios de incertidumbre (CPC, CPM, CPV) | **Sí** | Tabla 7 con las 12 ecuaciones, distribuciones, función objetivo y restricciones (p. 45); diagrama de flujo (Figura 1, p. 34); diccionario de datos (pp. 40-42) | El documento no declara cómo se agrega el alcance entre plataformas ni si hay solapamiento de audiencias (buscado en Tabla 7, p. 45, y diccionario, pp. 40-42) |
| 3. Desarrollar un prototipo funcional en Google Colab que compare alternativas | **Sí** | Figuras 3-5 con código, parámetros y tablero (pp. 47-48); pruebas funcionales (Tabla 8, pp. 51-52); enlace al notebook (p. 70) | El `.ipynb` que la p. 70 dice entregar «junto con este documento» no está en la carpeta compartida con los jurados: solo hay los dos PDF |
| 4. Evaluar el funcionamiento analizando alcance, impresiones, frecuencia, **eficiencia presupuestal** y recomendaciones | **Parcial** | Tablas 9-13 (pp. 52-55); autoevaluación del avance (tabla de trazabilidad, p. 56) | La **eficiencia presupuestal** está definida en el modelo (p. 45) y en el diccionario (p. 41) pero **no aparece con valor en ninguna tabla de resultados** (Tablas 9-11, pp. 52-54). La frecuencia solo aparece en la Tabla 10 (2,27 → 2,21) |

**Balance: 3 de 4 objetivos cumplidos y el cuarto parcial.** Los propios autores califican el objetivo 4 como «cumplido para validación interna controlada» y dejan constancia de que la validación con campañas reales y usuarios externos queda pendiente (p. 56).

---

## 3. Fortalezas verificables

1. **Honestidad epistémica documentada, y no en una línea suelta.** La discusión crítica dice que la validación es interna y que no se demuestra mejor desempeño en campañas reales (p. 56); la conclusión 5 declara que no se confirmó la «reducción de incertidumbre» porque nunca se definió ni midió esa variable (p. 58); el Anexo 7 se niega a atribuir resultados a usuarios que no probaron la herramienta y deja la matriz en blanco (p. 71). Es lo contrario del maquillaje habitual y merece reconocerse en sala.
2. **El modelo está formalizado, no descrito.** Doce ecuaciones con distribuciones, función objetivo, restricciones y método de generación de candidatos (Tabla 7, p. 45), más un diccionario de datos con tipo, unidad, rango, fuente y regla de validación por variable (pp. 40-42). En una especialización profesionalizante esto está por encima del promedio.
3. **Reproducibilidad tratada como requisito.** Semilla fija SEED = 42 con desplazamientos determinísticos, y prueba de que la misma semilla reproduce el mismo resultado y que con incertidumbre = 0 el resultado es idéntico con semillas distintas (p. 44; Tabla 8, p. 52).
4. **Ingeniería de calidad de datos explícita.** Reglas para datos faltantes, valores negativos, distribuciones que no suman 100 %, división por cero y techo de audiencia (pp. 43-44), cada una con su prueba correspondiente que arroja el `ValueError` esperado (Tabla 8, pp. 51-52).
5. **Autocrítica que corrigió el propio producto.** La nota de la Figura 5 admite que esa captura es de una iteración anterior en la que una distribución mayor al 100 % se normalizaba en silencio, y que la validación llevó a endurecer la regla para rechazar la entrada (pp. 48-49). Es trazabilidad de una corrección real.
6. **Justificación de los parámetros de cómputo, no números arbitrarios.** 3.000 simulaciones se sostienen con una prueba de convergencia (desviación de 0,266 % frente a 6.000, Tabla 12, p. 55) y 5.000 candidatas con una prueba de cobertura (Tabla 13, p. 55), advirtiendo que no garantizan el óptimo global.

---

## 4. OBSERVACIONES DEL DOCUMENTO — debilidades y huecos (con página)

1. **La recomendación se elige por el promedio en un trabajo cuyo tema es la incertidumbre.** El escenario recomendado mejora el valor esperado, pero su intervalo p10-p90 pasa de 5.484–8.384 a 7.064–14.228; el propio texto reconoce que «la función actual optimiza el promedio y no penaliza explícitamente el riesgo» (p. 53). Un simulador de escenarios de incertidumbre que decide sin criterio de riesgo tiene ahí su punto débil conceptual.
2. **El óptimo parece estructural, no descubierto.** Con CPC y tarifa constante los clics son proporcionales a la inversión (Tabla 7, p. 45), de modo que maximizar clics tiende a la esquina «todo a la plataforma más barata» hasta el piso `w_p ≥ 0,05`. La Tabla 13 (p. 55) lo insinúa: con 500, 1.000 y 3.000 candidatas el resultado es idéntico (5,14 / 88,39 / 6,47) y con 5.000 casi el mismo. El documento no discute si el modelo tiene rendimientos decrecientes o saturación por plataforma.
3. **Eficiencia presupuestal: indicador prometido y no reportado.** Está en el objetivo 4 (p. 16), en el alcance (p. 19), en la fórmula (p. 45) y en el diccionario (p. 41), pero no tiene valor numérico en las Tablas 9, 10 ni 11 (pp. 52-54).
4. **Agregación del alcance sin declarar.** No se explica cómo se totaliza el alcance de las tres plataformas ni cómo se trata el solapamiento de audiencias (buscado en Tabla 7, p. 45; diccionario, pp. 40-42; resultados, pp. 52-54). Con 88,77 % en una sola plataforma la pregunta es material.
5. **La validación documentada corrió con una sola función objetivo.** El modelo admite maximizar alcance, clics o visualizaciones (Tabla 7, p. 45), pero todas las corridas reportadas —Tablas 10, 12 y 13, pp. 53-55— optimizan **clics**, y así lo dicen la nota de la Tabla 7 y el paso 5 del manual (pp. 45 y 70). De las otras dos funciones objetivo no hay ni una corrida en las 71 páginas: el alcance aparece como indicador de salida en la Tabla 10, no como criterio de optimización.
6. **Evidencia del código no verificable en la carpeta.** La p. 70 anuncia el archivo `Prototipo_Validacion_Completa_Ejecutado.ipynb` entregado con el documento, y la carpeta del grupo solo contiene los dos PDF; el enlace de Colab de la p. 70 advierte que el acceso depende de permisos.
7. **Restos de plantilla y numeración descuidada** (no se pregunta en sala, se anota): campos de índice de Word sin actualizar en el Anexo, con la cadena `TOC \h \u \z \t "Heading 1,1…"` y el mensaje «No se encontraron entradas de tabla de contenido» (p. 60); falta el **Anexo 2** (el índice salta de Anexo 1 a Anexo 3, p. 3); numeración repetida de tablas (dos «Tabla 6», pp. 40 y 44; dos «Tabla 12», pp. 55 y 56, cuando la lista anuncia Tabla 14 para la segunda, p. 4); dos «Figura 8» seguidas (pp. 50 y 51) y una lista de figuras que se detiene en la Figura 8 mientras el cuerpo llega a la Figura 11 (p. 5 vs. p. 56); numeración de capítulos con el «2» usado dos veces (Planteamiento, p. 14, y Objetivos, p. 16) y subsecciones 1.1-1.3 dentro del capítulo 2 (p. 14); tiempos verbales en futuro heredados del anteproyecto («se aplicarán», «se seleccionarán», p. 33; «El prototipo estará orientado», p. 27; «será desarrollado mediante autogestión académica», p. 63); errata de fondo en la p. 15, «pueden incrementar la probabilidad de decisiones optimas», donde el sentido pedía lo contrario.
8. **Integridad: no se declara reporte de similitud.** Buscado «Turnitin» y «similitud» en las 71 páginas: sin resultados. Tampoco hay declaración de uso de IA generativa, aunque el presupuesto contempla «Herramientas de IA, almacenamiento o nube» por $300.000 (p. 64). No es una acusación: es un requisito de la rúbrica de integridad que le corresponde verificar al metodólogo.

---

## 5. OBSERVACIONES DE LAS DIAPOSITIVAS — qué proyectan y en qué se separan del documento

**Mazo:** `Presentación Final 25ET1 - Proyecto-Seminario II - Grupo 12.pptx.pdf` — **19 diapositivas** (1 portada · 2-6 introducción, problema, objetivos y marco · 7-10 metodología y encuesta · 11-13 herramienta, pruebas y resultado · 14-16 escenarios · 17 conclusiones · 18 referencias · 19 «Preguntas»). Es el mazo mejor amarrado a su documento de la jornada: los porcentajes de la encuesta y las nueve fuentes de la bibliografía se rastrean página por página. Lo que se separa está concentrado en cuatro diapositivas —13, 14-16 y 17—, y el antídoto de la 17 está en su propia diapositiva 5. Las preguntas que nacen de aquí están en la §6, en el banco de reserva, bajo **«De las diapositivas»**.

1. **Las diapositivas 14, 15 y 16 no traen ni un número: traen la orden de correr el Colab en vivo.** Cada una narra un caso —María, cosméticos sostenibles, $12.000.000, 40/40/20, «Objetivo en el Colab: **Maximizar Alcance**»; Carlos, e-commerce de moda en CyberWeek, $8.000.000, 50/30/20, «Maximizar Clics»; Andrea, cadena de gimnasios, $15.000.000, 20/30/50, «Maximizar Visualizaciones»— y **ninguna muestra resultado**. Los tres casos no existen en el documento, cuyas corridas cubren solo $10.000.000 con 40/30/30 (Tablas 9-13, pp. 52-55). Esto cambia lo que hay que hacer en sala: **si abren el notebook y lo ejecutan, es el mejor momento de la sustentación** —resuelve de una vez las dos funciones objetivo que el documento nunca corrió (§4, ítem 5) y suple el `.ipynb` que no está en la carpeta de los jurados—; **si solo leen la historia y pasan de largo, ahí entra la reserva 4**.
2. **La diapositiva 13 es la única con resultados, y solo proyecta promedios.** 6.902 clics del plan ingresado contra 10.441 del recomendado y «+51,28 % más clics con el mismo dinero». **El intervalo p10-p90 no aparece en ninguna de las 19 diapositivas:** en pantalla, un trabajo sobre incertidumbre reporta una media. El documento sí lo trae —5.484–8.384 en el ingresado, 7.064–14.228 en el recomendado (p. 53)—. Es el sostén visual de la pregunta prioritaria 1: la dispersión que se abre no se ve.
3. **Pero la 13 sí matiza, y hay que reconocérselo.** Cierra con «Esta mejora demuestra la **capacidad matemática del modelo** para redistribuir el presupuesto según la meta del usuario», que es casi la frase de la p. 53 —«coherencia interna con la función objetivo, no superioridad empírica en campañas reales»—. Lo que falta en pantalla es la segunda mitad, no la primera. **No entrar acusando a la 13 de vender el +51,28 % a secas:** se pregunta por lo que le falta, y con la propia frase de ellos delante.
4. **La contradicción está dentro del mazo: diapositiva 5 contra diapositiva 17.** La 5 declara «Limitaciones clave: **no integra APIs, datos en tiempo real ni campañas reales**. La validación se realiza con escenarios simulados y análisis documental». La 17 concluye que «la herramienta **supera los enfoques deterministas tradicionales**» y que «la organización logra una asignación de recursos más eficiente… **optimiza el retorno proyectado** de la inversión antes de la ejecución del gasto». Conviene preguntarlo con la 5 en la mano antes que con la conclusión 5 del documento (p. 58): la refutación es suya y está proyectada doce diapositivas antes.
5. **La eficiencia presupuestal se promete en tres diapositivas y no se reporta en ninguna.** Está en la 2 («fortalecer la eficiencia presupuestal»), en el objetivo específico 4 de la 4 y en los conceptos clave de la 6 — y no hay ni una cifra suya en el mazo, igual que no la hay en las Tablas 9-11 (pp. 52-54). La pregunta prioritaria 3 se puede abrir por su propia diapositiva 4 en vez de por el folio 16.
6. **La diapositiva 12 exagera su propio dato.** Dice que con 3.000 simulaciones «el resultado es tan preciso como con 6.000, pero **tarda la mitad del tiempo** (menos de 0,02 segundos)». Su Tabla 12 (p. 55) mide 0,0060 s con 3.000 y 0,0084 s con 6.000: es un 29 % menos, no la mitad. El «menos de 0,02 s» sí cuadra con la p. 56 (0,0102 s la simulación y 0,0146 s la evaluación de candidatas). Se anota con la forma (§9); **no se pregunta**: sería cambiar un hueco conceptual por una décima.
7. **Lo que sí está trazable, y conviene decirlo en voz alta.** Los tres 44,4 % y el 62,2 % de la diapositiva 9 son exactamente los de las notas del Anexo 5 (pp. 67-69); la tabla de trazabilidad encuesta → diseño de la 10 es la Tabla 6 (p. 44); el marco referencial de la 6 —racionalidad limitada de Simon (1997), teoría de la decisión de Clemen & Reilly (2014), simulación organizacional de Banks et al. (2015)— está citado en el cuerpo (pp. 23, 11-25 y 22-24); las nueve referencias de la 18 están todas en la lista de las pp. 58-59; y el título de la portada es palabra por palabra el del trabajo. En una jornada donde varios mazos dicen cosas que su documento no tiene, esto pesa a favor.

### Qué mirar en pantalla mientras exponen

- **Si el Colab aparece corriendo** (diapositivas 14-16): mirar el bloque de parámetros —tarifas, CTR, audiencia máxima— y comprobar si son los del caso reportado (Figura 4) o los de las Figuras 5 y 8, que son otros. Ahí se resuelve sola la pregunta 3.
- **La baldosa «Eficiencia /100K»** del tablero, si se proyecta: si sale con valor, la pregunta 3 pasa de reparo a confirmación y se hace en un tono distinto.
- **Si en la 13 aparece algo más que promedios** —una barra de rango, un p10, una desviación—: la pregunta 1 se abre reconociéndolo, no señalándolo.
- **Quién expone la 11 y la 12.** Son las dos diapositivas técnicas del mazo (flujo de datos y racionalidad del sistema). Si las lee la misma persona que todo lo demás, ahí va la petición de que otro integrante explique la Tabla 7 (p. 45).
- **Si la 17 se lee tal cual está escrita:** no interrumpir; anotar la frase textual y devolvérsela con su diapositiva 5.

---

## 6. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. El criterio de decisión: promedio o riesgo.**
> «La fila “ranking” de la tabla de arquitectura de datos del folio 40 ordena las distribuciones por clics promedio, y el párrafo que cierra el apartado 8.3, en el folio 53, dice que la función objetivo no penaliza el riesgo: el promedio sube de 6.902 a 10.441 clics mientras el intervalo p10-p90 se abre de 5.484–8.384 a 7.064–14.228. Si un director de agencia les pide hoy una recomendación, ¿entregan la que maximiza el promedio o la que protege el p10? Elijan una.»
- **Sale de:** el **documento** —la tabla de arquitectura de datos del folio 40, fila «ranking», y el párrafo que cierra el 8.3 con el p10-p90 (p. 53)—, y la **diapositiva 13** la refuerza por omisión: proyecta las dos medias, 6.902 y 10.441, y ningún intervalo (§5, ítem 2).
- **Por qué:** es el corazón conceptual del trabajo. El proyecto se llama «evaluación de escenarios de incertidumbre» y decide con un estadístico que ignora la incertidumbre. Cerrar la pregunta en «elijan una» impide la respuesta de manual —«depende del perfil del cliente»— que consume el minuto sin comprometerse. **Al citar en voz alta hay que decir «la tabla de arquitectura de datos del folio 40, fila ranking»: nunca «Tabla 5»**, porque la lista de tablas le asigna ese número al diccionario de datos y la tabla del folio 40 no lleva título. Y el intervalo p10-p90 se atribuye al párrafo de cierre del 8.3, no a la Tabla 10, que no tiene columna p10.
- **Resuelve:** elegir una de las dos, distinguir la aversión al riesgo del planeador y proponer el p10 o la media menos una penalización por dispersión como criterio alternativo —lo que ya anticipan en el folio 53 y en las recomendaciones, p. 58—, reconociendo que la recomendación actual es válida para un decisor neutral al riesgo.
- **Agrava:** decir que el promedio basta, no poder explicar qué significa p10-p90, o quedarse en el «depende» sin elegir.

**2. Por qué el óptimo siempre es TikTok.**
> «Con tres plataformas y su restricción w_p ≥ 0,05 de la Tabla 7, página 45, ¿cuál es el porcentaje máximo que su modelo permite darle a TikTok? Dígame el número.»
- **Sale de:** el **documento** —restricciones y linealidad en CPC de la Tabla 7 (p. 45) y la Tabla 13, donde 500, 1.000 y 3.000 candidatas dan el mismo 5,14 / 88,39 / 6,47 (p. 55)—. En el **mazo** el dato está en la diapositiva 13, que proyecta el reparto recomendado 5,3 / 88,8 / 5,9 sin decir que el 88,8 es el techo de su propia restricción.
- **Por qué:** la respuesta es 90 %, y en cuanto la dicen ellos mismos, el 88,77 % de su resultado deja de ser un hallazgo sobre TikTok y se ve como lo que es: el techo de su propia restricción. Hacerles calcular el techo es más eficaz que enunciárselo, y cabe en veinte segundos. La linealidad se sostiene con las filas de CPM y de Restricciones de la Tabla 7 (p. 45), **no con la Tabla 11**, que varía el presupuesto total y no la mezcla. La pregunta también queda blindada contra su propia Nota a la Tabla 13, que ya admite no afirmar que la búsqueda aleatoria garantice el óptimo global.
- **Resuelve:** dar el 90 % y sacar la conclusión sin ayuda: el resultado es la esquina del conjunto factible. Suma reconocer la linealidad en CPC, señalar que con alcance el techo de audiencia `Amax` sí hace el problema no trivial (p. 45) y admitir que no se modelaron saturación ni rendimientos decrecientes por plataforma.
- **Agrava:** no poder calcular el techo con su propia restricción a la vista; atribuirle al optimizador un aprendizaje o una inteligencia que no tiene; o presentar el 88,77 % como un hallazgo de mercado sobre TikTok.

**3. La eficiencia presupuestal que el objetivo 4 promete y el capítulo 8 no reporta.**
> «Su objetivo 4 nombra la eficiencia presupuestal como indicador a analizar. Los tableros de las Figuras 5 y 8, folios 48 y 50, la muestran, pero con otros parámetros —Meta a CPM 2.000 y TikTok a CPC 1.500, frente a los 18.000 y 14.000 de la Figura 4— y el capítulo 8 no trae ninguna figura. ¿Cuánto vale la eficiencia presupuestal en el caso de la Tabla 10, los diez millones repartidos 40/30/30, en el escenario ingresado y en el recomendado? Dígannos los dos números.»
- **Sale de:** el **documento** —objetivo 4 (p. 16), alcance (p. 19), fórmula (p. 45), diccionario (p. 41), y ni un valor en las Tablas 9-11 (pp. 52-54); sí dentro de las imágenes, folios 48 y 50— y también del **mazo**, que promete el indicador tres veces (diapositivas 2, 4 y 6) y no lo muestra en ninguna de las 19 (§5, ítem 5). Si en sala se proyecta la baldosa «Eficiencia /100K», la pregunta cambia de tono.
- **Por qué:** el indicador está comprometido en el objetivo 4 (p. 16) y no aparece en las Tablas 9, 10 ni 11 (pp. 52-54). La premisa hay que decirla así y no «la eficiencia no vuelve a aparecer después del folio 47»: sí reaparece, pero dentro de las imágenes —el código `eficiencia_100k_promedio` del folio 48, la baldosa «Eficiencia /100K 2.4K» de la Figura 5 y las de 8.9K y 15.4K de la Figura 8, folio 50—, y con parámetros distintos de los del caso reportado. Si la premisa se enuncia mal, la respuesta es «está en la Figura 5» y la pregunta se pierde.
- **Resuelve:** dar los dos números —del orden de 2.387 usuarios por cada $100.000 en el escenario ingresado y 3.227 en el recomendado— o decir con franqueza que el indicador quedó calculado en el prototipo y sin llevar a las tablas del capítulo 8, que es un reparo de forma y no de fondo.
- **Agrava:** remitir a la Figura 5 sin advertir que sus parámetros son otros, o improvisar una cifra que no cuadre con los clics y el alcance de la Tabla 10.

### Banco de reserva

#### Del documento

5. «El alcance total de la Tabla 10, ¿es la suma del alcance de las tres plataformas? Si lo es, ¿cómo tratan el solapamiento de audiencias entre Meta, TikTok y YouTube?» (p. 53; el documento no lo declara)
7. «Las tarifas, el CTR y las audiencias son supuestos académicos de referencia. ¿De dónde sacaría un planeador esos valores calibrados y cuánto podría cambiar la recomendación al hacerlo?» (nota, p. 45; recomendaciones, p. 58)
8. «¿Qué audiencia máxima configuraron por plataforma y qué pasa con la recomendación si el techo de TikTok se vuelve restrictivo?» (fórmula de alcance, p. 45)
9. «Su encuesta es muestreo por conveniencia con 45 registros válidos. ¿Qué decisión de diseño habrían cambiado si el resultado hubiera sido el contrario?» (p. 32) — pregunta para que muestren criterio, no para castigar la muestra.
10. «La p. 70 dice que el notebook se entrega junto con el documento, pero en la carpeta compartida con los jurados solo están los dos PDF. ¿Dónde podemos verificar el código?» *(No pedir que lo abran en sala: el archivo no está en la carpeta de los jurados y la pregunta solo busca dónde queda registrado. Si lo corren en vivo en las diapositivas 14-16, esta pregunta ya no se hace.)*

#### De las diapositivas

Estas dos solo se hacen **si la diapositiva sale en pantalla**. Los números de reserva no se reordenaron —la hoja de respuestas los cita— así que van fuera de secuencia a propósito.

4. «Sus diapositivas 14, 15 y 16 plantean tres casos —doce, ocho y quince millones— con objetivos de alcance, clics y visualizaciones, y la línea “Objetivo en el Colab”. La nota de su Tabla 7 y el paso 5 de su manual dicen que la validación documentada usó clics. ¿Ejecutaron el simulador maximizando alcance y visualizaciones, y dónde quedó registrada esa corrida?» (pp. 45 y 70 contra diapositivas 14-16, que no traen ningún resultado; las corridas del documento cubren solo $10.000.000 con 40/30/30, pp. 52-55). *(Si lo corren en vivo, la pregunta se convierte en un elogio: pedir que dejen a la vista los parámetros de tarifa y audiencia máxima.)*
6. «Su conclusión 5 dice que no se confirmó ninguna reducción de incertidumbre y su propia diapositiva 5 declara que no hay campañas reales; su diapositiva 17 dice que la herramienta supera los enfoques deterministas y optimiza el retorno proyectado. ¿Cuál de las dos sostienen hoy ante nosotros?» (p. 58 y diapositiva 5, contra diapositiva 17)

---

## 7. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si no ejecutan nada en vivo y solo muestran capturas** → pedir que expliquen la nota de la Figura 5: por qué esa captura corresponde a una versión que normalizaba automáticamente una distribución mayor al 100 % y qué cambió después de la validación (pp. 48-49).
- **Si presentan los casos de María, Carlos o Andrea con cifras concretas** → las diapositivas 14-16 no traen ninguna: o las corrieron en vivo —y entonces es lo mejor de la tarde— o salieron de una corrida que el documento no registra. Preguntar cuál de las dos, dado que los resultados del documento cubren solo $10.000.000 con 40/30/30 (pp. 52-55).
- **Si dicen «+51,28 % más clics con el mismo dinero» y se quedan en la primera mitad de su diapositiva 13** → devolverles su propia línea de cierre, «capacidad matemática del modelo para redistribuir el presupuesto», y pedir la segunda mitad, la de la p. 53: «coherencia interna con la función objetivo, no superioridad empírica en campañas reales». Es una oportunidad, no una trampa: si la sostienen bien, sube.
- **Si afirman que validaron con agencias, clientes o usuarios** → contrastar con el Anexo 7, que declara que no hubo pruebas ejecutadas por personas distintas a los desarrolladores (p. 71).
- **Si mencionan inteligencia artificial o aprendizaje automático como parte del simulador** → recordar que la limitación declarada dice que no incorpora modelos de machine learning ni IA (p. 20) y preguntar qué es exactamente lo que aprende el modelo.
- **Si hablan de «reducir la incertidumbre» como logro alcanzado** → pedirles cómo medirían esa reducción, dado que su conclusión 5 dice que la variable no se definió ni se midió (p. 58).
- **Si el tiempo se les va en el marco teórico y saltan los resultados** → ir directo a la Tabla 10 (p. 53): qué distribución recomendó el simulador y por qué.
- **Si solo hablan uno o dos de los cuatro** → pedir explícitamente a otro integrante que explique la Tabla 7 (p. 45): qué representa el factor lognormal de la tarifa y por qué se eligió esa distribución. Es la vía legítima para verificar dominio individual.
- **Si contestan el 90 % en la pregunta 2** → cerrar el círculo: «entonces su 88,77 % no es un hallazgo sobre TikTok, es el techo que fija su propia restricción: ¿qué tendría que incorporar el modelo para que el óptimo no fuera siempre esa esquina?».
- **Si invocan la Nota de su Tabla 13** para sostener que la búsqueda aleatoria encuentra el óptimo → leerles su propia nota, que dice lo contrario, y aceptarlo como punto a favor de la honestidad del documento: la pregunta 2 no depende de esa nota.
- **Si responden bien las tres prioritarias y sobra tiempo** → preguntar por las corridas de alcance y visualizaciones que la presentación anuncia y el documento no registra (reserva 4), que es el hueco más limpio entre el documento y las diapositivas.

---

## 8. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado: dominio · claridad · coherencia del documento · capacidad de defensa)

- **4,6–5,0 (excelente; solo aquí tiene sentido pensar en meritoria).** Necesito ver dos cosas juntas: (a) que expliquen el compromiso entre valor esperado y dispersión y propongan un criterio de decisión que incorpore el riesgo, sin que yo se lo sugiera (p. 53); y (b) que reconozcan la estructura del óptimo —por qué la recomendación se va a la plataforma más barata— y qué tendría que cambiar en el modelo. Sumado a que el producto se vea funcionando y a que los cuatro integrantes hablen de su parte. La honestidad del documento (pp. 56-58, 71) ya juega a favor.
- **3,6–4,5 (buen desempeño; es donde este trabajo llega por defecto).** Documento coherente, modelo formalizado, prototipo existente y limitaciones declaradas. Se queda en 4,0–4,4 si defienden el prototipo pero no logran explicar por qué el optimizador siempre elige TikTok, si no muestran el sistema corriendo, o si leen las diapositivas. Sube a 4,5 si contestan dos de las tres preguntas prioritarias con solvencia.
- **3,0–3,5 (aceptable).** Si sostienen en sala el discurso de la diapositiva 17 —que la herramienta «supera los enfoques deterministas» y mejora el retorno— contradiciendo su propia conclusión 5 (p. 58), o si presentan el +51,28 % como evidencia de campañas reales. El documento vale más que esa defensa y sería una lástima.
- **0,1–2,9 (insuficiente).** Solo si no pueden explicar las fórmulas de su propia Tabla 7 (p. 45), o si atribuyen resultados a usuarios, clientes o campañas que el Anexo 7 declara inexistentes (p. 71).

**Rango que hoy anticipo, antes de escuchar: 4,3–4,6** (no es una nota sugerida: la nota la pongo yo en sala contra estos umbrales). Es un trabajo por encima del promedio en formalización y honestidad, con dos huecos conceptuales reales (criterio de riesgo y estructura del óptimo) y defectos de forma que no son de fondo. Recordar que mi voto es una cuarta parte compartida con el Jurado 1: no apruebo ni repruebo, valido.

---

### 8.1 Formulario oficial del jurado — 5 criterios en escala 1–5

> **Instrumento distinto de los cuatro criterios de arriba.** Son las cinco preguntas del formulario que la Dirección le pide al jurado, cada una con opciones **1 2 3 4 5**. **Ninguna califica la sustentación oral:** las cinco se responden con el documento, así que van precargadas con la página que las sostiene y en sala solo se confirman.
>
> Lectura de la escala, fijada de antemano: **5** sobresaliente, sin reparos de fondo · **4** sólido, con reparos menores y declarados · **3** aceptable, con un reparo de fondo que el documento no resuelve · **2** deficiente: hay material, pero se contradice o no sostiene lo que afirma · **1** sin base verificable en el documento.
>
> ⚠️ **Este 1–5 no es la nota del acta.** La nota que se reporta sale de los cuatro criterios y de los umbrales de esta §8. La casilla del formulario la marca el jurado humano; esto es una propuesta con página.

**1. Planteamiento de la problemática y formulación de objetivos** — propuesto **4** / 5

> Claridad, pertinencia y delimitación del problema de investigación, así como la coherencia y precisión de los objetivos propuestos, verificando su alineación con el propósito del estudio y su viabilidad investigativa.

Título, pregunta (p. 15) y objetivo general (p. 16) dicen lo mismo y el verbo techo es **«diseñar»**: el trabajo no infla el alcance, lo supera —diseñó, desarrolló y evaluó internamente—. El problema parte de un diagnóstico sectorial con fuentes actuales (p. 14). No llega a 5 porque el objetivo 4 nombra la **eficiencia presupuestal** como indicador a analizar y ese indicador no aparece con valor en ninguna tabla de resultados (pp. 16, 19, 41, 45 frente a pp. 52-54).

**2. Marco teórico y referentes conceptuales** — propuesto **3** / 5

> Solidez del sustento teórico del proyecto, la pertinencia y actualidad de las fuentes consultadas, y la capacidad de articular conceptos, enfoques y antecedentes que fundamenten adecuadamente la investigación.

Tiene las fuentes más actuales del cohorte —Gartner 2022, IAB & PwC 2024, WARC 2024 (p. 14)— y eso cuenta, igual que el marco referencial sí construido: racionalidad limitada de Simon (1997, p. 23), teoría de la decisión de Clemen & Reilly (2014, citada en pp. 11, 14, 17, 19, 21, 23 y 25) y simulación organizacional de Banks et al. (2015, pp. 22-24), los tres además proyectados en la diapositiva 6. Lo que lo deja en 3 es que **esa teoría de la decisión no se usa para elegir criterio**: en las 71 páginas no aparece ni una fuente de decisión bajo riesgo aplicada —media-varianza, VaR/CVaR, optimización robusta— ni las palabras «aversión al riesgo», «varianza» o «portafolio» (buscadas: cero resultados). De ahí sale el hueco conceptual del criterio 4: optimizar el promedio en un trabajo cuyo tema es la incertidumbre.

**3. Metodología, muestra y coherencia del diseño** — propuesto **4** / 5

> Correspondencia entre el enfoque metodológico, el tipo de estudio, las técnicas e instrumentos de recolección de información y la definición de la muestra, garantizando la coherencia interna del diseño investigativo.

Es la formalización más sólida de la jornada: **12 ecuaciones con distribuciones, función objetivo y restricciones** (Tabla 7, p. 45), diccionario de datos con tipo, unidad, rango, fuente y regla de validación por variable (pp. 40-42), reglas de calidad de datos con su prueba correspondiente (pp. 43-44, 51-52), **reproducibilidad tratada como requisito** con semilla fija SEED = 42 (p. 44) y parámetros de cómputo justificados con pruebas de convergencia y de cobertura, no elegidos a dedo (Tablas 12-13, p. 55). La encuesta (50 aplicadas, 45 válidas, conveniencia, p. 32) está transcrita (Anexo 4, p. 65) y **amarrada a decisiones de diseño en una tabla de trazabilidad** (Tabla 6, p. 44). No llega a 5 porque tarifas, CTR y audiencias son «supuestos académicos de referencia» (nota, p. 45) y la agregación del alcance entre plataformas —con 88,77 % en una sola— no se declara.

**4. Resultados y conclusiones** — propuesto **4** / 5

> Calidad en la presentación, interpretación y análisis de los resultados obtenidos, así como la consistencia y pertinencia de las conclusiones en relación con los objetivos, la problemática y el marco teórico del estudio.

Batería de 10 pruebas funcionales con evidencia numérica y mensajes de error (Tabla 8, pp. 51-52), tres escenarios (Tabla 9), comparación 40/30/30 frente al recomendado con +51,28 % (Tabla 10, p. 53), sensibilidad univariada y convergencia Monte Carlo. Y una **honestidad epistémica que hay que reconocer en sala**: la discusión declara que la validación es interna y no prueba superioridad en campañas reales (pp. 56-57), la conclusión 5 admite que la «reducción de incertidumbre» nunca se definió ni se midió (p. 58) y el Anexo 7 deja la matriz en blanco antes que atribuir resultados a usuarios que no probaron la herramienta (p. 71). Lo que impide el 5: la eficiencia presupuestal prometida no se reporta, y **la diapositiva 17 afirma lo contrario de la conclusión 5 y de su propia diapositiva 5** —«supera los enfoques deterministas», «optimiza el retorno proyectado»—, con tres casos (12, 8 y 15 millones) que no existen en el documento y que las diapositivas 14-16 dejan sin resultado. La diapositiva 13 sí cierra hablando de «capacidad matemática del modelo», que es la mitad correcta del matiz.

**5. Pertinencia disciplinar y articulación con la especialización** — propuesto **4** / 5

> Grado de alineación del proyecto con el campo disciplinar y los énfasis de la especialización cursada, así como su aporte potencial al desarrollo académico, profesional o investigativo del área.

Simulación Monte Carlo para asignar presupuesto de pauta en Meta, TikTok y YouTube, con prototipo ejecutable en Colab: encaja en «Mejoramiento de procesos organizacionales» y el aporte metodológico es transferible. No llega a 5 porque el notebook que la p. 70 dice entregar no está en la carpeta compartida con los jurados y el criterio de decisión no incorpora riesgo.

**Suma propuesta: 19 / 25.**

**Qué subiría una casilla en sala:** El **criterio 2 pasa a 4** y el **criterio 4 a 5** con la misma respuesta: que expliquen el compromiso entre valor esperado y dispersión —el p10-p90 se abre de 5.484-8.384 a 7.064-14.228 (p. 53)— y propongan un criterio que incorpore el riesgo **sin que nadie se lo sugiera** (pregunta prioritaria 1). El **criterio 3 pasa a 5** si reconocen la estructura del óptimo: por qué con CPC constante la recomendación se va siempre a la plataforma más barata hasta el piso del 5 % (pregunta 2).

**Qué la bajaría:** El **criterio 4 baja a 3** si sostienen en sala el discurso de la diapositiva 17 contradiciendo su propia conclusión 5, o si presentan el +51,28 % como evidencia de campañas reales. El **criterio 1 baja a 3** si atribuyen al optimizador un aprendizaje que no tiene. Son cuatro integrantes: pedir que responda quien no expuso.

## 9. Observaciones administrativas (no académicas)

1. **Equipo de cuatro integrantes** (portada, p. 1, y firmas, pp. 8-9), cuando el máximo en Proyecto I/II de especialización es de tres. Es una observación para la Dirección del Programa, **no** un criterio para bajar la nota del trabajo.
2. **El nombre del archivo de la presentación conserva el periodo anterior:** «Presentación Final **25ET1** – Proyecto-Seminario II – Grupo 12». La portada interna sí está correcta y no dice periodo. Cosmético, pero conviene que lo corrijan antes de radicar.
3. **El notebook no está en la carpeta compartida con los jurados.** La p. 70 anuncia `Prototipo_Validacion_Completa_Ejecutado.ipynb` como entregado junto con el documento; la carpeta `26ET2-G-012` solo contiene los dos PDF. Puede estar radicado en el aula: vale confirmarlo con la Dirección antes de la sala para no preguntar por algo que sí entregaron por otro canal.
4. **No se declara reporte de similitud (Turnitin) ni porcentaje** en ninguna de las 71 páginas, ni hay declaración de uso de IA generativa. Corresponde a la verificación del metodólogo, no al jurado; lo dejo anotado porque pesa 15 % en la rúbrica de integridad.
5. **Ética y datos personales:** el documento sí incluye una nota de tratamiento de datos, resultados agregados y no identificación individual de los participantes (p. 61). No declara consentimiento informado explícito del instrumento, lo cual es admisible en este nivel para una encuesta anónima de opinión profesional.
6. **Dato de mi propio alistamiento, no del grupo:** el JSON de preparación solo registró la asignación del martes 18 (6:00-9:00 p.m., 9 proyectos). Verifiqué en la hoja `CRONOGRAMA` del cronograma 26ET2 (fila 10) que la segunda sesión, **miércoles 19 de agosto de 6:00 a 7:20 p.m. con 4 proyectos**, pertenece al mismo panel; por eso este grupo me corresponde igualmente como Jurado 2. Si alguien reutiliza ese JSON, tenerlo en cuenta.
