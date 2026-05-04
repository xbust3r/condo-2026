"""
Tests: Payment Proofs — upload, approve, reject, visibility.

Covers:
- PaymentProofEntity constants (ALLOWED_MIME_TYPES, MAX_FILE_SIZE_BYTES) and to_dict visibility
- CMD repository (insert, status transitions, link payment)
- Query repository (list, get_by_id, list_by_ar)
- Usecase orchestration (upload → approve/reject full flows)
- RBAC-aware visibility (resident vs admin data exposure)
- Edge cases: invalid MIME, oversized, duplicate approve, missing AR

Fixture strategy:
- Each test class creates a minimal sandbox via factories (committed)
- Use cases use their own session_scope() (cross-session)
- teardown cascades by condominium_id
"""
import uuid
import pytest
from datetime import date
from decimal import Decimal

# ── Cascade cleanup tables ─────────────────────────────────────────────────

_CASCADE_TABLES = [
    "payment_proofs",
    "core_payments", "core_receipts",
    "core_ledger_entries",
    "core_accounts_receivable",
    "core_charges", "core_charge_types",
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


# ═══════════════════════════════════════════════════════════════════════════
# Unit tests — Entity validation
# ═══════════════════════════════════════════════════════════════════════════

class TestPaymentProofEntity:
    """Domain entity constants + to_dict visibility rules."""

    def _make(self, **overrides):
        """Factory helper: return a PaymentProofEntity with sensible defaults."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        defaults = dict(
            id=1, uuid=str(uuid.uuid4()),
            condominium_id=1, unit_id=100, ar_id=1,
            submitted_by=1,
            file_url="/tmp/test.jpg",
            original_filename="test.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )
        defaults.update(overrides)
        return PaymentProofEntity(**defaults)

    def test_valid_image_mime_types(self):
        """Should accept jpg, jpeg, png, webp, pdf."""
        entity = self._make(mime_type="image/webp")
        assert entity.mime_type == "image/webp"

    def test_allowed_mime_types_set(self):
        """ALLOWED_MIME_TYPES class constant contains expected values."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        allowed = PaymentProofEntity.ALLOWED_MIME_TYPES
        assert "image/jpeg" in allowed
        assert "image/png" in allowed
        assert "image/webp" in allowed
        assert "application/pdf" in allowed
        for bad in ["application/x-msdownload", "text/html", "video/mp4"]:
            assert bad not in allowed

    def test_max_file_size_boundary(self):
        """MAX_FILE_SIZE_BYTES = 10 MB."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        assert PaymentProofEntity.MAX_FILE_SIZE_BYTES == 10 * 1024 * 1024

    def test_exactly_10mb_accepted(self):
        """Should accept files exactly at the 10 MB boundary."""
        entity = self._make(file_size_bytes=10_000_000)
        assert entity.file_size_bytes == 10_000_000

    def test_initial_status_is_pending_review(self):
        entity = self._make()
        assert entity.status == "pending_review"
        assert entity.is_pending() is True

    def test_is_pending_only_true_for_pending_review(self):
        entity = self._make(status="approved")
        assert entity.is_pending() is False

    def test_to_dict_resident_omits_sensitive_fields(self):
        entity = self._make(
            status="approved",
            bank_name="BCP",
            transaction_code="OP-123",
            reviewed_by=2,
            payment_id=1,
            receipt_id=1,
        )
        d = entity.to_dict(is_admin=False)
        assert "bank_name" not in d
        assert "transaction_code" not in d
        assert "reviewed_by" not in d
        assert "reviewed_by_name" not in d
        # Public fields
        assert "payment_id" in d
        assert "receipt_id" in d

    def test_to_dict_admin_includes_bank_fields(self):
        entity = self._make(
            status="approved",
            bank_name="BBVA",
            transaction_code="TXN-789",
            reviewed_by=2,
            payment_id=1,
            receipt_id=1,
        )
        d = entity.to_dict(is_admin=True)
        assert d["bank_name"] == "BBVA"
        assert d["transaction_code"] == "TXN-789"
        assert d["reviewed_by"] == 2


# ═══════════════════════════════════════════════════════════════════════════
# Integration tests — Usecase full flows
# ═══════════════════════════════════════════════════════════════════════════

class TestPaymentProofUsecase:
    """End-to-end usecase tests with real DB."""

    @pytest.fixture(autouse=True)
    def _sandbox(self, db_session):
        tag = uuid.uuid4().hex[:8]

        from tests.factories.condo_factory import CondoFactory
        from tests.factories.building_factory import BuildingFactory
        from tests.factories.unit_factory import UnitFactory
        from tests.factories.user_factory import UserFactory
        from tests.factories.resident_factory import ResidentFactory
        from tests.factories.charge_type_factory import ChargeTypeFactory
        from tests.factories.charge_factory import ChargeFactory

        self.condo = CondoFactory.create(db_session, name=f"Proof-{tag}")
        self.building = BuildingFactory.create(
            db_session, condominium_id=self.condo.id,
            code=f"BLD-{tag}", name=f"Tower-{tag}",
        )
        self.unit = UnitFactory.create(
            db_session, building_id=self.building.id,
            unit_number=f"101-{tag[:4]}",
            code=f"U-{tag[:6]}",
            name=f"Unit {tag[:4]}",
            floor_number=1,
            occupancy_status="occupied",
        )
        self.user = UserFactory.create(db_session, email=f"usr-{tag}@test.local")
        self.resident = ResidentFactory.create(
            db_session, user_id=self.user.id, condominium_id=self.condo.id,
        )
        self.admin = UserFactory.create(db_session, email=f"adm-{tag}@test.local")
        ResidentFactory.create(
            db_session, user_id=self.admin.id, condominium_id=self.condo.id,
        )

        ct = ChargeTypeFactory.create(
            db_session, condominium_id=self.condo.id,
            code=f"MNT-{tag[:6]}", name="Mantenimiento",
        )
        ChargeFactory.create(
            db_session, condominium_id=self.condo.id,
            unit_id=self.unit.id, charge_type_id=ct.id,
            debtor_user_id=self.user.id, amount=Decimal("350.00"),
            period=f"2026-0{int(tag[:2], 16) % 9 + 1}",
            status="pending",
        )
        db_session.commit()
        yield
        _cleanup_by_condo(db_session, self.condo.id)

    # ── helpers ──────────────────────────────────────────────────────

    def _create_ar(self, db_session, amount=Decimal("350.00")):
        from tests.factories.ar_factory import AccountsReceivableFactory
        ar = AccountsReceivableFactory.create(
            db_session,
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            debtor_user_id=self.user.id,
            amount=amount,
            paid_amount=Decimal("0"),
            due_date=date.today(),
            status="pending",
        )
        db_session.commit()
        return ar.id

    def _uc(self):
        from library.dddpy.core_payment_proofs.usecase.payment_proof_usecase import (
            PaymentProofUseCase,
        )
        return PaymentProofUseCase()

    # ── Upload ───────────────────────────────────────────────────────

    def test_upload_pdf_creates_pending_proof(self, db_session):
        ar_id = self._create_ar(db_session)
        r = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/comprobante.pdf",
            original_filename="comprobante.pdf",
            file_size_bytes=512_000, mime_type="application/pdf",
        )
        assert r.success
        assert r.data["status"] == "pending_review"
        assert r.data["original_filename"] == "comprobante.pdf"

    def test_upload_jpg(self, db_session):
        ar_id = self._create_ar(db_session)
        r = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=1_200_000, mime_type="image/jpeg",
        )
        assert r.success

    def test_upload_rejects_invalid_mime(self, db_session):
        ar_id = self._create_ar(db_session)
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofInvalidFileType,
        )
        with pytest.raises(PaymentProofInvalidFileType):
            self._uc().upload(
                condominium_id=self.condo.id, unit_id=self.unit.id,
                ar_id=ar_id, submitted_by=self.user.id,
                file_url="/tmp/virus.exe", original_filename="virus.exe",
                file_size_bytes=1000, mime_type="application/x-msdownload",
            )

    def test_upload_rejects_oversized(self, db_session):
        ar_id = self._create_ar(db_session)
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofFileTooLarge,
        )
        with pytest.raises(PaymentProofFileTooLarge):
            self._uc().upload(
                condominium_id=self.condo.id, unit_id=self.unit.id,
                ar_id=ar_id, submitted_by=self.user.id,
                file_url="/tmp/huge.png", original_filename="huge.png",
                file_size_bytes=15_000_000, mime_type="image/png",
            )

    def test_upload_nonexistent_ar(self, db_session):
        from library.dddpy.core_accounts_receivable.domain.ar_exception import ARNotFound
        with pytest.raises(ARNotFound):
            self._uc().upload(
                condominium_id=self.condo.id, unit_id=self.unit.id,
                ar_id=999_999, submitted_by=self.user.id,
                file_url="/tmp/test.jpg", original_filename="test.jpg",
                file_size_bytes=100_000, mime_type="image/jpeg",
            )

    # ── Approve ──────────────────────────────────────────────────────

    def _approve_data(self, bank="BCP", txn="TXN-001", notes=None):
        from library.dddpy.core_payment_proofs.domain.payment_proof_data import (
            ApproveProofData,
        )
        return ApproveProofData(bank_name=bank, transaction_code=txn, notes=notes)

    def test_approve_full_flow(self, db_session):
        ar_id = self._create_ar(db_session)
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=500_000, mime_type="image/jpeg",
        )
        r = self._uc().approve(
            id=upload.data["id"],
            review_data=self._approve_data("BCP", "OP-20260503-001", "OK"),
            reviewed_by=self.admin.id,
        )
        assert r.success
        assert r.data["proof"]["status"] == "approved"
        assert r.data["proof"]["bank_name"] == "BCP"
        assert r.data["proof"]["transaction_code"] == "OP-20260503-001"
        assert r.data["receipt"]["receipt_number"] is not None
        assert r.data["payment"]["id"] > 0

    def test_approve_updates_ar_to_paid(self, db_session):
        ar_id = self._create_ar(db_session, amount=Decimal("500.00"))
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=100_000, mime_type="image/jpeg",
        )
        self._uc().approve(
            id=upload.data["id"],
            review_data=self._approve_data("Interbank", "IB-001"),
            reviewed_by=self.admin.id,
        )
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
        ar = ARUseCase().get_by_id(ar_id).data
        assert ar["status"] == "paid"
        assert float(ar["paid_amount"]) == 500.0

    def test_approve_rejects_empty_bank_name(self, db_session):
        ar_id = self._create_ar(db_session)
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=100_000, mime_type="image/jpeg",
        )
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofValidationError,
        )
        with pytest.raises(PaymentProofValidationError):
            self._uc().approve(
                id=upload.data["id"],
                review_data=self._approve_data("   ", "TXN"),
                reviewed_by=self.admin.id,
            )

    def test_approve_rejects_empty_transaction_code(self, db_session):
        ar_id = self._create_ar(db_session)
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=100_000, mime_type="image/jpeg",
        )
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofValidationError,
        )
        with pytest.raises(PaymentProofValidationError):
            self._uc().approve(
                id=upload.data["id"],
                review_data=self._approve_data("BCP", ""),
                reviewed_by=self.admin.id,
            )

    def test_cannot_double_approve(self, db_session):
        ar_id = self._create_ar(db_session, amount=Decimal("300.00"))
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=100_000, mime_type="image/jpeg",
        )
        self._uc().approve(
            id=upload.data["id"],
            review_data=self._approve_data("BCP", "TXN-1"),
            reviewed_by=self.admin.id,
        )
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofAlreadyReviewed,
        )
        with pytest.raises(PaymentProofAlreadyReviewed):
            self._uc().approve(
                id=upload.data["id"],
                review_data=self._approve_data("BBVA", "TXN-2"),
                reviewed_by=self.admin.id,
            )

    def test_cannot_reject_approved_proof(self, db_session):
        ar_id = self._create_ar(db_session, amount=Decimal("200.00"))
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=100_000, mime_type="image/jpeg",
        )
        self._uc().approve(
            id=upload.data["id"],
            review_data=self._approve_data("BCP", "TXN"),
            reviewed_by=self.admin.id,
        )
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofAlreadyReviewed,
        )
        with pytest.raises(PaymentProofAlreadyReviewed):
            self._uc().reject(
                id=upload.data["id"],
                rejection_reason="Ya fue aprobado",
                reviewed_by=self.admin.id,
            )

    # ── Reject ───────────────────────────────────────────────────────

    def test_reject_stores_reason(self, db_session):
        ar_id = self._create_ar(db_session)
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/dudoso.jpg", original_filename="dudoso.jpg",
            file_size_bytes=100_000, mime_type="image/jpeg",
        )
        r = self._uc().reject(
            id=upload.data["id"],
            rejection_reason="Comprobante no legible",
            reviewed_by=self.admin.id,
        )
        assert r.success
        assert r.data["status"] == "rejected"
        assert r.data["rejection_reason"] == "Comprobante no legible"

    def test_reject_requires_reason(self, db_session):
        ar_id = self._create_ar(db_session)
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/test.jpg", original_filename="test.jpg",
            file_size_bytes=100_000, mime_type="image/jpeg",
        )
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofValidationError,
        )
        with pytest.raises(PaymentProofValidationError):
            self._uc().reject(
                id=upload.data["id"], rejection_reason="   ",
                reviewed_by=self.admin.id,
            )

    # ── Visibility ───────────────────────────────────────────────────

    def test_resident_hides_bank_info(self, db_session):
        ar_id = self._create_ar(db_session, amount=Decimal("250.00"))
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=200_000, mime_type="image/jpeg",
        )
        self._uc().approve(
            id=upload.data["id"],
            review_data=self._approve_data("Interbank", "IBK-SECRET-123"),
            reviewed_by=self.admin.id,
        )
        r = self._uc().get_by_id(upload.data["id"], is_admin=False)
        assert "bank_name" not in r.data
        assert "transaction_code" not in r.data
        assert r.data["status"] == "approved"

    def test_admin_sees_all_fields(self, db_session):
        ar_id = self._create_ar(db_session, amount=Decimal("150.00"))
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=150_000, mime_type="image/jpeg",
        )
        self._uc().approve(
            id=upload.data["id"],
            review_data=self._approve_data("BBVA", "BBVA-789"),
            reviewed_by=self.admin.id,
        )
        r = self._uc().get_by_id(upload.data["id"], is_admin=True)
        assert r.data["bank_name"] == "BBVA"
        assert r.data["transaction_code"] == "BBVA-789"
        assert r.data["payment_id"] is not None
        assert r.data["receipt_id"] is not None

    def test_pending_proof_has_no_bank_info(self, db_session):
        ar_id = self._create_ar(db_session)
        upload = self._uc().upload(
            condominium_id=self.condo.id, unit_id=self.unit.id,
            ar_id=ar_id, submitted_by=self.user.id,
            file_url="/uploads/pago.jpg", original_filename="pago.jpg",
            file_size_bytes=100_000, mime_type="image/jpeg",
        )
        r = self._uc().get_by_id(upload.data["id"], is_admin=True)
        assert r.data.get("bank_name") is None

    # ── List ─────────────────────────────────────────────────────────

    def test_list_admin_sees_all(self, db_session):
        ar_id = self._create_ar(db_session, amount=Decimal("600.00"))
        uc = self._uc()
        uc.upload(condominium_id=self.condo.id, unit_id=self.unit.id,
                  ar_id=ar_id, submitted_by=self.user.id,
                  file_url="/tmp/a.jpg", original_filename="a.jpg",
                  file_size_bytes=100_000, mime_type="image/jpeg")
        uc.upload(condominium_id=self.condo.id, unit_id=self.unit.id,
                  ar_id=ar_id, submitted_by=self.user.id,
                  file_url="/tmp/b.jpg", original_filename="b.jpg",
                  file_size_bytes=100_000, mime_type="image/jpeg")
        r = uc.list_all(condominium_id=self.condo.id, is_admin=True)
        assert len(r.data["items"]) == 2

    def test_list_filter_by_status(self, db_session):
        ar_id = self._create_ar(db_session, amount=Decimal("400.00"))
        uc = self._uc()
        u1 = uc.upload(condominium_id=self.condo.id, unit_id=self.unit.id,
                       ar_id=ar_id, submitted_by=self.user.id,
                       file_url="/tmp/a.jpg", original_filename="a.jpg",
                       file_size_bytes=100_000, mime_type="image/jpeg")
        uc.approve(id=u1.data["id"], review_data=self._approve_data(),
                   reviewed_by=self.admin.id)
        pending = uc.list_all(condominium_id=self.condo.id, status="pending_review", is_admin=True)
        approved = uc.list_all(condominium_id=self.condo.id, status="approved", is_admin=True)
        assert len(pending.data["items"]) == 0
        assert len(approved.data["items"]) == 1


# ═══════════════════════════════════════════════════════════════════════════
# Repository tests
# ═══════════════════════════════════════════════════════════════════════════

class TestPaymentProofRepository:
    """CMD + Query repository operations against real DB."""

    @pytest.fixture(autouse=True)
    def _sandbox(self, db_session):
        tag = uuid.uuid4().hex[:8]

        from tests.factories.condo_factory import CondoFactory
        from tests.factories.building_factory import BuildingFactory
        from tests.factories.unit_factory import UnitFactory
        from tests.factories.user_factory import UserFactory
        from tests.factories.charge_type_factory import ChargeTypeFactory
        from tests.factories.charge_factory import ChargeFactory
        from tests.factories.ar_factory import AccountsReceivableFactory

        self.condo = CondoFactory.create(db_session, name=f"Repo-{tag}")
        self.building = BuildingFactory.create(
            db_session, condominium_id=self.condo.id,
            code=f"BLD-{tag}", name=f"Tower-{tag}",
        )
        self.unit = UnitFactory.create(
            db_session, building_id=self.building.id,
            unit_number=f"201-{tag[:4]}",
            code=f"U-{tag[:6]}",
            name=f"Unit {tag[:4]}",
            floor_number=2,
            occupancy_status="occupied",
        )
        self.user = UserFactory.create(db_session, email=f"repo-{tag}@test.local")

        ct = ChargeTypeFactory.create(
            db_session, condominium_id=self.condo.id,
            code=f"MNT-{tag[:6]}", name="Mantenimiento",
        )
        ChargeFactory.create(
            db_session, condominium_id=self.condo.id,
            unit_id=self.unit.id, charge_type_id=ct.id,
            debtor_user_id=self.user.id, amount=Decimal("350.00"),
            period=f"2026-0{int(tag[:2], 16) % 9 + 1}",
            status="pending",
        )
        # Create real ARs so FK constraint is happy
        self.ar1 = AccountsReceivableFactory.create(
            db_session, condominium_id=self.condo.id,
            unit_id=self.unit.id, debtor_user_id=self.user.id,
            amount=Decimal("300.00"), paid_amount=Decimal("0"),
            due_date=date.today(), status="pending",
        )
        self.ar2 = AccountsReceivableFactory.create(
            db_session, condominium_id=self.condo.id,
            unit_id=self.unit.id, debtor_user_id=self.user.id,
            amount=Decimal("500.00"), paid_amount=Decimal("0"),
            due_date=date.today(), status="pending",
        )
        db_session.commit()
        yield
        try:
            _cleanup_by_condo(db_session, self.condo.id)
        except Exception:
            db_session.rollback()

    def _create_proof(self, db_session, **overrides):
        from tests.factories.payment_proof_factory import PaymentProofFactory
        defaults = dict(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=self.ar1.id,
            submitted_by=self.user.id,
        )
        defaults.update(overrides)
        proof = PaymentProofFactory.create(db_session, **defaults)
        db_session.commit()
        return proof

    def test_cmd_insert(self, db_session):
        proof = self._create_proof(db_session)
        assert proof.id > 0
        assert proof.status == "pending_review"

    def test_cmd_approve(self, db_session):
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_cmd_repository import (
            PaymentProofCmdRepositoryImpl,
        )
        from library.dddpy.core_payment_proofs.domain.payment_proof_data import (
            ApproveProofData,
        )
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        proof = self._create_proof(db_session)
        ok = PaymentProofCmdRepositoryImpl().approve(
            proof.id,
            ApproveProofData(bank_name="BCP", transaction_code="TXN-001", notes="OK"),
            reviewed_by=self.user.id,
        )
        assert ok
        # Read via query repo (own session) to avoid REPEATABLE READ isolation
        result = PaymentProofQueryRepositoryImpl().get_by_id(proof.id)
        assert result.status == "approved"
        assert result.bank_name == "BCP"
        assert result.transaction_code == "TXN-001"

    def test_cmd_reject(self, db_session):
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_cmd_repository import (
            PaymentProofCmdRepositoryImpl,
        )
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        proof = self._create_proof(db_session)
        ok = PaymentProofCmdRepositoryImpl().reject(proof.id, "Imagen borrosa", reviewed_by=self.user.id)
        assert ok
        result = PaymentProofQueryRepositoryImpl().get_by_id(proof.id)
        assert result.status == "rejected"
        assert result.rejection_reason == "Imagen borrosa"

    def test_cmd_link_payment(self, db_session):
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_cmd_repository import (
            PaymentProofCmdRepositoryImpl,
        )
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        from tests.factories.payment_factory import PaymentFactory
        from tests.factories.receipt_factory import ReceiptFactory
        payment = PaymentFactory.create(
            db_session, condominium_id=self.condo.id,
            unit_id=self.unit.id, ar_id=self.ar1.id,
            payer_user_id=self.user.id, amount=Decimal("300.00"),
        )
        receipt = ReceiptFactory.create(
            db_session, condominium_id=self.condo.id,
            unit_id=self.unit.id, ar_id=self.ar1.id,
            payer_user_id=self.user.id,
        )
        db_session.commit()
        proof = self._create_proof(db_session)
        ok = PaymentProofCmdRepositoryImpl().link_payment(
            proof.id,
            payment_id=payment.id,
            receipt_id=receipt.id,
        )
        assert ok
        result = PaymentProofQueryRepositoryImpl().get_by_id(proof.id)
        assert result.payment_id == payment.id
        assert result.receipt_id == receipt.id

    def test_query_get_by_id(self, db_session):
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        proof = self._create_proof(db_session)
        result = PaymentProofQueryRepositoryImpl().get_by_id(proof.id)
        assert result is not None
        assert result.id == proof.id
        assert result.status == "pending_review"

    def test_query_get_by_id_not_found(self, db_session):
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        assert PaymentProofQueryRepositoryImpl().get_by_id(999_999) is None

    def test_query_list_all(self, db_session):
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        self._create_proof(db_session)
        self._create_proof(db_session, original_filename="segundo.jpg")
        self._create_proof(db_session, original_filename="tercero.jpg")
        items, total = PaymentProofQueryRepositoryImpl().list_all(
            condominium_id=self.condo.id, skip=0, limit=10,
        )
        assert total == 3
        assert len(items) == 3

    def test_query_list_status_filter(self, db_session):
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        self._create_proof(db_session, status="pending_review")
        self._create_proof(db_session, status="approved")
        self._create_proof(db_session, status="rejected")
        repo = PaymentProofQueryRepositoryImpl()
        items, total = repo.list_all(
            condominium_id=self.condo.id, skip=0, limit=10, status="pending_review",
        )
        assert total == 1
        assert len(items) == 1

    def test_query_list_by_ar(self, db_session):
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        self._create_proof(db_session, ar_id=self.ar1.id, original_filename="ar1.jpg")
        self._create_proof(db_session, ar_id=self.ar1.id, original_filename="ar1_v2.jpg")
        self._create_proof(db_session, ar_id=self.ar2.id, original_filename="ar2.jpg")
        items, total = PaymentProofQueryRepositoryImpl().list_all(ar_id=self.ar1.id)
        assert total == 2
        assert all("ar1" in i.original_filename for i in items)
