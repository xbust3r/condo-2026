"""
OccupancyType Mapper — transforms between DB model and Domain entity.
"""
from library.dddpy.core_occupancy_types.infrastructure.dboccupancy_type import DBOccupancyType
from library.dddpy.core_occupancy_types.domain.occupancy_type_entity import OccupancyTypeEntity


class OccupancyTypeMapper:
    """Mapper para convertir entre DBOccupancyType y OccupancyTypeEntity."""

    @staticmethod
    def to_domain(db_ot: DBOccupancyType) -> OccupancyTypeEntity:
        return OccupancyTypeEntity(
            id=db_ot.id,
            uuid=db_ot.uuid,
            code=db_ot.code,
            name=db_ot.name,
            description=db_ot.description,
            scope=db_ot.scope or "system",
            condominium_id=db_ot.condominium_id,
            requires_authorization=bool(db_ot.requires_authorization),
            allows_primary=bool(db_ot.allows_primary),
            is_active=bool(db_ot.is_active),
            sort_order=db_ot.sort_order,
            created_at=db_ot.created_at,
            updated_at=db_ot.updated_at,
            deleted_at=db_ot.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: OccupancyTypeEntity) -> DBOccupancyType:
        return DBOccupancyType(
            id=entity.id,
            uuid=entity.uuid,
            code=entity.code,
            name=entity.name,
            description=entity.description,
            scope=entity.scope,
            condominium_id=entity.condominium_id,
            requires_authorization=int(entity.requires_authorization),
            allows_primary=int(entity.allows_primary),
            is_active=int(entity.is_active),
            sort_order=entity.sort_order,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )