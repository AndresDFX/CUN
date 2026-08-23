# -*- coding: utf-8 -*-
r"""
Ejecuta `PRINCIPAL - Comentar documentos de estudiantes.gs` en Node, con las globales de Apps Script
simuladas, y comprueba que se comporta como dice su documentación.

Por qué existe: ese `.gs` es un archivo **generado** que se pega en los servidores de Google y actúa
sobre el documento de un estudiante. Si falla, falla delante del estudiante y ya está publicado. Aquí
se prueba sin cuenta, sin red y sin tocar nada: se le da un documento de mentira y se mira qué hace.

Cubre lo que de verdad se puede romper:
  1. camino feliz — las citas se encuentran y se ubican en su párrafo
  2. tipografía distinta entre el .docx y el documento vivo (comillas curvas, guion largo, NBSP)
  3. cita que el estudiante ya editó → se omite, no se revienta ni se publica en el sitio equivocado
  4. criterio que no está en la guía del ACA → aborta y dice cuáles son los válidos
  5. compartido en modo Lector → aborta pidiendo «Comentador»
  6. publicar() sin CONFIRMAR → aborta
  7. publicar() con CONFIRMAR → publica, con quotedFileContent, y deshacer() los borra

    python config/gdocs/_prueba_apps_script.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import criterios_aca as CA  # noqa: E402

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

GS = CA.REPO / "PRINCIPAL - Comentar documentos de estudiantes.gs"

# Documento de mentira, con encabezado y tabla, como un anteproyecto de verdad.
DOC = {
    "body": {"content": [
        {"paragraph": {"paragraphStyle": {"namedStyleType": "HEADING_1"},
                       "elements": [{"textRun": {"content": "2. Planteamiento del problema\n"}}]}},
        {"paragraph": {"paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                       "elements": [{"textRun": {"content": "La gente tiene problemas con los "
                                                            "tramites en la ciudad.\n"}}]}},
        {"paragraph": {"paragraphStyle": {"namedStyleType": "HEADING_1"},
                       "elements": [{"textRun": {"content": "3. Objetivos\n"}}]}},
        {"paragraph": {"paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                       "elements": [{"textRun": {"content": "Desarrollar un “sistema” que "
                                                            "mejore —de forma medible— la "
                                                            "atención.\n"}}]}},
        {"table": {"tableRows": [{"tableCells": [
            {"content": [{"paragraph": {"paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                                        "elements": [{"textRun": {"content": "Cronograma: 6 meses\n"}}]}}]}
        ]}]}},
    ]}
}

CRIT_P1 = CA.criterios("proyecto1", "aca1")[1]

HARNESS = r"""
// ─── globales de Apps Script, simuladas ───
var _log = [], _posts = [], _deletes = [], _props = {};
var PRUEBA = JSON.parse(process.argv[2]);

var Logger = {log: function (t) { _log.push(String(t)); }};
var Session = {
  getActiveUser: function () { return {getEmail: function () { return 'julian_castanoe@cun.edu.co'; }}; },
  getScriptTimeZone: function () { return 'America/Bogota'; }
};
var ScriptApp = {getOAuthToken: function () { return 'TOKEN-FALSO'; }};
var DriveApp = {getRootFolder: function () { return {}; }};
var Utilities = {formatDate: function () { return '2026-08-20 10:00'; }};
var PropertiesService = {
  getScriptProperties: function () {
    return {
      getProperty: function (k) { return _props[k] || null; },
      setProperty: function (k, v) { _props[k] = v; },
      deleteProperty: function (k) { delete _props[k]; }
    };
  }
};
function _resp(codigo, cuerpo) {
  return {getResponseCode: function () { return codigo; },
          getContentText: function () { return JSON.stringify(cuerpo); }};
}
var UrlFetchApp = {
  fetch: function (url, opciones) {
    var metodo = (opciones && opciones.method ? opciones.method : 'get').toLowerCase();
    if (url.indexOf('docs.googleapis.com') >= 0) return _resp(200, PRUEBA.doc);
    if (url.indexOf('/comments') >= 0 && metodo === 'post') {
      _posts.push(JSON.parse(opciones.payload));
      return _resp(200, {id: 'comentario-' + (_posts.length)});
    }
    if (url.indexOf('/comments/') >= 0 && metodo === 'delete') {
      _deletes.push(url.split('/comments/')[1]);
      return _resp(204, {});
    }
    return _resp(200, {name: 'ACA 1 - Perez.docx',
                       owners: [{displayName: 'Estudiante Prueba', emailAddress: 'e@cun.edu.co'}],
                       capabilities: {canComment: PRUEBA.canComment}});
  }
};

var PLAN = PRUEBA.plan;
var CONFIRMAR = PRUEBA.confirmar;
"""

COLA = r"""
// ─── ejecutar lo que pida la prueba ───
var salida = {ok: true, error: null};
try {
  if (PRUEBA.accion === 'deshacer') { deshacer(); }
  else { _correr(PRUEBA.accion); }
} catch (e) {
  salida.ok = false;
  salida.error = String(e && e.message ? e.message : e);
}
salida.log = _log;
salida.posts = _posts;
salida.deletes = _deletes;
salida.props = _props;
console.log(JSON.stringify(salida));
"""


def correr(accion: str, plan: dict, *, confirmar: bool = False, can_comment: bool = True,
           props: dict | None = None) -> dict:
    fuente = GS.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        js = Path(tmp) / "prueba.js"
        pre = HARNESS
        if props:
            pre += "\n_props = " + json.dumps(props, ensure_ascii=False) + ";\n"
        js.write_text(pre + "\n" + fuente + "\n" + COLA, encoding="utf-8")
        entrada = json.dumps({"doc": DOC, "plan": plan, "confirmar": confirmar,
                              "canComment": can_comment, "accion": accion}, ensure_ascii=False)
        r = subprocess.run([("node"), str(js), entrada], capture_output=True, text=True,
                           encoding="utf-8")
        if r.returncode != 0:
            raise SystemExit(f"node falló:\n{r.stderr[:2000]}")
        return json.loads(r.stdout.strip().splitlines()[-1])


def plan_base(comentarios: list[dict]) -> dict:
    return {"docId": "DOC-FALSO", "titulo": "ACA 1 - Perez", "curso": "proyecto1",
            "aca": "aca1", "guia": "ACA 1", "comentarios": comentarios}


def main() -> int:
    if not GS.is_file():
        raise SystemExit(f"No está {GS.name}. Corre build_apps_script_comentarios.py primero.")

    fallos: list[str] = []

    def check(nombre: str, condicion: bool, detalle: str = "") -> None:
        print(("  OK   " if condicion else "  FALLA ") + nombre + ("" if condicion else f"  → {detalle}"))
        if not condicion:
            fallos.append(nombre)

    # 1. camino feliz
    r = correr("verificar", plan_base([
        {"criterio": CRIT_P1[0], "cita": "La gente tiene problemas con los tramites en la ciudad.",
         "texto": "«La gente» no es un usuario situado."},
    ]))
    log = "\n".join(r["log"])
    check("1. camino feliz: la cita se ubica en su párrafo", r["ok"] and "en pie 1 · omitidos 0" in log,
          r.get("error") or log[-300:])
    check("1b. ubica la sección y el párrafo del documento vivo", "párrafo 2" in log, log[-300:])

    # 2. tipografía distinta entre el .docx descargado y el documento vivo
    r = correr("simular", plan_base([
        {"criterio": CRIT_P1[0],
         # comillas rectas, guion corto y espacio normal: el documento vivo tiene curvas, raya y NBSP
         "cita": 'Desarrollar un "sistema" que mejore -de forma medible- la atención.',
         "texto": "El objetivo general no es medible todavía."},
    ]))
    log = "\n".join(r["log"])
    check("2. tipografía distinta: la cita se encuentra igual", r["ok"] and "omitidos 0" in log,
          r.get("error") or log[-400:])

    # 3. cita que el estudiante ya editó
    r = correr("verificar", plan_base([
        {"criterio": CRIT_P1[0], "cita": "Una frase que el estudiante ya borró del documento.",
         "texto": "…"},
        {"criterio": CRIT_P1[1], "cita": "Cronograma: 6 meses", "texto": "Ubica el cronograma."},
    ]))
    log = "\n".join(r["log"])
    check("3. cita perdida: se omite y sigue con las demás",
          r["ok"] and "en pie 1 · omitidos 1" in log, r.get("error") or log[-300:])
    check("3b. encuentra la cita que está dentro de una tabla", "Cronograma" not in log.split("✗")[-1]
          if "✗" in log else True, log[-300:])

    # 4. criterio inventado
    r = correr("verificar", plan_base([
        {"criterio": "Redacción bonita y uso de negritas", "cita": "Cronograma: 6 meses", "texto": "…"},
    ]))
    check("4. criterio que no está en la guía: aborta",
          (not r["ok"]) and "no están en la guía" in (r["error"] or ""), r.get("error", "")[:200])
    check("4b. al abortar dice cuáles son los criterios válidos",
          CRIT_P1[0] in (r["error"] or ""), (r.get("error") or "")[:200])

    bueno = plan_base([
        {"criterio": CRIT_P1[0], "cita": "La gente tiene problemas con los tramites en la ciudad.",
         "texto": "«La gente» no es un usuario situado."},
        {"criterio": CRIT_P1[3], "cita": "Cronograma: 6 meses", "texto": "El alcance no cabe en 6 meses."},
    ])

    # 5. modo Lector
    r = correr("verificar", bueno, can_comment=False)
    check("5. compartido como Lector: aborta pidiendo «Comentador»",
          (not r["ok"]) and "Comentador" in (r["error"] or ""), r.get("error", "")[:200])

    # 6. publicar sin CONFIRMAR
    r = correr("publicar", bueno, confirmar=False)
    check("6. publicar() sin CONFIRMAR: no publica nada",
          (not r["ok"]) and "CONFIRMAR" in (r["error"] or "") and not r["posts"],
          r.get("error", "")[:200])

    # 7. publicar de verdad
    r = correr("publicar", bueno, confirmar=True)
    check("7. publicar() con CONFIRMAR: publica los 2", r["ok"] and len(r["posts"]) == 2,
          r.get("error") or str(len(r["posts"])))
    if len(r["posts"]) == 2:
        p = r["posts"][0]
        check("7b. cada comentario lleva quotedFileContent con la cita",
              p.get("quotedFileContent", {}).get("value", "").startswith("La gente tiene"),
              json.dumps(p, ensure_ascii=False)[:200])
        check("7c. el cuerpo encabeza con el criterio y la ubicación viva",
              p["content"].startswith(f"Criterio «{CRIT_P1[0]}» — 2. Planteamiento del problema (párrafo 2)"),
              p["content"][:160])
        check("7d. queda registrada la publicación para poder deshacerla",
              "ultima_publicacion" in r["props"], str(list(r["props"])))

        # 8. deshacer
        r2 = correr("deshacer", bueno, props=r["props"])
        check("8. deshacer() borra los 2 comentarios publicados",
              r2["ok"] and len(r2["deletes"]) == 2, r2.get("error") or str(r2["deletes"]))
        check("8b. deshacer() limpia el registro", "ultima_publicacion" not in r2["props"],
              str(list(r2["props"])))

    print(f"\n{len(fallos)} fallos")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
