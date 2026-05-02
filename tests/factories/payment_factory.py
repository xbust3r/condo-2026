"""
Factory: Payment.

Creates test payment records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_payments.infrastructure.dbpayment import DBPayment


class PaymentFactory:
    """Factory for creating test Payment records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        unit_id: int,
        ar_id: int,
        payer_user_id: int,
        amount: Decimal = None,
        payment_method: str = "transfer",
        reference: str = None,
        paid_at: datetime = None,
        receipt_id: int = None,
        **kwargs,
    ) -> DBPayment:
        db_payment = DBPayment(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            unit_id=unit_id,
            ar_id=ar_id,
            payer_user_id=payer_user_id,
            amount=amount or Decimal("150.00"),
            payment_method=payment_method,
            reference=reference or f"PAY-{uuid.uuid4().hex[:8].upper()}",
            paid_at=paid_at or datetime.utcnow(),
            receipt_id=receipt_id,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_payment)
        session.flush()
        session.refresh(db_payment)
        return db_payment
