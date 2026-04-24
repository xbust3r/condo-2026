"""
from typing import Optional
AccountsReceivable domain entity — DDD for condominium accounts receivable.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any


class AREntity:
    """Entidad de dominio para una cuenta por cobrar."""

    # Valid status transitions:
    # pending → partial (when first payment received)
    # pending → overdue (when due_date < today AND amount > 0)
    # partial → paid (when paid_amount == amount)
    # partial → overdue (when due_date < today AND paid_amount < amount)
    # overdue → paid (when paid_amount == amount)
    VALID_STATUSES = {"pending", "partial", "paid", "overdue", "cancelled"}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        unit_id: int,
        debtor_user_id: int,
        reference_code: Optional[str] = None,
        description: Optional[str] = None,
        amount: Decimal = Decimal("0.00"),
        paid_amount: Decimal = Decimal("0.00"),
        currency: str = "PEN",
        status: str = "pending",
        due_date: date = None,
        period: Optional[str] = None,
        charge_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched fields
        debtor_name: Optional[str] = None,
        debtor_email: Optional[str] = None,
        unit_code: Optional[str] = None,
        condominium_name: Optional[str] = None,
        charge_description: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.unit_id = unit_id
        self.debtor_user_id = debtor_user_id
        self.reference_code = reference_code
        self.description = description
        self.amount = amount
        self.paid_amount = paid_amount
        self.currency = currency
        self.status = status
        self.due_date = due_date
        self.period = period
        self.charge_id = charge_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.debtor_name = debtor_name
        self.debtor_email = debtor_email
        self.unit_code = unit_code
        self.condominium_name = condominium_name
        self.charge_description = charge_description

    @property
    def pending_amount(self) -> Decimal:
        """Outstanding balance = amount - paid_amount."""
        return self.amount - self.paid_amount

    @property
    def is_fully_paid(self) -> bool:
        return self.paid_amount >= self.amount

    @property
    def is_overdue(self) -> bool:
        return (
            self.status in ("pending", "partial")
            and self.due_date < date.today()
            and self.pending_amount > 0
        )

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.status not in self.VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )
        if self.amount <= 0:
            raise ValueError("amount must be > 0")
        if self.paid_amount < 0:
            raise ValueError("paid_amount cannot be negative")
        if self.paid_amount > self.amount:
            raise ValueError("paid_amount cannot exceed amount")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "unit_id": self.unit_id,
            "debtor_user_id": self.debtor_user_id,
            "reference_code": self.reference_code,
            "description": self.description,
            "amount": float(self.amount),
            "paid_amount": float(self.paid_amount),
            "pending_amount": float(self.pending_amount),
            "currency": self.currency,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "period": self.period,
            "charge_id": self.charge_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # Enrichment
            "debtor_name": self.debtor_name,
            "debtor_email": self.debtor_email,
            "unit_code": self.unit_code,
            "condominium_name": self.condominium_name,
            "charge_description": self.charge_description,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status in ("pending", "partial", "overdue") and not self.is_deleted()
