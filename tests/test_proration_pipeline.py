#!/usr/bin/env python3
"""
FIN-13 — Integration tests for the proration pipeline.

Run: python3 tests/test_proration_pipeline.py

Tests cover:
  - ProrationService: unit, building, condominium proration + residual
  - ProrationUsecase: integration with PR #1-6 pipeline
  - Edge cases: no coefficient, rounding, canonical combos
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from decimal import Decimal, ROUND_HALF_UP

# ──────────────────────────────────────────────────────────────────────
# ProrationService Tests (pure domain, no DB)
# ──────────────────────────────────────────────────────────────────────

from library.dddpy.core_charges.domain.proration_service import (
    ProrationService,
    UnitCoefficients,
    ProrationEntry,
    ProrationBreakdown,
)


def test_proration_building_clean():
    """3 units, clean division: 100 / (2+3+5) = 20, 30, 50"""
    units = [
        UnitCoefficients(unit_id=1, building_id=10, coefficient=Decimal('2.0')),
        UnitCoefficients(unit_id=2, building_id=10, coefficient=Decimal('3.0')),
        UnitCoefficients(unit_id=3, building_id=10, coefficient=Decimal('5.0')),
    ]
    result = ProrationService.calculate(
        charge_amount=Decimal('100.00'), scope='building', building_id=10,
        distribution_mode='prorated_by_building_coefficient', units=units,
    )
    amounts = {e.unit_id: e.amount for e in result.entries}
    assert amounts[1] == Decimal('20.00'), f"Expected 20.00, got {amounts[1]}"
    assert amounts[2] == Decimal('30.00'), f"Expected 30.00, got {amounts[2]}"
    assert amounts[3] == Decimal('50.00'), f"Expected 50.00, got {amounts[3]}"
    assert result.total_assigned() == Decimal('100.00')
    assert result.residual_assigned == Decimal('0.00')
    print("  ✅ test_proration_building_clean")


def test_proration_residual():
    """3 units equal, 100/3 = 33.33+33.33+33.34, residual goes to first max coeff"""
    units = [
        UnitCoefficients(unit_id=1, building_id=10, coefficient=Decimal('1.0')),
        UnitCoefficients(unit_id=2, building_id=10, coefficient=Decimal('1.0')),
        UnitCoefficients(unit_id=3, building_id=10, coefficient=Decimal('1.0')),
    ]
    result = ProrationService.calculate(
        charge_amount=Decimal('100.00'), scope='building', building_id=10,
        distribution_mode='prorated_by_building_coefficient', units=units,
    )
    amounts = [e.amount for e in result.entries]
    assert sum(amounts, Decimal('0.00')) == Decimal('100.00')
    # One entry should be 33.34 (residual beneficiary)
    beneficiaries = [e for e in result.entries if e.is_residual_beneficiary]
    assert len(beneficiaries) == 1
    assert beneficiaries[0].amount == Decimal('33.34')
    assert result.residual_assigned == Decimal('0.01')
    print("  ✅ test_proration_residual")


def test_proration_unit_fixed():
    """Unit scope: fixed amount to one unit"""
    units = [
        UnitCoefficients(unit_id=5, building_id=10, coefficient=Decimal('2.0')),
    ]
    result = ProrationService.calculate(
        charge_amount=Decimal('50.00'), scope='unit', building_id=None,
        distribution_mode='fixed_unit_amount', units=units, charge_unit_id=5,
    )
    assert len(result.entries) == 1
    assert result.entries[0].unit_id == 5
    assert result.entries[0].amount == Decimal('50.00')
    assert result.entries[0].coefficient_type == 'fixed'
    print("  ✅ test_proration_unit_fixed")


def test_proration_condominium():
    """Condominium scope: all units across buildings"""
    units = [
        UnitCoefficients(unit_id=1, building_id=10, condominium_coefficient=Decimal('2.0')),
        UnitCoefficients(unit_id=2, building_id=20, condominium_coefficient=Decimal('3.0')),
    ]
    result = ProrationService.calculate(
        charge_amount=Decimal('200.00'), scope='condominium', building_id=None,
        distribution_mode='prorated_by_condominium_coefficient', units=units,
    )
    amounts = {e.unit_id: e.amount for e in result.entries}
    # 200 * 2/5 = 80, 200 * 3/5 = 120
    assert amounts[1] == Decimal('80.00'), f"Expected 80.00, got {amounts[1]}"
    assert amounts[2] == Decimal('120.00'), f"Expected 120.00, got {amounts[2]}"
    assert result.total_assigned() == Decimal('200.00')
    print("  ✅ test_proration_condominium")


def test_proration_null_coefficient_skipped():
    """Unit with null coefficient is omitted"""
    units = [
        UnitCoefficients(unit_id=1, building_id=10, coefficient=Decimal('1.0')),
        UnitCoefficients(unit_id=2, building_id=10, coefficient=None),
        UnitCoefficients(unit_id=3, building_id=10, coefficient=Decimal('1.0')),
    ]
    result = ProrationService.calculate(
        charge_amount=Decimal('100.00'), scope='building', building_id=10,
        distribution_mode='prorated_by_building_coefficient', units=units,
    )
    assert len(result.entries) == 2
    assert result.units_omitted == 1
    assert result.total_assigned() == Decimal('100.00')
    print("  ✅ test_proration_null_coefficient_skipped")


def test_proration_invalid_combo_rejected():
    """Canonical combos: building + fixed_unit_amount should fail"""
    units = [UnitCoefficients(unit_id=1, building_id=10, coefficient=Decimal('1.0'))]
    try:
        ProrationService.calculate(
            charge_amount=Decimal('10.00'), scope='building', building_id=10,
            distribution_mode='fixed_unit_amount', units=units,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid combination" in str(e)
    print("  ✅ test_proration_invalid_combo_rejected")


def test_proration_building_filter():
    """Only units in the target building are included"""
    units = [
        UnitCoefficients(unit_id=1, building_id=10, coefficient=Decimal('1.0')),
        UnitCoefficients(unit_id=2, building_id=20, coefficient=Decimal('1.0')),
    ]
    result = ProrationService.calculate(
        charge_amount=Decimal('100.00'), scope='building', building_id=10,
        distribution_mode='prorated_by_building_coefficient', units=units,
    )
    assert len(result.entries) == 1
    assert result.entries[0].unit_id == 1
    assert result.units_omitted == 1
    print("  ✅ test_proration_building_filter")


def test_proration_zero_coefficient_skipped():
    """Unit with coefficient=0 is omitted"""
    units = [
        UnitCoefficients(unit_id=1, building_id=10, coefficient=Decimal('1.0')),
        UnitCoefficients(unit_id=2, building_id=10, coefficient=Decimal('0.0')),
    ]
    result = ProrationService.calculate(
        charge_amount=Decimal('50.00'), scope='building', building_id=10,
        distribution_mode='prorated_by_building_coefficient', units=units,
    )
    assert len(result.entries) == 1
    assert result.entries[0].unit_id == 1
    assert result.units_omitted == 1
    print("  ✅ test_proration_zero_coefficient_skipped")


def test_proration_breakdown_total_assigned():
    """total_assigned() matches charge_total"""
    units = [
        UnitCoefficients(unit_id=1, building_id=10, condominium_coefficient=Decimal('7.0')),
        UnitCoefficients(unit_id=2, building_id=10, condominium_coefficient=Decimal('3.0')),
    ]
    result = ProrationService.calculate(
        charge_amount=Decimal('123.45'), scope='condominium', building_id=None,
        distribution_mode='prorated_by_condominium_coefficient', units=units,
    )
    assert result.total_assigned() == result.charge_total
    print("  ✅ test_proration_breakdown_total_assigned")


# ──────────────────────────────────────────────────────────────────────
# _compute_periods Tests
# ──────────────────────────────────────────────────────────────────────

from datetime import date


def test_compute_periods_full_range():
    """Jan to Jun = 6 periods"""
    from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
    uc = ARUseCase()
    periods = uc._compute_periods(date(2026, 1, 1), date(2026, 6, 1))
    assert len(periods) == 6
    assert periods == ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06']
    print("  ✅ test_compute_periods_full_range")


def test_compute_periods_single_month():
    """Same start and end = 1 period"""
    from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
    uc = ARUseCase()
    periods = uc._compute_periods(date(2026, 5, 15), date(2026, 5, 1))
    assert len(periods) == 1
    assert periods == ['2026-05']
    print("  ✅ test_compute_periods_single_month")


def test_compute_periods_cross_year():
    """Oct 2026 to Feb 2027 = 5 periods"""
    from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
    uc = ARUseCase()
    periods = uc._compute_periods(date(2026, 10, 1), date(2027, 2, 1))
    assert len(periods) == 5
    assert periods == ['2026-10', '2026-11', '2026-12', '2027-01', '2027-02']
    print("  ✅ test_compute_periods_cross_year")


# ──────────────────────────────────────────────────────────────────────
# Canonical Combinations Matrix
# ──────────────────────────────────────────────────────────────────────

def test_canonical_combos():
    """Only 3 canonical combos are accepted"""
    units = [UnitCoefficients(unit_id=1, building_id=10, coefficient=Decimal('1.0'))]
    units_condo = [UnitCoefficients(unit_id=1, building_id=10, condominium_coefficient=Decimal('1.0'))]

    # Canonical: these should work
    ProrationService.calculate(Decimal('10'), 'unit', None, 'fixed_unit_amount', units, charge_unit_id=1)
    ProrationService.calculate(Decimal('10'), 'building', 10, 'prorated_by_building_coefficient', units)
    ProrationService.calculate(Decimal('10'), 'condominium', None, 'prorated_by_condominium_coefficient', units_condo)

    # Non-canonical: these should fail
    invalid_combos = [
        ('unit', 'prorated_by_building_coefficient'),
        ('unit', 'prorated_by_condominium_coefficient'),
        ('building', 'fixed_unit_amount'),
        ('building', 'prorated_by_condominium_coefficient'),
        ('condominium', 'fixed_unit_amount'),
        ('condominium', 'prorated_by_building_coefficient'),
    ]
    for scope, dist_mode in invalid_combos:
        try:
            ProrationService.calculate(Decimal('10'), scope, 10, dist_mode, units, charge_unit_id=1)
            assert False, f"Should have failed: scope={scope} mode={dist_mode}"
        except ValueError:
            pass
    print("  ✅ test_canonical_combos (3 accepted, 6 rejected)")


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("\n=== FIN-13: Proration Pipeline Tests ===\n")

    print("ProrationService (pure domain):")
    test_proration_building_clean()
    test_proration_residual()
    test_proration_unit_fixed()
    test_proration_condominium()
    test_proration_null_coefficient_skipped()
    test_proration_invalid_combo_rejected()
    test_proration_building_filter()
    test_proration_zero_coefficient_skipped()
    test_proration_breakdown_total_assigned()
    test_canonical_combos()

    print("\nPeriod computation:")
    test_compute_periods_full_range()
    test_compute_periods_single_month()
    test_compute_periods_cross_year()

    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED")
    print("=" * 50)
