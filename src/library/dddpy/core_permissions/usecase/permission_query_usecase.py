"""
Permission Query UseCase.
"""
from typing import Optional, List

from library.dddpy.core_permissions.domain.permission_entity import PermissionEntity
from library.dddpy.core_permissions.domain.permission_exception import PermissionNotFound
from library.dddpy.core_permissions.domain.permission_query_repository import PermissionQueryRepository
from library.dddpy.core_permissions.infrastructure.permission_query_repository import PermissionQueryRepositoryImpl
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PermissionQueryUseCase")


class PermissionQueryUseCase:

    def __init__(self, repository: Optional[PermissionQueryRepository] = None) -> None:
        self._repository = repository or PermissionQueryRepositoryImpl()
        logger.info("PermissionQueryUseCase initialized")

    def get_by_id(self, id: int) -> PermissionEntity:
        logger.debug(f"Getting permission by id={id}")
        entity = self._repository.get_by_id(id)
        if not entity:
            logger.warning(f"Permission not found by id={id}")
            raise PermissionNotFound(id)
        return entity

    def get_by_code(self, code: str) -> PermissionEntity:
        logger.debug(f"Getting permission by code={code}")
        entity = self._repository.get_by_code(code)
        if not entity:
            logger.warning(f"Permission not found by code={code}")
            raise PermissionNotFound(code)
        return entity

    def list_all(self, skip: int = 0, limit: int = 100) -> tuple[List[PermissionEntity], int]:
        logger.debug(f"Listing all permissions skip={skip} limit={limit}")
        if limit > 500:
            limit = 500
        return self._repository.list_all(skip=skip, limit=limit)

    def list_by_resource(
        self, resource: str, skip: int = 0, limit: int = 100
    ) -> tuple[List[PermissionEntity], int]:
        logger.debug(f"Listing permissions for resource={resource}")
        if limit > 500:
            limit = 500
        return self._repository.list_by_resource(resource=resource, skip=skip, limit=limit)

    def list_by_action(
        self, action: str, skip: int = 0, limit: int = 100
    ) -> tuple[List[PermissionEntity], int]:
        logger.debug(f"Listing permissions for action={action}")
        if limit > 500:
            limit = 500
        return self._repository.list_by_action(action=action, skip=skip, limit=limit)
