# PDF Chatbot

A conversational AI app that lets you upload any PDF and ask questions about it. Built with Streamlit, Google Gemini, and ChromaDB.

---

## How It Works

1. You upload a PDF
2. The app extracts and splits the text into chunks
3. Each chunk is converted into embeddings using a local sentence transformer model
4. Embeddings are stored in ChromaDB
5. When you ask a question, the most relevant chunks are retrieved and sent to Gemini to generate an answer

---

## Requirements

- Python 3.9 or above
- A Google Gemini API key (free tier works)

---

## Installation

Clone or download the project, then open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

---

## Setup

Open `app.py` and replace the API key on this line with your own:

```python
GOOGLE_API_KEY = "your-api-key-here"
```

Get a free API key at: https://aistudio.google.com/app/apikey

---

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Usage

1. Upload a PDF using the file uploader
2. Click **Process Document** to generate and store embeddings
3. Type your question in the chat box at the bottom
4. The assistant will answer based on the content of your PDF
5. Click **Clear conversation** to reset the chat

---

## Dependencies

| Package | Purpose |
|---|---|
| streamlit | App interface |
| pdfplumber | Extract text from PDFs |
| chromadb | Store and retrieve embeddings |
| google-generativeai | Gemini API for generating answers |
| sentence-transformers | Local embeddings (free, no API needed) |

---

## Common Errors

**429 Quota exceeded**
Your API key has hit the daily free limit. Either wait a few minutes, create a new Google Cloud project at https://aistudio.google.com, or enable billing at https://console.cloud.google.com/billing.

**404 Model not found**
The Gemini model name is outdated. The app currently uses `gemini-2.5-flash` which is the latest free-tier model.

**No text extracted**
The PDF is likely scanned or image-based. This app only works with text-based PDFs.