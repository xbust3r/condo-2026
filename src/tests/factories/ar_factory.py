"""
Factory: AccountsReceivable.

Creates test AR records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR


class AccountsReceivableFactory:
    """Factory for creating test AccountsReceivable records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        unit_id: int,
        debtor_user_id: int,
        amount: Decimal = None,
        due_date: date = None,
        status: str = "pending",
        charge_id: int = None,
        paid_amount: Decimal = None,
        currency: str = "PEN",
        description: str = None,
        reference_code: str = None,
        period: str = None,
        **kwargs,
    ) -> DBAR:
        db_ar = DBAR(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            unit_id=unit_id,
            debtor_user_id=debtor_user_id,
            amount=amount or Decimal("150.00"),
            due_date=due_date or date.today(),
            status=status,
            charge_id=charge_id,
            paid_amount=paid_amount or Decimal("0.00"),
            currency=currency,
            description=description or "Factory-created AR",
            reference_code=reference_code or f"AR-{uuid.uuid4().hex[:8].upper()}",
            period=period,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_ar)
        session.flush()
        session.refresh(db_ar)
        return db_ar
