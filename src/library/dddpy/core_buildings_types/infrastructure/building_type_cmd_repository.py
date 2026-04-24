from typing import Optional
from datetime import datetime
from typing import Optional
import uuid as uuid_lib

from sqlalchemy.exc import IntegrityError

from library.dddpy.core_buildings_types.domain.building_type_cmd_repository import (
    BuildingTypeCmdRepository,
)
from library.dddpy.core_buildings_types.domain.building_type_data import (
    CreateBuildingTypeData,
    UpdateBuildingTypeData,
)
from library.dddpy.core_buildings_types.domain.building_type_entity import BuildingTypeEntity
from library.dddpy.core_buildings_types.domain.building_type_exception import (
    DuplicateBuildingTypeCode,
    BuildingTypeIsSystem,
)
from library.dddpy.core_buildings_types.infrastructure.dbbuildingtype import DBBuildingType
from library.dddpy.core_buildings_types.infrastructure.building_type_mapper import (
    BuildingTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingTypeCmdRepository")


class BuildingTypeCmdRepositoryImpl(BuildingTypeCmdRepository):

    def __init__(self):
        logger.info("BuildingTypeCmdRepositoryImpl initialized")

    def create(self, data: CreateBuildingTypeData) -> BuildingTypeEntity:
        logger.info(
            f"Creating building type code={data.code}, "
            f"condominium_id={data.condominium_id}"
        )
        try:
            with session_scope() as session:
                db_type = DBBuildingType(
                    uuid=str(uuid_lib.uuid4()),
                    condominium_id=data.condominium_id,
                    code=data.code,
                    name=data.name,
                    description=data.description,
                    is_system=int(data.is_system),
                    sort_order=data.sort_order,
                )
                session.add(db_type)
                session.flush()
                session.refresh(db_type)
                logger.info(f"Building type created with id={db_type.id}")
                return BuildingTypeMapper.to_domain(db_type)

        except IntegrityError:
            scope = "global" if data.condominium_id is None else f"condominium {data.condominium_id}"
            logger.warning(
                f"DuplicateBuildingTypeCode: code={data.code} in scope={scope}"
            )
            raise DuplicateBuildingTypeCode(code=data.code, scope=scope)

        except Exception as e:
            logger.error(f"Unexpected error creating building type: {e}")
            raise

    def update(self, id: int, data: UpdateBuildingTypeData) -> Optional[BuildingTypeEntity]:
        logger.info(f"Updating building type id={id}")
        with session_scope() as session:
            db_type = session.query(DBBuildingType).filter(
                DBBuildingType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Building type not found for update id={id}")
                return None

            if db_type.is_system:
                logger.warning(f"Attempt to modify system type id={id}")
                raise BuildingTypeIsSystem()

            if data.name is not None:
                db_type.name = data.name
            if data.description is not None:
                db_type.description = data.description
            if data.sort_order is not None:
                db_type.sort_order = data.sort_order
            if data.status is not None:
                db_type.status = data.status

            session.flush()
            session.refresh(db_type)
            logger.info(f"Building type updated id={id}")
            return BuildingTypeMapper.to_domain(db_type)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting building type id={id}")
        with session_scope() as session:
            db_type = session.query(DBBuildingType).filter(
                DBBuildingType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Building type not found for soft delete id={id}")
                return False

            if db_type.is_system:
                logger.warning(f"Attempt to delete system type id={id}")
                raise BuildingTypeIsSystem()

            db_type.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Building type soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring building type id={id}")
        with session_scope() as session:
            db_type = session.query(DBBuildingType).filter(
                DBBuildingType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Building type not found for restore id={id}")
                return False
            db_type.deleted_at = None
            session.flush()
            logger.info(f"Building type restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting building type id={id}")
        with session_scope() as session:
            db_type = session.query(DBBuildingType).filter(
                DBBuildingType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Building type not found for hard delete id={id}")
                return False

            if db_type.is_system:
                logger.warning(f"Attempt to hard-delete system type id={id}")
                raise BuildingTypeIsSystem()

            session.delete(db_type)
            session.flush()
            logger.info(f"Building type hard deleted id={id}")
            return True
