import os
from pathlib import Path

from azure.storage.blob import BlobServiceClient

# ---- ingestion pipeline ----
from app.ingestion.document_loader import load_documents
from app.ingestion.chunker import chunk_documents

# ---- vectorstore utilities ----
from app.core.vector_store import (
    create_faiss_vectorstore,
    save_vectorstore,
)

# -----------------------------
# Configuration (cloud-safe)
# -----------------------------
RAW_DATA_CONTAINER = os.getenv("RAW_DATA_CONTAINER", "raw-data")
VECTOR_CONTAINER = os.getenv("VECTOR_CONTAINER", "vector-store")

RAW_DATA_PATH = Path(os.getenv("RAW_DATA_PATH", "./_raw_data"))
VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", "./_vector_store"))

RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Blob helpers
# -----------------------------
def get_blob_service():
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING not set")
    return BlobServiceClient.from_connection_string(conn_str)


def download_container(container_name: str, target_dir: Path):
    print(f"⬇️ Downloading data from Blob container: {container_name}")
    service = get_blob_service()
    container = service.get_container_client(container_name)

    for blob in container.list_blobs():
        local_file = target_dir / blob.name
        local_file.parent.mkdir(parents=True, exist_ok=True)
        with open(local_file, "wb") as f:
            f.write(container.download_blob(blob.name).readall())


def upload_directory(container_name: str, source_dir: Path):
    print(f"⬆️ Uploading vectors to Blob container: {container_name}")
    service = get_blob_service()
    container = service.get_container_client(container_name)

    for file in source_dir.rglob("*"):
        if file.is_file():
            blob_path = file.relative_to(source_dir).as_posix()
            with open(file, "rb") as f:
                container.upload_blob(blob_path, f, overwrite=True)


# -----------------------------
# Main pipeline
# -----------------------------
def main():
    print("🚀 Starting vector build pipeline")

    # 1️⃣ Download raw data from Blob
    download_container(RAW_DATA_CONTAINER, RAW_DATA_PATH)

    # 2️⃣ Load documents
    print("📄 Loading documents")
    documents = load_documents(
        data_dir=RAW_DATA_PATH,
        metadata_path=RAW_DATA_PATH / "document_metadata.yaml",
    )

    if not documents:
        raise RuntimeError("No documents found in raw data")

    # 3️⃣ Chunk documents
    print("✂️ Chunking documents")
    chunks = chunk_documents(documents)

    if not chunks:
        raise RuntimeError("No chunks created")

    # 4️⃣ Create vector store
    print("🧠 Creating FAISS vector store")
    vectorstore = create_faiss_vectorstore(chunks)

    # 5️⃣ Save vectors locally
    print("💾 Saving vector store locally")
    save_vectorstore(vectorstore, VECTOR_STORE_PATH)

    # 6️⃣ Upload vectors back to Blob
    upload_directory(VECTOR_CONTAINER, VECTOR_STORE_PATH)

    print("🎉 Vector creation completed successfully")


if __name__ == "__main__":
    main()
