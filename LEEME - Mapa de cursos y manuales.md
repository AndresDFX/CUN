# Mapa de `Cursos/` — CUN

**Docente (interno):** Julian Andres Castaño · `julian_castanoe@cun.edu.co` · Regla: `.cursor/rules/cun-docente.mdc` · Perfil: `config/universidades/cun.json`

**Ajustes generales → las 5 asignaturas** (Proyecto I + Creatividad + Investigación + TG2 + TG3): se aplican y regeneran en **todas**. Slides: **pie vacío** (solo nº de slide); la hora de inicio efectivo va **una sola vez**, en la portada de la Presentación del Curso · `tutor_slide` genérico «Docente» · plataforma = **CDigital**, con la URL del aula resuelta por `sesiones_cun.cdigital_url(<curso>)` desde `carga_academica_2026.json` (los 5 cursos ya tienen aula real; el placeholder `[URL CDigital — campus del curso pendiente]` solo debe aparecer si el campo está vacío — nunca escrito a mano).

## Compartido

- **Publicaciones** — `Investigacion/Preprints 2026/`: los manuscritos y sus PDF, el `REGISTRO_DE_ENVIOS.md` con los números de envío y el estado, y los dictámenes de destino. Los agentes son `publicaciones-cun` (deposita) y `estado-publicaciones-cun` (solo vigila). Las herramientas de apoyo están en `config/investigacion/`: `md_a_pdf.py` porque esta máquina no tiene Word ni LibreOffice, y `preflight_pdf.py`, que rechaza un PDF con marcadores de pendiente antes de que salga.
- `Plantilla_APA_CUN_Proyecto de grado.docx` — se distribuye **dentro de la carpeta del estudiante**: `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` (ruta relativa; **no** se usa URL pública). La copia a cada curso la hace `sync_clases_estudiantes.py`.
- **Carga académica 2026:** `config/cursos/carga_academica_2026.json` · loader: `config/cursos/carga_academica.py` · Excel: `Carga academica 2026.xlsx`
- Builds: `config/slides/build_all_course_presentations.py`, `build_sesion_material.py`, `build_pregrado_cursos.py`, `build_cun_proyecto1.py`, `build_calendar_proyecto1_54es4.py`, `build_calendar_encuentros.py`, `build_apps_script_grabaciones.py`, `build_hitos_docentes_calendar.py`, `build_acas_estudiantes.py`, `build_correo_bienvenida.py`, `sync_clases_estudiantes.py`
- **Grabaciones de clase (automático):** `PRINCIPAL - Mover grabaciones de Meet.gs` + `LEEME - Mover las grabaciones de Meet.md` (esta raíz) — un solo proyecto de Apps Script, transversal a los 5 cursos, que cada 30 min saca las grabaciones de la carpeta por omisión de Meet en Mi unidad (hoy «Meet Recordings»; algunas cuentas ven «Google Meet») y las deja en la carpeta **única** de grabaciones (`carga_academica.py → GRABACIONES_URL`), cada encuentro en **su propia subcarpeta** —con el nombre buscable «periodo - grupo - asignatura - sesión», que llevan tanto la carpeta como los archivos—, de modo que el vídeo, la transcripción y el chat de una sesión van juntos. El número de sesión sale del **Calendar**: el del nombre que pone Meet viene congelado en «Sesion 01», y si el Calendar no lo confirma el archivo se mueve igual pero **suelto**, sin abrir una subcarpeta que llevaría ese número congelado. Sin credenciales. Generados por `config/slides/build_apps_script_grabaciones.py`; el `ORIGEN_ID` lo pega el Docente (no existe en el repositorio).
- **Comentar el documento de un estudiante:** `LEEME - Comentar documentos con Playwright.md` (esta raíz) — se le da el enlace del documento compartido y el curso, y deja los comentarios **anclados a la frase** en Google Docs, con el Syllabus de la asignatura y los 41 criterios de las 6 guías de ACA. Motor: `config/gdocs/comentar_docs.py` (`leer → simular → ensayar → comentar --confirmar`, más `deshacer`); sesión de Chrome en `config/gdocs/sesion_google.py`; arnés `config/gdocs/_prueba_comentar_docs.py` (42 comprobaciones, sin red). Agente: `comentar-documentos-cun`. La clave y el perfil viven en `%LOCALAPPDATA%\gdocs-cun\`, **no en el repositorio**, y el trabajo del estudiante en `_Revisiones/`, **ignorada por git**. Ruta alterna, sin navegador y sin ancla: `LEEME - Comentar documentos de estudiantes.md` (Apps Script). El por qué de las dos: `VIABILIDAD_COMENTARIOS_GOOGLE_DOCS.md`.
- Motor PPTX: `config/slides/cun_slides_engine.py` · Sesiones: `config/cursos/sesiones_cun.py`
- Agentes: `.cursor/agents/` (sync a `.claude/agents/` con `python config/sync_agents_cursor_claude.py`)

## Ciclo inicio → desarrollo → cierre (docente)
- **ALISTAMIENTO DE AULAS (OBLIGATORIO CADA SEMESTRE):** `ALISTAMIENTO_DE_AULAS_CDIGITAL.md` — procedimiento estándar completo para preparar las 7 aulas en CDigital antes del inicio de clases. **Ejecutar 1-2 días antes del inicio del semestre.** Incluye: activación de material, **depuración de lo no evaluativo** (`config/moodle/ocultar_no_evaluativo.py` — la plantilla trae foros vacíos y SCORM «Contenido N» visibles y sin nota; ver `OCULTAMIENTO_NO_EVALUATIVO_CDIGITAL.md` y `DIAGNOSTICO_FORO_1_CREATIVIDAD.md`), verificación de cuestionarios, ajuste de fechas, **destrabe de las 4 encuestas institucionales por aula** (`cdigital.py encuestas` — no las ve `fechas` porque no dan nota, y llegan abriendo en 2028/2030; ver `FECHAS_AJUSTADAS_CDIGITAL.md`) y documentación. Duración: 2-3 horas.
- **Herramienta de CDigital:** `README.md` (raíz) es la puerta de entrada · el detalle técnico, en `config/moodle/LEEME.md` · los tres scripts son `cdigital.py` (todo lo demás), `ocultar_no_evaluativo.py` (depurar la plantilla) y `revision_quiz.py` (opciones de revisión de los cuestionarios).
- **Corridas ya hechas (auditoría, no procedimiento):** `ALISTAMIENTO CDigital 2026-08-15.md` · `OCULTAMIENTO_NO_EVALUATIVO_CDIGITAL.md` · `FECHAS_AJUSTADAS_CDIGITAL.md` · `VERIFICACION_MATERIAL_VISIBLE_CDIGITAL.md` · `CONFIRMACION_MATERIAL_CORRECTO_CDIGITAL.md` · `VALIDACION_CALIDAD_PREGUNTAS_CUESTIONARIOS.md`
- **Especialización / AFI:** `Especializacion/0. General/LEEME - Inicio desarrollo y cierre de cursos.md` (+ instructivos en `01_`…`03_`)
- **Pregrado:** `Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md`
- **Checklists de cierre:** `Especializacion/Checklist…md` (+ `.docx`) · `Pregrado/Checklist…md` (+ `.docx`) — la fuente editable es el `.md`; el `.docx` se rehace desde él.
- **CSV hitos:** en cada `2026/<grupo>/` y copia en raíz del curso → `Entregas y hitos docentes - Importar a Calendar.csv` (todos los ítems del libro de calificaciones —quices, parciales, ACA Final, auto y coevaluación— + trámites; encuentros semanales van en CSV/ICS Encuentros…)

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
  Docente/                                   ← NUNCA compartida (lleva claves de respuesta)
    LEEME - Solo para el Docente.md
    Cuestionarios/<ÍTEM> - banco de preguntas.md + .xml
    Guiones/                                 ← solo .md (+ Capturas/ internas); movidos aquí el 2026-08-19
      Sesion NN - <Tema>.md
  2026/<grupo>/                              ← oferta / Calendar / correo
    Informacion.txt, CSV/ICS, hitos, Correo de bienvenida.docx
  Correo de bienvenida.docx                  ← solo multi-grupo (copia raíz; interno)
```

| Ubicación | Contenido |
|---|---|
| Raíz de la asignatura | Manual, Calendario oficial, syllabus `.docx` (falta en TG2), hitos CSV, `HERRAMIENTAS_EXAMLAB.md` (+ correo si multi-grupo) |
| `Clases/` | `Presentacion del Curso - ….pptx` · `LEEME - Material para estudiantes.docx` · `Sesion NN - …/` · `Recursos/`. **Sin** correo ni `.md` |
| `Docente/` | **No se comparte nunca.** `Cuestionarios/` = los bancos de preguntas maestros (`.xml` + su gemelo `.md`), que **llevan la respuesta correcta**. Movidos aquí desde `Clases/Recursos/Cuestionarios/` el 2026-08-18. Regla y motivo en `Docente/LEEME - Solo para el Docente.md` de cada asignatura |
| `Docente/Guiones/` | Solo `Sesion NN - ….md` + `Capturas/` (docente) |
| `2026/<grupo>/` | Informacion, roster (`Listado estudiantes (CDigital).csv` + `Correos estudiantes (invitados Calendar).txt`: ya está en los **7** grupos), encuentros CSV/ICS, hitos, Correo de bienvenida |

- **Última slide de contenido de toda deck de sesión:** `RUTA DE ENTREGABLES DEL CURSO`, penúltima, antes del cierre. La escribe `config/slides/ruta_entregables.py` y **no lleva fechas**: dice en qué punto del curso cierra cada entregable en número de sesión, con el peso y el tipo derivados del libro de calificaciones. Al cambiar el calendario del periodo se recoloca sola, así que no se reedita deck por deck.
- **El taller de cada sesión sale de `config/slides/talleres.py`, no del JSON.** El JSON de la sesión solo lleva el marcador `{"type": "taller"}` en el lugar exacto donde va, y `cun_contenido_sesion.load()` lo expande a **dos slides canónicas**: «TALLER · \<producto\>» (qué queda al final · los pasos numerados · qué es innegociable si el tiempo aprieta) y «TALLER · cómo se revisa y dónde se entrega» (criterios verificables · Plan B · el destino real). Tres reglas, cada una nacida de un defecto que ya estaba proyectado: **(1) ningún minuto absoluto** en la deck —`guion_evaluacion.py` recorta las fases largas los días con quiz, así que toda cifra fija acaba mintiendo; el reloj vive en el guion, y solo sobrevive en la deck la duración de un producto oral declarada en `cronometro=`—; **(2) el destino se deriva de `ruta_entregables`**, nunca se escribe a mano: sale como entrega real solo la semana en que cierra una tarea del libro de calificaciones (6 de 45), y en las demás dice que el avance se guarda en el Drive y a qué ítem alimenta; **(3) máximo 8 bullets por slide**, porque a los 9 el motor parte la slide en una «(cont.)» sin encabezado. Comprobación: `python config/slides/talleres.py --verificar` · `_prueba_talleres_pptx.py` (contrato en los `.pptx` reales) · `_alineacion_guion_taller.py` (que el guion no contradiga a la deck). Migrar un taller nuevo del JSON al módulo: `aplicar_talleres.py` (`--simular` por defecto).
- **Grupos en slides:** solo portada de Presentación del Curso. En Subject de Calendar sí van códigos.
- **Subject encuentros:** `{grupos} - {Asignatura corta} - Sesion NN` (`sesiones_cun.subject_encuentro`).
- **Meet:** un enlace por curso, en `carga_academica_2026.json → cursos.<key>.meet` (fuente única; **no** hardcodear en builds) → placeholder hasta URL real. Hoy solo Proyecto I la tiene.
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
- **Estructura del aula (CDigital, auditoría 2026-08-10):** corte 1 = **Quiz 25%** · corte 2 = **ACA 1 25%** · corte 3 = **ACA FINAL 42% + autoevaluación 4% (cuestionario) + coevaluación 4% (foro)**. Los enunciados del estudiante **ya se realinearon** (2026-08-10): `Clases/Recursos/ACAs/` tiene `Quiz (25%) - guia del cuestionario.docx`, `ACA 1 (25%) - Formulacion del problema y fundamentacion referencial.docx`, `ACA FINAL (42%) - Anteproyecto integrado.docx` y los dos instructivos. Catálogo en `build_acas_estudiantes.py`. **Ojo con el nombre:** en disco es «guia», **sin tilde** (lo escribe así `build_acas_estudiantes.py`); citarlo con tilde deja una ruta colgada.
- La **autoevaluación** y la **coevaluación** **no son ACAs** (instrumentos individuales de cierre que el estudiante diligencia/participa en CDigital) y **no son exclusivas de Proyecto I**: existen en los 5 cursos, con otro peso. Instructivos en `Clases/Recursos/ACAs/…instructivo.docx`; en `fechas_entrega_aca.py` son los ids `auto` y `coev`.
- 11 sesiones en `Clases/Sesion NN - …/` + guiones homónimos `.md`
- Contenido ~60 min + tutoría ~60 min · Tutorías: `links_afi` en `cun.json`
- Grupo: `2026/54ES4/` (Calendar + Apps Script invitados)

## Pregrado
| Asignatura | Horario | Sesiones | Nota |
|---|---|---|---|
| Investigación C&T (EI005) | Jue 5–6 pm | 6 | Syllabus EI005 · cierra 20/09 · **temario adelantado 2026-08-11**: U6+U8 en S04 · U7+U10–12 en S05 · S06 = cierre sin evaluar |
| Creatividad (EI004) | Mié 5–6 pm | 7 | Syllabus EI004 · cierra 27/09 · **temario adelantado 2026-08-11**: U6+U7 en S05 · U8 en S06 · S07 = cierre sin evaluar · **S01 guion = modelo de calidad** |
| TG2 | Lun 5–6 pm | 11 | ⚠️ Sin syllabus SIAC — temario orientativo |
| TG3 (94532) | Mar 5–6 pm | 15 | 54450 cierra 15/11; 54466/54467 hasta 22/11 · encuentros = **una sola serie** para los tres grupos en `2026/_combinado_todos/` (un `.gs`, una sala de Meet) |

## Guiones docentes (estándar de calidad)
- Cubren **todo el tiempo de clase** (Creatividad/Inv/TG = 60 min; Proyecto I ≈ 60 + tutoría 60).
- Minuto a minuto, texto casi literal, teórico-práctico.
- **Modelo de calidad:** `Pregrado/Creatividad y pensamiento innovador/Docente/Guiones/Sesion 01 - Presentación del curso · docente · estudiantes · ACAs.md` *(la versión anterior dejó de existir con el renombrado del 2026-08-09; está archivada como `_Archivo obsoleto 2026-08-09/Docente/Guiones/Sesion 01 - Introducción · Propuesta de Innovación (trabajo final).md` — la ruta que citaba antes este LEEME, «… creatividad e inteligencia em.md», no existe ni siquiera en el archivo)*

## Regenerar

**Orden ejecutable completo** (verificado leyendo cada build el 2026-08-11). Todo sale de tres fuentes que **no** se generan: `carga_academica_2026.json` (oferta), `sesiones_cun.py` (sesiones y temas) y `fechas_entrega_aca.py` (ítems, pesos y ventanas).

```text
python config/cursos/sync_manuales_fechas.py           # 1. Manuales de pregrado: sección 3 (Evaluación) + tabla de fechas
python config/slides/build_all_course_presentations.py # 2. Presentaciones del Curso de los 5 + calendarios oficiales + Informacion.txt/Fechas.txt + CSV/ICS de encuentros
python config/slides/build_calendar_encuentros.py      # 3. .gs de encuentros CON invitados de los otros 4 cursos (TG3 = un solo .gs en 2026/_combinado_todos/)
python config/slides/build_apps_script_grabaciones.py  # 3b. .gs + runbook para mover las grabaciones de Meet (lee salas y horarios; el ORIGEN_ID lo pega el Docente)
python config/slides/build_hitos_docentes_calendar.py  # 4. «Entregas y hitos docentes - Importar a Calendar.csv» (raíz del curso + 2026/<grupo>/)
python config/slides/build_sesion_material.py all all  # 5. Decks de sesión + guiones .md (invoca solo él los tres _regen_guiones_*)
python config/slides/build_acas_estudiantes.py         # 6. Clases/Recursos/ACAs/ — un .docx por ítem del aula
python config/slides/build_rompehielos_slido.py        # 7. Rompehielos del Docente en 2026/<grupo>/ (solo cursos de +20; Investigación se salta)
python config/slides/build_correo_bienvenida.py        # 8. Correo de bienvenida.docx en 2026/<grupo>/ (nunca en Clases/)
python config/slides/sync_clases_estudiantes.py        # 9. SIEMPRE al final — consolida Clases/ (ver por qué, abajo)
```

Por qué ese orden, y no el que había antes:

- **El paso 2 es un envoltorio**, no un build más: `build_all_course_presentations.main()` ejecuta por dentro `build_cun_proyecto1.py`, `build_pregrado_cursos.py` y `build_calendar_proyecto1_54es4.py` (líneas 145–147). Correrlos aparte **antes** —como hacía la lista anterior— solo duplica trabajo. *(Ojo si alguna vez se llama a la función `build_proyecto1()` de ese módulo a mano: es un deck compacto de respaldo, sigue rotulando «ACA1 / ACA2 / ACA3» y **pisaría** el deck rico de `build_cun_proyecto1.py`. `main()` no la usa.)*
- **`build_sesion_material.py` va antes que `sync_clases_estudiantes.py`.** El primero crea, renombra y **borra** carpetas `Clases/Sesion NN - …/` huérfanas (`generate_course`, líneas 740–742); el segundo escribe dentro de esas carpetas buscándolas por nombre en disco (la ficha de taller de Creatividad S01, `sync_clases_estudiantes.py:264–287`). Al revés, un cambio de título de sesión se lleva por delante la ficha recién escrita.
- **Los guiones no llevan comando propio en esta lista a propósito:** `build_sesion_material.py` invoca `_run_rich_guion_regen()` (línea 730), que lanza `_regen_guiones_proyecto1.py`, `_regen_guiones_creatividad.py` y `_regen_guiones_pregrado.py` según el curso. Para editar el contenido de un guion sigue siendo obligatorio tocar esos `.py` (ver «Guiones enriquecidos»).

Atajos (no sustituyen a la lista, sirven para iterar rápido):

```text
python config/slides/build_pregrado_cursos.py --calendar-only   # solo los 5 «Calendario de clases (oficial).md» + CSV/ICS
python config/slides/build_pregrado_cursos.py --proyecto1-only  # solo el calendario oficial de Proyecto I
python config/slides/build_sesion_material.py creatividad 5     # una sola sesión (deck + guion)
python config/slides/build_sesion_material.py all all --guion-only
python config/cursos/sync_manuales_fechas.py creatividad        # un solo manual
python config/sync_agents_cursor_claude.py                      # .cursor/agents → .claude/agents (no es material de curso)
```

## Archivo de obsoletos (limpieza 2026-08-09)

Cada asignatura puede tener `<Asignatura>/_Archivo obsoleto 2026-08-09/` (espejo de `Docente/Guiones/`, `Clases/`, `2026/<grupo>/`) con generaciones viejas de sesiones renumeradas, calendarios con fecha de inicio incorrecta y PPTX/carpetas `Temas/` redundantes. No es material vigente — no reutilizar sin verificar contra el `Calendario de clases (oficial).md` de la raíz de cada asignatura, que es el árbitro de qué tema va en cada número de sesión.

## Pendientes conocidos (no inventar)

> **Reauditado en disco el 2026-08-11** contra el modelo (`fechas_entrega_aca.py`, `sesiones_cun.py`, `carga_academica_2026.json`) y contra los artefactos reales (`.md`, `.docx`, `.pptx`, `.csv`). Fechas de arranque: **10/08** TG2 (lun 5pm) y Proyecto I (lun 8pm) · **11/08** TG3 (mar) · **12/08** Creatividad (mié) · **13/08** Investigación (jue). Las cinco Sesión 01 tienen deck, guion, lectura autónoma con PDF, ACAs, plantilla APA y calendario correctos.
> **Regla de este archivo:** cada afirmación con dato duro va contrastada contra el modelo o contra disco. Lo que no se pueda comprobar se borra o se marca **PENDIENTE DE VERIFICAR**; no se deja escrito «verificado» sin la comprobación al lado.

### Bloquea la próxima clase de ese curso
- **Enlace de Meet de TG2 / TG3 / Creatividad / Investigación: no existe.** Confirmado: `carga_academica_2026.json` tiene `"meet": ""` en los cuatro y `sesiones_cun.meet_url()` devuelve `[URL Meet — mismo enlace toda la serie · <Curso>]`. Solo Proyecto I tiene sala real. → **Docente** (crear la sala y pasar la URL a `carga_academica_2026.json → cursos.<key>.meet`, que es la fuente única) + regenerar.

### CDigital: la URL **sí existe** en los 5 cursos — lo que falta es propagarla
Corregido el 2026-08-11: la afirmación anterior («URL CDigital por curso: no existe») era **falsa**. Las aulas están en `carga_academica_2026.json` y las resuelve `sesiones_cun.cdigital_url(<curso>)`: Proyecto I `…id=130378` · Creatividad `…id=115463` · Investigación `…id=111070` · TG2 `…id=129268` · TG3 `…id=112321` (+ `116387` y `129270` por grupo). Las 5 **Presentaciones del Curso** ya muestran la URL real. El placeholder sobrevive solo donde está **escrito a mano en vez de resolverse**, y ahí sí hay trabajo:

- **3 JSON de contenido de Sesión 01 traen el placeholder como texto literal** → sale impreso en el deck del estudiante: `content/cun_investigacion_s01.json:141` (deck slide 11) · `content/cun_tg2_s01.json:198` (slide 13) · `content/cun_tg3_s01.json:199` (slide 12). También `content/cun_creatividad_s02.json:237`. Regenerar **no** lo arregla: hay que editar el JSON para que el texto no incluya la URL, o resolverla en el render. *(La lista anterior decía «TG2 Sesión 01, slides 13 y 20»: el deck de TG2 S01 tiene 23 slides y solo la **13** lo trae; y decía «Proyecto I RECURSOS slide 18», que hoy muestra la URL real.)*
- **`build_hitos_docentes_calendar.py` hardcodea el placeholder** (`CDIGITAL_PH`, línea 36, usado en 8 sitios) en vez de llamar a `cdigital_url()`. Por eso los CSV de hitos de los 7 grupos siguen diciendo «CDigital: [URL CDigital — campus del curso pendiente]».

### Meet de Proyecto I: ya está propagado
Corregido el 2026-08-11 — la nota anterior era **falsa en los tres puntos**. La URL `https://meet.google.com/omk-woqk-vsj` **no** está hardcodeada en `build_calendar_proyecto1_54es4.py`: vive en `carga_academica_2026.json:87` (`cursos.proyecto1.meet`), la lee `sesiones_cun.meet_url()` y el build la toma de ahí (`LOCATION`, línea 55, con el comentario «FUENTE ÚNICA»). Y sí llega a la **Presentación del Curso** (slide 18, verificado extrayendo el `.pptx`), al `Calendario de clases (oficial).md` (línea 10), a `2026/54ES4/Informacion.txt`, a `Fechas.txt` y al **CSV de hitos** (raíz y `2026/54ES4/`). No queda nada por propagar aquí.

### Modelo de evaluación y fechas — rehecho 2026-08-10 contra el aula (CDigital)

**Fuente única:** el libro de calificaciones de cada aula (auditoría `AUDITORIA CDigital 2026-08-10.md` §2), cargado en `config/cursos/fechas_entrega_aca.py` → `ACA_COMPONENTES` (ítem, tipo, peso, corte) + `VENTANAS` / `VENTANAS_POR_GRUPO` (apertura, cierre, límite de nota). **Nada se recalcula por pesos**; los pesos suman 100 por curso y el módulo lo verifica al importarse.

Queda **anulada** la regla anterior «cada ACA evalúa el 100% de su corte»: hay quices y parciales (Parcial 1 = 24% por sí solo), en pregrado existe **una sola «ACA Final»** (Tarea) y auto/coevaluación existen en los 5 cursos (la coevaluación es un **foro**).

Pregrado = **30 / 30 / 40** (Art. 52). **Proyecto I = 25 / 25 / 50** (estructura propia; nota única Art. 41 operada en tres cortes).

| Curso | Corte 1 | Corte 2 | Corte 3 |
|---|---|---|---|
| Investigación 53339 | Quiz 1 6% → 20/08 · Parcial 1 24% → 27/08 | Quiz 2 9% → 03/09 · Parcial 2 21% → 10/09 | ACA Final 32,8% → **12/09** (recepción) · Quiz 3 4% → **12/09** · Auto 1,6% y Coev 1,6% → 20/09 |
| Creatividad 54408 | Quiz 1 6% → 19/08 · Parcial 1 24% → 26/08 | Quiz 2 9% → 02/09 · Parcial 2 21% → 09/09 | Quiz 3 4% → 16/09 · ACA Final 32,8% → **19/09** (recepción) · Auto 1,6% y Coev 1,6% → 27/09 |
| TG2 54448 | Quiz 1 6% → 31/08 · Parcial 1 24% → 14/09 | Quiz 2 9% → 28/09 · Parcial 2 21% → 05/10 | Quiz 3 4% → 26/10 · ACA Final 32,8% → **14/11** (recepción) · Auto 1,6% y Coev 1,6% → 22/11 |
| TG3 54450 / 54466 / 54467 | Quiz 1 6% → 25/08 · Parcial 1 24% → 15/09 | Quiz 2 9% → 29/09 · Parcial 2 21% → 13/10 | Quiz 3 4% → 27/10 · ACA Final 32% → **07/11** (54450) / **14/11** (54466-67) · Auto 2% y Coev 2% → **10/11** (54450, S14) / **17/11** (54466-67, S15) — límite de nota 15/11 y 22/11 |
| Proyecto I 54ES4 *(25/25/50)* | Quiz 25% → 30/08 | ACA 1 25% → 04/10 | ACA FINAL 42% → 08/11 · Coev 4% (foro) → 15/11 · Auto 4% → 22/11 |

Criterio de las ventanas (decisión del docente, no recalcular): la recepción de **trabajos** limita solo la ACA Final (documento); los quices y parciales son cuestionarios y cierran **en día de clase** con la ventana abierta desde la sesión anterior; la Sesión 01 es de encuadre y no evalúa; auto/coevaluación van de la última semana al cierre de notas; **Proyecto I** conserva las fechas OFICIALES de Coordinación. En **TG3** auto y coevaluación cierran **el día de la última clase de cada grupo** (10/11 en el 54450 · 17/11 en el 54466/54467), no en el cierre de notas: la coevaluación es un **foro** y calificarla el mismo domingo del cierre no dejaba margen.

**Dónde se lee cada cosa (todo generado desde el módulo, nada escrito a mano):**

| Pregunta | Archivo | Regenerar |
|---|---|---|
| ¿Qué ítems tiene el aula y cuánto pesan? | `<Curso>/Manual del Docente…` → «3. Evaluación — estructura REAL del aula» | `python config/cursos/sync_manuales_fechas.py` |
| ¿Cuándo abre / cierra cada ítem y hasta cuándo hay para la nota? | mismo Manual → «Fechas de entrega ACA / cortes» | ídem |
| **¿En qué sesión cae cada quiz y cada parcial?** | `<Curso>/Calendario de clases (oficial).md` → columna «Evaluación (aula CDigital)» + bloque «Evaluación en el aula» | `python config/slides/build_pregrado_cursos.py --calendar-only` |
| ¿Qué ve el estudiante? | `Clases/Recursos/ACAs/*.docx` (ventana + tipo + peso del ítem real) | `python config/slides/build_acas_estudiantes.py` |
| ¿Qué va a mi Calendar? | `Entregas y hitos docentes - Importar a Calendar.csv` | `python config/slides/build_hitos_docentes_calendar.py` |

En Proyecto I el `Calendario de clases (oficial).md` **ya no se cura a mano**: desde 2026-08-11 lo genera `build_pregrado_cursos.py` (`write_calendario_proyecto1`, mismas tres fuentes que los de pregrado) y por eso lleva el aviso «Archivo generado — no editar a mano»; se rehace con `--calendar-only` o `--proyecto1-only`. Rotula los ítems **con el nombre del aula** (Quiz · ACA 1 · ACA FINAL); el puente muerto con la numeración del Syllabus (ACA 1→Quiz · ACA 2→ACA 1 · ACA 3→ACA FINAL) solo sobrevive en el **Manual del Docente**, que sí sigue curado a mano. Ningún ítem de Proyecto I cierra en día de clase (Coordinación cierra en domingo; la clase es lunes), así que su calendario marca la **última sesión sincrónica antes de cada cierre** en vez de «la sesión en que cae».

> **La última clase cae después del entregable final** en Creatividad e Investigación (ACA Final 19/09 < S07 23/09; ACA Final 12/09 < S06 17/09). **Ninguna fecha se movió por esto**: lo que se movió fue el **temario**.
>
> El problema real era otro y estaba en el contenido, no en el calendario: lo que la ACA Final **califica** se dictaba **después** de que la ACA Final cerraba. **Corregido el 2026-08-11 adelantando el temario** (reorden, no recorte — ninguna unidad se elimina). Estado definitivo, ya en `sesiones_cun.py` y en los JSON de `config/slides/content/`:
>
> | Curso | Sesión | Fecha | Título vigente | Unidades |
> |---|---|---|---|---|
> | Creatividad | **S05** | 09/09 | Validación de la propuesta · vigilancia tecnológica | U6+U7 (sesión doble) |
> | Creatividad | **S06** | 16/09 | Innovación local–internacional · entidades de apoyo | U8 |
> | Creatividad | **S07** | 23/09 | Taller de consolidación y sustentación de la propuesta | Cierre · no evalúa |
> | Investigación | **S04** | 03/09 | Problema y pregunta · bases de datos y gestores de citas | U6+U8 (sesión doble) |
> | Investigación | **S05** | 10/09 | Planteamiento del problema · marco teórico y revisión de literatura | U7+U10–12 (sesión doble) |
> | Investigación | **S06** | 17/09 | Socialización del artículo y cierre del curso | Cierre · no evalúa |
>
> Cualquier texto del repo que todavía diga que ese contenido «cae después del cierre» o «no entra» es **falso**: hay que corregirlo, no conservarlo. Lo que sigue siendo cierto es que la **última clase de esos dos cursos no evalúa** — es socialización y cierre, con auto y coevaluación abriéndose ese mismo día.
>
> Antes decía aquí que era «un límite estructural, no corregible moviendo fechas». **Es falso** y conviene saberlo: la recepción **no es institucional**. `config/cursos/carga_academica_2026.json` declara que «recepcion no viene en el Excel» y que se derivó como ~8 días antes del cierre de notas. Lo único institucional es el inicio del periodo y el cierre de notas, así que la recepción sí se puede mover.
>
> Por eso, en **Investigación**, el Quiz 3 se adelantó del 17/09 al **12/09** (decisión del Docente, 10/08/2026): todo el corte 3 cierra el mismo día y la S06 queda limpia para el cierre.

- **TG2 54448** — sigue sin Syllabus SIAC, pero los pesos **ya no son orientativos**: salen del libro de calificaciones del aula (30/30/40 con el mismo desglose de los otros cursos de pregrado).
- ~~**Pendiente de material (auditoría §5.1):** los decks y guiones siguen escritos como ACA 1/2/3 (y EV05/EXAM en TG3)~~ → **FALSO desde el 2026-08-11.** Barrido con `rg` sobre los 55 `.pptx` vigentes de `Clases/`, los 52 guiones `.md` y los JSON de `config/slides/content/`: **cero** decks de sesión y **cero** JSON de contenido con esa numeración. Las únicas apariciones son deliberadas y dicen «esto queda anulado»: slide 17 de la Presentación del Curso de Proyecto I (tabla puente Syllabus ↔ aula), los 4 Manuales de pregrado (bloque «Qué desmiente esto») y los guiones de TG3 S01 y S12 (que explican que TG3 **no** es corte único EV05/EXAM). La otra mitad de la frase —«los quices y parciales no existen como actividad en el aula»— también quedó **desmentida el 2026-08-15**: sí existen, y con banco de preguntas. Ver el pendiente correspondiente más abajo.

### Otros pendientes vigentes
- **Syllabus SIAC de TG2 ausente** — el material lo declara abiertamente (Manual, slide 7 de la Sesión 01, enunciados de ACA).
- ~~**Roster:** solo existe para Proyecto I `2026/54ES4/`; faltan los 6 grupos restantes~~ → **FALSO desde el 2026-08-11.** Los **7 grupos** tienen `Listado estudiantes (CDigital).csv` + `Correos estudiantes (invitados Calendar).txt`. Correos únicos por grupo: 54ES4 **52** (incluye coanfitrión y Docente) · 54408 **50** · 53339 **20** · 54448 **50** · 54450 **13** · 54466 **49** · 54467 **50**. El `.gs` de encuentros con invitados ya está generado en Creatividad, Investigación y TG2 (`2026/<grupo>/Crear encuentros con invitados.gs`) y en TG3 como uno solo para los tres grupos (`2026/_combinado_todos/PRINCIPAL - Crear encuentros con invitados (3 grupos).gs`). Lo único que falta para invitar es el **Meet** de esos 4 cursos (ver arriba).
- ~~**Correo de bienvenida = plantilla mínima** en los 7 grupos~~ → **FALSO desde el 2026-08-11.** El `.docx` trae tabla completa: curso, grupo, horario **con hora de inicio efectivo**, primera clase con fecha y aviso de que la S01 es encuadre, **Meet** (real en Proyecto I, placeholder en los otros 4 porque la sala no existe), **aula CDigital con URL real**, cierre del grupo, qué hacer antes de la Sesión 02 (lectura autónoma) y, en pregrado, la regla de festivo = clase autónoma. **Lo que sigue pendiente es solo la firma:** cierra con «el Docente · julian_castanoe@cun.edu.co» en vez del nombre propio.
- **URL de la herramienta institucional antiplagio** en CDigital (TG2/TG3) — no inventar URL de terceros. TG3 tiene una sesión entera de verificación antiplagio (Sesión 11, 20/10).
- **Manuales del Docente de pregrado siguen siendo cortos** (6,5–8,0 KB tras la sección de evaluación generada; medido el 2026-08-11) frente al de Proyecto I (**28 KB**): ya traen estructura de evaluación, ítems del aula y fechas, pero **no** guía sesión a sesión ni procedimiento de cierre.
- ~~**Los quices y parciales no existen como actividad en el aula** — solo como ítem del libro de calificaciones. Hay que crearlos (cuestionario + banco de preguntas)~~ → **FALSO desde el 2026-08-15.** El censo contra CDigital encontró que los **31 cuestionarios evaluativos ya existen** como actividad en las 7 aulas (los trae la plantilla institucional), con **0 intentos** todos. El problema real era el contrario y peor: **26 de los 31 estaban vacíos —0 preguntas, puntuación 0,00— y aun así visibles y abiertos** para los estudiantes; los otros 5 (Creatividad) servían 10 preguntas de plantilla. Eso ya está corregido: los 31 sirven **10 preguntas concretas** cada uno y quedaron **ocultos**, pendientes de que el Docente los active (ver «Alistamiento del aula» en `config/moodle/LEEME.md`). El maestro de las preguntas es el `.xml` de cada curso en `Docente/Cuestionarios/`. **Inventario para revisar y activar, con los 59 cmid: `ALISTAMIENTO CDigital 2026-08-15.md`** — ahí están también las 28 carpetas de material (167 archivos), igual de ocultas, y las decisiones que tomó la herramienta sola.
- ~~Auto/coevaluación de pregrado sin instructivo~~ → **resuelto 2026-08-10**: los 4 cursos ya tienen `Autoevaluacion individual (…) - instructivo.docx` y `Coevaluacion individual (…) - instructivo.docx`.
- ~~**`Fechas.txt` e `Informacion.txt` de Proyecto I siguen diciendo «Fecha de inicio: 03/08/2026»** y no los regenera ningún build~~ → **FALSO desde el 2026-08-11.** Los dos dicen **«Fecha de inicio: 10/08/2026»**, igual que `carga_academica_2026.json`, y los dos **sí** los regenera `build_calendar_proyecto1_54es4.py` (función en la línea 184, bucle `for nombre in ("Fechas.txt", "Informacion.txt")` en la 197) — el propio archivo lo dice. La cita `build_pregrado_cursos.py:704` era además una referencia equivocada: esa línea es una cadena de la sección de evaluación de TG2; el `Informacion.txt` de pregrado se escribe en la **1569**.
- ~~**Nota stale en el calendario de Investigación** («7 jueves 03/08–20/09»)~~ → **FALSO desde el 2026-08-11.** La nota vigente (línea 10 de ese calendario, generada desde `sesiones_cun.py → nota_syllabus`) ya dice: «el rango institucional tiene 7 jueves calendario (06/08–17/09), pero el inicio operativo del semestre es el 10/08, así que se dictan **6** (13/08–17/09) y el periodo cierra el 20/09» — que es exactamente lo que lista la tabla.
- ~~**Los calendarios de Creatividad y TG3 no documentan la unidad diferida** de la Sesión 01~~ → **FALSO desde el 2026-08-11.** Los **cinco** calendarios traen la fila `| — | — | (misma semana) | ⚠️ Lectura autónoma | <unidad diferida> | — |` justo debajo de la Sesión 01, con el texto de `sesiones_cun.py → unidad_diferida`. Verificado en Creatividad (línea 20: U1–U2 Propuesta de Innovación · creatividad e inteligencia emocional) y TG3 (línea 25: U1–U2 Casos de éxito · retomar proyecto · contexto y planteamiento).
- **Los decks de Sesión 01 mandan al estudiante a leer la hora en un pie que está vacío.** Regla vigente: pie = solo el nº de slide, y la hora de inicio efectivo va **una sola vez**, en la portada de la Presentación del Curso. Pero tres JSON de contenido dicen «Se empieza a la hora que indica el **pie de estas diapositivas**»: `content/cun_investigacion_s01.json:253` · `content/cun_tg2_s01.json:310` · `content/cun_tg3_s01.json:312`. Verificado extrayendo el pie del `.pptx`: solo contiene el número. Hay que reescribir esa frase en los tres JSON (la hora sí está en el `Correo de bienvenida.docx` y en la portada de la Presentación del Curso).
- ~~`fechas_entrega_aca.py` no reproduce el Cronograma OFICIAL de Proyecto I~~ → **resuelto 2026-08-10:** ese cronograma ES la tabla `VENTANAS["proyecto1"]` del módulo (ya no hay cálculo del que desviarse), mapeado a los ítems reales del aula (Quiz · ACA 1 · ACA FINAL · coev · auto).

### Resuelto — reverificado en disco el 2026-08-11, no volver a levantarlo
- ~~URL pública plantilla APA~~ → no se usa URL. El material referencia la ruta relativa `Recursos/Plantilla_APA_CUN_Proyecto de grado.docx`; **el archivo está presente en los 5 cursos**.
- ~~**Enlace/documento de la lectura autónoma** de la Sesión 01~~ → resuelto en los **5 cursos**: `Lectura autonoma - Sesion 01.txt` (escrito a mano; **ningún build lo sobrescribe**) + PDF de acceso abierto en la misma carpeta. Verificado listando las 5 carpetas `Clases/Sesion 01 - …/`: Proyecto I 3 PDF · Creatividad 1 · Investigación 2 · TG2 1 · TG3 1. Ver «Lectura autónoma S01» abajo.
- ~~**Un `.docx` por ítem del aula**~~ → los 5 cursos tienen su `Clases/Recursos/ACAs/` completo (verificado listando disco el 2026-08-11): pregrado con 8 documentos cada uno (Quiz 1/2/3, Parcial 1/2, ACA Final, instructivo de auto y de coevaluación) y Proyecto I con 5 (Quiz, ACA 1, ACA FINAL, instructivo de auto y de coevaluación). El nombre de las guías es `… - guia del cuestionario.docx`, **sin tilde**.
- ~~**Los enunciados ACA de Proyecto I siguen con las fechas viejas (28/09 para ACA2)**~~ → **FALSO desde la regeneración del 2026-08-10.** Verificado extrayendo los `.docx` (reverificado 2026-08-11): los enunciados **ya no se llaman ACA 1/2/3** sino como el aula — `Quiz (25%) - guia del cuestionario.docx` = 03/08→30/08 · `ACA 1 (25%) - Formulacion del problema y fundamentacion referencial.docx` = 07/09→04/10 · `ACA FINAL (42%) - Anteproyecto integrado.docx` = 12/10→08/11 · `Coevaluacion individual (4%)` = 09/11→15/11 · `Autoevaluacion individual (4%)` = 16/11→22/11. Los cinco traen la línea «Fechas OFICIALES de Coordinación (Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf)». El `LEEME - Material para estudiantes.docx` coincide. **No hay que avisarles nada a los estudiantes por este motivo.**
- ~~**Fechas.txt de TG2/TG3**~~ → archivados como obsoletos (el de Proyecto I no; ver arriba).
- **El «03/08/2026» de la slide 15 de la Presentación del Curso de Proyecto I NO es un error**, pero **no es la apertura de la ACA 1**: la slide 15 es «CRONOGRAMA — VENTANAS DE ENTREGA» y ese 03/08 es el **INICIO del Corte 1**, cuyo único ítem es el **Quiz** (cuestionario, 25%), que cierra el 30/08. La **ACA 1** (tarea, 25%, corte 2) abre el **07/09** y cierra el 04/10. Contrastado con `fechas_entrega_aca.py` → `VENTANAS["proyecto1"]` (`quiz` = 03/08 → 30/08 → nota 07/09; `aca1` = 07/09 → 04/10 → nota 12/10), con la tabla del `Calendario de clases (oficial).md` de Proyecto I y con el texto real de la slide 15 extraído del `.pptx`. *(Corregido el 2026-08-11; la redacción anterior decía «apertura oficial de ACA 1» y era falsa.)*
- **Las referencias de imagen de los guiones no están rotas**: reverificado 2026-08-11 sobre los 52 guiones `.md` vigentes → **84 referencias, 0 rotas**. `Docente/Guiones/Capturas/` poblada en los 5 (Proyecto I 9 · TG2 9 · TG3 9 · Creatividad 20 · Investigación 15). *(Si al recontar te salen «26 rotas», el barrido está mal hecho: los nombres llevan espacios y un `split` por espacio parte la ruta. Hay que resolver la ruta completa relativa a la carpeta del guion.)*
- **`.cursor/agents/` y `.claude/agents/` están sincronizados**: reverificado 2026-08-11 — mismos 3 archivos (`cun-dudas-material.md`, `disenador-curricular-cun.md`, `examlab-practica.md`) y la única diferencia es el frontmatter por plataforma (`model:` / `tools:`), que es lo que `config/sync_agents_cursor_claude.py` hace a propósito.
- **El modelo de evaluación del LEEME cuadra ítem por ítem con `fechas_entrega_aca.py`**: reverificados el 2026-08-11 los **37 ítems** de la tabla de cortes de más arriba (8 en cada curso de pregrado + 5 en Proyecto I, con las tres variantes de grupo de TG3) contra `entregas_curso()`. Cero discrepancias en ítem, tipo, peso, corte, cierre ni límite de nota.

## Sesión 01 = encuadre (cambio 2026-08-09)

En **los 5 cursos** la primera sesión **no dicta tema**: presenta el curso, al Docente, a los estudiantes y las ACAs, más acuerdos de trabajo. El rompehielos depende del tamaño: muro de Padlet hasta 20 estudiantes (solo Investigación), y por encima el juego «dos verdades y una mentira» en Slido — un muro de 50 o 112 notas no lo lee nadie. El contenido curricular arranca en la **Sesión 02**.
- Título fijo: `Sesion 01 - Presentación del curso · docente · estudiantes · ACAs` (carpeta en `Clases/` y guion en `Docente/Guiones/`).
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

> Nombres de archivo: mantenerlos **cortos**. Medido el 2026-08-11: la carpeta `…/Clases/Sesion 01 - Presentación del curso · docente · estudiantes · ACAs\` ya gasta **156 caracteres** con la ruta de Google Drive, y el archivo más largo del repo va en **236** (`Lectura complementaria - Metodo cientifico y sus etapas (Cienfuegos 2019).pdf`, Investigación) — a 24 del límite de 260 de Windows. Tres PDF lo superaron y se acortaron el 2026-08-10. Antes de dejar un archivo aquí, verificar que la ruta completa quede por debajo de ~245.

## Decks de sesión: contenido rico por sesión

El contenido proyectable de cada sesión vive en `config/slides/content/cun_<curso>_s<NN>.json` (bloques `bullets` / `table` / `boxes`) y lo renderiza `config/slides/cun_contenido_sesion.py`. **Para enriquecer una sesión se edita ese JSON**, no el builder — **con una excepción: el taller**, que es un marcador `{"type": "taller"}` y se edita en `config/slides/talleres.py`. Estándar: 12–16 slides dimensionadas para 2 horas, sin relleno genérico (ver `.cursor/rules/cun-docente.mdc` → «Decks de sesión»). **Los decks reales van hoy por encima de ese techo** (medido el 2026-08-11 sobre las 50 sesiones: Proyecto I 17–22 · Creatividad 19–27 · Investigación 19–35 · TG2 16–23 · TG3 18–25); el estándar es la meta, no una descripción de lo que hay.

## Guiones enriquecidos 2026-08-09

Las 45 sesiones de los 5 cursos (menos la Sesión 01 de cada uno, que ya era el modelo) se profundizaron al estándar de calidad (fases con protagonista propio, parlamento "GUION LITERAL" completo por fase, tabla de errores/preguntas trampa, tabla de acompañamiento en el taller). El contenido vive en los scripts generadores — **editar siempre el `.py`, nunca el `.md` directamente** (se sobrescribe al regenerar):
- Proyecto I: `Especializacion/Proyecto I/Docente/Guiones/_regen_guiones_proyecto1.py` (función `guion_NN` por sesión).
- Creatividad: `Pregrado/Creatividad y pensamiento innovador/Docente/Guiones/_regen_guiones_creatividad.py` (función `guion_NN` por sesión).
- Investigación + TG2 + TG3: `config/slides/_regen_guiones_pregrado.py` (compartido). Cada sesión es un `_spec(curso, n, ...)` con kwargs nuevos `fase1_texto`…`fase5_texto` y `errores` (si no se dan, cae a un texto genérico — por eso hay que darlos siempre al añadir/editar una sesión).
- Regenerar: `python <script> [curso] [N]` (ver docstring de cada script para la sintaxis exacta; `_regen_guiones_pregrado.py all` regenera los 3 cursos de pregrado a la vez).

**Verificar el mapa de slides — obligatorio después de tocar un deck:**

```text
python config/slides/verificar_mapas_slides.py     # sale 1 si hay algún desfase
```

Los tres generadores escriben la tabla «🗺️ Slides de esta presentación» y las referencias
`**Slides:** N (TÍTULO)` de cada fase **a mano**, no leyéndolas del `.pptx`. Cuando el deck se
reescribe, el guion queda mintiendo y el Docente busca en pantalla una slide con un título que ya
no existe — un fallo que solo se descubre en clase. El verificador compara las **1.020**
referencias (981 filas de tabla + 39 inline) de los 50 guiones contra los títulos reales de sus
decks; hoy va en **0 desfases**. Compara contra *todos* los cuadros de texto de la slide, no solo
`shapes.title`, porque en la slide del rompehielos «slido.com» está en letra más grande que el
encabezado y `titulos_pptx()` la toma por título.

## Resuelto 2026-08-15
- **Mapas de slides desfasados en 4 de los 5 cursos (10 títulos).** Los guiones de Sesión 01 de Investigación, TG2, TG3 y Proyecto I anunciaban slides que el deck ya no tiene: `LAS ACAs — QUÉ SE EVALÚA` (hoy `CÓMO SE EVALÚA — LOS ÍTEMS DEL AULA`), `Las ACAs, una por una` / `Las dos ACAs…` / `Las tres ACAs en detalle` (hoy `Corte por corte: qué hay en el aula y qué se prepara`) y `PRESÉNTATE — ROMPEHIELOS` (hoy `ROMPEHIELOS — DOS VERDADES Y UNA MENTIRA`). Corregidos en los generadores y blindado con `verificar_mapas_slides.py`.
- **Guion de evaluación:** la Sesión 01 le pedía al Docente «si alguna slide del deck todavía habla de las tres ACAs, corríjalo en voz alta». Verificado con `python-pptx` sobre los 50 decks: **ninguno** lo dice. La frase mandaba a buscar algo inexistente; ahora `guion_evaluacion.py:536` afirma en positivo cómo se llaman los ítems y menciona la numeración anulada como historia, no como sospecha.

## Resuelto 2026-08-10
- **Auto/coevaluación de Proyecto I ya no se llaman ACA.** Eran tres ACAs desde el Syllabus ESP329, pero el material las presentaba como una cuarta y quinta ACA. Ahora: `Clases/Recursos/ACAs/Autoevaluacion individual (4%) - instructivo.docx` y `…/Coevaluacion individual (4%) - instructivo.docx` (se borraron `ACA Autoevaluacion.docx` y `ACA Coevaluacion.docx`), redactados como instructivos de un instrumento que **se diligencia** en CDigital. Código (reverificado 2026-08-11): `build_acas_estudiantes.py` (campo `kind` + `acas_for()` en la línea 2046; `catalog_for_leeme()` en la 2060, devuelve dicts) y `sync_clases_estudiantes.py:32,110`, que lo consume. Sin cambios de % ni de fechas. **Corrección:** la vieja tabla «LAS ACAs» de la Sesión 01 **ya no existe** — la reemplazó la slide **«CÓMO SE EVALÚA — LOS ÍTEMS DEL AULA»**, con una fila por ítem del libro de calificaciones (quices, parciales, ACA Final, auto y coevaluación) y sin fechas. La arma `_evaluacion_rows()` en `build_sesion_material.py:246`, que lee todo de `fechas_entrega_aca.py`; la función `_acas_rows()` que citaba antes este LEEME ya no está en el repo.

## Resuelto 2026-08-09
- **Fechas ACA Proyecto I:** el Manual y el Calendario oficial se corrigieron para usar la Cronograma OFICIAL de Coordinación (fuente única). Con los nombres del aula (que es como se rotulan hoy): **Quiz** cierre **30/08**/nota **07/09** · **ACA 1** cierre **04/10**/nota **12/10** · **ACA FINAL** cierre **08/11**/nota **16/11**. *(En su momento se escribieron como ACA1 / ACA2 / ACA3, numeración del Syllabus ESP329 que ya no se usa en ninguna parte: el 30/08 lo cierra el **Quiz**, no la ACA 1.)* Se retiró la tabla duplicada calculada por `fechas_entrega_aca.py` que se había desviado. También se corrigió el CSV de hitos (`Entregas y hitos docentes - Importar a Calendar.csv`, raíz y `2026/54ES4/`) — **si ya se importó una versión vieja a Google Calendar, hay que reimportarlo o corregir esos eventos a mano.** ✅ *Actualización 2026-08-10:* los enunciados ACA (`Clases/Recursos/ACAs/*.docx`) **también quedaron con las fechas oficiales** en la regeneración del 10/08 (verificado en disco). Ya no hay desalineación que comunicar a los estudiantes.
- **Modalidad Investigación (EI005, 53339):** confirmado **virtual** (el `.docx` "_PRES" es la plantilla genérica del programa, no refleja la oferta real de este grupo).

---

## Si git dice «bad object refs/desktop.ini»

Este repositorio vive **dentro de Google Drive**, y Drive escribe un `desktop.ini` en cada carpeta
que decora — incluidas las de `.git`. Git lee cualquier archivo bajo `.git/refs/` como si fuera una
referencia, así que en cuanto aparece uno ahí, `git fetch` muere con:

```
fatal: bad object refs/desktop.ini
error: ... did not send all necessary objects
```

No es corrupción: son 150 archivos idénticos de 246 bytes (`[.ShellClassInfo]`, UTF-16, apuntando al
icono de `GoogleDriveFS.exe`). El arreglo es borrarlos y comprobar que el repositorio quedó sano:

```bash
find .git -iname "desktop.ini" -delete
git fsck --no-progress    # sin salida = sano
git fetch origin && git status --short --branch
```

Va a volver a pasar cada vez que Drive redecore las carpetas. `.gitignore` no sirve para esto: lo
ignorado es lo del árbol de trabajo, y estos están **dentro** de `.git`, donde `.gitignore` no
aplica. Ojo con el orden de los síntomas: `git commit` y `git push` siguen funcionando —lo que se
rompe primero es `fetch`—, así que se puede llevar días sin notarlo.

---

## Contexto rápido (para un agente nuevo)

Workspace de material docente CUN. Cinco cursos 2026: Proyecto I (esp. IA, 54ES4) + Creatividad, Investigación, TG2 y TG3 (pregrado). Config editable en `config/cursos/carga_academica_2026.json`. Material de estudiantes solo en `Clases/`; guiones solo `.md` en `Docente/Guiones/`; oferta en `2026/<grupo>/`. Marca y motor en `cun.json` + `cun_slides_engine.py`.
