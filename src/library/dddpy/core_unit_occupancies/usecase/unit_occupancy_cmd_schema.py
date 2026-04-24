from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CreateUnitOccupancySchema(BaseModel):
    unit_id: int = Field(..., description="ID of the unit")
    user_id: int = Field(..., description="ID of the user occupying the unit")
    occupancy_type_id: int = Field(
        ...,
        description="FK to core_occupancy_types.id. Must reference an active occupancy type.",
    )
    status: str = Field(
        "active",
        description="Occupancy status: active / inactive / historical / pending",
    )
    start_date: date = Field(..., description="Start date of occupancy")
    end_date: Optional[date] = Field(None, description="End date of occupancy (nullable)")
    is_primary: bool = Field(False, description="Whether this is the primary occupancy for the unit")
    authorized_by_user_id: Optional[int] = Field(
        None, description="ID of the user who authorized this occupancy"
    )
    notes: Optional[str] = Field(None, description="Administrative notes")


class UpdateUnitOccupancySchema(BaseModel):
    occupancy_type_id: Optional[int] = Field(
        None,
        description="FK to core_occupancy_types.id",
    )
    status: Optional[str] = Field(
        None,
        description="Occupancy status: active / inactive / historical / pending",
    )
    start_date: Optional[date] = Field(None, description="Start date of occupancy")
    end_date: Optional[date] = Field(None, description="End date of occupancy")
    is_primary: Optional[bool] = Field(None, description="Whether this is the primary occupancy")
    authorized_by_user_id: Optional[int] = Field(
        None, description="ID of the user who authorized this occupancy"
    )
    notes: Optional[str] = Field(None, description="Administrative notes")
