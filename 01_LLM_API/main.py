import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.config.settings import SERVER_CONFIG
from app.models.llm_singleton import LLMSingleton
from app.models.embedding import EmbeddingSingleton


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for the FastAPI application"""
    # Initialize LLM singleton on startup
    startup_event()
    yield


def startup_event():
    """Initialize LLM singleton on application startup"""
    LLMSingleton.get_instance()
    EmbeddingSingleton.get_instance()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=SERVER_CONFIG["host"],
        port=SERVER_CONFIG["port"],
        log_level=SERVER_CONFIG["log_level"],
    )
