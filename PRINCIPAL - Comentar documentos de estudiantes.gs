/**
 * CUN — Comentar el documento de un estudiante con los criterios de su ACA.
 *
 * ARCHIVO GENERADO — NO EDITAR A MANO.
 * Regenerar: python config/gdocs/build_apps_script_comentarios.py
 *
 * Este archivo se pega UNA VEZ y se queda. Lo que cambia en cada revisión es el otro archivo,
 * «Plan.gs», que lo produce `config/gdocs/plan_comentarios.py`.
 *
 * QUÉ EJECUTAR, EN ESTE ORDEN
 *   verificar()  → no escribe nada. Comprueba acceso, criterios y que cada cita siga en el
 *                  documento. Ejecútalo siempre primero.
 *   simular()    → no escribe nada. Imprime el comentario EXACTO que vería el estudiante.
 *   publicar()   → publica de verdad. Exige CONFIRMAR = true en Plan.gs.
 *   deshacer()   → borra los comentarios de la última publicación.
 *
 * NO PUEDE MODIFICAR EL DOCUMENTO. Solo lee (Docs API) y crea o borra comentarios (Drive API).
 * No hay ninguna llamada que escriba en el cuerpo del texto del estudiante.
 *
 * Los comentarios salen a nombre de la cuenta que ejecuta el script.
 */

// Línea que se añade al final de cada comentario. Vacía = no se añade nada.
// Las guías de ACA le exigen al estudiante «uso transparente de IA si la usaste»; si quieres
// corresponder, aquí es donde se declara. Ejemplo:
//   var NOTA_IA = '— Retroalimentación redactada con apoyo de IA y revisada por el Docente.';
var NOTA_IA = '';

// ─── Generado desde el repositorio: no editar ───
var CRITERIOS = {
  "creatividad": {
    "acafinal": {
      "guia": "ACA Final (32,8%) - Propuesta de Innovacion",
      "criterios": [
        "Usuario y problema concretos (no genéricos)",
        "Tipo de innovación bien justificado (Oslo)",
        "FODA y Canvas coherentes con el problema",
        "MVP claro y verificable",
        "Vigilancia tecnológica con fuentes",
        "Entidades de apoyo identificadas",
        "Pitch claro · presentación cuidada · integridad académica"
      ]
    }
  },
  "investigacion": {
    "acafinal": {
      "guia": "ACA Final (32,8%) - Articulo de nuevo conocimiento",
      "criterios": [
        "Línea de Ingeniería explícita y pertinente",
        "Problema argumentado con evidencias",
        "Pregunta clara y viable",
        "Fuentes confiables y matriz de fuentes completa",
        "Marco/revisión alineado a la pregunta (no un listado desconectado)",
        "Citas y referencias APA 7 · integridad académica",
        "Mejoras respecto a los avances previos"
      ]
    }
  },
  "proyecto1": {
    "aca1": {
      "guia": "ACA 1 (25%) - Formulacion del problema y fundamentacion referencial",
      "criterios": [
        "Coherencia entre problema, pregunta y objetivos",
        "Pertinencia del problema al campo / líneas del programa",
        "Justificación argumentada (no solo opinión)",
        "Alcances y limitaciones realistas",
        "Antecedentes ≥ 6 (nacionales e internacionales)",
        "Marco teórico, conceptual y contextual pertinentes y actualizados",
        "Escritura académica e integridad (citas, sin plagio)",
        "Referencias APA 7"
      ]
    },
    "acafinal": {
      "guia": "ACA FINAL (42%) - Anteproyecto integrado",
      "criterios": [
        "Correcciones de la ACA 1 incorporadas",
        "Metodología coherente con pregunta y objetivos",
        "Instrumentos propuestos (no aplicados)",
        "Cronograma y presupuesto/viabilidad",
        "Coherencia global del anteproyecto",
        "Escritura, fuentes, integridad y viabilidad"
      ]
    }
  },
  "tg2": {
    "acafinal": {
      "guia": "ACA Final (32,8%) - Avance consolidado hacia TG3",
      "criterios": [
        "Estado del proyecto y delimitación explícitos",
        "Problema, pregunta y objetivos coherentes",
        "Antecedentes y marcos pertinentes y actualizados",
        "Metodología propuesta coherente con la pregunta",
        "Instrumentos y plan de análisis definidos (propuestos)",
        "Documento integrado (no fragmentos pegados)",
        "Preparación explícita para TG3 · APA 7 · integridad académica"
      ]
    }
  },
  "tg3": {
    "acafinal": {
      "guia": "ACA Final (32%) - Documento final de grado",
      "criterios": [
        "Coherencia problema–pregunta–objetivos–método–resultados",
        "Revisión bibliográfica rigurosa (≥ 50 referencias)",
        "Extensión ≥ 4.000 palabras",
        "APA 7 e integridad académica (antiplagio verificado)",
        "Resultados y discusión sostenidos en evidencia",
        "Póster y evidencias listos"
      ]
    }
  }
};
var EQUIVALENCIAS = {
  "‘": "'",
  "’": "'",
  "‚": "'",
  "‛": "'",
  "“": "\"",
  "”": "\"",
  "„": "\"",
  "«": "\"",
  "»": "\"",
  "–": "-",
  "—": "-",
  "−": "-",
  "‐": "-",
  "‑": "-",
  " ": " ",
  " ": " ",
  " ": " ",
  "​": "",
  "…": "..."
};

// ─────────────────────────────────────────────────────────────────────────────

function verificar() { return _correr('verificar'); }
function simular()   { return _correr('simular'); }
function publicar()  { return _correr('publicar'); }

/**
 * Nunca se llama. Existe porque Apps Script decide los permisos leyendo el código: esta referencia
 * a DriveApp es lo que hace que la autorización pida https://www.googleapis.com/auth/drive, el
 * alcance que necesitan la API de Docs (leer) y la de Drive (comentar). Sin ella,
 * ScriptApp.getOAuthToken() devolvería un token sin permisos y todo fallaría con un 401.
 */
function _alcance_() {
  if (new Date().getTime() < 0) { DriveApp.getRootFolder(); }
}

function _norm(s) {
  s = String(s == null ? '' : s).normalize('NFC');
  for (var a in EQUIVALENCIAS) { s = s.split(a).join(EQUIVALENCIAS[a]); }
  return s.replace(/\s+/g, ' ').trim();
}

function _token() { return 'Bearer ' + ScriptApp.getOAuthToken(); }

function _pista(codigo) {
  if (codigo === 401) return 'El token no trae permisos: reautoriza el script (ver el runbook).';
  if (codigo === 403) return 'La cuenta no tiene permiso sobre ese documento. ¿Te lo compartieron como Comentador?';
  if (codigo === 404) return 'No existe ese docId, o esta cuenta no lo ve.';
  return '';
}

function _get(url, queDecir) {
  var r = UrlFetchApp.fetch(url, {
    method: 'get', headers: {Authorization: _token()}, muteHttpExceptions: true
  });
  if (r.getResponseCode() !== 200) {
    throw new Error(queDecir + ' — HTTP ' + r.getResponseCode() + '. ' + _pista(r.getResponseCode()) +
                    '\n' + r.getContentText().slice(0, 400));
  }
  return JSON.parse(r.getContentText());
}

function _metadatos(docId) {
  return _get('https://www.googleapis.com/drive/v3/files/' + encodeURIComponent(docId) +
              '?supportsAllDrives=true&fields=name,owners(displayName,emailAddress),capabilities(canComment)',
              'No se pudieron leer los datos del documento');
}

/** Aplana el documento a párrafos numerados, arrastrando el último encabezado como sección.
 *  Recorre también las celdas de las tablas: el cronograma y el presupuesto van en tabla. */
function _parrafos(doc) {
  var salida = [], seccion = '';
  function parrafo(el) {
    if (!el.paragraph) return;
    var estilo = (el.paragraph.paragraphStyle && el.paragraph.paragraphStyle.namedStyleType) || 'NORMAL_TEXT';
    var txt = (el.paragraph.elements || []).map(function (e) {
      return (e.textRun && e.textRun.content) || '';
    }).join('').trim();
    if (!txt) return;
    if (estilo.indexOf('HEADING') === 0 || estilo === 'TITLE') seccion = txt;
    salida.push({n: salida.length + 1, seccion: seccion, texto: txt});
  }
  function recorrer(contenido) {
    (contenido || []).forEach(function (el) {
      parrafo(el);
      if (el.table) {
        (el.table.tableRows || []).forEach(function (fila) {
          (fila.tableCells || []).forEach(function (celda) { recorrer(celda.content); });
        });
      }
    });
  }
  recorrer(doc.body && doc.body.content);
  return salida;
}

/** Localiza la cita en el documento VIVO. Devuelve {n, seccion} o null. */
function _ubicar(parrafos, cita) {
  var aguja = _norm(cita);
  if (!aguja) return null;
  for (var i = 0; i < parrafos.length; i++) {
    if (_norm(parrafos[i].texto).indexOf(aguja) >= 0) {
      return {n: parrafos[i].n, seccion: parrafos[i].seccion, varios: false};
    }
  }
  var entero = _norm(parrafos.map(function (p) { return p.texto; }).join(' '));
  if (entero.indexOf(aguja) >= 0) return {n: 0, seccion: '', varios: true};
  return null;
}

function _correr(modo) {
  if (typeof PLAN === 'undefined') {
    throw new Error('Falta el archivo «Plan.gs». Lo genera config/gdocs/plan_comentarios.py.');
  }
  var log = [];
  function d(t) { log.push(t); Logger.log(t); }

  d('modo      : ' + modo.toUpperCase());
  d('cuenta    : ' + Session.getActiveUser().getEmail());

  // 1. Los criterios del plan tienen que estar en la guía que recibió el estudiante.
  var guia = CRITERIOS[PLAN.curso] && CRITERIOS[PLAN.curso][PLAN.aca];
  if (!guia) {
    throw new Error('No hay guía para curso=«' + PLAN.curso + '» aca=«' + PLAN.aca + '». ' +
                    'Recuerda: pregrado solo tiene ACA Final.');
  }
  d('guía      : ' + guia.guia);
  var validos = {};
  guia.criterios.forEach(function (c) { validos[_norm(c)] = c; });
  var invalidos = PLAN.comentarios.filter(function (c) { return !validos[_norm(c.criterio)]; });
  if (invalidos.length) {
    throw new Error('Estos criterios no están en la guía:\n  ' +
      invalidos.map(function (c) { return c.criterio; }).join('\n  ') +
      '\nLa guía dice:\n  ' + guia.criterios.join('\n  '));
  }

  // 2. Acceso al documento.
  var meta = _metadatos(PLAN.docId);
  var dueno = (meta.owners || [{}])[0] || {};
  d('documento : ' + meta.name);
  d('dueño     : ' + (dueno.displayName || '?') + ' <' + (dueno.emailAddress || '?') + '>');
  var puede = !!(meta.capabilities && meta.capabilities.canComment);
  d('comentar  : ' + (puede ? 'SÍ' : 'NO'));
  if (!puede) {
    throw new Error('Lo compartieron en modo Lector. Pídele acceso de «Comentador» — con ese basta, ' +
                    'no hace falta Editor.');
  }

  // 3. Cada cita tiene que seguir en el documento vivo.
  var parrafos = _parrafos(_get('https://docs.googleapis.com/v1/documents/' +
                                encodeURIComponent(PLAN.docId), 'No se pudo leer el documento'));
  d('párrafos  : ' + parrafos.length);
  d('');

  var listos = [], perdidas = 0;
  PLAN.comentarios.forEach(function (c, i) {
    var donde = _ubicar(parrafos, c.cita);
    if (!donde) {
      perdidas++;
      d('✗ ' + (i + 1) + '. ' + c.criterio);
      d('    la cita ya no está en el documento (el estudiante la editó). Se OMITE.');
      d('    cita: «' + String(c.cita).slice(0, 110) + '»');
      return;
    }
    var cabecera = 'Criterio «' + validos[_norm(c.criterio)] + '»';
    if (donde.seccion) cabecera += ' — ' + donde.seccion;
    if (donde.varios) cabecera += ' (abarca varios párrafos)';
    else cabecera += ' (párrafo ' + donde.n + ')';
    var cuerpo = cabecera + '\n\n' + String(c.texto).trim();
    if (NOTA_IA) cuerpo += '\n\n' + NOTA_IA;
    listos.push({cuerpo: cuerpo, cita: c.cita, criterio: c.criterio});
    if (modo !== 'verificar') {
      d('─── ' + (i + 1) + '. ' + c.criterio + ' ───');
      d('cita: «' + String(c.cita).slice(0, 140) + '»');
      d(cuerpo);
      d('');
    } else {
      d('✓ ' + (i + 1) + '. ' + c.criterio + '  → párrafo ' + (donde.n || '?'));
    }
  });

  d('');
  d('en pie ' + listos.length + ' · omitidos ' + perdidas + ' de ' + PLAN.comentarios.length);

  if (modo !== 'publicar') {
    d(modo + ': no se publicó nada. El documento queda intacto.');
    return log.join('\n');
  }
  if (typeof CONFIRMAR === 'undefined' || CONFIRMAR !== true) {
    throw new Error('CONFIRMAR está en false. Revisa la salida de simular() y, si te convence, ' +
                    'pon `var CONFIRMAR = true;` en Plan.gs y vuelve a ejecutar publicar().');
  }
  if (!listos.length) throw new Error('No queda ningún comentario publicable.');

  var ids = [];
  listos.forEach(function (c) {
    var r = UrlFetchApp.fetch(
      'https://www.googleapis.com/drive/v3/files/' + encodeURIComponent(PLAN.docId) +
      '/comments?fields=id',
      {
        method: 'post', contentType: 'application/json',
        headers: {Authorization: _token()},
        // `quotedFileContent` es la única forma de que el comentario diga a qué frase se refiere:
        // Google muestra como NO anclados los comentarios que ancla un tercero por API.
        payload: JSON.stringify({
          content: c.cuerpo,
          quotedFileContent: {mimeType: 'text/plain', value: String(c.cita).slice(0, 1000)}
        }),
        muteHttpExceptions: true
      });
    if (r.getResponseCode() >= 300) {
      throw new Error('Falló al publicar «' + c.criterio + '» — HTTP ' + r.getResponseCode() +
                      '. ' + _pista(r.getResponseCode()) + '\n' + r.getContentText().slice(0, 300) +
                      '\nYa se publicaron ' + ids.length + '; deshacer() los quita.');
    }
    ids.push(JSON.parse(r.getContentText()).id);
    d('+ ' + c.criterio);
  });

  PropertiesService.getScriptProperties().setProperty('ultima_publicacion', JSON.stringify({
    docId: PLAN.docId, titulo: meta.name, ids: ids,
    cuando: Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm')
  }));
  d('');
  d('OK ' + ids.length + ' comentarios publicados en «' + meta.name + '».');
  d('Si algo salió mal, deshacer() los borra.');
  return log.join('\n');
}

/** Borra los comentarios de la última publicación. */
function deshacer() {
  var crudo = PropertiesService.getScriptProperties().getProperty('ultima_publicacion');
  if (!crudo) { Logger.log('No hay ninguna publicación registrada que deshacer.'); return; }
  var u = JSON.parse(crudo);
  Logger.log('Deshaciendo ' + u.ids.length + ' comentarios de «' + u.titulo + '» (' + u.cuando + ')');
  var borrados = 0;
  u.ids.forEach(function (id) {
    var r = UrlFetchApp.fetch(
      'https://www.googleapis.com/drive/v3/files/' + encodeURIComponent(u.docId) +
      '/comments/' + encodeURIComponent(id),
      {method: 'delete', headers: {Authorization: _token()}, muteHttpExceptions: true});
    if (r.getResponseCode() < 300 || r.getResponseCode() === 404) borrados++;
    else Logger.log('  no se pudo borrar ' + id + ' — HTTP ' + r.getResponseCode());
  });
  PropertiesService.getScriptProperties().deleteProperty('ultima_publicacion');
  Logger.log('Borrados ' + borrados + ' de ' + u.ids.length + '. Registro limpiado.');
}
