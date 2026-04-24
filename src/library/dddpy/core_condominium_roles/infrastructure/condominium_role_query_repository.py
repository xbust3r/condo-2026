from typing import Optional, List, Tuple
from sqlalchemy import and_

from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity
from library.dddpy.core_condominium_roles.domain.condominium_role_query_repository import CondominiumRoleQueryRepository
from library.dddpy.core_condominium_roles.infrastructure.dbcondominium_role import DBCondominiumRoles
from library.dddpy.core_condominium_roles.infrastructure.condominium_role_mapper import CondominiumRoleMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumRoleQueryRepository")


class CondominiumRoleQueryRepositoryImpl(CondominiumRoleQueryRepository):

    def __init__(self):
        logger.info("CondominiumRoleQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[CondominiumRoleEntity]:
        logger.debug(f"Fetching condominium role by id={id}")
        with session_scope() as session:
            db_role = (
                session.query(DBCondominiumRoles)
                .filter(
                    DBCondominiumRoles.id == id,
                    DBCondominiumRoles.deleted_at.is_(None),
                )
                .first()
            )
            if not db_role:
                return None
            return CondominiumRoleMapper.to_domain(db_role)

    def get_by_uuid(self, uuid: str) -> Optional[CondominiumRoleEntity]:
        logger.debug(f"Fetching condominium role by uuid={uuid}")
        with session_scope() as session:
            db_role = (
                session.query(DBCondominiumRoles)
                .filter(
                    DBCondominiumRoles.uuid == uuid,
                    DBCondominiumRoles.deleted_at.is_(None),
                )
                .first()
            )
            if not db_role:
                return None
            return CondominiumRoleMapper.to_domain(db_role)

    def get_active_by_user_and_condominium(
        self, user_id: int, condominium_id: int
    ) -> Optional[CondominiumRoleEntity]:
        logger.debug(
            f"Fetching active role for user_id={user_id} in condominium_id={condominium_id}"
        )
        with session_scope() as session:
            db_role = (
                session.query(DBCondominiumRoles)
                .filter(
                    and_(
                        DBCondominiumRoles.user_id == user_id,
                        DBCondominiumRoles.condominium_id == condominium_id,
                        DBCondominiumRoles.status == "active",
                        DBCondominiumRoles.deleted_at.is_(None),
                    )
                )
                .first()
            )
            if not db_role:
                return None
            return CondominiumRoleMapper.to_domain(db_role)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        user_id: Optional[int] = None,
        role: Optional[str] = None,
        scope: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        logger.debug(
            f"Listing condominium roles skip={skip} limit={limit} "
            f"condominium_id={condominium_id} user_id={user_id} scope={scope}"
        )
        with session_scope() as session:
            query = session.query(DBCondominiumRoles)

            if not include_deleted:
                query = query.filter(DBCondominiumRoles.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBCondominiumRoles.condominium_id == condominium_id)
            if user_id is not None:
                query = query.filter(DBCondominiumRoles.user_id == user_id)
            if role is not None:
                query = query.filter(DBCondominiumRoles.role == role)
            if scope is not None:
                query = query.filter(DBCondominiumRoles.scope == scope)
            if status is not None:
                query = query.filter(DBCondominiumRoles.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBCondominiumRoles.condominium_id, DBCondominiumRoles.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [CondominiumRoleMapper.to_domain(r) for r in results], total

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        logger.debug(f"Listing condominium roles for condominium_id={condominium_id}")
        with session_scope() as session:
            query = session.query(DBCondominiumRoles).filter(
                DBCondominiumRoles.condominium_id == condominium_id
            )

            if not include_deleted:
                query = query.filter(DBCondominiumRoles.deleted_at.is_(None))
            if role is not None:
                query = query.filter(DBCondominiumRoles.role == role)
            if status is not None:
                query = query.filter(DBCondominiumRoles.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBCondominiumRoles.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [CondominiumRoleMapper.to_domain(r) for r in results], total

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        logger.debug(f"Listing condominium roles for user_id={user_id}")
        with session_scope() as session:
            query = session.query(DBCondominiumRoles).filter(
                DBCondominiumRoles.user_id == user_id
            )

            if not include_deleted:
                query = query.filter(DBCondominiumRoles.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBCondominiumRoles.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBCondominiumRoles.condominium_id, DBCondominiumRoles.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [CondominiumRoleMapper.to_domain(r) for r in results], total

    def _get_by_id_any_status(self, id: int) -> Optional[CondominiumRoleEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching condominium role by id={id} (any status)")
        with session_scope() as session:
            db_role = session.query(DBCondominiumRoles).filter(DBCondominiumRoles.id == id).first()
            if not db_role:
                return None
            return CondominiumRoleMapper.to_domain(db_role)
