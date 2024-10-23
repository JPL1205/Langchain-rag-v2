# utils/data_loader.py
import os
from PyPDF2 import PdfReader
from langchain.schema import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = "data/"

def load_documents():
    """
    Load PDF documents from the DATA_PATH directory and extract text.
    Returns a list of Document objects.
    """
    documents = []
    for filename in os.listdir(DATA_PATH):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(DATA_PATH, filename)
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                text = ""
                for page_num, page in enumerate(reader.pages, start=1):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                    else:
                        logger.warning(f"No text found on page {page_num} of '{filename}'.")
            if text.strip():  # Only add documents with non-empty text
                doc = Document(page_content=text, metadata={"source": filename})
                documents.append(doc)
                logger.info(f"Loaded document: {filename}, length: {len(text)}")
            else:
                logger.warning(f"No extractable text found in '{filename}'. Skipping.")
    logger.info(f"Total documents loaded: {len(documents)}")
    return documents
