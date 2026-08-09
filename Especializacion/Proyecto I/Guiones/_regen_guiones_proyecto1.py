# -*- coding: utf-8 -*-
"""Regenera los 11 guiones docentes de Proyecto I (ESP329) a estándar locución.

Formato: solo .md (sin .docx).
Duración: ≈60 min contenido + 60 min tutoría.
Modelo de calidad: Creatividad Sesión 01.
Fuente curricular: ESP329 · Manual del Docente · sesiones_cun.py.
URLs AFI: desde sesiones_cun (cun.json → links_afi).

Uso:
  python _regen_guiones_proyecto1.py          # todas
  python _regen_guiones_proyecto1.py 3        # solo sesión 3
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.normpath(os.path.join(ROOT, "..", "..", "..", "config", "slides"))
CURSOS = os.path.normpath(os.path.join(ROOT, "..", "..", "..", "config", "cursos"))
sys.path.insert(0, SLIDES)
sys.path.insert(0, CURSOS)

from sesiones_cun import (  # noqa: E402
    COURSES,
    LINK_REGISTRO_DOCENTE_AFI,
    LINK_TUTORIAS,
    MSG_TUTORIAS_POR_GRUPO,
    meet_placeholder,
)
from cun_slides_engine import PADLET_PRESENTACION_URL  # noqa: E402

MEET = meet_placeholder("PROYECTO I")
COURSE = COURSES["proyecto1"]


def topic_filename(titulo: str, max_len: int = 70) -> str:
    import re

    s = re.sub(r'[<>:"/\\|?*]', "", titulo.strip())
    s = re.sub(r"\s+", " ", s).strip(" .")
    return (s[:max_len] or "Tema").rstrip()


def label_for(n: int, titulo: str) -> str:
    return f"Sesion {n:02d} - {topic_filename(titulo)}"


def plan_tabla(fases):
    rows = [
        "| Fase | Minutos | Reloj sugerido (desde el inicio) |",
        "| :--- | :---: | :--- |",
    ]
    start = 0
    for nombre, mins in fases:
        rows.append(f"| {nombre} | {mins} | min {start:02d}:00 – {start + mins:02d}:00 |")
        start += mins
    rows.append("")
    rows.append(f"> **Suma bloque contenido:** **{sum(m for _, m in fases)} minutos**.")
    rows.append("> Luego: **60 min tutoría** (2.ª hora del encuentro).")
    return "\n".join(rows)


def slides_table_std():
    return """🗺️ **Slides de esta presentación** (tema de hoy — no es el mapa del curso)

| Slide | Título en el PPTX | Cuándo usarla |
| :---: | :--- | :--- |
| **1** | Portada — Sesión NN | Apertura |
| **2** | OBJETIVOS | Encuadre |
| **3** | CONTENIDO CLAVE | Exposición |
| **4** | RECUERDA | Tutorías / instrumentos propuestos |
| **5** | ACTIVIDAD / TALLER | Consigna práctica |
| **6** | PARA CONTINUAR | Trabajo autónomo |
| **7** | Cierre | Despedida |
"""


def post_clase():
    return f"""
---

📋 **Checklist post-clase / seguimiento AFI**
- [ ] **Seguimiento docente — diligenciar formulario** de *Registro de Sesiones Sincrónicas y Tutorías Especialización* **dentro de 24h**, con el link de grabación: {LINK_REGISTRO_DOCENTE_AFI} *(uso exclusivo docente AFI — no compartir con estudiantes)*
- [ ] En tutoría: recordé a los estudiantes su formulario de asistencia: {LINK_TUTORIAS}
"""


def tutoria_block(foco: str) -> str:
    return f"""
---

#### 6️⃣ Tutoría / taller por equipos (~60 min) — Protagonista: Equipos + Docente
**Sin slides nuevas** (sigue abierta la deck de hoy o la plantilla APA en Google Docs).

> **Acuerdo:** {MSG_TUTORIAS_POR_GRUPO} Esta 2.ª hora del encuentro es el bloque de tutoría/taller en vivo; tutorías adicionales por equipo se agendan en la semana. En cada una, el estudiante registra asistencia en el formulario.

**GUION LITERAL (apertura tutoría):**
> “Segunda hora: **tutoría**. Cada equipo trabaja su avance. Yo circule. Cada estudiante que esté en tutoría diligencia su asistencia: {LINK_TUTORIAS} — lo pego en el chat. Recuerden: {MSG_TUTORIAS_POR_GRUPO}”

**Foco de hoy en tutoría:** {foco}

**Rutina por equipo (≈8–12 min c/u si hay varios):**
1. ¿Qué trajeron escrito? (pantalla compartida o párrafo en el chat).
2. Una pregunta de coherencia (¿pregunta ↔ objetivos ↔ método tentativo?).
3. Un acuerdo observable para la próxima (una sección o corrección concreta) y, si hace falta, **cita de tutoría adicional en la semana**.

**Cierre tutoría (2 min):**
> “Grabación completa. Yo registro la sesión en mi formulario docente dentro de 24h. Ustedes, si aún no, cierren el form de asistencia. Si necesitan otra revisión por equipo, la acordamos en la semana. Nos vemos en el próximo encuentro.”
"""


# ---------------------------------------------------------------------------
# Contenido rico por sesión (fundamento + fases + taller)
# ---------------------------------------------------------------------------

def guion_01(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fases = [
        ("1️⃣ Encuadre + Preséntate (Padlet en Presentación del Curso)", 12),
        ("2️⃣ Qué es (y no es) un anteproyecto · P-I vs P-II", 12),
        ("3️⃣ Enfoques, ética y rol del docente garante", 10),
        ("4️⃣ Taller: ficha de encuadre del equipo / tema tentativo", 18),
        ("5️⃣ Cierre contenido + puente a tutoría", 8),
    ]
    return f"""### GUIÓN DOCENTE — Sesión {n:02d}: {titulo}

> **Uso:** guion de locución de **esta** clase. Léalo en voz alta casi literal.
> Estudie primero el Fundamento Teórico. **Duración: ≈60 min contenido + 60 min tutoría**.
> Logística de semestre (fechas, grupos, cortes) → Presentación del Curso / Manual.
> **PPTX:** `Clases/{label}/Presentacion.pptx` — en cada fase se indica la slide de ESA presentación.

📌 **De esta sesión**
- **Sesión:** **{n:02d}** · **Tema:** {titulo}
- **Detalle:** {detalle}
- **PPTX estudiante:** `Clases/{label}/Presentacion.pptx`
- **Meet (serie del curso):** {MEET}

> ⚠️ Temario curricular = 7 unidades didácticas del ESP329. Las 11 sesiones semanales del calendario AFI desarrollan esas unidades.

{slides_table_std()}
> **Rompehielos Padlet:** slide **PRESÉNTATE** de `Clases/Presentacion del Curso - ….pptx` (esta Sesión 01 es la de presentación). No hay slide Padlet duplicada en esta deck.

🎯 **Objetivos de la sesión**
1. **Comprender** qué es un anteproyecto y la frontera Proyecto I → Proyecto II (instrumentos solo propuestos).
2. **Ubicar** el rol del docente como garante metodológico y las líneas oficiales de IA del programa.
3. **Dejar** un avance escrito: tema tentativo + expectativa + posibles compañeros de equipo.
4. **Registrar** el hábito de tutorías (formulario estudiante) y conocer la estructura 60+60.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Asuma que un colega nuevo dicta esta clase: las definiciones de aquí son las que dirá en voz alta.

#### 1. Qué es (y qué NO es) un anteproyecto
Un **anteproyecto de investigación** demuestra que una pregunta es **viable, coherente y metodológicamente defendible** **antes** de recolectar datos. En AFI / Especializaciones, Proyecto I culmina en ese anteproyecto; Proyecto II es la ejecución.

| Concepto | Proyecto I | Proyecto II |
| :--- | :--- | :--- |
| Producto | Anteproyecto aprobado | Investigación ejecutada / resultados |
| Instrumentos | Solo **propuestos** | Aplicados |
| Campo / encuestados | No | Sí (con aval) |
| Rol docente | Garante metodológico | Acompañamiento de ejecución |

**Error frecuente:** querer “ya encuestar” en la semana 2. Respuesta: “En Proyecto I diseñamos; en Proyecto II aplicamos, tras el aval.”

#### 2. Líneas oficiales de IA (anclaje temático)
Todo anteproyecto debe poder ubicarse en:
1. **Uso y adaptación de IA para entornos productivos**
2. **Implementación de IA en la educación**

Si el tema no entra, oriente a reformular (no “inventar” una tercera línea).

#### 3. Estructura del encuentro de 2 horas
- **60 min contenido:** concepto + modelación + taller breve.
- **60 min tutoría:** trabajo por equipos; el estudiante registra asistencia en {LINK_TUTORIAS}. {MSG_TUTORIAS_POR_GRUPO}
- Grabación obligatoria de todo el encuentro. Usted registra en formulario docente AFI <24h.

#### 4. Ética mínima del día 1
No prometan acceso a datos sensibles sin protocolo. No presenten “ya tengo resultados” sin método. El anteproyecto **propone**; no ejecuta.

#### 5. Errores frecuentes / preguntas trampa
- “¿Puedo aplicar la encuesta este mes?” → No en P-I.
- “Mi tema es IA en general” → Exija contexto + línea oficial + usuario/dolor.
- Confundir **tema amplio** con **pregunta investigable**.

---

🧭 **Plan de Clase por Fases** — *contenido ≈ 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Encuadre + Preséntate / Padlet (~12 min) — Protagonista: Docente
**Slides:** Presentación del Curso → PRESÉNTATE; luego esta deck 1 → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes. **Sesión 01** — presentación del curso y fundamentos. Al terminar la primera hora deben tener claro **qué es un anteproyecto** y un **tema tentativo** escrito. La segunda hora es tutoría por equipos.”

> “Abrimos la **Presentación del Curso**, slide **PRESÉNTATE**. Escaneen el QR o abran: {PADLET_PRESENTACION_URL} — también en el chat. Post-it con: (a) expectativa del curso y (b) **tema tentativo** de investigación en una frase. **~7 minutos**.”

> “Pasamos a la deck de Sesión 01. **Slide 2 — OBJETIVOS.** Hoy: frontera P-I/P-II, líneas de IA, acuerdos de trabajo, y un avance observable.”

**Qué hacer:** (1–2 min) Meet/audio · (6–7 min) Padlet · (3 min) objetivos de esta deck.

---

#### 2️⃣ Qué es un anteproyecto · P-I vs P-II (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) → 4 (RECUERDA)

**GUION LITERAL:**
> “**Slide 3.** Idea madre: el anteproyecto demuestra que la pregunta es **defendible antes de recolectar datos**. En Proyecto I **proponen** instrumentos; en Proyecto II los **aplican** con aval. Si alguien ya quiere encuestar, freno amable: diseñamos primero.”

> “**Slide 4 — RECUERDA.** {MSG_TUTORIAS_POR_GRUPO} Cada vez que asistan a tutoría, diligencien {LINK_TUTORIAS}. Es su evidencia; el mío es otro formulario, solo docente.”

**Qué hacer:** tabla P-I/P-II en pantalla (Google Docs / Excalidraw) · 1 pregunta oral a 2 estudiantes.

---

#### 3️⃣ Enfoques, ética y garante metodológico (~10 min) — Protagonista: Docente
**GUION LITERAL:**
> “Mi rol no es ser el experto de cada aplicación de IA que propongan. Soy **garante metodológico**: coherencia pregunta–objetivos–marco–método, viabilidad y APA CUN. Las líneas oficiales son dos: entornos productivos, o educación. Si su tema no cabe, lo reformulamos.”

> “Ética del día 1: no inventen datos; no prometan acceso a historias clínicas o bases privadas sin protocolo. El documento propone; no ejecuta.”

---

#### 4️⃣ Taller: ficha de encuadre (~18 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** 18 minutos. En Google Docs (plantilla APA CUN o doc corto) escriban: (1) nombres del equipo tentativo (máx. 3), (2) línea oficial de IA, (3) tema en una frase, (4) contexto (empresa/aula/proceso), (5) una duda metodológica. Criterio de éxito: si yo leo la frase del tema y entiendo **dónde** ocurre y **para quién**, sirve.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Solo dice “voy a usar ChatGPT” | “¿Qué problema de un usuario concreto resuelve y en qué línea oficial cabe?” |
| Tema planetario | “Bájenlo a un contexto observable este periodo.” |
| Quiere encuestar ya | “Hoy diseñamos; campo = Proyecto II.” |

---

#### 5️⃣ Cierre contenido (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Tres ideas: (1) anteproyecto = viabilidad **antes** del campo; (2) P-I propone, P-II aplica; (3) dos líneas oficiales de IA. **Slide 6:** suban a CDigital el avance `S01_Encuadre_Apellidos`; lean la plantilla APA CUN; traigan a S02 un problema delimitado en 8–12 líneas. **Slide 7:** pasamos a tutoría.”

{tutoria_block("confirmar equipos (máx. 3), línea oficial, tema tentativo; destrabar dudas de CDigital/plantilla APA.")}

---

🧩 **Entregable de hoy**
1. Ficha de encuadre (equipo + línea + tema + contexto) en CDigital: `S01_Encuadre_Apellidos`.
2. **Éxito:** un lector externo entiende contexto y para quién es el problema.
3. Rompehielos Padlet = Presentación del Curso (no se repite).

✅ **Checklist antes de clase**
- [ ] Fundamento teórico leído
- [ ] Presentación del Curso (Preséntate / Padlet): {PADLET_PRESENTACION_URL}
- [ ] PPTX `Clases/{label}/Presentacion.pptx`
- [ ] Espacio de entrega en CDigital
- [ ] Link tutorías listo para chat: {LINK_TUTORIAS}
- [ ] Meet: {MEET}
{post_clase()}
---
*Fin del Guión — Sesión 01. Autocontenido para dictar 60+60.*
"""


def _body(n, titulo, detalle, label, objetivos, fundamento, fases_plan, fases_texto, taller_foco, entregable, tutoria_foco):
    return f"""### GUIÓN DOCENTE — Sesión {n:02d}: {titulo}

> **Uso:** guion de locución de **esta** clase. Léalo en voz alta casi literal.
> Estudie primero el Fundamento Teórico. **Duración: ≈60 min contenido + 60 min tutoría**.
> Logística de semestre → Presentación del Curso / Manual. **Sin fechas de periodo en este guion.**
> **PPTX:** `Clases/{label}/Presentacion.pptx`

📌 **De esta sesión**
- **Sesión:** **{n:02d}** · **Tema:** {titulo}
- **Detalle:** {detalle}
- **PPTX estudiante:** `Clases/{label}/Presentacion.pptx`
- **Meet (serie del curso):** {MEET}

> ⚠️ Temario curricular = 7 unidades ESP329 · 11 sesiones AFI las desarrollan.

{slides_table_std()}
🎯 **Objetivos de la sesión**
{objetivos}

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

{fundamento}

---

🧭 **Plan de Clase por Fases** — *contenido ≈ 60 min*

{plan_tabla(fases_plan)}

---

{fases_texto}

{tutoria_block(tutoria_foco)}

---

🧩 **Entregable de hoy**
{entregable}

✅ **Checklist antes de clase**
- [ ] Fundamento teórico leído
- [ ] PPTX `Clases/{label}/Presentacion.pptx`
- [ ] Material / plantilla APA en CDigital o Google Docs
- [ ] Link tutorías para chat: {LINK_TUTORIAS}
- [ ] Meet: {MEET}
{post_clase()}
---
*Fin del Guión — Sesión {n:02d}. Autocontenido para dictar 60+60.*
"""


def guion_02(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = f"""#### 1. Del tema al problema investigable
Un **tema** es un campo amplio (“IA en educación”, “IA en la industria”). Un **problema de investigación** es una tensión concreta y observable: un actor identificable sufre una dificultad en un contexto, y esa dificultad tiene consecuencias que se pueden constatar. Sin síntoma, sin actor y sin contexto no hay problema defendible: solo hay una buena intención. La primera tarea del anteproyecto es bajar del tema (el territorio) al problema (la grieta específica dentro de ese territorio que vale la pena investigar).

#### 2. Pregunta de investigación (criterio de calidad)
La pregunta traduce el problema a una forma interrogativa que guiará todo el método. Una buena pregunta es **clara** (se entiende sin explicación adicional), **delimitada** (acota actor, fenómeno y contexto), **viable** en el tiempo del programa, **ética** y **alineada a una de las dos líneas oficiales de IA**. Evite las preguntas de sí/no triviales y las preguntas planetarias tipo “¿cómo mejorar el mundo con IA?”.

| Débil | Fuerte |
| :--- | :--- |
| ¿La IA es útil en empresas? | ¿Cómo perciben los supervisores de la planta X el uso de un asistente de IA para la tarea Y en el proceso Z? |
| ¿ChatGPT ayuda a estudiar? | ¿Qué prácticas de uso de un LLM reportan estudiantes de Ingeniería en la tarea W y qué fricciones emergen? |

#### 3. Delimitación (el filtro de las cinco preguntas)
Antes de dar por buena una pregunta, respóndase mentalmente: ¿quién es el actor?, ¿dónde ocurre?, ¿qué fenómeno se observa?, ¿en qué lapso razonable?, ¿con qué acceso a información —recordando que en Proyecto I **NO** se recolecta todavía en campo—? Si alguna respuesta es “no sé” o “todo el mundo”, la pregunta aún está cruda.

#### 4. Errores frecuentes / preguntas trampa
| El estudiante dice / hace… | Usted responde… |
| :--- | :--- |
| “Voy a hacer un chatbot” (empieza por la solución) | “Guarde la solución un minuto. ¿Qué le duele hoy a alguien SIN ese chatbot? Ese dolor es su problema.” |
| Pregunta tan amplia que no cabe en el periodo | “¿Podría responderla con los recursos de un semestre? Si no, recórtela a un actor y un contexto.” |
| “¿Puedo ya lanzar la encuesta?” | “En Proyecto I diseñamos y proponemos; el campo es Proyecto II, tras el aval.” |
| Confunde objetivo con pregunta | “El objetivo empieza con verbo; la pregunta empieza con interrogante. Sepárelos.” |
| Tema fuera de las dos líneas oficiales | “Reformulemos hacia entornos productivos o hacia educación; no inventamos una tercera línea.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre + puente desde S01", 8),
        ("2️⃣ Tema ≠ problema ≠ pregunta (exposición)", 14),
        ("3️⃣ Modelación en vivo (ejemplo IA)", 12),
        ("4️⃣ Taller: borrador de problema + pregunta", 18),
        ("5️⃣ Cierre contenido", 8),
    ]
    fases_texto = f"""#### 1️⃣ Encuadre + puente desde S01 (~8 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes. **Sesión 02**. La semana pasada dejaron su ficha de encuadre con un tema tentativo y su línea de IA. Hoy damos el paso más importante del anteproyecto: convertir ese tema en un **problema** y en una **pregunta de investigación** defendibles. Al terminar la primera hora deben salir con un borrador escrito de ambos.”
> “**Slide 2 — objetivos de hoy:** primero, distinguir tema, problema y pregunta; segundo, redactar el borrador de planteamiento y la pregunta; y tercero, aprender a detectar preguntas inviables antes de enamorarse de ellas. Levanten la mano quienes ya cambiaron de tema desde la semana pasada… perfecto, es normal, para eso es esta fase.”

#### 2️⃣ Tema ≠ problema ≠ pregunta (~14 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** Tres palabras que la gente usa como sinónimos y NO lo son. **Tema** es el territorio: ‘IA en educación’. **Problema** es la tensión concreta dentro de ese territorio: ‘los docentes de tal programa tardan días en retroalimentar y los estudiantes pierden el hilo’. **Pregunta** es la forma interrogativa que va a guiar todo el método: ‘cómo…’, ‘qué factores…’, ‘en qué medida…’.”
> “Fíjense en el orden: primero identifico a quién le duele algo, después lo formulo como pregunta. Si empiezo por la pregunta sin tener el dolor claro, me sale una pregunta bonita pero hueca. Y apliquen el filtro de las cinco preguntas: quién, dónde, qué fenómeno, en qué lapso y con qué acceso a la información —sin recolectar todavía, porque estamos en Proyecto I—.”

#### 3️⃣ Modelación en vivo (ejemplo IA) (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) → 4 (RECUERDA)

**GUION LITERAL:**
> “Vamos a modelarlo juntos en pantalla, en Google Docs. Tomo un ejemplo de la línea de educación: los estudiantes entregan sus laboratorios tarde porque no reciben retroalimentación oportuna. Miren cómo lo desarmo: **(a) síntoma** —entregas tardías y errores que se repiten—; **(b) contexto** —un curso concreto de un programa concreto—; **(c) actor** —estudiantes y docente de ese curso—; **(d) pregunta delimitada** —‘¿qué prácticas de retroalimentación mediadas por un asistente de IA podrían proponerse para el curso X?’—.”
> “Y ahora lo importante: les muestro qué **NO** es la pregunta. No es ‘¿la IA es buena para educar?’ —demasiado amplia—; no es ‘¿hago un bot?’ —eso es una solución, no una pregunta—. **Slide 4, RECUERDA:** en Proyecto I la pregunta debe poder responderse MÁS ADELANTE con un diseño que ustedes proponen; hoy no salimos a encuestar a nadie.”

#### 4️⃣ Taller: borrador de problema + pregunta (~18 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Dieciocho minutos, manos a la obra en su documento de Google Docs con la plantilla APA CUN. Escriban tres cosas: **(1)** ocho a doce líneas de planteamiento del problema —síntoma, contexto y consecuencia—; **(2)** su pregunta de investigación en UNA sola frase; **(3)** la línea oficial de IA en la que encaja. Yo voy pasando por los equipos. En los últimos tres minutos, tres equipos leen en voz alta SOLO su pregunta, en veinte segundos.”
> “El criterio de éxito es sencillo: si al leer su pregunta yo identifico **actor + fenómeno + contexto**, la pregunta avanza. Si me falta alguno de los tres, seguimos puliendo.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Solo tiene la solución escrita | “Borre la app un minuto: ¿qué duele hoy sin ella? Empiece por ahí.” |
| Formula una pregunta de sí/no | “Ábrala: cambie el ‘¿es…?’ por ‘cómo’, ‘en qué medida’ o ‘qué factores’.” |
| Su tema queda fuera de las líneas | “Reformulemos hacia entornos productivos o educación; no hay tercera línea.” |
| Quiere aplicar la encuesta ya | “Hoy diseñamos; el campo es Proyecto II, con aval previo.” |

#### 5️⃣ Cierre contenido (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Tres ideas para llevarse: **problema ≠ tema**; la **pregunta se delimita** con actor, fenómeno y contexto; y **Proyecto I no es campo**. **Slide 6, para continuar:** en trabajo autónomo pulan el planteamiento y traigan tres referencias exploratorias buscadas en Google Scholar o SciELO, con su cita generada en ZoteroBib o en las citas de Google Docs. Suban el avance a CDigital con el nombre `S02_ProblemaPregunta_Apellidos`.”
> “**Slide 7.** Guardamos el documento y pasamos a la segunda hora, la tutoría por equipos, donde revisamos pregunta por pregunta.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Distinguir** tema, problema y pregunta.
2. **Redactar** borrador de planteamiento + pregunta alineada a línea oficial de IA.
3. **Detectar** preguntas inviables o centradas solo en la solución.""",
        fundamento, fases_plan, fases_texto,
        "taller problema/pregunta",
        """1. Borrador planteamiento + pregunta en CDigital (`S02_ProblemaPregunta_Apellidos`).
2. **Éxito:** pregunta con actor + fenómeno + contexto.""",
        "revisar pregunta y delimitación; bloquear intentos de aplicar instrumentos.",
    )


def guion_03(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Objetivo general vs. objetivos específicos
El **objetivo general** declara el propósito global del anteproyecto y debe reflejar, en forma afirmativa, lo mismo que pregunta la pregunta de investigación. Los **objetivos específicos** (típicamente tres) son escalones verificables que, sumados, cumplen el general. NO son actividades de clase (“buscar papers”, “reunirnos”) ni pasos administrativos: son logros de conocimiento. Un buen específico se puede “tachar” el día que se cumpla en Proyecto II.

Verbos útiles (medibles): analizar, caracterizar, identificar, diseñar (una propuesta), contrastar, proponer. Verbos prohibidos (no observables): conocer, aprender, entender, interesarse, concientizar.

#### 2. Justificación
Responde a la pregunta “¿por qué vale la pena?”. Se apoya en tres pilares: (a) un **vacío** de conocimiento o de práctica; (b) la **relevancia** para el contexto y para el actor; (c) la **pertinencia** frente a la línea de IA del programa. La justificación argumenta el aporte ESPERABLE del anteproyecto —nunca resultados ya obtenidos, porque no se ha ejecutado nada—.

#### 3. Alcances y limitaciones
El **alcance** es la promesa: hasta dónde llega el estudio (población objetivo, periodo, variables o categorías, tipo de producto). La **limitación** es la honestidad: restricciones reales de acceso, de tiempo, de recursos, y la restricción estructural de que en Proyecto I no se aplican instrumentos. Declarar limitaciones no debilita el trabajo: lo hace creíble.

#### 4. Coherencia como hilo (cierre de ACA1)
Al terminar esta unidad, el bloque de formulación debe leerse como una sola historia sin saltos: problema → pregunta → objetivo general → específicos → justificación → alcances/limitaciones. Ese hilo es exactamente lo que se evalúa en ACA1.

#### 5. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Escribe específicos como tareas (“leer autores”) | “Eso es una actividad, no un objetivo. ¿Qué CONOCIMIENTO produce ese paso?” |
| Usa “conocer” o “entender” | “Cámbielo por un verbo que yo pueda verificar: analizar, caracterizar, proponer.” |
| Justifica con autobiografía (“me gusta la IA”) | “Su gusto no es argumento. ¿Qué vacío o necesidad del contexto lo justifica?” |
| Confunde alcance con limitación | “El alcance es lo que SÍ hará; la limitación es lo que NO podrá. Sepárelos en dos listas.” |
| Tiene objetivos que no responden la pregunta | “Léame la pregunta y luego el general: ¿dicen lo mismo? Si no, algo sobra.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre + revisión rápida de preguntas", 8),
        ("2️⃣ Objetivos y verbos (exposición)", 12),
        ("3️⃣ Justificación · alcances · limitaciones", 12),
        ("4️⃣ Taller de redacción", 20),
        ("5️⃣ Cierre", 8),
    ]
    fases_texto = f"""#### 1️⃣ Encuadre + revisión rápida de preguntas (~8 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 03**. Antes de arrancar: si su pregunta de S02 cambió durante la semana, es normal —actualícenla ahora en su documento, porque todo lo de hoy cuelga de esa pregunta—. Dos o tres equipos, díganme en una frase su pregunta actual.”
> “**Slide 2.** Hoy cerramos el bloque de formulación: **objetivos, justificación, alcances y limitaciones**. Cuando salgan de la primera hora, tendrán casi listo lo que compone la entrega de ACA1.”

#### 2️⃣ Objetivos y verbos (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** El objetivo general es el propósito: dice lo mismo que la pregunta, pero en afirmativo y empezando por un verbo. Los específicos son los escalones —normalmente tres— que, al subirlos todos, me dejan arriba del general.”
> “Regla de oro de los verbos: si el verbo no lo puedo VER cumplirse, no sirve. ‘Conocer’, ‘aprender’, ‘entender’ no se ven. ‘Analizar’, ‘caracterizar’, ‘diseñar una propuesta’, ‘contrastar’ sí. Miren cómo modelo un general y tres específicos a partir de esta pregunta de ejemplo en pantalla… y fíjense que cada específico se puede tachar el día que se cumpla.”

#### 3️⃣ Justificación · alcances · limitaciones (~12 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “**Slide 4.** La justificación NO es autobiografía. ‘Me gusta la IA’ no justifica nada. Justificar es responder por qué vale la pena: qué vacío llena, a quién le sirve, y por qué encaja en la línea del programa.”
> “Y las dos fronteras: el **alcance** es lo que SÍ voy a hacer —población, periodo, variables—; la **limitación** es lo que NO puedo —acceso, tiempo, y la grande: en Proyecto I no hay trabajo de campo—. Declarar limitaciones no los hace ver flojos; los hace ver serios.”

#### 4️⃣ Taller de redacción (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos en su documento de Google Docs. Redacten: el objetivo general, tres específicos, media a una página de justificación, y los alcances y limitaciones en viñetas. Yo circulo por los equipos. Criterio de éxito: cada objetivo específico debe poder ‘tacharse’ cuando se cumpla en Proyecto II, y el general debe sonar como la pregunta puesta en afirmativo.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe específicos como actividades | “Eso es una tarea. ¿Qué conocimiento produce? Reescríbalo con verbo de logro.” |
| Usa ‘conocer’, ‘entender’ | “Cámbielo por un verbo verificable: analizar, caracterizar, proponer.” |
| Justifica con gustos personales | “¿Qué necesidad del contexto lo respalda? Eso es la justificación.” |
| Mezcla alcance y limitación | “Dos listas: lo que SÍ hará y lo que NO podrá. Sepárelas.” |

#### 5️⃣ Cierre (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** En autónomo, empaqueten el bloque completo de formulación para la entrega de ACA1 siguiendo las indicaciones de CDigital: problema, pregunta, objetivos, justificación, alcances y limitaciones, con sus referencias en APA 7. Suban el avance de clase como `S03_ObjetivosJustificacion_Apellidos`.”
> “**Slide 7.** Recuerden que ACA1 es la primera de las tres entregas del mismo documento acumulativo; no es una tarea suelta. Pasamos a tutoría para revisar la coherencia pregunta–objetivos equipo por equipo.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Redactar** objetivo general y específicos coherentes con la pregunta.
2. **Argumentar** justificación y delimitar alcances/limitaciones.
3. **Integrar** el bloque de formulación del anteproyecto.""",
        fundamento, fases_plan, fases_texto, "objetivos",
        """1. Sección objetivos + justificación + alcances/limitaciones en CDigital.
2. **Éxito:** específicos con verbo preciso y alineados a la pregunta.""",
        "coherencia pregunta–objetivos; preparar cierre de bloque formulación (ACA1).",
    )


def guion_04(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Cómo dar retroalimentación de ACA1 (en 60+60)
Priorice dos cosas: **coherencia** (¿pregunta ↔ objetivos ↔ justificación cuentan la misma historia?) y **viabilidad**. No reescriba el texto del estudiante ni corrija comas: señale dos o tres hallazgos accionables por equipo, redactados como instrucción concreta (“delimite el actor”, “el específico 2 no responde la pregunta”). La retro es un mapa de ruta, no una calificación disfrazada.

#### 2. Qué es un antecedente de investigación (y qué no)
Un **antecedente** es un ESTUDIO PREVIO comparable —una investigación con autor, año, objetivo, método y hallazgos— que muestra qué se ha investigado ya sobre el fenómeno. NO es una noticia, un blog ni una definición de diccionario. La meta orientativa del programa es **mínimo 6**, con presencia nacional e internacional. Cada antecedente se ficha con: propósito, método, hallazgo clave y —lo más importante— **su relación explícita con la pregunta propia**.

#### 3. Dónde buscar (gratis y en la nube)
Google Scholar, SciELO, Redalyc y la biblioteca virtual CUN. Para la cita, un gestor ligero en la nube: **ZoteroBib** (zbib.org) o las citas integradas de Google Docs. No se exige instalar Mendeley ni Zotero de escritorio; todo puede hacerse desde el navegador.

#### 4. La diferencia con el marco teórico (viene en S05)
Antecedentes = qué se INVESTIGÓ (estudios). Marco teórico = con qué LENTES conceptuales se explica el fenómeno (teorías y constructos). Hoy trabajamos lo primero; no adelanten teoría.

#### 5. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Trae una noticia o un blog como antecedente | “Eso no es investigación. Búsqueme un estudio con método y hallazgos en Scholar o SciELO.” |
| Lista papers sin decir qué aportan | “Cada ficha cierra con ‘esto le sirve a mi pregunta porque…’. Sin esa frase, es decoración.” |
| Solo trae fuentes internacionales (o solo nacionales) | “Equilibre: el programa pide nacionales E internacionales.” |
| Copia el resumen del paper tal cual | “Resuma con SUS palabras: propósito, método, hallazgo. El copiar-pegar es riesgo de similitud.” |
| Confunde antecedente con teoría | “El antecedente es un estudio; la teoría llega en la próxima sesión. Hoy, estudios.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre + criterios de retro ACA1", 10),
        ("2️⃣ Qué es un antecedente (y qué no)", 12),
        ("3️⃣ Modelación de ficha de antecedente", 10),
        ("4️⃣ Taller de búsqueda y fichas", 20),
        ("5️⃣ Cierre", 8),
    ]
    fases_texto = f"""#### 1️⃣ Encuadre + criterios de retro ACA1 (~10 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 04**. Ya cerró ACA1. Hoy hago dos cosas: primero les explico con qué criterios la leí, y segundo abrimos el marco referencial empezando por los **antecedentes**.”
> “**Slide 2.** Los criterios de mi retro son tres: coherencia (que pregunta, objetivos y justificación digan lo mismo), delimitación (actor, fenómeno, contexto) y APA básica. Cuando lean mis comentarios, léanlos como un mapa de correcciones, no como un regaño: cada observación es una instrucción concreta para mejorar el documento acumulativo.”

#### 2️⃣ Qué es un antecedente (y qué no) (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** Un antecedente es una investigación PREVIA comparable a la suya: tiene autor, año, objetivo, método y hallazgos. Una noticia no es antecedente; un blog no es antecedente; una definición de Wikipedia no es antecedente.”
> “Necesitan mínimo seis, mezclando estudios nacionales e internacionales. Y ojo con esto, que es lo que más se olvida: cada antecedente TIENE que cerrar diciendo ‘esto le aporta a mi pregunta porque…’. Si no puedo conectar el estudio con mi problema, no lo pongo. Y no confundan esto con el marco teórico: hoy son estudios; los lentes conceptuales llegan la próxima sesión.”

#### 3️⃣ Modelación de ficha de antecedente (~10 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “Miren cómo lleno una ficha en pantalla, en Google Docs. Tomo un estudio real de Scholar y completo: autor y año, objetivo del estudio, método que usaron, hallazgo principal, y el vínculo con nuestra pregunta de ejemplo. Cinco casillas, ni una más.”
> “**Slide 4, recuerda:** la cita la genero en ZoteroBib pegando el DOI o el enlace, y la pego en APA 7. No necesitan instalar nada; todo desde el navegador.”

#### 4️⃣ Taller de búsqueda y fichas (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos. Busquen en Google Scholar o SciELO y consigan hoy al menos DOS antecedentes —van rumbo a los seis—. Llenen la ficha de cada uno en su documento, peguen el DOI o la URL, y generen la cita APA con ZoteroBib. Yo paso resolviendo dudas de búsqueda y de vínculo con la pregunta.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Trae una noticia como antecedente | “Necesito un estudio con método y resultados, no una nota de prensa.” |
| No conecta el paper con su pregunta | “Añada la frase: ‘esto le sirve a mi pregunta porque…’.” |
| No encuentra nada en Scholar | “Cambie los términos de búsqueda; pruebe sinónimos y en inglés.” |
| Copia el abstract literal | “Resúmalo con sus palabras; el copiar-pegar dispara la similitud.” |

#### 5️⃣ Cierre (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** En autónomo, completen las seis fichas mínimas y, en paralelo, vayan aplicando las correcciones de mi retro de ACA1 sobre el documento. Suban el avance como `S04_Antecedentes_Apellidos`.”
> “**Slide 7.** Recuerden: ACA2 acumula sobre ACA1, así que las correcciones no son opcionales. Pasamos a tutoría para revisar una o dos fichas por equipo.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Aplicar** criterios de retroalimentación al bloque de formulación.
2. **Elaborar** fichas de antecedentes (ruta a mín. 6).
3. **Usar** bases abiertas y citación APA vía ZoteroBib/Docs.""",
        fundamento, fases_plan, fases_texto, "antecedentes",
        """1. Avance de fichas de antecedentes en CDigital.
2. **Éxito:** cada ficha incluye vínculo explícito a la pregunta.""",
        "retro puntual ACA1 + revisar 1–2 fichas de antecedentes por equipo.",
    )


def guion_05(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Marco teórico ≠ resumen de libros
El marco teórico articula las **teorías, modelos y constructos** que sostienen la pregunta y que dan sentido a las categorías o variables del estudio. No es encadenar definiciones de Wikipedia ni copiar capítulos: es elegir los lentes conceptuales con los que se va a mirar el fenómeno y justificar por qué esos y no otros.

#### 2. El hilo de coherencia
El orden lógico es: pregunta → conceptos clave que la pregunta obliga a definir → autores que los definen u operacionalizan → relación con el contexto de aplicación (IA productiva o educativa). Si un concepto no cuelga de la pregunta, sobra; si un autor no aporta al concepto, sobra.

#### 3. Extensión y calidad
Prime la profundidad sobre la acumulación: dos a cuatro constructos bien hilados valen más que quince citas decorativas. La pregunta de control es: “¿este párrafo afirma algo que después el método podrá ‘tocar’?”. Si la teoría no reaparece en la metodología, quedó suelta.

#### 4. Antecedentes vs. teoría (la confusión más común)
Antecedentes (S04) = estudios previos. Marco teórico (hoy) = andamiaje conceptual. Un mismo autor puede aparecer en ambos, pero con función distinta: como estudio comparable en antecedentes, como definidor de un constructo en el teórico.

#### 5. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Copia definiciones encadenadas de la web | “¿Cuál de esos conceptos exige SU pregunta? Empiece por ahí, no por el diccionario.” |
| Mete teoría que nunca usa en el método | “Si no la va a ‘tocar’ con el método, quítela: es peso muerto.” |
| Confunde antecedentes con teoría | “El antecedente es un estudio; el constructo es un lente. ¿Qué función cumple aquí?” |
| Pone 15 citas para ‘verse riguroso’ | “Prefiero tres constructos bien hilados que quince citas sueltas.” |
| No cita al definir un constructo | “Toda definición operativa va con su autor y año en APA 7.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Qué es marco teórico (exposición)", 14),
        ("3️⃣ Modelación: mapa de constructos", 12),
        ("4️⃣ Taller: mapa + primer apartado", 20),
        ("5️⃣ Cierre", 8),
    ]
    fases_texto = """#### 1️⃣ Encuadre (~6 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 05**. La semana pasada trabajamos antecedentes: qué se ha INVESTIGADO. Hoy subimos un piso: el **marco teórico**, es decir, con qué LENTES conceptuales vamos a explicar el fenómeno.”
> “**Slide 2.** Meta de hoy: diferenciar antecedentes de teoría, mapear los constructos que su pregunta obliga a definir, y dejar escrito un primer apartado teórico usable.”

#### 2️⃣ Qué es marco teórico (~14 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** El marco teórico NO es un resumen de libros ni una fila de definiciones de Google. Es elegir las teorías y constructos que sostienen su pregunta y decir por qué esos. El orden es siempre el mismo: parto de la pregunta, veo qué conceptos me obliga a definir, busco los autores que los definen bien, y los conecto con mi contexto de IA.”
> “Hagan este ejercicio mental ahora: escriban los tres conceptos que su pregunta les obliga a definir sí o sí. Esos tres son la semilla de su marco teórico. Si un concepto no cuelga de la pregunta, sobra.”

#### 3️⃣ Modelación: mapa de constructos (~12 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “Vamos a dibujarlo. Abro Excalidraw —es gratis y en el navegador— y pongo la pregunta en el centro. De ahí salen flechas a los constructos; de cada constructo, una flecha al autor que lo define. Miren cómo el mapa me obliga a botar lo que no conecta.”
> “**Slide 4, recuerda:** cada definición que ponga en el texto va citada en APA 7, y cada constructo del mapa debe reaparecer después en la metodología. La teoría que no se usa, se cae.”

#### 4️⃣ Taller: mapa + primer apartado (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos. Produzcan dos entregables: primero, el mapa de constructos en Excalidraw (pregunta al centro, constructos, autores); segundo, una a dos páginas del primer apartado teórico en su documento de Google Docs. Yo circulo. Criterio de éxito: cada párrafo del apartado afirma algo que el método podrá ‘tocar’ más adelante.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Copia definiciones de la web encadenadas | “¿Cuál concepto exige su pregunta? Arranque por ahí, con autor.” |
| Escribe teoría que no usará | “Si el método no la va a tocar, quítela.” |
| No sabe qué constructos elegir | “Lea su pregunta en voz alta y subraye los sustantivos clave: esos son.” |
| No cita a los autores | “Cada definición operativa lleva su cita APA 7.” |

#### 5️⃣ Cierre (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** En autónomo, completen el apartado teórico a partir del mapa y traigan a la Sesión 06 definiciones operativas tentativas de sus términos. Suban el avance como `S05_MarcoTeorico_Apellidos`.”
> “**Slide 7.** Recuerden que todo esto acumula hacia ACA2. Pasamos a tutoría: revisamos el mapa de cada equipo y cortamos la teoría ornamental.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Diferenciar** antecedentes y marco teórico.
2. **Mapear** constructos alineados a la pregunta.
3. **Redactar** un avance teórico usable.""",
        fundamento, fases_plan, fases_texto, "marco teórico",
        """1. Mapa de constructos + avance de marco teórico en CDigital.
2. **Éxito:** constructos trazables a la pregunta.""",
        "revisar mapa teórico; cortar teoría ornamental.",
    )


def guion_06(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Marco conceptual
Es el **diccionario operativo** del estudio: cómo se entenderán, EN ESTE trabajo, los términos clave (“adopción”, “desempeño”, “retroalimentación”, “usabilidad”…). No es la definición general del término, sino la definición con la que USTED va a trabajar y medir. Un buen marco conceptual evita que dos lectores entiendan cosas distintas por la misma palabra.

#### 2. Marco contextual
Describe **dónde** ocurre el fenómeno con precisión: la organización, el nivel educativo, el proceso, el territorio, las restricciones reales. Evite el contexto de relleno panorámico (“en Colombia la IA crece…”); eso no es contexto, es titular. El contexto útil es el que después el método necesita para tener sentido.

#### 3. Cómo se conectan con lo anterior
El marco conceptual **baja a tierra** el marco teórico (traduce constructos abstractos a definiciones utilizables); el marco contextual **fija el escenario** de aplicación —siempre recordando que en Proyecto I ese escenario se describe, no se interviene todavía—.

#### 4. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Copia la definición general del término | “No quiero la del diccionario; quiero cómo la va a usar USTED en su estudio.” |
| Deja términos ambiguos sin definir | “Si dos lectores lo entienden distinto, defínalo. ¿Qué es ‘adopción’ aquí?” |
| Escribe contexto panorámico (‘en el mundo…’) | “Bájelo al ‘dónde’ concreto: qué organización, qué aula, qué proceso.” |
| Confunde conceptual con teórico | “El teórico explica; el conceptual define para usar. Aquí, definiciones operativas.” |
| Describe un contexto que el método no usará | “Si el método no lo necesita, sobra. El contexto sirve al método.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Conceptual vs contextual", 14),
        ("3️⃣ Modelación", 10),
        ("4️⃣ Taller de definiciones y contexto", 22),
        ("5️⃣ Cierre", 8),
    ]
    fases_texto = """#### 1️⃣ Encuadre (~6 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 06**. Ya tienen antecedentes y el arranque del marco teórico. Hoy cerramos casi todo el marco referencial con dos piezas: el **marco conceptual** y el **marco contextual**.”
> “**Slide 2.** Al final de la hora deben tener una tabla de definiciones operativas y una descripción precisa del contexto donde vive su problema.”

#### 2️⃣ Conceptual vs. contextual (~14 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** El marco conceptual es el diccionario de SU estudio: no la definición general de ‘retroalimentación’, sino cómo VAN A ENTENDER ‘retroalimentación’ ustedes, en este trabajo, para poder medirla después. Si dejan un término ambiguo, dos lectores entenderán cosas distintas y el método se les cae.”
> “El marco contextual es el ‘dónde’ real: qué organización, qué aula, qué proceso, qué restricciones. Ojo: ‘en Colombia la IA crece’ NO es contexto, es titular de periódico. El contexto que sirve es el que el método va a necesitar.”

#### 3️⃣ Modelación (~10 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “Miren la tabla que armo en pantalla, en Google Docs. Cuatro columnas: Término | Definición teórica breve | Definición operativa (cómo la uso yo) | Por qué le importa a la pregunta. Lleno una fila de ejemplo con ‘retroalimentación’.”
> “**Slide 4, recuerda:** el conceptual baja a tierra el teórico de la semana pasada, y el contextual fija el escenario —que en Proyecto I describimos, no intervenimos—.”

#### 4️⃣ Taller de definiciones y contexto (~22 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veintidós minutos. Completen la tabla con cuatro a seis términos operativos y redacten una página de contexto: la organización, el aula o el proceso donde ocurre su fenómeno, con sus restricciones reales. Yo circulo. Criterio de éxito: los términos no deben admitir dos interpretaciones, y el contexto debe ser algo que el método pueda usar. Suban como `S06_ConceptualContextual_Apellidos`.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Copia la definición del diccionario | “Quiero cómo la usará USTED, no la general.” |
| Deja un término ambiguo | “¿Qué es exactamente ‘adopción’ aquí? Defínalo para poder medirlo.” |
| Escribe contexto panorámico | “Bájelo al dónde concreto: qué organización, qué proceso.” |
| Da contexto que no usará | “Si el método no lo necesita, recórtelo.” |

#### 5️⃣ Cierre (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** En autónomo, terminen la tabla conceptual y el texto contextual, y guarden todo en el documento acumulativo. Suban el avance como `S06_ConceptualContextual_Apellidos`.”
> “**Slide 7.** La próxima sesión cerramos el marco referencial con el marco legal —si aplica— y una clínica de citación APA 7. Pasamos a tutoría para afinar definiciones.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Redactar** definiciones operativas.
2. **Describir** el contexto de aplicación con precisión.
3. **Conectar** conceptual/contextual con la pregunta.""",
        fundamento, fases_plan, fases_texto, "conceptual/contextual",
        """1. Tabla conceptual + texto contextual en CDigital.
2. **Éxito:** términos operativos no ambiguos.""",
        "afinar definiciones; contextualizar sin relleno panorámico.",
    )


def guion_07(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Marco legal (solo si aplica)
Son las normas, políticas o marcos que **condicionan** el estudio: protección de datos personales (en Colombia, la Ley 1581 de 2012 y su normativa), propiedad intelectual, y políticas de uso de IA. Si el anteproyecto trata datos personales, menores de edad o información propiedad de una empresa, el marco legal es obligatorio. Si el estudio es solo un diseño metodológico sin datos sensibles, se declara honestamente que no aplica —pero NO se inventan leyes para “rellenar”—.

#### 2. APA 7 — lo que más se rompe
- Confundir la **cita en el texto** con la **referencia** de la lista final: toda cita del cuerpo debe tener su referencia, y toda referencia debe estar citada al menos una vez (nada de “bibliografía huérfana”).
- Faltar el **DOI o la URL** en fuentes que lo tienen.
- Cita **narrativa** (Pérez, 2021, afirma que…) vs. cita **parentética** (…IA generativa (Pérez, 2021)).
- Ordenar mal la lista de referencias (es alfabética, con sangría francesa).

#### 3. Herramientas permitidas (en la nube)
ZoteroBib (zbib.org), las citas integradas de Google Docs, y la plantilla APA CUN en Google Docs o Word en línea. No se exige ningún plugin de escritorio.

#### 4. Cierre del marco referencial
Esta sesión cierra el bloque que compone ACA2: antecedentes, teórico, conceptual, contextual y legal, con referencias limpias. La meta mínima: cero citas huérfanas en el avance.

#### 5. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Inventa un marco legal para ‘rellenar’ | “Si no toca datos sensibles, DECLARE que no aplica; no inventamos leyes.” |
| Tiene referencias que no citó en el texto | “Bibliografía huérfana: o la cita en el cuerpo, o la quita de la lista.” |
| Citó algo que no está en referencias | “Toda cita necesita su referencia completa. Complétela con ZoteroBib.” |
| No sabe si su cita es narrativa o parentética | “¿El autor va DENTRO de la frase o entre paréntesis al final? Eso decide el formato.” |
| Trata datos de menores sin mencionarlo | “Eso exige marco legal sí o sí: protección de datos. No lo omita.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Marco legal pertinente", 12),
        ("3️⃣ Clínica APA 7", 14),
        ("4️⃣ Taller de limpieza bibliográfica", 20),
        ("5️⃣ Cierre bloque referencial", 8),
    ]
    fases_texto = f"""#### 1️⃣ Encuadre (~6 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 07**. Hoy cerramos el marco referencial completo, que es el corazón de ACA2. Dos frentes: el **marco legal** —si su proyecto lo necesita— y una **clínica de APA 7** para dejar las citas impecables.”
> “**Slide 2.** Meta de hoy: decidir si aplica marco legal y redactarlo con pertinencia, y normalizar todas sus citas y referencias sin citas huérfanas.”

#### 2️⃣ Marco legal pertinente (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** Pregunta clave: ¿su estudio toca datos personales, menores de edad o información propiedad de una empresa? Si la respuesta es sí, el marco legal es obligatorio —en Colombia, la protección de datos de la Ley 1581 de 2012, propiedad intelectual y políticas de uso de IA—.”
> “Si su estudio es solo un diseño metodológico sin datos sensibles, no pasa nada: lo DECLARAN honestamente, ‘no aplica marco legal porque…’. Lo que NO se hace es inventar leyes para rellenar; eso lo detecto de inmediato.”

#### 3️⃣ Clínica APA 7 (~14 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “**Slide 4.** Vamos a corregir en vivo tres errores típicos que pego en el chat. Primero, una cita narrativa —el autor va dentro de la frase: ‘Pérez (2021) afirma que…’—. Segundo, una parentética —el autor va al final entre paréntesis—. Tercero, una referencia completa con su DOI.”
> “Y la regla de oro de APA que más se rompe: toda cita del cuerpo tiene que estar en la lista de referencias, y toda referencia tiene que estar citada al menos una vez. Si sobra una referencia sin cita, es bibliografía huérfana y hay que quitarla.”

#### 4️⃣ Taller de limpieza bibliográfica (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos. Limpien las referencias de su documento con ZoteroBib o con las citas de Google Docs. Hagan la verificación cruzada: cada cita del cuerpo debe estar en la lista, y cada referencia debe estar citada. Y redacten el marco legal —o su declaración de no aplicabilidad—. Yo circulo. Suban como `S07_LegalAPA_Apellidos`.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Inventa leyes para rellenar | “Si no aplica, declárelo; no invente normativa.” |
| Tiene referencias sin citar | “Cítela en el texto o quítela: nada huérfano.” |
| No pone DOI/URL | “Si la fuente lo tiene, va. ZoteroBib lo trae solo.” |
| Mezcla estilos de cita | “Decida: ¿autor dentro de la frase o al final? Uniforme.” |

#### 5️⃣ Cierre bloque referencial (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** Con esto queda listo el marco referencial completo para ACA2: antecedentes, teórico, conceptual, contextual y legal, con referencias limpias. En autónomo, integren las correcciones y dejen cero citas huérfanas.”
> “**Slide 7.** La próxima sesión damos un salto: empezamos el **diseño metodológico** —paradigma, enfoque y alcance— para adelantar antes de los festivos de ACA3. Pasamos a tutoría para revisar APA y pertinencia legal equipo por equipo.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Valorar** si aplica marco legal y redactarlo con pertinencia.
2. **Normalizar** citas/referencias APA 7.
3. **Cerrar** el bloque referencial con bibliografía coherente.""",
        fundamento, fases_plan, fases_texto, "APA/legal",
        """1. Sección legal (o justificación de no aplicabilidad) + referencias limpias.
2. **Éxito:** 0 citas huérfanas evidentes en el avance.""",
        "revisar APA y pertinencia legal; checklist de cierre referencial.",
    )


def guion_08(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Paradigma, enfoque y alcance (vocabulario mínimo)
- **Paradigma:** la postura sobre cómo se conoce (positivista/pospositivista, interpretativo o mixto). Marca el “para qué” del conocimiento.
- **Enfoque:** cuantitativo, cualitativo o mixto. Debe CONVERSAR con la pregunta: si la pregunta busca magnitudes, es cuantitativo; si busca significados y experiencias, cualitativo; si busca ambos, mixto justificado.
- **Alcance:** exploratorio, descriptivo, correlacional o explicativo (según Hernández-Sampieri, texto guía del curso).
- **Diseño:** el esbozo de cómo se obtendrían las evidencias —que en Proyecto I solo se PROPONE, no se ejecuta—.

#### 2. La coherencia de oro
El error más caro es el desajuste pregunta–método. Una pregunta que busca comprender significados (“¿cómo VIVEN los docentes…?”) con una encuesta de escalas cerradas está rota; y una pregunta que busca magnitudes (“¿en qué MEDIDA…?”) con tres entrevistas también. El enfoque no se elige por gusto: se deriva de la pregunta.

#### 3. Por qué se adelanta aquí (sesión puente)
Esta sesión anticipa la metodología antes de las semanas más cargadas de ACA3, que por los festivos tienen solo dos lunes sincrónicos. Adelantar hoy da colchón para las tutorías extra de esas semanas.

#### 4. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Elige el enfoque ‘porque me gusta’ | “El enfoque se DERIVA de la pregunta, no del gusto. Léame su pregunta.” |
| Pregunta cualitativa con encuesta de escalas | “Si busca significados, entreviste; la escala mide magnitudes.” |
| Confunde enfoque con alcance | “Enfoque = cuali/cuanti/mixto; alcance = exploratorio/descriptivo/… Son ejes distintos.” |
| Quiere aplicar el instrumento ‘para probar’ | “En Proyecto I se PROPONE el diseño; aplicar es Proyecto II.” |
| Dice ‘mixto’ sin justificarlo | “Mixto exige justificar por qué necesita las dos rutas. ¿Por qué?” |
"""
    fases_plan = [
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Enfoque y alcance", 14),
        ("3️⃣ Modelación de coherencia pregunta–método", 12),
        ("4️⃣ Taller: ficha metodológica", 20),
        ("5️⃣ Cierre", 8),
    ]
    fases_texto = """#### 1️⃣ Encuadre (~6 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 08**. Cerramos el marco referencial y hoy damos el salto al **diseño metodológico**. Adelantamos a propósito, porque las semanas de ACA3 tienen menos lunes por los festivos.”
> “**Slide 2.** Hoy eligen el ‘cómo’ tentativo de su investigación: paradigma, enfoque y alcance. Insisto en ‘tentativo’ y en ‘propuesto’: hoy no aplicamos absolutamente nada.”

#### 2️⃣ Enfoque y alcance (~14 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** El **enfoque** es cuantitativo, cualitativo o mixto, y NO se elige por gusto: se deriva de la pregunta. Si su pregunta busca magnitudes —‘en qué medida’, ‘cuánto’—, es cuantitativo. Si busca significados y experiencias —‘cómo viven’, ‘qué sentido le dan’—, es cualitativo. Si necesita ambas, mixto, pero justificado.”
> “El **alcance** es otro eje: exploratorio, descriptivo, correlacional o explicativo, siguiendo a Hernández-Sampieri, que es el texto guía. No confundan enfoque con alcance: son dos preguntas distintas sobre su método.”

#### 3️⃣ Modelación de coherencia pregunta–método (~12 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “Armo en pantalla una matriz de coherencia, en Google Docs: Pregunta | Enfoque | Alcance | Técnica tentativa | Por qué es coherente. La lleno con una pregunta de ejemplo y les muestro cómo, si cambio la pregunta, cambia toda la fila.”
> “**Slide 4, recuerda:** el diseño en Proyecto I se PROPONE; el instrumento no se aplica ni ‘para probar’. Esa frontera es lo que evalúo con más rigor.”

#### 4️⃣ Taller: ficha metodológica (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos. Completen la matriz para SU proyecto: su pregunta, el enfoque que se deriva de ella, el alcance, la técnica tentativa y —la casilla más importante— por qué es coherente. Yo circulo por los equipos. Suban como `S08_DisenoMetodologico_Apellidos`.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Elige enfoque por gusto | “Derívelo de la pregunta; léamela otra vez.” |
| Pregunta cualitativa con encuesta | “Si busca significados, entreviste, no encueste.” |
| Confunde enfoque y alcance | “Enfoque = cuali/cuanti; alcance = descriptivo/… Dos ejes.” |
| Dice ‘mixto’ sin razón | “Justifique por qué necesita las dos rutas.” |

#### 5️⃣ Cierre (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** En autónomo, dejen la ficha metodológica con la justificación de coherencia bien redactada. Suban `S08_DisenoMetodologico_Apellidos`.”
> “**Slide 7.** La próxima sesión concretamos población, muestra y los instrumentos —siempre PROPUESTOS—. Pasamos a tutoría para validar la coherencia pregunta–enfoque de cada equipo.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Seleccionar** enfoque y alcance coherentes con la pregunta.
2. **Justificar** el diseño propuesto (sin aplicar).
3. **Dejar** ficha metodológica inicial.""",
        fundamento, fases_plan, fases_texto, "diseño metodológico",
        """1. Ficha paradigma/enfoque/alcance/diseño en CDigital.
2. **Éxito:** justificación explícita de coherencia con la pregunta.""",
        "validar coherencia pregunta–enfoque; anticipar técnicas.",
    )


def guion_09(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = f"""#### 1. Población y muestra (propuestas)
La **población** es el conjunto total de unidades de estudio (personas, procesos, documentos) que interesan; la **muestra** es el subconjunto que efectivamente se estudiaría, con sus **criterios de inclusión y exclusión** y su forma de selección (probabilística o no). En Proyecto I se DEFINE quiénes serían y cómo se elegirían —no se contacta a nadie para recolectar—.

#### 2. Técnicas e instrumentos **propuestos**
La **técnica** es el procedimiento (encuesta, entrevista, observación, análisis de logs/documentos); el **instrumento** es la herramienta concreta (el cuestionario, la guía de entrevista, la rúbrica). Cada instrumento propuesto debe declarar: propósito, estructura (bloques o ítems tipo), validez tentativa (cómo se validaría) y plan de análisis. Todo en condicional: se PROPONE, no se aplica.

#### 3. Alineación con los objetivos
Cada bloque del instrumento debe colgar de un objetivo específico o de una categoría/variable. Si un ítem no responde a ningún objetivo, sobra; si un objetivo no tiene ítems que lo alimenten, falta instrumento.

#### 4. Recordatorio institucional
La slide RECUERDA y el Manual son claros: en Proyecto I los instrumentos son PROPUESTOS. En la tutoría, el estudiante diligencia su formulario de asistencia: {LINK_TUTORIAS}.

#### 5. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Ya envió un formulario ‘de prueba’ a gente | “Eso no es avance de Proyecto I, es riesgo. Retírelo: hoy PROPONEMOS.” |
| Confunde población con muestra | “Población = el total; muestra = a quiénes estudiaría. ¿Cuál es cuál en su caso?” |
| Ítems que no responden a ningún objetivo | “¿A qué objetivo alimenta este ítem? Si a ninguno, quítelo.” |
| No define criterios de inclusión | “¿Quién SÍ entra y quién NO? Sin criterios, la muestra es un deseo.” |
| Redacta el instrumento en pasado (‘apliqué’) | “En condicional: ‘se aplicaría’. En Proyecto I se propone.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre + regla de oro P-I", 8),
        ("2️⃣ Población / muestra", 12),
        ("3️⃣ Técnicas e instrumentos propuestos", 12),
        ("4️⃣ Taller: bosquejo de instrumento", 20),
        ("5️⃣ Cierre", 8),
    ]
    fases_texto = f"""#### 1️⃣ Encuadre + regla de oro P-I (~8 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 09**. Empiezo con la regla de oro de hoy, porque es la que más se rompe: si alguien ya mandó un Google Form ‘de prueba’ a cuarenta personas, eso NO es avance de Proyecto I, es un riesgo —recolectó sin aval—. Hoy PROPONEMOS instrumentos; no aplicamos.”
> “**Slide 2.** Meta de hoy: definir población y muestra propuestas, y bosquejar el instrumento alineado a sus objetivos. Todo en condicional.”

#### 2️⃣ Población / muestra (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** Población no es lo mismo que muestra. La **población** es el total de unidades que me interesan; la **muestra** es a quiénes efectivamente estudiaría. Y la muestra necesita criterios: quién SÍ entra —inclusión— y quién NO —exclusión—, y cómo los seleccionaría.”
> “Recuerden: en Proyecto I definimos quiénes serían y cómo se elegirían, pero no contactamos a nadie para recolectar. Eso es Proyecto II, con aval.”

#### 3️⃣ Técnicas e instrumentos propuestos (~12 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “**Slide 4.** La técnica es el procedimiento —encuesta, entrevista, observación, análisis de documentos—; el instrumento es la herramienta concreta —el cuestionario, la guía, la rúbrica—. Cada instrumento propuesto declara cuatro cosas: propósito, estructura por bloques, cómo se validaría, y el plan de análisis.”
> “Y la alineación de oro: cada bloque del instrumento cuelga de un objetivo específico. Si un ítem no responde a ningún objetivo, sobra. Recuerden diligenciar su formulario de asistencia cuando estén en tutoría.”

#### 4️⃣ Taller: bosquejo de instrumento (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos. Bosquejen su instrumento: si es encuesta, diez a quince ítems; si es entrevista, una guía de ocho preguntas. Añadan un párrafo de plan de análisis. Y al lado de cada bloque, escriban a qué objetivo responde. Redacten todo en condicional. Yo circulo. Suban como `S09_InstrumentosPropuestos_Apellidos`.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Ya aplicó el instrumento | “Retírelo: en Proyecto I se propone. Aplicar es Proyecto II.” |
| Confunde población y muestra | “Población = total; muestra = a quiénes estudia. Sepárelas.” |
| Tiene ítems sueltos | “¿A qué objetivo responde este ítem? Si a ninguno, fuera.” |
| No define inclusión/exclusión | “¿Quién entra y quién no? Escriba los criterios.” |

#### 5️⃣ Cierre (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** En autónomo, completen el instrumento y dejen explícito, por escrito, que es una PROPUESTA para Proyecto II. Suban `S09_InstrumentosPropuestos_Apellidos`.”
> “**Slide 7.** La próxima sesión integramos todo: cronograma, viabilidad y el ensamble del anteproyecto para ACA3. Pasamos a tutoría; reviso instrumentos y freno cualquier aplicación prematura.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Definir** población/muestra propuestas.
2. **Bosquejar** instrumentos sin aplicarlos.
3. **Alinear** ítems/preguntas a objetivos/categorías.""",
        fundamento, fases_plan, fases_texto, "instrumentos",
        """1. Sección población/muestra + bosquejo de instrumento en CDigital.
2. **Éxito:** queda explícito que es propuesta para P-II.""",
        "revisar instrumentos; frenar cualquier aplicación prematura.",
    )


def guion_10(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Planeación y viabilidad
La **planeación** es el cronograma realista de fases hasta Proyecto II (con recursos y, si el formato lo pide, presupuesto). La **viabilidad** es la pregunta honesta: ¿de verdad se puede? ¿Hay acceso a la población? ¿Hay permisos? ¿Alcanza el tiempo? Viabilidad no es optimismo: un cronograma que promete encuestar a 500 personas en una semana NO es viable, es un deseo.

#### 2. Integración del anteproyecto
ACA3 exige el documento **completo e integrado**, no un fragmento nuevo pegado al final. “Integrar” significa que la formulación corregida, el marco referencial, el método y la planeación se lean como UN solo texto coherente, con las correcciones de ACA1 y ACA2 ya incorporadas.

#### 3. Checklist de coherencia final (previo a S11)
El hilo completo debe cerrar sin saltos: pregunta ↔ objetivos ↔ marco ↔ método ↔ instrumento propuesto ↔ cronograma. Cualquier eslabón que no conecte es un “gap” que hay que registrar y asignar a un responsable del equipo.

#### 4. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Cronograma irreal (todo en una semana) | “¿Eso se puede de verdad? Ajústelo a tiempos y accesos reales.” |
| Pega ACA3 como fragmento nuevo | “ACA3 es el documento COMPLETO integrado, no un anexo suelto.” |
| No incorporó las correcciones previas | “Las correcciones de ACA1 y ACA2 no son opcionales; el producto es acumulativo.” |
| Objetivos que ya no coinciden con el método | “Revise el hilo: si el método cambió, ¿siguen alineados los objetivos?” |
| Ignora la viabilidad de acceso | “¿Tiene permiso para llegar a esa población en Proyecto II? Declárelo.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Cronograma y viabilidad", 14),
        ("3️⃣ Integración del documento", 12),
        ("4️⃣ Taller: matriz de coherencia + gaps", 20),
        ("5️⃣ Cierre", 8),
    ]
    fases_texto = """#### 1️⃣ Encuadre (~6 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 10**. Ya tienen todas las piezas sueltas; hoy las miramos como un SISTEMA. Trabajamos planeación, viabilidad e integración del anteproyecto de cara a ACA3, que es el producto de cierre.”
> “**Slide 2.** Meta de hoy: construir un cronograma y una viabilidad realistas, integrar el documento completo y detectar los ‘gaps’ de coherencia antes del cierre.”

#### 2️⃣ Cronograma y viabilidad (~14 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** La planeación es el cronograma realista de las fases hasta Proyecto II. La viabilidad es la pregunta honesta: ¿de verdad se puede? Si su cronograma promete encuestar a quinientas personas en una semana, eso no es un plan, es un deseo.”
> “Piensen en tres frentes de viabilidad: acceso —¿los dejarán entrar a esa población?—, permisos —¿hay avales pendientes?— y tiempo. Un anteproyecto viable es más valioso que uno ambicioso e imposible.”

#### 3️⃣ Integración del documento (~12 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “**Slide 4.** ACA3 NO es un fragmento nuevo que se pega al final: es el documento COMPLETO e integrado. Integrar significa que la formulación corregida, el marco, el método y la planeación se lean como un solo texto, con las correcciones de ACA1 y ACA2 ya metidas.”
> “Recuerden que el producto es acumulativo: si no incorporaron mis correcciones anteriores, el documento no está integrado, está remendado. Hoy detectamos esos remiendos.”

#### 4️⃣ Taller: matriz de coherencia + gaps (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos. Armen una matriz de coherencia en Google Docs: filas = las secciones del anteproyecto; columnas = ¿existe?, ¿está alineada con la pregunta?, ¿qué falta? Marquen cada casilla y hagan una lista de ‘gaps’ con un responsable por cada uno. Yo circulo. Suban como `S10_IntegracionViabilidad_Apellidos`.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Cronograma irreal | “Ajústelo a accesos y tiempos reales; menos es más.” |
| Pega ACA3 como anexo | “Es el documento completo integrado, no un fragmento.” |
| No metió correcciones | “El producto es acumulativo; incorpórelas ahora.” |
| Método y objetivos no cuadran | “Revise el hilo: si el método cambió, realinee.” |

#### 5️⃣ Cierre (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** En autónomo, cierren los gaps priorizados por impacto y avancen el cronograma y —si el formato lo pide— el presupuesto. Suban `S10_IntegracionViabilidad_Apellidos`.”
> “**Slide 7.** La próxima es la última sesión sincrónica: coevaluación, autoevaluación e integración final. Pasamos a tutoría; priorizamos las correcciones de alto impacto equipo por equipo.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Construir** cronograma/viabilidad realistas.
2. **Integrar** el anteproyecto completo.
3. **Detectar** gaps de coherencia antes del cierre.""",
        fundamento, fases_plan, fases_texto, "integración",
        """1. Matriz de coherencia + avance de cronograma/presupuesto en CDigital.
2. **Éxito:** gaps priorizados con responsable.""",
        "revisar integración; priorizar correcciones de alto impacto.",
    )


def guion_11(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Integración final
Es la lectura de cierre del anteproyecto con tres preguntas: ¿el documento cuenta UNA sola historia de principio a fin?, ¿el APA está estable (sin citas huérfanas)?, ¿queda clarísimo que los instrumentos son PROPUESTOS y no aplicados? Si las tres respuestas son sí, el anteproyecto está listo para ACA3.

#### 2. Coevaluación y autoevaluación (ESP329)
Son componentes individuales de cierre (coevaluación 4% y autoevaluación 4%; ventanas y detalle logístico en la Presentación del Curso y en CDigital). En clase se practica una coevaluación **formativa** con una rúbrica breve —entrena el ojo crítico—, pero esa práctica NO sustituye la actividad oficial que cada estudiante diligencia en Moodle en su ventana.

#### 3. Puente a Proyecto II
Cierre honesto: dejar por escrito qué queda listo para ejecutar tras el aval y qué NO se hizo (todo el trabajo de campo). Ese “qué falta” no es una debilidad: es el alcance correcto de Proyecto I.

#### 4. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Cree que la coeval de clase reemplaza la de Moodle | “No: la de hoy entrena; la oficial se diligencia en CDigital en su ventana.” |
| Da feedback vago (‘está bien’) | “Feedback accionable: qué específicamente y cómo lo mejora.” |
| Presenta instrumentos como aplicados | “Deje explícito que son PROPUESTOS; es la frontera de Proyecto I.” |
| El documento suena a piezas pegadas | “Léalo de corrido: ¿es una historia o un collage? Integre las costuras.” |
| Se autoevalúa sin criterios | “Use la rúbrica: coherencia, delimitación, método, APA. Argumente su nota.” |
"""
    fases_plan = [
        ("1️⃣ Encuadre de cierre", 8),
        ("2️⃣ Checklist de integración final", 12),
        ("3️⃣ Coevaluación formativa (modelo)", 12),
        ("4️⃣ Taller: rúbrica entre pares + ajustes", 20),
        ("5️⃣ Cierre del encuentro sincrónico", 8),
    ]
    fases_texto = """#### 1️⃣ Encuadre de cierre (~8 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes. **Sesión 11**, la última sesión sincrónica de contenido del curso. Hoy cerramos el ciclo: verificamos la integración final del anteproyecto y practicamos la coevaluación con criterios claros.”
> “**Slide 2.** Meta de hoy: dejar el documento como UNA sola historia coherente, entrenar el ojo crítico con una rúbrica entre pares, y tener claras las ventanas de coevaluación y autoevaluación en CDigital.”

#### 2️⃣ Checklist de integración final (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** Vamos a pasar el checklist en voz alta, y cada equipo va marcando en su documento: ¿está el problema?, ¿la pregunta?, ¿los objetivos?, ¿el marco referencial completo?, ¿el método?, ¿los instrumentos propuestos?, ¿el cronograma?, ¿las referencias en APA?”
> “Tres preguntas de oro para la integración: ¿el documento cuenta una sola historia?, ¿el APA está estable sin citas huérfanas?, ¿queda clarísimo que los instrumentos son PROPUESTOS? Si las tres dan sí, están listos para ACA3.”

#### 3️⃣ Coevaluación formativa (modelo) (~12 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “**Slide 4.** Vamos a practicar feedback con una rúbrica de cuatro criterios: coherencia, delimitación, método propuesto y APA. Les modelo cómo se da un comentario ACCIONABLE: no ‘está bien’, sino ‘la pregunta no nombra el contexto; agregue dónde ocurre’.”
> “Aclaro algo importante: esta práctica de hoy NO reemplaza la coevaluación oficial que cada uno diligencia en Moodle en su ventana. Lo de hoy entrena el ojo; lo oficial va en CDigital, y vale su porcentaje.”

#### 4️⃣ Taller: rúbrica entre pares + ajustes (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos. Intercambien una sección de su anteproyecto con otro equipo —o hagan lecturas cruzadas— y devuelvan tres comentarios accionables usando la rúbrica de cuatro criterios. Después, apliquen los ajustes que valgan la pena en su propio documento. Yo circulo. Suban como `S11_CierreIntegracion_Apellidos`.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Da feedback vago (‘está bien’) | “Sea accionable: qué exactamente y cómo mejorarlo.” |
| Cree que reemplaza la coeval de Moodle | “No: la oficial va en CDigital, en su ventana.” |
| Presenta instrumentos como aplicados | “Marque que son PROPUESTOS; esa es la frontera.” |
| El texto suena a piezas pegadas | “Léalo de corrido y una las costuras.” |

#### 5️⃣ Cierre del encuentro sincrónico (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “**Slide 6.** No olviden las ventanas de coevaluación y autoevaluación en CDigital —el detalle logístico está en la Presentación del Curso—; cada una es individual y vale su porcentaje. En autónomo, pulido final del anteproyecto para ACA3.”
> “**Slide 7.** La tutoría de hoy es de pulido final. Gracias por el trabajo de todo el periodo: salen con un anteproyecto completo, viable y listo para ejecutar en Proyecto II tras el aval. Nos vemos en las tutorías de cierre.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Verificar** integración final del anteproyecto.
2. **Practicar** coevaluación formativa con criterios claros.
3. **Cerrar** el ciclo sincrónico con autonomos de plataforma claros.""",
        fundamento, fases_plan, fases_texto, "cierre",
        """1. Lista de verificación firmada por el equipo + ajustes en CDigital.
2. **Éxito:** 3 mejoras concretas aplicadas tras pares.""",
        "pulido final del anteproyecto; recordar forms de asistencia y cierres en CDigital.",
    )


BUILDERS = {
    1: guion_01,
    2: guion_02,
    3: guion_03,
    4: guion_04,
    5: guion_05,
    6: guion_06,
    7: guion_07,
    8: guion_08,
    9: guion_09,
    10: guion_10,
    11: guion_11,
}


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    only_n = int(argv[0]) if argv and argv[0].isdigit() else None
    for ses in COURSE["sesiones"]:
        n = ses["n"]
        if only_n is not None and n != only_n:
            continue
        label = label_for(n, ses["titulo"])
        md_path = os.path.join(ROOT, f"{label}.md")
        text = BUILDERS[n](ses)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("MD", md_path)


if __name__ == "__main__":
    main()
