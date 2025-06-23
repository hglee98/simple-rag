import requests
import os


class LLMClient:
    def __init__(self):
        host = os.getenv("LLM_API_HOST", "localhost")
        port = os.getenv("LLM_API_PORT", "8080")
        self.url = f"http://{host}:{port}"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.url}/generate",
            json={"query": prompt},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json().get("response", "")
