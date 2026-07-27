import requests
import base64
from src.config.settings import Config

def generate_image(prompt: str) -> str:
    """
    Generates an image based on a text prompt using HuggingFace's free API.
    Returns the image as a Base64 encoded string so the frontend can display it directly.
    """
    try:
        api_key = Config.HUGGINGFACE_API_KEY
        if not api_key:
            return "Error: HUGGINGFACE_API_KEY is missing in settings."

        API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": prompt}

        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        image_bytes = response.content
        base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
        
        return f"data:image/jpeg;base64,{base64_encoded}"

    except requests.exceptions.Timeout:
        return "Image generation failed: Request timed out."
    except Exception as e:
        return f"Image generation failed: {str(e)}"