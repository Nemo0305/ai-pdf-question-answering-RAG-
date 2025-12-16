📘 AI PDF Question Answering System (RAG-based)

An end-to-end Retrieval-Augmented Generation (RAG) system that allows users to upload any PDF document and ask natural language questions, with answers generated strictly from the uploaded document.

The system dynamically processes each uploaded PDF, builds a document-specific semantic index, and generates contextual, multi-sentence answers using modern embedding models and large language models.

🚀 Key Features

📄 User PDF Upload (any document)

🔍 Document-grounded Question Answering

🧠 Retrieval-Augmented Generation (RAG)

♻️ No context leakage between PDFs

🧩 Dynamic indexing per document

✨ Clean, professional Streamlit UI

⚡ Fast semantic search using FAISS

🤖 Answer generation using Gemini 2.5 Flash

🛡️ Hallucination-controlled (context-only answers)

🧠 System Architecture
User PDF
   ↓
PDF Ingestion (PyMuPDF)
   ↓
Text Chunking
   ↓
Sentence Embeddings
   ↓
FAISS Vector Index (per PDF)
   ↓
Semantic Retrieval
   ↓
LLM (Gemini 2.5 Flash)
   ↓
Contextual Answer

🛠️ Tech Stack
Component	Technology
UI	Streamlit
PDF Processing	PyMuPDF
Embeddings	Sentence-Transformers
Vector Store	FAISS
LLM	Gemini 2.5 Flash
Backend	Python
Env Management	python-dotenv
📂 Project Structure
multi_modal_rag/
│
├── src/
│   ├── app_streamlit.py      # Streamlit UI
│   ├── ingestion.py          # PDF ingestion & chunking
│   ├── embeddings.py         # Embedding + FAISS indexing
│   ├── retrieval.py          # Semantic retrieval
│   ├── qa_engine.py          # RAG-based QA logic
│   ├── config.py             # Paths & configuration
│
├── data/
│   ├── processed/            # Generated text chunks
│
├── vector_store/             # FAISS indexes (per PDF)
│
├── .env                      # API keys
├── requirements.txt
└── README.md

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone <your-repo-url>
cd multi_modal_rag

2️⃣ Create & Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate    # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in the project root:

GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash

▶️ Run the Application
streamlit run src/app_streamlit.py


Then open the browser at:

http://localhost:8501

🧪 How to Use

Upload any PDF document

Wait for processing & indexing

Ask questions like:

Summarize this document

What are the key findings?

What risks are discussed?

Give an executive summary

Receive document-grounded, multi-sentence answers

🔒 Important Design Decisions

Each uploaded PDF gets a fresh vector index

Old document embeddings are discarded

Prevents cross-document contamination

QA engine is instantiated per document

Summaries and answers are generated only from retrieved context

⚠️ Disclaimer

Answers are generated solely from the uploaded document and may require human verification for critical use cases.

🎓 Academic / Interview Highlights

Implements true RAG architecture

Avoids common pitfalls like context leakage

Demonstrates understanding of:

Semantic search

Vector databases

Prompt engineering

LLM grounding

UI/UX for ML systems

👨‍💻 Author

Manindra Ch Paul
M.Tech Student
Institute of Engineering & Management (IEM), Kolkata