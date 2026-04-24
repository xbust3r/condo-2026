"""
ChargeType query use case — handles reads.
"""
from typing import List, Optional, Tuple

from library.dddpy.core_charge_types.domain.charge_type_query_repository import (
    ChargeTypeQueryRepository,
)
from library.dddpy.core_charge_types.domain.charge_type_entity import ChargeTypeEntity
from library.dddpy.core_charge_types.infrastructure.charge_type_query_repository import (
    ChargeTypeQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeTypeQueryUseCase")


class ChargeTypeQueryUseCase:
    def __init__(self, query_repo: Optional[ChargeTypeQueryRepository] = None):
        self._repo = query_repo or ChargeTypeQueryRepositoryImpl()
        logger.info("ChargeTypeQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[ChargeTypeEntity]:
        return self._repo.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[ChargeTypeEntity]:
        return self._repo.get_by_uuid(uuid)

    def get_by_code(self, code: str) -> Optional[ChargeTypeEntity]:
        return self._repo.get_by_code(code)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeTypeEntity], int]:
        return self._repo.list_all(
            skip=skip,
            limit=limit,
            is_active=is_active,
            include_deleted=include_deleted,
        )

    def _get_by_id_any_status(self, id: int) -> Optional[ChargeTypeEntity]:
        return self._repo._get_by_id_any_status(id)


_charge_type_query_usecase_instance: Optional[ChargeTypeQueryUseCase] = None


def charge_type_query_usecase_factory() -> ChargeTypeQueryUseCase:
    global _charge_type_query_usecase_instance
    if _charge_type_query_usecase_instance is None:
        _charge_type_query_usecase_instance = ChargeTypeQueryUseCase()
    return _charge_type_query_usecase_instance
