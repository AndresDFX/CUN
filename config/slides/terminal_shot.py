# -*- coding: utf-8 -*-
"""
Genera "pantallazos" de TERMINAL LINUX (PNG) con comandos y su salida EXACTOS,
para incrustar en los guiones docentes (aspecto de terminal en línea).

No captura un navegador: dibuja una terminal fiel con Pillow (monoespaciada, tema oscuro),
con el prompt, los comandos y la salida reales. Es reproducible y legible; el docente
puede replicar lo mismo en la terminal Linux en línea (DistroSea/Webminal/Copy.sh).

Spec por imagen:
    {
      "id": "servidor_s1_pwd_ls",
      "title": "pwd y ls -la",                 # va en la barra de la ventana
      "prompt": "julian@servidor:~$",
      "lines": [
         {"t": "cmd", "text": "pwd"},
         {"t": "out", "text": "/home/julian"},
         {"t": "cmd", "text": "ls -la"},
         {"t": "out", "text": "-rw-r----- 1 julian ...", "hl": true},   # hl = resaltar
         {"t": "comment", "text": "# ..."}
      ]
    }

Uso:
    from terminal_shot import render_terminal, render_many
    render_terminal(spec, "salida.png")
    render_many([spec1, spec2, ...], "carpeta/destino")   # escribe <id>.png
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

# Tema de terminal (oscuro) + acento de marca FESNA para resaltar
BG      = (0x1E, 0x1E, 0x1E)
TITLEBG = (0x32, 0x32, 0x33)
FG      = (0xE6, 0xE6, 0xE6)   # texto de comando
OUT     = (0xC8, 0xC8, 0xC8)   # salida
DIM     = (0x8A, 0x8A, 0x8A)   # comentarios
USER    = (0x33, 0xD0, 0x79)   # usuario@host (verde)
PATH    = (0x4A, 0x9E, 0xEE)   # ruta (azul)
HL      = (0xFD, 0x8A, 0x53)   # resaltado (naranja de marca, claro para fondo oscuro)
WHITE   = (0xFF, 0xFF, 0xFF)
DOTS    = [(0xFF, 0x5F, 0x56), (0xFF, 0xBD, 0x2E), (0x27, 0xC9, 0x3F)]

SS = 2
_FONT_DIRS = [r"C:\Windows\Fonts", os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Fonts")]
_MONO = ["consola.ttf", "CascadiaMono.ttf", "CascadiaCode.ttf", "cour.ttf"]
_MONO_B = ["consolab.ttf", "CascadiaMono-Bold.ttf", "courbd.ttf"]
_CACHE = {}

def _font(px, bold=False):
    key = (px, bold)
    if key in _CACHE:
        return _CACHE[key]
    names = _MONO_B if bold else _MONO
    path = None
    for n in names:
        for d in _FONT_DIRS:
            p = os.path.join(d, n)
            if os.path.exists(p):
                path = p; break
        if path:
            break
    try:
        f = ImageFont.truetype(path, px) if path else ImageFont.load_default()
    except Exception:
        f = ImageFont.load_default()
    _CACHE[key] = f
    return f


_MEAS = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def _wrap(text, fnt, maxw):
    """Wrap por caracteres (fuente monoespaciada)."""
    if not text:
        return [""]
    cw = _MEAS.textlength("M", font=fnt) or 1
    n = max(10, int(maxw / cw))
    out = []
    while len(text) > n:
        out.append(text[:n]); text = text[n:]
    out.append(text)
    return out


def render_terminal(spec, out_path):
    W = spec.get("width", 1120)
    fs = spec.get("font", 25)
    pad = 26
    title_h = 46
    lh = int(fs * 1.42)
    fnt = _font(fs * SS); fntb = _font(fs * SS, bold=True)
    prompt = spec.get("prompt", "user@servidor:~$")
    maxw = (W - 2 * pad) * SS

    # Expandir líneas (prompt+cmd, con wrap) para calcular alto
    rows = []  # (kind, text, hl)  kind: cmd/out/comment/blank
    for ln in spec.get("lines", []):
        t = ln.get("t", "out"); txt = ln.get("text", ""); hl = ln.get("hl", False)
        if t == "cmd":
            full = prompt + " " + txt
            wrapped = _wrap(full, fntb, maxw)
            for i, w in enumerate(wrapped):
                rows.append(("cmd" if i == 0 else "cmdcont", w, hl))
        elif t == "blank" or txt == "":
            rows.append(("blank", "", False))
        else:
            for w in _wrap(txt, fnt, maxw):
                rows.append((t, w, hl))

    body_h = pad * 2 + max(1, len(rows)) * lh
    H = title_h + body_h
    img = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)

    # Barra de título
    d.rectangle([0, 0, W * SS, title_h * SS], fill=TITLEBG)
    for i, c in enumerate(DOTS):
        cx = (pad + i * 26) * SS; cy = (title_h // 2) * SS; r = 8 * SS
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    ttl = spec.get("title", "")
    env = spec.get("env", "Terminal Linux en línea")   # etiqueta de la barra (p. ej. "Consola JavaScript · examlab")
    label = (env + " — " + ttl) if ttl else env
    if label:
        d.text(((W // 2) * SS, (title_h // 2) * SS), label,
               font=_font(int(fs * 0.82) * SS), fill=(0xD0, 0xD0, 0xD0), anchor="mm")

    # Cuerpo
    y = title_h + pad
    x = pad
    for kind, text, hl in rows:
        if kind == "blank":
            y += lh; continue
        if kind == "cmd":
            # prompt coloreado (usuario@host en verde, ruta:$ en azul) + comando en blanco
            rest = text
            if rest.startswith(prompt):
                # dividir prompt en "user@host" ":path$"
                p = prompt
                col = p.find(":")
                userpart = p[:col] if col > 0 else p
                pathpart = p[col:] if col > 0 else ""
                cx = x * SS
                d.text((cx, y * SS), userpart, font=fntb, fill=USER, anchor="la")
                cx += _MEAS.textlength(userpart, font=fntb)
                if pathpart:
                    d.text((cx, y * SS), pathpart, font=fntb, fill=PATH, anchor="la")
                    cx += _MEAS.textlength(pathpart, font=fntb)
                cmd = rest[len(prompt):]
                d.text((cx, y * SS), cmd, font=fntb, fill=WHITE, anchor="la")
            else:
                d.text((x * SS, y * SS), rest, font=fntb, fill=WHITE, anchor="la")
        elif kind == "cmdcont":
            d.text((x * SS, y * SS), text, font=fntb, fill=WHITE, anchor="la")
        elif kind == "comment":
            d.text((x * SS, y * SS), text, font=fnt, fill=DIM, anchor="la")
        else:  # out
            d.text((x * SS, y * SS), text, font=fnt, fill=(HL if hl else OUT), anchor="la")
        y += lh

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img.resize((W, H), Image.LANCZOS).save(out_path, "PNG")
    return out_path


def render_many(specs, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    done = []
    for sp in specs:
        p = os.path.join(dest_dir, sp["id"] + ".png")
        render_terminal(sp, p)
        done.append(p)
    return done


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    demo = {
        "id": "demo", "title": "pwd y ls -la", "prompt": "julian@servidor:~$",
        "lines": [
            {"t": "cmd", "text": "pwd"},
            {"t": "out", "text": "/home/julian"},
            {"t": "cmd", "text": "ls -la"},
            {"t": "out", "text": "total 16"},
            {"t": "out", "text": "drwxr-xr-x 2 julian julian 4096 jul 14 09:12 ."},
            {"t": "out", "text": "drwxr-xr-x 4 root   root   4096 jul 14 09:10 .."},
            {"t": "out", "text": "-rw-r----- 1 julian desarrollo 128 jul 14 09:12 deploy.sh", "hl": True},
        ],
    }
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "diagramas", "_demo_term.png")
    render_terminal(demo, out)
    print("OK", out)
