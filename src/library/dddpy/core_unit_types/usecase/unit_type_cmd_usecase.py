from library.dddpy.core_unit_types.domain.unit_type_cmd_repository import (
    UnitTypeCmdRepository,
)
from library.dddpy.core_unit_types.domain.unit_type_data import (
    CreateUnitTypeData,
    UpdateUnitTypeData,
)
from library.dddpy.core_unit_types.domain.unit_type_query_repository import (
    UnitTypeQueryRepository,
)
from library.dddpy.core_unit_types.domain.unit_type_exception import (
    DuplicateUnitTypeCode,
    UnitTypeIsSystem,
    UnitTypeIsInUse,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitTypeCmdUseCase")


class UnitTypeCmdUseCase:
    """Use case for write operations on unit types."""

    def __init__(self, cmd_repo: UnitTypeCmdRepository, query_repo: UnitTypeQueryRepository):
        self._cmd = cmd_repo
        self._query = query_repo
        logger.info("UnitTypeCmdUseCase initialized")

    def create(self, data: CreateUnitTypeData) -> None:
        logger.add_inside_method("create")

        # Check for duplicate in the same scope (active only)
        existing = self._query.get_by_code_in_scope(data.condominium_id, data.code)
        if existing:
            scope = "global" if data.condominium_id is None else f"condominium {data.condominium_id}"
            logger.warning(f"Duplicate code={data.code} in scope={scope}")
            raise DuplicateUnitTypeCode(code=data.code, scope=scope)

        return self._cmd.create(data)

    def update(self, id: int, data: UpdateUnitTypeData) -> None:
        logger.add_inside_method("update")

        # Verify type exists and is active
        existing = self._query.get_by_id(id)
        if not existing:
            from library.dddpy.core_unit_types.domain.unit_type_exception import (
                UnitTypeNotFound,
            )
            raise UnitTypeNotFound()

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
            from library.dddpy.core_unit_types.domain.unit_type_exception import (
                UnitTypeNotFound,
            )
            raise UnitTypeNotFound()

        # Check references
        ref_count = self._query.count_references(id)
        if ref_count > 0:
            logger.warning(f"Unit type id={id} has {ref_count} unit references")
            raise UnitTypeIsInUse(id)

        return self._cmd.hard_delete(id)