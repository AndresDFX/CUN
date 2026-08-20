#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parte MECÁNICA del corte documento / diapositivas en las fichas de sustentación.

Las fichas nacieron con 8 secciones y un solo cajón de hallazgos (`## 4. Debilidades y
huecos`), donde convivían los reparos al **documento** y los reparos a las
**diapositivas**. En sala son dos cosas distintas: el documento ya está leído y no cambia,
y el mazo se ve proyectado mientras el grupo habla. Así que se parten en dos secciones:

    ## 4. OBSERVACIONES DEL DOCUMENTO   ← lo que ya estaba, sin los ítems de mazo
    ## 5. OBSERVACIONES DE LAS DIAPOSITIVAS   ← nueva, se escribe ficha por ficha

Este guion hace SOLO lo mecánico y verificable, que es lo que no conviene hacer a mano en
40 archivos: retitular la §4, correr la numeración de las secciones siguientes (5→6, 6→7,
7→8, 7.1→8.1, 8→9) y arreglar **todas** las remisiones «§N» de la ficha, de la hoja de
respuestas, del `4 - Evaluacion.md`, del índice y del LEEME.

Lo que NO hace, a propósito: escribir el contenido de la nueva §5. Eso exige juicio
—decidir qué hallazgo se mira en pantalla y qué diapositiva lo sostiene— y se redacta ficha
por ficha citando la diapositiva, igual que el resto del material.

TRES TRAMPAS QUE ESTE GUION EVITA
1. **Renumerar en ascendente se pisa a sí mismo**: 5→6 crearía un segundo «6» que 6→7
   volvería a mover. Todas las tablas van en **descendente**.
2. **No todo «§N» es de la ficha.** `§5.1 Alcances` es del documento del grupo, `§9.2 de la
   p. 11` es del instructivo, `§4: máximo 3 estudiantes` es del resumen del instructivo y
   `§3 de 4 - Evaluacion.md` es de otro archivo. Por eso no hay ni una sustitución por
   expresión regular sobre «§ + número»: cada remisión se cambia por su **frase completa**.
3. **Idempotencia**: correrlo dos veces no vuelve a mover nada (las frases de origen ya no
   existen). Al final avisa de cualquier «§N» viejo que quedara sin traducir.

USO
    python config/evaluaciones/reestructura_fichas_doc_diapos.py --simular     # no escribe
    python config/evaluaciones/reestructura_fichas_doc_diapos.py --confirmar
"""

import os
import sys

sys.stdout.reconfigure(encoding="utf-8")  # la consola de esta máquina es cp1252

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
FICHAS = os.path.join(
    REPO, "Especializacion", "Evaluaciones", "2026-2", "Fichas de evaluacion"
)

# ─────────────────────────────────────────────────────────────────────────────────────────
# 1 · Ficha: títulos de sección. Descendente, y el «\n» inicial ancla el comienzo de línea.
# ─────────────────────────────────────────────────────────────────────────────────────────
FICHA_TITULOS = [
    ("\n## 8. Observaciones administrativas", "\n## 9. Observaciones administrativas"),
    ("\n### 7.1 Formulario oficial del jurado", "\n### 8.1 Formulario oficial del jurado"),
    ("\n## 7. Umbrales de nota", "\n## 8. Umbrales de nota"),
    ("\n## 6. PREGUNTAS DESPUÉS", "\n## 7. PREGUNTAS DESPUÉS"),
    ("\n## 5. PREGUNTAS ANTES", "\n## 6. PREGUNTAS ANTES"),
    (
        "\n## 4. Debilidades y huecos (con página)",
        "\n## 4. OBSERVACIONES DEL DOCUMENTO — debilidades y huecos (con página)",
    ),
]

# 2 · Ficha: remisiones internas, una por frase real (censadas con grep antes de escribir).
FICHA_REFS = [
    ("umbrales de esta §7", "umbrales de esta §8"),
    ("bloque de cotejo de la §5)", "bloque de cotejo de la §6)"),
    ("la primera pregunta de la §5.", "la primera pregunta de la §6."),
    ("La §7 quedó escrita", "La §8 quedó escrita"),
    ("No se toca la §7 ", "No se toca la §8 "),
    ("la §7 y la §7.1", "la §8 y la §8.1"),
    ("ver §8)", "ver §9)"),
    ("ver §8.", "ver §9."),
    ("jurados: §8.)", "jurados: §9.)"),
    ("(§8)", "(§9)"),
]

# 3 · Hoja de respuestas: apunta a la ficha, nunca a sí misma (ella usa §A–§E).
HOJA_REFS = [
    ("desde la §7.1 de la ficha", "desde la §8.1 de la ficha"),
    ("(la §7.1 trae", "(la §8.1 trae"),
    ("(§7 de la ficha", "(§8 de la ficha"),
    ("la §7 de la ficha)", "la §8 de la ficha)"),   # «según la §7 de la ficha)» de G-008
    ("a priori de la §7)", "a priori de la §8)"),
    ("(§6 de la ficha)", "(§7 de la ficha)"),
    ("en la §5 de la ficha)", "en la §6 de la ficha)"),
]

# 4 · `4 - Evaluacion.md`: sus propias secciones son §1–§4 y NO se tocan; solo lo «de la ficha».
EVAL_REFS = [
    (
        "(§4 huecos, §5 preguntas, §6 condicionales, §7 umbrales)",
        "(§4 huecos del documento, §5 huecos de las diapositivas, §6 preguntas,"
        " §7 condicionales, §8 umbrales)",
    ),
    ("los de la §7 de la ficha:", "los de la §8 de la ficha:"),
    ("los umbrales de la §7 de la ficha", "los umbrales de la §8 de la ficha"),
    ("Umbral de la §7 que se cumplió", "Umbral de la §8 que se cumplió"),
    ("la §7 de la ficha manda", "la §8 de la ficha manda"),
    ("que la §5 de la ficha fijó", "que la §6 de la ficha fijó"),
    ("Pregunta (§5 de la ficha)", "Pregunta (§6 de la ficha)"),
    ("Condicionales de la §6 que se cumplieron", "Condicionales de la §7 que se cumplieron"),
    ("Las tres preguntas de la §5 de la ficha", "Las tres preguntas de la §6 de la ficha"),
]

# 5 · Índice. Ojo: «(§4: máximo 3 estudiantes» y «caso a caso** (§4)» son del INSTRUCTIVO,
#     y los «§3» son del `4 - Evaluacion.md` o del propio índice: no se tocan.
INDICE_REFS = [
    ("(ficha §8)", "(ficha §9)"),
    ("Rango anticipado (§7)", "Rango anticipado (§8)"),
    ("advertencia de §7 de su ficha", "advertencia de §8 de su ficha"),
    ("los umbrales de la §7 de cada ficha", "los umbrales de la §8 de cada ficha"),
    ("**§7.1 de `1 - Ficha de preparacion`", "**§8.1 de `1 - Ficha de preparacion`"),
    ("su §7 anticipa", "su §8 anticipa"),
    ("con una §7 de 4,0-4,5", "con una §8 de 4,0-4,5"),
    ("sale de la §7 de cada ficha", "sale de la §8 de cada ficha"),
    ("en la §8 de la ficha del grupo", "en la §9 de la ficha del grupo"),
    ("con los umbrales de la §7,", "con los umbrales de la §8,"),
    (
        "las 8 secciones de siempre: resumen, huecos con página, preguntas, umbrales",
        "las 9 secciones de siempre: resumen, coherencia, fortalezas, **huecos del documento**,"
        " **huecos de las diapositivas**, preguntas antes y después, umbrales, administrativas",
    ),
    (
        "leer de `1 - Ficha de preparacion` solo las secciones 1 y 4: cinco minutos de resumen"
        " y los huecos con página.",
        "leer de `1 - Ficha de preparacion` solo las secciones 1, 4 y 5: cinco minutos de"
        " resumen, los huecos del documento y —en una pasada rápida— lo que hay que mirar en"
        " pantalla mientras proyectan.",
    ),
]

# 6 · LEEME de la carpeta.
LEEME_REFS = [
    (
        "las 8 secciones de siempre: resumen de 5 minutos, coherencia, fortalezas, huecos con"
        " página, preguntas antes y después, umbrales de nota, observaciones administrativas"
        " — más la **§7.1**",
        "las 9 secciones de siempre: resumen de 5 minutos, coherencia, fortalezas, **huecos del"
        " documento**, **huecos de las diapositivas** (qué proyectan y qué mirar en pantalla),"
        " preguntas antes y después, umbrales de nota, observaciones administrativas — más la"
        " **§8.1**",
    ),
    (
        "de la ficha, solo la §1 (resumen) y la §4 (huecos con\npágina).",
        "de la ficha, solo la §1 (resumen), la §4 (huecos del\ndocumento) y la §5 (qué mirar en"
        " pantalla mientras proyectan).",
    ),
    ("lleva ese mismo dato a la §7.1 de la ficha", "lleva ese mismo dato a la §8.1 de la ficha"),
    ("los umbrales que la §7 de cada ficha", "los umbrales que la §8 de cada ficha"),
]

# 7 · El guion que escribe el formulario en las fichas trae los anclajes numerados a mano.
# Es el más delicado de todos: este guion no solo *habla* de las secciones, las **escribe**.
# Si sus plantillas siguen diciendo «§7», la próxima corrida deshace la renumeración.
FORMULARIO_PY = [
    ('ANCLA_FICHA = "### 7.1 ', 'ANCLA_FICHA = "### 8.1 '),
    ('CORTE_FICHA = "\\n## 8. Observaciones', 'CORTE_FICHA = "\\n## 9. Observaciones'),
    ("los umbrales de la §7 de la ficha", "los umbrales de la §8 de la ficha"),
    ("umbrales de esta §7.", "umbrales de esta §8."),          # va dentro de la ficha
    ("desde la §7.1 de la ficha", "desde la §8.1 de la ficha"),  # va dentro de la hoja
    ("(la §7.1 trae", "(la §8.1 trae"),                          # idem
    ("· §7.1 {accion}", "· §8.1 {accion}"),                      # solo la traza en pantalla
]

# `formulario_jurado.py` escribe la §3 del `4 - Evaluacion.md` y la §2.1 del índice, y en esos
# textos remite a la ficha: misma trampa que el anterior. Sus propias §1–§4 no se tocan.
FORMULARIO_JURADO_PY = [
    ("la §7 de la ficha manda", "la §8 de la ficha manda"),
    ("Las tres preguntas de la §5 de la ficha", "Las tres preguntas de la §6 de la ficha"),
    ("**§7.1 de `1 - Ficha de preparacion`", "**§8.1 de `1 - Ficha de preparacion`"),
    ("su §7 anticipa", "su §8 anticipa"),
    ("con una §7 de 4,0-4,5", "con una §8 de 4,0-4,5"),
    ("sale de la §7 de cada ficha", "sale de la §8 de cada ficha"),
]

# `preguntas_en_tres_sitios.py` no escribe en las fichas, pero su documentación es lo primero
# que se lee cuando la sincronía falla: si dice «§5», manda a la sección equivocada.
TRES_SITIOS_PY = [
    ("Manda la §5 de la ficha", "Manda la §6 de la ficha"),
    ("La §7 y §7.1 de la ficha", "La §8 y §8.1 de la ficha"),
    ("la §5 de la ficha da {len(f_q)}", "la §6 de la ficha da {len(f_q)}"),
]

# Remisiones que después de traducir NO pueden quedar en pie, con la explicación de por qué.
# Es la red de seguridad de verdad: si el censo a mano se me quedó corto, aquí sale.
PROHIBIDAS = [
    ("§7 de la ficha", "los umbrales pasaron a ser la §8"),
    ("§7.1 de la ficha", "el formulario pasó a ser la §8.1"),
    ("§7.1 de `1 - Ficha", "el formulario pasó a ser la §8.1"),
    ("esta §7", "los umbrales pasaron a ser la §8"),
    ("§6 de la ficha)", "los condicionales pasaron a ser la §7"),
    ("§5 de la ficha", "las preguntas pasaron a ser la §6"),
    ("§5 preguntas", "el rótulo viejo de la cabecera del `4 - Evaluacion.md`"),
    ("§7 umbrales", "el rótulo viejo de la cabecera del `4 - Evaluacion.md`"),
    ("ficha §8)", "las administrativas pasaron a ser la §9"),
    ("las 8 secciones", "ahora son 9"),
    ("## 4. Debilidades", "la §4 se retituló OBSERVACIONES DEL DOCUMENTO"),
]
# Excepciones: «§N» que NO son de la ficha y no se tocan nunca.
AJENAS = [
    "§5.1 Alcances",     # apartado del trabajo de grado de G-002
    "(§5.1, p. 23)",     # idem
    "§9.2 de la p. 11",  # instructivo AFI
    "§3 de `4 - Evalua", "§3 de su `4 - Evalua", "§3 de este documento", "§3 B",
    "(§4: **máximo 3", "caso a caso** (§4)",  # resumen del instructivo
]


def aplica(texto: str, reglas) -> tuple:
    """Devuelve (texto_nuevo, nº de sustituciones). Descendente y por frase completa."""
    n = 0
    for viejo, nuevo in reglas:
        if viejo in texto:
            n += texto.count(viejo)
            texto = texto.replace(viejo, nuevo)
    return texto, n


def prohibidas(texto: str, reglas) -> list:
    """Renglones que conservan una remisión vieja, ya descontadas las ajenas.

    Se descuenta también lo que las propias reglas acaban de escribir: al correr 6→7 nace un
    «(§7 de la ficha)» legítimo que, sin enmascarar, se confundiría con el §7 viejo.
    """
    fuera = []
    recien_escrito = [nuevo for _, nuevo in reglas]
    for i, linea in enumerate(texto.splitlines(), 1):
        limpia = linea
        for nuevo in recien_escrito:
            limpia = limpia.replace(nuevo.split("\n")[0], "")
        for ajena in AJENAS:
            limpia = limpia.replace(ajena, "")
        for mala, por_que in PROHIBIDAS:
            if mala in limpia:
                fuera.append((i, mala, por_que, linea.strip()[:100]))
    return fuera


def main() -> int:
    escribir = "--confirmar" in sys.argv
    if not escribir and "--simular" not in sys.argv:
        print(__doc__)
        return 2

    if not os.path.isdir(FICHAS):
        print(f"No encontré la carpeta de fichas: {FICHAS}")
        return 1

    trabajos = []  # (ruta, reglas)
    for nombre in sorted(os.listdir(FICHAS)):
        carpeta = os.path.join(FICHAS, nombre)
        if not os.path.isdir(carpeta) or not nombre[:2].isdigit():
            continue
        trabajos.append((os.path.join(carpeta, "1 - Ficha de preparacion.md"),
                         FICHA_TITULOS + FICHA_REFS))
        trabajos.append((os.path.join(carpeta, "2 - Hoja de respuestas.md"), HOJA_REFS))
        trabajos.append((os.path.join(carpeta, "4 - Evaluacion.md"), EVAL_REFS))
    trabajos.append((os.path.join(FICHAS, "00 - Indice y agenda de sustentaciones.md"),
                     INDICE_REFS))
    trabajos.append((os.path.join(FICHAS, "LEEME.md"), LEEME_REFS))
    trabajos.append((os.path.join(AQUI, "formulario_en_fichas.py"), FORMULARIO_PY))
    trabajos.append((os.path.join(AQUI, "formulario_jurado.py"), FORMULARIO_JURADO_PY))
    trabajos.append((os.path.join(AQUI, "preguntas_en_tres_sitios.py"), TRES_SITIOS_PY))

    total, tocados, pendientes = 0, 0, []
    usadas = {viejo: 0 for _, reglas in trabajos for viejo, _ in reglas}
    for ruta, reglas in trabajos:
        if not os.path.isfile(ruta):
            print(f"  ·  falta (se salta): {os.path.relpath(ruta, REPO)}")
            continue
        # Cada archivo conserva su propio fin de renglón: en esta carpeta hay CRLF (casi todo,
        # viene de Word y de Drive) y LF (el LEEME). Unificarlos ensuciaría el diff completo.
        with open(ruta, "rb") as fh:
            fin = "\r\n" if b"\r\n" in fh.read() else "\n"
        with open(ruta, encoding="utf-8") as fh:
            original = fh.read()
        for viejo, _ in reglas:
            usadas[viejo] += original.count(viejo)
        nuevo, n = aplica(original, reglas)
        rel = os.path.relpath(ruta, REPO)
        if n:
            tocados += 1
            total += n
            print(f"  ✔ {n:3d} cambios · {rel}")
            if escribir:
                with open(ruta, "w", encoding="utf-8", newline=fin) as fh:
                    fh.write(nuevo)
        else:
            print(f"  ·    0 cambios · {rel}")
        resto = prohibidas(nuevo, reglas)
        if resto:
            pendientes.append((rel, resto))

    print(f"\n{total} sustituciones en {tocados} archivos"
          f" ({'ESCRITAS' if escribir else 'simulación, no se escribió nada'})")

    # Regla que nunca disparó = frase que censé mal, o que ya se tradujo en una corrida previa.
    huerfanas = [v for v, c in usadas.items() if c == 0]
    if huerfanas:
        print(f"\n· {len(huerfanas)} reglas sin uso (ya traducidas antes, o mal censadas):")
        for v in huerfanas:
            print(f"   «{v[:70]}»")

    if pendientes:
        print("\n⚠ Remisiones VIEJAS en pie — hay que arreglarlas a mano:")
        for rel, resto in pendientes:
            for i, mala, por_que, linea in resto:
                print(f"   {rel}:{i}  «{mala}» → {por_que}\n      {linea}")
        return 1
    print("Sin remisiones viejas en pie: numeración coherente en los 5 tipos de archivo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
