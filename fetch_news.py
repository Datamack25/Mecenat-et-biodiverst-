import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent if (HERE.parent / "core.py").exists() else HERE))  # marche dans scripts/ ou à la racine
import core
print(core.fetch_news())
