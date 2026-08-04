from src.nodes import triage_node, web_search_node, deep_research_node, writer_node, chat_node, image_node, rag_node, human_review_node
from src.utils import should_stop_looping
from src.router import conditional_router_node
from langgraph.graph import StateGraph, START, END
from src.state import State
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()

def build_graph():

     build = StateGraph(State)

     build.add_node("triage_node", triage_node)
     build.add_node("writer_node", writer_node)
     build.add_node("chat_node", chat_node)
     build.add_node("deep_research_node", deep_research_node)
     build.add_node("image_node", image_node)
     build.add_node("web_search_node", web_search_node)
     build.add_node("rag_node", rag_node)
     build.add_node("human_review_node", human_review_node)

     build.add_edge(START, "triage_node")

     build.add_conditional_edges("triage_node", conditional_router_node)

     build.add_edge("chat_node", END)
     build.add_edge("deep_research_node", END)
     build.add_edge("web_search_node", END)
     build.add_edge("image_node", END)
     build.add_edge("rag_node", END)
     build.add_edge("writer_node", "human_review_node")
     build.add_conditional_edges("human_review_node", should_stop_looping)

     work_flow =build.compile(checkpointer= memory)

     return work_flow
