# -*- coding: utf-8 -*-
from datetime import date, timedelta

DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


def snap(target: date, weekday: int) -> date:
    """Día de clase (weekday) en o antes de target."""
    return target - timedelta(days=(target.weekday() - weekday) % 7)


def compute(inicio, recepcion, cierre, weekday, weights, labels):
    span = (recepcion - inicio).days
    total_w = sum(weights)
    cum = 0
    prev = inicio - timedelta(days=1)
    out = []
    for i, (lab, w) in enumerate(zip(labels, weights)):
        cum += w
        if i == len(weights) - 1:
            target = recepcion
        else:
            target = inicio + timedelta(days=round(span * cum / total_w))
        d = snap(target, weekday)
        if d < inicio:
            d = snap(inicio + timedelta(days=6), weekday)
            if d < inicio:
                d = inicio + timedelta(days=(weekday - inicio.weekday()) % 7)
        if d <= prev:
            # siguiente día de clase
            d = prev + timedelta(days=7)
            d = snap(d, weekday)
        if d > recepcion:
            d = snap(recepcion, weekday)
        out.append((lab, w, d))
        prev = d
    return out, span


courses = [
    ("P1", date(2026, 8, 10), date(2026, 11, 14), date(2026, 11, 22), 0, [25, 25, 42], ["ACA1", "ACA2", "ACA3"]),
    ("INV", date(2026, 8, 10), date(2026, 9, 12), date(2026, 9, 20), 3, [30, 30, 40], ["C1", "C2", "C3"]),
    ("CRE", date(2026, 8, 10), date(2026, 9, 19), date(2026, 9, 27), 2, [30, 30, 40], ["C1", "C2", "C3"]),
    ("TG2", date(2026, 8, 10), date(2026, 11, 14), date(2026, 11, 22), 0, [30, 30, 40], ["C1", "C2", "C3"]),
    ("TG3-50", date(2026, 8, 10), date(2026, 11, 7), date(2026, 11, 15), 1, [50, 50], ["EV05", "EXAM"]),
    ("TG3-66", date(2026, 8, 10), date(2026, 11, 14), date(2026, 11, 22), 1, [50, 50], ["EV05", "EXAM"]),
]

for name, ini, rec, cie, wd, ws, labs in courses:
    rows, span = compute(ini, rec, cie, wd, ws, labs)
    print(f"\n{name} span={span}d class={DIAS[wd]} inicio={ini} recepcion={rec} cierre={cie}")
    prev_end = ini
    for lab, w, d in rows:
        nota = snap(d + timedelta(days=7), wd)
        if nota <= d:
            nota = d + timedelta(days=7)
        print(f"  {lab} {w}% entrega={d.isoformat()} ({DIAS[d.weekday()]}) nota_doc={nota.isoformat()} ventana={prev_end}..{d}")
        prev_end = d + timedelta(days=1)
    if name == "P1":
        aca3 = rows[-1][2]
        coev_ini = aca3 + timedelta(days=1)
        coev_fin = snap(min(cie - timedelta(days=7), aca3 + timedelta(days=7)), 0)
        if coev_fin < coev_ini:
            coev_fin = coev_ini + timedelta(days=6)
        auto_ini = coev_fin + timedelta(days=1)
        auto_fin = cie
        print(f"  Coev {coev_ini}..{coev_fin}  Auto {auto_ini}..{auto_fin}")
