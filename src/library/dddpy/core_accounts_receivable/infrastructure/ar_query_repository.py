"""
AccountsReceivable query repository implementation — SQLAlchemy.
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy import func, and_

from library.dddpy.core_accounts_receivable.domain.ar_query_repository import ARQueryRepository
from library.dddpy.core_accounts_receivable.domain.ar_entity import AREntity
from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
from library.dddpy.core_accounts_receivable.infrastructure.ar_mapper import ARMapper
from library.dddpy.core_users.infrastructure.dbuser import DBUser
from library.dddpy.core_units.infrastructure.dbunits import DBUnits as DBUnit
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
from library.dddpy.core_charges.infrastructure.dbcharges import DBCharges as DBCharge
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ARQueryRepository")


class ARQueryRepositoryImpl(ARQueryRepository):

    def __init__(self):
        logger.info("ARQueryRepositoryImpl initialized")

    def _enrich(self, db_ar: DBAR, db_user=None, db_unit=None,
                 db_condo=None, db_charge=None) -> AREntity:
        """Apply enrichment to an AR entity."""
        entity = ARMapper.to_domain(db_ar)
        if db_user:
            entity.debtor_name = f"{db_user.first_name} {db_user.last_name}".strip()
            entity.debtor_email = getattr(db_user, 'email', None)
        if db_unit:
            entity.unit_code = db_unit.code
        if db_condo:
            entity.condominium_name = db_condo.name
        if db_charge:
            entity.charge_description = db_charge.description
        return entity

    def _bulk_enrich(self, rows: List[DBAR]) -> List[AREntity]:
        """Bulk-enrich AR rows with related data."""
        if not rows:
            return []

        user_ids = list({r.debtor_user_id for r in rows})
        unit_ids = list({r.unit_id for r in rows})
        condo_ids = list({r.condominium_id for r in rows})
        charge_ids = [r.charge_id for r in rows if r.charge_id]

        with session_scope() as session:
            users = {u.id: u for u in session.query(DBUser).filter(DBUser.id.in_(user_ids)).all()}
            units = {u.id: u for u in session.query(DBUnit).filter(DBUnit.id.in_(unit_ids)).all()}
            condos = {c.id: c for c in session.query(DBCondominium).filter(DBCondominium.id.in_(condo_ids)).all()}
            charges = {}
            if charge_ids:
                charges = {c.id: c for c in session.query(DBCharge).filter(DBCharge.id.in_(charge_ids)).all()}

            return [
                self._enrich(
                    row,
                    db_user=users.get(row.debtor_user_id),
                    db_unit=units.get(row.unit_id),
                    db_condo=condos.get(row.condominium_id),
                    db_charge=charges.get(row.charge_id) if row.charge_id else None,
                )
                for row in rows
            ]

    def get_by_id(self, id: int) -> Optional[AREntity]:
        logger.info(f"Fetching AR by id={id}")
        with session_scope() as session:
            row = session.query(DBAR).filter(
                DBAR.id == id,
                DBAR.deleted_at.is_(None),
            ).first()
            if not row:
                logger.warning(f"AR not found by id={id}")
                return None

            user = session.query(DBUser).filter(DBUser.id == row.debtor_user_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            charge = session.query(DBCharge).filter(DBCharge.id == row.charge_id).first() if row.charge_id else None
            return self._enrich(row, user, unit, condo, charge)

    def get_by_uuid(self, uuid: str) -> Optional[AREntity]:
        logger.info(f"Fetching AR by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBAR).filter(
                DBAR.uuid == uuid,
                DBAR.deleted_at.is_(None),
            ).first()
            if not row:
                logger.warning(f"AR not found by uuid={uuid}")
                return None

            user = session.query(DBUser).filter(DBUser.id == row.debtor_user_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            charge = session.query(DBCharge).filter(DBCharge.id == row.charge_id).first() if row.charge_id else None
            return self._enrich(row, user, unit, condo, charge)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        debtor_user_id: Optional[int] = None,
        status: Optional[str] = None,
        charge_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[AREntity], int]:
        logger.info(f"Listing AR entries skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBAR)

            if not include_deleted:
                query = query.filter(DBAR.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBAR.condominium_id == condominium_id)
            if unit_id is not None:
                query = query.filter(DBAR.unit_id == unit_id)
            if debtor_user_id is not None:
                query = query.filter(DBAR.debtor_user_id == debtor_user_id)
            if status is not None:
                query = query.filter(DBAR.status == status)
            if charge_id is not None:
                query = query.filter(DBAR.charge_id == charge_id)

            total = query.count()
            rows = (
                query
                .order_by(DBAR.due_date.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(rows), total

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[AREntity], int]:
        return self.list_all(
            skip=skip,
            limit=limit,
            unit_id=unit_id,
            status=status,
            include_deleted=include_deleted,
        )

    def list_overdue(
        self,
        condominium_id: int,
        as_of_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AREntity], int]:
        check_date = as_of_date or date.today()
        logger.info(f"Listing overdue ARs for condominium={condominium_id} as_of={check_date}")
        with session_scope() as session:
            query = session.query(DBAR).filter(
                and_(
                    DBAR.condominium_id == condominium_id,
                    DBAR.deleted_at.is_(None),
                    DBAR.status.in_("pending", "partial"),
                    DBAR.due_date < check_date,
                    DBAR.amount > DBAR.paid_amount,
                )
            )
            total = query.count()
            rows = (
                query
                .order_by(DBAR.due_date.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(rows), total

    def get_summary_by_unit(self, unit_id: int) -> dict:
        logger.info(f"Getting AR summary for unit_id={unit_id}")
        with session_scope() as session:
            rows = session.query(DBAR).filter(
                and_(
                    DBAR.unit_id == unit_id,
                    DBAR.deleted_at.is_(None),
                )
            ).all()

            total_debt = Decimal("0.00")
            pending_sum = Decimal("0.00")
            overdue_count = 0
            today = date.today()

            for r in rows:
                total_debt += r.amount
                pending = r.amount - r.paid_amount
                if pending > 0:
                    pending_sum += pending
                if r.status in ("pending", "partial") and r.due_date < today and pending > 0:
                    overdue_count += 1

            return {
                "unit_id": unit_id,
                "total_debt": float(total_debt),
                "total_pending": float(pending_sum),
                "overdue_count": overdue_count,
            }

    def _get_by_id_any_status(self, id: int) -> Optional[AREntity]:
        """Re-fetch entity ignoring soft-delete filter."""
        logger.info(f"Fetching AR by id={id} (any status)")
        with session_scope() as session:
            row = session.query(DBAR).filter(DBAR.id == id).first()
            if not row:
                logger.warning(f"AR not found by id={id}")
                return None
            return ARMapper.to_domain(row)

    def get_summary_by_condominium(self, condominium_id: int) -> dict:
        """
        Compute financial summary for all AR in a condominium.

        Returns:
          - total_debt:      sum of all AR amounts
          - total_pending:    sum of (amount - paid_amount) for non-paid AR
          - overdue_count:   count of overdue AR entries
          - overdue_amount:  sum of pending for overdue AR
          - overdue_30_days: count of overdue AR where due_date < today - 30 days
        """
        logger.info(f"Computing AR summary for condominium_id={condominium_id}")
        with session_scope() as session:
            cutoff_30 = date.today()

            rows = session.query(DBAR).filter(
                and_(
                    DBAR.condominium_id == condominium_id,
                    DBAR.deleted_at.is_(None),
                )
            ).all()

            total_debt = Decimal("0.00")
            total_pending = Decimal("0.00")
            overdue_count = 0
            overdue_amount = Decimal("0.00")
            overdue_30_count = 0
            today = date.today()
            from datetime import timedelta
            cutoff_30_days = today - timedelta(days=30)

            for r in rows:
                total_debt += r.amount
                pending = r.amount - r.paid_amount
                if r.status != "paid" and r.status != "cancelled" and pending > 0:
                    total_pending += pending
                if r.status in ("pending", "partial", "overdue") and r.due_date < today and pending > 0:
                    overdue_count += 1
                    overdue_amount += pending
                    if r.due_date < cutoff_30_days:
                        overdue_30_count += 1

            return {
                "condominium_id": condominium_id,
                "total_debt": float(total_debt),
                "total_pending": float(total_pending),
                "overdue_count": overdue_count,
                "overdue_amount": float(overdue_amount),
                "overdue_30_days_count": overdue_30_count,
            }
