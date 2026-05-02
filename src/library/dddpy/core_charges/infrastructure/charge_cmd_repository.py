"""
from typing import Optional
Charge command repository implementation — SQLAlchemy.
"""
from datetime import datetime
from typing import Optional
import uuid as uuid_lib

from library.dddpy.core_charges.domain.charge_cmd_repository import (
    ChargeCmdRepository,
)
from library.dddpy.core_charges.domain.charge_data import (
    CreateChargeData,
    UpdateChargeData,
)
from library.dddpy.core_charges.domain.charge_entity import ChargeEntity
from library.dddpy.core_charges.infrastructure.dbcharge import DBCharge
from library.dddpy.core_charges.infrastructure.charge_mapper import (
    ChargeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeCmdRepository")


class ChargeCmdRepositoryImpl(ChargeCmdRepository):

    def __init__(self):
        logger.info("ChargeCmdRepositoryImpl initialized")

    def create(self, data: CreateChargeData) -> ChargeEntity:
        logger.info(f"Creating charge condominium_id={data.condominium_id}")
        with session_scope() as session:
            db_c = DBCharge(
                uuid=str(uuid_lib.uuid4()),
                condominium_id=data.condominium_id,
                charge_type_id=data.charge_type_id,
                scope=data.scope,
                unit_id=data.unit_id,
                building_id=data.building_id,
                distribution_mode=data.distribution_mode,
                description=data.description,
                amount=data.amount,
                currency=data.currency,
                is_recurrent=int(data.is_recurrent),
                period_pattern=data.period_pattern,
                start_date=data.start_date,
                end_date=data.end_date,
                status=data.status,
            )
            session.add(db_c)
            session.flush()
            session.refresh(db_c)
            logger.info(f"Charge created with id={db_c.id}")
            return ChargeMapper.to_domain(db_c)

    def update(self, id: int, data: UpdateChargeData) -> Optional[ChargeEntity]:
        logger.info(f"Updating charge id={id}")
        with session_scope() as session:
            db_c = session.query(DBCharge).filter(DBCharge.id == id).first()
            if not db_c:
                logger.warning(f"Charge not found for update id={id}")
                return None

            if data.scope is not None:
                db_c.scope = data.scope
            if data.unit_id is not None:
                db_c.unit_id = data.unit_id
            if data.building_id is not None:
                db_c.building_id = data.building_id
            if data.distribution_mode is not None:
                db_c.distribution_mode = data.distribution_mode

            # Explicit clear flags (for FK cleanup without scope change)
            if data.clear_unit_id:
                db_c.unit_id = None
            if data.clear_building_id:
                db_c.building_id = None

            # Scope-driven FK cleanup: when scope changes, auto-clear FKs
            # that don't belong to the new scope
            if data.scope is not None:
                if data.scope == "unit":
                    db_c.building_id = None
                elif data.scope == "building":
                    db_c.unit_id = None
                elif data.scope == "condominium":
                    db_c.unit_id = None
                    db_c.building_id = None

            if data.description is not None:
                db_c.description = data.description
            if data.amount is not None:
                db_c.amount = data.amount
            if data.is_recurrent is not None:
                db_c.is_recurrent = int(data.is_recurrent)
            if data.period_pattern is not None:
                db_c.period_pattern = data.period_pattern
            if data.start_date is not None:
                db_c.start_date = data.start_date
            if data.end_date is not None:
                db_c.end_date = data.end_date
            if data.status is not None:
                db_c.status = data.status

            session.flush()
            session.refresh(db_c)
            logger.info(f"Charge updated id={id}")
            return ChargeMapper.to_domain(db_c)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting charge id={id}")
        with session_scope() as session:
            db_c = session.query(DBCharge).filter(DBCharge.id == id).first()
            if not db_c:
                logger.warning(f"Charge not found for soft delete id={id}")
                return False
            db_c.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Charge soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring charge id={id}")
        with session_scope() as session:
            db_c = session.query(DBCharge).filter(DBCharge.id == id).first()
            if not db_c:
                logger.warning(f"Charge not found for restore id={id}")
                return False
            db_c.deleted_at = None
            session.flush()
            logger.info(f"Charge restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting charge id={id}")
        with session_scope() as session:
            db_c = session.query(DBCharge).filter(DBCharge.id == id).first()
            if not db_c:
                logger.warning(f"Charge not found for hard delete id={id}")
                return False
            session.delete(db_c)
            session.flush()
            logger.info(f"Charge hard deleted id={id}")
            return True
