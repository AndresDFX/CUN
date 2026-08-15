# -*- coding: utf-8 -*-
"""Conector a **Synapse CUN** — https://dashboard-investigaciones.web.app/

Plataforma institucional de seguimiento de investigación de la CUN. Este módulo le da al
agente `escritor-investigacion-cun` la capacidad de leer los datos reales de la plataforma
(en especial los **pendientes de Producción**) en vez de pedírselos al usuario.

CÓMO FUNCIONA (y por qué así)
-----------------------------
La app es una SPA de Firebase (proyecto ``sapiolab-48252``) con inicio de sesión **Google SSO
restringido al dominio ``cun.edu.co``** y datos en Cloud Firestore. Eso impone dos cosas:

1. **El inicio de sesión lo hace SIEMPRE la persona, nunca el script.** El subcomando ``login``
   abre Chrome real, en un perfil dedicado y persistente, y espera a que el usuario complete el
   SSO de Google con sus propias credenciales. Este archivo no pide, no recibe y no guarda
   contraseñas en ningún momento. Google además bloquea el SSO en navegadores automatizados
   genéricos: por eso se usa Chrome de verdad (``channel="chrome"``) y no el Chromium empaquetado.
2. **Después del login no se necesita navegador.** De la sesión se extrae el *refresh token* de
   Firebase, y con él se piden tokens de acceso frescos para consultar la API REST de Firestore.
   Leer la API directamente es más fiable y más completo que raspar el DOM, y no depende de que
   la interfaz no cambie.

DÓNDE QUEDAN LAS COSAS
----------------------
El *refresh token* es una credencial de verdad: da acceso a la cuenta institucional hasta que se
revoque. **Nunca se escribe dentro de este repositorio** (que está en git y sincronizado a Google
Drive). Vive en ``%LOCALAPPDATA%\\synapse-cun\\``, junto con el perfil de Chrome. Los datos
descargados sí van a ``Investigacion/dashboard/datos/``, que está en ``.gitignore`` porque puede
contener información de terceros.

USO
---
    python Investigacion/dashboard/synapse.py login        # una sola vez (abre Chrome)
    python Investigacion/dashboard/synapse.py estado       # ¿hay sesión válida? ¿de quién?
    python Investigacion/dashboard/synapse.py pendientes   # informe de pendientes de Producción
    python Investigacion/dashboard/synapse.py calendario   # CSV de eventos: alerta + fecha exacta
    python Investigacion/dashboard/synapse.py recopilar     # volcado completo de lo accesible

Para revocar el acceso: ``python Investigacion/dashboard/synapse.py cerrar`` borra el token y el
perfil local. La sesión de Google se revoca aparte, desde la cuenta del usuario.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sys
from datetime import date, datetime, timedelta, timezone
from typing import Any

import requests

# --- Constantes de la plataforma, descubiertas del bundle público de la app -------------------
URL_APP = "https://dashboard-investigaciones.web.app/"
API_KEY = "AIzaSyASDOiqZZtcQlGzzVgi7nrrtW1VOoK4OYo"
PROJECT_ID = "sapiolab-48252"
FUNCIONES = f"https://us-central1-{PROJECT_ID}.cloudfunctions.net/dashboard_docentes"
FIRESTORE = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"
CUENTA_ESPERADA = "julian_castanoe@cun.edu.co"

# Colecciones del modelo de datos de Synapse.
#   products  -> un documento POR DOCENTE (id = uid), con un arreglo `products` dentro.
#   users     -> un documento por usuario (id = uid); se consulta por `email ==`.
COL_POR_DOCENTE = "products"
COLECCIONES_GLOBALES = [
    "users",
    "produccion_investigacion",
    "proyectos_investigacion",
    "grupos_investigacion",
    "estadisticas_semilleros",
    "estadisticas_profesores_semilleros",
    "estadisticas_detallado_estudiantes_semilleros",
]
ENDPOINTS_FUNCIONES = ["years", "year-vmax", "sheet-data", "cvlac-formacion"]

# --- Rutas locales: credenciales FUERA del repositorio ---------------------------------------
BASE_LOCAL = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "synapse-cun")
PERFIL_CHROME = os.path.join(BASE_LOCAL, "perfil-chrome")
ARCHIVO_CRED = os.path.join(BASE_LOCAL, "credenciales.json")

_AQUI = os.path.dirname(os.path.abspath(__file__))
DIR_DATOS = os.path.join(_AQUI, "datos")

ESTADOS_ABIERTOS = {"pendiente", "vencida", "vencido"}


# =============================================================================================
# Credenciales
# =============================================================================================
def _guardar_credenciales(datos: dict) -> None:
    os.makedirs(BASE_LOCAL, exist_ok=True)
    with open(ARCHIVO_CRED, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    try:  # best-effort en Windows: quitar herencia y dejar solo al usuario actual
        os.system(f'icacls "{ARCHIVO_CRED}" /inheritance:r /grant:r "%USERNAME%":F >nul 2>&1')
    except Exception:
        pass


def _leer_credenciales() -> dict | None:
    if not os.path.isfile(ARCHIVO_CRED):
        return None
    with open(ARCHIVO_CRED, encoding="utf-8") as f:
        return json.load(f)


def token_de_acceso() -> tuple[str, dict]:
    """Cambia el refresh token por un ID token fresco (válido ~1 hora)."""
    cred = _leer_credenciales()
    if not cred:
        raise SystemExit(
            "No hay sesión guardada.\n"
            "Ejecuta primero:  python Investigacion/dashboard/synapse.py login"
        )
    r = requests.post(
        f"https://securetoken.googleapis.com/v1/token?key={API_KEY}",
        data={"grant_type": "refresh_token", "refresh_token": cred["refreshToken"]},
        timeout=45,
    )
    if not r.ok:
        raise SystemExit(
            f"El refresh token ya no sirve ({r.status_code}). La sesión fue revocada o expiró.\n"
            f"Vuelve a ejecutar:  python Investigacion/dashboard/synapse.py login\n"
            f"Detalle: {r.text[:300]}"
        )
    d = r.json()
    return d["id_token"], cred


# =============================================================================================
# login — Chrome real, perfil persistente, el usuario escribe sus propias credenciales
# =============================================================================================
JS_LEER_AUTH = """
async () => {
  const abrir = (nombre) => new Promise((res, rej) => {
    const q = indexedDB.open(nombre);
    q.onsuccess = () => res(q.result);
    q.onerror = () => rej(q.error);
  });
  let db;
  try { db = await abrir('firebaseLocalStorageDb'); } catch (e) { return null; }
  if (!db.objectStoreNames.contains('firebaseLocalStorage')) return null;
  const filas = await new Promise((res) => {
    const q = db.transaction('firebaseLocalStorage', 'readonly')
                .objectStore('firebaseLocalStorage').getAll();
    q.onsuccess = () => res(q.result || []);
    q.onerror = () => res([]);
  });
  for (const fila of filas) {
    const k = fila && fila.fbase_key ? String(fila.fbase_key) : '';
    if (k.startsWith('firebase:authUser:')) return fila.value || null;
  }
  return null;
}
"""


def _ventana_cerrada(e: Exception) -> bool:
    """¿La excepción es «cerraron la ventana», y no un fallo real?"""
    t = f"{type(e).__name__} {e}".lower()
    return "targetclosed" in t or "has been closed" in t


def _cerrar(ctx) -> None:
    try:
        ctx.close()
    except Exception:
        pass          # si ya la cerró el usuario, cerrarla otra vez no es un error


def _auth_del_perfil(p) -> dict | None:
    """Lee la sesión del perfil en disco, sin pedirle nada más al usuario.

    El contexto de Chrome es **persistente**: si el SSO llegó a completarse, Firebase dejó la
    sesión en la IndexedDB del perfil y sigue ahí aunque la ventana se haya cerrado. Así que
    cerrar la ventana a mitad del proceso no obliga a repetir el inicio de sesión: se vuelve a
    abrir el perfil —esta vez sin interfaz, porque aquí no hay nada que teclear— solo para leerla.
    """
    try:
        ctx = p.chromium.launch_persistent_context(
            PERFIL_CHROME, channel="chrome", headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
    except Exception as e:
        print(f"   no pude reabrir el perfil para comprobarlo: {str(e)[:200]}")
        return None
    try:
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(URL_APP, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(3000)
        return pg.evaluate(JS_LEER_AUTH)
    except Exception as e:
        print(f"   no pude leer el perfil: {str(e)[:200]}")
        return None
    finally:
        _cerrar(ctx)


def cmd_login(args) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Falta Playwright.  Instálalo con:  pip install playwright", file=sys.stderr)
        return 2

    os.makedirs(PERFIL_CHROME, exist_ok=True)
    esperada = (args.cuenta or CUENTA_ESPERADA).strip().lower()

    print("Se abrirá Chrome en la página de Synapse CUN.")
    print(f"Inicia sesión con Google usando  {esperada}")
    print("Este script NO ve ni guarda tu contraseña: la escribes tú en la ventana de Google.")
    print(f"Esperando hasta {args.espera} segundos...\n")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PERFIL_CHROME,
            channel="chrome",          # Chrome real: Google bloquea el SSO en navegadores automatizados
            headless=False,
            viewport={"width": 1440, "height": 950},
            args=["--disable-blink-features=AutomationControlled"],
        )
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(URL_APP, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(2500)

        # Si ya hay sesión en el perfil, no hay nada que hacer.
        auth = pg.evaluate(JS_LEER_AUTH)
        if not auth:
            # Preseleccionar rol y lanzar el SSO; si la UI cambió, el usuario lo hace a mano.
            for etiqueta in (args.rol, "Continuar con Google"):
                try:
                    pg.get_by_role("button", name=etiqueta, exact=False).first.click(timeout=6000)
                    pg.wait_for_timeout(1200)
                except Exception:
                    print(f"   (no pude pulsar «{etiqueta}» automáticamente; hazlo tú en la ventana)")

        # `--espera 0` significa esperar sin límite: la ventana se queda ahí hasta que el usuario
        # entre o la cierre. Es lo cómodo cuando no se sabe cuándo va a poder atenderla.
        esperado_ms = args.espera * 1000 if args.espera else float("inf")
        transcurrido = 0
        cerrada = False
        while auth is None and transcurrido < esperado_ms:
            try:
                pg.wait_for_timeout(2000)
                auth = pg.evaluate(JS_LEER_AUTH)
            except Exception as e:
                if _ventana_cerrada(e):
                    cerrada = True
                    break
                auth = None       # navegación en curso (redirección de Google)
            transcurrido += 2000
            if transcurrido % 60000 == 0 and auth is None:
                print(f"   ...esperando el inicio de sesión ({transcurrido // 1000}s)")

        if cerrada:
            # No es un error: quizá inició sesión y cerró la ventana enseguida.
            print("\nSe cerró la ventana. Compruebo si la sesión quedó en el perfil...")
            _cerrar(ctx)
            auth = _auth_del_perfil(p)

        if not auth:
            print("\nNo se detectó sesión. Nada se guardó.", file=sys.stderr)
            if cerrada:
                print("   (la ventana se cerró antes de completar el inicio de sesión en Google)",
                      file=sys.stderr)
            _cerrar(ctx)
            return 1

        gestor = auth.get("stsTokenManager") or {}
        refresh = gestor.get("refreshToken")
        if not refresh:
            print("\nSesión detectada pero sin refresh token utilizable.", file=sys.stderr)
            _cerrar(ctx)
            return 1

        correo = (auth.get("email") or "").lower()
        print(f"\nSesión detectada: {correo}  (uid {auth.get('uid')})")
        if esperada and correo != esperada:
            print(f"AVISO: esperaba {esperada} y la sesión es de {correo}.")
            print("       Se guarda igual, pero verifica que sea la cuenta correcta.")

        _guardar_credenciales({
            "email": correo,
            "uid": auth.get("uid"),
            "displayName": auth.get("displayName"),
            "refreshToken": refresh,
            "guardado": datetime.now(timezone.utc).isoformat(),
        })
        print(f"Credencial guardada FUERA del repositorio, en:\n   {ARCHIVO_CRED}")
        _cerrar(ctx)

    print("\nListo. Ya no hace falta el navegador; usa:")
    print("   python Investigacion/dashboard/synapse.py calendario")
    return 0


def cmd_cerrar(args) -> int:
    borrado = []
    if os.path.isfile(ARCHIVO_CRED):
        os.remove(ARCHIVO_CRED)
        borrado.append(ARCHIVO_CRED)
    if os.path.isdir(PERFIL_CHROME) and args.perfil:
        shutil.rmtree(PERFIL_CHROME, ignore_errors=True)
        borrado.append(PERFIL_CHROME)
    print("Borrado:\n   " + "\n   ".join(borrado) if borrado else "No había nada guardado.")
    print("\nEsto elimina el acceso local. Para revocar el permiso en la cuenta de Google, "
          "hazlo desde https://myaccount.google.com/permissions")
    return 0


# =============================================================================================
# Firestore REST
# =============================================================================================
def _decodificar(v: Any) -> Any:
    """Convierte un `Value` tipado de la API REST de Firestore a JSON plano."""
    if not isinstance(v, dict):
        return v
    if "stringValue" in v:
        return v["stringValue"]
    if "integerValue" in v:
        return int(v["integerValue"])
    if "doubleValue" in v:
        return v["doubleValue"]
    if "booleanValue" in v:
        return v["booleanValue"]
    if "nullValue" in v:
        return None
    if "timestampValue" in v:
        return v["timestampValue"]
    if "referenceValue" in v:
        return v["referenceValue"]
    if "mapValue" in v:
        return {k: _decodificar(x) for k, x in (v["mapValue"].get("fields") or {}).items()}
    if "arrayValue" in v:
        return [_decodificar(x) for x in (v["arrayValue"].get("values") or [])]
    if "geoPointValue" in v or "bytesValue" in v:
        return v.get("geoPointValue") or v.get("bytesValue")
    return v


def _doc_a_dict(doc: dict) -> dict:
    plano = {k: _decodificar(v) for k, v in (doc.get("fields") or {}).items()}
    plano["_id"] = (doc.get("name") or "").rsplit("/", 1)[-1]
    return plano


def obtener_documento(tok: str, ruta: str) -> dict | None:
    r = requests.get(f"{FIRESTORE}/{ruta}", headers={"Authorization": f"Bearer {tok}"}, timeout=60)
    if r.status_code == 404:
        return None
    if r.status_code == 403:
        return {"_error": "permiso denegado por las reglas de seguridad"}
    r.raise_for_status()
    return _doc_a_dict(r.json())


def listar_coleccion(tok: str, coleccion: str, limite: int = 3000) -> list[dict] | dict:
    """Lista una colección completa, paginando. Devuelve {'_error': ...} si las reglas lo niegan."""
    salida: list[dict] = []
    token_pag = None
    while True:
        params = {"pageSize": 300}
        if token_pag:
            params["pageToken"] = token_pag
        r = requests.get(f"{FIRESTORE}/{coleccion}", params=params,
                         headers={"Authorization": f"Bearer {tok}"}, timeout=90)
        if r.status_code == 403:
            return {"_error": "permiso denegado por las reglas de seguridad"}
        if r.status_code == 404:
            return {"_error": "la colección no existe o no es visible"}
        r.raise_for_status()
        cuerpo = r.json()
        salida.extend(_doc_a_dict(d) for d in cuerpo.get("documents", []))
        token_pag = cuerpo.get("nextPageToken")
        if not token_pag or len(salida) >= limite:
            break
    return salida


def llamar_funcion(tok: str, ruta: str) -> Any:
    try:
        r = requests.get(f"{FUNCIONES}/dashboard-docentes/{ruta}",
                         headers={"Authorization": f"Bearer {tok}"}, timeout=90)
        if not r.ok:
            return {"_error": f"HTTP {r.status_code}", "_cuerpo": r.text[:400]}
        try:
            return r.json()
        except ValueError:
            return {"_texto": r.text[:2000]}
    except requests.RequestException as e:
        return {"_error": str(e)[:300]}


# =============================================================================================
# Análisis de productos
# =============================================================================================
def _lista_productos(doc: dict) -> list[dict]:
    """El campo `products` puede venir como arreglo o como mapa (la app maneja ambos)."""
    p = doc.get("products")
    if isinstance(p, list):
        return [x for x in p if isinstance(x, dict)]
    if isinstance(p, dict):
        return [x for x in p.values() if isinstance(x, dict)]
    return []


def _a_fecha(fecha: str | None) -> date | None:
    """La fecha de un campo de Synapse, o None si no se puede leer.

    Las fechas de entrega llegan como `YYYY-MM-DD` (la app hace
    `new Date(deliveryDate + "T00:00:00")`), pero `deliveredAt` y `lastActivity` son ISO con hora.
    Se acepta cualquiera de las dos formas y se descarta lo demás sin romperse.
    """
    if not fecha:
        return None
    t = str(fecha).strip()
    for intento in (t[:19].replace("Z", ""), t[:10]):
        try:
            return datetime.fromisoformat(intento).date()
        except ValueError:
            continue
    return None


def _iso(fecha: str | None) -> str:
    """La fecha en `YYYY-MM-DD`, o cadena vacía si no hay o no se entiende."""
    f = _a_fecha(fecha)
    return f.isoformat() if f else ""


def _vencido(fecha: str | None) -> bool:
    f = _a_fecha(fecha)
    return bool(f and f < datetime.now().date())


def analizar_productos(doc: dict) -> dict:
    productos = _lista_productos(doc)
    resumen = {"total": len(productos), "abiertos": [], "cerrados": [], "por_estado": {}}
    for pr in productos:
        estado = str(pr.get("status") or "sin estado")
        resumen["por_estado"][estado] = resumen["por_estado"].get(estado, 0) + 1

        hitos = pr.get("partialMilestones") or []
        hitos = hitos if isinstance(hitos, list) else list(hitos.values())
        hitos_abiertos = [
            {
                "titulo": h.get("title") or h.get("name") or h.get("id"),
                "estado": h.get("status"),
                "fecha_limite": h.get("dueDate"),
                "vencido": _vencido(h.get("dueDate")),
                "notas": h.get("assignmentNotes"),
            }
            for h in hitos
            if isinstance(h, dict) and str(h.get("status", "")).lower() in ESTADOS_ABIERTOS
        ]

        ficha = {
            "producto": pr.get("productName") or pr.get("title") or pr.get("id"),
            "tipo": pr.get("productType") or pr.get("tipoProducto"),
            "categoria_minciencias": pr.get("categoriaMinciencias") or pr.get("categoryId"),
            "estado": estado,
            "fecha_limite": pr.get("deliveryDate") or pr.get("dueDate"),
            "vencido": _vencido(pr.get("deliveryDate") or pr.get("dueDate")),
            "entregado": pr.get("deliveredAt"),
            "observacion_admin": pr.get("adminFeedback"),
            "hitos_abiertos": hitos_abiertos,
            "ultima_actividad": pr.get("lastActivity"),
        }
        destino = "abiertos" if (estado.lower() in ESTADOS_ABIERTOS or hitos_abiertos) else "cerrados"
        resumen[destino].append(ficha)

    resumen["abiertos"].sort(key=lambda x: (not x["vencido"], str(x["fecha_limite"] or "9999")))
    return resumen


# =============================================================================================
# Eventos de calendario del apartado «Producción»
# =============================================================================================
# Synapse NO tiene colección de calendario: el apartado de Producción arma sus eventos a partir
# de los productos del docente. Cada producto aporta un evento por su **entrega final**
# (`deliveryDate`) y uno por cada **hito parcial** (`partialMilestones[].dueDate` + `title`). Es
# exactamente el mismo par de fuentes que usa el panel de administración para su
# «Reporte_Entregas.xlsx», donde cada fila sale marcada `Tipo: Final` o como hito.
#
# `Rechazado` cuenta como pendiente: el producto volvió al docente y hay que reentregarlo.
ESTADOS_REQUIEREN_ACCION = ESTADOS_ABIERTOS | {"rechazado"}


def eventos_calendario(doc: dict, dias_alerta: int = 7, hoy: date | None = None) -> list[dict]:
    """Un evento por fecha de entrega, con su fecha de alerta `dias_alerta` días antes.

    Devuelve la lista ordenada por fecha de entrega. Los eventos sin fecha legible se conservan
    —son un hallazgo, no basura: un hito sin `dueDate` no se puede vigilar— y se van al final.
    """
    hoy = hoy or datetime.now().date()
    eventos: list[dict] = []

    for pr in _lista_productos(doc):
        producto = pr.get("productName") or pr.get("title") or pr.get("id") or "(sin nombre)"
        categoria = pr.get("categoriaMinciencias") or pr.get("categoryId") or ""

        crudas = [("Entrega final", "", pr.get("deliveryDate") or pr.get("dueDate"),
                   str(pr.get("status") or ""), pr.get("deliveredAt"), pr.get("documentUrl"))]
        hitos = pr.get("partialMilestones") or []
        hitos = hitos if isinstance(hitos, list) else list(hitos.values())
        for i, h in enumerate(x for x in hitos if isinstance(x, dict)):
            crudas.append(("Hito parcial", h.get("title") or h.get("name") or f"Hito {i + 1}",
                           h.get("dueDate"), str(h.get("status") or ""),
                           h.get("deliveredAt"), h.get("documentUrl")))

        for tipo, hito, fecha_txt, estado, entregado, url in crudas:
            f = _a_fecha(fecha_txt)
            vacia = not str(fecha_txt or "").strip()
            if tipo == "Entrega final" and vacia:
                continue   # un producto sin fecha final no es un evento; un hito sin fecha SÍ lo
                           # es, y sale marcado «SIN FECHA»: un hito que no se puede vigilar
                           # es justo lo que hay que ver en el informe.
            accion = estado.lower() in ESTADOS_REQUIEREN_ACCION
            alerta = f - timedelta(days=dias_alerta) if f else None
            eventos.append({
                "producto": producto,
                "categoria_minciencias": categoria,
                "tipo": tipo,
                "hito": hito,
                "estado": estado or "(sin estado)",
                "fecha_entrega": f.isoformat() if f else "",
                "fecha_alerta": alerta.isoformat() if alerta else "",
                "dias_para_entrega": (f - hoy).days if f else "",
                "requiere_accion": "sí" if accion else "no",
                # Lo que de verdad se mira cada mañana: ¿ya entré en la ventana de 7 días?
                "alerta_activa": "sí" if (accion and alerta and alerta <= hoy) else "no",
                # Una fecha ausente y una fecha ilegible no son lo mismo: la segunda es un dato
                # roto en la plataforma —Synapse la lee con `new Date(fecha+"T00:00:00")`, así
                # que allí también sale «Invalid Date»— y se muestra tal como vino para poder
                # corregirla. No se adivina si `20/08/2026` es día/mes o mes/día.
                "situacion": ("SIN FECHA" if vacia else
                              f"FECHA ILEGIBLE: {str(fecha_txt).strip()}" if not f else
                              "VENCIDO" if (accion and f < hoy) else
                              "cerrado" if not accion else
                              f"faltan {(f - hoy).days} días"),
                "entregado_el": _iso(entregado),
                "documento": url or "",
                "fecha_entrega_cruda": str(fecha_txt or ""),
            })

    eventos.sort(key=lambda e: (e["fecha_entrega"] == "", e["fecha_entrega"],
                                e["tipo"] != "Hito parcial", e["hito"]))
    return eventos


COLUMNAS_CSV = ["producto", "categoria_minciencias", "tipo", "hito", "estado",
                "fecha_alerta", "fecha_entrega", "dias_para_entrega",
                "alerta_activa", "requiere_accion", "situacion", "entregado_el", "documento"]


def escribir_csv(eventos: list[dict], ruta: str, sep: str = ",") -> str:
    """El CSV de revisión: una fila por evento, con la fecha de alerta y la fecha exacta.

    Se escribe en `utf-8-sig` (con BOM) porque sin él Excel en Windows abre las tildes como
    «Producción», y `newline=""` para que no salgan filas en blanco entre líneas.
    """
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS_CSV, delimiter=sep, extrasaction="ignore")
        w.writeheader()
        w.writerows(eventos)
    return ruta


def escribir_csv_google(eventos: list[dict], ruta: str) -> str:
    """CSV importable en Google Calendar, con dos eventos por entrega.

    La importación por CSV de Google Calendar **no sabe crear recordatorios**, así que la alerta
    de 7 días no puede viajar como propiedad del evento: se crea como un evento propio en la
    fecha de alerta («Revisar»), y el día del vencimiento va otro («ENTREGA»). Las fechas van en
    `MM/DD/YYYY`, que es el formato que exige el importador, y el separador es coma obligatoria.

    Solo entran los eventos que requieren acción: importar vencimientos ya aprobados llenaría el
    calendario de ruido pasado.
    """
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    cols = ["Subject", "Start Date", "All Day Event", "Description", "Private"]

    def mmddyyyy(iso: str) -> str:
        d = _a_fecha(iso)
        return d.strftime("%m/%d/%Y") if d else ""

    filas = []
    for e in eventos:
        if e["requiere_accion"] != "sí" or not e["fecha_entrega"]:
            continue
        que = f"{e['producto']}" + (f" — {e['hito']}" if e["hito"] else "")
        desc = (f"Synapse CUN · {e['tipo']} · estado: {e['estado']}"
                f" · vence {e['fecha_entrega']}"
                + (f" · categoría {e['categoria_minciencias']}" if e["categoria_minciencias"] else "")
                + (f" · {e['documento']}" if e["documento"] else ""))
        if e["fecha_alerta"]:
            filas.append({"Subject": f"[Revisar 7d] {que}", "Start Date": mmddyyyy(e["fecha_alerta"]),
                          "All Day Event": "True", "Description": desc, "Private": "True"})
        filas.append({"Subject": f"[ENTREGA] {que}", "Start Date": mmddyyyy(e["fecha_entrega"]),
                      "All Day Event": "True", "Description": desc, "Private": "True"})

    with open(ruta, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=",")
        w.writeheader()
        w.writerows(filas)
    return ruta


# =============================================================================================
# Subcomandos de consulta
# =============================================================================================
def cmd_estado(args) -> int:
    cred = _leer_credenciales()
    if not cred:
        print("Sin sesión guardada. Ejecuta:  python Investigacion/dashboard/synapse.py login")
        return 1
    tok, cred = token_de_acceso()
    print(f"Sesión válida: {cred['email']}  (uid {cred['uid']})")
    print(f"Guardada el:   {cred.get('guardado')}")
    yo = obtener_documento(tok, f"users/{cred['uid']}")
    if yo and "_error" not in yo:
        print("\nMi ficha en la plataforma:")
        for k in ("email", "role", "displayName", "escuela", "estado", "isActive", "isDocente", "blocked"):
            if k in yo:
                print(f"   {k}: {yo[k]}")
    elif yo:
        print(f"\nMi ficha en `users`: {yo['_error']}")
    else:
        print("\nNo existe documento `users/<uid>` para esta cuenta.")
    return 0


def _escribir(nombre: str, datos: Any) -> str:
    os.makedirs(DIR_DATOS, exist_ok=True)
    ruta = os.path.join(DIR_DATOS, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    return ruta


def cmd_pendientes(args) -> int:
    tok, cred = token_de_acceso()
    doc = obtener_documento(tok, f"{COL_POR_DOCENTE}/{cred['uid']}")
    if doc is None:
        print("No existe documento de productos para esta cuenta "
              f"(`{COL_POR_DOCENTE}/{cred['uid']}`).")
        print("En la plataforma eso significa que aún no hay productos asignados a este docente.")
        return 0
    if "_error" in doc:
        print(f"No pude leer los productos: {doc['_error']}")
        return 1

    an = analizar_productos(doc)
    _escribir("productos_propios.json", doc)
    _escribir("pendientes_produccion.json", an)

    lineas = [
        "# Pendientes de Producción — Synapse CUN",
        "",
        f"Cuenta: **{cred['email']}** · consultado el {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Fuente: colección `{COL_POR_DOCENTE}`, documento `{cred['uid']}` "
        f"(proyecto Firebase `{PROJECT_ID}`).",
        "",
        f"**{an['total']}** productos registrados · **{len(an['abiertos'])}** con algo abierto "
        f"· **{len(an['cerrados'])}** cerrados.",
        "",
        "Conteo por estado: " + (", ".join(f"{k}: {v}" for k, v in sorted(an["por_estado"].items()))
                                 or "(ninguno)"),
        "",
    ]
    if an["abiertos"]:
        lineas += ["## Abiertos (vencidos primero)", "",
                   "| Producto | Tipo | Estado | Fecha límite | ¿Vencido? | Hitos abiertos |",
                   "|---|---|---|---|---|---|"]
        for p in an["abiertos"]:
            hitos = "; ".join(
                f"{h['titulo']} ({h['estado']}"
                + (f", vence {h['fecha_limite']}" if h["fecha_limite"] else "")
                + (" — VENCIDO" if h["vencido"] else "") + ")"
                for h in p["hitos_abiertos"]
            ) or "—"
            lineas.append(
                f"| {p['producto']} | {p['tipo'] or '—'} | {p['estado']} | "
                f"{p['fecha_limite'] or '—'} | {'**SÍ**' if p['vencido'] else 'no'} | {hitos} |"
            )
        lineas.append("")
        for p in an["abiertos"]:
            if p["observacion_admin"]:
                lineas.append(f"- **{p['producto']}** — observación del administrador: "
                              f"{p['observacion_admin']}")
        lineas.append("")
    else:
        lineas += ["## Abiertos", "", "No hay productos pendientes ni vencidos.", ""]

    if an["cerrados"]:
        lineas += ["## Cerrados", "", "| Producto | Estado | Entregado |", "|---|---|---|"]
        lineas += [f"| {p['producto']} | {p['estado']} | {p['entregado'] or '—'} |"
                   for p in an["cerrados"]]
        lineas.append("")

    md = os.path.join(DIR_DATOS, "Pendientes de Produccion.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print("\n".join(lineas))
    print(f"\n---\nEscrito: {md}")
    return 0


def cmd_calendario(args) -> int:
    tok, cred = token_de_acceso()
    doc = obtener_documento(tok, f"{COL_POR_DOCENTE}/{cred['uid']}")
    if doc is None:
        print("No existe documento de productos para esta cuenta "
              f"(`{COL_POR_DOCENTE}/{cred['uid']}`): no hay nada que calendarizar.")
        return 0
    if "_error" in doc:
        print(f"No pude leer los productos: {doc['_error']}")
        return 1

    hoy = datetime.now().date()
    eventos = eventos_calendario(doc, dias_alerta=args.alerta, hoy=hoy)
    if not eventos:
        print("Los productos no traen ninguna fecha de entrega ni hito: no hay eventos.")
        return 0

    ruta = args.csv or os.path.join(DIR_DATOS, "eventos_produccion.csv")
    escribir_csv(eventos, ruta, sep=args.sep)
    ruta_gc = escribir_csv_google(
        eventos, os.path.splitext(ruta)[0] + "_google_calendar.csv")
    _escribir("eventos_produccion.json", eventos)

    accionables = [e for e in eventos if e["requiere_accion"] == "sí"]
    print(f"Cuenta: {cred['email']} · hoy {hoy.isoformat()} · alerta {args.alerta} días antes")
    print(f"{len(eventos)} eventos ({len(accionables)} requieren acción) de "
          f"{len(_lista_productos(doc))} productos\n")

    anchos = [46, 13, 12, 12, 13, 22]
    cab = ("producto / hito", "tipo", "alerta", "ENTREGA", "estado", "situación")
    print("  ".join(t[:a].ljust(a) for t, a in zip(cab, anchos)))
    print("  ".join("-" * a for a in anchos))
    for e in eventos:
        que = e["producto"] + (f" » {e['hito']}" if e["hito"] else "")
        fila = (que, "Final" if e["tipo"] == "Entrega final" else "Hito",
                e["fecha_alerta"] or "—", e["fecha_entrega"] or "—",
                e["estado"], e["situacion"])
        marca = "  <-- ALERTA" if e["alerta_activa"] == "sí" else ""
        print("  ".join(str(t)[:a].ljust(a) for t, a in zip(fila, anchos)) + marca)

    activas = [e for e in eventos if e["alerta_activa"] == "sí"]
    print(f"\ncon alerta activa hoy (dentro de los {args.alerta} días, o ya vencido): "
          f"{len(activas)}")

    # Lo que NO se puede vigilar hay que decirlo: sin fecha legible no hay alerta posible, y
    # estos eventos tampoco entran al CSV de Google Calendar.
    sin_fecha = [e for e in eventos if not e["fecha_entrega"]]
    if sin_fecha:
        print(f"\n!!! {len(sin_fecha)} evento(s) SIN fecha utilizable: no generan alerta ni "
              f"entran al CSV de Calendar.")
        for e in sin_fecha:
            print(f"       {e['producto']}{' » ' + e['hito'] if e['hito'] else ''} "
                  f"[{e['estado']}] -> {e['situacion']}")

    print(f"\nCSV de revisión:      {ruta}")
    print(f"CSV para Calendar:    {ruta_gc}")
    print("   (la importación por CSV de Google Calendar no crea recordatorios: la alerta va "
          "como\n    un evento propio «[Revisar 7d]» en la fecha de alerta.)")
    return 0


def cmd_recopilar(args) -> int:
    tok, cred = token_de_acceso()
    print(f"Sesión: {cred['email']} (uid {cred['uid']})\n")
    inventario: dict[str, Any] = {
        "_consultado": datetime.now(timezone.utc).isoformat(),
        "_cuenta": cred["email"],
        "_proyecto": PROJECT_ID,
    }

    yo = obtener_documento(tok, f"users/{cred['uid']}")
    inventario["mi_usuario"] = yo
    print(f"users/{cred['uid']}: {'OK' if yo and '_error' not in yo else yo}")

    prod = obtener_documento(tok, f"{COL_POR_DOCENTE}/{cred['uid']}")
    inventario["mis_productos"] = prod
    if prod and "_error" not in prod:
        inventario["mis_pendientes"] = analizar_productos(prod)
        print(f"{COL_POR_DOCENTE}/{cred['uid']}: {inventario['mis_pendientes']['total']} productos, "
              f"{len(inventario['mis_pendientes']['abiertos'])} abiertos")
    else:
        print(f"{COL_POR_DOCENTE}/{cred['uid']}: {prod}")

    if args.todo:
        print("\nBarrido de colecciones globales (--todo):")
        for col in COLECCIONES_GLOBALES:
            res = listar_coleccion(tok, col)
            inventario[col] = res
            n = len(res) if isinstance(res, list) else res.get("_error")
            print(f"   {col}: {n}")
    else:
        print("\n(Se omiten las colecciones globales: pueden contener datos de terceros.")
        print(" Usa  --todo  si de verdad necesitas el barrido completo.)")

    print("\nCloud Functions:")
    for ep in ENDPOINTS_FUNCIONES:
        res = llamar_funcion(tok, ep)
        inventario[f"funcion_{ep}"] = res
        marca = res.get("_error") if isinstance(res, dict) and "_error" in res else "OK"
        print(f"   {ep}: {marca}")

    ruta = _escribir("inventario_synapse.json", inventario)
    print(f"\nEscrito: {ruta}")
    return 0


# =============================================================================================
def main(argv: list[str]) -> int:
    try:  # la consola de Windows llega en cp1252 y parte de esta salida no cabe ahí
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(
        description="Conector a Synapse CUN (dashboard-investigaciones.web.app).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("login", help="Abrir Chrome e iniciar sesión con Google (una sola vez)")
    p.add_argument("--cuenta", default=CUENTA_ESPERADA, help="Correo institucional esperado")
    p.add_argument("--rol", default="Docente", help="Rol a preseleccionar (Docente/Administrador)")
    p.add_argument("--espera", type=int, default=300, help="Segundos de espera para el SSO")
    p.set_defaults(func=cmd_login)

    p = sub.add_parser("estado", help="Verificar la sesión guardada y la ficha propia")
    p.set_defaults(func=cmd_estado)

    p = sub.add_parser("pendientes", help="Informe de pendientes de Producción (lo habitual)")
    p.set_defaults(func=cmd_pendientes)

    p = sub.add_parser("calendario",
                       help="CSV de los eventos de calendario de Producción (fecha exacta + alerta)")
    p.add_argument("--alerta", type=int, default=7,
                   help="Días antes del vencimiento en que salta la alerta (por omisión 7)")
    p.add_argument("--csv", help="Ruta del CSV (por omisión datos/eventos_produccion.csv)")
    p.add_argument("--sep", default=",",
                   help='Separador de columnas. Usa --sep ";" si Excel te mete todo en una sola')
    p.set_defaults(func=cmd_calendario)

    p = sub.add_parser("recopilar", help="Volcado de todo lo accesible de la plataforma")
    p.add_argument("--todo", action="store_true",
                   help="Incluir colecciones globales (puede traer datos de terceros)")
    p.set_defaults(func=cmd_recopilar)

    p = sub.add_parser("cerrar", help="Borrar la credencial local")
    p.add_argument("--perfil", action="store_true", help="Borrar también el perfil de Chrome")
    p.set_defaults(func=cmd_cerrar)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
