from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):

     prompt: str

     route_to_take: Optional[str] = None

class ChatResponse(BaseModel):

     response: str

     route_taken: Optional[str] = None

     img_url: Optional[str] = None
