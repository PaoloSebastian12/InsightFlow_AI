import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_model():

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY was not found in the .env file")
    
    return ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.1, api_key=api_key, max_output_tokens=2048)




