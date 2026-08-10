# Manual del Docente — TRABAJO DE GRADO 2 (Modelos de Innovación, Ingeniería de Sistemas)
**Plantilla genérica.** Pregrado · opción de grado II · 2 créditos · Virtual.

> ⚠️ **Falta el syllabus oficial SIAC** en esta carpeta. El material de presentación es orientativo (analogía con TG3 + datos del portal). Cuando consigas el `.docx` SIAC, colócalo aquí y actualiza pesos/temario.

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

## 3. Evaluación
Art. 52 · **30% / 30% / 40%** orientativo mientras no aparezca el Syllabus SIAC (⚠️ confirmar los pesos). Lo que **sí** está decidido (2026-08-10) y ya está en el material del estudiante: **cada ACA evalúa el 100% de su corte**, sin subdividir en varios EV.
**Enunciados orientativos estudiantes:** `Clases/Recursos/ACAs/` (actualizar cuando exista SIAC).

## Fechas de entrega ACA / cortes

Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar con `python config/cursos/sync_manuales_fechas.py tg2`.

| Componente | Entrega | Apertura | Nota docente | Regla |
| :--- | :--- | :--- | :--- | :--- |
| **ACA 1** | 07/09/2026 | 10/08/2026 | 14/09/2026 | pesos + día de clase |
| **ACA 2** | 05/10/2026 | 14/09/2026 | 12/10/2026 | pesos + día de clase |
| **ACA 3** | 09/11/2026 | 12/10/2026 | 16/11/2026 | pesos + día de clase |

> Periodo [inicio–recepción] repartido por pesos del componente; entrega = día de clase semanal en o antes del fin de tramo (ultimo item <= recepcion). P1: coev/autoev tras ACA 3 hasta cierre. Fuente: config/cursos/fechas_entrega_aca.py + carga_academica_2026.json.

## 4. Grupos 2026
Fuente editable: `config/cursos/carga_academica_2026.json` (Excel: `Carga academica 2026.xlsx`). Código materia: **94453**.

| Grupo | Periodo | Bloque | Inicio | Recepción | Cierre |
|---|---|---|---|---|---|
| 54448 | 26V04 | BLOQUE UNICO | 10/08/2026 | 14/11/2026 | 22/11/2026 |

> Si se asigna un **segundo grupo** al mismo horario, agrégalo en el JSON/build y vuelve a generar el CSV/ICS combinado (el título del evento quedará tipo `Grupos 54448 / XXXXX`).
