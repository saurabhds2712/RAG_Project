from google import genai

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    TEMPERATURE,
    TOP_P,
    MAX_OUTPUT_TOKENS
)


class GeminiClient:

    def __init__(self):

        try:

            self.client = genai.Client(
                api_key=GEMINI_API_KEY
            )

        except Exception as e:

            raise RuntimeError(
                f"Gemini initialization failed: {e}"
            )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> str:

        try:

            response = (
                self.client.models.generate_content(
                    model=GEMINI_MODEL,

                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": user_prompt
                                }
                            ]
                        }
                    ],

                    config={
                        "system_instruction": system_prompt,
                        "temperature": TEMPERATURE,
                        "top_p": TOP_P,
                        "max_output_tokens": MAX_OUTPUT_TOKENS
                    }
                )
            )

            if (
                not response
                or not response.text
                or not response.text.strip()
            ):
                raise ValueError(
                    "Empty response received from Gemini."
                )

            return response.text

        except Exception as e:

            raise RuntimeError(
                f"Gemini generation failed: {e}"
            )