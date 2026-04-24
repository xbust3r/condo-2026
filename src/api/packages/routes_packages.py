from typing import Optional
"""API Routes: core_packages — package/maquil delivery management.

Endpoints:
  GET    /packages                          — health check
  POST   /packages                          — register a package
  GET    /packages                          — list with filters
  GET    /packages/{id}                     — get by id
  GET    /packages/uuid/{uuid}              — get by uuid
  GET    /packages/condominium/{condominium_id}/pending — pending packages for concierge
  GET    /packages/unit/{unit_id}           — list by unit
  PUT    /packages/{id}                     — update (status, carrier, etc.)
  POST   /packages/{id}/deliver             — mark as delivered (verify pickup_code)
  POST   /packages/{id}/cancel              — cancel package
  DELETE /packages/{id}                     — soft delete
  DELETE /packages/{id}/hard                — hard delete
"""

from fastapi import APIRouter, Query, Path
from typing import Optional

from library.dddpy.core_packages.usecase.package_usecase import PackageUseCase
from library.dddpy.core_packages.usecase.package_cmd_schema import (
    CreatePackageSchema,
    UpdatePackageSchema,
    DeliverPackageSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/packages"
package_routes = APIRouter(prefix=PREFIX)


@package_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_packages"}


@package_routes.post("")
@api_handler
def create_package(request: CreatePackageSchema) -> dict:
    """Register a new package delivery."""
    response = PackageUseCase().create(
        condominium_id=request.condominium_id,
        unit_id=request.unit_id,
        recipient_user_id=request.recipient_user_id,
        carrier=request.carrier,
        tracking_number=request.tracking_number,
        description=request.description,
    )
    return response.dict()


@package_routes.get("")
@api_handler
def list_packages(
    condominium_id: Optional[int] = Query(None, description="Filter by condominium"),
    unit_id: Optional[int] = Query(None, description="Filter by unit"),
    recipient_user_id: Optional[int] = Query(None, description="Filter by recipient user"),
    status: Optional[str] = Query(None, description="Filter by status"),
    include_deleted: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List packages with optional filters."""
    response = PackageUseCase().list_all(
        condominium_id=condominium_id,
        unit_id=unit_id,
        recipient_user_id=recipient_user_id,
        status=status,
        include_deleted=include_deleted,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@package_routes.get("/{id}")
@api_handler
def get_package(id: int = Path(..., description="Package ID")) -> dict:
    """Get a package by id."""
    response = PackageUseCase().get_by_id(id)
    return response.dict()


@package_routes.get("/uuid/{uuid}")
@api_handler
def get_package_by_uuid(uuid: str = Path(..., description="Package UUID")) -> dict:
    """Get a package by uuid."""
    response = PackageUseCase().get_by_uuid(uuid)
    return response.dict()


@package_routes.get("/condominium/{condominium_id}/pending")
@api_handler
def list_pending_packages(
    condominium_id: int = Path(..., description="Condominium ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List pending/with_concierge packages for a condominium (concierge view)."""
    response = PackageUseCase().list_pending(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@package_routes.get("/unit/{unit_id}")
@api_handler
def list_packages_by_unit(
    unit_id: int = Path(..., description="Unit ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List packages for a specific unit."""
    response = PackageUseCase().list_by_unit(
        unit_id=unit_id,
        status=status,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@package_routes.put("/{id}")
@api_handler
def update_package(
    id: int = Path(..., description="Package ID"),
    request: UpdatePackageSchema = ...,
) -> dict:
    """Update package (status, carrier, tracking_number, description)."""
    response = PackageUseCase().update(
        id=id,
        status=request.status,
        carrier=request.carrier,
        tracking_number=request.tracking_number,
        description=request.description,
    )
    return response.dict()


@package_routes.post("/{id}/deliver")
@api_handler
def deliver_package(
    id: int = Path(..., description="Package ID"),
    request: DeliverPackageSchema = ...,
) -> dict:
    """Mark package as delivered — verifies pickup_code first."""
    response = PackageUseCase().mark_delivered(
        id=id,
        pickup_code=request.pickup_code,
    )
    return response.dict()


@package_routes.post("/{id}/cancel")
@api_handler
def cancel_package(id: int = Path(..., description="Package ID")) -> dict:
    """Cancel a package."""
    response = PackageUseCase().cancel(id=id)
    return response.dict()


@package_routes.delete("/{id}")
@api_handler
def delete_package(id: int = Path(..., description="Package ID")) -> dict:
    """Soft delete a package."""
    response = PackageUseCase().soft_delete(id=id)
    return response.dict()


@package_routes.delete("/{id}/hard")
@api_handler
def hard_delete_package(id: int = Path(..., description="Package ID")) -> dict:
    """Permanently delete a package."""
    response = PackageUseCase().hard_delete(id=id)
    return response.dict()
