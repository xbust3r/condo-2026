from typing import List, Optional, Tuple

from sqlalchemy import and_, or_, func

from library.dddpy.core_unit_types.domain.unit_type_query_repository import (
    UnitTypeQueryRepository,
)
from library.dddpy.core_unit_types.domain.unit_type_entity import UnitTypeEntity
from library.dddpy.core_unit_types.infrastructure.dbunit_type import DBUnitType
from library.dddpy.core_unit_types.infrastructure.unit_type_mapper import (
    UnitTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitTypeQueryRepository")


class UnitTypeQueryRepositoryImpl(UnitTypeQueryRepository):

    def __init__(self):
        logger.info("UnitTypeQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[UnitTypeEntity]:
        logger.info(f"Fetching unit type by id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnitType).filter(
                DBUnitType.id == id,
                DBUnitType.deleted_at.is_(None),
            ).first()
            if not db_type:
                logger.warning(f"Unit type not found by id={id}")
                return None
            return UnitTypeMapper.to_domain(db_type)

    def get_by_uuid(self, uuid: str) -> Optional[UnitTypeEntity]:
        logger.info(f"Fetching unit type by uuid={uuid}")
        with session_scope() as session:
            db_type = session.query(DBUnitType).filter(
                DBUnitType.uuid == uuid,
                DBUnitType.deleted_at.is_(None),
            ).first()
            if not db_type:
                logger.warning(f"Unit type not found by uuid={uuid}")
                return None
            return UnitTypeMapper.to_domain(db_type)

    def get_by_code_in_scope(
        self,
        condominium_id: Optional[int],
        code: str,
    ) -> Optional[UnitTypeEntity]:
        scope_desc = "global" if condominium_id is None else f"condominium {condominium_id}"
        logger.info(f"Fetching unit type code={code} in scope={scope_desc}")

        with session_scope() as session:
            query = session.query(DBUnitType).filter(
                DBUnitType.code == code,
                DBUnitType.deleted_at.is_(None),
            )

            if condominium_id is None:
                query = query.filter(DBUnitType.condominium_id.is_(None))
            else:
                query = query.filter(DBUnitType.condominium_id == condominium_id)

            db_type = query.first()
            if not db_type:
                logger.warning(f"Unit type not found code={code} in scope={scope_desc}")
                return None
            return UnitTypeMapper.to_domain(db_type)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        include_system: bool = True,
        status: Optional[int] = None,
        usage_class: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitTypeEntity], int]:
        logger.info(
            f"Listing unit types (skip={skip}, limit={limit}, "
            f"condominium_id={condominium_id}, include_system={include_system}, "
            f"status={status}, usage_class={usage_class}, include_deleted={include_deleted})"
        )
        with session_scope() as session:
            query = session.query(DBUnitType)

            if not include_deleted:
                query = query.filter(DBUnitType.deleted_at.is_(None))

            # Scope filter: return global types + optionally types for this condo
            if condominium_id is not None:
                if include_system:
                    query = query.filter(
                        or_(
                            DBUnitType.condominium_id.is_(None),
                            DBUnitType.condominium_id == condominium_id,
                        )
                    )
                else:
                    query = query.filter(
                        DBUnitType.condominium_id == condominium_id
                    )
            elif not include_system:
                # Global request with system types excluded: only custom
                query = query.filter(DBUnitType.condominium_id.isnot(None))

            if status is not None:
                query = query.filter(DBUnitType.status == status)

            if usage_class is not None:
                query = query.filter(DBUnitType.usage_class == usage_class)

            total = query.count()
            db_types = (
                query
                .order_by(DBUnitType.sort_order.asc(), DBUnitType.id.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [UnitTypeMapper.to_domain(t) for t in db_types], total

    def count_references(self, type_id: int) -> int:
        """Count how many active units reference this type."""
        logger.info(f"Counting unit references for type_id={type_id}")
        with session_scope() as session:
            from sqlalchemy import text
            count = session.execute(
                text(
                    "SELECT COUNT(*) FROM core_units "
                    "WHERE unit_type_id = :type_id AND deleted_at IS NULL"
                ),
                {"type_id": type_id},
            ).scalar()
            logger.info(f"References for type_id={type_id}: {count}")
            return count or 0

    def get_active_in_scope(
        self,
        type_id: int,
        condominium_id: int,
    ) -> Optional[UnitTypeEntity]:
        """
        Get a unit type if it's active and accessible in scope.
        - Must not be soft-deleted
        - Must have status=1
        - Must be global (condominium_id IS NULL) or belong to the same condominium
        """
        logger.info(
            f"get_active_in_scope type_id={type_id}, condominium_id={condominium_id}"
        )
        with session_scope() as session:
            db_type = session.query(DBUnitType).filter(
                DBUnitType.id == type_id,
                DBUnitType.deleted_at.is_(None),
                DBUnitType.status == 1,
                or_(
                    DBUnitType.condominium_id.is_(None),
                    DBUnitType.condominium_id == condominium_id,
                ),
            ).first()
            if not db_type:
                logger.warning(
                    f"Unit type id={type_id} not accessible in scope={condominium_id}"
                )
                return None
            return UnitTypeMapper.to_domain(db_type)

    def _get_by_id_any_status(self, id: int) -> Optional[UnitTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Fetching unit type by id={id} (any status)")
        with session_scope() as session:
            db_type = session.query(DBUnitType).filter(
                DBUnitType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unit type not found by id={id}")
                return None
            return UnitTypeMapper.to_domain(db_type)