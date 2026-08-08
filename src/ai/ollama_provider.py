import json
import requests

from src.ai.base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model = "llama3.2"

    def ask(self, prompt: str) -> str:

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    def stream(self, prompt: str, history=None):

        messages = []

        if history:
            messages.extend(history)

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": messages,
                "stream": True
            },
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            data = json.loads(line.decode("utf-8"))

            if "message" in data:

                content = data["message"].get(
                    "content",
                    ""
                )

                if content:
                    yield content

            if data.get("done", False):
                break