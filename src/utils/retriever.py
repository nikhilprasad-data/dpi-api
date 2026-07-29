from src.services import get_embed_llm
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os

DB_FAISS_PATH = os.path.join("src", "data", "faiss_index")

embed_llm = get_embed_llm()

def ingestion_pdf_to_database(file_path: str):
     """
    Call this function whenever a client uploads a new PDF.
    It reads, splits, embeds, and saves the vector store persistently to disk.
    """

     try:
          if not os.path.exists( file_path):
               raise FileNotFoundError(f"No file found at {file_path}")

          loader = PyPDFLoader(file_path= file_path)

          docs = loader.load()

          splitter = RecursiveCharacterTextSplitter(chunk_size= 800, chunk_overlap= 200)

          chunks = splitter.split_documents(documents= docs)

          vector_store = FAISS.from_documents(
               embedding= embed_llm,
               documents= chunks,
          )

          os.makedirs(os.path.dirname(DB_FAISS_PATH), exist_ok= True)

          vector_store.save_local(DB_FAISS_PATH)

          print(f"Successfully ingested {file_path} and saved vector index to {DB_FAISS_PATH}")

          return True

     except Exception as e:
          print(f"Error during document ingestion: {e}")
          return False

     
def get_rag_retriever():
     """
    Call this inside your Graph Node.
    It loads the saved FAISS database instantly without re-processing the PDF.
    """

     try:
          if not os.path.exists(DB_FAISS_PATH):
               print(f"Warning: No vector store found at {DB_FAISS_PATH}. Returning None.")
               return None

          vector_store = FAISS.load_local(
               DB_FAISS_PATH,
               embeddings= embed_llm,
               allow_dangerous_deserialization= True
          )

          retriever = vector_store.as_retriever()


          return vector_store.as_retriever(
               search_type= "mmr",
               search_kwargs= {
                    "k" : 4,
                    "fetch_k" : 20 ,
                    "lambda_mult" : 0.8 
               }
          )

     except Exception as e:
          print(f"Error loading vector store: {e}")
          return None


     