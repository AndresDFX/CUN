# Calendario — Trabajo de Grado 2 — Modelos de Innovación (Ing. Sistemas)
**Grupo 54448** · Horario: **Lunes, 5:00 pm – 6:00 pm (1 hora sincrónica)**

> **Subject Calendar:** `{grupos} - {Asignatura} - Sesion NN` (fuente: `config/cursos/sesiones_cun.py`). Festivo → mismo patrón + `(autónoma)`. Sin tema largo.
> Regla general Pregrado: si la fecha cae en **festivo colombiano**, la sesión se cursa como **clase autónoma** (no se cancela).
> CSV/ICS **sin invitados** estudiantes. Description corta; Location vacío hasta Meet real.

| # | Fecha | Tipo | Subject (Calendar) |
|---|---|---|---|
| 1 | 10/08/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 01 |
| 2 | 17/08/2026 (lun) | Autónoma (Asunción de la Virgen) | 54448 - Trabajo de Grado 2 - Clase autonoma (Asunción de la Virgen) |
| 3 | 24/08/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 02 |
| 4 | 31/08/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 03 |
| 5 | 07/09/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 04 |
| 6 | 14/09/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 05 |
| 7 | 21/09/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 06 |
| 8 | 28/09/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 07 |
| 9 | 05/10/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 08 |
| 10 | 12/10/2026 (lun) | Autónoma (Día de la Raza) | 54448 - Trabajo de Grado 2 - Clase autonoma (Día de la Raza) |
| 11 | 19/10/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 09 |
| 12 | 26/10/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 10 |
| 13 | 02/11/2026 (lun) | Autónoma (Todos los Santos) | 54448 - Trabajo de Grado 2 - Clase autonoma (Todos los Santos) |
| 14 | 09/11/2026 (lun) | Sincrónica | 54448 - Trabajo de Grado 2 - Sesion 11 |
| 15 | 16/11/2026 (lun) | Autónoma (Independencia de Cartagena) | 54448 - Trabajo de Grado 2 - Clase autonoma (Independencia de Cartagena) |

## Fechas institucionales
- **54448** (26V04): inicio 10/08/2026 · recepción 14/11/2026 · cierre **22/11/2026**
- Cierre considerado en este archivo Calendar: **22/11/2026**
- Eventos generados: **15**
- Archivos: `Encuentros TRABAJO DE GRADO 2 - Grupo 54448 - Importar a Calendar.csv` / `Encuentros TRABAJO DE GRADO 2 - Grupo 54448 - Importar a Calendar.ics`

## Cómo importar (sin invitados · description corta)
1. Google Calendar → Configuración → Importar → `.ics` o `.csv`.
2. **No incluye estudiantes** (Pregrado no lleva Guests/ATTENDEE).
3. Location vacío: tras importar, añade Meet (mismo enlace en toda la serie) y publícalo en CDigital.
4. Subject corto: grupos - asignatura - Sesion NN. Description = una línea con el tema.
5. Placeholder Meet de referencia (no va en el ICS): [URL Meet — mismo enlace toda la serie · TRABAJO DE GRADO 2].

Regenerar (sin PPTX): `python config/slides/build_pregrado_cursos.py --calendar-only`
