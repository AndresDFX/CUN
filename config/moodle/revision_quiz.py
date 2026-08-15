"""Las «Opciones de revisión» de un cuestionario de CDigital: censarlas y cambiarlas.

Por qué existe aparte de `cdigital.py`
-------------------------------------
Un cuestionario con **más de un intento**, calificado por **nota más alta** y con «la respuesta
correcta» encendida *mientras está abierto* no es un cuestionario: el intento 1 sirve para leer la
clave y el intento 2 para transcribirla. Es el valor por omisión de Moodle, y así vino el Quiz de
Proyecto I (aula `130378`, cmid `7563699`, 25% del corte, 50 estudiantes matriculados).

`cdigital.py` no sabe tocar estas 32 casillas: Moodle 4.5 no expone servicio web para ellas y hay
que reenviar el formulario completo de `modedit.php`, igual que hace `fijar_fechas`. Este script
reutiliza exactamente esa maquinaria —`_campos_formulario`, `_boton_guardar`, `_diferencias`— y su
misma red de seguridad: el **round-trip nulo**. Antes de escribir nada, reenvía el formulario tal
como vino y comprueba que no cambió ni un ajuste; si el reenvío idéntico altera algo, el parser no
es fiel y aborta sin tocar el aula.

Las 32 casillas son el producto de 8 cosas por 4 momentos, y en este Moodle los campos del
formulario se llaman **planos** —`attemptduring`, `correctnessimmediately`—, no `reviewattempt[during]`
como dice la documentación. Buscar `reviewattempt` en el HTML no encuentra nada.

La columna `during` no se toca nunca: con `preferredbehaviour = deferredfeedback` es inerte, y
Moodle la deshabilita por JavaScript, así que el navegador ni la manda.

Uso
---
    python revision_quiz.py censar 7563699 6522194 ...       # solo mira, no escribe
    python revision_quiz.py pregrado 6522194                 # simula
    python revision_quiz.py pregrado 6522194 --confirmar     # escribe

Se niega a escribir si el cuestionario **ya tiene intentos**: cambiar las reglas a mitad de camino
le cambia el trato a quien ya contestó.
"""
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import cdigital as C

CAMPOS = ["attempt", "correctness", "maxmarks", "marks",
          "specificfeedback", "generalfeedback", "rightanswer", "overallfeedback"]
COLUMNAS = ["during", "immediately", "open", "closed"]
TODO = set(CAMPOS)

# Cada perfil dice qué debe quedar encendido en las tres columnas que sí se tocan.
# `maxmarks` («sobre 1,00») va siempre con `marks`: sin él la nota sale sin denominador.
PERFILES = {
    # Lo que traen los 18 cuestionarios de Pregrado. Nunca muestra la clave, ni al cerrar: el
    # banco de preguntas se reimporta en cada edición del curso y así no se filtra.
    "pregrado": {"immediately": {"maxmarks", "marks"},
                 "open":        {"maxmarks", "marks"},
                 "closed":      {"attempt", "maxmarks", "marks"}},
    # Mientras está abierto solo ve su nota; al cerrar se abre todo y ahí aprende. Es lo que
    # quedó en el Quiz de Proyecto I el 15/08/2026.
    "formativo": {"immediately": {"attempt", "maxmarks", "marks"},
                  "open":        {"attempt", "maxmarks", "marks"},
                  "closed":      TODO},
    # El camino intermedio: al cerrar ve en qué falló y por qué, pero no queda transcrito el
    # enunciado correcto, así que el banco sigue sirviendo el semestre siguiente.
    "sin-clave": {"immediately": {"attempt", "maxmarks", "marks"},
                  "open":        {"attempt", "maxmarks", "marks"},
                  "closed":      TODO - {"rightanswer"}},
}


def leer(h: str) -> dict[str, bool]:
    """Qué casillas de revisión están marcadas, según el formulario de ajustes."""
    d = {}
    for col in COLUMNAS:
        for campo in CAMPOS:
            n = campo + col
            m = re.search(rf'<input[^>]*\bname="{n}"[^>]*>', h, re.I)
            if m:
                d[n] = "checked" in m.group(0).lower()
    return d


def _seleccion(h: str, nombre: str) -> str | None:
    """El `value` de la opción marcada de un `<select>`, o None."""
    m = re.search(rf'<select[^>]*\bname="{nombre}"[^>]*>(.*?)</select>', h, re.I | re.S)
    if not m:
        return None
    o = re.search(r'<option[^>]*value="([^"]*)"[^>]*selected|'
                  r'<option[^>]*selected[^>]*value="([^"]*)"', m.group(1), re.I | re.S)
    return (o.group(1) or o.group(2)) if o else None


def rejilla(estado: dict[str, bool], destino: dict[str, set] | None = None) -> str:
    """La tabla de 8x4, y con `destino` marca lo que va a cambiar."""
    lineas = [f"{'':18}" + "".join(f"{c:>16}" for c in COLUMNAS)]
    for campo in CAMPOS:
        fila = f"  {campo:16}"
        for col in COLUMNAS:
            ahora = estado[campo + col]
            quiere = ahora if (destino is None or col == "during") else (campo in destino[col])
            if ahora != quiere:
                fila += f"{('sí' if ahora else 'no') + ' -> ' + ('SÍ' if quiere else 'NO'):>16}"
            else:
                fila += f"{('sí' if ahora else '·'):>16}"
        lineas.append(fila)
    return "\n".join(lineas)


def _casilla(campos, nombre: str, encender: bool):
    """Enciende o apaga una casilla imitando lo que manda el navegador.

    Moodle usa el patrón `advcheckbox`: un `<input type="hidden" name="X" value="0">` seguido del
    `<input type="checkbox" name="X" value="1">`. Se quita el par `("X", "1")` y, si hay que
    encender, se añade al final. El `"0"` se deja donde estaba: PHP se queda con el último valor,
    así que el orden hace el trabajo.
    """
    fuera = [(k, v) for k, v in campos if not (k == nombre and v == "1")]
    return fuera + [(nombre, "1")] if encender else fuera


def censar(cd: C.CDigital, cmid: int) -> dict:
    """Lee el estado sin escribir nada. Devuelve lo que hace falta para juzgarlo."""
    h = cd.get(f"/course/modedit.php?update={cmid}").text
    est = leer(h)
    faltan = [c + col for col in COLUMNAS for c in CAMPOS if c + col not in est]
    if faltan:
        raise SystemExit(f"cmid {cmid}: el formulario no trae {len(faltan)} casillas: {faltan[:6]}")
    # La fuga que importa: la clave (o lo que la insinúa) visible mientras el cuestionario está
    # abierto, en un cuestionario que permite repetir.
    fuga = sorted({c for c in ("rightanswer", "correctness", "specificfeedback", "generalfeedback")
                   if est[c + "immediately"] or est[c + "open"]})
    intentos_permitidos = _seleccion(h, "attempts") or "0"
    return {"html": h, "estado": est, "fuga": fuga,
            "nombre": (re.search(r'name="name"[^>]*value="([^"]*)"', h) or [None, "?"])[1],
            "curso": int((re.search(r'name="course"[^>]*value="(\d+)"', h) or [None, 0])[1]),
            "comportamiento": _seleccion(h, "preferredbehaviour"),
            "intentos_permitidos": intentos_permitidos,
            "metodo": _seleccion(h, "grademethod"),
            "intentos_hechos": C._intentos(cd, cmid),
            # Con un solo intento, ver la clave al enviar ya no sirve para mejorar la nota.
            "regala_nota": bool(fuga) and intentos_permitidos != "1"}


def aplicar(cd: C.CDigital, cmid: int, perfil: str, confirmar: bool) -> int:
    destino = PERFILES[perfil]
    info = censar(cd, cmid)
    h, est = info["html"], info["estado"]
    print(f"«{info['nombre']}» · cmid {cmid} · aula {info['curso']} · "
          f"{info['comportamiento']} · {info['intentos_permitidos']} intento(s) permitidos · "
          f"{info['intentos_hechos']} hechos")
    if info["intentos_hechos"]:
        print("   !!! ABORTO: ya hay intentos; no se le cambian las reglas a quien ya contestó.")
        return 1

    cambios = [(c + col, c in destino[col])
               for col in COLUMNAS if col != "during"
               for c in CAMPOS if est[c + col] != (c in destino[col])]
    print(rejilla(est, destino))
    print(f"   casillas a cambiar: {len(cambios)}")
    if not cambios:
        print("   ya está en ese perfil")
        return 0
    if not confirmar:
        print("   SIMULACIÓN: no se envió nada (falta --confirmar)")
        return 0

    campos = C._campos_formulario(h)
    boton = C._boton_guardar(h)

    # Round-trip nulo: si reenviar el formulario tal cual altera algo, el parser no es fiel.
    cd.post("/course/modedit.php", campos + [(boton, "Guardar")])
    h2 = cd.get(f"/course/modedit.php?update={cmid}").text
    difs = C._diferencias(campos, C._campos_formulario(h2))
    if difs:
        print("   !!! ABORTO: el reenvío idéntico cambió ajustes, no puedo confiar en el parser:")
        for d in difs[:10]:
            print(f"       {d}")
        return 1

    campos = C._campos_formulario(h2)
    for n, quiere in cambios:
        campos = _casilla(campos, n, quiere)
    cd.post("/course/modedit.php", campos + [(boton, "Guardar")])

    # Verificar releyendo el servidor: las 32 casillas, no solo las que se pidieron, y que no se
    # movió nada de lo que de verdad duele si se pierde.
    h3 = cd.get(f"/course/modedit.php?update={cmid}").text
    fin = leer(h3)
    malas = [f"{c}{col}: pedí {c in destino[col]} y quedó {fin[c + col]}"
             for col in COLUMNAS if col != "during"
             for c in CAMPOS if fin[c + col] != (c in destino[col])]
    intactos = []
    for k in ("attempts", "grademethod", "preferredbehaviour", "questionsperpage", "shuffleanswers",
              "navmethod", "browsersecurity"):
        a, b = _seleccion(h, k), _seleccion(h3, k)
        if a != b:
            intactos.append(f"{k}: {a} -> {b}")
    for k in ("grade", "timelimit[number]", "timelimit[timeunit]"):
        def val(x):
            m = re.search(rf'<input[^>]*\bname="{re.escape(k)}"[^>]*>', x, re.I)
            v = re.search(r'value="([^"]*)"', m.group(0)) if m else None
            return v.group(1) if v else None
        if val(h) != val(h3):
            intactos.append(f"{k}: {val(h)} -> {val(h3)}")
    for pref in ("timeopen", "timeclose"):
        if C._leer_fecha(h, pref) != C._leer_fecha(h3, pref):
            intactos.append(f"{pref}: {C._leer_fecha(h, pref)} -> {C._leer_fecha(h3, pref)}")

    for m in malas + intactos:
        print(f"   !!! {m}")
    print(f"   {'OK' if not (malas or intactos) else 'CON PROBLEMAS'} · "
          f"verificado releyendo el servidor · perfil «{perfil}»")
    print(rejilla(fin))
    return 1 if (malas or intactos) else 0


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows llega en cp1252
    confirmar = "--confirmar" in argv
    resto = [a for a in argv[1:] if not a.startswith("--")]
    if len(resto) < 2 or resto[0] not in (*PERFILES, "censar"):
        print(__doc__)
        print(f"perfiles: {', '.join(PERFILES)}  ·  o «censar» para solo mirar")
        for nombre, d in PERFILES.items():
            print(f"\n  {nombre}")
            for col in ("immediately", "open", "closed"):
                print(f"    {col:14} {', '.join(sorted(d[col])) or '(nada)'}")
        return 2
    modo, cmids = resto[0], [int(x) for x in resto[1:]]

    cd = C.CDigital()
    cd.entrar()
    if modo == "censar":
        print(f"{'cmid':9} {'aula':7} {'perm':>5} {'hechos':>7} {'método':4} "
              f"{'fuga mientras abierto':34} {'al cerrar ve':14}")
        malos = 0
        for cmid in cmids:
            i = censar(cd, cmid)
            cerrado = [c for c in CAMPOS if i["estado"][c + "closed"]]
            malos += i["regala_nota"]
            print(f"{cmid:<9} {i['curso']:<7} {i['intentos_permitidos']:>5} "
                  f"{i['intentos_hechos']:>7} {str(i['metodo']):>6} "
                  f"{(', '.join(i['fuga']) if i['fuga'] else 'ninguna'):34} "
                  f"{(str(len(cerrado)) + ' de 8' if cerrado else 'NADA'):14}"
                  f"{'  <-- regala la nota' if i['regala_nota'] else ''}")
        print(f"\nque regalan la nota (fuga + más de 1 intento): {malos} de {len(cmids)}")
        return 1 if malos else 0

    malas = 0
    for cmid in cmids:
        malas += aplicar(cd, cmid, modo, confirmar)
        print()
    return 1 if malas else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
