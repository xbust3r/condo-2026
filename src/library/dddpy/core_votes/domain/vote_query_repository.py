"""
Vote query repository ABC — read operations.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from library.dddpy.core_votes.domain.vote_entity import VoteEntity


class VoteQueryRepository(ABC):
    """Interfaz de lectura para consultas de votes."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[VoteEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[VoteEntity]:
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        created_by_user_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VoteEntity], int]:
        pass

    @abstractmethod
    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VoteEntity], int]:
        pass

    @abstractmethod
    def list_active(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
    ) -> Tuple[List[VoteEntity], int]:
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[VoteEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass
