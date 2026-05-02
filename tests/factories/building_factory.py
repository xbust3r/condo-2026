"""
Factory: BuildingEntity.

Creates test building records directly in the DB via SQLAlchemy,
bypassing the session_scope wrapper so tests control the session lifecycle.
"""
import uuid
from decimal import Decimal
from sqlalchemy.orm import Session

from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings


class BuildingFactory:
    """Factory for creating test Building records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        code: str = None,
        name: str = None,
        short_name: str = None,
        description: str = None,
        building_type_id: int = None,
        built_area: Decimal = None,
        common_area: Decimal = None,
        coefficient: Decimal = None,
        floors_count: int = None,
        basements_count: int = None,
        units_planned: int = None,
        sort_order: int = None,
        status: int = 1,
        **kwargs,
    ) -> DBBuildings:
        """
        Create and persist a Building record.

        Usage:
            building = BuildingFactory.create(
                session,
                condominium_id=condo.id,
                code="BLD-A",
                name="Torre A"
            )
        """
        if code is None:
            code = f"BLD-{uuid.uuid4().hex[:8].upper()}"

        db_building = DBBuildings(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            code=code,
            name=name or "Test Building",
            short_name=short_name or code,
            description=description or "Factory-created test building",
            building_type_id=building_type_id,
            built_area=built_area or Decimal("1500.0000"),
            common_area=common_area or Decimal("350.0000"),
            coefficient=coefficient or Decimal("25.500000"),
            floors_count=floors_count if floors_count is not None else 10,
            basements_count=basements_count if basements_count is not None else 2,
            units_planned=units_planned if units_planned is not None else 20,
            sort_order=sort_order if sort_order is not None else 1,
            status=status,
        )
        session.add(db_building)
        session.flush()
        session.refresh(db_building)
        return db_building
