import os
import openai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure Groq API
openai.api_key = GROQ_API_KEY
openai.api_base = "https://api.groq.com/openai/v1"

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="my_documents")

# Load SentenceTransformer ONLY for query encoding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Ask the user for a question
user_query = input("Ask your question: ")

# Embed the query
query_embedding = model.encode(user_query).tolist()

# Query the most relevant chunks from ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
retrieved_chunks = results['documents'][0]

# Build the final prompt
context = "\n\n".join(retrieved_chunks)
final_prompt = f"""Answer the question based on the context below:

Context:
{context}

Question: {user_query}

Answer:"""

# Use GROQ LLaMA 3 for inference
response = openai.ChatCompletion.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": final_prompt}],
    temperature=0.2
)

# Print the generated answer
print("\n🧠 LLaMA 3's Answer:")
print(response['choices'][0]['message']['content'])