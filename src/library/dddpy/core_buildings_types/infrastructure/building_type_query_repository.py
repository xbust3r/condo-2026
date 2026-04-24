from typing import Optional
from typing import List, Optional, Tuple

from sqlalchemy import and_, or_, func

from library.dddpy.core_buildings_types.domain.building_type_query_repository import (
    BuildingTypeQueryRepository,
)
from library.dddpy.core_buildings_types.domain.building_type_entity import BuildingTypeEntity
from library.dddpy.core_buildings_types.infrastructure.dbbuildingtype import DBBuildingType
from library.dddpy.core_buildings_types.infrastructure.building_type_mapper import (
    BuildingTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingTypeQueryRepository")


class BuildingTypeQueryRepositoryImpl(BuildingTypeQueryRepository):

    def __init__(self):
        logger.info("BuildingTypeQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[BuildingTypeEntity]:
        logger.info(f"Fetching building type by id={id}")
        with session_scope() as session:
            db_type = session.query(DBBuildingType).filter(
                DBBuildingType.id == id,
                DBBuildingType.deleted_at.is_(None),
            ).first()
            if not db_type:
                logger.warning(f"Building type not found by id={id}")
                return None
            return BuildingTypeMapper.to_domain(db_type)

    def get_by_uuid(self, uuid: str) -> Optional[BuildingTypeEntity]:
        logger.info(f"Fetching building type by uuid={uuid}")
        with session_scope() as session:
            db_type = session.query(DBBuildingType).filter(
                DBBuildingType.uuid == uuid,
                DBBuildingType.deleted_at.is_(None),
            ).first()
            if not db_type:
                logger.warning(f"Building type not found by uuid={uuid}")
                return None
            return BuildingTypeMapper.to_domain(db_type)

    def get_by_code_in_scope(
        self,
        condominium_id: Optional[int],
        code: str,
    ) -> Optional[BuildingTypeEntity]:
        """Find an active type by (condominium_id, code).
        
        condominium_id=None searches global types only.
        condominium_id=[id] searches custom types for that condominium.
        """
        scope_desc = "global" if condominium_id is None else f"condominium {condominium_id}"
        logger.info(f"Fetching building type code={code} in scope={scope_desc}")

        with session_scope() as session:
            query = session.query(DBBuildingType).filter(
                DBBuildingType.code == code,
                DBBuildingType.deleted_at.is_(None),
            )

            if condominium_id is None:
                query = query.filter(DBBuildingType.condominium_id.is_(None))
            else:
                query = query.filter(DBBuildingType.condominium_id == condominium_id)

            db_type = query.first()
            if not db_type:
                logger.warning(f"Building type not found code={code} in scope={scope_desc}")
                return None
            return BuildingTypeMapper.to_domain(db_type)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        include_system: bool = True,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[BuildingTypeEntity], int]:
        logger.info(
            f"Listing building types (skip={skip}, limit={limit}, "
            f"condominium_id={condominium_id}, include_system={include_system}, "
            f"status={status}, include_deleted={include_deleted})"
        )
        with session_scope() as session:
            query = session.query(DBBuildingType)

            if not include_deleted:
                query = query.filter(DBBuildingType.deleted_at.is_(None))

            # Scope filter: return global types + optionally types for this condo
            if condominium_id is not None:
                # Include global (condominium_id IS NULL) + custom for this condo
                # But exclude global if include_system=False
                if include_system:
                    query = query.filter(
                        or_(
                            DBBuildingType.condominium_id.is_(None),
                            DBBuildingType.condominium_id == condominium_id,
                        )
                    )
                else:
                    # Only custom types for the given condominium
                    query = query.filter(
                        DBBuildingType.condominium_id == condominium_id
                    )
            elif not include_system:
                # Global request (no specific condo) and system types excluded: only custom
                query = query.filter(DBBuildingType.condominium_id.isnot(None))

            if status is not None:
                query = query.filter(DBBuildingType.status == status)

            total = query.count()
            db_types = (
                query
                .order_by(DBBuildingType.sort_order.asc(), DBBuildingType.id.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [BuildingTypeMapper.to_domain(t) for t in db_types], total

    def count_references(self, type_id: int) -> int:
        """Count how many active buildings reference this type."""
        logger.info(f"Counting building references for type_id={type_id}")
        with session_scope() as session:
            from sqlalchemy import text
            count = session.execute(
                text(
                    "SELECT COUNT(*) FROM core_buildings "
                    "WHERE building_type_id = :type_id AND deleted_at IS NULL"
                ),
                {"type_id": type_id},
            ).scalar()
            logger.info(f"References for type_id={type_id}: {count}")
            return count or 0

    def get_active_in_scope(
        self,
        type_id: int,
        condominium_id: int,
    ) -> Optional[BuildingTypeEntity]:
        """
        Get a building type if it's active and accessible in scope.
        - Must not be soft-deleted
        - Must have status=1
        - Must be global (condominium_id IS NULL) or belong to the same condominium
        """
        logger.info(
            f"get_active_in_scope type_id={type_id}, condominium_id={condominium_id}"
        )
        with session_scope() as session:
            db_type = session.query(DBBuildingType).filter(
                DBBuildingType.id == type_id,
                DBBuildingType.deleted_at.is_(None),
                DBBuildingType.status == 1,
                or_(
                    DBBuildingType.condominium_id.is_(None),
                    DBBuildingType.condominium_id == condominium_id,
                ),
            ).first()
            if not db_type:
                logger.warning(
                    f"Building type id={type_id} not accessible in scope={condominium_id}"
                )
                return None
            return BuildingTypeMapper.to_domain(db_type)

    # ── Internal helpers for post-mutation re-fetch ──────────────────────────

    def _get_by_id_any_status(self, id: int) -> Optional[BuildingTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Fetching building type by id={id} (any status)")
        with session_scope() as session:
            db_type = session.query(DBBuildingType).filter(
                DBBuildingType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Building type not found by id={id}")
                return None
            return BuildingTypeMapper.to_domain(db_type)
