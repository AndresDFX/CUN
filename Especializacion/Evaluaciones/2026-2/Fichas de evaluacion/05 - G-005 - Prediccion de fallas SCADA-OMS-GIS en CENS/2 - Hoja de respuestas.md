# 05 · 26ET2-G-005 — Comparación de modelos estadísticos y de Machine Learning para la predicción de fallas con SCADA, OMS y GIS en CENS

**HOJA DE RESPUESTAS — se llena A MANO en sala.** martes 18 de agosto de 2026 · 7:20 – 7:40 p. m. · **Mi rol:** Jurado 2

**Entró** __:__ · **fin de la exposición** __:__ · **minutos usados** ____ · **fallas de plataforma:** ________________________

**Quién habló y de qué** (única vía legítima para juzgar dominio individual):
- Edward Alexis Orduz Rodríguez: ______________________________________________________
- Ángel David Ortiz Rivera: ______________________________________________________

---

## A · MIENTRAS EXPONEN — marcar, no redactar

| Bloque (min esperados) | ✓ ~ ✗ | Una línea |
|---|:-:|---|
| Problema y pregunta (2 min) |  |  |
| Objetivos (1 min) |  |  |
| Método (2-3 min) |  |  |
| Resultados (3 min) |  |  |
| Discusión y conclusión (2-3 min) |  |  |
| Aporte y cierre (1 min) |  |  |

`[ ] leyeron las diapositivas`  ·  `[ ] el demo corrió`  ·  `[ ] dijeron «no sé» y reconduje`  ·  `[ ] contradijeron el documento (p. ____)`

## B · CONDICIONALES (§6 de la ficha) — marcar oyendo; cada marca elige la pregunta

- [ ] Si en toda la exposición no dijeron «sintético» ni «simulado» → P1, directa y primera
- [ ] Si sí lo declararon con claridad → soltar la mitad de P1 y pasar a P2
- [ ] Si mostraron el tablero funcionando → pedir la lectura del activo ACT-012907
- [ ] Si no mostraron el tablero pero afirmaron que existe → P3
- [ ] Si se pasaron de tiempo y saltaron el modelamiento → pedir en una frase el mejor modelo y su AUC
- [ ] Si afirmaron que el clima mejora la predicción → pedir la evidencia en su propia tabla
- [ ] Si dijeron «validado con CENS» o «con usuarios técnicos» → pedir nombre del área y fecha
- [ ] Si habló solo uno de los dos → repartir: uno los datos, otro el modelamiento

## C · MIS 3 MINUTOS — leer la pregunta tal cual está escrita

**Pregunta 1 — La naturaleza del dato y su ausencia en las diapositivas**

> «El documento dice con claridad que no hubo acceso a los sistemas productivos de CENS y que todo el análisis se hizo sobre un conjunto sintético —lo dicen en la página 14 y lo repiten en la 112—, pero en las diapositivas 7 y 10 la población aparece como 87.500 eventos históricos y 600.000 usuarios de CENS sin ese matiz: cuéntenme cómo generaron ese conjunto y qué de lo que concluyen sigue en pie sabiendo que los patrones que el modelo aprendió los pusieron ustedes al generar los datos.»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual: ______________________________________________________________________`

`Verificar después: p. ____`

**Pregunta 2 — Sus propios criterios de éxito**

> «Ustedes fijaron como resultados esperados un AUC superior a 0,75 y un recall mínimo del 70 % —página 28—, y lo que obtuvieron fue un AUC de 0,616 con XGBoost y un recall máximo de 0,297 con Random Forest: ¿por qué esa comparación no aparece en las conclusiones y qué lectura técnica hacen de esa distancia?»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual: ______________________________________________________________________`

`Verificar después: p. ____`

**Pregunta 3 — La existencia del producto**

> «En la página 71 y en la diapositiva 13 hablan de un prototipo funcional en Streamlit que integra el modelo y SHAP, pero entre las dieciséis figuras del documento no hay ni una captura del tablero: ¿está corriendo hoy, y pueden describirme qué se ve en pantalla cuando se consulta el activo ACT-012907?»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual: ______________________________________________________________________`

`Verificar después: p. ____`

**Reserva (solo si sobra tiempo):** desbalance de clases y su tratamiento · umbral de decisión elegido y por qué · particiones y fuga de información en el panel activo-semana · el 18 % que no cuadra (p. 49)

## D · AL CIERRE — rodear el rango y poner la nota

- **Para 4,6+ hacen falta las cuatro:** (1) que enuncien lo sintético sin que se les pregunte y expliquen cómo se generó; (2) que reconozcan que sus metas de AUC y recall no se alcanzaron y sostengan la lectura correcta de un AUC de 0,616 (priorización, no predicción determinística); (3) que muestren el tablero o den evidencia equivalente; (4) que ambos demuestren dominio y respondan bien una de reserva.
- **Meritoria:** no la propondría con AUC 0,616, la hipótesis 1 sin contrastar y el 18 % de la p. 49 sin conciliar, salvo defensa sobresaliente en los cuatro puntos. Si pongo 4,4, la página es la 28 contra la 97.

**Partida antes de oír (§7 de la ficha):** 4,0 – 4,4 es el escenario más probable a la luz de los dos documentos.

| Criterio | Rodear | Nota |
|---|---|:-:|
| Dominio del tema | 0,1–2,9 · 3,0–3,5 · 3,6–4,5 · 4,6–5,0 | ____ |
| Claridad | 0,1–2,9 · 3,0–3,5 · 3,6–4,5 · 4,6–5,0 | ____ |
| Coherencia del documento | 0,1–2,9 · 3,0–3,5 · 3,6–4,5 · 4,6–5,0 | ____ |
| Capacidad de defensa | 0,1–2,9 · 3,0–3,5 · 3,6–4,5 · 4,6–5,0 | ____ |

**Retroalimentación (fortalezas · ajustes requeridos · acciones):**

1. ______________________________________________________________________________
2. ______________________________________________________________________________
3. ______________________________________________________________________________

⚠️ **Un 5,0 es proponer laureada** y exige que el Jurado 1 coincida. **Un 4,4 en un solo criterio bloquea la meritoria del grupo:** si bajo de 4,5, tengo que poder decir la página.

**Taquigrafía:** ✓ lo dijo · ✗ no lo dijo · ~ ambiguo · ! contradice el documento (p. __) · ☐ verificar después
