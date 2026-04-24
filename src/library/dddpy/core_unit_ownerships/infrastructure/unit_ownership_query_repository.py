from typing import Optional, List, Tuple
from sqlalchemy import func, and_

from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity
from library.dddpy.core_unit_ownerships.domain.unit_ownership_query_repository import UnitOwnershipQueryRepository
from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_mapper import UnitOwnershipMapper
from library.dddpy.core_users.infrastructure.dbuser import DBUser
from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOwnershipQueryRepository")


class UnitOwnershipQueryRepositoryImpl(UnitOwnershipQueryRepository):

    def __init__(self):
        logger.info("UnitOwnershipQueryRepositoryImpl initialized")

    def _bulk_enrich(self, rows: List[DBUnitOwnership]) -> List[UnitOwnershipEntity]:
        """Apply unit + building + condo + user enrichment to a list of ownership rows."""
        if not rows:
            return []

        unit_ids = list({r.unit_id for r in rows})
        user_ids = list({r.user_id for r in rows})

        with session_scope() as session:
            users = {u.id: u for u in session.query(DBUser).filter(DBUser.id.in_(user_ids)).all()}
            units = {u.id: u for u in session.query(DBUnits).filter(DBUnits.id.in_(unit_ids)).all()}
            building_ids = list({u.building_id for u in units.values() if u.building_id})
            buildings = {}
            if building_ids:
                buildings = {b.id: b for b in session.query(DBBuildings).filter(DBBuildings.id.in_(building_ids)).all()}
            condo_ids = list({b.condominium_id for b in buildings.values() if b.condominium_id})
            condos = {}
            if condo_ids:
                condos = {c.id: c for c in session.query(DBCondominium).filter(DBCondominium.id.in_(condo_ids)).all()}

            result = []
            for row in rows:
                unit = units.get(row.unit_id)
                building = buildings.get(unit.building_id) if unit else None
                condo = condos.get(building.condominium_id) if building else None
                user = users.get(row.user_id)

                entity = UnitOwnershipMapper.to_domain_enriched(
                    row,
                    unit_code=unit.code if unit else None,
                    building_name=building.name if building else None,
                    condominium_name=condo.name if condo else None,
                    user_email=user.email if user else None,
                    user_full_name=(
                        f"{user.first_name} {user.last_name}".strip() if user else None
                    ),
                )
                result.append(entity)
            return result

    def get_by_id(self, id: int) -> Optional[UnitOwnershipEntity]:
        logger.debug(f"Fetching unit ownership by id={id}")
        with session_scope() as session:
            db_ownership = (
                session.query(DBUnitOwnership)
                .filter(
                    DBUnitOwnership.id == id,
                    DBUnitOwnership.deleted_at.is_(None),
                )
                .first()
            )
            if not db_ownership:
                return None
            enriched = self._bulk_enrich([db_ownership])
            return enriched[0] if enriched else None

    def get_by_uuid(self, uuid: str) -> Optional[UnitOwnershipEntity]:
        logger.debug(f"Fetching unit ownership by uuid={uuid}")
        with session_scope() as session:
            db_ownership = (
                session.query(DBUnitOwnership)
                .filter(
                    DBUnitOwnership.uuid == uuid,
                    DBUnitOwnership.deleted_at.is_(None),
                )
                .first()
            )
            if not db_ownership:
                return None
            enriched = self._bulk_enrich([db_ownership])
            return enriched[0] if enriched else None

    def get_active_by_unit_and_user(
        self, unit_id: int, user_id: int
    ) -> Optional[UnitOwnershipEntity]:
        logger.debug(
            f"Fetching active unit ownership by unit_id={unit_id}, user_id={user_id}"
        )
        with session_scope() as session:
            db_ownership = (
                session.query(DBUnitOwnership)
                .filter(
                    and_(
                        DBUnitOwnership.unit_id == unit_id,
                        DBUnitOwnership.user_id == user_id,
                        DBUnitOwnership.status == "active",
                        DBUnitOwnership.deleted_at.is_(None),
                    )
                )
                .first()
            )
            if not db_ownership:
                return None
            enriched = self._bulk_enrich([db_ownership])
            return enriched[0] if enriched else None

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        logger.debug(
            f"Listing unit ownerships skip={skip} limit={limit} "
            f"unit_id={unit_id} user_id={user_id}"
        )
        with session_scope() as session:
            query = session.query(DBUnitOwnership)

            if not include_deleted:
                query = query.filter(DBUnitOwnership.deleted_at.is_(None))
            if unit_id is not None:
                query = query.filter(DBUnitOwnership.unit_id == unit_id)
            if user_id is not None:
                query = query.filter(DBUnitOwnership.user_id == user_id)
            if ownership_type is not None:
                query = query.filter(DBUnitOwnership.ownership_type == ownership_type)
            if status is not None:
                query = query.filter(DBUnitOwnership.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBUnitOwnership.unit_id, DBUnitOwnership.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        logger.debug(f"Listing unit ownerships for unit_id={unit_id}")
        with session_scope() as session:
            query = session.query(DBUnitOwnership).filter(
                DBUnitOwnership.unit_id == unit_id
            )

            if not include_deleted:
                query = query.filter(DBUnitOwnership.deleted_at.is_(None))
            if ownership_type is not None:
                query = query.filter(DBUnitOwnership.ownership_type == ownership_type)
            if status is not None:
                query = query.filter(DBUnitOwnership.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBUnitOwnership.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        logger.debug(f"Listing unit ownerships for user_id={user_id}")
        with session_scope() as session:
            query = session.query(DBUnitOwnership).filter(
                DBUnitOwnership.user_id == user_id
            )

            if not include_deleted:
                query = query.filter(DBUnitOwnership.deleted_at.is_(None))
            if ownership_type is not None:
                query = query.filter(DBUnitOwnership.ownership_type == ownership_type)
            if status is not None:
                query = query.filter(DBUnitOwnership.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBUnitOwnership.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def _get_by_id_any_status(self, id: int) -> Optional[UnitOwnershipEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching unit ownership by id={id} (any status)")
        with session_scope() as session:
            db_ownership = (
                session.query(DBUnitOwnership)
                .filter(DBUnitOwnership.id == id)
                .first()
            )
            if not db_ownership:
                return None
            enriched = self._bulk_enrich([db_ownership])
            return enriched[0] if enriched else None
