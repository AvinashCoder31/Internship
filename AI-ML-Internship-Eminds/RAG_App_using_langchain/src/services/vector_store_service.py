from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

CHROMA_DB_DIR = "database/chroma_db"
PDF_DIR = "data/"
PDF_PATTERN = "*.pdf"

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"

def create_or_load_vector_db():
    if os.path.exists(CHROMA_DB_DIR) and os.path.exists(os.path.join(CHROMA_DB_DIR, "chroma.sqlite3")):
        print("📦 Loading existing Chroma DB...")
        return Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL_NAME))

    print("📄 Creating new Chroma DB from PDFs...")
    loader = DirectoryLoader(PDF_DIR, glob=PDF_PATTERN, loader_cls=PyPDFLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(documents)

    embeddings = HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vector_store = Chroma.from_documents(split_docs, embeddings, persist_directory=CHROMA_DB_DIR)
    vector_store.persist()

    return vector_store