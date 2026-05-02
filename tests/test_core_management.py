"""
Integration tests for management modules: user profiles, unit occupancies,
unit ownerships, condominium roles, and dashboards.

Each test class:
  1. Creates a minimal sandbox (condo + building + units + users)
  2. Exercises the module's use cases against the real MariaDB
  3. Cleans up all records via _cleanup_by_condo()
"""
import uuid
import pytest
from datetime import datetime, date

from tests.test_core_foundations import _make_minimal_sandbox, _cleanup_by_condo


def _teardown(db_session, sb):
    _cleanup_by_condo(db_session, sb.condo.id)


def _ensure_occupancy_type(db_session) -> int:
    """Create an occupancy type via OccupancyTypeUseCase and return its id."""
    from library.dddpy.core_occupancy_types.usecase.occupancy_type_usecase import (
        OccupancyTypeUseCase,
    )
    from library.dddpy.core_occupancy_types.usecase.occupancy_type_cmd_schema import (
        CreateOccupancyTypeSchema,
    )

    # Check if one already exists
    uc = OccupancyTypeUseCase()
    all_types = uc.list_all()
    items = all_types.data if isinstance(all_types.data, list) else []
    active_items = [t for t in items if t.get("is_active", True) and not t.get("deleted_at")]
    if active_items:
        return active_items[0]["id"]

    result = uc.create(CreateOccupancyTypeSchema(
        name=f"Owner OT {uuid.uuid4().hex[:6]}",
        code="owner_ot",
    ))
    return result.data["id"]


# ═════════════════════════════════════════════════════════════════════════════
# User Profiles
# ═════════════════════════════════════════════════════════════════════════════

class TestUserProfileIntegration:
    """Create, read, update user profiles via UserProfileUseCase."""

    def test_create_profile(self, db_session):
        sb = _make_minimal_sandbox(db_session, "PRF Create")
        from library.dddpy.core_user_profiles.usecase.user_profile_usecase import UserProfileUseCase
        from library.dddpy.core_user_profiles.usecase.user_profile_cmd_schema import CreateUserProfileSchema

        uc = UserProfileUseCase()
        result = uc.create(CreateUserProfileSchema(
            user_id=sb.users[0].id,
            first_name=f"Naruto_{sb.tag}",
            last_name="Uzumaki",
        ))
        assert result.success
        data = result.data
        assert data["first_name"] == f"Naruto_{sb.tag}"
        _teardown(db_session, sb)

    def test_get_and_update_profile(self, db_session):
        sb = _make_minimal_sandbox(db_session, "PRF Update")
        from library.dddpy.core_user_profiles.usecase.user_profile_usecase import UserProfileUseCase
        from library.dddpy.core_user_profiles.usecase.user_profile_cmd_schema import (
            CreateUserProfileSchema,
            UpdateUserProfileSchema,
        )

        uc = UserProfileUseCase()
        uc.create(CreateUserProfileSchema(
            user_id=sb.users[0].id, first_name="Sakura", last_name="Haruno",
        ))

        fetched = uc.get_by_user_id(sb.users[0].id)
        assert fetched.success
        assert fetched.data["last_name"] == "Haruno"

        updated = uc.update(sb.users[0].id, UpdateUserProfileSchema(
            first_name="Sakura_Updated",
        ))
        assert updated.success
        assert updated.data["first_name"] == "Sakura_Updated"
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Unit Occupancies
# ═════════════════════════════════════════════════════════════════════════════

class TestUnitOccupancyIntegration:
    """Create, read, list, end occupancies via UnitOccupancyUseCase."""

    def test_create_occupancy(self, db_session):
        sb = _make_minimal_sandbox(db_session, "OCC Create")
        ot_id = _ensure_occupancy_type(db_session)

        from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_usecase import UnitOccupancyUseCase
        from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_cmd_schema import CreateUnitOccupancySchema

        uc = UnitOccupancyUseCase()
        result = uc.create(CreateUnitOccupancySchema(
            unit_id=sb.units[0].id,
            user_id=sb.users[0].id,
            occupancy_type_id=ot_id,
            start_date=date.today(),
            is_primary=True,
        ))
        assert result.success
        assert result.data["unit_id"] == sb.units[0].id
        _teardown(db_session, sb)

    def test_list_by_unit(self, db_session):
        sb = _make_minimal_sandbox(db_session, "OCC List")
        ot_id = _ensure_occupancy_type(db_session)

        from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_usecase import UnitOccupancyUseCase
        from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_cmd_schema import CreateUnitOccupancySchema

        uc = UnitOccupancyUseCase()
        uc.create(CreateUnitOccupancySchema(
            unit_id=sb.units[0].id, user_id=sb.users[0].id, occupancy_type_id=ot_id,
            start_date=date.today(), is_primary=True,
        ))
        uc.create(CreateUnitOccupancySchema(
            unit_id=sb.units[0].id, user_id=sb.users[1].id, occupancy_type_id=ot_id,
            start_date=date.today(), is_primary=False,
        ))

        result = uc.list_by_unit(unit_id=sb.units[0].id)
        items = result.data if isinstance(result.data, list) else result.data.get("items", [])
        assert len(items) >= 2
        _teardown(db_session, sb)

    def test_end_occupancy(self, db_session):
        sb = _make_minimal_sandbox(db_session, "OCC End")
        ot_id = _ensure_occupancy_type(db_session)

        from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_usecase import UnitOccupancyUseCase
        from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_cmd_schema import (
            CreateUnitOccupancySchema,
            UpdateUnitOccupancySchema,
        )

        uc = UnitOccupancyUseCase()
        created = uc.create(CreateUnitOccupancySchema(
            unit_id=sb.units[0].id, user_id=sb.users[0].id, occupancy_type_id=ot_id,
            start_date=date.today(), is_primary=True,
        ))
        occ_id = created.data["id"]

        end_date = date.today()
        result = uc.update(occ_id, UpdateUnitOccupancySchema(
            status="historical",
            end_date=end_date,
        ))
        assert result.success
        assert result.data["status"] in ("historical", "inactive")
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Unit Ownerships
# ═════════════════════════════════════════════════════════════════════════════

class TestUnitOwnershipIntegration:
    """Create, read, list ownerships via UnitOwnershipUseCase."""

    def test_create_ownership(self, db_session):
        sb = _make_minimal_sandbox(db_session, "OWN Create")
        from library.dddpy.core_unit_ownerships.usecase.unit_ownership_usecase import UnitOwnershipUseCase
        from library.dddpy.core_unit_ownerships.usecase.unit_ownership_cmd_schema import CreateUnitOwnershipSchema

        uc = UnitOwnershipUseCase()
        result = uc.create(CreateUnitOwnershipSchema(
            unit_id=sb.units[0].id,
            user_id=sb.users[0].id,
            ownership_type="owner",
            ownership_percentage=100.0,
            start_date=date.today(),
        ))
        assert result.success
        assert result.data["ownership_type"] == "owner"
        _teardown(db_session, sb)

    def test_list_by_unit(self, db_session):
        sb = _make_minimal_sandbox(db_session, "OWN List")
        from library.dddpy.core_unit_ownerships.usecase.unit_ownership_usecase import UnitOwnershipUseCase
        from library.dddpy.core_unit_ownerships.usecase.unit_ownership_cmd_schema import CreateUnitOwnershipSchema

        uc = UnitOwnershipUseCase()
        # Create two co-owners (50% each)
        uc.create(CreateUnitOwnershipSchema(
            unit_id=sb.units[0].id, user_id=sb.users[0].id,
            ownership_type="co_owner", ownership_percentage=50.0,
            start_date=date.today(),
        ))
        uc.create(CreateUnitOwnershipSchema(
            unit_id=sb.units[0].id, user_id=sb.users[1].id,
            ownership_type="co_owner", ownership_percentage=50.0,
            start_date=date.today(),
        ))

        result = uc.list_by_unit(unit_id=sb.units[0].id)
        items = result.data if isinstance(result.data, list) else result.data.get("items", [])
        assert len(items) >= 2
        _teardown(db_session, sb)

    def test_percentage_validation(self, db_session):
        sb = _make_minimal_sandbox(db_session, "OWN Valid")
        from library.dddpy.core_unit_ownerships.usecase.unit_ownership_usecase import UnitOwnershipUseCase
        from library.dddpy.core_unit_ownerships.usecase.unit_ownership_cmd_schema import CreateUnitOwnershipSchema

        uc = UnitOwnershipUseCase()
        uc.create(CreateUnitOwnershipSchema(
            unit_id=sb.units[0].id, user_id=sb.users[0].id,
            ownership_type="owner", ownership_percentage=100.0,
            start_date=date.today(),
        ))

        # Try to exceed 100% total — should raise
        from library.dddpy.core_unit_ownerships.domain.unit_ownership_exception import (
            OwnershipPercentageSumExceeded,
        )
        with pytest.raises(OwnershipPercentageSumExceeded):
            uc.create(CreateUnitOwnershipSchema(
                unit_id=sb.units[0].id, user_id=sb.users[1].id,
                ownership_type="co_owner", ownership_percentage=50.0,
                start_date=date.today(),
            ))
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Condominium Roles
# ═════════════════════════════════════════════════════════════════════════════

class TestCondominiumRoleIntegration:
    """Create, read, list, delete condominium roles via CondominiumRoleUseCase."""

    def test_create_role(self, db_session):
        sb = _make_minimal_sandbox(db_session, "ROL Create")
        from library.dddpy.core_condominium_roles.usecase.condominium_role_usecase import (
            CondominiumRoleUseCase,
        )
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )

        uc = CondominiumRoleUseCase()
        result = uc.create(CreateCondominiumRoleSchema(
            condominium_id=sb.condo.id,
            user_id=sb.users[0].id,
            role="board_member",
            status="active",
            scope="condominium",
        ))
        assert result.success
        assert result.data["role"] == "board_member"
        _teardown(db_session, sb)

    def test_list_by_condominium(self, db_session):
        sb = _make_minimal_sandbox(db_session, "ROL List")
        from library.dddpy.core_condominium_roles.usecase.condominium_role_usecase import (
            CondominiumRoleUseCase,
        )
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )

        uc = CondominiumRoleUseCase()
        uc.create(CreateCondominiumRoleSchema(
            condominium_id=sb.condo.id, user_id=sb.users[0].id,
            role="finance_reviewer", status="active", scope="condominium",
        ))

        result = uc.list_by_condominium(condominium_id=sb.condo.id)
        items = result.data if isinstance(result.data, list) else result.data.get("items", [])
        roles = [r["role"] for r in items]
        assert "finance_reviewer" in roles
        _teardown(db_session, sb)

    def test_delete_and_restore_role(self, db_session):
        sb = _make_minimal_sandbox(db_session, "ROL Delete")
        from library.dddpy.core_condominium_roles.usecase.condominium_role_usecase import (
            CondominiumRoleUseCase,
        )
        from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
            CreateCondominiumRoleSchema,
        )

        uc = CondominiumRoleUseCase()
        created = uc.create(CreateCondominiumRoleSchema(
            condominium_id=sb.condo.id, user_id=sb.users[0].id,
            role="security_staff", status="active", scope="condominium",
        ))
        role_id = created.data["id"]

        deleted = uc.delete(role_id)
        assert deleted.success

        restored = uc.restore(role_id)
        assert restored.success
        assert restored.data["role"] == "security_staff"
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Dashboards
# ═════════════════════════════════════════════════════════════════════════════

class TestDashboardIntegration:
    """Read-only dashboard queries via FinanceDashboardUseCase / OperationsDashboardUseCase."""

    def test_finance_dashboard(self, db_session):
        sb = _make_minimal_sandbox(db_session, "DASH Finance")
        from library.dddpy.core_dashboards.usecase.finance_dashboard_usecase import (
            FinanceDashboardUseCase,
        )

        uc = FinanceDashboardUseCase()
        result = uc.get_dashboard(condominium_id=sb.condo.id)

        # Dashboard returns a dict with financial summary keys
        assert isinstance(result, dict)
        # New sandbox has no financial data, so dashboard should be empty but valid
        _teardown(db_session, sb)

    def test_operations_dashboard(self, db_session):
        sb = _make_minimal_sandbox(db_session, "DASH Ops")
        from library.dddpy.core_dashboards.usecase.operations_dashboard_usecase import (
            OperationsDashboardUseCase,
        )

        uc = OperationsDashboardUseCase()
        result = uc.get_dashboard(condominium_id=sb.condo.id)

        assert isinstance(result, dict)
        _teardown(db_session, sb)
