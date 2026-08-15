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

Título, pregunta (p. 15) y objetivo general (p. 16) dicen lo mismo: el verbo techo es **diseñar** un prototipo. El trabajo no solo diseñó: desarrolló y evaluó internamente. No hay inflación de verbo, que es el problema habitual; el riesgo aquí es el inverso, la presentación promete más de lo que el documento sostiene (ver §4).

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

## 4. Debilidades y huecos (con página)

1. **La recomendación se elige por el promedio en un trabajo cuyo tema es la incertidumbre.** El escenario recomendado mejora el valor esperado, pero su intervalo p10-p90 pasa de 5.484–8.384 a 7.064–14.228; el propio texto reconoce que «la función actual optimiza el promedio y no penaliza explícitamente el riesgo» (p. 53). Un simulador de escenarios de incertidumbre que decide sin criterio de riesgo tiene ahí su punto débil conceptual.
2. **El óptimo parece estructural, no descubierto.** Con CPC y tarifa constante los clics son proporcionales a la inversión (Tabla 7, p. 45), de modo que maximizar clics tiende a la esquina «todo a la plataforma más barata» hasta el piso `w_p ≥ 0,05`. La Tabla 13 (p. 55) lo insinúa: con 500, 1.000 y 3.000 candidatas el resultado es idéntico (5,14 / 88,39 / 6,47) y con 5.000 casi el mismo. El documento no discute si el modelo tiene rendimientos decrecientes o saturación por plataforma.
3. **Eficiencia presupuestal: indicador prometido y no reportado.** Está en el objetivo 4 (p. 16), en el alcance (p. 19), en la fórmula (p. 45) y en el diccionario (p. 41), pero no tiene valor numérico en las Tablas 9, 10 ni 11 (pp. 52-54).
4. **Agregación del alcance sin declarar.** No se explica cómo se totaliza el alcance de las tres plataformas ni cómo se trata el solapamiento de audiencias (buscado en Tabla 7, p. 45; diccionario, pp. 40-42; resultados, pp. 52-54). Con 88,77 % en una sola plataforma la pregunta es material.
5. **Brecha documento ↔ presentación.** La diapositiva 13 vende «+51,28 % más clics con el mismo dinero» sin la advertencia que el documento sí trae («no constituye evidencia de superioridad en campañas reales», p. 53 y p. 57), y la diapositiva 17 afirma que «la herramienta supera los enfoques deterministas tradicionales» y que «la organización logra una asignación de recursos más eficiente… optimiza el retorno proyectado», cuando la conclusión 5 del documento dice exactamente que eso no se demostró (p. 58). Las diapositivas 14-16 introducen tres casos ($12.000.000, $8.000.000 y $15.000.000) que no existen en el documento, cuyos resultados solo cubren el caso de $10.000.000 con 40/30/30 (pp. 52-55).
6. **Solo un objetivo de optimización fue validado.** La nota de la Tabla 7 y el paso 5 del manual dicen que la validación documentada usó clics (pp. 45 y 70); la presentación anuncia maximizar alcance (diapositiva 14) y visualizaciones (diapositiva 16), sin registro de esas corridas.
7. **Evidencia del código no verificable en la carpeta.** La p. 70 anuncia el archivo `Prototipo_Validacion_Completa_Ejecutado.ipynb` entregado con el documento, y la carpeta del grupo solo contiene los dos PDF; el enlace de Colab de la p. 70 advierte que el acceso depende de permisos.
8. **Restos de plantilla y numeración descuidada** (no se pregunta en sala, se anota): campos de índice de Word sin actualizar en el Anexo, con la cadena `TOC \h \u \z \t "Heading 1,1…"` y el mensaje «No se encontraron entradas de tabla de contenido» (p. 60); falta el **Anexo 2** (el índice salta de Anexo 1 a Anexo 3, p. 3); numeración repetida de tablas (dos «Tabla 6», pp. 40 y 44; dos «Tabla 12», pp. 55 y 56, cuando la lista anuncia Tabla 14 para la segunda, p. 4); dos «Figura 8» seguidas (pp. 50 y 51) y una lista de figuras que se detiene en la Figura 8 mientras el cuerpo llega a la Figura 11 (p. 5 vs. p. 56); numeración de capítulos con el «2» usado dos veces (Planteamiento, p. 14, y Objetivos, p. 16) y subsecciones 1.1-1.3 dentro del capítulo 2 (p. 14); tiempos verbales en futuro heredados del anteproyecto («se aplicarán», «se seleccionarán», p. 33; «El prototipo estará orientado», p. 27; «será desarrollado mediante autogestión académica», p. 63); errata de fondo en la p. 15, «pueden incrementar la probabilidad de decisiones optimas», donde el sentido pedía lo contrario.
9. **Integridad: no se declara reporte de similitud.** Buscado «Turnitin» y «similitud» en las 71 páginas: sin resultados. Tampoco hay declaración de uso de IA generativa, aunque el presupuesto contempla «Herramientas de IA, almacenamiento o nube» por $300.000 (p. 64). No es una acusación: es un requisito de la rúbrica de integridad que le corresponde verificar al metodólogo.

---

## 5. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. El criterio de decisión: promedio o riesgo.**
> «En su Tabla 10 la distribución recomendada sube el promedio de clics de 6.902 a 10.441, pero el intervalo p10-p90 se abre de 5.484–8.384 a 7.064–14.228, y ustedes mismos escriben que la función objetivo no penaliza el riesgo. Si un director de agencia les pide una recomendación con ese resultado en la mano, ¿le entregan la distribución que maximiza el promedio o la que protege el p10, y con qué argumento?»
- **Por qué:** es el corazón conceptual del trabajo. El proyecto se llama «evaluación de escenarios de incertidumbre» y decide con un estadístico que ignora la incertidumbre (p. 53).
- **Resuelve:** distinguir aversión al riesgo del planeador, proponer el p10 o media menos penalización por dispersión como criterio alternativo —lo que ya anticipan en la p. 53 y en las recomendaciones, p. 58—, y reconocer que la recomendación actual es válida para un decisor neutral al riesgo.
- **Agrava:** decir que el promedio basta, o no poder explicar qué significa p10-p90.

**2. Por qué el óptimo siempre es TikTok.**
> «Con CPC y tarifa constante, los clics crecen proporcionalmente a la inversión, y su Tabla 13 muestra que con 500, 1.000 o 3.000 distribuciones candidatas el óptimo es el mismo 88 % en TikTok. ¿Qué aporta entonces evaluar 5.000 distribuciones, y qué tendría que incorporar el modelo para que la recomendación no fuera siempre "todo a la plataforma más barata con el 5 % mínimo en las otras"?»
- **Por qué:** Tabla 7 (p. 45) y Tabla 13 (p. 55). Si el resultado es la esquina del conjunto factible, el optimizador no está descubriendo nada y conviene que ellos lo digan antes de que lo diga el jurado.
- **Resuelve:** reconocer la linealidad en CPC, señalar que con alcance el techo de audiencia `Amax` sí hace el problema no trivial (p. 45), y admitir que no se modelaron saturación ni rendimientos decrecientes por plataforma.
- **Agrava:** atribuirle al optimizador un aprendizaje o una inteligencia que no tiene, o presentar el 88,77 % como un hallazgo de mercado sobre TikTok.

**3. Los objetivos de optimización que la presentación promete y el documento no valida.**
> «La nota de su Tabla 7 y el paso 5 de su manual dicen que la validación documentada usó clics como función objetivo; su presentación anuncia tres casos con objetivos de alcance, clics y visualizaciones, con presupuestos que no aparecen en el documento. ¿Ejecutaron el simulador maximizando alcance y visualizaciones, y dónde quedó registrada esa corrida?»
- **Por qué:** pp. 45 y 70 contra diapositivas 14-16; los resultados del documento solo cubren el caso de $10.000.000 con 40/30/30 (pp. 52-55).
- **Resuelve:** correrlo en vivo o mostrar la hoja del Excel exportado con ese objetivo, y explicar por qué al maximizar alcance el resultado no es la misma esquina.
- **Agrava:** afirmar que las tres corridas están en el documento —no lo están— o improvisar cifras.

### Banco de reserva

- «El objetivo 4 nombra la eficiencia presupuestal como indicador a analizar; en las Tablas 9, 10 y 11 no aparece. ¿Cuál fue su valor en el escenario ingresado y en el recomendado?» (pp. 16 y 52-54)
- «El alcance total de la Tabla 10, ¿es la suma del alcance de las tres plataformas? Si lo es, ¿cómo tratan el solapamiento de audiencias entre Meta, TikTok y YouTube?» (p. 53; el documento no lo declara)
- «Su conclusión 5 dice que no se confirmó ninguna reducción de incertidumbre; su diapositiva 17 dice que la herramienta supera los enfoques deterministas. ¿Cuál de las dos afirmaciones sostienen hoy ante nosotros?» (p. 58 vs. diapositiva 17)
- «Las tarifas, el CTR y las audiencias son supuestos académicos de referencia. ¿De dónde sacaría un planeador esos valores calibrados y cuánto podría cambiar la recomendación al hacerlo?» (nota, p. 45; recomendaciones, p. 58)
- «¿Qué audiencia máxima configuraron por plataforma y qué pasa con la recomendación si el techo de TikTok se vuelve restrictivo?» (fórmula de alcance, p. 45)
- «Su encuesta es muestreo por conveniencia con 45 registros válidos. ¿Qué decisión de diseño habrían cambiado si el resultado hubiera sido el contrario?» (p. 32) — pregunta para que muestren criterio, no para castigar la muestra.
- «La p. 70 dice que el notebook se entrega junto con el documento, pero en la carpeta compartida con los jurados solo están los dos PDF. ¿Dónde podemos verificar el código?»

---

## 6. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si no ejecutan nada en vivo y solo muestran capturas** → pedir que expliquen la nota de la Figura 5: por qué esa captura corresponde a una versión que normalizaba automáticamente una distribución mayor al 100 % y qué cambió después de la validación (pp. 48-49).
- **Si presentan los casos de María, Carlos o Andrea con cifras concretas** → preguntar de dónde salen esos números, dado que los resultados del documento solo cubren el caso de $10.000.000 con 40/30/30 (pp. 52-55).
- **Si dicen «+51,28 % más clics con el mismo dinero» sin matizarlo** (diapositiva 13) → pedirles que expliquen su propia frase de la p. 53: «demuestran coherencia interna con la función objetivo, no superioridad empírica en campañas reales». Es una oportunidad, no una trampa: si la sostienen bien, sube.
- **Si afirman que validaron con agencias, clientes o usuarios** → contrastar con el Anexo 7, que declara que no hubo pruebas ejecutadas por personas distintas a los desarrolladores (p. 71).
- **Si mencionan inteligencia artificial o aprendizaje automático como parte del simulador** → recordar que la limitación declarada dice que no incorpora modelos de machine learning ni IA (p. 20) y preguntar qué es exactamente lo que aprende el modelo.
- **Si hablan de «reducir la incertidumbre» como logro alcanzado** → pedirles cómo medirían esa reducción, dado que su conclusión 5 dice que la variable no se definió ni se midió (p. 58).
- **Si el tiempo se les va en el marco teórico y saltan los resultados** → ir directo a la Tabla 10 (p. 53): qué distribución recomendó el simulador y por qué.
- **Si solo hablan uno o dos de los cuatro** → pedir explícitamente a otro integrante que explique la Tabla 7 (p. 45): qué representa el factor lognormal de la tarifa y por qué se eligió esa distribución. Es la vía legítima para verificar dominio individual.
- **Si responden bien las tres prioritarias y sobra tiempo** → preguntar por la eficiencia presupuestal no reportada (reserva 1), que es el hueco más limpio del documento.

---

## 7. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado: dominio · claridad · coherencia del documento · capacidad de defensa)

- **4,6–5,0 (excelente; solo aquí tiene sentido pensar en meritoria).** Necesito ver dos cosas juntas: (a) que expliquen el compromiso entre valor esperado y dispersión y propongan un criterio de decisión que incorpore el riesgo, sin que yo se lo sugiera (p. 53); y (b) que reconozcan la estructura del óptimo —por qué la recomendación se va a la plataforma más barata— y qué tendría que cambiar en el modelo. Sumado a que el producto se vea funcionando y a que los cuatro integrantes hablen de su parte. La honestidad del documento (pp. 56-58, 71) ya juega a favor.
- **3,6–4,5 (buen desempeño; es donde este trabajo llega por defecto).** Documento coherente, modelo formalizado, prototipo existente y limitaciones declaradas. Se queda en 4,0–4,4 si defienden el prototipo pero no logran explicar por qué el optimizador siempre elige TikTok, si no muestran el sistema corriendo, o si leen las diapositivas. Sube a 4,5 si contestan dos de las tres preguntas prioritarias con solvencia.
- **3,0–3,5 (aceptable).** Si sostienen en sala el discurso de la diapositiva 17 —que la herramienta «supera los enfoques deterministas» y mejora el retorno— contradiciendo su propia conclusión 5 (p. 58), o si presentan el +51,28 % como evidencia de campañas reales. El documento vale más que esa defensa y sería una lástima.
- **0,1–2,9 (insuficiente).** Solo si no pueden explicar las fórmulas de su propia Tabla 7 (p. 45), o si atribuyen resultados a usuarios, clientes o campañas que el Anexo 7 declara inexistentes (p. 71).

**Rango que hoy anticipo, antes de escuchar: 4,3–4,6** (no es una nota sugerida: la nota la pongo yo en sala contra estos umbrales). Es un trabajo por encima del promedio en formalización y honestidad, con dos huecos conceptuales reales (criterio de riesgo y estructura del óptimo) y defectos de forma que no son de fondo. Recordar que mi voto es una cuarta parte compartida con el Jurado 1: no apruebo ni repruebo, valido.

---

## 8. Observaciones administrativas (no académicas)

1. **Equipo de cuatro integrantes** (portada, p. 1, y firmas, pp. 8-9), cuando el máximo en Proyecto I/II de especialización es de tres. Es una observación para la Dirección del Programa, **no** un criterio para bajar la nota del trabajo.
2. **El nombre del archivo de la presentación conserva el periodo anterior:** «Presentación Final **25ET1** – Proyecto-Seminario II – Grupo 12». La portada interna sí está correcta y no dice periodo. Cosmético, pero conviene que lo corrijan antes de radicar.
3. **El notebook no está en la carpeta compartida con los jurados.** La p. 70 anuncia `Prototipo_Validacion_Completa_Ejecutado.ipynb` como entregado junto con el documento; la carpeta `26ET2-G-012` solo contiene los dos PDF. Puede estar radicado en el aula: vale confirmarlo con la Dirección antes de la sala para no preguntar por algo que sí entregaron por otro canal.
4. **No se declara reporte de similitud (Turnitin) ni porcentaje** en ninguna de las 71 páginas, ni hay declaración de uso de IA generativa. Corresponde a la verificación del metodólogo, no al jurado; lo dejo anotado porque pesa 15 % en la rúbrica de integridad.
5. **Ética y datos personales:** el documento sí incluye una nota de tratamiento de datos, resultados agregados y no identificación individual de los participantes (p. 61). No declara consentimiento informado explícito del instrumento, lo cual es admisible en este nivel para una encuesta anónima de opinión profesional.
6. **Dato de mi propio alistamiento, no del grupo:** el JSON de preparación solo registró la asignación del martes 18 (6:00-9:00 p.m., 9 proyectos). Verifiqué en la hoja `CRONOGRAMA` del cronograma 26ET2 (fila 10) que la segunda sesión, **miércoles 19 de agosto de 6:00 a 7:20 p.m. con 4 proyectos**, pertenece al mismo panel; por eso este grupo me corresponde igualmente como Jurado 2. Si alguien reutiliza ese JSON, tenerlo en cuenta.
