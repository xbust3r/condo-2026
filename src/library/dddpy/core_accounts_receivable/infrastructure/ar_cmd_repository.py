"""
from typing import Optional
AccountsReceivable command repository implementation — SQLAlchemy.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
import uuid as uuid_lib

from library.dddpy.core_accounts_receivable.domain.ar_cmd_repository import ARCmdRepository
from library.dddpy.core_accounts_receivable.domain.ar_data import (
    CreateARData,
    UpdateARData,
)
from library.dddpy.core_accounts_receivable.domain.ar_entity import AREntity
from library.dddpy.core_accounts_receivable.domain.ar_exception import (
    InvalidARStatusTransition,
    ARPaymentExceedsBalance,
)
from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
from library.dddpy.core_accounts_receivable.infrastructure.ar_mapper import ARMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ARCmdRepository")


class ARCmdRepositoryImpl(ARCmdRepository):

    # Valid status transitions
    VALID_TRANSITIONS = {
        "pending": {"partial", "paid", "overdue", "cancelled"},
        "partial": {"paid", "overdue", "cancelled"},
        "overdue": {"paid", "partial", "cancelled"},
        "paid": set(),
        "cancelled": set(),
    }

    def __init__(self):
        logger.info("ARCmdRepositoryImpl initialized")

    def _can_transition(self, current: str, new: str) -> bool:
        return new in self.VALID_TRANSITIONS.get(current, set())

    def _recalculate_status(self, db_ar: DBAR) -> str:
        """Recalculate AR status based on paid_amount vs amount."""
        pending = db_ar.amount - db_ar.paid_amount
        if pending <= 0:
            return "paid"
        if db_ar.status not in ("pending", "partial", "overdue"):
            return db_ar.status
        if db_ar.due_date < date.today() and pending > 0:
            return "overdue"
        if db_ar.paid_amount > 0:
            return "partial"
        return "pending"

    def create(self, data: CreateARData) -> AREntity:
        logger.info(f"Creating AR for unit={data.unit_id} debtor={data.debtor_user_id}")
        with session_scope() as session:
            db_ar = DBAR(
                uuid=str(uuid_lib.uuid4()),
                condominium_id=data.condominium_id,
                unit_id=data.unit_id,
                debtor_user_id=data.debtor_user_id,
                reference_code=data.reference_code,
                description=data.description,
                amount=data.amount,
                paid_amount=Decimal("0.00"),
                currency=data.currency,
                status="pending",
                due_date=data.due_date,
                period=data.period,
                charge_id=data.charge_id,
            )
            session.add(db_ar)
            session.flush()
            session.refresh(db_ar)
            logger.info(f"AR created with id={db_ar.id}")
            return ARMapper.to_domain(db_ar)

    def create_batch(self, entries: list[CreateARData]) -> list[AREntity]:
        logger.info(f"Creating {len(entries)} AR entries in batch")
        with session_scope() as session:
            db_ars = []
            for data in entries:
                db_ar = DBAR(
                    uuid=str(uuid_lib.uuid4()),
                    condominium_id=data.condominium_id,
                    unit_id=data.unit_id,
                    debtor_user_id=data.debtor_user_id,
                    reference_code=data.reference_code,
                    description=data.description,
                    amount=data.amount,
                    paid_amount=Decimal("0.00"),
                    currency=data.currency,
                    status="pending",
                    due_date=data.due_date,
                    period=data.period,
                    charge_id=data.charge_id,
                )
                db_ars.append(db_ar)
            session.add_all(db_ars)
            session.flush()
            for db_ar in db_ars:
                session.refresh(db_ar)
            logger.info(f"Batch AR created: {len(db_ars)} entries")
            return [ARMapper.to_domain(ar) for ar in db_ars]

    def update(self, id: int, data: UpdateARData) -> Optional[AREntity]:
        logger.info(f"Updating AR id={id}")
        with session_scope() as session:
            db_ar = session.query(DBAR).filter(DBAR.id == id).first()
            if not db_ar:
                logger.warning(f"AR not found for update id={id}")
                return None

            if data.description is not None:
                db_ar.description = data.description
            if data.due_date is not None:
                db_ar.due_date = data.due_date
            if data.status is not None:
                if not self._can_transition(db_ar.status, data.status):
                    raise InvalidARStatusTransition(
                        f"Cannot transition from {db_ar.status} to {data.status}"
                    )
                db_ar.status = data.status

            session.flush()
            session.refresh(db_ar)
            logger.info(f"AR updated id={id}")
            return ARMapper.to_domain(db_ar)

    def update_status(self, id: int, status: str) -> Optional[AREntity]:
        logger.info(f"Updating AR id={id} status={status}")
        with session_scope() as session:
            db_ar = session.query(DBAR).filter(DBAR.id == id).first()
            if not db_ar:
                logger.warning(f"AR not found for status update id={id}")
                return None

            if not self._can_transition(db_ar.status, status):
                raise InvalidARStatusTransition(
                    f"Cannot transition from {db_ar.status} to {status}"
                )
            db_ar.status = status
            session.flush()
            session.refresh(db_ar)
            return ARMapper.to_domain(db_ar)

    def add_payment(self, id: int, amount: float) -> Optional[AREntity]:
        logger.info(f"Adding payment amount={amount} to AR id={id}")
        with session_scope() as session:
            db_ar = session.query(DBAR).filter(DBAR.id == id).first()
            if not db_ar:
                logger.warning(f"AR not found for payment id={id}")
                return None

            payment_dec = Decimal(str(amount))
            if payment_dec > (db_ar.amount - db_ar.paid_amount):
                raise ARPaymentExceedsBalance(
                    f"Payment {amount} exceeds pending {db_ar.amount - db_ar.paid_amount}"
                )

            db_ar.paid_amount = db_ar.paid_amount + payment_dec
            db_ar.status = self._recalculate_status(db_ar)
            session.flush()
            session.refresh(db_ar)
            logger.info(f"AR payment applied id={id}, new status={db_ar.status}")
            return ARMapper.to_domain(db_ar)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting AR id={id}")
        with session_scope() as session:
            db_ar = session.query(DBAR).filter(DBAR.id == id).first()
            if not db_ar:
                logger.warning(f"AR not found for soft delete id={id}")
                return False
            db_ar.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"AR soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring AR id={id}")
        with session_scope() as session:
            db_ar = session.query(DBAR).filter(DBAR.id == id).first()
            if not db_ar:
                logger.warning(f"AR not found for restore id={id}")
                return False
            db_ar.deleted_at = None
            session.flush()
            logger.info(f"AR restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting AR id={id}")
        with session_scope() as session:
            db_ar = session.query(DBAR).filter(DBAR.id == id).first()
            if not db_ar:
                logger.warning(f"AR not found for hard delete id={id}")
                return False
            session.delete(db_ar)
            session.flush()
            logger.info(f"AR hard deleted id={id}")
            return True
