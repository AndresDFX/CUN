# Manual del Docente — TRABAJO DE GRADO 2 (Modelos de Innovación, Ingeniería de Sistemas)
**Plantilla genérica.** Pregrado · opción de grado II · 2 créditos · Virtual.

> ⚠️ **Falta el syllabus oficial SIAC** en esta carpeta. El **temario** de presentación sigue siendo orientativo (analogía con TG3 + datos del portal). Cuando consigas el `.docx` SIAC, colócalo aquí y actualiza el temario.
>
> ✅ La **evaluación ya NO es orientativa** (2026-08-10): sale del libro de calificaciones del aula en CDigital — tres cortes 30/30/40 con quices, parciales, ACA Final, autoevaluación y coevaluación. Ver §3.

## 📁 Estructura
- **`Clases/`** — presentación del curso (temario orientativo ⚠️) + **`Sesion NN - <tema>/Presentacion.pptx`** · docente **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`
- **`Guiones/`** — `Sesion NN - <tema>.md` orientativos, solo Markdown (falta syllabus) + `Capturas/`
- **`Calendario…`** · festivo lunes = autónoma
- **`2026/<grupo>/`** — Informacion + CSV/ICS (Subject con grupo; **sin invitados estudiantes**)

**Horario confirmado:** lunes, **5:00–6:00 pm**.
**Festivo (lunes) → clase autónoma** (CDigital). En 2026 caen: 17/08, 12/10, 02/11, 16/11.

## 1. Qué es
Fase previa a Trabajo de Grado 3: avance consolidado del proyecto/artículo. **No** aplica instructivo AFI de Especializaciones.
Formato: `Plantilla_APA_CUN_Proyecto de grado.docx`.

## 2. Enfoque orientativo (confirmar con syllabus)

> **La Sesión 01 (10/08/2026) es de ENCUADRE: no se dicta tema.** Se presenta el curso, el Docente, los estudiantes (Padlet) y las ACAs. Delimitación / reformulación del tema → lectura autónoma; se retoma al abrir la Sesión 02. (El acuerdo pedagógico se firma en esta sesión de encuadre.) El contenido curricular arranca en la **Sesión 02**.

- Retomar/delimitar proyecto de semestres anteriores.
- Consolidar planteamiento, pregunta, objetivos, marco referencial.
- Avanzar diseño metodológico.
- Dejar listo el documento para culminación/sustentación en TG3.

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

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 54448 | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | 22/11/2026 |

> Si se asigna un **segundo grupo** al mismo horario, agrégalo en el JSON/build y vuelve a generar el CSV/ICS combinado (el título del evento quedará tipo `Grupos 54448 / XXXXX`).
