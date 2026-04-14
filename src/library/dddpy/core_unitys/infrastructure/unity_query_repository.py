from typing import Optional, List, Tuple
from sqlalchemy import func, and_

from library.dddpy.core_unitys.domain.unity_entity import UnityEntity
from library.dddpy.core_unitys.domain.unity_query_repository import UnityQueryRepository
from library.dddpy.core_unitys.infrastructure.dbunitys import DBUnitys
from library.dddpy.core_unitys.infrastructure.unity_mapper import UnityMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityQueryRepository")


class UnityQueryRepositoryImpl(UnityQueryRepository):

    def __init__(self):
        logger.info("UnityQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[UnityEntity]:
        logger.debug(f"Fetching unity by id={id}")
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(DBUnitys.id == id).first()
            if not db_unity:
                return None
            return UnityMapper.to_domain(db_unity)

    def get_by_uuid(self, uuid: str) -> Optional[UnityEntity]:
        logger.debug(f"Fetching unity by uuid={uuid}")
        with session_scope() as session:
            db_unity = (
                session.query(DBUnitys)
                .filter(DBUnitys.uuid == uuid)
                .first()
            )
            if not db_unity:
                return None
            return UnityMapper.to_domain(db_unity)

    def get_by_unit_number_in_building(
        self, building_id: int, unit_number: str
    ) -> Optional[UnityEntity]:
        logger.debug(
            f"Fetching unity by unit_number={unit_number} in building_id={building_id}"
        )
        with session_scope() as session:
            db_unity = (
                session.query(DBUnitys)
                .filter(
                    and_(
                        DBUnitys.building_id == building_id,
                        DBUnitys.unit_number == unit_number,
                    )
                )
                .first()
            )
            if not db_unity:
                return None
            return UnityMapper.to_domain(db_unity)

    def get_by_code_in_building(
        self, building_id: int, code: str
    ) -> Optional[UnityEntity]:
        logger.debug(f"Fetching unity by code={code} in building_id={building_id}")
        with session_scope() as session:
            db_unity = (
                session.query(DBUnitys)
                .filter(
                    and_(
                        DBUnitys.building_id == building_id,
                        DBUnitys.code == code,
                    )
                )
                .first()
            )
            if not db_unity:
                return None
            return UnityMapper.to_domain(db_unity)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unity_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnityEntity], int]:
        logger.debug(
            f"Listing unities skip={skip} limit={limit} building_id={building_id}"
        )
        with session_scope() as session:
            query = session.query(DBUnitys)

            if not include_deleted:
                query = query.filter(DBUnitys.deleted_at.is_(None))
            if building_id is not None:
                query = query.filter(DBUnitys.building_id == building_id)
            if unity_type_id is not None:
                query = query.filter(DBUnitys.unity_type_id == unity_type_id)
            if occupancy_status is not None:
                query = query.filter(DBUnitys.occupancy_status == occupancy_status)
            if status is not None:
                query = query.filter(DBUnitys.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBUnitys.building_id, DBUnitys.sort_order)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [UnityMapper.to_domain(u) for u in results], total

    def list_by_building(
        self,
        building_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnityEntity], int]:
        logger.debug(f"Listing unities for building_id={building_id}")
        with session_scope() as session:
            query = session.query(DBUnitys).filter(
                DBUnitys.building_id == building_id
            )

            if not include_deleted:
                query = query.filter(DBUnitys.deleted_at.is_(None))
            if occupancy_status is not None:
                query = query.filter(DBUnitys.occupancy_status == occupancy_status)
            if status is not None:
                query = query.filter(DBUnitys.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBUnitys.sort_order)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [UnityMapper.to_domain(u) for u in results], total

    def count_active_residents(self, unity_id: int) -> int:
        """Count active residents for a unity. Returns 0 if table doesn't exist yet."""
        logger.debug(f"Counting active residents for unity_id={unity_id}")
        try:
            with session_scope() as session:
                # Check if the table exists first
                result = session.execute(
                    """
                    SELECT COUNT(*)
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = 'users_residents'
                    """
                )
                if result.scalar() == 0:
                    logger.debug("users_residents table does not exist yet, returning 0")
                    return 0

                # Count active (status=1, deleted_at IS NULL) residents for this unity
                count_result = session.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM users_residents
                    WHERE unity_id = :unity_id
                      AND status = 1
                      AND deleted_at IS NULL
                    """,
                    {"unity_id": unity_id},
                )
                return count_result.scalar() or 0
        except Exception as e:
            logger.warning(f"Could not count residents for unity {unity_id}: {e}")
            return 0
