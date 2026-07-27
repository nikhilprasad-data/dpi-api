from src.config import Config
from pydantic import SecretStr
from langchain_groq import ChatGroq


def get_groq_llm(temperature: float = 0.0):

     """
     Initializes the Groq LLM (Llama 3).
     Used for high-speed, parallel tasks like Deep Research sub-agents.
     Temperature defaults to 0.0 for factual, analytical consistency.
     """
     groq_llm = ChatGroq(
          api_key=SecretStr(Config.GROQ_API_KEY),
          model=Config.GROQ_MODEL,
          temperature=temperature,
          max_tokens= 4000
     )

     return groq_llm
