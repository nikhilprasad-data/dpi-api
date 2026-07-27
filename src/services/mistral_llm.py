from src.config import Config
from pydantic import SecretStr
from langchain_mistralai import ChatMistralAI

def get_mistral_llm(temperature: float = 0.0):

     """
     Initializes the Mistral LLM.
     Available as a backup reasoning engine.
     """
     
     mistral_llm = ChatMistralAI(
          api_key=SecretStr(Config.MISTRAL_API_KEY),
          model_name=Config.MISTRAL_MODEL,
          temperature=temperature,
          max_tokens= 4000
     )

     return mistral_llm
