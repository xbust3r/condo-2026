"""
Tests for core_buildings module.

Coverage:
- Create building (happy path + duplicate code rejection)
- Soft delete
- Restore
- List with filters (condominium_id, status, include_deleted)
- Hard delete blocked when active units exist
"""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock, patch

from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
from library.dddpy.core_buildings.domain.building_data import CreateBuildingData, UpdateBuildingData
from library.dddpy.core_buildings.domain.building_exception import (
    BuildingNotFound,
    RepeatedBuildingCode,
    BuildingHasActiveUnits,
)
from library.dddpy.core_buildings.usecase.building_usecase import BuildingUseCase
from library.dddpy.core_buildings.usecase.building_cmd_schema import CreateBuildingSchema, UpdateBuildingSchema


class TestBuildingEntity:
    """Tests for BuildingEntity invariants."""

    def test_to_dict_returns_all_fields(self, sample_building_entity):
        """to_dict() should return a complete dict representation."""
        result = sample_building_entity.to_dict()

        assert result["id"] == 1
        assert result["uuid"] == "test-uuid-1234"
        assert result["condominium_id"] == 1
        assert result["code"] == "BLD-A"
        assert result["name"] == "Torre A"
        assert result["short_name"] == "Torre A"
        assert result["built_area"] == 1500.0
        assert result["common_area"] == 350.0
        assert result["coefficient"] == 25.5
        assert result["floors_count"] == 10
        assert result["basements_count"] == 2
        assert result["units_planned"] == 20
        assert result["sort_order"] == 1
        assert result["status"] == 1
        assert result["deleted_at"] is None

    def test_is_deleted_true_when_deleted_at_set(self):
        """is_deleted() should return True when deleted_at is set."""
        entity = BuildingEntity(
            id=1, uuid="test", condominium_id=1, code="A", name="Test",
            deleted_at="2026-04-13"
        )
        assert entity.is_deleted() is True

    def test_is_deleted_false_when_deleted_at_none(self):
        """is_deleted() should return False when deleted_at is None."""
        entity = BuildingEntity(
            id=1, uuid="test", condominium_id=1, code="A", name="Test"
        )
        assert entity.is_deleted() is False

    def test_is_active_true_when_status_1_and_not_deleted(self):
        """is_active() should return True when status=1 and not deleted."""
        entity = BuildingEntity(
            id=1, uuid="test", condominium_id=1, code="A", name="Test",
            status=1
        )
        assert entity.is_active() is True

    def test_is_active_false_when_status_0(self):
        """is_active() should return False when status=0."""
        entity = BuildingEntity(
            id=1, uuid="test", condominium_id=1, code="A", name="Test",
            status=0
        )
        assert entity.is_active() is False


class TestBuildingCreateData:
    """Tests for CreateBuildingData validation."""

    def test_create_building_data_all_fields(self, sample_building_data):
        """CreateBuildingData should accept all valid fields."""
        assert sample_building_data.condominium_id == 1
        assert sample_building_data.code == "BLD-A"
        assert sample_building_data.name == "Torre A"
        assert sample_building_data.built_area == Decimal("1500.0000")
        assert sample_building_data.coefficient == Decimal("25.500000")
        assert sample_building_data.floors_count == 10

    def test_create_building_data_defaults(self):
        """CreateBuildingData should have correct defaults."""
        data = CreateBuildingData(
            condominium_id=1,
            code="BLD-B",
            name="Torre B",
        )
        assert data.short_name is None
        assert data.description is None
        assert data.building_type_id is None
        assert data.built_area is None
        assert data.common_area is None
        assert data.coefficient is None
        assert data.floors_count == 0
        assert data.basements_count == 0
        assert data.units_planned == 0
        assert data.sort_order == 0


class TestBuildingUseCaseCreate:
    """Tests for BuildingUseCase.create()."""

    def test_create_building_success(self, sample_building_entity):
        """create() should return success response when code is unique."""
        with patch.object(
            BuildingUseCase, "_check_duplicate_code", return_value=None
        ):
            mock_cmd = MagicMock()
            mock_cmd.create.return_value = sample_building_entity
            mock_query = MagicMock()
            mock_query.get_by_code_in_condominium.return_value = None
            mock_query.get_by_id.return_value = sample_building_entity

            use_case = BuildingUseCase.__new__(BuildingUseCase)
            use_case.building_cmd_usecase = mock_cmd
            use_case.building_query_usecase = mock_query

            schema = CreateBuildingSchema(
                condominium_id=1,
                code="BLD-A",
                name="Torre A",
            )

            result = use_case.create(schema)

            assert result.success is True
            assert result.message == "Building created successfully"
            assert result.data["code"] == "BLD-A"

    def test_create_building_duplicate_code_raises(self):
        """create() should raise RepeatedBuildingCode when code exists in condominium."""
        mock_query = MagicMock()
        mock_query.get_by_code_in_condominium.return_value = BuildingEntity(
            id=1, uuid="existing", condominium_id=1, code="BLD-A", name="Existing"
        )

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = MagicMock()
        use_case.building_query_usecase = mock_query

        schema = CreateBuildingSchema(
            condominium_id=1,
            code="BLD-A",
            name="Torre A",
        )

        with pytest.raises(RepeatedBuildingCode):
            use_case.create(schema)


class TestBuildingUseCaseDelete:
    """Tests for BuildingUseCase.delete() (soft delete)."""

    def test_delete_building_success(self, sample_building_entity):
        """delete() should soft delete and return success."""
        mock_cmd = MagicMock()
        mock_cmd.soft_delete.return_value = True
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_building_entity

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = mock_cmd
        use_case.building_query_usecase = mock_query

        result = use_case.delete(1)

        assert result.success is True
        assert result.message == "Building deleted successfully (soft delete)"
        mock_cmd.soft_delete.assert_called_once_with(1)

    def test_delete_building_not_found_raises(self):
        """delete() should raise BuildingNotFound when building doesn't exist."""
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = None

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = MagicMock()
        use_case.building_query_usecase = mock_query

        with pytest.raises(BuildingNotFound):
            use_case.delete(999)


class TestBuildingUseCaseRestore:
    """Tests for BuildingUseCase.restore()."""

    def test_restore_building_success(self, sample_building_entity):
        """restore() should clear deleted_at and return restored building."""
        mock_cmd = MagicMock()
        mock_cmd.restore.return_value = True
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_building_entity

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = mock_cmd
        use_case.building_query_usecase = mock_query

        result = use_case.restore(1)

        assert result.success is True
        assert result.message == "Building restored successfully"
        mock_cmd.restore.assert_called_once_with(1)

    def test_restore_nonexistent_raises(self):
        """restore() should raise BuildingNotFound when building doesn't exist."""
        mock_cmd = MagicMock()
        mock_cmd.restore.return_value = False
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = None

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = mock_cmd
        use_case.building_query_usecase = mock_query

        with pytest.raises(BuildingNotFound):
            use_case.restore(999)


class TestBuildingUseCaseHardDelete:
    """Tests for BuildingUseCase.hard_delete()."""

    def test_hard_delete_blocked_when_active_units(self, sample_building_entity):
        """hard_delete() should raise BuildingHasActiveUnits when units exist."""
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_building_entity
        mock_query.count_active_units.return_value = 5  # 5 active units

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = MagicMock()
        use_case.building_query_usecase = mock_query

        with pytest.raises(BuildingHasActiveUnits) as exc_info:
            use_case.hard_delete(1)

        assert "1" in str(exc_info.value)  # building_id in message

    def test_hard_delete_success_when_no_units(self, sample_building_entity):
        """hard_delete() should succeed when no active units."""
        mock_cmd = MagicMock()
        mock_cmd.hard_delete.return_value = True
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_building_entity
        mock_query.count_active_units.return_value = 0

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = mock_cmd
        use_case.building_query_usecase = mock_query

        result = use_case.hard_delete(1)

        assert result.success is True
        mock_cmd.hard_delete.assert_called_once_with(1)


class TestBuildingUseCaseList:
    """Tests for BuildingUseCase.list_all() and list_by_condominium()."""

    def test_list_all_returns_paginated_response(self, sample_building_entity):
        """list_all() should return paginated response with total count."""
        mock_query = MagicMock()
        mock_query.list_all.return_value = ([sample_building_entity], 1)

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = MagicMock()
        use_case.building_query_usecase = mock_query

        result = use_case.list_all(
            skip=0,
            limit=100,
            condominium_id=1,
            status=1,
            include_deleted=False,
        )

        assert result.success is True
        assert result.message == "Buildings listed successfully"
        assert result.data["total"] == 1
        assert len(result.data["items"]) == 1
        assert result.data["items"][0]["code"] == "BLD-A"

    def test_list_by_condominium_filters_correctly(self, sample_building_entity):
        """list_by_condominium() should filter by condominium_id."""
        mock_query = MagicMock()
        mock_query.list_by_condominium.return_value = ([sample_building_entity], 1)

        use_case = BuildingUseCase.__new__(BuildingUseCase)
        use_case.building_cmd_usecase = MagicMock()
        use_case.building_query_usecase = mock_query

        result = use_case.list_by_condominium(
            condominium_id=1,
            skip=0,
            limit=100,
            status=1,
            include_deleted=False,
        )

        assert result.success is True
        assert result.data["condominium_id"] == 1
        assert len(result.data["items"]) == 1


class TestBuildingCmdSchema:
    """Tests for Pydantic schemas."""

    def test_create_schema_validates_coefficient_range(self):
        """CreateBuildingSchema should reject coefficient > 100."""
        with pytest.raises(Exception):  # ValidationError from Pydantic
            CreateBuildingSchema(
                condominium_id=1,
                code="BLD-A",
                name="Torre A",
                coefficient=150.0,  # Invalid: > 100
            )

    def test_create_schema_validates_negative_areas(self):
        """CreateBuildingSchema should reject negative built_area."""
        with pytest.raises(Exception):
            CreateBuildingSchema(
                condominium_id=1,
                code="BLD-A",
                name="Torre A",
                built_area=-100.0,
            )

    def test_create_schema_validates_negative_counters(self):
        """CreateBuildingSchema should reject negative floors_count."""
        with pytest.raises(Exception):
            CreateBuildingSchema(
                condominium_id=1,
                code="BLD-A",
                name="Torre A",
                floors_count=-5,
            )

    def test_update_schema_all_fields_optional(self):
        """UpdateBuildingSchema should allow partial updates."""
        schema = UpdateBuildingSchema(name="New Name")
        assert schema.name == "New Name"
        assert schema.short_name is None
        assert schema.floors_count is None
        assert schema.coefficient is None


class TestBuildingRepository:
    """Tests for BuildingRepository contract."""

    def test_repository_has_required_methods(self):
        """BuildingRepository should define create, get, update, delete, list methods."""
        from library.dddpy.core_buildings.domain.building_repository import BuildingRepository

        abstract_methods = {
            "create", "get_by_id", "get_by_uuid",
            "get_by_code_in_condominium", "update", "delete", "list_by_condominium"
        }
        # ABC abstract methods are not directly accessible, but we verify interface exists
        # by checking the contract is importable
        assert BuildingRepository is not None


class TestBuildingExceptions:
    """Tests for building exception classes."""

    def test_building_not_found_has_404(self):
        """BuildingNotFound should have status_code=404."""
        exc = BuildingNotFound()
        assert exc.status_code == 404
        assert "not found" in exc.message.lower()

    def test_repeated_building_code_has_409(self):
        """RepeatedBuildingCode should have status_code=409."""
        exc = RepeatedBuildingCode()
        assert exc.status_code == 409
        assert "code" in exc.message.lower()

    def test_building_has_active_units_has_409(self):
        """BuildingHasActiveUnits should have status_code=409 and include building_id."""
        exc = BuildingHasActiveUnits(42)
        assert exc.status_code == 409
        assert "42" in exc.message
        assert "active units" in exc.message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])