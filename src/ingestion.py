import fitz  # PyMuPDF
import json
import os
from pathlib import Path
from typing import List, Dict

from config import PROCESSED_DIR


def process_pdf(pdf_path: str) -> Path:
    """
    Extract text from PDF and save chunks for THIS PDF ONLY.
    Returns path to chunk file.
    """

    doc = fitz.open(pdf_path)
    chunks: List[Dict] = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            chunks.append({
                "page": page_num,
                "type": "text",
                "content": text
            })

    # 🔑 IMPORTANT: unique chunk file per PDF
    pdf_name = Path(pdf_path).stem
    chunk_path = PROCESSED_DIR / f"{pdf_name}_chunks.json"

    with open(chunk_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return chunk_path
