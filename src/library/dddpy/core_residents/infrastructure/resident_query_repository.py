"""
from typing import Optional
Resident query repository implementation — aggregates dashboard data from multiple modules.
"""
from typing import Optional, List, Tuple
from datetime import date

from sqlalchemy import text

from library.dddpy.core_residents.domain.resident_profile_entity import ResidentProfileEntity
from library.dddpy.core_residents.domain.resident_query_repository import ResidentQueryRepository
from library.dddpy.core_residents.infrastructure.dbresident import DBResidentProfile
from library.dddpy.core_residents.infrastructure.resident_mapper import ResidentMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ResidentQueryRepository")


class ResidentQueryRepositoryImpl(ResidentQueryRepository):

    def get_profile(self, user_id: int, condominium_id: int) -> Optional[ResidentProfileEntity]:
        logger.debug(f"Fetching resident profile for user_id={user_id}, condo={condominium_id}")
        with session_scope() as session:
            row = session.query(DBResidentProfile).filter(
                DBResidentProfile.user_id == user_id,
                DBResidentProfile.condominium_id == condominium_id,
                DBResidentProfile.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            return ResidentMapper.to_domain(row)

    def get_dashboard_summary(
        self,
        user_id: int,
        condominium_id: int,
    ) -> dict:
        """
        Aggregate dashboard data for a resident.
        Joins across modules to produce a single summary dict.
        """
        logger.debug(f"Building dashboard summary for user_id={user_id}, condo={condominium_id}")

        with session_scope() as session:
            # Unread notifications count
            notif_count = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_notifications n
                    WHERE n.user_id = :uid AND n.is_read = 0 AND n.deleted_at IS NULL
                """),
                {"uid": user_id},
            ).scalar() or 0

            # Pending incidents (open status)
            pending_incidents = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_incidents i
                    JOIN core_unit_occupancies occ ON occ.unit_id = i.unit_id
                    WHERE occ.user_id = :uid
                      AND occ.end_date IS NULL
                      AND i.condominium_id = :condo_id
                      AND i.status IN ('open', 'in_progress')
                      AND i.deleted_at IS NULL
                """),
                {"uid": user_id, "condo_id": condominium_id},
            ).scalar() or 0

            # Pending packages (not delivered/cancelled)
            pending_packages = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_packages p
                    WHERE p.recipient_user_id = :uid
                      AND p.condominium_id = :condo_id
                      AND p.status NOT IN ('delivered', 'cancelled')
                      AND p.deleted_at IS NULL
                """),
                {"uid": user_id, "condo_id": condominium_id},
            ).scalar() or 0

            # Upcoming visitor registrations (expected today or tomorrow)
            from datetime import datetime, timedelta
            today = datetime.utcnow().date()
            tomorrow = today + timedelta(days=1)
            upcoming_visitors = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_visitors v
                    JOIN core_unit_occupancies occ ON occ.unit_id = v.unit_id
                    WHERE occ.user_id = :uid
                      AND occ.end_date IS NULL
                      AND v.condominium_id = :condo_id
                      AND DATE(v.expected_date) <= :tomorrow
                      AND v.actual_checkin_at IS NULL
                      AND v.deleted_at IS NULL
                """),
                {"uid": user_id, "condo_id": condominium_id, "tomorrow": tomorrow},
            ).scalar() or 0

            # Recent announcements (last 5 active)
            recent_announcements_raw = session.execute(
                text("""
                    SELECT a.uuid, a.title, a.category, a.published_at, a.is_pinned
                    FROM core_announcements a
                    WHERE a.condominium_id = :condo_id
                      AND a.deleted_at IS NULL
                      AND a.published_at IS NOT NULL
                      AND (a.expires_at IS NULL OR a.expires_at >= :today)
                    ORDER BY a.is_pinned DESC, a.published_at DESC
                    LIMIT 5
                """),
                {"condo_id": condominium_id, "today": today},
            ).fetchall()

            recent_announcements = [
                {
                    "uuid": r.uuid,
                    "title": r.title,
                    "category": r.category,
                    "published_at": r.published_at.isoformat() if r.published_at else None,
                    "is_pinned": r.is_pinned,
                }
                for r in recent_announcements_raw
            ]

            # Payment summary (last 30 days pending)
            payment_pending = session.execute(
                text("""
                    SELECT COALESCE(SUM(ar.amount - ar.paid_amount), 0) AS pending
                    FROM core_accounts_receivable ar
                    JOIN core_unit_ownerships ow ON ow.unit_id = ar.unit_id
                    WHERE ow.user_id = :uid
                      AND ar.condominium_id = :condo_id
                      AND ar.status NOT IN ('paid', 'cancelled')
                      AND ar.deleted_at IS NULL
                """),
                {"uid": user_id, "condo_id": condominium_id},
            ).scalar() or 0.0

            return {
                "user_id": user_id,
                "condominium_id": condominium_id,
                "unread_notifications": notif_count,
                "pending_incidents": pending_incidents,
                "pending_packages": pending_packages,
                "upcoming_visitors": upcoming_visitors,
                "payment_pending_total": float(payment_pending),
                "recent_announcements": recent_announcements,
            }

    def list_my_incidents(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List, int]:
        with session_scope() as session:
            rows = session.execute(
                text("""
                    SELECT DISTINCT i.uuid, i.title, i.category, i.priority, i.status,
                           i.created_at, u.unit_code, b.name AS building_name
                    FROM core_incidents i
                    JOIN core_unit_occupancies occ ON occ.unit_id = i.unit_id
                    LEFT JOIN core_units u ON u.id = i.unit_id
                    LEFT JOIN core_buildings b ON b.id = u.building_id
                    WHERE occ.user_id = :uid
                      AND occ.end_date IS NULL
                      AND i.condominium_id = :condo_id
                      AND i.deleted_at IS NULL
                    ORDER BY i.created_at DESC
                    LIMIT :limit OFFSET :skip
                """),
                {"uid": user_id, "condo_id": condominium_id, "limit": limit, "skip": skip},
            ).fetchall()

            total = session.execute(
                text("""
                    SELECT COUNT(DISTINCT i.id)
                    FROM core_incidents i
                    JOIN core_unit_occupancies occ ON occ.unit_id = i.unit_id
                    WHERE occ.user_id = :uid
                      AND occ.end_date IS NULL
                      AND i.condominium_id = :condo_id
                      AND i.deleted_at IS NULL
                """),
                {"uid": user_id, "condo_id": condominium_id},
            ).scalar() or 0

            return [dict(row._mapping) for row in rows], int(total)

    def list_my_packages(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List, int]:
        with session_scope() as session:
            rows = session.execute(
                text("""
                    SELECT p.uuid, p.carrier, p.description, p.status,
                           p.received_at, p.pickup_code, u.unit_code
                    FROM core_packages p
                    LEFT JOIN core_units u ON u.id = p.unit_id
                    WHERE p.recipient_user_id = :uid
                      AND p.condominium_id = :condo_id
                      AND p.deleted_at IS NULL
                    ORDER BY p.received_at DESC
                    LIMIT :limit OFFSET :skip
                """),
                {"uid": user_id, "condo_id": condominium_id, "limit": limit, "skip": skip},
            ).fetchall()

            total = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_packages p
                    WHERE p.recipient_user_id = :uid
                      AND p.condominium_id = :condo_id
                      AND p.deleted_at IS NULL
                """),
                {"uid": user_id, "condo_id": condominium_id},
            ).scalar() or 0

            return [dict(row._mapping) for row in rows], int(total)

    def list_my_visitors(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List, int]:
        with session_scope() as session:
            rows = session.execute(
                text("""
                    SELECT v.uuid, v.visitor_name, v.expected_date, v.status,
                           v.access_code, u.unit_code
                    FROM core_visitors v
                    JOIN core_unit_occupancies occ ON occ.unit_id = v.unit_id
                    LEFT JOIN core_units u ON u.id = v.unit_id
                    WHERE occ.user_id = :uid
                      AND occ.end_date IS NULL
                      AND v.condominium_id = :condo_id
                      AND v.deleted_at IS NULL
                    ORDER BY v.expected_date DESC
                    LIMIT :limit OFFSET :skip
                """),
                {"uid": user_id, "condo_id": condominium_id, "limit": limit, "skip": skip},
            ).fetchall()

            total = session.execute(
                text("""
                    SELECT COUNT(*)
                    FROM core_visitors v
                    JOIN core_unit_occupancies occ ON occ.unit_id = v.unit_id
                    WHERE occ.user_id = :uid
                      AND occ.end_date IS NULL
                      AND v.condominium_id = :condo_id
                      AND v.deleted_at IS NULL
                """),
                {"uid": user_id, "condo_id": condominium_id},
            ).scalar() or 0

            return [dict(row._mapping) for row in rows], int(total)

    def list_all_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List, int]:
        """List all resident profiles for a condominium (admin view)."""
        with session_scope() as session:
            rows = session.execute(
                text("""
                    SELECT
                        rp.uuid, rp.id, rp.user_id, rp.condominium_id,
                        rp.notify_announcements, rp.notify_incidents,
                        rp.notify_packages, rp.notify_visitors, rp.notify_payments,
                        rp.language, rp.theme, rp.default_building_id,
                        rp.notes, rp.created_at, rp.updated_at,
                        CONCAT(COALESCE(up.first_name, ""), " ", COALESCE(up.last_name, "")) AS user_full_name,
                        u.email AS user_email,
                        up.phone AS user_phone,
                        c.name AS condominium_name
                    FROM core_resident_profiles rp
                    JOIN users u ON u.id = rp.user_id
                    LEFT JOIN user_profiles up ON up.user_id = rp.user_id
                    JOIN core_condominiums c ON c.id = rp.condominium_id
                    WHERE rp.condominium_id = :condo_id
                      AND rp.deleted_at IS NULL
                    ORDER BY rp.created_at DESC
                    LIMIT :limit OFFSET :skip
                """),
                {"condo_id": condominium_id, "limit": limit, "skip": skip},
            ).fetchall()

            total = session.execute(
                text("""
                    SELECT COUNT(*)
                    FROM core_resident_profiles rp
                    WHERE rp.condominium_id = :condo_id
                      AND rp.deleted_at IS NULL
                """),
                {"condo_id": condominium_id},
            ).scalar() or 0

            return [dict(row._mapping) for row in rows], int(total)

    def get_profile_by_id(self, profile_id: int) -> Optional[object]:
        """Get a specific resident profile by ID (admin)."""
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT
                        rp.uuid, rp.id, rp.user_id, rp.condominium_id,
                        rp.notify_announcements, rp.notify_incidents,
                        rp.notify_packages, rp.notify_visitors, rp.notify_payments,
                        rp.language, rp.theme, rp.default_building_id,
                        rp.notes, rp.created_at, rp.updated_at,
                        CONCAT(COALESCE(up.first_name, ""), " ", COALESCE(up.last_name, "")) AS user_full_name,
                        u.email AS user_email,
                        up.phone AS user_phone,
                        c.name AS condominium_name
                    FROM core_resident_profiles rp
                    JOIN users u ON u.id = rp.user_id
                    LEFT JOIN user_profiles up ON up.user_id = rp.user_id
                    JOIN core_condominiums c ON c.id = rp.condominium_id
                    WHERE rp.id = :profile_id
                      AND rp.deleted_at IS NULL
                """),
                {"profile_id": profile_id},
            ).fetchone()
            if not row:
                return None
            return dict(row._mapping)
