# Conector a Synapse CUN — pendientes de Producción

`synapse.py` conecta con **Synapse CUN** (<https://dashboard-investigaciones.web.app/>), la
plataforma institucional de seguimiento y analítica de investigación, y trae los datos reales:
sobre todo los **pendientes de Producción** del docente.

## Uso

```bash
python Investigacion/dashboard/synapse.py login        # una sola vez — abre Chrome
python Investigacion/dashboard/synapse.py estado       # ¿hay sesión? ¿de quién?
python Investigacion/dashboard/synapse.py pendientes   # lo que se usa a diario
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
