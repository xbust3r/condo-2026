"""
from typing import Optional
Vote query use case — read operations.
"""
from typing import Optional, List, Tuple

from library.dddpy.core_votes.domain.vote_entity import VoteEntity
from library.dddpy.core_votes.domain.vote_query_repository import VoteQueryRepository
from library.dddpy.shared.logging.logging import Logger


logger = Logger("VoteQueryUseCase")


class VoteQueryUseCase:

    def __init__(self, repository: VoteQueryRepository):
        self.repository = repository
        logger.info("VoteQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[VoteEntity]:
        logger.debug(f"Querying vote by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[VoteEntity]:
        logger.debug(f"Querying vote by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        created_by_user_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VoteEntity], int]:
        logger.debug(f"Listing votes skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            status=status,
            created_by_user_id=created_by_user_id,
            include_deleted=include_deleted,
        )

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VoteEntity], int]:
        logger.debug(f"Listing votes for condominium_id={condominium_id}")
        return self.repository.list_by_condominium(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def list_active(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
    ) -> Tuple[List[VoteEntity], int]:
        logger.debug(f"Listing active votes skip={skip} limit={limit}")
        return self.repository.list_active(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
        )
