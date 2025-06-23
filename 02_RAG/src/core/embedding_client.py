import requests
from typing import List
from langchain_core.embeddings import Embeddings
import os


class EmbeddingModel(Embeddings):
    def __init__(self):
        host = os.getenv("LLM_API_HOST", "localhost")
        port = os.getenv("LLM_API_PORT", "8080")
        self.url = f"http://{host}:{port}"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, query: str) -> List[float]:
        response = requests.post(
            f"{self.url}/embed",
            params={"text": query},
            headers={"Content-Type": "application/json"},
        )
        return response.json()
