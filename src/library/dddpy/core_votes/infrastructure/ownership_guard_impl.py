"""
OwnershipGuard implementation — verifies user controls a unit_ownership record.
"""
from library.dddpy.core_votes.domain.ownership_guard import OwnershipGuard
from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import (
    UnitOwnershipQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("OwnershipGuardImpl")


class OwnershipGuardImpl(OwnershipGuard):
    """Checks via core_unit_ownerships that user_id has an active record
    for the given unit_ownership_id."""

    def assert_user_controls_unit(
        self,
        user_id: int,
        unit_ownership_id: int,
    ) -> bool:
        repo = UnitOwnershipQueryRepositoryImpl()
        record = repo.get_by_id(unit_ownership_id)
        if record is None:
            return False
        # The owner is record.user_id and it must be active
        return record.user_id == user_id and record.status == "active"
