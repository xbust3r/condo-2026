"""
Factory: ChargeType.

Creates test charge type records directly in the DB via SQLAlchemy.
"""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_charge_types.infrastructure.dbcharge_type import DBChargeType


class ChargeTypeFactory:
    """Factory for creating test ChargeType records."""

    @staticmethod
    def create(
        session: Session,
        code: str = None,
        name: str = None,
        description: str = None,
        is_global: int = 1,
        is_active: int = 1,
        sort_order: int = 0,
        **kwargs,
    ) -> DBChargeType:
        if code is None:
            code = f"CT-{uuid.uuid4().hex[:8].upper()}"

        db_ct = DBChargeType(
            uuid=str(uuid.uuid4()),
            code=code,
            name=name or "Test Charge Type",
            description=description or "Factory-created charge type",
            is_global=is_global,
            is_active=is_active,
            sort_order=sort_order,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_ct)
        session.flush()
        session.refresh(db_ct)
        return db_ct
