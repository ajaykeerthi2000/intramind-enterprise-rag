from fastapi import FastAPI
from app.api.query import router as query_router

app = FastAPI(
    title="IntraMind – Internal Knowledge Intelligence Platform",
    description="Enterprise-grade RAG backend for internal organizational knowledge",
)


app.include_router(query_router)
