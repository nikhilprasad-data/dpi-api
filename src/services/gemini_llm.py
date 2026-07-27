from src.config import Config
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_llm(temperature: float = 0.0):

     """
     Initializes the Google Gemini LLM.
     Used for the Master Router and Supervisor tasks due to its massive context window.
     """

     gemini_llm = ChatGoogleGenerativeAI(
        api_key=SecretStr(Config.GOOGLE_API_KEY),
        model=Config.GOOGLE_MODEL,
        temperature=temperature,
        max_tokens=8000
     )

     return gemini_llm
