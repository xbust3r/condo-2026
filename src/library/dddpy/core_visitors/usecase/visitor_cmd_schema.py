"""Visitor command schemas — Pydantic input models."""
from typing import Optional
from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field


class CreateVisitorSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    unit_id: int = Field(..., description="Unit ID receiving the visit")
    visitor_name: str = Field(..., min_length=1, max_length=150, description="Visitor full name")
    visitor_phone: Optional[str] = Field(None, max_length=30, description="Visitor phone number")
    visitor_document_type: Optional[str] = Field(None, max_length=20, description="Document type: CI, Passport, etc.")
    visitor_document_number: Optional[str] = Field(None, max_length=50, description="Document number")
    expected_date: date = Field(..., description="Expected visit date")
    expected_time: time = Field(..., description="Expected visit time")
    visit_purpose: str = Field('other', description="Purpose: family, delivery, service, maintenance, other")
    notes: Optional[str] = Field(None, description="Additional notes")
    building_id: Optional[int] = Field(None, description="Building ID (optional, null for global)")


class UpdateVisitorSchema(BaseModel):
    expected_time: Optional[time] = Field(None, description="Updated expected time")
    notes: Optional[str] = Field(None, description="Updated notes")
    visit_purpose: Optional[str] = Field(None, description="Updated purpose")