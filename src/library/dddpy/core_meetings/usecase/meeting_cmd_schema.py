"""
Meeting command schemas — Pydantic input models.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateMeetingSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    created_by_user_id: int = Field(..., description="Creator user ID")
    title: str = Field(..., min_length=3, max_length=200, description="Title (min 3 chars)")
    meeting_type: str = Field('assembly', description="Meeting type: assembly, board, committee")
    description: Optional[str] = Field(None, description="Meeting description")
    meeting_date: datetime = Field(..., description="Date and time of the meeting")
    location: Optional[str] = Field(None, max_length=300, description="Meeting location")


class UpdateMeetingSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None)
    meeting_date: Optional[datetime] = Field(None)
    location: Optional[str] = Field(None, max_length=300)
    status: Optional[str] = Field(None, description="Status: scheduled, confirmed, held, cancelled")
