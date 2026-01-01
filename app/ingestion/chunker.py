from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    docs: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 100,) -> list[Document]:
    """
    Split documents into smaller chunks while preserving metadata.
    """
    splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)

    chunks=splitter.split_documents(docs)

    return chunks

