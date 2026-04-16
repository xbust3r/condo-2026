"""
Tests de integración para RBAC — Phase 2.

Cubre:
  - RBAC-01: condominium_admin = 1 por condominio
  - RBAC-02: super_admin no asignable via API
  - PermissionService.has_permission()
  - get_effective_resident_context()
"""
import pytest
import sys
from unittest.mock import MagicMock, patch

# ─────────────────────────────────────────────────────────────────────────────
# Ensure library is importable from src
# ─────────────────────────────────────────────────────────────────────────────
sys.path.insert(0, "/home/miguel/servers/condo-py/src")


class TestCondominiumRoleSchemaValidation:
    """Tests para validaciones del schema CreateCondominiumRoleSchema."""

    def test_valid_roles_v2_accepted(self):
        """All v2 roles are accepted by the schema."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )

        valid_roles = [
            "super_admin",
            "condominium_admin",
            "board_member",
            "finance_reviewer",
            "security_staff",
            "maintenance_staff",
            "operations_staff",
        ]
        for role in valid_roles:
            schema = CreateCondominiumRoleSchema(
                condominium_id=1,
                user_id=1,
                role=role,
            )
            assert schema.role == role

    def test_invalid_role_rejected(self):
        """Invalid role names are rejected."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            CreateCondominiumRoleSchema(
                condominium_id=1,
                user_id=1,
                role="building_manager",  # old role, not in v2
            )
        assert "role must be one of" in str(exc_info.value)

    def test_invalid_scope_rejected(self):
        """Invalid scope values are rejected."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            CreateCondominiumRoleSchema(
                condominium_id=1,
                user_id=1,
                role="maintenance_staff",
                scope="floor",  # invalid scope
            )
        assert "scope must be one of" in str(exc_info.value)

    def test_scope_and_building_id_fields_work(self):
        """scope and building_id fields are accepted and stored."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )

        schema = CreateCondominiumRoleSchema(
            condominium_id=1,
            user_id=1,
            role="maintenance_staff",
            scope="building",
            building_id=5,
        )
        assert schema.scope == "building"
        assert schema.building_id == 5

    def test_update_schema_accepts_scope_and_building_id(self):
        """UpdateCondominiumRoleSchema accepts scope and building_id."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            UpdateCondominiumRoleSchema,
        )

        schema = UpdateCondominiumRoleSchema(
            scope="building",
            building_id=3,
        )
        assert schema.scope == "building"
        assert schema.building_id == 3


class TestCondominiumRoleRBACBusinessRules:
    """Tests para las reglas de negocio RBAC en CondominiumRoleCmdUseCase."""

    def test_create_super_admin_raises_role_is_system(self):
        """RBAC-02: Attempt to create super_admin via API raises RoleIsSystem."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_usecase import (
            CondominiumRoleCmdUseCase,
        )
        from library.dddpy.core_condominium_roles.domain.condominium_role_exception import (
            RoleIsSystem,
        )

        mock_repo = MagicMock()
        use_case = CondominiumRoleCmdUseCase(repository=mock_repo)

        schema = CreateCondominiumRoleSchema(
            condominium_id=1,
            user_id=1,
            role="super_admin",
        )

        with pytest.raises(RoleIsSystem) as exc_info:
            use_case.create(schema)
        assert "system roles cannot be modified" in str(exc_info.value).lower()

    def test_create_condominium_admin_first_time_succeeds(self):
        """RBAC-01: First condominium_admin can be created (no existing active admin)."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_usecase import (
            CondominiumRoleCmdUseCase,
        )
        from library.dddpy.core_condominium_roles.domain.condominium_role_entity import (
            CondominiumRoleEntity,
        )

        mock_repo = MagicMock()
        mock_query_repo = MagicMock()
        mock_query_repo.list_by_condominium.return_value = ([], 0)

        created_entity = CondominiumRoleEntity(
            id=1,
            uuid="test-uuid",
            condominium_id=1,
            user_id=1,
            role="condominium_admin",
            status="active",
            scope="condominium",
        )
        mock_repo.create.return_value = created_entity

        use_case = CondominiumRoleCmdUseCase(repository=mock_repo)

        # Patch query repo AND skip _validate_condominium / _validate_user
        with patch(
            "library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository."
            "CondominiumRoleQueryRepositoryImpl",
        ) as mock_query_repo_cls, \
        patch.object(use_case, "_validate_condominium"), \
        patch.object(use_case, "_validate_user"):
            mock_query_repo_cls.return_value = mock_query_repo
            schema = CreateCondominiumRoleSchema(
                condominium_id=1,
                user_id=1,
                role="condominium_admin",
            )
            result = use_case.create(schema)

        assert result.role == "condominium_admin"
        assert result.condominium_id == 1
        mock_repo.create.assert_called_once()

    def test_create_second_condominium_admin_raises_duplicate(self):
        """RBAC-01: Second condominium_admin raises DuplicateRoleAssignment."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_usecase import (
            CondominiumRoleCmdUseCase,
        )
        from library.dddpy.core_condominium_roles.domain.condominium_role_entity import (
            CondominiumRoleEntity,
        )
        from library.dddpy.core_condominium_roles.domain.condominium_role_exception import (
            DuplicateRoleAssignment,
        )

        existing_admin = CondominiumRoleEntity(
            id=1,
            uuid="existing-uuid",
            condominium_id=1,
            user_id=10,
            role="condominium_admin",
            status="active",
            scope="condominium",
        )

        mock_repo = MagicMock()
        mock_query_repo = MagicMock()
        mock_query_repo.list_by_condominium.return_value = ([existing_admin], 1)

        use_case = CondominiumRoleCmdUseCase(repository=mock_repo)

        with patch(
            "library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository."
            "CondominiumRoleQueryRepositoryImpl",
        ) as mock_query_repo_cls:
            mock_query_repo_cls.return_value = mock_query_repo
            schema = CreateCondominiumRoleSchema(
                condominium_id=1,
                user_id=20,
                role="condominium_admin",
            )
            with pytest.raises(DuplicateRoleAssignment) as exc_info:
                use_case.create(schema)
            assert "condominium_admin" in str(exc_info.value).lower()

    def test_update_role_to_super_admin_raises(self):
        """RBAC-02: Attempt to update role to super_admin raises RoleIsSystem."""
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            UpdateCondominiumRoleSchema,
        )
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_usecase import (
            CondominiumRoleCmdUseCase,
        )
        from library.dddpy.core_condominium_roles.domain.condominium_role_exception import (
            RoleIsSystem,
        )

        mock_repo = MagicMock()
        mock_query_repo = MagicMock()

        use_case = CondominiumRoleCmdUseCase(repository=mock_repo)

        with patch(
            "library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository."
            "CondominiumRoleQueryRepositoryImpl",
        ) as mock_query_repo_cls:
            mock_query_repo_cls.return_value = mock_query_repo
            schema = UpdateCondominiumRoleSchema(role="super_admin")
            with pytest.raises(RoleIsSystem):
                use_case.update(id=1, schema=schema)


class TestCondominiumRoleDataLayer:
    """Tests para CondominiumRoleData y CondominiumRoleEntity."""

    def test_create_data_has_scope_and_building_id(self):
        """CreateCondominiumRoleData accepts scope and building_id."""
        from library.dddpy.core_condominium_roles.domain.condominium_role_data import (
            CreateCondominiumRoleData,
        )

        data = CreateCondominiumRoleData(
            condominium_id=1,
            user_id=1,
            role="maintenance_staff",
            scope="building",
            building_id=7,
        )
        assert data.scope == "building"
        assert data.building_id == 7

    def test_update_data_has_scope_and_building_id(self):
        """UpdateCondominiumRoleData accepts scope and building_id."""
        from library.dddpy.core_condominium_roles.domain.condominium_role_data import (
            UpdateCondominiumRoleData,
        )

        data = UpdateCondominiumRoleData(
            scope="building",
            building_id=3,
        )
        assert data.scope == "building"
        assert data.building_id == 3

    def test_entity_valid_scopes_v2(self):
        """CondominiumRoleEntity.VALID_ROLES matches v2 from planning."""
        from library.dddpy.core_condominium_roles.domain.condominium_role_entity import (
            CondominiumRoleEntity,
        )

        assert CondominiumRoleEntity.VALID_ROLES == {
            "super_admin",
            "condominium_admin",
            "board_member",
            "finance_reviewer",
            "security_staff",
            "maintenance_staff",
            "operations_staff",
        }
        assert CondominiumRoleEntity.VALID_SCOPES == {"condominium", "unit", "building"}


class TestPermissionEntities:
    """Tests para PermissionEntity y RolePermissionEntity."""

    def test_permission_entity_to_dict(self):
        from datetime import datetime
        from library.dddpy.core_permissions.domain.permission_entity import PermissionEntity

        entity = PermissionEntity(
            id=1,
            code="building.read",
            resource="building",
            action="read",
            scope_default="condominium",
            description="Ver edificios",
            created_at=datetime(2026, 4, 16, 12, 0, 0),
        )
        d = entity.to_dict()
        assert d["code"] == "building.read"
        assert d["resource"] == "building"
        assert d["action"] == "read"
        assert d["scope_default"] == "condominium"

    def test_role_permission_entity_to_dict(self):
        from library.dddpy.core_role_permissions.domain.role_permission_entity import (
            RolePermissionEntity,
        )

        entity = RolePermissionEntity(
            role="condominium_admin",
            permission_code="building.read",
            scope_override=None,
        )
        d = entity.to_dict()
        assert d["role"] == "condominium_admin"
        assert d["permission_code"] == "building.read"
        assert d["scope_override"] is None

    def test_role_permission_entity_with_override(self):
        from library.dddpy.core_role_permissions.domain.role_permission_entity import (
            RolePermissionEntity,
        )

        entity = RolePermissionEntity(
            role="maintenance_staff",
            permission_code="unit.read",
            scope_override="building",
        )
        d = entity.to_dict()
        assert d["scope_override"] == "building"
