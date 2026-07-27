from src.state.master_state import State
from src.services import get_groq_llm
from src.tools import tavily_search
from langchain_core.messages import AIMessage

groq_llm = get_groq_llm(temperature=0.0)

def web_search_node(state: State) -> dict:
    """
    Performs a blazingly fast standard web search.
    It relies strictly on search result snippets and does NOT scrape full webpages.
    """
    try:
        last_message = state['messages'][-1].content
        print(f"Starting Fast Web Search for: {last_message}")

        search_results = tavily_search(last_message)
        
        snippets_text = ""
        for result in search_results:
            if result.get("url") != "N/A": 
                snippets_text += f"Source: {result['url']}\nSnippet: {result['content']}\n\n"
                
        if not snippets_text.strip():
            return {"messages": [AIMessage(content="Web search failed to find relevant information.")]}

        prompt = f"""
        # Role
        You are a fast, factual AI assistant.
        
        # User Query
        {last_message}
        
        # Web Search Snippets
        {snippets_text}
        
        # Task
        Answer the user's query directly and concisely using ONLY the provided snippets.
        Do not invent information. 
        Briefly cite your sources by mentioning the URLs at the bottom of your answer.
        """
        
        fast_answer = groq_llm.invoke(prompt).content

        return {"messages": [AIMessage(content=fast_answer)]}

    except Exception as e:
        print(f"Web Search Node failed: {e}")
        return {"messages": [AIMessage(content=f"Web search encountered an error: {str(e)}")]}

    