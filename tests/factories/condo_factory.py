"""
Factory: CondominiumEntity.

Creates test condominium records directly in the DB via SQLAlchemy,
bypassing the session_scope wrapper so tests control the session lifecycle.
"""
import uuid
from decimal import Decimal
from sqlalchemy.orm import Session

from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums


class CondoFactory:
    """Factory for creating test Condominium records."""

    @staticmethod
    def create(
        session: Session,
        code: str = None,
        name: str = None,
        description: str = None,
        land_area: Decimal = None,
        built_area: Decimal = None,
        address: str = None,
        city: str = None,
        country: str = None,
        contact_email: str = None,
        document_number: str = None,
        **kwargs,
    ) -> DBCondominiums:
        """
        Create and persist a Condominium record.

        Usage:
            condo = CondoFactory.create(session, name="Las Lomas")
        """
        if code is None:
            code = f"CONDO-{uuid.uuid4().hex[:8].upper()}"

        db_condo = DBCondominiums(
            uuid=str(uuid.uuid4()),
            code=code,
            name=name or "Test Condominium",
            description=description or "Factory-created test condominium",
            land_area=land_area or Decimal("5000.0000"),
            built_area=built_area or Decimal("8000.0000"),
            area_unit="m2",
            address=address or "Av. Test 123",
            city=city or "Lima",
            country=country or "Perú",
            contact_email=contact_email,
            document_number=document_number,
            status=kwargs.get("status", 1),
        )
        session.add(db_condo)
        session.flush()
        session.refresh(db_condo)
        return db_condo
