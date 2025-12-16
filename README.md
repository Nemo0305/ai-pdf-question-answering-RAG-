📄 AI PDF Question Answering System (RAG + OCR)

A Document Intelligence system that allows users to upload any PDF document (text-based or scanned), automatically processes it using OCR + embeddings, and enables context-aware question answering using a Retrieval-Augmented Generation (RAG) pipeline.

Built with Streamlit, FAISS, Sentence Transformers, and Google Gemini (2.5 Flash).

🚀 Features

📤 Upload any PDF document (reports, standards, research papers, scanned PDFs)

🔍 Automatic text extraction + OCR (for image-based PDFs)

🧠 Semantic search using SentenceTransformer embeddings

📚 Context-aware answers using RAG architecture

✨ Answers are strictly grounded in the uploaded document

⚡ Fast and lightweight (optimized for local systems)

🎨 Clean, professional Streamlit UI

🧠 Architecture Overview
User PDF Upload
      ↓
PDF Parsing (Text + OCR)
      ↓
Chunking & Embeddings
      ↓
FAISS Vector Index
      ↓
Relevant Context Retrieval
      ↓
Gemini LLM Answer Generation

🛠️ Tech Stack
| Component   | Technology                     |
| ----------- | ------------------------------ |
| UI          | Streamlit                      |
| PDF Parsing | PyMuPDF (fitz), Tesseract OCR  |
| Embeddings  | Sentence-Transformers (MiniLM) |
| Vector DB   | FAISS                          |
| LLM         | Google Gemini 2.5 Flash        |
| Language    | Python                         |

📂 Project Structure
ai-pdf-question-answering-rag/
│
├── src/
│   ├── app_streamlit.py     # Streamlit UI
│   ├── ingestion.py         # PDF + OCR processing
│   ├── embeddings.py        # Embedding & FAISS indexing
│   ├── retrieval.py         # Context retrieval
│   ├── qa_engine.py         # RAG + Gemini logic
│   ├── session_index.py     # Per-session index handling
│   └── config.py            # Paths & configurations
│
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/ai-pdf-question-answering-rag.git
cd ai-pdf-question-answering-rag

2️⃣ Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Install Tesseract OCR
🔹 Windows

Download from:
https://github.com/UB-Mannheim/tesseract/wiki

Install and note the path, e.g.:

C:\Program Files\Tesseract-OCR\tesseract.exe


Add it to System PATH

Verify:

tesseract --version

5️⃣ Set Environment Variables

Create a .env file:

GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

▶️ Run the Application
streamlit run src/app_streamlit.py


Then open:

http://localhost:8501

🧪 Example Questions

Summarize this document

What are the key findings?

What risks are discussed?

Explain the methodology used

Give an executive summary

⚠️ Important Notes

Answers are generated only from the uploaded document

No external knowledge is used

OCR ensures support for scanned PDFs

Results may require human verification

🎓 Academic Relevance

This project demonstrates:

Retrieval-Augmented Generation (RAG)

Semantic Search with FAISS

OCR-based document intelligence

Real-world LLM integration

End-to-end AI system design

👨‍💻 Author

Manindra Ch Paul
M.Tech Student
Institute of Engineering & Management (IEM), Kolkata