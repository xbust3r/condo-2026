"""
Charge command repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_charges.domain.charge_data import (
    CreateChargeData,
    UpdateChargeData,
)
from library.dddpy.core_charges.domain.charge_entity import ChargeEntity


class ChargeCmdRepository(ABC):
    """Abstract write repository for charges."""

    @abstractmethod
    def create(self, data: CreateChargeData) -> ChargeEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateChargeData) -> Optional[ChargeEntity]:
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
