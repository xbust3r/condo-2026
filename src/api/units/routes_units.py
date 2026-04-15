# =============================================================================
# API Routes: core_units
# Módulo de gestión de unidades inmobiliarias
#
# RBAC: Todas las rutas que acceden/modifican unidades requieren que el
# usuario autenticado tenga un rol activo en el condominio al que pertenece
# el edificio de la unidad.
#
# Patrón RBAC:
#   1. Obtener el building para saber su condominium_id
#   2. Verificar que el usuario tiene rol en ese condominio
# =============================================================================

from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional

from library.dddpy.core_units.usecase.unit_usecase import UnitUseCase
from library.dddpy.core_units.usecase.unit_cmd_schema import (
    CreateUnitSchema,
    UpdateUnitSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler
from api.auth.auth_dependencies import get_current_user
from api.auth.rbac_dependencies import require_condominium_role
from library.dddpy.auth.domain.user_identity import UserIdentity


PREFIX = "/units"

unit_routes = APIRouter(prefix=PREFIX)


@unit_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_units"}


def _get_building_condominium_id(building_id: int) -> int:
    """Fetch building, return its condominium_id. Raises BuildingNotFound."""
    from library.dddpy.core_buildings.usecase.building_usecase import BuildingUseCase
    from library.dddpy.core_buildings.domain.building_exception import BuildingNotFound

    building_resp = BuildingUseCase().get_by_id(building_id)
    building_data = building_resp.data
    if not building_data:
        raise BuildingNotFound()
    condominium_id = building_data.get("condominium_id")
    if not condominium_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Building has no condominium association",
        )
    return condominium_id


@unit_routes.post("")
@api_handler
def create_unit(
    request: CreateUnitSchema,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Create a new unit in a building.
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(request.building_id)
    require_condominium_role(user, condominium_id)  # raises 403 if no role
    return UnitUseCase().create(request).dict()


@unit_routes.get("/{id}")
@api_handler
def get_unit(
    id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Get a unit by its ID.
    Requires authenticated user with an active role in the unit's building's condominium.
    """
    unit_resp = UnitUseCase().get_by_id(id)
    unit_data = unit_resp.data
    if not unit_data:
        from library.dddpy.core_units.domain.unit_exception import UnitNotFound
        raise UnitNotFound()
    condominium_id = _get_building_condominium_id(unit_data["building_id"])
    require_condominium_role(user, condominium_id)
    return unit_resp.dict()


@unit_routes.get("/uuid/{uuid}")
@api_handler
def get_unit_by_uuid(uuid: str) -> dict:
    """Get a unit by its UUID. No RBAC — public lookup."""
    return UnitUseCase().get_by_uuid(uuid).dict()


@unit_routes.put("/{id}")
@api_handler
def update_unit(
    id: int,
    request: UpdateUnitSchema,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Update an existing unit. Requires active role in the building's condominium."""
    unit_resp = UnitUseCase().get_by_id(id)
    unit_data = unit_resp.data
    if not unit_data:
        from library.dddpy.core_units.domain.unit_exception import UnitNotFound
        raise UnitNotFound()
    condominium_id = _get_building_condominium_id(unit_data["building_id"])
    require_condominium_role(user, condominium_id)
    return UnitUseCase().update(id, request).dict()


@unit_routes.delete("/{id}")
@api_handler
def delete_unit(
    id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Soft delete a unit. Requires active role in the building's condominium."""
    unit_resp = UnitUseCase().get_by_id(id)
    unit_data = unit_resp.data
    if not unit_data:
        from library.dddpy.core_units.domain.unit_exception import UnitNotFound
        raise UnitNotFound()
    condominium_id = _get_building_condominium_id(unit_data["building_id"])
    require_condominium_role(user, condominium_id)
    return UnitUseCase().delete(id).dict()


@unit_routes.post("/{id}/restore")
@api_handler
def restore_unit(
    id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Restore a soft-deleted unit. Requires active role."""
    unit_resp = UnitUseCase().get_by_id(id)
    unit_data = unit_resp.data
    if not unit_data:
        from library.dddpy.core_units.domain.unit_exception import UnitNotFound
        raise UnitNotFound()
    condominium_id = _get_building_condominium_id(unit_data["building_id"])
    require_condominium_role(user, condominium_id)
    return UnitUseCase().restore(id).dict()


@unit_routes.delete("/{id}/hard")
@api_handler
def hard_delete_unit(
    id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Hard delete a unit. Blocked if it has active residents. Requires active role."""
    unit_resp = UnitUseCase().get_by_id(id)
    unit_data = unit_resp.data
    if not unit_data:
        from library.dddpy.core_units.domain.unit_exception import UnitNotFound
        raise UnitNotFound()
    condominium_id = _get_building_condominium_id(unit_data["building_id"])
    require_condominium_role(user, condominium_id)
    return UnitUseCase().hard_delete(id).dict()


@unit_routes.get("")
@api_handler
def list_units(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    building_id: Optional[int] = Query(None, description="Filter by building"),
    unit_type_id: Optional[int] = Query(None, description="Filter by unit type"),
    occupancy_status: Optional[str] = Query(
        None,
        description="Filter by occupancy status: vacant|occupied|reserved|maintenance|blocked",
    ),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
) -> dict:
    """List all units with optional filters. No RBAC — admin-level list."""
    if limit > 500:
        limit = 500
    return UnitUseCase().list_all(
        skip=skip,
        limit=limit,
        building_id=building_id,
        unit_type_id=unit_type_id,
        occupancy_status=occupancy_status,
        status=status,
        include_deleted=include_deleted,
    ).dict()


@unit_routes.get("/building/{building_id}")
@api_handler
def list_units_by_building(
    building_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    occupancy_status: Optional[str] = Query(
        None,
        description="Filter by occupancy status: vacant|occupied|reserved|maintenance|blocked",
    ),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """List units for a specific building.
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(building_id)
    require_condominium_role(user, condominium_id)
    if limit > 500:
        limit = 500
    return UnitUseCase().list_by_building(
        building_id=building_id,
        skip=skip,
        limit=limit,
        occupancy_status=occupancy_status,
        status=status,
        include_deleted=include_deleted,
    ).dict()