"""
from typing import Optional
ChargeType command repository implementation — SQLAlchemy.
"""
from datetime import datetime
from typing import Optional
import uuid as uuid_lib

from sqlalchemy.exc import IntegrityError

from library.dddpy.core_charge_types.domain.charge_type_cmd_repository import (
    ChargeTypeCmdRepository,
)
from library.dddpy.core_charge_types.domain.charge_type_data import (
    CreateChargeTypeData,
    UpdateChargeTypeData,
)
from library.dddpy.core_charge_types.domain.charge_type_entity import ChargeTypeEntity
from library.dddpy.core_charge_types.domain.charge_type_exception import (
    ChargeTypeAlreadyExists,
)
from library.dddpy.core_charge_types.infrastructure.dbcharge_type import DBChargeType
from library.dddpy.core_charge_types.infrastructure.charge_type_mapper import (
    ChargeTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeTypeCmdRepository")


class ChargeTypeCmdRepositoryImpl(ChargeTypeCmdRepository):

    def __init__(self):
        logger.info("ChargeTypeCmdRepositoryImpl initialized")

    def create(self, data: CreateChargeTypeData) -> ChargeTypeEntity:
        logger.info(f"Creating charge type code={data.code}")
        try:
            with session_scope() as session:
                db_ct = DBChargeType(
                    uuid=str(uuid_lib.uuid4()),
                    code=data.code,
                    name=data.name,
                    description=data.description,
                    is_global=int(data.is_global),
                    is_active=int(data.is_active),
                    sort_order=data.sort_order,
                )
                session.add(db_ct)
                session.flush()
                session.refresh(db_ct)
                logger.info(f"Charge type created with id={db_ct.id}")
                return ChargeTypeMapper.to_domain(db_ct)

        except IntegrityError:
            logger.warning(f"ChargeTypeAlreadyExists: code={data.code}")
            raise ChargeTypeAlreadyExists()

        except Exception as e:
            logger.error(f"Unexpected error creating charge type: {e}")
            raise

    def update(self, id: int, data: UpdateChargeTypeData) -> Optional[ChargeTypeEntity]:
        logger.info(f"Updating charge type id={id}")
        with session_scope() as session:
            db_ct = session.query(DBChargeType).filter(
                DBChargeType.id == id
            ).first()
            if not db_ct:
                logger.warning(f"Charge type not found for update id={id}")
                return None

            if data.name is not None:
                db_ct.name = data.name
            if data.description is not None:
                db_ct.description = data.description
            if data.is_global is not None:
                db_ct.is_global = int(data.is_global)
            if data.is_active is not None:
                db_ct.is_active = int(data.is_active)
            if data.sort_order is not None:
                db_ct.sort_order = data.sort_order

            session.flush()
            session.refresh(db_ct)
            logger.info(f"Charge type updated id={id}")
            return ChargeTypeMapper.to_domain(db_ct)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting charge type id={id}")
        with session_scope() as session:
            db_ct = session.query(DBChargeType).filter(
                DBChargeType.id == id
            ).first()
            if not db_ct:
                logger.warning(f"Charge type not found for soft delete id={id}")
                return False

            db_ct.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Charge type soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring charge type id={id}")
        with session_scope() as session:
            db_ct = session.query(DBChargeType).filter(
                DBChargeType.id == id
            ).first()
            if not db_ct:
                logger.warning(f"Charge type not found for restore id={id}")
                return False
            db_ct.deleted_at = None
            session.flush()
            logger.info(f"Charge type restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting charge type id={id}")
        with session_scope() as session:
            db_ct = session.query(DBChargeType).filter(
                DBChargeType.id == id
            ).first()
            if not db_ct:
                logger.warning(f"Charge type not found for hard delete id={id}")
                return False

            session.delete(db_ct)
            session.flush()
            logger.info(f"Charge type hard deleted id={id}")
            return True
