import uvicorn
from fastapi import FastAPI, APIRouter
from api.rag import router

app = FastAPI()
app.include_router(router, prefix="/api/rag", tags=["rag"])
base_router = APIRouter()


@base_router.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(base_router, tags=["base"])


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
