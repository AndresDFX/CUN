# Ocultamiento de componentes no evaluativos en CDigital

**Fecha de ejecución:** 17 de agosto de 2026 · semestre 2026-2
**Alcance:** las 7 aulas del Docente
**Herramienta:** `config/moodle/ocultar_no_evaluativo.py`
**Resultado:** **168 componentes se quedan visibles · 101 ocultados · 0 errores**
**Reversible:** sí — `python config/moodle/cdigital.py mostrar <cmid>`

---

## 1. Por qué se hizo

Las aulas de CDigital llegan con mucho componente de plantilla institucional que el Docente
no usa y que **no da nota**: SCORM «Contenido N (Haz clic aquí)», páginas de podcast e
imágenes interactivas, placeholders «G1 / Video 1 / Recurso 1», foros vacíos sin consigna.
Todo eso estaba **visible** junto al material real del curso.

El estudiante no puede distinguir lo que cuenta de lo que sobra, y pregunta. El caso que
disparó esto: **«Foro 1 Temática»** y **«Generalidades del Proyecto de Aula»**, dos foros
visibles cuyo mensaje inicial estaba **literalmente en blanco** — ver
[DIAGNOSTICO_FORO_1_CREATIVIDAD.md](DIAGNOSTICO_FORO_1_CREATIVIDAD.md).

Decisión del Docente (17/08/2026): ocultar esos dos foros y, con ellos, todo componente no
evaluativo de los cursos, **con excepción del foro de presentación**.

---

## 2. Regla de clasificación

Está codificada en `config/moodle/ocultar_no_evaluativo.py` para que sea la misma cada
semestre y no dependa del criterio del momento.

### Se queda VISIBLE si cumple alguna de estas 7 condiciones

| # | Condición | Por qué |
|---|---|---|
| 1 | Tiene **peso > 0 %** en el libro de calificaciones | Es evaluativo. Se detecta leyendo `/grade/edit/tree/index.php`, no adivinando por el nombre. |
| 2 | Se llama `Evaluación Docente *` o `Evalúa tu Entorno` (`feedback`) | Evaluación institucional: el estudiante evalúa al Docente. Sin peso, pero obligatoria. |
| 3 | Se llama `Coevaluación *` | Foro valorado. En el libro figura como «Coevaluación calificación», con otro nombre que el del módulo. |
| 4 | Es una de las **4 carpetas del Docente** | Presentaciones de clase · Guías de las ACAs y de los cuestionarios · Lecturas obligatorias · Recursos del curso. Es el material del alistamiento. |
| 5 | Es un **enlace operativo** | Avisos · Material clases · Clases · Clases grabadas · Sesion en vivo · Horario. |
| 6 | Es el **foro de presentación** (`Te queremos Conocer`) | Excepción explícita del Docente: es el espacio social del aula. |
| 7 | Es **soporte institucional que el ACA necesita** | Normas APA · Ingreso a Biblioteca virtual · Acuerdo Pedagógico CUN. Ver §5. |
| — | Es un `resource` (documento subido por el Docente) | Lo publicó el Docente, no la plantilla. |

### Se OCULTA todo lo demás

Es decir: cualquier componente **sin peso en la nota** que no sea material del Docente ni
esté en la lista de excepciones.

---

## 3. Qué se ocultó, aula por aula

### Creatividad y Pensamiento Innovador · curso 115463 — 15 ocultados

| cmid | Tipo | Componente |
|---|---|---|
| `7706181` | forum | Prueba de recordatorios (era una prueba del Docente, se puede borrar) |
| `6745709` | page | Modelo Pedagógico |
| `6745713` | scorm | Contenido 1 (Haz clic aquí) |
| `6745714` | page | Podcast - Innovación |
| `6745715` | page | Podcast - Líneas estructurales |
| **`6745716`** | **forum** | **Foro 1 Temática** ← el del diagnóstico |
| **`6745717`** | **forum** | **Generalidades del Proyecto de Aula** ← el del diagnóstico |
| `6745718` | scorm | Contenido 2 (Haz clic aquí) |
| `6745721` | scorm | Contenido 3 (Haz clic aquí) |
| `6745723` | scorm | Contenido 4 (Haz clic aquí) |
| `6745726` | scorm | Contenido 5 (Haz clic aquí) |
| `6745728` | scorm | Contenido 6 (Haz clic aquí) |
| `6745730` | scorm | Contenido 7 (Haz clic aquí) |
| `6745732` | scorm | Contenido 8 (Haz clic aquí) |
| `6745737` | label | Área de texto y medios |

### Investigación en Ciencia y Tecnología · curso 111070 — 19 ocultados

| cmid | Tipo | Componente |
|---|---|---|
| `6522183` | page | Modelo Pedagógico |
| `6522187` | page | Contenido 1 (Da clic aquí) |
| **`6522188`** | **forum** | **Foro 1 Temática** ← también existía aquí, también vacío |
| **`6522189`** | **forum** | **Generalidades del Proyecto de Aula** ← ídem |
| `6522190` | page | Actividad h5p |
| `6522191` | page | Contenido 2 (Da clic aquí) |
| `6522192` | page | Imagen interactiva |
| `6522195` | page | Contenido 3 (Da clic aquí) |
| `6522196` | page | Podcast: Toda la verdad sobre la desinformación |
| `6522197` | page | Podcast |
| `6522199` | page | Contenido 4 (Da clic aquí) |
| `6522200` | page | Imagen interactiva 1 |
| `6522201` | page | Imagen interactiva 2 |
| `6522204` | page | Contenido 5 (Da clic aquí) |
| `6522205` | page | Imagen interactiva |
| `6522207` | page | Contenido 6 (Da clic aquí) |
| `6522209` | page | Contenido 7 (Da clic aquí) |
| `6522211` | page | Contenido 8 (Da clic aquí) |
| `6522216` | label | Área de texto y medios |

### Trabajo de Grado 2 · curso 129268 — 26 ocultados

| cmid | Tipo | Componente |
|---|---|---|
| `7448439` | page | Modelo pedagógico |
| `7448444` `7448447` `7448452` `7448456` `7448461` `7448465` `7448469` `7448473` | url | **G1 … G8** (placeholders de guía) |
| `7448445` `7448448` `7448453` `7448457` `7448462` `7448466` `7448470` `7448474` | url | **Video 1 … Video 8** (placeholders) |
| `7448446` `7448449` `7448454` `7448458` `7448463` `7448467` `7448471` `7448475` | url | **Recurso 1 … Recurso 8** (placeholders) |
| `7448480` | label | Área de texto y medios |

> TG2 era el aula más ruidosa: 24 de sus 26 ocultados eran placeholders `G/Video/Recurso`
> sin contenido real, uno por cada tema.

### Trabajo de Grado 3 · 54450 (112321) · 54466 (116387) · 54467 (129270) — 2 ocultados cada una

| Aula | cmid | Tipo | Componente |
|---|---|---|---|
| 112321 | `6608168` | page | Modelo pedagógico |
| 112321 | `6608184` | label | Área de texto y medios |
| 116387 | `6785562` | page | Modelo pedagógico |
| 116387 | `6785578` | label | Área de texto y medios |
| 129270 | `7448530` | page | Modelo pedagógico |
| 129270 | `7448546` | label | Área de texto y medios |

> Las tres aulas de TG3 ya venían limpias: sin SCORM de contenido, sin foros de plantilla,
> sin placeholders. Solo sobraba la página institucional y la etiqueta vacía.

### Proyecto I · curso 130378 — 35 ocultados

| cmid | Tipo | Componente |
|---|---|---|
| `7563679` `7563680` `7563725` | label | Área de texto y medios (×3) |
| `7563681` | page | Modelo pedagógico |
| `7563685` | url | 1. Aprende en 3,2,1 🎬 |
| `7563686` `7563692` `7563700` `7563708` `7563716` | url | **N. Conecta tu Mente: Descarga y Súbelo al NotebookLM 🚀** (temas 1–5) |
| `7563687` `7563693` `7563701` `7563709` `7563717` | url | **N. Hackea tu Cuaderno Inteligente: Descarga + Sube 🤖** (temas 1–5) |
| `7563688` `7563694` `7563702` `7563710` `7563718` | scorm | **N. Desbloquea el Saber: Tarjetas Clave 🧠** (temas 1–5) |
| `7563689` `7563695` `7563703` `7563711` `7563719` | url | **N. podcast 🗣️** (temas 1–5) |
| `7563690` `7563696` `7563704` `7563712` `7563720` | url | **N. FUNCUN 🧐** (temas 1–5) |
| `7563691` `7563697` `7563705` `7563713` `7563721` | url | **N. Infografía 🗿** (temas 1–5) |

> Proyecto I traía 6 recursos de plantilla por cada uno de los 5 temas. Ninguno con nota.

---

## 4. Qué quedó visible (168 componentes)

Idéntico en las 7 aulas, salvo el detalle propio de cada una:

| Bloque | Contenido |
|---|---|
| **Evaluativo** | Quiz 1 · Parcial 1 · Quiz 2 · Parcial 2 · Quiz 3 · ACA Final · Autoevaluación · Coevaluación. En Proyecto I: Quiz · ACA 1 · ACA FINAL · Autoevaluación · Coevaluación. |
| **Evaluación docente** | Evaluación Docente 1 · 2 · 3 · Evalúa tu Entorno |
| **Material del Docente** | Presentaciones de clase · Guías de las ACAs y de los cuestionarios · Lecturas obligatorias · Recursos del curso (+ el `resource` «Material de estudio U2» en Creatividad) |
| **Operativo** | Avisos · Material clases / Clases · Clases grabadas · Sesion en vivo · Horario |
| **Social** | **Te queremos Conocer** — excepción explícita del Docente |
| **Soporte institucional** | Normas APA · Ingreso a Biblioteca virtual · Acuerdo Pedagógico CUN (TG2) |

Verificación post-ejecución, releyendo las 7 aulas del servidor:

| Aula | Evaluativos visibles | Carpetas | Foro presentación | Avisos | Ocultos | Ocultados por error |
|---|---|---|---|---|---|---|
| 115463 Creatividad | 12 | 4 | 1 | 1 | 15 | **0** |
| 111070 Investigación | 12 | 4 | 1 | 1 | 19 | **0** |
| 129268 TG2 | 12 | 4 | 1 | 1 | 26 | **0** |
| 112321 TG3-54450 | 12 | 4 | 1 | 1 | 2 | **0** |
| 116387 TG3-54466 | 12 | 4 | 1 | 1 | 2 | **0** |
| 129270 TG3-54467 | 12 | 4 | 1 | 1 | 2 | **0** |
| 130378 Proyecto I | 9 | 4 | 1 | 1 | 35 | **0** |

---

## 5. Decisión que se apartó de la instrucción literal, y por qué

La instrucción fue «oculta todo el componente que no sea evaluativo, a excepción del foro de
presentación». Tres componentes **no** evaluativos se dejaron visibles a propósito:

| Componente | Por qué se dejó |
|---|---|
| **Normas APA** | La consigna del ACA Final exige «Referencias de todo lo que citaste» y el checklist evalúa la presentación cuidada. Ocultar la referencia APA estorba una entrega del 32,8 %. |
| **Ingreso a Biblioteca virtual** | La guía del ACA Final la lista como herramienta obligatoria («Google Scholar, SciELO, Redalyc, biblioteca virtual CUN»). Es la vía de acceso, no hay otra en el aula. |
| **Acuerdo Pedagógico CUN** (TG2, `7448443`) | Es ítem del checklist de INICIO del ciclo docente de pregrado. Obligación de inicio de semestre, no adorno de plantilla. |

**Si se quieren fuera también**, es un comando:

```bash
python config/moodle/cdigital.py ocultar 6745710   # Normas APA · Creatividad
python config/moodle/cdigital.py ocultar 6745711   # Biblioteca virtual · Creatividad
python config/moodle/cdigital.py ocultar 6522184   # Normas APA · Investigación
python config/moodle/cdigital.py ocultar 6522185   # Biblioteca virtual · Investigación
python config/moodle/cdigital.py ocultar 7448442   # Normas APA · TG2
python config/moodle/cdigital.py ocultar 7448441   # Biblioteca virtual · TG2
python config/moodle/cdigital.py ocultar 7448443   # Acuerdo Pedagógico CUN · TG2
python config/moodle/cdigital.py ocultar 6608171   # Normas APA · TG3-54450
python config/moodle/cdigital.py ocultar 6608170   # Biblioteca virtual · TG3-54450
python config/moodle/cdigital.py ocultar 6785565   # Normas APA · TG3-54466
python config/moodle/cdigital.py ocultar 6785564   # Biblioteca virtual · TG3-54466
python config/moodle/cdigital.py ocultar 7448533   # Normas APA · TG3-54467
python config/moodle/cdigital.py ocultar 7448532   # Biblioteca virtual · TG3-54467
python config/moodle/cdigital.py ocultar 7563684   # Normas APA · Proyecto I
python config/moodle/cdigital.py ocultar 7563683   # Biblioteca virtual · Proyecto I
```

O quitando la regla 7 (`SOPORTE_INSTITUCIONAL`) de `ocultar_no_evaluativo.py` y volviendo a
correrlo.

---

## 6. Cómo se ejecuta (cada semestre)

```bash
# 1. Plan de las 7 aulas — NO toca nada
python config/moodle/ocultar_no_evaluativo.py

# 2. Plan de una sola aula
python config/moodle/ocultar_no_evaluativo.py --curso 115463

# 3. Ejecutar
python config/moodle/ocultar_no_evaluativo.py --confirmar
```

Sin `--confirmar` solo imprime el plan. Con `--confirmar`, oculta y **verifica releyendo el
aula del servidor**, no confiando en la respuesta del GET; si algo quedó visible lo reporta
como `OJO sigue visible`.

**Orden dentro del alistamiento:** después de activar el material y antes de ajustar fechas.
Es la Fase 2 bis de [ALISTAMIENTO_DE_AULAS_CDIGITAL.md](ALISTAMIENTO_DE_AULAS_CDIGITAL.md).

---

## 7. Deshacer

Todo es reversible; ocultar no borra nada ni pierde datos.

```bash
# Un componente
python config/moodle/cdigital.py mostrar 6745716

# Los dos foros del diagnóstico, en las dos aulas donde estaban
python config/moodle/cdigital.py mostrar 6745716   # Foro 1 Temática · Creatividad
python config/moodle/cdigital.py mostrar 6745717   # Generalidades · Creatividad
python config/moodle/cdigital.py mostrar 6522188   # Foro 1 Temática · Investigación
python config/moodle/cdigital.py mostrar 6522189   # Generalidades · Investigación
```

Los cmid de todo lo ocultado están en las tablas de §3.

---

## 8. Qué decirle a los estudiantes

Ya no verán los dos foros vacíos, así que la pregunta no debería repetirse. Si alguien
pregunta por qué desapareció algo que sí vio antes:

> Se depuró el aula: se dejaron visibles **solo los componentes que cuentan para la nota**,
> el material de clase y los enlaces del curso. Lo que se ocultó era contenido de plantilla
> sin nota, que solo generaba confusión — entre ello dos foros que estaban en blanco.
>
> El **proyecto de aula sigue siendo el mismo** y se entrega en la tarea evaluada del aula
> (en Creatividad: **ACA Final — Propuesta de Innovación**, 32,8 %, cierre **19/09/2026**).
> No se eliminó ninguna entrega ni cambió ningún peso ni ninguna fecha.

**Nada evaluativo se tocó.** Los pesos y las fechas quedaron exactamente como los dejó el
ajuste de [FECHAS_AJUSTADAS_CDIGITAL.md](FECHAS_AJUSTADAS_CDIGITAL.md).

---

## 9. Cómo se verificó

| Qué | Cómo |
|---|---|
| Inventario y visibilidad de cada componente | `CDigital.estado_curso(<curso>)` (servicio de estado, no HTML) |
| Peso real en la nota de cada ítem | `GET /grade/edit/tree/index.php?id=<curso>` → `weight_<id>` |
| Que la ocultación se aplicó | Relectura de las 7 aulas tras el `--confirmar`: `siguen visibles: 0` en todas |
| Que nada evaluativo se ocultó | Control cruzado por nombre (quiz/parcial/aca/auto/coevaluación/evaluación docente) + carpetas + foro de presentación + Avisos → **0 errores en las 7 aulas** |

---

**Ejecutado:** 17 de agosto de 2026
**Ocultados:** 101 · **Visibles:** 168 · **Errores:** 0
**Próxima ejecución:** inicio de semestre 2027-1, dentro del alistamiento de aulas
