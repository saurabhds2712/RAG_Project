from fastapi import APIRouter
from app.models.schemas import QueryRequest
router = APIRouter()
rag_service = None


def set_rag_service(service):
    global rag_service
    rag_service = service


@router.post("/ask")
def ask(request: QueryRequest):

    if rag_service is None:

        return {
            "answer":
            "No data is present. Please upload data first.",
            "sources": []
        }

    return rag_service.ask(
        request.question
    )


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }