"""
from typing import Optional
Charge command use case — handles writes.
"""
from typing import Optional

from library.dddpy.core_charges.domain.charge_cmd_repository import ChargeCmdRepository
from library.dddpy.core_charges.domain.charge_data import (
    CreateChargeData,
    UpdateChargeData,
)
from library.dddpy.core_charges.domain.charge_entity import ChargeEntity
from library.dddpy.core_charges.infrastructure.charge_cmd_repository import (
    ChargeCmdRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeCmdUseCase")


class ChargeCmdUseCase:
    def __init__(self, cmd_repo: Optional[ChargeCmdRepository] = None):
        self._repo = cmd_repo or ChargeCmdRepositoryImpl()
        logger.info("ChargeCmdUseCase initialized")

    def create(self, data: CreateChargeData) -> ChargeEntity:
        return self._repo.create(data)

    def update(self, id: int, data: UpdateChargeData) -> ChargeEntity:
        return self._repo.update(id, data)

    def soft_delete(self, id: int) -> bool:
        return self._repo.soft_delete(id)

    def restore(self, id: int) -> bool:
        return self._repo.restore(id)

    def hard_delete(self, id: int) -> bool:
        return self._repo.hard_delete(id)


_charge_cmd_usecase_instance: Optional[ChargeCmdUseCase] = None


def charge_cmd_usecase_factory() -> ChargeCmdUseCase:
    global _charge_cmd_usecase_instance
    if _charge_cmd_usecase_instance is None:
        _charge_cmd_usecase_instance = ChargeCmdUseCase()
    return _charge_cmd_usecase_instance
