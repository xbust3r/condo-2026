"""
AmenityObservabilityUseCase — aggregated metrics for amenity operations (B8).

Layers on top of UsageReportUseCase + AmenityUsageUseCase to provide:
- Operational metrics (no-show rate, check-in rate, avg real usage)
- Waitlist metrics (promotions, expirations, conversion detail)
- Usage timeline per amenity/booking

Design decision: metrics derive from usage_logs (operational reality)
+ allocation_audit (engine decisions). Never from raw bookings alone.
"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import text

from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger

logger = Logger("AmenityObservabilityUseCase")


class AmenityObservabilityUseCase:
    """Aggregated metrics combining allocation audit + usage logs."""

    # ── Usage timeline ───────────────────────────────────────────────

    def usage_timeline(
        self,
        amenity_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """All usage events for an amenity in chronological order."""
        clauses = ["ul.amenity_id = :aid"]
        params: Dict[str, Any] = {'aid': amenity_id}
        if from_date:
            clauses.append("DATE(ul.event_at) >= :from_dt")
            params['from_dt'] = from_date
        if to_date:
            clauses.append("DATE(ul.event_at) <= :to_dt")
            params['to_dt'] = to_date
        params['lim'] = limit

        where = ' AND '.join(clauses)

        with session_scope() as session:
            rows = session.execute(
                text(f"""
                    SELECT
                        ul.id, ul.uuid, ul.booking_id, ul.amenity_id,
                        ul.unit_id, ul.owner_id,
                        ul.event_type, ul.event_at, ul.recorded_by, ul.source,
                        ul.notes, ul.event_context_json, ul.created_at
                    FROM core_amenity_usage_logs ul
                    WHERE {where}
                    ORDER BY ul.event_at DESC
                    LIMIT :lim
                """),
                params,
            ).fetchall()
        return [dict(r._mapping) for r in rows]

    # ── Operational metrics ──────────────────────────────────────────

    def operational_metrics(
        self,
        amenity_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Metrics derived from usage_logs: check-in rate, no-show rate,
        avg real usage minutes.
        """
        if not from_date:
            from_date = date.today().replace(day=1)
        if not to_date:
            to_date = date.today()

        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT
                        COUNT(DISTINCT CASE WHEN ul.event_type = 'CHECK_IN'
                            THEN ul.booking_id END) AS total_check_ins,
                        COUNT(DISTINCT CASE WHEN ul.event_type = 'NO_SHOW'
                            THEN ul.booking_id END) AS total_no_shows,
                        COUNT(DISTINCT ul.booking_id) AS total_tracked,
                        AVG(CASE WHEN ul.event_type = 'CHECK_IN' THEN
                            (SELECT TIMESTAMPDIFF(MINUTE,
                                ci.event_at,
                                COALESCE(
                                    (SELECT co.event_at FROM core_amenity_usage_logs co
                                     WHERE co.booking_id = ul.booking_id
                                     AND co.event_type = 'CHECK_OUT'
                                     LIMIT 1),
                                    ci.event_at
                                )
                            )
                            FROM core_amenity_usage_logs ci
                            WHERE ci.id = ul.id
                            ) END) AS avg_real_usage_minutes
                    FROM core_amenity_usage_logs ul
                    WHERE ul.amenity_id = :aid
                      AND DATE(ul.event_at) BETWEEN :from_dt AND :to_dt
                """),
                {'aid': amenity_id, 'from_dt': from_date, 'to_dt': to_date},
            ).fetchone()
        metrics = dict(row._mapping)

        # Derived rates
        total_tracked = metrics.get('total_tracked', 0) or 1
        metrics['check_in_rate'] = (
            round((metrics.get('total_check_ins', 0) or 0) / total_tracked, 4)
        )
        metrics['no_show_rate'] = (
            round((metrics.get('total_no_shows', 0) or 0) / total_tracked, 4)
        )
        return metrics

    # ── Waitlist metrics ─────────────────────────────────────────────

    def waitlist_metrics(
        self,
        amenity_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """Waitlist lifecycle metrics: promoted, expired, conversion."""
        if not from_date:
            from_date = date.today().replace(day=1)
        if not to_date:
            to_date = date.today()

        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT
                        COUNT(*) AS total_waitlisted,
                        SUM(CASE WHEN status = 'CONVERTED' THEN 1 ELSE 0 END) AS total_promoted,
                        SUM(CASE WHEN status = 'EXPIRED' THEN 1 ELSE 0 END) AS total_expired,
                        SUM(CASE WHEN status = 'NOTIFIED' THEN 1 ELSE 0 END) AS total_notified,
                        SUM(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) AS total_cancelled,
                        SUM(CASE WHEN status = 'WAITING' THEN 1 ELSE 0 END) AS total_waiting
                    FROM core_amenity_waitlist
                    WHERE amenity_id = :aid
                      AND DATE(booking_date) BETWEEN :from_dt AND :to_dt
                """),
                {'aid': amenity_id, 'from_dt': from_date, 'to_dt': to_date},
            ).fetchone()
        metrics = dict(row._mapping)
        total = metrics.get('total_waitlisted', 0) or 1
        metrics['conversion_rate'] = round(
            (metrics.get('total_promoted', 0) or 0) / total, 4
        )
        metrics['expiration_rate'] = round(
            (metrics.get('total_expired', 0) or 0) / total, 4
        )
        return metrics

    # ── Combined metrics snapshot ────────────────────────────────────

    def combined_amenity_metrics(
        self,
        amenity_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """Single snapshot of all amenity metrics."""
        from library.dddpy.core_amenity_bookings.usecase.usage_report_usecase import UsageReportUseCase

        ruc = UsageReportUseCase()
        op_metrics = self.operational_metrics(amenity_id, from_date, to_date)
        wl_metrics = self.waitlist_metrics(amenity_id, from_date, to_date)
        rejection = ruc.rejection_distribution(amenity_id, from_date, to_date)
        conversion = ruc.waitlist_conversion_rate(amenity_id, from_date, to_date)

        return {
            'amenity_id': amenity_id,
            'from_date': from_date.isoformat() if from_date else None,
            'to_date': to_date.isoformat() if to_date else None,
            'operational': op_metrics,
            'waitlist': wl_metrics,
            'rejection_distribution': rejection,
            'conversion_detail': conversion,
        }

    # ── Condominium-level metrics ────────────────────────────────────

    def condominium_amenity_metrics(
        self,
        condominium_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """Per-amenity metrics for the whole condominium."""
        if not from_date:
            from_date = date.today().replace(day=1)
        if not to_date:
            to_date = date.today()

        with session_scope() as session:
            rows = session.execute(
                text("""
                    SELECT
                        a.id AS amenity_id,
                        a.name AS amenity_name,
                        a.amenity_type,
                        COUNT(DISTINCT b.id) AS total_bookings,
                        SUM(CASE WHEN b.status = 'confirmed' THEN 1 ELSE 0 END) AS total_confirmed,
                        SUM(CASE WHEN b.status = 'completed' THEN 1 ELSE 0 END) AS total_completed,
                        COUNT(DISTINCT w.id) AS total_waitlisted,
                        SUM(CASE WHEN w.status = 'CONVERTED' THEN 1 ELSE 0 END) AS total_promoted
                    FROM core_amenities a
                    LEFT JOIN core_amenity_bookings b ON b.amenity_id = a.id
                        AND b.booking_date BETWEEN :from_dt AND :to_dt
                        AND b.deleted_at IS NULL
                    LEFT JOIN core_amenity_waitlist w ON w.amenity_id = a.id
                        AND DATE(w.booking_date) BETWEEN :from_dt AND :to_dt
                    WHERE a.condominium_id = :cid
                    GROUP BY a.id, a.name, a.amenity_type
                    ORDER BY total_bookings DESC
                """),
                {'cid': condominium_id, 'from_dt': from_date, 'to_dt': to_date},
            ).fetchall()
        return [dict(r._mapping) for r in rows]
