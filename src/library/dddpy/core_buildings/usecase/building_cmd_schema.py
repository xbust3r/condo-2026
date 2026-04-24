from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional


class CreateBuildingSchema(BaseModel):
    condominium_id: int = Field(..., description="ID of the parent condominium")
    code: str = Field(..., max_length=50, description="Unique code within the condominium")
    name: str = Field(..., max_length=255, description="Building name")
    short_name: Optional[str] = Field(None, max_length=50, description="Short name for UI")
    description: Optional[str] = Field(None, description="Administrative notes")
    building_type_id: Optional[int] = Field(None, description="Building type FK")
    built_area: Optional[float] = Field(None, ge=0, description="Built area in m²")
    common_area: Optional[float] = Field(None, ge=0, description="Common area in m²")
    coefficient: Optional[float] = Field(None, ge=0, le=100, description="Participation coefficient 0-100")
    floors_count: int = Field(0, ge=0, description="Number of floors above ground")
    basements_count: int = Field(0, ge=0, description="Number of basement floors")
    units_planned: int = Field(0, ge=0, description="Expected number of units")
    sort_order: int = Field(0, ge=0, description="Visual ordering")


class UpdateBuildingSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    short_name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None)
    building_type_id: Optional[int] = Field(None)
    built_area: Optional[float] = Field(None, ge=0)
    common_area: Optional[float] = Field(None, ge=0)
    coefficient: Optional[float] = Field(None, ge=0, le=100)
    floors_count: Optional[int] = Field(None, ge=0)
    basements_count: Optional[int] = Field(None, ge=0)
    units_planned: Optional[int] = Field(None, ge=0)
    sort_order: Optional[int] = Field(None, ge=0)
    status: Optional[int] = Field(None, ge=0)