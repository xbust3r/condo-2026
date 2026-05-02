"""
Amenity command repository implementation — SQLAlchemy.

Now supports scope + building_id persistence.
"""
from datetime import datetime, timezone
from typing import Optional

from library.dddpy.core_amenities.domain.amenity_cmd_repository import (
    AmenityCmdRepository,
)
from library.dddpy.core_amenities.domain.amenity_entity import AmenityEntity
from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AmenityCmdRepository")


class AmenityCmdRepositoryImpl(AmenityCmdRepository):

    def __init__(self):
        logger.info("AmenityCmdRepositoryImpl initialized")

    def create(self, entity: AmenityEntity) -> int:
        logger.info(
            f"Creating amenity condominium_id={entity.condominium_id} "
            f"scope={entity.scope} building_id={entity.building_id}"
        )
        with session_scope() as session:
            db_a = DBAmenity(
                uuid=entity.uuid,
                condominium_id=entity.condominium_id,
                scope=entity.scope,
                building_id=entity.building_id,
                name=entity.name,
                description=entity.description,
                location=entity.location,
                max_capacity=entity.max_capacity,
                booking_duration_min=entity.booking_duration_min,
                requires_approval=entity.requires_approval,
                status=entity.status,
            )
            session.add(db_a)
            session.flush()
            session.refresh(db_a)
            logger.info(f"Amenity created id={db_a.id}")
            return db_a.id

    def update(self, entity: AmenityEntity) -> bool:
        logger.info(
            f"Updating amenity id={entity.id} scope={entity.scope} "
            f"building_id={entity.building_id}"
        )
        with session_scope() as session:
            db_a = session.query(DBAmenity).filter(
                DBAmenity.id == entity.id,
                DBAmenity.deleted_at.is_(None),
            ).first()
            if not db_a:
                return False
            db_a.name = entity.name
            db_a.description = entity.description
            db_a.location = entity.location
            db_a.max_capacity = entity.max_capacity
            db_a.booking_duration_min = entity.booking_duration_min
            db_a.requires_approval = entity.requires_approval
            db_a.scope = entity.scope
            db_a.building_id = entity.building_id
            db_a.status = entity.status
            db_a.updated_at = datetime.now(timezone.utc)
            session.flush()
            logger.info(f"Amenity updated id={entity.id}")
            return True

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft-deleting amenity id={id}")
        with session_scope() as session:
            db_a = session.query(DBAmenity).filter(
                DBAmenity.id == id,
                DBAmenity.deleted_at.is_(None),
            ).first()
            if not db_a:
                return False
            db_a.deleted_at = datetime.now(timezone.utc)
            session.flush()
            logger.info(f"Amenity soft-deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard-deleting amenity id={id}")
        with session_scope() as session:
            db_a = session.query(DBAmenity).filter(
                DBAmenity.id == id,
            ).first()
            if not db_a:
                return False
            session.delete(db_a)
            session.flush()
            logger.info(f"Amenity hard-deleted id={id}")
            return True
