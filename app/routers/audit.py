from fastapi import APIRouter, Depends, HTTPException, status

from app.middleware.api_key_auth import verify_internal_api_key
from app.models.request import AnalyzeRequest
from app.models.response import AuditResponse
from app.services.gemini_client import (
    analyze_code,
    GeminiUnavailableError,
    GeminiInvalidResponseError,
)

router = APIRouter(
    prefix="/analyze",
    dependencies=[Depends(verify_internal_api_key)],
)


@router.post("", response_model=AuditResponse)
async def analyze(request: AnalyzeRequest) -> AuditResponse:
    try:
        return analyze_code(request.code, request.language)
    except GeminiInvalidResponseError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        )
    except GeminiUnavailableError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
