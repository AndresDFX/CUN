# -*- coding: utf-8 -*-
"""
Genera DIAGRAMAS DE CONCEPTO (PNG) con la identidad FESNA/Nueva América para
incrustar en las diapositivas (algunas slides son solo texto; otras, imagen+texto).

No usa matplotlib (no está disponible): dibuja con Pillow a 2x y reescala (LANCZOS)
para bordes suaves. Los diagramas NO llevan título dentro (el título va en la banda
gris de la diapositiva); solo dibujan el esquema.

Uso:
    python diagramas.py            # renderiza TODO el catálogo a assets/diagramas/<id>.png
    from diagramas import path_for, render_all
    render_all(); p = path_for("handshake")
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

# ---------------- Paleta oficial ----------------
ORANGE = (0xFD, 0x53, 0x1E)
BLUE   = (0x0A, 0x49, 0x9C)
GRAY   = (0x4A, 0x4A, 0x49)
DARK   = (0x1A, 0x1C, 0x1D)
BANNER = (0xF0, 0xF1, 0xF2)   # relleno claro de cajas neutras
BORDER = (0xC4, 0xC7, 0xCA)   # borde de caja neutra
SOFT   = (0x8F, 0x98, 0x9D)   # gris medio (subtítulos / notas)
TINT   = (0xFF, 0xE6, 0xDD)   # naranja muy claro (caja resaltada suave)
TINTB  = (0xE7, 0xEF, 0xF8)   # azul muy claro
ARROW  = (0x8F, 0x98, 0x9D)
WHITE  = (0xFF, 0xFF, 0xFF)

SS = 2  # supersampling
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "assets", "diagramas")

# ---------------- Fuentes ----------------
_FONT_DIRS = [
    r"C:\Windows\Fonts",
    os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Fonts"),
]
_REG = ["Barlow-Regular.ttf", "Barlow-Medium.ttf", "segoeui.ttf", "arial.ttf"]
_BLD = ["Barlow-Bold.ttf", "Barlow-SemiBold.ttf", "segoeuib.ttf", "arialbd.ttf"]
_SEMI = ["Barlow-SemiBold.ttf", "Barlow-Medium.ttf", "seguisb.ttf", "segoeuib.ttf", "arialbd.ttf"]
_MONO = ["consola.ttf", "CascadiaMono.ttf", "cour.ttf"]
_CACHE = {}

def _find(names):
    for n in names:
        for d in _FONT_DIRS:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None

def font(px, weight="reg"):
    px = int(px)
    key = (px, weight)
    if key in _CACHE:
        return _CACHE[key]
    table = {"reg": _REG, "bold": _BLD, "semi": _SEMI, "mono": _MONO}
    path = _find(table.get(weight, _REG))
    try:
        f = ImageFont.truetype(path, px) if path else ImageFont.load_default()
    except Exception:
        f = ImageFont.load_default()
    _CACHE[key] = f
    return f

# ---------------- Lienzo ----------------
class C:
    def __init__(self, w, h, bg=WHITE):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w * SS, h * SS), bg)
        self.d = ImageDraw.Draw(self.img)

    def rrect(self, x, y, w, h, r, fill=None, outline=None, width=2):
        r = max(0, min(r, min(w, h) / 2))
        self.d.rounded_rectangle([x*SS, y*SS, (x+w)*SS, (y+h)*SS], radius=r*SS,
                                 fill=fill, outline=outline, width=max(1, int(width*SS)))

    def line(self, x1, y1, x2, y2, color=ARROW, width=3):
        self.d.line([x1*SS, y1*SS, x2*SS, y2*SS], fill=color, width=max(1, int(width*SS)))

    def poly(self, pts, fill):
        self.d.polygon([(px*SS, py*SS) for px, py in pts], fill=fill)

    def text(self, x, y, s, size, color, weight="reg", anchor="mm"):
        self.d.text((x*SS, y*SS), s, font=font(size, weight), fill=color, anchor=anchor)

    def tw(self, s, size, weight="reg"):
        return self.d.textlength(s, font=font(size, weight)) / SS

    def wrap(self, s, size, weight, maxw):
        words = s.split()
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if self.tw(t, size, weight) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur); cur = w
        if cur:
            lines.append(cur)
        return lines

    def textblock(self, x, y, s, size, color, weight, maxw, lh, anchor="la"):
        lines = self.wrap(s, size, weight, maxw)
        for i, ln in enumerate(lines):
            self.text(x, y + i*lh, ln, size, color, weight, anchor=anchor)
        return len(lines) * lh

    def arrow_down(self, x, y1, y2, color=ARROW, width=4, head=13):
        self.line(x, y1, x, y2 - head + 2, color, width)
        self.poly([(x-head, y2-head), (x+head, y2-head), (x, y2)], color)

    def arrow_right(self, x1, x2, y, color=ARROW, width=4, head=13):
        self.line(x1, y, x2 - head + 2, y, color, width)
        self.poly([(x2-head, y-head), (x2-head, y+head), (x2, y)], color)

    def arrow_left(self, x1, x2, y, color=ARROW, width=4, head=13):
        self.line(x1, y, x2 + head - 2, y, color, width)
        self.poly([(x2+head, y-head), (x2+head, y+head), (x2, y)], color)

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.img.resize((self.w, self.h), Image.LANCZOS).save(path, "PNG")


_MEAS = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def _measure_lines(s, size, weight, maxw):
    """Nº de líneas tras el wrap, igual que Canvas.wrap (para dimensionar antes de dibujar)."""
    words = s.split(); lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if (_MEAS.textlength(t, font=font(size, weight)) / SS) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return max(1, len(lines))


def _boxstyle(kind):
    """(fill, textcolor, subcolor, outline)"""
    if kind == "orange":
        return ORANGE, WHITE, (255, 224, 214), None
    if kind == "blue":
        return BLUE, WHITE, (210, 224, 244), None
    if kind == "tint":
        return TINT, DARK, GRAY, ORANGE
    if kind == "tintb":
        return TINTB, DARK, GRAY, BLUE
    return BANNER, DARK, GRAY, BORDER


# ==================== RENDERERS ====================
def r_vflow(data, out):
    nodes = data["nodes"]; cap = data.get("caption")
    n = len(nodes)
    bw = data.get("bw", 820); bh = data.get("bh", 132); gap = 54
    top = 46; W = 1200
    H = top + n*bh + (n-1)*gap + (100 if cap else 44)
    c = C(W, H)
    x = (W - bw) / 2
    y = top
    for i, nd in enumerate(nodes):
        fill, tc, sc, ol = _boxstyle(nd.get("c", "neutral"))
        c.rrect(x, y, bw, bh, 20, fill=fill, outline=ol, width=3)
        cy = y + bh/2
        if nd.get("s"):
            c.text(x + bw/2, cy - 20, nd["t"], 37, tc, "bold")
            c.textblock(x + bw/2, cy + 16, nd["s"], 25, sc, "reg", bw-70, 30, anchor="ma")
        else:
            c.text(x + bw/2, cy, nd["t"], 37, tc, "bold")
        if i < n-1:
            c.arrow_down(W/2, y+bh, y+bh+gap)
        y += bh + gap
    if cap:
        c.textblock(W/2, y + 6, cap, 26, GRAY, "semi", W-160, 34, anchor="ma")
    c.save(out)


def r_stack(data, out):
    layers = data["layers"]; note = data.get("note"); bidir = data.get("bidir")
    n = len(layers); W = 1200
    lw = 800; lh = 116; top = 50
    x = (W - lw) / 2 - (40 if bidir else 0)
    H = top + n*lh + (110 if note else 46)
    c = C(W, H)
    y = top
    for i, ly in enumerate(layers):
        fill, tc, sc, ol = _boxstyle(ly.get("c", "neutral"))
        c.rrect(x, y, lw, lh, 6, fill=fill, outline=ol or BORDER, width=2)
        # chip de índice a la izquierda
        c.rrect(x, y, 14, lh, 0, fill=ORANGE)
        tx = x + 40
        c.text(tx, y + lh/2 - (16 if ly.get("s") else 0), ly["t"], 32, tc, "bold", anchor="lm")
        if ly.get("s"):
            c.text(tx, y + lh/2 + 22, ly["s"], 24, sc, "reg", anchor="lm")
        y += lh
    if bidir:
        ax = x + lw + 44
        c.arrow_down(ax, top+6, y-6); c.text(ax+26, (top+y)/2, "encapsula ↓", 22, GRAY, "semi", anchor="lm")
    if note:
        c.textblock(W/2, y + 14, note, 25, GRAY, "semi", W-150, 33, anchor="ma")
    c.save(out)


def r_dualstack(data, out):
    L, R = data["left"], data["right"]
    W = 1200; top = 120; colw = 500; gap = 60
    xL = (W - 2*colw - gap) / 2; xR = xL + colw + gap
    nmax = max(len(L["items"]), len(R["items"]))
    barea = 720;
    H = top + barea + 70
    c = C(W, H)
    c.text(xL + colw/2, 60, L["title"], 34, DARK, "bold")
    c.text(xR + colw/2, 60, R["title"], 34, BLUE, "bold")
    def col(x, items):
        lh = min(120, (barea - (len(items)-1)*10) / len(items))
        y = top
        for it in items:
            fill, tc, sc, ol = _boxstyle(it.get("c", "neutral"))
            c.rrect(x, y, colw, lh, 6, fill=fill, outline=ol or BORDER, width=2)
            c.text(x + colw/2, y + lh/2, it["t"], 28, tc, "semi")
            y += lh + 10
    col(xL, L["items"]); col(xR, R["items"])
    if data.get("caption"):
        c.textblock(W/2, top + barea + 6, data["caption"], 25, GRAY, "semi", W-150, 33, anchor="ma")
    c.save(out)


def r_sequence(data, out):
    msgs = data["msgs"]; cap = data.get("caption")
    W = 1000; xL = 265; xR = 735; htop = 46; hh = 116
    n = len(msgs); step = 150; start = htop + hh + 78
    H = start + n*step + (96 if cap else 34)
    c = C(W, H)
    for x, name, col in ((xL, data["left"], "blue"), (xR, data["right"], "orange")):
        fill, tc, sc, ol = _boxstyle(col)
        c.rrect(x-155, htop, 310, hh, 18, fill=fill, outline=ol, width=3)
        c.text(x, htop+hh/2, name, 30, tc, "bold")
        c.line(x, htop+hh, x, H - (96 if cap else 34) - 6, BORDER, 3)
    y = start
    for m in msgs:
        lab = (f"{m['n']}. " if m.get("n") else "") + m["t"]
        c.text((xL+xR)/2, y - 30, lab, 26, DARK, "semi")
        if m["dir"] == "LR":
            c.arrow_right(xL, xR, y, ORANGE, 4)
        else:
            c.arrow_left(xR, xL, y, BLUE, 4)
        y += step
    if cap:
        c.textblock(W/2, y - step + 60, cap, 25, GRAY, "semi", W-150, 33, anchor="ma")
    c.save(out)


def r_tree(data, out):
    root = data["root"]; kids = data["children"]; cap = data.get("caption")
    W = 1100; top = 54; rbw = 400; rbh = 132
    ky = top + rbh + 86; kh = 128
    maxgc = max((len(k.get("children", [])) for k in kids), default=0)
    gc_area = (54 + maxgc * 80) if maxgc else 0
    deepest = ky + kh + gc_area
    H = deepest + (92 if cap else 28)
    c = C(W, H)
    rx = (W - rbw)/2
    fill, tc, sc, ol = _boxstyle(root.get("c", "orange"))
    c.rrect(rx, top, rbw, rbh, 20, fill=fill, outline=ol, width=3)
    c.text(W/2, top+rbh/2 - (18 if root.get("s") else 0), root["t"], 40, tc, "bold")
    if root.get("s"):
        c.text(W/2, top+rbh/2+24, root["s"], 27, sc, "reg")
    n = len(kids); slot = (W - 100) / n; kbw = min(322, slot - 22)
    busx = W/2
    for i, k in enumerate(kids):
        kx = 50 + slot*i + (slot - kbw)/2
        kcx = kx + kbw/2
        if n > 1:
            c.line(busx, top+rbh, kcx, ky - 36, BORDER, 3)
            c.line(kcx, ky-36, kcx, ky, BORDER, 3)
        else:
            c.arrow_down(kcx, ky-36, ky)
        fill, tc, sc, ol = _boxstyle(k.get("c", "neutral"))
        c.rrect(kx, ky, kbw, kh, 18, fill=fill, outline=ol or BORDER, width=2)
        c.text(kcx, ky+kh/2 - (16 if k.get("s") else 0), k["t"], 35, tc, "semi")
        if k.get("s"):
            c.text(kcx, ky+kh/2+24, k["s"], 26, sc, "reg")
        if k.get("children"):
            gy = ky + kh + 54
            for j, g in enumerate(k["children"]):
                gyy = gy + j*80
                c.line(kcx, ky+kh, kcx, gyy+32, BORDER, 3)
                c.rrect(kx+34, gyy, kbw-34, 64, 14, fill=BANNER, outline=BORDER, width=2)
                c.text(kx+34+(kbw-34)/2, gyy+32, g, 29, DARK, "semi")
    if cap:
        c.textblock(W/2, deepest + 26, cap, 27, GRAY, "semi", W-140, 36, anchor="ma")
    c.save(out)


def r_bar(data, out):
    segs = data["segments"]; cap = data.get("caption"); topl = data.get("top_label")
    W = 1140; x0 = 90; x1 = 1050; bh = 250
    ytop = 90 + (86 if topl else 0)
    H = ytop + bh + 176 + (54 if cap else 0)
    c = C(W, H)
    if topl:
        c.text(W/2, 82, topl, 52, DARK, "bold" if not data.get("mono") else "mono")
    total = sum(s["frac"] for s in segs)
    x = x0
    for s in segs:
        w = (x1 - x0) * s["frac"] / total
        fill, tc, sc, ol = _boxstyle(s.get("c", "neutral"))
        c.rrect(x, ytop, w, bh, 10, fill=fill, outline=ol or BORDER, width=2)
        c.text(x + w/2, ytop + bh/2, s["t"], 34, tc, "bold")
        if s.get("s"):
            c.text(x + w/2, ytop + bh + 42, s["s"], 30, GRAY, "semi")
        x += w
    if cap:
        c.textblock(W/2, ytop + bh + 108, cap, 29, GRAY, "semi", W-140, 38, anchor="ma")
    c.save(out)


def r_nested(data, out):
    layers = data["layers"]  # de fuera hacia dentro
    W = 1200; H = 760; c = C(W, H)
    n = len(layers)
    x, y = 90, 70
    w, h = W - 180, H - 150
    inset_x, inset_y = 70, 74
    for i, ly in enumerate(layers):
        fill, tc, sc, ol = _boxstyle(ly.get("c", "neutral"))
        c.rrect(x, y, w, h, 16, fill=fill, outline=ol or BORDER, width=3)
        c.text(x + 20, y + 26, ly["t"], 27, tc, "bold", anchor="lm")
        x += inset_x; y += inset_y; w -= 2*inset_x; h -= 2*inset_y
    if data.get("caption"):
        c.textblock(W/2, H - 66, data["caption"], 25, GRAY, "semi", W-150, 33, anchor="ma")
    c.save(out)


def r_compare(data, out):
    L, R = data["left"], data["right"]; W = 1200
    pw = 520; gap = 60; top = 50
    xL = (W - 2*pw - gap)/2; xR = xL + pw + gap
    def panel_h(P):
        y = 118
        for it in P["items"]:
            nlines = _measure_lines(it, 25, "reg", pw - 100)
            y += max(44, nlines*33 + 16)
        return y + 26
    ph = max(panel_h(L), panel_h(R))
    H = top + ph + (80 if data.get("caption") else 30)
    c = C(W, H)
    for x, P in ((xL, L), (xR, R)):
        col = P.get("c", "blue")
        fill, tc, _, _ = _boxstyle(col)
        c.rrect(x, top, pw, ph, 18, fill=WHITE, outline=fill, width=3)
        c.rrect(x, top, pw, 78, 18, fill=fill)
        c.rrect(x, top+40, pw, 40, 0, fill=fill)
        c.text(x + pw/2, top + 40, P["title"], 30, tc, "bold")
        y = top + 118
        for it in P["items"]:
            c.text(x + 34, y, "•", 27, ORANGE, "bold", anchor="lm")
            used = c.textblock(x + 66, y - 14, it, 25, GRAY, "reg", pw - 100, 33, anchor="la")
            y += max(44, used + 16)
    if data.get("caption"):
        c.textblock(W/2, top + ph + 12, data["caption"], 25, GRAY, "semi", W-150, 33, anchor="ma")
    c.save(out)


def r_cards(data, out):
    cards = data["cards"]; cols = data.get("cols", len(cards)); cap = data.get("caption")
    W = 1200; rows = (len(cards) + cols - 1)//cols
    mx = 90; gap = 40; top = 60
    cw = (W - 2*mx - (cols-1)*gap)/cols; ch = data.get("ch", 300)
    H = top + rows*ch + (rows-1)*gap + (90 if cap else 40)
    c = C(W, H)
    for i, cd in enumerate(cards):
        r, col = divmod(i, cols)
        x = mx + col*(cw+gap); y = top + r*(ch+gap)
        c.rrect(x, y, cw, ch, 20, fill=WHITE, outline=BORDER, width=3)
        c.rrect(x, y, cw, 12, 0, fill=ORANGE)
        cx = x + cw/2
        yy = y + 46
        if cd.get("big"):
            c.text(cx, yy + 56, cd["big"], 94, ORANGE, "bold"); yy += 150
        c.text(cx, yy + 8, cd["t"], 36, DARK, "bold"); yy += 62
        for ln in cd.get("lines", []):
            used = c.textblock(cx, yy, ln, 27, GRAY, "reg", cw - 56, 34, anchor="ma")
            yy += used + 12
    if cap:
        c.textblock(W/2, H - (90 if cap else 0) + 6, cap, 25, GRAY, "semi", W-150, 33, anchor="ma")
    c.save(out)


def r_blocks(data, out):
    blocks = data["blocks"]; cap = data.get("caption"); topl = data.get("top_label")
    W = 1120; mx = 64; gap = 26; top = 96 + (88 if topl else 0)
    bh = 250
    total = sum(b.get("w", 1) for b in blocks)
    avail = W - 2*mx - (len(blocks)-1)*gap
    H = top + bh + 178 + (52 if cap else 0)
    c = C(W, H)
    if topl:
        c.text(W/2, 84, topl, 56, DARK, "mono")
    x = mx
    for b in blocks:
        w = avail * b.get("w", 1)/total
        fill, tc, sc, ol = _boxstyle(b.get("c", "neutral"))
        c.rrect(x, top, w, bh, 18, fill=fill, outline=ol or BORDER, width=3)
        c.text(x + w/2, top + bh/2, b["t"], b.get("ts", 58), tc, "mono")
        if b.get("cap"):
            c.text(x + w/2, top + bh + 44, b["cap"], 30, GRAY, "semi")
        x += w + gap
    if cap:
        c.textblock(W/2, top + bh + 110, cap, 29, GRAY, "semi", W-140, 38, anchor="ma")
    c.save(out)


# ---------------- Mockups tipo "imagen" (no esquemas): teléfono/UI, código→preview, paleta ----------------
def _phone(c, x, y, w, h, spec):
    """Dibuja un teléfono con una mini-UI dentro (parece captura de una app real)."""
    r = w * 0.12
    c.rrect(x, y, w, h, r, fill=(0x20, 0x22, 0x26), outline=(0x11, 0x12, 0x14), width=3)
    m = w * 0.05
    sx, sy, sw, sh = x + m, y + m * 1.3, w - 2 * m, h - 2 * m * 1.3
    c.rrect(sx, sy, sw, sh, r * 0.55, fill=WHITE)
    nw, nh = w * 0.32, h * 0.022
    c.rrect(x + (w - nw) / 2, y + m * 0.45, nw, nh, nh / 2, fill=(0x11, 0x12, 0x14))
    ab = sh * 0.11
    c.rrect(sx, sy, sw, ab, r * 0.55, fill=ORANGE)
    c.rrect(sx, sy + ab * 0.5, sw, ab * 0.5, 0, fill=ORANGE)
    fs = max(15, int(sw * 0.075))
    c.text(sx + sw * 0.06, sy + ab / 2, spec.get("title", ""), fs, WHITE, "bold", anchor="lm")
    pad = sw * 0.07
    cy = sy + ab + sh * 0.05
    for el in spec.get("screen", []):
        t = el.get("type")
        if t == "text":
            cy += c.textblock(sx + pad, cy, el["t"], fs, DARK, "semi", sw - 2 * pad, fs * 1.35) + sh * 0.03
        elif t == "sub":
            cy += c.textblock(sx + pad, cy, el["t"], int(fs * 0.82), GRAY, "reg", sw - 2 * pad, fs * 1.2) + sh * 0.025
        elif t == "button":
            bh = sh * 0.10; bw = sw - 2 * pad
            c.rrect(sx + pad, cy, bw, bh, bh * 0.3, fill=ORANGE)
            c.text(sx + pad + bw / 2, cy + bh / 2, el["t"], fs, WHITE, "bold", anchor="mm")
            cy += bh + sh * 0.04
        elif t == "field":
            fh = sh * 0.095; bw = sw - 2 * pad
            c.rrect(sx + pad, cy, bw, fh, fh * 0.25, fill=WHITE, outline=BORDER, width=2)
            c.text(sx + pad + fh * 0.35, cy + fh / 2, el["t"], int(fs * 0.9), SOFT, "reg", anchor="lm")
            cy += fh + sh * 0.035
        elif t == "card":
            chh = sh * 0.135; bw = sw - 2 * pad
            c.rrect(sx + pad, cy, bw, chh, chh * 0.16, fill=BANNER, outline=BORDER, width=2)
            c.rrect(sx + pad, cy, chh * 0.16, chh, 0, fill=ORANGE)
            c.text(sx + pad * 1.7, cy + chh * (0.36 if el.get("sub") else 0.5), el["t"], fs, DARK, "bold", anchor="lm")
            if el.get("sub"):
                c.text(sx + pad * 1.7, cy + chh * 0.70, el["sub"], int(fs * 0.8), GRAY, "reg", anchor="lm")
            cy += chh + sh * 0.028
        elif t == "spacer":
            cy += sh * 0.045


def r_phone(data, out):
    W = 560; caph = 84 if data.get("caption") else 34
    H = 1040 + caph
    c = C(W, H)
    _phone(c, 70, 24, W - 140, 1000, data)
    if data.get("caption"):
        c.textblock(W / 2, H - caph + 10, data["caption"], 26, GRAY, "semi", W - 90, 34, anchor="ma")
    c.save(out)


def r_codeui(data, out):
    """Código a la izquierda + el teléfono con el RESULTADO a la derecha (código → preview)."""
    W = 1240; caph = 84 if data.get("caption") else 40
    H = 720 + caph
    c = C(W, H)
    # Caja de código (oscura)
    cx, cy, cw, ch = 60, 40, 700, 660
    c.rrect(cx, cy, cw, ch, 22, fill=(0x1E, 0x20, 0x24))
    for i, dot in enumerate([(0xFF, 0x5F, 0x56), (0xFF, 0xBD, 0x2E), (0x27, 0xC9, 0x3F)]):
        c.d.ellipse([(cx + 34 + i * 34 - 9) * SS, (cy + 30 - 9) * SS,
                     (cx + 34 + i * 34 + 9) * SS, (cy + 30 + 9) * SS], fill=dot)
    ty = cy + 76; lh = 46
    for ln in data.get("code", []):
        col = ORANGE if (ln.strip().startswith("@") or ln.strip().startswith("fun ")) else (0xE8, 0xEA, 0xED)
        c.text(cx + 34, ty, ln, 30, col, "mono", anchor="lm")
        ty += lh
    # Flecha
    c.arrow_right(cx + cw + 6, cx + cw + 74, cy + ch / 2, color=ORANGE, width=6, head=18)
    # Teléfono con el resultado
    _phone(c, cx + cw + 96, 20, 320, 680, data)
    if data.get("caption"):
        c.textblock(W / 2, H - caph + 12, data["caption"], 26, GRAY, "semi", W - 120, 34, anchor="ma")
    c.save(out)


def r_palette(data, out):
    """Muestras de color (swatches) tipo tema Material."""
    sw_list = data["colors"]; cap = data.get("caption")
    W = 1200; mx = 70; gap = 30; top = 60
    n = len(sw_list); cw = (W - 2 * mx - (n - 1) * gap) / n; chh = 300
    H = top + chh + (96 if cap else 46)
    c = C(W, H)
    for i, sc in enumerate(sw_list):
        x = mx + i * (cw + gap)
        hexv = sc["hex"]; rgb = tuple(int(hexv.lstrip("#")[k:k + 2], 16) for k in (0, 2, 4))
        c.rrect(x, top, cw, chh * 0.66, 18, fill=rgb, outline=BORDER, width=2)
        c.text(x + cw / 2, top + chh * 0.82, sc["name"], 30, DARK, "bold")
        c.text(x + cw / 2, top + chh * 0.97, hexv.upper(), 26, GRAY, "mono")
    if cap:
        c.textblock(W / 2, H - 80, cap, 26, GRAY, "semi", W - 120, 34, anchor="ma")
    c.save(out)


def _ui_stack(c, sx, sy, sw, sh, screen, fs):
    """Dibuja una pila de elementos de UI (texto/botón/campo/tarjeta) en un área dada."""
    pad = sw * 0.06
    cy = sy + sh * 0.05
    for el in screen:
        t = el.get("type")
        if t == "text":
            cy += c.textblock(sx + pad, cy, el["t"], fs, DARK, "semi", sw - 2 * pad, fs * 1.35) + sh * 0.03
        elif t == "sub":
            cy += c.textblock(sx + pad, cy, el["t"], int(fs * 0.82), GRAY, "reg", sw - 2 * pad, fs * 1.2) + sh * 0.025
        elif t == "button":
            bh = sh * 0.11; bw = min(sw - 2 * pad, sw * 0.5)
            c.rrect(sx + pad, cy, bw, bh, bh * 0.3, fill=ORANGE)
            c.text(sx + pad + bw / 2, cy + bh / 2, el["t"], fs, WHITE, "bold", anchor="mm")
            cy += bh + sh * 0.04
        elif t == "field":
            fh = sh * 0.10; bw = sw - 2 * pad
            c.rrect(sx + pad, cy, bw, fh, fh * 0.22, fill=WHITE, outline=BORDER, width=2)
            c.text(sx + pad + fh * 0.35, cy + fh / 2, el["t"], int(fs * 0.9), SOFT, "reg", anchor="lm")
            cy += fh + sh * 0.035
        elif t == "card":
            chh = sh * 0.145; bw = sw - 2 * pad
            c.rrect(sx + pad, cy, bw, chh, chh * 0.16, fill=BANNER, outline=BORDER, width=2)
            c.rrect(sx + pad, cy, chh * 0.15, chh, 0, fill=ORANGE)
            c.text(sx + pad * 1.7, cy + chh * (0.36 if el.get("sub") else 0.5), el["t"], fs, DARK, "bold", anchor="lm")
            if el.get("sub"):
                c.text(sx + pad * 1.7, cy + chh * 0.70, el["sub"], int(fs * 0.8), GRAY, "reg", anchor="lm")
            cy += chh + sh * 0.028
        elif t == "spacer":
            cy += sh * 0.045


def _browser(c, x, y, w, h, spec):
    """Ventana de navegador con una mini-UI web dentro (parece captura de una página)."""
    r = 16
    c.rrect(x, y, w, h, r, fill=(0xE9, 0xEB, 0xEE), outline=BORDER, width=2)
    bar = h * 0.09
    c.rrect(x, y, w, bar, r, fill=(0xD6, 0xD9, 0xDE))
    c.rrect(x, y + bar * 0.5, w, bar * 0.5, 0, fill=(0xD6, 0xD9, 0xDE))
    for i, dot in enumerate([(0xFF, 0x5F, 0x56), (0xFF, 0xBD, 0x2E), (0x27, 0xC9, 0x3F)]):
        cx0 = x + 30 + i * 30
        c.d.ellipse([(cx0 - 8) * SS, (y + bar / 2 - 8) * SS, (cx0 + 8) * SS, (y + bar / 2 + 8) * SS], fill=dot)
    c.rrect(x + w * 0.16, y + bar * 0.24, w * 0.6, bar * 0.52, bar * 0.26, fill=WHITE, outline=BORDER, width=2)
    c.text(x + w * 0.18, y + bar / 2, spec.get("url", "localhost:3000"), max(14, int(w * 0.016)), SOFT, "mono", anchor="lm")
    pad = w * 0.03
    sx, sy = x + pad, y + bar + pad
    sw, sh = w - 2 * pad, h - bar - 2 * pad
    c.rrect(sx, sy, sw, sh, 10, fill=WHITE, outline=BORDER, width=2)
    fs = max(18, int(sw * 0.035))
    top = sy
    if spec.get("appbar"):
        ab = sh * 0.13
        c.rrect(sx, sy, sw, ab, 10, fill=ORANGE)
        c.rrect(sx, sy + ab * 0.5, sw, ab * 0.5, 0, fill=ORANGE)
        c.text(sx + sw * 0.04, sy + ab / 2, spec["appbar"], fs, WHITE, "bold", anchor="lm")
        top = sy + ab
    _ui_stack(c, sx, top, sw, sh - (top - sy), spec.get("screen", []), fs)


def r_browser(data, out):
    W = 1160; caph = 84 if data.get("caption") else 40
    H = 760 + caph
    c = C(W, H)
    _browser(c, 40, 30, W - 80, 700, data)
    if data.get("caption"):
        c.textblock(W / 2, H - caph + 12, data["caption"], 26, GRAY, "semi", W - 120, 34, anchor="ma")
    c.save(out)


def r_codeweb(data, out):
    """Código (JS/JSX) a la izquierda + el navegador con el RESULTADO a la derecha."""
    W = 1280; caph = 84 if data.get("caption") else 40
    H = 720 + caph
    c = C(W, H)
    cx, cy, cw, ch = 50, 40, 620, 660
    c.rrect(cx, cy, cw, ch, 22, fill=(0x1E, 0x20, 0x24))
    for i, dot in enumerate([(0xFF, 0x5F, 0x56), (0xFF, 0xBD, 0x2E), (0x27, 0xC9, 0x3F)]):
        c.d.ellipse([(cx + 34 + i * 34 - 9) * SS, (cy + 30 - 9) * SS,
                     (cx + 34 + i * 34 + 9) * SS, (cy + 30 + 9) * SS], fill=dot)
    ty = cy + 74; lh = 44
    for ln in data.get("code", []):
        st = ln.strip()
        col = ORANGE if (st.startswith("function") or st.startswith("const ") or st.startswith("<") or st.startswith("return")) else (0xE8, 0xEA, 0xED)
        c.text(cx + 30, ty, ln, 28, col, "mono", anchor="lm")
        ty += lh
    c.arrow_right(cx + cw + 6, cx + cw + 70, cy + ch / 2, color=ORANGE, width=6, head=18)
    _browser(c, cx + cw + 92, 40, W - (cx + cw + 92) - 40, 660, data)
    if data.get("caption"):
        c.textblock(W / 2, H - caph + 12, data["caption"], 26, GRAY, "semi", W - 120, 34, anchor="ma")
    c.save(out)


RENDERERS = {
    "phone": r_phone, "codeui": r_codeui, "palette": r_palette,
    "browser": r_browser, "codeweb": r_codeweb,
    "vflow": r_vflow, "stack": r_stack, "dualstack": r_dualstack, "sequence": r_sequence,
    "tree": r_tree, "bar": r_bar, "nested": r_nested, "compare": r_compare,
    "cards": r_cards, "blocks": r_blocks,
}

# ==================== CATÁLOGO ====================
CATALOG = {
 # ---- Cableado Estructurado ----
 "net_topologia": ("vflow", {"caption": "Los datos suben por las capas físicas hasta salir a Internet.", "nodes": [
    {"t": "PC / Cliente", "s": "genera y consume datos", "c": "neutral"},
    {"t": "Switch", "s": "capa 2 · entrega por dirección MAC", "c": "neutral"},
    {"t": "Router", "s": "capa 3 · decide rutas por IP", "c": "orange"},
    {"t": "Internet", "s": "otras redes", "c": "blue"},
 ]}),
 "stack_tcpip_osi": ("dualstack", {"caption": "El mismo territorio con dos mapas: OSI parte la capa de Aplicación en 3.",
    "left": {"title": "TCP/IP (5)", "items": [
        {"t": "5 · Aplicación", "c": "orange"}, {"t": "4 · Transporte"}, {"t": "3 · Red"},
        {"t": "2 · Enlace"}, {"t": "1 · Física"}]},
    "right": {"title": "OSI (7)", "items": [
        {"t": "7 · Aplicación", "c": "blue"}, {"t": "6 · Presentación", "c": "blue"},
        {"t": "5 · Sesión", "c": "blue"}, {"t": "4 · Transporte"}, {"t": "3 · Red"},
        {"t": "2 · Enlace"}, {"t": "1 · Física"}]}}),
 "duplex": ("cards", {"cols": 2, "ch": 420, "caption": "El trenzado de los pares cancela la interferencia (crosstalk).", "cards": [
    {"t": "Dúplex completo", "lines": ["Ambos extremos hablan", "a la vez", "(pares dedicados)"]},
    {"t": "Semidúplex", "lines": ["Hablan por turnos", "sobre el mismo medio", "(uno a la vez)"]}]}),
 "ip_32bits": ("bar", {"top_label": "192.168.1.10  /24", "mono": True,
    "caption": "La máscara /24 marca 24 bits de red y deja 8 de host (254 útiles).",
    "segments": [{"t": "RED (24 bits)", "frac": 0.72, "c": "blue", "s": "192.168.1"},
                 {"t": "HOST (8)", "frac": 0.28, "c": "orange", "s": ".10"}]}),
 "encapsulamiento": ("nested", {"caption": "Muñecas rusas: cada capa envuelve a la de arriba.", "layers": [
    {"t": "Trama Ethernet  (capa 2 · MAC + FCS)", "c": "neutral"},
    {"t": "Datagrama IP  (capa 3 · IP origen/destino)", "c": "tintb"},
    {"t": "Segmento TCP  (capa 4 · puertos)", "c": "tint"},
    {"t": "Datos", "c": "orange"}]}),
 "subred_split": ("tree", {"caption": "Una /24 se parte en 4 subredes /26 de 62 hosts útiles cada una.",
    "root": {"t": "192.168.10.0/24", "s": "254 hosts", "c": "orange"},
    "children": [{"t": ".0/26"}, {"t": ".64/26"}, {"t": ".128/26"}, {"t": ".192/26"}]}),
 "handshake": ("sequence", {"left": "Cliente", "right": "Servidor",
    "caption": "Tres pasos y la conexión queda ESTABLISHED (confiable).",
    "msgs": [{"dir": "LR", "n": 1, "t": "SYN (abro conexión)"},
             {"dir": "RL", "n": 2, "t": "SYN / ACK (acepto)"},
             {"dir": "LR", "n": 3, "t": "ACK (confirmo)"}]}),
 "socket_estados": ("vflow", {"bh": 104, "caption": "Ciclo de vida de una conexión TCP.", "nodes": [
    {"t": "LISTEN", "s": "el servidor espera", "c": "neutral"},
    {"t": "SYN_SENT / SYN_RCVD", "s": "handshake en curso", "c": "neutral"},
    {"t": "ESTABLISHED", "s": "conversando", "c": "orange"},
    {"t": "FIN_WAIT / CLOSE_WAIT", "s": "cerrando", "c": "neutral"},
    {"t": "CLOSED", "s": "conexión terminada", "c": "blue"}]}),
 "stack_viaje": ("stack", {"bidir": True, "note": "Cada capa usa a la de abajo y sirve a la de arriba.", "layers": [
    {"t": "Aplicación", "s": "HTTP pide la página", "c": "orange"},
    {"t": "Transporte", "s": "TCP · handshake al puerto 443"},
    {"t": "Red", "s": "IP cruza router a router"},
    {"t": "Enlace", "s": "trama llega al router (MAC)"},
    {"t": "Física", "s": "los bits viajan por el cable"}]}),
 "dns_resolucion": ("vflow", {"bh": 104, "caption": "Se resuelve una vez y se guarda en caché con un TTL.", "nodes": [
    {"t": "Caché local", "s": "¿ya lo tengo?", "c": "neutral"},
    {"t": "Servidor recursivo", "s": "pregunta por ti", "c": "neutral"},
    {"t": "Servidor raíz", "s": "¿quién maneja .com?", "c": "neutral"},
    {"t": "Servidor TLD (.com)", "s": "¿quién maneja el dominio?", "c": "neutral"},
    {"t": "Autoritativo", "s": "la IP definitiva", "c": "orange"}]}),
 "dora": ("sequence", {"left": "Cliente", "right": "Servidor DHCP",
    "caption": "La IP se entrega en arriendo (lease) por un tiempo.",
    "msgs": [{"dir": "LR", "n": "D", "t": "Discover (¿hay DHCP?)"},
             {"dir": "RL", "n": "O", "t": "Offer (te ofrezco esta IP)"},
             {"dir": "LR", "n": "R", "t": "Request (la acepto)"},
             {"dir": "RL", "n": "A", "t": "Ack (es tuya por X horas)"}]}),
 "nat": ("vflow", {"caption": "El router traduce muchas IP privadas a UNA pública (usa los puertos).", "nodes": [
    {"t": "PC privado", "s": "192.168.1.10", "c": "neutral"},
    {"t": "Router NAT/PAT", "s": "traduce IP + puerto", "c": "orange"},
    {"t": "Internet", "s": "IP pública 190.1.2.3", "c": "blue"}]}),
 "fttx": ("vflow", {"bh": 100, "caption": "Cuanto más cerca del hogar llega la fibra, mejor.", "nodes": [
    {"t": "Central del ISP", "c": "blue"},
    {"t": "FTTN — nodo del barrio", "c": "neutral"},
    {"t": "FTTB — edificio", "c": "neutral"},
    {"t": "FTTH — hogar", "c": "orange"}]}),
 "wan_vpn": ("sequence", {"left": "Sede A", "right": "Sede B",
    "caption": "La VPN sitio a sitio es la alternativa económica a una WAN dedicada.",
    "msgs": [{"dir": "LR", "t": "túnel cifrado por Internet"},
             {"dir": "RL", "t": "las dos redes, como una sola"}]}),
 "wifi_canales": ("cards", {"cols": 3, "ch": 360, "caption": "En 2.4 GHz solo 1, 6 y 11 no se solapan entre sí.", "cards": [
    {"big": "1", "t": "Canal 1", "lines": ["extremo bajo"]},
    {"big": "6", "t": "Canal 6", "lines": ["centro"]},
    {"big": "11", "t": "Canal 11", "lines": ["extremo alto"]}]}),
 "embudo": ("vflow", {"bh": 108, "caption": "Cada ping que funciona descarta una causa y acota el fallo.", "nodes": [
    {"t": "1 · ping a tu gateway", "s": "¿la red local vive?", "c": "neutral"},
    {"t": "2 · ping a 8.8.8.8", "s": "¿hay salida a Internet?", "c": "neutral"},
    {"t": "3 · ping a un dominio", "s": "si falla aquí → es DNS", "c": "orange"}]}),
 "ipv6_compresion": ("vflow", {"bh": 110, "caption": "Dos reglas: quitar ceros a la izquierda y UNA sola vez '::'.", "nodes": [
    {"t": "2001:0db8:0000:0000:0000:0000:0000:0001", "c": "neutral"},
    {"t": "2001:db8:0:0:0:0:0:1", "s": "sin ceros a la izquierda", "c": "neutral"},
    {"t": "2001:db8::1", "s": "un solo '::' colapsa los ceros", "c": "orange"}]}),

 # ---- Administración de Servidores ----
 "servidor_clientes": ("vflow", {"caption": "El servidor no tiene monitor: se administra por consola/red.", "nodes": [
    {"t": "Administrador", "s": "desde su PC (consola)", "c": "neutral"},
    {"t": "Red / SSH", "s": "conexión cifrada", "c": "orange"},
    {"t": "Servidor", "s": "sin teclado ni pantalla · sirve a muchos", "c": "blue"}]}),
 "ssh_remoto": ("sequence", {"left": "Tu PC", "right": "Servidor",
    "caption": "SSH = shell cifrada; el estándar para administrar sin estar al frente.",
    "msgs": [{"dir": "LR", "t": "ssh usuario@host  (puerto 22)"},
             {"dir": "RL", "t": "shell remota cifrada"}]}),
 "permisos_lsl": ("blocks", {"top_label": "- rwx r-x r--", "caption": "ls -l: 1 tipo + 3 tríadas (dueño · grupo · otros).", "blocks": [
    {"t": "-", "cap": "tipo", "w": 0.6, "ts": 44},
    {"t": "rwx", "cap": "dueño", "w": 1, "c": "orange"},
    {"t": "r-x", "cap": "grupo", "w": 1, "c": "tintb"},
    {"t": "r--", "cap": "otros", "w": 1, "c": "neutral"}]}),
 "privilegios_escalera": ("vflow", {"caption": "sudo eleva SOLO ese comando; nunca trabajes siempre como root.", "nodes": [
    {"t": "Usuario normal", "s": "permisos limitados", "c": "neutral"},
    {"t": "sudo <comando>", "s": "eleva un solo comando", "c": "orange"},
    {"t": "root (UID 0)", "s": "poder total — con cuidado", "c": "blue"}]}),
 "repo_flujo": ("vflow", {"caption": "Nunca bajes binarios sueltos: instala desde el repositorio firmado.", "nodes": [
    {"t": "Repositorio oficial", "s": "paquetes firmados (GPG)", "c": "blue"},
    {"t": "Gestor (apt / dnf)", "s": "resuelve dependencias", "c": "orange"},
    {"t": "Servidor", "s": "software instalado y verificado", "c": "neutral"}]}),
 "update_upgrade": ("compare", {"caption": "Primero update (refresca la lista), luego upgrade (instala).",
    "left": {"title": "apt update", "c": "blue", "items": [
        "Refresca la LISTA de versiones disponibles", "NO instala nada", "Consulta al repositorio"]},
    "right": {"title": "apt upgrade", "c": "orange", "items": [
        "INSTALA las versiones nuevas", "Cambia el sistema", "Requiere update antes"]}}),
 "storage_recorrido": ("vflow", {"bh": 100, "caption": "De un disco crudo a una carpeta donde por fin guardas archivos.", "nodes": [
    {"t": "Disco físico", "s": "/dev/sdb", "c": "neutral"},
    {"t": "Partición", "s": "fdisk / parted", "c": "neutral"},
    {"t": "Sistema de archivos", "s": "mkfs.ext4", "c": "orange"},
    {"t": "Punto de montaje", "s": "mount → /datos", "c": "blue"}]}),
 "lvm": ("vflow", {"caption": "LVM: volúmenes lógicos que crecen sin repartir el disco de nuevo.", "nodes": [
    {"t": "PV — Physical Volume", "s": "el disco/partición físico", "c": "neutral"},
    {"t": "VG — Volume Group", "s": "junta varios PV en un 'pozo'", "c": "orange"},
    {"t": "LV — Logical Volume", "s": "el volumen que montas y agrandas", "c": "blue"}]}),
 "arbol_procesos": ("tree", {"caption": "Todo proceso tiene un padre; el ancestro de todos es PID 1.",
    "root": {"t": "systemd", "s": "PID 1", "c": "orange"},
    "children": [
        {"t": "sshd", "s": "acceso remoto"},
        {"t": "nginx", "s": "servidor web", "children": ["worker 1", "worker 2"]},
        {"t": "cron", "s": "tareas programadas"}]}),
 "sigterm_sigkill": ("compare", {"caption": "SIGKILL (-9) es el ÚLTIMO recurso, nunca el primero.",
    "left": {"title": "SIGTERM (15)  ·  kill PID", "c": "blue", "items": [
        "'Termina, por favor'", "Guarda datos y cierra limpio", "Siempre se intenta PRIMERO"]},
    "right": {"title": "SIGKILL (9)  ·  kill -9 PID", "c": "orange", "items": [
        "Muere al instante", "No limpia nada", "Riesgo de archivos corruptos"]}}),
 "cron_campos": ("bar", {"top_label": "30  2  *  *  1", "mono": True,
    "caption": "30 2 * * 1  =  a las 2:30 AM, todos los lunes. ¡El 1.er campo es el minuto!",
    "segments": [{"t": "min", "frac": 1, "s": "30", "c": "orange"},
                 {"t": "hora", "frac": 1, "s": "2"},
                 {"t": "día-mes", "frac": 1.1, "s": "*"},
                 {"t": "mes", "frac": 1, "s": "*"},
                 {"t": "día-sem", "frac": 1.1, "s": "1"},
                 {"t": "comando", "frac": 2.3, "s": "/opt/bak.sh", "c": "blue"}]}),
 "backup_321": ("cards", {"cols": 3, "ch": 400, "caption": "La regla 3-2-1: sobrevive a borrados, fallos de disco e incendios.", "cards": [
    {"big": "3", "t": "copias", "lines": ["de tus datos", "(1 original + 2)"]},
    {"big": "2", "t": "medios", "lines": ["distintos", "(disco + nube)"]},
    {"big": "1", "t": "fuera de sitio", "lines": ["en otra ubicación", "(off-site)"]}]}),
 "troubleshooting_pasos": ("vflow", {"bh": 96, "caption": "Un método repetible sirve para CUALQUIER fallo del servidor.", "nodes": [
    {"t": "1 · Definir el síntoma", "s": "qué falla exactamente", "c": "neutral"},
    {"t": "2 · Reproducir y acotar", "s": "¿cuándo y dónde?", "c": "neutral"},
    {"t": "3 · Hipótesis y logs", "s": "mirar la evidencia", "c": "orange"},
    {"t": "4 · Aplicar un cambio", "s": "uno a la vez", "c": "neutral"},
    {"t": "5 · Verificar y documentar", "s": "confirmar y anotar", "c": "blue"}]}),

 # ---- Desarrollo de Aplicaciones Web (JavaScript · DOM · React · Redux) ----
 # Sesión 1 — JavaScript y DOM
 "web_js_dom": ("vflow", {"caption": "El navegador convierte el HTML en un árbol (DOM); tu JavaScript lo modifica en vivo.", "nodes": [
    {"t": "Documento HTML", "s": "estructura de la página", "c": "neutral"},
    {"t": "<script> JavaScript", "s": "el navegador lo ejecuta", "c": "orange"},
    {"t": "DOM", "s": "árbol vivo de la página", "c": "blue"}]}),
 "dom_tree": ("tree", {"caption": "El DOM representa el HTML como un árbol de nodos que JavaScript recorre y cambia.",
    "root": {"t": "document", "s": "la raíz de la página", "c": "orange"},
    "children": [
        {"t": "<head>", "s": "no visible", "children": ["<title>", "<meta>"]},
        {"t": "<body>", "s": "lo visible", "children": ["<h1>", "<div>", "<button>"]}]}),
 "text_vs_html": ("compare", {"caption": "Usa textContent salvo que de verdad necesites insertar etiquetas HTML.",
    "left": {"title": "textContent", "c": "blue", "items": [
        "Trata todo como TEXTO plano", "Más seguro: no interpreta HTML", "Ideal para datos del usuario"]},
    "right": {"title": "innerHTML", "c": "orange", "items": [
        "Interpreta etiquetas HTML", "Crea nodos desde el texto", "Riesgo de XSS con datos externos"]}}),
 # Sesión 2 — Eventos
 "evento_flujo": ("vflow", {"caption": "addEventListener conecta un evento del usuario con la función que responde.", "nodes": [
    {"t": "El usuario actúa", "s": "clic, tecleo, envío", "c": "neutral"},
    {"t": "El navegador crea el evento", "s": "objeto event: target, type", "c": "neutral"},
    {"t": "Se ejecuta el handler", "s": "tu función callback", "c": "orange"},
    {"t": "Cambias el DOM", "s": "la página responde", "c": "blue"}]}),
 "bubbling": ("vflow", {"bh": 116, "caption": "Bubbling: el evento nace en el elemento y 'burbujea' hacia sus ancestros.", "nodes": [
    {"t": "<button> (target)", "s": "donde ocurrió el clic", "c": "orange"},
    {"t": "<div> contenedor", "s": "recibe el evento después", "c": "neutral"},
    {"t": "<body> / document", "s": "el evento sigue subiendo", "c": "blue"}]}),
 # Sesión 3 — Arreglos y bucles
 "array_indices": ("bar", {"top_label": "[ 'a', 'b', 'c', 'd' ]", "mono": True,
    "caption": "Un arreglo guarda elementos en orden; se accede por índice desde 0. Aquí length = 4.",
    "segments": [{"t": "'a'", "frac": 1, "s": "[0]", "c": "orange"},
                 {"t": "'b'", "frac": 1, "s": "[1]"},
                 {"t": "'c'", "frac": 1, "s": "[2]"},
                 {"t": "'d'", "frac": 1, "s": "[3]", "c": "blue"}]}),
 "map_filter_reduce": ("cards", {"cols": 3, "ch": 380, "caption": "map, filter y reduce NO mutan el arreglo original: devuelven uno nuevo.", "cards": [
    {"t": "map", "lines": ["transforma cada elemento", "devuelve un arreglo NUEVO", "misma longitud"]},
    {"t": "filter", "lines": ["conserva los que cumplen", "arreglo más corto (o igual)"]},
    {"t": "reduce", "lines": ["combina todo en UN valor", "suma, total, objeto…"]}]}),
 "foreach_vs_map": ("compare", {"caption": "Si necesitas el resultado, usa map; si solo quieres recorrer, forEach.",
    "left": {"title": "forEach", "c": "blue", "items": [
        "Ejecuta algo por cada elemento", "NO devuelve nada (undefined)", "Para efectos secundarios"]},
    "right": {"title": "map", "c": "orange", "items": [
        "Transforma cada elemento", "DEVUELVE un arreglo nuevo", "Para obtener datos derivados"]}}),
 # Sesión 4 — React, ES6, JSX
 "dom_vs_react": ("compare", {"caption": "React es declarativo: describes el resultado, no los pasos para cambiar el DOM.",
    "left": {"title": "JS + DOM manual", "c": "blue", "items": [
        "Dices CÓMO cambiar cada nodo", "createElement, appendChild…", "Difícil de mantener al crecer"]},
    "right": {"title": "React (declarativo)", "c": "orange", "items": [
        "Describes CÓMO se ve la UI", "React actualiza el DOM por ti", "Componentes reutilizables"]}}),
 "jsx_transpila": ("vflow", {"caption": "JSX no lo entiende el navegador: Babel lo transpila a llamadas JavaScript.", "nodes": [
    {"t": "JSX", "s": "<h1>Hola {nombre}</h1>", "c": "orange"},
    {"t": "Babel (transpila)", "s": "convierte JSX en JS", "c": "neutral"},
    {"t": "React.createElement(...)", "s": "lo que corre el navegador", "c": "blue"}]}),
 "componente_jsx": ("vflow", {"caption": "Un componente es una función que retorna JSX y se usa como una etiqueta.", "nodes": [
    {"t": "function Saludo(props)", "s": "nombre en Mayúscula", "c": "neutral"},
    {"t": "return ( … JSX … )", "s": "un solo nodo raíz o Fragment", "c": "orange"},
    {"t": "<Saludo />", "s": "se usa como una etiqueta", "c": "blue"}]}),
 # Sesión 5 — Props
 "props_flujo": ("tree", {"caption": "Los datos fluyen de padre a hijo por props (top-down); el hijo no los modifica.",
    "root": {"t": "App", "s": "dueño de los datos", "c": "orange"},
    "children": [
        {"t": "<Lista items>", "s": "recibe una prop", "children": ["<Item> key=1", "<Item> key=2"]},
        {"t": "<Perfil usuario>", "s": "recibe una prop", "children": ["<Avatar>", "<Nombre>"]}]}),
 "flujo_unidireccional": ("vflow", {"bh": 116, "caption": "Flujo unidireccional: los datos bajan por props; nunca suben directamente.", "nodes": [
    {"t": "Componente padre", "s": "dueño del dato", "c": "orange"},
    {"t": "props ↓ (solo lectura)", "s": "pasa datos hacia abajo", "c": "neutral"},
    {"t": "Componente hijo", "s": "muestra el dato", "c": "blue"}]}),
 # Sesión 6 — useState
 "usestate_ciclo": ("vflow", {"bh": 108, "caption": "Cambiar el estado con el setter dispara un re-render: la UI se actualiza sola.", "nodes": [
    {"t": "Evento (clic)", "s": "el usuario interactúa", "c": "neutral"},
    {"t": "setValor(nuevo)", "s": "actualizas el estado", "c": "orange"},
    {"t": "React re-renderiza", "s": "ejecuta el componente otra vez", "c": "neutral"},
    {"t": "UI actualizada", "s": "la pantalla refleja el dato", "c": "blue"}]}),
 "usestate_anatomia": ("bar", {"top_label": "[valor, setValor] = useState(0)", "mono": True,
    "caption": "useState devuelve un par: el valor actual y la función para cambiarlo.",
    "segments": [{"t": "valor", "frac": 1, "s": "lectura", "c": "orange"},
                 {"t": "setValor", "frac": 1.2, "s": "actualiza", "c": "blue"},
                 {"t": "useState(0)", "frac": 1.3, "s": "valor inicial", "c": "neutral"}]}),
 "no_mutar": ("compare", {"caption": "Nunca mutes el estado: crea una copia nueva y pásala al setter.",
    "left": {"title": "Mutar directo (mal)", "c": "blue", "items": [
        "lista.push(x)", "valor = nuevo", "React NO se entera → no re-render"]},
    "right": {"title": "Usar el setter (bien)", "c": "orange", "items": [
        "setLista([...lista, x])", "copia con spread (…)", "React re-renderiza"]}}),
 # Sesión 7 — useEffect + APIs
 "useeffect_deps": ("cards", {"cols": 3, "ch": 360, "caption": "El arreglo de dependencias controla CUÁNDO se ejecuta el efecto.", "cards": [
    {"t": "[ ]", "lines": ["se ejecuta UNA vez", "al montar el componente"]},
    {"t": "[dep]", "lines": ["al montar y cada vez", "que dep cambia"]},
    {"t": "sin arreglo", "lines": ["en CADA render", "(cuidado: bucles)"]}]}),
 "fetch_estados": ("vflow", {"bh": 116, "caption": "Toda petición tiene tres estados: cargando, éxito y error. Manéjalos en la UI.", "nodes": [
    {"t": "Cargando", "s": "loading = true", "c": "neutral"},
    {"t": "fetch a la API", "s": "await res.json()", "c": "orange"},
    {"t": "Éxito o error", "s": "datos o mensaje de error", "c": "blue"}]}),
 "ciclo_vida": ("vflow", {"bh": 116, "caption": "useEffect cubre el ciclo de vida: montar, actualizar y limpiar al desmontar.", "nodes": [
    {"t": "Montar", "s": "useEffect(fn, [])", "c": "orange"},
    {"t": "Actualizar", "s": "useEffect(fn, [dep])", "c": "neutral"},
    {"t": "Desmontar", "s": "función de limpieza (cleanup)", "c": "blue"}]}),
 # Sesión 8 — Formularios
 "componente_controlado": ("sequence", {"left": "<input>", "right": "Estado (useState)",
    "caption": "Componente controlado: el estado es la única fuente de verdad del input.",
    "msgs": [{"dir": "LR", "n": 1, "t": "onChange: el usuario teclea"},
             {"dir": "LR", "n": 2, "t": "setTexto(e.target.value)"},
             {"dir": "RL", "n": 3, "t": "value={texto} pinta el input"}]}),
 "validacion_flujo": ("vflow", {"bh": 116, "caption": "Valida antes de enviar; muestra mensajes claros y deshabilita el botón si es inválido.", "nodes": [
    {"t": "onSubmit", "s": "preventDefault()", "c": "neutral"},
    {"t": "Validar campos", "s": "requerido · email · longitud", "c": "orange"},
    {"t": "¿Válido?", "s": "sí → enviar · no → mostrar error", "c": "blue"}]}),
 "controlado_vs_no": ("compare", {"caption": "En React se prefieren los componentes controlados (el estado manda).",
    "left": {"title": "Controlado", "c": "orange", "items": [
        "value + onChange al estado", "React conoce el valor siempre", "Fácil de validar en vivo"]},
    "right": {"title": "No controlado", "c": "blue", "items": [
        "El DOM guarda el valor", "Se lee con una ref", "Menos control"]}}),
 # Sesión 9 — Redux
 "redux_flujo": ("vflow", {"bh": 108, "caption": "Flujo unidireccional de Redux: dispatch → reducer → store → UI.", "nodes": [
    {"t": "Componente", "s": "dispatch(action)", "c": "neutral"},
    {"t": "Reducer", "s": "(state, action) → nuevo state", "c": "orange"},
    {"t": "Store", "s": "única fuente de verdad", "c": "blue"},
    {"t": "UI", "s": "useSelector lee y re-renderiza", "c": "neutral"}]}),
 "prop_drilling": ("compare", {"caption": "Redux evita pasar props por toda la jerarquía: el estado vive en un store central.",
    "left": {"title": "Prop drilling", "c": "blue", "items": [
        "Pasar props por muchos niveles", "Componentes que no usan el dato", "Difícil de mantener"]},
    "right": {"title": "Estado global (Redux)", "c": "orange", "items": [
        "El dato vive en el store", "Cualquier componente lo lee", "useSelector / useDispatch"]}}),
 "redux_piezas": ("tree", {"caption": "Las piezas de Redux: store (estado), actions (qué pasó) y reducers (cómo cambia).",
    "root": {"t": "store", "s": "única fuente de verdad", "c": "orange"},
    "children": [
        {"t": "state", "s": "los datos"},
        {"t": "actions", "s": "qué pasó"},
        {"t": "reducers", "s": "cómo cambia el state"}]}),

 # ---- Desarrollo de Aplicaciones Móviles 1 (Kotlin) ----
 # S1 — Introducción, variables y tipos
 "kt_flujo_playground": ("vflow", {"caption": "Sin instalar nada: escribes, ejecutas y ves el resultado en el navegador.", "nodes": [
    {"t": "1 · Escribes el código", "s": "en el editor de play.kotlinlang.org", "c": "neutral"},
    {"t": "2 · Pulsas ▶ Run", "s": "Kotlin compila tu programa", "c": "orange"},
    {"t": "3 · Ves la salida", "s": "en la consola de abajo", "c": "blue"}]}),
 "kt_val_var": ("compare", {"caption": "Regla de oro: empieza siempre con val; usa var solo si el valor de verdad cambia.",
    "left": {"title": "val — inmutable", "c": "blue", "items": [
        "Se asigna UNA sola vez", "No se puede reasignar", "Es la opción por defecto (más segura)", "val pi = 3.14"]},
    "right": {"title": "var — mutable", "c": "orange", "items": [
        "Se puede reasignar cuantas veces quieras", "Úsala solo si el valor CAMBIA", "var contador = 0  →  contador = 1"]}}),
 "kt_tipos_basicos": ("cards", {"cols": 3, "ch": 300, "caption": "Kotlin infiere el tipo solo, pero el tipo existe y es fijo.", "cards": [
    {"t": "Int", "lines": ["números enteros", "42, -7, 1000"]},
    {"t": "Double", "lines": ["decimales", "3.14, -0.5"]},
    {"t": "Boolean", "lines": ["verdadero / falso", "true, false"]},
    {"t": "String", "lines": ["texto", "\"Hola Kotlin\""]},
    {"t": "Char", "lines": ["un solo carácter", "'A', '9'"]}]}),

 # S2 — Condicionales
 "kt_if_else": ("tree", {"caption": "if evalúa una condición Boolean y toma UN camino.",
    "root": {"t": "condición (Boolean)", "s": "¿es verdadera?", "c": "orange"},
    "children": [{"t": "true", "s": "ejecuta el bloque if"}, {"t": "false", "s": "ejecuta el bloque else"}]}),
 "kt_when": ("tree", {"caption": "when compara un valor contra varias ramas; else cubre todo lo demás.",
    "root": {"t": "when (dia)", "s": "revisa el valor", "c": "orange"},
    "children": [{"t": "1..5", "s": "→ \"Entre semana\""}, {"t": "6, 7", "s": "→ \"Fin de semana\""}, {"t": "else", "s": "→ \"No válido\""}]}),
 "kt_if_expresion": ("compare", {"caption": "En Kotlin if y when también son EXPRESIONES: devuelven un valor.",
    "left": {"title": "if como sentencia", "c": "blue", "items": [
        "Solo ejecuta un bloque", "No devuelve nada útil", "Estilo tradicional (Java)"]},
    "right": {"title": "if como EXPRESIÓN", "c": "orange", "items": [
        "DEVUELVE un valor", "val max = if (a > b) a else b", "La última línea de cada rama es el valor"]}}),

 # S3 — Bucles
 "kt_rangos": ("bar", {"top_label": "for (i in 1..5)", "mono": True,
    "caption": "1..5 = del 1 al 5 (ambos incluidos) · until excluye el último · downTo baja · step salta.",
    "segments": [{"t": "1", "frac": 1}, {"t": "2", "frac": 1}, {"t": "3", "frac": 1},
                 {"t": "4", "frac": 1}, {"t": "5", "frac": 1, "c": "orange"}]}),
 "kt_while_do": ("compare", {"caption": "¿Revisas la condición ANTES o DESPUÉS de actuar?",
    "left": {"title": "while", "c": "blue", "items": [
        "Revisa la condición ANTES", "Si es falsa, no entra ni una vez", "while (x < 5) { ... }"]},
    "right": {"title": "do-while", "c": "orange", "items": [
        "Ejecuta y LUEGO revisa", "Se ejecuta al menos UNA vez", "do { ... } while (x < 5)"]}}),
 "kt_nested_loops": ("tree", {"caption": "Por cada vuelta del bucle exterior, el interior gira completo.",
    "root": {"t": "for i in 1..3", "s": "bucle exterior (filas)", "c": "orange"},
    "children": [{"t": "for j in 1..3", "s": "bucle interior (columnas)", "c": "blue",
        "children": ["i=1 → j=1,2,3", "i=2 → j=1,2,3", "i=3 → j=1,2,3"]}]}),
 "kt_break_continue": ("compare", {"caption": "break corta el bucle; continue solo salta una vuelta.",
    "left": {"title": "break", "c": "orange", "items": [
        "ROMPE el bucle por completo", "Sale de inmediato", "No sigue con más vueltas"]},
    "right": {"title": "continue", "c": "blue", "items": [
        "SALTA a la siguiente vuelta", "El bucle continúa", "Se salta solo esta iteración"]}}),

 # S4 — Funciones
 "kt_anatomia_funcion": ("blocks", {"top_label": "fun saludar(nombre: String): String",
    "caption": "Anatomía de una función: palabra clave, nombre, parámetros y tipo de retorno.",
    "blocks": [{"t": "fun", "cap": "palabra clave", "w": 0.7, "ts": 40},
               {"t": "saludar", "cap": "nombre", "w": 1, "c": "orange", "ts": 40},
               {"t": "(params)", "cap": "parámetros", "w": 1.2, "c": "tintb", "ts": 40},
               {"t": ": Tipo", "cap": "retorno", "w": 0.9, "ts": 40}]}),
 "kt_llamada_funcion": ("sequence", {"left": "main()", "right": "suma(a, b)",
    "caption": "main llama a la función con argumentos; la función devuelve un valor.",
    "msgs": [{"dir": "LR", "t": "llama con argumentos (3, 4)"},
             {"dir": "RL", "t": "return 7 (valor de retorno)"}]}),
 "kt_args": ("cards", {"cols": 2, "ch": 300, "caption": "Argumentos por defecto y nombrados hacen las funciones más flexibles.", "cards": [
    {"t": "Por defecto", "lines": ["fun saludar(msg: String = \"Hola\")", "si no pasas el valor, usa el default"]},
    {"t": "Nombrados", "lines": ["saludar(msg = \"Hey\")", "dices a qué parámetro va cada valor"]}]}),

 # S5 — POO I
 "kt_clase_objeto": ("tree", {"caption": "La clase es el molde; los objetos son las galletas hechas con él.",
    "root": {"t": "class Perro", "s": "el molde / plano", "c": "orange"},
    "children": [{"t": "firulais", "s": "objeto (instancia)"}, {"t": "rex", "s": "objeto (instancia)"}, {"t": "lassie", "s": "objeto (instancia)"}]}),
 "kt_anatomia_clase": ("stack", {"caption": "Una clase agrupa datos (propiedades) y comportamiento (métodos).", "layers": [
    {"t": "class Persona(...)", "s": "constructor primario", "c": "orange"},
    {"t": "val nombre · var edad", "s": "propiedades (datos)"},
    {"t": "init { }", "s": "se ejecuta al crear el objeto"},
    {"t": "fun saludar()", "s": "métodos (comportamiento)", "c": "blue"}]}),
 "kt_crear_objeto": ("sequence", {"left": "Tu código", "right": "objeto Persona",
    "caption": "Instanciar = crear un objeto usando el constructor de la clase.",
    "msgs": [{"dir": "LR", "n": 1, "t": "val p = Persona(\"Ana\", 20)"},
             {"dir": "RL", "n": 2, "t": "corre init y queda listo"},
             {"dir": "LR", "n": 3, "t": "p.saludar()"},
             {"dir": "RL", "n": 4, "t": "\"Hola, soy Ana\""}]}),

 # S6 — POO II
 "kt_herencia": ("tree", {"caption": "Los hijos heredan lo del padre y añaden lo suyo.",
    "root": {"t": "open class Animal", "s": "padre · comer(), dormir()", "c": "orange"},
    "children": [{"t": "Perro", "s": "ladrar()"}, {"t": "Gato", "s": "maullar()"}, {"t": "Vaca", "s": "mugir()"}]}),
 "kt_interface_abstract": ("compare", {"caption": "¿Comparto código hecho (abstracta) o defino un contrato (interface)?",
    "left": {"title": "Clase abstracta", "c": "blue", "items": [
        "Puede tener código ya hecho", "Puede guardar estado (propiedades)", "Se hereda con : (solo UNA)"]},
    "right": {"title": "Interface", "c": "orange", "items": [
        "Define QUÉ hacer (contrato)", "Una clase implementa VARIAS", "Sin estado propio, por lo general"]}}),
 "kt_polimorfismo": ("vflow", {"caption": "Polimorfismo: una misma llamada, muchos comportamientos.", "nodes": [
    {"t": "val animal: Animal = Perro()", "s": "tipo padre, objeto hijo", "c": "neutral"},
    {"t": "animal.hacerSonido()", "s": "la MISMA llamada", "c": "orange"},
    {"t": "\"Guau\"", "s": "Kotlin usa el método del objeto real", "c": "blue"}]}),
 "kt_visibilidad": ("stack", {"caption": "De más abierto (public) a más cerrado (private).", "layers": [
    {"t": "public", "s": "todos lo ven (por defecto)", "c": "neutral"},
    {"t": "internal", "s": "solo el mismo módulo"},
    {"t": "protected", "s": "la clase y sus hijas"},
    {"t": "private", "s": "solo dentro de la clase", "c": "orange"}]}),

 # S7 — Data class, enum, nulabilidad, excepciones
 "kt_dataclass": ("cards", {"cols": 2, "ch": 250, "caption": "data class genera todo esto por ti, automáticamente.", "cards": [
    {"t": "toString()", "lines": ["imprime bonito", "Persona(nombre=Ana, edad=20)"]},
    {"t": "equals() / hashCode()", "lines": ["compara por CONTENIDO", "no por dirección de memoria"]},
    {"t": "copy()", "lines": ["clona cambiando algo", "p.copy(edad = 21)"]},
    {"t": "componentN()", "lines": ["destructuring", "val (n, e) = persona"]}]}),
 "kt_nulabilidad": ("compare", {"caption": "El '?' es el permiso para poder valer null.",
    "left": {"title": "String", "c": "blue", "items": [
        "NUNCA puede ser null", "El compilador lo garantiza", "val n: String = \"hola\""]},
    "right": {"title": "String?", "c": "orange", "items": [
        "PUEDE ser null", "Debes manejar el caso null", "val n: String? = null"]}}),
 "kt_null_operadores": ("vflow", {"bh": 110, "caption": "?. y ?: son seguros; !! es el riesgoso (puede lanzar excepción).", "nodes": [
    {"t": "?.   safe call", "s": "si es null no explota; devuelve null", "c": "neutral"},
    {"t": "?:   Elvis", "s": "da un valor por defecto si es null", "c": "orange"},
    {"t": "!!   not-null", "s": "'confío en que no es null'... o crash", "c": "blue"}]}),
 "kt_try_catch": ("vflow", {"caption": "Atrapas el error y el programa sigue vivo en vez de caerse.", "nodes": [
    {"t": "try { }", "s": "código que PODRÍA fallar", "c": "neutral"},
    {"t": "catch (e) { }", "s": "qué hacer si falla", "c": "orange"},
    {"t": "finally { }", "s": "se ejecuta pase lo que pase", "c": "blue"}]}),
 "kt_enum": ("tree", {"caption": "Un enum es una lista cerrada de valores posibles.",
    "root": {"t": "enum class Dia", "s": "conjunto fijo", "c": "orange"},
    "children": [{"t": "LUNES"}, {"t": "MARTES"}, {"t": "...", "s": "hasta DOMINGO"}]}),

 # S8 — Colecciones
 "kt_colecciones": ("cards", {"cols": 3, "ch": 340, "caption": "Tres formas de agrupar datos: lista, conjunto y diccionario.", "cards": [
    {"t": "List", "lines": ["ordenada", "permite duplicados", "acceso por índice [0]"]},
    {"t": "Set", "lines": ["sin orden garantizado", "elementos ÚNICOS", "descarta duplicados"]},
    {"t": "Map", "lines": ["pares clave → valor", "acceso por clave", "como un diccionario"]}]}),
 "kt_inmutable_mutable": ("compare", {"caption": "Igual que val/var: prefiere la versión inmutable.",
    "left": {"title": "listOf() — inmutable", "c": "blue", "items": [
        "Solo lectura", "No puedes add() ni remove()", "Más segura · por defecto"]},
    "right": {"title": "mutableListOf() — mutable", "c": "orange", "items": [
        "Puedes add() y remove()", "Cambia después de crearla", "Úsala solo si debe cambiar"]}}),
 "kt_pipeline": ("vflow", {"bh": 108, "caption": "filter selecciona; map transforma. Se pueden encadenar.", "nodes": [
    {"t": "[1, 2, 3, 4, 5, 6]", "s": "lista original", "c": "neutral"},
    {"t": ".filter { it % 2 == 0 }", "s": "deja solo los pares  →  [2, 4, 6]", "c": "orange"},
    {"t": ".map { it * 10 }", "s": "transforma cada uno  →  [20, 40, 60]", "c": "blue"}]}),

 # S9 — Compose Multiplatform Web (WASM)
 "kt_compose_targets": ("tree", {"caption": "La misma UI declarativa en Kotlin, compilada a varias plataformas.",
    "root": {"t": "Compose Multiplatform", "s": "una sola UI en Kotlin", "c": "orange"},
    "children": [{"t": "Android"}, {"t": "iOS"}, {"t": "Desktop"}, {"t": "Web (WASM)", "s": "objetivo de hoy"}]}),
 "kt_wasm_flujo": ("vflow", {"caption": "WASM: formato compacto y veloz que el navegador ejecuta casi como nativo.", "nodes": [
    {"t": "Código Kotlin + Compose", "s": "funciones @Composable", "c": "neutral"},
    {"t": "Compilador Kotlin/Wasm", "s": "traduce a WebAssembly", "c": "orange"},
    {"t": "Navegador", "s": "corre la interfaz gráfica", "c": "blue"}]}),
 "kt_declarativo": ("compare", {"caption": "Compose describe el resultado; no ordena cada paso del dibujo.",
    "left": {"title": "Imperativo (tradicional)", "c": "blue", "items": [
        "Dices PASO A PASO cómo dibujar", "Tú actualizas la UI a mano al cambiar", "Más código y más errores"]},
    "right": {"title": "Declarativo (Compose)", "c": "orange", "items": [
        "Describes CÓMO se ve según el estado", "La UI se redibuja sola al cambiar", "@Composable fun Saludo()"]}}),
 "kt_playground_vs_compose": ("compare", {"caption": "De la consola (Playground) a la interfaz gráfica (Compose Web).",
    "left": {"title": "Kotlin en Playground", "c": "blue", "items": [
        "Programa de CONSOLA", "Entra y sale texto (println)", "Lo que hicimos en S1–S8"]},
    "right": {"title": "Compose Multiplatform Web", "c": "orange", "items": [
        "Interfaz gráfica (botones, texto)", "Corre en el navegador (WASM)", "Se arma en Android Studio / IntelliJ"]}}),

 # ==================================================================
 # ---- Desarrollo de Aplicaciones Móviles 1 · v2 (Jetpack Compose) ----
 # (asume Kotlin ya visto; enseña a CONSTRUIR apps con Compose)
 # ==================================================================
 # S1 — Introducción al desarrollo móvil y tu primera app
 "cmp_pila_movil": ("stack", {"caption": "Escribes Kotlin, Compose dibuja la UI y el sistema la muestra.", "layers": [
    {"t": "Tu app", "s": "pantallas con Jetpack Compose", "c": "orange"},
    {"t": "Jetpack Compose", "s": "el kit de interfaz (composables)"},
    {"t": "Kotlin", "s": "el lenguaje (ya lo conoces)"},
    {"t": "Android / navegador", "s": "el sistema donde corre", "c": "blue"}]}),
 "cmp_composable_funcion": ("vflow", {"caption": "Un composable no devuelve texto: emite UI que se ve en pantalla.", "nodes": [
    {"t": "@Composable fun Saludo()", "s": "una función que DESCRIBE interfaz", "c": "neutral"},
    {"t": "Text(\"Hola\")", "s": "adentro pones piezas de UI", "c": "orange"},
    {"t": "Se dibuja en pantalla", "s": "el usuario lo ve", "c": "blue"}]}),
 "cmp_flujo_web": ("vflow", {"caption": "El mismo Compose de Android, corriendo en una pestaña del navegador.", "nodes": [
    {"t": "1 · Escribes Compose (Kotlin)", "s": "funciones @Composable", "c": "neutral"},
    {"t": "2 · Kotlin/Wasm compila", "s": "traduce a WebAssembly", "c": "orange"},
    {"t": "3 · Lo ves en el navegador", "s": "la UI real, sin instalar nada", "c": "blue"}]}),

 # S2 — UI declarativa con Jetpack Compose
 "cmp_declarativo": ("compare", {"caption": "En Compose describes el QUÉ; Compose se encarga del CÓMO.",
    "left": {"title": "Imperativo (vista tradicional)", "c": "blue", "items": [
        "Buscas el widget y lo cambias a mano", "textView.setText(\"...\") paso a paso", "Tú sincronizas UI y datos"]},
    "right": {"title": "Declarativo (Compose)", "c": "orange", "items": [
        "Describes cómo se ve según el estado", "Text(mensaje) — y ya", "Compose redibuja solo al cambiar el dato"]}}),
 "cmp_composables_basicos": ("cards", {"cols": 2, "ch": 300, "caption": "Piezas de Lego: combinas composables para armar la pantalla.", "cards": [
    {"t": "Text", "lines": ["muestra texto", "Text(\"Hola\")"]},
    {"t": "Button", "lines": ["botón que reacciona", "Button(onClick = { }) { }"]},
    {"t": "Image", "lines": ["muestra una imagen", "Image(painter, ...)"]},
    {"t": "Spacer", "lines": ["deja espacio en blanco", "Spacer(Modifier.height(8.dp))"]}]}),
 "cmp_modifier_cadena": ("vflow", {"bh": 110, "caption": "Modifier se encadena y el ORDEN importa: cada uno envuelve al anterior.", "nodes": [
    {"t": ".padding(16.dp)", "s": "primero deja margen", "c": "neutral"},
    {"t": ".background(color)", "s": "luego pinta el fondo", "c": "orange"},
    {"t": ".clickable { }", "s": "y lo hace pulsable", "c": "blue"}]}),

 # S3 — Layouts y organización de la pantalla
 "cmp_column_row_box": ("cards", {"cols": 3, "ch": 320, "caption": "Tres contenedores para organizar la pantalla por bloques.", "cards": [
    {"t": "Column", "lines": ["apila en VERTICAL", "uno debajo de otro"]},
    {"t": "Row", "lines": ["alinea en HORIZONTAL", "uno al lado de otro"]},
    {"t": "Box", "lines": ["SUPERPONE capas", "uno encima de otro"]}]}),
 "cmp_arbol_composables": ("tree", {"caption": "La pantalla es un ÁRBOL de composables anidados.",
    "root": {"t": "Column", "s": "contenedor raíz", "c": "orange"},
    "children": [{"t": "Text", "s": "el título"},
                 {"t": "Row", "s": "una fila", "children": ["Image", "Text"]},
                 {"t": "Button", "s": "la acción"}]}),
 "cmp_weight": ("bar", {"top_label": "Row { Box(Modifier.weight(...)) }", "caption": "weight reparte el espacio sobrante en proporción.",
    "segments": [{"t": "weight(1f)", "frac": 1, "s": "1 parte", "c": "blue"},
                 {"t": "weight(2f)", "frac": 2, "s": "2 partes (el doble)", "c": "orange"}]}),

 # S4 — Estado e interacción
 "cmp_recomposicion": ("vflow", {"bh": 108, "caption": "Cambiar el estado dispara la recomposición: la UI se actualiza sola.", "nodes": [
    {"t": "El usuario actúa", "s": "toca un botón", "c": "neutral"},
    {"t": "Cambia el estado", "s": "count++  (mutableStateOf)", "c": "orange"},
    {"t": "Recomposición", "s": "Compose ejecuta el composable otra vez", "c": "neutral"},
    {"t": "UI actualizada", "s": "la pantalla refleja el nuevo dato", "c": "blue"}]}),
 "cmp_remember_state": ("bar", {"top_label": "var n by remember { mutableStateOf(0) }", "mono": True,
    "caption": "remember guarda el estado entre recomposiciones; mutableStateOf avisa cuando cambia.",
    "segments": [{"t": "remember", "frac": 1.2, "s": "lo conserva", "c": "blue"},
                 {"t": "mutableStateOf", "frac": 1.4, "s": "estado observable", "c": "orange"},
                 {"t": "0", "frac": 0.6, "s": "valor inicial", "c": "neutral"}]}),
 "cmp_state_hoisting": ("sequence", {"left": "Padre (dueño del estado)", "right": "Hijo (sin estado)",
    "caption": "State hoisting: el estado vive arriba; el hijo lo muestra y avisa los cambios.",
    "msgs": [{"dir": "LR", "n": 1, "t": "value = estado  (baja el dato)"},
             {"dir": "RL", "n": 2, "t": "onValueChange  (sube el evento)"}]}),

 # S5 — Listas y datos en pantalla
 "cmp_column_vs_lazy": ("compare", {"caption": "Para listas largas, LazyColumn: solo compone lo que se ve.",
    "left": {"title": "Column", "c": "blue", "items": [
        "Dibuja TODOS los elementos a la vez", "Bien para pocos ítems fijos", "Se traba con listas largas"]},
    "right": {"title": "LazyColumn", "c": "orange", "items": [
        "Solo compone lo VISIBLE en pantalla", "Recicla al desplazar (scroll)", "Ideal para listas largas de datos"]}}),
 "cmp_lista_flujo": ("vflow", {"bh": 104, "caption": "Separa el dato de su presentación: la UI pinta cada objeto como una tarjeta.", "nodes": [
    {"t": "data class Producto(...)", "s": "el DATO", "c": "neutral"},
    {"t": "List<Producto>", "s": "la colección", "c": "neutral"},
    {"t": "LazyColumn { items(lista) { … } }", "s": "recorre la lista", "c": "orange"},
    {"t": "Card por elemento", "s": "la PRESENTACIÓN de cada dato", "c": "blue"}]}),

 # S6 — Entrada del usuario y formularios
 "cmp_textfield_controlado": ("sequence", {"left": "TextField", "right": "Estado (remember)",
    "caption": "Campo controlado: el estado es la única fuente de verdad del texto.",
    "msgs": [{"dir": "LR", "n": 1, "t": "onValueChange: el usuario teclea"},
             {"dir": "LR", "n": 2, "t": "texto = nuevoValor"},
             {"dir": "RL", "n": 3, "t": "value = texto  (repinta el campo)"}]}),
 "cmp_validacion_flujo": ("vflow", {"bh": 116, "caption": "Valida en vivo: habilita el botón solo cuando los datos son correctos.", "nodes": [
    {"t": "El usuario escribe", "s": "cada tecla actualiza el estado", "c": "neutral"},
    {"t": "Validar", "s": "¿requerido? ¿formato? ¿longitud?", "c": "orange"},
    {"t": "¿Válido?", "s": "sí → habilita el botón · no → muestra error", "c": "blue"}]}),

 # S7 — Navegación entre pantallas
 "cmp_nav_grafo": ("tree", {"caption": "El NavHost declara las rutas; cada composable(route) es una pantalla.",
    "root": {"t": "NavHost", "s": "startDestination = \"home\"", "c": "orange"},
    "children": [{"t": "\"home\"", "s": "pantalla inicial"},
                 {"t": "\"detail/{id}\"", "s": "recibe un argumento"},
                 {"t": "\"settings\"", "s": "ajustes"}]}),
 "cmp_backstack": ("vflow", {"bh": 104, "caption": "El back stack es una PILA: navegar apila; atrás desapila.", "nodes": [
    {"t": "Home", "s": "pantalla base", "c": "neutral"},
    {"t": "navigate(\"detail\")", "s": "apila Detail encima", "c": "orange"},
    {"t": "Detail (arriba de la pila)", "s": "lo que ves ahora", "c": "blue"},
    {"t": "back → vuelve a Home", "s": "saca Detail de la pila", "c": "neutral"}]}),

 # S8 — Temas, Material Design y recursos
 "cmp_materialtheme": ("tree", {"caption": "MaterialTheme centraliza color, tipografía y formas: coherencia visual.",
    "root": {"t": "MaterialTheme", "s": "el tema de la app", "c": "orange"},
    "children": [{"t": "colorScheme", "s": "paleta (primary…)"},
                 {"t": "typography", "s": "estilos de texto"},
                 {"t": "shapes", "s": "esquinas y bordes"}]}),
 "cmp_claro_oscuro": ("compare", {"caption": "Un mismo diseño, dos esquemas de color según isSystemInDarkTheme().",
    "left": {"title": "Tema claro", "c": "blue", "items": [
        "Fondo claro, texto oscuro", "lightColorScheme()", "Por defecto de día"]},
    "right": {"title": "Tema oscuro", "c": "orange", "items": [
        "Fondo oscuro, texto claro", "darkColorScheme()", "Descansa la vista y ahorra batería"]}}),

 # S9 — Datos externos y Proyecto integrador
 "cmp_estados_ui": ("vflow", {"bh": 112, "caption": "Toda carga de datos tiene tres estados: cargando, éxito y error.", "nodes": [
    {"t": "Cargando", "s": "muestras un indicador de progreso", "c": "neutral"},
    {"t": "Llamada suspend a la API", "s": "traes los datos sin congelar la UI", "c": "orange"},
    {"t": "Éxito  o  Error", "s": "pintas la lista o un mensaje amable", "c": "blue"}]}),
 "cmp_arquitectura": ("stack", {"caption": "La app final integra todo lo del curso en capas.", "layers": [
    {"t": "Tema (Material 3)", "s": "el look & feel", "c": "orange"},
    {"t": "Navegación", "s": "varias pantallas y back stack"},
    {"t": "Estado", "s": "remember / mutableStateOf"},
    {"t": "UI · composables + listas", "s": "lo que se ve", "c": "blue"},
    {"t": "Datos", "s": "API o persistencia simple"}]}),
 "cmp_suspend_api": ("sequence", {"left": "App", "right": "API (servidor)",
    "caption": "Una función suspend hace la llamada sin congelar la interfaz.",
    "msgs": [{"dir": "LR", "t": "suspend fun: pide los datos"},
             {"dir": "RL", "t": "responde JSON (una lista)"}]}),

 # ===== MOCKUPS tipo imagen (teléfono/UI, código→preview, paleta) — dan variedad visual =====
 "cmp_s1_primera_app": ("codeui", {"caption": "Escribes un @Composable y ves el resultado en pantalla.",
    "code": ["@Composable", "fun PrimeraApp() {", "  Column {", "    Text(\"¡Hola, Móviles 1!\")", "    Button(onClick = {}) {", "      Text(\"Empezar\")", "    }", "  }", "}"],
    "title": "Mi primera app", "screen": [
        {"type": "text", "t": "¡Hola, Móviles 1!"}, {"type": "spacer"}, {"type": "button", "t": "Empezar"}]}),
 "cmp_s2_ui_mock": ("phone", {"title": "Perfil", "caption": "La misma UI que describes con composables, vista como app.",
    "screen": [{"type": "text", "t": "Tu perfil"}, {"type": "card", "t": "Nombre", "sub": "Ana Torres"},
               {"type": "card", "t": "Correo", "sub": "ana@correo.com"}, {"type": "spacer"}, {"type": "button", "t": "Editar"}]}),
 "cmp_s4_contador_mock": ("phone", {"title": "Contador", "caption": "El estado (remember) hace que la UI se actualice al tocar.",
    "screen": [{"type": "text", "t": "Toques: 3"}, {"type": "spacer"}, {"type": "button", "t": "+ Sumar"}, {"type": "button", "t": "Reiniciar"}]}),
 "cmp_s5_lista_mock": ("phone", {"title": "Tareas", "caption": "LazyColumn pinta una lista de objetos como tarjetas.",
    "screen": [{"type": "card", "t": "Estudiar Compose", "sub": "Hoy"}, {"type": "card", "t": "Hacer el taller", "sub": "Mañana"},
               {"type": "card", "t": "Subir evidencia", "sub": "Viernes"}, {"type": "card", "t": "Repasar estado", "sub": "Sábado"}]}),
 "cmp_s6_form_mock": ("phone", {"title": "Registro", "caption": "Campos controlados + validación antes de habilitar el botón.",
    "screen": [{"type": "field", "t": "Nombre"}, {"type": "field", "t": "Correo"}, {"type": "sub", "t": "Correo inválido"},
               {"type": "spacer"}, {"type": "button", "t": "Registrarme"}]}),
 "cmp_s8_paleta": ("palette", {"caption": "MaterialTheme usa un colorScheme; aquí, la marca Nueva América.",
    "colors": [{"name": "primary", "hex": "#FD531E"}, {"name": "onPrimary", "hex": "#FFFFFF"},
               {"name": "surface", "hex": "#F0F1F2"}, {"name": "onSurface", "hex": "#1A1C1D"}]}),
 "cmp_s9_app_final_mock": ("phone", {"title": "Mi app", "caption": "El proyecto integra UI + estado + lista + navegación + tema.",
    "screen": [{"type": "text", "t": "Inicio"}, {"type": "card", "t": "Elemento 1", "sub": "cargado desde datos"},
               {"type": "card", "t": "Elemento 2", "sub": "cargado desde datos"}, {"type": "spacer"}, {"type": "button", "t": "Ver detalle"}]}),

 # ===== MOCKUPS del curso WEB (navegador / código→navegador) — dan variedad visual =====
 "web_s1_dom_mock": ("codeweb", {"url": "index.html", "caption": "JavaScript cambia el DOM: lo que escribes se ve al instante en el navegador.",
    "code": ["const t = document", "  .querySelector('#saludo');", "t.textContent =", "  '¡Hola, Web!';", "t.style.color =", "  '#FD531E';"],
    "appbar": "Mi página", "screen": [{"type": "text", "t": "¡Hola, Web!"}, {"type": "sub", "t": "(texto cambiado desde JS)"}]}),
 "web_s4_primer_componente": ("codeweb", {"url": "localhost:3000", "caption": "Un componente es una función que retorna JSX; React lo pinta en el navegador.",
    "code": ["function Saludo() {", "  return (", "    <div>", "      <h1>Hola, React</h1>", "      <button>Entrar</button>", "    </div>", "  );", "}"],
    "appbar": "Mi app React", "screen": [{"type": "text", "t": "Hola, React"}, {"type": "spacer"}, {"type": "button", "t": "Entrar"}]}),
 "web_s6_contador_mock": ("browser", {"url": "localhost:3000", "appbar": "Contador (useState)",
    "caption": "El estado (useState) hace que la UI se vuelva a pintar al hacer clic.",
    "screen": [{"type": "text", "t": "Has hecho clic 3 veces"}, {"type": "spacer"}, {"type": "button", "t": "+ Sumar"}, {"type": "button", "t": "Reiniciar"}]}),
 "web_s7_fetch_mock": ("browser", {"url": "localhost:3000/usuarios", "appbar": "Usuarios (desde la API)",
    "caption": "useEffect + fetch: pides los datos y muestras cargando → éxito → error.",
    "screen": [{"type": "sub", "t": "✓ Cargado desde la API"}, {"type": "card", "t": "Ana Torres", "sub": "ana@correo.com"},
               {"type": "card", "t": "Carlos Ruiz", "sub": "carlos@correo.com"}, {"type": "card", "t": "Diana López", "sub": "diana@correo.com"}]}),
 "web_s8_form_mock": ("browser", {"url": "localhost:3000/registro", "appbar": "Registro",
    "caption": "Componente controlado: value + onChange, con validación y mensaje de error.",
    "screen": [{"type": "field", "t": "Nombre"}, {"type": "field", "t": "Correo"}, {"type": "sub", "t": "⚠ Correo inválido"},
               {"type": "spacer"}, {"type": "button", "t": "Registrarme"}]}),
 "web_s9_app_mock": ("browser", {"url": "localhost:3000", "appbar": "Mi App (proyecto final)",
    "caption": "El proyecto integra componentes + estado + APIs + Redux en una sola app.",
    "screen": [{"type": "text", "t": "Tablero"}, {"type": "card", "t": "Tarea 1", "sub": "en progreso"},
               {"type": "card", "t": "Tarea 2", "sub": "completada"}, {"type": "spacer"}, {"type": "button", "t": "Agregar tarea"}]}),

 # ===== Electiva de Profundización 3 — Redes de Nueva Generación (NGN) =====
 # ---- Clase 1: arquitecturas y tecnologías ----
 "ngn_evolucion": ("vflow", {"caption": "Cada salto agrega convergencia, virtualización e inteligencia.", "nodes": [
    {"t": "Redes tradicionales", "s": "circuitos dedicados · voz y datos por separado · hardware propietario", "c": "neutral"},
    {"t": "Redes convergentes (IP)", "s": "todo sobre IP: voz, datos y video en una sola red", "c": "neutral"},
    {"t": "Redes de nueva generación (NGN)", "s": "virtualizadas, programables y automatizadas", "c": "orange"},
    {"t": "Redes autónomas (IA)", "s": "se optimizan y se defienden solas", "c": "blue"}]}),
 "ngn_tradicional_vs_ngn": ("compare", {"caption": "NGN separa el software de la red del hardware que la transporta.",
    "left": {"title": "Red tradicional", "c": "blue", "items": [
        "Hardware propietario, difícil de cambiar",
        "Control distribuido, equipo por equipo (CLI)",
        "Escalar = comprar más equipos",
        "Configuración manual y lenta",
        "Servicios atados al hardware"]},
    "right": {"title": "Red NGN", "c": "orange", "items": [
        "Funciones virtualizadas sobre servidores estándar",
        "Control centralizado y programable (SDN)",
        "Escala elástica, como la nube",
        "Automatización y orquestación",
        "Servicios desacoplados del hardware (NFV)"]}}),
 "ngn_kpis": ("cards", {"cols": 4, "ch": 330, "caption": "Los KPIs traducen la calidad de la red en números medibles (SLA).", "cards": [
    {"t": "Latencia", "lines": ["Retardo extremo a extremo (ms).", "Menor es mejor; clave en tiempo real y 5G"]},
    {"t": "Throughput", "lines": ["Datos útiles por segundo (Gbps).", "Capacidad real de la red"]},
    {"t": "Jitter", "lines": ["Variación de la latencia.", "Afecta voz y video en tiempo real"]},
    {"t": "Disponibilidad", "lines": ["% de tiempo en servicio.", "99,9 % ≈ 8,7 h de caída al año"]}]}),
 "ngn_arquitectura_capas": ("stack", {"note": "En NGN el plano de control se separa del transporte y baja hasta la nube.", "layers": [
    {"t": "Aplicaciones y servicios", "s": "voz, video, IoT, nube", "c": "orange"},
    {"t": "Control / orquestación", "s": "SDN decide y programa la red"},
    {"t": "Transporte (IP / MPLS)", "s": "lleva los paquetes convergentes"},
    {"t": "Acceso", "s": "fibra, 5G, Wi-Fi 6/7"}]}),
 "ngn_redundancia": ("tree", {"caption": "Redundancia + failover = la red sigue viva aunque algo falle.",
    "root": {"t": "Alta disponibilidad", "s": "sin punto único de fallo (SPOF)", "c": "orange"},
    "children": [{"t": "Enlaces", "s": "doble ISP · rutas"}, {"t": "Equipos", "s": "HSRP · clúster"},
                 {"t": "Energía", "s": "UPS + planta"}, {"t": "Respaldo", "s": "3-2-1 · DR"}]}),
 "ngn_seleccion": ("vflow", {"caption": "Elegir tecnología es un proceso de decisión, no una moda.", "nodes": [
    {"t": "1 · Requisitos del negocio", "s": "usuarios, apps críticas, presupuesto", "c": "neutral"},
    {"t": "2 · Criterios técnicos", "s": "ancho de banda, latencia, cobertura, costo", "c": "neutral"},
    {"t": "3 · Comparar tecnologías", "s": "fibra vs 5G vs satélite vs cobre", "c": "orange"},
    {"t": "4 · Decisión justificada", "s": "la mejor relación desempeño / costo", "c": "blue"}]}),

 # ---- Clase 2: operación inteligente ----
 "ngn_sdn_planos": ("stack", {"note": "SDN separa QUIÉN decide (control) de QUIÉN reenvía (datos).", "layers": [
    {"t": "Plano de aplicación", "s": "apps de red · API northbound", "c": "orange"},
    {"t": "Plano de control", "s": "controlador SDN: el 'cerebro' central"},
    {"t": "Plano de datos", "s": "switches y routers · API southbound (OpenFlow)"}]}),
 "ngn_sdn_nfv": ("tree", {"caption": "SDN programa la red · NFV la virtualiza · MANO la orquesta y automatiza.",
    "root": {"t": "Operación NGN", "c": "orange"},
    "children": [{"t": "SDN", "s": "control central"}, {"t": "NFV", "s": "software de red"},
                 {"t": "MANO", "s": "orquestación"}]}),
 "ngn_ia_telecom": ("cards", {"cols": 4, "ch": 330, "caption": "La IA convierte la red en un sistema que aprende y se anticipa.", "cards": [
    {"t": "Predicción", "lines": ["Anticipa demanda y congestión", "antes de que ocurran"]},
    {"t": "Optimización", "lines": ["Ajusta rutas y recursos en tiempo real", "(self-optimizing networks)"]},
    {"t": "Mantenimiento", "lines": ["Predice qué equipo va a fallar", "antes de la caída"]},
    {"t": "Seguridad", "lines": ["Detecta anomalías y ataques", "por patrones de tráfico"]}]}),
 "ngn_qos": ("vflow", {"caption": "QoS garantiza que el tráfico crítico llegue a tiempo.", "nodes": [
    {"t": "1 · Clasificar", "s": "identifica el tipo de tráfico (voz, video, datos)", "c": "neutral"},
    {"t": "2 · Marcar", "s": "etiqueta la prioridad (DSCP / CoS)", "c": "neutral"},
    {"t": "3 · Encolar y priorizar", "s": "la voz pasa antes que una descarga", "c": "orange"},
    {"t": "4 · Gestionar congestión", "s": "policing / shaping: descarta lo menos crítico", "c": "neutral"}]}),
 "ngn_anomalias": ("sequence", {"left": "Red NGN", "right": "Motor de IA",
    "caption": "La IA aprende lo normal para señalar lo anómalo (posible ataque).",
    "msgs": [{"dir": "LR", "n": 1, "t": "telemetría y flujos de tráfico"},
             {"dir": "RL", "n": 2, "t": "aprende el patrón normal (baseline)"},
             {"dir": "LR", "n": 3, "t": "tráfico anómalo (pico raro)"},
             {"dir": "RL", "n": 4, "t": "alerta + mitigación automática"}]}),
 "ngn_dashboard": ("browser", {"url": "noc.miempresa.com/dashboard", "appbar": "NOC · Estado de la red NGN",
    "caption": "Un dashboard traduce miles de métricas en un semáforo de decisiones.",
    "screen": [{"type": "card", "t": "Disponibilidad", "sub": "99,97 % · SLA cumplido"},
               {"type": "card", "t": "Latencia media", "sub": "12 ms · dentro de lo normal"},
               {"type": "card", "t": "Tráfico", "sub": "6,4 Gbps · 71 % de capacidad"},
               {"type": "sub", "t": "Anomalia detectada por IA en el enlace WAN-2"}]}),
}


def path_for(diag_id):
    return os.path.join(OUT_DIR, diag_id + ".png")


def render_all(verbose=True):
    os.makedirs(OUT_DIR, exist_ok=True)
    done = 0
    for did, (kind, data) in CATALOG.items():
        out = path_for(did)
        RENDERERS[kind](data, out)
        done += 1
        if verbose:
            print("  ok", did)
    if verbose:
        print("Diagramas generados:", done, "->", OUT_DIR)
    return done


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    render_all()
