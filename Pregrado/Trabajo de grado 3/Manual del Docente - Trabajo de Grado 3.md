# Manual del Docente — TRABAJO DE GRADO 3 (Modelos de Innovación, Ingeniería de Sistemas)
**Plantilla genérica.** Código SIAC: **94532** · 32 h docente + 64 h autónomas · Opción de grado III.
Fuente: `TRABAJO DE GRADO 3-MDI_INGENIERIA DE SISTEMAS_94532_PRES_VIR.docx` (en esta carpeta).

> **NO** se rige por el instructivo AFI de Proyecto I/II.

## 📁 Estructura
- **`Clases/`** — presentación del curso (15 sesiones = encuadre + U3–U14 + 2 buffers) + **`Sesion NN - <tema>/Presentacion.pptx`** · docente **Julian Andres Castaño** · `julian_castanoe@cun.edu.co`
- **`Guiones/`** — `Sesion NN - <tema>.md` (solo Markdown; no hay `.docx`) + `Capturas/`
- **`Calendario…`** · festivo = autónoma · 54450 cierra 15/11; 54466/54467 hasta 22/11
- **`2026/<grupo>/`** + `_combinado_*` para Calendar multi-grupo (**sin invitados estudiantes**; Meet placeholder único)

**Horario confirmado:** martes, **5:00–6:00 pm**.
**Festivo en martes → clase autónoma.**

## 1. Qué es
Culminación del trabajo de grado: **artículo** (≥ 50 referencias; ≥ 4.000 palabras según syllabus) + **sustentación ante jurados** + carga a repositorio.
Prerrequisito: Opción de grado II.

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

## 3. Evaluación
**Corte único = 100%** · EV05 50% (proceso) + EXAM 50% (sustentación ante pares/jurados).
**Enunciados estudiantes:** `Clases/Recursos/ACAs/` (ACA 1 = EV05 · ACA 2 = EXAM).

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py tg3`.

| Componente | Entrega | Apertura | Nota docente | Regla |
| :--- | :--- | :--- | :--- | :--- |
| **ACA 1 (EV05)** (54450) | 22/09/2026 | 10/08/2026 | 29/09/2026 | pesos + día de clase |
| **ACA 2 (EXAM)** (54450) | 03/11/2026 | 29/09/2026 | 10/11/2026 | pesos + día de clase |
| **ACA 1 (EV05)** (54466) | 22/09/2026 | 10/08/2026 | 29/09/2026 | pesos + día de clase |
| **ACA 2 (EXAM)** (54466) | 10/11/2026 | 29/09/2026 | 17/11/2026 | pesos + día de clase |
| **ACA 1 (EV05)** (54467) | 22/09/2026 | 10/08/2026 | 29/09/2026 | pesos + día de clase |
| **ACA 2 (EXAM)** (54467) | 10/11/2026 | 29/09/2026 | 17/11/2026 | pesos + día de clase |

> Periodo [inicio–recepción] repartido por pesos del componente; entrega = día de clase semanal en o antes del fin de tramo (ultimo item <= recepcion). P1: coev/autoev tras ACA 3 hasta cierre. Fuente: config/cursos/fechas_entrega_aca.py + carga_academica_2026.json. Grupo 54450.
> Periodo [inicio–recepción] repartido por pesos del componente; entrega = día de clase semanal en o antes del fin de tramo (ultimo item <= recepcion). P1: coev/autoev tras ACA 3 hasta cierre. Fuente: config/cursos/fechas_entrega_aca.py + carga_academica_2026.json. Grupo 54466.
> Periodo [inicio–recepción] repartido por pesos del componente; entrega = día de clase semanal en o antes del fin de tramo (ultimo item <= recepcion). P1: coev/autoev tras ACA 3 hasta cierre. Fuente: config/cursos/fechas_entrega_aca.py + carga_academica_2026.json. Grupo 54467.

## 4. Grupos 2026
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`).

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 54450 | 26P04 | BLOQUE UNICO | 10/08/2026 | 07/11/2026 | 15/11/2026 |
| 54466 | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | 22/11/2026 |
| 54467 | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | 22/11/2026 |
