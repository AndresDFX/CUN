# -*- coding: utf-8 -*-
"""
Genera los 10 decks .pptx del curso DESARROLLO DE APLICACIONES WEB (FESNA) — v2 (material NUEVO).
Presentación del curso + 9 sesiones. Identidad Nueva América (motor fesna_slides_engine.py):
foto lavada en portadas, objetivos con foto duotono azul, gestores con flyer real,
naranja #FD531E solo para resaltar, escala de grises, tipografía Barlow.

Front-end: JavaScript + DOM (S1–S3) y React + Hooks + Redux (S4–S9).
Config: config/cursos/desarrollo-aplicaciones-web.json
Evaluación REAL: Coursera 90% + Asistencia 10% + bono Kahoot (opcional).
Práctica examlab: Tier 1 (editor de código JS de consola) para lógica pura; DOM en CodePen y
React en CodeSandbox (Tier 2); entregable como Taller/Proyecto en examlab.

Salida (dentro de Clases/Version vigente (nuevo dictado 2026)/):
  Clases/Version vigente (nuevo dictado 2026)/Presentacion del curso.pptx
  Clases/Version vigente (nuevo dictado 2026)/Sesion N/Sesion N - <Titulo>.pptx
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fesna_slides_engine import *

DIAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "diagramas")

def diag(diag_id):
    """Ruta del PNG del diagrama si existe (para las diapositivas mixtas)."""
    if not diag_id:
        return None
    p = os.path.join(DIAG_DIR, diag_id + ".png")
    return p if os.path.exists(p) else None

BASE = r"g:\Mi unidad\Trabajos\Empleo\FESNA\Cursos\Desarrollo de Aplicaciones Web\Clases\Version vigente (nuevo dictado 2026)"
CURSO = "Desarrollo de Aplicaciones Web"
PROGRAMA = "Ingeniería de Sistemas"
EXAMLAB = "https://examlab.lovable.app/app"

TUTOR = ("Julián Andrés Castaño Espinosa",
         ["Líder Técnico", "Ingeniero de Sistemas", "Candidato a MsC en IA"],
         "julian.castano@lanuevaamerica.edu.co")

OBJETIVOS_CURSO = [
    "Manipular el DOM con JavaScript puro —variables, tipos, funciones, eventos y estructuras de datos— para construir páginas interactivas del lado del cliente.",
    "Construir interfaces con React: componentes reutilizables, props, estado con useState y consumo de APIs con useEffect.",
    "Integrar formularios con validación y centralizar el estado global de la aplicación con Redux, aplicando las buenas prácticas actuales del front-end.",
]

# --- Evaluación REAL del curso (Coursera 90% + Asistencia 10%). NO el 50/40/10 por defecto. ---
EVAL_ROWS = [
    ["**Progreso en Coursera** — ruta de aprendizaje de los cursos base", "@@90%@@"],
    ["**Asistencia** — al final de la sesión", "@@10%@@"],
    ["**Total**", "**100%**"],
]
EVAL_NOTE = ("Participación en clase = **+0.3** (opcional)  ·  Reto en vivo (Kahoot): 🥇 **+0.5** · 🥈 **+0.4** · 🥉 **+0.3** (opcional).  "
             "Los Test y Talleres de examlab son de refuerzo/formativos.")

NIVELES = {
    1: "Nivel 1 — DOM con JavaScript",
    2: "Nivel 2 — Interfaces con React",
    3: "Nivel 3 — Formularios y Redux",
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
        "Repasa con el **Test de la sesión en examlab**; la práctica va en @@el editor de código de examlab o en CodePen/CodeSandbox@@ y el link se adjunta en el Taller.",
    ], size=15, idx=idx)


# ============================== SESIONES ==============================
# contenido: ("bullets", titulo, items[, diag_id])  ó  ("tabla", titulo, headers, rows, extra_dict)
SESIONES = {
 1: dict(
    titulo="Introducción a JavaScript y manipulación del DOM",
    subtitulo="El lenguaje de la web y cómo cambiar la página en vivo",
    archivo="Sesion 1 - Introduccion a JavaScript y manipulacion del DOM",
    nivel=1, gancho="¡Que la página cobre vida!",
    foco="Comprender qué es JavaScript, escribir código con variables, tipos y funciones, y realizar las primeras manipulaciones del DOM: seleccionar y cambiar elementos de la página.",
    contenido=[
        ("bullets", "¿Qué es JavaScript y dónde corre?", [
            "JavaScript es el **lenguaje de la web**: HTML es la estructura, CSS el estilo y @@JavaScript el comportamiento@@.",
            "Corre **dentro del navegador** (Chrome, Firefox…), en un motor de JS; no hay que instalar nada para probarlo.",
            "Se incluye con `<script>` interno o `<script src=\"app.js\">` (archivo externo).",
            "También corre fuera del navegador con **Node.js** (servidores y herramientas).",
            "Es **interpretado** y de **tipado dinámico**: no declaras el tipo de las variables.",
        ], "web_s1_dom_mock"),
        ("bullets", "Variables y tipos primitivos", [
            "`let` para lo que cambia, `const` para lo constante — usa @@const por defecto@@; evita `var`.",
            "Tipos primitivos: **string** (\"texto\"), **number** (10, 3.14), **boolean** (true/false), **null** y **undefined**.",
            "`typeof x` te dice el tipo de un valor.",
            "JavaScript **convierte tipos** solo (coerción): por eso `\"5\" + 1` da `\"51\"` (concatena).",
        ]),
        ("bullets", "Operadores, template literals e igualdad", [
            "Aritméticos (`+ - * / %`), de comparación (`> < >= <=`) y lógicos (`&& || !`).",
            "**Template literals** con backticks: `` `Hola ${nombre}, tienes ${edad}` ``.",
            "@@Usa siempre `===`: compara valor Y tipo.@@ `==` convierte tipos antes (traicionero).",
            "Ejemplo: `0 == \"\"` es `true`, pero `0 === \"\"` es `false`.",
        ]),
        ("bullets", "Funciones y console.log", [
            "Una función **agrupa instrucciones** reutilizables: recibe **parámetros** y devuelve un valor con `return`.",
            "Declaración: `function suma(a, b) { return a + b; }`.",
            "También como expresión / arrow (lo veremos a fondo en S3–S4).",
            "@@`console.log(...)` imprime en la consola@@ (F12 en el navegador, o el editor de examlab): tu mejor herramienta para depurar.",
        ]),
        ("bullets", "¿Qué es el DOM?", [
            "El **DOM** (Document Object Model) es el **árbol de nodos** que el navegador construye a partir del HTML.",
            "Cada etiqueta HTML es un **nodo**; los nodos se anidan como ramas de un árbol.",
            "`document` es la **raíz**: la puerta de entrada a toda la página desde JavaScript.",
            "Cambiar el DOM = @@cambiar la página en vivo, sin recargar@@.",
        ], "dom_tree"),
        ("bullets", "Seleccionar elementos del DOM", [
            "`document.getElementById(\"id\")` — un elemento por su id.",
            "`document.querySelector(\"selector CSS\")` — el **primer** elemento que coincide (`.clase`, `#id`, `div`).",
            "`document.querySelectorAll(\"...\")` — **todos** los que coinciden (una lista para recorrer).",
            "Guarda el resultado en una variable: `const titulo = document.querySelector(\"h1\");`.",
        ]),
        ("bullets", "Cambiar contenido, estilos y atributos", [
            "`elemento.textContent = \"...\"` — cambia el **texto** (seguro).",
            "`elemento.innerHTML = \"<b>...</b>\"` — inserta **HTML** (potente, pero riesgo de XSS con datos del usuario).",
            "`elemento.style.color = \"red\"` — estilos; `elemento.setAttribute(\"src\", \"...\")` — atributos.",
            "`elemento.classList.add/remove/toggle(\"clase\")` — maneja clases CSS.",
        ], "text_vs_html"),
        ("bullets", "Crear e insertar nodos nuevos", [
            "`document.createElement(\"li\")` — crea un nodo (aún NO está en la página).",
            "Le pones contenido: `nuevo.textContent = \"Item\";`.",
            "`padre.appendChild(nuevo)` — lo **inserta** como hijo → aparece en pantalla.",
            "Así se construyen listas, tarjetas y todo el @@contenido dinámico@@.",
        ]),
    ],
    autonomo=[
        "**Tier 1 — editor de código JavaScript de examlab** (" + EXAMLAB + "): declara `const nombre` y `let edad`, imprime un saludo con **template literals** y escribe una función `esMayor(edad)` que devuelva true/false.",
        "**Tier 2 — CodePen** (codepen.io): en un HTML con un `<h1>` y un `<button>`, usa `querySelector` y cambia el `textContent` del `<h1>` (adelanto de eventos de la S2).",
        "**Criterio de éxito:** la consola imprime el saludo correcto y el `<h1>` muestra el texto nuevo.",
        "**Entregable:** pega el **link de tu CodePen** en el **Taller S1 de examlab** y adjunta el pantallazo de la consola.",
    ],
    logros=[
        "Entendimos **qué es JavaScript** y dónde se ejecuta.",
        "Usamos **variables, tipos, operadores y funciones** con `console.log`.",
        "Descubrimos el **DOM** como árbol de nodos de la página.",
        "**Seleccionamos y cambiamos** elementos, y creamos nodos nuevos.",
    ],
    cierre=("¡Nos vemos en la Sesión 2!",
            ["Próxima sesión: **Eventos del usuario y programación interactiva**.",
             "Sube tu **CodePen** al Taller S1 en examlab."],
            "Ya cambiamos la página… ¡ahora haremos que responda al usuario!"),
 ),

 2: dict(
    titulo="Eventos del usuario y programación interactiva",
    subtitulo="Hacer que la página responda a clics, tecleo y formularios",
    archivo="Sesion 2 - Eventos del usuario y programacion interactiva",
    nivel=1, gancho="¡Tu página, a la escucha!",
    foco="Manejar el modelo de eventos del navegador: registrar handlers con addEventListener, leer el objeto event y responder a la interacción del usuario cambiando el DOM.",
    contenido=[
        ("bullets", "¿Qué es un evento?", [
            "Un **evento** es algo que ocurre en la página: un **clic**, una **tecla**, mover el ratón, enviar un formulario…",
            "El navegador **avisa** cuando pasa; tu código decide **cómo responder**.",
            "Programar con eventos = **programación dirigida por eventos**: no controlas *cuándo* pasa, sino *qué hacer* cuando pasa.",
            "Esto convierte una página estática en una @@aplicación interactiva@@.",
        ]),
        ("bullets", "addEventListener: el modelo de eventos", [
            "`elemento.addEventListener(\"click\", handler)` — conecta un evento con una función.",
            "El **handler** (o callback) es la función que se ejecuta cuando ocurre el evento.",
            "`removeEventListener(\"click\", handler)` — quita el escucha (usa la MISMA referencia de función).",
            "Puedes tener **varios handlers** para el mismo evento en el mismo elemento.",
        ], "evento_flujo"),
        ("bullets", "El objeto event", [
            "El handler recibe un objeto **event** con la info de lo que pasó.",
            "`event.target` — el elemento que disparó el evento.",
            "`event.type` — el tipo (\"click\", \"input\"…).",
            "@@`event.preventDefault()`@@ — cancela la acción por defecto (p. ej. que el formulario recargue la página).",
        ]),
        ("tabla", "Eventos comunes del navegador", ["Evento", "Cuándo ocurre", "Uso típico"], [
            ["**click**", "Clic sobre un elemento", "Botones, enlaces"],
            ["**input**", "El valor de un campo cambia (cada tecla)", "Búsqueda en vivo"],
            ["**change**", "El campo pierde foco tras cambiar", "Selects, checkboxes"],
            ["**submit**", "Se envía un formulario", "Validar antes de enviar"],
            ["**keydown**", "Se presiona una tecla", "Atajos de teclado"],
            ["**mouseover**", "El ratón entra en el elemento", "Efectos al pasar el cursor"],
        ], dict(col_w=[2.6, 5.4, 4.0], note="Con `submit` casi siempre llamarás a `event.preventDefault()` para manejar el envío con JavaScript.")),
        ("bullets", "Handlers y callbacks", [
            "El handler puede ser una **función con nombre**, una **anónima** o una **arrow**:",
            ("`btn.addEventListener(\"click\", () => { ... })`", 1),
            "**No** pongas los paréntesis al pasarla (`handler`, no `handler()`): pasas la función, no su resultado.",
            "Dentro del handler tienes acceso al `event` y al DOM para responder.",
        ]),
        ("bullets", "Leer valores del usuario y responder", [
            "`input.value` — lee lo que el usuario escribió en un campo.",
            "Patrón típico: **escucho un evento → leo un valor → cambio el DOM**.",
            "Ejemplo: al escribir en un buscador (`input`), filtro una lista y actualizo la pantalla.",
            "Ejemplo: al hacer `click`, agrego un `<li>` a una lista de tareas.",
        ]),
        ("bullets", "Propagación de eventos (bubbling)", [
            "Cuando haces clic en un elemento, el evento **'burbujea'** hacia sus ancestros: botón → div → body → document.",
            "Por eso un handler en un contenedor puede 'escuchar' clics de sus hijos (**delegación de eventos**).",
            "`event.stopPropagation()` detiene el burbujeo si no lo quieres.",
            "Es una noción introductoria: por ahora, @@basta saber que el evento sube por el árbol@@.",
        ], "bubbling"),
    ],
    autonomo=[
        "**Tier 2 — CodePen** (" + EXAMLAB + " para el entregable): construye una **lista de tareas (to-do)** mínima.",
        ("Un `<input>` y un botón **Agregar**: al hacer `click`, lee `input.value` y agrega un `<li>` con `createElement` + `appendChild`.", 1),
        ("Al hacer clic en un `<li>`, márcalo como hecho (`classList.toggle`).", 1),
        "**Criterio de éxito:** puedo agregar tareas y marcarlas; el `<input>` se limpia tras agregar.",
        "**Entregable:** pega el **link de CodePen** en el **Taller S2 de examlab** + pantallazo.",
    ],
    logros=[
        "Entendimos el **modelo de eventos** del navegador.",
        "Registramos handlers con **addEventListener** y usamos el objeto **event**.",
        "**Leímos valores** del usuario y cambiamos el DOM en respuesta.",
        "Vimos la **propagación (bubbling)** a nivel introductorio.",
    ],
    cierre=("¡Nos vemos en la Sesión 3!",
            ["Próxima sesión: **Arreglos y bucles en JavaScript** (lógica de datos).",
             "Sube tu **to-do** al Taller S2 en examlab."],
            "La página ya reacciona… ¡ahora organicemos los datos!"),
 ),

 3: dict(
    titulo="Estructuras de datos: Arreglos y bucles en JavaScript",
    subtitulo="Guardar, recorrer y transformar colecciones de datos",
    archivo="Sesion 3 - Arreglos y bucles en JavaScript",
    nivel=1, gancho="¡Domina tus datos!",
    foco="Manejar arreglos y objetos, recorrerlos con bucles y transformarlos con los métodos funcionales (map, filter, reduce) usando lógica pura, sin DOM.",
    contenido=[
        ("bullets", "Arreglos: qué son y cómo se usan", [
            "Un **arreglo** guarda varios valores en orden: `const frutas = [\"pera\", \"uva\", \"kiwi\"];`.",
            "Se accede por **índice**, empezando en @@0@@: `frutas[0]` es `\"pera\"`.",
            "`frutas.length` — cuántos elementos hay.",
            "Pueden guardar cualquier tipo, incluso otros arreglos u objetos.",
        ], "array_indices"),
        ("tabla", "Métodos para agregar y quitar", ["Método", "Qué hace", "Dónde"], [
            ["**push(x)**", "Agrega al final", "final"],
            ["**pop()**", "Quita y devuelve el último", "final"],
            ["**unshift(x)**", "Agrega al inicio", "inicio"],
            ["**shift()**", "Quita y devuelve el primero", "inicio"],
            ["**indexOf(x)**", "Posición de x (−1 si no está)", "—"],
            ["**includes(x)**", "¿Contiene x? (true/false)", "—"],
        ], dict(col_w=[2.8, 5.6, 3.6], note="push/pop/shift/unshift **mutan** el arreglo original. Ojo con eso cuando trabajemos con estado en React (S6).")),
        ("bullets", "Bucles: recorrer los datos", [
            "**for clásico**: `for (let i = 0; i < arr.length; i++) { ... }` — control total del índice.",
            "**while**: repite **mientras** una condición sea verdadera.",
            "**for...of**: `for (const item of arr) { ... }` — recorre los **valores** (más limpio).",
            "Usa `for...of` cuando solo necesitas los valores; `for` clásico cuando necesitas el índice.",
        ]),
        ("bullets", "Métodos funcionales: map, filter, reduce", [
            "**map**: transforma cada elemento y devuelve un **arreglo nuevo** del mismo tamaño.",
            "**filter**: conserva los que cumplen una condición → arreglo (posiblemente) más corto.",
            "**reduce**: combina todo en **un solo valor** (suma, total, objeto…).",
            "@@Los tres NO mutan el original: devuelven uno nuevo.@@ Serán clave en React.",
        ], "map_filter_reduce"),
        ("bullets", "forEach vs map (una confusión común)", [
            "**forEach** ejecuta algo por cada elemento pero **no devuelve nada** (undefined).",
            "**map** transforma y **devuelve** un arreglo nuevo.",
            "Si necesitas el resultado transformado → `map`. Si solo quieres recorrer → `forEach`.",
            "@@Regla:@@ no uses `map` si vas a ignorar lo que devuelve.",
        ], "foreach_vs_map"),
        ("bullets", "Objetos y arreglos de objetos", [
            "Un **objeto** agrupa datos con nombre: `const u = { nombre: \"Ana\", edad: 20 };`.",
            "Se accede con punto: `u.nombre`, o con corchetes: `u[\"nombre\"]`.",
            "Muy común: **arreglos de objetos**, `[{id:1,...}, {id:2,...}]` — así llegan los datos de una API.",
            "Combina: `usuarios.filter(u => u.edad >= 18).map(u => u.nombre)`.",
        ]),
        ("bullets", "Funciones y arrow functions", [
            "Una **arrow function** es una forma corta de escribir funciones: `const doble = n => n * 2;`.",
            "Si el cuerpo es una sola expresión, **devuelve** su valor sin `return`.",
            "Encajan perfecto como argumento de map/filter/reduce.",
            "Las usaremos todo el tiempo en React (S4 en adelante).",
        ]),
    ],
    autonomo=[
        "**Tier 1 — 100% en el editor de código JavaScript de examlab** (" + EXAMLAB + "):",
        ("Dado `const ventas = [120, 340, 55, 900, 210];`, imprime con `console.log`:", 1),
        ("el total (`reduce`), las ventas mayores a 200 (`filter`) y las mismas con IVA del 19% (`map`).", 1),
        "**Criterio de éxito:** la consola muestra el total, el arreglo filtrado y el arreglo con IVA correctos.",
        "**Entregable:** resuélvelo en el **Taller S3 (preguntas tipo `código`, JavaScript)** de examlab — calificable en la plataforma.",
    ],
    logros=[
        "Creamos y manipulamos **arreglos** (push/pop, índice, length).",
        "Recorrimos datos con **for, while y for...of**.",
        "Transformamos con **map, filter y reduce** sin mutar el original.",
        "Trabajamos **objetos y arreglos de objetos** con arrow functions.",
    ],
    cierre=("¡Nos vemos en la Sesión 4!",
            ["Próxima sesión: **Introducción a React, ES6 y JSX**.",
             "Completa el **Taller S3** en examlab."],
            "Ya dominas los datos… ¡ahora saltamos a React!"),
 ),

 4: dict(
    titulo="Introducción a React, ES6 y sintaxis JSX",
    subtitulo="De manipular el DOM a describir la UI por componentes",
    archivo="Sesion 4 - Introduccion a React ES6 y JSX",
    nivel=2, gancho="¡Bienvenido a React!",
    foco="Entender qué problema resuelve React frente a JS + DOM manual, dominar el ES6 esencial y escribir tu primer componente con la sintaxis JSX.",
    contenido=[
        ("bullets", "¿Qué problema resuelve React?", [
            "Con JS + DOM manual, mantener una UI grande es **frágil**: mil `querySelector` y `appendChild`.",
            "React es **declarativo**: describes @@cómo se ve la UI@@ y él actualiza el DOM por ti.",
            "La UI se arma con **componentes** reutilizables (piezas de interfaz).",
            "Usa un **DOM virtual** para actualizar solo lo que cambió (eficiente).",
        ], "dom_vs_react"),
        ("bullets", "ES6 esencial (I): arrow, destructuring", [
            "**Arrow functions**: `const suma = (a, b) => a + b;`.",
            "**Destructuring** de objetos: `const { nombre, edad } = usuario;`.",
            "**Destructuring** de arreglos: `const [primero, segundo] = lista;`.",
            "React usa estos patrones **por todas partes** (props, hooks…).",
        ]),
        ("bullets", "ES6 esencial (II): spread, rest, módulos", [
            "**Spread** `...`: copia/combina: `const nuevo = [...viejo, x];` · `{ ...obj, edad: 21 }`.",
            "**Rest** `...`: agrupa argumentos: `function f(...args) { }`.",
            "**Módulos**: `export` lo que compartes e `import` lo que usas.",
            ("`import Boton from \"./Boton\";`", 1),
            "@@Spread será clave para NO mutar el estado@@ (S6).",
        ]),
        ("bullets", "¿Qué es JSX?", [
            "**JSX** es escribir algo parecido a HTML **dentro de** JavaScript.",
            "El navegador no lo entiende: **Babel lo transpila** a llamadas `React.createElement`.",
            "Dentro de JSX, las **expresiones** van entre llaves: `<h1>Hola {nombre}</h1>`.",
            "No es HTML: es azúcar sintáctico que produce JavaScript.",
        ], "jsx_transpila"),
        ("tabla", "Reglas de JSX (HTML no es igual)", ["Regla", "HTML", "JSX"], [
            ["Un solo nodo raíz", "varios sueltos", "envuélvelos (o `<>…</>` Fragment)"],
            ["Clase CSS", "`class=\"...\"`", "`className=\"...\"`"],
            ["Atributos compuestos", "`onclick`, `tabindex`", "`onClick`, `tabIndex` (camelCase)"],
            ["Etiquetas vacías", "`<br>`", "`<br />` (autocierre)"],
        ], dict(col_w=[3.4, 3.4, 5.2], note="`class` es palabra reservada en JS → por eso `className`. Los eventos van en camelCase: `onClick`, `onChange`.")),
        ("bullets", "Tu primer componente funcional", [
            "Un **componente** es una función que **retorna JSX**.",
            "Su nombre va en **Mayúscula**: `function Saludo() { return <h1>Hola</h1>; }`.",
            "Se usa como una etiqueta: `<Saludo />`.",
            "Componer componentes = armar la UI como un **árbol** de piezas.",
        ], "web_s4_primer_componente"),
        ("bullets", "Entorno sin instalar nada", [
            "**CodeSandbox** (codesandbox.io) y **StackBlitz**: proyectos React en el navegador, sin configurar nada.",
            "Elige la plantilla **React** y ya tienes `App.js` listo.",
            "En el trabajo real usarás **Vite** o Create React App + Node.js + VS Code.",
            "Para el curso: @@CodeSandbox para React@@; el entregable se adjunta en examlab.",
        ]),
    ],
    autonomo=[
        "**Tier 1 — editor de código JS de examlab** (" + EXAMLAB + "): practica **ES6 puro**: crea un objeto `usuario`, desestructúralo, combina dos arreglos con **spread** y escribe una **arrow function**; imprime todo con `console.log`.",
        "**Tier 2 — CodeSandbox**: crea un componente `<Tarjeta />` que muestre tu nombre y un rol en un `<div>`, y úsalo dentro de `<App />`.",
        "**Criterio de éxito:** la consola muestra los resultados de ES6 y CodeSandbox renderiza tu tarjeta.",
        "**Entregable:** pega el **link de CodeSandbox** en el **Taller S4 de examlab** + pantallazo de la consola.",
    ],
    logros=[
        "Entendimos **qué resuelve React** frente al DOM manual.",
        "Practicamos el **ES6 esencial**: arrow, destructuring, spread/rest, módulos.",
        "Aprendimos **qué es JSX** y sus reglas.",
        "Escribimos nuestro **primer componente** en CodeSandbox.",
    ],
    cierre=("¡Nos vemos en la Sesión 5!",
            ["Próxima sesión: **Componentes y Props: paso de datos**.",
             "Sube tu **CodeSandbox** al Taller S4 en examlab."],
            "Ya tienes componentes… ¡ahora aprendamos a pasarles datos!"),
 ),

 5: dict(
    titulo="Componentes en React: Props y paso de datos",
    subtitulo="Reutilizar piezas de UI y pasarles información",
    archivo="Sesion 5 - Componentes en React Props y paso de datos",
    nivel=2, gancho="¡Componentes que hablan!",
    foco="Componer componentes reutilizables y pasarles datos con props (flujo unidireccional), desestructurando props y renderizando listas con la prop key.",
    contenido=[
        ("bullets", "Componentes reutilizables y composición", [
            "Un componente bien hecho hace **una sola cosa** y se reutiliza (`<Boton />`, `<Tarjeta />`).",
            "**Composición**: componentes dentro de componentes → la UI es un **árbol**.",
            "`<App>` contiene `<Lista>`, que contiene muchos `<Item>`.",
            "Componer > duplicar: cambias una pieza y se refleja en todos lados.",
        ], "props_flujo"),
        ("bullets", "Props: pasar datos de padre a hijo", [
            "Las **props** son los **argumentos** de un componente: `<Saludo nombre=\"Ana\" />`.",
            "El hijo las recibe como un objeto: `function Saludo(props) { return <h1>Hola {props.nombre}</h1>; }`.",
            "@@Las props son de SOLO LECTURA:@@ el hijo NO las modifica.",
            "Datos que cambian por dentro → eso es **estado** (S6), no props.",
        ]),
        ("bullets", "Desestructurar props y valores por defecto", [
            "En vez de `props.nombre`, desestructura en el parámetro: `function Saludo({ nombre }) { ... }`.",
            "Valor por defecto: `function Saludo({ nombre = \"invitado\" }) { ... }`.",
            "Queda más limpio y se ve de un vistazo qué props espera el componente.",
            "Puedes pasar cualquier tipo: strings, números, arreglos, objetos, **funciones**.",
        ]),
        ("bullets", "props.children", [
            "Lo que pongas **entre** las etiquetas llega como `props.children`:",
            ("`<Tarjeta><p>Contenido</p></Tarjeta>`", 1),
            "Dentro de `Tarjeta`: `function Tarjeta({ children }) { return <div class...>{children}</div>; }`.",
            "Ideal para **envoltorios** (cards, modales, layouts) que rodean contenido variable.",
        ]),
        ("bullets", "Renderizar listas con map y key", [
            "Para pintar una lista, **mapea** los datos a JSX: `items.map(i => <li>{i}</li>)`.",
            "Cada elemento necesita una prop **`key`** única: `<li key={i.id}>{i.texto}</li>`.",
            "@@La key ayuda a React a saber qué cambió@@ y actualizar solo eso (rendimiento y correctitud).",
            "No uses el índice como key si la lista se reordena o filtra.",
        ]),
        ("bullets", "Flujo de datos unidireccional", [
            "Los datos fluyen **de arriba hacia abajo** (top-down): del padre al hijo por props.",
            "El hijo **no** puede cambiar las props del padre.",
            "Para 'avisar hacia arriba', el padre pasa una **función** como prop y el hijo la llama.",
            "Este flujo predecible hace la app **fácil de razonar**.",
        ], "flujo_unidireccional"),
        ("tabla", "Props vs Estado (adelanto de S6)", ["", "Props", "Estado (state)"], [
            ["¿Quién lo controla?", "El padre", "El propio componente"],
            ["¿Se puede cambiar?", "No (solo lectura)", "Sí (con su setter)"],
            ["¿Para qué?", "Configurar / pasar datos", "Datos que cambian en el tiempo"],
        ], dict(col_w=[3.6, 4.2, 4.2], note="Regla: si un dato **cambia por interacción**, será estado; si solo se **recibe**, es prop.")),
    ],
    autonomo=[
        "**Tier 2 — CodeSandbox** (" + EXAMLAB + " para entregar): crea un componente `<TarjetaProducto />` que reciba por **props** `nombre`, `precio` e `imagen`.",
        ("En `<App />` define un arreglo de 3 productos y **renderízalos con `map`**, pasando `key`.", 1),
        "**Criterio de éxito:** se ven 3 tarjetas distintas; no hay warning de `key` en la consola.",
        "**Entregable:** pega el **link de CodeSandbox** en el **Taller S5 de examlab**. Opcional: dibuja el árbol de componentes en la **pizarra/Mermaid de examlab**.",
    ],
    logros=[
        "Compusimos **componentes reutilizables**.",
        "Pasamos datos con **props** (de solo lectura) y las desestructuramos.",
        "Usamos **props.children** para envoltorios.",
        "Renderizamos **listas con map y key** y entendimos el flujo unidireccional.",
    ],
    cierre=("¡Nos vemos en la Sesión 6!",
            ["Próxima sesión: **Estado dinámico con el Hook useState**.",
             "Sube tu **CodeSandbox** al Taller S5 en examlab."],
            "Ya pasas datos… ¡ahora haremos que la UI cambie sola!"),
 ),

 6: dict(
    titulo="Gestión del estado dinámico con el Hook useState",
    subtitulo="Que la interfaz cambie sola cuando cambian los datos",
    archivo="Sesion 6 - Gestion del estado con useState",
    nivel=2, gancho="¡La UI que se actualiza sola!",
    foco="Manejar estado local con el Hook useState, actualizarlo correctamente sin mutarlo y entender cómo el cambio de estado provoca el re-render de la interfaz.",
    contenido=[
        ("bullets", "¿Qué es el estado?", [
            "El **estado** son los datos que **cambian en el tiempo** dentro de un componente (un contador, un texto, una lista).",
            "Cuando el estado cambia, React **vuelve a dibujar** (re-render) el componente.",
            "A diferencia de una variable normal, @@cambiar el estado repinta la UI@@.",
            "Una variable `let x = 0` NO repinta nada: por eso existe useState.",
        ]),
        ("bullets", "useState: leer y actualizar", [
            "`const [valor, setValor] = useState(inicial);` — Hook que crea una pieza de estado.",
            "Devuelve un **par**: el **valor** actual y el **setter** para cambiarlo.",
            "Para actualizar: `setValor(nuevo)` — nunca `valor = nuevo`.",
            "Cada llamada al setter agenda un **re-render** con el nuevo valor.",
        ], "usestate_anatomia"),
        ("bullets", "El ciclo: evento → setState → re-render", [
            "1. Ocurre un **evento** (clic, tecleo…).",
            "2. Llamas al **setter**: `setContador(contador + 1)`.",
            "3. React **re-renderiza** el componente con el nuevo valor.",
            "4. La **UI** refleja el cambio. @@Todo automático.@@",
        ], "web_s6_contador_mock"),
        ("bullets", "No mutar el estado directamente", [
            "❌ Mal: `lista.push(x)` o `usuario.edad = 21` — React no se entera → no re-render.",
            "✅ Bien: crea una **copia nueva** con spread y pásala al setter.",
            ("`setLista([...lista, x]);`", 1),
            ("`setUsuario({ ...usuario, edad: 21 });`", 1),
            "El estado es **inmutable**: siempre un objeto/arreglo **nuevo**.",
        ], "no_mutar"),
        ("bullets", "Actualizar según el estado previo", [
            "Cuando el nuevo valor depende del anterior, usa la **forma de función**:",
            ("`setContador(prev => prev + 1);`", 1),
            "Evita errores cuando hay varias actualizaciones seguidas.",
            "React puede **agrupar** varios setstates en un mismo render (batching).",
        ]),
        ("bullets", "Estado con objetos y arreglos", [
            "Copia con spread y cambia solo lo necesario: `setForm({ ...form, email: v });`.",
            "Agregar a un arreglo: `setTodos([...todos, nuevo]);`.",
            "Quitar de un arreglo: `setTodos(todos.filter(t => t.id !== id));`.",
            "@@filter y map (S3) vuelven aquí@@ para actualizar sin mutar.",
        ]),
        ("bullets", "Reglas de los Hooks", [
            "Llama a los Hooks **solo en el nivel superior** del componente (no dentro de `if`, bucles o funciones anidadas).",
            "Llámalos **solo** desde componentes de React o desde otros Hooks.",
            "El nombre siempre empieza por **`use`** (`useState`, `useEffect`…).",
            "Respetar el **orden** de los Hooks es lo que permite a React asociarlos bien.",
        ]),
    ],
    autonomo=[
        "**Tier 2 — CodeSandbox** (" + EXAMLAB + " para entregar): construye un **contador** con botones **+**, **−** y **Reiniciar** usando `useState`.",
        ("Usa la forma de función `setContador(prev => prev + 1)` y no dejes que baje de 0.", 1),
        "Extra: una **lista** donde agregar items con un `<input>` (spread) y borrarlos (filter).",
        "**Criterio de éxito:** los botones cambian el número en pantalla sin recargar; la lista agrega/borra bien.",
        "**Entregable:** **link de CodeSandbox** en el **Taller S6 de examlab** + pantallazo.",
    ],
    logros=[
        "Entendimos **qué es el estado** y por qué re-renderiza.",
        "Usamos **useState** (valor + setter) correctamente.",
        "Aprendimos a **no mutar** el estado (spread, copias nuevas).",
        "Actualizamos según el estado previo y repasamos las **reglas de los Hooks**.",
    ],
    cierre=("¡Nos vemos en la Sesión 7!",
            ["Próxima sesión: **useEffect y consumo de APIs**.",
             "Sube tu **contador** al Taller S6 en examlab."],
            "Ya tienes estado… ¡ahora traigamos datos del servidor!"),
 ),

 7: dict(
    titulo="Efectos secundarios y consumo de APIs con useEffect",
    subtitulo="Traer datos del servidor y sincronizar la UI",
    archivo="Sesion 7 - Efectos secundarios y consumo de APIs con useEffect",
    nivel=2, gancho="¡Conecta tu app al mundo!",
    foco="Manejar efectos secundarios con useEffect, controlar cuándo se ejecutan con el arreglo de dependencias y consumir una API con fetch, manejando los estados de cargando, éxito y error.",
    contenido=[
        ("bullets", "¿Qué es un efecto secundario?", [
            "Un **efecto secundario** es algo que ocurre **fuera** del renderizado: pedir datos a una API, un temporizador, leer/escribir el navegador.",
            "El renderizado debe ser **puro** (solo calcular la UI); los efectos van aparte.",
            "**useEffect** es el Hook para ejecutar código **después** de que React pinta.",
            "Sintaxis: `useEffect(() => { ... }, [dependencias]);`.",
        ]),
        ("bullets", "El arreglo de dependencias", [
            "**`[]`** (vacío): el efecto corre **una vez**, al **montar** el componente.",
            "**`[dep]`**: corre al montar y **cada vez que `dep` cambia**.",
            "**Sin arreglo**: corre en **cada render** (peligro de bucles).",
            "@@El arreglo de dependencias controla CUÁNDO se ejecuta el efecto.@@",
        ], "useeffect_deps"),
        ("bullets", "Función de limpieza (cleanup)", [
            "Si el efecto `return` una función, React la ejecuta al **desmontar** (o antes de volver a correr el efecto).",
            "Sirve para **limpiar**: cancelar temporizadores, cerrar conexiones, quitar listeners.",
            ("`useEffect(() => { const id = setInterval(...); return () => clearInterval(id); }, []);`", 1),
            "Evita **fugas de memoria** y efectos duplicados.",
        ]),
        ("bullets", "Consumir una API con fetch", [
            "`fetch(url)` pide datos por HTTP y devuelve una **promesa**.",
            "Con **async/await** queda claro: `const res = await fetch(url); const datos = await res.json();`.",
            "Va **dentro** de useEffect (normalmente con `[]` para pedir al montar).",
            "Envuelve en `try / catch` para **manejar errores** de red.",
        ]),
        ("bullets", "Los tres estados de una petición", [
            "**Cargando**: mientras esperas → muestra un \"Cargando…\".",
            "**Éxito**: llegaron los datos → guárdalos en estado (`useState`) y muéstralos.",
            "**Error**: algo falló → muestra un mensaje claro.",
            "@@Maneja siempre los tres@@: es la diferencia entre una app amateur y una profesional.",
        ], "web_s7_fetch_mock"),
        ("tabla", "Patrón fetch + estado (resumen)", ["Paso", "Código", "Estado"], [
            ["Estados", "`useState([])` datos, `useState(true)` loading, `useState(null)` error", "iniciales"],
            ["Efecto", "`useEffect(() => { cargar(); }, [])`", "al montar"],
            ["Éxito", "`setDatos(json); setLoading(false)`", "muestra datos"],
            ["Error", "`catch { setError(e); setLoading(false) }`", "muestra error"],
        ], dict(col_w=[2.2, 6.8, 3.0], note="Mientras `loading` sea true, pinta el indicador; si hay `error`, el mensaje; si no, la lista.")),
        ("bullets", "Relación con el ciclo de vida", [
            "**Montar**: el componente aparece → `useEffect(fn, [])` (pedir datos).",
            "**Actualizar**: cambia una dependencia → el efecto vuelve a correr.",
            "**Desmontar**: el componente desaparece → corre el **cleanup**.",
            "useEffect **unifica** el ciclo de vida que antes se hacía con métodos separados.",
        ], "ciclo_vida"),
    ],
    autonomo=[
        "**Tier 2 — CodeSandbox** (" + EXAMLAB + " para entregar): consume una **API pública** (p. ej. `https://jsonplaceholder.typicode.com/users`) con `fetch` dentro de `useEffect([])`.",
        ("Maneja los **tres estados**: muestra \"Cargando…\", luego la lista de nombres, y un mensaje si hay error.", 1),
        "**Criterio de éxito:** al cargar se ve \"Cargando…\" y luego la lista real de la API; si cambias la URL a una mala, se ve el error.",
        "**Entregable:** **link de CodeSandbox** en el **Taller/Proyecto S7 de examlab** + pantallazo. Opcional: diagrama del flujo en **Mermaid (examlab)**.",
    ],
    logros=[
        "Entendimos los **efectos secundarios** y para qué sirve **useEffect**.",
        "Controlamos **cuándo** corre el efecto con el arreglo de dependencias.",
        "Usamos la **función de limpieza** y **fetch** con async/await.",
        "Manejamos los estados **cargando / éxito / error**.",
    ],
    cierre=("¡Nos vemos en la Sesión 8!",
            ["Próxima sesión: **Formularios y validación en React**.",
             "Sube tu consumo de API al Taller S7 en examlab."],
            "Ya traes datos… ¡ahora capturemos los del usuario!"),
 ),

 8: dict(
    titulo="Manejo de Formularios y validación en React",
    subtitulo="Capturar y validar datos del usuario correctamente",
    archivo="Sesion 8 - Manejo de Formularios y validacion en React",
    nivel=3, gancho="¡Formularios a prueba de errores!",
    foco="Construir formularios con componentes controlados, manejar varios campos y el envío, y validar los datos mostrando mensajes de error claros.",
    contenido=[
        ("bullets", "Componentes controlados", [
            "En un componente **controlado**, el **estado** es la única fuente de verdad del campo.",
            "Se enlaza con dos props: `value={texto}` y `onChange={e => setTexto(e.target.value)}`.",
            "Así React **siempre sabe** qué hay en el input.",
            "Cada tecla → onChange → setState → re-render con el nuevo valor.",
        ], "web_s8_form_mock"),
        ("bullets", "Manejar varios campos", [
            "Opción simple: un `useState` por campo (`nombre`, `email`, `edad`).",
            "Opción escalable: **un objeto** de estado y un handler genérico:",
            ("`setForm({ ...form, [e.target.name]: e.target.value })`", 1),
            "Usa el atributo `name` de cada input para saber cuál cambió.",
        ]),
        ("bullets", "El envío: onSubmit y preventDefault", [
            "Escucha `onSubmit` en el `<form>`, no `onClick` en el botón.",
            "@@Primera línea: `event.preventDefault()`@@ — evita que la página recargue.",
            "Luego validas y, si todo está bien, envías (o muestras el resultado).",
            "El botón de envío es `type=\"submit\"`.",
        ]),
        ("bullets", "Validación de datos", [
            "**Requerido**: el campo no puede estar vacío (`valor.trim() !== \"\"`).",
            "**Formato**: email con una expresión regular sencilla; solo números; etc.",
            "**Longitud**: mínimo/máximo de caracteres (contraseñas, usuarios).",
            "Guarda los errores en estado: `const [errores, setErrores] = useState({});`.",
        ], "validacion_flujo"),
        ("bullets", "Mostrar errores y bloquear el envío", [
            "Muestra el mensaje **junto al campo**: `{errores.email && <span>{errores.email}</span>}`.",
            "**Deshabilita** el botón si el formulario es inválido: `disabled={!esValido}`.",
            "Valida al **enviar** y, para mejor UX, también al **cambiar** (onChange).",
            "Mensajes claros y en español: \"El correo no es válido\".",
        ]),
        ("bullets", "Controlado vs no controlado", [
            "**Controlado**: el valor vive en el estado (value + onChange) — lo recomendado.",
            "**No controlado**: el DOM guarda el valor y lo lees con una **ref** (`useRef`).",
            "Controlado = más control, validación en vivo, fácil de resetear.",
            "@@En React se prefieren los controlados@@ salvo casos puntuales.",
        ], "controlado_vs_no"),
        ("tabla", "Errores comunes en formularios React", ["Síntoma", "Causa", "Solución"], [
            ["El input no deja escribir", "`value` sin `onChange`", "Agrega el onChange que hace setState"],
            ["La página recarga al enviar", "Falta `preventDefault()`", "Llámalo al inicio de onSubmit"],
            ["Warning \"controlled/uncontrolled\"", "value pasa de undefined a valor", "Inicia el estado con `\"\"`"],
        ], dict(col_w=[3.8, 3.6, 4.6], note="Regla de oro: si pones `value`, pon también `onChange`, e inicia el estado con un string vacío.")),
    ],
    autonomo=[
        "**Tier 2 — CodeSandbox** (" + EXAMLAB + " para entregar): crea un **formulario de registro** controlado con `nombre`, `email` y `contraseña`.",
        ("Valida: todos requeridos, email con `@`, contraseña de mínimo 6 caracteres. Muestra los mensajes de error.", 1),
        ("Deshabilita el botón mientras el formulario sea inválido; al enviar válido, muestra \"¡Registro exitoso!\".", 1),
        "**Criterio de éxito:** no se puede enviar con datos inválidos y los mensajes aparecen junto a cada campo.",
        "**Entregable:** **link de CodeSandbox** en el **Taller S8 de examlab** + pantallazo.",
    ],
    logros=[
        "Construimos **componentes controlados** (value + onChange).",
        "Manejamos **varios campos** y el envío con **preventDefault**.",
        "**Validamos** requeridos, formato y longitud con mensajes claros.",
        "Distinguimos **controlado vs no controlado**.",
    ],
    cierre=("¡Nos vemos en la Sesión 9!",
            ["Última sesión: **Redux y estado global** + proyecto final.",
             "Sube tu formulario al Taller S8 en examlab."],
            "Ya capturas datos… ¡ahora centralicemos el estado de TODA la app!"),
 ),

 9: dict(
    titulo="Introducción a Redux y gestión de estado global",
    subtitulo="Una única fuente de verdad para toda la aplicación",
    archivo="Sesion 9 - Introduccion a Redux y estado global",
    nivel=3, gancho="¡Una sola fuente de verdad!",
    foco="Entender por qué se necesita estado global, los conceptos de Redux (store, actions, reducers, dispatch) y cómo conectar React con Redux Toolkit para el proyecto final.",
    contenido=[
        ("bullets", "El problema: prop drilling", [
            "Con solo props, un dato que necesitan componentes lejanos hay que **pasarlo por muchos niveles**.",
            "Componentes intermedios reciben props que **ni usan**, solo para pasarlas: eso es **prop drilling**.",
            "Se vuelve **difícil de mantener** cuando la app crece.",
            "Solución: un **estado global** que cualquier componente pueda leer.",
        ], "prop_drilling"),
        ("bullets", "Conceptos de Redux", [
            "**Store**: la **única fuente de verdad**; guarda todo el estado global.",
            "**State**: los datos dentro del store.",
            "**Action**: un objeto que describe **qué pasó** (`{ type: \"carrito/agregar\", payload }`).",
            "**Reducer**: función que calcula el **nuevo estado** a partir del actual y una action.",
            "**dispatch**: la forma de **enviar** una action al store.",
        ], "web_s9_app_mock"),
        ("bullets", "El flujo unidireccional de Redux", [
            "1. La UI hace **`dispatch(action)`**.",
            "2. El **reducer** recibe `(state, action)` y devuelve el **nuevo state**.",
            "3. El **store** se actualiza.",
            "4. Los componentes suscritos **re-renderizan** con el nuevo dato.",
            "@@Siempre en un solo sentido: predecible y fácil de depurar.@@",
        ], "redux_flujo"),
        ("bullets", "Reducers puros e inmutabilidad", [
            "Un **reducer es puro**: con las mismas entradas da la misma salida y **no** tiene efectos secundarios.",
            "**No muta** el estado: devuelve un objeto **nuevo** (spread, como en useState).",
            "Nada de `fetch`, `Math.random()` ni fechas dentro del reducer.",
            "Esta pureza permite el **time-travel debugging** de Redux DevTools.",
        ]),
        ("bullets", "Redux Toolkit (la forma moderna)", [
            "**Redux Toolkit (RTK)** reduce el código repetitivo del Redux clásico.",
            "**`createSlice`** genera el reducer y las actions juntas.",
            "Dentro de un slice **sí** puedes 'mutar' (Immer lo convierte en inmutable por debajo).",
            "`configureStore({ reducer })` arma el store con buenas prácticas por defecto.",
        ]),
        ("tabla", "Conectar React con Redux", ["Pieza", "Qué hace", "Dónde"], [
            ["**<Provider store>**", "Da el store a toda la app", "envuelve `<App />`"],
            ["**useSelector**", "Lee un dato del store", "en el componente"],
            ["**useDispatch**", "Obtiene la función dispatch", "en el componente"],
            ["**dispatch(action)**", "Envía una action al store", "en un handler"],
        ], dict(col_w=[3.4, 4.8, 3.8], note="react-redux conecta ambos mundos: Provider arriba, y useSelector/useDispatch en los componentes.")),
        ("bullets", "Proyecto final: todo junto", [
            "Integra lo aprendido: **componentes + props + estado + efectos + Redux**.",
            "Idea: un **carrito de compras** o una **lista de tareas** con estado global.",
            "El estado global (carrito/tareas) vive en el **store**; los componentes lo leen con `useSelector`.",
            "@@Este es tu entregable estrella del curso.@@",
        ]),
    ],
    autonomo=[
        "**Tier 2 — CodeSandbox** (" + EXAMLAB + " para entregar): **proyecto final** — una app con **estado global** (Redux Toolkit o Context) que integre componentes, props y estado.",
        ("Ejemplo: carrito de compras: agregar/quitar productos actualiza un contador global visible en el header.", 1),
        "**Criterio de éxito:** un cambio disparado en un componente se refleja en otro **sin pasar props** entre ellos.",
        "**Entregable:** **link de CodeSandbox** (o ZIP) en el **Proyecto S9 de examlab**. Opcional: el flujo unidireccional en **Mermaid (examlab)**.",
    ],
    logros=[
        "Entendimos el **prop drilling** y por qué existe el estado global.",
        "Aprendimos las piezas de **Redux**: store, actions, reducers, dispatch.",
        "Seguimos el **flujo unidireccional** y la importancia de reducers puros.",
        "Conectamos React con **Redux Toolkit** en el proyecto final.",
    ],
    cierre=("¡Felicitaciones, terminaste el curso!",
            ["Sube tu **proyecto final** al Proyecto S9 en examlab y completa tu ruta en Coursera (90%).",
             "Responde la **encuesta de satisfacción** de hoy.",
             "Recorrimos de JavaScript y el DOM a React con Hooks y Redux."],
            "De cambiar un <h1>… ¡a construir una app React completa!"),
 ),
}


# ============================== BUILDERS ==============================
def build_presentacion():
    set_footer(CURSO)
    prs = new_prs()
    course_cover(prs, CURSO, None, "¡Bienvenidos estudiantes!",
        [PROGRAMA, "Cuatrimestre No. [20 — confirmar]", "Duración: **9 clases** (105 min c/u)",
         "Horario: Lunes, Miércoles y Viernes · 6:00–7:45 PM",
         "Fechas: 27/07/2026 – 15/08/2026"],
        "Empezamos a las 6:00 PM…")
    tutor_slide(prs, TUTOR[0], TUTOR[1], TUTOR[2], idx=2)
    content_slide(prs, "METODOLOGÍA", [
        "**Sesiones teórico-prácticas**: cada clase combina teoría, modelación y práctica en vivo.",
        "Momentos por clase:",
        ("**Motivación**: preguntas y ejemplos que generan interés y conexión.", 1),
        ("**Encuadre**: explicación de objetivos, ruta de aprendizaje y acuerdos.", 1),
        ("**Modelación**: ejemplos guiados para mostrar conceptos y técnicas (código en vivo).", 1),
        ("**Simulación**: trabajo en grupos pequeños para aplicar conceptos.", 1),
        ("**Ejercitación**: práctica individual en examlab y CodePen/CodeSandbox.", 1),
        ("**Cierre**: retroalimentación, resumen y conexión con objetivos.", 1),
        ("**Evaluación**: Reto en vivo (Kahoot), Test de repaso y avance de la ruta en Coursera.", 1),
    ], idx=3)
    objectives_slide(prs, "Objetivos", OBJETIVOS_CURSO, idx=4)
    table_content(prs, "¿Cómo se evalúa?", ["Componente", "Ponderación"], EVAL_ROWS,
                  col_w=[9.4, 2.6], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER], idx=5,
                  note=EVAL_NOTE)
    content_slide(prs, "EJEMPLO DE EVALUACIÓN", [
        "Progreso en Coursera (90%): nota 4.6 → 4.6 × 0.90 = **4.14**",
        "Asistencia (10%): asistió a todas → 5.0 × 0.10 = **0.50**",
        "Subtotal = 4.14 + 0.50 = **4.64**",
        "Reto en vivo (Kahoot): quedó de 1.° → **+0.5** (bono, tope 5.0)",
        "@@Nota final = mín(4.64 + 0.5 , 5.0) = 5.0@@",
    ], idx=6)
    content_slide(prs, "CONTENIDO", [
        f"**Sesión {n}** — {d['titulo']}." for n, d in SESIONES.items()
    ], size=15, idx=7)
    content_slide(prs, "RECURSOS", [
        "**Material de clases:** 🔗 [inserta aquí el hipervínculo] — guiones, diapositivas y material de apoyo.",
        "**Cursos base (Coursera):**",
        ("\"Interactividad con JavaScript\" — [URL del curso — confirmar con coordinación]", 1),
        ("\"Desarrollo de aplicaciones frontales con React\" — [URL del curso — confirmar con coordinación]", 1),
        "Guías, videos y ruta de aprendizaje: en **examlab**.",
        (EXAMLAB, 1),
    ], size=15, idx=8)
    content_slide(prs, "HERRAMIENTAS", [
        "**En examlab** (plataforma del curso · " + EXAMLAB + "):",
        ("Test (quizzes) · Reto en vivo (Kahoot) · editor de código JavaScript (consola) · pizarra/Mermaid · Taller/Proyecto.", 1),
        "**Solo online (gratuitas):**",
        ("CodePen (DOM/JS) · CodeSandbox / StackBlitz (React) · MDN Web Docs (referencia).", 1),
        "**En el mundo laboral** (lo que usarás en el trabajo):",
        ("Visual Studio Code + Node.js · React (Vite / CRA) · Redux Toolkit · Git/GitHub · Chrome DevTools.", 1),
    ], size=15, idx=9)
    content_slide(prs, "¡ IMPORTANTE !", [
        "El **progreso en Coursera (90%)** se calcula sobre la ruta de los cursos base; avanza cada semana del curso.",
        "La **asistencia (10%)** se registra al **final de cada sesión**.",
        "Las **notas** se cargan hasta **una semana** después de la última clase; tienes **3 días** hábiles para reclamaciones por correo.",
        "No olvides responder la **encuesta de satisfacción** el último día (vie 14-ago).",
    ], idx=10)
    image_slide(prs, "GESTORES", GESTORES_IMG, idx=11)
    out = os.path.join(BASE, "Presentacion del curso.pptx")
    prs.save(out)
    print("OK", out)


def build_sesion(n):
    d = SESIONES[n]
    set_footer(CURSO)
    prs = new_prs()
    session_cover(prs, f"SESIÓN {n}", NIVELES[d["nivel"]], d["titulo"], d["subtitulo"],
                  d["gancho"],
                  [f"{CURSO} · {PROGRAMA}", "Duración: **105 min** (1 h 45 min)"])
    # SIN slides "Recordemos la asignatura" ni "¿Cómo trabajaremos hoy?" (reglas del usuario)
    std_proposito(prs, d["foco"], d["nivel"])
    idx = 3
    for item in d["contenido"]:
        kind = item[0]
        if kind == "bullets":
            title, items = item[1], item[2]
            diag_id = item[3] if len(item) > 3 else None
            img = diag(diag_id)
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
    out = os.path.join(folder, f"Sesion {n} - {d['titulo']}.pptx")
    # nombre de archivo seguro (sin caracteres problemáticos)
    safe = d["archivo"] + ".pptx"
    out = os.path.join(folder, safe)
    prs.save(out)
    print("OK", out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    os.makedirs(BASE, exist_ok=True)
    build_presentacion()
    for n in SESIONES:
        build_sesion(n)
    print("LISTO: 10 decks generados.")
