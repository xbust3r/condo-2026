"""
Factory: PaymentProof.

Creates test payment_proof records directly in the DB via SQLAlchemy.
"""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_payment_proofs.infrastructure.dbpayment_proof import DBPaymentProof


class PaymentProofFactory:
    """Factory for creating test PaymentProof records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        unit_id: int,
        ar_id: int,
        submitted_by: int,
        file_url: str = "/uploads/test-proof.jpg",
        original_filename: str = "comprobante_test.jpg",
        file_size_bytes: int = 245000,
        mime_type: str = "image/jpeg",
        status: str = "pending_review",
        bank_name: str = None,
        transaction_code: str = None,
        rejection_reason: str = None,
        reviewed_by: int = None,
        payment_id: int = None,
        receipt_id: int = None,
        **kwargs,
    ) -> DBPaymentProof:
        db_proof = DBPaymentProof(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            unit_id=unit_id,
            ar_id=ar_id,
            submitted_by=submitted_by,
            file_url=file_url,
            original_filename=original_filename,
            file_size_bytes=file_size_bytes,
            mime_type=mime_type,
            status=status,
            bank_name=bank_name,
            transaction_code=transaction_code,
            rejection_reason=rejection_reason,
            reviewed_by=reviewed_by,
            payment_id=payment_id,
            receipt_id=receipt_id,
            created_at=kwargs.get("created_at", func.now()),
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_proof)
        session.flush()
        session.refresh(db_proof)
        return db_proof
