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
    meet_url,
)
from cun_slides_engine import PADLET_PRESENTACION_URL  # noqa: E402
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

    Cubre: el curso · el Docente · los estudiantes (Padlet) · las ACAs. La unidad
    del programa que antes ocupaba esta sesión pasa a LECTURA AUTÓNOMA y se retoma
    al abrir la Sesión 02 (campo `unidad_diferida` en sesiones_cun.py).
    """
    n, titulo, detalle = ses["n"], ses["titulo"], ses["detalle"]
    label = label_for(n, titulo)
    diferida = ses.get("unidad_diferida", "").split("→")[0].strip() or "la unidad de apertura del programa"
    fases = [
        ("1️⃣ Apertura y bienvenida", 5),
        ("2️⃣ Quién los acompaña: el Docente", 4),
        ("3️⃣ Rompehielos en Padlet: preséntense", 9),
        ("4️⃣ Recorrido del curso y su producto final", 10),
        ("5️⃣ Las ACAs y cómo se entrega", 12),
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
| **4** | PRESÉNTATE — ROMPEHIELOS | Padlet |
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
2. **Mostrar** el mapa de los 11 encuentros y el producto final: un único anteproyecto que crece entrega tras entrega.
3. **Explicar** las tres ACAs, el procedimiento de entrega en CDigital y las reglas de integridad académica y uso de IA.
4. **Cerrar** con equipos tentativos conformados, canal de ayuda claro y el encargo de lectura autónoma para la Sesión 02.

---

🧰 **Qué debe tener listo el Docente ANTES de la clase** *(no hay fundamento teórico: hoy no se dicta tema)*

| Elemento | Estado en el que debe llegar | Por qué |
| :--- | :--- | :--- |
| **Aula en CDigital** | Abierta, con el material de la sesión publicado y los tres espacios de entrega de ACA visibles | Los estudiantes van a preguntar dónde se sube; se muestra en pantalla, no se describe |
| **Padlet del rompehielos** | Abierto en una pestaña y con el enlace copiado para pegar en el chat | El QR falla en celulares viejos; el enlace debe estar listo en 3 segundos |
| **Enunciados de las ACAs** | Los tres abiertos desde `Clases/Recursos/ACAs/` | Se proyecta el enunciado real de la ACA 1, no un resumen |
| **Plantilla APA CUN** | `Clases/Recursos/Plantilla_APA_CUN_Proyecto de grado.docx` abierta en Google Docs | Se modela en vivo cómo se trabaja el documento del equipo |
| **Meet** | Iniciado 5 minutos antes, **grabación activada** y coanfitrión asignado | Se anuncia la grabación al abrir; sin grabación no hay evidencia de la sesión |
| **Deck de Sesión 01** | `Clases/{label}/Presentacion.pptx` en modo presentador | 21 slides: el guion las referencia por número |
| **Formulario de asistencia** | {LINK_TUTORIAS} copiado para el chat | Se pega apenas empieza la segunda hora |

**Decisiones que el Docente debe traer tomadas (no se improvisan en el aula):**
- Cómo nombrar los archivos de entrega (este guion usa `ACA1_Apellido1-Apellido2-Apellido3`).
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

> "**Slide 2 — AGENDA.** Cinco cosas: el curso, el Docente, ustedes, las ACAs y los acuerdos. La primera hora es esto. La segunda hora es tutoría: conformamos equipos y resolvemos dudas uno a uno."

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

#### 3️⃣ Rompehielos en Padlet: preséntense (~9 min) — Protagonistas: Estudiantes
**Slides:** 4 (PRESÉNTATE — ROMPEHIELOS)

**GUION LITERAL:**
> "**Slide 4.** Turno de ustedes. Escaneen el QR o abran el enlace que acabo de pegar en el chat: {PADLET_PRESENTACION_URL}"

> "Un post-it por persona, tres líneas, no más: **(1)** su nombre y a qué se dedica hoy; **(2)** qué espera del curso; **(3)** un **tema tentativo** de investigación, aunque sea una idea cruda de una sola frase. No tiene que estar bien: hoy nadie tiene el tema definitivo. Tienen **6 minutos** y el Padlet queda abierto toda la semana."

**Cómo conducirlo (esto es lo que decide si el rompehielos funciona):**
1. El Docente escribe **el primero**, con su propio post-it, mientras habla. Un tablero vacío no lo llena nadie.
2. Pegar el enlace en el chat **antes** de mostrar el QR: siempre hay alguien conectado desde el computador.
3. A los 2 minutos, leer en voz alta el primer post-it que aparezca y celebrarlo: "listo, ya tenemos el primero".
4. A los 4 minutos, leer **tres o cuatro** notas en voz alta, nombrando a la persona y devolviéndole algo concreto.

> **Si a los 3 minutos nadie escribe** — no repetir la consigna, cambiar de estrategia:
> "Veo el tablero quieto, así que vamos por otra vía: voy a nombrar a tres personas y me responden por micrófono, y yo les escribo el post-it desde acá. [Nombre], ¿a qué se dedica y qué le gustaría investigar? … Perfecto, lo dejo escrito."
> Con dos o tres respuestas habladas el tablero se destraba solo. Si aun así no se mueve, se sigue adelante: **el rompehielos no puede consumir más de 9 minutos**; el enlace queda abierto y se retoma en la tutoría.

**Cierre de la fase:**
> "Guarden ese tema tentativo: en la Sesión 02 lo convertimos en un problema y en una pregunta de investigación."

---

#### 4️⃣ Recorrido del curso y su producto final (~10 min) — Protagonista: Docente
**Slides:** 6 (Cómo trabajamos) → 7–8 (Mapa del curso) → 9 (El producto del curso)

**GUION LITERAL:**
> "**Slide 6.** Cómo trabajamos. El encuentro tiene dos mitades: **primera hora**, contenido, yo explico y modelo un ejemplo; **segunda hora**, tutoría, ustedes trabajan y yo paso por los equipos. Eso significa que la segunda hora **solo le sirve a quien trae algo escrito**. Aquí se corrige lo que ya existe; no venimos a empezar de cero en pantalla."

> "Los equipos son de **máximo tres personas** y se mantienen todo el curso. Sube un solo integrante, pero la nota es del equipo. ¿Se puede trabajar solo? Sí, y la carga es exactamente la misma. Decídanlo esta semana."

> "**Slides 7 y 8 — el mapa completo.** Son once encuentros. Hoy, encuadre. De la 02 a la 03, problema, pregunta y objetivos: eso es la ACA 1. De la 04 a la 07, todo el marco referencial: antecedentes, teórico, conceptual, contextual y citación: eso es la ACA 2. De la 08 a la 10, la metodología y la integración: eso es la ACA 3. La 11 cierra con coevaluación y autoevaluación."

> "Fíjense en algo: **cada sesión alimenta una entrega**. No hay clases decorativas. Si falta a una sesión, no perdió una charla: perdió un pedazo de su propio documento."

> "**Slide 9 — qué se llevan al final.** Un solo archivo: **el anteproyecto**. No son tres trabajos distintos, es el mismo documento que crece. La ACA 3 es ese documento completo, no algo nuevo escrito la última semana. Va en la **plantilla APA CUN**, desde hoy, y les sirve después como punto de partida de **Proyecto II** y como base de lo que sustentarán al cerrar el programa."

> "Y la frontera del curso, que repito ahora y voy a repetir todo el semestre: en **Proyecto I los instrumentos se proponen, nunca se aplican**. Aquí se diseña la encuesta; aplicarla es Proyecto II."

**Qué hacer:** abrir la plantilla APA en Google Docs y mostrarla 30 segundos en pantalla · señalar en el mapa dónde cae cada ACA.

---

#### 5️⃣ Las ACAs y cómo se entrega (~12 min) — Protagonista: Docente
**Slides:** 5 (LAS ACAs — QUÉ SE EVALÚA) → 10 (Las tres ACAs en detalle) → 11 (Cómo se entrega)

**GUION LITERAL:**
> "**Slide 5.** Estos son los pesos. No los memoricen: lo que importa es que **la última entrega es, por lejos, la que más pesa de las tres**, y que no es un trabajo nuevo: es todo lo anterior corregido e integrado. Quien haga bien las dos primeras ya tiene medio camino de la tercera."

> "**Slide 10 — qué se entrega en cada una y qué separa un buen trabajo de uno flojo.** ACA 1: problema, pregunta, objetivos, justificación, alcances y limitaciones. Un buen entregable permite señalar **a quién le duele algo y dónde**; uno flojo describe una tecnología de moda y nunca dice a quién le sirve. ACA 2: antecedentes —mínimo seis, nacionales e internacionales— y todo el marco. Un buen entregable **usa** cada fuente para responder a su pregunta; uno flojo pega resúmenes que no se hablan entre sí. ACA 3: el anteproyecto integrado. Un buen entregable se lee de portada a referencias sin contradecirse; uno flojo son tres capítulos escritos por tres personas con tres preguntas distintas."

> "Las **fechas exactas y los criterios completos** no los voy a dictar: están en el enunciado de cada ACA, en `Clases/Recursos/ACAs/` y en CDigital. Ábranlos hoy mismo. — [proyectar el enunciado de la ACA 1 en pantalla]"

> "**Slide 11 — cómo se entrega, paso a paso.** Uno: trabajan la plantilla APA en **Google Docs**, un documento por equipo, con permiso de edición para todos. Dos: antes de entregar, **descargan en PDF**. Tres: nombran el archivo `ACA1_Apellido1-Apellido2-Apellido3`. Cuatro: **un solo integrante** lo sube en CDigital y los demás verifican que quedó cargado. Cinco: la portada lleva los **nombres completos de todos**; si falta uno, esa persona no tiene nota."

> "Y la regla que evita el 90% de los problemas: **lo que no está en CDigital, no está entregado.** No recibo entregas por correo ni por WhatsApp. Si algo pasa, se avisa **antes** del cierre, no al día siguiente."

**Qué hacer:** mostrar en vivo el espacio de entrega de la ACA 1 en CDigital · preguntar en voz alta "¿alguien no ve el espacio de entrega?" y esperar respuesta.

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
> "**Slide 14.** Todo lo que usamos es **gratis y desde el navegador**: CDigital para entregar, Google Docs para escribir, Scholar, SciELO y Redalyc para buscar, ZoteroBib para generar las referencias en APA sin instalar nada, Excalidraw para dibujar, Padlet y Meet. Súmenle la biblioteca virtual de la CUN con su usuario institucional. Si una herramienta les pide pagar para continuar, no es la que estamos usando: pregúntenme antes de sacar la tarjeta."

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

> "**Uno: lectura autónoma.** {diferida}. Está publicada en CDigital. Hoy no la dictamos, la leen ustedes y **la retomamos al abrir la Sesión 02**. Mientras leen, anoten **tres términos** que no les queden claros: con esos tres arrancamos la próxima clase, así que tráiganlos escritos."

> "**Dos:** confirmen su equipo, máximo tres personas. **Tres:** abran y lean completo el enunciado de la ACA 1. **Cuatro:** creen el documento del equipo en Google Docs con la plantilla APA y compártanlo con todos. **Cinco:** traigan una idea de tema **en una frase** y el contexto donde ocurre: una empresa, un aula, un proceso concreto."

> "**Slide 18.** Y estas son las preguntas que siempre salen el primer día; las respondo ahora para que nadie se quede con la duda… [recorrer las tres cajas]. ¿Alguna otra antes de pasar a tutoría?"

> "**Slides 20 y 21.** Resumen en tres frases: uno, el curso entero se llama **anteproyecto** y es un solo archivo que crece; dos, cada sesión alimenta una entrega y se trae avance escrito; tres, se entrega en CDigital y se cita en APA 7. **Nos quedamos para la segunda hora: tutoría.**"

---

📣 **Si un estudiante pregunta… | Usted responde…** *(dudas reales del primer día)*

| Si un estudiante pregunta… | Usted responde… |
| :--- | :--- |
| "¿Esta materia se pierde fácil?" | "No se pierde por difícil: se pierde por entregar tarde o por subir un documento que nadie leyó antes. Quien trae avance cada semana llega al cierre del curso con el anteproyecto prácticamente listo." |
| "¿Puedo trabajar solo?" | "Sí, pero la carga es la misma para uno que para tres y el equipo es de máximo tres. Decídalo esta semana: después de la ACA 1 no conviene cambiar de equipo ni de tema." |
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
1. **Equipos (≈20 min).** Quien ya tenga equipo lo escribe en el chat: nombres completos, máximo tres. A quien esté solo, el Docente lo empareja según el tema tentativo que dejó en el Padlet.
2. **Plataforma (≈15 min).** Con pantalla compartida: dónde está el material, dónde el espacio de entrega de la ACA 1, dónde la plantilla APA y cómo se comparte el documento del equipo en Google Docs.
3. **Temas tentativos (≈15 min).** Dos o tres equipos leen su idea en una frase. El Docente devuelve **una sola** pregunta a cada uno: ¿quién tiene ese problema y dónde ocurre? No se corrige la idea todavía: eso es Sesión 02.
4. **Agenda (≈10 min).** Se propone la franja de tutorías de la semana y cada equipo indica su disponibilidad. Se cierra con un acuerdo observable por equipo: llegar a la Sesión 02 con la frase de tema y el contexto escritos.

**Cierre de la tutoría (2 min):**
> "Grabación completa. Yo registro la sesión en mi formulario docente dentro de las próximas 24 horas. Ustedes, si aún no lo han hecho, cierren su formulario de asistencia. Si necesitan una revisión por equipo antes del próximo encuentro, la acordamos por el canal del curso. Nos vemos en la Sesión 02: ahí sí arranca el contenido."

---

🧩 **Resultado esperado al terminar el encuentro**
1. Equipos tentativos conformados (máximo 3) y registrados en el chat o en CDigital.
2. Cada estudiante sabe dónde se entrega, con qué plantilla y con qué nombre de archivo.
3. El encargo autónomo quedó claro: **{diferida}** leída para la Sesión 02, más la frase de tema y su contexto.
4. Rompehielos del Padlet con post-its de la mayoría del grupo (queda abierto toda la semana).

✅ **Checklist antes de clase**
- [ ] Aula de CDigital abierta, con material publicado y espacios de entrega de ACA visibles
- [ ] Padlet abierto y enlace copiado para el chat: {PADLET_PRESENTACION_URL}
- [ ] Los tres enunciados de ACA abiertos desde `Clases/Recursos/ACAs/`
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
    return md


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
- [ ] Material / plantilla APA en CDigital o Google Docs
- [ ] Link tutorías para chat: {LINK_TUTORIAS}
- [ ] Meet: {MEET}
{post_clase()}
---
*Fin del Guión — Sesión {n:02d}. Autocontenido para dictar 60+60.*
"""
    # La narración de estas sesiones venía de la plantilla de 7 slides: sus números no
    # corresponden al deck real (17–19 slides). Se retiran; queda el nombre del momento.
    md, _ = limpiar_referencias(md)
    return md


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
