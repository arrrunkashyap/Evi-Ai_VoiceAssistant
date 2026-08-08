print("Inside GeminiProvider")
from google import genai
from google.genai.errors import ClientError
from src.prompts.system_prompt import SYSTEM_PROMPT
from src.ai.base_provider import BaseProvider
from src import config


class GeminiProvider(BaseProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

    def ask(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
            )

            return response.text

        except ClientError as e:
            if e.code == 429:
                return "I'm receiving too many requests right now."

            if e.code == 404:
                return f"Model '{config.GEMINI_MODEL}' not found."

            return f"Gemini API Error: {e}"

        except Exception as e:
            return f"Unexpected error: {e}"

    def stream(self, prompt: str, history=None):
        
        contents = [
            {
                "role": "user",
                "parts": [{"text": SYSTEM_PROMPT}]
            }
        ]

        if history:
            for msg in history:
                contents.append({
                    "role": msg["role"],
                    "parts": [{"text": msg["text"]}]
                })

        stream = self.client.models.generate_content_stream(
            model=config.GEMINI_MODEL,
            contents=contents,
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text