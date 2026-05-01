from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity


class CondominiumQueryRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100, status: Optional[int] = None, city: Optional[str] = None, country: Optional[str] = None, include_deleted: bool = False, ids: Optional[List[int]] = None) -> tuple[List[CondominiumEntity], int]:
        """List condominiums with optional filters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            status: Filter by status (1=active, 0=inactive)
            city: Filter by city (partial match)
            country: Filter by country (partial match)
            include_deleted: If True, include soft-deleted records
        """
        pass