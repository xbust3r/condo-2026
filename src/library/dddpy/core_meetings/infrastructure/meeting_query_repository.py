"""
from typing import Optional
Meeting Query Repository Implementation — with bulk enrichment.
"""
from datetime import datetime
from typing import Optional, List, Tuple

from sqlalchemy import and_, text

from library.dddpy.core_meetings.domain.meeting_entity import MeetingEntity
from library.dddpy.core_meetings.domain.meeting_query_repository import (
    MeetingQueryRepository,
)
from library.dddpy.core_meetings.infrastructure.dbmeeting import DBMeeting
from library.dddpy.core_meetings.infrastructure.meeting_mapper import (
    MeetingMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("MeetingQueryRepository")


class MeetingQueryRepositoryImpl(MeetingQueryRepository):

    def _bulk_enrich(
        self,
        rows: List[DBMeeting],
        created_by_names: dict = None,
        condo_names: dict = None,
    ) -> List[MeetingEntity]:
        return [
            MeetingMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id) if condo_names else None,
                created_by_name=created_by_names.get(row.created_by_user_id) if created_by_names else None,
            )
            for row in rows
        ]

    def _fetch_created_by_names(self, rows: List[DBMeeting]) -> dict:
        if not rows:
            return {}
        user_ids = list({r.created_by_user_id for r in rows})
        with session_scope() as session:
            result = session.execute(
                text("""
                    SELECT u.id, COALESCE(CONCAT(p.first_name, ' ', p.last_name), u.email) AS full_name
                    FROM users u
                    LEFT JOIN user_profiles p ON p.user_id = u.id AND p.deleted_at IS NULL
                    WHERE u.id IN :ids
                """),
                {"ids": tuple(user_ids)},
            )
            return {row.id: row.full_name for row in result}

    def _fetch_condo_names(self, rows: List[DBMeeting]) -> dict:
        if not rows:
            return {}
        condo_ids = list({r.condominium_id for r in rows})
        with session_scope() as session:
            from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
            result = session.query(DBCondominium.id, DBCondominium.name).filter(
                DBCondominium.id.in_(condo_ids)
            ).all()
            return dict(result)

    def get_by_id(self, id: int) -> Optional[MeetingEntity]:
        logger.debug(f"Fetching meeting by id={id}")
        with session_scope() as session:
            row = session.query(DBMeeting).filter(
                DBMeeting.id == id,
                DBMeeting.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            created_by_names = self._fetch_created_by_names([row])
            condo_names = self._fetch_condo_names([row])
            return MeetingMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id),
                created_by_name=created_by_names.get(row.created_by_user_id),
            )

    def get_by_uuid(self, uuid: str) -> Optional[MeetingEntity]:
        logger.debug(f"Fetching meeting by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBMeeting).filter(
                DBMeeting.uuid == uuid,
                DBMeeting.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            created_by_names = self._fetch_created_by_names([row])
            condo_names = self._fetch_condo_names([row])
            return MeetingMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id),
                created_by_name=created_by_names.get(row.created_by_user_id),
            )

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        meeting_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> Tuple[List[MeetingEntity], int]:
        logger.debug(f"Listing meetings skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBMeeting)
            if not include_deleted:
                query = query.filter(DBMeeting.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBMeeting.condominium_id == condominium_id)
            if status:
                query = query.filter(DBMeeting.status == status)
            if meeting_type:
                query = query.filter(DBMeeting.meeting_type == meeting_type)

            total = query.count()
            rows = query.order_by(DBMeeting.meeting_date.desc()).offset(skip).limit(limit).all()

            created_by_names = self._fetch_created_by_names(rows)
            condo_names = self._fetch_condo_names(rows)
            return self._bulk_enrich(rows, created_by_names, condo_names), total

    def list_upcoming(
        self,
        condominium_id: int,
        as_of_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[MeetingEntity], int]:
        check_date = as_of_date or datetime.utcnow()
        logger.debug(f"Listing upcoming meetings for condominium={condominium_id}")
        with session_scope() as session:
            query = session.query(DBMeeting).filter(
                and_(
                    DBMeeting.condominium_id == condominium_id,
                    DBMeeting.deleted_at.is_(None),
                    DBMeeting.meeting_date >= check_date,
                    DBMeeting.status.in_(['scheduled', 'confirmed']),
                ),
            )
            total = query.count()
            rows = (
                query
                .order_by(DBMeeting.meeting_date.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            created_by_names = self._fetch_created_by_names(rows)
            condo_names = self._fetch_condo_names(rows)
            return self._bulk_enrich(rows, created_by_names, condo_names), total
