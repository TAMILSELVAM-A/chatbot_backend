import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def load_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    return ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="deepseek-r1-distill-llama-70b")
