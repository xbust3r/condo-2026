# =============================================================================
# API Routes: core_receipts
# Módulo de recibos de pago
#
# Endpoints:
#   GET    /receipts                    — list with filters
#   GET    /receipts/{id}             — get by id
#   GET    /receipts/uuid/{uuid}      — get by uuid
#   GET    /receipts/number/{number}  — get by receipt number
#   GET    /receipts/unit/{unit_id}   — receipts by unit
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_receipts.usecase.receipt_usecase import ReceiptUseCase
from library.dddpy.core_receipts.usecase.receipt_cmd_schema import CreateReceiptSchema
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/receipts"

receipt_routes = APIRouter(prefix=PREFIX)


@receipt_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_receipts"}


@receipt_routes.get("")
@api_handler
def list_receipts(
    condominium_id: Optional[int] = Query(None),
    unit_id: Optional[int] = Query(None),
    ar_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List receipts with optional filters."""
    response = ReceiptUseCase().list_all(
        skip=skip, limit=limit,
        condominium_id=condominium_id,
        unit_id=unit_id,
        ar_id=ar_id,
    )
    return response.dict()


@receipt_routes.get("/{id}")
@api_handler
def get_receipt(id: int) -> dict:
    response = ReceiptUseCase().get_by_id(id)
    return response.dict()


@receipt_routes.get("/uuid/{uuid}")
@api_handler
def get_receipt_by_uuid(uuid: str) -> dict:
    response = ReceiptUseCase().get_by_uuid(uuid)
    return response.dict()


@receipt_routes.get("/number/{receipt_number}")
@api_handler
def get_receipt_by_number(receipt_number: str) -> dict:
    response = ReceiptUseCase().get_by_receipt_number(receipt_number)
    return response.dict()


@receipt_routes.get("/unit/{unit_id}")
@api_handler
def list_receipts_by_unit(
    unit_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List all receipts for a specific unit."""
    response = ReceiptUseCase().list_by_unit(unit_id=unit_id, skip=skip, limit=limit)
    return response.dict()
