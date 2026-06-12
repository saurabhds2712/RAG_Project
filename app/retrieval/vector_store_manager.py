from langchain_community.vectorstores import FAISS
from app.retrieval.embedding_manager import EmbeddingManager


class VectorStoreManager:

    def __init__(self):

        self.embedding_model = EmbeddingManager().get_model()

    def create(self, chunks):

        try:
            return FAISS.from_documents(
                chunks,
                self.embedding_model
            )

        except Exception as e:
            raise RuntimeError(f"FAISS creation failed: {e}")

    def save(self, db, path):

        try:
            db.save_local(path)

        except Exception as e:
            raise RuntimeError(f"FAISS save failed: {e}")

    def load(self, path):

        try:
            return FAISS.load_local(
                path,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )

        except Exception as e:
            raise RuntimeError(f"FAISS load failed: {e}")

    def add_documents(self, vector_db, new_chunks):

        try:

            vector_db.add_documents(new_chunks)
            return vector_db

        except Exception as e:
            raise RuntimeError(f"FAISS incremental update failed: {e}")