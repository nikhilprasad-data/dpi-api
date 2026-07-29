from src.state import State
from src.services import get_groq_llm
from langchain_core.messages import AIMessage


groq_llm = get_groq_llm()

def writer_node(state: State) -> dict:

     """Generates a clear, accurate, and user-friendly final response by interpreting the
     user's latest message and producing a helpful answer that is natural, conversational,
     and tailored to the user's request."""

     try: 
          last_message = state['messages'][-1].content

          prompt = f"""
     # Role

     You are an expert AI Writing Assistant responsible for generating high-quality, accurate,
     and natural responses to user requests.

     # User Message

     {last_message}

     # Objective

     Carefully understand the user's request and generate the best possible response.

     # Responsibilities

     - Fully understand the user's intent before responding.
     - Answer the user's request directly and accurately.
     - Provide complete and helpful information.
     - Maintain a natural, conversational tone.
     - Adapt the writing style to match the user's request.
     - Produce well-structured and easy-to-read responses.

     # Writing Guidelines

     1. Read the user's message carefully.
     2. Identify the primary intent.
     3. Respond only to what the user is asking.
     4. Keep the response clear, concise, and well organized.
     5. Use simple language unless the user requests technical detail.
     6. If the user requests code, provide correct and executable code.
     7. If the user requests an explanation, explain step-by-step when appropriate.
     8. If the user requests writing (email, letter, blog, story, documentation, etc.), write in the requested format.
     9. Preserve any facts, names, numbers, or context provided by the user.
     10. Do not invent facts or make unsupported claims.
     11. If information is insufficient, politely indicate what additional information is needed instead of guessing.

     # Quality Requirements

     - Accurate
     - Helpful
     - Professional
     - Grammatically correct
     - Logically organized
     - Context-aware
     - Free from unnecessary repetition

     # Tone

     Maintain a friendly, professional, and conversational tone unless the user explicitly requests a different style.

     # Output Requirements

     Return only the final response intended for the user.

     Do not include:
     - Internal reasoning
     - Explanations of your thought process
     - Analysis
     - System messages
     - Markdown code fences unless the user requests code
     - JSON unless the user explicitly requests JSON
     """

          attempt = state.get("attempt", 0) + 1
          prev_review_feedback = state.get("review_feedback", "")

          if attempt == 1:
               user_message = f"Please fulfill this request: {last_message}"
          else:
               user_message = (
                    f"Your previous draft was rejected.\n"
                    f"Here is the reviewer's feedback: \n{prev_review_feedback}\n\n"
                    f"Write a new, improved draft that fixes every issue mentioned. "
                    f"Do NOT repeat the same mistakes."
               )

          messages = [('system', prompt), ('human', user_message)]

          response = groq_llm.invoke(messages)

          return {
               "attempt": attempt,
               "messages": [AIMessage(content=response.content)],
               "draft": response.content
          }




     except Exception as e:
          print(f"Writer Node execution failed: {e}")
          fallback_msg = "I'm sorry, I encountered an error while trying to write the response. Please try again."
          return {
               "messages": [AIMessage(content=fallback_msg)]
          }

     

