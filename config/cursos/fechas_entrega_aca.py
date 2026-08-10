# -*- coding: utf-8 -*-
"""Fechas de entrega ACA — cálculo regenerable (los 5 cursos CUN).

Regla (documentada · usada por build_acas / hitos / Presentaciones / Manuales):

1. Periodo de entregas documentales = ``[inicio, recepción]`` de
   ``carga_academica_2026.json`` (la recepción es la fecha máx. de trabajos;
   el cierre de notas puede ser posterior).
2. Se reparte ese tramo según los **pesos** del componente (p. ej. 30/30/40,
   25/25/42, EV05/EXAM 50/50). El ítem final cae en el día de clase en o
   antes de la recepción.
3. Fecha de entrega = fin del tramo *n*, ajustada al **día de clase semanal**
   del curso (`horario.weekday` confirmado). Si el target no cae ese día,
   se usa el día de clase **anterior** (o el viernes académico si no hubiera
   weekday — no aplica a estos 5 cursos).
4. Las fechas quedan estrictamente crecientes (mín. +1 semana de clase si
   colisionan).
5. Proyecto I — autoevaluación / coevaluación: ventanas **después** de ACA 3
   y hasta el cierre de notas (coev primero, autoev al final), alineado a
   ESP329 / Manual (8% de cierre).
6. TG3: EV05 y EXAM se calculan **por grupo** cuando recepción/cierre difieren
   (54450 vs 54466/54467).
7. Límite de nota docente (hitos) = día de clase ~+7 días tras la entrega.

Inicio operativo del semestre 2026 (pedido docente): **2026-08-10**.
No hardcodear fechas sueltas en enunciados: leer esta API.

Uso:
  from fechas_entrega_aca import entregas_curso, fmt_entrega, blocks_para_slide
  python config/cursos/fechas_entrega_aca.py   # imprime tabla
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from carga_academica import curso, fmt_dmy, fmt_dmy_largo, load_carga, _parse_date

DIAS = ("lun", "mar", "mié", "jue", "vie", "sáb", "dom")

# Catálogo de componentes evaluados (pesos oficiales / orientativos).
# id estable → usado en builds, LEEME, hitos.
ACA_COMPONENTES: dict[str, list[dict[str, Any]]] = {
    "proyecto1": [
        {"id": "aca1", "code": "ACA 1", "label": "ACA 1", "weight": 25, "kind": "aca"},
        {"id": "aca2", "code": "ACA 2", "label": "ACA 2", "weight": 25, "kind": "aca"},
        {"id": "aca3", "code": "ACA 3", "label": "ACA 3", "weight": 42, "kind": "aca"},
        {"id": "coev", "code": "Coevaluación", "label": "Coevaluación", "weight": 4, "kind": "ventana"},
        {"id": "auto", "code": "Autoevaluación", "label": "Autoevaluación", "weight": 4, "kind": "ventana"},
    ],
    "investigacion": [
        {"id": "aca1", "code": "ACA 1", "label": "Corte 1", "weight": 30, "kind": "aca"},
        {"id": "aca2", "code": "ACA 2", "label": "Corte 2", "weight": 30, "kind": "aca"},
        {"id": "aca3", "code": "ACA 3", "label": "Corte 3", "weight": 40, "kind": "aca"},
    ],
    "creatividad": [
        {"id": "aca1", "code": "ACA 1", "label": "Corte 1", "weight": 30, "kind": "aca"},
        {"id": "aca2", "code": "ACA 2", "label": "Corte 2", "weight": 30, "kind": "aca"},
        {"id": "aca3", "code": "ACA 3", "label": "Corte 3", "weight": 40, "kind": "aca"},
    ],
    "tg2": [
        {"id": "aca1", "code": "ACA 1", "label": "Corte 1", "weight": 30, "kind": "aca"},
        {"id": "aca2", "code": "ACA 2", "label": "Corte 2", "weight": 30, "kind": "aca"},
        {"id": "aca3", "code": "ACA 3", "label": "Corte 3", "weight": 40, "kind": "aca"},
    ],
    "tg3": [
        {"id": "ev05", "code": "ACA 1 (EV05)", "label": "EV05", "weight": 50, "kind": "aca"},
        {"id": "exam", "code": "ACA 2 (EXAM)", "label": "EXAM", "weight": 50, "kind": "aca"},
    ],
}

REGLA_RESUMEN = (
    "Periodo [inicio–recepción] repartido por pesos del componente; "
    "entrega = día de clase semanal en o antes del fin de tramo "
    "(ultimo item <= recepcion). P1: coev/autoev tras ACA 3 hasta cierre. "
    "Fuente: config/cursos/fechas_entrega_aca.py + carga_academica_2026.json."
)

# ─────────────────────────────────────────────────────────────────────────────
# PROYECTO I — fechas OFICIALES, no calculadas.
#
# Para Proyecto I (AFI/ESP329) las ventanas NO se derivan del reparto por pesos:
# las fija la Coordinación de Gestión del Conocimiento en el
# `Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf`, y esa es la fuente que
# el docente adoptó (2026-08-09) para el Manual, el Calendario oficial y el CSV
# de hitos. El cálculo por pesos se desviaba (daba 31/08 · 28/09 · 09/11 frente a
# los 30/08 · 04/10 · 08/11 reales), lo que ponía fechas equivocadas en los
# enunciados de ACA que reciben los estudiantes. Si cambia el periodo, se
# actualiza ESTA tabla — no se vuelve al cálculo.
#
# (apertura, entrega/cierre, fecha límite de nota docente)
CRONOGRAMA_OFICIAL_P1: dict[str, tuple[date, date, date]] = {
    "aca1": (date(2026, 8, 3), date(2026, 8, 30), date(2026, 9, 7)),
    "aca2": (date(2026, 9, 7), date(2026, 10, 4), date(2026, 10, 12)),
    "aca3": (date(2026, 10, 12), date(2026, 11, 8), date(2026, 11, 16)),
    "coev": (date(2026, 11, 9), date(2026, 11, 15), date(2026, 11, 22)),
    "auto": (date(2026, 11, 16), date(2026, 11, 22), date(2026, 11, 22)),
}
REGLA_OFICIAL_P1 = (
    "Fechas OFICIALES de Coordinación (Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf); "
    "no se calculan por pesos. Cierre y registro de todas las notas: 22/11/2026."
)


def _entregas_oficiales_p1() -> list[EntregaAca]:
    """Proyecto I: ventanas tomadas del cronograma institucional (ver arriba)."""
    return _desde_tabla("proyecto1", CRONOGRAMA_OFICIAL_P1, REGLA_OFICIAL_P1)


# ─────────────────────────────────────────────────────────────────────────────
# CREATIVIDAD e INVESTIGACIÓN — ventanas FIJADAS POR EL DOCENTE (2026-08-10).
#
# Por qué no se calculan: al pasar la Sesión 01 a encuadre (no dicta tema), el
# reparto automático dejaba la ACA 1 cerrando el mismo día de la Sesión 02, es
# decir con CERO clases de contenido cursadas. El docente decidió correr la
# ACA 1 una semana; ACA 2 se corre en consecuencia y ACA 3 se mantiene dentro
# de la fecha de recepción institucional, que es el techo duro:
#   Creatividad  → recepción 19/09/2026 · cierre 27/09/2026
#   Investigación→ recepción 12/09/2026 · cierre 20/09/2026
#
# Clases de contenido que respalda cada entrega (S01 es encuadre en ambos):
#   Creatividad   ACA1 ← S02,S03 · ACA2 ← S04,S05 · ACA3 ← S06
#   Investigación ACA1 ← S02,S03 · ACA2 ← S04     · ACA3 ← S05
#
# (apertura, entrega/cierre, fecha límite de nota docente)
VENTANAS_DOCENTE: dict[str, dict[str, tuple[date, date, date]]] = {
    "creatividad": {
        "aca1": (date(2026, 8, 12), date(2026, 8, 26), date(2026, 9, 2)),
        "aca2": (date(2026, 8, 27), date(2026, 9, 9), date(2026, 9, 16)),
        "aca3": (date(2026, 9, 10), date(2026, 9, 16), date(2026, 9, 23)),
    },
    "investigacion": {
        "aca1": (date(2026, 8, 13), date(2026, 8, 27), date(2026, 9, 3)),
        "aca2": (date(2026, 8, 28), date(2026, 9, 3), date(2026, 9, 10)),
        "aca3": (date(2026, 9, 4), date(2026, 9, 10), date(2026, 9, 17)),
    },
}
REGLA_VENTANAS_DOCENTE = (
    "Ventanas fijadas por el Docente (2026-08-10) para que cada ACA tenga clases de "
    "contenido cursadas antes de su cierre — la Sesión 01 es de encuadre y no dicta tema. "
    "Respetan la fecha de recepción institucional del curso."
)


def _desde_tabla(key: str, tabla: dict, regla: str) -> list[EntregaAca]:
    """Construye las entregas de un curso a partir de una tabla explícita de fechas."""
    out: list[EntregaAca] = []
    for comp in ACA_COMPONENTES[key]:
        if comp["id"] not in tabla:
            continue
        ap, ent, nota = tabla[comp["id"]]
        out.append(
            EntregaAca(
                id=comp["id"],
                code=comp["code"],
                label=comp["label"],
                weight=comp["weight"],
                kind=comp["kind"],
                apertura=ap,
                entrega=ent,
                nota_docente=nota,
                regla=regla,
            )
        )
    return out


@dataclass(frozen=True)
class EntregaAca:
    id: str
    code: str
    label: str
    weight: int
    kind: str
    apertura: date
    entrega: date
    nota_docente: date | None
    grupo: str | None = None
    regla: str = REGLA_RESUMEN

    @property
    def weight_pct(self) -> str:
        return f"{self.weight}%"


def snap_dia_clase(target: date, weekday: int) -> date:
    """Día de clase semanal en o antes de ``target`` (0=lun … 6=dom)."""
    return target - timedelta(days=(target.weekday() - weekday) % 7)


def snap_viernes(target: date) -> date:
    """Viernes académico en o antes de ``target`` (fallback)."""
    return snap_dia_clase(target, 4)


def _next_class_after(prev: date, weekday: int) -> date:
    d = prev + timedelta(days=1)
    delta = (weekday - d.weekday()) % 7
    return d + timedelta(days=delta)


def _nota_docente(entrega: date, weekday: int) -> date:
    target = entrega + timedelta(days=7)
    d = snap_dia_clase(target, weekday)
    if d <= entrega:
        d = _next_class_after(entrega, weekday)
    return d


def _repartir_acas(
    inicio: date,
    recepcion: date,
    weekday: int,
    comps: list[dict[str, Any]],
    grupo: str | None = None,
) -> list[EntregaAca]:
    """Reparte componentes kind=aca en [inicio, recepción]."""
    acas = [c for c in comps if c["kind"] == "aca"]
    if not acas:
        return []
    span = max(1, (recepcion - inicio).days)
    total_w = sum(int(c["weight"]) for c in acas)
    cum = 0
    prev = inicio - timedelta(days=1)
    out: list[EntregaAca] = []
    apertura = inicio

    for i, c in enumerate(acas):
        w = int(c["weight"])
        cum += w
        if i == len(acas) - 1:
            target = recepcion
        else:
            target = inicio + timedelta(days=round(span * cum / total_w))
        entrega = snap_dia_clase(target, weekday)
        if entrega < inicio:
            entrega = _next_class_after(inicio - timedelta(days=1), weekday)
        if entrega <= prev:
            entrega = _next_class_after(prev, weekday)
        if entrega > recepcion:
            entrega = snap_dia_clase(recepcion, weekday)
            if entrega <= prev:
                entrega = recepcion  # último recurso (puede no ser día de clase)
        nota = _nota_docente(entrega, weekday)
        # Garantizar apertura < entrega (periodos cortos: Inv/Creatividad).
        if apertura >= entrega:
            apertura = inicio if i == 0 else (prev + timedelta(days=1))
            if apertura >= entrega:
                apertura = entrega  # mismo día: ventana de un día
        out.append(
            EntregaAca(
                id=c["id"],
                code=c["code"],
                label=c["label"],
                weight=w,
                kind="aca",
                apertura=apertura,
                entrega=entrega,
                nota_docente=nota,
                grupo=grupo,
            )
        )
        prev = entrega
        # Siguiente apertura: día de nota docente si aún queda margen; si no, día +1.
        nxt_ap = nota if nota > entrega else entrega + timedelta(days=1)
        apertura = nxt_ap
    return out


def _ventanas_p1(
    acas: list[EntregaAca],
    cierre: date,
    weekday: int,
) -> list[EntregaAca]:
    """Coevaluación y autoevaluación tras ACA 3 hasta cierre."""
    if not acas:
        return []
    aca3 = acas[-1]
    coev_ini = aca3.entrega + timedelta(days=1)
    # ~1 semana de coev, cerrando en día de clase
    coev_fin = snap_dia_clase(min(cierre - timedelta(days=6), aca3.entrega + timedelta(days=7)), weekday)
    if coev_fin < coev_ini:
        coev_fin = min(cierre, coev_ini + timedelta(days=6))
    auto_ini = coev_fin + timedelta(days=1)
    if auto_ini > cierre:
        auto_ini = cierre
    auto_fin = cierre
    return [
        EntregaAca(
            id="coev",
            code="Coevaluación",
            label="Coevaluación",
            weight=4,
            kind="ventana",
            apertura=coev_ini,
            entrega=coev_fin,
            nota_docente=cierre,
            regla=REGLA_RESUMEN + " Coev. justo después de ACA 3.",
        ),
        EntregaAca(
            id="auto",
            code="Autoevaluación",
            label="Autoevaluación",
            weight=4,
            kind="ventana",
            apertura=auto_ini,
            entrega=auto_fin,
            nota_docente=cierre,
            regla=REGLA_RESUMEN + " Autoev. en la última semana hasta cierre.",
        ),
    ]


def entregas_para_grupo(key: str, grupo: str | None = None) -> list[EntregaAca]:
    """Lista de entregas para un curso (y grupo, si aplica — TG3)."""
    c = curso(key)
    comps = ACA_COMPONENTES[key]
    if grupo and grupo in c["grupos"]:
        g = c["grupos"][grupo]
        inicio = _parse_date(g["inicio"])
        recepcion = _parse_date(g["recepcion"])
        cierre = _parse_date(g["cierre"])
    else:
        inicio = _parse_date(c["inicio"])
        recepcion = _parse_date(c["recepcion"])
        cierre = _parse_date(c["cierre"])
        grupo = None
    if key == "proyecto1":
        # Fechas institucionales, no calculadas (ver CRONOGRAMA_OFICIAL_P1).
        return _entregas_oficiales_p1()
    if key in VENTANAS_DOCENTE:
        # Ventanas fijadas por el docente (ver VENTANAS_DOCENTE).
        return _desde_tabla(key, VENTANAS_DOCENTE[key], REGLA_VENTANAS_DOCENTE)
    weekday = int(c["horario"]["weekday"])
    return _repartir_acas(inicio, recepcion, weekday, comps, grupo=grupo)


def entregas_curso(key: str) -> list[EntregaAca] | dict[str, list[EntregaAca]]:
    """Para TG3 (varios cierres) → dict por grupo; resto → lista."""
    c = curso(key)
    groups = list(c.get("groups") or [])
    if key == "tg3" and len(groups) > 1:
        # Compactar grupos con mismo (inicio, recepción, cierre)
        by_sig: dict[tuple, list[str]] = {}
        for g in groups:
            m = c["grupos"][g]
            sig = (m["inicio"], m["recepcion"], m["cierre"])
            by_sig.setdefault(sig, []).append(g)
        out: dict[str, list[EntregaAca]] = {}
        for gs in by_sig.values():
            # calcular una vez; etiquetar con el primer grupo representativo
            # y clonar por cada código
            base = entregas_para_grupo(key, gs[0])
            for g in gs:
                out[g] = [
                    EntregaAca(
                        id=e.id,
                        code=e.code,
                        label=e.label,
                        weight=e.weight,
                        kind=e.kind,
                        apertura=e.apertura,
                        entrega=e.entrega,
                        nota_docente=e.nota_docente,
                        grupo=g,
                        regla=e.regla + f" Grupo {g}.",
                    )
                    for e in base
                ]
        return out
    return entregas_para_grupo(key)


def entrega_por_id(key: str, aca_id: str, grupo: str | None = None) -> EntregaAca:
    data = entregas_curso(key)
    if isinstance(data, dict):
        if grupo is None:
            # fecha “canónica” = la más temprana entre grupos (avisar divergencia)
            grupo = sorted(data.keys())[0]
        items = data[grupo]
    else:
        items = data
    for e in items:
        if e.id == aca_id:
            return e
    raise KeyError(f"{key}/{aca_id}")


def fmt_entrega(d: date, *, largo: bool = True) -> str:
    return fmt_dmy_largo(d) if largo else fmt_dmy(d)


def texto_fecha_enunciado(e: EntregaAca, weekday: int) -> str:
    """Bloque markdown para el enunciado ACA."""
    dia = DIAS[weekday]
    if e.kind == "ventana":
        return (
            f"**Ventana de diligenciamiento:** {fmt_dmy(e.apertura)} – {fmt_dmy(e.entrega)} "
            f"(cierra **{fmt_dmy_largo(e.entrega)}**).\n\n"
            f"**Día de referencia del curso:** {dia}. Entrega / cierre solo por **CDigital**."
        )
    g = f" · Grupo {e.grupo}" if e.grupo else ""
    return (
        f"**Fecha de entrega (CDigital){g}:** **{fmt_dmy_largo(e.entrega)}** "
        f"({dia} · día de clase).\n\n"
        f"**Ventana:** apertura {fmt_dmy(e.apertura)} – cierre {fmt_dmy(e.entrega)}.\n\n"
        f"> Fecha calculada con la regla del periodo "
        f"(pesos + día de clase; ver Presentación del Curso / Manual)."
    )


def texto_fecha_curso(key: str, aca_id: str) -> str:
    """Texto de fecha para enunciado (TG3: lista por grupo si divergen)."""
    c = curso(key)
    weekday = int(c["horario"]["weekday"])
    data = entregas_curso(key)
    if isinstance(data, dict):
        # Compactar por fecha de entrega
        by_date: dict[date, list[str]] = {}
        sample: dict[date, EntregaAca] = {}
        for g, items in data.items():
            for e in items:
                if e.id != aca_id:
                    continue
                by_date.setdefault(e.entrega, []).append(g)
                sample[e.entrega] = e
        if not by_date:
            raise KeyError(f"{key}/{aca_id}")
        if len(by_date) == 1:
            e = next(iter(sample.values()))
            return texto_fecha_enunciado(e, weekday)
        lines = ["**Fechas de entrega (CDigital) según grupo:**", ""]
        for d in sorted(by_date):
            gs = " / ".join(sorted(by_date[d]))
            e = sample[d]
            lines.append(
                f"- **Grupos {gs}:** **{fmt_dmy_largo(d)}** "
                f"(ventana {fmt_dmy(e.apertura)} – {fmt_dmy(e.entrega)})"
            )
        lines.append("")
        lines.append(
            f"**Día de clase:** {DIAS[weekday]}. "
            "> Regla: pesos + día de clase sobre [inicio–recepción] por oferta."
        )
        return "\n".join(lines)
    e = entrega_por_id(key, aca_id)
    return texto_fecha_enunciado(e, weekday)


def blocks_para_slide(key: str, grupo: str | None = None) -> list[dict]:
    """Bloques ``{label, start, end, pct}`` para ``fechas_inicio_fin_slide``."""
    items = entregas_para_grupo(key, grupo)
    # P1: fusionar coev+auto en una tarjeta 8%
    if key == "proyecto1":
        acas = [e for e in items if e.kind == "aca"]
        vents = [e for e in items if e.kind == "ventana"]
        blocks = [
            {
                "label": e.label,
                "start": e.apertura,
                "end": e.entrega,
                "pct": e.weight_pct,
            }
            for e in acas
        ]
        if vents:
            blocks.append(
                {
                    "label": "Coev. + Autoev.",
                    "start": vents[0].apertura,
                    "end": vents[-1].entrega,
                    "pct": "8%",
                }
            )
        return blocks
    return [
        {
            "label": e.label,
            "start": e.apertura,
            "end": e.entrega,
            "pct": e.weight_pct + ("*" if key == "tg2" else ""),
        }
        for e in items
    ]


def blocks_tg3_slide() -> list[dict]:
    """TG3 en Presentación del Curso: usa el cierre mayoritario (22/11) + nota."""
    # Representativo 54466 (mismo que 54467)
    return blocks_para_slide("tg3", "54466")


def resumen_tabla_markdown(key: str) -> str:
    data = entregas_curso(key)
    lines = [
        f"| Componente | Entrega | Apertura | Nota docente | Regla |",
        f"| :--- | :--- | :--- | :--- | :--- |",
    ]
    if isinstance(data, dict):
        for g, items in data.items():
            for e in items:
                lines.append(
                    f"| **{e.code}** ({g}) | {fmt_dmy(e.entrega)} | {fmt_dmy(e.apertura)} | "
                    f"{fmt_dmy(e.nota_docente) if e.nota_docente else '—'} | pesos+día clase |"
                )
    else:
        for e in data:
            lines.append(
                f"| **{e.code}** | {fmt_dmy(e.entrega)} | {fmt_dmy(e.apertura)} | "
                f"{fmt_dmy(e.nota_docente) if e.nota_docente else '—'} | pesos+día clase |"
            )
    return "\n".join(lines)


def hitos_aca_rows(
    key: str,
    grupo: str | None = None,
    *,
    esencial: bool = True,
) -> list[tuple[str, date, str]]:
    """Filas (label, date, note) para Calendar de hitos docentes.

    Con ``esencial=True`` (default): solo deadlines — cierre entrega / límite nota
    docente; en ventanas (coeval/autoeval) habilitar + cierre. Sin aperturas ACA.
    """
    items = entregas_para_grupo(key, grupo)
    rows: list[tuple[str, date, str]] = []
    for e in items:
        if e.kind == "ventana":
            rows.append(
                (
                    f"{e.code} — ventana",
                    e.apertura,
                    f"{e.code} {e.weight}% · ventana {fmt_dmy(e.apertura)}–{fmt_dmy(e.entrega)}. Habilitar en CDigital.",
                )
            )
            rows.append(
                (
                    f"{e.code} — cierre",
                    e.entrega,
                    f"Cierre {e.code}.",
                )
            )
        else:
            if not esencial:
                rows.append(
                    (
                        f"{e.code} — apertura",
                        e.apertura,
                        f"Apertura {e.code} ({e.weight}%). Configurar en CDigital con rúbrica.",
                    )
                )
            rows.append(
                (
                    f"{e.code} — cierre entrega",
                    e.entrega,
                    f"Cierre entrega {e.code} (estudiantes).",
                )
            )
            if e.nota_docente:
                rows.append(
                    (
                        f"{e.code} — límite nota docente",
                        e.nota_docente,
                        f"Fecha límite ingreso de nota {e.code}.",
                    )
                )
    return rows


def as_json_dict() -> dict:
    """Snapshot serializable de todas las fechas (para docs / depuración)."""
    load_carga()
    out: dict[str, Any] = {"regla": REGLA_RESUMEN, "cursos": {}}
    for key in ACA_COMPONENTES:
        data = entregas_curso(key)
        if isinstance(data, dict):
            out["cursos"][key] = {
                g: [
                    {
                        "id": e.id,
                        "code": e.code,
                        "weight": e.weight,
                        "apertura": e.apertura.isoformat(),
                        "entrega": e.entrega.isoformat(),
                        "nota_docente": e.nota_docente.isoformat() if e.nota_docente else None,
                    }
                    for e in items
                ]
                for g, items in data.items()
            }
        else:
            out["cursos"][key] = [
                {
                    "id": e.id,
                    "code": e.code,
                    "weight": e.weight,
                    "apertura": e.apertura.isoformat(),
                    "entrega": e.entrega.isoformat(),
                    "nota_docente": e.nota_docente.isoformat() if e.nota_docente else None,
                }
                for e in data
            ]
    return out


def main() -> None:
    import json
    print(REGLA_RESUMEN)
    print()
    for key in ACA_COMPONENTES:
        c = curso(key)
        print(f"=== {key} · {c['titulo_corto']} ===")
        print(f"inicio={c['inicio']} recepcion={c['recepcion']} cierre={c['cierre']} "
              f"weekday={DIAS[c['horario']['weekday']]}")
        print(resumen_tabla_markdown(key))
        print()
    print(json.dumps(as_json_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
