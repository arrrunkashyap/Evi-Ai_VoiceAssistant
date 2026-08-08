import socket

from src.ai.gemini_provider import GeminiProvider
from src.ai.ollama_provider import OllamaProvider


class ProviderManager:

    def __init__(self):
        self.gemini = GeminiProvider()
        self.ollama = OllamaProvider()

    def is_online(self) -> bool:
        try:
            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=2
            )
            return True

        except OSError:
            return False

    def ask(self, prompt: str) -> str:

        if self.is_online():

            try:
                return self.gemini.ask(prompt)

            except Exception as e:
                print(f"[Gemini failed] {e}")
                print("[EVI] Switching to Ollama...")

        return self.ollama.ask(prompt)
    
    def stream(self, prompt: str, history=None):

        if self.is_online():

            try:
                yield from self.gemini.stream(
                    prompt,
                    history
                )

                return

            except Exception as e:
                print(f"\n[Gemini failed] {e}")
                print("[EVI] Switching to Ollama...\n")

        yield from self.ollama.stream(
            prompt,
            history
        )