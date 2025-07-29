import os
import httpx
import numpy as np
import chromadb
from dotenv import load_dotenv
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize SentenceTransformer model for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))
collection = chroma_client.get_collection("my_documents")

# Function to embed user query
def get_query_embedding(query):
    return embedding_model.encode(query).tolist()

# Function to retrieve similar documents from ChromaDB
def get_similar_documents(query, top_k=3):
    embedding = get_query_embedding(query)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results["documents"][0]

# Function to call Groq's LLaMA-3 model directly using HTTPX (no openai package)
def call_groq_llm(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Main pipeline function
def rag_pipeline(query):
    documents = get_similar_documents(query)
    context = "\n\n".join(documents)
    
    prompt = f"""Answer the following question using the context below:

Context:
{context}

Question: {query}
Answer:"""

    response = call_groq_llm(prompt)
    return response

# Example usage
if __name__ == "__main__":
    user_query = input("Ask your question: ")
    answer = rag_pipeline(user_query)
    print("\nResponse from Groq LLaMA3:\n", answer)
