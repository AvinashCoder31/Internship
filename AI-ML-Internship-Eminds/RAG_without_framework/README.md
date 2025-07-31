# 🧠 Metasploit RAG-Powered Question Answering API

This is a simple **RAG (Retrieval-Augmented Generation)** project built with **FAISS**, **SentenceTransformers**, and **Groq's LLaMA 3 LLM**. The system retrieves relevant content from a Metasploit book and uses it to generate answers with minimal hallucination.

---

## 📁 Project Structure

```
RAG_without_framework/
├── main.py                   # Flask app entry point
|── notebooks
|   └── RAG_Initialize.ipynb  # Initialization (text splitting,chunking)         
├── requirements.txt          # Dependencies
├── .env                      # Groq API key 
├── database/
│   ├── metasploit_index.faiss
│   └── metasploit_chunks.npy
└── src/
    ├── routes/
    │   └── query_routes.py    # Handles /ask endpoint
    └── services/
        └── service.py      # Chunk retriever and Groq answer generator
```

---

## 🚀 How It Works

1. User sends a query to the `/ask` endpoint.
2. The system:

   * Embeds the query using `all-MiniLM-L6-v2`
   * Searches for top matching chunks using FAISS
   * Sends the chunks and query to Groq's `llama3-8b-8192`
3. Returns the model's answer based **strictly on the retrieved context**.

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/AvinashCoder31/Intership/AI-ML-Internship-Eminds/RAG_App_without_framework.git
cd RAG_App_using_langchain
```

### 2. Setup virtual environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare `.env`

Create a `.env` file:

```
GROQ_API_KEY=gsk_xxxxyourkeyherexxxx
```

### 5. Ensure the database exists

Place the following files in `./database` folder:

* `metasploit_index.faiss`
* `metasploit_chunks.npy`

These should be created from the Metasploit book using chunking + embedding logic (not included in this repo).

---

## 🧪 Usage

### Start the Flask server

```bash
python main.py
```

### Make a POST request

Using `curl`:

```bash
curl -X POST http://127.0.0.1:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me how to exploit a vulnerability using metasploit"}'
```

Using Python:

```python
import requests
response = requests.post("http://127.0.0.1:5000/ask", json={"query": "your question here"})
print(response.json())
```

---

## 📌 Notes

* You **must** use the same embedding model for query and index.
* Groq API key must be valid and start with `gsk_`
* This system **will not hallucinate**; if the answer is not in the retrieved context, it will say "I don't know".

---

## 🔐 Security

* Never expose `.env` or your `GROQ_API_KEY`
* You can enforce rate-limiting or token-based auth using Flask middleware if deploying publicly

---

## 📚 Credits

* SentenceTransformers - Embedding model
* FAISS - Vector DB
* Groq LLaMA 3 - LLM used for final generation
* Metasploit book - Source of knowledge

---

## 📬 Contact

Feel free to reach out if you'd like to expand this project with PDF uploading, chunking pipeline, frontend UI, or multi-LLM support.

---

## ✅ TODO (Optional Enhancements)

* [ ] Add endpoint to upload PDF + auto index
* [ ] Add frontend UI using React/Flask
* [ ] Use ChromaDB or Qdrant instead of FAISS
* [ ] Add LLM fallback if Groq fails
* [ ] Unit tests for service layer
