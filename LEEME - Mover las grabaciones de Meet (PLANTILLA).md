# Mover las grabaciones de Meet — automático, sin credenciales

**1 sola carpeta destino** · barrido cada 30 minutos · un único proyecto de Apps Script, instalado una vez

> **Archivo generado — no editar a mano.** Perfil `PLANTILLA`. Regenerar: `python config/slides/build_apps_script_grabaciones.py PLANTILLA`

## Qué vas a conseguir

Que cada grabación de Meet salga sola de donde Google la deja —la carpeta por omisión de Meet en tu Mi unidad: hoy «Meet Recordings»— y aparezca en la **carpeta única de grabaciones** () en **la carpeta de su sesión**, que se llama con el nombre canónico del encuentro, el mismo con el que lo titula tu Calendar (`Asignatura de ejemplo - Sesion 01`). Los **tres** archivos que deja cada encuentro —vídeo, transcripción y chat— caen juntos ahí. **Unos diez minutos** de instalación, una sola vez; después no hay que volver a tocarlo, ni el semestre que viene.

No necesita contraseña, ni token, ni contraseña de aplicación (y en muchas cuentas institucionales el administrador ni siquiera las permite), ni que tu computador esté encendido. Apps Script corre en los servidores de Google con tu propia sesión.

Son dos archivos, y esto es **uno solo para todos los cursos** (no hay una copia por grupo): `PRINCIPAL - Mover grabaciones de Meet (PLANTILLA).gs`, que es el que se pega en Apps Script, y este runbook.

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

**El paso previo:** los encuentros de la asignatura tienen que **existir en tu Calendar**. Cuando Meet no nombra el archivo con el título del evento (pasa siempre que la reunión se inicia desde la sala), lo único que puede decir de qué clase es resulta ser el propio Calendar. Esas series las creas tú en el Calendar de esa misma cuenta, y sus títulos tienen que llevar la MARCA (« - Sesion ») y encajar con `RX_SUBJECT`: las dos cosas las declara el perfil `PLANTILLA`. Crea antes la serie de encuentros de cada asignatura en el Calendar. Sin eso, cada grabación saldrá en `--- sin clasificar ---` con «no hay ningún encuentro en el Calendar…» y se quedará quieta: no es que el automatismo no sirva, es que falta el paso anterior.

Y un supuesto que conviene confirmar el primer día: **la carpeta de grabaciones está en Mi unidad**, no en una unidad compartida. Si estuviera en una unidad compartida, `DriveApp` no bastaría (haría falta el servicio avanzado de Drive) y —lo importante— mover el vídeo allí **transferiría su propiedad a la institución de forma irreversible**. Si algún día se decide eso, se decide a propósito y no como efecto secundario de este script.

## Paso a paso

### 1. Abre Apps Script con la cuenta INSTITUCIÓN

**https://script.google.com** con **tu.correo@ejemplo.edu**. Tiene que ser la cuenta del **organizador** de las clases: las grabaciones nacen en *su* Mi unidad y ningún script puede ver el Drive de otra persona. **Nuevo proyecto** → borra el `function myFunction()` de fábrica → pega **todo** el contenido de `PRINCIPAL - Mover grabaciones de Meet (PLANTILLA).gs` → guarda. Ponle un nombre reconocible al proyecto: «Grabaciones».

No hace falta añadir ningún servicio avanzado. Este script usa solo Drive, Calendar y los disparadores, que vienen de serie.

### 2. Pega el `ORIGEN_ID`

En el bloque `// ─── CONFIGURACIÓN ───`, la única constante que sale vacía:

```js
var ORIGEN_ID = '';   // <- pega aquí el ENLACE de tu carpeta de grabaciones de Meet
```

Guarda. Lo demás ya viene puesto desde el perfil: la carpeta destino (`` → id ``), el calendario (`primary`) y las salas de Meet conocidas.

### 3. Ejecuta `verificarGrabaciones()` — siempre, antes que nada

Elige **`verificarGrabaciones`** en el desplegable de arriba y pulsa **Ejecutar**.

La primera vez Google pide permisos: **Revisar permisos** → tu cuenta INSTITUCIÓN → «Google no ha verificado esta aplicación» → **Configuración avanzada** → **Ir a (nombre del proyecto)** → **Permitir**. Es tu propio script; el aviso sale porque no está publicado en ninguna tienda.

`verificarGrabaciones()` **no mueve, no renombra, no borra y no instala nada**. Solo escribe en el registro (*Ver → Registro de ejecución*):

- el modo (`SIMULACIÓN` / `REAL`), la zona horaria y los márgenes;
- el **calendario** con su nombre y su id — comprueba que es el tuyo de INSTITUCIÓN;
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

Guarda y ejecuta **`moverGrabaciones()`**. Verás una línea `carpeta creada: …` por sesión nueva, una `movido: …` por archivo y el resumen `movidos=… · renombrados=… · sin clasificar=… · fallidos=… · subcarpetas creadas=… · a la raíz sin confirmar=… · en gracia=… · descartados antes=… · sin mirar por falta de tiempo=… · subcarpetas vaciadas=…`. Abre la carpeta destino y compruébalo con tus ojos: dentro verás una carpeta por materia y, en cada una, sus tres archivos.

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
- **No se borra nada, nunca.** Las subcarpetas que Meet deja en el origen quedan vacías en su sitio y se cuentan en el registro (`subcarpetas vaciadas=`).
- **Meter el archivo en una subcarpeta tampoco cambia el enlace.** Es el mismo movimiento de Drive que antes, solo que a un destino más adentro: el `fileId` no cambia y `revertirMovimientos()` lo devuelve igual a su carpeta y su nombre de antes.

## Una carpeta por sesión, con los tres archivos dentro

Cada encuentro deja **tres** archivos en Meet, con el mismo nombre salvo el final: `… - Recording`, `… - Transcript` y `… - Chat`. Sueltos en la carpeta destino se mezclan con los de las demás sesiones, así que el script crea **una subcarpeta por sesión** dentro del destino y los deja ahí. La subcarpeta se llama **exactamente** con el nombre del encuentro —el de siempre, «periodo - grupo - asignatura - sesión»—, así que lo prometido se sigue cumpliendo por partida doble: **buscando** ese nombre aparece la carpeta (y los archivos, que también lo llevan), y **navegando** se ve una carpeta por sesión.

- **El número de sesión sale del Calendar, no del nombre del archivo.** `Asignatura de ejemplo - Sesion 04` y no `… - Sesion 01`. Meet **congela** el título del evento con el que se estrenó la sala: está medido, los 19 artefactos reales de la carpeta decían «Sesion 01», también los del 11, 13, 18 y 20 de agosto. Si mandara el nombre, **todas** las sesiones del semestre caerían en la misma carpeta. Lo gobierna `CALENDAR_MANDA_SESION`.
- **Pero el Calendar manda en el número, no en la asignatura.** Si el encuentro que encaja en esa hora es de **otro curso** que el que dice el nombre del archivo, eso no es un número congelado: es una contradicción, y el nombre gana. Meet bautiza el archivo con el título de la sala desde la que se grabó, y hay una sala por curso, así que el nombre acierta la asignatura aunque mienta en la sesión. Sin este freno, una clase de un curso podría publicarse dentro de la carpeta de otro y con el nombre de otro. Cuando pasa, sale un `AVISO:` con los dos nombres.
- **Si la carpeta ya existe, se reutiliza.** Se busca *dentro* de la carpeta destino (nunca en todo tu Drive, que podría devolver una carpeta ajena que se llame igual), así que ejecutarlo dos veces no crea dos carpetas. Si encontrara **dos** con el mismo nombre usa la primera y te lo dice en el registro: es señal de que algo se duplicó.
- **El que llega tarde entra en la misma carpeta.** La transcripción puede aparecer horas después del vídeo; la pasada siguiente la mete en la carpeta que ya está. No hace falta que los tres estén a la vez.
- **Y si uno de los tres no se sabe clasificar por su cuenta, viaja con sus hermanos.** Los tres comparten el nombre hasta la marca de tiempo, así que el que sí se identificó decide por todos. Si ninguno se identifica, ninguno se mueve: **nunca** se crea una carpeta «desconocido». Por esa carpeta pasan 100+ estudiantes.
- **La carpeta solo se abre con un nombre que haya confirmado el Calendar.** Si de una grabación se sabe la asignatura (lo dice su nombre) pero **no** la sesión —no hay encuentro a esa hora, hay dos, o el nombre no traía hora—, el archivo **se mueve igual**, pero suelto a la carpeta destino, como antes de que existieran las subcarpetas. Abrirle una carpeta con el número que trae el nombre plantaría, al lado de la carpeta buena, otra que dice ser la «Sesion 01» y no lo es, y un estudiante entraría a ver la clase equivocada. El resumen los cuenta en `a la raíz sin confirmar=N` y el registro dice por qué. Se arregla creando la serie de encuentros de ese curso en el Calendar (los que ya estén en el destino se arrastran a mano: el script no vuelve a mirar allí).

Volver al reparto plano de antes es una constante, `AGRUPAR_POR_MATERIA = false`: todo suelto en la carpeta destino, sin subcarpetas, sin tocar nada más. La lista de sufijos que identifican los tres artefactos también es una constante (`SUFIJOS_ARTEFACTO`), porque esa convención es de Google y ya la ha cambiado antes.

## Cómo decide a qué asignatura pertenece cada grabación

Tres criterios en cascada, y una cuarta salida que es **no tocar**:

1. **Cruce con tu Calendar por fecha y hora, que es quien manda.** Busca el encuentro de esa hora en tu calendario y, si hay **exactamente uno**, mueve y renombra al nombre canónico. El Calendar es la autoridad: ya contiene las reprogramaciones (una clase movida de día sigue teniendo su evento en la fecha real en que se dio) y —lo que de verdad importa— es el único que sabe el **número de sesión de verdad**. Por eso el script **sigue funcionando el semestre que viene sin tocar una línea**. Dos detalles que evitan publicar una reunión ajena con nombre de clase: la marca de tiempo del nombre tiene que caer **dentro** del encuentro (se admiten 15 min antes del inicio, nada después del final), y si el nombre **no trae hora** solo queda la fecha de creación del archivo, que es posterior a la clase: entonces se mira hacia **atrás** (6 h) y solo valen encuentros ya terminados. Nunca «el día del archivo» — a las 00:20 ese día ya es el siguiente.
2. **El nombre del archivo, como respaldo.** Meet nombra el archivo con el título del evento desde el que se estrenó la sala, y esos títulos los pone tu Calendar (`Asignatura de ejemplo - Sesion 01`). Dice bien la **asignatura**, pero el **número de sesión** viene congelado —los 19 artefactos reales decían «Sesion 01»—, así que solo se usa cuando el Calendar no puede confirmar nada: no hay encuentro a esa hora, hay dos, o el nombre no traía hora. Entonces el archivo se mueve igual (como siempre se ha movido) y el registro dice que el número de sesión puede venir congelado. Se cambia con `CALENDAR_MANDA_SESION = false`, que devuelve el mando al nombre.
3. **El código de sala de Meet**, para desempatar y sobre todo para **desmentir**: si la sala es la de una asignatura y el único encuentro de esa hora es de otra, **no se mueve**. La sala sirve para desmentir, no para confirmar.
4. **Si no lo sabe, no lo mueve.** Sale en `--- sin clasificar ---` con el motivo. Un día sin clase (festivo, receso, una reunión que no era del curso) no tiene encuentro en el Calendar: la grabación se queda quieta, que es lo que debe pasar.

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
- **El nombre que Meet le pone al archivo es de Meet, no de la institución.** `RX_FECHA` es la misma para todos los perfiles a propósito: no está documentada por Google y ya cambió una vez sin avisar. Si cambia otra vez, se arregla en un sitio. **Ya cambió una vez y está corregido:** Meet dejó de escribir los separadores y hoy nombra `2026 08 13 17 00 GMT-05 00`, con espacios y sin dos puntos; el patrón anterior no cazaba ninguno (medido: 0 de 19) y todo caía al respaldo aproximado por fecha de creación. El de ahora acepta las dos formas (7 de 7). Importa más que antes: la hora del nombre es la señal con la que el Calendar corrige el número de sesión, así que si Google la vuelve a cambiar, lo que se ve es que las carpetas empiezan a llamarse `Sesion 01`.
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
| `no hay ningún encuentro en el Calendar …` | Lo más probable: **la serie de encuentros de ese curso todavía no existe**. Créala en tu Calendar con un título que encaje con `RX_SUBJECT`; si esa asignatura tiene sala fija de Meet, pégala en `salas` del perfil y regenera y ejecuta `reintentarPendientes()`. Si la serie ya existe y aun así sale esto, era una tutoría, un jurado o una reunión ajena: **no** debe publicarse. |
| `la sala dice «X» y … no es de esa asignatura` | El desempate por sala **desmintió** la clasificación: se quedó quieto a propósito. Comprueba la sala en `SALAS` (que sale de `salas` del perfil) y, si el archivo era de clase, muévelo a mano. |
| `sin encuentro en el Calendar … (fecha aproximada)` | El nombre no traía hora y hubo que usar la fecha de creación del archivo (se buscan encuentros terminados en las 6 h anteriores). Si de verdad era una clase, muévela a mano y renómbrala con el título del evento. |
| `ya intenté moverlo y Drive dejó un ATAJO` | El archivo está **aparcado a propósito**: reintentarlo cada pasada llenaría de atajos la carpeta que ven los estudiantes. Arregla el permiso sobre la carpeta destino, borra los atajos que hayan quedado y ejecuta `reintentarPendientes()`. |
| `descartado(s) en pasadas anteriores` / `Aparcados N archivo(s) sin clasificar` | Normal: lo que no se puede clasificar (tutorías, jurados) se deja de mirar durante 24 h para que no se coma el cupo de la pasada y tape las grabaciones nuevas. Se vuelve a mirar solo con `reintentarPendientes()` o cuando pasen esas 24 h. |
| `AVISO: hay N archivo(s) en el origen … pero NINGUNO se pudo clasificar` | El fallo silencioso que sí importa. Casi siempre falta la serie de encuentros en el Calendar; lee los motivos de arriba. |
| `AVISO: no encontré NINGÚN archivo … y hubo N encuentro(s) en las últimas 48 h` | O no grabaste, o Google volvió a cambiar la carpeta, o **la grabación la inició otra persona** — en ese caso el archivo nace en el Drive de esa persona y ningún script tuyo puede verlo. Graba siempre tú, como organizador. |
| `hay 2 carpetas que se llaman «…»` | Dentro del destino hay dos carpetas con el nombre de esa sesión. El script usa la **primera** y sigue —no duplica—, pero los estudiantes verían la sesión partida en dos sitios: junta los archivos a mano y borra la que sobre. |
| `no pude crear la subcarpeta «…»` / `sin subcarpeta (no movidos)=N` | No pudo crear la carpeta de la sesión, casi siempre por permiso de escritura sobre la carpeta destino. Esos archivos **no se mueven** a propósito: soltarlos en la raíz del destino rompería justo lo que se viene a arreglar. Se reintentan solos en la pasada siguiente. Si prefieres el reparto plano, `AGRUPAR_POR_MATERIA = false`. |
| `a la raíz sin confirmar=N`: archivos sueltos en el destino, sin carpeta | Se sabe de qué asignatura son —lo dice su nombre— pero el Calendar no confirmó **qué sesión**, y el número que trae el nombre lo congeló Meet. Se mueven igual (es el comportamiento de siempre), pero no se les abre una carpeta que mentiría. Comprueba que la serie de encuentros de ese curso existe en el Calendar a esa hora y que el nombre del archivo trae la marca de tiempo. Los que ya estén sueltos en el destino se arrastran a mano: el script no vuelve a mirar allí. |
| Una carpeta dice `Sesion 01` y la clase era otra | **Este script ya no crea esa carpeta** (desde el 25/08/2026 solo abre carpetas con un nombre confirmado por el Calendar). Si la ves, es de una pasada anterior a ese cambio o la creó alguien a mano: renómbrala o junta los archivos con los de la carpeta buena. |
| `AVISO: «…» dice ser de «…» y el encuentro que encaja en esa hora es «…»` | El nombre del archivo y el Calendar no coinciden **en la asignatura**, no solo en el número. El script no renombra nada y trata el archivo por su nombre. Casi siempre es una grabación hecha desde la sala de otro curso, o una tutoría en el horario de una clase. Si de verdad son el mismo curso, es que el título del evento cambió después de estrenar la sala — y hasta que vuelvan a coincidir, el número de sesión se queda congelado. |
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

- Perfil `PLANTILLA` — `config/slides/build_apps_script_grabaciones.py` → `PERFILES`. Ahí están la zona horaria, el desfase, la marca, el patrón del asunto, el calendario y los enlaces de las carpetas.
- Carpeta destino — el enlace que el perfil `PLANTILLA` trae en `destino_url`, pegado tal cual (`todavía SIN RELLENAR`). Si esa carpeta ya está publicada a los estudiantes, cambiarla dejaría mintiendo lo que ya está en sus manos: se cambia en el perfil y se regenera.
- Patrón del nombre buscable — `rx_subject` del perfil, que es la nomenclatura con la que tu institución titula los encuentros del Calendar.
- Salas de Meet — `salas` del perfil: `{código: nombre de la asignatura tal como aparece en el título del evento}`.
- Los eventos del calendario los crea quien monte la serie de encuentros en tu institución. Este script **los lee**, no los toca.

Si cambia cualquiera de esos datos, regenera: `python config/slides/build_apps_script_grabaciones.py PLANTILLA`.
