# Calendario — Investigación Ciencia y Tecnología — Escuela de Ingenierías
**Grupo 53339** · Horario: **Jueves, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela).
> CSV/ICS **sin invitados** estudiantes. Description corta; Location vacío hasta Meet real.

| # | Fecha | Tipo | Subject (Calendar) |
|---|---|---|---|
| 1 | 13/08/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 01 |
| 2 | 20/08/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 02 |
| 3 | 27/08/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 03 |
| 4 | 03/09/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 04 |
| 5 | 10/09/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 05 |
| 6 | 17/09/2026 (jue) | Sincrónica | 53339 - Investigación Ciencia y Tecnología - Sesion 06 |

## Fechas institucionales
- **53339** (26P03): inicio 10/08/2026 · recepción 12/09/2026 · cierre **20/09/2026**
- Cierre considerado en este archivo Calendar: **20/09/2026**
- Eventos generados: **6**
- Archivos: `Encuentros INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA - Grupo 53339 - Importar a Calendar.csv` / `Encuentros INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA - Grupo 53339 - Importar a Calendar.ics`

## Cómo importar (sin invitados · description corta)
1. Google Calendar → Configuración → Importar → `.ics` o `.csv`.
2. **No incluye estudiantes** (Pregrado no lleva Guests/ATTENDEE).
3. Location vacío: tras importar, añade Meet (mismo enlace en toda la serie) y publícalo en CDigital.
4. Subject corto: grupos - asignatura - Sesion NN. Description = una línea con el tema.
5. Placeholder Meet de referencia (no va en el ICS): [URL Meet — mismo enlace toda la serie · INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA].

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
