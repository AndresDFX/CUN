# -*- coding: utf-8 -*-
"""Realinea la sección 'Narración de las diapositivas' de cada guion .md al deck
ampliado de 15 slides (portada + propósito + 10 de contenido + autónomo + logros + cierre),
usando los títulos reales del JSON de contenido. Luego se regeneran los .docx."""
import os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SLIDES = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(SLIDES, "content")
CURSOS = r"g:\My Drive\Trabajos\Empleo\FESNA\Cursos"

GUIONES = {
 "cableado": (os.path.join(CURSOS, "Cableado Estructurado", "Guiones"), {
   1: "Guion Docente Sesion 1 - Fundamentos de Redes y Medios Fisicos.md",
   2: "Guion Docente Sesion 2 - La Capa de Red - Direccionamiento IP y Subredes.md",
   3: "Guion Docente Sesion 3 - Capas de Transporte y Aplicacion.md",
   4: "Guion Docente Sesion 4 - Servicios de Red - DNS DHCP NAT y VPN.md",
   5: "Guion Docente Sesion 5 - Conexion a Internet - Banda Ancha Fibra e Inalambricas.md",
   6: "Guion Docente Sesion 6 - Solucion de Problemas de Red y el Futuro - Nube e IPv6.md",
 }),
 "servidor": (os.path.join(CURSOS, "Administración de Sistemas Operativos de Servidor", "Guiones"), {
   1: "Guion Docente Sesion 1 - Administracion por Consola del Servidor.md",
   2: "Guion Docente Sesion 2 - Usuarios Grupos y Permisos del Servidor.md",
   3: "Guion Docente Sesion 3 - Gestion de Software y Servicios.md",
   4: "Guion Docente Sesion 4 - Almacenamiento del Servidor.md",
   5: "Guion Docente Sesion 5 - Procesos Recursos y Tareas Programadas.md",
   6: "Guion Docente Sesion 6 - Redes Logs Respaldos y Troubleshooting.md",
 }),
}

def clean(t):
    t = re.sub(r'\*\*(.*?)\*\*', r'\1', t)
    t = t.replace("@@", "").replace("`", "")
    return re.sub(r'\s+', ' ', t).strip()

def hint(sl):
    if sl.get("type") == "table":
        h = "compara " + " / ".join(clean(x) for x in sl.get("headers", [])[:3])
        if sl.get("note"):
            h += ". " + clean(sl["note"])
        return h
    for b in sl.get("bullets", []):
        if isinstance(b, str) and b.strip():
            return clean(b)
    return "concepto clave de la sesión."

def build_section(content):
    total = 5 + len(content)  # portada + propósito + contenido + autónomo + logros + cierre
    L = ["", "---", "", f"## 🎬 Guía de las diapositivas (deck de {total} · marca FESNA)", "",
         f"> El deck de esta sesión tiene **{total} diapositivas**. El *qué decir* a fondo está en el "
         "Fundamento Teórico y el Plan de Clase de arriba; aquí va la SECUENCIA y el foco de cada una.", "",
         "1. **Portada** — \"SESIÓN N\": título, nivel y frase gancho. Bienvenida y objetivo del día.",
         "2. **El propósito de hoy** — objetivo de la tutoría (verbo + contexto) y niveles de logro (1/2/3)."]
    n = 3
    for sl in content:
        h = hint(sl)
        if len(h) > 160:
            h = h[:157].rstrip() + "…"
        L.append(f"{n}. **{clean(sl['title'])}** — {h}")
        n += 1
    L.append(f"{n}. **Trabajo autónomo (15 min)** — la actividad individual; se resuelve en examlab (Lab) "
             f"o en la herramienta en línea y se sube a examlab.")
    L.append(f"{n+1}. **¿Qué logramos hoy?** — repaso de lo alcanzado + **quiz** de conceptos en examlab (Test).")
    L.append(f"{n+2}. **Cierre** — 3 puntos clave, entregable en examlab y puente a la próxima sesión.")
    L.append("")
    return "\n".join(L)

HDR = re.compile(r'Narraci[oó]n de las [dD]iapositivas|Gu[ií]a de las diapositivas')

def main():
    done = 0
    for slug, (folder, files) in GUIONES.items():
        for n, fn in files.items():
            jp = os.path.join(CONTENT, f"{slug}_s{n}.json")
            md = os.path.join(folder, fn)
            if not (os.path.exists(jp) and os.path.exists(md)):
                print("  falta:", slug, n); continue
            content = json.load(open(jp, encoding="utf-8"))
            raw = open(md, encoding="utf-8").read().split("\n")
            cut = next((i for i, ln in enumerate(raw) if HDR.search(ln)), None)
            if cut is None:
                print("  sin narración:", fn); continue
            head = raw[:cut]
            # quitar separadores/blancos colgantes al final del head
            while head and head[-1].strip() in ("", "---"):
                head.pop()
            new = "\n".join(head) + "\n" + build_section(content)
            open(md, "w", encoding="utf-8").write(new)
            done += 1
            print(f"  ✓ {slug} s{n}: narración → 15 slides ({len(content)} de contenido)")
    print("Realineados:", done)

if __name__ == "__main__":
    main()
