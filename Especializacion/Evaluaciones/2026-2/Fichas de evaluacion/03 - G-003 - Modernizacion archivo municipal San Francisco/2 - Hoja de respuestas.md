# 03 · 26ET2-G-003 — Análisis y modernización del archivo municipal de la Secretaría de Gobierno de San Francisco (Putumayo), vigencia 2024

**HOJA DE RESPUESTAS — se llena A MANO en sala.** martes 18 de agosto de 2026 · 6:40 – 7:00 p. m. · **Mi rol:** Jurado 2

**Entró** __:__ · **fin de la exposición** __:__ · **minutos usados** ____ · **fallas de plataforma:** _________________

**Quién habló y de qué** (única vía legítima para juzgar dominio individual):
- José Javier Galvis Noguera: _____________________________________________________________
- Eliana Naranjo Cortés: ________________________________________________________________
- Cristian David Forero Álvarez: __________________________________________________________
- Gloria Nahtaly Florez Susa: _____________________________________________________________

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

- [ ] Que sostengan en vivo la distinción de la Tabla 14 sin inflar el producto, corrigiendo ellos mismos la diapositiva del AES-256 —**sin (a) no hay 4,6**
- [ ] Una cifra concreta de la muestra del FUID con su criterio
- [ ] Que reconozcan que la verificación fue de laboratorio
- [ ] Que hablen al menos tres de los cuatro

## B · CONDICIONALES (§6 de la ficha) — marcar oyendo; cada marca elige la pregunta

> Lo que va entre « » se lee tal cual. La página en negrita es la que sostiene la pregunta: si la respuesta la contradice, se anota abajo con esa página.

- [ ] Si el video de la diapositiva 9 no corre o no lo alcanzan a mostrar → P3 y pedir descripción del prototipo por dentro
- [ ] Si el video muestra el prototipo funcionando → preguntar con qué datos y en qué entorno  **(p. 105)**
  - Preguntar así: «en el módulo de respaldos que acabo de ver, ¿ese respaldo cifrado se ejecuta o es la vista de la función proyectada?»
- [ ] Si dicen que el sistema «está implementado en la Alcaldía» → P3, directa  **(p. 105)**
- [ ] Si presentan la reducción de 45-90 min a menos de 5 como resultado obtenido → pedir la medición y su n  **(p. 92)**
- [ ] Si afirman que capacitaron al personal → pedir fecha, número de funcionarios y evidencia  **(p. 27)**
- [ ] Si dicen «muestra censal» en la exposición → P2, directa  **(pp. 78, 86 y 130)**
  - Preguntar así: «¿fue una muestra o el censo?»
- [ ] Si el diagnóstico se presenta como el resultado principal y el prototipo queda de adorno → pedir que expliquen qué decisión de diseño del SGDEA salió directamente de un hallazgo del diagnóstico; el documento tiene la respuesta buena (los cuatro hallazgos críticos que originan el RBAC, p. 95)
- [ ] Si no mencionan una sola limitación → preguntar directamente cuáles son los tres límites del trabajo y qué no se puede concluir de él; es el hueco de la sección 5 (pp. 23-32)
- [ ] Si solo habla uno o dos integrantes → pedir explícitamente a quien no habló que explique su parte: al que sostenga la parte archivística, cómo se construyó el DCF de tres niveles (p. 88); al de la parte técnica, cómo se probó la persistencia (CP-01, p. 109)
- [ ] Si atribuyen a la plataforma el «blindaje jurídico» de la Secretaría (p. 134) → preguntar qué obligación normativa concreta queda cubierta hoy y cuál solo quedará cubierta cuando se implemente, en particular frente a la Ley 1581 de 2012, que el propio diagnóstico calificó en 1/5 (p. 80) y cuyo protocolo se recomienda redactar (p. 136)
- [ ] Si el director ya preguntó por la muestra o por el estado del prototipo → pasar a P1 y a reserva
- [ ] Si se pasan de tiempo y saltan resultados → ir directo al objetivo 4
  - Preguntar así: «¿qué se verificó, dónde y con quién?»

**RESPUESTAS A LOS CONDICIONALES Y A LA RESERVA** — número del condicional (o «R» si es de reserva) y lo que contestó, con cifras y nombres tal como los diga.

____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________
____  ___________________________________________________________________________________

## C · MIS 3 MINUTOS — leer la pregunta tal cual está escrita

**Pregunta 1 — Qué quedó implementado y qué está solo representado**

> «Su Tabla 14 distingue con mucho cuidado lo implementado y probado de lo que está solo representado en la interfaz, y ubica el cifrado AES-256 y el hash SHA-256 en el segundo grupo. La diapositiva 10 concluye, en cambio, que se verificó la integridad con cifrado AES-256. ¿Me pueden precisar qué quedó implementado y probado en el prototipo y qué está representado a nivel de interfaz?»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Pregunta 2 — Cuántos expedientes se inventariaron de verdad**

> «El documento precisa tres veces que el FUID se aplicó sobre una muestra y no sobre el censo de la vigencia 2024, mientras la diapositiva 4 dice muestra de tipo censal. ¿Cuántos expedientes o cuántos folios quedaron efectivamente inventariados, y con qué criterio se escogieron?»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Pregunta 3 — Quién usó el prototipo y con qué datos**

> «Su cuarto objetivo es verificar el prototipo en un entorno institucional controlado. La verificación documentada se hizo sobre un portátil personal, en localhost, y la implementación institucional aparece como proyectada. ¿Algún funcionario de la Secretaría usó el prototipo, y con qué datos: expedientes reales de 2024 o datos de prueba?»

`Contestó:  [ ] Sí   [ ] A medias   [ ] La esquivó`

`Frase textual:`
________________________________________________________________________________________
________________________________________________________________________________________
________________________________________________________________________________________

`Verificar después: p. ____`

**Reserva (solo si sobra tiempo):** el «blindaje jurídico» atribuido a la plataforma (p. 134) · qué de las cifras de las pp. 24, 92 y 113 es proyección · cómo funciona el prototipo por dentro: DCF, DRS, RBAC, persistencia

## D · AL CIERRE — rodear el rango y poner la nota


**Partida antes de oír (§7 de la ficha):** 4,0 – 4,4 es el escenario más probable con el estado de los dos entregables.

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
