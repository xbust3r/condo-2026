"""
API Routes: balances — aggregated balance with separate rubros.

Endpoints:
  GET /balances/condominium/{condominium_id}  — consolidated condominium balance
  GET /balances/building/{building_id}        — building-level balance
  GET /balances/unit/{unit_id}                — unit-level balance
"""
from fastapi import APIRouter, Depends

from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
    BalanceSummaryUseCase,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/balances"
balance_routes = APIRouter(prefix=PREFIX)


@balance_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_balance_summary"}


@balance_routes.get("/condominium/{condominium_id}")
@api_handler
def get_condominium_balance(condominium_id: int) -> dict:
    """
    Balance consolidado del condominio con rubros separados:

    - maintenance:         Cargos de mantenimiento
    - amenity_bookings:    Ingresos por reservas de áreas comunes
    - security_deposits:   Garantías en custodia (pasivo, no ingreso)
    """
    usecase = BalanceSummaryUseCase()
    return usecase.get_condominium_balance(condominium_id)


@balance_routes.get("/building/{building_id}")
@api_handler
def get_building_balance(building_id: int) -> dict:
    """
    Balance de edificio con rubros separados:

    - maintenance:         Cargos de mantenimiento del edificio
    - amenity_bookings:    Ingresos por reservas de áreas comunes del edificio
    - security_deposits:   Garantías en custodia del edificio (pasivo)
    """
    usecase = BalanceSummaryUseCase()
    return usecase.get_building_balance(building_id)


@balance_routes.get("/unit/{unit_id}")
@api_handler
def get_unit_balance(unit_id: int) -> dict:
    """
    Balance de unidad con rubros separados:

    - maintenance:         Cargos de mantenimiento de la unidad
    - amenity_bookings:    Ingresos por reservas de áreas comunes de la unidad
    - security_deposits:   Garantías en custodia de la unidad (pasivo)

    Incluye contexto de edificio y condominio para trazabilidad.
    """
    usecase = BalanceSummaryUseCase()
    return usecase.get_unit_balance(unit_id)
