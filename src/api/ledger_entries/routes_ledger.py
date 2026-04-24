# =============================================================================
# API Routes: core_ledger_entries
# Módulo de libro mayor financiero por unidad (append-only)
#
# Endpoints:
#   POST   /ledger-entries                    — append entry
#   POST   /ledger-entries/batch             — append multiple entries
#   GET    /ledger-entries/{id}            — get by id
#   GET    /ledger-entries/uuid/{uuid}      — get by uuid
#   GET    /ledger-entries/unit/{unit_id}   — get unit ledger
#   GET    /ledger-entries/unit/{unit_id}/summary — balance summary
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_ledger_entries.usecase.ledger_usecase import LedgerUseCase
from library.dddpy.core_ledger_entries.usecase.ledger_cmd_schema import CreateLedgerEntrySchema
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/ledger-entries"

ledger_routes = APIRouter(prefix=PREFIX)


@ledger_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_ledger_entries"}


@ledger_routes.post("")
@api_handler
def create_ledger_entry(request: CreateLedgerEntrySchema) -> dict:
    """
    Append a ledger entry to a unit's financial ledger.

    The running balance is computed automatically.
    Ledger is append-only: entries are never modified or deleted,
    only new ones are added.
    """
    response = LedgerUseCase().create(request)
    return response.dict()


@ledger_routes.post("/batch")
@api_handler
def create_ledger_entries_batch(requests: list[CreateLedgerEntrySchema]) -> dict:
    """Append multiple ledger entries atomically."""
    response = LedgerUseCase().create_batch(requests)
    return response.dict()


@ledger_routes.get("/{id}")
@api_handler
def get_ledger_entry(id: int) -> dict:
    response = LedgerUseCase().get_by_id(id)
    return response.dict()


@ledger_routes.get("/uuid/{uuid}")
@api_handler
def get_ledger_entry_by_uuid(uuid: str) -> dict:
    response = LedgerUseCase().get_by_uuid(uuid)
    return response.dict()


@ledger_routes.get("/unit/{unit_id}")
@api_handler
def get_unit_ledger(
    unit_id: int,
    period: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """
    Get the complete financial ledger for a unit.

    Returns entries in chronological order with running balance.
    Optionally filter by period (YYYY-MM).
    """
    response = LedgerUseCase().list_by_unit(
        unit_id=unit_id,
        skip=skip,
        limit=limit,
        period=period,
    )
    return response.dict()


@ledger_routes.get("/unit/{unit_id}/summary")
@api_handler
def get_unit_balance_summary(unit_id: int) -> dict:
    """
    Get balance summary for a unit:
    - total_debt (sum of all debits)
    - total_paid (sum of all credits)
    - current_balance (debt - paid)
    - charge_count, payment_count
    """
    response = LedgerUseCase().get_balance_summary(unit_id)
    return response.dict()
