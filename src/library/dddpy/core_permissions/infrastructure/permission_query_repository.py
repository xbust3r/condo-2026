"""
from typing import Optional
Permission Query Repository Implementation.
"""
from typing import Optional, List, Tuple

from library.dddpy.core_permissions.domain.permission_entity import PermissionEntity
from library.dddpy.core_permissions.domain.permission_query_repository import PermissionQueryRepository
from library.dddpy.core_permissions.infrastructure.dbpermission import DBBPermissions
from library.dddpy.core_permissions.infrastructure.permission_mapper import PermissionMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PermissionQueryRepository")


class PermissionQueryRepositoryImpl(PermissionQueryRepository):

    def __init__(self) -> None:
        logger.info("PermissionQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[PermissionEntity]:
        logger.debug(f"Fetching permission by id={id}")
        with session_scope() as session:
            db_perm = session.query(DBBPermissions).filter(
                DBBPermissions.id == id,
            ).first()
            if not db_perm:
                return None
            return PermissionMapper.to_domain(db_perm)

    def get_by_code(self, code: str) -> Optional[PermissionEntity]:
        logger.debug(f"Fetching permission by code={code}")
        with session_scope() as session:
            db_perm = session.query(DBBPermissions).filter(
                DBBPermissions.code == code,
            ).first()
            if not db_perm:
                return None
            return PermissionMapper.to_domain(db_perm)

    def list_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[PermissionEntity], int]:
        logger.debug(f"Listing permissions skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBBPermissions)
            total = query.count()
            results = query.order_by(DBBPermissions.id).offset(skip).limit(limit).all()
            return [PermissionMapper.to_domain(p) for p in results], total

    def list_by_resource(
        self, resource: str, skip: int = 0, limit: int = 100
    ) -> Tuple[List[PermissionEntity], int]:
        logger.debug(f"Listing permissions by resource={resource}")
        with session_scope() as session:
            query = session.query(DBBPermissions).filter(DBBPermissions.resource == resource)
            total = query.count()
            results = query.order_by(DBBPermissions.id).offset(skip).limit(limit).all()
            return [PermissionMapper.to_domain(p) for p in results], total

    def list_by_action(
        self, action: str, skip: int = 0, limit: int = 100
    ) -> Tuple[List[PermissionEntity], int]:
        logger.debug(f"Listing permissions by action={action}")
        with session_scope() as session:
            query = session.query(DBBPermissions).filter(DBBPermissions.action == action)
            total = query.count()
            results = query.order_by(DBBPermissions.id).offset(skip).limit(limit).all()
            return [PermissionMapper.to_domain(p) for p in results], total
