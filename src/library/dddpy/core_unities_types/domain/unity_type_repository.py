from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_unities_types.domain.unity_type_entity import UnityTypeEntity


class UnityTypeRepository(ABC):
    """Repository interface for unity type operations."""

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[UnityTypeEntity]:
        pass

    @abstractmethod
    def find_by_uuid(self, uuid: str) -> Optional[UnityTypeEntity]:
        pass
