from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

def get_embed_llm():

     """
     Initializes the HuggFaceEmbedding LLM.
     Used for the creating the embeddings.
     """

     emed_model = HuggingFaceEmbeddings(
          model_name="sentence-transformers/all-MiniLM-L6-v2"
     )

     return emed_model

