# Formulario de participación · XIII Semana de la Investigación CUN

Respuestas listas para copiar y pegar. El formulario se envía con la cuenta
`julian_castanoe@cun.edu.co` (ya aparece arriba en el formulario, no hay que cambiar de cuenta).

**Adjunto obligatorio:** `Castaño Espinosa_Julian Andrés.docx` — en esta misma carpeta, ya en el
formato `Apellido_Nombre` que ellos piden y en Word. **Una sola página**, comprobado exportando a
PDF (queda ~28 % de hoja libre, así que la paginación de Word tampoco lo derrama).

Si hay que cambiar el texto, se edita el `.md` hermano —que es la fuente de verdad— y se regenera
con `python _armar_resumen_docx.py`. No usar `config/slides/guion_md_a_docx.py`: sirve para guiones
y fichas, pero con este documento tan corto reparte el texto en dos hojas.

## Campos

| # | Campo | Qué responder |
|---|---|---|
| 1 | Nombres y Apellidos completos * | `Julian Andrés Castaño Espinosa` |
| 2 | Número documento de identidad * | `1144194156` |
| 3 | Correo electrónico * | `julian_castanoe@cun.edu.co` |
| 4 | Número de contacto * | ⚠️ **Falta** — no está en el repositorio y no debe estarlo. Lo pones tú. |
| 5 | País y Ciudad * | `Colombia, Bogotá D.C.` |
| 6 | Institución educativa y cargo * | `Corporación Unificada Nacional de Educación Superior (CUN) — Docente, Escuela de Ingenierías. Especialización en Inteligencia Artificial (Proyecto I) y asignaturas de pregrado en Ingeniería de Sistemas.` |
| 7 | Empresa y cargo * | `N/A` |
| 8 | ¿En cuál evento desea participar? * | **IV Encuentro Internacional de Ingeniería, Tecnología y Transformación** |
| 9 | ¿Cómo desea participar? * | **Expositor/Obra** |
| 10 | ¿Requiere algún apoyo o consideración especial? * | **Sí** (ver texto abajo) |

### Texto para el campo 10, si se abre una casilla de detalle

```
La obra es una plataforma web en funcionamiento, así que la exposición es una demostración en
vivo. Requiero: conexión a internet estable, un punto de energía y una pantalla o proyector
con entrada HDMI. Llevo mi propio equipo portátil. Si no hay internet en el espacio de
exposición, puedo presentarla con video pregrabado.
```

## Por qué ese evento y esa modalidad

**Evento — IV Encuentro Internacional de Ingeniería, Tecnología y Transformación.** Es el que
corresponde a la Escuela desde la que participo, el objeto es un artefacto de ingeniería y el
aporte que se expone es arquitectónico. «Transformación» es además el eje exacto del trabajo.

**Alternativas defendibles, si prefieres otro encuadre:**

- **I Congreso Internacional de Experiencias y Nuevas Formas de Aprender** — si quieres que el
  foco sea pedagógico y no técnico. Es primera edición, así que hay menos competencia por cupo.
- **Emprendimiento** — solo si quieres presentar los cuatro modelos de negocio que ya están
  escritos en `docs/costos/` de ExamLab. Cambiaría por completo el resumen.

**Modalidad — Expositor/Obra.** La plataforma está desplegada y navegable
(<https://examlab.lovable.app>): se puede mostrar funcionando en un stand, que es más
demostrativo que veinte minutos de diapositivas. Si más adelante quieres además la ponencia, la
casilla de participación admite marcar varias.

## Lo que respalda cada afirmación del resumen

Ninguna cifra del resumen es estimada. Todas salen del repositorio `C:\Projects\examlab`:

| Afirmación | Fuente |
|---|---|
| Cuatro roles diferenciados | `README.md` § Roles y permisos (SuperAdmin, Admin, Docente, Estudiante) |
| Calificación asistida en modo inmediato y en cola diferida | `README.md` § Cola IA; `docs/articulo-revista-semillero.md` |
| Detección de similitudes con dos señales independientes | `docs/articulo-revista-semillero.md` (análisis textual por entrega + comparación pareada) |
| Ejecución de código en varios lenguajes | `README.md` § Stack (Python / Java / JavaScript) |
| Asistencia por código rotativo | `README.md` § Asistencia (QR rotativo tipo TOTP) |
| Un curso activo y 93 estudiantes matriculados | `CLAUDE.md` § Tenant FESNA — estado, snapshot 2026-06-08 |
| Batería de pruebas automatizadas | `CLAUDE.md` § Tests — 138 archivos / 2.467 pruebas (2026-08-07) |
| «La IA propone, el docente dispone» | `docs/articulo-revista-semillero.md` § Desarrollo |

## Tres cosas que hay que decidir antes de enviarlo

**1. Los 93 estudiantes no son de la CUN.** Están en el tenant FESNA, con correos
`@lanuevaamerica.edu.co`. El resumen dice «en una institución donde el autor ejerce docencia»
justamente para no atribuirle a la CUN un despliegue que no es suyo. Si en el stand te preguntan
dónde se usa, la respuesta es esa institución, no la CUN. **No la llames «institución aliada»:**
no existe convenio entre las dos.

**2. La cifra es de un censo de junio.** El snapshot del tenant es del 2026-06-08 y lo último
verificado por REST fue el nombre del curso (2026-08-07). Es el único número del resumen: vale
la pena reconsultarlo antes de enviar, con
`node scripts/db-query.mjs "course_enrollments?select=id&course_id=eq.01b397a3-e74f-4f66-becf-c63b643f247f"`.

**3. ExamLab es privado y tuyo.** El repositorio dice «Privado. Todos los derechos reservados.»
Al declarar filiación CUN en un producto de propiedad personal, la universidad podría más adelante
reclamar cotitularidad sobre lo presentado. Es habitual y suele no pasar nada, pero conviene que
la exposición sea explícita en que el desarrollo es previo y externo a la vinculación docente, y
que no se firme ninguna cesión de derechos del evento sin leerla.

## Ojo con la reutilización

`docs/articulo-revista-semillero.md` es un artículo sobre este mismo proyecto, redactado para la
**Revista Semillero 2026**. Nunca se envió, así que reutilizarlo aquí no es doble sometimiento. Pero
si ese envío sigue en pie, un resumen de memorias y un artículo de revista sobre el mismo objeto
deben declararse mutuamente: el resumen de memorias no bloquea la revista, pero la revista sí puede
preguntar por la difusión previa.
