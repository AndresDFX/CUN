# -*- coding: utf-8 -*-
"""Regenera guiones docentes de Creatividad (EI004) — solo .md, 60 min, con pantallazos.

Alineado a config/cursos/sesiones_cun.py (7 sesiones del periodo). **Un builder por sesión
canónica**: `GUIONES[n]` se escribió para la sesión `n` y para ninguna otra (ver la nota
«CORRIMIENTO RETIRADO» al final del archivo).

Sesión 01 = **ENCUADRE** (decisión del docente, 2026-08-09): no dicta tema. Presenta el
curso, al Docente, a los estudiantes (rompehielos como **juego en Slido**: el grupo tiene
50 matriculados y un muro colaborativo ya no se lee entero) y las ACAs; el contenido
curricular arranca en la Sesión 02, y la unidad que antes vivía en S01 (`unidad_diferida`
en `sesiones_cun.py` → U1–U2) pasa a **lectura autónoma**.
Por eso la S01 **ya no se protege**: se regenera como cualquier otra sesión en cada corrida
(el modelo de calidad del curso es hoy la Sesión 02). El flag ``--force-s01`` se sigue
aceptando por compatibilidad con pipelines antiguos, pero **no cambia nada**.

Temario adelantado (2026-08-11, ver `nota_syllabus` en `sesiones_cun.py`): la **S05** es
doble (**U6+U7**: validación *y* vigilancia tecnológica), la **S06** es **U8** (ecosistema,
entidades de apoyo y pitch) y la **S07** es el **taller de consolidación y sustentación**,
sin evaluación de contenido nueva. El reorden existe porque la **ACA Final califica U7 y U8**
y cierra antes de la última sesión: lo calificable tenía que llegar antes del cierre.

Evaluación: `guion_evaluacion.py` inyecta el aviso del ítem real del aula (Quiz 1, Parcial 1,
…, ACA Final, auto y coevaluación) y, cuando ese ítem cierra en día de clase, una fase con
minutos reservados dentro de los 60. Los datos salen del libro de calificaciones
(`config/cursos/fechas_entrega_aca.py`): aquí no se escribe ningún peso ni fecha a mano.
Ese inyector **recorta las fases más largas** para hacerle sitio a la evaluación, así que los
minutos que escribe cada builder son los de una hora **sin** evaluación; el .md en disco
muestra ya el reparto real y una nota de replaneación.

Uso:
    python _regen_guiones_creatividad.py            # todas las sesiones (incluida S01)
    python _regen_guiones_creatividad.py 1          # solo la Sesión 01
"""
from __future__ import annotations
import os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "config", "slides"))
CURSOS = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "config", "cursos"))
sys.path.insert(0, SLIDES)
sys.path.insert(0, CURSOS)

from sesiones_cun import COURSES, meet_url  # noqa: E402
from cun_slides_engine import slido_url  # noqa: E402
from guion_evaluacion import (  # noqa: E402
    KIND_CUESTIONARIO,
    inyectar_evaluacion,
    items_corte_txt,
    peso_item,
    peso_tipo,
)
from guion_slides import (  # noqa: E402
    NOTA_MOMENTOS,
    ajustar_mapa_manual,
    deck_path,
    limpiar_referencias,
    tabla_slides_md,
    titulos_pptx,
)

MEET = meet_url("creatividad", COURSES["creatividad"]["titulo"])

# --- Rompehielos de la Sesión 01: juego en Slido, no muro ---------------------------
# EI004 54408 tiene **50 matriculados** (roster de CDigital). Un Padlet de 50 notas no se
# lee entero en clase y el que escribe sin ser leído se desconecta. Por eso el rompehielos
# deja de ser «preséntate» y pasa a ser un **juego con premio**: «dos verdades y una
# mentira» sobre el Docente, en **Slido**. Acertar es 1 entre 3 —azar puro—, así que quien
# nunca abre la cámara arranca igual que quien siempre habla, y de paso queda hecha la
# presentación del Docente sin diapositiva de biografía.
# Slido y no Mentimeter: el plan gratis (Basic) da 100 participantes por evento, 3 encuestas,
# 1 quiz con tabla de posiciones y Q&A ilimitado; Mentimeter corta en 50 participantes AL MES.
# La decisión no se escribe aquí: la deriva `cun_slides_engine.modo_rompehielos()` de la
# matrícula, y el enlace sale de la misma fuente que el del Meet (mientras el Docente no
# cree el evento, `slido_url` devuelve el marcador de posición). El estudiante no necesita
# esa URL: entra a slido.com con el **código** que el Docente pega en el chat del Meet.
SLIDO = slido_url("creatividad")


def runbook_slido(course_key: str) -> str:
    """Ruta del runbook del rompehielos — **material del Docente**, no va en `Clases/`.

    Lo genera `config/slides/build_rompehielos_slido.py` en `2026/<grupo>/` (o en
    `2026/_combinado_todos/` cuando el curso corre sus grupos en una sola serie). Ahí
    viven las tres rondas y las casillas donde el Docente marca la mentira: el guion las
    **remite**, nunca las copia — un guion con las mentiras escritas deja de servir el día
    que un estudiante lo vea.
    """
    folder = COURSES[course_key]["folder"]
    base = os.path.join(folder, "2026")
    grupos = sorted(
        d for d in (os.listdir(base) if os.path.isdir(base) else [])
        if os.path.isdir(os.path.join(base, d)) and not d.startswith("_")
    )
    carpeta = "_combinado_todos" if len(grupos) > 1 else (grupos[0] if grupos else "<grupo>")
    return f"{os.path.basename(folder)}/2026/{carpeta}/Rompehielos Slido - Sesion 01.md"


RUNBOOK_SLIDO = runbook_slido("creatividad")


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


# ---------------------------------------------------------------------------
# SLIDES REALES DEL DECK  (para que cada fase diga qué se proyecta y en qué orden)
# ---------------------------------------------------------------------------
# El guion no puede citar números de slide a mano: el motor parte los bloques largos en
# «(cont.)», así que un deck de 19 bloques JSON sale con 27 slides y cualquier número
# escrito a mano queda corrido. Aquí el número se **calcula** desde el .pptx en disco a
# partir del título del bloque; si el deck no está, la fase igual nombra los títulos.
_DECK_CACHE: dict[str, list[str] | None] = {}


def _norm_titulo(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or "")).replace("(cont.)", " ")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.findall(r"[a-z0-9]+", s.lower()))


def _deck_titulos(label: str) -> list[str] | None:
    if label not in _DECK_CACHE:
        _DECK_CACHE[label] = titulos_pptx(deck_path(COURSES["creatividad"]["folder"], label))
    return _DECK_CACHE[label]


def slides_fase(label: str, *titulos: str) -> str:
    """Línea «Slides del deck» de una fase: rango real + los títulos, en orden de proyección.

    No usa el prefijo `**Slides:**` a propósito: `limpiar_referencias()` lo reescribiría a
    «Momento del deck» y borraría justo los números que aquí sí son correctos.
    """
    reales = _deck_titulos(label) or []
    idx = [
        i + 1
        for i, real in enumerate(reales)
        if any(_norm_titulo(real) == _norm_titulo(t) for t in titulos)
    ]
    rango = ""
    if idx:
        a, b = min(idx), max(idx)
        rango = f"**{a}**" if a == b else f"**{a}–{b}**"
    cuerpo = " → ".join(f"«{t}»" for t in titulos)
    return f"**Slides del deck:** {rango + ' · ' if rango else ''}{cuerpo}"


def portada_deck(n: int, titulo: str) -> str:
    return f"SESIÓN {n:02d} — {titulo}"


def cierre_deck(n: int) -> str:
    return f"Cierre — Sesión {n:02d}"


def shot(rel_path: str, caption: str, tip: str) -> str:
    return (
        f"\n![{caption}](Capturas/{rel_path})\n\n"
        f"> **En pantalla:** {tip}\n"
    )


# Pantallazos por sesión canónica (n) → {fase antes de la cual se insertan: [pantallazos]}.
# La clave es el keycap de la fase del builder (numeración **antes** de que el inyector de
# evaluación meta su propia fase), porque `inject_shots()` corre antes que él.
SHOTS = {
    # S01 = encuadre. El pantallazo del rompehielos queda pendiente: el que había es del
    # Padlet, que este curso ya no usa. Cuando el evento de Slido exista se captura
    # `Sesion 01/s01_slido_leaderboard.png` (la tabla de posiciones, que es lo que se
    # proyecta en la fase 3) y se enchufa aquí. El de Google Docs / plantilla APA va
    # incrustado dentro de la fase 5️⃣ del guion de encuadre.
    1: {},
    2: {
        "3️⃣": [
            ("Sesion 01/s01_miro_design_thinking.png", "Miro — Design Thinking (plantilla free)",
             "Mostrar etapas DT; plan B: Excalidraw si Miro pide login."),
            ("s01_excalidraw_pizarra.png", "Excalidraw — HMW + banco de ideas",
             "Escribir 1 How Might We y 10 ideas en voz alta."),
        ],
        "4️⃣": [
            ("Herramientas/dt_ideo_designkit.png", "IDEO Design Kit (referencia)",
             "Solo si carga bien; si no, continuar en Excalidraw/Miro free."),
        ],
    },
    3: {
        "3️⃣": [
            ("s01_google_docs_inicio.png", "Docs — tabla Oslo",
             "Clasificar 3 casos en producto/proceso/organización/marketing/social."),
        ],
        "4️⃣": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — ficha Oslo de su propuesta",
             "Tipo dominante + secundario + 1 justificación."),
        ],
    },
    4: {
        "3️⃣": [
            ("s01_google_docs_inicio.png", "Docs — matriz tipos de innovación",
             "Filas = tipos Oslo; columnas = ejemplo / su propuesta."),
        ],
        "4️⃣": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — cuadro comparativo",
             "Mejora socio-económica vs. tipo elegido."),
        ],
    },
    # S05 = sesión doble (U6+U7). La fase 2️⃣ lleva el Canvanizer incrustado en su propio
    # texto; aquí van la segunda mitad (vigilancia) y el taller.
    5: {
        "3️⃣": [
            ("s01_google_docs_inicio.png", "Docs — tablero de vigilancia (5 columnas)",
             "Señal · fuente y fecha · hallazgo · implicación · confianza. Scholar y Patents "
             "abiertos en pestañas aparte."),
        ],
        "4️⃣": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — FODA + MVP en 5 líneas",
             "FODA de 6 bullets con interna/externa separadas y el MVP escrito al lado."),
            ("s01_google_docs_inicio.png", "Docs — un solo documento con las dos mitades",
             "Títulos «A. Validación» y «B. Vigilancia»; se exporta a PDF y se sube a CDigital."),
        ],
    },
    6: {
        "3️⃣": [
            ("s01_google_docs_inicio.png", "Docs — mapa de entidades de apoyo",
             "Tres columnas: entidad (nombre verificado) · tipo de encaje · pedido concreto y acotado."),
        ],
        "5️⃣": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — los cinco tramos del pitch",
             "Un recuadro por tramo, una frase en cada uno. Cronómetro a la vista al ensayar."),
        ],
    },
    7: {
        "3️⃣": [
            ("s01_google_docs_inicio.png", "Docs — la propuesta consolidada, sección por sección",
             "Recorrer el documento del caso del laboratorio y mostrar dónde se rompen las costuras."),
        ],
        "5️⃣": [
            ("s01_excalidraw_pizarra.png", "Excalidraw — rúbrica de la ronda a la vista",
             "Los cuatro criterios escritos en pantalla mientras un compañero sustenta."),
        ],
    },
}


def inject_shots(md: str, n: int) -> str:
    for keycap, tiros in (SHOTS.get(n) or {}).items():
        bloque = "".join(shot(*t) for t in tiros)
        ancla = f"#### {keycap}"
        if bloque and ancla in md:
            md = md.replace(ancla, bloque + "\n" + ancla, 1)
        elif bloque:
            md = md + f"\n\n### Pantallazos (fase {keycap})\n" + bloque
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

# Sesión 07 = cierre: no dicta contenido nuevo ni evalúa contenido (la ACA Final y el Quiz 3
# ya cerraron). Sí abren la autoevaluación y la coevaluación, que el inyector agenda solo.
USO_SESION_CIERRE = (
    "> **Uso:** guion de **cierre**. Esta sesión **no dicta contenido nuevo y no evalúa contenido**:"
    " la ACA Final y el Quiz 3 ya cerraron.\n"
    "> Lo que pasa hoy es sustentación con el pitch, retroalimentación entre pares, revisión de"
    " coherencia del documento y apertura de auto y coevaluación.\n"
    "> Léalo en voz alta casi literal. Estudie primero el Fundamento Teórico. **Duración: 60"
    " minutos**.\n"
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

> **Criterio de numeración (declarado, para que no haya desfase):** los números de este guion
> son los del **PPTX en disco**, donde la **portada es la slide 1**. El deck tiene **23 slides**
> y en él se cuentan también las **«(cont.)»** que el motor inserta al partir un bloque largo
> (slides **18** y **20**). Si el conteo del deck cambia, se regenera el guion: no se corrige a mano.

| Slide | Título en el PPTX | Cuándo usarla |
| :---: | :--- | :--- |
| **1** | Portada — SESIÓN 01, PRESENTACIÓN DEL CURSO | Apertura |
| **2** | AGENDA DE HOY | Encuadre de la hora |
| **3** | Docente | Presentación del Docente |
| **4** | ROMPEHIELOS — DOS VERDADES Y UNA MENTIRA | Rompehielos (juego en Slido) |
| **5** | CÓMO SE EVALÚA — LOS ÍTEMS DEL AULA | Pesos y tipo de cada ítem |
| **6** | Cómo trabajamos: una hora juntos, el resto por su cuenta | Metodología / aula invertida |
| **7** | Mapa del curso: las 7 sesiones de un vistazo | Recorrido del curso |
| **8** | Qué se llevan al final: la Propuesta de Innovación | Producto del curso |
| **9** | Qué evalúa cada instrumento: lo que está en el libro de calificaciones | Alcance de Quiz 1 vs. Parcial 1 y de cada corte |
| **10** | Qué separa un entregable fuerte de uno flojo | Criterio de calidad |
| **11** | Cómo se entrega: paso a paso en CDigital | Procedimiento de entrega |
| **12** | Integridad académica: la línea que no se cruza | Plagio y APA 7 |
| **13** | IA generativa: se usa, se declara y se verifica | Regla de uso de IA |
| **14** | Herramientas del curso: gratis y desde el navegador | Alistamiento técnico |
| **15** | Cómo pedir ayuda (y recibir respuesta pronto) | Canales y tiempos |
| **16** | Acuerdos de convivencia del encuentro | Cámara, micrófono, foro |
| **17** | Para la Sesión 02: lectura autónoma y qué traer | Encargo autónomo |
| **18** | Para la Sesión 02: lectura autónoma y qué traer (cont.) | Sigue el encargo (misma slide partida) |
| **19** | Preguntas del primer día | Dudas típicas |
| **20** | Preguntas del primer día (cont.) | Sigue el bloque de dudas |
| **21** | ACUERDOS DE TRABAJO | Cierre de reglas |
| **22** | PARA LA PRÓXIMA SESIÓN | Tarea concreta |
| **23** | Cierre — Sesión 01 | Despedida |

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
    # El juego ocupa 8 minutos exactos (antes el rompehielos tenía 9). El minuto que se
    # libera va a la fase de evaluación, que es la que siempre se queda corta: hay que
    # recorrer el libro de calificaciones, el Quiz 1 y la plantilla APA en pantalla.
    fases = [
        ("1️⃣ Apertura y bienvenida", 5, 5),
        ("2️⃣ Quién es el Docente", 4, 9),
        ("3️⃣ Rompehielos: «Dos verdades y una mentira» en Slido", 8, 17),
        ("4️⃣ Cómo trabajamos, recorrido del curso y su producto final", 11, 28),
        ("5️⃣ Cómo se evalúa el curso (quices, parciales y ACA Final) y cómo se entrega", 13, 41),
        ("6️⃣ Integridad académica y uso de IA", 7, 48),
        ("7️⃣ Herramientas, canales de ayuda y acuerdos", 7, 55),
        ("8️⃣ Encargo autónomo y cierre", 5, 60),
    ]
    return header(*meta, uso=USO_SESION_ENCUADRE) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión (encuadre — no hay tema del Syllabus)**
1. Que el estudiante sepa **qué produce este curso**: una **Propuesta de Innovación** propia, no un ensayo.
2. Que sepa **cómo se trabaja**: una hora sincrónica de aplicación + trabajo autónomo con el material leído antes.
3. Que sepa **qué se evalúa y cómo se entrega**: los ítems reales del aula (quices y parciales por corte, **ACA Final**, auto y coevaluación), el formato APA CUN y el espacio de CDigital.
4. Que conozca las reglas de **integridad académica** y de **uso declarado de IA generativa**.
5. Que salga con **un solo encargo claro**: la lectura autónoma U1–U2 y un problema real escrito en tres líneas.

> **Lo que hoy NO se hace:** no se define creatividad, no se explica inteligencia emocional, no se dictan tipos de innovación. Todo eso **empieza en la Sesión 02**. Si usted se mete en el tema hoy, llega tarde al bloque de evaluación y el grupo se va sin saber que el **Quiz 1 cierra en la próxima sesión**.

---

🧰 **Antes de la clase — qué debe tener listo el Docente** *(esta sesión no tiene fundamento teórico: tiene alistamiento)*

| Qué abrir / tener listo | Dónde está | Para qué momento |
| :--- | :--- | :--- |
| **Aula del curso en CDigital**, con el anuncio de bienvenida publicado y los espacios de entrega visibles | Campus institucional (login CUN) | Fases 5, 7 y 8 |
| **Evento de Slido** creado y probado desde el celular: **quiz de 3 preguntas** (una por ronda), **una encuesta A/B/C** vacía para la ronda final y el **Q&A abierto**; el **código del evento** copiado para el chat | {SLIDO} | Fase 3 y todo el encuentro |
| **Las tres rondas ajustadas y la mentira de cada una marcada** *(material del Docente; no va en `Clases/`)* | `{RUNBOOK_SLIDO}` | **Antes** de entrar a la sala |
| **Libro de calificaciones** del aula, abierto en otra pestaña | Campus institucional (login CUN) | Fase 5 — de ahí salen los nombres, los tipos y los pesos que va a anunciar |
| **Enunciado de la ACA Final** (única entrega documental) | `Clases/Recursos/ACAs/` | Fase 5 |
| **Plantilla APA CUN**, ya abierta en **Google Docs** (no en Word de escritorio) | `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` | Fase 5 |
| **PPTX de esta sesión** (**23 slides**, portada incluida) | `Clases/{label}/Presentacion.pptx` | Toda la clase |
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
| Ronda final abierta a más gente, no solo al podio | +8 | Bajar de los tres primeros a los seis primeros de la tabla de posiciones: cada uno dice sus dos verdades y una mentira y el curso vota |
| Recorrido lento del **mapa del curso** (slide 7) | +10 | Preguntar sesión por sesión: “¿qué creen que sale de esta?” |
| **Plantilla APA CUN** en vivo | +12 | Compartir pantalla, crear la copia en Google Docs y mostrar dónde escribe cada quien |
| **Enunciado de la ACA Final** leído entero con el checklist | +10 | Abrirlo desde `Clases/Recursos/ACAs/` y marcar criterio por criterio |
| Mini-ejercicio “mi problema en tres líneas” escrito en clase | +15 | Cada quien escribe; dos voluntarios leen; el Docente solo pregunta “¿a quién le pasa?” |

> Lo que no alcance a hacer **no se elimina: se convierte en trabajo autónomo**. La actividad queda en la carpeta de esa sesión, en el **Drive de clases** —la carpeta `Clases/` que ellos ya tienen compartida—, y se anuncia en CDigital, que es donde miran las fechas y las notas.

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

#### 3️⃣ Rompehielos: «Dos verdades y una mentira» en Slido (~8 min) — Protagonista: Estudiantes
**Slides:** 4 (ROMPEHIELOS — DOS VERDADES Y UNA MENTIRA · juego en Slido)

**Objetivo de la fase:** romper el silencio del primer día jugando, dejar hecha la presentación del Docente sin diapositiva de biografía y que **tres estudiantes** se presenten habiéndose ganado el turno.

> ⚠️ **Antes de entrar a la sala.** Las **tres rondas** y **cuál es la mentira de cada una** están en
> `{RUNBOOK_SLIDO}` — material del Docente, no va en `Clases/`. **Márquelas ahí antes de la clase** y
> ajústelas a su vida: si las frases no son suyas, el juego no funciona. Aquí no se repiten a propósito:
> este guion se comparte, y una mentira escrita en él deja de ser mentira.

> **Por qué un juego y no un muro:** en este curso hay **50 matriculados**. Cincuenta notas en un tablero no alcanzan a leerse en clase, y el estudiante que escribe y nunca es leído se desconecta el primer día. Acertar en «dos verdades y una mentira» es **1 entre 3**: azar puro, así que el que nunca abre la cámara arranca igual que el que siempre habla. Va **aquí, antes de la primera tabla de porcentajes**: si lo primero que ven es una tabla de pesos, ya perdió la sala. Evento de Slido: {SLIDO}

**(1) GUION LITERAL — explicar el juego y anunciar el premio (~1 min):**
> “**Slide 4 — ROMPEHIELOS.** Antes de hablar de notas, de cortes y de porcentajes, ocho minutos de juego. Entren a **slido.com** —desde el celular o en otra pestaña— y escriban el **código** que acabo de pegar en el chat. No hay que instalar nada ni crear cuenta: se pone el código y ya están adentro. Pongan su **nombre real**, porque con ese nombre se arma la tabla de posiciones.”

> “Se llama **dos verdades y una mentira**, y va sobre mí. **Tres rondas.** En cada una les muestro **tres frases mías** y **una es falsa**: ustedes votan cuál creen que es la mentira. Acertar es una entre tres, así que aquí no gana el que sepa de innovación: gana el que me lea mejor. Todos empezamos empatados.”

> “Y se juega por algo: quien más veces me pille se gana una **revisión uno a uno conmigo**, media hora solo para su propuesta, **antes de la primera entrega**. No son décimas —eso no lo regalo—: es tiempo mío sobre su documento, que en este curso vale más.”

**(2) GUION LITERAL — las tres rondas (~4 min, unos 80 segundos cada una):**
> “**Ronda uno.** Ahí están las tres frases. Una de estas tres **no** es cierta: ¿cuál? Veinte segundos… y voten, que el que no vota no puntúa.”

> [Cierre la pregunta, proyecte el reparto de votos y **revele la mentira**.] “La mentira era la número [X]. Y lo bueno es lo otro: la que a más gente le costó creer **sí es verdad**.” [Cuente en **treinta segundos** la historia de la verdad más rara de la ronda. Ese es el momento en que usted se presenta de verdad.]

> “**Ronda dos.** Mismas reglas, otras tres frases…” [Vote → revele → historia de treinta segundos.]

> “**Ronda tres**, la última mía…” [Vote → revele → historia de treinta segundos.]

> **Regla de oro de esta fase:** revele la mentira **después de cada ronda**, no al final, y cuente la historia — la gracia del juego es la revelación, y la historia es su presentación. Pero **cronometre**: treinta segundos por historia, no tres minutos. Tres rondas caben en cuatro minutos solo si usted se contiene.

**(3) GUION LITERAL — tabla de posiciones (~1 min):**
> “Veamos quién me leyó mejor.” [Proyecte la **tabla de posiciones** de Slido.] “Podio: [nombre 1], [nombre 2] y [nombre 3]. Aplauso en el chat para los tres… y ojo, que el premio todavía no está entregado.”

**(4) GUION LITERAL — la ronda final, la del podio (~2 min):**
> “Ahora se invierte el juego: **los tres del podio se presentan jugando**. Cada uno abre el micrófono treinta segundos y nos dice **sus** dos verdades y una mentira: de dónde viene, en qué trabaja, lo que quiera. El resto vota en la encuesta que tengo abierta —**A, B o C**— y **gana el que engañe a más gente**.”

> [Lance la **encuesta A/B/C** una vez por cada persona del podio y anuncie en voz alta cuántos cayeron con cada una.]

> “Ganó [nombre]: nos engañó a [n] de nosotros. Esa revisión uno a uno es suya — le escribo hoy para agendarla. Y fíjense en lo que acaba de pasar: ya conocen a tres compañeros, y hablaron porque se lo ganaron, no porque yo los nombrara. Eso es exactamente lo que este curso pide todo el semestre: proponer algo y bancárselo.”

**Cómo conducirlo (esto es lo que hace que funcione con 50):**
1. **Pegue el código en el chat y dígalo en voz alta**, y vuelva a pegarlo al abrir la ronda uno: el chat del primer día entierra el primer mensaje. El QR de la slide es la ayuda, no el camino principal: la mitad está conectada desde el computador.
2. **No espere a que entren los cincuenta.** Arranque cuando el contador de participantes se mueva; quien llegue tarde entra en la ronda dos y no pasa nada — esto no tiene nota.
3. **Ocho minutos son ocho minutos.** Si una ronda se estira, lo que se recorta es su historia, nunca la revelación.
4. **Empate en el podio:** deje a los cuatro. Treinta segundos de más se recuperan; discutir un desempate en vivo, no.
5. **Si alguien del podio no quiere hablar:** no insista ni un segundo. “Pasamos al siguiente” y sigue el cuarto de la tabla. Obligar a hablar el primer día es justo lo que este juego vino a evitar.
6. **Deje el Q&A de Slido abierto** todo el encuentro y dígalo: “lo que les quede sonando, escríbanlo ahí y al final respondo las más votadas”. Con cincuenta personas, el Q&A ordena lo que el chat desordena.

**Cierre de la fase — y el diagnóstico que antes hacía el formulario:**
> “Última cosa, y esta sí me sirve a mí: en el **Q&A de Slido** escriban una línea con **algo que hayan visto funcionar mal** —en su trabajo, en su barrio o aquí mismo en la universidad—. Una línea basta, y no busquen que suene inteligente: busquen que sea verdad. Queda abierto toda la sesión y yo lo leo hoy mismo; de ahí salen los ejemplos con los que vamos a trabajar.”

**Después de clase, el Q&A no se bota:** expórtelo junto con la lista de participantes. De ahí salen los ejemplos de las próximas sesiones, los dúos con problemas parecidos y la lista de quién no se conectó. Y deje el evento **abierto 48 horas**, con el enlace publicado en el aula: quien no estuvo juega igual —fuera de la tabla de posiciones, que sería injusto con quien sí llegó— y llega a la Sesión 02 sabiendo quién le da clase.

---

#### 4️⃣ Cómo trabajamos, recorrido del curso y su producto final (~11 min) — Protagonista: Docente
**Slides:** 6 (CÓMO TRABAJAMOS) → 7 (MAPA DEL CURSO) → 8 (QUÉ SE LLEVAN AL FINAL)

**GUION LITERAL:**
> “**Slide 6 — Cómo trabajamos.** Esta materia son dos créditos: alrededor de 32 horas conmigo y **64 horas suyas**. Léanlo otra vez: el doble del tiempo lo pone usted, fuera de esta sala. No lo digo para asustar, lo digo para que nadie crea que esta hora semanal es el curso completo.”

> “Como la hora es corta, trabajamos en **aula invertida**: el material de cada unidad queda en la carpeta de esa sesión, en el **Drive de clases** que les comparto, y ustedes lo leen **antes**. La hora de encuentro no la voy a gastar leyéndoles diapositivas: la vamos a gastar **aplicando** eso a su propia propuesta. Traigan siempre su documento de trabajo abierto; aquí se trabaja sobre lo que ya está escrito, no sobre lo que uno recuerda.”

> “**Slide 7 — Mapa del curso.** Son siete encuentros. Hoy encuadre; la próxima, Design Thinking; luego el Manual de Oslo, los tipos de innovación, la validación con Canvas y MVP, la vigilancia tecnológica y, al final, el ecosistema y el pitch. Fíjense en la tercera columna: **cada sesión deja un pedazo del mismo documento**. Ninguna es un taller suelto.”

> “Van a notar que el mapa tiene ocho unidades y solo siete encuentros. Las dos primeras —la Propuesta de Innovación y el bloque de creatividad e inteligencia emocional— quedan como **lectura autónoma** y las retomamos al abrir la Sesión 02. Al final de la clase les digo exactamente qué leer.”

> “**Slide 8 — Qué se llevan al final.** El producto es una **Propuesta de Innovación** de ocho a doce páginas más un pitch de una página, que responde en orden: problema, usuario, propuesta de valor, tipo de innovación, validación, vigilancia y siguiente paso. Y una advertencia sincera: si al terminar solo tienen un archivo para la nota, desperdiciaron el semestre. Esto les sirve para una entrevista de trabajo, para proponer una mejora en la empresa donde están, o como semilla de su opción de grado.”

**Qué hacer:**
1. (3 min) Insistir en la proporción 32/64 horas: es la expectativa que evita el reclamo del corte 3.
2. (4 min) Recorrer el mapa preguntando al grupo qué creen que sale de dos o tres sesiones.
3. (4 min) Anclar el producto final y su utilidad fuera del aula.

---

#### 5️⃣ Cómo se evalúa el curso (quices, parciales y ACA Final) y cómo se entrega (~12 min) — Protagonista: Docente
**Slides:** 5 (CÓMO SE EVALÚA — LOS ÍTEMS DEL AULA) → 9 (QUÉ EVALÚA CADA INSTRUMENTO) → 10 (Qué separa un entregable fuerte de uno flojo) → 11 (CÓMO SE ENTREGA)

**GUION LITERAL:**
> “**Slide 5.** Evaluación por cortes: **30, 30 y 40 por ciento**. Pero escuchen los **nombres reales** de lo que van a ver en el aula, porque de ahí sale la nota: **{items_corte_txt('creatividad', 1)}** en el primer corte, **{items_corte_txt('creatividad', 2)}** en el segundo y **{items_corte_txt('creatividad', 3)}** en el tercero. Los quices y los parciales son **cuestionarios de CDigital**; la **ACA Final** es la única entrega con documento; y la **coevaluación es un foro**, o sea que hay que escribir en él.”

> “Ahora el dato que les va a cambiar la forma de organizarse: los **cuestionarios suman {peso_tipo('creatividad', KIND_CUESTIONARIO)} de la nota del curso**, y el **Parcial 1** solo vale {peso_item('creatividad', 'parcial1')}. Esto no es una materia que se salve con un buen documento al final: se salva viniendo a clase y respondiendo.”

> “Y lo más importante de hoy, anótenlo: los quices y los parciales **caen en día de clase** y **cierran ese mismo día**. El primero es el **Quiz 1**, y cierra en la **próxima sesión**. El que falte ese día no lo recupera. Las **fechas exactas no las dicto de memoria**: están en cada ítem de CDigital y en la Presentación del Curso; ábranlas hoy y pónganse alarma.”

> “**Slide 9 — qué evalúa cada instrumento.** Fíjense en la primera columna: el **Corte 1 aparece en dos filas** y no es un error de la diapositiva. **Quiz 1 y Parcial 1 no evalúan lo mismo**, y confundirlos es la forma más tonta de estudiar de más y perder puntos.”

> “El **Quiz 1** —6%, cierra en la próxima sesión— se responde **solo con el material de hoy**: la lectura autónoma **U1 y U2** del Syllabus. Es decir: la **Propuesta de Innovación** y el orden de sus partes, el **problema–oportunidad real y observable** con un **usuario concreto**, y **la inteligencia emocional y su incidencia en la innovación y la creatividad**. De la lectura obligatoria les pregunto **lo que el estudio reporta**: qué miró y qué encontró. Dicho sin rodeos: **el archivo de la lectura entra; el método Design Thinking, no** —el método lo dictamos la próxima semana, así que no puedo preguntarlo antes de explicarlo.”

> “El **Parcial 1** —24%— es el que **sí** les pregunta el método: las **fases del Design Thinking** y las **técnicas de ideación** de la Sesión 02 —árbol de problemas, seis sombreros, SCAMPER, océano azul— más **divergencia y convergencia**, y todo lo que se dicte antes de que cierre su ventana. Regla para estudiar sin desperdiciar tiempo: **para el Quiz 1, lo de hoy; para el Parcial 1, lo de hoy más lo de la Sesión 02.** Si alguien viene a preguntarme si SCAMPER está en el quiz: no está, y lo tienen por escrito en la diapositiva.”

> “Las otras dos filas son los cortes que siguen, y el hilo del curso no cambia: en el **Corte 2** tipifican la propuesta con el **Manual de Oslo** y la validan con **FODA, Canvas y MVP**; en el **Corte 3** la consolidan con vigilancia y entidades de apoyo, y ahí sí hay un documento que se sube, la **ACA Final**. Nada de lo que escriben se pierde: se acumula en ese documento.”

> “**Slide 10 — Qué separa un entregable fuerte de uno flojo.** Léanla completa esta semana. Resumo la columna izquierda: usuario genérico, problema deducido de la solución que ya eligieron, evidencia tipo ‘todo el mundo sabe que’, fuentes copiadas de un blog sin autor y un documento escrito la noche anterior. Yo no evalúo **cuánto** escribieron: evalúo si **se entiende, se sostiene y avanzó** desde el corte anterior.”

> “**Slide 11 — Cómo se entrega.** Seis pasos y ninguno es opcional: escriben en la **plantilla APA CUN** abierta en **Google Docs** —no necesitan Office instalado—, revisan el checklist del enunciado, exportan a **PDF**, nombran el archivo **CRE_ACAFinal_Apellido**, lo suben al espacio del corte en **CDigital** y **verifican que abra** desde la plataforma. Un archivo corrupto cuenta como no entregado.”

> “Y la regla que más disgustos evita: **entrega oficial es CDigital**. No recibo trabajos por correo, ni por WhatsApp, ni por mensaje privado. Si se les complica una fecha, hablamos **antes** del cierre, no después.”

**Qué hacer:**
1. (3 min) Recorrer los ítems **en el libro de calificaciones del aula**, en pantalla: nombre, tipo y peso. No de memoria.
2. (4 min) Abrir el enunciado de la **ACA Final**, mostrar dónde está el checklist de criterios y abrir también el **Quiz 1** para que vean que ya existe y cuándo cierra. **Diga en voz alta la separación de alcance de la slide 9:** el **Quiz 1** se resuelve con el material de hoy (U1–U2 + la lectura **en lo que reporta**) y el **método Design Thinking** se pregunta en el **Parcial 1**. Las dos guías escritas están en `Clases/Recursos/ACAs/`: `Quiz 1 (6%)` y `Parcial 1 (24%)`.
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
**Slides:** 14 (HERRAMIENTAS) → 15 (CÓMO PEDIR AYUDA) → 16 (Acuerdos de convivencia del encuentro) → 21 (ACUERDOS DE TRABAJO)

**GUION LITERAL:**
> “**Slide 14 — Herramientas.** Todas gratis y todas desde el navegador: CDigital para las entregas y las notas; el **Drive de clases** para el material de cada sesión; Google Docs y Slides para escribir; Excalidraw para bocetos; Canvanizer para el Canvas del corte 2; Scholar, SciELO y Redalyc para buscar; ZoteroBib para armar las referencias en APA 7 sin instalar nada. **Nada de pagar ni de instalar.** Si una herramienta les pide tarjeta, no es la que estamos pidiendo.”

> “**Slide 15 — Cómo pedir ayuda.** Tres canales, en este orden. En el encuentro, los últimos minutos son para dudas y casi nadie los usa. En el **foro de CDigital**, las dudas que le sirven a todo el grupo: formato, entrega, alcance de la **ACA Final**; ahí respondo y la respuesta queda para los demás. Por **correo institucional**, lo personal. Asunto sugerido: **EI004, su nombre y el tema en cuatro palabras**. Respondo en días hábiles, normalmente entre 24 y 48 horas; no hay atención de madrugada ni domingo.”

> “Y una petición concreta: pregunten **la duda puntual**. ‘No entendí nada’ no se puede responder. ‘No sé si mi usuario es el estudiante o el laboratorista’ sí se responde en dos líneas.”

> “**Slide 16 — Convivencia.** Empezamos a la hora en punto. Nombre real en la sala. Micrófono cerrado por defecto y abierto para participar; **cámara bienvenida pero no obligatoria** —si no pueden, participen por el chat—. Lo que no funciona es estar conectado y ausente. Aquí se piensa en voz alta y se muestran borradores a medio hacer: **ninguna idea se ridiculiza**; las ideas se critican con criterio, a las personas no. Y si el encuentro se graba, lo aviso al inicio y la grabación queda en CDigital.”

> “**Slide 21 — Acuerdos de trabajo.** Son los tres que ya dijimos, juntos: la entrega es en CDigital, se trae el avance escrito a cada encuentro, y se cita siempre en APA 7.”

**Qué hacer:**
1. (3 min) Recorrer herramientas y pedirles que abran CDigital **ahora**, en otra pestaña, para confirmar que entran.
2. (2 min) Canales y tiempos de respuesta.
3. (2 min) Convivencia y acuerdos, en tono de acuerdo mutuo y no de reglamento leído.

---

#### 8️⃣ Encargo autónomo y cierre (~5 min) — Protagonista: Docente
**Slides:** 17–18 (PARA LA SESIÓN 02, la segunda es la «(cont.)») → 19–20 (PREGUNTAS DEL PRIMER DÍA) → 22 (PARA LA PRÓXIMA SESIÓN) → 23 (Cierre)

**GUION LITERAL:**
> “**Slide 17 — Para la Sesión 02** (sigue en la **18**). Cuatro cosas, y son cortas. Primera: la **lectura autónoma obligatoria**, unidades **U1 y U2** del Syllabus —Propuesta de Innovación, y creatividad e inteligencia emocional—; el material está en la carpeta de esta sesión, en el **Drive de clases** (el enlace les llega en el correo de bienvenida). Las retomamos en los primeros minutos de la próxima sesión: las repasamos, no las dictamos completas. Léanlas con una pregunta en la mano: **¿qué de esto me sirve para el problema que voy a elegir?**”

> “Segunda: entren al aula y **abran el Quiz 1** —el primer cuestionario, que cierra en la próxima sesión— para ver cuántas preguntas tiene y cuánto tiempo da; y abran el **enunciado de la ACA Final** y léanlo entero, con checklist. Tercera: **traigan escrito**, con tres líneas basta, un problema real que les moleste, **a quién** le pasa y **dónde** lo vieron. No me traigan una solución; tráiganme un problema: la solución es el trabajo del resto del curso. Cuarta: creen su documento en Google Docs con la plantilla APA CUN y déjenlo listo.”

> “**Slide 19 — Preguntas del primer día** (sigue en la **20**). Las dejo en pantalla mientras me preguntan lo que quieran: si se pierde fácil, si se puede en dúo, si sirve un trabajo de otro semestre y si hace falta programar. Las respuestas cortas están ahí; las largas se las doy ahora.”

> “**Slide 22 — Para la próxima sesión.** Resumido en tres líneas para que nadie lo pierda: lectura autónoma U1–U2, **Quiz 1** ubicado en el aula, enunciado de la **ACA Final** leído, y su problema escrito. Lo pego también en el chat y lo anuncio hoy mismo en CDigital; el material para hacerlo está en la carpeta de esta sesión, en el Drive de clases.”

> “**Slide 23 — Cierre.** Hoy no vimos tema y salimos sabiendo cómo se trabaja, qué se entrega y con quién cuentan. La **Sesión 02** arranca el contenido: *Creatividad e innovación en I+D, Design Thinking y técnicas*, y se trabaja sobre lo que ustedes traigan. Mismo enlace de siempre. Nos vemos.”

**Qué hacer:**
1. (2 min) Dictar el encargo autónomo y **escribirlo también en el chat** (lo que solo se dice, se pierde).
2. (2 min) Preguntas abiertas con la slide 19 proyectada (y la 20, si alcanzan las dudas de la segunda mitad).
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
| “¿Cuándo es la primera entrega?” | “Lo primero que se califica no es una entrega escrita: es el **Quiz 1**, un cuestionario que cierra en la próxima sesión. La fecha exacta está en el ítem de CDigital; ábralo hoy y anótela.” |
| “¿Los quices y parciales son en clase?” | “Sí: son cuestionarios de CDigital que cierran el mismo día de la sesión y por eso les reservo tiempo en clase. Faltar ese día es perder el ítem.” |
| “¿Y si no puedo conectarme a un encuentro?” | “Avise antes, abra la carpeta de esa sesión en el **Drive de clases** —ahí quedan el material y la consigna— y llegue al siguiente con el avance. La ausencia no mueve la fecha de entrega, y las entregas siguen yendo a CDigital.” |
| “¿Qué tema escojo? No se me ocurre nada.” | “No busque un tema: busque algo que **funcione mal** donde usted está. Un trámite lento, un dato que se pierde, una fila. De ahí sale la propuesta.” |
| “¿Se puede cambiar de problema después?” | “Sí, y es normal, sobre todo tras la Sesión 02. Lo que no se puede es llegar al Corte 2 sin haber elegido ninguno.” |

---

🧩 **Qué se lleva el estudiante de esta sesión**

**No hay entregable evaluado hoy** (el encuadre no se califica). Se lleva **tres cosas verificables**:

1. Haber **jugado el rompehielos** en Slido y haber dejado escrito en el **Q&A** algo que ha visto funcionar mal: es la semilla del problema que va a trabajar todo el semestre. Evento: {SLIDO}
2. El **Quiz 1** ubicado en el aula (cierra en la próxima sesión) y el enunciado de la **ACA Final** leído, con sus fechas anotadas en el calendario.
3. El **encargo autónomo** para la Sesión 02: lectura U1–U2, que está en la carpeta de la Sesión 01 del **Drive de clases**, + un problema real escrito en tres líneas (a quién le pasa y dónde lo vio) + documento de trabajo creado en Google Docs con la plantilla APA CUN.

**Criterio de éxito de la clase:** si al terminar un estudiante puede responder sin dudar *“¿qué produce este curso, cómo entrego y qué debo traer la próxima semana?”*, el encuadre funcionó.

---

✅ **Checklist del Docente antes de clase**
- [ ] Pantallazos de apoyo abiertos (`Guiones/Capturas/Sesion 01/`)
- [ ] Aula de **CDigital** abierta, con el anuncio de bienvenida publicado
- [ ] Abrí `Clases/{label}/Presentacion.pptx` (**23 slides**, portada incluida)
- [ ] **Las tres rondas ajustadas y la mentira de cada una marcada** en `{RUNBOOK_SLIDO}` *(material del Docente — sin esto el juego no se puede jugar)*
- [ ] **Evento de Slido** creado y probado desde el celular, con el **quiz de 3 preguntas**, la **encuesta A/B/C** de la ronda final y el **Q&A abierto**; el **código** copiado para el chat: {SLIDO}
- [ ] Decidido el **premio** y cómo se agenda la revisión uno a uno del ganador
- [ ] Material de la sesión cargado en `Clases/{label}/` (**Drive de clases**) — CDigital queda para la entrega y las notas
- [ ] **Libro de calificaciones** del aula abierto (ítems, tipos y pesos reales) y enunciado de la **ACA Final** desde `Clases/Recursos/ACAs/`
- [ ] **Plantilla APA CUN** abierta en Google Docs, lista para compartir pantalla
- [ ] Tengo decidida mi respuesta a: dúo, IA y entregas tarde
- [ ] Meet listo: {MEET}

📋 **Después de la clase (mismo día)**
- [ ] Publiqué en **CDigital** el anuncio con: enlace del evento de Slido (abierto 48 h para quien no se conectó), encargo autónomo (lectura U1–U2, que está en el Drive de clases) y recordatorio de que el **Quiz 1** ya está abierto en el aula
- [ ] Exporté el **Q&A de Slido** y la lista de participantes: anoté 3 problemas del grupo para usarlos como ejemplo en la Sesión 02 · verifiqué quién no se conectó
- [ ] Le escribí al **ganador** para agendar su revisión uno a uno
- [ ] Verifiqué que el espacio de entrega del Corte 1 esté visible para los estudiantes

---
*Fin del Guión — Sesión 01 (encuadre). Aquí no se dicta tema: el contenido del Syllabus arranca en la Sesión 02 y la unidad U1–U2 queda como lectura autónoma.*
"""


def guion_u2_inteligencia_emocional(meta):
    """**NO PROGRAMADA.** Guion de la U2 del Syllabus (IE · bloqueadores y ensanchadores ·
    mapa de utilidad). No está en `GUIONES` y por tanto no se escribe ningún .md con él.

    Existe porque el Syllabus EI004 tiene **8 unidades** y el periodo solo **7 encuentros**:
    U1–U2 quedaron como **lectura autónoma** desde la decisión docente del 2026-08-09
    (`unidad_diferida` en `sesiones_cun.py`). Ninguna sesión dicta U2 y **ningún deck de
    `config/slides/content/` tiene slides de U2**, así que enchufarlo hoy produciría un guion
    que habla de lo que la pantalla no muestra — el defecto que este archivo acaba de corregir.

    Se conserva, y no se borra, porque es el único material escrito de esa unidad: si algún
    día el periodo gana un octavo encuentro (o la U2 entra al deck de la S02), esto ya está
    redactado. Para activarlo hacen falta **las dos cosas**: una sesión en `sesiones_cun.py`
    y su JSON de contenido en `config/slides/content/`.
    """
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


def guion_02(meta):
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre + retomada de U1–U2 y puente desde el encuadre", 6, 6),
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

Hoy el foco fuerte es **Definir + Idear**. La **empatía** no se dictó en clase: la S01 fue de encuadre y lo que el estudiante trae es su **problema escrito en tres líneas** (a quién le pasa y dónde lo vio) más la **lectura autónoma de U1–U2**. Cuente con eso y no con más: si alguien llega sin observación de usuario, sirve igual para arrancar. El prototipo de hoy puede ser solo conceptual (un boceto feo en Excalidraw).

> **U1–U2 (lectura autónoma) se retoma aquí, en dos minutos y de viva voz** — es lo que promete el encuadre. No hay slides de esa unidad en el deck y **no se dicta**: se pregunta qué se llevaron y se conecta con el HMW de hoy. Los dos ganchos que sí sirven: *creatividad se entrena, no se tiene* (por eso hoy se practica divergir y converger) y *el bloqueador más común es juzgar la idea antes de escribirla* (la regla sagrada de la fase de ideación).

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

#### 1️⃣ Encuadre + retomada de U1–U2 y puente desde el encuadre (~6 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**Objetivo de la fase:** cerrar la lectura autónoma de U1–U2 con dos ganchos y conectar el problema que traen escrito con el reto de hoy (definir un HMW e idear).

**GUION LITERAL:**
> “Buenas tardes. Hoy es la **Sesión {n:02d}** y el tema es **Design Thinking y técnicas de creatividad**. Empiezo cumpliendo lo que prometí el primer día: la lectura autónoma de las unidades **1 y 2** —Propuesta de Innovación, y creatividad e inteligencia emocional— la **retomamos aquí**, no la dictamos. Y me la llevo en dos frases: la creatividad **se entrena**, no se tiene; y el bloqueador que más ideas mata es **juzgarlas antes de escribirlas**. Guárdense la segunda, porque en veinte minutos la van a necesitar.”

> “Lo otro que traían era su **problema en tres líneas**: a quién le pasa y dónde lo vieron. Hoy lo convertimos en dos cosas concretas: un **How Might We** bien redactado y un **banco de al menos 8 ideas** con 1 o 2 elegidas.”

> “Miren la **slide 2 — OBJETIVOS**. No venimos a llenar post-its bonitos: venimos a practicar un músculo —abrir muchas ideas y luego cerrar con criterio— que van a usar toda su vida profesional. Al final de la hora, su Propuesta de Innovación tendrá un reto claro y un primer boceto.”

**Qué hacer:**
1. (2 min) Portada + control de audio/nombres en Meet.
2. (2 min) Retomar U1–U2 con los dos ganchos y leer objetivos (slide 2). No dictar la unidad: no hay slides de U1–U2 en este deck y el tiempo es del taller.
3. (2 min) Pedir en el chat de Meet que 2 personas peguen su problema en una frase (a quién le pasa y dónde lo vieron).

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

> “**Slide 6 — PARA CONTINUAR.** Trabajo autónomo: (a) suban a CDigital su HMW + banco de ideas + boceto como `S02_Ideacion_Apellido`; (b) mejoren el boceto con una segunda mirada; (c) traigan a la próxima sesión una **clasificación tentativa** de su idea en un tipo de innovación —producto, proceso, organización, marketing o social—, que es justo lo que veremos con el Manual de Oslo.”

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
5. **Entregable:** `S02_Ideacion_Apellido` en CDigital (HMW + ideas + captura del boceto).
6. **Trabajo autónomo:** clasificación tentativa del tipo de innovación para la próxima sesión.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Tengo Excalidraw abierto (y una plantilla free de Miro como opción)
- [ ] Tengo listo mi HMW y mis 10 ideas modelo para la demostración
- [ ] Publiqué en CDigital el espacio de entrega `S02_Ideacion`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_03(meta):
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

> “**Slide 6 — PARA CONTINUAR.** Autónomo: (a) suban su ficha como `S03_FichaOslo_Apellido` a CDigital; (b) traigan a la próxima sesión un **cuadro comparativo** de su tipo elegido contra un tipo alternativo que descartaron, explicando **por qué no**.”

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
4. **Entregable:** `S03_FichaOslo_Apellido` en CDigital.
5. **Trabajo autónomo:** cuadro comparativo de tipo elegido vs. tipo descartado.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Preparé 1 ejemplo de Ingeniería por cada tipo Oslo
- [ ] Tengo la tabla de Google Docs (o Excalidraw) lista para clasificar en vivo
- [ ] Publiqué en CDigital el espacio de entrega `S03_FichaOslo`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_04(meta):
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

> “**Slide 6 — PARA CONTINUAR.** Autónomo: (a) suban su matriz como `S04_MatrizTipos_Apellido`; (b) preparen un listado de **mínimo 5 supuestos** que su propuesta da por verdaderos —cosas que, si fueran falsas, tumbarían el proyecto—; escríbanlos como **afirmaciones**, no como preguntas, para poderlos poner a prueba; (c) anoten **una pregunta sobre el entorno** de su propuesta: ¿ya existe algo parecido?, ¿hay una norma o un permiso de por medio? De ahí arranca la segunda mitad de la próxima sesión.”

> “**Slide 7 — Cierre.** La próxima clase es **doble**: en la primera mitad, **validación** —FODA, Business Model Canvas y MVP— para poner a prueba el supuesto más riesgoso; en la segunda, **vigilancia tecnológica**, para contrastar la propuesta con lo que ya existe ahí afuera. Va doble porque la **ACA Final califica las dos** y cierra antes de la última sesión del curso. Vengan con los supuestos escritos. Mismo Meet. Gracias.”

**Qué hacer:**
1. (4 min) Leer 2 conclusiones y verificar que se apoyan en criterios.
2. (2 min) Enunciar el trabajo autónomo (los 5 supuestos y la pregunta de entorno) y el nombre del archivo.
3. (2 min) Anunciar la próxima sesión **como doble** y decir en voz alta por qué: la ACA Final califica validación y vigilancia, y cierra antes del último encuentro.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Matriz comparativa de tipos — insumo de la Propuesta de Innovación.

1. Comparar tipo elegido vs. tipo alternativo con mínimo 5 criterios.
2. Escribir una conclusión de 4 líneas basada en la comparación.
3. **Criterio de éxito:** criterios explícitos + conclusión argumentada (no gusto personal).
4. **Entregable:** `S04_MatrizTipos_Apellido` en CDigital.
5. **Trabajo autónomo:** listado de mínimo 5 supuestos (escritos como afirmaciones) **y** una pregunta sobre el entorno de la propuesta — insumos de las dos mitades de la próxima sesión.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Preparé 2 ejemplos locales de incremental vs. radical
- [ ] Tengo la matriz del caso laboratorio lista para llenar en vivo (Excalidraw/Docs)
- [ ] Publiqué en CDigital el espacio de entrega `S04_MatrizTipos`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_05(meta):
    """S05 = sesión **doble** (U6 + U7): validación por dentro, vigilancia por fuera.

    U7 se adelantó una sesión porque la **ACA Final la califica** y cierra el 19/09, antes de
    la última clase. El deck (`config/slides/content/cun_creatividad_s05.json`) trae las dos
    mitades como un solo hilo y pide **un solo entregable**: `S05_ValidacionVigilancia_Apellido`.
    Este guion sigue ese deck slide por slide; si el JSON cambia, este guion cambia con él.
    """
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre + por qué hoy la sesión es doble", 5, 5),
        ("2️⃣ Por dentro: FODA, Canvas, MVP y la cadena de validación", 12, 17),
        ("3️⃣ Por fuera: vigilancia, fuentes y ficha de señal", 12, 29),
        ("4️⃣ Taller: validar por dentro y por fuera", 25, 54),
        ("5️⃣ Cierre + trabajo autónomo", 6, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión** *(sesión doble: **U6 + U7** del Syllabus)*
1. **Escribir** un FODA de máximo 6 bullets **verificables**, con lo interno y lo externo bien separados.
2. **Llenar** los cuatro bloques del Business Model Canvas que aclaran la propuesta: propuesta de valor, segmento, canales y actividades clave.
3. **Definir** un **MVP de aprendizaje** —lo más barato que responde la duda más cara—, no una “app completa”.
4. **Diseñar** la cadena de validación del supuesto **más riesgoso**, con un criterio de éxito numérico u observable fijado **antes** de probar.
5. **Distinguir** “informarse” de **vigilar**, y ejecutar el ciclo de cuatro pasos: observar → analizar → comunicar → **usar**.
6. **Levantar** mínimo **2 fichas de señal** de **frentes distintos** (Scholar y Google Patents), con fuente y fecha, que terminen en **una decisión escrita**.

> **Por qué las dos mitades hoy y no en dos semanas.** La **ACA Final** califica **validación y vigilancia**, y cierra **antes** de la última sesión del curso. Si la vigilancia se dictara después de ese cierre, el estudiante entregaría calificada una sección que nunca vio. Es un **reorden, no un recorte**: no se elimina ninguna unidad, U7 solo se adelanta a hoy y U8 a la próxima. Dígalo en voz alta en el minuto uno: el grupo tiene que entender por qué hoy corre más rápido de lo normal.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Este apartado asume que usted **no** viene de negocios **ni** ha hecho vigilancia tecnológica formal. Léalo completo: hoy dicta dos unidades y no hay margen para improvisar ninguna de las dos.

#### 1. Cómo se sostiene una sesión doble sin atropellar al grupo
La hora tiene **una sola idea** y dos maneras de aplicarla: *poner la propuesta a prueba*. **Por dentro** —¿qué de lo que creo no he comprobado?— y **por fuera** —¿qué hay allá afuera que yo no he mirado?—. Si usted presenta las dos mitades como dos temas sueltos, el grupo se pierde; si las presenta como **dos caras de la misma pregunta**, la hora se sostiene sola.

Las dos mitades terminan igual: en **una decisión escrita**. La primera produce una frase de tipo *“si 3 de 5 no pasan, pivoto el flujo”*; la segunda, una frase de tipo *“ajusto mi diferencia hacia la asignación automática”*. **Ese es el criterio de éxito de la hora**: no el número de páginas, sino que haya dos frases de decisión.

**Regla de tiempo:** nada se explica dos veces y nada se lee de la pantalla. Cada slide tiene un mensaje; dígalo, ponga el ejemplo del caso del laboratorio y siga. Lo que no alcance es **trabajo autónomo de esta misma semana** —no de la próxima—, porque la ACA Final no espera.

#### 2. FODA (DAFO) — la radiografía rápida y su única regla
**FODA** = **F**ortalezas, **O**portunidades, **D**ebilidades, **A**menazas (también **DAFO**). La división que casi todos confunden: **Fortalezas y Debilidades son INTERNAS** —dependen de usted y su equipo, y las puede cambiar—; **Oportunidades y Amenazas son EXTERNAS** —están en el entorno, y solo puede aprovecharlas o cubrirse—. El error típico de aula: poner *“falta de presupuesto de la universidad”* como debilidad. No es interna: es **amenaza**.

Regla de oro, única e innegociable: **cada ítem debe ser específico y verificable**.

| Cuadrante | Versión vacía (no sirve) | Versión verificable (sí sirve) |
| :--- | :--- | :--- |
| **Fortaleza** (interna) | “Somos creativos y comprometidos” | “Tengo acceso a **30 usuarios del laboratorio** esta semana” |
| **Debilidad** (interna) | “Nos falta experiencia” | “**Nadie del equipo** ha hecho una entrevista de usuario antes” |
| **Oportunidad** (externa) | “Hay mucha tecnología disponible” | “El campus **ya publica el horario** de laboratorios en un archivo abierto” |
| **Amenaza** (externa) | “Puede haber competencia” | “El laboratorio **exige autorización escrita** para cualquier piloto” |

Prueba rápida que puede aplicar en voz alta: **si un compañero no puede comprobar esa frase esta semana, todavía es un adjetivo, no un dato**. Y fíjese en las dos filas externas: **ya son señales de vigilancia**. Ese es el puente natural hacia la segunda mitad, úselo.

#### 3. Business Model Canvas (Osterwalder) — cuatro bloques, no nueve
El **Business Model Canvas (BMC)**, de **Alexander Osterwalder**, es un lienzo de **9 bloques** que describe en una página cómo una propuesta **crea, entrega y captura valor**. Hoy **no** se llenan los nueve, y no hace falta: un Canvas a medias pero **concreto** decide más que uno completo lleno de frases generales.

| # | Bloque | Pregunta clave que responde | Hoy |
| :---: | :--- | :--- | :--- |
| 1 | **Segmento de clientes** | ¿Para quién es? ¿Quién **usa**? | **Obligatorio** |
| 2 | **Propuesta de valor** | ¿Qué dolor alivia o qué gana el usuario? | **Obligatorio** |
| 3 | **Canales** | ¿Cómo **llega** la propuesta al usuario? | **Obligatorio** |
| 4 | Relación con el cliente | ¿Cómo se capta y se retiene? | Autónomo |
| 5 | **Actividades clave** | ¿Qué hay que hacer **sí o sí**? | **Obligatorio** |
| 6 | Recursos clave | ¿Qué se necesita: datos, gente, infraestructura? | Autónomo |
| 7 | Socios clave | ¿Quién ayuda desde afuera? | Autónomo |
| 8 | Estructura de costos | ¿Qué cuesta, aunque sea cualitativo? | Autónomo |
| 9 | Fuentes de ingreso | ¿Quién paga o cómo se sostiene si es social? | Autónomo |

Cómo se llena **bien** cada obligatorio, con el contraste que hay que decir en voz alta:
- **Segmento** — una persona concreta, no una categoría. Vago: “estudiantes”. Concreto: “**estudiantes de Ingeniería de 4º semestre que cursan laboratorio los martes**”.
- **Propuesta de valor** — lo que **gana el usuario**, no lo que hace su sistema. Vago: “una plataforma de gestión de turnos”. Concreto: “**llegas y ya tienes equipo asignado; dejas de perder tu hora**”.
- **Canales** — el camino real hasta esa persona. Vago: “redes sociales”. Concreto: “**el docente lo anuncia al inicio del laboratorio; el aviso llega por CDigital**”.
- **Actividades clave** — lo que hay que hacer sí o sí. Vago: “desarrollar el sistema”. Concreto: “**conseguir el horario real de ocupación**” y “**obtener el permiso del laboratorio**”.

Regla de escritura para los cuatro: **si la frase le sirve igual a otro proyecto del salón, todavía no es su Canvas.** Herramienta de clase: **Canvanizer** (https://canvanizer.com/new/business-model-canvas, gratis y en el navegador); **Excalidraw** o una tabla en Google Docs también valen. **Strategyzer** se muestra solo como referencia visual. El bloque **7, socios clave**, es el puente con la próxima sesión: anúncielo.

#### 4. MVP — Producto Mínimo Viable, de aprendizaje
El **MVP** es la versión **más pequeña** que permite **aprender de un usuario real**. La analogía que hay que dejar grabada: **no construyan el edificio entero para saber si alguien quiere vivir ahí; armen la maqueta que responde la duda más cara.**

Lo que el MVP **NO** es: no es “la app fea pero completa”, no es “la fase 1 del software grande”, y no es una versión con menos funciones pero igual de cara en tiempo. La pregunta que responde **no** es “¿funciona el código?”, sino **“¿esto le importa a alguien?”**. Consecuencia práctica que sorprende al grupo: **un MVP puede no tener nada de software** y seguir siendo válido. Definición operativa para hoy: **lo más barato que responde su duda más cara**.

| Tipo de MVP | En qué consiste | Qué pregunta responde | Costo |
| :--- | :--- | :--- | :--- |
| **Landing page** | Una página con la promesa y un botón de lista de espera | ¿Cuánta gente se anota? ¿A alguien le interesa? | 1 tarde |
| **Prototipo clicable** | Pantallas enlazadas entre sí, sin backend ni datos reales | ¿La persona entiende el flujo sin que yo se lo explique? | 2–3 horas |
| **Piloto “concierge”** | Usted hace **a mano** lo que después haría el sistema | ¿El usuario valora el resultado, aunque sea manual? | 1 semana |
| **Storyboard** | 4 viñetas del antes/durante/después, mostradas a 5 usuarios | ¿Reconocen el dolor? ¿La solución les hace sentido? | 1 hora |

El **concierge** es el más subestimado y el que más conviene empujar: prueba el **valor** antes de escribir una sola línea de código.

#### 5. La cadena de validación y el criterio que decide
Validar **no** es “mostrarle la idea a alguien”. Es una cadena corta y disciplinada:

**Supuesto → Riesgo si es falso → Prueba → Criterio de éxito → Decisión (seguir / pivotar / parar)**

Con el caso del laboratorio, resuelto entero (téngalo escrito, no lo improvise):
1. **Supuesto** — se escribe como **afirmación**: *“Los estudiantes registrarían la reserva si el flujo toma menos de 1 minuto.”*
2. **Riesgo si es falso** — *“Nadie usa el sistema y el problema del laboratorio sigue igual.”* Por eso este supuesto va **primero**: si falla, todo lo demás sobra.
3. **Prueba** — acción concreta, con **cuántas personas**, **qué hacen** y **cuánto dura**: *“5 estudiantes cronometran el registro en un prototipo en papel, sin ayuda mía.”*
4. **Criterio de éxito** — el número que decide, **fijado ANTES de probar**: *“≥ 4 de 5 terminan en menos de 60 s **y** dicen que lo usarían cada semana.”*
5. **Decisión** — *“Si 3 de 5 → no pasa: pivoto el flujo.”* Seguir, pivotar y parar son **las tres resultados válidos** del método.

Por qué el criterio va antes: si se fija después, el estudiante **ve lo que quiere ver**. Ese sesgo no se vence con buena voluntad, se vence con anticipación. Y una advertencia que hay que decir: **no se valida con opiniones de amigos**; sus amigos no son el segmento y no le van a decir que no.

| Criterio que NO sirve | Por qué falla | Criterio reescrito |
| :--- | :--- | :--- |
| “Que a la gente le guste” | “Gustar” no se observa ni se cuenta | “**4 de 5** dicen que lo usarían **la próxima semana**” |
| “Que sea fácil de usar” | Sin umbral, cualquier resultado “pasa” | “**4 de 5** terminan el flujo **en menos de 60 s** sin ayuda” |
| “Que muchos se interesen” | “Muchos” no es un número | “**Al menos 15** de 40 dejan su correo en la lista de espera” |
| “Que funcione bien” | Mide el sistema, no al usuario | “**Ningún** usuario pregunta ‘¿y ahora qué hago?’ durante la prueba” |

Fórmula de bolsillo para corregir en el taller: **[cuántos] de [cuántos]** hacen **[qué acción observable]** en **[qué condición]**. Si el criterio no cabe ahí, todavía es un deseo.

#### 6. Vigilancia tecnológica: informarse no es vigilar
La **vigilancia tecnológica** es un proceso **sistemático** de **capturar, filtrar, analizar y usar** información sobre tecnologías, competidores, normas y tendencias, con un fin concreto: **decidir mejor**. La palabra que carga todo el peso es **sistemático**: no es leer el artículo que apareció en el celular, es un **método repetible** con fuentes definidas y registro.

Lo que **no** es: no es “me informé”, no es acumular enlaces en un documento, y no es leer solo lo que confirma lo que ya se pensaba. **La prueba de fuego cabe en una pregunta: ¿cambió alguna decisión de su propuesta?** Si no ajustó ni confirmó nada, no vigiló: leyó.

| | Informarse | **Vigilar** |
| :--- | :--- | :--- |
| **1. Observar** | Cuando algo aparece por casualidad | En un momento **planeado**, con fuentes definidas de antemano |
| **2. Analizar** | Se lee y se sigue de largo | Se separa el **hallazgo** (lo que dice la fuente) de la **implicación** (lo que significa para usted) |
| **3. Comunicar** | Un enlace guardado, o nada | Una **ficha** que otro entiende sin explicación: fuente, fecha, implicación |
| **4. Usar** | Ningún efecto visible | Un **ajuste concreto**: de alcance, usuario, tecnología o riesgo |
| Frecuencia | Aleatoria | Repetible: se puede volver a hacer igual |
| Cómo se sabe que sirvió | Uno “se enteró” | **Cambió o confirmó una decisión** |

El paso **4** es el que casi siempre falta, y es el único que justifica los tres anteriores. Para un ingeniero esto vale oro: evita reinventar lo que ya existe gratis y documentado, detecta que una tecnología **acaba de volverse viable o barata**, y anticipa la norma o la política institucional que aparece al final, cuando ya no hay tiempo de ajustar nada.

#### 7. Los cuatro frentes de señal y dónde buscarlos (todo gratis, en el navegador)

| Tipo de señal | Fuentes gratis / web | Pregunta que responde |
| :--- | :--- | :--- |
| **Tecnología** | **Google Scholar** (scholar.google.com) · **Google Patents** (patents.google.com) · repositorios de GitHub · documentación oficial de estándares (IEEE) | ¿Qué se volvió **posible** o **barato**? |
| **Mercado** | Reportes públicos · listas de precios · notas de adopción · portales de **datos abiertos** | ¿Quién **ya paga** por esto y cuánto? |
| **Normativa** | Leyes y resoluciones · políticas institucionales · sitios de entidades públicas | ¿Qué me **limita** o me **habilita**? |
| **Social** | Hábitos y demografía · quejas públicas en redes y prensa · foros de usuarios | ¿Qué **cambió en el usuario**? |

El error más común es mirar **solo** el frente tecnológico. Dígalo tal cual: **las propuestas de estudiantes suelen morir por el frente normativo, que nadie revisó.** Por eso el taller exige señales de **frentes distintos**, no dos tecnológicas.

#### 8. Scholar y Google Patents sin ahogarse
**Google Scholar** da el **estado del arte académico**: qué se ha estudiado y qué se encontró.
- **Busque el PROBLEMA, no su solución.** Mal: “app de reservas CUN”. Bien: “gestión de turnos laboratorio universitario”.
- **Pruebe en inglés** (“laboratory scheduling system”), **use comillas** para frases exactas y **filtre por año** (“Desde 2020”) en el panel izquierdo.
- Mire **“Citado por”**: muchas citas señalan una referencia central, y desde ahí se salta a lo más reciente.

**Google Patents** muestra soluciones **ya documentadas o protegidas**, muchísimas más de las que uno imagina. La reacción típica del estudiante al encontrar algo parecido es **“mi idea murió”**; es exactamente al revés: **ahora sabe contra qué compite**. Busque con las palabras del problema, filtre por fecha, lea **solo el resumen y las figuras**, y revise **“Similar documents”** al final de la ficha. Lo que se escribe no es “existe algo parecido”, sino: **“existe X; mi diferencia está en Y”**.

En los dos: **título + autor o número + año**, siempre. Sin esos tres datos, lo que encontró **no es evidencia**. Si alguna búsqueda muestra un aviso de “tráfico inusual”, se continúa en el navegador normal — **no se instala nada**.

#### 9. La ficha de señal: cinco campos, con el ejemplo resuelto

| Campo | Señal 1 (académica) | Señal 2 (patente) |
| :--- | :--- | :--- |
| **1. Título** (frase suya, no la del documento) | Los sistemas de turnos reducen el tiempo muerto de laboratorio | Ya existe reserva de espacios por código QR |
| **2. Fuente + fecha + enlace** (los tres) | Artículo sobre gestión de turnos en laboratorios universitarios, Google Scholar, 2021 | Patente de sistema de reserva por QR, Google Patents, 2019 |
| **3. Hallazgo en 2 líneas** (con sus palabras) | La mayor pérdida no está en reservar, sino en los **choques de horario entre cursos** | El registro por QR ya está documentado como solución de reserva de espacios |
| **4. Implicación** (confirma · obliga a pivotar · es un riesgo) | **Confirma** el problema, pero **desplaza el foco**: atacar los choques, no el trámite | **Obliga a pivotar**: mi diferencia debe estar en la **asignación automática**, no en el registro |
| **5. Confianza** (alta · media · baja) | **Alta** — publicación académica con revisión | **Alta** — documento oficial de patente |

Lo que hay que hacer notar del ejemplo es **la fila 4**: las dos señales **cambiaron algo**. Una movió el foco del problema; la otra movió la diferencia de la solución. **Eso es vigilar.** Confianza baja no invalida una señal: solo indica que todavía no puede decidir sola.

#### 10. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| “Mi FODA: fortaleza, somos creativos.” | “Eso no se verifica. Cámbialo por un hecho: ‘acceso a 30 usuarios esta semana’.” |
| “El MVP es la app terminada pero sin diseño.” | “No. El MVP es lo más barato que responde tu duda más cara: una landing o un prototipo en papel sirve.” |
| “Ya validé: a mis amigos les gustó.” | “Tus amigos no son el segmento y no te dirán que no. Prueba con usuarios reales y un criterio medible.” |
| “Lleno el Canvas con frases generales.” | “Si esa frase le sirve a otro proyecto del salón, todavía no es tu Canvas. Sé concreto en valor y segmento.” |
| “¿Para qué elegir un solo supuesto?” | “Porque el tiempo es finito. Valida primero el que, si es falso, tumba todo el proyecto.” |
| “Ya vigilé: leí un artículo.” | “¿Cambió alguna decisión de tu propuesta? Si no, te informaste, no vigilaste.” |
| “Encontré una patente igual, mi idea murió.” | “Al contrario: ahora sabes contra qué compites. ¿En qué se diferencia la tuya?” |
| Pega un enlace sin fecha ni autor | “Una fuente sin fecha ni autor no es evidencia. Busca quién lo dice y cuándo.” |
| “No encuentro nada.” | “Cambia las palabras: busca el problema, no tu solución. Y prueba en inglés.” |
| “¿Por qué hoy vemos dos temas?” | “Porque la ACA Final califica los dos y cierra antes de la última sesión. No se quitó nada: se adelantó.” |

> **Que la prueba falle es un buen resultado.** Descubrir en la semana 3 que el supuesto era falso vale mucho más que descubrirlo el día de la sustentación. Dígalo antes del taller: baja el miedo y sube la honestidad de los criterios.

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

> **Los minutos de arriba son los de una hora sin evaluación.** Esta sesión cierra el **Parcial 2**, así que el plan real —el que verá unas líneas más abajo con la fase de evaluación incluida— **recorta las fases más largas**. Cuando los números no coincidan, manda el plan de clase, no la consigna de la slide.

**Triage si el reloj aprieta** (y hoy va a apretar): lo que **no** se sacrifica es la **cadena de validación con criterio** y la **ficha de señal**; son lo que la ACA Final califica. Lo primero que se recorta son los ejemplos de MVP y el recorrido de los nueve bloques del Canvas: están en el deck y el estudiante los lee solo.

---

#### 1️⃣ Encuadre + por qué hoy la sesión es doble (~5 min) — Protagonista: Docente
{slides_fase(label, portada_deck(n, titulo), "Hoy la propuesta se pone a prueba: por dentro y por fuera")}

**Objetivo de la fase:** que entiendan en tres minutos que hoy la propuesta **deja de estar bien argumentada y pasa a estar puesta a prueba**, y que eso tiene dos caras.

**GUION LITERAL:**
> “Buenas tardes. Hoy la propuesta se pone a prueba, **por dentro y por fuera**. Hasta ahora la suya está **bien argumentada**: tiene usuario, tiene tipo, tiene grado y tiene criterios. Pero sigue apoyada en **cosas que ustedes creen** y que nadie ha comprobado, y en un entorno que nadie ha mirado.”

> “Con el caso del laboratorio se ve rapidísimo: todo el proyecto se sostiene sobre una creencia —**‘el estudiante sí registraría su turno’**— y sobre un silencio: nadie averiguó si **eso ya existe** ni si el laboratorio **permite** un piloto. La creencia se ataca por dentro, con FODA, Canvas, MVP y una prueba. El silencio se ataca por fuera, con vigilancia tecnológica.”

> “Y les digo de una vez por qué las dos hoy y no en dos semanas: la **ACA Final califica validación y vigilancia**, y **cierra antes de la última sesión** del curso. No se quitó nada del programa; se **adelantó**. Eso significa que hoy vamos rápido y que lo que no alcancemos en clase queda como trabajo autónomo **de esta misma semana**, no de la próxima.”

> “Salen de la hora con cuatro cosas: un **mini-Canvas**, un **MVP en 5 líneas**, **una prueba con criterio medible** y un **tablero con mínimo 2 señales**, cada una con su implicación.”

**Qué hacer:**
1. (2 min) Portada, control de audio y de nombres en Meet.
2. (2 min) Nombrar la creencia y el silencio del caso del laboratorio; anunciar las dos mitades y el entregable único.
3. (1 min) Decir por qué la sesión es doble y que hoy el ritmo es más alto de lo normal.

---

#### 2️⃣ Por dentro: FODA, Canvas, MVP y la cadena de validación (~12 min) — Protagonista: Docente
{slides_fase(label, "FODA: la radiografía rápida (y su única regla)", "FODA: la versión que no sirve y la que sí", "Business Model Canvas: cuatro bloques, no nueve", "Los nueve bloques del Canvas y su pregunta clave", "MVP: la maqueta, no el edificio", "Cuatro MVP baratos que sí caben en un semestre", "La cadena de validación, con el caso resuelto", "Criterios de éxito: el que no sirve y el que sí")}

**Objetivo de la fase:** dejar las cuatro herramientas operables —FODA, Canvas, MVP y cadena— sin convertir la clase en teoría de administración.

**GUION LITERAL:**
> “Primero el **FODA**. Cuatro cajas: fortalezas y debilidades son **internas** —dependen de ustedes—; oportunidades y amenazas son **externas** —están en el entorno—. El error clásico: poner ‘falta de presupuesto de la universidad’ como debilidad. No es interna: es una **amenaza**. Y regla única, innegociable: **cada frase se tiene que poder comprobar esta semana**. ‘Somos creativos’ no vale. ‘Tengo acceso a 30 usuarios del laboratorio esta semana’ sí. Seis bullets buenos valen más que veinte frases bonitas.”

> “Fíjense en las dos filas externas del cuadro: **ya son señales de vigilancia**. Guárdenlas, porque en diez minutos las vamos a necesitar.”

> “Segundo, el **Business Model Canvas**, de Osterwalder: nueve bloques que cuentan en una página cómo su propuesta **crea, entrega y captura valor**. Hoy **no llenamos los nueve** y no hace falta: cuatro bien escritos deciden más que nueve genéricos. **Propuesta de valor** —lo que gana el usuario, no lo que hace su sistema—; **segmento** —una persona concreta, con rol y situación, no ‘estudiantes’—; **canales** —el camino real hasta esa persona—; y **actividades clave** —lo que hay que hacer sí o sí—. La prueba: **si la frase le sirve igual a otro proyecto del salón, todavía no es su Canvas**.”

> “Tercero, el **MVP**, y aquí va la frase que quiero que se lleven: **no construyan el edificio entero para saber si alguien quiere vivir ahí; armen la maqueta que responde la duda más cara**. El MVP no es la app fea pero completa, ni la fase 1 del software grande. Es **lo más barato que responde su duda más cara**. Puede no tener **nada** de software y seguir siendo válido: una landing con lista de espera, un prototipo clicable, un storyboard, o el piloto ‘concierge’ —donde ustedes hacen a mano lo que después haría el sistema—. La pregunta no es ‘¿funciona el código?’; es **‘¿esto le importa a alguien?’**.”

> “Y cuarto, lo que amarra todo: la **cadena de validación**. Cinco eslabones: **supuesto → riesgo si es falso → prueba → criterio de éxito → decisión**. Con el caso: supuesto, ‘los estudiantes registrarían la reserva si el flujo toma menos de un minuto’. Riesgo si es falso: nadie usa el sistema y el problema sigue igual. Prueba: cinco estudiantes cronometran un prototipo en papel, sin ayuda mía. Criterio: **cuatro de cinco en menos de sesenta segundos**, y que digan que lo usarían cada semana. Decisión: si pasan tres de cinco, **no pasa**: pivoto el flujo.”

> “Lo importante del ejemplo no es el número: es **cuándo se escribió**. El criterio va **antes** de la prueba. Si lo fijan después, van a ver lo que quieren ver, y eso no se arregla con buena voluntad. Y no se valida con amigos: sus amigos no son el segmento y no les van a decir que no.”

**Qué hacer:**
1. (4 min) FODA con la regla “específico y verificable”; corregir en vivo un ejemplo vacío del grupo y señalar que las filas externas ya son señales.
2. (4 min) Recorrer el Canvas priorizando los cuatro obligatorios, con el contraste vago/concreto de cada uno. Modelar dos bloques en Canvanizer.
3. (2 min) MVP con la analogía del edificio y la maqueta; nombrar los cuatro tipos baratos y empujar el “concierge”.
4. (2 min) Escribir la cadena de validación completa del caso e insistir en que el criterio se fija **antes**.
{shot("Herramientas/bmc_canvanizer.png", "Canvanizer — Business Model Canvas en vivo", "Abrir https://canvanizer.com/new/business-model-canvas y llenar propuesta de valor y segmento del caso del laboratorio. Strategyzer solo como referencia visual.")}
> **Si hay que recortar esta fase** (día de evaluación, y hoy lo es): se comprime el recorrido del Canvas y los tipos de MVP; **no** se recorta la cadena de validación ni el momento en que se fija el criterio.

---

#### 3️⃣ Por fuera: vigilancia, fuentes y ficha de señal (~12 min) — Protagonista: Docente
{slides_fase(label, "Segunda mitad: su MVP no vive en una burbuja", "Informarse vs. vigilar, y el ciclo de cuatro pasos", "Cuatro frentes de señal y dónde buscarlos (todo gratis, en el navegador)", "Scholar y Patents: cómo buscar sin ahogarse", "La ficha de señal: cinco campos, con el ejemplo resuelto")}

**Objetivo de la fase:** separar “informarse” de “vigilar”, mostrar dónde se busca y dejar una ficha de señal llenada en vivo.

**GUION LITERAL:**
> “Segunda mitad. Ya saben probar su propuesta por dentro; ahora hay que **levantar la vista del prototipo** y mirar el entorno. Tres cosas pasan cuando nadie mira afuera: se **reinventa** algo que ya existe, gratis y documentado, y se pierden semanas; no se nota que una tecnología **acaba de volverse viable o barata**, y la propuesta nace desactualizada; y aparece **una norma o una política institucional** al final, cuando ya no hay tiempo de ajustar nada.”

> “**Vigilancia tecnológica** es un proceso **sistemático** de capturar, filtrar, analizar y usar información sobre tecnologías, competidores, normas y tendencias, con un fin concreto: **decidir mejor**. La palabra que carga todo el peso es **sistemático**: no es leer el artículo que le apareció en el celular, es un método repetible, con fuentes definidas y con registro.”

> “El ciclo tiene cuatro pasos —**observar, analizar, comunicar y usar**— y el que casi siempre falta es el cuarto, que es justamente el único que justifica los otros tres. Por eso la prueba de fuego cabe en una pregunta: **¿cambió alguna decisión de su propuesta?** Si no ajustaron ni confirmaron nada, no vigilaron: **leyeron**.”

> “¿Dónde se mira? Cuatro frentes. **Tecnología**: Scholar, Google Patents, repositorios, estándares. **Mercado**: reportes públicos, precios, datos abiertos. **Normativa**: leyes, resoluciones, políticas de la institución. Y **social**: qué cambió en el usuario. Aviso importante: casi todos miran solo el frente tecnológico, y **las propuestas de estudiantes suelen morir por el normativo**, que nadie revisó. Por eso hoy les voy a pedir señales de **frentes distintos**.”

> “Cómo buscar sin ahogarse. En **Scholar**, busquen **el problema, no su solución**: ‘gestión de turnos laboratorio universitario’, no ‘app de reservas CUN’. Prueben en inglés, usen comillas para frases exactas y filtren por año. En **Patents**, si encuentran algo parecido, la reacción típica es ‘mi idea murió’. Es al revés: **ahora saben contra qué compiten**. No escriban ‘existe algo parecido’; escriban **‘existe X; mi diferencia está en Y’**. Y en los dos, copien **título, autor o número, y año**: sin esos tres datos no es evidencia, es un recuerdo.”

**Modelación en vivo (esto es lo que hace que la fase funcione):** con Scholar y Patents abiertos, busque el caso del laboratorio pensando en voz alta y llene **una ficha completa** en Google Docs delante de ellos. Cinco campos: **título** con sus propias palabras, **fuente + fecha + enlace**, **hallazgo en 2 líneas**, **implicación** —confirma, obliga a pivotar o es un riesgo— y **confianza**. Termine señalando la implicación: *“esta señal me obliga a pivotar: mi diferencia ya no es el registro, es la asignación automática”*. Eso, y no el enlace, es la vigilancia.

**Qué hacer:**
1. (3 min) Las tres cosas que pasan cuando nadie mira afuera + definición y ciclo de cuatro pasos, con la pregunta “¿cambió una decisión?”.
2. (3 min) Los cuatro frentes con sus fuentes; insistir en el frente normativo.
3. (3 min) Buscar en Scholar y en Patents en pantalla, pensando en voz alta.
4. (3 min) Llenar la ficha de señal completa y leer la implicación en voz alta.

> **Si hay que recortar esta fase:** se acorta la búsqueda en vivo (deje una pestaña ya buscada de antes), **no** el llenado de la ficha: es el modelo que los estudiantes van a copiar en el taller.

---

#### 4️⃣ Taller: validar por dentro y por fuera (~25 min) — Protagonista: Estudiantes
{slides_fase(label, "Errores frecuentes y respuestas", "Paso a paso: un solo documento con las dos mitades", "TALLER — Validar por dentro y por fuera (25 minutos)")}

**Antes de soltar el taller (30 segundos, con la slide del paso a paso en pantalla):** un solo documento en Google Docs, `Validación y vigilancia — [su propuesta]`, con dos títulos dentro: **A. Validación** y **B. Vigilancia**. Todo va ahí; no se abren dos archivos.

**GUION LITERAL (consigna):**
> “Pasamos al **TALLER**. Tienen **25 minutos** y trabajan sobre SU propuesta, en un solo documento con dos títulos: A. Validación y B. Vigilancia.”

> “**Bloque A, por dentro.** Uno: **FODA de máximo 6 bullets**, todos verificables, con interna y externa bien separadas. Dos: **Canvas mínimo** en Canvanizer —propuesta de valor, segmento, canales y actividades clave—; guarden el enlace de compartir o peguen una captura. Tres: **MVP en 5 líneas** y **una prueba** de su supuesto más riesgoso, con criterio **numérico u observable** escrito **antes**.”

> “**Bloque B, por fuera.** Cuatro: escriban primero **la pregunta que quieren responder** con la vigilancia; sin pregunta, la búsqueda se dispersa. Cinco: **mínimo 2 fichas de señal**, de **frentes distintos** —no las dos tecnológicas—, con fuente, **fecha**, hallazgo, implicación y confianza; peguen los datos **en el momento**, porque después no encuentran de dónde salió. Seis: cierren con una frase que empiece por **‘Ajusto…’** o **‘Confirmo…’**.”

> “Al final, **dos personas** comparten **solo la implicación** de una señal y **solo el criterio** de su prueba. No el documento completo. **Criterio de éxito:** una prueba con criterio que se pueda medir hoy mismo y **que podría fallar**, y 2 señales con fuente y fecha que produjeron **1 decisión escrita**.”

| Paso del taller | Qué tiene que quedar escrito | Si hay que recortar |
| :--- | :--- | :--- |
| **1.** FODA | Máximo 6 bullets verificables, interna/externa separadas | Se reduce a 4 bullets: uno por cuadrante |
| **2.** Canvas mínimo | Valor, segmento, canales y actividades clave | Se dejan **valor y segmento**; los otros dos, autónomo |
| **3.** MVP + prueba | MVP en 5 líneas y la cadena completa con criterio | **No se recorta**: es lo que califica la ACA Final |
| **4.** Pregunta de vigilancia | Una pregunta escrita antes de buscar | No se recorta: sin ella el paso 5 se dispersa |
| **5.** Fichas de señal | Mínimo 2, de frentes distintos, con fuente y fecha | Se baja a **1 ficha en clase** y la segunda queda de autónomo |
| **6.** Decisión | Una frase que empiece por “Ajusto…” o “Confirmo…” | **No se recorta**: es el producto de la hora |

> **El número que trae el título de la slide es el del taller completo.** Si el plan de clase de arriba le asignó menos minutos —porque hoy corre el Parcial 2—, manda el plan: use la columna “Si hay que recortar” y anuncie en voz alta que el resto es trabajo autónomo **de esta semana**.

**Tabla de acompañamiento:**

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe un FODA con adjetivos vagos | “‘Somos buenos’ no se mide. Dame un hecho que puedas comprobar esta semana.” |
| Pone “falta de presupuesto de la universidad” como debilidad | “Eso no depende de ti: es una **amenaza**. Las debilidades son internas.” |
| Se pierde llenando los nueve bloques del Canvas | “Hoy solo cuatro: valor, segmento, canales y actividades. El resto queda para esta semana.” |
| Describe el MVP como la app completa | “Recórtalo: ¿cuál es la versión más pequeña que te dice si a alguien le importa?” |
| Pone una prueba sin criterio de éxito | “¿Cómo sabrás si pasó? Fija el número o la observación **antes** de probar.” |
| Va a validar con amigos | “Tus amigos no son el segmento. ¿Quién es el usuario real que puedes tocar esta semana?” |
| Trae las dos señales del frente tecnológico | “Cambia una: mira normativa o mercado. Ahí es donde se caen estos proyectos.” |
| Pega un enlace sin fecha ni autor | “Sin fecha y sin autor no es evidencia. ¿Quién lo dice y cuándo?” |
| Llena fichas que no cambian nada | “Vigilancia decorativa. Si la ficha no ajusta ni confirma, bórrala: ocupa el lugar de una que sí decide.” |
| Copia el abstract entero | “Resúmelo en dos líneas. Lo que importa es la implicación para TU propuesta.” |

---

#### 5️⃣ Cierre + trabajo autónomo (~6 min) — Protagonista: Docente
{slides_fase(label, "Antes de entregar: revise usted mismo", "Para continuar — trabajo autónomo", cierre_deck(n))}

**GUION LITERAL:**
> “Tres ideas de hoy. Una: el **MVP** es la maqueta que responde la duda más cara, **no el edificio**. Dos: validar es **supuesto → prueba → criterio → decisión**, con el criterio fijado **antes**. Tres: vigilar es un **sistema**; si la señal no cambia una decisión, no sirvió.”

> “**PARA CONTINUAR.** (a) Suban el documento con las dos mitades como **`S05_ValidacionVigilancia_Apellido`** a CDigital, en PDF. (b) **Ejecuten la prueba**, aunque sea con **3 usuarios**, y anoten lo que pasó **tal cual**, incluso si el criterio no se cumplió: ese dato es el más valioso que van a tener, y que falle es un buen resultado. (c) Completen el tablero hasta **3 señales** y llenen los **cinco bloques restantes** del Canvas; empiecen por **socios clave**, que es el puente con la próxima sesión. (d) Preparen un listado de **mínimo 3 entidades de apoyo** —con el **nombre correcto**— de tipo universitario, público, privado o internacional, y anoten en una línea **qué le pedirían a cada una**. Si no saben qué pedir, esa entidad todavía no les sirve.”

> “**Cierre.** La próxima clase es **innovación local–internacional, entidades de apoyo y el pitch de 60 segundos**, y es la **última antes del cierre de la ACA Final**. Vengan con la propuesta lista para conectarla con el afuera. Mismo Meet. Gracias.”

**Qué hacer:**
1. (2 min) Escuchar 2 implicaciones y 1 criterio, y verificar en voz alta que el criterio **podría fallar**.
2. (2 min) Recorrer el checklist de la slide “Antes de entregar” y confirmar el nombre exacto del archivo.
3. (2 min) Enunciar las cuatro tareas autónomas y anunciar la próxima sesión como la última antes del cierre de la ACA Final.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Validación y vigilancia — insumo doble (U6+U7) de la Propuesta de Innovación.

1. FODA de máximo 6 bullets verificables, con interna y externa separadas.
2. Canvas mínimo en Canvanizer: propuesta de valor, segmento, canales y actividades clave.
3. MVP en 5 líneas + la cadena completa del supuesto más riesgoso, con criterio fijado antes de probar.
4. Tablero con **mínimo 2 fichas de señal** de **frentes distintos** (título, fuente + fecha + enlace, hallazgo, implicación, confianza).
5. **Criterio de éxito:** una prueba con criterio medible **que podría fallar** + 2 señales con fuente y fecha que produjeron **1 decisión escrita** (“Ajusto…” / “Confirmo…”).
6. **Entregable:** `S05_ValidacionVigilancia_Apellido` en CDigital (PDF, un solo documento con las dos mitades).
7. **Trabajo autónomo de esta misma semana:** ejecutar la prueba con al menos 3 usuarios, subir a 3 señales, completar los 5 bloques restantes del Canvas y listar 3 entidades de apoyo con su pedido.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo (son **dos** unidades: U6 y U7)
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Abrí Canvanizer (https://canvanizer.com/new/business-model-canvas) para modelar en vivo
- [ ] Tengo la cadena de validación del caso laboratorio ya escrita (no se improvisa)
- [ ] Abrí Google Scholar y Google Patents, **con una búsqueda de ejemplo ya probada**
- [ ] Tengo la ficha de señal modelo lista para llenar en pantalla
- [ ] Publiqué en CDigital el espacio de entrega `S05_ValidacionVigilancia`
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d} (sesión doble U6+U7). Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_06(meta):
    """S06 = U8: ecosistema, entidades de apoyo y pitch de 60 s.

    Adelantada una sesión: es la **última sincrónica antes del cierre de la ACA Final**, que
    califica justamente ecosistema y pitch. Deck: `cun_creatividad_s06.json`; entregable
    `S06_EcosistemaPitch_Apellido`.
    """
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre: la última antes del cierre de la ACA Final", 5, 5),
        ("2️⃣ Qué da el ecosistema · escalas · tipos de impacto", 9, 14),
        ("3️⃣ Mapa de entidades, encaje y pedido concreto", 9, 23),
        ("4️⃣ El pitch de 60 segundos: cinco tramos y ejemplo", 9, 32),
        ("5️⃣ Taller: mapa de entidades + guion del pitch", 22, 54),
        ("6️⃣ Cierre: la semana en que se cierra la ACA Final", 6, 60),
    ]
    return header(*meta) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión** *(**U8** del Syllabus, adelantada una sesión)*
1. **Explicar** qué le puede dar un ecosistema de innovación —y qué no— con los seis insumos que una propuesta necesita.
2. **Ubicar** la propuesta en una **escala** (local, regional, nacional, internacional) y decir cuál sería el paso siguiente.
3. **Declarar** el **tipo de impacto** con la fórmula *a quién + qué cambia + en cuánto*.
4. **Armar** un mapa de **mínimo 3 entidades reales**, de cuadrantes distintos, con el **nombre verificado** y **un pedido concreto** a cada una.
5. **Escribir y cronometrar** un **pitch de 60 segundos** en cinco tramos, que empiece por la persona y termine pidiendo algo.

> **Esta es la última sesión sincrónica antes del cierre de la ACA Final**, y la ACA califica **dos cosas de hoy**: el **ecosistema** (entidades de apoyo) y el **pitch**. La próxima sesión ya no alcanza a alimentar la entrega: sirve para **sustentar y consolidar** lo que hoy quede escrito. Dígalo al abrir, no al cerrar.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Su rol hoy es doble: enseñar a **conectar la propuesta con el mundo real** y enseñar a **contarla en 60 segundos**. Léalo completo; la parte de entidades exige nombres correctos y usted los va a decir en voz alta.

#### 1. Por qué existe un “ecosistema” de innovación
Una innovación **rara vez sobrevive sola**. Para pasar de prototipo a impacto necesita insumos que el estudiante no tiene: **capital, mentoría, redes de contactos, infraestructura, marco normativo y clientes**. El **ecosistema de innovación** es ese conjunto de **actores y reglas** que rodean a un equipo de I+D o a un emprendedor.

La metáfora que funciona en clase: **una semilla buena no basta; necesita tierra, agua, luz y clima**. Por eso el trabajo del curso no termina cuando se sube el archivo a CDigital: termina —de verdad— cuando **alguien de afuera le abre una puerta** a la propuesta. Y para que alguien abra esa puerta hay que saber **a quién tocarla** y **qué pedir** cuando abra.

Los seis insumos, con lo que hay que decir de cada uno:
- **Capital** — dinero para materiales, licencias o dedicación. **Rara vez es lo primero que falta.**
- **Mentoría** — alguien que ya se equivocó antes y le ahorra tres meses de camino.
- **Redes de contactos** — acceso a las personas correctas; suele valer más que el dinero.
- **Infraestructura** — laboratorios, equipos, espacios, datos.
- **Marco normativo** — permisos, avales, respaldo institucional para poder probar.
- **Clientes o usuarios reales** — el insumo más escaso y el que más rápido madura un proyecto.

Lo que el ecosistema **no** hace: no valida por usted, no arregla una propuesta sin usuario y no reemplaza la evidencia. **Si llega a una entidad sin saber qué problema resuelve, la puerta se abre y no pasa nada.**

#### 2. Escalas: la misma innovación cambia según dónde la ponga

| Escala | Qué se innova ahí | Quién decide y financia | Qué le exigen a usted |
| :--- | :--- | :--- | :--- |
| **Local** (barrio, campus, empresa) | Mejora de un proceso concreto, con usuarios que usted puede ver | La institución o el jefe del área | Un piloto pequeño y un permiso |
| **Regional** (ciudad, departamento) | Soluciones replicables en varios sitios parecidos | Alcaldías, gobernaciones, cámaras de comercio | Que sirva a más de un caso y se pueda medir |
| **Nacional** | Propuestas alineadas con políticas y focos del país | **MinCiencias**, **iNNpulsa**, ministerios sectoriales | Formulación formal, indicadores y contrapartida |
| **Internacional** | Retos abiertos, cooperación y escalamiento | Programas de cooperación, **OCDE**/**CEPAL** como referencia, corporativos | Inglés, estándares y evidencia comparable |

El mensaje central: **no se sube de escala saltando pasos**. Un **piloto local bien medido es el pasaporte** para la escala siguiente; sin él, la postulación nacional se cae en la primera revisión. Casi todos los proyectos del curso están —y deben estar— en escala **local**: eso no es poca ambición, es orden.

#### 3. Tipos de impacto: por qué le importa a un país
Una entidad no financia “una buena idea”: financia **un impacto que puede mostrar**. Hay cuatro tipos y conviene que el estudiante sepa cuál es el suyo:
- **Económico** — ahorro, productividad, empleo, ingresos. El más fácil de medir y el más pedido en convocatorias.
- **Social** — calidad de vida, acceso, inclusión, tiempo devuelto a las personas.
- **Ambiental** — consumo de energía, residuos, huella, uso de recursos.
- **Institucional / de conocimiento** — capacidades nuevas, datos disponibles, procesos que antes no existían.

El caso del laboratorio, tipificado: el impacto **no** es “una app”; es **tiempo de práctica recuperado** (social) y **uso más eficiente de equipos ya comprados** (económico). Regla para escribirlo: **impacto = a quién + qué cambia + en cuánto**. “Mejorar la experiencia” no es impacto; “**30 estudiantes recuperan una hora de práctica por semana**” sí. Entre dos propuestas iguales, gana la que **nombró su impacto y dijo cómo lo mediría**.

#### 4. El mapa de entidades — un mapa, no un directorio
No convierta la clase en un listado interminable. Presente **cuatro cuadrantes** con un ejemplo en cada uno y **verifique nombres y vigencia el día de clase**, porque los programas cambian.

| Cuadrante | Ejemplos orientativos | Qué suelen ofrecer |
| :--- | :--- | :--- |
| **Universitario** | Unidad de emprendimiento de la CUN · semilleros de investigación · laboratorios y docentes del programa | Mentoría, espacio, validación, contactos |
| **Público / mixto** | Cámaras de Comercio · programas de alcaldías y gobernaciones · **iNNpulsa** · **MinCiencias** | Convocatorias, capital semilla, formación |
| **Privado / redes** | Hubs y aceleradoras · centros de desarrollo tecnológico (p. ej. **Cidei**) · comunidades tech · empresas ancla del sector | Piloto, inversión, red de clientes |
| **Internacional** | Programas de cooperación · **open innovation** de multilatinas · plataformas de retos · marcos de referencia (**OCDE**, **CEPAL**) | Retos abiertos, financiación, escalamiento |

**Regla docente ineludible: no prometa cupos ni financiaciones.** Usted no controla esas convocatorias. Y una advertencia de forma que sí cuesta nota: **un nombre mal escrito hunde la credibilidad del documento** —es “MinCiencias”, no “Min Ciencia”; es “iNNpulsa”, no “Impulsa”—.

#### 5. Preguntar el encaje y escribir un pedido que se pueda responder
Antes de acercarse a cualquier entidad hay **una sola pregunta**: **¿para qué me sirve ESTA entidad?** Cinco encajes posibles, y se elige **uno** por entidad, no los cinco: **mentoría**, **capital semilla**, **networking**, **infraestructura** o **validación**.

**Si el estudiante no sabe qué pediría, la entidad todavía no le sirve.** No falla la entidad: falla que la propuesta aún no sabe qué le falta. Truco para descubrirlo: **vuelva al MVP y a la prueba de validación de la sesión pasada. ¿Qué le faltó para ejecutarla bien? Eso es lo que pide.**

| Pedido vago | Por qué no funciona | Pedido concreto |
| :--- | :--- | :--- |
| “Necesito apoyo para mi proyecto” | El otro no sabe qué hacer con eso y archiva el correo | “Solicito **20 minutos** para que revisen mi Canvas y mi MVP” |
| “Quisiera que me ayuden con usuarios” | No dice cuántos, ni cuándo, ni para qué | “Solicito acceso a **10 usuarios por 2 semanas** para probar el flujo” |
| “Me interesa participar en convocatorias” | Pide información que ya es pública | “Solicito confirmar **fechas y requisitos** de la convocatoria vigente” |
| “Busco financiación” | Sin monto ni destino, no es evaluable | “Solicito apoyo para **materiales de un piloto de 4 semanas**” |

Criterio de calidad de un pedido: **cabe en un correo de 5 líneas** y le permite al otro decir **sí o no** sin tener que preguntar nada más.

#### 6. El pitch de 60 segundos
Un pitch **no es contar todo**: es lograr que el otro **quiera una segunda conversación**. Con eso claro, el resto es fácil: **todo lo que no ayude a conseguir esa segunda charla, sobra**.

| Tramo | Contenido | Tiempo | Pregunta que responde |
| :---: | :--- | :---: | :--- |
| **1** | **Usuario + dolor** | ~10 s | ¿A quién y qué le duele? |
| **2** | **Insight** | ~10 s | ¿Qué observación lo cambia todo? |
| **3** | **Propuesta + tipo de innovación** | ~15 s | ¿Qué proponen y qué cambia? |
| **4** | **Evidencia breve** | ~15 s | ¿Por qué debería creerles? |
| **5** | **Pedido / siguiente paso** | ~10 s | ¿Qué necesitan de mí ahora? |

El error número uno y el más caro: **empezar por la tecnología** (“hicimos una app con inteligencia artificial que…”). Nadie se conecta con eso, ni siquiera la gente técnica. La tecnología entra en el **tramo 3, como medio**, nunca como protagonista. El **tramo 4** es el que separa un proyecto de aula de una propuesta creíble: ahí entra la **validación** o la **vigilancia** de la sesión pasada.

Tres reglas de forma: **una sola idea por tramo** (si mete dos, se pierden las dos); **números concretos** cuando los tenga (un número vale por tres adjetivos); y **termine pidiendo algo** (un pitch sin pedido deja al otro sin saber qué hacer).

Y una regla de ensayo que hay que enseñar explícitamente: cuando el pitch se pasa de tiempo, **se corta, no se acelera**. Hablar más rápido no arregla un pitch largo: lo vuelve incomprensible. Se corta empezando por los adjetivos y las explicaciones técnicas del tramo 3. Se **memoriza la estructura, no el texto**: un pitch recitado suena a discurso; uno estructurado suena a convicción.

#### 7. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| Lista entidades sin decir qué les pediría | “Una entidad sin pedido concreto no sirve. ¿Le pides mentoría, piloto, capital o contactos?” |
| Pone entidades genéricas o inventadas | “Necesito el nombre real y bien escrito, verificado en su sitio. ¿Existe y hace lo que dices?” |
| Empieza el pitch por la tecnología | “Empieza por la persona y su dolor. La app va en el tramo 3, como medio.” |
| Pitch de 3 minutos “porque hay mucho que contar” | “En 60 s no cuentas todo: logras que quieran una segunda charla. Corta lo demás.” |
| Se pasa de tiempo y habla más rápido | “No aceleres: **corta**. Empieza por los adjetivos del tramo 3.” |
| Confunde el producto con el impacto | “‘Una app’ no es impacto. A quién + qué cambia + en cuánto, eso sí lo es.” |
| “¿Me pueden dar el cupo o la beca?” | “No manejo esas convocatorias y no puedo prometer nada. Te enseño a identificarlas y a preguntar el encaje.” |
| Dice que su propuesta es “nacional” sin piloto | “Sin un piloto local medido, la postulación nacional se cae en la primera revisión.” |

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

> **Los minutos de arriba son los de una hora sin evaluación.** Esta sesión cierra el **Quiz 3**, así que el plan real —el de abajo, con la fase de evaluación— recorta la fase más larga. Cuando los números no coincidan, manda el plan de clase.

**Triage si el reloj aprieta:** lo que **no** se sacrifica es el **pedido concreto** (fase 3) y los **cinco tramos del pitch** (fase 4): son exactamente lo que la ACA Final califica y cierra esta semana. Lo primero que se recorta es el recorrido de escalas e impacto, que el estudiante puede leer del deck.

---

#### 1️⃣ Encuadre: la última antes del cierre de la ACA Final (~5 min) — Protagonista: Docente
{slides_fase(label, portada_deck(n, titulo), "Una semilla buena no basta")}

**Objetivo de la fase:** que entiendan que hoy la propuesta se conecta con el afuera **y** que esta es la última clase que alimenta la ACA Final.

**GUION LITERAL:**
> “Buenas tardes. Una innovación **rara vez sobrevive sola**. Para pasar de prototipo a impacto necesita cosas que ustedes todavía no tienen: **capital, mentoría, contactos, infraestructura, permisos y usuarios reales**. La metáfora del día: **una semilla buena no basta; necesita tierra, agua, luz y clima**. Ese entorno de actores y reglas es el **ecosistema**.”

> “Por eso su trabajo no termina cuando suben el archivo a CDigital. Termina de verdad cuando **alguien de afuera le abre una puerta** a la propuesta. Y para que alguien abra esa puerta hay que saber **a quién tocarla** y **qué pedir** cuando abra. Eso es lo de hoy.”

> “Aviso de calendario, sin rodeos: esta es la **última sesión antes del cierre de la ACA Final**, y la ACA califica **dos cosas de hoy**: el **ecosistema** y el **pitch**. La próxima clase ya no alcanza a alimentar la entrega: sirve para **sustentar y consolidar** lo que hoy quede escrito. Las fechas exactas están en CDigital y en la Presentación del Curso: revísenlas hoy, no el fin de semana.”

> “Salen de la hora con un **mapa de mínimo 3 entidades reales** con un pedido concreto a cada una, y el **guion del pitch de 60 segundos** cronometrado.”

**Qué hacer:**
1. (2 min) Portada, control de audio y de nombres en Meet.
2. (2 min) Metáfora de la semilla y los seis insumos, en una pasada rápida.
3. (1 min) Anunciar el cierre de la ACA Final y pedir que abran hoy mismo el ítem en CDigital para ver la fecha.

---

#### 2️⃣ Qué da el ecosistema · escalas · tipos de impacto (~9 min) — Protagonista: Docente
{slides_fase(label, "Qué le puede dar el ecosistema (y qué no)", "La misma innovación cambia de escala: local → internacional", "Tipos de impacto: por qué le importa a un país")}

**Objetivo de la fase:** que cada estudiante pueda decir **qué insumo le falta**, **en qué escala está** y **qué impacto declara**.

**GUION LITERAL:**
> “Seis insumos que una propuesta necesita y casi nunca consigue sola: **capital, mentoría, redes, infraestructura, marco normativo y usuarios reales**. Antes de salir a buscar plata, háganse una pregunta honesta: **¿cuál de los seis me falta de verdad hoy?** Casi nunca es el primero. Y lo que el ecosistema **no** hace: no valida por ustedes, no arregla una propuesta sin usuario y no reemplaza la evidencia.”

> “Segundo, **la escala**. La misma innovación cambia según dónde la pongan. **Local**: un proceso concreto, usuarios que usted puede ver, y le piden un piloto pequeño y un permiso. **Regional**: que sirva en varios sitios parecidos y se pueda medir. **Nacional**: **MinCiencias**, **iNNpulsa**, ministerios; ahí le piden formulación formal, indicadores y contrapartida. **Internacional**: cooperación y retos abiertos, con inglés y estándares. Y la regla que evita el ridículo: **no se sube de escala saltando pasos**. Un **piloto local bien medido es el pasaporte** para la siguiente. Casi todos ustedes están en local, y está perfecto.”

> “Tercero, **el impacto**. Una entidad no financia una buena idea: financia **un impacto que puede mostrar**. Cuatro tipos: económico, social, ambiental e institucional. Con el caso del laboratorio: el impacto **no es la app**; es **tiempo de práctica recuperado** —social— y **mejor uso de equipos ya comprados** —económico—. Y se escribe con una fórmula: **a quién + qué cambia + en cuánto**. ‘Mejorar la experiencia’ no es impacto. ‘Treinta estudiantes recuperan una hora de práctica por semana’ sí lo es. Entre dos propuestas iguales, **gana la que nombró su impacto y dijo cómo lo mediría**.”

**Qué hacer:**
1. (3 min) Los seis insumos y la pregunta “¿cuál me falta hoy?”; pedir dos respuestas por el chat.
2. (3 min) Recorrer la tabla de escalas y ubicar el caso del laboratorio en **local**.
3. (3 min) Los cuatro tipos de impacto y la fórmula; reescribir en vivo un “mejorar la experiencia” que alguien proponga.

---

#### 3️⃣ Mapa de entidades, encaje y pedido concreto (~9 min) — Protagonista: Docente
{slides_fase(label, "El mapa de entidades: cuatro cuadrantes", "Aprender a preguntar el encaje", '"Pedir apoyo" no es un pedido', "Ejemplo modelado: mapa de entidades del caso del laboratorio")}

**Objetivo de la fase:** que salgan sabiendo **a quién** acercarse y, sobre todo, **con qué frase**.

**GUION LITERAL:**
> “El mapa tiene **cuatro cuadrantes**. **Universitario**: la unidad de emprendimiento de la CUN, semilleros, laboratorios y docentes del programa. **Público y mixto**: Cámaras de Comercio, programas de alcaldías y gobernaciones, **iNNpulsa**, **MinCiencias**. **Privado y redes**: hubs, aceleradoras, centros de desarrollo tecnológico como **Cidei**, comunidades tech y empresas ancla de su sector. E **internacional**: cooperación, *open innovation* de multilatinas, plataformas de retos, y marcos de referencia como **OCDE** y **CEPAL**.”

> “Dos advertencias. La primera: esto es un **mapa, no un directorio**; los programas cambian, así que **verifiquen el nombre y la vigencia** el día que vayan a escribirlo. Un nombre mal escrito hunde la credibilidad del documento entero. La segunda, y sean conscientes: yo **no** les puedo prometer cupos ni recursos, porque no manejo esas convocatorias. Lo que sí les enseño es a **preguntar el encaje**.”

> “Preguntar el encaje es responderse una sola cosa: **¿para qué me sirve ESTA entidad?** Cinco opciones y se elige **una** por entidad: **mentoría, capital semilla, networking, infraestructura o validación**. Si no saben qué pedirían, la entidad todavía no les sirve —y no es culpa de la entidad: es que la propuesta aún no sabe qué le falta—. El truco para descubrirlo: **vuelvan a su MVP y a la prueba de la clase pasada. ¿Qué les faltó para ejecutarla bien? Eso es lo que piden.**”

> “Y ahora lo que más cuesta: **‘pedir apoyo’ no es un pedido**. ‘Necesito apoyo para mi proyecto’ termina archivado. ‘**Solicito 20 minutos para que revisen mi Canvas y mi MVP**’ se puede responder con un sí o un no. ‘Quisiera ayuda con usuarios’ no dice nada; ‘**solicito acceso a 10 usuarios por 2 semanas para probar el flujo**’ sí. Un buen pedido **cabe en un correo de cinco líneas** y no obliga al otro a preguntar nada más.”

**Modelación en vivo:** abra una tabla de tres columnas en Google Docs y llénela con el caso del laboratorio delante de ellos — Unidad de emprendimiento CUN / **mentoría** / *revisión del Canvas y del pitch, y 5 contactos de estudiantes usuarios*; área de TI o empresa del sector / **piloto** / *10 usuarios reales durante 2 semanas para cronometrar el flujo*; programa público o Cámara de Comercio / **convocatoria** / *confirmación de fechas y requisitos vigentes*. Subraye la tercera columna: **medible y acotada en el tiempo**, ninguna dice “pedir ayuda”.

**Qué hacer:**
1. (3 min) Recorrer los cuatro cuadrantes con un ejemplo por cada uno, pronunciando bien los nombres.
2. (2 min) Los cinco encajes y la regla “si no sabe qué pedir, la entidad no le sirve todavía”.
3. (4 min) Llenar el mapa del caso en pantalla y contrastar cada pedido vago con su versión concreta.

---

#### 4️⃣ El pitch de 60 segundos: cinco tramos y ejemplo (~9 min) — Protagonista: Docente
{slides_fase(label, "El pitch de 60 segundos: qué logra y qué no", "Los cinco tramos del pitch de 60 segundos", "Ejemplo modelado: el pitch completo, tramo por tramo", "Paso a paso: escribir y ensayar su pitch")}

**Objetivo de la fase:** que escuchen un pitch completo, cronometrado, y sepan exactamente cómo escribir el suyo.

**GUION LITERAL:**
> “Un pitch **no es contar todo**. Es lograr que el otro **quiera una segunda conversación**. Si eso les queda claro, el resto es fácil: **todo lo que no ayude a conseguir esa segunda charla, sobra**.”

> “El error número uno, y el más caro, es **empezar por la tecnología**: ‘hicimos una app con inteligencia artificial que…’. Nadie se conecta con eso, ni siquiera los técnicos. Se empieza por **la persona y su dolor**, que es lo único que todo el mundo entiende sin contexto. La tecnología va en el tramo 3, **como medio**.”

> “Cinco tramos. Diez segundos de **usuario y dolor**; diez de **insight**, la observación que lo cambia todo; quince de **propuesta y tipo de innovación**; quince de **evidencia**; y diez de **pedido**. Ojo con el tramo 4: **es el que separa un proyecto de aula de una propuesta creíble**, y ahí entra la validación o la vigilancia de la clase pasada.”

> “Escúchenlo entero, con cronómetro: ‘*Los estudiantes de Ingeniería pierden **hasta una hora** buscando un laboratorio libre.* — usuario y dolor, y todavía no aparece ninguna tecnología. *Al observarlos notamos que el **70 % de los choques** se concentra en **dos franjas** del día.* — ese es el insight, la observación que uno no esperaba. *Proponemos una **asignación automática desde el horario del curso**, sin trámite de reserva; es una innovación **de proceso**.* — quince segundos, y nombra el tipo, que muestra que sabe lo que está haciendo. *En una prueba con 5 estudiantes, **4 de 5 completaron el flujo en menos de un minuto** y dijeron que lo usarían cada semana.* — un número real vence a cualquier adjetivo; aquí es donde su validación paga. *Buscamos un **piloto de dos semanas con un curso** para medirlo en condiciones reales.*’ **Sesenta segundos exactos, y empecé por la persona, no por la app.**”

> “Tres reglas de forma: **una sola idea por tramo**; **números concretos** cuando los tengan; y **terminen pidiendo algo**. Y una regla de ensayo: casi todos pasan de noventa segundos en el primer intento, y es normal. Cuando eso pase, **corten, no aceleren**. Hablar rápido no arregla un pitch largo: lo vuelve incomprensible. Corten adjetivos y explicaciones técnicas del tramo 3. Y **memoricen la estructura, no el texto**: un pitch recitado suena a discurso; uno estructurado suena a convicción.”

**Qué hacer:**
1. (2 min) Qué logra un pitch y el error de empezar por la tecnología.
2. (2 min) Recorrer los cinco tramos con sus tiempos, señalando el tramo 4.
3. (3 min) Leer el pitch modelo completo **con cronómetro a la vista**, tramo por tramo.
4. (2 min) Las tres reglas de forma y el “corte, no acelere” del ensayo.

---

#### 5️⃣ Taller: mapa de entidades + guion del pitch (~22 min) — Protagonista: Estudiantes
{slides_fase(label, "Errores frecuentes y respuestas", "TALLER — Mapa de entidades + guion del pitch (23 minutos)")}

**GUION LITERAL (consigna):**
> “Pasamos al **TALLER**. Tienen **22 minutos** y cinco pasos.”

> “**Uno:** completen su **mapa de entidades** en Google Docs con **mínimo 3 entidades reales**, de **cuadrantes distintos**, con el **nombre verificado en el sitio de la entidad** y **un pedido concreto** a cada una. Si no encuentran el nombre, esa entidad no entra. **Dos:** escriban su **frase de impacto** — a quién + qué cambia + en cuánto. Una sola frase. **Tres:** escriban el **guion del pitch** siguiendo los cinco tramos; pueden bocetarlo en Excalidraw. **Cuatro:** **ensayen en parejas** con cronómetro: el que escucha repite qué entendió, y el que habla ajusta. **Cinco:** **dos voluntarios** hacen su pitch en vivo y les tomo el tiempo; el resto sustenta la próxima sesión.”

> “**Criterio de éxito:** 3 entidades con pedido concreto, y un guion en el que en **60 segundos** se entiendan **dolor, valor y pedido**. Verificación en pareja: si su compañero no puede repetir el pedido después de escucharlo, el tramo 5 está mal escrito. El cronómetro no es para presionarlos: es para que descubran cuánto sobra — y casi siempre sobra el tramo 3.”

| Paso del taller | Qué tiene que quedar escrito | Si hay que recortar |
| :--- | :--- | :--- |
| **1.** Mapa de entidades | 3 entidades reales, cuadrantes distintos, nombre verificado, un pedido concreto | **No se recorta**: la ACA Final lo califica y cierra esta semana |
| **2.** Frase de impacto | Una frase con a quién + qué cambia + en cuánto | No se recorta: es una sola frase |
| **3.** Guion del pitch | Una frase por tramo, los cinco tramos | **No se recorta**: la ACA Final lo califica |
| **4.** Ensayo en parejas | Tiempo real anotado y qué entendió el compañero | Se hace **en casa** y se reporta por el foro |
| **5.** Pitch en vivo | Dos voluntarios cronometrados | Pasa completo a la próxima sesión, que es de sustentación |

> **El número que trae el título de la slide es el del taller completo.** Si el plan de clase de arriba le asignó menos minutos —porque hoy cierra el Quiz 3—, manda el plan: recorte por los pasos 4 y 5, nunca por el 1 y el 3.

**Tabla de acompañamiento:**

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe “pedir apoyo” sin concretar | “¿Apoyo de qué: mentoría, piloto, capital o contactos? Elige uno y pon cuánto y por cuánto tiempo.” |
| Pone entidades genéricas o inventadas | “Necesito el nombre real y bien escrito. Ábrelo en su sitio antes de pegarlo.” |
| Elige las tres entidades del mismo cuadrante | “Diversifica: universitario, público y privado piden cosas distintas y te enseñan cosas distintas.” |
| No sabe qué pedirle a la entidad | “Vuelve a tu MVP: ¿qué te faltó para ejecutar la prueba? Eso es lo que pides.” |
| Confunde producto con impacto | “‘Una app’ no es impacto. ¿A quién le cambia qué, y en cuánto?” |
| Empieza el pitch por la tecnología | “Arranca por la persona y su dolor. La app va en el tramo 3.” |
| Se pasa de 60 segundos | “**Corta, no aceleres.** Empieza por los adjetivos del tramo 3.” |
| Termina el pitch sin pedir nada | “¿Qué quieres que haga el que te escuchó? Eso es el tramo 5.” |

---

#### 6️⃣ Cierre: la semana en que se cierra la ACA Final (~6 min) — Protagonista: Docente
{slides_fase(label, "Antes de entregar: revise usted mismo", "Para continuar — la semana en que se cierra la ACA Final", cierre_deck(n))}

**GUION LITERAL:**
> “Tres ideas de hoy. Una: una innovación **no sobrevive sola**; necesita un ecosistema que le dé lo que le falta. Dos: una entidad **sin un pedido concreto** no le sirve todavía. Tres: un pitch se gana **empezando por la persona**, no por la tecnología.”

> “**PARA CONTINUAR.** (a) Suban su mapa y su guion como **`S06_EcosistemaPitch_Apellido`** a CDigital. (b) **Esta es la semana de la ACA Final**: armen el **paquete consolidado** con lo que ya tienen —ficha del problema, ficha Oslo, matriz de tipos, Canvas, MVP y validación, tablero de vigilancia, mapa de entidades y guion del pitch—. **Nada de esto hay que inventarlo ahora**: son documentos que ya existen; lo que falta es **integrarlos en un solo texto** y que el usuario sea el mismo en todos. (c) **Revisen en CDigital la rúbrica y el espacio de entrega de la ACA Final** antes de subir, y verifiquen ahí la fecha exacta de cierre. Cerrado el espacio, la nota es la que hay.”

> “**Cierre.** La próxima sesión es la **última**: taller de **consolidación y sustentación**. Ya no se entrega nada nuevo: cada quien **sustenta su propuesta con el pitch**, recibe retroalimentación y cerramos el curso. Vengan con el pitch ensayado y el documento abierto: se habla, no se lee. Mismo Meet. Gracias.”

**Qué hacer:**
1. (2 min) Recorrer el checklist de la slide “Antes de entregar”, deteniéndose en “nombre verificado” y “el tramo 5 pide algo”.
2. (2 min) Enunciar el paquete consolidado y repetir que no se escribe nada nuevo: se integra.
3. (2 min) Anunciar la última sesión y qué hay que traer a ella.

---

🧩 **Actividad práctica / taller (resumen del entregable de hoy)**

**Nombre:** Mapa de entidades + frase de impacto + guion del pitch — última pieza de la Propuesta de Innovación.

1. Mapa de **mínimo 3 entidades reales**, de cuadrantes distintos, con nombre verificado y **un pedido concreto y acotado** a cada una.
2. **Frase de impacto**: a quién + qué cambia + en cuánto, con su tipo (económico, social, ambiental o institucional).
3. **Guion del pitch de 60 s** en cinco tramos, con un número real en el tramo 4 y un pedido en el tramo 5.
4. **Criterio de éxito:** 3 entidades con pedido concreto + un pitch que en 60 segundos comunica **dolor, valor y pedido**.
5. **Entregable:** `S06_EcosistemaPitch_Apellido` en CDigital.
6. **Trabajo autónomo de esta semana:** integrar el **paquete consolidado** de la ACA Final y revisar su rúbrica y su fecha de cierre en CDigital.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] **Verifiqué hoy** el nombre y la vigencia de las entidades que voy a nombrar (MinCiencias, iNNpulsa, Cidei, Cámara de Comercio, unidad de emprendimiento CUN)
- [ ] Tengo el mapa de entidades del caso laboratorio listo para llenar en vivo
- [ ] Tengo el pitch modelo ensayado y un cronómetro visible
- [ ] Publiqué en CDigital el espacio de entrega `S06_EcosistemaPitch`
- [ ] Tengo a la vista la fecha exacta de cierre de la ACA Final, leída desde CDigital
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Última sincrónica antes del cierre de la ACA Final. Documento autocontenido: un docente sin trayectoria en innovación puede estudiarlo y dictar la hora completa.*
"""


def guion_07(meta):
    """S07 = cierre: taller de consolidación y sustentación. No dicta contenido nuevo.

    La ACA Final y el Quiz 3 **ya cerraron**; hoy solo abren autoevaluación y coevaluación,
    que el inyector de `guion_evaluacion.py` agenda con sus propios minutos. Deck:
    `cun_creatividad_s07.json`. **No pide ningún archivo nuevo en CDigital** — el producto de
    la hora es una lista escrita de ajustes y la devolución de un compañero.
    """
    n, label, titulo, detalle = meta
    fases = [
        ("1️⃣ Encuadre de cierre: hoy se sostiene lo que ya escribió", 5, 5),
        ("2️⃣ El hilo completo y la trazabilidad del documento", 7, 12),
        ("3️⃣ Cómo se sustenta en tres minutos · las cinco preguntas", 8, 20),
        ("4️⃣ Retroalimentar con criterio y revisar costuras", 7, 27),
        ("5️⃣ Taller: sustentación cruzada y consolidación", 25, 52),
        ("6️⃣ Cierre del curso", 8, 60),
    ]
    return header(*meta, uso=USO_SESION_CIERRE) + mapa_slides(n) + f"""🎯 **Objetivos de la sesión** *(cierre: no hay contenido nuevo del Syllabus)*
1. **Sustentar** la propuesta en tres minutos: pitch de 60 s, dos preguntas y la frase de qué está listo y qué falta.
2. **Responder** con material propio las cinco preguntas que se le hacen a cualquier propuesta.
3. **Retroalimentar** a un compañero con la fórmula de las tres frases y los cuatro criterios de la rúbrica.
4. **Revisar** las seis costuras del documento y salir con una **lista escrita de ajustes**, mínimo tres.
5. **Diligenciar** en clase la **autoevaluación** (cuestionario) y participar en la **coevaluación** (foro), que abren hoy.

> **Hoy no se entrega nada nuevo y no se evalúa contenido:** la ACA Final y el Quiz 3 ya cerraron. Eso no hace la sesión menos importante — lo que el estudiante responda hoy **no cambia la nota de la ACA**, pero sí cambia el documento con el que va a golpear puertas después. Y descubrir hoy que no sabe explicar su propia propuesta en un minuto es mucho mejor que descubrirlo en una entrevista.

---

📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*

> Esta es la **última** sesión del curso y la única en la que usted habla poco. Su trabajo hoy es **conducir una ronda**: cronometrar, preguntar bien, cortar a tiempo y lograr que la retroalimentación entre pares sea útil y no cortés. Léalo completo: dirigir bien una ronda es más difícil que dictar.

#### 1. Qué hace útil una sustentación después de la entrega
La objeción va a salir: *“ya entregué, ¿para qué sustento?”*. La respuesta honesta: porque **el documento no se acaba en la nota**. Es la base de una convocatoria, de una opción de grado o de una entrevista de trabajo. Y porque la sustentación es el único momento del semestre en que alguien le señala el hueco **mientras todavía hay alguien al lado para señalarlo**.

Hoy pasan cuatro cosas, en este orden: **sustentación** con el pitch, **retroalimentación entre pares** con una fórmula, **consolidación** —revisar que las piezas hablen del mismo proyecto— y **cierre**, con auto y coevaluación. Pida dos cosas al abrir: **documento abierto y pitch ensayado**. Hoy se habla, no se lee.

#### 2. El hilo completo: de dónde viene cada sección
Vale la pena decirlo en voz alta, porque el grupo no ve el arco hasta que se lo nombran: **su propuesta ya no es una ocurrencia, es un argumento con evidencia**. Partieron de un problema real con un usuario que duele; lo convirtieron en un *How Might We* y un banco de ideas del que eligieron con criterios; le pusieron nombre con el Manual de Oslo; lo argumentaron contra una alternativa con una matriz; lo pusieron a prueba con Canvas, MVP y una validación con criterio fijado de antemano; lo contrastaron con el entorno en un tablero de vigilancia; y lo conectaron con el afuera con entidades reales, una frase de impacto y un pitch.

| Sesión | Lo que produjo | Dónde vive en la propuesta |
| :---: | :--- | :--- |
| **02** | Reto (HMW), banco de ideas y criterios de selección | Problema–oportunidad: usuario, dolor y evidencia |
| **03** | **Ficha Oslo**: tipo dominante, novedad, valor | Propuesta de valor y tipo de innovación |
| **04** | **Matriz comparativa** contra una alternativa + conclusión | Justificación del tipo y del grado |
| **05** | FODA, **Canvas**, **MVP** y la prueba con criterio; **tablero de vigilancia** | Validación y vigilancia tecnológica |
| **06** | **Mapa de entidades**, frase de impacto y **guion del pitch** | Ecosistema, siguiente paso y pitch anexo |
| **07** (hoy) | Sustentación, ajustes de coherencia y cierre | El documento revisado que se lleva del curso |

Úsela como diagnóstico: **si alguna fila no tiene documento en su carpeta, esa es la sección que hay que reconstruir** antes de usar la propuesta para cualquier otra cosa.

#### 3. La ronda: tres minutos por persona, con reloj
- **0:00 – 1:00 · El pitch.** Los cinco tramos, tal como se ensayaron.
- **1:00 – 2:30 · Dos preguntas.** Un compañero y el Docente. Se responde **corto y concreto**.
- **2:30 – 3:00 · La frase honesta.** **Qué está listo** y **qué falta**, una frase cada cosa.

Esa última frase es la que más pesa. Decir *“me falta probar con usuarios reales”* **no es una debilidad: es madurez de proyecto**. Lo que sí se nota mal es la propuesta que se declara terminada y se cae en la primera pregunta.

Tres reglas de sala que conviene anunciar antes de empezar: **no se lee la pantalla** (si necesita apoyo, una sola diapositiva con el dolor y el número); **no se pide disculpas al empezar** (“es que no me quedó muy bien” le quita autoridad a todo lo que venga después); y **se responde lo que se preguntó** — si no sabe, se dice **“no lo verifiqué”** y se sigue: es una respuesta válida y profesional.

#### 4. Las cinco preguntas que hay que hacer (y qué mide cada una)

| Pregunta | Qué está midiendo | Respuesta que funciona |
| :--- | :--- | :--- |
| ¿Quién es exactamente su usuario? | Si el problema tiene una persona detrás | Rol + situación: “estudiantes de 4º que cursan laboratorio los martes” |
| ¿Qué evidencia tiene de que eso pasa? | Si el problema es observado o supuesto | Un dato, una observación o una frase textual del usuario |
| ¿En qué se diferencia de lo que ya existe? | Si hubo vigilancia real | “Existe X; mi diferencia está en Y”, con la fuente a la mano |
| ¿Cómo sabría que su propuesta funcionó? | Si hay criterio, no deseo | El criterio de la prueba: [cuántos] de [cuántos] en [qué condición] |
| ¿Qué necesita ahora que no tiene? | Si sabe pedir el encaje | Un pedido concreto a una entidad concreta, acotado en el tiempo |

Las cinco se responden con material que el estudiante **ya escribió**. Si alguna lo deja en blanco, **ahí está el hueco de su documento** — y eso, no la nota, es lo que se lleva de hoy.

#### 5. Retroalimentar bien: la fórmula de las tres frases
Escuchar una sustentación **no es un descanso**: es la mitad del ejercicio, y es exactamente lo que se evalúa en la **coevaluación**. La fórmula, en este orden y sin salirse de ahí:
- **“Me quedó claro que…”** — una cosa que entendió sin esfuerzo. Le dice al otro qué sí funciona.
- **“No me quedó claro…”** — **una** sola cosa, específica. “No entendí quién es el usuario” sirve; “estuvo confuso” no.
- **“Le sugiero…”** — una acción concreta y ejecutable, no un juicio.

Lo que **no** cuenta: “muy bien, felicitaciones” (amable e inútil); “a mí me parece que deberías hacer una app” (eso es imponer su idea, no evaluar la del otro); y corregir la ortografía de la diapositiva mientras el problema de fondo sigue sin usuario. **Se critica la propuesta, nunca a la persona** — con el mismo criterio que le van a aplicar a usted en cinco minutos.

| Criterio de la rúbrica | Señal de que está flojo | Señal de que está sólido |
| :--- | :--- | :--- |
| **Claridad del problema** | Empieza por la solución o por la tecnología | En 10 s ya sabemos a quién le duele qué |
| **Solidez de la evidencia** | “Todo el mundo sabe que…” | Un número, una observación o una cita del usuario |
| **Diferencia** | “No hay nada parecido” (sin haber buscado) | Nombra lo que existe y dice en qué se aparta |
| **Claridad del pedido** | Termina sin pedir nada | Se puede responder con un sí o un no |

Esos cuatro criterios son los que el estudiante debe usar también **en el foro de coevaluación**: escribir con ellos, no con adjetivos.

#### 6. Consolidar es revisar costuras, no escribir más
El error de la consolidación es creer que hay que **agregar páginas**. Casi siempre hay que **quitar contradicciones**. Las seis costuras que más se rompen:
1. **El usuario es el mismo en todo el documento.** Si en la ficha del problema era el estudiante y en el Canvas es el laboratorista, uno de los dos sobra.
2. **El tipo Oslo coincide con lo que el Canvas describe.** Si dijo “innovación de proceso” y su propuesta de valor habla de un producto nuevo, algo se movió.
3. **El MVP prueba el supuesto que declaró más riesgoso.** Es el desajuste más común de todos.
4. **Alguna señal de vigilancia cambió algo visible.** Si el tablero está y la propuesta quedó idéntica, la vigilancia fue decorativa.
5. **Lo que le pide a la entidad es lo que al proyecto le falta.** Si pide capital pero lo que le falta son usuarios, el pedido está mal dirigido.
6. **El pitch dice lo mismo que el documento.** Si el pitch promete algo que el texto no sostiene, gana el texto: se corrige el pitch.

Prueba final del paquete: **un lector externo debería poder contar su propuesta después de leerla una vez.** Si no puede, sobra texto o falta hilo.

#### 7. Auto y coevaluación: qué son y por qué se hacen en clase
Son **dos ítems del corte 3 con nota propia** y **abren hoy** en CDigital. La **autoevaluación** es un **cuestionario**: no se trata de ponerse 5,0 ni de castigarse, sino de **argumentar con hechos del semestre** — ¿entregué a tiempo?, ¿trabajé por semanas o la última noche?, ¿incorporé la retroalimentación?, ¿qué haría distinto? La **coevaluación** es un **foro**: se **participa escribiendo**, no se sube archivo, y se escribe con los cuatro criterios de la rúbrica.

Pesan poco por separado, pero **son las notas más fáciles de perder: se pierden por no entrar**. Por eso se abren en pantalla y se diligencian en clase. Los minutos y el guion exacto de esa fase los inserta el modelo de evaluación más abajo; no los improvise aquí.

#### 8. Errores frecuentes / preguntas trampa

| Error o pregunta trampa del estudiante | Respuesta sugerida del docente |
| :--- | :--- |
| “Ya entregué, ¿para qué sustentar?” | “Porque el documento no se acaba en la nota: es la base de una convocatoria, de una opción de grado o de una entrevista.” |
| Lee el documento en voz alta | “El pitch se cuenta, no se lee. Si necesitas apoyo, una sola diapositiva con el dolor y el número.” |
| Empieza pidiendo disculpas | “‘No me quedó muy bien’ borra seis sesiones de trabajo antes de tu primera frase. Arranca por el usuario.” |
| Inventa una respuesta que no verificó | “‘No lo verifiqué’ es una respuesta profesional. Inventar no lo es.” |
| “Mi propuesta cambió después de entregar.” | “Perfecto, dilo. Que la propuesta evolucione con la evidencia es exactamente lo que este curso quería enseñar.” |
| Retroalimenta con “muy bien, felicitaciones” | “Eso es amable e inútil. Usa las tres frases: me quedó claro / no me quedó claro / te sugiero.” |
| Cree que consolidar es escribir más | “Consolidar es quitar contradicciones. Revisa las seis costuras antes de agregar una sola página.” |
| Deja la coevaluación “para la casa” | “El foro tiene ventana. Lo que no queda escrito ahí no existe para el libro de calificaciones.” |

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

> Hoy **no hay evaluación de contenido**, pero **sí abren la autoevaluación y la coevaluación**: el modelo de evaluación inserta esa fase con sus propios minutos justo antes del cierre, y recorta la fase más larga para hacerle sitio. Las slides «Autoevaluación y coevaluación: qué son y cómo se diligencian» pertenecen a **esa** fase — no las adelante.

**Triage si el reloj aprieta:** lo que **no** se sacrifica es la **ronda de sustentación** (paso 1 del taller) ni los **minutos de auto y coevaluación**: son, respectivamente, el sentido de la sesión y una nota que se pierde por no entrar. Lo primero que se recorta es el recorrido del hilo y la trazabilidad, que está entero en el deck.

---

#### 1️⃣ Encuadre de cierre: hoy se sostiene lo que ya escribió (~5 min) — Protagonista: Docente
{slides_fase(label, portada_deck(n, titulo), "Hoy no se entrega nada nuevo: hoy se sostiene lo que ya escribió")}

**Objetivo de la fase:** dejar clarísimo que hoy no se entrega nada, que igual hay que trabajar, y anunciar el orden de la hora.

**GUION LITERAL:**
> “Buenas tardes. Esta es la **última sesión** del curso. La **ACA Final ya cerró** y el **Quiz 3** también, así que hoy **no hay evaluación de contenido nueva** — y eso no hace la sesión menos importante, se los digo de una vez.”

> “Hoy pasan cuatro cosas, en este orden. **Sustentación**: cada quien defiende su propuesta con el **pitch de 60 segundos** y responde dos preguntas. **Retroalimentación entre pares**, con una fórmula, no con ‘me gustó’. **Consolidación**: revisamos que las siete piezas de su documento hablen del mismo proyecto. Y **cierre**: la **autoevaluación** y la **coevaluación**, que se abren hoy en CDigital, más la ruta de lo que sigue.”

> “¿Por qué sustentar después de entregar? Por dos razones honestas. La primera: lo que respondan hoy **no cambia la nota de la ACA**, pero sí cambia el documento con el que van a golpear puertas después. La segunda: descubrir hoy que no saben explicar su propia propuesta en un minuto es **muchísimo mejor** que descubrirlo en una entrevista de trabajo.”

> “Dos cosas necesito de ustedes: **el documento abierto** y **el pitch ensayado**. Hoy se habla, no se lee.”

**Qué hacer:**
1. (2 min) Portada, control de audio y de nombres; confirmar quién tiene el pitch listo.
2. (2 min) Anunciar el orden de la hora y que hoy no se entrega archivo nuevo.
3. (1 min) Anunciar que la ronda es cronometrada, para que se preparen desde ya.

---

#### 2️⃣ El hilo completo y la trazabilidad del documento (~7 min) — Protagonista: Docente
{slides_fase(label, "El hilo completo de su Propuesta de Innovación", "Trazabilidad: qué sesión produjo qué sección del documento")}

**Objetivo de la fase:** que vean el arco completo y detecten, con la tabla en pantalla, qué sección les falta.

**GUION LITERAL:**
> “Miren de dónde vienen. Partieron de **un problema real**, con un usuario y un dolor concreto. Lo convirtieron en un **How Might We** y en un banco de ideas del que eligieron **con criterios**. Le pusieron **nombre** con el Manual de Oslo: un tipo dominante, justificado. Lo **argumentaron** contra una alternativa, con una matriz y una conclusión escrita. Lo pusieron a prueba con un **Canvas, un MVP y una validación** con criterio fijado de antemano. Lo **contrastaron con el entorno** en un tablero de vigilancia, y ajustaron. Y lo conectaron con el **afuera**: entidades reales, una frase de impacto y un pitch.”

> “Su propuesta ya no es una ocurrencia: es **un argumento con evidencia**. Y cada pieza de esa lista es un documento que **ya existe**. Hoy no se produce nada nuevo: se **verifica que todas hablen del mismo proyecto**.”

> “Usen la tabla de trazabilidad como diagnóstico, ahora mismo, con su carpeta abierta: si alguna fila **no tiene documento**, esa es justamente la sección que van a tener que reconstruir antes de usar esta propuesta para cualquier otra cosa — una convocatoria, la opción de grado o una entrevista.”

**Qué hacer:**
1. (3 min) Recorrer el arco completo en voz alta, sesión por sesión, sin detenerse en ninguna.
2. (3 min) Proyectar la tabla de trazabilidad y pedir que cada quien marque en su carpeta las filas que tiene.
3. (1 min) Preguntar por el chat cuántas filas le faltan a cada uno. Es el termómetro de la hora.

---

#### 3️⃣ Cómo se sustenta en tres minutos · las cinco preguntas (~8 min) — Protagonista: Docente
{slides_fase(label, "Cómo se sustenta una propuesta en tres minutos", "Las cinco preguntas que le van a hacer (y cómo se responden)")}

**Objetivo de la fase:** dejar el formato de la ronda sin ambigüedad y anticipar las preguntas, para que nadie sustente a ciegas.

**GUION LITERAL:**
> “La sustentación tiene **tres minutos y el reloj corre**. Del minuto cero al uno, **el pitch**: los cinco tramos tal como los ensayaron. Del uno al dos y medio, **dos preguntas**: una de un compañero y una mía; se responde **corto y concreto**. Y los últimos treinta segundos, **la frase honesta**: qué está listo y qué falta, una frase cada cosa.”

> “Esa última frase es la que más pesa, y quiero que me crean: decir ‘me falta probar con usuarios reales’ **no es una debilidad, es madurez de proyecto**. Lo que sí se nota mal es la propuesta que dice estar terminada y se cae en la primera pregunta.”

> “Tres reglas de la sala. **No se lee la pantalla**: si necesitan apoyo, una diapositiva con el dolor y el número de evidencia, una sola. **No se pide disculpas al empezar**: ‘es que no me quedó muy bien’ le quita autoridad a todo lo que venga después. Y **se responde lo que se preguntó**: si no saben, digan **‘no lo verifiqué’** y sigan. Es una respuesta válida y profesional; inventar no lo es.”

> “Y para que nadie sustente a ciegas, aquí están **las cinco preguntas** que les voy a hacer, en pantalla: quién es exactamente su usuario; qué evidencia tienen de que eso pasa; en qué se diferencia de lo que ya existe; cómo sabrían que su propuesta funcionó; y qué necesitan ahora que no tienen. Las cinco se responden con material que **ustedes ya escribieron**. Si alguna los deja en blanco, ahí está el hueco de su documento — y eso es lo que se llevan de hoy.”

**Qué hacer:**
1. (3 min) Explicar los tres tiempos de la ronda con el reloj a la vista.
2. (2 min) Las tres reglas de sala, en tono de acuerdo y no de reglamento.
3. (3 min) Recorrer las cinco preguntas y su columna de “respuesta que funciona”; pedir que cada quien marque cuál lo deja en blanco.

---

#### 4️⃣ Retroalimentar con criterio y revisar costuras (~7 min) — Protagonista: Docente
{slides_fase(label, "Retroalimentar bien: la fórmula de las tres frases", "Rúbrica de la ronda: qué mirar cuando escucha a un compañero", "Consolidar es revisar costuras, no escribir más", "Errores frecuentes en la sustentación")}

**Objetivo de la fase:** que el que escucha tenga trabajo —y que la consolidación se entienda como quitar contradicciones, no como escribir más.

**GUION LITERAL:**
> “Escuchar una sustentación **no es un descanso**: es la mitad del ejercicio, y es exactamente lo que se evalúa en la **coevaluación**. Van a usar **tres frases**, en este orden y sin salirse de ahí. **‘Me quedó claro que…’**: una cosa que entendieron sin esfuerzo, que es información útil para el otro. **‘No me quedó claro…’**: **una** sola cosa y específica —‘no entendí quién es el usuario’ sirve; ‘estuvo confuso’ no—. Y **‘le sugiero…’**: una acción concreta y ejecutable, no un juicio.”

> “Lo que **no** cuenta como retroalimentación: ‘muy bien, felicitaciones’, que es amable e inútil; ‘a mí me parece que deberías hacer una app’, que es imponer su idea en vez de evaluar la del otro; y corregir la ortografía de la diapositiva mientras el problema de fondo sigue sin usuario. Se critica **la propuesta**, nunca a la persona. Y se critica con criterio: el mismo que les van a aplicar a ustedes en cinco minutos.”

> “Mientras escuchan, miren **cuatro criterios**: claridad del problema —¿en diez segundos ya sabemos a quién le duele qué?—; solidez de la evidencia —¿hay un número o una cita, o es ‘todo el mundo sabe que’?—; diferencia —¿nombra lo que existe y dice en qué se aparta?—; y claridad del pedido —¿se puede responder con un sí o un no?—. Esos mismos cuatro son los que van a usar después en el foro.”

> “Y lo último antes del taller: **consolidar no es escribir más**. El error clásico es creer que hay que agregar páginas; casi siempre hay que **quitar contradicciones**. Seis costuras: que el **usuario sea el mismo** en todo el documento; que el **tipo Oslo coincida** con lo que describe el Canvas; que el **MVP pruebe el supuesto** que ustedes declararon más riesgoso —este es el desajuste más común de todos—; que **alguna señal de vigilancia haya cambiado algo visible**; que lo que le piden a la entidad sea **lo que al proyecto le falta**; y que **el pitch diga lo mismo que el documento** —si el pitch promete lo que el texto no sostiene, gana el texto: corrijan el pitch—.”

**Qué hacer:**
1. (3 min) La fórmula de las tres frases y lo que no cuenta como retroalimentación.
2. (2 min) Los cuatro criterios de la rúbrica, anunciando que se usan también en el foro.
3. (2 min) Las seis costuras, rápido, y la prueba final: “¿un lector externo podría contar su propuesta después de leerla una vez?”.

---

#### 5️⃣ Taller: sustentación cruzada y consolidación (~25 min) — Protagonista: Estudiantes
{slides_fase(label, "TALLER — Sustentación cruzada y consolidación (25 minutos)")}

**GUION LITERAL (consigna):**
> “Pasamos al **TALLER**. Tienen **25 minutos** y cuatro pasos.”

> “**Paso 1 — Ronda de sustentación.** Turnos de tres minutos: pitch de 60 segundos, dos preguntas, y la frase de qué está listo y qué falta. El que escucha toma nota con los **cuatro criterios de la rúbrica**: **una línea por criterio**, no más. **Paso 2 — Devolución en pareja.** Cada quien le entrega a su compañero las **tres frases**: me quedó claro, no me quedó claro, le sugiero. **Paso 3 — Revisión de costuras.** Con la devolución en la mano, revisen las **seis costuras** de su documento y anoten los ajustes en una lista. **No los hagan ahora: anótenlos.** Escribir la lista **es** el producto del taller. **Paso 4 — Abran CDigital** y verifiquen que ven los espacios de **autoevaluación** y **coevaluación**, y sus fechas.”

> “**Criterio de éxito:** salen de la sesión con **una lista escrita de ajustes** —mínimo tres— y con **la devolución de un compañero anotada, no recordada**. Segunda verificación: su compañero pudo repetir su **dolor, su valor y su pedido** sin mirar el documento. Y quien no alcance a sustentar hoy lo hace por el **foro del curso**: guion del pitch escrito más la frase de qué está listo y qué falta.”

| Paso del taller | Qué tiene que quedar escrito | Si hay que recortar |
| :--- | :--- | :--- |
| **1.** Ronda de sustentación | Notas del oyente: una línea por criterio de la rúbrica | **No se recorta**: es el sentido de la sesión. Si no alcanza para todos, los demás sustentan por el foro |
| **2.** Devolución en pareja | Las tres frases, escritas y entregadas al compañero | Se hace por escrito en el chat o en el foro |
| **3.** Revisión de costuras | Lista de **mínimo 3 ajustes** — anotados, no ejecutados | Se dejan **las tres costuras** que el compañero señaló |
| **4.** Abrir CDigital | Auto y coevaluación **vistas en pantalla**, con sus fechas | **No se recorta**: pasa a la fase de evaluación, que ya tiene minutos propios |

> **El número que trae el título de la slide es el del taller completo.** Si el plan de clase de arriba le asignó menos minutos, manda el plan: acorte la ronda a los voluntarios y mande el resto al foro, pero **no elimine la devolución en pareja**: sin ella, el paso 3 se queda sin insumo.

**Cómo conducir la ronda (esto es lo que hace que funcione):**
1. **Cronómetro visible y turnos anunciados de a dos**: “sustenta Camila, pregunta Andrés; después sustenta Andrés”. Nadie se queda esperando sin saber cuándo le toca.
2. **Corte a los 60 segundos, con amabilidad y sin excepción.** Si deja pasar el primer pitch de dos minutos, perdió la ronda entera.
3. **Pregunte usted de segundo, no de primero.** Si el docente pregunta primero, los compañeros se callan.
4. **Elija sus preguntas de la lista de cinco**, no improvise: así todos reciben el mismo trato y nadie se siente perseguido.
5. **Cierre cada turno con una sola frase suya** —un acierto y un ajuste—. No convierta cada turno en una minitutoría: hay más gente esperando.

---

#### 6️⃣ Cierre del curso (~8 min) — Protagonista: Docente
{slides_fase(label, "Qué hacer con esta propuesta después del curso", "Cierre del curso · últimos pendientes", cierre_deck(n))}

**GUION LITERAL:**
> “Antes de despedirnos, lo más importante que les voy a decir hoy: **el semestre termina, la propuesta no tiene por qué terminar con él**. Cuatro caminos reales, en orden de esfuerzo. Uno: **escriban el correo de cinco líneas**; ya tienen la entidad, el pedido y el pitch — es media hora de trabajo y es lo único que separa un documento de una respuesta real. Dos: **llévenla a la unidad de emprendimiento de la CUN o a un semillero**; es el cuadrante universitario, el más cercano y el que menos se usa. Tres: **conviértanla en opción de grado**: el problema ya está delimitado, hay evidencia y hay antecedentes, que es más de lo que tiene la mayoría al empezar. Cuatro: **úsenla en una entrevista de trabajo**, no como ‘un trabajo de la universidad’, sino como el caso donde ustedes detectaron un problema, lo validaron y decidieron con criterio.”

> “Antes de mostrarla afuera, actualicen dos cosas: **verifiquen la vigencia** de las entidades y convocatorias que citaron, porque cambian de un semestre a otro; y **ejecuten la prueba** si no alcanzaron a hacerla — un criterio cumplido cambia por completo el tramo 4 del pitch. Y una advertencia honesta: **nadie va a venir a preguntarles por su propuesta. La puerta se toca desde adentro.**”

> “Tres ideas para llevarse **del curso completo**. Una: la innovación **no es tener ideas**; es elegir un problema real y **defender una decisión con evidencia**. Dos: todo lo que no se puede **verificar** —un FODA, un criterio, una entidad— todavía no sirve para decidir. Tres: una propuesta que **no se conecta con el afuera** se queda en el archivo, por buena que sea.”

> “**Últimos pendientes de esta semana.** Diligenciar la **autoevaluación** y participar en la **coevaluación** dentro de su ventana en CDigital. Aplicar la **lista de ajustes** del taller a su documento y guardarlo en un sitio que no sea el escritorio del computador. Y revisar sus notas en el libro de calificaciones y **escribirme antes del cierre** si algo no cuadra: después del cierre ya no hay margen.”

> “**Cierre.** Cualquier duda administrativa, por el canal del curso. Gracias por el trabajo de todo el ciclo; fue un gusto acompañarlos.”

**Qué hacer:**
1. (3 min) Los cuatro caminos después del curso y las dos actualizaciones previas a mostrarla afuera.
2. (2 min) Las tres ideas del curso completo.
3. (3 min) Los tres pendientes de la semana y la despedida. **No** leer notas en voz alta ni comparar estudiantes.

---

🧩 **Actividad práctica / taller (resumen del producto de hoy)**

**Nombre:** Sustentación cruzada y consolidación — cierre de la Propuesta de Innovación.

1. Sustentación de 3 minutos: pitch de 60 s + dos preguntas + la frase de qué está listo y qué falta.
2. Devolución en pareja con las tres frases (me quedó claro / no me quedó claro / le sugiero).
3. Revisión de las **seis costuras** del documento.
4. **Criterio de éxito:** una **lista escrita de mínimo 3 ajustes** + la devolución de un compañero **anotada**, y que ese compañero pueda repetir su dolor, su valor y su pedido sin mirar el documento.
5. **Entregable: hoy NO se pide ningún archivo nuevo en CDigital.** La ACA Final ya cerró. Lo que sí queda en la plataforma es la **autoevaluación** (cuestionario) y la **coevaluación** (foro), que abren hoy.
6. **Trabajo autónomo de cierre:** aplicar la lista de ajustes al documento propio y guardarlo fuera del escritorio del computador.

---

✅ **Checklist del docente antes de clase**
- [ ] Leí el Fundamento Teórico completo (hoy conduzco una ronda, no dicto)
- [ ] Abrí `Clases/{label}/Presentacion.pptx`
- [ ] Tengo **cronómetro visible** y la lista de turnos armada de a dos
- [ ] Tengo a la mano **las cinco preguntas** para no improvisar y tratar a todos igual
- [ ] Anoté **los dos errores más repetidos** del grupo en la ACA Final, con un ejemplo anónimo para la devolución
- [ ] Verifiqué que el **foro del curso** esté abierto para quien no alcance a sustentar hoy
- [ ] **No** publiqué espacio de entrega nuevo: hoy no se entrega archivo
- [ ] Meet listo: {MEET}

---
*Fin del Guión — Sesión {n:02d}. Cierra el ciclo de encuentros del Syllabus EI004: sin contenido nuevo, sin entrega nueva y con la propuesta sostenida en voz alta.*
"""


# ---------------------------------------------------------------------------
# REGISTRO DE GUIONES — una función por sesión canónica, sin corrimiento
# ---------------------------------------------------------------------------
GUIONES = {
    1: guion_01,   # Encuadre
    2: guion_02,   # U3 · Design Thinking y técnicas
    3: guion_03,   # U4 · Gestión de la innovación (Manual de Oslo)
    4: guion_04,   # U5 · Tipos de innovación
    5: guion_05,   # U6+U7 · Validación y vigilancia tecnológica (sesión doble)
    6: guion_06,   # U8 · Ecosistema, entidades de apoyo y pitch
    7: guion_07,   # Cierre · consolidación y sustentación
}

# ── CORRIMIENTO RETIRADO (2026-08-11) ─────────────────────────────────────────
# Aquí vivían `BUILDERS_LEGACY` (guiones 1..8) + `CANON_TO_LEGACY = {1:1, 2:3, 3:4,
# 4:5, 5:6, 6:7, 7:8}` y un `_fix_session_numbers()` que renumeraba al vuelo las
# menciones «Sesión NN» y los nombres de entregable `SNN_…`.
#
# Por qué existió: el Syllabus EI004 tiene **8 unidades** y el periodo solo **7
# encuentros**. Cuando U1–U2 pasaron a lectura autónoma, en vez de reescribir los
# guiones se dejó el corrimiento fijo «canónica n → builder n+1» y un renumerado
# textual encima.
#
# Por qué se retira: tras el reorden del temario (U7 → S05, U8 → S06, S07 = cierre)
# el corrimiento **ya no describe nada real**. El builder que caía en la S05 dictaba
# solo validación (media sesión de las dos que hoy tiene), el de la S06 dictaba
# vigilancia —que hoy se dicta el 09/09— y el de la S07 dictaba el ecosistema, que
# hoy se dicta el 16/09. El renumerado disfrazaba el desajuste: cambiaba el número
# del encabezado y del entregable, y dejaba intactos los objetivos, el fundamento
# teórico y el plan minuto a minuto. Resultado: encabezado y tabla de slides nuevos
# sobre un parlamento viejo.
#
# Hoy cada `GUIONES[n]` se escribió **para la sesión n**: nombra su propio entregable
# (el mismo que muestra el deck), su propio tema y sus propias slides. No hay nada
# que renumerar y no debe volver a haberlo: si una sesión cambia de contenido, se
# reescribe su builder, no se le enchufa el de otra.
#
# El guion de la U2 (`guion_u2_inteligencia_emocional`) se conserva **fuera** del
# registro: es la única unidad del Syllabus sin sesión, y sin slides en el deck.
# Ver su docstring.


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
        builder = GUIONES.get(n)
        if builder is None:
            # `sesiones_cun.py` ganó una sesión y aquí no hay guion para ella: se avisa y no
            # se escribe nada. Antes esto reventaba con KeyError sobre el mapa de corrimiento.
            print(f"SIN GUION: sesión {n:02d} ({titulo}) — falta su builder en GUIONES")
            continue
        text_md = builder((n, label, titulo, detalle))
        _deck = deck_path(COURSES["creatividad"]["folder"], label)
        if n != 1:
            # Narración heredada de la plantilla de 7 slides: se retiran los números.
            # Las líneas «**Slides del deck:**» que escribe `slides_fase()` no caen aquí:
            # sus números salen del .pptx real y sí son correctos.
            text_md, _ = limpiar_referencias(text_md)
        else:
            # Mapa curado a mano: realinear contra el deck real («(cont.)» insertadas).
            text_md, _ = ajustar_mapa_manual(text_md, titulos_pptx(_deck))
        text_md = inject_shots(text_md, n)
        # Evaluación REAL del aula (quices, parciales, ACA Final, auto y coevaluación):
        # aviso, minutos reservados en el plan y checklist. Sale del modelo único.
        text_md = inyectar_evaluacion(text_md, "creatividad", n)
        if n == 1 and "Rompehielos" not in text_md:
            text_md = text_md.replace(
                "- **Meet (serie del curso):**",
                (
                    f"> **Rompehielos:** slide PRESÉNTATE de la Presentación del Curso. Con 50 "
                    f"matriculados no hay muro: se juega **«dos verdades y una mentira»** en "
                    f"**Slido** ({SLIDO} — el estudiante entra a slido.com con el código que el "
                    f"Docente pega en el chat del Meet). Las tres rondas y la mentira de cada "
                    f"una: `{RUNBOOK_SLIDO}`.\n\n- **Meet (serie del curso):**"
                ),
                1,
            )
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(text_md)
        print("MD", md_path)


if __name__ == "__main__":
    main()
