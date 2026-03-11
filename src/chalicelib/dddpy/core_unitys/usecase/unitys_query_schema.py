from pydantic import BaseModel
from typing import Optional


class UnityQuerySchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    building_id: Optional[int] = None
