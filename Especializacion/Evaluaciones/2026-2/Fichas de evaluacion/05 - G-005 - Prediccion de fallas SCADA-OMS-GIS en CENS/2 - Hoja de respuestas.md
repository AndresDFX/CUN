# 05 · 26ET2-G-005 — Comparación de modelos estadísticos y de Machine Learning para la predicción de fallas con SCADA, OMS y GIS en CENS

**HOJA DE RESPUESTAS — se llena A MANO en sala.** martes 18 de agosto de 2026 · 7:20 – 7:40 p. m. · **Mi rol:** Jurado 2

**Entró** __:__ · **fin de la exposición** __:__ · **minutos usados** ____ · **fallas de plataforma:** _________________

**Quién habló y de qué** (única vía legítima para juzgar dominio individual):
- Edward Alexis Orduz Rodríguez: _________________________________________________________
- Ángel David Ortiz Rivera: ______________________________________________________________

---

## A · MIENTRAS EXPONEN — marcar ✓ ~ ✗ y escribir en la línea

`[ ] leyeron las diapositivas`  ·  `[ ] el demo corrió`  ·  `[ ] dijeron «no sé» y reconduje`  ·  `[ ] contradijeron el documento (p. ____)`

**Problema y pregunta (2 min)** ✓ ~ ✗ · __________________________________________________________
**Objetivos (1 min)** ✓ ~ ✗ · ___________________________________________________________________
**Método (2-3 min)** ✓ ~ ✗ · ___________________________________________________________________
**Resultados (3 min)** ✓ ~ ✗ · __________________________________________________________________
**Discusión y conclusión (2-3 min)** ✓ ~ ✗ · _______________________________________________________
**Aporte y cierre (1 min)** ✓ ~ ✗ · _______________________________________________________________

**REQUISITOS PARA 4,6+ — marcarlos aquí, cuando ocurran** (§8 de la ficha; se cumplen durante la exposición, no al final)

- [ ] Que enuncien lo sintético sin que se les pregunte y expliquen cómo se generó
- [ ] Que reconozcan que sus metas de AUC y recall no se alcanzaron y sostengan la lectura correcta de un AUC de 0,616 (priorización, no predicción determinística)
- [ ] Que muestren el tablero o den evidencia equivalente
- [ ] Que ambos demuestren dominio y respondan bien una de reserva

## B · CONDICIONALES (§7 de la ficha) — marcar oyendo; cada marca elige la pregunta

> Lo que va entre « » se lee tal cual. La página en negrita es la que sostiene la pregunta: si la respuesta la contradice, se anota abajo con esa página.

- [ ] Si en toda la exposición no dijeron «sintético» ni «simulado» → esta va primera, antes de las tres  **(pp. 14, 112)**
  - Preguntar así: «¿los 83.900 eventos que acaban de mostrar son registros reales de CENS?»
- [ ] Si sí lo declararon con claridad → no gastar tiempo aquí y entrar directo a P1
- [ ] Si mostraron el tablero funcionando → pedir la lectura del activo ACT-012907  **(p. 73 · reserva del tablero)**
  - Preguntar así: «¿de dónde lee las variables del activo: del CSV del panel o de una consulta a la capa de integración? ¿Y qué pasa si al activo le faltan variables predictoras, como prevé el paso 2 de la Tabla 10 (p. 73)?»
- [ ] Si no mostraron el tablero pero afirmaron que existe → reserva del tablero: los seis pasos y la salida de ACT-012907  **(p. 72)**
- [ ] Si se pasaron de tiempo y saltaron el modelamiento → pedir en una frase el mejor modelo y su AUC  **(p. 111)**
- [ ] Si afirmaron que el clima mejora la predicción → pedir la evidencia en su propia tabla  **(p. 88)**
- [ ] Si dijeron «validado con CENS» o «con usuarios técnicos» → es P3: cuántos, cargo, fecha e instrumento  **(p. 66 contra pp. 12 y 75)**
- [ ] Si habló solo uno de los dos → repartir: uno los datos, otro el modelamiento  **(p. 48)**
- [ ] Si presentan el proyecto como implementable ya en CENS → recordar sus propias palabras de la p. 112 y preguntar qué tres condiciones tendrían que cumplirse antes (la p. 74 ya las enumera: acceso y calidad de las fuentes reales, reentrenamiento sobre datos reales, implementación del tablero)
- [ ] Si contestan todo bien y sobra medio minuto → cerrar con las 20 variables: 20 en la p. 100, 7 en la Tabla 9, 15 en la Figura 13. ¿En qué página están las 20?

**RESPUESTAS A LOS CONDICIONALES Y A LA RESERVA** — número del condicional (o «R» si es de reserva) y lo que contestó, con cifras y nombres tal como los diga.

____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________

## C · MIS 3 MINUTOS — leer la pregunta tal cual está escrita

**Pregunta 1 — Qué variable de SCADA entra al modelo**

> «El título y el objetivo general de la página 25 venden la integración SCADA-OMS-GIS. Pero la Tabla 9, página 68, marca las seis variables de SCADA como excluidas por data leakage, y en la Figura 13, página 101, ninguna de las quince variables del resumen SHAP viene de SCADA. Nómbrenme una variable de SCADA que entre al modelo final. Si no entra ninguna, díganlo con esas palabras.»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Pregunta 2 — La prevalencia real del panel**

> «Las páginas 49 y 51 fijan la clase positiva del panel en aproximadamente el 18 %. Pero las dos particiones de la página 96 suman 7.413.024 filas y los positivos son a lo sumo los 83.900 eventos de la página 47: eso da 1,13 %. Denme una sola cifra: ¿qué porcentaje de filas positivas tenía el panel con que entrenaron? Si el 18 % fue un supuesto de diseño y no una medición, díganlo así.»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Pregunta 3 — El juicio de expertos de CENS**

> «La página 66 afirma que los instrumentos fueron sometidos a un proceso de validación técnica interna mediante revisión por juicio de expertos de las áreas de Operación del Sistema, Gestión de Activos y Analítica de Datos de CENS. La página 12 dice que no fue posible acceder a los sistemas productivos de CENS. Díganme cuántos expertos fueron y en qué fecha. Si fue una conversación informal y sin acta, díganlo con esas palabras.»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Reserva (solo si sobra tiempo):** las 20 variables del XGBoost contra las 7 del diccionario y las 15 de la Figura 13 (pp. 68-70, 100, 101) · MES_SEMANA como señal dominante (pp. 100-101) · resumen contra abstract (pp. 12 y 14) · los 600 registros de la diapositiva 9 contra la Tabla 12 (p. 78) · la Fase 5 contra sí misma (p. 55) · datos reales, oficiales o sintéticos (pp. 45, 52 y 112) · las metas propias sin confrontar (pp. 28, 97, 110-112) · el tablero en pantalla (pp. 11, 71-73) · la bibliografía de la presentación (pp. 22, 27, 33, 113-115)

## D · AL CIERRE — rodear el rango y poner la nota

- **Meritoria:** no la propondría con AUC 0,616, la hipótesis 1 sin contrastar y el 18 % de la p. 49 sin conciliar, salvo defensa sobresaliente en los cuatro puntos. Si pongo 4,4, la página es la 28 contra la 97.

**Partida antes de oír (§8 de la ficha):** 4,0 – 4,4 es el escenario más probable a la luz de los dos documentos.

**Dominio del tema** — rodear:   0,1–2,9   ·   3,0–3,5   ·   3,6–4,5   ·   4,6–5,0   →   nota  ______

**Claridad** — rodear:   0,1–2,9   ·   3,0–3,5   ·   3,6–4,5   ·   4,6–5,0   →   nota  ______

**Coherencia del documento** — rodear:   0,1–2,9   ·   3,0–3,5   ·   3,6–4,5   ·   4,6–5,0   →   nota  ______

**Capacidad de defensa** — rodear:   0,1–2,9   ·   3,0–3,5   ·   3,6–4,5   ·   4,6–5,0   →   nota  ______

### NOTA QUE REPORTO A LA MODERADORA:  __________

Es **una sola** nota, y es la única que queda en el acta. Regla: promedio simple de los cuatro criterios de arriba — el instructivo **no publica ponderación entre ellos** (la de la p. 22, con pesos, califica otros seis criterios del informe escrito). Si la moderadora pide criterio por criterio, se leen los cuatro de arriba.

**Retroalimentación (fortalezas · ajustes requeridos · acciones):**

1. ______________________________________________________________________________________
2. ______________________________________________________________________________________
3. ______________________________________________________________________________________

⚠️ **Un 5,0 es proponer laureada** y exige que el Jurado 1 coincida. **Meritoria** (instructivo p. 11): promedio de jurados ≥ 4,6 y < 5,0, **ninguna nota de jurado** inferior a 4,5, y la pide al menos un jurado. Los cuatro criterios de arriba son **mi retícula interna**, no notas que se reporten: si la que baja de 4,5 es mi nota única, tengo que poder decir la página.

**Taquigrafía:** ✓ lo dijo · ✗ no lo dijo · ~ ambiguo · ! contradice el documento (p. __) · ☐ verificar después

## E · FORMULARIO OFICIAL DEL JURADO — 5 criterios, escala 1–5

Instrumento **distinto** de los cuatro criterios de la §D: aquellos dan la **nota del acta**, estos cinco van al formulario de la Dirección y **no son notas**. Las cinco se responden con el documento, así que vienen **precargadas** desde la §8.1 de la ficha, que trae la página que sostiene cada casilla. En sala solo se confirma; si la sustentación cambia una, se tacha y se rodea otra.

**1. Problemática y objetivos** — rodear:   1   ·   2   ·   3   ·   4   ·   5   →   precargado **4**

**2. Marco teórico y referentes** — rodear:   1   ·   2   ·   3   ·   4   ·   5   →   precargado **3**

**3. Metodología, muestra y diseño** — rodear:   1   ·   2   ·   3   ·   4   ·   5   →   precargado **3**

**4. Resultados y conclusiones** — rodear:   1   ·   2   ·   3   ·   4   ·   5   →   precargado **3**

**5. Pertinencia disciplinar** — rodear:   1   ·   2   ·   3   ·   4   ·   5   →   precargado **4**

**Suma:  ______ / 25**   ·   precargada: **17 / 25**

**Si cambio una casilla, la razón en una línea** (la §8.1 trae el sustento del precargado):   ______________________________________________________
