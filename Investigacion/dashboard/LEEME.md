# Conector a Synapse CUN — pendientes de Producción

`synapse.py` conecta con **Synapse CUN** (<https://dashboard-investigaciones.web.app/>), la
plataforma institucional de seguimiento y analítica de investigación, y trae los datos reales:
sobre todo los **pendientes de Producción** del docente.

## Uso

```bash
python Investigacion/dashboard/synapse.py login        # una sola vez — abre Chrome
python Investigacion/dashboard/synapse.py estado       # ¿hay sesión? ¿de quién?
python Investigacion/dashboard/synapse.py pendientes   # lo que se usa a diario
python Investigacion/dashboard/synapse.py calendario   # CSV de eventos: alerta + fecha exacta
python Investigacion/dashboard/synapse.py recopilar    # volcado de todo lo accesible
python Investigacion/dashboard/synapse.py cerrar       # borrar la credencial local
```

`login` abre Chrome de verdad en la pantalla de Synapse. **Usted inicia sesión con Google**; el
script espera hasta 5 minutos, detecta la sesión y guarda el token de refresco. A partir de ahí no
vuelve a hacer falta el navegador: los demás subcomandos consultan la API directamente.

`pendientes` escribe tres archivos en `datos/`: `Pendientes de Produccion.md` (informe legible, con
los vencidos primero), `pendientes_produccion.json` (el mismo análisis, para otros scripts) y
`productos_propios.json` (el documento crudo de la plataforma, sin interpretar).

`recopilar` añade `inventario_synapse.json`. Por defecto trae **solo los datos propios**; con
`--todo` barre además las colecciones globales, que pueden contener fichas y correos de otros
docentes — úselo solo si de verdad lo necesita.

## `calendario` — los eventos de Producción, con la alerta a siete días

```bash
python Investigacion/dashboard/synapse.py calendario                  # alerta a 7 días
python Investigacion/dashboard/synapse.py calendario --alerta 14      # otra antelación
python Investigacion/dashboard/synapse.py calendario --sep ";"        # si Excel no separa bien
```

**Synapse no tiene colección de calendario.** El apartado de Producción arma sus eventos a partir
de los productos del docente, y este subcomando reconstruye las mismas dos fuentes:

| Evento | De dónde sale |
|---|---|
| Entrega final | `deliveryDate` del producto (o `dueDate` si falta) |
| Hito parcial | un evento por cada `partialMilestones[]`, con su `title` y su `dueDate` |

Es el mismo par que usa el panel de administración para su `Reporte_Entregas.xlsx`, donde cada
fila sale marcada `Tipo: Final` o como hito. Si un día apareciera una colección de calendario de
verdad, este es el sitio a cambiar.

Escribe dos CSV en `datos/` (y el mismo análisis en `eventos_produccion.json`):

- **`eventos_produccion.csv`** — el de revisar. Una fila por evento, con `fecha_alerta`
  (= entrega − 7 días), `fecha_entrega` exacta, `dias_para_entrega` y dos columnas para filtrar:
  `alerta_activa` (¿ya entré en la ventana de siete días?) y `requiere_accion`.
- **`eventos_produccion_google_calendar.csv`** — importable en Google Calendar.

Tres decisiones que no son obvias:

1. **`Rechazado` cuenta como pendiente.** El producto volvió al docente y hay que reentregarlo, así
   que sigue necesitando alerta. Solo `Aprobado` y `Entregado` se consideran cerrados.
2. **La importación por CSV de Google Calendar no sabe crear recordatorios.** La alerta no puede
   viajar como propiedad del evento, así que el segundo CSV escribe **dos** eventos de día completo
   por entrega: `[Revisar 7d]` en la fecha de alerta y `[ENTREGA]` el día del vencimiento. Sus
   fechas van en `MM/DD/YYYY`, que es lo que exige el importador, y con coma obligatoria. Solo
   entran los eventos que requieren acción: importar vencimientos ya aprobados sería ruido pasado.
3. **Una fecha ausente y una fecha ilegible no son lo mismo.** La segunda sale como
   `FECHA ILEGIBLE: <valor>` y se muestra tal cual, sin adivinar si `20/08/2026` es día/mes o
   mes/día. Es un dato roto en la plataforma: Synapse la lee con `new Date(fecha + "T00:00:00")`,
   así que allí también sale «Invalid Date». Los eventos sin fecha utilizable **no** entran al CSV
   de Calendar —no hay dónde ponerlos— y por eso el subcomando los lista aparte al final: lo que no
   se puede vigilar hay que decirlo, no callarlo.

Los CSV van a `datos/`, que está en `.gitignore`.

## Sobre las credenciales

- **El script nunca ve su contraseña.** La escribe usted en la ventana de Google. Aquí no hay ningún
  campo, variable ni archivo donde se guarde una contraseña.
- **El token de refresco no se guarda en este repositorio.** Vive en
  `%LOCALAPPDATA%\synapse-cun\credenciales.json`, junto con el perfil de Chrome. La razón es
  concreta: este repositorio está en git **y** sincronizado a Google Drive, así que cualquier archivo
  que se escriba aquí se replica y queda en el historial. El `.gitignore` de esta carpeta es solo una
  segunda línea de defensa.
- El token da acceso a la cuenta institucional hasta que se revoque. Para revocarlo:
  `synapse.py cerrar` borra la copia local, y el permiso de la aplicación se retira desde
  <https://myaccount.google.com/permissions>.
- `datos/` está en `.gitignore`. Si necesita compartir un informe, copie el texto — no el archivo.

## Cómo está construida la plataforma (por si cambia)

Descubierto leyendo el JavaScript público de la app, sin autenticarse:

| Cosa | Valor |
|---|---|
| Proyecto Firebase | `sapiolab-48252` |
| Autenticación | Firebase Auth · Google, restringido a `hd: cun.edu.co` |
| Base de datos | Cloud Firestore (API REST) |
| Cloud Functions | `https://us-central1-sapiolab-48252.cloudfunctions.net/dashboard_docentes` |
| Roles en el login | Docente · Administrador |

**Modelo de datos relevante.** Los productos están en la colección `products`, **un documento por
docente**, cuyo id es el uid del usuario. Dentro hay un arreglo `products`, y cada producto lleva
`productName`, `status`, `documentUrl`, `deliveredAt`, `deliveryNotes`, `adminFeedback`,
`lastActivity` y un arreglo `partialMilestones` con `status` y `dueDate` por hito. Los estados que
usa la aplicación son `Pendiente`, `Vencida`/`Vencido`, `Entregado`, `Aprobado` y `Rechazado`; el
conector trata los tres primeros como "abiertos". Otras colecciones: `users`,
`produccion_investigacion`, `proyectos_investigacion`, `grupos_investigacion` y tres de
`estadisticas_*` de semilleros, estas últimas consultadas por `where("year","==",N)`.

**Dos decisiones técnicas que no son obvias:**

1. Se usa **Chrome real** (`channel="chrome"`), no el Chromium que trae Playwright, porque Google
   bloquea el inicio de sesión en navegadores con marcas de automatización.
2. Se usa un **contexto persistente** (carpeta de perfil) y no `storage_state()`, porque Firebase
   guarda la sesión en **IndexedDB** (`firebaseLocalStorageDb`) y `storage_state()` solo captura
   cookies y `localStorage`.

Y una trampa: `wait_until="networkidle"` nunca se cumple en esta app, porque mantiene abierta una
conexión permanente con Firestore. Hay que usar `domcontentloaded`.

## Si deja de funcionar

- *"El refresh token ya no sirve"* → la sesión se revocó o caducó. `synapse.py login` otra vez.
- *"permiso denegado por las reglas de seguridad"* → las reglas de Firestore no dejan leer esa
  colección con rol de docente. Es esperable en las colecciones globales; no es un error del script.
- *No pude pulsar «Docente» / «Continuar con Google»* → la interfaz cambió de etiquetas. No importa:
  la ventana queda abierta, hágalo a mano y el script detecta la sesión igual.
- Si cambia el `apiKey` o el bundle de la app, los valores están al principio de `synapse.py`, en el
  bloque de constantes.
