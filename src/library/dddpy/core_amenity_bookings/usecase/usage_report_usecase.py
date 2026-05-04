"""
UsageReportUseCase — reporting and usage history for amenities.

Provides:
- usage_by_amenity: reservations per amenity in a date range
- usage_by_user: reservations per user in a date range
- allocation_audit_trail: who got what and why
- waitlist_conversion_rate: how many waitlist entries become bookings
- rejection_distribution: why bookings were rejected
"""
import logging
from datetime import date, datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import text

from library.dddpy.shared.mysql.session_manager import session_scope

logger = logging.getLogger(__name__)


class UsageReportUseCase:
    """Reports and usage history for amenities."""

    # ── Usage by amenity ─────────────────────────────────────────────

    def usage_by_amenity(
        self,
        amenity_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        group_by: str = 'day',  # day | month | week
    ) -> List[Dict[str, Any]]:
        """Reservations per amenity in a date range, grouped by period."""
        if not from_date:
            from_date = date.today().replace(day=1)
        if not to_date:
            to_date = date.today()

        trunc = {'day': '%Y-%m-%d', 'month': '%Y-%m', 'week': '%Y-%u'}.get(group_by, '%Y-%m-%d')

        with session_scope() as session:
            rows = session.execute(
                text(f"""
                    SELECT
                        DATE_FORMAT(booking_date, :trunc) AS period,
                        COUNT(*) AS total_bookings,
                        SUM(guest_count) AS total_guests,
                        COUNT(DISTINCT unit_id) AS unique_units,
                        COUNT(DISTINCT owner_id) AS unique_users
                    FROM core_amenity_bookings
                    WHERE amenity_id = :aid
                      AND status IN ('confirmed','completed')
                      AND booking_date BETWEEN :from_dt AND :to_dt
                      AND deleted_at IS NULL
                    GROUP BY period
                    ORDER BY period
                """),
                {
                    'aid': amenity_id,
                    'from_dt': from_date,
                    'to_dt': to_date,
                    'trunc': trunc,
                },
            ).fetchall()
        return [dict(r._mapping) for r in rows]

    # ── Usage by user ────────────────────────────────────────────────

    def usage_by_user(
        self,
        condominium_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        amenity_id: Optional[int] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """How many bookings each user has in a date range."""
        if not from_date:
            from_date = date.today().replace(day=1)
        if not to_date:
            to_date = date.today()

        amenity_filter = "AND amenity_id = :aid" if amenity_id else ""

        with session_scope() as session:
            rows = session.execute(
                text(f"""
                    SELECT
                        owner_id,
                        COUNT(*) AS total_bookings,
                        SUM(guest_count) AS total_guests,
                        COUNT(DISTINCT amenity_id) AS unique_amenities,
                        COUNT(DISTINCT unit_id) AS unique_units,
                        MIN(booking_date) AS first_booking,
                        MAX(booking_date) AS last_booking
                    FROM core_amenity_bookings
                    WHERE condominium_id = :cid
                      AND status IN ('confirmed','completed')
                      AND booking_date BETWEEN :from_dt AND :to_dt
                      AND deleted_at IS NULL
                      {amenity_filter}
                    GROUP BY owner_id
                    ORDER BY total_bookings DESC
                    LIMIT :lim
                """),
                {
                    'cid': condominium_id,
                    'from_dt': from_date,
                    'to_dt': to_date,
                    'aid': amenity_id,
                    'lim': limit,
                },
            ).fetchall()
        return [dict(r._mapping) for r in rows]

    # ── Allocation audit trail ───────────────────────────────────────

    def allocation_audit_trail(
        self,
        amenity_id: Optional[int] = None,
        booking_id: Optional[int] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        decision_types: Optional[List[str]] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Who got what, when, and why — full audit trail."""
        clauses = []
        params: Dict[str, Any] = {}

        if amenity_id:
            clauses.append('audit.amenity_id = :aid')
            params['aid'] = amenity_id
        if booking_id:
            clauses.append('audit.booking_id = :bid')
            params['bid'] = booking_id
        if from_date:
            clauses.append('DATE(audit.created_at) >= :from_dt')
            params['from_dt'] = from_date
        if to_date:
            clauses.append('DATE(audit.created_at) <= :to_dt')
            params['to_dt'] = to_date
        if decision_types:
            placeholders = ','.join(f':dt{i}' for i in range(len(decision_types)))
            clauses.append(f'audit.decision_type IN ({placeholders})')
            for i, dt in enumerate(decision_types):
                params[f'dt{i}'] = dt

        params['lim'] = limit
        where = ('WHERE ' + ' AND '.join(clauses)) if clauses else ''

        with session_scope() as session:
            rows = session.execute(
                text(f"""
                    SELECT
                        audit.id,
                        audit.amenity_id,
                        a.name AS amenity_name,
                        audit.booking_id,
                        audit.waitlist_entry_id,
                        audit.decision_type,
                        audit.decision_reason,
                        audit.decision_context_json,
                        audit.created_at
                    FROM core_amenity_allocation_audit audit
                    JOIN core_amenities a ON a.id = audit.amenity_id
                    {where}
                    ORDER BY audit.created_at DESC
                    LIMIT :lim
                """),
                params,
            ).fetchall()

        return [dict(r._mapping) for r in rows]

    # ── Waitlist conversion rate ─────────────────────────────────────

    def waitlist_conversion_rate(
        self,
        amenity_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """How many waitlist entries convert to bookings."""
        if not from_date:
            from_date = date.today().replace(day=1)
        if not to_date:
            to_date = date.today()

        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT
                        COUNT(*) AS total_waitlisted,
                        SUM(CASE WHEN status = 'CONVERTED' THEN 1 ELSE 0 END) AS total_converted,
                        SUM(CASE WHEN status = 'NOTIFIED' THEN 1 ELSE 0 END) AS total_notified,
                        SUM(CASE WHEN status = 'EXPIRED' THEN 1 ELSE 0 END) AS total_expired,
                        SUM(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) AS total_cancelled,
                        AVG(CASE WHEN status = 'CONVERTED'
                            THEN TIMESTAMPDIFF(MINUTE, created_at, updated_at)
                            ELSE NULL END) AS avg_conversion_minutes
                    FROM core_amenity_waitlist
                    WHERE amenity_id = :aid
                      AND DATE(booking_date) BETWEEN :from_dt AND :to_dt
                """),
                {'aid': amenity_id, 'from_dt': from_date, 'to_dt': to_date},
            ).fetchone()
        return dict(row._mapping)

    # ── Rejection distribution ───────────────────────────────────────

    def rejection_distribution(
        self,
        amenity_id: Optional[int] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """Why bookings were rejected — distribution per reason."""
        clauses = ["decision_type = 'BOOKING_REJECTED'"]
        params = {}

        if amenity_id:
            clauses.append('amenity_id = :aid')
            params['aid'] = amenity_id
        if from_date:
            clauses.append('DATE(created_at) >= :from_dt')
            params['from_dt'] = from_date
        if to_date:
            clauses.append('DATE(created_at) <= :to_dt')
            params['to_dt'] = to_date

        where = ' AND '.join(clauses)

        with session_scope() as session:
            rows = session.execute(
                text(f"""
                    SELECT
                        decision_reason,
                        COUNT(*) AS count,
                        MIN(created_at) AS first_at,
                        MAX(created_at) AS last_at
                    FROM core_amenity_allocation_audit
                    WHERE {where}
                    GROUP BY decision_reason
                    ORDER BY count DESC
                """),
                params,
            ).fetchall()
        return [dict(r._mapping) for r in rows]

    # ── Amenity distribution ────────────────────────────────────────

    def amenity_distribution(
        self,
        condominium_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """Distribution of bookings across amenities."""
        if not from_date:
            from_date = date.today().replace(day=1)
        if not to_date:
            to_date = date.today()

        with session_scope() as session:
            rows = session.execute(
                text("""
                    SELECT
                        b.amenity_id,
                        a.name AS amenity_name,
                        a.amenity_type,
                        COUNT(*) AS total_bookings,
                        SUM(b.guest_count) AS total_guests,
                        COUNT(DISTINCT b.unit_id) AS unique_units,
                        COUNT(DISTINCT b.owner_id) AS unique_users
                    FROM core_amenity_bookings b
                    JOIN core_amenities a ON a.id = b.amenity_id
                    WHERE b.condominium_id = :cid
                      AND b.status IN ('confirmed','completed')
                      AND b.booking_date BETWEEN :from_dt AND :to_dt
                      AND b.deleted_at IS NULL
                    GROUP BY b.amenity_id, a.name, a.amenity_type
                    ORDER BY total_bookings DESC
                """),
                {'cid': condominium_id, 'from_dt': from_date, 'to_dt': to_date},
            ).fetchall()
        return [dict(r._mapping) for r in rows]
