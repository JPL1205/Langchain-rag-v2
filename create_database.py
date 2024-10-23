# create_database.py
from utils.data_loader import load_documents
from utils.text_splitter import split_text
from utils.database_manager import save_to_chroma
import os
import shutil
import openai
import nltk
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from PyPDF2 import PdfReader
import logging

nltk.download('punkt')

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()

#---- Set OpenAI API key 
openai.api_key = os.environ['OPENAI_API_KEY']

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_data_store():
    """
    Generate the Chroma data store by loading documents, splitting text,
    and saving to Chroma.
    """
    documents = load_documents()
    if not documents:
        logger.warning("No PDF documents found in the 'data/' directory.")
        return

    chunks = split_text(documents)
    if not chunks:
        logger.warning("No text chunks were created from the documents.")
        return

    try:
        save_to_chroma(chunks)
        logger.info(f"Saved {len(chunks)} chunks to the Chroma database.")
    except Exception as e:
        logger.error(f"Failed to save to Chroma: {e}")
        raise

if __name__ == "__main__":
    generate_data_store()



# import os
# import shutil
# import openai
# import nltk
# from dotenv import load_dotenv
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema import Document
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma
# from PyPDF2 import PdfReader

# nltk.download('punkt')

# # Load environment variables. Assumes that project contains .env file with API keys
# load_dotenv()

# #---- Set OpenAI API key 
# openai.api_key = os.environ['OPENAI_API_KEY']

# CHROMA_PATH = "chroma"
# DATA_PATH = "data/"

# def main():
#     generate_data_store()

# def generate_data_store():
#     documents = load_documents()
#     chunks = split_text(documents)
#     save_to_chroma(chunks)

# def load_documents():
#     """
#     Use PyPDF2 to load PDFs from the directory and convert them into Document objects.
#     """
#     documents = []
#     for filename in os.listdir(DATA_PATH):
#         if filename.endswith(".pdf"):
#             file_path = os.path.join(DATA_PATH, filename)
#             with open(file_path, "rb") as file:
#                 reader = PdfReader(file)
#                 text = ""
#                 for page_num in range(len(reader.pages)):
#                     page = reader.pages[page_num]
#                     text += page.extract_text()

#                 # Create a Langchain Document object
#                 doc = Document(page_content=text, metadata={"source": filename})
#                 documents.append(doc)

#     return documents

# def split_text(documents: list[Document]):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=300,
#         chunk_overlap=100,
#         length_function=len,
#         add_start_index=True,
#     )
#     chunks = text_splitter.split_documents(documents)
#     print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

#     document = chunks[10]  # Example access to the 10th document chunk
#     print(document.page_content)
#     print(document.metadata)

#     return chunks

# def save_to_chroma(chunks: list[Document]):
#     # Clear out the database first.
#     if os.path.exists(CHROMA_PATH):
#         shutil.rmtree(CHROMA_PATH)

#     # Create a new DB from the documents.
#     db = Chroma.from_documents(
#         chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
#     )
#     db.persist()
#     print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

# if __name__ == "__main__":
#     main()
