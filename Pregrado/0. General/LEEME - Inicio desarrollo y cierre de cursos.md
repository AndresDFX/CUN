# Ciclo docente — Pregrado CUN (Escuela de Ingenierías / Opciones de grado)

**Docente:** Julian Andres Castaño · `julian_castanoe@cun.edu.co`  
**Cursos en este workspace:** Creatividad (EI004) · Investigación C&T (EI005) · TG2 · TG3.  
**Fuente de fechas de oferta:** `config/cursos/carga_academica_2026.json`.

> Esta carpeta **no** mezcla material AFI/Proyecto I-II. Lo de especialización está en `Especializacion/0. General/`.

---

## Qué hay aquí (y qué no)

Hoy no hay PDFs institucionales de pregrado equivalentes a los instructivos AFI. Este LEEME concentra el **ciclo inicio → desarrollo → cierre** y marca con claridad:

| Etiqueta | Significado |
|---|---|
| **Institucional confirmado (workspace)** | Fechas de inicio / recepción / cierre y horarios del JSON de carga; evaluación Art. 52 (cortes 30/30/40) en manuales/syllabus; plataforma = **CDigital**; festivo = clase autónoma. |
| **Pendiente de confirmar con Coordinación** | Formulario exacto de acuerdo pedagógico / informe de cierre de pregrado; URL campus CDigital; canal oficial de cargue de notas (CDigital vs portal académico); plazos de evidencias post-cierre. |

**Compartido con Especialización (raíz workspace):** plantilla APA CUN, `config/`, marca CUN.

---

## Links

| Uso | Link | Estado |
|---|---|---|
| Google Meet (por curso) | `[URL Meet — mismo enlace toda la serie · <Curso>]` | Placeholder — sustituir. |
| CDigital (campus) | `cdigital_url("<curso>")` → `config/cursos/carga_academica_2026.json` | Ya registrado para los cuatro cursos. **No copiar la URL aquí:** TG3 tiene **un aula por grupo** y una sola URL sería la equivocada para dos tercios del curso. |
| Tutorías estudiante (AFI) | https://forms.gle/oZ8xCYiUo3KEWr1d9 | **Solo aplica a Proyecto I/II AFI**, no a pregrado estándar. |
| Registro docente sesiones AFI | https://forms.gle/6t6BXqQ2Kwmivpct8 | **Solo AFI** — no usar en pregrado salvo que Coordinación lo indique. |
| Informe cierre / Acuerdo (forms P1/P2) | https://docs.google.com/forms/d/e/1FAIpQLSej5yUK3b0p617XhccE7GZrm2C4ra3lk-hzfPTx43uJM_xAmg/viewform | **Especialización AFI.** No asumir que aplica a pregrado. |
| Normatividad CUN | https://cun.edu.co/somos-la-cun/normatividad/ | Reglamento estudiantil, estatuto docente, etc. |

### Cierre de pregrado — qué suele quedar pendiente (práctica habitual Colombia / CUN)

Fuentes públicas CUN confirman existencia de **Reglamento Estudiantil**, estatuto docente y normatividad en [cun.edu.co/somos-la-cun/normatividad](https://cun.edu.co/somos-la-cun/normatividad/). No hay en web abierta un instructivo único “cierre de curso pregrado CDigital” con checklist oficial descargable; perfiles y prácticas institucionales apuntan a Moodle/**CDigital** + sistemas de información académica (p. ej. activación/cierre académico) y seguimiento por coordinación de programa.

**Pendiente de confirmar con Coordinación / Escuela** (no inventar plazos ni forms):

1. **Acuerdo pedagógico** al inicio: ¿form/encuesta institucional propia de pregrado o solo socialización del syllabus en CDigital?
2. **Cargue / cierre de notas** en el sistema oficial (¿solo gradebook CDigital o también portal/Q10 u otro?).
3. **Informe de cierre / evidencias** de pregrado: ¿existe formato o solo conservar evidencias en CDigital?
4. **Plazo post-cierre** para correcciones o descargas (en AFI el Manual indica 3 días hábiles para informe; **no extrapolar a pregrado** sin confirmación).
5. URL real del **campus CDigital** de cada curso y Meet único de la serie.

Hasta confirmar: tratar los eventos de Calendar de pregrado marcados “(confirmar Coordinación)” como recordatorios operativos del docente, no como norma institucional.

---

## Checklist — INICIO

### PRE-INICIO: ALISTAMIENTO DE AULAS (OBLIGATORIO)
- [ ] **EJECUTAR ALISTAMIENTO DE AULAS 1-2 DÍAS ANTES DEL INICIO DE CLASES** — seguir el procedimiento completo en `../../ALISTAMIENTO_DE_AULAS_CDIGITAL.md`. Incluye:
  - [ ] Activar material (carpetas y cuestionarios) en las 4 aulas de pregrado
  - [ ] **Ocultar lo no evaluativo:** `python config/moodle/ocultar_no_evaluativo.py --confirmar` — la plantilla trae foros vacíos y SCORM «Contenido N» visibles y sin nota, y los estudiantes preguntan por ellos (caso 2026-2: `DIAGNOSTICO_FORO_1_CREATIVIDAD.md`)
  - [ ] Verificar que cuestionarios tengan preguntas correctas (no slots aleatorios)
  - [ ] Ajustar fechas de todos los elementos evaluativos con `--incluir-visibles`
  - [ ] **Destrabar las encuestas institucionales:** `python config/moodle/cdigital.py encuestas <aula>` — las 4 encuestas por aula («Evaluación Docente 1/2/3» y «Evalúa tu Entorno») **no las toca el paso anterior**, porque no dan nota. En 2026-2 llegaron abriendo en **2028/2030** y nunca abrían: el estudiante recibía «Ha ocurrido un error». ED 1/2/3 → `--sin-apertura`; «Evalúa tu Entorno» → `--abre <inicio del curso>`. **Siempre con `--cmid`**, y nunca las que digan «sin apertura programada» (tienen respuestas dentro)
  - [ ] Generar documentos de auditoría
  - **Duración:** 2-3 horas para las 7 aulas (pregrado + especialización)

### INICIO DEL SEMESTRE
- [ ] Revisar Manual del Docente + syllabus SIAC de la asignatura (el de TG2 llegó el 22/08/2026 sin el código en el nombre: `TRABJO DE GRADO II INGENIERIA DE SISTEMAS.docx`).
- [ ] Publicar Meet único + placeholder CDigital en Presentación del Curso / aula.
- [ ] Alistar CDigital semana 1: bienvenida, syllabus, cortes, rúbricas/actividades.
- [ ] Socializar evaluación Art. 52 (**30% + 30% + 40%**) y reglas de entrega.
- [ ] **Acuerdo pedagógico** — *confirmar canal con Coordinación* (no usar el form AFI salvo indicación).
- [ ] Rompehielos listo según el tamaño del grupo: con más de 20 estudiantes, el evento de Slido del juego «dos verdades y una mentira» (montaje en `2026/<grupo>/Rompehielos Slido - Sesion 01.md`); hasta 20, el muro de Padlet.
- [ ] Importar CSV/ICS de **encuentros** (clases semanales) y, aparte, CSV de **hitos docentes** (mínimo: deadlines ACA + inicio/cierre) desde `2026/<grupo>/`.

### Fechas de oferta 2026 (confirmadas en carga académica)

| Curso | Grupo | Inicio | Recepción | Cierre | Horario |
|---|---|---|---|---|---|
| Creatividad | 54408 | 03/08/2026 | 19/09/2026 | 27/09/2026 | Mié 5–6 pm |
| Investigación | 53339 | 03/08/2026 | 12/09/2026 | 20/09/2026 | Jue 5–6 pm |
| TG2 | 54448 | 03/08/2026 | 14/11/2026 | 22/11/2026 | Lun 5–6 pm |
| TG3 | 54450 | 03/08/2026 | 07/11/2026 | 15/11/2026 | Mar 5–6 pm |
| TG3 | 54466 / 54467 | 03/08/2026 | 14/11/2026 | 22/11/2026 | Mar 5–6 pm |

---

## Checklist — DESARROLLO

- [ ] Clase sincrónica semanal (60 min) · festivo = **autónoma**, con la actividad en el **Drive de clases** (no cancelar; queda en Calendar y se entrega en CDigital).
- [ ] Publicar y calificar actividades de **Corte 1 / 2 / 3** según fechas del aula (confirmar en CDigital; no hay cronograma ACA AFI en pregrado).
- [ ] Retroalimentación verificable antes del cierre de cada corte.
- [ ] Mantener evidencias en CDigital (Drive/correo no sustituyen).

---

## Checklist — CIERRE *(mezcla confirmado + confirmar)*

**Institucional confirmado (workspace):**

- [ ] Respetar **fecha de recepción** (máx. trabajos) y **fecha de cierre** del grupo en carga académica.
- [ ] Tener calificaciones de los tres cortes listas para el cierre del periodo del grupo.

**Pendiente de confirmar con Coordinación:**

- [ ] Cierre formal de notas en el sistema que indique la Escuela.
- [ ] Descarga/respaldo de evidencias (¿obligatorio? ¿plazo?).
- [ ] Informe / formato de cierre de pregrado (si aplica).
- [ ] Comunicación a estudiantes de notas definitivas / ventanas de revisión.

---

## Calendar de hitos vs encuentros

| Archivo | Qué importa el docente |
|---|---|
| `Encuentros…csv/ics` | Clases semanales (Sesión NN); pregrado **sin** invitados estudiantes |
| `Entregas y hitos docentes - Importar a Calendar.csv` | **Solo esencial:** inicio/Syllabus · deadlines ACA (cierre entrega + límite nota; sin aperturas) · cierre notas/evidencias |

En cada `2026/<grupo>/` (+ copia en raíz del curso). Eventos de cierre llevan **“confirmar con Coordinación”** en la Description.  
Regenerar: `python config/slides/build_hitos_docentes_calendar.py`.
