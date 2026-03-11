from pydantic import BaseModel
from typing import Optional


class UnityTypeQuerySchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
