import os
import sys
from typing import Dict, List
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

# Allow absolute imports
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from retrieval import Retriever
from ingestion import process_pdf
from embeddings import build_index

# --------------------------------------------------
# Environment setup
# --------------------------------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

genai.configure(api_key=GOOGLE_API_KEY)


# --------------------------------------------------
# LLM Call
# --------------------------------------------------
def call_llm(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": 0.25,
                "max_output_tokens": 1800,
                "top_p": 0.9,
            },
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[LLM ERROR]: {e}"


# --------------------------------------------------
# QA System (RAG)
# --------------------------------------------------
class QASystem:
    def __init__(self, index_path: Path, meta_path: Path, top_k: int = 6):
        self.retriever = Retriever(index_path, meta_path, top_k)

    def _build_context(self, contexts: List[Dict]) -> str:
        blocks = []
        for c in contexts:
            blocks.append(f"(Page {c['page']}) {c['content']}")
        return "\n\n".join(blocks)

    def answer(self, question: str) -> Dict:
        contexts = self.retriever.search(question)

        if not contexts:
            return {
                "answer": "No relevant information found in the document.",
                "contexts": [],
            }

        context_text = self._build_context(contexts)

        prompt = f"""
You are a professional document analyst.

Using ONLY the information from the context below,
answer the user's question in a clear, well-structured manner.

STRICT RULES:
- Write a MINIMUM of 6 complete sentences
- Each sentence must add new information
- Do NOT stop early
- Do NOT give a definition-only answer
- Do NOT use outside knowledge
- Base every claim strictly on the context

Context:
----------------
{context_text}
----------------

Question:
{question}

Answer:
"""

        answer = call_llm(prompt)

        return {
            "answer": answer,
            "contexts": contexts,
        }


# --------------------------------------------------
# SAFE CLI TEST (OPTIONAL)
# --------------------------------------------------
if __name__ == "__main__":
    """
    This block is ONLY for debugging.
    It will NOT be used by Streamlit.
    """

    sample_pdf = BASE_DIR + "/data/sample.pdf"

    if not os.path.exists(sample_pdf):
        print("❌ sample.pdf not found. Place a PDF at data/sample.pdf to test.")
        sys.exit(0)

    print("🔹 Processing PDF...")
    chunk_file = process_pdf(sample_pdf)

    print("🔹 Building index...")
    index_path, meta_path = build_index(chunk_file)

    print("🔹 Initializing QA system...")
    qa = QASystem(index_path, meta_path)

    print("\n--- ANSWER START ---\n")
    print(qa.answer("Summarize this document")["answer"])
    print("\n--- ANSWER END ---\n")
