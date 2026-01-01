from typing import List
from app.schemas.query import ChatMessage


def build_chat_prompt(
    question: str,
    chat_history: List[ChatMessage],
    context: str,
    max_history: int = 4,
) -> str:
    """
    Build ChatGPT-style prompt with limited conversation memory.
    """

    recent_history = chat_history[-max_history:]

    conversation = ""
    for msg in recent_history:
        role = "User" if msg.role == "user" else "Assistant"
        conversation += f"{role}: {msg.content}\n"

    prompt = f"""
You are IntraMind, an internal enterprise knowledge intelligence system.

Answer ONLY using the provided context.
If the answer is not present in the context, say you do not know.

Context:
{context}

Conversation so far:
{conversation}

User question:
{question}

Answer:
"""
    return prompt.strip()
