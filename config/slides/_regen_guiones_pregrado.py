# -*- coding: utf-8 -*-
"""Regenera guiones docentes ricos (solo .md) para Investigación, TG2 y TG3.

Duración: 60 min. Modelo: Creatividad Sesión 01.
Incluye pantallazos embebidos (`![…](Capturas/…)`) en demos/prácticas.

Evaluación: cada guion recibe, desde `guion_evaluacion.py` (que lee el modelo único
`config/cursos/fechas_entrega_aca.py` = libro de calificaciones de CDigital), el aviso de
qué ítem cierra o abre ese día y —si ese día cae un **quiz o un parcial**— una fase con
minutos reservados dentro de los 60 (las demás fases se recortan; la hora no crece).
Uso:
  python _regen_guiones_pregrado.py                  # los 3 cursos
  python _regen_guiones_pregrado.py investigacion
  python _regen_guiones_pregrado.py tg2 3
  python _regen_guiones_pregrado.py all
"""
from __future__ import annotations

import os
import re
import sys

SLIDES = os.path.dirname(os.path.abspath(__file__))
CURSOS = os.path.join(SLIDES, "..", "cursos")
sys.path.insert(0, SLIDES)
sys.path.insert(0, CURSOS)

from sesiones_cun import COURSES, meet_url  # noqa: E402
from cun_slides_engine import PADLET_PRESENTACION_URL  # noqa: E402
from guion_evaluacion import (  # noqa: E402
    KIND_CUESTIONARIO,
    desglose,
    inyectar_evaluacion,
    items_corte_txt,
    peso_corte_txt,
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

KEYS = ("investigacion", "tg2", "tg3")


def topic_filename(titulo: str, max_len: int = 70) -> str:
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
    rows.append(f"> **Suma:** **{sum(m for _, m in fases)} minutos** exactos.")
    return "\n".join(rows)


def slides_std():
    return """🗺️ **Slides de esta presentación** (tema de hoy — no es el mapa del curso)

| Slide | Título en el PPTX | Cuándo usarla |
| :---: | :--- | :--- |
| **1** | Portada — Sesión NN | Apertura |
| **2** | OBJETIVOS | Encuadre |
| **3** | CONTENIDO CLAVE | Exposición |
| **4** | ENFOQUE DE HOY | Anclaje |
| **5** | ACTIVIDAD / TALLER | Consigna |
| **6** | PARA CONTINUAR | Trabajo autónomo |
| **7** | Cierre | Despedida |
"""


def shot(rel_path: str, caption: str, tip: str) -> str:
    """Bloque markdown con imagen relativa a Guiones/ + tip de pantalla."""
    return (
        f"\n![{caption}](Capturas/{rel_path})\n\n"
        f"> **En pantalla:** {tip}\n"
    )


# Contenido pedagógico por (course_key, n) — alineado a sesiones_cun
SPEC: dict[tuple[str, int], dict] = {}


def _spec(key, n, **kwargs):
    SPEC[(key, n)] = kwargs


# ----- Investigación (6 sesiones · EI005 periodo corto) -----
_spec(
    "investigacion", 1,
    uso_texto="""> **Uso:** guion de la sesión de **encuadre**. Hoy **no se dicta tema**: se presenta el curso, el Docente, el grupo y las ACAs.
> El contenido del Syllabus arranca en la **Sesión 02**; las unidades **U1–U2** quedan como **lectura autónoma** de esta semana.
> Léalo en voz alta casi literal. **Duración: 60 minutos**.""",
    slides_map="""🗺️ **Slides de esta presentación** (deck de **encuadre**, 21 slides — no es el mapa del curso)

| Slide | Título en el PPTX | Fase |
| :---: | :--- | :---: |
| **1** | Portada — Sesión 01 | 1 |
| **2** | AGENDA DE HOY | 1 |
| **3** | Docente | 1 |
| **4** | PRESÉNTATE — ROMPEHIELOS (QR + Padlet) | 2 |
| **5** | LAS ACAs — QUÉ SE EVALÚA | 4 |
| **6** | Cómo trabajamos: una hora en vivo, el resto en su documento | 3 |
| **7** | Mapa del curso: las 6 sesiones | 3 |
| **8** | Qué se llevan al final: un artículo | 3 |
| **9** | Este es un periodo corto: qué implica | 3 |
| **10** | Las ACAs, una por una | 4 |
| **11** | Cómo se entrega, paso a paso | 4 |
| **12** | Integridad académica | 4 |
| **13** | Inteligencia artificial generativa | 4 |
| **14** | Herramientas del curso | 4 |
| **15** | Cómo pedir ayuda | 4 |
| **16** | Acuerdos de convivencia | 5 |
| **17** | Preguntas frecuentes del primer día | 5 |
| **18** | Lo que debe tener listo para la Sesión 02 | 5 |
| **19** | ACUERDOS DE TRABAJO | 5 |
| **20** | PARA LA PRÓXIMA SESIÓN | 5 |
| **21** | Cierre — Sesión 01 | 5 |
""",
    objetivos="""1. **Encuadrar** el curso: cómo se usa la hora sincrónica, qué se hace en trabajo autónomo y cuál es el producto final (**un artículo**).
2. **Presentar** al Docente y conocer al grupo, dejando a cada estudiante en el Padlet oficial.
3. **Explicar** las ACAs, la ruta de entrega en CDigital y las reglas de integridad académica y de uso de IA generativa.
4. **Cerrar** con acuerdos de trabajo y con el encargo autónomo: **lectura de U1–U2** + ficha de tema tentativo.""",
    fundamento_titulo="🧰 **Preparación del Docente ANTES de la clase** *(hoy no hay tema que estudiar: hay logística que dejar lista)*",
    fundamento=f"""> Esta sesión se cae si el Padlet no abre, si el espacio de entrega no existe o si usted no puede mostrar en pantalla los **ítems reales del libro de calificaciones** ({items_corte_txt('investigacion', 1)} en el primer corte). Todo lo de abajo se deja listo **antes** de entrar al Meet.

#### 1. Qué debe tener abierto y probado
| Qué | Para qué lo necesita hoy |
| :--- | :--- |
| Aula del curso en **CDigital**, con el espacio de entrega de la Sesión 01 creado | Va a proyectar dónde se sube el encargo; nada de “luego les aviso” |
| **Presentación del Curso** (`Clases/Presentacion del Curso - ….pptx`) | Slide **PRESÉNTATE** (QR + Padlet) y logística de periodo (grupo, fechas, evaluación) |
| **Esta deck** (`Clases/Sesion 01 - …/Presentacion.pptx`) | Es el hilo de la hora: 21 slides, en orden |
| **Padlet oficial** abierto y probado en una pestaña | Rompehielos; el link se pega en el chat apenas empiece |
| **Libro de calificaciones** del aula, abierto en otra pestaña | Es la fuente de los nombres, tipos y pesos que va a anunciar hoy: los ítems se muestran, no se describen de memoria |
| Enunciado de la **ACA Final** (`Clases/Recursos/ACAs/`) | Es la única entrega documental del curso; la **fecha exacta vive ahí y en CDigital**, no en la deck |
| **Plantilla APA CUN** (`Clases/Recursos/`) | Mostrar en vivo cómo se abre en Google Docs, sin instalar Office |
| **Meet** de la serie, 10 minutos antes | Recibir a quien llega temprano y probar audio |
| Lista del grupo | Saludar por nombre y registrar asistencia |

#### 2. Qué NO se hace hoy
**No se dicta tema.** Si alguien pregunta por el método científico o por qué el producto es un artículo, la respuesta es: *“eso es exactamente la lectura de esta semana y lo abrimos en la Sesión 02”*. Adelantar U1–U2 hoy deja la próxima sesión sin sustancia y el encuadre a medias.

#### 3. Los tres mensajes que deben quedar grabados
1. **El producto del curso es un artículo**, y se empieza a construir esta misma semana.
2. **Se entrega en CDigital**, siempre, con la plantilla APA CUN.
3. **Son seis encuentros**: en periodo corto no existe la semana de recuperación.

#### 4. Tono del primer día
Es la única clase donde usted “vende” el curso. Hable despacio, use el nombre de quien participa y explique cada acuerdo **con la razón detrás**, no como lista de prohibiciones. Un encuadre bien hecho ahorra medio periodo de preguntas repetidas.""",
    ejemplo_titulo="#### Qué proyectar en pantalla (y en qué orden)",
    ejemplo="""Deje **cinco pestañas** abiertas y páselas en este orden, sin buscar nada en vivo:
**1.** Padlet (rompehielos) → **2.** CDigital, en el espacio de entrega de la sesión → **3.** el **libro de calificaciones** del aula, para leer en pantalla los ítems con su nombre y su peso → **4.** `Clases/Recursos/ACAs/` con el enunciado de la **ACA Final** → **5.** plantilla APA CUN abierta en Google Docs (*Archivo → Abrir con → Documentos de Google*).
Modelar el paso 5 en vivo, treinta segundos, evita la mitad de las preguntas de la primera semana.""",
    errores_titulo="#### Si un estudiante pregunta… (dudas reales del primer día)",
    errores_headers=("Si un estudiante pregunta…", "Usted responde…"),
    errores=[
        ("“¿Hoy no vamos a ver tema?”",
         "“Hoy es el encuadre: cómo trabajamos, cómo se evalúa y quiénes somos. El tema arranca la próxima sesión, y la lectura de esta semana es la base.”"),
        ("“¿Esta materia se pierde fácil?”",
         "“Se pierde por no entregar, casi nunca por escribir mal. Quien entrega los tres cortes, pasa; el riesgo es dejar todo para la última semana.”"),
        ("“¿Puedo trabajar solo o toca en grupo?”",
         "“El artículo de este curso es individual, salvo que el enunciado de la **ACA Final** diga otra cosa. Y los cuestionarios —quices y parciales— son **siempre individuales**.”"),
        ("“¿Los quices y los parciales son en clase?”",
         "“Sí: son cuestionarios de CDigital que cierran el mismo día de la sesión, y por eso les reservo tiempo en clase. El que falte ese día pierde el ítem, así que la asistencia aquí sí pesa en la nota.”"),
        ("“¿Me sirve un trabajo de otro semestre?”",
         "“Puede partir de un tema suyo, pero el texto debe ser nuevo y hay que citar lo que reutilice. Reentregarlo tal cual es falta académica.”"),
        ("“¿La clase se graba?”",
         "Dígalo con claridad según lo que usted vaya a hacer, y aclare lo que sí es fijo: “el material y la consigna quedan siempre publicados en CDigital”."),
        ("“¿Puedo usar ChatGPT para escribir?”",
         "“Como apoyo sí, y se declara en una línea al final del documento. Pero verifique las fuentes: inventa citas. Lo que usted no pueda explicar en voz alta, no le sirve.”"),
        ("“Todavía no tengo tema, ¿estoy mal?”",
         "“No. Hoy nadie tiene tema definitivo. Salga con una frase tentativa; en la Sesión 02 la afinamos con la línea de investigación.”"),
        ("“¿Dónde entrego?”",
         "“Solo en CDigital, en el espacio de la sesión. Lo que llegue por WhatsApp o correo personal no cuenta como entregado.”"),
    ],
    fases=[
        ("1️⃣ Apertura, agenda y presentación del Docente", 10),
        ("2️⃣ Preséntate: rompehielos en Padlet", 10),
        ("3️⃣ Recorrido del curso: cómo trabajamos y qué se llevan", 14),
        ("4️⃣ Cómo se evalúa (quices, parciales y ACA Final), entrega e integridad", 18),
        ("5️⃣ Acuerdos, encargo autónomo y cierre", 8),
    ],
    fase_slides=[
        "Slides 1–3 (Portada · AGENDA · Docente)",
        "Slide 4 (PRESÉNTATE — Padlet)",
        "Slides 6–9 (cómo trabajamos · mapa · producto · periodo corto)",
        "Slides 5 y 10–15 (evaluación real del aula · entrega · integridad · IA · herramientas · ayuda)",
        "Slides 16–21 (convivencia · dudas · Sesión 02 · acuerdos · cierre)",
    ],
    s01_padlet=True,
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Buenas tardes y bienvenidos a Investigación, Ciencia y Tecnología. Soy el Docente que los va a acompañar este periodo. Aclaro algo de una vez: **hoy no vamos a ver tema**. Hoy vamos a entender cómo funciona este curso, qué se entrega, cómo se evalúa y quién es quién. El contenido arranca en la próxima sesión.”

> “**Slide 2 — AGENDA DE HOY.** El orden es este: les cuento de qué se trata el curso y cómo trabajamos; me presento; se presentan ustedes en un tablero; vemos las ACAs, es decir qué se entrega y cuánto pesa; y cerramos con los acuerdos y con la tarea de esta semana. Una hora exacta, sin dictado.”

> “**Slide 3 — Docente.** Un minuto sobre mí, para que sepan a quién le están escribiendo.” [Preséntese con las credenciales de la slide: formación, experiencia y una frase de por qué le interesa la investigación aplicada.] “Mi correo está en pantalla: úsenlo para novedades personales. Todo lo académico va por CDigital, porque ahí queda registro y lo ven todos.”

**Cómo se maneja este arranque:** salude por nombre a quien va entrando (no solo “presentes”); es el primer gesto de que aquí nadie es un número. Si el grupo está frío, no llene el silencio con más discurso: pase de una vez al Padlet.""",
    fase2_texto="""**Protagonista:** Estudiantes (Padlet) · Docente conduce.

**En pantalla:** Presentación del Curso → slide **PRESÉNTATE**, con el QR. URL: """ + PADLET_PRESENTACION_URL + """

**GUION LITERAL:**
> “**Slide 4 — PRESÉNTATE.** Ahora los quiero conocer. En pantalla hay un QR y un enlace; lo dejo también en el chat del Meet. Es un tablero colaborativo: pongan un post-it con (a) su nombre, (b) qué esperan de este curso y (c) una idea o un problema de ingeniería que les dé curiosidad. Una frase por punto, no un ensayo. Tienen unos siete minutos y no hay respuestas malas.”

> [Mientras escriben, deje el tablero proyectado y ponga **usted** el primer post-it, narrándolo en voz alta.] “Yo pongo el mío para romper el hielo.”

> “Voy a leer tres o cuatro en voz alta.” [Lea, agradezca por nombre y conecte cada post-it con el curso: *“esto que escribió [nombre] ya suena a tema investigable; lo trabajamos en la Sesión 02”*.]

**Si nadie escribe** — pasa casi siempre el primer día virtual:
| Situación | Qué hace el Docente |
| :--- | :--- |
| Silencio total a los 2 minutos | Escribe un segundo post-it de ejemplo y dice en voz alta lo que está escribiendo. |
| “No me abre el link” | Pega el URL otra vez en el chat y ofrece que lo digan por micrófono; usted lo transcribe al tablero. |
| Post-its de una palabra (“ninguna”) | Pregunta directo, por nombre: “¿qué le gustaría que le sirviera de este curso?”. |
| Alguien pone algo de broma | Se agradece con humor y se reencauza; **no se borra en vivo** delante del grupo. |""",
    fase3_texto="""**Protagonista:** Docente (recorrido de la deck).

**GUION LITERAL:**
> “**Slide 6 — Cómo trabajamos.** Este curso son seis encuentros de una hora. Con seis horas no se aprende a investigar oyendo: se aprende escribiendo. El trato es este: ustedes llegan con la lectura hecha, yo explico el criterio en diez o quince minutos, y el resto lo usamos para que cada uno escriba su documento mientras yo paso resolviendo. Por eso les pido siempre dos cosas: el documento abierto y una duda concreta.”

> “**Slide 7 — Mapa del curso.** Miren las seis sesiones. Fíjense en la última columna: ninguna sesión termina en apuntes, todas terminan en algo escrito —la línea, el avance, la pregunta, el planteamiento, el marco—. Y lean la nota de abajo: las unidades 1 y 2 del Syllabus no desaparecen; son la **lectura de esta semana** y las retomamos al abrir la Sesión 02.”

> “**Slide 8 — Qué se llevan al final.** El producto es **un artículo**. No seis trabajos sueltos: uno solo, que crece. Al final debe tener título, introducción, problema, pregunta, marco con fuentes citadas y lista de referencias. ¿Para qué sirve de verdad? Es la semilla de su trabajo de grado y la prueba de que usted puede sostener una idea con evidencia y no con opinión.”

> “**Slide 9 — Este es un periodo corto.** No se lo digo para asustarlos, sino para que se organicen: son seis encuentros, faltar a uno es perder casi la sexta parte del curso, y los avances se acumulan. Si faltan, revisen CDigital ese mismo día: la consigna queda publicada.”

**Pregunte a dos estudiantes:** “¿en qué semana creen que se empieza a escribir el artículo?”. Conviene que la respuesta —**esta semana**— la digan ellos.""",
    fase4_texto=f"""**Protagonista:** Docente, compartiendo pantalla (CDigital + libro de calificaciones + plantilla APA).

**GUION LITERAL:**
> “**Slide 5 — Cómo se evalúa este curso.** Miren la tabla, pero escuchen esto porque es lo que decide la nota: en el aula **no hay tres trabajos escritos**. hay **{items_corte_txt('investigacion', 1)}** en el primer corte, **{items_corte_txt('investigacion', 2)}** en el segundo y **{items_corte_txt('investigacion', 3)}** en el tercero. Los quices y los parciales son **cuestionarios de CDigital**; la ACA Final es la **única tarea con documento**; y la **coevaluación es un foro**, o sea que hay que escribir en él.”

> “Lo voy a decir de la forma que a ustedes les importa: los **cuestionarios suman {peso_tipo('investigacion', KIND_CUESTIONARIO)} del curso**, más que el documento. El **Parcial 1**, solo él, vale {peso_item('investigacion', 'parcial1')}. Quien viene a clase y responde, pasa; quien se guarda todo para el documento del final, no alcanza.”

> “**Slide 10 — ítem por ítem.** Los quices y los parciales caen **en día de clase**: se abren aquí, tienen tiempo y cierran el mismo día, así que faltar a esa sesión es perder ese ítem. La **ACA Final** es distinta: es el documento acumulativo, se sube en PDF y cierra en la fecha de recepción del periodo. La **autoevaluación** se diligencia y la **coevaluación** se participa; las dos abren al final y son individuales.”

> “Las **fechas exactas no están en esta presentación a propósito**, porque se desactualizan: viven en el ítem de CDigital y en el enunciado. Ábranlas hoy mismo y pásenlas a su calendario con alarma.”

> “**Slide 11 — Cómo se entrega.** Esto es puro procedimiento y les ahorra sustos.” [Hágalo en vivo: abra la plantilla APA CUN en Google Docs, muestre el nombre de archivo `SNN_Tema_Apellido`, descargue como PDF y abra el espacio de entrega en CDigital.] “Apellido en el nombre del archivo, PDF, CDigital. Y verifiquen el estado: **subido no es entregado**.”

> “**Slide 12 — Integridad académica.** Citar no es un adorno: es lo que separa un trabajo académico de un texto de internet. Todo lo que no es suyo se cita en APA 7. Copiar y pegar sin comillas, traducir un texto ajeno o entregar el trabajo de otro es plagio, y eso tiene **debido proceso institucional**; no es algo que yo arregle en privado. El truco práctico es simple: anoten la fuente en el mismo instante en que pegan algo.”

> “**Slide 13 — Inteligencia artificial.** Hablemos claro, porque todos la van a usar. Sí se puede usar para entender un concepto o pulir la redacción de un párrafo que ya escribieron. Se declara en una línea al final del documento. Y hay una regla que no negocio: **verifiquen las fuentes**, porque estas herramientas inventan citas y DOIs que no existen. Si yo les pregunto por qué escribieron algo y no lo pueden explicar, ese párrafo no les sirve.”

> “**Slide 14 — Herramientas.** Todas gratis y en el navegador: Docs, Google Académico, SciELO, Redalyc, la biblioteca CUN, ZoteroBib para las citas, Excalidraw para diagramar y CDigital para entregar. Nadie tiene que comprar ni instalar nada.”

> “**Slide 15 — Cómo pedir ayuda.** Foro de CDigital para lo académico, correo para lo personal, respuesta en días hábiles y siempre antes del siguiente encuentro. Y una petición: pregunten con contexto, con el texto en la mano. Miren los dos ejemplos de la slide y noten la diferencia.”""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “**Slides 16 y 17 — Convivencia y dudas frecuentes.** Dos minutos de acuerdos: empezamos a la hora, micrófono apagado mientras alguien habla, cámara si su conexión da, y respeto en el foro —se comenta el texto, nunca a la persona—. En la siguiente slide dejé las dudas que siempre salen el primer día; léanlas con calma después.”

> “**Slide 18 — Lo que debe tener listo para la Sesión 02.** Esta es la tarea, y es doble. Primero, la **lectura autónoma**: las unidades 1 y 2 del Syllabus, publicadas en CDigital. Media hora de lectura y traen **dos dudas anotadas**. Segundo, escriban su **tema tentativo** en un Google Doc llamado `S01_TemaTentativo_Apellido`: una frase con actor, fenómeno y contexto; dos o tres líneas de por qué les importa; y una fuente que encuentren en Google Académico. Súbanlo a CDigital antes de la próxima clase.”

> “**Slides 19 y 20 — Acuerdos y para la próxima.** Resumo el trato: se entrega en CDigital, se trae el avance escrito y se cita en APA 7. Con esas tres, este curso funciona.”

> “**Slide 21 — Cierre.** Ya saben qué vamos a hacer, cómo se evalúa y quién es quién. La próxima sesión abre con los temas de ustedes en pantalla y con las dudas de la lectura. Gracias, y nos vemos el próximo jueves en el mismo Meet.”""",
    entregable_titulo="🧩 **Encargo autónomo (para la Sesión 02)**",
    taller="**No se hace en clase, es trabajo autónomo:** leer las unidades **U1–U2** publicadas en CDigital y anotar 2 dudas; y redactar en Google Docs la ficha de **tema tentativo** — una frase con actor + fenómeno + contexto, 2–3 líneas de por qué importa y 1 fuente exploratoria de Google Académico.",
    entregable="`S01_TemaTentativo_Apellido` (Google Doc o PDF), **antes de la Sesión 02**.",
    checklist=[
        "- [ ] Aula del curso en **CDigital** abierta, con el espacio de entrega de la Sesión 01 creado",
        "- [ ] **Lectura autónoma U1–U2 publicada en CDigital** (sin eso el encargo de hoy no se puede cumplir)",
        "- [ ] **Padlet** oficial probado y el link listo para pegar en el chat: " + PADLET_PRESENTACION_URL,
        "- [ ] **Presentación del Curso** abierta en la slide PRESÉNTATE (QR)",
        "- [ ] Deck de hoy abierta (`Presentacion.pptx` de la Sesión 01 — 21 slides)",
        "- [ ] **Libro de calificaciones** del aula abierto (nombres, tipos y pesos reales) y enunciado de la **ACA Final** listo para proyectar",
        "- [ ] **Plantilla APA CUN** lista para mostrar en Google Docs",
        "- [ ] Lista del grupo para saludar por nombre y registrar asistencia",
        "- [ ] Meet de la serie abierto **10 minutos antes** (enlace en la ficha de arriba)",
    ],
    shots_fase2=[
        ("Sesion 01/inv_s01_padlet.png", "Padlet — Preséntate (tablero oficial)",
         "Tablero de la Presentación del Curso. Pegue el URL en el chat, ponga usted el primer post-it y lea 3–4 en voz alta (~7 min)."),
    ],
    shots_taller=[
        ("inv_google_docs.png", "Google Docs — plantilla APA CUN",
         "Modele en vivo: abrir la plantilla con *Archivo → Abrir con → Documentos de Google*, nombrar el archivo `SNN_Tema_Apellido` y descargar como PDF."),
    ],
)

_spec(
    "investigacion", 2,
    objetivos="""1. **Explicar** qué es MinCiencias y cómo el Sistema Nacional de CTeI organiza la investigación en líneas.
2. **Reconocer** las **6 líneas de Ingeniería** del programa (IoT, Big Data, IA, servicios cloud/FinTech, aplicaciones, telemática) y su alcance.
3. **Elegir** una línea tentativa para el artículo y **justificarla** en un párrafo, con 2 referentes exploratorios.""",
    fundamento="""#### 1. ¿Qué es MinCiencias y por qué le importa a su artículo?
El **Ministerio de Ciencia, Tecnología e Innovación (MinCiencias)** coordina el **Sistema Nacional de CTeI** de Colombia y organiza la investigación por **áreas y líneas** (orientan convocatorias, grupos y financiación). Para el estudiante la utilidad es muy concreta: la línea **define el vocabulario, los referentes y las revistas** donde buscará. Elegir bien la línea ahorra semanas de búsqueda perdida.

#### 2. Las 6 líneas de Ingeniería del programa
| Línea | De qué trata | Pregunta ejemplo |
| :--- | :--- | :--- |
| IoT (Internet de las Cosas) | Sensores y dispositivos conectados | ¿Cómo monitorear el consumo eléctrico de un laboratorio con sensores? |
| Big Data | Analítica de grandes volúmenes de datos | ¿Qué patrones de deserción revelan los datos de matrícula? |
| Inteligencia Artificial | Modelos que aprenden de datos | ¿Puede un clasificador detectar correos de phishing institucionales? |
| Servicios cloud / FinTech | Nube y servicios financieros | ¿Qué riesgos de seguridad tiene migrar los pagos a la nube? |
| Aplicaciones | Desarrollo de software | ¿Qué barreras de usabilidad tiene el portal X para adultos mayores? |
| Telemática | Redes y comunicaciones | ¿Cómo afecta la latencia a las clases sincrónicas en la sede Y? |

#### 3. La línea NO es un trámite: condiciona el marco
Si elige "IA", buscará en fuentes de IA y su marco hablará de modelos, datos y sesgos. Si elige "telemática", hablará de protocolos, latencia y topologías. Elegir la línea correcta es elegir **con qué comunidad de conocimiento va a dialogar** su artículo.

#### 4. Criterios para elegir bien
1. **Afinidad** con el tema tentativo de la Sesión 01.
2. **Viabilidad de fuentes/datos:** ¿hay literatura y datos accesibles este periodo?
3. **Pertinencia local:** ¿resuelve algo de su entorno o su práctica?

Regla de oro: **una sola línea principal**. Puede rozar otra, pero no trabajar tres a la vez.""",
    errores=[
        ("“Elijo IA porque está de moda.”",
         "La moda no da datos: elija donde haya fuentes accesibles y afinidad con su tema."),
        ("“Puedo trabajar en tres líneas a la vez.”",
         "No: una línea principal. Tres líneas = ningún marco sólido."),
        ("“La línea es un requisito administrativo.”",
         "Define su vocabulario y sus referentes; cambiarla luego obliga a reescribir el marco."),
        ("“Mi tema no cabe en ninguna línea.”",
         "Casi siempre cabe; ayúdelo a re-encuadrar hacia la línea más cercana."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ MinCiencias y líneas", 16),
        ("3️⃣ Criterios de elección", 10),
        ("4️⃣ Taller: línea + justificación", 20),
        ("5️⃣ Cierre", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Buenas tardes. Sesión 02. La semana pasada cada uno dejó un **tema tentativo**. Hoy le ponemos apellido a ese tema: lo ubicamos en una **línea de investigación** para saber dónde buscar y con quién dialogar.”

> “**Slide 2 — OBJETIVOS:** entender qué es MinCiencias, conocer las 6 líneas del programa y elegir la suya con una justificación escrita. Tengan a la mano su ficha de la Sesión 01, porque de ahí partimos.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Empecemos por MinCiencias. Es el Ministerio de Ciencia, Tecnología e Innovación; coordina el sistema nacional que organiza la investigación del país en áreas y líneas. Para ustedes lo importante es esto: la investigación no flota, se agrupa en líneas, y **cada línea tiene su propio lenguaje y sus propias fuentes**.”

> “**Slide 4 — ENFOQUE DE HOY.** Nuestro programa trabaja seis líneas: IoT, Big Data, Inteligencia Artificial, servicios cloud/FinTech, aplicaciones y telemática. Voy a describir cada una con una pregunta de ejemplo para que se ubiquen.” (Recorra la tabla del Fundamento línea por línea.)

> “Fíjense en algo: la misma idea de 'seguridad' se ve distinta según la línea. En IA es detección de fraude con modelos; en telemática es seguridad de la red; en cloud es proteger datos en la nube. **La línea decide el ángulo.**”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** tabla de decisión con columnas *Línea · Afinidad · ¿Hay fuentes? · Pertinencia local*.

**GUION LITERAL:**
> “Modelo la decisión con un caso. Tema: 'phishing en los correos de los estudiantes'. Comparo dos líneas: IA (clasificar correos maliciosos) y telemática (filtrar en la red). Lleno la tabla: en IA hay muchísima literatura y datos de ejemplo; en telemática también, pero necesito acceso a la red institucional. **Gana IA por viabilidad de datos.**”

> “Regla de oro, otra vez: **una línea principal**. Pueden mencionar que roza otra, pero el marco se escribe para una. Y ojo: no elijan por moda; elijan por dónde puedan conseguir fuentes este periodo.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En su Doc `S02_LineaInvestigacion_Apellido` escriban: (1) la **línea elegida**; (2) un **párrafo de justificación** que responda a los tres criterios —afinidad, fuentes disponibles y pertinencia local—; (3) **dos referentes exploratorios** que encuentren en Google Académico, en APA tentativa.”

> “Criterio de éxito: al leer su párrafo entiendo por qué esa línea y no otra, y veo que ya existe literatura para trabajarla.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Duda entre dos líneas | “¿En cuál consigue datos y papers esta semana? Esa gana.” |
| Elige por moda (IA) | “Muéstreme 2 fuentes reales; si no aparecen, reconsidere.” |
| Su tema 'no cabe' | “Re-encuádrelo: ¿es un problema de datos, de red o de software?” |
| No halla referentes | “Busque en inglés y con términos técnicos; luego lo traducimos.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) MinCiencias organiza la investigación en líneas; (2) el programa tiene 6 líneas de ingeniería; (3) la línea define su vocabulario y sus fuentes, así que se elige **una** principal y se justifica.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S02_LineaInvestigacion_Apellido` a CDigital y afinen los 2 referentes. La próxima sesión es clave: **prueba parcial + primer avance del artículo**; traigan su tema y su línea ya definidos, porque son la materia prima del avance.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet la próxima.”""",
    taller="En Google Docs: línea elegida + párrafo de justificación (afinidad + fuentes + pertinencia local) + 2 referentes exploratorios en APA tentativa (Google Académico).",
    entregable="`S02_LineaInvestigacion_Apellido` en CDigital.",
    ejemplo="Tema 'phishing en correos de estudiantes' → línea **Inteligencia Artificial** (detección de correos maliciosos), justificada por la abundancia de datasets y literatura.",
    shots_demo=[
        ("inv_google_docs.png", "Google Docs — tabla de decisión de línea",
         "Columnas: Línea | Afinidad | ¿Hay fuentes? | Pertinencia local. Llenar 2 filas en vivo y elegir."),
    ],
    shots_taller=[
        ("inv_google_scholar.png", "Google Académico — 2 referentes de la línea",
         "Con la línea elegida, localizar 2 títulos y anotar APA tentativa. Si aparece 'tráfico inusual', usar el navegador del docente."),
    ],
)

_spec(
    "investigacion", 3,
    objetivos="""1. **Aclarar** qué evalúa la prueba escrita parcial y qué debe contener el **1.er avance** del artículo.
2. **Distinguir** tipos de conocimiento (cotidiano, empírico, científico) y tipos de fuentes (primaria, secundaria, terciaria).
3. **Entregar** un borrador mínimo viable: título + introducción breve + problema/pregunta + primeras referencias.""",
    fundamento="""#### 1. Qué es el 1.er avance (y qué NO es)
El primer avance **no** es "media tesis". Es un **borrador mínimo viable**: título tentativo, una introducción breve, el problema/pregunta y 2–3 referencias. Repita el lema del curso: **calidad > extensión**. Media página bien planteada vale más que cinco de relleno.

#### 2. Estructura mínima del artículo en este punto
| Sección del avance | Qué va | Error típico |
| :--- | :--- | :--- |
| Título tentativo | Actor + fenómeno + contexto en ≤ 20 palabras | Título-eslogan sin variables |
| Introducción breve | Contexto → vacío → propósito (3 párrafos) | Empezar con "desde la antigüedad…" |
| Problema y pregunta | El vacío convertido en pregunta investigable | Pregunta de sí/no |
| Referencias iniciales | 2–3 fuentes en APA 7 | Copiar URLs sin formato |

#### 3. Tipos de conocimiento (lo que suele preguntar el parcial)
- **Cotidiano / vulgar:** "sé que llueve porque me mojé." Sin método.
- **Empírico:** basado en experiencia repetida y observación, pero sin sistematizar.
- **Científico:** sistemático, verificable, con método y evidencia. **Es el que sostiene su artículo.**

#### 4. Tipos de fuentes y confiabilidad
- **Primaria:** el estudio original (paper, dataset, norma).
- **Secundaria:** interpreta primarias (revisión, libro de texto).
- **Terciaria:** índices y enciclopedias (guían, no se citan como autoridad).

Regla: Wikipedia y blogs **orientan**, pero **no** son fuente para el artículo.""",
    errores=[
        ("“Más páginas = mejor nota en el avance.”",
         "No: se evalúa el planteamiento claro. Media página sólida gana a cinco de relleno."),
        ("“Cito Wikipedia y un blog.”",
         "Orientan, no son fuente. Lleve la referencia a una primaria o secundaria confiable."),
        ("“La introducción arranca con 'desde la antigüedad el ser humano…'.”",
         "Arranque en el contexto real del problema, no en la historia universal."),
        ("“Conocimiento empírico y científico son lo mismo.”",
         "El empírico observa; el científico sistematiza, verifica y usa método."),
    ],
    fases=[
        ("1️⃣ Encuadre criterios del avance", 8),
        ("2️⃣ Estructura mínima del artículo", 12),
        ("3️⃣ Modelación de introducción", 10),
        ("4️⃣ Taller de escritura", 22),
        ("5️⃣ Cierre / entrega", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 03, y es una sesión bisagra: hoy trabajamos la **prueba parcial** y el **primer avance** del artículo. Quiero bajarles la ansiedad de una vez: el avance no es media tesis, es un **borrador mínimo viable** bien planteado.”

> “**Slide 2 — OBJETIVOS.** Vamos a: aclarar qué evalúa el parcial, repasar tipos de conocimiento y de fuentes —porque suelen caer— y salir con el borrador del avance empezado. Tengan abierto su Doc con el tema y la línea de las sesiones anteriores.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** El avance tiene cuatro piezas: título, introducción breve, problema/pregunta y primeras referencias. Solo cuatro. Y una regla que voy a repetir todo el semestre: **calidad sobre extensión**.”

> “Ahora la parte conceptual que suele caer en el parcial. Tipos de conocimiento: el **cotidiano** —me mojé, luego llueve—, el **empírico** —lo he visto muchas veces— y el **científico** —lo mido, lo verifico, uso método—. Su artículo se sostiene en el tercero.”

> “**Slide 4 — ENFOQUE DE HOY.** Y los tipos de fuente: **primaria** es el estudio original; **secundaria** lo interpreta; **terciaria** es un índice o enciclopedia. Wikipedia orienta, pero no se cita como autoridad. Todo esto no es para memorizar: es para que su avance tenga fuentes que aguanten una revisión.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** escriba una introducción de 3 párrafos en vivo.

**GUION LITERAL:**
> “Modelo una introducción con la estructura **contexto → vacío → propósito**. Párrafo 1, contexto: 'En los laboratorios de redes se realizan prácticas que dependen de una conexión estable…'. Párrafo 2, vacío: 'Sin embargo, no se ha caracterizado con datos la pérdida de paquetes en el laboratorio X…'. Párrafo 3, propósito: 'Este artículo busca describir esa pérdida y su impacto en las prácticas.'”

> “Vean lo que **no** hice: no empecé con 'desde la antigüedad el ser humano se comunica'. Arranqué en el problema real. Ese es el estándar del curso.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~22 minutos. En `S03_Avance1_Apellido` escriban las cuatro piezas: (1) título tentativo con actor+fenómeno+contexto; (2) introducción de 3 párrafos contexto→vacío→propósito; (3) el problema convertido en una pregunta; (4) dos referencias en APA 7 usando ZoteroBib. Prefiero media página impecable a tres de relleno.”

> “Criterio de éxito: si leo su introducción sin conocer su tema, entiendo el contexto, el vacío y qué se proponen.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe una intro larguísima | “Recorte a 3 párrafos: contexto, vacío, propósito.” |
| No tiene referencias | “Vamos a ZoteroBib: pegue un DOI o título y genere el APA.” |
| Su pregunta se responde sí/no | “Reformule con 'cómo', 'qué' o 'en qué medida'.” |
| Copia una definición de un blog | “Lléveme a una fuente primaria o secundaria; el blog no cuenta.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cerramos. Tres ideas: (1) el avance son cuatro piezas bien hechas, no muchas páginas; (2) el conocimiento que sostiene el artículo es el **científico**; (3) mandan las fuentes primarias y secundarias, no los blogs.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S03_Avance1_Apellido` a CDigital. Y revisen en CDigital el **detalle de la evaluación de este corte** —el desglose oficial vive allí—. La próxima sesión afinamos el corazón del artículo: **identificar el problema y formular la pregunta**.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs (`S03_Avance1_Apellido`): título tentativo + introducción de 3 párrafos (contexto→vacío→propósito) + pregunta + 2 referencias en APA 7 con ZoteroBib.",
    entregable="`S03_Avance1_Apellido` en CDigital.",
    ejemplo="Introducción de 3 párrafos: contexto de las prácticas de laboratorio → vacío (sin datos de pérdida de paquetes) → propósito del artículo.",
    shots_demo=[
        ("inv_google_docs.png", "Google Docs — introducción modelada",
         "Escribir en vivo 3 párrafos: contexto / vacío / propósito. Señalar qué NO hacer (arranque histórico)."),
    ],
    shots_taller=[
        ("inv_zoterobib.png", "ZoteroBib — APA 7 en la nube",
         "Pegar 1 DOI/URL → generar APA 7 → copiar a Google Docs. Sin instalar Zotero de escritorio."),
    ],
)

_spec(
    "investigacion", 4,
    objetivos="""1. **Diferenciar** un problema de investigación de "la falta de mi solución".
2. **Aplicar** una herramienta de identificación —espina de pescado, árbol de problemas o método 3D— para ordenar causas y efectos.
3. **Formular** una pregunta investigable (clara, delimitada, viable) alineada al tema y a la línea.""",
    fundamento="""#### 1. Problema ≠ ausencia de mi solución
El error más común: "el problema es que no existe mi app". Eso no es un problema de investigación, es un **deseo de producto**. El problema es un **hecho observable que genera consecuencias**: "los tutores dan feedback tarde y los estudiantes repiten errores". La app es una posible respuesta, no el problema.

#### 2. Tres herramientas para ordenar el problema
- **Espina de pescado (Ishikawa):** la "cabeza" es el efecto/problema; las "espinas" son familias de causas (personas, proceso, tecnología, entorno). Evita quedarse con una sola causa.
- **Árbol de problemas:** raíces = causas, tronco = problema central, ramas = efectos. Luego se "voltea" en árbol de objetivos.
- **Método 3D (según el material del curso):** acota el hecho en tres momentos — **Describir** qué pasa, **Dimensionar** cuánto y a quiénes afecta, **Decidir** la pregunta. Útil cuando el tema es muy amplio.

| Herramienta | Qué produce | Cuándo usarla |
| :--- | :--- | :--- |
| Espina de pescado | Familias de causas de un efecto | Hay muchas causas dispersas |
| Árbol de problemas | Causas → problema → efectos | Necesita separar causa de consecuencia |
| Método 3D | Descripción acotada + pregunta | El tema está demasiado amplio |

#### 3. De problema a pregunta investigable
Una buena pregunta es **clara** (se entiende sola), **delimitada** (actor + contexto + tiempo), **viable** (hay datos/fuentes) y **relevante**. Evite las preguntas de sí/no y las preguntas planetarias.""",
    errores=[
        ("“El problema es que no existe mi aplicación.”",
         "Eso es un deseo de producto. El problema es el hecho que duele; la app es una posible respuesta."),
        ("“¿Es útil la inteligencia artificial? — como pregunta.”",
         "Es de sí/no y planetaria. Reformule con actor, contexto y 'en qué medida'."),
        ("“Confundo causas con efectos en el árbol.”",
         "Pregunte 'por qué ocurre' (causa) vs '¿qué provoca?' (efecto) para ubicarlos."),
        ("“Una sola causa lo explica todo.”",
         "Casi nunca; use la espina para abrir 3–4 familias de causas."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Problema y pregunta", 14),
        ("3️⃣ Modelación (espina / árbol)", 12),
        ("4️⃣ Taller", 20),
        ("5️⃣ Cierre", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 04. Llegamos al **corazón** de toda investigación: el problema y la pregunta. Si esto queda bien, el resto del artículo casi se escribe solo. Si queda mal, todo lo demás cojea.”

> “**Slide 2 — OBJETIVOS.** Hoy: separar el problema de 'la falta de mi solución', usar una herramienta para ordenar causas y efectos, y salir con una **pregunta investigable escrita**.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Primero, la trampa número uno: muchos escriben 'el problema es que no existe una app que…'. Eso no es un problema, es que **quieren hacer una app**. El problema es un hecho que genera consecuencias: 'los tutores dan feedback tarde, y por eso los estudiantes repiten el mismo error'. Uno se puede investigar; el otro es un antojo.”

> “**Slide 4 — ENFOQUE DE HOY.** Para ordenar el problema tenemos tres herramientas: la **espina de pescado** abre familias de causas; el **árbol de problemas** separa causas, problema y efectos; y el **método 3D** —describir, dimensionar, decidir— sirve para acotar temas gigantes.”

> “Y de ahí sale la **pregunta**. Una buena pregunta es clara, delimitada, viable y no se responde con sí o no. Nada de '¿sirve la IA?'; sí a '¿en qué medida un clasificador reduce el phishing en los correos de la sede X?'.”""",
    fase3_texto="""**Protagonista:** Docente (modela en pantalla).

**En pantalla (Excalidraw o Google Docs):** dibuje una espina de pescado o un árbol de problemas.

**GUION LITERAL:**
> “Modelo en vivo. Abro **Excalidraw** —sin cuenta, gratis— y dibujo la cabeza del pescado con el efecto: 'los estudiantes repiten errores en el laboratorio'. Ahora las espinas: personas (tutores saturados), proceso (feedback sin fecha límite), tecnología (no hay registro de entregas), entorno (grupos grandes).”

> “Con eso convierto el problema en pregunta: '¿en qué medida el tiempo de respuesta del feedback influye en la repetición de errores de los estudiantes del laboratorio X?'. Fíjense cómo la pregunta salió directa de **una** de las espinas.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S04_ProblemaPregunta_Apellido`: (1) describan el problema en 8–12 líneas, como hecho con consecuencias, no como falta de su solución; (2) hagan un diagrama —espina de pescado o árbol— en Excalidraw y peguen la captura; (3) escriban la pregunta en **una sola frase** investigable.”

> “Criterio de éxito: su pregunta tiene actor y contexto, no se responde con sí/no, y el diagrama muestra al menos tres causas.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe "no existe una app que…" | “Eso es su solución. ¿Qué hecho duele hoy, sin la app?” |
| Pregunta gigante ("¿sirve la IA?") | “Bájela a un actor y un lugar concretos.” |
| Mezcla causas y efectos | “En el árbol: causas abajo, efectos arriba. Reubique.” |
| Solo ve una causa | “Abra la espina: personas, proceso, tecnología, entorno.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el problema es un hecho con consecuencias, no la falta de su app; (2) espina, árbol y método 3D ordenan causas y efectos; (3) la pregunta se escribe en una frase investigable.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S04_ProblemaPregunta_Apellido` con el diagrama. La próxima sesión tomamos esta pregunta y la desarrollamos en el **planteamiento del problema** completo.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs + Excalidraw (`S04_ProblemaPregunta_Apellido`): problema en 8–12 líneas + diagrama (espina o árbol) + pregunta investigable en una frase.",
    entregable="`S04_ProblemaPregunta_Apellido` en CDigital (Doc + captura del diagrama).",
    ejemplo="De 'haré un chatbot' a '¿en qué medida el tiempo de respuesta del feedback influye en la repetición de errores en el laboratorio X?'.",
    shots_demo=[
        ("inv_google_docs.png", "Google Docs / Excalidraw — problema → pregunta",
         "Modelar síntoma → consecuencias → pregunta en una frase; abrir https://excalidraw.com/ (sin cuenta) para el diagrama."),
    ],
    shots_taller=[
        ("inv_google_scholar.png", "Google Académico — validar que la pregunta es investigable",
         "Buscar 2 términos de la pregunta; si aparece literatura, la pregunta es viable."),
    ],
)

_spec(
    "investigacion", 5,
    objetivos="""1. **Redactar** el planteamiento del problema completo (estado actual, evidencias, causas, consecuencias, vacío y pregunta).
2. **Respaldar** las afirmaciones con evidencia (datos o estudios), no con opinión.
3. **Alinear** el planteamiento con la pregunta formulada en la sesión anterior.""",
    fundamento="""#### 1. Qué es el planteamiento (y su estructura de embudo)
El planteamiento es la sección donde **argumenta que su problema existe y merece estudiarse**. Va de lo general a lo específico (un embudo): estado actual → evidencias → causas → consecuencias → vacío → pregunta. Al final del embudo debe caer, natural, la **misma pregunta** de la Sesión 04.

#### 2. Evidencia, no opinión
"Creo que muchos estudiantes reprueban" es opinión. "El 34 % reprobó según el reporte X (2024)" es evidencia. El planteamiento fuerte se apoya en datos, informes o estudios; la opinión sin respaldo debilita el artículo.

| Componente | Pregunta que responde | Ejemplo |
| :--- | :--- | :--- |
| Estado actual | ¿Qué ocurre hoy? | "Las prácticas dependen de una red inestable." |
| Evidencias | ¿Cómo lo sé? | "La bitácora del laboratorio: 12 caídas en un mes." |
| Causas | ¿Por qué ocurre? | "Cableado antiguo, saturación en horas pico." |
| Consecuencias | ¿A quién/qué afecta? | "Prácticas incompletas, repetición de sesiones." |
| Vacío | ¿Qué falta saber? | "No hay medición de la pérdida de paquetes." |
| Pregunta | ¿Qué me propongo responder? | La pregunta de la Sesión 04. |

#### 3. Del dato a la prosa
Truco de escritura: primero llene una **tabla síntoma / evidencia / consecuencia** y luego conviértala en párrafos. Escribir la tabla evita la página en blanco y garantiza que **cada afirmación tenga respaldo**.""",
    errores=[
        ("“Escribo lo que creo, sin datos.”",
         "Cada afirmación fuerte necesita una cifra o un estudio; sin evidencia es opinión."),
        ("“Empiezo por la solución que quiero proponer.”",
         "El planteamiento argumenta el problema; la solución va mucho después."),
        ("“El planteamiento no termina en la pregunta.”",
         "Debe caer exactamente en la pregunta de la sesión anterior; si no, algo está desalineado."),
        ("“Pongo 10 causas sin jerarquía.”",
         "Priorice 2–3 causas con evidencia; el resto dispersa."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Estructura del planteamiento", 14),
        ("3️⃣ Modelación", 10),
        ("4️⃣ Taller de redacción", 22),
        ("5️⃣ Cierre", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 05. Ya tienen la pregunta; hoy la **vestimos**: escribimos el planteamiento del problema. Es la sección donde ustedes convencen al lector de que su problema es real y vale la pena estudiarlo.”

> “**Slide 2 — OBJETIVOS.** Redactar el planteamiento con sus seis componentes, respaldarlo con evidencia y que termine, natural, en la pregunta de la clase pasada. Tengan abierto su `S04`.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Piensen el planteamiento como un **embudo**: arriba, ancho, el estado actual del tema; y va cerrándose por evidencias, causas, consecuencias y vacío, hasta caer en un solo punto: su pregunta. Seis componentes, un embudo.”

> “**Slide 4 — ENFOQUE DE HOY.** La regla dura de hoy: **evidencia, no opinión**. 'Creo que muchos reprueban' no sirve; 'el 34 % reprobó según el reporte X de 2024' sí. Cada afirmación fuerte lleva una cifra o un estudio detrás. Aquí Google Académico deja de ser opcional.”

> “Y un truco para no bloquearse frente a la hoja en blanco: primero llenamos una **tabla síntoma / evidencia / consecuencia** y después la volvemos párrafos. La tabla piensa por ustedes.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** tabla síntoma / evidencia / consecuencia con 3 filas.

**GUION LITERAL:**
> “Modelo la tabla. Fila 1 — síntoma: 'la red del laboratorio se cae'; evidencia: 'la bitácora registra 12 caídas en un mes'; consecuencia: 'prácticas incompletas'. Lleno la fila 2 y la 3 igual.”

> “Ahora convierto la primera fila en prosa: 'Durante el último mes, la red del laboratorio X presentó doce interrupciones registradas en la bitácora institucional, lo que impidió completar prácticas programadas…'. ¿Ven? Del renglón salió el párrafo, y **cada dato tiene respaldo**.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~22 minutos. En `S05_Planteamiento_Apellido`: (1) llenen la tabla síntoma/evidencia/consecuencia con al menos tres filas; (2) conviértanla en un planteamiento de 1 a 1.5 páginas con los seis componentes; (3) al menos una afirmación debe apoyarse en un dato o estudio hallado en Google Académico. Que el texto termine en su pregunta.”

> “Criterio de éxito: leo su planteamiento y, sin conocer su tema, entiendo qué pasa, cómo lo sabe y por qué importa; y al final aparece la pregunta.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Escribe solo opiniones | “¿Qué dato o estudio respalda eso? Vamos a Scholar.” |
| Se va a la solución | “Todavía no: hoy argumentamos el problema.” |
| No cierra en la pregunta | “Reescriba el último párrafo para que caiga en su pregunta.” |
| Pone 10 causas sueltas | “Priorice 2–3 con evidencia; el resto quítelo.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el planteamiento es un embudo de seis componentes; (2) evidencia, no opinión; (3) todo termina en la pregunta.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S05_Planteamiento_Apellido` a CDigital y revisen allí la **fecha límite de recepción** de trabajos de este corte. La próxima sesión es la más práctica del curso: **bases de datos, gestores de citas y marco teórico** —traigan su planteamiento, porque el marco responde a esta misma pregunta.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs (`S05_Planteamiento_Apellido`): tabla síntoma/evidencia/consecuencia (3+ filas) + planteamiento de 1–1.5 páginas con los 6 componentes + 1 afirmación respaldada con dato de Scholar.",
    entregable="`S05_Planteamiento_Apellido` en CDigital.",
    ejemplo="Tabla síntoma/evidencia/consecuencia convertida en el primer párrafo del planteamiento, con la cifra de la bitácora como evidencia.",
    shots_demo=[
        ("inv_google_docs.png", "Google Docs — tabla síntoma / evidencia / consecuencia",
         "Llenar 3 filas en vivo; luego convertir la primera en prosa del planteamiento."),
    ],
    shots_taller=[
        ("inv_scholar_busqueda.png", "Google Académico — evidencia de respaldo",
         "Buscar 1 dato/estudio que sostenga el 'estado actual' (no la solución). Anotar en APA tentativa."),
    ],
)

_spec(
    "investigacion", 6,
    objetivos="""1. **Buscar** en bases y buscadores académicos (Google Académico, SciELO, Redalyc, biblioteca CUN) con operadores.
2. **Generar** citas en **APA 7** con ZoteroBib (en la nube, sin instalar) y pegarlas en Google Docs.
3. **Avanzar** el marco teórico / revisión: fichas de lectura y una página que responda a la pregunta.""",
    fundamento="""> Sesión combinada por periodo corto: reúne U8 (bases + gestores) y U10–U12 (posturas teóricas · marco · revisión). Es la sesión más "de laboratorio" del curso.

#### 1. Buscador ≠ base de datos (y cuándo usar cada uno)
- **Google Académico (Scholar):** buscador amplio; bueno para empezar y para el enlace "citado por".
- **SciELO y Redalyc:** bases de acceso abierto, fuertes en español/portugués y en Latinoamérica.
- **Biblioteca CUN (web, con login institucional):** acceso a bases suscritas; úsela para el texto completo.

Estrategia: empezar amplio en Scholar → afinar en SciELO/Redalyc → descargar el texto completo desde la biblioteca CUN.

#### 2. Operadores de búsqueda que ahorran horas
| Recurso | Para qué | Tip |
| :--- | :--- | :--- |
| Google Académico | Arranque amplio + "citado por" | Comillas "…" para la frase exacta |
| SciELO | Fuentes en español/portugués | Filtre por área y país |
| Redalyc | Revistas iberoamericanas abiertas | Contraste con lo hallado en Scholar |
| Biblioteca CUN (web) | Texto completo de bases suscritas | Requiere login institucional |
| ZoteroBib (zbib.org) | Generar APA 7 sin instalar | Pegue DOI → Copy → Docs |

Además: **AND/OR** para combinar o ampliar, y filtro por **año** (últimos 5 cuando el tema es tecnológico).

#### 3. Gestor de citas ligero: ZoteroBib (zbib.org)
ZoteroBib genera **APA 7** desde un DOI, ISBN o URL, **sin instalar nada** ni crear cuenta. Es la opción gratis-nube del curso: nada de Mendeley de escritorio ni plugins de Word.

#### 4. El marco teórico responde a la pregunta (no decora)
Un marco **no** es un collage de definiciones. Se organiza por **constructos** (los conceptos clave de su pregunta) y cada fuente entra porque **ayuda a responder**. Herramienta: la **ficha de lectura** = dato bibliográfico + idea principal + cita textual + cómo se relaciona con mi pregunta.""",
    errores=[
        ("“El marco es copiar y pegar definiciones.”",
         "No: se organiza por constructos y cada cita debe ayudar a responder la pregunta."),
        ("“Cito sin haber leído.”",
         "Se nota y es riesgo de plagio. Haga la ficha de lectura de cada fuente antes de citar."),
        ("“Uso Wikipedia y blogs como marco.”",
         "Orientan; el marco se sostiene en fuentes académicas: Scholar, SciELO, Redalyc, biblioteca CUN."),
        ("“Instalo Mendeley/Zotero de escritorio.”",
         "No hace falta: ZoteroBib en el navegador genera el APA 7 gratis."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Bases y gestores", 14),
        ("3️⃣ Criterios de selección de fuentes", 10),
        ("4️⃣ Taller de búsqueda + fichas", 22),
        ("5️⃣ Cierre del ciclo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 06, y es la más 'de laboratorio' del curso. Como estamos en periodo corto, combinamos tres unidades del Syllabus: bases de datos, gestores de citas y marco teórico. Todo con herramientas **gratis y en la nube** —nada de instalar programas—.”

> “**Slide 2 — OBJETIVOS.** Vamos a buscar bien, a citar en APA 7 con ZoteroBib y a avanzar una página de marco que responda a su pregunta. Tengan abierto su planteamiento de la Sesión 05: el marco es su continuación, no un tema nuevo.”""",
    fase2_texto="""**Protagonista:** Docente (demo en pantalla).

**En pantalla:** Google Académico, SciELO, Redalyc, biblioteca CUN (login) y ZoteroBib.

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Primero: no todo es Google normal. **Scholar** es un buscador amplio, ideal para arrancar y para el enlace 'citado por'. **SciELO** y **Redalyc** son bases de acceso abierto fuertes en español y en Latinoamérica. Y la **biblioteca CUN**, con su login institucional, les da el texto completo de bases suscritas.”

> “Operadores que ahorran horas: comillas para la frase exacta, AND/OR para combinar, filtro por año —en tecnología, últimos cinco—. Miren: busco 'pérdida de paquetes' AND laboratorio, filtro 2020 en adelante, y ya tengo resultados usables.”

> “**Slide 4 — ENFOQUE DE HOY.** Para citar no instalamos nada: **ZoteroBib**, en zbib.org. Pego un DOI o un título, me arma el APA 7 y lo copio a Google Docs. Cero Mendeley de escritorio, cero plugins.”""",
    fase3_texto="""**Protagonista:** Docente (modela una ficha de lectura).

**En pantalla (Google Docs):** plantilla de ficha de lectura.

**GUION LITERAL:**
> “El marco no es un collage de definiciones. Se organiza por **constructos**: los conceptos clave de su pregunta. Si mi pregunta habla de 'pérdida de paquetes' y 'prácticas de laboratorio', esos son mis dos constructos, y busco fuentes para cada uno.”

> “Modelo una **ficha de lectura**: dato bibliográfico en APA, idea principal en una frase, una cita textual con página y —lo más importante— **cómo se relaciona con mi pregunta**. Una fuente que no ayuda a responder, no entra. Así el marco queda al servicio de la pregunta, no de relleno.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~22 minutos. En `S06_MarcoRevision_Apellido`: (1) busquen en Scholar y en SciELO o Redalyc y elijan **5 fuentes** pertinentes; (2) hagan una **ficha de lectura** por fuente; (3) generen las 5 citas en APA 7 con ZoteroBib; (4) escriban una página de marco organizada por sus **constructos**, citando esas fuentes.”

> “Criterio de éxito: cada fuente responde a un constructo de su pregunta, las citas están en APA 7 y el marco no es un collage: se lee como argumento.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Solo usa Google normal | “Vaya a Scholar/SciELO/Redalyc; la biblioteca CUN da el texto completo.” |
| Cita sin leer | “Haga la ficha: idea principal + cómo se relaciona con su pregunta.” |
| Copia definiciones sueltas | “Agrúpelas por constructo: ¿esto responde a qué parte de su pregunta?” |
| Quiere instalar Mendeley | “No hace falta: ZoteroBib en el navegador genera el APA 7.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre del ciclo. Tres ideas: (1) busquen amplio en Scholar y afinen en SciELO, Redalyc y biblioteca CUN; (2) citen en APA 7 con ZoteroBib, sin instalar nada; (3) el marco responde a la pregunta, organizado por constructos.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S06_MarcoRevision_Apellido` a CDigital con sus 5 fichas y la página de marco. Con esto tienen el esqueleto del artículo: tema, línea, problema, pregunta, planteamiento y marco. Revisen en CDigital el detalle de la evaluación del corte final.”

> “**Slide 7 — Cierre.** Gracias por el trabajo de este periodo; mismo Meet si queda encuentro de cierre.”""",
    taller="En Google Docs (`S06_MarcoRevision_Apellido`): 5 fuentes de Scholar/SciELO/Redalyc + 1 ficha de lectura por fuente + 5 citas APA 7 con ZoteroBib + 1 página de marco organizada por constructos.",
    entregable="`S06_MarcoRevision_Apellido` en CDigital.",
    ejemplo="Flujo en pantalla: Scholar → ZoteroBib → pegar la referencia APA 7 en Google Docs, ubicándola bajo su constructo.",
    shots_demo=[
        ("Sesion 06/inv_google_scholar.png", "Google Académico",
         "Home de Scholar; explicar comillas, AND/OR y el enlace 'citado por'."),
        ("Sesion 06/inv_zoterobib.png", "ZoteroBib (zbib.org)",
         "Pegar DOI/título → APA 7 → Copy to clipboard → Google Docs. Sin instalar nada."),
        ("Sesion 06/inv_scielo.png", "SciELO",
         "Búsqueda en español/portugués; abrir 1 artículo de acceso abierto."),
    ],
    shots_taller=[
        ("Sesion 06/inv_redalyc.png", "Redalyc — complemento iberoamericano",
         "Segunda base abierta; contrastar con lo hallado en Scholar."),
        ("Sesion 06/inv_google_docs.png", "Google Docs — marco por constructos",
         "Pegar 5 referencias APA 7 y redactar la página de marco agrupada por constructos."),
    ],
)

# ----- TG2 (11 sesiones · sin Syllabus SIAC) -----
_spec(
    "tg2", 1,
    uso_texto="""> **Uso:** guion de la sesión de **encuadre**. Hoy **no se dicta tema**: se presenta el curso, el Docente, el grupo y las ACAs, y se deja por escrito el **acuerdo pedagógico**.
> El temario arranca en la **Sesión 02**; la **delimitación / reformulación del tema** queda como **lectura autónoma** de esta semana.
> Léalo en voz alta casi literal. **Duración: 60 minutos**.""",
    slides_map="""🗺️ **Slides de esta presentación** (deck de **encuadre**, 23 slides — no es el mapa del curso)

| Slide | Título en el PPTX | Fase |
| :---: | :--- | :---: |
| **1** | Portada — Sesión 01 | 1 |
| **2** | AGENDA DE HOY | 1 |
| **3** | Docente | 1 |
| **4** | PRESÉNTATE — ROMPEHIELOS (QR + Padlet) | 2 |
| **5** | LAS ACAs — QUÉ SE EVALÚA | 4 |
| **6** | Cómo trabajamos: TG2 es un taller de escritura | 3 |
| **7** | Aviso honesto sobre este curso (sin Syllabus SIAC) | 3 |
| **8–9** | Mapa del curso (1/2 y 2/2): los 11 encuentros | 3 |
| **10** | Qué se llevan al final: el avance escrito | 3 |
| **11** | El acuerdo pedagógico: qué pactamos hoy | 3 |
| **12** | Las ACAs, una por una | 4 |
| **13** | Cómo se entrega, paso a paso | 4 |
| **14** | Integridad académica | 4 |
| **15** | Inteligencia artificial generativa | 4 |
| **16** | Herramientas del curso | 4 |
| **17** | Cómo pedir ayuda | 4 |
| **18** | Acuerdos de convivencia | 5 |
| **19** | Preguntas frecuentes del primer día | 5 |
| **20** | Lo que debe tener listo para la Sesión 02 | 5 |
| **21** | ACUERDOS DE TRABAJO | 5 |
| **22** | PARA LA PRÓXIMA SESIÓN | 5 |
| **23** | Cierre — Sesión 01 | 5 |
""",
    objetivos="""1. **Encuadrar** TG2 como **continuación**: qué se hace en la hora sincrónica, qué en autónomo y cuál es el producto (**el avance escrito** que alimenta TG3).
2. **Presentar** al Docente y conocer el estado real de cada proyecto a través del Padlet.
3. **Explicar** las ACAs, la ruta de entrega en CDigital, la integridad académica y el uso de IA generativa.
4. **Dejar por escrito el acuerdo pedagógico** y encargar el trabajo autónomo: lectura sobre delimitación + matriz de estado del proyecto.""",
    fundamento_titulo="🧰 **Preparación del Docente ANTES de la clase** *(hoy no hay tema que estudiar: hay logística que dejar lista)*",
    fundamento="""> Recuerde el punto de partida de este grupo: **cada estudiante llega con un proyecto a medias**, congelado o mal delimitado, y casi ninguno tiene claro qué se espera de TG2. El encuadre debe responder esa ansiedad antes de que se convierta en deserción.

#### 1. Qué debe tener abierto y probado
| Qué | Para qué lo necesita hoy |
| :--- | :--- |
| Aula del curso en **CDigital**, con el espacio de entrega de la Sesión 01 creado | Va a proyectar dónde se sube el encargo autónomo |
| **Presentación del Curso** (`Clases/Presentacion del Curso - ….pptx`) | Slide **PRESÉNTATE** (QR + Padlet) y la logística del periodo |
| **Esta deck** (`Clases/Sesion 01 - …/Presentacion.pptx`) | Es el hilo de la hora: 23 slides, en orden |
| **Padlet oficial** abierto y probado | Rompehielos: aquí se diagnostica el estado del grupo |
| **Libro de calificaciones** del aula, en otra pestaña | De ahí salen los nombres, los tipos y los pesos que va a anunciar: los ítems se muestran, no se citan de memoria |
| Enunciado de la **ACA Final** (`Clases/Recursos/ACAs/`) | Única entrega documental del curso: la **fecha exacta vive ahí y en CDigital**, no en la deck |
| **Plantilla APA CUN** (`Clases/Recursos/`) | Mostrar en vivo cómo se abre en Google Docs |
| Texto del **acuerdo pedagógico** y el espacio donde va a quedar registrado en CDigital | Hoy se firma: no puede improvisarse al minuto 50 |
| **Meet** de la serie, 10 minutos antes · lista del grupo | Recibir, saludar por nombre y registrar asistencia |

#### 2. Qué NO se hace hoy
**No se dicta tema.** Si alguien pide ayuda con su delimitación, respóndale: *“esa es exactamente la lectura de esta semana; la abrimos en la Sesión 02 con su matriz de estado en la mano”*. Tampoco se revisan proyectos uno por uno hoy: no alcanza la hora y el encuadre se pierde.

#### 3. La honestidad que este curso exige
TG2 **no tiene Syllabus SIAC cargado**. El temario es orientativo (Manual del Docente + ruta de TG3) y los pesos 30/30/40 llevan asterisco. Dígalo con todas sus letras en la Slide 7: reconocerlo genera más confianza que fingir un temario oficial, y deja claro cuál es la fuente que manda (**CDigital**). Añada la regla operativa del grupo: **lunes festivo = clase autónoma**, no clase cancelada.

#### 4. Los tres mensajes que deben quedar grabados
1. **TG2 continúa, no empieza de cero**: y en trabajo de grado **solo cuenta lo escrito**.
2. **El producto es el avance consolidado** que en TG3 solo habrá que ejecutar y sustentar.
3. **Se entrega en CDigital**, con plantilla APA CUN, y lo acordado hoy queda por escrito.""",
    ejemplo_titulo="#### Qué proyectar en pantalla (y en qué orden)",
    ejemplo="""Deje **cinco pestañas** abiertas y páselas en este orden, sin buscar nada en vivo:
**1.** Padlet (rompehielos) → **2.** CDigital, en el espacio de entrega de la sesión → **3.** el **libro de calificaciones** del aula, para leer los ítems con su peso, y el enunciado de la **ACA Final** → **4.** plantilla APA CUN abierta en Google Docs → **5.** el espacio donde queda registrado el **acuerdo pedagógico**.
Modelar en vivo cómo se abre la plantilla y cómo se sube un archivo (un minuto) elimina la mitad de los correos de la primera semana.""",
    errores_titulo="#### Si un estudiante pregunta… (dudas reales del primer día)",
    errores_headers=("Si un estudiante pregunta…", "Usted responde…"),
    errores=[
        ("“¿Hoy no vamos a ver tema?”",
         "“Hoy es el encuadre: cómo trabajamos, qué se entrega y qué pactamos. Delimitar el tema es su lectura de esta semana y lo abrimos en la Sesión 02.”"),
        ("“¿Esto se pierde fácil?”",
         "“Se pierde por no entregar, casi nunca por escribir mal. El documento se corrige; la entrega que no llegó, no.”"),
        ("“¿Puedo trabajar solo o toca en grupo?”",
         "“Según lo que autorice el programa para su opción de grado. Consúltelo hoy y lo dejamos escrito en el acuerdo pedagógico, no a mitad de periodo.”"),
        ("“¿Puedo cambiar de tema por completo?”",
         "“Reformular sí, y hoy mismo: es afinar el foco. Cambiar de proyecto entero cuesta semanas que este periodo no tiene; solo por fuerza mayor y hablado conmigo.”"),
        ("“¿Me sirve lo que hice el semestre pasado?”",
         "“Sí, esa es justamente la idea: TG2 continúa. Pero se revisa, se actualiza y se cita si reutiliza fragmentos propios.”"),
        ("“Casi no tengo nada escrito, ¿arranco mal?”",
         "“No. Marque ‘inexistente’ con honestidad en su matriz: ese es su punto de partida real y con eso se puede planear. Lo que no sirve es el ‘más o menos’.”"),
        ("“¿Y si el lunes es festivo?”",
         "“La sesión no se cancela: es **clase autónoma**, con la actividad publicada en CDigital. Cuenta igual.”"),
        ("“¿La clase se graba?”",
         "Dígalo con claridad según lo que usted vaya a hacer, y aclare lo fijo: “el material y la consigna quedan siempre publicados en CDigital”."),
        ("“¿Puedo usar ChatGPT?”",
         "“Como apoyo sí, y se declara en una línea al final del documento. Verifique las referencias: inventa autores y DOIs. En TG3 usted defiende ese texto ante jurados.”"),
    ],
    fases=[
        ("1️⃣ Apertura, agenda y presentación del Docente", 10),
        ("2️⃣ Preséntate: rompehielos y diagnóstico en Padlet", 10),
        ("3️⃣ Recorrido del curso, producto final y acuerdo pedagógico", 15),
        ("4️⃣ Cómo se evalúa (quices, parciales y ACA Final), entrega e integridad", 17),
        ("5️⃣ Acuerdos, encargo autónomo y cierre", 8),
    ],
    fase_slides=[
        "Slides 1–3 (Portada · AGENDA · Docente)",
        "Slide 4 (PRESÉNTATE — Padlet)",
        "Slides 6–11 (cómo trabajamos · aviso honesto · mapa · producto · acuerdo)",
        "Slides 5 y 12–17 (evaluación real del aula · entrega · integridad · IA · herramientas · ayuda)",
        "Slides 18–23 (convivencia · dudas · Sesión 02 · acuerdos · cierre)",
    ],
    s01_padlet=True,
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Buenas tardes y bienvenidos a Trabajo de Grado 2. Nos vemos los lunes de cinco a seis, una hora sincrónica. Aclaro dos cosas de entrada. La primera: **hoy no vamos a ver tema**; hoy encuadramos el curso, vemos qué se entrega y pactamos cómo vamos a trabajar. La segunda, más importante: **este curso no empieza de cero**. Ustedes traen un proyecto, y mi trabajo es ayudarlos a llevarlo a un avance consolidado.”

> “**Slide 2 — AGENDA DE HOY.** El orden: les cuento cómo trabajamos y cuál es el producto; me presento; se presentan ustedes en un tablero; vemos las ACAs y cómo se entrega; y cerramos con los acuerdos y con la tarea de esta semana.”

> “**Slide 3 — Docente.** Un minuto sobre mí, para que sepan a quién le escriben.” [Preséntese con las credenciales de la slide y una frase sobre su experiencia dirigiendo trabajos de grado.] “Mi correo está en pantalla para novedades personales; lo académico va por CDigital, donde queda registro.”

**Cómo se maneja este arranque:** salude por nombre a quien va entrando. Y no arranque preguntando “¿cómo van con el proyecto?” en abierto: casi nadie confiesa un atraso por micrófono el primer día. Ese diagnóstico se hace por escrito, en el Padlet, que resulta mucho más cómodo.""",
    fase2_texto="""**Protagonista:** Estudiantes (Padlet) · Docente conduce.

**En pantalla:** Presentación del Curso → slide **PRESÉNTATE**, con el QR. URL: """ + PADLET_PRESENTACION_URL + """

**GUION LITERAL:**
> “**Slide 4 — PRESÉNTATE.** Quiero conocerlos y, sobre todo, saber en qué punto llega cada proyecto. En pantalla está el QR y el enlace; lo dejo también en el chat del Meet. Suban un post-it con (a) su nombre, (b) el tema de su proyecto en una frase y (c) el estado real en el que llega: ‘lo tengo casi listo’, ‘está congelado’, ‘quiero reformularlo’, ‘la verdad, no tengo casi nada’. Tienen unos siete minutos.”

> “Y les pido algo: **sean honestos**. Aquí nadie califica el post-it. Si usted dice que está en cero, yo sé por dónde empezar con usted; si dice que está listo y no lo está, perdemos las dos primeras semanas.”

> [Deje el tablero proyectado, ponga usted el primer post-it y lea tres o cuatro en voz alta, agradeciendo por nombre. Anote mentalmente el patrón del grupo: ¿mayoría congelados? ¿mayoría sin problema escrito? Eso le dice cómo dosificar las próximas sesiones.]

**Si nadie escribe** — pasa casi siempre el primer día virtual:
| Situación | Qué hace el Docente |
| :--- | :--- |
| Silencio total a los 2 minutos | Escribe un post-it de ejemplo con un caso típico (“tema amplio, sin pregunta escrita”) y lo narra en voz alta. |
| “No me abre el link” | Pega el URL otra vez en el chat y ofrece que lo digan por micrófono; usted lo transcribe. |
| Todos escriben “voy bien” | Repregunta en abierto: “¿quién tiene ya el planteamiento **escrito**, no pensado?”. El silencio es el diagnóstico. |
| Alguien confiesa que abandonó el proyecto | Agradece la honestidad en público y ofrece revisar el caso al terminar la sesión. |""",
    fase3_texto="""**Protagonista:** Docente (recorrido de la deck).

**GUION LITERAL:**
> “**Slide 6 — Cómo trabajamos.** Once encuentros de una hora. En una hora no se escribe un trabajo de grado oyendo hablar al profesor, así que el trato es: yo doy criterio y ejemplo en quince minutos, y el resto lo usamos para que ustedes escriban o corrijan **su** documento mientras yo paso revisando. Traigan siempre el documento abierto y la sección de la semana anterior ya escrita, aunque esté fea. Aquí hay un principio que voy a repetir todo el periodo: **solo cuenta lo escrito**.”

> “**Slide 7 — Aviso honesto.** Les debo una aclaración: esta asignatura **no tiene Syllabus SIAC cargado** en la carpeta del programa. El temario que van a ver es orientativo; lo construí con el Manual del Docente y con la ruta que sigue TG3. Los porcentajes 30, 30 y 40 son la regla general del reglamento y por eso llevan asterisco: la fuente que manda es **CDigital**. Si algo se ajusta, se los aviso ahí, no de palabra.”

> “**Slides 8 y 9 — Mapa del curso.** Miren las once sesiones y fíjense en la última columna: ninguna termina en apuntes, todas terminan en algo escrito. Y ojo con la nota: cuando un lunes sea festivo, esa sesión es **clase autónoma**, no clase cancelada; la actividad queda publicada en CDigital.”

> “**Slide 10 — Qué se llevan al final.** El producto de TG2 es **un solo documento**: planteamiento, pregunta, objetivos, marco referencial y metodología propuesta. Terminar TG2 no es terminar el trabajo de grado; es dejarlo listo para que en TG3 solo quede ejecutar y sustentar. Y sean claros con esto: aquí todavía **no hay resultados**; el trabajo de campo es de TG3.”

> “**Slide 11 — El acuerdo pedagógico.** Esto lo pactamos hoy y queda por escrito en CDigital: ritmo de una sección por sesión, formato con plantilla APA CUN en Google Docs, entrega por CDigital, festivo igual a clase autónoma, y retroalimentación sobre lo entregado. No es un trámite: es lo que invoco cuando alguien me diga ‘yo no sabía’. Léanlo antes de aceptarlo y pregunten ahora.”""",
    fase4_texto=f"""**Protagonista:** Docente, compartiendo pantalla (CDigital + libro de calificaciones + plantilla APA).

**GUION LITERAL:**
> “**Slide 5 — Cómo se evalúa TG2.** Volvamos a esta tabla, pero con los nombres que van a ver en el aula, que es lo que importa a la hora de la nota: **{items_corte_txt('tg2', 1)}** en el primer corte, **{items_corte_txt('tg2', 2)}** en el segundo y **{items_corte_txt('tg2', 3)}** en el tercero. Ojo con la lectura que suele hacerse mal: aquí **no hay tres trabajos escritos**; hay cuatro cuestionarios de plataforma, una sola entrega documental —la **ACA Final**— y dos actividades individuales de cierre.”

> “Y el dato que cambia cómo se organizan: los **cuestionarios suman {peso_tipo('tg2', KIND_CUESTIONARIO)} del curso**, y el **Parcial 1** solo vale {peso_item('tg2', 'parcial1')}. Un avance escrito impecable no compensa un parcial no presentado.”

> “**Slide 12 — ítem por ítem.** Los quices y los parciales **caen en día de clase**: se abren en el encuentro, tienen tiempo y cierran ese mismo día; el que falte ese día pierde el ítem, no lo ‘recupera después’. La **ACA Final** es el documento acumulativo: el mismo texto que venimos escribiendo, en PDF, subido a CDigital. La **autoevaluación** se diligencia y la **coevaluación** es un **foro**: se escribe en él, con criterio, o no cuenta.”

> “**Slide 13 — Cómo se entrega.** Puro procedimiento, y les ahorra sustos.” [Hágalo en vivo: abra la plantilla APA CUN en Google Docs, muestre el nombre `SNN_Tema_Apellido`, descargue como PDF y abra el espacio de entrega en CDigital.] “Y una regla de TG2: **trabajen siempre sobre el mismo documento**. Aquí se evalúa un texto que crece, no una carpeta de archivos sueltos.”

> “**Slide 14 — Integridad académica.** En trabajo de grado esto se revisa de verdad. Todo lo que no es suyo se cita en APA 7, incluidos los fragmentos de su propio trabajo anterior: reutilizarlos sin declararlo es **autoplagio**. En TG3 la entrega pasa por la revisión de similitud institucional del aula, y allá el Docente confirma cómo opera; así que el hábito lo corregimos aquí. Y el consejo práctico: anoten la fuente en el instante en que pegan algo; en un documento que crece seis meses, reconstruirla después es imposible.”

> “**Slide 15 — Inteligencia artificial.** Hablemos claro. Sí se puede usar para entender un concepto, ordenar una sección o pulir un párrafo que ustedes ya escribieron. Se declara en una línea al final. Y verifiquen cada referencia, porque estas herramientas inventan autores y DOIs. Piensen en el semestre que viene: en TG3 hay sustentación ante jurados, y un párrafo que usted no pueda explicar en voz alta le va a costar caro.”

> “**Slide 16 — Herramientas.** Todas gratis y en el navegador: Docs, Google Académico, SciELO, Redalyc, biblioteca CUN, ZoteroBib para las citas, Excalidraw para diagramar y CDigital para entregar. No hay que instalar ni comprar nada.”

> “**Slide 17 — Cómo pedir ayuda.** Foro de CDigital para lo académico, correo para lo personal, respuesta en días hábiles y siempre antes del siguiente encuentro. Y pidan ayuda **con el texto en la mano**: miren los dos ejemplos de la slide.”""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “**Slides 18 y 19 — Convivencia y dudas frecuentes.** Dos minutos: empezamos a la hora, micrófono apagado mientras alguien expone, y compartir pantalla es parte del curso —vamos a proyectar borradores reales, y aquí nadie se burla de un texto a medio hacer, porque todos estamos mostrando lo mismo—. En la siguiente slide están las dudas que siempre salen el primer día.”

> “**Slide 20 — Lo que debe tener listo para la Sesión 02.** La tarea es doble. Primero, la **lectura autónoma** sobre delimitación y reformulación del tema, publicada en CDigital. Segundo, y esto es lo que quiero ver: hagan el inventario de su proyecto en un Doc llamado `S01_EstadoProyecto_Apellido`. Una **matriz de estado** donde cada sección —tema, problema, objetivos, marco, metodología— se marca como **lista, a medias o inexistente**, con la **evidencia** pegada: el párrafo o el enlace. Más su **tema delimitado en una sola frase** y **tres compromisos** suyos para las próximas dos semanas.”

> “Y les repito: ‘a medias’ e ‘inexistente’ son respuestas válidas y honestas. Lo único que no me sirve es ‘más o menos’ sin nada escrito debajo.”

> “**Slides 21 y 22 — Acuerdos y para la próxima.** Resumo el trato: se entrega en CDigital, se trae el avance escrito y se cita en APA 7.”

> “**Slide 23 — Cierre.** Ya saben qué vamos a hacer, cómo se evalúa y qué pactamos. La próxima sesión abrimos con sus matrices en pantalla y convertimos ese tema en pregunta, objetivos y título. Recuerden: si un lunes cae festivo, esa sesión es autónoma; el resto nos vemos en el mismo Meet.”""",
    entregable_titulo="🧩 **Encargo autónomo (para la Sesión 02)**",
    taller="**No se hace en clase, es trabajo autónomo:** leer el material sobre **delimitación / reformulación del tema** publicado en CDigital; y llenar en Google Docs la **matriz de estado** del proyecto (sección · lista/a medias/inexistente · evidencia), el **tema delimitado** en una frase (actor + fenómeno + contexto) y **3 compromisos** para las próximas dos semanas.",
    entregable="`S01_EstadoProyecto_Apellido` (Google Doc o PDF), **antes de la Sesión 02**.",
    checklist=[
        "- [ ] Aula del curso en **CDigital** abierta, con el espacio de entrega de la Sesión 01 creado",
        "- [ ] **Lectura autónoma sobre delimitación del tema publicada en CDigital** (sin eso el encargo no se puede cumplir)",
        "- [ ] Texto del **acuerdo pedagógico** listo y el sitio donde quedará registrado (hoy se firma)",
        "- [ ] **Padlet** oficial probado y el link listo para pegar en el chat: " + PADLET_PRESENTACION_URL,
        "- [ ] **Presentación del Curso** abierta en la slide PRESÉNTATE (QR)",
        "- [ ] Deck de hoy abierta (`Presentacion.pptx` de la Sesión 01 — 23 slides)",
        "- [ ] **Libro de calificaciones** del aula abierto (ítems, tipos y pesos reales) y enunciado de la **ACA Final** listo para proyectar",
        "- [ ] **Plantilla APA CUN** lista para mostrar en Google Docs",
        "- [ ] Verificado qué lunes del periodo caen en festivo (esas sesiones son **clase autónoma**)",
        "- [ ] Meet de la serie abierto **10 minutos antes** (enlace en la ficha de arriba) · lista del grupo a la mano",
    ],
    shots_fase2=[
        ("Sesion 01/tg_padlet.png", "Padlet — Preséntate / estado del proyecto",
         "Tablero de la Presentación del Curso. Consigna: nombre + tema en una frase + estado real del proyecto (~7 min). Lea 3–4 en voz alta."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib (zbib.org) — citar sin instalar nada",
         "Muestre 30 segundos: pegar un DOI o título → APA 7 → copiar al Doc. Es la respuesta a “¿con qué gestor de citas trabajamos?”."),
    ],
)

_spec(
    "tg2", 2,
    objetivos="""1. **Lograr:** Redactar pregunta, objetivos y título provisional.
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Núcleo del avance de grado: si la pregunta y los objetivos quedan bien, casi todo el documento se ordena solo. Este apartado le da los criterios para corregir en vivo.

#### 1. La pregunta gobierna el documento
La **pregunta de investigación** es la brújula: todo lo que entre después —marco, método, resultados— debe existir para responderla. Una buena pregunta es clara, delimitada (actor + contexto), viable (hay datos y fuentes) y **no se responde con sí o no**. En Ingeniería de Sistemas suele apuntar a un "cómo", un "en qué medida" o un "qué relación".

#### 2. Objetivos: general y específicos, con verbos medibles
El **objetivo general** es la pregunta convertida en propósito; los **específicos** son los pasos para llegar. La clave son los **verbos**: se evita "conocer", "entender" o "aprender" (no se pueden medir) y se usan verbos observables.

| Evite (no medible) | Prefiera (medible) |
| :--- | :--- |
| Conocer | Identificar, caracterizar |
| Entender | Analizar, comparar |
| Aprender sobre | Describir, clasificar |
| Ver / mirar | Evaluar, medir |
| Profundizar | Diseñar, proponer |

Regla práctica: 1 general + 3 específicos. Cada específico debería poder convertirse en una sección del documento. Y **coherencia vertical**: los específicos, sumados, responden al general; el general responde a la pregunta.

#### 3. El título provisional
Título tentativo ≤ 21 palabras, sin eslóganes: debe dejar ver el actor, el fenómeno y el contexto. "Una solución innovadora con IA" no es título; "Clasificación automática de tickets de soporte mediante aprendizaje supervisado en la mesa de ayuda de la empresa X" sí. Es provisional: se ajusta al cierre del curso.""",
    errores=[
        ("“Mi objetivo es ‘conocer sobre’ el machine learning.”",
         "‘Conocer’ no se mide. Cámbielo por identificar, caracterizar o analizar algo concreto."),
        ("“¿Sirve la IA para la empresa? — como pregunta.”",
         "Es de sí/no. Reformule con ‘en qué medida’ o ‘qué relación’, y con actor + contexto."),
        ("“Tengo 6 objetivos específicos.”",
         "Se dispersa. Deje 3 que, sumados, respondan al general; cada uno será una sección."),
        ("“El título es un eslogan bonito.”",
         "El título muestra actor, fenómeno y contexto en ≤ 21 palabras, no vende."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Buenas tardes. Sesión 02. La semana pasada dejamos el proyecto diagnosticado y el tema delimitado; y el lunes pasado, al ser festivo, tuvieron clase autónoma, así que espero que hayan avanzado su matriz. Hoy le ponemos el esqueleto al avance: **pregunta, objetivos y título**.”

> “**Slide 2 — OBJETIVOS.** Salimos con tres cosas escritas: una pregunta investigable, un objetivo general con tres específicos, y un título provisional. Tengan abierto su `S01` con el tema delimitado, porque de ahí sale todo.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** La pregunta de investigación es la **brújula** del documento. Todo lo que escriban después —marco, método, resultados— existe para responderla. Una buena pregunta es clara, delimitada, viable y no se contesta con sí o no. Nada de ‘¿sirve la IA?’; sí a ‘¿en qué medida un clasificador supervisado reduce el tiempo de atención de tickets en la mesa de ayuda de la empresa X?’.”

> “Ahora los objetivos. El **general** es la pregunta hecha propósito; los **específicos** son los pasos. Y aquí la regla dura del día: **verbos medibles**. Borren ‘conocer’, ‘entender’, ‘aprender’: no se pueden evaluar. Usen identificar, caracterizar, analizar, diseñar, evaluar. Un general y tres específicos; cada específico será después una sección del documento.”

> “**Slide 4 — ENFOQUE DE HOY.** Y el título provisional: máximo 21 palabras, sin eslóganes. Debe verse el actor, el fenómeno y el contexto. Es provisional; lo afinamos al cierre.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** bloque con Pregunta / Objetivo general / 3 específicos / Título.

**GUION LITERAL:**
> “Modelo en vivo con el caso de los tickets. Pregunta: ‘¿en qué medida un modelo de clasificación supervisada reduce el tiempo de clasificación de tickets de soporte en la mesa de ayuda de la empresa X?’. De ahí saco el **general**: ‘Evaluar el efecto de un modelo de clasificación supervisada sobre el tiempo de clasificación de tickets…’. Fíjense: la pregunta y el general dicen lo mismo, uno en interrogación y otro en propósito.”

> “Ahora los tres específicos, con verbos medibles: (1) **caracterizar** el flujo actual de tickets; (2) **diseñar** el modelo de clasificación; (3) **comparar** el tiempo con y sin el modelo. Sumo mentalmente: los tres responden al general. Eso es **coherencia vertical**. Y abro Google Académico un momento para confirmar cómo nombran los autores ‘clasificación de tickets’ —eso me da el vocabulario del título—.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S02_PreguntaObjetivos_Apellido`: (1) escriban la **pregunta** en una sola frase investigable; (2) un **objetivo general** que la refleje; (3) **tres específicos** con verbos medibles; (4) un **título provisional** ≤ 21 palabras. Revisen la coherencia vertical: ¿los específicos suman al general? ¿el general responde la pregunta?”

> “Criterio de éxito: si tapo la pregunta y leo solo los objetivos, puedo reconstruir qué se va a investigar.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Usa "conocer/entender" | “Cámbielo por un verbo que yo pueda medir: identificar, diseñar, comparar.” |
| Pregunta de sí/no | “Reformule con ‘en qué medida’, ‘cómo’ o ‘qué relación’.” |
| Objetivos que no suman al general | “Reordene: cada específico es un paso hacia el general, no un tema aparte.” |
| Título tipo eslogan | “Muéstreme actor, fenómeno y contexto; quite el adjetivo publicitario.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) la pregunta es la brújula y no se responde con sí/no; (2) los objetivos llevan **verbos medibles** y guardan coherencia vertical; (3) el título muestra actor, fenómeno y contexto.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S02_PreguntaObjetivos_Apellido` a CDigital. La próxima sesión tomamos este esqueleto y vemos **la estructura completa del documento de avance** con la Plantilla APA CUN: qué sección va dónde.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet el próximo lunes.”""",
    taller="En Google Docs (`S02_PreguntaObjetivos_Apellido`): pregunta investigable + objetivo general + 3 específicos con verbos medibles + título provisional ≤ 21 palabras, con coherencia vertical.",
    entregable="`S02_PreguntaObjetivos_Apellido` en CDigital.",
    ejemplo="Pregunta ‘¿en qué medida un clasificador supervisado reduce el tiempo de atención de tickets en la empresa X?’ → general con ‘evaluar’ + específicos ‘caracterizar / diseñar / comparar’.",
    shots_demo=[
        ("tg_scholar.png", "Scholar — vocabulario de la pregunta",
         "Extraer 3 términos del fenómeno para nombrar bien la pregunta y el título."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib",
         "1 referencia que sostenga la pertinencia del problema."),
    ],
)

_spec(
    "tg2", 3,
    objetivos="""1. **Lograr:** Dominar la estructura del artículo / documento de avance (plantilla APA CUN).
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Hoy no se escribe contenido nuevo: se ordena el envase. El estudiante debe salir sabiendo **qué va en cada sección** de la Plantilla APA CUN y qué NO va.

#### 1. La plantilla APA CUN es el mapa
El documento de avance sigue la **Plantilla APA CUN de proyecto de grado** (se abre en Google Docs; no exige Word de escritorio). Su valor es que ya trae el orden de las secciones y el formato de citas; el estudiante no inventa la estructura, la **llena**.

#### 2. Qué va en cada sección (y qué no)
| Sección | Qué va | Error típico |
| :--- | :--- | :--- |
| Introducción | Contexto → problema → propósito | Arrancar "desde la antigüedad…" |
| Planteamiento y pregunta | El problema argumentado + la pregunta | Meter la solución aquí |
| Objetivos | General + específicos | Verbos no medibles |
| Marco referencial | Antecedentes + teoría + conceptos | Collage de definiciones |
| Diseño metodológico | Enfoque, tipo, alcance, instrumentos | Mezclar con resultados |
| Referencias | APA 7, todo lo citado | URLs sueltas sin formato |

#### 3. El error rey: mezclar método y resultados
En un avance de TG2 casi nunca hay resultados todavía —el trabajo de campo es de TG3—. Por eso la metodología va en **futuro/propuesto** ("se aplicará", "se propone") y NO se cuela ningún hallazgo. Confundir "lo que voy a hacer" con "lo que encontré" es el error que más desordena el documento.

#### 4. Outline antes que prosa
Escribir directo a párrafo produce bloqueo. La técnica es hacer primero un **outline**: cada sección con 3–5 viñetas de lo que irá. El outline se revisa rápido y evita reescribir páginas enteras.""",
    errores=[
        ("“Escribo directo en párrafos, sin plan.”",
         "Primero el outline: 3–5 viñetas por sección; luego se convierte en prosa."),
        ("“Pongo mis resultados en la metodología.”",
         "En TG2 aún no hay resultados: la metodología va en ‘propuesto/se aplicará’, sin hallazgos."),
        ("“Invento el orden de las secciones.”",
         "La estructura ya existe: use la Plantilla APA CUN y llénela; no reinvente el mapa."),
        ("“La introducción arranca con la historia de la humanidad.”",
         "Arranque en el contexto real del problema: contexto → problema → propósito."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 03. Ya tienen tema, pregunta y objetivos. Hoy **no** escribimos contenido nuevo: ordenamos el envase. Al terminar deben saber qué va en cada sección del documento y, sobre todo, qué **no** va.”

> “**Slide 2 — OBJETIVOS.** Dominar la estructura de la Plantilla APA CUN y salir con un **outline** de todo el documento: cada sección con viñetas de lo que irá. Tengan abierto su `S02`.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Buena noticia: ustedes **no** inventan la estructura. La **Plantilla APA CUN** ya trae el orden y el formato; se abre en Google Docs, no necesitan Word de escritorio. Su trabajo es **llenarla**, no diseñarla.”

> “Recorramos qué va en cada sección: la introducción es contexto → problema → propósito; el planteamiento argumenta el problema y aterriza en la pregunta; los objetivos ya los tienen; el marco referencial junta antecedentes, teoría y conceptos; el diseño metodológico dice enfoque, tipo y alcance; y las referencias van en APA 7.”

> “**Slide 4 — ENFOQUE DE HOY.** Y ahora el **error rey** de TG2: mezclar método y resultados. En este curso casi nunca hay resultados —el campo es de TG3—. Por eso la metodología se escribe en **propuesto**: ‘se aplicará’, ‘se propone’. Si aparece un hallazgo en la sección de método, algo está fuera de lugar.”""",
    fase3_texto="""**Protagonista:** Docente (modela en pantalla).

**En pantalla (Google Docs / Plantilla APA CUN):** abra la plantilla y muestre las secciones; en un Doc aparte arme el outline.

**GUION LITERAL:**
> “Abro la Plantilla APA CUN en Google Docs para que vean el mapa real: portada, introducción, planteamiento, objetivos, marco, metodología, referencias. No toco el formato; solo miro el orden.”

> “Ahora modelo el **outline** con el caso de los tickets. Introducción: viñeta 1, contexto de la mesa de ayuda; viñeta 2, el problema de tiempos; viñeta 3, propósito. Metodología: viñeta 1, enfoque cuantitativo; viñeta 2, ‘se propone’ medir tiempos antes/después. Fíjense que escribo ‘se propone’, en futuro, y **no** meto ningún número de resultado. Con este esqueleto de viñetas, la próxima vez que escriban no van a mirar la hoja en blanco.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. Abran una copia de la **Plantilla APA CUN** en Google Docs y, en `S03_EstructuraAvance_Apellido`, hagan el **outline** completo: cada sección del documento con 3–5 viñetas de lo que irá. En metodología, escriban en ‘propuesto/se aplicará’. Marquen con color las secciones que hoy están vacías.”

> “Criterio de éxito: leo su outline y entiendo el documento entero de un vistazo, sin que haya un solo resultado colado en la metodología.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Quiere escribir párrafos ya | “Hoy solo viñetas; la prosa viene en las próximas sesiones.” |
| Mete resultados en método | “Todavía no hay campo: escríbalo como ‘se aplicará’.” |
| No sabe qué va en una sección | “Vuelva a la tabla del fundamento: ¿esta sección responde a qué?” |
| Reordena las secciones | “Respete el orden de la plantilla APA CUN; no lo reinvente.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) la estructura ya existe en la Plantilla APA CUN, ustedes la llenan; (2) el error rey es mezclar método y resultados —en TG2 el método va en ‘propuesto’—; (3) el outline evita la hoja en blanco.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S03_EstructuraAvance_Apellido` con el outline y la plantilla copiada. La próxima sesión empezamos a llenar de verdad: **antecedentes y referentes (Fase I)**, buscando en bases CUN y Scholar.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs (`S03_EstructuraAvance_Apellido`): copia de la Plantilla APA CUN + outline completo del documento (3–5 viñetas por sección), con la metodología en ‘propuesto’ y las secciones vacías marcadas.",
    entregable="`S03_EstructuraAvance_Apellido` en CDigital.",
    ejemplo="Outline sobre la plantilla APA CUN: introducción (contexto/problema/propósito) y metodología escrita en ‘se propone’, sin resultados.",
    shots_demo=[
        ("tg_scholar.png", "Plantilla APA CUN en Google Docs",
         "Abrir la Plantilla_APA_CUN_Proyecto de grado en Google Docs (nube); recorrer el orden de secciones."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib — bloque de referencias",
         "Dejar la sección de referencias lista en APA para ir llenándola."),
    ],
)

_spec(
    "tg2", 4,
    objetivos="""1. **Lograr:** Construir antecedentes y referentes (Fase I).
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Sesión muy de "escritura académica". Aquí conviene apoyarse en la guía transversal `Guiones/Guía práctica - Herramientas de escritura y citación.md`, que trae el flujo Scholar → ZoteroBib → Docs paso a paso; no lo repita entero, remita a ella.

#### 1. Antecedentes ≠ marco teórico
Los **antecedentes** son estudios previos que ya abordaron un problema parecido al suyo: qué hicieron, cómo y qué encontraron. No son definiciones (eso es marco conceptual) ni teoría de fondo (marco teórico): son **precedentes**. Sirven para mostrar que su problema es real y para no repetir lo ya hecho.

#### 2. La ficha de antecedente
Cada antecedente se resume en una **ficha**: dato bibliográfico en APA, objetivo del estudio, método, hallazgo principal y —lo más importante— **qué aporta a mi proyecto**. Sin esa última línea, la ficha es decorativa.

| Campo de la ficha | Pregunta que responde |
| :--- | :--- |
| Referencia APA 7 | ¿De dónde es? |
| Objetivo del estudio | ¿Qué buscaban? |
| Método | ¿Cómo lo hicieron? |
| Hallazgo principal | ¿Qué encontraron? |
| Aporte a mi proyecto | ¿Para qué me sirve a mí? |

#### 3. Mezcla nacional e internacional
Un buen bloque de antecedentes combina fuentes **nacionales/locales** (que muestran pertinencia en el contexto colombiano) e **internacionales** (que traen el estado del arte global). Buscar solo en español limita; buscar solo en inglés desconecta del contexto.

#### 4. El párrafo puente
Las fichas no se pegan crudas en el documento: se hilan con un **párrafo puente** que dice qué tienen en común, en qué difieren y qué vacío dejan —vacío que su proyecto viene a llenar—. Ese párrafo es lo que convierte una lista en argumento.""",
    errores=[
        ("“Pego el resumen del paper tal cual.”",
         "Haga la ficha con SUS palabras y agregue la línea ‘qué aporta a mi proyecto’."),
        ("“Solo busco en español (o solo en inglés).”",
         "Combine nacional e internacional: local da pertinencia, global da estado del arte."),
        ("“Antecedentes y marco teórico son lo mismo.”",
         "No: antecedentes son estudios previos parecidos; el marco es la teoría de fondo."),
        ("“Cito 8 estudios sin conectarlos.”",
         "Agréguelos con un párrafo puente: qué comparten, en qué difieren, qué vacío dejan."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 04. Ya tenemos el envase; hoy empezamos a llenarlo con lo primero del marco: los **antecedentes**. Es decir, quién ya trabajó algo parecido a lo suyo y qué encontró.”

> “**Slide 2 — OBJETIVOS.** Salir con al menos cuatro fichas de antecedentes bien hechas y un párrafo que las hile. Para el flujo de búsqueda y citación nos apoyamos en la **guía práctica de herramientas** que está en la carpeta Guiones; no repito todo el paso a paso de ZoteroBib, lo tienen ahí.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Cuidado con una confusión clásica: **antecedentes no es marco teórico**. Los antecedentes son **estudios previos** parecidos al suyo —qué hicieron, cómo y qué hallaron—. La teoría de fondo y las definiciones vienen después. Sirven para dos cosas: mostrar que su problema es real y no reinventar lo ya hecho.”

> “Cada antecedente se guarda en una **ficha**: referencia APA, objetivo, método, hallazgo y —la línea que nunca puede faltar— **qué aporta a mi proyecto**. Si esa línea no está, la ficha es adorno.”

> “**Slide 4 — ENFOQUE DE HOY.** Y busquen mezclando: algo **nacional o local**, que muestre pertinencia en Colombia, y algo **internacional**, que traiga el estado del arte. Usen Google Académico y las bases de la biblioteca CUN con su login. El flujo de citas en APA 7 lo tienen en la guía de herramientas.”""",
    fase3_texto="""**Protagonista:** Docente (modela en pantalla).

**En pantalla (Google Académico + Google Docs):** una búsqueda y una ficha llenándose.

**GUION LITERAL:**
> “Modelo la búsqueda. En Google Académico escribo tres palabras de mi pregunta —‘clasificación tickets soporte’— con comillas en la frase exacta y filtro los últimos cinco años. Abro un resultado que se parezca a mi caso. No leo entero: leo el resumen y las conclusiones para ver si sirve.”

> “Ahora lleno la **ficha** en Google Docs: referencia (la genero en ZoteroBib como dice la guía), objetivo del estudio, método, hallazgo y la línea de oro: ‘me aporta el modelo de medición de tiempos que puedo adaptar’. Repito con una fuente internacional y una local. Y al final escribo el **párrafo puente**: ‘estos estudios coinciden en X, difieren en Y, y ninguno abordó una mesa de ayuda local —ahí entra mi proyecto—’.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S04_Antecedentes_Apellido`: (1) busquen y elijan **4 antecedentes** —al menos uno nacional y uno internacional—; (2) hagan una **ficha** por cada uno con los cinco campos, sin copiar el resumen; (3) generen las referencias en APA 7 con ZoteroBib (guía de herramientas); (4) escriban un **párrafo puente** que las hile y muestre el vacío.”

> “Criterio de éxito: cada ficha tiene su línea de ‘qué me aporta’, y el párrafo puente convierte la lista en argumento.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Copia el abstract literal | “Resúmalo con sus palabras y agregue ‘qué me aporta’.” |
| Solo halla fuentes en español | “Busque en inglés con términos técnicos; luego lo integramos.” |
| Confunde antecedente con teoría | “¿Es un estudio previo parecido? Entonces es antecedente.” |
| Deja las fichas sueltas | “Escriba el párrafo puente: común, diferencia, vacío.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) antecedentes son estudios previos, no teoría de fondo; (2) cada ficha lleva ‘qué me aporta’; (3) el párrafo puente hila las fichas y muestra el vacío que su proyecto llena.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S04_Antecedentes_Apellido` con las 4 fichas y el párrafo puente. La próxima sesión pasamos de los estudios previos a la **teoría de fondo**: el marco teórico organizado por constructos.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs (`S04_Antecedentes_Apellido`): 4 fichas de antecedentes (≥1 nacional, ≥1 internacional) con los 5 campos + referencias APA 7 con ZoteroBib + párrafo puente. Flujo de citación: guía transversal de herramientas.",
    entregable="`S04_Antecedentes_Apellido` en CDigital.",
    ejemplo="Ficha con la línea ‘qué me aporta’ + párrafo puente: ‘coinciden en X, difieren en Y, ninguno abordó una mesa de ayuda local → ahí entra mi proyecto’.",
    shots_demo=[
        ("Herramientas/tg_scholar.png", "Google Académico",
         "Búsqueda con 3–5 palabras de la pregunta; comillas para la frase exacta; guardar 4 títulos (≥1 nacional, ≥1 internacional)."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib — APA de las 4 fichas",
         "Convertir a APA 7 y pegar en Docs. Paso a paso: guía transversal de herramientas."),
    ],
)

_spec(
    "tg2", 5,
    objetivos="""1. **Lograr:** Avanzar marco teórico usable.
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> El marco teórico es donde más se "rellena" por miedo. Su trabajo es enseñar a que cada cita **trabaje**, no adorne.

#### 1. El marco responde a la pregunta (no decora)
Un marco teórico **no** es un collage de definiciones bonitas. Es el conjunto de teorías y conceptos que hacen falta para **entender y responder su pregunta**. Si una cita no ayuda a responder, sobra —por prestigiosa que sea—.

#### 2. Se organiza por constructos
Un **constructo** es un concepto clave de su pregunta. En "clasificación de tickets con IA", los constructos son "clasificación supervisada", "gestión de mesa de ayuda" y "tiempo de atención". El marco se ordena **por constructo**, no por autor ni cronológicamente: para cada constructo, qué dicen las fuentes.

| Constructo | Fuentes que lo tratan | Para qué lo necesito |
| :--- | :--- | :--- |
| Clasificación supervisada | 2–3 fuentes | Fundamenta el método |
| Gestión de mesa de ayuda | 1–2 fuentes | Da contexto del proceso |
| Tiempo de atención | 1–2 fuentes | Define la variable a medir |

#### 3. Regla de los 3 constructos
En un avance de TG2, tres constructos bien desarrollados valen más que ocho superficiales. Más de tres suele significar que el estudiante no delimitó la pregunta. Menos de dos, que se quedó corto.

#### 4. Parafraseo con cita, no copia
Cada idea de otro autor se parafrasea y se cita en APA 7; la cita textual es la excepción (para definiciones clave), siempre con página. Copiar sin citar es plagio, y en TG3 la entrega pasa por la revisión de similitud institucional del aula; se corrige el hábito ahora.""",
    errores=[
        ("“El marco es pegar todas las definiciones que encuentre.”",
         "No: cada cita debe ayudar a responder la pregunta; si no, sobra."),
        ("“Organizo el marco autor por autor.”",
         "Organícelo por constructos: para cada concepto clave, qué dicen las fuentes."),
        ("“Tengo 8 constructos.”",
         "Se dispersó. Delimite a 3 constructos que salgan directo de su pregunta."),
        ("“Copio párrafos y luego ‘ya veré si cito’.”",
         "Parafrasee y cite en APA 7 desde ya; en TG3 hay antiplagio institucional."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 05. La semana pasada vimos quién ya trabajó algo parecido —los antecedentes—. Hoy vamos a la **teoría de fondo**: el marco teórico. Es la sección que más miedo da y donde más se rellena; vamos a evitar eso.”

> “**Slide 2 — OBJETIVOS.** Salir con un mapa de constructos y una a dos páginas de marco donde **cada cita trabaje**. Tengan abierta su pregunta del `S02` y sus fichas del `S04`.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** La primera regla del marco: **no es un collage de definiciones**. Es la teoría que ustedes necesitan para responder su pregunta. Si una cita no ayuda a responderla, sobra, aunque sea de un autor famoso.”

> “¿Cómo se ordena? Por **constructos**. Un constructo es un concepto clave de su pregunta. En el caso de los tickets, los constructos son ‘clasificación supervisada’, ‘gestión de mesa de ayuda’ y ‘tiempo de atención’. El marco se arma constructo por constructo, no autor por autor.”

> “**Slide 4 — ENFOQUE DE HOY.** Y una regla práctica: **tres constructos**. Tres bien hilados valen más que ocho superficiales. Si les salen ocho, no delimitaron la pregunta. Además: todo se parafrasea y se cita en APA 7; copiar sin citar es plagio, y en TG3 hay antiplagio institucional. El hábito se corrige ahora.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** mapa de constructos y un párrafo de marco.

**GUION LITERAL:**
> “Modelo el mapa. Escribo mis tres constructos como subtítulos. Debajo de ‘clasificación supervisada’ pongo las dos fuentes que la explican y, al lado, ‘para qué la necesito’: fundamenta mi método. Repito con los otros dos. Ese mapa es el esqueleto del marco.”

> “Ahora convierto un constructo en párrafo, parafraseando: ‘La clasificación supervisada consiste en… (Autor, 2023), y se ha usado para… (Autor, 2022). En este proyecto sirve para…’. Fíjense: cada oración tiene su cita, y la última frase conecta la teoría con **mi** pregunta. Eso es un marco que trabaja, no que adorna.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S05_MarcoTeorico_Apellido`: (1) definan sus **3 constructos** a partir de la pregunta; (2) hagan el **mapa** constructo → fuentes → para qué lo necesito; (3) redacten **1 a 2 páginas** de marco parafraseando y citando en APA 7, cerrando cada constructo con su conexión a la pregunta.”

> “Criterio de éxito: leo su marco y cada párrafo tiene cita y termina conectando con su pregunta; no hay definición suelta que no sirva.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Pega definiciones sin conectar | “¿Esto responde a qué parte de su pregunta? Si a ninguna, quítelo.” |
| Ordena por autor | “Reagrupe por constructo: ¿de qué concepto habla cada fuente?” |
| Tiene 7 constructos | “Vuelva a la pregunta y quédese con los 3 conceptos centrales.” |
| Copia sin citar | “Parafrasee y ponga (Autor, año); genere el APA en ZoteroBib.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el marco responde a la pregunta, no decora; (2) se organiza por **constructos**, tres bien hilados; (3) todo se parafrasea y se cita en APA 7.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S05_MarcoTeorico_Apellido` con el mapa y el avance de marco. La próxima sesión completamos el marco referencial con lo **conceptual y lo contextual**: las definiciones operativas y el contexto real de su proyecto.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs (`S05_MarcoTeorico_Apellido`): 3 constructos derivados de la pregunta + mapa (constructo → fuentes → para qué) + 1–2 páginas de marco parafraseado y citado en APA 7, cada constructo conectado a la pregunta.",
    entregable="`S05_MarcoTeorico_Apellido` en CDigital.",
    ejemplo="Constructos ‘clasificación supervisada / gestión de mesa de ayuda / tiempo de atención’, cada párrafo con cita y cierre que conecta con la pregunta.",
    shots_demo=[
        ("tg_scholar.png", "Scholar — buscar por constructo",
         "Buscar por cada constructo por separado, no por ‘todo el tema’."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib",
         "Citas de los 3 constructos en APA 7."),
    ],
)

_spec(
    "tg2", 6,
    objetivos="""1. **Lograr:** Redactar marco conceptual y contextual.
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Cierre del marco referencial. Dos piezas cortas pero decisivas: definir los términos como los usa SU proyecto, y ubicar el problema en un contexto real y acotado.

#### 1. Marco conceptual = definiciones operativas
El **marco conceptual** define los términos clave **tal como los usará su proyecto**, no como los trae un diccionario. A eso se le llama **definición operativa**: acotada, útil para medir. "Tiempo de atención" no es "lo que se demora"; es "minutos entre la apertura y el cierre de un ticket en el sistema X". La definición operativa es la que permite después medir.

| Término | Definición de diccionario (insuficiente) | Definición operativa (útil) |
| :--- | :--- | :--- |
| Tiempo de atención | "lo que tarda un servicio" | "minutos entre apertura y cierre del ticket en el sistema X" |
| Ticket | "solicitud" | "registro de incidente creado por un usuario en la mesa de ayuda" |
| Clasificación correcta | "acierto" | "categoría asignada por el modelo = categoría del analista" |

#### 2. Marco contextual = dónde ocurre, acotado
El **marco contextual** describe el escenario real: la organización, el área, el proceso donde vive el problema. El error clásico es describir "Colombia" o "el sector TI del país" cuando el proyecto pasa en **un** área de **una** empresa. Contexto = organización / proceso concreto, no país entero.

#### 3. Por qué importa para TG3
Estas definiciones operativas son las que en TG3 se convierten en **variables medibles** e instrumentos. Un término mal definido hoy es un instrumento imposible mañana. Por eso esta sesión, aunque corta, sostiene la metodología.""",
    errores=[
        ("“Copio la definición del diccionario / Wikipedia.”",
         "Necesita una definición operativa: acotada y medible en SU proyecto."),
        ("“El contexto es Colombia y el sector TI.”",
         "Acote: el contexto es la organización, el área y el proceso concretos."),
        ("“Defino el término tan amplio que sirve para todo.”",
         "Si sirve para todo, no sirve para medir; delimite a su caso."),
        ("“Marco conceptual y contextual son lo mismo.”",
         "No: el conceptual define términos; el contextual describe dónde ocurre."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 06. Cerramos el marco referencial con dos piezas cortas pero decisivas: el **marco conceptual** —definir los términos como los usa SU proyecto— y el **marco contextual** —dónde ocurre exactamente el problema—.”

> “**Slide 2 — OBJETIVOS.** Salir con una tabla de términos con definiciones operativas y una página de contexto acotada. Tengan a la mano su pregunta y sus constructos del `S05`.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** El marco conceptual define sus términos, pero **no** como el diccionario. Necesitan **definiciones operativas**: acotadas y medibles. ‘Tiempo de atención’ no es ‘lo que se demora’; es ‘los minutos entre que se abre y se cierra un ticket en el sistema X’. ¿Ven la diferencia? La segunda se puede medir; la primera no.”

> “**Slide 4 — ENFOQUE DE HOY.** El marco contextual dice **dónde** ocurre. Y aquí el error clásico: describir ‘Colombia’ o ‘el sector TI del país’ cuando su proyecto pasa en un área de una sola empresa. Contexto es la **organización y el proceso concretos**, no el país entero.”

> “Y les adelanto por qué esto importa: estas definiciones operativas son las que en TG3 se vuelven **variables e instrumentos**. Un término mal definido hoy es un instrumento imposible el próximo semestre.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** tabla de términos y un párrafo de contexto.

**GUION LITERAL:**
> “Modelo la tabla de términos. Columna 1: el término. Columna 2: la definición floja de diccionario. Columna 3: la definición operativa. ‘Clasificación correcta’ → floja: ‘acierto’; operativa: ‘cuando la categoría que asigna el modelo coincide con la que pondría el analista’. Esa sí la puedo medir.”

> “Ahora el contexto, acotado: no escribo sobre Colombia. Escribo: ‘La empresa X, área de soporte TI, recibe alrededor de N tickets diarios gestionados por un equipo de M analistas mediante el sistema Y’. Concreto, medible, verificable. Si contrasto dos definiciones del mismo término en Scholar, elijo la que puedo operacionalizar, no la más elegante.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S06_ConceptualContextual_Apellido`: (1) una **tabla de términos** (≥ 4) con la definición operativa de cada uno; (2) **una página de contexto** que describa organización, área y proceso concretos, con las citas que hagan falta en APA 7.”

> “Criterio de éxito: cada término se puede medir con su definición, y el contexto describe un lugar concreto, no un país.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Copia definición de diccionario | “Vuélvala operativa: ¿cómo la mediría en su caso?” |
| Describe el país entero | “Baje a la organización y al proceso: ¿dónde exactamente?” |
| Define tan amplio que sirve para todo | “Si sirve para todo, no mide nada; acote a su proyecto.” |
| Mezcla conceptual y contextual | “Términos en la tabla; el lugar, en el párrafo de contexto.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el marco conceptual son **definiciones operativas**, medibles; (2) el contextual es la organización y el proceso concretos, no el país; (3) estas definiciones sostienen la metodología de TG3.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S06_ConceptualContextual_Apellido`. Con esto el marco referencial queda armado. La próxima sesión damos el salto al **diseño metodológico propuesto**: cómo van a responder la pregunta.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs (`S06_ConceptualContextual_Apellido`): tabla de ≥ 4 términos con definiciones operativas + 1 página de contexto acotada (organización/área/proceso) con citas APA 7.",
    entregable="`S06_ConceptualContextual_Apellido` en CDigital.",
    ejemplo="‘Tiempo de atención’ → ‘minutos entre apertura y cierre del ticket en el sistema X’; contexto = área de soporte TI de la empresa X, no ‘Colombia’.",
    shots_demo=[
        ("tg_scholar.png", "Scholar / Docs — definiciones",
         "Contrastar 2 definiciones del mismo término; elegir la operacionalizable."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib",
         "Citar las definiciones elegidas en APA 7."),
    ],
)

_spec(
    "tg2", 7,
    objetivos="""1. **Lograr:** Proponer diseño metodológico coherente.
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Bisagra entre el "qué" y el "cómo". El estudiante debe proponer una ruta coherente para responder su pregunta. En TG2 todo es **propuesto**: aún no se ejecuta.

#### 1. La metodología responde "cómo voy a responder la pregunta"
El diseño metodológico es el plan para conseguir y analizar la evidencia que responderá la pregunta. Sus piezas encadenadas: **enfoque → tipo/alcance → diseño → población/datos → técnicas**. Cada pieza se justifica por la anterior; no se elige "porque sí".

#### 2. Enfoque, alcance y diseño (vocabulario mínimo)
| Decisión | Opciones típicas | Se elige según… |
| :--- | :--- | :--- |
| Enfoque | Cuantitativo / cualitativo / mixto | La naturaleza de la pregunta |
| Alcance | Exploratorio / descriptivo / correlacional / explicativo | Qué tanto se sabe ya |
| Diseño | Experimental / no experimental / estudio de caso | Si se manipulan variables |

Ejemplo: "¿en qué medida el modelo reduce el tiempo?" es cuantitativa, alcance correlacional/explicativo, con medición antes/después.

#### 3. La matriz pregunta–método
La herramienta del día es la **matriz de coherencia**: una fila por objetivo específico y, al frente, qué dato necesita, cómo lo consigue y cómo lo analiza. Si un objetivo no tiene método, o un método no responde a ningún objetivo, hay incoherencia. La matriz la hace visible.

#### 4. Todo en "propuesto"
En TG2 no hay campo todavía: se escribe en futuro —"se aplicará", "se propone", "se seleccionará"—. Prometer resultados aquí es el error que se arrastra hasta la sustentación. El campo real es de TG3.""",
    errores=[
        ("“Elijo enfoque cualitativo porque suena más fácil.”",
         "El enfoque se elige por la pregunta, no por comodidad: ¿mide o interpreta?"),
        ("“Tengo método pero no sé para qué objetivo.”",
         "Use la matriz pregunta–método: cada método debe responder a un objetivo."),
        ("“Escribo la metodología como si ya la hubiera hecho.”",
         "En TG2 es ‘propuesto’: se aplicará / se propone. El campo es de TG3."),
        ("“Enfoque, alcance y diseño son lo mismo.”",
         "Son tres decisiones distintas y encadenadas; defina cada una."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 07. Ya tienen el ‘qué’: problema, pregunta, marco. Hoy viene el ‘cómo’: el **diseño metodológico**. Es decir, con qué plan van a responder esa pregunta. Y una advertencia desde ya: en TG2 todo es **propuesto**, no ejecutado.”

> “**Slide 2 — OBJETIVOS.** Salir con una ficha metodológica coherente: enfoque, alcance, diseño y una matriz que conecte cada objetivo con su método. Tengan abiertos sus objetivos del `S02`.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** La metodología responde una sola cosa: **cómo voy a responder mi pregunta**. Tiene piezas encadenadas: enfoque, alcance, diseño, población o datos, y técnicas. Cada pieza se justifica por la anterior; nada se elige ‘porque sí’.”

> “Vocabulario mínimo: el **enfoque** puede ser cuantitativo, cualitativo o mixto, y se elige por la naturaleza de la pregunta. El **alcance** —exploratorio, descriptivo, correlacional, explicativo— depende de cuánto se sabe ya. El **diseño** dice si hay experimento o no. Si la pregunta es ‘¿en qué medida el modelo reduce el tiempo?’, eso es cuantitativo, con medición antes y después.”

> “**Slide 4 — ENFOQUE DE HOY.** Y la regla que no se les puede olvidar: escriban todo en **propuesto**. ‘Se aplicará’, ‘se propone’, ‘se seleccionará’. En TG2 no hay campo; prometer resultados aquí es un error que se arrastra hasta la sustentación.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** la matriz pregunta–método.

**GUION LITERAL:**
> “Modelo la **matriz de coherencia**. Una fila por objetivo específico. Objetivo 1, ‘caracterizar el flujo de tickets’: dato que necesito = histórico de tickets; cómo lo consigo = exportar del sistema; cómo lo analizo = estadística descriptiva. Objetivo 2, ‘diseñar el modelo’: dato = conjunto etiquetado; técnica = entrenamiento supervisado. Objetivo 3, ‘comparar tiempos’: dato = tiempos antes/después; análisis = comparación de medias.”

> “Miren la potencia de la matriz: de un vistazo veo si algún objetivo se quedó **sin método**, o si tengo un método que no responde a ningún objetivo. Si eso pasa, hay incoherencia, y la arreglo aquí, no en TG3. Todo lo escribo en futuro, porque es una **propuesta**.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S07_Metodologia_Apellido`: (1) definan **enfoque, alcance y diseño** con una línea de justificación cada uno; (2) armen la **matriz pregunta–método**: una fila por objetivo específico con dato / técnica / análisis; (3) redacten todo en **propuesto**.”

> “Criterio de éxito: cada objetivo tiene su método en la matriz, no sobra ni falta ninguno, y no hay un solo verbo en pasado.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Elige enfoque por comodidad | “¿Su pregunta mide o interpreta? Eso decide el enfoque.” |
| Tiene un método huérfano | “¿A qué objetivo responde? Si a ninguno, sobra.” |
| Escribe en pasado | “Póngalo en ‘se propone / se aplicará’: aún no hay campo.” |
| Confunde alcance y diseño | “Alcance = qué tanto se sabe; diseño = si manipula variables.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) la metodología dice **cómo** responder la pregunta, con piezas encadenadas; (2) la matriz pregunta–método muestra la coherencia; (3) en TG2 todo va en **propuesto**.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S07_Metodologia_Apellido` con la ficha y la matriz. La próxima sesión bajamos la metodología a lo concreto: **instrumentos y plan de análisis propuestos** —cómo se verá la encuesta, la guía o el experimento—.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs (`S07_Metodologia_Apellido`): enfoque + alcance + diseño (con justificación) + matriz pregunta–método (fila por objetivo: dato / técnica / análisis), todo redactado en ‘propuesto’.",
    entregable="`S07_Metodologia_Apellido` en CDigital.",
    ejemplo="Matriz: objetivo ‘comparar tiempos’ → dato ‘tiempos antes/después’ → análisis ‘comparación de medias’; enfoque cuantitativo justificado por la pregunta.",
    shots_demo=[
        ("tg_scholar.png", "Referentes metodológicos",
         "Buscar 1 artículo con un método similar; copiar la lógica, no el texto."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib",
         "Citar el referente metodológico en APA 7."),
    ],
)

_spec(
    "tg2", 8,
    objetivos="""1. **Lograr:** Diseñar instrumentos y plan de análisis (propuestos).
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Se aterriza la metodología en herramientas concretas. Todo sigue siendo **propuesto**: se diseña el instrumento, no se aplica.

#### 1. El instrumento nace de los objetivos, no de la ocurrencia
Un **instrumento** —encuesta, guía de entrevista, ficha de observación, protocolo de prueba— es la herramienta con la que se recogen los datos. Cada ítem debe **rastrearse hasta un objetivo**: si una pregunta de la encuesta no sirve a ningún objetivo, sobra. El error típico es inventar preguntas "interesantes" que no miden nada del proyecto.

#### 2. Tabla de operacionalización: el puente
Para no improvisar ítems se usa una **tabla de operacionalización**: variable/constructo → dimensión → indicador → ítem del instrumento. Así cada pregunta tiene un porqué trazable.

| Variable | Indicador | Ítem propuesto |
| :--- | :--- | :--- |
| Tiempo de atención | Minutos por ticket | "Registre la hora de apertura y de cierre" |
| Satisfacción del usuario | Escala 1–5 | "¿Qué tan conforme quedó con la solución?" |
| Exactitud del modelo | % de aciertos | (métrica del sistema, no ítem de encuesta) |

#### 3. El plan de análisis se decide ANTES de tener datos
Error frecuente: recoger datos y después preguntarse "¿y ahora qué hago con esto?". El **plan de análisis** se escribe desde ya: qué se hará con cada tipo de dato (estadística descriptiva, comparación de medias, análisis temático de respuestas abiertas). Decidirlo antes evita recoger datos inútiles.

#### 4. Tamaño razonable
En un avance, una encuesta de ~10 ítems o una guía de ~8 preguntas es suficiente para mostrar criterio. No se busca volumen, se busca **alineación** con los objetivos.""",
    errores=[
        ("“Pongo preguntas interesantes en la encuesta.”",
         "‘Interesante’ no basta: cada ítem debe rastrearse a un objetivo. Si no, sobra."),
        ("“Primero recojo datos y luego veo cómo los analizo.”",
         "El plan de análisis se decide ANTES: así no recoge datos inútiles."),
        ("“Hago una encuesta de 40 preguntas.”",
         "En el avance ~10 ítems bien alineados valen más que 40 dispersos."),
        ("“El instrumento ya lo apliqué.”",
         "En TG2 el instrumento es propuesto: se diseña, no se aplica; el campo es de TG3."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 08. La clase pasada definimos el ‘cómo’ a grandes rasgos; hoy lo bajamos a herramientas concretas: **el instrumento y el plan de análisis**. Aviso de calendario: el próximo lunes es festivo, así que será clase autónoma; aprovechen hoy para dejar el instrumento bien armado.”

> “**Slide 2 — OBJETIVOS.** Salir con un bosquejo de instrumento alineado a los objetivos y un plan de análisis escrito. Todo **propuesto**. Tengan abierta su matriz del `S07`.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** El instrumento —encuesta, entrevista, ficha de observación, protocolo de prueba— es con lo que van a recoger datos. Regla de oro: **cada ítem se rastrea hasta un objetivo**. Si una pregunta no sirve a ningún objetivo, por interesante que sea, sobra.”

> “Para no inventar preguntas al azar usamos una **tabla de operacionalización**: variable → indicador → ítem. Así cada pregunta tiene un porqué trazable. ‘Tiempo de atención’ → indicador ‘minutos por ticket’ → ítem ‘registre hora de apertura y cierre’. Directo.”

> “**Slide 4 — ENFOQUE DE HOY.** Y algo que casi nadie hace y cuesta caro: **el plan de análisis se decide antes de tener datos**. No recojan primero y después piensen qué hacer. Decidan ya: descriptiva para esto, comparación de medias para aquello, análisis temático para las respuestas abiertas. Y todo en ‘propuesto’: en TG2 se diseña, no se aplica.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** tabla de operacionalización + 3 ítems + plan de análisis.

**GUION LITERAL:**
> “Modelo la operacionalización. Variable ‘satisfacción del usuario’ → indicador ‘escala 1 a 5’ → ítem ‘¿qué tan conforme quedó con la solución del ticket?’. Variable ‘tiempo de atención’ → indicador ‘minutos’ → ítem ‘registre apertura y cierre’. Fíjense: no se me ocurrió la pregunta, **salió de la variable**.”

> “Ahora el plan de análisis, en una lista: los tiempos se comparan con medias antes/después; la satisfacción se resume en frecuencias; las respuestas abiertas se agrupan por temas. Lo escribo hoy, sin tener un solo dato. Cuando en TG3 recojan, ya sabrán exactamente qué hacer. Y reviso un modelo de instrumento en Scholar para ver cómo otros midieron lo mismo —copio la lógica, no el texto—.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S08_Instrumentos_Apellido`: (1) hagan la **tabla de operacionalización** (variable → indicador → ítem); (2) redacten el **instrumento**: ~10 ítems de encuesta o una guía de ~8 preguntas; (3) escriban el **plan de análisis**: qué harán con cada tipo de dato. Todo en propuesto.”

> “Criterio de éxito: cada ítem se rastrea a un objetivo por la tabla, y el plan de análisis ya dice qué se hará con cada dato.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Inventa preguntas sueltas | “Rastréela: ¿de qué variable e indicador sale este ítem?” |
| No tiene plan de análisis | “Escríbalo ya: ¿qué hará con estos datos cuando los tenga?” |
| Hace 40 preguntas | “Recorte a ~10 alineadas; el volumen no da puntos.” |
| Redacta como si ya lo aplicó | “Póngalo en propuesto: ‘se aplicará una encuesta de…’.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) cada ítem del instrumento **se rastrea a un objetivo**; (2) el plan de análisis se decide **antes** de tener datos; (3) todo en propuesto.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S08_Instrumentos_Apellido`. Recuerden: el próximo lunes es festivo, clase autónoma; usen esa semana para pulir el instrumento. Cuando volvamos, la sesión es de **integración del avance y corrección de gaps**: leeremos el documento completo de corrido.”

> “**Slide 7 — Cierre.** Gracias; nos leemos en la autónoma y nos vemos en el Meet la siguiente.”""",
    taller="En Google Docs (`S08_Instrumentos_Apellido`): tabla de operacionalización (variable → indicador → ítem) + instrumento (~10 ítems o guía de ~8 preguntas) + plan de análisis, todo en ‘propuesto’.",
    entregable="`S08_Instrumentos_Apellido` en CDigital.",
    ejemplo="Variable ‘satisfacción’ → indicador ‘escala 1–5’ → ítem ‘¿qué tan conforme quedó?’; plan: medias antes/después para tiempos, frecuencias para satisfacción.",
    shots_demo=[
        ("tg_scholar.png", "Modelos de instrumento",
         "Revisar cómo otros midieron variables similares; copiar la lógica, no el texto."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib",
         "Citar las bases del instrumento en APA 7."),
    ],
)

_spec(
    "tg2", 9,
    objetivos="""1. **Lograr:** Integrar el avance y corregir gaps.
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Sesión de costura, no de contenido nuevo. Se lee el documento completo buscando **coherencia** y se prioriza qué corregir.

#### 1. Coherencia global: leer de corrido
Hasta ahora se escribió por partes; hoy se lee **todo seguido** para ver si el documento cuenta una sola historia. Las tres preguntas de coherencia: ¿el marco responde a la pregunta? ¿los objetivos siguen alineados? ¿la metodología responde a esos objetivos? Un avance puede tener buenas secciones y ser incoherente como conjunto.

#### 2. El semáforo por sección
La herramienta del día es un **semáforo**: verde = sección lista, amarillo = existe pero necesita ajuste, rojo = falta o está incoherente. Da una foto rápida de por dónde empezar y evita pulir lo verde mientras lo rojo sigue vacío.

| Sección | Semáforo | Qué corregir |
| :--- | :--- | :--- |
| Introducción | verde / amarillo / rojo | … |
| Pregunta y objetivos | verde / amarillo / rojo | … |
| Marco | verde / amarillo / rojo | … |
| Metodología | verde / amarillo / rojo | … |

#### 3. Matriz de gaps con dueño y prioridad
Cada rojo o amarillo se vuelve una fila en una **matriz de gaps**: qué falta, prioridad (alta/media/baja) y una acción concreta. En TG2 el "dueño" es el propio estudiante, pero nombrarlo obliga a comprometerse. Priorizar evita el error de arreglar comas mientras falta media metodología.

#### 4. Coherencia > pulido
Repita el criterio: primero que el documento sea coherente de punta a punta; el pulido fino de redacción viene después. Un rojo estructural pesa más que diez amarillos cosméticos.""",
    errores=[
        ("“Me pongo a corregir comas y ortografía.”",
         "Primero coherencia estructural (rojos); el pulido cosmético va al final."),
        ("“Mis secciones son buenas, así que el documento está bien.”",
         "Buenas partes ≠ conjunto coherente: lea de corrido y revise que todo se conecte."),
        ("“Anoto ‘mejorar el marco’ sin más.”",
         "Convierta el gap en acción concreta con prioridad: qué, cuánto, para cuándo."),
        ("“Arreglo lo que está casi listo (verde).”",
         "Empiece por los rojos: pulir lo verde no cierra los huecos."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 09. Volvemos de la autónoma. Hasta hoy escribimos por partes; hoy hacemos algo distinto: leer el documento **completo, de corrido**, para ver si cuenta una sola historia coherente. No es sesión de contenido nuevo, es de **costura**.”

> “**Slide 2 — OBJETIVOS.** Salir con un semáforo por sección y una matriz de correcciones priorizadas. Tengan el documento consolidado a la vista, con todas las secciones que llevan.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Un documento puede tener secciones buenas y ser incoherente como conjunto. Por eso hoy leemos de corrido con tres preguntas: ¿el marco responde a la pregunta? ¿los objetivos siguen alineados? ¿la metodología responde a esos objetivos? Si alguna se rompe, ahí hay trabajo.”

> “La herramienta es un **semáforo**: verde, la sección está lista; amarillo, existe pero necesita ajuste; rojo, falta o está incoherente. De un vistazo saben por dónde empezar.”

> “**Slide 4 — ENFOQUE DE HOY.** Y un criterio duro: **coherencia antes que pulido**. No corrijan comas mientras falta media metodología. Cada rojo o amarillo se vuelve una fila en una **matriz de gaps** con prioridad y una acción concreta. Un rojo estructural pesa más que diez amarillos cosméticos.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** tabla semáforo + matriz de gaps.

**GUION LITERAL:**
> “Modelo el semáforo con un documento de ejemplo. Introducción: verde. Pregunta y objetivos: verde. Marco: **amarillo**, tiene dos constructos pero el tercero está flojo. Metodología: **rojo**, falta el plan de análisis. Con esa foto ya sé que no voy a tocar la introducción hoy: voy directo al rojo.”

> “Ahora la matriz de gaps: fila 1, ‘completar plan de análisis’, prioridad alta, acción ‘redactarlo desde la matriz del S08’. Fila 2, ‘reforzar tercer constructo’, prioridad media. Fíjense que cada gap es una **acción**, no un lamento: no escribo ‘mejorar el marco’, escribo qué, cuánto y con qué.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S09_Integracion_Apellido`: (1) lean su documento de corrido y llenen el **semáforo** por sección; (2) hagan la **matriz de gaps**: cada rojo/amarillo con prioridad y acción concreta; (3) empiecen a cerrar el gap de mayor prioridad aquí mismo.”

> “Criterio de éxito: su semáforo refleja el estado real —sin autoengaño— y cada gap tiene una acción concreta, no un ‘mejorar esto’.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Pone todo en verde | “Léalo de corrido: ¿la metodología responde a los objetivos de verdad?” |
| Corrige ortografía primero | “Deje lo cosmético; ataque el rojo estructural.” |
| Escribe gaps vagos | “Convierta ‘mejorar X’ en una acción: qué, cuánto, con qué.” |
| No sabe cuál priorizar | “Lo que rompe la coherencia va primero; lo cosmético al final.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) buenas partes no garantizan un **conjunto coherente**; (2) el semáforo da la foto y la matriz de gaps la acción; (3) coherencia antes que pulido.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S09_Integracion_Apellido` con el semáforo y la matriz, y cierren en la semana los gaps de prioridad alta. La próxima sesión es de **socialización**: van a presentar el avance en tres minutos y a dar y recibir retroalimentación.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
    taller="En Google Docs (`S09_Integracion_Apellido`): semáforo por sección (verde/amarillo/rojo) + matriz de gaps (qué falta / prioridad / acción concreta) + cierre iniciado del gap de mayor prioridad.",
    entregable="`S09_Integracion_Apellido` en CDigital.",
    ejemplo="Semáforo: introducción verde, marco amarillo (falta 3.er constructo), metodología roja (falta plan de análisis) → matriz con acciones priorizadas.",
    shots_demo=[
        ("tg_scholar.png", "Docs — semáforo",
         "Tabla verde/amarillo/rojo por sección del documento."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib — huecos de cita",
         "Completar las referencias faltantes detectadas en la integración."),
    ],
)

_spec(
    "tg2", 10,
    objetivos="""1. **Lograr:** Socializar avances con feedback accionable.
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Sesión oral y colaborativa. El estudiante presenta su avance en corto y aprende a dar y recibir feedback útil. Es ensayo temprano de la sustentación de TG3.

#### 1. El pitch de 3 minutos
Socializar no es leer el documento: es contarlo. La estructura del **pitch de 3 minutos**: problema (¿qué duele?) → pregunta y objetivos → avance (qué llevo del marco/método) → pedido concreto de feedback (¿en qué quiero que me ayuden?). Cronometrado, obliga a decir lo esencial.

| Bloque del pitch | Segundos aprox. | Contenido |
| :--- | :--- | :--- |
| Problema | 30 s | El dolor real, con contexto |
| Pregunta y objetivos | 40 s | La brújula del proyecto |
| Avance | 70 s | Lo que llevo escrito |
| Pedido de feedback | 40 s | En qué quiero ayuda |

#### 2. Feedback con criterio, no aplausos
Un buen comentario de par no es "está muy bien" ni "no me gustó": es específico y accionable. Herramienta simple: **una fortaleza + una pregunta + una sugerencia**. Así el feedback construye en vez de herir o adular.

#### 3. Recibir sin defenderse
El error del que presenta es discutir cada comentario. La regla: **anotar todo, discutir nada** en el momento; después se decide qué se toma. Escuchar sin defenderse es una habilidad que se entrena hoy y se cobra en la sustentación.

#### 4. Por qué es ensayo de TG3
En TG3 hay defensa ante jurados. Este pitch es el primer ensayo con red: público amable, tiempos cortos y consecuencias bajas. Quien practica hoy llega con ventaja.""",
    errores=[
        ("“Leo el documento en voz alta.”",
         "Eso no es pitch: cuente problema → pregunta → avance → pedido, cronometrado."),
        ("“Doy feedback tipo ‘está muy bien’.”",
         "Sea específico: una fortaleza + una pregunta + una sugerencia accionable."),
        ("“Discuto cada comentario que me hacen.”",
         "Anote todo, discuta nada en el momento; luego decide qué toma."),
        ("“Me paso de los 3 minutos.”",
         "El tiempo es parte del ejercicio: cronómetro en pantalla, se corta al minuto 3."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 10. Hoy cambiamos de modo: no escribimos, **presentamos**. Cada uno va a contar su avance en tres minutos y va a dar y recibir retroalimentación. Y les adelanto para qué sirve esto: es el primer ensayo de la **sustentación de TG3**, pero con red.”

> “**Slide 2 — OBJETIVOS.** Salir con un guion de pitch de 3 minutos y con notas de feedback de sus compañeros. Tengan a la mano su documento para no inventar en vivo.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Socializar **no** es leer el documento; es contarlo. La estructura del pitch de tres minutos: problema —¿qué duele?—, pregunta y objetivos, avance —qué llevo—, y un pedido concreto de feedback —¿en qué quiero que me ayuden?—. Cronometrado, porque el tiempo obliga a decir lo esencial.”

> “Ahora, el feedback. Un buen comentario no es ‘está muy bien’ ni ‘no me gustó’. Usamos una fórmula: **una fortaleza + una pregunta + una sugerencia**. Específico y accionable.”

> “**Slide 4 — ENFOQUE DE HOY.** Y para el que presenta, la regla de oro: **anotar todo, discutir nada** en el momento. Nada de defenderse comentario por comentario; se anota, y después cada uno decide qué toma. Escuchar sin defenderse es una habilidad, y hoy la entrenamos.”""",
    fase3_texto="""**Protagonista:** Docente (modela el pitch).

**En pantalla (Google Docs + cronómetro):** guion de pitch de 3 minutos.

**GUION LITERAL:**
> “Modelo un pitch con el cronómetro corriendo. ‘Problema: la mesa de ayuda de la empresa X clasifica tickets a mano y eso demora la atención —30 segundos—. Pregunta: en qué medida un clasificador reduce ese tiempo; objetivos: caracterizar, diseñar, comparar —40 segundos—. Avance: llevo marco de tres constructos y matriz metodológica —70 segundos—. Pedido: quiero feedback sobre si mi tercer constructo sobra —40 segundos—.’ Y paré en tres minutos.”

> “Ahora modelo el feedback: ‘Fortaleza: la pregunta está muy clara. Pregunta: ¿de dónde vas a sacar los tickets etiquetados? Sugerencia: quita el tercer constructo si no lo usas en el método.’ Fortaleza, pregunta, sugerencia. Eso ayuda; ‘está bonito’ no.”""",
    fase4_texto="""**Protagonista:** Estudiantes (pitch + feedback) · Docente modera.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos, en ronda. Cada quien: (1) da su **pitch de 3 minutos** con la estructura vista, cronómetro en pantalla; (2) al terminar, dos compañeros dan feedback con **fortaleza + pregunta + sugerencia**; (3) quien presentó **anota todo sin discutir**. Guarden las notas en `S10_Socializacion_Apellido`.”

> “Criterio de éxito: el pitch cabe en 3 minutos y las notas de feedback son accionables, no aplausos.”

**Acompañamiento (mientras presentan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Lee el documento | “Ciérrelo: cuénteme el problema mirándome a mí.” |
| Da feedback vago | “Deme una fortaleza, una pregunta y una sugerencia concretas.” |
| Se defiende de cada nota | “Solo anote; luego decide. No discuta ahora.” |
| Se pasa del tiempo | “Corte: ¿cuál es su pedido de feedback? Termine por ahí.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el pitch es problema → pregunta → avance → pedido, en 3 minutos; (2) el feedback útil es fortaleza + pregunta + sugerencia; (3) al recibir, se **anota, no se discute**.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S10_Socializacion_Apellido` con su guion de pitch y las notas de feedback, e incorporen al documento las sugerencias que decidan tomar. La próxima sesión es la última sincrónica: **cerramos el avance de TG2 y armamos el puente a TG3**.”

> “**Slide 7 — Cierre.** Gracias por exponerse; eso da valentía. Mismo Meet.”""",
    taller="En Google Docs (`S10_Socializacion_Apellido`): guion de pitch de 3 minutos (problema → pregunta → avance → pedido) + notas de feedback recibido (fortaleza + pregunta + sugerencia de ≥ 2 pares).",
    entregable="`S10_Socializacion_Apellido` en CDigital.",
    ejemplo="Pitch cronometrado (30/40/70/40 s) + feedback ‘fortaleza + pregunta + sugerencia’ sobre el tercer constructo.",
    shots_demo=[
        ("tg_scholar.png", "Guion de pitch en Docs",
         "Plantilla 3 min: problema → pregunta → avance → pedido de feedback; cronómetro en pantalla."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib (opcional)",
         "Si citan un referente en el pitch, tener el APA a la mano."),
    ],
)

_spec(
    "tg2", 11,
    objetivos="""1. **Lograr:** Cerrar avance TG2 y preparar puente a TG3.
2. **Producir** un avance observable en CDigital.
3. **Salir** con tarea autónoma clara.""",
    fundamento="""> Última sesión sincrónica. Se consolida una versión limpia del avance y se deja un puente explícito hacia TG3. El curso alimenta a TG3: eso guía el cierre.

#### 1. Versión limpia ≠ versión final
Cerrar TG2 no es "terminar el trabajo de grado": es dejar un **avance limpio y coherente** —planteamiento, pregunta, objetivos, marco y metodología propuesta— listo para que en TG3 solo haya que ejecutar y sustentar. Limpio significa: formato APA CUN aplicado, citas y referencias completas, sin secciones a medias sin marcar.

#### 2. El checklist de cierre
| Ítem | ¿Listo? |
| :--- | :--- |
| Tema/título coherente con el contenido | ☐ |
| Pregunta y objetivos alineados | ☐ |
| Marco referencial (antecedentes + teoría + conceptual/contextual) | ☐ |
| Metodología propuesta con matriz e instrumento | ☐ |
| Referencias en APA 7, todas las citadas | ☐ |
| Formato Plantilla APA CUN aplicado | ☐ |

#### 3. La lista de pendientes para TG3
Lo que quedó en propuesto o a medias no se esconde: se escribe una **lista de pendientes para TG3** —aplicar instrumentos, recoger y analizar datos, escribir resultados y discusión, preparar sustentación y repositorio—. Esa lista es el mejor regalo que el estudiante se hace a sí mismo para el próximo semestre.

#### 4. Antiplagio: hábito, no susto
Recuerde que en TG3 la entrega pasa por la **revisión de similitud institucional del aula (CDigital)** —el Docente de TG3 indica cómo opera; sin inventar servicios externos—. Cerrar TG2 con parafraseo y citas correctas evita sorpresas. No es una amenaza; es higiene académica.""",
    errores=[
        ("“Cerrar TG2 es terminar el trabajo de grado.”",
         "No: es dejar un avance limpio para ejecutar y sustentar en TG3."),
        ("“Escondo las secciones que quedaron a medias.”",
         "Al contrario: hágalas explícitas en la lista de pendientes para TG3."),
        ("“Ya reviso el antiplagio en TG3, no me preocupo ahora.”",
         "El hábito se cierra hoy: parafraseo y citas completas evitan sorpresas."),
        ("“Entrego sin aplicar la plantilla APA CUN.”",
         "Versión limpia = formato APA CUN aplicado y referencias completas."),
    ],
    fases=[
        ("1️⃣ Encuadre", 6),
        ("2️⃣ Exposición del concepto", 14),
        ("3️⃣ Modelación en vivo", 12),
        ("4️⃣ Taller aplicado al proyecto", 20),
        ("5️⃣ Cierre + autónomo", 8),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 11, la última sincrónica del curso. Ojo con el calendario: en este tramo final hay dos lunes festivos, que son clases autónomas, así que hoy es nuestro cierre en vivo. El objetivo es claro: dejar el avance **limpio** y construir el puente a Trabajo de Grado 3.”

> “**Slide 2 — OBJETIVOS.** Salir con una versión limpia del avance, un checklist de cierre y una lista explícita de pendientes para TG3. Tengan el documento consolidado abierto.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Aclaremos qué es cerrar TG2: **no** es terminar el trabajo de grado. Es dejar un avance limpio y coherente —planteamiento, pregunta, objetivos, marco y metodología propuesta— para que en TG3 solo quede ejecutar y sustentar. ‘Limpio’ tiene nombre: formato APA CUN aplicado, citas y referencias completas, y ninguna sección a medias sin marcar.”

> “Para eso usamos un **checklist de cierre**: título coherente, objetivos alineados, marco completo, metodología con matriz e instrumento, referencias en APA 7, plantilla aplicada. Lo que no esté, se marca.”

> “**Slide 4 — ENFOQUE DE HOY.** Y lo más importante para el próximo semestre: la **lista de pendientes para TG3**. Lo que quedó en propuesto —aplicar instrumentos, recoger datos, escribir resultados, sustentar— no se esconde, se escribe. Recuerden que en TG3 el documento pasa por el **antiplagio institucional del campus**; cerrar hoy con citas y parafraseo correctos les evita sustos. Es higiene, no amenaza.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** checklist de cierre + lista de pendientes TG3.

**GUION LITERAL:**
> “Modelo el cierre con un documento de ejemplo. Recorro el **checklist**: título coherente, sí; objetivos alineados, sí; marco completo, sí; metodología con matriz e instrumento, sí; referencias APA 7, casi —faltan dos por formatear—; plantilla APA CUN, sí. Ese ‘casi’ es una tarea concreta, no un ‘ya veré’.”

> “Ahora la **lista de pendientes para TG3**, en imperativo: aplicar la encuesta propuesta; recoger y analizar los tiempos; redactar resultados y discusión; preparar el póster y la sustentación; verificar antiplagio en CDigital. Esa lista es el mejor regalo que se hacen para el próximo semestre: van a llegar sabiendo exactamente qué sigue.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S11_CierreTG2_Apellido`: (1) recorran el **checklist de cierre** y marquen lo que está y lo que falta; (2) dejen una **versión limpia** del avance con formato APA CUN y referencias completas; (3) escriban la **lista de pendientes para TG3** en imperativo.”

> “Criterio de éxito: su documento se lee coherente de punta a punta, y cualquiera que abra su lista de pendientes sabe qué falta para TG3.”

**Acompañamiento:**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Cree que ya terminó el grado | “Es el avance: marque lo que queda para ejecutar en TG3.” |
| Oculta secciones a medias | “Anótelas en pendientes; esconderlas se paga el próximo semestre.” |
| No aplicó la plantilla APA | “Cópiela sobre la Plantilla APA CUN; limpio = formato aplicado.” |
| Referencias incompletas | “Complete el APA en ZoteroBib; toda cita necesita su referencia.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cerramos el curso. Tres ideas: (1) cerrar TG2 es dejar un avance **limpio**, no terminar el grado; (2) el checklist verifica que nada quede a medias sin marcar; (3) la lista de pendientes es el puente a TG3.”

> “**Slide 6 — PARA CONTINUAR.** Suban a CDigital `S11_CierreTG2_Apellido` con la versión limpia, el checklist y la lista de pendientes. Revisen en CDigital el detalle de la evaluación del corte final y la fecha de recepción. En TG3 retoman justo desde esta lista.”

> “**Slide 7 — Cierre.** Gracias por el trabajo de todo el periodo. Llegaron con un proyecto disperso y se van con un avance ordenado; eso es exactamente lo que TG2 debía lograr. Nos vemos en TG3.”""",
    taller="En Google Docs (`S11_CierreTG2_Apellido`): checklist de cierre marcado + versión limpia del avance (formato APA CUN + referencias completas) + lista de pendientes para TG3 en imperativo.",
    entregable="`S11_CierreTG2_Apellido` en CDigital.",
    ejemplo="Checklist recorrido (referencias ‘casi’ = formatear 2) + pendientes TG3: aplicar encuesta, analizar tiempos, redactar resultados, sustentar, verificar antiplagio.",
    shots_demo=[
        ("tg_scholar.png", "Checklist en Docs",
         "Lista de secciones listas / pendientes con acción concreta."),
    ],
    shots_taller=[
        ("Herramientas/tg_zoterobib.png", "ZoteroBib — bibliografía limpia",
         "Exportar/pegar la lista APA final del avance y revisar duplicados."),
    ],
)

# ----- TG3 (15 sesiones · Syllabus 94532) -----
TG3 = [
    # Sesión 01 = ENCUADRE (no se dicta tema). El detalle vive en TG3_RICH[1], que
    # sobreescribe objetivos, fases, textos de fase, checklist y capturas.
    (1, "Encuadre: presentación del curso, del Docente, del grupo (Padlet) y de las ACAs, más el acuerdo pedagógico.",
     "Sesión de presentación: cómo se trabaja, qué se entrega y cómo se evalúa. El contenido arranca en la Sesión 02.",
     "Encargo autónomo: lectura U1–U2 + matriz de herencia.",
     "`S01_AcuerdoRetoma_Apellido`.",
     [],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib (zbib.org) — citar sin instalar nada",
       "Muéstrelo 30 segundos: pegar DOI o título → APA 7 → copiar al Doc. Responde “¿con qué gestor citamos?”.")]),
    (2, "Formulación de pregunta, objetivos y título (variables visibles).",
     "Bloque alineado al producto de sustentación.",
     "Pregunta + objetivos + título en una página.",
     "`S02_PreguntaObjetivos_Apellido`.",
     [("Herramientas/tg_scholar.png", "Scholar — variables en la literatura",
       "Identificar cómo nombran las variables autores cercanos.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib",
       "2 APA que sostienen la pregunta.")]),
    (3, "Estructura del artículo + taller de introducción.",
     "Introducción con contexto, problema, pregunta y objetivos.",
     "Introducción 3–4 párrafos en plantilla APA CUN (Docs).",
     "`S03_Introduccion_Apellido`.",
     [("Herramientas/tg_scholar.png", "Docs + plantilla APA",
       "Abrir plantilla APA CUN en Google Docs; modelar gancho → vacío → propósito.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib",
       "Citas de la introducción.")]),
    (4, "Fase I de referentes de investigación.",
     "Fichas y mapa de literatura con diálogo colaborativo.",
     "4–6 fichas + mapa de diálogo entre autores.",
     "`S04_ReferentesFaseI_Apellido`.",
     [("Herramientas/tg_scholar.png", "Google Académico",
       "Búsqueda sistemática; anotar criterio de inclusión.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib — lote APA",
       "Generar APA de todas las fichas del día.")]),
    (5, "Diseño de instrumento y desarrollo metodológico.",
     "Coherencia método–instrumento–ética de datos; prototipado / obra-creación según opción.",
     "Ficha método + bosquejo de instrumento.",
     "`S05_MetodoInstrumento_Apellido`.",
     [("Herramientas/tg_scholar.png", "Referente metodológico",
       "1 estudio con diseño similar; copiar lógica.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib",
       "Citar bases del instrumento.")]),
    (6, "Comunidades de práctica y co-creación.",
     "Nutrir el proyecto con pares/expertos sin perder autoría.",
     "Bitácora de co-creación + 3 aprendizajes accionables.",
     "`S06_CoCreacion_Apellido`.",
     [("Sesion 01/tg_padlet.png", "Padlet / Docs — socialización breve",
       "Publicar problema+propuesta en 5 líneas; pedir 1 comentario de par.")],
     [("Herramientas/tg_scholar.png", "Scholar (opcional)",
       "1 referente sobre comunidades de práctica si aplica al marco.")]),
    (7, "Experiencia creativa · análisis de datos.",
     "De datos a hallazgos; evitar ‘dump’ de tablas sin lectura.",
     "Tabla de hallazgos + 1 página de lectura.",
     "`S07_AnalisisHallazgos_Apellido`.",
     [("Herramientas/tg_scholar.png", "Docs — tabla hallazgos",
       "Columnas: dato | hallazgo | vínculo a objetivo.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib",
       "Preparar citas para la discusión (próximas sesiones).")]),
    (8, "Fase III de referentes · cierre del marco teórico.",
     "Teoría suficiente y usable en discusión; cuerpo del documento.",
     "Cierre de marco + lista de huecos resueltos.",
     "`S08_MarcoCierre_Apellido`.",
     [("Herramientas/tg_scholar.png", "Scholar — huecos del marco",
       "Buscar solo lo que falta para cerrar constructos.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib — bibliografía del marco",
       "Lista APA limpia de la sección teórica.")]),
    (9, "Resultados, discusión y relación con referentes.",
     "Hallazgos ↔ literatura ↔ objetivos.",
     "Sección resultados+discusión (borrador).",
     "`S09_ResultadosDiscusion_Apellido`.",
     [("Herramientas/tg_scholar.png", "Diálogo con referentes",
       "Tabla: hallazgo | autor que confirma/contradicce | implicación.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib",
       "Citas de la discusión.")]),
    (10, "Resumen, palabras clave UNESCO, conclusiones y referencias.",
     "Culminación formal del artículo.",
     "Resumen + keywords + conclusiones + referencias APA.",
     "`S10_CierreArticulo_Apellido`.",
     [("Herramientas/tg_zoterobib.png", "ZoteroBib — lista final APA 7",
       "Pegar bibliografía completa; revisar duplicados.")],
     [("Herramientas/tg_scholar.png", "Keywords / UNESCO",
       "Contrastar términos con uso en Scholar; 3–5 keywords.")]),
    (11, "Póster · evidencias · verificación antiplagio.",
     "Checklist de integridad académica + pieza de divulgación (Canva free / Docs).",
     "Póster 1 página + anexos rotulados. (Informe de similitud **solo si el curso lo exige**, por la ruta institucional que confirme el Docente.)",
     "`S11_PosterEvidencias_Apellido`.",
     [("Herramientas/tg_scholar.png", "Estructura del póster en Docs/Canva free",
       "Bloques: problema, método, hallazgo, conclusión. Canva free opcional.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib — 3 citas del póster",
       "Solo las citas que caben en el póster.")]),
    (12, "Sustentación ante jurados (ensayo de defensa).",
     "Guion 10–12 min + anticipar preguntas tipo.",
     "Guion oral + 5 preguntas difíciles con respuesta corta.",
     "`S12_GuionSustentacion_Apellido`.",
     [("Herramientas/tg_scholar.png", "Guion en Docs + cronómetro",
       "Ensayar con timer; 1 colega toma notas de claridad.")],
     [("Herramientas/tg_zoterobib.png", "APA a mano para jurados",
       "Tener 3 citas clave memorizables.")]),
    (13, "Entregables para repositorio institucional.",
     "Paquete final según instructivo CUN (sin inventar URLs).",
     "Checklist de archivos del repositorio + versión limpia.",
     "`S13_PaqueteRepositorio_Apellido`.",
     [("Herramientas/tg_zoterobib.png", "Bibliografía final",
       "Verificar APA completa antes del paquete.")],
     [("Herramientas/tg_scholar.png", "Docs — checklist repositorio",
       "Lista de archivos requeridos según instructivo del semestre (CDigital).")]),
    (14, "Ajustes finales · seguimiento post-sustentación.",
     "Lista de correcciones del jurado con dueño (sin fechas de periodo en el guion).",
     "Matriz de ajustes + versión corregida.",
     "`S14_AjustesPost_Apellido`.",
     [("Herramientas/tg_scholar.png", "Docs — matriz de ajustes",
       "Columna: observación jurado | cambio | hecho/pendiente.")],
     [("Herramientas/tg_zoterobib.png", "ZoteroBib",
       "Completar citas pedidas en ajustes.")]),
    (15, "Cierre administrativo · recepción.",
     "Verificación de cargas en CDigital y pendientes admin (sin inventar fechas en el guion).",
     "Checklist de recepción + confirmación de cargas.",
     "`S15_CierreAdmin_Apellido`.",
     [("Herramientas/tg_scholar.png", "Checklist CDigital",
       "Recorrer entregables cargados; capturar evidencia de envío si el campus lo permite.")],
     [("Sesion 01/tg_padlet.png", "Cierre humano (opcional)",
       "1 post de cierre/aprendizaje si el grupo aún usa el tablero; no obligatorio.")]),
]
# Contenido rico y ESPECÍFICO por sesión de TG3 (fundamento + fases con parlamento
# literal propio + tabla de errores/preguntas trampa). Model de calidad:
# Creatividad `guion_01`. No toca objetivos/entregable/fases (minutos).
TG3_RICH: dict[int, dict] = {}


def _tg3(n, **kwargs):
    TG3_RICH[n] = kwargs


_tg3(
    1,
    uso_texto="""> **Uso:** guion de la sesión de **encuadre**. Hoy **no se dicta tema**: se presenta el curso, el Docente, el grupo y las ACAs, y se deja por escrito el **acuerdo pedagógico**.
> El contenido del Syllabus 94532 arranca en la **Sesión 02**; las unidades **U1–U2** (casos de éxito · retomar el proyecto) quedan como **lectura autónoma** de esta semana.
> Léalo en voz alta casi literal. **Duración: 60 minutos**.""",
    slides_map="""🗺️ **Slides de esta presentación** (deck de **encuadre**, 22 slides — no es el mapa del curso)

| Slide | Título en el PPTX | Fase |
| :---: | :--- | :---: |
| **1** | Portada — Sesión 01 | 1 |
| **2** | AGENDA DE HOY | 1 |
| **3** | Docente | 1 |
| **4** | PRESÉNTATE — ROMPEHIELOS (QR + Padlet) | 2 |
| **5** | LAS ACAs — QUÉ SE EVALÚA | 4 |
| **6** | Cómo trabajamos: una hora semanal para cerrar el trabajo de grado | 3 |
| **7** | Qué se llevan al final: artículo, sustentación y repositorio | 3 |
| **8–9** | Mapa del curso (1/2 y 2/2): los 15 encuentros | 3 |
| **10** | El acuerdo pedagógico: qué pactamos hoy | 3 |
| **11** | Las dos ACAs: qué se entrega y qué se mira | 4 |
| **12** | Cómo se entrega, paso a paso | 4 |
| **13** | Integridad académica: aquí sí pasa por antiplagio | 4 |
| **14** | Inteligencia artificial generativa | 4 |
| **15** | Herramientas del curso | 4 |
| **16** | Cómo pedir ayuda | 4 |
| **17** | Acuerdos de convivencia | 5 |
| **18** | Preguntas frecuentes del primer día | 5 |
| **19** | Lo que debe tener listo para la Sesión 02 | 5 |
| **20** | ACUERDOS DE TRABAJO | 5 |
| **21** | PARA LA PRÓXIMA SESIÓN | 5 |
| **22** | Cierre — Sesión 01 | 5 |
""",
    objetivos="""1. **Encuadrar** TG3 como **culminación**: cómo se usa la hora sincrónica, qué se hace en autónomo y cuál es el producto (**artículo + sustentación + repositorio**).
2. **Presentar** al Docente y conocer el estado real de cada proyecto a través del Padlet.
3. **Explicar** la evaluación real del aula (quices y parciales por corte + **ACA Final** + auto y coevaluación) y la sustentación ante jurados, la ruta de entrega en CDigital, la integridad académica con antiplagio institucional y el uso de IA generativa.
4. **Dejar por escrito el acuerdo pedagógico** y encargar el trabajo autónomo: lectura U1–U2 + matriz de herencia de lo que traen de TG2.""",
    fundamento_titulo="🧰 **Preparación del Docente ANTES de la clase** *(hoy no hay tema que estudiar: hay logística que dejar lista)*",
    fundamento="""> Este grupo llega con dos cargas: un proyecto heredado que casi nadie tiene ordenado y la ansiedad de la **sustentación ante jurados**. El encuadre tiene que nombrar las dos cosas hoy; nadie debería enterarse en la sesión 12 de que hay defensa oral.

#### 1. Qué debe tener abierto y probado
| Qué | Para qué lo necesita hoy |
| :--- | :--- |
| Aula del curso en **CDigital**, con el espacio de entrega de la Sesión 01 creado | Va a proyectar dónde se sube el encargo autónomo |
| **Presentación del Curso** (`Clases/Presentacion del Curso - ….pptx`) | Slide **PRESÉNTATE** (QR + Padlet) y la logística por grupo (recepción y cierre) |
| **Esta deck** (`Clases/Sesion 01 - …/Presentacion.pptx`) | Es el hilo de la hora: 22 slides, en orden |
| **Padlet oficial** abierto y probado | Rompehielos y diagnóstico del estado de cada proyecto |
| **Libro de calificaciones** del aula **de cada grupo**, abierto en otra pestaña | TG3 **no** es corte único EV05/EXAM: son tres cortes con quices, parciales y **ACA Final**, y las ventanas cambian por grupo. Los ítems se muestran, no se citan de memoria |
| Enunciado de la **ACA Final** (`Clases/Recursos/ACAs/`) | Única entrega documental: la **fecha exacta por grupo vive ahí y en CDigital**, no en la deck |
| **Plantilla APA CUN** (`Clases/Recursos/`) | Mostrar en vivo cómo se abre en Google Docs |
| Texto del **acuerdo pedagógico** y el espacio donde quedará registrado en CDigital | Hoy se firma: no puede improvisarse al minuto 50 |
| Fechas de **recepción y cierre de cada grupo** (Presentación del Curso) | Este curso tiene **grupos con cierres distintos**: no dé una sola fecha para todos |
| **Meet** de la serie, 10 minutos antes · lista del grupo | Recibir, saludar por nombre y registrar asistencia |

#### 2. Qué NO se hace hoy
**No se dicta tema.** Los casos de éxito y el retomar el proyecto (U1–U2) son la **lectura autónoma** de esta semana. Si alguien pide que le revise su proyecto hoy, agéndelo: la hora de encuadre no se sacrifica por una revisión individual.

#### 3. Los tres mensajes que deben quedar grabados
1. **TG3 culmina, no empieza**: se hereda de TG2 / Opción de grado II y hoy se inventaría esa herencia.
2. **El producto son tres piezas encadenadas**: artículo (≥ 50 referencias y no menos de 4.000 palabras según el Syllabus 94532), sustentación ante jurados y carga al repositorio.
3. **Se avanza una sección por semana.** Quien deje todo para el cierre no alcanza a defender con dominio.

#### 4. Un cuidado propio de TG3
Aquí hay **tres grupos con calendarios de recepción y cierre distintos**. Cuando alguien pregunte por fechas, remita a la Presentación del Curso y a CDigital, y pida que cada quien anote **la de su grupo**. Dar una sola fecha en voz alta es el error administrativo más caro de este curso.""",
    ejemplo_titulo="#### Qué proyectar en pantalla (y en qué orden)",
    ejemplo="""Deje **cinco pestañas** abiertas y páselas en este orden, sin buscar nada en vivo:
**1.** Padlet (rompehielos) → **2.** CDigital, en el espacio de entrega de la sesión → **3.** el **libro de calificaciones** del aula (para leer los ítems reales con su peso) y el enunciado de la **ACA Final** → **4.** plantilla APA CUN abierta en Google Docs → **5.** el espacio donde queda registrado el **acuerdo pedagógico**.
Un minuto modelando cómo se abre la plantilla y cómo se sube un archivo evita la mitad de los correos de la primera semana.""",
    errores_titulo="#### Si un estudiante pregunta… (dudas reales del primer día)",
    errores_headers=("Si un estudiante pregunta…", "Usted responde…"),
    errores=[
        ("“¿Hoy no vamos a ver tema?”",
         "“Hoy es el encuadre: cómo trabajamos, qué se entrega y qué pactamos. Los casos de éxito y el retomar el proyecto son su lectura de esta semana; los abrimos en la Sesión 02.”"),
        ("“¿Puedo cambiar de tema?”",
         "“No a estas alturas, salvo fuerza mayor y hablado conmigo. TG3 culmina un proyecto: cambiarlo aquí es no llegar a sustentar.”"),
        ("“¿50 referencias no es imposible?”",
         "“No: se arrastran las de TG2 y se suman las nuevas cada semana. Lo imposible es reunirlas la última semana.”"),
        ("“¿Me sirve lo que hice en TG2?”",
         "“Sí, y mucho: se reutiliza lo que está bien y se reescribe lo débil. Eso es exactamente la matriz de herencia que les encargo hoy.”"),
        ("“¿Puedo trabajar solo o en grupo?”",
         "“Según lo que autorice el programa para su opción de grado. Consúltelo hoy y lo dejamos escrito en el acuerdo pedagógico.”"),
        ("“¿Cuándo es la entrega final?”",
         "“Depende de su grupo: hay calendarios distintos. Busque el suyo en la Presentación del Curso y en CDigital, y anótelo hoy mismo.”"),
        ("“¿La sustentación es en vivo, ante quién?”",
         "“Ante jurados, y pesa tanto como todo el trabajo escrito. Se prepara desde ahora: cada sección que escriba es material de esa defensa.”"),
        ("“¿La clase se graba?”",
         "Dígalo con claridad según lo que usted vaya a hacer, y aclare lo fijo: “el material y la consigna quedan siempre publicados en CDigital”."),
        ("“¿Puedo usar ChatGPT?”",
         "“Como apoyo sí, y se declara al final del documento. Verifique cada referencia: inventa autores y DOIs, y esa bibliografía va al repositorio institucional.”"),
    ],
    fases=[
        ("1️⃣ Apertura, agenda y presentación del Docente", 10),
        ("2️⃣ Preséntate: rompehielos y diagnóstico en Padlet", 10),
        ("3️⃣ Recorrido del curso, producto final y acuerdo pedagógico", 15),
        ("4️⃣ Cómo se evalúa (quices, parciales y ACA Final), entrega e integridad", 17),
        ("5️⃣ Acuerdos, encargo autónomo y cierre", 8),
    ],
    fase_slides=[
        "Slides 1–3 (Portada · AGENDA · Docente)",
        "Slide 4 (PRESÉNTATE — Padlet)",
        "Slides 6–10 (cómo trabajamos · producto · mapa · acuerdo)",
        "Slides 5 y 11–16 (evaluación real del aula · entrega · integridad · IA · herramientas · ayuda)",
        "Slides 17–22 (convivencia · dudas · Sesión 02 · acuerdos · cierre)",
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Buenas tardes y bienvenidos a **Trabajo de Grado 3**. Nos vemos los martes de cinco a seis. Dos advertencias de entrada. La primera: **hoy no vamos a ver tema**; hoy encuadramos el curso, vemos qué se entrega y pactamos cómo trabajaremos. La segunda, y quiero que se les quede grabada: este curso **no empieza nada, lo termina**. Es la línea de meta del trabajo de grado que vienen cargando desde el semestre pasado.”

> “**Slide 2 — AGENDA DE HOY.** El orden: cómo trabajamos y cuál es el producto —que son tres cosas, no una—; me presento; se presentan ustedes en un tablero; vemos las ACAs y cómo se entrega; y cerramos con los acuerdos y con la tarea de esta semana.”

> “**Slide 3 — Docente.** Un minuto sobre mí, para que sepan a quién le escriben.” [Preséntese con las credenciales de la slide y una frase sobre su experiencia acompañando sustentaciones.] “Mi correo está en pantalla para novedades personales; lo académico va por CDigital, donde queda registro.”

**Cómo se maneja este arranque:** salude por nombre. Y no abra con la palabra “jurados” en tono de amenaza: el objetivo del primer día es que sepan que hay defensa oral y que **se prepara desde la primera semana**, no que se asusten.""",
    fase2_texto="""**Protagonista:** Estudiantes (Padlet) · Docente conduce.

**En pantalla:** Presentación del Curso → slide **PRESÉNTATE**, con el QR. URL: """ + PADLET_PRESENTACION_URL + """

**GUION LITERAL:**
> “**Slide 4 — PRESÉNTATE.** Quiero conocerlos y saber en qué estado llega cada proyecto. En pantalla está el QR y el enlace; lo dejo también en el chat del Meet. Suban un post-it con (a) su nombre, (b) el tema de su proyecto en una frase y (c) el estado real: ‘casi listo’, ‘a medias’, ‘congelado desde el semestre pasado’. Unos siete minutos.”

> “Y sean honestos, porque esto me sirve a mí para dosificar el curso: si la mayoría llega con el marco a medias, arrancamos distinto que si llegan con resultados. Aquí nadie califica el post-it.”

> [Deje el tablero proyectado, ponga usted el primer post-it y lea tres o cuatro en voz alta agradeciendo por nombre. Pregunte a dos: *“¿su proyecto está más cerca de ‘producto sin documentar’ o de ‘documento sin producto’?”*. Es el diagnóstico del día.]

**Si nadie escribe** — pasa casi siempre el primer día virtual:
| Situación | Qué hace el Docente |
| :--- | :--- |
| Silencio total a los 2 minutos | Escribe un post-it de ejemplo (“tema heredado de TG2, marco a medias”) y lo narra en voz alta. |
| “No me abre el link” | Pega el URL otra vez en el chat y ofrece que lo digan por micrófono; usted lo transcribe. |
| Todos escriben “voy bien” | Repregunta: “¿cuántas referencias tienen **citadas en el cuerpo** hoy?”. El silencio es el diagnóstico. |
| Alguien dice que su proyecto se cayó | Agradece la honestidad, no lo resuelve en público y lo cita al terminar la sesión. |""",
    fase3_texto="""**Protagonista:** Docente (recorrido de la deck).

**GUION LITERAL:**
> “**Slide 6 — Cómo trabajamos.** Quince encuentros de una hora. En una hora no se escribe un artículo oyendo hablar al profesor: yo doy criterio y ejemplo en pocos minutos y el resto lo usamos para revisar **su** documento real. Traigan siempre tres cosas: el artículo abierto en su versión vigente —una sola, no cinco copias—, su lista de referencias con el conteo real, y una duda concreta.”

> “**Slide 7 — Qué se llevan al final.** El producto son **tres cosas encadenadas** y se las digo hoy para que nadie se sorprenda: primero, un artículo resultado de investigación, con revisión amplia —el Syllabus habla de al menos cincuenta referencias y de no menos de cuatro mil palabras—; segundo, una **sustentación ante jurados**; y tercero, la **carga al repositorio institucional**. Y si su opción de grado incluye un producto de ingeniería, ese producto no reemplaza al artículo: se documenta dentro de él.”

> “**Slides 8 y 9 — Mapa del curso.** Miren los quince encuentros en tres tramos: escribir el artículo, alistar póster y antiplagio, y defender y cerrar. Fíjense en la última columna: cada sesión deja algo listo. Y lean la nota: **la recepción y el cierre varían según su grupo**; busque el suyo en la Presentación del Curso y anótelo hoy.”

> “**Slide 10 — El acuerdo pedagógico.** Esto lo pactamos hoy y queda por escrito en CDigital: una sección por sesión, plantilla APA CUN en Google Docs, entrega por CDigital, retroalimentación solo sobre lo entregado, y la sustentación se prepara desde ahora. Léanlo antes de aceptarlo y pregunten ahora, no en noviembre.”""",
    fase4_texto=f"""**Protagonista:** Docente, compartiendo pantalla (CDigital + libro de calificaciones + plantilla APA).

**GUION LITERAL:**
> “**Slide 5 — Cómo se evalúa TG3.** Aquí tengo que corregir algo que circula desde semestres pasados: **TG3 no es un corte único de 100%** con un ‘proceso’ y un ‘examen’. Abran su aula y miren el libro de calificaciones: son **tres cortes**, y los ítems son **{items_corte_txt('tg3', 1)}** en el primero, **{items_corte_txt('tg3', 2)}** en el segundo y **{items_corte_txt('tg3', 3)}** en el tercero. Si alguien les dijo otra cosa, la fuente que manda es CDigital.”

> “Lo que eso significa para ustedes: los **cuestionarios suman {peso_tipo('tg3', KIND_CUESTIONARIO)} del curso**, y caen **en día de clase**. El artículo —la **ACA Final**, {peso_item('tg3', 'aca_final')}— sigue siendo la pieza grande, pero no es la única, y no se puede llegar al final con todo pendiente. Y las **fechas cambian por grupo**: cada quien anota la de su aula, no la del compañero.”

> “**Slide 11 — ítem por ítem.** En los quices y parciales se evalúa que ustedes dominen lo que están escribiendo: son cuestionarios, individuales, con tiempo, y cierran ese mismo día. En la **ACA Final** lo que se mira es la **coherencia de cabo a rabo**: que los resultados respondan la pregunta y que las referencias estén citadas en el cuerpo, no solo listadas al final. Y la **sustentación ante jurados** —que preparamos desde ahora— es el hito donde se juega el **dominio**: explicar por qué eligió ese método, qué límites tiene su trabajo y qué encontró, sin leer.”

> “**Slide 12 — Cómo se entrega.** Procedimiento puro.” [Hágalo en vivo: abra la plantilla APA CUN en Google Docs, muestre el nombre `SNN_Tema_Apellido`, descargue como PDF y abra el espacio de entrega en CDigital.] “Y una regla: **un solo documento que crece**. El artículo no es una carpeta de archivos sueltos.”

> “**Slide 13 — Integridad académica.** Aquí sí pasa por antiplagio: antes de la sustentación el documento se verifica con la **herramienta institucional del campus**. No es una amenaza, es un paso del cronograma. Todo lo que no es suyo se cita en APA 7, incluido su propio texto de TG2 —reutilizarlo sin declararlo es **autoplagio**—. Y el consejo práctico: anoten la fuente en el instante en que pegan algo; con cincuenta referencias, reconstruir de memoria es imposible.”

> “**Slide 14 — Inteligencia artificial.** Sí se puede usar como apoyo, se declara en una línea al final, y se verifica cada referencia porque estas herramientas inventan autores y DOIs. Piensen en el final del curso: frente a jurados usted defiende **cada párrafo**. Lo que no pueda explicar en voz alta se nota en menos de un minuto.”

> “**Slide 15 — Herramientas.** Todas gratis y en el navegador: Docs, Google Académico, SciELO, Redalyc, biblioteca CUN, ZoteroBib para las referencias, Slides o Canva free para el póster y la defensa, y CDigital para entregar.”

> “**Slide 16 — Cómo pedir ayuda.** Foro de CDigital para lo académico, correo para lo personal, respuesta en días hábiles y antes del siguiente encuentro. Y para los trámites de sustentación y repositorio: **pregunten temprano**, esos pasos no se resuelven la víspera.”""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “**Slides 17 y 18 — Convivencia y dudas frecuentes.** Dos minutos: empezamos a la hora, micrófono apagado mientras alguien expone, y compartir pantalla es parte del curso —vamos a proyectar borradores reales—. La retroalimentación aquí es exigente y respetuosa: se comenta el trabajo, nunca a la persona, y siempre con una propuesta concreta. Así es exactamente como pregunta un jurado. En la siguiente slide están las dudas que siempre salen el primer día.”

> “**Slide 19 — Lo que debe tener listo para la Sesión 02.** La tarea es doble. Primero, la **lectura autónoma**: las unidades 1 y 2 —casos de éxito y retomar el proyecto—, publicadas en CDigital. Segundo, y esto es lo que quiero ver: su **matriz de herencia** en un Doc llamado `S01_AcuerdoRetoma_Apellido`, con tres columnas —**reutilizo tal cual, reescribo, creo de cero**— aplicada sección por sección a lo que traen de TG2. Agreguen el conteo honesto de referencias: cuántas tienen **citadas en el cuerpo** hoy y cuántas les faltan. Y tres compromisos suyos para las próximas dos semanas.”

> “**Slides 20 y 21 — Acuerdos y para la próxima.** El trato: se entrega en CDigital, se trae el avance escrito y se cita en APA 7 desde el primer día.”

> “**Slide 22 — Cierre.** Ya saben qué vamos a hacer, cómo se evalúa y qué pactamos. La próxima sesión abrimos con sus matrices en pantalla y formulamos la pregunta, los objetivos y el título definitivos. Gracias, buen arranque, y nos vemos el próximo martes en el mismo Meet.”""",
    entregable_titulo="🧩 **Encargo autónomo (para la Sesión 02)**",
    taller="**No se hace en clase, es trabajo autónomo:** leer las unidades **U1–U2** (casos de éxito · retomar el proyecto) publicadas en CDigital; y llenar en Google Docs la **matriz de herencia** (reutilizo tal cual · reescribo · creo de cero) sección por sección, el **conteo real de referencias citadas en el cuerpo** y **3 compromisos** para las próximas dos semanas.",
    entregable="`S01_AcuerdoRetoma_Apellido` (Google Doc o PDF), **antes de la Sesión 02**.",
    checklist=[
        "- [ ] Aula del curso en **CDigital** abierta, con el espacio de entrega de la Sesión 01 creado",
        "- [ ] **Lectura autónoma U1–U2 publicada en CDigital** (sin eso el encargo no se puede cumplir)",
        "- [ ] Texto del **acuerdo pedagógico** listo y el sitio donde quedará registrado (hoy se firma)",
        "- [ ] **Fechas de recepción y cierre de cada grupo** a la vista (este curso tiene calendarios distintos)",
        "- [ ] **Padlet** oficial probado y el link listo para pegar en el chat: " + PADLET_PRESENTACION_URL,
        "- [ ] **Presentación del Curso** abierta en la slide PRESÉNTATE (QR)",
        "- [ ] Deck de hoy abierta (`Presentacion.pptx` de la Sesión 01 — 22 slides)",
        "- [ ] **Libro de calificaciones** del aula de cada grupo abierto (tres cortes: quices, parciales, **ACA Final**, auto y coevaluación) y enunciado de la **ACA Final** listo para proyectar",
        "- [ ] **Plantilla APA CUN** lista en Google Docs",
        "- [ ] Meet de la serie abierto **10 minutos antes** (enlace en la ficha de arriba) · lista del grupo a la mano",
    ],
    shots_fase2=[
        ("Sesion 01/tg_padlet.png", "Padlet — Preséntate / estado del proyecto",
         "Tablero de la Presentación del Curso. Consigna: nombre + tema en una frase + estado real del proyecto (~7 min). Lea 3–4 en voz alta."),
    ],
)

_tg3(
    2,
    fundamento="""> Sesión bisagra: sin una buena pregunta, todo el artículo cojea. Léalo completo; aquí decide la coherencia de todo el documento.

#### 1. La pregunta manda: variables visibles
La pregunta de investigación es el eje del artículo. Una buena pregunta deja **ver sus variables** (o constructos): qué se relaciona con qué, en quién y dónde. "¿Sirve la automatización?" no muestra nada; "¿en qué medida la automatización de pruebas reduce el tiempo de despliegue en el equipo X?" muestra dos variables (automatización de pruebas ↔ tiempo de despliegue) y un contexto. Como el Syllabus define, **de la pregunta salen los objetivos**.

#### 2. Objetivo general vs. específicos (y los verbos que sí sirven)
El **objetivo general** es la pregunta convertida en propósito, con un verbo de alcance amplio (analizar, diseñar, evaluar). Los **específicos** son los pasos para lograrlo, y aquí está la regla de oro: **cada objetivo específico se convierte después en una sección del artículo**. Por eso los verbos importan: "conocer", "entender" o "saber" no se pueden medir ni redactar como sección; "identificar", "caracterizar", "comparar", "diseñar", "validar" sí.

| Verbo débil (evítelo) | Verbo operable (úselo) | Qué produce en el artículo |
| :--- | :--- | :--- |
| Conocer / entender / saber | Identificar / caracterizar | Una sección de descripción |
| Ver / analizar (vago) | Comparar / correlacionar | Una sección de análisis |
| Aprender sobre | Diseñar / construir | La obra-creación / prototipo |
| Profundizar en | Evaluar / validar | Resultados y discusión |

#### 3. El título es la puerta de entrada del jurado
El jurado lee **primero el título**. Un buen título es **actor + fenómeno + contexto** en pocas palabras (orientativamente ≤ 15–20), sin eslóganes ni signos de admiración. "Innovando el futuro con IA" no dice nada; "Detección de phishing con aprendizaje automático en los correos institucionales de la CUN" lo dice todo.

#### 4. Coherencia como criterio de calidad
Pregunta, objetivos y título deben ser **la misma idea dicha de tres formas**. Si el título habla de IA pero los objetivos hablan de redes, algo está roto. La prueba rápida: leer los tres seguidos; si suenan a proyectos distintos, hay que alinearlos antes de seguir.""",
    ejemplo="En pantalla, tomar una pregunta débil ('¿es buena la automatización?') y reescribirla mostrando variables; de ahí derivar 1 objetivo general + 3 específicos con verbos operables, y un título de ≤15 palabras. Mostrar que los tres 'suenan a lo mismo'.",
    errores=[
        ("“Objetivo: 'conocer sobre la automatización de pruebas'.”",
         "'Conocer' no se mide ni se vuelve sección. Use identificar, caracterizar, comparar, diseñar o evaluar."),
        ("“¿La IA es útil? — como pregunta de investigación.”",
         "Es de sí/no y sin variables. Reformule con actor, contexto y 'en qué medida / cómo'."),
        ("“Título tipo eslogan: 'Revolucionando el software'.”",
         "Sin variables ni contexto. Título = actor + fenómeno + contexto, ≤ ~15–20 palabras."),
        ("“Puse 7 objetivos específicos para que se vea completo.”",
         "Cada específico es una sección; con 7 el artículo se vuelve inmanejable. Deje 3–4 alineados."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Buenas tardes. Sesión 02. La semana pasada cada uno dejó su tema y su matriz de herencia. Hoy le damos el corazón al proyecto: la **pregunta**, los **objetivos** y el **título**. Si esto queda bien, el resto del artículo casi se ordena solo.”

> “**Slide 2 — OBJETIVOS.** Vamos a formular una pregunta con variables visibles, derivar de ella un objetivo general y sus específicos con verbos que sí se pueden medir, y cerrar con un título que un jurado entienda de una sola leída. Tengan abierta su matriz de la Sesión 01.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** La pregunta manda. Y una buena pregunta **deja ver sus variables**: qué se relaciona con qué, en quién y dónde. '¿Sirve la automatización?' no muestra nada. '¿En qué medida automatizar las pruebas reduce el tiempo de despliegue en el equipo X?' muestra dos variables y un contexto. De esa pregunta salen los objetivos.”

> “**Slide 4 — ENFOQUE DE HOY.** Los objetivos: uno **general** —la pregunta hecha propósito— y tres o cuatro **específicos**. Regla de oro: **cada objetivo específico será una sección del artículo**. Por eso destierro tres verbos: 'conocer', 'entender', 'saber'. No se miden ni se vuelven sección. En su lugar: identificar, caracterizar, comparar, diseñar, evaluar.”

> “Y el título. El jurado lo lee primero. Actor + fenómeno + contexto, sin eslóganes. 'Innovando el futuro' no es un título; 'Detección de phishing con aprendizaje automático en los correos de la CUN' sí lo es.”""",
    fase3_texto="""**Protagonista:** Docente (modela en Google Docs).

**En pantalla (Google Docs):** documento con tres bloques — Pregunta · Objetivos · Título.

**GUION LITERAL:**
> “Modelo en vivo. Parto de una pregunta floja: '¿es buena la automatización?'. La arreglo mostrando variables: '¿en qué medida la automatización de pruebas reduce el tiempo de despliegue y los errores en producción del equipo X?'. Ya se ve qué mido.”

> “De ahí bajo los objetivos. General: 'Evaluar el efecto de la automatización de pruebas sobre el tiempo de despliegue del equipo X'. Específicos: 1) *caracterizar* el proceso actual; 2) *diseñar* la automatización; 3) *comparar* tiempos antes y después. Fíjense que cada uno ya me dice qué sección voy a escribir. Y el título sale casi solo de la pregunta.”

> “La prueba final: leo pregunta, objetivos y título seguidos. Si suenan a lo mismo, hay coherencia; si suenan a tres proyectos, los alineo antes de seguir.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S02_PreguntaObjetivos_Apellido` escriban, en una sola página: (1) la **pregunta** con sus variables visibles; (2) **un objetivo general + 3 específicos** con verbos operables; (3) el **título** en ≤ 15–20 palabras. Al final, hagan la prueba de coherencia: léanlos seguidos.”

> “Criterio de éxito: cada objetivo específico deja ver qué sección producirá, y el título, la pregunta y los objetivos suenan a un solo proyecto.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Usa “conocer/entender” | “Cámbielo por un verbo que se pueda medir: caracterizar, comparar, evaluar.” |
| Pregunta de sí/no | “Ábrala con 'en qué medida' o 'cómo', y póngale contexto.” |
| Título eslogan | “Quítele el adjetivo bonito; deme actor, fenómeno y lugar.” |
| Objetivos que no cuadran con la pregunta | “Léalos seguidos: si suenan a otro proyecto, alinéelos con la pregunta.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) la pregunta manda y debe dejar ver sus variables; (2) cada objetivo específico será una sección, así que use verbos que se midan; (3) el título es la puerta del jurado: actor + fenómeno + contexto.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S02_PreguntaObjetivos_Apellido` a CDigital. La próxima sesión tomamos esta pregunta y estos objetivos y montamos la **estructura del artículo**, con un taller de **introducción** sobre la plantilla APA CUN.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet el próximo martes.”""",
)

_tg3(
    3,
    fundamento="""> Hoy el estudiante deja de tener "ideas sueltas" y empieza a tener un **documento con secciones**. Léalo completo.

#### 1. Anatomía del artículo (plantilla APA CUN / IMRyD)
Un artículo de resultados de investigación no es un ensayo libre: tiene **secciones fijas**. El esqueleto IMRyD, adaptado a la plantilla APA CUN, es:

| Sección | Qué va (y qué NO) | Error típico |
| :--- | :--- | :--- |
| Resumen + palabras clave | Síntesis del todo (se escribe al final) | Escribirlo primero, con citas |
| Introducción | Contexto → problema → pregunta → objetivos → propósito | Arrancar "desde la antigüedad" |
| Marco / referentes | Teoría y antecedentes que sostienen la pregunta | Collage de definiciones |
| Metodología | Enfoque, diseño, instrumentos, análisis | Mezclarla con resultados |
| Resultados | Qué se encontró (neutral) | Interpretar aquí |
| Discusión | Qué significa, en diálogo con autores | Repetir resultados |
| Conclusiones | Responder la pregunta, límites, futuro | Ideas nuevas sin respaldo |
| Referencias | ≥ 50, en APA 7 | Listar sin citar en el cuerpo |

#### 2. La introducción como embudo
La introducción va de lo ancho a lo estrecho: **gancho/contexto → problema → vacío → pregunta → objetivos → propósito del artículo**. Tres o cuatro párrafos bastan. El lector debe terminar la introducción sabiendo qué se pregunta el autor y qué se propone hacer, sin haber leído todavía la teoría.

#### 3. No mezclar secciones
El error de forma más común: meter método en la introducción, o interpretar en los resultados. Cada cosa en su sección. Regla mental: **introducción = por qué; método = cómo; resultados = qué encontré; discusión = qué significa**.

#### 4. Plantilla APA CUN en Google Docs (nube, sin Word de escritorio)
Se trabaja sobre la **plantilla APA CUN abierta en Google Docs** (`Plantilla_APA_CUN_Proyecto de grado.docx` subida a Drive y abierta como Documento de Google). Así se garantiza formato correcto sin depender de Word instalado. El flujo de citación (Scholar → ZoteroBib → Docs) está detallado en la guía transversal `Guiones/Guía práctica - Herramientas de escritura y citación.md`; no lo repita en clase, remítalos allí.""",
    ejemplo="En la plantilla APA CUN (abierta en Google Docs) escribir en vivo una introducción de 3–4 párrafos con la estructura gancho→contexto→problema→vacío→pregunta→objetivos, y marcar en rojo un mal arranque ('desde la antigüedad el ser humano…') para contrastar.",
    errores=[
        ("“La introducción arranca con 'desde la antigüedad el ser humano…'.”",
         "Arranque en el contexto real del problema, no en la historia universal."),
        ("“Meto un poco de método en la introducción para que se entienda.”",
         "No: introducción = por qué; el cómo va en Metodología. Cada cosa en su sección."),
        ("“Escribo el resumen ahora que estoy fresco.”",
         "El resumen se escribe al final; ahora no sabe aún qué resultado resumir."),
        ("“Doy formato a mano con negritas y sangrías.”",
         "Use la plantilla APA CUN en Google Docs; el formato ya viene resuelto."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 03. Ya tienen pregunta, objetivos y título. Hoy dejan de tener ideas sueltas y pasan a tener un **documento con secciones**. Vamos a montar el esqueleto del artículo y a escribir, en vivo, la **introducción**.”

> “**Slide 2 — OBJETIVOS.** Conocer la anatomía del artículo en la plantilla APA CUN, entender qué va en cada sección para no mezclarlas, y salir con la introducción empezada. Abran ya la **plantilla APA CUN en Google Docs**; hoy trabajamos sobre ella.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** El artículo tiene secciones fijas, no es un ensayo libre. Resumen, introducción, marco, metodología, resultados, discusión, conclusiones y referencias. Y una regla mental que les va a salvar la vida: **introducción = por qué; método = cómo; resultados = qué encontré; discusión = qué significa**. Si respetan eso, no mezclan.”

> “**Slide 4 — ENFOQUE DE HOY.** Hoy nos concentramos en la **introducción**, que funciona como un **embudo**: arranca ancho —contexto— y se va cerrando por el problema, el vacío, la pregunta y los objetivos, hasta el propósito del artículo. Tres o cuatro párrafos. Lo que **no** se hace: empezar con 'desde la antigüedad el ser humano se comunica'. Se arranca en el problema real.”

> “Y una nota de forma: trabajamos sobre la **plantilla APA CUN en Google Docs**. Nada de dar formato a mano ni de depender de Word instalado; el formato ya viene resuelto.”""",
    fase3_texto="""**Protagonista:** Docente (modela en la plantilla APA CUN, en Google Docs).

**En pantalla (Google Docs + plantilla APA CUN):** escriba una introducción de 3–4 párrafos en vivo.

**GUION LITERAL:**
> “Modelo la introducción como embudo. Párrafo 1, contexto: 'El despliegue continuo de software depende de pruebas confiables…'. Párrafo 2, problema y vacío: 'Sin embargo, en el equipo X las pruebas son manuales y no se ha medido su impacto en el tiempo de despliegue…'. Párrafo 3, pregunta y objetivos: 'Por ello este artículo se pregunta en qué medida… y se propone evaluar…'.”

> “Miren lo que NO hice —lo dejo en rojo un segundo—: no empecé con 'desde la antigüedad'. Arranqué en el problema. Y fíjense dónde citaré: el flujo Scholar → ZoteroBib → pegar en Docs está en la guía transversal; ahí lo tienen paso a paso, no lo repito hoy.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En la plantilla APA CUN (Google Docs), archivo `S03_Introduccion_Apellido`: escriban una **introducción de 3–4 párrafos** con el embudo contexto → problema → vacío → pregunta → objetivos → propósito. Debe cerrar exactamente en la pregunta y los objetivos de la Sesión 02.”

> “Criterio de éxito: si leo su introducción sin conocer su tema, entiendo el contexto, el vacío y qué se proponen; y termina en su pregunta, no en el aire.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Arranca con historia universal | “Empiece en el problema concreto, no en la antigüedad.” |
| Mete el método en la intro | “Eso va en Metodología; aquí solo el 'por qué'.” |
| La intro no cierra en la pregunta | “Reescriba el último párrafo para que caiga en su pregunta y objetivos.” |
| Pelea con el formato | “No dé formato a mano; escriba sobre la plantilla APA CUN.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el artículo tiene secciones fijas y no se mezclan —por qué, cómo, qué encontré, qué significa—; (2) la introducción es un embudo que termina en la pregunta; (3) se escribe sobre la plantilla APA CUN en Docs.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S03_Introduccion_Apellido` a CDigital. La próxima sesión abrimos la **Fase I de referentes**: búsqueda sistemática y fichas de lectura para empezar a sumar hacia las 50 referencias.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    4,
    fundamento="""> La sesión que decide si llegan o no a las 50 referencias. Léalo completo: es método de búsqueda, no "buscar en Google".

#### 1. Tres cosas que se confunden: antecedentes, marco y estado del arte
- **Antecedentes / referentes (Fase I):** estudios previos que ya abordaron su problema o uno cercano. Responden "¿quién más lo ha estudiado y qué encontró?".
- **Marco teórico:** los conceptos y teorías que sostienen su pregunta (se cierra más adelante, en la Sesión 08).
- **Estado del arte:** lo más reciente y avanzado del tema.

Hoy trabajamos **Fase I: los referentes**. No es lo mismo que el marco; es el mapa de quién ya caminó por aquí.

#### 2. La ficha de lectura (el ladrillo de todo)
Nadie cita bien lo que no leyó. La **ficha de lectura** obliga a leer y ordena la información:

| Campo de la ficha | Qué contiene |
| :--- | :--- |
| Dato bibliográfico (APA 7) | Autor, año, título, fuente |
| Idea principal | En una sola frase, con sus palabras |
| Cita textual | 1 frase clave con número de página |
| Relación con mi pregunta | Confirma / contradice / extiende / aporta método |

Una fuente que no se puede relacionar con la pregunta **no entra**.

#### 3. Búsqueda sistemática (no aleatoria)
Buscar bien ahorra semanas. Estrategia: empezar amplio en **Google Académico** (con comillas para frase exacta, AND/OR, filtro por año —últimos 5 en temas tecnológicos—), afinar en **SciELO/Redalyc**, y descargar el texto completo desde la **biblioteca CUN** con login institucional. Definir **criterios de inclusión/exclusión** (idioma, años, pertinencia) para no ahogarse. El enlace "citado por" de Scholar es oro: lleva de un buen paper a otros mejores.

#### 4. Mapa de diálogo entre autores (no una lista)
Los referentes no se apilan; se **ponen a conversar**. Un mapa de diálogo agrupa autores por lo que dicen: quiénes coinciden, quiénes discrepan, quién extiende a quién. Ese mapa es el borrador de la discusión que escribirán en la Sesión 09. El flujo Scholar → ZoteroBib → Docs está en la guía transversal `Guiones/Guía práctica - Herramientas de escritura y citación.md`.""",
    ejemplo="En pantalla, hacer una búsqueda en Google Académico con comillas + AND + filtro de año, abrir el enlace 'citado por' de un resultado, y llenar UNA ficha de lectura completa (APA + idea + cita + relación con la pregunta) para mostrar el estándar.",
    errores=[
        ("“Cito un paper por el título, sin leerlo.”",
         "Se nota en la discusión y es riesgo de plagio. Haga la ficha de lectura antes de citar."),
        ("“Junto 20 citas seguidas y ese es mi marco.”",
         "Eso es un collage. Agrupe por lo que dicen los autores: quién confirma, quién contradice."),
        ("“Busco solo en Google normal.”",
         "Vaya a Scholar, SciELO, Redalyc y a la biblioteca CUN; use comillas, AND/OR y filtro por año."),
        ("“Meto cualquier fuente para llegar a 50.”",
         "Cantidad sin pertinencia no cuenta; cada referente debe relacionarse con su pregunta."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 04. Hoy empieza la batalla de las **50 referencias**, pero con método, no a lo loco. Trabajamos la **Fase I de referentes**: quién más ha estudiado su problema y qué encontró.”

> “**Slide 2 — OBJETIVOS.** Distinguir antecedentes de marco teórico, dominar la **ficha de lectura**, buscar de forma sistemática y armar un primer **mapa de diálogo** entre autores. Tengan a la mano su pregunta de la Sesión 02: es la brújula de toda búsqueda de hoy.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Ojo con tres palabras que se confunden. **Antecedentes** —lo de hoy— son estudios previos: quién ya abordó esto. **Marco teórico** son los conceptos que sostienen la pregunta; ese lo cerramos más adelante. **Estado del arte** es lo más reciente. Hoy: referentes, Fase I.”

> “Segundo, el ladrillo de todo: la **ficha de lectura**. Nadie cita bien lo que no leyó. Cada fuente se resume en cuatro campos: dato bibliográfico en APA, idea principal en una frase, una cita textual con página, y —lo más importante— **cómo se relaciona con mi pregunta**. Si no la puedo relacionar, la fuente no entra.”

> “**Slide 4 — ENFOQUE DE HOY.** Y se busca con método: amplio en Scholar —comillas, AND/OR, filtro por año—, afino en SciELO y Redalyc, y bajo el texto completo desde la biblioteca CUN. Truco: el enlace 'citado por' de Scholar los lleva de un buen paper a otros mejores.”""",
    fase3_texto="""**Protagonista:** Docente (modela búsqueda + ficha).

**En pantalla (Google Académico + Google Docs):** una búsqueda real y una ficha de lectura en blanco.

**GUION LITERAL:**
> “Modelo la búsqueda. Escribo entre comillas 'tiempo de despliegue' AND 'automatización de pruebas', filtro del 2020 en adelante. Abro un resultado y —miren— hago clic en **'citado por'**: de un artículo salen otros diez pertinentes. Así se construye un corpus, no buscando al azar.”

> “Ahora lleno **una ficha** en el Doc: autor y año en APA, la idea principal en una frase mía, una cita textual con página, y la relación: 'este autor *confirma* que automatizar reduce tiempos, me sirve para el marco'. Si no logro escribir esa última línea, descarto la fuente. Esa disciplina es la que separa 50 referencias sólidas de 50 títulos de relleno.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S04_ReferentesFaseI_Apellido`: (1) definan su **criterio de inclusión** (años, idioma, pertinencia) en una línea; (2) busquen en Scholar y en SciELO o Redalyc y elijan **4–6 fuentes**; (3) hagan **una ficha de lectura** por fuente; (4) esbocen un **mapa de diálogo**: agrupen quién confirma, quién contradice, quién extiende.”

> “Criterio de éxito: cada ficha tiene su línea de 'relación con mi pregunta', y el mapa muestra a los autores conversando, no una lista apilada.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Cita sin haber leído | “Escriba la idea principal con SUS palabras; si no puede, no la leyó.” |
| Solo usa Google normal | “Vaya a Scholar/SciELO/Redalyc; la biblioteca CUN da el texto completo.” |
| Apila citas sin relación | “¿Esta fuente confirma o contradice a la anterior? Agrúpelas.” |
| Mete fuentes solo para sumar | “Si no la relaciona con su pregunta, fuera; cantidad sin pertinencia no cuenta.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) hoy son **antecedentes** (Fase I), no el marco completo; (2) nada se cita sin ficha de lectura; (3) los referentes se ponen a **dialogar**, no se apilan.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S04_ReferentesFaseI_Apellido` a CDigital con sus fichas y el mapa. Sigan sumando fichas en autónomo: cada semana deben acercarse a las 50. La próxima sesión diseñamos el **instrumento y el desarrollo metodológico**.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    5,
    fundamento="""> Aquí muchos proyectos se descarrilan: eligen un método "porque suena bien" y no mide lo que preguntaron. Léalo completo.

#### 1. La matriz de consistencia: todo debe encajar
El diseño metodológico no se inventa: **se deriva de la pregunta y los objetivos**. La herramienta que lo garantiza es la **matriz de consistencia**, que alinea cada pieza:

| Objetivo específico | Variable / constructo | Técnica | Instrumento | Análisis |
| :--- | :--- | :--- | :--- | :--- |
| Caracterizar el proceso actual | Tiempo de despliegue | Observación | Bitácora / log | Estadística descriptiva |
| Diseñar la automatización | Cobertura de pruebas | Prototipado | Prototipo (obra-creación) | Revisión técnica |
| Comparar antes/después | Errores en producción | Medición | Registro de incidencias | Comparación de medias |

Si una fila no encaja, el método está mal, no la matriz.

#### 2. Enfoque, alcance y diseño (las tres decisiones)
- **Enfoque:** cualitativo (comprender significados), cuantitativo (medir) o mixto.
- **Alcance:** exploratorio, descriptivo, correlacional o explicativo.
- **Diseño:** cómo se recogen los datos (estudio de caso, cuasi-experimento, investigación-creación con prototipado, etc.).

En investigación-creación, el **prototipado de la obra** es a la vez método y resultado: se diseña, se prueba y se documenta.

#### 3. El instrumento mide los objetivos (no otra cosa)
Un instrumento —encuesta, entrevista, guía de observación, rúbrica del prototipo— es bueno cuando **cada ítem apunta a un objetivo**. Una encuesta de 40 preguntas dispersas no sirve; una de 10 ítems alineados, sí. Regla: por cada ítem, preguntarse "¿a qué objetivo responde?". Si no responde a ninguno, se borra.

#### 4. Ética de datos (no opcional)
Si recoge datos de personas: **consentimiento informado**, anonimización y uso solo para el estudio. Es un criterio de evaluación y de integridad, no un trámite. En clase se diseña el instrumento y se **enuncia** el tratamiento ético.""",
    ejemplo="Llenar en vivo una fila de la matriz de consistencia (objetivo → variable → técnica → instrumento → análisis) y, a partir de ella, redactar 2–3 ítems de instrumento; mostrar un ítem 'huérfano' que no responde a ningún objetivo y borrarlo.",
    errores=[
        ("“Elegí encuesta porque es lo más fácil.”",
         "El método se deriva de la pregunta y los objetivos, no de la comodidad. Revise la matriz de consistencia."),
        ("“Mi encuesta tiene 40 preguntas para que sea completa.”",
         "Disperso. Cada ítem debe responder a un objetivo; si no, se borra. 10 ítems alineados valen más."),
        ("“Copié el método de un paper tal cual.”",
         "Puede copiar la lógica, no el texto; y debe justificar por qué aplica a SU pregunta."),
        ("“Recojo datos de personas sin más.”",
         "Necesita consentimiento informado y anonimización; la ética es criterio de evaluación."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 05. Aquí es donde se descarrilan muchos proyectos: eligen un método 'porque suena bien' y termina midiendo lo que no preguntaron. Hoy blindamos eso: el método se **deriva** de la pregunta y los objetivos.”

> “**Slide 2 — OBJETIVOS.** Construir una **matriz de consistencia** que amarre objetivos, técnica, instrumento y análisis; tomar las tres decisiones —enfoque, alcance, diseño—; y bosquejar el **instrumento**. Tengan abiertos sus objetivos de la Sesión 02.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** La herramienta reina de hoy es la **matriz de consistencia**. Una columna por objetivo específico, y al lado: variable, técnica, instrumento, análisis. Si una fila no encaja, el que está mal es el método, no la matriz. Esto obliga a que todo el diseño **responda a lo que ustedes preguntaron**.”

> “Tres decisiones que hay que enunciar: **enfoque** —cuali, cuanti o mixto—; **alcance** —exploratorio, descriptivo, correlacional—; y **diseño** —caso, cuasi-experimento, investigación-creación con prototipado—. En obra-creación, ojo: el **prototipo es método y resultado a la vez**: se diseña, se prueba y se documenta.”

> “**Slide 4 — ENFOQUE DE HOY.** Y el instrumento. Regla dura: **cada ítem responde a un objetivo**. Por cada pregunta de su encuesta o guía, háganse '¿a qué objetivo apunta?'. Si no apunta a ninguno, se borra. Y si recogen datos de personas: consentimiento y anonimización. Eso se evalúa.”""",
    fase3_texto="""**Protagonista:** Docente (modela la matriz + ítems).

**En pantalla (Google Docs):** una matriz de consistencia con 3 columnas y un bloque de ítems.

**GUION LITERAL:**
> “Modelo una fila completa. Objetivo: 'caracterizar el proceso actual de despliegue'. Variable: tiempo de despliegue. Técnica: observación. Instrumento: bitácora / log. Análisis: estadística descriptiva. Miren cómo la fila cierra sola: sé qué mido, con qué y cómo lo analizo.”

> “Ahora bajo esa fila a **ítems** de instrumento: '¿cuánto tarda hoy un despliegue?', '¿cuántos pasos manuales tiene?'. Y les muestro un ítem huérfano: '¿le gusta trabajar en equipo?'. ¿A qué objetivo responde? A ninguno. Lo borro. Esa es la disciplina: nada de relleno.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S05_MetodoInstrumento_Apellido`: (1) llenen su **matriz de consistencia** con una fila por objetivo específico; (2) declaren enfoque, alcance y diseño en tres líneas; (3) redacten un **bosquejo de instrumento** (10 ítems o una guía de 8 preguntas / rúbrica del prototipo), verificando que cada ítem responde a un objetivo; (4) escriban una línea sobre el tratamiento ético de los datos.”

> “Criterio de éxito: no queda ninguna fila suelta en la matriz y ningún ítem huérfano en el instrumento.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Eligió método por comodidad | “¿Ese método mide su objetivo? Compruébelo en la matriz.” |
| Encuesta larguísima | “Borre todo ítem que no responda a un objetivo; menos es más.” |
| Copió el método de un paper | “Copie la lógica, no el texto, y justifique por qué aplica aquí.” |
| No menciona ética | “Si hay personas, agregue consentimiento y anonimización.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el método se deriva de la pregunta —matriz de consistencia—; (2) cada ítem del instrumento responde a un objetivo; (3) si hay datos de personas, hay ética que declarar.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S05_MetodoInstrumento_Apellido` a CDigital. En autónomo, afinen el instrumento y —si aplica— empiecen el prototipo. La próxima sesión trabajamos **comunidades de práctica y co-creación** para nutrir el proyecto con pares.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    6,
    fundamento="""> Sesión de socialización: hoy el proyecto se expone a otros ojos. Léalo completo; el reto es nutrirse sin perder autoría.

#### 1. Comunidad de práctica: qué es y por qué nutre el proyecto
Una **comunidad de práctica** (concepto popularizado por Wenger) es un grupo que comparte un interés y aprende junto al hacer. En clase, el grupo TG3 **es** una comunidad de práctica: cada proyecto mejora cuando otro lo mira con ojos frescos. El aislamiento es el peor enemigo del trabajo de grado; la socialización, su mejor acelerador.

#### 2. Co-creación vs. copia (la línea que no se cruza)
Co-crear es **incorporar aportes de otros manteniendo la autoría**: la idea ajena se agradece, se adapta y —si es publicada— **se cita**. Copiar es apropiarse. La diferencia práctica: si un compañero les da una idea, la registran en su bitácora ("aporte de X"); si viene de una fuente, la citan. Esto conecta directo con el antiplagio de la Sesión 11.

#### 3. Cómo pedir feedback accionable
El feedback vago ("está bien", "me gusta") no sirve. Para que sirva, hay que **pedir bien**: un pitch de 3 minutos con estructura fija y un **pedido concreto** al final.

| Bloque del pitch (3 min) | Segundos | Qué se dice |
| :--- | :--- | :--- |
| Problema | 30 s | El dolor, con contexto |
| Pregunta y objetivos | 30 s | Qué se propone responder |
| Avance | 60 s | Dónde va (método, prototipo) |
| Pedido concreto | 60 s | "Necesito feedback sobre X" |

#### 4. La bitácora de co-creación
Todo lo que reciben se registra: quién aportó qué, qué decidieron hacer con eso (adoptar, adaptar, descartar) y por qué. La bitácora es evidencia del proceso —insumo directo de la **ACA Final**— y protege su autoría: deja claro qué es aporte externo y qué es decisión propia.""",
    ejemplo="Modelar un pitch de 3 minutos con el cronómetro en pantalla (problema→pregunta→avance→pedido concreto) y, en un Doc, mostrar una fila de bitácora de co-creación: 'aporte de X → decisión: adaptar → por qué'.",
    errores=[
        ("“Le pido feedback al grupo y me dicen 'está bien'.”",
         "Feedback vago. Haga un pedido concreto: 'necesito opinión sobre mi instrumento', y dé un pitch de 3 min."),
        ("“Un compañero me dio una idea buenísima, la uso y ya.”",
         "Regístrela en la bitácora como aporte de esa persona; co-crear no es apropiarse."),
        ("“Me defiendo de cada comentario que me hacen.”",
         "Primero escuche y anote; la defensa cierra puertas. El objetivo es nutrir el proyecto."),
        ("“No anoto nada de la socialización.”",
         "La bitácora es evidencia del proceso y alimenta la **ACA Final**; además protege su autoría. Registre aportes y decisiones."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 06. Cambiamos de ritmo: hoy el proyecto sale de su burbuja y se expone a otros ojos. El grupo entero es hoy una **comunidad de práctica**, y el reto es nutrirse sin perder autoría.”

> “**Slide 2 — OBJETIVOS.** Entender qué es una comunidad de práctica y la co-creación, aprender a **pedir feedback accionable** con un pitch de 3 minutos, y salir con una **bitácora de co-creación** con aprendizajes concretos. Tengan su avance a la mano; hoy se muestra.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Una comunidad de práctica es un grupo que aprende junto haciendo. El peor enemigo del trabajo de grado es encerrarse; el mejor acelerador es mostrarlo. Hoy cada proyecto mejora porque otro lo mira con ojos frescos.”

> “Ahora, la línea que **no** se cruza: co-crear no es copiar. Co-crear es tomar un aporte de otro, adaptarlo y —si viene de una fuente— **citarlo**; y si viene de un compañero, registrarlo como su aporte. Copiar es apropiarse. Esto conecta directo con el antiplagio que veremos en la Sesión 11.”

> “**Slide 4 — ENFOQUE DE HOY.** Y para que el feedback sirva, hay que pedirlo bien: un **pitch de 3 minutos** —problema, pregunta, avance, y un **pedido concreto** al final—. Nada de 'opinen'; sí de 'necesito feedback sobre mi instrumento'.”""",
    fase3_texto="""**Protagonista:** Docente (modela el pitch + bitácora).

**En pantalla (cronómetro + Google Docs):** un temporizador visible y una bitácora de co-creación en blanco.

**GUION LITERAL:**
> “Modelo un pitch con el cronómetro corriendo. 30 segundos de problema: 'en el equipo X los despliegues son lentos y manuales'. 30 de pregunta y objetivos. 60 de avance: 'ya tengo la matriz de consistencia y un instrumento de 10 ítems'. Y los últimos 60 —clave— el **pedido concreto**: 'necesito que me digan si mi instrumento realmente mide el tiempo de despliegue'. ¿Ven? Pedí algo específico; así el feedback es útil.”

> “Y abro la **bitácora**: una fila por aporte. 'Aporte de Ana: agregar un ítem sobre errores en producción → decisión: adopto → por qué: cubre un objetivo que tenía flojo'. Eso protege mi autoría y deja evidencia del proceso.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller de socialización) · Docente modera.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos, en parejas o tríos. Turnos: uno da su **pitch de 3 minutos** con pedido concreto; los demás dan feedback sobre lo que pidió, no sobre gustos. Cada quien llena su `S06_CoCreacion_Apellido` con: (1) el pedido que hizo; (2) **3 aprendizajes accionables** recibidos; (3) qué decide hacer con cada uno (adoptar/adaptar/descartar) y por qué.”

> “Criterio de éxito: la bitácora deja claro qué es aporte externo y qué es decisión propia, con una razón en cada caso.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Da feedback tipo “está bien” | “Sea concreto: responda al pedido que hizo el compañero.” |
| Se pasa de los 3 minutos | “Ajuste al cronómetro; en la sustentación el tiempo es nota.” |
| Se pone a la defensiva | “Primero anote, después decida; no discuta el comentario.” |
| Toma una idea ajena sin anotar | “Regístrela como aporte de esa persona en la bitácora.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el grupo es una comunidad de práctica y socializar acelera; (2) co-crear no es copiar: se registra y se cita; (3) el feedback útil se pide con un pedido concreto.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S06_CoCreacion_Apellido` con su bitácora. En autónomo, apliquen los aprendizajes al proyecto. La próxima sesión pasamos a la **experiencia creativa y el análisis de datos**: convertir datos en hallazgos.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    7,
    fundamento="""> Sesión clave: el dato en bruto no dice nada; el hallazgo sí. Léalo completo para no caer en el 'dump' de tablas.

#### 1. Dato ≠ hallazgo ≠ resultado
Es la distinción más importante del análisis:
- **Dato:** el registro en bruto ("el despliegue tardó 42 minutos").
- **Hallazgo:** la interpretación de ese dato a la luz de la pregunta ("el tiempo de despliegue casi duplica el estándar del equipo").
- **Resultado:** el hallazgo que **responde a un objetivo** ("se caracterizó el proceso actual: lento y con 6 pasos manuales").

Muchos estudiantes entregan datos y creen que entregaron resultados. No: falta la interpretación.

#### 2. Análisis según el enfoque
- **Cuantitativo:** estadística descriptiva (promedios, frecuencias, porcentajes), tablas y gráficos. Cada tabla necesita una **lectura en prosa**, no se deja sola.
- **Cualitativo:** codificación (etiquetar fragmentos), agrupación en **categorías**, y búsqueda de patrones.
- **Investigación-creación / obra-creación:** la experiencia creativa se analiza describiendo decisiones de diseño, iteraciones del prototipo y qué se aprendió en cada una.

#### 3. La tabla de hallazgos (herramienta del día)
| Dato (evidencia) | Hallazgo (interpretación) | Objetivo que responde |
| :--- | :--- | :--- |
| 42 min por despliegue | Casi el doble del estándar | Caracterizar proceso actual |
| 6 pasos manuales | Alta dependencia de intervención humana | Caracterizar proceso actual |
| 3 incidencias/semana | Errores frecuentes en producción | Comparar antes/después |

#### 4. El error del "data dump"
Pegar diez tablas sin leer no es análisis: es un volcado. Cada tabla o figura debe ir acompañada de una o dos frases que digan **qué se ve y qué significa**. Regla: si una tabla no tiene lectura, sobra.""",
    ejemplo="En pantalla, tomar un dato crudo ('42 minutos') y llevarlo por las tres etapas dato→hallazgo→resultado; luego mostrar una tabla 'muda' (sin lectura) y agregarle la frase que la interpreta.",
    errores=[
        ("“Pego mis tablas y ya están los resultados.”",
         "Eso es un 'data dump'. Cada tabla necesita una lectura: qué se ve y qué significa."),
        ("“Mi opinión sobre el tema es un hallazgo.”",
         "No: el hallazgo se sostiene en un dato. Opinión sin dato no entra."),
        ("“Analizo cosas que no pregunté porque son interesantes.”",
         "Analice solo lo que responde a un objetivo; lo demás dispersa."),
        ("“Tengo el dato pero no sé a qué objetivo va.”",
         "Si no responde a ningún objetivo, revise: o el dato sobra o falta un objetivo."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 07. Ya tienen datos —o los están recogiendo—. Hoy aprendemos lo que separa un buen artículo de uno mediocre: convertir **datos en hallazgos**. Porque el dato en bruto no dice nada; el hallazgo sí.”

> “**Slide 2 — OBJETIVOS.** Distinguir dato, hallazgo y resultado; analizar según el enfoque; y armar una **tabla de hallazgos** que conecte cada dato con un objetivo. Tengan a la mano lo que hayan recogido con su instrumento.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Tres palabras que muchos confunden. **Dato**: 'el despliegue tardó 42 minutos'. **Hallazgo**: 'eso casi duplica el estándar del equipo' —ahí ya interpreté—. **Resultado**: el hallazgo que **responde a un objetivo**. Si entregan datos y creen que entregaron resultados, les falta el paso del medio: interpretar.”

> “**Slide 4 — ENFOQUE DE HOY.** ¿Cómo se analiza? Si es cuantitativo: promedios, frecuencias, porcentajes, tablas —pero cada tabla con su **lectura en prosa**—. Si es cualitativo: codifican, agrupan en categorías y buscan patrones. Y si es obra-creación: describen las decisiones de diseño y qué aprendieron en cada iteración del prototipo.”

> “La advertencia del día: el **'data dump'**. Pegar diez tablas sin leerlas no es análisis, es un volcado. Si una tabla no tiene una frase que la explique, sobra.”""",
    fase3_texto="""**Protagonista:** Docente (modela el paso dato→hallazgo→resultado).

**En pantalla (Google Docs):** una tabla de hallazgos en blanco.

**GUION LITERAL:**
> “Modelo el recorrido. Dato crudo: '42 minutos por despliegue'. ¿Qué significa? Comparo con el estándar del equipo, que es 20: hallazgo, 'el tiempo actual casi duplica el estándar'. ¿A qué objetivo responde? A 'caracterizar el proceso actual'. Ahí ya es un resultado. Miren cómo el mismo número pasó de mudo a hablar.”

> “Ahora les muestro una tabla muda —solo números— y le agrego dos frases: 'se observa que… lo que indica que…'. Esa frase es la diferencia entre un anexo y un resultado. Repítanlo con cada tabla y cada gráfico.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S07_AnalisisHallazgos_Apellido`: (1) armen una **tabla de hallazgos** con columnas *dato · hallazgo · objetivo que responde*, mínimo 3 filas; (2) escriban **una página de lectura** en prosa que interprete esos hallazgos —qué se ve y qué significa—. Nada de tablas mudas.”

> “Criterio de éxito: cada dato tiene su interpretación y se amarra a un objetivo; si leo su página, entiendo qué encontró sin ver las tablas.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Pega tablas sin interpretarlas | “Agregue la frase: 'se observa X, lo que significa Y'.” |
| Confunde opinión con hallazgo | “¿Qué dato sostiene eso? Sin dato, no es hallazgo.” |
| Analiza lo que no preguntó | “¿A qué objetivo responde? Si a ninguno, quítelo.” |
| No sabe si es dato o hallazgo | “Dato es el número; hallazgo es lo que ese número significa.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) dato, hallazgo y resultado no son lo mismo —la clave es interpretar—; (2) cada tabla lleva su lectura; (3) todo hallazgo se amarra a un objetivo.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S07_AnalisisHallazgos_Apellido` a CDigital. Estos hallazgos son la materia prima de la discusión. La próxima sesión cerramos la **Fase III de referentes y el marco teórico** para poder discutir con autores.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    8,
    fundamento="""> Sesión de cierre del marco: la meta es teoría **suficiente y usable**, no una enciclopedia. Léalo completo.

#### 1. "Suficiente y usable": cuándo parar de buscar
El marco teórico tiene un defecto tentador: se puede agrandar hasta el infinito. La **Fase III** es la de **cerrar huecos**, no la de abrir temas nuevos. Criterio de **saturación teórica**: se para cuando las nuevas fuentes ya no aportan conceptos nuevos, solo repiten. Un marco cerrado es el que **tiene lo necesario para sostener la discusión** de la Sesión 09, ni más ni menos.

#### 2. Organizar por constructos (no por autores)
El marco se estructura por los **conceptos clave de la pregunta** (constructos), no autor por autor. Si la pregunta habla de "automatización de pruebas" y "tiempo de despliegue", esos son los dos constructos, y bajo cada uno entran los autores que aportan. Así el marco es un argumento, no una lista de resúmenes.

| Constructo | Qué debe quedar claro | Fuentes que lo sostienen |
| :--- | :--- | :--- |
| Automatización de pruebas | Definición, tipos, beneficios/riesgos | Autores A, B, C |
| Tiempo de despliegue | Cómo se mide, qué lo afecta | Autores D, E |
| Relación entre ambos | Qué dice la literatura del vínculo | Autores F, G |

#### 3. El conteo hacia las 50 referencias
Este es buen momento para **auditar el conteo**: cuántas referencias hay **citadas en el cuerpo** (no solo listadas) y cuántas faltan para las 50 que exige el Syllabus. Una referencia listada pero no citada no cuenta y, peor, es una alarma para el jurado.

#### 4. El puente marco → discusión
El marco no termina en sí mismo: prepara la **discusión**. Cada autor que se cierra aquí es alguien con quien luego se dialogará ("mis hallazgos confirman / contradicen / extienden a X"). Salga de esta sesión con claridad de **qué autores citará en la discusión**.""",
    ejemplo="Mostrar un marco 'de autores' (Autor 1 dice…, Autor 2 dice…) y reorganizarlo en vivo por constructos; luego auditar en pantalla cuántas referencias están realmente citadas en el cuerpo vs. solo listadas.",
    errores=[
        ("“Sigo agregando teoría, nunca siento que es suficiente.”",
         "Aplique saturación: pare cuando las fuentes solo repiten. El marco es 'suficiente y usable', no infinito."),
        ("“Organizo el marco autor por autor.”",
         "Organícelo por constructos; los autores entran bajo el concepto que sostienen."),
        ("“Tengo 50 referencias en la lista.”",
         "¿Cuántas están citadas en el cuerpo? Las que solo están listadas no cuentan y alertan al jurado."),
        ("“El marco no tiene nada que ver con lo que voy a discutir.”",
         "Cada autor del marco debe ser alguien con quien luego dialogar en la discusión."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 08. Hoy **cerramos** el marco teórico. Y la palabra clave es 'cerrar': no vamos a abrir temas nuevos, vamos a rematar lo que falta. La meta es teoría **suficiente y usable**, no una enciclopedia.”

> “**Slide 2 — OBJETIVOS.** Aplicar el criterio de saturación para saber cuándo parar, organizar el marco por **constructos**, auditar el conteo hacia las 50 referencias y dejar claro qué autores citaremos en la discusión. Tengan abierto su marco y sus fichas.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** El marco tiene una trampa: se puede agrandar hasta el infinito. Por eso existe la **saturación teórica**: paran cuando las fuentes nuevas ya no aportan conceptos, solo repiten. Un marco cerrado es el que tiene lo necesario para **sostener la discusión**, ni más ni menos.”

> “Y se organiza por **constructos**, no autor por autor. Si su pregunta habla de 'automatización de pruebas' y 'tiempo de despliegue', esos son sus constructos; debajo de cada uno entran los autores. Así el marco es un argumento, no una lista de resúmenes.”

> “**Slide 4 — ENFOQUE DE HOY.** Momento de auditar: ¿cuántas referencias tienen **citadas en el cuerpo**, no solo en la lista? El Syllabus pide 50. Una referencia listada y no citada no cuenta, y para el jurado es una alarma. Cada autor que cierran hoy es alguien con quien van a dialogar en la discusión de la próxima sesión.”""",
    fase3_texto="""**Protagonista:** Docente (modela reorganización + auditoría).

**En pantalla (Google Docs):** un marco 'de autores' y una tabla de constructos.

**GUION LITERAL:**
> “Modelo la reorganización. Aquí tengo un marco malo: 'Pérez dice…, luego González dice…, luego Ramírez dice…'. Lo reordeno por constructos: creo el bloque 'automatización de pruebas' y meto a Pérez y Ramírez ahí porque ambos hablan de eso; creo 'tiempo de despliegue' y meto a González. De golpe se lee como argumento.”

> “Ahora audito el conteo: uso Buscar (Ctrl+F) sobre el cuerpo y cuento cuántas citas reales hay. Tengo 34 citadas, aunque la lista tiene 41. Conclusión: siete están de adorno y me faltan referencias reales. Eso lo veo hoy, no en la sustentación.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S08_MarcoCierre_Apellido`: (1) reorganicen su marco **por constructos** (mínimo 2–3) y verifiquen que cada uno queda cerrado; (2) auditen el conteo: cuántas referencias citadas en el cuerpo tienen y cuántas faltan para 50; (3) hagan una **lista de huecos resueltos** y de los que quedan pendientes para autónomo.”

> “Criterio de éxito: el marco se lee como argumento por constructos y el conteo de referencias citadas es real, no inflado.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Quiere seguir agregando teoría | “¿Aporta algo nuevo o solo repite? Si repite, ciérrelo.” |
| Marco autor por autor | “Reagrúpelo por constructo; el autor va bajo el concepto.” |
| Cree que tiene 50 porque están en la lista | “Cuente las citadas en el cuerpo con Ctrl+F; esas son las que valen.” |
| Marco desconectado de la pregunta | “Si un bloque no sirve para discutir, sobra.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) marco 'suficiente y usable' —saturación, no infinito—; (2) se organiza por constructos; (3) cuentan las referencias **citadas en el cuerpo**, camino a las 50.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S08_MarcoCierre_Apellido` a CDigital y, en autónomo, cierren los huecos de referencias pendientes. La próxima sesión es el corazón del nuevo conocimiento: **resultados, discusión y relación con referentes**.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    9,
    fundamento="""> El corazón del artículo: aquí se demuestra que hay **nuevo conocimiento**. Léalo completo.

#### 1. Resultados ≠ discusión (la separación que todos violan)
- **Resultados:** qué se encontró, en tono **neutral**, sin interpretar. "El tiempo de despliegue bajó de 42 a 18 minutos".
- **Discusión:** qué **significa** eso, en **diálogo con los autores** del marco. "Esta reducción confirma lo que reporta X (2022) sobre automatización…".

Meter interpretación en resultados, o repetir resultados en discusión, es el error de forma más penalizado.

#### 2. La estructura de una buena discusión
Cada párrafo de discusión sigue el mismo latido:
1. **Retomar** un hallazgo.
2. **Confrontarlo** con un autor: ¿lo confirma, lo contradice, lo extiende?
3. **Implicación:** qué significa para el problema.
4. **Límite:** qué no se puede concluir todavía.

| Hallazgo | Autor (confirma/contradice/extiende) | Implicación |
| :--- | :--- | :--- |
| El tiempo bajó a la mitad | Confirma a X (2022) | La automatización sí impacta el despliegue |
| Aparecieron 2 fallos nuevos | Contradice a Y (2020) | El contexto local matiza el hallazgo |

#### 3. Responder los objetivos, uno por uno
La discusión debe **cerrar cada objetivo específico**. Si un objetivo no aparece respondido, el jurado lo notará. Buena práctica: subtítulos o párrafos ordenados por objetivo.

#### 4. Honestidad científica
Reportar también **lo que no salió** o lo que contradice la expectativa. Ocultarlo debilita el artículo y es un problema de integridad. Un buen investigador discute sus **limitaciones**: eso da credibilidad, no la quita. El flujo de citas está en la guía transversal `Guiones/Guía práctica - Herramientas de escritura y citación.md`.""",
    ejemplo="En pantalla, escribir un párrafo de discusión con el latido completo: retomar hallazgo → confrontar con autor (confirma/contradice) → implicación → límite; contrastarlo con un párrafo que solo repite el resultado.",
    errores=[
        ("“En resultados ya explico qué significa cada dato.”",
         "No: resultados es neutral (qué encontró). El significado va en discusión."),
        ("“En la discusión repito lo que dije en resultados.”",
         "La discusión dialoga con autores; si solo repite, no aporta. Confronte con la literatura."),
        ("“Oculto el dato que contradice mi hipótesis.”",
         "Repórtelo: la honestidad da credibilidad. Discuta la limitación, no la esconda."),
        ("“Un objetivo quedó sin responder, pero nadie lo notará.”",
         "El jurado lo nota. La discusión debe cerrar cada objetivo específico."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 09. Llegamos al corazón del artículo: **resultados y discusión**. Aquí es donde se demuestra que su trabajo produjo algo nuevo. Y aquí también está el error de forma que más se penaliza: mezclar las dos cosas.”

> “**Slide 2 — OBJETIVOS.** Separar resultados de discusión, escribir una discusión que **dialogue con los referentes**, responder cada objetivo y hacerlo con honestidad científica. Tengan abierta su tabla de hallazgos de la Sesión 07 y su marco de la Sesión 08.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Dos secciones, dos tareas distintas. **Resultados**: qué encontré, neutral, sin interpretar —'el tiempo bajó de 42 a 18 minutos'—. **Discusión**: qué significa, dialogando con los autores —'esto confirma lo que reporta X en 2022'—. Interpretar en resultados o repetir resultados en discusión es el error más castigado.”

> “**Slide 4 — ENFOQUE DE HOY.** Cada párrafo de discusión tiene el mismo latido: retomo un hallazgo, lo confronto con un autor —¿lo confirma, lo contradice, lo extiende?—, digo la implicación y reconozco un límite. Y algo serio: reporten también **lo que no salió**. Ocultar un dato que contradice su hipótesis debilita el artículo; discutir sus limitaciones, al contrario, les da credibilidad.”

> “Y no olviden: la discusión debe **responder cada objetivo específico**. Si uno queda huérfano, el jurado lo va a ver.”""",
    fase3_texto="""**Protagonista:** Docente (modela un párrafo de discusión).

**En pantalla (Google Docs):** un párrafo de resultado y uno de discusión, lado a lado.

**GUION LITERAL:**
> “Modelo el latido. Retomo el hallazgo: 'el tiempo de despliegue se redujo a la mitad'. Lo confronto: 'esto **confirma** lo reportado por X (2022), quien halló mejoras similares'. Implicación: 'la automatización impacta directamente el despliegue en equipos pequeños'. Y el límite: 'aunque en este caso aparecieron dos fallos nuevos, lo que **matiza** el resultado y coincide con la advertencia de Y (2020)'. Ese párrafo dialoga; no repite.”

> “Ahora les muestro el párrafo malo: 'el tiempo bajó a 18 minutos. Fue una mejora'. Eso ya lo dije en resultados. No aporta. La diferencia es citar y confrontar.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S09_ResultadosDiscusion_Apellido`: (1) redacten sus **resultados** en tono neutral (apoyados en la tabla de hallazgos); (2) escriban al menos **dos párrafos de discusión** con el latido completo —hallazgo → autor que confirma/contradice → implicación → límite—; (3) verifiquen que cada **objetivo específico** queda respondido.”

> “Criterio de éxito: resultados sin interpretación, discusión con al menos dos autores citados, y ningún objetivo huérfano.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Interpreta dentro de resultados | “Guarde el 'significa que' para la discusión; aquí solo el dato.” |
| Discute sin citar a nadie | “¿Quién de su marco confirma o contradice esto? Cítelo.” |
| Esconde lo que no salió | “Repórtelo como limitación; eso da credibilidad.” |
| Dejó un objetivo sin responder | “Agregue el párrafo que cierra ese objetivo.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) resultados neutral, discusión interpreta; (2) la discusión dialoga con autores, no repite; (3) se responde cada objetivo y se es honesto con lo que no salió.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S09_ResultadosDiscusion_Apellido` a CDigital. Con esto el cuerpo del artículo está casi completo. La próxima sesión le ponemos la cabeza y la cola: **resumen, palabras clave UNESCO, conclusiones y referencias**.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    10,
    fundamento="""> Sesión de culminación formal del artículo: lo que se escribe **al final**. Léalo completo.

#### 1. El resumen se escribe al final (y por algo)
El **resumen (abstract)** condensa todo el artículo en ~200–250 palabras, y por eso se redacta al final: solo ahora se sabe qué resultado resumir. Estructura: **contexto → objetivo → método → resultado principal → conclusión**. Sin citas, sin abreviaturas sin definir, sin "en este artículo se hablará de…". Es un espejo del trabajo completo.

#### 2. Palabras clave del tesauro UNESCO
Las **palabras clave** no se inventan: se eligen de un **vocabulario controlado**, el tesauro de la UNESCO. ¿Por qué? Para que el artículo sea **encontrable**: si todos usamos los mismos términos normalizados, las búsquedas funcionan. Se eligen 3–5 términos que un investigador usaría para encontrar este trabajo. Contrastarlos con el uso real en Scholar ayuda a validarlos.

#### 3. Conclusiones ≠ resumen de resultados
Las conclusiones **responden la pregunta de investigación**, no repiten los resultados. Incluyen: respuesta a la pregunta, cumplimiento de objetivos, **limitaciones** y **trabajo futuro**. No se introducen ideas nuevas ni datos que no aparecieron antes.

| Sección de cierre | Qué debe tener | Error típico |
| :--- | :--- | :--- |
| Resumen | Contexto→objetivo→método→resultado→conclusión, ~200–250 pal. | Escribirlo primero, con citas |
| Palabras clave | 3–5 términos del tesauro UNESCO | Inventar términos "bonitos" |
| Conclusiones | Responden la pregunta + límites + futuro | Repetir resultados o traer ideas nuevas |
| Referencias | ≥ 50, APA 7, orden alfabético, sangría francesa | Huérfanas (citadas o listadas de más) |

#### 4. Referencias sin huérfanas (ZoteroBib)
La lista de referencias debe cumplir: **≥ 50**, APA 7, orden alfabético y sin **huérfanas** (toda cita del cuerpo está en la lista, y toda entrada de la lista se cita). ZoteroBib (zbib.org) genera y ordena todo sin instalar nada; el flujo está en `Guiones/Guía práctica - Herramientas de escritura y citación.md`.""",
    ejemplo="En pantalla, escribir un resumen de ~200 palabras con la estructura contexto→objetivo→método→resultado→conclusión; luego elegir 4 palabras clave contrastándolas con el tesauro UNESCO y con el uso en Scholar.",
    errores=[
        ("“Escribo el resumen ahora para ir adelantando.”",
         "El resumen se escribe al final: solo entonces sabe qué resultado resumir."),
        ("“Pongo como palabras clave las que suenan bien.”",
         "Elíjalas del tesauro UNESCO; son vocabulario controlado para que el artículo sea encontrable."),
        ("“En conclusiones repito los resultados.”",
         "Las conclusiones responden la pregunta e incluyen límites y trabajo futuro; no repiten."),
        ("“Tengo citas en el cuerpo que no están en la lista.”",
         "Son huérfanas: toda cita va en la lista y toda entrada se cita. ZoteroBib ayuda a cuadrarlo."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 10. El cuerpo del artículo ya está; hoy le ponemos la **cabeza y la cola**: el resumen, las palabras clave, las conclusiones y las referencias. Todo esto se escribe **al final**, y hay una razón para cada cosa.”

> “**Slide 2 — OBJETIVOS.** Redactar un resumen que sea espejo del artículo, elegir palabras clave del **tesauro UNESCO**, escribir conclusiones que respondan la pregunta y cuadrar las referencias en APA 7 sin huérfanas. Tengan el artículo completo a la vista.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** El **resumen** se escribe de último porque solo ahora saben qué resultado resumir. Son ~200–250 palabras con cinco piezas: contexto, objetivo, método, resultado principal y conclusión. Sin citas, sin abreviaturas raras, sin 'en este artículo se hablará de…'. Es un espejo del trabajo.”

> “Las **palabras clave** no se inventan: se sacan del **tesauro UNESCO**, un vocabulario controlado. ¿Por qué? Para que el artículo sea **encontrable**. Elijan 3–5 términos que otro investigador usaría para dar con su trabajo.”

> “**Slide 4 — ENFOQUE DE HOY.** Las **conclusiones** responden la pregunta —no repiten resultados— e incluyen límites y trabajo futuro. Y las **referencias**: mínimo 50, APA 7, orden alfabético y **sin huérfanas**: toda cita del cuerpo está en la lista, y toda entrada de la lista se cita. ZoteroBib les cuadra eso sin instalar nada.”""",
    fase3_texto="""**Protagonista:** Docente (modela resumen + keywords).

**En pantalla (Google Docs + Scholar):** un resumen en construcción y una búsqueda de términos.

**GUION LITERAL:**
> “Modelo el resumen. Escribo pieza por pieza: contexto —'el despliegue continuo depende de pruebas confiables'—; objetivo —'este estudio evaluó el efecto de automatizarlas'—; método —'cuasi-experimento en el equipo X'—; resultado —'el tiempo bajó a la mitad'—; conclusión —'la automatización mejora el despliegue en equipos pequeños'—. Cuento palabras: 210. Perfecto.”

> “Ahora las keywords. Pienso 'automatización de pruebas', 'integración continua', 'tiempo de despliegue'. Las contrasto en Scholar para ver si así las nombran los autores, y las ajusto al término normalizado del tesauro UNESCO. Cuatro palabras clave, y mi artículo se vuelve encontrable.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S10_CierreArticulo_Apellido`: (1) escriban el **resumen** (~200–250 palabras, cinco piezas); (2) elijan **4–5 palabras clave** del tesauro UNESCO; (3) redacten las **conclusiones** respondiendo la pregunta, con límites y trabajo futuro; (4) revisen las **referencias** en ZoteroBib: conteo hacia 50, APA 7 y sin huérfanas.”

> “Criterio de éxito: el resumen se entiende solo, las keywords son términos reales, las conclusiones responden la pregunta y la lista de referencias no tiene huérfanas.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Mete citas en el resumen | “Quítelas; el resumen no cita, solo sintetiza.” |
| Inventa palabras clave | “Contraste con el tesauro UNESCO y con Scholar; use términos reales.” |
| Repite resultados en conclusiones | “Aquí responde la pregunta; agregue límites y trabajo futuro.” |
| Tiene citas fuera de la lista | “Son huérfanas; cuádrelas en ZoteroBib antes de cerrar.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el resumen es un espejo del artículo y se escribe al final; (2) las palabras clave vienen del tesauro UNESCO; (3) las conclusiones responden la pregunta y las referencias van sin huérfanas, camino a las 50.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S10_CierreArticulo_Apellido` a CDigital. El artículo debería estar completo. La próxima sesión preparamos la divulgación: **póster, evidencias y verificación antiplagio**.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    11,
    fundamento="""> Sesión de alistamiento para la sustentación + integridad académica. Léalo completo; el antiplagio se explica bien o genera pánico injustificado.

#### 1. El póster NO es el artículo en miniatura
Un póster es una **pieza de divulgación visual**: se lee de lejos, en un minuto, y cuenta lo esencial. Bloques mínimos: **título, problema, método, hallazgo principal, conclusión** y una imagen/gráfico. Pegar el artículo con letra 8 es el error clásico. Regla: si no se lee a un metro de distancia, sobra texto.

| Bloque del póster | Contenido | Espacio |
| :--- | :--- | :--- |
| Título + autor | Corto, legible de lejos | Cabecera |
| Problema y pregunta | 2–3 líneas | Columna 1 |
| Método | Diagrama o 3 pasos | Columna 1–2 |
| Hallazgo principal | 1 gráfico + 1 frase | Columna 2 (centro visual) |
| Conclusión | 1–2 líneas | Columna 3 |

Herramienta: **Canva free** o **Google Docs/Slides** (nube, gratis).

#### 2. Evidencias y anexos de la obra-creación
Los anexos respaldan el proceso: capturas del prototipo, instrumento aplicado, bitácora, consentimientos. Cada anexo se **referencia** desde el cuerpo ("ver Anexo A") y se **rotula**. No se anexa "todo lo que hay"; se anexa lo que sustenta.

#### 3. Antiplagio: qué mide y qué no
El software de similitud mide **coincidencia textual** con otras fuentes; **no** mide plagio por sí solo (una cita bien hecha también coincide). Un porcentaje alto suele venir de **parafraseo deficiente** o de no citar. La forma correcta de bajarlo no es "trucos", sino **reescribir con las propias palabras y citar bien**. La verificación se hace por la **ruta institucional en CDigital** (no se promocionan URLs de terceros; usar la del semestre).

#### 4. Integridad = citar lo prestado
Todo lo que no es propio se cita: texto, ideas, imágenes, código. Parafrasear no es cambiar tres palabras; es **reexpresar la idea** y aun así citar la fuente. Esto cierra el hilo abierto en co-creación (Sesión 06).""",
    ejemplo="En Canva free o Google Slides, montar el esqueleto de un póster (título, problema, método, hallazgo con gráfico, conclusión) mostrando jerarquía visual; luego tomar un párrafo 'copiado' y reescribirlo parafraseado + citado para mostrar cómo baja la similitud legítimamente.",
    errores=[
        ("“Pego el artículo completo en el póster.”",
         "El póster es divulgación visual, no el artículo en miniatura. Si no se lee a un metro, sobra texto."),
        ("“Tengo 40% de similitud, hago trucos para bajarlo.”",
         "No haga trucos: reescriba con sus palabras y cite bien. El % baja de forma legítima."),
        ("“Parafrasear es cambiar tres palabras.”",
         "Parafrasear es reexpresar la idea completa con sus palabras, y aun así citar la fuente."),
        ("“Anexo todo lo que tengo por si acaso.”",
         "Anexe solo lo que sustenta, rotulado y referenciado desde el cuerpo ('ver Anexo A')."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 11. Entramos en la recta de la sustentación. Hoy preparamos tres cosas: el **póster**, las **evidencias** para anexos y la **verificación antiplagio**. Y quiero desmontar de una el pánico: el antiplagio no muerde si citan bien.”

> “**Slide 2 — OBJETIVOS.** Diseñar un póster que sea divulgación visual —no el artículo pegado—, organizar los anexos de la obra-creación, y entender qué mide de verdad el software de similitud. Tengan su artículo y sus evidencias del prototipo a la mano.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** El póster **no** es el artículo en miniatura. Es una pieza que se lee de lejos, en un minuto: título, problema, método, hallazgo principal, conclusión y una imagen. El error clásico es pegar el artículo con letra 8. Regla: si no se lee a un metro, sobra texto. Se hace en **Canva free** o en Google Slides, gratis y en la nube.”

> “**Slide 4 — ENFOQUE DE HOY.** Ahora el antiplagio, sin mitos. El software mide **coincidencia textual**, no plagio por sí mismo: una cita bien hecha también coincide. Un porcentaje alto casi siempre viene de **parafraseo malo** o de no citar. ¿La forma de bajarlo? No trucos: **reescribir con sus palabras y citar bien**. La verificación se hace por la **ruta institucional en CDigital**; no busquen páginas de terceros. Y esto cierra lo que dijimos en co-creación: todo lo prestado se cita.”""",
    fase3_texto="""**Protagonista:** Docente (modela póster + parafraseo).

**En pantalla (Canva free / Google Slides + Google Docs):** un lienzo de póster y un párrafo a reescribir.

**GUION LITERAL:**
> “Modelo el póster. Abro Canva free, plantilla de póster. Pongo el título arriba, grande. Columna 1: problema y método en tres pasos. Centro: el gráfico del hallazgo, que es lo que el ojo busca primero. Columna 3: la conclusión en dos líneas. Nada de párrafos largos: bloques cortos y una imagen que manda.”

> “Ahora el antiplagio en vivo. Tomo un párrafo que quedó muy pegado a la fuente y lo **parafraseo de verdad**: no cambio tres palabras, reexpreso la idea con mi voz, y **igual cito** al autor. Así el porcentaje de similitud baja de forma legítima y el jurado ve rigor, no trampa.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S11_PosterEvidencias_Apellido`: (1) monten el **póster de una página** (Canva free o Slides) con los bloques problema-método-hallazgo-conclusión; (2) armen la **lista de anexos** rotulados y referenciados desde el cuerpo; (3) identifiquen en su artículo un párrafo con riesgo de similitud y **parafraséenlo + cítenlo**. Dejen por escrito **cómo opera la revisión de similitud en el aula** según lo que confirmó el Docente: cuándo ocurre y si el curso pide adjuntar algún informe.”

> “Criterio de éxito: el póster se entiende a un metro, los anexos están referenciados, y el párrafo reescrito conserva la idea con voz propia y su cita.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Pega texto largo en el póster | “Recorte a bloques; si no se lee de lejos, fuera.” |
| Entra en pánico por el % | “No es plagio automático; revise parafraseo y citas.” |
| Cambia tres palabras y cree parafrasear | “Reexprese la idea entera con su voz, y cite igual.” |
| Anexa todo sin rotular | “Deje solo lo que sustenta; rotúlelo y refiéralo desde el cuerpo.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el póster es divulgación visual, no el artículo pegado; (2) los anexos se seleccionan, rotulan y referencian; (3) el antiplagio mide coincidencia —se resuelve parafraseando bien y citando, por la ruta institucional—.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S11_PosterEvidencias_Apellido` a CDigital. **Si el curso exige verificación de similitud, yo les indico la ruta institucional**; no busquen servicios externos. La próxima sesión es grande: **ensayo de la sustentación ante jurados**.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    12,
    fundamento=f"""> Sesión decisiva: se ensaya la **sustentación ante pares y jurados**, el hito académico que valida el trabajo del periodo. Léalo completo.

#### 1. Qué es y dónde se registra la nota
El Syllabus 94532 describía una evaluación de «corte único» con dos componentes (EV05 / EXAM). **El aula no funciona así**: el libro de calificaciones de CDigital tiene **tres cortes** y estos ítems — {desglose('tg3')}. La sustentación es **requisito académico del programa**, y su valoración la registra el Docente dentro de los ítems del **tercer corte** ({items_corte_txt('tg3', 3)}), que es el corte que cierra el periodo.

> **Antes de dictar esta sesión:** confirme con la Dirección del Programa **en qué ítem** del aula queda la nota de la sustentación y dígalo así de claro en clase. Lo que **no** se puede hacer es anunciar «la sustentación vale el 50%»: ese porcentaje no existe en el libro de calificaciones de ninguno de los tres grupos.

El jurado evalúa **dominio del tema, claridad, coherencia del artículo y capacidad de defensa** (no la belleza de las diapositivas). Hoy es el **ensayo**; la sustentación real es ante los jurados asignados por la Dirección del Programa.

#### 2. Estructura del guion oral (10–12 min)
El tiempo es nota: pasarse o quedarse corto resta. Reparto sugerido:

| Bloque | Minutos | Qué se dice |
| :--- | :---: | :--- |
| Problema y pregunta | 2 | Por qué importa, qué se preguntó |
| Objetivos | 1 | Qué se propuso |
| Método | 2–3 | Cómo lo hizo (matriz, instrumento) |
| Resultados y hallazgos | 3 | Qué encontró (con 1–2 datos fuertes) |
| Discusión y conclusión | 2–3 | Qué significa, respuesta a la pregunta |
| Aporte / cierre | 1 | Qué deja al conocimiento |

#### 3. Anticipar las preguntas del jurado
El jurado pregunta casi siempre lo mismo. Prepararlas quita el 80% del miedo:

| Pregunta típica del jurado | Respuesta corta modelo |
| :--- | :--- |
| ¿Por qué eligió ese método? | "Porque responde al objetivo X; lo alineé en la matriz de consistencia." |
| ¿Cuáles son las limitaciones? | "El tamaño de muestra / el contexto local; por eso no generalizo." |
| ¿Qué aporta su trabajo? | "Evidencia local sobre X, y un prototipo replicable." |
| ¿Cómo garantiza la validez? | "Instrumento alineado a objetivos + triangulación / datos reales." |

#### 4. Nervios, tiempo y el "no sé"
Las diapositivas se **apoyan**, no se leen. Ante una pregunta que no sabe: honestidad breve + reconducir a lo que sí domina ("no lo medí en este estudio; sería trabajo futuro"). Nunca inventar. Practicar con cronómetro es la mejor vacuna contra el nervio.""",
    ejemplo="Modelar 2 minutos de sustentación con cronómetro visible (problema→pregunta→objetivos), y luego dramatizar una pregunta difícil del jurado con una respuesta corta y honesta vs. una respuesta inventada.",
    errores=[
        ("“Leo las diapositivas durante la sustentación.”",
         "Las diapositivas se apoyan, no se leen. El jurado evalúa dominio, no lectura."),
        ("“Si me preguntan algo que no sé, improviso una respuesta.”",
         "No invente: reconozca con honestidad y reconduzca a lo que sí domina o a trabajo futuro."),
        ("“El tiempo no importa, si me extiendo es porque sé.”",
         "El tiempo es nota. Pasarse resta; ensaye con cronómetro para caber en 10–12 min."),
        ("“Meto todo el artículo en las diapositivas.”",
         "Diapositivas con párrafos = lectura. Use frases y visuales; el contenido lo pone su voz."),
    ],
    fase1_texto=f"""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 12. Hoy ensayamos la **sustentación ante jurados**. Y quiero ser exacto con lo que les digo de la nota, porque circulan cifras viejas: en el aula, el **tercer corte** vale {peso_corte_txt('tg3', 3)} y está compuesto por **{items_corte_txt('tg3', 3)}**. La sustentación es el hito con el que el programa valida su trabajo, y lo que ustedes defiendan ahí es lo mismo que quedó escrito en la **ACA Final**. No hay un ítem llamado ‘examen’ que valga la mitad del curso: eso era del Syllabus viejo.”

> “**Slide 2 — OBJETIVOS.** Armar un guion oral de 10–12 minutos, **anticipar las preguntas** del jurado y ensayar con cronómetro. Esto es un simulacro: la defensa real es ante los jurados que asigna la Dirección del Programa. Tengan su artículo y su póster listos.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** El jurado evalúa cuatro cosas: **dominio del tema, claridad, coherencia del artículo y capacidad de defensa**. No evalúa lo bonitas que sean las diapositivas. Así que las diapositivas se **apoyan**, no se leen. Si leen, pierden dominio ante los ojos del jurado.”

> “El guion dura 10–12 minutos y el tiempo es nota. Reparto: dos minutos de problema y pregunta, uno de objetivos, dos o tres de método, tres de resultados, dos o tres de discusión y conclusión, y uno de aporte. Ensáyenlo con cronómetro: pasarse resta, quedarse corto también.”

> “**Slide 4 — ENFOQUE DE HOY.** Y la mejor vacuna contra el miedo: **anticipar las preguntas**. El jurado pregunta casi siempre lo mismo —por qué ese método, cuáles son las limitaciones, qué aporta, cómo garantiza la validez—. Si traen esas respuestas preparadas, se les va el 80% del nervio. Y si preguntan algo que no saben: honestidad breve y reconducen; nunca inventen.”""",
    fase3_texto="""**Protagonista:** Docente (modela sustentación + pregunta difícil).

**En pantalla (cronómetro + guion en Google Docs):** temporizador visible y el guion oral.

**GUION LITERAL:**
> “Modelo los primeros dos minutos con el cronómetro corriendo. 'Buenas tardes, jurados. Mi trabajo aborda un problema del equipo X: los despliegues son lentos y manuales. La pregunta fue: ¿en qué medida automatizar las pruebas reduce ese tiempo? Los objetivos fueron…'. Fíjense: miro al frente, no leo la slide, y voy justo en tiempo.”

> “Ahora dramatizo una pregunta difícil. Jurado: '¿por qué no usó una muestra más grande?'. Respuesta buena: 'Fue una limitación de alcance; trabajé con el equipo disponible este periodo, por eso no generalizo y lo dejo como trabajo futuro'. Respuesta mala: inventar un número que no medí. La honestidad breve **suma**; la invención **hunde**.”""",
    fase4_texto="""**Protagonista:** Estudiantes (ensayo por parejas) · Docente cronometra y observa.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos, en parejas. Uno sustenta con **cronómetro** mientras el otro toma notas de claridad y tiempo; luego cambian. Cada quien entrega `S12_GuionSustentacion_Apellido` con: (1) el **guion oral** por bloques con sus minutos; (2) **5 preguntas difíciles** que anticipa del jurado, cada una con una **respuesta corta**.”

> “Criterio de éxito: el guion cabe en 10–12 minutos, no se lee de las diapositivas, y las 5 respuestas son concretas y honestas.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Lee la diapositiva | “Míreme a mí; la slide es apoyo, el contenido lo pone su voz.” |
| Se pasa del tiempo | “Recorte; el tiempo es nota. ¿Qué bloque está inflado?” |
| No sabe qué preguntará el jurado | “Anticipe: método, limitaciones, aporte, validez. Prepárelas.” |
| Inventa una respuesta | “Mejor reconozca el límite y reconduzca a trabajo futuro.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) la sustentación es el hito que valida el trabajo del periodo, y lo que se defiende es la **ACA Final** que ya vienen escribiendo; (2) el jurado evalúa dominio, no diapositivas —no se lee—; (3) anticipar las preguntas y ensayar con cronómetro quita el miedo.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S12_GuionSustentacion_Apellido` a CDigital y sigan ensayando en voz alta, con reloj. La próxima sesión preparamos los **entregables para el repositorio institucional**.”

> “**Slide 7 — Cierre.** Gracias, y a practicar; mismo Meet.”""",
)

_tg3(
    13,
    fundamento="""> Sesión de empaquetado final: el artículo va a un repositorio institucional para quedar público y permanente. Léalo completo.

#### 1. Qué es un repositorio institucional (y por qué importa)
Un **repositorio institucional** es el archivo digital donde la universidad **preserva y da visibilidad** a la producción académica. Que su artículo quede allí significa: permanencia, acceso público (según licencia) y un identificador estable para que otros lo citen. No es "subir un archivo más": es **publicar** su trabajo de grado.

#### 2. El paquete de entregables (checklist)
El repositorio exige un paquete completo y bien formado, según el **instructivo institucional del semestre** (no se inventan URLs ni formularios; se usa la ruta oficial en CDigital):

| Entregable | Detalle |
| :--- | :--- |
| Artículo final | PDF, plantilla APA CUN, ≥ 4.000 palabras, ≥ 50 refs |
| Metadatos | Título, autor(es), resumen, palabras clave UNESCO |
| Autorización de publicación | Formato institucional firmado |
| Anexos / evidencias | Rotulados, referenciados desde el cuerpo |
| Constancia antiplagio | Según ruta institucional CDigital |

#### 3. Metadatos y licencia
Los **metadatos** son los datos que describen el artículo para que sea buscable (título, autor, resumen, keywords). La **licencia** define qué pueden hacer otros con el trabajo. Cargar mal los metadatos hace que un buen artículo sea invisible.

#### 4. Forma antes de cargar
Antes de subir, revisión de forma: portada correcta, numeración, tablas rotuladas, referencias en APA 7 sin huérfanas, nombre de archivo consistente. Se carga la **versión final**, no un borrador. Un descuido de forma en el repositorio queda público.""",
    ejemplo="En pantalla, recorrer un checklist de entregables del repositorio marcando qué está listo y qué falta; mostrar cómo unos metadatos bien puestos (título + resumen + keywords UNESCO) hacen buscable el artículo.",
    errores=[
        ("“Subo el borrador y luego lo cambio.”",
         "Se carga la versión final; lo que queda en el repositorio es público y permanente."),
        ("“Los metadatos son opcionales.”",
         "Sin buenos metadatos el artículo es invisible; título, resumen y keywords UNESCO son obligatorios."),
        ("“Invento la URL del repositorio para el guion.”",
         "No se inventan URLs; use la ruta y el instructivo institucional del semestre en CDigital."),
        ("“El nombre del archivo da igual.”",
         "Debe ser consistente con la norma institucional; un nombre desordenado complica la recepción."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 13. Ya defendieron (o están por hacerlo). Hoy preparamos el **paquete para el repositorio institucional**. Ojo con esto: subir el artículo al repositorio es **publicarlo**: queda público y permanente. Por eso hoy trabajamos con lupa.”

> “**Slide 2 — OBJETIVOS.** Entender qué es el repositorio y por qué importa, armar el **checklist de entregables** completo, y dejar la versión final revisada en forma. Tengan a la mano su artículo final, sus anexos y —si el curso lo exige— el informe de similitud que haya indicado el Docente.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Un repositorio institucional es donde la universidad **preserva y da visibilidad** a la producción académica. Que su artículo quede ahí significa permanencia, acceso público y un identificador estable para que otros lo citen. No es 'subir un archivo más': es **publicar** su trabajo de grado.”

> “El paquete tiene piezas fijas: el **artículo final** en PDF con la plantilla APA CUN, los **metadatos** —título, autor, resumen, palabras clave UNESCO—, la **autorización de publicación** firmada, los **anexos** rotulados y, **si el curso lo exige**, el **informe de similitud**. Todo según el **instructivo institucional del semestre**; no inventamos URLs ni formularios, usamos la ruta oficial de CDigital.”

> “**Slide 4 — ENFOQUE DE HOY.** Dos detalles que hunden a buenos trabajos: **metadatos mal puestos** —que vuelven invisible el artículo— y **descuidos de forma** que quedan públicos. Se carga la **versión final**, no un borrador.”""",
    fase3_texto="""**Protagonista:** Docente (modela el checklist + metadatos).

**En pantalla (Google Docs / ruta CDigital del semestre):** un checklist de repositorio y un formulario de metadatos de ejemplo.

**GUION LITERAL:**
> “Modelo el checklist. Voy marcando: artículo final en PDF —listo—; ≥ 4.000 palabras y ≥ 50 referencias —verifico el conteo—; autorización firmada —falta—; anexos rotulados —a medias—; informe de similitud —sólo si el curso lo exige, según confirmó el Docente—. En dos minutos sé exactamente qué me falta para poder cargar.”

> “Ahora los metadatos. Pongo el título tal cual, el resumen que ya escribimos y las palabras clave UNESCO. Les muestro por qué importa: si el resumen y las keywords están bien, el artículo aparece en las búsquedas; si están vacíos o mal, el trabajo queda enterrado aunque sea excelente.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S13_PaqueteRepositorio_Apellido`: (1) armen el **checklist de entregables** del repositorio marcando listo/falta; (2) redacten los **metadatos** (título, resumen, keywords UNESCO); (3) hagan la **revisión de forma** de la versión final —portada, numeración, tablas rotuladas, referencias sin huérfanas, nombre de archivo—. Anoten la **ruta institucional** de carga del semestre.”

> “Criterio de éxito: el checklist muestra sin ambigüedad qué falta, los metadatos están completos, y la versión es la final, no un borrador.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Quiere subir un borrador | “Cargue la versión final; lo del repositorio es público.” |
| Deja los metadatos vacíos | “Sin metadatos el artículo es invisible; complételos.” |
| Pregunta la URL del repositorio | “Use la ruta del instructivo del semestre en CDigital; no inventamos enlaces.” |
| Nombre de archivo caótico | “Ajústelo a la norma institucional; facilita la recepción.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) el repositorio publica su trabajo —permanente y público—; (2) el paquete tiene piezas fijas: artículo, metadatos, autorización, anexos, antiplagio; (3) se carga la versión final, revisada en forma, por la ruta institucional.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S13_PaqueteRepositorio_Apellido` a CDigital y completen lo que quedó en 'falta'. La próxima sesión hacemos los **ajustes finales y el seguimiento post-sustentación** con las observaciones del jurado.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    14,
    fundamento="""> Sesión buffer: incorporar las correcciones del jurado con orden. Léalo completo. (Sin fechas de periodo en el guion; la logística vive en la Presentación del Curso / Manual.)

#### 1. Los ajustes del jurado son parte de la evaluación
Tras la sustentación, el jurado suele dejar **observaciones**. Atenderlas no es opcional: es parte de cerrar el trabajo de grado y una condición para la carga limpia al repositorio. Se registran en una **matriz de ajustes** para no perder ninguna.

| Observación del jurado | Cambio a realizar | Prioridad | Estado |
| :--- | :--- | :--- | :--- |
| "Falta discutir la limitación X" | Agregar párrafo en discusión | Crítica | Pendiente |
| "Una figura sin rótulo" | Rotular figura 3 | Menor | Hecho |
| "Revisar 2 referencias" | Corregir APA en la lista | Mayor | Pendiente |

#### 2. Priorizar: crítico, mayor, menor
No todos los ajustes pesan igual. **Críticos**: afectan la validez o una conclusión (van primero). **Mayores**: afectan una sección. **Menores**: forma. Se atienden en ese orden; lo crítico es obligatorio antes del repositorio.

#### 3. Incorporar sin romper la coherencia
Un cambio en resultados puede obligar a ajustar la discusión y las conclusiones. Se revisa el **efecto dominó**. Herramienta gratis y en la nube: el **historial de versiones de Google Docs** (Archivo → Historial de versiones) permite volver atrás si un cambio empeora las cosas; no hace falta software de control de versiones.

#### 4. Seguimiento: qué queda para la carga final
El cierre de esta sesión es una **versión corregida** y una lista clara de lo que aún falta para dejar el artículo listo en el repositorio. Nada de cambios "de última hora sin registrar".""",
    ejemplo="En pantalla, llenar una matriz de ajustes con 3 observaciones (una crítica, una mayor, una menor) y mostrar el historial de versiones de Google Docs para revertir un cambio que empeoró un párrafo.",
    errores=[
        ("“Las observaciones menores las ignoro.”",
         "Todas se registran y se atienden por prioridad; las menores son de forma, pero cuentan."),
        ("“Cambio todo lo que dijo el jurado sin pensar.”",
         "Priorice: crítico, mayor, menor. Y revise el efecto dominó del cambio en otras secciones."),
        ("“Modifiqué y perdí la versión que estaba bien.”",
         "Use el historial de versiones de Google Docs para volver atrás; no trabaje sin respaldo."),
        ("“No marco qué está hecho y qué falta.”",
         "La matriz de ajustes debe mostrar estado (hecho/pendiente) para no perder ningún cambio."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 14. Ya pasó la sustentación y casi siempre el jurado deja **observaciones**. Hoy las convertimos en tareas ordenadas, no en pánico. Atender esos ajustes es parte de cerrar el trabajo de grado.”

> “**Slide 2 — OBJETIVOS.** Registrar las observaciones en una **matriz de ajustes**, priorizarlas —crítico, mayor, menor—, incorporarlas sin romper la coherencia y dejar una **versión corregida**. Tengan a la mano las notas de su sustentación.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Toda observación del jurado va a una **matriz de ajustes**: qué dijo, qué cambio implica, qué prioridad tiene y en qué estado está. Así no se pierde ninguna y ustedes ven de un vistazo cuánto les falta.”

> “Prioricen. **Crítico**: afecta la validez o una conclusión —va primero y es obligatorio antes del repositorio—. **Mayor**: afecta una sección. **Menor**: es forma. En ese orden.”

> “**Slide 4 — ENFOQUE DE HOY.** Cuidado con el **efecto dominó**: si tocan un resultado, revisen si la discusión y las conclusiones siguen cuadrando. Y trabajen con red: el **historial de versiones de Google Docs** les deja volver atrás si un cambio empeora las cosas. Gratis, en la nube, sin instalar nada.”""",
    fase3_texto="""**Protagonista:** Docente (modela la matriz + historial de versiones).

**En pantalla (Google Docs):** una matriz de ajustes y el menú Archivo → Historial de versiones.

**GUION LITERAL:**
> “Modelo la matriz. Fila 1: 'el jurado pidió discutir la limitación X' → cambio: agregar párrafo en discusión → prioridad: crítica → estado: pendiente. Fila 2: 'figura sin rótulo' → rotular → menor → la hago ya, hecho. En cinco filas tengo el plan de trabajo completo y priorizado.”

> “Y les muestro la red de seguridad: Archivo → Historial de versiones. Hago un cambio grande en un párrafo; no me gustó cómo quedó. Vuelvo a la versión anterior con un clic. Nunca trabajen sin respaldo, sobre todo en esta etapa donde un cambio puede romper la coherencia.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S14_AjustesPost_Apellido`: (1) armen su **matriz de ajustes** con todas las observaciones del jurado (columnas: observación · cambio · prioridad · estado); (2) atiendan al menos los ajustes **críticos** en la versión del artículo; (3) revisen el **efecto dominó** de cada cambio en las otras secciones.”

> “Criterio de éxito: la matriz muestra cada observación con su prioridad y estado, y los ajustes críticos ya están incorporados sin romper la coherencia del documento.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Quiere ignorar lo 'menor' | “Regístrelo igual; es rápido y suma a la forma final.” |
| Cambia sin priorizar | “Primero lo crítico: lo que afecta validez o conclusiones.” |
| Toca un dato y no revisa el resto | “Revise el dominó: ¿la discusión y las conclusiones siguen cuadrando?” |
| Teme dañar el documento | “Trabaje con el historial de versiones; puede volver atrás.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre. Tres ideas: (1) los ajustes del jurado se registran en una matriz con estado; (2) se priorizan —crítico, mayor, menor—; (3) se incorporan cuidando el efecto dominó y con el historial de versiones como red.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S14_AjustesPost_Apellido` a CDigital con la matriz y la versión corregida. Terminen los ajustes pendientes en autónomo para dejar el artículo listo. La próxima sesión hacemos el **cierre administrativo y la verificación de recepción**.”

> “**Slide 7 — Cierre.** Gracias; mismo Meet.”""",
)

_tg3(
    15,
    fundamento="""> Sesión buffer de cierre. Solo aplica a los grupos que la tienen en calendario (26V04). Léalo completo. (Sin fechas de periodo en el guion; consulte la Presentación del Curso / Manual para plazos por grupo.)

#### 1. Cierre administrativo ≠ cierre académico
El trabajo académico ya terminó (artículo, sustentación, ajustes). El **cierre administrativo** es asegurarse de que **todo quedó cargado y fue recibido** en CDigital. Un excelente trabajo que no se cargó, o que se cargó mal, no cuenta. Esta sesión es la red de seguridad final.

#### 2. Subir ≠ recibido
El error silencioso: creer que "lo subí" equivale a "lo recibieron". Hay que **verificar la recepción**: que el archivo esté en el espacio correcto, con el nombre correcto, y —si el campus lo permite— guardar **evidencia de envío** (captura del estado "entregado").

| Entregable | ¿Cargado? | ¿Recibido/confirmado? | Evidencia |
| :--- | :---: | :---: | :--- |
| Artículo final (PDF) | | | Captura de envío |
| Póster | | | Captura |
| Anexos / evidencias | | | Captura |
| Autorización repositorio | | | Formato firmado |
| Constancia antiplagio | | | Según ruta CDigital |

#### 3. Diferencia recepción vs. cierre (por grupo)
"Recepción" (última fecha para recibir trabajos) y "cierre" (fin del periodo) **no son lo mismo** y varían por grupo. El guion **no lleva fechas**: remita siempre a la Presentación del Curso / Manual del Docente y al calendario del grupo, porque un grupo no tiene siquiera esta sesión y otros cierran en fechas distintas.

#### 4. Checklist de recepción como último filtro
El objetivo de hoy es que nadie pierda la nota por un tema logístico: recorrer el checklist, confirmar cada carga y guardar evidencia. Cerrar bien es parte de ser profesional.""",
    ejemplo="En pantalla, recorrer el checklist de recepción confirmando cada entregable en CDigital y capturando (si el campus lo permite) el estado 'entregado' como evidencia de envío.",
    errores=[
        ("“Ya lo subí, entonces ya está recibido.”",
         "Subir no es recibido: verifique que esté en el espacio correcto y guarde evidencia de envío."),
        ("“Recepción y cierre son la misma fecha.”",
         "No: recepción es la última fecha para recibir; cierre es fin de periodo. Varían por grupo."),
        ("“No guardo captura de que entregué.”",
         "Si el campus lo permite, capture el estado 'entregado'; es su respaldo ante cualquier duda."),
        ("“Dejo un entregable sin cargar, luego lo subo.”",
         "Recorra el checklist hoy: un entregable faltante puede costar la nota."),
    ],
    fase1_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Sesión 15, la última. El trabajo académico ya está hecho: artículo, sustentación, ajustes. Hoy hacemos el **cierre administrativo**, que suena aburrido pero es la red de seguridad: verificar que **todo** quedó cargado y recibido en CDigital.”

> “**Slide 2 — OBJETIVOS.** Recorrer el checklist de recepción, confirmar cada carga y guardar evidencia de envío. Recuerden: un trabajo excelente que no se cargó, o que se cargó mal, no cuenta. Tengan CDigital abierto.”""",
    fase2_texto="""**Protagonista:** Docente (exposición).

**GUION LITERAL:**
> “**Slide 3 — CONTENIDO CLAVE.** Cierre administrativo no es lo mismo que cierre académico. Lo académico terminó; lo de hoy es asegurar que todo quedó **entregado y recibido**. Y ojo con el error silencioso: **subir no es igual a recibido**. Hay que verificar que el archivo esté en el espacio correcto, con el nombre correcto, y —si el campus lo permite— guardar la captura del estado 'entregado'.”

> “**Slide 4 — ENFOQUE DE HOY.** Dos palabras que se confunden: **recepción** —la última fecha para recibir trabajos— y **cierre** —el fin del periodo—. No son lo mismo y **cambian según el grupo**. Por eso no doy fechas aquí: cada quien consulta la Presentación del Curso, el Manual y el calendario de su grupo. Hoy nos concentramos en que nadie pierda la nota por un tema logístico.”""",
    fase3_texto="""**Protagonista:** Docente (modela la verificación en CDigital).

**En pantalla (CDigital + Google Docs):** el espacio de entregas y un checklist de recepción.

**GUION LITERAL:**
> “Modelo la verificación. Entro a CDigital y recorro cada espacio de entrega: artículo final —lo veo cargado, con el nombre correcto—; póster —cargado—; anexos —falta uno—; autorización —firmada y subida—; informe de similitud —sólo si el curso lo exige, según confirmó el Docente—. Voy marcando en el checklist: cargado y recibido.”

> “Y donde el campus lo permite, capturo el estado 'entregado': esa captura es su respaldo si más adelante hay cualquier duda sobre si entregaron o no. Cerrar bien y con evidencia es parte de ser profesional.”""",
    fase4_texto="""**Protagonista:** Estudiantes (taller) · Docente acompaña.

**GUION LITERAL (consigna):**
> “**Slide 5 — TALLER.** ~20 minutos. En `S15_CierreAdmin_Apellido`: (1) recorran el **checklist de recepción** —artículo, póster, anexos, autorización, antiplagio— marcando cargado y recibido; (2) capturen la **evidencia de envío** de cada entregable si el campus lo permite; (3) anoten cualquier **pendiente administrativo** que deban resolver antes de la recepción de su grupo.”

> “Criterio de éxito: cada entregable está confirmado como recibido (no solo subido) y con su evidencia; y no queda ningún pendiente sin anotar.”

**Acompañamiento (mientras trabajan):**
| Si el estudiante… | Usted responde… |
| :--- | :--- |
| Cree que subir = recibido | “Verifique el espacio y el estado; guarde la captura.” |
| Pregunta la fecha de cierre | “Consulte su grupo en la Presentación del Curso / Manual; varía.” |
| Le falta un entregable | “Cárguelo ahora; no lo deje para después de la recepción.” |
| No guarda evidencia | “Capture el 'entregado' si el campus lo permite; es su respaldo.” |""",
    fase5_texto="""**Protagonista:** Docente.

**GUION LITERAL:**
> “Cierre del curso. Tres ideas: (1) el cierre administrativo asegura que todo quedó **recibido**, no solo subido; (2) recepción y cierre no son lo mismo y varían por grupo —consulten su calendario—; (3) guarden evidencia de cada envío.”

> “**Slide 6 — PARA CONTINUAR.** Suban `S15_CierreAdmin_Apellido` a CDigital con su checklist y sus evidencias, y resuelvan los pendientes antes de la recepción de su grupo. Con esto culmina su trabajo de grado.”

> “**Slide 7 — Cierre.** Felicitaciones: cierran un proceso largo con un artículo publicado y una defensa hecha. Gracias por el trabajo de este periodo.”""",
)

for n, fund, note, taller, ent, shots_d, shots_t in TG3:
    rich = TG3_RICH.get(n, {})
    kwargs = dict(
        objetivos=(
            f"1. **Desarrollar:** {(fund.split(':')[0] if ':' in fund else fund[:80]).rstrip('.')}.\n"
            "2. **Dejar** evidencia en CDigital.\n"
            "3. **Preparar** el siguiente hito del artículo/sustentación."
        ),
        fundamento=rich.get("fundamento") or (
            f"#### Enfoque\n{fund}\n\n{note}\n\n"
            "Producto del Syllabus 94532: artículo + sustentación + repositorio. "
            "Práctica en nube (Docs, Canva free para póster, Scholar, ZoteroBib)."
        ),
        fases=[
            ("1️⃣ Encuadre", 6),
            ("2️⃣ Exposición / criterios", 14),
            ("3️⃣ Modelación", 12),
            ("4️⃣ Taller", 20),
            ("5️⃣ Cierre", 8),
        ],
        taller=rich.get("taller", taller),
        entregable=ent,
        ejemplo=rich.get("ejemplo", "Modelar en pantalla un fragmento bueno vs uno débil del entregable de hoy."),
        s01_padlet=(n == 1),
        shots_demo=shots_d,
        shots_taller=shots_t,
        fase1_texto=rich.get("fase1_texto"),
        fase2_texto=rich.get("fase2_texto"),
        fase3_texto=rich.get("fase3_texto"),
        fase4_texto=rich.get("fase4_texto"),
        fase5_texto=rich.get("fase5_texto"),
        errores=rich.get("errores"),
    )
    # Overrides opcionales de TG3_RICH (los usa la Sesión 01 de encuadre; el resto no los define).
    for _k in (
        "objetivos", "fases", "entregable", "uso_texto", "slides_map",
        "fundamento_titulo", "ejemplo_titulo", "errores_titulo", "errores_headers",
        "fase_slides", "entregable_titulo", "checklist",
        "shots_fase2", "shots_demo", "shots_taller",
    ):
        if _k in rich:
            kwargs[_k] = rich[_k]
    _spec("tg3", n, **kwargs)


def _shots_md(items) -> str:
    if not items:
        return ""
    return "".join(shot(rel, cap, tip) for rel, cap, tip in items)


def build_guion(course_key: str, ses: dict) -> str:
    course = COURSES[course_key]
    n = ses["n"]
    titulo = ses["titulo"]
    detalle = ses.get("detalle", "")
    label = label_for(n, titulo)
    meet = meet_url(course["key"], course["titulo"])
    spec = SPEC.get((course_key, n))
    if not spec:
        spec = {
            "objetivos": f"1. Comprender **{titulo}**.\n2. Aplicarlo al entregable del curso.\n3. Salir con avance en CDigital.",
            "fundamento": (
                f"#### Concepto central\nDesarrolle **{titulo}** con definición, por qué importa, "
                f"un ejemplo de Ingeniería y 3 errores frecuentes. Fuente: {course.get('fuente', 'Syllabus')}."
            ),
            "fases": [
                ("1️⃣ Encuadre", 6),
                ("2️⃣ Exposición", 16),
                ("3️⃣ Modelación", 12),
                ("4️⃣ Taller", 18),
                ("5️⃣ Cierre", 8),
            ],
            "taller": "Aplicar el concepto al propio proyecto/artículo.",
            "entregable": f"`S{n:02d}_Avance_Apellido`.",
            "ejemplo": "Ejemplo breve en pantalla alineado al tema.",
            "shots_demo": [("tg_scholar.png", "Google Académico", "Anclar el tema con 1 búsqueda.")],
            "shots_taller": [("Herramientas/tg_zoterobib.png", "ZoteroBib", "Generar 1 APA 7 y pegar en Docs.")],
        }

    padlet = ""
    if spec.get("s01_padlet"):
        padlet = f"""
> **Rompehielos Padlet:** slide **PRESÉNTATE** (QR + URL). Es el **mismo tablero y el mismo momento** que el de la Presentación del Curso —la Sesión 01 *es* la sesión de presentación—, no dos rompehielos distintos. URL: {PADLET_PRESENTACION_URL}
"""

    # Tutorías por grupo acordadas en la semana = solo Proyecto I (AFI). No inyectar en TG2/TG3.
    tutorias_nota = ""
    cierre_tutoria = ""

    fases = spec["fases"]
    fase2_shots = _shots_md(spec.get("shots_fase2") or [])
    demo_shots = _shots_md(spec.get("shots_demo") or [])
    taller_shots = _shots_md(spec.get("shots_taller") or [])

    # --- Rótulos configurables (la Sesión 01 de encuadre los sobreescribe; el resto usa el default) ---
    uso_texto = spec.get("uso_texto") or (
        "> **Uso:** guion de locución de **esta** clase. Léalo en voz alta casi literal.\n"
        "> Estudie primero el Fundamento Teórico. **Duración: 60 minutos**."
    )
    # Tabla de slides: la del spec (S01, escrita contra el deck real) o, si no hay,
    # la del deck REAL en disco. `slides_std()` queda solo como último recurso.
    slides_map = spec.get("slides_map")
    desde_plantilla = not slides_map
    if desde_plantilla:
        _label = label_for(n, titulo)
        slides_map = (
            tabla_slides_md(titulos_pptx(deck_path(COURSES[course_key]["folder"], _label)))
            or slides_std()
        )
        slides_map = f"{slides_map}\n{NOTA_MOMENTOS}\n"
    fundamento_titulo = spec.get("fundamento_titulo") or (
        "📚 **Fundamento Teórico para el Docente** *(estudiar ANTES de la clase)*"
    )
    ejemplo_titulo = spec.get("ejemplo_titulo") or "#### Ejemplo modelo para clase"
    errores_titulo = spec.get("errores_titulo") or "#### Errores frecuentes"
    entregable_titulo = spec.get("entregable_titulo") or "🧩 **Entregable de hoy**"
    fase_slides = spec.get("fase_slides") or [
        "Portada y objetivos", "Exposición del concepto", "Modelación en pantalla",
        "Taller", "Cierre y trabajo autónomo",
    ]

    # --- Errores frecuentes: tabla si el spec trae `errores`; si no, fallback genérico ---
    errores = spec.get("errores")
    er_h = spec.get("errores_headers") or ("Error frecuente / pregunta trampa", "Qué responde el docente")
    if errores:
        er_rows = [
            f"| {er_h[0]} | {er_h[1]} |",
            "| :--- | :--- |",
        ]
        for err, resp in errores:
            er_rows.append(f"| {err} | {resp} |")
        errores_md = "\n".join(er_rows)
    else:
        errores_md = (
            "1. Quedarse en definiciones sin conectar al entregable.\n"
            "2. Avanzar contenido sin verificar el estado del avance previo.\n"
            "3. Cerrar sin tarea observable en CDigital."
        )

    # --- Cuerpos de fase: `faseN_texto` distinto por sesión; si no, fallback genérico ---
    gen_f1 = (
        "**GUION LITERAL:**\n"
        f"> “Buenas tardes. Sesión **{n:02d}**: *{titulo}*. Al terminar esta hora deben salir "
        "con un **avance observable**. Slide 2: objetivos de hoy.”"
    )
    if not spec.get("fase1_texto") and spec.get("s01_padlet"):
        gen_f1 += (
            "\n\n> “Abrimos primero la **Presentación del Curso** → **PRESÉNTATE**. "
            f"QR o link: {PADLET_PRESENTACION_URL}. Post-it con expectativa + tema. ~7 min. "
            "Luego volvemos a esta deck.”"
        )
    gen_f2 = (
        "**GUION LITERAL:**\n"
        "> “**Slide 3 — CONTENIDO CLAVE.** Vamos al concepto del día. **Slide 4 — ENFOQUE DE HOY:** "
        "todo alimenta el mismo entregable del curso, no un taller isla.”\n\n"
        "Desarrolle en voz alta el fundamento (definiciones + tabla mental + 1 pregunta a 2 estudiantes)."
    )
    gen_f3 = (
        f"**En pantalla (Google Docs / Excalidraw / Scholar):** {spec.get('ejemplo')}\n\n"
        "**GUION LITERAL:**\n"
        "> “Miren el ejemplo y el pantallazo de apoyo. No buscamos perfección literaria: "
        "buscamos **criterio de calidad** reproducible en su propio avance.”"
    )
    gen_f4 = (
        "**GUION LITERAL:**\n"
        f"> “**Slide 5 — TALLER.** Tienen ~{fases[3][1]} minutos. Consigna: {spec['taller']} "
        "Criterio de éxito: si yo leo su avance sin conocerlos, entiendo el punto. "
        "Al final, 2–3 personas comparten 30 segundos.”"
    )
    gen_f5 = (
        "**GUION LITERAL:**\n"
        f"> “Tres ideas de hoy: (1) el concepto central de *{titulo}*; (2) el avance debe ser "
        f"**observable**; (3) el hilo del curso continúa. **Slide 6 — PARA CONTINUAR:** suban a CDigital "
        f"{spec['entregable']}. **Slide 7:** gracias; mismo Meet la próxima.”"
    )
    acomp_default = (
        "\n| Si el estudiante… | Usted responde… |\n"
        "| :--- | :--- |\n"
        "| Solo tiene idea vaga | “Escríbalo en una frase con actor + contexto.” |\n"
        "| Copia un caso famoso | “¿Cuál es SU ángulo local / de práctica?” |\n"
        "| No trae avance previo | “Parta hoy con un mínimo viable; el autónomo completa.” |"
    )
    checklist_default = [
        "- [ ] Fundamento teórico leído",
        f"- [ ] PPTX `Clases/{label}/Presentacion.pptx`",
        "- [ ] Pantallazos de esta sesión abiertos (carpeta `Guiones/Capturas/`)",
        ("- [ ] Presentación del Curso (Preséntate / Padlet): " + PADLET_PRESENTACION_URL)
        if spec.get("s01_padlet") else "- [ ] Ejemplo modelo listo para compartir pantalla",
        "- [ ] Espacio de entrega en CDigital",
        f"- [ ] Meet: {meet}",
    ]
    checklist_md = "\n".join(spec.get("checklist") or checklist_default)

    f1 = spec.get("fase1_texto") or gen_f1
    f2 = spec.get("fase2_texto") or gen_f2
    f3 = spec.get("fase3_texto") or gen_f3
    f4 = spec.get("fase4_texto") or gen_f4
    f5 = spec.get("fase5_texto") or gen_f5
    acomp = "" if spec.get("fase4_texto") else acomp_default

    phases_md = f"""#### {fases[0][0]} (~{fases[0][1]} min) — {fase_slides[0]}
{f1}

#### {fases[1][0]} (~{fases[1][1]} min) — {fase_slides[1]}
{f2}
{fase2_shots}
#### {fases[2][0]} (~{fases[2][1]} min) — {fase_slides[2]}
{f3}
{demo_shots}
#### {fases[3][0]} (~{fases[3][1]} min) — {fase_slides[3]}
{f4}
{taller_shots}{acomp}

#### {fases[4][0]} (~{fases[4][1]} min) — {fase_slides[4]}
{f5}
{cierre_tutoria}"""

    md = f"""### GUIÓN DOCENTE — Sesión {n:02d}: {titulo}

{uso_texto}
> Logística de semestre → Presentación del Curso / Manual. **Sin fechas de periodo.**
> **PPTX:** `Clases/{label}/Presentacion.pptx`

📌 **De esta sesión**
- **Sesión:** **{n:02d}** · **Tema:** {titulo}
- **Detalle:** {detalle}
- **PPTX estudiante:** `Clases/{label}/Presentacion.pptx`
- **Meet (serie del curso):** {meet}
{tutorias_nota}{padlet}
{slides_map}
🎯 **Objetivos de la sesión**
{spec['objetivos']}

---

{fundamento_titulo}

{spec['fundamento']}

{ejemplo_titulo}
{spec.get('ejemplo', 'Modele un caso breve del sector Ingeniería alineado al tema.')}

{errores_titulo}
{errores_md}

---

🧭 **Plan de Clase por Fases** — *Total: 60 min*

{plan_tabla(fases)}

---

{phases_md}
---

{entregable_titulo}
1. {spec['taller']}
2. Archivo en CDigital: {spec['entregable']}
3. Herramientas: gratis + nube (Docs, Scholar, ZoteroBib, Excalidraw, Padlet según aplique).
4. Pantallazos de apoyo en `Guiones/Capturas/` (y subcarpetas `Sesion NN/` / `Herramientas/`).

✅ **Checklist del docente antes de clase**
{checklist_md}

---
*Fin del Guión — Sesión {n:02d}. Autocontenido para dictar 60 minutos.*
"""
    if desde_plantilla:
        # La narración venía de la plantilla de 7 slides: sus números no corresponden al
        # deck real. Se retiran (queda el nombre del momento); nunca se inventa un número.
        md, _ = limpiar_referencias(md)
    else:
        # Mapa curado a mano (S01): se realinea contra el deck real por si el motor
        # partió algún bloque en «(cont.)» y corrió la numeración.
        md, _ = ajustar_mapa_manual(
            md, titulos_pptx(deck_path(COURSES[course_key]["folder"], label_for(n, titulo)))
        )
    # Evaluación REAL del aula (quices, parciales, ACA Final, auto y coevaluación): aviso,
    # reserva de minutos en el plan y checklist. Sale del modelo, no se escribe a mano.
    return inyectar_evaluacion(md, course_key, n)


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    if not argv or argv[0] in {"all", "*"}:
        keys = list(KEYS)
        only_n = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else None
    else:
        keys = [argv[0]]
        only_n = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else None
    for key in keys:
        if key not in COURSES or key not in KEYS:
            print("SKIP curso:", key)
            continue
        root = os.path.join(COURSES[key]["folder"], "Guiones")
        os.makedirs(root, exist_ok=True)
        os.makedirs(os.path.join(root, "Capturas"), exist_ok=True)
        # limpiar Sesion*.md obsoletos (conservar Guías / Capturas)
        keep = {f"{label_for(s['n'], s['titulo'])}.md" for s in COURSES[key]["sesiones"]}
        if only_n is None:
            for name in os.listdir(root):
                if name.startswith("Sesion ") and name.endswith(".md") and name not in keep:
                    try:
                        os.remove(os.path.join(root, name))
                        print("DEL", name)
                    except OSError:
                        pass
        for ses in COURSES[key]["sesiones"]:
            if only_n is not None and ses["n"] != only_n:
                continue
            label = label_for(ses["n"], ses["titulo"])
            path = os.path.join(root, f"{label}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(build_guion(key, ses))
            print("MD", path)


if __name__ == "__main__":
    main()
