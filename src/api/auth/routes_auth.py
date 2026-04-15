# =============================================================================
# API Routes: auth
# Módulo de autenticación JWT
#
# Endpoints:
#   POST   /auth/login                       — authenticate + return token pair
#   POST   /auth/refresh                    — rotate refresh token
#   POST   /auth/logout                     — revoke session
#   POST   /auth/logout-all                 — revoke all user sessions
#   GET    /auth/me                         — current user identity
#   GET    /auth/health
# =============================================================================

from fastapi import APIRouter, Request, Depends

from library.dddpy.auth.usecase.auth_usecase import AuthUseCase
from library.dddpy.auth.usecase.auth_cmd_schema import LoginSchema, RefreshSchema, LogoutSchema
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.auth.auth_dependencies import get_current_user
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/auth"
auth_routes = APIRouter(prefix=PREFIX)


def _client_info(request: Request) -> tuple[str | None, str | None]:
    """Extract user_agent and ip_address from request."""
    user_agent = request.headers.get("user-agent")
    # Try X-Forwarded-For first (behind proxy), then client host
    x_forwarded = request.headers.get("x-forwarded-for")
    if x_forwarded:
        ip_address = x_forwarded.split(",")[0].strip()
    else:
        ip_address = request.client.host if request.client else None
    return user_agent, ip_address


@auth_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "auth"}


@auth_routes.post("/login")
@api_handler
def login(request: Request, credentials: LoginSchema) -> dict:
    """
    Authenticate with email + password.

    Returns access_token (JWT, 15 min) + refresh_token (UUID, 7 days).
    Same error message whether email exists or not (no user enum).
    """
    user_agent, ip_address = _client_info(request)
    response = AuthUseCase().login(
        email=credentials.email,
        password=credentials.password,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    return response.dict()


@auth_routes.post("/refresh")
@api_handler
def refresh(body: RefreshSchema) -> dict:
    """
    Rotate refresh token and issue new token pair.
    Old refresh token is invalidated after use (rotation).
    """
    response = AuthUseCase().refresh(refresh_token=body.refresh_token)
    return response.dict()


@auth_routes.post("/logout")
@api_handler
def logout(body: LogoutSchema) -> dict:
    """Revoke the session associated with the given refresh token."""
    response = AuthUseCase().logout(refresh_token=body.refresh_token)
    return response.dict()


@auth_routes.post("/logout-all")
@api_handler
def logout_all(user: UserIdentity = Depends(get_current_user)) -> dict:
    """Revoke ALL sessions for the current user."""
    response = AuthUseCase().logout_all(user_id=user.id)
    return response.dict()


@auth_routes.get("/me")
@api_handler
def me(user: UserIdentity = Depends(get_current_user)) -> dict:
    """
    Get current authenticated user identity.

    Returns users + user_profiles join.
    password_hash is never included.
    """
    response = AuthUseCase().me(user_id=user.id)
    return response.dict()
