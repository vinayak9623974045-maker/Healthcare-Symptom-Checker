from pydantic import BaseModel
from typing import List, Optional

class SymptomRequest(BaseModel):
    text: str

class Condition(BaseModel):
    name: str
    likelihood: float  # 0-1
    rationale: Optional[str]

class SymptomResponse(BaseModel):
    conditions: List[Condition]
    recommendations: List[str]
    disclaimer: str
