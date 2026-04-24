"""
AccountsReceivable query use case — handles reads.
"""
from typing import List, Optional, Tuple

from library.dddpy.core_accounts_receivable.domain.ar_query_repository import ARQueryRepository
from library.dddpy.core_accounts_receivable.domain.ar_entity import AREntity
from library.dddpy.core_accounts_receivable.infrastructure.ar_query_repository import (
    ARQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ARQueryUseCase")


class ARQueryUseCase:
    def __init__(self, query_repo: Optional[ARQueryRepository] = None):
        self._repo = query_repo or ARQueryRepositoryImpl()
        logger.info("ARQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[AREntity]:
        return self._repo.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[AREntity]:
        return self._repo.get_by_uuid(uuid)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        debtor_user_id: Optional[int] = None,
        status: Optional[str] = None,
        charge_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[AREntity], int]:
        return self._repo.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            unit_id=unit_id,
            debtor_user_id=debtor_user_id,
            status=status,
            charge_id=charge_id,
            include_deleted=include_deleted,
        )

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[AREntity], int]:
        return self._repo.list_by_unit(
            unit_id=unit_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def list_overdue(
        self,
        condominium_id: int,
        as_of_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AREntity], int]:
        return self._repo.list_overdue(
            condominium_id=condominium_id,
            as_of_date=as_of_date,
            skip=skip,
            limit=limit,
        )

    def get_summary_by_unit(self, unit_id: int) -> dict:
        return self._repo.get_summary_by_unit(unit_id)

    def _get_by_id_any_status(self, id: int) -> Optional[AREntity]:
        return self._repo._get_by_id_any_status(id)


_ar_query_usecase_instance: Optional[ARQueryUseCase] = None


def ar_query_usecase_factory() -> ARQueryUseCase:
    global _ar_query_usecase_instance
    if _ar_query_usecase_instance is None:
        _ar_query_usecase_instance = ARQueryUseCase()
    return _ar_query_usecase_instance
