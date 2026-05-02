"""
Scenario Builder — creates complete test data graphs.

Each scenario method returns a dict with all created entities/IDs,
which is then registered in DataRegistry for cleanup/debugging.

Usage:
    scenario = create_full_condo_scenario(session, condo_name="Las Lomas")
    # scenario = {
    #     "condo": DBCondominiums,
    #     "buildings": [DBBuildings, ...],
    #     "units": [DBUnits, ...],
    #     "users": [DBUser, ...],
    #     "residents": [DBResidentProfile, ...],
    # }
"""
import uuid as uuid_module
from typing import Optional
from decimal import Decimal

from tests.factories.condo_factory import CondoFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.unit_factory import UnitFactory
from tests.factories.user_factory import UserFactory
from tests.factories.resident_factory import ResidentFactory


def create_full_condo_scenario(
    session,
    condo_name: str = "Test Condo Scenario",
    buildings_count: int = 2,
    units_per_building: int = 3,
    residents_per_unit: int = 1,
) -> dict:
    """
    Create a full scenario: condo + buildings + units + users + residents.

    Args:
        session: SQLAlchemy session
        condo_name: name for the condominium
        buildings_count: number of buildings to create
        units_per_building: units per building
        residents_per_unit: how many user+resident pairs to create per unit

    Returns:
        dict with keys: condo, buildings, units, users, residents
    """
    # 1. Condo
    condo = CondoFactory.create(session, name=condo_name)

    # 2. Buildings
    buildings = []
    for i in range(buildings_count):
        building = BuildingFactory.create(
            session,
            condominium_id=condo.id,
            code=f"BLD-{chr(65+i)}",  # BLD-A, BLD-B, ...
            name=f"Torre {chr(65+i)}",
            short_name=f"Torre {chr(65+i)}",
            floors_count=10,
            units_planned=units_per_building,
        )
        buildings.append(building)

    # 3. Units
    units = []
    for bldg in buildings:
        for u in range(units_per_building):
            unit = UnitFactory.create(
                session,
                building_id=bldg.id,
                unit_number=f"{(u+1):03d}",  # 001, 002, 003
                code=f"UNIT-{bldg.code}-{u+1:02d}",
                name=f"Unidad {u+1}",
                floor_number=(u % 10) + 1,
                occupancy_status="occupied",
            )
            units.append(unit)

    # 4. Users + Residents (email uses unit.id + uuid to avoid unique constraint violations)
    users = []
    residents = []
    for unit in units:
        for r in range(residents_per_unit):
            uid = uuid_module.uuid4().hex[:8]
            user = UserFactory.create(
                session,
                email=f"resident-{unit.id}-{r}@{uid}.test.local",
            )
            resident = ResidentFactory.create(
                session,
                user_id=user.id,
                condominium_id=condo.id,
            )
            users.append(user)
            residents.append(resident)

    return {
        "condo": condo,
        "buildings": buildings,
        "units": units,
        "users": users,
        "residents": residents,
    }


def create_condo_with_buildings(
    session,
    condo_name: str = "Condo Only",
    buildings_count: int = 1,
) -> dict:
    """Condo + buildings (no units or residents)."""
    condo = CondoFactory.create(session, name=condo_name)
    buildings = []
    for i in range(buildings_count):
        building = BuildingFactory.create(
            session,
            condominium_id=condo.id,
            code=f"BLD-{chr(65+i)}",
            name=f"Torre {chr(65+i)}",
        )
        buildings.append(building)
    return {"condo": condo, "buildings": buildings}


def create_condo_with_1_building_3_units(session, condo_name: str = "Minimal Condo") -> dict:
    """Minimal useful scenario: 1 condo + 1 building + 3 units."""
    condo = CondoFactory.create(session, name=condo_name)
    building = BuildingFactory.create(
        session,
        condominium_id=condo.id,
        code="BLD-A",
        name="Torre Unica",
    )
    units = []
    for u in range(1, 4):
        unit = UnitFactory.create(
            session,
            building_id=building.id,
            unit_number=f"{u:03d}",
            code=f"UNIT-BLDA-{u:02d}",
            floor_number=u,
            occupancy_status="occupied",
        )
        units.append(unit)
    return {"condo": condo, "buildings": [building], "units": units}
