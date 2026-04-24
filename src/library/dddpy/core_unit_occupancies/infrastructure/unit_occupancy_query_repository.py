from typing import Optional, List, Tuple
from sqlalchemy import func, and_

from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_query_repository import UnitOccupancyQueryRepository
from library.dddpy.core_unit_occupancies.infrastructure.dbunit_occupancy import DBUnitOccupancy
from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_mapper import UnitOccupancyMapper
from library.dddpy.core_occupancy_types.infrastructure.dboccupancy_type import DBOccupancyType
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOccupancyQueryRepository")


class UnitOccupancyQueryRepositoryImpl(UnitOccupancyQueryRepository):

    def __init__(self):
        logger.info("UnitOccupancyQueryRepositoryImpl initialized")

    def _enrich(self, db_occ: DBUnitOccupancy, db_occ_type: DBOccupancyType) -> UnitOccupancyEntity:
        """Apply catalog enrichment to a unit occupancy entity."""
        return UnitOccupancyMapper.to_domain_enriched(
            db_occ,
            code=db_occ_type.code,
            name=db_occ_type.name,
            requires_auth=bool(db_occ_type.requires_authorization),
            allows_primary=bool(db_occ_type.allows_primary),
        )

    def get_by_id(self, id: int) -> Optional[UnitOccupancyEntity]:
        logger.debug(f"Fetching unit occupancy by id={id}")
        with session_scope() as session:
            row = (
                session.query(DBUnitOccupancy)
                .filter(
                    DBUnitOccupancy.id == id,
                    DBUnitOccupancy.deleted_at.is_(None),
                )
                .first()
            )
            if not row:
                return None
            # Fetch the related occupancy type
            occ_type = session.query(DBOccupancyType).filter(DBOccupancyType.id == row.occupancy_type_id).first()
            if occ_type:
                return self._enrich(row, occ_type)
            return UnitOccupancyMapper.to_domain(row)

    def get_by_uuid(self, uuid: str) -> Optional[UnitOccupancyEntity]:
        logger.debug(f"Fetching unit occupancy by uuid={uuid}")
        with session_scope() as session:
            row = (
                session.query(DBUnitOccupancy)
                .filter(
                    DBUnitOccupancy.uuid == uuid,
                    DBUnitOccupancy.deleted_at.is_(None),
                )
                .first()
            )
            if not row:
                return None
            occ_type = session.query(DBOccupancyType).filter(DBOccupancyType.id == row.occupancy_type_id).first()
            if occ_type:
                return self._enrich(row, occ_type)
            return UnitOccupancyMapper.to_domain(row)

    def get_active_by_unit_and_user(
        self, unit_id: int, user_id: int
    ) -> Optional[UnitOccupancyEntity]:
        logger.debug(
            f"Fetching active occupancy by unit_id={unit_id}, user_id={user_id}"
        )
        with session_scope() as session:
            row = (
                session.query(DBUnitOccupancy)
                .filter(
                    and_(
                        DBUnitOccupancy.unit_id == unit_id,
                        DBUnitOccupancy.user_id == user_id,
                        DBUnitOccupancy.status == "active",
                        DBUnitOccupancy.deleted_at.is_(None),
                    )
                )
                .first()
            )
            if not row:
                return None
            occ_type = session.query(DBOccupancyType).filter(DBOccupancyType.id == row.occupancy_type_id).first()
            if occ_type:
                return self._enrich(row, occ_type)
            return UnitOccupancyMapper.to_domain(row)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        logger.debug(
            f"Listing unit occupancies skip={skip} limit={limit} unit_id={unit_id}"
        )
        with session_scope() as session:
            query = session.query(DBUnitOccupancy)

            if not include_deleted:
                query = query.filter(DBUnitOccupancy.deleted_at.is_(None))
            if unit_id is not None:
                query = query.filter(DBUnitOccupancy.unit_id == unit_id)
            if user_id is not None:
                query = query.filter(DBUnitOccupancy.user_id == user_id)
            if occupancy_type_id is not None:
                query = query.filter(DBUnitOccupancy.occupancy_type_id == occupancy_type_id)
            if status is not None:
                query = query.filter(DBUnitOccupancy.status == status)
            if is_primary is not None:
                query = query.filter(DBUnitOccupancy.is_primary == is_primary)

            total = query.count()
            results = (
                query
                .order_by(DBUnitOccupancy.unit_id, DBUnitOccupancy.id)
                .offset(skip)
                .limit(limit)
                .all()
            )

            # Bulk fetch occupancy types for enrichment
            occ_type_ids = list({r.occupancy_type_id for r in results})
            occ_types_map = {}
            if occ_type_ids:
                occ_types = session.query(DBOccupancyType).filter(DBOccupancyType.id.in_(occ_type_ids)).all()
                occ_types_map = {ot.id: ot for ot in occ_types}

            entities = []
            for row in results:
                occ_type = occ_types_map.get(row.occupancy_type_id)
                if occ_type:
                    entities.append(self._enrich(row, occ_type))
                else:
                    entities.append(UnitOccupancyMapper.to_domain(row))
            return entities, total

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        logger.debug(f"Listing occupancies for unit_id={unit_id}")
        with session_scope() as session:
            query = session.query(DBUnitOccupancy).filter(
                DBUnitOccupancy.unit_id == unit_id
            )

            if not include_deleted:
                query = query.filter(DBUnitOccupancy.deleted_at.is_(None))
            if occupancy_type_id is not None:
                query = query.filter(DBUnitOccupancy.occupancy_type_id == occupancy_type_id)
            if status is not None:
                query = query.filter(DBUnitOccupancy.status == status)
            if is_primary is not None:
                query = query.filter(DBUnitOccupancy.is_primary == is_primary)

            total = query.count()
            results = (
                query
                .order_by(DBUnitOccupancy.id)
                .offset(skip)
                .limit(limit)
                .all()
            )

            # Bulk fetch occupancy types for enrichment
            occ_type_ids = list({r.occupancy_type_id for r in results})
            occ_types_map = {}
            if occ_type_ids:
                occ_types = session.query(DBOccupancyType).filter(DBOccupancyType.id.in_(occ_type_ids)).all()
                occ_types_map = {ot.id: ot for ot in occ_types}

            entities = []
            for row in results:
                occ_type = occ_types_map.get(row.occupancy_type_id)
                if occ_type:
                    entities.append(self._enrich(row, occ_type))
                else:
                    entities.append(UnitOccupancyMapper.to_domain(row))
            return entities, total

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        logger.debug(f"Listing occupancies for user_id={user_id}")
        with session_scope() as session:
            query = session.query(DBUnitOccupancy).filter(
                DBUnitOccupancy.user_id == user_id
            )

            if not include_deleted:
                query = query.filter(DBUnitOccupancy.deleted_at.is_(None))
            if occupancy_type_id is not None:
                query = query.filter(DBUnitOccupancy.occupancy_type_id == occupancy_type_id)
            if status is not None:
                query = query.filter(DBUnitOccupancy.status == status)
            if is_primary is not None:
                query = query.filter(DBUnitOccupancy.is_primary == is_primary)

            total = query.count()
            results = (
                query
                .order_by(DBUnitOccupancy.id)
                .offset(skip)
                .limit(limit)
                .all()
            )

            # Bulk fetch occupancy types for enrichment
            occ_type_ids = list({r.occupancy_type_id for r in results})
            occ_types_map = {}
            if occ_type_ids:
                occ_types = session.query(DBOccupancyType).filter(DBOccupancyType.id.in_(occ_type_ids)).all()
                occ_types_map = {ot.id: ot for ot in occ_types}

            entities = []
            for row in results:
                occ_type = occ_types_map.get(row.occupancy_type_id)
                if occ_type:
                    entities.append(self._enrich(row, occ_type))
                else:
                    entities.append(UnitOccupancyMapper.to_domain(row))
            return entities, total

    def count_active_by_unit(self, unit_id: int) -> int:
        """Count active occupancy records for a unit."""
        logger.debug(f"Counting active occupancies for unit_id={unit_id}")
        with session_scope() as session:
            count_result = (
                session.query(DBUnitOccupancy)
                .filter(
                    DBUnitOccupancy.unit_id == unit_id,
                    DBUnitOccupancy.status == "active",
                    DBUnitOccupancy.deleted_at.is_(None),
                )
                .count()
            )
            return count_result

    def _get_by_id_any_status(self, id: int) -> Optional[UnitOccupancyEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching unit occupancy by id={id} (any status)")
        with session_scope() as session:
            row = (
                session.query(DBUnitOccupancy)
                .filter(DBUnitOccupancy.id == id)
                .first()
            )
            if not row:
                return None
            occ_type = session.query(DBOccupancyType).filter(DBOccupancyType.id == row.occupancy_type_id).first()
            if occ_type:
                return self._enrich(row, occ_type)
            return UnitOccupancyMapper.to_domain(row)
