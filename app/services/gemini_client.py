import json
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from pydantic import ValidationError

from app.config import settings
from app.models.response import AuditResponse
from app.services.prompt_builder import SYSTEM_PROMPT, build_user_message


genai.configure(api_key=settings.gemini_api_key)

_generation_config = genai.GenerationConfig(
    temperature=0.1,
    top_p=0.95,
    response_mime_type="application/json",
)


class GeminiUnavailableError(Exception):
    """Gemini no está disponible (red, quota, autenticación)."""


class GeminiInvalidResponseError(Exception):
    """Gemini respondió pero el formato no es el esperado."""


def analyze_code(code: str, language: str) -> AuditResponse:
    model = genai.GenerativeModel(
        model_name=settings.gemini_model,
        system_instruction=SYSTEM_PROMPT,
        generation_config=_generation_config,
    )

    message = build_user_message(code, language)

    try:
        response = model.generate_content(message)
    except GoogleAPIError as e:
        raise GeminiUnavailableError(f"Error de API de Google: {e}") from e
    except Exception as e:
        raise GeminiUnavailableError(f"Error de red o timeout: {e}") from e

    # Gemini bloquea el contenido por safety filters → response.text es None
    if not response.parts:
        raise GeminiInvalidResponseError(
            "Gemini bloqueó la respuesta (safety filters). "
            "Revisá que el código de entrada no sea considerado contenido dañino."
        )

    raw = response.text

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise GeminiInvalidResponseError(f"Gemini devolvió JSON inválido: {e}") from e

    try:
        return AuditResponse.model_validate(data)
    except ValidationError as e:
        raise GeminiInvalidResponseError(
            f"El JSON de Gemini no respeta el esquema esperado: {e.error_count()} error(es)"
        ) from e
