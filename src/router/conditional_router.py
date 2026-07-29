from src.state import State
from src.nodes import web_search_node, deep_research_node, image_node, writer_node, chat_node

def conditional_router_node(state: State):

     last_route_decision = state['route_decision']

     if last_route_decision == "web_search":
          return "web_search_node"
     
     elif last_route_decision == "deep_research":
          return "deep_research_node"
     
     elif last_route_decision == "image_gen":
          return "image_node"
     
     elif last_route_decision == "writer":
          return "writer_node"

     elif last_route_decision == "rag_search":
          return "rag_node"
     
     else:
          return "chat_node"
               

