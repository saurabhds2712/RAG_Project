# RAG AI Assistant (Gemini + FAISS + MiniLM)
A production-grade modular **Retrieval-Augmented Generation (RAG)** AI Assistant that answers users' query based on uploaded documents using Google Gemini LLM.

## Components/Technology:
- LLM - Google Gemini ('gemini-2.5-flash')
- Embeddings - 'sentence-transformers/all-MiniLM-L6-V2'
- Vector Store - FAISS 
- Document Support- '.txt', '.pdf'

## Features
- Supports PDF document ingestion
- Semantic search using FAISS
- Embeddings via 'sentence-transformers/all-MiniLM-L6-v2'
- Answer generation using Google Gemini
- Source citation with page-level references
- Config-driven architecture (.env based)
- Error handling & fallback responses
- Persistent vector store (no re-embedding on restart)
- Modular and production-style FastAPI backend

## Architecture:

        User Query
            ↓
        FastAPI Endpoint (/ask)
            ↓
        RAGService
            ↓
        Retriever (FAISS)
            ↓
        Top-K Relevant Chunks
            ↓
        Prompt Builder (System + User Prompt)
            ↓
        Gemini LLM
            ↓
        Response + Citations

## Project Structure
    RAG_Project/
    │
    ├── app/
    │ ├── api/
    │ ├── ingestion/
    │ ├── retrieval/
    │ ├── llm/
    │ ├── prompts/
    │ ├── services/
    │ ├── utils/
    │ ├── config.py
    │ └── main.py
    │
    ├── data/ # PDF documents
    ├── vector_store/ # FAISS index storage
    ├── .env
    ├── requirements.txt
    └── README.md

## Setup Instructions

## 1. Clone repository
git clone <repo-url>
cd RAG_Project

## 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

## 3. Install dependencies
pip install -r requirements.txt

## 4. Setup environment variables/Configure API Key
    Create .env file and set your Gemini API KEY (GEMINI_API_KEY = your api key)
    GEMINI_API_KEY="API Key"
    GEMINI_MODEL=gemini-2.5-flash
    CHUNK_SIZE=1500
    CHUNK_OVERLAP=300
    TOP_K=3
    TEMPERATURE=0.2
    TOP_P=0.9
    MAX_OUTPUT_TOKENS=1024
    DATA_DIR=data
    VECTOR_DB_PATH=vector_store/faiss_index
    EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

## 5. Add documents in data folder

## 6. Run the server
uvicorn app.main:app --reload

## API Usage

# Health Check
GET /health
# Ask Question
POST /ask

## Sample Request and Response

# Request:
    {
    "question": "What are the optimizers used in deep learning"
    }

# Response:

    {
    "answer": "Common optimization algorithms used in deep learning include:\n*   SGD\n*   Adam\n*   RMSProp",
    "sources": [
        {
        "document": "Deep_Learning_5_Page_Guide.pdf",
        "page": 4
        },
        {
        "document": "Deep_Learning_5_Page_Guide.pdf",
        "page": 2
        },
        {
        "document": "Deep_Learning_5_Page_Guide.pdf",
        "page": 3
        }
    ]
    }




## Design Decisions:

### Chunking strategy
- Documents are split into fixed-size overlapping chunks before embedding.
- Chunking is configured via environment variables:
    - CHUNK_SIZE (default: 1500)
    - CHUNK_OVERLAP (default: 300)
- Overlap is used to preserve semantic continuity between chunks and avoid context fragmentation across pages.
- This improves retrieval quality for multi-paragraph and multi-page PDF content.

### Embeddings
- Uses sentence-transformers/all-MiniLM-L6-v2 model for generating embeddings.
- Provides a strong balance between:
    - Speed (lightweight model)
    - Semantic accuracy (384-dimensional embeddings)
- Embeddings are generated once during ingestion and reused via FAISS persistence.
- Model is configurable via environment variable for flexibility.

### Vector store
- FAISS is used as the local vector database for similarity search.
- Uses exact search (IndexFlatL2 / cosine via normalized vectors indirectly through LangChain wrapper).
- Persistent storage strategy:
    - FAISS index is saved to disk (vector_store/)
    - Metadata is preserved alongside embeddings
- On application restart:
    - If index exists → it is loaded
    - If missing → index is rebuilt from documents

### Prompt engineering
- Uses a two-layer prompt design:
    - System Prompt: Defines strict behavior rules (grounding, hallucination control, refusal behavior)
    - User Prompt: Injects retrieved context + user question dynamically
- Model is configured with:
    - temperature = 0.2 (low randomness → higher factual accuracy)
    - top_p = 0.9 (controlled diversity)
    - max_output_tokens for complete responses without truncation

## Embedding Persistence Strategy
- FAISS index is saved locally on disk after first successful ingestion.
- Avoids recomputation on restart 
- Only rebuilds when missing

## Error Handling Strategy
- Multi-layered try-except handling across:
    - API layer (FastAPI routes)
    - Service layer (RAG pipeline)
    - Retrieval layer (FAISS search)
    - LLM layer (Gemini API calls) 
- Graceful fallback responses:
    - No documents available → “No data is present. Please upload data first.”
    - No relevant chunks found → “I could not find the answer in the provided documents.”
    - LLM failure → HTTP 500 with controlled error message
- Prevents server crashes even in edge cases like:
    - Missing data directory
    - Empty vector store
    - API failures 

## API Design Strategy
- Built using FastAPI for lightweight, high-performance REST APIs.
- Single primary endpoint:
    - POST /ask → handles full RAG pipeline execution
- Stateless request handling:
    - Each request independently retrieves context and generates response
- Health check endpoint:
    - GET /health for service monitoring

## Request Validation (Pydantic Schema)
- API input is validated using Pydantic models
- Ensures type safety and prevents invalid queries from entering the pipeline

## Future Improvements
- Add reranker model (Cross-Encoder) 
- Add hybrid search (BM25 + FAISS) 
- Add document upload API 
- Add streaming responses 
- Add Redis cache for queries 
- Add observability (logs + tracing)


