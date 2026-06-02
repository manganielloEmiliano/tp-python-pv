from typing import Literal
from pydantic import BaseModel, field_validator


SUPPORTED_LANGUAGES = {"python", "java", "kotlin"}


class AnalyzeRequest(BaseModel):
    code: str
    language: str

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        lang = v.strip().lower()
        if lang not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Lenguaje '{v}' no soportado. Soportados: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
            )
        return lang

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El código no puede estar vacío")
        return v
