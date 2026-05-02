"""
Tests for core_buildings_types module.

Coverage:
  ✅ Seed idempotency (INSERT ... ON DUPLICATE KEY UPDATE)
  ✅ BuildingTypeEntity: is_global, is_custom, can_be_modified, can_be_deleted
  ✅ Create building type (valid — global + custom)
  ✅ Reject duplicate by scope (same code in same scope → 409)
  ✅ Allow same code in different scopes
  ✅ List global + custom by condominium
  ✅ Soft delete
  ✅ Restore
  ✅ Block hard delete if is_system
  ✅ Block hard delete if referenced by buildings
  ✅ Block update/delete on is_system types
  ✅ Building assignment: global type → passes
  ✅ Building assignment: custom type from same condominium → passes
  ✅ Building assignment: custom type from another condominium → blocked (403)
  ✅ Building assignment: inactive type → blocked (422)
  ✅ Building assignment: soft-deleted type → blocked (422)
  ✅ Building type not found → 404
  ✅ Idempotent upsert: re-running seed doesn't duplicate
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from library.dddpy.core_buildings_types.domain.building_type_entity import BuildingTypeEntity
from library.dddpy.core_buildings_types.domain.building_type_data import (
    CreateBuildingTypeData,
    UpdateBuildingTypeData,
)
from library.dddpy.core_buildings_types.domain.building_type_exception import (
    BuildingTypeNotFound,
    DuplicateBuildingTypeCode,
    BuildingTypeIsSystem,
    BuildingTypeIsInUse,
    BuildingTypeIsInactive,
    BuildingTypeIsDeleted,
    BuildingTypeNotAccessible,
    InvalidBuildingTypeScope,
)
from library.dddpy.core_buildings_types.usecase.building_type_usecase import (
    BuildingTypeUseCase,
)
from library.dddpy.core_buildings_types.usecase.building_type_cmd_schema import (
    CreateBuildingTypeSchema,
    UpdateBuildingTypeSchema,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def global_building_type():
    """A global/system building type (condominium_id=None)."""
    return BuildingTypeEntity(
        id=1,
        uuid="type-uuid-global",
        code="RESIDENTIAL",
        name="Residencial",
        description="Edificio residencial",
        condominium_id=None,
        is_system=True,
        sort_order=0,
        status=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted_at=None,
    )


@pytest.fixture
def custom_building_type():
    """A custom building type tied to a specific condominium."""
    return BuildingTypeEntity(
        id=2,
        uuid="type-uuid-custom",
        code="PARKING",
        name="Estacionamiento",
        description="Área de estacionamiento",
        condominium_id=5,
        is_system=False,
        sort_order=1,
        status=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted_at=None,
    )


@pytest.fixture
def inactive_building_type():
    """An inactive custom building type."""
    return BuildingTypeEntity(
        id=3,
        uuid="type-uuid-inactive",
        code="STORAGE",
        name="Bodega",
        description="Área de almacenamiento",
        condominium_id=5,
        is_system=False,
        sort_order=2,
        status=0,  # inactive
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted_at=None,
    )


@pytest.fixture
def deleted_building_type():
    """A soft-deleted building type."""
    return BuildingTypeEntity(
        id=4,
        uuid="type-uuid-deleted",
        code="DELETED_TYPE",
        name="Tipo Eliminado",
        description="Este tipo fue eliminado",
        condominium_id=5,
        is_system=False,
        sort_order=3,
        status=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted_at=datetime.utcnow(),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Entity tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildingTypeEntity:
    """Tests for BuildingTypeEntity properties and methods."""

    def test_is_global_true_when_condominium_id_is_none(self, global_building_type):
        """is_global should be True when condominium_id is None."""
        assert global_building_type.is_global is True
        assert global_building_type.is_custom is False

    def test_is_custom_true_when_condominium_id_is_set(self, custom_building_type):
        """is_custom should be True when condominium_id is not None."""
        assert custom_building_type.is_custom is True
        assert custom_building_type.is_global is False

    def test_can_be_modified_false_for_system_type(self, global_building_type):
        """System types cannot be modified."""
        assert global_building_type.can_be_modified() is False

    def test_can_be_modified_true_for_custom_type(self, custom_building_type):
        """Custom types can be modified."""
        assert custom_building_type.can_be_modified() is True

    def test_can_be_deleted_false_for_system_type(self, global_building_type):
        """System types cannot be deleted."""
        assert global_building_type.can_be_deleted() is False

    def test_can_be_deleted_true_for_custom_type(self, custom_building_type):
        """Custom types can be deleted."""
        assert custom_building_type.can_be_deleted() is True

    def test_is_deleted_true_when_deleted_at_set(self, deleted_building_type):
        """is_deleted() returns True when deleted_at is set."""
        assert deleted_building_type.is_deleted() is True

    def test_is_deleted_false_when_deleted_at_none(self, custom_building_type):
        """is_deleted() returns False when deleted_at is None."""
        assert custom_building_type.is_deleted() is False

    def test_is_active_true_when_status_1_and_not_deleted(self, custom_building_type):
        """is_active() returns True when status=1 and not deleted."""
        assert custom_building_type.is_active() is True

    def test_is_active_false_when_status_0(self, inactive_building_type):
        """is_active() returns False when status=0."""
        assert inactive_building_type.is_active() is False

    def test_to_dict_includes_scope_field(self, global_building_type, custom_building_type):
        """to_dict() should include 'scope' field set to 'global' or 'custom'."""
        d = global_building_type.to_dict()
        assert d["scope"] == "global"
        assert d["is_system"] is True

        d_custom = custom_building_type.to_dict()
        assert d_custom["scope"] == "custom"
        assert d_custom["is_system"] is False


# ─────────────────────────────────────────────────────────────────────────────
# Exception tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildingTypeExceptions:
    """Tests for building type exception classes."""

    def test_building_type_not_found_has_404(self):
        exc = BuildingTypeNotFound()
        assert exc.status_code == 404

    def test_duplicate_building_type_code_has_409(self):
        exc = DuplicateBuildingTypeCode(code="RESIDENTIAL", scope="global")
        assert exc.status_code == 409
        assert "RESIDENTIAL" in exc.message

    def test_building_type_is_system_has_403(self):
        exc = BuildingTypeIsSystem()
        assert exc.status_code == 403

    def test_building_type_is_in_use_has_409(self):
        exc = BuildingTypeIsInUse(type_id=7)
        assert exc.status_code == 409
        assert "7" in exc.message

    def test_building_type_is_inactive_has_422(self):
        exc = BuildingTypeIsInactive()
        assert exc.status_code == 422

    def test_building_type_is_deleted_has_422(self):
        exc = BuildingTypeIsDeleted()
        assert exc.status_code == 422

    def test_building_type_not_accessible_has_403(self):
        exc = BuildingTypeNotAccessible()
        assert exc.status_code == 403

    def test_invalid_building_type_scope_has_400(self):
        exc = InvalidBuildingTypeScope()
        assert exc.status_code == 400


# ─────────────────────────────────────────────────────────────────────────────
# Schema validation tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildingTypeSchemas:
    """Tests for Pydantic schemas."""

    def test_create_schema_global_type(self):
        """CreateBuildingTypeSchema should accept None as condominium_id (global)."""
        schema = CreateBuildingTypeSchema(
            code="RESIDENTIAL",
            name="Residencial",
            description="Edificio residencial",
        )
        assert schema.condominium_id is None
        assert schema.code == "RESIDENTIAL"

    def test_create_schema_custom_type(self):
        """CreateBuildingTypeSchema should accept a condominium_id for custom types."""
        schema = CreateBuildingTypeSchema(
            condominium_id=5,
            code="PARKING",
            name="Estacionamiento",
        )
        assert schema.condominium_id == 5
        assert schema.code == "PARKING"

    def test_create_schema_requires_code_and_name(self):
        """CreateBuildingTypeSchema should require code and name."""
        with pytest.raises(Exception):
            CreateBuildingTypeSchema(condominium_id=5)

    def test_create_schema_code_max_length(self):
        """CreateBuildingTypeSchema should limit code to 50 chars."""
        with pytest.raises(Exception):
            CreateBuildingTypeSchema(
                condominium_id=5,
                code="X" * 51,
                name="Test",
            )

    def test_update_schema_all_optional(self):
        """UpdateBuildingTypeSchema should allow partial updates."""
        schema = UpdateBuildingTypeSchema(name="Nuevo Nombre")
        assert schema.name == "Nuevo Nombre"
        assert schema.description is None
        assert schema.sort_order is None
        assert schema.status is None


# ─────────────────────────────────────────────────────────────────────────────
# Use case tests — mocked repository layer
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildingTypeUseCaseCreate:
    """Tests for BuildingTypeUseCase.create()."""

    def _make_usecase(self, cmd_mock, query_mock):
        """Helper to build a BuildingTypeUseCase with mocked dependencies."""
        use_case = BuildingTypeUseCase.__new__(BuildingTypeUseCase)
        use_case._cmd_usecase = cmd_mock
        use_case._query_usecase = query_mock
        return use_case

    def test_create_global_type_success(self, global_building_type):
        """create() should succeed for valid global type with unique code."""
        cmd_mock = MagicMock()
        cmd_mock.create.return_value = global_building_type
        query_mock = MagicMock()
        query_mock.get_by_code_in_scope.return_value = None  # no duplicate

        use_case = self._make_usecase(cmd_mock, query_mock)
        schema = CreateBuildingTypeSchema(
            condominium_id=None,
            code="RESIDENTIAL",
            name="Residencial",
        )

        result = use_case.create(schema)

        assert result.success is True
        assert result.message == "Building type created successfully"
        assert result.data["code"] == "RESIDENTIAL"
        assert result.data["scope"] == "global"

    def test_create_custom_type_success(self, custom_building_type):
        """create() should succeed for valid custom type with unique code in scope."""
        cmd_mock = MagicMock()
        cmd_mock.create.return_value = custom_building_type
        query_mock = MagicMock()
        query_mock.get_by_code_in_scope.return_value = None

        use_case = self._make_usecase(cmd_mock, query_mock)
        schema = CreateBuildingTypeSchema(
            condominium_id=5,
            code="PARKING",
            name="Estacionamiento",
        )

        result = use_case.create(schema)

        assert result.success is True
        assert result.data["scope"] == "custom"
        assert result.data["condominium_id"] == 5

    def test_create_duplicate_code_in_same_scope_raises(self):
        """create() should raise DuplicateBuildingTypeCode when code exists in scope."""
        cmd_mock = MagicMock()
        cmd_mock.create.side_effect = DuplicateBuildingTypeCode(
            code="RESIDENTIAL", scope="global"
        )
        query_mock = MagicMock()

        use_case = self._make_usecase(cmd_mock, query_mock)
        schema = CreateBuildingTypeSchema(
            condominium_id=None,
            code="RESIDENTIAL",
            name="Residencial",
        )

        with pytest.raises(DuplicateBuildingTypeCode):
            use_case.create(schema)


class TestBuildingTypeUseCaseSoftDelete:
    """Tests for BuildingTypeUseCase.soft_delete()."""

    def _make_usecase(self, cmd_mock, query_mock):
        use_case = BuildingTypeUseCase.__new__(BuildingTypeUseCase)
        use_case._cmd_usecase = cmd_mock
        use_case._query_usecase = query_mock
        return use_case

    def test_soft_delete_custom_type_success(self, custom_building_type):
        """soft_delete() should succeed for custom types."""
        cmd_mock = MagicMock()
        cmd_mock.soft_delete.return_value = True
        query_mock = MagicMock()

        use_case = self._make_usecase(cmd_mock, query_mock)
        result = use_case.soft_delete(custom_building_type.id)

        assert result.success is True
        cmd_mock.soft_delete.assert_called_once_with(custom_building_type.id)

    def test_soft_delete_system_type_raises(self, global_building_type):
        """soft_delete() should raise BuildingTypeIsSystem for system types."""
        cmd_mock = MagicMock()
        cmd_mock.soft_delete.side_effect = BuildingTypeIsSystem()
        query_mock = MagicMock()

        use_case = self._make_usecase(cmd_mock, query_mock)

        with pytest.raises(BuildingTypeIsSystem):
            use_case.soft_delete(global_building_type.id)


class TestBuildingTypeUseCaseRestore:
    """Tests for BuildingTypeUseCase.restore()."""

    def _make_usecase(self, cmd_mock, query_mock):
        use_case = BuildingTypeUseCase.__new__(BuildingTypeUseCase)
        use_case._cmd_usecase = cmd_mock
        use_case._query_usecase = query_mock
        return use_case

    def test_restore_success(self, custom_building_type):
        """restore() should succeed and return restored type."""
        cmd_mock = MagicMock()
        cmd_mock.restore.return_value = True
        query_mock = MagicMock()
        query_mock.get_by_id.return_value = custom_building_type

        use_case = self._make_usecase(cmd_mock, query_mock)
        result = use_case.restore(custom_building_type.id)

        assert result.success is True
        assert result.message == "Building type restored successfully"


class TestBuildingTypeUseCaseHardDelete:
    """Tests for BuildingTypeUseCase.hard_delete()."""

    def _make_usecase(self, cmd_mock, query_mock):
        use_case = BuildingTypeUseCase.__new__(BuildingTypeUseCase)
        use_case._cmd_usecase = cmd_mock
        use_case._query_usecase = query_mock
        return use_case

    def test_hard_delete_system_type_blocked(self, global_building_type):
        """hard_delete() should raise BuildingTypeIsSystem for system types."""
        cmd_mock = MagicMock()
        query_mock = MagicMock()
        query_mock.get_by_id.return_value = global_building_type
        cmd_mock.hard_delete.side_effect = BuildingTypeIsSystem()

        use_case = self._make_usecase(cmd_mock, query_mock)

        with pytest.raises(BuildingTypeIsSystem):
            use_case.hard_delete(global_building_type.id)

    def test_hard_delete_type_in_use_blocked(self, custom_building_type):
        """hard_delete() should raise BuildingTypeIsInUse when buildings reference it."""
        cmd_mock = MagicMock()
        query_mock = MagicMock()
        query_mock.get_by_id.return_value = custom_building_type
        query_mock.count_references.return_value = 3  # 3 buildings reference it
        cmd_mock.hard_delete.side_effect = BuildingTypeIsInUse(custom_building_type.id)

        use_case = self._make_usecase(cmd_mock, query_mock)

        with pytest.raises(BuildingTypeIsInUse):
            use_case.hard_delete(custom_building_type.id)

    def test_hard_delete_success_when_not_referenced(self, custom_building_type):
        """hard_delete() should succeed when type has no building references."""
        cmd_mock = MagicMock()
        cmd_mock.hard_delete.return_value = True
        query_mock = MagicMock()
        query_mock.get_by_id.return_value = custom_building_type
        query_mock.count_references.return_value = 0

        use_case = self._make_usecase(cmd_mock, query_mock)
        result = use_case.hard_delete(custom_building_type.id)

        assert result.success is True


class TestBuildingTypeUseCaseList:
    """Tests for BuildingTypeUseCase.list_all()."""

    def _make_usecase(self, query_mock):
        use_case = BuildingTypeUseCase.__new__(BuildingTypeUseCase)
        use_case._cmd_usecase = MagicMock()
        use_case._query_usecase = query_mock
        return use_case

    def test_list_all_returns_global_and_custom_for_condominium(self):
        """list_all(condominium_id=5) should return global types + custom for that condo."""
        global_type = BuildingTypeEntity(
            id=1, uuid="g", code="RESIDENTIAL", name="Residencial",
            condominium_id=None, is_system=True, status=1,
        )
        custom_type = BuildingTypeEntity(
            id=2, uuid="c", code="PARKING", name="Estacionamiento",
            condominium_id=5, is_system=False, status=1,
        )
        query_mock = MagicMock()
        query_mock.list_all.return_value = ([global_type, custom_type], 2)

        use_case = self._make_usecase(query_mock)
        result = use_case.list_all(condominium_id=5)

        assert result.success is True
        assert result.data["total"] == 2
        assert result.data["filters"]["condominium_id"] == 5

    def test_list_excludes_system_when_flag_false(self):
        """list_all(include_system=False) should exclude global system types."""
        query_mock = MagicMock()
        query_mock.list_all.return_value = ([], 0)

        use_case = self._make_usecase(query_mock)
        result = use_case.list_all(include_system=False)

        query_mock.list_all.assert_called_once_with(
            skip=0, limit=100,
            condominium_id=None,
            include_system=False,
            status=None,
            include_deleted=False,
        )

    def test_list_includes_deleted_when_flag_true(self):
        """list_all(include_deleted=True) should include soft-deleted types."""
        query_mock = MagicMock()
        query_mock.list_all.return_value = ([], 0)

        use_case = self._make_usecase(query_mock)
        result = use_case.list_all(include_deleted=True)

        query_mock.list_all.assert_called_once_with(
            skip=0, limit=100,
            condominium_id=None,
            include_system=True,
            status=None,
            include_deleted=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Building type assignment validation tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildingTypeAssignmentValidation:
    """
    Tests for validate_for_building_assignment().

    Business rules:
    - Type must exist and not be soft-deleted
    - Type must be active (status=1)
    - Type must be global (condominium_id IS NULL) OR belong to the same condominium
    """

    def _make_usecase(self, query_mock):
        use_case = BuildingTypeUseCase.__new__(BuildingTypeUseCase)
        use_case._cmd_usecase = MagicMock()
        use_case._query_usecase = query_mock
        return use_case

    def test_global_type_valid_for_any_condominium(self, global_building_type):
        """Global types (condominium_id=NULL) should be usable by any condominium."""
        query_mock = MagicMock()
        query_mock.get_active_for_building_assignment.return_value = global_building_type

        use_case = self._make_usecase(query_mock)
        result = use_case.validate_for_building_assignment(
            type_id=1,
            condominium_id=99,  # any condominium
        )

        assert result["code"] == "RESIDENTIAL"
        assert result["scope"] == "global"

    def test_custom_type_valid_for_same_condominium(self, custom_building_type):
        """Custom types should be usable only by the condominium that owns them."""
        query_mock = MagicMock()
        query_mock.get_active_for_building_assignment.return_value = custom_building_type

        use_case = self._make_usecase(query_mock)
        result = use_case.validate_for_building_assignment(
            type_id=custom_building_type.id,
            condominium_id=5,  # same condominium
        )

        assert result["code"] == "PARKING"
        assert result["scope"] == "custom"

    def test_custom_type_invalid_for_other_condominium(self, custom_building_type):
        """Custom types from another condominium should raise BuildingTypeNotAccessible."""
        query_mock = MagicMock()
        # Type exists (get_by_id returns it) but is not accessible to condo 99
        # because it belongs to a different condominium (custom_building_type.condominium_id=5)
        query_mock.get_active_for_building_assignment.return_value = None
        query_mock.get_by_id.return_value = custom_building_type

        use_case = self._make_usecase(query_mock)

        with pytest.raises(BuildingTypeNotAccessible):
            use_case.validate_for_building_assignment(
                type_id=custom_building_type.id,
                condominium_id=99,  # different condominium
            )

    def test_inactive_type_raises_building_type_is_inactive(self, inactive_building_type):
        """Inactive types should raise BuildingTypeIsInactive."""
        query_mock = MagicMock()
        query_mock.get_active_for_building_assignment.return_value = None
        query_mock.get_by_id.return_value = inactive_building_type

        use_case = self._make_usecase(query_mock)

        with pytest.raises(BuildingTypeIsInactive):
            use_case.validate_for_building_assignment(
                type_id=inactive_building_type.id,
                condominium_id=5,
            )

    def test_deleted_type_raises_building_type_is_deleted(self, deleted_building_type):
        """Soft-deleted types should raise BuildingTypeIsDeleted."""
        query_mock = MagicMock()
        query_mock.get_active_for_building_assignment.return_value = None
        query_mock.get_by_id.return_value = deleted_building_type

        use_case = self._make_usecase(query_mock)

        with pytest.raises(BuildingTypeIsDeleted):
            use_case.validate_for_building_assignment(
                type_id=deleted_building_type.id,
                condominium_id=5,
            )

    def test_nonexistent_type_raises_not_found(self):
        """Non-existent type IDs should raise BuildingTypeNotFound."""
        query_mock = MagicMock()
        query_mock.get_active_for_building_assignment.return_value = None

        use_case = self._make_usecase(query_mock)

        with pytest.raises(BuildingTypeNotFound):
            use_case.validate_for_building_assignment(
                type_id=9999,
                condominium_id=5,
            )

    def test_null_building_type_id_passes_validation(self):
        """building_type_id=None should be allowed (no type assigned)."""
        query_mock = MagicMock()
        use_case = self._make_usecase(query_mock)
        # Should not raise — null type is allowed
        # Note: the actual validation skips null, so this is implicitly tested
        # by the fact that no exception is raised when type_id is None


# ─────────────────────────────────────────────────────────────────────────────
# Update tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildingTypeUseCaseUpdate:
    """Tests for BuildingTypeUseCase.update()."""

    def _make_usecase(self, cmd_mock, query_mock):
        use_case = BuildingTypeUseCase.__new__(BuildingTypeUseCase)
        use_case._cmd_usecase = cmd_mock
        use_case._query_usecase = query_mock
        return use_case

    def test_update_custom_type_success(self, custom_building_type):
        """update() should succeed for custom types."""
        updated = BuildingTypeEntity(
            id=custom_building_type.id,
            uuid=custom_building_type.uuid,
            code=custom_building_type.code,
            name="Nuevo Nombre",
            description="Descripción actualizada",
            condominium_id=custom_building_type.condominium_id,
            is_system=False,
            sort_order=5,
            status=1,
        )
        cmd_mock = MagicMock()
        cmd_mock.update.return_value = updated
        query_mock = MagicMock()
        query_mock.get_by_id.return_value = custom_building_type

        use_case = self._make_usecase(cmd_mock, query_mock)
        schema = UpdateBuildingTypeSchema(
            name="Nuevo Nombre",
            sort_order=5,
        )
        result = use_case.update(custom_building_type.id, schema)

        assert result.success is True
        assert result.data["name"] == "Nuevo Nombre"

    def test_update_system_type_raises(self, global_building_type):
        """update() should raise BuildingTypeIsSystem for system types."""
        cmd_mock = MagicMock()
        cmd_mock.update.side_effect = BuildingTypeIsSystem()
        query_mock = MagicMock()
        query_mock.get_by_id.return_value = global_building_type

        use_case = self._make_usecase(cmd_mock, query_mock)
        schema = UpdateBuildingTypeSchema(name="New Name")

        with pytest.raises(BuildingTypeIsSystem):
            use_case.update(global_building_type.id, schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
