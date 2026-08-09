# -*- coding: utf-8 -*-
"""One-shot patch for _regen_guiones_creatividad.py — run then delete."""
from pathlib import Path
import re

p = Path(
    r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\Pregrado"
    r"\CREATIVIDAD Y PENSAMIENTO INNOVADOR PARA ESCUELA DE INGENIERIAS"
    r"\Guiones\_regen_guiones_creatividad.py"
)
text = p.read_text(encoding="utf-8")

start = text.index("# (n, fecha, bloque")
end = text.index("# ---------------------------------------------------------------------------\n# CONTENIDOS POR SESIÓN")

new_block = '''# (n, titulo_archivo, titulo_oficial, detalle) — sin fechas de periodo (reutilizable)
SESIONES = [
    (1,
     "Sesion 01 - Introducción · Propuesta de Innovación (trabajo final)",
     "Introducción · Propuesta de Innovación (trabajo final)",
     "Anunciar el trabajo final desde el día 1 · ficha problema–oportunidad."),
    (2,
     "Sesion 02 - Inteligencia emocional, creatividad e innovación",
     "Inteligencia emocional, creatividad e innovación",
     "Bloqueadores/ensanchadores · mapa de utilidad."),
    (3,
     "Sesion 03 - Creatividadinnovación en I+D · Design Thinking y técnicas",
     "Creatividad/innovación en I+D · Design Thinking y técnicas",
     "Pensamiento divergente/convergente · ideación."),
    (4,
     "Sesion 04 - Gestión de la innovación (Manual de Oslo OCDE)",
     "Gestión de la innovación (Manual de Oslo / OCDE)",
     "Métodos en producto, proceso, organización, marketing, social."),
    (5,
     "Sesion 05 - Tipos de innovación",
     "Tipos de innovación",
     "Cuadro comparativo · mejoras en contextos socio-económicos."),
    (6,
     "Sesion 06 - Análisis de negocios · validación de la propuesta",
     "Análisis de negocios · validación de la propuesta",
     "FODA, Canvas, MVP · sustentación de propuesta."),
    (7,
     "Sesion 07 - Vigilancia tecnológica",
     "Vigilancia tecnológica",
     "Datos estratégicos sobre tecnologías y tendencias."),
    (8,
     "Sesion 08 - Innovación local–internacional · entidades de apoyo",
     "Innovación local–internacional · entidades de apoyo",
     "Cierre del hilo · impactos y programas de apoyo."),
]


def header(n, label, titulo, detalle):
    return f"""### GUIÓN DOCENTE — Sesión {n:02d}: {titulo}

> **Uso:** guion de locución de **esta** clase. Léalo en voz alta casi literal.
> Estudie primero el Fundamento Teórico. **Duración: 60 minutos**.
> Logística de semestre (fechas, grupos, cortes) → Presentación del Curso / Manual.
> **PPTX:** `Clases/{label}/Presentacion.pptx` — en cada fase se indica la slide de ESA presentación.

📌 **De esta sesión**
- **Sesión:** **{n:02d}** · **Tema:** {titulo}
- **Detalle:** {detalle}
- **PPTX estudiante:** `Clases/{label}/Presentacion.pptx`
- **Meet (serie del curso):** {MEET}

"""


def mapa_slides(n=None):
    """Mapa de slides de ESTA presentación (no el temario del curso)."""
    if n == 1:
        return """🗺️ **Slides de esta presentación** (Sesión 01 — tema puntual)

| Slide | Título en el PPTX | Cuándo usarla |
| :---: | :--- | :--- |
| **1** | Portada — Sesión 01 | Apertura |
| **2** | OBJETIVOS DE HOY | Encuadre |
| **3** | ENFOQUE DE HOY | Anclar el entregable de la hora |
| **4** | CREATIVIDAD ≠ INNOVACIÓN | Exposición |
| **5** | ANALOGÍA DE LA RECETA | Exposición |
| **6** | EL TRABAJO FINAL DESDE EL DÍA 1 | Modelación del hilo |
| **7** | TIPOS DE INNOVACIÓN (vista previa) | Vocabulario Oslo |
| **8** | EJEMPLO MODELADO — Ficha | Modelación en vivo |
| **9** | TALLER — Ficha problema–oportunidad | Consigna práctica |
| **10** | PARA CONTINUAR | Trabajo autónomo |
| **11** | Cierre — Sesión 01 | Despedida |

"""
    return """🗺️ **Slides de esta presentación** (tema de hoy — no es el mapa del curso)

| Slide | Título en el PPTX | Cuándo usarla |
| :---: | :--- | :--- |
| **1** | Portada (SESIÓN NN — tema) | Apertura |
| **2** | OBJETIVOS | Encuadre |
| **3** | CONTENIDO CLAVE | Exposición y modelación |
| **4** | ENFOQUE DE HOY | Anclaje del tema |
| **5** | ACTIVIDAD / TALLER | Consigna del taller |
| **6** | PARA CONTINUAR | Trabajo autónomo |
| **7** | Cierre | Despedida |

"""


def plan_tabla(fases):
    """fases: list of (nombre, min, acum) — reloj relativo al inicio del encuentro."""
    rows = ["| Fase | Minutos | Reloj sugerido (desde el inicio) |", "| :--- | :---: | :--- |"]
    start_m = 0
    for nombre, mins, _ in fases:
        m0 = start_m
        m1 = start_m + mins
        rows.append(f"| {nombre} | {mins} | min {m0:02d}:00 – {m1:02d}:00 |")
        start_m = m1
    rows.append("")
    rows.append(f"> **Suma:** **{sum(f[1] for f in fases)} minutos** exactos.")
    return "\\n".join(rows)


'''

# Fix accidental double-escape in plan_tabla join
new_block = new_block.replace('return "\\\\n".join(rows)', 'return "\\n".join(rows)')
# Actually in the triple-quoted string above I used return "\\n".join which becomes \n in file - good
# Wait I wrote return "\\n".join in the source of this patch file which writes \n to the target - correct.

text = text[:start] + new_block + text[end:]

text = text.replace(
    "n, fecha, bloque, label, titulo, detalle = meta",
    "n, label, titulo, detalle = meta",
)
text = text.replace("header(*meta) + mapa_slides() +", "header(*meta) + mapa_slides(n) +")

for a, b in [
    ("**Entregable LMS:**", "**Entregable CDigital:**"),
    ("archivo o captura de la ficha en el LMS", "archivo o captura de la ficha en CDigital"),
    ("en el archivo del LMS", "en el archivo de CDigital"),
    ("actividad en el LMS", "actividad en CDigital"),
    ("clase autónoma** en el LMS", "clase autónoma** en CDigital"),
    ("espacio LMS listo", "espacio CDigital listo"),
    ("fundamento · PPTX · LMS ·", "fundamento · PPTX · CDigital ·"),
    ("3. **LMS:**", "3. **CDigital:**"),
    ("Moodle/CDigital", "CDigital"),
    ("Publiqué en Moodle el espacio", "Publiqué en CDigital el espacio"),
    ("subir a Moodle el paquete", "subir a CDigital el paquete"),
    ("Confirmen en Moodle", "Confirmen en CDigital"),
    ("en Moodle", "en CDigital"),
]:
    text = text.replace(a, b)

text = re.sub(r"\bLMS\b", "CDigital", text)

text = text.replace(
    '("1️⃣ Encuadre y acuerdos", 8, 8),',
    '("1️⃣ Encuadre", 8, 8),',
)
text = text.replace(
    '("2️⃣ Creatividad vs. innovación + mapa del curso", 12, 20),',
    '("2️⃣ Creatividad vs. innovación + hilo de la propuesta", 12, 20),',
)
text = text.replace(
    "2. **Comprender** el mapa de las 8 unidades y que el hilo conductor es la **Propuesta de Innovación**.",
    "2. **Comprender** que el hilo conductor del curso es la **Propuesta de Innovación** (se construye desde hoy).",
)
text = text.replace(
    "- Confundir **trabajo autónomo** con “no hay clase”: si el miércoles es **festivo**, hay actividad en CDigital (clase autónoma), no cancelación.\n",
    "- Confundir creatividad con innovación: sin implementación y valor, solo hay idea.\n",
)

old_p1 = '''#### 1️⃣ Encuadre y acuerdos (~8 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS) → 4 (ACUERDOS)

**Objetivo de la fase:** que todos sepan qué curso es, cuánto dura el encuentro y qué se espera al final de la hora.

**GUION LITERAL:**
> “Buenas tardes. Bienvenidos a *Creatividad y Pensamiento Innovador*, Escuela de Ingenierías, código EI004. Somos encuentro de **una hora**: de 5:00 a 6:00 pm. Hoy es la **Sesión 01**. Al terminar esta hora no se van solo con teoría: se van con una **ficha escrita** del problema que van a atacar con su Propuesta de Innovación.”

> “Miren la **slide 2 — OBJETIVOS**. Hoy vamos a: (1) separar creatividad de innovación; (2) entender el mapa del curso; (3) anunciar el trabajo final desde el día 1; y (4) salir con un avance observable.”

> “Antes de contenido, acuerdos — **slide 4**. Uno: el Meet de esta serie es **el mismo enlace** todas las semanas. Dos: si el miércoles es **festivo colombiano**, no ‘se cancela’: hay **clase autónoma** en CDigital. Tres: el producto del curso se construye **desde hoy**, no en la última semana.”

**Qué hacer:**
1. (2 min) Portada + bienvenida + control de audio/nombres en Meet.
2. (3 min) Leer objetivos en slide 2.
3. (3 min) Acuerdos en slide 4; pedir en el chat: “escriban una palabra: ¿qué problema del mundo real les molesta hoy?”.

---

#### 2️⃣ Creatividad vs. innovación + mapa del curso (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE)

**GUION LITERAL:**
> “Vamos a la **slide 3 — CONTENIDO CLAVE**. Primera idea madre del curso, escríbanla: **creatividad no es lo mismo que innovación**.”

> “Creatividad = generar ideas nuevas. Innovación = llevar la idea a la práctica **con valor**. Analogía: inventar la receta vs. cocinarla, servirla y que alguien la pida otra vez. En Ingeniería vemos mucho ‘tengo una idea de app’ y muy poco ‘alguien la usó y le cambió el dolor’. Nosotros vamos por lo segundo.”

> “Este curso tiene **ocho unidades**. No son ocho temas sueltos: son ocho estaciones del **mismo tren**. El tren se llama **Propuesta de Innovación**. Cada semana le pone un vagón: inteligencia emocional, Design Thinking, Manual de Oslo, tipos, validación de negocio, vigilancia tecnológica y ecosistema de apoyo.”

> “Evaluación del curso, Art. 52: **Corte 1 30%, Corte 2 30%, Corte 3 40%**. Confirmen en CDigital el desglose EV. Pero el mensaje pedagógico es: si avanzan la propuesta cada semana, el corte no los sorprende.”

**Qué hacer:**
1. (5 min) Definiciones + analogía; pedir 1 ejemplo oral de “idea que no llegó a innovar”.
2. (4 min) Mapa U1–U8 (puede apoyarse en la Presentación del Curso si la tiene abierta).
3. (3 min) Mencionar cortes sin alargar; volver al hilo de la propuesta.

---

#### 3️⃣ Qué es la Propuesta de Innovación — modelación (~12 min) — Protagonista: Docente
**Slides:** 3 (CONTENIDO CLAVE) y, si quiere, anotar en pantalla compartida
'''

new_p1 = '''#### 1️⃣ Encuadre (~8 min) — Protagonista: Docente
**Slides:** 1 (Portada) → 2 (OBJETIVOS) → 3 (ENFOQUE DE HOY)

**Objetivo de la fase:** que sepan qué se espera al final de la hora (ficha escrita).

**GUION LITERAL:**
> “Buenas tardes. Hoy es la **Sesión 01**. Al terminar esta hora no se van solo con teoría: se van con una **ficha escrita** del problema que van a atacar con su Propuesta de Innovación.”

> “Miren la **slide 2 — OBJETIVOS**. Hoy vamos a: (1) separar creatividad de innovación; (2) anunciar el hilo conductor — la Propuesta de Innovación — desde el día 1; y (3) salir con un avance observable.”

> “**Slide 3 — ENFOQUE DE HOY.** No entregamos la propuesta completa: entregamos el **insumo #1**. Cada unidad alimentará el mismo documento. Sin problema claro no hay propuesta defendible. En el chat: escriban una palabra — ¿qué problema del mundo real les molesta hoy?”

**Qué hacer:**
1. (2 min) Portada + bienvenida + control de audio/nombres en Meet.
2. (3 min) Leer objetivos en slide 2.
3. (3 min) Enfoque en slide 3 + prompt en el chat.

---

#### 2️⃣ Creatividad vs. innovación + hilo de la propuesta (~12 min) — Protagonista: Docente
**Slides:** 4 (CREATIVIDAD ≠ INNOVACIÓN) → 5 (ANALOGÍA) → 6 (TRABAJO FINAL)

**GUION LITERAL:**
> “Vamos a la **slide 4**. Primera idea madre, escríbanla: **creatividad no es lo mismo que innovación**.”

> “Creatividad = generar ideas nuevas. Innovación = llevar la idea a la práctica **con valor**. Analogía en la **slide 5**: inventar la receta vs. cocinarla, servirla y que alguien la pida otra vez. En Ingeniería vemos mucho ‘tengo una idea de app’ y muy poco ‘alguien la usó y le cambió el dolor’. Nosotros vamos por lo segundo.”

> “**Slide 6.** El hilo conductor es la **Propuesta de Innovación**. Hoy no es el mapa de todo el semestre: es el anuncio de que cada encuentro alimenta **el mismo** documento. Si avanzan la propuesta cada semana, el corte no los sorprende.”

**Qué hacer:**
1. (6 min) Definiciones + analogía; pedir 1 ejemplo oral de “idea que no llegó a innovar”.
2. (6 min) Anclar el hilo de la Propuesta (sin listar las 8 unidades).

---

#### 3️⃣ Qué es la Propuesta de Innovación — modelación (~12 min) — Protagonista: Docente
**Slides:** 7 (TIPOS Oslo vista previa) → 8 (EJEMPLO MODELADO)
'''

if old_p1 not in text:
    print("WARN: old_p1 block not found")
else:
    text = text.replace(old_p1, new_p1)
    print("OK S01 phases")

text = text.replace(
    '''#### 4️⃣ Taller en clase: ficha del problema–oportunidad (~20 min) — Protagonista: Estudiantes
**Slides:** 5 (ACTIVIDAD / TALLER)

**GUION LITERAL (consigna):**
> “Pasamos a la **slide 5 — ACTIVIDAD**. Tienen **20 minutos**.''',
    '''#### 4️⃣ Taller en clase: ficha del problema–oportunidad (~20 min) — Protagonista: Estudiantes
**Slides:** 9 (TALLER)

**GUION LITERAL (consigna):**
> “Pasamos a la **slide 9 — TALLER**. Tienen **20 minutos**.''',
)

text = text.replace(
    '''#### 5️⃣ Cierre + trabajo autónomo (~8 min) — Protagonista: Docente
**Slides:** 6 (PARA CONTINUAR) → 7 (Cierre)

**GUION LITERAL:**
> “Tres ideas de hoy: (1) creatividad genera; innovación **implementa con valor**; (2) el curso es un solo hilo — la **Propuesta de Innovación**; (3) sin problema claro no hay propuesta defendible.”

> “**Slide 6 — PARA CONTINUAR.** Trabajo autónomo antes del 12 de agosto: (a) subir la ficha a CDigital en el espacio que indique el curso; (b) mejorar la redacción del problema con una observación real (foto, dato, frase de un usuario); (c) traer a la Sesión 02 una lista de **3 bloqueadores personales** que les impiden crear — cansancio, miedo al ridículo, perfeccionismo, etc.”

> “**Slide 7 — Cierre.** Próxima sesión: *Inteligencia emocional, creatividad e innovación*. Mismo Meet, mismo horario. Gracias y buen trabajo.”
''',
    '''#### 5️⃣ Cierre + trabajo autónomo (~8 min) — Protagonista: Docente
**Slides:** 10 (PARA CONTINUAR) → 11 (Cierre)

**GUION LITERAL:**
> “Tres ideas de hoy: (1) creatividad genera; innovación **implementa con valor**; (2) el curso es un solo hilo — la **Propuesta de Innovación**; (3) sin problema claro no hay propuesta defendible.”

> “**Slide 10 — PARA CONTINUAR.** Trabajo autónomo: (a) subir la ficha a CDigital (`S01_FichaProblema_Apellido`); (b) mejorar el problema con una observación real; (c) traer a la Sesión 02 **3 bloqueadores personales** que les impiden crear.”

> “**Slide 11 — Cierre.** Próxima: *Inteligencia emocional, creatividad e innovación*. Mismo Meet. Gracias y buen trabajo.”
''',
)

old_fund3 = '''#### 3. Por qué anunciar el trabajo final el día 1
Si no anuncia la **Propuesta de Innovación** desde hoy, cada taller se vuelve una isla. Cada unidad debe **alimentar el mismo entregable**:
- U2 (IE) → bloqueadores personales y mapa de utilidad del problema.
- U3 (Design Thinking) → empatía, ideación, prototipo conceptual.
- U4–U5 (Oslo / tipos) → clasificar y justificar el tipo de innovación.
- U6 (negocio) → FODA, Canvas, MVP, validación.
- U7 (vigilancia) → evidencia tecnológica y tendencias.
- U8 (ecosistema) → entidades de apoyo y cierre.
'''
new_fund3 = '''#### 3. Por qué anunciar el trabajo final el día 1
Si no anuncia la **Propuesta de Innovación** desde hoy, cada taller se vuelve una isla. Cada encuentro debe **alimentar el mismo entregable**; no hace falta recorrer el mapa completo en esta clase.
'''
if old_fund3 in text:
    text = text.replace(old_fund3, new_fund3)
    print("OK fund3")
else:
    print("WARN fund3")

text = text.replace("antes del 19/08 y traigan", "antes de la siguiente sesión y traigan")

text = text.replace(
    '''    for meta in SESIONES:
        n = meta[0]
        label = meta[3]
        md_path = os.path.join(ROOT, f"{label}.md")
''',
    '''    for meta in SESIONES:
        n = meta[0]
        label = meta[1]
        md_path = os.path.join(ROOT, f"{label}.md")
''',
)

# Verify plan_tabla join line
if 'return "\\\\n".join(rows)' in text or 'return "\\n".join(rows)' in text:
    # normalize to real join
    text = text.replace('return "\\\\n".join(rows)', 'return "\\n".join(rows)')

left = [i for i, line in enumerate(text.splitlines(), 1) if re.search(r"\bLMS\b", line)]
print("LMS lines left:", left)
moodle = [i for i, line in enumerate(text.splitlines(), 1) if "Moodle" in line]
print("Moodle lines left:", moodle)

# Check plan_tabla is valid Python
ns = {}
# quick syntax check of plan_tabla by compiling whole file later
p.write_text(text, encoding="utf-8")
print("Wrote", p)

# Fix plan_tabla if broken: read the function
import ast
try:
    ast.parse(text)
    print("AST OK")
except SyntaxError as e:
    print("AST FAIL", e)
    # show plan_tabla area
    i = text.index("def plan_tabla")
    print(repr(text[i:i+500]))
