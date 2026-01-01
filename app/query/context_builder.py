from langchain_core.documents import Document
from typing import List, Tuple


def build_context(
    docs_with_scores: List[Tuple[Document, float]],
    max_chunks: int = 3,
) -> str:
    """
    Build a clean textual context from retrieved Documents.
    Similarity scores are ignored here on purpose.
    """

    # Take only top-N documents
    selected = docs_with_scores[:max_chunks]

    context_blocks = []

    for i, (doc, _) in enumerate(selected, start=1):
        block = (
            f"[Source {i} | {doc.metadata.get('source_file')}]\n"
            f"{doc.page_content.strip()}"
        )
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)
    return context
