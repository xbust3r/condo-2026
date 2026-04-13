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

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_condominiums.usecase.condominium_usecase import CondominiumUseCase
from library.dddpy.core_condominiums.usecase.condominium_cmd_schema import CreateCondominiumSchema, UpdateCondominiumSchema
from library.dddpy.shared.decorators.api_handler import api_handler


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
def get_condominium(id: int) -> dict:
    response = CondominiumUseCase().get_by_id(id)
    return response.dict()


@condominium_routes.get("/uuid/{uuid}")
@api_handler
def get_condominium_by_uuid(uuid: str) -> dict:
    response = CondominiumUseCase().get_by_uuid(uuid)
    return response.dict()


@condominium_routes.get("/code/{code}")
@api_handler
def get_condominium_by_code(code: str) -> dict:
    response = CondominiumUseCase().get_by_code(code)
    return response.dict()


@condominium_routes.post("")
@api_handler
def create_condominium(request: CreateCondominiumSchema) -> dict:
    response = CondominiumUseCase().create(request)
    return response.dict()


@condominium_routes.put("/{id}")
@api_handler
def update_condominium(id: int, request: UpdateCondominiumSchema) -> dict:
    response = CondominiumUseCase().update(id, request)
    return response.dict()


@condominium_routes.delete("/{id}")
@api_handler
def delete_condominium(id: int) -> dict:
    """Soft delete a condominium (sets deleted_at timestamp)."""
    response = CondominiumUseCase().delete(id)
    return response.dict()


@condominium_routes.post("/{id}/restore")
@api_handler
def restore_condominium(id: int) -> dict:
    """Restore a soft-deleted condominium."""
    response = CondominiumUseCase().restore(id)
    return response.dict()
