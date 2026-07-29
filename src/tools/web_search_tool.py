from langchain_community.tools.tavily_search import TavilySearchResults
from src.config.settings import Config

tavily_search_engine = TavilySearchResults(
    api_key=Config.TAVILY_API_KEY,
    max_results=5
)

def tavily_search(query: str, max_results: int = 5) -> list:
    """
    Performs an advanced semantic search using Tavily API.
    Returns clean snippets and direct URLs, perfect for grounding LLM facts.
    """
    try:
        api_key = Config.TAVILY_API_KEY
        if not api_key:
            return [{"url": "N/A", "content": "Error: TAVILY_API_KEY not found in environment variables."}]
            
        results = tavily_search_engine.invoke({"query": query})
        
        return results[:max_results]
        
    except Exception as e:
        return [{"url": "N/A", "content": f"Tavily search failed: {str(e)}"}]