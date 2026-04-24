"""
from typing import Optional
Receipt query repository implementation — SQLAlchemy.
"""
from typing import List, Optional, Tuple

from library.dddpy.core_receipts.domain.receipt_query_repository import ReceiptQueryRepository
from library.dddpy.core_receipts.domain.receipt_entity import ReceiptEntity
from library.dddpy.core_receipts.infrastructure.dbreceipt import DBReceipt
from library.dddpy.core_receipts.infrastructure.receipt_mapper import ReceiptMapper
from library.dddpy.core_users.infrastructure.dbuser import DBUser
from library.dddpy.core_units.infrastructure.dbunits import DBUnits as DBUnit
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ReceiptQueryRepository")


class ReceiptQueryRepositoryImpl(ReceiptQueryRepository):

    def __init__(self):
        logger.info("ReceiptQueryRepositoryImpl initialized")

    def _enrich(self, db_r: DBReceipt, db_user=None, db_unit=None,
                 db_condo=None, db_ar=None) -> ReceiptEntity:
        entity = ReceiptMapper.to_domain(db_r)
        if db_user:
            entity.payer_name = f"{db_user.first_name} {db_user.last_name}".strip()
            entity.payer_email = getattr(db_user, 'email', None)
        if db_unit:
            entity.unit_code = db_unit.code
        if db_condo:
            entity.condominium_name = db_condo.name
        if db_ar:
            entity.ar_reference = db_ar.reference_code
        return entity

    def _bulk_enrich(self, rows: List[DBReceipt]) -> List[ReceiptEntity]:
        if not rows:
            return []
        user_ids = list({r.payer_user_id for r in rows})
        unit_ids = list({r.unit_id for r in rows})
        condo_ids = list({r.condominium_id for r in rows})
        ar_ids = list({r.ar_id for r in rows})
        with session_scope() as session:
            users = {u.id: u for u in session.query(DBUser).filter(DBUser.id.in_(user_ids)).all()}
            units = {u.id: u for u in session.query(DBUnit).filter(DBUnit.id.in_(unit_ids)).all()}
            condos = {c.id: c for c in session.query(DBCondominium).filter(DBCondominium.id.in_(condo_ids)).all()}
            ars = {a.id: a for a in session.query(DBAR).filter(DBAR.id.in_(ar_ids)).all()}
            return [
                self._enrich(
                    row,
                    db_user=users.get(row.payer_user_id),
                    db_unit=units.get(row.unit_id),
                    db_condo=condos.get(row.condominium_id),
                    db_ar=ars.get(row.ar_id),
                )
                for row in rows
            ]

    def get_by_id(self, id: int) -> Optional[ReceiptEntity]:
        logger.info(f"Fetching receipt by id={id}")
        with session_scope() as session:
            row = session.query(DBReceipt).filter(DBReceipt.id == id).first()
            if not row:
                return None
            user = session.query(DBUser).filter(DBUser.id == row.payer_user_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            ar = session.query(DBAR).filter(DBAR.id == row.ar_id).first()
            return self._enrich(row, user, unit, condo, ar)

    def get_by_uuid(self, uuid: str) -> Optional[ReceiptEntity]:
        logger.info(f"Fetching receipt by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBReceipt).filter(DBReceipt.uuid == uuid).first()
            if not row:
                return None
            user = session.query(DBUser).filter(DBUser.id == row.payer_user_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            ar = session.query(DBAR).filter(DBAR.id == row.ar_id).first()
            return self._enrich(row, user, unit, condo, ar)

    def get_by_receipt_number(self, receipt_number: str) -> Optional[ReceiptEntity]:
        logger.info(f"Fetching receipt by number={receipt_number}")
        with session_scope() as session:
            row = session.query(DBReceipt).filter(DBReceipt.receipt_number == receipt_number).first()
            if not row:
                return None
            user = session.query(DBUser).filter(DBUser.id == row.payer_user_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            ar = session.query(DBAR).filter(DBAR.id == row.ar_id).first()
            return self._enrich(row, user, unit, condo, ar)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        ar_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ReceiptEntity], int]:
        logger.info(f"Listing receipts skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBReceipt)
            if condominium_id is not None:
                query = query.filter(DBReceipt.condominium_id == condominium_id)
            if unit_id is not None:
                query = query.filter(DBReceipt.unit_id == unit_id)
            if ar_id is not None:
                query = query.filter(DBReceipt.ar_id == ar_id)
            total = query.count()
            rows = query.order_by(DBReceipt.issued_at.desc()).offset(skip).limit(limit).all()
            return self._bulk_enrich(rows), total

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[ReceiptEntity], int]:
        return self.list_all(skip=skip, limit=limit, unit_id=unit_id)
