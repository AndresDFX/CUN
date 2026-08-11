# -*- coding: utf-8 -*-
"""Guion de montaje del rompehielos de la Sesión 01 en **Slido**, por curso.

POR QUÉ EXISTE
    El rompehielos era un muro de Padlet donde cada quien se presentaba. Con 20 estudiantes
    eso funciona: se lee entero. Con 50 —y con los 112 de TG3— no lo lee nadie, y encima el
    plan gratis de Padlet solo da 3 tableros. Decisión del Docente (11/08/2026): en los
    cursos de más de 20 el rompehielos deja de ser una presentación y pasa a ser un **juego
    de azar con premio**, en Slido.

QUÉ NO ES
    No es un quiz sobre el curso. Un primer intento preguntaba pesos y fechas: el Docente lo
    descartó por «nerd», y con razón — eso es la clase, no el rompehielos, y va DESPUÉS. El
    juego va en la **slide 3**, entre «Docente» y «¿Qué es esta asignatura?», o sea **antes
    de que aparezca el primer porcentaje**. Se juega a «dos verdades y una mentira» sobre el
    Docente: acertar es 1 entre 3, azar puro, se ríen, y de paso queda hecha la presentación
    del Docente, que es una de las tres cosas que la Sesión 01 tiene que resolver.

POR QUÉ SLIDO Y NO MENTIMETER
    El plan gratis de Mentimeter corta en **50 participantes al mes**: no alcanza ni para un
    curso de 50, menos para TG3. El de Slido (Basic) da **100 participantes por evento**,
    **3 encuestas**, **1 quiz con tabla de posiciones** y **Q&A ilimitado**. Con 112
    matriculados en TG3 no se conectan los 112 a una clase virtual de una hora, así que el
    tope de 100 no estorba — pero queda declarado en el guion por si algún día estorba.

QUÉ GENERA
    <Asignatura>/2026/<grupo>/Rompehielos Slido - Sesion 01.md   (TG3: en _combinado_todos/)

    Es material del DOCENTE: lleva las casillas donde marca cuál de las tres frases de cada
    ronda es la mentira. Por eso NO va en `Clases/`.

Uso:
  python config/slides/build_rompehielos_slido.py            # todos los que apliquen
  python config/slides/build_rompehielos_slido.py tg3        # uno solo
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cursos"))

from sesiones_cun import COURSES, DOCENTE_CORREO  # noqa: E402
from build_acas_estudiantes import catalog_for_leeme  # noqa: E402

# Por encima de este número, el muro deja de leerse y el rompehielos pasa a ser juego.
UMBRAL_MURO = 20
# Tope del plan gratis de Slido (Basic), verificado el 2026-08-11.
SLIDO_TOPE_GRATIS = 100
NOMBRE = "Rompehielos Slido - Sesion 01.md"
EMAIL_RX = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# EL JUEGO: «Dos verdades y una mentira», en tres rondas sobre el Docente.
# Cada ronda es UNA pregunta del quiz con tres opciones: acertar es 1 entre 3, azar puro.
# El Docente marca cuál es la mentira antes de clase. Las frases vienen sugeridas para que
# montarlo cueste cinco minutos, pero hay que ajustarlas: si no son suyas, no funciona.
RONDAS = [
    {
        "titulo": "Ronda 1 · De dónde vengo",
        "frases": [
            "Mi primera línea de código la escribí en Visual Basic",
            "Aprendí a programar solo, antes de entrar a la universidad",
            "Reprobé la primera materia de programación que vi",
        ],
    },
    {
        "titulo": "Ronda 2 · Lo que hago hoy",
        "frases": [
            "Lidero técnicamente un equipo de software",
            "He dado charlas en más de cinco ciudades",
            "Estoy terminando una maestría en Inteligencia Artificial",
        ],
    },
    {
        "titulo": "Ronda 3 · Fuera del código",
        "frases": [
            "Toco un instrumento",
            "No tomo café",
            "Me sé de memoria todos los cumpleaños de mi familia",
        ],
    },
]


def _matriculados(base: Path, grupos: list[str]) -> int:
    """Estudiantes del curso, contados en los rosters de CDigital (0 si no hay).

    El roster de CDigital incluye al Docente como participante del aula: si no se descuenta,
    Investigación sale con 21 y cruza el umbral de 20 por una persona que no es estudiante.
    """
    correos: set[str] = set()
    for g in grupos:
        f = base / g / "Listado estudiantes (CDigital).csv"
        if f.is_file():
            correos |= set(EMAIL_RX.findall(f.read_text(encoding="utf-8", errors="replace")))
    return len({e for e in correos if e.lower() != DOCENTE_CORREO.lower()})


def _grupos(course_key: str, base: Path) -> list[str]:
    if not base.is_dir():
        return []
    return [p.name for p in sorted(base.iterdir()) if p.is_dir() and not p.name.startswith("_")]


def _primer_cierre(course_key: str) -> str:
    """Cierre del primer ítem evaluable — para que el premio tenga una fecha real."""
    rows = catalog_for_leeme(course_key)
    c1 = [r for r in rows if r["corte"] == 1] or rows
    return f"{c1[0]['code']} ({c1[0]['fecha']})" if c1 else "la primera entrega"


def _texto(course_key: str, grupos: list[str], n_est: int) -> str:
    c = COURSES[course_key]
    titulo = c["titulo"]
    etiqueta = " + ".join(grupos)
    primero = _primer_cierre(course_key)

    aforo = (
        f"El plan gratis de Slido admite **{SLIDO_TOPE_GRATIS} participantes por evento**"
        + (
            f". Hay {n_est} matriculados, así que si algún día se conectaran más de "
            f"{SLIDO_TOPE_GRATIS} a la vez, los últimos se quedarían fuera del juego (no de "
            "la clase). A una virtual de una hora no se conecta la matrícula completa, pero "
            "conviene saberlo."
            if n_est > SLIDO_TOPE_GRATIS else
            f", de sobra para los {n_est} de este grupo."
        )
    )

    bloques = []
    for r in RONDAS:
        frases = "\n".join(f"   - [ ] {f}" for f in r["frases"])
        bloques.append(f"### {r['titulo']}\n\n{frases}\n")

    return f"""# Rompehielos de la Sesión 01 — {titulo}

**Grupo(s):** {etiqueta} · **{n_est} matriculados**
**Juego:** Dos verdades y una mentira · **Slido** (plan gratis) · **8 minutos** · **slide 3**

> **Material del Docente.** Aquí marcas cuál es la mentira de cada ronda. No va en
> `Clases/`. Regenerar: `python config/slides/build_rompehielos_slido.py {course_key}`

---

## Dónde encaja y por qué ahí

Va **entre la slide «Docente» y «¿Qué es esta asignatura?»**, o sea **antes de que aparezca el
primer porcentaje**. Ese orden no es casual: si lo primero que ven es una tabla de pesos y
fechas, ya perdiste la sala.

Y no es relleno. Mientras juegan **te están conociendo**, que es una de las tres cosas que
la Sesión 01 tiene que resolver, y te ahorra la diapositiva de biografía que no lee nadie.
Acertar es 1 entre 3: **azar puro**, así que el que nunca abre la cámara arranca igual que
el que siempre habla.

Con {n_est} estudiantes, pedir que se presenten uno por uno no cabe en la hora, y un muro
donde cada quien escribe su nombre no lo lee nadie. Por eso se cambió.

---

## Antes de la clase (5 minutos, una sola vez)

1. Entra a **https://www.slido.com** y crea un evento para la sesión.
2. Crea **un Quiz de 3 preguntas**, una por ronda. Cada una dice *«Una de estas tres NO es
   cierta, ¿cuál?»* y lleva las tres frases como opciones. El plan gratis da **un solo quiz
   por evento**: no lo gastes en otra cosa. El quiz **pide nombre**, y eso es lo que produce
   la tabla de posiciones.
3. **Ajusta las frases de abajo a tu realidad y marca la mentira de cada ronda.** Las
   sugeridas son un punto de partida; si no son tuyas, el juego no funciona.
4. Crea **una encuesta de opción múltiple** vacía, con tres opciones A / B / C: es para la
   ronda final, que se juega en vivo (paso 4 de la clase).
5. Deja el **Q&A abierto** toda la sesión. En el plan gratis es ilimitado y, con {n_est}
   matriculados, es donde de verdad van a preguntar: por micrófono no lo hará casi nadie.

{aforo} Vas a usar 1 encuesta de las 3 gratis y el único quiz; quedan dos de reserva.

---

## En clase (8 minutos)

| # | Momento | Tiempo | Qué haces |
| :-: | :--- | :---: | :--- |
| 1 | Explicas y anuncias el premio | 1 min | «Tres rondas, en cada una miento una vez. El que más me pille, gana.» Si no saben qué se juega, no juegan. |
| 2 | Las tres rondas | 4 min | Lanzas la ronda, esperas 20–30 s, **revelas cuál era la mentira y cuentas la historia de la verdad más rara**. Ahí está tu presentación, sin diapositiva. |
| 3 | Tabla de posiciones | 1 min | La proyectas. Salen los tres primeros. |
| 4 | **La ronda final** | 2 min | Le das el micrófono al podio: cada uno dice **sus** dos verdades y una mentira, y el curso vota en la encuesta. **Gana el que engañe a más gente.** |

El paso 4 es el que cierra el círculo: los estudiantes también se presentan, pero hablan
tres, no {n_est}. Y hablan los que ya se ganaron el turno, no los de siempre.

---

## Las tres rondas

Marca la mentira de cada una **antes** de clase. Consejo: que las dos verdades sean las
raras y la mentira la creíble. Al revés no tiene gracia y lo adivinan todos.

{chr(10).join(bloques)}
---

## El premio

Anúncialo **antes** de la primera ronda:

> **Revisión 1 a 1 con el Docente** del avance del ganador, antes de {primero}. Media hora
> de tu tiempo, cero riesgo de distorsionar la nota, y para el estudiante vale mas que un
> punto suelto.

Dos alternativas que también funcionan: **elegir primero** el turno de sustentación o la
línea de investigación, y el **reconocimiento** en la tabla, que con un grupo grande motiva
más de lo que parece. Lo que **no** conviene es regalar décimas: distorsiona la evaluación y
te lo van a pedir todo el semestre.

---

## Los que no se conectaron

{('Con ' + str(n_est) + ' matriculados no llega todo el mundo a la sincrónica. ') if n_est > 40 else ''}Deja el evento
de Slido **abierto 48 horas** y publica el enlace en el aula. Quien no estuvo juega igual:
no entra en la tabla de posiciones —sería injusto con quien sí llegó— pero llega a la
Sesión 02 sabiendo quién le da clase.
"""


def build_curso(course_key: str) -> str | None:
    c = COURSES[course_key]
    base = Path(c["folder"]) / "2026"
    grupos = _grupos(course_key, base)
    if not grupos:
        print(f"SKIP {course_key}: sin carpetas de grupo en {base}")
        return None

    n_est = _matriculados(base, grupos)
    if n_est and n_est <= UMBRAL_MURO:
        print(f"SKIP {course_key}: {n_est} estudiantes (≤ {UMBRAL_MURO}) — conserva el muro")
        return None

    combinado = len(grupos) > 1
    out_dir = (base / "_combinado_todos") if combinado else (base / grupos[0])
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / NOMBRE
    dest.write_text(_texto(course_key, grupos, n_est), encoding="utf-8")
    raiz = Path(c["folder"]).parents[1]
    print(f"OK {course_key}: {dest.relative_to(raiz)} · {n_est} estudiantes")
    return str(dest)


def main(argv: list[str]) -> int:
    keys = [a for a in argv if a in COURSES] or list(COURSES)
    hechos = [k for k in keys if build_curso(k)]
    print(f"\nGenerados: {len(hechos)}/{len(keys)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
