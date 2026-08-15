# Recordatorios automáticos de entregables — qué canal usar

**15/08/2026.** Qué opciones hay para avisarles a los 282 estudiantes matriculados cuándo abre y
cuándo cierra cada entregable, sin intervención manual, sabiendo que **esta cuenta de Gmail no puede
generar contraseñas de aplicación** (el administrador de Workspace de la CUN tiene esa opción
deshabilitada; el mensaje «La opción de configuración que buscas no está disponible para tu cuenta»
no se arregla desde la cuenta del Docente).

## La respuesta corta

**El campus manda el correo, y el campus también hace de reloj.** El foro «Avisos» de cada aula
tiene suscripción forzada; publicar en él le llega por correo a todos los matriculados. Y con
«Mostrar período» (`timestart`) se puede publicar hoy un aviso cuyo correo el cron de CDigital
retiene hasta la fecha que se le diga.

Eso resuelve las tres cosas a la vez, y hay que verlo bien porque es la parte que no es obvia:

| Problema | Cómo queda resuelto |
|---|---|
| Sin contraseña de aplicación | La cuenta de Gmail **no participa**. El correo lo emite el servidor de la CUN |
| Automático | Lo programa el propio Moodle. **Este computador puede estar apagado** |
| Costo | 0. No hay proveedor, ni cuenta de AWS, ni dominio, ni cuota que agotar |
| Reutilizable el próximo semestre | Los ids del foro se redescubren solos; lo único con fechas dentro es `config/cursos/fechas_entrega_aca.py` |

No hace falta AWS, ni GitHub Actions, ni el Programador de tareas de Windows. Se pueden usar (§4),
pero para este caso son un reloj de repuesto para algo que ya trae reloj.

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

## 2. Lo verificado y lo que falta por probar

Verificado leyendo el servidor real, no supuesto:

- Los **7 foros «Avisos»** existen, están visibles y tienen **suscripción forzada**. Nadie se puede
  dar de baja del aviso.
- Los 7 ids de instancia se descubren automáticamente (aparecen de tres formas distintas según cómo
  pinte el aula la página; se prueban las tres).
- El formulario de publicación se lee y el envío se arma completo en los 7, con `mailnow` y con
  `timestart`.
- `timestart` retiene el correo: la consulta del cron de foros exige que la fecha de inicio ya haya
  pasado, y **`mailnow` no se la salta** —van unidas—. Un aviso programado se puede borrar antes de
  su fecha **sin que salga ningún correo**: por eso el modo programado es reversible.

**Lo único sin probar es el POST final.** No lo probé porque cada publicación es un correo a los 282
matriculados y no hay aula de pruebas: la más pequeña (TG3 grupo 54450) tiene 13 estudiantes reales.
El primer aviso de verdad es también su prueba — hacerlo con **una sola aula** y mirar el resultado:

```bash
python config/cursos/recordatorios.py --canal campus --aula 111070 --confirmar
```

Dos avisos que hay que dar antes de apretar:

- **El estudiante puede apagar el correo del foro.** El proveedor «Mensajes suscritos del foro» está
  activo por defecto, pero no está bloqueado por el administrador: quien lo apague en sus
  preferencias no recibirá el correo (sí verá el aviso al entrar al aula). Y quien tenga «resumen
  diario» lo recibirá de madrugada agrupado. Suscripción forzada garantiza que **está suscrito**, no
  que el correo le llegue.
- **El asunto del correo lleva delante el nombre corto del aula**, que es feo y no se puede cambiar
  sin ser administrador: el estudiante ve `EI004/54408/26V04/B1/FINVV/FINVI: Falta 1 día para Quiz 1`.

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

**Este semestre**, en este orden:

1. Poner las fechas de los 22 ítems visibles (ver `ALISTAMIENTO CDigital 2026-08-15.md` §5: Proyecto
   I anuncia sus dos ACAs para **enero de 2028**). Un recordatorio con la fecha mala es peor que no
   mandarlo.
2. Activar lo que ya está listo y oculto — **el Quiz de Proyecto I vale 25% y cierra el 30/08**.
3. Mandar el primer aviso a **una** aula y mirarlo.
4. Programar el resto del semestre de una vez: `--programar --confirmar`.

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
