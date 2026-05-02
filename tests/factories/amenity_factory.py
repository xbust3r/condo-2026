"""
Factory: Amenity.

Creates test amenity records directly in the DB via SQLAlchemy.
"""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity


class AmenityFactory:
    """Factory for creating test Amenity records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        name: str = None,
        scope: str = "CONDOMINIUM",
        building_id: int = None,
        description: str = None,
        location: str = None,
        max_capacity: int = 1,
        booking_duration_min: int = 60,
        requires_approval: bool = False,
        status: str = "active",
        **kwargs,
    ) -> DBAmenity:
        db_amenity = DBAmenity(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            scope=scope,
            building_id=building_id,
            name=name or "Factory Amenity",
            description=description or "Test amenity",
            location=location or "Floor 1",
            max_capacity=max_capacity,
            booking_duration_min=booking_duration_min,
            requires_approval=requires_approval,
            status=status,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_amenity)
        session.flush()
        session.refresh(db_amenity)
        return db_amenity
