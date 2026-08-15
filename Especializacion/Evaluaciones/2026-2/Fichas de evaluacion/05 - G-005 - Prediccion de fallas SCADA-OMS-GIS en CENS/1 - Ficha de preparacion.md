# 26ET2-G-005 — Comparación de modelos estadísticos y de Machine Learning para la predicción de fallas en sistemas eléctricos de distribución mediante integración de datos SCADA, OMS y GIS en Centrales Eléctricas de Norte de Santander

**Sustentación:** martes 18 de agosto de 2026 · 7:20 p. m. – 7:40 p. m. · **Mi rol:** Jurado 2
**Integrantes:** Edward Alexis Orduz Rodríguez (edward.orduz@cun.edu.co), Ángel David Ortiz Rivera (angel.ortizriv@cun.edu.co)
**Línea:** Gestión y Tecnología
**Documentos leídos:** `Proyecto final.pdf` (115 páginas) y `Sustentación proyecto de grado.pdf` (15 diapositivas), ambos en la carpeta del grupo. Solo hay una versión de cada uno; no hubo que elegir entre versiones.

---

## 1. Resumen para leer en 5 minutos

El proyecto parte de un problema real y bien delimitado: en Centrales Eléctricas de Norte de Santander (CENS) la gestión de fallas de la red de distribución es reactiva y se apoya en análisis históricos posteriores al evento, lo que limita la anticipación frente a los indicadores regulatorios SAIDI y SAIFI exigidos por la CREG y vigilados por la SSPD (pp. 12, 21-22, 30). La pregunta compara modelos estadísticos y de Machine Learning en desempeño predictivo, generalización e interpretabilidad, integrando SCADA, OMS y GIS (p. 23); el objetivo general y los cuatro específicos dicen exactamente eso (p. 25).

**Dato decisivo y hay que tenerlo presente antes de entrar:** no hubo acceso a los sistemas productivos de CENS, y el análisis completo se hizo sobre **un conjunto de datos construido/sintético** que reproduce la estructura y el comportamiento estadístico esperado de SCADA, OMS y GIS (p. 12; el abstract en inglés lo llama literalmente «simulated dataset», p. 14; la conclusión lo repite: «un conjunto sintético estructurado para fines académicos», p. 112).

Sobre ese conjunto: 87.500 eventos iniciales, 83.900 válidos tras depurar 3.600 (4,11 %), 20.900 activos trazables y 46 variables (pp. 76, 78). El aporte metodológico más sólido es haber definido la unidad de análisis **activo-semana** para construir la clase negativa y no acabar clasificando eventos ya ocurridos (pp. 48, 95), y haber excluido explícitamente como predictoras las variables de resultado (duración, usuarios afectados, ENS, SAIDI, SAIFI) para evitar fuga de información (pp. 49, 96).

Resultados: partición temporal con 6.409.824 filas de entrenamiento (2019-2024) y 1.003.200 de prueba (2025); ROC-AUC de 0,594 para Regresión Logística, 0,605 para Random Forest y 0,616 para XGBoost; PR-AUC máximo 0,053; mayor recall el de Random Forest, 0,297 (pp. 96-99, 111). SHAP sobre 5.000 registros identifica MES_SEMANA, EDAD_ACTIVO_SEMANA, TIPO_ACTIVO, MUNICIPIO y PRECIP_TOTAL_ULT_4S (p. 100). Una matriz multicriterio de 11 criterios selecciona XGBoost (0,6146 frente a 0,4189 y 0,3944) (pp. 104, 108).

**Producto:** un prototipo de tablero en Streamlit que integra el modelo XGBoost y SHAP, declarado prueba de concepto y no implementación productiva (pp. 71, 112). Caso de prueba: activo ACT-012907, conductor de MT en El Tarra, ~35 años, P(falla)=0,345 a cuatro semanas, riesgo alto, resultado retrospectivo **falso positivo**, que el documento reporta con honestidad (p. 72).

---

## 2. Coherencia título → objetivo → resultados

Título, pregunta (p. 23) y objetivo general (p. 25) son coherentes entre sí: el verbo es **comparar**, y comparar sí se hizo (tres modelos, mismas particiones, mismas métricas). El techo del trabajo está bien fijado: no promete implementar en producción y el alcance lo dice expresamente (p. 28). La incoherencia no está entre título y objetivo, sino entre **el objeto declarado** («los sistemas eléctricos de distribución de CENS») y **el objeto realmente analizado** (un conjunto sintético que los emula, pp. 14, 112).

| Objetivo específico | ¿Se cumplió? | Evidencia (p.) | Qué falta |
|---|---|---|---|
| 1. Recolectar y preprocesar SCADA, OMS y GIS | Sí, es el resultado más completo | ETL, reglas de exclusión, matriz de calidad, diccionario de datos y panel activo-semana: pp. 64-69, 76-78, 107 | Que sea sobre datos sintéticos no se enuncia en este apartado ni en la Tabla 14 (pp. 107-108); allí se lee «objetivo ejecutado sobre el conjunto de datos», sin el matiz |
| 2. Entrenar y ajustar modelos con validación cruzada y ajuste de hiperparámetros | Sí en entrenamiento; **parcial** en validación cruzada e hiperparámetros | Tres modelos y partición temporal: pp. 96, 107 | El documento anuncia k-fold estratificado por circuito y partición por circuito (pp. 51, 53), pero en resultados solo se reporta la partición temporal (p. 96). No hay tabla de hiperparámetros ni de folds |
| 3. Evaluar desempeño e interpretabilidad con métricas y XAI | Sí | Tabla 13 (p. 97), curvas PR y calibración (pp. 98-99), SHAP global y tres casos locales (pp. 100-103) | La Tabla 13 solo publica ROC-AUC, PR-AUC y precision; recall, F1, Brier y tiempos se mencionan en texto (pp. 99, 107) pero no se tabulan. La nota de la Tabla 13 habla del Brier Score, que no aparece en la tabla (p. 97) |
| 4. Marco comparativo multicriterio de selección | Sí | Puntajes 0,6146 / 0,4189 / 0,3944 (pp. 104, 108) | No se publican los 11 criterios, sus pesos ni las calificaciones parciales: solo el puntaje final (pp. 104, 108) |
| Hipótesis específica 1 (clima y espacio mejoran el desempeño) | **No contrastada** | El propio documento lo dice: requiere «comparar los modelos con y sin dichas variables» (pp. 87-88, 94) | Ese experimento de ablación no aparece en el capítulo de modelamiento (pp. 95-104). La hipótesis queda abierta y las conclusiones no lo declaran |
| Resultados esperados declarados (AUC > 0,75; recall ≥ 70 %) | **No alcanzados** | Metas en p. 28; logrado AUC 0,616 y recall máximo 0,297 (pp. 97, 111) | Las conclusiones (pp. 110-112) no confrontan la meta con el resultado |

---

## 3. Fortalezas verificables

1. **Honestidad declarada en los sitios que importan.** El resumen (p. 12), el abstract (p. 14) y la conclusión general (p. 112) dicen que el conjunto es sintético y que los resultados no representan el desempeño sobre datos reales de CENS. No es un trabajo que esconda su límite principal en el documento.
2. **La corrección metodológica del panel activo-semana está bien argumentada.** Reconocen que 83.900 eventos OMS son todos positivos y que un problema binario exige construir la clase negativa; lo construyen cruzando 20.900 activos trazables con el calendario semanal (pp. 47-48, 95). Es exactamente la falla conceptual que hunde a muchos trabajos de predicción de fallas, y aquí está resuelta y explicada.
3. **Tratamiento explícito de la fuga de información.** Excluyen duración, usuarios afectados, ENS, SAIDI, SAIFI, tipo de falla, causa y tipo de evento como predictoras, con la razón técnica correcta (pp. 49, 96). El diccionario de datos clasifica cada variable por uso: predictora, segmentación, respuesta o evaluación (pp. 68-70).
4. **Interpretación sobria de sus propios resultados.** Con AUC de 0,616 dicen «capacidad predictiva moderada» y que el modelo es «herramienta de priorización y no predictor determinístico» (p. 99); explicitan que la selección de XGBoost no lo hace universalmente superior (p. 104); y advierten que SHAP muestra contribuciones y no causalidad (p. 102).
5. **Reportan un falso positivo como caso de prueba.** El activo ACT-012907 fue clasificado de riesgo alto y no falló, y lo dicen (p. 72) en lugar de buscar un caso favorable. Es un gesto de integridad poco frecuente.
6. **Anclaje regulatorio real.** CREG 015 de 2018, vigilancia SSPD e IEEE 1366 están usados como marco de decisión y no como adorno (pp. 30-31), y la interpretabilidad se justifica desde la exigencia normativa (p. 22).
7. **Arquitectura de datos en cuatro capas** con orquestación, versionado, model registry y monitoreo de deriva, corrigiendo expresamente una versión anterior más pobre (pp. 56-58).

---

## 4. Debilidades y huecos (con página)

1. **La presentación no dice que los datos son sintéticos.** En las 15 diapositivas no aparece la palabra sintético ni la restricción de acceso. La diapositiva 7 presenta como **POBLACIÓN** «87.500 eventos históricos de interrupción + 600.000 usuarios CENS» y la 10 titula «600.000 usuarios analizados» y «ETL exitoso» (diapositivas 7 y 10). El documento dice lo contrario (pp. 14, 112). Es la brecha más grande entre documento y sustentación, y es la que hay que resolver en sala.
2. **Contradicciones internas sobre la naturaleza del dato.** En Tipo de investigación: «Se analizan datos históricos reales del sistema» (p. 45). En Validez: «Se garantiza mediante: uso de datos oficiales corporativos» (p. 52). Ambas frases son incompatibles con pp. 14 y 112. Las notas de las figuras atribuyen la fuente a «Distribuidora de Energía, Norte de Santander (2019-2025)» (pp. 86, 87), como si fuera el operador real.
3. **Restos de una versión anterior que se contradicen con los resultados finales.** La p. 29 afirma que la verificación cuantitativa de las metas «no forma parte del alcance ejecutado en esta entrega»; la p. 45 dice que el entrenamiento y la comparación real «queda fuera de los límites ejecutados»; la p. 55 dice que la Fase 5 «constituye la línea de trabajo recomendada para que CENS… ejecute»; la p. 77 dice que la aptitud del panel «se confirmará una vez se complete su construcción». Todo eso convive con pp. 96-108, donde el entrenamiento, la evaluación, SHAP y la matriz multicriterio **sí** están ejecutados. Un jurado que lea solo la metodología concluye que no hubo modelos.
4. **Desbalance de clases declarado que no cuadra con la aritmética del propio documento.** La p. 49 fija la clase positiva en «aproximadamente el 18 %» y la negativa en 82 %. Pero el panel tiene 7.413.024 filas (6.409.824 + 1.003.200, p. 96) y como máximo 83.900 pueden ser positivas (p. 47): eso da 1,13 %, no 18 %. Un tercer número, el PR-AUC de ~0,05 (p. 97), tampoco coincide con ninguna de las dos cifras. Alguno de los tres está mal y conviene saber cuál.
5. **Las particiones declaradas no son las ejecutadas.** La p. 51 y la Tabla 11 (p. 76) fijan 70 % / 30 %; la p. 96 y la diapositiva 11 reportan 2019-2024 contra 2025, que es 86,5 % / 13,5 %. La misma diapositiva 7 sigue anunciando «Train/Test 70 %-30 %» mientras la 11 muestra la partición temporal. También se anuncia partición por circuito y k-fold por circuito (pp. 51, 53) que no aparecen en resultados.
6. **Umbrales de decisión radicalmente distintos entre modelos:** 0,60 para Regresión Logística, 0,57 para Random Forest y **0,05** para XGBoost (p. 97). Precision, recall y F1 son métricas dependientes del umbral: compararlas con umbrales que difieren en un orden de magnitud no es una comparación entre iguales, y la selección de XGBoost se apoya en parte en esas métricas.
7. **Del prototipo no hay una sola imagen.** La p. 71 y la diapositiva 13 afirman «prototipo funcional en Streamlit»; la lista de figuras tiene 16 figuras y ninguna es una captura del tablero (p. 11). Además, en el mismo capítulo la p. 72 dice que «la especificación técnica del producto… **sí** forma parte del alcance ejecutado» y la nota de la Tabla 10 precisa que lo que queda fuera es «su ejecución sobre una implementación real y sobre datos operativos de CENS» (p. 74) —cita completa, porque recortada en «no forma parte del alcance ejecutado» parece negar el prototipo y no lo niega—, mientras Streamlit aparece en la lista de tecnologías «recomendadas para una eventual implementación», «documentada como recomendación técnica y no como stack ya implementado» (p. 73). El documento declara el prototipo tres veces (pp. 71, 112 y diap. 13); lo que no aporta es una sola evidencia visual de él.
8. **Dos probabilidades distintas para el mismo activo.** El caso oficial da P(falla)=0,345 (p. 72) y la Figura 14 da 0,236 para ACT-012907 (p. 102). El documento lo advierte en una nota metodológica (p. 104), lo cual está bien, pero en la diapositiva 12 aparece 0,236 y en la 13 aparece 34,5 % sin la aclaración.
9. **CRISP-DM aparece en la sustentación y no en el documento.** La diapositiva 7 declara la metodología «basada en CRISP-DM» con sus seis fases; el capítulo de Metodología del documento (pp. 44-55) organiza el trabajo en cinco fases propias y no menciona CRISP-DM en ningún punto del texto.
10. **Hipótesis 1 e hipótesis 2 sin cierre formal.** La 1 exige una ablación que no se hizo (pp. 87-88, 94). La 2 (Random Forest con mayor recall que la regresión logística) se sostiene solo con el recall de Random Forest, 0,297 (p. 111), sin publicar el de la regresión logística.
11. **Referencias:** ~28 entradas con buen núcleo arbitrado (IEEE, Springer, Elsevier), pero incluye Wikipedia como fuente sobre CENS, USA Today y PowerOutage.us (p. 115), y una entrada sin título de artículo, «Sánchez, H. N., & Pérez Santos, A. S. (2005). Revista Tecnura» (p. 114). El documento **no reporta índice de similitud ni informe antiplagio** (buscado en Preliminares pp. 16-17 y en todo el texto: no hay mención de Turnitin ni de porcentaje de similitud), ni declara uso de IA generativa.
12. **Estructura desordenada en el tramo final.** «Síntesis de hallazgos del análisis exploratorio» va en la p. 105, después del capítulo de modelamiento (pp. 95-104). El capítulo de modelamiento abre con el subtítulo «Influencia de la edad de los activos» (p. 95), copiado del apartado exploratorio de la p. 89, cuando su contenido es la construcción del panel. La p. 107 empieza con «En su lugar, presenta el alcance…», frase que quedó huérfana de su antecedente.

**Forma (no se pregunta en sala):** la Declaración de originalidad dice «Especialización en **Analítica de Datos**» en lugar de Transformación Digital (p. 16). Partición de palabras dentro de líneas por el interlineado del PDF («Cur vas», p. 98; «activo -semana» con espacio, varias páginas). En la diapositiva 6 hay doble punto final y en la 15 la referencia CREG 015 de 2018 está duplicada.

---

## 5. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**Pregunta 1 — La naturaleza del dato y su ausencia en las diapositivas**
> «El documento dice con claridad que no hubo acceso a los sistemas productivos de CENS y que todo el análisis se hizo sobre un conjunto sintético —lo dicen en la página 14 y lo repiten en la 112—, pero en las diapositivas 7 y 10 la población aparece como 87.500 eventos históricos y 600.000 usuarios de CENS sin ese matiz: cuéntenme cómo generaron ese conjunto y qué de lo que concluyen sigue en pie sabiendo que los patrones que el modelo aprendió los pusieron ustedes al generar los datos.»

- **Por qué se pregunta:** p. 12 y p. 14 («simulated dataset») frente a la diapositiva 7 («POBLACIÓN: 87.500 eventos históricos de interrupción + 600.000 usuarios CENS») y la diapositiva 10 («600.000 usuarios analizados»). Refuerzan la duda las frases «se analizan datos históricos reales del sistema» (p. 45), «uso de datos oficiales corporativos» (p. 52) y las notas de fuente de las figuras (pp. 86-87).
- **Qué la resuelve:** que describan el procedimiento generador (distribuciones, estacionalidad y relaciones inyectadas, semilla, herramienta), que digan explícitamente en voz alta que el conjunto es sintético, y que distingan qué sí queda validado —el flujo metodológico, la arquitectura, el pipeline reproducible— de lo que no —el desempeño esperable en CENS—.
- **Qué la agrava:** afirmar en sala que son datos reales de CENS o de «una distribuidora de Norte de Santander»; o no poder explicar cómo se generó el conjunto, porque entonces el AUC de 0,616 no se sabe qué está midiendo.

**Pregunta 2 — Sus propios criterios de éxito**
> «Ustedes fijaron como resultados esperados un AUC superior a 0,75 y un recall mínimo del 70 % —página 28—, y lo que obtuvieron fue un AUC de 0,616 con XGBoost y un recall máximo de 0,297 con Random Forest: ¿por qué esa comparación no aparece en las conclusiones y qué lectura técnica hacen de esa distancia?»

- **Por qué se pregunta:** metas cuantificables en p. 28 («AUC superior a 0.75», «recall mínimo del 70 %»); resultados en p. 97 (Tabla 13: XGBoost 0,616290) y p. 111 (recall 0,297). Las conclusiones (pp. 110-112) hablan de «desempeño moderado» y de «mejora frente al modelo estadístico de referencia», pero nunca contra la meta propia.
- **Qué la resuelve:** reconocer que las metas no se alcanzaron y explicar por qué es esperable —prevalencia muy baja, horizonte semanal, variables predictoras limitadas a estructura y clima, ausencia de señal SCADA fina—; y sostener que con AUC de 0,616 la utilidad es ordenar activos por riesgo relativo, como ya escriben en la p. 99.
- **Qué la agrava:** presentar 0,616 como buen desempeño, o atribuirlo únicamente a que los datos son sintéticos sin argumento; peor aún, decir que la meta «se cumplió parcialmente».

**Pregunta 3 — La existencia del producto**
> «En la página 71 y en la diapositiva 13 hablan de un prototipo funcional en Streamlit que integra el modelo y SHAP, pero entre las dieciséis figuras del documento no hay ni una captura del tablero: ¿está corriendo hoy, y pueden describirme qué se ve en pantalla cuando se consulta el activo ACT-012907?»

- **Por qué se pregunta:** p. 71 («se desarrolló un prototipo funcional de tablero predictivo utilizando Streamlit», «prueba de concepto funcional»); lista de figuras con 16 figuras y ninguna del tablero: son la arquitectura, ocho gráficas exploratorias, tres de métricas y cuatro de SHAP (p. 11). El matiz que hay que tener claro antes de hablar: la p. 73 lista Streamlit entre las tecnologías «recomendadas para una eventual implementación» —eso se refiere a la puesta en producción, no al prototipo— y la nota de la Tabla 10 (p. 74) excluye del alcance «su ejecución sobre una implementación real y sobre datos operativos de CENS», no la existencia del tablero. Y la p. 112 afirma que «el desarrollo del prototipo en Streamlit permitió comprobar la integración conceptual y funcional». Es decir: el documento no se contradice sobre el producto, simplemente no lo muestra. La pregunta es por la evidencia, no por una contradicción.
- **Qué la resuelve:** una demostración en vivo, un video, una captura, o una descripción precisa y consistente de los seis pasos del caso de uso con los valores del caso de prueba (P=0,345, riesgo alto, factores SHAP).
- **Qué la agrava:** que cada integrante describa un producto distinto, o que se refugien en «está especificado» cuando la afirmación del documento y de la diapositiva es «funcional».

### Banco de reserva (por si sobra tiempo o si contestan rápido)

- **Desbalance.** «La página 49 dice que la clase positiva es el 18 % del panel; con 7.413.024 filas y a lo sumo 83.900 positivos me sale 1,13 %. ¿Cuál de los dos números es el del panel que entrenaron?»
- **Umbrales.** «¿Por qué el umbral de XGBoost es 0,05 y el de la regresión logística 0,60 (p. 97), y en qué sentido son comparables la precision y el F1 calculados así?»
- **Particiones.** «La página 51 y la Tabla 11 dicen 70/30; la página 96 y la diapositiva 11 muestran 2019-2024 contra 2025. ¿Cuál se usó, y qué pasó con la partición por circuito y el k-fold estratificado por circuito que anuncian en la página 53?»
- **Hipótesis 1.** «Ustedes mismos escriben en la página 88 que la hipótesis del aporte del clima exige comparar modelos con y sin esas variables. ¿Se corrió esa comparación? Si no, ¿la hipótesis queda abierta?»
- **Multicriterio.** «Los 11 criterios de la matriz y sus pesos no están publicados (pp. 104, 108). ¿Cuánto pesó la interpretabilidad frente al desempeño, y XGBoost seguiría ganando si se invirtieran esos dos pesos?»
- **CRISP-DM.** «La diapositiva 7 declara CRISP-DM; el documento no lo menciona y organiza cinco fases propias. ¿Cómo se corresponden las seis fases de CRISP-DM con esas cinco?»
- **Reproducibilidad.** «¿Hay repositorio de código y versión de dataset (los mencionan en la arquitectura, p. 58)? ¿Un tercero podría reproducir la Tabla 13?»
- **Uso operativo.** «Con precision de 0,06, de cada 100 activos que el tablero marca como riesgo alto fallaría cerca de 6. ¿Cómo se le presenta eso a Gestión de Activos para que la cuadrilla no pierda credibilidad en la herramienta?»
- **Integridad.** «El documento no reporta índice de similitud ni informe antiplagio. ¿Se corrió? ¿Con qué resultado?» — *preferible planteárselo a la Dirección o al director, no en sala.*

---

## 6. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si en toda la exposición no dijeron la palabra «sintético» o «simulado»** → preguntar directamente: «¿los 83.900 eventos que acaban de mostrar son registros reales de CENS?» y dejar que ellos mismos hagan la corrección. Es la pregunta que no se puede dejar de hacer, y hay que hacerla sin ánimo acusatorio: el documento sí lo declara (pp. 14, 112), así que lo más probable es que sea una omisión de la diapositiva, no una intención.
- **Si sí lo declararon con claridad** → subir el nivel: preguntar cómo generaron el conjunto y qué relaciones inyectaron, y por qué un modelo entrenado sobre datos generados por ellos alcanza apenas 0,616 de AUC: la respuesta a eso distingue a quien entiende el experimento de quien lo ejecutó.
- **Si mostraron el tablero funcionando en pantalla** → cambiar la pregunta 3 por: «¿de dónde lee las variables del activo: del CSV del panel o de una consulta a la capa de integración? ¿Y qué pasa si al activo le faltan variables predictoras, como prevé el paso 2 de la Tabla 10 (p. 73)?»
- **Si no mostraron el tablero pero afirmaron que existe** → pedir la descripción de los seis pasos y de la salida concreta para ACT-012907, y anotar si coincide con la Tabla 10 y con el caso de la p. 72.
- **Si se pasaron de tiempo y saltaron el capítulo de modelamiento** → ir directo a los resultados: «díganme los tres AUC y el recall del modelo que seleccionaron, y por qué escogieron XGBoost si Random Forest tiene mejor recall (p. 111), que en mantenimiento es la métrica que evita dejar pasar una falla».
- **Si afirmaron que el clima mejora la predicción** → preguntar con qué evidencia, porque la p. 88 dice expresamente que eso no puede afirmarse sin comparar modelos con y sin esas variables.
- **Si dijeron «validado con CENS» o «validado con usuarios técnicos»** → preguntar quiénes, cuántos, cuándo y con qué instrumento; el documento sitúa esa validación como recomendación futura, no como algo hecho (pp. 74-75).
- **Si habló solo uno de los dos** → pedir explícitamente al otro que explique su parte, aprovechando que la diapositiva 2 declara perfiles distintos: al ingeniero electromecánico, cómo se traduce una probabilidad de 0,345 en una orden de trabajo y en el SAIDI del mercado; al ingeniero de sistemas, cómo se construyó la clase negativa del panel activo-semana (p. 48).
- **Si presentan el proyecto como implementable ya en CENS** → recordar sus propias palabras de la p. 112 y preguntar qué tres condiciones tendrían que cumplirse antes (la p. 74 ya las enumera: acceso y calidad de las fuentes reales, reentrenamiento sobre datos reales, implementación del tablero).
- **Si contestan todo bien y sobra medio minuto** → cerrar con la pregunta del desbalance (18 % contra 1,13 %): es la que mejor discrimina dominio técnico real.

---

## 7. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

Nivel de referencia: especialización profesionalizante. No se exige aporte teórico original, muestra representativa ni validación externa del instrumento; se exige coherencia, evidencia de que se hizo y honestidad sobre los límites.

**Para 4,6 o más (excelente, umbral de meritoria) necesito ver las cuatro cosas:**
1. Que **enuncien en voz alta** que el conjunto es sintético, sin que haya que preguntarlo, y que expliquen cómo se generó.
2. Que **reconozcan** que sus metas de AUC y recall no se alcanzaron y sostengan una lectura técnica correcta de un AUC de 0,616 (priorización, no predicción determinística).
3. Que **muestren el tablero** funcionando o den evidencia equivalente.
4. Que **ambos integrantes** demuestren dominio de su parte, y que respondan bien al menos una de las preguntas de reserva (desbalance, umbrales o particiones).

**4,0 – 4,4 (buen desempeño):** si declaran lo sintético y defienden bien la metodología —panel activo-semana y fuga de información, que es lo mejor que tienen—, pero **falta la evidencia del producto** o **eluden la comparación con sus propias metas**. Es el escenario más probable a la luz de los dos documentos. Aquí es donde hoy leo el trabajo.

**3,6 – 3,9:** si declaran lo sintético solo al ser preguntados, describen resultados sin poder explicar cómo se obtuvieron, y el producto queda en «especificado». La coherencia del documento pesa en contra por los restos de versión anterior (pp. 29, 45, 55, 77 contra pp. 96-108) y por el 18 % que no cuadra (p. 49).

**3,0 – 3,5 (aceptable):** si en sala se sostiene que los datos son reales de CENS y, al mostrarles la p. 14, no hay una explicación consistente; o si un solo integrante puede responder por todo el trabajo.

**Por debajo de 3,0:** solo si se afirma un producto o una validación institucional que el documento contradice y se insiste en ello tras la aclaración. Nada de lo leído hasta ahora apunta a este escenario: el documento es honesto donde importa.

**Nota sobre la meritoria:** con AUC de 0,616, con la hipótesis 1 sin contrastar y con el 18 % de la p. 49 sin conciliar, no propondría meritoria salvo que la defensa oral sea sobresaliente en los cuatro puntos de arriba. Y si voy a poner 4,4, la página es la 28 contra la 97.

---

## 8. Observaciones administrativas (no académicas)

- **Equipo de 2 integrantes.** Dentro del máximo de 3. Sin observación.
- **Correos institucionales del cronograma verificados** contra la portada y la diapositiva 1: los dos nombres coinciden (Edward Alexis Orduz Rodríguez y Ángel David Ortiz Rivera). Sin novedad.
- **Documento de originalidad con el programa equivocado:** la p. 16 dice «Especialización en **Analítica de Datos**» y el trabajo es de Especialización en Transformación Digital (portada, p. 1). Corrección de forma para la Dirección del Programa; no afecta la nota.
- **Firma fechada «Cúcuta, agosto de 2026»** (pp. 16-17), consistente con el periodo. Las declaraciones aparecen sin firma manuscrita ni digital, solo con la línea y el nombre.
- **No hay reporte de similitud ni informe antiplagio** en la carpeta del grupo ni en el documento (buscado en Preliminares, pp. 16-17, y en el texto completo). Vale plantearlo al director del programa **antes de la sala**, no en la sustentación: si la Dirección ya lo tiene, no es un hallazgo; si no, es un requisito de la rúbrica de integridad (15 %) que no puedo verificar como jurado.
- **Punto que conviene acordar con la moderadora antes de empezar:** cómo se va a tratar en sala el hecho de que la presentación no declare el carácter sintético del conjunto. Lo natural es que la Dirección lo pida al inicio o que el grupo lo aclare motu proprio; convertirlo en un «pillado» del jurado sería injusto con un grupo que lo declaró por escrito en tres lugares del documento.
- **Referencias con fecha 2026** (MinTIC, SSPD, PowerOutage.us, USA Today, Wikipedia; pp. 114-115): consistentes con el periodo, pero tres de ellas no son fuentes académicas. Observación de forma.
