from typing import List, Optional, Tuple

from sqlalchemy import and_, or_, func

from library.dddpy.core_unities_types.domain.unity_type_query_repository import (
    UnityTypeQueryRepository,
)
from library.dddpy.core_unities_types.domain.unity_type_entity import UnityTypeEntity
from library.dddpy.core_unities_types.infrastructure.dbunitytype import DBUnityType
from library.dddpy.core_unities_types.infrastructure.unity_type_mapper import (
    UnityTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityTypeQueryRepository")


class UnityTypeQueryRepositoryImpl(UnityTypeQueryRepository):

    def __init__(self):
        logger.info("UnityTypeQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[UnityTypeEntity]:
        logger.info(f"Fetching unity type by id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnityType).filter(
                DBUnityType.id == id,
                DBUnityType.deleted_at.is_(None),
            ).first()
            if not db_type:
                logger.warning(f"Unity type not found by id={id}")
                return None
            return UnityTypeMapper.to_domain(db_type)

    def get_by_uuid(self, uuid: str) -> Optional[UnityTypeEntity]:
        logger.info(f"Fetching unity type by uuid={uuid}")
        with session_scope() as session:
            db_type = session.query(DBUnityType).filter(
                DBUnityType.uuid == uuid,
                DBUnityType.deleted_at.is_(None),
            ).first()
            if not db_type:
                logger.warning(f"Unity type not found by uuid={uuid}")
                return None
            return UnityTypeMapper.to_domain(db_type)

    def get_by_code_in_scope(
        self,
        condominium_id: Optional[int],
        code: str,
    ) -> Optional[UnityTypeEntity]:
        scope_desc = "global" if condominium_id is None else f"condominium {condominium_id}"
        logger.info(f"Fetching unity type code={code} in scope={scope_desc}")

        with session_scope() as session:
            query = session.query(DBUnityType).filter(
                DBUnityType.code == code,
                DBUnityType.deleted_at.is_(None),
            )

            if condominium_id is None:
                query = query.filter(DBUnityType.condominium_id.is_(None))
            else:
                query = query.filter(DBUnityType.condominium_id == condominium_id)

            db_type = query.first()
            if not db_type:
                logger.warning(f"Unity type not found code={code} in scope={scope_desc}")
                return None
            return UnityTypeMapper.to_domain(db_type)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        include_system: bool = True,
        status: Optional[int] = None,
        usage_class: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnityTypeEntity], int]:
        logger.info(
            f"Listing unity types (skip={skip}, limit={limit}, "
            f"condominium_id={condominium_id}, include_system={include_system}, "
            f"status={status}, usage_class={usage_class}, include_deleted={include_deleted})"
        )
        with session_scope() as session:
            query = session.query(DBUnityType)

            if not include_deleted:
                query = query.filter(DBUnityType.deleted_at.is_(None))

            # Scope filter: return global types + optionally types for this condo
            if condominium_id is not None:
                if include_system:
                    query = query.filter(
                        or_(
                            DBUnityType.condominium_id.is_(None),
                            DBUnityType.condominium_id == condominium_id,
                        )
                    )
                else:
                    query = query.filter(
                        DBUnityType.condominium_id == condominium_id
                    )
            elif not include_system:
                # Global request with system types excluded: only custom
                query = query.filter(DBUnityType.condominium_id.isnot(None))

            if status is not None:
                query = query.filter(DBUnityType.status == status)

            if usage_class is not None:
                query = query.filter(DBUnityType.usage_class == usage_class)

            total = query.count()
            db_types = (
                query
                .order_by(DBUnityType.sort_order.asc(), DBUnityType.id.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [UnityTypeMapper.to_domain(t) for t in db_types], total

    def count_references(self, type_id: int) -> int:
        """Count how many active unities reference this type."""
        logger.info(f"Counting unity references for type_id={type_id}")
        with session_scope() as session:
            from sqlalchemy import text
            count = session.execute(
                text(
                    "SELECT COUNT(*) FROM core_unities "
                    "WHERE unity_type_id = :type_id AND deleted_at IS NULL"
                ),
                {"type_id": type_id},
            ).scalar()
            logger.info(f"References for type_id={type_id}: {count}")
            return count or 0

    def get_active_in_scope(
        self,
        type_id: int,
        condominium_id: int,
    ) -> Optional[UnityTypeEntity]:
        """
        Get a unity type if it's active and accessible in scope.
        - Must not be soft-deleted
        - Must have status=1
        - Must be global (condominium_id IS NULL) or belong to the same condominium
        """
        logger.info(
            f"get_active_in_scope type_id={type_id}, condominium_id={condominium_id}"
        )
        with session_scope() as session:
            db_type = session.query(DBUnityType).filter(
                DBUnityType.id == type_id,
                DBUnityType.deleted_at.is_(None),
                DBUnityType.status == 1,
                or_(
                    DBUnityType.condominium_id.is_(None),
                    DBUnityType.condominium_id == condominium_id,
                ),
            ).first()
            if not db_type:
                logger.warning(
                    f"Unity type id={type_id} not accessible in scope={condominium_id}"
                )
                return None
            return UnityTypeMapper.to_domain(db_type)

    # ── Internal helpers for post-mutation re-fetch ──────────────────────────

    def _get_by_id_any_status(self, id: int) -> Optional[UnityTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Fetching unity type by id={id} (any status)")
        with session_scope() as session:
            db_type = session.query(DBUnityType).filter(
                DBUnityType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unity type not found by id={id}")
                return None
            return UnityTypeMapper.to_domain(db_type)
