from fastapi import HTTPException
from app.prompts.prompt import SYSTEM_PROMPT,USER_PROMPT
from app.utils.citations import build_citations


class RAGService:

    def __init__(
        self,
        retriever,
        llm
    ):

        self.retriever = retriever
        self.llm = llm

    def ask(
        self,
        question: str
    ):

        try:

            if not question:

                return {
                    "answer":
                    "Question cannot be empty.",
                    "sources": []
                }

            if not question.strip():

                return {
                    "answer":
                    "Question cannot be empty.",
                    "sources": []
                }

            if self.retriever is None:

                return {
                    "answer":
                    "No data is present. Please upload data first.",
                    "sources": []
                }

            docs = (
                self.retriever.retrieve(
                    question
                )
            )

            if not docs:

                return {
                    "answer":
                    "I could not find the answer in the provided documents.",
                    "sources": []
                }

            context = "\n\n".join(
                doc.page_content
                for doc in docs
            )

            user_prompt = (
                USER_PROMPT.format(
                    context=context,
                    question=question
                )
            )

            answer = (
                self.llm.generate(
                    system_prompt=SYSTEM_PROMPT,
                    user_prompt=user_prompt
                )
            )

            return {
                "answer": answer,
                "sources": build_citations(
                    docs
                )
            }

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=f"RAG processing failed: {e}"
            )