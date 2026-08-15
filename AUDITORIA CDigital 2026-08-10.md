# Auditoría en CDigital — 10/08/2026

Se entró a `https://cdigital.cun.edu.co/` (Moodle **2024100701.01**) con Playwright, en **solo lectura**: no se modificó nada en la plataforma. Este documento es la **fuente de verdad** de lo que hay en el campus; donde nuestro material lo contradiga, manda el campus.

---

## 1. Aulas y enlaces (pendiente resuelto)

| Curso | Grupo | id aula | URL |
|---|---|---|---|
| Proyecto I | 54ES4 | 130378 | https://cdigital.cun.edu.co/course/view.php?id=130378 |
| Investigación C&T | 53339 | 111070 | https://cdigital.cun.edu.co/course/view.php?id=111070 |
| Creatividad | 54408 | 115463 | https://cdigital.cun.edu.co/course/view.php?id=115463 |
| Trabajo de Grado 2 | 54448 | 129268 | https://cdigital.cun.edu.co/course/view.php?id=129268 |
| Trabajo de Grado 3 | 54450 | 112321 | https://cdigital.cun.edu.co/course/view.php?id=112321 |
| Trabajo de Grado 3 | 54466 | 116387 | https://cdigital.cun.edu.co/course/view.php?id=116387 |
| Trabajo de Grado 3 | 54467 | 129270 | https://cdigital.cun.edu.co/course/view.php?id=129270 |

Viven en `config/cursos/carga_academica_2026.json` → `cursos.<key>.cdigital` (y por grupo en TG3). Resolutor: `sesiones_cun.cdigital_url(curso)`.

---

## 2. ⚠️ La estructura de evaluación del campus NO es la que tiene nuestro material

Esto es el hallazgo grande. El libro de calificaciones de cada aula ya está configurado, con **quices y parciales que nuestro material no menciona**.

### Los 4 cursos de pregrado — tres cortes, con quiz + parcial en cada uno

| Corte | Ítem | Tipo en Moodle | Peso (Inv · Crea · TG2) | Peso (TG3) |
|---|---|---|---|---|
| **Primer corte 30%** | Quiz 1 | Cuestionario | 6% | 6% |
| | Parcial 1 | Cuestionario | 24% | 24% |
| **Segundo corte 30%** | Quiz 2 | Cuestionario | 9% | 9% |
| | Parcial 2 | Cuestionario | 21% | 21% |
| **Tercer corte 40%** | ACA Final | Tarea | 32,8% | 32% |
| | Quiz 3 | Cuestionario | 4% | 4% |
| | Autoevaluación | Cuestionario | 1,6% | 2% |
| | Coevaluación | Foro | 1,6% | 2% |

### Proyecto I (ESP329) — estructura propia

| Corte | Ítem | Tipo | Peso |
|---|---|---|---|
| **Primer corte 25%** | Quiz | Cuestionario | 25% |
| **Segundo corte 25%** | ACA 1 | Tarea | 25% |
| **Tercer corte 50%** | ACA FINAL | Tarea | 42% |
| | Autoevaluación | Cuestionario | 4% |
| | Coevaluación | Foro | 4% |

### En qué contradice a nuestro material

1. **Existen quices y parciales, y pesan mucho.** El Parcial 1 vale **24%** por sí solo. Nuestro material no menciona ni un quiz ni un parcial en ningún curso.
2. **Solo hay UNA "ACA Final"** (Tarea) en el tercer corte. No existen ACA 1 / ACA 2 / ACA 3 como tres entregables, que es como está escrito todo nuestro material de pregrado.
3. **La autoevaluación y la coevaluación existen en los 5 cursos**, no solo en Proyecto I. Nuestro material afirma lo contrario, apoyado en el instructivo AFI. El campus manda.
4. **La coevaluación es un Foro**, no un cuestionario.
5. **TG3 no es «corte único 100%»** como dice su Syllabus: son tres cortes 30/30/40.
6. **Proyecto I:** el primer corte es un **Quiz** (25%), no la ACA 1 de formulación del problema. Lo que nuestro material llama ACA 2 es lo que el aula llama ACA 1.
7. La decisión previa de «cada ACA toma el 100% de su corte» **queda anulada**: el desglose real existe y es 6/24, 9/21, 32,8/4/1,6/1,6.

### Contenido institucional ya cargado (peso 0)

Paquetes SCORM presentes en las aulas: «Ingreso a la biblioteca virtual», «Desbloquea el Saber: Tarjetas Clave» (5 en Proyecto I) y «Contenido 1…8» (Creatividad). No suman nota.

Las aulas **no tienen secciones de contenido creadas** más allá del foro de Avisos: la estructura de evaluación está, el contenido está por subir.

---

## 3. Rosters — tus exportaciones venían truncadas

Extraídos de la página de participantes de cada aula, con el total verificado contra el contador que declara Moodle.

| Grupo | Estudiantes en el aula | Tu CSV en `Por organizar/` |
|---|---|---|
| Proyecto I 54ES4 | **50** | 40 (en el `.ods`) |
| Investigación 53339 | **20** | 20 ✔ |
| Creatividad 54408 | **50** | 20 ⚠️ |
| TG2 54448 | **50** | 20 ⚠️ |
| TG3 54450 | **13** | 13 ✔ |
| TG3 54466 | **49** | 19 ⚠️ |
| TG3 54467 | **50** | 50 ✔ |
| **Total** | **282** | — |

Las exportaciones de Creatividad, TG2 y TG3-54466 traían **20 filas** (21 líneas con encabezado): quedaron cortadas. De los 20 correos, 19 son estudiantes que sí están en el aula y el 20.º es el del propio docente. **CDigital cubre todo lo que traían tus CSV**, así que no se perdió a nadie.

Roster vigente por grupo: `<Curso>/2026/<grupo>/Listado estudiantes (CDigital).csv` y `Correos estudiantes (invitados Calendar).txt`.

> Proyecto I merece atención: el `.ods` tenía **40** y la matrícula real es **50**. Su builder de calendario leía solo el `.ods`, así que 10 estudiantes se habrían quedado sin invitación. Ya lee el roster de CDigital.

---

## 4. Apps Scripts de encuentros

Generados con `python config/slides/build_calendar_encuentros.py` (Proyecto I conserva el suyo, `build_calendar_proyecto1_54es4.py`). Google Calendar descarta los invitados al importar `.ics`/`.csv`, así que esta es la única vía que sí crea la sección Invitados.

| Curso | Archivo | Sesiones | Invitados |
|---|---|---|---|
| Proyecto I 54ES4 | `2026/54ES4/Crear encuentros con invitados.gs` | 11 | 51 |
| Creatividad 54408 | `2026/54408/Crear encuentros con invitados.gs` | 7 | 50 |
| Investigación 53339 | `2026/53339/Crear encuentros con invitados.gs` | 6 | 20 |
| TG2 54448 | `2026/54448/Crear encuentros con invitados.gs` | 11 | 50 |
| **TG3 (3 grupos)** | `2026/_combinado_todos/Crear encuentros con invitados (3 grupos).gs` | 15 | **112** |

**TG3 es una sola serie con un solo enlace de Meet** para los tres grupos, como se pidió. A la última sesión no se invita a **54450**, porque su curso cierra el 15/11 y los otros dos el 22/11.

Cada `.gs` trae `verificar()` (solo lectura, ejecútalo primero), `crearEncuentros()` y `borrarEncuentros()`.

---

## 4 bis. La fecha de «recepción» NO es institucional

Conviene tenerlo claro antes de discutir cualquier fecha: en `config/cursos/carga_academica_2026.json` la nota de cabecera dice literalmente que **«recepcion no viene en el Excel»** y que se conservó «la fecha operativa ya usada en el proyecto (típicamente ~8 días antes del cierre)».

Es decir: de cada curso solo son institucionales el **inicio del periodo** y el **cierre/registro de notas**. La recepción es una fecha **nuestra** y se puede mover sin pedirle permiso a nadie. Varias afirmaciones del material que decían «límite estructural, no corregible moviendo fechas» partían de creerla intocable.

**Decisión del Docente (10/08/2026) — Investigación 53339:** el Quiz 3 pasa de cerrar el 17/09 (S06) a cerrar el **12/09**, junto con la ACA Final. Todo el corte 3 cierra el mismo día y la **S06 (17/09) queda como socialización y cierre, sin evaluación**. Es una excepción consciente a la regla de «los cuestionarios cierran en día de clase»: la última sesión cae después de la recepción, así que la regla no era satisfacible.

---

## 4 ter. ⚠️ Corrección al pendiente 1: las actividades SÍ existen, y están vacías y abiertas

*Verificado el 15/08/2026 leyendo las 7 aulas con `config/moodle/cdigital.py` (servicio `core_courseformat_get_state` + `/mod/quiz/edit.php`), no con Playwright.*

El pendiente 1 de §5 decía que los quices y parciales «existen solo como ítem del libro de calificaciones, sin la actividad detrás». **Eso es falso.** El censo de los **38 cuestionarios** de las 7 aulas encuentra:

| Aula | Curso | Cuestionarios evaluativos | Estado real |
|---|---|---|---|
| 115463 | Creatividad 54408 | 6 | Quiz 1 con nuestras 10 preguntas; los otros 4 con **10 slots aleatorios de plantilla** |
| 111070 | Investigación 53339 | — | **0 slots**: vacíos, puntuación total 0.00 |
| 129268 | TG2 54448 | — | **0 slots** |
| 112321 · 116387 · 129270 | TG3 54450/54466/54467 | — | **0 slots** |
| 130378 | Proyecto I 54ES4 | — | **0 slots** |

Dos consecuencias, y ninguna es cosmética:

1. **Un cuestionario vacío pero visible es peor que uno que no existe.** Los de esas 6 aulas están **visibles y abiertos desde el 11/08/2026, cierran el 20/09**, con 2 intentos y 45 minutos (comprobado en `cmid 6522194` y `7448451`). El estudiante puede entrar, no ver ninguna pregunta y gastar un intento. No hay que «crearlos»: hay que **llenarlos**, y mientras no estén llenos deberían estar ocultos.
2. **La buena noticia: los 38 tienen 0 intentos.** Nadie ha entrado. Nada está bloqueado, así que todos se pueden recomponer sin hablar con nadie. Ese freno —`quiz-sustituir` aborta con intentos ≠ 0— no se ha activado ni una vez.

### Decisión que NO tomé: la ventana del Quiz 1 de Creatividad

Hay dos ventanas distintas para el mismo cuestionario y **no las igualé a propósito**:

| Fuente | Abre | Cierra | Intentos | Tiempo |
|---|---|---|---|---|
| El material entregado al estudiante | 12/08/2026 | 19/08/2026 | 1 | ~12 min |
| El aula 115463 (`cmid 6745720`), hoy | 11/08/2026 | 20/09/2026 | 2 | 30 min |

El aula es **más permisiva** que lo anunciado, así que nadie queda fuera y no hay urgencia. Pero cambiar la ventana de un cuestionario **ya visible y ya cargado con las 10 preguntas reales**, con 50 estudiantes matriculados, es modificar una evaluación en curso: no es alistamiento, es intervención. Eso lo decide el Docente. **Recomendación:** dejar cerrar el **19/08 a las 23:59, 1 intento, 12 minutos**, que es lo que dice el documento que los estudiantes ya tienen; si se prefiere la ventana ancha del aula, entonces hay que corregir la guía del cuestionario, no al revés.

---

## 5. Qué queda pendiente

*Registro actualizado el 11/08/2026; §4 ter lo corrige el 15/08/2026. Lo tachado se cerró; lo que queda solo se puede hacer en la plataforma o depende de la Universidad.*

### Ya cerrado

- ~~Alinear el material a la estructura del campus~~ — hecho en los 5 cursos: un documento por ítem real, quices y parciales con su peso, coevaluación como foro. La regla «cada ACA toma el 100% de su corte» queda anulada.
- ~~Salas de Meet de los otros 4 cursos~~ — ya no hacen falta a mano: **el `.gs` crea la suya**. El primer evento de la serie la crea con el servicio avanzado de Calendar y los demás reutilizan su `conferenceData`, así que la serie entera comparte enlace y chip nativo. El script imprime la URL en el registro.
- ~~Enlaces del aula~~ — los 7 obtenidos y resueltos por código (§1).

### Lo que solo puedes hacer tú, en la plataforma

1. ~~**Crear en el aula los quices y parciales.**~~ **Reformulado el 15/08/2026 (ver §4 ter): las actividades ya existen; están vacías, visibles y abiertas.** Lo que queda no es crearlas sino **revisar y activar** lo que el alistamiento deja puesto y oculto: los bancos de preguntas importados, los cuestionarios ya apuntados a esos bancos y el material de estudio subido como recurso. Todo llega oculto y ninguno se activa sin ti. El material ya está listo: cada cuestionario tiene su guía con el alcance exacto, generada desde las sesiones dictadas antes de su cierre, así que nunca pregunta algo no visto.
2. **Pegar la URL de Meet** que imprima el `.gs` en `carga_academica_2026.json` → `cursos.<key>.meet`, y reconstruir. Con eso el correo de bienvenida y el LEEME del estudiante dejan de mostrar el marcador de posición.
3. **Subir el contenido a las aulas**: no tienen secciones creadas más allá de Avisos. *Parcialmente en marcha:* el `subir-recurso` de `cdigital.py` ya publica material como recurso oculto en la sección del tema — probado con el `Material de estudio U2` de Creatividad (`cmid 7705987`, sección «Tema 2», oculto).
4. **Decidir la ventana del Quiz 1 de Creatividad** (§4 ter): el aula deja hasta el 20/09 con 2 intentos y 30 min; el documento del estudiante dice 19/08, 1 intento, 12 min.

### Lo que depende de la Universidad

5. **Syllabus SIAC de TG2**, ausente. Es el único de los cinco sin él; su Manual del Docente lo dice explícitamente en vez de inventar unidades.
5. **El Syllabus de Creatividad es el de otra escuela.** El archivo se llama `…PARA ESCUELA DE INGENIERIAS EI004_VIR.docx`, pero adentro dice «PARA LA ESCUELA DE CIENCIAS ADMINISTRATIVAS», `CÓDIGO SÍAC: AE003` y nivel «Tecnológico», cuando la oferta es EI004 de Ingenierías, nivel Profesional. **La tabla de unidades sí es la de Creatividad** y coincide con lo que enseña el material, así que el contenido no está en riesgo: es el mismo temario reutilizado entre escuelas. Conviene confirmarlo con Coordinación antes de citar el código en algo formal.

---

*Reproducible con los scripts de auditoría del scratchpad de la sesión (Playwright, solo lectura). Las credenciales no se guardaron en el repo.*
