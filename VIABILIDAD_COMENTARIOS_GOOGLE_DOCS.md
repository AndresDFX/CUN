# Viabilidad — comentar el documento de un estudiante en Google Docs

**Pregunta:** conectarme con `julian_castanoe@cun.edu.co`, recibir el enlace de un documento que
compartió un estudiante y **hacer directamente los comentarios** según el criterio del curso.

**Fecha:** 20 de agosto de 2026 · **Estado:** **resuelto e implementado.**

> **Decisión del Docente (20/08/2026):** la **opción A** (OAuth de escritorio, todo automático desde
> el computador) **no es viable** y se descarta. Se implementó la **opción C**: Apps Script,
> ejecutado **a demanda**, sin ninguna credencial guardada en disco. El procedimiento está en
> **[LEEME - Comentar documentos de estudiantes.md](LEEME%20-%20Comentar%20documentos%20de%20estudiantes.md)**.
>
> Este informe se conserva porque es donde está la evidencia de **por qué** el resultado tiene la
> forma que tiene: los dos límites de Google del §1 mandan igual en la opción C, y son la razón de
> que el comentario viaje con la cita literal en vez de anclado al párrafo.

> **Añadido el 22/08/2026 — el ancla sí se consiguió, saliéndose de la API.** Los dos límites del §1
> siguen siendo ciertos **para la API**, y por eso la salida fue **no usar la API**: manejar Google
> Docs con el navegador del Docente y repetir su secuencia de teclas (`Ctrl+F` para llevar la
> selección a la frase, `Ctrl+Alt+M` para comentarla). Así el comentario queda **anclado exactamente
> a la cita**, comprobado leyendo `word/comments.xml` y los `w:commentRangeStart/End` del `.docx`
> exportado. Es la ruta de
> **[LEEME - Comentar documentos con Playwright.md](LEEME%20-%20Comentar%20documentos%20con%20Playwright.md)**,
> y es la recomendada desde esa fecha. La opción C no se retira: no necesita Chrome ni sesión de
> navegador.
>
> Lo que **no** cambió: sigue sin existir el modo sugerencia, y sigue sin existir un alcance de «solo
> comentar». Lo segundo dejó de importar porque ya no se pide ningún alcance.

> **Regla de este informe:** cada afirmación técnica está contrastada contra la API de Google (su
> propio documento de descubrimiento y su guía oficial) o contra disco, en esta sesión. Lo que no
> pude comprobar va marcado **SIN VERIFICAR** y con el modo de comprobarlo.

---

## 1. Veredicto

**Sí es viable**, y ya está funcionando. Lo que la decisión del §5 cambió no es *si* se puede, sino
**cuánto** de la cadena corro yo sola: quedó un pegado y un clic tuyos por documento, y a cambio no
hay ninguna credencial guardada en este computador.

Dos cosas que pedías **no** se pueden hacer, y no por falta de maña:

| Lo que suena natural | Realidad |
|---|---|
| Comentarios **anclados** al párrafo, como cuando seleccionas texto y comentas | **No.** Google muestra como *no anclados* los comentarios que ancla un tercero por API |
| Comentarios en **modo sugerencia** («Sugerir cambios») | **No existe** en la API. Cero peticiones de las 40 del Docs API crean sugerencias |

Lo que sí sale, y sale bien: **comentarios reales en la barra lateral del documento**, cada uno con
la **cita literal** del fragmento al que se refiere, la sección y el número de párrafo, y el
**criterio publicado del ACA** que lo motiva. Para el estudiante es retroalimentación citada y
trazable; lo único que pierde es el globo colgado del renglón.

---

## 2. La cadena, eslabón por eslabón

| # | Eslabón | Veredicto | Evidencia |
|---|---|---|---|
| 1 | Actuar como la cuenta CUN | **Sí, resuelto** | Apps Script corre con la sesión de la propia cuenta: no hay que autenticar nada (§5) |
| 2 | Leer el documento del estudiante | **Sí** | `docs.documents.get`; alcances `documents.readonly`, `drive.readonly`, `drive` |
| 3 | Escribir los comentarios | **Sí, sin anclar** | `POST files/{fileId}/comments`; `content` y `quotedFileContent` escribibles |
| 4 | Aplicar el criterio del curso | **Sí, ya funciona** | Extraído de las guías de ACA: **6 guías, 41 criterios**, 6–8 por guía, 0 vacías |
| 5 | Que yo escriba el texto de los comentarios | **Sí** | Es lo único que no necesita permiso de nadie |

### Eslabón 3, el que decide la calidad

De la guía oficial de Drive, sobre anclar comentarios:

> «Los anclajes son inmutables, y su posición relativa al contenido de un documento no se puede
> garantizar entre revisiones» · «las aplicaciones de los editores de Workspace tratan los
> comentarios anclados definidos por el desarrollador **como comentarios no anclados** en su
> visualización».

Es decir: el campo `anchor` existe y se puede escribir —lo confirmé en el esquema— pero Google Docs
**lo ignora al mostrarlo**. Recomiendan anclar solo donde la posición no se mueve (imágenes,
documentos de solo lectura). Un anteproyecto que el estudiante sigue editando es el caso contrario.

**Cómo lo compenso** (ya implementado): cada comentario lleva `quotedFileContent` con el fragmento
textual y encabeza con `Criterio «…» — <sección> (párrafo N)`. El estudiante ve la cita dentro del
comentario, así que sabe exactamente de qué frase le hablas.

### Eslabón 4, el que ya está resuelto y es el que más importa

Los criterios **no hay que dictármelos**: salen del `.docx` de la guía del ACA que ese mismo
estudiante recibió. Comprobado ejecutándolo:

```
proyecto1     aca1      8 criterios  ACA 1 (25%) - Formulacion del problema y fundamentacion...
proyecto1     acafinal  6 criterios  ACA FINAL (42%) - Anteproyecto integrado
creatividad   acafinal  7 criterios  ACA Final (32,8%) - Propuesta de Innovacion
investigacion acafinal  7 criterios  ACA Final (32,8%) - Articulo de nuevo conocimiento
tg2           acafinal  7 criterios  ACA Final (32,8%) - Avance consolidado hacia TG3
tg3           acafinal  6 criterios  ACA Final (32%) - Documento final de grado
```

Que sea **esa** la fuente no es comodidad, es lo correcto: al estudiante se le comenta contra el
checklist que se le entregó, no contra una rúbrica paralela que yo redacte. Y si el criterio cambia,
cambia en un solo sitio (`build_acas_estudiantes.py`) y el comentario lo sigue.

`aca1` no existe en los 4 cursos de pregrado y el script lo dice en vez de inventarlo: pregrado
tiene **una sola** tarea documental (ACA Final) y Especialización dos. Coincide con el aula.

---

## 3. Lo que se construyó (opción C) y cómo está probado

Dos mitades que no se hablan por la red, solo por el portapapeles: **ninguna credencial cruza**.

| Mitad | Archivo | Corre en |
|---|---|---|
| Leer y redactar | `config/gdocs/plan_comentarios.py` | este computador, sin red |
| Criterios (fuente única) | `config/gdocs/criterios_aca.py` | este computador, sin red |
| Generador | `config/gdocs/build_apps_script_comentarios.py` | este computador, sin red |
| Publicar | `PRINCIPAL - Comentar documentos de estudiantes.gs` | servidores de Google, con tu sesión |
| Prueba | `config/gdocs/_prueba_apps_script.py` | Node, con Apps Script simulado |

El procedimiento paso a paso está en
[LEEME - Comentar documentos de estudiantes.md](LEEME%20-%20Comentar%20documentos%20de%20estudiantes.md).

### Verificado, no supuesto

- **La sintaxis del `.gs` parsea** (`node --check`), así que no se descubre un paréntesis suelto al
  pegarlo.
- **Su lógica está probada de punta a punta sin cuenta ni red:** `_prueba_apps_script.py` ejecuta el
  `.gs` en Node con `UrlFetchApp`, `Logger`, `PropertiesService` y compañía simulados, y le da un
  documento de mentira. **15 comprobaciones, 0 fallos:** camino feliz, tipografía distinta entre el
  `.docx` y el documento vivo, cita que el estudiante ya editó, criterio inventado, compartido en
  modo Lector, `publicar` sin `CONFIRMAR`, y que `deshacer` borre lo que `publicar` creó.
- **La mitad Python, con un `.docx` real:** `leer` numera los 5 párrafos y **encuentra el texto dentro
  de las tablas** (donde van el cronograma y el presupuesto, que son dos criterios del ACA Final);
  `generar` rechaza los tres tipos de error —criterio inventado, cita ausente, texto vacío— y **no
  escribe el `Plan.gs`**; con el plan bueno lo emite y la diferencia de tipografía no lo despista.
- **41 criterios de 6 guías incrustados** en el `.gs`, y **19 equivalencias tipográficas** que se
  escriben **una sola vez** en `plan_comentarios.py` y se incrustan desde ahí: las dos mitades no
  pueden divergir en cómo comparan las citas.

### El paso intermedio es a propósito

El plan no se publica solo. Yo lo redacto, `generar` lo valida, y en Google `verificar` y `simular`
te imprimen **el texto exacto** que verá el estudiante. `publicar` no hace nada mientras
`CONFIRMAR` esté en `false`. Es la convención de `cdigital.py`, por el mismo motivo: al otro lado hay
estudiantes matriculados.

### Lo que no puede hacer, por construcción

- **No puede modificar el texto del estudiante.** No hay en el `.gs` ninguna llamada que escriba en
  el cuerpo del documento: solo lee (Docs API) y crea o borra comentarios (Drive API).
- **No pone notas.** La nota la pone el Docente.
- **No comenta un criterio que no esté en la guía.** Se valida aquí *y otra vez* en Google.
- **No inventa una ubicación.** Si la cita ya no está en el documento, omite ese comentario y lo dice.

---

## 4. Seguridad: el costo real de esto

**Hace falta el alcance amplio `https://www.googleapis.com/auth/drive`, y de eso no se escapa.** No
es pereza: el alcance restringido `drive.file` solo cubre los archivos que la aplicación creó o que el
usuario eligió con el Picker de Google, y el documento del estudiante no es ninguno de los dos. Para
comentar un archivo ajeno compartido, Drive exige el alcance completo. **No existe un alcance de solo
comentar.** Consecuencia honesta: mientras la autorización esté concedida, ese script **podría** leer
y escribir todo el Drive de la cuenta CUN.

Lo que la opción C cambia, y es la razón de elegirla:

- **No hay token en disco.** El permiso vive **dentro de la cuenta de Google**, no en un archivo de
  este computador. Nada que se filtre por una copia de seguridad, por Drive o por un `.gitignore` mal
  puesto; nada que caduque en silencio.
- **Lo revocas tú, en un sitio, cuando quieras:** <https://myaccount.google.com/permissions> →
  «CUN - Comentarios» → *Quitar acceso*. Con la opción A había que revocar **y** borrar el archivo.
- **Solo corre cuando pulsas *Ejecutar*.** No hay proceso local que pueda usar el permiso por su
  cuenta, ni desatendido, ni por error mío.
- **El código que puede usar ese permiso lo tienes delante**, en el editor de Apps Script, y lo pegas
  tú. No hay una dependencia que se actualice sola detrás.
- **No ve `G:`.** El repositorio y el material de los cursos están en la **otra** cuenta de Drive.
- **El trabajo del estudiante no entra al repositorio:** el `.docx` cae en `_Revisiones/`, que está
  ignorada por git (ver [`_Revisiones/LEEME.md`](_Revisiones/LEEME.md)).
- **Tu contraseña no pasa por aquí.** El consentimiento lo das en tu navegador, en Google.

### Defecto que encontré por el camino y corregí

`create_encuentros_p1_calendar_api.py` apuntaba su token OAuth a `config/slides/secrets/` —**sin**
guion bajo—, y el `.gitignore` solo cubre `_secrets/`. Un token guardado ahí **habría entrado a
git**, y de git a Drive. Además el script ni encontraba el `credentials.json` que su propio README
manda poner en `_secrets/`: estaba roto y era una fuga a la vez. Lo apunté a
`%LOCALAPPDATA%\gcal-cun\` y actualicé el README para que no vuelvan a divergir. Nunca llegó a
filtrarse nada, porque esa carpeta jamás se creó.

---

## 5. La incógnita que había, y por qué dejó de importar

> **Resuelta por decisión, no por prueba.** La pregunta de abajo quedó **sin comprobar** y así se
> queda: el Docente descartó la ruta que la necesitaba. Se conserva porque explica por qué la solución
> tiene la forma que tiene.

**¿Puede la cuenta CUN crear un proyecto en Google Cloud Console?** El OAuth de escritorio lo
necesita, y el administrador de Workspace puede tenerlo bloqueado. Hay dos señales, y apuntan a
lados distintos:

- **A favor:** esa cuenta **ya autorizó** un script propio no verificado. El runbook de las
  grabaciones documenta el paso exacto —«Google no ha verificado esta aplicación → Configuración
  avanzada → Permitir»—, así que el consentimiento a una app propia **no está bloqueado**.
- **En contra:** el mismo runbook dice que esa cuenta **no puede generar contraseñas de
  aplicación** porque «el administrador de Workspace lo tiene deshabilitado». El dominio está
  intervenido.

La prueba habría sido entrar a <https://console.cloud.google.com> con la cuenta CUN e intentar crear un
proyecto. **No se hizo, y ya no hace falta.**

### Las tres rutas, y en qué quedó cada una

| | Ruta | Quién ejecuta | Qué necesita | En qué quedó |
|---|---|---|---|---|
| **A** | OAuth de escritorio | Yo, de principio a fin | Proyecto en Google Cloud + token amplio en disco | **Descartada por el Docente** (20/08/2026). El código está archivado en `config/_Archivo obsoleto 2026-08-09/gdocs/comentar_documento.py`, sin haberse ejecutado nunca |
| **B** | Apps Script publicado como aplicación web | Yo la llamo por HTTPS | Despliegue accesible + secreto compartido | **No se intentó.** Reintroduce un secreto que hay que guardar en algún sitio, que es justo lo que se quería evitar |
| **C** | Apps Script ejecutado a mano | Tú pulsas *Ejecutar* | Nada más | **Implementada y probada** (§3) |

**La C no era el premio de consolación, era la opción preferible.** Es el mecanismo del script de
grabaciones, que en esta cuenta ya se sabe que funciona; no tiene incógnitas de dominio ni de
administrador; y el permiso amplio de Drive —que es inevitable, venga por donde venga— queda dentro de
la cuenta de Google en vez de en un archivo de este computador. El costo es un pegado y un clic por
documento. Lo que se compra con ese clic está en el §4.

**Lo único que quedó pendiente de comprobar** es una ejecución real contra un documento de verdad: la
lógica del `.gs` está probada con Apps Script simulado (15/15), pero nadie ha pulsado *Ejecutar*
todavía. La primera vez conviene hacerlo con **un documento tuyo**, no de un estudiante, y quedarse en
`simular`.

---

## 6. Dos decisiones que son tuyas, no mías

1. **Los comentarios salen a tu nombre**, porque es tu sesión la que ejecuta el script: el estudiante
   no puede distinguir si los redactaste tú o yo. Y las guías de ACA le exigen al estudiante «uso
   transparente de IA si la usaste». Pedir esa transparencia y no darla es una asimetría que
   conviene resolver a propósito. El `.gs` trae la constante `NOTA_IA`, que añade la declaración que
   decidas al final de cada comentario; sale **vacía por omisión** porque es tu decisión, no la mía.
   La alternativa razonable es anunciarlo una vez en el curso y dejarla vacía.
2. **La nota no la toca esto.** Puedo proponerte una calificación con la evidencia al lado, pero no
   se escribe en CDigital por esta vía.

---

## 7. Lo que falta de tu lado

No hay nada que descargar ni ningún proyecto que crear. Queda la instalación, unos diez minutos y una
sola vez, con los pasos exactos en
**[LEEME - Comentar documentos de estudiantes.md](LEEME%20-%20Comentar%20documentos%20de%20estudiantes.md)**:

1. **Pegar el `.gs`** en un proyecto nuevo de <https://script.google.com> con la cuenta CUN y ponerle
   nombre «CUN - Comentarios». No hay que habilitar ningún servicio avanzado.
2. **Decidir `NOTA_IA`** (la decisión 1 del §6). Vacía es una respuesta válida.
3. **Autorizar** por el camino de la app no verificada, el mismo del script de grabaciones. Te pedirá
   acceso a todo tu Drive; el §4 dice por qué es inevitable y qué lo acota.
4. **Un documento de prueba tuyo**, no de un estudiante, para el primer `verificar` + `simular`. Es lo
   único que aún no está comprobado contra Google de verdad.

Y después, por cada documento: que el estudiante comparta como **Comentador** (no hace falta Editor).
Si comparte como Lector, el script se detiene solo y te dice qué pedirle.

**Gmail no hace falta.** Con que me pegues el enlace en el chat basta; leer el correo exigiría un
segundo alcance amplio sobre todo tu buzón para ahorrar una acción de dos segundos. No lo
recomiendo.
