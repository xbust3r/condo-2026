"""
from typing import Optional
ChargeType command repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_charge_types.domain.charge_type_data import (
    CreateChargeTypeData,
    UpdateChargeTypeData,
)
from library.dddpy.core_charge_types.domain.charge_type_entity import ChargeTypeEntity


class ChargeTypeCmdRepository(ABC):
    """Abstract write repository for charge types."""

    @abstractmethod
    def create(self, data: CreateChargeTypeData) -> ChargeTypeEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateChargeTypeData) -> Optional[ChargeTypeEntity]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        pass
