from fastapi import APIRouter, status, HTTPException
from src.graph import build_graph
from src.schemas import ChatRequest, ChatResponse
from langchain_core.messages import HumanMessage




chat = APIRouter()
graph = build_graph()

@chat.post('/chat', response_model= ChatResponse, status_code= status.HTTP_200_OK)
def chat_response(request: ChatRequest):

     user_last_prompt = request.prompt 

     result = graph.invoke({"messages" : [HumanMessage(content=user_last_prompt)]},
                         config={"configurable": {"thread_id": request.thread_id}})

     return {
          "response": result['messages'][-1].content,
          "route_taken": result.get('route_decision'),
          "img_url": result.get('image_url')
     }
