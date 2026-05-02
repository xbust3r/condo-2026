"""
Proration usecase — orchestrates DB queries + domain service to produce
a full proration breakdown for a charge.

This is the integration layer (FIN-05 + FIN-06):
  1. Resolve unit universe from DB based on charge scope
  2. Build UnitCoefficients from unit entities
  3. Call ProrationService.calculate()
  4. Return auditable ProrationBreakdown

No AR creation. No side effects on payments/receipts/ledger.
"""
from typing import Optional

from library.dddpy.core_charges.domain.charge_entity import ChargeEntity
from library.dddpy.core_charges.domain.proration_service import (
    ProrationService,
    ProrationBreakdown,
    UnitCoefficients,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ProrationUsecase")


class ProrationUsecase:
    """
    Application service that resolves the unit universe for a charge
    and delegates the actual math to ProrationService.
    """

    def __init__(self):
        logger.info("ProrationUsecase initialized")

    def generate_breakdown(self, charge: ChargeEntity) -> ProrationBreakdown:
        """
        Given a charge entity, query the relevant units and produce
        a proration breakdown.

        Args:
            charge: The charge entity with scope, amount, building_id, etc.

        Returns:
            ProrationBreakdown with per-unit allocations
        """
        logger.add_inside_method("generate_breakdown")
        logger.info(
            f"Generating breakdown for charge id={charge.id} "
            f"scope={charge.scope} amount={charge.amount}"
        )

        # 1. Resolve units based on scope
        units = self._resolve_units(charge)

        # 2. Build UnitCoefficients from unit entities
        coeffs = [
            UnitCoefficients(
                unit_id=u.id,
                building_id=u.building_id,
                coefficient=u.coefficient,
                condominium_coefficient=u.condominium_coefficient,
            )
            for u in units
        ]

        # 3. Delegate to pure domain service
        return ProrationService.calculate(
            charge_amount=charge.amount,
            scope=charge.scope,
            building_id=charge.building_id,
            distribution_mode=charge.distribution_mode,
            units=coeffs,
            charge_unit_id=charge.unit_id,
        )

    def _resolve_units(self, charge: ChargeEntity):
        """
        Query active units from DB based on charge scope.
        """
        from library.dddpy.core_units.infrastructure.unit_query_repository import (
            UnitQueryRepositoryImpl,
        )

        repo = UnitQueryRepositoryImpl()

        if charge.scope == "unit":
            # Single unit — fetch directly, must be active
            entity = repo.get_by_id(charge.unit_id)
            if not entity:
                raise ValueError(f"Unit id={charge.unit_id} not found")
            if not entity.is_active():
                raise ValueError(f"Unit id={charge.unit_id} is not active")
            return [entity]

        elif charge.scope == "building":
            # All active units in the building
            entities, _ = repo.list_all(
                building_id=charge.building_id,
                status=1,  # active
                include_deleted=False,
                limit=1000,
            )
            return entities

        elif charge.scope == "condominium":
            # All active units across all active buildings in the condominium
            # Query building-by-building to keep filtering in DB
            from library.dddpy.core_buildings.infrastructure.building_query_repository import (
                BuildingQueryRepositoryImpl,
            )
            building_repo = BuildingQueryRepositoryImpl()
            buildings, _ = building_repo.list_by_condominium(
                condominium_id=charge.condominium_id,
                status=1,
                limit=200,
            )

            all_units = []
            for b in buildings:
                units, _ = repo.list_all(
                    building_id=b.id,
                    status=1,
                    include_deleted=False,
                    limit=500,
                )
                all_units.extend(units)
            return all_units

        raise ValueError(f"Unknown scope: {charge.scope}")
