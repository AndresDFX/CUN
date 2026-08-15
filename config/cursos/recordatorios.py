"""Recordatorios automáticos de entregas para los estudiantes.

Qué es esto
-----------
Un planificador que, dado un día, dice **qué recordatorios toca mandar hoy** y los publica en el
foro «Avisos» del aula (que tiene suscripción forzada, así que el campus manda el correo a todos los
matriculados). Nada de credenciales de Gmail, nada de servidor de correo propio, nada de contraseñas
de aplicación —que esta cuenta institucional no puede generar—.

Tres decisiones de diseño que conviene no deshacer:

1. **Una sola fuente de fechas**: `fechas_entrega_aca.py`. Ni este archivo ni el aula deciden nada.
   Cambiar una entrega es cambiarla allí; el recordatorio y la ventana del aula se mueven detrás.
2. **Sólo se recuerda lo que el estudiante puede ver.** Si la actividad está oculta en el aula, el
   enlace del recordatorio sería un 404 y el aviso, ruido. Se omite y se dice por qué. Así, los
   recordatorios se encienden solos a medida que el Docente va activando los ítems.
3. **Simula por defecto.** Publicar manda correo a 282 personas y no se puede deshacer. Hace falta
   `--canal campus --confirmar` para que salga algo de verdad.

Sirve igual el semestre que viene: lo único con año dentro es `fechas_entrega_aca.py`, y las aulas
nuevas se declaran en `AULAS_CURSO` de `config/moodle/cdigital.py`.

Uso
---
    python config/cursos/recordatorios.py                      # qué se mandaría hoy (simulación)
    python config/cursos/recordatorios.py --fecha 2026-08-18   # ensayo de otro día
    python config/cursos/recordatorios.py --calendario         # todos los avisos del semestre
    python config/cursos/recordatorios.py --canal campus --confirmar   # publica de verdad

Registro de lo ya enviado: %LOCALAPPDATA%\\cdigital-cun\\recordatorios_enviados.json (fuera del
repositorio, que está en git y sincronizado a Drive). Se puede correr varias veces al día sin
duplicar avisos.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "moodle"))

import fechas_entrega_aca as fea  # noqa: E402

# Cuántos días antes del cierre se avisa. El 0 es el mismo día del cierre.
DIAS_ANTES = (7, 3, 1, 0)
HORA_CIERRE = "23:59"
CARGA = os.path.join(AQUI, "carga_academica_2026.json")
REGISTRO = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
                        "cdigital-cun", "recordatorios_enviados.json")

DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre")


def fecha_larga(f: dt.date) -> str:
    return f"{DIAS[f.weekday()]} {f.day} de {MESES[f.month - 1]} de {f.year}"


def norma(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return " ".join(s.replace("-", " ").split())


# =============================================================================================
# Plan: qué avisos corresponden a un día
# =============================================================================================

class Aviso:
    """Un recordatorio concreto: un ítem, un aula y un motivo."""

    def __init__(self, aula: int, clave: str, grupo: str | None, entrega, motivo: str,
                 dia: dt.date):
        self.aula, self.clave, self.grupo, self.entrega = aula, clave, grupo, entrega
        self.motivo, self.dia = motivo, dia          # motivo: "abre" | "faltan" | "cierra_hoy"

    @property
    def id(self) -> str:
        return f"{self.aula}|{self.entrega.id}|{self.motivo}|{self.dia:%Y-%m-%d}"

    @property
    def dias_para_cierre(self) -> int:
        return (self.entrega.entrega - self.dia).days


def plan(dia: dt.date, aulas: dict) -> list[Aviso]:
    """Los avisos que corresponden a `dia`, en orden de urgencia."""
    fuera: list[Aviso] = []
    for aula, (clave, grupo) in sorted(aulas.items()):
        entregas = fea.entregas_curso(clave)
        if isinstance(entregas, dict):
            entregas = entregas[grupo]
        for e in entregas:
            if e.apertura == dia:
                fuera.append(Aviso(aula, clave, grupo, e, "abre", dia))
            faltan = (e.entrega - dia).days
            # Si el ítem abre hoy, el aviso de apertura ya dice cuándo cierra: no se manda además
            # un «faltan N días» del mismo ítem el mismo día. Pasa en las entregas de ventana corta.
            if faltan in DIAS_ANTES and e.apertura != dia:
                fuera.append(Aviso(aula, clave, grupo, e,
                                   "cierra_hoy" if faltan == 0 else "faltan", dia))
    return sorted(fuera, key=lambda a: (a.dias_para_cierre, a.aula))


# =============================================================================================
# Redacción del aviso
# =============================================================================================

def _docente() -> dict:
    return json.load(open(CARGA, encoding="utf-8"))["docente"]


def _titulo_curso(clave: str) -> str:
    c = json.load(open(CARGA, encoding="utf-8"))["cursos"][clave]
    return c.get("titulo_corto") or clave


def _cuantos_dias(n: int) -> str:
    return "1 día" if n == 1 else f"{n} días"


def asunto(a: Aviso) -> str:
    e = a.entrega
    if a.motivo == "abre":
        return f"Ya está abierta la entrega: {e.label} (cierra el {e.entrega.day} de " \
               f"{MESES[e.entrega.month - 1]})"
    if a.motivo == "cierra_hoy":
        return f"HOY cierra {e.label} · {HORA_CIERRE}"
    return f"Falta{'' if a.dias_para_cierre == 1 else 'n'} {_cuantos_dias(a.dias_para_cierre)} " \
           f"para {e.label} (cierra el {DIAS[e.entrega.weekday()]} {e.entrega.day} de " \
           f"{MESES[e.entrega.month - 1]})"


def cuerpo(a: Aviso, url: str | None) -> str:
    """El HTML del mensaje. Sin adornos: qué es, cuánto pesa, cuándo cierra y dónde se entrega."""
    e, d = a.entrega, _docente()
    esc = html.escape
    if a.motivo == "abre":
        primera = (f"Ya quedó abierta la entrega de <strong>{esc(e.label)}</strong> "
                   f"({esc(e.kind)}, {e.weight:g}% de la nota del corte {e.corte}).")
    elif a.motivo == "cierra_hoy":
        primera = (f"<strong>Hoy es el último día</strong> para entregar "
                   f"<strong>{esc(e.label)}</strong> ({esc(e.kind)}, {e.weight:g}% de la nota "
                   f"del corte {e.corte}). Cierra a las {HORA_CIERRE}.")
    else:
        primera = (f"Les recuerdo que <strong>{esc(e.label)}</strong> ({esc(e.kind)}, "
                   f"{e.weight:g}% de la nota del corte {e.corte}) cierra en "
                   f"<strong>{_cuantos_dias(a.dias_para_cierre)}</strong>.")
    filas = [f"<li>Abre: {fecha_larga(e.apertura)}</li>",
             f"<li><strong>Cierra: {fecha_larga(e.entrega)}, {HORA_CIERRE}</strong></li>"]
    if e.nota_docente:
        filas.append(f"<li>Publico la nota a más tardar el {fecha_larga(e.nota_docente)}</li>")
    # `e.regla` NO va aquí: es la nota interna que explica cómo el Docente fijó las ventanas.
    donde = (f'<p>Se entrega aquí en el aula: <a href="{esc(url)}">{esc(e.label)}</a>.</p>'
             if url else f"<p>Se entrega en el aula, en la actividad «{esc(e.label)}».</p>")
    return ("<p>Buen día,</p>"
            f"<p>{primera}</p><ul>{''.join(filas)}</ul>{donde}"
            "<p>Si algo no les abre o tienen dudas, respondan por este medio o escríbanme a "
            f'<a href="mailto:{esc(d["correo"])}">{esc(d["correo"])}</a>; es mejor preguntar '
            "tres días antes que el mismo día del cierre.</p>"
            f"<p>{esc(d['nombre'])}<br>Docente · {esc(_titulo_curso(a.clave))}</p>")


# =============================================================================================
# Registro de enviados (idempotencia): correr dos veces el mismo día no duplica avisos
# =============================================================================================

def registro_leer() -> dict:
    try:
        return json.load(open(REGISTRO, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def registro_anotar(clave: str, detalle: dict) -> None:
    d = registro_leer()
    d[clave] = detalle
    os.makedirs(os.path.dirname(REGISTRO), exist_ok=True)
    with open(REGISTRO, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1, sort_keys=True)


# =============================================================================================
# Salida
# =============================================================================================

def calendario(aulas: dict, desde: dt.date, hasta: dt.date) -> int:
    """Todos los avisos del semestre, para revisar el plan de un tirón."""
    dia, total = desde, 0
    print(f"Avisos programados del {desde} al {hasta}\n")
    while dia <= hasta:
        avisos = plan(dia, aulas)
        if avisos:
            print(f"{dia:%Y-%m-%d} {DIAS[dia.weekday()][:3]}  "
                  f"({len(avisos)} aviso{'' if len(avisos) == 1 else 's'})")
            for a in avisos:
                print(f"     aula {a.aula} {a.clave:<13} {a.entrega.label:<16} {a.motivo}")
            total += len(avisos)
        dia += dt.timedelta(days=1)
    print(f"\ntotal: {total} avisos en {(hasta - desde).days + 1} días")
    return 0


def correr(dia: dt.date, aulas: dict, canal: str, confirmar: bool, rehacer: bool,
           incluir_ocultos: bool, hasta: dt.date | None = None) -> int:
    """Manda (o simula) los avisos de `dia`. Con `hasta`, los de todo el rango, programados.

    El modo programado es el que hace que esto funcione de verdad sin depender de este computador:
    los avisos se publican de una sola vez con «Mostrar período» en su fecha, y el correo lo suelta
    el cron del campus el día que toca.
    """
    if hasta:
        avisos, d = [], dia
        while d <= hasta:
            avisos += plan(d, aulas)
            d += dt.timedelta(days=1)
        cab = f"Recordatorios del {dia} al {hasta}, PROGRAMADOS en el aula"
    else:
        avisos = plan(dia, aulas)
        cab = f"Recordatorios del {fecha_larga(dia)}"
    print(f"{cab} · canal «{canal}»{' · CONFIRMADO' if confirmar else ' · simulación'}")
    print(f"Fuente de fechas: config/cursos/fechas_entrega_aca.py · {len(avisos)} avisos "
          f"candidatos\n")
    if not avisos:
        print("No toca ningún recordatorio.")
        return 0

    import cdigital as C  # noqa: PLC0415  (sólo hace falta al correr, no al importar el plan)

    ya = registro_leer()
    cd = mods = None
    if canal == "campus":
        cd = C.CDigital()
        cd.entrar()
        print(f"Sesión en CDigital como {cd.nombre}\n")
        mods = {}

    hechos = saltados = fallos = 0
    for a in avisos:
        cab = f"[{a.aula} {a.clave}] {a.entrega.label} · {a.motivo}"
        if not rehacer and a.id in ya:
            print(f"{cab}: ya se envió el {ya[a.id]['cuando'][:16]}, no lo repito")
            saltados += 1
            continue

        url = None
        if canal == "campus":
            if a.aula not in mods:
                mods[a.aula] = {norma(c.get("name")): c
                                for c in cd.estado_curso(a.aula).get("cm", [])}
            cm = mods[a.aula].get(norma(a.entrega.code))
            if not cm:
                print(f"{cab}: no encuentro la actividad «{a.entrega.code}» en el aula")
                fallos += 1
                continue
            if not cm.get("visible") and not incluir_ocultos:
                print(f"{cab}: la actividad está OCULTA (cmid {cm['id']}); no aviso de algo que el "
                      "estudiante no puede abrir")
                saltados += 1
                continue
            url = f"{cd.base}/mod/{cm['module']}/view.php?id={cm['id']}"

        print(cab)
        s, c = asunto(a), cuerpo(a, url)
        if canal == "simular":
            print(f"   asunto: {s}")
            for linea in c.replace("</p>", "\n").replace("</li>", "\n").split("\n"):
                t = html.unescape(re.sub(r"<[^>]+>", "", linea)).strip()
                if t:
                    print(f"   | {t}")
            print()
            hechos += 1
            continue

        r = C.publicar_aviso(cd, a.aula, s, c, confirmar,
                             desde=a.dia if hasta else None)
        if r:
            fallos += 1
        else:
            hechos += 1
            if confirmar:
                registro_anotar(a.id, {"cuando": dt.datetime.now().isoformat(timespec="seconds"),
                                       "asunto": s, "aula": a.aula, "item": a.entrega.id})
        print()

    verbo = "publicados" if (canal == "campus" and confirmar) else "listos para publicar"
    print(f"{verbo}: {hechos} · saltados: {saltados} · con problema: {fallos}")
    if canal == "simular" or not confirmar:
        print("Nada salió del computador. Para publicar de verdad: --canal campus --confirmar")
    return 1 if fallos else 0


def main(argv: list[str]) -> int:
    import cdigital as C
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--fecha", help="Día a evaluar (AAAA-MM-DD). Por defecto, hoy")
    p.add_argument("--aula", type=int, action="append",
                   help="Sólo esta aula de CDigital (repetible). Por defecto, las 7")
    p.add_argument("--canal", choices=("simular", "campus"), default="simular",
                   help="«simular» imprime; «campus» publica en el foro Avisos del aula")
    p.add_argument("--confirmar", action="store_true",
                   help="Publica de verdad. Sin esto no sale nada, aunque el canal sea campus")
    p.add_argument("--rehacer", action="store_true",
                   help="Ignora el registro de enviados y vuelve a mandar")
    p.add_argument("--incluir-ocultos", action="store_true",
                   help="Avisa también de actividades ocultas (el enlace no les abrirá)")
    p.add_argument("--calendario", action="store_true",
                   help="En vez de correr hoy, lista todos los avisos hasta fin de semestre")
    p.add_argument("--programar", action="store_true",
                   help="Publica de una vez los avisos de todo el rango, cada uno con «Mostrar "
                        "período» en su fecha: el correo lo suelta el cron del campus el día que "
                        "toca, sin que este computador tenga que estar encendido")
    p.add_argument("--hasta", help="Último día a programar (AAAA-MM-DD). Por defecto, el último "
                                   "cierre del semestre")
    a = p.parse_args(argv)

    aulas = dict(C.AULAS_CURSO)
    if a.aula:
        aulas = {k: v for k, v in aulas.items() if k in a.aula}
        if not aulas:
            print(f"Ninguna de esas aulas está en AULAS_CURSO: {sorted(C.AULAS_CURSO)}")
            return 1
    hoy = dt.date.fromisoformat(a.fecha) if a.fecha else dt.date.today()

    def ultimo_cierre() -> dt.date:
        return max(e.entrega for k, g in aulas.values()
                   for e in (fea.entregas_curso(k)[g] if isinstance(fea.entregas_curso(k), dict)
                             else fea.entregas_curso(k)))

    if a.calendario:
        return calendario(aulas, hoy, ultimo_cierre())
    hasta = None
    if a.programar:
        hasta = dt.date.fromisoformat(a.hasta) if a.hasta else ultimo_cierre()
        if a.canal != "campus":
            print("--programar sólo tiene sentido con --canal campus (lo programa el aula).")
            return 1
    return correr(hoy, aulas, a.canal, a.confirmar, a.rehacer, a.incluir_ocultos, hasta)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
