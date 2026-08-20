# -*- coding: utf-8 -*-
"""Reescribe la **sección de evaluación** y el bloque de **fechas** de los Manuales del
Docente de PREGRADO desde `fechas_entrega_aca` (libro de calificaciones de CDigital).

Por qué existe: los cuatro manuales de pregrado tenían la tabla **congelada** con el
reparto por pesos que se abandonó el 2026-08-10. Ningún build vivo los regeneraba
(el único consumidor de `resumen_tabla_markdown` era un script archivado que ya ni
siquiera corre: apuntaba a nombres de carpeta inexistentes), así que Creatividad e
Investigación anunciaban al docente fechas **7 días antes** de las que ya estaban en
los enunciados del estudiante.

Ampliado el 2026-08-10: además de las fechas, este script escribe la **sección 3
(Evaluación)** de cada manual. Antes estaba a mano y afirmaba tres cosas que la
auditoría del aula desmintió — «cada ACA evalúa el 100% de su corte», «ACA 1/2/3 = un
entregable por corte» y, en TG3, «corte único 100% = EV05 50% + EXAM 50%». Al generarla
desde el modelo, ningún ítem, tipo ni peso vuelve a copiarse a mano.

Qué hace, por manual:
  1. Sustituye el bloque `## 3. Evaluación…` (hasta el siguiente `## `) por la sección
     generada: cortes, tabla de ítems por corte y lo que queda anulado.
  2. Sustituye el bloque `## Fechas de entrega ACA…` por `resumen_tabla_markdown()`.

Uso:
    python config/cursos/sync_manuales_fechas.py            # los 4 de pregrado
    python config/cursos/sync_manuales_fechas.py creatividad

Proyecto I NO se toca aquí: su manual lleva una tabla propia con el puente
«componente del material ↔ ítem del aula», curada a mano contra el cronograma oficial
de Coordinación (que es la tabla `VENTANAS["proyecto1"]` del módulo de fechas).
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from carga_academica import workspace_root  # noqa: E402
from fechas_entrega_aca import (  # noqa: E402
    componentes_curso,
    cortes_curso,
    fmt_peso,
    peso_corte,
    resumen_tabla_markdown,
)

MANUALES = {
    "creatividad": "Pregrado/Creatividad y pensamiento innovador/"
                   "Manual del Docente - Creatividad y Pensamiento Innovador.md",
    "investigacion": "Pregrado/Investigacion en ciencia y tecnologia/"
                     "Manual del Docente - Investigacion Ciencia y Tecnologia.md",
    "tg2": "Pregrado/Trabajo de grado 2/Manual del Docente - Trabajo de Grado 2.md",
    "tg3": "Pregrado/Trabajo de grado 3/Manual del Docente - Trabajo de Grado 3.md",
}

HEADING = "## Fechas de entrega ACA / cortes"
HEADING_EVAL = "## 3. Evaluación — estructura REAL del aula (CDigital)"

# Líneas propias de cada curso que la sección de evaluación conserva (producto,
# ruta de enunciados, avisos que no salen del modelo).
NOTAS_CURSO: dict[str, list[str]] = {
    "creatividad": [
        "**Producto documental del curso:** la **Propuesta de Innovación**, hilo conductor "
        "desde la Sesión 02. Es lo que se entrega como **ACA Final** (tarea) en el tercer corte.",
        "**Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem "
        "del aula** (guía de cada quiz y parcial, enunciado de la ACA Final, instructivo de "
        "auto y coevaluación). Regenerar: "
        "`python config/slides/build_acas_estudiantes.py creatividad`.",
    ],
    "investigacion": [
        "**Producto documental del curso:** avance del **artículo / proyecto de "
        "investigación** (formato `Plantilla_APA_CUN_Proyecto de grado.docx`). Es lo que se "
        "entrega como **ACA Final** (tarea) en el tercer corte.",
        "**Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem "
        "del aula** (guía de cada quiz y parcial, enunciado de la ACA Final, instructivo de "
        "auto y coevaluación). Regenerar: "
        "`python config/slides/build_acas_estudiantes.py investigacion`.",
        "La **prueba escrita parcial** que el Syllabus pide en U5 y U11–12 ya tiene dónde "
        "vivir: son los **Parcial 1 y Parcial 2** del aula (24% y 21%).",
    ],
    "tg2": [
        "**Producto documental del curso:** avance consolidado del **documento** de grado "
        "(`Plantilla_APA_CUN_Proyecto de grado.docx`), que se entrega como **ACA Final** "
        "(tarea) en el tercer corte.",
        "**Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem "
        "del aula**, incluidas las guías de los quices y parciales.",
        "⚠️ Sigue faltando el **Syllabus SIAC**, pero los pesos **ya no son orientativos**: "
        "salen del libro de calificaciones del aula. Lo que falta del SIAC es el **temario**, "
        "no la evaluación.",
    ],
    "tg3": [
        "**Producto documental del curso:** el **documento** de grado —por defecto, "
        "*artículo resultado de investigación*— (≥ 50 referencias, ≥ 4.000 palabras) + "
        "sustentación ante jurados + carga a repositorio. Se entrega como **ACA Final** "
        "(tarea) en el tercer corte. Otras modalidades cumplen los mismos mínimos.",
        "**Enunciados para estudiantes:** `Clases/Recursos/ACAs/` — **un documento por ítem "
        "del aula**. Los antiguos «ACA 1 (EV05)» y «ACA 2 (EXAM)» se refundieron en el "
        "enunciado de la **ACA Final**, que es el único entregable documental del aula.",
        "La **sustentación ante jurados** sigue siendo obligatoria (Sesión 12) y se califica "
        "dentro de la **ACA Final**: en el aula no existe un ítem «EXAM» separado.",
    ],
}

# Lo que la sección de evaluación deja explícitamente anulado, por curso.
ANULADO_COMUN = [
    "**No hay tres ACAs.** El aula tiene **una sola «ACA Final»** (tarea) en el tercer "
    "corte. Los antiguos enunciados ACA 1 / ACA 2 / ACA 3 no correspondían a tres ítems del "
    "libro de calificaciones; ya se rehicieron como **un documento por ítem real** "
    "(2026-08-10).",
    "**Queda anulada la regla «cada ACA evalúa el 100% de su corte»** (decisión del "
    "2026-08-10, derogada el mismo día por la auditoría): el desglose real existe y está en "
    "la tabla de arriba.",
    "**Autoevaluación y coevaluación SÍ hacen parte de la nota de este curso** — no son "
    "exclusivas de Proyecto I. La **coevaluación es un FORO** (se participa, no se entrega "
    "documento) y la **autoevaluación un cuestionario**.",
    # OJO con el nombre del archivo: en disco es «guia», SIN tilde (así lo escribe
    # build_acas_estudiantes.py). Escribirlo con tilde deja una ruta colgada en los
    # cuatro manuales de pregrado a la vez.
    "**Los quices y parciales existen y pesan.** El **Parcial 1 vale 24%** por sí solo. Ya "
    "tienen guía para el estudiante en `Clases/Recursos/ACAs/` (`Quiz N (…) - guia del "
    "cuestionario.docx` · `Parcial N (…) - guia del cuestionario.docx`), pero en el aula "
    "**existen solo como ítem del libro de calificaciones**: falta **crear la actividad** "
    "(cuestionario + banco de preguntas) antes de su ventana.",
]
ANULADO_EXTRA: dict[str, list[str]] = {
    "tg3": [
        "**TG3 no es «corte único = 100%».** El Syllabus 94532 decía corte único con "
        "**EV05 50% + EXAM 50%**; el aula tiene **tres cortes 30/30/40** y ni EV05 ni EXAM "
        "existen como ítems. Manda el aula.",
    ],
}


def seccion_evaluacion(key: str) -> str:
    """Sección 3 del manual, generada desde el libro de calificaciones."""
    cortes = cortes_curso(key)
    resumen_cortes = " · ".join(
        f"**Corte {c} = {fmt_peso(peso_corte(key, c))}**" for c in cortes
    )
    lines = [
        HEADING_EVAL,
        "",
        "**Fuente:** libro de calificaciones del aula en CDigital (auditoría 2026-08-10), "
        "cargado en `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — regenerar "
        f"con `python config/cursos/sync_manuales_fechas.py {key}`.",
        "",
        f"Régimen: **Art. 52 · tres cortes** — {resumen_cortes}. Configúralo así en CDigital: "
        "estos son los ítems que **ya existen** en el libro de calificaciones, con este tipo "
        "de actividad y este peso.",
        "",
        "| Corte | Ítem en el aula | Tipo de actividad | Peso |",
        "| :---: | :--- | :--- | ---: |",
    ]
    for c in cortes:
        items = [x for x in componentes_curso(key) if int(x["corte"]) == c]
        for j, comp in enumerate(items):
            corte_cell = f"**{c}** ({fmt_peso(peso_corte(key, c))})" if j == 0 else ""
            tipo = {"cuestionario": "Cuestionario", "tarea": "Tarea", "foro": "Foro"}[comp["kind"]]
            lines.append(
                f"| {corte_cell} | **{comp['code']}** | {tipo} | {fmt_peso(comp['weight'])} |"
            )
    lines += ["", "### Qué desmiente esto del material anterior", ""]
    for b in ANULADO_COMUN + ANULADO_EXTRA.get(key, []):
        lines.append(f"- {b}")
    lines += ["", "### Notas de este curso", ""]
    for b in NOTAS_CURSO.get(key, []):
        lines.append(f"- {b}")
    lines += [
        "",
        "Ventanas (apertura · cierre · límite de nota) y en qué sesión cae cada cuestionario: "
        "«Fechas de entrega ACA / cortes» más abajo y "
        "`Calendario de clases (oficial).md` → «Evaluación en el aula».",
        "",
        "",  # línea en blanco antes del `## ` siguiente (el lookahead no la consume)
    ]
    return "\n".join(lines)


def bloque(key: str) -> str:
    return (
        f"{HEADING}\n"
        "\n"
        "Fuente en vivo: `config/cursos/fechas_entrega_aca.py`. **No editar a mano** — "
        f"regenerar con `python config/cursos/sync_manuales_fechas.py {key}`.\n"
        "\n"
        f"{resumen_tabla_markdown(key)}\n"
        "\n"
    )


def sync(key: str) -> bool:
    path = workspace_root() / MANUALES[key]
    text = io.open(path, encoding="utf-8").read()
    original = text
    cambios: list[str] = []

    pat_eval = re.compile(r"^## 3\. Evaluación.*?(?=^## )", re.S | re.M)
    if pat_eval.search(text):
        nuevo = pat_eval.sub(lambda _m: seccion_evaluacion(key), text, count=1)
        if nuevo != text:
            cambios.append("sección 3 (Evaluación)")
        text = nuevo
    else:
        print(f"AVISO {path.name}: no encontré la sección «## 3. Evaluación» — sin cambios ahí")

    pat = re.compile(r"^## Fechas de entrega ACA.*?(?=^## )", re.S | re.M)
    if pat.search(text):
        nuevo = pat.sub(lambda _m: bloque(key), text, count=1)
        if nuevo != text:
            cambios.append("tabla de fechas")
        text = nuevo
    else:
        print(f"AVISO {path.name}: no encontré el bloque de fechas — sin cambios ahí")

    if text == original:
        print(f"OK {path.name} (ya estaba al día)")
        return False
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print(f"OK {path.name} — actualizado: {', '.join(cambios)}")
    return True


def main(argv: list[str] | None = None) -> None:
    argv = list(argv if argv is not None else sys.argv[1:])
    keys = [a for a in argv if a in MANUALES] or list(MANUALES)
    for k in keys:
        sync(k)


if __name__ == "__main__":
    main()
