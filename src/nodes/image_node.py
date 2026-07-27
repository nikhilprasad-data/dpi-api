from src.state.master_state import State
from src.services import get_groq_llm
from src.tools import generate_image
from langchain_core.messages import AIMessage

groq_llm = get_groq_llm(temperature=0.7)

def image_node(state: State) -> dict:
    """
    Enhances the user's image request using Groq, passes the optimized prompt 
    to the Hugging Face image tool, and saves the Base64 result to the state.
    """
    try:
        last_message = state['messages'][-1].content
        print(f"Starting Image Generation for: {last_message}")

        prompt_enhancer = f"""
        # Role
        You are an expert prompt engineer for AI image generators like FLUX or Midjourney.
        
        # User Request
        {last_message}
        
        # Task
        Take the user's request and write a highly detailed, descriptive prompt for an image generation model.
        Include details about lighting, style, camera angle, and atmosphere.
        If the user specified a style (e.g., "cartoon", "sketch"), keep it. Otherwise, default to high-quality, photorealistic.
        
        # Output
        Return ONLY the enhanced prompt string. No explanation, no quotes.
        """
        
        optimized_prompt = groq_llm.invoke(prompt_enhancer).content.strip()
        print(f"Optimized Prompt: {optimized_prompt}")

        base64_image = generate_image(optimized_prompt)
        
        if base64_image.startswith("Error") or base64_image.startswith("Image generation failed"):
            return {
                "messages": [AIMessage(content=f"Sorry, I couldn't generate the image. {base64_image}")]
            }

        return {
            "image_url": base64_image,
            "messages": [AIMessage(content="Here is your generated image!")]
        }

    except Exception as e:
        print(f"Image Node failed: {e}")
        return {"messages": [AIMessage(content=f"An error occurred during image generation: {str(e)}")]}
    