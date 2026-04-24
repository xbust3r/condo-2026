"""
OccupancyType query repository implementation — SQLAlchemy.
"""
from typing import List, Optional, Tuple

from sqlalchemy import func

from library.dddpy.core_occupancy_types.domain.occupancy_type_query_repository import (
    OccupancyTypeQueryRepository,
)
from library.dddpy.core_occupancy_types.domain.occupancy_type_entity import OccupancyTypeEntity
from library.dddpy.core_occupancy_types.infrastructure.dboccupancy_type import DBOccupancyType
from library.dddpy.core_occupancy_types.infrastructure.occupancy_type_mapper import (
    OccupancyTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("OccupancyTypeQueryRepository")


class OccupancyTypeQueryRepositoryImpl(OccupancyTypeQueryRepository):

    def __init__(self):
        logger.info("OccupancyTypeQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[OccupancyTypeEntity]:
        logger.info(f"Fetching occupancy type by id={id}")
        with session_scope() as session:
            db_ot = session.query(DBOccupancyType).filter(
                DBOccupancyType.id == id,
                DBOccupancyType.deleted_at.is_(None),
            ).first()
            if not db_ot:
                logger.warning(f"Occupancy type not found by id={id}")
                return None
            return OccupancyTypeMapper.to_domain(db_ot)

    def get_by_uuid(self, uuid: str) -> Optional[OccupancyTypeEntity]:
        logger.info(f"Fetching occupancy type by uuid={uuid}")
        with session_scope() as session:
            db_ot = session.query(DBOccupancyType).filter(
                DBOccupancyType.uuid == uuid,
                DBOccupancyType.deleted_at.is_(None),
            ).first()
            if not db_ot:
                logger.warning(f"Occupancy type not found by uuid={uuid}")
                return None
            return OccupancyTypeMapper.to_domain(db_ot)

    def get_by_code(self, code: str) -> Optional[OccupancyTypeEntity]:
        logger.info(f"Fetching occupancy type by code={code}")
        with session_scope() as session:
            db_ot = session.query(DBOccupancyType).filter(
                DBOccupancyType.code == code,
                DBOccupancyType.deleted_at.is_(None),
            ).first()
            if not db_ot:
                logger.warning(f"Occupancy type not found by code={code}")
                return None
            return OccupancyTypeMapper.to_domain(db_ot)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[OccupancyTypeEntity], int]:
        logger.info(
            f"Listing occupancy types (skip={skip}, limit={limit}, "
            f"is_active={is_active}, include_deleted={include_deleted})"
        )
        with session_scope() as session:
            query = session.query(DBOccupancyType)

            if not include_deleted:
                query = query.filter(DBOccupancyType.deleted_at.is_(None))

            if is_active is not None:
                query = query.filter(DBOccupancyType.is_active == int(is_active))

            total = query.count()
            db_types = (
                query
                .order_by(DBOccupancyType.sort_order.asc(), DBOccupancyType.id.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [OccupancyTypeMapper.to_domain(t) for t in db_types], total

    def _get_by_id_any_status(self, id: int) -> Optional[OccupancyTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Fetching occupancy type by id={id} (any status)")
        with session_scope() as session:
            db_ot = session.query(DBOccupancyType).filter(
                DBOccupancyType.id == id
            ).first()
            if not db_ot:
                logger.warning(f"Occupancy type not found by id={id}")
                return None
            return OccupancyTypeMapper.to_domain(db_ot)