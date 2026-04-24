"""
Notification command schemas — Pydantic input models.
"""
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class CreateNotificationSchema(BaseModel):
    user_id: int = Field(..., description="Target user ID for the notification")
    channel: str = Field('in_app', description="Channel: in_app, email")
    type: str = Field(..., description="Notification type")
    resource_type: str = Field(..., description="Resource type: announcement, incident, payment, receipt")
    resource_id: int = Field(..., description="Related resource ID")
    title: str = Field(..., min_length=1, max_length=200, description="Notification title")
    body: Optional[str] = Field(None, description="Notification body text")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata as JSON")


class UpdateNotificationSchema(BaseModel):
    is_read: Optional[bool] = Field(None, description="Mark notification as read/unread")