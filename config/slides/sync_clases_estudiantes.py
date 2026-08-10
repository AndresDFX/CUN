# -*- coding: utf-8 -*-
"""Consolida en Clases/ lo que se comparte con estudiantes (los 5 cursos).

- Genera enunciados ACA en Clases/Recursos/ACAs/ (.docx)
- Copia Plantilla APA a Clases/Recursos/
- Escribe Clases/LEEME - Material para estudiantes.docx (nunca .md en Clases/)
- Regenera Correo de bienvenida en rutas docentes (`2026/<grupo>/`; nunca en Clases/)
- (Creatividad) ficha taller S01 en carpeta de sesión como .docx

Uso: python config/slides/sync_clases_estudiantes.py
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))

from sesiones_cun import (
    COURSES,
    CURSOS_CON_TUTORIAS_POR_GRUPO,
    DOCENTE_CORREO,
    LINK_TUTORIAS,
    MSG_TUTORIAS_POR_GRUPO,
    meet_url,
)
from cun_slides_engine import PADLET_PRESENTACION_URL
from guion_md_a_docx import convert as md_to_docx
from build_acas_estudiantes import build_course as build_acas, catalog_for_leeme
from build_correo_bienvenida import build_course as build_correo, CORREO_NAME
from carga_academica import curso as carga_curso
from sesiones_cun import cdigital_url, CDIGITAL_PLACEHOLDER  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
APA_SRC = os.path.join(ROOT, "Plantilla_APA_CUN_Proyecto de grado.docx")
APA_NAME = "Plantilla_APA_CUN_Proyecto de grado.docx"
# Placeholder de respaldo: los usos por curso deben llamar a
# `cdigital_url(<clave del curso>)`, que devuelve la URL real del aula si existe
# en carga_academica_2026.json (auditadas el 2026-08-10) y el placeholder si no.
URL_CDIGITAL = CDIGITAL_PLACEHOLDER

LEEME_NAME = "LEEME - Material para estudiantes.docx"
FICHA_CREATIVIDAD_NAME = "Ficha_problema_oportunidad.docx"

PRESENTACION_CURSO = {
    "proyecto1": "Presentacion del Curso - Proyecto I.pptx",
    "investigacion": "Presentacion del Curso - Investigacion Ciencia y Tecnologia.pptx",
    "creatividad": "Presentacion del Curso - Creatividad y Pensamiento Innovador.pptx",
    "tg2": "Presentacion del Curso - Trabajo de Grado 2.pptx",
    "tg3": "Presentacion del Curso - Trabajo de Grado 3.pptx",
}

FICHA_CREATIVIDAD_S01 = """# Ficha problema–oportunidad (Sesión 01)

**Curso:** Creatividad y Pensamiento Innovador  
**Entregable:** sube a CDigital como `S01_FichaProblema_Apellido`  
**Preferible:** Google Docs / Word Online (no se exige Office de escritorio).

Completa los 6 campos:

1. **Título tentativo:**

2. **Usuario concreto:** (quién sufre el problema; no “la gente”)

3. **Problema (3–5 líneas):**

4. **Evidencia o síntoma observable:**

5. **Tipo de innovación tentativo:** (producto / proceso / organización / marketing / social)

6. **Valor esperado (1 frase):**

---

**Criterio de éxito:** si alguien externo entiende el usuario + el dolor + el contexto sin pedirte aclaración, la ficha sirve.
"""


def write_md_as_docx(
    md_text: str,
    docx_path: str,
    *,
    subtitle: str | None = None,
    footer: str | None = None,
) -> None:
    """Genera .docx con marca CUN (sin dejar .md en Clases/)."""
    fd, tmp = tempfile.mkstemp(suffix=".md", prefix="clases_est_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(md_text)
        md_to_docx(tmp, docx_path, brand=True, subtitle=subtitle, footer=footer)
    finally:
        if os.path.isfile(tmp):
            os.remove(tmp)


def remove_if_exists(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)
        print("RM", path)


def leeme_md(key: str) -> str:
    c = COURSES[key]
    pptx_curso = PRESENTACION_CURSO[key]
    meet = meet_url(key, c["titulo"])
    aca_rows = catalog_for_leeme(key)
    # La tabla lista los **ítems reales del libro de calificaciones** (auditoría
    # CDigital 10/08/2026), no solo las tareas: en pregrado 5 de los 8 ítems son
    # cuestionarios (quices y parciales) y antes no aparecían en ningún lado.
    aca_table = "\n".join(
        f"| **{r['code']}** — {r['title']} | {r['corte']} | {r['tipo']} · **{r['weight']}** "
        f"| **{r['fecha']}** | `{r['rel']}` |"
        for r in aca_rows
    )
    # Auto/coevaluación: existen en los 5 cursos (no solo Proyecto I). NO son ACAs
    # — van aparte y rotuladas como instrumentos individuales de cierre.
    instrumentos = [r for r in aca_rows if r["kind"] == "instrumento"]
    documental = [r for r in aca_rows if r["kind"] == "aca"]
    instrumentos_bloque = ""
    arbol_instrumentos = ""
    if instrumentos:
        pesos = " / ".join(dict.fromkeys(r["weight"] for r in instrumentos))
        arbol_instrumentos = (
            f"\n      Autoevaluacion / Coevaluacion individual ({pesos}) - instructivo.docx"
            "   ← no son ACAs"
        )
        lineas = "\n".join(
            f"- **{r['code']}** ({r['weight']}) — se diligencia hasta el **{r['fecha']}** · "
            f"instructivo: `{r['rel']}`"
            for r in instrumentos
        )
        instrumentos_bloque = (
            "\n### Autoevaluación y coevaluación — **no son ACAs**\n\n"
            "Al cierre del curso hay además dos **instrumentos individuales**: no se entrega documento "
            "ni se usa la plantilla APA. **Cada estudiante los diligencia** (tipo formulario) en **CDigital**, "
            "dentro de su ventana. **No sustituyen "
            + (f"la {documental[-1]['code']}" if documental else "el entregable del corte 3")
            + "**; si no los diligencias, ese porcentaje queda en cero.\n\n"
            f"{lineas}\n"
        )
    tutorias_bloque = ""
    # Solo Proyecto I (AFI). No inventar esta sección en TG2/TG3.
    if key in CURSOS_CON_TUTORIAS_POR_GRUPO:
        tutorias_bloque = (
            "\n---\n\n"
            "## Tutorías por grupo\n\n"
            f"{MSG_TUTORIAS_POR_GRUPO}\n\n"
            "En Proyecto I, la 2.ª hora del encuentro semanal es tutoría/taller en vivo; "
            "las revisiones adicionales por equipo también se acuerdan en la semana. "
            f"Cuando asistas a tutoría, registra asistencia en: {LINK_TUTORIAS}.\n"
        )
    return f"""# Material para estudiantes — {c["titulo"]}

Esta carpeta **`Clases/`** es lo único que el Docente comparte contigo para la asignatura.
Guiones, manuales y calendarios con datos internos **no** van aquí.

**Contacto del Docente:** {DOCENTE_CORREO}

---

## Empieza por aquí

1. Este **LEEME** — mapa de la carpeta y listado de ACAs.
2. **Presentación del Curso** — encuadre, el Docente, rompehielos Padlet y acuerdos.
3. **`Sesion 01 - …/`** — además del deck, trae la **lectura autónoma** de la semana en PDF y el archivo `Lectura autonoma - Sesion 01.txt` con la cita, el enlace y **qué traer a la Sesión 02**. La Sesión 01 es de **encuadre**: no se dicta tema, el contenido arranca en la Sesión 02.
4. **`Recursos/ACAs/`** — enunciados de las entregas evaluadas.

La **bienvenida del curso** (grupo, horario y contacto) la recibes por **correo electrónico** del Docente; no forma parte de esta carpeta compartida.

---

## Enlaces del curso

| Recurso | Enlace / ubicación |
| :--- | :--- |
| **Padlet** (rompehielos / Preséntate) | {PADLET_PRESENTACION_URL} |
| **Google Meet** (mismo enlace toda la serie) | {meet} |
| **CDigital** (campus del curso) | {cdigital_url(key)} |
| **Plantilla APA CUN** | `Recursos/{APA_NAME}` (ábrela en Google Docs / Word Online) |

{tutorias_bloque}
---

## Lo que se evalúa (los ítems de CDigital, uno por uno)

Esta tabla es **el libro de calificaciones de tu aula**: cada fila es un ítem que existe en **CDigital** y tiene su propio documento en **`Recursos/ACAs/`**. Los cuestionarios (quices y parciales) **se resuelven en el aula, no se sube archivo**; su documento es la **guía** que te dice qué entra. Las tareas sí se suben. Léelo antes de cada fecha: las notas oficiales solo salen de CDigital.

| Ítem del aula | Corte | Tipo · peso | Cierre | Documento |
| :--- | :---: | :--- | :--- | :--- |
{aca_table}
{instrumentos_bloque}
---

## Cómo está organizada esta carpeta

```text
Clases/
  LEEME - Material para estudiantes.docx   ← este archivo
  {pptx_curso}
  Recursos/
    {APA_NAME}
    ACAs/
      Quiz / Parcial N (peso) - guia del cuestionario.docx   ← qué entra; se resuelve en el aula
      ACA … (peso) - ….docx                                  ← tarea: esto sí se sube{arbol_instrumentos}
  Sesion 01 - …/
    Presentacion.pptx
    Lectura autonoma - Sesion 01.txt       ← qué leer, para cuándo y dónde está
    Lectura … .pdf                          ← la(s) lectura(s), en acceso abierto
    (fichas / capturas de apoyo si aplica)
  Sesion 02 - …/
  …
```

1. **Presentación del Curso** — bienvenida, el Docente, rompehielos Padlet (slide Preséntate), contenido, recursos y acuerdos. La **Sesión 01** de encuadre usa este deck para el Preséntate.
2. **`Sesion NN - <tema>/`** — diapositivas de esa clase (`Presentacion.pptx`) y, si hay, plantillas o capturas de apoyo para el taller. En **`Sesion 01 - …/`** están además la **lectura autónoma** (PDF de acceso abierto) y el `.txt` que dice qué leer, cuánto tarda y qué traer a la Sesión 02: **no hay que buscarla en ningún otro lado**.
3. **`Recursos/`** — plantilla APA + carpeta **`ACAs/`** con los enunciados. No busques estos archivos fuera de `Clases/`.

---

## Entregas

- Las entregas y notas oficiales van por **CDigital** (cuando esté el enlace del campus).
- Usa la plantilla APA de `Recursos/` cuando el entregable sea documental.
- Sigue el enunciado de `Recursos/ACAs/` correspondiente a cada corte/ACA.
- El Padlet es para presentarte / mapear expectativas; no sustituye la entrega en CDigital.

---

*Si falta un enlace (Meet o CDigital), el Docente lo publicará en el canal del curso.*
"""


def sync_course(key: str) -> None:
    c = COURSES[key]
    clases = os.path.join(c["folder"], "Clases")
    recursos = os.path.join(clases, "Recursos")
    os.makedirs(recursos, exist_ok=True)

    # Enunciados ACA (docx) en Recursos/ACAs/
    build_acas(key)

    # Correo de bienvenida: solo rutas docentes (2026/<grupo>/); limpia si quedó en Clases/
    build_correo(key)
    remove_if_exists(os.path.join(clases, CORREO_NAME))

    cc = carga_curso(key)
    brand_sub = f"Material para estudiantes · {cc['titulo_corto']}"
    brand_foot = f"CUN · {cc['titulo_corto']} · Clases/ · Vigilada Mineducación"
    leeme_docx = os.path.join(clases, LEEME_NAME)
    write_md_as_docx(leeme_md(key), leeme_docx, subtitle=brand_sub, footer=brand_foot)
    print("OK LEEME", leeme_docx)
    remove_if_exists(os.path.join(clases, "LEEME - Material para estudiantes.md"))

    if not os.path.isfile(APA_SRC):
        raise FileNotFoundError(APA_SRC)
    apa_dst = os.path.join(recursos, APA_NAME)
    shutil.copy2(APA_SRC, apa_dst)
    print("OK APA", apa_dst)

    if key == "creatividad":
        s01 = None
        for name in os.listdir(clases):
            if name.startswith("Sesion 01"):
                s01 = os.path.join(clases, name)
                break
        if s01:
            ficha_docx = os.path.join(s01, FICHA_CREATIVIDAD_NAME)
            write_md_as_docx(
                FICHA_CREATIVIDAD_S01,
                ficha_docx,
                subtitle=f"Ficha de taller · {cc['titulo_corto']}",
                footer=brand_foot,
            )
            print("OK ficha", ficha_docx)
            remove_if_exists(os.path.join(s01, "Ficha_problema_oportunidad.md"))
            # Ejemplo modelo (referencia visual) — opcional si existe en Guiones/Capturas
            modelo_src = os.path.join(
                c["folder"], "Guiones", "Capturas", "Sesion 01", "s01_ficha_modelo.html"
            )
            if os.path.isfile(modelo_src):
                modelo_dst = os.path.join(s01, "Ejemplo_ficha_modelo.html")
                shutil.copy2(modelo_src, modelo_dst)
                print("OK ejemplo ficha", modelo_dst)


def main():
    for key in ("proyecto1", "investigacion", "creatividad", "tg2", "tg3"):
        sync_course(key)
    print("Listo: Clases/ sincronizado en los 5 cursos (material estudiante = .docx).")


if __name__ == "__main__":
    main()
