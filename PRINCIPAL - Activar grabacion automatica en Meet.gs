/**
 * ACTIVAR LA GRABACIÓN AUTOMÁTICA en las salas de Meet que ya existen.
 *
 * EL PROBLEMA QUE RESUELVE
 * ------------------------
 * Los encuentros ya están creados y todos comparten UNA sola sala por asignatura —así los crea
 * «PRINCIPAL - Crear encuentros con invitados.gs»—. Eso es la buena noticia: la grabación
 * automática no se configura evento por evento, se configura EN LA SALA. Una llamada por
 * asignatura y quedan cubiertos todos los encuentros: los que ya pasaron, el de hoy y los que
 * queden. No hay que volver a tocar Calendar ni acordarse de pulsar «Grabar».
 *
 * POR QUÉ NO USA UN SERVICIO AVANZADO
 * -----------------------------------
 * Porque NO EXISTE. La primera versión de este script llamaba a `Meet.Spaces.patch()` y fallaba
 * con «Meet is not defined»: la API de Google Meet no está en la lista de servicios avanzados de
 * Apps Script, así que no aparece en Servicios ⊕ y no hay nada que añadir. Se llama a la API REST
 * con UrlFetchApp y el token del propio script.
 *
 * ANTES DE EJECUTAR — SON DOS COSAS, Y LAS DOS SON OBLIGATORIAS
 * -------------------------------------------------------------
 * 1. HABILITAR LA API DE MEET en el proyecto de Cloud del script. Apps Script crea un proyecto
 *    de Google Cloud oculto por cada script, y las APIs vienen apagadas. Sin esto la respuesta es:
 *      403 · «Google Meet API has not been used in project NNNNNN before or it is disabled»
 *    El número del proyecto viene EN ESE MISMO MENSAJE. Se habilita abriendo:
 *      https://console.developers.google.com/apis/api/meet.googleapis.com/overview?project=NNNNNN
 *    y pulsando «Habilitar». Tarda un par de minutos en surtir efecto.
 *    Ojo: Cloud Console pide reautenticarse con contraseña, y en una cuenta institucional el
 *    administrador puede tener restringido el acceso. Si te lo bloquea, mira la ALTERNATIVA de
 *    más abajo, que no necesita Cloud.
 * 2. DECLARAR LOS ALCANCES en el manifiesto: engranaje (Configuración del proyecto) → marca
 *    «Mostrar el archivo de manifiesto appsscript.json», y añade el bloque `oauthScopes` que está
 *    al final de este comentario.
 * 3. Ejecuta `revisar()` PRIMERO. No escribe nada.
 * 4. Si te convence, `activarGrabacion()`.
 *
 * ⚠️ ESTADO EN LA CUENTA DE LA CUN (comprobado el 24/08/2026): EL PASO 1 ESTÁ BLOQUEADO.
 * Cloud Console responde «Necesitas acceso adicional a proyecto 209594026188 · falta
 * resourcemanager.projects.get». El proyecto oculto que Apps Script creó no es accesible para el
 * Docente, así que la API de Meet no se puede habilitar y ESTE SCRIPT NO PUEDE FUNCIONAR tal cual.
 * Para revivirlo haría falta que Sistemas conceda acceso a ese proyecto, o migrar el script a un
 * proyecto de Cloud propio (Configuración del proyecto → Proyecto de Google Cloud → Cambiar).
 *
 * LAS DOS VÍAS QUE SÍ FUNCIONAN HOY, en orden de preferencia
 * ----------------------------------------------------------
 * A) PEDÍRSELO AL ADMINISTRADOR. Es la buena, y hay evidencia de que es viable: la sala de
 *    Proyecto I ya dice «Esta videollamada se está transcribiendo», y eso NO lo activó el Docente
 *    —lo activó un administrador desde Consola de administración → Aplicaciones → Google
 *    Workspace → Google Meet → Configuración de vídeo de Meet → artefactos automáticos—. El mismo
 *    ajuste que enciende la transcripción enciende la grabación. Una petición y queda resuelto
 *    para las cinco asignaturas, para siempre y sin scripts.
 *
 * B) LA CASILLA DE CALENDAR, evento por evento. Abre el evento → en la sección de la videollamada
 *    aparece «Registros de la reunión» con las casillas de grabar, transcribir y tomar notas.
 *    Esas casillas SOLO salen si el evento ya tiene Meet adjunto —en un evento nuevo y vacío no
 *    están, comprobado—. No depende de ningún permiso de Cloud, pero hay que repetirlo en cada
 *    encuentro.
 *
 * El manifiesto tiene que quedar así (conserva lo que ya tenga, añade oauthScopes):
 *
 *   {
 *     "timeZone": "America/Bogota",
 *     "dependencies": {},
 *     "exceptionLogging": "STACKDRIVER",
 *     "runtimeVersion": "V8",
 *     "oauthScopes": [
 *       "https://www.googleapis.com/auth/script.external_request",
 *       "https://www.googleapis.com/auth/meetings.space.settings",
 *       "https://www.googleapis.com/auth/meetings.space.readonly"
 *     ]
 *   }
 *
 * `meetings.space.settings` es el alcance que permite fijar los artefactos automáticos, y Google lo
 * clasifica como NO SENSIBLE: no arrastra proceso de verificación. `meetings.space.readonly` solo
 * sirve para que `revisar()` pueda leer antes de escribir; si prefieres no concederlo, quítalo: el
 * script lo detecta, lo dice, y se apoya en la respuesta del PATCH, que devuelve la sala ya
 * modificada y sirve igual de comprobación.
 *
 * QUÉ HACE, EXACTAMENTE
 * ---------------------
 * Pone `autoRecordingGeneration = ON` en la sala. A partir de ahí Meet empieza a grabar solo
 * cuando entra alguien con permiso de grabar —normalmente tú—. Si nadie con ese permiso entra, no
 * graba: no es un vigilante, es un automatismo atado a tu presencia.
 *
 * REQUISITO QUE NO DEPENDE DE ESTE SCRIPT
 * ---------------------------------------
 * La grabación automática solo existe en Business Plus, Enterprise Standard/Plus, Education Plus y
 * Enterprise Essentials. En tu sala de Proyecto I ya aparece «Esta videollamada se está
 * transcribiendo», así que los artefactos automáticos SÍ están disponibles en tu cuenta. Si tu
 * administrador tuviera la grabación restringida, verás un 403 y el script te lo dirá con esas
 * palabras.
 *
 * Deshacer: `desactivarGrabacion()`.
 */

// ── Las salas, una por asignatura ────────────────────────────────────────────
// El código es lo que va después de meet.google.com/. Acepta también la URL entera.
var SALAS = {
  'Proyecto I': 'omk-woqk-vsj',
  'Investigación': 'jby-wwjm-ocg',
  'Creatividad': 'oeq-ixey-kqh',
  'Trabajo de Grado 2': 'isy-xgom-kio',
  'Trabajo de Grado 3': 'ddh-vhef-fjz'
};

var TAMBIEN_TRANSCRIPCION = true;   // la transcripción ya parece activa; esto la deja explícita
var TAMBIEN_NOTAS_GEMINI = false;   // las notas de Gemini requieren su propia licencia

var BASE = 'https://meet.googleapis.com/v2/spaces/';

// ─────────────────────────────────────────────────────────────────────────────

/** SOLO LECTURA. Qué hay hoy en cada sala y qué cambiaría. Ejecuta esto primero. */
function revisar() {
  var salas = _salasConfiguradas_();
  if (!salas.length) { Logger.log('No hay ninguna sala en SALAS.'); return; }

  Logger.log('REVISIÓN — no se escribe nada\n');
  var sinAlcance = 0;
  salas.forEach(function (s) {
    var r = _llamar_('GET', BASE + s.codigo, null);
    if (!r.ok) {
      if (r.codigo === 403) sinAlcance++;
      Logger.log(s.nombre + ' (' + s.codigo + ')  ✗  HTTP ' + r.codigo + ' · ' + r.mensaje);
      return;
    }
    var a = _artefactos_(r.datos);
    Logger.log(s.nombre + ' (' + s.codigo + ')');
    Logger.log('    grabación     : ' + a.grabacion + (a.grabacion === 'ON' ? '' : '   -> pasaría a ON'));
    Logger.log('    transcripción : ' + a.transcripcion);
    Logger.log('    notas Gemini  : ' + a.notas);
  });
  if (sinAlcance === salas.length) {
    Logger.log('\nNinguna sala se pudo leer, y todas dieron 403. Dos causas posibles:');
    Logger.log('  · falta «meetings.space.readonly» en el manifiesto -> añádelo, o');
    Logger.log('  · decidiste no concederlo -> entonces salta la revisión y ejecuta');
    Logger.log('    activarGrabacion() directamente: su respuesta confirma el cambio.');
  } else {
    Logger.log('\nSi te convence, ejecuta activarGrabacion().');
  }
}

/** ESCRIBE. Deja la grabación automática encendida en las salas configuradas. */
function activarGrabacion() { _aplicar_('ON'); }

/** ESCRIBE. La apaga. Para volver atrás sin pensar. */
function desactivarGrabacion() { _aplicar_('OFF'); }

// ── Interior ─────────────────────────────────────────────────────────────────

function _aplicar_(valor) {
  var salas = _salasConfiguradas_();
  if (!salas.length) { Logger.log('No hay ninguna sala en SALAS.'); return; }

  var hechos = 0, fallos = [];
  salas.forEach(function (s) {
    // Se manda SOLO lo que se cambia, y updateMask lo nombra campo por campo. Mandar el objeto
    // de configuración entero es la forma de pisar sin querer algo que no querías tocar.
    var art = { recordingConfig: { autoRecordingGeneration: valor } };
    var mascara = ['config.artifactConfig.recordingConfig.autoRecordingGeneration'];
    if (TAMBIEN_TRANSCRIPCION) {
      art.transcriptionConfig = { autoTranscriptionGeneration: valor };
      mascara.push('config.artifactConfig.transcriptionConfig.autoTranscriptionGeneration');
    }
    if (TAMBIEN_NOTAS_GEMINI) {
      art.smartNotesConfig = { autoSmartNotesGeneration: valor };
      mascara.push('config.artifactConfig.smartNotesConfig.autoSmartNotesGeneration');
    }
    var url = BASE + s.codigo + '?updateMask=' + encodeURIComponent(mascara.join(','));
    var r = _llamar_('PATCH', url, { config: { artifactConfig: art } });

    if (r.ok) {
      // La respuesta del PATCH trae la sala ya modificada: es la comprobación, no hace falta releer.
      var a = _artefactos_(r.datos);
      hechos++;
      Logger.log('OK  ' + s.nombre + ' (' + s.codigo + ') -> grabación ' + a.grabacion +
                 ' · transcripción ' + a.transcripcion);
    } else {
      fallos.push({ n: s.nombre, c: r.codigo, m: r.mensaje });
      Logger.log('✗   ' + s.nombre + ' (' + s.codigo + ')  HTTP ' + r.codigo + ' · ' + r.mensaje);
    }
  });

  Logger.log('\n' + hechos + ' de ' + salas.length + ' salas con grabación ' + valor + '.');
  if (fallos.length) {
    Logger.log('\nQué significa cada error, porque no son el mismo problema:');
    Logger.log('  · 401/403 con «insufficient authentication scopes» -> falta el alcance en el');
    Logger.log('    manifiesto. Añádelo, guarda, y vuelve a ejecutar: pedirá permiso otra vez.');
    Logger.log('  · 403 con «permission» o «not allowed» -> tu administrador tiene la grabación');
    Logger.log('    restringida. Eso no lo arregla ningún script: hay que pedirlo a Sistemas.');
    Logger.log('  · 404 -> el código de la sala no es ese, o la sala no la creaste tú.');
    Logger.log('  · 400 con «updateMask» -> Google cambió el nombre del campo; hay que releer');
    Logger.log('    la referencia de spaces.patch.');
    fallos.forEach(function (f) { Logger.log('      ' + f.n + ' (' + f.c + '): ' + f.m); });
  }
}

function _llamar_(metodo, url, cuerpo) {
  var opciones = {
    method: metodo,
    muteHttpExceptions: true,          // sin esto, un 403 lanza y no se puede explicar
    headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() },
    contentType: 'application/json'
  };
  if (cuerpo) opciones.payload = JSON.stringify(cuerpo);

  var resp, texto;
  try {
    resp = UrlFetchApp.fetch(url, opciones);
    texto = resp.getContentText();
  } catch (e) {
    return { ok: false, codigo: 0, mensaje: String(e).replace(/\s+/g, ' ').slice(0, 170) };
  }
  var codigo = resp.getResponseCode();
  var datos = null;
  try { datos = JSON.parse(texto); } catch (e) { /* respuesta no-JSON: se reporta cruda */ }

  if (codigo >= 200 && codigo < 300) return { ok: true, codigo: codigo, datos: datos || {} };

  var msg = (datos && datos.error && datos.error.message) || texto || 'sin cuerpo';
  return { ok: false, codigo: codigo, mensaje: String(msg).replace(/\s+/g, ' ').slice(0, 170) };
}

function _salasConfiguradas_() {
  var out = [];
  Object.keys(SALAS).forEach(function (nombre) {
    var c = String(SALAS[nombre] || '').trim();
    if (!c) return;
    c = c.replace(/^https?:\/\/meet\.google\.com\//i, '').replace(/[?#].*$/, '').trim();
    out.push({ nombre: nombre, codigo: c });
  });
  return out;
}

function _artefactos_(espacio) {
  var cfg = (espacio && espacio.config) || {};
  var art = cfg.artifactConfig || {};
  return {
    grabacion: ((art.recordingConfig || {}).autoRecordingGeneration) || 'sin fijar',
    transcripcion: ((art.transcriptionConfig || {}).autoTranscriptionGeneration) || 'sin fijar',
    notas: ((art.smartNotesConfig || {}).autoSmartNotesGeneration) || 'sin fijar'
  };
}
