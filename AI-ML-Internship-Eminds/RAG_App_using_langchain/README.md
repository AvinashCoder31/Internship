# 📚 RAG with LangChain, Groq, HuggingFace, ChromaDB & Flask

This project is a lightweight Retrieval-Augmented Generation (RAG) pipeline that uses:

* 📄 **PDF documents** as input source
* 🧠 **HuggingFace BGE embeddings** for vectorization
* 🧠 **ChromaDB** for storing and retrieving vectors
* 🤖 **Groq LLaMA 3 (via LangChain)** for answering questions
* 🌐 **Flask** for providing an API layer

---

## 📁 Project Structure

```
RAG_App_using_langchain/
├── main.py                   # Flask app entry point
├── requirements.txt          # Dependencies
├── .env                      # Contains GROQ_API_KEY
├── database/                 # For DB files (if needed)
└── src/
    ├── routes/               # Flask routes (if needed)
    └── services/
        └── vector_store_service.py   # Vector store logic
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/AvinashCoder31/Intership/AI-ML-Internship-Eminds/RAG_App_using_langchain.git
cd RAG_App_using_langchain
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variable

Create a `.env` file:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Data Folder

Make sure your PDF is in a folder called `data/` at root level. Example:

```
data/
└── CanWeBeStrangersAgain.pdf
```

---

## ▶️ How to Run

### Run CLI mode:

```bash
python main.py
```

Then ask any question from your PDF.

### Run Flask (API) mode:

You can modify `main.py` to expose a Flask route using the `get_response` method.

---

## 🧠 How It Works

1. Loads PDF using `PyPDFLoader`
2. Splits documents using `RecursiveCharacterTextSplitter`
3. Embeds using `BAAI/bge-base-en-v1.5`
4. Stores/retrieves using ChromaDB
5. Runs RAG with Groq’s LLaMA 3 via LangChain

---

## ✅ Dependencies

See `requirements.txt` or install directly:

```txt
flask
python-dotenv
langchain
langchain-community
langchain-groq
chromadb
```

---

## 🛠️ TODOs

* [ ] Add Flask routes in `src/routes/`
* [ ] Deploy with Gunicorn
* [ ] Add PDF upload support
* [ ] Add frontend (optional)

---

## 📜 License

MIT License

---

## 🙋‍♂️ Author

Avinash R — Built with 💙 and Groq 🧠
