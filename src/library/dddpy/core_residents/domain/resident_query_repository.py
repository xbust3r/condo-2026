"""
Resident query repository — aggregates dashboard data for a resident.
"""
from typing import Optional, List, Tuple


class ResidentQueryRepository:
    """
    Resident dashboard aggregation query repository.
    Provides consolidated views by joining multiple modules.
    """

    def get_profile(self, user_id: int, condominium_id: int) -> Optional[object]:
        """Get resident preferences profile for a user in a condominium."""
        pass

    def get_dashboard_summary(
        self,
        user_id: int,
        condominium_id: int,
    ) -> dict:
        """
        Aggregate dashboard data for a resident.
        Returns: unread notifications count, pending incidents, pending packages, recent announcements.
        """
        pass

    def list_my_incidents(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[object], int]:
        pass

    def list_my_packages(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[object], int]:
        pass

    def list_my_visitors(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[object], int]:
        pass
