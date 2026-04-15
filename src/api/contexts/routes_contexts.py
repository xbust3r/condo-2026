# =============================================================================
# API Routes: Context aggregation endpoints
#
# Endpoints:
#   GET  /me/contexts          — full context for current authenticated user
#   GET  /users/{id}/contexts  — full context for any user (admin)
#   GET  /units/{id}/summary   — summary for a unit (building + ownerships + occupancies)
# =============================================================================

from fastapi import APIRouter, Depends

from api.contexts.context_usecase import ContextUseCase
from api.auth.auth_dependencies import get_current_user
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = ""
context_routes = APIRouter(prefix=PREFIX)


@context_routes.get("/me/contexts")
@api_handler
def get_my_context(
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Full context for the currently authenticated user.
    Includes: user identity + profile + ownerships + occupancies + roles by condominium.
    """
    response = ContextUseCase().get_user_context(user.id)
    return {"success": True, "message": "Context retrieved", "data": response}


@context_routes.get("/users/{id}/contexts")
@api_handler
def get_user_context(id: int) -> dict:
    """
    Full context for any user by ID (admin endpoint).
    Same data structure as /me/contexts.
    """
    response = ContextUseCase().get_user_context(id)
    return {"success": True, "message": "Context retrieved", "data": response}


@context_routes.get("/units/{id}/summary")
@api_handler
def get_unit_summary(id: int) -> dict:
    """
    Summary for a unit including:
    unit data + building info + active ownerships + active occupancies + resident count.
    """
    response = ContextUseCase().get_unit_summary(id)
    return {"success": True, "message": "Unit summary retrieved", "data": response}
