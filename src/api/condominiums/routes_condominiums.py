# =============================================================================
# API Routes: core_condominiums
# Módulo ✅ ACTUALIZADO — Gestión de condominios
#
# Campos actuales:
#   id, uuid, code, name, legal_name, document_number, description,
#   land_area, built_area, area_unit, address, city, country,
#   contact_email, contact_phone, status, created_at, updated_at, deleted_at
#
# Features: soft delete, filtros por status/city/country, restore
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Depends, Query

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.core_condominiums.usecase.condominium_usecase import CondominiumUseCase
from library.dddpy.core_condominiums.usecase.condominium_cmd_schema import CreateCondominiumSchema, UpdateCondominiumSchema
from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import CondominiumRoleQueryRepositoryImpl
from library.dddpy.core_users.infrastructure.user_query_repository import UserQueryRepositoryImpl
from library.dddpy.core_user_profiles.infrastructure.user_profile_query_repository import UserProfileQueryRepositoryImpl
from library.dddpy.core_condominiums.domain.condominium_exception import CondominiumNotFound
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.decorators.rbac_handler import rbac_required
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


PREFIX = "/condominiums"

condominium_routes = APIRouter(prefix=PREFIX)


@condominium_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@condominium_routes.get("")
@api_handler
def list_condominiums(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    city: Optional[str] = Query(None, description="Filter by city (partial match)"),
    country: Optional[str] = Query(None, description="Filter by country (partial match)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
    user: UserIdentity = Depends(rbac_required("condominium", "read")),
) -> dict:
    """List all condominiums with optional filters."""
    if limit > 500:
        limit = 500  # Safety cap
    response = CondominiumUseCase().list_all(
        skip=skip, 
        limit=limit, 
        status=status, 
        city=city, 
        country=country,
        include_deleted=include_deleted
    )
    return response.dict()


@condominium_routes.get("/{id}")
@api_handler
def get_condominium(
    id: int,
    user: UserIdentity = Depends(rbac_required("condominium", "read")),
) -> dict:
    response = CondominiumUseCase().get_by_id(id)
    return response.dict()


@condominium_routes.get("/uuid/{uuid}")
@api_handler
def get_condominium_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("condominium", "read")),
) -> dict:
    response = CondominiumUseCase().get_by_uuid(uuid)
    return response.dict()


@condominium_routes.get("/code/{code}")
@api_handler
def get_condominium_by_code(
    code: str,
    user: UserIdentity = Depends(rbac_required("condominium", "read")),
) -> dict:
    response = CondominiumUseCase().get_by_code(code)
    return response.dict()


@condominium_routes.get("/{id}/users")
@api_handler
def get_condominium_users(
    id: int,
    role_status: Optional[str] = Query(None, description="Filter roles by status (active/inactive/historical)"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user: UserIdentity = Depends(rbac_required("condominium", "read")),
) -> dict:
    """
    Get all users with an active role in a condominium.
    Returns user identity + profile + all their roles in this condominium.
    """
    # Verify condominium exists
    condo = CondominiumUseCase().get_by_id(id)
    if not condo.data:
        raise CondominiumNotFound()

    role_repo = CondominiumRoleQueryRepositoryImpl()
    user_repo = UserQueryRepositoryImpl()
    profile_repo = UserProfileQueryRepositoryImpl()

    roles, total_roles = role_repo.list_by_condominium(
        condominium_id=id,
        status=role_status or "active",
        include_deleted=False,
        limit=limit,
        offset=offset,
    )

    # Group by user
    users_map: dict = {}
    for role in roles:
        if role.user_id not in users_map:
            user = user_repo.get_by_id(role.user_id, include_deleted=False)
            profile = profile_repo.get_by_user_id(role.user_id)
            users_map[role.user_id] = {
                "user": user.to_dict() if user else None,
                "profile": profile.to_dict() if profile else None,
                "roles": [],
            }
        users_map[role.user_id]["roles"].append(role.to_dict())

    return ResponseSuccessSchema(
        success=True,
        message="Condominium users retrieved",
        data={
            "condominium": condo.data,
            "users": list(users_map.values()),
            "count": len(users_map),
            "total_roles": total_roles,
            "pagination": {
                "limit": limit,
                "offset": offset,
            },
        },
    ).dict()


@condominium_routes.get("/{id}/admins")
@api_handler
def get_condominium_admins(
    id: int,
    user: UserIdentity = Depends(rbac_required("condominium", "read")),
) -> dict:
    """
    Get all users with roles in a condominium, including their profile and role details.
    Returns active roles only.
    """
    # Verify condominium exists
    condo = CondominiumUseCase().get_by_id(id)
    if not condo.data:
        raise CondominiumNotFound()

    role_repo = CondominiumRoleQueryRepositoryImpl()
    user_repo = UserQueryRepositoryImpl()
    profile_repo = UserProfileQueryRepositoryImpl()

    roles, _ = role_repo.list_by_condominium(
        condominium_id=id,
        status="active",
        include_deleted=False,
        limit=500,
    )

    # Group by user
    users_map: dict = {}
    for role in roles:
        if role.user_id not in users_map:
            user = user_repo.get_by_id(role.user_id, include_deleted=False)
            profile = profile_repo.get_by_user_id(role.user_id)
            users_map[role.user_id] = {
                "user": user.to_dict() if user else None,
                "profile": profile.to_dict() if profile else None,
                "roles": [],
            }
        users_map[role.user_id]["roles"].append(role.to_dict())

    return ResponseSuccessSchema(
        success=True,
        message="Condominium admins retrieved",
        data={
            "condominium": condo.data,
            "admins": list(users_map.values()),
            "count": len(users_map),
        },
    ).dict()


@condominium_routes.get("/{id}/summary")
@api_handler
def get_condominium_summary(
    id: int,
    user: UserIdentity = Depends(rbac_required("condominium", "read")),
) -> dict:
    """
    Consolidated summary for a condominium.

    Returns:
      - Condominium identity + unit/building stats
      - AR financial summary:
          total_debt, total_pending,
          overdue_count, overdue_30_days_count,
          overdue_amount
    """
    response = CondominiumUseCase().get_summary(id)
    return response.dict()


@condominium_routes.post("")
@api_handler
def create_condominium(
    request: CreateCondominiumSchema,
    user: UserIdentity = Depends(rbac_required("condominium", "create")),
) -> dict:
    response = CondominiumUseCase().create(request)
    return response.dict()


@condominium_routes.put("/{id}")
@api_handler
def update_condominium(
    id: int,
    request: UpdateCondominiumSchema,
    user: UserIdentity = Depends(rbac_required("condominium", "update")),
) -> dict:
    response = CondominiumUseCase().update(id, request)
    return response.dict()


@condominium_routes.delete("/{id}")
@api_handler
def delete_condominium(
    id: int,
    user: UserIdentity = Depends(rbac_required("condominium", "delete")),
) -> dict:
    """Soft delete a condominium (sets deleted_at timestamp)."""
    response = CondominiumUseCase().delete(id)
    return response.dict()


@condominium_routes.post("/{id}/restore")
@api_handler
def restore_condominium(
    id: int,
    user: UserIdentity = Depends(rbac_required("condominium", "update")),
) -> dict:
    """Restore a soft-deleted condominium."""
    response = CondominiumUseCase().restore(id)
    return response.dict()
