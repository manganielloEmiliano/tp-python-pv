# code-audit-ai

Servicio de inferencia de la **Plataforma de Auditoría de Código**.
Recibe fragmentos de código desde el orquestador (Repo B) y usa la API de Gemini para auditarlos como un "Senior Developer".

## Stack

- Python 3.13 / FastAPI
- Google Generative AI SDK (`google-generativeai`)
- Pydantic v2 para validación de request y response
- Uvicorn como servidor ASGI

## Requisitos

- Python 3.12+
- API Key de [Google AI Studio](https://aistudio.google.com/)

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

## Configuración

Copiar `.env.example` a `.env` y completar:

```
GEMINI_API_KEY=tu_api_key
GEMINI_MODEL=gemini-2.5-flash
INTERNAL_API_KEY=mismo_valor_que_en_repo_b
```

## Correr

```bash
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Docs en: `http://localhost:8000/docs`

## Endpoint

**POST /analyze**

Header requerido: `X-Internal-Api-Key: <valor>`

```json
// Request
{ "code": "SELECT * FROM users WHERE id = '" + id + "'", "language": "java" }

// Response
{
  "pedagogical_explanation": "...",
  "issues": [
    {
      "severity": "CRITICO",
      "category": "SECURITY",
      "title": "SQL Injection detectado",
      "description": "...",
      "line_start": 1,
      "line_end": 1,
      "refactored_code": "SELECT * FROM users WHERE id = ?"
    }
  ]
}
```

## Lenguajes soportados

`python`, `java`, `kotlin`
