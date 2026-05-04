"""
Tests: Payment Proofs — upload, approve, reject, visibility.

Covers:
- PaymentProofEntity validation (MIME types, file size)
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
import os
import pytest
import uuid as _uuid
from datetime import date, datetime
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
    """Domain entity: validation rules, status transitions, to_dict."""

    def test_valid_image_mime_types(self):
        """Should accept jpg, jpeg, png, webp."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        for mime in ["image/jpeg", "image/jpg", "image/png", "image/webp", "application/pdf"]:
            entity = PaymentProofEntity(
                condominium_id=1, unit_id=100, ar_id=1,
                submitted_by=1,
                file_url="/tmp/test.jpg",
                original_filename="test.jpg",
                file_size_bytes=100_000,
                mime_type=mime,
            )
            assert entity.mime_type == mime

    def test_reject_invalid_mime(self):
        """Should raise for non-image, non-pdf types."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import PaymentProofValidationError
        for mime in ["application/x-msdownload", "text/html", "video/mp4", "audio/mp3"]:
            with pytest.raises(PaymentProofValidationError) as exc:
                PaymentProofEntity(
                    condominium_id=1, unit_id=100, ar_id=1,
                    submitted_by=1,
                    file_url="/tmp/bad.ext",
                    original_filename="bad.ext",
                    file_size_bytes=100_000,
                    mime_type=mime,
                )
            assert "Tipo de archivo no permitido" in str(exc.value)

    def test_reject_oversized_file(self):
        """Should raise for files > 10 MB."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import PaymentProofValidationError
        with pytest.raises(PaymentProofValidationError) as exc:
            PaymentProofEntity(
                condominium_id=1, unit_id=100, ar_id=1,
                submitted_by=1,
                file_url="/tmp/big.jpg",
                original_filename="big.jpg",
                file_size_bytes=10_500_000,  # 10.5 MB
                mime_type="image/jpeg",
            )
        assert "excede el límite" in str(exc.value)

    def test_exactly_10mb_accepted(self):
        """Should accept files exactly at the 10 MB boundary."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        entity = PaymentProofEntity(
            condominium_id=1, unit_id=100, ar_id=1,
            submitted_by=1,
            file_url="/tmp/exact.jpg",
            original_filename="exact.jpg",
            file_size_bytes=10_000_000,
            mime_type="image/jpeg",
        )
        assert entity.file_size_bytes == 10_000_000

    def test_initial_status_is_pending_review(self):
        """New proofs start in pending_review."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        entity = PaymentProofEntity(
            condominium_id=1, unit_id=100, ar_id=1,
            submitted_by=1,
            file_url="/tmp/test.jpg",
            original_filename="test.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )
        assert entity.status == "pending_review"
        assert entity.is_pending() is True

    def test_is_pending_only_true_for_pending_review(self):
        """is_pending() should only return True for pending_review status."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        entity = PaymentProofEntity(
            condominium_id=1, unit_id=100, ar_id=1,
            submitted_by=1, status="approved",
            file_url="/tmp/test.jpg",
            original_filename="test.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )
        assert entity.is_pending() is False

    def test_to_dict_resident_omits_sensitive_fields(self):
        """Resident view must NOT include bank_name, transaction_code, etc."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        entity = PaymentProofEntity(
            id=1, condominium_id=1, unit_id=100, ar_id=1,
            submitted_by=1, status="approved",
            file_url="/tmp/test.jpg",
            original_filename="test.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
            bank_name="BCP",
            transaction_code="OP-123",
            rejection_reason=None,
            reviewed_by=2,
            payment_id=1,
            receipt_id=1,
        )
        resident_dict = entity.to_dict(is_admin=False)
        assert "bank_name" not in resident_dict
        assert "transaction_code" not in resident_dict
        assert "rejection_reason" not in resident_dict
        assert "reviewed_by" not in resident_dict
        assert "payment_id" not in resident_dict
        assert "receipt_id" not in resident_dict
        # Non-sensitive fields should be present
        assert "id" in resident_dict
        assert "status" in resident_dict
        assert "original_filename" in resident_dict
        assert "file_url" in resident_dict

    def test_to_dict_admin_includes_all_fields(self):
        """Admin view must include bank_name, transaction_code and review data."""
        from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
        entity = PaymentProofEntity(
            id=1, condominium_id=1, unit_id=100, ar_id=1,
            submitted_by=1, status="approved",
            file_url="/tmp/test.jpg",
            original_filename="test.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
            bank_name="BCP",
            transaction_code="OP-123",
            rejection_reason=None,
            reviewed_by=2,
            payment_id=1,
            receipt_id=1,
        )
        admin_dict = entity.to_dict(is_admin=True)
        assert admin_dict["bank_name"] == "BCP"
        assert admin_dict["transaction_code"] == "OP-123"
        assert admin_dict["reviewed_by"] == 2
        assert admin_dict["payment_id"] == 1
        assert admin_dict["receipt_id"] == 1


# ═══════════════════════════════════════════════════════════════════════════
# Integration tests — Usecase full flows
# ═══════════════════════════════════════════════════════════════════════════

class TestPaymentProofUsecase:
    """End-to-end usecase tests with real DB."""

    @pytest.fixture(autouse=True)
    def _sandbox(self, db_session):
        """Create a minimal sandbox for each test method."""
        from tests.factories.condo_factory import CondoFactory
        from tests.factories.building_factory import BuildingFactory
        from tests.factories.unit_factory import UnitFactory
        from tests.factories.user_factory import UserFactory
        from tests.factories.resident_factory import ResidentFactory
        from tests.factories.charge_type_factory import ChargeTypeFactory
        from tests.factories.charge_factory import ChargeFactory

        tag = _uuid.uuid4().hex[:8]

        self.condo = CondoFactory.create(db_session, name=f"ProofTest-{tag}")
        self.building = BuildingFactory.create(
            db_session, condominium_id=self.condo.id,
            code=f"BLD-{tag}", name=f"Tower-{tag}",
        )
        self.unit = UnitFactory.create(
            db_session, building_id=self.building.id,
            unit_number=f"{tag[-4:]}-101",
            code=f"UNIT-{tag}-01",
            name=f"Unit {tag} #1",
            floor_number=1,
            occupancy_status="occupied",
        )
        self.user = UserFactory.create(db_session, email=f"proof-usr-{tag}@test.local")
        self.resident = ResidentFactory.create(
            db_session, user_id=self.user.id, condominium_id=self.condo.id
        )
        # Admin user for review operations
        self.admin = UserFactory.create(db_session, email=f"proof-admin-{tag}@test.local")
        ResidentFactory.create(
            db_session, user_id=self.admin.id, condominium_id=self.condo.id
        )

        # AR requires a charge_type and charge
        ct = ChargeTypeFactory.create(
            db_session, condominium_id=self.condo.id,
            code=f"MAINT-{tag}", name="Mantenimiento",
        )
        ChargeFactory.create(
            db_session, condominium_id=self.condo.id,
            unit_id=self.unit.id, charge_type_id=ct.id,
            debtor_user_id=self.user.id, amount=Decimal("350.00"),
            period=f"2026-0{uuid.uuid4().int % 9 + 1}",
            status="pending",
        )

        db_session.commit()

        yield

        _cleanup_by_condo(db_session, self.condo.id)

    # ── helpers ──────────────────────────────────────────────────────────

    def _create_test_ar(self, db_session, amount=Decimal("350.00")):
        """Create a pending AR and return its id."""
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

    def _get_usecase(self):
        from library.dddpy.core_payment_proofs.usecase.payment_proof_usecase import PaymentProofUseCase
        return PaymentProofUseCase()

    # ── Upload ───────────────────────────────────────────────────────────

    def test_upload_pdf_creates_pending_review_proof(self, db_session):
        """Happy path: upload a PDF comprobante."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        result = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/comprobante.pdf",
            original_filename="comprobante_enero.pdf",
            file_size_bytes=512_000,
            mime_type="application/pdf",
        )

        assert result.success is True
        assert result.data["status"] == "pending_review"
        assert result.data["original_filename"] == "comprobante_enero.pdf"
        assert result.data["mime_type"] == "application/pdf"
        assert result.data["id"] > 0

    def test_upload_jpg(self, db_session):
        """Upload image/jpeg."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        result = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/transferencia.jpg",
            original_filename="transferencia_bcp.jpg",
            file_size_bytes=1_200_000,
            mime_type="image/jpeg",
        )

        assert result.success is True
        assert result.data["mime_type"] == "image/jpeg"

    def test_upload_png(self, db_session):
        """Upload image/png."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        result = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/screenshot.png",
            original_filename="screenshot.png",
            file_size_bytes=800_000,
            mime_type="image/png",
        )

        assert result.success is True

    def test_upload_rejects_invalid_mime(self, db_session):
        """Upload with invalid MIME type must raise validation error."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofValidationError,
        )
        with pytest.raises(PaymentProofValidationError) as exc:
            usecase.upload(
                condominium_id=self.condo.id,
                unit_id=self.unit.id,
                ar_id=ar_id,
                submitted_by=self.user.id,
                file_url="/tmp/virus.exe",
                original_filename="factura.exe",
                file_size_bytes=1000,
                mime_type="application/x-msdownload",
            )
        assert "no permitido" in str(exc.value)

    def test_upload_rejects_oversized_file(self, db_session):
        """Files > 10 MB are rejected."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofValidationError,
        )
        with pytest.raises(PaymentProofValidationError) as exc:
            usecase.upload(
                condominium_id=self.condo.id,
                unit_id=self.unit.id,
                ar_id=ar_id,
                submitted_by=self.user.id,
                file_url="/tmp/huge.png",
                original_filename="huge.png",
                file_size_bytes=15_000_000,
                mime_type="image/png",
            )
        assert "excede" in str(exc.value)

    def test_upload_rejects_nonexistent_ar(self, db_session):
        """Upload against a non-existent AR must fail."""
        usecase = self._get_usecase()
        from library.dddpy.core_accounts_receivable.domain.ar_exception import ARNotFound

        with pytest.raises(ARNotFound):
            usecase.upload(
                condominium_id=self.condo.id,
                unit_id=self.unit.id,
                ar_id=999_999,
                submitted_by=self.user.id,
                file_url="/tmp/test.jpg",
                original_filename="test.jpg",
                file_size_bytes=100_000,
                mime_type="image/jpeg",
            )

    # ── Approve ──────────────────────────────────────────────────────────

    def test_approve_full_flow(self, db_session):
        """Approve creates payment + receipt + updates AR to paid."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        # Upload first
        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago_bcp.jpg",
            file_size_bytes=500_000,
            mime_type="image/jpeg",
        )
        proof_id = upload.data["id"]

        # Approve
        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        result = usecase.approve(
            id=proof_id,
            review_data=ApproveProofData(
                bank_name="BCP",
                transaction_code="OP-20260503-001",
                notes="Pago verificado correctamente",
            ),
            reviewed_by=self.admin.id,
        )

        assert result.success is True
        assert result.data["proof"]["status"] == "approved"
        assert result.data["proof"]["bank_name"] == "BCP"
        assert result.data["proof"]["transaction_code"] == "OP-20260503-001"
        assert result.data["receipt"]["receipt_number"] is not None
        assert result.data["payment"]["id"] > 0

    def test_approve_updates_ar_status(self, db_session):
        """After approve, AR must transition from pending → paid."""
        ar_id = self._create_test_ar(db_session, amount=Decimal("500.00"))
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )

        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        usecase.approve(
            id=upload.data["id"],
            review_data=ApproveProofData(
                bank_name="Interbank",
                transaction_code="IB-001",
            ),
            reviewed_by=self.admin.id,
        )

        # Verify AR via usecase (cross-session safe)
        from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
        ar_data = ARUseCase().get_by_id(ar_id).data
        assert ar_data["status"] == "paid"
        assert float(ar_data["paid_amount"]) == 500.0
        assert float(ar_data["pending_amount"]) == 0.0

    def test_approve_rejects_empty_bank_name(self, db_session):
        """bank_name is required for approve."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )

        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofValidationError,
        )
        with pytest.raises(PaymentProofValidationError) as exc:
            usecase.approve(
                id=upload.data["id"],
                review_data=ApproveProofData(bank_name="   ", transaction_code="TXN"),
                reviewed_by=self.admin.id,
            )
        assert "banco" in str(exc.value).lower()

    def test_approve_rejects_empty_transaction_code(self, db_session):
        """transaction_code is required for approve."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )

        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofValidationError,
        )
        with pytest.raises(PaymentProofValidationError) as exc:
            usecase.approve(
                id=upload.data["id"],
                review_data=ApproveProofData(bank_name="BCP", transaction_code=""),
                reviewed_by=self.admin.id,
            )
        assert "código" in str(exc.value).lower() or "transacción" in str(exc.value).lower()

    def test_cannot_approve_already_reviewed_proof(self, db_session):
        """Duplicate approve must raise AlreadyReviewed."""
        ar_id = self._create_test_ar(db_session, amount=Decimal("300.00"))
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )
        proof_id = upload.data["id"]

        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        usecase.approve(
            id=proof_id,
            review_data=ApproveProofData(bank_name="BCP", transaction_code="TXN-1"),
            reviewed_by=self.admin.id,
        )

        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofAlreadyReviewed,
        )
        with pytest.raises(PaymentProofAlreadyReviewed):
            usecase.approve(
                id=proof_id,
                review_data=ApproveProofData(bank_name="BBVA", transaction_code="TXN-2"),
                reviewed_by=self.admin.id,
            )

    def test_cannot_reject_approved_proof(self, db_session):
        """Cannot reject a proof that was already approved."""
        ar_id = self._create_test_ar(db_session, amount=Decimal("200.00"))
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )
        proof_id = upload.data["id"]

        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        usecase.approve(
            id=proof_id,
            review_data=ApproveProofData(bank_name="BCP", transaction_code="TXN"),
            reviewed_by=self.admin.id,
        )

        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofAlreadyReviewed,
        )
        with pytest.raises(PaymentProofAlreadyReviewed):
            usecase.reject(id=proof_id, rejection_reason="Ya fue aprobado", reviewed_by=self.admin.id)

    # ── Reject ───────────────────────────────────────────────────────────

    def test_reject_sets_rejection_reason(self, db_session):
        """Reject stores the reason and updates status."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/dudoso.jpg",
            original_filename="dudoso.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )
        proof_id = upload.data["id"]

        result = usecase.reject(
            id=proof_id,
            rejection_reason="El comprobante no es legible",
            reviewed_by=self.admin.id,
        )

        assert result.success is True
        assert result.data["status"] == "rejected"
        assert result.data["rejection_reason"] == "El comprobante no es legible"

    def test_reject_requires_reason(self, db_session):
        """Reject with empty reason must fail."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/test.jpg",
            original_filename="test.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )

        from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
            PaymentProofValidationError,
        )
        with pytest.raises(PaymentProofValidationError) as exc:
            usecase.reject(id=upload.data["id"], rejection_reason="   ", reviewed_by=self.admin.id)
        assert "motivo" in str(exc.value).lower() or "rechazo" in str(exc.value).lower()

    # ── Visibility ───────────────────────────────────────────────────────

    def test_resident_cannot_see_bank_info(self, db_session):
        """Resident view must strip sensitive financial data."""
        ar_id = self._create_test_ar(db_session, amount=Decimal("250.00"))
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago_interbank.jpg",
            file_size_bytes=200_000,
            mime_type="image/jpeg",
        )
        proof_id = upload.data["id"]

        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        usecase.approve(
            id=proof_id,
            review_data=ApproveProofData(
                bank_name="Interbank",
                transaction_code="IBK-SECRET-123",
            ),
            reviewed_by=self.admin.id,
        )

        # Resident view
        resident_result = usecase.get_by_id(proof_id, is_admin=False)
        assert "bank_name" not in resident_result.data
        assert "transaction_code" not in resident_result.data
        assert resident_result.data["status"] == "approved"
        assert resident_result.data["original_filename"] == "pago_interbank.jpg"

    def test_admin_can_see_all_fields(self, db_session):
        """Admin view includes everything."""
        ar_id = self._create_test_ar(db_session, amount=Decimal("150.00"))
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago_bbva.jpg",
            file_size_bytes=150_000,
            mime_type="image/jpeg",
        )
        proof_id = upload.data["id"]

        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        usecase.approve(
            id=proof_id,
            review_data=ApproveProofData(
                bank_name="BBVA",
                transaction_code="BBVA-789",
            ),
            reviewed_by=self.admin.id,
        )

        admin_result = usecase.get_by_id(proof_id, is_admin=True)
        assert admin_result.data["bank_name"] == "BBVA"
        assert admin_result.data["transaction_code"] == "BBVA-789"
        assert admin_result.data["payment_id"] is not None
        assert admin_result.data["receipt_id"] is not None

    def test_pending_proof_admin_sees_no_bank_info(self, db_session):
        """Pending (unreviewed) proofs have no bank info even for admin."""
        ar_id = self._create_test_ar(db_session)
        usecase = self._get_usecase()

        upload = usecase.upload(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=ar_id,
            submitted_by=self.user.id,
            file_url="/uploads/pago.jpg",
            original_filename="pago.jpg",
            file_size_bytes=100_000,
            mime_type="image/jpeg",
        )

        admin_result = usecase.get_by_id(upload.data["id"], is_admin=True)
        assert admin_result.data.get("bank_name") is None

    # ── List ─────────────────────────────────────────────────────────────

    def test_list_all_as_admin(self, db_session):
        """Admin sees all proofs for a condominium."""
        ar_id = self._create_test_ar(db_session, amount=Decimal("600.00"))
        usecase = self._get_usecase()

        # Upload 2 proofs
        usecase.upload(
            condominium_id=self.condo.id, unit_id=self.unit.id, ar_id=ar_id,
            submitted_by=self.user.id, file_url="/tmp/a.jpg",
            original_filename="a.jpg", file_size_bytes=100_000, mime_type="image/jpeg",
        )
        usecase.upload(
            condominium_id=self.condo.id, unit_id=self.unit.id, ar_id=ar_id,
            submitted_by=self.user.id, file_url="/tmp/b.jpg",
            original_filename="b.jpg", file_size_bytes=100_000, mime_type="image/jpeg",
        )

        result = usecase.list_all(condominium_id=self.condo.id, is_admin=True)
        assert len(result.data["items"]) == 2

    def test_list_filter_by_status(self, db_session):
        """Filter proofs by status."""
        ar_id = self._create_test_ar(db_session, amount=Decimal("400.00"))
        usecase = self._get_usecase()

        u1 = usecase.upload(
            condominium_id=self.condo.id, unit_id=self.unit.id, ar_id=ar_id,
            submitted_by=self.user.id, file_url="/tmp/a.jpg",
            original_filename="a.jpg", file_size_bytes=100_000, mime_type="image/jpeg",
        )
        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData
        usecase.approve(
            id=u1.data["id"],
            review_data=ApproveProofData(bank_name="BCP", transaction_code="TXN"),
            reviewed_by=self.admin.id,
        )

        pending = usecase.list_all(
            condominium_id=self.condo.id, status="pending_review", is_admin=True
        )
        approved = usecase.list_all(
            condominium_id=self.condo.id, status="approved", is_admin=True
        )

        assert len(pending.data["items"]) == 0
        assert len(approved.data["items"]) == 1


# ═══════════════════════════════════════════════════════════════════════════
# Repository tests
# ═══════════════════════════════════════════════════════════════════════════

class TestPaymentProofRepository:
    """CMD + Query repository operations against real DB."""

    @pytest.fixture(autouse=True)
    def _sandbox(self, db_session):
        from tests.factories.condo_factory import CondoFactory
        from tests.factories.building_factory import BuildingFactory
        from tests.factories.unit_factory import UnitFactory
        from tests.factories.user_factory import UserFactory

        tag = _uuid.uuid4().hex[:8]
        self.condo = CondoFactory.create(db_session, name=f"RepoTest-{tag}")
        self.building = BuildingFactory.create(
            db_session, condominium_id=self.condo.id,
            code=f"BLD-{tag}", name=f"Tower-{tag}",
        )
        self.unit = UnitFactory.create(
            db_session, building_id=self.building.id,
            unit_number=f"{tag[-4:]}-201",
            code=f"UNIT-{tag}-02",
            name=f"Unit {tag} #2",
            floor_number=2,
            occupancy_status="occupied",
        )
        self.user = UserFactory.create(db_session, email=f"repo-{tag}@test.local")
        db_session.commit()
        yield
        _cleanup_by_condo(db_session, self.condo.id)

    def _create_proof(self, db_session, **overrides):
        from tests.factories.payment_proof_factory import PaymentProofFactory
        defaults = dict(
            condominium_id=self.condo.id,
            unit_id=self.unit.id,
            ar_id=1,
            submitted_by=self.user.id,
        )
        defaults.update(overrides)
        proof = PaymentProofFactory.create(db_session, **defaults)
        db_session.commit()
        return proof

    def test_cmd_insert_creates_record(self, db_session):
        """CMD repo insert persists a proof."""
        proof = self._create_proof(db_session)
        assert proof.id > 0
        assert proof.status == "pending_review"

    def test_cmd_approve_transitions_status(self, db_session):
        """CMD repo approve() updates status + bank fields."""
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_cmd_repository import (
            PaymentProofCMDRepositoryImpl,
        )
        from library.dddpy.core_payment_proofs.domain.payment_proof_data import ApproveProofData

        proof = self._create_proof(db_session)
        repo = PaymentProofCMDRepositoryImpl()

        ok = repo.approve(
            proof.id,
            ApproveProofData(bank_name="BCP", transaction_code="TXN-001", notes="OK"),
            reviewed_by=self.user.id,
        )
        assert ok is True

        # Re-fetch via raw SQL (avoid session cache)
        db_session.expire_all()
        from sqlalchemy import text
        row = db_session.execute(
            text("SELECT status, bank_name, transaction_code FROM payment_proofs WHERE id = :id"),
            {"id": proof.id},
        ).fetchone()
        assert row[0] == "approved"
        assert row[1] == "BCP"
        assert row[2] == "TXN-001"

    def test_cmd_reject_transitions_status(self, db_session):
        """CMD repo reject() updates status + reason."""
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_cmd_repository import (
            PaymentProofCMDRepositoryImpl,
        )

        proof = self._create_proof(db_session)
        repo = PaymentProofCMDRepositoryImpl()

        ok = repo.reject(proof.id, "Imagen borrosa", reviewed_by=self.user.id)
        assert ok is True

        db_session.expire_all()
        from sqlalchemy import text
        row = db_session.execute(
            text("SELECT status, rejection_reason FROM payment_proofs WHERE id = :id"),
            {"id": proof.id},
        ).fetchone()
        assert row[0] == "rejected"
        assert row[1] == "Imagen borrosa"

    def test_cmd_link_payment(self, db_session):
        """CMD repo link_payment() sets payment_id + receipt_id."""
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_cmd_repository import (
            PaymentProofCMDRepositoryImpl,
        )

        proof = self._create_proof(db_session)
        repo = PaymentProofCMDRepositoryImpl()

        ok = repo.link_payment(proof.id, payment_id=42, receipt_id=7)
        assert ok is True

        db_session.expire_all()
        from sqlalchemy import text
        row = db_session.execute(
            text("SELECT payment_id, receipt_id FROM payment_proofs WHERE id = :id"),
            {"id": proof.id},
        ).fetchone()
        assert row[0] == 42
        assert row[1] == 7

    def test_query_get_by_id_returns_entity(self, db_session):
        """Query repo get_by_id() returns a valid entity."""
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )

        proof = self._create_proof(db_session)
        repo = PaymentProofQueryRepositoryImpl()

        result = repo.get_by_id(proof.id)
        assert result is not None
        assert result.id == proof.id
        assert result.status == "pending_review"

    def test_query_get_by_id_not_found(self, db_session):
        """Query repo returns None for non-existent id."""
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )
        repo = PaymentProofQueryRepositoryImpl()
        assert repo.get_by_id(999_999) is None

    def test_query_list_by_condominium(self, db_session):
        """Query repo list_by_condominium returns paginated results."""
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )

        self._create_proof(db_session)
        self._create_proof(db_session, original_filename="segundo.jpg")
        self._create_proof(db_session, original_filename="tercero.jpg")

        repo = PaymentProofQueryRepositoryImpl()
        items, total = repo.list_by_condominium(
            condominium_id=self.condo.id, skip=0, limit=10
        )
        assert total == 3
        assert len(items) == 3

    def test_query_list_by_condominium_with_status_filter(self, db_session):
        """Query repo filters by status correctly."""
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )

        self._create_proof(db_session, status="pending_review")
        self._create_proof(db_session, status="approved")
        self._create_proof(db_session, status="rejected")

        repo = PaymentProofQueryRepositoryImpl()
        pending_items, pending_total = repo.list_by_condominium(
            condominium_id=self.condo.id, skip=0, limit=10, status="pending_review"
        )
        assert pending_total == 1
        assert len(pending_items) == 1

        approved_items, _ = repo.list_by_condominium(
            condominium_id=self.condo.id, skip=0, limit=10, status="approved"
        )
        assert len(approved_items) == 1

    def test_query_list_by_ar(self, db_session):
        """Query repo list_by_ar returns proofs for a specific AR."""
        from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
            PaymentProofQueryRepositoryImpl,
        )

        self._create_proof(db_session, ar_id=100, original_filename="ar100.jpg")
        self._create_proof(db_session, ar_id=100, original_filename="ar100_v2.jpg")
        self._create_proof(db_session, ar_id=200, original_filename="ar200.jpg")

        repo = PaymentProofQueryRepositoryImpl()
        items, total = repo.list_by_ar(ar_id=100)
        assert total == 2
        assert all(i.original_filename.startswith("ar100") for i in items)
