from pydantic import BaseModel
from typing import Optional


class CondominiumQuerySchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
