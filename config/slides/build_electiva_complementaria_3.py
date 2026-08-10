# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import sys
sys.path.insert(0, r"g:/My Drive/Trabajos/Empleo/FESNA/config/slides")
from fesna_slides_engine import *
set_footer("Electiva Complementaria III · Política Económica en Colombia")
BASE = r"g:/My Drive/Trabajos/Empleo/FESNA/Cursos/Electiva Complementaria 3/Clases"
from pptx.enum.text import PP_ALIGN

# =================================================================
# DECK 0 — PRESENTACIÓN DEL CURSO
# =================================================================
def deck_presentacion():
    prs = new_prs()
    course_cover(prs,
        "Electiva Complementaria III",
        "Política Económica en Colombia",
        "¡Bienvenidos estudiantes!",
        ["**Programa Transversal** · Administración / Contaduría y afines",
         "Asignatura **Tipo C** — Proyecto Integrador",
         "Duración: **3 clases** de **105 min (1h45)** c/u",
         "Cuatrimestre: [N]   ·   Horario: [DÍAS Y HORA]",
         "Fechas: [INICIO] – [FIN]"],
        start_note="Empezamos a las [HORA]…")

    tutor_slide(prs,
        "Julian Andrés Castaño Espinosa",
        ["Líder Técnico",
         "Ingeniero de Sistemas",
         "Candidato a MsC en IA"],
        "julian.castano@lanuevaamerica.edu.co", idx=2)

    table_content(prs, "Metodología",
        ["Momento", "¿Qué hacemos?"],
        [["**Motivación**", "Pregunta o caso real que conecta con tu emprendimiento"],
         ["**Encuadre**", "Objetivo de la sesión, conceptos clave y ruta de la clase"],
         ["**Modelación**", "El tutor explica y demuestra cómo se lee cada indicador"],
         ["@@Simulación / Ejercitación@@", "Practicas con datos reales (DANE, Banco de la República)"],
         ["**Cierre**", "Síntesis e ideas fuerza de la sesión"],
         ["**Evaluación**", "Actividad o evidencia de aprendizaje del día"]],
        sub="Cada clase de 105 min combina teoría y práctica",
        col_w=[1.1, 2.4], idx=3)

    content_slide(prs, "Objetivos del curso",
        ["@@Identificar@@ los indicadores económicos clave de Colombia y describir sus características.",
         "@@Analizar@@ la evolución de esos indicadores y su impacto en los sectores económicos.",
         "@@Evaluar@@ la viabilidad de un emprendimiento en el contexto económico colombiano."],
        sub="Al finalizar el curso serás capaz de:", top=2.2, size=18, idx=4)

    table_content(prs, "¿Cómo se evalúa?",
        ["Componente", "Ponderación"],
        [["**Destreza** — entrenamientos en la ruta de aprendizaje (LMS)", "@@50%@@"],
         ["**Entrega final** — LMS", "@@40%@@"],
         ["**Asistencia** — al final de la sesión", "@@10%@@"],
         ["**Total**", "**100%**"]],
        sub="Escala 0–5",
        note="Opcionales (bonificación): participación en clase +0.3 · Kahoot 🥇+0.5 🥈+0.4 🥉+0.3.",
        col_w=[3.2, 1.0], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER], idx=5)

    table_content(prs, "Así se calcula tu nota final",
        ["Componente", "Nota", "Pond.", "Aporte"],
        [["Destreza — ruta de aprendizaje", "4.5", "50%", "4.5 × 0.50 = **2.25**"],
         ["Entrega final — LMS", "4.8", "40%", "4.8 × 0.40 = **1.92**"],
         ["Asistencia", "5.0", "10%", "5.0 × 0.10 = **0.50**"],
         ["Kahoot (1er puesto, opcional)", "", "+0.5", "+ **0.50**"],
         ["**Nota final**", "", "", "@@5.0 (tope)@@"]],
        sub="Ejemplo: la estudiante “Valentina”",
        note="Base: 2.25 + 1.92 + 0.50 = 4.67; con el bono de Kahoot (+0.5) la nota se topa en 5.0.",
        col_w=[2.4, 0.7, 0.8, 1.8],
        aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER], idx=6)

    table_content(prs, "Contenido del curso",
        ["Sesión", "Título"],
        [["**1**", "Los Indicadores Económicos de Colombia: el tablero de control del país"],
         ["**2**", "Política Económica en Movimiento"],
         ["**3**", "@@¿Es Viable mi Emprendimiento?@@ (entrega del proyecto)"]],
        sub="3 sesiones · un solo proyecto que se construye sesión a sesión",
        col_w=[0.8, 3.5], aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT], idx=7)

    content_slide(prs, "Recursos del curso",
        [("**Portales oficiales de datos**", 0),
         ("DANE — PIB, IPC/inflación, desempleo", 1),
         ("Banco de la República — tasa de interés, tasa de cambio", 1),
         ("**Materiales de aprendizaje**", 0),
         ("Lecturas, infografías y guías de clase (en el LMS)", 1),
         ("**Requisitos técnicos**", 0),
         ("@@Solo necesitas navegador web e internet — no se requiere software especial@@", 1)],
        top=2.0, size=16, idx=8)

    content_slide(prs, "Importante — entregas y plazos",
        ["@@La entrega final del proyecto abre 8 días antes del cierre@@ y queda hasta el siguiente día hábil.",
         "**Publicación de notas:** dentro de los plazos institucionales tras el cierre.",
         "**Reclamaciones:** tienes 3 días para solicitar revisión, por correo al tutor.",
         "**Encuesta de satisfacción:** se diligencia el último día de clase."],
        top=2.2, size=16, idx=9)

    closing_slide(prs, "¡Nos vemos en clase!",
        ["Gestores: FESNA / La Nueva América",
         "Tutor: [NOMBRE DEL TUTOR] · [usuario]@lanuevaamerica.edu.co"],
        "¡Éxitos en Electiva Complementaria III!")

    out = BASE + "/Presentacion del Curso - Electiva Complementaria III.pptx"
    prs.save(out); return out

# =================================================================
# DECK 1 — SESIÓN 1 (Nivel 1 · Identificar)
# =================================================================
def deck_s1():
    prs = new_prs()
    session_cover(prs, "SESIÓN 1",
        "Nivel 1 · Identificar  —  Electiva Complementaria III",
        "Los Indicadores Económicos de Colombia",
        "El Tablero de Control del País",
        "Hoy aprendemos a leer el tablero",
        ["Asignatura: **Electiva Complementaria III**",
         "Duración: **105 min**   ·   Tipo C — Proyecto Integrador"])

    content_slide(prs, "Recordemos la asignatura",
        [("El curso avanza en **tres niveles**, uno por sesión:", 0),
         ("@@Nivel 1 — Identificar@@  (estamos aquí)", 1),
         ("Nivel 2 — Analizar", 1),
         ("Nivel 3 — Evaluar", 1),
         ("**Meta del curso:** evaluar la viabilidad de un emprendimiento con los indicadores.", 0)],
        top=2.1, size=17, idx=2)

    content_slide(prs, "El propósito de hoy",
        ["@@Reconocer@@ qué es un indicador económico y por qué es la brújula de un negocio.",
         "@@Identificar@@ los 5 indicadores clave: PIB, inflación (IPC), desempleo, tasa de cambio (TRM) y tasa de interés.",
         "@@Describir@@ qué entidad mide cada uno (DANE, Banco de la República) y dónde consultarlo."],
        top=2.2, size=17, idx=3)

    table_content(prs, "Cómo trabajaremos hoy (105 min)",
        ["Momento", "Min"],
        [["Motivación y encuadre", "15"],
         ["Enunciación — los 5 indicadores", "25"],
         ["Modelación — buscar un dato oficial en vivo", "25"],
         ["Ejercitación — completas tu ficha", "25"],
         ["Cierre y conexión", "10"],
         ["@@Tu reto individual (entregable)@@", "@@15@@"]],
        col_w=[3.6, 0.7], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER], idx=4)

    content_slide(prs, "¿Qué es un indicador económico?",
        [("Un indicador es un @@número que resume el estado de una parte de la economía@@ y permite compararlo en el tiempo.", 0),
         ("Piensa en el país como un avión enorme: el piloto no “siente” la velocidad, **necesita un tablero con agujas**.", 0),
         ("Esas agujas son los indicadores. Hoy aprendes a **leer el tablero**, no a hacer economía avanzada.", 0)],
        top=2.2, size=17, idx=5)

    content_slide(prs, "¿Para qué sirve la política económica?",
        [("El Estado busca **cinco objetivos**, y cada indicador vigila uno:", 0),
         ("**Empleo** → tasa de desempleo", 1),
         ("**Estabilidad de precios** → inflación (IPC)", 1),
         ("**Crecimiento** → PIB", 1),
         ("**Distribución del ingreso** y **calidad de vida**", 1)],
        top=2.1, size=16, idx=6)

    table_content(prs, "Los 5 indicadores en una frase",
        ["Indicador", "¿Qué mide?"],
        [["**PIB**", "El tamaño de la economía: todo lo que produce el país"],
         ["**Inflación (IPC)**", "Cuánto suben los precios; cuánto poder de compra pierde tu plata"],
         ["**Desempleo**", "% de la fuerza laboral que busca empleo y no lo encuentra"],
         ["**Tasa de cambio (TRM)**", "Cuántos pesos cuesta un dólar (lo fija el mercado)"],
         ["**Tasa de interés de política**", "El “precio del dinero”; palanca para controlar la inflación"]],
        col_w=[1.4, 3.2], idx=7, fs_body=13)

    content_slide(prs, "El tablero de control del país",
        [("Las 5 agujas apuntan a una sola cosa: la @@salud de la economía@@.", 0),
         ("**PIB** · **Inflación** · **Desempleo** · **TRM** · **Tasa de interés**", 1),
         ("Hoy enfocamos la lupa en la **inflación**: cuando sube, el peso pierde poder de compra (como una fiebre del cuerpo).", 0)],
        top=2.2, size=17, idx=8)

    table_content(prs, "Tabla resumen — ¿quién mide qué?",
        ["Indicador", "¿Quién lo mide / controla?", "¿Dónde?"],
        [["PIB", "@@DANE@@", "dane.gov.co"],
         ["Inflación (IPC)", "@@DANE@@ · meta del Banco de la Rep. (3% ±1pp)", "dane.gov.co"],
         ["Desempleo", "@@DANE@@ (encuesta GEIH)", "dane.gov.co"],
         ["Tasa de cambio (TRM)", "El mercado la fija; @@Banco de la República@@ la publica", "banrep.gov.co"],
         ["Tasa de interés", "@@Banco de la República@@", "banrep.gov.co"]],
        col_w=[1.5, 3.0, 1.3], idx=9, fs_body=12,
        note="Regla de oro: un dato solo vale si viene del portal oficial y tiene fecha.")

    content_slide(prs, "Quién es quién",
        [("@@El DANE mide@@ — fotografía la realidad con estadísticas (PIB, IPC, desempleo).", 0),
         ("@@El Banco de la República controla el dinero@@ — política monetaria y cambiaria; mueve la tasa de interés.", 0),
         ("@@Hacienda maneja la plata del Estado@@ — impuestos y gasto público (lo vemos en la Sesión 2).", 0)],
        sub="La confusión número uno — déjala clara desde hoy", top=2.2, size=16, idx=10)

    content_slide(prs, "Tu reto (15 min)",
        [("**Mi primer tablero — Ficha de los 5 indicadores.**", 0),
         ("Para cada indicador anota: **definición con tus palabras**, **quién lo mide**, **enlace oficial** y **dato con fecha**.", 0),
         ("**Criterio de éxito:** los 5 completos, con la entidad correcta y fuente oficial.", 0),
         ("@@Entregable: sube tu ficha al LMS — es el primer insumo de tu proyecto@@", 0)],
        top=2.0, size=16, idx=11)

    closing_slide(prs, "¿Qué logramos hoy?",
        ["Sé qué es un indicador · conozco los 5 de Colombia · sé quién los mide y dónde",
         "Próxima sesión: Política Económica en Movimiento (Nivel 2 — Analizar)"],
        "Guarda tu ficha: es la primera pieza del proyecto")

    out = BASE + "/Sesion 1/Presentacion Sesion 1.pptx"
    prs.save(out); return out

# =================================================================
# DECK 2 — SESIÓN 2 (Nivel 2 · Analizar)
# =================================================================
def deck_s2():
    prs = new_prs()
    session_cover(prs, "SESIÓN 2",
        "Nivel 2 · Analizar  —  Electiva Complementaria III",
        "Política Económica en Movimiento",
        "Cómo las decisiones del Estado mueven los sectores",
        "Hoy las agujas del tablero se mueven",
        ["Asignatura: **Electiva Complementaria III**",
         "Duración: **105 min**   ·   Tipo C — Proyecto Integrador"])

    content_slide(prs, "De dónde venimos",
        [("En la Sesión 1 aprendiste a **leer el tablero** (los 5 indicadores).", 0),
         ("Hoy pasamos de @@Identificar@@ a @@Analizar@@: por qué se mueven y a quién afectan.", 0),
         ("Nivel 1 — Identificar  →  @@Nivel 2 — Analizar (hoy)@@  →  Nivel 3 — Evaluar", 1)],
        top=2.2, size=17, idx=2)

    content_slide(prs, "El propósito de hoy",
        ["@@Diferenciar@@ la política fiscal, la monetaria y la cambiaria, y quién las maneja.",
         "@@Explicar@@ los ciclos económicos (expansión y recesión) leyéndolos en los indicadores.",
         "@@Analizar@@ cómo una misma medida impacta distinto a cada sector y emprendimiento."],
        top=2.2, size=17, idx=3)

    table_content(prs, "Cómo trabajaremos hoy (105 min)",
        ["Momento", "Min"],
        [["Motivación y encuadre", "15"],
         ["Enunciación — las 3 políticas y los ciclos", "25"],
         ["Modelación — una medida y sus efectos", "25"],
         ["Ejercitación en parejas (ensayo, no se entrega)", "20"],
         ["@@Tu actividad individual (entregable)@@", "@@15@@"],
         ["Cierre y conexión", "5"]],
        col_w=[3.6, 0.7], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER], idx=4)

    table_content(prs, "Las tres políticas del Estado",
        ["Política", "¿Quién la maneja?", "Herramienta principal"],
        [["**Fiscal**", "Ministerio de Hacienda", "Impuestos y gasto público"],
         ["**Monetaria**", "Banco de la República", "Tasa de interés de intervención"],
         ["**Cambiaria**", "Mercado (régimen flotante)", "Oferta y demanda de dólares"]],
        sub="El Estado tiene tres controles, como un carro", col_w=[1.1, 1.9, 2.2], idx=5, fs_body=13)

    content_slide(prs, "Política monetaria: el termostato",
        [("La **tasa de interés de intervención** del Banco de la República es el “precio del dinero”.", 0),
         ("@@Inflación alta → sube la tasa@@ → el crédito se encarece → se gasta menos → los precios se enfrían (freno).", 0),
         ("@@Economía lenta → baja la tasa@@ → el crédito se abarata → se consume e invierte más (acelerador).", 0)],
        top=2.2, size=16, idx=6)

    content_slide(prs, "Política cambiaria: el dólar sube y baja",
        [("Colombia tiene **régimen flotante**: el dólar lo fija el mercado, no un decreto.", 0),
         ("**Dólar sube (devaluación):** bueno para el @@exportador@@ y el turismo; malo para el @@importador@@.", 0),
         ("Un dato extra: una tasa de interés más alta suele **atraer dólares y fortalecer el peso**.", 0)],
        top=2.2, size=16, idx=7)

    content_slide(prs, "Los ciclos económicos",
        [("La economía sube y baja como una **montaña rusa**, en cuatro fases:", 0),
         ("**Expansión → Auge → Recesión → Recuperación**", 1),
         ("Algunos indicadores avisan temprano (líderes) y otros reaccionan tarde (rezagados, como el desempleo).", 0)],
        top=2.2, size=16, idx=8)

    table_content(prs, "Una medida, distintos sectores",
        ["Si el Banco SUBE la tasa de interés…", "Efecto"],
        [["**Construcción / vivienda**", "Se frena: los créditos hipotecarios se encarecen"],
         ["**Comercio minorista**", "Cae el consumo a cuotas; ventas más lentas"],
         ["**Exportador**", "Puede beneficiarse si el peso se fortalece y baja la inflación"]],
        sub="Ninguna medida es buena o mala para todos — depende del sector",
        col_w=[1.8, 2.8], idx=9, fs_body=13)

    content_slide(prs, "Tu actividad individual (15 min)",
        [("**“Una medida, dos sectores”.**", 0),
         ("Elige una medida de política económica reciente (verifica el dato en fuente oficial).", 0),
         ("Explica su **efecto esperado sobre dos sectores distintos**, con tu argumento.", 0),
         ("@@Entregable al LMS — segundo insumo de tu proyecto@@", 0)],
        top=2.0, size=16, idx=10)

    closing_slide(prs, "¿Qué logramos hoy?",
        ["Diferencio las 3 políticas · leo los ciclos · analizo el impacto por sector",
         "Próxima sesión: ¿Es Viable mi Emprendimiento? (Nivel 3 — Evaluar)"],
        "Ya tienes dos piezas del proyecto: tablero + análisis")

    out = BASE + "/Sesion 2/Presentacion Sesion 2.pptx"
    prs.save(out); return out

# =================================================================
# DECK 3 — SESIÓN 3 (Nivel 3 · Evaluar)
# =================================================================
def deck_s3():
    prs = new_prs()
    session_cover(prs, "SESIÓN 3",
        "Nivel 3 · Evaluar  —  Electiva Complementaria III",
        "¿Es Viable mi Emprendimiento?",
        "Evaluar una idea de negocio con los indicadores",
        "Hoy construyes tu dictamen final",
        ["Asignatura: **Electiva Complementaria III**",
         "Duración: **105 min**   ·   Tipo C — Proyecto Integrador"])

    content_slide(prs, "El camino que recorrimos",
        [("Sesión 1 — **Identificaste** los indicadores (tu tablero).", 0),
         ("Sesión 2 — **Analizaste** las políticas y su impacto por sector.", 0),
         ("Hoy, @@Nivel 3 — Evaluar@@: juntamos todo para decidir si un negocio es viable.", 0)],
        top=2.2, size=17, idx=2)

    content_slide(prs, "El propósito de hoy",
        ["@@Interpretar@@ los indicadores actuales para leer retos y oportunidades del entorno.",
         "@@Evaluar@@ la viabilidad de una idea de negocio según su sensibilidad a cada indicador.",
         "@@Argumentar@@ un dictamen de viabilidad claro y defendible."],
        top=2.2, size=17, idx=3)

    table_content(prs, "Cómo trabajaremos hoy (105 min)",
        ["Momento", "Min"],
        [["Motivación y encuadre", "15"],
         ["Enunciación — del macro al negocio", "20"],
         ["Modelación — un mini-dictamen", "20"],
         ["Ejercitación — empiezas tu dictamen", "25"],
         ["Cierre del curso", "10"],
         ["@@Tu entregable final (borrador)@@", "@@15@@"]],
        col_w=[3.6, 0.7], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER], idx=4)

    table_content(prs, "Del macro al negocio: 4 canales",
        ["Canal", "¿Cómo llega a tu negocio?"],
        [["**Costos / insumos**", "Inflación y dólar encarecen materias primas (sobre todo importadas)"],
         ["**Costo del crédito**", "La tasa de interés define cuánto cuesta financiarte"],
         ["**Demanda**", "El poder de compra de tus clientes sube o baja con el empleo y los precios"],
         ["**Tipo de cambio**", "Te ayuda si exportas; te golpea si importas"]],
        col_w=[1.4, 3.2], idx=5, fs_body=13)

    table_content(prs, "Matriz de sensibilidad (ejemplo)",
        ["Indicador", "Si sube…", "Riesgo para el negocio"],
        [["Inflación", "Suben costos y precios", "Alto si no puedo subir mis precios"],
         ["Tasa de interés", "Crédito más caro", "Alto si dependo de financiación"],
         ["Dólar (TRM)", "Importar cuesta más", "Alto si mis insumos son importados"],
         ["Desempleo", "Menos consumo", "Alto si vendo bienes no esenciales"]],
        sub="Evaluar = medir qué tan sensible es tu idea a cada aguja",
        col_w=[1.3, 1.5, 2.2], idx=6, fs_body=12)

    content_slide(prs, "Retos y oportunidades de Colombia",
        [("**Retos estructurales:** informalidad laboral y dependencia de las materias primas (commodities).", 0),
         ("**Oportunidades:** sectores que crecen, nichos sin atender, ventajas regionales.", 0),
         ("Un buen emprendedor **lee el entorno** antes de invertir: convierte datos en decisiones.", 0)],
        top=2.2, size=16, idx=7)

    content_slide(prs, "Cómo se arma un dictamen",
        [("1. **Lectura del entorno** con los indicadores (tu tablero actualizado).", 0),
         ("2. **Matriz de sensibilidad**: a qué indicadores es vulnerable tu idea.", 0),
         ("3. **Riesgos y oportunidades** concretos para ese negocio.", 0),
         ("4. @@Recomendación final argumentada@@: ¿viable, viable con ajustes, o no viable?", 0)],
        top=2.1, size=16, idx=8)

    content_slide(prs, "Tu entregable FINAL (15 min para arrancar)",
        [("**Dictamen de viabilidad (1–2 páginas)** de un emprendimiento que elijas.", 0),
         ("Incluye: lectura del entorno, matriz de sensibilidad, riesgos/oportunidades y recomendación.", 0),
         ("@@Es el entregable final del Proyecto Integrador — súbelo al LMS@@", 0)],
        top=2.1, size=16, idx=9)

    table_content(prs, "Rúbrica — qué hace un buen dictamen",
        ["Criterio", "Lo que se espera"],
        [["**Uso de datos**", "Indicadores oficiales, con fuente y fecha"],
         ["**Análisis**", "Conecta cada indicador con el negocio concreto"],
         ["**Argumentación**", "La recomendación se sostiene en los datos"],
         ["**Comunicación**", "Claro, ordenado y bien presentado"]],
        col_w=[1.4, 3.2], idx=10, fs_body=13)

    closing_slide(prs, "¡Completaste el curso!",
        ["Identificaste · Analizaste · Evaluaste: ya lees la economía como un profesional",
         "Recuerda diligenciar la encuesta de satisfacción"],
        "Entrega tu dictamen de viabilidad en el LMS")

    out = BASE + "/Sesion 3/Presentacion Sesion 3.pptx"
    prs.save(out); return out

if __name__ == "__main__":
    outs = [deck_presentacion(), deck_s1(), deck_s2(), deck_s3()]
    for o in outs:
        print("OK ->", o)
