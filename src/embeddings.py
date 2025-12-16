import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

from config import VECTOR_DB_DIR, EMBEDDING_MODEL_NAME


def build_index(chunk_file: Path):
    """
    Build FAISS index ONLY for the given PDF
    """

    with open(chunk_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["content"] for c in chunks]

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embeddings = model.encode(texts, show_progress_bar=False)
    embeddings = np.array(embeddings, dtype="float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # 🔑 unique index per PDF
    index_path = VECTOR_DB_DIR / f"{chunk_file.stem}.faiss"
    meta_path = VECTOR_DB_DIR / f"{chunk_file.stem}_meta.json"

    faiss.write_index(index, str(index_path))
    json.dump(chunks, open(meta_path, "w", encoding="utf-8"), indent=2)

    return index_path, meta_path
