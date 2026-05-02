"""
Amenity Query Repository Implementation — with scope-aware filtering.

Scope-semantics for building_id parameter:

| condominium_id | building_id | Returns                                                |
|---------------|-------------|--------------------------------------------------------|
| set           | None        | scope=CONDOMINIUM amenities of that condominium        |
| set           | set         | CONDOMINIUM amenities + BUILDING amenities for building |
| None          | set         | Resolves condominium from building, same as above       |
"""
from typing import Optional, List, Tuple
from sqlalchemy import or_, and_

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
        condo_names: Optional[dict] = None,
        building_names: Optional[dict] = None,
    ) -> List[AmenityEntity]:
        return [
            AmenityMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id) if condo_names else None,
                building_name=building_names.get(row.building_id) if building_names and row.building_id else None,
            )
            for row in rows
        ]

    def _fetch_condo_names(self, rows: List[DBAmenity]) -> dict:
        if not rows:
            return {}
        condo_ids = list({r.condominium_id for r in rows})
        with session_scope() as session:
            from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
            result = session.query(DBCondominium.id, DBCondominium.name).filter(
                DBCondominium.id.in_(condo_ids)
            ).all()
            return dict(result)

    def _fetch_building_names(self, rows: List[DBAmenity]) -> dict:
        if not rows:
            return {}
        building_ids = list({r.building_id for r in rows if r.building_id is not None})
        if not building_ids:
            return {}
        with session_scope() as session:
            from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
            result = session.query(DBBuildings.id, DBBuildings.name).filter(
                DBBuildings.id.in_(building_ids)
            ).all()
            return dict(result)

    def _resolve_condominium_for_building(self, building_id: int) -> Optional[int]:
        """Resolve condominium_id from a building when only building_id is provided."""
        with session_scope() as session:
            from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
            building = session.query(DBBuildings.condominium_id).filter(
                DBBuildings.id == building_id,
                DBBuildings.deleted_at.is_(None),
            ).first()
            return building.condominium_id if building else None

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
            building_names = self._fetch_building_names([row])
            return AmenityMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id),
                building_name=building_names.get(row.building_id) if row.building_id else None,
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
            building_names = self._fetch_building_names([row])
            return AmenityMapper.to_domain_enriched(
                row,
                condominium_name=condo_names.get(row.condominium_id),
                building_name=building_names.get(row.building_id) if row.building_id else None,
            )

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        building_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> Tuple[List[AmenityEntity], int]:
        logger.debug(
            f"Listing amenities condo={condominium_id} building={building_id} "
            f"skip={skip} limit={limit}"
        )
        with session_scope() as session:
            query = session.query(DBAmenity)

            if not include_deleted:
                query = query.filter(DBAmenity.deleted_at.is_(None))
            if status:
                query = query.filter(DBAmenity.status == status)

            # --- Scope-aware filtering logic ---
            if building_id is not None and condominium_id is None:
                condominium_id = self._resolve_condominium_for_building(building_id)

            if condominium_id is not None and building_id is not None:
                # Building view: CONDOMINIUM amenities + BUILDING amenities for this building
                query = query.filter(
                    DBAmenity.condominium_id == condominium_id,
                    or_(
                        DBAmenity.scope == 'CONDOMINIUM',
                        and_(
                            DBAmenity.scope == 'BUILDING',
                            DBAmenity.building_id == building_id,
                        ),
                    ),
                )
            elif condominium_id is not None:
                # Condominium view: CONDOMINIUM scope only
                query = query.filter(
                    DBAmenity.condominium_id == condominium_id,
                    DBAmenity.scope == 'CONDOMINIUM',
                )
            # else: no filter on condominium (global admin view — returns everything)

            total = query.count()
            rows = query.order_by(DBAmenity.name.asc()).offset(skip).limit(limit).all()

            condo_names = self._fetch_condo_names(rows)
            building_names = self._fetch_building_names(rows)
            return self._bulk_enrich(rows, condo_names, building_names), total

    def list_active(
        self,
        condominium_id: int,
        building_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AmenityEntity], int]:
        logger.debug(
            f"Listing active amenities condo={condominium_id} building={building_id}"
        )
        with session_scope() as session:
            query = session.query(DBAmenity).filter(
                DBAmenity.condominium_id == condominium_id,
                DBAmenity.deleted_at.is_(None),
                DBAmenity.status == 'active',
            )

            if building_id is not None:
                # Building view: global + exclusive
                query = query.filter(
                    or_(
                        DBAmenity.scope == 'CONDOMINIUM',
                        and_(
                            DBAmenity.scope == 'BUILDING',
                            DBAmenity.building_id == building_id,
                        ),
                    ),
                )
            else:
                # Condominium view: global only
                query = query.filter(DBAmenity.scope == 'CONDOMINIUM')

            total = query.count()
            rows = query.order_by(DBAmenity.name.asc()).offset(skip).limit(limit).all()

            condo_names = self._fetch_condo_names(rows)
            building_names = self._fetch_building_names(rows)
            return self._bulk_enrich(rows, condo_names, building_names), total
