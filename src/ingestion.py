import os
import sys
import json
from pathlib import Path
from typing import List, Dict

import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path
# Allow absolute imports
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config import PROCESSED_DIR

# -----------------------------
# Configuration
# -----------------------------
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


# -----------------------------
# Utilities
# -----------------------------
def chunk_text(text: str, page: int, chunk_type: str) -> List[Dict]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "page": page,
                "type": chunk_type,
                "content": chunk
            })

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# -----------------------------
# Extract digital text
# -----------------------------
def extract_text_chunks(pdf_path: Path) -> List[Dict]:
    doc = fitz.open(pdf_path)
    all_chunks = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")

        if text.strip():
            all_chunks.extend(
                chunk_text(text, page_num, "text")
            )

    return all_chunks


# -----------------------------
# OCR for scanned pages/images
# -----------------------------
def extract_ocr_chunks(pdf_path: Path) -> List[Dict]:
    all_chunks = []

    try:
        images = convert_from_path(str(pdf_path), dpi=300)

        for page_num, img in enumerate(images, start=1):
            ocr_text = pytesseract.image_to_string(img)

            if ocr_text.strip():
                all_chunks.extend(
                    chunk_text(ocr_text, page_num, "ocr")
                )

    except Exception as e:
        print(f"OCR skipped: {e}")

    return all_chunks


# -----------------------------
# Main ingestion pipeline
# -----------------------------
def process_pdf(pdf_path: Path) -> Path: 
    pdf_path = Path(pdf_path)
    print(f"Processing PDF: {pdf_path.name}")


    text_chunks = extract_text_chunks(pdf_path)
    ocr_chunks = extract_ocr_chunks(pdf_path)

    all_chunks = text_chunks + ocr_chunks

    if not all_chunks:
        raise ValueError("No content extracted from PDF.")

    output_path = PROCESSED_DIR / "document_chunks.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_chunks)} chunks → {output_path}")
    return output_path


