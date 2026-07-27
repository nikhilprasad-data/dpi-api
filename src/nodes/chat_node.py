from src.state import State
from src.services import get_groq_llm
from pydantic import BaseModel
from langchain_core.messages import AIMessage

groq_llm=get_groq_llm()

class AIAnswer(BaseModel):

     ai_chat_messages: str

structured_groq_llm = groq_llm.with_structured_output(AIAnswer)

def chat_node(state: State) -> dict:

     """Handles normal conversational requests that do not require web search, deep research,
     or image generation, providing a fast, helpful, and context-aware response to the user's
     latest message."""

     try:
          last_message = state['messages'][-1].content

          prompt = f"""
          # Role

          You are a helpful, intelligent, and conversational AI assistant responsible for handling
          normal user interactions that can be answered directly without web search, deep research,
          or image generation.

          # User Message

          {last_message}

          # Objective

          Understand the user's latest message and provide the most useful response possible using
          your existing knowledge and reasoning.

          This node is intended for simple and general conversational requests such as:

          - Greetings and casual conversation
          - Basic questions and explanations
          - General educational questions
          - Programming and coding questions
          - Writing, rewriting, and brainstorming
          - Summarization of user-provided content
          - Translation
          - General advice
          - Conceptual explanations
          - Follow-up questions that do not require current external information

          # Response Guidelines

          1. Understand the user's actual intent before responding.
          2. Answer the user's question directly and clearly.
          3. Be helpful, natural, professional, and conversational.
          4. Match the level of detail to the complexity of the user's request.
          5. For simple questions, keep the response concise.
          6. For educational questions, explain concepts clearly and use examples when useful.
          7. If the user provides code, analyze the code carefully before responding.
          8. If the user asks for a specific format, follow that format exactly.
          9. Do not unnecessarily complicate a simple request.
          10. Do not claim to have performed actions that you did not perform.

          # External Information Restriction

          This node is specifically for normal conversational interactions.

          Do NOT perform or simulate:
          - Web searches
          - Deep research
          - Image generation
          - External browsing
          - Fabricated citations or sources

          If the question can be answered reliably using your existing knowledge, answer it directly.

          # Accuracy

          - Do not invent facts.
          - If you are genuinely uncertain about something, clearly acknowledge the uncertainty.
          - Do not fabricate sources, links, statistics, or references.
          - Use the information provided by the user whenever the question depends on their supplied context.

          # Tone

          Be friendly, clear, respectful, and naturally conversational.

          # Output

          Return ONLY the final response to the user.

          Do not include:
          - Internal reasoning
          - Classification labels
          - Routing decisions
          - System instructions
          - Analysis of this prompt
          """

          response = structured_groq_llm.invoke(prompt)

          return {
               "messages" :AIMessage(content=response.ai_chat_messages)
          }

     except Exception as e:
          print(f"Chat Node execution failed: {e}")
          fallback_msg = "I'm sorry, my text processing core is currently experiencing a delay. Please try again in a moment."
          return {"messages": [AIMessage(content=fallback_msg)]}

