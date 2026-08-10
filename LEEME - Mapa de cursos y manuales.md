# Mapa de `Cursos/` — CUN

**Docente (interno):** Julian Andres Castaño · `julian_castanoe@cun.edu.co` · Regla: `.cursor/rules/cun-docente.mdc` · Perfil: `config/universidades/cun.json`

**Ajustes generales → las 5 asignaturas** (Proyecto I + Creatividad + Investigación + TG2 + TG3): se aplican y regeneran en **todas**. Slides: **pie vacío** (solo nº de slide); la hora de inicio efectivo va **una sola vez**, en la portada de la Presentación del Curso · `tutor_slide` genérico «Docente» · plataforma = **CDigital** (placeholder `[URL CDigital — campus del curso pendiente]`).

## Compartido
- `Plantilla_APA_CUN_Proyecto de grado.docx` — se distribuye **dentro de la carpeta del estudiante**: `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` (ruta relativa; **no** se usa URL pública). La copia a cada curso la hace `sync_clases_estudiantes.py`.
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
- **Las ACAs son TRES** (25% · 25% · 42%). La **autoevaluación (4%)** y la **coevaluación (4%)** **no son ACAs**: instrumentos individuales de cierre que el estudiante diligencia en CDigital (el Docente los habilita y registra). Solo en Proyecto I. Instructivos en `Clases/Recursos/ACAs/…instructivo.docx`; en `fechas_entrega_aca.py` van con `kind="ventana"`.
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
- **Modelo de calidad:** `Pregrado/Creatividad y pensamiento innovador/Guiones/Sesion 01 - Presentación del curso · docente · estudiantes · ACAs.md` *(la ruta anterior, `Sesion 01 - Introducción · Propuesta de Innovación · creatividad e inteligencia em.md`, dejó de existir con el renombrado del 2026-08-09; está en `_Archivo obsoleto 2026-08-09/`)*

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

> **Auditado en disco el 2026-08-10** (arranque real: TG2 hoy 5pm · Proyecto I hoy 8pm · TG3 mar · Creatividad mié · Investigación jue).
> **Nada bloquea dictar hoy:** TG2 y Proyecto I tienen deck de Sesión 01, guion completo, lectura autónoma con PDF, ACAs, plantilla APA y calendario correctos (verificado archivo por archivo).

### Bloquea la próxima clase de ese curso
- **Enlace de Meet de TG2 / TG3 / Creatividad / Investigación: no existe.** Solo Proyecto I tiene uno real (ver abajo). Sin él, el material sigue mostrando `[URL Meet — mismo enlace toda la serie · <Curso>]`. → **Docente** (crear la sala y pasar la URL).
- **URL CDigital (campus) por curso: no existe.** El placeholder `[URL CDigital — campus del curso pendiente]` es **visible para el estudiante** en las slides (p. ej. TG2 Sesión 01, slides 13 y 20; Proyecto I «RECURSOS…» slide 18). → **Docente** (URL) + regenerar.

### Meet de Proyecto I: existe pero no está propagado
La URL real `https://meet.google.com/omk-woqk-vsj` está **hardcodeada** en `config/slides/build_calendar_proyecto1_54es4.py:48` y solo llega al CSV/ICS/Apps Script de `2026/54ES4/`. **No** llega a: la Presentación del Curso (slide 18), `2026/54ES4/Informacion.txt`, el CSV de hitos ni los guiones — todos siguen con el placeholder. Falta subirla a `config/universidades/cun.json` / `sesiones_cun.py` y regenerar.

### Fechas de ACA calculadas que chocan con el temario (confirmar EV en CDigital antes de anunciarlas)
Creatividad e Investigación **no tienen desglose EV oficial**: sus ventanas salen de repartir `[inicio, recepción]` por 30/30/40 en `config/cursos/fechas_entrega_aca.py`. El resultado no cuadra con el plan de clases:
- **Investigación 53339** — ACA 1 «Fundamentos y **primer avance**» cierra el **20/08**, pero la sesión dedicada al 1.er avance es la del **27/08**. ACA 3 (marco teórico) cierra el **10/09** y la sesión que enseña marco teórico es la del **17/09**. Además la **recepción oficial es 12/09**, anterior a la última clase (17/09).
- **Creatividad 54408** — ACA 3 (Propuesta de Innovación final, 40%) cierra el **16/09**, una semana **antes** de la última clase (23/09); recepción 19/09 < última clase 23/09.
- **TG2 54448** — sin Syllabus SIAC: ACA 1 07/09 · ACA 2 05/10 · ACA 3 09/11 y los pesos 30/30/40 son orientativos (Art. 52). Coherentes entre Manual, enunciados, LEEME del estudiante y CSV de hitos, pero **no confirmados**.

### Otros pendientes vigentes
- **Syllabus SIAC de TG2 ausente** — el material lo declara abiertamente (Manual, slide 7 de la Sesión 01, enunciados de ACA).
- **Roster (listado de estudiantes y correos):** solo existe para Proyecto I `2026/54ES4/` (40 estudiantes + coanfitrión). Faltan los 6 grupos restantes (Investigación 53339 · Creatividad 54408 · TG2 54448 · TG3 54450/54466/54467) — sin ellos no se pueden generar invitaciones de Calendar con invitados para esos cursos.
- **Correo de bienvenida = plantilla mínima** en los 7 grupos: solo curso, grupo, horario y contacto. No trae fecha de la primera clase, Meet, CDigital, qué traer ni lectura autónoma, y firma «el Docente» en vez del nombre.
- **URL de la herramienta institucional antiplagio** en CDigital (TG2/TG3) — no inventar URL de terceros. TG3 tiene una sesión entera de verificación antiplagio (Sesión 11, 20/10).
- **Manuales del Docente de pregrado son stubs** (2,6–3,4 KB) frente al de Proyecto I (22,8 KB): no traen guía sesión a sesión ni procedimiento de cierre.
- **`Fechas.txt` e `Informacion.txt` de Proyecto I** (`2026/54ES4/`) siguen diciendo «Fecha de inicio: 03/08/2026», contra el `2026-08-10` de `carga_academica_2026.json` que el propio `Informacion.txt` declara como fuente. Los `Fechas.txt` equivalentes de TG2/TG3 sí se archivaron; el de Proyecto I no. Además `Informacion.txt` de Proyecto I **no lo regenera ningún build** (`build_pregrado_cursos.py:704` solo cubre pregrado).
- **Nota stale en el calendario de Investigación:** dice «Periodo corto 26P03 = 7 jueves (03/08–20/09)»; con el inicio real (13/08) son **6 jueves**, que es lo que lista la tabla.
- **Los calendarios de Creatividad y TG3 no documentan la unidad diferida** de la Sesión 01 (sí está en `sesiones_cun.py` y sí se documenta en Proyecto I e Investigación): Creatividad salta a U3 y TG3 a U3 sin explicar dónde quedaron U1–U2.
- **`fechas_entrega_aca.py` sigue sin poder reproducir el Cronograma OFICIAL de Proyecto I** (ver nota al pie del calendario de Proyecto I). Las fechas oficiales viven hoy fuera de esa API.

### Resuelto — verificado en disco el 2026-08-10, no volver a levantarlo
- ~~URL pública plantilla APA~~ → no se usa URL. El material referencia la ruta relativa `Recursos/Plantilla_APA_CUN_Proyecto de grado.docx`; **el archivo está presente en los 5 cursos**.
- ~~**Enlace/documento de la lectura autónoma** de la Sesión 01~~ → resuelto en los **5 cursos**: `Lectura autonoma - Sesion 01.txt` (escrito a mano; **ningún build lo sobrescribe**) + PDF de acceso abierto en la misma carpeta. Ver «Lectura autónoma S01» abajo.
- ~~**Los enunciados ACA de Proyecto I siguen con las fechas viejas (28/09 para ACA2)**~~ → **FALSO desde la regeneración del 2026-08-10.** Verificado extrayendo los `.docx`: ACA 1 = 03/08→30/08 · ACA 2 = 07/09→04/10 · ACA 3 = 12/10→08/11, y los tres traen la línea «Fechas OFICIALES de Coordinación (Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf)». El `LEEME - Material para estudiantes.docx` coincide. **No hay que avisarles nada a los estudiantes por este motivo.**
- ~~**Fechas.txt de TG2/TG3**~~ → archivados como obsoletos (el de Proyecto I no; ver arriba).
- **El «03/08/2026» de la slide 15 de la Presentación del Curso de Proyecto I NO es un error**: es la apertura oficial de ACA 1 según el cronograma de Coordinación.
- **Las referencias de imagen de los guiones no están rotas**: 84 referencias en los 5 cursos, 0 rotas; `Guiones/Capturas/` poblada en los 5.
- **`.cursor/agents/` y `.claude/agents/` están sincronizados**: la única diferencia es el frontmatter por plataforma, que es lo que `sync_agents_cursor_claude.py` hace a propósito.

## Sesión 01 = encuadre (cambio 2026-08-09)

En **los 5 cursos** la primera sesión **no dicta tema**: presenta el curso, al Docente, a los estudiantes (Padlet) y las ACAs, más acuerdos de trabajo. El contenido curricular arranca en la **Sesión 02**.
- Título fijo: `Sesion 01 - Presentación del curso · docente · estudiantes · ACAs` (carpeta en `Clases/` y guion en `Guiones/`).
- Fuente: `config/cursos/sesiones_cun.py` → la sesión 1 lleva `presentacion: True`, `bloque: "Encuadre"` y `unidad_diferida` (la unidad del Syllabus que pasa a **lectura autónoma** y se retoma al abrir la S02 — no se elimina del Syllabus).
- Deck: `build_pptx_presentacion()` en `build_sesion_material.py`. El builder rico de tema de Creatividad S01 quedó obsoleto (archivado en `config/_Archivo obsoleto 2026-08-09/slides/`).
- Los artefactos de S01 con el título viejo están en `<Curso>/_Archivo obsoleto 2026-08-09/`.

### Lectura autónoma S01 (resuelta 2026-08-10 · auditada)

Cada `Clases/Sesion 01 - …/` tiene un `Lectura autonoma - Sesion 01.txt` (legible por el estudiante: qué leer, para cuándo, dónde está y **qué traer a la Sesión 02**) más el PDF de acceso abierto descargado. **Regla legal aplicada:** solo acceso abierto real con licencia que permita redistribuir; la bibliografía comercial del Syllabus (Hernández-Sampieri, Creswell, Maxwell, manual APA 7) **no se distribuye** — se enlaza o se remite a Biblioteca CUN. Ningún libro comercial quedó descargado.

| Curso | Lectura obligatoria | Fuente / licencia | PDF en carpeta |
|---|---|---|---|
| Proyecto I | Cadena-Iñiguez et al. (2017), *Métodos cuantitativos, cualitativos o su combinación*, RMCA 8(7) 1603-1617 · + Montes del Castillo (2014) secs. 1-2, pp. 91-102 · + Cruz-Ortiz et al. (2020) ética (recomendada) | SciELO MX (CC BY-NC 4.0) · Universitas UPS (CC BY-NC-SA 4.0) · SciELO MX (CC BY-NC 4.0) | 3 PDF |
| Creatividad | Latorre-Cosculluela et al. (2020), *Design Thinking: creatividad y pensamiento crítico en la universidad*, REDIE 22 e28 | SciELO MX / REDIE UABC (CC BY-NC 4.0) | 1 PDF |
| Investigación C&T | Casares-Salazar et al. (2019), *Cómo organizar eficientemente un documento científico*, Ingeniería UADY 23(1) 21-35 · + Cienfuegos (2019) método científico (complementaria) | Redalyc (CC BY-NC 4.0) · RICSH (CC BY-NC 4.0) | 2 PDF |
| TG2 | Arias Castrillón (2020), *Plantear y formular un problema de investigación*, Rev. Lasallista 17(1) 301-313 | Repositorio Unilasallista (CC BY-NC-ND 2.5 CO) | 1 PDF |
| TG3 | Itriago y Zerpa (2011), *El planteamiento del problema en el proyecto de investigación en ingeniería*, Rev. Fac. Ing. UCV 26(3) 39-54 | SciELO VE / SABER-UCV (CC BY-NC-ND 4.0) | 1 PDF |

Complementarias **solo enlazadas** (licencia no permite redistribuir o no hace falta copiar): Elizondo y González Videgaray (2021) en Libros OA UNAM (TG2) · Pereira coord. (2024) en Dialnet (TG3) · Aperribai et al. (2024) en Educación XX1 / UNED (Creatividad).

**Sigue pendiente aquí:** la ficha individual del artículo de Cienfuegos en `ricsh.org.mx` devuelve **error 500** del servidor de la revista (falla también vía DOI `10.23913/ricsh.v8i15.161`); el `.txt` enlaza el PDF directo y el índice del número, que sí responden. El DOI `10.22507/rli.v17n1a4` (Arias, TG2) apunta a un host dado de baja — el `.txt` usa el enlace del repositorio, que sí funciona. Revisar ambos más adelante; no afectan al estudiante porque el PDF está en la carpeta.

> Nombres de archivo: mantenerlos **cortos**. Con la ruta de Google Drive estos `Clases/Sesion 01 - …/` ya gastan ~160 caracteres, y tres PDF superaron el límite de 260 de Windows (se acortaron el 2026-08-10). Antes de dejar un archivo aquí, verificar que la ruta completa quede por debajo de ~245.

## Decks de sesión: contenido rico por sesión

El contenido proyectable de cada sesión vive en `config/slides/content/cun_<curso>_s<NN>.json` (bloques `bullets` / `table` / `boxes`) y lo renderiza `config/slides/cun_contenido_sesion.py`. **Para enriquecer una sesión se edita ese JSON**, no el builder. Estándar: 12–16 slides dimensionadas para 2 horas, sin relleno genérico (ver `.cursor/rules/cun-docente.mdc` → «Decks de sesión»).

## Guiones enriquecidos 2026-08-09

Las 45 sesiones de los 5 cursos (menos la Sesión 01 de cada uno, que ya era el modelo) se profundizaron al estándar de calidad (fases con protagonista propio, parlamento "GUION LITERAL" completo por fase, tabla de errores/preguntas trampa, tabla de acompañamiento en el taller). El contenido vive en los scripts generadores — **editar siempre el `.py`, nunca el `.md` directamente** (se sobrescribe al regenerar):
- Proyecto I: `Especializacion/Proyecto I/Guiones/_regen_guiones_proyecto1.py` (función `guion_NN` por sesión).
- Creatividad: `Pregrado/Creatividad y pensamiento innovador/Guiones/_regen_guiones_creatividad.py` (función `guion_NN` por sesión).
- Investigación + TG2 + TG3: `config/slides/_regen_guiones_pregrado.py` (compartido). Cada sesión es un `_spec(curso, n, ...)` con kwargs nuevos `fase1_texto`…`fase5_texto` y `errores` (si no se dan, cae a un texto genérico — por eso hay que darlos siempre al añadir/editar una sesión).
- Regenerar: `python <script> [curso] [N]` (ver docstring de cada script para la sintaxis exacta; `_regen_guiones_pregrado.py all` regenera los 3 cursos de pregrado a la vez).

## Resuelto 2026-08-10
- **Auto/coevaluación de Proyecto I ya no se llaman ACA.** Eran tres ACAs desde el Syllabus ESP329, pero el material las presentaba como una cuarta y quinta ACA. Ahora: `Clases/Recursos/ACAs/Autoevaluacion individual (4%) - instructivo.docx` y `…/Coevaluacion individual (4%) - instructivo.docx` (se borraron `ACA Autoevaluacion.docx` y `ACA Coevaluacion.docx`), redactados como instructivos de un instrumento que **se diligencia** en CDigital. La tabla «LAS ACAs» de la Sesión 01 lista solo las 3 ACAs y las nombra aparte al pie. Código: `build_acas_estudiantes.py` (nuevo campo `kind` + `acas_for()`; `catalog_for_leeme()` devuelve dicts), `build_sesion_material._acas_rows()` (devuelve `(rows, instrumentos)`), `sync_clases_estudiantes.py`. Sin cambios de % ni de fechas.

## Resuelto 2026-08-09
- **Fechas ACA Proyecto I:** el Manual y el Calendario oficial se corrigieron para usar la Cronograma OFICIAL de Coordinación (fuente única): ACA1 cierre **30/08** · ACA2 cierre **04/10**/nota **12/10** · ACA3 cierre **08/11**. Se retiró la tabla duplicada calculada por `fechas_entrega_aca.py` que se había desviado. También se corrigió el CSV de hitos (`Entregas y hitos docentes - Importar a Calendar.csv`, raíz y `2026/54ES4/`) — **si ya se importó una versión vieja a Google Calendar, hay que reimportarlo o corregir esos eventos a mano.** ✅ *Actualización 2026-08-10:* los enunciados ACA (`Clases/Recursos/ACAs/*.docx`) **también quedaron con las fechas oficiales** en la regeneración del 10/08 (verificado en disco). Ya no hay desalineación que comunicar a los estudiantes.
- **Modalidad Investigación (EI005, 53339):** confirmado **virtual** (el `.docx` "_PRES" es la plantilla genérica del programa, no refleja la oferta real de este grupo).

---

## Contexto rápido (para un agente nuevo)

Workspace de material docente CUN. Cinco cursos 2026: Proyecto I (esp. IA, 54ES4) + Creatividad, Investigación, TG2 y TG3 (pregrado). Config editable en `config/cursos/carga_academica_2026.json`. Material de estudiantes solo en `Clases/`; guiones solo `.md` en `Guiones/`; oferta en `2026/<grupo>/`. Marca y motor en `cun.json` + `cun_slides_engine.py`.
