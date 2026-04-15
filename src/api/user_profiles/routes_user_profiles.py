# =============================================================================
# API Routes: core_user_profiles
#
# Endpoints:
#   POST   /user-profiles           — create profile
#   GET    /user-profiles/{user_id} — get profile by user_id
#   PUT    /user-profiles/{user_id} — update profile
#   GET    /user-profiles/health
# =============================================================================

from fastapi import APIRouter

from library.dddpy.core_user_profiles.usecase.user_profile_usecase import UserProfileUseCase
from library.dddpy.core_user_profiles.usecase.user_profile_cmd_schema import (
    CreateUserProfileSchema,
    UpdateUserProfileSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/user-profiles"
user_profile_routes = APIRouter(prefix=PREFIX)


@user_profile_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_user_profiles"}


@user_profile_routes.post("")
@api_handler
def create_profile(request: CreateUserProfileSchema) -> dict:
    """Create a profile for a user."""
    response = UserProfileUseCase().create(request)
    return response.dict()


@user_profile_routes.get("/{user_id}")
@api_handler
def get_profile(user_id: int) -> dict:
    """Get a profile by user_id."""
    response = UserProfileUseCase().get_by_user_id(user_id)
    return response.dict()


@user_profile_routes.put("/{user_id}")
@api_handler
def update_profile(user_id: int, request: UpdateUserProfileSchema) -> dict:
    """Update a user's profile."""
    response = UserProfileUseCase().update(user_id, request)
    return response.dict()
