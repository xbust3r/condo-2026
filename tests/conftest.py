"""
Pytest configuration and shared fixtures.
Covers: core_buildings, core_unitys
"""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock, patch
from datetime import datetime

# Mock session_scope before importing modules that use it
_mock_session = MagicMock()
_mock_session.__enter__ = MagicMock(return_value=_mock_session)
_mock_session.__exit__ = MagicMock(return_value=False)


@pytest.fixture(autouse=True)
def mock_session_scope():
    """Auto-apply session_scope mock to all tests."""
    with patch("library.dddpy.shared.mysql.session_manager.session_scope") as mock:
        mock.return_value = _mock_session
        yield mock


@pytest.fixture
def sample_building_data():
    """Sample data for creating a building."""
    from library.dddpy.core_buildings.domain.building_data import CreateBuildingData
    return CreateBuildingData(
        condominium_id=1,
        code="BLD-A",
        name="Torre A",
        short_name="Torre A",
        description="Edificio principal",
        building_type_id=1,
        built_area=Decimal("1500.0000"),
        common_area=Decimal("350.0000"),
        coefficient=Decimal("25.500000"),
        floors_count=10,
        basements_count=2,
        units_planned=20,
        sort_order=1,
    )


@pytest.fixture
def sample_update_building_data():
    """Sample data for updating a building."""
    from library.dddpy.core_buildings.domain.building_data import UpdateBuildingData
    return UpdateBuildingData(
        name="Torre A - Renovada",
        short_name="Torre A",
        floors_count=12,
        status=1,
    )


@pytest.fixture
def sample_building_entity():
    """Sample building entity for tests."""
    from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
    return BuildingEntity(
        id=1,
        uuid="test-uuid-1234",
        condominium_id=1,
        code="BLD-A",
        name="Torre A",
        short_name="Torre A",
        description="Edificio principal",
        building_type_id=1,
        built_area=Decimal("1500.0000"),
        common_area=Decimal("350.0000"),
        coefficient=Decimal("25.500000"),
        floors_count=10,
        basements_count=2,
        units_planned=20,
        sort_order=1,
        status=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted_at=None,
    )


@pytest.fixture
def mock_building_cmd_repository():
    """Mock BuildingCmdRepository implementation."""
    from library.dddpy.core_buildings.infrastructure.building_cmd_repository import BuildingCmdRepositoryImpl
    return BuildingCmdRepositoryImpl()


@pytest.fixture
def mock_building_query_repository():
    """Mock BuildingQueryRepository implementation."""
    from library.dddpy.core_buildings.infrastructure.building_query_repository import BuildingQueryRepositoryImpl
    return BuildingQueryRepositoryImpl()


# ─── core_unitys fixtures ────────────────────────────────────────────────────


@pytest.fixture
def sample_unity_data():
    """Sample data for creating a unity."""
    from library.dddpy.core_unitys.domain.unity_data import CreateUnityData
    return CreateUnityData(
        building_id=1,
        unit_number="101",
        unity_type_id=1,
        code="UNIT-101",
        name="Apartamento 101",
        description="Apartamento de 3 habitaciones",
        private_area=Decimal("75.0000"),
        coefficient=Decimal("5.500000"),
        floor_number=1,
        floor_label="Piso 1",
        occupancy_status="occupied",
        sort_order=10,
    )


@pytest.fixture
def sample_update_unity_data():
    """Sample data for updating a unity."""
    from library.dddpy.core_unitys.domain.unity_data import UpdateUnityData
    return UpdateUnityData(
        name="Apartamento 101 - Renovado",
        occupancy_status="occupied",
        private_area=Decimal("80.0000"),
        coefficient=Decimal("6.000000"),
        sort_order=15,
        status=1,
    )


@pytest.fixture
def sample_unity_entity():
    """Sample unity entity for tests."""
    from library.dddpy.core_unitys.domain.unity_entity import UnityEntity
    return UnityEntity(
        id=1,
        uuid="test-uuid-unity",
        building_id=1,
        unity_type_id=1,
        unit_number="101",
        code="UNIT-101",
        name="Apartamento 101",
        description="Apartamento de 3 habitaciones",
        private_area=Decimal("75.0000"),
        coefficient=Decimal("5.500000"),
        floor_number=1,
        floor_label="Piso 1",
        occupancy_status="vacant",
        sort_order=0,
        status=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted_at=None,
    )