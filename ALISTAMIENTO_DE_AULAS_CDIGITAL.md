# ALISTAMIENTO DE AULAS EN CDIGITAL
## Procedimiento estándar para cada semestre

---

## 📋 ¿QUÉ ES EL ALISTAMIENTO DE AULAS?

El **alistamiento de aulas** es el proceso completo de preparar las aulas de CDigital (Moodle CUN) para que los estudiantes tengan acceso a todo el material del curso con las fechas correctas.

**Resultado esperado:** Aulas completamente funcionales con:
- ✅ Todo el material visible para estudiantes
- ✅ Cuestionarios con preguntas correctas (no slots aleatorios de plantilla)
- ✅ Fechas alineadas con el calendario del semestre (no fechas de 2028 o 2030)
- ✅ Carpetas con contenido (presentaciones, guías, lecturas, recursos)
- ✅ Evaluación docente (autoevaluación y coevaluación) configurada
- ✅ Encuestas institucionales (`feedback`) **abiertas de verdad** — no con la apertura de plantilla
  en 2028 o 2030, que hace que nunca abran

---

## ⏰ CUÁNDO SE EJECUTA

**Momento ideal:** 1-2 días antes del inicio de clases del semestre.

**Frecuencia:** Una vez por semestre, al inicio del periodo académico.

**Duración estimada:** 2-3 horas para 7 aulas.

---

## 🎯 AULAS QUE SE ALISTAN

### Pregrado (6 aulas):
1. **Creatividad y Pensamiento Innovador** (curso 115463)
2. **Investigación en Ciencia y Tecnología** (curso 111070)
3. **Trabajo de Grado 2** (curso 129268)
4. **Trabajo de Grado 3 - Grupo 54450** (curso 112321)
5. **Trabajo de Grado 3 - Grupo 54466** (curso 116387)
6. **Trabajo de Grado 3 - Grupo 54467** (curso 129270)

### Especialización (1 aula):
7. **Proyecto I - Inteligencia Artificial** (curso 130378)

**Nota:** Los IDs de curso pueden cambiar cada semestre. Verificar en el correo de asignación de aulas o en CDigital.

---

## 📦 PRE-REQUISITOS

### 1. Repositorio actualizado
Verificar que el repositorio en `g:\My Drive\Trabajos\Empleo\CUN\Cursos` tenga:
- ✅ Material de clases actualizado (presentaciones, guías, lecturas)
- ✅ Bancos de preguntas actualizados (XML en `Docente/Cuestionarios/`)
- ✅ Fechas del semestre actualizadas en `config/cursos/fechas_entrega_aca.py`

### 2. Credenciales configuradas
- ✅ Archivo `%LOCALAPPDATA%\cdigital-cun\credenciales.json` con usuario y contraseña

### 3. Python y dependencias instaladas
```bash
python --version  # Debe ser Python 3.8+
pip install requests
```

### 4. Acceso a las aulas en CDigital
- ✅ Confirmación de que fuiste asignado como docente de las aulas
- ✅ Puedes acceder a https://cdigital.cun.edu.co

---

## 🔧 HERRAMIENTAS

Todas las operaciones se ejecutan desde la línea de comandos con:
```bash
python config/moodle/cdigital.py <subcomando> [opciones]
```

### Subcomandos principales:
- `estado` — Verificar sesión
- `curso <id>` — Listar actividades de un aula
- `mostrar <cmid>` — Hacer visible una actividad
- `fechas <curso> --incluir-visibles --confirmar` — Alinear fechas de los ítems evaluativos
- `encuestas <curso>` — Censar las encuestas institucionales (`feedback`); con
  `--sin-apertura --cmid <cmid> --confirmar` destraba la que nunca abre dejándola siempre
  disponible, y con `--abre AAAA-MM-DD` le pone una apertura concreta
- `quiz <cmid>` — Ver detalles de un cuestionario

---

## ✅ PROCEDIMIENTO COMPLETO

### FASE 1: PREPARACIÓN (15 minutos)

#### 1.1. Actualizar fechas del semestre
**Archivo:** `config/cursos/fechas_entrega_aca.py`

**Qué actualizar:**
- Las fechas de `VENTANAS` y `VENTANAS_POR_GRUPO`
- Ajustar por festivos (usar `festivos_colombia.py`)
- Verificar que todos los ítems tengan fechas definidas

**Ejemplo:**
```python
VENTANAS = {
    "creatividad": {
        "quiz_1": ("2026-08-12", "2026-08-19"),
        "parcial_1": ("2026-08-20", "2026-08-26"),
        # ... resto de ítems
    }
}
```

#### 1.2. Verificar que el material esté actualizado
Revisar que existan:
- Presentaciones en `Clases/Sesion NN - */Presentacion.pptx`
- Guías de ACAs en `Clases/ACAs/`
- Lecturas obligatorias en `Clases/Lecturas/`
- Bancos de preguntas XML en `Docente/Cuestionarios/`

#### 1.3. Obtener los IDs de las aulas
**Si no los tienes:**
1. Acceder a https://cdigital.cun.edu.co
2. Entrar a cada aula
3. El ID está en la URL: `?id=115463`

**O desde Python:**
```bash
python config/moodle/cdigital.py estado
```

---

### FASE 2: ACTIVACIÓN DEL MATERIAL (30 minutos)

#### 2.1. Listar elementos ocultos de cada aula

**Comando:**
```bash
python config/moodle/cdigital.py curso 115463
python config/moodle/cdigital.py curso 111070
python config/moodle/cdigital.py curso 129268
python config/moodle/cdigital.py curso 112321
python config/moodle/cdigital.py curso 116387
python config/moodle/cdigital.py curso 129270
python config/moodle/cdigital.py curso 130378
```

**Buscar en la salida:**
- Líneas con `[oculto]` — elementos no visibles para estudiantes
- Identificar CMIDs de carpetas y cuestionarios ocultos

#### 2.2. Activar carpetas (4 por aula en pregrado)

**Carpetas estándar:**
1. Presentaciones de clase
2. Guías de las ACAs y de los cuestionarios
3. Lecturas obligatorias
4. Recursos del curso

**Comando (ejemplo para Creatividad):**
```bash
python config/moodle/cdigital.py mostrar 7705992  # Presentaciones
python config/moodle/cdigital.py mostrar 7705993  # Guías
python config/moodle/cdigital.py mostrar 7705994  # Lecturas
python config/moodle/cdigital.py mostrar 7705995  # Recursos
```

**Repetir para las 7 aulas.**

**Total esperado:** ~28 carpetas activadas (4 × 7 aulas)

#### 2.3. Activar cuestionarios

**Cuestionarios estándar en pregrado:**
1. Quiz 1
2. Parcial 1
3. Quiz 2
4. Parcial 2
5. Quiz 3

**Cuestionarios estándar en Proyecto I:**
1. Quiz
2. Autoevaluación (puede estar visible)

**Comando (ejemplo para Creatividad):**
```bash
python config/moodle/cdigital.py mostrar 6745720  # Quiz 1
python config/moodle/cdigital.py mostrar 6745722  # Parcial 1
python config/moodle/cdigital.py mostrar 6745725  # Quiz 2
python config/moodle/cdigital.py mostrar 6745727  # Parcial 2
python config/moodle/cdigital.py mostrar 6745736  # Quiz 3
```

**Repetir para las 7 aulas.**

**Total esperado:** ~35 cuestionarios activados

**NOTA IMPORTANTE:** Autoevaluación y Coevaluación suelen estar visibles desde la plantilla. Si están ocultos, activarlos también.

---

### FASE 2 BIS: DEPURAR LO NO EVALUATIVO (15 minutos)

#### 2.4. Ocultar los componentes de plantilla que no dan nota

**Por qué:** las aulas llegan con mucho componente institucional visible que el Docente no
usa y que no da nota — SCORM «Contenido N (Haz clic aquí)», páginas de podcast e imágenes
interactivas, placeholders «G1 / Video 1 / Recurso 1», **foros vacíos sin consigna**. El
estudiante no distingue lo que cuenta de lo que sobra, y pregunta.

> **Caso real 2026-2:** los foros «Foro 1 Temática» y «Generalidades del Proyecto de Aula»
> estaban visibles en Creatividad y en Investigación con el **mensaje inicial en blanco**.
> Los estudiantes escribieron al Docente para preguntar qué debían hacer ahí. Diagnóstico:
> `DIAGNOSTICO_FORO_1_CREATIVIDAD.md`.

**Comando:**

```bash
# 1. Plan de las 7 aulas — NO toca nada
python config/moodle/ocultar_no_evaluativo.py

# 2. Revisar el plan y ejecutar
python config/moodle/ocultar_no_evaluativo.py --confirmar
```

**Qué se queda visible** (regla codificada en el script, no criterio del momento):

1. Todo lo que tiene **peso > 0 %** en el libro de calificaciones
2. Evaluación Docente 1/2/3 y Evalúa tu Entorno (evaluación institucional)
3. Coevaluación (foro valorado)
4. Las 4 carpetas del Docente
5. Enlaces operativos: Avisos · Material clases · Clases grabadas · Sesion en vivo · Horario
6. Foro de presentación «Te queremos Conocer»
7. Soporte institucional que el ACA necesita: Normas APA · Biblioteca virtual · Acuerdo Pedagógico

**Todo lo demás se oculta.**

**Verificar en la salida:**
- ✅ `verificado releyendo el servidor · siguen visibles: 0`
- ✅ Ningún `OJO sigue visible`
- ✅ Que la lista `SE QUEDAN VISIBLES` incluya los 8 ítems evaluativos y las 4 carpetas

**Referencia 2026-2:** 168 visibles · 101 ocultados · 0 errores. Desglose por aula en
`OCULTAMIENTO_NO_EVALUATIVO_CDIGITAL.md`.

**Reversible:** `python config/moodle/cdigital.py mostrar <cmid>`

---

### FASE 3: VERIFICACIÓN DE CUESTIONARIOS (30 minutos)

#### 3.1. Verificar que tengan preguntas concretas (no slots aleatorios)

**Objetivo:** Confirmar que los cuestionarios tienen las preguntas correctas del banco, no los slots aleatorios vacíos de la plantilla.

**Comando (muestra representativa):**
```bash
python config/moodle/cdigital.py quiz 6745720  # Creatividad Quiz 1
python config/moodle/cdigital.py quiz 6522194  # Investigación Quiz 1
python config/moodle/cdigital.py quiz 7448451  # TG2 Quiz 1
python config/moodle/cdigital.py quiz 6608173  # TG3-54450 Quiz 1
python config/moodle/cdigital.py quiz 7563699  # Proyecto I Quiz
```

**Verificar en la salida:**
- ✅ `10 slots` — todos los cuestionarios deben tener 10 preguntas
- ✅ Nombres de preguntas concretas (ej: `CRE-Q06`, `TG2-Q1-01`, `PRO-Q01`)
- ❌ **NO** debe aparecer `aleatorio` o `Por defecto en Quiz`

**Si aparecen slots aleatorios:**
```bash
# Identificar categorías con preguntas
python config/moodle/cdigital.py preguntas --curso 115463

# Sustituir slots con preguntas de la categoría correcta
python config/moodle/cdigital.py quiz-sustituir 6745720 --categoria <id_categoria> --confirmar
```

#### 3.2. Verificar calidad de preguntas (opcional pero recomendado)

**Objetivo:** Confirmar que las preguntas sean específicas del contenido del curso, no genéricas.

**Método:** Leer una muestra de los bancos XML:

```bash
# Ver preguntas de Quiz 1 de Creatividad
cat "Pregrado/Creatividad y pensamiento innovador/Docente/Cuestionarios/Quiz 1 - banco de preguntas (Moodle XML).xml"
```

**Verificar:**
- ✅ Las preguntas referencian lecturas obligatorias específicas
- ✅ Las retroalimentaciones incluyen citas literales de las fuentes
- ✅ No son preguntas genéricas ("¿Qué es creatividad?")

**Documentar hallazgos en:** `VALIDACION_CALIDAD_PREGUNTAS_CUESTIONARIOS.md`

---

### FASE 4: AJUSTE DE FECHAS (30 minutos)

#### 4.1. Alinear fechas con el repositorio

**Objetivo:** Corregir las fechas de todos los elementos evaluativos (cuestionarios, tareas, foros) para que coincidan con el calendario del semestre definido en `fechas_entrega_aca.py`.

**IMPORTANTE:** Usar `--incluir-visibles` para ajustar también los ítems ya visibles.

**Comando para cada aula:**
```bash
python config/moodle/cdigital.py fechas 115463 --incluir-visibles --confirmar
python config/moodle/cdigital.py fechas 111070 --incluir-visibles --confirmar
python config/moodle/cdigital.py fechas 129268 --incluir-visibles --confirmar
python config/moodle/cdigital.py fechas 112321 --incluir-visibles --confirmar
python config/moodle/cdigital.py fechas 116387 --incluir-visibles --confirmar
python config/moodle/cdigital.py fechas 129270 --incluir-visibles --confirmar
python config/moodle/cdigital.py fechas 130378 --incluir-visibles --confirmar
```

**Qué ajusta este comando:**
- Cuestionarios: `timeopen`, `timeclose`
- Tareas: `allowsubmissionsfromdate`, `duedate`, `cutoffdate`, `gradingduedate`
- Foros: `duedate`, `cutoffdate`

**Verificar en la salida:**
- ✅ Cada ítem debe mostrar `2026-XX-XX -> 2026-XX-XX`
- ✅ `OK · verificado releyendo el servidor · sigue visible`
- ✅ `ítems: N · con problema: 0 · omitidos por visibles: 0`

**Total esperado:** ~53 elementos ajustados (40 cuestionarios + 9 tareas + 4 foros)

**⛔ LO QUE ESTE COMANDO NO AJUSTA:** las **encuestas institucionales** (`feedback`) —«Evaluación
Docente 1/2/3» y «Evalúa tu Entorno»—. No están en `fechas_entrega_aca.py`, así que `fechas` no las
mira. **Van en el paso 4.2, que es obligatorio.**

#### 4.2. Destrabar las encuestas institucionales (`feedback`)

**Objetivo:** corregir las encuestas que llegan de la plantilla con la apertura en **2028 o 2030** y
por tanto **nunca abren**. Son 4 por aula (28 en 7 aulas) y **están visibles desde el primer día**.

> **Caso real 2026-2:** «Evaluación Docente 1» de Investigación decía *«Abre: viernes, 18 de febrero
> de 2028, 11:04 · Cierra: viernes, 18 de febrero de 2028, 11:04»* — apertura y cierre en el mismo
> instante, en el futuro. 13 de las 28 estaban así. Ver Problema 7. Desglose de las 13 en
> `FECHAS_AJUSTADAS_CDIGITAL.md`.

**Paso 1 — censar las 7 aulas (lectura pura, no toca nada):**

```bash
for a in 115463 111070 129268 112321 116387 129270 130378; do
  PYTHONIOENCODING=utf-8 python config/moodle/cdigital.py encuestas $a
done
```

**Cómo se lee el censo:**

| Lo que dice | Qué significa | Qué hacer |
|-------------|---------------|-----------|
| `sin apertura programada · FUNCIONA, no la toco` | Siempre disponible. **Es el estado bueno.** | 🚫 **Nada.** Ver el aviso de abajo |
| `YA ABRIÓ, no la toco` | Ya está abierta | 🚫 Nada |
| `NUNCA ABRE` con fecha de **2028 / 2030** | 🔴 **Rota.** Es la que hay que corregir | ✅ Paso 2 |
| `NUNCA ABRE` con fecha de **2026 aún por llegar** | Apertura futura puesta a propósito | 🚫 Nada. **Falso positivo** (Problema 9) |

**Paso 2 — corregir SOLO las rotas, una por una y con `--cmid`:**

```bash
# Plan en seco (sin --confirmar solo simula)
PYTHONIOENCODING=utf-8 python config/moodle/cdigital.py encuestas 111070 --sin-apertura --cmid 6522193

# Escribir
PYTHONIOENCODING=utf-8 python config/moodle/cdigital.py encuestas 111070 --sin-apertura --cmid 6522193 --confirmar
```

**Qué ponerles:**

| Encuesta | Qué se le pone | Comando |
|----------|----------------|---------|
| Evaluación Docente 1 / 2 / 3 | **Nada: sin apertura.** Siempre disponible | `--sin-apertura` |
| Evalúa tu Entorno | El **inicio del curso** (`carga_academica.curso()`) — en 2026-2 fue 10/08/2026 | `--abre 2026-08-10` |

`--abre` es `AAAA-MM-DD` y fija la apertura a las **00:00** de ese día. `--sin-apertura` desmarca la
casilla `timeopen[enabled]`, que es como quedan las 21 encuestas que funcionan bien.

> **⚠️ POR QUÉ LAS «EVALUACIÓN DOCENTE» VAN SIN VENTANA. No es pereza, son dos razones.**
>
> 1. **El formulario de una encuesta no expone `timeclose`.** Solo hay `timeopen`. Una fecha de
>    apertura sin cierre editable no acota nada: solo puede **retrasar** el acceso, nunca ordenarlo.
> 2. **La fecha de la encuesta se contagia al ítem evaluativo que la usa como candado.** Los ítems
>    están restringidos por la **finalización** de su encuesta, así que una ED que abra tarde le
>    cierra con llave los primeros días de su ventana. En 2026-2 el ACA Final de Investigación quedó
>    con **2 días útiles de 31** en un ítem del **32,8 %** con `cutoffdate = duedate` (sin prórroga),
>    y el de Creatividad con 10 de 39. Ver **Problema 11**.
>
> Es decir: **en estas aulas la fecha de una encuesta sin nota puede ser la fecha real de una entrega
> del 32,8 %.** Antes de ponerle ventana a cualquier encuesta, comprobar qué ítem la usa de candado
> (`availabilityconditionsjson` con `"type":"completion"` apuntando a su cmid).

> **🚨 LAS DOS REGLAS QUE NO SE NEGOCIAN**
>
> 1. **NO tocar la encuesta que aparece «sin apertura programada».** Está siempre disponible y **por
>    eso funciona**; suele tener **respuestas reales de estudiantes dentro** (en 2026-2: 15 encuestas
>    con **206 respuestas**). Ponerle una ventana puede **cerrar una encuesta institucional que está
>    recogiendo datos en este momento**. El comando ya la salta solo, pero no hay que forzarlo.
> 2. **Usar SIEMPRE `--cmid`, nunca el aula completa.** Las cuatro encuestas del aula **no llevan lo
>    mismo**: las tres «Evaluación Docente» van sin ventana y «Evalúa tu Entorno» con la fecha de
>    inicio. Un comando sobre el aula entera aplicaría lo mismo a las cuatro. Ver Problema 9.

**Verificar en la salida:**
- ✅ `OK · verificado releyendo el servidor · sigue visible`
- ✅ `corregidas: N · intactas por seguridad: M · con problema: 0`
- ✅ Ningún `!!! el «Cierra:» de la vista pasó de X a Y`
- ⚠️ Si la fecha aplicada ya pasó, la línea `vista del estudiante: abre None` es un **falso susto**:
  Moodle cambia la etiqueta a «Abrió:» y el lector no la reconoce. **No relanzar el comando.**
  Ver Problema 10.

**Total esperado 2026-2:** 28 encuestas censadas · 13 corregidas (las de 2028/2030) · 15 intactas por
seguridad (las que ya funcionaban, con 206 respuestas dentro). De las 13 corregidas, **6 se
rectificaron después a «sin apertura»** al descubrirse el Problema 11. **Estado final: 21 sin ventana
(siempre disponibles) + 7 «Evalúa tu Entorno» abiertas el 10/08/2026 · 0 en 2028/2030 · 0
degeneradas.** El detalle encuesta por encuesta está en `FECHAS_AJUSTADAS_CDIGITAL.md`.

---

### FASE 5: VERIFICACIÓN FINAL (30 minutos)

#### 5.1. Verificar estado completo de cada aula

**Comando:**
```bash
python config/moodle/cdigital.py curso 115463
python config/moodle/cdigital.py curso 111070
python config/moodle/cdigital.py curso 129268
python config/moodle/cdigital.py curso 112321
python config/moodle/cdigital.py curso 116387
python config/moodle/cdigital.py curso 129270
python config/moodle/cdigital.py curso 130378
```

**Verificar:**
- ✅ Todas las carpetas están `[visible]`
- ✅ Todos los cuestionarios están `[visible]`
- ✅ Todas las tareas (ACAs) están `[visible]`
- ✅ Autoevaluación y Coevaluación están `[visible]`

#### 5.2. Verificar carpetas vía web (5 minutos)

**Acceder a una carpeta de "Presentaciones" de cada aula:**
- Creatividad: https://cdigital.cun.edu.co/mod/folder/view.php?id=7705992
- Investigación: https://cdigital.cun.edu.co/mod/folder/view.php?id=7705988
- TG2: https://cdigital.cun.edu.co/mod/folder/view.php?id=7705996
- Proyecto I: https://cdigital.cun.edu.co/mod/folder/view.php?id=7706012

**Verificar:**
- ✅ La carpeta contiene archivos .pptx
- ✅ Los nombres de archivos corresponden a las sesiones del curso

**Si las carpetas están vacías:**
```bash
# Subir contenido con subir-carpeta
python config/moodle/cdigital.py subir-carpeta "Pregrado/Creatividad*/Clases/Sesion*/Presentacion.pptx" --curso 115463 --seccion 0 --nombre "Presentaciones de clase" --confirmar
```

#### 5.3. Acceder a cada aula como docente

**Revisar manualmente:**
1. ✅ Material visible en la página principal
2. ✅ Fechas correctas en cuestionarios y tareas
3. ✅ Avisos actualizados (si corresponde)

---

### FASE 6: DOCUMENTACIÓN (15 minutos)

#### 6.1. Generar documentos de auditoría

**Crear estos archivos:**

1. **`VERIFICACION_MATERIAL_VISIBLE_CDIGITAL.md`**
   - Análisis detallado de elementos activados
   - Estado de cuestionarios (slots, preguntas)
   - Pendientes identificados

2. **`CONFIRMACION_MATERIAL_CORRECTO_CDIGITAL.md`**
   - Resumen ejecutivo
   - Checklist de verificación
   - Estadísticas finales

3. **`VALIDACION_CALIDAD_PREGUNTAS_CUESTIONARIOS.md`**
   - Análisis de 30+ preguntas
   - Verificación de que no sean genéricas
   - Evidencia de que referencian material específico

4. **`FECHAS_AJUSTADAS_CDIGITAL.md`**
   - Desglose por aula
   - Fechas ajustadas por elemento
   - Verificación de fechas correctas

#### 6.2. Commit al repositorio

```bash
git add .
git commit -m "$(cat <<'EOF'
Alistamiento de aulas CDigital para semestre 2026-2

- Activadas 28 carpetas y 35 cuestionarios en 7 aulas
- Verificadas preguntas concretas en todos los cuestionarios
- Validada calidad de 30+ preguntas (específicas, no genéricas)
- Ajustadas fechas de 53 elementos evaluativos
- Destrabadas las encuestas institucionales que abrían en 2028/2030
- Generados 4 documentos de auditoría

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## 📊 CHECKLIST DE ALISTAMIENTO

### Pre-alistamiento
- [ ] Fechas del semestre actualizadas en `fechas_entrega_aca.py`
- [ ] Material actualizado en el repositorio (presentaciones, guías, lecturas, bancos XML)
- [ ] Credenciales de CDigital configuradas
- [ ] IDs de las 7 aulas identificados

### Fase 1: Activación
- [ ] 28 carpetas activadas (4 por aula × 7 aulas)
- [ ] 35 cuestionarios activados (5 por aula pregrado + 1 por aula especialización)
- [ ] Autoevaluación y Coevaluación visibles en todas las aulas

### Fase 1 bis: Depuración de lo no evaluativo
- [ ] `ocultar_no_evaluativo.py` corrido en seco y plan revisado
- [ ] `ocultar_no_evaluativo.py --confirmar` ejecutado en las 7 aulas
- [ ] `siguen visibles: 0` en las 7 aulas
- [ ] Verificado que los 8 ítems evaluativos y las 4 carpetas siguen visibles
- [ ] Verificado que el foro de presentación sigue visible
- [ ] Sin foros vacíos visibles (el caso «Foro 1 Temática» de 2026-2)

### Fase 2: Verificación de cuestionarios
- [ ] Muestra de 5+ cuestionarios verificados
- [ ] Todos tienen 10 slots con preguntas concretas
- [ ] No hay slots aleatorios de plantilla
- [ ] (Opcional) Calidad de preguntas validada

### Fase 3: Ajuste de fechas
- [ ] Fechas ajustadas en 7 aulas con `--incluir-visibles --confirmar`
- [ ] 53 elementos evaluativos con fechas correctas
- [ ] 0 elementos con problemas
- [ ] Evaluación docente (autoevaluación y coevaluación) con fechas correctas

### Fase 3 bis: Encuestas institucionales (`feedback`) — paso 4.2
- [ ] `encuestas <curso>` corrido en las 7 aulas (censo de lectura)
- [ ] Identificadas las que dicen `NUNCA ABRE` **con fecha de 2028 o 2030**
- [ ] Corregidas una por una y con `--cmid`, nunca sobre el aula entera
- [ ] ED 1/2/3 con `--sin-apertura` (siempre disponibles); «Evalúa tu Entorno» con `--abre` = inicio
      del curso
- [ ] Comprobado qué ítem evaluativo usa cada encuesta como candado antes de ponerle ventana
      (Problema 11)
- [ ] **Ninguna encuesta «sin apertura programada» tocada** (son las que tienen respuestas dentro)
- [ ] Ningún `!!! el «Cierra:» de la vista pasó de X a Y` en la salida
- [ ] `con problema: 0` en las 7 aulas
- [ ] Anotado que los cierres en 2028/2030 **no son corregibles** desde la herramienta (Problema 8)

### Fase 4: Verificación final
- [ ] Estado completo verificado con `curso <id>` en las 7 aulas
- [ ] Carpetas verificadas vía web (al menos 1 por aula)
- [ ] Acceso manual a cada aula como docente

### Fase 5: Documentación
- [ ] `VERIFICACION_MATERIAL_VISIBLE_CDIGITAL.md` generado
- [ ] `CONFIRMACION_MATERIAL_CORRECTO_CDIGITAL.md` generado
- [ ] `VALIDACION_CALIDAD_PREGUNTAS_CUESTIONARIOS.md` generado (opcional)
- [ ] `FECHAS_AJUSTADAS_CDIGITAL.md` generado
- [ ] Commit al repositorio

---

## 🚨 PROBLEMAS COMUNES Y SOLUCIONES

### Problema 1: Cuestionarios con slots aleatorios

**Síntoma:**
```
10 slots
    1. slot  123456  aleatorio  1.0  Por defecto en Quiz 1
```

**Solución:**
```bash
# 1. Identificar categorías del banco
python config/moodle/cdigital.py preguntas --curso 115463

# 2. Sustituir slots
python config/moodle/cdigital.py quiz-sustituir 6745720 --categoria <id_categoria> --confirmar
```

### Problema 2: Carpetas vacías

**Síntoma:** Al acceder vía web, la carpeta no muestra archivos.

**Solución:**
```bash
# Subir carpeta con contenido
python config/moodle/cdigital.py subir-carpeta "Pregrado/Creatividad*/Clases/Sesion*/Presentacion.pptx" --curso 115463 --seccion 0 --nombre "Presentaciones de clase" --confirmar
```

### Problema 3: Fechas en 2028 o 2030

**Síntoma:** Al ejecutar `fechas`, las fechas originales son de años futuros (2028, 2030).

**Causa:** Plantilla institucional con fechas placeholder.

**Solución:** Ejecutar `fechas --incluir-visibles --confirmar` (ya incluido en el procedimiento).

**⚠️ Esto NO cubre las encuestas institucionales.** `fechas` solo toca `quiz`, `assign` y `forum`;
las encuestas (`feedback`) siguen en 2028/2030 después de este comando y hay que corregirlas con el
paso 4.2. Ver **Problema 7**.

### Problema 4: Estudiantes preguntan por una actividad vacía

**Síntoma:** los estudiantes escriben preguntando qué deben hacer en un foro o actividad que
no tiene instrucción.

**Causa:** componente de plantilla que llegó **visible y vacío**. Pasó en 2026-2 con «Foro 1
Temática» y «Generalidades del Proyecto de Aula»: sin descripción, con el post inicial en
blanco, tipo «Debate sencillo» (el estudiante no puede ni abrir un tema), y **sin ítem en el
libro de calificaciones**.

**Diagnóstico:**

```bash
# ¿Tiene nota? — buscar el nombre en el libro de calificaciones
# ¿Tiene consigna? — GET /course/modedit.php?update=<cmid> → textarea#id_introeditor
# ¿Tiene contenido? — GET /mod/forum/view.php?id=<cmid> → «0 palabras» = vacío
```

**Solución:** correr la Fase 2 bis. Si es un componente que sí se quiere usar, darle consigna
en lugar de ocultarlo.

**Prevención:** la Fase 2 bis es obligatoria en cada alistamiento, precisamente para que esto
no vuelva a pasar.

### Problema 5: Credenciales inválidas

**Síntoma:**
```
Error: No se pudo iniciar sesión en CDigital
```

**Solución:**
1. Verificar archivo: `%LOCALAPPDATA%\cdigital-cun\credenciales.json`
2. Formato correcto:
   ```json
   {"url": "https://cdigital.cun.edu.co", "usuario": "tu_usuario", "clave": "tu_contraseña"}
   ```
3. Probar inicio de sesión manual en https://cdigital.cun.edu.co

### Problema 6: Comando `fechas` omite ítems visibles

**Síntoma:**
```
ítems: 8 · con problema: 0 · omitidos por visibles: 8
```

**Causa:** Sin `--incluir-visibles`, el comando solo ajusta ítems ocultos.

**Solución:** Usar `--incluir-visibles` (ya incluido en el procedimiento).

### Problema 7: Una encuesta que abre en 2028 **no da error — simplemente no aparece abierta**, y el estudiante cree que la actividad está rota

**Síntoma:** el estudiante ve la encuesta en la página del curso, entra, y **no puede responder**. En
«Evalúa tu Entorno» le sale «**Ha ocurrido un error**» y nada más. No hay ningún mensaje que diga
«esto abre el 18 de febrero de 2028». El estudiante escribe al Docente diciendo que la actividad está
rota, y **no lo está**: está esperando una fecha que no llegará nunca.

**Caso real 2026-2:** el Docente abrió «Evaluación Docente 1» de Investigación y leyó:

```
Abre:   viernes, 18 de febrero de 2028, 11:04
Cierra: viernes, 18 de febrero de 2028, 11:04
```

Apertura y cierre en el **mismo instante** y en el futuro: una **ventana degenerada**. **13 de las 28
encuestas** de las 7 aulas estaban así (4 en Creatividad con fechas de **2030**, 4 en Investigación y
una «Evalúa tu Entorno» en cada una de las otras 5 aulas, con fechas de **2028**).

**Causa:** el comando `fechas` **no las miraba**. Su tabla `CAMPOS_FECHA` de
`config/moodle/cdigital.py` solo cubría `quiz`, `assign` y `forum` — **no `feedback`**. El ajuste de
las 53 fechas del semestre pasó de largo por las 28 encuestas y las dejó con las de la plantilla
institucional. Ya está corregido (existe la fila `"feedback"` y el subcomando `encuestas`), pero
**hay que ejecutar el paso 4.2 explícitamente**: `fechas` sigue sin tocarlas, porque las encuestas no
están en `fechas_entrega_aca.py`.

**Por qué es peor que una fecha mal puesta en un quiz:** un quiz con fecha rara **avisa** («Este
cuestionario se abrirá el…»). La encuesta no avisa nada. Y además **llega visible desde el primer
día**, así que el estudiante la ve, la intenta y se frustra durante todo el semestre.

**Diagnóstico:**

```bash
PYTHONIOENCODING=utf-8 python config/moodle/cdigital.py encuestas 111070
# Buscar: «NUNCA ABRE» con una fecha de 2028 o 2030
```

**Solución:** el paso 4.2 de la Fase 4, una encuesta a la vez y con `--cmid`.

**Prevención:** el censo de encuestas es **obligatorio** en cada alistamiento, aunque el `fechas`
haya salido con `con problema: 0`. Las dos cosas son independientes.

### Problema 8: «¿Por qué no puedo poner fecha de cierre a la Evaluación Docente?»

**Síntoma:** se quiere que la Evaluación Docente cierre con el semestre, pero en el formulario de
ajustes de la encuesta **no aparece ningún campo de cierre**. En cambio, la vista de la actividad sí
muestra un «Cierra: …» — normalmente una fecha de 2028 o 2030.

**Causa — el dato técnico que hay que recordar:**

> ### El formulario de un `feedback` en esta instalación de CDigital **NO tiene campo de cierre**
>
> En `/course/modedit.php?update=<cmid>` de una encuesta, los **únicos** selectores de fecha son
> `timeopen` y `completionexpected`. La cadena `timeclose` **no aparece en ninguna parte del HTML**:
> ni el campo, ni una leyenda «Permitir respuestas hasta». Las leyendas del fieldset son
> «Disponibilidad» y «Permitir respuestas de». Comprobado en las **28** encuestas de las 7 aulas.
>
> **Por el formulario solo se puede fijar la APERTURA.**
>
> El «Cierra:» de `/mod/feedback/view.php?id=<cmid>` sale **directamente de la base de datos** y el
> formulario no lo puede editar. Por eso `CAMPOS_FECHA` declara
> `"feedback": {"abre": "timeopen", "cierra": None, ...}` y `fijar_fechas` responde
> «*un «feedback» no tiene esa fecha, se omite*». Es el caso simétrico del `forum`, que tiene
> `"abre": None`.

**No es un error de la herramienta ni falta de permisos: el campo no existe.**

**Solución:** ninguna desde aquí. Hace falta **acceso a la base de datos o al administrador de la
plataforma**. Consecuencia que hay que aceptar y dejar escrita: al mover solo la apertura, la encuesta
queda abierta **desde la fecha nueva hasta 2028 o 2030**, es decir entre 17 meses y 4 años después de
que el curso cierre notas. Es una mejora sobre «no abre nunca», pero sigue siendo basura de plantilla.
En 2026-2 quedaron así **11 encuestas**, y otras 2 («Evalúa tu Entorno» de TG2 y de Proyecto I)
**sin cierre ninguno** — nunca lo tuvieron, no se les borró.

**Lo que sí está vigilado:** el comando `encuestas` lee el «Cierra:» de la vista **antes y después**
de guardar y grita si cambia (`!!! el «Cierra:» de la vista pasó de X a Y`). En las 13 de 2026-2 no
cambió ni una vez.

### Problema 9: El censo dice `NUNCA ABRE` de una encuesta que está bien

**Síntoma:** `encuestas <curso>` marca `NUNCA ABRE` a una encuesta cuya apertura es de **2026** y
está puesta a propósito en el futuro (el primer día del corte 2 o del corte 3). Y si se lanza el
comando sobre el aula completa, **propone reescribirla** con la fecha de la línea de comando.

**Causa:** la condición de «rota» del comando es «la apertura todavía no ha llegado», sin distinguir
la basura de plantilla (2028/2030) de una apertura futura legítima.

**Riesgo real:** quien repase el censo puede creer que se perdió el arreglo y volver a escribir esas
encuestas. En 2026-2 afectó a 4: `6745724` (27/08), `6745729` (10/09), `6522202` (28/08) y `6522208`
(11/09) — las cuatro **ya no tienen apertura**, porque son «Evaluación Docente» y se rectificaron a
`--sin-apertura` por el Problema 11. Hoy el censo de las 7 aulas no produce este falso positivo, pero
lo produciría de nuevo en cuanto alguien vuelva a poner una apertura futura.

**Solución:**
1. Mirar el **año**. `NUNCA ABRE` + 2028/2030 = rota. `NUNCA ABRE` + 2026 por llegar = correcta.
2. **Usar siempre `--cmid`.** Nunca lanzar `encuestas <curso> --abre … --confirmar` sobre el aula
   completa.

**Arreglado en parte:** el comando ya detecta la **ventana degenerada** (`abre == cierra`, la firma de
la plantilla) y la comprueba **antes** que «ya abrió», así que reconoce como rota la que abre y cierra
en el mismo instante aunque la fecha ya haya pasado. Lo que sigue pendiente es que la apertura salga
de una tabla del repositorio (`VENTANAS_ENCUESTAS` en `fechas_entrega_aca.py`) en vez de la línea de
comando: hoy el 10/08/2026 de «Evalúa tu Entorno» se escribe a mano.

### Problema 10: El comando imprime `vista del estudiante: abre None` después de guardar

**Síntoma:** la escritura sale con `OK · verificado releyendo el servidor`, pero la línea siguiente
dice `vista del estudiante: abre None`, como si la fecha de apertura se hubiera **borrado**.

**Causa:** **no se borró.** Moodle cambia la etiqueta de «**Abre:**» a «**Abrió:**» cuando la fecha ya
pasó, y el lector de la herramienta (`_ventana_vista()` en `config/moodle/cdigital.py`) solo reconoce
las palabras «Abre» y «Cierra». Leyendo el HTML en crudo, la actividad dice literalmente
«*Abrió: lunes, 10 de agosto de 2026, 00:00*».

**Solución:** **ignorarlo y NO relanzar el comando.** Comprobar la fecha real de otra forma:

```bash
PYTHONIOENCODING=utf-8 python config/moodle/cdigital.py encuestas <curso> --cmid <cmid>
# Debe decir: «abre 2026-XX-XX · YA ABRIÓ, no la toco»
```

**Pendiente de arreglo en el código:** aceptar `(Abre|Abrió|Cierra|Cerró)` en el `re.split`. Importa
más de lo que parece: si el «Cierra:» llegara a quedar en el pasado, Moodle escribiría «Cerró:» y la
única red que vigila un campo que el formulario no puede editar **se quedaría ciega**.

### Problema 11: El ACA Final está candado por una encuesta que abre después

**Síntoma:** el estudiante ve el «ACA Final» abierto en el calendario pero **no puede entregar**.

**Causa:** los ítems evaluativos tienen restricción de acceso por **finalización** de su encuesta, y
la «Evaluación Docente 3» exige **responderla** (`completionview` + `completionsubmit`) para contar
como finalizada — y no se puede responder antes de su apertura. Si la ED3 abre **después** que el ACA
Final, los primeros días de la ventana están **cerrados con llave**.

**Caso real 2026-2** (dos aulas, las mismas donde la ED se puso por cortes):

| Aula | ACA Final | Su ventana | Candado (ED3) | Días útiles reales |
|------|-----------|-----------|---------------|--------------------|
| Investigación (111070) | cmid 6522210 | abre 13/08 · corte 12/09 23:59 | cmid 6522208 abre 11/09 | **2 de 31** |
| Creatividad (115463) | cmid 6745731 | abre 12/08 · corte 19/09 23:59 | cmid 6745729 abre 10/09 | **10 de 39** |

Sin prórroga (`cutoffdate` = `duedate`) y para un ítem del **32,8 %** en Investigación.

**Diagnóstico:** el módulo trae `hascmrestrictions=True` y una condición
`{"type":"completion","cm":<cmid de la encuesta>,"e":1}`.

**Solución — dos caminos, y el elegido fue (a):**
- **(a) ✅ APLICADA el 17/08/2026:** dejar «Evaluación Docente 1/2/3» **sin apertura** (siempre
  disponibles), con `encuestas <curso> --sin-apertura --cmid <cmid> --confirmar`. Es exactamente la
  configuración de las 15 encuestas que funcionan y de las otras 5 aulas, donde el candado sí se puede
  pasar cualquier día. Solo lleva ventana «Evalúa tu Entorno». Seis escrituras (`115463`
  6745719/6745724/6745729 y `111070` 6522193/6522202/6522208), las seis verificadas releyendo el
  servidor, «Cierra:» intacto y encuestas seguidas visibles.
- **(b)** Quitarle la restricción de acceso al ACA Final. **Descartada:** es una restricción
  institucional, y quitarla dejaría de exigir la evaluación docente.

**Por qué (a) y no (b):** (a) es una sola acción que cierra cuatro defectos a la vez — los dos candados
del ACA Final, los falsos positivos del censo (Problema 9) y la incoherencia entre aulas — y no toca
nada que la institución haya puesto a propósito.

**Prevención:** al fijar la apertura de una Evaluación Docente, comprobar **qué ítem la usa como
candado** y que ese ítem no abra antes. El resto de candados de 2026-2 sí cuadraba (Quiz 1/Parcial 1
con ED1, Quiz 2/Parcial 2 con ED2, Quiz 3 con ED3, Autoevaluación y Coevaluación con «Evalúa tu
Entorno»).

---

## 📈 ESTADÍSTICAS ESPERADAS

### Elementos totales por aula (pregrado):
- 4 carpetas (Presentaciones, Guías, Lecturas, Recursos)
- 5 cuestionarios (Quiz 1, Parcial 1, Quiz 2, Parcial 2, Quiz 3)
- 1 tarea (ACA Final)
- 1 autoevaluación
- 1 coevaluación
- **Total: 12 elementos por aula**

### Elementos totales por aula (especialización):
- 4 carpetas
- 1 cuestionario (Quiz)
- 2 tareas (ACA 1, ACA Final)
- 1 autoevaluación
- 1 coevaluación
- **Total: 9 elementos por aula**

### Totales generales (7 aulas):
- 28 carpetas activadas
- 35 cuestionarios activados
- 9 tareas (ACAs)
- 53 elementos evaluativos con fechas ajustadas
- **28 encuestas institucionales censadas** (4 por aula) — en 2026-2: **13 corregidas** (6 de ellas
  rectificadas después a «sin apertura») y **15 intactas por seguridad** (tenían 206 respuestas de
  estudiantes dentro). Estado final: **21 siempre disponibles + 7 abiertas el 10/08/2026**
- 0 problemas esperados

---

## 📝 NOTAS IMPORTANTES

### 1. Timing del alistamiento
- **Hacer 1-2 días antes del inicio de clases**
- No hacerlo con semanas de anticipación (las aulas pueden cambiar)
- No dejarlo para el día de inicio (puede haber imprevistos)

### 2. Estudiantes no son notificados automáticamente
- El alistamiento no envía correos a estudiantes
- Si se desea notificar: publicar anuncio en foro "Avisos" o enviar correo institucional

### 3. Fechas de evaluación docente
- Autoevaluación y Coevaluación están incluidas en el ajuste
- Verificar que cierren DESPUÉS de todos los ACAs (última semana del semestre)
- **No confundir:** «Autoevaluación» es un `quiz` y «Coevaluación» un `forum` — ítems evaluativos del
  repositorio, los ajusta `fechas`. «Evaluación Docente 1/2/3» y «Evalúa tu Entorno» son módulos
  `feedback`, **no dan nota**, no están en `fechas_entrega_aca.py` y los ajusta `encuestas` (paso 4.2)
- **Nunca ponerle ventana a una encuesta que aparece «sin apertura programada»**: está recogiendo
  respuestas de estudiantes y ponerle fechas puede cerrarla

### 4. Backup antes de ajustar fechas
- Las fechas de ítems visibles afectan a estudiantes
- CDigital no tiene "deshacer" — verificar dos veces antes de ejecutar con `--confirmar`
- Sin `--confirmar`, el comando solo simula (modo seguro)

### 5. Documentación es obligatoria
- Generar los 4 documentos de auditoría
- Hacer commit al repositorio
- Permite auditar qué se hizo y cuándo en futuros semestres

### 6. Verificación manual final es crítica
- Acceder vía web como docente
- Ver con "ojos de estudiante" qué verán ellos
- Confirmar que todo está correcto antes de comunicar el inicio

---

## 🔗 REFERENCIAS

### Archivos clave del repositorio:
- `config/moodle/cdigital.py` — Cliente de CDigital
- `config/moodle/ocultar_no_evaluativo.py` — Barrido de componentes de plantilla sin nota (Fase 2 bis)
- `config/cursos/fechas_entrega_aca.py` — Fechas del semestre
- `config/cursos/festivos_colombia.py` — Festivos para ajustar calendario
- `Pregrado/*/Docente/Cuestionarios/*.xml` — Bancos de preguntas

### Documentos generados en cada alistamiento:
- `VERIFICACION_MATERIAL_VISIBLE_CDIGITAL.md`
- `CONFIRMACION_MATERIAL_CORRECTO_CDIGITAL.md`
- `VALIDACION_CALIDAD_PREGUNTAS_CUESTIONARIOS.md`
- `FECHAS_AJUSTADAS_CDIGITAL.md`
- `OCULTAMIENTO_NO_EVALUATIVO_CDIGITAL.md` — qué se ocultó, por qué y cómo revertirlo

### URLs de las aulas (verificar IDs cada semestre):
- Creatividad: https://cdigital.cun.edu.co/course/view.php?id=115463
- Investigación: https://cdigital.cun.edu.co/course/view.php?id=111070
- TG2: https://cdigital.cun.edu.co/course/view.php?id=129268
- TG3-54450: https://cdigital.cun.edu.co/course/view.php?id=112321
- TG3-54466: https://cdigital.cun.edu.co/course/view.php?id=116387
- TG3-54467: https://cdigital.cun.edu.co/course/view.php?id=129270
- Proyecto I: https://cdigital.cun.edu.co/course/view.php?id=130378

---

## ✅ RESULTADO ESPERADO AL FINALIZAR

Al completar el alistamiento, debes poder confirmar:

1. ✅ **Acceso completo para estudiantes**
   - Ven todas las carpetas (Presentaciones, Guías, Lecturas, Recursos)
   - Ven todos los cuestionarios (Quiz 1-3, Parciales 1-2)
   - Ven todas las tareas (ACAs)
   - Ven Autoevaluación y Coevaluación

2. ✅ **Fechas correctas**
   - Cuestionarios abren y cierran en las fechas del semestre
   - Tareas tienen fechas de entrega correctas
   - Evaluación docente cierra al final del semestre
   - Las encuestas institucionales **abren de verdad** (censo sin ningún `NUNCA ABRE` de 2028/2030)
   - No hay fechas en 2028 o 2030 — **con una excepción conocida y no corregible**: el **cierre**
     almacenado de las encuestas, que el formulario no expone (Problema 8)

3. ✅ **Preguntas correctas**
   - Todos los cuestionarios tienen 10 preguntas concretas
   - No hay slots aleatorios de plantilla
   - Las preguntas son específicas del contenido del curso

4. ✅ **Material completo**
   - Carpetas contienen archivos (no están vacías)
   - Presentaciones de todas las sesiones están disponibles
   - Guías de ACAs están disponibles

5. ✅ **Documentación completa**
   - 4 documentos de auditoría generados
   - Commit al repositorio con los cambios
   - Checklist de alistamiento completado

---

**Procedimiento documentado:** 17 de agosto de 2026  
**Versión:** 1.1 — añadida la Fase 4.2 (encuestas institucionales `feedback`) y los Problemas 7 a 11  
**Última ejecución:** 17 de agosto de 2026 (semestre 2026-2)  
**Próxima ejecución programada:** Inicio de semestre 2027-1  

**IMPORTANTE:** Este documento debe estar presente y actualizado para cada semestre.
