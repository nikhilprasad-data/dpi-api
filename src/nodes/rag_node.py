from src.utils import get_rag_retriever, ingestion_pdf_to_database
from src.state import State
from src.services import get_groq_llm
from langchain_core.messages import AIMessage

groq_llm = get_groq_llm()

def rag_node(state: State):

     try:


          last_message = state['messages'][-1].content

          retriever = get_rag_retriever()

          if retriever is None:
               return {"messages": [AIMessage(content="I don't have any documents uploaded to search from yet")]}

          docs = retriever.invoke(last_message)

          context = "\n\n".join([doc.page_content for doc in docs])

          prompt = f"""
               You are a smart assistant. Answer the user's question using ONLY the provided context.
               If the answer is not in the context, say you don't know.
               
               Context:
               {context}
               
               User Question:
               {last_message}
               """

          response = groq_llm.invoke(prompt)

          return {"messages" : [AIMessage(content= response.content)]}

     except Exception as e:
          print(f"failed: {e}")
          return {"messages": [AIMessage(content="Failed to read the documents. Please try again.")]}

     