# CDigital — poner contenido evaluativo en el campus virtual sin hacerlo a mano

`cdigital.py` habla con **CDigital** (<https://cdigital.cun.edu.co>), el Moodle de la CUN: importa
bancos de preguntas en **Moodle XML**, apunta los cuestionarios de plantilla a esos bancos, sube
material de estudio como recurso y controla la visibilidad de cualquier actividad. Es la herramienta
del **«alistamiento del aula»** (ver más abajo).

## Uso

```bash
python config/moodle/cdigital.py estado
python config/moodle/cdigital.py curso 115463
python config/moodle/cdigital.py preguntas --curso 115463
python config/moodle/cdigital.py importar "ruta/al/banco.xml" --curso 115463 --simular
python config/moodle/cdigital.py importar "ruta/al/banco.xml" --curso 115463
python config/moodle/cdigital.py borrar-categoria "Quiz 1 - ..." --curso 115463 --confirmar
python config/moodle/cdigital.py quiz 6745720
python config/moodle/cdigital.py quiz-sustituir 6745720 --categoria 4976278,8271261 --confirmar
python config/moodle/cdigital.py quiz-sustituir 6745720 --categoria 4976278,8271261 --dejar-oculto --confirmar
python config/moodle/cdigital.py quiz-ordenar 6745720 --xml "ruta/al/banco.xml" --dejar-oculto --confirmar
python config/moodle/cdigital.py subir-recurso "ruta/Material U2.docx" --curso 115463 --seccion 3 --confirmar
python config/moodle/cdigital.py subir-carpeta "ruta/S01.pptx" "ruta/S02.pptx" --curso 115463 --nombre "Presentaciones de clase" --confirmar
python config/moodle/cdigital.py fechas 115463 --confirmar
python config/moodle/cdigital.py fechas 115463 --incluir-visibles --confirmar
python config/moodle/cdigital.py aviso 115463 "Asunto" "<p>Cuerpo en HTML</p>" --confirmar
python config/moodle/cdigital.py ocultar 7705987
python config/moodle/cdigital.py mostrar 7705987
```

**`--simular` siempre primero.** Valida el XML como lo validaría Moodle (una sola opción correcta
por pregunta, fracciones que sumen 100, ninguna opción vacía, categoría declarada) y muestra a qué
categoría iría, **sin tocar el aula**. Estos cursos tienen estudiantes matriculados.

`subir-recurso`, `subir-carpeta` y `visibilidad` son las piezas que permiten dejar el aula completa
sin activarla: nacen **ocultas** salvo que se pase `--visible`, y `quiz-sustituir --dejar-oculto` deja
el cuestionario oculto en vez de restaurar la visibilidad que traía.

`subir-recurso` publica **un** documento como actividad «Archivo»; `subir-carpeta` publica **varios**
en una sola actividad «Carpeta». La diferencia importa a escala: el material de los cinco cursos son
167 archivos contando que Trabajo de Grado 3 se importa en tres aulas. Como «Archivo» sueltos serían
167 actividades que revisar y activar una por una; en cuatro carpetas por aula son 28. El estudiante
ve la lista de archivos igual y puede descargar la carpeta completa.

Si una importación sale mal, `borrar-categoria` la deshace: borra las preguntas y después la
categoría. Sirve para reintentar sin quedarse con preguntas duplicadas en el banco — que es el único
desenlace de verdad molesto de este flujo, porque Moodle no detecta duplicados al importar.

**Importar no basta.** Las preguntas quedan en el banco, pero ningún cuestionario las sirve todavía:
para eso está `quiz-sustituir`. Ver «Los cuestionarios de plantilla» más abajo.

`quiz-ordenar` sirve para lo que `quiz-sustituir` **no puede**: cambiar el orden de las preguntas que
el cuestionario ya tiene. Toma el orden del `.xml` maestro —que es el que manda— y aborta si las
preguntas del cuestionario no son exactamente las del archivo: reordena, nunca añade ni borra.

## `fechas` — poner las ventanas del aula iguales a las del repositorio

La fuente única de las fechas de entrega es `config/cursos/fechas_entrega_aca.py`, **no el aula**: es
la decisión del Docente y es la que ya llevan impresa las guías `.docx` que tienen los estudiantes.
La plantilla institucional deja a todos los ítems una misma ventana genérica que no corresponde a
ninguna sesión (en Proyecto I decía enero de **2028**; la Coevaluación de Creatividad, **2030**).

Este sitio **no tiene editor masivo de fechas** —`/report/editdates/index.php` y
`/admin/tool/dates/index.php` dan 404— y Moodle 4.5 no expone un servicio web para cambiarlas, así
que la única vía es reenviar el formulario completo de `/course/modedit.php`. Eso es delicado: un
campo que se pierda en el camino es un ajuste que se borra. Tres defensas, en este orden:

1. **Round-trip nulo.** Antes de escribir nada se reenvía el formulario *idéntico* y se comprueba que
   el aula no cambió. Si un reenvío igual altera algo, el parser no es fiel y la escritura se aborta.
2. **Orden del documento.** Los campos viajan como lista de pares, no como diccionario: el patrón
   `advcheckbox` de Moodle pone un `<input type=hidden name=X value=0>` justo antes del checkbox
   `name=X value=1`, y PHP se queda con el último. Un diccionario perdería la casilla marcada.
3. **Relectura.** Después de guardar se vuelve a leer del servidor y se compara con lo pedido.

Una trampa que costó un aborto en falso: los selectores de fecha **desactivados** los pinta Moodle
con la hora actual, así que entre dos cargas de la misma página cambian solos (`:29` → `:30`). Se
excluyen de la comparación los que no tienen su `[enabled]` marcado.

Por defecto **sólo toca los ítems ocultos**. Los visibles se saltan y se listan: cambiarle la fecha a
un ítem visible le mueve el calendario a los estudiantes matriculados, y eso se decide a mano
(`--incluir-visibles`).

## `aviso` y los recordatorios automáticos

El foro **«Avisos»** existe, es visible y tiene **suscripción forzada** en las 7 aulas: publicar un
tema ahí manda correo a todos los matriculados desde el servidor de la CUN. Sin cuenta de correo del
Docente en el circuito, sin contraseña de aplicación —que esta cuenta institucional no puede
generar— y sin cuota que se pueda agotar.

El id que pide `/mod/forum/post.php?forum=N` **no es el cmid**, es el de la instancia del foro, y
según cómo pinte el aula la página aparece de tres formas distintas; `foro_avisos()` las prueba en
orden (`<input name="forum">`, el enlace `post.php?forum=`, y `instance` en el formulario de
ajustes). Los siete, a 15/08/2026: `111070`→770097, `112321`→778919, `115463`→906293,
`116387`→802859, `129268`→885879, `129270`→885889, `130378`→897760. Se redescubren solos.

**`desde` programa el aviso y esa es la parte importante.** Con «Mostrar período» (`timestart`) el
tema se publica hoy pero el correo lo retiene el cron del propio campus hasta la fecha indicada: no
hace falta que este computador esté encendido el día del recordatorio, ni un planificador en la nube.
`mailnow` no se salta esa espera —las dos condiciones van unidas en la consulta del cron—, sólo evita
el retardo extra de la ventana de edición cuando la fecha llega. Un aviso programado se puede borrar
antes de su fecha sin que salga ningún correo: por eso es reversible.

El planificador que usa todo esto es `config/cursos/recordatorios.py`. Ver su cabecera.

**Lo único que no está probado contra el servidor es el POST final.** Se verificó el camino completo
—login, censo del aula, descubrimiento del foro, lectura del formulario y armado del envío en los 7
foros— pero no la publicación, porque probarla es mandarles un correo de prueba a 282 estudiantes.
El primer aviso de verdad es también su prueba: hacer el primero con una sola aula y mirarlo.

## Credenciales

Viven en `%LOCALAPPDATA%\cdigital-cun\credenciales.json`, **fuera de este repositorio**, que está en
git *y* sincronizado a Google Drive: cualquier archivo escrito aquí se replica y queda en el
historial. El formato es `{"url": ..., "usuario": ..., "clave": ...}`.

## Aula del POC

| Cosa | Valor |
|---|---|
| Curso | CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS / 54408 / PRIMER BLOQUE / 26V04 |
| `courseid` | 115463 |
| `contextid` | 8271261 |
| Actividades | **34**, en «General» + Temas 1-8 (8 SCORM «Contenido N», 6 cuestionarios, 3 encuestas de evaluación docente, foros, ACA Final, etiquetas) |
| Cuestionarios | **6**, todos de la plantilla y todos visibles: Quiz 1 `6745720`, Parcial 1 `6745722`, Quiz 2 `6745725`, Parcial 2 `6745727`, Autoevaluación `6745735`, Quiz 3 `6745736` |
| Categorías del banco | 7 en el contexto del curso: 6 heredadas de la plantilla + `Quiz 1 - Creatividad U1-U2` (`4976278`), la nuestra. Cada quiz tiene además **su propio contexto de módulo** con su «Por defecto en …» |

## Los cuestionarios de plantilla — el paso que falta después de importar

El aula no se crea vacía. La plantilla (`plantilla_cero` / `PEE26042019`) trae los **seis
cuestionarios ya creados, visibles y abiertos**, y cada uno con **10 slots aleatorios** que sacan
preguntas de su propia categoría «Por defecto en \<nombre del quiz\>», en el **contexto del módulo**.
Las preguntas importadas caen en una categoría del **contexto del curso**. Son dos sitios distintos:
importar el banco no cambia lo que responde el estudiante. Antes del arreglo, los cinco
cuestionarios evaluativos del aula 115463 servían las **mismas 15 preguntas de plantilla**: el mismo
examen cinco veces.

Un slot aleatorio no se puede reapuntar: **`editrandom.php` devuelve 404 en Moodle 4.5**. Hay que
sustituir los slots, y eso hace `quiz-sustituir`: añade las preguntas indicadas, borra las
anteriores, repagina, verifica y restaura la visibilidad original —o la deja oculta con
`--dejar-oculto`. Aborta si el cuestionario ya tiene intentos, y si algo falla lo deja **oculto** a
propósito.

**Y no todas las aulas vienen igual.** De las 7 aulas del periodo 2026-2, sólo la **115463**
(Creatividad) trae los slots aleatorios de plantilla. En las otras seis —111070, 129268, 112321,
116387, 129270 y 130378— los cuestionarios evaluativos tienen **0 slots**: están *vacíos*, con
puntuación total 0.00… **y visibles y abiertos desde el 11/08/2026**. Un cuestionario vacío pero
visible no es una precaución, es un fallo: el estudiante entra, no ve preguntas y su intento cuenta.
Para esas aulas no hay nada que sustituir, sólo **añadir**; `sustituir_slots` trata `viejos == []`
sin quejarse. Censar antes de tocar no es opcional.

## Alistamiento del aula

Es el nombre del proceso completo: dejar el curso **puesto y completo en la plataforma, pero
OCULTO** — listo para que el Docente lo revise a mano y lo active él. Nunca se activa nada en su
nombre. El orden:

1. **Censar** intentos, slots y visibilidad de todos los cuestionarios del aula. Uno con intentos
   ≠ 0 **no se recompone jamás**; la herramienta aborta sola, pero el censo evita descubrirlo tarde.
2. **Importar** el banco: `importar … --simular` y después de verdad.
3. **Apuntar** el cuestionario: `quiz-sustituir <cmid> --categoria <catid,ctxid> --dejar-oculto
   --confirmar`. Sin `--dejar-oculto` restaura la visibilidad que encontró, que es lo contrario de lo
   que quiere el alistamiento.
4. **Material de estudio** en cuatro carpetas ocultas por aula, en la sección 0 («General»):
   «Presentaciones de clase», «Guías de las ACAs y de los cuestionarios», «Lecturas obligatorias» y
   «Recursos del curso». Con `subir-carpeta … --nombre "<carpeta>" --seccion 0`.

   **No se reparte por sesiones a propósito.** Las secciones del aula institucional («Tema 1…Tema 8»)
   no se corresponden una a una con las sesiones de clase: Investigación tiene 6 sesiones y 8
   secciones; TG3, 15 sesiones y 9 secciones. Cualquier reparto automático sería una adivinanza que
   el Docente tendría que verificar archivo por archivo — justo lo contrario de «listo para revisión
   manual». Puestas juntas y ocultas, se arrastran a donde toque en dos gestos.
5. **Informar por aula** qué quedó puesto, qué quedó oculto y qué decidió la herramienta sola.

Dos detalles de contexto que cambian el trabajo: **una carpeta del repositorio puede ser varias aulas
del campus** —Trabajo de Grado 3 es una carpeta y son tres aulas (54450 → 112321, 54466 → 116387,
54467 → 129270)—, así que las categorías del banco se nombran **sin el número de grupo** y el mismo
`.xml` se importa tres veces. Y las preguntas evalúan **tema, no asignatura**: contenido que aparece
en la presentación, no pesos, fechas, créditos ni reglas de IA.

## Por qué por formulario y no por servicios web

Moodle **no tiene** un servicio web para crear preguntas: las funciones `mod_quiz_*` sirven para
*resolver* cuestionarios, y no existe ningún `core_question_create`. El único camino es el mismo que
usa la interfaz. Son dos pasos, y el primero no es evidente:

1. **Subir el archivo al área de borradores** — `POST /repository/repository_ajax.php?action=upload`
   con `sesskey`, `itemid` (el valor del campo oculto `newfile`), `savepath=/`, `author`, `license` y
   el archivo en `repo_upload_file`. El repositorio «Subir un archivo» es **`repo_id=5`** en esta
   instalación; ese número sale del JSON del *filepicker*, que viene escapado dentro de una cadena de
   JavaScript (hay que deshacer `\"` y `\/` antes de buscarlo).
2. **Enviar el formulario de importación** — `POST /question/bank/importquestions/import.php` con
   `sesskey`, `courseid`, `context`, `_qf__qbank_importquestions_form_question_import_form=1`,
   `format=xml`, `category=<catid>,<contextid>`, `matchgrades`, `stoponerror`,
   `newfile=<itemid del paso 1>` y `submitbutton=Importar`. Con `catfromfile=1` y `contextfromfile=1`
   manda la categoría declarada en el XML (`<question type="category">`) y Moodle la crea si no
   existe — que es lo que queremos: cada quiz en su propia categoría.

Respuesta de éxito: la página contiene «Importando N preguntas desde archivo».

## Cosas que cuestan un rato descubrir

1. **Los campos ocultos no se pueden leer con una expresión posicional.** Moodle intercala atributos:
   `<input type="hidden" name="newfile" id="id_newfile" value="310962382" .../>`. Buscar
   `name="newfile"\s+value=` falla en silencio. Hay que extraer todos los `<input>` y armar un
   diccionario `name → value`.
2. **El `sesskey` cambia en cada carga de página.** Hay que tomar el de la página desde la que se va
   a enviar el formulario, no reutilizar uno anterior.
3. **`confirm` no es `1`, es un hash.** Al borrar una pregunta, `deletequestion/delete.php` genera un
   `confirm` md5 que hay que devolver tal cual; inventarse `confirm=1` da un 404. Y una categoría con
   preguntas dentro **no se puede borrar**: Moodle obliga a moverlas. Por eso `borrar-categoria`
   borra primero las preguntas y después la categoría vacía.
4. **La página de un curso no trae sus actividades.** En Moodle 4.5 sólo la sección «General» viene
   servida en el HTML; los Temas 1-8 los pinta el navegador. Raspar `/course/view.php` o
   `/mod/quiz/index.php` reporta de menos, y así se llegó a afirmar que un aula con 34 actividades y
   6 cuestionarios tenía «4 recursos y ningún cuestionario». La fuente correcta es el servicio
   `core_courseformat_get_state` (`POST /lib/ajax/service.php`), que devuelve **todos** los módulos,
   incluidos los ocultos. Eso usa `CDigital.estado_curso()`.
5. **Los botones de la página de edición de un quiz no son enlaces.** «Borrar» un slot es un
   `<a>` con `data-action="delete"`: el GET a su `href` (`edit.php?…&remove=N`) responde 200 y **no
   hace nada**. El JavaScript hace en realidad `POST /mod/quiz/edit_rest.php` con
   `class=resource, action=DELETE, id=<slotid>`, y el `slotid` es el número de `id="slot-…"` del DOM.
   Los saltos de página son el mismo endpoint con `field=updatepagebreak, value=2|1`. Añadir sí
   funciona por GET: `edit.php?cmid=…&sesskey=…&addquestion=<qid>&addonpage=0`.
6. **La consola de Windows es cp1252.** Un `print` con «←» o con una tilde revienta el proceso a
   mitad del informe. `cdigital.py` reconfigura `stdout` a UTF-8 al importarse; con `reconfigure`,
   no envolviendo en `TextIOWrapper`, porque envolver dos veces cierra el buffer del que ya lo hizo.
7. **En el banco, el nombre de la pregunta no está donde en el quiz.** En `/question/edit.php` es un
   campo editable en línea (`data-itemtype="questionname" data-itemid=… data-value=…`); en
   `/mod/quiz/edit.php` es un `<span class="questionname">`.
8. **`availabilityconditionsjson` es un `<textarea>` vacío, y sin él no se crea nada.** El
   diccionario de campos ocultos se arma leyendo `<input>`, y ese campo no es un `<input>`: es un
   `<textarea>` que el JavaScript de Moodle rellena en el navegador. Enviar el formulario sin él da
   **HTTP 404 «Invalid JSON from availabilityconditionsjson»**, un error que no menciona el campo que
   falta sino el que llegó vacío. Hay que mandarlo a mano: `{"op":"&","c":[],"showc":[]}`.
9. **Crear un recurso son los mismos dos pasos que importar, con otro formulario.**
   `GET /course/modedit.php?add=resource&type=&course=<id>&section=<n>&return=0&sr=0` devuelve 37
   campos, entre ellos `files` (el itemid del borrador), `context`, `module=19` y
   `modulename=resource`; el archivo sube a `repository_ajax.php?action=upload` con `repo_id=5` e
   `itemid=<files>`; y el `POST /course/modedit.php` necesita además `visible` (**1** = Mostrar,
   **0** = Ocultar), `display=0`, `printintro` y `submitbutton2`. Ojo con el sentido de `visible`:
   es al revés de lo que sugiere el nombre del botón «Ocultar».
10. **Para ocultar o mostrar basta un GET.** `/course/mod.php?sesskey=<sk>&hide=<cmid>` y `&show=`.
    Lo que no viene en la respuesta es a qué curso pertenece el `cmid`, y hace falta para verificar:
    se saca de `/course/modedit.php?update=<cmid>`, del `name="course" value="(\d+)"`.
11. **Una «Carpeta» con varios archivos es el mismo formulario, con todas las subidas al MISMO
    borrador.** `GET /course/modedit.php?add=folder&…` trae `module=9`, `modulename=folder` y un
    `files` que es el itemid del área de borradores; se sube archivo por archivo a
    `repository_ajax.php?action=upload` repitiendo ese `itemid`, y el `POST` final necesita
    `showexpanded`, `showdownloadfolder`, `display` y el mismo `availabilityconditionsjson` a mano.
    Dos cuidados: el nombre del archivo dentro de la carpeta es el del `multipart`, **no** el del
    disco —así se le puede poner «03 - Gestion de la innovacion.pptx» a un archivo que en el
    repositorio se llama `Presentacion.pptx`, y hay que hacerlo, porque 15 sesiones traen 15 archivos
    llamados igual y `overwrite=1` los iría pisando uno tras otro—, y conviene transliterar acentos y
    «·» antes de subir, para que la verificación final pueda buscar el nombre exacto en la vista de
    la carpeta sin tropezar con lo que Moodle reescriba.
12. **Las categorías del banco no se pueden renombrar desde aquí.** No hay endpoint:
    `category.php?courseid=<id>&edit=<catid>` no pinta formulario de edición —sólo un `<select>` de
    salto— y la página de gestión no emite el `data-inplaceeditable` / `data-itemtype` /
    `data-component` que usa el editor en línea de Moodle para otras cosas. Cuando hace falta
    canonizar el nombre de una categoría que ya existe, el camino es **importar y borrar**: crear una
    temporal, apuntar el cuestionario a ella, borrar la vieja, reimportar con el nombre bueno y
    borrar la temporal. Nunca se queda sin preguntas en medio porque `sustituir_slots` añade antes de
    borrar. Ojo también con que `borrar-categoria` **se niega** si hay dos categorías con el mismo
    nombre: no puede saber cuál es la que sobra.

13. **Moodle no añade dos veces la misma pregunta al mismo cuestionario, así que reordenar no se
    puede hacer sustituyendo.** `quiz-sustituir` añade antes de borrar —para que el cuestionario no
    quede vacío ni un segundo—, pero si las preguntas que va a añadir ya están dentro, el GET a
    `addquestion` responde **200 y no crea slot**, y la comprobación «añadir no creó un slot» aborta
    con razón. El orden se cambia con el endpoint del arrastrar-y-soltar de la página, que la
    interfaz no expone de otra forma: `POST /mod/quiz/edit_rest.php` con `class=resource`,
    `field=move`, `id=<slotid>`, `sectionId=<el número de id="section-…">`, `previousid=<el slot que
    queda delante>` —se **omite** si va primero— y `page=<número de página>`. Los parámetros salen del
    módulo YUI `moodle-mod_quiz-dragdrop`
    (`/theme/yui_combo.php?m/<rev>/mod_quiz/dragdrop/dragdrop-min.js`), no del HTML. Para que `page`
    no sea una adivinanza, `quiz-ordenar` **aplana a una sola página**, mueve, y repagina al final.

El nombre del usuario no aparece en el HTML del panel; se lee de `/user/profile.php`.

## Verificado

- **2026-08-15, importación.** Se importó un XML de una sola pregunta al aula 115463, se comprobó que
  llegó al banco en su propia categoría, y se borró la pregunta y la categoría: el banco quedó con
  las mismas 6 categorías originales. La tubería completa —subida, importación y deshacer— está
  probada contra el servidor real, no supuesta.
- **2026-08-15, sustitución de slots (primera prueba).** `Quiz 1` (cmid `6745720`) pasó de 10 slots
  aleatorios sobre «Por defecto en Quiz 1» a servir 10 preguntas concretas de
  `Quiz 1 - Creatividad U1-U2`, en orden, 1.00 cada una, puntuación total 10.00 sobre nota máxima 5,
  en 5 páginas de 2. Con **0 intentos antes y después**. Aquellas 10 preguntas eran `CRE-Q01…CRE-Q10`
  y **ya no son las que sirve**: cinco de ellas evaluaban la asignatura (orden de las partes, qué
  traer escrito, peso del quiz, créditos y horas, verificación de citas de la IA) y se reemplazaron
  por `CRE-Q06…CRE-Q15`, de tema. Lo que quedó puesto es lo de la entrada siguiente.
- **2026-08-15, recurso oculto.** Se creó un recurso de prueba en el aula 115463, se comprobó por
  `estado_curso()` que nacía con `visible=False`, y se borró. Después se publicó de verdad el
  `Material de estudio U2 - Bloqueadores y ensanchadores de la creatividad.docx` en la sección 3
  («Tema 2»), junto al Quiz 1: **cmid `7705987`, oculto**, confirmado releyendo el estado del curso.
- **2026-08-15, censo de cuestionarios.** Los **38 cuestionarios** de las 7 aulas tienen **0
  intentos**: nada está bloqueado. Y 5 aulas de 7 tienen cuestionarios evaluativos **vacíos pero
  visibles y abiertos** (p. ej. cmid `6522194`: 0 slots, puntuación 0.00, abre 11/08 cierra 20/09,
  2 intentos, 45 min).
- **2026-08-15, alistamiento completo de las 7 aulas.** Es la corrida de verdad, y la verificación es
  independiente: un script aparte releyó **el servidor** y lo comparó contra los `.xml` del
  repositorio, sin fiarse de lo que dijeron los pasos que escribieron.
  **31 cuestionarios · 31 sin problema** y **28 carpetas · 28 sin problema**, ninguna alarma. Cada
  cuestionario: 10 slots concretos (ningún aleatorio), puntuación total 10.00, **0 intentos**,
  **oculto**, y los nombres de las preguntas **en el mismo orden que su `.xml`**. Cada carpeta:
  presente, **oculta**, y con cada nombre de archivo encontrado uno por uno en
  `/mod/folder/view.php` — **167 archivos**, 16,3 MB, en la sección 0 de las 7 aulas. Los 21 bancos
  maestros se importaron 31 veces (los 5 de TG3, tres veces cada uno). El inventario aula por aula,
  con los 59 cmid, está en `ALISTAMIENTO CDigital 2026-08-15.md`, en la raíz del repositorio.
- **2026-08-15, las dos mezclas.** Reordenar los slots sólo sirve si el estudiante ve ese orden, así
  que se leyó la casilla de la página de edición en los 31 cuestionarios: **«Reordenar las preguntas
  al azar» está desactivada en los 31**, luego el orden del `.xml` maestro es el que llega.
  «Mezclar dentro de las preguntas» (`shuffleanswers`) está en **Sí** en los 31, heredado de la
  plantilla, y se dejó así: se revisaron las 210 preguntas de los 21 bancos y **ninguna depende de la
  posición de una opción** —ni un «todas las anteriores»; los siete casos donde aparece «opción A / B»
  son las alternativas del proyecto descritas en el enunciado, no letras de respuesta—.
  La casilla es `<input type="checkbox" id="shuffle-<sectionid>">` en `/mod/quiz/edit.php` (sin
  atributo `checked` = desactivada) y el desplegable es `name="shuffleanswers"` en
  `/course/modedit.php?update=<cmid>`.
- **2026-08-15, reordenar slots.** `Quiz 1` de Creatividad (cmid `6745720`) servía las 10 preguntas
  buenas pero en orden de código (`CRE-Q06`→`CRE-Q15`), porque `preguntas_de_categoria` las lista
  así; su `.xml` maestro tiene un orden deliberado (`CRE-Q11, Q10, Q12, Q09, Q13, Q14, Q08, Q07,
  Q15, Q06`) y es el único de los 21 bancos escrito fuera del orden del código —los otros 20
  coincidían por casualidad. `quiz-ordenar` lo dejó en el orden del maestro con **9 movimientos**,
  puntuación total 10.00 igual que antes, **0 intentos** y oculto. La verificación completa volvió a
  correr después: 31/31.
- **2026-08-15, fechas.** Los **53 ítems evaluativos** de las 7 aulas discrepaban del repositorio:
  todos. `fechas` corrigió los **31 ocultos** y dejó los **22 visibles** como estaban. La comprobación
  la hizo un script aparte que releyó `/course/modedit.php` de los 53: **31 coinciden, 22 discrepan**,
  y los 22 son exactamente los visibles. Están listados uno por uno, con cmid y con los dos valores,
  en `ALISTAMIENTO CDigital 2026-08-15.md` §5. Lo peor que decía el aula: Proyecto I anunciaba sus dos
  ACAs para **enero de 2028** y Creatividad, la Coevaluación para **2030**; seis Coevaluaciones no
  tienen fecha ninguna. El round-trip nulo se disparó una vez de verdad (cmid `6785577`) y era un
  falso positivo por los selectores desactivados; se arregló y volvió a correr limpio.
- **2026-08-15, foro de avisos: verificado todo menos el envío.** Los 7 foros «Avisos» existen, están
  visibles y tienen suscripción forzada; sus 7 ids de instancia se descubrieron solos; el formulario de
  `/mod/forum/post.php` se leyó y se armó el envío completo en los 7, con `mailnow` y con `timestart`.
  **No se publicó nada**: cada publicación es un correo a los 282 estudiantes matriculados y no hay
  aula de pruebas donde ensayar (la más pequeña, TG3 grupo 54450, tiene 13). El POST final es el único
  paso sin probar de toda la herramienta, y está dicho arriba a propósito.
