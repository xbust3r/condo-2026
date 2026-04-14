from library.dddpy.core_unities_types.domain.unity_type_cmd_repository import (
    UnityTypeCmdRepository,
)
from library.dddpy.core_unities_types.domain.unity_type_data import (
    CreateUnityTypeData,
    UpdateUnityTypeData,
)
from library.dddpy.core_unities_types.domain.unity_type_query_repository import (
    UnityTypeQueryRepository,
)
from library.dddpy.core_unities_types.domain.unity_type_exception import (
    DuplicateUnityTypeCode,
    UnityTypeIsSystem,
    UnityTypeIsInUse,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityTypeCmdUseCase")


class UnityTypeCmdUseCase:
    """Use case for write operations on unity types."""

    def __init__(self, cmd_repo: UnityTypeCmdRepository, query_repo: UnityTypeQueryRepository):
        self._cmd = cmd_repo
        self._query = query_repo
        logger.info("UnityTypeCmdUseCase initialized")

    def create(self, data: CreateUnityTypeData) -> None:
        logger.add_inside_method("create")

        # Check for duplicate in the same scope (active only)
        existing = self._query.get_by_code_in_scope(data.condominium_id, data.code)
        if existing:
            scope = "global" if data.condominium_id is None else f"condominium {data.condominium_id}"
            logger.warning(f"Duplicate code={data.code} in scope={scope}")
            raise DuplicateUnityTypeCode(code=data.code, scope=scope)

        return self._cmd.create(data)

    def update(self, id: int, data: UpdateUnityTypeData) -> None:
        logger.add_inside_method("update")

        # Verify type exists and is active
        existing = self._query.get_by_id(id)
        if not existing:
            from library.dddpy.core_unities_types.domain.unity_type_exception import (
                UnityTypeNotFound,
            )
            raise UnityTypeNotFound()

        return self._cmd.update(id, data)

    def soft_delete(self, id: int) -> bool:
        logger.add_inside_method("soft_delete")
        return self._cmd.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.add_inside_method("restore")
        return self._cmd.restore(id)

    def hard_delete(self, id: int) -> bool:
        logger.add_inside_method("hard_delete")

        # Verify it exists
        existing = self._query.get_by_id(id)
        if not existing:
            from library.dddpy.core_unities_types.domain.unity_type_exception import (
                UnityTypeNotFound,
            )
            raise UnityTypeNotFound()

        # Check references
        ref_count = self._query.count_references(id)
        if ref_count > 0:
            logger.warning(f"Unity type id={id} has {ref_count} unity references")
            raise UnityTypeIsInUse(id)

        return self._cmd.hard_delete(id)
