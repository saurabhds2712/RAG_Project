from pathlib import Path
import os
import json

from app.config import (
    VECTOR_DB_PATH,
    DATA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K
)

from app.ingestion.document_processor import DocumentProcessor
from app.retrieval.vector_store_manager import VectorStoreManager
from app.retrieval.retriever import Retriever


class InitializationService:

    REGISTRY_FILE = "vector_store/index_registry.json"

    def initialize(self):

        try:

            vector_manager = VectorStoreManager()

            processor = DocumentProcessor(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP
            )

            faiss_file = Path(f"{VECTOR_DB_PATH}.faiss")

            # =====================================================
            # STEP 1: Load registry safely
            # =====================================================
            registry = {}

            os.makedirs("vector_store", exist_ok=True)

            if os.path.exists(self.REGISTRY_FILE):

                try:
                    with open(self.REGISTRY_FILE, "r") as f:
                        content = f.read().strip()

                        if content:
                            registry = json.loads(content)
                        else:
                            registry = {}

                except json.JSONDecodeError:
                    print("⚠️ Corrupted registry file detected. Resetting registry...")
                    registry = {}

                except Exception as e:
                    print(f"⚠️ Registry load error: {e}")
                    registry = {}

            # =====================================================
            # STEP 2: Load FAISS safely (IMPORTANT FIX HERE)
            # =====================================================
            vector_db = None

            if faiss_file.exists():

                print("Loading existing FAISS index...")

                try:
                    vector_db = vector_manager.load(VECTOR_DB_PATH)

                except Exception as e:
                    print(f"⚠️ FAISS load failed: {e}")
                    vector_db = None

            print(f"DATA_DIR = {DATA_DIR}")

            # =====================================================
            # STEP 3: Load documents
            # =====================================================
            documents = processor.load_documents(DATA_DIR)

            if not documents:

                print("No documents available. Starting without vector DB.")
                return None

            # =====================================================
            # STEP 4: Identify new documents
            # =====================================================
            new_docs = []

            for doc in documents:

                source_path = doc.metadata.get("source")

                if not source_path:
                    continue

                filename = Path(source_path).name

                if filename not in registry:
                    new_docs.append(doc)

            # =====================================================
            # STEP 5: If no new documents
            # =====================================================
            if not new_docs:

                print("No new documents found. Using existing FAISS index.")

                # 🔥 HARD SAFETY CHECK (CRITICAL FIX)
                if vector_db is None:

                    print("FAISS not in memory. Trying reload...")

                    try:
                        vector_db = vector_manager.load(VECTOR_DB_PATH)

                    except Exception as e:
                        print(f"FAISS reload failed: {e}")
                        return None

                return Retriever(vector_db, TOP_K)

            # =====================================================
            # STEP 6: Chunk new documents only
            # =====================================================
            new_chunks = processor.chunk_documents(new_docs)

            print(f"New chunks created: {len(new_chunks)}")

            # =====================================================
            # STEP 7: Update FAISS (incremental)
            # =====================================================
            if vector_db is None:

                vector_db = vector_manager.create(new_chunks)

            else:

                vector_db.add_documents(new_chunks)

            print("Vector DB updated successfully")

            # =====================================================
            # STEP 8: Save FAISS
            # =====================================================
            vector_manager.save(vector_db, VECTOR_DB_PATH)

            # =====================================================
            # STEP 9: Update registry
            # =====================================================
            for doc in new_docs:

                source_path = doc.metadata.get("source")

                if source_path:
                    filename = Path(source_path).name
                    registry[filename] = True

            with open(self.REGISTRY_FILE, "w") as f:
                json.dump(registry, f, indent=2)

            # =====================================================
            # STEP 10: Return retriever
            # =====================================================
            return Retriever(vector_db, TOP_K)

        except Exception as e:

            print(f"Initialization warning: {e}")

            return None