# -*- coding: utf-8 -*-
"""
Genera los 3 decks .pptx del curso ELECTIVA DE PROFUNDIZACIÓN 3 — REDES DE NUEVA GENERACIÓN
(FESNA / La Nueva América). Identidad gráfica Nueva América (Barlow, naranja #FD531E para
resaltar, escala de grises, azul solo en logo/portada/velo de fotos).

Estructura:
  - Presentación del curso (11 slides) — EVALUACIÓN con porcentajes en placeholder
    "[ % por confirmar ]" (la coordinación aún no los define).
  - Clase 1 — Diseño de redes NGN: arquitecturas y tecnologías (~14 slides, 6 imágenes).
  - Clase 2 — Operación inteligente de redes NGN (~14 slides, 6 imágenes).

Config: config/cursos/electiva-profundizacion-3-redes-ngn.json
Motor:  config/slides/fesna_slides_engine.py  ·  Diagramas: config/slides/diagramas.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fesna_slides_engine import *
from pptx.enum.text import PP_ALIGN

set_footer("Electiva de Profundización 3 · Redes de nueva generación")

DIAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "diagramas")
BASE = r"g:\Mi unidad\Trabajos\Empleo\FESNA\Cursos\Electiva de Profundizacion 3 - Redes de nueva generacion\Clases"

def P(did):
    """Ruta del diagrama <did>.png si existe (si no, None -> la slide degrada a solo texto)."""
    p = os.path.join(DIAG_DIR, did + ".png")
    return p if os.path.exists(p) else None

CENTER = PP_ALIGN.CENTER
LEFT = PP_ALIGN.LEFT

TUTOR = ("Julian Andrés Castaño Espinosa",
         ["Líder Técnico", "Ingeniero de Sistemas", "Candidato a MsC en IA"],
         "julian.castano@lanuevaamerica.edu.co")

EXAMLAB = "https://examlab.lovable.app/app"

OBJ_1 = ("@@Diseñar@@ propuestas de redes de nueva generación comparando arquitecturas y "
         "tecnologías avanzadas, según requerimientos de desempeño, en contextos organizacionales "
         "y de telecomunicaciones.")
OBJ_2 = ("@@Evaluar@@ escenarios de conectividad NGN aplicando criterios de desempeño, seguridad y "
         "escalabilidad, y proponer soluciones técnicas alineadas con la responsabilidad profesional.")


# =================================================================
# DECK 0 — PRESENTACIÓN DEL CURSO (11 slides)
# =================================================================
def deck_presentacion():
    prs = new_prs()

    # 1 · Portada
    course_cover(prs,
        "Electiva de Profundización 3",
        "Redes de nueva generación",
        "¡Bienvenidos estudiantes!",
        ["**Programa** Ingeniería de Sistemas · Electiva de Profundización (flexible)",
         "Asignatura **Tipo A** · 2 créditos · Teórico-práctica",
         "Duración: **2 clases** de **105 min (1h45)** c/u",
         "Cuatrimestre y horario: [por confirmar]",
         "Fechas: 30/07/2026 – 08/08/2026"],
        start_note="Empezamos a las [hora]…")

    # 2 · Tutor
    tutor_slide(prs, TUTOR[0], TUTOR[1], TUTOR[2], idx=2)

    # 3 · Metodología
    table_content(prs, "Metodología",
        ["Momento", "¿Qué hacemos?"],
        [["**Motivación**", "Un caso real: una red que debe evolucionar a NGN"],
         ["**Encuadre**", "Objetivo de la clase, conceptos clave y ruta de trabajo"],
         ["**Modelación**", "El tutor diseña / diagnostica una red NGN paso a paso"],
         ["@@Simulación / Ejercitación@@", "Diagramas y comparativas en examlab y draw.io"],
         ["**Cierre**", "Síntesis e ideas fuerza de la clase"],
         ["**Evaluación**", "Evidencia de aprendizaje del día (Test / entregable)"]],
        sub="Cada clase de 105 min combina teoría, modelación y práctica",
        col_w=[1.2, 3.2], idx=3)

    # 4 · Objetivos (los 2 del EP)
    objectives_slide(prs, "Objetivos", [OBJ_1, OBJ_2], idx=4,
        title_in_card="Al finalizar el curso serás capaz de:")

    # 5 · Evaluación
    table_content(prs, "¿Cómo se evalúa?",
        ["Componente", "Ponderación"],
        [["**Destreza** — entrenamientos en la ruta de aprendizaje (LMS)", "@@50%@@"],
         ["**Notas de tus evidencias** — entregas del curso (LMS)", "@@40%@@"],
         ["**Asistencia** — al final de la sesión", "@@10%@@"],
         ["**Total**", "**100 %**"]],
        sub="Escala 0–5",
        note="Opcionales (bonificación): participación en clase +0.3 · Reto en vivo / Kahoot 🥇+0.5 · 🥈+0.4 · 🥉+0.3.",
        col_w=[3.4, 1.2], aligns=[LEFT, CENTER], idx=5)

    # 6 · Ejemplo de evaluación
    table_content(prs, "Así se calculará tu nota final",
        ["Componente", "Nota (ej.)", "Pond.", "Aporte"],
        [["Destreza — ruta de aprendizaje", "4.5", "50%", "4.5 × 0.50 = **2.25**"],
         ["Notas de tus evidencias", "4.0", "40%", "4.0 × 0.40 = **1.60**"],
         ["Asistencia", "5.0", "10%", "5.0 × 0.10 = **0.50**"],
         ["Reto en vivo (1er puesto, opcional)", "", "+0.5", "+ **0.50**"],
         ["**Nota final**", "", "", "@@2.25 + 1.60 + 0.50 + 0.50 = 4.85@@"]],
        sub="Ejemplo con notas ficticias",
        note="Fórmula: Nota final = Σ (nota del componente × su ponderación) + bonificaciones opcionales.",
        col_w=[2.4, 0.8, 0.8, 1.9],
        aligns=[LEFT, CENTER, CENTER, CENTER], idx=6)

    # 7 · Contenido (las 2 clases)
    table_content(prs, "Contenido del curso",
        ["Clase", "Título"],
        [["**1**", "Diseño de redes de nueva generación: arquitecturas y tecnologías"],
         ["**2**", "@@Operación inteligente de redes NGN@@: virtualización, IA, desempeño, seguridad y sostenibilidad"]],
        sub="2 clases sincrónicas de 105 min (1h45) · una por semana",
        col_w=[0.8, 4.8], aligns=[CENTER, LEFT], idx=7)

    # 8 · Recursos
    content_slide(prs, "Recursos del curso",
        [("**Material de clases** (guiones y diapositivas)", 0),
         ("🔗 [inserta aquí el hipervínculo]", 1),
         ("**Ruta de aprendizaje, guías y recursos**", 0),
         ("En examlab — " + EXAMLAB, 1),
         ("**Curso base (Coursera)**", 0),
         ("Electiva sin curso base asociado — [N/A o por confirmar]", 1),
         ("**Requisitos técnicos**", 0),
         ("@@Solo necesitas navegador web e internet — no se instala software@@", 1)],
        size=15, idx=8)

    # 9 · Herramientas (3 grupos, SIN Packet Tracer)
    content_slide(prs, "Herramientas",
        [("**En examlab** (" + EXAMLAB + ")", 0),
         ("Test / quiz · Reto en vivo (Kahoot) · pizarra y diagramas (Mermaid / Excalidraw) para arquitecturas · Taller para el entregable", 1),
         ("**Solo online (gratuitas)**", 0),
         ("draw.io / diagrams.net para diagramar topologías y arquitecturas NGN", 1),
         ("**En el mundo laboral** (contexto profesional)", 0),
         ("Controladores SDN (OpenDaylight / ONOS) · plataformas NFV y orquestación · GNS3 / EVE-NG · monitoreo de KPIs/QoS · Wireshark · dashboards de red", 1),
         ("@@Nunca usamos Packet Tracer ni software que se instale@@", 0)],
        size=14, idx=9)

    # 10 · Importante
    content_slide(prs, "Importante — entregas y plazos",
        [("@@La entrega final abre 8 días antes del cierre@@ y queda hasta el siguiente día hábil.", 0),
         ("**Publicación de notas:** dentro de los plazos institucionales tras el cierre.", 0),
         ("**Reclamaciones:** tienes 3 días para solicitar revisión, por correo al tutor.", 0),
         ("**Encuesta de satisfacción:** se diligencia el último día de clase.", 0)],
        size=16, idx=10)

    # 11 · Gestores (flyer real)
    image_slide(prs, "Gestores estudiantiles", GESTORES_IMG, idx=11)

    out = BASE + r"\Presentacion del curso.pptx"
    prs.save(out); return out


# =================================================================
# DECK 1 — CLASE 1 (Nivel 1 · Diseño de arquitecturas y tecnologías)
# =================================================================
def deck_clase1():
    prs = new_prs()

    # 1 · Portada de clase
    session_cover(prs, "CLASE 1",
        "Nivel 1 · Identificar y diseñar  —  Redes de nueva generación",
        "Diseño de redes de nueva generación",
        "Arquitecturas y tecnologías",
        "Hoy diseñas y comparas arquitecturas NGN",
        ["Asignatura: **Electiva de Profundización 3**",
         "Duración: **105 min (1h45)**   ·   Semana 1"])

    # 2 · Propósito + niveles de logro
    content_slide(prs, "El propósito de hoy",
        [("@@Diseñar@@ una propuesta preliminar de red NGN comparando arquitecturas y tecnologías, según requerimientos de desempeño.", 0),
         ("**Niveles de logro de la asignatura:**", 0),
         ("@@Nivel 1 — Identificar@@ conceptos de NGN, SDN/NFV y QoS  (foco de hoy)", 1),
         ("Nivel 2 — Analizar e interpretar escenarios de red", 1),
         ("Nivel 3 — Aplicar y sustentar decisiones con lenguaje técnico", 1)],
        size=16, idx=2)

    # 3 · Evolución (IMG)
    image_text_slide(prs, "De las redes tradicionales a NGN",
        [("La infraestructura de red evolucionó por saltos; cada uno resolvió un límite del anterior.", 0),
         ("**Tradicionales:** circuitos dedicados; voz y datos separados; hardware propietario.", 1),
         ("**Convergentes (IP):** todo viaja sobre IP en una sola red.", 1),
         ("@@NGN:@@ red virtualizada, programable y automatizada.", 1)],
        P("ngn_evolucion"), size=15, layout="right", idx=3)

    # 4 · ¿Qué es NGN? (texto)
    content_slide(prs, "¿Qué es una red de nueva generación?",
        [("Una @@red de nueva generación (NGN)@@ es una red basada en paquetes (IP) donde las funciones de red se **desacoplan del hardware** y se controlan por software.", 0),
         ("Un único transporte convergente lleva **voz, datos y video** con la calidad que cada servicio necesita.", 0),
         ("Objetivo: más **flexibilidad, escalabilidad y automatización**; menos dependencia de equipos propietarios.", 0)],
        size=16, idx=4)

    # 5 · Tradicional vs NGN (IMG)
    image_text_slide(prs, "Red tradicional vs. red NGN",
        [("La diferencia clave: en NGN el **software de la red se separa del hardware** que transporta los paquetes.", 0),
         ("Tradicional: control equipo por equipo; se escala comprando hardware.", 1),
         ("@@NGN: control centralizado (SDN) y funciones virtualizadas (NFV); escala como la nube.@@", 1)],
        P("ngn_tradicional_vs_ngn"), size=15, layout="right", idx=5)

    # 6 · KPIs (IMG)
    image_text_slide(prs, "Indicadores de desempeño en NGN",
        [("Para diseñar y comparar necesitas medir. Estos KPIs son el lenguaje del desempeño:", 0),
         ("**Latencia** y **jitter** mandan en tiempo real (voz, video, 5G).", 1),
         ("**Throughput:** la capacidad real, no la nominal.", 1),
         ("@@Disponibilidad:@@ los 'nueves' del SLA (99,9 % ≈ 8,7 h de caída al año).", 1)],
        P("ngn_kpis"), size=15, idx=6)

    # 7 · Arquitectura NGN empresarial (IMG)
    image_text_slide(prs, "Arquitectura de una red NGN empresarial",
        [("Una red NGN se piensa por **capas funcionales**, no por cajas sueltas:", 0),
         ("**Acceso** (fibra, 5G, Wi-Fi 6/7) → **Transporte** (IP/MPLS) → **Control** (SDN) → **Servicios**.", 1),
         ("El @@plano de control se separa del transporte@@: ahí vive la inteligencia programable.", 1)],
        P("ngn_arquitectura_capas"), size=15, layout="right", idx=7)

    # 8 · Disponibilidad y redundancia (IMG)
    image_text_slide(prs, "Disponibilidad y redundancia",
        [("Una buena red no es la que nunca falla, sino la que **sigue funcionando cuando algo falla**.", 0),
         ("Elimina el **punto único de fallo (SPOF)**: enlaces, equipos, energía y respaldo redundantes.", 1),
         ("@@Redundancia + failover@@ = alta disponibilidad (más 'nueves' de SLA).", 1)],
        P("ngn_redundancia"), size=15, idx=8)

    # 9 · Comparativa de conectividad (tabla)
    table_content(prs, "Comparativa de tecnologías de conectividad",
        ["Tecnología", "Fortaleza", "Límite / cuándo evitarla"],
        [["**Fibra óptica**", "Alto ancho de banda, baja latencia, estable", "Costo de despliegue y obra civil"],
         ["**Cobre / DSL**", "Bajo costo; ya está instalado", "Distancia y ancho de banda limitados"],
         ["**Inalámbrico / 5G**", "Movilidad y despliegue rápido", "Interferencia; depende de la cobertura"],
         ["**Satélite (LEO)**", "Cobertura donde no llega el cable", "Mayor latencia/costo; sensible al clima"]],
        note="No hay una tecnología 'mejor': se elige según requisitos, cobertura, latencia y costo.",
        col_w=[1.4, 2.4, 2.4], idx=9, fs_body=12)

    # 10 · Cómo elegir tecnología (IMG)
    image_text_slide(prs, "¿Cómo elegir la tecnología?",
        [("Elegir bien es un **proceso de decisión**, no seguir la moda:", 0),
         ("Parte de los **requisitos del negocio** → define **criterios técnicos** → **compara** tecnologías.", 1),
         ("@@La decisión final se justifica@@ por la mejor relación desempeño / costo.", 1)],
        P("ngn_seleccion"), size=15, layout="right", idx=10)

    # 11 · Diseño preliminar (texto)
    content_slide(prs, "Diseño preliminar de una red NGN",
        [("Un diseño preliminar responde, en un diagrama, a 4 preguntas:", 0),
         ("**1. ¿Qué conecta?** usuarios, sedes, servidores y nube.", 1),
         ("**2. ¿Con qué capas?** acceso, transporte, control y servicios.", 1),
         ("**3. ¿Con qué tecnología?** justificada con criterios y KPIs.", 1),
         ("**4. ¿Cómo sobrevive a fallos?** redundancia y disponibilidad.", 1),
         ("@@Hoy tú dibujas ese diagrama en examlab (pizarra) o draw.io.@@", 0)],
        size=15, idx=11)

    # 12 · Trabajo autónomo
    content_slide(prs, "Trabajo autónomo (15 min)",
        [("**Reto:** diseña el **diagrama preliminar de una red NGN** para una empresa con 2 sedes.", 0),
         ("Incluye las capas (acceso/transporte/control/servicios), la **tecnología elegida con su justificación** y un mecanismo de **redundancia**.", 0),
         ("**Criterio de éxito:** el diagrama muestra las capas, al menos una tecnología justificada por KPIs y un punto de redundancia.", 0),
         ("@@Herramientas: examlab (pizarra/diagramas) o draw.io — sin instalar nada.@@", 0),
         ("📤 **Entregable:** sube tu diagrama al Taller de examlab (imagen o enlace).", 0)],
        size=15, idx=12)

    # 13 · ¿Qué logramos hoy?
    content_slide(prs, "¿Qué logramos hoy?",
        [("Entiendo la **evolución** de las redes tradicionales a NGN y qué la hace distinta.", 0),
         ("Sé leer los **KPIs** y aplicar **redundancia** para lograr alta disponibilidad.", 0),
         ("Puedo **comparar tecnologías** y **diseñar** una red NGN preliminar justificada.", 0)],
        size=17, idx=13)

    # 14 · Cierre
    closing_slide(prs, "¡Buen trabajo hoy!",
        ["Diseñaste y comparaste: evolución NGN · KPIs · redundancia · selección de tecnología",
         "Próxima clase: Operación inteligente de redes NGN (SDN/NFV, IA, QoS, seguridad y sostenibilidad)"],
        "📤 Sube tu diagrama al Taller de examlab")

    out = BASE + r"\Clase 1\Clase 1 - Diseño de redes de nueva generación - arquitecturas y tecnologías.pptx"
    prs.save(out); return out


# =================================================================
# DECK 2 — CLASE 2 (Nivel 2 · Operación inteligente)
# =================================================================
def deck_clase2():
    prs = new_prs()

    # 1 · Portada de clase
    session_cover(prs, "CLASE 2",
        "Nivel 2 · Analizar y evaluar  —  Redes de nueva generación",
        "Operación inteligente de redes NGN",
        "Virtualización, IA, desempeño, seguridad y sostenibilidad",
        "Hoy evalúas y operas la red con criterios profesionales",
        ["Asignatura: **Electiva de Profundización 3**",
         "Duración: **105 min (1h45)**   ·   Semana 2"])

    # 2 · Propósito + niveles de logro
    content_slide(prs, "El propósito de hoy",
        [("@@Evaluar@@ escenarios de conectividad NGN con criterios de desempeño, seguridad y escalabilidad, y **proponer soluciones**.", 0),
         ("**Niveles de logro de la asignatura:**", 0),
         ("Nivel 1 — Identificar conceptos de NGN", 1),
         ("@@Nivel 2 — Analizar e interpretar escenarios@@  (foco de hoy)", 1),
         ("Nivel 3 — Aplicar y sustentar decisiones con lenguaje técnico", 1)],
        size=16, idx=2)

    # 3 · SDN: planos (IMG)
    image_text_slide(prs, "SDN: el cerebro de la red NGN",
        [("**SDN (Software-Defined Networking)** separa la red en planos:", 0),
         ("**Datos** (los equipos reenvían) · **Control** (el controlador decide) · **Aplicación** (apps de red).", 1),
         ("@@Un solo 'cerebro' central programa toda la red@@ por software, sin tocar equipo por equipo.", 1)],
        P("ngn_sdn_planos"), size=15, idx=3)

    # 4 · SDN / NFV / orquestación (IMG)
    image_text_slide(prs, "SDN, NFV y orquestación",
        [("Tres piezas que trabajan juntas en NGN:", 0),
         ("**SDN:** programa el comportamiento de la red (control central).", 1),
         ("**NFV:** convierte funciones de red (firewall, router) en **software** sobre servidores.", 1),
         ("@@Orquestación (MANO):@@ despliega y coordina todo automáticamente.", 1)],
        P("ngn_sdn_nfv"), size=15, idx=4)

    # 5 · Automatización (texto)
    content_slide(prs, "Automatización y administración centralizada",
        [("La automatización reemplaza la configuración manual **caja por caja** por cambios **centralizados y repetibles**.", 0),
         ("Beneficios: menos errores humanos, despliegues en minutos y **escalabilidad** real.", 0),
         ("@@La red se administra como código@@ (políticas y plantillas), no comando por comando.", 0)],
        size=16, idx=5)

    # 6 · IA aplicada a telecom (IMG)
    image_text_slide(prs, "IA aplicada a las telecomunicaciones",
        [("La IA hace que la red **aprenda y se anticipe**:", 0),
         ("**Predicción** de demanda y congestión · **optimización** automática de rutas.", 1),
         ("**Mantenimiento predictivo** (avisa antes de la caída) · @@detección de anomalías y ataques@@.", 1)],
        P("ngn_ia_telecom"), size=15, idx=6)

    # 7 · KPIs, monitoreo, diagnóstico (IMG dashboard)
    image_text_slide(prs, "Métricas, KPIs y monitoreo inteligente",
        [("No puedes mejorar lo que no mides: el **monitoreo** vigila los KPIs en tiempo real.", 0),
         ("Un **dashboard** resume disponibilidad, latencia, jitter y tráfico en un 'semáforo'.", 0),
         ("@@El diagnóstico@@ correlaciona métricas para hallar la causa raíz de un problema.", 0)],
        P("ngn_dashboard"), size=15, layout="right", idx=7)

    # 8 · QoS (IMG)
    image_text_slide(prs, "QoS y optimización del tráfico",
        [("**QoS (Quality of Service)** decide **qué tráfico pasa primero** cuando la red se congestiona.", 0),
         ("Flujo: **clasificar → marcar → encolar/priorizar → gestionar congestión**.", 1),
         ("@@La voz y el video en tiempo real@@ tienen prioridad sobre una descarga.", 1)],
        P("ngn_qos"), size=15, layout="right", idx=8)

    # 9 · Análisis de tráfico y ciberseguridad (IMG anomalías)
    image_text_slide(prs, "Análisis de tráfico y ciberseguridad con IA",
        [("La IA aprende el **patrón normal** del tráfico (baseline) y señala lo que se sale de él.", 0),
         ("Un pico raro puede ser un **ataque** (DDoS) o una fuga: la IA **alerta y mitiga** automáticamente.", 0),
         ("@@Seguridad proactiva:@@ detectar la anomalía antes de que cause daño.", 0)],
        P("ngn_anomalias"), size=15, idx=9)

    # 10 · Sostenibilidad y resiliencia (texto)
    content_slide(prs, "Sostenibilidad y resiliencia",
        [("Las redes NGN y sus **centros de datos** consumen mucha energía: la eficiencia es un criterio de diseño.", 0),
         ("**Eficiencia energética** (PUE), **refrigeración** eficiente y **energías renovables**.", 1),
         ("**Resiliencia:** la red se recupera de fallos y ataques y mantiene el servicio.", 1),
         ("@@Diseñar verde y resiliente@@ ya es parte de la responsabilidad profesional.", 0)],
        size=16, idx=10)

    # 11 · Comunicación técnica (texto)
    content_slide(prs, "Comunicación técnica: informes y dashboards",
        [("Un buen ingeniero **comunica** sus hallazgos: un diseño o diagnóstico vale por cómo se sustenta.", 0),
         ("**Informe técnico:** contexto, KPIs medidos, hallazgos y recomendaciones con lenguaje profesional.", 0),
         ("@@Dashboards@@ para el día a día; **informes** para decidir e invertir.", 0)],
        size=16, idx=11)

    # 12 · Trabajo autónomo
    content_slide(prs, "Trabajo autónomo (15 min)",
        [("**Reto:** recibes un escenario NGN con sus KPIs (latencia, disponibilidad, tráfico y una anomalía).", 0),
         ("**Evalúa** el escenario: ¿cumple el SLA? ¿dónde está el riesgo de seguridad o el cuello de botella?", 0),
         ("Propón **2 mejoras** justificadas (QoS, redundancia, automatización, seguridad o sostenibilidad).", 0),
         ("@@Herramientas: examlab (Test + diagramas) o draw.io — sin instalar nada.@@", 0),
         ("📤 **Entregable:** sube un **mini-informe** (o dashboard conceptual) al Taller de examlab.", 0)],
        size=15, idx=12)

    # 13 · ¿Qué logramos hoy?
    content_slide(prs, "¿Qué logramos hoy?",
        [("Entiendo **SDN, NFV y orquestación** y cómo la **IA** opera la red.", 0),
         ("Sé leer **KPIs / QoS** y aplicar **seguridad** con detección de anomalías.", 0),
         ("Puedo **evaluar** un escenario NGN y **proponer** mejoras con criterios profesionales.", 0)],
        size=17, idx=13)

    # 14 · Cierre
    closing_slide(prs, "¡Cerramos la electiva!",
        ["Operación inteligente: SDN/NFV · IA · KPIs/QoS · seguridad · sostenibilidad",
         "Recuerda diligenciar la encuesta de satisfacción"],
        "📤 Sube tu mini-informe al Taller de examlab")

    out = BASE + r"\Clase 2\Clase 2 - Operación inteligente de redes NGN.pptx"
    prs.save(out); return out


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    outs = [deck_presentacion(), deck_clase1(), deck_clase2()]
    for o in outs:
        print("OK ->", o)
