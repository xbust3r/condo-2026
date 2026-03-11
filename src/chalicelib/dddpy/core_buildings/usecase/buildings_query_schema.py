from pydantic import BaseModel
from typing import Optional


class BuildingQuerySchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    condominium_id: Optional[int] = None
