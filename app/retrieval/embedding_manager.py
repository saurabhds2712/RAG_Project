from langchain_huggingface import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL

class EmbeddingManager:
    def __init__(self):
        self.EMBEDDING_MODEL = EMBEDDING_MODEL

    def get_model(self):

        try:
            return HuggingFaceEmbeddings(
                model_name=self.EMBEDDING_MODEL
            )

        except Exception as e:
            raise RuntimeError(
                f"Embedding error: {e}"
            )