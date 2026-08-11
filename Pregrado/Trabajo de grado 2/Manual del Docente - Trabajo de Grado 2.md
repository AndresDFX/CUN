# Manual del Docente — TRABAJO DE GRADO 2 (Modelos de Innovación, Ingeniería de Sistemas)

**Pregrado · Ingeniería de Sistemas · opción de grado II · código 94453 · 2 créditos · virtual.**
Grupo **54448** · periodo **26V04** · BLOQUE ÚNICO · **50 estudiantes** (cupo lleno) · docente **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`

> **Léelo entero antes de la Sesión 01.** Está escrito para alguien que nunca ha dictado esta asignatura: qué pasa en cada encuentro, qué se evalúa y cuándo, qué hay que dejar configurado la primera semana y qué se le entrega a la universidad.
>
> **Ningún dato duro de este manual se escribe a mano.** Fechas, pesos, nombres de ítem, horario y número de estudiantes salen de `config/cursos/carga_academica_2026.json`, `config/cursos/sesiones_cun.py` y `config/cursos/fechas_entrega_aca.py`. Si algo aquí contradice esos archivos, mandan ellos — y hay que corregir este manual.

## 0. Ficha rápida y los tres avisos que cambian tu planeación

| Dato | Valor | Fuente |
|---|---|---|
| Asignatura / código | Trabajo de Grado 2 — Modelos de Innovación (Ing. Sistemas) · **94453** | `carga_academica_2026.json` |
| Unidad / pensum | OPCGV — Opciones de Grado Virtual · OPGVI | ídem |
| Grupo · periodo · bloque | **54448** · 26V04 · BLOQUE ÚNICO (id de grupo en portal: 813242) | ídem |
| Estudiantes | **50 / 50** (cupo lleno) | ídem |
| Modalidad / sede | Virtual · Regional Bogotá · Bogotá Centro · jornada única | ídem |
| **Encuentro sincrónico** | **Lunes, 5:00–6:00 pm — 1 hora** | ídem (`horario.fuente = confirmado_docente`) |
| Encuentros del periodo | **11 sincrónicas** + **4 clases autónomas** por festivo = 15 eventos en la plantilla de calendario | `sesiones_cun.py` + calendario oficial |
| Aula en CDigital | https://cdigital.cun.edu.co/course/view.php?id=129268 | `carga_academica_2026.json → cursos.tg2.cdigital` |
| Enlace de Meet | **vacío todavía** — lo crea el Apps Script de la carpeta del grupo (ver §8) | `…cursos.tg2.meet` |
| Inicio de la oferta | **10/08/2026** | ídem |
| Recepción máx. de trabajos | **14/11/2026** — *fecha operativa, no institucional* (ver §7) | ídem |
| Cierre / registro de notas | **22/11/2026** | ídem |
| Régimen de evaluación | Art. 52 · tres cortes **30 / 30 / 40** · 8 ítems en el libro de calificaciones | §3 |

### ⏱️ Aviso 1 — el encuentro es de UNA hora, no de dos

TG2 tiene **60 minutos sincrónicos por semana**, no más. No hay un segundo bloque de tutoría dentro del encuentro como en Proyecto I: lo que no cabe en esos 60 minutos se va a trabajo autónomo. Y esos 60 minutos **se comparten con los cuestionarios**: los quices y parciales se aplican en clase y consumen entre 10 y 22 minutos del encuentro (ver §5.4). En la Sesión 05 y en la Sesión 08 te quedan menos de 40 minutos reales de contenido. Plan de contingencia obligatorio: en esas dos sesiones el bloque teórico va comprimido y el taller se manda a autónomo.

### 📄 Aviso 2 — TG2 es el único de los cinco cursos sin Syllabus SIAC

En el repositorio, los otros cuatro cursos tienen su `.docx` institucional en la carpeta de la asignatura (`…EI004_VIR.docx`, `…EI005_PRES.docx`, `…94532_PRES_VIR.docx`, `…Proyecto_I_ESP329.docx`). **En `Pregrado/Trabajo de grado 2/` no hay ninguno.** Consecuencia práctica: **no existen «unidades oficiales» de TG2 y este manual no las inventa** (§2). Lo que sí existe y sí manda está listado en «Fuentes que mandan», abajo. Cuando aparezca el `.docx` SIAC, ponlo en la raíz de la asignatura y revisa §2 y el catálogo de sesiones.

### 🔴 Aviso 3 — los cuestionarios existen como ítem, pero NO como actividad

El libro de calificaciones ya tiene los ocho ítems con su peso (§3). Lo que **no** existe todavía en el aula es la **actividad**: Quiz 1–3 y Parcial 1–2 están como línea del gradebook, sin cuestionario y sin banco de preguntas. Entre los cinco suman **64% de la nota** y el primero **abre el 24/08 y cierra el 31/08**. Es la tarea más urgente del periodo y no depende de nadie más. Las guías del estudiante ya están escritas (`Clases/Recursos/ACAs/`) y dicen qué entra en cada uno: úsalas como especificación al redactar las preguntas.

## Fuentes que mandan (y en qué orden)

1. **El aula en CDigital** — https://cdigital.cun.edu.co/course/view.php?id=129268. Manda sobre todo lo demás, incluido este manual. Es la fuente de la estructura de evaluación (auditoría del libro de calificaciones, 2026-08-10).
2. **`config/cursos/fechas_entrega_aca.py`** — ítems, tipos, pesos y ventanas. Genera §3 y la tabla de fechas.
3. **`config/cursos/carga_academica_2026.json`** — oferta: grupo, horario, inicio/recepción/cierre, enlaces de aula y Meet. Excel de origen: `Carga academica 2026.xlsx`.
4. **`config/cursos/sesiones_cun.py`** — catálogo de las 11 sesiones (número, fecha, tema, detalle) y duración del encuentro.
5. **`Calendario de clases (oficial).md`** (raíz de la asignatura) — cronograma con festivos y en qué sesión cae cada ítem. Generado.
6. **`Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`** — ciclo inicio→desarrollo→cierre de pregrado y, sobre todo, **qué sigue pendiente de confirmar con Coordinación**.
7. **`Pregrado/Checklist de cierre de curso a satisfaccion.md`** — verificables de cierre para los cuatro cursos de pregrado.
8. **`Plantilla_APA_CUN_Proyecto de grado.docx`** — formato del documento (raíz del repositorio; copia para estudiantes en `Clases/Recursos/`).

**No aplica a TG2:** el instructivo AFI de Proyecto I/II de Especializaciones (rúbricas, equipos de máximo 3, formularios de registro de sesión y de tutorías). Es de otro programa; usarlo aquí te haría prometerle al grupo reglas que la Escuela de Ingenierías no ha pedido. Ver §7.

## 📁 Estructura de carpetas

| Ruta | Qué hay y para quién |
|---|---|
| `Manual del Docente - Trabajo de Grado 2.md` | Este archivo. **Interno.** Dos bloques suyos se regeneran solos (ver el recuadro que abre §3). |
| `Calendario de clases (oficial).md` | Cronograma generado: 15 eventos, festivos, y en qué sesión cierra cada ítem. **Interno.** |
| `HERRAMIENTAS_EXAMLAB.md` | Análisis de ExamLab como apoyo para redactar los bancos de preguntas. **Borrador para aprobación docente**, no es norma. |
| `Clases/` | **La única carpeta que se comparte con estudiantes.** `Presentacion del Curso - Trabajo de Grado 2.pptx`, `LEEME - Material para estudiantes.docx`, `Recursos/` (plantilla APA + `ACAs/`) y una carpeta `Sesion NN - <tema>/` por sesión con su `Presentacion.pptx`. |
| `Clases/Recursos/ACAs/` | **Un documento por ítem real del aula:** guía de Quiz 1/2/3, guía de Parcial 1/2, enunciado de la ACA Final e instructivos de autoevaluación y coevaluación. Ocho ítems, ocho documentos. |
| `Guiones/` | **Solo docente.** `Sesion NN - <tema>.md`: guion minuto a minuto, autocontenido para los 60 minutos, con fundamento teórico y checklist previo. Más `Guía práctica - Herramientas de escritura y citación.md` (flujo Scholar → ZoteroBib → Docs → CDigital) y `Capturas/`. |
| `2026/54448/` | Todo lo específico de esta oferta: `Informacion.txt`, roster (`Listado estudiantes (CDigital).csv`, `Correos estudiantes (invitados Calendar).txt`), `Correo de bienvenida.docx`, el Apps Script de Calendar y su runbook (§8). |
| `_Archivo obsoleto 2026-08-09/` | Material anterior al renombrado. No usarlo. |

> **Convención de nombres, con una trampa:** el tema del catálogo se usa tal cual en la carpeta del deck y en el guion, **pero los caracteres inválidos para el sistema de archivos se eliminan**. El tema «Estructura del documento / artículo de avance» está en disco como `Sesion 03 - Estructura del documento artículo de avance` (sin la barra). Si buscas la carpeta por el título exacto del calendario, no la encuentras.

## 1. Qué es Trabajo de Grado 2

Es la **fase intermedia** de la opción de grado: el estudiante retoma el proyecto que trae de semestres anteriores, lo delimita, lo sostiene con literatura y **deja diseñada la metodología**, de modo que en Trabajo de Grado 3 solo quede ejecutar y sustentar.

Tres consecuencias que conviene tener claras desde el primer día:

- **Aquí no hay resultados.** No se recolecta, no se aplica instrumento, no se analizan datos. Todo el diseño metodológico se escribe **en propuesto**. El trabajo de campo es de TG3.
- **El producto es un texto que crece, no una carpeta de archivos.** El mismo documento se amplía sesión a sesión sobre la `Plantilla_APA_CUN_Proyecto de grado.docx` y termina siendo la **ACA Final**. Cuando un estudiante entrega fragmentos pegados, es que trabajó por tareas sueltas: corrígelo temprano.
- **El punto de partida real del grupo es un proyecto a medias.** Casi ninguno llega con problema escrito y delimitado; muchos vienen congelados de un semestre anterior. El encuadre de la Sesión 01 existe para responder esa ansiedad antes de que se convierta en deserción.

**No aplica el instructivo AFI de Especializaciones** (Proyecto I/II): ni sus rúbricas unificadas, ni los equipos de máximo tres, ni su cronograma. Extensión orientativa del avance: 18–30 páginas (enunciado de la ACA Final).

## 2. Temario: de dónde sale, ya que no hay Syllabus SIAC

**Este manual no lista «unidades oficiales» de TG2 porque no existen en el repositorio.** Inventarlas sería el error más caro que puede cometer este documento: quedarían citadas en las guías del estudiante, en los cuestionarios y en el acuerdo pedagógico, y no habría con qué respaldarlas.

Lo que sí existe, y sobre lo que puedes pararte sin riesgo:

- **El catálogo de 11 sesiones** de `config/cursos/sesiones_cun.py` (campo `fuente`: «Manual del Docente · analogía con TG3»). Es una ruta coherente de trabajo de grado: formulación (S02–S04) → marcos (S05–S06) → metodología e instrumentos (S07–S08) → integración, socialización y cierre (S09–S11).
- **El material ya construido** sobre ese catálogo: 11 decks, 11 guiones minuto a minuto y ocho documentos de estudiante.
- **El aula en CDigital**, que es la fuente oficial de este grupo para pesos, ventanas y alcance evaluado.

**Dilo con todas sus letras en la Sesión 01** (el guion de esa sesión ya lo trae, slide 7): TG2 no tiene syllabus cargado, el temario es orientativo y lo que manda es CDigital. Reconocerlo genera más confianza que fingir un temario oficial, y deja claro dónde mirar cuando haya dudas.

**Ruta trazada del curso, en una línea:** retomar y delimitar el proyecto → pregunta, objetivos y título → estructura del documento en plantilla APA → antecedentes y marcos → diseño metodológico e instrumentos propuestos → integración y cierre listo para TG3.

> ### ⚠️ Las dos secciones que siguen son GENERADAS — no las edites
>
> `config/cursos/sync_manuales_fechas.py` reescribe **completo** el bloque «## 3. Evaluación…» y el bloque «## Fechas de entrega ACA / cortes» (cada uno, hasta el siguiente encabezado `## `). Nada escrito a mano **dentro** de ellos sobrevive a la próxima ejecución. Si necesitas añadir algo sobre evaluación, va en §6, §7 o §10, que sí son de escritura manual. Regenerar: `python config/cursos/sync_manuales_fechas.py tg2`.

## 3. Evaluación — estructura REAL del aula (CDigital)

**Fuente:** libro de calificaciones del aula en CDigital (auditoría 2026-08-10), cargado en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py tg2`.

Régimen: **Art. 52 · tres cortes** — **Corte 1 = 30%** · **Corte 2 = 30%** · **Corte 3 = 40%**. Configúralo así en CDigital: estos son los ítems que **ya existen** en el libro de calificaciones, con este tipo de actividad y este peso.

| Corte | Ítem en el aula | Tipo de actividad | Peso |
| :---: | :--- | :--- | ---: |
| **1** (30%) | **Quiz 1** | Cuestionario | 6% |
|  | **Parcial 1** | Cuestionario | 24% |
| **2** (30%) | **Quiz 2** | Cuestionario | 9% |
|  | **Parcial 2** | Cuestionario | 21% |
| **3** (40%) | **ACA Final** | Tarea | 32,8% |
|  | **Quiz 3** | Cuestionario | 4% |
|  | **Autoevaluación** | Cuestionario | 1,6% |
|  | **Coevaluación** | Foro | 1,6% |

### Qué desmiente esto del material anterior

- **No hay tres ACAs.** El aula tiene **una sola «ACA Final»** (tarea) en el tercer corte. Los antiguos enunciados ACA 1 / ACA 2 / ACA 3 no correspondían a tres ítems del libro de calificaciones; ya se rehicieron como **un documento por ítem real** (2026-08-10).
- **Queda anulada la regla «cada ACA evalúa el 100% de su corte»** (decisión del 2026-08-10, derogada el mismo día por la auditoría): el desglose real existe y está en la tabla de arriba.
- **Autoevaluación y coevaluación SÍ hacen parte de la nota de este curso** — no son exclusivas de Proyecto I. La **coevaluación es un FORO** (se participa, no se entrega documento) y la **autoevaluación un cuestionario**.
- **Los quices y parciales existen y pesan.** El **Parcial 1 vale 24%** por sí solo. Ya tienen guía para el estudiante en `Clases/Recursos/ACAs/` (`Quiz N (…) - guia del cuestionario.docx` · `Parcial N (…) - guia del cuestionario.docx`), pero en el aula **existen solo como ítem del libro de calificaciones**: falta **crear la actividad** (cuestionario + banco de preguntas) antes de su ventana.

### Notas de este curso

- **Producto documental del curso:** avance consolidado del proyecto/artículo (`Plantilla_APA_CUN_Proyecto de grado.docx`), que se entrega como **ACA Final** (tarea) en el tercer corte.
- **Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem del aula**, incluidas las guías de los quices y parciales.
- ⚠️ Sigue faltando el **Syllabus SIAC**, pero los pesos **ya no son orientativos**: salen del libro de calificaciones del aula. Lo que falta del SIAC es el **temario**, no la evaluación.

Ventanas (apertura · cierre · límite de nota) y en qué sesión cae cada cuestionario: «Fechas de entrega ACA / cortes» más abajo y `Calendario de clases (oficial).md` → «Evaluación en el aula».

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py tg2`.

| Ítem | Tipo | Corte | Peso | Apertura | Cierre | Nota docente |
| :--- | :--- | :---: | ---: | :--- | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 24/08/2026 | 31/08/2026 | 07/09/2026 |
| **Parcial 1** | Cuestionario | 1 | 24% | 07/09/2026 | 14/09/2026 | 21/09/2026 |
| **Quiz 2** | Cuestionario | 2 | 9% | 21/09/2026 | 28/09/2026 | 05/10/2026 |
| **Parcial 2** | Cuestionario | 2 | 21% | 29/09/2026 | 05/10/2026 | 19/10/2026 |
| **ACA Final** | Tarea | 3 | 32,8% | 10/08/2026 | 14/11/2026 | 22/11/2026 |
| **Quiz 3** | Cuestionario | 3 | 4% | 19/10/2026 | 26/10/2026 | 09/11/2026 |
| **Autoevaluación** | Cuestionario | 3 | 1,6% | 09/11/2026 | 22/11/2026 | 22/11/2026 |
| **Coevaluación** | Foro | 3 | 1,6% | 09/11/2026 | 22/11/2026 | 22/11/2026 |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32,8% + Quiz 3 4% + Autoevaluación 1,6% + Coevaluación 1,6%.

> Ventanas fijadas por el Docente (2026-08-10) sobre la estructura real del aula en CDigital: los quices y parciales son cuestionarios y cierran en día de clase (la Sesión 01 es de encuadre y no evalúa); la ACA Final es una tarea y cierra en la fecha máxima de recepción de trabajos; auto y coevaluación van de la última semana al cierre de notas.

## 4. Grupos 2026
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`). Código materia: **94453**.

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre | Inscritos |
|---|---|---|---|---|---|---|
| 54448 | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | 22/11/2026 | 50 / 50 |

> Si se asigna un **segundo grupo** al mismo horario, agrégalo en el JSON y vuelve a generar el material (el título del evento quedará tipo `Grupos 54448 / XXXXX`).

## 5. Cómo guiar cada sesión

### 5.1 La hora, minuto a minuto

El encuentro dura **60 minutos** (lunes 5:00–6:00 pm) y el catálogo lo dimensiona como **60 minutos de contenido**: no hay bloque de tutoría dentro del encuentro. La estructura que traen los guiones es siempre la misma.

| Momento | Duración típica | Qué haces |
|---|---|---|
| Antes de la clase | — | Estudiar el **Fundamento Teórico** del guion, abrir el deck, tener el ejemplo modelado listo y el espacio de entrega de la sesión visible en CDigital. Cada guion cierra con su checklist previo. |
| Apertura | ~5 min | Recibir por nombre, recordar dónde quedó la sesión anterior y qué se produce hoy. |
| Contenido + modelación | ~25–30 min | Explicar el concepto y **modelarlo en vivo sobre un ejemplo**, no solo enunciarlo. Los guiones traen el texto casi literal. |
| Taller sobre el propio proyecto | ~15–20 min | Cada estudiante aplica lo del día a **su** proyecto, con la pantalla compartida cuando haga falta. |
| Cierre y encargo autónomo | ~5–8 min | Nombrar el entregable de la semana, anunciar el movimiento de plataforma del día (§5.4) y decir qué viene. |

**Cuando ese día se aplica un quiz o un parcial, este reparto no cabe.** Reserva el tiempo del cuestionario primero (§5.4) y recorta el taller, nunca la modelación.

### 5.2 Dónde están el guion y el deck

Para cada sesión hay exactamente dos archivos, con el mismo nombre de tema:

- **Guion (solo docente):** `Guiones/Sesion NN - <tema>.md` — autocontenido para 60 minutos, con fundamento teórico, guion literal por bloque, respuestas a las dudas reales que salen ese día, entregable de la sesión y checklist previo. Van de ~1.900 a ~4.000 palabras.
- **Deck (estudiante):** `Clases/Sesion NN - <tema>/Presentacion.pptx`.

Regenerar ambos: `python config/slides/build_sesion_material.py tg2 all` (solo guiones: añade `--guion-only`). Y recuerda la trampa del nombre de carpeta descrita arriba: los caracteres inválidos del tema se eliminan en disco.

### 5.3 Las 11 sesiones

Fechas y temas salen de `config/cursos/sesiones_cun.py`; el movimiento de plataforma, de `config/cursos/fechas_entrega_aca.py`.

| # | Fecha | Qué haces tú en el encuentro | Qué se lleva el estudiante | Plataforma ese día |
|:--:|---|---|---|---|
| **01** | 10/08 | **Encuadre: no dictas tema.** Presentas curso, Docente y grupo (rompehielos en Padlet), abres en pantalla el **libro de calificaciones** para leer los ítems con sus nombres reales, explicas entrega e integridad y **dejas por escrito el acuerdo pedagógico**. | Lectura autónoma sobre delimitación del tema (Arias Castrillón, 2020, en la carpeta de la sesión) + inventario del estado de su proyecto. | Abre la ventana de la **ACA Final** (queda abierta todo el periodo). |
| — | 17/08 | **Festivo (Asunción). Clase autónoma:** no se cancela — la semana se cursa con la lectura y el inventario en CDigital. | — | — |
| **02** | 24/08 | Primera sesión de contenido. Pregunta investigable, objetivo general + 3 específicos con **verbos medibles**, título provisional ≤ 21 palabras, y coherencia vertical entre los tres. | `S02_PreguntaObjetivos_Apellido` | **Abre Quiz 1.** Ábrelo en pantalla en el cierre de la clase. |
| **03** | 31/08 | Estructura del artículo/documento sobre la plantilla APA CUN: outline completo, secciones vacías marcadas, metodología escrita en «propuesto». | `S03_EstructuraAvance_Apellido` | **Cierra Quiz 1** — se aplica en clase (~12 min). |
| **04** | 07/09 | Antecedentes y referentes: búsqueda en Scholar y bases CUN, fichas con ≥ 1 fuente nacional y ≥ 1 internacional, citación con ZoteroBib. | `S04_Antecedentes_Apellido` | **Abre Parcial 1** (24%: anúncialo con nombre y peso). |
| **05** | 14/09 | Marco teórico: derivar 3 constructos de la pregunta y mapearlos a fuentes. **Sesión corta:** el parcial se lleva ~22 de los 60 minutos. | `S05_MarcoTeorico_Apellido` | **Cierra Parcial 1** — se aplica en clase (~22 min). |
| **06** | 21/09 | Marco conceptual y contextual: ≥ 4 definiciones operativas propias del proyecto + 1 página de contexto acotada, con citas. | `S06_ConceptualContextual_Apellido` | **Abre Quiz 2.** |
| **07** | 28/09 | Diseño metodológico **propuesto**: enfoque, tipo, alcance, diseño, y matriz pregunta–método (una fila por objetivo). | `S07_Metodologia_Apellido` | **Cierra Quiz 2** — se aplica en clase (~15 min). |
| **08** | 05/10 | Instrumentos y plan de análisis propuestos: operacionalización variable → indicador → ítem. **Sesión corta** por el parcial. | `S08_Instrumentos_Apellido` | **Cierra Parcial 2** — se aplica en clase (~22 min). ⚠️ Ese parcial **abrió el martes 29/09**, fuera de encuentro: prográmalo con anticipación y anúncialo en la S07. |
| — | 12/10 | **Festivo (Día de la Raza). Clase autónoma.** | — | — |
| **09** | 19/10 | Integración: semáforo por sección (verde/amarillo/rojo) y matriz de gaps con acción concreta. Es la sesión que evita entregas fragmentadas. | `S09_Integracion_Apellido` | **Abre Quiz 3.** |
| **10** | 26/10 | Socialización: pitch de 3 minutos (problema → pregunta → avance → pedido) y feedback entre pares. | `S10_Socializacion_Apellido` | **Cierra Quiz 3** — se aplica en clase (~10 min). |
| — | 02/11 | **Festivo (Todos los Santos). Clase autónoma.** | — | — |
| **11** | 09/11 | Cierre: versión limpia del avance, checklist de cierre y lista de pendientes para TG3. **Última sincrónica antes de la recepción.** | `S11_CierreTG2_Apellido` | **Abren Autoevaluación (cuestionario) y Coevaluación (foro)** — se hacen **en clase**, con el aula proyectada. Es el momento de mayor deserción silenciosa del periodo. |
| — | 16/11 | **Festivo (Independencia de Cartagena). Clase autónoma** — y cae **después** de la recepción del 14/11: no sirve para contenido evaluable, úsala para pendientes y dudas de cierre. | — | — |

### 5.4 Cómo se aplican los quices y los parciales

Es la regla operativa más importante del curso y hay que anunciarla en la Sesión 01:

- Se **abren en un encuentro** y se **cierran en el encuentro siguiente**, en día de clase. La única excepción es **Parcial 2**, que abre un martes.
- **Se resuelven en el aula, dentro del encuentro** — no son entregas que el estudiante suba. Reserva el tiempo dentro de la hora y anúncialo la semana anterior.
- Quien falta ese día **pierde el ítem**; no se «recupera después». Dilo el primer día, no cuando ya pasó.
- Su **documento de estudiante no es el examen**: `Clases/Recursos/ACAs/Quiz N (…) - guia del cuestionario.docx` y `Parcial N (…) - guia del cuestionario.docx` son **la guía de qué entra**. Cada uno lista **las sesiones ya dictadas al cierre** y deja fuera, explícitamente, el tema que se dicta ese mismo día. Los parámetros que sí definen el examen (intentos, tiempo, número y tipo de preguntas, material permitido) los publicas **tú en la descripción de la actividad en CDigital**.

*(La tabla completa de ventanas y límites de nota está en «Fechas de entrega ACA / cortes», arriba. En qué sesión cae cada ítem: `Calendario de clases (oficial).md` → «Evaluación en el aula».)*

### 5.5 Los cuatro festivos

Caen **17/08, 12/10, 02/11 y 16/11** — todos lunes, todos día de clase. **Festivo no es cancelación: es clase autónoma**, con actividad publicada en CDigital. Los cuatro ya están en el calendario y en los archivos de Calendar como eventos marcados «(autónoma)». Cuatro semanas de las quince quedan sin encuentro: si dejas la ACA Final para «las últimas clases», te encuentras con que entre la S11 (09/11) y la recepción (14/11) no hay ningún encuentro más.

## 6. Qué entregan los estudiantes

### 6.1 Los ocho ítems del aula, y qué revisas en cada uno

Los pesos y las ventanas están en §3 y en la tabla de fechas. Aquí va **qué se revisa y con qué criterio**.

| Ítem del aula | Qué es realmente | Qué revisas |
|---|---|---|
| **Quiz 1** | Cuestionario, en clase. | Conceptos de la Sesión 02 (pregunta, objetivos, título) más la lectura autónoma de la S01. Es el primero: sirve tanto de diagnóstico como de nota. |
| **Parcial 1** | Cuestionario, en clase. **Vale 24% por sí solo** — más que cualquier otro ítem salvo la ACA Final. | Acumula S02–S04: formulación, estructura del documento y antecedentes. |
| **Quiz 2** | Cuestionario, en clase. | Acumula hasta S06: marcos teórico, conceptual y contextual. |
| **Parcial 2** | Cuestionario, en clase. | Acumula hasta S07: diseño metodológico propuesto. |
| **Quiz 3** | Cuestionario, en clase. | Acumula hasta S09: instrumentos, plan de análisis e integración. |
| **ACA Final** | **La única entrega documental calificada del curso.** Tarea; documento sobre la plantilla APA CUN; nombre sugerido `TG2_ACAFinal_Apellido`; 18–30 páginas orientativas. | Checklist del enunciado: (1) estado del proyecto y delimitación explícitos; (2) problema, pregunta y objetivos coherentes; (3) antecedentes y marcos pertinentes y actualizados; (4) metodología **propuesta** coherente con la pregunta; (5) instrumentos y plan de análisis definidos, no aplicados; (6) **documento integrado, no fragmentos pegados**; (7) apartado «listo para TG3» + APA 7 + integridad. Además: trazabilidad de las correcciones que ya recibió. |
| **Autoevaluación** | **Cuestionario** individual. No se sube documento, no usa plantilla APA. | Que esté diligenciada dentro de la ventana. Se valora la propia trayectoria (compromiso, aportes, avance del producto) con criterio, no poniéndose cinco. |
| **Coevaluación** | **Foro.** Se **participa escribiendo**; no hay archivo que subir. | Que haya aporte real en el foro: un comentario por compañero, con criterio concreto y algo accionable. «Buen trabajo» no cuenta como participación y no da la nota. |

**Los enunciados ya están escritos**, uno por ítem, en `Clases/Recursos/ACAs/`. Regenerarlos: `python config/slides/build_acas_estudiantes.py tg2`. Ojo con el nombre en disco: es «guia», **sin tilde**.

### 6.2 Los entregables de sesión (formativos, no van al libro de calificaciones)

De la S02 a la S11, cada guion cierra pidiendo un archivo `SNN_<Tema>_Apellido` en CDigital. **No son ítems del gradebook**: son el andamiaje que hace posible la ACA Final, y se revisan en clase o en retroalimentación corta. Son la señal temprana de quién se está descolgando — y también la única forma de detectar a tiempo un documento que se está armando como colección de fragmentos.

Díselo así al grupo: *la nota de cada corte la ponen los cuestionarios y la ACA Final; estos avances semanales son lo que hace que la ACA Final exista.*

### 6.3 Formato de entrega, siempre

- Plantilla institucional `Plantilla_APA_CUN_Proyecto de grado.docx` (en `Clases/Recursos/`), abierta en Google Docs o Word Online — **no se exige Office de escritorio**.
- **Normas APA 7** en todas las citas y referencias.
- **Un solo documento que crece** durante todo el periodo, no un archivo nuevo por sesión.
- Entrega **solo por CDigital**. Drive y correo no sustituyen la plataforma: lo que no está en el aula no existe para el libro de calificaciones.
- Herramientas del curso: gratuitas y en el navegador (Google Docs, Scholar, SciELO, Redalyc, biblioteca CUN, ZoteroBib, Excalidraw). Flujo completo en `Guiones/Guía práctica - Herramientas de escritura y citación.md`.
- **Entrega individual.** Los nombres de archivo son por apellido y cada estudiante trae su propio proyecto (ver §8.3 sobre el punto pendiente de grupos).

## 7. Qué le entregas tú a la universidad

### 7.1 Durante el periodo

| Qué | Cuándo | Dónde |
|---|---|---|
| Aula alistada: bienvenida, material, cortes 30/30/40 y **las actividades de los cinco cuestionarios creadas** | Semana 1 (a partir del **10/08/2026**); Quiz 1 debe estar creado antes del **24/08** | CDigital |
| Clase sincrónica semanal de 60 min · en festivo, **clase autónoma publicada** (no cancelación) | Lunes 5:00–6:00 pm, todo el periodo | Meet + CDigital |
| **Acuerdo pedagógico** socializado y por escrito | Sesión 01 (10/08/2026) | CDigital — *canal institucional pendiente de confirmar (§7.3)* |
| Nota **y retroalimentación** de cada ítem, antes de su fecha límite | **07/09** (Quiz 1) · **21/09** (Parcial 1) · **05/10** (Quiz 2) · **19/10** (Parcial 2) · **09/11** (Quiz 3) · **22/11** (ACA Final, Autoevaluación, Coevaluación) | Libro de calificaciones de CDigital |
| Autoevaluación (cuestionario) y Coevaluación (**foro**) habilitadas y con participación registrada | Ventana **09/11 → 22/11/2026**; se hacen en la Sesión 11 | CDigital |
| Evidencias del curso conservadas en la plataforma | Continuo | CDigital |

Las seis fechas límite de nota salen de la columna «Nota docente» de la tabla de fechas de este manual (`config/cursos/fechas_entrega_aca.py`). No las copies a otro documento: cámbialas ahí y regenera.

### 7.2 Al cierre

| Qué | Fecha | Estatus |
|---|---|---|
| **Recepción máxima de trabajos** — cierra la ACA Final | **14/11/2026** (sábado) | ⚠️ **No es una fecha institucional.** Se derivó como ~8 días antes del cierre de notas y así quedó en la carga académica. Es movible si el periodo lo pide; no la anuncies como norma de la universidad, sino como la fecha de entrega del curso — pero, una vez publicada en CDigital, es la que vale para el estudiante. |
| **Cierre / registro de notas del grupo 54448** | **22/11/2026** | Fecha de la oferta en la carga académica. Todas las notas de los tres cortes deben estar en el libro de calificaciones. |
| Respaldo de evidencias del aula | Antes del cierre | Práctica prudente: hazlo antes de perder acceso. Obligatoriedad y plazo, **por confirmar** (§7.3). |

### 7.3 Lo que NO aplica, y lo que está pendiente de confirmar

**No uses los formularios AFI.** El registro de sesiones del docente, el formulario de asistencia a tutorías del estudiante, el acuerdo pedagógico AFI y el informe de cierre AFI son de **Especializaciones (Proyecto I/II)**. `config/universidades/cun.json → links_afi` los marca así explícitamente. En pregrado no hay hoy PDFs institucionales equivalentes; usarlos aquí sería inventarle a la Escuela de Ingenierías un procedimiento que no ha pedido.

**Sigue pendiente de confirmar con Coordinación / Escuela** (fuente: `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`) — pregúntalo en la semana 1, no en noviembre:

1. Canal del **acuerdo pedagógico** de pregrado: ¿formulario institucional, o basta socializarlo y dejarlo en CDigital?
2. **Cargue y cierre de notas**: ¿solo el gradebook de CDigital, o también un portal académico?
3. **Informe o formato de cierre** de pregrado: ¿existe, o basta con conservar evidencias?
4. **Plazo post-cierre** para correcciones, revisión de notas y descarga de evidencias. *(El plazo de 3 días hábiles del manual AFI es de especialización: no lo extrapoles.)*

Hasta que estén confirmados, los eventos de Calendar de cierre llevan «confirmar con Coordinación» en su descripción: trátalos como recordatorios tuyos, no como norma.

## 8. Configuración técnica de la semana 1

### 8.1 El aula en CDigital

**https://cdigital.cun.edu.co/course/view.php?id=129268** — es el aula real del grupo 54448, ya asignada (`carga_academica_2026.json → cursos.tg2.cdigital`). En la semana 1:

1. Verifica que el libro de calificaciones tenga los **ocho ítems** con los pesos de §3 y que **la suma de cada corte dé 30 / 30 / 40**.
2. **Crea las actividades que faltan.** Los cinco cuestionarios (Quiz 1–3, Parcial 1–2) existen solo como línea del gradebook. Por cada uno: cuestionario + banco de preguntas + ventana + parámetros publicados en la descripción (intentos, tiempo, tipo de preguntas, material permitido). Usa la guía del estudiante correspondiente como especificación de alcance. **Quiz 1 debe estar listo antes del 24/08.**
3. Confirma que la **ACA Final** esté como **tarea** con su ventana abierta desde el 10/08, que la **Autoevaluación** sea **cuestionario** y que la **Coevaluación** sea **foro** — no una entrega de archivo.
4. Publica el material del estudiante: presentación del curso, plantilla APA, enunciados de `Clases/Recursos/ACAs/` y el enlace de Meet.

### 8.2 El encuentro sincrónico

**No crees el evento a mano.** El campo `cursos.tg2.meet` del JSON está vacío a propósito: la sala la crea el propio Apps Script cuando generas los encuentros (§8.4), y el mismo enlace queda en las 11 sesiones. Mientras ese campo siga vacío, el correo de bienvenida, el material del estudiante y el calendario muestran el marcador `[URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 2]` en lugar del enlace real. Cuando lo tengas: pégalo en el JSON, regenera, publícalo en el aula y añade el coanfitrión desde la ficha del evento (eso la API no lo hace).

### 8.3 Grupos: en TG2, por defecto NO hay que configurarlos

A diferencia de Proyecto I, **aquí no hay equipos documentados**: los 50 estudiantes traen cada uno su propio proyecto, los nombres de archivo son por apellido y la ACA Final se entrega individualmente. **No configures grupos ni «elección de grupo» en el aula.**

⚠️ **Punto abierto que sale el primer día.** La pregunta «¿puedo trabajar solo o toca en grupo?» está en el guion de la Sesión 01 sin respuesta cerrada: depende de lo que autorice el programa para la opción de grado. **Resuélvelo con Coordinación en la semana 1 y déjalo escrito en el acuerdo pedagógico**, no a mitad de periodo. Si el programa autoriza equipos, entonces sí hay que crear los grupos y marcar la ACA Final como entrega grupal **antes** de recibir la primera entrega — cambiar eso con entregas ya recibidas desincroniza calificaciones.

### 8.4 Los eventos de Calendar → usa el runbook, no improvises

Hay un runbook paso a paso, específico de este grupo, y es el que manda:

**`Pregrado/Trabajo de grado 2/2026/54448/LEEME - Crear los eventos de Calendar.md`**

Cubre lo que aquí no se repite: activar el servicio avanzado de Calendar, ejecutar `verificar()` antes de tocar nada, crear los **11 encuentros con los 50 estudiantes invitados** y una sola sala de Meet, llevar esa URL al JSON, y cómo deshacer si algo sale mal.

Dos cosas de ese runbook que conviene saber antes de abrirlo:

- **El flujo bueno es `PRINCIPAL - Crear encuentros con invitados.gs`** (Apps Script). Es lo único que añade invitados y crea la sala.
- **Los `.ics` y `.csv` de esa carpeta llevan el prefijo `RESPALDO sin invitados` por una razón:** Google Calendar **descarta la lista de invitados** al importarlos. Si los importas, te quedan los eventos con cero estudiantes y encima ya no puedes usar el script sin borrarlos antes.
- **El script crea las 11 sincrónicas, no las 4 autónomas.** El respaldo `.ics`/`.csv` trae los 15 eventos (incluye los cuatro festivos marcados «Clase autonoma»); el `.gs` solo crea los encuentros. Si quieres los cuatro festivos visibles en tu calendario, créalos tú a mano — es un recordatorio para ti de que esa semana hay que publicar actividad en CDigital, no un encuentro al que invitar a nadie.

Aparte, y ese sí se importa normalmente porque son recordatorios tuyos sin invitados: `Entregas y hitos docentes - Importar a Calendar.csv` (cierres de ítem y trámites del docente).

### 8.5 Comandos de regeneración que te tocan

```text
python config/cursos/sync_manuales_fechas.py tg2         # este manual: §3 + tabla de fechas
python config/slides/build_pregrado_cursos.py --calendar-only   # calendario oficial (rehace el de los 4 cursos de pregrado)
python config/slides/build_calendar_encuentros.py tg2    # el .gs de encuentros con invitados
python config/slides/build_hitos_docentes_calendar.py    # CSV de hitos del docente
python config/slides/build_sesion_material.py tg2 all    # decks + guiones de las 11 sesiones
python config/slides/build_acas_estudiantes.py tg2       # los 8 documentos de Clases/Recursos/ACAs/
python config/slides/build_correo_bienvenida.py          # correo de bienvenida en 2026/54448/
```

## 9. Integridad académica y uso de IA

Se explica en la Sesión 01 (slides 14 y 15 del deck de encuadre) y se sostiene todo el periodo. En trabajo de grado esto se revisa de verdad.

- **Todo lo que no es del estudiante se cita en APA 7**, incluidos fragmentos de sus propios trabajos anteriores: reutilizarlos sin declararlo es **autoplagio**, y en TG2 —un curso que retoma un proyecto de semestres previos— es el riesgo más frecuente.
- **Consejo práctico que sí funciona:** anotar la fuente en el instante de pegar algo. En un documento que crece durante seis meses, reconstruirla después es imposible.
- **IA generativa: sí, con reglas.** Se puede usar para entender un concepto, ordenar una sección o pulir un párrafo ya escrito. Se **declara en una línea al final** del documento. Y **toda referencia se verifica**: estas herramientas inventan autores y DOIs. El argumento que más cala con el grupo: en TG3 hay sustentación ante jurados, y un párrafo que no puedas explicar en voz alta te va a costar caro allá.
- **Similitud:** en TG3 la entrega pasa por la revisión institucional del aula. **No anuncies un umbral numérico en TG2**: el «≤ 10% orientativo» es del instructivo AFI de Especializaciones y no hay equivalente documentado para pregrado. Lo que sí corresponde aquí es formar el hábito de citar y advertir que en TG3 se revisa.
- Un porcentaje alto **no es plagio automáticamente**: exige análisis cualitativo y debido proceso.

## 10. Checklist antes de cada hito

**Antes de la Sesión 01 (10/08/2026)**
- [ ] Guion de la Sesión 01 leído completo (es de encuadre: **no se dicta tema**).
- [ ] Aula de CDigital revisada: ocho ítems, pesos que suman 30/30/40, ACA Final abierta.
- [ ] Encuentros creados con el Apps Script y URL de Meet pegada en `carga_academica_2026.json → cursos.tg2.meet`.
- [ ] Padlet del rompehielos abierto y probado: https://padlet.com/andres_dfx/cun-wruz81hmf9k06gd7 (el QR está en la presentación del curso).
- [ ] Acuerdo pedagógico redactado y listo para dejar por escrito en CDigital.
- [ ] Preguntado a Coordinación: ¿individual o en equipo? ¿canal del acuerdo pedagógico?
- [ ] Anunciado en clase: los cuestionarios **se aplican en clase** y quien falte pierde el ítem.

**Antes de cada quiz o parcial** *(úsalo cinco veces)*
- [ ] **Una semana antes:** actividad creada en CDigital con banco de preguntas, ventana, intentos y tiempo publicados en la descripción; alcance coherente con la guía del estudiante.
- [ ] **En la sesión de apertura:** abierto en pantalla y anunciado con nombre, tipo y peso reales.
- [ ] **El día del cierre:** minutos reservados dentro de la hora (Quiz 1 ~12 · Parcial 1 ~22 · Quiz 2 ~15 · Parcial 2 ~22 · Quiz 3 ~10) y contenido de ese día ajustado a lo que queda.
- [ ] **Antes de la fecha límite de nota:** calificado y con retroalimentación en el libro de calificaciones.
- [ ] ⚠️ **Parcial 2** abre un **martes (29/09)**, fuera de encuentro: programado con antelación y anunciado en la S07.

**Antes de la Sesión 11 (09/11/2026)**
- [ ] Autoevaluación (cuestionario) y Coevaluación (**foro**) habilitadas y visibles, con la ruta ensayada para mostrarlas en pantalla.
- [ ] Anunciado que la ACA Final cierra **después** del último encuentro, y que después no hay más sincrónicas.
- [ ] Ambas actividades **hechas en clase**, no dejadas «de tarea».

**Antes de la recepción (14/11/2026)**
- [ ] Recordatorio con la fecha, el nombre del ítem y la ruta exacta de entrega en CDigital.
- [ ] Verificado que la tarea **ACA Final** acepta entregas hasta ese día y que ningún estudiante quedó sin poder subir.

**Antes del cierre (22/11/2026)**
- [ ] Los ocho ítems calificados, con retroalimentación en la ACA Final.
- [ ] Suma de cortes correcta en el libro de calificaciones: 30 + 30 + 40 = 100.
- [ ] Estudiantes informados de dónde ven la nota definitiva y de la ventana de revisión.
- [ ] Evidencias respaldadas.
- [ ] Repasado `Pregrado/Checklist de cierre de curso a satisfaccion.md`.

## 11. Lo que este manual no puede resolver

Honestidad sobre los bordes, para que nadie los descubra en noviembre:

1. **No hay Syllabus SIAC de TG2.** No hay unidades oficiales, competencias declaradas ni bibliografía institucional. El temario de §2 es una ruta coherente, no un documento aprobado.
2. **No hay rúbrica institucional de la ACA Final.** El checklist de siete criterios de §6.1 sale del enunciado que se le entregó al estudiante — que es lo correcto: se califica con lo que se le anunció. Si la Escuela emite una rúbrica, reemplaza ese checklist y actualiza también el enunciado.
3. **No hay escala de niveles de desempeño documentada para pregrado.** La escala 0,1–2,9 / 3,0–3,5 / 3,6–4,5 / 4,6–5,0 que aparece en el material de Proyecto I es de las rúbricas AFI de Especializaciones. No la traslades sin confirmar.
4. **El trámite de cierre de pregrado está a medias** (§7.3): confírmalo en la semana 1.
5. **Los cuestionarios están por construir.** Es trabajo del docente y es el 64% de la nota (§0, aviso 3).

---

*Manual escrito para un docente que entra por primera vez a esta asignatura. Los bloques §3 y «Fechas de entrega ACA / cortes» son generados: no los edites a mano.*
