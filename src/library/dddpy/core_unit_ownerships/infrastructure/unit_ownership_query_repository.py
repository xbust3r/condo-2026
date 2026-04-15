from typing import Optional, List, Tuple
from sqlalchemy import func, and_

from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity
from library.dddpy.core_unit_ownerships.domain.unit_ownership_query_repository import UnitOwnershipQueryRepository
from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_mapper import UnitOwnershipMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOwnershipQueryRepository")


class UnitOwnershipQueryRepositoryImpl(UnitOwnershipQueryRepository):

    def __init__(self):
        logger.info("UnitOwnershipQueryRepositoryImpl initialized")

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
            return UnitOwnershipMapper.to_domain(db_ownership)

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
            return UnitOwnershipMapper.to_domain(db_ownership)

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
            return UnitOwnershipMapper.to_domain(db_ownership)

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
            return [UnitOwnershipMapper.to_domain(o) for o in results], total

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
            return [UnitOwnershipMapper.to_domain(o) for o in results], total

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
            return [UnitOwnershipMapper.to_domain(o) for o in results], total

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
            return UnitOwnershipMapper.to_domain(db_ownership)
