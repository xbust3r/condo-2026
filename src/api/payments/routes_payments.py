# =============================================================================
# API Routes: core_payments
# Módulo de pagos contra cuentas por cobrar
#
# Endpoints:
#   POST   /payments                      — register payment + generate receipt
#   GET    /payments                      — list with filters
#   GET    /payments/{id}                — get by id
#   GET    /payments/uuid/{uuid}        — get by uuid
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_payments.usecase.payment_usecase import PaymentUseCase
from library.dddpy.core_payments.usecase.payment_cmd_schema import CreatePaymentSchema
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/payments"

payment_routes = APIRouter(prefix=PREFIX)


@payment_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_payments"}


@payment_routes.post("")
@api_handler
def create_payment(request: CreatePaymentSchema) -> dict:
    """
    Register a payment against an AR.

    Automatically:
      - Generates a sequential receipt number (C{condo}-{YYYYMM}-{NNNNNN})
      - Creates a receipt
      - Updates AR status (pending→partial, partial→paid, overdue→partial)
      - Validates PAY-01: amount ≤ pending balance
    """
    response = PaymentUseCase().create_with_ar_update(request)
    return response.dict()


@payment_routes.get("")
@api_handler
def list_payments(
    condominium_id: Optional[int] = Query(None),
    unit_id: Optional[int] = Query(None),
    ar_id: Optional[int] = Query(None),
    include_deleted: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List payments with optional filters."""
    response = PaymentUseCase().list_all(
        skip=skip, limit=limit,
        condominium_id=condominium_id,
        unit_id=unit_id,
        ar_id=ar_id,
        include_deleted=include_deleted,
    )
    return response.dict()


@payment_routes.get("/{id}")
@api_handler
def get_payment(id: int) -> dict:
    response = PaymentUseCase().get_by_id(id)
    return response.dict()


@payment_routes.get("/uuid/{uuid}")
@api_handler
def get_payment_by_uuid(uuid: str) -> dict:
    response = PaymentUseCase().get_by_uuid(uuid)
    return response.dict()
