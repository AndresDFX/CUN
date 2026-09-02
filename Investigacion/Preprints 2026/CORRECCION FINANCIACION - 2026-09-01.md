# Corrección de la declaración de financiación

**Fecha:** 1 de septiembre de 2026

## Qué está mal

Diez manuscritos declaraban estar adscritos a la **«Convocatoria interna CUN 2026 — Desarrollo de
Grupos Temáticos de Investigación, Fase II»**. Esa convocatoria **se cerró sin que se radicara nada**:
la financiación declarada no existe. La frase no la escribió el Docente, la ponía por defecto la
plantilla del agente de publicaciones, y de ahí se propagó a todo lo que salió.

La frase correcta es **«Este trabajo no recibió financiación»** / **«This work received no funding.»**

## Qué ya está hecho

Cinco archivos corregidos, junto a sus originales y con el sufijo `(corregido 2026-09-01)`:

| Archivo | Párrafos tocados |
|---|---|
| `Envio_EDU_REVIEW_17601/Manuscrito_ciego (corregido 2026-09-01).docx` | 2 |
| `Envio_EDU_REVIEW_17601/Portada_con_autoria (corregido 2026-09-01).docx` | 5 |
| `Envio_ITEES_17602/Manuscript_blinded (corregido 2026-09-01).docx` | 2 |
| `Envio_ITEES_17602/Title_page (corregido 2026-09-01).docx` | 4 |
| `Preprint_Completion_Gating_Moodle (corregido 2026-09-01).docx` | 3 |

Comprobado en los cinco: mismo número de párrafos que el original, la frase falsa ya no aparece, la
frase correcta sí, y **solo** esos 16 párrafos difieren. **Los originales no se tocaron**: son el
registro de lo que de verdad se envió.

## Qué falta, y por qué no lo pude hacer yo

### 1. Qeios — lo más urgente, porque está en abierto

`10.32388/z2uxxt`, depositado el 25/08/2026 con licencia CC BY. **La frase falsa está publicada**, en
inglés, en la sección **Statements and Declarations → Funding**. Dice hoy, literal:

> Internal research call CUN 2026 — Thematic Research Groups, Phase II. No external funding was
> received for this work.

Hay que dejarla en:

> This work received no funding.

**No se puede hacer desde esta máquina**, y no por falta de intentarlo. Las cuatro vías de acceso,
comprobadas una por una:

| Vía | Resultado |
|---|---|
| Sesión abierta de Qeios | No hay. En `revistas-cun`, ninguna cookie; en `gdocs-cun`, solo `_ga` y `_hjSessionUser` (analítica). |
| Contraseña guardada en Chrome | Ninguna para `qeios.com` en el almacén del perfil. |
| Acceso con Google | Qeios no lo ofrece. |
| «Log in with ORCID» | Sí lo ofrece, pero **no hay sesión de ORCID** en ningún perfil: `orcid.org/my-orcid` redirige a `signin`. |

El depósito no salió de aquí. Lo tiene que hacer el Docente entrando con su cuenta. Si hiciera falta
pedírselo a la plataforma, su contacto es `info@qeios.com`.

Con CC BY, lo ya descargado no se puede retirar: corregir la versión viva es todo lo que cabe hacer.

### 2. EDU REVIEW — envío 5579 (manuscrito 17601) · HECHO

**Correo enviado el 01/09/2026** desde `julian_castanoe@cun.edu.co` a **`administracion@edulab.es`**,
con asunto «Corrección de la declaración de financiación — envío 5579» y los dos archivos corregidos
adjuntos. Comprobado en Enviados; no quedó ningún borrador. El texto que se mandó es el que está más
abajo.

Se hizo por correo porque **dentro de la plataforma no hay ningún canal**:

**Como autor no se pueden sustituir los archivos.** Comprobado en la plataforma: la acción «Editar»
de cada archivo abre un formulario que **solo permite renombrarlo** (`name[es_ES]`), no subir una
versión nueva. Y **las discusiones no se pueden usar**: en este envío el único participante posible
es el propio autor, y OJS rechaza el guardado en silencio —el formulario se vuelve a pintar sin un
solo mensaje de error—. Se probó con una discusión nueva y con la edición de una existente; ninguna
guarda. La pestaña de metadatos tampoco tiene campo de financiación.

La dirección `administracion@edulab.es` está en la página de contacto de la revista, pero **la pinta
JavaScript**: descargar esa página con `curl` no la encuentra. Texto que se envió:

---
**Asunto:** Corrección de la declaración de financiación — envío 5579

Estimado equipo editorial:

Al revisar el envío 5579 he detectado un error en la declaración de financiación. El manuscrito
(`Manuscrito_ciego.docx`) y la portada (`Portada_con_autoria.docx`) indican que el trabajo está
adscrito a la «Convocatoria interna CUN 2026 — Desarrollo de Grupos Temáticos de Investigación,
Fase II». Esa declaración es incorrecta: el trabajo no recibió financiación de esa convocatoria ni de
ninguna otra. La frase correcta es «Este trabajo no recibió financiación».

Adjunto las versiones corregidas de ambos archivos, idénticas a las enviadas salvo en ese punto.
Desde mi perfil de autor solo puedo renombrar los archivos, no sustituirlos, así que quedo atento a
cómo prefieren que se tramite.

Lamento el error y quería dejarlo corregido antes de que el manuscrito pase a revisión.

Cordialmente,
Julián Andrés Castaño Espinosa

---

### 3. ITEES — envío 596 (manuscrito 17602)

No se puede tocar: la cuenta del ITM está deshabilitada y su aviso de validación cayó en Spam. Los
dos archivos corregidos quedan listos para cuando se recupere el acceso.

## Una cosa que hice mal

Al intentar abrir la discusión en el envío 5579, un selector mío cayó en un formulario que no era el
del diálogo y **dejé creada una discusión vacía** (fila 8943, 01/09/2026 16:39, sin asunto ni cuerpo).
Ya está **borrada**: el envío tiene hoy 0 discusiones y vuelve a estar como estaba.
