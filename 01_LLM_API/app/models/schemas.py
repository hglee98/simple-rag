from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

class RAGRequest(BaseModel):
    query: str
    context: str
    sources: List[str] = []

class RAGResponse(BaseModel):
    response: str
    sources: List[str] = []

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    error: Optional[str] = None