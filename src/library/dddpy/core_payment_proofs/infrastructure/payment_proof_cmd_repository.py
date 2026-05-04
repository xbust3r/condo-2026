"""
Payment Proof Command Repository Implementation.
"""
from datetime import datetime

from library.dddpy.core_payment_proofs.domain.payment_proof_cmd_repository import (
    PaymentProofCmdRepository,
)
from library.dddpy.core_payment_proofs.domain.payment_proof_data import CreatePaymentProofData
from library.dddpy.core_payment_proofs.infrastructure.dbpayment_proof import DBPaymentProof
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PaymentProofCmdRepository")


class PaymentProofCmdRepositoryImpl(PaymentProofCmdRepository):

    def create(self, data: CreatePaymentProofData) -> int:
        logger.info(
            f"Creating payment proof ar_id={data.ar_id} "
            f"submitted_by={data.submitted_by}"
        )
        with session_scope() as session:
            import uuid as uuid_lib

            db_pp = DBPaymentProof(
                uuid=str(uuid_lib.uuid4()),
                condominium_id=data.condominium_id,
                unit_id=data.unit_id,
                ar_id=data.ar_id,
                submitted_by=data.submitted_by,
                file_url=data.file_url,
                original_filename=data.original_filename,
                file_size_bytes=data.file_size_bytes,
                mime_type=data.mime_type,
                status="pending_review",
            )
            session.add(db_pp)
            session.flush()
            session.refresh(db_pp)
            logger.info(f"Payment proof created id={db_pp.id}")
            return db_pp.id

    def approve(self, proof_id: int, review_data, reviewed_by: int) -> bool:
        logger.info(f"Approving payment proof id={proof_id}")
        with session_scope() as session:
            db_pp = session.query(DBPaymentProof).filter(
                DBPaymentProof.id == proof_id,
                DBPaymentProof.deleted_at.is_(None),
            ).first()
            if not db_pp:
                return False
            db_pp.status = "approved"
            db_pp.bank_name = review_data.bank_name
            db_pp.transaction_code = review_data.transaction_code
            db_pp.notes = review_data.notes
            db_pp.reviewed_by = reviewed_by
            db_pp.reviewed_at = datetime.utcnow()
            session.flush()
            logger.info(f"Payment proof approved id={proof_id}")
            return True

    def reject(self, proof_id: int, rejection_reason: str, reviewed_by: int) -> bool:
        logger.info(f"Rejecting payment proof id={proof_id}")
        with session_scope() as session:
            db_pp = session.query(DBPaymentProof).filter(
                DBPaymentProof.id == proof_id,
                DBPaymentProof.deleted_at.is_(None),
            ).first()
            if not db_pp:
                return False
            db_pp.status = "rejected"
            db_pp.rejection_reason = rejection_reason
            db_pp.reviewed_by = reviewed_by
            db_pp.reviewed_at = datetime.utcnow()
            session.flush()
            logger.info(f"Payment proof rejected id={proof_id}")
            return True

    def link_payment(
        self, proof_id: int, payment_id: int, receipt_id: int
    ) -> bool:
        logger.info(
            f"Linking payment proof id={proof_id} to "
            f"payment_id={payment_id} receipt_id={receipt_id}"
        )
        with session_scope() as session:
            db_pp = session.query(DBPaymentProof).filter(
                DBPaymentProof.id == proof_id,
                DBPaymentProof.deleted_at.is_(None),
            ).first()
            if not db_pp:
                return False
            db_pp.payment_id = payment_id
            db_pp.receipt_id = receipt_id
            session.flush()
            logger.info(f"Payment proof linked id={proof_id}")
            return True

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft-deleting payment proof id={id}")
        with session_scope() as session:
            db_pp = session.query(DBPaymentProof).filter(
                DBPaymentProof.id == id,
                DBPaymentProof.deleted_at.is_(None),
            ).first()
            if not db_pp:
                return False
            db_pp.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Payment proof soft-deleted id={id}")
            return True
