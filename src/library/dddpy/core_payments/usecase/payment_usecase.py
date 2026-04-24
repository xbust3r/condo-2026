"""
Payment use case — orchestrates payment + receipt generation.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from library.dddpy.core_payments.usecase.payment_cmd_schema import CreatePaymentSchema
from library.dddpy.core_payments.domain.payment_entity import PaymentEntity
from library.dddpy.core_payments.domain.payment_exception import (
    PaymentNotFound,
    PaymentExceedsBalance,
)
from library.dddpy.core_payments.domain.payment_success import PaymentSuccessMessage
from library.dddpy.core_payments.infrastructure.payment_cmd_repository import (
    PaymentCmdRepositoryImpl,
)
from library.dddpy.core_payments.infrastructure.payment_query_repository import (
    PaymentQueryRepositoryImpl,
)
from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
from library.dddpy.core_receipts.usecase.receipt_usecase import ReceiptUseCase
from library.dddpy.core_receipts.usecase.receipt_cmd_schema import CreateReceiptSchema
from library.dddpy.core_accounts_receivable.domain.ar_exception import ARPaymentExceedsBalance
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PaymentUseCase")


class PaymentUseCase:

    def __init__(self):
        self._cmd = PaymentCmdRepositoryImpl()
        self._query = PaymentQueryRepositoryImpl()
        self._ar_usecase = ARUseCase()
        self._receipt_usecase = ReceiptUseCase()
        logger.info("PaymentUseCase initialized")

    def create(self, data: CreatePaymentSchema) -> PaymentEntity:
        """
        Register a payment:
          1. Validate AR exists and amount ≤ pending balance (PAY-01)
          2. Generate receipt_number (auto-incremental per condominium)
          3. Create receipt
          4. Create payment with receipt_id
          5. Update AR status (add_payment handles recalculation)
        All within a consistent transaction.
        """
        logger.add_inside_method("create") if hasattr(logger, 'add_inside_method') else None

        # Get AR to validate and get context
        ar_response = self._ar_usecase.get_by_id(data.ar_id)
        ar = ar_response.data

        # PAY-01: validate amount ≤ pending
        pending = ar["pending_amount"]
        if float(data.amount) > pending:
            raise PaymentExceedsBalance(
                f"Payment {data.amount} exceeds pending {pending}"
            )

        # Generate receipt number
        receipt_number = self._receipt_usecase.get_next_receipt_number(ar["condominium_id"])

        # Create receipt first
        receipt_data = CreateReceiptSchema(
            condominium_id=ar["condominium_id"],
            unit_id=ar["unit_id"],
            ar_id=ar["id"],
            receipt_number=receipt_number,
            issued_at=data.paid_at or datetime.utcnow(),
            payer_user_id=data.payer_user_id,
            amount_paid=float(data.amount),
            payment_method=data.payment_method,
            reference=data.reference,
        )
        receipt = self._receipt_usecase.create(receipt_data)

        # Create payment with receipt_id
        payment_data = self._cmd.create(
            data,
            receipt_id=receipt.id,
        )
        return payment_data

    def create_with_ar_update(self, data: CreatePaymentSchema) -> ResponseSuccessSchema:
        """Full flow: register payment + update AR status + return receipt."""
        ar_response = self._ar_usecase.get_by_id(data.ar_id)
        ar = ar_response.data

        # PAY-01 check
        if float(data.amount) > ar["pending_amount"]:
            raise PaymentExceedsBalance(
                f"Payment {data.amount} exceeds pending {ar['pending_amount']}"
            )

        receipt_number = self._receipt_usecase.get_next_receipt_number(ar["condominium_id"])

        # Create receipt
        receipt_data = CreateReceiptSchema(
            condominium_id=ar["condominium_id"],
            unit_id=ar["unit_id"],
            ar_id=ar["id"],
            receipt_number=receipt_number,
            issued_at=data.paid_at or datetime.utcnow(),
            payer_user_id=data.payer_user_id,
            amount_paid=float(data.amount),
            payment_method=data.payment_method,
            reference=data.reference,
        )
        receipt = self._receipt_usecase.create(receipt_data)

        # Create payment
        payment = self._cmd.create(data, receipt_id=receipt.id)

        # Update AR (recalculates status)
        from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import RecordPaymentSchema
        ar_update_response = self._ar_usecase.record_payment(
            data.ar_id,
            RecordPaymentSchema(
                amount=float(data.amount),
                payment_method=data.payment_method,
                reference=data.reference,
                paid_by_user_id=data.payer_user_id,
            )
        )

        return ResponseSuccessSchema(
            success=True,
            message=PaymentSuccessMessage.CREATED,
            data={
                "payment": payment.to_dict(),
                "receipt": receipt.to_dict(),
                "ar": ar_update_response.data,
            },
        )

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        entity = self._query.get_by_id(id)
        if not entity:
            raise PaymentNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=PaymentSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise PaymentNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=PaymentSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        ar_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        if limit > 500:
            limit = 500
        entities, total = self._query.list_all(
            skip=skip, limit=limit,
            condominium_id=condominium_id,
            unit_id=unit_id,
            ar_id=ar_id,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message=PaymentSuccessMessage.LISTED,
            data={
                "items": [e.to_dict() for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
            },
        )
