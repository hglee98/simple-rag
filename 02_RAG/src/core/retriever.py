from langchain_chroma import Chroma
import os
import chromadb

from .embedding_client import EmbeddingModel


class Retriever:
    def __init__(self, collection_name: str):
        """Initialize the retriever with a specific collection."""
        self.client = chromadb.HttpClient(
            host=os.getenv("VECTOR_DB_HOST"),
            port=os.getenv("VECTOR_DB_PORT"),
        )
        self.collection = Chroma(
            collection_name=collection_name, client=self.client, embedding_function=EmbeddingModel()
        )

    def retrieve(self, query: str, n_results: int = 5) -> str:
        """Retrieve documents similar to the query."""
        results = self.collection.similarity_search_with_score(query=query, k=n_results)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        return context_text
