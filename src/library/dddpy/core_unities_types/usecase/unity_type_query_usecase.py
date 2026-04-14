from typing import Optional, Tuple, List

from library.dddpy.core_unities_types.domain.unity_type_query_repository import (
    UnityTypeQueryRepository,
)
from library.dddpy.core_unities_types.domain.unity_type_entity import UnityTypeEntity
from library.dddpy.core_unities_types.domain.unity_type_exception import (
    UnityTypeNotFound,
    UnityTypeIsInactive,
    UnityTypeIsDeleted,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityTypeQueryUseCase")


class UnityTypeQueryUseCase:
    """Use case for read operations on unity types."""

    def __init__(self, query_repo: UnityTypeQueryRepository):
        self._query = query_repo
        logger.info("UnityTypeQueryUseCase initialized")

    def get_by_id(self, id: int) -> UnityTypeEntity:
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        if not entity:
            raise UnityTypeNotFound()
        return entity

    def get_by_uuid(self, uuid: str) -> UnityTypeEntity:
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise UnityTypeNotFound()
        return entity

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
        logger.add_inside_method("list_all")
        return self._query.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            include_system=include_system,
            status=status,
            usage_class=usage_class,
            include_deleted=include_deleted,
        )

    def get_active_for_unity_assignment(
        self,
        type_id: int,
        condominium_id: int,
    ) -> UnityTypeEntity:
        """
        Validate a unity_type_id for assignment to a unity.

        Rules:
        - Type must exist and not be soft-deleted
        - Type must be active (status=1)
        - Type must be global (condominium_id IS NULL) OR belong to the same condominium
        """
        logger.add_inside_method("get_active_for_unity_assignment")

        entity = self._query.get_active_in_scope(type_id, condominium_id)
        if not entity:
            # Distinguish not-found from not-accessible for better error messages
            exists = self._query.get_by_id(type_id)
            if not exists:
                raise UnityTypeNotFound()
            if exists.is_deleted():
                raise UnityTypeIsDeleted()
            if exists.status != 1:
                raise UnityTypeIsInactive()
            from library.dddpy.core_unities_types.domain.unity_type_exception import (
                UnityTypeNotAccessible,
            )
            raise UnityTypeNotAccessible()

        return entity

    def get_by_id_any_status(self, id: int) -> Optional[UnityTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Delegating unity type fetch by id={id} (any status)")
        return self._query._get_by_id_any_status(id)
