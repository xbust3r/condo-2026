from datetime import datetime
from typing import Optional
import uuid as uuid_lib

from sqlalchemy.exc import IntegrityError

from library.dddpy.core_unities_types.domain.unity_type_cmd_repository import (
    UnityTypeCmdRepository,
)
from library.dddpy.core_unities_types.domain.unity_type_data import (
    CreateUnityTypeData,
    UpdateUnityTypeData,
)
from library.dddpy.core_unities_types.domain.unity_type_entity import UnityTypeEntity
from library.dddpy.core_unities_types.domain.unity_type_exception import (
    DuplicateUnityTypeCode,
    UnityTypeIsSystem,
)
from library.dddpy.core_unities_types.infrastructure.dbunitytype import DBUnityType
from library.dddpy.core_unities_types.infrastructure.unity_type_mapper import (
    UnityTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityTypeCmdRepository")


class UnityTypeCmdRepositoryImpl(UnityTypeCmdRepository):

    def __init__(self):
        logger.info("UnityTypeCmdRepositoryImpl initialized")

    def create(self, data: CreateUnityTypeData) -> UnityTypeEntity:
        logger.info(
            f"Creating unity type code={data.code}, "
            f"condominium_id={data.condominium_id}"
        )
        try:
            with session_scope() as session:
                db_type = DBUnityType(
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
                logger.info(f"Unity type created with id={db_type.id}")
                return UnityTypeMapper.to_domain(db_type)

        except IntegrityError:
            scope = "global" if data.condominium_id is None else f"condominium {data.condominium_id}"
            logger.warning(
                f"DuplicateUnityTypeCode: code={data.code} in scope={scope}"
            )
            raise DuplicateUnityTypeCode(code=data.code, scope=scope)

        except Exception as e:
            logger.error(f"Unexpected error creating unity type: {e}")
            raise

    def update(self, id: int, data: UpdateUnityTypeData) -> Optional[UnityTypeEntity]:
        logger.info(f"Updating unity type id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnityType).filter(
                DBUnityType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unity type not found for update id={id}")
                return None

            if db_type.is_system:
                logger.warning(f"Attempt to modify system type id={id}")
                raise UnityTypeIsSystem()

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
            logger.info(f"Unity type updated id={id}")
            return UnityTypeMapper.to_domain(db_type)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting unity type id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnityType).filter(
                DBUnityType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unity type not found for soft delete id={id}")
                return False

            if db_type.is_system:
                logger.warning(f"Attempt to delete system type id={id}")
                raise UnityTypeIsSystem()

            db_type.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Unity type soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring unity type id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnityType).filter(
                DBUnityType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unity type not found for restore id={id}")
                return False
            db_type.deleted_at = None
            session.flush()
            logger.info(f"Unity type restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting unity type id={id}")
        with session_scope() as session:
            db_type = session.query(DBUnityType).filter(
                DBUnityType.id == id
            ).first()
            if not db_type:
                logger.warning(f"Unity type not found for hard delete id={id}")
                return False

            if db_type.is_system:
                logger.warning(f"Attempt to hard-delete system type id={id}")
                raise UnityTypeIsSystem()

            session.delete(db_type)
            session.flush()
            logger.info(f"Unity type hard deleted id={id}")
            return True
