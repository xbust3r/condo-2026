from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CreateResidentsCmdSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    condominium_id: int
    building_id: int
    unity_id: int
    user_id: int
    type: str = Field(..., max_length=100)
    status: int = Field(default=1, ge=0, le=2)

class UpdateResidentsCmdSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    condominium_id: Optional[int] = None
    building_id: Optional[int] = None
    unity_id: Optional[int] = None
    user_id: Optional[int] = None
    type: Optional[str] = Field(None, max_length=100)
    status: Optional[int] = Field(None, ge=0, le=2)
