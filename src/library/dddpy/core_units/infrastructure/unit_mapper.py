"""
Unit Mapper - Transforma entre DB model y Domain entity.
"""
from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from library.dddpy.core_units.domain.unit_entity import UnitEntity


class UnitMapper:
    """Mapper para convertir entre DBUnits y UnitEntity."""

    @staticmethod
    def to_domain(db_unit: DBUnits) -> UnitEntity:
        """Convierte modelo DB a entidad de dominio."""
        return UnitEntity(
            id=db_unit.id,
            uuid=db_unit.uuid,
            building_id=db_unit.building_id,
            unit_type_id=db_unit.unit_type_id,
            unit_number=db_unit.unit_number,
            code=db_unit.code,
            name=db_unit.name,
            description=db_unit.description,
            private_area=db_unit.private_area,
            coefficient=db_unit.coefficient,
            floor_number=db_unit.floor_number,
            floor_label=db_unit.floor_label,
            occupancy_status=db_unit.occupancy_status,
            sort_order=db_unit.sort_order,
            status=db_unit.status,
            created_at=db_unit.created_at,
            updated_at=db_unit.updated_at,
            deleted_at=db_unit.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: UnitEntity) -> DBUnits:
        """Convierte entidad de dominio a modelo DB."""
        return DBUnits(
            id=entity.id,
            uuid=entity.uuid,
            building_id=entity.building_id,
            unit_type_id=entity.unit_type_id,
            unit_number=entity.unit_number,
            code=entity.code,
            name=entity.name,
            description=entity.description,
            private_area=entity.private_area,
            coefficient=entity.coefficient,
            floor_number=entity.floor_number,
            floor_label=entity.floor_label,
            occupancy_status=entity.occupancy_status,
            sort_order=entity.sort_order,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )