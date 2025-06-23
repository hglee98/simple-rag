from pydantic import BaseModel, Field
from typing import List, Optional


class Query(BaseModel):
    """Query model for the RAG system."""

    text: str = Field(..., description="The query string to search for relevant documents.")


class QueryResponse(BaseModel):
    """Response model for the query."""

    query: str = Field(..., description="The original query string.")
    documents: List[str] = Field(
        ..., description="List of relevant documents retrieved for the query."
    )
    metadata: Optional[dict] = Field(
        None, description="Optional metadata related to the query response."
    )
