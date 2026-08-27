# -*- coding: utf-8 -*-
r"""Crea las cuentas del Docente en los OJS de las revistas gratuitas.

QUÉ HACE Y QUÉ NO
-----------------
Crea **cuentas**. No somete manuscritos, no sube archivos y no publica nada. Someter es
irreversible y va aparte, con el visto bueno del Docente en ese momento.

EL CAPTCHA
----------
De las cinco revistas sondeadas (`_sondear_registro.py`), **dos no tienen captcha** y se
registran solas; **tres tienen reCAPTCHA v2** y ahí hace falta la mano del Docente. El guion
no intenta resolverlo ni lo rodea: rellena todo lo demás, deja la ventana abierta en el
captcha y **sondea la página** cada 3 s hasta que el registro sale. No espera en la consola
—ese patrón ya está probado en `config/gdocs/sesion_google.py:login`— para que la espera no
bloquee nada.

DÓNDE VAN LAS CLAVES
--------------------
En ``%LOCALAPPDATA%\revistas-cun\credenciales.json``, **fuera del repositorio**, que está en
git y sincronizado a Google Drive. Se genera una clave distinta por revista con `secrets` y
**nunca se imprime**: el guion dice la ruta del archivo, no el contenido.

LA INSTALACIÓN DEL ITM ES UNA SOLA
----------------------------------
`revistas.itm.edu.co` aloja TecnoLógicas y Revista CEA en el mismo OJS. En un OJS
multirrevista la cuenta es del **sitio**, no de la revista, así que con registrarse una vez
sirve para las dos: la segunda solo pide inscribirse en esa revista.

Uso:
  python config/revistas/registrar_revistas.py                 # todas
  python config/revistas/registrar_revistas.py --solo ucn      # una
  python config/revistas/registrar_revistas.py --sin-captcha   # solo las automáticas
  python config/revistas/registrar_revistas.py --espera 420    # más margen para el captcha
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import string
import sys
from pathlib import Path

for _f in (sys.stdout, sys.stderr):
    if hasattr(_f, "reconfigure"):
        _f.reconfigure(encoding="utf-8", errors="replace")

# ─────────────────────────── identidad del Docente ───────────────────────────
# Lo único que se escribe aquí son datos ya públicos (los que van en la portada de un
# artículo). La clave no: esa se genera y se guarda fuera del repositorio.
NOMBRE = "Julian Andrés"
APELLIDOS = "Castaño Espinosa"
FILIACION = "Corporación Unificada Nacional de Educación Superior — CUN, Escuela de Ingenierías"
CORREO = "julian_castanoe@cun.edu.co"
USUARIO = "jcastanoe"          # si alguna revista lo tiene cogido, el guion lo dice
PAIS = "CO"                     # Colombia, código ISO que usa OJS
INTERESES = ("analítica del aprendizaje, tecnología educativa, aprendizaje automático aplicado "
             "a la educación, Moodle, evaluación formativa")

# ¿Ofrecerse como evaluador al registrarse? Se deja en False a propósito: compromete al
# Docente a revisar para esa revista, y esa es su decisión, no la del guion.
OFRECERSE_COMO_EVALUADOR = False

# ─────────────────────────────── los destinos ────────────────────────────────
REVISTAS = [
    # (clave, nombre, url de registro, ¿tiene captcha?, nota)
    ("ucn", "Revista Virtual UCN",
     "https://revistavirtual.ucn.edu.co/index.php/RevistaUCN/user/register", False,
     "Destino 2. Sin cargos por escrito, recepción permanente."),
    ("itees", "ITEES (EIDEC)",
     "https://revistaseidec.com/index.php/ITEES/user/register", False,
     "Cargos sin verificar: preguntar a revistaitees@eidec.com.co."),
    ("edu", "EDU REVIEW",
     "https://edulab.es/revEDU/user/register", True,
     "Destino 1. Gratuita y permite preprints, las dos cosas por escrito."),
    ("tecnologicas", "TecnoLógicas (ITM)",
     "https://revistas.itm.edu.co/index.php/tecnologicas/user/register", True,
     "Publindex B. Misma instalación que CEA: una cuenta sirve para las dos."),
    ("cea", "Revista CEA (ITM)",
     "https://revistas.itm.edu.co/index.php/revista-cea/user/register", True,
     "Misma instalación que TecnoLógicas."),
    ("nodo", "Revista NODO (UAN)",
     "https://revistas.uan.edu.co/index.php/nodo/user/register", True,
     "Sin cargos por escrito. Ámbito artes y humanidades: encaje flojo, cuenta útil igual."),
    ("ignis", "Revista Ignis (CUN)",
     "https://revistas.cun.edu.co/index.php/ignis/user/register", True,
     "Revista de la casa. Solo alcanzable con Chrome real: BunkerWeb bloquea las herramientas."),
    ("opinion", "Revista Opinión Pública (CUN)",
     "https://revistas.cun.edu.co/index.php/opinionpublica/user/register", True,
     "Revista de la casa. Igual que Ignis: hace falta Chrome real."),
]

# Gratuitas de la lista donde NO se puede registrar, y por qué. Se dejan anotadas para que nadie
# vuelva a intentarlo: su `/user/register` no trae formulario ninguno, así que no es un problema
# de automatización sino que esa vía está cerrada.
SIN_FORMULARIO_DE_REGISTRO = {
    "HUMAN REVIEW (Eagora)": "https://historicoeagora.net/revHUMAN/user/register",
    "Sinergias Educativas": "https://sinergiaseducativas.mx/index.php/revista/user/register",
}

BASE = Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))) / "revistas-cun"
PERFIL = BASE / "perfil"
CREDENCIALES = BASE / "credenciales.json"

ARGS_CHROME = [
    "--disable-blink-features=AutomationControlled",
    "--no-first-run",
    "--no-default-browser-check",
]


# ──────────────────────────────── claves ─────────────────────────────────────
def clave_nueva(n: int = 20) -> str:
    """Clave fuerte sin caracteres que se confundan al leerlos ni rompan un formulario."""
    alfabeto = (string.ascii_letters + string.digits + "!@#$%*-_=+").replace("l", "") \
        .replace("I", "").replace("O", "").replace("0", "")
    return "".join(secrets.choice(alfabeto) for _ in range(n))


def guardadas() -> dict:
    if not CREDENCIALES.is_file():
        return {}
    try:
        return json.loads(CREDENCIALES.read_text(encoding="utf-8"))
    except Exception:
        return {}


def guardar(clave_revista: str, datos: dict) -> None:
    """Escribe la credencial fuera del repositorio. Idempotente: no pisa lo que ya sirve."""
    BASE.mkdir(parents=True, exist_ok=True)
    todo = guardadas()
    todo[clave_revista] = datos
    CREDENCIALES.write_text(json.dumps(todo, indent=2, ensure_ascii=False), encoding="utf-8")
    try:  # en Windows no hay chmod real, pero no cuesta intentarlo
        os.chmod(CREDENCIALES, 0o600)
    except Exception:
        pass


def _tapar(t: str) -> str:
    """Ninguna clave sale por pantalla, ni dentro de un mensaje de error."""
    for d in guardadas().values():
        c = d.get("clave")
        if c:
            t = t.replace(c, "********")
    return t


# ──────────────────────────────── navegador ──────────────────────────────────
def abrir(headless: bool):
    """Chrome de verdad y perfil propio: el mismo motivo que en `sesion_google`."""
    from playwright.sync_api import sync_playwright

    PERFIL.mkdir(parents=True, exist_ok=True)
    p = sync_playwright().start()
    try:
        ctx = p.chromium.launch_persistent_context(
            str(PERFIL), channel="chrome", headless=headless,
            viewport={"width": 1500, "height": 1000}, args=ARGS_CHROME,
            locale="es-CO", timezone_id="America/Bogota",
        )
    except Exception as e:
        p.stop()
        if "chrome" in str(e).lower():
            raise SystemExit("No encontré Google Chrome instalado; hace falta Chrome de verdad.")
        raise
    return p, ctx, (ctx.pages[0] if ctx.pages else ctx.new_page())


def cerrar(p, ctx) -> None:
    for accion in (lambda: ctx.close(), lambda: p.stop()):
        try:
            accion()
        except Exception:
            pass


# ───────────────────────────── el formulario ─────────────────────────────────
def _poner(pg, nombre_campo: str, valor: str) -> bool:
    """Rellena `input[name=X]` si está. Devuelve si lo encontró. Tolera los sufijos de idioma."""
    for sel in (f'input[name="{nombre_campo}"]', f'input[name^="{nombre_campo}["]',
                f'textarea[name="{nombre_campo}"]'):
        try:
            c = pg.locator(sel).first
            if c.count() and c.is_visible():
                c.fill(valor)
                return True
        except Exception:
            pass
    return False


def _marcar(pg, nombre_campo: str, marcar: bool = True) -> bool:
    for sel in (f'input[name="{nombre_campo}"]', f'input[name^="{nombre_campo}["]'):
        try:
            c = pg.locator(sel).first
            if c.count() and c.is_visible():
                c.check() if marcar else c.uncheck()
                return True
        except Exception:
            pass
    return False


def aviso_en_pagina(pg, revista: str) -> None:
    """Pinta un cartel dentro de la propia página.

    La ventana tiene que explicarse sola: en las dos primeras corridas el captcha se quedó sin
    resolver porque nada en la pantalla decía qué se esperaba ni de qué revista era el formulario.
    """
    js = """
    (revista) => {
      const viejo = document.getElementById('aviso-cun'); if (viejo) viejo.remove();
      const d = document.createElement('div');
      d.id = 'aviso-cun';
      d.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:2147483647;' +
        'background:#0C2340;color:#fff;padding:14px 18px;font:600 15px/1.45 Segoe UI,Arial,sans-serif;' +
        'box-shadow:0 2px 12px rgba(0,0,0,.45);text-align:center';
      d.innerHTML = '<span style="color:#91DC00">CREAR CUENTA · ' + revista + '</span><br>' +
        'El formulario ya está relleno. <b>Solo marca el reCAPTCHA «No soy un robot».</b> ' +
        'NO pulses «Registrarse»: lo envío yo en el momento en que lo marques, ' +
        'porque el token caduca en 2 minutos.' +
        '<br><span style="font-weight:400;opacity:.85">Puedes cerrar esta ventana para cancelar.</span>';
      document.body.appendChild(d);
      document.body.style.paddingTop = '92px';
    }
    """
    try:
        pg.evaluate(js, revista)
    except Exception:
        pass  # si no se puede pintar, no es motivo para abortar el registro


def captcha_resuelto(pg) -> bool:
    """¿Está ya marcado el reCAPTCHA?

    Se lee el token que Google deja en `textarea[name=g-recaptcha-response]`. Importa porque el
    token **caduca en unos 2 minutos**: en el tercer intento el formulario se envió con el captcha
    ya marcado y EDU REVIEW contestó «No superó la comprobación de validación utilizada para evitar
    envíos de spam». La respuesta es no depender de que el humano pulse a tiempo: en cuanto aparece
    el token, el guion envía.
    """
    try:
        return bool(pg.evaluate("""() => {
          const t = document.querySelector('textarea[name="g-recaptcha-response"]');
          if (t && t.value && t.value.length > 20) return true;
          try { const r = grecaptcha.getResponse(); return !!(r && r.length > 20); } catch (e) {}
          return false;
        }"""))
    except Exception:
        return False


def errores_en_pagina(pg) -> list[str]:
    """Los mensajes que OJS pinta cuando algo no cuadra (usuario cogido, correo repetido…)."""
    try:
        return [t.strip() for t in pg.locator(
            ".pkp_form_error, .error, [role=alert], .alert-danger").all_inner_texts()
            if t.strip()][:6]
    except Exception:
        return []


def ya_registrado(pg) -> bool:
    """En un OJS multirrevista, si la cuenta ya existe la página de registro no pide clave."""
    try:
        return not pg.locator('input[name="password"]').first.count()
    except Exception:
        return False


def rellenar(pg, clave: str) -> dict:
    """Pone todo salvo el captcha. Devuelve qué campos se encontraron."""
    puesto = {
        "givenName": _poner(pg, "givenName", NOMBRE),
        "familyName": _poner(pg, "familyName", APELLIDOS),
        "affiliation": _poner(pg, "affiliation", FILIACION),
        "email": _poner(pg, "email", CORREO),
        "username": _poner(pg, "username", USUARIO),
        "password": _poner(pg, "password", clave),
        "password2": _poner(pg, "password2", clave),
        "interests": _poner(pg, "interests", INTERESES),
    }
    try:
        s = pg.locator('select[name="country"]').first
        if s.count():
            s.select_option(value=PAIS)
            puesto["country"] = True
    except Exception:
        puesto["country"] = False

    # El consentimiento de privacidad es obligatorio para poder registrarse.
    puesto["privacyConsent"] = _marcar(pg, "privacyConsent", True)
    # Los otros dos se dejan sin marcar a propósito: no comprometen al Docente a nada.
    _marcar(pg, "emailConsent", False)
    for grupo in ("reviewerGroup",):
        _marcar(pg, grupo, OFRECERSE_COMO_EVALUADOR)
    return puesto


def registrar(pg, rev, espera_s: int) -> tuple[str, str]:
    """Devuelve `(estado, detalle)`. Estado: ok | ya | error | espera_agotada."""
    clave_rev, nombre, url, con_captcha, _ = rev
    try:
        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(2500)
    except Exception as e:
        return "error", f"no abre: {str(e).splitlines()[0][:110]}"

    if ya_registrado(pg):
        return "ya", "la cuenta ya existe en esta instalación (no pide clave)"

    clave = guardadas().get(clave_rev, {}).get("clave") or clave_nueva()
    puesto = rellenar(pg, clave)
    faltan = [k for k, v in puesto.items() if not v]
    detalle_campos = f"campos sin encontrar: {faltan}" if faltan else "todos los campos puestos"

    if con_captcha:
        aviso_en_pagina(pg, nombre)
        print(f"    {detalle_campos}")
        print("    >>> MARCA SOLO EL reCAPTCHA EN LA VENTANA. El envío lo hago yo. <<<")
        print(f"        La ventana lleva un cartel con la instrucción. Sondeo cada 3 s"
              f" hasta {espera_s} s; cierra la ventana para cancelar.")
    else:
        try:
            pg.locator('button[type="submit"], input[type="submit"]').first.click()
            pg.wait_for_timeout(4000)
        except Exception as e:
            return "error", f"no pude pulsar Registrarse: {str(e).splitlines()[0][:110]}"

    # Sondeo: el registro salió cuando la página de registro deja de pedir la clave.
    # Con captcha se vigila cada 1,5 s y se ENVÍA en cuanto aparece el token, sin esperar a que
    # el humano pulse: así el token no puede caducar entre el clic y el envío.
    transcurrido = 0
    paso = 1500 if con_captcha else 3000
    limite = espera_s * 1000 if con_captcha else 12000
    enviados = 0
    while transcurrido < limite:
        try:
            if "/user/register" not in pg.url or ya_registrado(pg):
                guardar(clave_rev, {"revista": nombre, "usuario": USUARIO,
                                    "correo": CORREO, "clave": clave, "url": url})
                return "ok", f"registrado · credencial en {CREDENCIALES}"

            if con_captcha and captcha_resuelto(pg):
                # Se rellena otra vez por si la página se recargó tras un envío fallido.
                if enviados:
                    rellenar(pg, clave)
                enviados += 1
                print(f"        captcha marcado -> envío yo el formulario (intento {enviados})")
                try:
                    pg.locator('button[type="submit"], input[type="submit"]').first.click()
                    pg.wait_for_timeout(5000)
                except Exception:
                    pass
                if "/user/register" not in pg.url or ya_registrado(pg):
                    guardar(clave_rev, {"revista": nombre, "usuario": USUARIO,
                                        "correo": CORREO, "clave": clave, "url": url})
                    return "ok", f"registrado · credencial en {CREDENCIALES}"
                errs = errores_en_pagina(pg)
                if errs:
                    print(f"        rechazado: {_tapar(' · '.join(errs))[:150]}")
                if enviados >= 4:
                    return "error", _tapar(" · ".join(errs or ["rechazado 4 veces"]))[:220]
                aviso_en_pagina(pg, nombre)

            errs = errores_en_pagina(pg)
            if errs and not con_captcha:
                return "error", _tapar(" · ".join(errs))[:220]
            # El cartel se pierde en cada recarga de la página, así que se repinta.
            if con_captcha and transcurrido and transcurrido % 15000 == 0:
                aviso_en_pagina(pg, nombre)
        except Exception as e:
            if "closed" in str(e).lower():
                return "error", "se cerró la ventana (cancelado)"
        pg.wait_for_timeout(paso)
        transcurrido += paso
        if con_captcha and transcurrido % 60000 == 0:
            print(f"        ...esperando ({transcurrido // 60000} min)")

    errs = errores_en_pagina(pg)
    if errs:
        return "error", _tapar(" · ".join(errs))[:220]
    return ("espera_agotada", "no se completó el captcha a tiempo") if con_captcha \
        else ("error", "el formulario no avanzó y no mostró error")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo", default=None, help="clave de una revista: " +
                    ", ".join(r[0] for r in REVISTAS))
    ap.add_argument("--sin-captcha", action="store_true", help="solo las que no piden captcha")
    ap.add_argument("--espera", type=int, default=300, help="segundos de espera por captcha (300)")
    a = ap.parse_args(argv)

    lista = REVISTAS
    if a.solo:
        lista = [r for r in REVISTAS if r[0] == a.solo]
        if not lista:
            raise SystemExit(f"No conozco «{a.solo}». Claves: {[r[0] for r in REVISTAS]}")
    if a.sin_captcha:
        lista = [r for r in lista if not r[3]]

    hay_captcha = any(r[3] for r in lista)
    print("═" * 78)
    print("CREAR CUENTAS EN LOS OJS DE LAS REVISTAS")
    print(f"  Autor: {NOMBRE} {APELLIDOS} · usuario «{USUARIO}» · {CORREO}")
    print(f"  Claves: se generan y se guardan en {CREDENCIALES}")
    print("  Esto crea CUENTAS. No somete ningún manuscrito.")
    if hay_captcha:
        print("  La ventana se abre visible: hay captchas que resuelves tú.")
    print("═" * 78)

    p, ctx, pg = abrir(headless=not hay_captcha)
    resultados = []
    try:
        for rev in lista:
            clave_rev, nombre, url, con_captcha, nota = rev
            print(f"\n▸ {nombre}   {'[captcha]' if con_captcha else '[automática]'}")
            print(f"    {nota}")
            estado, detalle = registrar(pg, rev, a.espera)
            simbolo = {"ok": "OK ", "ya": "YA ", "error": "ERR", "espera_agotada": "···"}[estado]
            print(f"    {simbolo} {detalle}")
            resultados.append((nombre, estado, detalle))
    finally:
        cerrar(p, ctx)

    print("\n" + "═" * 78)
    print("RESUMEN")
    for nombre, estado, detalle in resultados:
        print(f"  {estado.upper():<14} {nombre}")
    ok = sum(1 for _, e, _ in resultados if e in ("ok", "ya"))
    print(f"\n  {ok} de {len(resultados)} con cuenta.")
    if any(e == "ok" for _, e, _ in resultados):
        print(f"  Las claves están en {CREDENCIALES} (fuera del repositorio).")
        print("  Pendiente en cada cuenta: meter el ORCID en el perfil "
              "(0009-0003-6598-432X); OJS no lo pide al registrarse.")
        print("  Revisa el correo: OJS suele mandar un mensaje de validación.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
