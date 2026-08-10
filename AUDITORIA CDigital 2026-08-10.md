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

## 5. Qué queda pendiente

1. **Alinear el material a la estructura del campus** (§2). Es un cambio de fondo: hay que introducir quices y parciales, y renombrar/reagrupar las ACAs. Afecta enunciados, decks, guiones y manuales de los 5 cursos.
2. **Crear en el aula los quices y parciales** (hoy solo existen como ítems del libro de calificaciones, sin la actividad).
3. **Salas de Meet** de TG2, TG3, Creatividad e Investigación (solo Proyecto I tiene). Van en `carga_academica_2026.json` → `cursos.<key>.meet`.
4. **Subir el contenido a las aulas**: no tienen secciones creadas más allá de Avisos.
5. **Syllabus SIAC de TG2**, aún ausente.

---

*Reproducible con los scripts de auditoría del scratchpad de la sesión (Playwright, solo lectura). Las credenciales no se guardaron en el repo.*
