"""
Payment Mapper — transforms between DB model and domain entity.
"""
from library.dddpy.core_payments.infrastructure.dbpayment import DBPayment
from library.dddpy.core_payments.domain.payment_entity import PaymentEntity


class PaymentMapper:
    """Mapper para convertir entre DBPayment y PaymentEntity."""

    @staticmethod
    def to_domain(db_p: DBPayment) -> PaymentEntity:
        return PaymentEntity(
            id=db_p.id,
            uuid=db_p.uuid,
            condominium_id=db_p.condominium_id,
            unit_id=db_p.unit_id,
            ar_id=db_p.ar_id,
            receipt_id=db_p.receipt_id,
            payer_user_id=db_p.payer_user_id,
            amount=db_p.amount,
            payment_method=db_p.payment_method,
            reference=db_p.reference,
            paid_at=db_p.paid_at,
            created_at=db_p.created_at,
            updated_at=db_p.updated_at,
            deleted_at=db_p.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: PaymentEntity) -> DBPayment:
        return DBPayment(
            id=entity.id,
            uuid=entity.uuid,
            condominium_id=entity.condominium_id,
            unit_id=entity.unit_id,
            ar_id=entity.ar_id,
            receipt_id=entity.receipt_id,
            payer_user_id=entity.payer_user_id,
            amount=entity.amount,
            payment_method=entity.payment_method,
            reference=entity.reference,
            paid_at=entity.paid_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
