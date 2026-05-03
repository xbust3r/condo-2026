"""
Integration tests: Balance Summary — Condominium, Building, Unit levels.

Verifies rubro separation: maintenance, amenity_bookings, security_deposits.
Each test creates a minimal sandbox, runs BalanceSummaryUseCase, then cleans up.

Notes:
- BalanceSummaryUseCase uses session_scope() (separate session, auto-commit)
- Cross-session verification via use case responses
- Booking stats verified through raw SQL when needed
"""
import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal
import uuid as _uuid

from tests.factories.condo_factory import CondoFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.unit_factory import UnitFactory
from tests.factories.user_factory import UserFactory
from tests.factories.resident_factory import ResidentFactory
from tests.factories.charge_type_factory import ChargeTypeFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.ar_factory import AccountsReceivableFactory


# ─────────────────────────────────────────────────────────────────────────────
# Cleanup
# ─────────────────────────────────────────────────────────────────────────────

_CASCADE_TABLES = [
    "core_amenity_bookings",
    "core_amenities", "core_announcements", "core_documents",
    "core_incidents", "core_meetings", "core_notifications",
    "core_packages", "core_visitors",
    "core_payments", "core_receipts",
    "core_ledger_entries",
    "core_accounts_receivable",
    "core_charges", "core_charge_types",
    "core_resident_profiles",
    "core_votes", "core_vote_options",
    "core_units",
    "core_buildings",
    "core_condominiums",
]


def _cleanup_by_condo(db_session, condo_id: int):
    """Delete ALL test data for a condominium and commit."""
    from sqlalchemy import text
    for table in _CASCADE_TABLES:
        try:
            db_session.execute(
                text(f"DELETE FROM {table} WHERE condominium_id = :cid"),
                {"cid": condo_id},
            )
        except Exception:
            pass
    try:
        db_session.execute(
            text(
                "DELETE FROM users WHERE id IN ("
                " SELECT user_id FROM core_resident_profiles WHERE condominium_id = :cid"
                ") AND id NOT IN ("
                " SELECT user_id FROM core_resident_profiles WHERE condominium_id != :cid"
                ")"
            ),
            {"cid": condo_id},
        )
    except Exception:
        pass
    db_session.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Sandbox builders
# ─────────────────────────────────────────────────────────────────────────────

def _make_balance_sandbox(db_session):
    """
    Create a minimal sandbox for balance testing:
    - 1 condo, 2 buildings, 4 units (2 per building)
    - 2 charge types (maintenance, extraordinary)
    - 2 users + residents
    - NO ARs/charges initially (tests add what they need)
    """
    tag = _uuid.uuid4().hex[:8]

    condo = CondoFactory.create(db_session, name=f"BalTest-{tag}")
    building_a = BuildingFactory.create(
        db_session, condominium_id=condo.id,
        code=f"BLD-A-{tag}", name="Torre A",
        floors_count=5, units_planned=2,
    )
    building_b = BuildingFactory.create(
        db_session, condominium_id=condo.id,
        code=f"BLD-B-{tag}", name="Torre B",
        floors_count=5, units_planned=2,
    )

    units = []
    for bldg in [building_a, building_b]:
        for u_num in [1, 2]:
            unit = UnitFactory.create(
                db_session,
                building_id=bldg.id,
                unit_number=f"{u_num:03d}",
                code=f"UNIT-{bldg.code}-{u_num:02d}",
                name=f"Unidad {u_num}",
                floor_number=u_num,
                occupancy_status="occupied",
            )
            units.append(unit)

    users = []
    for i in range(4):
        user = UserFactory.create(
            db_session,
            email=f"baltest-{tag}-{i}@test.local",
        )
        ResidentFactory.create(
            db_session,
            user_id=user.id,
            condominium_id=condo.id,
        )
        users.append(user)

    ct_maintenance = ChargeTypeFactory.create(
        db_session,
        code=f"MAINT-{tag}",
        name="Cuota de mantenimiento",
        is_global=1,
    )
    ct_extra = ChargeTypeFactory.create(
        db_session,
        code=f"EXTRA-{tag}",
        name="Cargo extraordinario",
        is_global=1,
    )

    db_session.commit()

    return {
        "tag": tag,
        "condo": condo,
        "buildings": [building_a, building_b],
        "building_a": building_a,
        "building_b": building_b,
        "units": units,
        "users": users,
        "charge_types": [ct_maintenance, ct_extra],
        "ct_maintenance": ct_maintenance,
        "ct_extra": ct_extra,
    }


def _insert_ar(session, condo_id, unit_id, user_id, amount, paid=0,
               origin_type=None, origin_id=None, status="pending",
               charge_id=None):
    """Insert a raw AR via SQLAlchemy model for balance testing."""
    from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
    ar = DBAR(
        uuid=str(_uuid.uuid4()),
        condominium_id=condo_id,
        unit_id=unit_id,
        debtor_user_id=user_id,
        amount=amount,
        paid_amount=paid,
        due_date=date.today() + timedelta(days=30),
        status=status,
        charge_id=charge_id,
        origin_type=origin_type,
        origin_id=origin_id,
        currency="PEN",
        description="Test AR for balance",
        reference_code=f"ARB-{_uuid.uuid4().hex[:8]}",
    )
    session.add(ar)
    session.flush()
    session.refresh(ar)
    return ar


def _insert_booking(session, condo_id, building_id, amenity_id, unit_id,
                     owner_id, status="confirmed", booking_fee=Decimal("0"),
                     deposit_amount=Decimal("0"), deposit_status="not_required",
                     booking_date=None):
    """Insert a raw amenity booking for balance stats testing."""
    from sqlalchemy import text
    if booking_date is None:
        booking_date = date.today()
    session.execute(
        text("""
            INSERT INTO core_amenity_bookings
                (uuid, condominium_id, building_id, amenity_id, unit_id,
                 owner_id, booking_date, start_at, end_at, status,
                 booking_fee_amount, security_deposit_amount, currency,
                 deposit_status, unit_number_snapshot, owner_name_snapshot)
            VALUES
                (:uuid, :condo_id, :building_id, :amenity_id, :unit_id,
                 :owner_id, :booking_date, :start_at, :end_at, :status,
                 :fee, :deposit, 'PEN',
                 :deposit_status, 'UNIT-101', 'Test Owner')
        """),
        {
            "uuid": str(_uuid.uuid4()),
            "condo_id": condo_id,
            "building_id": building_id,
            "amenity_id": amenity_id,
            "unit_id": unit_id,
            "owner_id": owner_id,
            "booking_date": booking_date,
            "start_at": datetime.utcnow() + timedelta(hours=1),
            "end_at": datetime.utcnow() + timedelta(hours=3),
            "status": status,
            "fee": booking_fee,
            "deposit": deposit_amount,
            "deposit_status": deposit_status,
        },
    )
    session.flush()


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Condominium Balance
# ─────────────────────────────────────────────────────────────────────────────

class TestCondominiumBalance:
    """Balance consolidado del condominio con rubros separados."""

    def test_empty_condominium_returns_zeros(self, db_session):
        """Condominium with no ARs → all zeros."""
        sandbox = _make_balance_sandbox(db_session)

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        assert result["condominium_id"] == sandbox["condo"].id
        assert result["total"]["expected"] == 0.0
        assert result["total"]["collected"] == 0.0
        assert result["total"]["pending"] == 0.0
        assert result["total"]["collection_rate_pct"] == 0.0

        for rubro in ["maintenance", "amenity_bookings", "security_deposits"]:
            assert result["rubros"][rubro]["expected"] == 0.0
            assert result["rubros"][rubro]["collected"] == 0.0

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_maintenance_ar_appears_in_maintenance_rubro(self, db_session):
        """ARs with origin_type=NULL go to maintenance rubro."""
        sandbox = _make_balance_sandbox(db_session)

        _insert_ar(
            db_session, sandbox["condo"].id,
            sandbox["units"][0].id, sandbox["users"][0].id,
            Decimal("200.00"), origin_type=None,
        )
        _insert_ar(
            db_session, sandbox["condo"].id,
            sandbox["units"][1].id, sandbox["users"][1].id,
            Decimal("300.00"), paid=Decimal("300.00"), origin_type=None,
        )
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        m = result["rubros"]["maintenance"]
        assert m["expected"] == 500.00
        assert m["collected"] == 300.00
        assert m["pending"] == 200.00
        assert m["ar_count"] == 2

        # Other rubros should be zero
        assert result["rubros"]["amenity_bookings"]["expected"] == 0.0
        assert result["rubros"]["security_deposits"]["expected"] == 0.0

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_booking_fee_ar_appears_in_amenity_bookings_rubro(self, db_session):
        """ARs with origin_type=amenity_booking_fee go to amenity_bookings."""
        sandbox = _make_balance_sandbox(db_session)

        _insert_ar(
            db_session, sandbox["condo"].id,
            sandbox["units"][0].id, sandbox["users"][0].id,
            Decimal("150.00"), origin_type="amenity_booking_fee",
        )
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        ab = result["rubros"]["amenity_bookings"]
        assert ab["expected"] == 150.00
        assert ab["collected"] == 0.0
        assert ab["pending"] == 150.00
        assert ab["ar_count"] == 1

        assert result["rubros"]["maintenance"]["expected"] == 0.0
        assert result["rubros"]["security_deposits"]["expected"] == 0.0

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_security_deposit_ar_appears_in_security_deposits_rubro(self, db_session):
        """ARs with origin_type=amenity_security_deposit go to the right rubro."""
        sandbox = _make_balance_sandbox(db_session)

        _insert_ar(
            db_session, sandbox["condo"].id,
            sandbox["units"][0].id, sandbox["users"][0].id,
            Decimal("500.00"), paid=Decimal("500.00"),
            origin_type="amenity_security_deposit",
        )
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        sd = result["rubros"]["security_deposits"]
        assert sd["expected"] == 500.00
        assert sd["collected"] == 500.00
        assert sd["pending"] == 0.0
        assert sd["ar_count"] == 1

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_mixed_rubros_total_correct(self, db_session):
        """All three rubros present → total sums correctly."""
        sandbox = _make_balance_sandbox(db_session)

        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("200.00"))  # maintenance
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][1].id, sandbox["users"][1].id,
                   Decimal("100.00"), origin_type="amenity_booking_fee")
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][2].id, sandbox["users"][2].id,
                   Decimal("300.00"), origin_type="amenity_security_deposit")
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        t = result["total"]
        assert t["expected"] == 600.00  # 200 + 100 + 300
        assert t["collected"] == 0.0
        assert t["pending"] == 600.00
        assert t["collection_rate_pct"] == 0.0

        # Verify rubros individually
        assert result["rubros"]["maintenance"]["expected"] == 200.00
        assert result["rubros"]["amenity_bookings"]["expected"] == 100.00
        assert result["rubros"]["security_deposits"]["expected"] == 300.00

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_cancelled_ar_excluded(self, db_session):
        """ARs with status=cancelled are excluded from balance."""
        sandbox = _make_balance_sandbox(db_session)

        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("200.00"), status="pending")  # counts
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][1].id, sandbox["users"][1].id,
                   Decimal("999.00"), status="cancelled")  # excluded
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        assert result["total"]["expected"] == 200.00
        assert result["rubros"]["maintenance"]["ar_count"] == 1

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_collection_rate_calculation(self, db_session):
        """Collection rate = (collected / expected) * 100."""
        sandbox = _make_balance_sandbox(db_session)

        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("100.00"), paid=Decimal("60.00"))
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][1].id, sandbox["users"][1].id,
                   Decimal("100.00"), paid=Decimal("100.00"))
        # expected=200, collected=160 → rate = 80%
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        assert result["total"]["expected"] == 200.00
        assert result["total"]["collected"] == 160.00
        assert result["total"]["pending"] == 40.00
        assert result["total"]["collection_rate_pct"] == 80.0

        _cleanup_by_condo(db_session, sandbox["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Building Balance
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildingBalance:
    """Balance de edificio con rubros separados."""

    def test_building_balance_filters_by_building(self, db_session):
        """ARs from building A don't appear in building B balance."""
        sandbox = _make_balance_sandbox(db_session)

        # ARs for building A units
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("200.00"))  # BLD-A, unit 1
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][1].id, sandbox["users"][1].id,
                   Decimal("150.00"))  # BLD-A, unit 2
        # AR for building B unit
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][2].id, sandbox["users"][2].id,
                   Decimal("500.00"))  # BLD-B, unit 1
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()

        result_a = uc.get_building_balance(sandbox["building_a"].id)
        assert result_a["total"]["expected"] == 350.00  # 200 + 150

        result_b = uc.get_building_balance(sandbox["building_b"].id)
        assert result_b["total"]["expected"] == 500.00

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_building_not_found(self, db_session):
        """Non-existent building returns error."""
        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_building_balance(99999)
        assert "error" in result

    def test_building_balance_includes_bookings(self, db_session):
        """Booking fees with origin_type filter appear in building balance."""
        sandbox = _make_balance_sandbox(db_session)

        # Maintenance AR
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("200.00"))
        # Booking fee AR for same building
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("80.00"), origin_type="amenity_booking_fee")
        # Security deposit for same building
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("200.00"), origin_type="amenity_security_deposit")
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_building_balance(sandbox["building_a"].id)

        assert result["rubros"]["maintenance"]["expected"] == 200.00
        assert result["rubros"]["amenity_bookings"]["expected"] == 80.00
        assert result["rubros"]["security_deposits"]["expected"] == 200.00
        assert result["total"]["expected"] == 480.00

        _cleanup_by_condo(db_session, sandbox["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Unit Balance
# ─────────────────────────────────────────────────────────────────────────────

class TestUnitBalance:
    """Balance de unidad con rubros separados."""

    def test_unit_balance_with_maintenance(self, db_session):
        """Unit balance shows only that unit's ARs."""
        sandbox = _make_balance_sandbox(db_session)

        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("250.00"), paid=Decimal("250.00"))
        # Another unit's AR (should not appear)
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][1].id, sandbox["users"][1].id,
                   Decimal("999.00"))
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_unit_balance(sandbox["units"][0].id)

        assert result["unit_id"] == sandbox["units"][0].id
        assert result["unit_number"] is not None
        assert result["building_id"] == sandbox["building_a"].id
        assert result["building_name"] == "Torre A"
        assert result["condominium_id"] == sandbox["condo"].id

        assert result["rubros"]["maintenance"]["expected"] == 250.00
        assert result["rubros"]["maintenance"]["collected"] == 250.00
        assert result["rubros"]["maintenance"]["pending"] == 0.0
        assert result["rubros"]["maintenance"]["ar_count"] == 1

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_unit_not_found(self, db_session):
        """Non-existent unit returns error."""
        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_unit_balance(99999)
        assert "error" in result

    def test_unit_balance_all_rubros(self, db_session):
        """Unit with ARs across all three rubros."""
        sandbox = _make_balance_sandbox(db_session)

        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][2].id, sandbox["users"][2].id,
                   Decimal("300.00"))  # maintenance
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][2].id, sandbox["users"][2].id,
                   Decimal("120.00"), origin_type="amenity_booking_fee")
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][2].id, sandbox["users"][2].id,
                   Decimal("500.00"), origin_type="amenity_security_deposit")
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_unit_balance(sandbox["units"][2].id)

        assert result["rubros"]["maintenance"]["expected"] == 300.00
        assert result["rubros"]["amenity_bookings"]["expected"] == 120.00
        assert result["rubros"]["security_deposits"]["expected"] == 500.00
        assert result["total"]["expected"] == 920.00

        _cleanup_by_condo(db_session, sandbox["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Booking Stats in Balance
# ─────────────────────────────────────────────────────────────────────────────

class TestBookingStats:
    """Booking statistics embedded in balance responses."""

    def test_booking_stats_with_bookings(self, db_session):
        """Balance includes booking counts and deposit custody when bookings exist."""
        sandbox = _make_balance_sandbox(db_session)

        # Need an amenity for the booking FK
        from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity
        amenity = DBAmenity(
            uuid=str(_uuid.uuid4()),
            condominium_id=sandbox["condo"].id,
            name="Salón de Eventos",
            scope="CONDOMINIUM",
            location="Piso 1",
            max_capacity=50,
            booking_duration_min=120,
            requires_approval=False,
            status="active",
            booking_price=Decimal("100.00"),
            security_deposit_amount=Decimal("200.00"),
        )
        db_session.add(amenity)
        db_session.flush()
        db_session.refresh(amenity)

        # Insert bookings with known states
        # confirmed booking with deposit pending
        _insert_booking(
            db_session, sandbox["condo"].id, sandbox["building_a"].id,
            amenity.id, sandbox["units"][0].id, sandbox["users"][0].id,
            status="confirmed", booking_fee=Decimal("100.00"),
            deposit_amount=Decimal("200.00"), deposit_status="pending",
        )
        # completed booking
        _insert_booking(
            db_session, sandbox["condo"].id, sandbox["building_a"].id,
            amenity.id, sandbox["units"][1].id, sandbox["users"][1].id,
            status="completed", booking_fee=Decimal("80.00"),
            deposit_amount=Decimal("0"), deposit_status="not_required",
        )
        # Another confirmed with deposit paid
        _insert_booking(
            db_session, sandbox["condo"].id, sandbox["building_b"].id,
            amenity.id, sandbox["units"][2].id, sandbox["users"][2].id,
            status="confirmed", booking_fee=Decimal("120.00"),
            deposit_amount=Decimal("300.00"), deposit_status="paid",
        )
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        ab = result["rubros"]["amenity_bookings"]
        assert ab["booking_count"] == 3
        assert ab["confirmed"] == 2
        assert ab["completed"] == 1

        sd = result["rubros"]["security_deposits"]
        # deposits_in_custody = pending(200) + paid(300) = 500
        assert sd["in_custody"] == 500.00

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_booking_stats_empty(self, db_session):
        """Balance with no bookings → zero booking stats."""
        sandbox = _make_balance_sandbox(db_session)

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        ab = result["rubros"]["amenity_bookings"]
        assert ab["booking_count"] == 0
        assert ab["confirmed"] == 0
        assert ab["completed"] == 0

        sd = result["rubros"]["security_deposits"]
        assert sd["in_custody"] == 0.0

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_building_booking_stats_scoped(self, db_session):
        """Booking stats at building level only count that building's bookings."""
        sandbox = _make_balance_sandbox(db_session)

        from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity
        amenity = DBAmenity(
            uuid=str(_uuid.uuid4()),
            condominium_id=sandbox["condo"].id,
            name="Gimnasio",
            scope="CONDOMINIUM",
            location="Piso 1",
            max_capacity=20,
            booking_duration_min=60,
            requires_approval=False,
            status="active",
            booking_price=Decimal("50.00"),
            security_deposit_amount=Decimal("0"),
        )
        db_session.add(amenity)
        db_session.flush()

        # 2 bookings in building A
        _insert_booking(
            db_session, sandbox["condo"].id, sandbox["building_a"].id,
            amenity.id, sandbox["units"][0].id, sandbox["users"][0].id,
            status="confirmed",
        )
        _insert_booking(
            db_session, sandbox["condo"].id, sandbox["building_a"].id,
            amenity.id, sandbox["units"][1].id, sandbox["users"][1].id,
            status="completed",
        )
        # 1 booking in building B
        _insert_booking(
            db_session, sandbox["condo"].id, sandbox["building_b"].id,
            amenity.id, sandbox["units"][2].id, sandbox["users"][2].id,
            status="confirmed",
        )
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()

        result_a = uc.get_building_balance(sandbox["building_a"].id)
        assert result_a["rubros"]["amenity_bookings"]["booking_count"] == 2

        result_b = uc.get_building_balance(sandbox["building_b"].id)
        assert result_b["rubros"]["amenity_bookings"]["booking_count"] == 1

        _cleanup_by_condo(db_session, sandbox["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Response Structure
# ─────────────────────────────────────────────────────────────────────────────

class TestBalanceResponseStructure:
    """Ensure all response fields are present and correctly typed."""

    def test_condominium_response_structure(self, db_session):
        """Verify all expected keys exist in condominium balance response."""
        sandbox = _make_balance_sandbox(db_session)
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("100.00"))
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_condominium_balance(sandbox["condo"].id)

        # Top-level keys
        for key in ["condominium_id", "period", "as_of", "total", "rubros"]:
            assert key in result, f"Missing key: {key}"

        # Total keys
        for key in ["expected", "collected", "pending", "collection_rate_pct"]:
            assert key in result["total"], f"Missing total key: {key}"

        # Rubros
        for rubro in ["maintenance", "amenity_bookings", "security_deposits"]:
            assert rubro in result["rubros"], f"Missing rubro: {rubro}"
            r = result["rubros"][rubro]
            for key in ["label", "expected", "collected", "pending", "ar_count"]:
                assert key in r, f"Missing rubro key {rubro}.{key}"

        # Amenity bookings extra fields
        ab = result["rubros"]["amenity_bookings"]
        for key in ["booking_count", "confirmed", "completed"]:
            assert key in ab, f"Missing amenity_bookings.{key}"

        # Security deposits extra field
        assert "in_custody" in result["rubros"]["security_deposits"]

        _cleanup_by_condo(db_session, sandbox["condo"].id)

    def test_unit_response_has_context(self, db_session):
        """Unit balance response includes building/condo context."""
        sandbox = _make_balance_sandbox(db_session)
        _insert_ar(db_session, sandbox["condo"].id,
                   sandbox["units"][0].id, sandbox["users"][0].id,
                   Decimal("100.00"))
        db_session.commit()

        from library.dddpy.core_balance_summary.usecase.balance_summary_usecase import (
            BalanceSummaryUseCase,
        )
        uc = BalanceSummaryUseCase()
        result = uc.get_unit_balance(sandbox["units"][0].id)

        for key in ["unit_id", "unit_number", "building_id", "building_name",
                     "condominium_id", "period", "as_of", "total", "rubros"]:
            assert key in result, f"Missing unit balance key: {key}"

        _cleanup_by_condo(db_session, sandbox["condo"].id)
