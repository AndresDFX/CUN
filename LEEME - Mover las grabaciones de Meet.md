# Mover las grabaciones de Meet — automático, sin credenciales

**5 asignaturas · 7 aulas · 1 sola carpeta destino** · barrido cada 30 minutos · un único proyecto de Apps Script, instalado una vez

> **Archivo generado — no editar a mano.** Perfil `CUN`. Regenerar: `python config/slides/build_apps_script_grabaciones.py CUN`

## Qué vas a conseguir

Que cada grabación de Meet salga sola de donde Google la deja —la carpeta por omisión de Meet en tu Mi unidad: hoy «Meet Recordings»— y aparezca en la **carpeta única de grabaciones** (https://drive.google.com/drive/folders/1EHck-ZdbwwLJtDk2NsS4UDL1UMf1sLqZ?usp=sharing) con el nombre por el que el correo de bienvenida y el `LEEME - Material para estudiantes` le dicen al estudiante que la busque: «periodo - grupo - asignatura - sesión». **Unos diez minutos** de instalación, una sola vez; después no hay que volver a tocarlo, ni el semestre que viene.

No necesita contraseña, ni token, ni contraseña de aplicación (que esta cuenta **no puede generar**: el administrador de Workspace lo tiene deshabilitado), ni que tu computador esté encendido. Apps Script corre en los servidores de Google con tu propia sesión.

Son dos archivos, los dos en la raíz de `Cursos/` porque esto es **uno solo para todos los cursos** (no hay una copia por grupo): `PRINCIPAL - Mover grabaciones de Meet.gs`, que es el que se pega en Apps Script, y este runbook.

## ⚠️ Lo primero: un dato que pegar y un paso previo

**El dato:** `ORIGEN_ID` sale **vacío a propósito**. Es la carpeta por omisión donde Meet te deja las grabaciones, en tu Mi unidad — **hoy «Meet Recordings»**; si tu Drive muestra en su lugar una carpeta **«Google Meet»** con una subcarpeta por reunión, usa esa (y si dentro tienes «Legacy Meet Recordings», es lo antiguo: se deja fuera salvo que pongas `ORIGEN_LEGACY_ID`). No está en el repositorio porque no se puede deducir, y el script tampoco elige «la primera carpeta con ese nombre»: Google ha movido y renombrado estas carpetas más de una vez, así que **el enlace se pega a mano** (o el id, si lo prefieres).

Cómo se saca: abre la carpeta en Drive y **copia el enlace de la barra de direcciones, entero**. No hay que sacarle el id a mano —eso es de donde salen los errores tontos—: el propio `.gs` lo extrae, y entiende las cuatro formas en que Drive reparte enlaces, además del id pelado.

```
https://drive.google.com/drive/folders/1AbCdEfG...              <- pégalo así, entero
https://drive.google.com/drive/u/0/folders/1AbCdEfG...          <- también vale
https://drive.google.com/drive/folders/1AbCdEfG...?usp=sharing  <- también
https://drive.google.com/open?id=1AbCdEfG...                    <- también
1AbCdEfG...                                                     <- y el id pelado
```

Si pegas por error el enlace de un **archivo** (los que llevan `/d/`) en vez del de la carpeta, el registro te lo dice con esas palabras y esa constante queda vacía: el script avisa y no mueve nada, nunca adivina.

Mientras `ORIGEN_ID` esté vacío el script **no mueve nada** y te dice que falta; `verificarGrabaciones()` incluso te lista candidatos por nombre para copiar y pegar.

**El paso previo:** los encuentros de la asignatura tienen que **existir en tu Calendar**. Cuando Meet no nombra el archivo con el título del evento (pasa siempre que la reunión se inicia desde la sala), lo único que puede decir de qué clase es resulta ser el propio Calendar. Esas series las crea `PRINCIPAL - Crear encuentros con invitados.gs` de cada curso, y hoy **solo Proyecto I la tiene**: los otros cuatro siguen con `"meet": ""` en `carga_academica_2026.json` y su serie no se ha creado (ver «Pendientes» en `LEEME - Mapa de cursos y manuales.md`). Sin eso, en esas 6 aulas cada grabación saldrá en `--- sin clasificar ---` con «no hay ningún encuentro en el Calendar…» y se quedará quieta: no es que el automatismo no sirva, es que falta el paso anterior.

Y un supuesto que conviene confirmar el primer día: **la carpeta de grabaciones está en Mi unidad**, no en una unidad compartida. Si estuviera en una unidad compartida, `DriveApp` no bastaría (haría falta el servicio avanzado de Drive) y —lo importante— mover el vídeo allí **transferiría su propiedad a la institución de forma irreversible**. Si algún día se decide eso, se decide a propósito y no como efecto secundario de este script.

## Paso a paso

### 1. Abre Apps Script con la cuenta CUN

**https://script.google.com** con **julian_castanoe@cun.edu.co**. Tiene que ser la cuenta del **organizador** de las clases: las grabaciones nacen en *su* Mi unidad y ningún script puede ver el Drive de otra persona. **Nuevo proyecto** → borra el `function myFunction()` de fábrica → pega **todo** el contenido de `PRINCIPAL - Mover grabaciones de Meet.gs` → guarda. Ponle un nombre reconocible al proyecto: «CUN - Grabaciones».

No hace falta añadir ningún servicio avanzado. Este script usa solo Drive, Calendar y los disparadores, que vienen de serie.

### 2. Pega el `ORIGEN_ID`

En el bloque `// ─── CONFIGURACIÓN ───`, la única constante que sale vacía:

```js
var ORIGEN_ID = '';   // <- pega aquí el ENLACE de tu carpeta de grabaciones de Meet
```

Guarda. Lo demás ya viene puesto desde el perfil: la carpeta destino (`https://drive.google.com/drive/folders/1EHck-ZdbwwLJtDk2NsS4UDL1UMf1sLqZ?usp=sharing` → id `1EHck-ZdbwwLJtDk2NsS4UDL1UMf1sLqZ`), el calendario (`primary`) y las salas de Meet conocidas.

### 3. Ejecuta `verificarGrabaciones()` — siempre, antes que nada

Elige **`verificarGrabaciones`** en el desplegable de arriba y pulsa **Ejecutar**.

La primera vez Google pide permisos: **Revisar permisos** → tu cuenta CUN → «Google no ha verificado esta aplicación» → **Configuración avanzada** → **Ir a (nombre del proyecto)** → **Permitir**. Es tu propio script; el aviso sale porque no está publicado en ninguna tienda.

`verificarGrabaciones()` **no mueve, no renombra, no borra y no instala nada**. Solo escribe en el registro (*Ver → Registro de ejecución*):

- el modo (`SIMULACIÓN` / `REAL`), la zona horaria y los márgenes;
- el **calendario** con su nombre y su id — comprueba que es el tuyo de CUN;
- las carpetas **ORIGEN** y **DESTINO** con nombre e id;
- si hay disparador instalado y cuántos movimientos se pueden deshacer;
- un bloque **`--- se moverían ---`** con una línea por archivo, el criterio con el que lo identificó y **el nombre nuevo** si va a renombrarlo;
- un bloque **`--- sin clasificar ---`** con lo que se queda quieto **y por qué**;
- el resumen contable: `se moverían=… · se renombrarían=… · sin clasificar=…`.

Si algo no cuadra —calendario equivocado, un archivo ajeno en la lista de «se moverían»— párate aquí. Todavía no has tocado nada.

### 4. Apaga la simulación y muévelo una vez a mano

```js
var SIMULAR = true;    // ponlo en false
```

Guarda y ejecuta **`moverGrabaciones()`**. Verás una línea `movido: …` por archivo y el resumen `movidos=… · renombrados=… · sin clasificar=… · fallidos=… · en gracia=… · descartados antes=… · sin mirar por falta de tiempo=… · subcarpetas vaciadas=…`. Abre la carpeta destino y compruébalo con tus ojos.

`en gracia=` son los archivos que aparecieron hace menos de 20 minutos: se dejan a propósito, por si Meet todavía está depositando la transcripción o las notas. Los recoge la pasada siguiente.

Volver a ejecutarlo **no mueve nada dos veces**: lo ya movido no está en el origen. Y lo que no supo clasificar sigue donde estaba, con su nombre intacto.

### 5. Instala el disparador

Ejecuta **`instalarDisparador()`**. Crea un disparador temporal que llama a `moverGrabaciones()` **cada 30 minutos**. Si ya hay uno, **no crea un segundo**: te dice cuál existe.

Por qué 30 y no cada 15 o cada minuto: la cuota de Workspace es **360 min/día de disparadores**, y este script se permite hasta **4,5 min por pasada** (`LIMITE_MS`, el freno con el que evita morir en los 6 min que da Apps Script). En el peor caso, 30 min son 48 pasadas × 4,5 = **216 min**, que caben; cada 15 min serían 96 × 4,5 = 432 min, que **no** caben —Google cortaría el disparador el resto del día con «Service invoked too many times for one day»— y cada minuto ni de lejos. En la práctica una pasada normal tarda segundos: los 4,5 min solo se acercan si hay un lote grande. Y Apps Script programa con ventanas de ±15 min, así que la hora exacta no está garantizada y tampoco hace falta: la grabación tarda en generarse.

Si un día falla, Google te manda un correo con el error. No hay que vigilarlo.

## Qué permisos pide y por qué

| Permiso | Para qué lo usa |
|---|---|
| **Ver y gestionar tus archivos de Google Drive** | Leer la carpeta de grabaciones de Meet, mover el archivo a la carpeta de grabaciones y renombrarlo. Es el permiso amplio de `DriveApp`: Google no ofrece uno más estrecho para mover archivos. El script solo recorre `ORIGEN_ID` y escribe en `DESTINO_ID`, y **nunca borra**. |
| **Ver los eventos de tus calendarios** | Preguntar qué encuentro había a la hora de la grabación. Es de solo lectura: el script no crea ni modifica eventos. |
| **Ejecutarse cuando no estás presente** | El disparador temporal. Es lo que hace que funcione con el computador apagado. |

Nada de eso guarda una credencial: el script se ejecuta *como tú*, y si algún día quieres cortarlo, borras el proyecto de Apps Script y se acabó.

## Qué NO rompe (y la única cosa que sí cambia)

- **Los enlaces siguen funcionando.** Mover un archivo en Drive **no cambia su `fileId`**, así que el enlace que Meet te envió por correo, el que hayas pegado en CDigital y el que tenga cualquier estudiante siguen abriendo el mismo vídeo. Google se apoyó en esa misma propiedad para su mudanza de julio de 2026 («your old recording links will continue to work»). Por eso el script **mueve y no copia**: una copia tendría otro id y habría dos verdades.
- **Renombrar tampoco cambia el enlace.** Solo se renombra lo que **no** traía el nombre buscable; el nombre que puso Meet se conserva íntegro entre paréntesis, y `revertirMovimientos()` restaura nombre **y** carpeta.
- **Lo que sí cambia: el acceso que se heredaba de la carpeta.** Los permisos propios del archivo (con quién lo compartiste explícitamente) viajan con él, pero quien llegaba a él *porque tenía acceso a la carpeta de Meet* deja de tener ese camino, y quien tenga acceso a la carpeta de grabaciones lo gana. Como la carpeta destino es justo la que está publicada a los estudiantes, el efecto va en la dirección deseada — pero conviene saberlo.
- **No se borra nada, nunca.** Las subcarpetas de reunión quedan vacías en su sitio y se cuentan en el registro (`subcarpetas vaciadas=`).

## Cómo decide a qué asignatura pertenece cada grabación

Tres criterios en cascada, y una cuarta salida que es **no tocar**:

1. **El nombre ya trae el subject canónico.** Meet nombra el archivo con el título del evento desde el que se inició la reunión, y esos títulos los genera este repositorio (`26V04 - 54448 - Trabajo de Grado 2 - Sesion 01`). Se mueve tal cual, sin renombrar.
2. **Cruce con tu Calendar por fecha y hora.** Si el nombre no trae el subject (pasa cuando la reunión se inicia desde la sala y no desde el evento), busca el encuentro de esa hora en tu calendario y, si hay **exactamente uno**, mueve y renombra al nombre canónico. El Calendar es la autoridad: ya contiene las reprogramaciones —TG2 dictó la Sesión 01 el **viernes 14/08/2026**, no el lunes— y por eso el script **sigue funcionando el semestre que viene sin tocar una línea**. Dos detalles que evitan publicar una reunión ajena con nombre de clase: la marca de tiempo del nombre tiene que caer **dentro** del encuentro (se admiten 15 min antes del inicio, nada después del final), y si el nombre **no trae hora** solo queda la fecha de creación del archivo, que es posterior a la clase: entonces se mira hacia **atrás** (6 h) y solo valen encuentros ya terminados. Nunca «el día del archivo» — a las 00:20 ese día ya es el siguiente.
3. **El código de sala de Meet**, para desempatar y sobre todo para **desmentir**: si la sala es la de Proyecto I y el único encuentro de esa hora es de TG3, **no se mueve** (antes se movía, y el registro decía «+ sala Proyecto I» como si la sala lo hubiera confirmado).
4. **Si no lo sabe, no lo mueve.** Sale en `--- sin clasificar ---` con el motivo. Los cuatro lunes festivos de 2026 (17/08, 12/10, 02/11, 16/11) no tienen clase: una grabación de esas fechas es una tutoría, un jurado o una reunión ajena y **no** debe acabar en la carpeta que ven 100+ estudiantes.

| Asignatura | Grupos | Horario | ¿Sala en config? |
|---|---|---|---|
| Proyecto I | 54ES4 | lunes 20:00–22:00 | sí |
| Creatividad y Pensamiento Innovador | 54408 | miércoles 17:00–18:00 | **pendiente** |
| Investigación Ciencia y Tecnología | 53339 | jueves 17:00–18:00 | **pendiente** |
| Trabajo de Grado 2 | 54448 | lunes 17:00–18:00 | **pendiente** |
| Trabajo de Grado 3 | 54450/54466/54467 | martes 17:00–18:00 | **pendiente** |

Las salas «pendientes» no impiden nada (el criterio 2 no las necesita), pero conviene pegarlas: son la red de seguridad cuando una grabación no trae el nombre del evento. Las imprime el propio `PRINCIPAL - Crear encuentros con invitados.gs` al crear la serie; van a `config/cursos/carga_academica_2026.json → cursos.<key>.meet` y después se regenera este `.gs`.

## Otra institución: los perfiles

Este `.gs` y este runbook los escribe un generador que lleva **un perfil por institución** (`config/slides/build_apps_script_grabaciones.py` → `PERFILES`). Sin argumentos usa `CUN`, que es lo de siempre; con un argumento, ese perfil:

```
python config/slides/build_apps_script_grabaciones.py            # CUN
python config/slides/build_apps_script_grabaciones.py PLANTILLA  # otra institución
```

Si le pides un perfil que no existe, te lista los que hay y no escribe nada. Cada perfil declara: nombre de la institución y correo, zona horaria y desfase UTC esperado, la marca que identifica un encuentro en el título del evento, el patrón del asunto, los nombres de carpeta de origen que se usan para sugerir candidatos, el id del calendario, las salas de Meet y **los enlaces de las carpetas de Drive, pegados tal cual**. Los perfiles que no son el de la CUN escriben sus dos archivos con el nombre sufijado, así que no se pisan.

## Lo que NO se puede parametrizar

Un perfil cambia constantes, no supuestos. Estos siguen ahí, y conviene leerlos antes de prometerle esto a otra institución:

- **La clasificación va por el Calendar, y eso no es opcional.** El número de sesión del *nombre del archivo* no sirve: está medido —los 19 artefactos reales de la carpeta decían todos «Sesion 01»— porque Meet congela el título del evento con el que se estrenó la sala. Así que la institución necesita **tener los encuentros en el Calendar** y titularlos de forma reconocible (`MARCA` y `RX_SUBJECT`). Sin eso, el script no clasifica nada y todo se queda quieto: no falla, no hace.
- **El nombre que Meet le pone al archivo es de Meet, no de la institución.** `RX_FECHA` es la misma para todos los perfiles a propósito: no está documentada por Google y ya cambió una vez sin avisar. Si cambia otra vez, se arregla en un sitio. **Y hoy está sin arreglar:** medido sobre los archivos reales de la carpeta, ese patrón **no caza ninguno** —Meet los nombra `2026 08 13 17 00 GMT-05 00`, con espacios y sin dos puntos—, así que la hora del nombre nunca se usa y todo pasa por el respaldo aproximado (fecha de creación, mirando hacia atrás). Corregirlo cambia el comportamiento y se decide aparte; y mientras no cace, poner otro `DESFASE_ESPERADO` en un perfil nuevo no cambia nada.
- **`DESFASE_ESPERADO` es uno solo.** Vale donde no hay horario de verano (Colombia). Donde sí lo hay, media parte del año la hora del nombre se descarta y todo cae al respaldo por fecha de creación: sale más «AMBIGUO», nunca un movimiento erróneo. Y un huso a media hora (`+05:30`) no se distingue de `+05`.
- **Una cuenta, un Drive, un organizador.** Apps Script solo ve el Drive de su dueño. Si la clase la graba otra persona, el archivo nace en *su* Mi unidad y ningún script tuyo lo ve. Se instala un proyecto por organizador; no es un parámetro.
- **Supone Mi unidad, no unidades compartidas.** Con una unidad compartida `DriveApp` ya no basta y mover el vídeo allí transfiere su propiedad. Eso sería otro camino de código, no otro valor en el perfil.
- **Los topes son cuota de Google.** `CADA_MIN`, `LIMITE_MS`, `MAX_*`: se pueden bajar, no subir. Y la cuota de disparadores de una cuenta **sin** Workspace es bastante menor: ahí `CADA_MIN = 30` deja de caber y hay que espaciarlo más.
- **Las carpetas de origen no se eligen por nombre, nunca.** Los nombres los pone Google (y los renombró en julio de 2026): `NOMBRES_ORIGEN` solo sirve para *sugerir* candidatos en el registro. El id —o el enlace— lo pega una persona.
- **La prosa del `.gs` es de la CUN.** Habla de «estudiantes», de «tutorías y jurados», del correo de bienvenida y de rutas de este repositorio. Se deja tal cual a propósito: parametrizar los textos del cuerpo obligaría a tocar el código que ya funciona, y ese es el riesgo que no compensa. Léelos como ejemplos, no como descripción de tu institución.

## Si algo sale mal

| Lo que ves | Qué pasa y qué haces |
|---|---|
| `ORIGEN : SIN CONFIGURAR — no se moverá nada` | Te saltaste el paso 2. El registro te lista candidatos con su id: copia el de «Google Meet» y pégalo en `ORIGEN_ID`. |
| `SIMULAR = true: NO se movió nada de verdad` | Sigue en modo simulación. Paso 4. |
| `ERROR en «…»: probablemente Drive creó un ATAJO en vez de mover` | No tienes permiso para mover a la carpeta destino. Drive falla en silencio dejando un atajo, así que el script comprueba el resultado y lo cuenta como `fallidos=`. Revisa que la carpeta de grabaciones sea tuya (o que puedas escribir en ella), **borra a mano el atajo que haya quedado en ella** y vuelve a ejecutar. |
| Un archivo sale en `--- sin clasificar ---` con `AMBIGUO` | Había dos encuentros que encajaban a esa hora. Muévelo a mano; el script no adivina. |
| `no hay ningún encuentro en el Calendar …` | Lo más probable: **la serie de encuentros de ese curso todavía no existe**. Créala con `PRINCIPAL - Crear encuentros con invitados.gs` del curso —**no necesitas la sala de antemano: ese script la crea y la imprime**; el enlace que imprime se pega en `carga_academica_2026.json → cursos.<key>.meet` y después se regenera este `.gs`— y ejecuta `reintentarPendientes()`. Si la serie ya existe y aun así sale esto, era una tutoría, un jurado o una reunión ajena: **no** debe publicarse. |
| `la sala dice «X» y … no es de esa asignatura` | El desempate por sala **desmintió** la clasificación: se quedó quieto a propósito. Comprueba la sala en `carga_academica_2026.json` y, si el archivo era de clase, muévelo a mano. |
| `sin encuentro en el Calendar … (fecha aproximada)` | El nombre no traía hora y hubo que usar la fecha de creación del archivo (se buscan encuentros terminados en las 6 h anteriores). Si de verdad era una clase, muévela a mano y renómbrala con el título del evento. |
| `ya intenté moverlo y Drive dejó un ATAJO` | El archivo está **aparcado a propósito**: reintentarlo cada pasada llenaría de atajos la carpeta que ven los estudiantes. Arregla el permiso sobre la carpeta destino, borra los atajos que hayan quedado y ejecuta `reintentarPendientes()`. |
| `descartado(s) en pasadas anteriores` / `Aparcados N archivo(s) sin clasificar` | Normal: lo que no se puede clasificar (tutorías, jurados) se deja de mirar durante 24 h para que no se coma el cupo de la pasada y tape las grabaciones nuevas. Se vuelve a mirar solo con `reintentarPendientes()` o cuando pasen esas 24 h. |
| `AVISO: hay N archivo(s) en el origen … pero NINGUNO se pudo clasificar` | El fallo silencioso que sí importa. Casi siempre falta la serie de encuentros en el Calendar; lee los motivos de arriba. |
| `AVISO: no encontré NINGÚN archivo … y hubo N encuentro(s) en las últimas 48 h` | O no grabaste, o Google volvió a cambiar la carpeta, o **la grabación la inició otra persona** — en ese caso el archivo nace en el Drive de esa persona y ningún script tuyo puede verlo. Graba siempre tú, como organizador. |
| `AVISO: registro recortado en N entrada(s)` | El historial de deshacer solo guarda lo reciente (tope de tamaño de las propiedades del proyecto). Lo antiguo ya no se puede revertir automáticamente; moverlo a mano, sí. |
| «Se ha excedido el tiempo máximo de ejecución» | No debería salir: el script corta solo a los 4,5 min y avisa de cuántos archivos deja para la próxima. Si sale, vuelve a ejecutar (el disparador lo haría solo). **No hay estado guardado del barrido**: la pasada siguiente vuelve a empezar, pero mirando **primero lo más nuevo**, así que la grabación de hoy entra antes que el residuo viejo. |
| Un vídeo llegó a la carpeta pero su transcripción no | Normal: los artefactos de Meet aparecen en momentos distintos (los subtítulos pueden tardar horas). La siguiente pasada la recoge y le pone el mismo nombre. |

## Cómo deshacer

- **`revertirMovimientos()`** — devuelve cada archivo del registro a su carpeta y a su nombre anteriores, del más reciente al más antiguo. No borra nada y no toca lo que no movió este script. Con `SIMULAR = true` solo dice qué haría.
- **`quitarDisparador()`** — para el automatismo. Lo ya movido sigue movido.
- **`reintentarPendientes()`** — vuelve a mirar lo aparcado: lo que no se pudo clasificar (aparcado 24 h para que el residuo no tape las grabaciones nuevas) y lo que **falló al moverse** (aparcado hasta aquí para no llenar de atajos la carpeta publicada). Ejecútalo después de crear la serie de encuentros que faltaba, de pegar una sala en el JSON o de arreglar el permiso del destino. No mueve nada por sí solo.
- **`olvidarRegistro()`** — suelta el historial. **No devuelve ningún archivo**: después de esto `revertirMovimientos()` ya no puede deshacer lo olvidado. La idempotencia no depende de él (lo ya movido no vuelve a moverse porque ya no está en el origen).
- **Quitarlo del todo:** `quitarDisparador()` → borra el proyecto de Apps Script. No queda ninguna credencial que revocar.

## De dónde sale cada dato

- Perfil `CUN` — `config/slides/build_apps_script_grabaciones.py` → `PERFILES`. Ahí están la zona horaria, el desfase, la marca, el patrón del asunto, el calendario y los enlaces de las carpetas.
- Carpeta destino `1EHck-ZdbwwLJtDk2NsS4UDL1UMf1sLqZ` — de `config/cursos/carga_academica.py` → `GRABACIONES_URL`, que es **una sola para los 5 cursos y todos los periodos** y ya está publicada en el correo de bienvenida (`config/slides/build_correo_bienvenida.py`) y en el LEEME del estudiante (`config/slides/sync_clases_estudiantes.py`). Por eso no hay una carpeta por asignatura: cambiarla dejaría mintiendo documentos que ya están en manos de los estudiantes.
- Patrón del nombre buscable — `config/cursos/sesiones_cun.py` → `subject_encuentro()`. El periodo va delante justamente porque esa carpeta acumula todos los periodos.
- Horarios, grupos y salas de Meet — `config/cursos/carga_academica_2026.json`.
- Los eventos del calendario los crea `config/slides/build_calendar_encuentros.py` → `PRINCIPAL - Crear encuentros con invitados.gs` (uno por grupo, en `<Curso>/2026/<grupo>/`). Este script **los lee**, no los toca.

Si cambia cualquiera de esos datos, regenera: `python config/slides/build_apps_script_grabaciones.py CUN`.
