"""
Factory: Charge.

Creates test charge records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_charges.infrastructure.dbcharge import DBCharge


class ChargeFactory:
    """Factory for creating test Charge records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        charge_type_id: int,
        scope: str = "unit",
        unit_id: int = None,
        building_id: int = None,
        amount: Decimal = None,
        currency: str = "PEN",
        distribution_mode: str = "fixed_unit_amount",
        description: str = None,
        is_recurrent: int = 0,
        period_pattern: str = None,
        start_date: date = None,
        end_date: date = None,
        status: str = "active",
        **kwargs,
    ) -> DBCharge:
        db_charge = DBCharge(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            charge_type_id=charge_type_id,
            scope=scope,
            unit_id=unit_id,
            building_id=building_id,
            distribution_mode=distribution_mode,
            description=description or "Factory-created charge",
            amount=amount or Decimal("150.00"),
            currency=currency,
            is_recurrent=is_recurrent,
            period_pattern=period_pattern,
            start_date=start_date or date.today(),
            end_date=end_date,
            status=status,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_charge)
        session.flush()
        session.refresh(db_charge)
        return db_charge
