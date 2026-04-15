"""
UnitOccupancy Mapper - Transforma entre DB model y Domain entity.
"""
from library.dddpy.core_unit_occupancies.infrastructure.dbunit_occupancy import DBUnitOccupancy
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity


class UnitOccupancyMapper:
    """Mapper para convertir entre DBUnitOccupancy y UnitOccupancyEntity."""

    @staticmethod
    def to_domain(db_occupancy: DBUnitOccupancy) -> UnitOccupancyEntity:
        """Convierte modelo DB a entidad de dominio."""
        return UnitOccupancyEntity(
            id=db_occupancy.id,
            uuid=db_occupancy.uuid,
            unit_id=db_occupancy.unit_id,
            user_id=db_occupancy.user_id,
            occupancy_type=db_occupancy.occupancy_type,
            status=db_occupancy.status,
            start_date=db_occupancy.start_date,
            end_date=db_occupancy.end_date,
            is_primary=db_occupancy.is_primary,
            authorized_by_user_id=db_occupancy.authorized_by_user_id,
            notes=db_occupancy.notes,
            created_at=db_occupancy.created_at,
            updated_at=db_occupancy.updated_at,
            deleted_at=db_occupancy.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: UnitOccupancyEntity) -> DBUnitOccupancy:
        """Convierte entidad de dominio a modelo DB."""
        return DBUnitOccupancy(
            id=entity.id,
            uuid=entity.uuid,
            unit_id=entity.unit_id,
            user_id=entity.user_id,
            occupancy_type=entity.occupancy_type,
            status=entity.status,
            start_date=entity.start_date,
            end_date=entity.end_date,
            is_primary=entity.is_primary,
            authorized_by_user_id=entity.authorized_by_user_id,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
