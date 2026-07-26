from langchain_community.tools import DuckDuckGoSearchRun
from langchain_tavily import TavilySearch
from src.config import Config

ddg_search_engine = DuckDuckGoSearchRun()

tavily_search_engine = TavilySearch(
    tavily_api_key=Config.TAVILY_API_KEY,
    max_results=5
)

def duckduckgo_search(query: str) -> str:
    """
    Performs a completely free web search using DuckDuckGo.
    Ideal for high-frequency parallel searches in Deep Research to save API limits.
    """
    try:
        return ddg_search_engine.run(query)
    except Exception as e:
        return f"DuckDuckGo search failed: {str(e)}"

def tavily_search(query: str) -> list:
    """
    Performs an advanced semantic search using Tavily API.
    Returns clean snippets and direct URLs, perfect for grounding LLM facts.
    """
    try:
        api_key = Config.TAVILY_API_KEY
        if not api_key:
            return [{"url": "N/A", "content": "Error: TAVILY_API_KEY not found in environment variables."}]
            
        results = tavily_search_engine.invoke(
            {"query": query}
        )

        return results
    except Exception as e:
        return [{"url": "N/A", "content": f"Tavily search failed: {str(e)}"}]

    