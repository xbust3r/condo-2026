"""
from typing import Optional
AccountsReceivable command use case — handles writes.
"""
from typing import Optional

from library.dddpy.core_accounts_receivable.domain.ar_cmd_repository import ARCmdRepository
from library.dddpy.core_accounts_receivable.domain.ar_data import (
    CreateARData,
    UpdateARData,
)
from library.dddpy.core_accounts_receivable.domain.ar_entity import AREntity
from library.dddpy.core_accounts_receivable.infrastructure.ar_cmd_repository import (
    ARCmdRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ARCmdUseCase")


class ARCmdUseCase:
    def __init__(self, cmd_repo: Optional[ARCmdRepository] = None):
        self._repo = cmd_repo or ARCmdRepositoryImpl()
        logger.info("ARCmdUseCase initialized")

    def create(self, data: CreateARData) -> AREntity:
        return self._repo.create(data)

    def create_batch(self, entries: list[CreateARData]) -> list[AREntity]:
        return self._repo.create_batch(entries)

    def update(self, id: int, data: UpdateARData) -> Optional[AREntity]:
        return self._repo.update(id, data)

    def update_status(self, id: int, status: str) -> Optional[AREntity]:
        return self._repo.update_status(id, status)

    def add_payment(self, id: int, amount: float) -> Optional[AREntity]:
        return self._repo.add_payment(id, amount)

    def soft_delete(self, id: int) -> bool:
        return self._repo.soft_delete(id)

    def restore(self, id: int) -> bool:
        return self._repo.restore(id)

    def hard_delete(self, id: int) -> bool:
        return self._repo.hard_delete(id)


_ar_cmd_usecase_instance: Optional[ARCmdUseCase] = None


def ar_cmd_usecase_factory() -> ARCmdUseCase:
    global _ar_cmd_usecase_instance
    if _ar_cmd_usecase_instance is None:
        _ar_cmd_usecase_instance = ARCmdUseCase()
    return _ar_cmd_usecase_instance
