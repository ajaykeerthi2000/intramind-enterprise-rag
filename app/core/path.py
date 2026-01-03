import os
from pathlib import Path

# Raw data (downloaded from Blob for processing)
RAW_DATA_PATH = Path(
    os.getenv("RAW_DATA_PATH", "./_raw_data")
)

# Vector store (FAISS index location)
VECTOR_STORE_PATH = Path(
    os.getenv("VECTOR_STORE_PATH", "./_vector_store")
)

# Ensure directories exist
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
