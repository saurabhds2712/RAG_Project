from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router,set_rag_service
from app.llm.gemini_client import GeminiClient
from app.services.rag_service import RAGService
from app.services.initialization_service import InitializationService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    Creates/loads FAISS, initializes retriever,
    initializes Gemini client, and injects
    RAGService into API routes.
    """

    try:
        print("=" * 50)
        print("Initializing RAG Application...")
        print("=" * 50)

        # Load or create FAISS index
        retriever = InitializationService().initialize()

        if retriever:
            print("Retriever initialized successfully.")
        else:
            print(  
                "Retriever not initialized. "
                "No documents available."
            )


        # Initialize Gemini
        llm_client = GeminiClient()

        print("Gemini client initialized successfully.")

        # Create RAG service
        rag_service = RAGService(
            retriever=retriever,
            llm=llm_client
        )

        # Inject into routes
        set_rag_service(rag_service)

        print("RAG service initialized successfully.")
        print("Application startup completed.")
        print("=" * 50)

    except Exception as e:
        print(
            f"Application startup failed: {str(e)}"
        )
        raise

    yield

    print("Shutting down application...")


app = FastAPI(
    title="RAG Assistant",
    description=(
        "Retrieval-Augmented Generation "
        "using Gemini + MiniLM + FAISS"
    ),
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
def root():
    """
    Root endpoint.
    """

    return {
        "message": "RAG Assistant is running",
        "status": "healthy"
    }