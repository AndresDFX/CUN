# -*- coding: utf-8 -*-
"""Genera el Apps Script que mueve las grabaciones de Meet a la carpeta única de
grabaciones — más su runbook (`LEEME - Mover las grabaciones de Meet.md`).

POR QUÉ EXISTE
    Meet deja las grabaciones en el Drive del ORGANIZADOR, en su carpeta por omisión de Mi
    unidad: hoy «Meet Recordings» (lo reportado por el docente el 2026-08-15). Algunas
    cuentas ven en su lugar una carpeta «Google Meet» con una subcarpeta por reunión, y
    puede que la vieja aparezca dentro como «Legacy Meet Recordings» — PENDIENTE DE
    VERIFICAR en esta cuenta; el .gs contempla los dos nombres y el id lo pega el docente.
    Pero el correo de bienvenida (`build_correo_bienvenida.py`) y el LEEME del estudiante
    (`sync_clases_estudiantes.py`) prometen otra cosa: que TODAS las grabaciones están en
    UNA carpeta —`carga_academica.GRABACIONES_URL`— y que el vídeo se encuentra buscando
    «periodo - grupo - asignatura - sesion». Mover a mano cada semana es lo que el docente
    quiere dejar de hacer, y no hay ajuste de administrador ni paso de Workspace Studio que
    mueva un archivo de Drive: hoy la única vía es un script.

    Apps Script es la vía viable porque corre en los servidores de Google con la sesión del
    dueño del proyecto: SIN credencial guardada. La cuenta @cun.edu.co no puede generar
    contraseñas de aplicación (el administrador lo tiene deshabilitado), y la política ya
    escrita del repositorio es «Flujo preferido sin OAuth: Apps Script»
    (`config/slides/_secrets/README.md`).

UN PERFIL POR INSTITUCIÓN
    Todo lo que es de la CUN —zona horaria, desfase UTC, marca de sesión, patrón del asunto,
    nombres de carpeta de origen, calendario, salas y los enlaces de las carpetas de Drive—
    vive en `PERFILES`, un `Perfil` por institución. El perfil por omisión es `CUN`, así que
    la invocación de siempre (sin argumentos) sigue escribiendo exactamente lo de siempre;
    otra institución se añade copiando la entrada `PLANTILLA` y no se toca ni una línea del
    cuerpo JS. Lo que NO se puede parametrizar está documentado en el propio .gs y en el
    runbook («Lo que NO se puede parametrizar»): la clasificación por Calendar exige que los
    encuentros existan y se titulen de forma reconocible, un solo desfase no cubre el horario
    de verano, y los topes son cuota de Apps Script.

LOS ENLACES DE CARPETA SE PEGAN TAL CUAL
    Ni el perfil ni el docente tienen que extraer el id de la URL de Drive: las tres
    constantes de carpeta del .gs (ORIGEN_ID, ORIGEN_LEGACY_ID, DESTINO_ID) aceptan el enlace
    completo —`/folders/…`, `/drive/u/0/folders/…`, con `?usp=sharing`, `open?id=…`— o el id
    pelado, y `_idDeCarpeta_()` normaliza al cargar el archivo. Si lo pegado es el enlace de
    un ARCHIVO (lleva `/d/`) se dice con esas palabras en el registro y esa constante queda
    vacía: el script avisa y no mueve. La misma comprobación se hace en el build
    (`id_de_carpeta()`) para que un perfil mal pegado falle al regenerar, no en Apps Script.

QUÉ SE INYECTA Y DE DÓNDE (nada se escribe a mano en el .gs)
    DESTINO_ID  <- el enlace de `Perfil.destino_url` (para la CUN,
                   `carga_academica.GRABACIONES_URL`), pegado tal cual.
    SALAS       <- `cursos.<key>.meet` de `carga_academica_2026.json`, solo las reales.
                   Hoy únicamente `proyecto1`; los otros cuatro están en `""` y por eso no
                   aparecen. En cuanto se peguen, se regenera y el .gs los usa.
    HORARIOS    <- `cursos.<key>.horario` (comentario del .gs, para leer el log a ojo).
    ORIGEN_ID   <- NO EXISTE en el repositorio y no se puede deducir: es el id de la
                   carpeta por omisión de Meet en el Mi unidad del docente. Se emite VACÍO
                   y el script se niega a mover mientras lo esté, sugiriendo candidatos por
                   nombre.

UNA SOLA COPIA, EN LA RAÍZ
    A diferencia de `build_calendar_encuentros.py` (un .gs por grupo), aquí hay un único
    proyecto de Apps Script instalado una vez y transversal a los 5 cursos: el .gs y su
    runbook van a la raíz de `Cursos/`, donde ya viven los entregables transversales
    (`LEEME - Mapa de cursos y manuales.md`, `ALISTAMIENTO CDigital ….md`).

Uso:
  python config/slides/build_apps_script_grabaciones.py            # perfil CUN
  python config/slides/build_apps_script_grabaciones.py PLANTILLA  # otra institución
  python config/slides/build_apps_script_grabaciones.py --perfiles # los que hay
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))

from sesiones_cun import (  # noqa: E402
    COURSES,
    DOCENTE_CORREO,
    meet_url,
    titulo_para_calendar,
)
from carga_academica import (  # noqa: E402
    GRABACIONES_URL,
    curso as carga_curso,
    workspace_root,
)

# Nombre base de los dos entregables. El perfil por omisión (CUN) no lleva sufijo, así que
# sigue escribiendo EXACTAMENTE los dos archivos de siempre; cualquier otro perfil añade
# « (CLAVE)» para no pisárselos.
GS_BASE = "PRINCIPAL - Mover grabaciones de Meet"
LEEME_BASE = "LEEME - Mover las grabaciones de Meet"
GS_NAME = f"{GS_BASE}.gs"
LEEME_NAME = f"{LEEME_BASE}.md"
# Nombres que usaron versiones anteriores de este build; se borran al regenerar para que no
# queden dos .gs con el mismo contenido y distinto nombre en la carpeta del docente. SOLO se
# borran cuando se genera el perfil por omisión: los archivos de otro perfil no son basura.
GS_LEGACY = ("Mover grabaciones de Meet.gs",)

CURSOS_CUN = ("proyecto1", "creatividad", "investigacion", "tg2", "tg3")
DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")

# everyMinutes() solo admite 1, 5, 10, 15 o 30. 30 y no 15 por la cuota REAL: Workspace da
# 360 min/día de disparadores y cada pasada se permite hasta LIMITE_MS (4,5 min), así que 96
# pasadas/día podrían pedir 432 min y Google cortaría el resto del día.
CADA_MIN = 30
MARGEN_MIN = 20    # gracia antes de tocar un archivo recién aparecido
VENTANA_MIN = 30   # ±minutos con los que se consulta el Calendar alrededor de la hora
TOL_INICIO_MIN = 15  # cuánto antes del inicio del encuentro se admite la marca de tiempo
HORAS_ATRAS_APROX = 6  # sin hora en el nombre: se mira hacia ATRÁS desde la creación

# Fecha y hora que Meet estampa en el nombre del archivo. NO es institucional: es la
# convención de Meet, la misma en cualquier universidad, y no está documentada por Google
# (ya cambió una vez sin avisar). Por eso vive FUERA de los perfiles: una sola definición
# para todos, o cada perfil arrastraría su propia copia desfasada.
# Corregida el 25/08/2026 contra los nombres REALES de la cuenta. Meet dejó de escribir los
# separadores: hoy pone «2026 08 13 17 00 GMT-05 00», con espacios y sin dos puntos, y la fecha ya
# no va entre paréntesis sino como un tramo más del nombre. La versión anterior exigía
# «2026-08-13 17:00 GMT-05:00» y por eso NO cazaba ni uno: medido, 0 de 19 archivos. El efecto no
# era un movimiento erróneo —sin fecha, el script cae al respaldo aproximado por ventana— pero sí
# renunciaba a la señal más fiable que hay en el nombre.
# Ahora acepta los dos formatos: separador «-», «_» o espacio en la fecha y en la hora, y «GMT-05»
# con o sin espacio detrás. Comprobado: 7 de 7 sobre nombres reales y sobre los del formato viejo.
RX_FECHA_MEET = r"(\d{4})[-_ ](\d{2})[-_ ](\d{2})[ _T]+(\d{2})[:._h ](\d{2})(?:[^)]*?GMT\s*([+-]\d{2}))?"


# ── perfiles por institución ─────────────────────────────────────────────────
@dataclass(frozen=True)
class Perfil:
    """Todo lo que cambia de una institución a otra, en un solo sitio.

    Lo que NO está aquí es deliberado: los topes de cuota de Apps Script, el MIME de los
    atajos y `RX_FECHA_MEET` los decide Google, no la institución. Los límites honestos se
    escriben en los dos entregables: el bloque «LO QUE ES DEL PERFIL … Y NO ES UNIVERSAL» del
    .gs y la sección «Lo que NO se puede parametrizar» del runbook.
    """

    clave: str
    institucion: str            # nombre corto; sale en el .gs y en el runbook
    timezone: str               # Utilities.parseDate / formatDate del .gs
    desfase_esperado: str       # el «GMT-05» que Meet escribe en el nombre
    desfase_nota: str           # de dónde sale ese desfase, para el comentario del .gs
    marca: str                  # fragmento que identifica un encuentro en el título del evento
    rx_subject: str             # fuente JS de la expresión regular, SIN las barras
    rx_subject_forma: str       # la misma regla en palabras, para el comentario
    rx_subject_ejemplos: tuple[str, ...]
    nombres_origen: tuple[str, ...]   # solo para SUGERIR candidatos a ORIGEN_ID
    nombres_legacy: tuple[str, ...]
    calendario_id: str
    destino_url: str            # ENLACE de Drive pegado tal cual (o id pelado)
    origen_url: str = ""        # vacío = lo pega el docente en el .gs
    origen_legacy_url: str = ""
    docente_correo: str = ""
    proyecto_sugerido: str = "Grabaciones"   # nombre sugerido del proyecto de Apps Script
    prop_prefijo: str = "GRABACIONES"        # prefijo de las claves de ScriptProperties
    sufijo: str = ""            # sufijo de los nombres de archivo («» = los de siempre)
    cursos: tuple[str, ...] = ()             # claves de carga_academica_2026.json, si aplica
    salas: dict[str, str] = field(default_factory=dict)  # se rellena del JSON si `cursos`
    nota_series: str = ""       # aviso sobre qué series de encuentros existen ya
    resumen_aulas: str = "1 sola carpeta destino"
    usa_repositorio_cun: bool = False   # si el runbook puede citar rutas de este repositorio

    @property
    def gs_name(self) -> str:
        return f"{GS_BASE}{self.sufijo}.gs"

    @property
    def leeme_name(self) -> str:
        return f"{LEEME_BASE}{self.sufijo}.md"

    def prop(self, cola: str) -> str:
        return f"{self.prop_prefijo}_{cola}"


PERFIL_POR_OMISION = "CUN"

PERFILES: dict[str, Perfil] = {
    # ── CUN — el perfil real, y el que sale sin argumentos ───────────────────
    "CUN": Perfil(
        clave="CUN",
        institucion="CUN",
        timezone="America/Bogota",
        desfase_esperado="-05",
        desfase_nota="Bogotá",
        marca=" - Sesion ",
        # «periodo - grupo(s) - Asignatura - Sesion NN», lo que arma
        # `sesiones_cun.subject_encuentro()`. Periodo = 2 dígitos + 1-2 letras + 1-2 dígitos;
        # grupo = 5 alfanuméricos; varios de cada cosa se unen con «/».
        rx_subject=(
            r"\d{2}[A-Z]{1,2}\d{1,2}(?:\/\d{2}[A-Z]{1,2}\d{1,2})*"
            r" - [0-9A-Z]{5}(?:\/[0-9A-Z]{5})*"
            r" - [^()]{3,60}? - Sesion \d{1,2}(?: \(autónoma\))?"
        ),
        rx_subject_forma="«periodo - grupo(s) - Asignatura - Sesion NN»   (sesiones_cun.subject_encuentro)",
        rx_subject_ejemplos=(
            "26ES4 - 54ES4 - Proyecto I - Sesion 01",
            "26P04/26V04 - 54450/54466/54467 - Trabajo de Grado 3 - Sesion 01",
        ),
        nombres_origen=("Meet Recordings", "Google Meet"),
        nombres_legacy=("Legacy Meet Recordings",),
        calendario_id="primary",
        destino_url=GRABACIONES_URL,
        docente_correo=DOCENTE_CORREO,
        proyecto_sugerido="CUN - Grabaciones",
        cursos=CURSOS_CUN,
        nota_series="Hoy solo Proyecto I tiene serie y sala creadas.",
        resumen_aulas="5 asignaturas · 7 aulas · 1 sola carpeta destino",
        usa_repositorio_cun=True,
    ),
    # ── PLANTILLA — para otra universidad. Copia esta entrada, ponle la clave de
    # tu institución y cambia lo de dentro. Todo lo que aquí está en mayúsculas o
    # vacío es lo que hay que rellenar; los enlaces de Drive se pegan TAL CUAL, no
    # hace falta sacarles el id (lo hace el propio .gs).
    "PLANTILLA": Perfil(
        clave="PLANTILLA",
        institucion="INSTITUCIÓN",
        timezone="America/Bogota",
        desfase_esperado="-05",
        desfase_nota="RELLENA con el desfase de tu huso (ojo si tu país cambia la hora "
                     "en verano: ver los límites)",
        marca=" - Sesion ",
        rx_subject=r"[^()]{3,60}? - Sesion \d{1,2}",
        rx_subject_forma="«Asignatura - Sesion NN» (RELLENA esto con tu nomenclatura)",
        rx_subject_ejemplos=("Asignatura de ejemplo - Sesion 01",),
        nombres_origen=("Meet Recordings", "Google Meet"),
        nombres_legacy=("Legacy Meet Recordings",),
        calendario_id="primary",
        destino_url="",   # pega aquí el enlace de la carpeta destino, entero
        docente_correo="tu.correo@ejemplo.edu",
        proyecto_sugerido="Grabaciones",
        prop_prefijo="GRABACIONES_PLANTILLA",
        sufijo=" (PLANTILLA)",
        salas={},         # {'abc-defg-hij': 'Nombre de la asignatura en el título del evento'}
        nota_series="Crea antes la serie de encuentros de cada asignatura en el Calendar.",
    ),
}


def perfil(clave: str | None = None) -> Perfil:
    """El perfil pedido. Sin argumento, el de la CUN: la invocación de siempre no cambia."""
    c = (clave or PERFIL_POR_OMISION).strip()
    if c in PERFILES:
        return PERFILES[c]
    for k in PERFILES:
        if k.lower() == c.lower():
            return PERFILES[k]
    raise SystemExit(
        f"No existe el perfil «{c}». Perfiles disponibles: "
        + ", ".join(sorted(PERFILES))
        + f"  (sin argumento se usa {PERFIL_POR_OMISION})"
    )


# ── emisión del .gs ──────────────────────────────────────────────────────────
def _js(s: str) -> str:
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"


RX_ID_DRIVE = re.compile(r"^[A-Za-z0-9_-]{11,}$")


def id_de_carpeta(valor: str, etiqueta: str) -> str:
    """Id de carpeta de Drive a partir del ENLACE pegado tal cual (o del id pelado).

    Misma lógica que `_idDeCarpeta_()` del .gs, aquí para fallar en el build y no en Apps
    Script: si un perfil trae un enlace que no es de carpeta, se dice al regenerar. Cadena
    vacía = «lo pega el docente», que es legítimo para el origen.
    """
    s = (valor or "").strip().strip("<>\"'")
    if not s:
        return ""
    if s.startswith("http") or "google.com" in s:
        m = re.search(r"/folders/([^/?#]+)", s)
        if m:
            s = m.group(1)
        elif re.search(r"/(?:file|document|spreadsheets|presentation|forms)/d/", s):
            raise SystemExit(
                f"{etiqueta}: ese enlace es de un ARCHIVO, no de una carpeta (lleva «/d/»). "
                f"Pega el enlace de la CARPETA, el que lleva «/folders/»: {valor}"
            )
        else:
            m = re.search(r"[?&]id=([^&#]+)", s)
            if not m:
                raise SystemExit(
                    f"{etiqueta}: no reconozco esa URL de Drive. Pega el enlace de la carpeta "
                    f"(lleva «/folders/») o el id pelado: {valor}"
                )
            s = m.group(1)
    if not RX_ID_DRIVE.match(s):
        raise SystemExit(
            f"{etiqueta}: «{s}» no tiene forma de id de carpeta de Drive "
            f"(letras, dígitos, «-» y «_»). Valor pegado: {valor}"
        )
    return s


def destino_id(p: Perfil) -> str:
    """Id de la carpeta única de grabaciones — para citarlo en el runbook y en la traza.

    En el .gs ya NO se emite el id pelado: se emite el enlace del perfil tal cual y el propio
    script extrae el id. Esto es la misma cuenta hecha en el build, para poder validarla y
    escribirla en el LEEME.
    """
    return id_de_carpeta(p.destino_url, f"perfil {p.clave}: destino_url")


def salas_del_perfil(p: Perfil) -> dict[str, str]:
    """`{código de sala: fragmento del título del evento}`.

    El valor es el nombre de asignatura tal como aparece en el Subject de los encuentros
    (`sesiones_cun.titulo_para_calendar`), porque de eso sirve: desempatar contra los
    títulos reales del Calendar. Los cursos con `meet` vacío quedan fuera a propósito —
    inventarles un código sería exactamente lo prohibido.

    Con `cursos` (perfil respaldado por `carga_academica_2026.json`) se deriva del JSON; sin
    `cursos`, se usan las salas que el perfil declare a mano.
    """
    if not p.cursos:
        return dict(p.salas)
    out: dict[str, str] = {}
    for k in p.cursos:
        url = meet_url(k)
        if not url.startswith("https://meet.google.com/"):
            continue
        codigo = url.replace("https://meet.google.com/", "").strip().strip("/")
        if codigo:
            out[codigo] = titulo_para_calendar(k)
    return out


def sin_sala(p: Perfil) -> list[str]:
    """Cursos del perfil que todavía no tienen sala de Meet en config."""
    if not p.cursos:
        return []
    return [k for k in p.cursos if not meet_url(k).startswith("https://meet.google.com/")]


def _horario(key: str) -> tuple[str, str, str]:
    """('lunes', '17:00', '18:00') del curso, desde `carga_academica_2026.json`."""
    h = carga_curso(key)["horario"]
    ics = h["hora_ics"]
    return (
        DIAS[int(h["weekday"])],
        f"{ics[0][:2]}:{ics[0][2:4]}",
        f"{ics[1][:2]}:{ics[1][2:4]}",
    )


def _tabla_horarios_js(p: Perfil) -> str:
    """Comentario con la tabla día+hora -> curso. NO es código: es para leer el log a ojo."""
    if not p.cursos:
        return ("//   (este perfil no declara cursos: la tabla de horarios se omite. El "
                "criterio real\n//    es el Calendar, no esta tabla.)")
    filas = []
    for k in p.cursos:
        dia, ini, fin = _horario(k)
        grupos = "/".join(carga_curso(k)["groups"])
        filas.append(
            f"//   {dia:<10} {ini}–{fin}  ->  {titulo_para_calendar(k)} · {grupos}"
        )
    return "\n".join(filas)


def _salas_js(p: Perfil, sal: dict[str, str]) -> str:
    if not sal:
        donde = ("cursos.<key>.meet está vacío" if p.cursos
                 else f"PERFILES[{p.clave!r}].salas está vacío")
        return f"var SALAS = {{}};  // ninguna sala en config todavía: {donde}"
    cuerpo = ",\n".join(f"  {_js(c)}: {_js(t)}" for c, t in sorted(sal.items()))
    return "var SALAS = {\n" + cuerpo + "\n};"


# Normalización de los enlaces de carpeta, en el propio .gs: las tres constantes de arriba
# admiten la URL de Drive pegada tal cual O el id pelado. Se hace aquí y no en el generador
# porque ORIGEN_ID lo pega el docente a mano en Apps Script, y sacar el id de la URL es
# justo el paso donde se cuelan los errores tontos. Fuera de la f-string, como el cuerpo.
GS_ENLACES = r"""
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
"""

# Cuerpo JS invariable del script: todo lo que cambia (destino, salas, horarios) viaja en
# las constantes que emite `_gs_texto`. Se mantiene FUERA de la f-string a propósito —
# doblar un centenar de llaves de JavaScript para meterlas en una f-string es exactamente
# de donde salen los errores tontos.
GS_FUNCIONES = r"""
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
               '@@FUENTE_DESTINO@@');
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
  // DESMIENTE: @@VETO_CUERPO@@
  // ese encuentro en la agenda. Puede venir en el nombre del archivo o en el de la subcarpeta
  // de la reunión.
  var pista = _asignaturaDeSala_(nombre) || _asignaturaDeSala_(it.carpeta.getName());

  // Criterio 2 — cruce por fecha y hora contra los eventos REALES del Calendar, que es la
  // @@AUTORIDAD_CUERPO@@
  var fecha = _fechaDelNombre_(nombre);
  var aprox = !fecha;
  if (!fecha) {
    // Sin hora en el nombre (o con un desfase que no es el de @@SITIO_DESFASE@@): lo único que queda es
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
 * Canónico = @@FORMA_SUBJECT@@
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
 * no está. Se interpreta en TIMEZONE; si el nombre trae un desfase que NO es el de @@SITIO_DESFASE@@,
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
             '@@CREA_SERIE@@, o lo que hay en la ' +
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
"""


def _cuerpo_js(p: Perfil) -> str:
    """`GS_FUNCIONES` con los tres textos que dependen de la institución rellenados.

    El cuerpo JS es fijo a propósito (925 líneas que no se tocan), pero tres de sus cadenas
    SÍ son de la institución: dos salen en el registro de ejecución —y mandaban al operador
    de otra universidad a ficheros de este repositorio— y la tercera es el docblock que
    describe la nomenclatura, que contradecía a `RX_SUBJECT` en cualquier perfil que no fuera
    el de la CUN. Para el perfil CUN los tres se sustituyen por el texto literal de antes.
    """
    if p.usa_repositorio_cun:
        fuente_destino = "config/cursos/carga_academica.py -> GRABACIONES_URL."
        crea_serie = "«PRINCIPAL - Crear encuentros con invitados.gs» del curso)"
    else:
        fuente_destino = (
            f"PERFILES -> {p.clave} -> destino_url, en el generador."
        )
        crea_serie = "quien monte la serie de encuentros en tu institución)"
    # Colapsar los espacios de alineación reproduce el literal de antes para la CUN.
    forma = re.sub(r"\s{2,}", " ", p.rx_subject_forma) + "."
    # Para la CUN, `desfase_nota` es justo «Bogotá», que es lo que decía el comentario a mano.
    sitio = p.desfase_nota if p.usa_repositorio_cun else "DESFASE_ESPERADO"
    if p.usa_repositorio_cun:
        veto_cuerpo = (
            "si la sala es la de Proyecto I, el archivo no es de TG3 por muy solo que esté"
        )
        autoridad_cuerpo = (
            "autoridad de nombres: los creó «PRINCIPAL - Crear encuentros con invitados.gs» y ya\n"
            "  // contienen las excepciones (TG2 dictó la Sesión 01 el VIERNES 14/08/2026, reprogramada\n"
            "  // desde el lunes 10/08). Una tabla de horarios horneada aquí la habría perdido."
        )
    else:
        veto_cuerpo = (
            "si la sala es la de otra asignatura, el archivo no es de esta por muy solo que esté"
        )
        autoridad_cuerpo = (
            "autoridad de nombres, y ya contiene las excepciones: una clase reprogramada a otro\n"
            "  // día tiene su evento en el día real en que se dio. Una tabla de horarios horneada\n"
            "  // aquí la habría perdido."
        )
    return (
        GS_FUNCIONES
        .replace("@@FUENTE_DESTINO@@", fuente_destino)
        .replace("@@CREA_SERIE@@", crea_serie)
        .replace("@@FORMA_SUBJECT@@", forma)
        .replace("@@SITIO_DESFASE@@", sitio)
        .replace("@@VETO_CUERPO@@", veto_cuerpo)
        .replace("@@AUTORIDAD_CUERPO@@", autoridad_cuerpo)
    )


def _gs_texto(p: Perfil, sal: dict[str, str]) -> str:
    salas_js = _salas_js(p, sal)
    faltan = sin_sala(p)
    nota_salas = (
        "// PENDIENTE: siguen sin sala en el JSON " + ", ".join(faltan) + " -> cuando el .gs de\n"
        "// encuentros las cree y las pegues en cursos.<key>.meet, regenera este archivo.\n"
        if faltan else ""
    )
    ejemplos_subject = "\n".join("//   " + e for e in p.rx_subject_ejemplos)
    # El ejemplo del veto por sala nombra asignaturas: para la CUN son las suyas, para
    # cualquier otro perfil se dice en abstracto. Lleva el salto de línea dentro porque va
    # dentro de un comentario ya partido a 90 columnas.
    # La promesa que este script cumple. Para la CUN son dos documentos concretos suyos; para
    # otro perfil, la misma idea sin citarlos. Lleva los saltos de línea dentro porque va
    # dentro del docblock de cabecera, ya partido a 90 columnas.
    promesa = (
        "El correo de bienvenida y\n"
        " * el «LEEME - Material para estudiantes» prometen otra cosa: que TODAS las "
        "grabaciones están\n"
        " * en UNA carpeta y que el vídeo se encuentra buscando "
        "«periodo - grupo - asignatura - sesion»."
        if p.usa_repositorio_cun else
        "Lo que se le ha prometido al estudiante es\n"
        " * otra cosa: que TODAS las grabaciones están en UNA carpeta y que el vídeo se "
        "encuentra\n"
        " * buscando por el título del encuentro."
    )
    # La CUN no lleva comentario en TIMEZONE (y así se queda). Cualquier otro perfil sí: es
    # de las primeras cosas que hay que revisar al copiar la PLANTILLA.
    nota_tz = "" if p.usa_repositorio_cun else (
        "// Zona horaria (IANA) con la que se leen las horas del Calendar y las del nombre del\n"
        "// archivo. Sale del perfil: compruébala antes de nada si copiaste la PLANTILLA.\n"
    )
    if p.usa_repositorio_cun:
        quien_crea = "los crea «PRINCIPAL - Crear encuentros con invitados.gs» de cada curso"
        autoridad_cal = (
            "los eventos los creó\n"
            "// «PRINCIPAL - Crear encuentros con invitados.gs», así que al abrir el semestre siguiente"
        )
    else:
        quien_crea = "los creas tú en ese calendario, con MARCA en el título"
        autoridad_cal = (
            "los títulos de los eventos son\n"
            "// los que manda RX_SUBJECT, así que al abrir el semestre siguiente"
        )
    veto_ejemplo = (
        "si\n// la sala dice «Proyecto I» y el único encuentro de esa hora es de TG3, no se "
        "mueve. Una sala"
        if p.usa_repositorio_cun else
        "si la\n// sala dice una asignatura y el único encuentro de esa hora es de otra, no se "
        "mueve. Una sala"
    )
    nombres_origen = ", ".join(_js(n) for n in p.nombres_origen)
    nombres_legacy = ", ".join(_js(n) for n in p.nombres_legacy)
    if p.usa_repositorio_cun:
        nota_destino = (
            "// DESTINO — la carpeta ÚNICA de grabaciones: la misma para los 5 cursos y para todos los\n"
            "// periodos, plana y sin subcarpetas. Fuente única: config/cursos/carga_academica.py ->\n"
            "// GRABACIONES_URL (y la nota normativa de carga_academica_2026.json). Esta URL ya está\n"
            "// impresa en el correo de bienvenida y en el LEEME del estudiante: no la cambies aquí."
        )
        fuente_salas = (
            "// Fuente: carga_academica_2026.json -> cursos.<key>.meet (solo las salas REALES)."
        )
        nota_tabla = (
            "// Tabla día+hora -> curso. NO se usa como criterio (el Calendar ya la contiene, y además\n"
            "// contempla las reprogramaciones: TG2 dictó la Sesión 01 el viernes 14/08/2026). Está aquí\n"
            "// para leer el registro a ojo:"
        )
    else:
        nota_destino = (
            "// DESTINO — la carpeta ÚNICA de grabaciones: la misma para todos los cursos y todos los\n"
            f"// periodos, plana y sin subcarpetas. La declara el perfil {p.clave} en PERFILES, dentro de\n"
            "// config/slides/build_apps_script_grabaciones.py. Si ya está publicada a los estudiantes,\n"
            "// no la cambies aquí: cámbiala en el perfil y regenera."
        )
        fuente_salas = f"// Fuente: PERFILES[{p.clave!r}].salas del generador."
        nota_tabla = (
            "// Tabla día+hora -> curso. NO se usa como criterio (el Calendar ya la contiene, con sus\n"
            "// reprogramaciones). Está aquí para leer el registro a ojo:"
        )
    cabecera = f"""/**
 * GRABACIONES DE MEET — Mover cada grabación a la carpeta ÚNICA de grabaciones.
 *
 * Meet deja las grabaciones en el Drive del ORGANIZADOR, en su carpeta por omisión de Mi
 * unidad: hoy «Meet Recordings». Algunas cuentas ven en su lugar una carpeta «Google Meet»
 * con una subcarpeta por reunión (y la vieja dentro, como «Legacy Meet Recordings») — mira
 * cuál tienes tú y pega ESE id. {promesa}
 * Este script cumple esa promesa cada {CADA_MIN} minutos y SIN NINGUNA CREDENCIAL: Apps Script
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
 * PASOS  (detalle completo en «{p.leeme_name}», misma carpeta)
 * 0. REQUISITO PREVIO: los encuentros de la asignatura tienen que EXISTIR en tu Calendar
 *    ({quien_crea}). Sin ellos,
 *    una grabación que no traiga el nombre del evento no se puede clasificar y se queda
 *    quieta. {p.nota_series}
 * 1. https://script.google.com con la cuenta {p.institucion} ({p.docente_correo}) — TIENE que ser la del
 *    organizador de las clases: las grabaciones nacen en SU Mi unidad.
 * 2. Nuevo proyecto -> pega TODO este archivo -> guarda.
 * 3. Pega en ORIGEN_ID el ENLACE de la carpeta de Meet de Mi unidad, tal cual, el de la
 *    barra de direcciones (también vale el id pelado: el script entiende las dos formas).
 *    Es el ÚNICO dato que falta.
 * 4. Ejecuta `verificarGrabaciones()` (SOLO LECTURA) y lee el registro entero.
 * 5. Si cuadra: pon SIMULAR = false, guarda y ejecuta `moverGrabaciones()` UNA vez a mano.
 * 6. `instalarDisparador()` -> a partir de ahí corre solo cada {CADA_MIN} minutos.
 *
 * Deshacer: `revertirMovimientos()` (devuelve carpeta y nombre) · `quitarDisparador()`
 *           (para el automatismo) · `olvidarRegistro()` (suelta el historial de deshacer) ·
 *           `reintentarPendientes()` (vuelve a mirar lo descartado y lo que falló al mover).
 *
 * LO QUE ES DEL PERFIL {p.clave} Y NO ES UNIVERSAL  (los perfiles viven en el generador)
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
 * Regenerar este .gs: python config/slides/build_apps_script_grabaciones.py {p.clave}
 */

// ───────────────────────────── CONFIGURACIÓN ─────────────────────────────────

// MODO SIMULACIÓN, y por omisión ENCENDIDO: la regla de esta casa es simular primero. Con
// true nada escribe —ni moverGrabaciones(), ni el disparador, ni revertirMovimientos()—:
// solo dicen qué harían. Ponlo en false cuando verificarGrabaciones() te cuadre.
var SIMULAR = true;

{nota_tz}var TIMEZONE = {_js(p.timezone)};

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
var ORIGEN_ID = {_js(p.origen_url)};

// «Legacy Meet Recordings» — la carpeta de grabaciones antiguas que algunas cuentas tienen
// DENTRO de «Google Meet». VACÍO A PROPÓSITO: así el primer despliegue NO arrastra de golpe
// periodos viejos (con nombres que quizá no son canónicos) a la carpeta publicada. Ponlo solo
// el día que quieras barrer también lo antiguo, y ejecuta verificarGrabaciones() ANTES para
// ver la lista completa. Si tu origen es «Meet Recordings» (plana), esto no aplica.
var ORIGEN_LEGACY_ID = {_js(p.origen_legacy_url)};

{nota_destino}
// Va el ENLACE tal cual, como lo copia Drive (el id pelado también vale).
var DESTINO_ID = {_js(p.destino_url)};

// Calendario donde están los encuentros. Es la AUTORIDAD de nombres: {autoridad_cal}
// esto sigue funcionando sin tocar el script. 'primary' = el principal de la cuenta.
var CALENDARIO_ID = {_js(p.calendario_id)};

// Cada cuántos minutos barre el disparador. everyMinutes() solo admite 1, 5, 10, 15 o 30, y
// Apps Script programa con ventanas de ±15 min: no dependas del minuto exacto. 30 y no 15
// por la cuota: Workspace da 360 min/día de disparadores y esta función se permite hasta
// LIMITE_MS (4,5 min) por pasada -> 48 x 4,5 = 216 min caben; 96 x 4,5 = 432 no.
var CADA_MIN = {CADA_MIN};

// Gracia antes de tocar un archivo recién aparecido, para no llevarse el vídeo dejando atrás
// la transcripción y las notas. HEURÍSTICA, no garantía: Google no expone a DriveApp ninguna
// señal de «ya está completo». Lo que de verdad cubre el caso es reincidir cada CADA_MIN.
var MARGEN_MIN = {MARGEN_MIN};

// Ventana con la que se CONSULTA el Calendar alrededor de la hora del archivo. Encontrar un
// evento en esa ventana no basta: después se exige que la marca de tiempo caiga DENTRO del
// encuentro (ver TOL_INICIO_MIN), porque getEvents() devuelve todo lo que roce el intervalo y
// una tutoría de las 19:40 rozaría la clase de las 20:00.
var VENTANA_MIN = {VENTANA_MIN};

// Cuánto ANTES del inicio del encuentro se admite la marca de tiempo del nombre (Meet estampa
// la hora en que empezó la reunión, y a veces se entra unos minutos antes). Después del FINAL
// no se admite nada: una reunión que empieza cuando la clase ya acabó no es la clase.
var TOL_INICIO_MIN = {TOL_INICIO_MIN};

// Sin hora en el nombre solo queda la fecha de CREACIÓN del archivo, que es POSTERIOR a la
// clase. Así que se mira hacia ATRÁS estas horas y solo valen encuentros ya TERMINADOS: el
// vídeo de la clase del lunes 20:00–22:00 que aparece a las 00:20 del martes pertenece al
// lunes, no al martes. Nunca se mira «el día natural del archivo».
var HORAS_ATRAS_APROX = {HORAS_ATRAS_APROX};

// Fragmento que identifica a un encuentro en el título del evento. Se busca CONTENIDO, no
// prefijo (mismo criterio que MARCA en «Actualizar Meet en encuentros (mismo enlace).gs»).
var MARCA = {_js(p.marca)};

// Subject canónico dentro del nombre del archivo:
//   {p.rx_subject_forma}
{ejemplos_subject}
// Sin anclas: Meet añade « (2026-08-11 17:00 GMT-05:00)» al final y puede añadir cosas
// delante (los artefactos llevan sufijos tipo «- Transcript»).
var RX_SUBJECT = /{p.rx_subject}/;

// Fecha y hora que Meet escribe en el nombre: « (2026-08-11 17:00 GMT-05:00)».
var RX_FECHA = /{RX_FECHA_MEET}/;
var DESFASE_ESPERADO = {_js(p.desfase_esperado)};   // {p.desfase_nota}. Otro desfase -> la hora del nombre no se usa.

// Código de sala de Meet -> asignatura tal como aparece en el título del evento. Sirve para
// desempatar cuando la ventana de tiempo da más de un candidato Y, sobre todo, para VETAR: {veto_ejemplo}
// reconocida no clasifica por sí sola (no dice de qué sesión es), pero sí desmiente.
{fuente_salas}
{nota_salas}{salas_js}

{nota_tabla}
{_tabla_horarios_js(p)}

// Nombres con los que buscar candidatos a ORIGEN_ID. SOLO para SUGERIR en el registro: el
// script nunca elige «la primera que aparezca». Son los nombres que documenta Google en
// inglés; si tu Drive los muestra traducidos no aparecerá ninguno, y entonces el enlace se
// copia a mano de Drive (que es lo que hay que hacer de todas formas).
var NOMBRES_ORIGEN = [{nombres_origen}];
var NOMBRES_LEGACY = [{nombres_legacy}];

var MIME_ATAJO = 'application/vnd.google-apps.shortcut';

// Registro de lo movido — existe SOLO para deshacer, no para saber qué falta (eso lo dice el
// propio origen). Misma convención que PROP_MEET en los .gs de Calendar.
var PROP_MOVIDOS = {_js(p.prop('MOVIDAS'))};
var MAX_REGISTRO = 150;          // entradas
var MAX_REGISTRO_BYTES = 8000;   // una propiedad de script no admite más de 9 KB

// Archivos que ya se miraron y NO se pudieron clasificar (tutorías, jurados, reuniones
// ajenas). Por «Google Meet» no sale nunca nada de eso, así que sin memoria el residuo se
// vuelve a mirar en cada pasada, se come el cupo de MAX_ARCHIVOS y acaba tapando la clase de
// ayer. Se apuntan con la fecha en que se descartaron y se reintentan cada REINTENTO_H horas
// (por si aparece el encuentro en el Calendar o se pega la sala que faltaba).
var PROP_DESCARTADAS = {_js(p.prop('DESCARTADAS'))};
var MAX_DESCARTADAS = 120;
var REINTENTO_H = 24;

// Archivos cuyo movimiento FALLÓ (Drive deja un atajo en el destino y el original donde
// estaba). Sin memoria, cada pasada crearía un atajo nuevo en la carpeta que ven los
// estudiantes. Al primer fallo se apunta; a partir del segundo intento no se vuelve a tocar
// hasta que lo desbloquees con reintentarPendientes().
var PROP_FALLIDAS = {_js(p.prop('FALLIDAS'))};

// Tope de archivos que se CLASIFICAN por pasada (cada uno puede costar una consulta al
// Calendar) y de archivos cuyos metadatos se leen al barrer. Se ordena de más nuevo a más
// viejo antes de recortar, para que una grabación reciente no quede detrás del residuo.
var MAX_ARCHIVOS = 40;
var MAX_EXAMINADOS = 400;
var MAX_PROFUNDIDAD = 4;   // raíz de Meet / subcarpeta de la reunión / ... y para de contar
var LIMITE_MS = 270000;    // 4,5 min de los 6 que da Apps Script por ejecución
"""
    return cabecera + GS_ENLACES + _cuerpo_js(p)


# ── runbook ──────────────────────────────────────────────────────────────────
def _leeme_texto(p: Perfil, sal: dict[str, str], dest: str) -> str:
    faltan = sin_sala(p)
    nota_festivos = (
        "Los cuatro lunes festivos de 2026 (17/08, 12/10, 02/11, 16/11) no tienen clase: una "
        "grabación de esas fechas es una tutoría, un jurado o una reunión ajena y **no** debe "
        "acabar en la carpeta que ven 100+ estudiantes."
        if p.usa_repositorio_cun else
        "Un día sin clase (festivo, receso, una reunión que no era del curso) no tiene "
        "encuentro en el Calendar: la grabación se queda quieta, que es lo que debe pasar."
    )
    # Trozos de prosa que son de la CUN. Con `usa_repositorio_cun` se recomponen tal cual
    # estaban; sin él, la misma idea sin nombrar cursos, grupos ni ficheros de este repo.
    ejemplo_subject = (
        p.rx_subject_ejemplos[0] if p.rx_subject_ejemplos else "Asignatura - Sesion 01"
    )
    if p.usa_repositorio_cun:
        nombre_buscable = (
            "con el nombre por el que el correo de bienvenida y el "
            "`LEEME - Material para estudiantes` le dicen al estudiante que la busque: "
            "«periodo - grupo - asignatura - sesión»."
        )
        donde_viven = "los dos en la raíz de `Cursos/` porque esto es"
        paso_previo = (
            "Esas series las crea `PRINCIPAL - Crear encuentros con invitados.gs` de cada "
            "curso, y hoy **solo Proyecto I la tiene**: los otros cuatro siguen con "
            "`\"meet\": \"\"` en `carga_academica_2026.json` y su serie no se ha creado "
            "(ver «Pendientes» en `LEEME - Mapa de cursos y manuales.md`)."
        )
        donde_faltan = "en esas 6 aulas "
        origen_titulos = "los genera este repositorio"
        ejemplo_nombre = "26V04 - 54448 - Trabajo de Grado 2 - Sesion 01"
        ejemplo_sala = (
            "si la sala es la de Proyecto I y el único encuentro de esa hora es de TG3, **no "
            "se mueve** (antes se movía, y el registro decía «+ sala Proyecto I» como si la "
            "sala lo hubiera confirmado)."
        )
        crea_la_serie = (
            "Créala con `PRINCIPAL - Crear encuentros con invitados.gs` del curso —**no "
            "necesitas la sala de antemano: ese script la crea y la imprime**; el enlace que "
            "imprime se pega en `carga_academica_2026.json → cursos.<key>.meet` y después se "
            "regenera este `.gs`—"
        )
        donde_salas = "`carga_academica_2026.json`"
        reprogramada = (
            "—TG2 dictó la Sesión 01 el **viernes 14/08/2026**, no el lunes—"
        )
        # Dato de la cuenta @cun.edu.co: no se puede afirmar de la cuenta de otra institución.
        sin_contrasena = (
            "que esta cuenta **no puede generar**: el administrador de Workspace lo tiene "
            "deshabilitado"
        )
    else:
        nombre_buscable = (
            "con el nombre canónico del encuentro, el mismo con el que lo titula tu Calendar "
            f"(`{ejemplo_subject}`)."
        )
        donde_viven = "y esto es"
        paso_previo = (
            "Esas series las creas tú en el Calendar de esa misma cuenta, y sus títulos "
            f"tienen que llevar la MARCA («{p.marca}») y encajar con `RX_SUBJECT`: las dos "
            f"cosas las declara el perfil `{p.clave}`. "
            + (p.nota_series or "")
        ).strip()
        donde_faltan = ""
        origen_titulos = "los pone tu Calendar"
        ejemplo_nombre = ejemplo_subject
        ejemplo_sala = (
            "si la sala es la de una asignatura y el único encuentro de esa hora es de otra, "
            "**no se mueve**. La sala sirve para desmentir, no para confirmar."
        )
        crea_la_serie = (
            "Créala en tu Calendar con un título que encaje con `RX_SUBJECT`; si esa "
            "asignatura tiene sala fija de Meet, pégala en `salas` del perfil y regenera"
        )
        donde_salas = "`SALAS` (que sale de `salas` del perfil)"
        reprogramada = (
            "(una clase movida de día sigue teniendo su evento en la fecha real en que se dio)"
        )
        sin_contrasena = (
            "y en muchas cuentas institucionales el administrador ni siquiera las permite"
        )

    horarios = []
    for k in p.cursos:
        dia, ini, fin = _horario(k)
        horarios.append(
            f"| {titulo_para_calendar(k)} | {'/'.join(carga_curso(k)['groups'])} | "
            f"{dia} {ini}–{fin} | "
            + ("sí" if k not in faltan else "**pendiente**")
            + " |"
        )
    L = [
        "# Mover las grabaciones de Meet — automático, sin credenciales",
        "",
        f"**{p.resumen_aulas}** · barrido cada {CADA_MIN} minutos "
        "· un único proyecto de Apps Script, instalado una vez",
        "",
        f"> **Archivo generado — no editar a mano.** Perfil `{p.clave}`. Regenerar: "
        f"`python config/slides/build_apps_script_grabaciones.py {p.clave}`",
        "",
        "## Qué vas a conseguir",
        "",
        "Que cada grabación de Meet salga sola de donde Google la deja —la carpeta por omisión "
        "de Meet en tu Mi unidad: hoy «Meet Recordings»— y aparezca en la **carpeta única de "
        f"grabaciones** ({p.destino_url}) {nombre_buscable} **Unos diez minutos** de "
        "instalación, una sola vez; después no hay que volver a tocarlo, ni el semestre que "
        "viene.",
        "",
        f"No necesita contraseña, ni token, ni contraseña de aplicación ({sin_contrasena}), ni que "
        "tu computador esté encendido. Apps Script corre en los servidores de Google con tu "
        "propia sesión.",
        "",
        f"Son dos archivos, {donde_viven} **uno solo para "
        f"todos los cursos** (no hay una copia por grupo): `{p.gs_name}`, que es el que se pega "
        "en Apps Script, y este runbook.",
        "",
        "## ⚠️ Lo primero: un dato que pegar y un paso previo",
        "",
        "**El dato:** `ORIGEN_ID` sale **vacío a propósito**. Es la carpeta por "
        "omisión donde Meet te deja las grabaciones, en tu Mi unidad — **hoy «Meet "
        "Recordings»**; si tu Drive muestra en su lugar una carpeta **«Google Meet»** con una "
        "subcarpeta por reunión, usa esa (y si dentro tienes «Legacy Meet Recordings», es lo "
        "antiguo: se deja fuera salvo que pongas `ORIGEN_LEGACY_ID`). No está en el "
        "repositorio porque no se puede deducir, y el script tampoco elige «la primera "
        "carpeta con ese nombre»: Google ha movido y renombrado estas carpetas más de una "
        "vez, así que **el enlace se pega a mano** (o el id, si lo prefieres).",
        "",
        "Cómo se saca: abre la carpeta en Drive y **copia el enlace de la barra de "
        "direcciones, entero**. No hay que sacarle el id a mano —eso es de donde salen los "
        "errores tontos—: el propio `.gs` lo extrae, y entiende las cuatro formas en que "
        "Drive reparte enlaces, además del id pelado.",
        "",
        "```",
        "https://drive.google.com/drive/folders/1AbCdEfG...              <- pégalo así, entero",
        "https://drive.google.com/drive/u/0/folders/1AbCdEfG...          <- también vale",
        "https://drive.google.com/drive/folders/1AbCdEfG...?usp=sharing  <- también",
        "https://drive.google.com/open?id=1AbCdEfG...                    <- también",
        "1AbCdEfG...                                                     <- y el id pelado",
        "```",
        "",
        "Si pegas por error el enlace de un **archivo** (los que llevan `/d/`) en vez del de la "
        "carpeta, el registro te lo dice con esas palabras y esa constante queda vacía: el "
        "script avisa y no mueve nada, nunca adivina.",
        "",
        "Mientras `ORIGEN_ID` esté vacío el script **no mueve nada** y te dice que falta; "
        "`verificarGrabaciones()` incluso te lista candidatos por nombre para copiar y pegar.",
        "",
        "**El paso previo:** los encuentros de la asignatura tienen que **existir en tu "
        "Calendar**. Cuando Meet no nombra el archivo con el título del evento (pasa siempre "
        "que la reunión se inicia desde la sala), lo único que puede decir de qué clase es "
        f"resulta ser el propio Calendar. {paso_previo} Sin eso, {donde_faltan}cada grabación "
        "saldrá en `--- sin clasificar ---` con «no hay ningún encuentro en el Calendar…» y se "
        "quedará quieta: no es que el automatismo no sirva, es que falta el paso anterior.",
        "",
        "Y un supuesto que conviene confirmar el primer día: **la carpeta de grabaciones está en "
        "Mi unidad**, no en una unidad compartida. Si estuviera en una unidad compartida, "
        "`DriveApp` no bastaría (haría falta el servicio avanzado de Drive) y —lo importante— "
        "mover el vídeo allí **transferiría su propiedad a la institución de forma "
        "irreversible**. Si algún día se decide eso, se decide a propósito y no como efecto "
        "secundario de este script.",
        "",
        "## Paso a paso",
        "",
        f"### 1. Abre Apps Script con la cuenta {p.institucion}",
        "",
        f"**https://script.google.com** con **{p.docente_correo}**. Tiene que ser la cuenta del "
        "**organizador** de las clases: las grabaciones nacen en *su* Mi unidad y ningún script "
        "puede ver el Drive de otra persona. **Nuevo proyecto** → borra el `function "
        "myFunction()` de fábrica → pega **todo** el contenido de "
        f"`{p.gs_name}` → guarda. Ponle un nombre reconocible al proyecto: "
        f"«{p.proyecto_sugerido}».",
        "",
        "No hace falta añadir ningún servicio avanzado. Este script usa solo Drive, Calendar y "
        "los disparadores, que vienen de serie.",
        "",
        "### 2. Pega el `ORIGEN_ID`",
        "",
        "En el bloque `// ─── CONFIGURACIÓN ───`, la única constante que sale vacía:",
        "",
        "```js",
        "var ORIGEN_ID = '';   // <- pega aquí el ENLACE de tu carpeta de grabaciones de Meet",
        "```",
        "",
        "Guarda. Lo demás ya viene puesto desde el perfil: la carpeta destino "
        f"(`{p.destino_url}` → id `{dest}`), el calendario (`{p.calendario_id}`) y las salas de "
        "Meet conocidas.",
        "",
        "### 3. Ejecuta `verificarGrabaciones()` — siempre, antes que nada",
        "",
        "Elige **`verificarGrabaciones`** en el desplegable de arriba y pulsa **Ejecutar**.",
        "",
        "La primera vez Google pide permisos: **Revisar permisos** → tu cuenta "
        f"{p.institucion} → «Google no "
        "ha verificado esta aplicación» → **Configuración avanzada** → **Ir a (nombre del "
        "proyecto)** → **Permitir**. Es tu propio script; el aviso sale porque no está "
        "publicado en ninguna tienda.",
        "",
        "`verificarGrabaciones()` **no mueve, no renombra, no borra y no instala nada**. Solo "
        "escribe en el registro (*Ver → Registro de ejecución*):",
        "",
        "- el modo (`SIMULACIÓN` / `REAL`), la zona horaria y los márgenes;",
        f"- el **calendario** con su nombre y su id — comprueba que es el tuyo de "
        f"{p.institucion};",
        "- las carpetas **ORIGEN** y **DESTINO** con nombre e id;",
        "- si hay disparador instalado y cuántos movimientos se pueden deshacer;",
        "- un bloque **`--- se moverían ---`** con una línea por archivo, el criterio con el que "
        "lo identificó y **el nombre nuevo** si va a renombrarlo;",
        "- un bloque **`--- sin clasificar ---`** con lo que se queda quieto **y por qué**;",
        "- el resumen contable: `se moverían=… · se renombrarían=… · sin clasificar=…`.",
        "",
        "Si algo no cuadra —calendario equivocado, un archivo ajeno en la lista de «se "
        "moverían»— párate aquí. Todavía no has tocado nada.",
        "",
        "### 4. Apaga la simulación y muévelo una vez a mano",
        "",
        "```js",
        "var SIMULAR = true;    // ponlo en false",
        "```",
        "",
        "Guarda y ejecuta **`moverGrabaciones()`**. Verás una línea `movido: …` por archivo y el "
        "resumen `movidos=… · renombrados=… · sin clasificar=… · fallidos=… · en gracia=… · "
        "descartados antes=… · sin mirar por falta de tiempo=… · subcarpetas vaciadas=…`. Abre "
        "la carpeta destino y compruébalo con tus ojos.",
        "",
        "`en gracia=` son los archivos que aparecieron hace menos de "
        f"{MARGEN_MIN} minutos: se dejan a propósito, por si Meet todavía está depositando la "
        "transcripción o las notas. Los recoge la pasada siguiente.",
        "",
        "Volver a ejecutarlo **no mueve nada dos veces**: lo ya movido no está en el origen. Y "
        "lo que no supo clasificar sigue donde estaba, con su nombre intacto.",
        "",
        "### 5. Instala el disparador",
        "",
        "Ejecuta **`instalarDisparador()`**. Crea un disparador temporal que llama a "
        f"`moverGrabaciones()` **cada {CADA_MIN} minutos**. Si ya hay uno, **no crea un segundo**: "
        "te dice cuál existe.",
        "",
        f"Por qué {CADA_MIN} y no cada 15 o cada minuto: la cuota de Workspace es **360 "
        "min/día de disparadores**, y este script se permite hasta **4,5 min por pasada** "
        "(`LIMITE_MS`, el freno con el que evita morir en los 6 min que da Apps Script). En el "
        f"peor caso, {CADA_MIN} min son 48 pasadas × 4,5 = **216 min**, que caben; cada 15 min "
        "serían 96 × 4,5 = 432 min, que **no** caben —Google cortaría el disparador el resto "
        "del día con «Service invoked too many times for one day»— y cada minuto ni de lejos. "
        "En la práctica una pasada normal tarda segundos: los 4,5 min solo se acercan si hay "
        "un lote grande. Y Apps Script programa con ventanas de ±15 min, así que la hora exacta "
        "no está garantizada y tampoco hace falta: la grabación tarda en generarse.",
        "",
        "Si un día falla, Google te manda un correo con el error. No hay que vigilarlo.",
        "",
        "## Qué permisos pide y por qué",
        "",
        "| Permiso | Para qué lo usa |",
        "|---|---|",
        "| **Ver y gestionar tus archivos de Google Drive** | Leer la carpeta de grabaciones de "
        "Meet, mover el archivo a la carpeta de grabaciones y renombrarlo. Es el permiso amplio de "
        "`DriveApp`: Google no ofrece uno más estrecho para mover archivos. El script solo "
        "recorre `ORIGEN_ID` y escribe en `DESTINO_ID`, y **nunca borra**. |",
        "| **Ver los eventos de tus calendarios** | Preguntar qué encuentro había a la hora de "
        "la grabación. Es de solo lectura: el script no crea ni modifica eventos. |",
        "| **Ejecutarse cuando no estás presente** | El disparador temporal. Es lo que hace que "
        "funcione con el computador apagado. |",
        "",
        "Nada de eso guarda una credencial: el script se ejecuta *como tú*, y si algún día "
        "quieres cortarlo, borras el proyecto de Apps Script y se acabó.",
        "",
        "## Qué NO rompe (y la única cosa que sí cambia)",
        "",
        "- **Los enlaces siguen funcionando.** Mover un archivo en Drive **no cambia su "
        "`fileId`**, así que el enlace que Meet te envió por correo, el que hayas pegado en "
        "CDigital y el que tenga cualquier estudiante siguen abriendo el mismo vídeo. Google "
        "se apoyó en esa misma propiedad para su mudanza de julio de 2026 («your old recording "
        "links will continue to work»). Por eso el script **mueve y no copia**: una copia "
        "tendría otro id y habría dos verdades.",
        "- **Renombrar tampoco cambia el enlace.** Solo se renombra lo que **no** traía el "
        "nombre buscable; el nombre que puso Meet se conserva íntegro entre paréntesis, y "
        "`revertirMovimientos()` restaura nombre **y** carpeta.",
        "- **Lo que sí cambia: el acceso que se heredaba de la carpeta.** Los permisos propios "
        "del archivo (con quién lo compartiste explícitamente) viajan con él, pero quien "
        "llegaba a él *porque tenía acceso a la carpeta de Meet* deja de tener ese camino, y "
        "quien tenga acceso a la carpeta de grabaciones lo gana. Como la carpeta destino es "
        "justo la que está publicada a los estudiantes, el efecto va en la dirección "
        "deseada — pero conviene saberlo.",
        "- **No se borra nada, nunca.** Las subcarpetas de reunión quedan vacías en su sitio y "
        "se cuentan en el registro (`subcarpetas vaciadas=`).",
        "",
        "## Cómo decide a qué asignatura pertenece cada grabación",
        "",
        "Tres criterios en cascada, y una cuarta salida que es **no tocar**:",
        "",
        "1. **El nombre ya trae el subject canónico.** Meet nombra el archivo con el título del "
        f"evento desde el que se inició la reunión, y esos títulos {origen_titulos} "
        f"(`{ejemplo_nombre}`). Se mueve tal cual, sin renombrar.",
        "2. **Cruce con tu Calendar por fecha y hora.** Si el nombre no trae el subject (pasa "
        "cuando la reunión se inicia desde la sala y no desde el evento), busca el encuentro de "
        "esa hora en tu calendario y, si hay **exactamente uno**, mueve y renombra al nombre "
        f"canónico. El Calendar es la autoridad: ya contiene las reprogramaciones {reprogramada}"
        " y por eso el script **sigue "
        "funcionando el semestre que viene sin tocar una línea**. Dos detalles que evitan "
        "publicar una reunión ajena con nombre de clase: la marca de tiempo del nombre tiene "
        "que caer **dentro** del encuentro (se admiten 15 min antes del inicio, nada después "
        "del final), y si el nombre **no trae hora** solo queda la fecha de creación del "
        "archivo, que es posterior a la clase: entonces se mira hacia **atrás** (6 h) y solo "
        "valen encuentros ya terminados. Nunca «el día del archivo» — a las 00:20 ese día ya "
        "es el siguiente.",
        "3. **El código de sala de Meet**, para desempatar y sobre todo para **desmentir**: "
        f"{ejemplo_sala}",
        "4. **Si no lo sabe, no lo mueve.** Sale en `--- sin clasificar ---` con el motivo. "
        + nota_festivos,
    ]
    if p.cursos:
        L += [
            "",
            "| Asignatura | Grupos | Horario | ¿Sala en config? |",
            "|---|---|---|---|",
        ]
        L += horarios
    if faltan:
        L += [
            "",
            "Las salas «pendientes» no impiden nada (el criterio 2 no las necesita), pero "
            "conviene pegarlas: son la red de seguridad cuando una grabación no trae el nombre "
            "del evento. Las imprime el propio `PRINCIPAL - Crear encuentros con invitados.gs` "
            "al crear la serie; van a `config/cursos/carga_academica_2026.json → "
            "cursos.<key>.meet` y después se regenera este `.gs`.",
        ]
    L += [
        "",
        "## Otra institución: los perfiles",
        "",
        "Este `.gs` y este runbook los escribe un generador que lleva **un perfil por "
        "institución** (`config/slides/build_apps_script_grabaciones.py` → `PERFILES`). Sin "
        f"argumentos usa `{PERFIL_POR_OMISION}`, que es lo de siempre; con un argumento, ese "
        "perfil:",
        "",
        "```",
        "python config/slides/build_apps_script_grabaciones.py            # "
        f"{PERFIL_POR_OMISION}",
        "python config/slides/build_apps_script_grabaciones.py PLANTILLA  # otra institución",
        "```",
        "",
        "Si le pides un perfil que no existe, te lista los que hay y no escribe nada. Cada "
        "perfil declara: nombre de la institución y correo, zona horaria y desfase UTC "
        "esperado, la marca que identifica un encuentro en el título del evento, el patrón del "
        "asunto, los nombres de carpeta de origen que se usan para sugerir candidatos, el id "
        "del calendario, las salas de Meet y **los enlaces de las carpetas de Drive, pegados "
        "tal cual**. Los perfiles que no son el de la CUN escriben sus dos archivos con el "
        "nombre sufijado, así que no se pisan.",
        "",
        "## Lo que NO se puede parametrizar",
        "",
        "Un perfil cambia constantes, no supuestos. Estos siguen ahí, y conviene leerlos antes "
        "de prometerle esto a otra institución:",
        "",
        "- **La clasificación va por el Calendar, y eso no es opcional.** El número de sesión "
        "del *nombre del archivo* no sirve: está medido —los 19 artefactos reales de la carpeta "
        "decían todos «Sesion 01»— porque Meet congela el título del evento con el que se "
        "estrenó la sala. Así que la institución necesita **tener los encuentros en el "
        "Calendar** y titularlos de forma reconocible (`MARCA` y `RX_SUBJECT`). Sin eso, el "
        "script no clasifica nada y todo se queda quieto: no falla, no hace.",
        "- **El nombre que Meet le pone al archivo es de Meet, no de la institución.** "
        "`RX_FECHA` es la misma para todos los perfiles a propósito: no está documentada por "
        "Google y ya cambió una vez sin avisar. Si cambia otra vez, se arregla en un sitio. "
        "**Y hoy está sin arreglar:** medido sobre los archivos reales de la carpeta, ese "
        "patrón **no caza ninguno** —Meet los nombra `2026 08 13 17 00 GMT-05 00`, con "
        "espacios y sin dos puntos—, así que la hora del nombre nunca se usa y todo pasa por "
        "el respaldo aproximado (fecha de creación, mirando hacia atrás). Corregirlo cambia el "
        "comportamiento y se decide aparte; y mientras no cace, poner otro "
        "`DESFASE_ESPERADO` en un perfil nuevo no cambia nada.",
        "- **`DESFASE_ESPERADO` es uno solo.** Vale donde no hay horario de verano (Colombia). "
        "Donde sí lo hay, media parte del año la hora del nombre se descarta y todo cae al "
        "respaldo por fecha de creación: sale más «AMBIGUO», nunca un movimiento erróneo. Y un "
        "huso a media hora (`+05:30`) no se distingue de `+05`.",
        "- **Una cuenta, un Drive, un organizador.** Apps Script solo ve el Drive de su dueño. "
        "Si la clase la graba otra persona, el archivo nace en *su* Mi unidad y ningún script "
        "tuyo lo ve. Se instala un proyecto por organizador; no es un parámetro.",
        "- **Supone Mi unidad, no unidades compartidas.** Con una unidad compartida `DriveApp` "
        "ya no basta y mover el vídeo allí transfiere su propiedad. Eso sería otro camino de "
        "código, no otro valor en el perfil.",
        "- **Los topes son cuota de Google.** `CADA_MIN`, `LIMITE_MS`, `MAX_*`: se pueden bajar, "
        "no subir. Y la cuota de disparadores de una cuenta **sin** Workspace es bastante "
        "menor: ahí `CADA_MIN = 30` deja de caber y hay que espaciarlo más.",
        "- **Las carpetas de origen no se eligen por nombre, nunca.** Los nombres los pone "
        "Google (y los renombró en julio de 2026): `NOMBRES_ORIGEN` solo sirve para *sugerir* "
        "candidatos en el registro. El id —o el enlace— lo pega una persona.",
        "- **La prosa del `.gs` es de la CUN.** Habla de «estudiantes», de «tutorías y "
        "jurados», del correo de bienvenida y de rutas de este repositorio. Se deja tal cual a "
        "propósito: parametrizar los textos del cuerpo obligaría a tocar el código que ya "
        "funciona, y ese es el riesgo que no compensa. Léelos como ejemplos, no como "
        "descripción de tu institución.",
        "",
        "## Si algo sale mal",
        "",
        "| Lo que ves | Qué pasa y qué haces |",
        "|---|---|",
        "| `ORIGEN : SIN CONFIGURAR — no se moverá nada` | Te saltaste el paso 2. El registro "
        "te lista candidatos con su id: copia el de «Google Meet» y pégalo en `ORIGEN_ID`. |",
        "| `SIMULAR = true: NO se movió nada de verdad` | Sigue en modo simulación. Paso 4. |",
        "| `ERROR en «…»: probablemente Drive creó un ATAJO en vez de mover` | No tienes permiso "
        "para mover a la carpeta destino. Drive falla en silencio dejando un atajo, así que el "
        "script comprueba el resultado y lo cuenta como `fallidos=`. Revisa que la carpeta de "
        "grabaciones sea tuya (o que puedas escribir en ella), **borra a mano el atajo que haya "
        "quedado en ella** y vuelve a ejecutar. |",
        "| Un archivo sale en `--- sin clasificar ---` con `AMBIGUO` | Había dos encuentros que "
        "encajaban a esa hora. Muévelo a mano; el script no adivina. |",
        "| `no hay ningún encuentro en el Calendar …` | Lo más probable: **la serie de "
        f"encuentros de ese curso todavía no existe**. {crea_la_serie} y ejecuta "
        "`reintentarPendientes()`. Si "
        "la serie ya existe y aun así sale esto, era una tutoría, un jurado o una reunión "
        "ajena: **no** debe publicarse. |",
        "| `la sala dice «X» y … no es de esa asignatura` | "
        "El desempate por sala **desmintió** la clasificación: se quedó quieto a propósito. "
        f"Comprueba la sala en {donde_salas} y, si el archivo era de clase, muévelo "
        "a mano. |",
        "| `sin encuentro en el Calendar … (fecha aproximada)` | El nombre no traía hora y hubo "
        "que usar la fecha de creación del archivo (se buscan encuentros terminados en las 6 h "
        "anteriores). Si de verdad era una clase, muévela a mano y renómbrala con el título del "
        "evento. |",
        "| `ya intenté moverlo y Drive dejó un ATAJO` | El archivo está **aparcado a "
        "propósito**: reintentarlo cada pasada llenaría de atajos la carpeta que ven los "
        "estudiantes. Arregla el permiso sobre la carpeta destino, borra los atajos que hayan "
        "quedado y ejecuta `reintentarPendientes()`. |",
        "| `descartado(s) en pasadas anteriores` / `Aparcados N archivo(s) sin clasificar` | "
        "Normal: lo que no se puede clasificar (tutorías, jurados) se deja de mirar durante 24 h "
        "para que no se coma el cupo de la pasada y tape las grabaciones nuevas. Se vuelve a "
        "mirar solo con `reintentarPendientes()` o cuando pasen esas 24 h. |",
        "| `AVISO: hay N archivo(s) en el origen … pero NINGUNO se pudo clasificar` | El fallo "
        "silencioso que sí importa. Casi siempre falta la serie de encuentros en el Calendar; "
        "lee los motivos de arriba. |",
        "| `AVISO: no encontré NINGÚN archivo … y hubo N encuentro(s) en las últimas 48 h` | O "
        "no grabaste, o Google volvió a cambiar la carpeta, o **la grabación la inició otra "
        "persona** — en ese caso el archivo nace en el Drive de esa persona y ningún script "
        "tuyo puede verlo. Graba siempre tú, como organizador. |",
        "| `AVISO: registro recortado en N entrada(s)` | El historial de deshacer solo guarda lo "
        "reciente (tope de tamaño de las propiedades del proyecto). Lo antiguo ya no se puede "
        "revertir automáticamente; moverlo a mano, sí. |",
        "| «Se ha excedido el tiempo máximo de ejecución» | No debería salir: el script corta "
        "solo a los 4,5 min y avisa de cuántos archivos deja para la próxima. Si sale, vuelve a "
        "ejecutar (el disparador lo haría solo). **No hay estado guardado del barrido**: la "
        "pasada siguiente vuelve a empezar, pero mirando **primero lo más nuevo**, así que la "
        "grabación de hoy entra antes que el residuo viejo. |",
        "| Un vídeo llegó a la carpeta pero su transcripción no | Normal: los artefactos de Meet "
        "aparecen en momentos distintos (los subtítulos pueden tardar horas). La siguiente "
        "pasada la recoge y le pone el mismo nombre. |",
        "",
        "## Cómo deshacer",
        "",
        "- **`revertirMovimientos()`** — devuelve cada archivo del registro a su carpeta y a su "
        "nombre anteriores, del más reciente al más antiguo. No borra nada y no toca lo que no "
        "movió este script. Con `SIMULAR = true` solo dice qué haría.",
        "- **`quitarDisparador()`** — para el automatismo. Lo ya movido sigue movido.",
        "- **`reintentarPendientes()`** — vuelve a mirar lo aparcado: lo que no se pudo "
        "clasificar (aparcado 24 h para que el residuo no tape las grabaciones nuevas) y lo que "
        "**falló al moverse** (aparcado hasta aquí para no llenar de atajos la carpeta "
        "publicada). Ejecútalo después de crear la serie de encuentros que faltaba, de pegar una "
        "sala en el JSON o de arreglar el permiso del destino. No mueve nada por sí solo.",
        "- **`olvidarRegistro()`** — suelta el historial. **No devuelve ningún archivo**: "
        "después de esto `revertirMovimientos()` ya no puede deshacer lo olvidado. La "
        "idempotencia no depende de él (lo ya movido no vuelve a moverse porque ya no está en "
        "el origen).",
        "- **Quitarlo del todo:** `quitarDisparador()` → borra el proyecto de Apps Script. No "
        "queda ninguna credencial que revocar.",
        "",
        "## De dónde sale cada dato",
        "",
        f"- Perfil `{p.clave}` — `config/slides/build_apps_script_grabaciones.py` → `PERFILES`. "
        "Ahí están la zona horaria, el desfase, la marca, el patrón del asunto, el calendario "
        "y los enlaces de las carpetas.",
    ]
    # Las fuentes son rutas de ESTE repositorio: solo valen para un perfil respaldado por él.
    if p.usa_repositorio_cun:
        L += [
            f"- Carpeta destino `{dest}` — de `config/cursos/carga_academica.py` → "
            "`GRABACIONES_URL`, que es **una sola para los 5 cursos y todos los periodos** y ya "
            "está publicada en el correo de bienvenida "
            "(`config/slides/build_correo_bienvenida.py`) y en el LEEME del estudiante "
            "(`config/slides/sync_clases_estudiantes.py`). Por eso no hay una carpeta por "
            "asignatura: cambiarla dejaría mintiendo documentos que ya están en manos de los "
            "estudiantes.",
            "- Patrón del nombre buscable — `config/cursos/sesiones_cun.py` → "
            "`subject_encuentro()`. El periodo va delante justamente porque esa carpeta acumula "
            "todos los periodos.",
            "- Horarios, grupos y salas de Meet — `config/cursos/carga_academica_2026.json`.",
            "- Los eventos del calendario los crea "
            "`config/slides/build_calendar_encuentros.py` → "
            "`PRINCIPAL - Crear encuentros con invitados.gs` (uno por grupo, en "
            "`<Curso>/2026/<grupo>/`). Este script **los lee**, no los toca.",
        ]
    else:
        L += [
            f"- Carpeta destino — el enlace que el perfil `{p.clave}` trae en `destino_url`, "
            f"pegado tal cual (`{p.destino_url or 'todavía SIN RELLENAR'}`"
            + (f" → id `{dest}`" if dest else "")
            + "). Si esa carpeta ya está publicada a los estudiantes, cambiarla dejaría "
            "mintiendo lo que ya está en sus manos: se cambia en el perfil y se regenera.",
            "- Patrón del nombre buscable — `rx_subject` del perfil, que es la nomenclatura con "
            "la que tu institución titula los encuentros del Calendar.",
            "- Salas de Meet — `salas` del perfil: `{código: nombre de la asignatura tal como "
            "aparece en el título del evento}`.",
            "- Los eventos del calendario los crea quien monte la serie de encuentros en tu "
            "institución. Este script **los lee**, no los toca.",
        ]
    L += [
        "",
        "Si cambia cualquiera de esos datos, regenera: "
        f"`python config/slides/build_apps_script_grabaciones.py {p.clave}`.",
    ]
    return "\n".join(L) + "\n"


def main(argv: list[str]) -> int:
    """Sin argumentos, el perfil de la CUN: la invocación de siempre sigue igual."""
    arg = (argv[0].strip() if argv else "")
    if arg in ("-h", "--help", "--perfiles"):
        print("Uso: python config/slides/build_apps_script_grabaciones.py [PERFIL]")
        print(f"     sin PERFIL se usa {PERFIL_POR_OMISION}")
        for k in sorted(PERFILES):
            q = PERFILES[k]
            print(f"     {k:<10} {q.institucion} · {q.timezone} · {q.gs_name}")
        return 0

    p = perfil(arg or None)
    raiz = workspace_root()
    dest = destino_id(p)
    sal = salas_del_perfil(p)

    gs = raiz / p.gs_name
    gs.write_text(_gs_texto(p, sal), encoding="utf-8")
    leeme = raiz / p.leeme_name
    leeme.write_text(_leeme_texto(p, sal, dest), encoding="utf-8")

    # Los nombres viejos solo los limpia el perfil por omisión: los archivos de otro perfil
    # llevan sufijo y no son basura de una versión anterior de este build.
    if not p.sufijo:
        for viejo in GS_LEGACY:
            ruta = raiz / viejo
            if viejo != p.gs_name and ruta.exists():
                try:
                    ruta.unlink()
                except OSError:
                    pass

    faltan = sin_sala(p)
    total = len(p.cursos) or len(sal)
    print(f"OK {p.gs_name} · perfil={p.clave} · destino={dest or '(SIN DESTINO)'} · "
          f"salas en config={len(sal)}/{total}")
    print(f"   runbook: {p.leeme_name}")
    print("   ORIGEN_ID sale VACÍO a propósito: la carpeta por omisión de Meet (hoy «Meet "
          "Recordings») la pega el docente — y ahora acepta el ENLACE tal cual, no solo el id.")
    if not dest:
        print(f"   AVISO: el perfil {p.clave} no trae destino_url: pega el enlace de la carpeta "
              "de grabaciones en PERFILES antes de usarlo.")
    if faltan:
        print("   sin sala en carga_academica_2026.json -> cursos.<key>.meet: "
              + ", ".join(faltan))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
