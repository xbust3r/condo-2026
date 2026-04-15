from typing import Optional, Tuple, List

from library.dddpy.core_unit_types.domain.unit_type_query_repository import (
    UnitTypeQueryRepository,
)
from library.dddpy.core_unit_types.domain.unit_type_entity import UnitTypeEntity
from library.dddpy.core_unit_types.domain.unit_type_exception import (
    UnitTypeNotFound,
    UnitTypeIsInactive,
    UnitTypeIsDeleted,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitTypeQueryUseCase")


class UnitTypeQueryUseCase:
    """Use case for read operations on unit types."""

    def __init__(self, query_repo: UnitTypeQueryRepository):
        self._query = query_repo
        logger.info("UnitTypeQueryUseCase initialized")

    def get_by_id(self, id: int) -> UnitTypeEntity:
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        if not entity:
            raise UnitTypeNotFound()
        return entity

    def get_by_uuid(self, uuid: str) -> UnitTypeEntity:
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise UnitTypeNotFound()
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
    ) -> Tuple[List[UnitTypeEntity], int]:
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

    def get_active_for_unit_assignment(
        self,
        type_id: int,
        condominium_id: int,
    ) -> UnitTypeEntity:
        """
        Validate a unit_type_id for assignment to a unit.

        Rules:
        - Type must exist and not be soft-deleted
        - Type must be active (status=1)
        - Type must be global (condominium_id IS NULL) OR belong to the same condominium
        """
        logger.add_inside_method("get_active_for_unit_assignment")

        entity = self._query.get_active_in_scope(type_id, condominium_id)
        if not entity:
            # Distinguish not-found from not-accessible for better error messages
            exists = self._query.get_by_id(type_id)
            if not exists:
                raise UnitTypeNotFound()
            if exists.is_deleted():
                raise UnitTypeIsDeleted()
            if exists.status != 1:
                raise UnitTypeIsInactive()
            from library.dddpy.core_unit_types.domain.unit_type_exception import (
                UnitTypeNotAccessible,
            )
            raise UnitTypeNotAccessible()

        return entity

    def get_by_id_any_status(self, id: int) -> Optional[UnitTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Delegating unit type fetch by id={id} (any status)")
        return self._query._get_by_id_any_status(id)