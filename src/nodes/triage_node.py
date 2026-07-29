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

          2. "deep_research"
          Choose this when the user is asking for comprehensive, multi-source research,
          detailed investigation, comparison, analysis, or a complex topic that requires
          gathering and synthesizing substantial information.

          3. "image_gen"
          Choose this when the user explicitly wants an image to be created, generated,
          drawn, designed, visualized, rendered, or edited.

          4. "writer"
          Choose this when the user explicitly asks you to draft, compose, or format a 
          structured piece of text (e.g., emails, blogs, letters, reports).

          5. "rag_search"
          Choose this when the user's message is asking questions about uploaded files, 
          documents, PDFs, custom attachments, context sheets, or their knowledge base.
          
          Examples:
          - "Based on the uploaded PDF..."
          - "What does the document say about the rules?"
          - "Search through the files I uploaded for..."
          - "Analyze the attached schedule..."

          6. "normal_chat"
          Choose this for requests that can be answered directly using standard knowledge
          without web searching, deep research, image generation, writing scripts, or 
          querying uploaded documents.

          Examples:
          - General conversation and greetings
          - Explanations and conceptual questions
          - Coding questions
          - Translation
          - Casual questions

          # Decision Rules

          - Select exactly ONE route.
          - Determine the user's PRIMARY intent rather than matching isolated keywords.
          - Use "rag_search" when the request depends directly on content within uploaded, 
            attached, or reference documents.
          - Use "deep_research" when the request explicitly requires comprehensive,
            multi-source, or detailed investigation.
          - Use "web_search" for focused online information retrieval or current information.
          - Use "image_gen" only when the user wants an image created, generated, visualized,
            or edited.
          - Use "writer" for drafting text structures.
          - Use "normal_chat" when the request can be handled directly without external
            information, files, or image generation.
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
          writer
          rag_search
          normal_chat
          """
               
          response = structured_gemini_llm.invoke(prompt)

          return {
               "route_decision" : response.route_decision.lower()
          }

     except Exception as e:
          print(f"Triage Node failed: {e}. Falling back to normal_chat.")
          return {"route_decision": "normal_chat"}

     