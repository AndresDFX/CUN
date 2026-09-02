# Paquete de envío — Revista PACA

**Preparado el 2 de septiembre de 2026.** Todo lo que el formulario de OJS va a pedir, en el orden en
que lo pide, para que el envío sea mecánico.

- **Revista:** Revista PACA · Universidad Surcolombiana · ISSN 2027-257x
- **Contacto:** revistapaca@usco.edu.co
- **Archivo a subir:** `Anchored_Feedback_PACA.docx` — 42 KB, **11 páginas** en Arial 12
  con interlineado 1.5, dentro de su horquilla de 8 a 15.

## Antes de nada: dos cosas que solo puedes hacer tú

1. **Crear la cuenta**, en <https://journalusco.edu.co/index.php/paca/user/register>. El formulario
   está protegido con **reCAPTCHA** (comprobado: dos iframes de Google y su `data-sitekey`), así que
   no se puede automatizar y no se ha intentado.

   **Y no hay ninguna cuenta previa que recuperar.** Comprobado el 02/09 por las tres vías: no hay
   credencial guardada en el almacén de Chrome de ninguno de los dos perfiles; las cookies
   `OJSSID_USCO_33022` solo prueban que el sitio se visitó, no que haya cuenta; y se pidió el
   restablecimiento de contraseña para `julian_castanoe@cun.edu.co` —el formulario **no** lleva
   CAPTCHA, solo el registro— y **no llegó ningún correo**. OJS responde «Se ha enviado una
   confirmación a su dirección de correo electrónico» exista o no la cuenta, así que el buzón es la
   única prueba, y dice que no existe. Campos obligatorios: nombre, apellidos, filiación,
   país, correo, usuario y contraseña. Usa el patrón de las otras cuatro revistas —usuario
   `jcastanoe`, correo `julian_castanoe@cun.edu.co`— y guarda la clave en
   `%LOCALAPPDATA%\revistas-cun\credenciales.json`.
2. **Diligenciar la Declaración de Originalidad**, que es requisito para que empiecen a evaluar:
   <https://forms.gle/kyckU5qWUB9ieQy87>. Sin ella «la omisión de este requisito impedirá el inicio del proceso de
   evaluación».

## Y una que depende de su respuesta

La consulta enviada el 01/09 a `revistapaca@usco.edu.co` pregunta si un preprint **depositado y aún
sin publicar** en SciELO Preprints es compatible con su casilla 1. **No firmes esa casilla hasta que
contesten.** Si dicen que no lo es, la salida es retirar el depósito del 17606 —hace falta la sesión
de `andresdfx` en SciELO, que no está en esta máquina— y entonces sí queda limpia.

## Metadatos, campo por campo

### Título
- **Español:** Retroalimentación formativa anclada en Google Docs sin acceso total a Drive: una limitación documentada de la API y una solución basada en sesión con verificación por exportación
- **Inglés:** Anchored Formative Feedback in Google Docs Without Full-Drive Access: A Documented API Limitation and a Session-Based Workaround with Export Verification

### Resumen (español)
La retroalimentación formativa es más útil cuando va pegada a la frase de la que habla que cuando llega como una lista aparte. En Google Docs —la plataforma en la que se escribe y se comparte buena parte de la producción estudiantil en la educación superior latinoamericana— anclar programáticamente un comentario a una frase resulta más difícil de lo que sugiere la superficie de la API. Reportamos tres hallazgos establecidos al construir una herramienta de retroalimentación para cinco asignaturas universitarias. Primero: la API de Drive expone un campo `anchor` escribible, pero la propia documentación de Google indica que los editores de Workspace muestran los comentarios anclados definidos por el desarrollador **como no anclados**, de modo que el campo se escribe y no surte efecto visual. Segundo: no existe un alcance OAuth de «solo comentar»; comentar un documento ajeno exige el alcance completo `drive`, que concede lectura y escritura sobre todo el Drive del docente. Tercero: el modo sugerencia que los docentes piden no existe en la API. Describimos después la solución adoptada —conducir el editor con la sesión de navegador que el docente ya tiene, sin pedir ninguna autorización nueva— y la verificación de cada comentario publicado exportando el documento y comprobando las marcas `w:commentRangeStart` y `w:commentRangeEnd`, en lugar de mirar la pantalla. Reportamos las salvaguardas que esto exigió, incluido un incidente en el que se publicaron comentarios en el documento real de un estudiante y hubo que retirarlos, y decimos con claridad qué no resuelve el enfoque.

**Palabras clave (español):** retroalimentación formativa, API de Google Docs, alcances OAuth, tecnología

### Abstract (inglés)
Formative feedback is more useful when it is attached to the sentence it refers to than when it arrives as a separate list of remarks. In Google Docs — the platform on which a large share of student writing in Latin American higher education is produced and shared — attaching feedback to a specific phrase programmatically turns out to be harder than the API surface suggests. We report three findings established while building a feedback tool for five university courses. First, the Drive API exposes a writable `anchor` field on comments, but Google's own documentation states that Workspace editors render developer-defined anchored comments **as unanchored**, so the field is writable and cosmetically ineffective. Second, no "comment-only" OAuth scope exists: commenting on a document owned by someone else requires the full `drive` scope, which grants read and write access to the instructor's entire Drive — a disproportionate privacy cost for a feedback tool. Third, the suggestion mode that instructors actually ask for is absent from the API entirely. We then describe the workaround adopted: driving the editor through the instructor's existing browser session, which requires no new authorisation grant, and verifying every published comment by exporting the document and checking for `w:commentRangeStart` and `w:commentRangeEnd` markers in the resulting archive rather than by reading the screen. We report the operational safeguards this required, including an incident in which comments were published to a real student document and had to be withdrawn, and we state plainly what the approach does not solve. No student data are reported and no learning outcome is claimed.

**Keywords (English):** formative feedback, Google Docs API, OAuth scopes, educational technology, browser

### Autoría
Único autor. Julián Andrés Castaño Espinosa · Escuela de Ingeniería, Corporación Unificada Nacional
de Educación Superior (CUN) · Bogotá, Colombia · `julian_castanoe@cun.edu.co` ·
ORCID `0009-0003-6598-432X`.

### Financiación
**Ninguna.** «Este trabajo no recibió financiación» / «No funding was received for this work».
No se declara la Convocatoria interna CUN 2026: esa convocatoria cerró sin que se radicara nada.

### Declaración de uso de IA
La exige su política, nombrando la herramienta y su papel. El manuscrito ya la trae: asistentes
generativos —Claude (Anthropic) y ChatGPT (OpenAI)— para redacción, edición y comprobación de
coherencia interna, y en la construcción de la herramienta descrita. Ninguna generó datos,
mediciones ni referencias que el autor no verificara una por una.

### Tipología
**Pendiente de su respuesta.** El trabajo es un resultado negativo documentado con solución alterna
verificada; no reporta datos de estudiantes ni resultados de aprendizaje, y lo declara. De las tres
tipologías que publican no encaja limpio en ninguna hoy. La segunda consulta pregunta exactamente
eso. Si contestan «reflexión», hay que reestructurarlo a Introducción · Desarrollo y discusión ·
Conclusiones —ya está maquetado así— y **citar de verdad en el cuerpo** las nueve referencias
educativas, que hoy están en la bibliografía sin aparecer en el texto.

## Estado del manuscrito

- 2793 palabras en el archivo fuente; 1.464 de cuerpo (§1–§6).
- **17 referencias** en APA 7, tras añadirse la de Google el 01/09.
- Cero tablas, cero figuras, cero marcadores pendientes.
- Sin ninguna de las cifras contaminadas.
- Corregido el 01/09: dos frases que estaban entrecomilladas **no eran las de la fuente**. Ahora son
  literales y llevan su referencia.
