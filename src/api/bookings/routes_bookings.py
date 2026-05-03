"""
API Routes: amenity_bookings

Endpoints:
  POST   /bookings                  — create booking  [RBAC: bookings.create]
  GET    /bookings                  — list bookings   [RBAC: bookings.read]
  GET    /bookings/report           — booking report  [RBAC: bookings.read]
  GET    /bookings/{id}             — get booking     [RBAC: bookings.read]
  GET    /bookings/uuid/{uuid}      — get by uuid     [RBAC: bookings.read]
  PUT    /bookings/{id}             — update booking  [RBAC: bookings.update]
  DELETE /bookings/{id}             — cancel booking  [RBAC: bookings.delete]
  POST   /bookings/{id}/confirm     — confirm booking [RBAC: bookings.update]
  POST   /bookings/{id}/cancel      — cancel booking  [RBAC: bookings.update]
  POST   /bookings/{id}/complete    — complete        [RBAC: bookings.update]
  POST   /bookings/{id}/deposit/return   — return deposit  [RBAC: bookings.update]
  POST   /bookings/{id}/deposit/apply    — apply deposit   [RBAC: bookings.update]
"""
from fastapi import APIRouter, Depends, Query

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
from library.dddpy.core_amenity_bookings.usecase.booking_cmd_schema import (
    CreateBookingSchema,
    UpdateBookingSchema,
    CancelBookingSchema,
    DepositActionSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.decorators.rbac_handler import rbac_required


PREFIX = "/bookings"
booking_routes = APIRouter(prefix=PREFIX)


@booking_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_amenity_bookings"}


@booking_routes.post("")
@api_handler
def create_booking(
    request: CreateBookingSchema,
    user: UserIdentity = Depends(rbac_required("bookings", "create")),
) -> dict:
    """Create a new amenity booking."""
    response = BookingUseCase().create(
        condominium_id=request.condominium_id,
        building_id=request.building_id,
        amenity_id=request.amenity_id,
        unit_id=request.unit_id,
        owner_id=request.owner_id,
        booking_date=request.booking_date,
        start_at=request.start_at,
        end_at=request.end_at,
        notes=request.notes,
        created_by=user.user_id if user else None,
    )
    return response.dict()


@booking_routes.get("")
@api_handler
def list_bookings(
    condominium_id: int = Query(None, description="Filter by condominium"),
    building_id: int = Query(None, description="Filter by building"),
    amenity_id: int = Query(None, description="Filter by amenity"),
    unit_id: int = Query(None, description="Filter by unit"),
    owner_id: int = Query(None, description="Filter by owner"),
    status: str = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("bookings", "read")),
) -> dict:
    """List bookings with optional filters."""
    response = BookingUseCase().list_all(
        condominium_id=condominium_id,
        building_id=building_id,
        amenity_id=amenity_id,
        unit_id=unit_id,
        owner_id=owner_id,
        status=status,
        skip=skip,
        limit=limit,
        include_deleted=include_deleted,
    )
    return response.dict()


@booking_routes.get("/report")
@api_handler
def booking_report(
    condominium_id: int = Query(..., description="Condominium ID"),
    building_id: int = Query(None, description="Filter by building"),
    amenity_id: int = Query(None, description="Filter by amenity"),
    date_from: str = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: str = Query(None, description="End date (YYYY-MM-DD)"),
    user: UserIdentity = Depends(rbac_required("bookings", "read")),
) -> dict:
    """Generate detailed booking report with breakdowns."""
    from datetime import date as date_type
    response = BookingUseCase().get_report(
        condominium_id=condominium_id,
        building_id=building_id,
        amenity_id=amenity_id,
        date_from=date_type.fromisoformat(date_from) if date_from else None,
        date_to=date_type.fromisoformat(date_to) if date_to else None,
    )
    return response.dict()


@booking_routes.get("/{id}")
@api_handler
def get_booking(
    id: int,
    user: UserIdentity = Depends(rbac_required("bookings", "read")),
) -> dict:
    """Get a booking by id."""
    response = BookingUseCase().get_by_id(id)
    return response.dict()


@booking_routes.get("/uuid/{uuid}")
@api_handler
def get_booking_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("bookings", "read")),
) -> dict:
    """Get a booking by uuid."""
    response = BookingUseCase().get_by_uuid(uuid)
    return response.dict()


@booking_routes.put("/{id}")
@api_handler
def update_booking(
    id: int,
    request: UpdateBookingSchema,
    user: UserIdentity = Depends(rbac_required("bookings", "update")),
) -> dict:
    """Update a booking (dates, notes). Only in draft/pending_approval."""
    response = BookingUseCase().update(id, request)
    return response.dict()


@booking_routes.delete("/{id}")
@api_handler
def delete_booking(
    id: int,
    user: UserIdentity = Depends(rbac_required("bookings", "delete")),
) -> dict:
    """Soft-delete (cancel) a booking."""
    response = BookingUseCase().soft_delete(id)
    return response.dict()


# ── Lifecycle endpoints ──────────────────────────────────────────────

@booking_routes.post("/{id}/confirm")
@api_handler
def confirm_booking(
    id: int,
    user: UserIdentity = Depends(rbac_required("bookings", "update")),
) -> dict:
    """Confirm booking → generates AR entries for fee + deposit."""
    response = BookingUseCase().confirm(id)
    return response.dict()


@booking_routes.post("/{id}/cancel")
@api_handler
def cancel_booking(
    id: int,
    request: CancelBookingSchema,
    user: UserIdentity = Depends(rbac_required("bookings", "update")),
) -> dict:
    """Cancel a booking with reason."""
    response = BookingUseCase().cancel(id, reason=request.reason)
    return response.dict()


@booking_routes.post("/{id}/complete")
@api_handler
def complete_booking(
    id: int,
    user: UserIdentity = Depends(rbac_required("bookings", "update")),
) -> dict:
    """Mark a booking as completed."""
    response = BookingUseCase().complete(id)
    return response.dict()


# ── Deposit endpoints ────────────────────────────────────────────────

@booking_routes.post("/{id}/deposit/return")
@api_handler
def return_deposit(
    id: int,
    notes: str = Query(None, description="Return notes"),
    user: UserIdentity = Depends(rbac_required("bookings", "update")),
) -> dict:
    """Full refund of security deposit."""
    response = BookingUseCase().return_deposit(id, notes=notes)
    return response.dict()


@booking_routes.post("/{id}/deposit/apply")
@api_handler
def apply_deposit(
    id: int,
    request: DepositActionSchema,
    user: UserIdentity = Depends(rbac_required("bookings", "update")),
) -> dict:
    """Apply deposit (partial or full) for damages."""
    response = BookingUseCase().apply_deposit(
        id=id,
        action=request.action,
        amount=request.amount,
        notes=request.notes,
    )
    return response.dict()
