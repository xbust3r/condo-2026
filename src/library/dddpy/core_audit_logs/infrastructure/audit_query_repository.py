"""
Audit log query repository implementation — raw SQL for JSON column and date filters.
"""
from typing import List, Optional, Tuple
from sqlalchemy import text

from library.dddpy.core_audit_logs.domain.audit_query_repository import AuditLogQueryRepository
from library.dddpy.core_audit_logs.domain.audit_log_entity import AuditLogEntity
from library.dddpy.core_audit_logs.infrastructure.dbaudit import DBAuditLog
from library.dddpy.core_audit_logs.infrastructure.audit_mapper import AuditLogMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AuditQueryRepository")


class AuditQueryRepositoryImpl(AuditLogQueryRepository):

    def __init__(self):
        logger.info("AuditQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[AuditLogEntity]:
        logger.info(f"Fetching audit log by id={id}")
        with session_scope() as session:
            db_row = session.query(DBAuditLog).filter(DBAuditLog.id == id).first()
            if not db_row:
                return None
            return AuditLogMapper.to_domain(db_row)

    def list_by_resource(
        self,
        resource_type: str,
        resource_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AuditLogEntity], int]:
        logger.info(f"Listing audit logs for resource {resource_type}:{resource_id}")
        with session_scope() as session:
            # count
            count_q = text("SELECT COUNT(*) FROM core_audit_logs WHERE resource_type = :rt AND resource_id = :rid")
            total = session.execute(count_q, {"rt": resource_type, "rid": resource_id}).scalar() or 0

            # rows
            rows_q = text("""
                SELECT id FROM core_audit_logs
                WHERE resource_type = :rt AND resource_id = :rid
                ORDER BY created_at DESC
                LIMIT :lim OFFSET :off
            """)
            rows = session.execute(rows_q, {
                "rt": resource_type,
                "rid": resource_id,
                "lim": limit,
                "off": skip,
            }).fetchall()

            if not rows:
                return [], total

            ids = [r.id for r in rows]
            db_rows = session.query(DBAuditLog).filter(DBAuditLog.id.in_(ids)).all()
            return [AuditLogMapper.to_domain(r) for r in db_rows], total

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AuditLogEntity], int]:
        logger.info(f"Listing audit logs for user_id={user_id}")
        with session_scope() as session:
            total = session.query(DBAuditLog).filter(DBAuditLog.user_id == user_id).count()
            rows = (
                session.query(DBAuditLog)
                .filter(DBAuditLog.user_id == user_id)
                .order_by(DBAuditLog.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [AuditLogMapper.to_domain(r) for r in rows], total

    def list_all(
        self,
        filters: dict,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AuditLogEntity], int]:
        logger.info(f"Listing all audit logs with filters={filters}")
        with session_scope() as session:
            conditions = []
            params = {}

            action = filters.get("action")
            if action:
                conditions.append("action = :action")
                params["action"] = action

            resource_type = filters.get("resource_type")
            if resource_type:
                conditions.append("resource_type = :resource_type")
                params["resource_type"] = resource_type

            user_id = filters.get("user_id")
            if user_id is not None:
                conditions.append("user_id = :user_id")
                params["user_id"] = user_id

            date_from = filters.get("date_from")
            if date_from:
                conditions.append("created_at >= :date_from")
                params["date_from"] = date_from

            date_to = filters.get("date_to")
            if date_to:
                conditions.append("created_at <= :date_to")
                params["date_to"] = date_to

            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

            # count
            count_q = text(f"SELECT COUNT(*) FROM core_audit_logs {where_clause}")
            total = session.execute(count_q, params).scalar() or 0

            # rows
            params["lim"] = limit
            params["off"] = skip
            rows_q = text(f"""
                SELECT id FROM core_audit_logs
                {where_clause}
                ORDER BY created_at DESC
                LIMIT :lim OFFSET :off
            """)
            rows = session.execute(rows_q, params).fetchall()

            if not rows:
                return [], total

            ids = [r.id for r in rows]
            db_rows = session.query(DBAuditLog).filter(DBAuditLog.id.in_(ids)).all()
            return [AuditLogMapper.to_domain(r) for r in db_rows], total