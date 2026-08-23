# Comentar el documento de un estudiante — a demanda, sin credenciales

**5 cursos · 6 guías de ACA · 41 criterios** · un solo proyecto de Apps Script, instalado una vez

> **Hay una segunda ruta, y para el uso normal es mejor:**
> [LEEME - Comentar documentos con Playwright.md](LEEME%20-%20Comentar%20documentos%20con%20Playwright.md).
> Deja el comentario **anclado a la frase**, que es lo que esta no puede hacer (ver el recuadro de
> abajo), lee además el Syllabus de la asignatura y no hay que pegar nada por cada documento.
> Esta ruta **no se retira**: no necesita Chrome ni sesión de navegador, así que sigue siendo la
> salida cuando la otra no se pueda abrir.

> Los dos archivos de este proceso son **generados**. Regenerar:
> `python config/gdocs/build_apps_script_comentarios.py`

## Qué vas a conseguir

Que el documento que te comparte un estudiante quede **comentado en Google Docs**, un comentario por
criterio, cada uno citando la frase exacta del estudiante y el criterio **de la guía del ACA que él
mismo recibió**. Sin contraseñas, sin token guardado en disco, sin proyecto en Google Cloud. Unos
diez minutos de instalación, una sola vez; después son dos comandos y un pegado por documento.

Esto es la **opción C** del informe [VIABILIDAD_COMENTARIOS_GOOGLE_DOCS.md](VIABILIDAD_COMENTARIOS_GOOGLE_DOCS.md).
La opción A (OAuth de escritorio, todo automático desde el computador) se descartó: exigía crear un
proyecto en Google Cloud con la cuenta CUN. A cambio de un pegado por documento, aquí **no queda
ningún token con acceso a todo tu Drive guardado en el disco**.

## ⚠️ Lo primero: dos límites de Google que no son de este script

| Lo que suena natural | Realidad |
|---|---|
| El comentario colgado del párrafo, como cuando seleccionas texto y comentas | **No.** Google muestra como *no anclados* los comentarios que ancla un tercero por API |
| Comentarios en «modo sugerencia» | **No existe** en la API de Docs: ninguna de sus 40 operaciones crea sugerencias |

Los comentarios salen en la **barra lateral**, y cada uno lleva dentro la **cita literal** de la
frase y su sección y número de párrafo. Es lo más cerca del comentario anclado que la API permite.

Y una consecuencia que conviene tener presente: **salen a tu nombre**, porque es tu cuenta la que
ejecuta el script. El estudiante no puede distinguir quién los redactó. Si quieres corresponder a lo
que las guías le exigen a él —«uso transparente de IA si la usaste»— hay una constante para eso:
`NOTA_IA`, en el paso 2.

---

## Instalación (una vez)

### 1. Abre Apps Script con la cuenta CUN

**https://script.google.com** con **julian_castanoe@cun.edu.co**. Tiene que ser la cuenta a la que el
estudiante compartió el documento. **Nuevo proyecto** → borra el `function myFunction()` de fábrica →
pega **todo** el contenido de `PRINCIPAL - Comentar documentos de estudiantes.gs` → guarda. Ponle
nombre reconocible: **«CUN - Comentarios»**.

**No hace falta añadir ningún servicio avanzado.** El script habla con las APIs de Docs y de Drive
por HTTPS con el token de tu propia sesión, así que no hay nada más que habilitar.

### 2. Decide `NOTA_IA` — es la única cosa que configuras

Arriba del archivo:

```js
var NOTA_IA = '';
```

Vacía, no se añade nada. Si quieres que cada comentario lo declare:

```js
var NOTA_IA = '— Retroalimentación redactada con apoyo de IA y revisada por el Docente.';
```

Sale **apagada por omisión** a propósito: es una decisión tuya, no del script. La alternativa
razonable es anunciarlo una vez en el curso y dejarla vacía.

### 3. Autoriza

La primera vez que ejecutes algo, Google pide permisos: **Revisar permisos** → tu cuenta CUN →
«Google no ha verificado esta aplicación» → **Configuración avanzada** → **Ir a CUN - Comentarios** →
**Permitir**. Es tu propio script; el aviso sale porque no está publicado en ninguna tienda. Es el
mismo camino del script de grabaciones.

**Te va a pedir acceso a todo tu Drive**, y conviene saber por qué: para comentar un archivo que te
compartió otra persona, Google exige el permiso amplio. El permiso restringido solo cubre los
archivos que la propia aplicación creó. No hay término medio y no es opcional.

Si algún día falla con **HTTP 401**, es que el permiso no quedó concedido: *Configuración del
proyecto → Mostrar el archivo de manifiesto `appsscript.json`* y comprueba que dice

```json
"oauthScopes": ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/script.external_request"]
```

Si no está, añádelo, guarda y vuelve a autorizar.

---

## El ciclo, por cada documento

### 1. Descarga la copia

Abre el documento compartido → **Archivo → Descargar → Microsoft Word (.docx)** → guárdalo en
**`_Revisiones/`** con nombre corto, p. ej. `ACA1 - Perez.docx`. Esa carpeta está **ignorada por
git**: el trabajo del estudiante no entra al historial (ver [su LEEME](_Revisiones/LEEME.md)).

Y copia el **id del documento** de la barra de direcciones:

```
https://docs.google.com/document/d/1AbCdEfG.../edit    <- esto es el id
```

### 2. Pásame el `.docx` y el id

Yo leo el documento con

```bash
python config/gdocs/plan_comentarios.py leer "_Revisiones/ACA1 - Perez.docx" \
    --curso proyecto1 --aca aca1
```

que lo vuelca numerado junto a los criterios del ACA, y escribo `_Revisiones/ACA1 - Perez.plan.json`:
un comentario por criterio, cada uno con la **cita literal** de la frase a la que se refiere.

**Los criterios no hay que dictármelos.** Salen del `.docx` de la guía del ACA, la misma que recibió
el estudiante. Claves de `--curso`: `proyecto1`, `creatividad`, `investigacion`, `tg2`, `tg3`. Claves
de `--aca`: `aca1` (solo Proyecto I) y `acafinal` (los cinco). Pregrado tiene **una sola** tarea
documental; si te equivocas, el comando te dice cuáles hay.

### 3. Genera el `Plan.gs`

```bash
python config/gdocs/plan_comentarios.py generar "_Revisiones/ACA1 - Perez.plan.json"
```

**No escribe nada si algo no cuadra:** un criterio que no esté en la guía, un comentario sin texto, o
—la importante— una cita que no aparezca en el documento. Te dice cuál y por qué.

### 4. Pega y ejecuta, en este orden

En el proyecto «CUN - Comentarios», **archivo nuevo** llamado `Plan` (o reemplaza el de la revisión
anterior) y pega el `Plan.gs` completo. Luego, en el desplegable de arriba:

| Ejecuta | Qué hace | Escribe algo |
|---|---|---|
| **`verificar`** | acceso, criterios y que cada cita siga en el documento vivo | **no** |
| **`simular`** | además, imprime el comentario **exacto** que vería el estudiante | **no** |
| **`publicar`** | publica | **sí** |
| `deshacer` | borra los comentarios de la última publicación | sí |

Todo sale en **Ver → Registro de ejecución**.

`publicar` **no hace nada** mientras `Plan.gs` diga `var CONFIRMAR = false;`. Cuando la salida de
`simular` te convenza, ponlo en `true`, guarda y ejecuta `publicar`.

### 5. Si te arrepientes

`deshacer` borra los comentarios de la última publicación —guarda sus ids— y limpia el registro. Solo
la última: si publicas en dos documentos seguidos, solo puedes deshacer el segundo.

---

## Por qué la cita y no el número de párrafo

El `.docx` descargado y el documento vivo **no numeran igual** los párrafos: la exportación junta y
parte cosas, y el estudiante sigue editando mientras tú revisas. Si el comentario viajara con
«párrafo 12» acabaría señalando la frase equivocada delante del estudiante.

Así que viaja con la **cita literal**, y el script la busca en el documento vivo antes de publicar:

- la encuentra → publica, y calcula el párrafo y la sección **sobre el documento real**;
- no la encuentra → **omite ese comentario** y lo dice, no inventa una ubicación;
- la comparación ignora las comillas curvas, la raya, el guion y los espacios duros, porque Word y
  Google Docs se los intercambian a su gusto.

Que la comparación sea idéntica en los dos lados no es confianza: la tabla de equivalencias se
escribe una vez en `plan_comentarios.py` y el generador la **incrusta** en el `.gs`.

---

## Lo que este script no puede hacer

- **No puede modificar el documento.** Solo lee y crea o borra comentarios. No existe en el código
  ninguna llamada que escriba en el cuerpo del texto del estudiante.
- **No pone notas.** La nota la pone el Docente, en CDigital, a mano.
- **No comenta un criterio que no esté en la guía.** Lo valida `plan_comentarios.py` aquí y otra vez
  el propio `.gs` allá, contra los 41 criterios que lleva incrustados.

## Cuando algo falla

| Síntoma | Qué es |
|---|---|
| `HTTP 401` | el permiso no quedó concedido → reautoriza (paso 3 de la instalación) |
| `HTTP 403` | la cuenta no tiene permiso sobre ese documento |
| `HTTP 404` | id equivocado, o esta cuenta no ve el documento |
| «Lo compartieron en modo Lector» | pídele acceso de **Comentador**; con ese basta, no hace falta Editor |
| «la cita ya no está en el documento» | el estudiante editó esa frase → vuelve a descargar el `.docx` y regenera |
| «CONFIRMAR está en false» | es lo correcto: revisa `simular` y luego ponlo en `true` |
| «Falta el archivo Plan.gs» | no pegaste el plan, o lo llamaste de otro modo |

## Mantenimiento

Si cambian los criterios de un ACA (es decir, si cambia `build_acas_estudiantes.py`), regenera y
vuelve a pegar el archivo principal:

```bash
python config/gdocs/build_apps_script_comentarios.py
python config/gdocs/_prueba_apps_script.py     # 15 comprobaciones, sin red y sin cuenta
```

`_prueba_apps_script.py` ejecuta el `.gs` en Node con las globales de Apps Script simuladas y le da
un documento de mentira: comprueba el camino feliz, la tipografía distinta, la cita que el estudiante
borró, el criterio inventado, el modo Lector, `publicar` sin `CONFIRMAR`, y que `deshacer` borre lo
que `publicar` creó. Es lo que evita que un fallo se descubra delante de un estudiante.
