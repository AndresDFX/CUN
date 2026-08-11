# Manual del Docente — TRABAJO DE GRADO 3 (Modelos de Innovación, Ingeniería de Sistemas)

**Léelo completo antes de la Sesión 01.** Está escrito para alguien que nunca ha dictado esta asignatura.

Código SIAC **94532** · 2 créditos · **32 h de trabajo con docente + 64 h autónomas** · Opción de grado III · prerrequisito **Opción de grado II** · modalidad **VIRTUAL** · unidad **OPCGV — Opciones de Grado Virtual** (Vicerrectoría Académica y de Investigación).
Docente: **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`.

**Horario confirmado: martes, 5:00–6:00 pm. La clase dura UNA hora, no dos.** No es el formato de dos horas de Proyecto I: aquí no hay una segunda hora de tutoría dentro del encuentro. Si necesitas acompañar a alguien aparte, lo acuerdas por fuera.
**Festivo en martes → clase autónoma** (actividad en CDigital, no cancelación). En 2026 esto no llega a pasar: las 15 fechas de la serie aparecen como *Sincrónica* en el `Calendario de clases (oficial).md`, sin ninguna marcada como autónoma.

> **Este curso NO se rige por el instructivo AFI de Proyecto I/II.** Es pregrado. Los formularios AFI —registro docente de sesiones, asistencia de estudiantes a tutorías, informe final de curso, acuerdo pedagógico en Google Forms— **no aplican aquí** salvo indicación escrita de Coordinación. Está dicho así en `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`. Si vienes de leer el Manual de Proyecto I, esa es la primera diferencia que tienes que soltar: **no hay formularios que diligenciar cada 24 horas.**

## Ruta de lectura (media hora, en este orden)

1. **Esta portada** — horario, grupos, qué no aplica.
2. **PARTE 1 · Cómo guiar cada sesión** — el encuentro de 60 minutos y qué pasa en cada una de las 15 clases.
3. **Sección 3 (Evaluación) y Fechas de entrega** — los ocho ítems reales del aula. *Son bloques generados: no los edites a mano.*
4. **PARTE 4 · Configuración técnica de la semana 1** — lo que tienes que dejar montado antes del 11/08.
5. **Checklist accionable** al final — imprímelo.

## Fuentes de este manual

Ningún dato duro de este documento se escribió de memoria. Cada uno sale de aquí:

| # | Fuente | Qué aporta |
|---|---|---|
| 1 | `TRABAJO DE GRADO 3-MDI_INGENIERIA DE SISTEMAS_94532_PRES_VIR.docx` (en esta carpeta) | **Syllabus SIAC.** Descripción, propósito, competencia, **14 unidades de conocimiento**, requisitos del artículo (≥ 50 referencias, ≥ 4.000 palabras), bibliografía, mecanismos de evaluación. |
| 2 | `config/cursos/fechas_entrega_aca.py` | Los **ítems reales del libro de calificaciones** (auditoría CDigital del 2026-08-10): nombre, tipo, peso, corte y ventana **por grupo**. |
| 3 | `config/cursos/carga_academica_2026.json` | Grupos, periodos, horario, inicio/recepción/cierre, aulas de CDigital. |
| 4 | `config/cursos/sesiones_cun.py` | Catálogo de las **15 sesiones**: fecha, título, unidad y detalle. |
| 5 | `Calendario de clases (oficial).md` (esta carpeta) | Cronograma en tabla + «Evaluación en el aula»: en qué sesión cae cada cuestionario. Generado. |
| 6 | `2026/_combinado_todos/LEEME - Crear los eventos de Calendar.md` | **Runbook** para crear los encuentros con invitados y Meet. |
| 7 | `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md` | Ciclo inicio → desarrollo → cierre de pregrado, y **qué sigue pendiente de confirmar con Coordinación**. |
| 8 | `Pregrado/Checklist de cierre de curso a satisfaccion.md` | Verificables de cierre, comunes a los cuatro cursos de pregrado. |
| 9 | `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` | Formato obligatorio del artículo (hay copia en la raíz `Cursos/`). |

Si un dato de este manual choca con el aula de CDigital, **manda el aula** y avisa para corregir la fuente.

## 📁 Estructura de carpetas

- **`Clases/`** — lo que ve el estudiante. `Presentacion del Curso - Trabajo de Grado 3.pptx` (encuadre del semestre) + una carpeta `Sesion NN - <tema>/Presentacion.pptx` por cada una de las **15 sesiones** + `LEEME - Material para estudiantes.docx`.
- **`Clases/Recursos/`** — `Plantilla_APA_CUN_Proyecto de grado.docx` y la subcarpeta **`ACAs/`**, con **un documento por ítem del aula** (8 documentos: 3 guías de quiz, 2 de parcial, el enunciado de la ACA Final y los instructivos de auto y coevaluación).
- **`Guiones/`** — tu material, **solo Markdown**, `Sesion NN - <tema>.md`, uno por sesión (entre ~1.960 y ~4.000 palabras cada uno; el de la S01 es el más largo porque es el de encuadre). Incluye `Capturas/` con los pantallazos que se comparten en pantalla, y `Guía práctica - Herramientas de escritura y citación.md`.
- **`Calendario de clases (oficial).md`** — cronograma + evaluación por sesión. **Generado.**
- **`HERRAMIENTAS_EXAMLAB.md`** — borrador de trabajo sobre el banco de preguntas de los cuestionarios. Es material de decisión, no normativa.
- **`2026/<grupo>/`** (`54450`, `54466`, `54467`) — `Informacion.txt`, `Listado estudiantes (CDigital).csv`, `Correos estudiantes (invitados Calendar).txt`, correo de bienvenida y el calendario recortado al cierre de **ese** grupo.
- **`2026/_combinado_todos/`** — **los encuentros**. Los tres grupos son **una sola serie**: mismo horario, misma sala de Meet, un solo juego de eventos. Contiene el `PRINCIPAL - Crear encuentros con invitados (3 grupos).gs` y su runbook.
- **`_Archivo obsoleto 2026-08-09/`** — no lo uses como referencia.

## 1. Qué es esta asignatura

Es la **culminación del trabajo de grado**. El Syllabus lo define como el espacio en el que el estudiante profundiza en un tema pertinente a su contexto y lo materializa, de manera argumentada y crítica, en **un artículo derivado de un proceso de investigación-creación**.

El producto tiene tres piezas y las tres son obligatorias:

1. **El artículo.** El Syllabus fija el estándar: revisión bibliográfica rigurosa de **al menos 50 referencias** (citando Colciencias, 2009) y una extensión **no inferior a cuatro mil palabras**. En plantilla APA CUN.
2. **La sustentación ante jurados.** La evalúan pares/jurados asignados por la **Dirección del Programa** (Syllabus U13), no solo tú. En el libro de calificaciones **no existe un ítem separado para esto**: se refleja dentro de la ACA Final.
3. **La carga al repositorio institucional** de los entregables del trabajo de grado (Syllabus U14).

**Tu rol.** El Syllabus dice que «se evaluará la calidad argumentativa de los artículos» y que «la evaluación será dada por el docente y por jurados asignados por la Dirección del Programa». En la práctica eres el **garante metodológico y de escritura académica**: llevas a 112 estudiantes desde un proyecto a medio hacer hasta un artículo publicable y defendible. No eres el experto temático de cada uno de los proyectos, y no tienes que serlo.

> **Ojo con el lenguaje del Syllabus.** El documento 94532 es la plantilla MDI (Modelos de Innovación) y habla de «comunicación visual», «obra-creación» y «producto de diseño». Aplicado a **Ingeniería de Sistemas**, léelo como *artefacto o prototipo de software / sistema* donde dice obra-creación. No lo cites literal frente al grupo: confunde.

## 2. Unidades de conocimiento del Syllabus (14 **unidades**, no sesiones)

> **La Sesión 01 (11/08/2026) es de ENCUADRE: no se dicta tema.** Se presenta el curso, el Docente, los estudiantes (Padlet) y las ACAs. U1–U2 (Casos de éxito · retomar proyecto · contexto y planteamiento) → lectura autónoma; se retoma al abrir la Sesión 02. (El acuerdo pedagógico se firma en esta sesión de encuadre.) El contenido curricular arranca en la **Sesión 02**.

> ⚠️ La columna **U#** es la numeración del Syllabus. **U1–U2 se cursan como lectura autónoma de la Sesión 01**, así que a partir de ahí **sesión = unidad − 1**: leer esta tabla como si fueran sesiones es lo que producía el error «sustentación = Sesión 13».

| U# (Syllabus) | Sesión real | Temática |
|---|---|---|
| U1–U2 | **S01** (lectura autónoma) | Casos de éxito · retomar proyecto · contexto y planteamiento |
| U3–U4 | S02–S03 | Pregunta/objetivos · estructura del artículo · introducción |
| U5–U6 | S04–S05 | Referentes I · diseño metodológico / instrumento |
| U7–U8 | S06–S07 | Comunidades de práctica · co-creación · análisis de datos |
| U9–U10 | S08–S09 | Cierre marco teórico · resultados y discusión |
| U11–U12 | S10–S11 | Resumen/UNESCO · póster · antiplagio |
| U13–U14 | **S12–S13** | Sustentación ante jurados · repositorio institucional |
| — | S14–S15 | Buffer de calendario (el grupo 54450 no tiene la S15) |

Elementos de competencia que el Syllabus pide evidenciar: **analizar** información para resolver un problema, **decidir** qué información usar según la función comunicativa del artículo y **argumentar** en procesos de investigación. Resultado de aprendizaje esperado: **divulgar** resultados de investigación con evidencia epistemológica y procedimental.

---

# PARTE 1 · CÓMO GUIAR CADA SESIÓN

## 1.1 El encuentro dura 60 minutos y ya viene repartido

No improvises la estructura: los guiones ya la traen, y está calibrada para una hora exacta.

| Momento | Duración típica | Qué haces |
|---|---|---|
| Antes de la clase | — | Publica el material de la semana en CDigital y abre/cierra en la plataforma lo que corresponda a esa fecha (ver la tabla de 1.2). |
| 1️⃣ **Encuadre** | ~6 min | Portada, objetivos del día, avisos de plataforma. |
| 2️⃣ **Exposición / criterios** | ~14 min | El concepto del día con el deck. |
| 3️⃣ **Modelación** | ~12 min | Lo haces tú en pantalla, con un ejemplo. Es la parte que más se agradece. |
| 4️⃣ **Taller** | ~20 min | Ellos aplican sobre **su propio** artículo. Tú circulas. |
| 5️⃣ **Cierre** | ~8 min | Tres ideas fuerza + tarea autónoma + anuncio de la próxima sesión. |

**En los cinco días en que se aplica un cuestionario, el reparto se recorta** para dejarle sitio a la evaluación dentro de la hora: **S03 → 12 min**, **S06 → 22 min**, **S08 → 15 min**, **S10 → 22 min**, **S12 → 10 min**. En **S14 y S15** se reservan **4 + 4 min** para autoevaluación y coevaluación. Eso ya está descontado en el guion de esas sesiones; no le agregues contenido nuevo.

**Cada guion cierra con dos cosas que te sirven el mismo día:** un bloque «🧩 Entregable de hoy» (el archivo que el estudiante sube a CDigital) y un «✅ Checklist del docente antes de clase» (deck, capturas, ejemplo modelo, espacio de entrega y el ítem de CDigital que se habilita ese día). Ábrelo la noche anterior.

**Dónde está cada cosa, para la sesión NN:**
- Guion → `Guiones/Sesion NN - <tema>.md`
- Deck → `Clases/Sesion NN - <tema>/Presentacion.pptx`
- Capturas de pantalla → `Guiones/Capturas/` (subcarpetas `Sesion NN/` y `Herramientas/`)

## 1.2 Las 15 sesiones, una línea útil cada una

Fechas y títulos salen de `config/cursos/sesiones_cun.py`; la columna de evaluación, de `config/cursos/fechas_entrega_aca.py`. Todas las fechas son **martes**.

| Sesión | Fecha | Unidad | Qué tiene que pasar en el encuentro | Entregable del estudiante | Movimiento en CDigital ese día |
|---|---|---|---|---|---|
| **S01** | 11/08 | Encuadre | Presentarte, presentar el curso y el grupo (Padlet), explicar los 8 ítems del aula por su nombre real y firmar el acuerdo pedagógico. **Hoy no se dicta tema.** | `S01_AcuerdoRetoma_Apellido` | **Abre ACA Final** (queda abierta todo el periodo) |
| **S02** | 18/08 | U3 | Que cada estudiante salga con pregunta, objetivos y título formulados, y con las **variables** identificadas dentro de la pregunta-problema. | `S02_PreguntaObjetivos_Apellido` | **Abre Quiz 1** |
| **S03** | 25/08 | U4 | Estructura del artículo y taller de introducción: contexto → problema → pregunta → objetivos, encadenados. | `S03_Introduccion_Apellido` | **Cierra Quiz 1** (12 min en clase) |
| **S04** | 01/09 | U5 | Fase I de referentes: buscar y fichar literatura por las variables del tema, en diálogo colaborativo. | `S04_ReferentesFaseI_Apellido` | — |
| **S05** | 08/09 | U6 | Matriz de consistencia, enfoque/alcance/diseño, instrumento (o prototipado) y ética de datos. | `S05_MetodoInstrumento_Apellido` | **Abre Parcial 1** |
| **S06** | 15/09 | U7 | Comunidades de práctica y co-creación: socializar problemas y propuestas entre pares. | `S06_CoCreacion_Apellido` | **Cierra Parcial 1** (22 min en clase — la sesión más recortada) |
| **S07** | 22/09 | U8 | Análisis de datos y experiencia creativa; socialización del avance con correcciones aplicadas. | `S07_AnalisisHallazgos_Apellido` | **Abre Quiz 2** |
| **S08** | 29/09 | U9 | Fase III de referentes: cerrar el marco teórico y presentar el cuerpo del documento. | `S08_MarcoCierre_Apellido` | **Cierra Quiz 2** (15 min en clase) |
| **S09** | 06/10 | U10 | Resultados y discusión **con relación explícita a los referentes**: hallazgo contra literatura, no hallazgo suelto. | `S09_ResultadosDiscusion_Apellido` | **Abre Parcial 2** |
| **S10** | 13/10 | U11 | Resumen, palabras clave con **tesauro UNESCO**, conclusiones y referencias: el artículo queda completo hoy. | `S10_CierreArticulo_Apellido` | **Cierra Parcial 2** (22 min en clase) |
| **S11** | 20/10 | U12 | Póster, anexos/evidencias y **verificación antiplagio institucional**. Alistamiento para sustentar. | `S11_PosterEvidencias_Apellido` | **Abre Quiz 3** |
| **S12** | 27/10 | U13 | **Sustentación ante jurados.** Defensa oral. Los jurados los asigna la Dirección del Programa: confírmalos con semanas de anticipación. | `S12_GuionSustentacion_Apellido` | **Cierra Quiz 3** (10 min en clase) |
| **S13** | 03/11 | U14 | Paquete de entregables para el repositorio institucional. Cierre formal del trabajo de grado. | `S13_PaqueteRepositorio_Apellido` | **Abren Autoevaluación y Coevaluación** del **54450** |
| **S14** | 10/11 | Buffer | Ajustes finales y seguimiento post-sustentación. **Última clase del 54450.** | `S14_AjustesPost_Apellido` | **Cierran auto y coevaluación del 54450** · **abren las del 54466/54467** |
| **S15** | 17/11 | Buffer | Cierre administrativo y recepción de entregables. **Solo 54466 y 54467**: el 54450 ya cerró. | `S15_CierreAdmin_Apellido` | **Cierran auto y coevaluación del 54466/54467** |

## 1.3 Los entregables semanales no son notas — y hay que decirlo

Los quince archivos `SNN_..._Apellido` de la columna anterior **no existen como ítem del libro de calificaciones**. Son **avances formativos**: se revisan en clase o por encima en la plataforma, y su función es que la ACA Final del corte 3 llegue escrita en vez de improvisada.

Dilo explícitamente en la Sesión 01, porque genera dos malentendidos opuestos y los dos hacen daño:

- El estudiante que cree que cada archivo semanal le da nota y se relaja creyendo que ya tiene el curso ganado.
- El estudiante que descubre que no dan nota y deja de subirlos — y llega al 07/11 (o al 14/11) con la ACA Final en blanco. **Es la forma más común de perder este curso**, y así está advertido en el propio enunciado del estudiante.

La frase que funciona: *«esto no suma puntos hoy, pero es literalmente el 32% de su nota escrito por partes».*

## 1.4 Tres grupos, una sola clase (y por qué esto importa)

Los 112 estudiantes de 54450, 54466 y 54467 asisten al **mismo encuentro**, en la **misma sala de Meet**, a la misma hora. Es una sola serie de eventos y un solo `.gs` que la crea.

Lo que **no** es igual entre grupos:

- **La fecha de cierre de la ACA Final:** 54450 → **07/11/2026**; 54466 y 54467 → **14/11/2026**.
- **Las ventanas de auto y coevaluación:** una semana antes para el 54450.
- **El cierre de notas:** 15/11 contra 22/11.
- **El aula de CDigital:** son **tres aulas distintas** (ver §4). Todo lo que publiques hay que publicarlo tres veces.
- **La S15 (17/11):** el 54450 **no la tiene**. Para ese grupo el curso termina en la S14.

Práctica que evita el 90% de los líos: **anuncia siempre las dos fechas en voz alta** («los del 54450 cierran el sábado 7; los del 54466 y 54467, el sábado 14») y déjalas escritas en el chat del Meet. Los enunciados en `Clases/Recursos/ACAs/` ya traen las dos.

## 1.5 Metodología que pide el Syllabus

Núcleos problémicos integradores y **plan de aula concertado en el acuerdo pedagógico**, con ABP y proceso dialéctico sobre conceptos y experiencias. Bajo «Metodologías complementarias», el Syllabus ofrece un menú de casillas: clase magistral, seminario, seminario-taller, taller, salida de campo, prácticas, proyectos tutorados y «otros». **Cuáles están marcadas no se puede leer**: las casillas del `.docx` son glifos de formulario y no sobreviven a la extracción de texto. Trátalo como el menú disponible, no como una selección prescrita; si necesitas la marcada, ábrelo en Word. Traducido a una hora semanal con 112 estudiantes: **exposición corta, modelación en pantalla y taller sobre el proyecto propio** — que es exactamente el reparto de 1.1. La clase magistral de 60 minutos no cumple el Syllabus y además no aguanta el formato.

Medios que el Syllabus autoriza y que ya usan los guiones: suite Google en línea, gestor de referencias (Mendeley / ZoteroBib) y biblioteca. Todo gratuito y en la nube: **no exijas software de escritorio de pago.**

## 3. Evaluación — estructura REAL del aula (CDigital)

**Fuente:** libro de calificaciones del aula en CDigital (auditoría 2026-08-10), cargado en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py tg3`.

Régimen: **Art. 52 · tres cortes** — **Corte 1 = 30%** · **Corte 2 = 30%** · **Corte 3 = 40%**. Configúralo así en CDigital: estos son los ítems que **ya existen** en el libro de calificaciones, con este tipo de actividad y este peso.

| Corte | Ítem en el aula | Tipo de actividad | Peso |
| :---: | :--- | :--- | ---: |
| **1** (30%) | **Quiz 1** | Cuestionario | 6% |
|  | **Parcial 1** | Cuestionario | 24% |
| **2** (30%) | **Quiz 2** | Cuestionario | 9% |
|  | **Parcial 2** | Cuestionario | 21% |
| **3** (40%) | **ACA Final** | Tarea | 32% |
|  | **Quiz 3** | Cuestionario | 4% |
|  | **Autoevaluación** | Cuestionario | 2% |
|  | **Coevaluación** | Foro | 2% |

### Qué desmiente esto del material anterior

- **No hay tres ACAs.** El aula tiene **una sola «ACA Final»** (tarea) en el tercer corte. Los antiguos enunciados ACA 1 / ACA 2 / ACA 3 no correspondían a tres ítems del libro de calificaciones; ya se rehicieron como **un documento por ítem real** (2026-08-10).
- **Queda anulada la regla «cada ACA evalúa el 100% de su corte»** (decisión del 2026-08-10, derogada el mismo día por la auditoría): el desglose real existe y está en la tabla de arriba.
- **Autoevaluación y coevaluación SÍ hacen parte de la nota de este curso** — no son exclusivas de Proyecto I. La **coevaluación es un FORO** (se participa, no se entrega documento) y la **autoevaluación un cuestionario**.
- **Los quices y parciales existen y pesan.** El **Parcial 1 vale 24%** por sí solo. Ya tienen guía para el estudiante en `Clases/Recursos/ACAs/` (`Quiz N (…) - guia del cuestionario.docx` · `Parcial N (…) - guia del cuestionario.docx`), pero en el aula **existen solo como ítem del libro de calificaciones**: falta **crear la actividad** (cuestionario + banco de preguntas) antes de su ventana.
- **TG3 no es «corte único = 100%».** El Syllabus 94532 decía corte único con **EV05 50% + EXAM 50%**; el aula tiene **tres cortes 30/30/40** y ni EV05 ni EXAM existen como ítems. Manda el aula.

### Notas de este curso

- **Producto documental del curso:** el **artículo** (≥ 50 referencias, ≥ 4.000 palabras) + sustentación ante jurados + carga a repositorio. Se entrega como **ACA Final** (tarea) en el tercer corte.
- **Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem del aula**. Los antiguos «ACA 1 (EV05)» y «ACA 2 (EXAM)» se refundieron en el enunciado de la **ACA Final**, que es el único entregable documental del aula.
- La **sustentación ante jurados** sigue siendo obligatoria (Sesión 12) y se califica dentro de la **ACA Final**: en el aula no existe un ítem «EXAM» separado.

Ventanas (apertura · cierre · límite de nota) y en qué sesión cae cada cuestionario: «Fechas de entrega ACA / cortes» más abajo y `Calendario de clases (oficial).md` → «Evaluación en el aula».

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py tg3`.

| Ítem | Tipo | Corte | Peso | Apertura | Cierre | Nota docente |
| :--- | :--- | :---: | ---: | :--- | :--- | :--- |
| **Quiz 1** | Cuestionario | 1 | 6% | 18/08/2026 | 25/08/2026 | 01/09/2026 |
| **Parcial 1** | Cuestionario | 1 | 24% | 08/09/2026 | 15/09/2026 | 22/09/2026 |
| **Quiz 2** | Cuestionario | 2 | 9% | 22/09/2026 | 29/09/2026 | 06/10/2026 |
| **Parcial 2** | Cuestionario | 2 | 21% | 06/10/2026 | 13/10/2026 | 20/10/2026 |
| **ACA Final** (54450) | Tarea | 3 | 32% | 11/08/2026 | 07/11/2026 | 15/11/2026 |
| **ACA Final** (54466 / 54467) | Tarea | 3 | 32% | 11/08/2026 | 14/11/2026 | 22/11/2026 |
| **Quiz 3** | Cuestionario | 3 | 4% | 20/10/2026 | 27/10/2026 | 03/11/2026 |
| **Autoevaluación** (54450) | Cuestionario | 3 | 2% | 03/11/2026 | 10/11/2026 | 15/11/2026 |
| **Autoevaluación** (54466 / 54467) | Cuestionario | 3 | 2% | 10/11/2026 | 17/11/2026 | 22/11/2026 |
| **Coevaluación** (54450) | Foro | 3 | 2% | 03/11/2026 | 10/11/2026 | 15/11/2026 |
| **Coevaluación** (54466 / 54467) | Foro | 3 | 2% | 10/11/2026 | 17/11/2026 | 22/11/2026 |

**Cortes:** Corte 1 30% = Quiz 1 6% + Parcial 1 24% · Corte 2 30% = Quiz 2 9% + Parcial 2 21% · Corte 3 40% = ACA Final 32% + Quiz 3 4% + Autoevaluación 2% + Coevaluación 2%.

> Ventanas fijadas por el Docente (2026-08-10) sobre la estructura real del aula en CDigital: los quices y parciales son cuestionarios y cierran en día de clase (la Sesión 01 es de encuadre y no evalúa); la ACA Final es una tarea y cierra en la fecha máxima de recepción de trabajos; auto y coevaluación van de la última semana al cierre de notas.

## 4. Grupos 2026

Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`).

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre | Estudiantes en el roster | Aula en CDigital |
|---|---|---|---|---|---|---:|---|
| **54450** | 26P04 | BLOQUE UNICO | 10/08/2026 | 07/11/2026 | **15/11/2026** | 13 | https://cdigital.cun.edu.co/course/view.php?id=112321 |
| **54466** | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | **22/11/2026** | 49 | https://cdigital.cun.edu.co/course/view.php?id=116387 |
| **54467** | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | **22/11/2026** | 50 | https://cdigital.cun.edu.co/course/view.php?id=129270 |

**112 estudiantes en total** (conteo del rol «Estudiante» en los tres `2026/<grupo>/Listado estudiantes (CDigital).csv`; coincide con los 112 invitados que reporta el runbook de Calendar). El campo `inscritos` del JSON dice 11/50/50 = 111 porque viene del portal y va un paso atrás: **para invitar y para pasar lista, el roster manda**.

> ⚠️ **La fecha de «recepción» no es institucional.** El JSON de carga lo dice literalmente: *«recepcion no viene en el Excel: se conserva la fecha operativa ya usada en el proyecto (típicamente ~8 días antes del cierre)»*. Lo **institucional** son el **inicio del periodo** y el **cierre/registro de notas**. La recepción es una fecha de trabajo que fijamos nosotros para tener margen de calificar, y es movible si Coordinación pide otra cosa.
>
> Consecuencia práctica: el cierre de la **ACA Final** está amarrado a esa fecha derivada (07/11 y 14/11, ambos **sábados**), no a una norma. Si la mueves, muévela en `carga_academica_2026.json` y **regenera**; no la corrijas a mano en los documentos.

---

# PARTE 2 · QUÉ LE ENTREGAS TÚ A LA UNIVERSIDAD

### Durante el periodo

| Qué | Cuándo | Dónde |
|---|---|---|
| Aula alistada: bienvenida, Syllabus, cortes 30/30/40, actividades y enlace de Meet publicado | **Semana 1** (antes del 11/08) | Las **tres** aulas de CDigital |
| **Crear la actividad** de cada cuestionario (Quiz 1/2/3, Parcial 1/2) con su banco de preguntas | Antes de que abra su ventana: 18/08 · 08/09 · 22/09 · 06/10 · 20/10 | CDigital · las tres aulas |
| Calificación **con retroalimentación** de cada ítem | Antes de su «nota docente»: Quiz 1 **01/09** · Parcial 1 **22/09** · Quiz 2 **06/10** · Parcial 2 **20/10** · Quiz 3 **03/11** | Libro de calificaciones |
| Habilitar **Autoevaluación** (cuestionario) y **Coevaluación** (foro) | 54450: ventana 03/11–10/11 · 54466/54467: 10/11–17/11 | CDigital |
| Confirmar **jurados y logística de la sustentación** con la Dirección del Programa | Con semanas de anticipación a la **S12 (27/10)** | Dirección del Programa |
| Verificación **antiplagio institucional** de los artículos | Antes de la sustentación (se trabaja en la **S11, 20/10**) | Ruta oficial del semestre en CDigital |
| Calificar la **ACA Final** | 54450: antes del **15/11** · 54466/54467: antes del **22/11** | Libro de calificaciones |

### Al cierre — y aquí las fechas son dos, no una

| Qué | 54450 | 54466 / 54467 |
|---|---|---|
| Fecha máxima de recepción de trabajos (derivada, ver §4) | 07/11/2026 (sáb) | 14/11/2026 (sáb) |
| Última clase del grupo | **S14 · 10/11** | **S15 · 17/11** |
| **Todas las notas registradas** (institucional) | **15/11/2026** (dom) | **22/11/2026** (dom) |
| Descarga y respaldo de evidencias | Antes del cierre | Antes del cierre |

**Descarga las evidencias antes del cierre.** Una vez cerrada el aula puedes perder el acceso, y el correo o Drive no sustituyen a CDigital como evidencia.

### Lo que en pregrado NO está confirmado (no lo inventes)

Según `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`, estos cuatro puntos siguen **pendientes de confirmar con Coordinación / la Escuela**, y por eso este manual no trae formulario ni plazo para ellos:

1. **Canal del acuerdo pedagógico** en pregrado: ¿formulario institucional propio o basta con socializar el Syllabus y dejar el acta en CDigital? *(El form de Proyecto I es AFI/especialización: no lo uses por defecto.)*
2. **Canal de cargue y cierre de notas:** ¿solo el gradebook de CDigital, o también portal académico?
3. **Informe de cierre de pregrado:** ¿existe formato? El plazo de «3 días hábiles» del AFI **no se extrapola** aquí.
4. **Plazo post-cierre** para correcciones y descarga de evidencias.

Pregúntalos por escrito en la semana 1 y anota la respuesta en ese LEEME, no en este manual.

---

# PARTE 3 · QUÉ TE ENTREGAN LOS ESTUDIANTES

Ocho ítems en el libro de calificaciones y **una sola entrega documental**. Cada ítem tiene su documento en `Clases/Recursos/ACAs/`. **Nómbralos siempre como están en el aula**: así es como el estudiante los va a buscar.

### Los cinco cuestionarios (Quiz 1/2/3, Parcial 1/2) — **no se sube nada**

Se resuelven **en CDigital, dentro de su ventana, y se aplican dentro de la clase** del día en que cierran (por eso el guion de esas sesiones reserva minutos). No son entrega documental: no hay archivo, no hay plantilla APA.

Su documento en `Recursos/ACAs/` es una **guía de estudio**, no el cuestionario. Lo que hace, y por lo que vale la pena que el estudiante la lea, es decir **qué entra**, con dos reglas que tienes que respetar al armar el banco de preguntas:

- **El alcance es acumulativo:** entran *todas* las sesiones ya dictadas cuando el cuestionario cierra, no solo las nuevas desde el anterior. La lectura autónoma de la S01 (U1–U2) también cuenta.
- **El tema del mismo día NO entra:** cada cuestionario cierra en una sesión cuyo contenido se dicta ese mismo día. Si preguntas por él, estás preguntando por algo que aún no se dictó.

| Ítem | Guía en `Clases/Recursos/ACAs/` | Alcance (acumulativo) y qué revisas |
|---|---|---|
| **Quiz 1** (6%) | `Quiz 1 (6%) - guia del cuestionario.docx` | Hasta **S02**. Pregunta, objetivos, título y variables. Es el primero: úsalo como diagnóstico. |
| **Parcial 1** (24%) | `Parcial 1 (24%) - guia del cuestionario.docx` | Hasta **S05** *(nuevo desde Quiz 1: S03–S05)*. Estructura del artículo, referentes fase I, diseño metodológico e instrumento. El ítem más pesado del curso después de la ACA Final. |
| **Quiz 2** (9%) | `Quiz 2 (9%) - guia del cuestionario.docx` | Hasta **S07** *(nuevo: S06–S07)*. Co-creación y análisis de datos. |
| **Parcial 2** (21%) | `Parcial 2 (21%) - guia del cuestionario.docx` | Hasta **S09** *(nuevo: S08–S09)*. Cierre de marco teórico, resultados y discusión. |
| **Quiz 3** (4%) | `Quiz 3 (4%) - guia del cuestionario.docx` | Hasta **S11** *(nuevo: S10–S11)*. Resumen y UNESCO, póster, evidencias y antiplagio. Cae el día de la sustentación. |

**Tú defines en la actividad de CDigital** número de preguntas, intentos, tiempo y tipo de pregunta. Las guías dicen expresamente que esos parámetros los publica el Docente y que **manda lo que diga el aula**. Decídelo antes de abrir cada ventana, no después.

### ACA Final (Tarea · 32%) — la única entrega documental del curso

`Clases/Recursos/ACAs/ACA Final (32%) - Articulo de investigacion.docx`. Abierta desde el **11/08** hasta el 07/11 (54450) o el 14/11 (54466/54467). Nombre sugerido: `TG3_ACAFinal_Articulo_Apellido`.

Qué debe contener, y qué revisas en cada cosa:

| Componente | Criterio con el que lo miras |
|---|---|
| Título, resumen y palabras clave **UNESCO** | Que las palabras clave vengan del tesauro, no inventadas. |
| Introducción: contexto, problema, pregunta y objetivos | Encadenamiento: el problema explica la pregunta y la pregunta genera los objetivos. |
| Marco teórico / referentes (fases completas) | **≥ 50 referencias**, articuladas a la pregunta y no listadas de adorno. |
| Metodología e instrumento (o prototipado / obra-creación) | Matriz de consistencia: cada ítem del instrumento responde a un objetivo. Ética declarada si hay personas. |
| Resultados y discusión | Que los hallazgos se contrasten **explícitamente** con los referentes. Discusión ≠ repetir resultados. |
| Conclusiones y referencias | APA 7 completo y consistente. |
| Extensión | **≥ 4.000 palabras** (Syllabus). |
| Anexos, evidencias y póster | Según lo que hayas pedido en la S11. |
| **Antiplagio verificado** | Antes de la sustentación, por la ruta institucional. |

La **sustentación (S12)** no tiene ítem propio: su desempeño —dominio del contenido, claridad en la defensa, calidad del póster, entregables de repositorio completos— entra dentro de esta misma calificación. El artículo es **acumulativo**: lo que revisas el 07/11 es lo que se fue construyendo desde la S02.

### Autoevaluación (cuestionario · 2%) y Coevaluación (foro · 2%)

**No son ACAs y no se sube documento.** La autoevaluación se diligencia como cuestionario; la coevaluación **se participa en un foro** — si no publica, no participó, y no vale que lo haga un vocero por el equipo. Instructivos: `Autoevaluacion individual (2%) - instructivo.docx` y `Coevaluacion individual (2%) - instructivo.docx`.

Se aplican dentro de la clase (4 + 4 min reservados en S14 y S15). **Ojo con las ventanas por grupo:** el 54450 las tiene del 03/11 al 10/11; el 54466 y el 54467, del 10/11 al 17/11. La autoevaluación del curso **no** es la encuesta institucional SIAC de `acreditacion.cun.edu.co`: esa no da nota.

### Formato de entrega (siempre)

- Plantilla institucional `Plantilla_APA_CUN_Proyecto de grado.docx` (en `Clases/Recursos/`, y copia en la raíz `Cursos/`).
- **APA 7** en todas las citas y referencias.
- Entrega **solo por CDigital**. Correo y Drive no cuentan como entrega ni como evidencia.
- Herramientas gratuitas y en la nube: Google Docs / Word Online, Scholar, SciELO, Redalyc, biblioteca virtual CUN, ZoteroBib, Google Slides o Canva free para el póster.

---

# PARTE 4 · CONFIGURACIÓN TÉCNICA (hazlo tú, semana 1)

### 4.1 Las tres aulas de CDigital

**Son tres aulas separadas.** Todo lo que publiques —avisos, enlace de Meet, deck, cuestionarios, foro de coevaluación— hay que publicarlo tres veces:

- **54450** → https://cdigital.cun.edu.co/course/view.php?id=112321
- **54466** → https://cdigital.cun.edu.co/course/view.php?id=116387
- **54467** → https://cdigital.cun.edu.co/course/view.php?id=129270

> ⚠️ **Detalle que muerde:** los documentos de `Clases/Recursos/ACAs/` imprimen como «entrega oficial» el aula **112321**, que es la del **54450**. Si los publicas tal cual en el 54466 o el 54467, el estudiante hace clic y aterriza en un aula que no es la suya. Adviértelo en clase o entrégalos acompañados del enlace correcto de cada grupo.

En cada aula, semana 1: bienvenida, Syllabus, régimen de **tres cortes 30/30/40** con el desglose por ítem, calendario y reglas de entrega. **Verifica que los ocho ítems sumen 30 + 30 + 40 = 100** en el libro de calificaciones antes de calificar nada.

**Equipos y «Elección de grupo»: no los montes.** La regla de «máximo 3 integrantes» es del instructivo AFI de Proyecto I/II y **es de especialización**. En todo el material de TG3 el trabajo aparece como **individual**: los quince entregables semanales y la ACA Final se nombran `…_Apellido` (en singular), ninguna fuente del curso define equipos y el aula no tiene configuración grupal. Configura la ACA Final como **entrega individual**. *(La única mención a «equipo» está en el instructivo de coevaluación, y es texto de plantilla compartida con los otros cursos: si el programa te dice que en este periodo se trabaja en parejas o tríos, confírmalo antes de abrir la entrega — cambiar el modo de grupo después de recibir trabajos desincroniza calificaciones.)*

### 4.2 Los encuentros y la sala de Meet — usa el runbook, no improvises

**No dupliques aquí los pasos: están en el runbook y ese es el que se mantiene al día.**

📄 **`Pregrado/Trabajo de grado 3/2026/_combinado_todos/LEEME - Crear los eventos de Calendar.md`**

Ese archivo te lleva de cero a los **15 eventos creados, con los 112 estudiantes como invitados y una sola sala de Meet**, en unos cinco minutos, usando `PRINCIPAL - Crear encuentros con invitados (3 grupos).gs` en Apps Script. Cubre: activar el servicio avanzado de Calendar, correr `verificar()` antes de tocar nada, `crearEncuentros()`, el interruptor `SEND_INVITES`, qué hacer si algo falla y cómo deshacer.

Lo único que tienes que saber antes de abrirlo:

1. **No importes el `.ics` ni el `.csv`.** Google Calendar **descarta la lista de invitados** al importar esos formatos: te quedarían 15 eventos con cero estudiantes. Por eso se llaman `RESPALDO sin invitados - …`.
2. **Es una sola serie para los tres grupos.** No ejecutes el script tres veces ni crees una sala por grupo.
3. **La S15 (17/11) invita solo al 54466 y al 54467.** El script ya lo hace solo.
4. **Al terminar, pega la URL de Meet** en `config/cursos/carga_academica_2026.json → cursos.tg3.meet` (hoy está vacío) y regenera el material. Mientras siga vacío, el correo de bienvenida, los guiones y el calendario muestran el marcador `[URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 3]` en vez del enlace real. **Es el único paso manual que queda.**
5. **A mano en Calendar, después:** coanfitrión del Meet y publicación del enlace en las **tres** aulas.

Aparte de la serie de encuentros, cada `2026/<grupo>/` trae su `Entregas y hitos docentes - Importar a Calendar.csv` con los hitos del grupo (deadlines y cierre). Ese sí se importa, y es **distinto por grupo**: no importes el mismo tres veces.

### 4.3 Antes de la Sesión 01

Guion `Guiones/Sesion 01 - …md` (léelo casi literal, dura 60 min). Ten listo: el deck de encuadre (22 slides), el tablero **Padlet** del rompehielos (https://padlet.com/andres_dfx/cun-wruz81hmf9k06gd7 — es el mismo tablero de la Presentación del Curso, no dos rompehielos), el **acuerdo pedagógico** para firmar en esa sesión, y el aviso de que la **ACA Final abre hoy**.

---

# PARTE 5 · INTEGRIDAD ACADÉMICA

- **Verificación antiplagio institucional obligatoria** antes de la sustentación; es una unidad del Syllabus (U12), no un trámite opcional. Usa la ruta oficial que publique el semestre en CDigital — **no cites una URL de herramienta que no sea la institucional**.
- Un porcentaje de similitud alto **no es plagio automático**: exige tu análisis cualitativo y debido proceso. Similitud depurada baja es orientativamente aceptable; lo que descalifica es la copia sin atribución.
- **Los cuestionarios son individuales.** Suplantación, copia o compartir preguntas y respuestas tienen debido proceso disciplinario. Con 112 estudiantes en una sola sala, aleatoriza el orden de preguntas y respuestas en CDigital.
- **IA generativa:** para entender, no para transcribir. El criterio que ya está escrito en las guías del estudiante es que el cuestionario pregunta por comprensión y el artículo se defiende ante jurados — quien no escribió su texto no lo sostiene en la S12.
- **Toda entrega en APA 7**, con las correcciones de la revisión anterior incorporadas. El artículo es acumulativo: entregar el 07/11 algo que no pasó por las revisiones semanales es la señal de alarma más confiable.

---

# CHECKLIST ACCIONABLE

### Antes del 11/08 — semana 1
- [ ] Syllabus 94532 leído (14 unidades) y este manual completo.
- [ ] **Tres** aulas de CDigital alistadas: bienvenida, Syllabus, cortes 30/30/40 con desglose por ítem, calendario.
- [ ] Los **8 ítems** verificados en el libro de calificaciones de cada aula: suman 30 + 30 + 40.
- [ ] Encuentros creados con el `.gs` del runbook (`2026/_combinado_todos/LEEME - Crear los eventos de Calendar.md`); `verificar()` corrido antes.
- [ ] URL de Meet pegada en `carga_academica_2026.json → cursos.tg3.meet` y material regenerado.
- [ ] Enlace de Meet publicado en las tres aulas; coanfitrión asignado.
- [ ] `Entregas y hitos docentes - Importar a Calendar.csv` importado **por grupo** (son distintos).
- [ ] Canal del acuerdo pedagógico preguntado por escrito a Coordinación (ver Parte 2).
- [ ] Guion y deck de la S01 abiertos; Padlet probado.

### Antes de cada cuestionario (18/08 · 08/09 · 22/09 · 06/10 · 20/10)
- [ ] **Actividad creada** en las tres aulas, no solo el ítem del libro de calificaciones.
- [ ] Banco de preguntas cargado; intentos, tiempo y aleatorización definidos.
- [ ] Alcance anunciado en clase y coherente con la guía del estudiante (hasta la sesión anterior).
- [ ] Minutos reservados en el guion del día del cierre (12 / 22 / 15 / 22 / 10).
- [ ] Nota y retroalimentación cargadas antes de su fecha límite (01/09 · 22/09 · 06/10 · 20/10 · 03/11).

### Antes de la sustentación (S12 · 27/10)
- [ ] Jurados confirmados con la Dirección del Programa.
- [ ] Antiplagio institucional corrido para todos los artículos (trabajado en la S11).
- [ ] Póster y evidencias revisados.
- [ ] Orden, tiempos y modalidad de la defensa comunicados al grupo.

### Cierre — 54450
- [ ] ACA Final recibida el **07/11**; auto y coevaluación cerradas el **10/11**.
- [ ] **Todas las notas** en CDigital antes del **15/11**.
- [ ] Evidencias descargadas antes de perder el acceso al aula.

### Cierre — 54466 / 54467
- [ ] ACA Final recibida el **14/11**; auto y coevaluación cerradas el **17/11**.
- [ ] **Todas las notas** en CDigital antes del **22/11**.
- [ ] Evidencias descargadas antes de perder el acceso al aula.

---

## Lo que este manual deliberadamente NO trae

- **Rúbrica con escala de niveles por criterio.** El Syllabus 94532 no la incluye y el aula tampoco; la escala 0,1–2,9 / 3,0–3,5 / 3,6–4,5 / 4,6–5,0 del instructivo AFI es de especialización y aquí no aplica por defecto. Los criterios de la Parte 3 salen del enunciado real del estudiante; si necesitas una rúbrica formal, pídesela a la Escuela.
- **Formularios de registro de sesiones, tutorías e informe de cierre.** Son AFI/especialización. Usarlos en pregrado sin instrucción de Coordinación genera evidencia en el sitio equivocado.
- **Configuración de equipos y «Elección de grupo».** Todo el material de TG3 trata el trabajo como individual y ninguna fuente del curso define equipos; la regla de «máximo 3» es del instructivo AFI de especialización. Si el programa dispone otra cosa este periodo, confírmalo **antes** de abrir la entrega (ver §4.1).
- **Fecha, hora y jurados de la sustentación.** Los asigna la Dirección del Programa y no están en ninguna de las fuentes del repositorio. Confírmalos tú.
- **Parámetros de los cuestionarios** (número de preguntas, tiempo, intentos). Los define el Docente en el aula; ninguna fuente los fija, y las guías del estudiante lo dicen así explícitamente.
