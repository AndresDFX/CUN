# -*- coding: utf-8 -*-
"""Genera la V2 del Apps Script de grabaciones de Meet — versión PARAMETRIZABLE.

La v1 (`build_apps_script_grabaciones.py`) inyecta todo desde el repositorio: lee
`carga_academica.py`, `sesiones_cun.py` y `carga_academica_2026.json` y genera un .gs con
las constantes ya resueltas. Cambiar un curso obliga a regenerar.

Esta v2 DEJA UN DICCIONARIO EDITABLE al principio del .gs: el docente lo edita directo en Apps
Script sin tocar el generador. Por cada curso: un fragmento del título, el código de Meet (si
aplica) y el enlace de la carpeta destino. Eso es TODO lo que se configura.

Uso:
  python config/slides/build_apps_script_grabaciones_v2.py

Escribe:
  - PRINCIPAL - Mover grabaciones de Meet (v2).gs
  - LEEME - Mover las grabaciones de Meet (v2).md
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GS_NAME = "PRINCIPAL - Mover grabaciones de Meet (v2).gs"
LEEME_NAME = "LEEME - Mover las grabaciones de Meet (v2).md"

# ── el .gs ─────────────────────────────────────────────────────────────
GS_CONTENT = """/**
 * GRABACIONES DE MEET — V2 PARAMETRIZABLE
 *
 * Mueve cada grabación de Meet a la carpeta de Drive que le corresponde, según el curso.
 * La configuración está en el diccionario CONFIG_CURSOS (línea 30): por cada curso pones un
 * fragmento del título, el código de Meet si aplica, y la carpeta destino. Eso es TODO.
 *
 * DIFERENCIAS CON LA V1
 * - La v1 usa UN destino para todo y crea subcarpetas por materia. Esta v2 deja que CADA
 *   curso vaya a SU CARPETA, y no crea subcarpetas: todo queda suelto ahí.
 * - La v1 se regenera desde Python cada vez que cambias un curso. Esta v2 se EDITA DIRECTO
 *   en Apps Script: cambias el diccionario de abajo y listo.
 * - La v1 consulta Calendar para corregir el número de sesión. Esta v2 NO: se queda con el
 *   número de sesión del nombre del archivo (que Meet congela). Es más rápido y no pide
 *   permisos de Calendar, a cambio de no corregir nada.
 *
 * PASOS
 * 1. https://script.google.com con la cuenta que ORGANIZA las clases (las grabaciones nacen
 *    en SU Mi unidad).
 * 2. Nuevo proyecto -> pega TODO este archivo -> guarda.
 * 3. Edita CONFIG_CURSOS (abajo): por cada curso, el fragmento del título, el código de Meet
 *    (si todos usan la misma sala) y la carpeta destino. Pega el ENLACE tal cual, no el id.
 * 4. Pega en ORIGEN_ID el enlace de la carpeta de Meet de Mi unidad (Meet Recordings).
 * 5. Ejecuta verificarGrabaciones() (solo lectura) y lee el registro entero.
 * 6. Si cuadra: pon SIMULAR = false, guarda y ejecuta moverGrabaciones() UNA vez a mano.
 * 7. instalarDisparador() -> corre solo cada 30 minutos.
 *
 * Deshacer: revertirMovimientos() (devuelve todo) · quitarDisparador() (para el automatismo)
 *           olvidarRegistro() (suelta el historial) · reintentarPendientes() (lo fallido).
 */

// ═══════════════════════ CONFIGURACIÓN POR CURSO ═══════════════════════
// Edita esta tabla para agregar cursos o cambiar destinos. Por cada curso:
//   tituloContiene: fragmento del título (busca con "contains", NO tiene que ser exacto)
//   meetLink: código de la sala (el «abc-defg-hij» de meet.google.com/abc-defg-hij)
//             O déjalo en "" si no todos usan la misma sala
//   carpetaDestino: enlace o ID de la carpeta de Drive donde van las grabaciones de ESE curso

var CONFIG_CURSOS = [
  {
    tituloContiene: "Trabajo de grado 3",
    meetLink: "",
    carpetaDestino: ""  // <- pega aquí el enlace de la carpeta de TG3
  },
  {
    tituloContiene: "Trabajo de grado 2",
    meetLink: "",
    carpetaDestino: ""
  },
  {
    tituloContiene: "Proyecto I",
    meetLink: "",  // <- si todos usan meet.google.com/abc-defg-hij, pon "abc-defg-hij"
    carpetaDestino: ""
  },
  {
    tituloContiene: "Creatividad",
    meetLink: "",
    carpetaDestino: ""
  },
  {
    tituloContiene: "Investigación",
    meetLink: "",
    carpetaDestino: ""
  }
];

// ═══════════════════════ CONFIGURACIÓN GENERAL ═════════════════════════

// MODO SIMULACIÓN: con true nada escribe, solo dice qué haría. Ponlo en false cuando
// verificarGrabaciones() te cuadre.
var SIMULAR = true;

var TIMEZONE = 'America/Bogota';

// ORIGEN — carpeta donde Meet deja las grabaciones (Meet Recordings o Google Meet).
// VACÍO A PROPÓSITO: pega aquí el ENLACE tal cual, el de la barra de direcciones.
// Mientras esté vacío, verificarGrabaciones() te SUGIERE candidatos y no mueve nada.
var ORIGEN_ID = '';

// Subcarpeta antigua de grabaciones (Legacy Meet Recordings), si aplica. Déjalo vacío si no
// la tienes o si no quieres barrer lo viejo todavía.
var ORIGEN_LEGACY_ID = '';

// Cuánto esperar antes de mover un archivo recién creado (minutos)
var MARGEN_MIN = 20;

// Fecha límite: solo mueve archivos creados ANTES de esta fecha (formato YYYY-MM-DD).
// Si está vacío, mueve todo sin mirar la fecha de creación.
// Útil para separar grabaciones de diferentes periodos académicos sin depender del nombre.
var FECHA_HASTA = '';  // ej: '2026-12-31' para mover solo archivos del semestre 2026-ES4

// ══════════════════════════════ LÓGICA ══════════════════════════════════

var RX_FECHA = /(\\d{4})[-_\\/ ](\\d{2})[-_\\/ ](\\d{2})[ _T]+(\\d{2})[:._h ](\\d{2})(?:[^)]*?GMT\\s*([+-]\\d{2}))?/;
var RX_SESSION = /Sesi[oó]n\\s+(\\d{1,2})/i;
var SUFIJOS_ARTEFACTO = [' - Recording', ' - Transcript', ' - Chat'];
var NOMBRES_ORIGEN = ['Meet Recordings', 'Google Meet'];
var NOMBRES_LEGACY = ['Legacy Meet Recordings'];

var MAX_ARCHIVOS = 200;
var MAX_MOVIMIENTOS = 50;
var LIMITE_MS = 4.5 * 60 * 1000;

// ── helpers ──────────────────────────────────────────────────────────────

function _idDeCarpeta_(textoOUrl) {
  if (!textoOUrl || textoOUrl.trim() === '') return '';
  var t = textoOUrl.trim();
  // si es un enlace de Drive, extrae el id
  var m = t.match(/\/folders\/([a-zA-Z0-9_-]+)/);
  if (m) return m[1];
  m = t.match(/[?&]id=([a-zA-Z0-9_-]+)/);
  if (m) return m[1];
  // si lleva /d/, es un archivo (no carpeta)
  if (t.indexOf('/d/') >= 0) return '';
  // lo demás se toma como id pelado
  return t.replace(/[?&].*$/, '');
}

function _parseFecha_(nombre) {
  var m = nombre.match(RX_FECHA);
  if (!m) return null;
  var yyyy = m[1], mm = m[2], dd = m[3], hh = m[4], min = m[5];
  return Utilities.parseDate(yyyy + '-' + mm + '-' + dd + ' ' + hh + ':' + min, TIMEZONE, 'yyyy-MM-dd HH:mm');
}

function _parseSession_(nombre) {
  var m = nombre.match(RX_SESSION);
  return m ? parseInt(m[1], 10) : null;
}

function _esArtefactoMeet_(nombre) {
  for (var i = 0; i < SUFIJOS_ARTEFACTO.length; i++) {
    if (nombre.indexOf(SUFIJOS_ARTEFACTO[i]) >= 0) return true;
  }
  return false;
}

function _quitarSufijo_(nombre) {
  for (var i = 0; i < SUFIJOS_ARTEFACTO.length; i++) {
    var suf = SUFIJOS_ARTEFACTO[i];
    var idx = nombre.indexOf(suf);
    if (idx >= 0) return nombre.substring(0, idx);
  }
  return nombre;
}

function _clasificarPorTitulo_(base) {
  for (var i = 0; i < CONFIG_CURSOS.length; i++) {
    var cfg = CONFIG_CURSOS[i];

    // Verificar el título
    if (cfg.tituloContiene && base.toLowerCase().indexOf(cfg.tituloContiene.toLowerCase()) >= 0) {
      return cfg;
    }
  }
  return null;
}

function _clasificarPorMeetLink_(meetLink, base) {
  if (!meetLink) return null;
  for (var i = 0; i < CONFIG_CURSOS.length; i++) {
    var cfg = CONFIG_CURSOS[i];

    if (cfg.meetLink && cfg.meetLink === meetLink) {
      return cfg;
    }
  }
  return null;
}

function _carpetaPorId_(id) {
  if (!id) return null;
  try {
    return DriveApp.getFolderById(id);
  } catch (e) {
    return null;
  }
}

function _sugerirOrigenes_() {
  var cands = [];
  var all = DriveApp.getFolders();
  while (all.hasNext()) {
    var f = all.next();
    var n = f.getName();
    for (var i = 0; i < NOMBRES_ORIGEN.length; i++) {
      if (n === NOMBRES_ORIGEN[i]) {
        cands.push(f.getId() + ' <- ' + n);
        break;
      }
    }
    for (var j = 0; j < NOMBRES_LEGACY.length; j++) {
      if (n === NOMBRES_LEGACY[j]) {
        cands.push(f.getId() + ' <- ' + n + ' (legacy)');
        break;
      }
    }
  }
  return cands;
}

function _prop_(k) {
  return 'GRABACIONES_V2_' + k;
}

function _leer_() {
  var ps = PropertiesService.getScriptProperties();
  var raw = ps.getProperty(_prop_('MOVIMIENTOS'));
  return raw ? JSON.parse(raw) : [];
}

function _escribir_(arr) {
  PropertiesService.getScriptProperties().setProperty(_prop_('MOVIMIENTOS'), JSON.stringify(arr));
}

function _registrar_(fileId, nombreViejo, carpetaViejaId, carpetaNuevaId, razon) {
  var mov = _leer_();
  mov.push({
    fileId: fileId,
    nombreViejo: nombreViejo,
    carpetaViejaId: carpetaViejaId,
    carpetaNuevaId: carpetaNuevaId,
    razon: razon,
    cuando: new Date().toISOString()
  });
  _escribir_(mov);
}

// ── funciones principales ────────────────────────────────────────────────

function verificarGrabaciones() {
  Logger.log('═════════ VERIFICAR GRABACIONES (v2) ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var origenId = _idDeCarpeta_(ORIGEN_ID);
  if (!origenId) {
    Logger.log('⚠️  ORIGEN_ID vacío. Pega el enlace de tu carpeta de Meet.');
    Logger.log('Candidatos sugeridos:');
    var sugs = _sugerirOrigenes_();
    for (var i = 0; i < sugs.length; i++) {
      Logger.log('  ' + sugs[i]);
    }
    return;
  }

  var origen = _carpetaPorId_(origenId);
  if (!origen) {
    Logger.log('❌ No se pudo abrir ORIGEN_ID: ' + origenId);
    return;
  }
  Logger.log('✓ Origen: ' + origen.getName() + ' (' + origenId + ')');
  Logger.log('');

  // validar destinos
  Logger.log('Validando destinos de CONFIG_CURSOS:');
  for (var i = 0; i < CONFIG_CURSOS.length; i++) {
    var cfg = CONFIG_CURSOS[i];
    var destId = _idDeCarpeta_(cfg.carpetaDestino);
    if (!destId) {
      Logger.log('  ⚠️  [' + cfg.tituloContiene + '] carpetaDestino vacía');
    } else {
      var carpeta = _carpetaPorId_(destId);
      if (carpeta) {
        Logger.log('  ✓ [' + cfg.tituloContiene + '] -> ' + carpeta.getName());
      } else {
        Logger.log('  ❌ [' + cfg.tituloContiene + '] carpetaDestino inválida: ' + destId);
      }
    }
  }
  Logger.log('');

  var ahora = new Date();
  var margen = MARGEN_MIN * 60 * 1000;
  var archivos = origen.getFiles();
  var cuenta = 0, candidatos = 0, viejos = 0;

  Logger.log('Archivos en origen:');
  while (archivos.hasNext() && cuenta < MAX_ARCHIVOS) {
    var file = archivos.next();
    cuenta++;
    var nombre = file.getName();

    if (!_esArtefactoMeet_(nombre)) {
      Logger.log('  [' + cuenta + '] ' + nombre + ' <- NO es artefacto de Meet, se ignora');
      continue;
    }

    var creado = file.getDateCreated();
    var edad = ahora.getTime() - creado.getTime();
    if (edad < margen) {
      viejos++;
      continue;  // muy reciente, no lo muestro
    }

    candidatos++;
    var base = _quitarSufijo_(nombre);
    var sesion = _parseSession_(nombre);
    var cfg = _clasificarPorTitulo_(base);

    if (cfg) {
      Logger.log('  [' + cuenta + '] ' + nombre);
      Logger.log('       -> [' + cfg.tituloContiene + '] sesión ' + (sesion || '?'));
    } else {
      Logger.log('  [' + cuenta + '] ' + nombre + ' <- NO clasificado');
    }
  }

  Logger.log('');
  Logger.log('Total: ' + cuenta + ' archivos, ' + candidatos + ' movibles, ' + viejos + ' muy recientes');
  Logger.log('');
  Logger.log('Si cuadra: pon SIMULAR = false y ejecuta moverGrabaciones().');
}

function moverGrabaciones() {
  var inicio = new Date().getTime();
  Logger.log('═════════ MOVER GRABACIONES (v2) ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var origenId = _idDeCarpeta_(ORIGEN_ID);
  if (!origenId) {
    Logger.log('❌ ORIGEN_ID vacío.');
    return;
  }

  var origen = _carpetaPorId_(origenId);
  if (!origen) {
    Logger.log('❌ No se pudo abrir origen: ' + origenId);
    return;
  }

  var ahora = new Date();
  var margen = MARGEN_MIN * 60 * 1000;
  var archivos = origen.getFiles();
  var movidos = 0, descartados = 0, errores = 0;

  while (archivos.hasNext() && movidos < MAX_MOVIMIENTOS) {
    if (new Date().getTime() - inicio > LIMITE_MS) {
      Logger.log('⏱️  Límite de tiempo alcanzado. Continúa en la próxima pasada.');
      break;
    }

    var file = archivos.next();
    var nombre = file.getName();

    if (!_esArtefactoMeet_(nombre)) {
      descartados++;
      continue;
    }

    var creado = file.getDateCreated();
    var edad = ahora.getTime() - creado.getTime();
    if (edad < margen) {
      continue;  // muy reciente
    }

    // Verificar fecha límite si está configurada
    if (FECHA_HASTA && FECHA_HASTA.trim() !== '') {
      var limite = new Date(FECHA_HASTA + ' 23:59:59');
      if (creado > limite) {
        continue;  // archivo creado después del límite, no lo movemos
      }
    }

    var base = _quitarSufijo_(nombre);
    var cfg = _clasificarPorTitulo_(base);

    if (!cfg) {
      Logger.log('❓ ' + nombre + ' <- NO clasificado, se deja quieto');
      descartados++;
      continue;
    }

    var destId = _idDeCarpeta_(cfg.carpetaDestino);
    if (!destId) {
      Logger.log('⚠️  ' + nombre + ' -> [' + cfg.tituloContiene + '] carpetaDestino vacía');
      errores++;
      continue;
    }

    var destino = _carpetaPorId_(destId);
    if (!destino) {
      Logger.log('❌ ' + nombre + ' -> carpeta inválida: ' + destId);
      errores++;
      continue;
    }

    try {
      if (SIMULAR) {
        Logger.log('✓ SIMULAR: ' + nombre + ' -> ' + destino.getName());
      } else {
        file.moveTo(destino);
        _registrar_(file.getId(), nombre, origenId, destId, cfg.tituloContiene);
        Logger.log('✓ MOVIDO: ' + nombre + ' -> ' + destino.getName());
      }
      movidos++;
    } catch (e) {
      Logger.log('❌ ERROR al mover ' + nombre + ': ' + e.toString());
      errores++;
    }
  }

  Logger.log('');
  Logger.log('Resumen: ' + movidos + ' movidos, ' + descartados + ' descartados, ' + errores + ' errores');
}

function revertirMovimientos() {
  Logger.log('═════════ REVERTIR MOVIMIENTOS ═════════');
  Logger.log('SIMULAR = ' + SIMULAR);
  Logger.log('');

  var mov = _leer_();
  if (mov.length === 0) {
    Logger.log('No hay movimientos registrados.');
    return;
  }

  Logger.log('Revirtiendo ' + mov.length + ' movimientos...');
  var ok = 0, fallo = 0;

  for (var i = mov.length - 1; i >= 0; i--) {
    var m = mov[i];
    try {
      var file = DriveApp.getFileById(m.fileId);
      var origen = _carpetaPorId_(m.carpetaViejaId);
      if (!origen) {
        Logger.log('⚠️  ' + m.nombreViejo + ' <- carpeta origen no existe');
        fallo++;
        continue;
      }

      if (SIMULAR) {
        Logger.log('✓ SIMULAR: devolver ' + m.nombreViejo + ' a ' + origen.getName());
      } else {
        file.moveTo(origen);
        Logger.log('✓ DEVUELTO: ' + m.nombreViejo);
      }
      ok++;
    } catch (e) {
      Logger.log('❌ ' + m.nombreViejo + ': ' + e.toString());
      fallo++;
    }
  }

  Logger.log('');
  Logger.log('Resumen: ' + ok + ' devueltos, ' + fallo + ' fallos');

  if (!SIMULAR && ok > 0) {
    Logger.log('Borrando el registro...');
    _escribir_([]);
  }
}

function olvidarRegistro() {
  PropertiesService.getScriptProperties().deleteProperty(_prop_('MOVIMIENTOS'));
  Logger.log('✓ Registro borrado.');
}

function instalarDisparador() {
  // quitar disparadores anteriores
  var trigs = ScriptApp.getProjectTriggers();
  for (var i = 0; i < trigs.length; i++) {
    if (trigs[i].getHandlerFunction() === 'moverGrabaciones') {
      ScriptApp.deleteTrigger(trigs[i]);
    }
  }

  // instalar uno nuevo
  ScriptApp.newTrigger('moverGrabaciones')
    .timeBased()
    .everyMinutes(30)
    .create();

  Logger.log('✓ Disparador instalado: moverGrabaciones() cada 30 minutos.');
}

function quitarDisparador() {
  var trigs = ScriptApp.getProjectTriggers();
  var borrados = 0;
  for (var i = 0; i < trigs.length; i++) {
    if (trigs[i].getHandlerFunction() === 'moverGrabaciones') {
      ScriptApp.deleteTrigger(trigs[i]);
      borrados++;
    }
  }
  Logger.log('✓ Disparadores quitados: ' + borrados);
}

function reintentarPendientes() {
  Logger.log('reintentarPendientes() no implementado en v2. Ejecuta moverGrabaciones().');
}
""".strip()

# ── el LEEME ───────────────────────────────────────────────────────────
LEEME_CONTENT = """# Mover las grabaciones de Meet (v2) — Guía de uso

**Versión 2 — parametrizable por diccionario**

Este es el Apps Script que mueve automáticamente las grabaciones de Google Meet a las carpetas
de Drive que les corresponden, según el curso.

## Diferencias con la v1

| | v1 | v2 |
|:--|:--|:--|
| **Destinos** | UN destino para todo + subcarpetas por materia | Cada curso va a SU carpeta |
| **Configuración** | Se regenera desde Python cuando cambias un curso | Se edita directo en Apps Script |
| **Número de sesión** | Consulta Calendar para corregirlo | Se queda con el del nombre (congelado por Meet) |
| **Dependencias** | Lee `carga_academica.py` y `sesiones_cun.py` | Solo editas el diccionario del `.gs` |

## Qué hace

1. Cada 30 minutos, lee la carpeta de Meet donde nacen las grabaciones (Meet Recordings).
2. Por cada archivo de grabación:
   - Lee el título y busca qué curso coincide (por fragmento: "Trabajo de grado 3", "Proyecto", etc.).
   - O, si el curso tiene código de Meet configurado, también puede clasificar por sala.
   - Mueve el archivo a la carpeta destino de ese curso.
3. No borra nada, no copia: MUEVE (el enlace que Meet envió por correo sigue funcionando).
4. Si no sabe clasificar algo, lo deja quieto y lo nombra en el registro.

## Pasos de instalación

### 1. Abre Apps Script

Ve a [script.google.com](https://script.google.com) con la cuenta que **organiza las clases**
(las grabaciones nacen en el Mi unidad del organizador).

### 2. Crea un proyecto nuevo

- Nuevo proyecto
- Pega TODO el contenido de `PRINCIPAL - Mover grabaciones de Meet (v2).gs`
- Guarda (le pone nombre automáticamente, o cámbiale el nombre si quieres)

### 3. Edita `CONFIG_CURSOS`

Al principio del archivo hay un diccionario. Por cada curso:

```javascript
{
  tituloContiene: "Trabajo de grado 3",  // <- fragmento del título del evento
  meetLink: "",                           // <- código de meet.google.com/abc-defg-hij, o "" si no aplica
  carpetaDestino: ""                      // <- enlace de la carpeta de Drive (pégalo tal cual)
}
```

**Cómo obtener el enlace de carpetaDestino:**
1. Abre la carpeta en Google Drive donde quieres que vayan las grabaciones de ESE curso
2. Copia el enlace de la barra de direcciones (el que dice `drive.google.com/drive/folders/...`)
3. Pégalo tal cual en `carpetaDestino`

No hace falta sacarle el ID: el script lo extrae solo.

### 4. Pega `ORIGEN_ID`

Es la carpeta donde Meet deja las grabaciones (normalmente se llama "Meet Recordings").

1. Busca esa carpeta en tu Mi unidad de Drive
2. Copia el enlace (igual que arriba)
3. Pégalo en `ORIGEN_ID` (línea ~80)

**Si no la encuentras:** ejecuta `verificarGrabaciones()` (paso 5) con `ORIGEN_ID` vacío, y el
script te SUGIERE candidatos.

### 5. Verifica (solo lectura)

Ejecuta la función `verificarGrabaciones()`:
- Botón ▶️ arriba, elige `verificarGrabaciones`
- La primera vez pedirá permisos (Autorizar → elige tu cuenta → Avanzado → Ir a [nombre del proyecto])
- Lee TODO el registro: te dice qué archivos hay, a qué carpeta iría cada uno, y si falta algo

### 6. Ejecuta una vez a mano

Si el paso anterior cuadra:
1. Cambia `SIMULAR = true` por `SIMULAR = false` (línea ~77)
2. Guarda
3. Ejecuta `moverGrabaciones()` UNA vez a mano
4. Lee el registro: debe decir "✓ MOVIDO:" para cada archivo

### 7. Instala el disparador automático

Ejecuta `instalarDisparador()`:
- Se crea un trigger que corre `moverGrabaciones()` cada 30 minutos
- A partir de ahí es automático: no hace falta que el computador esté encendido

## Funciones disponibles

| Función | Qué hace |
|:--|:--|
| `verificarGrabaciones()` | Solo lectura. Dice qué haría sin mover nada. |
| `moverGrabaciones()` | Mueve las grabaciones (respeta `SIMULAR`). |
| `instalarDisparador()` | Instala el trigger de 30 minutos. |
| `quitarDisparador()` | Quita el trigger (para el automatismo). |
| `revertirMovimientos()` | Devuelve todo a la carpeta origen. |
| `olvidarRegistro()` | Borra el historial de movimientos. |

## Cómo agregar un curso nuevo

1. Abre el proyecto en Apps Script
2. Edita `CONFIG_CURSOS` (línea ~30): agrega una entrada más
3. Guarda
4. Ejecuta `verificarGrabaciones()` para comprobar

**No hace falta regenerar nada**: editas directo en Apps Script.

## Separar grabaciones por periodo académico

Si quieres usar el MISMO script en DOS semestres seguidos (ej: 26ES4 y 27ES4), pero con carpetas
destino diferentes, usa el campo `FECHA_HASTA` en lugar de cambiar CONFIG_CURSOS:

### Ejemplo: Transición de 26ES4 a 27ES4

**Paso 1 - Durante 26ES4:**
```javascript
var FECHA_HASTA = '2026-12-31';  // solo mueve archivos creados en 2026

var CONFIG_CURSOS = [
  {
    tituloContiene: "Trabajo de grado 3",
    carpetaDestino: "https://drive.google.com/drive/folders/1ABC..."  // <- carpeta de 26ES4
  },
  // ... resto de cursos con carpetas de 26ES4
];
```

El script mueve solo las grabaciones creadas ANTES del 2027-01-01, hacia las carpetas de 26ES4.

**Paso 2 - Al iniciar 27ES4:**
1. Cambia las carpetas destino en CONFIG_CURSOS por las de 27ES4
2. Cambia FECHA_HASTA a la nueva fecha límite: `'2027-12-31'`
3. Las grabaciones de 27ES4 (creadas en 2027) van a las carpetas nuevas
4. Las grabaciones viejas de 26ES4 ya están movidas, no las vuelve a tocar

**Alternativa: sin fecha límite**

Si dejas `FECHA_HASTA = ''`, el script mueve TODO sin mirar la fecha de creación (útil cuando
no hay riesgo de mezclar periodos o cuando solo das un curso por año).

## El campo FECHA_HASTA

`FECHA_HASTA` filtra por fecha de creación del archivo en Drive, NO por lo que diga el nombre.

- **Formato:** `'YYYY-MM-DD'` (ej: `'2026-12-31'`)
- **Comportamiento:**
  - Si está configurado: solo mueve archivos creados ANTES de esa fecha (inclusive)
  - Si está vacío (`''`): mueve todo sin filtrar por fecha
- **Se aplica después de MARGEN_MIN:** primero espera 20 minutos, luego verifica la fecha límite
- **Útil para:**
  - Reutilizar el mismo script en varios semestres sin editar CONFIG_CURSOS cada vez
  - Evitar que grabaciones nuevas se muevan a carpetas de semestres viejos
  - Separar periodos académicos sin depender del formato del nombre del archivo

## Cómo cambiar la carpeta destino de un curso

Igual: editas el diccionario, cambias el enlace en `carpetaDestino`, guardas, listo.

## Limitaciones

- **Número de sesión congelado:** Meet congela el título del evento con el que se estrenó la
  sala. Si la segunda clase dice "Sesión 01", el archivo también lo dirá. La v1 corregía esto
  consultando Calendar; la v2 no, porque es más simple y no pide permisos de Calendar.
- **Cuota de Apps Script:** 360 minutos/día de ejecución de triggers. Con 30 min entre pasadas
  y un límite de 4,5 min por pasada, no lo alcanzas.
- **Una cuenta, un organizador:** Si otra persona organiza un Meet, la grabación nace en SU
  Mi unidad, y este script no la ve.

## Dónde están los archivos

- Generador: `config/slides/build_apps_script_grabaciones_v2.py`
- .gs generado: `PRINCIPAL - Mover grabaciones de Meet (v2).gs`
- Este LEEME: `LEEME - Mover las grabaciones de Meet (v2).md`

Regenerar:
```bash
python config/slides/build_apps_script_grabaciones_v2.py
```

## Versión y autoría

**v2 — 26/08/2026**
Parametrizable por diccionario editable en Apps Script. No depende del repositorio CUN.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
""".strip()


def main():
    gs_path = ROOT / GS_NAME
    leeme_path = ROOT / LEEME_NAME

    print(f"Escribiendo {GS_NAME}...")
    gs_path.write_text(GS_CONTENT, encoding="utf-8")

    print(f"Escribiendo {LEEME_NAME}...")
    leeme_path.write_text(LEEME_CONTENT, encoding="utf-8")

    print()
    print(f"OK {GS_NAME}  ({len(GS_CONTENT):,} bytes)")
    print(f"OK {LEEME_NAME}  ({len(LEEME_CONTENT):,} bytes)")
    print()
    print("Próximos pasos:")
    print("1. Abre script.google.com con la cuenta CUN")
    print(f"2. Nuevo proyecto -> pega el contenido de '{GS_NAME}'")
    print("3. Edita CONFIG_CURSOS: por cada curso, el fragmento del título y la carpeta destino")
    print("4. Pega ORIGEN_ID (la carpeta de Meet Recordings)")
    print("5. Ejecuta verificarGrabaciones() -> si cuadra, SIMULAR=false -> moverGrabaciones()")
    print("6. instalarDisparador() -> listo, corre cada 30 minutos")


if __name__ == "__main__":
    main()
