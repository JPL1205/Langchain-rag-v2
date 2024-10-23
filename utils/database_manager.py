# utils/database_manager.py
import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

CHROMA_PATH = "chroma"

def save_to_chroma(chunks: list[Document], chroma_path=CHROMA_PATH):
    """
    Save document chunks to Chroma vector store.
    """
    # Clear existing database
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)
    
    # Initialize embeddings and Chroma DB
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(
        chunks, embeddings, persist_directory=chroma_path
    )
    db.persist()
    return db

def load_chroma(chroma_path=CHROMA_PATH):
    """
    Load existing Chroma vector store.
    """
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=chroma_path, embedding_function=embeddings)
    return db

