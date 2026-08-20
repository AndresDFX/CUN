# -*- coding: utf-8 -*-
r"""Inyecta el FORMULARIO OFICIAL DEL JURADO (5 criterios, escala 1-5) en cada
`4 - Evaluacion.md` de las fichas de sustentación, y consolida la matriz 13x5 en el índice.

**Por qué existe este script y no se editaron los 13 archivos a mano.** El formulario que la
Dirección le pide al jurado es un instrumento **distinto** de la rúbrica de Proyecto II · ACA 3
(instructivo unificado, p. 22) que las fichas ya traen plantillada en su §2. Son cinco preguntas,
cada una con opciones `1 2 3 4 5`:

  1. Planteamiento de la problemática y formulación de objetivos
  2. Marco teórico y referentes conceptuales
  3. Metodología, muestra y coherencia del diseño
  4. Resultados y conclusiones
  5. Pertinencia disciplinar y articulación con la especialización

**Ninguna de las cinco califica la sustentación oral.** Las cinco se responden con el documento
en la mano, así que se pueden precargar **antes** de la sala —que es la única forma de aprovechar
los ~3 minutos que le tocan al Jurado 2 en turnos de 20 minutos con tres evaluadores—. Este script
las escribe como una nueva §3 en los 13 archivos y renumera las secciones siguientes (§3→§4,
§4→§5, §5→§6), de modo que los 13 queden con la misma estructura. Es idempotente: si la sección
ya está, la reemplaza.

⚠️ **El 1-5 de este formulario no es la nota 0,1-5,0 del acta.** La nota final del estudiante es
75 % metodólogo + 25 % jurados, con meritoria ≥ 4,6 y ninguna individual por debajo de 4,5. El
1-5 de aquí es un ordinal de calidad **documental**, con esta lectura fijada de antemano:

  5 · sobresaliente, sin reparos de fondo
  4 · sólido, con reparos menores y declarados
  3 · aceptable, con un reparo de fondo que el documento no resuelve
  2 · deficiente: hay material, pero se contradice o no sostiene lo que afirma
  1 · sin base verificable en el documento

Cada respuesta se sostiene con página del documento del grupo, tomada de la ficha
`1 - Ficha de preparacion.md` de ese grupo, y va acompañada de qué la subiría o la bajaría una
casilla en sala.

**G-011 no se puntúa.** Su carpeta de Drive está vacía (cero archivos, verificado el 15/08/2026):
sin documento no hay base probatoria para ninguno de los cinco criterios, y el script escribe el
protocolo condicional en vez de inventar números.

Uso:
    python config/evaluaciones/formulario_jurado.py --simular    # muestra el plan, no toca nada
    python config/evaluaciones/formulario_jurado.py --confirmar  # escribe los 14 archivos
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHAS = os.path.join(
    RAIZ, "Especializacion", "Evaluaciones", "2026-2", "Fichas de evaluacion"
)
INDICE = os.path.join(FICHAS, "00 - Indice y agenda de sustentaciones.md")

CRITERIOS = [
    "Planteamiento de la problemática y formulación de objetivos",
    "Marco teórico y referentes conceptuales",
    "Metodología, muestra y coherencia del diseño",
    "Resultados y conclusiones",
    "Pertinencia disciplinar y articulación con la especialización",
]

CABECERA = """## 3. Formulario oficial del jurado — 5 criterios en escala 1–5

> **Instrumento distinto de la rúbrica del ACA 3** de la §2: son las cinco preguntas del
> formulario que la Dirección le pide al jurado, cada una con opciones **1 2 3 4 5**. Ninguna de
> las cinco califica la sustentación oral, así que **las cinco se responden con el documento** y
> van precargadas aquí, con la página que las sostiene, **antes** de entrar a la sala.
>
> ⚠️ **Este 1–5 no es la nota 0,1–5,0 del acta.** La nota final es 75 % metodólogo + 25 % jurados,
> con meritoria ≥ 4,6 y ninguna individual por debajo de 4,5. Aquí el 1–5 es un ordinal de calidad
> **documental**, con esta lectura fijada de antemano: **5** sobresaliente, sin reparos de fondo ·
> **4** sólido, con reparos menores y declarados · **3** aceptable, con un reparo de fondo que el
> documento no resuelve · **2** deficiente: hay material, pero se contradice o no sostiene lo que
> afirma · **1** sin base verificable en el documento.
>
> La casilla que se marca en el formulario la marca el jurado humano. Esto es una propuesta con
> página, y **la §8 de la ficha manda sobre la nota del acta**, no esta suma.
"""

# ---------------------------------------------------------------------------
# Las respuestas, grupo por grupo. Cada criterio: (casilla, sustento con página).
# ---------------------------------------------------------------------------

DATOS: dict[str, dict] = {
    "G-001": {
        "carpeta": "01 - G-001 - Sistema agropecuario TuFinca con chatbot",
        "respuestas": [
            (5, "Título, objetivo general (p. 35) y pregunta de investigación (p. 34) dicen lo "
                "mismo, el problema está delimitado a una unidad productiva concreta (pp. 32, 40) "
                "y la madurez se declara como TRL 5-6 sin pretensión comercial (p. 42). Los cuatro "
                "objetivos específicos tienen sección de resultados que los cierra, incluido el "
                "«evaluar» que casi nadie ejecuta. Sin reparos: el plural «chatbots» viene del "
                "listado de la Dirección, no del trabajo —el título (pp. 1-2) y el objetivo general "
                "(p. 35) dicen «chatbot» en singular, y «chatbots» aparece una sola vez en las 273 "
                "páginas (p. 51)—; se entrega uno, con WhatsApp declarado como trabajo futuro "
                "(p. 22)."),
            (4, "Marco conceptual pertinente y continuidad con la Fase I citada como antecedente "
                "sin apropiársela (pp. 56, 64). No llega a 5 por dos razones verificables: las "
                "entradas de pp. 250-255 que no se citan en el cuerpo pasan de una docena "
                "(ASOHOFRUCOL, Uniminuto, QGIS, MQTT, Bahga y Madisetti, Ander-Egg 1990, Yin, "
                "Hernández-Sampieri, Tamayo y Tamayo, Troelsen, Zabaleta, Clavijo, Li, Rivera y "
                "Saltos), varias de ellas arrastre del dominio agrícola de la fase anterior; y la "
                "tecnología del motor conversacional no tiene referente conceptual propio en las "
                "273 páginas: IBM Watson 2021 figura **solo** en el listado (p. 252) y OpenAI 2021, "
                "aunque sí se cita tres veces en el cuerpo (pp. 29, 32, 36), aparece únicamente "
                "dentro de cadenas de autoridad, nunca sosteniendo el componente (Tabla 18, "
                "p. 171)."),
            (4, "Estudio descriptivo y aplicado (p. 65), de enfoque mixto (pp. 64 y 66), Scrum con "
                "14 sprints (p. 45), muestreo intencional que corresponde a la totalidad de los "
                "operarios vinculados a los procesos pecuarios de la finca (pp. 67-68), "
                "instrumentos declarados (p. 71) y —lo que "
                "distingue este trabajo— umbrales de interpretación fijados **antes** de aplicar el "
                "instrumento y declarados locales, no normativos (pp. 199-200). No llega a 5 porque "
                "el «antes» que promete el OE4 (p. 35) es una condición reproducida en la misma "
                "jornada con los mismos seis operarios que ya conocían el sistema (p. 196), y "
                "porque se plantea H₀/H₁ formal (p. 34) con tratamiento estadístico solo descriptivo "
                "(p. 66)."),
            (5, "Publican los conteos crudos y no solo los porcentajes (Tabla 30, p. 213: 65/90, "
                "88/90, 47/60, 56/60), y recalculados cuadran —es la firma de una medición que de "
                "verdad ocurrió—. Los cuatro objetivos cierran con resultados (pp. 209-213) y las "
                "conclusiones se autolimitan a «mejoras descriptivas» que no constituyen "
                "demostración poblacional (p. 238), reconociendo incluso que el indicador de "
                "trazabilidad aún no cubre auditoría (p. 232). Única errata: 98,8 % en la Tabla 27 "
                "(p. 210) frente a 59/60 = 98,3 % del conteo crudo (p. 213); el dato bueno es "
                "98,3 %, y así lo dice también la narrativa (p. 232) y la propia Tabla 27 sumando "
                "78,3 + 20,0."),
            (5, "Sistema desplegado en Azure App Service y verificado (pp. 191-194) y entregado con "
                "acta de certificación a la unidad productiva (p. 218), en la línea «Liderazgo y "
                "Adaptación con Tecnologías Emergentes». Es transformación digital ejecutada sobre "
                "un proceso real, no propuesta."),
        ],
        "sube": "El **criterio 2 pasa a 5** si nombran con precisión el componente que resuelve "
                "intención y entidades (pregunta prioritaria 1): eso le da referente conceptual al "
                "núcleo del producto. Nada más puede subir: los criterios 1, 4 y 5 ya están en el "
                "techo y el reparo del criterio 3 es de diseño ya ejecutado, no se corrige hablando.",
        "baja": "El **criterio 4 baja a 4** si defienden el 63-95 % como impacto poblacional o "
                "niegan que la condición manual se reprodujo en la misma jornada de pruebas "
                "(p. 196). El **criterio 5 baja a 4** si no saben si el despliegue sigue en línea "
                "hoy o si la sostenibilidad del hosting no tiene responsable ni cifra: en 273 "
                "páginas no aparece la palabra «presupuesto» y a la finca se le recomienda poner "
                "fecha de fin a los registros en papel (pp. 46, 245).",
    },
    "G-002": {
        "carpeta": "02 - G-002 - Plataforma turistica PWA Rivera Huila",
        "nota_cita": "En este grupo el **folio impreso va dos números por debajo de la página del "
                     "PDF**; las páginas de esta tabla son las del PDF, como en toda la ficha.",
        "respuestas": [
            (4, "Título, pregunta y objetivo general apuntan al mismo sitio y los 25 requerimientos "
                "en 7 categorías (p. 40) delimitan bien el alcance funcional. Baja de 5 porque el "
                "documento entregado como final todavía se llama «anteproyecto» en tres sitios "
                "(pp. 11, 15, 47) y porque el objetivo general promete «fortalecer los "
                "emprendimientos productivos», un nivel de efecto que el trabajo nunca se pone en "
                "condiciones de medir."),
            (2, "Es el criterio más débil del trabajo y se sostiene con un solo dato: **10 "
                "referencias en total** (p. 86), **ninguna posterior a 2021** y **ninguna sobre "
                "PWA**, que es la tecnología que da nombre y sentido al proyecto. Además la p. 31 "
                "cita «(Pressman, 2014)» mientras la lista registra Pressman & Maxim (2020). Un "
                "producto construido sobre una arquitectura de la que no se cita literatura no "
                "tiene sustento teórico, tenga el producto la calidad que tenga."),
            (3, "El diseño es interiormente coherente y —esto cuenta a favor— el propio documento "
                "declara que con n = 3 actores institucionales por muestreo intencional los "
                "resultados muestran tendencias y no permiten inferencia (p. 38). La trazabilidad "
                "requerimiento → módulo está tabulada (Tabla 20, p. 79). El reparo de fondo: con "
                "tres informantes se sostiene un diagnóstico de necesidades, no la evaluación de "
                "impacto que el OE4 promete, y no hay cronograma ni presupuesto en las 86 páginas."),
            (3, "Lo verificable está bien verificado: URL pública con TLS (p. 74), condición de PWA "
                "probada con manifest, service worker y ocho tamaños de icono (Tabla 16, "
                "pp. 75-76), mediana de respuesta ~101 ms (p. 78). Pero el **OE4 no se ejecutó**: el "
                "protocolo de usabilidad está diseñado y la columna «Valor obtenido» de la Tabla 23 "
                "está en blanco (p. 82); y el estado del chat se reporta en dos versiones "
                "incompatibles —«siguiente fase de desarrollo» (pp. 69-70) frente a «opera sobre el "
                "entorno productivo» (pp. 73, 84)—. Con un objetivo sin resultado y una "
                "contradicción sobre el producto, las conclusiones no pueden cerrar."),
            (4, "Una PWA turística municipal en producción, con URL pública y flujo de moderación de "
                "la Secretaría, es transformación digital aplicada a un territorio concreto y el "
                "aporte es demostrable sin depender de la sala. No llega a 5 porque el efecto sobre "
                "los emprendimientos —el aporte que el objetivo general reclama— no está medido."),
        ],
        "sube": "El **criterio 4 pasa a 4** si el chat funciona en vivo y aclaran cuál de los dos "
                "estados es el de hoy (pregunta prioritaria 1), o si aparecen publicaciones creadas "
                "por empresarios de Rivera que pasaron por moderación (pregunta 3). El criterio 2 no "
                "sube: la bibliografía es lo que está impreso.",
        "baja": "El **criterio 4 baja a 2** si sostienen que el objetivo 4 está cumplido con el "
                "diseño del instrumento, sin aplicarlo. El **criterio 1 baja a 3** si en sala "
                "presentan el trabajo como anteproyecto o no distinguen lo entregado de lo "
                "proyectado.",
    },
    "G-003": {
        "carpeta": "03 - G-003 - Modernizacion archivo municipal San Francisco",
        "respuestas": [
            (3, "El problema está bien delimitado y es real —archivo municipal, FUID del Acuerdo 042 "
                "de 2002, vigencia 2024— y los objetivos son claros. El reparo de fondo está en el "
                "alcance: la **p. 27 afirma en pasado** un despliegue piloto, jornadas de "
                "digitalización y sesiones de capacitación de las que no hay una sola evidencia en "
                "el resto de las 169 páginas, y el OE4 promete verificar «en un entorno institucional "
                "controlado» algo que se verificó en un portátil personal, en localhost:5000 "
                "(pp. 89-91)."),
            (2, "El anclaje normativo es correcto y pertinente (Acuerdo 042 de 2002, AGN). Lo que "
                "impide más de un 2 es material y no interpretable: la bibliografía llega al "
                "documento final con **marcadores «[por verificar]»** (pp. 138-140) y hay citas del "
                "cuerpo que no existen en la lista (Contraloría 2024, AGN 2024, MinTIC 2024). Un "
                "referente que el propio documento marca como no verificado no puede fundamentar "
                "nada."),
            (2, "Hay trabajo de campo real: matriz de 20 aspectos en 6 dimensiones con escala 1-5 y "
                "cuatro entrevistas fechadas el 24/06/2026. Pero **la muestra nunca se cuantifica** "
                "en las 169 páginas y el documento declara tres veces que no es censal (pp. 78, 86, "
                "130), mientras la diapositiva 4 dice «muestra de tipo censal». Un diseño cuyo "
                "número de unidades analizadas no aparece en ninguna página, y cuyo propio mazo lo "
                "contradice, no acredita coherencia interna. Tampoco hay sección de limitaciones."),
            (3, "El diagnóstico está bien construido y es la parte fuerte: 1,9/5 global (p. 81) "
                "desagregado en trazabilidad 1,33, tecnología 1,67, organización 1,75 y conservación "
                "3,25 (p. 82). Y la **Tabla 14 (pp. 104-105) es lo mejor de todo el cohorte en "
                "honestidad de reporte**: clasifica cada componente como implementado, representado, "
                "diseñado o proyectado. Lo que lo frena en 3 es que las diapositivas 7 y 10 "
                "concluyen «cifrado de grado militar (AES-256)» sobre un componente que esa misma "
                "Tabla 14 marca como solo representado en la interfaz: el documento se corrige y el "
                "mazo lo deshace."),
            (4, "Gestión documental electrónica en una alcaldía, con SGDEA, DCF de tres niveles, DRS, "
                "modelo ER de 14 entidades, RBAC de 6 perfiles y auditoría append-only "
                "(pp. 89-91): es transformación digital del sector público con necesidad "
                "documentada. No llega a 5 porque nada de eso salió del portátil."),
        ],
        "sube": "El **criterio 4 pasa a 4** si sostienen en sala la distinción de su propia Tabla 14 "
                "—qué quedó implementado y probado frente a qué está representado— en vez de "
                "defender la diapositiva 10 (pregunta prioritaria 1). El **criterio 3 pasa a 3** si "
                "dan una cifra de expedientes o folios inventariados y el criterio con que se "
                "escogieron (pregunta 2).",
        "baja": "El **criterio 1 baja a 2** si defienden como ejecutado el despliegue de la p. 27. "
                "Ojo con el tiempo: son cuatro integrantes en 20 minutos, y si solo exponen sin "
                "responder, el que se resiente es el criterio 3, no estos cinco.",
    },
    "G-004": {
        "carpeta": "04 - G-004 - Gestion del cambio en seguridad electronica",
        "respuestas": [
            (3, "El problema está claramente planteado y el trabajo es de los más ordenados del "
                "cohorte en estructura. El reparo de fondo es de formulación: el objetivo general "
                "dice **«determinar la incidencia»** sobre un diseño descriptivo-correlacional "
                "(p. 37), que por definición no determina incidencia; y el documento acaba "
                "afirmando causalidad desde ese diseño (p. 99). El verbo del objetivo está por "
                "encima de lo que el diseño puede entregar, y ahí nace la contradicción del "
                "criterio 4."),
            (3, "Marco de gestión del cambio utilizable y coherente con el objeto, con producto "
                "derivado (Estrategia de Sostenibilidad en tres líneas, revisada por nueve expertos "
                "internos, p. 108). Baja de 4 porque **diez obras citadas en el cuerpo no están en "
                "la lista de referencias** (pp. 137-140)."),
            (3, "Tiene lo que casi nadie: psicometría real. Instrumento de 9 ítems Likert más uno de "
                "0-10 (p. 55), prueba piloto con 30 y **alfa de Cronbach 0,924** (pp. 75-77), 1.000 "
                "registros llevados a Power BI. Dos reparos que lo dejan en 3: el alfa **nunca se "
                "recalcula sobre la base final**, y el denominador se reporta de tres maneras "
                "distintas —los mil usuarios son el 33 % de la entidad (p. 42), el 33 % de la "
                "población contactada (p. 48) y «los 1.000 funcionarios del Nivel Central» (p. 74), "
                "más las diapositivas 7 y 10—. Además IND_CAPAC e IND_ACOMP se construyen con un "
                "solo ítem cada uno (p. 100), que es un índice de nombre."),
            (2, "Es el hueco más grave del cohorte y no admite lectura benévola: **dos modelos OLS "
                "incompatibles sobre el mismo objetivo general**. La p. 98 da p = 0,000, β = 0,5746 "
                "y R² = 0,076 y se vende como incidencia probada; las pp. 101-102, con los mismos "
                "mil registros, dan Spearman 0,052, R² = 0,003 y p = 0,063, y el propio texto "
                "escribe que «carecen de significancia estadística». El resumen (p. 11) y la "
                "conclusión 3 (p. 134) se quedan con la primera versión. A favor: el documento "
                "declara con franqueza que la estrategia **no** se implementó (pp. 120, 132)."),
            (4, "Gestión del cambio para la adopción de tecnología en seguridad electrónica, con "
                "inventario documental real y una estrategia de sostenibilidad revisada "
                "internamente: encaja de lleno en la dimensión organizacional de la transformación "
                "digital. No llega a 5 porque el producto no se implementó y el efecto no se midió."),
        ],
        "sube": "El **criterio 4 pasa a 3** si dicen sin rodeos cuál de los dos modelos responde el "
                "objetivo general y qué cambió entre uno y otro (pregunta prioritaria 1) —reconocer "
                "que el resultado no es significativo es la respuesta que sube, no la que baja—. El "
                "**criterio 3 pasa a 4** si ordenan el denominador con tres cifras: cuántos "
                "trabajan en Nivel Central, a cuántos se envió y cuántos respondieron (pregunta 2).",
        "baja": "El **criterio 4 baja a 1** si sostienen en sala la incidencia significativa sin "
                "mencionar las pp. 101-102, o si atribuyen causalidad al diseño correlacional. El "
                "**criterio 1 baja a 2** si defienden que un diseño correlacional «determina "
                "incidencia».",
    },
    "G-005": {
        "carpeta": "05 - G-005 - Prediccion de fallas SCADA-OMS-GIS en CENS",
        "respuestas": [
            (4, "Problema técnicamente pertinente y bien delimitado, y algo que casi nadie hace: "
                "**fijan sus propias metas antes de medir** —AUC > 0,75 y recall ≥ 70 % (p. 28)—, "
                "que es lo que hace falsable el trabajo. Baja de 5 porque la hipótesis 1 (la de "
                "ablación) no se contrasta en ninguna página, y porque la declaración de "
                "originalidad dice «Especialización en Analítica de Datos» (p. 16)."),
            (3, "El encuadre de dominio es correcto (SAIDI, SAIFI, ENS) y el trabajo demuestra "
                "entender el problema de fuga de información. Se queda en 3 porque CRISP-DM, que "
                "estructura el discurso de las diapositivas, **no aparece en el documento**, y "
                "porque no hay referente que respalde la matriz multicriterio con la que se elige "
                "el modelo."),
            (3, "Contiene la mejor decisión metodológica del cohorte en términos de aprendizaje "
                "automático: el **panel activo-semana** para construir la clase negativa (pp. 48, "
                "95) y la **exclusión explícita por fuga** de duración, usuarios, ENS, SAIDI y "
                "SAIFI (pp. 49, 96), con partición temporal 6.409.824 / 1.003.200. Lo que impide "
                "más de 3 es el material sobre el que corre: **todo el análisis usa un conjunto "
                "sintético** (pp. 12, 14, 112) mientras las pp. 45 y 52 hablan de «datos históricos "
                "reales» y «datos oficiales corporativos», y las diapositivas 7 y 10 declaran "
                "87.500 eventos históricos y 600.000 usuarios de CENS sin el matiz. Añádase el "
                "desbalance reportado como 18 % (p. 49) frente al 1,13 % que sale de los propios "
                "conteos, y los pesos de la matriz de 11 criterios sin publicar."),
            (3, "La comparación de modelos está bien ejecutada y las métricas se reportan sin "
                "maquillaje: ROC-AUC 0,594 / 0,605 / 0,616, PR-AUC máximo 0,053, recall máximo "
                "0,297, con SHAP sobre 5.000 registros. Pero **las metas propias de la p. 28 no se "
                "alcanzan y las conclusiones no las confrontan** (p. 97): un trabajo que se fija un "
                "umbral y luego no lo menciona pierde justo lo que había ganado. Los umbrales de "
                "decisión distintos por modelo (0,60 / 0,57 / 0,05) hacen precisión y F1 no "
                "comparables entre sí, y del prototipo Streamlit declarado tres veces (pp. 71, 112, "
                "diap. 13) no hay ni una captura entre las 16 figuras."),
            (4, "Analítica predictiva sobre la integración SCADA-OMS-GIS de una distribuidora "
                "eléctrica: el dominio es exigente y el aporte potencial es claro si se corre sobre "
                "datos reales. No llega a 5 porque sin acceso a los sistemas productivos el aporte "
                "se queda en el método, y porque la propia declaración de originalidad ubica el "
                "trabajo en otro programa (p. 16)."),
        ],
        "sube": "El **criterio 4 pasa a 4** si ellos mismos ponen sobre la mesa la distancia entre "
                "el AUC 0,616 y la meta de 0,75 y hacen una lectura técnica de por qué (pregunta "
                "prioritaria 2). El **criterio 3 pasa a 4** si explican cómo generaron el conjunto "
                "sintético y qué de lo que concluyen sigue en pie sabiendo que los patrones los "
                "pusieron ellos (pregunta 1) — mejor todavía si lo aclaran de entrada, sin que "
                "nadie lo pregunte.",
        "baja": "El **criterio 3 baja a 2** si sostienen en sala los 87.500 eventos históricos y "
                "los 600.000 usuarios de CENS como datos reales. El **criterio 4 baja a 2** si "
                "presentan el 0,616 como resultado satisfactorio o describen el tablero Streamlit "
                "sin poder decir si corre hoy (pregunta 3).",
    },
    "G-006": {
        "carpeta": "06 - G-006 - Sistema web de licitaciones Agroindustrial Palma",
        "respuestas": [
            (4, "Es el problema mejor cuantificado del cohorte: línea base **medida**, no estimada "
                "—50 % de error manual, ~32 h de consolidación y evaluación, ciclo de ~12,5 días "
                "(p. 100)— sobre un registro de observación de 16 actividades con tiempos "
                "(pp. 97-99). Baja de 5 por dos cosas de formulación: el título dice «inteligente» "
                "cuando el motor es una fórmula ponderada determinista y la IA queda como trabajo "
                "futuro (p. 242), y el capítulo de metodología está redactado en futuro."),
            (3, "El aparato de ingeniería está bien referenciado en su práctica —BPMN AS-IS (p. 167) "
                "y TO-BE (p. 178), reglas de negocio RN-01 a RN-12, decisión multicriterio con "
                "pesos declarados (pp. 143-144)—, pero para 249 páginas la base conceptual es "
                "delgada: 21 referencias, y **seis obras citadas no están en la lista**. Sobre todo, "
                "no hay referente que sustente el instrumento de madurez digital que el OE4 usa "
                "como vara."),
            (3, "Diseño mixto con **censo de los 6 funcionarios** —cuando la población son 6, el "
                "censo es la decisión correcta y está bien argumentada— y línea base medida con "
                "cronómetro. El reparo de fondo: el instrumento del OE4 no es el que se declaró. La "
                "p. 76 anuncia cinco dimensiones en escala 1-5 antes y después; lo que se reporta "
                "en las pp. 235-236 es la matriz ADKAR de adopción rebautizada «Índice de Madurez "
                "Digital», y **el 35 % de línea base no tiene instrumento, fecha ni encuestados**. "
                "Las pruebas de seguridad se anuncian (p. 68) y no se reportan (p. 228)."),
            (4, "Producto **en producción real on-premise desde el 1/6/2026 con 10 licitaciones "
                "tramitadas** (p. 181), con API REST documentada endpoint por endpoint (pp. 117-158) "
                "y ~50 capturas de prueba (Figs. 35-86); la Tabla 55 (p. 233) reporta 12,5 → 4,8 "
                "días (−61,6 %), 32 h → 0,5 h, error 50 % → 0 % y madurez 35 % → 88 %. Lo que "
                "impide el 5: las **32 horas están contadas dos veces** en esa misma tabla, el "
                "mismo resultado se reporta como +151,4 % y como 53 %, la mejora de madurez se mide "
                "con el instrumento equivocado y el acta de aceptación sigue «(pendiente)» (p. 73)."),
            (5, "Un sistema en producción en una empresa real, que sustituye un proceso de negocio "
                "completo y cuyo efecto operativo se puede discutir con cifras: es el caso más "
                "claro de transformación digital ejecutada de la jornada, junto con G-001."),
        ],
        "sube": "El **criterio 4 pasa a 5** si aclaran si las 32 horas son dos bloques distintos o "
                "el mismo contado dos veces (pregunta prioritaria 3) y si responden con qué "
                "instrumento, cuándo y a quiénes se midió el 35 % (pregunta 1) —o reconocen que ese "
                "35 % no tiene instrumento—. Preguntar en cuántas de las 10 licitaciones se "
                "adjudicó al proveedor sugerido (pregunta 2) puede subir el criterio 3 a 4: sería "
                "evidencia de uso, no de despliegue.",
        "baja": "El **criterio 4 baja a 3** si defienden el 35 % → 88 % como medición del "
                "instrumento de la p. 76. Cuidado con lo que se lee en voz alta: el documento va "
                "marcado «CONFIDENCIAL» y las capturas traen datos de proveedores y estados "
                "financieros.",
    },
    "G-007": {
        "carpeta": "07 - G-007 - Diagnostico de madurez digital en pymes",
        "respuestas": [
            (3, "El problema es pertinente y el diseño descriptivo-propositivo es adecuado al "
                "objeto. El reparo de fondo: el alcance de la p. 19 promete la **validación** del "
                "instrumento y esa validación no ocurre —el propio documento lo dice en la p. 38—, "
                "y el objetivo 3 queda autodeclarado «cumplido parcialmente» (p. 89). El "
                "planteamiento compromete más de lo que el trabajo se propone hacer."),
            (2, "El referente conceptual existe (niveles de madurez, Gartner) pero **no está "
                "articulado**: el documento maneja a la vez una escala 0-3 del instrumento, una 1-4 "
                "de clasificación, tres segmentos y los cinco niveles de Gartner, sin una "
                "correspondencia declarada entre ellas. Y el instrumento mide madurez mientras el "
                "trabajo concluye sobre competitividad, un constructo del que no se cita "
                "literatura ni se pregunta nada (p. 34)."),
            (3, "Es el trabajo con el marco muestral mejor definido del cohorte: **30 pymes del "
                "banco de elegibles «MiPymes Innovadoras»** (p. 33), nombradas con razón social "
                "(p. 44), en 10 localidades, con instrumento propio de 11 preguntas y puntuación "
                "0-3 sobre máximo 30 en cuatro niveles. Cuenta a favor que **declaren** que no hay "
                "alfa de Cronbach (p. 38) en vez de esconderlo. Lo que lo deja en 3: el índice de "
                "competitividad se reporta empresa por empresa (p. 83) **sin fórmula** y sin que el "
                "cuestionario pregunte por competitividad."),
            (2, "La sección de resultados no es interpretable tal como está impresa. El coeficiente "
                "de correlación aparece como **«001»** en cuatro sitios distintos, incluida la "
                "diapositiva 16 (pp. 53, 84, 89), los promedios como «003 / 4» y las brechas como "
                "«002»: son referencias de hoja de cálculo roscas, no cifras. Hay **dos "
                "clasificaciones incompatibles de las mismas 30 empresas** —12/10/8 (pp. 46, 48, 52, "
                "76, 78, 79) y 13/1/6/10 (p. 80)—, con la tabla de la p. 79 certificando «OK» "
                "inmediatamente antes de que la p. 80 la contradiga. Y hay **circularidad**: "
                "competitividad esperada, riesgo, ecosistema y prioridad se asignan desde el nivel "
                "de madurez (pp. 78, 85) y después la conclusión afirma la asociación entre madurez "
                "y competitividad (pp. 79, 90). Sostiene el 2, y no el 1, el diagnóstico crudo por "
                "dimensión, que sí es usable: promedio 2,54/4, índice ponderado 71 %, canales "
                "digitales 2,07 y automatización 2,40 (pp. 78-82)."),
            (4, "Diagnóstico de madurez digital en pymes es tema central de la especialización, con "
                "30 empresas reales y un instrumento propio: el aporte al ecosistema es real. No "
                "llega a 5 porque el prototipo (React + Node/Express + MySQL) no tiene URL ni "
                "repositorio y el objetivo 3 quedó parcial (p. 89)."),
        ],
        "sube": "El **criterio 4 pasa a 3** si dicen el coeficiente real, con qué prueba y sobre qué "
                "par de variables (pregunta prioritaria 1) **y** cuál de las dos distribuciones es "
                "la del modelo que entregan (pregunta 3). El **criterio 3 pasa a 4** si dan la "
                "fórmula del índice de competitividad y de qué ítems sale (pregunta 2).",
        "baja": "El **criterio 4 baja a 1** si presentan el «001» como si fuera un coeficiente, o si "
                "sostienen la asociación madurez-competitividad sin reconocer que la competitividad "
                "se derivó de la madurez. Antes de leer el título en público: el del cronograma trae "
                "tres erratas, el correcto es el de la portada (p. 1).",
    },
    "G-008": {
        "carpeta": "08 - G-008 - Modelo conceptual energia solar rural",
        "respuestas": [
            (3, "Lo mejor de este planteamiento es la honestidad del verbo: el objetivo dice "
                "**«proponer»** (p. 19) y el trabajo se queda dentro, sin inflar el alcance —algo "
                "que en este cohorte es la excepción—. El reparo de fondo está en la delimitación "
                "territorial: el título y el objetivo anclan el estudio al Valle del Cauca y "
                "**ninguna de las fuentes de la matriz tiene alcance Valle del Cauca** "
                "(pp. 43-48); los documentos de la Gobernación, la CVC y el DANE están en las "
                "referencias (p. 127) y no en el corpus, mientras la p. 77 afirma la "
                "contextualización regional. La delimitación es nominal."),
            (4, "Es su criterio más fuerte, y con razón: el trabajo **es** una síntesis documental, "
                "con corpus explícito de 35 fuentes codificadas D01-D35 (p. 40) y una matriz de "
                "caracterización que se puede auditar. Reparo que impide el 5: hay **cuatro "
                "duplicados** —IEA 2022 como D06 y D16, Verhoef como D07 y D19, Deloitte como D08 y "
                "D17, McKinsey como D09 y D18—, de modo que el corpus real es de **31 fuentes "
                "únicas**, que es justo lo que suma la Tabla 7 (p. 76) sin que nadie lo advierta; y "
                "el mazo dice 52 en la diapositiva 7 y 35 en la 8. Quedan además entradas sin año y "
                "un «(o documento oficial vigente)» sin editar."),
            (3, "El diseño documental es apropiado al verbo «proponer» y hay una precaución que "
                "conviene reconocer: la p. 42 declara que la codificación en Excel «no se utilizó "
                "como un procedimiento de análisis estadístico», lo que evita el abuso más común de "
                "este tipo de estudio. Lo que lo deja en 3: la muestra —que aquí es el corpus— se "
                "reporta con tres tamaños distintos (35 en el documento, 52 y 35 en el mazo, 31 "
                "reales) y la duplicación no se controló."),
            (3, "El producto es describible y coherente con lo prometido: modelo de cinco "
                "componentes, arquitectura de datos e IoT en seis etapas (Fig. 11, p. 110), siete "
                "riesgos con alternativas (Tabla 19) y ruta de aplicación (Fig. 12, p. 116). Dos "
                "cosas lo frenan. Primera, **las diapositivas inventan tres cifras —87 %, 81 % y "
                "76 %— que no existen en ninguna de las 129 páginas** (§5, punto 2), y la "
                "diapositiva 9 atribuye "
                "ODS 7/9/11 y reducción de costos que el documento nunca evalúa. Segunda, el techo "
                "está declarado y es real: **no hay juicio de expertos, ni piloto, ni validación** "
                "(p. 23), así que las conclusiones no pueden ir más allá de una propuesta —y no "
                "van—. Curiosamente, el producto bueno no está en el mazo."),
            (3, "El anclaje con la especialización pasa por la arquitectura de datos e IoT del "
                "modelo, que sí es transformación digital; el contenido energético es más sectorial "
                "que disciplinar, y la línea registrada es «Desarrollo de soluciones técnicas "
                "aplicadas». Sin validación de ningún tipo, el aporte potencial queda enunciado."),
        ],
        "sube": "El **criterio 4 pasa a 4** si exponen el modelo real —la arquitectura de seis "
                "etapas, los siete riesgos, la ruta de aplicación— en lugar de los tres porcentajes "
                "inventados, y si dicen de dónde salen esos porcentajes o los retiran (pregunta "
                "prioritaria 3). El **criterio 1 pasa a 4** si distinguen qué parte del modelo es "
                "específica del Valle del Cauca y qué parte sería idéntica en cualquier zona rural "
                "del país (pregunta 2).",
        "baja": "El **criterio 2 baja a 3** si sostienen las 52 fuentes o no pueden explicar la "
                "duplicación (pregunta 1). Aviso operativo antes de proyectar: el PDF del mazo tiene "
                "141 páginas porque desde la 13 trae pegado el documento completo — **hay que "
                "pararse en la diapositiva 12**.",
    },
    "G-009": {
        "carpeta": "09 - G-009 - Ecosistema digital RRHH con celulas agiles",
        "respuestas": [
            (3, "Techo declarado y techo alcanzado coinciden (pp. 22, 103-104), que es una virtud "
                "real. El reparo de fondo: las dos cifras que sostienen la magnitud del problema "
                "—«70 % manual» (p. 45) y «rotación superior al 30 %» (p. 24)— **no tienen fuente**, "
                "y son precisamente las que justifican el proyecto."),
            (2, "La lista de referencias no es la de este proyecto. Viene en **dos series "
                "alfabéticas** y contiene entradas sin relación con el objeto: IEEE 802.15.4, SPSS "
                "27 —que no se usa en ninguna parte—, Rioja 2008 sobre personas sordas, y "
                "producción agraria PGS. Con ese material no se puede acreditar pertinencia ni "
                "articulación de referentes, aunque el cuerpo del texto sí maneje los conceptos. "
                "**De dónde sale el reparo:** del documento. La dp. 21 proyecta sólo la primera "
                "serie —36 entradas, 21 sin año— y deja fuera la segunda, que es donde están esas "
                "cuatro entradas ajenas (§5, punto 9); en la sala este 2 no se ve."),
            (2, "El campo es el más grande del cohorte —**150 encuestas** de 22 ítems Likert en "
                "cuatro dimensiones y **25 entrevistas**, 175 participantes— y eso vale. Lo que "
                "impide más de 2 son tres cosas verificables: se declara **«muestreo estratificado "
                "probabilístico»** (pp. 45, 49) **sin marco, sin tamaño, sin confianza y sin error**, "
                "y los estratos declarados (nivel jerárquico y antigüedad) no son los reportados "
                "(área y antigüedad, pp. 99-101); los instrumentos se dicen validados por juicio de "
                "expertos (Anexo 5, pp. 125-126) **sin decir cuántos ni quiénes**; y en 126 páginas "
                "con 175 participantes hay **cero menciones** de consentimiento, confidencialidad, "
                "ética, anonimato o habeas data, ni carta de autorización de la empresa. **De "
                "dónde sale el reparo:** del documento, y el mazo no lo empeora ni lo arregla —la "
                "dp. 7 no repite la sobredeclaración del muestreo (§5, punto 12) y las 23 "
                "diapositivas tampoco mencionan la ética—."),
            (3, "Los resultados están cuantificados dimensión por dimensión (eficiencia 3,2/5, "
                "gestión documental 3,05, tiempos 3,07, acceso a la información 2,85, adecuación de "
                "herramientas 2,96; continuar con TD 4,13; ágiles 4,27; vinculaciones 52 % y "
                "gestión documental 36 %, p. 74), con matriz de priorización (pp. 75-76), AS IS "
                "(p. 79) / TO BE (p. 80) y **16 indicadores plenamente operacionalizados** "
                "(Tabla 14, pp. 93-97). Pero la columna «Línea base» de esos 16 indicadores dice "
                "«Diagnóstico inicial» en los 16 y **no hay un solo número en ninguna página**: un "
                "tablero de control sin líneas base no mide nada todavía. Y el OE2 se contradice: la "
                "p. 48 registra la conformación de cuatro células ágiles como actividad ya fechada "
                "en mayo-junio de 2026, mientras las pp. 87-88 y 104 hablan de «futura "
                "implementación»."),
            (4, "Ecosistema digital de recursos humanos con células ágiles sobre Power Apps y "
                "SharePoint (p. 81), con modelo de roles, sprint de dos semanas, backlog de siete "
                "historias y cuatro ceremonias (pp. 83-88): es transformación digital organizacional "
                "en el sentido pleno. No llega a 5 porque todo está en nivel de diseño y ningún "
                "indicador tiene punto de partida."),
        ],
        "sube": "El **criterio 4 pasa a 4** si dan un número —el valor de línea base de cualquiera "
                "de los dieciséis indicadores y de dónde sale (pregunta prioritaria 2)— y si aclaran "
                "si las cuatro células se conformaron con personas de la empresa o el OE2 cerró en "
                "diseño (pregunta 1). El **criterio 3 pasa a 3** si reconocen que el muestreo es no "
                "probabilístico por conveniencia y no lo defienden como estratificado "
                "probabilístico.",
        "baja": "El **criterio 3 baja a 1** si defienden el muestreo probabilístico sin poder dar "
                "marco ni error. **Turno de riesgo:** cierran la jornada del martes detrás de ocho "
                "grupos; si hay retraso acumulado, van solo las preguntas 1 y 2.",
    },
    "G-010": {
        "carpeta": "10 - G-010 - Plataforma preparacion concursos DIAN",
        "respuestas": [
            (2, "Es el planteamiento más desordenado de la jornada, y no por interpretación: el "
                "documento trae **dos juegos de objetivos específicos** —los de la p. 15 y los "
                "«Requisito 1-4» que estructuran las pp. 36-73—, sin decir cuál manda. La pregunta "
                "de investigación indaga por el **rendimiento** (p. 14) y la metodología anuncia "
                "medir rendimiento inicial y final (p. 28) sobre un diseño no experimental "
                "transeccional (p. 30) que no puede hacerlo. Y la población que valida son "
                "funcionarios de la DIAN, no los aspirantes que la p. 31 declara como participantes."),
            (3, "El marco normativo es lo mejor del documento y se sostiene con página: Decreto Ley "
                "714 de 2020 con el umbral de 65/100 (pp. 25-26), Decreto 1165 de 2019 (p. 37) y "
                "los manuales de funciones (pp. 46-49). No pasa de 3 porque el referente es "
                "normativo y no conceptual: no hay literatura sobre plataformas de preparación, "
                "usabilidad ni evaluación del aprendizaje, y lo que hay son enlaces bibliográficos "
                "(pp. 76-78)."),
            (2, "El diseño se declara (no experimental transeccional, muestreo por conveniencia, "
                "p. 30) pero no se puede reconstruir: **la sección de participantes no da tamaño de "
                "muestra** (pp. 31-32), el objetivo 4 habla de **10 personas** (p. 42) y los "
                "resultados de **100 funcionarios de la DIAN** (pp. 52, 59, 65), un resultado se "
                "presenta «según la simulación» (p. 43), no hay anexo del instrumento y no hay "
                "ninguna consideración ética para una encuesta a funcionarios públicos. Se queda en "
                "2 y no en 1 porque el diseño y la técnica sí están nombrados."),
            (2, "Los resultados son de aceptación —90 a 100 % de acuerdo con 0 % de desacuerdo en "
                "casi todos los ítems—, sin línea base con la que comparar, y **el indicador que "
                "ellos mismos fijaron, SUS superior a 68/100 (pp. 15-16, 28), no se aplica en "
                "ninguna página**. La conclusión sobre «accesibilidad total» (pp. 39, 43) contradice "
                "su propio reconocimiento de que no se cumple WCAG 2.1 (pp. 20-21). Lo que sostiene "
                "el 2 es que la sección de limitaciones es honesta y admite ese incumplimiento."),
            (3, "Una plataforma de preparación para concursos de méritos es una solución digital "
                "útil y con destinatario claro, pero el componente de transformación digital es "
                "moderado —no hay rediseño de proceso, ni arquitectura de datos, ni analítica— y no "
                "hay URL, repositorio ni QR que permita verificar el producto."),
        ],
        "sube": "El **criterio 1 pasa a 3** si dicen cuál de los dos juegos de objetivos manda y "
                "cuál de las dos arquitecturas construyeron (pregunta prioritaria 1). El **criterio "
                "3 pasa a 3** si aclaran cuántos usuarios probaron el prototipo, quiénes eran y "
                "cómo consiguieron el acceso (pregunta 2). El **criterio 4 pasa a 3** si reconocen "
                "que sin puntajes del mismo usuario en dos momentos la conclusión de la p. 74 no "
                "puede hablar de rendimiento (pregunta 3).",
        "baja": "El **criterio 4 baja a 1** si presentan los porcentajes de aceptación como medición "
                "de rendimiento o sostienen la «accesibilidad total». **No entregaron presentación**: "
                "si sustentan con diapositivas que los jurados no pudieron revisar, califico contra "
                "el documento y lo digo.",
    },
    "G-011": {
        "carpeta": "11 - G-011 - Intranet CDS para atencion al cliente",
        "sin_documento": True,
    },
    "G-012": {
        "carpeta": "12 - G-012 - Simulador presupuestal de pauta digital",
        "respuestas": [
            (4, "Título, pregunta (p. 15) y objetivo general (p. 16) dicen lo mismo y el verbo techo "
                "es **«diseñar»**: el trabajo no infla el alcance, lo supera —diseñó, desarrolló y "
                "evaluó internamente—. El problema parte de un diagnóstico sectorial con fuentes "
                "actuales (p. 14). No llega a 5 porque el objetivo 4 nombra la **eficiencia "
                "presupuestal** como indicador a analizar y ese indicador no aparece con valor en "
                "ninguna tabla de resultados (pp. 16, 19, 41, 45 frente a pp. 52-54)."),
            (3, "Tiene las fuentes más actuales del cohorte —Gartner 2022, IAB & PwC 2024, WARC "
                "2024 (p. 14)— y eso cuenta, igual que el marco referencial sí construido: "
                "racionalidad limitada de Simon (1997, p. 23), teoría de la decisión de Clemen & "
                "Reilly (2014, citada en pp. 11, 14, 17, 19, 21, 23 y 25) y simulación "
                "organizacional de Banks et al. (2015, pp. 22-24), los tres además proyectados en "
                "la diapositiva 6. Lo que lo deja en 3 es que **esa teoría de la decisión no se usa "
                "para elegir criterio**: en las 71 páginas no aparece ni una fuente de decisión "
                "bajo riesgo aplicada —media-varianza, VaR/CVaR, optimización robusta— ni las "
                "palabras «aversión al riesgo», «varianza» o «portafolio» (buscadas: cero "
                "resultados). De ahí sale el hueco conceptual del criterio 4: optimizar el promedio "
                "en un trabajo cuyo tema es la incertidumbre."),
            (4, "Es la formalización más sólida de la jornada: **12 ecuaciones con distribuciones, "
                "función objetivo y restricciones** (Tabla 7, p. 45), diccionario de datos con tipo, "
                "unidad, rango, fuente y regla de validación por variable (pp. 40-42), reglas de "
                "calidad de datos con su prueba correspondiente (pp. 43-44, 51-52), "
                "**reproducibilidad tratada como requisito** con semilla fija SEED = 42 (p. 44) y "
                "parámetros de cómputo justificados con pruebas de convergencia y de cobertura, no "
                "elegidos a dedo (Tablas 12-13, p. 55). La encuesta (50 aplicadas, 45 válidas, "
                "conveniencia, p. 32) está transcrita (Anexo 4, p. 65) y **amarrada a decisiones de "
                "diseño en una tabla de trazabilidad** (Tabla 6, p. 44). No llega a 5 porque tarifas, "
                "CTR y audiencias son «supuestos académicos de referencia» (nota, p. 45) y la "
                "agregación del alcance entre plataformas —con 88,77 % en una sola— no se declara."),
            (4, "Batería de 10 pruebas funcionales con evidencia numérica y mensajes de error "
                "(Tabla 8, pp. 51-52), tres escenarios (Tabla 9), comparación 40/30/30 frente al "
                "recomendado con +51,28 % (Tabla 10, p. 53), sensibilidad univariada y convergencia "
                "Monte Carlo. Y una **honestidad epistémica que hay que reconocer en sala**: la "
                "discusión declara que la validación es interna y no prueba superioridad en campañas "
                "reales (pp. 56-57), la conclusión 5 admite que la «reducción de incertidumbre» "
                "nunca se definió ni se midió (p. 58) y el Anexo 7 deja la matriz en blanco antes "
                "que atribuir resultados a usuarios que no probaron la herramienta (p. 71). Lo que "
                "impide el 5: la eficiencia presupuestal prometida no se reporta, y **la diapositiva "
                "17 afirma lo contrario de la conclusión 5 y de su propia diapositiva 5** —«supera "
                "los enfoques deterministas», «optimiza el retorno proyectado»—, con tres casos "
                "(12, 8 y 15 millones) que no existen en el documento y que las diapositivas 14-16 "
                "dejan sin resultado. La diapositiva 13 sí cierra hablando de «capacidad matemática "
                "del modelo», que es la mitad correcta del matiz."),
            (4, "Simulación Monte Carlo para asignar presupuesto de pauta en Meta, TikTok y YouTube, "
                "con prototipo ejecutable en Colab: encaja en «Mejoramiento de procesos "
                "organizacionales» y el aporte metodológico es transferible. No llega a 5 porque el "
                "notebook que la p. 70 dice entregar no está en la carpeta compartida con los "
                "jurados y el criterio de decisión no incorpora riesgo."),
        ],
        "sube": "El **criterio 2 pasa a 4** y el **criterio 4 a 5** con la misma respuesta: que "
                "expliquen el compromiso entre valor esperado y dispersión —el p10-p90 se abre de "
                "5.484-8.384 a 7.064-14.228 (p. 53)— y propongan un criterio que incorpore el "
                "riesgo **sin que nadie se lo sugiera** (pregunta prioritaria 1). El **criterio 3 "
                "pasa a 5** si reconocen la estructura del óptimo: por qué con CPC constante la "
                "recomendación se va siempre a la plataforma más barata hasta el piso del 5 % "
                "(pregunta 2).",
        "baja": "El **criterio 4 baja a 3** si sostienen en sala el discurso de la diapositiva 17 "
                "contradiciendo su propia conclusión 5, o si presentan el +51,28 % como evidencia "
                "de campañas reales. El **criterio 1 baja a 3** si atribuyen al optimizador un "
                "aprendizaje que no tiene. Son cuatro integrantes: pedir que responda quien no "
                "expuso.",
    },
    "G-013": {
        "carpeta": "13 - G-013 - Estrategia digital tesoreria cooperativas Bogota",
        "respuestas": [
            (3, "Título (p. 1), objetivo general (p. 16) y pregunta (p. 15) sí dicen lo mismo, y el "
                "verbo **«diseñar»** fija un techo honesto y alcanzable. El reparo de fondo es que "
                "el documento fija **tres alturas distintas para el mismo trabajo**: el objetivo "
                "específico 3 promete un prototipo funcional validado con pruebas e indicadores "
                "(p. 16), las limitaciones dicen que el alcance «no contempla la ejecución ni prueba "
                "directa de las herramientas» (p. 19) y la p. 37 que no hay implementación. A eso se "
                "suma que el título habla en plural sectorial —las cooperativas de Bogotá— sobre un "
                "estudio de caso único (pp. 31, 35)."),
            (2, "El referente de sector es correcto (regulación de la Supersolidaria, pp. 26-30) y "
                "el DMM de Gartner se presenta como marco aplicable (p. 23). Pero la lista de "
                "referencias (pp. 71-73) no sostiene el cuerpo: **ocho citas del texto no están en "
                "la lista** —Westerman et al. 2014, McKinsey 2020, Orozco & Mejía 2022, Gartner "
                "2018, BID 2022, Parviainen et al. 2017, ISO 2018, Van Horne & Wachowicz 2010—, "
                "tres «referencias» son notas y no referencias, Hernández/Sampieri 2014 se repite "
                "tres veces y la misma obra de Yin se cita como 2018 (p. 31) y como 2011 (p. 34)."),
            (2, "Hay trabajo de campo real y anexado —instrumento completo (pp. 74-76) y nueve "
                "páginas de encuestas diligenciadas a mano (pp. 77-85)—, lo que en este cohorte "
                "pesa. Pero el método declarado y el aplicado son distintos y no se puede "
                "reconstruir cuál rigió: se anuncian **seis participantes con entrevistas "
                "semiestructuradas** —dos directivos, tres de tesorería, uno de TI—, observación no "
                "participante y triangulación (pp. 33, 36, 38), y el capítulo de resultados es "
                "**100 % encuesta Likert con n = 10** (p. 45), sin una línea de entrevistas ni de "
                "observación. La caracterización tampoco cuadra con el anexo: la p. 45 dice "
                "antigüedad «entre 1 y 4 años», una categoría **que no existe en el instrumento** "
                "(p. 74), y en dos de las tres encuestas escaneadas lo marcado es «Menos de 1 año» "
                "(pp. 80, 83); las áreas manuscritas son Control Operativo, Contabilidad y Cartera "
                "—**ninguna es Tesorería**—."),
            (2, "El análisis del diagnóstico está hecho ítem por ítem y **la trazabilidad "
                "diagnóstico → diseño se puede rastrear**: el middleware por archivos existe porque "
                "el 100 % dijo que el Core no integra por API (p. 52 → p. 61), la interfaz "
                "«zero-training» porque el 50 % declaró brechas digitales (p. 59 → pp. 61-62). Lo "
                "que impide más de 2: del **objetivo 3 no hay resultado** —solo un panel semáforo "
                "con 94,2 %, 12 casos y 0 riesgos (p. 62) sin decir sobre cuántos registros ni qué "
                "archivo, y la p. 64 admite que solo se «reprodujo el comportamiento esperado»—; "
                "las **conclusiones (pp. 69-70) no cierran ni el prototipo, ni las pruebas, ni la "
                "evaluación de usuarios**, y no hay sección de limitaciones al final; la "
                "diapositiva 13 afirma un 40 % de madurez nivel IV del DMM que no está en ninguna "
                "de las 85 páginas; y la diapositiva 16 titula «resultados esperados» una "
                "proyección de McKinsey (p. 15)."),
            (4, "Tesorería cooperativa con middleware de conciliación no invasivo, arquitectura de "
                "datos por capas, modelo lógico de siete entidades, ETL, seguridad y trazabilidad "
                "(pp. 63-64): encaja de lleno en «Transformación Digital e Innovación "
                "Organizacional», y la solución al Core sin API por archivos estructurados con SFTP "
                "es una decisión defendible en una cooperativa real (pp. 65-66). Suma que reconozca "
                "el límite de gobierno —la validación normativa corresponde a jurídica, riesgos y "
                "cumplimiento (p. 61)—. No llega a 5 porque el producto no pasó de la maqueta."),
        ],
        "sube": "El **criterio 4 pasa a 3** si muestra el prototipo procesando un archivo con número "
                "de registros declarado, o si dice con franqueza que el panel es una maqueta y el "
                "94,2 % es ilustrativo (pregunta prioritaria 1) — reconocerlo sube, no baja. El "
                "**criterio 3 pasa a 3** si ordena el dato de la muestra: cuántas encuestas, a qué "
                "áreas y qué pasó con las entrevistas (pregunta 2). El **criterio 1 pasa a 4** si "
                "acota honestamente el alcance a la cooperativa estudiada y nombra la condición que "
                "hace transferible el MACM (pregunta 3).",
        "baja": "El **criterio 4 baja a 1** si presenta el 94,2 % o el 25 % de McKinsey como "
                "medición de su prototipo. El **criterio 1 baja a 2** si sostiene que implementó, "
                "capacitó y midió indicadores en la cooperativa sin poder mostrar nada. Es trabajo "
                "individual y cierra la jornada: todo el dominio y toda la defensa recaen en una "
                "persona, y eso se reconoce a favor.",
    },
}

BLOQUE_SIN_DOCUMENTO = """### 3.1 No hay base documental para responderlo

**Los cinco criterios de este formulario se responden con el documento, y este grupo no entregó
ninguno.** La carpeta `G:\\.shortcut-targets-by-id\\1q8TC3kuLuOFTwhnhMPdy0nW1IagfN-af\\26ET2-G-011`
existe desde el 05/08/2026 y contiene **cero archivos** (verificado el 15/08/2026 a las 07:21; las
carpetas de los otros doce grupos resuelven bien, así que no es un fallo de sincronización local).
No hay trabajo de grado ni presentación.

Con eso, cuatro de los cinco criterios **no son puntuables desde el documento** por definición: el 2
pregunta por «pertinencia y actualidad de las fuentes consultadas» y no hay fuentes que consultar; el
4 pregunta por «consistencia de las conclusiones» y no hay conclusiones escritas. **No se inventa un
número.** Lo único citable antes de la sala es el cronograma —hoja `MARIA-ESPTD`, fila 46, cols.
B-K—, donde el objetivo general (col. I) cubre recepción → higienización → transformación →
visualización de bases de datos de clientes para **validación de pólizas**, mientras el título
(col. G) promete optimizar la **atención al cliente**: dos niveles distintos.

**Antes del miércoles hay que preguntarle a la Dirección** si el documento se radicó en CUN Digital
o con el metodólogo y solo no llegó a la carpeta de jurados (§3 B2 del índice). Y hay un dato que
puede explicarlo todo: el correo del cronograma es `flor.hernandezg@`**`con`**`.edu.co`, con dominio
`con` en lugar de `cun`, así que **es posible que las citaciones nunca hayan llegado** (§3 B3).

### 3.2 Qué marcar si el formulario exige un valor, según lo que se escuche

El formulario es de opción obligatoria, así que en sala habrá que marcar algo. Estas son las dos
únicas lecturas que puedo sostener, y **ningún criterio pasa de 3 sin documento**, porque por encima
de 3 la escala afirma calidad verificable y aquí no hay nada que verificar:

| # | Criterio | Si expone con orden y cierra sus objetivos | Si la exposición no cierra los objetivos |
|:-:|---|:-:|:-:|
| 1 | Planteamiento de la problemática y formulación de objetivos | **3** | **2** |
| 2 | Marco teórico y referentes conceptuales | **2** | **1** |
| 3 | Metodología, muestra y coherencia del diseño | **2** | **1** |
| 4 | Resultados y conclusiones | **2** | **1** |
| 5 | Pertinencia disciplinar y articulación con la especialización | **3** | **2** |
| | **Suma** | **12 / 25** | **7 / 25** |

**En los dos escenarios, dejar escrito en el formulario y en el acta:** «respondido únicamente sobre
la exposición oral; el grupo no entregó trabajo de grado ni presentación a la carpeta de jurados
(verificado el 15/08/2026)». Sin esa constancia, un 2 parece un juicio sobre el trabajo cuando es la
consecuencia de que no haya trabajo que leer.

**Las tres preguntas de la §6 de la ficha no presuponen documento** —estado de la intranet, indicador
antes/después, autorización para tratar datos de clientes—, así que sirven igual. **El paradero del
documento se habla con el director, no en sala.**
"""


def bloque(codigo: str, datos: dict) -> str:
    """El texto de la §3 para un grupo."""
    partes = [CABECERA]

    if datos.get("sin_documento"):
        partes.append("\n" + BLOQUE_SIN_DOCUMENTO)
        return "".join(partes)

    if datos.get("nota_cita"):
        partes.append("\n> 📄 " + datos["nota_cita"] + "\n")

    respuestas = datos["respuestas"]
    suma = sum(v for v, _ in respuestas)

    partes.append("\n| # | Criterio | Respuesta | Qué la sostiene (página del documento) |\n")
    partes.append("|:-:|---|:-:|---|\n")
    for i, (valor, sustento) in enumerate(respuestas, start=1):
        partes.append(f"| {i} | {CRITERIOS[i - 1]} | **{valor}** | {sustento} |\n")
    partes.append(f"| | **Suma** | **{suma} / 25** | |\n")

    partes.append(f"\n**Qué subiría una casilla en sala:** {datos['sube']}\n")
    partes.append(f"\n**Qué la bajaría:** {datos['baja']}\n")
    return "".join(partes)


def renumerar(texto: str) -> str:
    """§3→§4, §4→§5, §5→§6 en los encabezados de nivel 2, de atrás hacia adelante."""
    for viejo, nuevo in ((5, 6), (4, 5), (3, 4)):
        texto = re.sub(rf"^## {viejo}\. ", f"## {nuevo}. ", texto, flags=re.MULTILINE)
    return texto


ANCLA_NUEVA = "## 3. Formulario oficial del jurado"
ANCLA_VIEJA = "## 3. Retroalimentación"
ANCLA_RENUMERADA = "## 4. Retroalimentación"


def procesar_evaluacion(ruta: str, codigo: str, datos: dict, simular: bool) -> str:
    with open(ruta, encoding="utf-8") as fh:
        original = fh.read()

    nuevo_bloque = bloque(codigo, datos)

    if ANCLA_NUEVA in original:
        # Idempotencia: reemplazar la sección ya existente, sin volver a renumerar.
        ini = original.index(ANCLA_NUEVA)
        fin = original.index(ANCLA_RENUMERADA, ini)
        salida = original[:ini] + nuevo_bloque + "\n" + original[fin:]
        accion = "reemplazada"
    elif ANCLA_VIEJA in original:
        cuerpo = renumerar(original)
        ini = cuerpo.index(ANCLA_RENUMERADA)
        salida = cuerpo[:ini] + nuevo_bloque + "\n" + cuerpo[ini:]
        accion = "insertada"
    else:
        return f"  ⛔ {codigo}: no encontré «{ANCLA_VIEJA}» ni «{ANCLA_NUEVA}» — sin tocar"

    if salida == original:
        return f"  = {codigo}: sin cambios"
    if not simular:
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write(salida)
    delta = len(salida.splitlines()) - len(original.splitlines())
    return f"  ✓ {codigo}: §3 {accion} ({delta:+d} líneas)"


# ---------------------------------------------------------------------------
# La matriz consolidada del índice
# ---------------------------------------------------------------------------

ANCLA_INDICE = "### 2.1 El formulario oficial del jurado"
CORTE_INDICE = "\n---\n\n## 3. BANDERAS ADMINISTRATIVAS"

ORDEN = ["G-001", "G-002", "G-003", "G-004", "G-005", "G-006", "G-007",
         "G-008", "G-009", "G-010", "G-011", "G-012", "G-013"]

CORTO = {
    "G-001": "TuFinca: módulo pecuario y chatbot",
    "G-002": "PWA turística de Rivera (Huila)",
    "G-003": "Archivo municipal de San Francisco",
    "G-004": "Gestión del cambio en seguridad electrónica",
    "G-005": "Predicción de fallas SCADA-OMS-GIS",
    "G-006": "Sistema web de licitaciones",
    "G-007": "Diagnóstico de madurez digital en pymes",
    "G-008": "Modelo conceptual de energía solar rural",
    "G-009": "Ecosistema digital de RR. HH.",
    "G-010": "Plataforma para concursos DIAN",
    "G-011": "Intranet CDS",
    "G-012": "Simulador de pauta digital",
    "G-013": "Tesorería de cooperativas de Bogotá",
}

# La razón de una línea por grupo: lo que decide la casilla más baja.
DECIDE = {
    "G-001": "El único con los cuatro objetivos cerrados y conteos crudos verificables (p. 213); "
             "frena el motor conversacional sin tecnología nombrada (p. 171)",
    "G-002": "Producto público y verificado (p. 74) sobre 10 referencias, ninguna posterior a 2021 "
             "y ninguna sobre PWA (p. 86)",
    "G-003": "La Tabla 14 (pp. 104-105) es lo más honesto del cohorte; la muestra no se cuantifica "
             "en 169 páginas y la bibliografía llega con «[por verificar]»",
    "G-004": "Alfa de Cronbach 0,924 (pp. 75-77) y dos modelos OLS incompatibles sobre el mismo "
             "objetivo (p. 98 frente a pp. 101-102)",
    "G-005": "Panel activo-semana y exclusión por fuga bien hechos (pp. 48-49); las metas propias "
             "de la p. 28 no se alcanzan ni se confrontan",
    "G-006": "En producción desde el 1/6/2026 con 10 licitaciones (p. 181); la madurez se midió con "
             "ADKAR y no con el instrumento declarado (pp. 76, 235)",
    "G-007": "Marco muestral real de 30 pymes nombradas (pp. 33, 44); el coeficiente se imprime "
             "como «001» y hay dos clasificaciones incompatibles (pp. 79-80)",
    "G-008": "El corpus documental es su fortaleza (D01-D35, p. 40) con 4 duplicados; el mazo "
             "inventa 87 %, 81 % y 76 %, que no están en 129 páginas",
    "G-009": "175 participantes reales; muestreo «probabilístico» sin marco ni error (p. 45) y cero "
             "menciones de ética en 126 páginas",
    "G-010": "Marco normativo sólido (pp. 25-26, 37); dos juegos de objetivos, dos arquitecturas y "
             "10 frente a 100 participantes",
    "G-011": "**Sin documento**: cuatro de los cinco criterios no son puntuables. Ver §3 de su "
             "`4 - Evaluacion.md`",
    "G-012": "12 ecuaciones, semilla fija y trazabilidad encuesta → diseño (pp. 44-45); optimiza el "
             "promedio en un trabajo sobre incertidumbre (p. 53)",
    "G-013": "Encuestas diligenciadas anexadas (pp. 77-85); el método declarado no es el aplicado y "
             "el objetivo 3 no tiene resultado",
}


def bloque_indice() -> str:
    filas = []
    for i, cod in enumerate(ORDEN, start=1):
        d = DATOS[cod]
        if d.get("sin_documento"):
            celdas = ["—"] * 5
            suma = "**n/a**"
        else:
            celdas = [f"**{v}**" for v, _ in d["respuestas"]]
            suma = f"**{sum(v for v, _ in d['respuestas'])}**"
        filas.append(
            f"| {i} | **{cod}** | {CORTO[cod]} | " + " | ".join(celdas)
            + f" | {suma} | {DECIDE[cod]} |"
        )

    puntuados = [d for c, d in DATOS.items() if not d.get("sin_documento")]
    medias = []
    for j in range(5):
        vals = [d["respuestas"][j][0] for d in puntuados]
        # Coma decimal, como el resto del documento.
        medias.append("**" + f"{sum(vals) / len(vals):.1f}".replace(".", ",") + "**")

    return f"""{ANCLA_INDICE} — las 5 respuestas, grupo por grupo

> **Es otro instrumento, no la rúbrica del ACA 3.** La Dirección pide al jurado cinco preguntas con
> opciones **1 2 3 4 5**, y **ninguna de las cinco califica la sustentación oral**: las cinco se
> responden con el documento. Por eso están precargadas. Esta tabla es solo la vista de conjunto;
> el formulario de cada grupo vive en tres sitios, y los tres salen del mismo dato:
> **§8.1 de `1 - Ficha de preparacion`** para leer antes de entrar (casilla + página que la sostiene
> + qué la subiría o bajaría), **§E de `2 - Hoja de respuestas`** para rodear en sala, y
> **§3 de `4 - Evaluacion.md`** para el sustento completo al cerrar.
>
> ⚠️ **Este 1–5 no es la nota 0,1–5,0 del acta** (75 % metodólogo + 25 % jurados; meritoria ≥ 4,6 sin
> ninguna individual por debajo de 4,5). Es un ordinal de calidad **documental**: **5** sobresaliente ·
> **4** sólido con reparos menores · **3** aceptable con un reparo de fondo · **2** deficiente: hay
> material pero se contradice · **1** sin base verificable. La suma sobre 25 **no se convierte** a la
> escala del acta; sirve para ordenar, no para calificar.

| # | Grupo | Título corto | 1 · Problema y objetivos | 2 · Marco teórico | 3 · Metodología y muestra | 4 · Resultados | 5 · Pertinencia | Σ/25 | Lo que decide la casilla más baja |
|:-:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
{chr(10).join(filas)}
| | | **Promedio de los 12 puntuados** | {" | ".join(medias)} | | |

**Lo que se lee en la columna, no en la fila:**
- **El criterio 2 (marco teórico) es el más bajo de la jornada** y es un asunto del programa, no de
  un grupo: bibliografías con marcadores «[por verificar]» (G-003, pp. 138-140), listas en dos series
  con entradas ajenas al proyecto (G-009), entre seis y diez citas del cuerpo ausentes de la lista
  (G-001, G-004, G-006, G-013) y un producto sin literatura sobre su propia tecnología (G-002, 10
  referencias, ninguna sobre PWA). Va al correo a la Dirección, no a la sala.
- **El criterio 5 (pertinencia disciplinar) es el más alto**: los trece temas encajan en la
  especialización. Nadie está fuera de campo; lo que falla es cómo se sostiene lo que se afirma.
- **El criterio 4 (resultados) es el que más se mueve en sala**, porque siete de los trece tienen el
  cuarto objetivo parcial o sin ejecutar. Ahí está casi siempre la mejor pregunta.
- **Ojo con leer la suma como un ranking de mérito.** No incluye dominio del tema ni capacidad de
  defensa, que son la mitad de lo que se juega el martes: G-005 puntúa alto aquí por lo cuidadoso de
  su diseño y su §8 anticipa 4,0-4,4, mientras G-004 puntúa bajo con una §8 de 4,0-4,5. **La nota del
  acta sale de la §8 de cada ficha, no de esta tabla.**
"""


def procesar_indice(simular: bool) -> str:
    with open(INDICE, encoding="utf-8") as fh:
        original = fh.read()

    nuevo = bloque_indice()

    if ANCLA_INDICE in original:
        ini = original.index(ANCLA_INDICE)
        fin = original.index(CORTE_INDICE, ini)
        salida = original[:ini] + nuevo + original[fin:]
        accion = "reemplazada"
    elif CORTE_INDICE in original:
        ini = original.index(CORTE_INDICE)
        salida = original[:ini] + "\n" + nuevo + original[ini:]
        accion = "insertada"
    else:
        return "  ⛔ índice: no encontré el corte de «## 3. BANDERAS ADMINISTRATIVAS» — sin tocar"

    if salida == original:
        return "  = índice: sin cambios"
    if not simular:
        with open(INDICE, "w", encoding="utf-8") as fh:
            fh.write(salida)
    delta = len(salida.splitlines()) - len(original.splitlines())
    return f"  ✓ índice: §2.1 {accion} ({delta:+d} líneas)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--simular", action="store_true", help="muestra el plan y no escribe nada")
    g.add_argument("--confirmar", action="store_true", help="escribe los archivos")
    args = ap.parse_args()
    simular = not args.confirmar

    print("FORMULARIO OFICIAL DEL JURADO — 5 criterios, escala 1-5")
    print(f"{'SIMULACIÓN (no escribe nada)' if simular else 'ESCRIBIENDO'}\n")

    if not os.path.isdir(FICHAS):
        raise SystemExit(f"no encontré la carpeta de fichas: {FICHAS}")

    for cod in ORDEN:
        datos = DATOS[cod]
        ruta = os.path.join(FICHAS, datos["carpeta"], "4 - Evaluacion.md")
        if not os.path.isfile(ruta):
            print(f"  ⛔ {cod}: no existe {ruta}")
            continue
        print(procesar_evaluacion(ruta, cod, datos, simular))

    print()
    print(procesar_indice(simular))

    if simular:
        print("\nNada escrito. Repetir con --confirmar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
