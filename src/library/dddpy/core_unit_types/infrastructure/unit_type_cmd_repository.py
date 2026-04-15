from datetime import datetime
from typing import Optional
import uuid as uuid_lib

from sqlalchemy.exc import IntegrityError

from library.dddpy.core_unit_types.domain.unit_type_cmd_repository import (
    UnitTypeCmdRepository,
)
from library.dddpy.core_unit_types.domain.unit_type_data import (
    CreateUnitTypeData,
    UpdateUnitTypeData,
)
from library.dddpy.core_unit_types.domain.unit_type_entity import UnitTypeEntity
from library.dddpy.core_unit_types.domain.unit_type_exception import (
    DuplicateUnitTypeCode,
    UnitTypeIsSystem,
)
from library.dddpy.core_unit_types.infrastructure.dbunit_type import DBUnitType
from library.dddpy.core_unit_types.infrastructure.unit_type_mapper import (
    UnitTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitTypeCmdRepository")


class UnitTypeCmdRepositoryImpl(UnitTypeCmdRepository):

    def __init__(self):
        logger.info("UnitTypeCmdRepositoryImpl initialized")

    def create(self, data: CreateUnitTypeData) -> UnitTypeEntity:
        logger.info(
            f"Creating unit type code={data.code}, "
            f"condominium_id={data.condominium_id}"
        )
        try:
            with session_scope() as session:
                db_type = DBUnitType(
                    uuid=str(uuid_lib.uuid4()),
                    condominium_id=data.condominium_id,
                    code=data.code,
                    name=data.name,
                    description=data.description,
                    usage_class=data.usage_class,
                    is_system=int(data.is_system),
                    sort_order=data.sort_order,
                )
                session.add(db_type)
                session.flush()
                session.refresh(db_type)
                logger.info(f"Unit type created with id={db_type.id}")
                return UnitTypeMapper.to_domain(db_type)

        except IntegrityError:
            scope = "global" if data.condominium_id is None else f"condominium {data.condominium_id}"
            logger.warning(
                f"DuplicateUnitTypeCode: code={data.code} in scope={scope}"
            )
            raise DuplicateUnitTypeCode(code=data.code, scope=scope)

        except Exception as e:
            logger.error(f"Unexpected error creating unit type: {e}")
            raise

    def update(self, id: int, data: UpdateUnitTypeData) -> Optional[UnitTypeEntity]:
        logger.info(f"Updating unit type id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnitType).filter(
                DBUnitType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unit type not found for update id={id}")
                return None

            if db_type.is_system:
                logger.warning(f"Attempt to modify system type id={id}")
                raise UnitTypeIsSystem()

            if data.name is not None:
                db_type.name = data.name
            if data.description is not None:
                db_type.description = data.description
            if data.usage_class is not None:
                db_type.usage_class = data.usage_class
            if data.sort_order is not None:
                db_type.sort_order = data.sort_order
            if data.status is not None:
                db_type.status = data.status

            session.flush()
            session.refresh(db_type)
            logger.info(f"Unit type updated id={id}")
            return UnitTypeMapper.to_domain(db_type)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting unit type id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnitType).filter(
                DBUnitType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unit type not found for soft delete id={id}")
                return False

            if db_type.is_system:
                logger.warning(f"Attempt to delete system type id={id}")
                raise UnitTypeIsSystem()

            db_type.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Unit type soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring unit type id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnitType).filter(
                DBUnitType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unit type not found for restore id={id}")
                return False
            db_type.deleted_at = None
            session.flush()
            logger.info(f"Unit type restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting unit type id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnitType).filter(
                DBUnitType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unit type not found for hard delete id={id}")
                return False

            if db_type.is_system:
                logger.warning(f"Attempt to hard-delete system type id={id}")
                raise UnitTypeIsSystem()

            session.delete(db_type)
            session.flush()
            logger.info(f"Unit type hard deleted id={id}")
            return True