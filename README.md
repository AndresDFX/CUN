# Material Docente CUN — Workspace 2026

**Docente:** Julian Andres Castaño Espinosa · `julian_castanoe@cun.edu.co`

---

## 🚨 PROCEDIMIENTO OBLIGATORIO CADA SEMESTRE

### ALISTAMIENTO DE AULAS EN CDIGITAL

**ANTES DE INICIAR CADA SEMESTRE, EJECUTAR:**

📋 **[ALISTAMIENTO_DE_AULAS_CDIGITAL.md](ALISTAMIENTO_DE_AULAS_CDIGITAL.md)**

**Qué hace:**
- ✅ Activa todo el material para estudiantes (carpetas + cuestionarios)
- ✅ **Oculta los componentes de plantilla que no dan nota** (foros vacíos, SCORM «Contenido N», placeholders)
- ✅ Verifica que los cuestionarios tengan preguntas correctas
- ✅ Ajusta fechas de todos los elementos evaluativos
- ✅ **Destraba las encuestas institucionales** que llegan abriendo en 2028 o 2030 (nunca abren)
- ✅ Genera documentación de auditoría

**Cuándo:**
- **1-2 días antes del inicio de clases**
- Una vez por semestre

**Duración:**
- 2-3 horas para las 7 aulas

**IMPORTANTE:** Este procedimiento debe ejecutarse **SÍ O SÍ** al inicio de cada semestre para que los estudiantes tengan acceso al material con fechas correctas.

---

## 📚 Documentación Principal

### Mapas y Referencias
- **[LEEME - Mapa de cursos y manuales.md](LEEME%20-%20Mapa%20de%20cursos%20y%20manuales.md)** — Mapa completo del workspace
- **[Pregrado/0. General/LEEME - Inicio desarrollo y cierre de cursos.md](Pregrado/0.%20General/LEEME%20-%20Inicio%20desarrollo%20y%20cierre%20de%20cursos.md)** — Ciclo docente pregrado
- **[Especializacion/0. General/LEEME - Inicio desarrollo y cierre de cursos.md](Especializacion/0.%20General/LEEME%20-%20Inicio%20desarrollo%20y%20cierre%20de%20cursos.md)** — Ciclo docente especialización

### Investigación y eventos
- **`Investigacion/Preprints 2026/`** — manuscritos, PDF y `REGISTRO_DE_ENVIOS.md` (números de envío, estado y DOI). Agentes: `publicaciones-cun` (deposita) · `estado-publicaciones-cun` (solo vigila).
- **`Eventos/<Nombre del evento>/`** — postulaciones a congresos y encuentros. Una carpeta por evento con el `.md` del resumen (**fuente de verdad**), el `.docx` generado, `HOJA_DE_RESPUESTAS_Formulario.md` y su propio `_armar_resumen_docx.py`. El texto se edita en el `.md` y se regenera — nunca en Word — y `config/slides/guion_md_a_docx.py` **no sirve** aquí (derrama un resumen corto en dos hojas). Un evento paga el producto de *Evento científico* de Synapse, **no `ART_OPEN_D`**.

### Auditorías y Verificaciones (última ejecución: agosto 2026)
- **[VERIFICACION_MATERIAL_VISIBLE_CDIGITAL.md](VERIFICACION_MATERIAL_VISIBLE_CDIGITAL.md)** — Análisis detallado de activación
- **[CONFIRMACION_MATERIAL_CORRECTO_CDIGITAL.md](CONFIRMACION_MATERIAL_CORRECTO_CDIGITAL.md)** — Resumen ejecutivo
- **[VALIDACION_CALIDAD_PREGUNTAS_CUESTIONARIOS.md](VALIDACION_CALIDAD_PREGUNTAS_CUESTIONARIOS.md)** — Validación de preguntas (no genéricas)
- **[FECHAS_AJUSTADAS_CDIGITAL.md](FECHAS_AJUSTADAS_CDIGITAL.md)** — Desglose de fechas ajustadas · incluye las **13 encuestas institucionales que nunca abrían** (2028/2030), el hallazgo del **ACA Final candado por la Evaluación Docente 3** y los 8 pendientes que salieron de la auditoría: **5 resueltos, 1 a medias y 2 que necesitan a la plataforma** (los cierres en 2028/2030, que no son editables desde el formulario)
- **[OCULTAMIENTO_NO_EVALUATIVO_CDIGITAL.md](OCULTAMIENTO_NO_EVALUATIVO_CDIGITAL.md)** — 101 componentes de plantilla ocultados · regla y reversa
- **[DIAGNOSTICO_FORO_1_CREATIVIDAD.md](DIAGNOSTICO_FORO_1_CREATIVIDAD.md)** — Los foros vacíos por los que preguntaban los estudiantes

---

## 🎓 Cursos en este Workspace

### Pregrado (Escuela de Ingenierías)
1. **Creatividad y Pensamiento Innovador** (EI004, grupo 54408)
2. **Investigación en Ciencia y Tecnología** (EI005, grupo 53339)
3. **Trabajo de Grado 2** (grupo 54448)
4. **Trabajo de Grado 3** (grupos 54450, 54466, 54467)

### Especialización (Inteligencia Artificial)
5. **Proyecto I** (ESP329, grupo 54ES4)

**Total: 7 aulas en CDigital**

---

## 🔧 Herramientas Principales

### Cliente CDigital
```bash
python config/moodle/cdigital.py <comando> [opciones]
```

**Comandos clave:**
- `estado` — Verificar sesión
- `curso <id>` — Listar actividades de un aula
- `mostrar <cmid>` / `ocultar <cmid>` — Cambiar visibilidad de una actividad
- `fechas <curso> --incluir-visibles --confirmar` — Ajustar fechas de los ítems evaluativos
- `encuestas <curso>` — Censar las encuestas institucionales (`feedback`); con `--sin-apertura` o
  `--abre AAAA-MM-DD` más `--cmid` las destraba
- `quiz <cmid>` — Ver detalles de un cuestionario

### Destrabar las encuestas institucionales
```bash
python config/moodle/cdigital.py encuestas 111070                                                   # censo, no toca nada
python config/moodle/cdigital.py encuestas 111070 --sin-apertura --cmid 6522193 --confirmar          # la norma: siempre disponible
python config/moodle/cdigital.py encuestas 111070 --abre 2026-08-10 --cmid 6522212 --confirmar       # solo «Evalúa tu Entorno»
```
Las 4 encuestas por aula («Evaluación Docente 1/2/3» y «Evalúa tu Entorno») **no las ajusta
`fechas`**: llegan con la apertura de plantilla en 2028/2030 y **nunca abren**, sin dar ningún error.
Se corrigen una por una con `--cmid`, y **nunca** las que dicen «sin apertura programada» (tienen
respuestas de estudiantes dentro). ⛔ Un `feedback` **no tiene campo de fecha de cierre** en esta
instalación, así que una apertura no acota nada: solo retrasa. Por eso «Evaluación Docente 1/2/3» van
con `--sin-apertura`, y más aún porque **el ACA Final está candado por la finalización de la ED3**: la
fecha de una encuesta sin nota acaba siendo la fecha real de una entrega del 32,8 %. Detalle en
[FECHAS_AJUSTADAS_CDIGITAL.md](FECHAS_AJUSTADAS_CDIGITAL.md) y Problemas 7 a 11 de
[ALISTAMIENTO_DE_AULAS_CDIGITAL.md](ALISTAMIENTO_DE_AULAS_CDIGITAL.md).

### Depurar lo no evaluativo
```bash
python config/moodle/ocultar_no_evaluativo.py              # plan, no toca nada
python config/moodle/ocultar_no_evaluativo.py --confirmar  # ejecuta
```
Deja visible solo lo que da nota + el material del Docente + Avisos + el foro de
presentación. Detalle en [OCULTAMIENTO_NO_EVALUATIVO_CDIGITAL.md](OCULTAMIENTO_NO_EVALUATIVO_CDIGITAL.md).

### Opciones de revisión de los cuestionarios
```bash
python config/moodle/revision_quiz.py censar 6745720   # lee las 32 casillas de revisión
```
Las cuatro columnas («Durante el intento / Inmediatamente después / Más tarde / Después de cerrar»)
deciden si un cuestionario **regala la respuesta correcta**. `cdigital.py` no tiene subcomando para
esto. Va en seco por omisión.

### Builds y Regeneración
```bash
# Orden completo (ver LEEME - Mapa):
python config/cursos/sync_manuales_fechas.py
python config/slides/build_all_course_presentations.py
python config/slides/build_calendar_encuentros.py
python config/slides/build_apps_script_grabaciones.py
python config/slides/build_hitos_docentes_calendar.py
python config/slides/build_sesion_material.py all all
python config/slides/build_acas_estudiantes.py
python config/slides/build_rompehielos_slido.py
python config/slides/build_correo_bienvenida.py
python config/slides/sync_clases_estudiantes.py
```

---

## 📅 Fechas Clave (Semestre 2026-2)

| Curso | Inicio | Recepción | Cierre | Horario |
|-------|--------|-----------|--------|---------|
| Creatividad | 03/08 | 19/09 | 27/09 | Mié 5-6 pm |
| Investigación | 03/08 | 12/09 | 20/09 | Jue 5-6 pm |
| TG2 | 03/08 | 14/11 | 22/11 | Lun 5-6 pm |
| TG3 (54450) | 03/08 | 07/11 | 15/11 | Mar 5-6 pm |
| TG3 (54466/54467) | 03/08 | 14/11 | 22/11 | Mar 5-6 pm |
| Proyecto I | 10/08 | 14/11 | 22/11 | Lun 8-10 pm |

**Fuente:** `config/cursos/carga_academica_2026.json` + `fechas_entrega_aca.py`

---

## 🔒 Credenciales

**CDigital:** `%LOCALAPPDATA%\cdigital-cun\credenciales.json`
```json
{"url": "https://cdigital.cun.edu.co", "usuario": "...", "clave": "..."}
```

**NUNCA** commitear credenciales al repositorio.

---

## 📞 Contactos

- **Dirección Nacional de Investigación (DNI):** convocatoria_investigacion@cun.edu.co
- **Coordinación Especializaciones AFI:** investigacion_especializaciones@cun.edu.co
- **Plataforma:** CDigital (Moodle CUN) — https://cdigital.cun.edu.co

---

## ⚠️ Recordatorio Final

**ANTES DE CADA SEMESTRE:**

1. ✅ Actualizar fechas en `config/cursos/fechas_entrega_aca.py`
2. ✅ Regenerar material con los builds
3. ✅ **EJECUTAR ALISTAMIENTO DE AULAS** ([ver procedimiento](ALISTAMIENTO_DE_AULAS_CDIGITAL.md))
4. ✅ Verificar que todo esté correcto antes del inicio de clases

**El alistamiento NO es opcional — es el procedimiento estándar obligatorio.**

---

**Última actualización:** 27 de agosto de 2026  
**Próximo alistamiento programado:** Inicio de semestre 2027-1
