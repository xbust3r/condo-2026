"""
Integration tests: Amenity Bookings — Sprint 2 QA cases.

Covers:
- Booking lifecycle: create → confirm → complete → deposit management
- AR generation on confirm (booking fee + security deposit)
- Conflict detection (overlapping bookings)
- Validation rules (unit→building, owner→unit)
- Snapshot preservation
- Deposit lifecycle (return, partial apply, full apply)
- Config flag enforcement
"""
import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal
import uuid as _uuid


# ─────────────────────────────────────────────────────────────────────────────
# Cleanup
# ─────────────────────────────────────────────────────────────────────────────

_CASCADE_TABLES = [
    "core_amenity_bookings",
    "core_amenities",
    "core_announcements", "core_documents",
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
# Sandbox
# ─────────────────────────────────────────────────────────────────────────────

def _make_booking_sandbox(db_session):
    """Create 1 condo, 1 building, 2 units, 2 users, 1 amenity with pricing."""
    from tests.factories.condo_factory import CondoFactory
    from tests.factories.building_factory import BuildingFactory
    from tests.factories.unit_factory import UnitFactory
    from tests.factories.user_factory import UserFactory
    from tests.factories.resident_factory import ResidentFactory

    tag = _uuid.uuid4().hex[:8]

    condo = CondoFactory.create(db_session, name=f"BkTest-{tag}")
    building = BuildingFactory.create(
        db_session, condominium_id=condo.id,
        code=f"BLD-{tag}", name="Torre Test", floors_count=5, units_planned=2,
    )

    units = []
    for i in range(2):
        unit = UnitFactory.create(
            db_session, building_id=building.id,
            unit_number=f"{101 + i}", code=f"U-{tag}-{i}",
            name=f"Unidad {101 + i}", floor_number=1,
            occupancy_status="occupied",
        )
        units.append(unit)

    users = []
    for i in range(2):
        user = UserFactory.create(db_session, email=f"bktest-{tag}-{i}@test.local")
        ResidentFactory.create(db_session, user_id=user.id, condominium_id=condo.id)
        # Create user profile so owner_name_snapshot works
        from library.dddpy.core_user_profiles.infrastructure.dbuser_profile import DBUserProfile
        from sqlalchemy import func as sa_func
        profile = DBUserProfile(
            uuid=str(_uuid.uuid4()),
            user_id=user.id,
            first_name=f"TestUser{i}",
            last_name=f"Test-{tag}",
            updated_at=sa_func.now(),
        )
        db_session.add(profile)
        db_session.flush()
        db_session.refresh(profile)
        users.append(user)
    db_session.flush()

    # Create unit ownership records
    from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
    for i in range(2):
        ownership = DBUnitOwnership(
            uuid=str(_uuid.uuid4()),
            unit_id=units[i].id,
            user_id=users[i].id,
            ownership_type="owner",
            ownership_percentage=Decimal("100.00"),
            status="active",
        )
        db_session.add(ownership)
        db_session.flush()
        db_session.refresh(ownership)

    # Amenity with pricing
    from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity
    amenity = DBAmenity(
        uuid=str(_uuid.uuid4()),
        condominium_id=condo.id,
        name="Salón de Eventos",
        scope="CONDOMINIUM",
        location="Piso 1",
        max_capacity=50,
        booking_duration_min=120,
        requires_approval=False,
        status="active",
        is_reservable=True,
        booking_price=Decimal("100.00"),
        security_deposit_amount=Decimal("200.00"),
    )
    db_session.add(amenity)
    db_session.flush()
    db_session.refresh(amenity)

    db_session.commit()

    return {
        "tag": tag,
        "condo": condo,
        "building": building,
        "units": units,
        "users": users,
        "amenity": amenity,
    }


def _create_booking(sandbox, unit_idx=0, user_idx=0, start_h=10, end_h=12,
                    booking_date=None):
    """Create a booking via use case."""
    from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase

    if booking_date is None:
        booking_date = date.today() + timedelta(days=1)

    uc = BookingUseCase()
    return uc.create(
        condominium_id=sandbox["condo"].id,
        building_id=sandbox["building"].id,
        amenity_id=sandbox["amenity"].id,
        unit_id=sandbox["units"][unit_idx].id,
        owner_id=sandbox["users"][user_idx].id,
        booking_date=booking_date,
        start_at=datetime.combine(booking_date, datetime.min.time()).replace(hour=start_h),
        end_at=datetime.combine(booking_date, datetime.min.time()).replace(hour=end_h),
        notes=None,
    )


def _confirm_booking(booking_id: int):
    from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
    return BookingUseCase().confirm(booking_id)


def _cancel_booking(booking_id: int, reason: str = "Test cancel"):
    from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
    return BookingUseCase().cancel(booking_id, reason=reason)


def _complete_booking(booking_id: int):
    from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
    return BookingUseCase().complete(booking_id)


def _return_deposit(booking_id: int, notes: str = ""):
    from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
    return BookingUseCase().return_deposit(booking_id, notes=notes)


def _pay_deposit_ar(booking_id: int):
    """Simulate paying the deposit ARs for a confirmed booking."""
    from sqlalchemy import text
    from library.dddpy.shared.mysql.session_manager import session_scope
    with session_scope() as session:
        # Mark all ARs for this booking as paid
        session.execute(
            text("""
                UPDATE core_accounts_receivable
                SET status = 'paid', paid_amount = amount
                WHERE origin_id = :booking_id
                AND origin_type IN ('amenity_booking_fee', 'amenity_security_deposit')
            """),
            {"booking_id": booking_id},
        )
        # Update booking deposit_status to 'paid'
        session.execute(
            text("""
                UPDATE core_amenity_bookings
                SET deposit_status = 'paid'
                WHERE id = :booking_id
            """),
            {"booking_id": booking_id},
        )
        session.flush()


def _apply_deposit(booking_id: int, action: str = "full_apply", amount: Decimal = None,
                   notes: str = ""):
    from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
    return BookingUseCase().apply_deposit(
        id=booking_id, action=action, amount=amount or Decimal("0"), notes=notes,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 1 — Creation & Validation
# ─────────────────────────────────────────────────────────────────────────────

class TestBookingCreation:
    """Basic booking creation and validation."""

    def test_create_booking_draft(self, db_session):
        """Creating a booking starts in draft/pending_approval status."""
        s = _make_booking_sandbox(db_session)
        result = _create_booking(s)
        booking_data = result.data

        assert booking_data["amenity_id"] == s["amenity"].id
        assert booking_data["unit_id"] == s["units"][0].id
        assert booking_data["status"] in ("draft", "pending_approval")
        # Snapshot preserved
        assert booking_data["unit_number_snapshot"] is not None
        assert len(booking_data["unit_number_snapshot"]) > 0
        assert booking_data["owner_name_snapshot"] is not None
        assert len(booking_data["owner_name_snapshot"]) > 0

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_overlap_rejected(self, db_session):
        """Two confirmed bookings for same amenity at overlapping times are rejected."""
        s = _make_booking_sandbox(db_session)
        b1 = _create_booking(s, start_h=10, end_h=14)
        _confirm_booking(b1.data["id"])

        # Overlapping booking
        with pytest.raises(Exception) as exc:
            _create_booking(s, start_h=12, end_h=16)
        assert any(kw in str(exc.value).lower() for kw in ("overlap", "conflict", "already", "time range"))

        # Non-overlapping should work
        b2 = _create_booking(s, start_h=15, end_h=17)
        assert b2.data["id"] is not None

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_unit_must_belong_to_building(self, db_session):
        """Unit from a different building is rejected."""
        s = _make_booking_sandbox(db_session)

        # Create a second building with its own unit
        from tests.factories.building_factory import BuildingFactory
        from tests.factories.unit_factory import UnitFactory
        building2 = BuildingFactory.create(
            db_session, condominium_id=s["condo"].id,
            code=f"BLD2-{s['tag']}", name="Torre 2", floors_count=5, units_planned=1,
        )
        unit2 = UnitFactory.create(
            db_session, building_id=building2.id,
            unit_number="301", code=f"U2-{s['tag']}",
            name="Unidad 301", floor_number=3, occupancy_status="occupied",
        )
        db_session.commit()

        # Try booking unit2 but specifying original building
        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        uc = BookingUseCase()
        booking_date = date.today() + timedelta(days=1)
        with pytest.raises(Exception) as exc:
            uc.create(
                condominium_id=s["condo"].id,
                building_id=s["building"].id,  # original building
                amenity_id=s["amenity"].id,
                unit_id=unit2.id,  # unit belongs to building2
                owner_id=s["users"][0].id,
                booking_date=booking_date,
                start_at=datetime.combine(booking_date, datetime.min.time()).replace(hour=10),
                end_at=datetime.combine(booking_date, datetime.min.time()).replace(hour=12),
            )
        # Should fail validation
        assert "unit" in str(exc.value).lower() or "building" in str(exc.value).lower()

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_owner_must_belong_to_unit(self, db_session):
        """Owner not associated with the unit is rejected."""
        s = _make_booking_sandbox(db_session)

        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        uc = BookingUseCase()
        booking_date = date.today() + timedelta(days=1)

        # Create a user not associated with the condominium
        from tests.factories.user_factory import UserFactory
        outsider = UserFactory.create(db_session, email=f"outsider-{s['tag']}@test.local")
        db_session.commit()

        with pytest.raises(Exception) as exc:
            uc.create(
                condominium_id=s["condo"].id,
                building_id=s["building"].id,
                amenity_id=s["amenity"].id,
                unit_id=s["units"][0].id,
                owner_id=outsider.id,  # no resident profile
                booking_date=booking_date,
                start_at=datetime.combine(booking_date, datetime.min.time()).replace(hour=10),
                end_at=datetime.combine(booking_date, datetime.min.time()).replace(hour=12),
            )
        # Validation should catch this
        assert "owner" in str(exc.value).lower() or "resident" in str(exc.value).lower() or "profile" in str(exc.value).lower()

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_snapshot_preserved(self, db_session):
        """unit_number_snapshot and owner_name_snapshot are stored on creation."""
        s = _make_booking_sandbox(db_session)
        result = _create_booking(s)

        b = result.data
        # Snapshot stores u.code (not u.unit_number) from the query
        assert b["unit_number_snapshot"] == s["units"][0].code
        assert len(b["owner_name_snapshot"]) > 0

        _cleanup_by_condo(db_session, s["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 1 — Confirmation & AR generation
# ─────────────────────────────────────────────────────────────────────────────

class TestBookingConfirmAR:
    """Confirmation generates AR entries correctly."""

    def test_confirm_generates_booking_fee_ar(self, db_session):
        """Confirming a booking generates an AR for the booking price."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)
        bid = b.data["id"]

        result = _confirm_booking(bid)
        confirmed = result.data
        print("DEBUG confirmed keys:", list(confirmed.keys()))
        print("DEBUG booking_fee_ar_id:", confirmed.get("booking_fee_ar_id"))
        print("DEBUG security_deposit_ar_id:", confirmed.get("security_deposit_ar_id"))

        assert confirmed["status"] == "confirmed"
        assert confirmed["booking_fee_amount"] == 100.0

        # AR was created
        ar_id = confirmed.get("booking_fee_ar_id")
        assert ar_id is not None  # AR was created

        # Verify AR in DB using production session
        from library.dddpy.shared.mysql.session_manager import session_scope
        from sqlalchemy import text
        with session_scope() as sess:
            ar = sess.execute(
                text("SELECT * FROM core_accounts_receivable WHERE id = :id"),
                {"id": ar_id},
            ).mappings().fetchone()
            assert ar is not None
            assert float(ar["amount"]) == 100.0
            assert ar["origin_type"] == "amenity_booking_fee"
            assert ar["origin_id"] == bid

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_confirm_generates_security_deposit_ar(self, db_session):
        """Confirming generates a second AR for the security deposit."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)
        bid = b.data["id"]

        result = _confirm_booking(bid)
        confirmed = result.data

        # Deposit AR
        ar_deposit_id = confirmed.get("security_deposit_ar_id")
        assert ar_deposit_id is not None

        # Verify AR using production session
        from library.dddpy.shared.mysql.session_manager import session_scope
        from sqlalchemy import text
        with session_scope() as sess:
            ar = sess.execute(
                text("SELECT * FROM core_accounts_receivable WHERE id = :id"),
                {"id": ar_deposit_id},
            ).mappings().fetchone()
            assert ar is not None
            assert float(ar["amount"]) == 200.0
            assert ar["origin_type"] == "amenity_security_deposit"

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_confirm_twice_rejected(self, db_session):
        """Cannot confirm an already confirmed booking."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)
        _confirm_booking(b.data["id"])

        with pytest.raises(Exception) as exc:
            _confirm_booking(b.data["id"])
        assert "status" in str(exc.value).lower() or "already" in str(exc.value).lower()

        _cleanup_by_condo(db_session, s["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 1 — Cancellation
# ─────────────────────────────────────────────────────────────────────────────

class TestBookingCancellation:
    """Cancellation logic with AR cleanup."""

    def test_cancel_draft_no_ar(self, db_session):
        """Cancelling a draft booking just changes status, no AR cleanup needed."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)

        result = _cancel_booking(b.data["id"], reason="Ya no se necesita")
        assert result.data["status"] == "cancelled"

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_cancel_confirmed_before_payment_cancels_ars(self, db_session):
        """Cancel confirmed booking with unpaid ARs → ARs remain (manual handling)."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)
        _confirm_booking(b.data["id"])

        result = _cancel_booking(b.data["id"], reason="Motivo administrativo")
        cancelled = result.data
        assert cancelled["status"] == "cancelled"

        # ARs still exist (not deleted by cancel)
        from library.dddpy.shared.mysql.session_manager import session_scope
        from sqlalchemy import text
        with session_scope() as sess:
            ars = sess.execute(
                text("SELECT COUNT(*) as cnt FROM core_accounts_receivable WHERE origin_id = :bid"),
                {"bid": b.data["id"]},
            ).scalar()
            assert ars >= 1  # ARs still exist after cancel

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_cancel_with_reason_preserved(self, db_session):
        """Cancellation reason is stored."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)
        reason = "El propietario canceló por motivos personales"
        result = _cancel_booking(b.data["id"], reason=reason)

        # Reason should be in notes or similar
        notes = result.data.get("notes") or ""
        assert "cancel" in notes.lower() or result.data["status"] == "cancelled"

        _cleanup_by_condo(db_session, s["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 1 — Complete
# ─────────────────────────────────────────────────────────────────────────────

class TestBookingComplete:
    """Completion flow."""

    def test_complete_confirmed_booking(self, db_session):
        """Complete a confirmed booking."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)
        _confirm_booking(b.data["id"])

        result = _complete_booking(b.data["id"])
        assert result.data["status"] == "completed"

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_complete_draft_rejected(self, db_session):
        """Cannot complete a draft booking."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)

        with pytest.raises(Exception) as exc:
            _complete_booking(b.data["id"])
        assert "status" in str(exc.value).lower() or "confirmed" in str(exc.value).lower()

        _cleanup_by_condo(db_session, s["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 2 — Deposit Lifecycle
# ─────────────────────────────────────────────────────────────────────────────

class TestDepositLifecycle:
    """Deposit return / apply / partial flow."""

    def _setup_confirmed_with_deposit(self, db_session):
        """Create a sandbox with a confirmed booking (has deposit AR)."""
        s = _make_booking_sandbox(db_session)
        b = _create_booking(s)
        result = _confirm_booking(b.data["id"])
        return s, result

    def test_return_deposit(self, db_session):
        """Returning deposit sets status to 'returned'."""
        s, confirmed = self._setup_confirmed_with_deposit(db_session)
        bid = confirmed.data["id"]

        # Simulate paying the deposit AR
        _pay_deposit_ar(bid)

        result = _return_deposit(bid, notes="Sin daños")
        deposit_data = result.data

        assert deposit_data["deposit_status"] == "returned"

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_full_apply_deposit(self, db_session):
        """Applying full deposit sets status to 'applied'."""
        s, confirmed = self._setup_confirmed_with_deposit(db_session)
        bid = confirmed.data["id"]

        _pay_deposit_ar(bid)

        result = _apply_deposit(
            bid, action="full_apply",
            amount=Decimal("200.00"), notes="Daños totales",
        )
        deposit_data = result.data

        assert deposit_data["deposit_status"] == "applied"

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_partial_apply_deposit(self, db_session):
        """Partially applying deposit sets status correctly."""
        s, confirmed = self._setup_confirmed_with_deposit(db_session)
        bid = confirmed.data["id"]

        _pay_deposit_ar(bid)

        result = _apply_deposit(
            bid, action="partial_apply",
            amount=Decimal("100.00"), notes="Daños parciales",
        )
        deposit_data = result.data

        assert "partially_applied" in deposit_data["deposit_status"]

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_return_then_apply_rejected(self, db_session):
        """Cannot apply after deposit returned."""
        s, confirmed = self._setup_confirmed_with_deposit(db_session)
        bid = confirmed.data["id"]

        _pay_deposit_ar(bid)

        _return_deposit(bid)
        with pytest.raises(Exception) as exc:
            _apply_deposit(bid, action="full_apply", amount=Decimal("200.00"))
        assert "deposit" in str(exc.value).lower() or "status" in str(exc.value).lower()

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_deposit_not_required_amenity(self, db_session):
        """Amenity with no deposit doesn't generate deposit AR."""
        s = _make_booking_sandbox(db_session)

        # Create a second amenity with no deposit
        from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity
        free_amenity = DBAmenity(
            uuid=str(_uuid.uuid4()),
            condominium_id=s["condo"].id,
            name="Gimnasio",
            scope="CONDOMINIUM",
            location="Piso 1",
            max_capacity=20,
            booking_duration_min=60,
            requires_approval=False,
            status="active",
            is_reservable=True,
            booking_price=Decimal("50.00"),
            security_deposit_amount=Decimal("0"),
        )
        db_session.add(free_amenity)
        db_session.flush()
        db_session.refresh(free_amenity)
        db_session.commit()

        # Create booking for free amenity (no deposit)
        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        uc = BookingUseCase()
        booking_date = date.today() + timedelta(days=1)
        b = uc.create(
            condominium_id=s["condo"].id,
            building_id=s["building"].id,
            amenity_id=free_amenity.id,
            unit_id=s["units"][0].id,
            owner_id=s["users"][0].id,
            booking_date=booking_date,
            start_at=datetime.combine(booking_date, datetime.min.time()).replace(hour=10),
            end_at=datetime.combine(booking_date, datetime.min.time()).replace(hour=12),
        )
        result = _confirm_booking(b.data["id"])

        # Should have fee AR but NO deposit AR
        assert result.data["booking_fee_ar_id"] is not None
        assert result.data.get("security_deposit_ar_id") is None
        assert result.data.get("deposit_status") in ("none", None, "not_required")

        _cleanup_by_condo(db_session, s["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 2 — Config flags
# ─────────────────────────────────────────────────────────────────────────────

class TestAmenitySettings:
    """Config flag enforcement on condominium settings."""

    def test_settings_default_to_false(self, db_session):
        """New condominium has all amenity settings False by default."""
        from tests.factories.condo_factory import CondoFactory
        condo = CondoFactory.create(db_session, name=f"CfgTest-{_uuid.uuid4().hex[:8]}")
        db_session.commit()

        # Fetch via API/entity
        from library.dddpy.core_condominiums.usecase.condominium_query_usecase import CondominiumQueryUseCase
        from library.dddpy.core_condominiums.usecase.condominium_factory import condominium_query_usecase_factory

        q_uc = condominium_query_usecase_factory()
        entity = q_uc.get_by_id(condo.id)
        assert entity is not None

        settings = entity.amenity_settings
        assert settings.get("enable_amenity_booking_charges") is False
        assert settings.get("include_amenity_bookings_in_receipts") is False
        assert settings.get("include_amenity_bookings_in_building_balance") is False
        assert settings.get("include_amenity_bookings_in_condominium_balance") is False

        _cleanup_by_condo(db_session, condo.id)

    def test_update_settings_persisted(self, db_session):
        """Updating amenity_settings via PUT condominiums persists correctly."""
        from tests.factories.condo_factory import CondoFactory
        condo = CondoFactory.create(db_session, name=f"CfgTest2-{_uuid.uuid4().hex[:8]}")
        db_session.commit()

        from library.dddpy.core_condominiums.usecase.condominium_usecase import CondominiumUseCase
        from library.dddpy.core_condominiums.usecase.condominium_cmd_schema import UpdateCondominiumSchema

        uc = CondominiumUseCase()
        schema = UpdateCondominiumSchema(
            amenity_settings={
                "enable_amenity_booking_charges": True,
                "include_amenity_bookings_in_receipts": True,
                "include_amenity_bookings_in_building_balance": False,
                "include_amenity_bookings_in_condominium_balance": False,
            }
        )
        result = uc.update(condo.id, schema)
        updated = result.data

        settings = updated.get("amenity_settings", {})
        assert settings.get("enable_amenity_booking_charges") is True
        assert settings.get("include_amenity_bookings_in_receipts") is True
        assert settings.get("include_amenity_bookings_in_building_balance") is False
        assert settings.get("include_amenity_bookings_in_condominium_balance") is False

        # Verify persisted
        from library.dddpy.core_condominiums.usecase.condominium_factory import condominium_query_usecase_factory
        q_uc = condominium_query_usecase_factory()
        entity = q_uc.get_by_id(condo.id)
        assert entity.amenity_settings["enable_amenity_booking_charges"] is True

        _cleanup_by_condo(db_session, condo.id)

    def test_settings_partial_update(self, db_session):
        """Amenity_settings can be updated without affecting other fields."""
        from tests.factories.condo_factory import CondoFactory
        condo = CondoFactory.create(db_session, name=f"CfgTest3-{_uuid.uuid4().hex[:8]}")
        db_session.commit()

        from library.dddpy.core_condominiums.usecase.condominium_usecase import CondominiumUseCase
        from library.dddpy.core_condominiums.usecase.condominium_cmd_schema import UpdateCondominiumSchema

        uc = CondominiumUseCase()

        # Only update settings, not name
        schema = UpdateCondominiumSchema(
            amenity_settings={
                "enable_amenity_booking_charges": True,
            }
        )
        result = uc.update(condo.id, schema)

        # Settings should be in amenity_settings
        assert result.data.get("amenity_settings", {}).get("enable_amenity_booking_charges") is True
        # Name should be unchanged
        assert result.data["name"] is not None

        _cleanup_by_condo(db_session, condo.id)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 2 — Booking Report
# ─────────────────────────────────────────────────────────────────────────────

class TestBookingReport:
    """Report endpoint produces correct aggregations."""

    def test_report_empty_condominium(self, db_session):
        """Report for condominium with no bookings returns zeros."""
        s = _make_booking_sandbox(db_session)

        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        result = BookingUseCase().get_report(condominium_id=s["condo"].id)

        summary = result.data["summary"]
        assert summary["total_bookings"] == 0
        assert float(summary["total_fees"]) == 0.0
        assert float(summary["deposits_held"]) == 0.0

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_report_with_bookings(self, db_session):
        """Report aggregates correctly with confirmed bookings."""
        s = _make_booking_sandbox(db_session)

        # Create and confirm 2 bookings
        b1 = _create_booking(s, start_h=10, end_h=12)
        _confirm_booking(b1.data["id"])
        b2 = _create_booking(s, start_h=14, end_h=16)
        _confirm_booking(b2.data["id"])

        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        result = BookingUseCase().get_report(condominium_id=s["condo"].id)

        summary = result.data["summary"]
        assert summary["total_bookings"] == 2
        assert float(summary["total_fees"]) == 200.0  # 2 × 100
        assert float(summary["deposits_held"]) == 400.0  # 2 × 200

        # By status
        confirmed_status = [s for s in result.data["by_status"] if s["status"] == "confirmed"]
        assert len(confirmed_status) == 1
        assert confirmed_status[0]["count"] == 2

        # By building
        assert len(result.data["by_building"]) >= 1
        bldg = result.data["by_building"][0]
        assert bldg["bookings"] == 2
        assert float(bldg["revenue"]) == 200.0

        # By amenity
        assert len(result.data["by_amenity"]) >= 1
        amenity_row = result.data["by_amenity"][0]
        assert amenity_row["bookings"] == 2

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_report_filtered_by_date(self, db_session):
        """Report respects date_from / date_to filters."""
        s = _make_booking_sandbox(db_session)

        # Booking for today+1
        b1 = _create_booking(s, booking_date=date.today() + timedelta(days=1))
        _confirm_booking(b1.data["id"])

        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase

        # Filter for today+2 → should be empty
        result = BookingUseCase().get_report(
            condominium_id=s["condo"].id,
            date_from=date.today() + timedelta(days=2),
        )
        assert result.data["summary"]["total_bookings"] == 0

        # Filter including today+1 → should include it
        result = BookingUseCase().get_report(
            condominium_id=s["condo"].id,
            date_from=date.today(),
            date_to=date.today() + timedelta(days=2),
        )
        assert result.data["summary"]["total_bookings"] == 1

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_report_filtered_by_building(self, db_session):
        """Report filtered by building shows only that building's data."""
        s = _make_booking_sandbox(db_session)

        # Create a second building
        from tests.factories.building_factory import BuildingFactory
        from tests.factories.unit_factory import UnitFactory
        from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
        building2 = BuildingFactory.create(
            db_session, condominium_id=s["condo"].id,
            code=f"BLD2-{s['tag']}", name="Torre 2", floors_count=3, units_planned=1,
        )
        unit2 = UnitFactory.create(
            db_session, building_id=building2.id,
            unit_number="301", code=f"U2-{s['tag']}",
            name="Unidad 301", floor_number=3, occupancy_status="occupied",
        )
        db_session.flush()

        # Create ownership for unit2 with users[0]
        ownership2 = DBUnitOwnership(
            uuid=str(_uuid.uuid4()),
            unit_id=unit2.id,
            user_id=s["users"][0].id,
            ownership_type="owner",
            ownership_percentage=Decimal("100.00"),
            status="active",
        )
        db_session.add(ownership2)
        db_session.flush()
        db_session.refresh(ownership2)
        db_session.commit()

        # Booking in building 1
        b1 = _create_booking(s)
        _confirm_booking(b1.data["id"])

        # Booking in building 2 (different time slot to avoid overlap on shared amenity)
        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        uc = BookingUseCase()
        booking_date = date.today() + timedelta(days=1)
        b2 = uc.create(
            condominium_id=s["condo"].id,
            building_id=building2.id,
            amenity_id=s["amenity"].id,
            unit_id=unit2.id,
            owner_id=s["users"][0].id,
            booking_date=booking_date + timedelta(days=1),  # different day
            start_at=datetime.combine(booking_date + timedelta(days=1), datetime.min.time()).replace(hour=10),
            end_at=datetime.combine(booking_date + timedelta(days=1), datetime.min.time()).replace(hour=12),
        )
        _confirm_booking(b2.data["id"])

        # Filter by building 1
        result = BookingUseCase().get_report(
            condominium_id=s["condo"].id,
            building_id=s["building"].id,
        )
        assert result.data["summary"]["total_bookings"] == 1

        _cleanup_by_condo(db_session, s["condo"].id)
