"""
Unit tests: resident dashboard — payment_pending_total with ownership + occupancy.

Validates the deduplication logic in get_dashboard_summary() per the
business rule defined in docs/BULMA/task-payment-occupancy-20260503.md.

Cases:
  1. Only owner          → sees debt via ownership
  2. Only active tenant  → sees debt via active occupancy
  3. Owner + tenant same unit → no duplication
  4. Expired occupancy   → excluded from calculation
  5. User with multiple valid units → correct summed total
"""
import pytest
import uuid as _uuid
from datetime import date, datetime, timedelta
from decimal import Decimal


# ── Helpers ─────────────────────────────────────────────────────────────

from tests.factories.condo_factory import CondoFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.unit_factory import UnitFactory
from tests.factories.user_factory import UserFactory


def _create_ar(session, condominium_id: int, unit_id: int, debtor_user_id: int,
               amount: Decimal, status: str = "pending", paid_amount: Decimal = None):
    """Insert an AR record directly."""
    from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
    ar = DBAR(
        uuid=str(_uuid.uuid4()),
        condominium_id=condominium_id,
        unit_id=unit_id,
        debtor_user_id=debtor_user_id,
        reference_code=f"TEST-AR-{_uuid.uuid4().hex[:8]}",
        description="Test AR",
        amount=amount,
        paid_amount=paid_amount or Decimal("0.00"),
        currency="PEN",
        status=status,
        due_date=date.today() + timedelta(days=30),
        origin_type="charge",
    )
    session.add(ar)
    session.flush()
    return ar


def _create_ownership(session, unit_id: int, user_id: int):
    """Insert a unit ownership record."""
    from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
    ownership = DBUnitOwnership(
        uuid=str(_uuid.uuid4()),
        unit_id=unit_id,
        user_id=user_id,
        ownership_type="owner",
        ownership_percentage=Decimal("100.00"),
        status="active",
    )
    session.add(ownership)
    session.flush()
    return ownership


def _create_occupancy(session, unit_id: int, user_id: int, end_date=None):
    """Insert a unit occupancy record via raw SQL. end_date=None means active.
    
    Bypasses the SQLAlchemy model layer because occupancy_type_id requires
    a FK to core_occupancy_types which may not exist in test data.
    """
    from sqlalchemy import text
    occ_uuid = str(_uuid.uuid4())
    session.execute(text("""
        INSERT INTO core_unit_occupancies (uuid, unit_id, user_id, occupancy_type_id,
                start_date, end_date, status)
        SELECT :uuid, :unit_id, :user_id, COALESCE(
            (SELECT id FROM core_occupancy_types WHERE code = 'owner' LIMIT 1),
            (SELECT id FROM core_occupancy_types LIMIT 1),
            1
        ), :start_date, :end_date, :status
    """), {
        "uuid": occ_uuid,
        "unit_id": unit_id,
        "user_id": user_id,
        "start_date": date.today() - timedelta(days=60),
        "end_date": end_date,
        "status": "active" if end_date is None else "inactive",
    })
    session.flush()

    row = session.execute(text(
        "SELECT id, uuid FROM core_unit_occupancies WHERE uuid = :uuid"
    ), {"uuid": occ_uuid}).fetchone()
    return type("Occupancy", (), {"id": row.id, "uuid": row.uuid})()


def _get_payment_pending(user_id: int, condominium_id: int) -> float:
    """Call get_dashboard_summary and return payment_pending_total.
    
    Data must be committed before calling — session_scope() opens its own
    DB session which reads committed data.
    """
    from library.dddpy.core_residents.infrastructure.resident_query_repository import (
        ResidentQueryRepositoryImpl,
    )
    repo = ResidentQueryRepositoryImpl()
    summary = repo.get_dashboard_summary(user_id, condominium_id)
    return summary["payment_pending_total"]


_CASCADE_TABLES = [
    "core_accounts_receivable",
    "core_unit_ownerships",
    "core_unit_occupancies",
    "core_units",
    "core_buildings",
    "core_condominiums",
]

def _cleanup_by_condo(db_session, condo_id: int):
    from sqlalchemy import text
    for table in _CASCADE_TABLES:
        try:
            db_session.execute(
                text(f"DELETE FROM {table} WHERE condominium_id = :cid"),
                {"cid": condo_id},
            )
        except Exception:
            pass
    db_session.commit()


# ── Tests ───────────────────────────────────────────────────────────────

class TestPaymentPendingOwnerOnly:
    """Case 1: Only owner (ownership, no occupancy)."""

    def test_owner_sees_debt(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso 1 — Owner")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-O", name="Torre Owner")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="101", code="U-O-01")
        user = UserFactory.create(db_session, email=f"owner-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit.id, user.id)
        _create_ar(db_session, condo.id, unit.id, user.id, Decimal("350.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 350.0, f"Owner should see 350.00 debt, got {pending}"

        _cleanup_by_condo(db_session, condo.id)

    def test_owner_no_debt(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso 1b — Owner no debt")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-O2", name="Torre Owner 2")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="201", code="U-O-02")
        user = UserFactory.create(db_session, email=f"owner2-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit.id, user.id)
        # No AR created — should be 0
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 0.0, f"Owner with no AR should have 0 debt, got {pending}"

        _cleanup_by_condo(db_session, condo.id)


class TestPaymentPendingTenantOnly:
    """Case 2: Only active tenant (occupancy, no ownership)."""

    def test_active_tenant_sees_debt(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso 2 — Tenant")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-T", name="Torre Tenant")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="301", code="U-T-01")
        user = UserFactory.create(db_session, email=f"tenant-{_uuid.uuid4().hex[:8]}@test.local")

        _create_occupancy(db_session, unit.id, user.id)  # active = no end_date
        _create_ar(db_session, condo.id, unit.id, user.id, Decimal("500.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 500.0, f"Active tenant should see 500.00 debt, got {pending}"

        _cleanup_by_condo(db_session, condo.id)

    def test_active_tenant_no_debt(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso 2b — Tenant no debt")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-T2", name="Torre Tenant 2")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="302", code="U-T-02")
        user = UserFactory.create(db_session, email=f"tenant2-{_uuid.uuid4().hex[:8]}@test.local")

        _create_occupancy(db_session, unit.id, user.id)
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 0.0, f"Active tenant with no AR should have 0 debt, got {pending}"

        _cleanup_by_condo(db_session, condo.id)


class TestPaymentPendingDualLink:
    """Case 3: Owner + active occupant of the SAME unit → NO duplication."""

    def test_dual_link_no_duplication(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso 3 — Dual Link")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-D", name="Torre Dual")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="401", code="U-D-01")
        user = UserFactory.create(db_session, email=f"dual-{_uuid.uuid4().hex[:8]}@test.local")

        # Same user is both owner AND active occupant of the same unit
        _create_ownership(db_session, unit.id, user.id)
        _create_occupancy(db_session, unit.id, user.id)  # active
        _create_ar(db_session, condo.id, unit.id, user.id, Decimal("600.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 600.0, (
            f"Dual link should NOT duplicate debt. Expected 600.00, got {pending}"
        )

        _cleanup_by_condo(db_session, condo.id)

    def test_dual_link_multiple_ar_no_duplication(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso 3b — Dual Link multi AR")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-D2", name="Torre Dual 2")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="402", code="U-D-02")
        user = UserFactory.create(db_session, email=f"dual2-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit.id, user.id)
        _create_occupancy(db_session, unit.id, user.id)
        _create_ar(db_session, condo.id, unit.id, user.id, Decimal("250.00"))
        _create_ar(db_session, condo.id, unit.id, user.id, Decimal("150.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 400.0, (
            f"Dual link with 2 ARs should sum to 400.00, got {pending}"
        )

        _cleanup_by_condo(db_session, condo.id)


class TestPaymentPendingExpiredOccupancy:
    """Case 4: Expired occupancy → excluded from calculation."""

    def test_expired_occupancy_excluded(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso 4 — Expired Occ")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-E", name="Torre Expired")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="501", code="U-E-01")
        user = UserFactory.create(db_session, email=f"expired-{_uuid.uuid4().hex[:8]}@test.local")

        # Occupancy that ended 30 days ago
        _create_occupancy(
            db_session, unit.id, user.id,
            end_date=date.today() - timedelta(days=30),
        )
        _create_ar(db_session, condo.id, unit.id, user.id, Decimal("700.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 0.0, (
            f"Expired occupancy should be excluded. Expected 0.00, got {pending}"
        )

        _cleanup_by_condo(db_session, condo.id)

    def test_expired_occupancy_still_no_ownership(self, db_session):
        """User with expired occupancy and no ownership should see 0 debt."""
        condo = CondoFactory.create(db_session, name="Caso 4b — Expired no link")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-E2", name="Torre Expired 2")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="502", code="U-E-02")
        user = UserFactory.create(db_session, email=f"exp-nolink-{_uuid.uuid4().hex[:8]}@test.local")

        _create_occupancy(
            db_session, unit.id, user.id,
            end_date=date.today() - timedelta(days=90),
        )
        # No ownership — only expired occupancy
        _create_ar(db_session, condo.id, unit.id, user.id, Decimal("800.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 0.0, (
            f"User with only expired occupancy should have 0 debt, got {pending}"
        )

        _cleanup_by_condo(db_session, condo.id)


class TestPaymentPendingMultipleUnits:
    """Case 5: User with multiple valid units → correct summed total."""

    def test_multiple_units_sum_correctly(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso 5 — Multi Unit")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-M", name="Torre Multi")
        unit_a = UnitFactory.create(db_session, building_id=bldg.id, unit_number="601", code="U-M-01")
        unit_b = UnitFactory.create(db_session, building_id=bldg.id, unit_number="602", code="U-M-02")
        user = UserFactory.create(db_session, email=f"multi-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit_a.id, user.id)
        _create_ownership(db_session, unit_b.id, user.id)
        _create_ar(db_session, condo.id, unit_a.id, user.id, Decimal("300.00"))
        _create_ar(db_session, condo.id, unit_b.id, user.id, Decimal("450.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 750.0, (
            f"Multiple units should sum to 750.00, got {pending}"
        )

        _cleanup_by_condo(db_session, condo.id)

    def test_mixed_links_across_units(self, db_session):
        """Unit A via ownership, Unit B via occupancy → correct sum, no cross-duplication."""
        condo = CondoFactory.create(db_session, name="Caso 5b — Mixed Links")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-M2", name="Torre Mixed")
        unit_a = UnitFactory.create(db_session, building_id=bldg.id, unit_number="701", code="U-M-03")
        unit_b = UnitFactory.create(db_session, building_id=bldg.id, unit_number="702", code="U-M-04")
        user = UserFactory.create(db_session, email=f"mixed-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit_a.id, user.id)        # unit A = owner
        _create_occupancy(db_session, unit_b.id, user.id)         # unit B = active tenant
        _create_ar(db_session, condo.id, unit_a.id, user.id, Decimal("200.00"))
        _create_ar(db_session, condo.id, unit_b.id, user.id, Decimal("300.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 500.0, (
            f"Mixed links across units should sum to 500.00, got {pending}"
        )

        _cleanup_by_condo(db_session, condo.id)

    def test_mixed_links_one_unit_dual(self, db_session):
        """Unit A: ownership only. Unit B: ownership + occupancy (dual). Correct sum, no dup."""
        condo = CondoFactory.create(db_session, name="Caso 5c — Mixed + Dual")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-M3", name="Torre MxDual")
        unit_a = UnitFactory.create(db_session, building_id=bldg.id, unit_number="801", code="U-M-05")
        unit_b = UnitFactory.create(db_session, building_id=bldg.id, unit_number="802", code="U-M-06")
        user = UserFactory.create(db_session, email=f"mxdual-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit_a.id, user.id)         # Unit A: owner
        _create_ownership(db_session, unit_b.id, user.id)         # Unit B: owner
        _create_occupancy(db_session, unit_b.id, user.id)         # Unit B: also occupant (dual)
        _create_ar(db_session, condo.id, unit_a.id, user.id, Decimal("100.00"))
        _create_ar(db_session, condo.id, unit_b.id, user.id, Decimal("200.00"))
        _create_ar(db_session, condo.id, unit_b.id, user.id, Decimal("50.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        # Unit A: 100. Unit B: 200+50 = 250. Total: 350
        assert pending == 350.0, (
            f"Mixed + dual should sum to 350.00 (no AR duplication), got {pending}"
        )

        _cleanup_by_condo(db_session, condo.id)


class TestPaymentPendingPaidExcluded:
    """Paid and cancelled AR should always be excluded."""

    def test_paid_ar_excluded(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso Paid")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-P", name="Torre Paid")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="901", code="U-P-01")
        user = UserFactory.create(db_session, email=f"paid-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit.id, user.id)
        _create_ar(db_session, condo.id, unit.id, user.id,
                   Decimal("350.00"), status="paid", paid_amount=Decimal("350.00"))
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 0.0, f"Paid AR should be excluded, got {pending}"

        _cleanup_by_condo(db_session, condo.id)

    def test_cancelled_ar_excluded(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso Cancelled")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-C", name="Torre Cancel")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="1001", code="U-C-01")
        user = UserFactory.create(db_session, email=f"cancel-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit.id, user.id)
        _create_ar(db_session, condo.id, unit.id, user.id,
                   Decimal("350.00"), status="cancelled")
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 0.0, f"Cancelled AR should be excluded, got {pending}"

        _cleanup_by_condo(db_session, condo.id)

    def test_mixed_pending_and_paid(self, db_session):
        condo = CondoFactory.create(db_session, name="Caso Mixed Paid")
        bldg = BuildingFactory.create(db_session, condominium_id=condo.id, code="BLD-MP", name="Torre MixPaid")
        unit = UnitFactory.create(db_session, building_id=bldg.id, unit_number="1101", code="U-MP-01")
        user = UserFactory.create(db_session, email=f"mixpaid-{_uuid.uuid4().hex[:8]}@test.local")

        _create_ownership(db_session, unit.id, user.id)
        _create_ar(db_session, condo.id, unit.id, user.id,
                   Decimal("300.00"), status="pending")
        _create_ar(db_session, condo.id, unit.id, user.id,
                   Decimal("200.00"), status="paid", paid_amount=Decimal("200.00"))
        _create_ar(db_session, condo.id, unit.id, user.id,
                   Decimal("100.00"), status="cancelled")
        db_session.commit()

        pending = _get_payment_pending(user.id, condo.id)
        assert pending == 300.0, (
            f"Only pending AR should count. Expected 300.00, got {pending}"
        )

        _cleanup_by_condo(db_session, condo.id)
