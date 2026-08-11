# -*- coding: utf-8 -*-
"""Regenera los 11 guiones docentes de Proyecto I (ESP329) a estándar locución.

Formato: solo .md (sin .docx).
Duración: ≈60 min contenido + 60 min tutoría.
Modelo de calidad: Creatividad Sesión 01.
Fuente curricular: ESP329 · Manual del Docente · sesiones_cun.py.
URLs AFI: desde sesiones_cun (cun.json → links_afi).

Evaluación: `guion_evaluacion.py` inyecta los ítems reales del aula — **Quiz** (25%, corte 1),
ACA 1 (25%, corte 2), ACA FINAL (42%) + auto y coevaluación —. El Quiz no cierra en día de
clase, así que se anuncia con guion literal en las sesiones que lo rodean en vez de reservarle
tiempo; sí se reservan minutos el día que abre la coevaluación.

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
    meet_url,
)
from cun_slides_engine import slido_url  # noqa: E402
from guion_evaluacion import (  # noqa: E402
    inyectar_evaluacion,
    items_corte_txt,
    peso_item,
)
from guion_slides import (  # noqa: E402
    NOTA_MOMENTOS,
    ajustar_mapa_manual,
    deck_path,
    limpiar_referencias,
    tabla_slides_md,
    titulos_pptx,
)

MEET = meet_url("proyecto1", "PROYECTO I")
COURSE = COURSES["proyecto1"]

# --- Rompehielos de la Sesión 01: juego en Slido, no muro ---------------------------
# ESP329 54ES4 tiene **50 matriculados** (roster de CDigital). Un Padlet de 50 notas no
# se lee entero en clase y cincuenta presentaciones habladas se comen el encuadre. Por eso
# el rompehielos deja de ser «preséntate» y pasa a ser un **juego con premio**: «dos
# verdades y una mentira» sobre el Docente, en **Slido**. Acertar es 1 entre 3 —azar puro—,
# así que quien nunca abre la cámara arranca igual que quien siempre habla, y de paso queda
# hecha la presentación del Docente sin diapositiva de biografía.
# Slido y no Mentimeter: el plan gratis (Basic) da 100 participantes por evento, 3 encuestas,
# 1 quiz con tabla de posiciones y Q&A ilimitado; Mentimeter corta en 50 participantes AL MES.
# La decisión no se escribe aquí: la deriva `cun_slides_engine.modo_rompehielos()` de la
# matrícula, y el enlace sale de la misma fuente que el del Meet (mientras el Docente no
# cree el evento, `slido_url` devuelve el marcador de posición). El estudiante no necesita
# esa URL: entra a slido.com con el **código** que el Docente pega en el chat del Meet.
SLIDO = slido_url("proyecto1")


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


RUNBOOK_SLIDO = runbook_slido("proyecto1")


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
    """Sesión 01 = ENCUADRE (no se dicta tema). Guion de presentación del curso.

    Cubre: el curso · el Docente · los estudiantes (juego de rompehielos en Slido) · la
    evaluación real del aula (Quiz del primer corte, ACA 1, ACA FINAL, auto y
    coevaluación). La unidad del programa que antes ocupaba esta sesión pasa a LECTURA
    AUTÓNOMA y se retoma al abrir la Sesión 02 (campo `unidad_diferida` en sesiones_cun.py).
    """
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    diferida = ses.get("unidad_diferida", "").split("→")[0].strip() or "la unidad de apertura del programa"
    # El juego ocupa 8 minutos exactos (antes el rompehielos tenía 9). El minuto que se
    # libera va a la fase de evaluación, que es la que siempre se queda corta: hay que
    # mostrar en pantalla el Quiz, el espacio de entrega y el enunciado de la ACA 1.
    fases = [
        ("1️⃣ Apertura y bienvenida", 5),
        ("2️⃣ Quién los acompaña: el Docente", 4),
        ("3️⃣ Rompehielos: «Dos verdades y una mentira» en Slido", 8),
        ("4️⃣ Recorrido del curso y su producto final", 10),
        ("5️⃣ Las ACAs y cómo se entrega", 13),
        ("6️⃣ Integridad académica y uso de IA", 8),
        ("7️⃣ Herramientas, cómo pedir ayuda y acuerdos", 7),
        ("8️⃣ Encargo autónomo y cierre del bloque", 5),
    ]
    md = f"""### GUIÓN DOCENTE — Sesión {n:02d}: {titulo}

> **Uso:** guion de locución de **esta** clase. Léalo en voz alta casi literal.
> **Esta sesión es de ENCUADRE: no se dicta tema.** El contenido curricular arranca en la Sesión 02.
> **Duración: ≈60 min de encuadre + 60 min de tutoría** (conformación de equipos y primeras dudas).
> **PPTX:** `Clases/{label}/Presentacion.pptx` — en cada fase se indica la slide de ESA presentación.

📌 **De esta sesión**
- **Sesión:** **{n:02d}** · **Tema:** {titulo}
- **Detalle:** {detalle}
- **PPTX estudiante:** `Clases/{label}/Presentacion.pptx`
- **Meet (serie del curso):** {MEET}

> ⚠️ **{diferida} pasa a LECTURA AUTÓNOMA.** Hoy no se dicta: se encarga como trabajo de la semana y se retoma al abrir la Sesión 02. Si un estudiante reclama "no vimos nada", muéstrele el encargo de la slide **Antes de la Sesión 02**.

🗺️ **Slides de esta presentación** (deck de encuadre — 21 slides)

| Slide | Título en el PPTX | Cuándo usarla |
| :---: | :--- | :--- |
| **1** | Portada — Sesión 01 | Apertura |
| **2** | AGENDA DE HOY | Apertura |
| **3** | Docente | Presentación del Docente |
| **4** | PRESÉNTATE — ROMPEHIELOS | Juego en Slido (dos verdades y una mentira) |
| **5** | LAS ACAs — QUÉ SE EVALÚA | Pesos de las entregas |
| **6** | Cómo trabajamos: el encuentro tiene dos mitades | Método del curso |
| **7–8** | Mapa del curso (11 encuentros) | Recorrido del curso |
| **9** | El producto del curso: qué archivo entregan al final | Producto final |
| **10** | Las tres ACAs en detalle | Qué se entrega y qué se evalúa |
| **11** | Cómo se entrega: paso a paso en CDigital | Procedimiento de entrega |
| **12** | Integridad académica: la línea que no se cruza | Plagio y debido proceso |
| **13** | IA generativa: se puede usar, con tres condiciones | Uso responsable de IA |
| **14** | Herramientas del curso | Solo gratis + navegador |
| **15** | Cómo pedir ayuda: canales, tutorías y tiempos | Tutorías y formulario |
| **16** | Acuerdos de convivencia del encuentro | Cámara, puntualidad, foro |
| **17** | Antes de la Sesión 02: lectura autónoma y qué traer | Encargo de la semana |
| **18** | Las preguntas que siempre salen el primer día | Dudas frecuentes |
| **19** | ACUERDOS DE TRABAJO | Cierre del encuadre |
| **20** | PARA LA PRÓXIMA SESIÓN | Trabajo autónomo |
| **21** | Cierre — Sesión 01 | Paso a tutoría |

🎯 **Objetivos de la sesión**
1. **Dejar claro** cómo funciona el curso: dos mitades del encuentro, avance escrito semanal y equipos de máximo 3.
2. **Mostrar** el mapa de los 11 encuentros y el producto final: un único anteproyecto que crece entrega tras entrega, y **romper el hielo jugando** —no con una ronda hablada que no cabe en un grupo de 50—, de modo que el grupo conozca al Docente y tres estudiantes se presenten habiéndose ganado el turno.
3. **Explicar** cómo se califica el curso en CDigital —**Quiz** (primer corte), **ACA 1** (segundo) y **ACA FINAL** con auto y coevaluación (tercero)—, el procedimiento de entrega y las reglas de integridad académica y uso de IA.
4. **Cerrar** con equipos tentativos conformados, canal de ayuda claro y el encargo de lectura autónoma para la Sesión 02.

---

🧰 **Qué debe tener listo el Docente ANTES de la clase** *(no hay fundamento teórico: hoy no se dicta tema)*

| Elemento | Estado en el que debe llegar | Por qué |
| :--- | :--- | :--- |
| **Aula en CDigital** | Abierta, con los tres espacios de entrega de ACA visibles | Los estudiantes van a preguntar dónde se sube; se muestra en pantalla, no se describe |
| **Carpeta `Clases/` en Drive** | Compartida con el grupo y con el material de esta sesión ya cargado | Es donde vive el material de clase (y la actividad, cuando una sesión sea autónoma). CDigital es para entregar y para las notas |
| **Evento de Slido** del curso | Creado y probado desde el celular, con el **quiz de 3 preguntas** montado (una por ronda), **una encuesta A/B/C** vacía para la ronda final y el **Q&A abierto**. El **código del evento** copiado para pegarlo en el chat | Es el rompehielos entero. Enlace del evento: {SLIDO} |
| **Las tres rondas, con la mentira ya marcada** | `{RUNBOOK_SLIDO}` diligenciado **antes** de entrar a la sala | Ahí están las frases y las casillas donde usted marca cuál es la mentira de cada ronda. Es material del Docente: **no** va en `Clases/`. Si llega a clase sin marcarlas, el juego se cae |
| **Libro de calificaciones del aula** | Abierto en otra pestaña | De ahí salen los nombres, tipos y pesos que se anuncian hoy. **El primer corte es un Quiz (cuestionario), no una entrega escrita**: hay que mostrarlo en pantalla |
| **Enunciados de las ACAs** | `Clases/Recursos/ACAs/` (ACA 1 y ACA FINAL) | Se proyecta el enunciado real, no un resumen |
| **Plantilla APA CUN** | `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` abierta en Google Docs | Se modela en vivo cómo se trabaja el documento del equipo |
| **Meet** | Iniciado 5 minutos antes, **grabación activada** y coanfitrión asignado | Se anuncia la grabación al abrir; sin grabación no hay evidencia de la sesión |
| **Deck de Sesión 01** | `Clases/{label}/Presentacion.pptx` en modo presentador | 21 slides: el guion las referencia por número |
| **Formulario de asistencia** | {LINK_TUTORIAS} copiado para el chat | Se pega apenas empieza la segunda hora |

**Decisiones que el Docente debe traer tomadas (no se improvisan en el aula):**
- Cómo nombrar los archivos de entrega (este guion usa `ACA1_Apellido1-Apellido2-Apellido3` para la ACA 1 y `ACAFinal_Apellido1-Apellido2-Apellido3` para la ACA FINAL).
- Franja tentativa para las tutorías por equipo de la semana, para poder proponerla al cierre.
- Qué hacer con quien llegue sin equipo: se anota su nombre y el Docente arma pareja/trío en la segunda hora.

> **Regla del día:** todo lo que hoy se afirma se muestra en pantalla. Nada de "eso lo buscan en la plataforma".

---

🧭 **Plan de Clase por Fases** — *encuadre ≈ 60 min*

{plan_tabla(fases)}

---

#### 1️⃣ Apertura y bienvenida (~5 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (AGENDA DE HOY)

**GUION LITERAL:**
> "Buenas noches y bienvenidos a **Proyecto I**. Antes de arrancar: la sesión **queda grabada** y la grabación se publica en CDigital, así que si alguien pierde un encuentro puede verlo después."

> "**Slide 1.** Esta primera sesión es distinta a todas las demás: **hoy no vemos tema**. Hoy usamos la hora en dejar clarísimo cómo funciona el curso, quién los acompaña, quiénes son ustedes y qué se les va a evaluar. El contenido del programa arranca la próxima sesión, y arranca en firme."

> "**Slide 2 — AGENDA.** Cinco cosas: el curso, el Docente, ustedes, **cómo se califica** y los acuerdos. La primera hora es esto. La segunda hora es tutoría: conformamos equipos y resolvemos dudas uno a uno."

**Qué hacer:** verificar audio y pantalla compartida (1 min) · confirmar grabación en voz alta (30 s) · recorrer la agenda señalando cada punto (3 min).

---

#### 2️⃣ Quién los acompaña: el Docente (~4 min) — Protagonista: Docente
**Slides:** 3 (Docente)

**GUION LITERAL:**
> "**Slide 3.** Un minuto sobre quién los va a acompañar. Mi perfil está ahí: ingeniería de sistemas, formación en inteligencia artificial y trabajo real en industria, no solo en aula."

> "Lo importante no es el título, es **el rol que juego en este curso**: yo no soy el experto del tema que cada equipo escoja. Soy el garante de que su documento se sostenga: que la pregunta, los objetivos, el marco y el método se hablen entre sí y que el trabajo sea viable en el tiempo que tienen."

> "Mi correo está en la slide. Úsenlo para lo que es de su equipo. Lo que le sirve a todo el curso, al foro de CDigital: así la respuesta le llega a todos."

**Qué hacer:** no leer la slide entera; contar en 30 segundos un proyecto real y aterrizar el rol de garante.

---

#### 3️⃣ Rompehielos: «Dos verdades y una mentira» en Slido (~8 min) — Protagonistas: Estudiantes
**Slides:** 4 (PRESÉNTATE — ROMPEHIELOS)

> ⚠️ **Antes de entrar a la sala.** Las **tres rondas** y **cuál es la mentira de cada una** están en
> `{RUNBOOK_SLIDO}` — material del Docente, no va en `Clases/`. **Márquelas ahí antes de la clase** y
> ajústelas a su vida: si las frases no son suyas, el juego no funciona. Aquí no se repiten a propósito:
> este guion se comparte y una mentira escrita en él deja de ser mentira.

> **Por qué un juego y no un muro:** el grupo tiene **50 matriculados**. Cincuenta notas en un tablero no
> se leen en clase y cincuenta presentaciones habladas se comen el encuadre entero. Acertar en «dos
> verdades y una mentira» es **1 entre 3**: azar puro, así que el que nunca abre la cámara arranca igual
> que el que siempre habla. Y mientras juegan, **usted queda presentado** — sin diapositiva de biografía.
> Va aquí, **antes de la primera tabla de porcentajes**: si lo primero que ven es una tabla de pesos, ya
> perdió la sala. Evento de Slido: {SLIDO}

**(1) GUION LITERAL — explicar el juego y anunciar el premio (~1 min):**
> "**Slide 4.** Antes de hablar de notas, de fechas y de porcentajes, ocho minutos de juego. Entren a **slido.com** —desde el celular o en otra pestaña— y escriban el **código** que acabo de pegar en el chat. No hay que instalar nada ni crear cuenta: se pone el código y ya están adentro. Y pongan su **nombre real**, porque con ese nombre se arma la tabla de posiciones."

> "El juego se llama **dos verdades y una mentira**, y va sobre mí. Son **tres rondas**. En cada una les muestro **tres frases mías** y **una es falsa**: ustedes votan cuál creen que es la mentira. Acertar es una entre tres, así que aquí no gana el que más sepa de investigación: gana el que me lea mejor. Empezamos todos empatados."

> "Y se juega por algo. Quien más veces me pille se gana una **revisión uno a uno conmigo**, media hora solo para su avance, **antes de la primera entrega** —la ACA 1—. No son décimas: es tiempo mío sobre su documento, que en este curso vale más."

**(2) GUION LITERAL — las tres rondas (~4 min, unos 80 segundos cada una):**
> "**Ronda uno.** Ahí están las tres frases. Una de estas tres **no** es cierta: ¿cuál? Tienen veinte segundos… y voten, que el que no vota no puntúa."

> [Cierre la pregunta, proyecte el reparto de votos y **revele la mentira**.] "La mentira era la número [X]. Lo curioso es lo otro: la que a más gente le costó creer **sí es verdad**." [Cuente en **treinta segundos** la historia de la verdad más rara de la ronda. Ese es el minuto en que usted se presenta de verdad.]

> "**Ronda dos.** Mismas reglas, otras tres frases…" [Vote → revele → historia de treinta segundos.]

> "**Ronda tres**, la última mía…" [Vote → revele → historia de treinta segundos.]

> **Regla de oro de esta fase:** revele la mentira **después de cada ronda**, no al final, y cuente la historia. La gracia del juego es la revelación; y la historia es la presentación del Docente. Pero **cronometre**: treinta segundos por historia, no tres minutos. Tres rondas caben en cuatro minutos solo si usted se contiene.

**(3) GUION LITERAL — tabla de posiciones (~1 min):**
> "Veamos quién me leyó mejor." [Proyecte la **tabla de posiciones** de Slido.] "Podio: [nombre 1], [nombre 2] y [nombre 3]. Aplauso en el chat para los tres… y ojo, que todavía no se ha jugado el premio."

**(4) GUION LITERAL — la ronda final, la del podio (~2 min):**
> "Ahora se invierte el juego: **los tres del podio se presentan jugando**. Cada uno abre el micrófono treinta segundos y nos dice **sus** dos verdades y una mentira sobre sí mismo: de dónde viene, en qué trabaja, lo que quiera. El resto del curso vota en la encuesta que tengo abierta —**A, B o C**— y **gana el que engañe a más gente**."

> [Lance la **encuesta A/B/C** una vez por cada persona del podio; anuncie en voz alta cuántos cayeron con cada una.]

> "Ganó [nombre]: nos engañó a [n] de nosotros. Esa revisión uno a uno es suya — le escribo hoy para agendarla. Y fíjense en lo que acaba de pasar: ya conocen a tres compañeros, y hablaron porque se lo ganaron, no porque yo los nombrara."

**Cómo conducirlo (con 50, esto es lo que decide si funciona):**
1. **Pegue el código en el chat y dígalo en voz alta**, y vuelva a pegarlo al empezar la ronda uno: el chat del primer día entierra el primer mensaje. El QR de la slide es la ayuda, no el camino principal: la mitad del grupo está en computador.
2. **No espere a que entren los cincuenta.** Arranque cuando vea moverse el contador de participantes; el que llega tarde entra en la ronda dos y no pasa nada — el juego no es la nota.
3. **Ocho minutos son ocho minutos.** Si una ronda se estira, la que se recorta es su historia, nunca la revelación.
4. **Empate en el podio:** deje a los cuatro. Un turno de treinta segundos de más se recupera; discutir un desempate en vivo, no.
5. **Si alguien del podio no quiere hablar:** no insista ni un segundo. "Pasamos al siguiente" y sigue el cuarto de la tabla. Obligar a hablar el primer día es exactamente lo que este juego vino a evitar.
6. **Todo el encuentro:** deje el **Q&A de Slido** abierto y anúncielo. Con cincuenta personas el chat del Meet se vuelve ilegible; el Q&A ordena por votos y al cierre usted responde las más votadas.

**Cierre de la fase — y el diagnóstico que antes hacía el formulario:**
> "Última cosa antes de seguir, y esta sí me sirve a mí: en el **Q&A de Slido** escriban una línea con su **tema tentativo** de investigación —una idea cruda basta, hoy nadie tiene el tema definitivo—. Lo pueden hacer mientras avanzo con lo demás; queda abierto toda la sesión y yo lo leo hoy mismo. El que todavía no tiene equipo, tranquilo: en la segunda hora lo empato con esos temas en pantalla."

**Después de clase:** exporte el **Q&A** y la lista de participantes del evento. De ahí salen los equipos de quien llegó solo, los ejemplos de las próximas sesiones y la lista de quién no se conectó. Y deje el evento **abierto 48 horas**, con el enlace publicado en el aula: quien no estuvo juega igual —fuera de la tabla de posiciones, que sería injusto con quien sí llegó— y llega a la Sesión 02 sabiendo quién le da clase.

---

#### 4️⃣ Recorrido del curso y su producto final (~10 min) — Protagonista: Docente
**Slides:** 6 (Cómo trabajamos) → 7–8 (Mapa del curso) → 9 (El producto del curso)

**GUION LITERAL:**
> "**Slide 6.** Cómo trabajamos. El encuentro tiene dos mitades: **primera hora**, contenido, yo explico y modelo un ejemplo; **segunda hora**, tutoría, ustedes trabajan y yo paso por los equipos. Eso significa que la segunda hora **solo le sirve a quien trae algo escrito**. Aquí se corrige lo que ya existe; no venimos a empezar de cero en pantalla."

> "Los equipos son de **máximo tres personas** y se mantienen todo el curso. Sube un solo integrante, pero la nota es del equipo. ¿Se puede trabajar solo? Sí, y la carga es exactamente la misma. Decídanlo esta semana."

> "**Slides 7 y 8 — el mapa completo.** Son once encuentros. Hoy, encuadre. De la 02 a la 03, problema, pregunta y objetivos. De la 04 a la 07, todo el marco referencial: antecedentes, teórico, conceptual, contextual y citación; **todo eso junto es lo que se entrega en la ACA 1**, la del segundo corte. De la 08 a la 10, la metodología y la integración: eso es la **ACA FINAL**. La 11 cierra con coevaluación y autoevaluación."

> "Y falta la pieza que casi nadie ve venir: el **primer corte no es un documento, es un Quiz** —un cuestionario en CDigital que vale el **{peso_item('proyecto1', 'quiz')} del curso** y que **cierra antes de la Sesión 03**—. Ya está abierto. Lo repito porque es el error más caro de este curso: la primera nota no se gana entregando un archivo, se gana entrando al aula y respondiendo ese cuestionario."

> "Fíjense en algo: **cada sesión alimenta una entrega**. No hay clases decorativas. Si falta a una sesión, no perdió una charla: perdió un pedazo de su propio documento."

> "**Slide 9 — qué se llevan al final.** Un solo archivo: **el anteproyecto**. No son trabajos distintos, es el mismo documento que crece: lo que entregan en la **ACA 1** es su primera mitad, y la **ACA FINAL** es ese documento completo, no algo nuevo escrito la última semana. Va en la **plantilla APA CUN**, desde hoy, y les sirve después como punto de partida de **Proyecto II** y como base de lo que sustentarán al cerrar el programa."

> "Y la frontera del curso, que repito ahora y voy a repetir todo el semestre: en **Proyecto I los instrumentos se proponen, nunca se aplican**. Aquí se diseña la encuesta; aplicarla es Proyecto II."

**Qué hacer:** abrir la plantilla APA en Google Docs y mostrarla 30 segundos en pantalla · señalar en el mapa dónde cae cada ACA.

---

#### 5️⃣ Las ACAs y cómo se entrega (~12 min) — Protagonista: Docente
**Slides:** 5 (LAS ACAs — QUÉ SE EVALÚA) → 10 (Las tres ACAs en detalle) → 11 (Cómo se entrega)

**GUION LITERAL:**
> "**Slide 5.** Estos son los pesos, y los nombres que van a ver en el aula son estos: **{items_corte_txt('proyecto1', 1)}** en el primer corte, **{items_corte_txt('proyecto1', 2)}** en el segundo y **{items_corte_txt('proyecto1', 3)}** en el tercero. Retengan dos cosas: la **ACA FINAL es, por lejos, la que más pesa**, y no es un trabajo nuevo —es todo lo anterior corregido e integrado—; y el **primer corte se juega en un cuestionario**, no en un documento."

> "Esa es la sorpresa que quiero quitarles hoy: el **Quiz** ya está **abierto** en CDigital y **cierra antes de la Sesión 03**. Vale {peso_item('proyecto1', 'quiz')}, o sea el primer corte completo. Entren esta semana, mírenlo y resuélvanlo con tiempo: no hay reapertura por olvido."

> "**Slide 10 — qué se entrega y qué separa un buen trabajo de uno flojo.** La **ACA 1** recoge dos bloques: la formulación —problema, pregunta, objetivos, justificación, alcances y limitaciones— y el marco referencial con sus antecedentes, mínimo seis, nacionales e internacionales. Un buen entregable permite señalar **a quién le duele algo y dónde** y **usa** cada fuente para responder a su pregunta; uno flojo describe una tecnología de moda, nunca dice a quién le sirve y pega resúmenes que no se hablan entre sí. La **ACA FINAL** es el anteproyecto integrado: un buen entregable se lee de portada a referencias sin contradecirse; uno flojo son tres capítulos escritos por tres personas con tres preguntas distintas."

> "Y el **Quiz** del primer corte no es un documento: es un cuestionario individual, con tiempo, sobre lo que trabajemos en las primeras sesiones. Se responde en la plataforma, y cuando terminen deben ver el mensaje de **enviado**: un intento abierto y sin enviar cuenta como no presentado."

> "Las **fechas exactas y los criterios completos** no los voy a dictar: están en cada ítem de CDigital y en el enunciado, en `Clases/Recursos/ACAs/`. Ábranlos hoy mismo. — [proyectar en pantalla el **Quiz** dentro del aula y el enunciado de la **ACA 1**]"

> "**Slide 11 — cómo se entrega, paso a paso.** Uno: trabajan la plantilla APA en **Google Docs**, un documento por equipo, con permiso de edición para todos. Dos: antes de entregar, **descargan en PDF**. Tres: nombran el archivo `ACA1_Apellido1-Apellido2-Apellido3`. Cuatro: **un solo integrante** lo sube en CDigital y los demás verifican que quedó cargado. Cinco: la portada lleva los **nombres completos de todos**; si falta uno, esa persona no tiene nota."

> "Y la regla que evita el 90% de los problemas: **lo que no está en CDigital, no está entregado.** No recibo entregas por correo ni por WhatsApp. Si algo pasa, se avisa **antes** del cierre, no al día siguiente."

**Qué hacer:** mostrar en vivo, en CDigital, **el Quiz del primer corte** y el espacio de entrega de la **ACA 1** · preguntar en voz alta "¿alguien no ve el Quiz en su aula?" y esperar respuesta: si alguien no lo ve, es un problema de matrícula o de grupo que hay que resolver esta misma semana.

---

#### 6️⃣ Integridad académica y uso de IA (~8 min) — Protagonista: Docente
**Slides:** 12 (Integridad académica) → 13 (IA generativa)

**GUION LITERAL:**
> "**Slide 12.** Esto lo digo el primer día para no tener que decirlo cuando ya no haya cómo arreglarlo. **Plagio es tomar lo ajeno y no decirlo**: pegar texto sin comillas ni cita, traducir un párrafo ajeno y firmarlo, reusar un trabajo propio de otro semestre como si fuera nuevo, o entregar el documento de otro equipo con la portada cambiada."

> "Citar en **APA 7** no debilita el trabajo: lo sostiene. Una idea que no es suya y no está citada es un problema; esa misma idea citada es un argumento con respaldo. Y si se detecta plagio, **hay debido proceso**: no depende de mi ánimo, es un procedimiento institucional con notificación y descargos. Por eso: pregunten antes de improvisar."

> "**Slide 13 — la inteligencia artificial generativa.** En este curso **no está prohibida**. Estaría fuera de lugar prohibirla en una especialización en IA. Pero se usa con tres condiciones."

> "**Primera: declararla.** Una nota al final del documento: qué herramienta usaron y para qué. **Segunda: verificar todo.** Los modelos **inventan referencias** que parecen perfectas: autor creíble, año creíble, enlace que no existe. Citar una fuente inexistente no es un error de formato, es una fuente falsa en un trabajo académico. **Tercera: la autoría es suya.** Si no pueden explicar en voz alta un párrafo de su propio anteproyecto, ese párrafo todavía no es suyo, y en sustentación se nota en diez segundos."

**Qué hacer:** si hay tiempo, pedirle a la IA una referencia sobre el tema del curso y verificarla en Scholar en vivo. Treinta segundos de demostración valen más que cinco minutos de advertencia.

---

#### 7️⃣ Herramientas, cómo pedir ayuda y acuerdos (~7 min) — Protagonista: Docente
**Slides:** 14 (Herramientas) → 15 (Cómo pedir ayuda) → 16 (Acuerdos de convivencia) → 19 (ACUERDOS DE TRABAJO)

**GUION LITERAL:**
> "**Slide 14.** Todo lo que usamos es **gratis y desde el navegador**: CDigital para entregar, Google Docs para escribir, Scholar, SciELO y Redalyc para buscar, ZoteroBib para generar las referencias en APA sin instalar nada, Excalidraw para dibujar, el **Drive de clases** donde les dejo el material de cada sesión, y Meet. Súmenle la biblioteca virtual de la CUN con su usuario institucional. Si una herramienta les pide pagar para continuar, no es la que estamos usando: pregúntenme antes de sacar la tarjeta."

> "**Slide 15 — cómo pedir ayuda.** Tres canales. El primero y más rápido: la **segunda hora de cada encuentro**. El segundo: **tutorías por equipo**, que se piden y se agendan durante la semana; no hay atención espontánea sin cita, así que escríbanme diciendo qué necesitan y qué tienen escrito, y la acordamos. El tercero: el **foro de CDigital**, para lo que le sirve a todo el curso; respondo en días hábiles."

> "Y algo obligatorio: **cada estudiante que asiste a tutoría registra su asistencia** en este formulario — lo pego en el chat: {LINK_TUTORIAS}. Es **su** evidencia de acompañamiento ante el programa. Sin registro, la tutoría no consta en ningún lado."

> "**Slide 16 — acuerdos de convivencia.** Empezamos a la hora en punto. Cámara encendida al menos cuando se presenten y en la tutoría de su equipo: revisar un avance a ciegas no funciona. Micrófono en silencio mientras alguien expone, y el chat abierto para preguntar cuando quieran. En el foro se critica el documento, nunca a la persona."

> "**Slide 19 — los acuerdos que resumen todo:** se entrega en CDigital; se trae avance escrito a cada encuentro; se cita en APA 7; y las tutorías por equipo se agendan en la semana."

**Qué hacer:** pegar en el chat, en este orden, el enlace del formulario de asistencia y el del aula en CDigital.

---

#### 8️⃣ Encargo autónomo y cierre del bloque (~5 min) — Protagonista: Docente
**Slides:** 17 (Antes de la Sesión 02) → 18 (Preguntas del primer día) → 20 (PARA LA PRÓXIMA SESIÓN) → 21 (Cierre)

**GUION LITERAL:**
> "**Slide 17 — lo que hay que hacer antes de la próxima sesión.** Escuchen bien esta parte, porque es la única tarea de hoy y es la que define cómo arranca la Sesión 02."

> "**Uno: lectura autónoma.** {diferida}. Está en la carpeta de esta sesión, en el **Drive de clases** —el enlace les llega en el correo de bienvenida—. Hoy no la dictamos, la leen ustedes y **la retomamos al abrir la Sesión 02**. Mientras leen, anoten **tres términos** que no les queden claros: con esos tres arrancamos la próxima clase, así que tráiganlos escritos."

> "**Dos:** confirmen su equipo, máximo tres personas. **Tres:** entren al aula, **abran el Quiz del primer corte** para ver cuántas preguntas tiene y cuánto tiempo da, y lean completo el enunciado de la **ACA 1**. **Cuatro:** creen el documento del equipo en Google Docs con la plantilla APA y compártanlo con todos. **Cinco:** traigan una idea de tema **en una frase** y el contexto donde ocurre: una empresa, un aula, un proceso concreto."

> "**Slide 18.** Y estas son las preguntas que siempre salen el primer día; las respondo ahora para que nadie se quede con la duda… [recorrer las tres cajas]. ¿Alguna otra antes de pasar a tutoría?"

> "**Slides 20 y 21.** Resumen en tres frases: uno, el curso entero se llama **anteproyecto** y es un solo archivo que crece; dos, cada sesión alimenta una entrega y se trae avance escrito; tres, se entrega en CDigital y se cita en APA 7. **Nos quedamos para la segunda hora: tutoría.**"

---

📣 **Si un estudiante pregunta… | Usted responde…** *(dudas reales del primer día)*

| Si un estudiante pregunta… | Usted responde… |
| :--- | :--- |
| "¿Esta materia se pierde fácil?" | "No se pierde por difícil: se pierde por entregar tarde o por subir un documento que nadie leyó antes. Quien trae avance cada semana llega al cierre del curso con el anteproyecto prácticamente listo." |
| "¿Puedo trabajar solo?" | "Sí, pero la carga es la misma para uno que para tres y el equipo es de máximo tres. Decídalo esta semana: una vez avanzada la ACA 1 no conviene cambiar de equipo ni de tema." |
| "¿El Quiz también es en equipo?" | "No. El **Quiz es individual**, igual que la autoevaluación y la coevaluación. En equipo se entregan la **ACA 1** y la **ACA FINAL**." |
| "¿Sirve un trabajo de otro semestre?" | "Como punto de partida sí, si usted lo declara y lo reformula para este curso. Entregarlo tal cual como si fuera nuevo también es plagio y entra en el mismo debido proceso." |
| "¿La clase se graba?" | "Sí, el encuentro completo, y la grabación queda en CDigital. Si falta a una sesión puede verla, pero la tutoría de su equipo no se recupera con un video." |
| "¿Ya puedo aplicar mi encuesta?" | "En Proyecto I no. Aquí se **propone** el instrumento; aplicarlo es Proyecto II, con aval previo. Si aplica algo ahora, no cuenta y le desordena el anteproyecto." |
| "¿Puedo usar ChatGPT para escribir?" | "Puede usarlo, con tres condiciones: lo declara al final del documento, verifica cada fuente en el original y responde por lo que entrega. Si no puede explicar un párrafo suyo, reescríbalo." |
| "¿Y si todavía no tengo tema?" | "Es lo normal el primer día. Traiga a la Sesión 02 un contexto que conozca —su trabajo, su área, un proceso— y de ahí sacamos el tema entre los dos." |
| "¿Dónde subo la entrega?" | "Solo en CDigital, en el espacio de esa ACA. Se lo muestro ahora en pantalla. Correo y WhatsApp no son canal de entrega." |

---

#### 9️⃣ Tutoría / conformación de equipos (~60 min) — Protagonistas: Estudiantes + Docente
**Sin slides nuevas** (queda abierta la deck de Sesión 01 o el aula de CDigital en pantalla).

> **Acuerdo:** {MSG_TUTORIAS_POR_GRUPO} Esta 2.ª hora del encuentro es el bloque de tutoría en vivo; las tutorías adicionales por equipo se agendan durante la semana. En cada una, el estudiante registra su asistencia en el formulario.

**GUION LITERAL (apertura de la tutoría):**
> "Segunda hora: **tutoría**. Hoy no hay avances que revisar, así que la usamos en tres cosas: cerrar equipos, resolver dudas de plataforma y dejar agendada la primera tutoría por equipo. Cada persona que se quede diligencia su asistencia aquí: {LINK_TUTORIAS} — lo dejo en el chat."

**Rutina de esta primera tutoría:**
1. **Equipos (≈20 min).** Quien ya tenga equipo lo escribe en el chat: nombres completos, máximo tres. A quien esté solo, el Docente lo empareja con el **Q&A de Slido** proyectado —ahí quedaron los temas tentativos que pidió al cerrar el rompehielos—: con 50 personas, emparejar de memoria no funciona; emparejar leyendo los temas en pantalla, sí.
2. **Plataforma (≈15 min).** Con pantalla compartida: dónde está el material, **dónde está el Quiz del primer corte** —que ya corre—, dónde el espacio de entrega de la ACA 1, dónde la plantilla APA y cómo se comparte el documento del equipo en Google Docs.
3. **Temas tentativos (≈15 min).** Dos o tres equipos leen su idea en una frase. El Docente devuelve **una sola** pregunta a cada uno: ¿quién tiene ese problema y dónde ocurre? No se corrige la idea todavía: eso es Sesión 02.
4. **Agenda (≈10 min).** Se propone la franja de tutorías de la semana y cada equipo indica su disponibilidad. Se cierra con un acuerdo observable por equipo: llegar a la Sesión 02 con la frase de tema y el contexto escritos.

**Cierre de la tutoría (2 min):**
> "Grabación completa. Yo registro la sesión en mi formulario docente dentro de las próximas 24 horas. Ustedes, si aún no lo han hecho, cierren su formulario de asistencia. Si necesitan una revisión por equipo antes del próximo encuentro, la acordamos por el canal del curso. Nos vemos en la Sesión 02: ahí sí arranca el contenido."

---

🧩 **Resultado esperado al terminar el encuentro**
1. Equipos tentativos conformados (máximo 3) y registrados en el chat o en CDigital.
2. Cada estudiante sabe dónde se entrega, con qué plantilla y con qué nombre de archivo.
3. El encargo autónomo quedó claro: **{diferida}** leída para la Sesión 02, más la frase de tema y su contexto.
4. El juego jugado, el podio presentado y el ganador con su revisión uno a uno agendada; los temas tentativos escritos en el **Q&A de Slido** y leídos el mismo día.

✅ **Checklist antes de clase**
- [ ] Aula de CDigital abierta, con los espacios de entrega de ACA visibles
- [ ] Material de esta sesión cargado en `Clases/{label}/` del **Drive de clases**, y la carpeta compartida con el grupo
- [ ] **Las tres rondas ajustadas y la mentira de cada una marcada** en `{RUNBOOK_SLIDO}` *(material del Docente — sin esto el juego no se puede jugar)*
- [ ] **Evento de Slido** creado y probado desde el celular, con el **quiz de 3 preguntas**, la **encuesta A/B/C** de la ronda final y el **Q&A abierto**; el **código** copiado para el chat: {SLIDO}
- [ ] Decidido el **premio** y cómo se agenda la revisión uno a uno del ganador
- [ ] **Libro de calificaciones** del aula abierto (Quiz · ACA 1 · ACA FINAL · auto · coevaluación) y los enunciados de ACA en `Clases/Recursos/ACAs/`
- [ ] Plantilla APA CUN abierta en Google Docs para mostrarla en vivo
- [ ] PPTX `Clases/{label}/Presentacion.pptx` en modo presentador (21 slides)
- [ ] Link del formulario de asistencia listo para el chat: {LINK_TUTORIAS}
- [ ] Meet iniciado con **grabación activada**: {MEET}
{post_clase()}
---
*Fin del Guión — Sesión 01 (encuadre). No se dicta tema: el contenido arranca en la Sesión 02.*
"""
    # Mapa de slides curado a mano: se realinea contra el deck real por si el motor
    # partió algún bloque en «(cont.)» y corrió la numeración de la narración.
    md, _ = ajustar_mapa_manual(
        md, titulos_pptx(deck_path(COURSES["proyecto1"]["folder"], label))
    )
    # Evaluación real del aula. En la S01 solo entra el aviso (es encuadre: no se le
    # inserta fase ni se le toca el plan), y ese aviso es justo el que faltaba: el
    # **Quiz** del primer corte ya está abierto y cierra antes de la Sesión 03.
    return inyectar_evaluacion(md, "proyecto1", n)


def _slides_map(label: str) -> str:
    """Tabla de slides del deck REAL (no la plantilla fija de 7)."""
    tabla = tabla_slides_md(titulos_pptx(deck_path(COURSES["proyecto1"]["folder"], label)))
    if not tabla:
        return slides_table_std()
    return f"{tabla}\n{NOTA_MOMENTOS}\n"


def _body(n, titulo, detalle, label, objetivos, fundamento, fases_plan, fases_texto, taller_foco, entregable, tutoria_foco):
    md = f"""### GUIÓN DOCENTE — Sesión {n:02d}: {titulo}

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

{_slides_map(label)}
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
- [ ] Material de la sesión en `Clases/{label}/` (**Drive de clases**) y plantilla APA lista en Google Docs · CDigital queda para la entrega y las notas
- [ ] Link tutorías para chat: {LINK_TUTORIAS}
- [ ] Meet: {MEET}
{post_clase()}
---
*Fin del Guión — Sesión {n:02d}. Autocontenido para dictar 60+60.*
"""
    # La narración de estas sesiones venía de la plantilla de 7 slides: sus números no
    # corresponden al deck real (17–19 slides). Se retiran; queda el nombre del momento.
    md, _ = limpiar_referencias(md)
    # Evaluación real del aula: aviso de lo que corre en esta sesión (el Quiz del primer
    # corte, la ACA 1, la ACA FINAL, auto y coevaluación) + checklist. En Proyecto I
    # ningún cuestionario cierra en día de clase, así que no se reserva tiempo salvo el
    # bloque de auto/coevaluación de la última sesión.
    return inyectar_evaluacion(md, "proyecto1", n)


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

#### 4. Coherencia como hilo (primer bloque de la ACA 1)
Al terminar esta unidad, el bloque de formulación debe leerse como una sola historia sin saltos: problema → pregunta → objetivo general → específicos → justificación → alcances/limitaciones. Ese hilo es la **primera mitad de la ACA 1** (la entrega del segundo corte) y es lo que el Docente revisa en la retroalimentación de la Sesión 04. Ojo con no confundir instrumentos: la nota del **primer corte** no sale de este texto, sale del **Quiz** (cuestionario en CDigital) que cierra antes de la Sesión 03.

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
> “**Slide 2.** Hoy cerramos el bloque de formulación: **objetivos, justificación, alcances y limitaciones**. Cuando salgan de la primera hora tendrán escrita la **primera mitad de la ACA 1**, que es la entrega del segundo corte.”

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
> “**Slide 6.** En autónomo, empaqueten el bloque completo de formulación —problema, pregunta, objetivos, justificación, alcances y limitaciones, con sus referencias en APA 7— siguiendo las indicaciones de CDigital. Suban el avance de clase como `S03_ObjetivosJustificacion_Apellidos`.”
> “**Slide 7.** Dos recordatorios de plataforma antes de la tutoría. Uno: esto que acaban de escribir **no es una tarea suelta**, es la primera mitad de la **ACA 1** del segundo corte, el mismo documento que va a seguir creciendo. Dos: la nota del **primer corte** es el **Quiz**, y ese cuestionario **ya cerró o está por cerrar**; si alguien no lo ha presentado, revísenlo ahora mismo en el aula, no mañana. Pasamos a tutoría para revisar la coherencia pregunta–objetivos equipo por equipo.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Redactar** objetivo general y específicos coherentes con la pregunta.
2. **Argumentar** justificación y delimitar alcances/limitaciones.
3. **Integrar** el bloque de formulación del anteproyecto.""",
        fundamento, fases_plan, fases_texto, "objetivos",
        """1. Sección objetivos + justificación + alcances/limitaciones en CDigital.
2. **Éxito:** específicos con verbo preciso y alineados a la pregunta.""",
        "coherencia pregunta–objetivos; cerrar el bloque de formulación (primera mitad de la ACA 1) y verificar equipo por equipo que el Quiz del primer corte quedó presentado.",
    )


def guion_04(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Cómo retroalimentar el bloque de formulación (en 60+60)
Priorice dos cosas: **coherencia** (¿pregunta ↔ objetivos ↔ justificación cuentan la misma historia?) y **viabilidad**. No reescriba el texto del estudiante ni corrija comas: señale dos o tres hallazgos accionables por equipo, redactados como instrucción concreta (“delimite el actor”, “el específico 2 no responde la pregunta”). La retro es un mapa de ruta, no una calificación disfrazada — y aquí, literalmente, no hay nota que devolver: la formulación es **avance** de la ACA 1, que cierra en el segundo corte.

#### 1.b Lo que sí tiene nota en esta sesión: el Quiz del primer corte
El **Quiz** (cuestionario en CDigital) ya cerró y su nota debe quedar registrada en el libro de calificaciones dentro de este corte. Dedique dos o tres minutos a una **devolución de grupo** —los dos errores más repetidos, sin nombres y sin leer notas en voz alta— y deje claro que el cuestionario no se reabre. Si algún equipo confunde «entregué el avance» con «presenté el Quiz», corríjalo hoy: son dos instrumentos distintos.

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
        ("1️⃣ Encuadre + retro del bloque de formulación y del Quiz", 10),
        ("2️⃣ Qué es un antecedente (y qué no)", 12),
        ("3️⃣ Modelación de ficha de antecedente", 10),
        ("4️⃣ Taller de búsqueda y fichas", 20),
        ("5️⃣ Cierre", 8),
    ]
    fases_texto = f"""#### 1️⃣ Encuadre + retro del bloque de formulación y del Quiz (~10 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 04**. Dos cosas antes del tema. Primera: **ya cerró el Quiz del primer corte**; les devuelvo en dos minutos los errores que más se repitieron, sin nombres, y la nota queda en el libro de calificaciones del aula. Segunda: leí su bloque de formulación y les explico con qué criterios lo leí, porque eso es la **primera mitad de la ACA 1** y esas correcciones no son opcionales.”
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
> “**Slide 6.** En autónomo, completen las seis fichas mínimas y, en paralelo, vayan aplicando sobre el documento las correcciones que les devolví de la formulación. Suban el avance como `S04_Antecedentes_Apellidos`.”
> “**Slide 7.** Recuerden cómo se acumula esto: los antecedentes y el marco se suman a la formulación corregida **dentro de la misma ACA 1**, la del segundo corte. No es una entrega nueva: es el mismo archivo, más grande y mejor. Pasamos a tutoría para revisar una o dos fichas por equipo.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Aplicar** criterios de retroalimentación al bloque de formulación.
2. **Elaborar** fichas de antecedentes (ruta a mín. 6).
3. **Usar** bases abiertas y citación APA vía ZoteroBib/Docs.""",
        fundamento, fases_plan, fases_texto, "antecedentes",
        """1. Avance de fichas de antecedentes en CDigital.
2. **Éxito:** cada ficha incluye vínculo explícito a la pregunta.""",
        "retro puntual del bloque de formulación (avance de la ACA 1) + revisar 1–2 fichas de antecedentes por equipo; confirmar que todos presentaron el Quiz.",
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
> “**Slide 7.** Recuerden que todo esto acumula hacia la **ACA 1**, la entrega del segundo corte. Pasamos a tutoría: revisamos el mapa de cada equipo y cortamos la teoría ornamental.”
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
Esta sesión cierra el marco referencial completo —antecedentes, teórico, conceptual, contextual y legal, con referencias limpias— que junto con la formulación corregida compone la **ACA 1**, la entrega del segundo corte. La meta mínima: cero citas huérfanas en el avance.

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
> “Buenas tardes, **Sesión 07**. Hoy cerramos el marco referencial completo, que es el corazón de la **ACA 1** —la entrega del segundo corte, y cierra pronto—. Dos frentes: el **marco legal** —si su proyecto lo necesita— y una **clínica de APA 7** para dejar las citas impecables.”
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
> “**Slide 6.** Con esto queda listo el marco referencial completo de la **ACA 1**: antecedentes, teórico, conceptual, contextual y legal, con referencias limpias. En autónomo, integren las correcciones, dejen cero citas huérfanas y **suban el documento a la tarea de la ACA 1 en CDigital**: cierra antes de nuestro próximo encuentro, así que no lo dejen para el último día.”
> “**Slide 7.** La próxima sesión damos un salto: empezamos el **diseño metodológico** —paradigma, enfoque y alcance— para adelantar antes de los festivos del tramo final, que es cuando se arma la **ACA FINAL**. Pasamos a tutoría para revisar APA y pertinencia legal equipo por equipo.”
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
Esta sesión anticipa la metodología antes de las semanas más cargadas del tramo de la **ACA FINAL**, que por los festivos tienen solo dos lunes sincrónicos. Adelantar hoy da colchón para las tutorías extra de esas semanas.

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
> “Buenas tardes, **Sesión 08**. Cerramos el marco referencial —que ya quedó entregado en la **ACA 1**— y hoy damos el salto al **diseño metodológico**. Adelantamos a propósito, porque las semanas de la **ACA FINAL** tienen menos lunes por los festivos.”
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
    fundamento = f"""#### 1. La clase abre con la devolución de la ACA 1 (20 min, no 5)
La **ACA 1** (tarea grupal del segundo corte) ya está calificada y esta es la primera sesión después de su cierre. Se devuelven **tres cosas, no una**: la nota en el libro de calificaciones, los **comentarios por criterio de la rúbrica** y el **documento comentado**. Que el equipo los abra HOY, en pantalla y con usted delante, es la única garantía de que los lea a tiempo: el que los deja para después los abre en la semana de la **ACA FINAL**, cuando ya no hay margen para rehacer el marco.

Va primero por una razón operativa, no ceremonial: lo que se bosqueja en la segunda mitad de hoy —población, muestra, instrumento— **cuelga de los objetivos**. Si una corrección va a mover un objetivo, hay que moverlo ANTES de redactar ítems; si no, el equipo escribe un instrumento alineado a un objetivo que va a cambiar.

#### 2. Cómo se devuelve una rúbrica (y qué es «trazabilidad»)
Cada comentario es una **instrucción accionable** —“delimite el actor”, “este objetivo no responde la pregunta”, “esta afirmación necesita fuente”—, no una nota disfrazada. Recorra la rúbrica **en el orden en que lista sus criterios**, diga en cada uno qué se miró y qué se corrige, y hágalo **sin nombres y sin leer notas en voz alta**; el detalle por equipo va en la segunda hora.

El criterio literal de la ACA FINAL es «**correcciones de la ACA 1 incorporadas**», y se demuestra con **trazabilidad visible**: bitácora al final del documento (comentario recibido · qué se cambió · en qué sección quedó), historial de Google Docs y comentarios marcados como resueltos solo cuando el texto ya cambió. Una corrección que se decide NO aplicar también se declara y se sustenta: eso también es trazabilidad, no un descuido.

#### 3. Reparto de tiempos de hoy (léalo antes de entrar)
La devolución se lleva los **primeros 20 minutos** y el taller, otros 20: quedan **16 minutos** para toda la exposición. El deck de hoy es **denso a propósito** —tipos de muestreo, tamaño de muestra, ítems modelados, ética y datos— y buena parte es **material de consulta** que el estudiante relee en autónomo y que usted retoma caso por caso en la tutoría. En vivo narre solo la espina: unidad de análisis → población y muestra delimitadas → criterios de inclusión/exclusión → técnica vs. instrumento → matriz de alineación. Lo demás se nombra y se deja señalado.

#### 4. Población y muestra (propuestas)
La **población** es el conjunto total de unidades de estudio (personas, procesos, documentos) que interesan; la **muestra** es el subconjunto que efectivamente se estudiaría, con sus **criterios de inclusión y exclusión** y su forma de selección (probabilística o no). En Proyecto I se DEFINE quiénes serían y cómo se elegirían —no se contacta a nadie para recolectar—.

#### 5. Técnicas e instrumentos **propuestos**
La **técnica** es el procedimiento (encuesta, entrevista, observación, análisis de logs/documentos); el **instrumento** es la herramienta concreta (el cuestionario, la guía de entrevista, la rúbrica). Cada instrumento propuesto debe declarar: propósito, estructura (bloques o ítems tipo), validez tentativa (cómo se validaría) y plan de análisis. Todo en condicional: se PROPONE, no se aplica.

#### 6. Alineación con los objetivos
Cada bloque del instrumento debe colgar de un objetivo específico o de una categoría/variable. Si un ítem no responde a ningún objetivo, sobra; si un objetivo no tiene ítems que lo alimenten, falta instrumento.

#### 7. Recordatorio institucional
La slide RECUERDA y el Manual son claros: en Proyecto I los instrumentos son PROPUESTOS. En la tutoría, el estudiante diligencia su formulario de asistencia: {LINK_TUTORIAS}.

#### 8. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Pide que le “suban” la nota de la ACA 1 | “La nota se sustenta en la rúbrica. Lo que sí sube es la ACA FINAL, si las correcciones se ven.” |
| Dice que no ha visto los comentarios | “Ábralos ahora, en pantalla. La ACA FINAL exige que estén incorporados y con trazabilidad.” |
| Su equipo no entregó la ACA 1 | “La devolución igual le aplica: esas secciones vuelven a pedirse, integradas, en la ACA FINAL.” |
| Ya envió un formulario ‘de prueba’ a gente | “Eso no es avance de Proyecto I, es riesgo. Retírelo: hoy PROPONEMOS.” |
| Confunde población con muestra | “Población = el total; muestra = a quiénes estudiaría. ¿Cuál es cuál en su caso?” |
| Ítems que no responden a ningún objetivo | “¿A qué objetivo alimenta este ítem? Si a ninguno, quítelo.” |
| No define criterios de inclusión | “¿Quién SÍ entra y quién NO? Sin criterios, la muestra es un deseo.” |
| Redacta el instrumento en pasado (‘apliqué’) | “En condicional: ‘se aplicaría’. En Proyecto I se propone.” |
"""
    # Reparto: el deck abre con tres slides de devolución de la ACA 1 rotuladas «Primeros
    # 20 minutos», y la slide de taller dice «(20 minutos)». Esos dos bloques son fijos y
    # se llevan 40 de los 60 min de contenido: la exposición se recorta a 16 (8 + 8) y el
    # cierre a 4. El §3 del fundamento le dice al Docente qué narra en vivo y qué queda
    # como material de consulta.
    fases_plan = [
        ("1️⃣ Encuadre + devolución de la ACA 1", 20),
        ("2️⃣ Regla de oro P-I + población, muestra y muestreo", 8),
        ("3️⃣ Técnica, instrumento y alineación a objetivos", 8),
        ("4️⃣ Taller: bosquejo de instrumento", 20),
        ("5️⃣ Cierre", 4),
    ]
    fases_texto = """#### 1️⃣ Encuadre + devolución de la ACA 1 (~20 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (Primeros 20 minutos: la devolución de la ACA 1) → 3 (Cómo se lee la rúbrica, criterio por criterio) → 4 (Qué hacer con las correcciones antes de la ACA FINAL)

**GUION LITERAL:**
> “Buenas tardes, **Sesión 09**. Los primeros veinte minutos de hoy son para la **devolución de la ACA 1**: ya está calificada en CDigital. Y les devuelvo tres cosas, no una: la **nota** en el libro de calificaciones, los **comentarios por criterio de la rúbrica** y el **documento comentado**. Ábranlos ahora, en pantalla, mientras hablo. El equipo que no los abre hoy los abre en la semana de la ACA FINAL, cuando ya no hay tiempo de rehacer el marco.”
> “Un aviso de lectura: mis comentarios **no son una nota disfrazada**. Cada uno es una instrucción concreta —‘delimite el actor’, ‘este objetivo no responde la pregunta’, ‘esta afirmación necesita fuente’—. Léanlos como mapa de trabajo, no como regaño.”
> “Ahora la **rúbrica, criterio por criterio**, en el orden de la tabla. **Coherencia problema–pregunta–objetivos:** miré que los tres cuenten la misma historia; se corrige el objetivo específico que no responde la pregunta, uno a la vez. **Pertinencia:** que el problema sea de IA aplicada y no un tema suelto, y que la línea del programa quede dicha explícitamente. **Justificación:** vacío, beneficiario y aporte; no opinión personal. **Alcances y limitaciones:** que no prometan lo que es Proyecto II. **Antecedentes:** mínimo seis, nacionales e internacionales, cada ficha cerrando con ‘esto le aporta a mi pregunta porque…’. **Marco teórico, conceptual y contextual:** amarrado a las variables de la pregunta, no un listado. **Escritura e integridad:** citar o borrar la afirmación sin fuente. **APA 7:** que la cita en texto y la lista final se correspondan en los dos sentidos.”
> “Voy criterio por criterio sin nombres y sin leer notas en voz alta. El detalle de su caso lo vemos en la segunda hora.”
> “Y esto es lo que hacen con las correcciones: la **ACA FINAL no es un documento nuevo**, es este mismo documento corregido más metodología, cronograma y viabilidad. El criterio dice, literal, ‘correcciones de la ACA 1 incorporadas’, y eso se demuestra con **trazabilidad**: una bitácora al final —comentario recibido, qué se cambió, en qué sección quedó—, el historial de Google Docs, y comentarios marcados como resueltos solo cuando el texto ya cambió. Si deciden NO aplicar una corrección, díganlo y susténtenlo: eso también cuenta.”
> “Corrijan en este orden, porque cada nivel arrastra al siguiente: primero coherencia pregunta–objetivos; después justificación, alcances y limitaciones; luego antecedentes y marco; al final, forma y APA 7. Y si su equipo no alcanzó a entregar la ACA 1, esto igual le aplica: esas secciones son parte del anteproyecto y la ACA FINAL las vuelve a pedir, ya integradas.”
> “Por qué les devuelvo esto ANTES del tema de hoy y no al final: lo que van a bosquejar en la segunda parte —población, muestra, instrumento— cuelga de sus objetivos. Si una corrección les va a mover un objetivo, muévanlo **antes** de escribir ítems. Las dudas sobre un comentario se resuelven hoy o en la tutoría de la semana, nunca en la víspera de la entrega.”

#### 2️⃣ Regla de oro P-I + población, muestra y muestreo (~8 min) — Protagonista: Docente
**Slides:** 5 (La regla de oro de hoy) → 6 (Unidad de análisis) → 7 (Población, muestra y muestreo) → 8 (Inclusión y exclusión) → 9 (Tipos de muestreo) → 10 (Tamaño de la muestra)

**GUION LITERAL:**
> “Cerrada la devolución, sigo con la regla de oro de hoy, porque es la que más se rompe: si alguien ya mandó un Google Form ‘de prueba’ a cuarenta personas, eso NO es avance de Proyecto I, es un riesgo —recolectó datos personales sin aval ni consentimiento—. Hoy PROPONEMOS instrumentos; no aplicamos. Esa frontera no tiene excepciones.”
> “Antes de la muestra, la pregunta que casi nadie se hace: **¿qué voy a estudiar, uno por uno?** Esa es la **unidad de análisis**, y en proyectos de IA no siempre es una persona: puede ser un registro, un documento o un evento del sistema. Definirla mal tuerce la muestra, el instrumento y el análisis.”
> “Con eso claro: la **población** es el total de unidades que me interesan, **delimitada** por lugar y periodo; la **muestra** es el subconjunto que efectivamente estudiaría; y necesita criterios —quién SÍ entra, quién NO— verificables por un tercero. El **muestreo** es el procedimiento para elegirla: el no probabilístico no está prohibido, está permitido si se declara y se reconoce su límite. Lo que no se acepta es esconderlo.”
> “El tamaño se justifica, no se inventa: fórmula con sus parámetros si es cuantitativa, saturación con un rango si es cualitativa, periodo y cobertura si son registros. Las tablas de tipos de muestreo y de tamaño quedan en el deck para que las relean en autónomo; en tutoría las miramos caso por caso.”

#### 3️⃣ Técnica, instrumento y alineación a objetivos (~8 min) — Protagonista: Docente
**Slides:** 11 (Técnica e instrumento no son sinónimos) → 12 (De la técnica al instrumento) → 13 (Las cuatro declaraciones) → 14 (Matriz de alineación) → 15 (Ejemplo modelado) → 16 (Ética y datos) → 18 (Paso a paso en Google Docs)

**GUION LITERAL:**
> “La **técnica** es el procedimiento —encuestar, entrevistar, observar, analizar documentos—; el **instrumento** es la herramienta concreta que ustedes construyen y adjuntan: el cuestionario, la guía, la matriz. La técnica es ‘tomar una fotografía’; el instrumento es la cámara con sus ajustes. Escribir ‘se aplicará una encuesta’ no es un instrumento propuesto: no hay nada que revisar ni que validar.”
> “Todo instrumento propuesto declara **cuatro cosas**: propósito —a qué objetivo específico responde—, estructura —bloques, número de ítems, escala—, validación tentativa —juicio de expertos y prueba piloto, en condicional— y plan de análisis. Sin las cuatro está incompleto, aunque tenga cincuenta preguntas.”
> “Y la alineación de oro, que es la **matriz**: cada bloque cuelga de un objetivo. La regla va en dos direcciones: **ítem sin objetivo, se elimina; objetivo sin ítems, falta instrumento**. En el deck les dejo ítems modelados de los dos tipos, el paso a paso en Google Docs y las cajas de **ética** —consentimiento, anonimización, menores, aval institucional—: se redactan ahora aunque se usen en Proyecto II. Y recuerden diligenciar su formulario de asistencia cuando estén en tutoría.”

#### 4️⃣ Taller: bosquejo de instrumento (~20 min) — Protagonista: Estudiantes
**Slides:** 19 (TALLER · Bosquejo de instrumento)

**GUION LITERAL:**
> “Veinte minutos. Primero, población y muestra delimitadas —quiénes, dónde, en qué periodo— con sus criterios de inclusión y exclusión, y el tipo de muestreo propuesto. Después bosquejen el instrumento: si es cuestionario, entre diez y quince ítems; si es guía de entrevista, ocho preguntas abiertas. Al lado de cada bloque, a qué objetivo responde. Cierren con un párrafo de plan de análisis. Todo en condicional. Yo circulo. Suban como `S09_InstrumentosPropuestos_Apellidos`.”
> “Criterio de éxito, y lo reviso equipo por equipo: **ningún ítem sin objetivo y ningún objetivo sin ítems**.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Ya aplicó el instrumento | “Retírelo: en Proyecto I se propone. Aplicar es Proyecto II.” |
| Confunde población y muestra | “Población = total; muestra = a quiénes estudia. Sepárelas.” |
| Tiene ítems sueltos | “¿A qué objetivo responde este ítem? Si a ninguno, fuera.” |
| No define inclusión/exclusión | “¿Quién entra y quién no? Escriba los criterios.” |
| Aún no abrió la retro de la ACA 1 | “Ábrala ya: si una corrección mueve un objetivo, se mueve antes de los ítems.” |

#### 5️⃣ Cierre (~4 min) — Protagonista: Docente
**Slides:** 20 (Checklist de autoevaluación) → 21 (Trabajo autónomo y qué viene después) → 22 (Cierre)

**GUION LITERAL:**
> “En autónomo, dos frentes. Uno: terminen los ítems y redacten el consentimiento informado propuesto; dejen explícito, por escrito, que el instrumento es una PROPUESTA para Proyecto II. Dos: **abran hoy mismo la bitácora de correcciones de la ACA 1** —comentario, qué se cambió, en qué sección quedó—. Repasen el checklist antes de darlo por cerrado y suban `S09_InstrumentosPropuestos_Apellidos`.”
> “La próxima sesión integramos todo: cronograma, viabilidad y el ensamble del anteproyecto para la **ACA FINAL**; traigan el documento completo en un solo archivo, no fragmentos. Pasamos a tutoría: resuelvo dudas de los comentarios de la ACA 1, reviso instrumentos y freno cualquier aplicación prematura.”
"""
    return _body(
        n, titulo, detalle, label,
        """1. **Interpretar** la devolución de la ACA 1 y planear sus correcciones con trazabilidad.
2. **Definir** población/muestra propuestas.
3. **Bosquejar** instrumentos sin aplicarlos.
4. **Alinear** ítems/preguntas a objetivos/categorías.""",
        fundamento, fases_plan, fases_texto, "instrumentos",
        """1. Sección población/muestra + bosquejo de instrumento en CDigital.
2. Bitácora de correcciones de la ACA 1 abierta (comentario · qué se cambió · dónde quedó).
3. **Éxito:** queda explícito que es propuesta para P-II y ningún ítem queda sin objetivo.""",
        "resolver dudas de los comentarios de la ACA 1; revisar instrumentos y frenar cualquier aplicación prematura.",
    )


def guion_10(ses):
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    fundamento = """#### 1. Planeación y viabilidad
La **planeación** es el cronograma realista de fases hasta Proyecto II (con recursos y, si el formato lo pide, presupuesto). La **viabilidad** es la pregunta honesta: ¿de verdad se puede? ¿Hay acceso a la población? ¿Hay permisos? ¿Alcanza el tiempo? Viabilidad no es optimismo: un cronograma que promete encuestar a 500 personas en una semana NO es viable, es un deseo.

#### 2. Integración del anteproyecto
La **ACA FINAL** exige el documento **completo e integrado**, no un fragmento nuevo pegado al final. “Integrar” significa que la formulación corregida, el marco referencial, el método y la planeación se lean como UN solo texto coherente, con las correcciones de la **ACA 1** ya incorporadas.

#### 3. Checklist de coherencia final (previo a S11)
El hilo completo debe cerrar sin saltos: pregunta ↔ objetivos ↔ marco ↔ método ↔ instrumento propuesto ↔ cronograma. Cualquier eslabón que no conecte es un “gap” que hay que registrar y asignar a un responsable del equipo.

#### 4. Errores frecuentes / preguntas trampa
| El estudiante… | Usted responde… |
| :--- | :--- |
| Cronograma irreal (todo en una semana) | “¿Eso se puede de verdad? Ajústelo a tiempos y accesos reales.” |
| Pega la ACA FINAL como fragmento nuevo | “La ACA FINAL es el documento COMPLETO integrado, no un anexo suelto.” |
| No incorporó las correcciones previas | “Las correcciones de la ACA 1 no son opcionales; el producto es acumulativo.” |
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
> “Buenas tardes, **Sesión 10**. Ya tienen todas las piezas sueltas; hoy las miramos como un SISTEMA. Trabajamos planeación, viabilidad e integración del anteproyecto de cara a la **ACA FINAL**, que es el producto de cierre y la entrega que más pesa del curso.”
> “**Slide 2.** Meta de hoy: construir un cronograma y una viabilidad realistas, integrar el documento completo y detectar los ‘gaps’ de coherencia antes del cierre.”

#### 2️⃣ Cronograma y viabilidad (~14 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “**Slide 3.** La planeación es el cronograma realista de las fases hasta Proyecto II. La viabilidad es la pregunta honesta: ¿de verdad se puede? Si su cronograma promete encuestar a quinientas personas en una semana, eso no es un plan, es un deseo.”
> “Piensen en tres frentes de viabilidad: acceso —¿los dejarán entrar a esa población?—, permisos —¿hay avales pendientes?— y tiempo. Un anteproyecto viable es más valioso que uno ambicioso e imposible.”

#### 3️⃣ Integración del documento (~12 min) — Protagonista: Docente
**Slides:** 4 (RECUERDA)

**GUION LITERAL:**
> “**Slide 4.** La **ACA FINAL** NO es un fragmento nuevo que se pega al final: es el documento COMPLETO e integrado. Integrar significa que la formulación corregida, el marco, el método y la planeación se lean como un solo texto, con las correcciones de la ACA 1 ya metidas.”
> “Recuerden que el producto es acumulativo: si no incorporaron mis correcciones anteriores, el documento no está integrado, está remendado. Hoy detectamos esos remiendos.”

#### 4️⃣ Taller: matriz de coherencia + gaps (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL:**
> “**Slide 5.** Veinte minutos. Armen una matriz de coherencia en Google Docs: filas = las secciones del anteproyecto; columnas = ¿existe?, ¿está alineada con la pregunta?, ¿qué falta? Marquen cada casilla y hagan una lista de ‘gaps’ con un responsable por cada uno. Yo circulo. Suban como `S10_IntegracionViabilidad_Apellidos`.”

| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Cronograma irreal | “Ajústelo a accesos y tiempos reales; menos es más.” |
| Pega la ACA FINAL como anexo | “Es el documento completo integrado, no un fragmento.” |
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
Es la lectura de cierre del anteproyecto con tres preguntas: ¿el documento cuenta UNA sola historia de principio a fin?, ¿el APA está estable (sin citas huérfanas)?, ¿queda clarísimo que los instrumentos son PROPUESTOS y no aplicados? Si las tres respuestas son sí, el anteproyecto está listo para la **ACA FINAL**.

#### 2. Coevaluación y autoevaluación (ESP329)
Son componentes individuales de cierre (**coevaluación**, un **foro**, y **autoevaluación**, un **cuestionario**; los pesos exactos están en el libro de calificaciones y las ventanas, en la Presentación del Curso y en CDigital). En clase se practica una coevaluación **formativa** con una rúbrica breve —entrena el ojo crítico—, pero esa práctica NO sustituye la actividad oficial que cada estudiante diligencia en Moodle en su ventana.

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
> “Tres preguntas de oro para la integración: ¿el documento cuenta una sola historia?, ¿el APA está estable sin citas huérfanas?, ¿queda clarísimo que los instrumentos son PROPUESTOS? Si las tres dan sí, están listos para la **ACA FINAL**.”

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
> “**Slide 6.** No olviden las ventanas de **coevaluación** y **autoevaluación** en CDigital —el detalle logístico está en la Presentación del Curso—: la coevaluación es un **foro** en el que hay que escribir y la autoevaluación un **cuestionario**; cada una es individual y vale su porcentaje del tercer corte. En autónomo, pulido final del anteproyecto para la **ACA FINAL**.”
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
