# Recordatorios automáticos de entregables — qué canal usar

**15/08/2026.** Qué opciones hay para avisarles a los 282 estudiantes matriculados cuándo abre y
cuándo cierra cada entregable, sin intervención manual, sabiendo que **esta cuenta de Gmail no puede
generar contraseñas de aplicación** (el administrador de Workspace de la CUN tiene esa opción
deshabilitada; el mensaje «La opción de configuración que buscas no está disponible para tu cuenta»
no se arregla desde la cuenta del Docente).

## La respuesta corta

**No es el foro. Son las fechas de las tareas.** Y la corrección importa, porque durante un día
entero este documento afirmó lo contrario.

CDigital tiene **apagado el correo del proveedor «Mensajes suscritos del foro»** en los valores por
omisión del sitio (§2b). Publicar en el foro «Avisos» deja el aviso **visible dentro del aula** y
manda un *push* a quien tenga la app de Moodle — pero **no manda correo** a los 282. La suscripción
forzada garantiza que el estudiante está suscrito, no que le llegue nada.

Lo que **sí** sale por correo, sin pedirle nada a nadie, son los avisos de vencimiento de las
**tareas** (`assign`), que Moodle trae encendidos de fábrica y que en CDigital siguen encendidos:

| Proveedor | Cuándo dispara | Con qué antelación exacta |
|---|---|---|
| `mod_assign_assign_due_digest` | resumen de lo que vence | **7 días** (`INTERVAL_DUE_DIGEST = WEEKSECS`) |
| `mod_assign_assign_due_soon` | la tarea está por cerrar | **48 horas** (`INTERVAL_DUE_SOON = DAYSECS * 2`) |
| `mod_assign_assign_overdue` | la tarea se cerró y no entregó | **2 horas después** (`INTERVAL_OVERDUE = HOURSECS * 2`) |

Y son mejores que el foro en lo que de verdad cuenta: van **por estudiante**, y
`get_users_within_assignment()` **excluye a quien ya entregó**. No le insiste a quien ya hizo el
trabajo. Respetan las excepciones por usuario y por grupo (`ao.duedate`). El precio: exigen
`cm.visible = 1 AND c.visible = 1` —la actividad y el curso visibles— y sólo cubren **tareas**.

Así queda repartido el semestre, y hay un hueco que hay que decir en voz alta:

| Entregable | Canal que de verdad le llega por correo |
|---|---|
| **ACAs** (son tareas `assign`) | **Nativo de Moodle.** Basta la `duedate` correcta y el ítem visible |
| **Quices y Parciales** (`quiz`) | `mod_quiz_quiz_open_soon` avisa cuando **abre**. Del **cierre no avisa nada** |
| **Coevaluación** (foro) | Nada por correo |

Para ese hueco —el cierre de los cuestionarios— sólo hay dos salidas reales: pedirle al
administrador que devuelva el correo del proveedor de foros a su valor de fábrica (§2b), o mandarlo
desde el buzón del Docente con **Apps Script + `MailApp`** (§3), que no necesita contraseña ni token.

Lo que sí sigue en pie del diseño anterior: **el campus hace de reloj.** Con «Mostrar período»
(`timestart`) se publica hoy un aviso que el cron suelta el día indicado, sin AWS, sin GitHub
Actions, sin Programador de tareas y sin que este computador esté encendido (§4).

## 1. La herramienta ya está escrita

```bash
# Qué se mandaría hoy. No manda nada: simula.
python config/cursos/recordatorios.py

# Todos los avisos del semestre de un vistazo (226 avisos en 100 días, 7 aulas)
python config/cursos/recordatorios.py --calendario

# Ensayo de un día concreto
python config/cursos/recordatorios.py --fecha 2026-08-30

# PROGRAMAR el semestre completo: publica cada aviso con su fecha y el campus los va soltando
python config/cursos/recordatorios.py --canal campus --programar --confirmar

# Un solo día, ahora mismo (para el arranque, o si algo se corrió)
python config/cursos/recordatorios.py --canal campus --confirmar
```

Cuatro reglas que trae puestas:

1. **Las fechas salen de `config/cursos/fechas_entrega_aca.py`**, no del aula ni de este archivo.
   Mover una entrega es moverla ahí; el recordatorio y la ventana del aula van detrás.
2. **Sólo avisa de lo que el estudiante puede ver.** Si la actividad está oculta, el enlace sería un
   404: se omite y se dice. Los recordatorios se encienden solos a medida que se activan los ítems.
3. **Simula por defecto.** Sin `--canal campus --confirmar` no sale nada.
4. **No repite.** Lleva registro en `%LOCALAPPDATA%\cdigital-cun\recordatorios_enviados.json`, fuera
   del repositorio. Correrlo dos veces el mismo día no manda el aviso dos veces.

Cuándo avisa: el día que abre, y **7, 3 y 1 días antes** del cierre, más el mismo día del cierre
(`DIAS_ANTES` en el archivo). Cada aviso dice qué es, de qué tipo, **cuánto pesa y de qué corte**,
cuándo abre, cuándo cierra a las 23:59, cuándo se publica la nota, y lleva el enlace directo a la
actividad.

## 2. Lo verificado

Verificado contra el servidor real, no supuesto:

- Los **7 foros «Avisos»** existen, están visibles y tienen **suscripción forzada**. Nadie se puede
  dar de baja del aviso.
- Los 7 ids de instancia se descubren automáticamente (aparecen de tres formas distintas según cómo
  pinte el aula la página; se prueban las tres).
- El formulario de publicación se lee y el envío se arma completo en los 7, con `mailnow` y con
  `timestart`.
- `timestart` retiene el correo: la consulta del cron de foros exige que la fecha de inicio ya haya
  pasado, y **`mailnow` no se la salta** —van unidas—. Un aviso programado se puede borrar antes de
  su fecha **sin que salga ningún correo**: por eso el modo programado es reversible.
- **El envío llega, y se comprobó sin escribirle a ningún estudiante.** En Creatividad hay un foro
  `Prueba de recordatorios` **oculto** y de suscripción **opcional**, con **un único suscriptor: el
  Docente** (`cmid 7706181`, instancia `909536`). Publicando ahí con `mailnow`, el correo llegó al
  buzón del Docente el 15/08 a las 12:20, remitido por `restablecimiento_digital1@cun.edu.co` con
  asunto `EI004/54408/26V04/B1/FINVV/FINVI: [PRUEBA 2 · 17:19] Comprobación de correo del foro`.
  **Ese foro se conserva a propósito**: es el único banco de pruebas seguro que hay: no existe aula
  de pruebas y la más pequeña tiene 13 estudiantes.

### 2a. Y lo que se cayó al comprobarlo

**La primera prueba no llegó.** Este documento afirmó durante un día que el envío estaba verificado,
y era falso: se había verificado que el POST publicaba el tema, no que el correo saliera. La causa
del silencio no fue el foro ni el cron, sino la cuenta: el proveedor «Mensajes suscritos del foro»
tenía **Web y Email apagados y sólo Móvil encendido**. Nada podía entregarse. Con los tres
encendidos, la segunda prueba llegó a la primera.

Dos cosas más que hay que tener presentes, porque las dos me llevaron por el camino equivocado:

- **La campana nunca muestra tu propio mensaje de foro.** `message/output/popup/message_output_popup.php`
  se niega a insertar en `message_popup_notifications` cuando `userfrom == userto`, con el comentario
  «*Prevent users from getting popup notifications from themselves (happens with forum notifications)*»,
  y la campana sólo consulta esa tabla. Al probar un envío propio, **la campana vacía no es evidencia
  de nada**: sólo cuenta el buzón.
- **Ocultar el foro sigue sin bastar**, y ahora está comprobado por dos vías. Por código:
  `mod/forum/classes/task/cron_task.php` no mira visibilidad; `mod/forum/classes/subscriptions.php`
  filtra con `get_enrolled_sql()` y con `info_module::filter_user_list()`, que **no hace nada** si el
  ítem no tiene restricciones de acceso (`availability/classes/info.php`: `if (is_null($this->availability)
  || !$CFG->enableavailability) { return $users; }`); la única puerta de visibilidad es
  `forum_user_can_see_post()` → `$cm->uservisible`, y un `editingteacher` la pasa por arquetipo porque
  tiene `moodle/course:viewhiddenactivities`. Y por experimento: **el correo de la PRUEBA 2 salió de un
  foro oculto**. Luego un foro oculto con suscripción *forzada* les llegaría igual a los 50; lo que
  aísla la prueba es la suscripción **opcional**.

### 2b. El hallazgo grave: el sitio trae el correo del foro apagado

`core_user_get_user_preferences` mostró que esta cuenta **no tenía guardada ni una sola preferencia
`message_provider_*`** antes del 15/08 (las que hay son las que se escribieron ese día). Y
`lib/messagelib.php` y `message/classes/output/preferences/notification_list_processor.php` usan la
misma cadena de respaldo: si el usuario no tiene valor propio, manda
`get_message_output_default_preferences()`, el **valor por omisión del sitio**. Luego lo que la
pantalla mostraba —Móvil sí, Web no, Email no— **es el valor del sitio**, y es el que hereda todo
estudiante que nunca haya abierto Preferencias → Notificaciones. Que son casi todos.

Moodle trae ese proveedor con los tres canales encendidos
(`mod/forum/db/messages.php`: `'posts' => ['popup' => MESSAGE_PERMITTED + MESSAGE_DEFAULT_ENABLED,
'email' => …, 'airnotifier' => …]`). **La divergencia la introdujo la institución.** Y no es un
descuido al azar: mirando los 31 proveedores del sitio se ve un criterio claro —apagaron los dos más
ruidosos, `mod_forum_posts` (a Móvil) y `mod_assign_assign_notification` (a nada), y dejaron
intactos los avisos de vencimiento—. Lo que el sitio **sí** manda por correo a un estudiante que no
ha tocado sus preferencias:

| Encendido de fábrica y sigue encendido | Apagado por el sitio |
|---|---|
| `mod_assign_assign_due_soon`, `assign_overdue`, `assign_due_digest` | `mod_forum_posts` → **sólo Móvil** |
| `mod_quiz_quiz_open_soon` (avisa al **abrir**, no al cerrar) | `mod_assign_assign_notification` → **nada** |
| `moodle_enrolcoursewelcomemessage`, `mod_googlemeet_notification` | `moodle_gradenotifications` → sólo campana |
| `enrol_manual_expiry_notification`, `enrol_self_expiry_notification` | `mod_forum_digests`, `mod_feedback_*` → nada |

**Cómo se arregla de raíz, si algún día se puede:** Administración del sitio → Mensajería →
*Preferencias de notificación por omisión* (`/admin/message.php`), marcando Email en «Mensajes
suscritos del foro». Requiere administrador; no se puede desde la cuenta del Docente. Vale la pena
pedirlo por dos razones: arregla el canal para las 7 aulas de una vez, y es volver al valor de fábrica
de Moodle, no un permiso especial.

**Cómo se comprueba, y cómo NO.** Borrar la preferencia con `core_user_update_user_preferences` sin
`value` **no la elimina: escribe vacío**. Eso invalidó la primera medición del valor del sitio y por
poco deja documentado un hallazgo falso. Se detectó con un control: se hizo lo mismo con
`mod_quiz_quiz_open_soon`, que estaba con los tres canales encendidos, y «al borrarlo» apareció con
los tres apagados. La vía buena es el volcado de preferencias, que dice qué claves existen de verdad.

Dos avisos más, menores:

- **El asunto del correo lleva delante el nombre corto del aula**, que es feo y no se puede cambiar
  sin ser administrador: el estudiante ve `EI004/54408/26V04/B1/FINVV/FINVI: Falta 1 día para Quiz 1`.
- **Quien tenga «resumen diario»** (`maildigest > 0`) lo recibirá de madrugada agrupado;
  `mod/forum/classes/task/cron_task.php` desvía a `forum_queue` y `mailnow` tampoco se salta eso.
  En esta cuenta el resumen está en **0 (Sin resumen)**.

## 3. Gmail sin contraseña de aplicación — lo que sí se puede

Por si en algún momento hace falta que el correo salga **del buzón del Docente** (algo personalizado
por estudiante, que el foro no puede hacer porque es público):

| Opción | Cómo | Cuota | Veredicto |
|---|---|---|---|
| **Apps Script + `MailApp` con disparador temporal** | Un `.gs` en Google Drive con un *time-driven trigger*. **Ni contraseña, ni token guardado, ni contraseña de aplicación**: corre en los servidores de Google con la sesión del dueño | 1.500 destinatarios/día (2.000 si todos son `@cun.edu.co`). Los 282 caben de sobra | **La alternativa buena.** Ya hay 6 `.gs` funcionando en el repositorio y las 7 listas de correos (282 direcciones) |
| Gmail API + OAuth (`gmail.send`) | Proyecto en Google Cloud, consentimiento una vez, *refresh token* | 282 envíos = 0,035% de la cuota diaria | Viable, más trabajo. **El refresh token es una credencial: va fuera del repositorio** (que está en git y sincronizado a Drive) |
| Invitaciones de Calendar | Google ya manda recordatorio a los invitados | — | Ya se usa; sirve para las clases, no para los cierres de entrega |
| SMTP relay de Workspace / XOAUTH2 sobre SMTP | — | — | **Descartadas.** La primera necesita un ticket al administrador de la CUN, IP fija y máquina encendida; la segunda pide un permiso mucho mayor que la Gmail API y da menos capacidad |
| Mail merge de Gmail | A mano, desde la interfaz | 1.500/día | No es automático: 2 a 6 horas de trabajo repetitivo por semestre |

## 4. AWS y otros servicios — para qué sí y para qué no

La distinción que importa: **una cosa es el reloj y otra el que manda el correo.**

- **Como reloj, AWS es gratis y sirve:** Lambda (1M peticiones/mes en capa gratuita permanente) +
  EventBridge Scheduler (14M invocaciones/mes gratis). Ojo con el sitio donde se guarda la
  contraseña de CDigital: **Secrets Manager cuesta 0,40 USD por secreto y mes**; el Parameter Store
  estándar es gratis. Pero no hace falta ningún reloj: ya lo trae el campus.
- **Como remitente, Amazon SES está descartado**, y la razón no es el precio (0,10 USD por 1.000
  correos) sino que **no llegarían**: enviar como `@cun.edu.co` exige firmar con DKIM ese dominio, y
  el DNS de `cun.edu.co` no lo controla el Docente. Sin eso, DMARC lo rechaza o lo manda a spam. Lo
  mismo vale para Brevo, Resend, Mailjet, SendGrid y Mailgun — y además sus planes gratuitos topan
  en 100–200 correos/día, por debajo del pico de un día en que vence algo en varias aulas (282).
- Alternativas de reloj sin AWS: **GitHub Actions** (el repo ya está ahí, privado; 2.000 min/mes en
  el plan Free, mínimo cada 5 minutos, con retrasos en horas de mucha carga) o el **Programador de
  tareas de Windows** (gratis, pero exige que el computador esté encendido a esa hora).

Si algún día hace falta un reloj externo —porque los avisos dejen de poder programarse en el
campus—, el orden es: Programador de tareas de Windows → GitHub Actions → Lambda + EventBridge. La
contraseña de CDigital **nunca dentro del repositorio**: hoy vive en
`%LOCALAPPDATA%\cdigital-cun\credenciales.json`, y en GitHub Actions iría como *secret* del
repositorio.

## 5. El plan

**Creatividad ya está hecha, y sirve de plantilla para las otras seis.** El orden que se siguió:

1. **Probar el envío** en un foro oculto de suscripción opcional (§2). Sin esto, publicar es apostar.
2. **Alinear las fechas del aula con el repositorio**, incluidos los visibles:
   `python config/moodle/cdigital.py fechas 115463 --incluir-visibles --confirmar`. Los 8 ítems
   quedaron alineados. Antes de tocar un ítem visible hay que comprobar que **no haya nada
   entregado** —en Creatividad: 0 intentos, 0 envíos con 50 participantes, 0 temas en el foro—, porque
   mover la ventana de algo ya trabajado sí le quita trabajo a alguien.
3. **Programar el semestre**:
   `python config/cursos/recordatorios.py --canal campus --programar --aula 115463 --confirmar`.
   Quedaron **12 avisos** del 12/09 al 27/09; los otros 19 se saltaron porque sus ítems están ocultos.

Un recordatorio con la fecha mala es peor que no mandarlo: por eso el paso 2 va antes del 3. Y como
sólo se avisa de lo visible, **los avisos de los Quices y Parciales aparecerán solos** el día que se
activen esos ítems — basta volver a correr el paso 3, que no repite lo ya publicado.

**El paso 2 dejó de ser sólo higiene: es el canal.** Descubierto lo de §2b, alinear la `duedate` de
las tareas ya no es «que el aula diga lo mismo que la guía», es **lo único que hace que le llegue un
correo al estudiante** — 7 días antes por el resumen, 48 horas antes, y 2 horas después si no
entregó. De ahí que el orden correcto de prioridades hoy sea:

**Lo que queda de este semestre**, para las otras seis aulas:

1. Las **19 discrepancias de fechas** que siguen en pie (`ALISTAMIENTO CDigital 2026-08-15.md` §5:
   Proyecto I anuncia sus dos ACAs para **enero de 2028**). **Esto es ahora lo más urgente de todo**:
   una ACA con `duedate` en 2028 no sólo confunde, es que su aviso de vencimiento no dispara nunca.
2. Activar lo que ya está listo y oculto — **el Quiz de Proyecto I vale 25% y cierra el 30/08**.
   Doble motivo: `assign_due_soon` exige `cm.visible = 1`, así que un ítem oculto está mudo también
   para el canal nativo.
3. Repetir los pasos 2 y 3 de arriba aula por aula, o de golpe sin `--aula`.
4. **Cubrir el cierre de los cuestionarios**, que ningún proveedor nativo cubre: pedir el cambio de
   `/admin/message.php` al administrador, o montar el Apps Script de §3. Mientras no esté, el aviso
   del foro para un Quiz vive **sólo dentro del aula**.

Una comprobación que falta y no se puede hacer sin administrador: que las tareas programadas
`\mod_assign\task\queue_all_assignment_due_soon_notification_tasks` y sus hermanas estén **habilitadas**
en `/admin/tool/task/scheduledtasks.php`. Vienen habilitadas de fábrica, y se sabe que el cron del
sitio corre —el correo de la PRUEBA 2 lo entregó el cron de foros—, pero eso no prueba que estas
concretas no estén deshabilitadas. La prueba barata: cuando la primera ACA visible quede a 48 horas,
mirar si llega el correo.

**El próximo semestre** cambian tres cosas y nada más: las fechas en
`config/cursos/fechas_entrega_aca.py`, los ids de aula en `AULAS_CURSO`
(`config/moodle/cdigital.py`) y los cmid de las actividades — que se descubren solos por nombre. El
texto de los avisos no se toca.

---

**Fuentes.** Configuración leída del servidor de CDigital (foros, formularios, permisos) y código de
`MOODLE_405_STABLE` para el comportamiento del cron de foros (`mod/forum/classes/task/cron_task.php`,
`mod/forum/classes/post_form.php`, `mod/forum/db/messages.php`, `lib/messagelib.php`). Cuotas de Apps
Script y Gmail API, de la documentación de Google; precios de AWS, de sus páginas de precios. La
verificación del campus se hizo **sólo con peticiones de lectura**: no se publicó nada.
