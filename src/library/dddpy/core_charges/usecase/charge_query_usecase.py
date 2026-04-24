"""
Charge query use case — handles reads.
"""
from typing import List, Optional, Tuple

from library.dddpy.core_charges.domain.charge_query_repository import ChargeQueryRepository
from library.dddpy.core_charges.domain.charge_entity import ChargeEntity
from library.dddpy.core_charges.infrastructure.charge_query_repository import (
    ChargeQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeQueryUseCase")


class ChargeQueryUseCase:
    def __init__(self, query_repo: Optional[ChargeQueryRepository] = None):
        self._repo = query_repo or ChargeQueryRepositoryImpl()
        logger.info("ChargeQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[ChargeEntity]:
        return self._repo.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[ChargeEntity]:
        return self._repo.get_by_uuid(uuid)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        charge_type_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        status: Optional[str] = None,
        is_recurrent: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeEntity], int]:
        return self._repo.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            charge_type_id=charge_type_id,
            unit_id=unit_id,
            status=status,
            is_recurrent=is_recurrent,
            include_deleted=include_deleted,
        )

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        is_recurrent: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeEntity], int]:
        return self._repo.list_by_condominium(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            status=status,
            is_recurrent=is_recurrent,
            include_deleted=include_deleted,
        )

    def _get_by_id_any_status(self, id: int) -> Optional[ChargeEntity]:
        return self._repo._get_by_id_any_status(id)


_charge_query_usecase_instance: Optional[ChargeQueryUseCase] = None


def charge_query_usecase_factory() -> ChargeQueryUseCase:
    global _charge_query_usecase_instance
    if _charge_query_usecase_instance is None:
        _charge_query_usecase_instance = ChargeQueryUseCase()
    return _charge_query_usecase_instance
