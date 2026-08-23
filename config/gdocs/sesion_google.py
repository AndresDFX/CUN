# -*- coding: utf-8 -*-
r"""
La sesión de Google con la que se comentan los documentos. Se abre una vez y se reutiliza.

POR QUÉ UN PERFIL DE CHROME Y NO UN TOKEN
-----------------------------------------
Comentar un documento ajeno por API exige el alcance amplio `drive` y **no existe un alcance de
solo comentar** (ver `VIABILIDAD_COMENTARIOS_GOOGLE_DOCS.md` §4). Con Playwright no hace falta
ninguna autorización: se usa la sesión del navegador, la misma que el Docente ya tiene. Lo que se
guarda en disco no es una llave a todo el Drive, es una sesión de navegador que caduca sola y que se
revoca cerrando sesión.

Y hay una razón técnica que decide la implementación, ya comprobada en este repositorio (ver
`Investigacion/dashboard/synapse.py` y el commit «Importar la sesion de Synapse del Chrome del
propio usuario»):

    El SSO de Google NO se completa en el Chromium empaquetado de Playwright: detecta marcas de
    automatización y deja la ventana sin autenticar.

Por eso aquí se usa **Chrome de verdad** (`channel="chrome"`), un **perfil persistente propio** y
`--disable-blink-features=AutomationControlled`. El perfil es propio y no el del usuario a propósito:
los perfiles no comparten sesión, y abrir el perfil de siempre lo bloquearía mientras Chrome esté
abierto.

DÓNDE VIVEN LOS SECRETOS
------------------------
En `%LOCALAPPDATA%\gdocs-cun\`, **fuera del repositorio**, que está en git y sincronizado a Google
Drive. Nunca escribas usuario ni clave en un archivo de aquí.

    credenciales.json   {"usuario": "...", "clave": "..."}   ← opcional, solo autocompleta
    perfil/             el perfil de Chrome con la sesión    ← esto es lo que evita re-entrar

La clave es **opcional**: si el archivo no está, la ventana se abre igual y la escribes tú. Lo que de
verdad hace falta para las corridas siguientes es el perfil.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))) / "gdocs-cun"
PERFIL = BASE / "perfil"
CREDENCIALES = BASE / "credenciales.json"

CUENTA_ESPERADA = "julian_castanoe@cun.edu.co"

# Chrome real y sin la marca de automatización: con el Chromium empaquetado el SSO no pasa.
ARGS_CHROME = [
    "--disable-blink-features=AutomationControlled",
    "--no-first-run",
    "--no-default-browser-check",
]


def credenciales() -> dict:
    """`{'usuario': ..., 'clave': ...}` si el archivo está. Nunca se imprime la clave."""
    if not CREDENCIALES.is_file():
        return {}
    try:
        d = json.loads(CREDENCIALES.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"No pude leer {CREDENCIALES}: {e}")
    return {"usuario": (d.get("usuario") or "").strip(), "clave": d.get("clave") or ""}


def _sin_clave(t: str) -> str:
    """Tapa la clave si por accidente llega a un mensaje. Los registros los lee otra gente."""
    c = credenciales().get("clave")
    return t.replace(c, "********") if c else t


def _escribir(pg, selectores: list[str], valor: str, *, espera: int = 15000) -> None:
    """Escribe en el primero de `selectores` que exista y sea visible. Nunca informa del valor."""
    ultimo = ""
    for sel in selectores:
        try:
            campo = pg.locator(sel).first
            campo.wait_for(state="visible", timeout=espera)
            campo.fill(valor)
            return
        except Exception as e:
            ultimo = str(e).splitlines()[0]
    raise RuntimeError(f"ningún campo de {selectores} quedó visible: {ultimo}")


def abrir(*, headless: bool = True, viewport: tuple[int, int] = (1600, 1000)):
    """Abre el perfil persistente. Devuelve `(playwright, contexto, pagina)`; ciérralo con `cerrar`.

    `headless=False` es obligatorio para iniciar sesión y **recomendado para comentar**: Google Docs
    es una aplicación de lienzo y en headless el foco y el teclado se comportan distinto.
    """
    from playwright.sync_api import sync_playwright

    PERFIL.mkdir(parents=True, exist_ok=True)
    p = sync_playwright().start()
    try:
        ctx = p.chromium.launch_persistent_context(
            str(PERFIL),
            channel="chrome",
            headless=headless,
            viewport={"width": viewport[0], "height": viewport[1]},
            args=ARGS_CHROME,
            locale="es-CO",
            timezone_id="America/Bogota",
        )
    except Exception as e:
        p.stop()
        if "channel" in str(e) or "chrome" in str(e).lower():
            raise SystemExit(
                "No encontré Google Chrome instalado. Hace falta Chrome de verdad: en el Chromium\n"
                "de Playwright, Google no deja completar el inicio de sesión.\n"
                f"Detalle: {_sin_clave(str(e).splitlines()[0])}"
            )
        raise
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    return p, ctx, pg


def cerrar(p, ctx) -> None:
    """Cierra sin romperse si la ventana ya no está (el usuario pudo cerrarla a mano)."""
    for accion in (lambda: ctx.close(), lambda: p.stop()):
        try:
            accion()
        except Exception:
            pass


def cuenta_activa(pg) -> str | None:
    """El correo con el que está iniciada la sesión, o `None`. No navega si ya estás en Docs."""
    try:
        pg.goto("https://myaccount.google.com/", wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(1500)
        # El correo aparece en varios sitios de la página; el más estable es el texto plano.
        cuerpo = pg.evaluate("() => document.body.innerText || ''")
        for linea in cuerpo.splitlines():
            t = linea.strip()
            if "@" in t and " " not in t and "." in t.split("@")[-1]:
                return t.lower()
    except Exception:
        return None
    return None


def sesion_viva(pg, *, doc_id: str | None = None) -> bool:
    """¿Sirve la sesión? Se comprueba contra lo que de verdad importa, no contra la página de cuenta.

    Si se da un `doc_id`, se prueba el documento: es la única comprobación que no miente, porque una
    sesión puede estar viva y aun así no tener acceso a ese documento.
    """
    url = (f"https://docs.google.com/document/d/{doc_id}/edit" if doc_id
           else "https://drive.google.com/drive/my-drive")
    try:
        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(2500)
    except Exception:
        return False
    actual = pg.url
    return "accounts.google.com" not in actual and "ServiceLogin" not in actual


def login(*, espera: int = 300, cuenta: str | None = None) -> int:
    """Abre Chrome para iniciar sesión y deja la sesión en el perfil. Idempotente."""
    esperada = (cuenta or CUENTA_ESPERADA).strip().lower()
    cred = credenciales()
    p, ctx, pg = abrir(headless=False)
    try:
        if sesion_viva(pg):
            quien = cuenta_activa(pg)
            print(f"Ya había sesión en el perfil{f' ({quien})' if quien else ''}. No hay nada que hacer.")
            if quien and esperada not in quien:
                print(f"AVISO: la sesión es de «{quien}», no de «{esperada}».")
                print("       Cierra sesión en la ventana y vuelve a ejecutar login.")
                return 1
            return 0

        print(f"Se abrió Chrome. Inicia sesión con  {esperada}")
        if cred.get("clave"):
            print(f"Autocompleto el correo y la clave desde {CREDENCIALES}.")
        else:
            print("No hay clave guardada: escríbela tú en la ventana. (Es lo más seguro.)")
        print("Si Google pide verificación en dos pasos, atiéndela en la ventana.")
        print(f"Espero hasta {espera} s.\n")

        try:
            pg.goto("https://accounts.google.com/ServiceLogin?service=wise",
                    wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(2000)
            # El correo NO es un input[type=email]: es `#identifierId` (type=text, name=identifier).
            # Y en esa misma página hay un input[type=password] OCULTO, así que hay que pedir el
            # visible o se rellena el equivocado y el paso de la clave se queda esperando.
            if cred.get("usuario"):
                _escribir(pg, ["#identifierId", 'input[name="identifier"]'], cred["usuario"])
                pg.keyboard.press("Enter")
                pg.wait_for_timeout(4000)
            if cred.get("clave"):
                _escribir(pg, ['input[name="Passwd"]', 'input[type="password"]:visible'],
                          cred["clave"], espera=25000)
                pg.keyboard.press("Enter")
                pg.wait_for_timeout(5000)
        except Exception as e:
            print(f"   (no pude autocompletar; hazlo tú en la ventana) {_sin_clave(str(e).splitlines()[0])[:120]}")

        # Esperar sin adivinar: se sondea el destino real cada 3 s hasta que la sesión sirva.
        transcurrido = 0
        while transcurrido < espera * 1000:
            try:
                if "accounts.google.com" not in pg.url:
                    if sesion_viva(pg):
                        break
                pg.wait_for_timeout(3000)
            except Exception as e:
                if "closed" in str(e).lower():
                    print("\nSe cerró la ventana. Compruebo si la sesión quedó guardada...")
                    break
                pg.wait_for_timeout(3000)
            transcurrido += 3000
            if transcurrido % 30000 == 0:
                print(f"   ...esperando ({transcurrido // 1000}s)")
        else:
            print("\nSe agotó la espera sin sesión. Vuelve a ejecutar login.")
            return 1
    finally:
        cerrar(p, ctx)

    # Comprobar en frío, con una ventana nueva: es la única prueba de que el perfil quedó bien.
    p, ctx, pg = abrir(headless=True)
    try:
        if sesion_viva(pg):
            quien = cuenta_activa(pg)
            print(f"\nOK  sesión guardada en {PERFIL}")
            if quien:
                print(f"    cuenta: {quien}")
                if esperada not in quien:
                    print(f"    AVISO: esperaba «{esperada}».")
                    return 1
            return 0
        print("\nLa sesión NO quedó en el perfil. Vuelve a ejecutar login y no cierres la ventana.")
        return 1
    finally:
        cerrar(p, ctx)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Iniciar o comprobar la sesión de Google del Docente.")
    ap.add_argument("orden", choices=["login", "estado"], help="login: abre Chrome · estado: solo comprueba")
    ap.add_argument("--espera", type=int, default=300, help="segundos de espera en login (300)")
    ap.add_argument("--cuenta", default=None)
    ap.add_argument("--doc", default=None, help="id de documento con el que probar el acceso en «estado»")
    a = ap.parse_args()

    if a.orden == "login":
        raise SystemExit(login(espera=a.espera, cuenta=a.cuenta))

    p, ctx, pg = abrir(headless=True)
    try:
        if sesion_viva(pg, doc_id=a.doc):
            quien = cuenta_activa(pg)
            print(f"Sesión viva{f' · {quien}' if quien else ''}")
            if a.doc:
                print(f"Acceso al documento {a.doc}: sí")
            raise SystemExit(0)
        print("No hay sesión (o no hay acceso a ese documento).")
        print(f"Corre:  python config/gdocs/sesion_google.py login")
        raise SystemExit(1)
    finally:
        cerrar(p, ctx)
