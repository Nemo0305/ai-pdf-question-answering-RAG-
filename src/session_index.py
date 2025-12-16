import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# ================= CONFIG =================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 32


def build_temp_index(chunks: List[Dict]):
    """
    Build a FAISS index from text chunks.

    Args:
        chunks (List[Dict]): List of chunks with 'content', 'page', etc.

    Returns:
        index (faiss.Index): FAISS vector index
        metadata (List[Dict]): Original chunk metadata
    """

    # 1️⃣ Load embedding model (FAST)
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # 2️⃣ Extract text from chunks
    texts = [chunk["content"] for chunk in chunks]

    # 3️⃣ Generate embeddings (BATCHED + NORMALIZED)
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    embeddings = np.array(embeddings).astype("float32")

    # 4️⃣ Create FAISS index
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)

    # 5️⃣ Return index + metadata
    return index, chunks
