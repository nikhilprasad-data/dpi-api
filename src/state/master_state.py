from langgraph.graph import add_messages
from typing import TypedDict, Annotated
import operator


class State(TypedDict):

     messages: Annotated[list, add_messages]

     route_decision: str

     review_feedback: str

     attempt: int

     research_data: Annotated[list,operator.add]

     image_url: str

     draft: str

     review_feedback: str

     is_approved: bool

     attempt: int

