from pydantic import BaseModel
from typing import Optional, Literal

class ChatRequest(BaseModel):

     prompt: str

     route_to_take: Literal[
          "web_search",
          "deep_research",
          "image_gen",
          "writer",
          "rag_search",
          "normal_chat"
     ] = "normal_chat"

     thread_id: str

class ChatResponse(BaseModel):

     response: str

     route_taken: Optional[str] = None

     img_url: Optional[str] = None

     is_awaiting_review: bool = False

class ResumeRequest(BaseModel):

     thread_id: str

     feedback: str
     