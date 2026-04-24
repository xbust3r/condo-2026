"""
from typing import Optional
Resident use case schemas.
"""
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class UpdatePreferencesSchema(BaseModel):
    notify_announcements: Optional[bool] = Field(None)
    notify_incidents: Optional[bool] = Field(None)
    notify_packages: Optional[bool] = Field(None)
    notify_visitors: Optional[bool] = Field(None)
    notify_payments: Optional[bool] = Field(None)
    language: Optional[str] = Field(None, max_length=10)
    theme: Optional[str] = Field(None, max_length=20)
    default_building_id: Optional[int] = Field(None)
    notes: Optional[str] = Field(None)
