# Proyecto I · 54ES4 · Calendar (mínimo)

## Qué hay aquí
- `Listado estudiantes.ods` — roster (fuente)
- `Correos estudiantes (invitados Calendar).txt` — lista plana
- `Crear encuentros con invitados.gs` — **flujo principal** (sí mete invitados)
- `Encuentros Proyecto I - Importar a Calendar.csv` / `.ics` — fechas/respaldo (Google **no** importa invitados)
- `Entregas y hitos docentes - Importar a Calendar.csv` — deadlines ACA / hitos AFI
- `Correo de bienvenida.docx` · `Informacion.txt` — oferta del grupo

## Qué hacer
1. **Encuentros con invitados:** script.google.com → pegar `Crear encuentros con invitados.gs` → `createEncuentrosP1` (`SEND_INVITES=false` al inicio).
2. **Hitos docentes:** Calendar → Importar el CSV de entregas (sin invitados).
3. Regenerar CSV/ICS/.gs/correos: `python config/slides/build_calendar_proyecto1_54es4.py`
