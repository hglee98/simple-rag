from typing import List
from langchain_openai import OpenAIEmbeddings


class EmbeddingSingleton:
    _instance = None
    _embeddings = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self, model_name: str = "text-embedding-3-small", **kwargs):
        if self._embeddings is None:
            self._embeddings = OpenAIEmbeddings(model=model_name, **kwargs)

    def embed_text(self, text: str) -> List[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            embedding = self._embeddings.embed_query(text)
            return embedding
        except Exception as e:
            raise RuntimeError(f"Failed to embed text: {str(e)}")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            raise ValueError("Texts list cannot be empty")

        if any(not text.strip() for text in texts):
            raise ValueError("All texts must be non-empty")

        try:
            embeddings = self._embeddings.embed_documents(texts)
            return embeddings
        except Exception as e:
            raise RuntimeError(f"Failed to embed texts: {str(e)}")

    def get_embedding_dimension(self) -> int:
        model_dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }

        return model_dimensions.get(self.model_name, 1536)

    @classmethod
    def get_instance(cls, model_name: str = "text-embedding-3-small", **kwargs):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._initialize(model_name, **kwargs)
        return cls._instance
