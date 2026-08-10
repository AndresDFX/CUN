# Calendario de clases — PROYECTO I · Periodo 26ES4
Especialización en Inteligencia Artificial

> ⚠️ **Este archivo se corrigió** con el **cronograma oficial** (`Cronograma_Proyecto_I_II_Especializaciones_26ES4.pdf`, Coordinación de Gestión del Conocimiento) recibido después de la primera versión. Los pesos reales por ítem son **25% + 25% + 42% + 4% coevaluación + 4% autoevaluación**; sumados dan los tres cortes que el aula declara (**25 / 25 / 50**).
>
> 🔁 **Actualizado el 2026-08-10 con la auditoría del aula (CDigital).** El libro de calificaciones nombra los ítems **distinto** de nuestro material: el corte 1 es un **Quiz** (cuestionario, 25%), lo que el material llama ACA 2 es la **ACA 1** del aula y el anteproyecto final es la **ACA FINAL**. La **coevaluación es un foro** (se participa) y la **autoevaluación un cuestionario**. **Las fechas no cambiaron** — siguen siendo las de Coordinación. Fuente cargada en `config/cursos/fechas_entrega_aca.py` → `VENTANAS["proyecto1"]`.

## ✅ Horario CONFIRMADO: lunes, 8:00–10:00 pm (2 horas)
Cumple el `Instructivo_encuentros_sincronicos_Especializaciones_AFI.pdf`: franja 19:00-22:00h ✓, duración 1h30-2h ✓, coincide además con la "sugerencia" del propio portal (20:00-22:00h). *(Se descarta la alerta anterior de horario 5-6pm — quedó resuelta.)*

> 📌 **El CONTENIDO NUEVO de cada sesión se prepara para ~1 hora** (el bloque de enseñanza: teoría + modelación). La **2ª hora del encuentro de 2h se reserva para tutoría/taller en vivo** con los equipos (revisión de avances, dudas puntuales) — así que el guion docente de cada sesión trae solo ~60 min de contenido estructurado; el resto del tiempo es acompañamiento flexible, no material nuevo que preparar.

## 🔴 ALERTA PENDIENTE: ACA 3 (42%, el entregable más grande) solo tiene 2 lunes de clase disponibles
Cruzando el cronograma oficial con los festivos colombianos de 2026, la ventana de ACA 3 (12/10–08/11) pierde **2 de sus 4 lunes** por festivo (12/10 Día de la Raza, 02/11 Todos los Santos trasladado). Quedan únicamente **19/10 y 26/10** como sesiones sincrónicas para todo el diseño metodológico + integración del anteproyecto final. **Recomendación:** adelanta contenido de metodología en las sesiones "puente" de ACA2 (05/10) y refuerza con tutorías adicionales durante esas semanas — no dependas solo de las 2 sesiones sincrónicas para ese tramo.

---

## 📅 Cronograma OFICIAL (fuente: Coordinación de Gestión del Conocimiento)

| Actividad (material) | Ítem en el aula (CDigital) | Tipo en el aula | Apertura | Cierre | Fecha límite nota | % | Corte | Última sincrónica antes del cierre |
|---|---|---|---|---|---|---|---|---|
| **ACA 1** — Primer avance del anteproyecto | **Quiz** | Cuestionario | lun 03/08/2026 | dom 30/08/2026 | lun 07/09/2026 | **25%** | I | **S02** (24/08) |
| **ACA 2** — Segundo avance del anteproyecto | **ACA 1** | Tarea | lun 07/09/2026 | dom 04/10/2026 | lun 12/10/2026 | **25%** | II | **S07** (28/09) |
| **ACA 3** — Anteproyecto (final) | **ACA FINAL** | Tarea | lun 12/10/2026 | dom 08/11/2026 | lun 16/11/2026 | **42%** | III | **S10** (26/10) |
| **Coevaluación** (no es ACA) | **Coevaluación** | **Foro** | lun 09/11/2026 | dom 15/11/2026 | dom 22/11/2026 | **4%** | III | **S11** (09/11) |
| **Autoevaluación** (no es ACA) | **Autoevaluación** | Cuestionario | lun 16/11/2026 | dom 22/11/2026 | dom 22/11/2026 | **4%** | III | **S11** (09/11) · 16/11 es festivo |

> **Ningún ítem cierra en día de clase**: las ventanas de Coordinación cierran en **domingo** y el día de clase es **lunes**. Por eso la última columna marca la última sesión sincrónica útil antes de cada cierre, en vez de «la sesión en que cae».
> Los **tres cortes del aula** (I=25%, II=25%, III=50% = ACA FINAL 42% + coev. 4% + autoev. 4%) están confirmados en el libro de calificaciones (auditoría 2026-08-10) y no dejan de ser **nota única** para efectos del Reglamento Estudiantil (Art. 41).
> A diferencia de pregrado, Proyecto I **no tiene quices ni parciales adicionales**: su único cuestionario evaluativo del primer corte es el **Quiz** (25%) que en el material se enuncia como ACA 1.
> **Fecha oficial de cierre y registro de TODAS las calificaciones: domingo 22 de noviembre de 2026.** No te guíes por recordatorios de Moodle — pueden estar desactualizados; esa es la única fecha válida (comunicada directamente por la Coordinación).

## 🚫 Lunes SIN clase (festivos colombianos 2026 en el periodo)
| Fecha | Festivo | Cae en ventana de |
|---|---|---|
| 17/08/2026 | Asunción de la Virgen (trasladado del sáb. 15/08) | ACA 1 |
| 12/10/2026 | Día de la Raza y la Diversidad Étnica | ACA 3 |
| 02/11/2026 | Todos los Santos (trasladado del dom. 01/11) | ACA 3 |
| 16/11/2026 | Independencia de Cartagena (trasladado del mié. 11/11) | Autoevaluación (fecha límite de nota ACA3, no día de clase) |

> Instructivo de encuentros sincrónicos, sección 3: en lunes festivo, **NO se hace sincrónico**. Opción principal = clase pregrabada disponible en Moodle; opción excepcional = reprogramar (solo por coincidencia con festivo, avisando con anticipación).

## 📚 Las sesiones de clase reales (lunes) — alineadas a ESP329

Fuente de las **fechas de sesión**: `config/cursos/sesiones_cun.py` → `COURSES["proyecto1"]["sesiones"]` (la misma que alimenta el CSV/ICS de encuentros que se importa a Calendar). Fuente **curricular**: `Especializacion_En_Inteligencia_Artificial_Proyecto_I_ESP329.docx` (7 unidades).

> ✅ **Corregido el 2026-08-09:** esta tabla estaba **desfasada una sesión** (arrancaba el 03/08, lunes anterior al inicio del periodo, lo que contradecía el «Inicio del periodo: 10/08/2026» de este mismo archivo). Ya está alineada con la fuente. Las fechas de ACA y la tabla «Cronograma OFICIAL» **no se tocaron**.

| # | Fecha | Bloque | Unidad ESP329 | Contenido |
|---|---|---|---|---|
| 1 | **10/08/2026** | Encuadre | — (U1 → lectura autónoma) | **Presentación del curso · docente · estudiantes · ACAs.** No se dicta tema: se presentan el curso, el Docente, los estudiantes (rompehielos en Padlet) y las ACAs (qué se entrega, peso, cómo se entrega). ⚠️ **La U1 (Fundamentos y enfoque de investigación) pasa a LECTURA AUTÓNOMA** y se retoma al abrir la Sesión 02. |
| — | *17/08: festivo (Asunción). Sin sincrónico — trabajo autónomo en CDigital.* | | | |
| 2 | **24/08/2026** | ACA 1 | U2 | Problema y pregunta de investigación · líneas IA del programa. **Última sincrónica antes del cierre de ACA 1 (dom 30/08 · en el aula es el ítem «Quiz», cuestionario 25%)** — equipos conformados en CDigital a más tardar esta semana. |
| 3 | **31/08/2026** | ACA 1 | U3 | Objetivos, justificación, alcances y limitaciones. ⚠️ Cae **después** del cierre de ACA 1 (30/08) y **antes** de la fecha límite de nota (07/09): úsela para cerrar coherencia problema ↔ objetivos y preparar la retroalimentación. |
| 4 | **07/09/2026** | ACA 2 (abre) | U4 | Retroalimentación ACA 1 · antecedentes (mín. 6 nacionales/internacionales). |
| 5 | **14/09/2026** | ACA 2 | U4 | Marco teórico. |
| 6 | **21/09/2026** | ACA 2 | U4 | Marco conceptual y marco contextual. |
| 7 | **28/09/2026** | ACA 2 | U4 | Marco legal (si aplica) · citación APA 7. **Última sincrónica antes del cierre de ACA 2 (dom 04/10 · en el aula es el ítem «ACA 1», tarea 25%).** |
| 8 | **05/10/2026** | Puente ACA2→ACA3 | U5 | Diseño metodológico: paradigma, enfoque y alcance — última sesión antes de los festivos de ACA 3. |
| — | *12/10: festivo (Día de la Raza). Sin sincrónico.* | | | |
| 9 | **19/10/2026** | ACA 3 (#1 de 2) | U5 | Población/muestra, técnicas e instrumentos (**propuestos, NO aplicados**). Tutoría extra recomendada. |
| 10 | **26/10/2026** | ACA 3 (#2 de 2) | U6–U7 | Planeación, viabilidad e integración del anteproyecto. **Última sincrónica antes del cierre de ACA 3 (dom 08/11 · en el aula es el ítem «ACA FINAL», tarea 42%).** |
| — | *02/11: festivo (Todos los Santos). Sin sincrónico.* | | | |
| 11 | **09/11/2026** | Cierre | U7 | Integración y evaluación · **coevaluación** (foro, 09–15/11) y **autoevaluación** (cuestionario, 16–22/11). Es la **única** sesión para explicar ambas ventanas: **última sesión sincrónica** (16/11 es festivo). |
| — | *16/11 y 22/11: sin sincrónico (16/11 festivo); trabajo autónomo en CDigital hasta el cierre del 22/11.* | | | |

**Total: 11 sesiones sincrónicas = los 11 lunes no festivos del periodo (10/08 → 09/11).** Cuadra exacto: entre el 10/08 y el 22/11 hay **15 lunes**; menos los **4 festivos** (17/08, 12/10, 02/11, 16/11) quedan **11**. No sobra ni falta ningún lunes.

## 🎯 Fechas institucionales resumen
- Inicio del periodo: **10/08/2026**
- Fecha máxima de recepción de trabajos (informativa, portal): **14/11/2026**
- **Cierre oficial y registro de notas: 22/11/2026** (única fecha válida)
- Créditos/horas: 2
- Informe Final de Curso: dentro de los **3 días hábiles siguientes** al cierre.

## Registro obligatorio de cada sesión/tutoría (dentro de 24h)
Formulario exclusivo del docente titular (NO compartir con estudiantes):
**Registro de Sesiones Sincrónicas y Tutorías Especialización:** https://forms.gle/6t6BXqQ2Kwmivpct8

Ver el **Manual del Docente** en la raíz de PROYECTO I para la guía completa (cómo preparar la sesión, qué le entregas a la universidad, qué te entregan los estudiantes).

## ⚠️ Tabla retirada (contradecía la Cronograma OFICIAL de arriba)

Este archivo tuvo aquí una segunda tabla "Fechas de entrega ACA (regenerables)" calculada por `config/cursos/fechas_entrega_aca.py` asumiendo inicio 10/08/2026, que se desvió de la **Cronograma OFICIAL** (Coordinación, §arriba) en ACA2 (nota 05/10 vs. **12/10** real) y en los cierres de ACA1/ACA3 (31/08/09/11 calculados vs. **30/08/08/11** reales). Se retiró el 2026-08-09 para no tener dos fuentes de fecha en el mismo archivo — **la única tabla de fechas válida es la "📅 Cronograma OFICIAL" de arriba.** **Corregido el 2026-08-09** y **rehecho el 2026-08-10:** esta tabla ES ahora la tabla explícita `VENTANAS["proyecto1"]` de `config/cursos/fechas_entrega_aca.py` (30/08 · 04/10 · 08/11 · coev 15/11 · autoev 22/11), mapeada a los ítems reales del aula en CDigital (Quiz 25% · ACA 1 25% · ACA FINAL 42% · coevaluación 4% en foro · autoevaluación 4%). Ya no existe cálculo por pesos del que desviarse; los builds leen esa tabla.
