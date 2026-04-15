from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class CreateCondominiumRoleData:
    """Data required to create a new condominium role assignment."""
    condominium_id: int
    user_id: int
    role: str
    status: str = "active"
    start_date: Optional[date] = None
    end_date: Optional[date] = None


@dataclass(frozen=True)
class UpdateCondominiumRoleData:
    """Data required to update an existing condominium role assignment."""
    role: Optional[str] = None
    status: Optional[str] = None
    end_date: Optional[date] = None
