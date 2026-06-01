from fastapi import FastAPI
from app.routers import audit

app = FastAPI(
    title="Code Audit AI Service",
    description="Servicio de inferencia que analiza código usando Gemini",
    version="1.0.0",
)

app.include_router(audit.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "UP", "service": "code-audit-ai"}
