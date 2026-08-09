# -*- coding: utf-8 -*-
# ⚠️ OBSOLETO — builder del Kotlin basico anterior. Reemplazado por build_desarrollo_moviles_1_v2.py. NO EJECUTAR.
# -*- coding: utf-8 -*-
"""
Genera los 10 decks .pptx del curso DESARROLLO DE APLICACIONES MÓVILES 1 (Kotlin):
presentación del curso + 9 sesiones. Identidad Nueva América (motor fesna_slides_engine).

Reglas aplicadas:
- Las diapositivas de sesión NO incluyen "Recordemos la asignatura" ni "¿Cómo trabajaremos hoy?".
- Sin porcentajes de nota en las sesiones (la evaluación va SOLO en la presentación del curso).
- Todas las clases duran lo mismo (105 min).
- Evaluación REAL del curso: Progreso Coursera 90% + Asistencia 10% + bono Kahoot (NO el 50/40/10).
- Práctica de 2 niveles: Tier 1 examlab (Test, Reto en vivo, Taller/Proyecto) + Tier 2 Kotlin Playground
  (examlab NO ejecuta Kotlin → programar Kotlin va SIEMPRE en Kotlin Playground). Nada se instala.
- Diapositivas mixtas: ~3-4 por sesión llevan un diagrama de concepto (config/slides/diagramas.py).

Config del curso: config/cursos/desarrollo-aplicaciones-moviles-1.json
Salida: Cursos/Desarrollo de Aplicaciones Moviles 1/Clases/v2/
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fesna_slides_engine import *

# --- Diapositivas MIXTAS: mapa (substring del título → id del diagrama del catálogo) ---
DIAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "diagramas")
IMG = [
    # S1
    ("Kotlin Playground", "kt_flujo_playground"),
    ("Variables: val", "kt_val_var"),
    ("Tipos básicos", "kt_tipos_basicos"),
    # S2
    ("if, else", "kt_if_else"),
    ("como expresión", "kt_if_expresion"),
    ("La estructura when", "kt_when"),
    # S3
    ("for y los rangos", "kt_rangos"),
    ("while y do-while", "kt_while_do"),
    ("Bucles anidados", "kt_nested_loops"),
    ("break y continue", "kt_break_continue"),
    # S4
    ("Anatomía de una función", "kt_anatomia_funcion"),
    ("valores de retorno", "kt_llamada_funcion"),
    ("por defecto y nombrados", "kt_args"),
    # S5
    ("clase es el molde", "kt_clase_objeto"),
    ("Anatomía de una clase", "kt_anatomia_clase"),
    ("Crear objetos", "kt_crear_objeto"),
    # S6
    ("La herencia", "kt_herencia"),
    ("Interfaces y clases abstractas", "kt_interface_abstract"),
    ("El polimorfismo", "kt_polimorfismo"),
    ("Modificadores de visibilidad", "kt_visibilidad"),
    # S7
    ("data class", "kt_dataclass"),
    ("Nulabilidad", "kt_nulabilidad"),
    ("Operadores de null", "kt_null_operadores"),
    ("Manejo de excepciones", "kt_try_catch"),
    # S8
    ("List, Set y Map", "kt_colecciones"),
    ("Inmutable vs mutable", "kt_inmutable_mutable"),
    ("filter y map", "kt_pipeline"),
    # S9
    ("de la consola a la interfaz", "kt_playground_vs_compose"),
    ("Qué es Compose Multiplatform", "kt_compose_targets"),
    ("WebAssembly", "kt_wasm_flujo"),
    ("UI declarativa", "kt_declarativo"),
]

def img_for(title):
    tl = (title or "").lower()
    for sub, did in IMG:
        if sub.lower() in tl:
            p = os.path.join(DIAG_DIR, did + ".png")
            return p if os.path.exists(p) else None
    return None

BASE = r"g:\Mi unidad\Trabajos\Empleo\FESNA\Cursos\Desarrollo de Aplicaciones Moviles 1\Clases\_OBSOLETO-no-usar"
CURSO = "Desarrollo de Aplicaciones Móviles 1"
CURSO_CORTO = "Desarrollo de Aplicaciones Móviles 1"
PROGRAMA = "Ingeniería de Sistemas"

TUTOR = ("Julian Andrés Castaño Espinosa",
         ["Líder Técnico", "Ingeniero de Sistemas", "Candidato a MsC en IA"],
         "julian.castano@lanuevaamerica.edu.co")

OBJETIVOS_CURSO = [
    "Escribir programas en Kotlin con variables y tipos, condicionales, bucles y funciones, ejecutándolos en Kotlin Playground.",
    "Aplicar la programación orientada a objetos en Kotlin: clases y objetos, herencia, interfaces, polimorfismo y visibilidad.",
    "Usar colecciones, nulabilidad, data classes, enums y manejo de excepciones, y comprender el salto a interfaces con Compose Multiplatform Web.",
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
    1: "Nivel 1 — Fundamentos del lenguaje",
    2: "Nivel 2 — Programación orientada a objetos",
    3: "Nivel 3 — Colecciones, robustez e interfaces",
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
        "Chequea tu saber con el **quiz de la sesión (Test)** y el **Reto en vivo (Kahoot)** en examlab; el código se escribe en **Kotlin Playground**.",
    ], size=15, idx=idx)


# ============================== SESIONES ==============================
SESIONES = {
 1: dict(
    titulo="Introducción a Kotlin y primeros programas",
    subtitulo="Tu primer código Kotlin en el navegador (Kotlin Playground)",
    archivo="Sesion 1 - Introduccion a Kotlin y primeros programas",
    nivel=1, gancho="¡Tu primer programa Kotlin!",
    foco="Escribir y ejecutar un primer programa Kotlin en Kotlin Playground, usando variables (val/var), tipos básicos, impresión por consola y plantillas de string.",
    contenido=[
        ("bullets", "¿Qué es Kotlin y para qué sirve?", [
            "Kotlin es un lenguaje **moderno** creado por JetBrains; lenguaje **oficial de Android** desde 2019 (Google).",
            "Es **conciso**, **seguro** (evita errores de null) e **interoperable** con Java.",
            "Corre en la JVM y también compila a JavaScript y nativo: es la base del desarrollo Android.",
            "En este curso aprendes los @@fundamentos del lenguaje@@: el cimiento para crear apps móviles.",
            "Hoy solo necesitas un navegador: no se instala nada.",
        ]),
        ("bullets", "Kotlin Playground: tu laboratorio en el navegador", [
            "Kotlin Playground (play.kotlinlang.org) es un editor **online** que compila y ejecuta Kotlin.",
            "Escribes el código, pulsas @@Run (▶)@@ y ves la salida en la consola de abajo.",
            "No instala nada; puedes guardar y compartir con un enlace.",
            "Es la herramienta oficial para practicar TODO el curso.",
        ]),
        ("bullets", "La estructura de un programa: fun main()", [
            "Todo programa Kotlin arranca en la función main:  fun main() { ... }.",
            "Entre las llaves { } va el **cuerpo**: las instrucciones que se ejecutan en orden.",
            "Cada instrucción va en una línea; Kotlin **no exige punto y coma**.",
            "main es el @@punto de entrada@@: donde el programa empieza a correr.",
        ]),
        ("tabla", "Imprimir en consola: println() vs print()", ["Instrucción", "Qué hace", "Ejemplo → salida"], [
            ["println(\"Hola\")", "Imprime y **salta** de línea", "Hola ⏎"],
            ["print(\"Hola\")", "Imprime **sin** saltar de línea", "Hola (sigue en la misma línea)"],
            ["println()", "Imprime una línea en blanco", "(línea vacía)"],
        ], dict(col_w=[3.6, 4.2, 4.2], note="println = 'print line'. Es lo que usarás para ver resultados en la consola.")),
        ("bullets", "Variables: val vs var", [
            "Una **variable** guarda un dato con un nombre.",
            "@@val@@ = inmutable: se asigna una vez y no cambia  (val pi = 3.14).",
            "@@var@@ = mutable: se puede reasignar  (var contador = 0; contador = 1).",
            "Regla de oro: usa **val por defecto**; var solo si de verdad cambia.",
        ]),
        ("bullets", "Tipos básicos e inferencia de tipos", [
            "Cada dato tiene un **tipo**: Int, Double, Boolean, String, Char.",
            "Kotlin @@infiere el tipo@@ solo:  val edad = 20  ya es Int.",
            "Puedes escribirlo:  val edad: Int = 20.",
            "El tipo es fijo: a un Int no le metes texto.",
        ]),
        ("bullets", "Comentarios en el código", [
            "// comenta **una línea**.",
            "/* ... */ comenta **un bloque** de varias líneas.",
            "El compilador @@ignora@@ los comentarios: son notas para humanos.",
            "Buen hábito: comenta el **porqué**, no lo obvio.",
        ]),
        ("bullets", "Plantillas de string: $ y ${}", [
            "Insertas una variable dentro de un texto con $:  \"Hola $nombre\".",
            "Para una **expresión**, usa ${}:  \"Doble: ${x * 2}\".",
            "Evita concatenar con + : queda más limpio y legible.",
            "Ejemplo:  \"Tengo $edad años\"  →  @@Tengo 20 años@@.",
        ]),
    ],
    autonomo=[
        "Abre **Kotlin Playground** (play.kotlinlang.org).",
        "Escribe un programa con fun main() que declare val nombre (tu nombre) y var edad (tu edad).",
        "Imprime con plantilla de string:  println(\"Hola, soy $nombre y tengo $edad años.\")  y ejecuta con **Run**.",
        ("Captura la salida en la consola de Playground.", 1),
        "Entregable en **examlab**: pega tu código (o el enlace de Playground) + la captura en la entrega de la sesión.",
    ],
    logros=[
        "Sabemos **qué es Kotlin** y para qué sirve.",
        "Ejecutamos código en **Kotlin Playground**.",
        "Distinguimos **val** (inmutable) de **var** (mutable) y los tipos básicos.",
        "Imprimimos con **println** y usamos **plantillas de string**.",
    ],
    cierre=("¡Nos vemos en la Sesión 2!",
            ["Próxima sesión: **Condicionales — if, else y when**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya imprimes en pantalla… ¡ahora enseña a tu programa a DECIDIR!"),
 ),

 2: dict(
    titulo="Condicionales: if, else y when",
    subtitulo="Tomar decisiones en el programa",
    archivo="Sesion 2 - Condicionales - if, else y when",
    nivel=1, gancho="¡Que el programa decida!",
    foco="Controlar el flujo del programa con condicionales en Kotlin: if/else, if como expresión, when y los operadores de comparación y lógicos.",
    contenido=[
        ("bullets", "¿Por qué necesitamos decisiones?", [
            "Un programa útil **elige caminos** según los datos.",
            "\"Si la nota es ≥ 3.0, aprueba; si no, reprueba\".",
            "Las decisiones se basan en condiciones @@Boolean@@ (true / false).",
            "Kotlin ofrece dos herramientas: **if/else** y **when**.",
        ]),
        ("bullets", "if, else y else if", [
            "if (condición) { ... } ejecuta el bloque si la condición es **true**.",
            "else { ... } es el camino alternativo.",
            "else if encadena varias condiciones.",
            "Solo se ejecuta @@el primer bloque@@ cuya condición sea verdadera.",
        ]),
        ("tabla", "Operadores de comparación y lógicos", ["Operador", "Significado", "Ejemplo"], [
            ["==  /  !=", "igual / distinto", "a == b   ·   a != b"],
            [">  <  >=  <=", "mayor / menor / o igual", "edad > 18   ·   nota >= 3.0"],
            ["&&", "Y — ambas verdaderas", "a > 0 && b > 0"],
            ["||", "O — alguna verdadera", "a > 0 || b > 0"],
            ["!", "NO — niega", "!activo"],
        ], dict(col_w=[3.2, 4.0, 4.8], note="== compara valores. && y || (dobles) son los operadores lógicos.")),
        ("bullets", "if como expresión (¡devuelve un valor!)", [
            "En Kotlin, if también es una @@expresión@@: devuelve un valor.",
            "val max = if (a > b) a else b.",
            "La **última línea** de cada rama es el valor que retorna.",
            "Reemplaza al operador ternario de otros lenguajes.",
        ]),
        ("bullets", "La estructura when", [
            "when compara un valor contra varias ramas (un switch mejorado).",
            "when (dia) { 1 -> \"Lunes\"; else -> \"Otro\" }.",
            "Cada rama:  valor -> resultado.",
            "@@else@@ cubre todos los casos restantes.",
        ]),
        ("tabla", "when: todas sus formas", ["Forma", "Ejemplo"], [
            ["Valor único", "1 -> \"Lunes\""],
            ["Varios valores", "6, 7 -> \"Fin de semana\""],
            ["Rango", "in 1..5 -> \"Entre semana\""],
            ["Sin argumento (como if/else if)", "when { x > 90 -> \"A\"; else -> \"F\" }"],
            ["Como expresión", "val txt = when (n) { ... }"],
        ], dict(col_w=[4.6, 7.4], note="when con rangos usa in; sin argumento funciona como un if/else if encadenado.")),
        ("bullets", "if/else vs when: ¿cuándo cada uno?", [
            "Usa @@if/else@@ para 1-2 condiciones o rangos simples.",
            "Usa @@when@@ cuando comparas UN valor contra muchas opciones.",
            "when es más legible que un if/else if largo.",
            "Ambos pueden ser **expresiones** que devuelven un valor.",
        ]),
        ("bullets", "Ejemplo resuelto: clasificar una nota", [
            "val nota = 4.2",
            "val estado = if (nota >= 3.0) \"Aprobó\" else \"Reprobó\"  →  Aprobó",
            "val letra = when { nota >= 4.5 -> \"Excelente\"; nota >= 3.0 -> \"Aceptable\"; else -> \"Insuficiente\" }",
            "println(\"$estado - $letra\")  →  @@Aprobó - Aceptable@@",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground**, declara una variable nota: Double.",
        "Con **when**, imprime \"Excelente/Bueno/Aceptable/Insuficiente\" según rangos (>=4.5, >=4.0, >=3.0, else).",
        "Usa **if como expresión** para imprimir \"Aprobó\"/\"Reprobó\".",
        ("Captura la salida de la consola.", 1),
        "Entregable en **examlab**: código (o enlace de Playground) + captura.",
    ],
    logros=[
        "Tomamos decisiones con **if / else / else if**.",
        "Usamos **if como expresión** (devuelve un valor).",
        "Dominamos **when** con valores, rangos y sin argumento.",
        "Aplicamos operadores de **comparación** y **lógicos**.",
    ],
    cierre=("¡Nos vemos en la Sesión 3!",
            ["Próxima sesión: **Bucles — for, while y nested loops**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya decides caminos… ¡ahora aprende a REPETIR tareas!"),
 ),

 3: dict(
    titulo="Bucles: for, while y nested loops",
    subtitulo="Repetir tareas y recorrer datos",
    archivo="Sesion 3 - Bucles - for, while y nested loops",
    nivel=1, gancho="¡Repetir sin copiar y pegar!",
    foco="Repetir instrucciones y recorrer datos con bucles en Kotlin: for sobre rangos y colecciones, while y do-while, bucles anidados, break/continue e iteración con índices.",
    contenido=[
        ("bullets", "¿Por qué repetir con bucles?", [
            "Un **bucle** repite instrucciones sin copiar-pegar.",
            "\"Saludar a 100 usuarios\" = un bucle de 2 líneas.",
            "Recorren **rangos** (1..10) y **colecciones** (listas).",
            "Kotlin: for, while y do-while.",
        ]),
        ("bullets", "for y los rangos: 1..5, until, downTo, step", [
            "for (i in 1..5) recorre del 1 al 5 (**ambos incluidos**).",
            "until excluye el último:  1 until 5  →  1, 2, 3, 4.",
            "downTo cuenta al revés:  5 downTo 1.",
            "step salta:  1..10 step 2  →  1, 3, 5, 7, 9.",
        ]),
        ("bullets", "for sobre colecciones", [
            "for recorre cada elemento de una lista:  for (fruta in frutas) { ... }.",
            "No manejas índices: te da @@el elemento directo@@.",
            "Ejemplo:  for (n in listOf(2, 4, 6)) println(n).",
            "Es la forma más común de recorrer datos.",
        ]),
        ("bullets", "while y do-while", [
            "while (condición) repite **mientras** sea true; revisa @@antes@@.",
            "do { ... } while (condición) ejecuta y revisa @@después@@ (al menos 1 vez).",
            "Úsalos cuando no sabes cuántas vueltas serán.",
            "Cuida el fin: cambia algo que rompa la condición (evita bucles infinitos).",
        ]),
        ("bullets", "Bucles anidados (nested loops)", [
            "Un bucle **dentro de otro**: útil para tablas y matrices.",
            "Por cada vuelta del exterior, el interior gira @@completo@@.",
            "Ejemplo clásico: la tabla de multiplicar (filas x columnas).",
            "Cuidado: multiplican el trabajo (3x3 = 9 vueltas).",
        ]),
        ("bullets", "break y continue", [
            "@@break@@ rompe el bucle y sale de inmediato.",
            "@@continue@@ salta a la siguiente vuelta (ignora el resto de esta).",
            "Útiles para cortar al encontrar algo o saltar casos.",
            "Úsalos con moderación: en exceso vuelven el código confuso.",
        ]),
        ("tabla", "Iterar con índices", ["Necesito", "Uso", "Ejemplo"], [
            ["El elemento", "for (x in lista)", "for (f in frutas)"],
            ["Solo los índices", "indices", "for (i in lista.indices)"],
            ["Índice + valor", "withIndex()", "for ((i, v) in lista.withIndex())"],
            ["Un rango numérico", "1..n", "for (i in 1..lista.size)"],
        ], dict(col_w=[3.2, 3.2, 5.6], note="withIndex() te da el índice y el valor a la vez.")),
        ("bullets", "Ejemplo resuelto: tabla de multiplicar", [
            "for (i in 1..3) { for (j in 1..3) { print(\"${i * j}\\t\") }; println() }",
            "Exterior i = filas;  interior j = columnas.",
            "Salida:  1 2 3  /  2 4 6  /  3 6 9.",
            "Este es el reto del @@Taller de hoy@@ (entregable .kt en examlab).",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground**: escribe la **tabla de multiplicar del 1 al 5** con @@bucles anidados@@.",
        "Formatea con \\t (tabulador) y un salto de línea por fila.",
        ("Ejecuta con Run y verifica la cuadrícula.", 1),
        "Entregable en **examlab** (Taller S3, .kt): sube tu archivo .kt (o el enlace de Playground) + captura.",
    ],
    logros=[
        "Recorrimos **rangos** con for (until, downTo, step).",
        "Recorrimos **colecciones** con for.",
        "Distinguimos **while** de **do-while** y usamos **break/continue**.",
        "Construimos una tabla con **bucles anidados**.",
    ],
    cierre=("¡Nos vemos en la Sesión 4!",
            ["Próxima sesión: **Funciones — parámetros, argumentos y retorno**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya repites tareas… ¡ahora empaquétalas en FUNCIONES reutilizables!"),
 ),

 4: dict(
    titulo="Funciones: parámetros, argumentos y valores de retorno",
    subtitulo="Reutilizar código con funciones",
    archivo="Sesion 4 - Funciones - parametros, argumentos y retorno",
    nivel=1, gancho="¡Escribe una vez, usa mil!",
    foco="Declarar y usar funciones en Kotlin: parámetros y tipo de retorno, Unit, argumentos por defecto y nombrados, funciones de una sola expresión y vararg.",
    contenido=[
        ("bullets", "¿Qué es una función y por qué usarla?", [
            "Una **función** es un bloque de código con nombre que hace una tarea.",
            "La defines una vez y la @@reutilizas@@ muchas.",
            "Evita repetir código (principio DRY: Don't Repeat Yourself).",
            "Ya usaste una: **main()** es una función.",
        ]),
        ("bullets", "Anatomía de una función", [
            "fun (palabra clave) · nombre · (parámetros) · : tipo de retorno.",
            "fun suma(a: Int, b: Int): Int { return a + b }.",
            "**Parámetros** = datos que entran; **retorno** = dato que sale.",
            "La llamas por su nombre:  @@suma(3, 4)@@.",
        ]),
        ("bullets", "Parámetros, argumentos y valores de retorno", [
            "@@Parámetro@@ = la variable en la definición  (a: Int).",
            "@@Argumento@@ = el valor real al llamar  (suma(3, 4) → 3 y 4).",
            "return devuelve el resultado a quien la llamó.",
            "El resultado se puede guardar:  val r = suma(3, 4).",
        ]),
        ("bullets", "El tipo Unit (funciones sin retorno)", [
            "Si una función no devuelve nada, su tipo es @@Unit@@ (y se omite).",
            "fun saludar(nombre: String) { println(\"Hola $nombre\") }.",
            "Hace algo (imprime) pero **no retorna** un valor.",
            "Unit es como el void de otros lenguajes.",
        ]),
        ("bullets", "Argumentos por defecto y nombrados", [
            "Por defecto:  fun saludar(msg: String = \"Hola\"); si no lo pasas, usa \"Hola\".",
            "Nombrados:  saludar(msg = \"Hey\") dice a qué parámetro va cada valor.",
            "Evitan crear muchas versiones de la misma función.",
            "Mejoran la @@legibilidad@@ al llamar.",
        ]),
        ("bullets", "Funciones de una sola expresión", [
            "Si el cuerpo es una sola expresión, usa = en vez de { return }.",
            "fun doble(x: Int) = x * 2.",
            "Más corto y legible.",
            "Kotlin infiere el tipo de retorno.",
        ]),
        ("bullets", "vararg: número variable de argumentos", [
            "vararg permite pasar @@cuantos argumentos quieras@@.",
            "fun sumar(vararg nums: Int): Int { ... }.",
            "sumar(1, 2, 3, 4) funciona igual que sumar(1, 2).",
            "Dentro, nums se comporta como un arreglo.",
        ]),
        ("tabla", "Alcance (scope) de las variables", ["Dónde se declara", "Dónde vive"], [
            ["Dentro de una función (local)", "Solo dentro de esa función"],
            ["Un parámetro", "Solo dentro de la función"],
            ["Fuera de toda función (top-level)", "En todo el archivo"],
        ], dict(col_w=[6.0, 6.0], note="Una variable local NO existe fuera de su función. Cada función es una 'cajita' independiente.")),
    ],
    autonomo=[
        "En **Kotlin Playground**: escribe una función esMayorDeEdad(edad: Int): Boolean que retorne edad >= 18.",
        "Escribe saludar(nombre: String, saludo: String = \"Hola\") con un **argumento por defecto**.",
        "Llama ambas desde main y usa **argumentos nombrados** al menos una vez; imprime los resultados.",
        ("Captura la salida.", 1),
        "Entregable en **examlab**: código (o enlace) + captura.",
    ],
    logros=[
        "Declaramos funciones con **parámetros** y **tipo de retorno**.",
        "Entendimos **Unit** (funciones sin retorno).",
        "Usamos **argumentos por defecto y nombrados** y funciones de una expresión.",
        "Conocimos **vararg** y el **alcance** de las variables.",
    ],
    cierre=("¡Nos vemos en la Sesión 5!",
            ["Próxima sesión: **POO I — clases, objetos, propiedades y métodos**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya reutilizas con funciones… ¡ahora modela el mundo con OBJETOS!"),
 ),

 5: dict(
    titulo="POO I: clases, objetos, propiedades y métodos",
    subtitulo="Modelar el mundo con clases y objetos",
    archivo="Sesion 5 - POO I - Clases, Objetos, Propiedades y Metodos",
    nivel=2, gancho="¡Modela el mundo con objetos!",
    foco="Definir clases y crear objetos en Kotlin: constructor primario, propiedades val/var, bloque init, métodos, instanciación y this.",
    contenido=[
        ("bullets", "¿Qué es la Programación Orientada a Objetos?", [
            "La POO organiza el programa en @@objetos@@ que representan cosas del mundo (un usuario, un producto).",
            "Cada objeto tiene **datos** (propiedades) y **acciones** (métodos).",
            "Hace el código más ordenado, reutilizable y cercano a la realidad.",
            "Es la base de Android: pantallas, botones y datos son objetos.",
        ]),
        ("bullets", "Una clase es el molde; el objeto, el producto", [
            "Una @@clase@@ define cómo son las cosas de un tipo (el plano/molde).",
            "Un @@objeto@@ es una cosa concreta hecha con ese molde (una instancia).",
            "class Perro es el molde;  firulais y rex son objetos.",
            "De una clase salen **muchos objetos** distintos.",
        ]),
        ("bullets", "Anatomía de una clase", [
            "Constructor primario:  class Persona(val nombre: String, var edad: Int).",
            "**Propiedades**: los datos (val = fijo, var = cambia).",
            "**init { }**: bloque que corre al crear el objeto.",
            "**Métodos**: funciones dentro de la clase (fun saludar()).",
        ]),
        ("bullets", "Crear objetos (instanciar) y this", [
            "Instanciar:  val p = Persona(\"Ana\", 20)  — @@sin new@@ en Kotlin.",
            "Accedes con punto:  p.nombre,  p.saludar().",
            "@@this@@ se refiere al objeto actual dentro de la clase.",
            "Cada objeto guarda **sus propios** valores.",
        ]),
        ("tabla", "Propiedades: val vs var en una clase", ["", "val", "var"], [
            ["¿Se puede cambiar?", "No (solo lectura)", "Sí"],
            ["Ejemplo", "val id", "var saldo"],
            ["Cuándo usarla", "dato fijo (documento)", "dato que cambia (edad, saldo)"],
        ], dict(col_w=[4.0, 4.0, 4.0], note="Mismas reglas que en variables: val por defecto, var solo si el dato cambia.")),
        ("bullets", "El bloque init y los constructores secundarios", [
            "init { } **valida o prepara** datos al crear el objeto.",
            "Ejemplo:  init { require(edad >= 0) }.",
            "Un **constructor secundario** ofrece otra forma de crear el objeto:  constructor(...) : this(...).",
            "El primario es el principal; los secundarios lo complementan.",
        ]),
        ("bullets", "Métodos: el comportamiento del objeto", [
            "Un método es una función que @@pertenece@@ a la clase.",
            "Puede usar las propiedades del objeto.",
            "fun cumplirAnios() { edad++ } modifica el estado.",
            "Se llama sobre el objeto:  p.cumplirAnios().",
        ]),
        ("bullets", "Ejemplo resuelto: clase CuentaBancaria", [
            "class CuentaBancaria(val titular: String, var saldo: Double)",
            "fun depositar(monto: Double) { saldo += monto }",
            "val c = CuentaBancaria(\"Ana\", 0.0);  c.depositar(50.0)",
            "println(c.saldo)  →  50.0.  Este es el @@Taller de hoy@@ (entregable .kt).",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground**: modela una clase (Estudiante o Producto) con al menos 2 propiedades, un constructor primario y 2 métodos.",
        "Crea un objeto en main y usa sus métodos; imprime el estado.",
        ("Verifica con Run.", 1),
        "Entregable en **examlab** (Taller S5, .kt): sube archivo (o enlace) + captura.",
    ],
    logros=[
        "Entendimos **clase vs objeto** (molde vs producto).",
        "Definimos **constructor primario**, **propiedades** e **init**.",
        "Escribimos **métodos** y **instanciamos** objetos con this.",
        "Modelamos una clase real (CuentaBancaria).",
    ],
    cierre=("¡Nos vemos en la Sesión 6!",
            ["Próxima sesión: **POO II — herencia, interfaces y polimorfismo**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya modelas con objetos… ¡ahora reutiliza y EXTIENDE su comportamiento!"),
 ),

 6: dict(
    titulo="POO II: herencia, interfaces y polimorfismo",
    subtitulo="Reutilizar y extender comportamiento",
    archivo="Sesion 6 - POO II - Herencia, Interfaces y Polimorfismo",
    nivel=2, gancho="¡Reutiliza y extiende!",
    foco="Reutilizar y extender comportamiento en Kotlin: herencia (open/override/super), clases abstractas, interfaces, polimorfismo y modificadores de visibilidad.",
    contenido=[
        ("bullets", "Reutilizar y extender: el problema", [
            "Sin herencia, repetirías el mismo código en Perro, Gato, Vaca.",
            "La POO evita repetir: define lo común una vez y @@extiéndelo@@.",
            "Hoy: herencia, interfaces, polimorfismo y visibilidad.",
            "Son los pilares que hacen el código **escalable**.",
        ]),
        ("bullets", "La herencia: open, override y super", [
            "Una clase **hija** @@hereda@@ propiedades y métodos del **padre**.",
            "El padre debe ser open:  class Perro : Animal().",
            "override redefine un método heredado.",
            "super.metodo() llama la versión del padre.",
        ]),
        ("bullets", "Interfaces y clases abstractas", [
            "@@Clase abstracta@@: no se instancia; puede tener código y estado; se hereda (una sola).",
            "@@Interface@@: un contrato de QUÉ hacer; una clase implementa varias.",
            "abstract fun ...  ·  interface { fun ... }.",
            "Interface para 'capacidades'; abstracta para 'es un tipo de'.",
        ]),
        ("bullets", "El polimorfismo", [
            "Polimorfismo = 'muchas formas': una misma llamada, distinto comportamiento.",
            "val a: Animal = Perro();  a.hacerSonido()  →  \"Guau\".",
            "Kotlin usa el método del @@objeto real@@, no del tipo declarado.",
            "Permite tratar objetos distintos de forma uniforme.",
        ]),
        ("bullets", "Modificadores de visibilidad", [
            "@@public@@: visible para todos (por defecto).",
            "@@internal@@: solo el mismo módulo.",
            "@@protected@@: la clase y sus hijas.",
            "@@private@@: solo dentro de la clase. Protege los datos (encapsulación).",
        ]),
        ("tabla", "open, override, abstract: quién es quién", ["Palabra", "Significado"], [
            ["open", "permite que la clase/método se herede o redefina"],
            ["override", "redefine un miembro heredado"],
            ["abstract", "declara sin implementar (obliga a la hija)"],
            ["super", "llama la versión del padre"],
            ["final (por defecto)", "no se puede heredar/redefinir"],
        ], dict(col_w=[3.6, 8.4], note="En Kotlin las clases son final por defecto: hay que abrirlas con open para heredar.")),
        ("bullets", "Interface vs clase abstracta: cuándo cada una", [
            "Una clase implementa @@muchas interfaces@@ pero hereda de @@una sola@@ clase.",
            "Interface: sin estado (por lo general), solo el contrato.",
            "Abstracta: puede compartir código ya hecho y estado.",
            "¿Necesitas 'herencia múltiple' de comportamiento? Usa **interfaces**.",
        ]),
        ("bullets", "Ejemplo resuelto: Animal y sus hijos", [
            "open class Animal { open fun hacerSonido() = \"...\" }",
            "class Perro : Animal() { override fun hacerSonido() = \"Guau\" }",
            "val animales: List<Animal> = listOf(Perro(), Gato())",
            "for (a in animales) println(a.hacerSonido())  →  @@Guau / Miau@@ (polimorfismo).",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground**: crea open class Vehiculo con un método describir(); crea Carro y Moto que hagan **override**.",
        "Guarda varios en una List<Vehiculo> y recórrela llamando describir() (**polimorfismo**).",
        ("Captura la salida mostrando distintos comportamientos.", 1),
        "Entregable en **examlab**: código (o enlace) + captura.",
    ],
    logros=[
        "Aplicamos **herencia** (open, override, super).",
        "Distinguimos **interface** de **clase abstracta**.",
        "Entendimos el **polimorfismo**.",
        "Protegimos datos con **modificadores de visibilidad**.",
    ],
    cierre=("¡Nos vemos en la Sesión 7!",
            ["Próxima sesión: **Data classes, Enums, Nulabilidad y Excepciones**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya extiendes comportamiento… ¡ahora haz tu código a prueba de errores!"),
 ),

 7: dict(
    titulo="Clases de datos, Enums, Nulabilidad y Manejo de Excepciones",
    subtitulo="Modelar datos con seguridad y sin nulos sorpresa",
    archivo="Sesion 7 - Data classes, Enums, Nulabilidad y Excepciones",
    nivel=2, gancho="¡Código a prueba de errores!",
    foco="Modelar datos con seguridad en Kotlin: data classes, enums, nulabilidad (T?, ?., ?:, !!, let) y manejo de excepciones (try/catch/finally).",
    contenido=[
        ("bullets", "El día de las herramientas que dan robustez", [
            "Hoy, 4 herramientas que hacen tu código **seguro y expresivo**.",
            "data class (datos), enum (opciones fijas), nulabilidad (sin nulos sorpresa), excepciones (manejar errores).",
            "Son marca registrada de Kotlin frente a Java.",
            "Te evitan los errores más comunes en apps reales.",
        ]),
        ("bullets", "data class: clases hechas para guardar datos", [
            "data class Persona(val nombre: String, val edad: Int).",
            "Kotlin te @@genera gratis@@ toString(), equals()/hashCode(), copy() y componentN().",
            "toString() imprime bonito; equals compara por **contenido**.",
            "copy() clona cambiando algo:  p.copy(edad = 21).",
        ]),
        ("bullets", "Destructuring: desarmar un objeto", [
            "Una data class permite:  val (nombre, edad) = persona.",
            "Extrae las propiedades en variables de una vez.",
            "Funciona gracias a componentN() (component1, component2...).",
            "Útil al recorrer un Map o retornar varios valores.",
        ]),
        ("bullets", "enum: un conjunto cerrado de valores", [
            "enum class Dia { LUNES, MARTES, ... } fija las **opciones posibles**.",
            "Evita errores de 'strings mágicos' (\"lunes\" mal escrito).",
            "Cada valor puede tener propiedades y métodos.",
            "Combínalo con @@when@@ para cubrir todos los casos.",
        ]),
        ("bullets", "Nulabilidad: el problema del null", [
            "null = 'sin valor'. Es el error #1 en muchos lenguajes (NullPointerException).",
            "Kotlin separa los tipos:  String @@nunca@@ es null;  String? @@puede@@ serlo.",
            "El compilador te **obliga** a manejar el caso null.",
            "Así se evitan los crashes por null en ejecución.",
        ]),
        ("bullets", "Operadores de null: ?., ?: y !!", [
            "@@?.@@ safe call: si es null no explota; devuelve null  (nombre?.length).",
            "@@?:@@ Elvis: da un valor por defecto  (nombre ?: \"Anónimo\").",
            "@@!!@@ not-null: 'confío en que no es null'… o lanza excepción. Úsalo poco.",
            "let: ejecuta un bloque solo si no es null  (nombre?.let { ... }).",
        ]),
        ("bullets", "Manejo de excepciones: try/catch/finally", [
            "Una **excepción** es un error en ejecución (dividir por cero, texto no numérico).",
            "try { } rodea el código que **podría fallar**.",
            "catch (e: Exception) { } reacciona sin que el programa muera.",
            "finally { } corre siempre; throw lanza tu propia excepción.",
        ]),
        ("bullets", "Ejemplo resuelto: parsear un número con seguridad", [
            "val texto = \"abc\"",
            "val n = texto.toIntOrNull() ?: 0  →  0  (Elvis salva del null).",
            "O con try:  try { texto.toInt() } catch (e: NumberFormatException) { 0 }.",
            "Resultado: el programa @@no se cae@@ aunque el dato sea inválido.",
        ]),
    ],
    autonomo=[
        "En **Kotlin Playground**: crea data class Producto(val nombre: String, val precio: Double); crea 2 y usa copy() para variar uno.",
        "Maneja un valor nullable:  val desc: String? = null;  imprime  desc ?: \"Sin descripción\".",
        "Usa try/catch al convertir \"10x\".toInt() y muestra un mensaje amable.",
        ("Captura la salida.", 1),
        "Entregable en **examlab**: código (o enlace) + captura.",
    ],
    logros=[
        "Modelamos datos con **data class** (toString, copy, equals).",
        "Usamos **enum** para conjuntos cerrados de valores.",
        "Manejamos **nulabilidad** con ?., ?: y !! (con cuidado).",
        "Controlamos errores con **try/catch/finally**.",
    ],
    cierre=("¡Nos vemos en la Sesión 8!",
            ["Próxima sesión: **Colecciones — List, Set y Map**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya proteges tu código de errores… ¡ahora maneja MUCHOS datos a la vez!"),
 ),

 8: dict(
    titulo="Colecciones en Kotlin (List, Set, Map)",
    subtitulo="Agrupar y procesar muchos datos",
    archivo="Sesion 8 - Colecciones - List, Set y Map",
    nivel=3, gancho="¡Domina muchos datos!",
    foco="Agrupar y procesar datos con colecciones en Kotlin: List, Set y Map, inmutable vs mutable, acceso por índice/clave y operaciones funcionales (filter, map, forEach).",
    contenido=[
        ("bullets", "¿Por qué colecciones?", [
            "Casi ninguna app maneja UN dato: manejan @@muchos@@ (usuarios, productos, mensajes).",
            "Una **colección** agrupa varios datos bajo un nombre.",
            "Kotlin ofrece List, Set y Map, cada una para un caso.",
            "Sobre ellas aplicas operaciones potentes (filter, map...).",
        ]),
        ("bullets", "List, Set y Map de un vistazo", [
            "@@List@@: ordenada, permite duplicados, acceso por índice [0].",
            "@@Set@@: elementos **únicos**, sin duplicados.",
            "@@Map@@: pares clave → valor (como un diccionario).",
            "Eliges según: ¿orden?, ¿duplicados?, ¿busco por clave?",
        ]),
        ("bullets", "List: crear y acceder", [
            "val frutas = listOf(\"pera\", \"uva\", \"pera\").",
            "Acceso por índice:  frutas[0]  →  \"pera\".",
            ".size (cuántos), .first(), .last(), .contains(\"uva\").",
            "Recorres con  for (f in frutas).",
        ]),
        ("bullets", "Set: elementos únicos", [
            "val ids = setOf(1, 2, 2, 3)  →  {1, 2, 3}  (el duplicado se descarta).",
            "Útil para eliminar repetidos:  lista.toSet().",
            "No garantiza el orden.",
            ".contains() es muy **rápido** en un Set.",
        ]),
        ("bullets", "Map: pares clave-valor", [
            "val edades = mapOf(\"Ana\" to 20, \"Luis\" to 25).",
            "Acceso por clave:  edades[\"Ana\"]  →  20.",
            ".keys, .values, .containsKey(\"Ana\").",
            "Recorres:  for ((nombre, edad) in edades) { ... }.",
        ]),
        ("bullets", "Inmutable vs mutable", [
            "listOf / setOf / mapOf  →  @@solo lectura@@ (no add/remove).",
            "mutableListOf / mutableSetOf / mutableMapOf  →  @@se pueden modificar@@.",
            "En mutables:  .add(),  .remove(),  map[clave] = valor.",
            "Regla: usa **inmutable** por defecto; mutable solo si cambia.",
        ]),
        ("bullets", "Operaciones: filter y map", [
            "@@filter { }@@ deja solo los que cumplen:  nums.filter { it % 2 == 0 }.",
            "@@map { }@@ transforma cada uno:  nums.map { it * 10 }.",
            "it es el **elemento actual** dentro de la lambda.",
            "Se encadenan:  nums.filter { it > 0 }.map { it * 2 }.",
        ]),
        ("tabla", "Operaciones útiles sobre colecciones", ["Operación", "Qué hace", "Ejemplo"], [
            ["size", "cuántos elementos", "lista.size"],
            ["contains", "¿está el elemento?", "lista.contains(x)"],
            ["forEach", "hace algo con cada uno", "lista.forEach { println(it) }"],
            ["filter", "filtra por condición", "lista.filter { it > 0 }"],
            ["map", "transforma cada uno", "lista.map { it.uppercase() }"],
            ["sum / average", "agregan valores", "numeros.sum()"],
        ], dict(col_w=[2.8, 4.2, 5.0], note="filter y map devuelven una NUEVA colección; no modifican la original.")),
    ],
    autonomo=[
        "En **Kotlin Playground**: dada una lista de números, usa **filter** para quedarte con algunos y **map** para transformarlos; imprime el resultado.",
        "Crea un **Map** (nombre → nota) y recórrelo imprimiendo \"nombre: nota\".",
        ("Captura la salida.", 1),
        "Entregable en **examlab** (Taller S8, .kt): archivo (o enlace) + captura.",
    ],
    logros=[
        "Distinguimos **List**, **Set** y **Map** y cuándo usar cada una.",
        "Accedimos por **índice** y por **clave**.",
        "Diferenciamos **inmutable** de **mutable**.",
        "Procesamos datos con **filter**, **map** y **forEach**.",
    ],
    cierre=("¡Nos vemos en la Sesión 9!",
            ["Última sesión: **Kotlin Compose Multiplatform Web (WASM)**.",
             "Avanza tu ruta en **Coursera** y sube tu entregable en **examlab**."],
            "Ya procesas muchos datos… ¡ahora salta de la consola a la PANTALLA!"),
 ),

 9: dict(
    titulo="Kotlin Compose Multiplatform Web (WASM)",
    subtitulo="De la consola a una interfaz multiplataforma",
    archivo="Sesion 9 - Kotlin Compose Multiplatform Web (WASM)",
    nivel=3, gancho="¡De la consola a la pantalla!",
    foco="Comprender (a nivel conceptual) Compose Multiplatform y su objetivo Web con WebAssembly (WASM): funciones @Composable, UI declarativa y la diferencia con Kotlin puro en Playground.",
    contenido=[
        ("bullets", "De la consola a la interfaz gráfica", [
            "Hasta hoy: programas de @@consola@@ (entra/sale texto con println).",
            "Las apps reales tienen @@interfaz gráfica@@: botones, textos, imágenes.",
            "Hoy vemos cómo Kotlin salta a interfaces con **Compose Multiplatform**.",
            "Sesión **demostrativa**/conceptual: no se evalúa código nuevo.",
        ]),
        ("bullets", "Qué es Compose Multiplatform", [
            "Compose Multiplatform (JetBrains) crea interfaces con **Kotlin**.",
            "Una @@sola UI@@ que corre en Android, iOS, Desktop y Web.",
            "Nace de **Jetpack Compose** (el estándar de UI de Android).",
            "Menos código repetido para varias plataformas.",
        ]),
        ("bullets", "El objetivo Web con WebAssembly (WASM)", [
            "WebAssembly (WASM) es un formato que el navegador ejecuta @@casi a velocidad nativa@@.",
            "Kotlin/Wasm compila tu Compose a WASM.",
            "Resultado: una app **gráfica** Kotlin corriendo en el navegador.",
            "Es tecnología nueva (en evolución), pero muy prometedora.",
        ]),
        ("bullets", "Qué es una función @Composable", [
            "Una función marcada con @@@Composable@@ describe un trozo de interfaz.",
            "@Composable fun Saludo() { Text(\"Hola\") }.",
            "Se combinan como piezas de Lego para armar la pantalla.",
            "Devuelven **UI**, no texto de consola.",
        ]),
        ("bullets", "UI declarativa: describir, no dibujar paso a paso", [
            "@@Declarativa@@: describes cómo debe verse la UI según el **estado**.",
            "Cuando el estado cambia, la UI se @@redibuja sola@@.",
            "Frente a lo imperativo (actualizar cada widget a mano).",
            "Menos errores y código más claro.",
        ]),
        ("tabla", "Kotlin en Playground vs Compose Web", ["", "Kotlin Playground", "Compose Web"], [
            ["Tipo de programa", "consola (texto)", "interfaz gráfica"],
            ["Dónde corre", "navegador (compila en servidor)", "navegador (WASM)"],
            ["Herramienta", "play.kotlinlang.org", "Android Studio / IntelliJ"],
            ["En este curso", "práctica de S1–S8", "demostración de hoy"],
        ], dict(col_w=[3.4, 4.6, 4.0], note="Compose Web y Android Studio quedan FUERA de examlab: son demostrativos/online.")),
        ("bullets", "El puente: lo que aprendiste sigue vivo", [
            "Variables, funciones, clases, colecciones… @@todo se usa@@ en Compose.",
            "Un @Composable es una función; el estado son variables; las listas se pintan con colecciones.",
            "Kotlin es el mismo; cambia el 'para qué' (UI en vez de consola).",
            "Lo de este curso es el cimiento de **Desarrollo de Aplicaciones Móviles 2**.",
        ]),
        ("bullets", "Recapitulación del curso completo", [
            "**Fundamentos**: variables, tipos, condicionales, bucles, funciones.",
            "**POO**: clases, objetos, herencia, interfaces, polimorfismo.",
            "**Robustez**: data class, enum, nulabilidad, excepciones, colecciones.",
            "Y el @@futuro@@: interfaces con Compose Multiplatform Web.",
        ]),
    ],
    autonomo=[
        "Sube la **evidencia** de un mini-programa Kotlin del curso: enlace público de **Kotlin Playground** (o repositorio) + captura.",
        "Escribe una breve explicación: ¿qué conceptos del curso aplicaste?",
        ("Demostrativo (no se evalúa código): explora una demo de Compose Web en el navegador. Android Studio y Compose quedan fuera de examlab.", 1),
        "Entregable en **examlab** (Proyecto S9, abierta): enlace/captura + explicación.",
    ],
    logros=[
        "Entendimos qué es **Compose Multiplatform** y su objetivo Web (WASM).",
        "Distinguimos **@Composable** y la **UI declarativa**.",
        "Vimos la diferencia entre Kotlin de **consola** (Playground) y **Compose Web**.",
        "Cerramos el recorrido: de los fundamentos a la interfaz.",
    ],
    cierre=("¡Felicitaciones, terminaste el curso!",
            ["Completa tu **ruta en Coursera** dentro del plazo y responde la **encuesta de satisfacción**.",
             "De la consola a la interfaz: ya tienes la base para crear apps móviles."],
            "Este es el punto de partida de tu carrera como desarrollador Kotlin."),
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
        "**Sesiones teórico-prácticas**: cada clase combina teoría, modelación y práctica en Kotlin Playground.",
        "Momentos por clase:",
        ("**Motivación**: preguntas y ejemplos que generan interés y conexión.", 1),
        ("**Encuadre**: explicación de objetivos, ruta de aprendizaje y acuerdos.", 1),
        ("**Modelación**: código guiado que muestra conceptos y técnicas.", 1),
        ("**Simulación**: trabajo en grupos pequeños para aplicar conceptos.", 1),
        ("**Ejercitación**: práctica individual en Kotlin Playground.", 1),
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
        "**Curso base (Coursera):** [confirmar el curso base de Kotlin en Coursera]",
        ("[URL del curso base — confirmar con coordinación]", 1),
        "**Escribe y ejecuta Kotlin:** Kotlin Playground",
        ("https://play.kotlinlang.org/", 1),
        "**Documentación oficial de Kotlin:**",
        ("https://kotlinlang.org/docs/home.html", 1),
        "**Guías, quizzes y ruta de aprendizaje:** en examlab",
        ("https://examlab.lovable.app/app", 1),
    ], size=14, idx=8)
    content_slide(prs, "HERRAMIENTAS", [
        "**En examlab** (plataforma del curso · https://examlab.lovable.app/app):",
        ("Test (quizzes de conceptos) · Reto en vivo (Kahoot) · Taller/Proyecto (entrega de .kt). examlab NO ejecuta Kotlin.", 1),
        "**Solo online (gratuitas):**",
        ("Kotlin Playground (play.kotlinlang.org) para escribir y ejecutar Kotlin · documentación kotlinlang.org.", 1),
        "**En el mundo laboral** (lo que usarás en el trabajo):",
        ("Android Studio · Jetpack Compose · Gradle · Git/GitHub · emuladores y dispositivos Android.", 1),
    ], size=14, idx=9)
    content_slide(prs, "¡ IMPORTANTE !", [
        "La **ruta de Coursera** es el **90%** de la nota: completa tu progreso a tiempo (licencias activas hasta el día hábil posterior al fin del curso).",
        "La programación de Kotlin se hace en **Kotlin Playground** (examlab no ejecuta Kotlin); los quizzes de código son de **lectura** (\"¿qué imprime?\").",
        "Las **notas** se cargan hasta **una semana** después de la última clase; hay **3 días** para reclamaciones por correo.",
        "Responde la **encuesta de satisfacción** el último día del curso (sáb. 15-ago).",
    ], size=15, idx=10)
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
    build_presentacion()
    for n in SESIONES:
        build_sesion(n)
    print("LISTO: 10 decks generados (presentación + 9 sesiones).")
