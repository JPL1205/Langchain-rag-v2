# test_chroma.py
from utils.database_manager import save_to_chroma
from utils.data_loader import load_documents
from utils.text_splitter import split_text
import logging
from dotenv import load_dotenv
load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_chroma_initialization():
    documents = load_documents()
    if not documents:
        logger.warning("No PDF documents found in the 'data/' directory. Please add PDFs before testing.")
        return
    
    chunks = split_text(documents)
    if not chunks:
        logger.warning("No text chunks were created from the documents.")
        return
    
    try:
        save_to_chroma(chunks)
        logger.info("Chroma database initialized successfully with documents.")
    except Exception as e:
        logger.error(f"Failed to initialize Chroma database: {e}")

if __name__ == "__main__":
    test_chroma_initialization()
