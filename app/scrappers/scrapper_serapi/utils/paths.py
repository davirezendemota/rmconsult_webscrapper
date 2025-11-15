from pathlib import Path

# Base do projeto (pasta raiz)
BASE_DIR = Path(__file__).resolve().parents[4]

# Pasta raiz de storage
STORAGE_DIR = BASE_DIR / "storage"

# Pasta onde ficam os resultados dos scrapers
RESULTADOS_DIR = STORAGE_DIR / "resultados"

# Garantir que existe
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
