
import requests
import faiss
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# Load .env variables (if you created one)
load_dotenv()

# Get your Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Print to confirm
print("✅ Groq key loaded:", "✔️" if GROQ_API_KEY.startswith("gsk_") else "❌ (Replace your key manually)")

# Load local FAISS index and original text chunks
index = faiss.read_index("./database/metasploit_index.faiss")
chunks = np.load("./database/metasploit_chunks.npy", allow_pickle=True)

# Load embedding model (same as used for chunk embeddings)
embedder = SentenceTransformer("all-MiniLM-L6-v2")



def retrieve_chunks(query: str, top_k=20):
    # Step 1: Embed the query using the same model
    query_embedding = embedder.encode([query], convert_to_numpy=True)

    # Step 2: Search in the FAISS index
    distances, indices = index.search(query_embedding, top_k)

    # Step 3: Return the top-k matched text chunks
    return [chunks[i] for i in indices[0]]



def generate_answer(query: str, context_chunks):
    context = "\n".join([f"- {chunk}" for chunk in context_chunks])
    prompt = f"""You are a helpful assistant. Use only the given context to answer the question truthfully. Dont make up answers or hallucinate. If the answer is not in the context, say "I don't know" and make the normal chat like conversation.

Context:
{context}

Question: {query}
Answer:"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 8192
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    result = response.json()

    if "choices" in result:
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"Groq error: {result}")