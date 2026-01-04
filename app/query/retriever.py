from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List, Tuple


def retrieve_chunks(
    question: str,
    vectorstore_path: str = "_vector_store",
    top_k: int = 4,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> List[Tuple[Document, float]]:
    """
    Retrieve top-k relevant document chunks with similarity scores.
    """

    # 1. Load embedding model
    embedder = HuggingFaceEmbeddings(model_name=model_name)

    # 2. Load FAISS vector store
    vectorstore = FAISS.load_local(
        vectorstore_path,
        embedder,
        allow_dangerous_deserialization=True,
    )

    # 3. Retrieve documents WITH scores
    retrieved_with_scores = vectorstore.similarity_search_with_score(
        query=question,
        k=top_k,
    )

    # returned format: [(Document, score), ...]
    return retrieved_with_scores
