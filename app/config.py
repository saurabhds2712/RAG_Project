from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE",300)
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP",60)
)

TOP_K = int(
    os.getenv("TOP_K",4)
)

DATA_DIR = (
    BASE_DIR /
    os.getenv(
        "DATA_DIR",
        "data"
    )
)

VECTOR_DB_PATH = str(
    BASE_DIR /
    os.getenv(
        "VECTOR_DB_PATH",
        "vector_store/faiss_index"
    )
)

TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))

TOP_P = float(os.getenv("TOP_P",0.9))
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS",1024))