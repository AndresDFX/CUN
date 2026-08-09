# -*- coding: utf-8 -*-
"""Carga `carga_academica_2026.json` — fuente editable de grupos/horarios/bloques 2026."""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

_JSON = Path(__file__).resolve().parent / "carga_academica_2026.json"
_CACHE: dict | None = None


def _parse_date(value) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def load_carga(force: bool = False) -> dict:
    global _CACHE
    if _CACHE is not None and not force:
        return _CACHE
    with open(_JSON, encoding="utf-8") as f:
        _CACHE = json.load(f)
    return _CACHE


def docente() -> tuple[str, str]:
    d = load_carga()["docente"]
    return d["nombre"], d["correo"]


def curso(key: str) -> dict:
    data = load_carga()["cursos"][key]
    return data


def workspace_root() -> Path:
    """Raíz del workspace `Cursos/` (dos niveles arriba de este archivo)."""
    return Path(__file__).resolve().parents[2]


def course_dir(key: str) -> Path:
    """Ruta absoluta de la carpeta de asignatura (`folder` relativo en el JSON)."""
    rel = curso(key)["folder"].replace("\\", "/")
    return (workspace_root() / Path(rel)).resolve()


def fmt_dmy(d: date | None) -> str:
    if not d:
        return "—"
    return d.strftime("%d/%m/%Y")


def fmt_dmy_largo(d: date | None) -> str:
    """03 de agosto – estilo portada."""
    if not d:
        return "—"
    meses = (
        "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    )
    return f"{d.day:02d} de {meses[d.month]} de {d.year}"


def pregrado_build_dict(key: str) -> dict:
    """Shape esperado por `build_pregrado_cursos.COURSES` (fechas como date)."""
    c = curso(key)
    folder_name = Path(c["folder"]).name
    group_meta = {}
    for g, meta in c["grupos"].items():
        group_meta[g] = {
            "periodo": meta["periodo"],
            "inicio": _parse_date(meta["inicio"]),
            "recepcion": _parse_date(meta["recepcion"]),
            "cierre": _parse_date(meta["cierre"]),
            "bloque": meta.get("bloque"),
            "id_grupo": meta.get("id_grupo"),
            "capacidad": meta.get("capacidad"),
            "inscritos": meta.get("inscritos"),
            "num_nivel": meta.get("num_nivel"),
        }
    h = c["horario"]
    return {
        "key": key,
        "folder": folder_name,
        "titulo_corto": c["titulo_corto"],
        "titulo_largo": c["titulo_largo"],
        "codigo": c.get("codigo_display") or c["codigo"],
        "codigo_corto": c["codigo"],
        "creditos": c["creditos"],
        "periodos_nota": c["periodos_nota"],
        "bloque_portada": c.get("bloque_portada"),
        "modalidad": c.get("modalidad", "VIRTUAL"),
        "jornada": c.get("jornada"),
        "dependencia": c.get("dependencia"),
        "unidad": c.get("unidad"),
        "sede_entrega": c.get("sede_entrega", "Virtual"),
        "aula": c.get("aula", "Aula virtual - Google Meet"),
        "horario_txt": h["texto"],
        "horario_corto": h.get("texto_corto") or h["texto"],
        "weekday": h["weekday"],
        "hora_ini": h["hora_ini"],
        "hora_fin": h["hora_fin"],
        "hora_ics": tuple(h["hora_ics"]),
        "inicio": _parse_date(c["inicio"]),
        "cierre": _parse_date(c["cierre"]),
        "recepcion": _parse_date(c["recepcion"]),
        "groups": list(c["groups"]),
        "group_meta": group_meta,
        "sin_syllabus": bool(c.get("sin_syllabus")),
    }


def _parse_hora_ampm(hora: str) -> datetime:
    """Parsea `hora_ini` del JSON (`8:00 PM`, `5:00 pm`, `20:00`, …)."""
    s = (hora or "").strip()
    if not s:
        raise ValueError("hora vacía")
    for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M", "%H%M%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    # Fallback: "8:00 pm" / "20:00"
    m = re.match(r"^(\d{1,2}):(\d{2})\s*([ap]\.?m\.?)?$", s, re.I)
    if not m:
        raise ValueError(f"hora no reconocida: {hora!r}")
    hh, mm = int(m.group(1)), int(m.group(2))
    ampm = (m.group(3) or "").lower().replace(".", "")
    if ampm.startswith("p") and hh < 12:
        hh += 12
    elif ampm.startswith("a") and hh == 12:
        hh = 0
    return datetime(2000, 1, 1, hh, mm)


def fmt_hora_ampm(dt: datetime) -> str:
    """Formato estudiante: `8:10 pm` (sin cero a la izquierda; am/pm en minúsculas)."""
    h12 = dt.hour % 12 or 12
    ampm = "am" if dt.hour < 12 else "pm"
    return f"{h12}:{dt.minute:02d} {ampm}"


def hora_inicio_efectiva(key: str, offset_min: int = 10) -> str:
    """Horario oficial de clase + N minutos (ingreso / inicio de contenido).

    Ej.: Proyecto I `8:00 PM` → `8:10 pm`.
    """
    h = curso(key)["horario"]["hora_ini"]
    base = _parse_hora_ampm(h)
    return fmt_hora_ampm(base + timedelta(minutes=offset_min))


def footer_inicio_efectivo(key: str, offset_min: int = 10) -> str:
    """Texto exacto del pie de slides: `Inicio 8:10 pm`."""
    return f"Inicio {hora_inicio_efectiva(key, offset_min)}"


def bold_var(text) -> str:
    """Marca un dato de periodo/oferta en negrita (`**…**` → motor `_rich`).

    Usar en Presentación del Curso para lo que cambia entre semestres
    (periodo, grupos, bloque, fechas, horario de la oferta, placeholders Meet/CDigital).
    No usar para docente/correo fijos, temario ni marca CUN.
    """
    return f"**{text}**"


def groups_label(groups: list[str] | None) -> str:
    """Etiqueta de grupo(s) — solo para la portada (primera slide) de la Presentación del Curso."""
    groups = list(groups or [])
    if not groups:
        return ""
    if len(groups) == 1:
        return f"**Grupo:** {bold_var(groups[0])}"
    return f"**Grupos:** {bold_var(' / '.join(groups))}"


def cover_meta_lines(
    key: str,
    *,
    extra: list[str] | None = None,
    include_area: bool = False,
    horario_suffix: str = "",
) -> list[str]:
    """Líneas de portada (Presentación del Curso). Único lugar de slides con grupo(s).

    Los valores de periodo/oferta van en negrita (`bold_var`).
    Contacto: correo institucional sin nombre propio (material proyectado = «el Docente»).
    """
    c = curso(key)
    ini = _parse_date(c["inicio"])
    cie = _parse_date(c["cierre"])
    h = c["horario"]
    periodo = c["periodos_nota"]
    h_txt = h.get("texto_corto") or h["texto"]
    if horario_suffix:
        h_txt = f"{h_txt}{horario_suffix}"

    if " / " in str(periodo):
        periodo_ln = (
            f"**Periodos de referencia:** {bold_var(periodo)} · "
            f"desde {bold_var(fmt_dmy_largo(ini))}"
        )
    else:
        label = "Periodo" if c.get("nivel") == "especializacion" else "Periodo de referencia"
        rango = f"{fmt_dmy_largo(ini)} – {fmt_dmy_largo(cie)}"
        periodo_ln = f"**{label}:** {bold_var(periodo)} · {bold_var(rango)}"

    modalidad = (
        "**Modalidad:** Virtual — encuentro sincrónico semanal por Google Meet"
        if c.get("nivel") == "especializacion"
        else "**Modalidad:** Virtual — encuentro sincrónico por Google Meet"
    )
    lines = [
        periodo_ln,
        modalidad,
        f"**Horario confirmado:** {bold_var(h_txt)}",
    ]
    g_ln = groups_label(c.get("groups"))
    if g_ln:
        lines.append(g_ln)
    if c.get("bloque_portada"):
        lines.append(f"**Bloque:** {bold_var(c['bloque_portada'])}")
    if include_area and c.get("dependencia"):
        lines.append(f"**Área / dependencia:** {c['dependencia']}")
    _, correo = docente()
    # Sin nombre propio en slides; correo como canal de contacto.
    lines.append(f"**Contacto del Docente:** {correo}")
    if extra:
        lines.extend(extra)
    return lines
