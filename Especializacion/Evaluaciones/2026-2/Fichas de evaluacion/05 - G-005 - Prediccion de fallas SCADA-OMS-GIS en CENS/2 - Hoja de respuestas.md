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

**REQUISITOS PARA 4,6+ — marcarlos aquí, cuando ocurran** (§7 de la ficha; se cumplen durante la exposición, no al final)

- [ ] Que enuncien lo sintético sin que se les pregunte y expliquen cómo se generó
- [ ] Que reconozcan que sus metas de AUC y recall no se alcanzaron y sostengan la lectura correcta de un AUC de 0,616 (priorización, no predicción determinística)
- [ ] Que muestren el tablero o den evidencia equivalente
- [ ] Que ambos demuestren dominio y respondan bien una de reserva

## B · CONDICIONALES (§6 de la ficha) — marcar oyendo; cada marca elige la pregunta

> Lo que va entre « » se lee tal cual. La página en negrita es la que sostiene la pregunta: si la respuesta la contradice, se anota abajo con esa página.

- [ ] Si en toda la exposición no dijeron «sintético» ni «simulado» → P1, directa y primera  **(pp. 14, 112)**
  - Preguntar así: «¿los 83.900 eventos que acaban de mostrar son registros reales de CENS?»
- [ ] Si sí lo declararon con claridad → soltar la mitad de P1 y pasar a P2
- [ ] Si mostraron el tablero funcionando → pedir la lectura del activo ACT-012907  **(p. 73 · sustituye P3)**
  - Preguntar así: «¿de dónde lee las variables del activo: del CSV del panel o de una consulta a la capa de integración? ¿Y qué pasa si al activo le faltan variables predictoras, como prevé el paso 2 de la Tabla 10 (p. 73)?»
- [ ] Si no mostraron el tablero pero afirmaron que existe → P3  **(p. 72)**
- [ ] Si se pasaron de tiempo y saltaron el modelamiento → pedir en una frase el mejor modelo y su AUC  **(p. 111)**
- [ ] Si afirmaron que el clima mejora la predicción → pedir la evidencia en su propia tabla  **(p. 88)**
- [ ] Si dijeron «validado con CENS» o «con usuarios técnicos» → pedir nombre del área y fecha  **(pp. 74-75)**
- [ ] Si habló solo uno de los dos → repartir: uno los datos, otro el modelamiento  **(p. 48)**
- [ ] Si presentan el proyecto como implementable ya en CENS → recordar sus propias palabras de la p. 112 y preguntar qué tres condiciones tendrían que cumplirse antes (la p. 74 ya las enumera: acceso y calidad de las fuentes reales, reentrenamiento sobre datos reales, implementación del tablero)
- [ ] Si contestan todo bien y sobra medio minuto → cerrar con la pregunta del desbalance (18 % contra 1,13 %): es la que mejor discrimina dominio técnico real

**RESPUESTAS A LOS CONDICIONALES Y A LA RESERVA** — número del condicional (o «R» si es de reserva) y lo que contestó, con cifras y nombres tal como los diga.

____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________

## C · MIS 3 MINUTOS — leer la pregunta tal cual está escrita

**Pregunta 1 — La naturaleza del dato y su ausencia en las diapositivas**

> «El documento dice con claridad que no hubo acceso a los sistemas productivos de CENS y que todo el análisis se hizo sobre un conjunto sintético —lo dicen en la página 14 y lo repiten en la 112—, pero en las diapositivas 7 y 10 la población aparece como 87.500 eventos históricos y 600.000 usuarios de CENS sin ese matiz: cuéntenme cómo generaron ese conjunto y qué de lo que concluyen sigue en pie sabiendo que los patrones que el modelo aprendió los pusieron ustedes al generar los datos.»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Pregunta 2 — Sus propios criterios de éxito**

> «Ustedes fijaron como resultados esperados un AUC superior a 0,75 y un recall mínimo del 70 % —página 28—, y lo que obtuvieron fue un AUC de 0,616 con XGBoost y un recall máximo de 0,297 con Random Forest: ¿por qué esa comparación no aparece en las conclusiones y qué lectura técnica hacen de esa distancia?»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Pregunta 3 — La existencia del producto**

> «En la página 71 y en la diapositiva 13 hablan de un prototipo funcional en Streamlit que integra el modelo y SHAP, pero entre las dieciséis figuras del documento no hay ni una captura del tablero: ¿está corriendo hoy, y pueden describirme qué se ve en pantalla cuando se consulta el activo ACT-012907?»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Reserva (solo si sobra tiempo):** desbalance de clases y su tratamiento · umbral de decisión elegido y por qué · particiones y fuga de información en el panel activo-semana · el 18 % que no cuadra (p. 49)

## D · AL CIERRE — rodear el rango y poner la nota

- **Meritoria:** no la propondría con AUC 0,616, la hipótesis 1 sin contrastar y el 18 % de la p. 49 sin conciliar, salvo defensa sobresaliente en los cuatro puntos. Si pongo 4,4, la página es la 28 contra la 97.

**Partida antes de oír (§7 de la ficha):** 4,0 – 4,4 es el escenario más probable a la luz de los dos documentos.

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
