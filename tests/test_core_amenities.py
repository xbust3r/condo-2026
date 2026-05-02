"""
Tests for core_amenities module.

Coverage:
- Entity: scope/building_id invariants, to_dict, scope_label, validate_scope_consistency
- Schema: CreateAmenitySchema / UpdateAmenitySchema scope validation
- UseCase: create both scopes, reject invalid combos, list with building_id filter
- Semantics: building view sees CONDOMINIUM + its own BUILDING, not other buildings'
- Backward compatibility: existing create flow (no scope) defaults to CONDOMINIUM
"""
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from library.dddpy.core_amenities.domain.amenity_entity import AmenityEntity
from library.dddpy.core_amenities.domain.amenity_exception import (
    AmenityNotFound,
    AmenityValidationError,
)
from library.dddpy.core_amenities.usecase.amenity_cmd_schema import (
    CreateAmenitySchema,
    UpdateAmenitySchema,
)
from library.dddpy.core_amenities.usecase.amenity_usecase import AmenityUseCase


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def condo_amenity_entity():
    """Sample CONDOMINIUM-scope amenity."""
    return AmenityEntity(
        id=1,
        uuid="amenity-condo-001",
        condominium_id=1,
        name="Piscina General",
        description="Piscina pública del condominio",
        location="Zona central",
        max_capacity=50,
        booking_duration_min=120,
        requires_approval=False,
        scope="CONDOMINIUM",
        building_id=None,
        status="active",
        created_at=datetime(2026, 1, 1),
        condominium_name="Condominio Test",
    )


@pytest.fixture
def building_amenity_entity():
    """Sample BUILDING-scope amenity."""
    return AmenityEntity(
        id=2,
        uuid="amenity-building-001",
        condominium_id=1,
        name="Gimnasio Torre A",
        description="Gimnasio exclusivo Torre A",
        location="Piso 1",
        max_capacity=15,
        booking_duration_min=60,
        requires_approval=False,
        scope="BUILDING",
        building_id=1,
        status="active",
        created_at=datetime(2026, 1, 1),
        condominium_name="Condominio Test",
        building_name="Torre A",
    )


@pytest.fixture
def mock_session():
    """Mock session_scope at the shared module level so all internal calls use it."""
    with patch(
        "library.dddpy.shared.mysql.session_manager.session_scope"
    ) as mock:
        mock_session = MagicMock()
        mock.return_value.__enter__.return_value = mock_session
        mock.return_value.__exit__.return_value = False
        yield mock_session


def _setup_mock_building(mock_session, building_id, condominium_id):
    """Configure a mock session to return a building with the given ids."""
    mock_building = MagicMock()
    mock_building.id = building_id
    mock_building.condominium_id = condominium_id
    # Need to mock the chain: session.query(DBBuildings).filter(...).first()
    mock_filter = MagicMock()
    mock_filter.first.return_value = mock_building
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_session.query.return_value = mock_query
    return mock_building


# ---------------------------------------------------------------------------
# AmenityEntity tests
# ---------------------------------------------------------------------------

class TestAmenityEntity:

    def test_condo_amenity_scope_properties(self, condo_amenity_entity):
        """CONDOMINIUM scope should report correct properties."""
        assert condo_amenity_entity.is_condominium_scope is True
        assert condo_amenity_entity.is_building_scope is False
        assert condo_amenity_entity.scope_label == "General"

    def test_building_amenity_scope_properties(self, building_amenity_entity):
        """BUILDING scope should report correct properties."""
        assert building_amenity_entity.is_condominium_scope is False
        assert building_amenity_entity.is_building_scope is True
        assert building_amenity_entity.scope_label == "Exclusiva edificio"

    def test_validate_scope_consistency_condo_without_building(self):
        """CONDOMINIUM + building_id=None should pass validation."""
        entity = AmenityEntity(
            id=0, uuid="test", condominium_id=1, name="Test",
            scope="CONDOMINIUM", building_id=None,
        )
        entity.validate_scope_consistency()  # should not raise

    def test_validate_scope_consistency_condo_with_building_raises(self):
        """CONDOMINIUM + building_id set should raise ValueError."""
        entity = AmenityEntity(
            id=0, uuid="test", condominium_id=1, name="Test",
            scope="CONDOMINIUM", building_id=1,
        )
        with pytest.raises(ValueError, match="building_id=None"):
            entity.validate_scope_consistency()

    def test_validate_scope_consistency_building_with_id(self):
        """BUILDING + building_id set should pass validation."""
        entity = AmenityEntity(
            id=0, uuid="test", condominium_id=1, name="Test",
            scope="BUILDING", building_id=1,
        )
        entity.validate_scope_consistency()  # should not raise

    def test_validate_scope_consistency_building_without_id_raises(self):
        """BUILDING + building_id=None should raise ValueError."""
        entity = AmenityEntity(
            id=0, uuid="test", condominium_id=1, name="Test",
            scope="BUILDING", building_id=None,
        )
        with pytest.raises(ValueError, match="requires a building_id"):
            entity.validate_scope_consistency()

    def test_to_dict_condo_amenity(self, condo_amenity_entity):
        """to_dict should include scope, building_id, scope_label."""
        d = condo_amenity_entity.to_dict()
        assert d["scope"] == "CONDOMINIUM"
        assert d["building_id"] is None
        assert d["scope_label"] == "General"
        assert d["condominium_name"] == "Condominio Test"
        assert d["building_name"] is None

    def test_to_dict_building_amenity(self, building_amenity_entity):
        """to_dict should include building_name for BUILDING scope."""
        d = building_amenity_entity.to_dict()
        assert d["scope"] == "BUILDING"
        assert d["building_id"] == 1
        assert d["scope_label"] == "Exclusiva edificio"
        assert d["building_name"] == "Torre A"


# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------

class TestCreateAmenitySchema:

    def test_default_scope_is_condominium(self):
        """Default scope should be CONDOMINIUM (backward compatible)."""
        schema = CreateAmenitySchema(
            condominium_id=1,
            name="Test Amenity",
        )
        assert schema.scope == "CONDOMINIUM"
        assert schema.building_id is None

    def test_condo_scope_rejects_building_id(self):
        """scope=CONDOMINIUM should reject building_id."""
        with pytest.raises(ValueError, match="building_id=None"):
            CreateAmenitySchema(
                condominium_id=1,
                name="Test",
                scope="CONDOMINIUM",
                building_id=1,
            )

    def test_building_scope_requires_building_id(self):
        """scope=BUILDING should require building_id."""
        with pytest.raises(ValueError, match="requires building_id"):
            CreateAmenitySchema(
                condominium_id=1,
                name="Test",
                scope="BUILDING",
                building_id=None,
            )

    def test_building_scope_with_building_id_passes(self):
        """scope=BUILDING + building_id should pass."""
        schema = CreateAmenitySchema(
            condominium_id=1,
            name="Gimnasio Torre A",
            scope="BUILDING",
            building_id=1,
        )
        assert schema.scope == "BUILDING"
        assert schema.building_id == 1

    def test_invalid_scope_rejected(self):
        """Invalid scope value should be rejected."""
        with pytest.raises(ValueError, match="CONDOMINIUM or BUILDING"):
            CreateAmenitySchema(
                condominium_id=1,
                name="Test",
                scope="INVALID",
            )

    def test_backward_compat_no_scope_given(self):
        """Omitting scope should default to CONDOMINIUM (existing API compat)."""
        schema = CreateAmenitySchema(condominium_id=1, name="Legacy Amenity")
        assert schema.scope == "CONDOMINIUM"
        assert schema.building_id is None


class TestUpdateAmenitySchema:

    def test_partial_update_no_scope_provided(self):
        """Update without scope should be valid (partial)."""
        schema = UpdateAmenitySchema(name="New Name")
        assert schema.name == "New Name"
        assert schema.scope is None

    def test_update_condo_scope_rejects_building_id(self):
        """Setting scope=CONDOMINIUM with building_id=1 should fail."""
        with pytest.raises(ValueError, match="building_id=None"):
            UpdateAmenitySchema(scope="CONDOMINIUM", building_id=1)

    def test_update_building_scope_requires_building_id(self):
        """Setting scope=BUILDING without building_id should fail."""
        with pytest.raises(ValueError, match="requires building_id"):
            UpdateAmenitySchema(scope="BUILDING")


# ---------------------------------------------------------------------------
# AmenityUseCase tests (with mocked repositories)
# ---------------------------------------------------------------------------

class TestAmenityUseCaseCreate:

    def test_create_condominium_amenity(self, mock_session):
        """Creating a CONDOMINIUM amenity should succeed."""
        mock_session.add = MagicMock()
        mock_session.flush = MagicMock()
        mock_session.refresh = MagicMock()

        usecase = AmenityUseCase()
        with patch.object(usecase._cmd_repo, "create", return_value=1):
            response = usecase.create(
                condominium_id=1,
                name="Piscina General",
                scope="CONDOMINIUM",
                building_id=None,
            )

        assert response.success is True
        assert response.data["scope"] == "CONDOMINIUM"
        assert response.data["building_id"] is None
        assert response.data["scope_label"] == "General"

    def test_create_building_amenity(self, mock_session):
        """Creating a BUILDING amenity with valid building should succeed."""
        mock_session.add = MagicMock()
        mock_session.flush = MagicMock()
        mock_session.refresh = MagicMock()

        # Setup mock so building validation in usecase resolves correctly
        _setup_mock_building(mock_session, building_id=1, condominium_id=1)

        usecase = AmenityUseCase()
        with patch.object(usecase._cmd_repo, "create", return_value=2):
            response = usecase.create(
                condominium_id=1,
                name="Gimnasio Torre A",
                scope="BUILDING",
                building_id=1,
            )

        assert response.success is True
        assert response.data["scope"] == "BUILDING"
        assert response.data["building_id"] == 1
        assert response.data["scope_label"] == "Exclusiva edificio"

    def test_create_building_scope_rejects_null_building_id(self):
        """scope=BUILDING without building_id should raise AmenityValidationError."""
        usecase = AmenityUseCase()
        with pytest.raises(AmenityValidationError, match="requires building_id"):
            usecase.create(
                condominium_id=1,
                name="Bad Amenity",
                scope="BUILDING",
                building_id=None,
            )

    def test_create_condo_scope_rejects_building_id(self):
        """scope=CONDOMINIUM with building_id should raise AmenityValidationError."""
        usecase = AmenityUseCase()
        with pytest.raises(AmenityValidationError, match="building_id=None"):
            usecase.create(
                condominium_id=1,
                name="Bad Amenity",
                scope="CONDOMINIUM",
                building_id=5,
            )

    def test_create_building_not_belonging_to_condo(self, mock_session):
        """Building from a different condominium should be rejected."""
        # Mock building that belongs to condominium 2 (not 1)
        _setup_mock_building(mock_session, building_id=5, condominium_id=2)

        usecase = AmenityUseCase()
        with pytest.raises(AmenityValidationError, match="does not belong"):
            usecase.create(
                condominium_id=1,
                name="Cross-Condo Amenity",
                scope="BUILDING",
                building_id=5,
            )

    def test_create_building_not_found(self, mock_session):
        """Non-existent building_id should be rejected."""
        # Mock query returning None for building
        mock_filter = MagicMock()
        mock_filter.first.return_value = None
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query

        usecase = AmenityUseCase()
        with pytest.raises(AmenityValidationError, match="not found"):
            usecase.create(
                condominium_id=1,
                name="Ghost Building",
                scope="BUILDING",
                building_id=9999,
            )

    def test_create_invalid_scope(self):
        """Invalid scope should raise AmenityValidationError."""
        usecase = AmenityUseCase()
        with pytest.raises(AmenityValidationError, match="Invalid scope"):
            usecase.create(
                condominium_id=1,
                name="Bad",
                scope="UNIT",
            )


class TestAmenityUseCaseList:

    def test_list_condominium_only_returns_condo_scope(self):
        """Listing by condominium_id alone should return CONDOMINIUM scope only."""
        condo_entity = AmenityEntity(
            id=1, uuid="a", condominium_id=1, name="Piscina",
            scope="CONDOMINIUM", building_id=None, status="active",
        )
        usecase = AmenityUseCase()
        with patch.object(usecase._query_repo, "list_all", return_value=([condo_entity], 1)):
            response = usecase.list_all(condominium_id=1)
            assert response.success is True
            assert len(response.data) == 1
            assert response.data[0]["scope"] == "CONDOMINIUM"
            assert response.data[0]["building_id"] is None

    def test_list_with_building_sees_condo_plus_building(self):
        """Listing with building_id should return CONDOMINIUM + BUILDING amenities."""
        entities = [
            AmenityEntity(
                id=1, uuid="a", condominium_id=1, name="Piscina",
                scope="CONDOMINIUM", building_id=None, status="active",
            ),
            AmenityEntity(
                id=2, uuid="b", condominium_id=1, name="Gimnasio A",
                scope="BUILDING", building_id=1, status="active",
            ),
        ]
        usecase = AmenityUseCase()
        with patch.object(usecase._query_repo, "list_all", return_value=(entities, 2)):
            response = usecase.list_all(condominium_id=1, building_id=1)
            assert response.success is True
            assert len(response.data) == 2
            scopes = {item["scope"] for item in response.data}
            assert scopes == {"CONDOMINIUM", "BUILDING"}

    def test_list_active_with_building(self):
        """list_active with building_id should pass building_id to repo."""
        usecase = AmenityUseCase()
        with patch.object(usecase._query_repo, "list_active", return_value=([], 0)) as mock_list:
            usecase.list_active(condominium_id=1, building_id=1)
            mock_list.assert_called_once_with(
                condominium_id=1, building_id=1, skip=0, limit=100,
            )

    def test_list_condominium_sees_only_condo_scope(self):
        """Condominium view (no building_id) should ONLY see CONDOMINIUM scope."""
        condo_a = AmenityEntity(
            id=1, uuid="a", condominium_id=1, name="Piscina",
            scope="CONDOMINIUM", building_id=None, status="active",
        )
        usecase = AmenityUseCase()
        with patch.object(usecase._query_repo, "list_all", return_value=([condo_a], 1)):
            response = usecase.list_all(condominium_id=1)
            scopes = {item["scope"] for item in response.data}
            # Should NOT contain any BUILDING scope amenities
            assert "BUILDING" not in scopes
            assert scopes == {"CONDOMINIUM"}


# ---------------------------------------------------------------------------
# Backward compatibility tests
# ---------------------------------------------------------------------------

class TestBackwardCompatibility:

    def test_entity_default_scope_is_condominium(self):
        """New entity without explicit scope should default to CONDOMINIUM."""
        entity = AmenityEntity(
            id=0, uuid="test", condominium_id=1, name="Legacy",
        )
        assert entity.scope == "CONDOMINIUM"
        assert entity.building_id is None

    def test_create_schema_default_scope_is_condominium(self):
        """CreateSchema without scope should default to CONDOMINIUM."""
        schema = CreateAmenitySchema(condominium_id=1, name="Legacy")
        assert schema.scope == "CONDOMINIUM"
        assert schema.building_id is None

    def test_to_dict_includes_new_fields(self, condo_amenity_entity):
        """Existing to_dict consumers get scope + scope_label in response."""
        d = condo_amenity_entity.to_dict()
        assert "scope" in d
        assert "building_id" in d
        assert "scope_label" in d
        assert "building_name" in d
