"""
Incident domain entity — DDD for maintenance ticketing / incident reports.
"""
from datetime import datetime, date
from typing import Dict, Any, Optional


# ── Enums as plain Python sets ───────────────────────────────────────────────

class IncidentStatus:
    PENDING = "pending"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"

    ALL = {PENDING, OPEN, IN_PROGRESS, RESOLVED, CLOSED, CANCELLED}


class IncidentPriority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

    ALL = {LOW, MEDIUM, HIGH, URGENT}
    DEFAULT = MEDIUM


class IncidentCategory:
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    STRUCTURAL = "structural"
    COMMON_AREAS = "common_areas"
    ELEVATOR = "elevator"
    PAINTING = "painting"
    CLEANING = "cleaning"
    PEST_CONTROL = "pest_control"
    SECURITY = "security"
    OTHER = "other"

    ALL = {
        PLUMBING, ELECTRICAL, STRUCTURAL, COMMON_AREAS,
        ELEVATOR, PAINTING, CLEANING, PEST_CONTROL, SECURITY, OTHER,
    }


class IncidentEntity:
    """
    Entidad de dominio para incidencias / tickets de mantenimiento.
    """

    VALID_STATUSES = IncidentStatus.ALL
    VALID_PRIORITIES = IncidentPriority.ALL
    VALID_CATEGORIES = IncidentCategory.ALL

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        building_id: Optional[int],
        unit_id: int,
        reported_by_user_id: int,
        assigned_to_user_id: Optional[int],
        category: str,
        priority: str,
        status: str,
        title: str,
        description: str,
        photos: Optional[list] = None,
        internal_notes: Optional[str] = None,
        resolution_notes: Optional[str] = None,
        scheduled_date: Optional[date] = None,
        completed_date: Optional[date] = None,
        is_escalated: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enrichment fields
        unit_code: Optional[str] = None,
        building_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
        reported_by_user_full_name: Optional[str] = None,
        assigned_to_user_full_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.building_id = building_id
        self.unit_id = unit_id
        self.reported_by_user_id = reported_by_user_id
        self.assigned_to_user_id = assigned_to_user_id
        self.category = category
        self.priority = priority
        self.status = status
        self.title = title
        self.description = description
        self.photos = photos or []
        self.internal_notes = internal_notes
        self.resolution_notes = resolution_notes
        self.scheduled_date = scheduled_date
        self.completed_date = completed_date
        self.is_escalated = is_escalated
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.unit_code = unit_code
        self.building_name = building_name
        self.condominium_name = condominium_name
        self.reported_by_user_full_name = reported_by_user_full_name
        self.assigned_to_user_full_name = assigned_to_user_full_name

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.category not in self.VALID_CATEGORIES:
            raise ValueError(
                f"category must be one of: {', '.join(sorted(self.VALID_CATEGORIES))}"
            )
        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError(
                f"priority must be one of: {', '.join(sorted(self.VALID_PRIORITIES))}"
            )
        if self.status not in self.VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )
        # INC-04: can only close if completed_date is set
        if self.status == IncidentStatus.CLOSED and self.completed_date is None:
            raise ValueError(
                "Cannot close an incident without a completed_date"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "building_id": self.building_id,
            "unit_id": self.unit_id,
            "reported_by_user_id": self.reported_by_user_id,
            "assigned_to_user_id": self.assigned_to_user_id,
            "category": self.category,
            "priority": self.priority,
            "status": self.status,
            "title": self.title,
            "description": self.description,
            "photos": self.photos,
            "internal_notes": self.internal_notes,
            "resolution_notes": self.resolution_notes,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None,
            "is_escalated": self.is_escalated,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            # Enrichment
            "unit_code": self.unit_code,
            "building_name": self.building_name,
            "condominium_name": self.condominium_name,
            "reported_by_user_full_name": self.reported_by_user_full_name,
            "assigned_to_user_full_name": self.assigned_to_user_full_name,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None
