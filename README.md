# 📄 PDF Chatbot (RAG-Based)

A conversational AI web app that allows users to upload PDF documents and ask questions about their content.

Built using **Streamlit**, **Google Gemini**, **Sentence Transformers**, and **ChromaDB**.

---

## 📸 Screenshot

<img width="1911" height="694" alt="image" src="https://github.com/user-attachments/assets/1261f07a-2ff0-4038-ae38-a2c56a513cda" />
<img width="1903" height="1069" alt="image" src="https://github.com/user-attachments/assets/730fb0e5-073c-4642-bb3e-29e25d4016b1" />



---

## ✨ Features

✔ Upload any text-based PDF
✔ Ask questions in natural language
✔ Semantic search using embeddings
✔ Fast AI responses using Google Gemini
✔ Local vector storage with ChromaDB
✔ Clean and simple Streamlit interface

---

## 🧠 How It Works

1. Upload a PDF
2. Text is extracted and split into chunks
3. Chucks are converted into embeddings
4. Stored in ChromaDB vector database
5. Relevant chunks retrieved for your query
6. Gemini generates a contextual answer

---

## 🛠 Tech Stack

* **Frontend:** Streamlit
* **LLM:** Google Gemini API
* **Embeddings:** Sentence Transformers
* **Vector Database:** ChromaDB
* **PDF Processing:** pdfplumber

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Tanishq22A/RAG-Pdf-Reader.git
cd pdf-chatbot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup API Key

Open **app.py** and replace:

```python
GOOGLE_API_KEY = "your-api-key-here"
```

Get your API key:

https://aistudio.google.com/app/apikey

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 📌 Usage

1️⃣ Upload your PDF
2️⃣ Click **Process Document**
3️⃣ Ask questions in the chat box
4️⃣ Get answers instantly
5️⃣ Clear chat anytime

---

## 📁 Project Structure

```
├── app.py
├── requirements.txt
├── chroma_db/
├── images/
│   └── demo.png
└── README.md
```

---

## 🔮 Future Improvements

* Multi-PDF support
* Chat history export
* OCR for scanned PDFs
* Cloud deployment

---




## 🤝 Contributing

Pull requests are welcome!
Feel free to fork and improve.

---

⭐ If you like this project, consider giving it a star!
