"""
from typing import Optional
Payment domain entity — DDD for payments against AR.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any


class PaymentEntity:
    """Entidad de dominio para un pago contra AR."""

    VALID_PAYMENT_METHODS = {"cash", "bank_transfer", "yape", "plin", "card", "other"}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        unit_id: int,
        ar_id: int,
        receipt_id: Optional[int] = None,
        payer_user_id: int = None,
        amount: Decimal = Decimal("0.00"),
        payment_method: str = None,
        reference: Optional[str] = None,
        paid_at: datetime = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched
        receipt_number: Optional[str] = None,
        payer_name: Optional[str] = None,
        unit_code: Optional[str] = None,
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.unit_id = unit_id
        self.ar_id = ar_id
        self.receipt_id = receipt_id
        self.payer_user_id = payer_user_id
        self.amount = amount
        self.payment_method = payment_method
        self.reference = reference
        self.paid_at = paid_at
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.receipt_number = receipt_number
        self.payer_name = payer_name
        self.unit_code = unit_code
        self.condominium_name = condominium_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "unit_id": self.unit_id,
            "ar_id": self.ar_id,
            "receipt_id": self.receipt_id,
            "payer_user_id": self.payer_user_id,
            "amount": float(self.amount),
            "payment_method": self.payment_method,
            "reference": self.reference,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # Enrichment
            "receipt_number": self.receipt_number,
            "payer_name": self.payer_name,
            "unit_code": self.unit_code,
            "condominium_name": self.condominium_name,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None
