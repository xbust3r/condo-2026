"""
Charge Mapper — transforms between DB model and domain entity.
"""
from library.dddpy.core_charges.infrastructure.dbcharges import DBCharges as DBCharge
from library.dddpy.core_charges.domain.charge_entity import ChargeEntity


class ChargeMapper:
    """Mapper para convertir entre DBCharge y ChargeEntity."""

    @staticmethod
    def to_domain(db_c: DBCharge) -> ChargeEntity:
        """Convierte modelo DB a entidad de dominio."""
        return ChargeEntity(
            id=db_c.id,
            uuid=db_c.uuid,
            condominium_id=db_c.condominium_id,
            charge_type_id=db_c.charge_type_id,
            unit_id=db_c.unit_id,
            description=db_c.description,
            amount=db_c.amount,
            currency=db_c.currency,
            is_recurrent=bool(db_c.is_recurrent),
            period_pattern=db_c.period_pattern,
            start_date=db_c.start_date,
            end_date=db_c.end_date,
            status=db_c.status,
            created_at=db_c.created_at,
            updated_at=db_c.updated_at,
            deleted_at=db_c.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: ChargeEntity) -> DBCharge:
        """Convierte entidad de dominio a modelo DB."""
        return DBCharge(
            id=entity.id,
            uuid=entity.uuid,
            condominium_id=entity.condominium_id,
            charge_type_id=entity.charge_type_id,
            unit_id=entity.unit_id,
            description=entity.description,
            amount=entity.amount,
            currency=entity.currency,
            is_recurrent=int(entity.is_recurrent),
            period_pattern=entity.period_pattern,
            start_date=entity.start_date,
            end_date=entity.end_date,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
