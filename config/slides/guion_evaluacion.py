# -*- coding: utf-8 -*-
"""Evaluación real del aula **dentro de los guiones docentes**.

Problema que resuelve
---------------------
Los guiones de sesión hablaban de «ACA 1 / ACA 2 / ACA 3» y no mencionaban los
**quices y parciales**, que en el libro de calificaciones de CDigital existen, pesan
mucho (Parcial 1 = 24 %) y **cierran en día de clase**: el Docente entraba a dictar
una sesión completa sin saber que ese día tenía que aplicar un cuestionario.

Este módulo lee el modelo único (`config/cursos/fechas_entrega_aca.py`, que copia el
libro de calificaciones auditado el 2026-08-10) y produce, para una sesión concreta:

* `bloque_aviso()`  → tabla «qué toca hoy en CDigital» (ítem real, tipo, corte, peso).
* `fase_evaluacion()` → el cuerpo de la fase de clase (guion literal + operativa).
* `inyectar_evaluacion()` → aplica todo sobre el markdown ya generado: inserta el
  aviso, **reserva minutos en el plan de clase** (rebalanceando las fases para que la
  suma siga siendo la misma), renumera las fases, corrige los minutos que la narración
  menciona y añade los ítems al checklist previo a clase.

Convenciones que respeta (las del resto de los guiones)
-------------------------------------------------------
* **Sin fechas de periodo**: aquí no se imprime ninguna fecha. Las fechas viven en la
  Presentación del Curso, en el enunciado del ítem y en CDigital. El guion solo dice
  *hoy / antes del próximo encuentro / ya cerró*, que es lo que el Docente necesita
  saber mientras dicta.
* Plataforma = **CDigital**; el docente es **el Docente**.
* La **Sesión 01 es de encuadre**: recibe el aviso (es información, no estructura) pero
  **nunca** se le inserta una fase ni se le toca el plan de clase.

Uso:
    from guion_evaluacion import inyectar_evaluacion
    md = inyectar_evaluacion(md, "creatividad", n)
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime

_SLIDES = os.path.dirname(os.path.abspath(__file__))
_CURSOS = os.path.normpath(os.path.join(_SLIDES, "..", "cursos"))
for _p in (_SLIDES, _CURSOS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fechas_entrega_aca import (  # noqa: E402
    ACA_COMPONENTES,
    GRUPO_REFERENCIA,
    IDS_INSTRUMENTO_CIERRE,
    KIND_CUESTIONARIO,
    KIND_FORO,
    KIND_TAREA,
    EntregaAca,
    cortes_curso,
    desglose_corte_texto,
    entregas_curso,
    entregas_para_grupo,
    fmt_peso,
    peso_corte,
)
from sesiones_cun import COURSES  # noqa: E402

# ─────────────────────────────────────────────────────────────────────────────
# Minutos que se reservan en el plan de clase
# ─────────────────────────────────────────────────────────────────────────────
# Un cuestionario que cierra en día de clase se aplica EN clase: si no se le reserva
# tiempo, el Docente lo deja «para la noche» y la mitad del grupo no lo presenta.
# El tramo depende del peso, que es el mejor proxy de su longitud en el aula.
MIN_PARCIAL = 22      # peso ≥ 20 % (Parcial 1 / Parcial 2 / Quiz de Proyecto I)
MIN_QUIZ_MEDIO = 15   # peso ≥ 8 %  (Quiz 2)
MIN_QUIZ = 12         # peso ≥ 5 %  (Quiz 1)
MIN_QUIZ_CORTO = 10   # peso < 5 %  (Quiz 3)
MIN_INSTRUMENTO = 4   # autoevaluación / coevaluación, cada una, el día que abren
MIN_FASE_EVAL = 6     # piso de la fase: por debajo no cabe en el plan de clase

PISO_FASE = 6         # ninguna fase de contenido baja de aquí
PISO_APERTURA = 4     # el encuadre puede bajar más: es el más comprimible

_KEYCAP = {
    1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣",
    6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟",
}
_RE_KEYCAP = re.compile(r"^(?:[0-9]️⃣|\U0001f51f)\s*")

_NUM_PALABRA = {
    4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho", 9: "nueve",
    10: "diez", 11: "once", 12: "doce", 13: "trece", 14: "catorce",
    15: "quince", 16: "dieciséis", 17: "diecisiete", 18: "dieciocho",
    19: "diecinueve", 20: "veinte", 21: "veintiún", 22: "veintidós",
    23: "veintitrés", 24: "veinticuatro", 25: "veinticinco", 26: "veintiséis",
    28: "veintiocho", 30: "treinta",
}

NOTA_SIN_FECHAS = (
    "> **En este guion no van fechas de periodo.** El aviso dice *hoy*, *antes del "
    "próximo encuentro* o *ya cerró*: las fechas exactas están en la Presentación del "
    "Curso, en el enunciado del ítem y en el propio ítem de CDigital."
)


# ─────────────────────────────────────────────────────────────────────────────
# Agenda de evaluación de una sesión
# ─────────────────────────────────────────────────────────────────────────────
def _fecha(txt: str) -> date:
    return datetime.strptime(txt.strip(), "%d/%m/%Y").date()


def fechas_sesiones(key: str) -> dict[int, date]:
    return {int(s["n"]): _fecha(s["fecha"]) for s in COURSES[key]["sesiones"]}


def _grupos(key: str) -> list[str | None]:
    """Grupos del curso con el **de referencia primero** (TG3 → 54466, el mayoritario)."""
    data = entregas_curso(key)
    if not isinstance(data, dict):
        return [None]
    grupos = sorted(data)
    ref = GRUPO_REFERENCIA.get(key)
    if ref in grupos:
        grupos.remove(ref)
        grupos.insert(0, ref)
    return grupos


@dataclass
class AgendaEval:
    """Qué ítems del libro de calificaciones toca una sesión concreta."""

    key: str
    n: int
    hoy: list[EntregaAca] = field(default_factory=list)        # cierran hoy
    abren_hoy: list[EntregaAca] = field(default_factory=list)  # ventana que abre hoy
    semana: list[EntregaAca] = field(default_factory=list)     # cierran antes del próximo
    recien: list[EntregaAca] = field(default_factory=list)     # cerraron desde el anterior
    en_curso: list[EntregaAca] = field(default_factory=list)   # abiertos, cierran más allá
    ultima: bool = False
    grupos_divergen: bool = False

    @property
    def vacia(self) -> bool:
        return not (self.hoy or self.abren_hoy or self.semana or self.recien or self.en_curso)

    def reservables(self) -> list[EntregaAca]:
        """Ítems que ocupan tiempo de clase: cuestionarios que cierran hoy y los
        instrumentos individuales el día que abren (se diligencian en el encuentro)."""
        out = [e for e in self.hoy if e.kind == KIND_CUESTIONARIO and not e.es_instrumento_cierre]
        out += [e for e in self.abren_hoy if e.es_instrumento_cierre]
        out += [e for e in self.hoy if e.es_instrumento_cierre and e not in out]
        return out

    def minutos(self) -> int:
        """Minutos de clase que hay que reservar (0 si la sesión no aplica nada).

        Una fase de menos de `MIN_FASE_EVAL` minutos no cabe en un plan de clase: si el
        cálculo por pesos queda por debajo (p. ej. una sola coevaluación de foro), se
        sube al mínimo — abrir la actividad y ver que todos entran nunca toma menos.
        """
        total = sum(minutos_reserva(e) for e in self.reservables())
        return max(total, MIN_FASE_EVAL) if total else 0


def minutos_reserva(e: EntregaAca) -> int:
    if e.es_instrumento_cierre:
        return MIN_INSTRUMENTO
    if e.kind != KIND_CUESTIONARIO:
        return 0
    if e.weight >= 20:
        return MIN_PARCIAL
    if e.weight >= 8:
        return MIN_QUIZ_MEDIO
    if e.weight >= 5:
        return MIN_QUIZ
    return MIN_QUIZ_CORTO


def _agenda_grupo(key: str, n: int, grupo: str | None) -> AgendaEval:
    fechas = fechas_sesiones(key)
    d = fechas[n]
    prev = max((f for f in fechas.values() if f < d), default=None)
    nxt = min((f for f in fechas.values() if f > d), default=None)
    ag = AgendaEval(key=key, n=n, ultima=(nxt is None))
    for e in entregas_para_grupo(key, grupo):
        if e.apertura == d and e.entrega != d:
            ag.abren_hoy.append(e)
            continue           # ya tiene su fila: no repetirlo como «abierto»
        if e.entrega == d:
            ag.hoy.append(e)
        elif e.entrega > d and (nxt is None or e.entrega < nxt):
            ag.semana.append(e)
        elif e.entrega < d and (prev is None or e.entrega > prev):
            ag.recien.append(e)
        elif e.apertura <= d < e.entrega:
            ag.en_curso.append(e)
    return ag


def agenda_sesion(key: str, n: int) -> AgendaEval:
    """Agenda de la sesión. En cursos con ventanas por grupo (TG3) se usa el grupo de
    referencia y se marca `grupos_divergen` si algún grupo cae en otro cajón."""
    grupos = _grupos(key)
    ag = _agenda_grupo(key, n, grupos[0] if grupos[0] else None)
    if len(grupos) > 1:
        def firma(a: AgendaEval) -> tuple:
            return tuple(
                sorted((e.id, cajon) for cajon, lst in
                       (("hoy", a.hoy), ("abren", a.abren_hoy), ("semana", a.semana),
                        ("recien", a.recien))
                       for e in lst)
            )
        base = firma(ag)
        for g in grupos[1:]:
            if firma(_agenda_grupo(key, n, g)) != base:
                ag.grupos_divergen = True
                break
    return ag


# ─────────────────────────────────────────────────────────────────────────────
# Textos derivados del modelo (para narración de los guiones)
# ─────────────────────────────────────────────────────────────────────────────
def item_txt(e: EntregaAca) -> str:
    """«**Parcial 1** (Cuestionario · 24 % · corte 1)»."""
    return f"**{e.code}** ({e.tipo_label} · {e.weight_pct} · corte {e.corte})"


def items_corte_txt(key: str, corte: int) -> str:
    """«Quiz 1 6% + Parcial 1 24%» — los ítems reales de un corte, sin fechas."""
    items = [c for c in ACA_COMPONENTES[key] if int(c["corte"]) == corte]
    return " + ".join(f"{c['code']} {fmt_peso(c['weight'])}" for c in items)


def peso_item(key: str, item_id: str) -> str:
    """Peso de un ítem concreto («24%»), leído del catálogo — nunca escrito a mano."""
    for c in ACA_COMPONENTES[key]:
        if c["id"] == item_id:
            return fmt_peso(c["weight"])
    raise KeyError(f"{key}/{item_id}")


def peso_corte_txt(key: str, corte: int) -> str:
    """Peso del corte formateado («40%»)."""
    return fmt_peso(peso_corte(key, corte))


def peso_tipo(key: str, kind: str) -> str:
    """Cuánto del curso se juega en un tipo de actividad («cuestionarios = 65,6%»)."""
    return fmt_peso(sum(float(c["weight"]) for c in ACA_COMPONENTES[key] if c["kind"] == kind))


def desglose(key: str) -> str:
    """Desglose completo de cortes tal como está en el aula (del modelo, no a mano)."""
    return desglose_corte_texto(key)


def tabla_items_curso(key: str) -> str:
    """Tabla **sin fechas** de los ítems del aula: para la sesión de encuadre.

    Reemplaza las listas «ACA 1 / ACA 2 / ACA 3» que el material traía inventadas.
    """
    lines = [
        "| Ítem en CDigital | Tipo de actividad | Corte | Peso |",
        "| :--- | :--- | :---: | ---: |",
    ]
    for corte in cortes_curso(key):
        for c in ACA_COMPONENTES[key]:
            if int(c["corte"]) != corte:
                continue
            lines.append(
                f"| **{c['code']}** | {'Cuestionario' if c['kind'] == KIND_CUESTIONARIO else ('Tarea' if c['kind'] == KIND_TAREA else 'Foro')} "
                f"| {corte} | {fmt_peso(c['weight'])} |"
            )
    lines.append("")
    lines.append(f"> **Cortes:** {desglose_corte_texto(key)}.")
    return "\n".join(lines)


def frase_cortes(key: str) -> str:
    """Párrafo que el Docente lee para explicar la evaluación real del aula."""
    partes = []
    for corte in cortes_curso(key):
        items = [c for c in ACA_COMPONENTES[key] if int(c["corte"]) == corte]
        det = ", ".join(
            f"**{c['code']}** ({'cuestionario' if c['kind'] == KIND_CUESTIONARIO else ('tarea' if c['kind'] == KIND_TAREA else 'foro')}, {fmt_peso(c['weight'])})"
            for c in items
        )
        partes.append(f"**corte {corte}** ({fmt_peso(peso_corte(key, corte))}): {det}")
    return "; ".join(partes) + "."


def _ruta_corte(e: EntregaAca) -> str:
    return f"la sección del **corte {e.corte}** del aula"


def sesion_tope(key: str, d: date) -> int | None:
    """Número de la primera sesión **posterior** a `d` (o `None`: cierra tras la última).

    Permite decir «cierra antes de la Sesión 03» sin escribir una sola fecha, que es la
    convención de los guiones: el Docente ubica el hito en el calendario de clases.
    """
    post = sorted(n for n, f in fechas_sesiones(key).items() if f > d)
    return post[0] if post else None


def _cierra_antes_de(key: str, e: EntregaAca) -> str:
    """«antes de la Sesión 03» / «después del último encuentro» — sin negritas ni fechas."""
    tope = sesion_tope(key, e.entrega)
    return f"antes de la Sesión {tope:02d}" if tope else "después del último encuentro"


# ─────────────────────────────────────────────────────────────────────────────
# Bloque de aviso (va arriba, junto a «📌 De esta sesión»)
# ─────────────────────────────────────────────────────────────────────────────
def _estado_txt(e: EntregaAca, cajon: str, mins: int, ultima: bool = False,
                key: str = "") -> str:
    if cajon == "hoy":
        if e.es_instrumento_cierre:
            verbo = ("**Cierra hoy** el foro: se participa en el encuentro"
                     if e.kind == KIND_FORO else "**Cierra hoy**: se diligencia en el encuentro")
            return verbo + (f" (~{mins} min reservados)" if mins else "")
        if e.kind == KIND_CUESTIONARIO:
            return (f"**Cierra hoy** — se aplica en clase"
                    + (f" (~{mins} min reservados en el plan)" if mins else ""))
        return "**Cierra hoy** — se sube en CDigital antes del cierre"
    if cajon == "abre":
        if e.es_instrumento_cierre:
            return ("**Abre hoy** — " + ("se participa en el foro" if e.kind == KIND_FORO
                                         else "se diligencia")
                    + (f" en clase (~{mins} min reservados)" if mins else " en CDigital"))
        return "**Abre hoy** la ventana en CDigital"
    if cajon == "semana":
        if ultima:
            return ("Abierto: **cierra después de este último encuentro** — si no se anuncia hoy, "
                    "ya no hay clase donde anunciarlo")
        return "Abierto: **cierra antes del próximo encuentro**"
    if cajon == "recien":
        return "**Ya cerró** — hoy toca devolución y registro de la nota"
    return f"Abierto: **cierra {_cierra_antes_de(key, e) if key else 'más adelante'}**"


_CAJON_TXT = {
    "hoy": "cierra hoy",
    "abren": "abre hoy",
    "semana": "cierra antes del próximo encuentro",
    "recien": "ya cerró",
}


def _diferencias_grupos(key: str, n: int) -> dict[str, str]:
    """Qué cambia, en esta sesión, en los grupos que no son el de referencia (TG3)."""
    grupos = _grupos(key)
    ref = _agenda_grupo(key, n, grupos[0])

    def mapa(a: AgendaEval) -> dict[str, str]:
        out: dict[str, str] = {}
        for cajon, lst in (("hoy", a.hoy), ("abren", a.abren_hoy),
                           ("semana", a.semana), ("recien", a.recien)):
            for e in lst:
                out[e.code] = cajon
        return out

    base = mapa(ref)
    salida: dict[str, str] = {}
    for g in grupos[1:]:
        m = mapa(_agenda_grupo(key, n, g))
        difs = [f"**{code}** {_CAJON_TXT[cajon]}"
                for code, cajon in m.items() if base.get(code) != cajon]
        difs += [f"**{code}** hoy no aplica" for code in base if code not in m]
        if difs:
            salida[g] = "; ".join(difs) + "."
    return salida


def _anuncio_literal(key: str, ag: AgendaEval) -> str:
    """Guion literal para anunciar lo que **no** ocupa tiempo de clase.

    Es el caso de los ítems que cierran entre dos encuentros (el **Quiz** de Proyecto I
    cierra en fin de semana, y vale el 25 %) y de los que acaban de cerrar y hoy toca
    devolver. Sin este bloque el Docente dicta la sesión y no menciona un ítem que ya
    está corriendo en el aula.
    """
    porvenir = [e for e in ag.semana if not e.es_instrumento_cierre]
    # Un cuestionario que corre por fuera del día de clase (el **Quiz** de Proyecto I:
    # 25 % y cierra en fin de semana) también se anuncia: si no, pasa de largo.
    porvenir += [e for e in ag.en_curso
                 if e.kind == KIND_CUESTIONARIO and not e.es_instrumento_cierre]
    if ag.n == 1:
        porvenir += [e for e in ag.en_curso if e.kind == KIND_TAREA]
    instrumentos = [e for e in ag.semana if e.es_instrumento_cierre and e not in ag.abren_hoy]
    cerrados = list(ag.recien)
    abren = [e for e in ag.abren_hoy if not e.es_instrumento_cierre]
    if not (porvenir or cerrados or abren or instrumentos):
        return ""
    cuando = ("después de este último encuentro" if ag.ultima
              else "antes del próximo encuentro")
    out = ["**Cómo anunciarlo (guion literal, en el cierre de la clase — no en el último minuto):**"]
    for e in abren:
        out.append(
            f"> “Aviso de plataforma: **{e.code}** ya está **abierto** en CDigital, en la sección "
            f"del corte {e.corte}. Es un **{e.tipo_label.lower()}** y vale **{e.weight_pct}** del "
            "curso. Ábranlo hoy mismo aunque no lo vayan a resolver todavía: así saben cuántas "
            "preguntas tiene y cuánto tiempo les da.”"
        )
    for e in porvenir:
        plazo = cuando if e in ag.semana else _cierra_antes_de(key, e)
        if e.kind == KIND_CUESTIONARIO:
            out.append(
                f"> “Ojo con esto, que es plata: **{e.code}** es un **cuestionario en CDigital** que "
                f"**cierra {plazo}** y pesa **{e.weight_pct}** del curso — todo el corte "
                f"{e.corte} vale {fmt_peso(peso_corte(key, e.corte))}. No cae en clase, así que "
                "nadie se lo va a recordar el día del cierre: agéndenlo ustedes hoy. Cuando lo "
                "resuelvan, verifiquen que la plataforma diga **enviado**.”"
            )
        else:
            out.append(
                f"> “**{e.code}** es la **{e.tipo_label.lower()}** del corte {e.corte} y **cierra "
                f"{plazo}**: pesa **{e.weight_pct}**. Es el documento acumulativo, no un trabajo "
                "nuevo: se sube en CDigital, en PDF, y quien no lo vea cargado en la plataforma "
                "asuma que no está entregado.”"
            )
    for e in instrumentos:
        out.append(
            f"> “**{e.code}** ({e.tipo_label.lower()}, **{e.weight_pct}**) queda abierta y **cierra "
            f"{cuando}**. Entren desde el aula; no se recupera después.”"
        )
    for e in cerrados:
        if e.es_instrumento_cierre:
            out.append(
                f"> “**{e.code}** ya cerró. Quien no entró, no tiene esa nota: no hay reapertura "
                "por olvido.”"
            )
        elif e.kind == KIND_CUESTIONARIO:
            quedan = [c for c in ACA_COMPONENTES[key]
                      if c["kind"] == KIND_CUESTIONARIO
                      and c["id"] not in IDS_INSTRUMENTO_CIERRE
                      and c["id"] != e.id and int(c["corte"]) >= e.corte]
            destino = "el siguiente cuestionario" if quedan else "la entrega que cierra el curso"
            out.append(
                f"> “**{e.code}** ya cerró. La nota queda en el libro de calificaciones del aula y "
                "hoy les devuelvo lo importante: dónde se equivocó el grupo y qué no se puede "
                f"repetir en {destino}. Lo que revisamos aquí no cambia la nota; evita que se "
                "repita.”"
            )
        else:
            out.append(
                f"> “**{e.code}** ya cerró. Quien alcanzó a subir, verifique en CDigital que el "
                "archivo abre; un PDF corrupto cuenta como no entregado.”"
            )
    if cerrados:
        out.append("")
        out.append(
            "**Devolución mínima que sí sirve (3–4 min):** los dos errores más repetidos del grupo, "
            "con un ejemplo anónimo en pantalla, y una instrucción concreta para el siguiente ítem. "
            "Nunca leer notas en voz alta ni comparar estudiantes."
        )
    return "\n".join(out)


def bloque_aviso(key: str, n: int, ag: AgendaEval | None = None) -> str:
    """Tabla «qué toca hoy en CDigital» + operativa previa. `''` si no hay nada."""
    ag = ag or agenda_sesion(key, n)
    if ag.vacia:
        return ""
    mins = {e.id: minutos_reserva(e) for e in ag.reservables()}
    filas: list[tuple[EntregaAca, str]] = []
    for e in ag.hoy:
        filas.append((e, "hoy"))
    for e in ag.abren_hoy:
        filas.append((e, "abre"))
    for e in ag.semana:
        filas.append((e, "semana"))
    for e in ag.recien:
        filas.append((e, "recien"))
    if n == 1:  # en el encuadre sí importa nombrar lo que ya está abierto
        for e in ag.en_curso:
            filas.append((e, "en_curso"))

    lines = ["⏱️ **Evaluación de esta sesión en CDigital** *(ítems reales del libro de calificaciones)*", ""]
    if filas:
        lines.append("| Ítem en el aula | Tipo | Corte | Peso | Qué pasa en esta sesión |")
        lines.append("| :--- | :--- | :---: | ---: | :--- |")
        for e, cajon in filas:
            lines.append(
                f"| **{e.code}** | {e.tipo_label} | {e.corte} | {e.weight_pct} | "
                f"{_estado_txt(e, cajon, mins.get(e.id, 0), ag.ultima, key)} |"
            )
    else:
        lines.append(
            "**Hoy no cierra ni abre ningún ítem del libro de calificaciones.** La sesión es de "
            "contenido y avance; lo único que sigue corriendo es lo que está abajo."
        )
    lines.append("")

    anuncio = _anuncio_literal(key, ag)
    if anuncio:
        lines.append(anuncio)
        lines.append("")

    if n != 1:
        docs = [e for e in ag.en_curso if e.kind == KIND_TAREA]
        otros = [e for e in ag.en_curso if e.kind != KIND_TAREA]
        if docs:
            lines.append(
                "> **Abierto todo el periodo (hoy no cierra):** "
                + " · ".join(item_txt(e) for e in docs)
                + ". Es el producto acumulativo: cada sesión le agrega una sección, así que el "
                "avance de hoy es parte de esa entrega."
            )
        if otros:
            lines.append(
                "> **También abierto en el aula:** "
                + " · ".join(f"{item_txt(e)}, cierra {_cierra_antes_de(key, e)}" for e in otros)
                + "."
            )
    if ag.minutos():
        lines.append(
            f"> **Reserva de tiempo:** el plan de clase de abajo ya trae la fase de "
            f"evaluación (**{ag.minutos()} min**) y el resto de las fases están recortadas "
            "para que la hora siga sumando lo mismo. No es tiempo adicional."
        )
    if ag.grupos_divergen:
        lines.append(
            "> ⚠️ **Este curso tiene grupos con ventanas distintas.** La tabla de arriba es la del "
            f"grupo de referencia (**{_grupos(key)[0]}**). En los demás cambia así:"
        )
        for g, difs in _diferencias_grupos(key, n).items():
            lines.append(f"> - **Grupo {g}:** {difs}")
        lines.append(
            "> Antes de anunciar una fecha, ábrala en el libro de calificaciones **del aula de ese "
            "grupo**: es la única fuente que no se equivoca de grupo."
        )
    if n == 1:
        lines.append(
            "> **Nómbrelos como están en el aula.** En el libro de calificaciones de este curso "
            f"hay: {frase_cortes(key)} Si alguna slide del deck todavía habla de «las tres ACAs», "
            "corríjalo en voz alta: los ítems son estos y con estos nombres los va a buscar el "
            "estudiante en CDigital."
        )
    lines.append(NOTA_SIN_FECHAS)
    return "\n".join(lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Fase de clase
# ─────────────────────────────────────────────────────────────────────────────
def _nombre_fase(items: list[EntregaAca]) -> str:
    codes = " · ".join(e.code for e in items)
    if all(e.es_instrumento_cierre for e in items):
        return f"{codes} en el aula"
    return f"{codes} en CDigital (se aplica en clase)"


def _cuerpo_cuestionario(e: EntregaAca, key: str, mins: int, ag: AgendaEval) -> list[str]:
    palabra = _NUM_PALABRA.get(mins, str(mins))
    hermanos = [x for x in ACA_COMPONENTES[key]
                if int(x["corte"]) == e.corte and x["id"] != e.id]
    otros = ", ".join(f"**{x['code']}** ({fmt_peso(x['weight'])})" for x in hermanos)
    resto = (
        f" El resto del corte {e.corte} lo aportan {otros}."
        if otros else f" Es el único ítem del corte {e.corte}."
    )
    ya_cerro = [x.code for x in ag.recien if x.corte == e.corte]
    pendiente = [x.code for x in ag.semana if x.corte == e.corte]
    out = [
        "**Sin slides nuevas.** Se comparte la pantalla del aula solo para mostrar dónde está "
        "el cuestionario; el resto de la fase el Docente no proyecta nada.",
        "",
        f"**Antes de abrirlo (1 min, con el aula ya en pantalla):**",
        f"- Verificar que **{e.code}** esté **visible** para el grupo y con la configuración "
        "prevista: número de intentos, tiempo límite, orden aleatorio de preguntas y "
        "retroalimentación **diferida** (que no muestre respuestas antes del cierre).",
        "- Decir en voz alta la regla de conexión: si se cae el internet, **no se cierra la "
        "pestaña** y se avisa al Docente por el canal del curso **mientras la ventana sigue "
        "abierta**; después del cierre ya no hay nada que hacer desde el aula.",
        "- Recordar que es **individual**: el Docente responde fallas técnicas, no contenido.",
        "",
        "**GUION LITERAL:**",
        f"> “Guarden lo que estén escribiendo. Los próximos **{palabra} minutos** son para "
        f"**{e.code}**, que es un **{e.tipo_label.lower()} en CDigital** y **cierra hoy**: no "
        "queda abierto para la noche ni para mañana.”",
        f"> “Pesa **{e.weight_pct}** del curso dentro del **corte {e.corte}**, que vale "
        f"**{fmt_peso(peso_corte(key, e.corte))}**.{resto} Con esto ya saben por qué no es un "
        "trámite.”",
        f"> “Ruta exacta: entran al aula del curso en CDigital, {_ruta_corte(e)}, y abren el ítem "
        f"**{e.code}**. Cuando terminen, la plataforma tiene que decirles **enviado**: un intento "
        "empezado y no enviado cuenta como no presentado.”",
        "> “Yo me quedo en el Meet con el micrófono abierto **solo** para fallas técnicas. "
        "Preguntas de contenido no las respondo mientras el cuestionario corre; las dejamos para "
        "el cierre.”",
        "",
        f"**Qué hace el Docente mientras corre (~{max(mins - 3, 5)} min):** mirar el chat del Meet, "
        "anotar quién reporta falla técnica (nombre y hora: es la evidencia para cualquier "
        "reclamación posterior) y **no** empezar a calificar todavía. Si el grupo termina antes, "
        "se adelanta el cierre de la sesión: no se rellena con contenido nuevo.",
        "",
        "**Si alguien no lo presenta:** el estudiante avisa **antes** del cierre por el canal del "
        "curso; el Docente verifica en el aula si el intento quedó abierto y resuelve con el "
        "reglamento en la mano. Nada se arregla “después” por WhatsApp ni por correo personal.",
        "",
        f"**Cierre de la fase (1 min):** “¿Todos vieron el mensaje de **enviado**? Quien NO lo haya "
        "visto, escríbalo en el chat ahora, no cuando ya se haya cerrado.”",
    ]
    if ya_cerro:
        out.append("")
        out.append(
            f"> **Contexto del corte {e.corte}:** ya cerró **{', '.join(ya_cerro)}**; si la nota "
            "todavía no está publicada, quedó pendiente de registro en el libro de calificaciones."
        )
    if pendiente:
        out.append("")
        out.append(
            f"> **Todavía del corte {e.corte}:** **{', '.join(pendiente)}** cierra antes del "
            "próximo encuentro. Anúncielo aquí, no en el minuto final."
        )
    return out


def _cuerpo_instrumentos(items: list[EntregaAca], key: str, mins: int) -> list[str]:
    auto = next((e for e in items if e.kind == KIND_CUESTIONARIO), None)
    coev = next((e for e in items if e.kind == KIND_FORO), None)
    total = fmt_peso(sum(e.weight for e in items))
    nombres = " y ".join("**" + e.code + "**" for e in items)
    plural = len(items) > 1
    frase_peso = (
        f"ya están en CDigital y entre las dos valen **{total}** del curso"
        if plural else f"ya está en CDigital y vale **{total}** del curso"
    )
    out = [
        "**Sin slides nuevas.** Se comparte el aula en pantalla para que nadie diga después que "
        "no encontró la actividad.",
        "",
        "**GUION LITERAL:**",
        f"> “Los últimos **{_NUM_PALABRA.get(mins, mins)} minutos** son de ustedes y de la "
        f"plataforma: {nombres} {frase_peso}. Se "
        f"{'pierden' if plural else 'pierde'} por no entrar, que es la forma más tonta de perder "
        "nota.”",
    ]
    if auto is not None:
        out.append(
            f"> “La **{auto.code.lower()}** es un **{auto.tipo_label.lower()}**: se diligencia una "
            "vez, con criterios. No es ponerse cinco: es sustentar con qué evidencia se pone la "
            "nota que se pone — cumplimiento, calidad del avance y participación.”"
        )
    if coev is not None:
        out.append(
            f"> “La **{coev.code.lower()}** es un **{coev.tipo_label.lower()}**: hay que "
            "**escribir** en él. No se «diligencia»: se participa. Un comentario por compañero o "
            "por equipo, con un criterio concreto y algo accionable. ‘Buen trabajo’ no es "
            "coevaluar y no cuenta como participación.”"
        )
    out += [
        "",
        "**Operativa del Docente en esta fase:** abrir el aula en pantalla, mostrar la ruta de cada "
        "actividad, pedir que la abran **ahora** desde el celular o el computador y confirmar en voz "
        "alta quién ya la ve. Es el momento con más deserción silenciosa del periodo: se resuelve "
        "haciéndolo en clase, no anunciándolo.",
        "",
        "**Qué NO se hace:** dejar la coevaluación como «tarea de la casa» sin haberla abierto en "
        "clase, ni pedir que se coevalúen por el chat del Meet — lo que no queda en el foro de "
        "CDigital no existe para el libro de calificaciones.",
    ]
    return out


def fase_evaluacion(key: str, n: int, ag: AgendaEval | None = None) -> tuple[str, int, str] | None:
    """`(nombre_fase, minutos, cuerpo_markdown)` o `None` si la sesión no evalúa.

    La Sesión 01 es de encuadre: nunca recibe fase (solo el aviso informativo).
    """
    ag = ag or agenda_sesion(key, n)
    if n == 1:
        return None
    items = ag.reservables()
    if not items:
        return None
    mins = ag.minutos()
    cuerpo: list[str] = []
    cuestionarios = [e for e in items if not e.es_instrumento_cierre]
    instrumentos = [e for e in items if e.es_instrumento_cierre]
    for i, e in enumerate(cuestionarios):
        if i:
            cuerpo.append("")
        cuerpo += _cuerpo_cuestionario(e, key, minutos_reserva(e), ag)
    if instrumentos:
        if cuerpo:
            cuerpo.append("")
            cuerpo.append(
                "**Y en el mismo bloque, los instrumentos individuales de cierre:**"
            )
        cuerpo += _cuerpo_instrumentos(
            instrumentos, key,
            max(mins - sum(minutos_reserva(e) for e in cuestionarios), MIN_FASE_EVAL),
        )
    cuerpo.append("")
    cuerpo.append(
        "> **El orden lo decide el Docente:** si el grupo llega disperso, esta fase se puede "
        "aplicar justo después del encuadre y dejar el taller al final; lo que no se puede es "
        "dejarla sin tiempo propio."
    )
    return _nombre_fase(items), mins, "\n".join(cuerpo)


# ─────────────────────────────────────────────────────────────────────────────
# Inyección sobre el markdown ya generado
# ─────────────────────────────────────────────────────────────────────────────
_RE_PLAN_HEAD = re.compile(r"^\| Fase \| Minutos \| Reloj sugerido \(desde el inicio\) \|$", re.M)
_RE_PLAN_ROW = re.compile(r"^\| (.+?) \| (\d+) \| min \d+:00 – \d+:00 \|$")
_RE_HEADING = re.compile(
    r"^#### (?:[0-9]️⃣|\U0001f51f)\s*(.*?)\s*\(~(\d+) min\)(.*)$", re.M
)


def _reparto(mins: list[int], reserva: int) -> tuple[list[int], int]:
    """Quita `reserva` minutos a las fases existentes sin bajar de los pisos.

    Water-filling sobre las fases de contenido (todas menos la primera y la última):
    se recorta primero lo más largo, así ninguna fase queda en un minuto y la suma del
    plan no cambia. Si no alcanza, se recorta el cierre y luego el encuadre; si aún no
    alcanza, se devuelve la reserva realmente aplicada.
    """
    out = list(mins)
    falta = reserva
    medio = list(range(1, max(1, len(out) - 1)))
    while falta > 0:
        cands = [i for i in medio if out[i] > PISO_FASE]
        if not cands:
            break
        i = max(cands, key=lambda k: (out[k], -k))
        out[i] -= 1
        falta -= 1
    for i in ([len(out) - 1] if len(out) > 1 else []) + [0]:
        while falta > 0 and out[i] > (PISO_APERTURA if i == 0 else PISO_FASE):
            out[i] -= 1
            falta -= 1
    return out, reserva - falta


def _renumerar(nombre: str, i: int) -> str:
    base = _RE_KEYCAP.sub("", nombre).strip()
    return f"{_KEYCAP.get(i, str(i))} {base}"


def _reescribir_plan(md: str, nombre: str, mins_reserva: int) -> tuple[str, list[int], list[int], int]:
    """Inserta la fila de evaluación en el plan de clase y rebalancea el reloj.

    → `(md, minutos_viejos, minutos_nuevos, reserva_aplicada)`; si no hay plan, no toca nada.
    """
    m = _RE_PLAN_HEAD.search(md)
    if not m:
        return md, [], [], 0
    lineas = md.split("\n")
    i0 = md[:m.start()].count("\n")
    i = i0 + 2  # salta el encabezado y la línea de separación
    filas: list[tuple[str, int]] = []
    while i < len(lineas):
        mm = _RE_PLAN_ROW.match(lineas[i])
        if not mm:
            break
        filas.append((mm.group(1), int(mm.group(2))))
        i += 1
    if len(filas) < 3:
        return md, [], [], 0
    viejos = [f[1] for f in filas]
    nuevos, aplicada = _reparto(viejos, mins_reserva)
    if aplicada <= 0:
        return md, [], [], 0
    nombres = [f[0] for f in filas]
    pos = len(filas) - 1  # antes del cierre
    nombres = nombres[:pos] + [nombre] + nombres[pos:]
    nuevos_full = nuevos[:pos] + [aplicada] + nuevos[pos:]
    nombres = [_renumerar(nb, k + 1) for k, nb in enumerate(nombres)]
    reloj = 0
    salida = []
    for nb, mn in zip(nombres, nuevos_full):
        salida.append(f"| {nb} | {mn} | min {reloj:02d}:00 – {reloj + mn:02d}:00 |")
        reloj += mn
    md = "\n".join(lineas[:i0 + 2] + salida + lineas[i:])
    return md, viejos, nuevos, aplicada


def _ajustar_cuerpo_fases(
    md: str, viejos: list[int], nuevos: list[int], pos: int, nombre: str, cuerpo: str, mins: int
) -> str:
    """Actualiza los encabezados `#### N️⃣ … (~M min)`, renumera y mete la fase nueva."""
    heads = list(_RE_HEADING.finditer(md))
    if not heads:
        return md
    # 1) Cuerpo de cada fase acortada: corregir los minutos que la narración menciona
    #    («Tienen 22 minutos» → «Tienen 8 minutos»), en dígitos y en palabra.
    cuerpos: list[tuple[int, int, int, int]] = []  # (ini, fin, viejo, nuevo)
    for k, h in enumerate(heads):
        if k >= len(nuevos) or nuevos[k] == viejos[k]:
            continue
        ini = h.end()
        fin = heads[k + 1].start() if k + 1 < len(heads) else len(md)
        cuerpos.append((ini, fin, viejos[k], nuevos[k]))

    out = md
    for ini, fin, viejo, nuevo in reversed(cuerpos):
        trozo = out[ini:fin]
        trozo = re.sub(rf"\b{viejo}\b(?=\s*minutos)", str(nuevo), trozo)
        pal_v, pal_n = _NUM_PALABRA.get(viejo), _NUM_PALABRA.get(nuevo)
        if pal_v and pal_n:
            for a, b in ((pal_v.capitalize(), pal_n.capitalize()), (pal_v, pal_n)):
                trozo = re.sub(rf"\b{a}\b(?=\s+minutos)", b, trozo)
        out = out[:ini] + trozo + out[fin:]

    # 2) Encabezados: minutos nuevos y renumerado (las fases posteriores a la insertada
    #    corren un puesto; los bloques que no están en el plan —la tutoría de Proyecto I—
    #    conservan sus minutos y solo se renumeran). De atrás hacia adelante para no
    #    invalidar los offsets.
    heads = list(_RE_HEADING.finditer(out))
    for k in range(len(heads) - 1, -1, -1):
        h = heads[k]
        titulo, mins_txt, cola = h.group(1), int(h.group(2)), h.group(3)
        idx = k + 1 if k < pos else k + 2
        nuevo_min = nuevos[k] if k < len(nuevos) else mins_txt
        out = (out[:h.start()]
               + f"#### {_KEYCAP.get(idx, str(idx))} {titulo} (~{nuevo_min} min){cola}"
               + out[h.end():])

    # 3) La fase de evaluación, justo antes del cierre.
    heads = list(_RE_HEADING.finditer(out))
    if pos < len(heads):
        anclaje = heads[pos].start()
    else:
        anclaje = len(out)
    bloque = (
        f"#### {_KEYCAP.get(pos + 1, str(pos + 1))} {_RE_KEYCAP.sub('', nombre).strip()} "
        f"(~{mins} min) — Protagonistas: Estudiantes + Docente\n"
        f"{cuerpo}\n\n"
    )
    return out[:anclaje] + bloque + out[anclaje:]


def _nota_replan(viejos: list[int], nuevos: list[int], md: str, mins: int) -> str:
    """Línea honesta de qué se recortó para hacerle espacio a la evaluación."""
    heads = list(_RE_HEADING.finditer(md))
    cambios = []
    for k, (v, nv) in enumerate(zip(viejos, nuevos)):
        if v == nv:
            continue
        nombre = heads[k].group(1) if k < len(heads) else f"fase {k + 1}"
        cambios.append(f"{nombre} {v}→{nv} min")
    if not cambios:
        return ""
    return (
        f"> **Replaneación de hoy (la hora no crece):** la fase de evaluación toma **{mins} min** "
        f"y por eso se recortan: {', '.join(cambios)}. Donde la consigna del taller diga otra "
        "cantidad de minutos, manda el plan de clase."
    )


# ─────────────────────────────────────────────────────────────────────────────
# RETIRADO (2026-08-11): `PUENTE_LEGACY` / `PUENTE_PREGRADO` / `sanear_detalle()`
# ─────────────────────────────────────────────────────────────────────────────
# Eran un puente temporal: reescribían al vuelo la línea «- **Detalle:**» del guion
# porque `sesiones_cun.py` todavía describía Proyecto I con el esquema viejo del
# ESP329 («ACA1 ya cerró (dom 30/08)») y había que traducirlo a los nombres reales
# del aula (Quiz · ACA 1 · ACA FINAL) y borrarle la fecha de periodo.
#
# El origen ya está corregido: los `bloque`/`titulo`/`detalle` de `sesiones_cun.py`
# usan los nombres EXACTOS del libro de calificaciones y no llevan fechas. Mantener
# el puente sería dañino, no inocuo: volvería a mapear un texto YA correcto
# («cierre de la ACA 1» → «cierre de la Quiz») y reintroduciría el error que
# resolvía. Por eso se retira en vez de dejarse como no-op.
#
# Nadie más lo importaba (verificado con grep sobre el repo: solo se usaba dentro
# de `inyectar_evaluacion`). Si algún día un `detalle` vuelve a traer un nombre que
# no existe en el aula, se arregla en `sesiones_cun.py`, que es la fuente.


def _insertar_aviso(md: str, aviso: str) -> str:
    if not aviso:
        return md
    for marca in ("🗺️ **Slides", "🎯 **Objetivos"):
        i = md.find(marca)
        if i > 0:
            return md[:i] + aviso + "\n" + md[i:]
    return md + "\n" + aviso


def _insertar_checklist(md: str, ag: AgendaEval, key: str) -> str:
    items = ag.reservables()
    extra: list[str] = []
    for e in items:
        if e.es_instrumento_cierre:
            extra.append(
                f"- [ ] **{e.code}** ({e.tipo_label} · {e.weight_pct}) **habilitada y visible** en "
                "CDigital, y la ruta ensayada para mostrarla en pantalla"
            )
        else:
            extra.append(
                f"- [ ] **{e.code}** ({e.tipo_label} · {e.weight_pct} · corte {e.corte}) publicado en "
                "CDigital con intentos, tiempo límite y retroalimentación diferida ya configurados"
            )
    for e in ag.abren_hoy:
        if e in items:
            continue
        extra.append(
            f"- [ ] **{e.code}** ({e.tipo_label} · {e.weight_pct} · corte {e.corte}) **habilitado hoy** "
            "en CDigital y anunciado en clase (su ventana abre en esta sesión)"
        )
    for e in ag.semana:
        cuando = ("cierra **después de este último encuentro**" if ag.ultima
                  else "cierra **antes del próximo encuentro**")
        extra.append(
            f"- [ ] Anunciar en clase que **{e.code}** ({e.tipo_label} · {e.weight_pct}) {cuando} "
            "(la fecha exacta, leída desde CDigital)"
        )
    for e in ag.recien:
        extra.append(
            f"- [ ] Nota de **{e.code}** ({e.weight_pct}) revisada en el libro de calificaciones "
            "antes de entrar: hoy se devuelve"
        )
    if not extra:
        return md
    m = re.search(r"^✅ \*\*Checklist[^\n]*$", md, re.M)
    if not m:
        return md
    return md[:m.end()] + "\n" + "\n".join(extra) + md[m.end():]


def inyectar_evaluacion(md: str, key: str, n: int) -> str:
    """Mete en el guion la evaluación real del aula (aviso + fase + plan + checklist)."""
    # La línea «- **Detalle:**» ya no se sanea: llega correcta desde `sesiones_cun.py`
    # (nombres del aula, sin fechas de periodo). Ver la nota «RETIRADO» más arriba.
    ag = agenda_sesion(key, n)
    if ag.vacia:
        return md
    md = _insertar_aviso(md, bloque_aviso(key, n, ag))
    fase = fase_evaluacion(key, n, ag)
    if fase:
        nombre, mins, cuerpo = fase
        md2, viejos, nuevos, aplicada = _reescribir_plan(md, nombre, mins)
        if viejos:
            pos = len(viejos) - 1
            nota = _nota_replan(viejos, nuevos, md2, aplicada)
            cuerpo_final = f"{nota}\n\n{cuerpo}" if nota else cuerpo
            md = _ajustar_cuerpo_fases(
                md2, viejos, nuevos, pos, nombre, cuerpo_final, aplicada
            )
    md = _insertar_checklist(md, ag, key)
    return md


def main() -> None:
    """`python config/slides/guion_evaluacion.py` → qué evalúa cada sesión de cada curso."""
    for key in ("proyecto1", "creatividad", "investigacion", "tg2", "tg3"):
        print(f"=== {key} · {desglose(key)}")
        for n in sorted(fechas_sesiones(key)):
            ag = agenda_sesion(key, n)
            fase = fase_evaluacion(key, n, ag)
            def _c(lst):
                return ",".join(e.code for e in lst) or "—"
            print(
                f"  S{n:02d} hoy={_c(ag.hoy)} | abren={_c(ag.abren_hoy)} | "
                f"semana={_c(ag.semana)} | recien={_c(ag.recien)} | "
                f"fase={(fase[0] + ' ' + str(fase[1]) + 'min') if fase else '—'}"
            )
        print()


if __name__ == "__main__":
    main()
