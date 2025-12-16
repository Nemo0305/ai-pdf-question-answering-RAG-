import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

from config import EMBEDDING_MODEL_NAME


class Retriever:
    def __init__(self, index_path: Path, meta_path: Path, top_k: int = 6):
        self.index = faiss.read_index(str(index_path))
        self.metadata = json.load(open(meta_path, "r", encoding="utf-8"))
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.top_k = top_k

    def search(self, query: str):
        query_vec = self.model.encode([query])
        query_vec = np.array(query_vec, dtype="float32")

        scores, indices = self.index.search(query_vec, self.top_k)

        results = []
        for idx in indices[0]:
            results.append(self.metadata[idx])

        return results
