"""
UnitOwnership Mapper — transforms between DB model and domain entity.
"""
from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity


class UnitOwnershipMapper:
    """Mapper para convertir entre DBUnitOwnership y UnitOwnershipEntity."""

    @staticmethod
    def to_domain(db_ownership: DBUnitOwnership) -> UnitOwnershipEntity:
        """Convierte modelo DB a entidad de dominio."""
        return UnitOwnershipEntity(
            id=db_ownership.id,
            uuid=db_ownership.uuid,
            unit_id=db_ownership.unit_id,
            user_id=db_ownership.user_id,
            ownership_type=db_ownership.ownership_type,
            ownership_percentage=db_ownership.ownership_percentage,
            status=db_ownership.status,
            start_date=db_ownership.start_date,
            end_date=db_ownership.end_date,
            notes=db_ownership.notes,
            created_at=db_ownership.created_at,
            updated_at=db_ownership.updated_at,
            deleted_at=db_ownership.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        db_ownership: DBUnitOwnership,
        unit_code: str = None,
        building_name: str = None,
        condominium_name: str = None,
        user_email: str = None,
        user_full_name: str = None,
    ) -> UnitOwnershipEntity:
        """Convierte modelo DB a entidad de dominio con datos enriquecidos de join."""
        entity = UnitOwnershipMapper.to_domain(db_ownership)
        entity.unit_code = unit_code
        entity.building_name = building_name
        entity.condominium_name = condominium_name
        entity.user_email = user_email
        entity.user_full_name = user_full_name
        return entity

    @staticmethod
    def to_infrastructure(entity: UnitOwnershipEntity) -> DBUnitOwnership:
        """Convierte entidad de dominio a modelo DB."""
        return DBUnitOwnership(
            id=entity.id,
            uuid=entity.uuid,
            unit_id=entity.unit_id,
            user_id=entity.user_id,
            ownership_type=entity.ownership_type,
            ownership_percentage=entity.ownership_percentage,
            status=entity.status,
            start_date=entity.start_date,
            end_date=entity.end_date,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
