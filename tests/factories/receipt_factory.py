"""
Factory: Receipt.

Creates test receipt records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_receipts.infrastructure.dbreceipt import DBReceipt


class ReceiptFactory:
    """Factory for creating test Receipt records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        unit_id: int,
        ar_id: int,
        payer_user_id: int,
        amount_paid: Decimal = None,
        payment_method: str = "transfer",
        receipt_number: str = None,
        reference: str = None,
        issued_at: datetime = None,
        notes: str = None,
        **kwargs,
    ) -> DBReceipt:
        db_receipt = DBReceipt(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            unit_id=unit_id,
            ar_id=ar_id,
            receipt_number=receipt_number or f"REC-{uuid.uuid4().hex[:8].upper()}",
            issued_at=issued_at or datetime.utcnow(),
            payer_user_id=payer_user_id,
            amount_paid=amount_paid or Decimal("150.00"),
            payment_method=payment_method,
            reference=reference,
            notes=notes,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_receipt)
        session.flush()
        session.refresh(db_receipt)
        return db_receipt
