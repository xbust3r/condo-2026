"""
Priority engine for waitlist promotion (B6).

Strategies:
- fifo: first-in-first-out, score = -created_at (earlier = higher)
- less_usage_first: fewer bookings in evaluation window gets priority
- equal_share: round-robin by user usage count
"""
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import text


class WaitlistEntryScore:
    """Lightweight representation of a waitlist entry with its computed score."""

    def __init__(
        self,
        entry_id: int,
        user_id: int,
        unit_id: int,
        amenity_id: int,
        score: float,
        reason: str,
    ):
        self.entry_id = entry_id
        self.user_id = user_id
        self.unit_id = unit_id
        self.amenity_id = amenity_id
        self.score = score
        self.reason = reason


class PriorityEngine:
    """
    Stateless engine that scores waitlist entries for promotion.

    All strategies accept a session to run queries scoped to the current transaction.
    """

    # ── FIFO ─────────────────────────────────────────────────────────

    @staticmethod
    def score_fifo(entry_created_at: datetime) -> float:
        """
        Earlier entries get higher score.
        Score = -timestamp / 1_000_000 to fit in standard precision.
        """
        return -(entry_created_at.timestamp() / 1_000_000.0)

    @staticmethod
    def fifo_reason(entry_created_at: datetime) -> str:
        return f"fifo: created_at={entry_created_at.isoformat()}"

    # ── LESS_USAGE_FIRST ─────────────────────────────────────────────

    @staticmethod
    def score_less_usage_first(
        session,
        user_id: int,
        condominium_id: int,
        amenity_type: Optional[str] = None,
        window_days: int = 30,
    ) -> float:
        """
        Fewer bookings in window = higher score.

        Score = window_days - booking_count (so 0 bookings = max score).

        If amenity_type is provided, only counts bookings for that type
        (scoped to AMENITY_TYPE level). Otherwise counts all amenity bookings.
        """
        window_start = datetime.utcnow() - timedelta(days=window_days)
        params = {
            'user_id': user_id,
            'condominium_id': condominium_id,
            'window_start': window_start,
        }
        if amenity_type:
            rows = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_amenity_bookings b
                    JOIN core_amenities a ON a.id = b.amenity_id
                    WHERE b.owner_id = :user_id
                      AND b.condominium_id = :condominium_id
                      AND b.status IN ('confirmed', 'completed')
                      AND b.deleted_at IS NULL
                      AND b.created_at >= :window_start
                      AND a.amenity_type = :amenity_type
                """),
                {**params, 'amenity_type': amenity_type},
            ).fetchone()
        else:
            rows = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_amenity_bookings
                    WHERE owner_id = :user_id
                      AND condominium_id = :condominium_id
                      AND status IN ('confirmed', 'completed')
                      AND deleted_at IS NULL
                      AND created_at >= :window_start
                """),
                params,
            ).fetchone()

        count = int(rows[0]) if rows and rows[0] else 0
        return float(window_days - count)

    @staticmethod
    def less_usage_reason(booking_count: int, window_days: int) -> str:
        return f"less_usage_first: {booking_count} bookings in last {window_days}d"

    # ── EQUAL_SHARE ──────────────────────────────────────────────────

    @staticmethod
    def score_equal_share(
        session,
        user_id: int,
        condominium_id: int,
        amenity_type: Optional[str] = None,
    ) -> float:
        """
        Users with fewer total bookings get higher score.

        Score = 1 / (1 + total_bookings) — decays naturally.
        """
        params = {
            'user_id': user_id,
            'condominium_id': condominium_id,
        }
        if amenity_type:
            rows = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_amenity_bookings b
                    JOIN core_amenities a ON a.id = b.amenity_id
                    WHERE b.owner_id = :user_id
                      AND b.condominium_id = :condominium_id
                      AND b.status IN ('confirmed', 'completed')
                      AND b.deleted_at IS NULL
                      AND a.amenity_type = :amenity_type
                """),
                {**params, 'amenity_type': amenity_type},
            ).fetchone()
        else:
            rows = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_amenity_bookings
                    WHERE owner_id = :user_id
                      AND condominium_id = :condominium_id
                      AND status IN ('confirmed', 'completed')
                      AND deleted_at IS NULL
                """),
                params,
            ).fetchone()

        count = int(rows[0]) if rows and rows[0] else 0
        return 1.0 / (1.0 + count)

    @staticmethod
    def equal_share_reason(booking_count: int) -> str:
        return f"equal_share: {booking_count} total bookings"

    # ── Orchestrator ─────────────────────────────────────────────────

    def score_entries(
        self,
        session,
        entries: List[Dict[str, Any]],
        priority_policy: str,
        condominium_id: int,
        amenity_type: Optional[str] = None,
        evaluation_window_days: int = 30,
    ) -> List[WaitlistEntryScore]:
        """
        Score a list of waitlist entries according to the priority policy.

        Returns entries sorted by score descending (highest first = wins).
        """
        scored: List[WaitlistEntryScore] = []

        for entry in entries:
            entry_id = entry['id']
            user_id = entry['user_id']

            if priority_policy == 'fifo':
                created_at = entry['created_at']
                score = self.score_fifo(created_at)
                reason = self.fifo_reason(created_at)

            elif priority_policy == 'less_usage_first':
                count = self._get_booking_count(
                    session, user_id, condominium_id, amenity_type,
                    window_days=evaluation_window_days,
                )
                score = float(evaluation_window_days - count)
                reason = self.less_usage_reason(count, evaluation_window_days)

            elif priority_policy == 'equal_share':
                count = self._get_booking_count(
                    session, user_id, condominium_id, amenity_type,
                )
                score = 1.0 / (1.0 + count)
                reason = self.equal_share_reason(count)

            else:
                # Default to FIFO
                created_at = entry['created_at']
                score = self.score_fifo(created_at)
                reason = self.fifo_reason(created_at)

            scored.append(WaitlistEntryScore(
                entry_id=entry_id,
                user_id=user_id,
                unit_id=entry['unit_id'],
                amenity_id=entry['amenity_id'],
                score=score,
                reason=reason,
            ))

        scored.sort(key=lambda e: e.score, reverse=True)
        return scored

    @staticmethod
    def _get_booking_count(
        session,
        user_id: int,
        condominium_id: int,
        amenity_type: Optional[str] = None,
        window_days: Optional[int] = None,
    ) -> int:
        """Count confirmed/completed bookings for a user."""
        params = {
            'user_id': user_id,
            'condominium_id': condominium_id,
        }
        type_join = ''
        type_filter = ''
        if amenity_type:
            type_join = 'JOIN core_amenities a ON a.id = b.amenity_id'
            type_filter = 'AND a.amenity_type = :amenity_type'
            params['amenity_type'] = amenity_type

        window_filter = ''
        if window_days is not None:
            window_start = datetime.utcnow() - timedelta(days=window_days)
            window_filter = 'AND b.created_at >= :window_start'
            params['window_start'] = window_start

        rows = session.execute(
            text(f"""
                SELECT COUNT(*) FROM core_amenity_bookings b
                {type_join}
                WHERE b.owner_id = :user_id
                  AND b.condominium_id = :condominium_id
                  AND b.status IN ('confirmed', 'completed')
                  AND b.deleted_at IS NULL
                  {type_filter}
                  {window_filter}
            """),
            params,
        ).fetchone()
        return int(rows[0]) if rows and rows[0] else 0
