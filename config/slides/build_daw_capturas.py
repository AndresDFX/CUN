# -*- coding: utf-8 -*-
"""
Genera los "pantallazos" de CONSOLA JavaScript (examlab) para los guiones del curso
Desarrollo de Aplicaciones Web. Salida: Clases/Version vigente (nuevo dictado 2026)/Guiones/Capturas/<id>.png
(comandos y salida EXACTOS; se enlazan en los guiones con [[captura: <id>.png]]).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terminal_shot import render_many

DEST = r"g:\My Drive\Trabajos\Empleo\FESNA\Cursos\Desarrollo de Aplicaciones Web\Clases\Version vigente (nuevo dictado 2026)\Guiones\Capturas"
ENV = "Consola JavaScript · examlab"
PROMPT = "›"

SPECS = [
    # ---- Sesión 1: variables, tipos, template literals, === vs ==, función ----
    {"id": "js_s1_tipos", "title": "Variables, tipos y funciones", "env": ENV, "prompt": PROMPT,
     "lines": [
        {"t": "cmd", "text": "const nombre = 'Ana'; let edad = 20;"},
        {"t": "cmd", "text": "console.log(typeof nombre, typeof edad);"},
        {"t": "out", "text": "string number"},
        {"t": "cmd", "text": "console.log(`Hola ${nombre}, tienes ${edad} años`);"},
        {"t": "out", "text": "Hola Ana, tienes 20 años", "hl": True},
        {"t": "cmd", "text": "console.log(0 == '', 0 === '');"},
        {"t": "out", "text": "true false"},
        {"t": "cmd", "text": "function esMayor(e){ return e >= 18; }"},
        {"t": "cmd", "text": "console.log(esMayor(edad));"},
        {"t": "out", "text": "true", "hl": True},
     ]},
    # ---- Sesión 3: arreglos, map/filter/reduce ----
    {"id": "js_s3_arreglos", "title": "Arreglos: map, filter, reduce", "env": ENV, "prompt": PROMPT,
     "lines": [
        {"t": "cmd", "text": "const nums = [1, 2, 3, 4, 5];"},
        {"t": "cmd", "text": "console.log(nums.length, nums[0]);"},
        {"t": "out", "text": "5 1"},
        {"t": "cmd", "text": "const dobles = nums.map(n => n * 2);"},
        {"t": "cmd", "text": "console.log(dobles);"},
        {"t": "out", "text": "[ 2, 4, 6, 8, 10 ]", "hl": True},
        {"t": "cmd", "text": "const pares = nums.filter(n => n % 2 === 0);"},
        {"t": "cmd", "text": "console.log(pares);"},
        {"t": "out", "text": "[ 2, 4 ]"},
        {"t": "cmd", "text": "const suma = nums.reduce((a, n) => a + n, 0);"},
        {"t": "cmd", "text": "console.log(suma);"},
        {"t": "out", "text": "15", "hl": True},
     ]},
    # ---- Sesión 4: ES6 (arrow, destructuring, spread) ----
    {"id": "js_s4_es6", "title": "ES6: arrow, destructuring, spread", "env": ENV, "prompt": PROMPT,
     "lines": [
        {"t": "cmd", "text": "const usuario = { nombre: 'Ana', rol: 'dev' };"},
        {"t": "cmd", "text": "const { nombre, rol } = usuario;"},
        {"t": "cmd", "text": "console.log(nombre, rol);"},
        {"t": "out", "text": "Ana dev", "hl": True},
        {"t": "cmd", "text": "const base = [1, 2]; const mas = [...base, 3, 4];"},
        {"t": "cmd", "text": "console.log(mas);"},
        {"t": "out", "text": "[ 1, 2, 3, 4 ]", "hl": True},
        {"t": "cmd", "text": "const saludar = (n) => `Hola ${n}`;"},
        {"t": "cmd", "text": "console.log(saludar(nombre));"},
        {"t": "out", "text": "Hola Ana"},
     ]},
]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    done = render_many(SPECS, DEST)
    for p in done:
        print("OK", p)
