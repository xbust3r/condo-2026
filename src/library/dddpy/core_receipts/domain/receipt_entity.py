"""
Receipt domain entity — DDD for payment receipts.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any


class ReceiptEntity:
    """Entidad de dominio para un recibo de pago."""

    VALID_PAYMENT_METHODS = {"cash", "bank_transfer", "yape", "plin", "card", "other"}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        unit_id: int,
        ar_id: int,
        receipt_number: str,
        issued_at: datetime,
        payer_user_id: int,
        amount_paid: Decimal,
        payment_method: str,
        reference: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        # Enriched
        payer_name: Optional[str] = None,
        payer_email: Optional[str] = None,
        unit_code: Optional[str] = None,
        condominium_name: Optional[str] = None,
        ar_reference: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.unit_id = unit_id
        self.ar_id = ar_id
        self.receipt_number = receipt_number
        self.issued_at = issued_at
        self.payer_user_id = payer_user_id
        self.amount_paid = amount_paid
        self.payment_method = payment_method
        self.reference = reference
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        # Enrichment
        self.payer_name = payer_name
        self.payer_email = payer_email
        self.unit_code = unit_code
        self.condominium_name = condominium_name
        self.ar_reference = ar_reference

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "unit_id": self.unit_id,
            "ar_id": self.ar_id,
            "receipt_number": self.receipt_number,
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
            "payer_user_id": self.payer_user_id,
            "amount_paid": float(self.amount_paid),
            "payment_method": self.payment_method,
            "reference": self.reference,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # Enrichment
            "payer_name": self.payer_name,
            "payer_email": self.payer_email,
            "unit_code": self.unit_code,
            "condominium_name": self.condominium_name,
            "ar_reference": self.ar_reference,
        }
