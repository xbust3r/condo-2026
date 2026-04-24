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

    def find_active_by_unit(self, unit_id: int) -> list[UnitOwnershipEntity]:
        """Find all active (non-deleted, non-historical) ownerships for a unit."""
        with session_scope() as session:
            db_records = (
                session.query(DBUnitOwnership)
                .filter(
                    DBUnitOwnership.unit_id == unit_id,
                    DBUnitOwnership.status == "active",
                    DBUnitOwnership.deleted_at.is_(None),
                )
                .all()
            )
            return [UnitOwnershipMapper.to_domain(r) for r in db_records]

    def get_by_id_any_status(self, id: int) -> Optional[UnitOwnershipEntity]:
        """Get ownership record by id ignoring deleted_at filter."""
        with session_scope() as session:
            db_record = session.query(DBUnitOwnership).filter(DBUnitOwnership.id == id).first()
            if not db_record:
                return None
            return UnitOwnershipMapper.to_domain(db_record)

    def soft_delete_by_user(self, user_id: int) -> int:
        """
        USR-01 cascade: mark all active ownerships for a user as historical.
        Sets status='historical', end_date=today, deleted_at=now.
        Returns count of affected rows.
        """
        logger.info(f"USR-01 cascade: soft-deleting ownerships for user_id={user_id}")
        count = 0
        with session_scope() as session:
            rows = (
                session.query(DBUnitOwnership)
                .filter(
                    DBUnitOwnership.user_id == user_id,
                    DBUnitOwnership.status == "active",
                    DBUnitOwnership.deleted_at.is_(None),
                )
                .all()
            )
            today = datetime.utcnow().date()
            for row in rows:
                row.status = "historical"
                row.end_date = today
                row.deleted_at = datetime.utcnow()
                count += 1
            session.flush()
            logger.info(f"USR-01 cascade: {count} ownerships marked historical for user_id={user_id}")
            return count
