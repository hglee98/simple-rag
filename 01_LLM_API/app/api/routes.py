from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, HealthResponse
from app.models.llm_singleton import LLMSingleton
from app.models.embedding import EmbeddingSingleton
from app.config.settings import SYSTEM_PROMPT, get_tokenizer

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        LLMSingleton.get_instance()
        return HealthResponse(status="healthy", model_loaded=True)
    except Exception as e:
        return HealthResponse(status="unhealthy", model_loaded=False, error=str(e))


@router.post("/generate", response_model=QueryResponse)
async def generate_response(request: QueryRequest):
    try:
        llm = LLMSingleton.get_instance()
        tokenizer = get_tokenizer()

        messages = [SYSTEM_PROMPT, {"role": "user", "content": request.query}]
        query = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        response_text = llm.generate(query)
        return QueryResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embed", response_model=list)
async def embed_single_text(text: str):
    try:
        embeddings = EmbeddingSingleton.get_instance()
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        embedding = embeddings.embed_text(text)
        return embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
