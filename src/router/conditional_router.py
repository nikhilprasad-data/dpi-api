from src.state import State

def conditional_router_node(state: State):
     # 1. ALWAYS respect the frontend's explicit choice first!
     frontend_choice = state.get('route_to_take')
     
     if frontend_choice == "writer":
          return "writer_node"
     elif frontend_choice == "rag_search":
          return "rag_node"
     elif frontend_choice == "web_search":
          return "web_search_node"
     elif frontend_choice == "deep_research":
          return "deep_research_node"
     elif frontend_choice == "image_gen":
          return "image_node"
          

     last_route_decision = state.get('route_decision')

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