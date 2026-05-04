"""
Payment Proof mapper.
"""
from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
from library.dddpy.core_payment_proofs.infrastructure.dbpayment_proof import DBPaymentProof


class PaymentProofMapper:
    @staticmethod
    def to_domain(row: DBPaymentProof) -> PaymentProofEntity:
        return PaymentProofEntity(
            id=row.id,
            uuid=row.uuid,
            condominium_id=row.condominium_id,
            unit_id=row.unit_id,
            ar_id=row.ar_id,
            submitted_by=row.submitted_by,
            file_url=row.file_url,
            original_filename=row.original_filename,
            file_size_bytes=row.file_size_bytes,
            mime_type=row.mime_type,
            bank_name=row.bank_name,
            transaction_code=row.transaction_code,
            notes=row.notes,
            status=row.status,
            reviewed_by=row.reviewed_by,
            reviewed_at=row.reviewed_at,
            rejection_reason=row.rejection_reason,
            payment_id=row.payment_id,
            receipt_id=row.receipt_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        row: DBPaymentProof,
        submitted_by_name: str = None,
        reviewed_by_name: str = None,
        unit_code: str = None,
        condominium_name: str = None,
        ar_reference: str = None,
        ar_amount: float = None,
        receipt_number: str = None,
    ) -> PaymentProofEntity:
        entity = PaymentProofMapper.to_domain(row)
        entity.submitted_by_name = submitted_by_name
        entity.reviewed_by_name = reviewed_by_name
        entity.unit_code = unit_code
        entity.condominium_name = condominium_name
        entity.ar_reference = ar_reference
        entity.ar_amount = ar_amount
        entity.receipt_number = receipt_number
        return entity
