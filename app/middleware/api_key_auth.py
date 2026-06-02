from fastapi import Request, HTTPException, status
from app.config import settings


async def verify_internal_api_key(request: Request) -> None:
    key = request.headers.get("X-Internal-Api-Key")
    if key != settings.internal_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida o ausente",
        )
