# -*- coding: utf-8 -*-
"""Documentos del estudiante para los ítems REALES del aula (los 5 cursos CUN).

Salida (única convención, los 5 cursos):
  <Asignatura>/Clases/Recursos/ACAs/<Ítem del aula> (<peso>) - <qué es>.docx

Cada documento corresponde **1 a 1** a un ítem del libro de calificaciones de
CDigital (auditoría 2026-08-10), leído de `config/cursos/fechas_entrega_aca.py`.
Ya **no** existen los «ACA 1 / ACA 2 / ACA 3» de pregrado ni «EV05 / EXAM» de TG3:
el aula no los tiene. Tres familias de documento, distinguidas por ``kind``:

  kind="aca"          → la **tarea** documental: la que se sube (ACA Final; en
                        Proyecto I, ACA 1 y ACA FINAL). Lleva rúbrica y plantilla APA.
  kind="guia"         → guía de un **cuestionario** del aula (quices y parciales):
                        qué cubre, cómo prepararse, qué confirma el Docente. No se
                        sube documento.
  kind="instrumento"  → instructivo de **autoevaluación** (cuestionario) y
                        **coevaluación** (FORO: se participa, no se llena un
                        formulario). Existen en los CINCO cursos.

Nada de evaluación se escribe a mano aquí: peso, tipo de actividad, corte y
ventana salen de `fechas_entrega_aca`. Lo que no consta en ninguna fuente
(número de intentos, tiempo límite, tipo de pregunta) **no se inventa**: el
documento dice que lo confirma el Docente en la actividad del aula.

Consumidores:
  · `catalog_for_leeme(key)` devuelve **todo** el catálogo, con ``kind``, para que el
    LEEME de estudiantes (`sync_clases_estudiantes.leeme_md`) separe tareas / guías /
    instrumentos. ⚠️ Ese LEEME todavía filtra solo ``aca`` e ``instrumento``: hasta que
    se actualice, las **guías** de quices y parciales no salen listadas en su tabla
    (los .docx sí quedan en la carpeta).
  · `acas_for(key)` se conserva por compatibilidad y **excluye las guías** por defecto
    (``incluir_guias=True`` devuelve todo): quien hable de «ACAs» no debe recibir un
    cuestionario en la lista. La slide de evaluación de la Sesión 01 ya no lo usa: lee
    el modelo directamente (`build_sesion_material._evaluacion_rows`).

Lenguaje al estudiante: «el Docente» (sin nombre propio).
Sin .md en Clases/ — se genera .docx vía guion_md_a_docx.

Uso:
  python config/slides/build_acas_estudiantes.py
  python config/slides/build_acas_estudiantes.py proyecto1
"""
from __future__ import annotations

import os
import sys

# Consola de Windows en cp1252: sin esto, imprimir «→» en el resumen final aborta el
# build con UnicodeEncodeError DESPUÉS de haber escrito los .docx (defensa que ya
# tenían los demás builders del repo).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import tempfile
import unicodedata
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))

from sesiones_cun import COURSES, LINK_TUTORIAS, MSG_TUTORIAS_POR_GRUPO  # noqa: E402
from guion_md_a_docx import convert as md_to_docx  # noqa: E402
from fechas_entrega_aca import (  # noqa: E402
    IDS_INSTRUMENTO_CIERRE,
    KIND_CUESTIONARIO,
    KIND_FORO,
    KIND_LABEL,
    KIND_TAREA,
    REGLA_OFICIAL_P1,
    REGLA_RESUMEN,
    REGLA_VENTANAS_DOCENTE,
    componente,
    componentes_curso,
    desglose_corte_texto,
    entrega_por_id,
    entregas_curso,
    fmt_dmy,
    fmt_peso,
    peso_corte,
    texto_fecha_curso,
)
from carga_academica import curso as carga_curso  # noqa: E402

# Placeholder de respaldo: los usos por curso deben llamar a
from sesiones_cun import cdigital_url, CDIGITAL_PLACEHOLDER  # noqa: E402
# `cdigital_url(<clave del curso>)`, que devuelve la URL real del aula si existe
# en carga_academica_2026.json (auditadas el 2026-08-10) y el placeholder si no.
URL_CDIGITAL = CDIGITAL_PLACEHOLDER
APA_REL = "Recursos/Plantilla_APA_CUN_Proyecto de grado.docx"
ACAS_REL = "Recursos/ACAs"

# Familias de documento (valor de ``kind`` en el catálogo).
KIND_ACA = "aca"                  # tarea documental del aula
KIND_GUIA = "guia"                # guía de un cuestionario (quiz / parcial)
KIND_INSTRUMENTO = "instrumento"  # auto (cuestionario) / coevaluación (foro)

# Nombres anteriores que ya no corresponden a ningún ítem del aula. Se borran al
# regenerar para no dejar en manos de estudiantes un «ACA 2» que el libro de
# calificaciones no tiene. (Además, `_purge_obsoletos` limpia cualquier .docx de
# las familias generadas que ya no esté en el catálogo: p. ej. si cambia el peso
# que va en el nombre del archivo.)
LEGACY_FILENAMES = {
    "proyecto1": [
        "ACA Autoevaluacion.docx",     # → Autoevaluacion individual (4%) - instructivo.docx
        "ACA Coevaluacion.docx",       # → Coevaluacion individual (4%) - instructivo.docx
        "ACA 1 - Formulacion del problema.docx",          # el corte 1 del aula es un Quiz
        "ACA 2 - Fundamentacion referencial.docx",        # → ACA 1 (25%) del aula
        "ACA 3 - Diseno metodologico y anteproyecto final.docx",   # → ACA FINAL (42%)
    ],
    "investigacion": [
        "ACA 1 - Corte 1 - Fundamentos y primer avance.docx",
        "ACA 2 - Corte 2 - Pregunta y planteamiento.docx",
        "ACA 3 - Corte 3 - Fuentes marco y avance consolidado.docx",
    ],
    "creatividad": [
        "ACA 1 - Corte 1 - Problema oportunidad y base creativa.docx",
        "ACA 2 - Corte 2 - Tipologia gestion y validacion.docx",
        "ACA 3 - Corte 3 - Propuesta de Innovacion final.docx",
    ],
    "tg2": [
        "ACA 1 - Corte 1 - Delimitacion y formulacion.docx",
        "ACA 2 - Corte 2 - Marco referencial.docx",
        "ACA 3 - Corte 3 - Metodologia e integracion.docx",
    ],
    "tg3": [
        "ACA 1 - EV05 Proceso academico (articulo).docx",
        "ACA 2 - EXAM Sustentacion ante jurados.docx",
    ],
}

# Prefijos de archivo que este build gobierna (para limpiar renombrados).
_PREFIJOS_GENERADOS = ("ACA ", "Quiz", "Parcial", "Autoevaluacion", "Coevaluacion", "Guia ")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def write_md_as_docx(
    md_text: str,
    docx_path: str,
    *,
    subtitle: str | None = None,
    footer: str | None = None,
) -> None:
    fd, tmp = tempfile.mkstemp(suffix=".md", prefix="aca_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(md_text)
        md_to_docx(tmp, docx_path, brand=True, subtitle=subtitle, footer=footer)
    finally:
        if os.path.isfile(tmp):
            os.remove(tmp)


def _ascii(s: str) -> str:
    """«Autoevaluación» → «Autoevaluacion» (los nombres de archivo van sin tildes)."""
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch)
    )


def _cierre(course_key: str, item_id: str) -> date:
    """Cierre del ítem (grupo de referencia en cursos con ventanas por grupo)."""
    return entrega_por_id(course_key, item_id).entrega


def _cierres_texto(course_key: str, item_id: str) -> str:
    """«12/09» o «07/11 / 14/11» (TG3, cuando el cierre depende del grupo)."""
    data = entregas_curso(course_key)
    if isinstance(data, dict):
        fechas = sorted({e.entrega for items in data.values() for e in items if e.id == item_id})
        return " / ".join(fmt_dmy(d) for d in fechas)
    return fmt_dmy(_cierre(course_key, item_id))


def _cuestionarios(course_key: str) -> list[dict]:
    """Quices y parciales del aula (cuestionarios que NO son la autoevaluación)."""
    items = [
        c for c in componentes_curso(course_key)
        if c["kind"] == KIND_CUESTIONARIO and c["id"] not in IDS_INSTRUMENTO_CIERRE
    ]
    return sorted(items, key=lambda c: (_cierre(course_key, c["id"]), c["corte"]))


def _tareas(course_key: str) -> list[dict]:
    items = [c for c in componentes_curso(course_key) if c["kind"] == KIND_TAREA]
    return sorted(items, key=lambda c: (_cierre(course_key, c["id"]), c["corte"]))


def _items_del_corte(course_key: str, corte: int) -> list[dict]:
    return [c for c in componentes_curso(course_key) if int(c["corte"]) == int(corte)]


def _tareas_txt(course_key: str) -> str:
    """«la **ACA Final** (la tarea documental del curso)» / «las tareas … (A y B)»."""
    tareas = _tareas(course_key)
    if len(tareas) == 1:
        return f"la **{tareas[0]['code']}** (la tarea documental del curso)"
    codes = " y ".join(f"**{t['code']}**" for t in tareas)
    return f"las tareas documentales del curso ({codes})"


def _peso_item_txt(course_key: str, item_id: str, *, con_code: bool = True) -> str:
    """«**Parcial 1 = 24%** del curso (corte 1 = 30%, repartido entre 2 ítems)».

    Reemplaza los «esta ACA vale 30%» del material viejo: el 30% es el peso del
    CORTE y en el aula casi siempre lo reparten varios ítems (cuando no, se dice).
    """
    c = componente(course_key, item_id)
    n = len(_items_del_corte(course_key, c["corte"]))
    reparto = "es el único ítem del corte" if n == 1 else f"repartido entre {n} ítems"
    cabeza = f"**{c['code']} = {fmt_peso(c['weight'])}**" if con_code else f"**{fmt_peso(c['weight'])}**"
    return (
        f"{cabeza} de la nota del curso "
        f"(corte {c['corte']} = {fmt_peso(peso_corte(course_key, c['corte']))}, {reparto})"
    )


def _aviso_reparto_corte(course_key: str, item_id: str) -> str:
    """Frase honesta sobre el corte: depende de cuántos ítems lo compongan."""
    c = componente(course_key, item_id)
    otros = [x for x in _items_del_corte(course_key, c["corte"]) if x["id"] != item_id]
    if not otros:
        return (
            f"Es el **único** ítem del corte {c['corte']}: lo que saques aquí es la nota de ese "
            "corte. Revisa la tabla del punto 8 para ver cómo se compone el resto del curso."
        )
    lista = " + ".join(f"**{x['code']}** {fmt_peso(x['weight'])}" for x in otros)
    return (
        f"El corte {c['corte']} **no** se juega en un solo ítem: también lo componen {lista}. "
        "Revisa la tabla del punto 8 antes de sacar conclusiones sobre tu nota."
    )


def _tabla_items_md(course_key: str) -> str:
    """Tabla «así se califica el curso» tomada del libro de calificaciones."""
    lines = [
        "| Ítem en CDigital | Tipo | Corte | Peso | Cierre |",
        "| :--- | :--- | :---: | ---: | :--- |",
    ]
    for c in componentes_curso(course_key):
        lines.append(
            f"| **{c['code']}** | {KIND_LABEL[c['kind']]} | {c['corte']} | "
            f"{fmt_peso(c['weight'])} | {_cierres_texto(course_key, c['id'])} |"
        )
    lines.append("")
    lines.append(f"**Cortes:** {desglose_corte_texto(course_key)}.")
    return "\n".join(lines)


def _nota_curso_block(course_key: str, item_id: str, n: int) -> str:
    """Sección «dónde encaja en la nota», idéntica en los tres tipos de documento."""
    c = componente(course_key, item_id)
    return f"""## {n}. Dónde encaja en la nota del curso

Este documento corresponde a **un** ítem: **{c['code']}** ({KIND_LABEL[c['kind']]}, {fmt_peso(c['weight'])}). El resto de la nota lo registran los demás ítems del aula:

{_tabla_items_md(course_key)}

> Tabla generada del libro de calificaciones del aula (auditoría 2026-08-10). Si en CDigital ves un ítem distinto, **manda CDigital** y avísale al Docente.
"""


# ---------------------------------------------------------------------------
# Temario cubierto (se deriva del catálogo de sesiones + la ventana del ítem)
# ---------------------------------------------------------------------------
def _sesiones_dictadas(course_key: str) -> list[dict]:
    """Sesiones que **sí dictan tema** (la 01 es de encuadre), ordenadas por fecha."""
    out: list[dict] = []
    for s in COURSES[course_key].get("sesiones") or []:
        if s.get("presentacion"):
            continue
        try:
            f = datetime.strptime(str(s["fecha"]), "%d/%m/%Y").date()
        except Exception:
            continue
        out.append({"n": int(s["n"]), "titulo": s["titulo"], "fecha": f})
    return sorted(out, key=lambda x: x["fecha"])


def _lista_sesiones(sesiones: list[dict]) -> str:
    if not sesiones:
        return "- (todavía no se ha dictado tema antes de este cierre: revisa la lectura autónoma y lo publicado en CDigital)"
    return "\n".join(
        f"- **Sesión {s['n']:02d}** ({fmt_dmy(s['fecha'])}) — {s['titulo']}" for s in sesiones
    )


def _temario_block(course_key: str, item_id: str, n: int) -> str:
    """«Qué cubre» de un quiz/parcial: sesiones dictadas hasta su cierre.

    El alcance se **deriva** del calendario (no se inventa): todo lo trabajado en
    clase hasta la fecha de cierre del cuestionario, señalando qué se vio desde el
    cierre del cuestionario anterior. El detalle fino (número de preguntas, tipo,
    recorte de temas) lo publica el Docente en la actividad del aula.
    """
    cuest = _cuestionarios(course_key)
    ids = [c["id"] for c in cuest]
    pos = ids.index(item_id)
    cierre = _cierre(course_key, item_id)
    previo = cuest[pos - 1] if pos > 0 else None
    cierre_previo = _cierre(course_key, previo["id"]) if previo else None

    ses = _sesiones_dictadas(course_key)
    hasta = [s for s in ses if s["fecha"] <= cierre]
    nuevas = [s for s in hasta if cierre_previo is None or s["fecha"] > cierre_previo]

    if previo is None:
        detalle = (
            "Es el **primer** cuestionario del curso: entra todo lo trabajado hasta su cierre."
        )
    elif nuevas:
        rango = ", ".join(f"Sesión {s['n']:02d}" for s in nuevas)
        detalle = (
            f"**Nuevo desde el cierre de {previo['code']}** ({fmt_dmy(cierre_previo)}): {rango}. "
            "Lo anterior sigue siendo base — el curso es acumulativo."
        )
    else:
        detalle = (
            f"Entre el cierre de {previo['code']} ({fmt_dmy(cierre_previo)}) y este cierre no hay "
            "sesión nueva: el cuestionario recoge lo ya trabajado."
        )

    diferida = ""
    for s in COURSES[course_key].get("sesiones") or []:
        if s.get("presentacion") and s.get("unidad_diferida"):
            diferida = (
                f"\nLa **Sesión 01** fue de **encuadre** (no dictó tema). Su unidad quedó como "
                f"**lectura autónoma** y se retomó al abrir la Sesión 02, así que también hace "
                f"parte del temario: {s['unidad_diferida']}\n"
            )
            break

    return f"""## {n}. Qué cubre

Temario trabajado en clase **hasta el cierre** ({fmt_dmy(cierre)}):

{_lista_sesiones(hasta)}

{detalle}
{diferida}
> El **recorte exacto** de temas, el número de preguntas y el tipo de pregunta los publica **el Docente** en la actividad del aula. Este documento no los inventa: si CDigital dice otra cosa, manda CDigital.
"""


# ---------------------------------------------------------------------------
# Bloques comunes
# ---------------------------------------------------------------------------
def _header(course_key: str, item_id: str, curso: str, codigo: str, fuente: str) -> str:
    c = componente(course_key, item_id)
    return f"""# Enunciado para estudiantes — {c['code']}

**Curso:** {curso}
**Código:** {codigo}
**Ítem en CDigital:** **{c['code']}** · {KIND_LABEL[c['kind']]} · {fmt_peso(c['weight'])} de la nota (corte {c['corte']})
**Entrega oficial:** solo por **CDigital** ({cdigital_url(course_key)})
**Fuente curricular:** {fuente}

> Lee este enunciado completo antes de empezar. Si hay duda de peso, rúbrica o ventana de entrega, confirma con **el Docente** y con lo publicado en CDigital.

---
"""


def _header_guia(course_key: str, item_id: str, curso: str, codigo: str, fuente: str) -> str:
    c = componente(course_key, item_id)
    return f"""# Guía para estudiantes — {c['code']} ({KIND_LABEL[c['kind']]})

**Curso:** {curso}
**Código:** {codigo}
**Ítem en CDigital:** **{c['code']}** · {KIND_LABEL[c['kind']]} · {fmt_peso(c['weight'])} de la nota (corte {c['corte']})
**Qué haces:** resuelves el **{KIND_LABEL[c['kind']].lower()}** dentro de su ventana en **CDigital** ({cdigital_url(course_key)})
**No es una entrega documental:** no subes archivo y no usa la plantilla APA
**Fuente curricular:** {fuente}

> Esta guía es **orientación de estudio**. La actividad que califica es la del aula: lo que diga CDigital sobre intentos, tiempo y preguntas es lo que aplica.

---
"""


def _header_instrumento(course_key: str, item_id: str, curso: str, codigo: str,
                        fuente: str) -> str:
    """Encabezado de autoevaluación / coevaluación (NO son ACAs).

    El tipo real de la actividad sale del aula (auditoría 2026-08-10): la
    autoevaluación es un **cuestionario** y la coevaluación es un **foro**.
    """
    c = componente(course_key, item_id)
    verbo = (
        "**participas** en el foro" if c["kind"] == KIND_FORO
        else "**diligencias** la actividad"
    )
    return f"""# Instructivo para estudiantes — {c['code']} (instrumento individual de cierre)

**Curso:** {curso}
**Código:** {codigo}
**Ítem en CDigital:** **{c['code']}** · {KIND_LABEL[c['kind']]} · {fmt_peso(c['weight'])} de la nota (corte {c['corte']})
**Qué haces:** {verbo}, de forma **individual**, en **CDigital** ({cdigital_url(course_key)})
**No es una ACA:** no se sube documento, no usa la plantilla APA y no es entrega de equipo
**Fuente curricular:** {fuente}

> Existe en **los cinco cursos** del Docente, no solo en Proyecto I (así está creada en las aulas). Lo que cambia entre cursos es el **peso**.

---
"""


def _fecha_block(course_key: str, item_id: str) -> str:
    """Bloque de fecha del ítem. El título depende del tipo real de actividad."""
    c = componente(course_key, item_id)
    if c["id"] in IDS_INSTRUMENTO_CIERRE:
        titulo = (
            "Ventana para participar en el foro" if c["kind"] == KIND_FORO
            else "Ventana para diligenciarla"
        )
    elif c["kind"] == KIND_TAREA:
        titulo = "Fecha de entrega"
    else:
        titulo = "Ventana del cuestionario"
    return f"""## {titulo}

{texto_fecha_curso(course_key, item_id)}

"""


def _tools_block(*extra: str, n: int = 6) -> str:
    base = [
        "Google Docs / Word Online (abre la plantilla APA ahí; no se exige Office de escritorio)",
        "Google Scholar, SciELO, Redalyc, biblioteca virtual CUN",
        "ZoteroBib (https://zbib.org/) o citas nativas de Google Docs",
        "CDigital (entrega y retroalimentación)",
    ]
    base.extend(extra)
    lines = "\n".join(f"- {x}" for x in base)
    return f"""## {n}. Herramientas (solo gratis + nube)

{lines}

**No se exige** software de escritorio de pago ni instalaciones locales pesadas.
"""


def _relacion_block(texto: str, *, n: int, regla: str | None = None) -> str:
    """Cierre del documento: relación con las sesiones + de dónde salen las fechas."""
    return f"""## {n}. Relación con sesiones

{texto}

> Fechas de este documento: {regla or REGLA_RESUMEN}
"""


# ---------------------------------------------------------------------------
# Guías de cuestionario (quices y parciales) — se generan del modelo
# ---------------------------------------------------------------------------
def _guia_md(
    course_key: str,
    item_id: str,
    *,
    curso: str,
    codigo: str,
    fuente: str,
    preparacion: list[str],
    aviso_ventana: str = "",
    relacion: str,
    regla: str,
) -> str:
    c = componente(course_key, item_id)
    prep = "\n".join(f"- {x}" for x in preparacion)
    aviso = f"\n{aviso_ventana}\n" if aviso_ventana else ""
    return (
        _header_guia(course_key, item_id, curso, codigo, fuente)
        + f"""## 1. Qué es este documento (y qué NO es)

**{c['code']}** es un **{KIND_LABEL[c['kind']].lower()}** del aula: se resuelve **en CDigital**, dentro de su ventana, y la nota queda registrada al enviarlo.

- **No** es una entrega documental: no subes archivo ni usas la plantilla APA.
- **No** reemplaza {_tareas_txt(course_key)} ni al revés: son ítems distintos y todos pesan.
- Esta guía **no** es el cuestionario: es orientación para que estudies lo correcto.
{aviso}
## 2. Cuánto pesa y en qué corte

{_peso_item_txt(course_key, item_id)}.

{_aviso_reparto_corte(course_key, item_id)}

{_temario_block(course_key, item_id, 3)}
## 4. Formato: lo que confirma el Docente en el aula

Estos parámetros los define la actividad en CDigital y **este documento no los inventa**:

| Parámetro | Dónde se confirma |
| :--- | :--- |
| Número de intentos | Descripción de la actividad **{c['code']}** en CDigital |
| Tiempo límite | idem |
| Cantidad y tipo de preguntas | idem |
| Material permitido (a libro abierto o no) | idem |
| Si se puede retomar un intento interrumpido | idem |

**Antes de pulsar «Intentar»:** lee la descripción de la actividad. Por regla general, en un cuestionario con tiempo límite el reloj **empieza a correr al abrir el intento** y sigue corriendo aunque cierres el navegador.

**Requisitos técnicos:** navegador actualizado, sesión iniciada con tu **cuenta institucional CUN** y conexión estable. No resuelvas un cuestionario con tiempo desde una conexión que sabes inestable.

## 5. Cómo prepararte

{prep}
- Resuélvelo **sin** dejarlo para la última hora de la ventana: si algo falla, necesitas margen para avisarle al Docente.

## 6. Si no lo presentas

- El peso de **{c['code']}** ({fmt_peso(c['weight'])}) queda en **cero**: no hay trabajo extra que lo reemplace.
- La ventana cierra en la fecha indicada arriba y **no se reabre** por olvido.
- Si tienes una situación de fuerza mayor, escríbele al Docente **antes** del cierre. Supletorios y habilitaciones se rigen por el **Reglamento Estudiantil** y los define el programa: no los define este documento.

## 7. Integridad académica

- Es **individual**, salvo que la actividad diga expresamente otra cosa.
- Suplantación, copia o compartir preguntas y respuestas tiene **debido proceso** disciplinario.
- Si usas IA para estudiar, úsala para **entender**, no para transcribir: el cuestionario pregunta por comprensión.

{_nota_curso_block(course_key, item_id, 8)}
{_relacion_block(relacion, n=9, regla=regla)}"""
    )


# ---------------------------------------------------------------------------
# Instructivos de autoevaluación / coevaluación (los 5 cursos)
# ---------------------------------------------------------------------------
def _instrumento_md(
    course_key: str,
    item_id: str,
    *,
    curso: str,
    codigo: str,
    fuente: str,
    contexto: str,
    relacion: str,
    regla: str,
) -> str:
    c = componente(course_key, item_id)
    es_foro = c["kind"] == KIND_FORO
    tarea = _tareas(course_key)[-1]["code"]
    otro_id = "coev" if item_id == "auto" else "auto"
    otro = componente(course_key, otro_id)

    if es_foro:
        que_es = (
            f"**{c['code']}** es un **foro** del aula (así está creada la actividad en "
            f"CDigital): **participas publicando tu aporte**, en el que valoras el trabajo "
            f"colaborativo y los aportes de tus compañeros con criterio académico y respeto."
        )
        no_es = [
            "**No** es un formulario de preguntas: es un **foro**. Si no publicas, no participaste.",
            "**No** se sube documento ni se usa la plantilla APA: no hay archivo que entregar.",
            "**No** la publica un vocero por el equipo: cada quien escribe su propio aporte.",
            f"**No** sustituye la **{tarea}** ni cambia la calificación de las entregas documentales.",
        ]
        pasos = [
            "Revisa en CDigital el **aviso de apertura** de la ventana (lo publica el Docente).",
            f"Entra al **foro «{c['code']}»** del aula y lee la consigna y la escala publicadas.",
            "**Publica tu aporte** siguiendo esa consigna (una intervención por estudiante, salvo que el Docente pida réplicas).",
            "Valora **hechos** del trabajo conjunto: entregas cumplidas, reparto de tareas, calidad de los aportes. Nunca la persona.",
            "Recuerda que el foro **lo leen otros**: escribe lo que sostendrías de frente, con respeto.",
            "Verifica que tu mensaje quedó **publicado** dentro de la ventana (en un foro, un borrador sin enviar no cuenta).",
        ]
        evidencia = "tu **participación publicada en el foro** (queda con fecha y hora)"
        canal = f"**CDigital (Moodle)** — foro **«{c['code']}»** del aula. Único canal válido."
        checklist = [
            "Publicaste **tú** tu aporte en el foro, dentro de la ventana",
            "La valoración es respetuosa y está fundamentada en el trabajo del equipo",
            f"Tienes claro que **no** reemplaza ni compensa la **{tarea}**",
        ]
    else:
        que_es = (
            f"**{c['code']}** es un **cuestionario** del aula: **lo diligencias tú**, de forma "
            f"individual, para valorar tu propia trayectoria en el periodo (compromiso, aportes "
            f"y avance del producto del curso)."
        )
        no_es = [
            "**No** se sube documento ni se usa la plantilla APA: no hay archivo que entregar.",
            "**No** es grupal: no la diligencia un vocero por el equipo.",
            f"**No** sustituye la **{tarea}** ni compensa una entrega no hecha o con baja nota.",
            "**No es** la autoevaluación institucional SIAC (acreditacion.cun.edu.co): esa no suma nota en este curso.",
        ]
        pasos = [
            "Revisa en CDigital el **aviso de apertura** de la ventana (lo publica el Docente).",
            f"Entra a la actividad **«{c['code']}»** del aula.",
            "Diligénciala **con honestidad**, según tu participación real en el periodo (no según lo que hubieras querido hacer).",
            "**Envía** dentro de la ventana; conserva acuse o captura si el aula lo permite.",
            "Dudas sobre los ítems o la escala: pregunta al Docente **antes** del cierre, no después.",
        ]
        evidencia = "la actividad **completada** en CDigital (queda con fecha y hora)"
        canal = f"**CDigital (Moodle)** — actividad **«{c['code']}»** del aula. Único canal válido."
        checklist = [
            "La diligenciaste **tú**, dentro de la ventana",
            "Las respuestas son coherentes con tu participación real",
            f"Tienes claro que **no** reemplaza ni compensa la **{tarea}**",
        ]

    no_es_md = "\n".join(f"- {x}" for x in no_es)
    pasos_md = "\n".join(f"{i}. {x}" for i, x in enumerate(pasos, 1))
    checklist_md = "\n".join(f"  - [ ] {x}" for x in checklist)

    return (
        _header_instrumento(course_key, item_id, curso, codigo, fuente)
        + f"""## 1. Qué es este documento (y qué NO es)

**{c['code']}** · **{fmt_peso(c['weight'])}** de la nota del curso · corte {c['corte']} · instrumento individual de cierre.

{que_es}

{no_es_md}

{contexto}

Con **{otro['code']}** ({KIND_LABEL[otro['kind']]}, {fmt_peso(otro['weight'])}) forman los **dos** instrumentos individuales que cierran el corte {c['corte']}: son actividades distintas y cada una tiene su propia ventana. Hacer una no cuenta como haber hecho la otra.

## 2. Quién, dónde y cuándo

| Pregunta | Respuesta |
| :--- | :--- |
| **¿Quién?** | **Cada estudiante, de forma individual.** Nadie lo hace por otro. |
| **¿Dónde?** | En el aula del curso en **CDigital** ({cdigital_url(course_key)}), actividad «{c['code']}». Ningún otro canal cuenta. |
| **¿Cuándo?** | Solo dentro de la **ventana** indicada arriba. El Docente la habilita al abrir y la cierra al terminar. |
| **¿Qué queda como evidencia?** | {evidencia.capitalize()}. |

## 3. Paso a paso

{pasos_md}

## 4. Qué pasa si no lo haces

- Ese **{fmt_peso(c['weight'])}** queda en **cero**: no hay entregable alternativo ni trabajo extra que lo reemplace.
- La ventana cierra en la fecha indicada y **no se reabre**: la nota debe quedar registrada antes del cierre de notas del periodo.
- Si tienes una situación de fuerza mayor, escríbele al Docente **antes** del cierre de la ventana.

## 5. Evidencia y registro de la nota

- La **evidencia oficial** es {evidencia}.
- El Docente habilita la ventana, verifica el cumplimiento y registra el **{fmt_peso(c['weight'])}** en el libro de calificaciones antes del cierre de notas.
- Checklist rápido:
{checklist_md}

## 6. Canal y requisitos

- {canal}
- Navegador actualizado y sesión iniciada con tu **cuenta institucional CUN**.
- No requiere instalar nada, ni pagar, ni usar la plantilla APA (no hay documento que subir).

{_nota_curso_block(course_key, item_id, 7)}
{_relacion_block(relacion, n=8, regla=regla)}"""
    )


# ---------------------------------------------------------------------------
# Catálogos por curso
# ---------------------------------------------------------------------------
def _doc(
    course_key: str,
    item_id: str,
    *,
    kind: str,
    title: str,
    md: str,
    source: str,
    slug: str | None = None,
) -> dict:
    """Fila del catálogo. El nombre de archivo se **deriva** del ítem del aula."""
    c = componente(course_key, item_id)
    peso = fmt_peso(c["weight"])
    code = _ascii(c["code"])
    if kind == KIND_INSTRUMENTO:
        filename = f"{code} individual ({peso}) - instructivo.docx"
    elif kind == KIND_GUIA:
        filename = f"{code} ({peso}) - guia del cuestionario.docx"
    else:
        filename = f"{code} ({peso}) - {slug or _ascii(title)}.docx"
    return {
        "item": item_id,
        "code": c["code"],
        "title": title,
        "filename": filename,
        "weight": peso,
        "tipo": KIND_LABEL[c["kind"]],
        "corte": c["corte"],
        "source": source,
        "kind": kind,
        "md": md,
    }


# ---------- PROYECTO I 54ES4 ----------
def docs_proyecto1() -> list[dict]:
    key = "proyecto1"
    fuente = (
        "ESP329 (Art. 41: nota única del periodo) · **libro de calificaciones del aula "
        f"(CDigital, auditoría 2026-08-10):** {desglose_corte_texto(key)} · "
        "ventanas del **cronograma oficial de Coordinación (AFI)** · Manual del Docente / "
        "Instructivo Proyecto I (contenido de cada entrega)"
    )
    curso = "PROYECTO I — Especialización en Inteligencia Artificial"
    codigo = "ESP329"
    regla = REGLA_OFICIAL_P1

    quiz = _guia_md(
        key, "quiz", curso=curso, codigo=codigo, fuente=fuente,
        preparacion=[
            "Repasa el deck y tus apuntes de cada sesión (`Clases/Sesion NN - …/Presentacion.pptx`).",
            "Ten claros los **fundamentos de investigación** de la unidad diferida (lectura autónoma de la Sesión 01).",
            "Distingue con tus palabras **problema, pregunta, objetivo general y objetivos específicos**: es lo que más se confunde.",
            "Repasa qué hace **viable** una pregunta en el alcance de Proyecto I → Proyecto II (se **diseña**, no se aplica).",
            "Revisa las **líneas de IA** del programa y por qué tu tema encaja en una.",
        ],
        aviso_ventana=(
            "> **Ojo con la ventana:** la fija la **Coordinación** (cronograma AFI) y abre "
            "**antes** de que el tema se trabaje en clase. Revisa el temario del punto 3 antes "
            "de abrir el intento: puedes resolverlo cualquier día de la ventana, no hace falta "
            "hacerlo el primero."
        ),
        relacion=(
            "El tema entra con la **Sesión 02** (problema y pregunta de investigación); la "
            "**Sesión 03** (objetivos, justificación, alcances) cae **después** del cierre, así "
            "que para el Quiz apóyate en la Sesión 02, en la lectura autónoma y en la **tutoría "
            "acordada de la semana**. La **Sesión 01** fue de encuadre."
        ),
        regla=regla,
    )

    aca1 = (
        _header(key, "aca1", curso, codigo, fuente)
        + f"""## 1. Qué es y cuánto pesa

**ACA 1 — Formulación del problema y fundamentación referencial** · {_peso_item_txt(key, 'aca1', con_code=False)}.

Es la **primera de las dos tareas documentales** del curso: se sube en CDigital y se califica con rúbrica. La segunda es la **ACA FINAL** (anteproyecto integrado). El corte 1 **no** tiene tarea: lo califica el **Quiz** ({fmt_peso(componente(key, 'quiz')['weight'])}).

## 2. Propósito / competencia que evalúa

Delimitar una situación problemática pertinente al campo de la especialización y sostenerla con literatura: problema, pregunta, objetivos, justificación, alcances y limitaciones (ESP329 U2–U3) **más** el marco referencial (U4).

Macrocompetencia ESP329: formular un anteproyecto pertinente mediante delimitación del problema, revisión crítica inicial y definición de objetivos.

## 3. Consigna (paso a paso)

Trabajo **por equipo** (máx. 3 integrantes, según AFI). Un solo integrante sube la entrega grupal en CDigital.

1. Acuerda con tu equipo el tema/línea de IA y el contexto de aplicación.
2. Redacta el **planteamiento del problema** (situación actual, evidencias, por qué importa).
3. Formula la **pregunta de investigación** (clara, viable en el alcance de Proyecto I→II).
4. Escribe el **objetivo general** y los **objetivos específicos** (verbos medibles, alineados a la pregunta).
5. Desarrolla la **justificación** (teórica, práctica y/o social, según aplique).
6. Define **alcances y limitaciones** del estudio.
7. Elabora **antecedentes** (mínimo **6**, nacionales e internacionales) alineados a tu pregunta.
8. Desarrolla el **marco teórico** (bases alineadas a variables/categorías), el **marco conceptual** (definiciones operativas) y el **marco contextual** (dónde se aplica); añade **marco legal** si aplica.
9. Verifica que el marco «responda» a la pregunta: no es un listado desconectado.
10. Cierra con **referencias en APA 7** (citas en texto + lista final).

## 4. Producto entregable

- Documento en **Plantilla APA CUN – Proyecto de Grado** (`{APA_REL}`), preferible en Google Docs.
- Portada con nombres completos de **todos** los integrantes.
- Extensión orientativa: **12–20 páginas** de cuerpo (formulación + marco referencial), sin contar portada ni referencias.
- Formato: PDF o DOCX según indique CDigital.
- **No** recolectes datos ni apliques instrumentos en Proyecto I.

## 5. Criterios de evaluación / checklist (ESP329)

- [ ] Coherencia entre problema, pregunta y objetivos
- [ ] Pertinencia del problema al campo / líneas del programa
- [ ] Justificación argumentada (no solo opinión)
- [ ] Alcances y limitaciones realistas
- [ ] Antecedentes ≥ 6 (nacionales e internacionales)
- [ ] Marco teórico, conceptual y contextual pertinentes y actualizados
- [ ] Escritura académica e integridad (citas, sin plagio)
- [ ] Referencias APA 7

{_tools_block(
    "ZoteroBib / Google Docs para citas",
    "Biblioteca virtual CUN + Scholar / SciELO / Redalyc",
    f"Formulario de asistencia a tutorías (estudiante): {LINK_TUTORIAS}",
    MSG_TUTORIAS_POR_GRUPO,
)}
{_nota_curso_block(key, "aca1", 7)}
{_relacion_block(
    "La formulación se trabaja en **Sesiones 02–03**; el marco referencial en "
    "**Sesiones 04–07** (retro · antecedentes · teórico · conceptual/contextual · legal y APA). "
    "La **Sesión 07** (28/09) es la última sincrónica antes del cierre.",
    n=8, regla=regla,
)}"""
    )

    aca_final = (
        _header(key, "aca_final", curso, codigo, fuente)
        + f"""## 1. Qué es y cuánto pesa

**ACA FINAL — Anteproyecto integrado** · {_peso_item_txt(key, 'aca_final', con_code=False)}.

Es la **entrega de cierre** del curso: el anteproyecto completo, no un fragmento. Junto con la **Autoevaluación** ({fmt_peso(componente(key, 'auto')['weight'])}) y la **Coevaluación** ({fmt_peso(componente(key, 'coev')['weight'])}) cierra el corte {componente(key, 'aca_final')['corte']}.

## 2. Propósito / competencia que evalúa

Integrar el **anteproyecto completo** (ESP329 U5–U7): metodología **diseñada** (no aplicada), planeación/viabilidad e integración coherente del documento. Producto de cierre de Proyecto I y base para Proyecto II.

## 3. Consigna (paso a paso)

1. Incorpora **todas** las correcciones de la **ACA 1** (trazabilidad visible en el documento).
2. Completa la **metodología**: paradigma/enfoque, tipo y alcance, diseño, población/muestra o unidades de análisis, variables/categorías, técnicas e **instrumentos propuestos** (no aplicados), plan de análisis, ética.
3. Elabora **cronograma** y **presupuesto** (o recursos) viables para la continuidad del proyecto.
4. Integra todo el anteproyecto en un solo documento coherente (de portada a referencias).
5. Revisa integridad académica (similitud, citas, uso transparente de IA si la usaste).
6. Prepara el envío final grupal en CDigital.

## 4. Producto entregable

- **Anteproyecto FINAL integrado** (no un fragmento suelto) en plantilla APA CUN (`{APA_REL}`).
- Extensión orientativa: documento completo típico de anteproyecto de especialización (U2–U7).
- Instrumentos solo **propuestos** (anexos opcionales); **sin** recolección de datos en Proyecto I.
- Un solo envío grupal; portada con todos los integrantes.

## 5. Criterios de evaluación / checklist (ESP329)

- [ ] Correcciones de la ACA 1 incorporadas
- [ ] Metodología coherente con pregunta y objetivos
- [ ] Instrumentos propuestos (no aplicados)
- [ ] Cronograma y presupuesto/viabilidad
- [ ] Coherencia global del anteproyecto
- [ ] Escritura, fuentes, integridad y viabilidad

{_tools_block(
    f"Tutorías: registra asistencia en {LINK_TUTORIAS}",
    MSG_TUTORIAS_POR_GRUPO,
)}
{_nota_curso_block(key, "aca_final", 7)}
{_relacion_block(
    "Puente metodológico en **Sesión 08**; desarrollo en **Sesiones 09–10** (la 10 es la última "
    "sincrónica antes del cierre); integración y evaluación en **Sesión 11**. Usa las tutorías "
    "acordadas en la semana: en esta fase hay pocas sesiones sincrónicas.",
    n=8, regla=regla,
)}"""
    )

    contexto_p1 = (
        "**Contexto:** en Proyecto I la nota es **única** (Art. 41 Reglamento Estudiantil) y este "
        "instrumento vale **{peso}** (ESP329 · «MECANISMOS Y ESTRATEGIAS DE EVALUACIÓN»). Es "
        "obligatorio al cierre de Proyecto I (cronograma AFI / Instructivo Proyecto I)."
    )
    auto = _instrumento_md(
        key, "auto", curso=curso, codigo=codigo, fuente=fuente,
        contexto=contexto_p1.format(peso=fmt_peso(componente(key, "auto")["weight"])),
        relacion=(
            "Se comenta en la **Sesión 11** (integración y evaluación). La ventana abre después "
            "de la ACA FINAL, en la fase final del periodo."
        ),
        regla=regla,
    )
    coev = _instrumento_md(
        key, "coev", curso=curso, codigo=codigo, fuente=fuente,
        contexto=contexto_p1.format(peso=fmt_peso(componente(key, "coev")["weight"])),
        relacion=(
            "Se comenta en la **Sesión 11**. Su ventana cierra **antes** que la de la "
            "autoevaluación (fechas oficiales del periodo)."
        ),
        regla=regla,
    )

    return [
        _doc(key, "quiz", kind=KIND_GUIA,
             title="Corte 1 · fundamentos, problema y pregunta", md=quiz, source=fuente),
        _doc(key, "aca1", kind=KIND_ACA,
             title="Formulación del problema y fundamentación referencial",
             slug="Formulacion del problema y fundamentacion referencial",
             md=aca1, source=fuente),
        _doc(key, "aca_final", kind=KIND_ACA,
             title="Anteproyecto integrado", slug="Anteproyecto integrado",
             md=aca_final, source=fuente),
        _doc(key, "coev", kind=KIND_INSTRUMENTO,
             title="Coevaluación individual (instructivo)", md=coev, source=fuente),
        _doc(key, "auto", kind=KIND_INSTRUMENTO,
             title="Autoevaluación individual (instructivo)", md=auto, source=fuente),
    ]


# ---------- Bloques compartidos por los 4 cursos de pregrado ----------
def _contexto_pregrado(course_key: str, item_id: str, codigo_fuente: str) -> str:
    c = componente(course_key, item_id)
    return (
        f"**Contexto:** el curso se califica en **tres cortes** (Art. 52) y este instrumento "
        f"vale **{fmt_peso(c['weight'])}** dentro del corte {c['corte']}. Está creado así en el "
        f"aula ({codigo_fuente}); no es un añadido de este documento."
    )


def _guias_pregrado(
    course_key: str,
    *,
    curso: str,
    codigo: str,
    fuente: str,
    preparacion: list[str],
    relaciones: dict[str, str],
) -> list[dict]:
    """Una guía por cuestionario del aula (Quiz 1/2/3, Parcial 1/2)."""
    out = []
    for c in _cuestionarios(course_key):
        md = _guia_md(
            course_key, c["id"], curso=curso, codigo=codigo, fuente=fuente,
            preparacion=preparacion,
            relacion=relaciones.get(c["id"], ""),
            regla=REGLA_VENTANAS_DOCENTE,
        )
        out.append(
            _doc(course_key, c["id"], kind=KIND_GUIA,
                 title=f"Corte {c['corte']} · {KIND_LABEL[c['kind']].lower()} del aula",
                 md=md, source=fuente)
        )
    return out


def _instrumentos_pregrado(
    course_key: str,
    *,
    curso: str,
    codigo: str,
    fuente: str,
    codigo_fuente: str,
    relacion: str,
) -> list[dict]:
    out = []
    for item_id, title in (
        ("auto", "Autoevaluación individual (instructivo)"),
        ("coev", "Coevaluación individual (instructivo)"),
    ):
        md = _instrumento_md(
            course_key, item_id, curso=curso, codigo=codigo, fuente=fuente,
            contexto=_contexto_pregrado(course_key, item_id, codigo_fuente),
            relacion=relacion, regla=REGLA_VENTANAS_DOCENTE,
        )
        out.append(_doc(course_key, item_id, kind=KIND_INSTRUMENTO, title=title,
                        md=md, source=fuente))
    return out


def _ruta_cortes_block(course_key: str, etapas: list[tuple[int, str, str]], n: int) -> str:
    """«Ruta de trabajo por cortes»: avances formativos + quién pone la nota del corte.

    ``etapas`` = [(corte, título del avance, qué se produce)]. La nota de cada corte
    la registran los ítems reales del aula, así que el texto los nombra: sin esto el
    estudiante lee «avance del corte 1» y cree que hay una entrega calificada ahí.
    """
    lines = [f"## {n}. Ruta de trabajo (avances por corte)", ""]
    lines.append(
        "En el aula **no** hay una tarea por corte: la única tarea documental es la "
        f"**{_tareas(course_key)[-1]['code']}**. Los avances de abajo son **formativos**: se "
        "revisan en clase o en tutoría y son los que hacen posible la entrega final. La **nota** "
        "de cada corte la registran los ítems que aparecen entre paréntesis."
    )
    lines.append("")
    for corte, titulo, produce in etapas:
        items = [
            f"{c['code']} {fmt_peso(c['weight'])}"
            for c in componentes_curso(course_key) if c["corte"] == corte
        ]
        lines.append(
            f"- **Corte {corte} — {titulo}.** {produce} "
            f"*(la nota del corte la ponen: {' + '.join(items)})*"
        )
    lines.append("")
    lines.append(
        "> Llegar a la entrega final sin los avances es la forma más común de perderla: el "
        "documento es acumulativo."
    )
    return "\n".join(lines)


# ---------- INVESTIGACIÓN 53339 ----------
def docs_investigacion() -> list[dict]:
    key = "investigacion"
    fuente = (
        "Syllabus SIAC EI005_PRES · Art. 52: Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%. "
        f"**Libro de calificaciones del aula (CDigital, auditoría 2026-08-10):** "
        f"{desglose_corte_texto(key)}. Producto del curso: artículo de nuevo conocimiento, que "
        "se entrega como **ACA Final** (única tarea calificada); quices y parciales son "
        "**cuestionarios** del aula."
    )
    curso = "INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA — Escuela de Ingenierías"
    codigo = "EI005"
    regla = REGLA_VENTANAS_DOCENTE

    aca_final = (
        _header(key, "aca_final", curso, codigo, fuente)
        + f"""## 1. Qué es y cuánto pesa

**ACA Final — Artículo de nuevo conocimiento** · {_peso_item_txt(key, 'aca_final', con_code=False)}.

Es la **única entrega documental calificada** del curso: el artículo/protocolo consolidado que venías construyendo desde la primera semana. Los quices y parciales de los cortes 1 y 2 son cuestionarios; aquí se califica el **documento**.

## 2. Propósito / competencia que evalúa

Aplicar el método científico a un problema de tu entorno dentro de una de las **6 líneas de Ingeniería** (MinCiencias) y sostener por escrito problema, pregunta y revisión de literatura (Syllabus U1–U8 · U10–U12).

{_ruta_cortes_block(key, [
    (1, "tema, línea y 1.er avance",
     "Elige la temática y la línea (IoT, Big Data, IA, cloud/FinTech, aplicaciones, telemática) y escribe el primer avance: portada, introducción breve, problema tentativo y fuentes iniciales."),
    (2, "pregunta y planteamiento del problema",
     "Analiza causas (espina de pescado, árbol de problemas o método 3D), formula la pregunta y redacta el planteamiento completo: estado actual, evidencias, causas y posibles vías de solución."),
    (3, "fuentes, marco y consolidación",
     "Busca en biblioteca CUN + Scholar / SciELO / Redalyc, organiza citas con ZoteroBib, arma la matriz de fuentes y redacta el avance de marco teórico / revisión de literatura."),
], 3)}

## 4. Consigna (qué debe contener la entrega)

1. **Título** y datos de autoría.
2. **Introducción**: tema, línea de Ingeniería elegida y motivación.
3. **Problema y pregunta**: planteamiento con evidencias y causas; pregunta clara y viable.
4. **Objetivos** (si tu ruta los exige) alineados a la pregunta.
5. **Marco teórico / revisión de literatura** en progreso, con la **matriz de fuentes** (autor, año, aporte, relación con tu pregunta) como sección o anexo.
6. **Referencias en APA 7**: citas en texto + lista final.
7. **Incorpora** la retroalimentación recibida en los cortes anteriores.

## 5. Producto entregable

- Documento consolidado en plantilla APA CUN (`{APA_REL}`) o estructura equivalente en Google Docs.
- Extensión orientativa: **10–15 páginas** acumuladas (avance realista del periodo corto).
- Nombre sugerido: `INV_ACAFinal_Apellido`.
- Formato: PDF o DOCX según indique CDigital.

## 6. Criterios de evaluación / checklist

- [ ] Línea de Ingeniería explícita y pertinente
- [ ] Problema argumentado con evidencias
- [ ] Pregunta clara y viable
- [ ] Fuentes confiables y matriz de fuentes completa
- [ ] Marco/revisión alineado a la pregunta (no un listado desconectado)
- [ ] Citas y referencias APA 7 · integridad académica
- [ ] Mejoras respecto a los avances previos

{_tools_block("ZoteroBib (zbib.org)", "Biblioteca virtual CUN (login institucional)", n=7)}
{_nota_curso_block(key, "aca_final", 8)}
{_relacion_block(
    "Se construye a lo largo de **Sesiones 02–05** y se cierra en la fecha de recepción de "
    "trabajos. La **Sesión 06** (bases de datos CUN · gestores de citas · marco teórico y "
    "revisión, que concentra U8+U10–12 por periodo corto) cae **después** del cierre: sirve de "
    "refuerzo y para el **Quiz 3**, no es requisito de esta entrega. La **Sesión 01** fue de encuadre.",
    n=9, regla=regla,
)}"""
    )

    prep = [
        "Repasa el deck y tus apuntes de cada sesión (`Clases/Sesion NN - …/Presentacion.pptx`).",
        "Ten a mano la **lectura autónoma de la Sesión 01** (fundamentos del método científico) y lo que el Docente publique en CDigital.",
        "Ten claro cómo distinguir **tipos de conocimiento**, **tipos de fuente** y qué hace confiable una fuente.",
        "Repasa las **6 líneas de Ingeniería** de MinCiencias y en cuál se ubica tu tema.",
        "Ten claro con tus palabras: **problema ≠ pregunta ≠ objetivo**, y qué es una pregunta viable.",
    ]
    relaciones = {
        "quiz1": "Cierra el día de la **Sesión 02** (MinCiencias · 6 líneas de Ingeniería): entra esa sesión y la lectura autónoma de la Sesión 01.",
        "parcial1": "Cierra el día de la **Sesión 03** (prueba parcial · 1.er avance del artículo): es el parcial del corte 1 y acumula lo trabajado hasta ahí.",
        "quiz2": "Cierra el día de la **Sesión 04** (identificación de problemas y pregunta de investigación).",
        "parcial2": "Cierra el día de la **Sesión 05** (formulación del planteamiento del problema): cierra el corte 2 junto con el Quiz 2.",
        "quiz3": "Cierra el día de la **Sesión 06** (bases de datos CUN · gestores de citas · marco teórico y revisión, U8+U10–12): es el último cuestionario del curso.",
    }

    docs = [_doc(key, "aca_final", kind=KIND_ACA,
                 title="Artículo de nuevo conocimiento",
                 slug="Articulo de nuevo conocimiento", md=aca_final, source=fuente)]
    docs += _guias_pregrado(key, curso=curso, codigo=codigo, fuente=fuente,
                            preparacion=prep, relaciones=relaciones)
    docs += _instrumentos_pregrado(
        key, curso=curso, codigo=codigo, fuente=fuente,
        codigo_fuente="Syllabus SIAC EI005_PRES + libro de calificaciones",
        relacion=(
            "Van al final del periodo, después de la recepción de trabajos y antes del cierre "
            "de notas. La **Sesión 06** es la última sesión sincrónica del curso."
        ),
    )
    return docs


# ---------- CREATIVIDAD 54408 ----------
def docs_creatividad() -> list[dict]:
    key = "creatividad"
    fuente = (
        "Syllabus SIAC EI004_VIR · Art. 52: Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%. "
        f"**Libro de calificaciones del aula (CDigital, auditoría 2026-08-10):** "
        f"{desglose_corte_texto(key)}. Producto conductor: Propuesta de Innovación (desde la "
        "semana 1), que se entrega como **ACA Final** (única tarea calificada); quices y "
        "parciales son **cuestionarios** del aula."
    )
    curso = "CREATIVIDAD Y PENSAMIENTO INNOVADOR — Escuela de Ingenierías"
    codigo = "EI004"
    regla = REGLA_VENTANAS_DOCENTE

    aca_final = (
        _header(key, "aca_final", curso, codigo, fuente)
        + f"""## 1. Qué es y cuánto pesa

**ACA Final — Propuesta de Innovación** · {_peso_item_txt(key, 'aca_final', con_code=False)}.

Es la **única entrega documental calificada** del curso: la Propuesta de Innovación consolidada, del problema–oportunidad hasta la vigilancia tecnológica. Los quices y parciales son cuestionarios; aquí se califica el **documento**.

## 2. Propósito / competencia que evalúa

Convertir una oportunidad detectada en una **propuesta de innovación** tipificada, validada y situada en su ecosistema (Syllabus U1–U8).

{_ruta_cortes_block(key, [
    (1, "problema–oportunidad y base creativa",
     "Completa la ficha problema–oportunidad (usuario concreto, dolor, evidencia, tipo tentativo Oslo, valor esperado), el mapa de utilidad / bloqueadores–ensanchadores y una ideación con al menos 3 ideas; elige la semilla de tu propuesta."),
    (2, "tipología, gestión y validación",
     "Tipifica la innovación (producto, proceso, organización, marketing, social) con cuadro comparativo y valida con FODA + Canvas (BMC) + definición de MVP; prepara un pitch breve."),
    (3, "vigilancia tecnológica y cierre",
     "Haz una vigilancia tecnológica breve (tendencias, patentes/documentos, referentes), identifica entidades de apoyo pertinentes e integra todo el recorrido en un solo documento."),
], 3)}

## 4. Consigna (qué debe contener la entrega)

1. **Problema–oportunidad**: usuario concreto, dolor y evidencia observable.
2. **Propuesta de valor** y **tipo(s) de innovación** justificados con el Manual de Oslo / OCDE.
3. **Validación**: FODA + Canvas (BMC) + **MVP** definido y verificable.
4. **Vigilancia tecnológica**: tendencias, referentes o patentes, con fuentes citadas.
5. **Ecosistema**: entidades de apoyo (locales, nacionales o internacionales) pertinentes.
6. **Siguiente paso** realista de la propuesta.
7. **Pitch de 1 página** (Docs / Slides / Canva free) como anexo o sección.
8. **Referencias** de todo lo que citaste.

## 5. Producto entregable

- **Propuesta de Innovación consolidada** (documento) + pitch de 1 página.
- Extensión orientativa: **8–12 páginas** de documento.
- Nombre sugerido: `CRE_ACAFinal_Apellido`.
- La ficha de la Sesión 01 (`Ficha_problema_oportunidad.docx`, en la carpeta de esa sesión) es insumo válido.

## 6. Criterios de evaluación / checklist

- [ ] Usuario y problema concretos (no genéricos)
- [ ] Tipo de innovación bien justificado (Oslo)
- [ ] FODA y Canvas coherentes con el problema
- [ ] MVP claro y verificable
- [ ] Vigilancia tecnológica con fuentes
- [ ] Entidades de apoyo identificadas
- [ ] Pitch claro · presentación cuidada · integridad académica

{_tools_block(
    "Excalidraw / tldraw / Miro free",
    "Canvanizer (BMC)",
    "Google Scholar / Google Patents (web)",
    "Canva free (opcional, para el pitch)",
    n=7,
)}
{_nota_curso_block(key, "aca_final", 8)}
{_relacion_block(
    "Se construye a lo largo de **Sesiones 02–06** (Design Thinking e ideación · Oslo · tipos de "
    "innovación · FODA/Canvas/MVP · vigilancia tecnológica). La **Sesión 06** es la última antes "
    "del cierre; la **Sesión 07** (innovación local–internacional · entidades de apoyo) cierra el "
    "curso **después** de la recepción y sirve de refuerzo. La **Sesión 01** fue de encuadre.",
    n=9, regla=regla,
)}"""
    )

    prep = [
        "Repasa el deck y tus apuntes de cada sesión (`Clases/Sesion NN - …/Presentacion.pptx`).",
        "Ten a mano la **lectura autónoma de la Sesión 01** (Propuesta de Innovación · creatividad e inteligencia emocional).",
        "Distingue **creatividad** de **innovación** y **pensamiento divergente** de **convergente**, con ejemplos propios.",
        "Repasa los **tipos de innovación** del Manual de Oslo / OCDE y para qué sirve cada herramienta (Design Thinking, FODA, Canvas, MVP, vigilancia tecnológica).",
        "Ten fresca **tu propia propuesta**: varios ítems se responden mejor pensando en tu caso.",
    ]
    relaciones = {
        "quiz1": "Cierra el día de la **Sesión 02** (creatividad/innovación en I+D · Design Thinking y técnicas de ideación).",
        "parcial1": "Cierra el día de la **Sesión 03** (gestión de la innovación · Manual de Oslo / OCDE): es el parcial del corte 1.",
        "quiz2": "Cierra el día de la **Sesión 04** (tipos de innovación).",
        "parcial2": "Cierra el día de la **Sesión 05** (análisis de negocios · validación: FODA, Canvas, MVP): cierra el corte 2.",
        "quiz3": "Cierra el día de la **Sesión 06** (vigilancia tecnológica): es el último cuestionario del curso.",
    }

    docs = [_doc(key, "aca_final", kind=KIND_ACA,
                 title="Propuesta de Innovación", slug="Propuesta de Innovacion",
                 md=aca_final, source=fuente)]
    docs += _guias_pregrado(key, curso=curso, codigo=codigo, fuente=fuente,
                            preparacion=prep, relaciones=relaciones)
    docs += _instrumentos_pregrado(
        key, curso=curso, codigo=codigo, fuente=fuente,
        codigo_fuente="Syllabus SIAC EI004_VIR + libro de calificaciones",
        relacion=(
            "Van al final del periodo, después de la recepción de trabajos y antes del cierre de "
            "notas. La **Sesión 07** es la última sesión del curso."
        ),
    )
    return docs


# ---------- TG2 54448 ----------
def docs_tg2() -> list[dict]:
    key = "tg2"
    fuente = (
        "Manual del Docente TG2 (⚠️ sin Syllabus SIAC en carpeta) · Art. 52: tres cortes "
        f"30/30/40. **Libro de calificaciones del aula (CDigital, auditoría 2026-08-10):** "
        f"{desglose_corte_texto(key)} — ya verificado en el aula, no orientativo. Producto: "
        "avance consolidado del proyecto/artículo hacia TG3, que se entrega como **ACA Final** "
        "(única tarea calificada); quices y parciales son **cuestionarios** del aula. Plantilla APA CUN."
    )
    curso = "TRABAJO DE GRADO 2 — Modelos de Innovación (Ing. Sistemas)"
    codigo = "94453"
    regla = REGLA_VENTANAS_DOCENTE

    aca_final = (
        _header(key, "aca_final", curso, codigo, fuente)
        + f"""## 1. Qué es y cuánto pesa

**ACA Final — Avance consolidado hacia TG3** · {_peso_item_txt(key, 'aca_final', con_code=False)}.

Es la **única entrega documental calificada** del curso: el avance de tu trabajo de grado integrado y listo para continuar en **Trabajo de Grado 3**. Los quices y parciales son cuestionarios; aquí se califica el **documento**.

## 2. Propósito / competencia que evalúa

Retomar el proyecto de semestres anteriores, delimitarlo, sostenerlo con literatura y dejar **diseñada** la metodología, de modo que TG3 pueda ejecutar y sustentar.

{_ruta_cortes_block(key, [
    (1, "delimitación y formulación",
     "Diagnostica el estado del proyecto (qué tienes / qué falta), delimita o reformula el problema, formula pregunta, objetivos y título provisional, y arma la estructura del documento en plantilla APA CUN."),
    (2, "marco referencial",
     "Amplía antecedentes y referentes (Fase I) con bases CUN + Scholar y avanza marco teórico, conceptual y contextual, con referencias APA 7 al día."),
    (3, "metodología e integración",
     "Completa enfoque, tipo, alcance y diseño metodológico propuesto, define instrumentos y plan de análisis (propuestos), integra el documento y cierra con un apartado «listo para TG3»."),
], 3)}

## 4. Consigna (qué debe contener la entrega)

1. **Título provisional**, problema delimitado y **pregunta** de investigación.
2. **Objetivos** general y específicos, alineados a la pregunta.
3. **Antecedentes / referentes** pertinentes al campo de Ingeniería de Sistemas.
4. **Marco teórico, conceptual y contextual** articulados a la pregunta.
5. **Diseño metodológico propuesto**: enfoque, tipo, alcance, diseño.
6. **Instrumentos y plan de análisis** propuestos (no aplicados en TG2).
7. Apartado **«listo para TG3»**: qué queda por ejecutar y por sustentar.
8. **Referencias APA 7** y trazabilidad de las correcciones recibidas.

## 5. Producto entregable

- Avance consolidado en `{APA_REL}` (ábrelo en Google Docs).
- Extensión orientativa: documento integrado del avance TG2 (típicamente **18–30 páginas**).
- Nombre sugerido: `TG2_ACAFinal_Apellido`.

## 6. Criterios de evaluación / checklist

- [ ] Estado del proyecto y delimitación explícitos
- [ ] Problema, pregunta y objetivos coherentes
- [ ] Antecedentes y marcos pertinentes y actualizados
- [ ] Metodología propuesta coherente con la pregunta
- [ ] Instrumentos y plan de análisis definidos (propuestos)
- [ ] Documento integrado (no fragmentos pegados)
- [ ] Preparación explícita para TG3 · APA 7 · integridad académica

{_tools_block("ZoteroBib", "Biblioteca CUN / Scholar", n=7)}
{_nota_curso_block(key, "aca_final", 8)}
{_relacion_block(
    "Se construye a lo largo de **Sesiones 02–11**: formulación (02–04), marcos (05–06), "
    "metodología e instrumentos (07–08), integración y correcciones (09), socialización (10) y "
    "cierre/preparación para TG3 (11). La **Sesión 11** (09/11) es la última sincrónica antes de "
    "la recepción. La **Sesión 01** fue de encuadre y allí se firmó el acuerdo pedagógico.",
    n=9, regla=regla,
)}"""
    )

    prep = [
        "Repasa el deck y tus apuntes de cada sesión (`Clases/Sesion NN - …/Presentacion.pptx`).",
        "Ten a mano la **lectura autónoma de la Sesión 01** (delimitación / reformulación del tema).",
        "Ten claras las **partes del documento de grado** y qué va en cada una (problema, marcos, metodología, instrumentos, plan de análisis).",
        "Repasa **APA 7**: cita en texto, referencia final y qué constituye plagio.",
        "Piensa las respuestas **sobre tu propio proyecto**: varios ítems se responden mejor con tu caso a la vista.",
    ]
    relaciones = {
        "quiz1": "Cierra el día de la **Sesión 03** (estructura del documento / artículo de avance). Recuerda que el 17/08 fue clase autónoma por festivo.",
        "parcial1": "Cierra el día de la **Sesión 05** (marco teórico — avance): es el parcial del corte 1 y acumula desde la Sesión 02.",
        "quiz2": "Cierra el día de la **Sesión 07** (diseño metodológico propuesto).",
        "parcial2": "Cierra el día de la **Sesión 08** (instrumentos y plan de análisis propuestos): cierra el corte 2.",
        "quiz3": "Cierra el día de la **Sesión 10** (socialización de avances): es el último cuestionario del curso.",
    }

    docs = [_doc(key, "aca_final", kind=KIND_ACA,
                 title="Avance consolidado hacia TG3", slug="Avance consolidado hacia TG3",
                 md=aca_final, source=fuente)]
    docs += _guias_pregrado(key, curso=curso, codigo=codigo, fuente=fuente,
                            preparacion=prep, relaciones=relaciones)
    docs += _instrumentos_pregrado(
        key, curso=curso, codigo=codigo, fuente=fuente,
        codigo_fuente="Manual del Docente TG2 + libro de calificaciones",
        relacion=(
            "Van en la fase de cierre, alrededor de la **Sesión 11** y de la recepción de "
            "trabajos, antes del cierre de notas."
        ),
    )
    return docs


# ---------- TG3 54450 / 54466 / 54467 ----------
def docs_tg3() -> list[dict]:
    key = "tg3"
    fuente = (
        "Syllabus SIAC 94532 (declara «corte único 100%: EV05 50% + EXAM 50%») frente al "
        "**libro de calificaciones del aula (CDigital, auditoría 2026-08-10), que es el que "
        f"califica:** {desglose_corte_texto(key)}. El artículo se entrega como **ACA Final** "
        "(tarea); la sustentación ante jurados sigue siendo requisito del proceso pero **no "
        "tiene ítem propio** en el aula. Artículo ≥ 50 referencias y ≥ 4.000 palabras. "
        "Cierre: póster, antiplagio, repositorio."
    )
    curso = "TRABAJO DE GRADO 3 — Modelos de Innovación (Ing. Sistemas)"
    codigo = "94532"
    regla = REGLA_VENTANAS_DOCENTE

    aca_final = (
        _header(key, "aca_final", curso, codigo, fuente)
        + f"""## 1. Qué es y cuánto pesa

**ACA Final — Artículo de investigación** · {_peso_item_txt(key, 'aca_final', con_code=False)}.

Es la **única entrega documental calificada** del curso. Ojo con el Syllabus: dice «corte único 100% (EV05 + EXAM)», pero **el aula califica en tres cortes** (ver punto 9) y **EV05/EXAM no existen** como ítems. La **sustentación ante jurados** sigue siendo requisito del proceso de grado (punto 7) aunque no tenga ítem propio en el libro de calificaciones.

**Tu fecha depende del grupo:** el 54450 recibe una semana antes que el 54466 y el 54467 (ver arriba).

## 2. Propósito / competencia que evalúa

Desarrollar y consolidar el **artículo resultado de investigación** (o investigación-creación) con calidad argumentativa, bajo acompañamiento del Docente (Syllabus U1–U14).

{_ruta_cortes_block(key, [
    (1, "formulación y estructura del artículo",
     "Retoma o define el proyecto, formula pregunta, objetivos y título, y redacta introducción y estructura del artículo en plantilla APA CUN (contexto, problema, pregunta, objetivos)."),
    (2, "referentes, metodología y análisis",
     "Desarrolla las fases de referentes, diseña el instrumento o el prototipado/obra-creación, ejecuta tu ruta metodológica y trabaja el análisis de datos y la experiencia creativa."),
    (3, "cierre del artículo y alistamiento",
     "Cierra marco teórico, resultados y discusión, resumen, palabras clave UNESCO, conclusiones y referencias; alista póster, evidencias/anexos y la verificación antiplagio institucional."),
], 3)}

## 4. Consigna (qué debe contener la entrega)

1. **Título**, resumen y **palabras clave UNESCO**.
2. **Introducción**: contexto, problema, pregunta y objetivos.
3. **Marco teórico / referentes** (fases completas) articulados a la pregunta.
4. **Metodología** e instrumento (o prototipado / obra-creación) efectivamente trabajados.
5. **Resultados y discusión**, con relación explícita a los referentes.
6. **Conclusiones** y **referencias**: mínimo **50**, en APA 7.
7. **Anexos/evidencias** y **póster** según indique el Docente.
8. **Verificación antiplagio** institucional realizada antes de la sustentación.

## 5. Producto entregable

- Artículo en plantilla APA CUN (`{APA_REL}`).
- Requisitos del Syllabus: **≥ 50 referencias** · **≥ 4.000 palabras**.
- Póster + evidencias para anexos (formato que indique el Docente).
- Nombre sugerido: `TG3_ACAFinal_Articulo_Apellido`.

## 6. Criterios de evaluación / checklist

- [ ] Coherencia problema–pregunta–objetivos–método–resultados
- [ ] Revisión bibliográfica rigurosa (≥ 50 referencias)
- [ ] Extensión ≥ 4.000 palabras
- [ ] APA 7 e integridad académica (antiplagio verificado)
- [ ] Resultados y discusión sostenidos en evidencia
- [ ] Póster y evidencias listos

## 7. Sustentación ante jurados (requisito del proceso, sin ítem propio en el aula)

La sustentación **no** aparece como ítem del libro de calificaciones, pero **sí** es parte del proceso de grado: la evalúan los pares/jurados que asigna la Dirección del Programa (Syllabus U13) y su preparación se refleja en la calidad de este artículo.

1. Confirma **fecha, modalidad y requisitos** con el Docente / el programa.
2. Prepara la exposición: póster + síntesis del artículo (problema, método, hallazgos, aporte).
3. Ensaya tiempos y respuestas a preguntas de jurados.
4. Realiza la **sustentación**.
5. Carga los **entregables al repositorio institucional** según el checklist oficial (Syllabus U14).

- [ ] Dominio del contenido del artículo
- [ ] Claridad y argumentación en la defensa
- [ ] Material visual (póster) adecuado
- [ ] Entregables de repositorio completos

{_tools_block(
    "ZoteroBib",
    "Google Slides / Canva free (póster)",
    "Herramienta antiplagio institucional (ruta oficial del semestre en CDigital — no inventar URL)",
    "CDigital / repositorio institucional",
    n=8,
)}
{_nota_curso_block(key, "aca_final", 9)}
{_relacion_block(
    "Proceso a lo largo de **Sesiones 02–11** (formulación → referentes → instrumento → análisis "
    "→ cierre del artículo → póster y antiplagio). **Sesión 12** = sustentación ante jurados · "
    "**Sesión 13** = entregables para repositorio · **Sesiones 14–15** son buffer de calendario "
    "(el grupo 54450 no tiene la Sesión 15). La **Sesión 01** fue de encuadre y allí se firmó el "
    "acuerdo pedagógico.",
    n=10, regla=regla,
)}"""
    )

    prep = [
        "Repasa el deck y tus apuntes de cada sesión (`Clases/Sesion NN - …/Presentacion.pptx`).",
        "Ten a mano la **lectura autónoma de la Sesión 01** (casos de éxito · retomar el proyecto · contexto y planteamiento).",
        "Ten claras las **partes del artículo científico** (resumen, introducción, referentes, metodología, resultados, discusión, conclusiones) y qué va en cada una.",
        "Repasa **APA 7** (cita, referencia, parafraseo) y qué cuenta como plagio.",
        "Piensa las respuestas **sobre tu propio artículo**: varios ítems se responden mejor con tu caso a la vista.",
    ]
    relaciones = {
        "quiz1": "Cierra el día de la **Sesión 03** (estructura del artículo · taller de introducción).",
        "parcial1": "Cierra el día de la **Sesión 06** (comunidades de práctica y co-creación): es el parcial del corte 1 y acumula desde la Sesión 02.",
        "quiz2": "Cierra el día de la **Sesión 08** (Fase III de referentes · cierre del marco teórico).",
        "parcial2": "Cierra el día de la **Sesión 10** (resumen, palabras clave UNESCO, conclusiones y referencias): cierra el corte 2.",
        "quiz3": "Cierra el día de la **Sesión 12** (sustentación ante jurados): es el último cuestionario del curso.",
    }

    docs = [_doc(key, "aca_final", kind=KIND_ACA,
                 title="Artículo de investigación", slug="Articulo de investigacion",
                 md=aca_final, source=fuente)]
    docs += _guias_pregrado(key, curso=curso, codigo=codigo, fuente=fuente,
                            preparacion=prep, relaciones=relaciones)
    docs += _instrumentos_pregrado(
        key, curso=curso, codigo=codigo, fuente=fuente,
        codigo_fuente="Syllabus SIAC 94532 + libro de calificaciones",
        relacion=(
            "Van en la fase de cierre, tras la sustentación (**Sesión 12**) y los entregables de "
            "repositorio (**Sesión 13**). **Las fechas dependen de tu grupo:** el 54450 cierra "
            "una semana antes que el 54466 y el 54467."
        ),
    )
    return docs


DOCS_BY_COURSE = {
    "proyecto1": docs_proyecto1,
    "investigacion": docs_investigacion,
    "creatividad": docs_creatividad,
    "tg2": docs_tg2,
    "tg3": docs_tg3,
}
# Alias histórico (algunos builds lo importaban por nombre).
ACAS_BY_COURSE = DOCS_BY_COURSE


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------
def documentos_for(key: str) -> list[dict]:
    """Catálogo completo del curso, en orden cronológico de cierre del ítem."""
    items = DOCS_BY_COURSE[key]()
    for a in items:
        a.setdefault("kind", KIND_ACA)
    return sorted(items, key=lambda a: (_cierre(key, a["item"]), a["corte"], a["code"]))


def acas_for(key: str, *, incluir_guias: bool = False) -> list[dict]:
    """Catálogo para consumidores que hablan de «ACAs».

    Por defecto **excluye las guías** de quices y parciales: así la slide «LAS ACAs»
    de la Sesión 01 sigue listando solo las tareas documentales (``kind="aca"``) y
    rotulando aparte los instrumentos de cierre (``kind="instrumento"``), sin
    llamar «ACA» a un cuestionario. Con ``incluir_guias=True`` devuelve todo.
    """
    items = documentos_for(key)
    if incluir_guias:
        return items
    return [a for a in items if a["kind"] != KIND_GUIA]


def catalog_for_leeme(key: str) -> list[dict]:
    """Filas para el LEEME de estudiantes — **todos** los documentos del curso.

    Cada ítem: ``{code, title, rel, fecha, weight, kind, tipo, corte, item}``.
    ``kind`` separa las tres familias (``aca`` / ``guia`` / ``instrumento``) y
    ``fecha`` es el cierre del ítem REAL del aula (en TG3, las fechas de los dos
    calendarios de grupo separadas por « / »).
    """
    out = []
    for a in documentos_for(key):
        out.append({
            "code": a["code"],
            "title": a["title"],
            "rel": f"{ACAS_REL}/{a['filename']}",
            "fecha": _cierres_texto(key, a["item"]),
            "weight": a["weight"],
            "kind": a["kind"],
            "tipo": a["tipo"],
            "corte": a["corte"],
            "item": a["item"],
        })
    return out


def _inject_fecha(md: str, course_key: str, item_id: str) -> str:
    """Inserta el bloque de fecha justo después del encabezado (primer `---`)."""
    bloque = _fecha_block(course_key, item_id)
    if "\n---\n" in md:
        pre, post = md.split("\n---\n", 1)
        return pre + "\n---\n\n" + bloque + post.lstrip("\n")
    return bloque + md


_SUBTITULO = {
    KIND_ACA: "Enunciado de entrega (tarea del aula)",
    KIND_GUIA: "Guía de cuestionario del aula",
    KIND_INSTRUMENTO: "Instrumento individual de cierre (no es una ACA)",
}


def _purge_obsoletos(out_dir: Path, key: str, escritos: set[str]) -> list[str]:
    """Borra los .docx que este build gobierna y que ya no están en el catálogo.

    Dos vías, complementarias:
      · `LEGACY_FILENAMES` — renombrados conocidos (documenta el cambio).
      · barrido por prefijo — cualquier «ACA … / Quiz … / Parcial … / Auto… / Coev…»
        que sobre, p. ej. si cambia el peso que va en el nombre del archivo.
    Nunca toca otros tipos de archivo (`desktop.ini` de Drive, PDFs del Docente).
    """
    borrados: list[str] = []
    for name in LEGACY_FILENAMES.get(key, ()):
        old = out_dir / name
        if old.is_file() and name not in escritos:
            old.unlink()
            borrados.append(name)
            print("RM obsoleto", old)
    for p in sorted(out_dir.glob("*.docx")):
        if p.name in escritos or p.name in borrados:
            continue
        if p.name.startswith(_PREFIJOS_GENERADOS):
            p.unlink()
            borrados.append(p.name)
            print("RM obsoleto", p)
    return borrados


def build_course(key: str) -> list[str]:
    if key not in DOCS_BY_COURSE:
        raise KeyError(key)
    c = COURSES[key]
    cc = carga_curso(key)
    out_dir = Path(c["folder"]) / "Clases" / "Recursos" / "ACAs"
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for a in documentos_for(key):
        path = out_dir / a["filename"]
        etiqueta = _SUBTITULO[a["kind"]]
        subtitle = f"{etiqueta} · {cc['titulo_corto']}"
        footer = f"CUN · {cc['titulo_corto']} · {etiqueta} · Vigilada Mineducación"
        md = _inject_fecha(a["md"], key, a["item"])
        write_md_as_docx(md, str(path), subtitle=subtitle, footer=footer)
        written.append(str(path))
        print("OK", a["kind"].upper(), key, a["filename"])
    for p in out_dir.glob("*.md"):
        p.unlink()
        print("RM", p)
    _purge_obsoletos(out_dir, key, {Path(p).name for p in written})
    return written


def main(argv: list[str] | None = None) -> None:
    argv = list(argv or sys.argv[1:])
    keys = argv if argv else list(DOCS_BY_COURSE.keys())
    resultado: dict[str, list[str]] = {}
    for key in keys:
        resultado[key] = build_course(key)
    print()
    print("=== Clases/Recursos/ACAs/ por curso ===")
    for key, paths in resultado.items():
        docs = {d["filename"]: d for d in documentos_for(key)}
        print(f"\n{key} · {carga_curso(key)['titulo_corto']}")
        for p in paths:
            name = Path(p).name
            d = docs[name]
            print(
                f"  [{d['kind']:11}] {name}"
                f"   → {d['code']} ({d['tipo']}, {d['weight']}, corte {d['corte']}) "
                f"cierra {_cierres_texto(key, d['item'])}"
            )
    print(
        "\nListo: un documento por ítem evaluable del aula. Las guías de quices y parciales "
        "no inventan intentos ni tiempo límite: los confirma el Docente en CDigital."
    )


if __name__ == "__main__":
    main()
