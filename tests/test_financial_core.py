"""
Integration tests: Financial Core — Charges, Payments, Receipts, AR, Ledger.

Each test creates a minimal sandbox (committed), exercises real use cases,
then cascade-deletes by condominium_id.

Notes:
- Use cases use session_scope() (separate session, auto-commit)
- The test fixture session may not see cross-session commits (REPEATABLE READ)
- We validate via use case responses + follow-up use case queries
- Cross-DB-verification uses raw SQL/expire_all where needed
"""
import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal
import uuid as _uuid


# ─────────────────────────────────────────────────────────────────────────────
# Sandbox helpers
# ─────────────────────────────────────────────────────────────────────────────

_CASCADE_TABLES = [
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


def _make_minimal_sandbox(db_session):
    """Create minimal financial sandbox — unique IDs per invocation."""
    from tests.factories.condo_factory import CondoFactory
    from tests.factories.building_factory import BuildingFactory
    from tests.factories.unit_factory import UnitFactory
    from tests.factories.user_factory import UserFactory
    from tests.factories.resident_factory import ResidentFactory
    from tests.factories.charge_type_factory import ChargeTypeFactory

    tag = _uuid.uuid4().hex[:8]

    condo = CondoFactory.create(db_session, name=f"FinTest-{tag}")
    building = BuildingFactory.create(
        db_session, condominium_id=condo.id,
        code=f"BLD-{tag}", name=f"Tower {tag}",
    )
    units = []
    for i in range(2):
        units.append(UnitFactory.create(
            db_session, building_id=building.id,
            unit_number=f"{tag[-4:]}-{i+1:03d}",
            code=f"UNIT-{tag}-{i+1:02d}",
            name=f"Unit {tag} #{i+1}",
            floor_number=i + 1,
            occupancy_status="occupied",
        ))
    users = []
    residents = []
    for i in range(2):
        user = UserFactory.create(db_session, email=f"fin-{tag}-{i+1}@test.local")
        resident = ResidentFactory.create(db_session, user_id=user.id, condominium_id=condo.id)
        users.append(user)
        residents.append(resident)

    charge_types = []
    for prefix, desc in [("MANT", "Cuota"), ("AGUA", "Agua")]:
        ct = ChargeTypeFactory.create(
            db_session,
            code=f"{prefix}-{tag}",
            name=f"{desc} ({tag})",
            is_global=1,
        )
        charge_types.append(ct)

    db_session.commit()
    return {
        "condo": condo, "buildings": [building],
        "units": units, "users": users,
        "residents": residents, "charge_types": charge_types,
    }


def _teardown(db_session, sandbox):
    _cleanup_by_condo(db_session, sandbox["condo"].id)


# ─────────────────────────────────────────────────────────────────────────────
# Charges
# ─────────────────────────────────────────────────────────────────────────────


class TestChargeIntegration:

    def test_create_unit_charge(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase

        result = ChargeUseCase().create(CreateChargeSchema(
            condominium_id=sandbox["condo"].id,
            charge_type_id=sandbox["charge_types"][0].id,
            scope="unit",
            unit_id=sandbox["units"][0].id,
            amount=250.00,
            description="Mantenimiento — Unidad 1",
            is_recurrent=True,
            period_pattern=date.today().strftime("%Y-%m"),
            start_date=date.today(),
            distribution_mode="fixed_unit_amount",
        ))

        assert result.success is True
        charge = result.data["charge"]
        assert charge["scope"] == "unit"
        assert float(charge["amount"]) == 250.00
        assert charge["unit_id"] == sandbox["units"][0].id
        assert "id" in charge and charge["id"] > 0

        # Cross-verify via use case get_by_id
        fetched = ChargeUseCase().get_by_id(charge["id"])
        assert fetched.success is True
        assert fetched.data["scope"] == "unit"

        _teardown(db_session, sandbox)

    def test_create_building_charge(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase

        result = ChargeUseCase().create(CreateChargeSchema(
            condominium_id=sandbox["condo"].id,
            charge_type_id=sandbox["charge_types"][0].id,
            scope="building",
            building_id=sandbox["buildings"][0].id,
            amount=500.00,
            description="Agua — Torre",
            distribution_mode="prorated_by_building_coefficient",
            start_date=date.today(),
        ))

        charge = result.data["charge"]
        assert charge["scope"] == "building"
        assert charge["building_id"] == sandbox["buildings"][0].id
        assert float(charge["amount"]) == 500.00

        _teardown(db_session, sandbox)

    def test_create_condominium_charge(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase

        result = ChargeUseCase().create(CreateChargeSchema(
            condominium_id=sandbox["condo"].id,
            charge_type_id=sandbox["charge_types"][0].id,
            scope="condominium",
            amount=1000.00,
            description="Seguridad — todo el condominio",
            distribution_mode="prorated_by_condominium_coefficient",
            start_date=date.today(),
        ))

        charge = result.data["charge"]
        assert charge["scope"] == "condominium"
        assert charge["unit_id"] is None
        assert charge["building_id"] is None

        _teardown(db_session, sandbox)

    def test_create_charge_missing_required_fk(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase

        with pytest.raises(Exception):
            ChargeUseCase().create(CreateChargeSchema(
                condominium_id=sandbox["condo"].id,
                charge_type_id=sandbox["charge_types"][0].id,
                scope="unit",
                amount=100.00,
                start_date=date.today(),
            ))

        _teardown(db_session, sandbox)

    def test_update_charge_amount(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import (
            CreateChargeSchema, UpdateChargeSchema,
        )
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase

        uc = ChargeUseCase()
        created = uc.create(CreateChargeSchema(
            condominium_id=sandbox["condo"].id,
            charge_type_id=sandbox["charge_types"][0].id,
            scope="unit", unit_id=sandbox["units"][0].id,
            amount=100.00, start_date=date.today(),
        ))
        charge_id = created.data["charge"]["id"]

        updated = uc.update(charge_id, UpdateChargeSchema(amount=350.00))
        assert updated.data["amount"] == 350.00

        # Cross-verify the update persisted
        fetched = uc.get_by_id(charge_id)
        assert fetched.data["amount"] == 350.00

        _teardown(db_session, sandbox)

    def test_soft_delete_and_restore_charge(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase

        uc = ChargeUseCase()
        created = uc.create(CreateChargeSchema(
            condominium_id=sandbox["condo"].id,
            charge_type_id=sandbox["charge_types"][0].id,
            scope="unit", unit_id=sandbox["units"][0].id,
            amount=150.00, start_date=date.today(),
        ))
        charge_id = created.data["charge"]["id"]

        # Soft-delete and verify it appears in include_deleted list
        assert uc.soft_delete(charge_id).success is True

        listed = uc.list_all(
            condominium_id=sandbox["condo"].id, include_deleted=True,
        )
        deleted = [c for c in listed.data["items"] if c["id"] == charge_id]
        assert len(deleted) == 1

        # Restore and verify it's back
        assert uc.restore(charge_id).success is True
        fetched = uc.get_by_id(charge_id)
        assert fetched.success is True

        _teardown(db_session, sandbox)

    def test_list_charges_by_condominium(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase

        uc = ChargeUseCase()
        for i in range(3):
            uc.create(CreateChargeSchema(
                condominium_id=sandbox["condo"].id,
                charge_type_id=sandbox["charge_types"][0].id,
                scope="unit",
                unit_id=sandbox["units"][i % 2].id,
                amount=100.00 * (i + 1),
                description=f"Charge #{i+1}",
                start_date=date.today(),
            ))

        listed = uc.list_all(condominium_id=sandbox["condo"].id)
        assert listed.data["total"] >= 3

        _teardown(db_session, sandbox)


# ─────────────────────────────────────────────────────────────────────────────
# Accounts Receivable
# ─────────────────────────────────────────────────────────────────────────────


class TestAccountsReceivableIntegration:

    def test_create_ar_entry(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import CreateARSchema
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase

        result = ARUseCase().create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            amount=200.00,
            due_date=date.today() + timedelta(days=30),
            description="Cuota — Unidad 1",
            period=date.today().strftime("%Y-%m"),
        ))

        ar = result.data
        assert float(ar["amount"]) == 200.00
        assert ar["status"] == "pending"
        assert ar["id"] > 0

        # Cross-verify via use case get_by_id
        fetched = ARUseCase().get_by_id(ar["id"])
        assert fetched.data["amount"] == 200.00
        assert fetched.data["status"] == "pending"

        _teardown(db_session, sandbox)

    def test_create_ar_with_charge_link(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase
        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import CreateARSchema
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase

        charge = ChargeUseCase().create(CreateChargeSchema(
            condominium_id=sandbox["condo"].id,
            charge_type_id=sandbox["charge_types"][0].id,
            scope="unit", unit_id=sandbox["units"][0].id,
            amount=300.00, start_date=date.today(),
        ))

        ar = ARUseCase().create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            charge_id=charge.data["charge"]["id"],
            amount=300.00,
            due_date=date.today() + timedelta(days=30),
        ))

        assert ar.data["charge_id"] == charge.data["charge"]["id"]

        _teardown(db_session, sandbox)

    def test_record_payment_on_ar(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import (
            CreateARSchema, RecordPaymentSchema,
        )
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase

        uc = ARUseCase()
        created = uc.create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            amount=400.00,
            due_date=date.today() + timedelta(days=30),
        ))
        ar_id = created.data["id"]

        # Partial payment
        result = uc.record_payment(ar_id, RecordPaymentSchema(
            amount=150.00, payment_method="yape",
            reference="YAPE-123", paid_by_user_id=sandbox["users"][0].id,
        ))
        assert result.data["ar"]["status"] == "partial"
        assert float(result.data["payment_registered"]) == 150.00

        # Full payment
        result2 = uc.record_payment(ar_id, RecordPaymentSchema(
            amount=250.00, payment_method="bank_transfer",
            paid_by_user_id=sandbox["users"][0].id,
        ))
        assert result2.data["ar"]["status"] == "paid"
        assert float(result2.data["payment_registered"]) == 250.00

        # Cross-verify via get_by_id
        fetched = uc.get_by_id(ar_id)
        assert fetched.data["status"] == "paid"
        assert float(fetched.data["paid_amount"]) == 400.00

        _teardown(db_session, sandbox)

    def test_list_ar_by_unit(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import CreateARSchema
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase

        uc = ARUseCase()
        for i in range(2):
            uc.create(CreateARSchema(
                condominium_id=sandbox["condo"].id,
                unit_id=sandbox["units"][0].id,
                debtor_user_id=sandbox["users"][0].id,
                amount=100.00 * (i + 1),
                due_date=date.today() + timedelta(days=(i + 1) * 30),
                period=f"2026-0{i+1}",
            ))

        listed = uc.list_all(unit_id=sandbox["units"][0].id)
        assert listed.data["total"] >= 2

        _teardown(db_session, sandbox)


# ─────────────────────────────────────────────────────────────────────────────
# Payments
# ─────────────────────────────────────────────────────────────────────────────


class TestPaymentIntegration:

    def test_create_payment(self, db_session):
        """PaymentUseCase.create creates receipt + payment + updates AR."""
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import CreateARSchema
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
        from library.dddpy.core_payments.usecase.payment_cmd_schema import CreatePaymentSchema
        from library.dddpy.core_payments.usecase.payment_usecase import PaymentUseCase

        ar = ARUseCase().create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            amount=200.00,
            due_date=date.today() + timedelta(days=30),
        ))

        payment = PaymentUseCase().create(CreatePaymentSchema(
            ar_id=ar.data["id"],
            payer_user_id=sandbox["users"][0].id,
            amount=200.00,
            payment_method="bank_transfer",
            reference="TRF-001",
        ))

        # Returns PaymentEntity
        assert float(payment.amount) == 200.00
        assert payment.payment_method == "bank_transfer"
        assert payment.id > 0

        _teardown(db_session, sandbox)

    def test_payment_auto_updates_ar(self, db_session):
        """PaymentUseCase.create_with_ar_update should auto-update AR status."""
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import CreateARSchema
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
        from library.dddpy.core_payments.usecase.payment_cmd_schema import CreatePaymentSchema
        from library.dddpy.core_payments.usecase.payment_usecase import PaymentUseCase

        ar = ARUseCase().create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            amount=500.00,
            due_date=date.today() + timedelta(days=30),
        ))

        # Use create_with_ar_update for full flow (payment + AR update)
        PaymentUseCase().create_with_ar_update(CreatePaymentSchema(
            ar_id=ar.data["id"],
            payer_user_id=sandbox["users"][0].id,
            amount=500.00,
            payment_method="yape",
        ))

        # Verify AR is now paid
        fetched = ARUseCase().get_by_id(ar.data["id"])
        assert fetched.data["status"] == "paid"
        assert float(fetched.data["paid_amount"]) == 500.00

        _teardown(db_session, sandbox)


# ─────────────────────────────────────────────────────────────────────────────
# Receipts
# ─────────────────────────────────────────────────────────────────────────────


class TestReceiptIntegration:

    def test_create_receipt_direct(self, db_session):
        """Create a receipt directly (without Payment orchestrator)."""
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import CreateARSchema
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
        from library.dddpy.core_receipts.usecase.receipt_cmd_schema import CreateReceiptSchema
        from library.dddpy.core_receipts.usecase.receipt_usecase import ReceiptUseCase

        ar = ARUseCase().create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            amount=300.00,
            due_date=date.today() + timedelta(days=30),
        ))

        receipt = ReceiptUseCase().create(CreateReceiptSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            ar_id=ar.data["id"],
            payer_user_id=sandbox["users"][0].id,
            amount_paid=300.00,
            payment_method="transfer",
            receipt_number="REC-2026-001",
            issued_at=datetime.utcnow(),
        ))

        assert receipt.receipt_number == "REC-2026-001"
        assert receipt.amount_paid == 300.00
        assert receipt.id > 0

        _teardown(db_session, sandbox)

    def test_get_receipt_by_id(self, db_session):
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import CreateARSchema
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
        from library.dddpy.core_receipts.usecase.receipt_cmd_schema import CreateReceiptSchema
        from library.dddpy.core_receipts.usecase.receipt_usecase import ReceiptUseCase

        ar = ARUseCase().create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            amount=150.00,
            due_date=date.today() + timedelta(days=30),
        ))

        receipt = ReceiptUseCase().create(CreateReceiptSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            ar_id=ar.data["id"],
            payer_user_id=sandbox["users"][0].id,
            amount_paid=150.00,
            payment_method="yape",
            receipt_number=f"REC-TEST-{_uuid.uuid4().hex[:6]}",
            issued_at=datetime.utcnow(),
        ))

        fetched = ReceiptUseCase().get_by_id(receipt.id)
        assert fetched.data["id"] == receipt.id
        assert fetched.data["amount_paid"] == 150.00

        _teardown(db_session, sandbox)


# ─────────────────────────────────────────────────────────────────────────────
# Ledger Entries
# ─────────────────────────────────────────────────────────────────────────────


class TestLedgerIntegration:

    def test_ledger_entries_on_charge_and_payment(self, db_session):
        """Verify ledger entries for charge + payment flow."""
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase
        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import (
            CreateARSchema, RecordPaymentSchema,
        )
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
        from library.dddpy.core_ledger_entries.usecase.ledger_usecase import LedgerUseCase
        from library.dddpy.core_ledger_entries.usecase.ledger_cmd_schema import CreateLedgerEntrySchema

        charge = ChargeUseCase().create(CreateChargeSchema(
            condominium_id=sandbox["condo"].id,
            charge_type_id=sandbox["charge_types"][0].id,
            scope="unit", unit_id=sandbox["units"][0].id,
            amount=300.00, start_date=date.today(),
        ))

        ar = ARUseCase().create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            charge_id=charge.data["charge"]["id"],
            amount=300.00,
            due_date=date.today() + timedelta(days=30),
        ))

        # Manually create ledger entries (system doesn't auto-generate them)
        charge_id = charge.data["charge"]["id"]
        ar_id = ar.data["id"]

        LedgerUseCase().create(CreateLedgerEntrySchema(
            unit_id=sandbox["units"][0].id,
            entry_type="charge",
            charge_id=charge_id,
            ar_id=ar_id,
            description="Cuota de mantenimiento",
            debit=300.00,
            period=date.today().strftime("%Y-%m"),
        ))

        ARUseCase().record_payment(ar_id, RecordPaymentSchema(
            amount=300.00, payment_method="bank_transfer",
            reference="TRF-LEDGER-001", paid_by_user_id=sandbox["users"][0].id,
        ))

        LedgerUseCase().create(CreateLedgerEntrySchema(
            unit_id=sandbox["units"][0].id,
            entry_type="payment",
            ar_id=ar_id,
            description="Pago de mantenimiento",
            credit=300.00,
            period=date.today().strftime("%Y-%m"),
        ))

        ledger = LedgerUseCase().list_by_unit(sandbox["units"][0].id)
        items = ledger.data.get("items", [])
        entry_types = [i.get("entry_type") for i in items]
        assert "charge" in entry_types, f"Expected charge, got {entry_types}"
        assert "payment" in entry_types, f"Expected payment, got {entry_types}"

        _teardown(db_session, sandbox)

    def test_ledger_list_by_condominium(self, db_session):
        """Ledger entries aggregated across units."""
        sandbox = _make_minimal_sandbox(db_session)

        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase
        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import (
            CreateARSchema, RecordPaymentSchema,
        )
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
        from library.dddpy.core_ledger_entries.usecase.ledger_usecase import LedgerUseCase
        from library.dddpy.core_ledger_entries.usecase.ledger_cmd_schema import CreateLedgerEntrySchema

        charge = ChargeUseCase().create(CreateChargeSchema(
            condominium_id=sandbox["condo"].id,
            charge_type_id=sandbox["charge_types"][0].id,
            scope="unit", unit_id=sandbox["units"][0].id,
            amount=100.00, start_date=date.today(),
        ))

        ar = ARUseCase().create(CreateARSchema(
            condominium_id=sandbox["condo"].id,
            unit_id=sandbox["units"][0].id,
            debtor_user_id=sandbox["users"][0].id,
            charge_id=charge.data["charge"]["id"],
            amount=100.00,
            due_date=date.today() + timedelta(days=30),
        ))

        ar_id = ar.data["id"]

        # Create charge ledger entry
        LedgerUseCase().create(CreateLedgerEntrySchema(
            unit_id=sandbox["units"][0].id,
            entry_type="charge",
            charge_id=charge.data["charge"]["id"],
            ar_id=ar_id,
            description="Cuota",
            debit=100.00,
            period=date.today().strftime("%Y-%m"),
        ))

        ARUseCase().record_payment(ar_id, RecordPaymentSchema(
            amount=100.00, payment_method="yape",
            paid_by_user_id=sandbox["users"][0].id,
        ))

        # Create payment ledger entry
        LedgerUseCase().create(CreateLedgerEntrySchema(
            unit_id=sandbox["units"][0].id,
            entry_type="payment",
            ar_id=ar_id,
            description="Pago",
            credit=100.00,
            period=date.today().strftime("%Y-%m"),
        ))

        total_entries = 0
        for unit in sandbox["units"]:
            ledger = LedgerUseCase().list_by_unit(unit.id)
            total_entries += ledger.data.get("total", 0)

        assert total_entries >= 2

        _teardown(db_session, sandbox)


# ─────────────────────────────────────────────────────────────────────────────
# End-to-end financial flow
# ─────────────────────────────────────────────────────────────────────────────


class TestFinancialFlowE2E:

    def test_full_financial_cycle(self, db_session):
        """Charge → AR → Payment (auto-receipt + AR update) → Ledger."""
        sandbox = _make_minimal_sandbox(db_session)

        cd = {
            "condo": sandbox["condo"].id,
            "unit": sandbox["units"][0].id,
            "user": sandbox["users"][0].id,
            "ct": sandbox["charge_types"][0].id,
        }

        # 1. Create charge
        from library.dddpy.core_charges.usecase.charge_cmd_schema import CreateChargeSchema
        from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase

        charge = ChargeUseCase().create(CreateChargeSchema(
            condominium_id=cd["condo"], charge_type_id=cd["ct"],
            scope="unit", unit_id=cd["unit"],
            amount=450.00, description="Cuota Abril 2026",
            is_recurrent=True, period_pattern="2026-04",
            start_date=date.today(),
        ))
        assert charge.success
        charge_id = charge.data["charge"]["id"]

        # 2. Generate AR
        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import CreateARSchema
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase

        ar = ARUseCase().create(CreateARSchema(
            condominium_id=cd["condo"], unit_id=cd["unit"],
            debtor_user_id=cd["user"], charge_id=charge_id,
            amount=450.00,
            due_date=date.today() + timedelta(days=15),
            period="2026-04",
        ))
        assert ar.success
        ar_id = ar.data["id"]
        assert ar.data["status"] == "pending"

        # 3. Payment (creates receipt internally, updates AR)
        from library.dddpy.core_payments.usecase.payment_cmd_schema import CreatePaymentSchema
        from library.dddpy.core_payments.usecase.payment_usecase import PaymentUseCase

        payment_response = PaymentUseCase().create_with_ar_update(CreatePaymentSchema(
            ar_id=ar_id, payer_user_id=cd["user"],
            amount=450.00, payment_method="bank_transfer",
            reference="TRF-E2E-001",
        ))
        assert payment_response.success
        pay_id = payment_response.data["payment"]["id"]

        # 4. AR should be paid (verify via use case)
        fetched_ar = ARUseCase().get_by_id(ar_id)
        assert fetched_ar.data["status"] == "paid"
        assert float(fetched_ar.data["paid_amount"]) == 450.00

        # 5. Manually create ledger entries
        from library.dddpy.core_ledger_entries.usecase.ledger_usecase import LedgerUseCase
        from library.dddpy.core_ledger_entries.usecase.ledger_cmd_schema import CreateLedgerEntrySchema

        LedgerUseCase().create(CreateLedgerEntrySchema(
            unit_id=cd["unit"],
            entry_type="charge",
            charge_id=charge_id,
            ar_id=ar_id,
            description="Cuota Abril 2026",
            debit=450.00,
            period="2026-04",
        ))
        LedgerUseCase().create(CreateLedgerEntrySchema(
            unit_id=cd["unit"],
            entry_type="payment",
            ar_id=ar_id,
            payment_id=pay_id,
            description="Pago cuota Abril 2026",
            credit=450.00,
            period="2026-04",
        ))

        # 6. Ledger entries exist
        ledger = LedgerUseCase().list_by_unit(cd["unit"])
        items = ledger.data.get("items", [])
        entry_types = [i.get("entry_type") for i in items]
        assert "charge" in entry_types
        assert "payment" in entry_types

        _teardown(db_session, sandbox)
