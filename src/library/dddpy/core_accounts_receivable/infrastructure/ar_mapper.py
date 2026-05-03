"""
AccountsReceivable Mapper — transforms between DB model and domain entity.
"""
from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
from library.dddpy.core_accounts_receivable.domain.ar_entity import AREntity


class ARMapper:
    """Mapper para convertir entre DBAR y AREntity."""

    @staticmethod
    def to_domain(db_ar: DBAR) -> AREntity:
        """Convierte modelo DB a entidad de dominio."""
        return AREntity(
            id=db_ar.id,
            uuid=db_ar.uuid,
            condominium_id=db_ar.condominium_id,
            unit_id=db_ar.unit_id,
            debtor_user_id=db_ar.debtor_user_id,
            reference_code=db_ar.reference_code,
            description=db_ar.description,
            amount=db_ar.amount,
            paid_amount=db_ar.paid_amount,
            currency=db_ar.currency,
            status=db_ar.status,
            due_date=db_ar.due_date,
            period=db_ar.period,
            charge_id=db_ar.charge_id,
            origin_type=db_ar.origin_type,
            origin_id=db_ar.origin_id,
            created_at=db_ar.created_at,
            updated_at=db_ar.updated_at,
            deleted_at=db_ar.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: AREntity) -> DBAR:
        """Convierte entidad de dominio a modelo DB."""
        return DBAR(
            id=entity.id,
            uuid=entity.uuid,
            condominium_id=entity.condominium_id,
            unit_id=entity.unit_id,
            debtor_user_id=entity.debtor_user_id,
            reference_code=entity.reference_code,
            description=entity.description,
            amount=entity.amount,
            paid_amount=entity.paid_amount,
            currency=entity.currency,
            status=entity.status,
            due_date=entity.due_date,
            period=entity.period,
            charge_id=entity.charge_id,
            origin_type=entity.origin_type,
            origin_id=entity.origin_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
