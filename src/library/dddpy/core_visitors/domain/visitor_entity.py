"""Visitor domain entity — DDD for visitor / access management."""
from typing import Optional
from datetime import datetime, date, time
from typing import Dict, Any, Optional


class VisitorStatus:
    PENDING = "pending"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    ALL = {PENDING, CHECKED_IN, CHECKED_OUT, CANCELLED, NO_SHOW}


class VisitPurpose:
    FAMILY = "family"
    DELIVERY = "delivery"
    SERVICE = "service"
    MAINTENANCE = "maintenance"
    OTHER = "other"
    ALL = {FAMILY, DELIVERY, SERVICE, MAINTENANCE, OTHER}


class VisitorEntity:
    """
    Entidad de dominio para visitantes / invitados del condominio.
    """

    VALID_STATUSES = VisitorStatus.ALL
    VALID_PURPOSES = VisitPurpose.ALL

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        building_id: Optional[int],
        unit_id: int,
        host_user_id: int,
        visitor_name: str,
        visitor_document_type: Optional[str] = None,
        visitor_document_number: Optional[str] = None,
        visitor_phone: Optional[str] = None,
        expected_date: date = None,
        expected_time: time = None,
        actual_checkin_at: Optional[datetime] = None,
        actual_checkout_at: Optional[datetime] = None,
        status: str = VisitorStatus.PENDING,
        visit_purpose: str = VisitPurpose.OTHER,
        access_code: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enrichment fields
        host_user_full_name: Optional[str] = None,
        unit_code: Optional[str] = None,
        building_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.building_id = building_id
        self.unit_id = unit_id
        self.host_user_id = host_user_id
        self.visitor_name = visitor_name
        self.visitor_document_type = visitor_document_type
        self.visitor_document_number = visitor_document_number
        self.visitor_phone = visitor_phone
        self.expected_date = expected_date
        self.expected_time = expected_time
        self.actual_checkin_at = actual_checkin_at
        self.actual_checkout_at = actual_checkout_at
        self.status = status
        self.visit_purpose = visit_purpose
        self.access_code = access_code
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.host_user_full_name = host_user_full_name
        self.unit_code = unit_code
        self.building_name = building_name
        self.condominium_name = condominium_name

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.status not in self.VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )
        if self.visit_purpose not in self.VALID_PURPOSES:
            raise ValueError(
                f"visit_purpose must be one of: {', '.join(sorted(self.VALID_PURPOSES))}"
            )
        # VIS-04: can only be checked_out if already checked_in
        if self.status == VisitorStatus.CHECKED_OUT and self.actual_checkin_at is None:
            raise ValueError(
                "Cannot check out a visitor that has not checked in"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "building_id": self.building_id,
            "unit_id": self.unit_id,
            "host_user_id": self.host_user_id,
            "visitor_name": self.visitor_name,
            "visitor_document_type": self.visitor_document_type,
            "visitor_document_number": self.visitor_document_number,
            "visitor_phone": self.visitor_phone,
            "expected_date": self.expected_date.isoformat() if self.expected_date else None,
            "expected_time": self.expected_time.isoformat() if self.expected_time else None,
            "actual_checkin_at": self.actual_checkin_at.isoformat() if self.actual_checkin_at else None,
            "actual_checkout_at": self.actual_checkout_at.isoformat() if self.actual_checkout_at else None,
            "status": self.status,
            "visit_purpose": self.visit_purpose,
            "access_code": self.access_code,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            # Enrichment
            "host_user_full_name": self.host_user_full_name,
            "unit_code": self.unit_code,
            "building_name": self.building_name,
            "condominium_name": self.condominium_name,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.deleted_at is None

    def is_pending(self) -> bool:
        return self.status == VisitorStatus.PENDING and not self.is_deleted()

    def is_checked_in(self) -> bool:
        return self.status == VisitorStatus.CHECKED_IN

    def is_checked_out(self) -> bool:
        return self.status == VisitorStatus.CHECKED_OUT