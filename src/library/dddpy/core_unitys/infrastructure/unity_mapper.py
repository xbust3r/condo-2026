"""
Unity Mapper - Transforma entre DB model y Domain entity.
"""
from library.dddpy.core_unitys.infrastructure.dbunitys import DBUnitys
from library.dddpy.core_unitys.domain.unity_entity import UnityEntity


class UnityMapper:
    """Mapper para convertir entre DBUnitys y UnityEntity."""

    @staticmethod
    def to_domain(db_unity: DBUnitys) -> UnityEntity:
        """Convierte modelo DB a entidad de dominio."""
        return UnityEntity(
            id=db_unity.id,
            uuid=db_unity.uuid,
            building_id=db_unity.building_id,
            unity_type_id=db_unity.unity_type_id,
            unit_number=db_unity.unit_number,
            code=db_unity.code,
            name=db_unity.name,
            description=db_unity.description,
            private_area=db_unity.private_area,
            coefficient=db_unity.coefficient,
            floor_number=db_unity.floor_number,
            floor_label=db_unity.floor_label,
            occupancy_status=db_unity.occupancy_status,
            sort_order=db_unity.sort_order,
            status=db_unity.status,
            created_at=db_unity.created_at,
            updated_at=db_unity.updated_at,
            deleted_at=db_unity.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: UnityEntity) -> DBUnitys:
        """Convierte entidad de dominio a modelo DB."""
        return DBUnitys(
            id=entity.id,
            uuid=entity.uuid,
            building_id=entity.building_id,
            unity_type_id=entity.unity_type_id,
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
