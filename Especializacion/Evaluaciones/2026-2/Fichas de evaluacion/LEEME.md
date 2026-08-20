# Cómo se usa esta carpeta

Soy **Jurado 2** de 13 proyectos de la Especialización en Transformación Digital (26ET2): **9 el martes
18 de agosto** (6:00–9:00 p. m.) y **4 el miércoles 19** (6:00–7:20 p. m.). Veinte minutos por
proyecto, de los que unos **3 son míos**. Esta carpeta existe para que esos 3 minutos rindan.

## La estructura

Una subcarpeta por proyecto, numerada por **orden de sustentación**, así que el orden alfabético del
explorador es el orden de la sesión: `01 - G-001 - …` hasta `13 - G-013 - …`. Dentro, siempre los
mismos cuatro nombres, numerados por el orden en que se usan:

| Archivo | Qué es |
|---|---|
| `1 - Ficha de preparacion.md` / `.docx` | las 9 secciones de siempre: resumen de 5 minutos, coherencia, fortalezas, **huecos del documento**, **huecos de las diapositivas** (qué proyectan y qué mirar en pantalla), preguntas antes y después, umbrales de nota, observaciones administrativas — más la **§8.1**, el formulario oficial del jurado con su casilla propuesta y la página que la sostiene. Se lee; no se escribe en ella |
| `2 - Hoja de respuestas.md` / `.docx` | **lo único que se tiene delante en sala.** Las tres preguntas de ese grupo ya impresas, con casillas y huecos, y la **§E** con las cinco casillas del formulario oficial para rodear. Se llena a mano |
| `3 - Transcripcion.md` | donde se pega la transcripción de la llamada, **si llega**. **No entra a git** |
| `4 - Evaluacion.md` | la evaluación posterior, criterio por criterio con la rúbrica de Proyecto II · ACA 3 (p. 22). Sí entra a git |

El índice y la agenda hora por hora están en `00 - Indice y agenda de sustentaciones.md`.

## El flujo

**Antes de la sala** — 5 minutos por grupo: de la ficha, solo la §1 (resumen), la §4 (huecos del
documento) y la §5 (qué mirar en pantalla mientras proyectan). Imprimir o abrir en tableta las 13 `2 - Hoja de respuestas.docx`.

**En la sala** — la hoja de respuestas delante, la ficha al lado por si hay que confirmar una página.
Mientras exponen se marca todo en la primera cara: §A qué bloque cubrieron y una frase por bloque, las
casillas **REQUISITOS PARA 4,6+** (se cumplen mientras hablan, no al final) y §B qué condicional se
cumplió —cada marca trae su página y, cuando existe, la pregunta literal—; lo que contesten a un
condicional va en el bloque **RESPUESTAS A LOS CONDICIONALES Y A LA RESERVA**, con su número delante.
En mis 3 minutos se lee la pregunta **tal como está escrita** en la §C y se anota la frase textual en
sus tres renglones. Al cerrar se rodea el rango de cada criterio en la §D y se escribe la nota única en
`NOTA QUE REPORTO`; y en la §E se confirman o se corrigen las cinco casillas del formulario oficial.
Escribir es rellenar, no redactar.

**Dos instrumentos distintos, y no se mezclan.** La **nota del acta** sale de los cuatro criterios
internos de la §D en escala 0,1–5,0 (75 % metodólogo + 25 % jurados; meritoria ≥ 4,6 sin ninguna
individual por debajo de 4,5). El **formulario de la Dirección** son otras cinco preguntas en escala
**1–5**, y **ninguna de las cinco califica la sustentación oral**: las cinco se responden con el
documento. Por eso vienen precargadas y en sala solo se confirman. Su suma sobre 25 **no se convierte**
a la escala del acta. Vive en tres sitios, los tres generados del mismo dato:
`config/evaluaciones/formulario_jurado.py` escribe la §3 de cada `4 - Evaluacion.md` y la §2.1 del
índice, y `config/evaluaciones/formulario_en_fichas.py` lleva ese mismo dato a la §8.1 de la ficha y a
la §E de la hoja, y rehace los `.docx`. **Si una casilla cambia, se cambia en `DATOS` del primero y se
vuelven a correr los dos** (`--simular` para ver, `--confirmar` para escribir); a mano se desincronizan.

**Después** — pegar la transcripción en `3 - Transcripcion.md` si la moderadora la comparte (lo normal
es que **no** llegue: la sala es suya y solo el anfitrión puede transcribir), y pasar la hoja escrita a
`4 - Evaluacion.md` con el agente `evaluador-proyectos-grado-cun`. Sin transcripción ni hoja, el agente
no evalúa: dice qué falta. De los cuatro archivos, el único que no entra a git es la transcripción.

## Tres reglas que no se negocian

- **Ninguna cédula en ningún archivo de esta carpeta.** El cronograma trae 196 y está fuera de git a
  propósito; de él se usan orden, código, título, fecha y hora. La transcripción tampoco se versiona:
  es voz sin revisar, con nombres y datos de empresas.
- **Mover sí, borrar no.** Esto se sincroniza con Google Drive. Los `desktop.ini` son de Drive: no se
  tocan.
- **La nota la pone el jurado humano**, contra los umbrales que la §8 de cada ficha escribió *antes* de
  oír nada. Si bajo de 4,5, tengo que poder decir la página: un 4,4 mío bloquea la meritoria del grupo.
