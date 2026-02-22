import streamlit as st
import pdfplumber
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import time
import re

GOOGLE_API_KEY = "AIzaSyDVmtJqGCUZD3c03mYqzc84bJmcdUZe6JY"

if not GOOGLE_API_KEY.strip():
    st.error("GOOGLE_API_KEY is empty. Please paste your Gemini API key.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

GEN_MODEL = "gemini-2.5-flash"

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def get_collection():
    client = PersistentClient(path="./chroma_db")
    return client.get_or_create_collection("pdf_chunks")

embedding_model = load_embedding_model()
collection = get_collection()


def extract_text_from_pdf(pdf_file):
    all_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() or ""
    return all_text


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += chunk_size - overlap
    return chunks


def embed_and_store(chunks):
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    embeddings = embedding_model.encode(chunks, show_progress_bar=False).tolist()
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)


def retrieve_context(query, top_k=3):
    total = collection.count()
    if total == 0:
        return ""
    query_emb = embedding_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_emb, n_results=min(top_k, total))
    if results and "documents" in results:
        return "\n\n".join(results["documents"][0])
    return ""


def generate_answer(context, query, max_retries=3):
    prompt = f"""You are a helpful AI assistant. Use the context below to answer the question.
If the answer is not found in the context, say "I couldn't find relevant information in the document."

Context:
{context}

Question:
{query}

Answer:"""

    model = genai.GenerativeModel(GEN_MODEL)

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            error_str = str(e)

            if "429" in error_str:
                wait_time = 65
                match = re.search(r"retry in (\d+)", error_str, re.IGNORECASE)
                if match:
                    wait_time = int(match.group(1)) + 5
                if attempt < max_retries - 1:
                    st.warning(f"Rate limit hit. Waiting {wait_time}s then retrying... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    return (
                        "Quota exceeded after all retries.\n\n"
                        "Fix options:\n"
                        "1. Wait a few minutes and try again\n"
                        "2. Go to https://aistudio.google.com, create a New Project, and generate a fresh API key\n"
                        "3. Enable billing at https://console.cloud.google.com/billing"
                    )
            elif "404" in error_str:
                return (
                    f"Model {GEN_MODEL} not found on your API key.\n\n"
                    "Check your key at https://aistudio.google.com/app/apikey "
                    "or see available models at https://ai.google.dev/gemini-api/docs/models"
                )
            else:
                return f"Gemini API Error: {error_str}"

    return "Failed after all retries."


st.set_page_config(page_title="PDF Chatbot", layout="centered")

st.title("PDF Chatbot")
st.caption("Upload a PDF and ask questions about it.")

st.divider()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading document..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

    if not pdf_text.strip():
        st.error("Could not extract text. The PDF may be scanned or image-based.")
        st.stop()

    chunks = chunk_text(pdf_text)

    col1, col2, col3 = st.columns(3)
    col1.metric("File", uploaded_file.name[:20])
    col2.metric("Characters", f"{len(pdf_text):,}")
    col3.metric("Chunks", len(chunks))

    if st.button("Process Document", use_container_width=True):
        with st.spinner("Generating embeddings..."):
            embed_and_store(chunks)
        st.success(f"Done. {len(chunks)} chunks stored and ready.")

    st.divider()

    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.markdown(chat["answer"])
        st.divider()

    query = st.chat_input("Ask a question about your document...")

    if query:
        if collection.count() == 0:
            st.warning("Please process the document first.")
        else:
            with st.chat_message("user"):
                st.write(query)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context = retrieve_context(query)
                    if context:
                        answer = generate_answer(context, query)
                        st.markdown(answer)
                        st.session_state.chat_history.append({"question": query, "answer": answer})
                    else:
                        st.warning("No relevant context found. Try processing the document first.")

    if st.session_state.chat_history:
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()