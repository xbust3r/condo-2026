"""
Payment command repository implementation — SQLAlchemy.
"""
from typing import Optional
import uuid as uuid_lib

from library.dddpy.core_payments.domain.payment_cmd_repository import PaymentCmdRepository
from library.dddpy.core_payments.domain.payment_data import CreatePaymentData
from library.dddpy.core_payments.domain.payment_entity import PaymentEntity
from library.dddpy.core_payments.infrastructure.dbpayment import DBPayment
from library.dddpy.core_payments.infrastructure.payment_mapper import PaymentMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PaymentCmdRepository")


class PaymentCmdRepositoryImpl(PaymentCmdRepository):

    def __init__(self):
        logger.info("PaymentCmdRepositoryImpl initialized")

    def create(self, data: CreatePaymentData, receipt_id: int) -> PaymentEntity:
        logger.info(f"Creating payment for ar_id={data.ar_id}")
        with session_scope() as session:
            db_p = DBPayment(
                uuid=str(uuid_lib.uuid4()),
                condominium_id=data.condominium_id,
                unit_id=data.unit_id,
                ar_id=data.ar_id,
                receipt_id=receipt_id,
                payer_user_id=data.payer_user_id,
                amount=data.amount,
                payment_method=data.payment_method,
                reference=data.reference,
                paid_at=data.paid_at,
            )
            session.add(db_p)
            session.flush()
            session.refresh(db_p)
            logger.info(f"Payment created with id={db_p.id}")
            return PaymentMapper.to_domain(db_p)
