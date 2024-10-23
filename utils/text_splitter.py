# utils/text_splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def split_text(documents: list[Document], chunk_size=300, chunk_overlap=100):
    """
    Split documents into smaller chunks for embedding.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks
