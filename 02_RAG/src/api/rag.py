from fastapi import APIRouter, HTTPException
from langchain.prompts import ChatPromptTemplate
from model.model import Query
from core.retriever import Retriever
from core.llm_client import LLMClient

router = APIRouter()
retriever = Retriever(collection_name="rag_collection")
llm_client = LLMClient()

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


@router.post("/generate")
async def generate_rag_response(query: Query):
    """
    Generate a response for the given query using RAG.

    Args:
        query (Query): The query object containing the query string.

    Returns:
        dict: A dictionary containing the response.
    """
    try:
        # Retrieve relevant documents
        context = retriever.retrieve(query.text, n_results=3)
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format_prompt(context=context, question=query.text)
        # Generate response using LLM
        response_text = llm_client.generate(prompt.to_string())

        return response_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
