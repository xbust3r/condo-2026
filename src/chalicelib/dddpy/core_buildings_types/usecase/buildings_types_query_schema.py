from pydantic import BaseModel
from typing import Optional


class BuildingTypeQuerySchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
