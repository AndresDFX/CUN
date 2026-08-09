# -*- coding: utf-8 -*-
"""Crea eventos Proyecto I 54ES4 vía Google Calendar API CON attendees.

Preferido si ya tienes OAuth local. Si no: usa el Apps Script
`Crear encuentros con invitados.gs` (más simple en cuenta CUN).

Setup (una vez):
1. Google Cloud Console → proyecto → habilitar «Google Calendar API».
2. Credenciales → OAuth client ID (Desktop) → descarga JSON.
3. Guarda como: config/slides/secrets/credentials.json
   (carpeta secrets/ no versionar; crea si no existe).
4. pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
5. python config/slides/create_encuentros_p1_calendar_api.py

Primera ejecución abre el navegador; guarda token en
config/slides/secrets/token_calendar_p1.json.

Datos: se construyen en memoria desde el roster ODS + sesiones_cun
(mismo origen que build_calendar_proyecto1_54es4.py; sin JSON intermedio).

Por defecto NO envía notificaciones (sendUpdates=none).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Raíz del workspace derivada del propio archivo. Antes estaba hardcodeada como
# «G:\\Mi unidad\\...» y rompía cuando Google Drive monta la unidad en inglés
# («G:\\My Drive»). Corregido 2026-08-09.
_WS = Path(__file__).resolve().parents[2]


ROOT = (_WS)
SECRETS = Path(__file__).resolve().parent / "secrets"
CREDENTIALS = SECRETS / "credentials.json"
TOKEN = SECRETS / "token_calendar_p1.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_calendar_proyecto1_54es4 import build_calendar_payload  # noqa: E402


def _load_service():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as e:
        raise SystemExit(
            "Faltan paquetes. Instala:\n"
            "  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2\n"
            f"Detalle: {e}"
        ) from e

    if not CREDENTIALS.is_file():
        raise SystemExit(
            f"No está {CREDENTIALS}.\n"
            "Crea OAuth Desktop en Google Cloud, descarga el JSON y guárdalo ahí.\n"
            "Alternativa sin API: pegar Crear encuentros con invitados.gs en script.google.com"
        )

    SECRETS.mkdir(parents=True, exist_ok=True)
    creds = None
    if TOKEN.is_file():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return build("calendar", "v3", credentials=creds)


def main() -> None:
    payload = build_calendar_payload()
    service = _load_service()
    cal_id = payload.get("calendar_id") or "primary"
    guests = [{"email": e} for e in payload["guests"]]
    send_updates = payload.get("send_updates") or "none"
    created = 0
    for ev in payload["events"]:
        body = {
            "summary": ev["subject"],
            "description": ev["description"],
            "location": payload.get("location") or "",
            "start": {"dateTime": ev["start"], "timeZone": ev["timezone"]},
            "end": {"dateTime": ev["end"], "timeZone": ev["timezone"]},
            "attendees": guests,
            "guestsCanModify": False,
            "guestsCanInviteOthers": False,
            "guestsCanSeeOtherGuests": True,
        }
        service.events().insert(
            calendarId=cal_id,
            body=body,
            sendUpdates=send_updates,
        ).execute()
        created += 1
        print(f"  + {ev['subject']}")
    print(
        f"OK {created} eventos en {cal_id} · "
        f"attendees={len(guests)} · sendUpdates={send_updates}"
    )


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
