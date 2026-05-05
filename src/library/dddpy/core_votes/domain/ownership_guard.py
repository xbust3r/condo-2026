"""
OwnershipGuard — domain interface for actor authorization.
Verifies that a user controls a given unit_ownership_id before any
electoral operation is performed.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class OwnershipGuard(ABC):
    """
    Answers: "Can this user_id act on behalf of this unit_ownership_id?"

    This is NOT eligibility — it's plain authorization.
    If the user does NOT control the unit → raise or return False.
    """

    @abstractmethod
    def assert_user_controls_unit(
        self,
        user_id: int,
        unit_ownership_id: int,
    ) -> bool:
        """Return True if user controls the unit. False otherwise."""
        ...
