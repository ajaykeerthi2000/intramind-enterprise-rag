from pathlib import Path
import yaml

from langchain_core.documents import Document


from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredHTMLLoader,
)


def load_text_file(file_path: Path) -> list[Document]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    return [Document(page_content=text, metadata={})]


def load_documents(data_dir: Path, metadata_path: Path):
    with metadata_path.open("r") as f:
        metadata_map = yaml.safe_load(f)["documents"]

    documents = []

    for file_path in data_dir.iterdir():
        if not file_path.is_file():
            continue

        meta = metadata_map.get(file_path.name)
        if not meta:
            continue

        ext = file_path.suffix.lower()

        if ext == ".pdf":
            docs = PyPDFLoader(str(file_path)).load()
        elif ext == ".docx":
            docs = UnstructuredWordDocumentLoader(str(file_path)).load()
        elif ext == ".html":
            docs = UnstructuredHTMLLoader(str(file_path)).load()
        elif ext in [".md", ".txt"]:
            docs = load_text_file(file_path)
        else:
            continue

        for doc in docs:
            doc.metadata |= meta
            doc.metadata["source_file"] = file_path.name

        documents.extend(docs)

    return documents



# # ---- test ---- 
# out = load_documents( data_dir=Path("Data"), metadata_path=Path("document_metadata.yaml") )
# print(out[0].metadata["source_file"])
