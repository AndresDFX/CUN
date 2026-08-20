# -*- coding: utf-8 -*-
"""Los TALLERES de las decks de sesión: **una sola forma** para los cinco cursos.

Cada sesión de contenido tiene un taller. Antes, cada uno estaba escrito a mano dentro de
`content/cun_<curso>_s<NN>.json` y los 45 habían derivado a cuatro formas distintas de
título, con y sin nombre de archivo, con y sin criterio de éxito, y con minutos por paso.
Este módulo es la **fuente única** de los 45: el JSON de la sesión solo deja el marcador

    {"type": "taller"}

en el lugar exacto donde va, y `cun_contenido_sesion.load()` lo expande a las **dos slides
canónicas** que devuelve `bloques(curso, n)`. Así el estudiante ve siempre la misma
estructura y el orden de las slides de la sesión no cambia.

    Slide A — «TALLER · <producto>»
        **Al final tiene:** …                 (el producto, en una frase)
        **Paso 1 …** … **Paso N …**           (en orden, sin relojes)
        **En clase, sin falta:** …            (qué es innegociable si el tiempo aprieta)
    Slide B — «TALLER · cómo se revisa y dónde se entrega»
        **Quedó bien si** …                   (criterios verificables, no opinables)
        **Plan B:** …                         (la salida concreta, casi siempre condicional)
        **Entrega / Hoy no se sube nada al aula:** …
        **Esto alimenta:** …                  (el ítem real que sí recibe CDigital)

Tres reglas gobiernan este archivo, y las tres salen de un defecto real que ya estaba
proyectado en clase:

1. **Ningún minuto absoluto.** Los títulos decían «(22 minutos)» y el plan de clase del
   guion daba 12: el inyector de evaluación (`guion_evaluacion.py`) **recorta las fases más
   largas** los días con quiz o parcial, así que ninguna cifra fija en la deck puede ser
   cierta siempre. El guion de Investigación S04 hasta imprimía la excusa en voz alta («la
   slide dice ~24 minutos porque la deck está dimensionada para dos horas»). Lo que el
   estudiante necesita no es el reloj —lo anuncia el Docente— sino **el orden y qué es
   innegociable**: de ahí `en_clase`.
2. **El destino se deriva, no se declara.** 39 de los 45 talleres mandaban a subir el
   archivo «a CDigital, en el espacio de esa sesión». Ese espacio **no existe**: el aula
   tiene 12 componentes en pregrado (5 cuestionarios + ACA Final + auto + coevaluación) y 9
   en especialización, y los propios enunciados de `Clases/Recursos/ACAs/` ya lo dicen —«en
   el aula **no** hay una tarea por corte: la única tarea documental es la ACA Final; los
   avances son **formativos**». Aquí la línea de entrega la calcula
   `ruta_entregables.ruta()` desde `fechas_entrega_aca.py`: si en la semana de esta sesión
   cierra una **tarea** real, dice «suba»; si no, dice «guárdelo» y nombra la tarea que sí
   la recibe. Si el aula cambia de ítems, la frase se recoloca sola.
3. **Ninguna URL a mano.** El aula sale de `sesiones_cun.cdigital_url()`. TG3 tiene **tres**
   aulas para una sola serie de encuentros, así que ahí se dice «el aula de su grupo» en vez
   de una URL que sería falsa para dos tercios del curso.

Y una consecuencia de forma: `cun_contenido_sesion` parte los bloques de más de 9 viñetas
añadiendo « (cont.) » al título. 13 talleres desbordaban, así que el estudiante veía una
segunda slide titulada «TALLER — … (cont.)» sin saber qué era. Las dos slides de aquí
**nunca** desbordan, y `verificar()` lo comprueba.

    python config/slides/talleres.py             # imprime los 45 talleres como se proyectan
    python config/slides/talleres.py --verificar # 0 si todos cumplen el contrato
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.join(os.path.dirname(_HERE), "cursos")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ruta_entregables  # noqa: E402
from sesiones_cun import CDIGITAL_PLACEHOLDER, cdigital_url, cdigital_urls_por_grupo  # noqa: E402

MARCADOR = "taller"                 # {"type": "taller"} en el JSON de la sesión
TITULO_A = "TALLER · {producto}"
TITULO_B = "TALLER · cómo se revisa y dónde se entrega"

# Límites que impone `cun_contenido_sesion` (MAX_BULLETS_PER_SLIDE = 9). Se dejan aquí como
# tope del contenido, no del render: si un taller los pasa, `verificar()` lo grita en vez de
# dejar que la deck lo parta en una slide «(cont.)» sin título propio.
MAX_PASOS = 7
MAX_EXITO = 4

TALLERES: dict[tuple[str, int], dict] = {}


def _t(curso: str, n: int, *, producto: str, archivo: str, formato: str, modo: str,
       resultado: str, pasos: list[str], en_clase: int, exito: list[str], atasco: str,
       nota: str | None = None, cronometro: str | None = None) -> None:
    """Registra un taller.

    `en_clase`   cuántos de los primeros pasos son innegociables en clase.
    `cronometro` la única duración que este taller puede nombrar, porque es un requisito del
                 **producto** —el pitch de 3 minutos, la sustentación de 10–12— y no la fase de
                 clase, que el inyector de evaluación recorta. `verificar()` exige que toda cifra
                 de tiempo del taller coincida con esta; si es None, no se admite ninguna.
    """
    TALLERES[(curso, int(n))] = {
        "curso": curso, "n": int(n), "producto": producto, "archivo": archivo,
        "formato": formato, "modo": modo, "resultado": resultado, "pasos": list(pasos),
        "en_clase": int(en_clase), "exito": list(exito), "atasco": atasco, "nota": nota,
        "cronometro": cronometro,
    }


# ===========================================================================
# CREATIVIDAD Y PENSAMIENTO INNOVADOR — sesiones 02 a 07
# ===========================================================================
_t("creatividad", 2,
   producto="Ideación sobre su propio problema",
   archivo="S02_Ideacion_Apellido", formato="Google Doc o PDF",
   modo="Individual o en dúo, sobre **su** problema · el Docente pasa acompañando",
   resultado="su HMW, el banco de ideas y la captura del boceto, en un solo archivo",
   pasos=[
       "Redacte **su HMW** con la fórmula: ¿Cómo podríamos [acción] para [usuario] de modo "
       "que [resultado]?",
       "Genere **mínimo 8 ideas** sin juzgar ninguna. Si se seca antes de 8, aplique **SCAMPER**.",
       "**Elija 1 o 2** y justifíquelas con los tres criterios: alivia el dolor · factible "
       "este semestre · aprendo rápido.",
       "Haga el **boceto de 1 minuto** en Excalidraw: cajitas y flechas del flujo elegido.",
       "Lea **solo su HMW** en voz alta a tres compañeros, una frase cada uno.",
   ], en_clase=2, cronometro="1 minuto",
   exito=[
       "Su HMW nombra **al usuario** y **el dolor**.",
       "Su HMW **no** nombra ninguna tecnología: si aparece app, plataforma, IA o sistema, "
       "todavía no está listo y hay que reescribirlo.",
       "Hay **8 ideas o más** y ninguna se borró mientras las escribía.",
   ],
   atasco="Si no llega a 8 ideas, deje de buscar ideas nuevas: aplique SCAMPER a la que ya "
          "tiene —sustituir, combinar, adaptar, invertir— y salen solas.")

_t("creatividad", 3,
   producto="Ficha Oslo de su propuesta",
   archivo="S03_FichaOslo_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente lee tres fichas en voz alta al cerrar",
   resultado="la Ficha Oslo de su propuesta con los seis campos llenos",
   pasos=[
       "Abra la **Ficha Oslo** en Google Docs o Excalidraw, con sus **seis campos**.",
       "Decida el **tipo dominante** y escriba la justificación empezando por «porque lo que "
       "cambia es…».",
       "Escriba la **novedad** —¿nueva para quién?— y el **valor esperado** en una frase, "
       "**desde el usuario**, no desde la técnica.",
       "Añada el **tipo secundario** si lo hay, las **dos actividades de gestión** con "
       "responsable y fecha, y el **riesgo #1**.",
       "Relea y borre toda frase que sirva para cualquier proyecto.",
   ], en_clase=3,
   exito=[
       "El tipo dominante está **justificado** con una razón, no solo nombrado.",
       "Las dos actividades de gestión tienen **responsable y fecha real**.",
       "No queda ninguna frase que sirva igual para otro proyecto.",
   ],
   atasco="Si duda entre dos tipos, use la tabla de desempate: ¿lo que cambia es una función "
          "nueva, o el mismo resultado con menos tiempo o menos error?")

_t("creatividad", 4,
   producto="Matriz comparativa de su propuesta",
   archivo="S04_MatrizTipos_Apellido", formato="Google Doc o PDF",
   modo="Individual · dos personas leen **solo su conclusión** al cerrar, no la tabla",
   resultado="la matriz de su tipo elegido contra el que descartó, más la conclusión de 4 líneas",
   pasos=[
       "Nombre **A** (su tipo elegido) y **B** (el tipo alternativo que descartó), y declare "
       "el **grado** —incremental o radical— con una razón.",
       "Escriba **mínimo 5 criterios** en las filas. Uno tiene que tocar el **contexto "
       "socio-económico**: quién paga, quién usa, qué restringe.",
       "Puntúe **alto / medio / bajo** en **las dos** columnas, fila por fila, con el porqué "
       "entre paréntesis.",
       "Escriba la **conclusión de 4 líneas** con la estructura: elijo / empatan en / gana en "
       "/ descarto porque.",
   ], en_clase=3,
   exito=[
       "La conclusión **cita por su nombre al menos dos criterios** de la tabla.",
       "No aparece «me gusta más» ni ningún equivalente.",
       "Si se tapa la conclusión, otra persona llega a la **misma decisión** leyendo solo la "
       "tabla.",
   ],
   atasco="Si no le salen 5 criterios, saque tres de su propia HMW —usuario, dolor, "
          "resultado— y dos del contexto: quién paga y qué restricción hay.")

_t("creatividad", 5,
   producto="Validar por dentro y por fuera",
   archivo="S05_ValidacionVigilancia_Apellido", formato="Google Doc o PDF",
   modo="Individual · dos personas comparten **solo** una implicación y **solo** su criterio de prueba",
   resultado="FODA, Canvas mínimo, MVP con su prueba, dos fichas de señal y una decisión escrita",
   pasos=[
       "**Por dentro —** FODA de **máximo 6 viñetas**, todas verificables, con interna y "
       "externa bien separadas.",
       "**Por dentro —** Canvas mínimo en Canvanizer: **propuesta de valor, segmento, canales "
       "y actividades clave**. Hoy solo esos cuatro bloques.",
       "**Por dentro —** **MVP en 5 líneas** más **una prueba** de su supuesto más riesgoso, "
       "con criterio **numérico u observable**.",
       "**Por fuera —** escriba la pregunta de vigilancia y busque en Scholar y/o Patents.",
       "**Por fuera —** **mínimo 2 fichas de señal** de **frentes distintos**, con fuente, "
       "**fecha**, hallazgo, implicación y confianza.",
       "**Por fuera —** escriba abajo **su decisión** en una frase.",
   ], en_clase=3,
   exito=[
       "La prueba tiene un criterio que **se puede medir hoy mismo** y **podría fallar**.",
       "Las 2 señales traen **fuente y fecha** y son de frentes distintos, no las dos "
       "tecnológicas.",
       "Las señales produjeron **1 decisión** escrita.",
   ],
   atasco="Si se pierde llenando los nueve bloques del Canvas, deténgase: hoy solo cuatro. Y "
          "si una ficha no cambia ni confirma nada, bórrela —ocupa el lugar de una que sí decide—.")

_t("creatividad", 6,
   producto="Mapa de entidades + guion del pitch",
   archivo="S06_EcosistemaPitch_Apellido", formato="Google Doc o PDF",
   modo="Individual, con un ensayo en parejas y cronómetro · dos voluntarios hacen el pitch en vivo",
   resultado="el mapa de entidades, su frase de impacto y el guion del pitch de 60 segundos",
   pasos=[
       "Complete el **Mapa de entidades**: **mínimo 3 entidades reales** de **cuadrantes "
       "distintos**, con el **nombre correcto** y un **pedido concreto** a cada una. "
       "Verifique el nombre en el sitio de la entidad; si no lo encuentra, esa entidad no entra.",
       "Escriba su **frase de impacto**: a quién + qué cambia + en cuánto. Una sola frase.",
       "Escriba el **guion del pitch de 60 s** con los **cinco tramos**. Puede bocetarlo en "
       "Excalidraw.",
       "**Ensaye en parejas** con cronómetro: quien escucha repite qué entendió y quien habla "
       "ajusta.",
   ], en_clase=3, cronometro="60 segundos",
   exito=[
       "Las **3 entidades** tienen nombre verificado y **pedido concreto**.",
       "En **60 segundos** se entienden **dolor, valor y pedido**.",
       "Su compañero pudo **repetir el pedido** después de escucharlo; si no, el tramo 5 está "
       "mal escrito.",
   ],
   atasco="Si el guion no cabe en 60 segundos, recorte el tramo 3: casi siempre es el que sobra.",
   nota="Si quiere una diapositiva de apoyo: **Canva free**, opcional, una sola. El cronómetro "
        "no es para presionar, es para descubrir cuánto sobra.")

_t("creatividad", 7,
   producto="Sustentación cruzada y consolidación",
   archivo="S07_AjustesCierre_Apellido", formato="Google Doc o PDF",
   modo="En ronda, por turnos · el Docente modera y toma el tiempo",
   resultado="una lista escrita de ajustes —mínimo tres— y la devolución de un compañero anotada",
   pasos=[
       "**Ronda de sustentación:** pitch de 60 s + dos preguntas + la frase «qué está listo / "
       "qué falta». Quien escucha toma nota con los **cuatro criterios de la rúbrica**, una "
       "línea por criterio.",
       "**Devolución en pareja:** entréguele a su compañero las **tres frases** —me quedó "
       "claro / no me quedó claro / le sugiero—.",
       "**Revisión de costuras:** con la devolución en la mano, revise las **seis costuras** de "
       "su documento y **anote** los ajustes. No los haga ahora: escribir la lista es el "
       "producto del taller.",
       "**Abra CDigital** y verifique que ve los espacios de **autoevaluación** y "
       "**coevaluación**, y sus fechas.",
   ], en_clase=2, cronometro="60 segundos",
   exito=[
       "Sale con **mínimo tres ajustes escritos**, no recordados.",
       "Tiene **anotada** la devolución de un compañero.",
       "Su compañero pudo repetir su **dolor, su valor y su pedido** sin mirar el documento.",
   ],
   atasco="Si no alcanza a sustentar hoy, hágalo por el **foro del curso**: el guion del pitch "
          "escrito más la frase de qué está listo y qué falta.",
   nota="El objetivo no es lucirse: es descubrir el hueco mientras todavía hay alguien al lado "
        "para señalarlo.")

# ===========================================================================
# INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA — sesiones 02 a 06
# ===========================================================================
_t("investigacion", 2,
   producto="Línea elegida + justificación",
   archivo="S02_LineaInvestigacion_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente pasa acompañando · Google Docs + Google Académico, nada que instalar",
   resultado="su línea elegida, el párrafo que la justifica, dos referentes y la tabla de decisión",
   pasos=[
       "Escriba la **línea elegida** con su **nombre exacto** de las seis del programa.",
       "Escriba un **párrafo de justificación** con los tres movimientos —afinidad, fuentes y "
       "pertinencia local— y nombre también **la línea que descartó**.",
       "Busque en Google Académico **dos referentes exploratorios** y páselos a APA tentativa: "
       "autor, año, título, fuente.",
       "Llene la **tabla de decisión** comparando las dos líneas candidatas.",
   ], en_clase=2,
   exito=[
       "Al leer **solo su párrafo**, sin conocer su tema, se entiende **por qué esa línea y no "
       "la otra**.",
       "Los dos referentes demuestran que **ya existe literatura** para trabajarla.",
       "Si sus dos referentes no aparecen, la justificación **no está terminada**: el criterio "
       "de fuentes no se cumplió.",
   ],
   atasco="Si no encuentra referentes de su línea, cambie **una** palabra clave por su sinónimo "
          "técnico antes de cambiar de línea: el problema casi siempre es el vocabulario.")

_t("investigacion", 3,
   producto="Escribir el 1.er avance",
   archivo="S03_Avance1_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente pasa acompañando · se prefiere media página impecable a tres de relleno",
   resultado="título tentativo, introducción de 3 párrafos, la pregunta y dos referencias en APA 7",
   pasos=[
       "**Título tentativo** con actor + fenómeno + contexto, en 20 palabras o menos.",
       "**Introducción** de exactamente **3 párrafos**: contexto → vacío → propósito.",
       "**El problema convertido en pregunta**, en una sola frase, que no se responda con sí o no.",
       "**Dos referencias en APA 7** generadas con ZoteroBib, de fuentes que usted abrió.",
   ], en_clase=2,
   exito=[
       "Otra persona lee su introducción **sin conocer su tema** y le dice cuál es el contexto, "
       "cuál el vacío y qué se propone usted.",
       "Puede **subrayar el vacío**: si no puede subrayarlo, no lo escribió.",
       "La pregunta no se contesta con sí o no.",
   ],
   atasco="Escriba primero y corrija después: no se quede puliendo la primera frase. Si la "
          "introducción no arranca, empiece por el párrafo del propósito, que ya lo tiene claro.")

_t("investigacion", 4,
   producto="Pregunta + tres fuentes citadas",
   archivo="S04_ProblemaPreguntaFuentes_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente pasa acompañando · todo en el navegador",
   resultado="el problema en 8–12 líneas, el diagrama, la pregunta y 3 fuentes citadas en APA 7",
   pasos=[
       "Describa el problema en **8 a 12 líneas**, como un hecho con consecuencias, **no** como "
       "la falta de su solución.",
       "Haga el diagrama en **Excalidraw** —espina de pescado o árbol de problemas— y pegue la "
       "captura. **Empiece por aquí:** pensar dibujando desatasca más rápido que pensar escribiendo.",
       "Escriba la pregunta en **una sola frase** investigable.",
       "Busque en **Google Académico** y en **SciELO o Redalyc** y quédese con **3 fuentes** que "
       "pasen el filtro de 60 segundos.",
       "Genere las **3 referencias en APA 7** con **ZoteroBib**, revíselas a mano y péguelas "
       "bajo *Referencias*.",
   ], en_clase=3, cronometro="60 segundos",
   exito=[
       "Su pregunta **tiene actor y contexto** y **no** se responde con sí/no.",
       "El diagrama muestra **al menos tres causas** en familias distintas.",
       "Las **3 referencias** están completas —autor, año, título, fuente— y usted **abrió las "
       "tres**.",
       "Leyó su pregunta a un compañero y **no tuvo que explicársela**.",
   ],
   atasco="Si el problema no arranca escrito, dibuje el diagrama primero y ponga en palabras "
          "cada rama: el texto sale de ahí.",
   nota="Al menos **una** de las tres fuentes debería ser regional (SciELO o Redalyc): es la que "
        "le da pertinencia local al artículo.")

_t("investigacion", 5,
   producto="Planteamiento + primera página de marco",
   archivo="S05_PlanteamientoMarco_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente pasa revisando la alineación entre pregunta, planteamiento y marco",
   resultado="el planteamiento de 1 a 1.5 páginas, sus 2 constructos, 5 fichas de lectura y un párrafo de marco por constructo",
   pasos=[
       "Llene la tabla **síntoma / evidencia / consecuencia** con **al menos tres filas**.",
       "Conviértala en un planteamiento de **1 a 1.5 páginas** con los **seis componentes** en "
       "orden, que **termine en su pregunta**.",
       "Declare sus **2 constructos** y ponga un **subtítulo** para cada uno.",
       "Complete **5 fuentes** con su **ficha de lectura** —los cinco campos—, citadas en APA 7.",
       "Escriba **un párrafo de marco** por constructo con los **cuatro movimientos**, y cierre "
       "cada uno volviendo a su caso.",
   ], en_clase=2,
   exito=[
       "Al leer su planteamiento **sin conocer su tema** se entiende **qué pasa, cómo lo sabe y "
       "por qué importa**.",
       "Cada párrafo del marco **se puede etiquetar** con uno de sus constructos.",
       "Cuente cuántas veces aparece **un número o una cita** en su texto: si la respuesta es "
       "cero, todavía es opinión.",
   ],
   atasco="Si el tiempo aprieta, priorice el planteamiento completo y **un** párrafo de marco "
          "bien hecho. Media página con argumento vale más que dos páginas de definiciones.")

_t("investigacion", 6,
   producto="Ronda de socialización",
   archivo="S06_AjustesCierre_Apellido", formato="Google Doc o PDF",
   modo="En ronda, por turnos · el Docente modera y toma el tiempo",
   resultado="una lista escrita de tres ajustes y la devolución de un compañero anotada",
   pasos=[
       "**Ronda:** cuente su artículo con la estructura de hoy y reciba dos preguntas. Quien "
       "escucha toma nota con los **cuatro criterios de la rúbrica**, una línea por criterio.",
       "**Devolución en pareja:** entréguele a su compañero las **tres frases** —me quedó claro "
       "/ no me quedó claro / le sugiero—.",
       "**Lista de ajustes:** con la devolución en la mano, escriba los **tres arreglos** que le "
       "va a hacer al documento. No los haga ahora: **anótelos**.",
       "**Abra CDigital** y verifique que ve los espacios de **autoevaluación** y "
       "**coevaluación**, y sus fechas.",
   ], en_clase=2,
   exito=[
       "Sale con **tres ajustes escritos**, no recordados.",
       "Tiene **anotada** la devolución de un compañero.",
       "Su compañero pudo repetir **su pregunta y a quién afecta** sin mirar el documento.",
   ],
   atasco="Si no alcanza a socializar en clase, hágalo por el **foro del curso**: la pregunta, "
          "los dos constructos y la frase de qué está listo y qué falta.",
   nota="El objetivo no es lucirse: es descubrir el hueco mientras todavía hay alguien al lado "
        "para señalarlo.")

# ===========================================================================
# PROYECTO I (Especialización) — sesiones 02 a 11 · se trabaja por EQUIPOS
# ===========================================================================
_t("proyecto1", 2,
   producto="Borrador de problema y pregunta",
   archivo="S02_ProblemaPregunta_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos, en el documento del equipo · el Docente pasa por los equipos mientras escriben",
   resultado="el planteamiento, la pregunta en una frase y la línea oficial de IA en que encaja",
   pasos=[
       "**De 8 a 12 líneas de planteamiento:** síntoma, contexto, actores y consecuencia.",
       "Su **pregunta de investigación** en **una sola frase**.",
       "La **línea oficial de IA** en la que encaja, escrita tal cual aparece en el programa.",
       "Al cerrar, tres equipos leen en voz alta **solo su pregunta**, una frase cada uno.",
   ], en_clase=2,
   exito=[
       "Al escuchar la pregunta se identifican **actor + fenómeno + contexto**.",
       "Si falta uno de los tres, la pregunta vuelve a taller: no avanza a objetivos todavía.",
   ],
   atasco="Si se atasca en el síntoma, levante la mano: es donde el Docente entra primero. Y "
          "escriba el síntoma como algo que **se puede contar** —cuántos, cada cuánto, cuánto cuesta—.",
   nota="Prohibido durante el taller: escribir la solución, prometer resultados o nombrar la "
        "herramienta que van a construir.")

_t("proyecto1", 3,
   producto="Redacción del bloque de formulación",
   archivo="S03_ObjetivosJustificacion_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos · el Docente circula, con prioridad para quienes no pasen del específico 1",
   resultado="objetivo general, tres específicos, la justificación y los alcances y limitaciones",
   pasos=[
       "**Objetivo general** con la fórmula verbo + qué + dónde + para qué.",
       "**Tres específicos** numerados, un verbo cada uno, en el orden describir → fundamentar "
       "→ proponer.",
       "**De media a una página de justificación:** tres párrafos, un pilar por párrafo.",
       "**Alcances y limitaciones** en dos listas de viñetas separadas.",
   ], en_clase=2,
   exito=[
       "Cada específico se puede **«tachar»** el día que se cumpla.",
       "El general suena igual que la pregunta, en afirmativo.",
       "Tache mentalmente los tres específicos: ¿ya quedó cumplido el general? Si no, falta uno.",
   ],
   atasco="Si no pasa del específico 1, no invente verbos: mire su pregunta y pregúntese qué "
          "hay que **describir** primero, qué hay que **fundamentar** después y qué se **propone** al final.",
   nota="Prohibido en este taller: verbos no observables, objetivos que exijan recolectar datos "
        "y justificaciones que hablen de ustedes.")

_t("proyecto1", 4,
   producto="Búsqueda y fichaje de antecedentes",
   archivo="S04_Antecedentes_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos · el Docente resuelve dudas de términos de búsqueda y de vínculo con la pregunta",
   resultado="al menos dos antecedentes nuevos fichados y sus dos referencias en APA 7",
   pasos=[
       "Localicen **al menos dos antecedentes** nuevos en Google Scholar, SciELO o Redalyc.",
       "Al menos uno debe ser **latinoamericano o colombiano**.",
       "Llenen la **ficha de cinco casillas** de cada uno, con la casilla 5 redactada por ustedes.",
       "Generen las dos referencias en **APA 7** con ZoteroBib y péguenlas al final del documento.",
   ], en_clase=3,
   exito=[
       "Al leer cada ficha queda claro **qué método usó el estudio**.",
       "Y queda claro **por qué le sirve a esta pregunta**.",
       "Van rumbo a seis: dos hoy, el resto en trabajo autónomo.",
   ],
   atasco="Si una búsqueda no da nada en tres intentos, cambie una palabra clave. Y si en el "
          "taller consiguen **solo un** antecedente bien fichado, eso vale más que cinco enlaces "
          "pegados sin leer.")

_t("proyecto1", 5,
   producto="Mapa de constructos y primer apartado",
   archivo="S05_MarcoTeorico_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos, todo en el navegador · prioridad para los equipos que no pasen de dos constructos",
   resultado="el mapa de constructos exportado y una a dos páginas del primer apartado teórico",
   pasos=[
       "El **mapa de constructos** en Excalidraw: pregunta al centro, constructos, autores y "
       "punto de reaparición en el método.",
       "**De una a dos páginas** del primer apartado teórico, que desarrolla **un solo "
       "constructo** con la arquitectura de cuatro movimientos vista hoy.",
       "Suban el mapa exportado y el texto **dentro del mismo documento acumulativo**.",
   ], en_clase=2,
   exito=[
       "Cada párrafo del apartado afirma algo que el método podrá **«tocar»**.",
       "Prueba en voz alta: se señala un párrafo al azar y ustedes dicen **en qué parte de la "
       "metodología reaparece**.",
   ],
   atasco="Si no pasa de dos constructos, quédese en dos y desarrolle bien uno: el apartado de "
          "hoy es de **un solo** constructo.",
   nota="Prohibido en este taller: pegar definiciones sin autor y abrir un apartado de "
        "«historia de la inteligencia artificial».")

_t("proyecto1", 6,
   producto="Definiciones operativas y contexto",
   archivo="S06_ConceptualContextual_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos · prioridad para los equipos que no logren ponerle umbral a sus definiciones",
   resultado="la tabla conceptual de cuatro a seis términos y una página de marco contextual",
   pasos=[
       "La **tabla conceptual** con **cuatro a seis términos** y las cuatro columnas completas. "
       "Los términos se toman de la pregunta y de los objetivos: si un término no aparece allí, "
       "no va en la tabla.",
       "Una página de **marco contextual**: organización o aula, proceso, actores, ritmos y "
       "restricciones.",
   ], en_clase=1,
   exito=[
       "**Ningún término admite dos interpretaciones.**",
       "Cada dato de contexto se puede vincular a **una decisión del método**.",
       "Prueba en voz alta: el Docente lee una definición del equipo vecino y pregunta «¿esto "
       "cuenta o no cuenta?». Debe haber **una sola** respuesta posible.",
   ],
   atasco="Si una definición no tiene umbral, póngale un número: «alto» no sirve, «más de tres "
          "por semana» sí.",
   nota="Prohibido en este taller: definiciones copiadas de un diccionario y párrafos de "
        "contexto que empiecen por «en el mundo actual…».")

_t("proyecto1", 7,
   producto="Limpieza legal y bibliográfica",
   archivo="S07_LegalAPA_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos, con el documento de avance abierto en Google Docs · el Docente circula",
   resultado="el párrafo legal (o la declaración de no aplicabilidad) y todas las referencias verificadas",
   pasos=[
       "Decida si aplica marco legal y escriba **un párrafo con la fórmula de tres tiempos** — "
       "norma, principio pertinente, implicación para su estudio.",
       "Si **no** aplica, escriba la **declaración argumentada de no aplicabilidad**: mínimo dos "
       "renglones, con razón explícita.",
       "Regenere **todas** sus referencias en ZoteroBib con estilo APA 7 y aplique sangría "
       "francesa.",
       "Haga la **verificación cruzada** con Ctrl + F: marque en amarillo toda referencia que no "
       "encuentre en el cuerpo. Levante la mano cuando llegue aquí.",
   ], en_clase=4,
   exito=[
       "**Cero resaltados en amarillo** al terminar.",
       "El párrafo legal tiene la implicación redactada **en condicional**.",
   ],
   atasco="Si no sabe si su proyecto tiene marco legal, escriba la declaración de no "
          "aplicabilidad: una razón explícita vale más que una norma pegada que no lo toca.",
   nota="Con esto queda cerrado el bloque referencial: antecedentes, teórico, conceptual, "
        "contextual y legal.")

_t("proyecto1", 8,
   producto="Su ficha metodológica",
   archivo="S08_DisenoMetodologico_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos, en un Google Doc nuevo · tengan la pregunta visible en pantalla cuando pase el Docente",
   resultado="la fila de su matriz de coherencia más el párrafo de paradigma y el de justificación del enfoque",
   pasos=[
       "Arme la tabla de cinco columnas: **Pregunta | Enfoque | Alcance | Técnica propuesta | "
       "Por qué es coherente**.",
       "Llene **una sola fila**, con **SU** pregunta real. No con la del ejemplo.",
       "Debajo de la tabla, escriba el **párrafo de paradigma** —mínimo cuatro renglones— y el "
       "**párrafo de justificación del enfoque**.",
       "En la justificación debe aparecer **citado el verbo de su pregunta**: «dado que la "
       "pregunta indaga *en qué medida*…».",
   ], en_clase=2,
   exito=[
       "Un lector que **solo** vea su tabla puede **predecir el tipo de instrumento** que usted "
       "usaría.",
       "La justificación cita el verbo de su propia pregunta.",
   ],
   atasco="Si al llenar la fila descubre que su pregunta no encaja en ninguna ruta, **no fuerce "
          "el método: corrija la pregunta**. Eso también es avance.")

_t("proyecto1", 9,
   producto="Bosquejo de instrumento",
   archivo="S09_InstrumentosPropuestos_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos, con el documento de instrumento abierto · el Docente frena cualquier intento de aplicación anticipada",
   resultado="población y muestra delimitadas, el instrumento bosquejado y el plan de análisis",
   pasos=[
       "**Población** y **muestra** delimitadas —quiénes, dónde, en qué periodo— más los "
       "criterios de **inclusión** y **exclusión**.",
       "Declare el **tipo de muestreo** propuesto y por qué es el pertinente para su enfoque.",
       "Bosqueje su instrumento: si es **cuestionario**, entre **10 y 15 ítems**; si es **guía "
       "de entrevista**, **8 preguntas** abiertas.",
       "Al lado de cada bloque, escriba **a qué objetivo específico responde**.",
       "Cierre con un párrafo de **plan de análisis**, mínimo tres renglones.",
   ], en_clase=3,
   exito=[
       "**Ningún ítem queda sin objetivo.**",
       "**Ningún objetivo queda sin ítems.**",
       "Todo el texto está **en condicional**: en Proyecto I los instrumentos se proponen, no se "
       "aplican.",
   ],
   atasco="Si no sabe cuántos ítems poner, empiece por los objetivos: dos o tres ítems por "
          "objetivo específico y ya tiene el bosquejo.")

_t("proyecto1", 10,
   producto="Matriz de coherencia y lista de gaps",
   archivo="S10_IntegracionViabilidad_Apellidos", formato="Google Doc o PDF",
   modo="Por equipos, con el documento completo abierto en un solo archivo · tengan la matriz en pantalla",
   resultado="la matriz de las ocho secciones, los gaps con responsable y el cronograma cerrado",
   pasos=[
       "Cree una tabla con cinco columnas: **Sección | ¿Existe? | ¿Alineada con la pregunta? | "
       "Gap | Responsable**.",
       "Use como filas las **ocho secciones** del hilo: problema, pregunta, objetivos, marco, "
       "método, instrumento, cronograma, referencias.",
       "Marque cada casilla **con evidencia**: si dice «sí», debe poder señalar **en qué "
       "página** está.",
       "Convierta cada casilla en rojo o parcial en un **gap con responsable** y ordénelos por "
       "impacto.",
       "Termine el bosquejo del **cronograma** con las fases que falten, empezando por la "
       "gestión de permisos.",
   ], en_clase=4,
   exito=[
       "**Ningún gap queda sin responsable.**",
       "Las **ocho secciones** tienen casilla marcada.",
       "Cada «sí» se puede sustentar señalando la página.",
   ],
   atasco="Si una sección no existe todavía, márquela en rojo y siga: el producto de hoy es "
          "**saber qué falta**, no taparlo.")

_t("proyecto1", 11,
   producto="Coevaluación entre pares y ajustes",
   archivo="S11_CierreIntegracion_Apellidos", formato="Google Doc o PDF",
   modo="En parejas de equipos, lectura cruzada · el Docente modera el intercambio",
   resultado="tres mejoras concretas ya aplicadas en su documento y los pendientes anotados",
   pasos=[
       "Intercambien **una sección** del anteproyecto —de preferencia el método o el instrumento "
       "propuesto—.",
       "Ubique la sección recibida en la **rúbrica de cuatro criterios** y marque un nivel por "
       "criterio.",
       "Escriba **tres comentarios accionables**, uno por criterio distinto, con la fórmula "
       "observación + ubicación + acción.",
       "Devuelva los comentarios al equipo autor y reciba los suyos.",
       "**Aplique de inmediato**, en su propio documento, al menos las mejoras claramente "
       "pertinentes.",
   ], en_clase=4,
   exito=[
       "Su documento tiene **tres mejoras concretas aplicadas** y usted puede señalarlas en "
       "pantalla.",
       "Los comentarios que recibió y no aplicó hoy quedaron anotados **como pendientes con "
       "responsable**.",
   ],
   atasco="Si un comentario que recibió no le parece pertinente, no lo aplique: anótelo con la "
          "razón por la que lo descarta. Eso también es coevaluación.")

# ===========================================================================
# TRABAJO DE GRADO 2 — sesiones 02 a 11
# ===========================================================================
_t("tg2", 2,
   producto="Pregunta, objetivos y título de su proyecto",
   archivo="S02_PreguntaObjetivos_Apellido", formato="Google Doc o PDF",
   modo="Individual, sobre su propio proyecto · el Docente pasa revisando caso por caso",
   resultado="su pregunta, el objetivo general, tres específicos y el título provisional",
   pasos=[
       "La **pregunta** de su proyecto, en una sola frase investigable.",
       "Un **objetivo general** que la refleje, con un solo verbo observable.",
       "**Tres objetivos específicos** con verbos medibles, en orden de pasos.",
       "Un **título provisional** de máximo 21 palabras.",
       "Resalte en amarillo la parte de la que **más duda**: eso es lo que se revisa primero en "
       "el acompañamiento.",
   ], en_clase=3,
   exito=[
       "Si se tapa la pregunta y se leen **solo los objetivos**, un compañero puede reconstruir "
       "qué se va a investigar.",
       "Ningún objetivo usa verbos que no se puedan medir.",
       "El título cabe en 21 palabras.",
   ],
   atasco="Si la pregunta no sale, escriba primero los tres específicos: la pregunta es casi "
          "siempre el general en interrogativo.")

_t("tg2", 3,
   producto="Dejar el documento armado",
   archivo="S03_EstructuraAvance_Apellido", formato="Google Doc (copia de la Plantilla APA CUN)",
   modo="Individual · el Docente revisa ubicación de ideas y tiempo verbal",
   resultado="el outline de todo el documento en la Plantilla APA CUN",
   pasos=[
       "Haga una copia de la **Plantilla APA CUN** en Google Docs y llámela con su nombre de "
       "archivo.",
       "Cada sección con **3 a 5 viñetas afirmativas** de lo que irá.",
       "La metodología escrita en **«se propone / se aplicará»**, sin ningún resultado.",
       "Las secciones aún vacías **resaltadas en color**.",
       "La sección **Referencias** creada, aunque tenga solo una entrada.",
   ], en_clase=3,
   exito=[
       "Al leer **solo su outline** se entiende el documento completo de un vistazo.",
       "No hay **un solo resultado** colado en la metodología.",
       "Las secciones vacías están resaltadas, no disimuladas.",
   ],
   atasco="Si le sobran minutos, convierta en párrafo únicamente el **primer punto de la "
          "introducción**; no empiece a redactar todo.")

_t("tg2", 4,
   producto="Búsqueda y fichaje de antecedentes",
   archivo="S04_Antecedentes_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente acompaña la búsqueda de quienes no encuentren resultados",
   resultado="cuatro antecedentes fichados, sus referencias en APA 7 y el párrafo puente",
   pasos=[
       "Busque y elija **cuatro antecedentes**, con al menos **uno nacional o local** y **uno "
       "internacional**.",
       "Haga una **ficha** por cada uno con los cinco campos, redactada con sus palabras.",
       "Genere las cuatro referencias en **APA 7** con ZoteroBib y péguelas en la sección "
       "Referencias.",
       "Escriba el **párrafo puente** con la fórmula coinciden / difieren / vacío.",
   ], en_clase=2,
   exito=[
       "Cada ficha tiene su línea **«me aporta…»**.",
       "El párrafo puente **nombra explícitamente el vacío** que llena su proyecto.",
       "Las cuatro referencias están en APA 7, no pegadas del buscador.",
   ],
   atasco="Si una búsqueda no da nada en tres intentos, cambie una palabra clave: el problema "
          "casi siempre es el vocabulario, no el tema.")

_t("tg2", 5,
   producto="Dejar el marco arrancado",
   archivo="S05_MarcoTeorico_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente revisa constructo por constructo y corrige paráfrasis dudosas",
   resultado="sus tres constructos, el mapa constructo → fuentes → para qué, y una a dos páginas de marco",
   pasos=[
       "Defina sus **tres constructos** a partir de la pregunta, subrayándolos en ella.",
       "Arme el **mapa**: constructo → fuentes → para qué lo necesito.",
       "Redacte **una a dos páginas** de marco, parafraseando y citando en APA 7.",
       "Cierre cada constructo con una frase que lo **conecte con su pregunta**.",
   ], en_clase=2,
   exito=[
       "Todo párrafo tiene **al menos una cita**.",
       "Todo párrafo **termina conectando** con la pregunta.",
       "Autocontrol rápido: cuente los párrafos sin cita. Deben ser **cero**.",
   ],
   atasco="Si no le salen tres constructos, subraye los sustantivos de su pregunta: los "
          "constructos están ahí, no en la bibliografía.")

_t("tg2", 6,
   producto="Cerrar el marco referencial",
   archivo="S06_ConceptualContextual_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente revisa término por término si la definición es medible",
   resultado="la tabla de términos con definición operativa y una página de contexto concreto",
   pasos=[
       "Una **tabla de mínimo cuatro términos** con su definición operativa, siguiendo las "
       "cuatro piezas.",
       "**Una página de contexto** que describa organización, área y proceso **concretos**.",
       "Las **citas en APA 7** de las definiciones que haya tomado de autores.",
       "**Un dato con origen** por cada párrafo de contexto: informe, documento del área o "
       "fuente citada.",
   ], en_clase=2,
   exito=[
       "**Cada término se puede medir tal como está escrito.**",
       "El contexto describe **un lugar concreto**, no un país.",
       "Prueba en pareja, si alcanza: intercambien definiciones y verifiquen si ambos medirían "
       "igual.",
   ],
   atasco="Si una definición no es medible, añádale la unidad y el umbral: qué se cuenta, cada "
          "cuánto y desde qué valor cuenta.")

_t("tg2", 7,
   producto="Ficha metodológica y matriz de coherencia",
   archivo="S07_Metodologia_Apellido", formato="Google Doc o PDF",
   modo="Individual, con acompañamiento del Docente",
   resultado="enfoque, alcance y diseño justificados, más la matriz pregunta–método",
   pasos=[
       "Defina **enfoque, alcance y diseño**, cada uno con una línea de justificación que "
       "empiece con «porque».",
       "Arme la **matriz pregunta–método**: una fila por objetivo específico, con dato / técnica "
       "/ análisis.",
       "Redacte todo **en propuesto**: ni un verbo en pasado referido a datos.",
   ], en_clase=2,
   exito=[
       "**Todos** sus objetivos específicos tienen fila.",
       "**Ninguna técnica queda huérfana.**",
       "Ctrl+F de «se aplicó» y «se obtuvo» devuelve **cero** resultados.",
   ],
   atasco="Si no sabe qué técnica poner en una fila, mire el verbo del objetivo: describir pide "
          "medir, comprender pide preguntar, proponer pide validar.")

_t("tg2", 8,
   producto="Operacionalización, instrumento y plan de análisis",
   archivo="S08_Instrumentos_Apellido", formato="Google Doc o PDF",
   modo="Individual, con acompañamiento del Docente",
   resultado="la tabla de operacionalización, su instrumento redactado y el plan de análisis",
   pasos=[
       "Complete la **tabla de operacionalización** —variable → dimensión → indicador → ítem— "
       "para al menos dos variables de su proyecto.",
       "Redacte su **instrumento**: unos 10 ítems de encuesta, o una guía de unas 8 preguntas, o "
       "un protocolo de 5 a 8 casos de prueba.",
       "Escriba el **plan de análisis** en tabla: qué hará con cada tipo de dato y a qué "
       "objetivo responde.",
   ], en_clase=2,
   exito=[
       "**Cada ítem se rastrea a un objetivo** por la tabla.",
       "**Cada objetivo tiene al menos un ítem.**",
       "El plan de análisis **no deja ningún dato sin destino**.",
   ],
   atasco="Si un indicador no le sugiere ningún ítem, es que todavía es una dimensión: bájelo un "
          "nivel hasta que se pueda preguntar u observar.")

_t("tg2", 9,
   producto="Semáforo y matriz de gaps de su propio avance",
   archivo="S09_Integracion_Apellido", formato="Google Doc o PDF",
   modo="Individual, con acompañamiento del Docente",
   resultado="el semáforo por sección, la matriz de gaps y el gap de prioridad alta ya empezado",
   pasos=[
       "Lea su documento de corrido usando **al menos dos** de las cuatro técnicas y llene el "
       "**semáforo** por sección.",
       "Construya la **matriz de gaps**: cada amarillo y cada rojo con prioridad, acción "
       "concreta y evidencia de cierre.",
       "Empiece aquí mismo a cerrar el gap de **prioridad más alta**, no el más fácil.",
   ], en_clase=2,
   exito=[
       "El semáforo refleja el **estado real**, sin autoengaño.",
       "**Ningún gap está escrito como «mejorar X»**: todos dicen qué se hace.",
       "El gap de prioridad alta ya tiene **avance visible** en el documento.",
   ],
   atasco="Si todo le parece amarillo, aplique una sola regla: rojo es lo que **no existe**, "
          "amarillo lo que existe pero **no está alineado** con la pregunta.")

_t("tg2", 10,
   producto="Pitch de 3 minutos y ronda de retroalimentación",
   archivo="S10_Socializacion_Apellido", formato="Google Doc o PDF",
   modo="En ronda, moderada por el Docente, con cronómetro a la vista",
   resultado="su guion de pitch y las notas de dos pares, con qué incorpora y qué no",
   pasos=[
       "Presente su **pitch de 3 minutos** con la estructura problema → pregunta y objetivos → "
       "avance → pedido.",
       "Dé retroalimentación a **al menos dos compañeros** con la fórmula fortaleza + pregunta + "
       "sugerencia.",
       "Registre en su documento el feedback que reciba, **textual**, y marque cuál va a "
       "incorporar y cuál no, **con una razón**.",
   ], en_clase=2, cronometro="3 minutos",
   exito=[
       "El pitch **cierra dentro de los 3 minutos**.",
       "Su documento tiene el **guion de cuatro frases** y **notas de dos pares**.",
       "**Ninguna nota dice solo «está bien».**",
   ],
   atasco="Si se pasa de los 3 minutos, recorte el bloque de avance: el pedido nunca se recorta, "
          "porque es lo único que le devuelve algo.")

_t("tg2", 11,
   producto="Versión limpia, checklist y pendientes para TG3",
   archivo="S11_CierreTG2_Apellido", formato="Google Doc o PDF",
   modo="Individual, con acompañamiento del Docente",
   resultado="el checklist recorrido, una versión limpia del avance y la lista de pendientes para TG3",
   pasos=[
       "Recorra el **checklist de cierre** ítem por ítem y marque lo que está listo y lo que no.",
       "Deje una **versión limpia** del avance: formato de la Plantilla APA CUN aplicado y "
       "referencias completas en APA 7.",
       "Escriba la **lista de pendientes para TG3** en imperativo, con por qué quedó pendiente y "
       "qué necesita para ejecutarlo.",
   ], en_clase=3,
   exito=[
       "El documento **se lee coherente de punta a punta**.",
       "**Ningún ítem del checklist quedó sin marcar** ni sin pasar a pendientes.",
       "Cualquier persona que abra su lista **sabe qué falta** para TG3.",
   ],
   atasco="Si un ítem del checklist no está listo y hoy no se puede resolver, no lo deje en "
          "blanco: páselo a la lista de pendientes con lo que necesita para cerrarlo.")

# ===========================================================================
# TRABAJO DE GRADO 3 — sesiones 02 a 15 · TRES aulas para una sola serie
# ===========================================================================
_t("tg3", 2,
   producto="Pregunta, objetivos y título en una página",
   archivo="S02_PreguntaObjetivos_Apellido", formato="Google Doc o PDF",
   modo="Individual, sobre su propio proyecto · el Docente pasa por los grupos y corrige en el momento",
   resultado="una página con su pregunta, un general, tres específicos, el título y la prueba de coherencia",
   pasos=[
       "Escriba su **pregunta** con las dos variables visibles, el actor y el contexto.",
       "Derive **un objetivo general + tres específicos** con verbos operables, y anote al frente "
       "de cada específico **la sección que producirá**.",
       "Escriba el **título** en 15 a 20 palabras, sin eslóganes.",
       "Cierre con la **prueba de coherencia**: lea los tres bloques seguidos y escriba una línea "
       "diciendo si suenan al mismo proyecto.",
   ], en_clase=3,
   exito=[
       "Un compañero que no conoce su tema lee su página y puede decir **qué va a medir usted y "
       "en quién**.",
       "**Ningún** objetivo específico usa conocer, entender, saber o profundizar.",
       "El título **no contiene ningún adjetivo publicitario**.",
   ],
   atasco="Si su pregunta se responde con sí o no, cámbiele el arranque: «¿en qué medida…?», "
          "«¿de qué manera…?», «¿cuál es la relación entre…?».")

_t("tg3", 3,
   producto="Su introducción en la plantilla APA CUN",
   archivo="S03_Introduccion_Apellido", formato="Google Doc (plantilla APA CUN)",
   modo="Individual, en la plantilla APA CUN abierta en Google Docs",
   resultado="una introducción de 3 a 4 párrafos que cierra exactamente en su pregunta y objetivos",
   pasos=[
       "Escriba la **introducción de 3 a 4 párrafos** con el embudo contexto → problema → vacío "
       "→ pregunta → objetivos → propósito.",
       "Debe **cerrar exactamente** en la pregunta y los objetivos de la Sesión 02, **sin "
       "cambiarles la redacción**.",
       "Incluya al menos **dos citas en APA** en el párrafo de contexto, generadas en zbib.org.",
       "Marque con color el **conector que abre el párrafo del vacío** —«sin embargo», «no "
       "obstante»— para verificar que sí está.",
   ], en_clase=2,
   exito=[
       "Si el Docente lee su introducción **sin conocer su tema**, entiende el contexto, el vacío "
       "y qué se propone usted.",
       "El texto **termina en su pregunta**, no en el aire.",
       "**No aparece ni una palabra** sobre instrumentos, muestras o resultados: eso va en otras "
       "secciones.",
   ],
   atasco="Si se traba, escriba primero el párrafo 3 —pregunta y objetivos—, que ya lo tiene "
          "resuelto, y luego devuélvase a construir el contexto.")

_t("tg3", 4,
   producto="Fichas de lectura y primer mapa de diálogo",
   archivo="S04_ReferentesFaseI_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente pasa acompañando la búsqueda",
   resultado="su criterio de inclusión, 4 a 6 fichas de lectura y el mapa de diálogo esbozado",
   pasos=[
       "Escriba en **una línea** su **criterio de inclusión**: años, idioma y qué debe tocar la "
       "fuente para entrar.",
       "Busque en Google Académico y en SciELO o Redalyc y seleccione **4 a 6 fuentes** "
       "pertinentes.",
       "Haga **una ficha de lectura por fuente**, con los cuatro campos completos.",
       "Esboce el **mapa de diálogo**: agrupe quién confirma, quién contradice, quién extiende y "
       "quién le aporta método.",
   ], en_clase=3,
   exito=[
       "Cada ficha tiene escrita su línea de **«relación con mi pregunta»**; ninguna en blanco.",
       "Cada idea principal está redactada con **sus** palabras, no copiada del resumen del "
       "artículo.",
       "El mapa muestra a los autores **conversando entre sí**, no una lista apilada.",
   ],
   atasco="Si una fuente no le deja escribir la cuarta fila de la ficha, descártela en el momento "
          "y busque otra. Descartar temprano es ganar tiempo.")

_t("tg3", 5,
   producto="Matriz de consistencia y bosquejo del instrumento",
   archivo="S05_MetodoInstrumento_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente revisa fila por fila: «¿ese instrumento sí mide esa variable?»",
   resultado="la matriz de consistencia completa, enfoque/alcance/diseño y el instrumento bosquejado",
   pasos=[
       "Llene su **matriz de consistencia** con **una fila por objetivo específico** y las cinco "
       "columnas completas.",
       "Declare en **tres líneas** su enfoque, su alcance y su diseño, cada uno con media línea "
       "de justificación.",
       "Redacte el **bosquejo del instrumento**: 10 ítems de cuestionario, o una guía de 8 "
       "preguntas, o la rúbrica del prototipo con 4 a 6 criterios.",
       "Escriba **una línea** sobre el tratamiento ético de los datos.",
   ], en_clase=2,
   exito=[
       "**No queda ninguna celda vacía** en la matriz.",
       "**No queda ningún ítem huérfano**: todos tienen anotado al frente el objetivo que "
       "responden.",
       "Un compañero puede leer su matriz y decirle **qué va a hacer usted**, sin que se lo "
       "explique.",
   ],
   atasco="Si un instrumento no mide la variable de su fila, no cambie la variable: cambie el "
          "ítem. La matriz manda sobre el instrumento.")

_t("tg3", 6,
   producto="Pitch de 3 minutos y bitácora de co-creación",
   archivo="S06_CoCreacion_Apellido", formato="Google Doc o PDF",
   modo="En parejas o tríos, por turnos · el Docente modera y corta a los 3 minutos exactos",
   resultado="su bitácora con el pedido que hizo, tres aprendizajes accionables y qué decide con cada uno",
   pasos=[
       "Dé su **pitch de 3 minutos** con la estructura problema → pregunta → avance → **pedido "
       "concreto**.",
       "Cuando le toque escuchar, dé feedback **sobre lo que el compañero pidió**, no sobre sus "
       "gustos.",
       "Registre en su documento: el pedido que hizo, **tres aprendizajes accionables** que "
       "recibió, y qué decide con cada uno —adoptar / adaptar / descartar— **con su razón**.",
   ], en_clase=3, cronometro="3 minutos",
   exito=[
       "La bitácora deja claro **qué es aporte externo y qué es decisión propia**, con una razón "
       "en cada caso.",
       "**Ninguno** de los tres aprendizajes dice «me dijeron que estaba bien».",
       "Su pitch **cupo en los 3 minutos** y terminó en un pedido específico, no en «bueno, eso "
       "es todo».",
   ],
   atasco="Si no sabe qué pedir, pida lo que más le duele: la pregunta, la muestra o el "
          "instrumento. Un pedido concreto es lo que hace útil el turno del otro.",
   nota="Pasarse de tiempo hoy es gratis; en la sustentación, no.")

_t("tg3", 7,
   producto="Tabla de hallazgos y página de lectura",
   archivo="S07_AnalisisHallazgos_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente pasa acompañando",
   resultado="la tabla de hallazgos y una página en prosa que los interpreta",
   pasos=[
       "Arme una **tabla de hallazgos** con las columnas *dato · hallazgo · objetivo que "
       "responde*, con **mínimo 3 filas**.",
       "Escriba **una página de lectura en prosa** que interprete esos hallazgos: qué se ve y qué "
       "significa.",
       "Use al menos una vez la fórmula «**se observa que… lo que indica que…**».",
       "Marque con color los hallazgos que piensa retomar en la discusión.",
   ], en_clase=2,
   exito=[
       "Cada dato tiene su interpretación y está amarrado a un objetivo: **ninguna celda de la "
       "tercera columna vacía**.",
       "Si el Docente lee su página **sin ver las tablas**, entiende qué encontró usted.",
       "**No hay ni una tabla muda** en su documento.",
   ],
   atasco="Si todavía tiene pocos datos, haga el ejercicio con los que tenga: hoy se evalúa la "
          "**lógica del análisis**, no el volumen de la muestra.")

_t("tg3", 8,
   producto="Cierre del marco y auditoría de referencias",
   archivo="S08_MarcoCierre_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente revisa que ningún párrafo empiece con un apellido y que el conteo sea el del Ctrl+F",
   resultado="el marco reorganizado por constructos, su tabla de estado y el conteo real de referencias",
   pasos=[
       "Reorganice su marco **por constructos** —mínimo 2, máximo 3— y verifique que bajo cada "
       "uno haya definición, tipos y forma de medición.",
       "Arme su **tabla de constructos** con la columna de estado: cerrado o qué le falta.",
       "Audite el conteo con **Ctrl+F**: cuántas referencias tiene **listadas**, cuántas están "
       "**citadas en el cuerpo** y cuántas le faltan para 50.",
       "Haga la **lista de huecos**: cuáles resolvió hoy y cuáles quedan para trabajo autónomo, "
       "con fecha propia de cumplimiento.",
   ], en_clase=2,
   exito=[
       "El marco **se lee como argumento por constructos**, no como lista de resúmenes por autor.",
       "El conteo de referencias citadas es **real, no inflado**: puede mostrar dónde se cita "
       "cada una.",
       "Cada bloque del marco tiene anotado su **movimiento previsto para la discusión**.",
   ],
   atasco="Si un párrafo empieza con un apellido, reescríbalo empezando por la idea y deje el "
          "autor en el paréntesis: eso solo convierte la lista en argumento.")

_t("tg3", 9,
   producto="Resultados y discusión de su documento",
   archivo="S09_ResultadosDiscusion_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente pasa acompañando",
   resultado="Resultados en tono neutral, dos párrafos de Discusión, limitaciones y la tabla de cierre",
   pasos=[
       "Redacte **Resultados** en tono neutral, apoyándose en su tabla de hallazgos: mínimo tres "
       "hallazgos, cada uno con su dato.",
       "Escriba al menos **dos párrafos de Discusión** con el latido completo: hallazgo → autor "
       "que confirma/contradice/extiende → implicación → límite.",
       "Agregue el párrafo de **limitaciones** con la fórmula de tres partes.",
       "Cierre con la tabla **objetivo específico | párrafo que lo responde** y verifique que "
       "ninguna fila quede vacía.",
   ], en_clase=2,
   exito=[
       "Resultados **sin ninguna frase interpretativa**: búsquelas con Ctrl+F —*significa*, "
       "*demuestra*, *claramente*—.",
       "Discusión con **mínimo dos autores citados** en APA 7 dentro del texto.",
       "**Cero objetivos huérfanos** en la tabla de cierre.",
   ],
   atasco="Si su proyecto todavía no tiene datos finales, trabaje con los **hallazgos "
          "preliminares**: hoy el objetivo es dominar la estructura, no cerrar el documento.")

_t("tg3", 10,
   producto="Cierre del documento",
   archivo="S10_CierreArticulo_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente acompaña y revisa resúmenes en voz alta",
   resultado="el resumen, las palabras clave verificadas, las conclusiones y las referencias auditadas",
   pasos=[
       "Escriba el **resumen**, **~200–250 palabras**, con las cinco piezas en orden. Anote al "
       "final el conteo real de palabras.",
       "Elija **4 o 5 palabras clave**, verificadas en el tesauro UNESCO y contrastadas en "
       "Scholar; anote al lado cuántos resultados relevantes arrojó cada una.",
       "Redacte las **conclusiones** con las cuatro piezas: respuesta a la pregunta, cumplimiento "
       "de objetivos, limitaciones y trabajo futuro.",
       "Revise sus **referencias** en ZoteroBib: conteo, estilo APA 7, orden alfabético y "
       "**auditoría anti-huérfanas en las dos direcciones**.",
   ], en_clase=2,
   exito=[
       "El resumen **se entiende sin leer el documento** y cae dentro del rango de palabras.",
       "Las palabras clave existen como **términos reales** y arrojan resultados pertinentes en "
       "Scholar.",
       "Las conclusiones **responden la pregunta**, no repiten datos.",
       "**Cero huérfanas**: cada apellido de la lista aparece en el cuerpo y viceversa.",
   ],
   atasco="Control en pareja: intercambien resúmenes. Si su compañero no puede decir qué hizo "
          "usted y qué encontró, el resumen todavía no está listo.")

_t("tg3", 11,
   producto="Póster, anexos y revisión de similitud",
   archivo="S11_PosterEvidencias_Apellido", formato="PDF (póster) + Google Doc",
   modo="Individual · el Docente pasa haciendo la «prueba del metro» a los pósteres",
   resultado="el póster de una página, la lista de anexos y un párrafo reescrito con su cita",
   pasos=[
       "**Póster de una página** en Canva free o Google Slides, con los bloques problema · método "
       "· hallazgo · conclusión, un gráfico al centro y máximo 3 referencias al pie. Exportado en PDF.",
       "**Lista de anexos** en tabla —anexo · contenido · dónde se referencia · estado—, con "
       "mínimo tres anexos reales de su proyecto.",
       "**Un párrafo reescrito:** identifique el de mayor riesgo de similitud, transcríbalo y "
       "debajo escriba su **paráfrasis real con la cita**.",
       "Deje por escrito **cómo opera la revisión de similitud en el aula** según lo que "
       "confirmó el Docente: cuándo ocurre y si el curso pide adjuntar algún informe.",
   ], en_clase=2, cronometro="30 segundos",
   exito=[
       "El póster **se entiende a un metro de distancia** y tiene menos de ~150 palabras.",
       "Cada anexo tiene rótulo y una sección donde se referencia: **ninguna celda «se "
       "referencia en» vacía**.",
       "El párrafo reescrito **conserva la idea**, no comparte la estructura del original y "
       "**mantiene la cita**.",
   ],
   atasco="Control en pareja: muéstrele su póster a un compañero **30 segundos** y quítelo. Si no "
          "puede repetirle su hallazgo principal, el póster todavía no funciona.")

_t("tg3", 12,
   producto="Guion oral y preguntas anticipadas",
   archivo="S12_GuionSustentacion_Apellido", formato="Google Doc o PDF",
   modo="En parejas: uno sustenta con cronómetro y el otro toma notas de tiempo y claridad; al terminar, cambian",
   resultado="el guion oral cronometrado, cinco preguntas difíciles con respuesta y las tres correcciones de su pareja",
   pasos=[
       "**El guion oral por bloques**, con los **minutos asignados** a cada uno y el tiempo real "
       "que le tomó en el ensayo.",
       "**Cinco preguntas difíciles** que anticipa del jurado, **cada una con su respuesta "
       "corta** de máximo cuatro líneas.",
       "Al menos **una** de las cinco debe ser una pregunta que usted **no sabe responder**, "
       "resuelta con la fórmula de tres partes.",
       "**Las tres correcciones** que su pareja le señaló y qué hizo con cada una.",
   ], en_clase=2, cronometro="10–12 minutos",
   exito=[
       "El guion completo **cabe en 10–12 minutos** cronometrados de verdad, no estimados.",
       "Durante el ensayo **no leyó ninguna diapositiva**: su pareja lo certifica.",
       "Las cinco respuestas son **concretas, cortas y honestas**; ninguna inventa un dato.",
       "Puede decir **tres citas (autor, año)** de memoria.",
   ],
   atasco="Si se pasa del tiempo, recorte el marco teórico del guion, no los resultados: el "
          "jurado pregunta por lo que encontró, no por lo que leyó.")

_t("tg3", 13,
   producto="Paquete para el repositorio",
   archivo="S13_PaqueteRepositorio_Apellido", formato="Google Doc o PDF + el documento final en PDF",
   modo="Individual · el Docente acompaña resolviendo dudas del instructivo",
   resultado="el checklist de las seis piezas, la ficha de metadatos y el acta de revisión de forma",
   pasos=[
       "**El checklist de entregables** en tabla —entregable · requisito · **estado (listo / "
       "falta / en trámite)** · responsable—, cubriendo las seis piezas del paquete.",
       "**La ficha de metadatos** completa: título, autoría, resumen íntegro y palabras clave "
       "UNESCO, **copiados** del documento.",
       "**El acta de revisión de forma**: los nueve puntos del recorrido, cada uno marcado como "
       "revisado o corregido, hecho **sobre el PDF exportado**.",
       "La **ruta institucional de carga** del semestre, anotada tal como aparece en CDigital.",
   ], en_clase=3,
   exito=[
       "El checklist muestra **sin ambigüedad** qué falta y quién lo resuelve; ninguna casilla "
       "vacía.",
       "Los metadatos están **completos y copiados** del documento, no reescritos.",
       "La versión revisada es la **final en PDF**, no un borrador.",
       "Las palabras clave de la ficha coinciden **exactamente** con las del documento.",
   ],
   atasco="Si le falta una firma o un formato en trámite, eso **también es un resultado válido**: "
          "quedó identificado y con responsable, que es justamente el punto.")

_t("tg3", 14,
   producto="Matriz de ajustes y versión corregida",
   archivo="S14_AjustesPost_Apellido", formato="Google Doc o PDF",
   modo="Individual · el Docente acompaña resolviendo dudas de clasificación por prioridad",
   resultado="la matriz con todas las observaciones y los ajustes críticos ya incorporados",
   pasos=[
       "**La matriz de ajustes completa** —observación · cambio a realizar · prioridad · "
       "estado—, con **todas** las observaciones recibidas, sin filtrar.",
       "**Los ajustes CRÍTICOS ya incorporados** en el documento.",
       "**La revisión del efecto dominó** de cada ajuste crítico: qué otras secciones tocó y qué "
       "verificó en ellas.",
       "**Una versión nombrada** en el historial de Google Docs: «Ajustes críticos aplicados». "
       "Adjunte la captura del panel de historial.",
   ], en_clase=2,
   exito=[
       "**Cada observación** aparece en la matriz con su prioridad y su estado; **ninguna celda "
       "vacía**.",
       "Los ajustes **críticos** están incorporados en el documento, no solo listados.",
       "Para cada crítico se documentó la revisión de las secciones dependientes.",
       "Existe al menos **una versión nombrada** en el historial antes de los cambios.",
   ],
   atasco="Si aún no ha sustentado, trabaje con las **observaciones del ensayo de la sesión "
          "anterior** y con lo que su checklist marcó como pendiente: la mecánica es la misma.")

_t("tg3", 15,
   producto="Verificación de recepción",
   archivo="S15_CierreAdmin_Apellido", formato="Google Doc o PDF + capturas",
   modo="Individual, con CDigital abierto · el Docente acompaña resolviendo dudas de ubicación de entregas",
   resultado="el checklist de recepción con evidencia y la lista de pendientes administrativos",
   pasos=[
       "**El checklist de recepción completo** —entregable · cargado · confirmado · evidencia—, "
       "cubriendo **todos** sus entregables del curso.",
       "**Las capturas de evidencia** de cada entrega confirmada, o el registro escrito si el "
       "campus no permite capturar.",
       "**La lista de pendientes administrativos**: qué falta, **quién** lo resuelve y **para "
       "cuándo**.",
       "**La fecha de recepción de SU grupo**, tomada del calendario oficial en CDigital.",
   ], en_clase=4,
   exito=[
       "Cada entregable está marcado como **confirmado**, no solo como cargado.",
       "Cada uno tiene su **evidencia** guardada en la carpeta del Drive.",
       "**Ningún pendiente sin responsable ni sin fecha.**",
       "Todos los enlaces compartidos **abren en ventana de incógnito**.",
   ],
   atasco="Lo que dependa solo de usted, resuélvalo dentro del taller: no salga de clase con eso "
          "pendiente. Lo que dependa de un tercero, pásela a la lista con nombre y fecha.")


# ---------------------------------------------------------------- derivaciones
def _tareas(curso: str) -> list[dict]:
    """Las tareas documentales reales del aula, en orden del curso (de `fechas_entrega_aca`)."""
    return [it for it in ruta_entregables.ruta(curso) if it["kind"] == "tarea"]


def tarea_de_la_semana(curso: str, n: int) -> dict | None:
    """La tarea del aula que cierra en la semana de esta sesión, si existe."""
    return next((it for it in _tareas(curso) if it["ancla"] == int(n)), None)


def proxima_tarea(curso: str, n: int) -> dict | None:
    """La primera tarea del aula que todavía no ha cerrado. None si ya cerraron todas."""
    return next((it for it in _tareas(curso) if (it["ancla"] or 99) >= int(n)), None)


def cierres_de_la_semana(curso: str, n: int) -> list[dict]:
    """Lo que **no** es tarea y cierra en esta semana: autoevaluación, coevaluación, quiz.

    Importa en la cola del curso: los cinco talleres que caen después del cierre de la ACA
    coinciden justo con la semana de la autoevaluación y la coevaluación, así que ahí sí hay algo
    que el aula espera, y no es un documento.
    """
    return [it for it in ruta_entregables.ruta(curso)
            if it["kind"] != "tarea" and it["ancla"] == int(n)]


def donde_aula(curso: str) -> str:
    """Cómo se nombra el aula en la slide, con la misma fórmula de `ruta_entregables`: sin URL.

    La URL no ayuda a nadie proyectada —el estudiante entra al campus y ve su curso— y en TG3
    sería directamente falsa para dos tercios del grupo, porque son **tres** aulas distintas para
    una sola serie de encuentros. La URL vive en `sesiones_cun.cdigital_url()`, la usa el guion del
    Docente, y aquí solo sirve para que `verificar()` avise si el aula todavía no está registrada.
    """
    return ("**el aula de su grupo** en CDigital" if cdigital_urls_por_grupo(curso)
            else "**CDigital**")


def _linea_en_clase(e: dict) -> str:
    k, total = e["en_clase"], len(e["pasos"])
    if k >= total:
        return ("**En clase, sin falta:** los **%d pasos**. Lo que no alcance, ciérrelo hoy mismo "
                "en autónomo." % total)
    rango = "el **paso 1**" if k == 1 else "los **pasos 1 a %d**" % k
    return ("**En clase, sin falta:** %s. Del %d en adelante puede quedar en trabajo autónomo, "
            "pero antes de la próxima sesión." % (rango, k + 1))


def _linea_destino(curso: str, n: int, e: dict) -> list[str]:
    """La línea de entrega, derivada del libro de calificaciones. Nunca escrita a mano.

    Solo 6 de los 45 talleres caen en la semana de una tarea real; los otros 39 producen un
    **avance formativo** que el aula no recibe, y decirle al estudiante «súbalo a CDigital»
    lo manda a buscar un espacio que no existe.
    """
    tarea = tarea_de_la_semana(curso, n)
    if tarea:
        return [
            "**Entrega:** suba `%s` (%s) como **%s** —%s, %s— en %s."
            % (e["archivo"], e["formato"], tarea["code"], tarea["tipo"].lower(), tarea["peso"],
               donde_aula(curso)),
            "**Verifique el estado:** *subido* no es lo mismo que *entregado*. Lo que no esté en "
            "el aula, no está entregado.",
        ]
    prox = proxima_tarea(curso, n)
    if prox:
        return [
            "**Hoy no se sube nada al aula:** guarde `%s` (%s) en su Drive y tráigalo a la próxima "
            "sesión. Es un **avance formativo**, se revisa en clase."
            % (e["archivo"], e["formato"]),
            "**Esto alimenta:** **%s** —%s, %s—, el documento que **sí** recibe %s; cierra en la "
            "semana de la **Sesión %02d**."
            % (prox["code"], prox["tipo"].lower(), prox["peso"], donde_aula(curso), prox["ancla"] or 0),
        ]

    # Cola del curso: la ACA ya cerró. Decir «esto alimenta la ACA Final» aquí sería mandar al
    # estudiante a una entrega que ya pasó.
    ult = _tareas(curso)[-1]
    out = ["**Las entregas documentales del aula ya cerraron:** la **%s** cerró en la semana de la "
           "**Sesión %02d**. Guarde `%s` (%s) en su Drive."
           % (ult["code"], ult["ancla"] or 0, e["archivo"], e["formato"])]
    esta = cierres_de_la_semana(curso, n)
    if esta:
        out.append("**Esta semana el aula sí espera:** %s. Eso se responde **en %s**, no se sube "
                   "como archivo." % (" y ".join("**%s** (%s)" % (i["code"], i["peso"]) for i in esta),
                                      donde_aula(curso)))
    else:
        out.append("**Lo que queda es verificar**, no entregar: que cada cosa que subió aparezca "
                   "en %s con su estado confirmado." % donde_aula(curso))
    return out


# ---------------------------------------------------------------- API pública
def tiene(curso: str, n: int) -> bool:
    return (curso, int(n)) in TALLERES


def entrada(curso: str, n: int) -> dict | None:
    return TALLERES.get((curso, int(n)))


def bloques(curso: str, n: int) -> list[dict] | None:
    """Las **dos** slides canónicas del taller, listas para `cun_contenido_sesion.render()`."""
    e = entrada(curso, n)
    if not e:
        return None
    pasos = ["**Paso %d** · %s" % (i, p) for i, p in enumerate(e["pasos"], 1)]
    a = {
        "type": "bullets",
        "title": TITULO_A.format(producto=e["producto"]),
        "sub": e["modo"],
        "bullets": ["**Al final tiene:** %s." % e["resultado"]] + pasos + [_linea_en_clase(e)],
    }
    if e["nota"]:
        a["note"] = e["nota"]
    b = {
        "type": "bullets",
        "title": TITULO_B,
        "sub": e["producto"],
        "bullets": (
            ["**Quedó bien si** —compruébelo usted antes de cerrar el documento—:"]
            + ["  " + c for c in e["exito"]]
            # «Plan B» y no «Si se atasca», porque 41 de los 45 atascos empiezan ellos mismos con
            # «Si …» y en la deck salía «Si se atasca: Si no llega a 8 ideas, …». Cambiar la
            # etiqueta arregla los 41 de una vez; reescribir los atascos habría borrado justo la
            # condición concreta que los hace útiles («si no llega a 8», no «si se atasca»).
            + ["**Plan B:** " + e["atasco"]]
            + _linea_destino(curso, n, e)
        ),
    }
    return [a, b]


def narracion(curso: str, n: int) -> str | None:
    """Una línea para el plan de clase del guion, con los mismos pasos y el mismo archivo.

    Existe para que el `taller=` de los generadores de guiones no vuelva a ser una segunda
    copia escrita a mano de lo que proyecta la deck.
    """
    e = entrada(curso, n)
    if not e:
        return None
    # Los pasos ya vienen con su punto final: unirlos con «. » dejaba «sus fechas.. En clase».
    pasos = "; ".join(
        "(%d) %s" % (i, p.replace("**", "").rstrip(". "))
        for i, p in enumerate(e["pasos"], 1)
    )
    return "En `%s`: %s. En clase, sin falta: %s." % (
        e["archivo"], pasos,
        "los %d pasos" % len(e["pasos"]) if e["en_clase"] >= len(e["pasos"])
        else "hasta el paso %d" % e["en_clase"],
    )


import re  # noqa: E402  (lo usa `verificar()`)

# Lo que el inyector de evaluación recorta es la **fase** del taller, así que ponerle reloj en la
# deck garantiza que algún día mienta: los títulos decían «(22 minutos)» donde el plan de clase daba
# 12. En cambio la duración de un producto oral —el pitch de 3 minutos, la sustentación de 10–12— es
# un requisito verificable del entregable, y nadie la recorta: si el tiempo aprieta se hacen menos
# turnos, no pitches más cortos.
#
# Distinguirlas por cercanía de palabras no funcionó —«Ronda de sustentación: pitch de 60 s» daba
# falso positivo—, así que la duración del producto **se declara** en `cronometro=` y aquí solo se
# comprueba que ninguna otra cifra se cuele.
_RELOJ = re.compile(r"(\d{1,3})\s*(minutos?|min\b|segundos?|s\b)", re.IGNORECASE)


def _relojes(texto: str) -> set[tuple[int, str]]:
    """Las duraciones que nombra un texto, normalizadas a (cantidad, 'min'|'seg')."""
    return {(int(m.group(1)), "min" if m.group(2).lower().startswith("min") else "seg")
            for m in _RELOJ.finditer(texto or "")}


def verificar() -> list[str]:
    """Avisos para el build: contrato de forma de los 45 talleres. Vacío = todos cumplen."""
    avisos: list[str] = []
    MAX_BULLETS = 9      # el mismo de cun_contenido_sesion; pasarlo produce una slide «(cont.)»
    for (curso, n), e in sorted(TALLERES.items()):
        ref = "%s s%02d" % (curso, n)
        if len(e["pasos"]) > MAX_PASOS:
            avisos.append("%s: %d pasos (máx. %d) — la slide se partiría en «(cont.)»."
                          % (ref, len(e["pasos"]), MAX_PASOS))
        if len(e["exito"]) > MAX_EXITO:
            avisos.append("%s: %d criterios de éxito (máx. %d)." % (ref, len(e["exito"]), MAX_EXITO))
        if not 1 <= e["en_clase"] <= len(e["pasos"]):
            avisos.append("%s: en_clase=%d fuera de rango 1..%d."
                          % (ref, e["en_clase"], len(e["pasos"])))
        if not re.match(r"^S%02d_[A-Za-z0-9]+_Apellidos?$" % n, e["archivo"]):
            avisos.append("%s: el archivo «%s» no sigue SNN_Tema_Apellido(s)." % (ref, e["archivo"]))
        permitido = _relojes(e["cronometro"] or "")
        for blk in bloques(curso, n) or []:
            if len(blk["bullets"]) > MAX_BULLETS:
                avisos.append("%s: «%s» con %d viñetas (máx. %d)."
                              % (ref, blk["title"], len(blk["bullets"]), MAX_BULLETS))
            for b in blk["bullets"] + [blk.get("sub") or "", blk.get("note") or ""]:
                if CDIGITAL_PLACEHOLDER in b:
                    avisos.append("%s: se proyectaría el marcador de URL de CDigital." % ref)
                for cant, uni in _relojes(b) - permitido:
                    avisos.append(
                        "%s: «%s…» nombra %d %s. Si es la duración del producto, decláre la en "
                        "`cronometro=`; si es la de la fase de clase, quítela: el inyector de "
                        "evaluación la recorta." % (ref, b[:44], cant, uni))
        if not _tareas(curso):
            avisos.append("%s: el curso no tiene ninguna tarea en el libro de calificaciones; "
                          "la línea de entrega quedaría muda." % ref)
        if not cdigital_urls_por_grupo(curso) and cdigital_url(curso) == CDIGITAL_PLACEHOLDER:
            avisos.append("%s: el aula del curso no está registrada en `sesiones_cun`; el taller "
                          "manda a CDigital sin que se sepa a qué campus." % ref)
    return avisos


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    for (curso, n) in sorted(TALLERES):
        print("\n===== %s · Sesión %02d" % (curso, n))
        for blk in bloques(curso, n):
            print("  ── %s" % blk["title"])
            print("     [%s]" % blk["sub"])
            for b in blk["bullets"]:
                print("     " + b.replace("**", ""))
            if blk.get("note"):
                print("     · %s" % blk["note"].replace("**", ""))
    avisos = verificar()
    print("\n%d talleres · %d avisos" % (len(TALLERES), len(avisos)))
    for a in avisos:
        print("   ⚠ " + a)
    return 1 if ("--verificar" in argv and avisos) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
