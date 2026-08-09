# -*- coding: utf-8 -*-
"""Contenido RICO por sesión para las decks CUN (Proyecto I, Investigación, Creatividad, TG2, TG3).

Cada sesión puede tener su propio guion proyectable en un JSON:

    config/slides/content/cun_<curso>_s<NN>.json      (curso ∈ proyecto1|investigacion|
                                                       creatividad|tg2|tg3 · NN con cero: s03)

El JSON es una **lista** de bloques; cada bloque = una slide. Tipos válidos:

  1) {"type": "bullets", "title": "…", "bullets": ["línea", "  sub-línea"], "note": "opcional"}
  2) {"type": "table",   "title": "…", "headers": ["A","B"], "rows": [["a1","b1"]],
      "note": "opcional", "col_w": [3.0, 6.0]}
  3) {"type": "boxes",   "title": "…", "boxes": [["info","…"],["aclaracion","…"],
                                                 ["advertencia","…"]]}

MARKUP: solo ``**negrita**`` (el motor CUN la interpreta). Sin @@…@@, sin cursivas, sin HTML.
SUB-VIÑETAS: dos espacios al inicio de la cadena → se renderizan como segundo nivel (●).

API pública
-----------
    CONTENT_DIR                      ruta de config/slides/content
    content_path(course_key, n)      ruta canónica del JSON de esa sesión
    has_content(course_key, n)       bool
    load(course_key, n)              -> list[dict] | None  (None si no existe / vacío / inválido)
    render(prs, blocks, start_idx=2) -> int  (siguiente índice de slide libre)

`render()` numera las slides consecutivamente desde `start_idx`, parte las tablas largas
(máx. 8 filas por slide) y los bloques de viñetas largos (máx. 9 viñetas por slide) añadiendo
« (cont.) » al título, y ajusta el cuerpo de fuente para que el contenido no se desborde.

CLI de validación:
    python cun_contenido_sesion.py proyecto1 3      → valida y resume los bloques
    python cun_contenido_sesion.py --all            → valida todos los JSON cun_*
"""
from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cun_slides_engine as eng
from cun_slides_engine import box_note_slide, content_slide, table_content

SLIDES_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(SLIDES_DIR, "content")
PREFIX = "cun_"

COURSE_KEYS = ("proyecto1", "investigacion", "creatividad", "tg2", "tg3")

# --- Límites de partición (evitan desbordes en la proyección) ---
MAX_ROWS_PER_TABLE = 8      # filas de datos por slide (sin contar el encabezado)
MAX_BULLETS_PER_SLIDE = 9   # viñetas (nivel 0 + sub-viñetas) por slide
MAX_BOXES_PER_SLIDE = 4     # cajas de color por slide
CONT_SUFFIX = " (cont.)"

# --- Ajuste tipográfico ---
BULLET_SIZE_MAX = 16
BULLET_SIZE_MIN = 12
NOTE_SIZE = 12
NOTE_RESERVE_IN = 0.55      # alto reservado abajo cuando el bloque trae "note"


# ---------------------------------------------------------------- carga
def content_path(course_key: str, n: int) -> str:
    """Ruta canónica: config/slides/content/cun_<curso>_s<NN>.json (NN con cero)."""
    return os.path.join(CONTENT_DIR, f"{PREFIX}{course_key}_s{int(n):02d}.json")


def _candidate_paths(course_key: str, n: int):
    yield content_path(course_key, n)
    # tolerancia: nombre sin cero a la izquierda (s3) por si alguien lo crea así
    alt = os.path.join(CONTENT_DIR, f"{PREFIX}{course_key}_s{int(n)}.json")
    if alt != content_path(course_key, n):
        yield alt


def has_content(course_key: str, n: int) -> bool:
    return any(os.path.isfile(p) for p in _candidate_paths(course_key, n))


def load(course_key: str, n: int):
    """Devuelve la lista de bloques de la sesión, o None si no hay contenido usable.

    Nunca lanza: un JSON roto se reporta por stderr y se trata como «sin contenido»
    (la deck cae al comportamiento genérico de siempre).
    """
    path = next((p for p in _candidate_paths(course_key, n) if os.path.isfile(p)), None)
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:  # JSON inválido → fallback silencioso pero avisado
        print(f"WARN contenido inválido {os.path.basename(path)}: {exc}", file=sys.stderr)
        return None
    if isinstance(data, dict):
        data = data.get("blocks") or data.get("slides") or data.get("bloques")
    if not isinstance(data, list):
        print(f"WARN {os.path.basename(path)}: se esperaba una lista de bloques", file=sys.stderr)
        return None
    blocks = [b for b in data if isinstance(b, dict) and _block_type(b)]
    return blocks or None


def _block_type(blk: dict) -> str | None:
    """Tipo del bloque; si falta `type`, se infiere por las llaves presentes."""
    t = (blk.get("type") or "").strip().lower()
    if t in ("bullets", "table", "boxes"):
        return t
    if blk.get("headers") and blk.get("rows"):
        return "table"
    if blk.get("boxes"):
        return "boxes"
    if blk.get("bullets"):
        return "bullets"
    return None


# ---------------------------------------------------------------- utilidades
def _txt(v) -> str:
    return v if isinstance(v, str) else ("" if v is None else str(v))


def _items(raw_bullets):
    """['texto', '  sub'] → [('texto', 0), ('sub', 1)] (2 espacios = segundo nivel)."""
    out = []
    for b in raw_bullets or []:
        if isinstance(b, (list, tuple)) and len(b) == 2:      # ("texto", nivel) ya explícito
            text, lvl = _txt(b[0]).strip(), int(b[1] or 0)
        else:
            s = _txt(b)
            if not s.strip():
                continue
            lvl = 1 if (len(s) - len(s.lstrip(" "))) >= 2 else 0
            text = s.strip()
        if text:
            out.append((text, min(lvl, 1)))
    return out


def _plain_len(text: str) -> int:
    """Longitud visible: los delimitadores ** no ocupan ancho al proyectar."""
    return len(text.replace("**", ""))


def _bullets_height(items, size, width=eng.CONTENT_W) -> float:
    """Alto estimado (pulgadas) del bloque de viñetas a ese cuerpo de fuente."""
    total = 0.0
    for text, lvl in items:
        w = width - (0.45 if lvl else 0.0)
        cpl = max(8, int(w / (size * 0.48 / 72.0)))
        lines = max(1, math.ceil((_plain_len(text) + 4) / cpl))
        total += lines * (size * 1.22 / 72.0) + (10 if lvl == 0 else 6) / 72.0
    return total


def _fit_bullet_size(items, avail_in: float) -> int:
    size = BULLET_SIZE_MAX
    while size > BULLET_SIZE_MIN and _bullets_height(items, size) > avail_in:
        size -= 1
    return size


def _avail_for_bullets(sub, note) -> float:
    top = (2.05 if sub else 1.7) + 0.15          # igual que content_slide/title_block
    avail = eng.SH - top - 0.6
    if note:
        avail -= NOTE_RESERVE_IN
    return avail


def _split_at_level0(items, limit):
    """Corta `items` en trozos de ≤ limit sin separar una sub-viñeta de su viñeta madre."""
    chunks, i, n = [], 0, len(items)
    while i < n:
        end = min(i + limit, n)
        if end < n:
            back = end
            while back > i + 1 and items[back][1] != 0:
                back -= 1
            if back > i + 1:
                end = back
        chunks.append(items[i:end])
        i = end
    return chunks


def _cont_title(title: str, part: int) -> str:
    return title if part == 0 else f"{title}{CONT_SUFFIX}"


def _note_line(slide, note: str) -> None:
    """Línea inferior en cursiva (mismo look que la `note` de table_content)."""
    tf = eng.textbox(slide, eng.MARGIN, eng.SH - 1.0, eng.CONTENT_W - 1.0, 0.5)
    eng._rich(tf.paragraphs[0], note, NOTE_SIZE, eng.GRAY, italic=True)


# ---------------------------------------------------------------- render por tipo
def _render_bullets(prs, blk, idx) -> int:
    title = _txt(blk.get("title")).strip() or "CONTENIDO"
    sub = _txt(blk.get("sub")).strip() or None
    note = _txt(blk.get("note")).strip() or None
    items = _items(blk.get("bullets"))
    if not items:
        return idx

    avail = _avail_for_bullets(sub, note)
    chunks = _split_at_level0(items, MAX_BULLETS_PER_SLIDE)
    # Si aún al cuerpo mínimo no cabe, seguir partiendo (máx. 4 pasadas).
    for _ in range(3):
        if all(_bullets_height(c, BULLET_SIZE_MIN) <= avail for c in chunks):
            break
        nuevos = []
        for c in chunks:
            if _bullets_height(c, BULLET_SIZE_MIN) > avail and len(c) > 2:
                nuevos.extend(_split_at_level0(c, max(2, (len(c) + 1) // 2)))
            else:
                nuevos.append(c)
        chunks = nuevos

    for i, chunk in enumerate(chunks):
        size = _fit_bullet_size(chunk, avail)
        s = content_slide(prs, _cont_title(title, i), chunk, sub=sub, size=size, idx=idx)
        if note and i == len(chunks) - 1:
            _note_line(s, note)
        idx += 1
    return idx


def _table_font(rows) -> int:
    maxlen = 0
    for r in rows:
        for c in r:
            maxlen = max(maxlen, _plain_len(_txt(c)))
    if len(rows) > 6 or maxlen > 95:
        return 11
    if len(rows) > 7 and maxlen > 115:
        return 10
    return 12


def _render_table(prs, blk, idx) -> int:
    title = _txt(blk.get("title")).strip() or "TABLA"
    headers = [_txt(h) for h in (blk.get("headers") or [])]
    rows = [[_txt(c) for c in r] for r in (blk.get("rows") or []) if isinstance(r, (list, tuple))]
    if not headers or not rows:
        return idx
    ncol = len(headers)
    rows = [(r + [""] * ncol)[:ncol] for r in rows]     # normaliza nº de columnas
    sub = _txt(blk.get("sub")).strip() or None
    note = _txt(blk.get("note")).strip() or None
    col_w = blk.get("col_w") if isinstance(blk.get("col_w"), list) else None
    if col_w and len(col_w) != ncol:
        col_w = None

    parts = [rows[i:i + MAX_ROWS_PER_TABLE] for i in range(0, len(rows), MAX_ROWS_PER_TABLE)]
    for i, chunk in enumerate(parts):
        table_content(
            prs, _cont_title(title, i), headers, chunk,
            sub=sub, note=note if i == len(parts) - 1 else None,
            col_w=col_w, idx=idx, fs_body=_table_font(chunk),
        )
        idx += 1
    return idx


def _box_pairs(raw):
    out = []
    for b in raw or []:
        if isinstance(b, dict):
            tipo = _txt(b.get("tipo") or b.get("type") or "info").strip().lower()
            texto = _txt(b.get("texto") or b.get("text") or b.get("body")).strip()
        elif isinstance(b, (list, tuple)) and len(b) >= 2:
            tipo, texto = _txt(b[0]).strip().lower(), _txt(b[1]).strip()
        else:
            continue
        if not texto:
            continue
        if tipo not in eng._BOX_COLORS:
            tipo = "info"
        out.append((tipo, texto))
    return out


def _box_height(texto: str) -> float:
    return 0.5 + 0.28 * max(1, (_plain_len(texto) // 90) + 1) + 0.25   # + separación


def _render_boxes(prs, blk, idx) -> int:
    title = _txt(blk.get("title")).strip() or "PARA TENER EN CUENTA"
    sub = _txt(blk.get("sub")).strip() or None
    boxes = _box_pairs(blk.get("boxes"))
    if not boxes:
        return idx
    avail = eng.SH - ((2.05 if sub else 1.7) + 0.2) - 0.5

    chunks, cur, acc = [], [], 0.0
    for tipo, texto in boxes:
        h = _box_height(texto)
        if cur and (len(cur) >= MAX_BOXES_PER_SLIDE or acc + h > avail):
            chunks.append(cur)
            cur, acc = [], 0.0
        cur.append((tipo, texto))
        acc += h
    if cur:
        chunks.append(cur)

    for i, chunk in enumerate(chunks):
        box_note_slide(prs, _cont_title(title, i), chunk, sub=sub, idx=idx)
        idx += 1
    return idx


_RENDERERS = {"bullets": _render_bullets, "table": _render_table, "boxes": _render_boxes}


# ---------------------------------------------------------------- API principal
def render(prs, blocks, start_idx: int = 2) -> int:
    """Renderiza los bloques sobre `prs` numerando desde `start_idx`.

    Devuelve el **siguiente índice libre** (útil para seguir añadiendo slides).
    """
    idx = int(start_idx)
    for blk in blocks or []:
        if not isinstance(blk, dict):
            continue
        fn = _RENDERERS.get(_block_type(blk) or "")
        if fn:
            idx = fn(prs, blk, idx)
    return idx


# ---------------------------------------------------------------- CLI de validación
def _describe(course_key: str, n: int) -> bool:
    blocks = load(course_key, n)
    path = content_path(course_key, n)
    if not blocks:
        print(f"— {os.path.basename(path)}: sin contenido rico")
        return False
    tipos = {}
    for b in blocks:
        t = _block_type(b) or "?"
        tipos[t] = tipos.get(t, 0) + 1
    resumen = " · ".join(f"{k}×{v}" for k, v in sorted(tipos.items()))
    print(f"OK {os.path.basename(path)}: {len(blocks)} bloques ({resumen})")
    for b in blocks:
        print(f"   [{_block_type(b)}] {_txt(b.get('title'))[:70]}")
    return True


def _main(argv):
    args = argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == "--all":
        import glob
        import re as _re
        ok = True
        for p in sorted(glob.glob(os.path.join(CONTENT_DIR, f"{PREFIX}*_s*.json"))):
            m = _re.match(rf"{PREFIX}(.+)_s(\d+)\.json$", os.path.basename(p))
            if m:
                ok = _describe(m.group(1), int(m.group(2))) and ok
        if not ok:
            sys.exit(1)
        return
    if len(args) < 2:
        print(__doc__)
        return
    if not _describe(args[0], int(args[1])):
        sys.exit(1)


if __name__ == "__main__":
    _main(sys.argv)
