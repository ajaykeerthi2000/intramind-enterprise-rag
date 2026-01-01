from pathlib import Path

# ---- ingestion pipeline ----
from app.ingestion.document_loader import load_documents
from app.ingestion.chunker import chunk_documents

# ---- vectorstore utilities ----
from app.core.vector_store import (
    create_faiss_vectorstore,
    save_vectorstore,
)

# ---- paths (adjust only if needed) ----
DATA_DIR = Path("Data")
METADATA_PATH = Path("document_metadata.yaml")
VECTORSTORE_PATH = "vector_store"


def main():
    print("🚀 Starting ingestion pipeline...")

    # 1️⃣ Load raw documents + metadata
    print("📄 Loading documents...")
    documents = load_documents(
        data_dir=DATA_DIR,
        metadata_path=METADATA_PATH,
    )
    print(f"✅ Loaded {len(documents)} documents")

    if not documents:
        raise RuntimeError("No documents found. Check Data directory or metadata.")

    # 2️⃣ Chunk documents
    print("✂️ Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")

    if not chunks:
        raise RuntimeError("Chunking failed. No chunks created.")

    # 3️⃣ Create FAISS vector store (embeddings)
    print("🧠 Creating FAISS vector store...")
    vectorstore = create_faiss_vectorstore(chunks)

    # 4️⃣ Save vector store to disk
    print("💾 Saving vector store to disk...")
    save_vectorstore(vectorstore, VECTORSTORE_PATH)

    print("🎉 Vector store built successfully!")
    print(f"📂 Saved at: {VECTORSTORE_PATH}/")


if __name__ == "__main__":
    main()
