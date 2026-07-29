from src.state import State
from langgraph.graph import END

def should_use_tool(state: State):
     last_message = state['messages'][-1]

     if getattr(last_message, "tool_calls", None):
          return "tools"
     
     return "human_review_node" 

def should_stop_looping(state: State): 
     if state.get('is_approved'):
          return END

     elif state.get('attempt', 0) >= 3:
          return END

     else:
          return "writer_node"