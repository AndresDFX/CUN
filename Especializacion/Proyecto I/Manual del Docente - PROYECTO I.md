# Manual del Docente — PROYECTO I
Especialización en Inteligencia Artificial · Código ESP329
**Léelo ANTES de preparar las guías de las sesiones.** Consolida y cruza TODOS los documentos institucionales recibidos. Es **genérico**: sirve para cualquier grupo/periodo de Proyecto I de este programa — los datos específicos de TU grupo (fechas exactas si cambia el periodo, roster de estudiantes, export de Moodle) viven en `2026/<TU GRUPO>/` (p. ej. `2026/54ES4/`), un nivel abajo de este archivo.

**Fuentes cruzadas en este manual:**
1. **Fuente curricular primaria (syllabus ESP329):** `Especializacion/Proyecto I/Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx` — propósito, macrocompetencia, 7 unidades didácticas, estrategia didáctica, evaluación (ACA 25/25/42 + auto 4% + coev 4%), bibliografía. **No inventar fuera de este documento**; el material de curso se alinea a él.
2. `Especializacion/0. General/01_Instructivos_AFI_Proyecto_I_II/Instructivo_Docentes_Proyecto_I_II_Especializaciones_Rubricas_Unificado.pdf` → resumen en `…/Resumen instructivo - Proyecto I y II.md` — rúbricas, equipos, integridad (cruce AFI **solo si no contradice** el ESP329). Ciclo inicio/cierre: `Especializacion/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`.
3. `Especializacion/0. General/02_Cronogramas_periodo/Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf` — fechas operativas del periodo vigente (ventanas ACA).
4. `Especializacion/0. General/01_Instructivos_AFI_Proyecto_I_II/Instructivo_Configuracion_Grupos_CDigital_Moodle_Docentes_AFI.pdf` — Moodle/CDigital
5. `Especializacion/0. General/01_Instructivos_AFI_Proyecto_I_II/Instructivo_encuentros_sincronicos_Especializaciones_AFI.pdf` — Google Meet
6. `Especializacion/0. General/03_Lineas_investigacion/Lineas_y_ejes_de_investigacion_por_especializacion.xlsx` — líneas de programa IA (complementan el marco institucional del ESP329)
7. `Plantilla_APA_CUN_Proyecto de grado.docx` (en `Cursos/`, raíz) — formato del documento
8. **Específico de tu grupo** (en `2026/<TU GRUPO>/`): `Informacion.txt`, roster/export de Moodle, y los archivos de invitación a Calendar (.ics/.csv + lista de correos).
9. **Carga académica del semestre (editable):** `config/cursos/carga_academica_2026.json` — Proyecto I no figura en el Excel de pregrado; el JSON conserva periodo 26ES4 / grupo 54ES4 / horario lun 8–10 pm.

## 📁 Estructura de carpetas (`Clases/` = estudiante, `Guiones/` = docente)
- **`Clases/`** — **`Presentacion del Curso - Proyecto I.pptx`** (alineada al ESP329: propósito, 7 unidades, evaluación; contacto `julian_castanoe@cun.edu.co`; slide rompehielos con QR; horario lun 8–10 pm; tutorías remarcadas) + **`Sesion NN - <tema>/Presentacion.pptx`** (contenido de la sesión; sin bio docente).
- **`Calendario de clases (oficial).md`** — fechas ACA + festivos + encuentros (raíz).
- **`Guiones/`** — `Sesion NN - <tema>.md` (**solo Markdown**; no hay `.docx`) + `Capturas/`. Regenerar: `python config/slides/build_sesion_material.py proyecto1 all`.
- **`2026/<TU GRUPO>/`** — SOLO lo de esa oferta: `Informacion.txt`, roster, CSV/ICS de Calendar (54ES4 puede incluir invitados). Ver `LEEME - Importar encuentros a Calendar.md`.
- Para generar/regenerar material, usa el agente `disenador-curricular-cun` (temario del **ESP329** + este Manual + AFI sin contradicción; nunca inventar).

---

## ✅ Horario confirmado + 🔴 1 cosa pendiente
- **Horario de la sesión sincrónica: lunes, 8:00–10:00 pm (2 horas).** Cumple el instructivo (franja 19:00-22:00h, 1h30-2h). El **contenido nuevo que preparas por sesión está dimensionado para ~1 hora** (bloque de teoría + modelación); la 2ª hora del encuentro es tutoría/taller en vivo con los equipos — no necesitas material adicional para ese tramo, es acompañamiento flexible.
- 🔴 **Pendiente: ACA 3 (42%) solo tiene 2 lunes de clase** por festivos (19/10 y 26/10). Planea tutorías extra en esas semanas — no lo dejes solo para las sesiones sincrónicas.

---

## PARTE 1 · CÓMO GUIAR CADA SESIÓN

### 1.1 Qué es Proyecto I (para no perder el enfoque)
Según el **ESP329**: inicia la ruta de trabajo de grado; el estudiante delimita una situación problemática y la convierte en un **anteproyecto** coherente, viable y éticamente fundamentado. Macrocompetencia: formular ese anteproyecto (problema, antecedentes, objetivos y ruta metodológica). Producto final: anteproyecto completo para Proyecto II. **Nada se recolecta ni se aplica en Proyecto I** — trabajo de campo = Proyecto II, después del aval metodológico. Tu rol es **garante metodológico**, no experto temático de cada proyecto.

### 1.1-bis Estructura temática ESP329 (7 unidades)
1. Fundamentos y enfoque de investigación  
2. Problema y pregunta de investigación  
3. Objetivos y justificación  
4. Construcción del marco referencial  
5. Diseño metodológico  
6. Planeación y viabilidad del proyecto  
7. Integración y evaluación del anteproyecto  

Las sesiones semanales del calendario AFI **desarrollan** estas unidades (ver `config/cursos/sesiones_cun.py` · campo `unidad_esp329`).

> **La Sesión 01 (10/08/2026) es de ENCUADRE: no se dicta tema.** Se presenta el curso, el Docente, los estudiantes (Padlet) y las ACAs. ESP329 U1 (Fundamentos y enfoque de investigación) → lectura autónoma; se retoma al abrir la Sesión 02. El contenido curricular arranca en la **Sesión 02**.
>
> Consecuencia operativa para la **ACA 1** (cierra dom 30/08, fecha institucional): la única sesión sincrónica de contenido antes del cierre es la **Sesión 02** (24/08). Objetivos, justificación y alcances se acompañan en **tutoría acordada de esa semana**; la Sesión 03 (31/08) los amplía ya después del cierre. Anúncialo en la Sesión 01.

### 1.2 Estructura del encuentro de 2h (8:00-10:00 pm) + tutorías aparte
| Momento | Duración | Qué haces |
|---|---|---|
| Antes de la sesión | — | Publica el material de la semana en Moodle (aula invertida: que el estudiante llegue con lectura/insumo hecho). |
| **Bloque de contenido** (1ª hora, 8:00-9:00 pm) | ~60 min | Explica el concepto del día (con el guion/diapositivas preparados), modelación con ejemplo, resuelve dudas comunes, deja claro el entregable de la semana. |
| **Bloque de tutoría/taller** (2ª hora, 9:00-10:00 pm) | ~60 min | Trabajo en vivo por equipos sobre sus avances puntuales — no requiere material nuevo, es acompañamiento flexible dentro del mismo encuentro. |
| Grabación | — | Todo el encuentro de 2h se graba de corrido. |
| Tutorías adicionales fuera del encuentro (≈5h/semana repartidas, según el instructivo) | — | **Las tutorías por grupo se acuerdan en la semana con el Docente (no hay atención espontánea sin cita).** Revisión extra por equipo cuando lo necesiten — especialmente en las semanas de ACA3 (solo 2 lunes de clase). |
| Dentro de 24h después de cada sesión/tutoría | — | **Tú** registras en tu formulario docente (enlace abajo). |
| En cada tutoría a la que asista un estudiante | — | **El estudiante** debe diligenciar su propio formulario de asistencia: https://forms.gle/oZ8xCYiUo3KEWr1d9 — recuérdaselo, es su evidencia oficial (no sustituye tu registro ni viceversa). |

### 1.3 Metodologías sugeridas por el instructivo
Aula invertida · Aprendizaje Basado en Problemas · microaprendizaje · trabajo colaborativo. **No es clase disciplinar tradicional** — es seguimiento real a los proyectos con intervención didáctica.

### 1.4 Guion de las sesiones (ESP329 × calendario AFI)
Ver fechas en `Calendario de clases (oficial).md`. El AFI exige **frecuencia semanal** (salvo festivo); el **contenido curricular** son las 7 unidades del ESP329.
Cada guion en `Guiones/Sesion NN - ….md` (**solo Markdown**; sin `.docx`) cierra con un **checklist post-clase / seguimiento AFI**: (1) **tú** diligencias el registro de sesión/tutoría **dentro de 24h** con link de grabación — clave `links_afi.formulario_registro_sesiones_docente` en `config/universidades/cun.json` (solo docente); (2) en tutoría recuerdas el formulario de asistencia del **estudiante** — `links_afi.formulario_asistencia_tutorias_estudiante`. **Si Coordinación cambia los URLs el próximo semestre, actualiza solo `cun.json` y regenera.** Solo guiones `.md`: `python "Especializacion/Proyecto I/Guiones/_regen_guiones_proyecto1.py"` o `python config/slides/build_sesion_material.py proyecto1 all --guion-only`.
- **ACA1 (25%) — U2–U3** *(aula: ítem «Quiz», cuestionario)*: problema/pregunta (S02) → objetivos/justificación/alcances (tutoría de esa semana; S03 los amplía tras el cierre). **U1 no se dicta**: va como lectura autónoma de la S01.
- **ACA2 (25%) — U4** *(aula: ítem «ACA 1», tarea)*: antecedentes → marco teórico → conceptual/contextual → legal/APA.
- **Puente (05/10) — U5**: adelantar diseño metodológico antes de festivos de ACA3.
- **ACA3 (42%) — U5–U7** *(aula: ítem «ACA FINAL», tarea)* (solo 2 lunes sincrónicos): metodología completa + planeación/viabilidad + integración del anteproyecto.
- **Cierre — U7**: coevaluación (4%, **foro**) y autoevaluación (4%, **cuestionario**) según ESP329 / cronograma AFI. **No son ACAs**: son instrumentos individuales que cada estudiante participa/diligencia en CDigital (tú los habilitas y registras la nota).

### 1.5 Equipos de trabajo (regla que debes verificar tú)
- **Máximo 3 estudiantes** por equipo (el instructivo de rúbricas dice máx. 3; el instructivo de configuración de Moodle dice mín. 1 – máx. 3 "sin excepción" — usa siempre el máximo de 3).
- Conformación **idealmente en la semana 2, a más tardar al final de la semana 3**.
- **Debes configurar tú mismo en Moodle** (ver Parte 4) los grupos vacíos + la actividad "Elección de grupo" ANTES de habilitar cualquier ACA para entrega.
- Estudiante individual → igual necesita un grupo propio en Moodle (nunca lo dejes sin grupo).

### 1.6 Anclaje temático — líneas de investigación institucionales (Especialización en IA)
Todo anteproyecto de tus estudiantes debe poder ubicarse en alguna de estas 2 líneas oficiales de la Especialización en Inteligencia Artificial (fuente: `Lineas_y_ejes_de_investigacion_por_especializacion.xlsx`):
- **Uso y adaptación de IA para entornos productivos**
- **Implementación de IA en la educación**

Si un equipo propone un tema fuera de estas líneas, oriéntalo para que lo reformule dentro de una de ellas (o consulta a Coordinación si genuinamente no encaja).

### 1.7 Título del anteproyecto (según Plantilla APA)
Sugerencias de la plantilla institucional: máx. 21 palabras, tono afirmativo, claro y directo, alineado con el objetivo general, sin repetir "Estudio sobre…/Investigación de…". Responde qué/por qué/cuándo/cómo/dónde/quién/para qué.

---

## PARTE 2 · QUÉ LE ENTREGAS TÚ (docente) A LA UNIVERSIDAD

### Durante el periodo
| Qué | Cuándo | Dónde |
|---|---|---|
| Configuración de grupos en Moodle (grupos + elección de grupo + ACA configuradas para entrega grupal) | Antes de habilitar la primera ACA, idealmente semana 1 | CDigital (Moodle), aula del curso |
| Alistamiento completo del aula | **Primera semana** del curso | CDigital (Moodle) |
| Calificación + retroalimentación cualitativa **y** cuantitativa de cada ACA | Antes de la "fecha límite para ingreso de nota" de cada una (07/09/2026, 12/10/2026, 16/11/2026) | Moodle (gradebook del curso) |
| Registro de cada sesión sincrónica y cada tutoría, **dentro de 24h**, con el enlace directo de grabación (sin texto adicional en ese campo) | Continuo, todo el periodo | Formulario: https://forms.gle/6t6BXqQ2Kwmivpct8 (uso exclusivo docente, NO compartir con estudiantes) |
| Actualización semanal de invitados al evento de Meet (primeras 3 semanas) | Semanas 1-3 | Google Calendar |
| Habilitar Autoevaluación (**cuestionario**) y Coevaluación (**foro**) individuales (**no son ACAs**: instrumentos que cada estudiante diligencia o en los que participa) | Ventanas oficiales (09-15/11 coevaluación; 16-22/11 autoevaluación) | Moodle |

### Al cierre del periodo (22/11/2026)
| Qué | Plazo | Nota |
|---|---|---|
| **Todas las calificaciones registradas en Moodle** | A más tardar **domingo 22/11/2026** | Fecha oficial única — ignora recordatorios de Moodle desactualizados |
| **Informe Final de Curso** | Dentro de los **3 días hábiles siguientes** al cierre | Formulario (distinto del Acuerdo Pedagógico): https://docs.google.com/forms/d/e/1FAIpQLSej5yUK3b0p617XhccE7GZrm2C4ra3lk-hzfPTx43uJM_xAmg/viewform |
| **Acuerdo Pedagógico** (inicio) | Semana 1 / al abrir el periodo | https://forms.gle/EPHb7tbrEJTC6ey77 — **no** confundir con el Informe de cierre |
| **Descarga y conservación de evidencias** (archivos, entregas, calificaciones) | Antes del cierre — **una vez cerrada el aula, NO se puede volver a entrar** | Local / Drive propio |

### No olvides
- El aval metodológico de cada equipo (que el anteproyecto esté completo, coherente, viable) es tuyo — se documenta a través de la calificación de ACA3.
- Si un proyecto requiere revisión ética, tú lo apruebas metodológicamente PRIMERO y luego se remite a la instancia que indique la DNI — eso normalmente ocurre después del cierre de Proyecto I, no lo gestionas dentro de este periodo salvo que la DNI te lo pida.

---


## Fechas de entrega ACA (Cronograma OFICIAL — fuente única)

Fuente: `Calendario de clases (oficial).md` (raíz de Proyecto I) → tabla "📅 Cronograma OFICIAL", tomada del `Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf` de Coordinación. **No recalcular con otro script** — la tabla que antes vivía aquí (calculada desde inicio 10/08) se retiró el 2026-08-09 por desviarse de estas fechas oficiales.

| Componente (material) | Ítem en el aula (CDigital) | Tipo en el aula | Apertura | Cierre | Fecha límite nota | % | Corte |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **ACA 1** | **Quiz** | Cuestionario | 03/08/2026 | 30/08/2026 | 07/09/2026 | 25% | I |
| **ACA 2** | **ACA 1** | Tarea | 07/09/2026 | 04/10/2026 | 12/10/2026 | 25% | II |
| **ACA 3** | **ACA FINAL** | Tarea | 12/10/2026 | 08/11/2026 | 16/11/2026 | 42% | III |
| **Coevaluación** (no es ACA) | **Coevaluación** | **Foro** | 09/11/2026 | 15/11/2026 | 22/11/2026 | 4% | III |
| **Autoevaluación** (no es ACA) | **Autoevaluación** | Cuestionario | 16/11/2026 | 22/11/2026 | 22/11/2026 | 4% | III |

> **Ojo con los nombres:** la auditoría del libro de calificaciones (2026-08-10) mostró que el aula nombra los ítems distinto — el corte I es un **Quiz** (25%), lo que el material llama ACA 2 es la **ACA 1** del aula y el anteproyecto final es la **ACA FINAL**. Las fechas no cambian (son las de Coordinación); lo pendiente es renombrar los enunciados. El puente documento ↔ ítem vive en `build_acas_estudiantes.ACA_ID_BY_CODE`.
>
> **Las ACAs son tres.** Coevaluación y autoevaluación son **instrumentos individuales de cierre** dentro de su ventana en CDigital (la coevaluación es un **foro**: se participa; la autoevaluación, un **cuestionario**); no son entregables con rúbrica y no llevan el prefijo «ACA». En `config/cursos/fechas_entrega_aca.py` son los ids `coev` y `auto` (`kind="foro"` / `kind="cuestionario"`), y su ventana sale de la tabla `VENTANAS["proyecto1"]`.

## PARTE 3 · QUÉ TE ENTREGAN LOS ESTUDIANTES (por equipo, máx. 3)

> **Nombres en el aula:** ACA 1 → ítem **«Quiz»** (cuestionario) · ACA 2 → ítem **«ACA 1»** (tarea) · ACA 3 → ítem **«ACA FINAL»** (tarea). Ver la tabla de la Parte 5. Los **enunciados del estudiante ya usan los nombres del aula** (realineados el 2026-08-10): `Quiz (25%) - guia del cuestionario.docx` · `ACA 1 (25%) - Formulacion del problema y fundamentacion referencial.docx` · `ACA FINAL (42%) - Anteproyecto integrado.docx`. Los encabezados que siguen abajo conservan la numeración del ESP329 para no romper la trazabilidad curricular.

### ACA 1 — Formulación del problema (25%, cierra 30/08/2026, nota máx. 07/09/2026) · aula: **«Quiz»** (cuestionario)
Planteamiento del problema · Pregunta de investigación · Objetivo general · Objetivos específicos · Justificación · Alcances y limitaciones · Referencias APA 7.
**Enunciado estudiante:** `Clases/Recursos/ACAs/Quiz (25%) - guia del cuestionario.docx`

### ACA 2 — Fundamentación referencial (25%, cierra 04/10/2026, nota máx. 12/10/2026) · aula: **«ACA 1»** (tarea)
Correcciones de ACA1 · Marco referencial (antecedentes —mínimo 6, nacionales e internacionales—, teórico, conceptual, contextual, legal si aplica) · Referencias APA 7.
**Enunciado estudiante:** `Clases/Recursos/ACAs/ACA 1 (25%) - Formulacion del problema y fundamentacion referencial.docx`

### ACA 3 — Diseño metodológico y anteproyecto FINAL (42%, cierra 08/11/2026, nota máx. 16/11/2026) · aula: **«ACA FINAL»** (tarea)
Correcciones de ACA1+ACA2 · Metodología completa (enfoque, tipo/alcance, diseño, población/muestra, plan de análisis, técnicas e instrumentos **propuestos, no aplicados**) · Cronograma · Presupuesto · Referencias APA 7.
**Este es el producto de cierre**: debe ser el anteproyecto COMPLETO e integrado, no un fragmento nuevo.
**Enunciado estudiante:** `Clases/Recursos/ACAs/ACA FINAL (42%) - Anteproyecto integrado.docx`

### Coevaluación (4%, **foro**, ventana 09-15/11) y Autoevaluación (4%, **cuestionario**, ventana 16-22/11) — **no son ACAs**
Son **instrumentos individuales de cierre**, no entregables: la coevaluación se **participa en un foro** y la autoevaluación se **diligencia como cuestionario** en Moodle/CDigital dentro de su ventana. No se sube documento, no usan plantilla APA, no son grupales y **no sustituyen la ACA 3**. Tú los habilitas, verificas cumplimiento y registras el 4% de cada uno antes del cierre de notas. (No aplican en Proyecto II. **Sí existen en los 4 cursos de pregrado**, con peso menor — la afirmación previa de que eran exclusivas de Proyecto I quedó desmentida por la auditoría del 2026-08-10.)
**Instructivos para el estudiante:** `Clases/Recursos/ACAs/Autoevaluacion individual (4%) - instructivo.docx` · `Clases/Recursos/ACAs/Coevaluacion individual (4%) - instructivo.docx` (regen: `python config/slides/build_acas_estudiantes.py proyecto1`).

### Además, en cada tutoría: registro de asistencia del estudiante
El estudiante debe diligenciar **su propio** formulario de asistencia (distinto del tuyo): https://forms.gle/oZ8xCYiUo3KEWr1d9 — recuérdalo en cada encuentro; es su evidencia oficial de participación.

### Formato de entrega (siempre)
- Plantilla institucional: `Plantilla_APA_CUN_Proyecto de grado.docx` (en `Cursos/`, raíz — compartida con Pregrado-Trabajo de Grado).
- Normas **APA 7.ª edición** en todas las citas y referencias.
- Portada con nombres completos de **todos** los integrantes del equipo.
- **Solo un integrante sube** la entrega grupal en Moodle (una vez el equipo esté correctamente configurado).
- Nada aplicado/recolectado — solo lo *propuesto*.

---

## PARTE 4 · CONFIGURACIÓN TÉCNICA (hazlo tú, semana 1)

### 4.1 Moodle — grupos (resumen; detalle en el PDF `Instructivo_Configuracion_Grupos_CDigital_Moodle_Docentes_AFI.pdf`)
1. Configuración del curso → Grupos → **Modo de grupo: Grupos visibles** · **Forzar modo de grupo: Sí**.
2. Participantes → Grupos → Crear grupos automáticamente: esquema `Equipo@`, 3 miembros por grupo, rol Estudiante, **Asignar miembros: No asignación** (quedan vacíos).
3. Crear actividad "Elección de grupo": máx. 3 integrantes, cierre "idealmente semana 2, máximo semana 3".
4. Ítems del aula que reciben entrega grupal — **«ACA 1»** y **«ACA FINAL»** (nuestras ACA 2 y ACA 3) → Entrega por grupos: **Sí**; Requerir pertenecer a grupo: **Sí**; Requerir que todos entreguen: **No**. El ítem **«Quiz»** (nuestra ACA 1) está creado como **cuestionario**: resuelve primero cómo lo vas a operar (ver Parte 5) antes de configurar grupos ahí.
5. Verificar: ningún equipo con más de 3, ningún estudiante sin grupo al terminar semana 3.
⚠️ **No cambies esta configuración después de recibir entregas** — puede desincronizar calificaciones.

### 4.2 Google Meet — encuentro sincrónico (resumen; detalle en `Instructivo_encuentros_sincronicos_Especializaciones_AFI.pdf` + correo Coordinación 6/08/2026)
1. Crear el evento **desde tu cuenta institucional** en Google Calendar, lunes 8:00–10:00 pm (ya confirmado). Para fechas **e invitados del roster**, importa `2026/<TU GRUPO>/Encuentros Proyecto I - Importar a Calendar.ics` (**no** el `.csv`: Google Calendar ignora Guests al importar CSV; ver `LEEME - Importar encuentros a Calendar.md`). Subject corto: `54ES4 - Proyecto I - Sesion NN`. **Aparte**, importa `Entregas y hitos docentes - Importar a Calendar.csv` (mínimo: Acuerdo/Meet AFI + deadlines ACA/auto·coeval + 1 recordatorio registro AFI + recepción/cierre/informe — **no** duplica las Sesión NN).
2. Añadir Google Meet **dentro del evento ya creado** (el mismo enlace se reutiliza automáticamente en todas las repeticiones — "el mismo link siempre"). Programar **todos** los encuentros del periodo 26ES4.
3. Repetición semanal, terminando en la última semana del curso (09/11/2026); los 4 lunes festivos quedan excluidos automáticamente si usas el .ics.
4. Invitar **solo** a estudiantes inscritos del grupo + a `investigacion_especializaciones@cun.edu.co`. **No** agregar otros correos.
5. Asignar a Coordinación como **coanfitrión obligatorio** (Opciones de videollamada → Administración de anfitriones → Coanfitriones) — esto SOLO se puede hacer manualmente en Calendar/Meet; un archivo importado no lo configura.
6. Habilitar **grabación** en cada encuentro (obligatorio AFI).
7. Activar "Ver lista de invitados"; visibilidad Pública si la cuenta lo permite.
8. Publicar el enlace en **CDigital** / Moodle (texto sugerido en el instructivo) y en Avisos.
9. Actualizar invitados semanalmente durante las 3 primeras semanas (estudiantes que se matriculan tarde) — siempre solo inscritos + Coordinación.
10. **Lunes 10/08/2026:** la clase de Proyecto I debe realizarse y grabarse (Coordinación AFI).
11. En lunes festivo: **NO hay sincrónico** — deja clase pregrabada en CDigital (o reprograma solo por esa razón, avisando con anticipación).
12. Si además tienes **Proyecto II**: crear Meet + publicar en Avisos; **no** agregar estudiantes aún.

---

## PARTE 5 · EVALUACIÓN Y RÚBRICAS

### Pesos (ESP329 — nota única Art. 41) y su ítem en el aula (CDigital)

| Componente (material / ESP329) | Ítem en el aula | Tipo de actividad | Peso | Corte del aula |
|---|---|---|---:|:---:|
| **ACA 1** — formulación del problema | **Quiz** | Cuestionario | **25%** | 1 (25%) |
| **ACA 2** — fundamentación referencial | **ACA 1** | Tarea | **25%** | 2 (25%) |
| **ACA 3** — anteproyecto consolidado | **ACA FINAL** | Tarea | **42%** | 3 (50%) |
| **Autoevaluación** (no es ACA) | **Autoevaluación** | Cuestionario | **4%** | 3 (50%) |
| **Coevaluación** (no es ACA) | **Coevaluación** | **Foro** | **4%** | 3 (50%) |

Fuente de la columna del aula: auditoría del libro de calificaciones del **2026-08-10** (`AUDITORIA CDigital 2026-08-10.md` §2), cargada en `config/cursos/fechas_entrega_aca.py` → `ACA_COMPONENTES["proyecto1"]`. **Los pesos y las fechas no cambiaron**; lo que cambió es que ahora sabemos **cómo se llama cada cosa en el aula**, y ahí es donde entras la nota.

Tres consecuencias operativas de esa auditoría:
- **El primer corte del aula es un cuestionario («Quiz»), no una tarea.** Si lo configuras como entrega de documento, el ítem del libro de calificaciones queda sin actividad asociada. Decide cómo lo resuelves (crear la actividad como cuestionario y calificar el documento aparte, o pedirle a Coordinación el cambio de tipo) **antes del 30/08**.
- **La coevaluación es un FORO:** el estudiante *participa*, no sube archivo. Habilítalo como foro con su ventana.
- **A diferencia de pregrado, Proyecto I no tiene quices ni parciales adicionales:** los 5 ítems de la tabla son todo el libro de calificaciones. No busques un «Parcial 1» acá.

**Entregas ACA: tres** (ACA 1, ACA 2, ACA 3) — la DNI establece al menos tres entregas parciales y esa es la configuración operativa de Proyecto I. La autoevaluación y la coevaluación **no son ACAs**: son instrumentos individuales de cierre que diligencia el estudiante (ver Parte 3); **sí existen también en los 4 cursos de pregrado**, con otro peso (allá 1,6% o 2% cada una), así que no las presentes como algo exclusivo de la especialización. Las tres ACAs son seguimiento formativo de un producto único y acumulativo: si ACA 3 evidencia que el estudiante incorporó correcciones y alcanzó resultados, el docente **puede ajustar favorablemente** ACA 1 y ACA 2 con trazabilidad en CDigital (criterio ESP329).

### Escala (AFI / rúbricas)
| Rango | Nivel |
|---|---|
| 0,1–2,9 | Insuficiente |
| 3,0–3,5 | Aceptable |
| 3,6–4,5 | Buen desempeño |
| 4,6–5,0 | Excelente |

Cada una de las **tres ACAs** tiene su propia rúbrica de 5-6 criterios ponderados (PDF `Instructivo_Docentes_Proyecto_I_II_Especializaciones_Rubricas_Unificado.pdf`, Anexo 2, o el resumen). Criterios ESP329 a mirar en conjunto: coherencia, pertinencia, rigor metodológico, calidad de fuentes, escritura académica, integridad y viabilidad.

---

## PARTE 6 · INTEGRIDAD ACADÉMICA
- Similitud (Turnitin u similar) **≤10%** depurada = orientativamente aceptable; por encima **no implica plagio automáticamente**, requiere tu análisis cualitativo con debido proceso.
- Toda entrega en APA 7, con las correcciones de la entrega anterior incorporadas.

---

## Checklist rápido para ti (marca antes de cada hito)
- [x] Horario de la sesión sincrónica confirmado (lunes 8:00-10:00 pm).
- [ ] Aula alistada completamente en la semana 1.
- [ ] Grupos + "Elección de grupo" + los ítems **«ACA 1»** y **«ACA FINAL»** del aula configurados para entrega grupal — ANTES de habilitar entregas.
- [ ] Decidido cómo se opera el ítem **«Quiz»** del primer corte (25%), que en el aula es un **cuestionario** y en el material es la ACA 1 (documento) — antes del 30/08.
- [ ] Coevaluación creada como **foro** (no como cuestionario) con su ventana 09–15/11.
- [ ] Evento de Meet creado (o .ics importado), coanfitrión Coordinación asignado, grabación habilitada, enlace publicado en CDigital.
- [ ] Acuerdo Pedagógico diligenciado/socializado: https://forms.gle/EPHb7tbrEJTC6ey77
- [ ] Clase del **10/08/2026** realizada y grabada.
- [ ] Ningún estudiante sin equipo al cierre de la semana 3.
- [ ] Cada sesión/tutoría registrada por TI en <24h con enlace de grabación — y recuérdales a los estudiantes registrar la suya.
- [ ] ACA1 calificada con retro antes del 07/09/2026; ACA2 antes del 12/10/2026; ACA3 antes del 16/11/2026.
- [ ] Coevaluación y Autoevaluación (instrumentos individuales, **no** ACAs) habilitadas en sus ventanas y diligenciadas por cada estudiante.
- [ ] **Todas las notas en Moodle antes del 22/11/2026.**
- [ ] Informe Final de Curso enviado dentro de 3 días hábiles tras el cierre.
- [ ] Evidencias descargadas ANTES de que se cierre el acceso al aula.
