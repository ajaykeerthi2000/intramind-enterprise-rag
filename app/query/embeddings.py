from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

def Embed_documents(docs:list[Document],model_name:str="sentence-transformers/all-MiniLM-L6-v2",):
    
    """
    Generate embeddings for a list of Documents.
    Returns list of (embedding_vector, Document).
    """
    embedder=HuggingFaceEmbeddings(model_name=model_name)
    texts=[doc.page_content for doc in docs]
    embeddings=embedder.embed_documents(texts)

    return embeddings
