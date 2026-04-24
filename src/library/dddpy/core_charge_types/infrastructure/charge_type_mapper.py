"""
ChargeType Mapper — transforms between DB model and domain entity.
"""
from library.dddpy.core_charge_types.infrastructure.dbcharge_type import DBChargeType
from library.dddpy.core_charge_types.domain.charge_type_entity import ChargeTypeEntity


class ChargeTypeMapper:
    """Mapper para convertir entre DBChargeType y ChargeTypeEntity."""

    @staticmethod
    def to_domain(db_ct: DBChargeType) -> ChargeTypeEntity:
        """Convierte modelo DB a entidad de dominio."""
        return ChargeTypeEntity(
            id=db_ct.id,
            uuid=db_ct.uuid,
            code=db_ct.code,
            name=db_ct.name,
            description=db_ct.description,
            is_global=bool(db_ct.is_global),
            is_active=bool(db_ct.is_active),
            sort_order=db_ct.sort_order,
            created_at=db_ct.created_at,
            updated_at=db_ct.updated_at,
            deleted_at=db_ct.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: ChargeTypeEntity) -> DBChargeType:
        """Convierte entidad de dominio a modelo DB."""
        return DBChargeType(
            id=entity.id,
            uuid=entity.uuid,
            code=entity.code,
            name=entity.name,
            description=entity.description,
            is_global=int(entity.is_global),
            is_active=int(entity.is_active),
            sort_order=entity.sort_order,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
