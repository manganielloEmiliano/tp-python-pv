from typing import Literal, Optional
from pydantic import BaseModel


class AuditIssue(BaseModel):
    severity: Literal["CRITICO", "ADVERTENCIA", "SUGERENCIA"]
    category: Literal["SECURITY", "REFACTORING", "SYNTAX", "PERFORMANCE"]
    title: str
    description: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    refactored_code: Optional[str] = None


class AuditResponse(BaseModel):
    pedagogical_explanation: str
    issues: list[AuditIssue]
