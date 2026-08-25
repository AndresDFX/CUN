/**
 * GRABACIONES DE MEET — Mover cada grabación a la carpeta ÚNICA de grabaciones.
 *
 * Meet deja las grabaciones en el Drive del ORGANIZADOR, en su carpeta por omisión de Mi
 * unidad: hoy «Meet Recordings». Algunas cuentas ven en su lugar una carpeta «Google Meet»
 * con una subcarpeta por reunión (y la vieja dentro, como «Legacy Meet Recordings») — mira
 * cuál tienes tú y pega ESE id. El correo de bienvenida y
 * el «LEEME - Material para estudiantes» prometen otra cosa: que TODAS las grabaciones están
 * en UNA carpeta y que el vídeo se encuentra buscando «periodo - grupo - asignatura - sesion».
 * Este script cumple esa promesa cada 30 minutos y SIN NINGUNA CREDENCIAL: Apps Script
 * corre en los servidores de Google con la sesión del dueño del proyecto. No hace falta que el
 * computador esté encendido, y no hay token ni contraseña de aplicación que guardar (que
 * además esta cuenta no puede generar).
 *
 * LO QUE NO HACE, A PROPÓSITO
 * - No borra nada. Ni las subcarpetas de reunión que deja vacías.
 * - No copia: MUEVE. Mover conserva el fileId, así que el enlace que Meet envió por correo y
 *   cualquiera que ya se haya compartido siguen funcionando. Copiar crearía dos verdades.
 * - No mueve lo que no sabe clasificar: lo deja quieto y lo nombra en el registro. Por esa
 *   carpeta la ven 100+ estudiantes, y por Meet pasan también tutorías y jurados.
 *
 * PASOS  (detalle completo en «LEEME - Mover las grabaciones de Meet.md», misma carpeta)
 * 0. REQUISITO PREVIO: los encuentros de la asignatura tienen que EXISTIR en tu Calendar
 *    (los crea «PRINCIPAL - Crear encuentros con invitados.gs» de cada curso). Sin ellos,
 *    una grabación que no traiga el nombre del evento no se puede clasificar y se queda
 *    quieta. Hoy solo Proyecto I tiene serie y sala creadas.
 * 1. https://script.google.com con la cuenta CUN (julian_castanoe@cun.edu.co) — TIENE que ser la del
 *    organizador de las clases: las grabaciones nacen en SU Mi unidad.
 * 2. Nuevo proyecto -> pega TODO este archivo -> guarda.
 * 3. Pega en ORIGEN_ID el ENLACE de la carpeta de Meet de Mi unidad, tal cual, el de la
 *    barra de direcciones (también vale el id pelado: el script entiende las dos formas).
 *    Es el ÚNICO dato que falta.
 * 4. Ejecuta `verificarGrabaciones()` (SOLO LECTURA) y lee el registro entero.
 * 5. Si cuadra: pon SIMULAR = false, guarda y ejecuta `moverGrabaciones()` UNA vez a mano.
 * 6. `instalarDisparador()` -> a partir de ahí corre solo cada 30 minutos.
 *
 * Deshacer: `revertirMovimientos()` (devuelve carpeta y nombre) · `quitarDisparador()`
 *           (para el automatismo) · `olvidarRegistro()` (suelta el historial de deshacer) ·
 *           `reintentarPendientes()` (vuelve a mirar lo descartado y lo que falló al mover).
 *
 * LO QUE ES DEL PERFIL CUN Y NO ES UNIVERSAL  (los perfiles viven en el generador)
 * - La clasificación va por el CALENDARIO. NO puede ir por el número de sesión del nombre
 *   del archivo: se midió sobre los 19 artefactos reales y TODOS decían «Sesion 01» (Meet
 *   congela el título del evento con el que se estrenó la sala). Eso exige que los
 *   encuentros existan en el Calendar y que sus títulos lleven MARCA y encajen con
 *   RX_SUBJECT: una institución que titule sus eventos de otra forma cambia esas dos
 *   constantes en su perfil — no el código de abajo, que no sabe nada de nomenclaturas.
 * - RX_FECHA es la convención de MEET, no de la institución: no está documentada por Google
 *   y ya cambió una vez sin avisar. Es la misma para todos los perfiles a propósito.
 *   MEDIDO Y TODAVÍA SIN ARREGLAR: sobre los archivos reales de la carpeta no caza NINGUNO
 *   —Meet los nombra «2026 08 13 17 00 GMT-05 00», con espacios y sin dos puntos—, así que
 *   hoy la hora del nombre NUNCA se usa y toda la clasificación va por el respaldo
 *   aproximado (fecha de creación, mirando hacia atrás). Corregir el patrón cambia el
 *   comportamiento de lo que ya está funcionando, así que se decide aparte; y mientras no
 *   cace, poner otro DESFASE_ESPERADO en un perfil nuevo no cambia nada.
 * - DESFASE_ESPERADO es UNO solo, y con eso basta donde no hay horario de verano (Colombia).
 *   Con cambio de hora, media parte del año la hora del nombre se descarta y todo cae al
 *   respaldo aproximado por fecha de creación: más «AMBIGUO», nunca un movimiento erróneo.
 * - Las carpetas se identifican por ID (o por su enlace), NUNCA por nombre: los nombres los
 *   pone Google, ya los cambió en julio de 2026, y NOMBRES_ORIGEN solo sirve para sugerir.
 * - Los topes (MAX_*, LIMITE_MS, CADA_MIN) son cuota de Apps Script, no de la institución:
 *   se pueden bajar, no subir. Con una cuenta sin Workspace la cuota diaria es menor.
 * - Un despliegue por ORGANIZADOR: Apps Script solo ve el Drive de su dueño. Si la grabación
 *   la inicia otra persona, nace en SU Mi unidad y este script no la ve. Y supone Mi unidad:
 *   con unidades compartidas haría falta otro camino de código, no otro parámetro.
 * - Los textos de este archivo hablan de «estudiantes», de «tutorías y jurados», del correo
 *   de bienvenida y de rutas de este repositorio: son de la CUN, donde nació el script, y se
 *   dejan tal cual a propósito. Parametrizar la prosa obligaría a tocar el cuerpo del
 *   script, que es justo lo que no se toca para no cambiar lo que ya funciona.
 *
 * Regenerar este .gs: python config/slides/build_apps_script_grabaciones.py CUN
 */

// ───────────────────────────── CONFIGURACIÓN ─────────────────────────────────

// MODO SIMULACIÓN, y por omisión ENCENDIDO: la regla de esta casa es simular primero. Con
// true nada escribe —ni moverGrabaciones(), ni el disparador, ni revertirMovimientos()—:
// solo dicen qué harían. Ponlo en false cuando verificarGrabaciones() te cuadre.
var SIMULAR = true;

var TIMEZONE = 'America/Bogota';

// ORIGEN — la carpeta por omisión de Meet en el Mi unidad del organizador: hoy «Meet
// Recordings»; si tu Drive muestra una «Google Meet» con una subcarpeta por reunión, usa esa.
// VACÍO A PROPÓSITO: este id NO está en el repositorio y no se puede deducir. Tampoco se
// elige por nombre: Google ha movido y renombrado estas carpetas más de una vez, y elegir
// «la primera que aparezca» sería adivinar.
// Cómo obtenerlo: abre la carpeta en Drive y PEGA AQUÍ EL ENLACE TAL CUAL, el de la barra
// de direcciones. No hace falta sacarle el id: lo hace el propio script (ver «ENLACES DE
// CARPETA» al final de esta sección). Si prefieres pegar solo el id, también vale.
//   https://drive.google.com/drive/folders/<id>          <- pégalo entero, así
// Mientras esté vacío, verificarGrabaciones() te SUGIERE candidatos y no mueve nada.
var ORIGEN_ID = '';

// «Legacy Meet Recordings» — la carpeta de grabaciones antiguas que algunas cuentas tienen
// DENTRO de «Google Meet». VACÍO A PROPÓSITO: así el primer despliegue NO arrastra de golpe
// periodos viejos (con nombres que quizá no son canónicos) a la carpeta publicada. Ponlo solo
// el día que quieras barrer también lo antiguo, y ejecuta verificarGrabaciones() ANTES para
// ver la lista completa. Si tu origen es «Meet Recordings» (plana), esto no aplica.
var ORIGEN_LEGACY_ID = '';

// DESTINO — la carpeta ÚNICA de grabaciones: la misma para los 5 cursos y para todos los
// periodos, plana y sin subcarpetas. Fuente única: config/cursos/carga_academica.py ->
// GRABACIONES_URL (y la nota normativa de carga_academica_2026.json). Esta URL ya está
// impresa en el correo de bienvenida y en el LEEME del estudiante: no la cambies aquí.
// Va el ENLACE tal cual, como lo copia Drive (el id pelado también vale).
var DESTINO_ID = 'https://drive.google.com/drive/folders/1EHck-ZdbwwLJtDk2NsS4UDL1UMf1sLqZ?usp=sharing';

// Calendario donde están los encuentros. Es la AUTORIDAD de nombres: los eventos los creó
// «PRINCIPAL - Crear encuentros con invitados.gs», así que al abrir el semestre siguiente
// esto sigue funcionando sin tocar el script. 'primary' = el principal de la cuenta.
var CALENDARIO_ID = 'primary';

// Cada cuántos minutos barre el disparador. everyMinutes() solo admite 1, 5, 10, 15 o 30, y
// Apps Script programa con ventanas de ±15 min: no dependas del minuto exacto. 30 y no 15
// por la cuota: Workspace da 360 min/día de disparadores y esta función se permite hasta
// LIMITE_MS (4,5 min) por pasada -> 48 x 4,5 = 216 min caben; 96 x 4,5 = 432 no.
var CADA_MIN = 30;

// Gracia antes de tocar un archivo recién aparecido, para no llevarse el vídeo dejando atrás
// la transcripción y las notas. HEURÍSTICA, no garantía: Google no expone a DriveApp ninguna
// señal de «ya está completo». Lo que de verdad cubre el caso es reincidir cada CADA_MIN.
var MARGEN_MIN = 20;

// Ventana con la que se CONSULTA el Calendar alrededor de la hora del archivo. Encontrar un
// evento en esa ventana no basta: después se exige que la marca de tiempo caiga DENTRO del
// encuentro (ver TOL_INICIO_MIN), porque getEvents() devuelve todo lo que roce el intervalo y
// una tutoría de las 19:40 rozaría la clase de las 20:00.
var VENTANA_MIN = 30;

// Cuánto ANTES del inicio del encuentro se admite la marca de tiempo del nombre (Meet estampa
// la hora en que empezó la reunión, y a veces se entra unos minutos antes). Después del FINAL
// no se admite nada: una reunión que empieza cuando la clase ya acabó no es la clase.
var TOL_INICIO_MIN = 15;

// Sin hora en el nombre solo queda la fecha de CREACIÓN del archivo, que es POSTERIOR a la
// clase. Así que se mira hacia ATRÁS estas horas y solo valen encuentros ya TERMINADOS: el
// vídeo de la clase del lunes 20:00–22:00 que aparece a las 00:20 del martes pertenece al
// lunes, no al martes. Nunca se mira «el día natural del archivo».
var HORAS_ATRAS_APROX = 6;

// Fragmento que identifica a un encuentro en el título del evento. Se busca CONTENIDO, no
// prefijo (mismo criterio que MARCA en «Actualizar Meet en encuentros (mismo enlace).gs»).
var MARCA = ' - Sesion ';

// Subject canónico dentro del nombre del archivo:
//   «periodo - grupo(s) - Asignatura - Sesion NN»   (sesiones_cun.subject_encuentro)
//   26ES4 - 54ES4 - Proyecto I - Sesion 01
//   26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 01
// Sin anclas: Meet añade « (2026-08-11 17:00 GMT-05:00)» al final y puede añadir cosas
// delante (los artefactos llevan sufijos tipo «- Transcript»).
var RX_SUBJECT = /\d{2}[A-Z]{1,2}\d{1,2}(?:\/\d{2}[A-Z]{1,2}\d{1,2})* - [0-9A-Z]{5}(?:\/[0-9A-Z]{5})* - [^()]{3,60}? - Sesion \d{1,2}(?: \(autónoma\))?/;

// Fecha y hora que Meet escribe en el nombre: « (2026-08-11 17:00 GMT-05:00)».
var RX_FECHA = /(\d{4})[-_ ](\d{2})[-_ ](\d{2})[ _T]+(\d{2})[:._h ](\d{2})(?:[^)]*?GMT\s*([+-]\d{2}))?/;
var DESFASE_ESPERADO = '-05';   // Bogotá. Otro desfase -> la hora del nombre no se usa.

// Código de sala de Meet -> asignatura tal como aparece en el título del evento. Sirve para
// desempatar cuando la ventana de tiempo da más de un candidato Y, sobre todo, para VETAR: si
// la sala dice «Proyecto I» y el único encuentro de esa hora es de TG3, no se mueve. Una sala
// reconocida no clasifica por sí sola (no dice de qué sesión es), pero sí desmiente.
// Fuente: carga_academica_2026.json -> cursos.<key>.meet (solo las salas REALES).
// PENDIENTE: siguen sin sala en el JSON creatividad, investigacion, tg2, tg3 -> cuando el .gs de
// encuentros las cree y las pegues en cursos.<key>.meet, regenera este archivo.
var SALAS = {
  'omk-woqk-vsj': 'Proyecto I'
};

// Tabla día+hora -> curso. NO se usa como criterio (el Calendar ya la contiene, y además
// contempla las reprogramaciones: TG2 dictó la Sesión 01 el viernes 14/08/2026). Está aquí
// para leer el registro a ojo:
//   lunes      20:00–22:00  ->  Proyecto I · 54ES4
//   miércoles  17:00–18:00  ->  Creatividad y Pensamiento Innovador · 54408
//   jueves     17:00–18:00  ->  Investigación Ciencia y Tecnología · 53339
//   lunes      17:00–18:00  ->  Trabajo de Grado 2 · 54448
//   martes     17:00–18:00  ->  Trabajo de Grado 3 · 54450/54466/54467

// Nombres con los que buscar candidatos a ORIGEN_ID. SOLO para SUGERIR en el registro: el
// script nunca elige «la primera que aparezca». Son los nombres que documenta Google en
// inglés; si tu Drive los muestra traducidos no aparecerá ninguno, y entonces el enlace se
// copia a mano de Drive (que es lo que hay que hacer de todas formas).
var NOMBRES_ORIGEN = ['Meet Recordings', 'Google Meet'];
var NOMBRES_LEGACY = ['Legacy Meet Recordings'];

var MIME_ATAJO = 'application/vnd.google-apps.shortcut';

// Registro de lo movido — existe SOLO para deshacer, no para saber qué falta (eso lo dice el
// propio origen). Misma convención que PROP_MEET en los .gs de Calendar.
var PROP_MOVIDOS = 'GRABACIONES_MOVIDAS';
var MAX_REGISTRO = 150;          // entradas
var MAX_REGISTRO_BYTES = 8000;   // una propiedad de script no admite más de 9 KB

// Archivos que ya se miraron y NO se pudieron clasificar (tutorías, jurados, reuniones
// ajenas). Por «Google Meet» no sale nunca nada de eso, así que sin memoria el residuo se
// vuelve a mirar en cada pasada, se come el cupo de MAX_ARCHIVOS y acaba tapando la clase de
// ayer. Se apuntan con la fecha en que se descartaron y se reintentan cada REINTENTO_H horas
// (por si aparece el encuentro en el Calendar o se pega la sala que faltaba).
var PROP_DESCARTADAS = 'GRABACIONES_DESCARTADAS';
var MAX_DESCARTADAS = 120;
var REINTENTO_H = 24;

// Archivos cuyo movimiento FALLÓ (Drive deja un atajo en el destino y el original donde
// estaba). Sin memoria, cada pasada crearía un atajo nuevo en la carpeta que ven los
// estudiantes. Al primer fallo se apunta; a partir del segundo intento no se vuelve a tocar
// hasta que lo desbloquees con reintentarPendientes().
var PROP_FALLIDAS = 'GRABACIONES_FALLIDAS';

// Tope de archivos que se CLASIFICAN por pasada (cada uno puede costar una consulta al
// Calendar) y de archivos cuyos metadatos se leen al barrer. Se ordena de más nuevo a más
// viejo antes de recortar, para que una grabación reciente no quede detrás del residuo.
var MAX_ARCHIVOS = 40;
var MAX_EXAMINADOS = 400;
var MAX_PROFUNDIDAD = 4;   // raíz de Meet / subcarpeta de la reunión / ... y para de contar
var LIMITE_MS = 270000;    // 4,5 min de los 6 que da Apps Script por ejecución

// ─────────────────── ENLACES DE CARPETA: URL o id, da igual ──────────────────
// Las tres constantes de arriba (ORIGEN_ID, ORIGEN_LEGACY_ID, DESTINO_ID) aceptan LAS DOS
// FORMAS, y aquí se normalizan al id, que es lo único que entiende DriveApp:
//
//   https://drive.google.com/drive/folders/<id>
//   https://drive.google.com/drive/u/0/folders/<id>
//   https://drive.google.com/drive/folders/<id>?usp=sharing
//   https://drive.google.com/open?id=<id>
//   <id>                                      (el id pelado, como siempre)
//
// Si lo pegado no es una carpeta —el caso típico: el enlace de un ARCHIVO, que lleva
// «/d/»— se dice en el registro y esa constante queda VACÍA, que es exactamente el estado
// de antes de pegar nada: el script avisa y no mueve. Nunca adivina.

/** Avisos de configuración de esta ejecución. Se llenan al cargar el archivo. */
var AVISOS_ENLACES = [];

function _avisoEnlace_(comoSeLlama, pegado, porque) {
  var msg = comoSeLlama + ': ' + porque;
  AVISOS_ENLACES.push(msg);
  Logger.log('AVISO CONFIGURACIÓN — ' + msg);
  Logger.log('      lo pegado fue: «' + pegado + '»');
  Logger.log('      ' + comoSeLlama + ' queda VACÍO: por ese lado no se moverá nada.');
  return '';
}

/**
 * Id de carpeta a partir de lo que haya pegado el humano: enlace de Drive o id pelado.
 * NUNCA lanza: esto corre al cargar el archivo, y una excepción aquí rompería TODAS las
 * funciones del proyecto. Devuelve '' y deja dicho por qué en el registro.
 */
function _idDeCarpeta_(valor, comoSeLlama) {
  var s = String(valor == null ? '' : valor).trim().replace(/^[<"']+|[>"']+$/g, '');
  if (!s) return '';

  if (/^https?:\/\//i.test(s) || s.indexOf('google.com') >= 0) {
    var mCarpeta = s.match(/\/folders\/([^\/?#]+)/);
    var mParam = s.match(/[?&]id=([^&#]+)/);
    if (mCarpeta) {
      s = mCarpeta[1];
    } else if (/\/(?:file|document|spreadsheets|presentation|forms)\/d\//.test(s)) {
      return _avisoEnlace_(comoSeLlama, s, 'ese enlace es de un ARCHIVO, no de una carpeta ' +
        '(lleva «/d/»). Abre en Drive la CARPETA que contiene las grabaciones y copia el ' +
        'enlace de la barra de direcciones: el de una carpeta lleva «/folders/».');
    } else if (mParam) {
      s = mParam[1];
    } else {
      return _avisoEnlace_(comoSeLlama, s, 'no reconozco esa URL de Drive. Pega el enlace de ' +
        'la CARPETA (el que lleva «/folders/») o, si lo prefieres, solo el id.');
    }
  }

  if (!/^[A-Za-z0-9_-]{11,}$/.test(s)) {
    return _avisoEnlace_(comoSeLlama, valor, 'esto no tiene forma de id de carpeta de Drive ' +
      '(letras, dígitos, «-» y «_»; los ids de verdad rondan los 30 caracteres). Lo que ' +
      'entendí como id fue: «' + s + '».');
  }
  return s;
}

// Se reasignan las MISMAS constantes: de aquí para abajo ORIGEN_ID, ORIGEN_LEGACY_ID y
// DESTINO_ID son ids, como lo han sido siempre. Todo lo que hay debajo no se enteró.
ORIGEN_ID = _idDeCarpeta_(ORIGEN_ID, 'ORIGEN_ID');
ORIGEN_LEGACY_ID = _idDeCarpeta_(ORIGEN_LEGACY_ID, 'ORIGEN_LEGACY_ID');
DESTINO_ID = _idDeCarpeta_(DESTINO_ID, 'DESTINO_ID');

// ═════════════════════════════ PÚBLICAS ══════════════════════════════════════

/**
 * SOLO LECTURA. Dice exactamente qué archivos movería, a dónde, con qué nombre y cuáles NO
 * sabe clasificar. No mueve, no renombra, no borra y no instala nada. Ejecuta SIEMPRE esto
 * primero, y otra vez cada vez que cambies la configuración.
 */
function verificarGrabaciones() {
  _arrancar_();
  var ctx = _contexto_();
  Logger.log('DISPARADOR: ' + _estadoDisparador_());
  Logger.log('REGISTRO  : ' + _registro_().length + ' movimiento(s) que revertirMovimientos() ' +
             'aún puede deshacer');
  if (!ctx) return;

  var lote = _archivosDeMeet_(ctx);
  Logger.log('ARCHIVOS  : ' + lote.archivos.length + ' candidato(s)  ·  omitidos: ' +
             lote.recientes + ' recién tocados (<' + MARGEN_MIN + ' min) · ' +
             lote.legacy + ' en «Legacy» · ' + lote.atajos + ' atajo(s) · ' +
             lote.descartados + ' descartado(s) en pasadas anteriores');

  var plan = _plan_(ctx, lote);
  Logger.log('--- se moverían ------------------------------------------------');
  if (!plan.mover.length) Logger.log('(ninguno)');
  plan.mover.forEach(function (p) {
    Logger.log(p.nombre);
    Logger.log('    criterio: ' + p.criterio);
    Logger.log('    ' + (p.nuevo === p.nombre
      ? 'nombre YA canónico: se mueve tal cual'
      : 'RENOMBRA a: ' + p.nuevo));
  });
  Logger.log('--- sin clasificar (se quedan donde están) ---------------------');
  if (!plan.quietos.length) Logger.log('(ninguno)');
  plan.quietos.forEach(function (p) {
    Logger.log(p.nombre);
    Logger.log('    <- ' + p.motivo);
  });
  Logger.log('----------------------------------------------------------------');
  Logger.log('Simulado: se moverían=' + plan.mover.length +
             ' · se renombrarían=' + plan.renombra +
             ' · sin clasificar=' + plan.quietos.length +
             ' · sin mirar por falta de tiempo=' + plan.sinMirar +
             ' · destino=«' + ctx.destino.getName() + '»');
  _avisoSilencio_(ctx.cal, lote, plan);
  if (lote.descartados) {
    Logger.log('NOTA: ' + lote.descartados + ' archivo(s) ya se descartaron antes y no se ' +
               'vuelven a mirar hasta ' + REINTENTO_H + ' h después (para que el residuo de ' +
               'tutorías y jurados no tape las grabaciones nuevas). Para volver a mirarlos ' +
               'ya: reintentarPendientes().');
  }
  if (lote.cortado) {
    Logger.log('AVISO: había más candidatos que el cupo de ' + MAX_ARCHIVOS + ' de esta pasada; ' +
               'esta lista está recortada. Se miran primero los MÁS NUEVOS, así que la clase ' +
               'de hoy entra antes que el residuo viejo.');
  }
  Logger.log(SIMULAR
    ? 'SIMULAR = true: moverGrabaciones() tampoco movería nada. Cuando esto cuadre, ponlo ' +
      'en false (línea de CONFIGURACIÓN) y ejecuta moverGrabaciones() una vez a mano.'
    : 'SIMULAR = false: moverGrabaciones() SÍ mueve. Si esto cuadra, ejecútalo.');
}

/**
 * Mueve a la carpeta única de grabaciones lo que sabe identificar, y solo eso. Es la
 * función que llama el disparador. Idempotente: lo ya movido no está en el origen, así que
 * una segunda pasada no lo vuelve a tocar; y es REINCIDENTE a propósito — la transcripción
 * y las notas pueden llegar horas después del vídeo y se recogen en una pasada posterior.
 */
function moverGrabaciones() {
  _arrancar_();
  var ctx = _contexto_();
  if (!ctx) return;

  var lote = _archivosDeMeet_(ctx);
  var plan = _plan_(ctx, lote);
  var movidos = 0, renombrados = 0, fallidos = 0, simulados = 0, nuevosFallos = 0;
  var nuevas = [];

  for (var i = 0; i < plan.mover.length; i++) {
    var p = plan.mover[i];
    if (_agotado_()) {
      Logger.log('AVISO: me acerco al límite de 6 minutos de Apps Script; corto aquí. ' +
                 'Quedan ' + (plan.mover.length - i) + ' archivo(s) para la próxima pasada.');
      break;
    }
    if (SIMULAR) {
      simulados++;
      Logger.log('SIMULACIÓN: movería «' + p.nombre + '»  ->  ' + p.nuevo);
      continue;
    }
    // Primero mover y comprobar, DESPUÉS renombrar: si el movimiento falla, el archivo se
    // queda intacto y con su nombre de siempre, no rebautizado en la carpeta de Meet.
    var padreAnterior = p.carpeta.getId();
    if (!_moverYVerificar_(p.archivo, ctx.destino)) {
      fallidos++;
      nuevosFallos++;
      _apuntarFallo_(p.archivo.getId());
      continue;
    }
    movidos++;
    var entrada = { id: p.archivo.getId(), nombreAnterior: p.nombre, padreAnterior: padreAnterior };
    if (p.nuevo !== p.nombre) {
      try { p.archivo.setName(p.nuevo); renombrados++; }
      catch (e) { Logger.log('AVISO: movido pero no pude renombrar «' + p.nombre + '»: ' + e); }
    }
    nuevas.push(entrada);
    Logger.log('movido: ' + p.nuevo + '   [' + p.criterio + ']');
  }

  plan.quietos.forEach(function (p) {
    Logger.log('SIN CLASIFICAR (no se movió): ' + p.nombre + '   <- ' + p.motivo);
  });

  if (nuevas.length) _registrar_(nuevas);
  if (!SIMULAR) _apuntarDescartes_(plan.quietos);
  var vaciadas = SIMULAR ? 0 : _subcarpetasVacias_(lote);

  Logger.log('Grabaciones: movidos=' + movidos + ' · renombrados=' + renombrados +
             ' · sin clasificar=' + plan.quietos.length + ' · fallidos=' + fallidos +
             (SIMULAR ? ' · SIMULADOS=' + simulados : '') +
             ' · en gracia=' + lote.recientes + ' · atajos=' + lote.atajos +
             ' · descartados antes=' + lote.descartados +
             ' · sin mirar por falta de tiempo=' + plan.sinMirar +
             ' · subcarpetas vaciadas=' + vaciadas);
  // «Ya estaban» no se cuenta y no hace falta: lo movido en pasadas anteriores ya no está en
  // la carpeta de origen, así que ni aparece. La idempotencia la da el destino, no el registro.
  Logger.log('Ya estaban (movidos antes): no salen en el barrido porque ya no están en el ' +
             'origen. Destino: «' + ctx.destino.getName() + '» (' + DESTINO_ID + ').');
  if (SIMULAR) {
    Logger.log('SIMULAR = true: NO se movió nada de verdad. Pon SIMULAR = false para que ' +
               'esto surta efecto (y recuerda que el disparador también simula).');
  }
  if (fallidos) {
    Logger.log('Revisa los ERROR de arriba: casi siempre es permiso sobre la carpeta destino ' +
               '(Drive crea un atajo en vez de mover, y parece que funcionó).');
    Logger.log('Esos archivos quedan APUNTADOS y NO se reintentan: si se reintentaran cada ' +
               CADA_MIN + ' min, la carpeta que ven los estudiantes se llenaría de atajos. ' +
               'Arregla el permiso, borra a mano los atajos que hayan quedado y ejecuta ' +
               'reintentarPendientes().');
  }
  _avisoSilencio_(ctx.cal, lote, plan);
  // Y que no dependa de que alguien abra el registro: si falló un movimiento NUEVO, esta
  // ejecución termina con error a propósito, para que Google mande el correo de fallo del
  // disparador. Todo lo anterior ya está hecho y escrito en el log.
  if (nuevosFallos && !SIMULAR) {
    throw new Error('No pude mover ' + nuevosFallos + ' archivo(s) a la carpeta de ' +
                    'grabaciones: Drive dejó un ATAJO en vez de mover. Revisa permisos sobre ' +
                    '«' + ctx.destino.getName() + '», borra los atajos y ejecuta ' +
                    'reintentarPendientes(). Lo demás de esta pasada sí se hizo.');
  }
}

/**
 * Deja el automatismo corriendo: un disparador temporal cada CADA_MIN minutos sobre
 * moverGrabaciones(). No crea un segundo si ya hay uno (consulta los del proyecto antes,
 * igual que los .gs de Calendar buscan el evento antes de crearlo).
 */
function instalarDisparador() {
  if (!_origenConfigurado_()) {
    Logger.log('NO instalo nada: ORIGEN_ID está vacío. Un disparador que no puede leer la ' +
               'carpeta de Meet solo produce silencio. Pega el id y repite.');
    _sugerirOrigen_();
    return;
  }
  var ya = _disparadores_();
  if (ya.length) {
    Logger.log('Ya había ' + ya.length + ' disparador(es) para moverGrabaciones: no creo otro.');
    Logger.log('Estado: ' + _estadoDisparador_());
    return;
  }
  ScriptApp.newTrigger('moverGrabaciones').timeBased().everyMinutes(CADA_MIN).create();
  Logger.log('Disparador instalado: moverGrabaciones() cada ' + CADA_MIN + ' minutos.');
  Logger.log('Ojo: Apps Script programa con ventanas de ±15 min, así que la hora exacta no ' +
             'está garantizada (y no hace falta: la grabación tarda en generarse).');
  if (SIMULAR) {
    Logger.log('AVISO: SIMULAR sigue en true, así que el disparador NO moverá nada — solo ' +
               'escribirá lo que haría. Ponlo en false y guarda cuando estés listo.');
  }
  Logger.log('Deshacer: quitarDisparador().');
}

/** Deshacer (automatismo): quita TODOS los disparadores de moverGrabaciones. */
function quitarDisparador() {
  var t = _disparadores_(), n = 0;
  t.forEach(function (tr) { ScriptApp.deleteTrigger(tr); n++; });
  Logger.log('Disparadores eliminados=' + n + '. Los archivos ya movidos siguen movidos ' +
             '(para eso está revertirMovimientos()).');
  Logger.log('Estado: ' + _estadoDisparador_());
}

/**
 * Deshacer (archivos): devuelve cada archivo del registro a su carpeta y a su nombre
 * anteriores, del más reciente al más antiguo. No borra nada y no toca lo que no esté en el
 * registro. Respeta SIMULAR: con SIMULAR = true solo dice qué haría.
 */
function revertirMovimientos() {
  var reg = _registro_();
  if (!reg.length) { Logger.log('El registro está vacío: no hay nada que revertir.'); return; }
  Logger.log('Entradas en el registro: ' + reg.length + (SIMULAR ? '  (SIMULACIÓN)' : ''));

  var quedan = [], hechos = 0, fallidos = 0;
  for (var i = reg.length - 1; i >= 0; i--) {
    var e = reg[i];
    if (SIMULAR) {
      Logger.log('SIMULACIÓN: devolvería ' + e.id + ' a la carpeta ' + e.padreAnterior +
                 ' con el nombre «' + e.nombreAnterior + '»');
      quedan.push(e);
      continue;
    }
    try {
      var f = DriveApp.getFileById(e.id);
      var destino = DriveApp.getFolderById(e.padreAnterior);
      f.moveTo(destino);
      if (f.getName() !== e.nombreAnterior) f.setName(e.nombreAnterior);
      hechos++;
      Logger.log('revertido: «' + e.nombreAnterior + '»  ->  «' + destino.getName() + '»');
    } catch (err) {
      fallidos++;
      quedan.push(e);   // no se pudo: se queda en el registro para reintentar
      Logger.log('ERROR al revertir ' + e.id + ': ' + err);
    }
  }
  if (!SIMULAR) {
    PropertiesService.getScriptProperties().setProperty(PROP_MOVIDOS, JSON.stringify(quedan));
  }
  Logger.log('Reversión: revertidos=' + hechos + ' · fallidos=' + fallidos +
             ' · quedan en el registro=' + quedan.length);
  if (SIMULAR) Logger.log('SIMULAR = true: no se revirtió nada. Ponlo en false para deshacer.');
}

/**
 * Deshacer (registro): olvida el historial de movimientos. NO devuelve ningún archivo —
 * después de esto, revertirMovimientos() ya no puede deshacer nada de lo olvidado.
 */
function olvidarRegistro() {
  var n = _registro_().length;
  PropertiesService.getScriptProperties().deleteProperty(PROP_MOVIDOS);
  Logger.log('Registro olvidado: ' + n + ' entrada(s). Los archivos siguen donde están.');
  Logger.log('Ojo: esto NO afecta a la idempotencia. Lo ya movido no vuelve a moverse porque ' +
             'ya no está en la carpeta de origen, no porque estuviera apuntado.');
}

/**
 * Vuelve a mirar lo aparcado: los archivos que no se pudieron clasificar (se aparcan
 * REINTENTO_H horas para que el residuo de tutorías y jurados no tape las grabaciones
 * nuevas) y los que fallaron al moverse (se aparcan hasta aquí para no llenar de atajos la
 * carpeta publicada). Ejecútalo después de crear la serie de encuentros que faltaba, de
 * pegar una sala en el JSON o de arreglar el permiso del destino. No mueve nada por sí solo:
 * solo suelta el freno de la próxima pasada.
 */
function reintentarPendientes() {
  var d = _cuantas_(PROP_DESCARTADAS), f = _cuantas_(PROP_FALLIDAS);
  var props = PropertiesService.getScriptProperties();
  props.deleteProperty(PROP_DESCARTADAS);
  props.deleteProperty(PROP_FALLIDAS);
  Logger.log('Soltados: ' + d + ' descartado(s) y ' + f + ' movimiento(s) fallido(s). La ' +
             'próxima pasada los vuelve a mirar.');
  if (f) {
    Logger.log('Ojo con los fallidos: si el permiso sobre la carpeta destino sigue mal, Drive ' +
               'volverá a dejar un ATAJO. Borra primero los atajos que hayan quedado ahí.');
  }
  Logger.log('Esto NO devuelve ningún archivo movido: para eso está revertirMovimientos().');
}

// ═════════════════════════════ INTERNAS ══════════════════════════════════════

// ── reloj: los 6 minutos de Apps Script son el límite duro de todo ───────────

// Milisegundos en que arrancó esta ejecución. Cada ejecución de Apps Script es una instancia
// nueva, así que esto se reinicia solo; _arrancar_() está para no depender de eso.
var T0_MS = 0;

function _arrancar_() {
  T0_MS = new Date().getTime();
  _CACHE_EVENTOS_ = {};
}

/** ¿Me estoy acercando al límite de 6 minutos por ejecución? */
function _agotado_() {
  return (new Date().getTime() - (T0_MS || new Date().getTime())) > LIMITE_MS;
}

// ── contexto: carpetas, calendario y las excusas para no hacer nada ──────────

/** ¿ORIGEN_ID trae un id de verdad o sigue con el vacío que emite el builder? */
function _origenConfigurado_() {
  return typeof ORIGEN_ID === 'string' && ORIGEN_ID.replace(/\s/g, '').length > 10;
}

/** Carpeta por id, con el rótulo impreso para verlo a ojo. null si no se pudo abrir. */
function _carpeta_(id, rotulo) {
  try {
    var f = DriveApp.getFolderById(id);
    Logger.log(rotulo + ' : «' + f.getName() + '»  (' + id + ')');
    return f;
  } catch (e) {
    Logger.log('ERROR en ' + rotulo + ': no pude abrir la carpeta ' + id + ' -> ' + e);
    Logger.log('Comprueba que el id es correcto y que esta cuenta tiene acceso a la carpeta.');
    return null;
  }
}

/** El calendario donde están los encuentros. 'primary' = el principal de la cuenta. */
function _calendario_() {
  if (CALENDARIO_ID && CALENDARIO_ID !== 'primary') {
    var c = CalendarApp.getCalendarById(CALENDARIO_ID);
    if (c) return c;
    Logger.log('AVISO: no existe el calendario ' + CALENDARIO_ID + '; uso el principal.');
  }
  return CalendarApp.getDefaultCalendar();
}

/**
 * Cabecera de contexto y las tres cosas que hacen falta para trabajar: carpeta origen,
 * carpeta destino y calendario. Devuelve null —y explica por qué— si falta algo. Nunca
 * lanza: si no se puede trabajar, se dice y se sale.
 */
function _contexto_() {
  Logger.log('MODO      : ' + (SIMULAR
    ? 'SIMULACIÓN — no se mueve, no se renombra, no se borra'
    : 'REAL — SÍ mueve y renombra'));
  Logger.log('ZONA      : ' + TIMEZONE + '  ·  gracia=' + MARGEN_MIN + ' min  ·  ventana ' +
             'Calendar=±' + VENTANA_MIN + ' min  ·  barrido cada ' + CADA_MIN + ' min');
  var cal = _calendario_();
  Logger.log('CALENDARIO: «' + cal.getName() + '»  (' + cal.getId() + ')');
  var destino = _carpeta_(DESTINO_ID, 'DESTINO');
  if (!destino) {
    Logger.log('Sin carpeta destino no se hace nada. Fuente del id: ' +
               'config/cursos/carga_academica.py -> GRABACIONES_URL.');
    return null;
  }
  if (!_origenConfigurado_()) {
    Logger.log('ORIGEN    : SIN CONFIGURAR — no se moverá nada.');
    _sugerirOrigen_();
    return null;
  }
  var origen = _carpeta_(ORIGEN_ID, 'ORIGEN ');
  if (!origen) return null;
  if (origen.getId() === destino.getId()) {
    Logger.log('ERROR: ORIGEN_ID y DESTINO_ID son la misma carpeta. Revisa la configuración.');
    return null;
  }

  var raices = [origen];
  if (ORIGEN_LEGACY_ID) {
    var legacy = _carpeta_(ORIGEN_LEGACY_ID, 'LEGACY ');
    if (legacy) {
      raices.push(legacy);
      Logger.log('AVISO: ORIGEN_LEGACY_ID está puesto, así que TAMBIÉN se barren las ' +
                 'grabaciones anteriores a julio de 2026. Si no era eso, déjalo vacío.');
    }
  }
  return { origen: origen, destino: destino, cal: cal, raices: raices };
}

/**
 * Candidatos para ORIGEN_ID, buscados por nombre. Es una SUGERENCIA para copiar y pegar:
 * el script nunca elige «la primera que aparezca». Google reorganizó estas carpetas en
 * julio de 2026 y su propio anuncio pide auditar lo que dependa de nombres de carpeta.
 */
function _sugerirOrigen_() {
  Logger.log('  +--------------------------------------------------------------');
  Logger.log('  | FALTA ORIGEN_ID: la carpeta de grabaciones de Meet de tu Mi unidad.');
  Logger.log('  | Ábrela en Drive y copia el ENLACE de la barra de direcciones, entero:');
  Logger.log('  |   https://drive.google.com/drive/folders/<id>');
  Logger.log('  | Pégalo arriba, en  var ORIGEN_ID = \'\';  — el script le saca el id solo');
  Logger.log('  | (o pega solo el id, si lo prefieres: las dos formas valen).');
  var vistos = 0;
  NOMBRES_ORIGEN.forEach(function (n) {
    var it = DriveApp.getFoldersByName(n);
    while (it.hasNext()) {
      var f = it.next();
      vistos++;
      Logger.log('  | candidato: «' + f.getName() + '»  ->  ' + f.getId());
    }
  });
  if (!vistos) {
    Logger.log('  | (no encontré ninguna carpeta con esos nombres: puede que todavía no');
    Logger.log('  |  hayas grabado nada, o que Google la haya vuelto a renombrar)');
  }
  Logger.log('  +--------------------------------------------------------------');
}

// ── barrido del origen ──────────────────────────────────────────────────────

/**
 * Los archivos del origen que SÍ se pueden tocar, más el recuento de los que se dejaron a
 * propósito. Se salta: la papelera, los atajos, lo modificado en los últimos MARGEN_MIN
 * minutos, lo ya descartado en pasadas anteriores (menos de REINTENTO_H horas) y «Legacy
 * Meet Recordings» (salvo que su id esté en ORIGEN_LEGACY_ID).
 *
 * El orden importa: se ordena de MÁS NUEVO a más viejo antes de aplicar MAX_ARCHIVOS. Por
 * esta carpeta pasan tutorías, jurados y reuniones ajenas que nunca se van a poder clasificar
 * y que nadie borra; con el orden que dé Drive, ese residuo acabaría comiéndose el cupo y la
 * grabación de ayer no se alcanzaría nunca. Y se corta por RELOJ además de por cupo: barrer y
 * clasificar es la parte cara, y morir por «tiempo máximo de ejecución» antes del primer
 * moveTo dejaría la pasada sin efecto.
 */
function _archivosDeMeet_(ctx) {
  var out = { archivos: [], carpetas: [], recientes: 0, legacy: 0, atajos: 0,
              descartados: 0, examinados: 0, cortado: false };
  // Margen de gracia. Es una HEURÍSTICA, no una garantía: Google no documenta ninguna señal
  // de «archivo completo» visible desde DriveApp (la que sí existe, Recording.state =
  // FILE_GENERATED, vive en la Meet REST API, que aquí no se usa). Mover es un cambio de
  // metadato —no existe «mover medio archivo»—; el riesgo real es llevarse el vídeo y dejar
  // huérfanas la transcripción y las notas, y contra eso lo que sirve es reincidir.
  var corte = new Date().getTime() - MARGEN_MIN * 60000;
  var aparcados = _mapa_(PROP_DESCARTADAS);
  var vigencia = new Date().getTime() - REINTENTO_H * 3600000;
  var pendientes = [];
  var vistos = [];
  ctx.raices.forEach(function (f) { pendientes.push({ carpeta: f, prof: 0, raiz: true }); });

  while (pendientes.length) {
    if (_agotado_()) { out.cortado = true; break; }
    var nodo = pendientes.shift();
    out.carpetas.push({ carpeta: nodo.carpeta, raiz: nodo.raiz });
    var fs = nodo.carpeta.getFiles();
    while (fs.hasNext()) {
      var f = fs.next();
      try {
        if (f.isTrashed()) continue;
        // Un atajo no es la grabación: moverlo dejaría el vídeo donde estaba y encima
        // parecería que se hizo el trabajo.
        if (f.getMimeType() === MIME_ATAJO) { out.atajos++; continue; }
        var id = f.getId();
        if (aparcados[id] && aparcados[id] > vigencia) { out.descartados++; continue; }
        var mod = f.getLastUpdated().getTime();
        if (mod > corte) { out.recientes++; continue; }
        vistos.push({ archivo: f, carpeta: nodo.carpeta, mod: mod });
        out.examinados++;
        if (out.examinados >= MAX_EXAMINADOS) { out.cortado = true; break; }
      } catch (e) {
        Logger.log('AVISO: no pude leer un archivo de «' + nodo.carpeta.getName() + '»: ' + e);
      }
    }
    if (out.cortado) break;
    if (nodo.prof >= MAX_PROFUNDIDAD) continue;
    var cs = nodo.carpeta.getFolders();
    while (cs.hasNext()) {
      var c = cs.next();
      if (!ORIGEN_LEGACY_ID && _esLegacy_(c.getName())) { out.legacy++; continue; }
      pendientes.push({ carpeta: c, prof: nodo.prof + 1, raiz: false });
    }
  }

  // Lo más nuevo primero, y SOLO ENTONCES se recorta.
  vistos.sort(function (a, b) { return b.mod - a.mod; });
  if (vistos.length > MAX_ARCHIVOS) {
    out.cortado = true;
    vistos = vistos.slice(0, MAX_ARCHIVOS);
  }
  out.archivos = vistos;
  return out;
}

/** ¿Es la carpeta de las grabaciones viejas («Legacy Meet Recordings»), si tu Drive la tiene? */
function _esLegacy_(nombre) {
  for (var i = 0; i < NOMBRES_LEGACY.length; i++) {
    if (String(nombre).toLowerCase().indexOf(NOMBRES_LEGACY[i].toLowerCase()) >= 0) return true;
  }
  return false;
}

/** Subcarpetas de reunión que quedaron sin archivos. Se vacían, NO se borran. */
function _subcarpetasVacias_(lote) {
  var n = 0;
  lote.carpetas.forEach(function (c) {
    if (c.raiz) return;
    try { if (!c.carpeta.getFiles().hasNext()) n++; } catch (e) { /* da igual: es un conteo */ }
  });
  return n;
}

// ── identificación: a qué encuentro pertenece cada archivo ───────────────────

/**
 * El plan de la pasada: qué se movería y con qué nombre, y qué se queda quieto y por qué.
 * Lo consumen igual verificarGrabaciones() (que solo lo imprime) y moverGrabaciones().
 *
 * Esta es la fase CARA (una consulta al Calendar por hora distinta), así que corta por reloj:
 * lo que no se alcanza a mirar se cuenta en `sinMirar` y se atiende en la pasada siguiente,
 * que empieza otra vez por lo más nuevo.
 */
function _plan_(ctx, lote) {
  var mover = [], quietos = [], renombra = 0, sinMirar = 0;
  var fallidas = _mapa_(PROP_FALLIDAS);
  for (var i = 0; i < lote.archivos.length; i++) {
    if (_agotado_()) { sinMirar = lote.archivos.length - i; break; }
    var it = lote.archivos[i];
    var nombre = it.archivo.getName();
    var id = it.archivo.getId();
    if (fallidas[id]) {
      quietos.push({
        id: id, nombre: nombre,
        fallo: true,
        motivo: 'ya intenté moverlo y Drive dejó un ATAJO en vez de mover: no lo reintento ' +
                'para no llenar de atajos la carpeta que ven los estudiantes. Revisa permisos ' +
                'sobre el destino, borra los atajos y ejecuta reintentarPendientes()'
      });
      continue;
    }
    var c = _clasificar_(ctx.cal, it);
    if (!c.subject) { quietos.push({ id: id, nombre: nombre, motivo: c.motivo }); continue; }
    var nuevo = c.renombrar ? _nombreCanonico_(c.subject, nombre) : nombre;
    if (nuevo !== nombre) renombra++;
    mover.push({
      archivo: it.archivo, carpeta: it.carpeta, nombre: nombre,
      nuevo: nuevo, criterio: c.criterio
    });
  }
  return { mover: mover, quietos: quietos, renombra: renombra, sinMirar: sinMirar };
}

/**
 * ¿A qué encuentro pertenece este archivo? Devuelve { subject, criterio, renombrar, motivo }
 * con subject = '' cuando NO se sabe — y entonces `motivo` explica por qué y el archivo se
 * queda donde está. ANTE LA DUDA NO SE MUEVE: esa carpeta la ven 100+ estudiantes, y por
 * ahí pasan tutorías, jurados de proyectos de grado y reuniones ajenas.
 */
function _clasificar_(cal, it) {
  var nombre = it.archivo.getName();

  // Criterio 1 — el nombre YA trae el subject canónico, porque Meet nombra el archivo con
  // el título del evento desde el que se inició la reunión. Tiene prioridad sobre el
  // Calendar: es lo que Google escribió en el momento de la clase, no lo que el calendario
  // diga hoy. Se busca CONTENIDO, no prefijo — un match anclado al inicio dejaba de
  // encontrar los eventos y el script quedaba mudo (corregido el 2026-08-11 en
  // «Actualizar Meet en encuentros (mismo enlace).gs»).
  var enNombre = _subjectDelNombre_(nombre);
  if (enNombre) {
    return { subject: enNombre, criterio: 'nombre del archivo (subject canónico)',
             renombrar: false, motivo: '' };
  }

  // Criterio 3 — el código de sala. No clasifica por sí solo (no dice de qué sesión es), pero
  // DESMIENTE: si la sala es la de Proyecto I, el archivo no es de TG3 por muy solo que esté
  // ese encuentro en la agenda. Puede venir en el nombre del archivo o en el de la subcarpeta
  // de la reunión.
  var pista = _asignaturaDeSala_(nombre) || _asignaturaDeSala_(it.carpeta.getName());

  // Criterio 2 — cruce por fecha y hora contra los eventos REALES del Calendar, que es la
  // autoridad de nombres: los creó «PRINCIPAL - Crear encuentros con invitados.gs» y ya
  // contienen las excepciones (TG2 dictó la Sesión 01 el VIERNES 14/08/2026, reprogramada
  // desde el lunes 10/08). Una tabla de horarios horneada aquí la habría perdido.
  var fecha = _fechaDelNombre_(nombre);
  var aprox = !fecha;
  if (!fecha) {
    // Sin hora en el nombre (o con un desfase que no es el de Bogotá): lo único que queda es
    // la fecha de CREACIÓN, que es POSTERIOR a la clase. Se mira hacia ATRÁS —nunca «el día
    // natural del archivo», que a las 00:20 ya es el día siguiente— y solo cuentan encuentros
    // ya terminados. En lunes hay dos cursos -> saldrá «ambiguo», y eso es correcto.
    fecha = it.archivo.getDateCreated();
  }
  var cands = _encajan_(_eventosCandidatos_(cal, fecha, aprox), fecha, aprox);

  if (!cands.length) {
    return {
      subject: '', criterio: '', renombrar: false,
      motivo: 'no hay ningún encuentro en el Calendar ' +
              (aprox ? 'que terminara en las ' + HORAS_ATRAS_APROX + ' h anteriores al ' +
                       _hm_(fecha) + ' (fecha aproximada: la saqué de la creación del ' +
                       'archivo, el nombre no traía hora)'
                     : 'que contenga el ' + _hm_(fecha)) +
              (pista ? ' · la sala sí la reconozco: ' + pista : '') +
              ' · ¿ya creaste la serie de encuentros de ese curso?'
    };
  }

  // El VETO de la sala se aplica SIEMPRE, no solo cuando hay empate: un único candidato que
  // la sala contradice es justo la señal de que la clasificación está mal, no una
  // confirmación. Antes esto solo corría con cands.length > 1 y el archivo se movía igual.
  var corroborada = false;
  if (pista) {
    var filtrados = cands.filter(function (ev) {
      return (ev.getTitle() || '').indexOf(pista) >= 0;
    });
    if (!filtrados.length) {
      return {
        subject: '', criterio: '', renombrar: false,
        motivo: 'la sala dice «' + pista + '» y ' +
                (cands.length === 1
                  ? 'el único encuentro de esa hora es otro: '
                  : 'ninguno de los ' + cands.length + ' encuentros de esa hora es de esa ' +
                    'asignatura: ') + _titulos_(cands) + '. No lo muevo.'
      };
    }
    cands = filtrados;
    corroborada = true;
  }

  if (cands.length > 1) {
    return {
      subject: '', criterio: '', renombrar: false,
      motivo: 'AMBIGUO: encajan ' + cands.length + ' encuentros y no sé de cuál es: ' +
              _titulos_(cands)
    };
  }
  return {
    subject: cands[0].getTitle(),
    criterio: 'Calendar ' + (aprox ? 'aprox. (creado ' + _hm_(fecha) + ', encuentro anterior)'
                                   : _hm_(fecha)) +
              (corroborada ? ' + sala ' + pista : ''),
    renombrar: true, motivo: ''
  };
}

/** Títulos de unos encuentros, para escribirlos en el registro. */
function _titulos_(cands) {
  return cands.map(function (ev) { return '«' + ev.getTitle() + '»'; }).join(' y ');
}

/**
 * Subject canónico que ya viene dentro del nombre del archivo, o '' si no hay ninguno.
 * Canónico = «periodo - grupo(s) - Asignatura - Sesion NN» (sesiones_cun.subject_encuentro).
 */
function _subjectDelNombre_(nombre) {
  var m = String(nombre).match(RX_SUBJECT);
  return m ? m[0].trim() : '';
}

/** Asignatura cuyo código de sala aparece en `texto`, o '' si ninguno. */
function _asignaturaDeSala_(texto) {
  var t = String(texto || '').toLowerCase();
  for (var codigo in SALAS) {
    if (t.indexOf(codigo.toLowerCase()) >= 0) return SALAS[codigo];
  }
  return '';
}

/**
 * Fecha y hora que Meet escribió en el nombre —«… (2026-08-11 17:00 GMT-05:00)»— o null si
 * no está. Se interpreta en TIMEZONE; si el nombre trae un desfase que NO es el de Bogotá,
 * se devuelve null a propósito y se cae al criterio de día completo, que es más flojo pero
 * no se equivoca de hora. La convención de nombre de Meet NO está documentada por Google:
 * es observación de campo, y por eso nunca es el único criterio.
 */
function _fechaDelNombre_(nombre) {
  var m = String(nombre).match(RX_FECHA);
  if (!m) return null;
  if (m[6] && m[6] !== DESFASE_ESPERADO) return null;
  var iso = m[1] + '-' + m[2] + '-' + m[3] + ' ' + m[4] + ':' + m[5] + ':00';
  try { return Utilities.parseDate(iso, TIMEZONE, 'yyyy-MM-dd HH:mm:ss'); }
  catch (e) { return null; }
}

// Consultas al Calendar ya hechas en ESTA ejecución, indexadas por ventana. Los 3-4 artefactos
// de una misma reunión (vídeo, transcripción, chat, notas) llevan la misma fecha y hora y
// producían la misma consulta 4 veces; a 0,3-1 s cada una, eso es lo que revienta los 6
// minutos antes de mover nada. _arrancar_() la vacía en cada ejecución.
var _CACHE_EVENTOS_ = {};

/**
 * Encuentros del calendario en la ventana que puede corresponder a un archivo de esa fecha.
 * Con hora en el nombre: ±VENTANA_MIN minutos alrededor de la marca. Sin hora: las
 * HORAS_ATRAS_APROX anteriores a la creación del archivo, porque el artefacto nace DESPUÉS de
 * la clase (mirar «el día del archivo» clasificaba la clase del lunes 22:00 como la del martes
 * cuando el vídeo aparecía pasada la medianoche).
 * OJO: getEvents() devuelve todo evento que ROCE el intervalo. Quién encaja de verdad lo
 * decide _encajan_(); esto solo trae los candidatos.
 */
function _eventosCandidatos_(cal, fecha, aprox) {
  var ini, fin;
  if (aprox) {
    ini = new Date(fecha.getTime() - HORAS_ATRAS_APROX * 3600000);
    fin = new Date(fecha.getTime());
  } else {
    ini = new Date(fecha.getTime() - VENTANA_MIN * 60000);
    fin = new Date(fecha.getTime() + VENTANA_MIN * 60000);
  }
  var clave = ini.getTime() + '|' + fin.getTime();
  if (_CACHE_EVENTOS_.hasOwnProperty(clave)) return _CACHE_EVENTOS_[clave];
  var res = [];
  try {
    res = cal.getEvents(ini, fin).filter(function (ev) {
      return (ev.getTitle() || '').indexOf(MARCA) >= 0;
    });
  } catch (e) {
    Logger.log('AVISO: no pude consultar el Calendar para el ' + _dia_(fecha) + ': ' + e);
    res = [];
  }
  _CACHE_EVENTOS_[clave] = res;
  return res;
}

/**
 * De los candidatos de la ventana, los que de verdad pueden ser este archivo:
 *  - con hora en el nombre: la marca de tiempo tiene que caer DENTRO del encuentro (se
 *    admiten TOL_INICIO_MIN minutos antes del inicio, porque a veces se entra antes; después
 *    del final NO se admite nada). Sin esto, una tutoría grabada a las 19:40 rozaba la ventana
 *    de la clase de las 20:00 y se publicaba con su nombre.
 *  - sin hora: el encuentro tiene que haber TERMINADO antes de que el archivo existiera.
 */
function _encajan_(cands, fecha, aprox) {
  var t = fecha.getTime();
  return cands.filter(function (ev) {
    var ini = ev.getStartTime().getTime();
    var fin = ev.getEndTime().getTime();
    if (aprox) return fin <= t;
    return t >= ini - TOL_INICIO_MIN * 60000 && t <= fin;
  });
}

/**
 * Nombre con el que el archivo cumple la promesa publicada: el subject canónico delante
 * —«dentro se busca por el nombre del evento», dice el correo de bienvenida— y el nombre
 * que puso Meet conservado íntegro entre paréntesis, con su fecha y su hora. La extensión,
 * si la tenía, se queda al final: dentro del paréntesis rompería la descarga.
 */
function _nombreCanonico_(subject, original) {
  var m = String(original).match(/\.[A-Za-z0-9]{2,5}$/);
  var ext = m ? m[0] : '';
  var base = ext ? original.substring(0, original.length - ext.length) : original;
  if (base.indexOf(subject) === 0) return original;   // ya empieza por el subject: no lo toques
  return subject + ' (' + base + ')' + ext;
}

// ── mover, con comprobación ─────────────────────────────────────────────────

/**
 * Mueve el archivo y COMPRUEBA que llegó. La comprobación no es paranoia: Drive documenta
 * que sin permiso para mover «a shortcut is created in the destination folder instead» —el
 * fallo es silencioso y parece un éxito—. Devuelve true solo si el único padre es el destino.
 */
function _moverYVerificar_(archivo, destino) {
  var nombre = archivo.getName();
  try {
    archivo.moveTo(destino);
  } catch (e) {
    Logger.log('ERROR en «' + nombre + '»: no se pudo mover -> ' + e);
    return false;
  }
  try {
    var ids = [], it = archivo.getParents();
    while (it.hasNext()) ids.push(it.next().getId());
    if (ids.length === 1 && ids[0] === destino.getId()) return true;
    Logger.log('ERROR en «' + nombre + '»: sigue en [' + ids.join(', ') + '] y no en ' +
               destino.getId() + '; probablemente Drive creó un ATAJO en vez de mover.');
    Logger.log('Revisa que esta cuenta pueda mover archivos a «' + destino.getName() + '», y ' +
               'borra a mano el atajo que haya quedado ahí: los estudiantes ven esa carpeta.');
    return false;
  } catch (e) {
    Logger.log('AVISO: moví «' + nombre + '» pero no pude confirmar el destino: ' + e);
    return false;   // ante la duda NO se apunta como movido
  }
}

// ── registro de lo movido: existe SOLO para deshacer ────────────────────────

/**
 * Movimientos apuntados, del más antiguo al más reciente. NO es lo que da idempotencia:
 * eso lo da el destino (lo ya movido ya no está en el origen), igual que los .gs de
 * Calendar preguntan al calendario en vez de llevar un libro de registro.
 */
function _registro_() {
  var raw = PropertiesService.getScriptProperties().getProperty(PROP_MOVIDOS) || '[]';
  try {
    var a = JSON.parse(raw);
    return (a instanceof Array) ? a : [];
  } catch (e) {
    Logger.log('AVISO: el registro estaba ilegible; lo trato como vacío. revertirMovimientos() ' +
               'no podrá deshacer lo anterior.');
    return [];
  }
}

/**
 * Apunta los movimientos nuevos, en FIFO. Dos topes: MAX_REGISTRO entradas y, sobre todo,
 * MAX_REGISTRO_BYTES — una propiedad de script no admite más de 9 KB, y un semestre son
 * ~75 encuentros con 2-3 artefactos cada uno, así que el que muerde es el de bytes.
 */
function _registrar_(nuevas) {
  var todo = _registro_().concat(nuevas);
  var recortadas = 0;
  while (todo.length > MAX_REGISTRO ||
         (todo.length > 1 && JSON.stringify(todo).length > MAX_REGISTRO_BYTES)) {
    todo.shift();
    recortadas++;
  }
  try {
    PropertiesService.getScriptProperties().setProperty(PROP_MOVIDOS, JSON.stringify(todo));
  } catch (e) {
    Logger.log('AVISO: no pude guardar el registro (' + e + '). Los archivos SÍ se movieron; ' +
               'lo que se pierde es el deshacer automático.');
    return;
  }
  if (recortadas) {
    Logger.log('AVISO: registro recortado en ' + recortadas + ' entrada(s); ' +
               'revertirMovimientos() ya no alcanza a las más antiguas.');
  }
}

// ── memoria de lo aparcado: descartados y movimientos fallidos ──────────────

/** `{fileId: marca de tiempo}` de una propiedad de script. {} si no hay o está ilegible. */
function _mapa_(prop) {
  var raw = PropertiesService.getScriptProperties().getProperty(prop) || '{}';
  try {
    var o = JSON.parse(raw);
    return (o && typeof o === 'object' && !(o instanceof Array)) ? o : {};
  } catch (e) {
    Logger.log('AVISO: ' + prop + ' estaba ilegible; lo trato como vacío.');
    return {};
  }
}

function _cuantas_(prop) {
  var m = _mapa_(prop), n = 0;
  for (var k in m) n++;
  return n;
}

/**
 * Guarda un mapa recortando por número de entradas y por bytes (una propiedad de script no
 * admite más de 9 KB). Se tiran las entradas MÁS ANTIGUAS: son las que menos importan, porque
 * este mapa es una optimización, no la fuente de la verdad.
 */
function _guardarMapa_(prop, mapa, maxEntradas) {
  var claves = [];
  for (var k in mapa) claves.push(k);
  claves.sort(function (a, b) { return mapa[a] - mapa[b]; });
  while (claves.length > maxEntradas ||
         (claves.length > 1 && JSON.stringify(mapa).length > MAX_REGISTRO_BYTES)) {
    delete mapa[claves.shift()];
  }
  try {
    PropertiesService.getScriptProperties().setProperty(prop, JSON.stringify(mapa));
  } catch (e) {
    Logger.log('AVISO: no pude guardar ' + prop + ' (' + e + '); la próxima pasada volverá a ' +
               'mirar esos archivos.');
  }
}

/**
 * Apunta que este archivo NO se pudo mover. A partir del segundo intento ya no se toca: el
 * fallo típico es que Drive deje un ATAJO en el destino en vez de mover, y reintentarlo cada
 * pasada llenaría de atajos la carpeta que ven los estudiantes. Se suelta con
 * reintentarPendientes().
 */
function _apuntarFallo_(id) {
  var m = _mapa_(PROP_FALLIDAS);
  m[id] = new Date().getTime();
  _guardarMapa_(PROP_FALLIDAS, m, MAX_DESCARTADAS);
}

/**
 * Apunta los archivos que no se pudieron clasificar, para no gastar en ellos el cupo de las
 * próximas REINTENTO_H horas. Por la carpeta de Meet pasan tutorías, jurados y reuniones
 * ajenas que NUNCA se van a poder clasificar y que nadie borra: sin esto, el residuo crece y
 * acaba tapando la grabación de ayer. Los que fallaron al moverse ya tienen su propia lista.
 */
function _apuntarDescartes_(quietos) {
  if (!quietos.length) return;
  var m = _mapa_(PROP_DESCARTADAS);
  var ahora = new Date().getTime();
  var n = 0;
  quietos.forEach(function (p) {
    if (!p.id || p.fallo) return;
    m[p.id] = ahora;
    n++;
  });
  if (!n) return;
  _guardarMapa_(PROP_DESCARTADAS, m, MAX_DESCARTADAS);
  Logger.log('Aparcados ' + n + ' archivo(s) sin clasificar: no se vuelven a mirar hasta ' +
             REINTENTO_H + ' h después (reintentarPendientes() los suelta ya). Es lo que ' +
             'impide que el residuo de tutorías y jurados tape las grabaciones nuevas.');
}

// ── avisos ──────────────────────────────────────────────────────────────────

/**
 * El silencio es el fallo más peligroso: si Google vuelve a mover o renombrar las carpetas de
 * Meet, el script barrería un id que no recibe nada y nadie se enteraría hasta que un
 * estudiante preguntara. Y hay un silencio peor, porque no parece un fallo: que haya archivos
 * pero NINGUNO se pueda clasificar (típico si los encuentros de ese curso todavía no están en
 * el Calendar). Así que: hubo clase en las últimas 48 h y no se mueve nada = aviso explícito.
 */
function _avisoSilencio_(cal, lote, plan) {
  var vacio = !lote.archivos.length && !lote.recientes;
  var nadaQueMover = plan && !plan.mover.length;
  if (!vacio && !nadaQueMover) return;
  var ahora = new Date();
  var desde = new Date(ahora.getTime() - 48 * 3600 * 1000);
  var n = 0;
  try {
    n = cal.getEvents(desde, ahora).filter(function (ev) {
      return (ev.getTitle() || '').indexOf(MARCA) >= 0;
    }).length;
  } catch (e) { return; }
  if (!n) return;
  if (vacio) {
    Logger.log('AVISO: no encontré NINGÚN archivo en la carpeta origen y hubo ' + n +
               ' encuentro(s) en las últimas 48 h.');
    Logger.log('Puede ser normal (aún no has grabado, o la grabación tarda), pero si se ' +
               'repite: confirma ORIGEN_ID y que la grabación la inicias TÚ como organizador ' +
               '— si la inicia un coanfitrión, el archivo nace en el Drive de esa persona y ' +
               'este script no puede verlo.');
    return;
  }
  Logger.log('AVISO: hay ' + lote.archivos.length + ' archivo(s) en el origen y hubo ' + n +
             ' encuentro(s) en las últimas 48 h, pero NINGUNO se pudo clasificar.');
  Logger.log('Lee los motivos de «sin clasificar» de arriba. Lo más frecuente: la serie de ' +
             'encuentros de ese curso todavía no existe en tu Calendar (la crea ' +
             '«PRINCIPAL - Crear encuentros con invitados.gs» del curso), o lo que hay en la ' +
             'carpeta son tutorías y jurados, que NO deben publicarse.');
}

/** Disparadores temporales de este proyecto que llaman a moverGrabaciones. */
function _disparadores_() {
  return ScriptApp.getProjectTriggers().filter(function (t) {
    return t.getHandlerFunction() === 'moverGrabaciones';
  });
}

function _estadoDisparador_() {
  var n = _disparadores_().length;
  if (!n) return 'NO instalado (instalarDisparador() lo deja cada ' + CADA_MIN + ' min)';
  return n + ' instalado(s) para moverGrabaciones' +
         (n > 1 ? '  <- SOBRAN: quitarDisparador() y vuelve a instalar' : '') +
         (SIMULAR ? '  ·  pero SIMULAR = true: no mueve nada' : '');
}

// ── fechas ──────────────────────────────────────────────────────────────────

function _dia_(d) { return Utilities.formatDate(d, TIMEZONE, 'dd/MM/yyyy'); }

function _hm_(d) { return Utilities.formatDate(d, TIMEZONE, 'dd/MM HH:mm'); }
