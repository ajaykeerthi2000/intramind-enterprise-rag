from pydantic import BaseModel
from typing import List, Literal


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class QueryRequest(BaseModel):
    question: str
    chat_history: List[ChatMessage] = []


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]
