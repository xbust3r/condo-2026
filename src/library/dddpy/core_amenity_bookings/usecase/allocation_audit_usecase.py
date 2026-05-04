"""
AllocationAuditUseCase — writes allocation audit trail entries.

Invoked by booking_usecase and waitlist_usecase at key decision points:
- BOOKING_ACCEPTED / BOOKING_REJECTED
- WAITLIST_INSERTED / WAITLIST_PROMOTED / WAITLIST_CONFIRMED
- BOOKING_CANCELLED
"""
import json
import logging
from datetime import datetime
from typing import Optional

from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.core_amenity_bookings.infrastructure.dballocation_audit import DBAllocationAudit

logger = logging.getLogger(__name__)

VALID_DECISION_TYPES = frozenset({
    'BOOKING_ACCEPTED',
    'BOOKING_REJECTED',
    'WAITLIST_INSERTED',
    'WAITLIST_PROMOTED',
    'WAITLIST_CONFIRMED',
    'WAITLIST_NOTIFIED',
    'BOOKING_CANCELLED',
    'WAITLIST_EXPIRED',
})


class AllocationAuditUseCase:
    """Write allocation audit trail entries."""

    def record(
        self,
        *,
        amenity_id: int,
        decision_type: str,
        decision_reason: Optional[str] = None,
        booking_id: Optional[int] = None,
        waitlist_entry_id: Optional[int] = None,
        context: Optional[dict] = None,
    ) -> int:
        if decision_type not in VALID_DECISION_TYPES:
            raise ValueError(f"Unknown decision_type={decision_type}")

        with session_scope() as session:
            entry = DBAllocationAudit(
                amenity_id=amenity_id,
                booking_id=booking_id,
                waitlist_entry_id=waitlist_entry_id,
                decision_type=decision_type,
                decision_reason=decision_reason or '',
                decision_context_json=context,
                created_at=datetime.utcnow(),
            )
            session.add(entry)
            session.flush()
            audit_id = entry.id
            logger.debug(
                "AllocationAudit #%d: %s amenity=%d booking=%d wl=%d",
                audit_id, decision_type, amenity_id,
                booking_id or 0, waitlist_entry_id or 0,
            )
            return audit_id
