"""
Resident use case — resident dashboard and profile management.
"""
from typing import Optional

from library.dddpy.core_residents.domain.resident_exception import (
    ResidentProfileNotFound,
    ResidentProfileValidationError,
)
from library.dddpy.core_residents.domain.resident_query_repository import ResidentQueryRepository
from library.dddpy.core_residents.domain.resident_cmd_repository import ResidentProfileCmdRepository
from library.dddpy.core_residents.infrastructure.resident_query_repository import ResidentQueryRepositoryImpl
from library.dddpy.core_residents.infrastructure.resident_cmd_repository import ResidentProfileCmdRepositoryImpl
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


logger = Logger("ResidentUseCase")


class ResidentUseCase:

    def __init__(self):
        self._query_repo = ResidentQueryRepositoryImpl()
        self._cmd_repo = ResidentProfileCmdRepositoryImpl()

    def get_dashboard(
        self,
        user_id: int,
        condominium_id: int,
    ) -> ResponseSuccessSchema:
        """
        Consolidated resident dashboard.
        Returns notification count, pending incidents/packages/visitors,
        payment summary, and recent announcements.
        """
        logger.add_inside_method("get_dashboard")
        summary = self._query_repo.get_dashboard_summary(user_id, condominium_id)
        return ResponseSuccessSchema(
            success=True,
            message="Dashboard retrieved",
            data=summary,
        )

    def get_profile(
        self,
        user_id: int,
        condominium_id: int,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("get_profile")
        profile = self._query_repo.get_profile(user_id, condominium_id)
        if not profile:
            # Return empty profile response (not found is not an error here)
            return ResponseSuccessSchema(
                success=True,
                message="Resident profile not found — returning defaults",
                data=None,
            )
        return ResponseSuccessSchema(
            success=True,
            message="Resident profile retrieved",
            data=profile.to_dict(),
        )

    def upsert_profile(
        self,
        user_id: int,
        condominium_id: int,
        preferences: dict,
    ) -> ResponseSuccessSchema:
        """Create or update resident preferences profile."""
        logger.add_inside_method("upsert_profile")
        ok = self._cmd_repo.update_preferences(user_id, condominium_id, preferences)
        if not ok:
            raise ResidentProfileNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Preferences updated",
            data=None,
        )

    def list_my_incidents(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_my_incidents")
        data, total = self._query_repo.list_my_incidents(
            user_id, condominium_id, skip, limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="My incidents retrieved",
            data=data,
            total=total,
            skip=skip,
            limit=limit,
        )

    def list_my_packages(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_my_packages")
        data, total = self._query_repo.list_my_packages(
            user_id, condominium_id, skip, limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="My packages retrieved",
            data=data,
            total=total,
            skip=skip,
            limit=limit,
        )

    def list_my_visitors(
        self,
        user_id: int,
        condominium_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_my_visitors")
        data, total = self._query_repo.list_my_visitors(
            user_id, condominium_id, skip, limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="My visitors retrieved",
            data=data,
            total=total,
            skip=skip,
            limit=limit,
        )
