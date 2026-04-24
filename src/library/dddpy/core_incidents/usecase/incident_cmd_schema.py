"""
Incident command schemas — Pydantic input models.
"""
from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Field


class CreateIncidentSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    unit_id: int = Field(..., description="Unit ID where the incident occurred")
    category: str = Field(..., description="Category: plumbing, electrical, structural, common_areas, elevator, painting, cleaning, pest_control, security, other")
    title: str = Field(..., min_length=3, max_length=150, description="Incident title")
    description: str = Field(..., min_length=10, description="Detailed description (min 10 chars)")
    priority: str = Field('medium', description="Priority: low, medium, high, urgent (default medium)")
    photos: Optional[List[str]] = Field(None, description="List of photo URLs")
    building_id: Optional[int] = Field(None, description="Building ID (optional, null for global common areas)")


class UpdateIncidentSchema(BaseModel):
    category: Optional[str] = Field(None, description="Category")
    priority: Optional[str] = Field(None, description="Priority")
    status: Optional[str] = Field(None, description="Status: pending, open, in_progress, resolved, closed, cancelled")
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = Field(None, min_length=10)
    photos: Optional[List[str]] = Field(None)
    internal_notes: Optional[str] = Field(None)
    resolution_notes: Optional[str] = Field(None)
    assigned_to_user_id: Optional[int] = Field(None)
    scheduled_date: Optional[date] = Field(None)
    completed_date: Optional[date] = Field(None)
