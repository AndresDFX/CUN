# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────────────────────
# OBSOLETO — no usar. Archivado el 2026-08-20, nunca se llegó a ejecutar.
#
# Era la «opción A» del informe VIABILIDAD_COMENTARIOS_GOOGLE_DOCS.md: comentar el documento
# del estudiante desde este computador, con un OAuth de escritorio. Se descartó porque exigía
# crear un proyecto en Google Cloud con la cuenta CUN, y además dejaba en disco un token con
# acceso de lectura y escritura a TODO el Drive de esa cuenta.
#
# En su lugar se hizo la «opción C», que no guarda ningún token:
#   LEEME - Comentar documentos de estudiantes.md
#   config/gdocs/plan_comentarios.py + PRINCIPAL - Comentar documentos de estudiantes.gs
#
# Su extracción de criterios vive ahora en config/gdocs/criterios_aca.py.
# ─────────────────────────────────────────────────────────────────────────────
r"""
Comentar en Google Docs el documento de un estudiante, con los criterios de su curso.

QUÉ HACE Y QUÉ NO
-----------------
Hace tres cosas y ninguna más: **lee** el documento que el estudiante compartió, **extrae** los
criterios de evaluación de la guía del ACA que ese mismo estudiante recibió, y **publica
comentarios** en el documento. No pone notas —la nota la pone el Docente— y **no puede modificar
el texto del estudiante**: el código solo llama a `documents.get` y a `comments.create`, nunca a
`documents.batchUpdate`.

Los comentarios salen **a nombre del Docente**, porque el token es del Docente. Decide antes de
publicar si quieres que lleven la nota de que los redactó una IA (`--nota-ia`).

LÍMITE DE GOOGLE, NO DE ESTE SCRIPT
-----------------------------------
Un comentario creado por la API **no queda anclado al texto** dentro de Google Docs: la propia
documentación de Drive dice que los editores de Workspace muestran como *no anclados* los
comentarios anclados por un tercero. Así que el comentario aparece en la barra lateral, no colgado
del párrafo. Por eso cada comentario lleva (a) la **cita literal** del fragmento en
`quotedFileContent` y (b) la sección y el número de párrafo en el encabezado del texto. Es lo más
cerca del comentario anclado que la API permite hoy.

CREDENCIALES
------------
Se leen de ``%LOCALAPPDATA%\gdocs-cun\credenciales.json`` (el OAuth de escritorio descargado de
Google Cloud) y el token se guarda en ``%LOCALAPPDATA%\gdocs-cun\token.json``, **fuera de este
repositorio**, que está en git y sincronizado a Google Drive. Igual que `cdigital-cun` y
`synapse-cun`. El script se niega a arrancar si esa ruta cae dentro del repositorio.

El trabajo del estudiante **tampoco entra al repositorio**: `bajar` lo escribe en
``%LOCALAPPDATA%\gdocs-cun\revisiones\<docId>\``.

Alcance OAuth: ``https://www.googleapis.com/auth/drive`` — uno solo, y es el mínimo posible.
`drive.file` no sirve: solo cubre los archivos que la app creó o que el usuario eligió con el
Picker, y el documento del estudiante no es ninguno de los dos.

USO
---
    python config/gdocs/comentar_documento.py estado
    python config/gdocs/comentar_documento.py criterios --curso proyecto1 --aca aca1
    python config/gdocs/comentar_documento.py bajar "https://docs.google.com/document/d/XXX/edit" \
        --curso proyecto1 --aca aca1
    python config/gdocs/comentar_documento.py publicar XXX --simular
    python config/gdocs/comentar_documento.py publicar XXX --confirmar

`--simular` imprime el comentario exacto que se enviaría y no toca el documento. **Úsalo siempre
primero**: esto lo ve un estudiante. Sin `--confirmar` no se publica nada.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))) / "gdocs-cun"
CREDENCIALES = BASE / "credenciales.json"
TOKEN = BASE / "token.json"
REVISIONES = BASE / "revisiones"
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Carpeta de las guías de ACA de cada curso. Son los .docx que el estudiante ya tiene: los criterios
# con los que se le comenta son, literalmente, los que se le entregaron.
CURSOS = {
    "proyecto1": "Especializacion/Proyecto I",
    "creatividad": "Pregrado/Creatividad y pensamiento innovador",
    "investigacion": "Pregrado/Investigacion en ciencia y tecnologia",
    "tg2": "Pregrado/Trabajo de grado 2",
    "tg3": "Pregrado/Trabajo de grado 3",
}


def _fuera_del_repo() -> None:
    """El repositorio está en git y sincronizado a Drive: ningún secreto puede caer dentro."""
    try:
        BASE.resolve().relative_to(REPO)
    except ValueError:
        return
    raise SystemExit(
        f"ABORTA: {BASE} está dentro del repositorio ({REPO}).\n"
        "Las credenciales van en %LOCALAPPDATA%, nunca en una carpeta que se sube a git y a Drive."
    )


# ─────────────────────────── criterios (sin autenticación) ───────────────────────────

def guias_aca(curso: str) -> list[Path]:
    raiz = REPO / CURSOS[curso] / "Clases" / "Recursos" / "ACAs"
    return sorted(Path(p) for p in glob.glob(str(raiz / "*.docx")))


def criterios(curso: str, aca: str) -> tuple[str, list[str]]:
    """Saca el checklist «Criterios de evaluación» de la guía del ACA.

    `aca` se busca por subcadena en el nombre del archivo («aca1» → «ACA 1 (25%) - …»), porque el
    nombre real lleva el peso dentro y el peso lo decide `fechas_entrega_aca.py`, no este script.
    """
    patron = aca.lower().replace("_", " ").replace("aca", "aca")
    candidatas = [g for g in guias_aca(curso) if patron.replace(" ", "") in
                  g.stem.lower().replace(" ", "").replace("-", "")]
    if not candidatas:
        disponibles = "\n  ".join(g.stem for g in guias_aca(curso)) or "(ninguna)"
        raise SystemExit(f"No hay guía que coincida con «{aca}» en {curso}.\nGuías:\n  {disponibles}")
    guia = candidatas[0]

    from docx import Document
    parrafos = [p.text.strip() for p in Document(str(guia)).paragraphs]
    fuera = None
    items: list[str] = []
    for i, t in enumerate(parrafos):
        if re.search(r"Criterios de evaluaci", t, re.I):
            fuera = i
            continue
        if fuera is None:
            continue
        if t.startswith("[ ]") or t.startswith("[x]"):
            items.append(t[3:].strip())
        elif items and re.match(r"^\d+\.\s+\S", t):
            break  # empezó la sección siguiente
    return guia.stem, items


# ─────────────────────────── Google (autenticado) ───────────────────────────

def servicios():
    _fuera_del_repo()
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as e:
        raise SystemExit(
            "Faltan paquetes:\n"
            "  pip install --user google-api-python-client google-auth-oauthlib google-auth-httplib2\n"
            f"Detalle: {e}"
        ) from e

    if not CREDENCIALES.is_file():
        raise SystemExit(
            f"No está {CREDENCIALES}.\n"
            "Google Cloud Console (con la cuenta CUN) → habilitar «Google Docs API» y «Google Drive\n"
            "API» → Credenciales → ID de cliente OAuth → Aplicación de escritorio → descargar el\n"
            "JSON → guardarlo con ese nombre y en esa ruta."
        )

    BASE.mkdir(parents=True, exist_ok=True)
    creds = None
    if TOKEN.is_file():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Abre el navegador: la contraseña la escribe el Docente en Google, nunca pasa por aquí.
            creds = InstalledAppFlow.from_client_secrets_file(str(CREDENCIALES), SCOPES).run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
        os.chmod(TOKEN, 0o600)
    return build("docs", "v1", credentials=creds), build("drive", "v3", credentials=creds)


def doc_id(url_o_id: str) -> str:
    m = re.search(r"/document/d/([A-Za-z0-9_-]{20,})", url_o_id)
    return m.group(1) if m else url_o_id.strip()


def _parrafos(doc: dict) -> list[dict]:
    """Aplana el documento a párrafos numerados, arrastrando el último encabezado como sección."""
    salida: list[dict] = []
    seccion = ""

    def parrafo(el: dict) -> None:
        nonlocal seccion
        p = el.get("paragraph")
        if not p:
            return
        estilo = p.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        txt = "".join(e.get("textRun", {}).get("content", "") for e in p.get("elements", [])).strip()
        if not txt:
            return
        if estilo.startswith("HEADING") or estilo == "TITLE":
            seccion = txt
        salida.append({"n": len(salida) + 1, "seccion": seccion, "texto": txt})

    def recorrer(contenido: list[dict]) -> None:
        for el in contenido:
            parrafo(el)
            tabla = el.get("table")
            if tabla:
                for fila in tabla.get("tableRows", []):
                    for celda in fila.get("tableCells", []):
                        recorrer(celda.get("content", []))

    recorrer(doc.get("body", {}).get("content", []))
    return salida


def bajar(url_o_id: str, curso: str, aca: str) -> int:
    did = doc_id(url_o_id)
    docs, drive = servicios()

    meta = drive.files().get(
        fileId=did, fields="name,owners(displayName,emailAddress),capabilities(canComment)",
        supportsAllDrives=True,
    ).execute()
    puede = meta.get("capabilities", {}).get("canComment")
    dueno = (meta.get("owners") or [{}])[0]
    print(f"Documento: {meta.get('name')}")
    print(f"   dueño: {dueno.get('displayName')} <{dueno.get('emailAddress')}>")
    print(f"   ¿puedo comentar?: {'SÍ' if puede else 'NO'}")
    if not puede:
        raise SystemExit(
            "El estudiante lo compartió en modo Lector. Pídele acceso de «Comentador» (basta ese;\n"
            "no hace falta Editor) y repite."
        )

    parrafos = _parrafos(docs.documents().get(documentId=did).execute())
    guia, items = criterios(curso, aca)

    destino = REVISIONES / did
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "documento.md").write_text(
        "\n".join(f"[{p['n']:>3}] ({p['seccion']}) {p['texto']}" for p in parrafos),
        encoding="utf-8",
    )
    plan = {
        "docId": did,
        "titulo": meta.get("name"),
        "curso": curso,
        "aca": aca,
        "guia_criterios": guia,
        "criterios": items,
        "comentarios": [
            {"criterio": c, "parrafo": 0, "cita": "", "texto": ""} for c in items
        ],
    }
    ruta_plan = destino / "plan.json"
    if ruta_plan.is_file():
        print(f"   (ya existía un plan.json; se deja intacto en {ruta_plan})")
    else:
        ruta_plan.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK  {len(parrafos)} párrafos · {len(items)} criterios de «{guia}»")
    print(f"    {destino}")
    print("    Rellena `texto` y `parrafo` de cada comentario y luego: publicar "
          f"{did} --simular")
    return 0


def publicar(did: str, simular: bool, confirmar: bool, nota_ia: str | None) -> int:
    ruta = REVISIONES / did / "plan.json"
    if not ruta.is_file():
        raise SystemExit(f"No está {ruta}. Corre primero: bajar <url> --curso <c> --aca <a>")
    plan = json.loads(ruta.read_text(encoding="utf-8"))
    pendientes = [c for c in plan["comentarios"] if c.get("texto", "").strip()]
    if not pendientes:
        raise SystemExit("Ningún comentario tiene `texto`. No hay nada que publicar.")

    docs, drive = (None, None) if simular else servicios()
    parrafos = {}
    if not simular:
        parrafos = {p["n"]: p for p in _parrafos(docs.documents().get(documentId=did).execute())}

    enviados = 0
    for c in pendientes:
        n = int(c.get("parrafo") or 0)
        p = parrafos.get(n, {})
        cita = (c.get("cita") or p.get("texto") or "").strip()
        donde = c.get("seccion") or p.get("seccion") or ""
        cabecera = f"Criterio «{c['criterio']}»"
        if donde:
            cabecera += f" — {donde}"
        if n:
            cabecera += f" (párrafo {n})"
        cuerpo = f"{cabecera}\n\n{c['texto'].strip()}"
        if nota_ia:
            cuerpo += f"\n\n{nota_ia}"

        if simular or not confirmar:
            print(f"\n─── comentario {enviados + 1} ───")
            if cita:
                print(f"cita: «{cita[:160]}{'…' if len(cita) > 160 else ''}»")
            print(cuerpo)
            enviados += 1
            continue

        cuerpo_api = {"content": cuerpo}
        if cita:
            cuerpo_api["quotedFileContent"] = {"mimeType": "text/plain", "value": cita[:1000]}
        drive.comments().create(fileId=did, body=cuerpo_api, fields="id").execute()
        enviados += 1
        print(f"  + {c['criterio']}")

    if simular:
        print(f"\n--simular: {enviados} comentarios NO enviados. El documento queda intacto.")
    elif not confirmar:
        print(f"\nSin --confirmar no se envió nada ({enviados} comentarios listos).")
    else:
        print(f"\nOK {enviados} comentarios publicados en «{plan['titulo']}» a nombre del Docente.")
    return 0


def estado() -> int:
    print(f"repositorio : {REPO}")
    print(f"credenciales: {CREDENCIALES}  {'OK' if CREDENCIALES.is_file() else 'FALTA'}")
    print(f"token       : {TOKEN}  {'OK' if TOKEN.is_file() else 'sin autorizar'}")
    print(f"alcance     : {SCOPES[0]}")
    _fuera_del_repo()
    print("ubicación   : fuera del repositorio (OK)")
    for m in ("googleapiclient", "google_auth_oauthlib", "docx"):
        try:
            __import__(m)
            print(f"paquete     : {m} OK")
        except ImportError:
            print(f"paquete     : {m} FALTA")
    for c in CURSOS:
        print(f"guías {c:<13}: {len(guias_aca(c))} .docx")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("estado", help="Diagnóstico local: credenciales, paquetes y guías. Sin red.")

    p = sub.add_parser("criterios", help="Mostrar el checklist del ACA. Sin red.")
    p.add_argument("--curso", required=True, choices=sorted(CURSOS))
    p.add_argument("--aca", required=True, help="p. ej. aca1, acafinal")

    p = sub.add_parser("bajar", help="Leer el documento y preparar el plan de comentarios")
    p.add_argument("url")
    p.add_argument("--curso", required=True, choices=sorted(CURSOS))
    p.add_argument("--aca", required=True)

    p = sub.add_parser("publicar", help="Publicar los comentarios del plan")
    p.add_argument("doc_id")
    p.add_argument("--simular", action="store_true",
                   help="Imprimir los comentarios exactos SIN tocar el documento")
    p.add_argument("--confirmar", action="store_true", help="Publicar de verdad")
    p.add_argument("--nota-ia", default=None,
                   help="Línea que se añade a cada comentario declarando el uso de IA")

    a = ap.parse_args()
    if a.cmd == "estado":
        return estado()
    if a.cmd == "criterios":
        guia, items = criterios(a.curso, a.aca)
        print(f"{guia}\n")
        for i, c in enumerate(items, 1):
            print(f"  {i}. {c}")
        return 0
    if a.cmd == "bajar":
        return bajar(a.url, a.curso, a.aca)
    return publicar(a.doc_id, a.simular, a.confirmar, a.nota_ia)


if __name__ == "__main__":
    raise SystemExit(main())
