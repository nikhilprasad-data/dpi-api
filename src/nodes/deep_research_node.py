from src.state import State
from src.tools import tavily_search, scrape_website
from src.services import get_groq_llm
from langchain_core.messages import AIMessage


groq_llm=get_groq_llm()

def deep_research_node(state: State) -> dict:
    """
    Performs Deep Research by searching the web, extracting the top URL, 
    scraping the full article, and summarizing the facts for the final answer.
    """
    try:
        last_message = state['messages'][-1].content
        print(f"Starting Deep Research for: {last_message}")

        search_results = tavily_search(last_message)
        
        if not search_results or search_results[0].get("url") == "N/A":
            return {"messages": [AIMessage(content="Deep research failed: No relevant data found on the web.")]}

        top_url = search_results[0]['url']
        print(f"Scraping top source: {top_url}")

        scraped_text = scrape_website(top_url)

        analysis_prompt = f"""
        You are a Deep Research Analyst. 
        User Query: {last_message}
        
        Here is the raw scraped data from the web ({top_url}):
        {scraped_text}
        
        Extract the most important facts, numbers, and details that directly answer the user's query.
        Write a highly detailed, structured summary.
        """
        
        research_summary = groq_llm.invoke(analysis_prompt).content
        
        final_output = f"Deep Research Complete (Source: {top_url}):\n\n{research_summary}"

        return {
            "research_data": [final_output],
            "messages": [AIMessage(content=final_output)]
        }

    except Exception as e:
        print(f"Search Node execution failed: {e}")
        return {"messages": [AIMessage(content=f"Research module encountered an error: {str(e)}")]}

