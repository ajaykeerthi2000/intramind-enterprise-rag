# app/core/blob_storage.py

import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient


def _get_blob_service():
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise RuntimeError(
            "AZURE_STORAGE_CONNECTION_STRING is not set"
        )
    return BlobServiceClient.from_connection_string(conn_str)


def download_container(container_name: str, target_dir: Path):
    """
    Download all blobs from a container into a local directory.
    """
    service = _get_blob_service()
    container = service.get_container_client(container_name)

    for blob in container.list_blobs():
        local_file = target_dir / blob.name
        local_file.parent.mkdir(parents=True, exist_ok=True)

        with open(local_file, "wb") as f:
            f.write(container.download_blob(blob.name).readall())


def upload_directory(container_name: str, source_dir: Path):
    """
    Upload all files from a local directory to a Blob container.
    """
    service = _get_blob_service()
    container = service.get_container_client(container_name)

    for file in source_dir.rglob("*"):
        if file.is_file():
            blob_path = file.relative_to(source_dir).as_posix()
            with open(file, "rb") as f:
                container.upload_blob(
                    blob_path,
                    f,
                    overwrite=True
                )
