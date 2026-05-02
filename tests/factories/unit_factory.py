"""
Factory: UnitEntity (core_units table).

Creates test unit records directly in the DB via SQLAlchemy.
"""
import uuid
from decimal import Decimal
from sqlalchemy.orm import Session

from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from sqlalchemy import func


class UnitFactory:
    """Factory for creating test Unit records."""

    @staticmethod
    def create(
        session: Session,
        building_id: int,
        unit_number: str = None,
        code: str = None,
        name: str = None,
        unit_type_id: int = None,
        private_area: Decimal = None,
        coefficient: Decimal = None,
        floor_number: int = None,
        floor_label: str = None,
        occupancy_status: str = "occupied",
        sort_order: int = None,
        status: int = 1,
        **kwargs,
    ) -> DBUnits:
        """
        Create and persist a Unit record.

        Usage:
            unit = UnitFactory.create(
                session,
                building_id=building.id,
                unit_number="101",
                code="UNIT-101"
            )
        """
        if code is None:
            code = f"UNIT-{uuid.uuid4().hex[:8].upper()}"
        if unit_number is None:
            unit_number = code

        db_unit = DBUnits(
            uuid=str(uuid.uuid4()),
            building_id=building_id,
            unit_type_id=unit_type_id,
            unit_number=unit_number,
            code=code,
            name=name or f"Unit {unit_number}",
            description=kwargs.get("description", "Factory-created test unit"),
            private_area=private_area or Decimal("75.0000"),
            coefficient=coefficient or Decimal("5.500000"),
            floor_number=floor_number if floor_number is not None else 1,
            floor_label=floor_label or f"Floor {floor_number or 1}",
            occupancy_status=occupancy_status,
            sort_order=sort_order if sort_order is not None else 10,
            updated_at=kwargs.get("updated_at", func.now()),
            status=status,
        )
        session.add(db_unit)
        session.flush()
        session.refresh(db_unit)
        return db_unit
