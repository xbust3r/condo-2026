from typing import Optional
from datetime import datetime
import uuid as uuid_lib
from sqlalchemy.exc import IntegrityError

from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity
from library.dddpy.core_unit_ownerships.domain.unit_ownership_data import CreateUnitOwnershipData, UpdateUnitOwnershipData
from library.dddpy.core_unit_ownerships.domain.unit_ownership_cmd_repository import UnitOwnershipCmdRepository
from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_mapper import UnitOwnershipMapper
from library.dddpy.core_unit_ownerships.domain.unit_ownership_exception import (
    DuplicateOwnershipRecord,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOwnershipCmdRepository")


class UnitOwnershipCmdRepositoryImpl(UnitOwnershipCmdRepository):

    def __init__(self):
        logger.info("UnitOwnershipCmdRepositoryImpl initialized")

    def create(self, data: CreateUnitOwnershipData) -> UnitOwnershipEntity:
        logger.info(
            f"Creating unit ownership unit_id={data.unit_id}, user_id={data.user_id}, "
            f"ownership_type={data.ownership_type}"
        )
        try:
            with session_scope() as session:
                db_ownership = DBUnitOwnership(
                    uuid=str(uuid_lib.uuid4()),
                    unit_id=data.unit_id,
                    user_id=data.user_id,
                    ownership_type=data.ownership_type,
                    ownership_percentage=data.ownership_percentage,
                    status="active",
                    start_date=data.start_date,
                    end_date=data.end_date,
                    notes=data.notes,
                )
                session.add(db_ownership)
                session.flush()
                session.refresh(db_ownership)
                logger.info(f"Unit ownership created with id={db_ownership.id}")
                return UnitOwnershipMapper.to_domain(db_ownership)
        except IntegrityError as e:
            error_str = str(e).lower()
            logger.warning(f"IntegrityError creating unit ownership: {e}")
            raise DuplicateOwnershipRecord()

    def update(self, id: int, data: UpdateUnitOwnershipData) -> Optional[UnitOwnershipEntity]:
        logger.info(f"Updating unit ownership id={id}")
        try:
            with session_scope() as session:
                db_ownership = (
                    session.query(DBUnitOwnership)
                    .filter(DBUnitOwnership.id == id)
                    .first()
                )
                if not db_ownership:
                    logger.warning(f"Unit ownership not found for update id={id}")
                    return None

                if data.ownership_type is not None:
                    db_ownership.ownership_type = data.ownership_type
                if data.ownership_percentage is not None:
                    db_ownership.ownership_percentage = data.ownership_percentage
                if data.status is not None:
                    db_ownership.status = data.status
                if data.start_date is not None:
                    db_ownership.start_date = data.start_date
                if data.end_date is not None:
                    db_ownership.end_date = data.end_date
                if data.notes is not None:
                    db_ownership.notes = data.notes

                session.flush()
                session.refresh(db_ownership)
                logger.info(f"Unit ownership updated id={id}")
                return UnitOwnershipMapper.to_domain(db_ownership)
        except IntegrityError as e:
            logger.warning(f"IntegrityError updating unit ownership id={id}: {e}")
            raise DuplicateOwnershipRecord()

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting unit ownership id={id}")
        with session_scope() as session:
            db_ownership = (
                session.query(DBUnitOwnership)
                .filter(DBUnitOwnership.id == id)
                .first()
            )
            if not db_ownership:
                logger.warning(f"Unit ownership not found for soft delete id={id}")
                return False
            db_ownership.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Unit ownership soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring unit ownership id={id}")
        with session_scope() as session:
            db_ownership = (
                session.query(DBUnitOwnership)
                .filter(DBUnitOwnership.id == id)
                .first()
            )
            if not db_ownership:
                logger.warning(f"Unit ownership not found for restore id={id}")
                return False
            db_ownership.deleted_at = None
            session.flush()
            logger.info(f"Unit ownership restored id={id}")
            return True
