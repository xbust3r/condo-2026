"""
VoteWeightPolicy — domain interface for vote weight calculation.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal


class VoteWeightPolicy(ABC):
    """
    Calculates the weight of a vote for a specific unit_ownership_id
    in a given vote.

    - BY_UNIT      → 1.0
    - BY_COEFFICIENT → coefficient of the unit
    """

    @abstractmethod
    def calculate_weight(
        self,
        unit_ownership_id: int,
        vote,  # VoteEntity — forward ref
    ) -> Decimal:
        ...
