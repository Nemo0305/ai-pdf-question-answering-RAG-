import streamlit as st
import tempfile

from ingestion import process_pdf
from embeddings import build_index
from qa_engine import QASystem

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Document Intelligence | AI PDF QA",
    page_icon="📘",
    layout="wide",
)

# --------------------------------------------------
# Custom CSS (Clean & Minimal)
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(120deg, #eef2f7, #dbeafe);
    }

    .block-container {
        padding-top: 2.5rem;
    }

    /* Title */
    .title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #0f172a;
        margin-bottom: 6px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #475569;
        margin-bottom: 36px;
    }

    /* Upload section */
    .upload-box {
        text-align: center;
        padding: 32px;
        border-radius: 18px;
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(4px);
        margin-bottom: 32px;
    }

    /* Answer box */
    .answer-box {
        background: #ffffff;
        border-left: 6px solid #2563eb;
        padding: 22px;
        border-radius: 14px;
        font-size: 16px;
        line-height: 1.75;
        color: #0f172a;
        white-space: pre-wrap;
        box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #020617);
        color: white;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
        border: none;
    }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 13px;
        color: #64748b;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Sidebar (UNCHANGED – already good)
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 📘 Document Intelligence")
    st.markdown(
        """
        **How it works**
        1. Upload a PDF  
        2. AI indexes the document  
        3. Ask natural questions  
        4. Answers are document-grounded  
        """
    )

    st.markdown("---")

    st.markdown("### 💡 Sample Questions")
    st.markdown(
        """
        • Summarize this document  
        • What are the key findings?  
        • What risks are discussed?  
        • Give an executive summary  
        """
    )

    st.markdown("---")

    st.markdown(
        """
        **Built by**  
        **Manindra Ch Paul**  
        M.Tech Student  
        Institute of Engineering & Management  
        Kolkata
        """
    )

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown("<div class='title'>📘 AI Document Question Answering</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Upload any PDF and extract reliable, document-grounded insights</div>",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "qa" not in st.session_state:
    st.session_state.qa = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

# --------------------------------------------------
# Upload Section (NO WHITE CARD)
# --------------------------------------------------
st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
st.markdown("### 📤 Upload a PDF Document")

uploaded_file = st.file_uploader(
    "",
    type=["pdf"],
    label_visibility="collapsed",
)

if uploaded_file:
    st.success(f"Uploaded **{uploaded_file.name}**")

    if st.session_state.pdf_name != uploaded_file.name:
        with st.spinner("Processing document..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name

            chunk_file = process_pdf(pdf_path)
            index_path, meta_path = build_index(chunk_file)

            st.session_state.qa = QASystem(index_path, meta_path)
            st.session_state.pdf_name = uploaded_file.name

        st.success("Document ready. Ask your questions below.")

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Question Input (NO CARD)
# --------------------------------------------------
st.markdown("### 💬 Ask a Question")

question = st.text_input(
    "",
    placeholder="e.g. Summarize this document",
)

ask_btn = st.button("Generate Answer")

# --------------------------------------------------
# Answer (ONLY IMPORTANT CARD)
# --------------------------------------------------
if ask_btn:
    if not uploaded_file:
        st.warning("Please upload a PDF first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            result = st.session_state.qa.answer(question)

        st.markdown("### ✅ Answer")
        st.markdown(
            f"<div class='answer-box'>{result['answer']}</div>",
            unsafe_allow_html=True,
        )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    "<div class='footer'>⚠️ Answers are generated solely from the uploaded document and may require human verification.</div>",
    unsafe_allow_html=True,
)
