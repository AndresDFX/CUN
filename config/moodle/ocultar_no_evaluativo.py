"""Dejar en el aula SOLO lo evaluativo y el material del Docente.

Las aulas de CDigital llegan con un montón de componentes de plantilla institucional que
el Docente no usa: SCORM «Contenido N (Haz clic aquí)», páginas de podcast e imágenes
interactivas, foros vacíos sin consigna, placeholders «G1/Video 1/Recurso 1»…  Todos
visibles para el estudiante y todos sin nota.  El estudiante no distingue lo que cuenta de
lo que sobra, y pregunta (caso real: «Foro 1 Temática» y «Generalidades del Proyecto de
Aula», ambos con el mensaje inicial en blanco — ver DIAGNOSTICO_FORO_1_CREATIVIDAD.md).

Este script hace el barrido: censa el aula, clasifica cada componente y oculta lo que no
sea evaluativo ni material del Docente.  Es parte del **alistamiento del aula**
(ALISTAMIENTO_DE_AULAS_CDIGITAL.md, Fase 2 bis).

Ocultar es reversible: `cdigital.py mostrar <cmid>`.  El script escribe el listado de todo
lo que ocultó, precisamente para poder deshacerlo.

    python config/moodle/ocultar_no_evaluativo.py                 # plan de las 7 aulas
    python config/moodle/ocultar_no_evaluativo.py --curso 115463  # plan de una
    python config/moodle/ocultar_no_evaluativo.py --confirmar     # ejecuta

Sin `--confirmar` solo enseña el plan; no toca el aula.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cdigital as cd  # noqa: E402

AULAS = {
    115463: "Creatividad",
    111070: "Investigación C&T",
    129268: "TG2",
    112321: "TG3 · 54450",
    116387: "TG3 · 54466",
    129270: "TG3 · 54467",
    130378: "Proyecto I",
}

# ---------------------------------------------------------------------------------------------
# Qué se queda visible.  Todo lo que no case con estas reglas se oculta.
# ---------------------------------------------------------------------------------------------

# 1) Ítems con peso en la nota → se quedan siempre (los detecta el libro de calificaciones).

# 2) Evaluación docente.  No tiene peso, pero es evaluación institucional: el estudiante
#    evalúa al Docente.  Se queda.
EVALUACION_DOCENTE = re.compile(r"(?i)^(evaluaci[oó]n docente|eval[uú]a tu entorno)")

# 3) Coevaluación: foro valorado.  En el libro aparece como «Coevaluación calificación»,
#    con otro nombre que el del módulo, así que se nombra aparte.
COEVALUACION = re.compile(r"(?i)^coevaluaci[oó]n")

# 4) Material que publica el Docente en el alistamiento.
CARPETAS_DOCENTE = {
    "presentaciones de clase",
    "guías de las acas y de los cuestionarios",
    "guias de las acas y de los cuestionarios",
    "lecturas obligatorias",
    "recursos del curso",
}

# 5) Enlaces operativos del aula (los pone el Docente, no la plantilla).
OPERATIVOS = {
    "avisos",            # canal de anuncios del curso
    "material clases",
    "clases",
    "clases grabadas",
    "sesion en vivo",
    "sesión en vivo",
    "horario",
}

# 6) Foro de presentación: excepción explícita del Docente — es el espacio social del aula.
FORO_PRESENTACION = re.compile(r"(?i)^te queremos conocer")

# 7) Institucionales que el estudiante NECESITA para la entrega calificada, o que son
#    obligación de inicio de semestre.  No dan nota, pero ocultarlos estorba el ACA:
#    la consigna del ACA Final exige citas APA y fuentes de la biblioteca virtual CUN, y el
#    acuerdo pedagógico es ítem del checklist de INICIO del ciclo docente.
#    Si se quieren fuera también, basta: cdigital.py ocultar <cmid>.
SOPORTE_INSTITUCIONAL = re.compile(
    r"(?i)^\s*(normas apa|ingreso a (la )?biblioteca virtual|acuerdo pedag[oó]gico)"
)


def clasificar(modulo: str, nombre: str, peso: float | None) -> tuple[bool, str]:
    """(se_queda, motivo)."""
    n = nombre.strip().lower()

    if peso is not None and peso > 0:
        return True, f"evaluativo · peso {peso * 100:.1f}%"
    if EVALUACION_DOCENTE.match(nombre.strip()):
        return True, "evaluación docente (institucional)"
    if COEVALUACION.match(nombre.strip()):
        return True, "coevaluación · foro valorado"
    if modulo == "folder" and n in CARPETAS_DOCENTE:
        return True, "carpeta de material del Docente"
    if n in OPERATIVOS:
        return True, "enlace operativo del aula"
    if FORO_PRESENTACION.match(nombre.strip()):
        return True, "foro de presentación (excepción del Docente)"
    if SOPORTE_INSTITUCIONAL.match(nombre):
        return True, "soporte institucional que el ACA necesita"
    if modulo == "resource":
        return True, "documento subido por el Docente"

    return False, f"plantilla institucional sin nota ({modulo})"


# ---------------------------------------------------------------------------------------------


def pesos_del_libro(cliente: cd.CDigital, curso: int) -> dict[str, float]:
    """Nombre del ítem de nota -> peso (fracción), leído del libro de calificaciones."""
    pagina = cliente.get("/grade/edit/tree/index.php", params={"id": curso}).text
    pesos: dict[str, float] = {}
    for fila in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", pagina):
        titulo = re.search(
            r'(?is)<a[^>]*class="[^"]*gradeitemheader[^"]*"[^>]*>(.*?)</a>', fila
        )
        if not titulo:
            continue
        nombre = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", titulo.group(1)))).strip()
        peso = re.search(r'(?is)name="weight_(\d+)"[^>]*value="([^"]*)"', fila)
        if peso:
            try:
                pesos[nombre] = float(peso.group(2))
            except ValueError:
                pass
    return pesos


def peso_de(nombre: str, pesos: dict[str, float]) -> float | None:
    """El libro a veces renombra el ítem («Coevaluación» -> «Coevaluación calificación»)."""
    if nombre in pesos:
        return pesos[nombre]
    for clave, valor in pesos.items():
        if clave.startswith(nombre) or nombre.startswith(clave):
            return valor
    return None


def barrer(cliente: cd.CDigital, curso: int, alias: str, confirmar: bool) -> dict:
    estado = cliente.estado_curso(curso)
    modulos = {str(m["id"]): m for m in estado.get("cm", [])}
    pesos = pesos_del_libro(cliente, curso)

    print("=" * 96)
    print(f"AULA {curso}  ·  {alias}")
    print("=" * 96)

    quedan, ocultar, ya_ocultos = [], [], []
    for seccion in estado.get("section", []):
        for cmid in [str(x) for x in (seccion.get("cmlist") or [])]:
            m = modulos.get(cmid, {})
            nombre = html.unescape(str(m.get("name", "?")))
            modulo = str(m.get("module", "?"))
            visible = bool(m.get("visible", True))
            se_queda, motivo = clasificar(modulo, nombre, peso_de(nombre, pesos))
            fila = (cmid, modulo, nombre, motivo)
            if se_queda:
                quedan.append(fila)
            elif visible:
                ocultar.append(fila)
            else:
                ya_ocultos.append(fila)

    print(f"\nSE QUEDAN VISIBLES ({len(quedan)}):")
    for cmid, modulo, nombre, motivo in quedan:
        print(f"   {modulo:9s} {cmid:>9s}  {nombre[:48]:48s} {motivo}")

    if ya_ocultos:
        print(f"\nYA ESTABAN OCULTOS ({len(ya_ocultos)}) — no se toca nada:")
        for cmid, modulo, nombre, _ in ya_ocultos:
            print(f"   {modulo:9s} {cmid:>9s}  {nombre[:48]}")

    print(f"\nSE OCULTAN ({len(ocultar)}):")
    for cmid, modulo, nombre, motivo in ocultar:
        print(f"   {modulo:9s} {cmid:>9s}  {nombre[:48]:48s} {motivo}")

    fallidos = []
    if confirmar and ocultar:
        print(f"\nOcultando {len(ocultar)} componentes…")
        # `cdigital.visibilidad()` verifica ítem por ítem, y eso son 3 peticiones por
        # componente. Aquí son ~130, así que se manda el GET de ocultar y se verifica una
        # sola vez al final releyendo el aula completa.
        for cmid, modulo, nombre, _ in ocultar:
            try:
                cliente.get(f"/course/mod.php?sesskey={cliente.sesskey}&hide={cmid}")
            except Exception as exc:  # noqa: BLE001
                fallidos.append((cmid, nombre, str(exc)))
                print(f"   FALLÓ {cmid} {nombre[:40]}: {exc}")
        # Releer el aula para verificar, no confiar en el GET
        de_nuevo = {str(m["id"]): m for m in cliente.estado_curso(curso).get("cm", [])}
        sigue_visible = [
            (cmid, nombre)
            for cmid, _mod, nombre, _mot in ocultar
            if bool(de_nuevo.get(cmid, {}).get("visible", True))
        ]
        print(f"   verificado releyendo el servidor · siguen visibles: {len(sigue_visible)}")
        for cmid, nombre in sigue_visible:
            print(f"      OJO sigue visible: {cmid} {nombre[:50]}")

    print()
    return {
        "curso": curso,
        "alias": alias,
        "quedan": quedan,
        "ocultar": ocultar,
        "ya_ocultos": ya_ocultos,
        "fallidos": fallidos,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--curso", type=int, action="append", help="Aula concreta (repetible)")
    p.add_argument("--confirmar", action="store_true", help="Ejecutar; sin esto solo simula")
    args = p.parse_args()

    cursos = args.curso or list(AULAS)
    cliente = cd.CDigital()
    cliente.entrar()

    total_ocultos = total_quedan = 0
    for curso in cursos:
        r = barrer(cliente, curso, AULAS.get(curso, str(curso)), args.confirmar)
        total_ocultos += len(r["ocultar"])
        total_quedan += len(r["quedan"])

    print("=" * 96)
    print(f"TOTAL en {len(cursos)} aulas  ·  se quedan {total_quedan}  ·  "
          f"{'ocultados' if args.confirmar else 'por ocultar'} {total_ocultos}")
    if not args.confirmar:
        print("\nEsto fue una simulación. Repite con --confirmar para aplicarlo.")
    else:
        print("\nPara deshacer un componente:  python config/moodle/cdigital.py mostrar <cmid>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
