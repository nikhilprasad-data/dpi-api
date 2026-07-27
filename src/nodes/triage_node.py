from src.state import State
from src.services import get_gemini_llm
from pydantic import BaseModel

gemini_llm = get_gemini_llm()

class RouteDecision(BaseModel):

     route_decision: str

structured_gemini_llm = gemini_llm.with_structured_output(RouteDecision)

def triage_node(state: State) -> dict:

     """Analyzes the user's latest message and determines the appropriate workflow route
     based on the user's intent, updating the state with one of the supported routing
     decisions: 'web_search', 'deep_research', 'image_gen', or 'normal_chat'."""

     try: 

          last_message = state['messages'][-1].content

          prompt = f"""
          # Role

          You are an intelligent request-routing AI responsible for determining which workflow
          should handle the user's latest message.

          # User Message

          {last_message}

          # Objective

          Analyze the user's message and select exactly ONE routing decision based on the
          user's primary intent.

          # Available Routes

          1. "web_search"
          Choose this when the user needs current, factual, or externally verifiable
          information that can be answered through a focused web search.

          Examples:
          - Current news or recent events
          - Current prices, product information, or availability
          - A specific fact that needs online verification
          - Current information about a company, person, technology, or topic
          - Finding a specific webpage, documentation, or online resource

          2. "deep_research"
          Choose this when the user is asking for comprehensive, multi-source research,
          detailed investigation, comparison, analysis, or a complex topic that requires
          gathering and synthesizing substantial information.

          Examples:
          - "Do deep research on..."
          - Comprehensive market research
          - Detailed comparison of multiple technologies
          - Academic or technical research
          - Complex questions requiring multiple reliable sources

          3. "image_gen"
          Choose this when the user explicitly wants an image to be created, generated,
          drawn, designed, visualized, rendered, or edited.

          Examples:
          - "Generate an image of..."
          - "Create a logo..."
          - "Draw a diagram..."
          - "Make a poster..."
          - "Edit this image..."

          4. "normal_chat"
          Choose this for requests that can be answered directly without web searching,
          deep research, or image generation.

          Examples:
          - General conversation
          - Explanations
          - Coding questions
          - Writing or rewriting
          - Summarization of provided text
          - Brainstorming
          - Translation
          - Casual questions

          # Decision Rules

          - Select exactly ONE route.
          - Determine the user's PRIMARY intent rather than matching isolated keywords.
          - Use "deep_research" when the request explicitly requires comprehensive,
          multi-source, or detailed investigation.
          - Use "web_search" for focused online information retrieval or current information.
          - Use "image_gen" only when the user wants an image created, generated, visualized,
          or edited.
          - Use "normal_chat" when the request can be handled directly without external
          information or image generation.
          - Do not invent a new route.
          - Do not return explanations.
          - Do not return reasoning.
          - Do not return Markdown.
          - Do not return JSON.

          # Output

          Return ONLY ONE of these exact strings:

          web_search
          deep_research
          image_gen
          normal_chat
          """

          response = structured_gemini_llm.invoke(prompt)

          return {
               "route_decision" : response.route_decision.lower()
          }

     except Exception as e:
          print(f"Triage Node failed: {e}. Falling back to normal_chat.")
          return {"route_decision": "normal_chat"}
     