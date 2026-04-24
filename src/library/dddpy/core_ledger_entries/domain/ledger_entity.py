"""
LedgerEntry domain entity — DDD for unit financial ledger.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any


class LedgerEntryEntity:
    """Entidad de dominio para una entrada del libro mayor de una unidad."""

    VALID_ENTRY_TYPES = {"charge", "payment", "adjustment", "balance_forward"}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        unit_id: int,
        entry_type: str,
        ar_id: Optional[int] = None,
        payment_id: Optional[int] = None,
        charge_id: Optional[int] = None,
        description: str = "",
        debit: Decimal = Decimal("0.00"),
        credit: Decimal = Decimal("0.00"),
        balance: Decimal = Decimal("0.00"),
        period: Optional[str] = None,
        reference: Optional[str] = None,
        created_at: Optional[datetime] = None,
        # Enrichment
        unit_code: Optional[str] = None,
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.unit_id = unit_id
        self.entry_type = entry_type
        self.ar_id = ar_id
        self.payment_id = payment_id
        self.charge_id = charge_id
        self.description = description
        self.debit = debit
        self.credit = credit
        self.balance = balance
        self.period = period
        self.reference = reference
        self.created_at = created_at
        # Enrichment
        self.unit_code = unit_code
        self.condominium_name = condominium_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "unit_id": self.unit_id,
            "entry_type": self.entry_type,
            "ar_id": self.ar_id,
            "payment_id": self.payment_id,
            "charge_id": self.charge_id,
            "description": self.description,
            "debit": float(self.debit),
            "credit": float(self.credit),
            "balance": float(self.balance),
            "period": self.period,
            "reference": self.reference,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # Enrichment
            "unit_code": self.unit_code,
            "condominium_name": self.condominium_name,
        }
