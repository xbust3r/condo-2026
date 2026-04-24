"""
from typing import Optional
Announcement Query Repository Implementation — with bulk enrichment.
"""
from datetime import date
from typing import Optional, List, Tuple

from sqlalchemy import and_, or_, text

from library.dddpy.core_announcements.domain.announcement_entity import AnnouncementEntity
from library.dddpy.core_announcements.domain.announcement_query_repository import (
    AnnouncementQueryRepository,
)
from library.dddpy.core_announcements.infrastructure.dbannouncement import DBAnnouncement
from library.dddpy.core_announcements.infrastructure.announcement_mapper import (
    AnnouncementMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AnnouncementQueryRepository")


class AnnouncementQueryRepositoryImpl(AnnouncementQueryRepository):

    def _bulk_enrich(
        self,
        rows: List[DBAnnouncement],
        author_names: dict = None,
        condo_names: dict = None,
    ) -> List[AnnouncementEntity]:
        return [
            AnnouncementMapper.to_domain_enriched(
                row,
                author_name=author_names.get(row.author_user_id) if author_names else None,
                condominium_name=condo_names.get(row.condominium_id) if condo_names else None,
            )
            for row in rows
        ]

    def _fetch_author_names(self, rows: List[DBAnnouncement]) -> dict:
        if not rows:
            return {}
        user_ids = [r.author_user_id for r in {r.author_user_id: r for r in rows}.keys()]
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

    def _fetch_condo_names(self, rows: List[DBAnnouncement]) -> dict:
        if not rows:
            return {}
        condo_ids = [r.condominium_id for r in {r.condominium_id: r for r in rows}.keys()]
        with session_scope() as session:
            from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
            result = session.query(DBCondominium.id, DBCondominium.name).filter(
                DBCondominium.id.in_(condo_ids)
            ).all()
            return dict(result)

    def get_by_id(self, id: int) -> Optional[AnnouncementEntity]:
        logger.debug(f"Fetching announcement by id={id}")
        with session_scope() as session:
            row = session.query(DBAnnouncement).filter(
                DBAnnouncement.id == id,
                DBAnnouncement.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            author_names = self._fetch_author_names([row])
            condo_names = self._fetch_condo_names([row])
            return AnnouncementMapper.to_domain_enriched(
                row,
                author_name=author_names.get(row.author_user_id),
                condominium_name=condo_names.get(row.condominium_id),
            )

    def get_by_uuid(self, uuid: str) -> Optional[AnnouncementEntity]:
        logger.debug(f"Fetching announcement by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBAnnouncement).filter(
                DBAnnouncement.uuid == uuid,
                DBAnnouncement.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            author_names = self._fetch_author_names([row])
            condo_names = self._fetch_condo_names([row])
            return AnnouncementMapper.to_domain_enriched(
                row,
                author_name=author_names.get(row.author_user_id),
                condominium_name=condo_names.get(row.condominium_id),
            )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[AnnouncementEntity], int]:
        logger.debug(f"Listing announcements skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBAnnouncement)
            if not include_deleted:
                query = query.filter(DBAnnouncement.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBAnnouncement.condominium_id == condominium_id)
            if category:
                query = query.filter(DBAnnouncement.category == category)
            if visibility:
                query = query.filter(DBAnnouncement.visibility == visibility)

            total = query.count()
            rows = query.order_by(DBAnnouncement.created_at.desc()).offset(skip).limit(limit).all()

            author_names = self._fetch_author_names(rows)
            condo_names = self._fetch_condo_names(rows)
            return self._bulk_enrich(rows, author_names, condo_names), total

    def list_active(
        self,
        condominium_id: int,
        as_of_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AnnouncementEntity], int]:
        check_date = as_of_date or date.today()
        logger.debug(f"Listing active announcements for condominium={condominium_id}")
        with session_scope() as session:
            query = session.query(DBAnnouncement).filter(
                and_(
                    DBAnnouncement.condominium_id == condominium_id,
                    DBAnnouncement.deleted_at.is_(None),
                    DBAnnouncement.published_at.isnot(None),
                ),
            ).filter(
                or_(
                    DBAnnouncement.expires_at.is_(None),
                    DBAnnouncement.expires_at > check_date,
                )
            )
            total = query.count()
            rows = (
                query
                .order_by(DBAnnouncement.is_pinned.desc(), DBAnnouncement.published_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            author_names = self._fetch_author_names(rows)
            condo_names = self._fetch_condo_names(rows)
            return self._bulk_enrich(rows, author_names, condo_names), total
