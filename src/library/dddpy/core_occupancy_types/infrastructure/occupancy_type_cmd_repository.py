"""
OccupancyType command repository implementation — SQLAlchemy.
"""
from datetime import datetime
from typing import Optional
import uuid as uuid_lib

from sqlalchemy.exc import IntegrityError

from library.dddpy.core_occupancy_types.domain.occupancy_type_cmd_repository import (
    OccupancyTypeCmdRepository,
)
from library.dddpy.core_occupancy_types.domain.occupancy_type_data import (
    CreateOccupancyTypeData,
    UpdateOccupancyTypeData,
)
from library.dddpy.core_occupancy_types.domain.occupancy_type_entity import OccupancyTypeEntity
from library.dddpy.core_occupancy_types.domain.occupancy_type_exception import (
    OccupancyTypeAlreadyExists,
)
from library.dddpy.core_occupancy_types.infrastructure.dboccupancy_type import DBOccupancyType
from library.dddpy.core_occupancy_types.infrastructure.occupancy_type_mapper import (
    OccupancyTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("OccupancyTypeCmdRepository")


class OccupancyTypeCmdRepositoryImpl(OccupancyTypeCmdRepository):

    def __init__(self):
        logger.info("OccupancyTypeCmdRepositoryImpl initialized")

    def create(self, data: CreateOccupancyTypeData) -> OccupancyTypeEntity:
        logger.info(f"Creating occupancy type code={data.code}")
        try:
            with session_scope() as session:
                db_ot = DBOccupancyType(
                    uuid=str(uuid_lib.uuid4()),
                    code=data.code,
                    name=data.name,
                    description=data.description,
                    requires_authorization=int(data.requires_authorization),
                    is_active=int(data.is_active),
                    sort_order=data.sort_order,
                )
                session.add(db_ot)
                session.flush()
                session.refresh(db_ot)
                logger.info(f"Occupancy type created with id={db_ot.id}")
                return OccupancyTypeMapper.to_domain(db_ot)

        except IntegrityError:
            logger.warning(f"OccupancyTypeAlreadyExists: code={data.code}")
            raise OccupancyTypeAlreadyExists()

        except Exception as e:
            logger.error(f"Unexpected error creating occupancy type: {e}")
            raise

    def update(self, id: int, data: UpdateOccupancyTypeData) -> Optional[OccupancyTypeEntity]:
        logger.info(f"Updating occupancy type id={id}")
        with session_scope() as session:
            db_ot = session.query(DBOccupancyType).filter(
                DBOccupancyType.id == id
            ).first()
            if not db_ot:
                logger.warning(f"Occupancy type not found for update id={id}")
                return None

            if data.name is not None:
                db_ot.name = data.name
            if data.description is not None:
                db_ot.description = data.description
            if data.requires_authorization is not None:
                db_ot.requires_authorization = int(data.requires_authorization)
            if data.is_active is not None:
                db_ot.is_active = int(data.is_active)
            if data.sort_order is not None:
                db_ot.sort_order = data.sort_order

            session.flush()
            session.refresh(db_ot)
            logger.info(f"Occupancy type updated id={id}")
            return OccupancyTypeMapper.to_domain(db_ot)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting occupancy type id={id}")
        with session_scope() as session:
            db_ot = session.query(DBOccupancyType).filter(
                DBOccupancyType.id == id
            ).first()
            if not db_ot:
                logger.warning(f"Occupancy type not found for soft delete id={id}")
                return False

            db_ot.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Occupancy type soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring occupancy type id={id}")
        with session_scope() as session:
            db_ot = session.query(DBOccupancyType).filter(
                DBOccupancyType.id == id
            ).first()
            if not db_ot:
                logger.warning(f"Occupancy type not found for restore id={id}")
                return False
            db_ot.deleted_at = None
            session.flush()
            logger.info(f"Occupancy type restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting occupancy type id={id}")
        with session_scope() as session:
            db_ot = session.query(DBOccupancyType).filter(
                DBOccupancyType.id == id
            ).first()
            if not db_ot:
                logger.warning(f"Occupancy type not found for hard delete id={id}")
                return False

            session.delete(db_ot)
            session.flush()
            logger.info(f"Occupancy type hard deleted id={id}")
            return True