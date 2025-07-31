from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.services.vector_store_service import create_or_load_vector_db


import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"
LLM_MODEL_NAME = "llama3-8b-8192"

def initialize_llm():
    return ChatGroq(
        model=LLM_MODEL_NAME,
        api_key=GROQ_API_KEY,
        temperature=0.2,
        max_tokens=1000
    )

def setup_qa_chain():
    llm = initialize_llm()
    vector_db = create_or_load_vector_db()
    retriever = vector_db.as_retriever()

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a helpful assistant. Use only the given context to answer the question
truthfully. Don't make up answers or hallucinate. If the answer is not in the context, say \"I don't know\".

Context:
{context}
Question: {question}
Answer:"""
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template}
    )

    return qa_chain

qa_chain = setup_qa_chain()

def get_response(user_query: str) -> str:
    return qa_chain.run(user_query)