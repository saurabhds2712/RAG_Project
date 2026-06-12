from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class DocumentProcessor:

    def __init__(self, chunk_size, chunk_overlap):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # =====================================================
    # LOAD DOCUMENTS (ROBUST + FAULT TOLERANT)
    # =====================================================
    def load_documents(self, directory):

        path = Path(directory)

        if not path.exists():
            print(f"Directory not found: {directory}")
            return []

        documents = []

        try:
            files = list(path.rglob("*"))
        except Exception as e:
            raise RuntimeError(f"Failed to read directory: {e}")

        for file in files:

            try:

                if file.is_dir():
                    continue

                file_path = str(file.resolve())

                print(f"Loading file: {file.name}")

                # -------------------------
                # PDF LOADER
                # -------------------------
                if file.suffix.lower() == ".pdf":

                    loader = PyPDFLoader(file_path)
                    docs = loader.load()

                # -------------------------
                # TXT LOADER (SAFE ENCODING)
                # -------------------------
                elif file.suffix.lower() == ".txt":

                    try:
                        loader = TextLoader(file_path, encoding="utf-8")
                        docs = loader.load()

                    except UnicodeDecodeError:
                        print(f"UTF-8 failed, trying latin-1 for {file.name}")
                        loader = TextLoader(file_path, encoding="latin-1")
                        docs = loader.load()

                else:
                    print(f"Skipping unsupported file: {file.name}")
                    continue

                documents.extend(docs)
                print(f"Loaded {len(docs)} chunks from {file.name}")

            except Exception as e:
                print(f"Skipping file due to error: {file.name} → {e}")
                continue

        if not documents:
            print(f"No valid documents found in: {directory}")

        return documents

    # =====================================================
    # CHUNKING
    # =====================================================
    def chunk_documents(self, documents):

        try:

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

            chunks = splitter.split_documents(documents)

            if not chunks:
                raise ValueError("No chunks generated from documents")

            return chunks

        except Exception as e:
            raise RuntimeError(f"Chunking failed: {e}")