"""
Receipt command repository implementation — SQLAlchemy.
"""
from datetime import datetime
from typing import Optional
import uuid as uuid_lib

from sqlalchemy.exc import IntegrityError

from library.dddpy.core_receipts.domain.receipt_cmd_repository import ReceiptCmdRepository
from library.dddpy.core_receipts.domain.receipt_data import CreateReceiptData
from library.dddpy.core_receipts.domain.receipt_entity import ReceiptEntity
from library.dddpy.core_receipts.domain.receipt_exception import ReceiptNumberAlreadyExists
from library.dddpy.core_receipts.infrastructure.dbreceipt import DBReceipt
from library.dddpy.core_receipts.infrastructure.receipt_mapper import ReceiptMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ReceiptCmdRepository")


class ReceiptCmdRepositoryImpl(ReceiptCmdRepository):

    def __init__(self):
        logger.info("ReceiptCmdRepositoryImpl initialized")

    def get_next_receipt_number(self, condominium_id: int) -> str:
        """Generate next sequential receipt number: C{condo_id}-{YYYY}{MM}-{correlativo:06d}."""
        with session_scope() as session:
            from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
            condo = session.query(DBCondominium).filter(DBCondominium.id == condominium_id).first()
            condo_code = condo.code if condo else str(condominium_id)

            now = datetime.utcnow()
            year_month = now.strftime("%Y%m")

            # Get max correlativo for this condo + year-month
            prefix = f"C{condo_code}-{year_month}-"
            result = session.execute(
                __import__('sqlalchemy').text(
                    "SELECT MAX(CAST(SUBSTRING(receipt_number, :prefix_len + 1) AS UNSIGNED)) "
                    "FROM core_receipts WHERE receipt_number LIKE :prefix"
                ),
                {"prefix": f"{prefix}%", "prefix_len": len(prefix)}
            )
            row = result.fetchone()
            next_seq = (row[0] or 0) + 1
            return f"{prefix}{next_seq:06d}"

    def create(self, data: CreateReceiptData) -> ReceiptEntity:
        logger.info(f"Creating receipt for ar_id={data.ar_id}")
        try:
            with session_scope() as session:
                db_r = DBReceipt(
                    uuid=str(uuid_lib.uuid4()),
                    condominium_id=data.condominium_id,
                    unit_id=data.unit_id,
                    ar_id=data.ar_id,
                    receipt_number=data.receipt_number,
                    issued_at=data.issued_at,
                    payer_user_id=data.payer_user_id,
                    amount_paid=data.amount_paid,
                    payment_method=data.payment_method,
                    reference=data.reference,
                    notes=data.notes,
                )
                session.add(db_r)
                session.flush()
                session.refresh(db_r)
                logger.info(f"Receipt created with id={db_r.id}, number={db_r.receipt_number}")
                return ReceiptMapper.to_domain(db_r)

        except IntegrityError:
            logger.warning(f"Receipt number already exists: {data.receipt_number}")
            raise ReceiptNumberAlreadyExists()
