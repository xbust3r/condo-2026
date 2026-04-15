from pydantic import BaseModel, Field, validator
from typing import Optional


_VALID_OCCUPANCY_STATUSES = {"vacant", "occupied", "reserved", "maintenance", "blocked"}


class CreateUnitSchema(BaseModel):
    building_id: int = Field(..., description="ID of the parent building")
    unit_number: str = Field(
        ...,
        max_length=50,
        description="Unit number (e.g. 101, A-12, PH-1). Must be unique within building.",
    )
    unit_type_id: Optional[int] = Field(
        None, description="Unit type FK (e.g. apartment, office, local)"
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
    condominium_coefficient: Optional[float] = Field(
        None, ge=0, le=100,
        description="Condominium participation coefficient 0-100 — for maintenance fee calculation",
    )


class UpdateUnitSchema(BaseModel):
    unit_type_id: Optional[int] = Field(None)
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

    @validator("occupancy_status")
    def validate_occupancy_status(cls, value):
        if value is not None and value not in _VALID_OCCUPANCY_STATUSES:
            raise ValueError(
                f"occupancy_status must be one of: {', '.join(sorted(_VALID_OCCUPANCY_STATUSES))}"
            )
        return value
    sort_order: Optional[int] = Field(None, ge=0)
    status: Optional[int] = Field(None, ge=0)
    condominium_coefficient: Optional[float] = Field(
        None, ge=0, le=100,
        description="Condominium participation coefficient 0-100",
    )