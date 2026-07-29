from src.state import State
from langgraph.types import interrupt

def human_review_node(state: State):

     human_response = interrupt({
          "draft" : state['draft'],
          "attempt" : state['attempt'],
          "instruction" : "Type 'approved' to accept or type your feedback"
     })

     response = human_response.strip()

     if response.lower() in ['accept', "accepted", "ok", "done", "approve", "approved", "yes"]:
          return {
               "is_approved" : True,
               "review_feedback" : "Approved by human"
          }

     return {
          "is_approved" : False,
          "review_feedback" : response
     }

