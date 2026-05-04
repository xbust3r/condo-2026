"""
AmenityUsageUseCase — operational usage tracking for amenity bookings (B8).

Handles:
- check_in: record start of amenity usage
- check_out: record end of amenity usage
- mark_no_show: record booking no-show
- get_booking_usage: retrieve usage timeline for a booking

Rules:
- CHECK_IN requires booking status = 'confirmed'
- CHECK_OUT requires prior CHECK_IN without CHECK_OUT
- NO_SHOW excludes CHECK_IN for the same booking
- No usage logging for cancelled bookings
"""
import uuid as uuid_lib
from datetime import datetime
from typing import Optional, List, Dict, Any

from library.dddpy.core_amenity_bookings.infrastructure.dbusage_log import DBUsageLog
from library.dddpy.core_amenity_bookings.domain.usage_log_entity import UsageLogEntity
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger

logger = Logger("AmenityUsageUseCase")


class AmenityUsageUseCase:
    """Manages operational check-in/check-out lifecycle for booked amenities."""

    # ── check_in ────────────────────────────────────────────────────

    def check_in(
        self,
        booking_id: int,
        recorded_by: Optional[int] = None,
        notes: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Record a check-in event for a confirmed booking."""
        with session_scope() as session:
            self._validate_booking_for_check_in(session, booking_id)
            self._ensure_no_active_check_in(session, booking_id)

            log = DBUsageLog(
                uuid=str(uuid_lib.uuid4()),
                booking_id=booking_id,
                amenity_id=self._resolve_amenity_id(session, booking_id),
                condominium_id=self._resolve_condominium_id(session, booking_id),
                unit_id=self._resolve_unit_id(session, booking_id),
                owner_id=self._resolve_owner_id(session, booking_id),
                event_type='CHECK_IN',
                event_at=datetime.utcnow(),
                recorded_by=recorded_by,
                source='resident_app' if recorded_by else 'admin_panel',
                notes=notes,
                event_context_json=context,
                created_at=datetime.utcnow(),
            )
            session.add(log)
            session.flush()
            result = log.to_dict()
            logger.info(f"CHECK_IN recorded booking_id={booking_id} log_id={log.id}")
            return result

    # ── check_out ───────────────────────────────────────────────────

    def check_out(
        self,
        booking_id: int,
        recorded_by: Optional[int] = None,
        notes: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Record a check-out event. Requires prior CHECK_IN without CHECK_OUT."""
        with session_scope() as session:
            self._ensure_check_in_exists(session, booking_id)
            self._ensure_no_existing_check_out(session, booking_id)

            log = DBUsageLog(
                uuid=str(uuid_lib.uuid4()),
                booking_id=booking_id,
                amenity_id=self._resolve_amenity_id(session, booking_id),
                condominium_id=self._resolve_condominium_id(session, booking_id),
                unit_id=self._resolve_unit_id(session, booking_id),
                owner_id=self._resolve_owner_id(session, booking_id),
                event_type='CHECK_OUT',
                event_at=datetime.utcnow(),
                recorded_by=recorded_by,
                source='resident_app' if recorded_by else 'admin_panel',
                notes=notes,
                event_context_json=context,
                created_at=datetime.utcnow(),
            )
            session.add(log)
            session.flush()
            result = log.to_dict()
            logger.info(f"CHECK_OUT recorded booking_id={booking_id} log_id={log.id}")
            return result

    # ── mark_no_show ────────────────────────────────────────────────

    def mark_no_show(
        self,
        booking_id: int,
        recorded_by: Optional[int] = None,
        notes: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Mark a booking as no-show. Must not have an active CHECK_IN."""
        with session_scope() as session:
            self._validate_booking_for_no_show(session, booking_id)

            log = DBUsageLog(
                uuid=str(uuid_lib.uuid4()),
                booking_id=booking_id,
                amenity_id=self._resolve_amenity_id(session, booking_id),
                condominium_id=self._resolve_condominium_id(session, booking_id),
                unit_id=self._resolve_unit_id(session, booking_id),
                owner_id=self._resolve_owner_id(session, booking_id),
                event_type='NO_SHOW',
                event_at=datetime.utcnow(),
                recorded_by=recorded_by,
                source='admin_panel',
                notes=notes,
                event_context_json=context,
                created_at=datetime.utcnow(),
            )
            session.add(log)
            session.flush()
            result = log.to_dict()
            logger.info(f"NO_SHOW recorded booking_id={booking_id} log_id={log.id}")
            return result

    # ── get_booking_usage ───────────────────────────────────────────

    def get_booking_usage(self, booking_id: int) -> List[Dict[str, Any]]:
        """Retrieve all usage events for a booking in chronological order."""
        with session_scope() as session:
            from sqlalchemy import text as sa_text
            rows = session.execute(
                sa_text(
                    "SELECT * FROM core_amenity_usage_logs "
                    "WHERE booking_id = :bid ORDER BY event_at ASC"
                ),
                {'bid': booking_id},
            ).fetchall()
            return [dict(r._mapping) for r in rows]

    # ── Helpers ─────────────────────────────────────────────────────

    def _validate_booking_for_check_in(self, session, booking_id: int) -> None:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text("SELECT status FROM core_amenity_bookings WHERE id = :bid"),
            {'bid': booking_id},
        ).first()
        if not row:
            raise ValueError(f"Booking {booking_id} not found")
        status = row[0] if isinstance(row, tuple) else row.status
        if status != 'confirmed':
            raise ValueError(f"Cannot check-in: booking {booking_id} is {status}, must be confirmed")

    def _ensure_no_active_check_in(self, session, booking_id: int) -> None:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text(
                "SELECT COUNT(*) FROM core_amenity_usage_logs "
                "WHERE booking_id = :bid AND event_type = 'CHECK_IN'"
            ),
            {'bid': booking_id},
        ).first()
        count = row[0]
        if count > 0:
            raise ValueError(f"Booking {booking_id} already has an active CHECK_IN")

    def _ensure_check_in_exists(self, session, booking_id: int) -> None:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text(
                "SELECT COUNT(*) FROM core_amenity_usage_logs "
                "WHERE booking_id = :bid AND event_type = 'CHECK_IN'"
            ),
            {'bid': booking_id},
        ).first()
        if row[0] == 0:
            raise ValueError(f"Cannot check-out: no CHECK_IN found for booking {booking_id}")

    def _ensure_no_existing_check_out(self, session, booking_id: int) -> None:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text(
                "SELECT COUNT(*) FROM core_amenity_usage_logs "
                "WHERE booking_id = :bid AND event_type = 'CHECK_OUT'"
            ),
            {'bid': booking_id},
        ).first()
        if row[0] > 0:
            raise ValueError(f"Booking {booking_id} already has a CHECK_OUT")

    def _validate_booking_for_no_show(self, session, booking_id: int) -> None:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text("SELECT status FROM core_amenity_bookings WHERE id = :bid"),
            {'bid': booking_id},
        ).first()
        if not row:
            raise ValueError(f"Booking {booking_id} not found")
        status = row[0] if isinstance(row, tuple) else row.status
        if status not in ('confirmed',):
            raise ValueError(f"Cannot mark no-show: booking {booking_id} is {status}")
        # Must not already have CHECK_IN
        ci = session.execute(
            sa_text(
                "SELECT COUNT(*) FROM core_amenity_usage_logs "
                "WHERE booking_id = :bid AND event_type = 'CHECK_IN'"
            ),
            {'bid': booking_id},
        ).first()
        if ci[0] > 0:
            raise ValueError(f"Cannot mark no-show: booking {booking_id} already has CHECK_IN")

    def _resolve_amenity_id(self, session, booking_id: int) -> int:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text("SELECT amenity_id FROM core_amenity_bookings WHERE id = :bid"),
            {'bid': booking_id},
        ).first()
        return row[0] if row else 0

    def _resolve_condominium_id(self, session, booking_id: int) -> int:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text("SELECT condominium_id FROM core_amenity_bookings WHERE id = :bid"),
            {'bid': booking_id},
        ).first()
        return row[0] if row else 0

    def _resolve_unit_id(self, session, booking_id: int) -> Optional[int]:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text("SELECT unit_id FROM core_amenity_bookings WHERE id = :bid"),
            {'bid': booking_id},
        ).first()
        return row[0] if row else None

    def _resolve_owner_id(self, session, booking_id: int) -> Optional[int]:
        from sqlalchemy import text as sa_text
        row = session.execute(
            sa_text("SELECT owner_id FROM core_amenity_bookings WHERE id = :bid"),
            {'bid': booking_id},
        ).first()
        return row[0] if row else None
