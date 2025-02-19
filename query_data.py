# query_data.py
from utils.database_manager import load_chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
Answer the question with your knowledge and with the following information:

{context}

---

Answer the question based on the above context: {question}
"""

def query_database(query_text: str, k=3, relevance_threshold=0.7):
    db = load_chroma()
    results = db.similarity_search_with_relevance_scores(query_text, k=k)
    
    if len(results) == 0 or results[0][1] < relevance_threshold:
        return None, None
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    model = ChatOpenAI()
    response_text = model.predict(prompt)
    
    sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]
    return response_text, sources

# import argparse
# # from dataclasses import dataclass
# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from dotenv import load_dotenv
# import os
# import openai 

# load_dotenv()
# #---- Set OpenAI API key 
# # Change environment variable name from "OPENAI_API_KEY" to the name given in 
# # your .env file.
# openai.api_key = os.environ['OPENAI_API_KEY']

# CHROMA_PATH = "chroma"

# PROMPT_TEMPLATE = """
# Answer the question with your knowledge and with the following information:

# {context}

# ---

# Answer the question based on the above context: {question}
# """


# def main():
#     # Create CLI.
#     parser = argparse.ArgumentParser()
#     parser.add_argument("query_text", type=str, help="The query text.")
#     args = parser.parse_args()
#     query_text = args.query_text

#     # Prepare the DB.
#     embedding_function = OpenAIEmbeddings()
#     db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

#     # Search the DB.
#     results = db.similarity_search_with_relevance_scores(query_text, k=3)
#     if len(results) == 0 or results[0][1] < 0.7:
#         print(f"Unable to find matching results.")
#         return

#     context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
#     prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#     prompt = prompt_template.format(context=context_text, question=query_text)
#     print(prompt)

#     model = ChatOpenAI()
#     response_text = model.predict(prompt)

#     sources = [doc.metadata.get("source", None) for doc, _score in results]
#     formatted_response = f"Response: {response_text}\nSources: {sources}"
#     print(formatted_response)


# if __name__ == "__main__":
#     main()
