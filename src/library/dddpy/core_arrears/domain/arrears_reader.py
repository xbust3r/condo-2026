"""
ArrearsReader — domain interface for reading property arrears data.
Decouples eligibility providers from the specific AR data source.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class UnitArrears:
    """Immutable snapshot of a unit's arrears status at query time."""
    unit_id: int
    months_in_arrears: int
    total_overdue: Decimal
    oldest_period: Optional[str] = None  # 'YYYY-MM'


class ArrearsReader(ABC):
    """
    Reads arrears data for a given unit.

    The implementation may source data from:
    - core_accounts_receivable
    - core_unit_arrears_summary (future cache table)
    - external ERP/accounting system
    """

    @abstractmethod
    def get_arrears(self, unit_id: int) -> UnitArrears:
        """
        Return arrears status for a unit.
        months_in_arrears = count of distinct months with overdue debt.
        """
        ...
