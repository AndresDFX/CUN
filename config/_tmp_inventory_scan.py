# temporary inventory helper — safe to delete after scan
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "config" / "cursos"))
sys.path.insert(0, str(ROOT / "config" / "slides"))
from sesiones_cun import COURSES  # noqa: E402
from build_sesion_material import session_folder_name  # noqa: E402


def main() -> None:
    for key, c in COURSES.items():
        folder = Path(c["folder"])
        clases = folder / "Clases"
        print(f"\n## {key}")
        expected = {session_folder_name(s["n"], s["titulo"]) for s in c["sesiones"]}
        actual = {
            p.name
            for p in clases.iterdir()
            if p.is_dir() and p.name.startswith("Sesion")
        }
        print("EXPECTED:")
        for name in sorted(expected):
            print(f"  {name}")
        print("ACTUAL:")
        for name in sorted(actual):
            print(f"  {name}")
        orphans = actual - expected
        missing = expected - actual
        if orphans:
            print("ORPHANS (cleanup candidates):")
            for name in sorted(orphans):
                p = clases / name
                files = [str(x.relative_to(p)) for x in p.rglob("*") if x.is_file()]
                print(f"  {name}")
                print(f"    -> {files}")
        if missing:
            print("MISSING expected folders:")
            for name in sorted(missing):
                print(f"  {name}")


if __name__ == "__main__":
    main()
