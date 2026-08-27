# -*- coding: utf-8 -*-
"""Sondeo de solo lectura: qué campos y qué captcha tiene el registro de cada revista.

No rellena, no envía, no crea nada. Abre cada `/user/register`, lista los campos del
formulario y dice si hay reCAPTCHA (y de qué tipo). Sirve para escribir el registrador
sin adivinar selectores.

Uso:
  python config/revistas/_sondear_registro.py
"""
from __future__ import annotations

import sys
from pathlib import Path

for _f in (sys.stdout, sys.stderr):
    if hasattr(_f, "reconfigure"):
        _f.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gdocs"))

REVISTAS = [
    ("EDU REVIEW", "https://edulab.es/revEDU/user/register"),
    ("Revista Virtual UCN", "https://revistavirtual.ucn.edu.co/index.php/RevistaUCN/user/register"),
    ("Revista CEA (ITM)", "https://revistas.itm.edu.co/index.php/revista-cea/user/register"),
    ("TecnoLógicas (ITM)", "https://revistas.itm.edu.co/index.php/tecnologicas/user/register"),
    ("ITEES (EIDEC)", "https://revistaseidec.com/index.php/ITEES/user/register"),
]

JS_CAMPOS = """
() => {
  const out = {campos: [], captcha: [], checkboxes: [], selects: [], submit: []};
  document.querySelectorAll('input, textarea').forEach(e => {
    if (e.type === 'hidden') return;
    out.campos.push({tag: e.tagName.toLowerCase(), type: e.type || '', name: e.name || '',
                     id: e.id || '', required: e.required === true,
                     label: (document.querySelector('label[for="'+e.id+'"]')||{}).innerText || ''});
  });
  document.querySelectorAll('select').forEach(e => {
    out.selects.push({name: e.name || '', id: e.id || '', opciones: e.options.length});
  });
  document.querySelectorAll('button[type=submit], input[type=submit]').forEach(e => {
    out.submit.push({txt: (e.innerText || e.value || '').trim(), name: e.name || ''});
  });
  if (document.querySelector('.g-recaptcha, [data-sitekey]')) out.captcha.push('recaptcha v2 (widget)');
  if (document.querySelector('iframe[src*="recaptcha"]')) out.captcha.push('recaptcha (iframe)');
  if (document.querySelector('iframe[src*="hcaptcha"]')) out.captcha.push('hcaptcha');
  if (/grecaptcha/.test(document.documentElement.innerHTML)) out.captcha.push('grecaptcha en el html');
  if (document.querySelector('img[src*="captcha"]')) out.captcha.push('captcha de imagen propio');
  return out;
}
"""


def main() -> int:
    from sesion_google import abrir, cerrar

    p, ctx, pg = abrir(headless=True)
    try:
        for nombre, url in REVISTAS:
            print("=" * 78)
            print(f"{nombre}\n  {url}")
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=45000)
                pg.wait_for_timeout(2500)
            except Exception as e:
                print(f"  NO ABRE: {str(e).splitlines()[0][:110]}")
                continue

            if "register" not in pg.url:
                print(f"  redirige a: {pg.url}")

            try:
                d = pg.evaluate(JS_CAMPOS)
            except Exception as e:
                print(f"  no pude leer el formulario: {str(e).splitlines()[0][:110]}")
                continue

            campos = [c for c in d["campos"] if c["name"] or c["id"]]
            if not campos:
                cuerpo = (pg.evaluate("() => document.body.innerText || ''") or "")[:200]
                print(f"  SIN FORMULARIO. Empieza la página con: {cuerpo.strip()[:160]!r}")
                continue

            print(f"  campos ({len(campos)}):")
            for c in campos:
                marca = "*" if c["required"] else " "
                et = (c["label"] or "").replace("\n", " ")[:34]
                print(f"    {marca} {c['type']:<9} name={c['name']:<28} {et}")
            for s in d["selects"]:
                print(f"      select    name={s['name']:<28} ({s['opciones']} opciones)")
            print(f"  botones: {[b['txt'][:28] for b in d['submit']]}")
            print(f"  CAPTCHA: {sorted(set(d['captcha'])) or 'ninguno detectado'}")
        print("=" * 78)
    finally:
        cerrar(p, ctx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
