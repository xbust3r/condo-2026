"""
Dashboard API routes — executive reporting for condominiums.

Query-only facade: no domain entities, no repositories.
Aggregates data from existing modules.
"""
from fastapi import APIRouter, Depends

from api.auth.auth_dependencies import get_current_user
from library.dddpy.core_dashboards.usecase.finance_dashboard_usecase import (
    FinanceDashboardUseCase,
)
from library.dddpy.core_dashboards.usecase.operations_dashboard_usecase import (
    OperationsDashboardUseCase,
)


PREFIX = "/condominiums"
dashboard_routes = APIRouter(prefix=PREFIX)


@dashboard_routes.get("/{condominium_id}/finance")
def get_finance_dashboard(
    condominium_id: int,
    user=Depends(get_current_user),
) -> dict:
    """
    Financial dashboard for a condominium.

    Returns accounts receivable aging, collections this month,
    recent payments, and charges breakdown.
    """
    usecase = FinanceDashboardUseCase()
    return usecase.get_dashboard(condominium_id)


@dashboard_routes.get("/{condominium_id}/operations")
def get_operations_dashboard(
    condominium_id: int,
    user=Depends(get_current_user),
) -> dict:
    """
    Operations dashboard for a condominium.

    Returns open incidents (by priority/category), visitor counts
    (today and this week), and package delivery status.
    """
    usecase = OperationsDashboardUseCase()
    return usecase.get_dashboard(condominium_id)
