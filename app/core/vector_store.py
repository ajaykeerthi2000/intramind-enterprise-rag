from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List


def create_faiss_vectorstore(
    docs: List[Document],
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> FAISS:
    """
    Create a FAISS vector store from chunked Documents.
    (Ingestion phase)
    """
    embedder = HuggingFaceEmbeddings(model_name=model_name)

    vectorstore = FAISS.from_documents(
        documents=docs,
        embedding=embedder,
    )

    return vectorstore


def save_vectorstore(
    vectorstore: FAISS,
    path: str = "vector_store",
) -> None:
    """
    Persist FAISS vector store to disk.
    """
    vectorstore.save_local(path)


def load_vectorstore(
    path: str = "vector_store",
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> FAISS:
    """
    Load FAISS vector store from disk.
    (Query phase)
    """
    embedder = HuggingFaceEmbeddings(model_name=model_name)

    return FAISS.load_local(
        path,
        embedder,
        allow_dangerous_deserialization=True,
    )
