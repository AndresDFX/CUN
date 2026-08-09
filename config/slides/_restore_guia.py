# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(
    r"C:\Users\Andre\.cursor\projects\g-Mi-unidad-Trabajos-Empleo-CUN-Cursos"
    r"\agent-transcripts\ba52933b-6dbc-4709-ac1a-41fce23b11e6"
    r"\subagents\5f788633-f998-403c-9b63-f88a4dce3b79.jsonl"
)
out_tg3 = Path(
    r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\Pregrado"
    r"\TRABAJO DE GRADO 3 - MODELOS DE INNOVACION INGENIERIA DE SISTEMAS\Guiones"
)
found = {}
for line in p.read_text(encoding="utf-8").splitlines():
    if "Herramientas de escritura" not in line:
        continue
    try:
        obj = json.loads(line)
    except Exception:
        continue
    msg = obj.get("message", {})
    content = msg.get("content")
    if not isinstance(content, list):
        continue
    for part in content:
        if part.get("type") != "tool_use" or part.get("name") != "Write":
            continue
        inp = part.get("input", {})
        path = inp.get("path", "")
        if "Herramientas de escritura" in path and path.endswith(".md"):
            found[path] = inp.get("contents", "")
            print("FOUND", path, "len", len(found[path]))

for path, contents in found.items():
    Path(path).write_text(contents, encoding="utf-8")
    print("RESTORED", path)

tg2 = [k for k in found if "TRABAJO DE GRADO 2" in k]
tg3 = [k for k in found if "TRABAJO DE GRADO 3" in k]
if tg2 and not tg3:
    src = found[tg2[0]]
    dst = out_tg3 / "Guía práctica - Herramientas de escritura y citación.md"
    text = src.replace("TG2", "TG3").replace("de TG2", "de TG3")
    dst.write_text(text, encoding="utf-8")
    print("RESTORED from TG2 template", dst)

# Convert docx if possible
import sys
conv = Path(r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\config\slides\guion_md_a_docx.py")
sys.path.insert(0, str(conv.parent))
import importlib.util
spec = importlib.util.spec_from_file_location("guion_md_a_docx", conv)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for folder_name in ("TRABAJO DE GRADO 2", "TRABAJO DE GRADO 3"):
    base = Path(r"G:\Mi unidad\Trabajos\Empleo\CUN\Cursos\Pregrado")
    # find folder
    for d in base.iterdir():
        if d.is_dir() and folder_name in d.name:
            md = d / "Guiones" / "Guía práctica - Herramientas de escritura y citación.md"
            if md.exists():
                docx = md.with_suffix(".docx")
                mod.convert(str(md), str(docx))
                print("DOCX", docx)
