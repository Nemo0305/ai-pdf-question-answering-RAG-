from pathlib import Path
import os

# ================= PATHS =================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = BASE_DIR / "vector_store"

# ================= MODELS =================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GEMINI_MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "models/gemini-2.5-flash"
)

# ================= ENSURE DIRS =================
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
