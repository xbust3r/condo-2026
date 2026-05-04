"""
Payment Proof Use Case — orchestrates upload, review, and payment flow.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
from library.dddpy.core_payment_proofs.domain.payment_proof_data import (
    CreatePaymentProofData,
    ApproveProofData,
    RejectProofData,
)
from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
    PaymentProofNotFound,
    PaymentProofAlreadyReviewed,
    PaymentProofInvalidFileType,
    PaymentProofFileTooLarge,
    PaymentProofValidationError,
)
from library.dddpy.core_payment_proofs.domain.payment_proof_success import (
    PaymentProofSuccessMessage,
)
from library.dddpy.core_payment_proofs.infrastructure.payment_proof_cmd_repository import (
    PaymentProofCmdRepositoryImpl,
)
from library.dddpy.core_payment_proofs.infrastructure.payment_proof_query_repository import (
    PaymentProofQueryRepositoryImpl,
)
from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
from library.dddpy.core_receipts.usecase.receipt_usecase import ReceiptUseCase
from library.dddpy.core_receipts.usecase.receipt_cmd_schema import CreateReceiptSchema
from library.dddpy.core_payments.usecase.payment_usecase import PaymentUseCase
from library.dddpy.core_payments.usecase.payment_cmd_schema import CreatePaymentSchema
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PaymentProofUseCase")


class PaymentProofUseCase:

    def __init__(self):
        self._cmd = PaymentProofCmdRepositoryImpl()
        self._query = PaymentProofQueryRepositoryImpl()
        self._ar_usecase = ARUseCase()
        self._receipt_usecase = ReceiptUseCase()
        self._payment_usecase = PaymentUseCase()
        logger.info("PaymentProofUseCase initialized")

    def upload(
        self,
        condominium_id: int,
        unit_id: int,
        ar_id: int,
        submitted_by: int,
        file_url: str,
        original_filename: str,
        file_size_bytes: int,
        mime_type: str,
    ) -> ResponseSuccessSchema:
        """
        Register a payment proof upload.
        Validates MIME type and file size before persisting.
        """
        logger.add_inside_method("upload") if hasattr(logger, "add_inside_method") else None

        # Validate MIME type
        if mime_type not in PaymentProofEntity.ALLOWED_MIME_TYPES:
            raise PaymentProofInvalidFileType(mime_type)

        # Validate file size
        if file_size_bytes > PaymentProofEntity.MAX_FILE_SIZE_BYTES:
            raise PaymentProofFileTooLarge(
                max_mb=PaymentProofEntity.MAX_FILE_SIZE_BYTES // (1024 * 1024)
            )

        # Validate AR exists
        ar_response = self._ar_usecase.get_by_id(ar_id)

        data = CreatePaymentProofData(
            condominium_id=condominium_id,
            unit_id=unit_id,
            ar_id=ar_id,
            submitted_by=submitted_by,
            file_url=file_url,
            original_filename=original_filename,
            file_size_bytes=file_size_bytes,
            mime_type=mime_type,
        )
        proof_id = self._cmd.create(data)

        entity = self._query.get_by_id(proof_id)
        return ResponseSuccessSchema(
            success=True,
            message=PaymentProofSuccessMessage.CREATED,
            data=entity.to_dict(),
        )

    def get_by_id(self, id: int, is_admin: bool = False) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        if not entity:
            raise PaymentProofNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=PaymentProofSuccessMessage.RETRIEVED,
            data=entity.to_dict(is_admin=is_admin),
        )

    def get_by_uuid(self, uuid: str, is_admin: bool = False) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise PaymentProofNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=PaymentProofSuccessMessage.RETRIEVED,
            data=entity.to_dict(is_admin=is_admin),
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        ar_id: Optional[int] = None,
        status: Optional[str] = None,
        submitted_by: Optional[int] = None,
        include_deleted: bool = False,
        is_admin: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500

        entities, total = self._query.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            unit_id=unit_id,
            ar_id=ar_id,
            status=status,
            submitted_by=submitted_by,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message=PaymentProofSuccessMessage.LISTED,
            data={
                "items": [e.to_dict(is_admin=is_admin) for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
            },
        )

    def approve(
        self,
        id: int,
        review_data: ApproveProofData,
        reviewed_by: int,
    ) -> ResponseSuccessSchema:
        """
        Approve a payment proof:
        1. Validate proof is pending_review
        2. Create payment + receipt + update AR (via PaymentUseCase)
        3. Update proof with bank/transaction data + link payment/receipt

        Note: PaymentUseCase.create_with_ar_update handles receipt creation
        and AR status update atomically. We don't create a separate receipt.
        """
        logger.add_inside_method("approve") if hasattr(logger, "add_inside_method") else None

        proof = self._query.get_by_id(id)
        if not proof:
            raise PaymentProofNotFound()
        if not proof.is_pending():
            raise PaymentProofAlreadyReviewed()

        if not review_data.bank_name or not review_data.bank_name.strip():
            raise PaymentProofValidationError("El nombre del banco es requerido")
        if not review_data.transaction_code or not review_data.transaction_code.strip():
            raise PaymentProofValidationError(
                "El código de transacción es requerido"
            )

        # Get AR pending amount for the payment
        ar_response = self._ar_usecase.get_by_id(proof.ar_id)
        ar = ar_response.data

        # Create payment + receipt + update AR (all handled by PaymentUseCase)
        payment_schema = CreatePaymentSchema(
            ar_id=proof.ar_id,
            payer_user_id=proof.submitted_by,
            amount=float(ar["pending_amount"]),
            payment_method=review_data.payment_method,
            reference=review_data.transaction_code,
            paid_at=datetime.utcnow(),
        )
        payment_response = self._payment_usecase.create_with_ar_update(payment_schema)
        payment = payment_response.data["payment"]
        receipt = payment_response.data["receipt"]

        # Update proof: status, admin data, payment/receipt linkage
        ok = self._cmd.approve(id, review_data, reviewed_by)
        if not ok:
            raise PaymentProofNotFound()

        self._cmd.link_payment(id, payment["id"], receipt["id"])

        # Re-fetch fresh entity
        updated_proof = self._query.get_by_id(id)

        return ResponseSuccessSchema(
            success=True,
            message=PaymentProofSuccessMessage.APPROVED,
            data={
                "proof": updated_proof.to_dict(is_admin=True),
                "payment": payment,
                "receipt": receipt,
                "ar": payment_response.data.get("ar", {}),
            },
        )

    def reject(
        self,
        id: int,
        rejection_reason: str,
        reviewed_by: int,
    ) -> ResponseSuccessSchema:
        """
        Reject a payment proof.
        Does NOT create any payment or modify AR.
        """
        logger.add_inside_method("reject") if hasattr(logger, "add_inside_method") else None

        proof = self._query.get_by_id(id)
        if not proof:
            raise PaymentProofNotFound()
        if not proof.is_pending():
            raise PaymentProofAlreadyReviewed()

        if not rejection_reason or not rejection_reason.strip():
            raise PaymentProofValidationError("El motivo de rechazo es requerido")

        ok = self._cmd.reject(id, rejection_reason.strip(), reviewed_by)
        if not ok:
            raise PaymentProofNotFound()

        updated_proof = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=PaymentProofSuccessMessage.REJECTED,
            data=updated_proof.to_dict(is_admin=True),
        )

    def soft_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("soft_delete")
        ok = self._cmd.soft_delete(id)
        if not ok:
            raise PaymentProofNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Comprobante eliminado",
            data=None,
        )
