from pydantic import BaseModel, field_validator


class QueryRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):

        if not value.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        return value