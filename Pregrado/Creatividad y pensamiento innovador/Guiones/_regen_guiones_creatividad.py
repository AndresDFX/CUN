# -*- coding: utf-8 -*-
"""Regenera guiones docentes de Creatividad (EI004) — solo .md, 60 min, con pantallazos.

Alineado a config/cursos/sesiones_cun.py (7 sesiones del periodo).

Sesión 01 = **ENCUADRE** (decisión del docente, 2026-08-09): no dicta tema. Presenta el
curso, al Docente, a los estudiantes (rompehielos Padlet) y las ACAs; el contenido
curricular arranca en la Sesión 02, y la unidad que antes vivía en S01 (`unidad_diferida`
en `sesiones_cun.py` → U1–U2) pasa a **lectura autónoma**.
Por eso la S01 **ya no se protege**: se regenera como cualquier otra sesión en cada corrida
(el modelo de calidad del curso es hoy la Sesión 02). El flag ``--force-s01`` se sigue
aceptando por compatibilidad con pipelines antiguos, pero **no cambia nada**.

Uso:
    python _regen_guiones_creatividad.py            # todas las sesiones (incluida S01)
    python _regen_guiones_creatividad.py 1          # solo la Sesión 01
"""
from __future__ import annotations
import os, sys, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "config", "slides"))
CURSOS = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "config", "cursos"))
sys.path.insert(0, SLIDES)
sys.path.insert(0, CURSOS)

from sesiones_cun import COURSES, meet_url  # noqa: E402
from cun_slides_engine import PADLET_PRESENTACION_URL  # noqa: E402
from guion_slides import (  # noqa: E402
    NOTA_MOMENTOS,
    ajustar_mapa_manual,
    deck_path,
    limpiar_referencias,
    tabla_slides_md,
    titulos_pptx,
)

MEET = meet_url("creatividad", COURSES["creatividad"]["titulo"])


def topic_filename(titulo: str, max_len: int = 70) -> str:
    s = re.sub(r'[<>:"/\\|?*]', "", titulo.strip())
    s = re.sub(r"\s+", " ", s).strip(" .")
    return (s[:max_len] or "Tema").rstrip()


def sesiones_meta():
    """(n, label_archivo, titulo, detalle) desde sesiones_cun."""
    out = []
    for s in COURSES["creatividad"]["sesiones"]:
        n = s["n"]
        titulo = s["titulo"]
        label = f"Sesion {n:02d} - {topic_filename(titulo)}"
        out.append((n, label, titulo, s.get("detalle", "")))
    return out


SESIONES = sesiones_meta()


def shot(rel_path: str, caption: str, tip: str) -> str:
    return (
        f"\n![{caption}](Capturas/{rel_path})\n\n"
        f"> **En pantalla:** {tip}\n"
    )


# Pantallazos por sesión canónica (n)
SHOTS = {
    # S01 = encuadre: solo el pantallazo del rompehielos (se inyecta antes de la fase 3️⃣).
    # El de Google Docs / plantilla APA va incrustado dentro de la fase 5️⃣ del guion_01.
    1: {
        "demo": [
            ("Sesion 01/s01_padlet.png", "Padlet — Preséntate",
             f"Tablero oficial del rompehielos. URL: {PADLET_PRESENTACION_URL}. ~5 min de escritura."),
        ],
    },
    2: {
        "demo": [
            ("Sesion 01/s01_miro_design_thinking.png", "Miro — Design Thinking (plantilla free)",
             "Mostrar etapas DT; plan B: Excalidraw si Miro pide login."),
            ("s01_excalidraw_pizarra.png", "Excalidraw — HMW + banco de ideas",
             "Escribir 1 How Might We y 10 ideas en voz alta."),
        ],
        "taller": [
            ("Herramientas/dt_ideo_designkit.png", "IDEO Design Kit (referencia)",
             "Solo si carga bien; si no, continuar en Excalidraw/Miro free."),
        ],
    },
    3: {
        "demo": [
            ("s01_google_docs_inicio.png", "Docs — tabla Oslo",
             "Clasificar 3 casos en producto/proceso/organización/marketing/social."),
        ],
        "taller": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — ficha Oslo de su propuesta",
             "Tipo dominante + secundario + 1 justificación."),
        ],
    },
    4: {
        "demo": [
            ("s01_google_docs_inicio.png", "Docs — matriz tipos de innovación",
             "Filas = tipos Oslo; columnas = ejemplo / su propuesta."),
        ],
        "taller": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — cuadro comparativo",
             "Mejora socio-económica vs. tipo elegido."),
        ],
    },
    5: {
        "demo": [
            ("Herramientas/bmc_canvanizer.png", "Canvanizer — Business Model Canvas",
             "Abrir https://canvanizer.com/new/business-model-canvas; llenar 3 bloques clave en vivo."),
            ("Herramientas/strategyzer_bmc.png", "Strategyzer BMC (referencia visual)",
             "Solo referencia; el trabajo se hace en Canvanizer/Excalidraw/Docs."),
        ],
        "taller": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — FODA + MVP",
             "FODA 4 cuadrantes + hipótesis de MVP en 5 líneas."),
            ("s01_google_docs_inicio.png", "Docs — consolidar Canvas/MVP",
             "Pegar captura o texto del Canvas y subir a CDigital."),
        ],
    },
    6: {
        "demo": [
            ("s01_google_docs_inicio.png", "Docs — matriz de vigilancia",
             "Columnas: señal / fuente / implicación para mi propuesta."),
        ],
        "taller": [
            ("s01_google_docs_inicio.png", "Scholar en otra pestaña + matriz",
             "Abrir https://scholar.google.com/; anotar 3 señales tecnológicas."),
        ],
    },
    7: {
        "demo": [
            ("s01_google_docs_inicio.png", "Docs — mapa de entidades de apoyo",
             "Mínimo 3 entidades reales (nombre correcto) + pedido concreto."),
        ],
        "taller": [
            ("s01_excalidraw_pizarra.png", "Pitch 60 s — guion",
             "Ensayar con cronómetro; 4 voluntarios. Canva free opcional para 1 slide."),
        ],
    },
}


def inject_shots(md: str, n: int) -> str:
    cfg = SHOTS.get(n) or {}
    demo = "".join(shot(*t) for t in cfg.get("demo", []))
    taller = "".join(shot(*t) for t in cfg.get("taller", []))
    if demo and "#### 3️⃣" in md:
        md = md.replace("#### 3️⃣", demo + "\n#### 3️⃣", 1)
    elif demo:
        md = md + "\n\n### Pantallazos (demo)\n" + demo
    if taller and "#### 4️⃣" in md:
        md = md.replace("#### 4️⃣", taller + "\n#### 4️⃣", 1)
    elif taller:
        md = md + "\n\n### Pantallazos (taller)\n" + taller
    if "Pantallazos de esta sesión" not in md and "Pantallazos en `Guiones/Capturas/`" not in md:
        md = md.replace(
            "✅ **Checklist del docente antes de clase**",
            "✅ **Checklist del docente antes de clase**\n- [ ] Pantallazos en `Guiones/Capturas/` abiertos",
            1,
        )
    return md

USO_SESION_TEMA = (
    "> **Uso:** guion de locución de **esta** clase. Léalo en voz alta casi literal.\n"
    "> Estudie primero el Fundamento Teórico. **Duración: 60 minutos**.\n"
    "> Logística de semestre (fechas, grupos, cortes) → Presentación del Curso / Manual."
)

# Sesión 01 = encuadre: no hay fundamento teórico de unidad (el tema arranca en la S02).
USO_SESION_ENCUADRE = (
    "> **Uso:** guion de **encuadre**. Esta sesión **no dicta tema**: presenta el curso, al Docente,"
    " a los estudiantes y las ACAs.\n"
    "> El contenido curricular arranca en la **Sesión 02**; la unidad U1–U2 queda como **lectura autónoma**.\n"
    "> **Duración del encuentro: 60 minutos.** El material da para dos horas: lo que no alcance se"
    " convierte en extensión y trabajo autónomo (ver tabla de ampliación).\n"
    "> Logística de semestre (fechas, grupos, cortes) → Presentación del Curso / Manual."
)


def header(n, label, titulo, detalle, uso: str | None = None):
    """Cabecera del guion. `uso` permite cambiar el bloque de encabezado (S01 = encuadre)."""
    uso = uso or USO_SESION_TEMA
    return f"""### GUIÓN DOCENTE — Sesión {n:02d}: {titulo}

{uso}
> **PPTX:** `Clases/{label}/Presentacion.pptx` — en cada fase se indica la slide de ESA presentación.

📌 **De esta sesión**
- **Sesión:** **{n:02d}** · **Tema:** {titulo}
- **Detalle:** {detalle}
- **PPTX estudiante:** `Clases/{label}/Presentacion.pptx`
- **Meet (serie del curso):** {MEET}

"""


def mapa_slides(n=None):
    """Mapa de slides de ESTA presentación (no el temario del curso)."""
    if n == 1:
        return """🗺️ **Slides de esta presentación** (Sesión 01 — encuadre; aquí no hay tema del Syllabus)

| Slide | Título en el PPTX | Cuándo usarla |
| :---: | :--- | :--- |
| **1** | Portada — SESIÓN 01, PRESENTACIÓN DEL CURSO | Apertura |
| **2** | AGENDA DE HOY | Encuadre de la hora |
| **3** | Docente | Presentación del Docente |
| **4** | PRESÉNTATE — ROMPEHIELOS (QR + Padlet) | Rompehielos |
| **5** | LAS ACAs — QUÉ SE EVALÚA | Pesos y entregas |
| **6** | Cómo trabajamos: una hora juntos, el resto por su cuenta | Metodología / aula invertida |
| **7** | Mapa del curso: las 7 sesiones de un vistazo | Recorrido del curso |
| **8** | Qué se llevan al final: la Propuesta de Innovación | Producto del curso |
| **9** | Las tres ACAs: qué se entrega en cada corte | Detalle de cada ACA |
| **10** | Qué separa un entregable fuerte de uno flojo | Criterio de calidad |
| **11** | Cómo se entrega: paso a paso en CDigital | Procedimiento de entrega |
| **12** | Integridad académica: la línea que no se cruza | Plagio y APA 7 |
| **13** | IA generativa: se usa, se declara y se verifica | Regla de uso de IA |
| **14** | Herramientas del curso: gratis y desde el navegador | Alistamiento técnico |
| **15** | Cómo pedir ayuda (y recibir respuesta pronto) | Canales y tiempos |
| **16** | Acuerdos de convivencia del encuentro | Cámara, micrófono, foro |
| **17** | Para la Sesión 02: lectura autónoma y qué traer | Encargo autónomo |
| **18** | Preguntas del primer día | Dudas típicas |
| **19** | ACUERDOS DE TRABAJO | Cierre de reglas |
| **20** | PARA LA PRÓXIMA SESIÓN | Tarea concreta |
| **21** | Cierre — Sesión 01 | Despedida |

"""
    # S02+: tabla del deck REAL en disco (16–26 slides), no la plantilla fija de 7.
    if n:
        label = None
        for m in sesiones_meta():
            if m[0] == n:
                label = m[1]
                break
        if label:
            tabla = tabla_slides_md(titulos_pptx(deck_path(COURSES["creatividad"]["folder"], label)))
            if tabla:
                return f"{tabla}\n{NOTA_MOMENTOS}\n\n"
    return """🗺️ **Slides de esta presentación** (tema de hoy — no es el mapa del curso)

| Slide | Título en el PPTX | Cuándo usarla |
| :---: | :--- | :--- |
| **1** | Portada (SESIÓN NN — tema) | Apertura |
| **2** | OBJETIVOS | Encuadre |
| **3** | CONTENIDO CLAVE | Exposición y modelación |
| **4** | ENFOQUE DE HOY | Anclaje del tema |
| **5** | ACTIVIDAD / TALLER | Consigna del taller |
| **6** | PARA CONTINUAR | Trabajo autónomo |
| **7** | Cierre | Despedida |

"""


def plan_tabla(fases):
    """fases: list of (nombre, min, acum) — reloj relativo al inicio del encuentro."""
    rows = ["| Fase | Minutos | Reloj sugerido (desde el inicio) |", "| :--- | :---: | :--- |"]
    start_m = 0
    for nombre, mins, _ in fases:
        m0 = start_m
        m1 = start_m + mins
        rows.append(f"| {nombre} | {mins} | min {m0:02d}:00 – {m1:02d}:00 |")
        start_m = m1
    rows.append("")
    rows.append(f"> **Suma:** **{sum(f[1] for f in fases)} minutos** exactos.")
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# CONTENIDOS POR SESIÓN
# ---------------------------------------------------------------------------

def guion_01(meta):
    """Sesión 01 = ENCUADRE. No dicta tema: presenta curso, Docente, estudiantes y ACAs."""
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Apertura y bienvenida", 5, 5),
        ("2️⃣ Quién es el Docente", 4, 9),
        ("3️⃣ Rompehielos Padlet — que se presenten ellos", 9, 18),
        ("4️⃣ Cómo trabajamos, recorrido del curso y su producto final", 11, 29),
        ("5️⃣ Las ACAs y cómo se entrega", 12, 41),
        ("6️⃣ Integridad académica y uso de IA", 7, 48),
        ("7️⃣ Herramientas, canales de ayuda y acuerdos", 7, 55),
        ("8️⃣ Encargo autónomo y cierre", 5, 60),
    ]
    return header(*meta, uso=USO_SESION_ENCUADRE) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión (encuadre — no hay tema del Syllabus)**
1. Que el estudiante sepa **qué produce este curso**: una **Propuesta de Innovación** propia, no un ensayo.
2. Que sepa **cómo se trabaja**: una hora sincrónica de aplicación + trabajo autónomo con el material leído antes.
3. Que sepa **qué se evalúa y cómo se entrega**: las tres ACAs, el formato APA CUN y el espacio de CDigital.
4. Que conozca las reglas de **integridad académica** y de **uso declarado de IA generativa**.
5. Que salga con **un solo encargo claro**: la lectura autónoma U1–U2 y un problema real escrito en tres líneas.

> **Lo que hoy NO se hace:** no se define creatividad, no se explica inteligencia emocional, no se dictan tipos de innovación. Todo eso **empieza en la Sesión 02**. Si usted se mete en el tema hoy, llega tarde a las ACAs y el grupo se va sin saber cómo entrega.

---

🧰 **Antes de la clase — qué debe tener listo el Docente** *(esta sesión no tiene fundamento teórico: tiene alistamiento)*

| Qué abrir / tener listo | Dónde está | Para qué momento |
| :--- | :--- | :--- |
| **Aula del curso en CDigital**, con el anuncio de bienvenida publicado y los espacios de entrega visibles | Campus institucional (login CUN) | Fases 5, 7 y 8 |
| **Padlet oficial** del rompehielos, abierto en una pestaña y con la URL copiada al portapapeles | {PADLET_PRESENTACION_URL} | Fase 3 |
| **Enunciados de las ACAs 1–3** | `Clases/Recursos/ACAs/` | Fase 5 |
| **Plantilla APA CUN**, ya abierta en **Google Docs** (no en Word de escritorio) | `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` | Fase 5 |
| **PPTX de esta sesión** (21 slides) | `Clases/{label}/Presentacion.pptx` | Toda la clase |
| **Sala de Meet** abierta 5 minutos antes | {MEET} | Fase 1 |

**Tres decisiones que debe tener tomadas ANTES de entrar** (se las van a preguntar hoy, no la próxima semana):

1. **Trabajo individual o en dúo:** en este curso se puede trabajar en dúo si comparten el mismo problema, pero **cada estudiante entrega su propio documento** en CDigital.
2. **Uso de IA generativa:** permitido y **declarado** al final del documento; toda cita que entregue la IA se verifica antes de usarla.
3. **Entregas tarde:** se conversan **antes** del cierre del espacio de entrega, nunca después. Cerrado el espacio, la nota es la que hay.

> Si duda de alguna de las tres, decida ahora y dígalo igual todo el semestre. Lo que desordena un curso no es la regla dura: es la regla que cambia.

---

🧭 **Plan de Clase por Fases** — *Total: 60 min (encuentro oficial)*

{plan_tabla(fases)}

**Si dispone de dos horas (o si el grupo va rápido)** — el material de la deck da para el doble; amplíe en este orden:

| Ampliación | Minutos extra | Cómo se hace |
| :--- | :---: | :--- |
| Padlet leído completo, no tres notas | +8 | Leer en voz alta todas las notas y agrupar temas parecidos en pantalla |
| Recorrido lento del **mapa del curso** (slide 7) | +10 | Preguntar sesión por sesión: “¿qué creen que sale de esta?” |
| **Plantilla APA CUN** en vivo | +12 | Compartir pantalla, crear la copia en Google Docs y mostrar dónde escribe cada quien |
| **Enunciado de la ACA 1** leído entero con el checklist | +10 | Abrirlo desde `Clases/Recursos/ACAs/` y marcar criterio por criterio |
| Mini-ejercicio “mi problema en tres líneas” escrito en clase | +15 | Cada quien escribe; dos voluntarios leen; el Docente solo pregunta “¿a quién le pasa?” |

> Lo que no alcance a hacer **no se elimina: se convierte en trabajo autónomo** y se anuncia como tal en CDigital.

---

#### 1️⃣ Apertura y bienvenida (~5 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (AGENDA DE HOY)

**Objetivo de la fase:** que entiendan en un minuto que hoy es una sesión de reglas y no de contenido, y que eso es deliberado.

**GUION LITERAL:**
> “Buenas tardes y bienvenidos a **Creatividad y Pensamiento Innovador**. Antes de arrancar: verifiquen que su nombre real aparezca en la sala, porque por ese nombre los voy a llamar y voy a registrar su participación.”

> “**Slide 2 — AGENDA DE HOY.** Hoy no vamos a ver tema. Y no es porque sobre tiempo: es una decisión. Hoy resolvemos las cuatro cosas por las que se pierde un curso sin necesidad: **qué se hace aquí, quién los acompaña, quiénes son ustedes y cómo se evalúa**. El contenido arranca la próxima semana, en la **Sesión 02**, con Design Thinking.”

> “Se los digo de una vez para que nadie se lleve sorpresas: este curso tiene **un solo producto**, una **Propuesta de Innovación** que ustedes van a escribir por partes desde la próxima sesión. No es un ensayo sobre innovación; es su propuesta, sobre un problema real, con un usuario de carne y hueso.”

**Qué hacer:**
1. (1 min) Portada compartida, saludo, verificación de audio y de nombres.
2. (2 min) Leer la agenda de la slide 2 y decir explícitamente que hoy no hay tema.
3. (2 min) Anunciar el producto del curso y que la evaluación es **por cortes**.

---

#### 2️⃣ Quién es el Docente (~4 min) — Protagonista: Docente
**Slides:** 3 (Docente)

**GUION LITERAL:**
> “**Slide 3.** Un minuto sobre quién los acompaña: soy Ingeniero de Sistemas, candidato a Magíster en Inteligencia Artificial, y trabajo como líder técnico en la industria. Les cuento esto por una razón práctica: lo que vamos a hacer aquí —mirar un problema, proponer algo y sustentarlo— es literalmente lo que hago cada semana en mi trabajo.”

> “Mi correo institucional está en pantalla y lo tienen también en CDigital. Más adelante les explico cuál duda va por foro y cuál por correo, para que la respuesta no se demore.”

**Qué hacer:**
1. (2 min) Perfil breve, sin currículum extendido: lo que le da autoridad ante el grupo es el vínculo con la práctica.
2. (2 min) Anunciar que los canales de contacto se explican en la fase 7 (no dispersar la información ahora).

---

#### 3️⃣ Rompehielos Padlet — que se presenten ellos (~9 min) — Protagonista: Estudiantes
**Slides:** 4 (PRESÉNTATE — QR + Padlet)

**Objetivo de la fase:** romper el silencio del primer día y, de paso, tener por escrito los intereses del grupo (le sirven de ejemplo todo el semestre).

**GUION LITERAL:**
> “**Slide 4 — PRESÉNTATE.** Ahora los escucho a ustedes, pero por escrito, que es más rápido que veinte presentaciones habladas. Escaneen el **QR** de la pantalla o abran este enlace, que también les pego en el chat: {PADLET_PRESENTACION_URL}.”

> “Publiquen **un solo post-it** con tres cosas: (1) su **nombre**; (2) **una expectativa** de este curso —qué quieren llevarse—; y (3) **un tema o problema que les interese**, algo que hayan visto que funciona mal en su trabajo, en su barrio o aquí mismo en la universidad. Sirve una línea. No busquen que suene inteligente: busquen que sea verdad. Tienen **cinco minutos** y yo los voy leyendo en voz alta.”

**Cómo conducirlo (esto es lo que hace que funcione):**
1. Proyecte el tablero mientras escriben: ver aparecer notas ajenas destraba a los que dudan.
2. Lea en voz alta **tres o cuatro** notas, sin juzgar ninguna, y conecte dos que se parezcan: “miren, dos personas dijeron algo de tiempo perdido en trámites”.
3. Cierre nombrando lo que ve: “tenemos gente de sistemas, gente que trabaja y gente que viene de otro semestre; eso ayuda, porque los problemas buenos salen de contextos distintos”.

**Si nadie escribe** (pasa, sobre todo en el primer encuentro virtual):
- **Escriba usted el primer post-it** en vivo, con su nombre y un problema real suyo. El tablero vacío paraliza; el tablero con una nota se llena solo.
- Baje el costo de entrada: “no tiene que ser el tema definitivo, ni tiene que ser original; puede cambiar la próxima semana”.
- Nombre a dos o tres personas directamente y con amabilidad: “Camila, ¿qué escribiste? Yo lo pego por ti si quieres”.
- Si aun así no pasa nada, **no alargue**: pida que lo publiquen antes de la Sesión 02 y siga. Un rompehielos que se estira diez minutos en silencio hace más daño que uno corto.

---

#### 4️⃣ Cómo trabajamos, recorrido del curso y su producto final (~11 min) — Protagonista: Docente
**Slides:** 6 (CÓMO TRABAJAMOS) → 7 (MAPA DEL CURSO) → 8 (QUÉ SE LLEVAN AL FINAL)

**GUION LITERAL:**
> “**Slide 6 — Cómo trabajamos.** Esta materia son dos créditos: alrededor de 32 horas conmigo y **64 horas suyas**. Léanlo otra vez: el doble del tiempo lo pone usted, fuera de esta sala. No lo digo para asustar, lo digo para que nadie crea que esta hora semanal es el curso completo.”

> “Como la hora es corta, trabajamos en **aula invertida**: el material de cada unidad queda en **CDigital** y ustedes lo leen **antes**. La hora de encuentro no la voy a gastar leyéndoles diapositivas: la vamos a gastar **aplicando** eso a su propia propuesta. Traigan siempre su documento de trabajo abierto; aquí se trabaja sobre lo que ya está escrito, no sobre lo que uno recuerda.”

> “**Slide 7 — Mapa del curso.** Son siete encuentros. Hoy encuadre; la próxima, Design Thinking; luego el Manual de Oslo, los tipos de innovación, la validación con Canvas y MVP, la vigilancia tecnológica y, al final, el ecosistema y el pitch. Fíjense en la tercera columna: **cada sesión deja un pedazo del mismo documento**. Ninguna es un taller suelto.”

> “Van a notar que el mapa tiene ocho unidades y solo siete encuentros. Las dos primeras —la Propuesta de Innovación y el bloque de creatividad e inteligencia emocional— quedan como **lectura autónoma** y las retomamos al abrir la Sesión 02. Al final de la clase les digo exactamente qué leer.”

> “**Slide 8 — Qué se llevan al final.** El producto es una **Propuesta de Innovación** de ocho a doce páginas más un pitch de una página, que responde en orden: problema, usuario, propuesta de valor, tipo de innovación, validación, vigilancia y siguiente paso. Y una advertencia sincera: si al terminar solo tienen un archivo para la nota, desperdiciaron el semestre. Esto les sirve para una entrevista de trabajo, para proponer una mejora en la empresa donde están, o como semilla de su opción de grado.”

**Qué hacer:**
1. (3 min) Insistir en la proporción 32/64 horas: es la expectativa que evita el reclamo del corte 3.
2. (4 min) Recorrer el mapa preguntando al grupo qué creen que sale de dos o tres sesiones.
3. (4 min) Anclar el producto final y su utilidad fuera del aula.

---

#### 5️⃣ Las ACAs y cómo se entrega (~12 min) — Protagonista: Docente
**Slides:** 5 (LAS ACAs — QUÉ SE EVALÚA) → 9 (LAS TRES ACAs EN DETALLE) → 10 (FUERTE vs. FLOJO) → 11 (CÓMO SE ENTREGA)

**GUION LITERAL:**
> “**Slide 5.** Evaluación por cortes: **30, 30 y 40 por ciento**. Los pesos están ahí y también en la Presentación del Curso. Las **fechas exactas no las dicto de memoria**: están en el enunciado de cada ACA, en `Clases/Recursos/ACAs/`, y en el espacio de entrega de CDigital. Anótenlas hoy mismo en su calendario.”

> “**Slide 9 — Las tres ACAs en detalle.** ACA 1: la ficha del problema, el mapa de bloqueadores y la síntesis de ideación; se evalúa que el problema sea **real, observable y de alguien concreto**. ACA 2: la propuesta tipificada, con FODA, Canvas y MVP; se evalúa que esté **validada**, no solo descrita. ACA 3: la propuesta consolidada con vigilancia, entidades de apoyo y pitch; se evalúa que **cierre el hilo**, del problema al siguiente paso.”

> “**Slide 10 — Qué separa un entregable fuerte de uno flojo.** Léanla completa esta semana. Resumo la columna izquierda: usuario genérico, problema deducido de la solución que ya eligieron, evidencia tipo ‘todo el mundo sabe que’, fuentes copiadas de un blog sin autor y un documento escrito la noche anterior. Yo no evalúo **cuánto** escribieron: evalúo si **se entiende, se sostiene y avanzó** desde el corte anterior.”

> “**Slide 11 — Cómo se entrega.** Seis pasos y ninguno es opcional: escriben en la **plantilla APA CUN** abierta en **Google Docs** —no necesitan Office instalado—, revisan el checklist del enunciado, exportan a **PDF**, nombran el archivo **CRE_ACA1_Apellido**, lo suben al espacio del corte en **CDigital** y **verifican que abra** desde la plataforma. Un archivo corrupto cuenta como no entregado.”

> “Y la regla que más disgustos evita: **entrega oficial es CDigital**. No recibo trabajos por correo, ni por WhatsApp, ni por mensaje privado. Si se les complica una fecha, hablamos **antes** del cierre, no después.”

**Qué hacer:**
1. (3 min) Recorrer las tres ACAs sin leer el enunciado completo: el detalle vive en `Clases/Recursos/ACAs/`.
2. (4 min) Abrir en pantalla el enunciado de la **ACA 1** y mostrar dónde está el checklist de criterios.
3. (5 min) Compartir pantalla con la **plantilla APA CUN en Google Docs** y mostrar el flujo real: copia propia → escribir → exportar PDF → subir a CDigital.
{shot("Sesion 01/s01_google_docs_inicio.png", "Google Docs — plantilla APA CUN y flujo de entrega", "Abrir la plantilla en Google Docs, hacer una copia propia y mostrar el camino hasta CDigital.")}

---

#### 6️⃣ Integridad académica y uso de IA (~7 min) — Protagonista: Docente
**Slides:** 12 (INTEGRIDAD ACADÉMICA) → 13 (IA GENERATIVA)

**GUION LITERAL:**
> “**Slide 12.** Todo lo que no sea suyo se **cita en APA 7**: texto, datos, imágenes, código y también las ideas que resumieron con sus palabras. Citar no les resta mérito; demuestra que leyeron. Cuenta como plagio copiar y pegar sin fuente, parafrasear sin citar, traducir un texto ajeno y presentarlo como propio, o entregar un trabajo que hizo otra persona.”

> “Sean conscientes de una cosa: si aparece plagio, **esto no se arregla entre ustedes y yo**. Sigue el conducto que fija el Reglamento Estudiantil de la CUN. Por eso les pido que pregunten antes, no que expliquen después: nadie ha perdido puntos por preguntar cómo se cita.”

> “**Slide 13 — IA generativa.** En este curso la IA **no está prohibida: está regulada**. Tres reglas. Primera: **declárenla** en una nota corta al final del documento —qué herramienta, para qué y qué hicieron ustedes con la salida—. Declararlo no baja la nota; ocultarlo sí es una falta. Segunda: **verifiquen toda cita** que les dé; el error número uno son las referencias inventadas, autor y año que suenan perfectos y no existen. Si no lograron abrir el documento original, esa fuente no entra.”

> “Tercera, y es la importante: la IA **no puede hacer lo que este curso evalúa**. No puede observar a un usuario real, no puede elegir su problema y no puede defender su criterio. Un texto impecable sobre un problema que ustedes nunca miraron se cae en la primera pregunta que yo haga. Ustedes firman el entregable: responden por cada frase.”

**Qué hacer:**
1. (3 min) Integridad y debido proceso, sin dramatizar y sin amenazar.
2. (4 min) Regla de IA con ejemplo: pedirle a una IA tres referencias y mostrar cómo se verifica una en Google Scholar.

---

#### 7️⃣ Herramientas, canales de ayuda y acuerdos (~7 min) — Protagonista: Docente
**Slides:** 14 (HERRAMIENTAS) → 15 (CÓMO PEDIR AYUDA) → 16 (CONVIVENCIA) → 19 (ACUERDOS DE TRABAJO)

**GUION LITERAL:**
> “**Slide 14 — Herramientas.** Todas gratis y todas desde el navegador: CDigital para material y entregas; Google Docs y Slides para escribir; Padlet para tableros; Excalidraw para bocetos; Canvanizer para el Canvas del corte 2; Scholar, SciELO y Redalyc para buscar; ZoteroBib para armar las referencias en APA 7 sin instalar nada. **Nada de pagar ni de instalar.** Si una herramienta les pide tarjeta, no es la que estamos pidiendo.”

> “**Slide 15 — Cómo pedir ayuda.** Tres canales, en este orden. En el encuentro, los últimos minutos son para dudas y casi nadie los usa. En el **foro de CDigital**, las dudas que le sirven a todo el grupo: formato, entrega, alcance de un ACA; ahí respondo y la respuesta queda para los demás. Por **correo institucional**, lo personal. Asunto sugerido: **EI004, su nombre y el tema en cuatro palabras**. Respondo en días hábiles, normalmente entre 24 y 48 horas; no hay atención de madrugada ni domingo.”

> “Y una petición concreta: pregunten **la duda puntual**. ‘No entendí nada’ no se puede responder. ‘No sé si mi usuario es el estudiante o el laboratorista’ sí se responde en dos líneas.”

> “**Slide 16 — Convivencia.** Empezamos a la hora en punto. Nombre real en la sala. Micrófono cerrado por defecto y abierto para participar; **cámara bienvenida pero no obligatoria** —si no pueden, participen por el chat—. Lo que no funciona es estar conectado y ausente. Aquí se piensa en voz alta y se muestran borradores a medio hacer: **ninguna idea se ridiculiza**; las ideas se critican con criterio, a las personas no. Y si el encuentro se graba, lo aviso al inicio y la grabación queda en CDigital.”

> “**Slide 19 — Acuerdos de trabajo.** Son los tres que ya dijimos, juntos: la entrega es en CDigital, se trae el avance escrito a cada encuentro, y se cita siempre en APA 7.”

**Qué hacer:**
1. (3 min) Recorrer herramientas y pedirles que abran CDigital **ahora**, en otra pestaña, para confirmar que entran.
2. (2 min) Canales y tiempos de respuesta.
3. (2 min) Convivencia y acuerdos, en tono de acuerdo mutuo y no de reglamento leído.

---

#### 8️⃣ Encargo autónomo y cierre (~5 min) — Protagonista: Docente
**Slides:** 17 (PARA LA SESIÓN 02) → 18 (PREGUNTAS DEL PRIMER DÍA) → 20 (PARA LA PRÓXIMA SESIÓN) → 21 (Cierre)

**GUION LITERAL:**
> “**Slide 17 — Para la Sesión 02.** Cuatro cosas, y son cortas. Primera: la **lectura autónoma obligatoria**, unidades **U1 y U2** del Syllabus —Propuesta de Innovación, y creatividad e inteligencia emocional—; el material está en CDigital. Las retomamos en los primeros minutos de la próxima sesión: las repasamos, no las dictamos completas. Léanlas con una pregunta en la mano: **¿qué de esto me sirve para el problema que voy a elegir?**”

> “Segunda: abran el **enunciado de la ACA 1** y léanlo entero, con checklist. Tercera: **traigan escrito**, con tres líneas basta, un problema real que les moleste, **a quién** le pasa y **dónde** lo vieron. No me traigan una solución; tráiganme un problema: la solución es el trabajo del resto del curso. Cuarta: creen su documento en Google Docs con la plantilla APA CUN y déjenlo listo.”

> “**Slide 18 — Preguntas del primer día.** Las dejo en pantalla mientras me preguntan lo que quieran: si se pierde fácil, si se puede en dúo, si sirve un trabajo de otro semestre y si hace falta programar. Las respuestas cortas están ahí; las largas se las doy ahora.”

> “**Slide 20 — Para la próxima sesión.** Resumido en tres líneas para que nadie lo pierda: lectura autónoma U1–U2, enunciado de la ACA 1 leído, y su problema escrito. Lo pego también en el chat y lo publico hoy mismo en CDigital.”

> “**Slide 21 — Cierre.** Hoy no vimos tema y salimos sabiendo cómo se trabaja, qué se entrega y con quién cuentan. La **Sesión 02** arranca el contenido: *Creatividad e innovación en I+D, Design Thinking y técnicas*, y se trabaja sobre lo que ustedes traigan. Mismo enlace de siempre. Nos vemos.”

**Qué hacer:**
1. (2 min) Dictar el encargo autónomo y **escribirlo también en el chat** (lo que solo se dice, se pierde).
2. (2 min) Preguntas abiertas con la slide 18 proyectada.
3. (1 min) Cierre y despedida.

---

❓ **Si un estudiante pregunta… — Usted responde…** *(las dudas reales del primer día)*

| Si un estudiante pregunta… | Usted responde… |
| :--- | :--- |
| “¿Esta materia se pierde fácil?” | “No, si entrega. Se pierde por no entregar y por dejarlo todo para el Corte 3, que pesa el 40%. Quien avanza cada semana llega tranquilo.” |
| “¿Puedo trabajar solo o toca en grupo?” | “Puede trabajar en dúo si comparten el mismo problema, pero **cada uno entrega su documento** en CDigital. La nota es individual.” |
| “¿Sirve un trabajo de otro semestre?” | “Puede **partir** de un proyecto suyo si lo declara y lo lleva más lejos. Volver a entregar lo mismo es autoplagio, y eso sí es falta.” |
| “¿La clase se graba?” | “Si se graba, lo aviso al inicio y la grabación queda en CDigital. No es reemplazo de la clase: el taller se hace en vivo.” |
| “¿Puedo usar ChatGPT?” | “Sí, declarándolo al final del documento y verificando toda cita que le dé. Lo que la IA no puede hacer es observar a su usuario ni defender su criterio.” |
| “¿Necesito saber programar o diseñar?” | “No. Aquí se evalúa criterio: problema real, propuesta clara y evidencia. La tecnología es un medio, no el requisito.” |
| “¿Cuándo es la primera entrega?” | “La fecha exacta está en el enunciado de la ACA 1 y en el espacio de entrega de CDigital. Ábralo hoy y anótela en su calendario.” |
| “¿Y si no puedo conectarme a un encuentro?” | “Avise antes, revise el material en CDigital y llegue al siguiente con el avance. La ausencia no mueve la fecha de entrega.” |
| “¿Qué tema escojo? No se me ocurre nada.” | “No busque un tema: busque algo que **funcione mal** donde usted está. Un trámite lento, un dato que se pierde, una fila. De ahí sale la propuesta.” |
| “¿Se puede cambiar de problema después?” | “Sí, y es normal, sobre todo tras la Sesión 02. Lo que no se puede es llegar al Corte 2 sin haber elegido ninguno.” |

---

🧩 **Qué se lleva el estudiante de esta sesión**

**No hay entregable evaluado hoy** (el encuadre no se califica). Se lleva **tres cosas verificables**:

1. Su **post-it publicado** en el Padlet del curso: {PADLET_PRESENTACION_URL}
2. El **enunciado de la ACA 1** abierto y leído, con la fecha de entrega anotada en su calendario.
3. El **encargo autónomo** para la Sesión 02: lectura U1–U2 en CDigital + un problema real escrito en tres líneas (a quién le pasa y dónde lo vio) + documento de trabajo creado en Google Docs con la plantilla APA CUN.

**Criterio de éxito de la clase:** si al terminar un estudiante puede responder sin dudar *“¿qué produce este curso, cómo entrego y qué debo traer la próxima semana?”*, el encuadre funcionó.

---

✅ **Checklist del Docente antes de clase**
- [ ] Pantallazos de apoyo abiertos (`Guiones/Capturas/Sesion 01/`)
- [ ] Aula de **CDigital** abierta, con el anuncio de bienvenida publicado
- [ ] Abrí `Clases/{label}/Presentacion.pptx` (21 slides)
- [ ] **Padlet** abierto y URL copiada para pegar en el chat: {PADLET_PRESENTACION_URL}
- [ ] Enunciados **ACA 1–3** abiertos desde `Clases/Recursos/ACAs/`
- [ ] **Plantilla APA CUN** abierta en Google Docs, lista para compartir pantalla
- [ ] Tengo decidida mi respuesta a: dúo, IA y entregas tarde
- [ ] Meet listo: {MEET}

📋 **Después de la clase (mismo día)**
- [ ] Publiqué en **CDigital** el anuncio con: enlace del Padlet, encargo autónomo (lectura U1–U2) y recordatorio del enunciado de la ACA 1
- [ ] Revisé el Padlet y anoté 3 problemas del grupo para usarlos como ejemplo en la Sesión 02
- [ ] Verifiqué que el espacio de entrega del Corte 1 esté visible para los estudiantes

---
*Fin del Guión — Sesión 01 (encuadre). Aquí no se dicta tema: el contenido del Syllabus arranca en la Sesión 02 y la unidad U1–U2 queda como lectura autónoma.*
"""


def guion_02(meta):
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre + puente desde S01", 5, 5),
        ("2️⃣ IE: qué es y por qué importa para innovar", 12, 17),
        ("3️⃣ Bloqueadores vs. ensanchadores (modelación)", 13, 30),
        ("4️⃣ Taller: mapa de utilidad + plan anti-bloqueador", 22, 52),
        ("5️⃣ Cierre + autónomo", 8, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión**
1. **Explicar** qué es inteligencia emocional (IE) en lenguaje operativo (no clínico).
2. **Identificar** bloqueadores y ensanchadores de la creatividad en sí mismos.
3. **Conectar** la IE con el problema de la Propuesta de Innovación (mapa de utilidad).
4. **Salir** con un plan anti-bloqueador aplicable esta semana.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

#### 1. Inteligencia emocional (versión de aula)
Para este curso, **inteligencia emocional** = capacidad de **reconocer, nombrar y regular** emociones propias y ajenas para **decidir mejor** bajo incertidumbre. No es “ser simpático”; es **gestionar el estado interno** para poder observar, idear y prototipar sin sabotearse.

Componentes útiles en clase (basados en el marco popularizado por Goleman, simplificados):
1. **Autoconciencia** — ¿qué siento ahora?
2. **Autorregulación** — ¿qué hago con eso?
3. **Motivación** — ¿qué me mueve a insistir?
4. **Empatía** — ¿qué siente el usuario del problema?
5. **Habilidades sociales** — ¿cómo pido feedback sin cerrarme?

#### 2. Bloqueadores vs. ensanchadores
| Bloqueadores (cierran) | Ensanchadores (abren) |
| :--- | :--- |
| Miedo al ridículo / al “qué dirán” | Permiso de borrador feo |
| Perfeccionismo (“aún no está listo”) | Timebox: 10 min y se muestra |
| Juicio prematuro (“eso no sirve”) | Separar divergencia de convergencia |
| Compararse con expertos | Compararse con la versión de ayer |
| Fatiga / multitasking | Ritual breve de foco (2 min) |

#### 3. Mapa de utilidad (puente al entregable)
El mapa de utilidad responde: **¿para quién es útil mi propuesta y en qué momento del dolor?** Campos mínimos:
- Usuario
- Momento del dolor (cuándo ocurre)
- Emoción del usuario (frustración, miedo, aburrimiento…)
- Emoción/bloqueador del innovador (usted)
- Acción ensanchadora (qué haré distinto esta semana)

#### 4. Errores frecuentes
- Tratar la IE como charla motivacional sin producto escrito.
- Confundir empatía con “yo también sufrí”: empatía = **entender al usuario**, no protagonizar.
- Listar bloqueadores sin **plan** (el plan es el entregable).

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Encuadre (~5 min)
**Slides:** 1 → 2

**GUION LITERAL:**
> “Buenas tardes. Sesión **02**. En la slide **2** ven los objetivos. Traían la ficha de problema y tres bloqueadores. Si alguien no trajo, anote ahora en el chat uno solo: el que más le pesa. Hoy vamos a convertir eso en un **mapa de utilidad** conectado a su Propuesta de Innovación.”

---

#### 2️⃣ IE y creatividad (~12 min)
**Slide:** 3

**GUION LITERAL:**
> “**Slide 3.** Inteligencia emocional, en este curso, no es terapia: es **herramienta de innovación**. Si no nombro lo que siento —miedo a mostrar un borrador, ansiedad por la nota— ese sentimiento me dirige en silencio y mato ideas buenas antes de probarlas.”

> “Innovar exige empatía con el **usuario** y honestidad conmigo. Sin la primera, diseño para mí. Sin la segunda, abandono al primer ‘no’.”

Explique los 5 componentes en 6–7 minutos con un ejemplo de ingeniería (code review, demo fallida, usuario que no adopta el sistema).

---

#### 3️⃣ Bloqueadores / ensanchadores — modelación (~13 min)
**Slide:** 3

Modele en pantalla una tabla con SU ejemplo (o el del laboratorio de la S01):

| Momento | Bloqueador | Ensanchador concreto |
| :--- | :--- | :--- |
| Mostrar ficha en clase | “Me van a decir que es obvio” | “Leo solo usuario+dolor en 30 s; el juicio viene después” |
| Pedir feedback a un usuario | “No quiero molestar” | “Hago 3 preguntas de 5 minutos esta semana” |

**GUION LITERAL:**
> “Fíjense: el ensanchador no es un poster motivacional. Es una **acción con tiempo**. ‘Voy a ser creativo’ no sirve. ‘El jueves a las 7 pm hago tres preguntas a un usuario’ sí sirve.”

---

#### 4️⃣ Taller (~22 min)
**Slide:** 5

**Consigna:**
> “**Slide 5.** Tienen 22 minutos. Llenen el **Mapa de utilidad S02** con: usuario, momento del dolor, emoción del usuario, su bloqueador #1, ensanchador con fecha/hora, y cómo eso mejora la ficha de la S01. Al final, dos voluntarios leen solo el ensanchador.”

---

#### 5️⃣ Cierre (~8 min)
**Slides:** 6 → 7

**GUION LITERAL:**
> “Ideas clave: (1) la IE se **opera**, no se declara; (2) todo bloqueador necesita ensanchador con agenda; (3) la empatía mira al usuario de su ficha.”

> “**Slide 6.** Autónomo: ejecuten el ensanchador antes de la siguiente sesión y traigan **evidencia** (nota de entrevista, audio con permiso, captura). Sesión 03: Design Thinking e ideación.”

---

🧩 **Actividad práctica**
1. Mapa de utilidad S02 en clase.
2. **Criterio de éxito:** ensanchador con día/hora + vínculo explícito al problema S01.
3. **Entregable CDigital:** `S02_MapaUtilidad_Apellido` + evidencia del ensanchador (autónomo).

---

✅ **Checklist del docente**
- [ ] Fundamento leído · PPTX abierto · espacio CDigital listo · {MEET}
"""


def guion_03(meta):
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre + puente desde la sesión anterior", 6, 6),
        ("2️⃣ Design Thinking + divergente/convergente", 13, 19),
        ("3️⃣ Modelación de ideación (HMW + SCAMPER)", 12, 31),
        ("4️⃣ Taller: ideación sobre su problema", 22, 53),
        ("5️⃣ Cierre + trabajo autónomo", 7, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión**
1. **Describir** las cinco etapas del Design Thinking (DT) en una versión operable, no decorativa.
2. **Practicar** pensamiento divergente y, por separado, pensamiento convergente.
3. **Redactar** un *How Might We* (HMW) centrado en el usuario y el dolor de su propuesta.
4. **Generar** mínimo 8 ideas y **elegir** 1–2 para un prototipo conceptual (boceto).
5. **Actualizar** la Propuesta de Innovación con el HMW y el boceto de hoy.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Este apartado asume que usted **no** es especialista en Design Thinking. Léalo completo: las definiciones, la analogía del doble diamante y los ejemplos de aquí son los que dirá en voz alta.

#### 1. Qué es Design Thinking (y por qué a un ingeniero le sirve)
**Design Thinking (DT)** es un enfoque de resolución de problemas **centrado en las personas**, popularizado por la consultora **IDEO** y la **d.school de Stanford**. Su idea central es simple pero incómoda para quien viene de Ingeniería: **primero se entiende profundamente al usuario y su problema; la solución se pospone**. El ingeniero promedio salta al “cómo lo construyo” en el minuto uno; DT lo obliga a quedarse un rato más en el “qué le duele y a quién”.

No es una receta lineal: es **iterativo**. Se avanza, se prueba con un usuario, se descubre que el problema estaba mal planteado y se retrocede. Ese ir y volver no es fracaso, es el método funcionando. En el aula lo trabajamos en cinco etapas:

| Etapa | Pregunta | Producto mínimo |
| :--- | :--- | :--- |
| **Empatizar** | ¿Qué vive y siente el usuario? | Notas de observación/entrevista |
| **Definir** | ¿Cuál es el problema real? | Pregunta *How Might We* (HMW) |
| **Idear** | ¿Qué alternativas hay? | Lista amplia sin juzgar |
| **Prototipar** | ¿Cómo se ve/toca la idea? | Boceto, storyboard, mock feo |
| **Evaluar / testear** | ¿Qué aprendimos al mostrarlo? | 3 aprendizajes del usuario |

Hoy el foco fuerte es **Definir + Idear**. La empatía ya la traen de la sesión anterior (evidencia de observación) y el prototipo de hoy puede ser solo conceptual (un boceto feo en Excalidraw).

#### 2. Divergencia y convergencia — el “doble diamante”
La imagen que mejor funciona en clase es el **doble diamante**: se **abre** (divergencia) y se **cierra** (convergencia) **dos veces** — una para entender el problema y otra para construir la solución.

- **Pensamiento divergente:** ampliar opciones. Importa la **cantidad** y se acepta la rareza. Regla sagrada: **prohibido juzgar**. Una idea mala dicha en voz alta suele ser el trampolín de una buena.
- **Pensamiento convergente:** filtrar y decidir con **criterios explícitos**: deseabilidad (¿lo quiere el usuario?), factibilidad (¿lo podemos hacer en el semestre?) y viabilidad (¿se sostiene?).

El error clásico —y el que usted verá hoy en clase— es **converger a los 30 segundos**: alguien propone algo y otro dice “eso no se puede”. Ahí mataron la idea antes de que naciera. Su trabajo como docente es **separar los dos momentos en el tiempo**: “ahora solo generamos; en cinco minutos filtramos”.

#### 3. How Might We (HMW) — la bisagra entre problema y solución
El HMW es la frase que traduce un problema en un **reto accionable**. Fórmula:

**¿Cómo podríamos [acción] para [usuario] de modo que [resultado deseado]?**

- Mal (mira la tecnología): “¿Cómo hacemos una app con IA?”
- Bien (mira al usuario y el dolor): “¿Cómo podríamos **reducir la incertidumbre de reserva de laboratorio** para que **el estudiante de Ingeniería** **no pierda su hora de práctica**?”

Un buen HMW no es tan amplio que no se pueda atacar (“¿cómo salvamos la educación?”) ni tan estrecho que ya contenga la solución (“¿cómo hacemos un botón de reserva?”). Es el punto medio que abre espacio para muchas ideas.

#### 4. Técnicas de ideación (para que no se queden mirando la hoja en blanco)
- **SCAMPER** — una batería de siete preguntas para forzar variaciones sobre el problema: **S**ustituir, **C**ombinar, **A**daptar, **M**odificar, **P**oner en otro uso, **E**liminar, **R**eordenar. Ejemplo en Ingeniería: “¿Y si *eliminamos* el paso de reserva y el sistema asigna el equipo automáticamente por horario?”.
- **Brainwriting (6-3-5):** en vez de gritar ideas, cada quien escribe 3 ideas en silencio y las pasa; evita que hable solo el extrovertido y multiplica el volumen.
- **Analogías:** “¿Cómo resuelve este dolor otra industria?” (turnos de banco, reservas de restaurante, casilleros de gimnasio). Trasplantar soluciones de otro sector es una fuente enorme de innovación.

#### 5. Del boceto al prototipo conceptual (herramientas gratis + nube)
Un prototipo no es la app terminada: es **lo mínimo para que otro entienda y opine**. Cajitas y flechas en **Excalidraw** (https://excalidraw.com, sin cuenta), un **storyboard** de 4 viñetas, o el journey en una **plantilla free de Miro** bastan. Si Miro pide login, el plan B siempre es Excalidraw o **tldraw**. El **IDEO Design Kit** se usa **solo como referencia visual** si carga; nunca instalen software ni exijan cuentas de pago.

#### 6. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| “Design Thinking es solo llenar post-its de colores.” | “Los post-its son el envase. El método es *entender antes de resolver* e *iterar con el usuario*. Sin usuario, es manualidad.” |
| “Ya sé la solución, ¿para qué idear más?” | “Porque tu primera idea es la más obvia y la que ya existe. La divergencia te da 2 alternativas mejores en 10 minutos.” |
| “Mi HMW es: ¿cómo hago una app?” | “Eso ya es una solución disfrazada de pregunta. Reescríbelo: ¿cómo podríamos [resultado] para [usuario]? La app quizá ni sea la respuesta.” |
| “Prototipar es programar la versión 1.” | “No. Prototipar es lo más barato que responde tu duda más cara. Un dibujo en Excalidraw es un prototipo válido hoy.” |
| “Esa idea es ridícula, no la anoto.” | “Anótala igual. La idea rara #7 casi siempre destraba la idea seria #8.” |

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Encuadre + puente desde la sesión anterior (~6 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**Objetivo de la fase:** conectar la observación/empatía que traen con el reto de hoy (definir un HMW e idear) y dejar claro el entregable de la hora.

**GUION LITERAL:**
> “Buenas tardes. Hoy es la **Sesión {n:02d}** y el tema es **Design Thinking y técnicas de creatividad**. La sesión pasada salieron con evidencia de empatía —una observación real o unas notas de su usuario— y con sus bloqueadores. Hoy convertimos eso en dos cosas concretas: un **How Might We** bien redactado y un **banco de al menos 8 ideas** con 1 o 2 elegidas.”

> “Miren la **slide 2 — OBJETIVOS**. No venimos a llenar post-its bonitos: venimos a practicar un músculo —abrir muchas ideas y luego cerrar con criterio— que van a usar toda su vida profesional. Al final de la hora, su Propuesta de Innovación tendrá un reto claro y un primer boceto.”

**Qué hacer:**
1. (2 min) Portada + control de audio/nombres en Meet.
2. (2 min) Leer objetivos (slide 2) y recordar en una línea qué trajeron de la sesión anterior.
3. (2 min) Pedir en el chat de Meet que 2 personas peguen su observación de usuario en una frase.

---

#### 2️⃣ Design Thinking + divergente/convergente (~13 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) → 4 (ENFOQUE DE HOY)

**Objetivo de la fase:** que entiendan el ciclo DT y, sobre todo, que **divergir y converger son dos momentos distintos** que no se mezclan.

**GUION LITERAL:**
> “**Slide 3.** Design Thinking no es un póster bonito: es un ciclo para **no enamorarnos de la primera solución**. Empatizar → Definir → Idear → Prototipar → Evaluar. Y ojo: no es una escalera, es un ciclo. Uno prueba, descubre que el problema estaba mal y vuelve atrás. Eso no es perder tiempo, es el método haciendo su trabajo.”

> “La regla de oro de hoy está en la **slide 4**: primero **divergimos** —muchas ideas, cero juicios— y **después** convergemos —elegimos con criterios—. Si juzgan mientras idean, es como manejar con el freno de mano puesto. Imagínense una lluvia de ideas donde cada propuesta recibe un ‘eso no sirve’: a los dos minutos nadie habla. Por eso separamos los momentos: ahora abrimos, luego cerramos.”

> “Y para pasar del problema a las ideas usamos una bisagra: el **How Might We**. La fórmula es ‘¿Cómo podríamos [acción] para [usuario] de modo que [resultado]?’. Ejemplo del laboratorio: en vez de ‘¿cómo hago una app?’, decimos ‘¿cómo podríamos reducir la incertidumbre de reserva para que el estudiante no pierda su hora de práctica?’. ¿Ven la diferencia? La segunda deja espacio para muchas soluciones; la primera ya me encerró en una.”

**Qué hacer:**
1. (5 min) Explicar el ciclo de 5 etapas con la tabla del fundamento.
2. (4 min) Explicar el doble diamante: abrir/cerrar dos veces; insistir en “prohibido juzgar” durante la divergencia.
3. (4 min) Enseñar la fórmula HMW con el ejemplo del laboratorio y un contraejemplo (“¿cómo hago una app?”).

---

#### 3️⃣ Modelación de ideación — HMW + SCAMPER (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**Objetivo de la fase:** mostrar en vivo cómo se generan muchas ideas sin juzgar y cómo se filtran después con criterios.

**Modelar EN VIVO** (en Excalidraw o una plantilla free de Miro, compartiendo pantalla): escriba **1 HMW** y genere **en voz alta 10 ideas** mezclando serias y disparatadas —incluya 2 absurdas a propósito—. Luego pase a SCAMPER una o dos preguntas (“¿y si *eliminamos* el paso de reserva?”). Al final, **converja**: filtre a 2 ideas usando tres criterios visibles en pantalla —impacto en el dolor, factibilidad en el semestre, aprendizaje rápido—.

**GUION LITERAL:**
> “Miren cómo se hace. Este es mi HMW —lo escribo aquí— y ahora voy a soltar diez ideas sin filtrar. Algunas van a ser malas a propósito: ‘un semáforo gigante en la puerta del laboratorio’, ‘un mayordomo que asigna equipos’… Anótenlas todas. ¿Por qué? Porque la idea del mayordomo, si le quito lo absurdo, es en realidad ‘asignación automática por horario’. La idea loca destrabó una seria.”

> “Ahora **convergemos**. De estas diez, me quedo con dos usando tres criterios que escribo aquí en pantalla: ¿cuánto alivia el dolor?, ¿la puedo probar este semestre?, ¿aprendo rápido si la muestro? La que no pase ningún criterio, la suelto sin culpa.”

**Qué hacer:**
1. (7 min) Generar 10 ideas en pantalla sin juzgar; aplicar 1–2 preguntas SCAMPER.
2. (5 min) Converger a 2 ideas con los tres criterios visibles; pensar en voz alta al descartar.

---

#### 4️⃣ Taller: ideación sobre su problema (~22 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL (consigna):**
> “Pasamos a la **slide 5 — TALLER**. Tienen **22 minutos** y trabajan sobre SU problema. Cuatro pasos: (1) redacten **su HMW** con la fórmula de la pizarra; (2) generen **mínimo 8 ideas** —solos o en dúo— sin juzgar ninguna; (3) **elijan 1 o 2** y justifíquenlas con los tres criterios; (4) hagan un **boceto de 1 minuto** en Excalidraw —cajitas y flechas, feo está bien—. Al final le pido a **tres personas** que lean **solo su HMW** en 20 segundos. Criterio de éxito: si su HMW menciona al usuario y el dolor —y no la tecnología— vamos bien.”

**Tabla de acompañamiento:**

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe el HMW empezando por la tecnología | “Bórralo y empieza por el usuario: ¿para quién y para aliviar qué?” |
| Se queda con 3 ideas y dice “ya no hay más” | “Usa SCAMPER: ¿qué pasa si combinas dos? ¿si eliminas un paso? Sácame 5 más.” |
| Juzga sus propias ideas mientras las escribe | “Ahora estamos abriendo. Anota todo, hasta lo ridículo; filtramos en 5 minutos.” |
| Elige la idea sin justificar | “¿Con qué criterio la elegiste: alivia el dolor, es factible o aprendes rápido?” |
| No sabe dibujar el boceto | “No es arte: son cajitas y flechas. En 60 segundos, ¿cómo se ve el flujo?” |

---

#### 5️⃣ Cierre + trabajo autónomo (~7 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Tres ideas de hoy: (1) **primero entiendo, después resuelvo**; (2) **divergir y converger son momentos distintos**, no los mezclo; (3) un buen **HMW** mira al usuario, no a la tecnología.”

> “**Slide 6 — PARA CONTINUAR.** Trabajo autónomo: (a) suban a CDigital su HMW + banco de ideas + boceto como `S03_Ideacion_Apellido`; (b) mejoren el boceto con una segunda mirada; (c) traigan a la próxima sesión una **clasificación tentativa** de su idea en un tipo de innovación —producto, proceso, organización, marketing o social—, que es justo lo que veremos con el Manual de Oslo.”

> “**Slide 7 — Cierre.** La próxima clase es **Gestión de la innovación con el Manual de Oslo**. Mismo Meet. Buen trabajo.”

**Qué hacer:**
1. (3 min) Recoger 3 HMW en voz alta y corregir amablemente si empiezan por la tecnología.
2. (2 min) Enunciar el trabajo autónomo y el nombre del archivo.
3. (2 min) Anunciar el tema de la próxima sesión.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Ideación DT (HMW + banco de ideas + boceto) — insumo de la Propuesta de Innovación.

1. Redactar el HMW con la fórmula usuario/dolor/resultado.
2. Generar mínimo 8 ideas (divergencia) y elegir 1–2 con tres criterios (convergencia).
3. Boceto de 1 minuto en Excalidraw (o plantilla free de Miro).
4. **Criterio de éxito:** el HMW se centra en usuario y dolor (no en “hacer una app”).
5. **Entregable:** `S03_Ideacion_Apellido` en CDigital (HMW + ideas + captura del boceto).
6. **Trabajo autónomo:** clasificación tentativa del tipo de innovación para la próxima sesión.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Tengo Excalidraw abierto (y una plantilla free de Miro como opción)
- [ ] Tengo listo mi HMW y mis 10 ideas modelo para la demostración
- [ ] Publiqué en CDigital el espacio de entrega `S03_Ideacion`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_04(meta):
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre + puente desde la sesión anterior", 5, 5),
        ("2️⃣ Gestionar la innovación + Manual de Oslo", 15, 20),
        ("3️⃣ Modelación: clasificar 3 casos en vivo", 12, 32),
        ("4️⃣ Taller: ficha Oslo de su propuesta", 20, 52),
        ("5️⃣ Cierre + trabajo autónomo", 8, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión**
1. **Explicar** qué significa *gestionar* la innovación (no solo “tener ideas”).
2. **Usar** el Manual de Oslo (OCDE) como lenguaje común para clasificar innovaciones.
3. **Clasificar** la propuesta del estudiante en un tipo dominante (+ secundario si aplica).
4. **Distinguir** novedad e implementación como condiciones para hablar de innovación.
5. **Definir** 2 actividades de gestión (quién, qué, cuándo) para su proyecto.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Este apartado asume que usted **no** conoce el Manual de Oslo. Léalo completo: la taxonomía de tipos y los ejemplos de aquí son los que usará para clasificar en vivo.

#### 1. Qué es “gestionar” la innovación
Gestionar la innovación **no** es tener un departamento mágico ni una lluvia de ideas los viernes. Es el conjunto de **decisiones, procesos y roles** que permiten pasar de ideas a **valor** de forma **repetible**: priorizar qué problema atacar, prototipar barato, medir aprendizaje, y decidir si se escala, se pivota o se mata.

La creatividad produce chispas; la gestión decide **cuáles chispas se convierten en fuego y cuáles se apagan a tiempo**. Un gestor de innovación se hace cuatro preguntas de forma disciplinada:

- ¿Qué problema **priorizamos** (y cuáles dejamos ir)?
- ¿Con qué **recursos** contamos (tiempo, datos, personas, dinero)?
- ¿Cómo **medimos aprendizaje** (no solo actividad)?
- ¿**Cuándo paramos** una idea que no funciona?

En Ingeniería esto es clave: muchos proyectos técnicamente brillantes mueren porque nadie gestionó el ritmo de validación. Gestionar **no** es hacer más reuniones; es imponer un **ritmo de aprendizaje**.

#### 2. Manual de Oslo (OCDE) — el idioma común
El **Manual de Oslo** es el documento de referencia de la **OCDE** que orienta cómo **medir y clasificar** la innovación en empresas y sistemas económicos. Para el aula no lo usamos como norma contable: lo usamos como **taxonomía**, un idioma común para no discutir en abstracto. En vez de pelear si algo “es innovador o no”, decimos **de qué tipo** es.

| Tipo | Cambio típico | Señal de que “sí es” ese tipo | Ejemplo en Ingeniería / negocio |
| :--- | :--- | :--- | :--- |
| **Producto** | Nuevo/mejorado bien o servicio | El usuario percibe una función nueva | Módulo o app que resuelve un dolor concreto |
| **Proceso** | Método de producción/entrega | Baja el tiempo, el error o el costo | Automatizar pruebas o el despliegue de software |
| **Organización** | Prácticas, roles, relaciones | El equipo se coordina distinto | Pasar de sprints caóticos a Kanban con rituales |
| **Marketing** | Diseño, precio, promoción, plaza | Cambia la adopción o el posicionamiento | Nuevo canal de onboarding para un servicio digital |
| **Social** | Valor público/comunitario | Mejora un bien común medible | App gratuita que articula a la comunidad con la alcaldía |

> Nota: la versión más reciente del manual (2018) agrupa en **producto** y **proceso de negocio**; en este curso mantenemos las cinco categorías porque son más fáciles de usar como vocabulario y porque nos interesa visibilizar el impacto **social**.

#### 3. Novedad + implementación (las dos condiciones)
Oslo insiste en dos cosas que el estudiante suele olvidar: **novedad** (algo nuevo o significativamente mejorado, al menos para la firma o el mercado) e **implementación** (se puso en marcha, no quedó en la diapositiva). Una idea en PowerPoint **no es** una innovación: es una intención. Por eso en el curso el estudiante debe apuntar, como mínimo, a un **prototipo o piloto pequeño** que demuestre que la idea salió del papel.

#### 4. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| “Innovación = tecnología nueva, ¿no?” | “No. Cambiar la forma de coordinar un equipo (organización) o de entregar (proceso) es innovación sin ningún gadget.” |
| “Mi proyecto es de todos los tipos.” | “Puede tener capas, pero elige **uno dominante**. En sustentación defiendes un eje, no cinco a la vez.” |
| “Es un producto tech” (cuando el cambio real es de proceso) | “¿Qué cambia para el usuario: una función nueva o que el proceso tarda menos? Si es lo segundo, es proceso, no producto.” |
| “Gestionar es hacer más reuniones.” | “Gestionar es imponer un **ritmo de aprendizaje**: prototipar, medir, decidir. Una reunión sin decisión no gestiona nada.” |
| “Ya lo pensé bien, con eso basta.” | “Oslo pide **implementación**. Sin un piloto o prototipo, sigues teniendo una idea, no una innovación.” |

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Encuadre + puente desde la sesión anterior (~5 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**Objetivo de la fase:** enlazar la idea elegida en la sesión de Design Thinking con la clasificación de hoy.

**GUION LITERAL:**
> “Buenas tardes. **Sesión {n:02d}**: **Gestión de la innovación con el Manual de Oslo**. La sesión pasada eligieron una o dos ideas para su propuesta. Hoy hacemos dos cosas: le ponemos **nombre** a esa innovación con el idioma de Oslo y le ponemos **gestión mínima** —quién hace qué esta semana—.”

> “Miren la **slide 2 — OBJETIVOS**. La meta de la hora es que salgan con una **ficha Oslo** de su propuesta: tipo dominante, novedad, valor y dos actividades de gestión con fecha.”

**Qué hacer:**
1. (2 min) Portada + control de audio/nombres en Meet.
2. (2 min) Leer objetivos (slide 2).
3. (1 min) Pedir a 1–2 estudiantes que recuerden en una frase la idea que eligieron.

---

#### 2️⃣ Gestionar la innovación + Manual de Oslo (~15 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) → 4 (ENFOQUE DE HOY)

**Objetivo de la fase:** que entiendan qué es gestionar y que dominen la taxonomía de cinco tipos.

**GUION LITERAL:**
> “**Slide 3.** Empecemos por gestionar. Gestionar la innovación es ponerle **ritmo y criterio** a la creatividad. La creatividad da chispas; la gestión decide cuáles se vuelven fuego y cuáles se apagan a tiempo. No es hacer más reuniones: es priorizar, prototipar, medir y decidir cuándo parar.”

> “Ahora el idioma común. El **Manual de Oslo**, de la OCDE, nos da nombres para no pelear en abstracto sobre si algo ‘es innovador’. Son cinco tipos: **producto** —una función nueva que el usuario percibe—; **proceso** —hago o entrego con menos tiempo, error o costo—; **organización** —me coordino distinto, como pasar de sprints caóticos a Kanban—; **marketing** —cambio cómo llego o me posiciono—; y **social** —genero un valor público medible—.”

> “**Slide 4.** Y dos condiciones que casi todos olvidan: **novedad** e **implementación**. Una idea en PowerPoint no es innovación, es una intención. Para que cuente, tiene que salir del papel: aunque sea un prototipo pequeñito, algo que se pueda mostrar y usar.”

**Qué hacer:**
1. (6 min) Explicar qué es gestionar con las 4 preguntas de gestor.
2. (7 min) Recorrer la tabla de 5 tipos con **1 ejemplo de Ingeniería por fila** (prepárelos antes).
3. (2 min) Recalcar novedad + implementación con la frase “una idea en PPT no es innovación”.

---

#### 3️⃣ Modelación: clasificar 3 casos en vivo (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**Objetivo de la fase:** que vean cómo se clasifica y por qué a veces hay tipo dominante + secundario.

Abra una **tabla en Google Docs** compartiendo pantalla (o Excalidraw). Presente 3 mini-casos y pida por el chat de Meet: ¿producto / proceso / organización / marketing / social?

1. Una empresa pasa de sprints caóticos a **Kanban con rituales** → **organización** (+ proceso).
2. Una universidad lanza un **chatbot de matrícula** → **producto** (servicio digital).
3. Una **app gratuita para reportar huecos en las vías**, articulada con la alcaldía → **social** (+ producto).

**GUION LITERAL:**
> “Vamos a clasificar juntos. Caso 1: la empresa no cambió su producto ni su tecnología; cambió **cómo se coordina la gente**. Eso es **organización**, con algo de proceso. Caso 2: aparece un servicio nuevo que el usuario usa —el chatbot—; eso es **producto**. Caso 3: la app existe, sí, pero lo importante es el **bien común** que genera al conectar ciudadanos con la alcaldía; el eje es **social**, apoyado en un producto.”

> “Fíjense en algo: casi todos tienen un tipo **dominante** y uno **secundario**. Ustedes van a defender el dominante en su sustentación; el secundario es un matiz, no una excusa para no decidir.”

**Qué hacer:**
1. (8 min) Clasificar los 3 casos con participación por el chat; escribir la respuesta en la tabla.
2. (4 min) Mostrar por qué cada caso tiene dominante + secundario.

---

#### 4️⃣ Taller: ficha Oslo de su propuesta (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL (consigna):**
> “Pasamos a la **slide 5 — TALLER**. Tienen **20 minutos**. Completen la **Ficha Oslo** de su propuesta en Google Docs o Excalidraw con seis campos: (1) **tipo dominante**; (2) tipo **secundario** opcional; (3) **novedad** —¿nueva para quién: para usted, para el campus, para el mercado?—; (4) **valor esperado** en una frase; (5) **dos actividades de gestión** con responsable y fecha; (6) **riesgo #1**. Al final leo tres fichas en voz alta. Criterio de éxito: el tipo dominante está **justificado** y las dos actividades tienen **fecha real**.”

**Tabla de acompañamiento:**

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Dice “es de todos los tipos” | “Elige **uno dominante**. ¿Qué es lo que más cambia: la función, el proceso o la coordinación?” |
| Marca “producto” pero el cambio es de flujo | “¿El usuario ve una función nueva o el proceso tarda menos? Si es lo segundo, es proceso.” |
| Deja las actividades sin fecha | “Una actividad sin fecha no es gestión, es deseo. ¿Qué día y quién?” |
| No sabe la novedad | “Novedad no es ‘es único en el mundo’. Basta con: nueva para el campus, para tu área o para tu usuario.” |
| Confunde valor con la función técnica | “El valor es lo que gana el usuario —tiempo, dinero, tranquilidad—, no la característica técnica.” |

---

#### 5️⃣ Cierre + trabajo autónomo (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Tres ideas de hoy: (1) gestionar innovación es imponer **ritmo y criterio**, no hacer más reuniones; (2) el Manual de Oslo nos da **cinco tipos** para hablar el mismo idioma; (3) sin **novedad e implementación**, sigue siendo una idea, no una innovación.”

> “**Slide 6 — PARA CONTINUAR.** Autónomo: (a) suban su ficha como `S04_FichaOslo_Apellido` a CDigital; (b) traigan a la próxima sesión un **cuadro comparativo** de su tipo elegido contra un tipo alternativo que descartaron, explicando **por qué no**.”

> “**Slide 7 — Cierre.** La próxima clase profundizamos en los **tipos de innovación** y en incremental vs. radical. Mismo Meet. Gracias.”

**Qué hacer:**
1. (4 min) Leer 3 fichas Oslo y corregir clasificaciones dudosas con amabilidad.
2. (2 min) Enunciar el trabajo autónomo y el nombre del archivo.
3. (2 min) Anunciar el tema de la próxima sesión.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Ficha Oslo de la propuesta — insumo de la Propuesta de Innovación.

1. Clasificar la propuesta en un tipo dominante (+ secundario opcional).
2. Definir novedad, valor y dos actividades de gestión con responsable y fecha.
3. **Criterio de éxito:** tipo dominante justificado + 2 actividades **fechadas**.
4. **Entregable:** `S04_FichaOslo_Apellido` en CDigital.
5. **Trabajo autónomo:** cuadro comparativo de tipo elegido vs. tipo descartado.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Preparé 1 ejemplo de Ingeniería por cada tipo Oslo
- [ ] Tengo la tabla de Google Docs (o Excalidraw) lista para clasificar en vivo
- [ ] Publiqué en CDigital el espacio de entrega `S04_FichaOslo`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_05(meta):
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre + puente desde la sesión anterior", 5, 5),
        ("2️⃣ Profundizar tipos + incremental/radical", 14, 19),
        ("3️⃣ Modelación con matriz comparativa", 12, 31),
        ("4️⃣ Taller: matriz de su propuesta", 21, 52),
        ("5️⃣ Cierre + trabajo autónomo", 8, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión**
1. **Comparar** los tipos de innovación usando criterios comunes (no gusto personal).
2. **Distinguir** innovación incremental vs. radical, sin mitificar lo radical.
3. **Argumentar** por qué el tipo elegido encaja en un contexto socio-económico real.
4. **Producir** una matriz comparativa lista para la validación de la siguiente unidad.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Este apartado asume que usted **no** es especialista. La clase pasada se clasificó el tipo; hoy el reto es más fino: **argumentar** la elección comparándola con una alternativa. Léalo completo.

#### 1. De clasificar a argumentar (repaso activo de tipos)
En la sesión anterior el estudiante puso una **etiqueta** Oslo a su propuesta (producto, proceso, organización, marketing o social). Hoy no repetimos etiquetas: las **defendemos**. Dos matices que debe dejar claros:

- Un mismo proyecto suele tener **capas** (varios tipos a la vez), pero en sustentación se defiende **un eje**. Tener capas no exime de decidir cuál es el dominante.
- **“Digitalizar” no define el tipo.** Poner algo en una app no dice nada por sí solo. Hay que decir **qué cambia**: ¿el servicio que recibe el usuario (producto)?, ¿el método de trabajo (proceso)?, ¿la coordinación del equipo (organización)? La palabra “digital” es el envase, no el tipo.

#### 2. Incremental vs. radical (y por qué no idolatrar lo radical)
Otra dimensión, ortogonal a los tipos Oslo, es el **grado** de la innovación:

| | Incremental | Radical |
| :--- | :--- | :--- |
| Cambio | Mejora paso a paso sobre lo que ya existe | Rompe las reglas del juego / crea una categoría |
| Riesgo | Menor, más predecible | Mayor, más incierto |
| Evidencia posible en un semestre | Alta (se puede medir la mejora) | Baja (requiere apuestas grandes) |
| Ejemplo | Reducir 30% el tiempo de onboarding | Un modelo que elimina por completo al intermediario |

El mensaje que debe transmitir: en un **semestre**, una innovación **incremental bien ejecutada y medida** casi siempre es más defendible que una “radical” sin evidencia. Muchos estudiantes escriben “mi innovación es radical” como adorno; ayúdelos a ver que **lo radical sin datos es solo una ilusión ambiciosa**, y que mejorar de verdad un 30% ya es un logro real.

#### 3. Contexto socio-económico (la prueba de realidad)
Una innovación que ignora sus restricciones es **ficción**. Antes de comparar tipos, pida ubicar cuatro cosas:

- **¿Quién paga?** (usuario, empresa, Estado, publicidad, nadie —y entonces cómo se sostiene—).
- **¿Quién usa?** (puede no ser el mismo que paga).
- **¿Qué restricción real hay?** (tiempo, dinero, norma, conectividad, cultura).
- **¿Qué beneficio socio-económico** genera? (ahorro, empleo, inclusión, reducción de riesgo).

En Ingeniería es frecuente enamorarse de la elegancia técnica y olvidar que si nadie paga ni la restricción legal lo permite, la mejor arquitectura del mundo no se implementa.

#### 4. Cómo se compara con criterios (no con gusto)
Comparar “bien” significa poner los **mismos criterios** a las dos opciones. Criterios útiles: **impacto en el dolor**, **esfuerzo/costo**, **evidencia posible este semestre**, **riesgo** y **beneficio socio-económico**. Se puntúa cada criterio (por ejemplo, alto/medio/bajo) para **ambos** tipos, y la conclusión sale de la comparación, no de la preferencia.

#### 5. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| “Mi innovación es radical” (como adorno) | “¿Qué regla del juego rompe y con qué evidencia? Si no la tienes, es incremental ambiciosa, y está bien.” |
| “Es innovación porque es digital / usa IA” | “Digital es el envase. ¿Qué cambia para el usuario: el servicio, el proceso o la coordinación?” |
| Compara tipos “porque me gusta más uno” | “Gusto no es criterio. Pon los mismos 5 criterios a ambos y que decida la comparación.” |
| Olvida quién paga y quién usa | “Una innovación sin modelo de sostenibilidad es un hobby caro. ¿Quién paga y quién usa?” |
| Pierde de vista al usuario del problema inicial | “Vuelve a tu ficha del primer día: ¿este tipo sigue aliviando el dolor de ESE usuario?” |

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Encuadre + puente desde la sesión anterior (~5 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**Objetivo de la fase:** subir la exigencia de clasificar a argumentar.

**GUION LITERAL:**
> “Buenas tardes. **Sesión {n:02d}**: **Tipos de innovación**. La clase pasada le pusimos una etiqueta Oslo a su propuesta. Hoy subimos el nivel: no basta con la etiqueta, hay que **argumentar por qué ese tipo y no otro**.”

> “Miren la **slide 2 — OBJETIVOS**. Salimos de la hora con una **matriz comparativa**: su tipo elegido contra una alternativa, con criterios claros y una conclusión escrita.”

**Qué hacer:**
1. (2 min) Portada + control de audio/nombres en Meet.
2. (2 min) Leer objetivos (slide 2).
3. (1 min) Recordar en una frase el tipo que cada quien eligió la sesión anterior.

---

#### 2️⃣ Profundizar tipos + incremental/radical (~14 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) → 4 (ENFOQUE DE HOY)

**Objetivo de la fase:** distinguir tipo (qué cambia) de grado (cuánto rompe) y anclar el contexto socio-económico.

**GUION LITERAL:**
> “**Slide 3.** Repasemos, pero activos. Los tipos —producto, proceso, organización, marketing, social— dicen **qué cambia**. Cuidado con la trampa: ‘lo hago digital’ no define nada. Digital es el envase. Díganme si cambia el servicio, el método o la coordinación.”

> “Ahora una segunda dimensión que va aparte: el **grado**. **Incremental** es mejorar paso a paso; **radical** es romper las reglas del juego. En un semestre, una mejora incremental bien medida —‘bajé el tiempo de reserva un 30%’— es mucho más defendible que un ‘esto es revolucionario’ sin un solo dato. No idolatren lo radical.”

> “**Slide 4.** Y la prueba de realidad: ¿quién paga?, ¿quién usa?, ¿qué restricción hay —tiempo, dinero, norma, conectividad—? Una innovación que ignora sus restricciones es ficción, por más elegante que sea la ingeniería.”

**Qué hacer:**
1. (6 min) Repasar los 5 tipos insistiendo en “qué cambia, no el envase digital”.
2. (5 min) Explicar incremental vs. radical con 2 ejemplos locales (campus, pyme, servicio público).
3. (3 min) Introducir las 4 preguntas de contexto socio-económico.

---

#### 3️⃣ Modelación con matriz comparativa (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**Objetivo de la fase:** mostrar cómo se llena y cómo se lee una matriz de comparación.

Llene en pantalla (Excalidraw o Google Docs) una **matriz de criterios × 2 opciones**: filas = criterios; columnas = **Tipo A (elegido)** vs. **Tipo B (alternativa descartada)**. Use el caso del laboratorio de turnos.

| Criterio | Tipo A: Proceso (reserva) | Tipo B: Producto (app nueva) |
| :--- | :--- | :--- |
| Impacto en el dolor | Alto | Alto |
| Esfuerzo / costo | Bajo | Alto |
| Evidencia este semestre | Alta | Media |
| Riesgo | Bajo | Alto |
| Beneficio socio-económico | Medio | Medio |

**GUION LITERAL:**
> “Fíjense cómo decido. Con los mismos criterios, el **proceso** me da la misma reducción del dolor que la **app nueva**, pero con menos esfuerzo y más evidencia este semestre. Entonces mi conclusión no es ‘me gusta más’: es ‘el tipo A gana en esfuerzo, evidencia y riesgo con impacto equivalente’. Eso es argumentar.”

**Qué hacer:**
1. (7 min) Construir la matriz en vivo, puntuando cada criterio para las dos opciones.
2. (5 min) Escribir la conclusión de 3–4 líneas mostrando de dónde sale.

---

#### 4️⃣ Taller: matriz de su propuesta (~21 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL (consigna):**
> “Pasamos a la **slide 5 — TALLER**. Tienen **21 minutos**. Armen su **Matriz comparativa**: su **tipo elegido** contra un **tipo alternativo** que descartaron. Mínimo **5 criterios**. Terminen con una **conclusión de 4 líneas** que explique, con base en los criterios, por qué se quedan con el tipo A. Al final, dos personas leen solo su conclusión. Criterio de éxito: la conclusión se apoya en los criterios, no en ‘me gusta más’.”

**Tabla de acompañamiento:**

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Compara sin criterios explícitos | “Escribe primero las filas de criterios; sin ellas es opinión, no comparación.” |
| Pone el mismo puntaje a todo | “Si todo empata, tu comparación no discrimina. Sé honesto: ¿dónde de verdad difieren?” |
| Insiste en que su idea es radical | “Muéstrame la evidencia de que rompe la regla. Si no la hay, compáralo como incremental.” |
| Olvida el contexto socio-económico | “Agrega una fila: ¿quién paga y quién usa? Eso mueve la decisión.” |
| No logra concluir | “Mira qué columna gana en más criterios de peso. Esa es tu conclusión, en 4 líneas.” |

---

#### 5️⃣ Cierre + trabajo autónomo (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Tres ideas de hoy: (1) el **tipo** dice qué cambia, el **grado** dice cuánto rompe; (2) **incremental bien medido** vence a radical sin evidencia; (3) se compara con **criterios**, no con gusto.”

> “**Slide 6 — PARA CONTINUAR.** Autónomo: (a) suban su matriz como `S05_MatrizTipos_Apellido`; (b) preparen un listado de **mínimo 5 supuestos** que su propuesta da por verdaderos —cosas que, si fueran falsas, tumbarían el proyecto—. Eso lo vamos a validar la próxima sesión.”

> “**Slide 7 — Cierre.** La próxima clase es **Análisis de negocios: FODA, Canvas, MVP y validación**. Mismo Meet. Gracias.”

**Qué hacer:**
1. (4 min) Leer 2 conclusiones y verificar que se apoyan en criterios.
2. (2 min) Enunciar el trabajo autónomo (los 5 supuestos) y el nombre del archivo.
3. (2 min) Anunciar el tema de la próxima sesión.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Matriz comparativa de tipos — insumo de la Propuesta de Innovación.

1. Comparar tipo elegido vs. tipo alternativo con mínimo 5 criterios.
2. Escribir una conclusión de 4 líneas basada en la comparación.
3. **Criterio de éxito:** criterios explícitos + conclusión argumentada (no gusto personal).
4. **Entregable:** `S05_MatrizTipos_Apellido` en CDigital.
5. **Trabajo autónomo:** listado de mínimo 5 supuestos para la validación de la próxima sesión.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Preparé 2 ejemplos locales de incremental vs. radical
- [ ] Tengo la matriz del caso laboratorio lista para llenar en vivo (Excalidraw/Docs)
- [ ] Publiqué en CDigital el espacio de entrega `S05_MatrizTipos`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_06(meta):
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre + puente desde la sesión anterior", 5, 5),
        ("2️⃣ FODA + Business Model Canvas + MVP", 14, 19),
        ("3️⃣ Modelación de validación (supuesto → prueba)", 12, 31),
        ("4️⃣ Taller: mini-Canvas + plan MVP", 22, 53),
        ("5️⃣ Cierre + pista de sustentación", 7, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión**
1. **Usar** el FODA como radiografía rápida y verificable (sin prosa vacía).
2. **Completar** un Business Model Canvas **mínimo** centrado en la propuesta de valor.
3. **Definir** un MVP (producto mínimo viable) de **aprendizaje**, no una “app completa”.
4. **Diseñar** una prueba de validación para el supuesto más riesgoso, con criterio de éxito medible.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Este apartado asume que usted **no** viene de negocios. Léalo completo: FODA, Canvas, MVP y la cadena de validación son las herramientas con las que la propuesta deja de ser un ensayo y empieza a sostenerse.

#### 1. FODA (DAFO) — la radiografía rápida
**FODA** = **F**ortalezas, **O**portunidades, **D**ebilidades, **A**menazas. Fortalezas y Debilidades son **internas** (dependen de usted/su equipo); Oportunidades y Amenazas son **externas** (del entorno). Regla de oro: cada ítem debe ser **específico y verificable**, no un adjetivo bonito.

- Mal: “Fortaleza: somos creativos.” (no se puede verificar).
- Bien: “Fortaleza: tenemos acceso a 30 usuarios del laboratorio esta semana.” (concreto y comprobable).

Un FODA de 6 bullets bien escritos vale más que uno de 20 frases genéricas. Su función no es decorar: es **decidir dónde apoyarse y qué vigilar**.

#### 2. Business Model Canvas (Osterwalder) — foco de aula
El **Business Model Canvas (BMC)** de Alexander Osterwalder es un lienzo de **9 bloques** que describe cómo una propuesta **crea, entrega y captura valor**. No exija una obra maestra; en una hora priorice los bloques que más aclaran la propuesta:

| # | Bloque | Pregunta clave |
| :--- | :--- | :--- |
| 1 | **Segmento de clientes** | ¿Para quién es (quién usa)? |
| 2 | **Propuesta de valor** | ¿Qué dolor alivia o qué gana el usuario? |
| 3 | **Canales** | ¿Cómo llega la propuesta al usuario? |
| 4 | **Relación con el cliente** | ¿Cómo se capta y se retiene? |
| 5 | **Actividades clave** | ¿Qué hay que hacer sí o sí? |
| 6 | **Recursos clave** | ¿Qué se necesita (datos, gente, infra)? |
| 7 | **Socios clave** | ¿Quién ayuda desde afuera? |
| 8 | **Estructura de costos** | ¿Qué cuesta (aunque sea cualitativo)? |
| 9 | **Fuentes de ingreso** | ¿Quién paga o cómo se sostiene (si es social)? |

En clase se trabaja en **Canvanizer** (https://canvanizer.com/new/business-model-canvas, gratis, en la nube). **Strategyzer** solo se muestra como referencia visual; el trabajo real se hace en Canvanizer, Excalidraw o Google Docs. Prioridad mínima de hoy: **propuesta de valor, segmento, canales y actividades clave**.

#### 3. MVP — Producto Mínimo Viable (de aprendizaje)
El **MVP** es la versión **más pequeña** que permite **aprender** de un usuario real. **No** es “la app fea pero completa” ni “la fase 1 del software grande”. Ejemplos válidos y baratos:

- Una **landing page** con un botón y una lista de espera (¿cuánta gente se anota?).
- Un **prototipo clicable** (pantallas enlazadas, sin backend).
- Un **piloto manual tipo “concierge”**: usted hace a mano lo que después haría el sistema, para ver si el usuario lo valora.
- Un **storyboard** probado con 5 usuarios.

La pregunta que responde un MVP no es “¿funciona el código?”, sino “¿esto le importa a alguien?”.

#### 4. La cadena de validación
Validar es una cadena corta y disciplinada:

**Supuesto → Riesgo si es falso → Prueba → Criterio de éxito → Decisión (seguir / pivotar / parar)**

Se empieza por el supuesto **más riesgoso**: aquel que, si es falso, tumba el proyecto. No se valida con opiniones de amigos; se valida con el **segmento real** y un **criterio medible u observable** definido de antemano (para no “ver lo que quiero ver”).

#### 5. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| “Mi FODA: fortaleza, somos creativos.” | “Eso no se verifica. Cámbialo por un hecho: ‘acceso a 30 usuarios esta semana’.” |
| “El MVP es la app terminada pero sin diseño.” | “No. El MVP es lo más barato que responde tu duda más cara. Una landing o un prototipo en papel sirve.” |
| “Ya validé: a mis amigos les gustó.” | “Tus amigos no son el segmento y no te dirán que no. Prueba con usuarios reales y un criterio medible.” |
| “Lleno el Canvas con frases generales.” | “Un Canvas genérico no decide nada. Sé concreto en propuesta de valor y segmento.” |
| “¿Para qué elegir un solo supuesto?” | “Porque el tiempo es finito. Valida primero el que, si es falso, tumba todo el proyecto.” |

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Encuadre + puente desde la sesión anterior (~5 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**Objetivo de la fase:** anunciar que hoy la propuesta pasa de idea argumentada a idea **sostenible y validada**.

**GUION LITERAL:**
> “Buenas tardes. **Sesión {n:02d}**: **Análisis de negocios y validación**. Aquí la propuesta deja de ser un ensayo y empieza a **sostenerse**: con un FODA honesto, un Canvas mínimo y —lo más importante— una **prueba** al supuesto más peligroso. La sesión pasada les pedí una lista de supuestos; hoy elegimos el más riesgoso y lo ponemos a prueba.”

> “Miren la **slide 2 — OBJETIVOS**. Salen de la hora con un mini-Canvas, un MVP descrito en 5 líneas y una prueba de validación con criterio de éxito medible.”

**Qué hacer:**
1. (2 min) Portada + control de audio/nombres en Meet.
2. (2 min) Leer objetivos (slide 2).
3. (1 min) Pedir a 1–2 estudiantes que lean uno de sus supuestos.

---

#### 2️⃣ FODA + Business Model Canvas + MVP (~14 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) → 4 (ENFOQUE DE HOY)

**Objetivo de la fase:** que sepan qué es cada herramienta y para qué sirve, sin convertirlo en teoría de administración.

**GUION LITERAL:**
> “**Slide 3.** Tres herramientas, una detrás de otra. Primero el **FODA**: cuatro cajas —fortalezas y debilidades internas, oportunidades y amenazas externas—. Regla única: cada frase debe poderse verificar. ‘Somos creativos’ no vale; ‘tengo 30 usuarios a la mano esta semana’ sí.”

> “Segundo, el **Business Model Canvas**: nueve bloques que cuentan cómo su propuesta crea y entrega valor. Hoy no lleno los nueve; me concentro en cuatro que aclaran todo: **propuesta de valor, segmento, canales y actividades clave**. Lo trabajamos en Canvanizer, gratis y en el navegador.”

> “**Slide 4.** Y el **MVP**. Aquí está la analogía que quiero que recuerden: **no construyan el edificio entero para saber si alguien quiere vivir ahí; armen la maqueta que responde la duda más cara**. El MVP no es la app terminada; es lo más pequeño que me enseña si a alguien le importa: una landing con lista de espera, un prototipo clicable, un piloto hecho a mano.”

**Qué hacer:**
1. (5 min) Explicar FODA con la regla “específico y verificable”.
2. (6 min) Recorrer el Canvas priorizando 4 bloques; mencionar Canvanizer.
3. (3 min) Definir MVP con la analogía del edificio/maqueta.

---

#### 3️⃣ Modelación de validación: supuesto → prueba (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**Objetivo de la fase:** mostrar la cadena completa de validación con un ejemplo cronometrable.

Tome el caso del laboratorio de turnos y escriba en pantalla (Canvanizer/Excalidraw/Docs) la cadena:

- **Supuesto riesgoso:** “Los estudiantes registrarían la reserva si el flujo toma menos de 1 minuto.”
- **Riesgo si es falso:** nadie usa el sistema y el problema sigue igual.
- **Prueba:** 5 estudiantes cronometran un prototipo en papel o clicable.
- **Criterio de éxito:** ≥ 4 de 5 completan en menos de 60 s y dicen que lo usarían cada semana.
- **Decisión:** si pasa, seguir; si no, pivotar el flujo o parar.

**GUION LITERAL:**
> “Miren la cadena completa. No digo ‘voy a validar mi idea’ en abstracto. Digo: este es el supuesto que si es falso me hunde; esta es la prueba concreta; y —clave— **defino el criterio de éxito ANTES de probar**, para no engañarme viendo lo que quiero ver. Cuatro de cinco en menos de un minuto: pasa. Tres de cinco: no pasa, y toca pivotar.”

**Qué hacer:**
1. (7 min) Escribir la cadena supuesto → prueba → criterio → decisión en pantalla.
2. (5 min) Insistir en fijar el criterio de éxito antes de la prueba; pedir un ejemplo oral a un estudiante.

---

#### 4️⃣ Taller: mini-Canvas + plan MVP (~22 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL (consigna):**
> “Pasamos a la **slide 5 — TALLER**. Tienen **22 minutos**. Cuatro entregas: (1) un **FODA** de máximo 6 bullets en total, todos verificables; (2) un **Canvas mínimo** en Canvanizer con al menos propuesta de valor, segmento, canales y actividades clave; (3) su **MVP descrito en 5 líneas** —qué es lo mínimo que van a mostrar—; (4) **una prueba de validación** de su supuesto más riesgoso, con criterio numérico u observable. Al final dos personas comparten solo su prueba y su criterio. Éxito: la prueba tiene un criterio que se pueda medir.”

**Tabla de acompañamiento:**

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe un FODA con adjetivos vagos | “‘Somos buenos’ no se mide. Dame un hecho verificable para cada casilla.” |
| Describe el MVP como la app completa | “Recórtalo: ¿cuál es la versión más pequeña que te dice si a alguien le importa?” |
| Pone una prueba sin criterio de éxito | “¿Cómo sabrás si pasó? Fija el número o la observación ANTES de probar.” |
| Va a validar con amigos | “Tus amigos no son el segmento. ¿Quién es el usuario real que puedes tocar esta semana?” |
| Se pierde llenando los 9 bloques | “Hoy solo 4: valor, segmento, canales y actividades. El resto queda para después.” |

---

#### 5️⃣ Cierre + pista de sustentación (~7 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Tres ideas de hoy: (1) el **FODA** solo sirve si es verificable; (2) el **MVP** es la maqueta que responde la duda más cara, no el edificio; (3) validar es **supuesto → prueba → criterio → decisión**, con el criterio fijado antes.”

> “**Slide 6 — PARA CONTINUAR.** Autónomo: (a) suban su Canvas + MVP + prueba como `S06_CanvasMVP_Apellido`; (b) **ejecuten la prueba** aunque sea con 3 usuarios y traigan los resultados a la próxima sesión. Eso alimenta directamente su sustentación.”

> “**Slide 7 — Cierre.** La próxima clase es **Vigilancia tecnológica**, para que su MVP no viva en una burbuja. Mismo Meet. Gracias.”

**Qué hacer:**
1. (3 min) Escuchar 2 pruebas y verificar que tengan criterio medible.
2. (2 min) Enunciar el trabajo autónomo (ejecutar la prueba) y el nombre del archivo.
3. (2 min) Anunciar el tema de la próxima sesión.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Mini-Canvas + MVP + prueba de validación — insumo de la Propuesta de Innovación.

1. FODA de máximo 6 bullets verificables.
2. Canvas mínimo en Canvanizer (valor, segmento, canales, actividades).
3. MVP descrito en 5 líneas + 1 prueba del supuesto más riesgoso con criterio medible.
4. **Criterio de éxito:** supuesto riesgoso + prueba concreta + criterio de éxito definido de antemano.
5. **Entregable:** `S06_CanvasMVP_Apellido` en CDigital.
6. **Trabajo autónomo:** ejecutar la prueba con al menos 3 usuarios y traer resultados.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Abrí Canvanizer (https://canvanizer.com/new/business-model-canvas) para modelar en vivo
- [ ] Tengo la cadena de validación del caso laboratorio lista para escribir
- [ ] Publiqué en CDigital el espacio de entrega `S06_CanvasMVP`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_07(meta):
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre + puente desde la sesión anterior", 5, 5),
        ("2️⃣ Qué es vigilancia tecnológica + fuentes", 12, 17),
        ("3️⃣ Modelación: buscar y fichar una señal en vivo", 13, 30),
        ("4️⃣ Taller: tablero de vigilancia de su tema", 22, 52),
        ("5️⃣ Cierre + trabajo autónomo", 8, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión**
1. **Definir** vigilancia tecnológica y diferenciarla de “buscar en Google un rato”.
2. **Identificar** fuentes confiables (académicas, patentes, mercado, normativa).
3. **Registrar** al menos 3 señales o tendencias relevantes para su propuesta, con ficha.
4. **Decidir** un ajuste (o una confirmación) de la propuesta a partir de la evidencia hallada.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Este apartado asume que usted **no** ha hecho vigilancia tecnológica formal. Léalo completo: la diferencia entre “informarse” y “vigilar” es el corazón de la clase.

#### 1. Qué es (y qué no es) la vigilancia tecnológica
La **vigilancia tecnológica** es un proceso **sistemático** de **capturar, filtrar, analizar y usar** información sobre tecnologías, competidores, normas y tendencias, con un fin concreto: **decidir mejor**. La palabra clave es *sistemático*: no es leer un artículo suelto que apareció en el celular, es un método repetible.

La trampa más común es confundirla con “me informé”. Buscar en Google un rato **no** es vigilancia; es curiosidad. La vigilancia se distingue porque **cambia una decisión**: si después de mirar el entorno usted no ajusta ni confirma nada de su propuesta, no vigiló, solo leyó. El ciclo mínimo es:

**Observar → Analizar → Comunicar → Usar.**

Para un ingeniero esto es vital: evita reinventar lo que ya existe, detecta que una tecnología acaba de volverse viable (o barata), y anticipa una norma que puede habilitar o bloquear el proyecto.

#### 2. Tipos de señales y dónde buscarlas (fuentes gratis + web)
No todas las señales son técnicas. Conviene mirar cuatro frentes, todos con fuentes gratuitas y en el navegador:

| Tipo de señal | Fuentes gratis / web | Pregunta que responde |
| :--- | :--- | :--- |
| **Tecnología** | **Google Scholar** (scholar.google.com), **Google Patents** (patents.google.com), repos de GitHub, documentación oficial de IEEE/estándares | ¿Qué se volvió posible o barato? |
| **Mercado** | Reportes públicos, precios, notas de adopción, portales de datos abiertos | ¿Quién ya paga por esto y cuánto? |
| **Normativa** | Leyes, resoluciones, políticas institucionales, sitios de entidades públicas | ¿Qué me limita o me habilita? |
| **Social** | Hábitos, demografía, quejas públicas en redes/prensa | ¿Qué cambió en el usuario? |

**Google Patents** merece un párrafo: muchas soluciones ya están patentadas o documentadas ahí. Ver una patente parecida **no** mata la idea del estudiante; le obliga a decir **en qué se diferencia** la suya. **Google Scholar** da el estado del arte académico. En clase se usan sin login para lo básico; si aparece “tráfico inusual” en una búsqueda profunda, se sigue con el navegador normal del docente.

#### 3. La ficha de señal (para que la vigilancia sea utilizable)
Cada señal se registra en una ficha mínima —en Google Docs— para que sirva a la decisión:

- **Título de la señal.**
- **Fuente + fecha + enlace** (sin fecha ni autor, no vale).
- **Hallazgo en 2 líneas.**
- **Implicación para MI propuesta:** ¿confirma, obliga a pivotar, o es un riesgo?
- **Nivel de confianza:** alto / medio / bajo.

#### 4. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| “Ya vigilé: leí un artículo.” | “¿Cambió alguna decisión de tu propuesta? Si no, te informaste, no vigilaste.” |
| “Encontré una patente igual, mi idea murió.” | “Al contrario: ahora sabes contra qué compites. ¿En qué se diferencia la tuya?” |
| Pega un enlace sin fecha ni autor | “Una fuente sin fecha ni autor no es evidencia. Busca quién lo dice y cuándo.” |
| “Hay muchas apps parecidas.” | “‘Parecidas’ no es análisis. ¿En qué se parecen y en qué te diferencias tú?” |
| Vigilancia decorativa (no cambia nada) | “Si tu tablero no ajusta alcance, usuario, tecnología ni riesgo, todavía no sirve.” |

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Encuadre + puente desde la sesión anterior (~5 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**Objetivo de la fase:** conectar los resultados de validación con la mirada al entorno.

**GUION LITERAL:**
> “Buenas tardes. **Sesión {n:02d}**: **Vigilancia tecnológica**. La sesión pasada probaron su MVP con usuarios. Hoy levantamos la vista del prototipo y miramos el **entorno**: ¿qué tecnología, qué competidor, qué norma afecta su propuesta? La idea es que su MVP no viva en una burbuja.”

> “Miren la **slide 2 — OBJETIVOS**. Salen con un **tablero de al menos 3 señales** y, muy importante, con **una decisión** tomada a partir de ellas.”

**Qué hacer:**
1. (2 min) Portada + control de audio/nombres en Meet.
2. (2 min) Leer objetivos (slide 2).
3. (1 min) Preguntar a 1–2 estudiantes cómo les fue con la prueba del MVP.

---

#### 2️⃣ Qué es vigilancia tecnológica + fuentes (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) → 4 (ENFOQUE DE HOY)

**Objetivo de la fase:** separar “informarse” de “vigilar” y presentar las fuentes.

**GUION LITERAL:**
> “**Slide 3.** Vigilancia tecnológica no es ‘me informé’. Es un **sistema**: observar, analizar, comunicar y usar. La prueba de fuego es simple: si después de mirar el entorno **no cambia ninguna decisión** de su propuesta, no vigilaron, solo leyeron.”

> “**Slide 4.** ¿Dónde miro? Cuatro frentes. Tecnología: **Google Scholar** y **Google Patents**. Ojo con Patents: si encuentran algo parecido, la idea no muere; ahora saben contra qué compiten y tienen que decir en qué se diferencian. Mercado: reportes y datos abiertos. Normativa: leyes y políticas de entidades. Y lo social: qué cambió en el usuario. Todo gratis, todo en el navegador.”

**Qué hacer:**
1. (5 min) Explicar el ciclo Observar → Analizar → Comunicar → Usar y la prueba “¿cambió una decisión?”.
2. (7 min) Recorrer los 4 tipos de señal con sus fuentes; abrir Scholar y Patents para mostrarlos.

---

#### 3️⃣ Modelación: buscar y fichar una señal en vivo (~13 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**Objetivo de la fase:** demostrar la búsqueda y el llenado de una ficha de señal.

En vivo, con el caso del laboratorio: busque en **Google Scholar** un paper y/o en **Google Patents** un producto/solución relacionada con sistemas de reserva/turnos. Complete una **ficha de señal** en Google Docs compartiendo pantalla. Insista en **fuente + fecha + implicación**.

**GUION LITERAL:**
> “Busco ‘sistema de reserva de laboratorios’ en Scholar… miren, hay estudios sobre gestión de turnos. Copio el título, el autor y el año —sin eso no es evidencia—. Ahora paso a Patents… aquí hay una solución de reserva por QR. ¿Esto mata mi idea? No: me dice que mi diferencia debe estar en otro lado, por ejemplo en la asignación automática. Eso lo escribo en la implicación: ‘pivotar hacia asignación automática’. Fíjense: la señal **cambió** algo. Eso es vigilar.”

**Qué hacer:**
1. (7 min) Buscar en Scholar y/o Patents en pantalla, pensando en voz alta.
2. (6 min) Llenar una ficha de señal completa, subrayando fuente, fecha e implicación.

---

#### 4️⃣ Taller: tablero de vigilancia de su tema (~22 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL (consigna):**
> “Pasamos a la **slide 5 — TALLER**. Tienen **22 minutos**. Abran Google Scholar y Google Patents en otra pestaña y armen su **Tablero de vigilancia** en Google Docs con **mínimo 3 fichas de señal**: título, fuente con fecha y enlace, hallazgo en 2 líneas, implicación y nivel de confianza. **Al menos una** señal debe obligarlos a **ajustar algo**: alcance, usuario, tecnología o riesgo. Al final, dos personas comparten solo la **implicación** de una señal. Éxito: 3 señales con fuente y fecha + 1 decisión explícita.”

**Tabla de acompañamiento:**

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Pega enlaces sin fecha ni autor | “Sin fecha y autor no es evidencia. ¿Quién lo dice y cuándo?” |
| Dice “no encuentro nada” | “Cambia las palabras: busca el problema, no tu solución. Prueba en inglés en Scholar.” |
| Encuentra algo igual y se bloquea | “Perfecto, ya sabes contra qué compites. Escribe en qué te diferencias.” |
| Llena fichas que no cambian nada | “Vigilancia decorativa. Que al menos una señal te haga ajustar alcance o riesgo.” |
| Copia el abstract entero | “Resúmelo en 2 líneas. Lo que importa es la implicación para TU propuesta.” |

---

#### 5️⃣ Cierre + trabajo autónomo (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Tres ideas de hoy: (1) vigilar es un **sistema**, no una lectura suelta; (2) una fuente **sin fecha ni autor** no es evidencia; (3) si la señal **no cambia una decisión**, no sirvió.”

> “**Slide 6 — PARA CONTINUAR.** Autónomo: (a) pulan su tablero y súbanlo como `S07_Vigilancia_Apellido`; (b) preparen para la próxima sesión un listado de **mínimo 3 entidades de apoyo** —nombre correcto— a las que podrían acercarse. Eso es justo lo que trabajaremos en el cierre del curso.”

> “**Slide 7 — Cierre.** La próxima es la **última sesión**: innovación local–internacional, entidades de apoyo y pitch. Mismo Meet. Gracias.”

**Qué hacer:**
1. (4 min) Escuchar 2 implicaciones y verificar que cambien una decisión.
2. (2 min) Enunciar el trabajo autónomo (3 entidades) y el nombre del archivo.
3. (2 min) Anunciar el tema de la última sesión.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Tablero de vigilancia tecnológica — insumo de la Propuesta de Innovación.

1. Buscar en Google Scholar y Google Patents (gratis, en el navegador).
2. Registrar mínimo 3 fichas de señal (título, fuente+fecha, hallazgo, implicación, confianza).
3. **Criterio de éxito:** 3 señales con fuente y fecha + al menos 1 decisión explícita (ajuste o confirmación).
4. **Entregable:** `S07_Vigilancia_Apellido` en CDigital.
5. **Trabajo autónomo:** listado de mínimo 3 entidades de apoyo para la próxima sesión.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Abrí Google Scholar y Google Patents en el navegador del docente
- [ ] Tengo una búsqueda de ejemplo probada (para no improvisar en vivo)
- [ ] Publiqué en CDigital el espacio de entrega `S07_Vigilancia`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_08(meta):
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre de cierre", 5, 5),
        ("2️⃣ Ecosistema local–internacional", 12, 17),
        ("3️⃣ Modelación: mapa de entidades + pitch 60 s", 12, 29),
        ("4️⃣ Taller: pitch + plan de siguiente paso", 23, 52),
        ("5️⃣ Cierre del curso", 8, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión**
1. **Ubicar** la propuesta en un ecosistema de apoyo (local e internacional).
2. **Identificar** entidades concretas por su nombre real y por el tipo de apoyo que darían.
3. **Comunicar** la propuesta en un pitch de 60 segundos, cronometrado.
4. **Cerrar** el hilo del curso con un plan de continuidad y el paquete consolidado para el corte.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Esta es la **última** sesión sincrónica. Su rol hoy es doble: enseñar a conectar la propuesta con el mundo real (entidades de apoyo) y ayudar a comunicarla en 60 segundos. Léalo completo.

#### 1. Por qué existe un “ecosistema” de innovación
Una innovación **rara vez sobrevive sola**. Para pasar de prototipo a impacto necesita insumos que el estudiante no tiene por sí mismo: **capital, mentoría, redes de contactos, infraestructura, marco normativo y clientes**. El **ecosistema de innovación** es precisamente ese conjunto de **actores y reglas** que rodean a un emprendedor o a un equipo de I+D.

La metáfora útil en clase: una semilla buena no basta; necesita **tierra, agua, luz y clima**. El ecosistema es ese entorno. Por eso el trabajo del curso no termina cuando se sube el archivo a CDigital: termina —de verdad— cuando **alguien de afuera le abre una puerta** a la propuesta.

#### 2. Entidades típicas (Colombia / región) — un mapa, no un directorio
No convierta la clase en un listado interminable. Presente un mapa de **cuatro cuadrantes** y dé un ejemplo por cada uno (verifique vigencia y enlaces el día de clase, porque los programas cambian):

| Cuadrante | Ejemplos orientativos | Qué suelen ofrecer |
| :--- | :--- | :--- |
| **Universitario** | Unidad de emprendimiento CUN, semilleros, laboratorios | Mentoría, espacio, validación, contactos |
| **Público / mixto** | Cámaras de Comercio, programas de alcaldías/gobernaciones, iNNpulsa, Minciencias | Convocatorias, capital semilla, formación |
| **Privado / redes** | Hubs, aceleradoras, comunidades tech, empresas ancla | Piloto, inversión, red de clientes |
| **Internacional** | Programas de cooperación, open innovation de multilatinas, plataformas de retos | Retos abiertos, financiación, escalamiento |

**Regla docente ineludible:** **no prometa cupos ni financiaciones**. Usted no controla esas convocatorias. Lo que sí enseña es a **preguntar el encaje**: ¿esta entidad me sirve para mentoría, capital semilla, networking, infraestructura o validación? Si el estudiante no sabe **qué pediría**, la entidad no le sirve todavía.

#### 3. El pitch de 60 segundos (estructura probada)
Un pitch no es contar todo; es lograr que el otro **quiera una segunda conversación**. Estructura de 60 segundos:

| Tramo | Contenido | Tiempo |
| :--- | :--- | :--- |
| 1 | **Usuario + dolor** (a quién y qué le duele) | ~10 s |
| 2 | **Insight** (la observación que lo cambia todo) | ~10 s |
| 3 | **Propuesta + tipo de innovación** | ~15 s |
| 4 | **Evidencia breve** (validación o vigilancia) | ~15 s |
| 5 | **Pedido / siguiente paso** | ~10 s |

El error número uno es **empezar por la tecnología** (“hicimos una app con IA…”). Nadie se conecta con eso. El pitch empieza por **la persona y su dolor**; la tecnología aparece como medio, no como protagonista.

#### 4. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| Lista entidades sin decir qué les pediría | “Una entidad sin un pedido concreto no sirve. ¿Le pides mentoría, piloto o capital?” |
| Empieza el pitch por la tecnología | “Empieza por la persona y el dolor. La tecnología va en el tramo 3, como medio.” |
| Pitch de 3 minutos “porque hay mucho que contar” | “En 60 s no cuentas todo; logras que quieran una segunda charla. Corta lo demás.” |
| “¿Me pueden dar el cupo/beca?” (al docente) | “No manejo esas convocatorias. Te enseño a identificarlas y a preguntar el encaje.” |
| Cierra el curso sin saber qué falta | “Di explícitamente qué está listo y qué falta. Eso es madurez de proyecto.” |

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Encuadre de cierre (~5 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**Objetivo de la fase:** enmarcar la sesión como cierre del hilo y anunciar el doble entregable de hoy (mapa de entidades + pitch).

**GUION LITERAL:**
> “Buenas tardes. Esta es la **última sesión sincrónica** del curso — **Sesión {n:02d}**: **Innovación local–internacional y entidades de apoyo**. Hoy conectamos su propuesta con el **afuera**: quién podría ayudarles a que esto no se quede en un archivo, y cómo lo cuentan en 60 segundos.”

> “Miren la **slide 2 — OBJETIVOS**. Salen con dos cosas: un **mapa de al menos 3 entidades reales** con un pedido concreto a cada una, y un **pitch de 60 segundos** ensayado.”

**Qué hacer:**
1. (2 min) Portada + control de audio/nombres en Meet.
2. (2 min) Leer objetivos (slide 2) y recordar que traían un listado de entidades.
3. (1 min) Anunciar que habrá pitch en vivo con cronómetro (para que se preparen).

---

#### 2️⃣ Ecosistema local–internacional (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) → 4 (ENFOQUE DE HOY)

**Objetivo de la fase:** que entiendan qué es el ecosistema y aprendan a preguntar el encaje sin esperar promesas.

**GUION LITERAL:**
> “**Slide 3.** Innovar en Ingeniería no termina cuando suben el archivo a CDigital. Termina cuando alguien —un usuario, un aliado, una institución— **le abre la puerta** a su propuesta. Ese entorno de actores y reglas es el **ecosistema**. Piénsenlo como el clima de una semilla: no basta la semilla buena, necesita tierra, agua y luz.”

> “**Slide 4.** El mapa tiene cuatro cuadrantes: **universitario** —la unidad de emprendimiento de la CUN, semilleros—; **público** —Cámaras de Comercio, alcaldías, iNNpulsa, Minciencias—; **privado y redes** —hubs, aceleradoras, empresas—; e **internacional** —cooperación, retos abiertos—. Aviso importante: yo **no** les puedo prometer cupos ni plata; eso no lo manejo. Lo que sí les enseño es a **preguntar el encaje**: ¿esta entidad me da mentoría, un piloto, capital o contactos? Si no saben qué pedir, la entidad todavía no les sirve.”

**Qué hacer:**
1. (5 min) Explicar qué es el ecosistema con la metáfora de la semilla y el clima.
2. (5 min) Recorrer los 4 cuadrantes con 1 ejemplo por cada uno.
3. (2 min) Insistir en “preguntar el encaje” y en no prometer cupos ni financiación.

---

#### 3️⃣ Modelación: mapa de entidades + pitch 60 s (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**Objetivo de la fase:** modelar cómo se llena el mapa de entidades y cómo suena un pitch de 60 segundos.

Abra una tabla en **Google Docs** (compartiendo pantalla) y llénela con el caso del laboratorio; luego modele el pitch **cronometrado** (use el reloj a la vista).

| Entidad | Tipo de apoyo | Qué le pediría en un correo de 5 líneas |
| :--- | :--- | :--- |
| Unidad de emprendimiento CUN | Mentoría / pitch | Revisión de Canvas y contactos de usuarios |
| Empresa o área de TI | Piloto | 10 usuarios reales por 2 semanas |
| Programa público / cámara | Convocatoria | Info de fechas y requisitos de postulación |

**GUION LITERAL:**
> “Fíjense en la tercera columna: cada entidad tiene un **pedido concreto**. No escribo ‘pedir ayuda’; escribo ‘revisión de Canvas y 5 contactos de usuarios’. Ahora el pitch, con cronómetro… ‘Los estudiantes de Ingeniería pierden hasta una hora buscando laboratorio libre (usuario + dolor). Notamos que el 70% de los choques se dan en dos franjas (insight). Proponemos una reserva con asignación automática (propuesta, tipo proceso). En una prueba, 4 de 5 reservaron en menos de un minuto (evidencia). Buscamos un piloto de dos semanas con un curso (pedido).’ Sesenta segundos, y empecé por la persona, no por la app.”

**Qué hacer:**
1. (6 min) Llenar el mapa de entidades en Docs, subrayando el pedido concreto de cada una.
2. (6 min) Modelar el pitch de 60 s cronometrado, siguiendo los 5 tramos.

---

#### 4️⃣ Taller: pitch + plan de siguiente paso (~23 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL (consigna):**
> “Pasamos a la **slide 5 — TALLER**. Tienen **23 minutos**. Cuatro pasos: (1) completen su **Mapa de entidades** en Google Docs con **mínimo 3 entidades reales** —nombre correcto— y un pedido concreto a cada una; (2) escriban el **guion del pitch de 60 s** siguiendo los cinco tramos (pueden bocetarlo en Excalidraw); (3) **ensayen en parejas** con cronómetro; (4) al final, **4 voluntarios** pichan en vivo y les tomo el tiempo. Si necesitan una diapositiva de apoyo, Canva free —opcional—. Criterio de éxito: si en 60 segundos entendemos **dolor + valor + pedido**, sirve.”

**Tabla de acompañamiento:**

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe “pedir apoyo” sin concretar | “¿Apoyo de qué? Mentoría, piloto, capital, contactos. Elige uno y sé específico.” |
| Empieza el pitch por la tecnología | “Arranca por la persona y su dolor. La app va en el tramo 3.” |
| Se pasa de 60 segundos | “Corta la mitad. En un pitch no cuentas todo; buscas una segunda reunión.” |
| Pone entidades genéricas o inventadas | “Necesito nombre real y correcto. ¿Existe esa entidad y hace lo que dices?” |
| No sabe qué pedir a la entidad | “Vuelve a tu MVP: ¿qué te falta para probarlo? Eso es lo que pides.” |

---

#### 5️⃣ Cierre del curso (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Cierre del hilo. Partimos de un **problema real**, pasamos por creatividad e inteligencia emocional, Design Thinking, el Manual de Oslo, los tipos de innovación, la validación con Canvas y MVP, la vigilancia tecnológica y hoy el ecosistema. Su Propuesta de Innovación ya no es una ocurrencia: es un **argumento con evidencia**.”

> “**Slide 6 — PARA CONTINUAR.** Autónomo de cierre: suban a CDigital el **paquete consolidado** que pida el corte —ficha del problema, ficha Oslo, matriz de tipos, Canvas/MVP, tablero de vigilancia, mapa de entidades y guion del pitch— como `S08_EcosistemaPitch_Apellido`. Revisen las **rúbricas y los espacios de entrega (EV) del corte final** en CDigital.”

> “**Slide 7 — Cierre.** Gracias por el trabajo de todo el ciclo. Cualquier duda administrativa, por el canal del curso. Fue un gusto acompañarlos.”

**Qué hacer:**
1. (3 min) Cerrar los pitches en vivo (si quedaron voluntarios) y dar 1 elogio + 1 mejora a cada uno.
2. (3 min) Recorrer el paquete consolidado que se sube al corte final.
3. (2 min) Despedida y canal de dudas administrativas.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Mapa de entidades + pitch de 60 s — cierre de la Propuesta de Innovación.

1. Mapa de mínimo 3 entidades reales con un pedido concreto a cada una (Google Docs).
2. Guion del pitch de 60 s en 5 tramos (boceto en Excalidraw; Canva free opcional para 1 slide).
3. Ensayo en parejas + pitch en vivo cronometrado.
4. **Criterio de éxito:** 3 entidades con pedido concreto + pitch que en 60 s comunica dolor, valor y pedido.
5. **Entregable:** `S08_EcosistemaPitch_Apellido` en CDigital + paquete consolidado del corte final.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Tengo el mapa de entidades y el pitch modelo del caso laboratorio listos
- [ ] Tengo un cronómetro visible para los pitches en vivo
- [ ] Revisé las rúbricas/EV del corte final en CDigital para orientar el paquete consolidado
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Cierra el ciclo de encuentros del Syllabus EI004.*
"""



# Builders originales (1..8). Mapa canónico 7 sesiones: 1→1, 2→3, 3→4, 4→5, 5→6, 6→7, 7→8
BUILDERS_LEGACY = {
    1: guion_01,
    2: guion_02,
    3: guion_03,
    4: guion_04,
    5: guion_05,
    6: guion_06,
    7: guion_07,
    8: guion_08,
}

CANON_TO_LEGACY = {1: 1, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}


def _fix_session_numbers(md: str, n: int) -> str:
    """Renumera un guion escrito para otra sesión (builder legacy ≠ sesión canónica).

    Solo se aplica cuando ``CANON_TO_LEGACY[n] != n``: reescribe **todas** las menciones
    «Sesión NN», así que aplicarlo a un guion escrito para su propia sesión destruiría las
    referencias legítimas a otras sesiones (p. ej. la S01 de encuadre, que remite a la S02).
    """
    md = re.sub(r"Sesión \*\*\d{2}\*\*", f"Sesión **{n:02d}**", md)
    md = re.sub(r"Sesión \d{2}\b", f"Sesión {n:02d}", md)
    md = re.sub(r"Fin del Guión — Sesión \d{2}", f"Fin del Guión — Sesión {n:02d}", md)
    md = re.sub(r"ciclo de 8 encuentros", "ciclo de encuentros del Syllabus EI004", md)
    # El nombre del entregable lleva el numero de sesion (`S03_Ideacion_Apellido`). Al heredar
    # un guion de otra sesion tambien hay que renumerarlo: si no, el docente le pide al
    # estudiante un archivo con el numero de la sesion vieja (y llegaba a pedir una `S08`
    # que ya no existe). Cada guion legacy nombra unicamente SU propio entregable.
    md = re.sub(r"\bS\d{2}_", f"S{n:02d}_", md)
    return md


def main(argv=None):
    """Escribe solo .md (guiones docentes = Markdown; sin .docx).

    **Sesión 01 = encuadre y se regenera siempre**, como cualquier otra sesión. La protección
    antigua («SKIP S01 (modelo en disco)») existía cuando la S01 era el modelo de calidad del
    workspace y dictaba tema; desde la decisión docente del 2026-08-09 la S01 ya no dicta tema
    (el modelo de calidad es la S02), así que conservarla en disco solo dejaba un guion viejo.
    ``--force-s01`` se acepta por compatibilidad con pipelines antiguos y **no cambia nada**.
    """
    argv = list(argv or sys.argv[1:])
    if "--force-s01" in argv:  # compat: la S01 ya se regenera siempre
        print("NOTA: --force-s01 es innecesario (la S01 se regenera en cada corrida)")
    argv = [a for a in argv if a != "--force-s01"]
    only_n = int(argv[0]) if argv and argv[0].isdigit() else None

    metas = sesiones_meta()
    keep = {f"{m[1]}.md" for m in metas}
    for name in os.listdir(ROOT):
        if name.startswith("Sesion ") and name.endswith(".md") and name not in keep:
            try:
                os.remove(os.path.join(ROOT, name))
                print("DEL", name)
            except OSError:
                pass

    for meta in metas:
        n, label, titulo, detalle = meta
        if only_n is not None and n != only_n:
            continue
        md_path = os.path.join(ROOT, f"{label}.md")
        legacy_n = CANON_TO_LEGACY[n]
        builder = BUILDERS_LEGACY[legacy_n]
        text_md = builder((n, label, titulo, detalle))
        if legacy_n != n:
            # Solo los guiones heredados de otra sesión necesitan renumerarse (ver docstring).
            text_md = _fix_session_numbers(text_md, n)
        _deck = deck_path(COURSES["creatividad"]["folder"], label)
        if n != 1:
            # Narración heredada de la plantilla de 7 slides: se retiran los números.
            text_md, _ = limpiar_referencias(text_md)
        else:
            # Mapa curado a mano: realinear contra el deck real («(cont.)» insertadas).
            text_md, _ = ajustar_mapa_manual(text_md, titulos_pptx(_deck))
        text_md = inject_shots(text_md, n)
        if n == 1 and "Rompehielos Padlet" not in text_md:
            text_md = text_md.replace(
                "- **Meet (serie del curso):**",
                (
                    f"> **Rompehielos Padlet:** slide PRESÉNTATE de la Presentación del Curso. "
                    f"URL: {PADLET_PRESENTACION_URL}\n\n- **Meet (serie del curso):**"
                ),
                1,
            )
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(text_md)
        print("MD", md_path)


if __name__ == "__main__":
    main()
