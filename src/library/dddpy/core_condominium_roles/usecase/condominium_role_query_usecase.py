from typing import Optional
from typing import Optional, List, Tuple

from library.dddpy.core_condominium_roles.domain.condominium_role_query_repository import CondominiumRoleQueryRepository
from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumRoleQueryUseCase")


class CondominiumRoleQueryUseCase:

    def __init__(self, repository: CondominiumRoleQueryRepository):
        self.repository = repository
        logger.info("CondominiumRoleQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[CondominiumRoleEntity]:
        logger.debug(f"Querying condominium role by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[CondominiumRoleEntity]:
        logger.debug(f"Querying condominium role by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def get_active_by_user_and_condominium(
        self, user_id: int, condominium_id: int
    ) -> Optional[CondominiumRoleEntity]:
        logger.debug(
            f"Querying active role for user_id={user_id} in condominium_id={condominium_id}"
        )
        return self.repository.get_active_by_user_and_condominium(user_id, condominium_id)

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
        logger.debug(f"Listing condominium roles skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            user_id=user_id,
            role=role,
            scope=scope,
            status=status,
            include_deleted=include_deleted,
        )

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
        return self.repository.list_by_condominium(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            role=role,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        logger.debug(f"Listing condominium roles for user_id={user_id}")
        return self.repository.list_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def _get_by_id_any_status(self, id: int) -> Optional[CondominiumRoleEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Delegating condominium role fetch by id={id} (any status)")
        return self.repository._get_by_id_any_status(id)
