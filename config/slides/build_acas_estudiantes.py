# -*- coding: utf-8 -*-
"""Genera enunciados ACA (.docx) para estudiantes en los 5 cursos CUN.

Convención (única, los 5):
  <Asignatura>/Clases/Recursos/ACAs/ACA N - <título corto>.docx

Excepción — Proyecto I: además de las **tres** ACAs, la carpeta lleva dos
documentos que **no son ACAs**: los instructivos de la **autoevaluación (4%)**
y la **coevaluación (4%)**, instrumentos individuales que cada estudiante
*diligencia* en CDigital al cierre (no llevan prefijo «ACA» ni son entregables
con rúbrica). Se distinguen por ``kind``:

  kind="aca"          → enunciado de entregable evaluado (ACA 1/2/3, EV05/EXAM)
  kind="instrumento"  → instructivo de instrumento individual de cierre

Fuente de pesos/estructura: syllabus / Manual (no inventar % que contradigan).
ESP329: ACA 1 25% · ACA 2 25% · ACA 3 42% · autoevaluación 4% · coevaluación 4%
(las ACAs son tres; auto/coev son instrumentos, no una cuarta y quinta ACA).
Lenguaje al estudiante: «el Docente» (sin nombre propio).
Sin .md en Clases/ — se genera .docx vía guion_md_a_docx.

Uso:
  python config/slides/build_acas_estudiantes.py
  python config/slides/build_acas_estudiantes.py proyecto1
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))

from sesiones_cun import COURSES, LINK_TUTORIAS, MSG_TUTORIAS_POR_GRUPO  # noqa: E402
from guion_md_a_docx import convert as md_to_docx  # noqa: E402
from fechas_entrega_aca import (  # noqa: E402
    REGLA_OFICIAL_P1,
    REGLA_RESUMEN,
    REGLA_VENTANAS_DOCENTE,
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

# id de fechas_entrega_aca.py → cada documento del catálogo.
# Los `code` coinciden con `ACA_COMPONENTES` de config/cursos/fechas_entrega_aca.py
# (allí auto/coev ya están marcados kind="ventana", no kind="aca").
ACA_ID_BY_CODE = {
    "proyecto1": {
        "ACA 1": "aca1", "ACA 2": "aca2", "ACA 3": "aca3",
        "Autoevaluación": "auto", "Coevaluación": "coev",
    },
    "investigacion": {"ACA 1": "aca1", "ACA 2": "aca2", "ACA 3": "aca3"},
    "creatividad": {"ACA 1": "aca1", "ACA 2": "aca2", "ACA 3": "aca3"},
    "tg2": {"ACA 1": "aca1", "ACA 2": "aca2", "ACA 3": "aca3"},
    "tg3": {"ACA 1 (EV05)": "ev05", "ACA 2 (EXAM)": "exam"},
}

# Nombres anteriores que ya no deben existir en Clases/Recursos/ACAs/
# (se borran al regenerar para no dejar duplicados en manos de estudiantes).
LEGACY_FILENAMES = {
    "proyecto1": [
        "ACA Autoevaluacion.docx",   # ahora: Autoevaluacion individual (4%) - instructivo.docx
        "ACA Coevaluacion.docx",     # ahora: Coevaluacion individual (4%) - instructivo.docx
    ],
}


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


def _header(curso: str, codigo: str, fuente: str, aula: str = CDIGITAL_PLACEHOLDER) -> str:
    return f"""# Enunciado para estudiantes

**Curso:** {curso}  
**Código:** {codigo}  
**Entrega oficial:** solo por **CDigital** ({aula})  
**Fuente curricular:** {fuente}

> Lee este enunciado completo antes de empezar. Si hay duda de peso, rúbrica o ventana de entrega, confirma con **el Docente** y lo publicado en CDigital.

---
"""


def _header_instrumento(curso: str, codigo: str, fuente: str, nombre: str,
                        aula: str = CDIGITAL_PLACEHOLDER) -> str:
    """Encabezado de los instrumentos individuales de cierre (NO son ACAs)."""
    return f"""# Instructivo para estudiantes — instrumento individual de cierre

**Curso:** {curso}
**Código:** {codigo}
**Qué es:** un **formulario individual** que **tú diligencias** en **CDigital** ({aula})
**No es una ACA:** no se sube documento, no usa la plantilla APA y no es entrega de equipo
**Fuente curricular:** {fuente}

> Las ACAs de este curso son **tres** (ACA 1, ACA 2 y ACA 3). La {nombre} es un **instrumento individual de cierre**: se diligencia dentro de su ventana en CDigital. Si tienes dudas, confirma con **el Docente** y con lo publicado en el aula.

---
"""


def _fecha_block(course_key: str, aca_id: str, *, kind: str = "aca") -> str:
    titulo = "Ventana para diligenciarla" if kind == "instrumento" else "Fecha de entrega"
    return f"""## {titulo}

{texto_fecha_curso(course_key, aca_id)}

"""


def _tools_block(*extra: str) -> str:
    base = [
        "Google Docs / Word Online (abre la plantilla APA ahí; no se exige Office de escritorio)",
        "Google Scholar, SciELO, Redalyc, biblioteca virtual CUN",
        "ZoteroBib (https://zbib.org/) o citas nativas de Google Docs",
        "CDigital (entrega y retroalimentación)",
    ]
    base.extend(extra)
    lines = "\n".join(f"- {x}" for x in base)
    return f"""## 6. Herramientas (solo gratis + nube)

{lines}

**No se exige** software de escritorio de pago ni instalaciones locales pesadas.
"""


def _footer_sesiones(relacion: str, *, regla: str | None = None) -> str:
    """Cierre del enunciado.

    `regla` = de dónde salen REALMENTE las fechas de este curso, para no decirle
    al estudiante que se «calculan» cuando no es así:
      · Proyecto I            → REGLA_OFICIAL_P1 (cronograma de Coordinación).
      · Creatividad / Invest. → REGLA_VENTANAS_DOCENTE (tabla fijada por el Docente).
      · TG2 / TG3             → None ⇒ cálculo regenerable por pesos (único caso en
                                que la frase «cálculo regenerable» es cierta).
    """
    nota = (
        f"> Fechas de este enunciado: {regla}"
        if regla
        else f"> Fechas de este enunciado: cálculo regenerable (`config/cursos/fechas_entrega_aca.py`) · {REGLA_RESUMEN}"
    )
    return f"""## 7. Relación con sesiones

{relacion}

{nota}
"""


def _footer_instrumento(relacion: str) -> str:
    """Cierre de los instructivos de Proyecto I: sus ventanas son OFICIALES."""
    return f"""## 7. Relación con sesiones

{relacion}

> Ventanas de este instructivo: {REGLA_OFICIAL_P1}
"""


# ---------------------------------------------------------------------------
# Catálogo: course_key → list[{code, title, filename, weight, source, md}]
# ---------------------------------------------------------------------------

def acas_proyecto1() -> list[dict]:
    fuente = (
        "ESP329 (evaluación Art. 41: ACA1 25% · ACA2 25% · ACA3 42% · "
        "autoevaluación 4% · coevaluación 4%) · Manual del Docente / AFI (contenido de cada entrega)"
    )
    aula_p1 = cdigital_url("proyecto1")
    curso = "PROYECTO I — Especialización en Inteligencia Artificial"
    codigo = "ESP329"
    h = _header(curso, codigo, fuente, cdigital_url("proyecto1"))

    a1 = h + f"""## 1. Título / código

**ACA 1 — Formulación del problema** · **25%** de la nota del curso

## 2. Propósito / competencia que evalúa

Delimitar una situación problemática pertinente al campo de la especialización y convertirla en un avance coherente del anteproyecto: problema, pregunta, objetivos, justificación, alcances y limitaciones (unidades ESP329 U1–U3).

Macrocompetencia ESP329: formular un anteproyecto pertinente mediante delimitación del problema, revisión crítica inicial y definición de objetivos.

## 3. Consigna (paso a paso)

Trabajo **por equipo** (máx. 3 integrantes, según AFI). Un solo integrante sube la entrega grupal en CDigital.

1. Acuerda con tu equipo el tema/línea de IA y el contexto de aplicación.
2. Redacta el **planteamiento del problema** (situación actual, evidencias, por qué importa).
3. Formula la **pregunta de investigación** (clara, viable en el alcance de Proyecto I→II).
4. Escribe el **objetivo general** y los **objetivos específicos** (verbos medibles, alineados a la pregunta).
5. Desarrolla la **justificación** (teórica, práctica y/o social, según aplique).
6. Define **alcances y limitaciones** del estudio.
7. Incluye **referencias en APA 7** (mínimo las usadas en este avance).
8. Revisa coherencia: contexto ↔ problema ↔ pregunta ↔ objetivos.

## 4. Producto entregable

- Documento en **Plantilla APA CUN – Proyecto de Grado** (`{APA_REL}`), abierto preferente en Google Docs.
- Portada con nombres completos de **todos** los integrantes.
- Extensión orientativa: **6–10 páginas** de cuerpo (sin contar portada/referencias), suficiente para U2–U3.
- Formato: PDF o DOCX según indique CDigital.
- **No** recolectes datos ni apliques instrumentos en Proyecto I.

## 5. Criterios de evaluación / checklist (ESP329)

- [ ] Coherencia entre problema, pregunta y objetivos  
- [ ] Pertinencia del problema al campo / líneas del programa  
- [ ] Justificación argumentada (no solo opinión)  
- [ ] Alcances y limitaciones realistas  
- [ ] Escritura académica e integridad (citas, sin plagio)  
- [ ] Referencias APA 7  

{_tools_block(
    f"Formulario de asistencia a tutorías (estudiante): {LINK_TUTORIAS}",
    MSG_TUTORIAS_POR_GRUPO,
)}
{_footer_sesiones("Se construye tras la **Sesión 02** (problema y pregunta de investigación): es la última sesión sincrónica antes del cierre. La **Sesión 01** es de encuadre y la unidad de fundamentos va como lectura autónoma. Objetivos, justificación y alcances se trabajan en la **tutoría acordada de esa semana**; la **Sesión 03** (31/08) los amplía ya después del cierre del 30/08. Cierre de avance ACA 1 según ventana en CDigital.", regla=REGLA_OFICIAL_P1)}
"""

    a2 = h + f"""## 1. Título / código

**ACA 2 — Fundamentación referencial** · **25%** de la nota del curso

## 2. Propósito / competencia que evalúa

Construir el **marco referencial** del anteproyecto (ESP329 U4): antecedentes, marco teórico, conceptual, contextual y legal (si aplica), con fuentes académicas de calidad y citación APA 7. Incorporar las correcciones de ACA 1.

## 3. Consigna (paso a paso)

1. Incorpora **todas** las correcciones y observaciones de ACA 1 (trazabilidad visible en el documento).
2. Elabora **antecedentes** (mínimo **6**, nacionales e internacionales) alineados a tu pregunta.
3. Desarrolla el **marco teórico** (bases alineadas a variables/categorías de la pregunta).
4. Completa **marco conceptual** (definiciones operativas) y **marco contextual** (dónde se aplica).
5. Si aplica, añade **marco legal / normativo** breve y pertinente.
6. Actualiza referencias APA 7 (citas en texto + lista final).
7. Verifica que el marco “responde” a la pregunta (no es un listado desconectado).

## 4. Producto entregable

- Mismo documento acumulativo en plantilla APA CUN (`{APA_REL}`).
- Extensión orientativa del bloque referencial: **8–15 páginas** adicionales o integradas, según profundidad.
- Portada con todos los integrantes · un solo envío grupal en CDigital.

## 5. Criterios de evaluación / checklist (ESP329)

- [ ] Correcciones de ACA 1 incorporadas  
- [ ] Antecedentes ≥ 6 (nacionales e internacionales)  
- [ ] Marco teórico pertinente y actualizado  
- [ ] Conceptual + contextual claros  
- [ ] Calidad de fuentes y citación APA 7  
- [ ] Coherencia con pregunta y objetivos  

{_tools_block("ZoteroBib / Google Docs para citas", "Biblioteca virtual CUN + Scholar / SciELO / Redalyc")}
{_footer_sesiones("Se desarrolla en **Sesiones 04–07** (retro ACA1 · antecedentes · teórico · conceptual/contextual · legal/APA).", regla=REGLA_OFICIAL_P1)}
"""

    a3 = h + f"""## 1. Título / código

**ACA 3 — Diseño metodológico y anteproyecto FINAL** · **42%** de la nota del curso

## 2. Propósito / competencia que evalúa

Integrar el **anteproyecto completo** (ESP329 U5–U7): metodología **diseñada** (no aplicada), planeación/viabilidad e integración coherente del documento. Producto de cierre de Proyecto I y base para Proyecto II.

## 3. Consigna (paso a paso)

1. Incorpora correcciones de **ACA 1 y ACA 2**.
2. Completa la **metodología**: paradigma/enfoque, tipo y alcance, diseño, población/muestra o unidades de análisis, variables/categorías, técnicas e **instrumentos propuestos** (no aplicados), plan de análisis, ética.
3. Elabora **cronograma** y **presupuesto** (o recursos) viables para la continuidad del proyecto.
4. Integra todo el anteproyecto en un solo documento coherente (de portada a referencias).
5. Revisa integridad académica (similitud, citas, uso transparente de IA si la usaste).
6. Prepara el envío final grupal en CDigital.

## 4. Producto entregable

- **Anteproyecto FINAL integrado** (no un fragmento suelto) en plantilla APA CUN (`{APA_REL}`).
- Extensión orientativa: documento completo típico de anteproyecto de especialización (cuerpo suficiente para U2–U7).
- Instrumentos solo **propuestos** (anexos opcionales); **sin** recolección de datos en Proyecto I.

## 5. Criterios de evaluación / checklist (ESP329)

- [ ] Correcciones previas incorporadas  
- [ ] Metodología coherente con pregunta y objetivos  
- [ ] Instrumentos propuestos (no aplicados)  
- [ ] Cronograma y presupuesto/viabilidad  
- [ ] Coherencia global del anteproyecto  
- [ ] Escritura, fuentes, integridad y viabilidad  

{_tools_block(
    f"Tutorías: registra asistencia en {LINK_TUTORIAS}",
    MSG_TUTORIAS_POR_GRUPO,
)}
{_footer_sesiones(
    "Puente metodológico en **Sesión 08**; desarrollo ACA 3 en **Sesiones 09–10**; "
    "integración/cierre en **Sesión 11**. Usa tutorías acordadas en la semana con el Docente: "
    "hay pocas sesiones sincrónicas en esta fase.",
    regla=REGLA_OFICIAL_P1,
)}
"""

    h_auto = _header_instrumento(curso, codigo, fuente, "autoevaluación", cdigital_url("proyecto1"))
    h_coev = _header_instrumento(curso, codigo, fuente, "coevaluación", cdigital_url("proyecto1"))

    auto = h_auto + f"""## 1. Qué es este documento (y qué NO es)

**Autoevaluación individual** · **4%** de la nota única del curso · instrumento de cierre.

Es un **instrumento que tú diligencias** (tipo formulario) en CDigital para valorar tu propia trayectoria en el periodo: compromiso, aportes al equipo y avance del anteproyecto.

**No es una ACA.** Las ACAs de Proyecto I son **tres** — ACA 1 (25%), ACA 2 (25%) y ACA 3 / anteproyecto consolidado (42%) —, y son entregas documentales por equipo con rúbrica. La autoevaluación (4%) y la coevaluación (4%) completan el 100% de la nota única (Art. 41), pero **no** son una cuarta ni una quinta ACA:

- **No** subes documento ni usas la plantilla APA: no hay archivo que entregar.
- **No** es grupal: no la diligencia un vocero por el equipo.
- **No sustituye la ACA 3** ni compensa una ACA no entregada o con baja calificación.
- **No es** la autoevaluación institucional SIAC (acreditacion.cun.edu.co): esa no suma nota en este curso.
- **Solo existe en Proyecto I.** No aplica en Proyecto II ni en los cursos de pregrado (Art. 52).

**Fuente:** ESP329 («MECANISMOS Y ESTRATEGIAS DE EVALUACIÓN») · Art. 41 Reglamento Estudiantil (nota única) · cronograma AFI / Instructivo Proyecto I.

## 2. Quién la diligencia, dónde y cuándo

| Pregunta | Respuesta |
| :--- | :--- |
| **¿Quién?** | **Cada estudiante, de forma individual.** Si el equipo tiene 3 integrantes, se diligencian 3 autoevaluaciones. |
| **¿Dónde?** | En el aula del curso en **CDigital** ({aula_p1}), actividad «Autoevaluación». Ningún otro canal cuenta. |
| **¿Cuándo?** | Solo dentro de la **ventana** indicada arriba. El Docente la habilita al abrir y la cierra al terminar. |
| **¿Qué se entrega?** | Nada por archivo: el registro queda en CDigital al enviar el formulario. |

## 3. Paso a paso

1. Revisa en CDigital el **aviso de apertura** de la ventana (la publica el Docente).
2. Entra a la actividad **Autoevaluación** del aula (formulario / tarea individual en Moodle).
3. Diligénciala **con honestidad**, según tu participación real en el periodo (no según lo que quisieras haber hecho).
4. **Envía** dentro de la ventana; conserva acuse o captura si el aula lo permite.
5. Dudas sobre los ítems o la escala: pregunta al Docente **antes** del cierre, no después.

## 4. Qué pasa si no la diligencias

- Ese **4% queda en cero**: no hay entregable alternativo ni trabajo extra que lo reemplace.
- La ventana cierra en la fecha indicada y **no se reabre**: la nota debe quedar registrada antes del cierre de notas del periodo.
- Si tienes una situación de fuerza mayor, escríbele al Docente **antes** del cierre de la ventana.

## 5. Evidencia y registro de la nota

- La **evidencia oficial** es la actividad completada en CDigital (queda con fecha y hora).
- El Docente habilita la ventana, verifica el cumplimiento y registra el **4%** en el gradebook antes del cierre de notas.
- Checklist rápido:
  - [ ] Diligenciaste **tú** la autoevaluación dentro de la ventana
  - [ ] Respuestas coherentes con tu participación real
  - [ ] Tienes claro que **no** reemplaza ni compensa la ACA 3

## 6. Canal y requisitos

- **CDigital (Moodle)** — actividad «Autoevaluación» del aula. Único canal válido.
- Navegador actualizado y sesión iniciada con tu **cuenta institucional CUN**.
- No requiere instalar nada, ni pagar, ni usar la plantilla APA (no hay documento que subir).

{_footer_instrumento("Se comenta en la **Sesión 11** (integración y evaluación). La ventana abre después de la ACA 3, en la fase final del periodo.")}
"""

    coev = h_coev + f"""## 1. Qué es este documento (y qué NO es)

**Coevaluación individual** · **4%** de la nota única del curso · instrumento de cierre.

Es un **instrumento que tú diligencias** (tipo formulario) en CDigital para valorar el trabajo colaborativo y los aportes de **tus compañeros de equipo** (máx. 3), con criterio académico y respeto.

**No es una ACA.** Las ACAs de Proyecto I son **tres** — ACA 1 (25%), ACA 2 (25%) y ACA 3 / anteproyecto consolidado (42%) —, y son entregas documentales por equipo con rúbrica. La coevaluación (4%) y la autoevaluación (4%) completan el 100% de la nota única (Art. 41), pero **no** son una cuarta ni una quinta ACA:

- **No** subes documento ni usas la plantilla APA: no hay archivo que entregar.
- **No** la diligencia el equipo en bloque: cada integrante diligencia la suya.
- **No sustituye la ACA 3** ni cambia la calificación docente de las entregas grupales.
- **Solo existe en Proyecto I.** No aplica en Proyecto II ni en los cursos de pregrado (Art. 52).

**Fuente:** ESP329 · Art. 41 Reglamento Estudiantil (nota única) · cronograma AFI / Instructivo Proyecto I (obligatoria al cierre de Proyecto I; **no** en Proyecto II).

## 2. Quién la diligencia, dónde y cuándo

| Pregunta | Respuesta |
| :--- | :--- |
| **¿Quién?** | **Cada estudiante, de forma individual**, sobre sus compañeros de equipo. Nadie la diligencia por otro. |
| **¿Dónde?** | En el aula del curso en **CDigital** ({aula_p1}), actividad «Coevaluación». Ningún otro canal cuenta. |
| **¿Cuándo?** | Solo dentro de la **ventana** indicada arriba (abre justo después de la ACA 3). |
| **¿Qué se entrega?** | Nada por archivo: el registro queda en CDigital al enviar el formulario. |

## 3. Paso a paso

1. Revisa en CDigital el **aviso de apertura** de la ventana (la publica el Docente).
2. Entra a la actividad **Coevaluación** del aula.
3. Diligénciala **individualmente**, siguiendo las instrucciones y la escala publicadas.
4. Sé objetivo: valora **hechos** del trabajo conjunto (entregas cumplidas, reparto de tareas, calidad de los aportes), nunca la persona.
5. **Envía** dentro de la ventana; conserva evidencia si el aula lo permite.

## 4. Qué pasa si no la diligencias

- Ese **4% queda en cero**: no hay entregable alternativo ni trabajo extra que lo reemplace.
- La ventana cierra en la fecha indicada y **no se reabre**: la nota debe quedar registrada antes del cierre de notas del periodo.
- Si tienes una situación de fuerza mayor, escríbele al Docente **antes** del cierre de la ventana.

## 5. Evidencia y registro de la nota

- La **evidencia oficial** es la actividad completada en CDigital (queda con fecha y hora).
- El Docente habilita la ventana, verifica el cumplimiento y registra el **4%** en el gradebook antes del cierre de notas.
- Checklist rápido:
  - [ ] Diligenciaste **tú** la coevaluación dentro de la ventana
  - [ ] Valoración respetuosa y fundamentada en el trabajo del equipo
  - [ ] Cada integrante diligenció la suya (es individual)

## 6. Canal y requisitos

- **CDigital (Moodle)** — actividad «Coevaluación» del aula. Único canal válido.
- Navegador actualizado y sesión iniciada con tu **cuenta institucional CUN**.
- No requiere instalar nada, ni pagar, ni usar la plantilla APA (no hay documento que subir).

{_footer_instrumento("Se comenta en la **Sesión 11**. La ventana cierra **antes** de la de autoevaluación (ver fechas oficiales del periodo).")}
"""

    return [
        {"code": "ACA 1", "title": "Formulación del problema", "filename": "ACA 1 - Formulacion del problema.docx",
         "weight": "25%", "source": fuente, "kind": "aca", "md": a1},
        {"code": "ACA 2", "title": "Fundamentación referencial", "filename": "ACA 2 - Fundamentacion referencial.docx",
         "weight": "25%", "source": fuente, "kind": "aca", "md": a2},
        {"code": "ACA 3", "title": "Anteproyecto final", "filename": "ACA 3 - Diseno metodologico y anteproyecto final.docx",
         "weight": "42%", "source": fuente, "kind": "aca", "md": a3},
        # NO son ACAs: instrumentos individuales de cierre (se diligencian en
        # CDigital). Orden cronológico de sus ventanas: coevaluación → autoevaluación.
        {"code": "Coevaluación", "title": "Coevaluación individual (instructivo)",
         "filename": "Coevaluacion individual (4%) - instructivo.docx",
         "weight": "4%", "source": fuente, "kind": "instrumento", "md": coev},
        {"code": "Autoevaluación", "title": "Autoevaluación individual (instructivo)",
         "filename": "Autoevaluacion individual (4%) - instructivo.docx",
         "weight": "4%", "source": fuente, "kind": "instrumento", "md": auto},
    ]


def acas_investigacion() -> list[dict]:
    fuente = (
        "Syllabus SIAC EI005_PRES · Art. 52: Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%. "
        "Mecanismos: problema, protocolo, seguimiento y presentación oral/escrita. "
        "Producto: avance de artículo de nuevo conocimiento. "
        "Esta ACA evalúa el **100% de su corte**: no se subdivide en varios EV."
    )
    curso = "INVESTIGACIÓN, CIENCIA Y TECNOLOGÍA — Escuela de Ingenierías"
    codigo = "EI005"
    h = _header(curso, codigo, fuente, cdigital_url("investigacion"))

    c1 = h + f"""## 1. Título / código

**ACA 1 — Corte 1 · Fundamentos y 1.er avance del artículo** · **30%** del curso

## 2. Propósito / competencia que evalúa

Aplicar fundamentos del método científico, ubicar el tema en una de las **6 líneas** de Ingeniería y entregar el **primer avance** del artículo/protocolo (Syllabus U1–U5).

## 3. Consigna (paso a paso)

1. Elige una temática ligada a tu entorno y a una línea (IoT, Big Data, IA, cloud/FinTech, aplicaciones, telemática).
2. Resume en 1 página: tema, línea, motivación y pregunta tentativa.
3. Elabora el **1.er avance del artículo** (portada + introducción breve + problema tentativo + fuentes iniciales).
4. Prepárate para la **prueba / talleres** del corte (tipos de conocimiento, fuentes, caracterización del problema) según lo indique el Docente en CDigital.

## 4. Producto entregable

- Avance documental en plantilla APA CUN (`{APA_REL}`) o estructura equivalente en Google Docs.
- Extensión orientativa: **4–7 páginas** de avance.
- Nombre sugerido de archivo: `INV_ACA1_Apellido`.

## 5. Criterios / checklist

- [ ] Línea de Ingeniería explícita  
- [ ] Problema/tema delimitado de forma preliminar  
- [ ] Avance escrito comprensible y con fuentes iniciales  
- [ ] Integridad académica (citas)  
- [ ] Cumplimiento de talleres/quices del corte en CDigital  

{_tools_block("Padlet solo para rompehielos de presentación — no sustituye esta entrega")}
{_footer_sesiones("Tras **Sesiones 02–03** (MinCiencias y las 6 líneas de Ingeniería · prueba parcial y 1.er avance del artículo). La **Sesión 01** es de encuadre: las unidades U1–U2 (Syllabus y producto final · fundamentos del método científico) van como lectura autónoma.", regla=REGLA_VENTANAS_DOCENTE)}
"""

    c2 = h + f"""## 1. Título / código

**ACA 2 — Corte 2 · Pregunta y planteamiento del problema** · **30%** del curso

## 2. Propósito / competencia que evalúa

Identificar el problema, formular la pregunta y redactar el **planteamiento del problema** completo (Syllabus U6–U7), avanzando el artículo.

## 3. Consigna (paso a paso)

1. Usa herramientas vistas (espina de pescado, árbol de problemas o método 3D) para analizar causas.
2. Formula la **pregunta de investigación**.
3. Redacta el planteamiento: estado actual, evidencias, causas, posibles vías de solución.
4. Actualiza el documento del artículo (introducción + problema + pregunta).
5. Incorpora retroalimentación del Corte 1.

## 4. Producto entregable

- Avance actualizado del artículo/protocolo (plantilla APA CUN).
- Extensión orientativa: **6–10 páginas** acumuladas.
- Archivo: `INV_ACA2_Apellido`.

## 5. Criterios / checklist

- [ ] Problema argumentado con evidencias  
- [ ] Pregunta clara y viable  
- [ ] Planteamiento estructurado (U7)  
- [ ] Mejoras respecto al 1.er avance  
- [ ] Citas APA / integridad  

{_tools_block()}
{_footer_sesiones("Tras la **Sesión 04** (identificación de problemas y pregunta de investigación), última sesión antes del cierre de este corte.", regla=REGLA_VENTANAS_DOCENTE)}
"""

    c3 = h + f"""## 1. Título / código

**ACA 3 — Corte 3 · Fuentes, marco y avance consolidado del artículo** · **40%** del curso

## 2. Propósito / competencia que evalúa

Usar bases de datos / gestores de citas y avanzar el **marco teórico / revisión de literatura**, consolidando el producto del curso (Syllabus U8 + U10–U12; en periodo corto pueden ir combinados).

## 3. Consigna (paso a paso)

1. Busca fuentes en biblioteca CUN + Scholar / SciELO / Redalyc.
2. Organiza citas con **ZoteroBib** o Google Docs.
3. Elabora matriz de fuentes (autor, año, aporte, relación con tu pregunta).
4. Redacta avance de **marco teórico / revisión**.
5. Entrega el **paquete consolidado** del artículo hasta donde alcance el periodo (problema + pregunta + marco en progreso).
6. Cumple talleres/quices residuales del corte en CDigital.

## 4. Producto entregable

- Documento consolidado (plantilla APA CUN) + matriz de fuentes (puede ir como anexo o sección).
- Extensión orientativa: **10–15 páginas** acumuladas (según avance realista del periodo).
- Archivo: `INV_ACA3_Apellido`.

## 5. Criterios / checklist

- [ ] Fuentes confiables y pertinentes  
- [ ] Citas/referencias correctas  
- [ ] Marco/revisión alineado a la pregunta  
- [ ] Coherencia del avance global  
- [ ] Entrega completa en CDigital  

{_tools_block("ZoteroBib (zbib.org)", "Biblioteca virtual CUN (login institucional)")}
{_footer_sesiones("Tras la **Sesión 05** (formulación del planteamiento del problema). La **Sesión 06** (bases de datos CUN · gestores de citas · marco teórico y revisión, que concentra U8+U10–12 por periodo corto) es **posterior** al cierre de este corte: sirve de refuerzo, no es requisito de la entrega.", regla=REGLA_VENTANAS_DOCENTE)}
"""

    return [
        {"code": "ACA 1", "title": "Corte 1 · 1.er avance del artículo",
         "filename": "ACA 1 - Corte 1 - Fundamentos y primer avance.docx",
         "weight": "30%", "source": fuente, "md": c1},
        {"code": "ACA 2", "title": "Corte 2 · Planteamiento del problema",
         "filename": "ACA 2 - Corte 2 - Pregunta y planteamiento.docx",
         "weight": "30%", "source": fuente, "md": c2},
        {"code": "ACA 3", "title": "Corte 3 · Marco y avance consolidado",
         "filename": "ACA 3 - Corte 3 - Fuentes marco y avance consolidado.docx",
         "weight": "40%", "source": fuente, "md": c3},
    ]


def acas_creatividad() -> list[dict]:
    fuente = (
        "Syllabus SIAC EI004_VIR · Art. 52: Corte 1 = 30% · Corte 2 = 30% · Corte 3 = 40%. "
        "Producto conductor: Propuesta de Innovación (desde semana 1). "
        "Mecanismos: talleres, parciales, simulaciones, etc. con rúbrica. "
        "Esta ACA evalúa el **100% de su corte**: no se subdivide en varios EV."
    )
    curso = "CREATIVIDAD Y PENSAMIENTO INNOVADOR — Escuela de Ingenierías"
    codigo = "EI004"
    h = _header(curso, codigo, fuente, cdigital_url("creatividad"))

    c1 = h + f"""## 1. Título / código

**ACA 1 — Corte 1 · Problema–oportunidad y base creativa** · **30%** del curso

## 2. Propósito / competencia que evalúa

Identificar habilidades de creatividad/inteligencia emocional y formular el **punto de partida** de la Propuesta de Innovación (Syllabus U1–U3).

## 3. Consigna (paso a paso)

1. Completa la **ficha problema–oportunidad** (usuario concreto, dolor, evidencia, tipo tentativo Oslo, valor esperado).
2. Elabora un **mapa de utilidad / bloqueadores–ensanchadores** (Sesión 02).
3. Aplica una técnica de ideación o Design Thinking (empatía → definición → ideas) y documenta 3 ideas.
4. Elige 1 idea como semilla de tu Propuesta de Innovación.
5. Sube el paquete del corte a CDigital (y cumple talleres/quices del corte).

## 4. Producto entregable

- Paquete Corte 1 en Google Docs (o PDF): ficha + mapa + síntesis de ideación (3–6 páginas orientativas).
- Archivo: `CRE_ACA1_Apellido`.
- La ficha de Sesión 01 (`Ficha_problema_oportunidad.docx` en la carpeta de sesión) puede reutilizarse como insumo.

## 5. Criterios / checklist

- [ ] Usuario y problema concretos (no genéricos)  
- [ ] Evidencia o síntoma observable  
- [ ] Tipo de innovación tentativo (Oslo)  
- [ ] Ideación documentada  
- [ ] Claridad y entrega a tiempo en CDigital  

{_tools_block("Excalidraw / tldraw / Miro free", "Google Docs")}
{_footer_sesiones("Tras **Sesiones 02–03** (Design Thinking y técnicas de ideación · gestión de la innovación / Manual de Oslo). La **Sesión 01** es de encuadre: las unidades U1–U2 (Propuesta de Innovación · creatividad e inteligencia emocional) van como lectura autónoma.", regla=REGLA_VENTANAS_DOCENTE)}
"""

    c2 = h + f"""## 1. Título / código

**ACA 2 — Corte 2 · Tipología, gestión y validación de la propuesta** · **30%** del curso

## 2. Propósito / competencia que evalúa

Clasificar y gestionar la innovación (Manual de Oslo/OCDE), tipificar la propuesta y **validarla** con herramientas de análisis de negocios (Syllabus U4–U6).

## 3. Consigna (paso a paso)

1. Actualiza tu propuesta con tipo(s) de innovación (producto, proceso, organización, marketing, social).
2. Elabora un **cuadro comparativo** de tipos y justifica el tuyo.
3. Aplica al menos: **FODA** + **Canvas (BMC)** + definición de **MVP**.
4. Prepara una **sustentación breve** (oral o video corto / slides 1 página) de la validación.
5. Entrega el paquete del corte en CDigital.

## 4. Producto entregable

- Documento/slides: propuesta actualizada + FODA + Canvas + MVP (orientativo 6–10 páginas o equivalente visual + 1 pág. pitch).
- Herramientas sugeridas: Canvanizer / Excalidraw / Google Docs o Slides.
- Archivo: `CRE_ACA2_Apellido`.

## 5. Criterios / checklist

- [ ] Tipo de innovación bien justificado  
- [ ] FODA y Canvas coherentes con el problema  
- [ ] MVP claro y verificable  
- [ ] Sustentación comprensible  
- [ ] Mejora respecto al Corte 1  

{_tools_block("Canvanizer (BMC)", "Excalidraw", "Google Docs / Slides")}
{_footer_sesiones("Tras **Sesiones 04–05** (tipos de innovación · análisis de negocios y validación de la propuesta).", regla=REGLA_VENTANAS_DOCENTE)}
"""

    c3 = h + f"""## 1. Título / código

**ACA 3 — Corte 3 · Propuesta de Innovación final** · **40%** del curso

## 2. Propósito / competencia que evalúa

Consolidar la **Propuesta de Innovación** con vigilancia tecnológica y articulación a ecosistemas/entidades de apoyo (Syllabus U7–U8). Producto final del curso.

## 3. Consigna (paso a paso)

1. Realiza una **vigilancia tecnológica** breve (tendencias, patentes/docs, competidores o referentes).
2. Identifica **entidades de apoyo** (locales/nacionales/internacionales) pertinentes a tu propuesta.
3. Integra: problema → propuesta de valor → tipo de innovación → validación → vigilancia → siguiente paso.
4. Entrega el **paquete final** + pitch de 1 página (Docs/Slides/Canva free).
5. Cumple actividades residuales del corte en CDigital.

## 4. Producto entregable

- **Propuesta de Innovación consolidada** (documento) + pitch 1 página.
- Extensión orientativa del documento: **8–12 páginas**.
- Archivo: `CRE_ACA3_Apellido`.

## 5. Criterios / checklist

- [ ] Propuesta completa y coherente  
- [ ] Vigilancia tecnológica con fuentes  
- [ ] Ecosistema/entidades de apoyo identificados  
- [ ] Pitch claro  
- [ ] Integridad y calidad de presentación  

{_tools_block("Google Scholar / Patents (web)", "Canva free (opcional)", "Google Docs / Slides")}
{_footer_sesiones("Tras la **Sesión 06** (vigilancia tecnológica), última sesión antes del cierre. La **Sesión 07** (innovación local–internacional · entidades de apoyo) es el cierre del curso y va **después** de la recepción.", regla=REGLA_VENTANAS_DOCENTE)}
"""

    return [
        {"code": "ACA 1", "title": "Corte 1 · Problema–oportunidad",
         "filename": "ACA 1 - Corte 1 - Problema oportunidad y base creativa.docx",
         "weight": "30%", "source": fuente, "md": c1},
        {"code": "ACA 2", "title": "Corte 2 · Validación de la propuesta",
         "filename": "ACA 2 - Corte 2 - Tipologia gestion y validacion.docx",
         "weight": "30%", "source": fuente, "md": c2},
        {"code": "ACA 3", "title": "Corte 3 · Propuesta de Innovación final",
         "filename": "ACA 3 - Corte 3 - Propuesta de Innovacion final.docx",
         "weight": "40%", "source": fuente, "md": c3},
    ]


def acas_tg2() -> list[dict]:
    fuente = (
        "Manual del Docente TG2 (⚠️ sin Syllabus SIAC en carpeta). "
        "Evaluación orientativa Art. 52: 30/30/40 — CONFIRMAR en CDigital. "
        "Producto: avance consolidado del proyecto/artículo hacia TG3. "
        "Plantilla APA CUN."
    )
    curso = "TRABAJO DE GRADO 2 — Modelos de Innovación (Ing. Sistemas)"
    codigo = "94453"
    h = _header(curso, codigo, fuente, cdigital_url("tg2"))

    c1 = h + f"""## 1. Título / código

**ACA 1 — Corte 1 · Delimitación y formulación** · **30%** (orientativo)

> Confirmar peso exacto en CDigital / Syllabus cuando esté disponible.

## 2. Propósito / competencia que evalúa

Retomar el proyecto de semestres anteriores, delimitar/reformular tema y problema, y fijar pregunta, objetivos y título provisional + estructura del documento.

## 3. Consigna (paso a paso)

1. Diagnostica el estado actual de tu proyecto (qué tienes / qué falta).
2. Delimita o reformula el **problema** alineado a Ingeniería de Sistemas.
3. Formula **pregunta, objetivos y título provisional**.
4. Arma la estructura del documento en plantilla APA CUN.
5. Entrega el avance del Corte 1 en CDigital.

## 4. Producto entregable

- Avance en `{APA_REL}` (abrir en Google Docs).
- Extensión orientativa: **6–10 páginas**.
- Archivo: `TG2_ACA1_Apellido`.

## 5. Criterios / checklist

- [ ] Estado del proyecto explícito  
- [ ] Problema y pregunta coherentes  
- [ ] Objetivos alineados  
- [ ] Estructura APA iniciada  
- [ ] Integridad académica  

{_tools_block()}
{_footer_sesiones("Tras **Sesiones 02–04** (pregunta, objetivos y título provisional · estructura del documento / artículo de avance · antecedentes y referentes). La **Sesión 01** es de encuadre — allí se firma el acuerdo pedagógico — y la delimitación/reformulación del tema va como lectura autónoma.")}
"""

    c2 = h + f"""## 1. Título / código

**ACA 2 — Corte 2 · Marco referencial** · **30%** (orientativo)

## 2. Propósito / competencia que evalúa

Consolidar antecedentes y marcos (teórico, conceptual, contextual) del avance de grado.

## 3. Consigna (paso a paso)

1. Incorpora retroalimentación del Corte 1.
2. Amplía **antecedentes / referentes** (Fase I) con bases CUN + Scholar.
3. Avanza **marco teórico**, conceptual y contextual.
4. Actualiza referencias APA 7.
5. Entrega en CDigital.

## 4. Producto entregable

- Documento acumulativo (plantilla APA CUN).
- Extensión orientativa: **10–18 páginas** acumuladas.
- Archivo: `TG2_ACA2_Apellido`.

## 5. Criterios / checklist

- [ ] Correcciones previas  
- [ ] Antecedentes pertinentes  
- [ ] Marcos alineados a la pregunta  
- [ ] Citas APA 7  
- [ ] Coherencia global  

{_tools_block("ZoteroBib", "Biblioteca CUN / Scholar")}
{_footer_sesiones("Tras **Sesiones 05–08** (marco teórico · marco conceptual y contextual · diseño metodológico propuesto · instrumentos y plan de análisis).")}
"""

    c3 = h + f"""## 1. Título / código

**ACA 3 — Corte 3 · Metodología e integración del avance** · **40%** (orientativo)

## 2. Propósito / competencia que evalúa

Avanzar el diseño metodológico (propuesto), instrumentos/plan de análisis e integrar el documento listo para continuidad en **Trabajo de Grado 3**.

## 3. Consigna (paso a paso)

1. Completa enfoque, tipo, alcance y diseño metodológico **propuesto**.
2. Define instrumentos y plan de análisis (propuestos).
3. Integra el avance completo y socializa (según indique el Docente).
4. Cierra con un apartado “listo para TG3” (qué falta ejecutar/sustentar).
5. Entrega final del periodo en CDigital.

## 4. Producto entregable

- Avance consolidado (plantilla APA CUN).
- Extensión orientativa: documento integrado del avance TG2.
- Archivo: `TG2_ACA3_Apellido`.

## 5. Criterios / checklist

- [ ] Metodología coherente  
- [ ] Instrumentos/plan propuestos  
- [ ] Documento integrado  
- [ ] Preparación explícita para TG3  
- [ ] Integridad académica  

{_tools_block()}
{_footer_sesiones("Tras **Sesiones 09–11** (integración del avance y correcciones · socialización de avances · cierre del avance y preparación para TG3).")}
"""

    return [
        {"code": "ACA 1", "title": "Corte 1 · Delimitación y formulación",
         "filename": "ACA 1 - Corte 1 - Delimitacion y formulacion.docx",
         "weight": "30%*", "source": fuente, "md": c1},
        {"code": "ACA 2", "title": "Corte 2 · Marco referencial",
         "filename": "ACA 2 - Corte 2 - Marco referencial.docx",
         "weight": "30%*", "source": fuente, "md": c2},
        {"code": "ACA 3", "title": "Corte 3 · Metodología e integración",
         "filename": "ACA 3 - Corte 3 - Metodologia e integracion.docx",
         "weight": "40%*", "source": fuente, "md": c3},
    ]


def acas_tg3() -> list[dict]:
    fuente = (
        "Syllabus SIAC 94532 · Corte único 100%: EV05 50% (proceso académico) + "
        "EXAM 50% (sustentación ante pares/jurados). "
        "Artículo ≥ 50 referencias; extensión no inferior a 4.000 palabras. "
        "Cierre: póster, antiplagio, repositorio."
    )
    curso = "TRABAJO DE GRADO 3 — Modelos de Innovación (Ing. Sistemas)"
    codigo = "94532"
    h = _header(curso, codigo, fuente, cdigital_url("tg3"))

    ev05 = h + f"""## 1. Título / código

**ACA 1 — EV05 · Proceso académico (artículo)** · **50%** del curso

## 2. Propósito / competencia que evalúa

Desarrollar y consolidar el **artículo resultado de investigación** (o investigación-creación) con calidad argumentativa, bajo acompañamiento del Docente (Syllabus U1–U12 / proceso).

## 3. Consigna (paso a paso)

1. Retoma/define el proyecto y formula pregunta, objetivos y título.
2. Redacta introducción y estructura del artículo (plantilla APA CUN).
3. Desarrolla referentes (fases), metodología/instrumento y análisis según tu ruta.
4. Cierra marco teórico, resultados/discusión, resumen, palabras clave UNESCO, conclusiones y referencias.
5. Alista póster, evidencias/anexos y **verificación antiplagio** institucional antes de la sustentación.
6. Entrega los avances de proceso en las actividades EV05 de CDigital (según hitos del Docente).

## 4. Producto entregable

- Artículo en plantilla APA CUN (`{APA_REL}`).
- Requisitos syllabus: **≥ 50 referencias** · **≥ 4.000 palabras**.
- Póster + evidencias para anexos (formato que indique el Docente).
- Archivo sugerido: `TG3_EV05_Articulo_Apellido`.

## 5. Criterios / checklist

- [ ] Coherencia problema–pregunta–objetivos–método–resultados  
- [ ] Revisión bibliográfica rigurosa (≥ 50 refs)  
- [ ] Extensión ≥ 4.000 palabras  
- [ ] APA 7 e integridad (antiplagio)  
- [ ] Póster/evidencias listos  
- [ ] Calidad argumentativa (evaluación docente + preparación a jurados)  

{_tools_block(
    "ZoteroBib",
    "Google Docs",
    "Herramienta antiplagio institucional (ruta oficial del semestre en CDigital — no inventar URL)",
)}
{_footer_sesiones("Proceso a lo largo de **Sesiones 02–11** (del artículo hasta el póster y la verificación de similitud; la **Sesión 01** es de encuadre y U1–U2 van como lectura autónoma). Los hitos parciales los define el Docente dentro de EV05.")}
"""

    exam = h + f"""## 1. Título / código

**ACA 2 — EXAM · Sustentación ante jurados** · **50%** del curso

## 2. Propósito / competencia que evalúa

Sustentar oralmente el trabajo de grado ante pares/jurados asignados por la Dirección del Programa (Syllabus U13) y completar entregables de repositorio (U14).

## 3. Consigna (paso a paso)

1. Confirma fecha, modalidad y requisitos de sustentación con el Docente / programa.
2. Prepara exposición (póster + síntesis del artículo: problema, método, hallazgos, aporte).
3. Ensaya tiempos y respuestas a preguntas de jurados.
4. Realiza la **sustentación**.
5. Carga los **entregables al repositorio institucional** según checklist oficial (U14).

## 4. Producto entregable

- Sustentación oral (evidencia según protocolo del programa).
- Paquete final para repositorio (artículo + anexos que exija la institución).
- Archivo de apoyo sugerido: `TG3_EXAM_Sustentacion_Apellido` (slides/póster).

## 5. Criterios / checklist

- [ ] Dominio del contenido del artículo  
- [ ] Claridad y argumentación en la defensa  
- [ ] Respuesta a jurados  
- [ ] Material visual (póster) adecuado  
- [ ] Entregables de repositorio completos  

{_tools_block(
    "Google Slides / Canva free (póster)",
    "CDigital / repositorio institucional",
)}
{_footer_sesiones("**Sesión 12** = sustentación ante jurados · **Sesión 13** = entregables para repositorio institucional · **Sesiones 14–15** son buffer de calendario, solo si el calendario del grupo las contempla (el grupo 54450 no tiene la Sesión 15).")}
"""

    return [
        {"code": "ACA 1 (EV05)", "title": "Proceso académico (artículo)",
         "filename": "ACA 1 - EV05 Proceso academico (articulo).docx",
         "weight": "50%", "source": fuente, "md": ev05},
        {"code": "ACA 2 (EXAM)", "title": "Sustentación ante jurados",
         "filename": "ACA 2 - EXAM Sustentacion ante jurados.docx",
         "weight": "50%", "source": fuente, "md": exam},
    ]


ACAS_BY_COURSE = {
    "proyecto1": acas_proyecto1,
    "investigacion": acas_investigacion,
    "creatividad": acas_creatividad,
    "tg2": acas_tg2,
    "tg3": acas_tg3,
}


def acas_for(key: str) -> list[dict]:
    """Catálogo del curso con ``kind`` normalizado.

    ``kind="aca"`` → enunciado de entregable evaluado (por defecto).
    ``kind="instrumento"`` → instructivo de instrumento individual de cierre
    (autoevaluación / coevaluación de Proyecto I): NO son ACAs.
    """
    items = ACAS_BY_COURSE[key]()
    for a in items:
        a.setdefault("kind", "aca")
    return items


def catalog_for_leeme(key: str) -> list[dict]:
    """Filas para el LEEME de estudiantes.

    Cada ítem: ``{code, title, rel, fecha, weight, kind}``. ``kind`` permite al
    consumidor separar las ACAs de los instrumentos individuales de cierre
    (auto/coevaluación de Proyecto I), que **no** deben listarse como una ACA más.
    """
    from fechas_entrega_aca import entrega_por_id, entregas_curso, fmt_dmy

    items = acas_for(key)
    out = []
    for a in items:
        aca_id = ACA_ID_BY_CODE[key][a["code"]]
        data = entregas_curso(key)
        if isinstance(data, dict):
            dates = sorted({
                e.entrega for items_g in data.values() for e in items_g if e.id == aca_id
            })
            fecha_txt = " / ".join(fmt_dmy(d) for d in dates)
        else:
            fecha_txt = fmt_dmy(entrega_por_id(key, aca_id).entrega)
        out.append({
            "code": a["code"],
            "title": a["title"],
            "rel": f"{ACAS_REL}/{a['filename']}",
            "fecha": fecha_txt,
            "weight": a.get("weight") or "—",
            "kind": a["kind"],
        })
    return out


def _inject_fecha(md: str, course_key: str, code: str, kind: str = "aca") -> str:
    aca_id = ACA_ID_BY_CODE[course_key][code]
    bloque = _fecha_block(course_key, aca_id, kind=kind)
    if "\n---\n" in md:
        pre, post = md.split("\n---\n", 1)
        return pre + "\n---\n\n" + bloque + post.lstrip("\n")
    return bloque + md


def build_course(key: str) -> list[str]:
    if key not in ACAS_BY_COURSE:
        raise KeyError(key)
    c = COURSES[key]
    cc = carga_curso(key)
    out_dir = Path(c["folder"]) / "Clases" / "Recursos" / "ACAs"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for a in acas_for(key):
        path = out_dir / a["filename"]
        if a["kind"] == "instrumento":
            subtitle = f"Instrumento individual de cierre · {cc['titulo_corto']}"
            footer = (
                f"CUN · {cc['titulo_corto']} · Instrumento individual de cierre "
                "(no es una ACA) · Vigilada Mineducación"
            )
        else:
            subtitle = f"Enunciado ACA · {cc['titulo_corto']}"
            footer = f"CUN · {cc['titulo_corto']} · Enunciado ACA · Vigilada Mineducación"
        md = _inject_fecha(a["md"], key, a["code"], a["kind"])
        write_md_as_docx(md, str(path), subtitle=subtitle, footer=footer)
        written.append(str(path))
        print("OK", "INSTRUMENTO" if a["kind"] == "instrumento" else "ACA", key, a["filename"])
    for p in out_dir.glob("*.md"):
        p.unlink()
        print("RM", p)
    # Nombres viejos (p. ej. "ACA Autoevaluacion.docx"): se borran para no dejar
    # duplicados que sigan llamando ACA a lo que no lo es.
    for name in LEGACY_FILENAMES.get(key, ()):
        old = out_dir / name
        if old.is_file():
            old.unlink()
            print("RM obsoleto", old)
    return written


def main(argv: list[str] | None = None) -> None:
    argv = list(argv or sys.argv[1:])
    keys = argv if argv else list(ACAS_BY_COURSE.keys())
    for key in keys:
        build_course(key)
    print(
        "Listo: enunciados ACA en Clases/Recursos/ACAs/ (los cursos solicitados). "
        "Proyecto I incluye además los instructivos de autoevaluación y coevaluación "
        "(instrumentos individuales de cierre, NO son ACAs)."
    )


if __name__ == "__main__":
    main()
