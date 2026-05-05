"""
ArrearsSqlReader — reads arrears from core_accounts_receivable (DBAR).
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func

from library.dddpy.core_arrears.domain.arrears_reader import ArrearsReader, UnitArrears
from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ArrearsSqlReader")


class ArrearsSqlReader(ArrearsReader):
    """
    Implementation that reads arrears from the existing
    core_accounts_receivable table.

    months_in_arrears = count of DISTINCT periods with overdue/pending
    AR for the given unit_id, where due_date < today.
    """

    STATUS_OVERDUE = ("pending", "partial", "overdue")

    def get_arrears(self, unit_id: int) -> UnitArrears:
        today = date.today()

        with session_scope() as session:
            # Count distinct overdue months
            months_count = (
                session.query(func.count(func.distinct(DBAR.period)))
                .filter(DBAR.unit_id == unit_id)
                .filter(DBAR.deleted_at.is_(None))
                .filter(DBAR.status.in_(self.STATUS_OVERDUE))
                .filter(DBAR.due_date < today)
                .scalar()
            ) or 0

            # Sum total overdue amount (amount - paid_amount)
            total_row = (
                session.query(
                    func.coalesce(
                        func.sum(DBAR.amount - DBAR.paid_amount),
                        0,
                    )
                )
                .filter(DBAR.unit_id == unit_id)
                .filter(DBAR.deleted_at.is_(None))
                .filter(DBAR.status.in_(self.STATUS_OVERDUE))
                .filter(DBAR.due_date < today)
                .first()
            )
            total_overdue = Decimal(str(total_row[0])) if total_row else Decimal("0")

            # Oldest overdue period
            oldest = (
                session.query(DBAR.period)
                .filter(DBAR.unit_id == unit_id)
                .filter(DBAR.deleted_at.is_(None))
                .filter(DBAR.status.in_(self.STATUS_OVERDUE))
                .filter(DBAR.due_date < today)
                .order_by(DBAR.period.asc())
                .first()
            )

            return UnitArrears(
                unit_id=unit_id,
                months_in_arrears=months_count,
                total_overdue=total_overdue,
                oldest_period=oldest[0] if oldest else None,
            )
