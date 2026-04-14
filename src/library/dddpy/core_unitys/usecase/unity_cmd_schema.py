from pydantic import BaseModel, Field
from typing import Optional


class CreateUnitySchema(BaseModel):
    building_id: int = Field(..., description="ID of the parent building")
    unit_number: str = Field(
        ...,
        max_length=50,
        description="Unit number (e.g. 101, A-12, PH-1). Must be unique within building.",
    )
    unity_type_id: Optional[int] = Field(
        None, description="Unity type FK (e.g. apartment, office, local)"
    )
    code: Optional[str] = Field(
        None,
        max_length=50,
        description="Internal operational code. Unique within building if set.",
    )
    name: Optional[str] = Field(
        None, max_length=255, description="Optional display/commercial name"
    )
    description: Optional[str] = Field(
        None, description="Administrative notes"
    )
    private_area: Optional[float] = Field(
        None, ge=0, description="Private area in m²"
    )
    coefficient: Optional[float] = Field(
        None, ge=0, le=100, description="Copropiedad coefficient 0-100"
    )
    floor_number: Optional[int] = Field(
        None, description="Floor number for logic/ordering (negatives allowed for basement)"
    )
    floor_label: Optional[str] = Field(
        None, max_length=30,
        description="Floor label for UI (e.g. 'Sótano 1', 'Mezzanine', 'PH')"
    )
    occupancy_status: str = Field(
        "vacant",
        description="Occupancy status: vacant|occupied|reserved|maintenance|blocked",
    )
    sort_order: int = Field(0, ge=0, description="Visual ordering within building")


class UpdateUnitySchema(BaseModel):
    unity_type_id: Optional[int] = Field(None)
    unit_number: Optional[str] = Field(None, max_length=50)
    code: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    private_area: Optional[float] = Field(None, ge=0)
    coefficient: Optional[float] = Field(None, ge=0, le=100)
    floor_number: Optional[int] = Field(None)
    floor_label: Optional[str] = Field(None, max_length=30)
    occupancy_status: Optional[str] = Field(
        None,
        description="Occupancy status: vacant|occupied|reserved|maintenance|blocked",
    )
    sort_order: Optional[int] = Field(None, ge=0)
    status: Optional[int] = Field(None, ge=0)
