from pydantic import BaseModel
from typing import Optional


class ResidentQuerySchema(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    unity_id: Optional[int] = None
    building_id: Optional[int] = None
    condominium_id: Optional[int] = None
    status: Optional[str] = None
