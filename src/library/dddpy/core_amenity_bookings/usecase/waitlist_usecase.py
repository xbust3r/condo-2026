"""
Waitlist Use Case — lifecycle: create, promote, expire (B6).

Handles:
- Inserting into waitlist when slot capacity is exceeded
- Promoting the top-priority entry to a confirmed booking
- Expiring entries past their deadline
"""
import uuid as uuid_lib
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any

from sqlalchemy import text

from library.dddpy.core_amenity_bookings.infrastructure.dbwaitlist import DBWaitlistEntry
from library.dddpy.core_amenity_bookings.usecase.priority_engine import (
    PriorityEngine, WaitlistEntryScore,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("WaitlistUseCase")


class WaitlistUseCase:
    """Manages waitlist lifecycle and promotion to bookings."""

    def __init__(self):
        self._priority_engine = PriorityEngine()

    # ── Create ───────────────────────────────────────────────────────

    def create_entry(
        self,
        amenity_id: int,
        unit_id: int,
        user_id: int,
        booking_date: date,
        requested_start_at: datetime,
        requested_end_at: datetime,
        guest_count: int = 1,
        idempotency_key: Optional[str] = None,
        policy_snapshot: Optional[Dict] = None,
        notes: Optional[str] = None,
        expires_at: Optional[datetime] = None,
    ) -> int:
        """Insert a new waitlist entry. Returns the new entry id."""
        logger.add_inside_method("create_entry")

        with session_scope() as session:
            # Idempotency check
            if idempotency_key:
                existing = session.query(DBWaitlistEntry).filter(
                    DBWaitlistEntry.idempotency_key == idempotency_key,
                ).first()
                if existing:
                    return existing.id

            entry = DBWaitlistEntry(
                uuid=str(uuid_lib.uuid4()),
                amenity_id=amenity_id,
                unit_id=unit_id,
                user_id=user_id,
                booking_date=booking_date,
                requested_start_at=requested_start_at,
                requested_end_at=requested_end_at,
                guest_count=guest_count,
                status='WAITING',
                idempotency_key=idempotency_key,
                effective_policy_snapshot_json=policy_snapshot,
                notes=notes,
                expires_at=expires_at,
                created_at=datetime.utcnow(),
            )
            session.add(entry)
            session.flush()
            entry_id = entry.id

        return entry_id

    # ── Read ─────────────────────────────────────────────────────────

    def get_waiting_entries(
        self, amenity_id: int, booking_date: date, limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Get all WAITING entries for an amenity on a date, sorted by created_at."""
        with session_scope() as session:
            rows = session.query(DBWaitlistEntry).filter(
                DBWaitlistEntry.amenity_id == amenity_id,
                DBWaitlistEntry.booking_date == booking_date,
                DBWaitlistEntry.status == 'WAITING',
            ).order_by(DBWaitlistEntry.created_at.asc()).limit(limit).all()
            return [
                {
                    'id': r.id,
                    'user_id': r.user_id,
                    'unit_id': r.unit_id,
                    'amenity_id': r.amenity_id,
                    'guest_count': r.guest_count,
                    'requested_start_at': r.requested_start_at,
                    'requested_end_at': r.requested_end_at,
                    'created_at': r.created_at,
                    'booking_date': r.booking_date,
                }
                for r in rows
            ]

    def get_entry(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Get a single waitlist entry by id."""
        with session_scope() as session:
            row = session.get(DBWaitlistEntry, entry_id)
            if row:
                return row.to_dict()
            return None

    # ── Promote ──────────────────────────────────────────────────────

    def promote(
        self,
        amenity_id: int,
        booking_date: date,
        priority_policy: str = 'fifo',
        condominium_id: Optional[int] = None,
        amenity_type: Optional[str] = None,
        evaluation_window_days: int = 30,
        waitlist_mode: str = 'auto_confirm',
    ) -> Optional[Dict[str, Any]]:
        """
        Promote the top-priority waiting entry according to waitlist_mode.

        waitlist_mode determines what happens:
        - auto_confirm: winner → convert to booking immediately
        - notify_and_confirm: winner → NOTIFIED (waits for user confirmation)
        - admin_review: winner → status unchanged (admin reviews later)

        Returns the promotion result dict, or None if no eligible entries.
        """
        logger.add_inside_method("promote")

        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        from library.dddpy.core_amenity_bookings.usecase.policy_resolver import get_policy_resolver

        # 1. Get waiting entries
        entries = self.get_waiting_entries(amenity_id, booking_date)
        if not entries:
            return None

        # 2. Resolve effective policy for scoring context
        if condominium_id is None:
            condominium_id = self._resolve_condominium_id(amenity_id)

        # 3. Score and pick winner
        with session_scope() as session:
            scored = self._priority_engine.score_entries(
                session=session,
                entries=entries,
                priority_policy=priority_policy,
                condominium_id=condominium_id,
                amenity_type=amenity_type,
                evaluation_window_days=evaluation_window_days,
            )

        if not scored:
            return None

        winner = scored[0]

        # 4. Look up winner entry data (raw SQL — avoid ORM detach)
        booking_uc = BookingUseCase()
        entry_data = None
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT unit_id, user_id, booking_date,
                           requested_start_at, requested_end_at, guest_count
                    FROM core_amenity_waitlist WHERE id = :id
                """),
                {'id': winner.entry_id},
            ).fetchone()
            if row:
                entry_data = {
                    'unit_id': int(row[0]),
                    'user_id': int(row[1]),
                    'booking_date': row[2],
                    'requested_start_at': row[3],
                    'requested_end_at': row[4],
                    'guest_count': int(row[5]),
                }
        if not entry_data:
            return None

        # 5. Apply waitlist_mode to determine action
        booking_id = None
        with session_scope() as session:
            row = session.get(DBWaitlistEntry, winner.entry_id)
            if not row:
                return None

            if waitlist_mode == 'auto_confirm':
                # Create booking NOW, then mark CONVERTED
                try:
                    result = booking_uc.create(
                        condominium_id=condominium_id,
                        building_id=self._resolve_building_id(amenity_id),
                        amenity_id=amenity_id,
                        unit_id=entry_data['unit_id'],
                        owner_id=entry_data['user_id'],
                        booking_date=entry_data['booking_date'],
                        start_at=entry_data['requested_start_at'],
                        end_at=entry_data['requested_end_at'],
                        guest_count=entry_data['guest_count'],
                        allocation_source='WAITLIST_PROMOTION',
                    )
                    booking_id = result.data['id']
                except Exception as e:
                    import traceback
                    logger.error(f"auto_confirm booking creation failed: {e}")
                    logger.error(traceback.format_exc())
                    raise

                row.status = 'CONVERTED'
                row.converted_booking_id = booking_id
                row.priority_score_snapshot = winner.score
                row.priority_reason_json = {
                    'policy': priority_policy,
                    'reason': winner.reason,
                }
                row.updated_at = datetime.utcnow()
                session.flush()
                session.refresh(row)
                entry_dict = row.to_dict()

                # B7: Allocation audit — waitlist promoted
                self._audit_record(
                    amenity_id=amenity_id,
                    decision_type='WAITLIST_PROMOTED',
                    decision_reason=f"{priority_policy}, score={winner.score:.2f}",
                    booking_id=booking_id,
                    waitlist_entry_id=winner.entry_id,
                    context={
                        'policy': priority_policy,
                        'reason': winner.reason,
                        'waitlist_mode': waitlist_mode,
                    },
                )

            elif waitlist_mode == 'notify_and_confirm':
                # Do NOT create booking yet — just notify, user confirms later
                row.status = 'NOTIFIED'
                row.notified_at = datetime.utcnow()
                row.priority_score_snapshot = winner.score
                row.priority_reason_json = {
                    'policy': priority_policy,
                    'reason': winner.reason,
                }
                if not row.expires_at:
                    row.expires_at = datetime.utcnow() + timedelta(hours=24)
                row.updated_at = datetime.utcnow()
                session.flush()
                session.refresh(row)
                entry_dict = row.to_dict()

                # B7: Allocation audit — waitlist notified
                self._audit_record(
                    amenity_id=amenity_id,
                    decision_type='WAITLIST_NOTIFIED',
                    decision_reason=f"{priority_policy}, score={winner.score:.2f}",
                    waitlist_entry_id=winner.entry_id,
                    context={
                        'policy': priority_policy,
                        'reason': winner.reason,
                        'waitlist_mode': waitlist_mode,
                        'expires_at': row.expires_at.isoformat() if row.expires_at else None,
                    },
                )

            elif waitlist_mode == 'admin_review':
                # Do NOT create booking — admin reviews later
                # Annotate score for auditability
                row.priority_score_snapshot = winner.score
                row.priority_reason_json = {
                    'policy': priority_policy,
                    'reason': winner.reason,
                }
                row.updated_at = datetime.utcnow()
                session.flush()
                session.refresh(row)
                entry_dict = row.to_dict()

            else:
                return None

        return {
            'waitlist_entry': entry_dict,
            'booking_id': booking_id,
            'waitlist_mode': waitlist_mode,
            'priority_score': winner.score,
            'priority_reason': winner.reason,
            'scored_entries': len(scored),
        }

    # ── Expire ───────────────────────────────────────────────────────

    def expire_overdue(self) -> int:
        """Expire all WAITING entries past their expires_at."""
        with session_scope() as session:
            result = session.execute(
                text("""
                    UPDATE core_amenity_waitlist
                    SET status = 'EXPIRED', updated_at = NOW()
                    WHERE status = 'WAITING'
                      AND expires_at IS NOT NULL
                      AND expires_at < NOW()
                """),
            )
            count = result.rowcount
            if count:
                logger.info(f"Expired {count} overdue waitlist entries")
            return count

    # ── Confirm (notify_and_confirm flow) ────────────────────────────

    def confirm_entry(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """
        Called when a user confirms their NOTIFIED waitlist entry.
        Converts it to CONFIRMED, then triggers promotion to booking.
        """
        logger.add_inside_method("confirm_entry")
        with session_scope() as session:
            row = session.get(DBWaitlistEntry, entry_id)
            if not row or row.status != 'NOTIFIED':
                return None

            from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase

            booking_uc = BookingUseCase()
            condominium_id = self._resolve_condominium_id(row.amenity_id)
            building_id = self._resolve_building_id(row.amenity_id)

            try:
                result = booking_uc.create(
                    condominium_id=condominium_id,
                    building_id=building_id,
                    amenity_id=row.amenity_id,
                    unit_id=row.unit_id,
                    owner_id=row.user_id,
                    booking_date=row.booking_date,
                    start_at=row.requested_start_at,
                    end_at=row.requested_end_at,
                    guest_count=row.guest_count,
                    allocation_source='WAITLIST_PROMOTION',
                )
                booking_id = result.data['id']
            except Exception as e:
                import traceback
                logger.error(f"Confirm entry booking creation failed: {e}")
                logger.error(traceback.format_exc())
                raise

            row.status = 'CONVERTED'
            row.converted_booking_id = booking_id
            row.updated_at = datetime.utcnow()
            session.flush()
            session.refresh(row)
            entry_dict = row.to_dict()

            # B7: Allocation audit — waitlist confirmed
            from library.dddpy.core_amenity_bookings.usecase.allocation_audit_usecase import AllocationAuditUseCase
            audit_uc = AllocationAuditUseCase()
            audit_uc.record(
                amenity_id=row.amenity_id,
                decision_type='WAITLIST_CONFIRMED',
                decision_reason='User confirmed after notification',
                booking_id=booking_id,
                waitlist_entry_id=entry_id,
            )

        return {
            'waitlist_entry': entry_dict,
            'booking_id': booking_id,
        }

    # ── Helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _resolve_condominium_id(amenity_id: int) -> int:
        """Resolve condominium_id from amenity."""
        with session_scope() as session:
            row = session.execute(
                text("SELECT condominium_id FROM core_amenities WHERE id = :id"),
                {'id': amenity_id},
            ).fetchone()
            return int(row[0]) if row else 0

    @staticmethod
    def _resolve_building_id(amenity_id: int) -> int:
        """Resolve building_id from amenity."""
        with session_scope() as session:
            row = session.execute(
                text("SELECT building_id FROM core_amenities WHERE id = :id"),
                {'id': amenity_id},
            ).fetchone()
            return int(row[0]) if row and row[0] else 1

    @staticmethod
    def _audit_record(
        *,
        amenity_id: int,
        decision_type: str,
        decision_reason: str,
        booking_id: Optional[int] = None,
        waitlist_entry_id: Optional[int] = None,
        context: Optional[dict] = None,
    ):
        """B7: Write allocation audit entry."""
        from library.dddpy.core_amenity_bookings.usecase.allocation_audit_usecase import AllocationAuditUseCase
        try:
            AllocationAuditUseCase().record(
                amenity_id=amenity_id,
                decision_type=decision_type,
                decision_reason=decision_reason,
                booking_id=booking_id,
                waitlist_entry_id=waitlist_entry_id,
                context=context,
            )
        except Exception:
            logger.exception("Failed to write allocation audit")
