import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables once
load_dotenv()


def get_rag_chain():
    """
    Return a configured LLM client.
    Prompt construction is handled upstream.
    """
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.0,
    )
