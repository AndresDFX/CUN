# -*- coding: utf-8 -*-
"""Notas de cierre — baja el libro de calificaciones de CDigital y dice qué falta para cerrar.

**ESTE SCRIPT SOLO LEE.** No tiene `--confirmar` porque no hay nada que confirmar: todas las
peticiones son GET (la única escritura es el POST de inicio de sesión de `cdigital.py`). Se puede
correr sobre un aula con estudiantes matriculados sin más precaución que la de siempre.

QUÉ CONTESTA
------------
1. **Fiabilidad**: ¿el aula califica como dice el repositorio? Compara los ítems, los pesos
   efectivos, la escala y el número de estudiantes del aula contra
   `config/cursos/fechas_entrega_aca.py` y contra el roster de `2026/<grupo>/`.
2. **Cierre**: ¿qué falta? Por ítem, cuántos estudiantes tienen nota y cuántos no; en las tareas,
   cuántas entregas están pendientes de calificar; en los foros, cuántas discusiones no tienen
   respuesta del Docente; y la nota final proyectada de cada estudiante con los pesos del curso.

REPLICABLE A CUALQUIER CURSO
----------------------------
No hay ni un nombre de curso escrito en la lógica. Todo sale de dos tablas:

  · `cdigital.AULAS_CURSO`      aula de CDigital → (curso del repositorio, grupo)
  · `fechas_entrega_aca`        ítems, pesos, cortes y ventanas de ese curso

Para añadir un curso nuevo basta declararlo ahí (y en `carga_academica_2026.json`); este script no
se toca. Por eso la fiabilidad se mide corriéndolo sobre **todas** las aulas existentes: si los
controles pasan en las siete, el modelo describe el aula y no una de ellas en particular.

LO QUE CUESTA UN RATO DESCUBRIR (y por qué el código hace lo que hace)
---------------------------------------------------------------------
· **La columna «Nombre de usuario» del libro de calificaciones ES LA CÉDULA.** El informe del
  calificador la sirve en `<td class="userfield userusername">`. Este script la descarta al
  parsear —ni la guarda en memoria— porque ningún archivo del repositorio puede llevar cédulas.
  Nombre y correo institucional sí: ya están en `2026/<grupo>/Listado estudiantes (CDigital).csv`.
· **El informe del calificador pagina de 20 en 20.** Sin `perpage` alto, un aula de 50 reporta 20
  estudiantes y todo lo demás sale mal callado.
· **`-` en una celda es «sin calificar», no un cero.** Son cosas distintas al cerrar: por eso el
  informe cuenta «con nota / falta» y, aparte, proyecta la final poniendo en 0 lo que falta.
· **El «Total del curso» de Moodle NO es la nota final mientras el curso corre**: agrega solo los
  ítems ya calificados (`aggregateonlygraded`). Comparar la final proyectada contra ese total es un
  error; lo que sí se puede comparar —y este script compara— es el total de Moodle contra el mismo
  cálculo restringido a los ítems calificados.
· **Los pesos del árbol son relativos a la categoría, no al curso.** En estas aulas el árbol es
  curso → NOTA UNICA (1.0) → PRIMER/SEGUNDO/TERCER CORTE (0.3/0.3/0.4) → ítems (0.06, 0.24…). El
  peso efectivo de un ítem es el producto de su cuota entre hermanos por la de cada antepasado.
  Da exactamente el porcentaje del repositorio, y así se verifica.
· **La escala es 0,00–5,00 por ítem** (columna «Rango» del árbol), no 0–100. No se asume: se lee.
· **La nota para aprobar no está declarada** en estas aulas (`gradepass = 0,00` en los ítems), así
  que este script **no dice quién aprueba**. Eso lo decide el Docente con el Reglamento.

USO
---
    python config/moodle/notas_cierre.py                        # las 7 aulas: fiabilidad + cierre
    python config/moodle/notas_cierre.py --curso 111070         # una aula (repetible)
    python config/moodle/notas_cierre.py --fiabilidad           # solo los controles del modelo
    python config/moodle/notas_cierre.py --notas                # + nota final por estudiante
    python config/moodle/notas_cierre.py --informe              # escribe CIERRE_NOTAS_CDIGITAL.md
    python config/moodle/notas_cierre.py --detalle              # CSV por estudiante FUERA del repo

`--informe` escribe en el repositorio y por eso **solo lleva agregados** (ni notas individuales ni
cédulas). El detalle por estudiante va a `%LOCALAPPDATA%\\cdigital-cun\\cierre\\` con `--detalle`,
fuera de git y fuera de Drive.

Sale 1 si algún control de fiabilidad falla; 0 si todos pasan (aunque falten notas: eso no es un
fallo del modelo, es el estado del curso).
"""
from __future__ import annotations

import argparse
import csv
import html
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))          # cdigital.py
sys.path.insert(0, str(RAIZ / "config" / "cursos"))               # fechas_entrega_aca.py

import cdigital as cd            # noqa: E402
import fechas_entrega_aca as fe  # noqa: E402
from carga_academica import curso as curso_cfg  # noqa: E402

for _f in (sys.stdout, sys.stderr):
    if hasattr(_f, "reconfigure"):
        _f.reconfigure(encoding="utf-8", errors="replace")

INFORME_REPO = RAIZ / "CIERRE_NOTAS_CDIGITAL.md"
CARPETA_DETALLE = Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))) / "cdigital-cun" / "cierre"
TOLERANCIA = 0.011   # el libro muestra 2 decimales; por debajo de esto es redondeo, no discrepancia


# =============================================================================================
# Lectura del aula (todo GET)
# =============================================================================================
@dataclass
class Item:
    """Una fila del árbol del libro de calificaciones: ítem u categoría."""

    itemid: str
    nombre: str
    nivel: int
    peso: float | None          # el valor crudo del input weight_ (relativo a su categoría)
    grademax: float | None
    tipo: str = ""              # «Cuestionario» / «Tarea» / «Foro» (vacío en categorías)
    cmid: str | None = None
    modulo: str | None = None   # quiz | assign | forum
    agregacion: str = ""
    categoria: bool = False
    efectivo: float | None = None   # peso sobre el curso completo (0..1), calculado
    padre: str | None = None
    visible: bool = True            # visible para el estudiante en el aula


@dataclass
class Alumno:
    userid: str
    nombre: str
    correo: str
    notas: dict[str, float | None] = field(default_factory=dict)


def _num(txt: str | None) -> float | None:
    """«4,50» / «4.50» / «-» / «» → float o None. El libro va en coma decimal."""
    if txt is None:
        return None
    t = html.unescape(txt).replace("\xa0", " ").strip()
    t = re.sub(r"<[^>]+>", "", t).strip()
    if t in ("", "-", "–", "—"):
        return None
    t = t.replace("%", "").replace(" ", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def arbol(cli: cd.CDigital, curso: int) -> list[Item]:
    """El árbol del libro de calificaciones de `/grade/edit/tree/index.php`, en orden.

    De cada fila saca: nombre, nivel de anidación, peso, rango (nota máxima), tipo de actividad,
    el **cmid** de la actividad que la respalda (del href del enlace) y la agregación de la
    categoría. El cmid es lo que después permite ir a mirar entregas, intentos o mensajes del foro
    sin adivinar por el nombre.
    """
    pagina = cli.get("/grade/edit/tree/index.php", params={"id": curso}).text
    filas = re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", pagina)
    items: list[Item] = []
    for f in filas:
        m_niv = re.search(r"column-name\s+level(\d+)", f)
        if not m_niv:
            continue
        nivel = int(m_niv.group(1))
        m_w = re.search(r'name="weight_(\d+)"[^>]*value="([^"]*)"', f)
        m_nom = re.search(r'(?is)<div class="rowtitle">(.*?)</div>', f)
        nombre = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m_nom.group(1)))).strip() \
            if m_nom else ""
        m_mod = re.search(r'(?is)class="gradeitemheader[^"]*"[^>]*href="[^"]*/mod/(\w+)/view\.php\?id=(\d+)"', f)
        m_tipo = re.search(r'(?is)<span class="[^"]*dimmed_text[^"]*">(.*?)</span>', f)
        m_rango = re.search(r'(?is)<td class="[^"]*column-range[^"]*"[^>]*>(.*?)</td>', f)
        m_agr = re.search(r"(?is)category_grade_icons.*?<strong>(.*?)</strong>", f)
        es_cat = m_mod is None and bool(re.search(r'(?is)category_grade_icons', f))
        if not m_w and not nombre:
            continue
        items.append(Item(
            itemid=m_w.group(1) if m_w else f"nivel{nivel}",
            nombre=nombre or "(sin nombre)",
            nivel=nivel,
            peso=_num(m_w.group(2)) if m_w else None,
            grademax=_num(m_rango.group(1)) if m_rango else None,
            tipo=re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m_tipo.group(1)))).strip()
            if m_tipo else "",
            cmid=m_mod.group(2) if m_mod else None,
            modulo=m_mod.group(1) if m_mod else None,
            agregacion=re.sub(r"\s+", " ", html.unescape(m_agr.group(1))).strip() if m_agr else "",
            categoria=es_cat,
        ))
    _pesos_efectivos(items)
    return items


def _pesos_efectivos(items: list[Item]) -> None:
    """Peso de cada ítem sobre el CURSO, no sobre su categoría.

    En una media ponderada, la cuota de un ítem dentro de su categoría es `w / Σw(hermanos)`, y su
    peso efectivo es esa cuota multiplicada por la de cada antepasado. Con el árbol
    curso → NOTA UNICA (1.0) → CORTE (0.3) → ítem (0.06) sale 0.06/0.3 × 0.3/1.0 = 6% — el mismo
    número que declara el repositorio, que es justo lo que hay que poder comprobar.

    El anidamiento se deduce del `levelN` de cada fila: las filas vienen en profundidad primero, así
    que el padre de una fila de nivel L es la última fila vista de nivel L-1.
    """
    ultimo_por_nivel: dict[int, Item] = {}
    for it in items:
        padre = ultimo_por_nivel.get(it.nivel - 1)
        it.padre = padre.itemid if padre else None
        ultimo_por_nivel[it.nivel] = it
        # los descendientes de esta fila se resuelven después; hay que limpiar niveles más profundos
        for n in [k for k in ultimo_por_nivel if k > it.nivel]:
            del ultimo_por_nivel[n]

    suma_hermanos: dict[str | None, float] = {}
    for it in items:
        if it.peso is not None:
            suma_hermanos[it.padre] = suma_hermanos.get(it.padre, 0.0) + it.peso

    por_id = {it.itemid: it for it in items}

    def efectivo(it: Item) -> float:
        if it.efectivo is not None:
            return it.efectivo
        padre = por_id.get(it.padre or "")
        arriba = efectivo(padre) if padre else 1.0
        if it.peso is None:
            # La fila raíz («Total del curso») no trae input de peso: no reparte nada, lo contiene
            # todo. Si se la trata como peso 0 —el error obvio— el 0 se propaga a todo el árbol y
            # los ocho ítems salen al 0,00 %.
            it.efectivo = arriba
        else:
            total = suma_hermanos.get(it.padre) or 0.0
            it.efectivo = (it.peso / total if total else 0.0) * arriba
        return it.efectivo

    for it in items:
        efectivo(it)


def calificador(cli: cd.CDigital, curso: int) -> tuple[dict[str, str], list[Alumno]]:
    """`(itemid → nombre de columna, alumnos con sus notas)` del informe del calificador.

    `perpage=1000` porque el informe pagina de 20 en 20 y una aula de 50 pasaría desapercibida.
    La columna «Nombre de usuario» del informe **es la cédula**: se ignora a propósito.
    """
    pagina = cli.get("/grade/report/grader/index.php",
                     params={"id": curso, "perpage": 1000}).text

    columnas: dict[str, str] = {}
    for itemid, cuerpo in re.findall(r'(?is)<th[^>]*data-itemid="(\d+)"[^>]*>(.*?)</th>', pagina):
        plano = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", cuerpo))).strip()
        # el encabezado repite el nombre: «Expandir columna Quiz 1 Quiz 1 Acciones de la celda …»
        plano = re.sub(r"^Expandir columna\s+", "", plano)
        plano = re.split(r"\s+Acciones de la celda", plano)[0].strip()
        mitad = len(plano) // 2
        if plano[:mitad].strip() and plano[:mitad].strip() == plano[mitad:].strip():
            plano = plano[:mitad].strip()
        columnas[itemid] = plano

    alumnos: list[Alumno] = []
    for fila in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", pagina):
        m_u = re.search(rf'/user/view\.php\?id=(\d+)&(?:amp;)?course={curso}"[^>]*>(.*?)</a>', fila)
        if not m_u:
            continue
        nombre = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m_u.group(2)))).strip()
        m_mail = re.search(r'(?is)<td[^>]*class="[^"]*useremail[^"]*"[^>]*>(.*?)</td>', fila)
        correo = re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", "", m_mail.group(1)))) \
            if m_mail else ""
        al = Alumno(userid=m_u.group(1), nombre=nombre, correo=correo)
        for celda in re.findall(r'(?is)<td[^>]*class="[^"]*gradecell[^"]*"[^>]*data-itemid="(\d+)"[^>]*>(.*?)</td>',
                                fila):
            val = re.search(r'(?is)<span class="gradevalue[^"]*">(.*?)</span>', celda[1])
            al.notas[celda[0]] = _num(val.group(1)) if val else None
        alumnos.append(al)
    return columnas, alumnos


def informe_usuario(cli: cd.CDigital, curso: int, userid: str) -> dict:
    """Lo que Moodle mismo declara sobre los pesos, leído del informe de UN estudiante.

    `/grade/report/user/index.php` trae dos columnas que no están en ninguna otra página:
    «Ponderación calculada» —la cuota del ítem DENTRO de su categoría, ya normalizada a 100 %— y
    «Rango». Sirven para cotejar el cálculo de pesos contra la aritmética de Moodle en vez de
    contra sí mismo: si el árbol dice 0,06 sobre 0,30 y Moodle dice «20,00 %», coinciden.

    El rango importa porque en estas aulas el «Total del curso» **no empieza en 0,00** sino en
    0,10, y entonces la nota que Moodle muestra no es la media ponderada sobre 0–5: es
    `mínimo + porcentaje × (máximo − mínimo)`. Sin leer el rango, cualquier comparación falla por
    una décima y parecería un error de cálculo.

    No se imprime ni se guarda nada de este estudiante: solo se usan los pesos, que son del curso.
    """
    pagina = cli.get("/grade/report/user/index.php",
                     params={"id": curso, "userid": userid}).text
    prefijos = ("Cálculo total", "Cuestionario", "Tarea", "Foro", "Taller", "Manual", "Texto")
    share: dict[str, float] = {}
    rango: dict[str, tuple[float | None, float | None]] = {}
    for fila in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", pagina):
        celdas = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
                  for c in re.findall(r"(?is)<t[hd][^>]*>(.*?)</t[hd]>", fila)]
        celdas = [c for c in celdas if c]
        if len(celdas) < 4:
            continue
        nombre = celdas[0]
        for pre in prefijos:
            if nombre.startswith(pre + " "):
                nombre = nombre[len(pre) + 1:]
                break
        clave = _norm(nombre)
        m = re.search(r"([\d.,]+)\s*%", celdas[1])
        if m:
            share[clave] = (_num(m.group(1)) or 0.0) / 100
        r = re.search(r"([\d.,]+)\s*[–—-]\s*([\d.,]+)", " ".join(celdas[2:5]))
        if r:
            rango[clave] = (_num(r.group(1)), _num(r.group(2)))
    return {"share": share, "rango": rango}


def efectivo_segun_moodle(it: Item, por_id: dict[str, Item], share: dict[str, float]) -> float | None:
    """Peso del ítem sobre el curso según las «Ponderación calculada» de Moodle, multiplicadas.

    La cuota de una categoría no está en su fila sino en la de su total («Total PRIMER CORTE»),
    porque el coeficiente de agregación de una categoría vive en su ítem de total —de hecho
    comparten el mismo id, y por eso `categoria.itemid` sirve para leer la nota de la categoría en
    el informe del calificador.
    """
    factores: list[float] = []
    actual: Item | None = it
    while actual is not None and actual.padre is not None:
        clave = _norm(("Total " + actual.nombre) if actual.categoria else actual.nombre)
        if clave not in share:
            return None
        factores.append(share[clave])
        actual = por_id.get(actual.padre or "")
    total = 1.0
    for f in factores:
        total *= f
    return total


def hijos_de(items: list[Item]) -> dict[str | None, list[Item]]:
    """Hijos que sí reparten peso. Las filas «Total X» se excluyen: son hermanas de su categoría,
    no hijas, y no llevan input de peso."""
    out: dict[str | None, list[Item]] = {}
    for it in items:
        if it.peso is not None:
            out.setdefault(it.padre, []).append(it)
    return out


def agregar(cat: Item, hijos: dict[str | None, list[Item]], al: Alumno) -> tuple[float, int, int]:
    """Agrega una categoría como la agrega esta aula: `(valor 0..1, hojas con nota, hojas en total)`.

    Estas aulas tienen **desactivado** «excluir calificaciones vacías»: se comprobó en el aula, no
    se supone. Con Quiz 1 en 5,00 y Parcial 1 sin calificar, PRIMER CORTE marca 1,00 = 20 %, que es
    exactamente `(1 × 0,06 + 0 × 0,24) / 0,30`. Es decir: **lo no calificado ya cuenta como cero**,
    así que el «Total del curso» de Moodle no es una nota parcial, es una proyección de cierre.
    """
    num = den = 0.0
    con = tot = 0
    for h in hijos.get(cat.itemid, []):
        den += h.peso or 0.0
        if h.categoria:
            v, c, t = agregar(h, hijos, al)
            num += v * (h.peso or 0.0)
            con += c
            tot += t
        else:
            tot += 1
            nota = al.notas.get(h.itemid)
            if nota is not None and h.grademax:
                num += (nota / h.grademax) * (h.peso or 0.0)
                con += 1
    return (num / den if den else 0.0), con, tot


def resumen_tarea(cli: cd.CDigital, cmid: str) -> dict[str, int | None]:
    """Participantes / enviados / pendientes por calificar de una tarea."""
    plano = cd._texto(cli.get(f"/mod/assign/view.php?id={cmid}").text)
    def campo(etiqueta: str) -> int | None:
        m = re.search(etiqueta + r"\s*\|?\s*(\d+)", plano)
        return int(m.group(1)) if m else None
    return {"participantes": campo("Participantes"),
            "enviados": campo("Enviados"),
            "pendientes": campo("Pendientes por calificar")}


def resumen_foro(cli: cd.CDigital, cmid: str, docente: str) -> dict:
    """Discusiones del foro y cuáles no tienen respuesta (ni del Docente ni de nadie).

    «Respondido» aquí es lo que se puede comprobar leyendo el listado: número de respuestas > 0 y
    quién firmó la última. Un foro valorado sin ninguna discusión es participación cero, que al
    cerrar es lo mismo que un cuestionario sin intentos.
    """
    pagina = cli.get(f"/mod/forum/view.php?id={cmid}").text
    disc = []
    for fila in re.findall(r'(?is)<tr[^>]*class="[^"]*discussion[^"]*"[^>]*>(.*?)</tr>', fila_o(pagina)):
        d = re.search(r"discuss\.php\?d=(\d+)", fila)
        tit = re.search(r'(?is)discuss\.php\?d=\d+"[^>]*>(.*?)</a>', fila)
        autores = re.findall(r'(?is)class="mb-1 line-height-3 text-truncate">(.*?)</div>', fila)
        resp = re.search(r"(?is)<td[^>]*>\s*<span>(\d+)</span>\s*</td>", fila)
        if not d:
            continue
        limpio = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()
        disc.append({
            "d": d.group(1),
            "titulo": limpio(tit.group(1)) if tit else "(sin título)",
            "autor": limpio(autores[0]) if autores else "",
            "ultimo": limpio(autores[-1]) if len(autores) > 1 else (limpio(autores[0]) if autores else ""),
            "respuestas": int(resp.group(1)) if resp else 0,
        })
    sin_respuesta = [x for x in disc if x["respuestas"] == 0]
    sin_docente = [x for x in disc if _norm(docente) not in _norm(x["ultimo"])]
    return {"discusiones": disc, "sin_respuesta": sin_respuesta, "sin_docente": sin_docente}


def fila_o(pagina: str) -> str:
    """El listado de discusiones vive dentro de la tabla del foro; el resto de la página también
    trae `<tr>`s (bloques del tema lateral). Recortar por la tabla evita contar de más."""
    m = re.search(r"(?is)<table[^>]*>(.*?)</table>", pagina)
    return m.group(1) if m else pagina


def _norm(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return re.sub(r"[^a-z0-9 ]", "", "".join(c for c in s if not unicodedata.combining(c))).strip()


# =============================================================================================
# El modelo del repositorio
# =============================================================================================
def modelo(aula: int) -> tuple[str, str | None, list[fe.EntregaAca]]:
    """`(clave de curso, grupo, ítems con ventanas)` del repositorio para esa aula."""
    clave, grupo = cd.AULAS_CURSO[aula]
    return clave, grupo, fe.entregas_para_grupo(clave, grupo)


def roster(clave: str, grupo: str | None) -> int | None:
    """Estudiantes del listado del repositorio (`2026/<grupo>/`), o None si no está."""
    cfg = curso_cfg(clave)
    g = grupo or (list(cfg.get("groups") or [None]) or [None])[0]
    if not g:
        return None
    ruta = RAIZ / cfg["folder"] / "2026" / str(g) / "Listado estudiantes (CDigital).csv"
    if not ruta.is_file():
        return None
    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        return sum(1 for r in csv.DictReader(fh)
                   if (r.get("rol") or "").strip().lower().startswith("estud"))


def emparejar(entregas: list[fe.EntregaAca], items: list[Item]) -> dict[str, Item | None]:
    """Ítem del catálogo → fila del libro. El libro renombra alguno («Coevaluación» pasa a
    «Coevaluación calificación»), así que tras la coincidencia exacta se prueba por prefijo."""
    hojas = [i for i in items if not i.categoria and i.peso is not None]
    por_nombre = {_norm(i.nombre): i for i in hojas}
    out: dict[str, Item | None] = {}
    for e in entregas:
        clave = _norm(e.code)
        it = por_nombre.get(clave)
        if it is None:
            cands = [i for i in hojas if _norm(i.nombre).startswith(clave)
                     or clave.startswith(_norm(i.nombre))]
            it = cands[0] if len(cands) == 1 else None
        out[e.id] = it
    return out


# =============================================================================================
# Controles de fiabilidad
# =============================================================================================
@dataclass
class Control:
    ok: bool | None      # None = no verificable todavía (no es un fallo)
    texto: str
    aviso: bool = False  # el aula hace algo que hay que saber, pero el modelo no está roto


def controles(aula: int, clave: str, grupo: str | None, entregas: list[fe.EntregaAca],
              items: list[Item], pareja: dict[str, Item | None],
              alumnos: list[Alumno], columnas: dict[str, str],
              declarado: dict) -> list[Control]:
    out: list[Control] = []
    hojas = [i for i in items if not i.categoria and i.peso is not None]

    # 1. Todos los ítems del catálogo existen en el libro.
    faltan = [e.code for e in entregas if pareja[e.id] is None]
    out.append(Control(not faltan,
                       f"{len(entregas) - len(faltan)}/{len(entregas)} ítems del catálogo están en "
                       f"el libro" + (f" · NO están: {', '.join(faltan)}" if faltan else "")))

    # 2. Ítems del libro que el catálogo no conoce. Lo que importa no es que existan —las aulas CUN
    #    llegan con relleno de plantilla que trae ítem de nota— sino si **reparten peso**. Todos los
    #    que hay hoy están en 0 % y colgados del curso, fuera de NOTA UNICA: no mueven ninguna nota.
    #    Uno con peso > 0 sí diluiría los porcentajes del repositorio, y ese sí es un fallo.
    conocidos = {id(i) for i in pareja.values() if i is not None}
    extra = [i for i in hojas if id(i) not in conocidos]
    con_peso = [i.nombre for i in extra if (i.efectivo or 0) > 0.0005]
    if con_peso:
        out.append(Control(False, "ítems fuera del catálogo que SÍ reparten peso: "
                                  + ", ".join(con_peso)))
    elif extra:
        escalas_extra = " y ".join(f"0,00–{x:.2f}".replace(".", ",")
                                   for x in sorted({i.grademax for i in extra if i.grademax}))
        out.append(Control(True, f"aviso: {len(extra)} ítems de relleno de la plantilla con 0 % de "
                                 f"peso (escala {escalas_extra}) — no afectan la nota: "
                                 + ", ".join(i.nombre for i in extra)[:110], aviso=True))
    else:
        out.append(Control(True, "el libro no tiene ítems fuera del catálogo"))

    # 3. Peso EFECTIVO de cada ítem == peso del repositorio.
    difs = []
    for e in entregas:
        it = pareja[e.id]
        if it is None or it.efectivo is None:
            continue
        if abs(it.efectivo * 100 - e.weight) > 0.05:
            difs.append(f"{e.code} aula {it.efectivo * 100:.2f}% ≠ repo {e.weight}%")
    suma = sum((pareja[e.id].efectivo or 0) for e in entregas if pareja[e.id]) * 100
    out.append(Control(not difs and abs(suma - 100) < 0.1,
                       f"pesos efectivos iguales al repositorio · suman {suma:.1f} %".replace(".", ",")
                       if not difs else "pesos distintos: " + " · ".join(difs)))

    # 4. Una sola escala en los ítems que califican (no se asume 5,00: se lee). El relleno de la
    #    plantilla usa 0–1 y 0–100, pero pesa 0 %, así que su escala da igual.
    califican = [pareja[e.id] for e in entregas if pareja[e.id] is not None]
    escalas = sorted({i.grademax for i in califican if i.grademax is not None})
    out.append(Control(len(escalas) == 1,
                       f"escala única 0,00–{escalas[0]:.2f}".replace(".", ",")
                       + f" en los {len(califican)} ítems que califican"
                       if len(escalas) == 1 else
                       f"los ítems que califican no comparten escala: {escalas}"))

    # 5. Agregación de las categorías: si no es media ponderada, los % del repositorio no
    #    describen cómo suma Moodle, y entonces el cálculo de este script tampoco valdría.
    agr = sorted({i.agregacion for i in items if i.categoria and i.agregacion})
    ponderada = all("ponderada" in _norm(a) for a in agr) if agr else False
    out.append(Control(ponderada if agr else None,
                       f"agregación de las categorías: {', '.join(agr) or '(no visible)'}"))

    # 6. Estudiantes del libro contra el listado del repositorio. Que no cuadre NO es un fallo del
    #    modelo: el CSV es una foto del día que se descargó y la matrícula se mueve (retiros,
    #    ingresos tardíos). Es un aviso, y al cerrar hay que descargar el listado otra vez.
    n_roster = roster(clave, grupo)
    if n_roster is None:
        out.append(Control(None, f"{len(alumnos)} estudiantes en el libro · no hay listado en el "
                                 f"repositorio con el que comparar"))
    elif n_roster == len(alumnos):
        out.append(Control(True, f"{len(alumnos)} estudiantes en el libro = {n_roster} en el "
                                 f"listado del repositorio"))
    else:
        d = len(alumnos) - n_roster
        out.append(Control(True, f"aviso: {len(alumnos)} estudiantes en el libro y {n_roster} en el "
                                 f"listado del repositorio ({d:+d}) — la matrícula cambió desde que "
                                 f"se descargó el CSV; para cerrar, vuelve a descargarlo",
                           aviso=True))

    # 7. El peso calculado a mano contra el que Moodle declara en «Ponderación calculada». Este es
    #    el control fuerte: coteja la aritmética contra Moodle, no contra sí misma.
    por_id = {i.itemid: i for i in items}
    share = declarado.get("share") or {}
    iguales = distintos = 0
    sin_dato: list[str] = []
    for e in entregas:
        it = pareja[e.id]
        if it is None:
            continue
        m = efectivo_segun_moodle(it, por_id, share)
        if m is None:
            sin_dato.append(e.code)
        elif abs(m - (it.efectivo or 0)) < 0.0005:
            iguales += 1
        else:
            distintos += 1
    out.append(Control(None if not (iguales + distintos) else distintos == 0,
                       f"Moodle declara el mismo peso efectivo en {iguales}/{iguales + distintos} "
                       f"ítems" + (f" · sin ponderación declarada en el informe: "
                                   f"{', '.join(sin_dato)} (el árbol y el repositorio sí coinciden)"
                                   if sin_dato else "")))

    # 8. El «Total del curso» de esta aula no arranca en 0,00 (rango 0,10–5,00): la nota que muestra
    #    es `mínimo + porcentaje × (máximo − mínimo)`, no la media ponderada sobre 0–5. Es un aviso,
    #    no un fallo del modelo: los pesos de los ítems siguen siendo los del repositorio.
    rango = (declarado.get("rango") or {}).get(_norm("Total del curso"))
    if rango and rango[0]:
        out.append(Control(True, f"aviso: el «Total del curso» del aula va de {rango[0]:.2f} a "
                                 f"{rango[1]:.2f} — su mínimo no es 0,00, así que ese número no se "
                                 f"puede copiar como nota final sin convertirlo".replace(".", ","),
                           aviso=True))
    else:
        out.append(Control(True, "el «Total del curso» va de 0,00 a la nota máxima"))

    # 9. Cortes reproducibles: para cada categoría, recalcular su total y compararlo con el que
    #    sirve el libro. Se cotejan solo las categorías que ya tienen alguna nota, porque una
    #    categoría enteramente vacía no da 0,00 en estas aulas (control 10).
    cats = [i for i in items if i.categoria and i.peso is not None]
    hijos = hijos_de(items)
    cotejados = fallos = 0
    for cat in cats:
        for al in alumnos:
            moodle = al.notas.get(cat.itemid)
            v, con, tot = agregar(cat, hijos, al)
            if moodle is None or con == 0 or _tiene_cat_vacia(cat, hijos, al):
                continue
            cotejados += 1
            if abs(v * (cat.grademax or 5.0) - moodle) > TOLERANCIA:
                fallos += 1
    out.append(Control(None if not cotejados else fallos == 0,
                       f"los totales por categoría se reproducen en {cotejados - fallos}/{cotejados} "
                       f"casos (estudiante × corte con notas)" if cotejados else
                       "aún no hay ningún corte con notas: los totales no se pueden cotejar"))

    # 10. Categorías sin ninguna nota cuyo total no es 0,00. En estas aulas marcan 0,10 (2 %) y ese
    #     2 % se propaga hacia arriba, así que el «Total del curso» de hoy está inflado. Desaparece
    #     en cuanto el corte tiene una sola nota: PRIMER CORTE con Quiz 1 marca 20,00 % exacto.
    vacias = []
    for cat in cats:
        # «Sin ninguna nota» es del grupo entero, no de un estudiante: PRIMER CORTE tiene notas de
        # siete personas, así que mirar solo a la primera de la lista lo declararía vacío.
        calificadas = sum(agregar(cat, hijos, al)[1] for al in alumnos)
        vals = {al.notas.get(cat.itemid) for al in alumnos}
        vals = {x for x in vals if x is not None}
        if calificadas == 0 and vals and any(abs(x) > TOLERANCIA for x in vals):
            vacias.append(f"{cat.nombre} marca {max(vals):.2f}".replace(".", ","))
    if vacias:
        out.append(Control(True, "aviso: categorías sin ninguna nota que no marcan 0,00 — "
                                 + " · ".join(vacias)
                                 + ". Mientras eso pase, el total del aula está por encima de la "
                                   "nota real y no sirve para informar al estudiante", aviso=True))
    return out


def _tiene_cat_vacia(cat: Item, hijos: dict[str | None, list[Item]], al: Alumno) -> bool:
    """¿Alguna subcategoría de `cat` está entera sin calificar? Entonces el total de `cat` arrastra
    el 2 % del control 10 y compararlo sería comparar contra el defecto del aula."""
    for h in hijos.get(cat.itemid, []):
        if h.categoria:
            _, con, tot = agregar(h, hijos, al)
            if (tot and con == 0) or _tiene_cat_vacia(h, hijos, al):
                return True
    return False


# =============================================================================================
# Nota final
# =============================================================================================
@dataclass
class Final:
    alumno: Alumno
    proyectada: float       # lo no calificado cuenta 0 — la nota si el curso cerrara hoy
    con_lo_hecho: float | None   # solo sobre lo ya calificado, renormalizado — cómo va, no cuánto tiene
    aula: float | None      # el «Total del curso» tal como lo muestra Moodle, sin retocar
    faltantes: list[str]


def finales(entregas: list[fe.EntregaAca], pareja: dict[str, Item | None],
            alumnos: list[Alumno], total_id: str | None) -> list[Final]:
    """Tres números por estudiante, que no son el mismo y no se deben confundir:

    · **proyectada**: la nota si el curso cerrara hoy, con lo pendiente en 0. Es la que sirve para
      avisar a tiempo a quien va a perder.
    · **con_lo_hecho**: el promedio ponderado solo de lo ya calificado. Dice cómo le va a quien va
      al día, sin castigarlo por lo que todavía no se ha aplicado.
    · **aula**: lo que Moodle muestra, copiado sin tocar. No se corrige nunca: si no cuadra con lo
      anterior, el que tiene que cambiar es el aula, y quien lo cambia es el Docente.
    """
    out = []
    for al in alumnos:
        proy = num = den = 0.0
        faltan = []
        for e in entregas:
            it = pareja[e.id]
            if it is None:
                faltan.append(f"{e.code} (no está en el libro)")
                continue
            w = it.efectivo or 0.0
            nota = al.notas.get(it.itemid)
            if nota is None:
                faltan.append(e.code)
            else:
                proy += nota * w
                num += nota * w
                den += w
        out.append(Final(al, round(proy, 2), round(num / den, 2) if den else None,
                         al.notas.get(total_id) if total_id else None, faltan))
    return out


# =============================================================================================
# Informe por consola
# =============================================================================================
def marca(c: Control) -> str:
    if c.aviso:
        return "⚠"
    return "✓" if c.ok else ("—" if c.ok is None else "⛔")


def revisar(cli: cd.CDigital, aula: int, args) -> dict:
    clave, grupo, entregas = modelo(aula)
    cfg = curso_cfg(clave)
    titulo = f"{cfg.get('titulo_corto') or clave}" + (f" · grupo {grupo}" if grupo else "")

    items = arbol(cli, aula)
    # Estas aulas se alistan con todo OCULTO hasta que el Docente lo revisa, así que un ítem
    # calificable invisible es la falla más fácil de pasar por alto: el estudiante no puede entregar
    # y la nota nunca va a existir. La visibilidad se lee del estado real del aula, no del libro.
    estado = {str(m["id"]): m for m in cli.estado_curso(aula).get("cm", [])}
    for it in items:
        if it.cmid:
            it.visible = bool(estado.get(it.cmid, {}).get("visible", True))
    columnas, alumnos = calificador(cli, aula)
    pareja = emparejar(entregas, items)
    # Un solo informe de estudiante por aula: los pesos que trae son del curso, no suyos.
    declarado = informe_usuario(cli, aula, alumnos[0].userid) if alumnos else {}
    ctrls = controles(aula, clave, grupo, entregas, items, pareja, alumnos, columnas, declarado)
    total_id = next((i for i, n in columnas.items() if _norm(n).startswith("total del curso")), None)

    print("=" * 98)
    print(f"AULA {aula}  ·  {titulo}")
    print("=" * 98)
    print("\nFIABILIDAD (el aula contra el repositorio)")
    for c in ctrls:
        print(f"  {marca(c)} {c.texto}")

    fin = finales(entregas, pareja, alumnos, total_id)
    actividad: list[str] = []                      # una línea por tarea/quiz, para consola e informe
    foros: list[tuple[str, bool, dict]] = []       # (nombre, ¿califica?, resumen)
    ocultos: list[str] = []
    if not args.fiabilidad:
        print("\nCIERRE (qué falta)")
        print(f"  {'ítem':22s} {'tipo':13s} {'peso':>6s}  {'ventana':17s} {'estado':16s} "
              f"{'con nota':>9s} {'falta':>6s}")
        hoy = date.today()
        for e in entregas:
            it = pareja[e.id]
            con = sum(1 for al in alumnos if it and al.notas.get(it.itemid) is not None)
            cual = "cerrado" if e.entrega < hoy else ("abierto" if e.apertura <= hoy else "no abre")
            if it and not it.visible:
                cual += " OCULTO"
            peso = f"{(it.efectivo or 0) * 100:.1f}%" if it else "—"
            print(f"  {e.code[:22]:22s} {e.tipo_label:13s} {peso:>6s}  "
                  f"{e.apertura.strftime('%d/%m')}→{e.entrega.strftime('%d/%m')}      {cual:16s} "
                  f"{con:>4d}/{len(alumnos):<4d} {len(alumnos) - con:>6d}")
        ocultos += [e.code for e in entregas if pareja[e.id] and not pareja[e.id].visible]
        if ocultos:
            print(f"  ⚠ calificables ocultos para el estudiante: {', '.join(ocultos)} — mientras "
                  f"sigan ocultos nadie puede entregar y esa nota no va a existir")

        for e in entregas:
            it = pareja[e.id]
            if not it or not it.cmid:
                continue
            con = sum(1 for al in alumnos if al.notas.get(it.itemid) is not None)
            if it.modulo == "assign":
                r = resumen_tarea(cli, it.cmid)
                actividad.append(f"tarea · {e.code}: {r['participantes']} participantes · "
                                 f"{r['enviados']} enviados · {r['pendientes']} pendientes por "
                                 f"calificar")
            elif it.modulo == "quiz":
                n = cd._intentos(cli, int(it.cmid))
                # Más intentos que notas = algo quedó sin calificar: un intento abierto sin enviar o
                # una pregunta abierta que Moodle no puede puntuar solo.
                mas = (f" · {n - con} más que notas: hay intentos sin calificar o sin enviar"
                       if n > con >= 0 else "")
                actividad.append(f"quiz · {e.code}: {n if n >= 0 else '?'} intentos{mas}")
            elif it.modulo == "forum":
                foros.append((e.code, True, resumen_foro(cli, it.cmid, cli.nombre)))

        # Foros del aula que NO dan nota pero sí esperan respuesta del Docente: la presentación es
        # el único componente de relleno que el alistamiento deja visible, y sigue esperando.
        for nombre, r in foros_sin_nota(
                cli, estado, {it.cmid for it in items if it.modulo == "forum" and it.cmid}):
            foros.append((nombre, False, r))

        for linea in actividad:
            print(f"  {linea}")
        for nombre, califica, r in foros:
            print(f"  foro   · {nombre}{'' if califica else ' (sin nota)'}: "
                  f"{len(r['discusiones'])} discusiones · "
                  f"{len(r['sin_respuesta'])} sin ninguna respuesta · "
                  f"{len(r['sin_docente'])} sin respuesta del Docente")

        completos = [f for f in fin if not f.faltantes]
        print(f"\n  nota final completa (sin ítems pendientes): {len(completos)}/{len(fin)} estudiantes")
        if args.notas:
            print(f"\n  {'estudiante':38s} {'proyectada':>10s} {'con lo hecho':>12s} "
                  f"{'aula':>6s}  pendientes")
            for f in sorted(fin, key=lambda x: x.alumno.nombre):
                num = lambda v: f"{v:.2f}".replace(".", ",") if v is not None else "—"
                print(f"  {f.alumno.nombre[:38]:38s} {num(f.proyectada):>10s} "
                      f"{num(f.con_lo_hecho):>12s} {num(f.aula):>6s}  {len(f.faltantes)}")

    print()
    return {"aula": aula, "clave": clave, "grupo": grupo, "titulo": titulo,
            "controles": ctrls, "entregas": entregas, "pareja": pareja,
            "alumnos": alumnos, "finales": fin, "actividad": actividad, "foros": foros,
            "ocultos": ocultos}


def foros_sin_nota(cli: cd.CDigital, estado: dict[str, dict],
                   ya_vistos: set[str | None]) -> list[tuple[str, dict]]:
    """Los foros del aula que no son ítem del libro. «Avisos» se salta: es de una sola vía."""
    out = []
    for cmid, m in estado.items():
        if str(m.get("module")) != "forum":
            continue
        nombre = html.unescape(str(m.get("name", "")))
        if cmid in ya_vistos or _norm(nombre) == "avisos" or not m.get("visible", True):
            continue
        out.append((nombre, resumen_foro(cli, cmid, cli.nombre)))
    return out


# =============================================================================================
# Salidas a archivo
# =============================================================================================
def escribir_informe(revisiones: list[dict]) -> Path:
    """Markdown de cierre **sin notas individuales y sin cédulas** — va dentro del repositorio."""
    hoy = date.today().strftime("%Y-%m-%d")
    L = [f"# Cierre de notas en CDigital — {hoy}", "",
         "Generado por `python config/moodle/notas_cierre.py --informe`. **Solo agregados**: este",
         "archivo está en git y sincronizado a Drive, así que no lleva notas individuales ni",
         "documentos de identidad. El detalle por estudiante se saca con `--detalle`, que escribe",
         "fuera del repositorio.", "",
         "| Aula | Curso | Estudiantes | Ítems | Con nota final completa | Fiabilidad |",
         "|---|---|---:|---:|---:|---|"]
    for r in revisiones:
        malos = sum(1 for c in r["controles"] if c.ok is False and not c.aviso)
        pend = sum(1 for c in r["controles"] if c.ok is None)
        avisos = sum(1 for c in r["controles"] if c.aviso)
        estado = f"⛔ {malos} fallan" if malos else ("✓ todos" if not pend else f"— {pend} sin datos")
        if avisos:
            estado += f" · ⚠ {avisos}"
        completos = sum(1 for f in r["finales"] if not f.faltantes)
        L.append(f"| {r['aula']} | {r['titulo']} | {len(r['alumnos'])} | {len(r['entregas'])} | "
                 f"{completos} | {estado} |")
    L += ["", "## Detalle por aula", ""]
    for r in revisiones:
        L.append(f"### {r['aula']} · {r['titulo']}")
        L.append("")
        for c in r["controles"]:
            L.append(f"- {marca(c)} {c.texto}")
        L.append("")
        L.append("| Ítem | Tipo | Peso efectivo | Ventana | Con nota | Falta |")
        L.append("|---|---|---:|---|---:|---:|")
        for e in r["entregas"]:
            it = r["pareja"][e.id]
            con = sum(1 for al in r["alumnos"] if it and al.notas.get(it.itemid) is not None)
            peso = f"{(it.efectivo or 0) * 100:.1f}%" if it else "—"
            oculto = " · **oculto**" if it and not it.visible else ""
            L.append(f"| {e.code}{oculto} | {e.tipo_label} | {peso} | "
                     f"{e.apertura.strftime('%d/%m')}→{e.entrega.strftime('%d/%m')} | "
                     f"{con}/{len(r['alumnos'])} | {len(r['alumnos']) - con} |")
        L.append("")
        if r.get("ocultos"):
            L.append(f"- ⚠ calificables ocultos para el estudiante: {', '.join(r['ocultos'])} — "
                     f"nadie puede entregar y esa nota no va a existir")
        for linea in r.get("actividad") or []:
            L.append(f"- {linea}")
        for nombre, califica, fr in r.get("foros") or []:
            aviso = "" if not fr["sin_docente"] else \
                f" — **{len(fr['sin_docente'])} esperan respuesta del Docente**"
            L.append(f"- foro · {nombre}{'' if califica else ' (sin nota)'}: "
                     f"{len(fr['discusiones'])} discusiones · "
                     f"{len(fr['sin_respuesta'])} sin ninguna respuesta{aviso}")
        L.append("")
    INFORME_REPO.write_text("\n".join(L) + "\n", encoding="utf-8")
    return INFORME_REPO


def escribir_detalle(revisiones: list[dict]) -> list[Path]:
    """CSV por estudiante, **fuera del repositorio**. Nombre y correo institucional; nunca cédula."""
    CARPETA_DETALLE.mkdir(parents=True, exist_ok=True)
    hoy = date.today().strftime("%Y%m%d")
    rutas = []
    for r in revisiones:
        ruta = CARPETA_DETALLE / f"notas-{r['aula']}-{hoy}.csv"
        cols = ["estudiante", "correo"] + [e.code for e in r["entregas"]] + \
               ["final_proyectada", "con_lo_hecho", "total_del_curso_en_el_aula", "pendientes"]
        with open(ruta, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(cols)
            for f in sorted(r["finales"], key=lambda x: x.alumno.nombre):
                fila = [f.alumno.nombre, f.alumno.correo]
                for e in r["entregas"]:
                    it = r["pareja"][e.id]
                    v = f.alumno.notas.get(it.itemid) if it else None
                    fila.append("" if v is None else f"{v:.2f}".replace(".", ","))
                fila += [f"{f.proyectada:.2f}".replace(".", ","),
                         "" if f.con_lo_hecho is None else f"{f.con_lo_hecho:.2f}".replace(".", ","),
                         "" if f.aula is None else f"{f.aula:.2f}".replace(".", ","),
                         " · ".join(f.faltantes)]
                w.writerow(fila)
        rutas.append(ruta)
    return rutas


# =============================================================================================
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--curso", type=int, action="append", metavar="AULA",
                   help="Aula de CDigital (repetible). Por omisión, todas las declaradas.")
    p.add_argument("--fiabilidad", action="store_true",
                   help="Solo los controles del modelo contra el aula")
    p.add_argument("--notas", action="store_true", help="Tabla de nota final por estudiante")
    p.add_argument("--informe", action="store_true",
                   help=f"Escribe {INFORME_REPO.name} (agregados, sin cédulas)")
    p.add_argument("--detalle", action="store_true",
                   help=f"CSV por estudiante en {CARPETA_DETALLE}")
    args = p.parse_args(argv)

    aulas = args.curso or list(cd.AULAS_CURSO)
    desconocidas = [a for a in aulas if a not in cd.AULAS_CURSO]
    if desconocidas:
        print(f"⛔ aulas sin declarar en cdigital.AULAS_CURSO: {desconocidas}")
        print("   Declárala ahí (aula → curso, grupo) y en fechas_entrega_aca; el script no cambia.")
        return 2

    cli = cd.CDigital()
    cli.entrar()
    print(f"Sesión de CDigital como {cli.nombre}. Este script solo lee.\n")

    revisiones = [revisar(cli, a, args) for a in aulas]

    todos = [(r["aula"], c) for r in revisiones for c in r["controles"]]
    fallan = [(a, c) for a, c in todos if c.ok is False and not c.aviso]
    avisos = [(a, c) for a, c in todos if c.aviso]
    print("=" * 98)
    print(f"{len(revisiones)} aulas · "
          f"{sum(len(r['alumnos']) for r in revisiones)} estudiantes · "
          f"{sum(1 for a, c in todos if c.ok and not c.aviso)} controles pasan · "
          f"{len(fallan)} fallan · {len(avisos)} avisos · "
          f"{sum(1 for a, c in todos if c.ok is None)} sin datos todavía")
    for aula, c in fallan + avisos:
        print(f"  {marca(c)} {aula}: {c.texto}")

    if args.informe:
        print(f"\n✓ informe en {escribir_informe(revisiones)}")
    if args.detalle:
        for ruta in escribir_detalle(revisiones):
            print(f"✓ detalle en {ruta}")
    return 1 if fallan else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
