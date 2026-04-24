# =============================================================================
# API Routes: auth
# Módulo de autenticación JWT
#
# Endpoints:
#   POST   /auth/login                       — authenticate + return token pair
#   POST   /auth/refresh                     — rotate refresh token
#   POST   /auth/logout                      — revoke session
#   POST   /auth/logout-all                  — revoke all user sessions
#   GET    /auth/me                          — current user identity
#   POST   /auth/forgot-password             — initiate password reset
#   POST   /auth/reset-password              — complete password reset
#   POST   /auth/verify-email                — verify email address
#   POST   /auth/resend-verification         — resend verification email
#   GET    /auth/sessions                    — list active sessions
#   GET    /auth/health
# =============================================================================

import time
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps

from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Optional, Tuple, Callable

from library.dddpy.auth.usecase.auth_usecase import AuthUseCase
from library.dddpy.auth.usecase.auth_cmd_schema import (
    LoginSchema,
    RefreshSchema,
    LogoutSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    VerifyEmailSchema,
)
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.auth.domain.auth_exception import RateLimitExceeded
from api.auth.auth_dependencies import get_current_user
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/auth"
auth_routes = APIRouter(prefix=PREFIX)


# ─────────────────────────────────────────────────────────────────────────────
# Rate limiter — simple in-memory store
# Production: replace with Redis-based sliding window
# ─────────────────────────────────────────────────────────────────────────────

_RATE_LIMIT_STORE: dict[str, list[float]] = defaultdict(list)

# Auth endpoint limits (per IP, per endpoint)
_AUTH_RATE_LIMITS = {
    "login": {"max_requests": 5, "window_seconds": 300},      # 5 attempts / 5 min
    "forgot_password": {"max_requests": 3, "window_seconds": 3600},  # 3 / hour
    "refresh": {"max_requests": 10, "window_seconds": 3600},  # 10 / hour
}


def _check_rate_limit(key: str, max_requests: int, window_seconds: int) -> None:
    """
    Sliding window rate limiter.
    Raises RateLimitExceeded if limit exceeded.
    """
    now = time.time()
    window_start = now - window_seconds

    # Prune old entries
    _RATE_LIMIT_STORE[key] = [
        ts for ts in _RATE_LIMIT_STORE[key] if ts > window_start
    ]

    if len(_RATE_LIMIT_STORE[key]) >= max_requests:
        retry_after = int(_RATE_LIMIT_STORE[key][0] + window_seconds - now) + 1
        raise RateLimitExceeded(retry_after_seconds=max(retry_after, 60))

    _RATE_LIMIT_STORE[key].append(now)


def _rate_limit(endpoint: str) -> Callable:
    """Decorator: apply rate limit to a route handler."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            limit_config = _AUTH_RATE_LIMITS.get(endpoint, {"max_requests": 60, "window_seconds": 3600})

            # Use client IP as key (X-Forwarded-For if behind proxy)
            request = None
            for arg in args:
                if hasattr(arg, 'client') and hasattr(arg, 'headers'):
                    request = arg
                    break
            if not request:
                # Try to extract request from kwargs
                request = kwargs.get('request')

            ip = "unknown"
            if request:
                forwarded = request.headers.get("x-forwarded-for")
                ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "unknown")

            key = f"{endpoint}:{ip}"
            _check_rate_limit(key, **limit_config)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _client_info(request: Request) -> Tuple[Optional[str], Optional[str]]:
    """Extract user_agent and ip_address from request."""
    user_agent = request.headers.get("user-agent")
    x_forwarded = request.headers.get("x-forwarded-for")
    if x_forwarded:
        ip_address = x_forwarded.split(",")[0].strip()
    else:
        ip_address = request.client.host if request.client else None
    return user_agent, ip_address


# ─────────────────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────────────────

@auth_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "auth"}


@auth_routes.post("/login")
@api_handler
def login(request: Request, credentials: LoginSchema) -> dict:
    """
    Authenticate with email + password.
    Rate limit: 5 attempts per 5 minutes per IP.
    """
    _rate_limit("login")(lambda: None)()  # Apply rate limit
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
    Rate limit: 10 per hour per IP.
    """
    _rate_limit("refresh")(lambda: None)()
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
    """Get current authenticated user identity."""
    response = AuthUseCase().me(user_id=user.id)
    return response.dict()


# ─────────────────────────────────────────────────────────────────────────────
# Password Reset Flow
# ─────────────────────────────────────────────────────────────────────────────

@auth_routes.post("/forgot-password")
@api_handler
def forgot_password(request: Request, body: ForgotPasswordSchema) -> dict:
    """
    Initiate password reset flow.
    Rate limit: 3 requests per hour per IP.
    Always returns success to prevent email enumeration.
    """
    _rate_limit("forgot_password")(lambda: None)()
    response = AuthUseCase().forgot_password(email=body.email)
    return response.dict()


@auth_routes.post("/reset-password")
@api_handler
def reset_password(body: ResetPasswordSchema) -> dict:
    """
    Complete password reset with token.
    Token is single-use. All sessions are revoked after success.
    """
    response = AuthUseCase().reset_password(
        token=body.token,
        new_password=body.new_password,
    )
    return response.dict()


# ─────────────────────────────────────────────────────────────────────────────
# Email Verification
# ─────────────────────────────────────────────────────────────────────────────

@auth_routes.post("/verify-email")
@api_handler
def verify_email(body: VerifyEmailSchema) -> dict:
    """
    Verify email address using a valid verification token.
    """
    response = AuthUseCase().verify_email(token=body.token)
    return response.dict()


@auth_routes.post("/resend-verification")
@api_handler
def resend_verification(body: ForgotPasswordSchema) -> dict:
    """
    Resend verification email if not yet confirmed.
    Always returns success to prevent email enumeration.
    """
    response = AuthUseCase().resend_verification_email(email=body.email)
    return response.dict()


# ─────────────────────────────────────────────────────────────────────────────
# Active Sessions
# ─────────────────────────────────────────────────────────────────────────────

@auth_routes.get("/sessions")
@api_handler
def list_sessions(user: UserIdentity = Depends(get_current_user)) -> dict:
    """
    List all active sessions for the current user.
    Returns session UUID, device/ip, created_at, expires_at.
    Does NOT return refresh token values (hashed).
    """
    from library.dddpy.auth.infrastructure.auth_session_repository import AuthSessionRepository
    from library.dddpy.auth.infrastructure.dbauth_session import DBAuthSession
    from library.dddpy.shared.mysql.session_manager import session_scope

    repo = AuthSessionRepository()
    sessions = repo.list_active_sessions(user.id)

    return {
        "success": True,
        "data": [
            {
                "uuid": s.uuid,
                "user_agent": s.user_agent,
                "ip_address": s.ip_address,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "expires_at": s.expires_at.isoformat() if s.expires_at else None,
                "is_current": False,  # Client can't easily know its own session UUID
            }
            for s in sessions
        ],
        "total": len(sessions),
    }


@auth_routes.post("/change-password")
@api_handler
def change_password(
    body: ChangePasswordSchema,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Change password for the authenticated user.
    Requires current password. Revokes all sessions on success (like logout-all).
    """
    response = AuthUseCase().change_password(
        user_id=user.id,
        current_password=body.current_password,
        new_password=body.new_password,
    )
    return response.dict()
