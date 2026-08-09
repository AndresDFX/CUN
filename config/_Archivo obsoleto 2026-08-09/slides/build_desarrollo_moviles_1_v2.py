# -*- coding: utf-8 -*-
"""
Genera los 10 decks .pptx del curso DESARROLLO DE APLICACIONES MÓVILES 1 · v2
(REFACTOR — Jetpack Compose, asume Kotlin ya visto): presentación del curso + 9 sesiones.
Identidad Nueva América (motor fesna_slides_engine).

Contenido NUEVO (Compose): S1 intro+primer composable · S2 UI declarativa · S3 layouts ·
S4 estado/interacción · S5 listas · S6 formularios · S7 navegación · S8 temas/Material · S9 datos+proyecto.

Reglas aplicadas:
- Las diapositivas de sesión NO incluyen "Recordemos la asignatura" ni "¿Cómo trabajaremos hoy?".
- Sin porcentajes de nota en las sesiones (la evaluación va SOLO en la presentación del curso).
- Todas las clases duran lo mismo (105 min).
- Evaluación REAL del curso: Progreso Coursera 90% + Asistencia 10% + bono Kahoot (NO el 50/40/10).
- Entorno práctico = Compose Multiplatform para Web (Kotlin/Wasm): la UI Compose real se ve EN EL NAVEGADOR
  (Kotlin Playground con entorno Compose para los ejemplos · plantilla en Codespaces/Gitpod solo para el proyecto final), gratis y sin instalar.
  Demo del docente: Google AI Studio (app Android con emulador web). NO Firebase Studio.
- examlab = evaluación: Test + Reto en vivo (Kahoot) por sesión + Taller/Proyecto (entregable: enlace del preview / repo).
  examlab NO ejecuta Kotlin/Compose (quizzes de código = lectura de un composable).
- Diapositivas mixtas: 2-3 por sesión llevan un diagrama de concepto (config/slides/diagramas.py, prefijo cmp_).

Config del curso: config/cursos/desarrollo-aplicaciones-moviles-1.json (v2.0)
Salida: Cursos/Desarrollo de Aplicaciones Moviles 1/Clases/Version vigente (nuevo dictado 2026)/
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fesna_slides_engine import *

# --- Diapositivas MIXTAS: mapa (substring ÚNICO del título → id del diagrama del catálogo) ---
DIAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "diagramas")
IMG = [
    # S1
    ("Kotlin + Jetpack Compose", "cmp_pila_movil"),
    ("¿Qué es un @Composable", "cmp_composable_funcion"),
    ("laboratorio en el navegador", "cmp_flujo_web"),
    # S2
    ("Declarativo vs imperativo", "cmp_declarativo"),
    ("Composables básicos", "cmp_composables_basicos"),
    ("Modifier: el", "cmp_modifier_cadena"),
    # S3
    ("Column, Row y Box", "cmp_column_row_box"),
    ("Anidar layouts", "cmp_arbol_composables"),
    ("Diseño responsivo", "cmp_weight"),
    # S4
    ("estado y la recomposición", "cmp_recomposicion"),
    ("remember + mutableStateOf", "cmp_remember_state"),
    ("State hoisting", "cmp_state_hoisting"),
    # S5
    ("Column vs LazyColumn", "cmp_column_vs_lazy"),
    ("Del dato a la tarjeta", "cmp_lista_flujo"),
    # S6
    ("campo controlado", "cmp_textfield_controlado"),
    ("Validación: requerido", "cmp_validacion_flujo"),
    # S7
    ("NavController y NavHost", "cmp_nav_grafo"),
    ("Navegar: navigate", "cmp_backstack"),
    # S8
    ("MaterialTheme: colorScheme", "cmp_materialtheme"),
    ("Tema claro y oscuro", "cmp_claro_oscuro"),
    # S9
    ("Consumir datos: suspend", "cmp_suspend_api"),
    ("estados de la UI", "cmp_estados_ui"),
    ("Integrar todo el curso", "cmp_arquitectura"),
    # --- MOCKUPS tipo imagen (teléfono/UI, código→preview, paleta): en slides de EJEMPLO ---
    ("Tu primer 'Hola'", "cmp_s1_primera_app"),
    ("Ejemplo: una tarjeta de perfil", "cmp_s2_ui_mock"),
    ("Ejemplo: un contador", "cmp_s4_contador_mock"),
    ("Ejemplo: lista de productos", "cmp_s5_lista_mock"),
    ("Mensajes de error e isError", "cmp_s6_form_mock"),
    ("Usar el tema en tus composables", "cmp_s8_paleta"),
    ("El Proyecto Integrador", "cmp_s9_app_final_mock"),
]

def img_for(title):
    tl = (title or "").lower()
    for sub, did in IMG:
        if sub.lower() in tl:
            p = os.path.join(DIAG_DIR, did + ".png")
            return p if os.path.exists(p) else None
    return None

BASE = r"g:\Mi unidad\Trabajos\Empleo\FESNA\Cursos\Desarrollo de Aplicaciones Moviles 1\Clases\Version vigente (nuevo dictado 2026)"
CURSO = "Desarrollo de Aplicaciones Móviles 1"
CURSO_CORTO = "Desarrollo de Aplicaciones Móviles 1"
PROGRAMA = "Ingeniería de Sistemas"

TUTOR = ("Julian Andrés Castaño Espinosa",
         ["Líder Técnico", "Ingeniero de Sistemas", "Candidato a MsC en IA"],
         "julian.castano@lanuevaamerica.edu.co")

OBJETIVOS_CURSO = [
    "Componer interfaces de usuario con Jetpack Compose (composables, Modifier y layouts) y previsualizarlas ejecutándolas en el navegador con Compose para Web.",
    "Gestionar estado e interacción, mostrar listas de datos y capturar entrada del usuario con formularios validados.",
    "Navegar entre pantallas, aplicar temas de Material Design e integrar datos en una app móvil final funcional.",
]

# --- Evaluación REAL del curso (config): Coursera 90% + Asistencia 10% ---
EVAL_ROWS = [
    ["**Progreso del curso en Coursera**", "@@90%@@"],
    ["**Asistencia** — al final de la sesión", "@@10%@@"],
    ["**Total**", "**100%**"],
]
EVAL_NOTE = ("Participación en clase **+0.3** (opcional)  ·  "
             "Kahoot / Reto en vivo: 🥇 **+0.5** · 🥈 **+0.4** · 🥉 **+0.3** (opcional)")

NIVELES = {
    1: "Nivel 1 — Componer interfaces con Compose",
    2: "Nivel 2 — Estado, listas y formularios",
    3: "Nivel 3 — Navegación, temas y datos",
}


def std_proposito(prs, foco, nivel):
    items = ["**El propósito de la tutoría de hoy es:**", (foco, 1), "Niveles de logro de la asignatura:"]
    for n in (1, 2, 3):
        txt = NIVELES[n]
        items.append((f"@@{txt}  ←  hoy@@" if n == nivel else txt, 1))
    content_slide(prs, "El propósito de hoy", items, size=16, idx=2)

def std_autonomo(prs, items, idx):
    content_slide(prs, "Trabajo autónomo (15 min)", items, size=15, idx=idx)

def std_logros(prs, items, idx):
    content_slide(prs, "¿Qué logramos hoy?", items + [
        "Chequea tu saber con el **Test** y el **Reto en vivo (Kahoot)** de la sesión en **examlab**; la UI se construye en **Compose para Web**.",
    ], size=15, idx=idx)


# ============================== SESIONES ==============================
SESIONES = {
 1: dict(
    titulo="Introducción al desarrollo móvil y tu primera app",
    subtitulo="De programar Kotlin a construir apps con Compose (en el navegador)",
    archivo="Sesion 1 - Introduccion al desarrollo movil y tu primera app",
    nivel=1, gancho="¡Tu primera app en el navegador!",
    foco="Comprender el panorama del desarrollo móvil con Kotlin y Jetpack Compose y escribir tu primer @Composable, viéndolo en el navegador con Compose para Web.",
    contenido=[
        ("bullets", "El desarrollo de aplicaciones móviles hoy", [
            "Una **app móvil** es un programa que corre en un teléfono o tablet (Android, iOS).",
            "**Android** domina el mercado y su lenguaje oficial es @@Kotlin@@ (que ya viste en el complementario).",
            "La interfaz moderna de Android se construye con @@Jetpack Compose@@ (kit oficial de Google desde 2021).",
            "En este curso pasas de 'programar Kotlin' a **construir apps con interfaz de verdad**.",
        ]),
        ("bullets", "Kotlin + Jetpack Compose: el equipo", [
            "**Kotlin** = el lenguaje;  **Compose** = el kit para dibujar la interfaz.",
            "Compose reemplazó al viejo sistema de XML + Views (más simple y potente).",
            "Con Compose describes la UI con @@funciones de Kotlin@@.",
            "El mismo Compose funciona en Android, iOS, escritorio y web.",
        ]),
        ("bullets", "¿Qué es un @Composable?", [
            "Un @@@Composable@@ es una función normal marcada con la anotación @Composable.",
            "En vez de devolver un dato, **emite interfaz** (Text, Button, Image…).",
            "Se combinan como piezas de Lego para armar la pantalla.",
            "Su nombre va en **Mayúscula** por convención:  fun Saludo().",
        ]),
        ("tabla", "Anatomía de un proyecto de app", ["Parte", "Qué es y para qué sirve"], [
            ["MainActivity / punto de entrada", "Donde arranca la app"],
            ["setContent { }", "Aquí 'cuelgas' tu interfaz Compose"],
            ["Funciones @Composable", "Describen cada pantalla o pieza de UI"],
            ["@Preview", "Ver la UI sin ejecutar toda la app"],
            ["Recursos (strings, colores)", "Textos, colores e imágenes centralizados"],
        ], dict(col_w=[4.6, 7.4], note="La UI vive en las funciones @Composable; el resto es el 'andamiaje' del proyecto.")),
        ("bullets", "Tu primer 'Hola' en Compose", [
            "@Composable fun Saludo() { Text(\"Hola, Compose\") }.",
            "**Text(...)** es el composable más básico: muestra texto en pantalla.",
            "@Preview fun VistaPrevia() { Saludo() } permite verlo @@sin teléfono@@.",
            "Cambias el texto y la vista previa se actualiza al instante.",
        ]),
        ("bullets", "Tu laboratorio: Kotlin Playground (modo Compose)", [
            "Practicarás en @@Kotlin Playground@@ (play.kotlinlang.org), entorno **Compose** — gratis, sin instalar.",
            "Es el **mismo Compose de Android**, compilado a WebAssembly y visible en el navegador.",
            "Cada ejemplo es una **mini-app completa**: la **pegas**, pulsas **Run** y **ves la UI** — un fragmento a la vez.",
            "Solo el **proyecto final** usa una **plantilla** en GitHub Codespaces / Gitpod.",
        ]),
        ("tabla", "Herramientas del curso", ["Para qué", "Herramienta"], [
            ["Escribir UI Compose y verla", "Kotlin Playground — entorno Compose (play.kotlinlang.org)"],
            ["Ver una app Android 'de verdad'", "Google AI Studio (emulador web · demo del docente)"],
            ["Evaluación (Test, Reto, entrega)", "examlab — https://examlab.lovable.app/app"],
            ["En el trabajo (referencia)", "Android Studio (IDE profesional, local)"],
        ], dict(col_w=[4.4, 7.6], note="Todo se hace en el navegador, gratis y sin instalar nada.")),
        ("bullets", "El plan del curso (9 sesiones)", [
            "**Nivel 1**: componer la UI (composables, Modifier, layouts).",
            "**Nivel 2**: estado e interacción, listas y formularios.",
            "**Nivel 3**: navegación, temas Material y datos.",
            "Al final construyes una @@app de varias pantallas@@ funcional.",
        ]),
    ],
    autonomo=[
        "Abre **Kotlin Playground** (play.kotlinlang.org) y selecciona arriba a la derecha el entorno **Compose**.",
        "Escribe un @Composable llamado Saludo() que muestre  Text(\"Hola, soy [tu nombre]\").",
        "Añade @Preview y ejecuta para ver tu texto **en el navegador**.",
        ("Captura la vista previa (la pestaña del navegador con tu UI).", 1),
        "Entregable en **examlab**: pega tu código (o el enlace del preview) + la captura en la entrega de la sesión.",
    ],
    logros=[
        "Entendemos qué es una **app móvil** y el rol de **Kotlin + Compose**.",
        "Sabemos qué es un **@Composable** (una función que describe UI).",
        "Escribimos y previsualizamos nuestro **primer Text()**.",
        "Conocemos el entorno: **Kotlin Playground (modo Compose)** en el navegador.",
    ],
    cierre=("¡Nos vemos en la Sesión 2!",
            ["Próxima sesión: **UI declarativa — Text, Button, Image y Modifier**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya dibujas tu primer texto… ¡ahora construye interfaces completas!"),
 ),

 2: dict(
    titulo="UI declarativa con Jetpack Compose",
    subtitulo="Describir la interfaz como funciones",
    archivo="Sesion 2 - UI declarativa con Jetpack Compose",
    nivel=1, gancho="¡Describe la interfaz, no la dibujes!",
    foco="Construir y estilizar la interfaz con los composables básicos (Text, Button, Image, Spacer) y Modifier, entendiendo el enfoque declarativo y usando @Preview.",
    contenido=[
        ("bullets", "Declarativo vs imperativo: describir la interfaz", [
            "En el enfoque **imperativo** dices paso a paso cómo cambiar cada elemento.",
            "En Compose (**declarativo**) @@describes cómo se ve@@ la UI según el estado.",
            "Cuando el dato cambia, Compose @@redibuja solo@@ lo necesario (recomposición).",
            "Menos código, menos errores y una UI más fácil de razonar.",
        ]),
        ("bullets", "Composables básicos", [
            "@@Text@@: muestra texto  —  Text(\"Hola\").",
            "@@Button@@: botón con acción  —  Button(onClick = { }) { Text(\"OK\") }.",
            "@@Image@@: muestra una imagen o un ícono.",
            "@@Spacer@@: deja espacio en blanco entre elementos.",
        ]),
        ("bullets", "Text con estilo", [
            "Text(\"Título\", fontSize = 24.sp, fontWeight = FontWeight.Bold).",
            "color = Color(0xFFFD531E) para el color del texto.",
            "textAlign, maxLines y overflow controlan cómo se muestra.",
            "Unidades: @@sp@@ para texto,  @@dp@@ para tamaños y espacios.",
        ]),
        ("bullets", "Modifier: el 'cómo se ve y se comporta'", [
            "Un @@Modifier@@ ajusta tamaño, espaciado, fondo y comportamiento.",
            "Se encadena:  Modifier.padding(16.dp).background(color).clickable { }.",
            "El **orden importa**: cada modifier envuelve al anterior.",
            "Casi todos los composables aceptan un parámetro modifier.",
        ]),
        ("tabla", "Modifiers más usados", ["Modifier", "Qué hace", "Ejemplo"], [
            ["size / width / height", "fija el tamaño", "Modifier.size(48.dp)"],
            ["padding", "margen interior", "Modifier.padding(8.dp)"],
            ["fillMaxWidth", "ocupa todo el ancho", "Modifier.fillMaxWidth()"],
            ["background", "color de fondo", "Modifier.background(Color.LightGray)"],
            ["clickable", "reacciona al toque", "Modifier.clickable { }"],
        ], dict(col_w=[3.0, 3.4, 5.6], note="Un Modifier se pasa a casi cualquier composable; encadena varios para lograr el efecto.")),
        ("bullets", "Button y la interacción básica", [
            "Button(onClick = { /* acción */ }) { Text(\"Enviar\") }.",
            "El lambda **onClick** se ejecuta al pulsar el botón.",
            "Variantes:  OutlinedButton, TextButton, IconButton.",
            "enabled = false lo deshabilita (lo usarás en los formularios).",
        ]),
        ("bullets", "@Preview: ver la UI mientras la construyes", [
            "@Preview sobre un @Composable muestra la UI **sin ejecutar** la app.",
            "Puedes tener @@varias previews@@ (distintos estados o tamaños).",
            "En Kotlin Playground (modo Compose) ves el resultado en el navegador al ejecutar.",
            "Iterar rápido es clave para diseñar interfaces.",
        ]),
        ("bullets", "Ejemplo: una tarjeta de perfil", [
            "Column { Text(nombre); Text(cargo); Button(...) { Text(\"Seguir\") } }.",
            "Cada pieza es un composable; se combinan dentro de un contenedor.",
            "Con Modifier ajustas padding, fondo y tamaños.",
            "Este es el @@reto de hoy@@ (entregable: enlace del preview).",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground (modo Compose)**: crea un @Composable Tarjeta() con un Text de título, un Text de subtítulo y un Button.",
        "Aplica al menos 3 **Modifier** (padding, background, fillMaxWidth) y estiliza el título (tamaño y negrita).",
        ("Ejecuta y captura la vista previa en el navegador.", 1),
        "Entregable en **examlab** (Taller S2): enlace del preview (o el .kt) + captura.",
    ],
    logros=[
        "Entendimos la **UI declarativa** de Compose.",
        "Usamos **Text, Button, Image y Spacer**.",
        "Estilizamos y ajustamos con **Modifier** (y su orden).",
        "Iteramos con **@Preview** viendo la UI en el navegador.",
    ],
    cierre=("¡Nos vemos en la Sesión 3!",
            ["Próxima sesión: **Layouts — Column, Row y Box**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya conoces las piezas… ¡ahora organízalas en una pantalla completa!"),
 ),

 3: dict(
    titulo="Layouts y organización de la pantalla",
    subtitulo="Column, Row y Box: armar la pantalla por bloques",
    archivo="Sesion 3 - Layouts y organizacion de la pantalla",
    nivel=1, gancho="¡Arma la pantalla por bloques!",
    foco="Organizar y alinear la interfaz con los contenedores de Compose (Column, Row, Box), usando Arrangement, Alignment, espaciado y diseño responsivo básico (weight, fillMax…).",
    contenido=[
        ("bullets", "El problema: ordenar la pantalla", [
            "Una pantalla real tiene muchos elementos: hay que @@organizarlos@@.",
            "Compose usa **contenedores (layouts)** que colocan a sus hijos.",
            "Los tres fundamentales:  **Column, Row y Box**.",
            "Se anidan entre sí para lograr cualquier diseño.",
        ]),
        ("bullets", "Column, Row y Box", [
            "@@Column@@: apila los hijos en **vertical** (uno debajo de otro).",
            "@@Row@@: los alinea en **horizontal** (uno al lado del otro).",
            "@@Box@@: los **superpone** (uno encima de otro), útil para capas.",
            "Todos reciben un contenido { } con los composables hijos.",
        ]),
        ("bullets", "Alinear y distribuir: Arrangement y Alignment", [
            "En Column:  verticalArrangement (repartir) + horizontalAlignment (alinear).",
            "En Row:  horizontalArrangement + verticalAlignment.",
            "Ejemplos:  Arrangement.SpaceBetween, Center, spacedBy(8.dp).",
            "Alignment:  CenterHorizontally, Start, End.",
        ]),
        ("tabla", "Arrangement vs Alignment", ["", "En Column", "En Row"], [
            ["Repartir (eje principal)", "verticalArrangement", "horizontalArrangement"],
            ["Alinear (eje cruzado)", "horizontalAlignment", "verticalAlignment"],
            ["Separación fija entre hijos", "Arrangement.spacedBy(8.dp)", "Arrangement.spacedBy(8.dp)"],
        ], dict(col_w=[4.0, 4.0, 4.0], note="Arrangement reparte en el eje del contenedor; Alignment alinea en el eje contrario.")),
        ("bullets", "Espaciado: padding, Spacer y spacedBy", [
            "Modifier.padding(16.dp) da aire alrededor de un composable.",
            "Spacer(Modifier.height(8.dp)) separa dos elementos puntuales.",
            "Arrangement.spacedBy(8.dp) separa @@todos@@ los hijos por igual.",
            "Un buen espaciado hace la UI legible y ordenada.",
        ]),
        ("bullets", "Anidar layouts para componer pantallas", [
            "Un Column puede contener un Row, y ese Row otros composables.",
            "Así la pantalla se vuelve un @@árbol@@ de composables.",
            "Ejemplo:  Column { Text; Row { Image; Column { Text; Text } } }.",
            "Piensa el diseño 'de fuera hacia dentro'.",
        ]),
        ("bullets", "Diseño responsivo: weight y fillMax", [
            "Modifier.fillMaxWidth() / fillMaxSize() ocupa todo el espacio disponible.",
            "En un Row/Column, Modifier.weight(1f) @@reparte el espacio sobrante@@.",
            "weight(2f) toma el doble de espacio que weight(1f).",
            "Así la UI se adapta a distintos tamaños de pantalla.",
        ]),
        ("bullets", "Ejemplo: barra superior con título y acción", [
            "Row(Modifier.fillMaxWidth(), horizontalArrangement = SpaceBetween) { Text(\"Inicio\"); IconButton(...) }.",
            "El Text va a la izquierda; el ícono, a la derecha.",
            "Con weight y arrangement controlas el reparto del espacio.",
            "@@Reto de hoy@@: maquetar una pantalla (entregable: preview).",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground (modo Compose)**: maqueta una pantalla con un **Column** que contenga un **Text** de título y un **Row** con 2-3 elementos.",
        "Usa **Arrangement/Alignment** y al menos un **weight** o **fillMaxWidth** para el reparto.",
        ("Ejecuta y captura la pantalla en el navegador.", 1),
        "Entregable en **examlab** (Taller S3): enlace del preview + captura.",
    ],
    logros=[
        "Organizamos con **Column, Row y Box**.",
        "Distribuimos y alineamos con **Arrangement y Alignment**.",
        "Espaciamos con **padding, Spacer y spacedBy**.",
        "Hicimos diseño responsivo con **weight y fillMax**.",
    ],
    cierre=("¡Nos vemos en la Sesión 4!",
            ["Próxima sesión: **Estado e interacción — remember y recomposición**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya ordenas la pantalla… ¡ahora haz que reaccione al usuario!"),
 ),

 4: dict(
    titulo="Estado e interacción",
    subtitulo="Que la interfaz reaccione al usuario",
    archivo="Sesion 4 - Estado e interaccion",
    nivel=2, gancho="¡Que la interfaz reaccione!",
    foco="Hacer que la UI reaccione al usuario con el estado de Compose y la recomposición: remember + mutableStateOf, eventos (onClick, onValueChange) y la idea de state hoisting.",
    contenido=[
        ("bullets", "El problema: una UI que no cambia", [
            "Hasta ahora las pantallas eran @@estáticas@@ (siempre iguales).",
            "Una app real **reacciona**: al tocar un botón, algo cambia.",
            "Para eso necesitamos **estado** (state) en la UI.",
            "Compose observa el estado y actualiza la pantalla por ti.",
        ]),
        ("bullets", "¿Qué es el estado y la recomposición?", [
            "**Estado** = un dato que puede cambiar y que la UI muestra (un contador, un texto).",
            "Cuando el estado cambia, Compose vuelve a ejecutar el composable: @@recomposición@@.",
            "Solo se redibuja lo que depende de ese dato.",
            "Tú cambias el dato; Compose actualiza la UI sola.",
        ]),
        ("bullets", "remember + mutableStateOf", [
            "mutableStateOf(0) crea un estado @@observable@@.",
            "remember { } lo **conserva** entre recomposiciones (no se reinicia).",
            "Patrón típico:  var count by remember { mutableStateOf(0) }.",
            "Sin remember, el valor se perdería en cada recomposición.",
        ]),
        ("bullets", "Eventos: onClick y onValueChange", [
            "Los composables interactivos reciben @@lambdas de evento@@.",
            "Button(onClick = { count++ }) reacciona al toque.",
            "TextField(onValueChange = { texto = it }) reacciona al teclear.",
            "En el evento actualizas el estado  →  recomposición.",
        ]),
        ("bullets", "Ejemplo: un contador", [
            "var count by remember { mutableStateOf(0) }.",
            "Text(\"Clics: $count\").",
            "Button(onClick = { count++ }) { Text(\"Sumar\") }.",
            "Cada clic sube count y el Text se actualiza @@solo@@.",
        ]),
        ("tabla", "Errores comunes con el estado", ["Error", "Consecuencia", "Solución"], [
            ["Olvidar remember", "el valor se reinicia en cada recomposición", "envuélvelo con remember"],
            ["Usar var normal (no state)", "la UI no se entera del cambio", "usa mutableStateOf"],
            ["Mutar una lista in-place", "no dispara recomposición", "crea una lista/estado nuevo"],
        ], dict(col_w=[3.2, 5.0, 3.8], note="Regla: el estado que la UI muestra SIEMPRE va en un mutableStateOf recordado.")),
        ("bullets", "State hoisting (elevar el estado)", [
            "Idea: sacar el estado del composable hijo y ponerlo en el @@padre@@.",
            "El hijo recibe el value y una lambda onValueChange (sin estado propio).",
            "Ventajas: el hijo es **reutilizable** y fácil de previsualizar.",
            "Patrón: 'estado abajo (value), eventos arriba (callbacks)'.",
        ]),
        ("bullets", "Ejemplo: un interruptor (toggle)", [
            "var activo by remember { mutableStateOf(false) }.",
            "Switch(checked = activo, onCheckedChange = { activo = it }).",
            "Text(if (activo) \"Encendido\" else \"Apagado\").",
            "La UI refleja el estado @@al instante@@.",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground (modo Compose)**: construye un **contador** con un Text y dos botones (+ y −) usando remember + mutableStateOf.",
        "Añade un **Switch** o un botón 'Reiniciar' que ponga el contador en 0.",
        ("Ejecuta, prueba la interacción y captura.", 1),
        "Entregable en **examlab** (Taller S4): enlace del preview + captura.",
    ],
    logros=[
        "Entendimos **estado** y **recomposición**.",
        "Guardamos estado con **remember + mutableStateOf**.",
        "Reaccionamos con **onClick / onValueChange**.",
        "Conocimos el **state hoisting**.",
    ],
    cierre=("¡Nos vemos en la Sesión 5!",
            ["Próxima sesión: **Listas y datos — LazyColumn**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya reaccionas a un dato… ¡ahora muestra colecciones enteras!"),
 ),

 5: dict(
    titulo="Listas y datos en pantalla",
    subtitulo="Mostrar colecciones con LazyColumn",
    archivo="Sesion 5 - Listas y datos en pantalla",
    nivel=2, gancho="¡Muestra colecciones enteras!",
    foco="Renderizar listas de datos de forma eficiente con LazyColumn/LazyRow, items() y key, separando el dato (data class) de su presentación (Card/fila).",
    contenido=[
        ("bullets", "El problema: muchos datos en pantalla", [
            "Casi toda app muestra @@listas@@ (chats, productos, tareas).",
            "Pintar cientos de elementos a la vez sería lento.",
            "Compose ofrece listas **perezosas (lazy)** que solo componen lo visible.",
            "La base: ya sabes usar List y colecciones en Kotlin.",
        ]),
        ("bullets", "Column vs LazyColumn", [
            "Column dibuja @@todos@@ los hijos de golpe (bien para pocos, fijos).",
            "LazyColumn solo compone lo @@visible@@ y recicla al hacer scroll.",
            "LazyRow es la versión horizontal.",
            "Para datos dinámicos o largos: **siempre Lazy**.",
        ]),
        ("bullets", "items(): recorrer la colección", [
            "LazyColumn { items(lista) { producto -> ... } }.",
            "Por cada elemento defines cómo se ve (una fila o tarjeta).",
            "items(lista) recorre toda la colección.",
            "item { } añade un elemento suelto (cabecera, botón).",
        ]),
        ("bullets", "La importancia de key", [
            "items(lista, key = { it.id }) da a cada fila una @@identidad estable@@.",
            "Ayuda a Compose a reciclar y animar bien al cambiar la lista.",
            "Usa un **id único**, no la posición.",
            "Sin key funciona, pero con key es más eficiente y correcto.",
        ]),
        ("bullets", "Del dato a la tarjeta: separar datos y presentación", [
            "Modela el dato con una @@data class@@:  Producto(val nombre, val precio).",
            "Ten una  List<Producto>  (tus datos).",
            "La UI recorre la lista y pinta cada uno como una @@Card@@.",
            "Separar dato y UI hace el código claro y reutilizable.",
        ]),
        ("bullets", "Card y filas de lista", [
            "Card { } es un contenedor con sombra y esquinas redondeadas.",
            "Dentro pones un Row/Column con el contenido del elemento.",
            "ListItem (Material 3) da un formato de fila listo para usar.",
            "Añade padding y separación entre tarjetas.",
        ]),
        ("tabla", "Piezas para una lista", ["Pieza", "Rol"], [
            ["data class", "modela cada elemento (el dato)"],
            ["List<T>", "la colección de datos"],
            ["LazyColumn", "el contenedor perezoso"],
            ["items(...)", "recorre la colección"],
            ["Card / Row", "la presentación de cada elemento"],
        ], dict(col_w=[4.0, 8.0], note="El dato y su presentación son cosas distintas: la data class es el dato; la Card, cómo se ve.")),
        ("bullets", "Ejemplo: lista de productos", [
            "val productos = listOf(Producto(\"Café\", 3.5), Producto(\"Té\", 2.0)).",
            "LazyColumn { items(productos) { p -> Card { Text(p.nombre); Text(\"$${p.precio}\") } } }.",
            "Compose pinta una tarjeta por producto.",
            "@@Reto de hoy@@: una lista de tarjetas (entregable: preview).",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground (modo Compose)**: crea una **data class** (Tarea, Producto o Contacto) y una **List** con 4-5 elementos.",
        "Muéstralos en una **LazyColumn** con **items()**, pintando cada uno en una **Card** (usa key).",
        ("Ejecuta, desplázate por la lista y captura.", 1),
        "Entregable en **examlab** (Taller S5): enlace del preview + captura.",
    ],
    logros=[
        "Usamos **LazyColumn/LazyRow** para listas eficientes.",
        "Recorrimos datos con **items()** y usamos **key**.",
        "Presentamos cada elemento en una **Card**.",
        "Separamos el **dato** (data class) de su **presentación**.",
    ],
    cierre=("¡Nos vemos en la Sesión 6!",
            ["Próxima sesión: **Entrada del usuario y formularios**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya muestras datos… ¡ahora deja que el usuario los escriba!"),
 ),

 6: dict(
    titulo="Entrada del usuario y formularios",
    subtitulo="Capturar y validar datos en la app",
    archivo="Sesion 6 - Entrada del usuario y formularios",
    nivel=2, gancho="¡Captura y valida datos!",
    foco="Capturar entrada con TextField/OutlinedTextField y su estado, manejar varios campos, validar (requerido, formato, longitud) y habilitar el botón según la validez.",
    contenido=[
        ("bullets", "El problema: recibir datos del usuario", [
            "Los formularios (login, registro, búsqueda) son el corazón de muchas apps.",
            "Hay que **capturar**, **validar** y reaccionar a lo que el usuario escribe.",
            "En Compose, un campo de texto se conecta a un @@estado@@.",
            "Reutilizamos lo de la Sesión 4 (estado y eventos).",
        ]),
        ("bullets", "TextField y OutlinedTextField", [
            "TextField muestra un campo para escribir texto.",
            "OutlinedTextField es la variante con borde (muy usada).",
            "Reciben value (qué muestran) y onValueChange (qué hacer al teclear).",
            "label, placeholder y leadingIcon mejoran la experiencia.",
        ]),
        ("bullets", "El campo controlado: el estado manda", [
            "var texto by remember { mutableStateOf(\"\") }.",
            "value = texto  y  onValueChange = { texto = it }.",
            "El @@estado es la fuente de verdad@@: el campo muestra siempre su valor.",
            "Este patrón (controlado) es el estándar en Compose.",
        ]),
        ("bullets", "Manejar varios campos", [
            "Un estado por campo:  nombre, email, clave.",
            "O un solo estado con una data class del formulario.",
            "Cada TextField actualiza @@su parte@@ del estado.",
            "Todo el formulario vive en el estado de la pantalla.",
        ]),
        ("bullets", "Validación: requerido, formato y longitud", [
            "@@Requerido@@: el campo no puede estar vacío  (texto.isNotBlank()).",
            "@@Formato@@: el email contiene '@' y '.' (o un patrón).",
            "@@Longitud@@: la clave tiene al menos N caracteres.",
            "Valida **en vivo** mientras el usuario escribe.",
        ]),
        ("bullets", "Mensajes de error e isError", [
            "OutlinedTextField(isError = emailInvalido) marca el campo en rojo.",
            "Muestra un Text de ayuda debajo cuando hay error.",
            "Sé claro:  'El correo no es válido', no 'Error'.",
            "Buen feedback = menos frustración del usuario.",
        ]),
        ("bullets", "Habilitar el botón según la validez", [
            "val formularioValido = nombre.isNotBlank() && emailValido.",
            "Button(enabled = formularioValido, onClick = { ... }).",
            "El botón @@se activa solo@@ cuando todo es correcto.",
            "Evita envíos con datos incompletos o erróneos.",
        ]),
        ("tabla", "Reglas de validación típicas", ["Campo", "Regla", "Comprobación"], [
            ["Nombre", "requerido", "texto.isNotBlank()"],
            ["Email", "formato", "\"@\" in email && \".\" in email"],
            ["Clave", "longitud mínima", "clave.length >= 6"],
            ["Confirmar clave", "coincide", "clave == confirmar"],
        ], dict(col_w=[3.2, 3.0, 5.8], note="Combina las reglas: el botón se habilita solo si TODAS se cumplen.")),
    ],
    autonomo=[
        "En **Kotlin Playground (modo Compose)**: crea un formulario con 2-3 **OutlinedTextField** (nombre, email, clave) usando estado.",
        "Valida cada campo, muestra un **mensaje de error** y **habilita el botón** solo si el formulario es válido.",
        ("Ejecuta, prueba datos válidos e inválidos y captura.", 1),
        "Entregable en **examlab** (Taller S6): enlace del preview + captura.",
    ],
    logros=[
        "Capturamos entrada con **TextField/OutlinedTextField**.",
        "Usamos **campos controlados** (el estado manda).",
        "Validamos por **requerido, formato y longitud**.",
        "Habilitamos el **botón** según la validez y mostramos errores.",
    ],
    cierre=("¡Nos vemos en la Sesión 7!",
            ["Próxima sesión: **Navegación entre pantallas**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya capturas datos… ¡ahora conecta varias pantallas en una app!"),
 ),

 7: dict(
    titulo="Navegación entre pantallas",
    subtitulo="Varias pantallas y el paso de datos",
    archivo="Sesion 7 - Navegacion entre pantallas",
    nivel=3, gancho="¡Conecta varias pantallas!",
    foco="Estructurar una app de varias pantallas con navigation-compose: NavHost, composable(route), NavController, navegar y volver atrás (back stack) y pasar argumentos.",
    contenido=[
        ("bullets", "El problema: una app tiene varias pantallas", [
            "Login, lista, detalle, ajustes… una app son @@varias pantallas@@.",
            "Hay que ir de una a otra y poder **volver atrás**.",
            "Compose usa la librería @@navigation-compose@@.",
            "Cada pantalla es un @Composable con una ruta (una dirección de texto).",
        ]),
        ("bullets", "NavController y NavHost", [
            "@@NavController@@: el 'GPS' que recuerda dónde estás y a dónde vas.",
            "@@NavHost@@: declara el mapa de rutas de la app.",
            "composable(\"home\") { HomeScreen() } asocia una ruta a una pantalla.",
            "startDestination indica la pantalla inicial.",
        ]),
        ("bullets", "Navegar: navigate() y volver atrás", [
            "navController.navigate(\"detail\") @@apila@@ la pantalla Detail.",
            "El conjunto de pantallas apiladas es el @@back stack@@.",
            "navController.popBackStack() (o el botón atrás) @@desapila@@ y vuelve.",
            "Navegar = apilar;  atrás = desapilar.",
        ]),
        ("tabla", "Piezas de navigation-compose", ["Pieza", "Rol"], [
            ["NavController", "controla la navegación y el back stack"],
            ["NavHost", "contiene el grafo de rutas"],
            ["composable(route)", "define una pantalla"],
            ["navigate(\"ruta\")", "va a otra pantalla"],
            ["popBackStack()", "vuelve a la pantalla anterior"],
        ], dict(col_w=[4.0, 8.0], note="El NavHost es el mapa; el NavController, quien te lleva por él.")),
        ("bullets", "Pasar argumentos entre pantallas", [
            "Ruta con parámetro:  composable(\"detail/{id}\") { ... }.",
            "Navegas con el valor:  navigate(\"detail/42\").",
            "Lees el argumento:  backStackEntry.arguments?.getString(\"id\").",
            "Así el detalle sabe @@qué elemento@@ mostrar.",
        ]),
        ("bullets", "Estructurar una app de varias pantallas", [
            "Una función @Composable por pantalla (HomeScreen, DetailScreen).",
            "Un NavHost central que las conecta.",
            "Cada pantalla recibe el navController o lambdas de navegación.",
            "Mejor: pasa lambdas onNavigate para @@desacoplar@@ (hoisting de navegación).",
        ]),
        ("bullets", "Ejemplo: lista → detalle", [
            "Home muestra una lista; al tocar un ítem:  navigate(\"detail/${item.id}\").",
            "Detail lee el id y muestra ese elemento.",
            "El botón atrás vuelve a la lista (back stack).",
            "Es el patrón clásico @@maestro-detalle@@.",
        ]),
        ("bullets", "Buenas prácticas de navegación", [
            "Rutas como **constantes** (evita 'strings mágicos').",
            "No pases objetos grandes por la ruta: pasa un **id**.",
            "Piensa el flujo del usuario antes de codificar.",
            "Mantén el NavHost como el @@único mapa@@ de la app.",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground (modo Compose)**: crea 2 pantallas (Home y Detalle) con un **NavHost** y **composable(route)**.",
        "Desde Home, **navega** a Detalle pasando un **argumento** (un id o un nombre) y muéstralo; permite **volver atrás**.",
        ("Ejecuta, navega ida y vuelta y captura ambas pantallas.", 1),
        "Entregable en **examlab** (Taller S7): enlace del preview + captura.",
    ],
    logros=[
        "Entendimos rutas, **NavHost** y **NavController**.",
        "Navegamos con **navigate()** y volvimos con el **back stack**.",
        "Pasamos **argumentos** entre pantallas.",
        "Estructuramos una app de **varias pantallas**.",
    ],
    cierre=("¡Nos vemos en la Sesión 8!",
            ["Próxima sesión: **Temas, Material Design y recursos**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya conectas pantallas… ¡ahora haz que tu app se vea profesional!"),
 ),

 8: dict(
    titulo="Temas, Material Design y recursos",
    subtitulo="Que la app se vea profesional",
    archivo="Sesion 8 - Temas, Material Design y recursos",
    nivel=3, gancho="¡Que tu app se vea profesional!",
    foco="Dar identidad visual con Material 3: MaterialTheme (colorScheme, typography), tema claro/oscuro, íconos e imágenes, y centralizar recursos (strings, colores) para coherencia y accesibilidad.",
    contenido=[
        ("bullets", "¿Qué es Material Design?", [
            "@@Material Design@@ es el sistema de diseño de Google.",
            "Da reglas de color, tipografía, espaciado y componentes.",
            "Compose trae **Material 3** (la versión actual) listo para usar.",
            "Una app con Material se ve @@profesional y familiar@@.",
        ]),
        ("bullets", "MaterialTheme: colorScheme, typography, shapes", [
            "MaterialTheme envuelve tu app y define su estilo.",
            "@@colorScheme@@: la paleta (primary, secondary, background…).",
            "@@typography@@: los estilos de texto (titleLarge, bodyMedium…).",
            "@@shapes@@: el redondeo de esquinas de los componentes.",
        ]),
        ("bullets", "Usar el tema en tus composables", [
            "Color:  MaterialTheme.colorScheme.primary.",
            "Texto:  style = MaterialTheme.typography.titleLarge.",
            "Así todo cambia de forma @@coherente@@ desde un solo lugar.",
            "Cambias la paleta una vez  →  toda la app se actualiza.",
        ]),
        ("bullets", "Tema claro y oscuro", [
            "lightColorScheme() y darkColorScheme() definen ambos modos.",
            "isSystemInDarkTheme() detecta la preferencia del sistema.",
            "El tema oscuro @@descansa la vista@@ y ahorra batería.",
            "Diseña pensando en los dos modos desde el inicio.",
        ]),
        ("bullets", "Íconos e imágenes", [
            "Material Icons:  Icon(Icons.Default.Favorite, contentDescription = \"...\").",
            "Image(painterResource(...)) para tus propias imágenes.",
            "contentDescription es clave para la @@accesibilidad@@.",
            "Usa íconos consistentes con Material.",
        ]),
        ("bullets", "Recursos: centralizar strings y valores", [
            "Evita los 'textos mágicos' repartidos por el código.",
            "Centraliza los textos (strings) y colores en un solo lugar.",
            "Facilita **traducir** la app y mantener la coherencia.",
            "Un cambio en un sitio se refleja en toda la app.",
        ]),
        ("tabla", "Antes vs con MaterialTheme", ["Aspecto", "Sin tema", "Con MaterialTheme"], [
            ["Color", "a mano en cada composable", "MaterialTheme.colorScheme"],
            ["Texto", "tamaños sueltos", "MaterialTheme.typography"],
            ["Modo oscuro", "difícil de mantener", "casi automático"],
            ["Coherencia visual", "frágil", "centralizada"],
        ], dict(col_w=[3.2, 4.4, 4.4], note="El tema centraliza el estilo: cámbialo en un lugar y toda la app lo hereda.")),
        ("bullets", "Accesibilidad básica", [
            "contentDescription en íconos e imágenes (lectores de pantalla).",
            "Buen @@contraste@@ de color (texto legible).",
            "Áreas de toque suficientes (mínimo ~48.dp).",
            "Diseñar accesible = diseñar para **todos**.",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground (modo Compose)**: envuelve una pantalla anterior en un **MaterialTheme** y usa **colorScheme** y **typography** en tus textos y botones.",
        "Define un **colorScheme** propio y prueba el **modo oscuro** (dark/light).",
        ("Ejecuta en ambos modos y captura.", 1),
        "Entregable en **examlab** (Taller S8): enlace del preview + captura (claro y oscuro).",
    ],
    logros=[
        "Aplicamos **Material 3** con **MaterialTheme**.",
        "Usamos **colorScheme** y **typography** de forma coherente.",
        "Implementamos **tema claro/oscuro**.",
        "Añadimos **íconos** y cuidamos la **accesibilidad**.",
    ],
    cierre=("¡Nos vemos en la Sesión 9!",
            ["Última sesión: **Datos externos y Proyecto integrador**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya tienes una app bonita… ¡ahora dale datos reales y complétala!"),
 ),

 9: dict(
    titulo="Datos externos y Proyecto integrador",
    subtitulo="Una app completa de principio a fin",
    archivo="Sesion 9 - Datos externos y Proyecto integrador",
    nivel=3, gancho="¡Tu app completa, de principio a fin!",
    foco="Integrar datos (una API con suspend o persistencia local simple) manejando los estados cargando/éxito/error, y construir el proyecto integrador: una app de varias pantallas que combine UI, estado, listas, navegación y tema.",
    contenido=[
        ("bullets", "El último salto: datos que vienen de afuera", [
            "Hasta ahora los datos estaban @@escritos en el código@@.",
            "Las apps reales traen datos de una **API** o los **guardan** localmente.",
            "Hoy conectamos la UI con datos externos.",
            "Y armamos el @@proyecto final@@ que integra todo el curso.",
        ]),
        ("bullets", "Consumir datos: suspend y corrutinas", [
            "Una @@función suspend@@ hace tareas largas (red) sin congelar la UI.",
            "Se lanza desde una corrutina (rememberCoroutineScope / LaunchedEffect).",
            "La app pide datos y sigue respondiendo mientras llegan.",
            "Idea clave: **no bloquear** el hilo de la interfaz.",
        ]),
        ("bullets", "Los estados de la UI: cargando, éxito, error", [
            "@@Cargando@@: muestra un CircularProgressIndicator.",
            "@@Éxito@@: pinta la lista o los datos.",
            "@@Error@@: muestra un mensaje amable y un botón 'reintentar'.",
            "Maneja **siempre los tres**: el usuario nunca ve una pantalla rota.",
        ]),
        ("bullets", "Persistencia local simple (alternativa)", [
            "No siempre hay API: a veces guardas datos en el @@dispositivo@@.",
            "Opciones:  DataStore (preferencias), Room (base de datos local).",
            "Para el proyecto basta una fuente de datos simple.",
            "Lo esencial: **separar** de dónde vienen los datos y la UI.",
        ]),
        ("bullets", "Integrar todo el curso", [
            "@@UI@@ (composables + listas) + @@estado@@ (remember).",
            "@@Navegación@@ entre pantallas + @@tema@@ Material 3.",
            "@@Datos@@ (API o local) alimentando la interfaz.",
            "Todas las piezas del curso, juntas en una sola app.",
        ]),
        ("bullets", "El Proyecto Integrador", [
            "Una app de @@2-3 pantallas@@ funcional (p. ej. lista → detalle).",
            "Debe usar: layouts, estado, una lista, navegación y un tema.",
            "Bonus: un formulario o datos externos.",
            "Entregable: enlace del preview web (o repositorio) + explicación.",
        ]),
        ("tabla", "Checklist del proyecto", ["Requisito", "¿Incluido?"], [
            ["Varios composables y layouts (Column/Row/Box)", "✔"],
            ["Estado con remember + interacción", "✔"],
            ["Una lista con LazyColumn", "✔"],
            ["Navegación entre 2+ pantallas", "✔"],
            ["Un tema MaterialTheme (color/tipografía)", "✔"],
        ], dict(col_w=[9.0, 3.0], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER],
                note="Marca cada requisito antes de entregar: es la rúbrica del proyecto final.")),
        ("bullets", "Cómo presentar y entregar", [
            "Ejecuta tu app en **Compose para Web** y consigue el enlace del preview.",
            "O sube el **repositorio** (plantilla en Codespaces / Gitpod).",
            "Demo del docente: la app corriendo en **Google AI Studio** (emulador).",
            "Sube todo a **examlab** (Proyecto S9) con una breve explicación.",
        ]),
    ],
    autonomo=[
        "**Proyecto integrador** en **Compose para Web**: una app de 2-3 pantallas con layouts, **estado**, una **LazyColumn**, **navegación** y un **MaterialTheme**.",
        "Añade el manejo de datos (una lista propia o una llamada simple) con estados de **carga/éxito**.",
        ("Ejecuta la app completa en el navegador y captura las pantallas.", 1),
        "Entregable en **examlab** (Proyecto S9): enlace del preview / repositorio + explicación de qué integraste.",
    ],
    logros=[
        "Consumimos datos con **suspend** y manejamos **cargando/éxito/error**.",
        "Conocimos la **persistencia local** simple.",
        "Integramos **UI + estado + listas + navegación + tema**.",
        "Construimos y presentamos la **app final**.",
    ],
    cierre=("¡Felicitaciones, terminaste el curso!",
            ["Completa tu **ruta en Coursera** dentro del plazo y responde la **encuesta de satisfacción**.",
             "De un composable 'Hola' a una app completa: ya construyes apps móviles con Compose."],
            "Este es tu punto de partida como desarrollador de aplicaciones móviles."),
 ),
}


# ============================== BUILDERS ==============================
def build_presentacion():
    set_footer(CURSO)
    prs = new_prs()
    course_cover(prs, CURSO_CORTO, None, "¡Bienvenidos estudiantes!",
        [PROGRAMA, "Cuatrimestre No. [20 — confirmar]", "Duración: **9 clases** (105 min c/u)",
         "Horario: Martes y Jueves 6:00–7:45 PM · Sábado 8:00–9:45 AM",
         "Fechas: 27/07/2026 – 15/08/2026"],
        "Empezamos a las 6:00 PM (sáb. 8:00 AM)…")
    tutor_slide(prs, TUTOR[0], TUTOR[1], TUTOR[2], idx=2)
    content_slide(prs, "METODOLOGÍA", [
        "**Sesiones teórico-prácticas**: cada clase combina teoría, modelación y práctica construyendo UI en Compose para Web.",
        "Momentos por clase:",
        ("**Motivación**: preguntas y ejemplos que generan interés y conexión.", 1),
        ("**Encuadre**: explicación de objetivos, ruta de aprendizaje y acuerdos.", 1),
        ("**Modelación**: código Compose guiado que muestra conceptos y técnicas.", 1),
        ("**Simulación**: trabajo en grupos pequeños para aplicar conceptos.", 1),
        ("**Ejercitación**: práctica individual construyendo UI en Compose para Web.", 1),
        ("**Cierre**: retroalimentación, resumen y conexión con objetivos.", 1),
        ("**Evaluación**: progreso en Coursera + Reto en vivo (Kahoot) en examlab.", 1),
    ], idx=3)
    objectives_slide(prs, "Objetivos", OBJETIVOS_CURSO, idx=4)
    table_content(prs, "¿Cómo se evalúa?", ["Componente", "Ponderación"], EVAL_ROWS,
                  col_w=[9.2, 2.8], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER], idx=5, note=EVAL_NOTE)
    content_slide(prs, "EJEMPLO DE EVALUACIÓN", [
        "Escala de 0 a 5.0.",
        "Progreso Coursera (90%): completó el 80% → 4.0 × 0.90 = **3.6**",
        "Asistencia (10%): asistió → 5.0 × 0.10 = **0.5**",
        "Participación en clase: no participó → **0**",
        "Kahoot / Reto en vivo: quedó de segundo → **+0.4**",
        "@@Nota final = 3.6 + 0.5 + 0 + 0.4 = 4.5@@",
    ], idx=6)
    content_slide(prs, "CONTENIDO", [
        f"**Sesión {n}** — {d['titulo']}." for n, d in SESIONES.items()
    ], size=14, idx=7)
    content_slide(prs, "RECURSOS", [
        "**Material de clases:** 🔗 [inserta aquí el hipervínculo] — guiones, diapositivas y material de apoyo.",
        "**Curso base (Coursera):** [confirmar el curso base de Android/Jetpack Compose en Coursera]",
        ("[URL del curso base — CONFIRMAR con coordinación (debe ser de desarrollo de apps Android/Compose, no de fundamentos de Kotlin)]", 1),
        "**Construye UI y previsualízala:** Kotlin Playground — entorno Compose",
        ("https://play.kotlinlang.org/", 1),
        "**Demo de app Android nativa (docente):** Google AI Studio",
        ("https://aistudio.google.com/", 1),
        "**Guías, quizzes y ruta de aprendizaje:** en examlab",
        ("https://examlab.lovable.app/app", 1),
    ], size=13, idx=8)
    content_slide(prs, "HERRAMIENTAS", [
        "**En examlab** (plataforma del curso · https://examlab.lovable.app/app):",
        ("Test (quizzes de conceptos) · Reto en vivo (Kahoot) · Taller/Proyecto (recibe el entregable). examlab NO ejecuta Compose.", 1),
        "**Solo online (gratuitas):**",
        ("Kotlin Playground — entorno Compose (play.kotlinlang.org) · GitHub Codespaces/Gitpod solo para el proyecto final · Google AI Studio (demo del docente).", 1),
        "**En el mundo laboral** (lo que usarás en el trabajo):",
        ("Android Studio · Jetpack Compose en Android · Gradle · Git/GitHub · emuladores y dispositivos Android · Google Play Console.", 1),
    ], size=14, idx=9)
    content_slide(prs, "¡ IMPORTANTE !", [
        "La **ruta de Coursera** es el **90%** de la nota: completa tu progreso a tiempo (licencias activas hasta el día hábil posterior al fin del curso).",
        "Construyes y ejecutas la UI en **Kotlin Playground (modo Compose)** (examlab no ejecuta Compose); los quizzes de código son de **lectura** ('¿qué muestra este composable?').",
        "Las **notas** se cargan hasta **una semana** después de la última clase; hay **3 días** para reclamaciones por correo.",
        "Responde la **encuesta de satisfacción** el último día del curso (sáb. 15-ago).",
    ], size=14, idx=10)
    image_slide(prs, "GESTORES", GESTORES_IMG, idx=11)
    out = os.path.join(BASE, "Presentacion del curso.pptx")
    prs.save(out)
    print("OK", out)


def build_sesion(n):
    d = SESIONES[n]
    set_footer(CURSO)
    prs = new_prs()
    # SIN "Recordemos la asignatura" NI "¿Cómo trabajaremos hoy?" (reglas del agente)
    session_cover(prs, f"SESIÓN {n}", NIVELES[d["nivel"]], d["titulo"], d["subtitulo"],
                  d["gancho"],
                  [f"{CURSO_CORTO} · {PROGRAMA}", "Duración: **105 min** (1 h 45 min)"])
    std_proposito(prs, d["foco"], d["nivel"])
    idx = 3
    for item in d["contenido"]:
        kind = item[0]
        if kind == "bullets":
            _, title, items = item
            img = img_for(title)
            if img:
                image_text_slide(prs, title, items, img, size=14, idx=idx)
            else:
                content_slide(prs, title, items, size=15, idx=idx)
        else:
            _, title, headers, rows, extra = item
            table_content(prs, title, headers, rows, idx=idx, **extra)
        idx += 1
    std_autonomo(prs, d["autonomo"], idx); idx += 1
    std_logros(prs, d["logros"], idx)
    big, lines, accent = d["cierre"]
    closing_slide(prs, big, lines, accent)
    folder = os.path.join(BASE, f"Sesion {n}")
    os.makedirs(folder, exist_ok=True)
    out = os.path.join(folder, d["archivo"] + ".pptx")
    prs.save(out)
    print("OK", out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    os.makedirs(BASE, exist_ok=True)
    fail = []
    def _safe(fn, label):
        try:
            fn()
        except PermissionError:
            fail.append(label + " (BLOQUEADO — ciérralo en PowerPoint)")
            print("  ⚠ SALTADO (bloqueado):", label)
        except Exception as e:
            fail.append(label + " (" + type(e).__name__ + ")")
            print("  ⚠ ERROR:", label, e)
    _safe(build_presentacion, "Presentacion del curso")
    for n in SESIONES:
        _safe(lambda n=n: build_sesion(n), f"Sesion {n}")
    if fail:
        print("LISTO CON PENDIENTES. No se pudieron escribir:", "; ".join(fail))
    else:
        print("LISTO: 10 decks generados (presentación + 9 sesiones de Compose).")
