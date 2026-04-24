# =============================================================================
# API Routes: core_buildings
# Gestión de edificios/torres dentro de condominios.
#
# RBAC: Todas las rutas que acceden/modifican edificios requieren que el
# usuario autenticado tenga un rol activo en el condominio del edificio.
#
# Patrón RBAC en cada ruta:
#   1. Obtener el building para saber su condominium_id
#   2. Verificar que el usuario tiene rol en ese condominio
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException, status, Path
from typing import Optional

from library.dddpy.core_buildings.usecase.building_usecase import BuildingUseCase
from library.dddpy.core_buildings.usecase.building_cmd_schema import CreateBuildingSchema, UpdateBuildingSchema
from library.dddpy.shared.decorators.api_handler import api_handler
from api.auth.auth_dependencies import get_current_user
from api.auth.rbac_dependencies import require_condominium_role, CondominiumUserContext
from library.dddpy.auth.domain.user_identity import UserIdentity


PREFIX = "/buildings"

building_routes = APIRouter(prefix=PREFIX)


@building_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@building_routes.post("")
@api_handler
def create_building(
    request: CreateBuildingSchema,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Create a new building.
    Requires authenticated user with an active role in the target condominium.
    """
    # Validate user has role in the building's condominium
    ctx = require_condominium_role(user, request.condominium_id)

    # Prevent creating a building in a condominium the user has no access to
    if request.condominium_id != ctx.condominium_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create building in a condominium you don't have access to",
        )

    return BuildingUseCase().create(request).dict()


def _get_building_condominium_id(building_id: int) -> int:
    """Fetch building, return its condominium_id. Raises BuildingNotFound."""
    building_resp = BuildingUseCase().get_by_id(building_id)
    building_data = building_resp.data
    if not building_data:
        from library.dddpy.core_buildings.domain.building_exception import BuildingNotFound
        raise BuildingNotFound()
    condominium_id = building_data.get("condominium_id")
    if not condominium_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Building has no condominium association",
        )
    return condominium_id


@building_routes.get("/{id}")
@api_handler
def get_building(
    id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Get a building by its ID.
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(id)
    require_condominium_role(user, condominium_id)  # raises 403 if no role
    return BuildingUseCase().get_by_id(id).dict()


@building_routes.get("/uuid/{uuid}")
@api_handler
def get_building_by_uuid(uuid: str) -> dict:
    """Get a building by its UUID. No RBAC (public lookup)."""
    return BuildingUseCase().get_by_uuid(uuid).dict()


@building_routes.put("/{id}")
@api_handler
def update_building(
    id: int,
    request: UpdateBuildingSchema,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Update an existing building.
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(id)
    require_condominium_role(user, condominium_id)
    return BuildingUseCase().update(id, request).dict()


@building_routes.delete("/{id}")
@api_handler
def delete_building(
    id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Soft delete a building. Requires active role in the building's condominium."""
    condominium_id = _get_building_condominium_id(id)
    require_condominium_role(user, condominium_id)
    return BuildingUseCase().delete(id).dict()


@building_routes.post("/{id}/restore")
@api_handler
def restore_building(
    id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Restore a soft-deleted building. Requires active role."""
    condominium_id = _get_building_condominium_id(id)
    require_condominium_role(user, condominium_id)
    return BuildingUseCase().restore(id).dict()


@building_routes.delete("/{id}/hard")
@api_handler
def hard_delete_building(
    id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Hard delete a building. Blocked if it has active units. Requires active role."""
    condominium_id = _get_building_condominium_id(id)
    require_condominium_role(user, condominium_id)
    return BuildingUseCase().hard_delete(id).dict()


@building_routes.get("")
@api_handler
def list_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    condominium_id: Optional[int] = Query(None, description="Filter by condominium"),
    building_type_id: Optional[int] = Query(None, description="Filter by building type"),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
) -> dict:
    """List all buildings with optional filters. No RBAC — admin-level list."""
    if limit > 500:
        limit = 500
    return BuildingUseCase().list_all(
        skip=skip, limit=limit,
        condominium_id=condominium_id,
        building_type_id=building_type_id,
        status=status,
        include_deleted=include_deleted,
    ).dict()


@building_routes.post("/{building_id}/recalculate")
@api_handler
def recalculate_building(
    building_id: int,
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """Recalculate and persist computed stats for a building.

    Computes from all active units belonging to this building:
      - built_area:      sum of private_area
      - coefficient:     sum of unit coefficients (tower participation)
      - floors_count:    count of distinct floor numbers >= 0
      - basements_count: count of distinct floor numbers < 0
      - units_planned:   count of active units

    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(building_id)
    require_condominium_role(user, condominium_id)
    return BuildingUseCase().recalculate(building_id).dict()


@building_routes.get("/condominium/{condominium_id}")
@api_handler
def list_buildings_by_condominium(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """List buildings for a specific condominium.
    Requires authenticated user with an active role in the target condominium.
    """
    require_condominium_role(user, condominium_id)
    if limit > 500:
        limit = 500
    return BuildingUseCase().list_by_condominium(
        condominium_id=condominium_id,
        skip=skip, limit=limit,
        status=status,
        include_deleted=include_deleted,
    ).dict()