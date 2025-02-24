# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()

openapikey = os.getenv('OPENAI_API_KEY')

def create_vector_store(chunks):
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    embeddings=OpenAIEmbeddings(api_key=openapikey)
    return FAISS.from_documents(chunks, embeddings)
    # return FAISS.from_texts(chunks, embeddings)

def retrieve_answer(query, vector_store):
    return vector_store.similarity_search(query, k=1)[0].page_content
