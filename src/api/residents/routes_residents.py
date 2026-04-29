# =============================================================================
# API Routes: core_residents — Resident portal
#
# Endpoints:
#   GET  /residents/dashboard                     — consolidated dashboard
#   GET  /residents/profile                       — my preferences profile
#   PUT  /residents/profile                       — update preferences
#   GET  /residents/incidents                     — my incidents
#   GET  /residents/packages                      — my packages
#   GET  /residents/visitors                      — my visitor registrations
# =============================================================================

from fastapi import APIRouter, Depends, Query

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.auth.domain.auth_exception import TokenInvalid
from library.dddpy.core_residents.usecase.resident_usecase import ResidentUseCase
from library.dddpy.core_residents.usecase.resident_cmd_schema import UpdatePreferencesSchema
from api.auth.auth_dependencies import get_current_user
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/residents"
resident_routes = APIRouter(prefix=PREFIX)


@resident_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_residents"}


@resident_routes.get("/dashboard")
@api_handler
def get_resident_dashboard(
    condominium_id: int = Query(..., description="Condominium ID"),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Consolidated resident dashboard.
    Returns unread notifications, pending incidents/packages/visitors,
    payment balance, and recent announcements.
    """
    response = ResidentUseCase().get_dashboard(
        user_id=user.id,
        condominium_id=condominium_id,
    )
    return response.dict()


@resident_routes.get("/profile")
@api_handler
def get_resident_profile(
    condominium_id: int = Query(..., description="Condominium ID"),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Get my preferences profile for this condominium."""
    response = ResidentUseCase().get_profile(
        user_id=user.id,
        condominium_id=condominium_id,
    )
    return response.dict()


@resident_routes.put("/profile")
@api_handler
def update_resident_profile(
    body: UpdatePreferencesSchema,
    condominium_id: int = Query(...),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Update my notification preferences for this condominium."""
    preferences = body.model_dump(exclude_none=True)
    response = ResidentUseCase().upsert_profile(
        user_id=user.id,
        condominium_id=condominium_id,
        preferences=preferences,
    )
    return response.dict()


@resident_routes.get("/incidents")
@api_handler
def list_my_incidents(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """List my incidents in this condominium (via occupancy)."""
    response = ResidentUseCase().list_my_incidents(
        user_id=user.id,
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@resident_routes.get("/packages")
@api_handler
def list_my_packages(
    condominium_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """List my packages in this condominium."""
    response = ResidentUseCase().list_my_packages(
        user_id=user.id,
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@resident_routes.get("/visitors")
@api_handler
def list_my_visitors(
    condominium_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """List my visitor registrations in this condominium."""
    response = ResidentUseCase().list_my_visitors(
        user_id=user.id,
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


# =============================================================================
# Admin endpoints — resident profiles management
# =============================================================================
from library.dddpy.auth.domain.user_identity import UserIdentity
from api.auth.auth_dependencies import get_current_user


@resident_routes.get("/admin/profiles")
@api_handler
def list_resident_profiles(
    condominium_id: int = Query(..., description="Condominium ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """List all resident profiles for a condominium (admin)."""
    response = ResidentUseCase().list_all_by_condominium(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@resident_routes.get("/admin/profiles/{profile_id}")
@api_handler
def get_resident_profile_by_id(
    profile_id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Get a specific resident profile by ID."""
    response = ResidentUseCase().get_profile_by_id(profile_id)
    return response.dict()


@resident_routes.put("/admin/profiles/{profile_id}")
@api_handler
def update_resident_profile_by_id(
    profile_id: int,
    body: UpdatePreferencesSchema,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Update a specific resident profile by ID (admin)."""
    preferences = body.model_dump(exclude_none=True)
    response = ResidentUseCase().update_profile_by_id(profile_id, preferences)
    return response.dict()
