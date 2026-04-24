"""
Audit command schema — for AuditFactory internal use.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CreateAuditLogSchema(BaseModel):
    user_id: int = Field(..., description="User who performed the action")
    action: str = Field(..., description="Action: create, update, delete, restore")
    resource_type: str = Field(..., description="Module name: charge, payment, announcement, etc.")
    resource_id: int = Field(..., description="ID of the affected resource")
    resource_uuid: str = Field(..., description="UUID of the affected resource")
    old_values: Optional[Dict[str, Any]] = Field(None, description="Previous state (for updates/deletes)")
    new_values: Optional[Dict[str, Any]] = Field(None, description="New state (for creates/updates)")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")