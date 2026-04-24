"""
Receipt Mapper — transforms between DB model and domain entity.
"""
from library.dddpy.core_receipts.infrastructure.dbreceipt import DBReceipt
from library.dddpy.core_receipts.domain.receipt_entity import ReceiptEntity


class ReceiptMapper:
    """Mapper para convertir entre DBReceipt y ReceiptEntity."""

    @staticmethod
    def to_domain(db_r: DBReceipt) -> ReceiptEntity:
        """Convierte modelo DB a entidad de dominio."""
        return ReceiptEntity(
            id=db_r.id,
            uuid=db_r.uuid,
            condominium_id=db_r.condominium_id,
            unit_id=db_r.unit_id,
            ar_id=db_r.ar_id,
            receipt_number=db_r.receipt_number,
            issued_at=db_r.issued_at,
            payer_user_id=db_r.payer_user_id,
            amount_paid=db_r.amount_paid,
            payment_method=db_r.payment_method,
            reference=db_r.reference,
            notes=db_r.notes,
            created_at=db_r.created_at,
            updated_at=db_r.updated_at,
        )

    @staticmethod
    def to_infrastructure(entity: ReceiptEntity) -> DBReceipt:
        """Convierte entidad de dominio a modelo DB."""
        return DBReceipt(
            id=entity.id,
            uuid=entity.uuid,
            condominium_id=entity.condominium_id,
            unit_id=entity.unit_id,
            ar_id=entity.ar_id,
            receipt_number=entity.receipt_number,
            issued_at=entity.issued_at,
            payer_user_id=entity.payer_user_id,
            amount_paid=entity.amount_paid,
            payment_method=entity.payment_method,
            reference=entity.reference,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
