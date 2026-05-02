"""
Proration domain service — pure calculation of charge distribution across units.

No side effects. No DB access. No AR creation.
Input: charge amount + scope + universe of units + coefficients
Output: auditable breakdown of {unit_id, amount, coefficient_used, residual_assigned}
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional


@dataclass(frozen=True)
class UnitCoefficients:
    """Coefficient data for one unit, used as input to proration."""
    unit_id: int
    building_id: int
    coefficient: Optional[Decimal] = None
    condominium_coefficient: Optional[Decimal] = None


@dataclass(frozen=True)
class ProrationEntry:
    """One unit's share of a prorated charge."""
    unit_id: int
    amount: Decimal
    coefficient_used: Decimal
    coefficient_type: str  # 'coefficient' | 'condominium_coefficient' | 'fixed'
    is_residual_beneficiary: bool = False


@dataclass(frozen=True)
class ProrationBreakdown:
    """Complete breakdown of a proration calculation (auditable)."""
    charge_total: Decimal
    entries: List[ProrationEntry]
    residual_assigned: Decimal  # cents assigned via deterministic rule
    units_omitted: int = 0  # units skipped (no coefficient, inactive, etc.)

    def total_assigned(self) -> Decimal:
        return sum((e.amount for e in self.entries), Decimal("0.00"))


class ProrationService:
    """
    Pure domain service that distributes a charge amount across units
    according to their coefficients.

    Scope rules:
      - unit:          one unit only, no proration
      - building:      units in the same building, using coefficient
      - condominium:   all units in the condominium, using condominium_coefficient

    Distribution modes:
      - fixed_unit_amount:            charge amount applied directly (no coefficient)
      - prorated_by_building_coefficient:     charge ÷ Σ(coefficient) × unit.coefficient
      - prorated_by_condominium_coefficient:  charge ÷ Σ(condominium_coefficient) × unit.condominium_coefficient
    """

    @staticmethod
    def calculate(
        charge_amount: Decimal,
        scope: str,
        building_id: Optional[int],
        distribution_mode: str,
        units: List[UnitCoefficients],
        charge_unit_id: Optional[int] = None,
    ) -> ProrationBreakdown:
        """
        Calculate prorated amounts for a charge across affected units.

        Args:
            charge_amount: Total charge amount to distribute
            scope: 'unit' | 'building' | 'condominium'
            building_id: Building id (required when scope='building')
            distribution_mode: 'fixed_unit_amount' | 'prorated_by_building_coefficient' | 'prorated_by_condominium_coefficient'
            units: All candidate units with their coefficients
            charge_unit_id: Specific unit id (required when scope='unit')

        Returns:
            ProrationBreakdown with per-unit allocations
        """
        # 1. Filter units by scope
        if scope == "unit":
            if charge_unit_id is None:
                raise ValueError("charge_unit_id is required when scope='unit'")
            affected = [u for u in units if u.unit_id == charge_unit_id]
        elif scope == "building":
            if building_id is None:
                raise ValueError("building_id is required when scope='building'")
            affected = [u for u in units if u.building_id == building_id]
        elif scope == "condominium":
            affected = list(units)
        else:
            raise ValueError(f"Unknown scope: {scope}")

        omitted = len(units) - len(affected)

        # 2. Handle fixed amount (no proration needed)
        if distribution_mode == "fixed_unit_amount":
            entries = [
                ProrationEntry(
                    unit_id=u.unit_id,
                    amount=charge_amount,
                    coefficient_used=Decimal("1.0"),
                    coefficient_type="fixed",
                )
                for u in affected
            ]
            return ProrationBreakdown(
                charge_total=charge_amount,
                entries=entries,
                residual_assigned=Decimal("0.00"),
                units_omitted=omitted,
            )

        # 3. Determine which coefficient to use
        if distribution_mode == "prorated_by_building_coefficient":
            coeff_attr = "coefficient"
            coeff_type = "coefficient"
        elif distribution_mode == "prorated_by_condominium_coefficient":
            coeff_attr = "condominium_coefficient"
            coeff_type = "condominium_coefficient"
        else:
            raise ValueError(f"Unknown distribution_mode: {distribution_mode}")

        # 4. Collect coefficient data, skip units with no coefficient
        unit_coeffs: List[tuple] = []  # (unit_id, coefficient_value)
        skipped = 0
        for u in affected:
            val = getattr(u, coeff_attr, None)
            if val is None or val <= 0:
                skipped += 1
                continue
            unit_coeffs.append((u.unit_id, val))

        if not unit_coeffs:
            raise ValueError(
                f"No units with valid {coeff_attr} found for proration"
            )

        total_coeff = sum((c for _, c in unit_coeffs), Decimal("0"))

        # 5. Prorate using Decimal for precision; work in fractional units
        allocated = Decimal("0.00")
        raw_allocations: List[tuple] = []  # (unit_id, raw_amount, coefficient)

        for unit_id, coeff in unit_coeffs:
            share = (charge_amount * coeff / total_coeff).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            allocated += share
            raw_allocations.append((unit_id, share, coeff))

        # 6. Calculate residual (difference between total and sum of rounded shares)
        residual = charge_amount - allocated

        # Distribute residual to the unit with highest coefficient
        # (deterministic tie-break: first unit with highest coeff wins)
        residual_beneficiary_idx = max(
            range(len(raw_allocations)),
            key=lambda i: raw_allocations[i][2],
        )

        # Build entries, apply residual to beneficiary
        entries = []
        for idx, (unit_id, share, coeff) in enumerate(raw_allocations):
            is_beneficiary = (idx == residual_beneficiary_idx and residual != 0)
            final_amount = share + residual if is_beneficiary else share
            entries.append(ProrationEntry(
                unit_id=unit_id,
                amount=final_amount,
                coefficient_used=coeff,
                coefficient_type=coeff_type,
                is_residual_beneficiary=is_beneficiary,
            ))

        return ProrationBreakdown(
            charge_total=charge_amount,
            entries=entries,
            residual_assigned=residual,
            units_omitted=omitted + skipped,
        )
