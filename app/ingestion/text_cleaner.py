import re
from langchain_core.documents import Document


def clean_document(doc: Document) -> Document:
    """
    Clean a single Document's text while preserving metadata.
    """
    text = doc.page_content

    # Normalize whitespace (multiple spaces, newlines → single space)
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing spaces
    text = text.strip()

    return Document(
        page_content=text,
        metadata=doc.metadata
    )


def clean_documents(docs: list[Document]) -> list[Document]:
    """
    Clean a list of Documents.
    """
    return [clean_document(doc) for doc in docs]
