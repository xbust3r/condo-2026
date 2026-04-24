"""
from typing import Optional
ChargeType command use case — handles writes.
"""
from typing import Optional

from library.dddpy.core_charge_types.domain.charge_type_cmd_repository import (
    ChargeTypeCmdRepository,
)
from library.dddpy.core_charge_types.domain.charge_type_data import (
    CreateChargeTypeData,
    UpdateChargeTypeData,
)
from library.dddpy.core_charge_types.domain.charge_type_entity import ChargeTypeEntity
from library.dddpy.core_charge_types.infrastructure.charge_type_cmd_repository import (
    ChargeTypeCmdRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeTypeCmdUseCase")


class ChargeTypeCmdUseCase:
    def __init__(self, cmd_repo: Optional[ChargeTypeCmdRepository] = None):
        self._repo = cmd_repo or ChargeTypeCmdRepositoryImpl()
        logger.info("ChargeTypeCmdUseCase initialized")

    def create(self, data: CreateChargeTypeData) -> ChargeTypeEntity:
        return self._repo.create(data)

    def update(self, id: int, data: UpdateChargeTypeData) -> ChargeTypeEntity:
        return self._repo.update(id, data)

    def soft_delete(self, id: int) -> bool:
        return self._repo.soft_delete(id)

    def restore(self, id: int) -> bool:
        return self._repo.restore(id)

    def hard_delete(self, id: int) -> bool:
        return self._repo.hard_delete(id)


_charge_type_cmd_usecase_instance: Optional[ChargeTypeCmdUseCase] = None


def charge_type_cmd_usecase_factory() -> ChargeTypeCmdUseCase:
    global _charge_type_cmd_usecase_instance
    if _charge_type_cmd_usecase_instance is None:
        _charge_type_cmd_usecase_instance = ChargeTypeCmdUseCase()
    return _charge_type_cmd_usecase_instance
