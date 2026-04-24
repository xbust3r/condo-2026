# =============================================================================
# API Routes: core_condominium_roles
# Módulo de roles administrativos por condominio
#
# Endpoints:
#   POST   /condominium-roles                      — create
#   GET    /condominium-roles/{id}                — get by id
#   GET    /condominium-roles/uuid/{uuid}         — get by uuid
#   PUT    /condominium-roles/{id}                — update
#   DELETE /condominium-roles/{id}                — soft delete
#   POST   /condominium-roles/{id}/restore        — restore
#   DELETE /condominium-roles/{id}/hard           — hard delete
#   GET    /condominium-roles                     — list with filters
#   GET    /condominium-roles/condominium/{condominium_id} — list by condo
#   GET    /condominium-roles/user/{user_id}      — list by user
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_condominium_roles.usecase.condominium_role_usecase import (
    CondominiumRoleUseCase,
)
from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
    CreateCondominiumRoleSchema,
    UpdateCondominiumRoleSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/condominium-roles"

condominium_role_routes = APIRouter(prefix=PREFIX)


@condominium_role_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_condominium_roles"}


@condominium_role_routes.post("")
@api_handler
def create_condominium_role(request: CreateCondominiumRoleSchema) -> dict:
    response = CondominiumRoleUseCase().create(request)
    return response.dict()


@condominium_role_routes.get("/{id}")
@api_handler
def get_condominium_role(id: int) -> dict:
    response = CondominiumRoleUseCase().get_by_id(id)
    return response.dict()


@condominium_role_routes.get("/uuid/{uuid}")
@api_handler
def get_condominium_role_by_uuid(uuid: str) -> dict:
    response = CondominiumRoleUseCase().get_by_uuid(uuid)
    return response.dict()


@condominium_role_routes.put("/{id}")
@api_handler
def update_condominium_role(id: int, request: UpdateCondominiumRoleSchema) -> dict:
    response = CondominiumRoleUseCase().update(id, request)
    return response.dict()


@condominium_role_routes.delete("/{id}")
@api_handler
def delete_condominium_role(id: int) -> dict:
    response = CondominiumRoleUseCase().delete(id)
    return response.dict()


@condominium_role_routes.post("/{id}/restore")
@api_handler
def restore_condominium_role(id: int) -> dict:
    response = CondominiumRoleUseCase().restore(id)
    return response.dict()


@condominium_role_routes.delete("/{id}/hard")
@api_handler
def hard_delete_condominium_role(id: int) -> dict:
    response = CondominiumRoleUseCase().hard_delete(id)
    return response.dict()


@condominium_role_routes.get("")
@api_handler
def list_condominium_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    condominium_id: Optional[int] = Query(None, description="Filter by condominium"),
    user_id: Optional[int] = Query(None, description="Filter by user"),
    role: Optional[str] = Query(
        None,
        description="Filter by role: super_admin / condominium_admin / board_member / finance_reviewer / security_staff / maintenance_staff / operations_staff",
    ),
    scope: Optional[str] = Query(None, description="Filter by scope: condominium / building / unit"),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = CondominiumRoleUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        user_id=user_id,
        role=role,
        scope=scope,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()


@condominium_role_routes.get("/condominium/{condominium_id}")
@api_handler
def list_roles_by_condominium(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    role: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = CondominiumRoleUseCase().list_by_condominium(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
        role=role,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()


@condominium_role_routes.get("/user/{user_id}")
@api_handler
def list_roles_by_user(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = CondominiumRoleUseCase().list_by_user(
        user_id=user_id,
        skip=skip,
        limit=limit,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()