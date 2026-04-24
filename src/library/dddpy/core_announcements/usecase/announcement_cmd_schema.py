"""
from typing import Optional
Announcement command schemas — Pydantic input models.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateAnnouncementSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    author_user_id: int = Field(..., description="Author user ID")
    title: str = Field(..., min_length=3, max_length=200, description="Title (min 3 chars)")
    content: str = Field(..., min_length=10, description="Content (min 10 chars)")
    category: str = Field('info', description="Category: info, warning, urgent, event")
    visibility: str = Field('public', description="Visibility: public, owners_only, residents_only")
    is_pinned: bool = Field(False, description="Pin this announcement")
    published_at: Optional[datetime] = Field(None, description="Publication date (null = immediately)")
    expires_at: Optional[datetime] = Field(None, description="Expiration date (null = never)")


class UpdateAnnouncementSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    category: Optional[str] = Field(None)
    visibility: Optional[str] = Field(None)
    is_pinned: Optional[bool] = Field(None)
    published_at: Optional[datetime] = Field(None)
    expires_at: Optional[datetime] = Field(None)
