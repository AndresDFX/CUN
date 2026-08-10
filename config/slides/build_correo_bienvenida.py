# -*- coding: utf-8 -*-
"""Genera `Correo de bienvenida.docx` (marca CUN) — solo rutas docentes/internas.

Correo corto: quién soy · grupo(s) · horario · contacto.
Fuente de datos: `config/cursos/carga_academica_2026.json` (+ horarios confirmados).

Salida (NUNCA en Clases/ — esa carpeta es solo material compartido con estudiantes):
  <Asignatura>/2026/<grupo>/Correo de bienvenida.docx
  Si hay varios grupos: también <Asignatura>/Correo de bienvenida.docx (copia multi-grupo)

Uso:
  python config/slides/build_correo_bienvenida.py
  python config/slides/build_correo_bienvenida.py proyecto1
También se invoca desde `sync_clases_estudiantes.py` (regenera rutas internas; no escribe en Clases/).
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))

from carga_academica import (  # noqa: E402
    bold_var,
    course_dir,
    curso as carga_curso,
    docente as _docente_pair,
    fmt_dmy,
    hora_inicio_efectiva,
    load_carga,
    _parse_date,
)
from sesiones_cun import COURSES, meet_url  # noqa: E402

URL_CDIGITAL = "[URL CDigital — campus del curso pendiente]"
from guion_md_a_docx import convert as md_to_docx  # noqa: E402

CORREO_NAME = "Correo de bienvenida.docx"
COURSE_KEYS = ("proyecto1", "investigacion", "creatividad", "tg2", "tg3")


def _grupos_txt(c: dict) -> str:
    groups = list(c.get("groups") or [])
    if not groups:
        return "[Grupo(s) — pendiente]"
    return " / ".join(groups)


def _titulo_display(key: str, c: dict) -> str:
    return c.get("titulo_largo") or COURSES.get(key, {}).get("titulo_largo") or c.get("titulo_corto") or key


def _primera_sesion(key: str) -> dict:
    ses = (COURSES.get(key) or {}).get("sesiones") or [{}]
    return ses[0]


def correo_md(key: str, grupo: str | None = None) -> str:
    """Correo de bienvenida. `grupo` = código del grupo destinatario (no la lista entera).

    Todos los datos salen de fuentes que ya existen: `sesiones_cun` (fecha y carácter de
    la Sesión 01, unidad diferida), `carga_academica_2026.json` (horario, Meet, cierre
    del grupo) y la carpeta del estudiante (lectura autónoma de la S01).
    """
    c = carga_curso(key)
    _, correo = _docente_pair()
    titulo = _titulo_display(key, c)
    grupos = grupo or _grupos_txt(c)
    etiqueta_grupo = "Grupo" if grupo or len(list(c.get("groups") or [])) == 1 else "Grupo(s)"
    horario = (c.get("horario") or {}).get("texto_corto") or (c.get("horario") or {}).get("texto") or "—"
    s1 = _primera_sesion(key)
    primera = s1.get("fecha", "—")
    diferida = (s1.get("unidad_diferida") or "").strip()
    es_pregrado = c.get("nivel") != "especializacion"

    filas = [
        f"| **Curso** | {bold_var(titulo)} |",
        f"| **{etiqueta_grupo}** | {bold_var(grupos)} |",
        f"| **Horario** | {bold_var(horario)} · empezamos puntuales a las "
        f"{bold_var(hora_inicio_efectiva(key))} |",
        f"| **Primera clase** | {bold_var(primera)} — sesión de **encuadre**: presento el curso, "
        "las ACAs y nos conocemos. **No se dicta tema**; el contenido arranca en la Sesión 02. |",
        f"| **Google Meet** (mismo enlace toda la serie) | {meet_url(key, c['titulo_corto'])} |",
        f"| **Aula CDigital** (entregas y notas) | {URL_CDIGITAL} |",
    ]
    if grupo:
        meta = (c.get("grupos") or {}).get(grupo) or {}
        cierre = _parse_date(meta.get("cierre"))
        if cierre:
            filas.append(f"| **Cierre de tu grupo** | {bold_var(fmt_dmy(cierre))} |")
    filas.append(
        "| **Antes de la Sesión 02** | la **lectura autónoma** de la semana viene en la carpeta "
        "del curso, en `Clases/Sesion 01 - …/`: el PDF y el archivo "
        "`Lectura autonoma - Sesion 01.txt`, que dice qué leer, cuánto tarda y qué traer. |"
    )
    if es_pregrado:
        filas.append(
            "| **Si el día de clase es festivo** | la clase **no se cancela**: queda como "
            "**clase autónoma**, con la actividad publicada en CDigital. |"
        )
    filas.append(f"| **Docente (contacto)** | el Docente · {correo} |")
    tabla = "\n".join(filas)

    nota_diferida = f"\n\n> {diferida}" if diferida else ""

    return f"""# Correo de bienvenida — {titulo}

**Asunto sugerido:** Bienvenida · {titulo} — primera clase {primera}

---

Estimada/o estudiante:

Te doy la bienvenida al curso **{titulo}**. Soy el Docente de la asignatura.

| Dato | Valor |
| :--- | :--- |
{tabla}

**Lo mínimo para el primer día:** conéctate por el Meet a la hora indicada y ten a mano la
carpeta del curso. En esa primera sesión revisamos juntos las ACAs (qué se entrega, cuándo
y con qué formato) y dejamos acordadas las reglas de trabajo.{nota_diferida}

Cualquier duda, escríbeme al correo de contacto.

Cordialmente,
**El Docente**
{correo}
Corporación Unificada Nacional de Educación Superior — CUN
"""


def write_md_as_docx(
    md_text: str,
    docx_path: str | Path,
    *,
    subtitle: str | None = None,
    footer: str | None = None,
) -> None:
    fd, tmp = tempfile.mkstemp(suffix=".md", prefix="correo_bienvenida_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(md_text)
        md_to_docx(str(tmp), str(docx_path), brand=True, subtitle=subtitle, footer=footer)
    finally:
        if os.path.isfile(tmp):
            os.remove(tmp)


def remove_from_clases(root: Path) -> None:
    """Garantiza que no quede copia en la carpeta compartida con estudiantes."""
    stale = root / "Clases" / CORREO_NAME
    if stale.is_file():
        stale.unlink()
        print("RM (no compartir en Clases/)", stale)


def build_course(key: str, *, copy_to_grupos: bool = True) -> list[Path]:
    """Escribe el correo en `2026/<grupo>/` (y raíz si multi-grupo). Nunca en Clases/."""
    if key not in COURSE_KEYS:
        raise KeyError(f"Curso desconocido: {key}")
    c = carga_curso(key)
    root = course_dir(key)
    remove_from_clases(root)

    groups = [str(g) for g in (c.get("groups") or [])]
    sub = f"Correo de bienvenida · {c['titulo_corto']}"
    foot = f"CUN · {c['titulo_corto']} · uso docente · Vigilada Mineducación"
    written: list[Path] = []

    if not groups:
        # Sin grupo en carga: copia en raíz del curso (interno).
        out = root / CORREO_NAME
        write_md_as_docx(correo_md(key), out, subtitle=sub, footer=foot)
        print("OK", out)
        written.append(out)
        return written

    if copy_to_grupos:
        for g in groups:
            gdir = root / "2026" / g
            gdir.mkdir(parents=True, exist_ok=True)
            dst = gdir / CORREO_NAME
            # Un correo POR GRUPO: el estudiante de 54450 no debe recibir un correo que
            # nombra los otros dos grupos ni el cierre que no es el suyo.
            write_md_as_docx(correo_md(key, g), dst, subtitle=sub, footer=foot)
            print("OK", dst)
            written.append(dst)

    if len(groups) > 1:
        # Multi-grupo: copia de referencia en la raíz del curso, esta sí con los 3 códigos.
        root_copy = root / CORREO_NAME
        write_md_as_docx(correo_md(key), root_copy, subtitle=sub, footer=foot)
        print("OK multi-grupo (raíz)", root_copy)
        written.append(root_copy)

    return written


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    keys = [a for a in argv if not a.startswith("-")] or list(COURSE_KEYS)
    load_carga(force=True)
    for key in keys:
        build_course(key)
    print(f"Listo: Correo de bienvenida regenerado en rutas docentes ({len(keys)} curso(s)).")


if __name__ == "__main__":
    main()
