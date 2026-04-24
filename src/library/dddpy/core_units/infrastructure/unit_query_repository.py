from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy import func, and_, text

from library.dddpy.core_units.domain.unit_entity import UnitEntity
from library.dddpy.core_units.domain.unit_query_repository import UnitQueryRepository
from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from library.dddpy.core_units.infrastructure.unit_mapper import UnitMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitQueryRepository")


class UnitQueryRepositoryImpl(UnitQueryRepository):

    def __init__(self):
        logger.info("UnitQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[UnitEntity]:
        logger.debug(f"Fetching unit by id={id}")
        with session_scope() as session:
            db_unit = (
                session.query(DBUnits)
                .filter(
                    DBUnits.id == id,
                    DBUnits.deleted_at.is_(None),
                )
                .first()
            )
            if not db_unit:
                return None
            return UnitMapper.to_domain(db_unit)

    def get_by_uuid(self, uuid: str) -> Optional[UnitEntity]:
        logger.debug(f"Fetching unit by uuid={uuid}")
        with session_scope() as session:
            db_unit = (
                session.query(DBUnits)
                .filter(
                    DBUnits.uuid == uuid,
                    DBUnits.deleted_at.is_(None),
                )
                .first()
            )
            if not db_unit:
                return None
            return UnitMapper.to_domain(db_unit)

    def get_by_unit_number_in_building(
        self, building_id: int, unit_number: str
    ) -> Optional[UnitEntity]:
        logger.debug(
            f"Fetching unit by unit_number={unit_number} in building_id={building_id}"
        )
        with session_scope() as session:
            db_unit = (
                session.query(DBUnits)
                .filter(
                    and_(
                        DBUnits.building_id == building_id,
                        DBUnits.unit_number == unit_number,
                        DBUnits.deleted_at.is_(None),
                    )
                )
                .first()
            )
            if not db_unit:
                return None
            return UnitMapper.to_domain(db_unit)

    def get_by_code_in_building(
        self, building_id: int, code: str
    ) -> Optional[UnitEntity]:
        logger.debug(f"Fetching unit by code={code} in building_id={building_id}")
        with session_scope() as session:
            db_unit = (
                session.query(DBUnits)
                .filter(
                    and_(
                        DBUnits.building_id == building_id,
                        DBUnits.code == code,
                        DBUnits.deleted_at.is_(None),
                    )
                )
                .first()
            )
            if not db_unit:
                return None
            return UnitMapper.to_domain(db_unit)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unit_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitEntity], int]:
        logger.debug(
            f"Listing units skip={skip} limit={limit} building_id={building_id}"
        )
        with session_scope() as session:
            query = session.query(DBUnits)

            if not include_deleted:
                query = query.filter(DBUnits.deleted_at.is_(None))
            if building_id is not None:
                query = query.filter(DBUnits.building_id == building_id)
            if unit_type_id is not None:
                query = query.filter(DBUnits.unit_type_id == unit_type_id)
            if occupancy_status is not None:
                query = query.filter(DBUnits.occupancy_status == occupancy_status)
            if status is not None:
                query = query.filter(DBUnits.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBUnits.building_id, DBUnits.sort_order)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [UnitMapper.to_domain(u) for u in results], total

    def list_by_building(
        self,
        building_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitEntity], int]:
        logger.debug(f"Listing units for building_id={building_id}")
        with session_scope() as session:
            query = session.query(DBUnits).filter(
                DBUnits.building_id == building_id
            )

            if not include_deleted:
                query = query.filter(DBUnits.deleted_at.is_(None))
            if occupancy_status is not None:
                query = query.filter(DBUnits.occupancy_status == occupancy_status)
            if status is not None:
                query = query.filter(DBUnits.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBUnits.sort_order)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [UnitMapper.to_domain(u) for u in results], total

    def list_units_for_buildings(
        self,
        skip: int = 0,
        limit: int = 100,
        building_ids: Optional[List[int]] = None,
        building_id: Optional[int] = None,
        unit_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitEntity], int]:
        """
        List units filtered to specific building_ids (RBAC scope).
        building_ids=None means use building_id single filter.
        """
        logger.debug(
            f"Listing units for building_ids={building_ids}, "
            f"building_id={building_id}, skip={skip}, limit={limit}"
        )
        with session_scope() as session:
            query = session.query(DBUnits)

            if not include_deleted:
                query = query.filter(DBUnits.deleted_at.is_(None))

            if building_ids is not None:
                if not building_ids:
                    # Empty scope → return nothing
                    return [], 0
                query = query.filter(DBUnits.building_id.in_(building_ids))
            elif building_id is not None:
                query = query.filter(DBUnits.building_id == building_id)

            if unit_type_id is not None:
                query = query.filter(DBUnits.unit_type_id == unit_type_id)
            if occupancy_status is not None:
                query = query.filter(DBUnits.occupancy_status == occupancy_status)
            if status is not None:
                query = query.filter(DBUnits.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBUnits.building_id, DBUnits.sort_order)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [UnitMapper.to_domain(u) for u in results], total

    def count_active_residents(self, unit_id: int) -> int:
        """Count active residents for a unit. Returns 0 if table doesn't exist yet."""
        logger.debug(f"Counting active residents for unit_id={unit_id}")
        try:
            with session_scope() as session:
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

                count_result = session.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM users_residents
                    WHERE unity_id = :unit_id
                      AND status = 1
                      AND deleted_at IS NULL
                    """,
                    {"unit_id": unit_id},
                )
                return count_result.scalar() or 0
        except Exception as e:
            logger.warning(f"Could not count residents for unit {unit_id}: {e}")
            return 0

    def _get_by_id_any_status(self, id: int) -> Optional[UnitEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching unit by id={id} (any status)")
        with session_scope() as session:
            db_unit = session.query(DBUnits).filter(DBUnits.id == id).first()
            if not db_unit:
                return None
            return UnitMapper.to_domain(db_unit)

    def get_stats_per_building(self, building_ids: List[int]) -> Dict[int, Dict[str, Any]]:
        """
        Compute aggregated unit statistics per building.
        Returns a dict: {building_id: {built_area, coefficient_sum,
                                      condominium_coefficient_sum, units_count,
                                      floors_count, basements_count}}
        Active units only (status=1, deleted_at IS NULL).
        """
        logger.info(f"Computing unit stats for {len(building_ids)} buildings")
        if not building_ids:
            return {}
        stats: Dict[int, Dict[str, Any]] = {bid: {
            "built_area": 0.0,
            "coefficient_sum": 0.0,
            "condominium_coefficient_sum": 0.0,
            "units_count": 0,
            "floors_count": 0,
            "basements_count": 0,
        } for bid in building_ids}

        try:
            with session_scope() as session:
                result = session.execute(
                    text("""
                        SELECT
                            building_id,
                            COUNT(*) as units_count,
                            COALESCE(SUM(private_area), 0) as built_area,
                            COALESCE(SUM(coefficient), 0) as coefficient_sum,
                            COALESCE(SUM(condominium_coefficient), 0) as ccoeff_sum,
                            COUNT(DISTINCT CASE WHEN floor_number IS NOT NULL AND floor_number >= 0 THEN floor_number END) as floors_count,
                            COUNT(DISTINCT CASE WHEN floor_number IS NOT NULL AND floor_number < 0 THEN floor_number END) as basements_count
                        FROM core_units
                        WHERE building_id IN :building_ids
                          AND status = 1
                          AND deleted_at IS NULL
                        GROUP BY building_id
                    """),
                    {"building_ids": tuple(building_ids)}
                )
                for row in result:
                    bid = row[0]
                    if bid in stats:
                        stats[bid] = {
                            "built_area": float(row[2]) if row[2] else 0.0,
                            "coefficient_sum": float(row[3]) if row[3] else 0.0,
                            "condominium_coefficient_sum": float(row[4]) if row[4] else 0.0,
                            "units_count": int(row[1]) if row[1] else 0,
                            "floors_count": int(row[5]) if row[5] else 0,
                            "basements_count": int(row[6]) if row[6] else 0,
                        }
        except Exception as e:
            logger.warning(f"Could not compute unit stats: {e}")
        return stats

    def get_condominium_stats(self, condominium_id: int) -> Dict[str, Any]:
        """
        Compute aggregated stats across all buildings in a condominium.
        Returns: {built_area, coefficient_sum, condominium_coefficient_sum, units_count}
        """
        logger.info(f"Computing stats for condominium_id={condominium_id}")
        try:
            with session_scope() as session:
                result = session.execute(
                    text("""
                        SELECT
                            COUNT(u.id) as units_count,
                            COALESCE(SUM(u.private_area), 0) as built_area,
                            COALESCE(SUM(u.coefficient), 0) as coefficient_sum,
                            COALESCE(SUM(u.condominium_coefficient), 0) as ccoeff_sum
                        FROM core_units u
                        JOIN core_buildings b ON u.building_id = b.id
                        WHERE b.condominium_id = :condo_id
                          AND u.status = 1
                          AND u.deleted_at IS NULL
                          AND b.deleted_at IS NULL
                    """),
                    {"condo_id": condominium_id}
                )
                row = result.first()
                if row:
                    return {
                        "built_area": float(row[1]) if row[1] else 0.0,
                        "coefficient_sum": float(row[2]) if row[2] else 0.0,
                        "condominium_coefficient_sum": float(row[3]) if row[3] else 0.0,
                        "units_count": int(row[0]) if row[0] else 0,
                    }
        except Exception as e:
            logger.warning(f"Could not compute condominium stats: {e}")
        return {
            "built_area": 0.0,
            "coefficient_sum": 0.0,
            "condominium_coefficient_sum": 0.0,
            "units_count": 0,
        }