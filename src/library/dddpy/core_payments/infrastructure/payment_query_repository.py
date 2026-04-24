"""
Payment query repository implementation — SQLAlchemy.
"""
from typing import List, Optional, Tuple

from library.dddpy.core_payments.domain.payment_query_repository import PaymentQueryRepository
from library.dddpy.core_payments.domain.payment_entity import PaymentEntity
from library.dddpy.core_payments.infrastructure.dbpayment import DBPayment
from library.dddpy.core_payments.infrastructure.payment_mapper import PaymentMapper
from library.dddpy.core_users.infrastructure.dbuser import DBUser
from library.dddpy.core_units.infrastructure.dbunits import DBUnits as DBUnit
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
from library.dddpy.core_receipts.infrastructure.dbreceipt import DBReceipt
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PaymentQueryRepository")


class PaymentQueryRepositoryImpl(PaymentQueryRepository):

    def __init__(self):
        logger.info("PaymentQueryRepositoryImpl initialized")

    def _enrich(self, db_p: DBPayment, db_user=None, db_unit=None,
                db_condo=None, db_receipt=None) -> PaymentEntity:
        entity = PaymentMapper.to_domain(db_p)
        if db_user:
            entity.payer_name = f"{db_user.first_name} {db_user.last_name}".strip()
        if db_unit:
            entity.unit_code = db_unit.code
        if db_condo:
            entity.condominium_name = db_condo.name
        if db_receipt:
            entity.receipt_number = db_receipt.receipt_number
        return entity

    def _bulk_enrich(self, rows: List[DBPayment]) -> List[PaymentEntity]:
        if not rows:
            return []
        user_ids = list({r.payer_user_id for r in rows})
        unit_ids = list({r.unit_id for r in rows})
        condo_ids = list({r.condominium_id for r in rows})
        receipt_ids = [r.receipt_id for r in rows if r.receipt_id]
        with session_scope() as session:
            users = {u.id: u for u in session.query(DBUser).filter(DBUser.id.in_(user_ids)).all()}
            units = {u.id: u for u in session.query(DBUnit).filter(DBUnit.id.in_(unit_ids)).all()}
            condos = {c.id: c for c in session.query(DBCondominium).filter(DBCondominium.id.in_(condo_ids)).all()}
            receipts = {}
            if receipt_ids:
                receipts = {r.id: r for r in session.query(DBReceipt).filter(DBReceipt.id.in_(receipt_ids)).all()}
            return [
                self._enrich(
                    row,
                    db_user=users.get(row.payer_user_id),
                    db_unit=units.get(row.unit_id),
                    db_condo=condos.get(row.condominium_id),
                    db_receipt=receipts.get(row.receipt_id) if row.receipt_id else None,
                )
                for row in rows
            ]

    def get_by_id(self, id: int) -> Optional[PaymentEntity]:
        logger.info(f"Fetching payment by id={id}")
        with session_scope() as session:
            row = session.query(DBPayment).filter(DBPayment.id == id).first()
            if not row:
                return None
            user = session.query(DBUser).filter(DBUser.id == row.payer_user_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            receipt = session.query(DBReceipt).filter(DBReceipt.id == row.receipt_id).first() if row.receipt_id else None
            return self._enrich(row, user, unit, condo, receipt)

    def get_by_uuid(self, uuid: str) -> Optional[PaymentEntity]:
        logger.info(f"Fetching payment by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBPayment).filter(DBPayment.uuid == uuid).first()
            if not row:
                return None
            user = session.query(DBUser).filter(DBUser.id == row.payer_user_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            receipt = session.query(DBReceipt).filter(DBReceipt.id == row.receipt_id).first() if row.receipt_id else None
            return self._enrich(row, user, unit, condo, receipt)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        ar_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[PaymentEntity], int]:
        logger.info(f"Listing payments skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBPayment)
            if not include_deleted:
                query = query.filter(DBPayment.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBPayment.condominium_id == condominium_id)
            if unit_id is not None:
                query = query.filter(DBPayment.unit_id == unit_id)
            if ar_id is not None:
                query = query.filter(DBPayment.ar_id == ar_id)
            total = query.count()
            rows = query.order_by(DBPayment.paid_at.desc()).offset(skip).limit(limit).all()
            return self._bulk_enrich(rows), total
