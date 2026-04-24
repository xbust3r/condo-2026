from typing import Optional
from typing import Optional, List
from sqlalchemy import and_, func, text

from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
from library.dddpy.core_buildings.domain.building_query_repository import BuildingQueryRepository
from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
from library.dddpy.core_buildings.infrastructure.building_mapper import BuildingMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingQueryRepository")


class BuildingQueryRepositoryImpl(BuildingQueryRepository):

    def __init__(self):
        logger.info("BuildingQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[BuildingEntity]:
        logger.info(f"Fetching building by id={id}")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.id == id,
                DBBuildings.deleted_at.is_(None)
            ).first()
            if not db_building:
                logger.warning(f"Building not found by id={id}")
                return None
            return BuildingMapper.to_domain(db_building)

    def get_by_uuid(self, uuid: str) -> Optional[BuildingEntity]:
        logger.info(f"Fetching building by uuid={uuid}")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.uuid == uuid,
                DBBuildings.deleted_at.is_(None)
            ).first()
            if not db_building:
                logger.warning(f"Building not found by uuid={uuid}")
                return None
            return BuildingMapper.to_domain(db_building)

    def get_by_code_in_condominium(self, condominium_id: int, code: str) -> Optional[BuildingEntity]:
        logger.info(f"Fetching building by code={code} in condominium_id={condominium_id}")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                and_(
                    DBBuildings.condominium_id == condominium_id,
                    DBBuildings.code == code,
                    DBBuildings.deleted_at.is_(None)
                )
            ).first()
            if not db_building:
                logger.warning(f"Building not found by code={code} in condominium_id={condominium_id}")
                return None
            return BuildingMapper.to_domain(db_building)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        building_type_id: Optional[int] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[BuildingEntity], int]:
        logger.info(
            f"Fetching buildings (skip={skip}, limit={limit}, "
            f"condominium_id={condominium_id}, building_type_id={building_type_id}, "
            f"status={status}, include_deleted={include_deleted})"
        )
        with session_scope() as session:
            query = session.query(DBBuildings)

            if not include_deleted:
                query = query.filter(DBBuildings.deleted_at.is_(None))

            if condominium_id is not None:
                query = query.filter(DBBuildings.condominium_id == condominium_id)
            if building_type_id is not None:
                query = query.filter(DBBuildings.building_type_id == building_type_id)
            if status is not None:
                query = query.filter(DBBuildings.status == status)

            total = query.count()
            db_buildings = query.offset(skip).limit(limit).all()
            return [BuildingMapper.to_domain(b) for b in db_buildings], total

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[BuildingEntity], int]:
        logger.info(f"Fetching buildings for condominium_id={condominium_id} (skip={skip}, limit={limit})")
        with session_scope() as session:
            query = session.query(DBBuildings).filter(DBBuildings.condominium_id == condominium_id)

            if not include_deleted:
                query = query.filter(DBBuildings.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBBuildings.status == status)

            total = query.count()
            db_buildings = query.order_by(DBBuildings.sort_order.asc()).offset(skip).limit(limit).all()
            return [BuildingMapper.to_domain(b) for b in db_buildings], total

    def count_active_units(self, building_id: int) -> int:
        """Count active units for a building.
        
        Uses raw SQL to avoid circular dependency with core_unities module.
        Active = status=1 AND deleted_at IS NULL.
        Returns 0 if core_unities table doesn't exist yet.
        """
        logger.info(f"Counting active units for building_id={building_id}")
        try:
            with session_scope() as session:
                # Raw SQL to avoid import of core_unities that may not exist yet
                result = session.execute(
                    text("SELECT COUNT(*) FROM core_units WHERE building_id = :building_id AND status = 1 AND deleted_at IS NULL"),
                    {"building_id": building_id}
                )
                count = result.scalar() or 0
                logger.info(f"Active units count for building_id={building_id}: {count}")
                return count
        except Exception as e:
            # Table may not exist yet (core_unities not built)
            logger.warning(f"Could not count active units for building_id={building_id}: {e}")
            return 0

    # ── Internal helpers for post-mutation re-fetch ──────────────────────────

    def _get_by_id_any_status(self, id: int) -> Optional[BuildingEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Fetching building by id={id} (any status)")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.id == id
            ).first()
            if not db_building:
                logger.warning(f"Building not found by id={id}")
                return None
            return BuildingMapper.to_domain(db_building)

    def get_building_ids_by_condominiums(
        self,
        condominium_ids: List[int],
    ) -> List[int]:
        """Get all building IDs belonging to given condominium_ids."""
        logger.info(f"Fetching building IDs for condominium_ids={condominium_ids}")
        if not condominium_ids:
            return []
        with session_scope() as session:
            results = (
                session.query(DBBuildings.id)
                .filter(
                    DBBuildings.condominium_id.in_(condominium_ids),
                    DBBuildings.deleted_at.is_(None),
                )
                .all()
            )
            return [r[0] for r in results]