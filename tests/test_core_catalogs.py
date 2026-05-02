"""
Integration tests for catalog modules: building types, charge types,
unit types, and occupancy types.

All catalog modules follow the same CRUD pattern: create, read, list,
update, soft-delete, restore via their composite UseCase classes.

Each test:
  1. Creates a minimal sandbox (for modules that need condominium_id)
  2. Exercises CRUD operations against real MariaDB
  3. Cleans up all records via _cleanup_by_condo()
"""
import uuid
import pytest

from tests.test_core_foundations import _make_minimal_sandbox, _cleanup_by_condo


def _teardown(db_session, sb):
    _cleanup_by_condo(db_session, sb.condo.id)


# ═════════════════════════════════════════════════════════════════════════════
# Building Types
# ═════════════════════════════════════════════════════════════════════════════

class TestBuildingTypeIntegration:
    """CRUD building types via BuildingTypeUseCase."""

    def test_create_and_get(self, db_session):
        sb = _make_minimal_sandbox(db_session, "BT Create")
        from library.dddpy.core_buildings_types.usecase.building_type_usecase import BuildingTypeUseCase
        from library.dddpy.core_buildings_types.usecase.building_type_cmd_schema import CreateBuildingTypeSchema

        uc = BuildingTypeUseCase()
        code = f"bt_{sb.tag[:6]}"
        result = uc.create(CreateBuildingTypeSchema(
            condominium_id=sb.condo.id,
            code=code,
            name=f"Torre Tipo {sb.tag[:6]}",
        ))
        assert result.success
        bt_id = result.data["id"]

        fetched = uc.get_by_id(bt_id)
        assert fetched.success
        assert fetched.data["code"] == code
        _teardown(db_session, sb)

    def test_list_all(self, db_session):
        sb = _make_minimal_sandbox(db_session, "BT List")
        from library.dddpy.core_buildings_types.usecase.building_type_usecase import BuildingTypeUseCase
        from library.dddpy.core_buildings_types.usecase.building_type_cmd_schema import CreateBuildingTypeSchema

        uc = BuildingTypeUseCase()
        uc.create(CreateBuildingTypeSchema(
            condominium_id=sb.condo.id, code=f"a_{sb.tag[:4]}", name=f"Alpha {sb.tag[:4]}",
        ))

        all_types = uc.list_all(condominium_id=sb.condo.id)
        # list_all returns data as flat list or dict with items
        items = all_types.data if isinstance(all_types.data, list) else all_types.data.get("items", [])
        codes = [t["code"] for t in items]
        assert f"a_{sb.tag[:4]}" in codes
        _teardown(db_session, sb)

    def test_soft_delete_and_restore(self, db_session):
        sb = _make_minimal_sandbox(db_session, "BT Delete")
        from library.dddpy.core_buildings_types.usecase.building_type_usecase import BuildingTypeUseCase
        from library.dddpy.core_buildings_types.usecase.building_type_cmd_schema import CreateBuildingTypeSchema

        uc = BuildingTypeUseCase()
        result = uc.create(CreateBuildingTypeSchema(
            condominium_id=sb.condo.id, code=f"del_{sb.tag[:4]}", name=f"ToDelete {sb.tag[:4]}",
        ))
        bt_id = result.data["id"]

        deleted = uc.soft_delete(bt_id)
        assert deleted.success

        restored = uc.restore(bt_id)
        assert restored.success
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Charge Types
# ═════════════════════════════════════════════════════════════════════════════

class TestChargeTypeIntegration:
    """CRUD charge types via ChargeTypeUseCase."""

    def test_create_and_get(self, db_session):
        sb = _make_minimal_sandbox(db_session, "CT Create")
        from library.dddpy.core_charge_types.usecase.charge_type_usecase import ChargeTypeUseCase
        from library.dddpy.core_charge_types.usecase.charge_type_cmd_schema import CreateChargeTypeSchema

        uc = ChargeTypeUseCase()
        code = f"ct_{sb.tag[:6]}"
        result = uc.create(CreateChargeTypeSchema(
            code=code,
            name=f"Cargo {sb.tag[:6]}",
        ))
        assert result.success
        ct_id = result.data["id"]

        fetched = uc.get_by_id(ct_id)
        assert fetched.success
        assert fetched.data["code"] == code
        _teardown(db_session, sb)

    def test_list_all(self, db_session):
        sb = _make_minimal_sandbox(db_session, "CT List")
        from library.dddpy.core_charge_types.usecase.charge_type_usecase import ChargeTypeUseCase
        from library.dddpy.core_charge_types.usecase.charge_type_cmd_schema import CreateChargeTypeSchema

        uc = ChargeTypeUseCase()
        uc.create(CreateChargeTypeSchema(code=f"x_{sb.tag[:4]}", name=f"Extra {sb.tag[:4]}"))

        all_types = uc.list_all()
        items = all_types.data if isinstance(all_types.data, list) else all_types.data.get("items", [])
        codes = [c["code"] for c in items]
        assert f"x_{sb.tag[:4]}" in codes
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Unit Types
# ═════════════════════════════════════════════════════════════════════════════

class TestUnitTypeIntegration:
    """CRUD unit types via UnitTypeUseCase."""

    def test_create_and_get(self, db_session):
        sb = _make_minimal_sandbox(db_session, "UT Create")
        from library.dddpy.core_unit_types.usecase.unit_type_usecase import UnitTypeUseCase
        from library.dddpy.core_unit_types.usecase.unit_type_cmd_schema import CreateUnitTypeSchema

        uc = UnitTypeUseCase()
        code = f"ut_{sb.tag[:6]}"
        result = uc.create(CreateUnitTypeSchema(
            condominium_id=sb.condo.id,
            code=code,
            name=f"Depto {sb.tag[:6]}",
            usage_class="residential",
        ))
        assert result.success
        ut_id = result.data["id"]

        fetched = uc.get_by_id(ut_id)
        assert fetched.success
        assert fetched.data["code"] == code
        _teardown(db_session, sb)

    def test_list_all(self, db_session):
        sb = _make_minimal_sandbox(db_session, "UT List")
        from library.dddpy.core_unit_types.usecase.unit_type_usecase import UnitTypeUseCase
        from library.dddpy.core_unit_types.usecase.unit_type_cmd_schema import CreateUnitTypeSchema

        uc = UnitTypeUseCase()
        uc.create(CreateUnitTypeSchema(
            condominium_id=sb.condo.id, code=f"r_{sb.tag[:4]}", name=f"Residencial {sb.tag[:4]}",
            usage_class="residential",
        ))

        all_types = uc.list_all(condominium_id=sb.condo.id)
        items = all_types.data if isinstance(all_types.data, list) else all_types.data.get("items", [])
        codes = [u["code"] for u in items]
        assert f"r_{sb.tag[:4]}" in codes
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Occupancy Types (catalog)
# ═════════════════════════════════════════════════════════════════════════════

class TestOccupancyTypeIntegration:
    """CRUD occupancy types via OccupancyTypeUseCase."""

    def test_create_and_get(self, db_session):
        sb = _make_minimal_sandbox(db_session, "OT Create")
        from library.dddpy.core_occupancy_types.usecase.occupancy_type_usecase import OccupancyTypeUseCase
        from library.dddpy.core_occupancy_types.usecase.occupancy_type_cmd_schema import CreateOccupancyTypeSchema

        uc = OccupancyTypeUseCase()
        code = f"ot_{sb.tag[:6]}"
        result = uc.create(CreateOccupancyTypeSchema(
            code=code,
            name=f"Ocupante {sb.tag[:6]}",
        ))
        assert result.success
        ot_id = result.data["id"]

        fetched = uc.get_by_id(ot_id)
        assert fetched.success
        assert fetched.data["code"] == code
        _teardown(db_session, sb)

    def test_list_all(self, db_session):
        sb = _make_minimal_sandbox(db_session, "OT List")
        from library.dddpy.core_occupancy_types.usecase.occupancy_type_usecase import OccupancyTypeUseCase
        from library.dddpy.core_occupancy_types.usecase.occupancy_type_cmd_schema import CreateOccupancyTypeSchema

        uc = OccupancyTypeUseCase()
        uc.create(CreateOccupancyTypeSchema(code=f"v_{sb.tag[:4]}", name=f"Visitante {sb.tag[:4]}"))

        all_types = uc.list_all()
        items = all_types.data if isinstance(all_types.data, list) else all_types.data.get("items", [])
        codes = [o["code"] for o in items]
        assert f"v_{sb.tag[:4]}" in codes
        _teardown(db_session, sb)
