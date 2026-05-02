"""
Factory: Package.

Creates test package records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_packages.infrastructure.dbpackage import DBPackage


class PackageFactory:
    """Factory for creating test Package records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        unit_id: int,
        recipient_user_id: int,
        carrier: str = None,
        tracking_number: str = None,
        description: str = None,
        status: str = "pending",
        received_at: datetime = None,
        pickup_code: str = None,
        **kwargs,
    ) -> DBPackage:
        db_pkg = DBPackage(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            unit_id=unit_id,
            recipient_user_id=recipient_user_id,
            carrier=carrier or "Test Carrier",
            tracking_number=tracking_number or f"TRK-{uuid.uuid4().hex[:8].upper()}",
            description=description or "Factory-created package",
            status=status,
            received_at=received_at or datetime.utcnow(),
            pickup_code=pickup_code or "1234",
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_pkg)
        session.flush()
        session.refresh(db_pkg)
        return db_pkg
