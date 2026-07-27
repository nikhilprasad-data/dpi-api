import os
from dotenv import load_dotenv
load_dotenv()

class Config():

     GROQ_API_KEY=os.environ.get("GROQ_API_KEY","")

     GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY","")

     MISTRAL_API_KEY=os.environ.get("MISTRAL_API_KEY","")

     TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY","")

     GROQ_MODEL=os.environ.get("GROQ_MODEL","")

     GOOGLE_MODEL=os.environ.get("GOOGLE_MODEL","")

     MISTRAL_MODEL=os.environ.get("MISTRAL_MODEL","")

     HUGGINGFACE_API_KEY=os.environ.get("HUGGINGFACE_API_KEY","")