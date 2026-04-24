from typing import Optional
from datetime import datetime
import uuid as uuid_lib
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_data import CreateUnitOccupancyData, UpdateUnitOccupancyData
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_cmd_repository import UnitOccupancyCmdRepository
from library.dddpy.core_unit_occupancies.infrastructure.dbunit_occupancy import DBUnitOccupancy
from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_mapper import UnitOccupancyMapper
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_exception import (
    DuplicateOccupancyRecord,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOccupancyCmdRepository")


class UnitOccupancyCmdRepositoryImpl(UnitOccupancyCmdRepository):

    def __init__(self):
        logger.info("UnitOccupancyCmdRepositoryImpl initialized")

    def create(self, data: CreateUnitOccupancyData) -> UnitOccupancyEntity:
        logger.info(
            f"Creating unit occupancy unit_id={data.unit_id}, user_id={data.user_id}, "
            f"occupancy_type_id={data.occupancy_type_id}"
        )
        try:
            with session_scope() as session:
                db_occupancy = DBUnitOccupancy(
                    uuid=str(uuid_lib.uuid4()),
                    unit_id=data.unit_id,
                    user_id=data.user_id,
                    occupancy_type_id=data.occupancy_type_id,
                    status=data.status,
                    start_date=data.start_date,
                    end_date=data.end_date,
                    is_primary=data.is_primary,
                    authorized_by_user_id=data.authorized_by_user_id,
                    notes=data.notes,
                )
                session.add(db_occupancy)
                session.flush()
                session.refresh(db_occupancy)
                logger.info(f"Unit occupancy created with id={db_occupancy.id}")
                return UnitOccupancyMapper.to_domain(db_occupancy)
        except IntegrityError as e:
            logger.warning(f"IntegrityError creating unit occupancy: {e}")
            raise DuplicateOccupancyRecord()

    def update(self, id: int, data: UpdateUnitOccupancyData) -> Optional[UnitOccupancyEntity]:
        logger.info(f"Updating unit occupancy id={id}")
        try:
            with session_scope() as session:
                db_occupancy = session.query(DBUnitOccupancy).filter(DBUnitOccupancy.id == id).first()
                if not db_occupancy:
                    logger.warning(f"Unit occupancy not found for update id={id}")
                    return None

                if data.occupancy_type_id is not None:
                    db_occupancy.occupancy_type_id = data.occupancy_type_id
                if data.status is not None:
                    db_occupancy.status = data.status
                if data.start_date is not None:
                    db_occupancy.start_date = data.start_date
                if data.end_date is not None:
                    db_occupancy.end_date = data.end_date
                if data.is_primary is not None:
                    db_occupancy.is_primary = data.is_primary
                if data.authorized_by_user_id is not None:
                    db_occupancy.authorized_by_user_id = data.authorized_by_user_id
                if data.notes is not None:
                    db_occupancy.notes = data.notes

                session.flush()
                session.refresh(db_occupancy)
                logger.info(f"Unit occupancy updated id={id}")
                return UnitOccupancyMapper.to_domain(db_occupancy)
        except IntegrityError as e:
            logger.warning(f"IntegrityError updating unit occupancy id={id}: {e}")
            raise DuplicateOccupancyRecord()

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting unit occupancy id={id}")
        with session_scope() as session:
            db_occupancy = session.query(DBUnitOccupancy).filter(DBUnitOccupancy.id == id).first()
            if not db_occupancy:
                logger.warning(f"Unit occupancy not found for soft delete id={id}")
                return False
            db_occupancy.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Unit occupancy soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring unit occupancy id={id}")
        with session_scope() as session:
            db_occupancy = session.query(DBUnitOccupancy).filter(DBUnitOccupancy.id == id).first()
            if not db_occupancy:
                logger.warning(f"Unit occupancy not found for restore id={id}")
                return False
            db_occupancy.deleted_at = None
            session.flush()
            logger.info(f"Unit occupancy restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting unit occupancy id={id}")
        with session_scope() as session:
            db_occupancy = session.query(DBUnitOccupancy).filter(DBUnitOccupancy.id == id).first()
            if not db_occupancy:
                logger.warning(f"Unit occupancy not found for hard delete id={id}")
                return False
            session.delete(db_occupancy)
            session.flush()
            logger.info(f"Unit occupancy hard deleted id={id}")
            return True

    def find_primary_by_unit(self, unit_id: int) -> Optional[UnitOccupancyEntity]:
        """Find active primary occupancy for a unit."""
        with session_scope() as session:
            db_occ = (
                session.query(DBUnitOccupancy)
                .filter(
                    and_(
                        DBUnitOccupancy.unit_id == unit_id,
                        DBUnitOccupancy.is_primary == True,
                        DBUnitOccupancy.deleted_at.is_(None),
                    )
                )
                .first()
            )
            if db_occ:
                return UnitOccupancyMapper.to_domain(db_occ)
            return None

    def get_unit_id(self, occupancy_id: int) -> Optional[int]:
        """Get unit_id for an existing occupancy record."""
        with session_scope() as session:
            db_occ = session.query(DBUnitOccupancy.id, DBUnitOccupancy.unit_id).filter(
                DBUnitOccupancy.id == occupancy_id
            ).first()
            return db_occ.unit_id if db_occ else None

    def soft_delete_by_user(self, user_id: int) -> int:
        """
        USR-01 cascade: mark all active occupancies for a user as inactive.
        Sets status='inactive', end_date=today, deleted_at=now.
        Returns count of affected rows.
        """
        logger.info(f"USR-01 cascade: soft-deleting occupancies for user_id={user_id}")
        count = 0
        with session_scope() as session:
            rows = (
                session.query(DBUnitOccupancy)
                .filter(
                    DBUnitOccupancy.user_id == user_id,
                    DBUnitOccupancy.status == "active",
                    DBUnitOccupancy.deleted_at.is_(None),
                )
                .all()
            )
            today = datetime.utcnow().date()
            for row in rows:
                row.status = "inactive"
                row.end_date = today
                row.deleted_at = datetime.utcnow()
                count += 1
            session.flush()
            logger.info(f"USR-01 cascade: {count} occupancies marked inactive for user_id={user_id}")
            return count