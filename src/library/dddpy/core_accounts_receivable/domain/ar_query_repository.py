"""
from typing import Optional
AccountsReceivable query repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from library.dddpy.core_accounts_receivable.domain.ar_entity import AREntity


class ARQueryRepository(ABC):
    """Abstract read repository for accounts receivable."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[AREntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[AREntity]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[AREntity], int]:
        pass

    @abstractmethod
    def list_overdue(
        self,
        condominium_id: int,
        as_of_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AREntity], int]:
        """List overdue AR entries for a condominium."""
        pass

    @abstractmethod
    def get_summary_by_unit(self, unit_id: int) -> dict:
        """Get debt summary for a unit: total debt, pending, overdue count."""
        pass

    @abstractmethod
    def get_summary_by_condominium(self, condominium_id: int) -> dict:
        """Get debt summary for a condominium: total debt, pending, overdue count, overdue_30_days."""
        pass

    @abstractmethod
    def exists_by_charge_period_unit(
        self, charge_id: int, period: str, unit_id: int
    ) -> bool:
        """Check if an AR already exists for charge + period + unit (idempotency)."""
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[AREntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass
