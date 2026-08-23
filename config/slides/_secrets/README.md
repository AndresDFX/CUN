# Secretos OAuth — aquí ya NO va nada

Esta carpeta se queda vacía a propósito. Los secretos de Google viven **fuera del repositorio**,
que está en git y sincronizado a Google Drive, igual que `cdigital-cun` y `synapse-cun`:

| Para qué | Dónde |
|---|---|
| Calendar API (`create_encuentros_p1_calendar_api.py`) | `%LOCALAPPDATA%\gcal-cun\credentials.json` · `token_calendar_p1.json` |

Comentar los documentos de los estudiantes **no usa OAuth ni guarda ningún token**: se hace con
Apps Script, que corre con la sesión de la propia cuenta. Ver
`LEEME - Comentar documentos de estudiantes.md`.

**Por qué se movieron (2026-08-20):** el script apuntaba a `config/slides/secrets/` —sin guion
bajo—, y el `.gitignore` solo cubre `_secrets/`. Un token guardado ahí **habría entrado a git** y de
ahí a Drive. El `.gitignore` tampoco impide la sincronización con Drive, así que ni `_secrets/`
servía: la única ubicación correcta está fuera del árbol del repositorio.

Flujo preferido sin OAuth: Apps Script
`Especializacion/Proyecto I/2026/54ES4/Crear encuentros con invitados.gs`
