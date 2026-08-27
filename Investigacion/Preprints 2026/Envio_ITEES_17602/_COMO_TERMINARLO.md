# Cómo terminar el envío 596 de ITEES

El envío **existe y está a medias**. Lo que falta son dos clics y pegar metadatos que ya están
escritos aquí abajo. **No hay que volver a subir nada.**

**Panel:** <https://revistaseidec.com/index.php/ITEES/submission/wizard/2?submissionId=596>
Usuario `jcastanoe` · clave en `%LOCALAPPDATA%\revistas-cun\credenciales.json`

## Lo que ya está hecho

| Paso | Estado |
|---|---|
| 1 · Inicio | **completo** — sección *Artículos de Reflexión* (id 18), idioma español, lista de comprobación marcada y **el preprint 17602 declarado por escrito** en «Comentarios al editor» |
| 2 · Archivos | **subidos los tres**: `1486` Manuscript_blinded.docx · `1487` Title_page.docx · `1488` Carta_de_presentacion.docx |
| 2 · Tipo de archivo | **FALTA** — es lo único que bloquea |
| 3 · Metadatos | pendiente (el texto está más abajo, listo para pegar) |
| 4 · Confirmación | pendiente |

## Lo único que bloquea

Cada archivo pide «¿Qué tipo de archivo es?». Hay que pulsar, en la página del paso 2:

| Archivo | Pulsar |
|---|---|
| `Manuscript_blinded.docx` | **Texto del artículo** |
| `Title_page.docx` | **Otro** |
| `Carta_de_presentacion.docx` | **Otro** |

Después, **Guardar y continuar**.

> **Por qué no lo hizo la herramienta.** Ese botón es un componente Vue que no reacciona a clics
> automatizados, y la vía de la API (`PUT /api/v1/submissions/596/files/<id>` con
> `{"genreId": 37}` para «Texto del artículo» o `48` para «Otro») **devuelve HTTP 403**: el servidor
> bloquea la escritura por API. Los identificadores quedan anotados por si sirven más adelante.
> Tras unos quince accesos automatizados el sitio **dejó de aceptar conexiones** de esta máquina
> (el dominio resuelve, pero las conexiones expiran), así que conviene esperar un rato antes de
> volver a entrar, y hacerlo a mano.

## Paso 3 · Metadatos, listos para pegar

**Título (español)**

```
Una arquitectura de repositorio como fuente única para la autoría de material docente asistida por IA: informe de experiencia en cinco asignaturas de pregrado y posgrado
```

**Título (inglés)**

```
A Repository-as-Source-of-Truth Architecture for AI-Assisted Course Material Authoring: An Experience Report from Five Undergraduate and Graduate Courses
```

El resumen en español (223 palabras) y en inglés (245) están **tal cual** en el manuscrito
`Preprint_AI_Assisted_Course_Authoring.md`, en las secciones `## RESUMEN` y `## ABSTRACT`. Se pegan
sin cambios: ITEES no declara límite de palabras para el resumen.

**Palabras clave (español)**

```
autoría asistida por IA, tecnología educativa, fuente única de verdad, reproducibilidad, diseño instruccional, educación superior
```

**Keywords (English)**

```
AI-assisted authoring, educational technology, single source of truth, reproducibility, instructional design, higher education
```

**Referencias:** las 19 del manuscrito están en `_citas.txt`, una por párrafo, por si ITEES pide un
campo de citas aparte como hace EDU REVIEW. En el paso 3 de ITEES **no apareció** ese campo.

## Antes de pulsar «Finalizar envío»

Comprobar en el panel del autor que el título y el resumen quedaron guardados de verdad. En EDU
REVIEW el formulario del paso 3 **se pinta vacío al recargarlo aunque haya guardado**, y eso hace
creer que se perdió todo; lo que vale es el panel del autor, no el formulario.
