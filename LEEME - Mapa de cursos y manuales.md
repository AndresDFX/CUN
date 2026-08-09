# Mapa de `Cursos/` — CUN

**Docente (interno):** Julian Andres Castaño · `julian_castanoe@cun.edu.co` · Regla: `.cursor/rules/cun-docente.mdc` · Perfil: `config/universidades/cun.json`

**Ajustes generales → las 5 asignaturas** (Proyecto I + Creatividad + Investigación + TG2 + TG3): se aplican y regeneran en **todas**. Slides: pie = hora de inicio efectivo · `tutor_slide` genérico «Docente» · plataforma = **CDigital** (placeholder `[URL CDigital — campus del curso pendiente]`).

## Compartido
- `Plantilla_APA_CUN_Proyecto de grado.docx` (local; URL pública aún pendiente)
- **Carga académica 2026:** `config/cursos/carga_academica_2026.json` · loader: `config/cursos/carga_academica.py` · Excel: `Carga academica 2026.xlsx`
- Builds: `config/slides/build_all_course_presentations.py`, `build_sesion_material.py`, `build_pregrado_cursos.py`, `build_cun_proyecto1.py`, `build_calendar_proyecto1_54es4.py`, `build_hitos_docentes_calendar.py`, `build_acas_estudiantes.py`, `build_correo_bienvenida.py`, `sync_clases_estudiantes.py`
- Motor PPTX: `config/slides/cun_slides_engine.py` · Sesiones: `config/cursos/sesiones_cun.py`
- Agentes: `.cursor/agents/` (sync a `.claude/agents/` con `python config/sync_agents_cursor_claude.py`)

## Ciclo inicio → desarrollo → cierre (docente)
- **Especialización / AFI:** `Especializacion/0. General/LEEME - Inicio desarrollo y cierre de cursos.md` (+ instructivos en `01_`…`03_`)
- **Pregrado:** `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`
- **Checklists de cierre:** `Especializacion/Checklist…docx` · `Pregrado/Checklist…docx`
- **CSV hitos:** en cada `2026/<grupo>/` y copia en raíz del curso → `Entregas y hitos docentes - Importar a Calendar.csv` (ACA + trámites; encuentros semanales van en CSV/ICS Encuentros…)

## Convención de carpetas (cada asignatura)

```text
<Asignatura>/
  Manual del Docente…
  Calendario de clases (oficial).md
  Clases/                                    ← ÚNICA carpeta compartida con estudiantes
    LEEME - Material para estudiantes.docx
    Presentacion del Curso - ….pptx
    Recursos/ACAs/ + Plantilla APA (si aplica)
    Sesion NN - <Tema>/
      Presentacion.pptx
      (fichas .docx / apoyo estudiante)
  Guiones/                                   ← solo .md (+ Capturas/ internas)
    Sesion NN - <Tema>.md
  2026/<grupo>/                              ← oferta / Calendar / correo
    Informacion.txt, CSV/ICS, hitos, Correo de bienvenida.docx
  Correo de bienvenida.docx                  ← solo multi-grupo (copia raíz; interno)
```

| Ubicación | Contenido |
|---|---|
| Raíz de la asignatura | Manual, Calendario oficial, syllabus `.docx`, hitos CSV (+ correo si multi-grupo) |
| `Clases/` | Presentación del Curso · LEEME.docx · `Sesion NN/` · `Recursos/`. **Sin** correo ni `.md` |
| `Guiones/` | Solo `Sesion NN - ….md` + `Capturas/` (docente) |
| `2026/<grupo>/` | Informacion, roster (si aplica), encuentros CSV/ICS, hitos, Correo de bienvenida |

- **Grupos en slides:** solo portada de Presentación del Curso. En Subject de Calendar sí van códigos.
- **Subject encuentros:** `{grupos} - {Asignatura corta} - Sesion NN` (`sesiones_cun.subject_encuentro`).
- **Meet:** un enlace por curso → placeholder hasta URL real.
- **Festivo Pregrado** = clase autónoma (no cancelar).

## Horarios confirmados (2026)
| Curso | Horario | Sesiones | Cierre |
|---|---|---|---|
| Proyecto I | Lun 8:00–10:00 pm | 11 | 54ES4 → 22/11 |
| TG2 | Lun 5:00–6:00 pm | 11 | 54448 → 22/11 |
| TG3 | Mar 5:00–6:00 pm | 15 | 54450 → 15/11; 54466/54467 → 22/11 |
| Creatividad | Mié 5:00–6:00 pm | 7 | 54408 → 27/09 |
| Investigación | Jue 5:00–6:00 pm | 6 | 53339 → 20/09 |

## Especialización — Proyecto I
- Presentación: `Clases/Presentacion del Curso - Proyecto I.pptx`
- Syllabus fuente: `Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx`
- 11 sesiones en `Clases/Sesion NN - …/` + guiones homónimos `.md`
- Contenido ~60 min + tutoría ~60 min · Tutorías: `links_afi` en `cun.json`
- Grupo: `2026/54ES4/` (Calendar + Apps Script invitados)

## Pregrado
| Asignatura | Horario | Sesiones | Nota |
|---|---|---|---|
| Investigación C&T (EI005) | Jue 5–6 pm | 6 | Syllabus EI005 · U8+U10–12 en Sesión 06 · cierra 20/09 |
| Creatividad (EI004) | Mié 5–6 pm | 7 | Syllabus EI004 · cierra 27/09 · **S01 guion = modelo de calidad** |
| TG2 | Lun 5–6 pm | 11 | ⚠️ Sin syllabus SIAC — temario orientativo |
| TG3 (94532) | Mar 5–6 pm | 15 | 54450 cierra 15/11; 54466/54467 hasta 22/11 · `_combinado_*` en `2026/` para import Calendar multi-grupo |

## Guiones docentes (estándar de calidad)
- Cubren **todo el tiempo de clase** (Creatividad/Inv/TG = 60 min; Proyecto I ≈ 60 + tutoría 60).
- Minuto a minuto, texto casi literal, teórico-práctico.
- **Modelo de calidad:** `Pregrado/Creatividad y pensamiento innovador/Guiones/Sesion 01 - Introducción · Propuesta de Innovación · creatividad e inteligencia em.md`

## Regenerar
```text
python config/slides/build_cun_proyecto1.py
python config/slides/build_pregrado_cursos.py
python config/slides/build_all_course_presentations.py
python config/slides/build_calendar_proyecto1_54es4.py
python config/slides/build_hitos_docentes_calendar.py
python config/slides/build_acas_estudiantes.py
python config/slides/build_correo_bienvenida.py
python config/slides/sync_clases_estudiantes.py
python config/slides/build_sesion_material.py all all
```

## Archivo de obsoletos (limpieza 2026-08-09)

Cada asignatura puede tener `<Asignatura>/_Archivo obsoleto 2026-08-09/` (espejo de `Guiones/`, `Clases/`, `2026/<grupo>/`) con generaciones viejas de sesiones renumeradas, calendarios con fecha de inicio incorrecta y PPTX/carpetas `Temas/` redundantes. No es material vigente — no reutilizar sin verificar contra el `Calendario de clases (oficial).md` de la raíz de cada asignatura, que es el árbitro de qué tema va en cada número de sesión.

## Pendientes conocidos (no inventar)
- URLs Meet reales por curso (hoy solo placeholders)
- URL CDigital (campus) por curso
- URL pública plantilla APA
- Syllabus SIAC de TG2 ausente
- Desglose EV exacto Corte 1–3 en tablas SIAC de Creatividad/Investigación (confirmar en CDigital)
- **Fechas.txt de TG2/TG3** (por grupo, en `2026/<grupo>/`): tenían fecha de inicio 03-04/08 contradicha por el Manual/Calendario (10-11/08) — ya archivados como obsoletos
- **PLAN_VIABILIDAD_EXAMLAB.md (Proyecto I) §8/§9:** sus fechas de ACA1-3 (31/08·28/09·09/11) quedaron desalineadas tras la corrección 2026-08-09 de fechas (ver abajo) — pendiente de actualizar si se retoma el plan ExamLab

## Sesión 01 = encuadre (cambio 2026-08-09)

En **los 5 cursos** la primera sesión **no dicta tema**: presenta el curso, al Docente, a los estudiantes (Padlet) y las ACAs, más acuerdos de trabajo. El contenido curricular arranca en la **Sesión 02**.
- Título fijo: `Sesion 01 - Presentación del curso · docente · estudiantes · ACAs` (carpeta en `Clases/` y guion en `Guiones/`).
- Fuente: `config/cursos/sesiones_cun.py` → la sesión 1 lleva `presentacion: True`, `bloque: "Encuadre"` y `unidad_diferida` (la unidad del Syllabus que pasa a **lectura autónoma** y se retoma al abrir la S02 — no se elimina del Syllabus).
- Deck: `build_pptx_presentacion()` en `build_sesion_material.py`. El builder rico de tema de Creatividad S01 quedó obsoleto (archivado en `config/_Archivo obsoleto 2026-08-09/slides/`).
- Los artefactos de S01 con el título viejo están en `<Curso>/_Archivo obsoleto 2026-08-09/`.

## Decks de sesión: contenido rico por sesión

El contenido proyectable de cada sesión vive en `config/slides/content/cun_<curso>_s<NN>.json` (bloques `bullets` / `table` / `boxes`) y lo renderiza `config/slides/cun_contenido_sesion.py`. **Para enriquecer una sesión se edita ese JSON**, no el builder. Estándar: 12–16 slides dimensionadas para 2 horas, sin relleno genérico (ver `.cursor/rules/cun-docente.mdc` → «Decks de sesión»).

## Guiones enriquecidos 2026-08-09

Las 45 sesiones de los 5 cursos (menos la Sesión 01 de cada uno, que ya era el modelo) se profundizaron al estándar de calidad (fases con protagonista propio, parlamento "GUION LITERAL" completo por fase, tabla de errores/preguntas trampa, tabla de acompañamiento en el taller). El contenido vive en los scripts generadores — **editar siempre el `.py`, nunca el `.md` directamente** (se sobrescribe al regenerar):
- Proyecto I: `Especializacion/Proyecto I/Guiones/_regen_guiones_proyecto1.py` (función `guion_NN` por sesión).
- Creatividad: `Pregrado/Creatividad y pensamiento innovador/Guiones/_regen_guiones_creatividad.py` (función `guion_NN` por sesión).
- Investigación + TG2 + TG3: `config/slides/_regen_guiones_pregrado.py` (compartido). Cada sesión es un `_spec(curso, n, ...)` con kwargs nuevos `fase1_texto`…`fase5_texto` y `errores` (si no se dan, cae a un texto genérico — por eso hay que darlos siempre al añadir/editar una sesión).
- Regenerar: `python <script> [curso] [N]` (ver docstring de cada script para la sintaxis exacta; `_regen_guiones_pregrado.py all` regenera los 3 cursos de pregrado a la vez).

## Resuelto 2026-08-09
- **Fechas ACA Proyecto I:** el Manual y el Calendario oficial se corrigieron para usar la Cronograma OFICIAL de Coordinación (fuente única): ACA1 cierre **30/08** · ACA2 cierre **04/10**/nota **12/10** · ACA3 cierre **08/11**. Se retiró la tabla duplicada calculada por `fechas_entrega_aca.py` que se había desviado. También se corrigió el CSV de hitos (`Entregas y hitos docentes - Importar a Calendar.csv`, raíz y `2026/54ES4/`) — **si ya se importó una versión vieja a Google Calendar, hay que reimportarlo o corregir esos eventos a mano.** ⚠️ Los enunciados ACA (`Clases/Recursos/ACAs/*.docx`, ya entregados a los 40 estudiantes) siguen con las fechas viejas (28/09 para ACA2, etc.) — si se quiere alinear, hay que comunicárselo a los estudiantes explícitamente; no se tocó ese documento en esta limpieza.
- **Modalidad Investigación (EI005, 53339):** confirmado **virtual** (el `.docx` "_PRES" es la plantilla genérica del programa, no refleja la oferta real de este grupo).

---

## Contexto rápido (para un agente nuevo)

Workspace de material docente CUN. Cinco cursos 2026: Proyecto I (esp. IA, 54ES4) + Creatividad, Investigación, TG2 y TG3 (pregrado). Config editable en `config/cursos/carga_academica_2026.json`. Material de estudiantes solo en `Clases/`; guiones solo `.md` en `Guiones/`; oferta en `2026/<grupo>/`. Marca y motor en `cun.json` + `cun_slides_engine.py`.
