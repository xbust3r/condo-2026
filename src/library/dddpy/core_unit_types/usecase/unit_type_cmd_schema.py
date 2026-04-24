from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional


class CreateUnitTypeSchema(BaseModel):
    condominium_id: Optional[int] = Field(
        None,
        description="Condominium ID. NULL or omitted = global/system type. Set to a condominium ID for custom types.",
    )
    code: str = Field(..., max_length=50, description="Unique code within the scope")
    name: str = Field(..., max_length=255, description="Type name")
    description: Optional[str] = Field(None, description="Detailed description")
    usage_class: Optional[str] = Field(
        None,
        description="Usage classification: residential|commercial|parking|storage|service",
    )
    sort_order: int = Field(0, ge=0, description="Display order")


class UpdateUnitTypeSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    usage_class: Optional[str] = Field(
        None,
        description="Usage classification: residential|commercial|parking|storage|service",
    )
    sort_order: Optional[int] = Field(None, ge=0)
    status: Optional[int] = Field(None, ge=0, le=1, description="1=active, 0=inactive")