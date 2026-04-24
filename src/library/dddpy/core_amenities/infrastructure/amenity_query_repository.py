"""
Amenity Query Repository Implementation — with bulk enrichment.
"""
from typing import Optional, List, Tuple

from sqlalchemy import and_, text

from library.dddpy.core_amenities.domain.amenity_entity import AmenityEntity
from library.dddpy.core_amenities.domain.amenity_query_repository import (
    AmenityQueryRepository,
)
from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity
from library.dddpy.core_amenities.infrastructure.amenity_mapper import (
    AmenityMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AmenityQueryRepository")


class AmenityQueryRepositoryImpl(AmenityQueryRepository):

    def _bulk_enrich(
        self,
        rows: List[DBAmenity],
        condo_names: dict = None,
    ) -> List[AmenityEntity]:
        return [
            AmenityMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id) if condo_names else None,
            )
            for row in rows
        ]

    def _fetch_condo_names(self, rows: List[DBAmenity]) -> dict:
        if not rows:
            return {}
        condo_ids = [r.condominium_id for r in {r.condominium_id: r for r in rows}.keys()]
        with session_scope() as session:
            from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
            result = session.query(DBCondominium.id, DBCondominium.name).filter(
                DBCondominium.id.in_(condo_ids)
            ).all()
            return dict(result)

    def get_by_id(self, id: int) -> Optional[AmenityEntity]:
        logger.debug(f"Fetching amenity by id={id}")
        with session_scope() as session:
            row = session.query(DBAmenity).filter(
                DBAmenity.id == id,
                DBAmenity.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            condo_names = self._fetch_condo_names([row])
            return AmenityMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id),
            )

    def get_by_uuid(self, uuid: str) -> Optional[AmenityEntity]:
        logger.debug(f"Fetching amenity by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBAmenity).filter(
                DBAmenity.uuid == uuid,
                DBAmenity.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            condo_names = self._fetch_condo_names([row])
            return AmenityMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id),
            )

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> Tuple[List[AmenityEntity], int]:
        logger.debug(f"Listing amenities skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBAmenity)
            if not include_deleted:
                query = query.filter(DBAmenity.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBAmenity.condominium_id == condominium_id)
            if status:
                query = query.filter(DBAmenity.status == status)

            total = query.count()
            rows = query.order_by(DBAmenity.name.asc()).offset(skip).limit(limit).all()

            condo_names = self._fetch_condo_names(rows)
            return self._bulk_enrich(rows, condo_names), total

    def list_active(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AmenityEntity], int]:
        logger.debug(f"Listing active amenities for condominium={condominium_id}")
        with session_scope() as session:
            query = session.query(DBAmenity).filter(
                and_(
                    DBAmenity.condominium_id == condominium_id,
                    DBAmenity.deleted_at.is_(None),
                    DBAmenity.status == 'active',
                ),
            )
            total = query.count()
            rows = (
                query
                .order_by(DBAmenity.name.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            condo_names = self._fetch_condo_names(rows)
            return self._bulk_enrich(rows, condo_names), total
