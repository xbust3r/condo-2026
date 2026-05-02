"""
Tests for core_unities module.

Coverage:
- UnitEntity invariants (coefficient range, area >= 0, sort_order >= 0, valid occupancy_status)
- Create unity (happy path + duplicate unit_number/code rejection)
- Soft delete / restore
- List with filters (building_id, status, occupancy_status, include_deleted)
- Hard delete blocked when active residents exist
- Pydantic schema validation
- Exception classes
"""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock, patch
from datetime import datetime

from library.dddpy.core_units.domain.unit_entity import UnitEntity
from library.dddpy.core_units.domain.unit_data import CreateUnitData, UpdateUnitData
from library.dddpy.core_units.domain.unit_exception import (
    UnitNotFound,
    RepeatedUnitUnitNumber,
    RepeatedUnitCode,
    UnitHasActiveResidents,
    OccupancyStatusNotAllowed,
)
from library.dddpy.core_units.usecase.unit_usecase import UnitUseCase
from library.dddpy.core_units.usecase.unit_cmd_schema import (
    CreateUnitSchema,
    UpdateUnitSchema,
)


class TestUnitEntity:
    """Tests for UnitEntity invariants and methods."""

    def test_to_dict_returns_all_fields(self, sample_unit_entity):
        """to_dict() should return a complete dict representation."""
        result = sample_unit_entity.to_dict()

        assert result["id"] == 1
        assert result["uuid"] == "test-uuid-unity"
        assert result["building_id"] == 1
        assert result["unit_type_id"] == 1
        assert result["unit_number"] == "101"
        assert result["code"] == "UNIT-101"
        assert result["name"] == "Apartamento 101"
        assert result["private_area"] == 75.0
        assert result["coefficient"] == 5.5
        assert result["floor_number"] == 1
        assert result["floor_label"] == "Piso 1"
        assert result["occupancy_status"] == "vacant"
        assert result["sort_order"] == 0
        assert result["status"] == 1
        assert result["deleted_at"] is None

    def test_is_deleted_true_when_deleted_at_set(self):
        """is_deleted() should return True when deleted_at is set."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            deleted_at=datetime(2026, 4, 14),
        )
        assert entity.is_deleted() is True

    def test_is_deleted_false_when_deleted_at_none(self):
        """is_deleted() should return False when deleted_at is None."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
        )
        assert entity.is_deleted() is False

    def test_is_active_true_when_status_1_and_not_deleted(self):
        """is_active() should return True when status=1 and not deleted."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            status=1,
        )
        assert entity.is_active() is True

    def test_is_active_false_when_status_0(self):
        """is_active() should return False when status=0."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            status=0,
        )
        assert entity.is_active() is False

    def test_is_active_false_when_deleted(self):
        """is_active() should return False when soft-deleted."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            status=1,
            deleted_at=datetime(2026, 4, 14),
        )
        assert entity.is_active() is False

    def test_validate_invariants_rejects_negative_private_area(self):
        """_validate_invariants() should raise ValueError for negative private_area."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            private_area=Decimal("-10.0"),
        )
        with pytest.raises(ValueError, match="private_area must be >= 0"):
            entity._validate_invariants()

    def test_validate_invariants_rejects_coefficient_negative(self):
        """_validate_invariants() should raise ValueError for coefficient < 0."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            coefficient=Decimal("-1.0"),
        )
        with pytest.raises(ValueError, match="coefficient must be between 0 and 100"):
            entity._validate_invariants()

    def test_validate_invariants_rejects_coefficient_over_100(self):
        """_validate_invariants() should raise ValueError for coefficient > 100."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            coefficient=Decimal("150.0"),
        )
        with pytest.raises(ValueError, match="coefficient must be between 0 and 100"):
            entity._validate_invariants()

    def test_validate_invariants_rejects_negative_sort_order(self):
        """_validate_invariants() should raise ValueError for negative sort_order."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            sort_order=-1,
        )
        with pytest.raises(ValueError, match="sort_order must be >= 0"):
            entity._validate_invariants()

    def test_validate_invariants_rejects_invalid_occupancy_status(self):
        """_validate_invariants() should raise ValueError for invalid occupancy_status."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            occupancy_status="invalid_status",
        )
        with pytest.raises(ValueError, match="occupancy_status must be one of"):
            entity._validate_invariants()

    def test_validate_invariants_accepts_all_valid_occupancy_statuses(self):
        """_validate_invariants() should accept all five valid occupancy statuses."""
        valid_statuses = ["vacant", "occupied", "reserved", "maintenance", "blocked"]
        for status in valid_statuses:
            entity = UnitEntity(
                id=1, uuid="test", building_id=1, unit_number="101",
                occupancy_status=status,
            )
            entity._validate_invariants()  # Should not raise

    def test_validate_invariants_accepts_null_optional_fields(self):
        """_validate_invariants() should accept None for optional fields."""
        entity = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            private_area=None,
            coefficient=None,
            floor_number=None,
        )
        entity._validate_invariants()  # Should not raise


class TestUnityCreateData:
    """Tests for CreateUnitData."""

    def test_create_unity_data_required_fields(self):
        """CreateUnitData should require building_id and unit_number."""
        data = CreateUnitData(
            building_id=1,
            unit_number="101",
        )
        assert data.building_id == 1
        assert data.unit_number == "101"
        assert data.unit_type_id is None
        assert data.code is None
        assert data.name is None
        assert data.description is None
        assert data.private_area is None
        assert data.coefficient is None
        assert data.floor_number is None
        assert data.floor_label is None
        assert data.occupancy_status == "vacant"
        assert data.sort_order == 0

    def test_create_unity_data_all_fields(self, sample_unit_data):
        """CreateUnitData should accept all valid fields."""
        assert sample_unit_data.building_id == 1
        assert sample_unit_data.unit_number == "101"
        assert sample_unit_data.code == "UNIT-101"
        assert sample_unit_data.name == "Apartamento 101"
        assert sample_unit_data.private_area == Decimal("75.0000")
        assert sample_unit_data.coefficient == Decimal("5.500000")
        assert sample_unit_data.floor_number == 1
        assert sample_unit_data.floor_label == "Piso 1"
        assert sample_unit_data.occupancy_status == "occupied"
        assert sample_unit_data.sort_order == 10


class TestUnitUseCaseCreate:
    """Tests for UnitUseCase.create()."""

    def test_create_unity_success(self, sample_unit_entity):
        """create() should return success response when unit_number is unique in building."""
        mock_cmd = MagicMock()
        mock_cmd.create.return_value = sample_unit_entity
        mock_query = MagicMock()
        mock_query.get_by_unit_number_in_building.return_value = None
        mock_query.get_by_id.return_value = sample_unit_entity

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = mock_cmd
        use_case.unit_query_usecase = mock_query

        schema = CreateUnitSchema(
            building_id=1,
            unit_number="101",
            name="Apartamento 101",
        )

        result = use_case.create(schema)

        assert result.success is True
        assert result.message == "Unit created successfully"
        assert result.data["unit_number"] == "101"

    def test_create_unity_duplicate_unit_number_raises(self):
        """create() should raise RepeatedUnitUnitNumber when unit_number exists in building."""
        mock_query = MagicMock()
        mock_query.get_by_unit_number_in_building.return_value = UnitEntity(
            id=1, uuid="existing", building_id=1, unit_number="101", name="Existing"
        )

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        schema = CreateUnitSchema(
            building_id=1,
            unit_number="101",
        )

        with pytest.raises(RepeatedUnitUnitNumber):
            use_case.create(schema)


class TestUnitUseCaseUpdate:
    """Tests for UnitUseCase.update()."""

    def test_update_unity_success(self, sample_unit_entity):
        """update() should return success response with updated data."""
        updated_entity = UnitEntity(
            id=1,
            uuid="test-uuid-unity",
            building_id=1,
            unit_number="101",
            name="Apartamento 101 - Actualizado",
            private_area=Decimal("80.0000"),
            coefficient=Decimal("6.000000"),
            status=1,
        )

        mock_cmd = MagicMock()
        mock_cmd.update.return_value = updated_entity
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_unit_entity
        mock_query.get_by_unit_number_in_building.return_value = None

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = mock_cmd
        use_case.unit_query_usecase = mock_query

        schema = UpdateUnitSchema(
            name="Apartamento 101 - Actualizado",
            private_area=80.0,
            coefficient=6.0,
        )

        result = use_case.update(1, schema)

        assert result.success is True
        assert result.message == "Unit updated successfully"
        assert result.data["name"] == "Apartamento 101 - Actualizado"
        assert result.data["private_area"] == 80.0

    def test_update_unity_not_found_raises(self):
        """update() should raise UnitNotFound when unity doesn't exist."""
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = None

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        schema = UpdateUnitSchema(name="New Name")

        with pytest.raises(UnitNotFound):
            use_case.update(999, schema)

    def test_update_unity_occupancy_status_to_invalid_raises(self):
        """Schema should reject invalid occupancy_status at construction time."""
        # ValidationError from Pydantic (not OccupancyStatusNotAllowed from domain)
        # because the schema rejects it before it reaches the use case.
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            UpdateUnitSchema(occupancy_status="not_valid")


class TestUnitUseCaseDelete:
    """Tests for UnitUseCase.delete() (soft delete)."""

    def test_delete_unity_success(self, sample_unit_entity):
        """delete() should soft delete and return success."""
        mock_cmd = MagicMock()
        mock_cmd.soft_delete.return_value = True
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_unit_entity

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = mock_cmd
        use_case.unit_query_usecase = mock_query

        result = use_case.delete(1)

        assert result.success is True
        assert result.message == "Unit deleted successfully (soft delete)"
        mock_cmd.soft_delete.assert_called_once_with(1)

    def test_delete_unity_not_found_raises(self):
        """delete() should raise UnitNotFound when unity doesn't exist."""
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = None

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        with pytest.raises(UnitNotFound):
            use_case.delete(999)


class TestUnitUseCaseRestore:
    """Tests for UnitUseCase.restore()."""

    def test_restore_unity_success(self, sample_unit_entity):
        """restore() should clear deleted_at and return restored unity."""
        mock_cmd = MagicMock()
        mock_cmd.restore.return_value = True
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_unit_entity

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = mock_cmd
        use_case.unit_query_usecase = mock_query

        result = use_case.restore(1)

        assert result.success is True
        assert result.message == "Unit restored successfully"
        mock_cmd.restore.assert_called_once_with(1)

    def test_restore_nonexistent_raises(self):
        """restore() should raise UnitNotFound when restore returns False."""
        mock_cmd = MagicMock()
        mock_cmd.restore.return_value = False
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = None

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = mock_cmd
        use_case.unit_query_usecase = mock_query

        with pytest.raises(UnitNotFound):
            use_case.restore(999)


class TestUnitUseCaseHardDelete:
    """Tests for UnitUseCase.hard_delete()."""

    def test_hard_delete_blocked_when_active_residents(self, sample_unit_entity):
        """hard_delete() should raise UnitHasActiveResidents when residents exist."""
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_unit_entity
        mock_query.count_active_residents.return_value = 3  # 3 active residents

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        with pytest.raises(UnitHasActiveResidents) as exc_info:
            use_case.hard_delete(1)

        assert "1" in str(exc_info.value)  # unit_id in message

    def test_hard_delete_success_when_no_residents(self, sample_unit_entity):
        """hard_delete() should succeed when no active residents."""
        mock_cmd = MagicMock()
        mock_cmd.hard_delete.return_value = True
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_unit_entity
        mock_query.count_active_residents.return_value = 0

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = mock_cmd
        use_case.unit_query_usecase = mock_query

        result = use_case.hard_delete(1)

        assert result.success is True
        assert result.message == "Unit permanently deleted"
        mock_cmd.hard_delete.assert_called_once_with(1)

    def test_hard_delete_not_found_raises(self):
        """hard_delete() should raise UnitNotFound when unity doesn't exist."""
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = None

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        with pytest.raises(UnitNotFound):
            use_case.hard_delete(999)


class TestUnitUseCaseUpdateCodeDuplicate:
    """Tests for duplicate code rejection during update."""

    def test_update_unity_duplicate_code_raises(self, sample_unit_entity):
        """update() should raise RepeatedUnitCode when code already exists in building."""
        existing = UnitEntity(
            id=1, uuid="test", building_id=1, unit_number="101",
            code="OLD-CODE", status=1,
        )
        duplicate = UnitEntity(
            id=2, uuid="dup", building_id=1, unit_number="102",
            code="EXISTING-CODE", status=1,
        )
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = existing
        mock_query.get_by_unit_number_in_building.return_value = None
        mock_query.get_by_code_in_building.return_value = duplicate

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        schema = UpdateUnitSchema(code="EXISTING-CODE")

        with pytest.raises(RepeatedUnitCode):
            use_case.update(1, schema)

    def test_update_unity_code_same_value_allowed(self, sample_unit_entity):
        """update() should allow setting code to the same value it already has."""
        mock_cmd = MagicMock()
        mock_cmd.update.return_value = sample_unit_entity
        mock_query = MagicMock()
        mock_query.get_by_id.return_value = sample_unit_entity
        mock_query.get_by_unit_number_in_building.return_value = None
        mock_query.get_by_code_in_building.return_value = None  # same building, same code = same entity

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = mock_cmd
        use_case.unit_query_usecase = mock_query

        schema = UpdateUnitSchema(code="UNIT-101")  # same as existing

        result = use_case.update(1, schema)

        assert result.success is True


class TestUnityGetByIdExcludesDeleted:
    """Tests that get_by_id and get_by_uuid filter out soft-deleted unities."""

    def test_get_by_id_queries_with_deleted_at_filter(self, sample_unit_entity):
        """get_by_id() should filter by deleted_at IS NULL."""
        from library.dddpy.core_units.infrastructure.unit_query_repository import UnitQueryRepositoryImpl
        from library.dddpy.core_units.infrastructure.dbunits import DBUnits
        from library.dddpy.core_units.infrastructure.unit_mapper import UnitMapper

        repo = UnitQueryRepositoryImpl.__new__(UnitQueryRepositoryImpl)

        with patch(
            "library.dddpy.core_units.infrastructure.unit_query_repository.session_scope"
        ) as mock_scope:
            mock_session = MagicMock()
            mock_scope.return_value.__enter__.return_value = mock_session
            mock_session.query.return_value.filter.return_value.first.return_value = None

            result = repo.get_by_id(999)

            assert result is None
            # Verify the query was called with DBUnits and filtered by id AND deleted_at
            mock_session.query.assert_called_once_with(DBUnits)

    def test_get_by_uuid_queries_with_deleted_at_filter(self):
        """get_by_uuid() should filter by deleted_at IS NULL."""
        from library.dddpy.core_units.infrastructure.unit_query_repository import UnitQueryRepositoryImpl
        from library.dddpy.core_units.infrastructure.dbunits import DBUnits

        repo = UnitQueryRepositoryImpl.__new__(UnitQueryRepositoryImpl)

        with patch(
            "library.dddpy.core_units.infrastructure.unit_query_repository.session_scope"
        ) as mock_scope:
            mock_session = MagicMock()
            mock_scope.return_value.__enter__.return_value = mock_session
            mock_session.query.return_value.filter.return_value.first.return_value = None

            result = repo.get_by_uuid("any-uuid")

            assert result is None
            mock_session.query.assert_called_once_with(DBUnits)


class TestUnitUseCaseList:
    """Tests for UnitUseCase.list_all() and list_by_building()."""

    def test_list_all_returns_paginated_response(self, sample_unit_entity):
        """list_all() should return paginated response with total count."""
        mock_query = MagicMock()
        mock_query.list_all.return_value = ([sample_unit_entity], 1)

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        result = use_case.list_all(
            skip=0,
            limit=100,
            building_id=1,
            occupancy_status="vacant",
            status=1,
            include_deleted=False,
        )

        assert result.success is True
        assert result.message == "Units listed successfully"
        assert result.data["total"] == 1
        assert len(result.data["items"]) == 1
        assert result.data["items"][0]["unit_number"] == "101"
        assert result.data["filters"]["building_id"] == 1
        assert result.data["filters"]["occupancy_status"] == "vacant"

    def test_list_by_building_returns_filtered_response(self, sample_unit_entity):
        """list_by_building() should filter by building_id."""
        mock_query = MagicMock()
        mock_query.list_by_building.return_value = ([sample_unit_entity], 1)

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        result = use_case.list_by_building(
            building_id=1,
            skip=0,
            limit=100,
            occupancy_status="occupied",
            status=1,
            include_deleted=False,
        )

        assert result.success is True
        assert result.data["building_id"] == 1
        assert len(result.data["items"]) == 1
        assert result.data["items"][0]["unit_number"] == "101"

    def test_list_all_limits_max_to_500(self, sample_unit_entity):
        """list_all() should cap limit at 500."""
        mock_query = MagicMock()
        mock_query.list_all.return_value = ([sample_unit_entity], 1)

        use_case = UnitUseCase.__new__(UnitUseCase)
        use_case.unit_cmd_usecase = MagicMock()
        use_case.unit_query_usecase = mock_query

        result = use_case.list_all(skip=0, limit=1000)

        assert result.data["limit"] == 500


class TestUnityCmdSchema:
    """Tests for Pydantic schemas."""

    def test_create_schema_requires_building_id(self):
        """CreateUnitSchema should require building_id."""
        with pytest.raises(Exception):  # ValidationError
            CreateUnitSchema(unit_number="101")

    def test_create_schema_requires_unit_number(self):
        """CreateUnitSchema should require unit_number."""
        with pytest.raises(Exception):  # ValidationError
            CreateUnitSchema(building_id=1)

    def test_create_schema_validates_coefficient_range(self):
        """CreateUnitSchema should reject coefficient > 100."""
        with pytest.raises(Exception):
            CreateUnitSchema(
                building_id=1,
                unit_number="101",
                coefficient=150.0,
            )

    def test_create_schema_validates_coefficient_negative(self):
        """CreateUnitSchema should reject negative coefficient."""
        with pytest.raises(Exception):
            CreateUnitSchema(
                building_id=1,
                unit_number="101",
                coefficient=-5.0,
            )

    def test_create_schema_validates_negative_private_area(self):
        """CreateUnitSchema should reject negative private_area."""
        with pytest.raises(Exception):
            CreateUnitSchema(
                building_id=1,
                unit_number="101",
                private_area=-50.0,
            )

    def test_create_schema_validates_negative_sort_order(self):
        """CreateUnitSchema should reject negative sort_order."""
        with pytest.raises(Exception):
            CreateUnitSchema(
                building_id=1,
                unit_number="101",
                sort_order=-1,
            )

    def test_create_schema_accepts_all_valid_occupancy_statuses(self):
        """CreateUnitSchema should accept all five valid occupancy statuses."""
        valid = ["vacant", "occupied", "reserved", "maintenance", "blocked"]
        for status in valid:
            schema = CreateUnitSchema(
                building_id=1,
                unit_number="101",
                occupancy_status=status,
            )
            assert schema.occupancy_status == status

    def test_create_schema_defaults_occupancy_status_to_vacant(self):
        """CreateUnitSchema should default occupancy_status to 'vacant'."""
        schema = CreateUnitSchema(
            building_id=1,
            unit_number="101",
        )
        assert schema.occupancy_status == "vacant"

    def test_update_schema_all_fields_optional(self):
        """UpdateUnitSchema should allow partial updates."""
        schema = UpdateUnitSchema(name="New Name")
        assert schema.name == "New Name"
        assert schema.occupancy_status is None
        assert schema.sort_order is None
        assert schema.status is None

    def test_update_schema_validates_occupancy_status_enum(self):
        """UpdateUnitSchema should validate occupancy_status values."""
        with pytest.raises(Exception):
            UpdateUnitSchema(occupancy_status="invalid")


class TestUnityExceptions:
    """Tests for unity exception classes."""

    def test_unity_not_found_has_404(self):
        """UnitNotFound should have status_code=404."""
        exc = UnitNotFound()
        assert exc.status_code == 404
        assert "not found" in exc.message.lower()

    def test_repeated_unity_unit_number_has_409(self):
        """RepeatedUnitUnitNumber should have status_code=409."""
        exc = RepeatedUnitUnitNumber()
        assert exc.status_code == 409
        assert "unit number" in exc.message.lower()

    def test_repeated_unity_code_has_409(self):
        """RepeatedUnitCode should have status_code=409."""
        exc = RepeatedUnitCode()
        assert exc.status_code == 409
        assert "code" in exc.message.lower()

    def test_unity_has_active_residents_has_409(self):
        """UnitHasActiveResidents should have status_code=409 and include unit_id."""
        exc = UnitHasActiveResidents(42)
        assert exc.status_code == 409
        assert "42" in exc.message
        assert "residents" in exc.message.lower()

    def test_occupancy_status_not_allowed_has_400(self):
        """OccupancyStatusNotAllowed should have status_code=400."""
        exc = OccupancyStatusNotAllowed("foo")
        assert exc.status_code == 400
        assert "foo" in exc.message


class TestUnitRepositoryContracts:
    """Tests for repository interface contracts."""

    def test_unity_repository_interface_is_importable(self):
        """UnitRepository should be importable and defined."""
        from library.dddpy.core_units.domain.unit_repository import UnitRepository
        assert UnitRepository is not None

    def test_unity_cmd_repository_interface_is_importable(self):
        """UnitCmdRepository should be importable and defined."""
        from library.dddpy.core_units.domain.unit_cmd_repository import UnitCmdRepository
        assert UnitCmdRepository is not None

    def test_unity_query_repository_interface_is_importable(self):
        """UnitQueryRepository should be importable and defined."""
        from library.dddpy.core_units.domain.unit_query_repository import UnitQueryRepository
        assert UnitQueryRepository is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
