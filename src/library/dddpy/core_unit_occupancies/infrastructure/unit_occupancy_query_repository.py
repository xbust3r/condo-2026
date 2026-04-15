from typing import Optional, List, Tuple
from sqlalchemy import func, and_

from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_query_repository import UnitOccupancyQueryRepository
from library.dddpy.core_unit_occupancies.infrastructure.dbunit_occupancy import DBUnitOccupancy
from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_mapper import UnitOccupancyMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOccupancyQueryRepository")


class UnitOccupancyQueryRepositoryImpl(UnitOccupancyQueryRepository):

    def __init__(self):
        logger.info("UnitOccupancyQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[UnitOccupancyEntity]:
        logger.debug(f"Fetching unit occupancy by id={id}")
        with session_scope() as session:
            db_occupancy = (
                session.query(DBUnitOccupancy)
                .filter(
                    DBUnitOccupancy.id == id,
                    DBUnitOccupancy.deleted_at.is_(None),
                )
                .first()
            )
            if not db_occupancy:
                return None
            return UnitOccupancyMapper.to_domain(db_occupancy)

    def get_by_uuid(self, uuid: str) -> Optional[UnitOccupancyEntity]:
        logger.debug(f"Fetching unit occupancy by uuid={uuid}")
        with session_scope() as session:
            db_occupancy = (
                session.query(DBUnitOccupancy)
                .filter(
                    DBUnitOccupancy.uuid == uuid,
                    DBUnitOccupancy.deleted_at.is_(None),
                )
                .first()
            )
            if not db_occupancy:
                return None
            return UnitOccupancyMapper.to_domain(db_occupancy)

    def get_active_by_unit_and_user(
        self, unit_id: int, user_id: int
    ) -> Optional[UnitOccupancyEntity]:
        logger.debug(
            f"Fetching active occupancy by unit_id={unit_id}, user_id={user_id}"
        )
        with session_scope() as session:
            db_occupancy = (
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
            if not db_occupancy:
                return None
            return UnitOccupancyMapper.to_domain(db_occupancy)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        occupancy_type: Optional[str] = None,
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
            if occupancy_type is not None:
                query = query.filter(DBUnitOccupancy.occupancy_type == occupancy_type)
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
            return [UnitOccupancyMapper.to_domain(o) for o in results], total

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type: Optional[str] = None,
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
            if occupancy_type is not None:
                query = query.filter(DBUnitOccupancy.occupancy_type == occupancy_type)
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
            return [UnitOccupancyMapper.to_domain(o) for o in results], total

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type: Optional[str] = None,
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
            if occupancy_type is not None:
                query = query.filter(DBUnitOccupancy.occupancy_type == occupancy_type)
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
            return [UnitOccupancyMapper.to_domain(o) for o in results], total

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
            db_occupancy = (
                session.query(DBUnitOccupancy)
                .filter(DBUnitOccupancy.id == id)
                .first()
            )
            if not db_occupancy:
                return None
            return UnitOccupancyMapper.to_domain(db_occupancy)
