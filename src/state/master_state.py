from langgraph.graph import add_messages
from typing import TypedDict, Annotated
import operator


class State(TypedDict):

     messages: Annotated[list, add_messages]

     route_decision: str

     draft: str

     review_feedback: str

     attempt: int

     research_data: Annotated[list,operator.add]

     image_url: str

