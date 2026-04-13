from typing import Optional
import uuid as uuid_lib
from sqlalchemy.exc import IntegrityError

from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity
from library.dddpy.core_condominiums.domain.condominium_data import CreateCondominiumData, UpdateCondominiumData
from library.dddpy.core_condominiums.domain.condominium_cmd_repository import CondominiumCmdRepository
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums
from library.dddpy.core_condominiums.infrastructure.condominium_mapper import CondominiumMapper
from library.dddpy.core_condominiums.domain.condominium_exception import RepeatedCondominiumCode
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumCmdRepository")


class CondominiumCmdRepositoryImpl(CondominiumCmdRepository):

    def __init__(self):
        logger.info("CondominiumCmdRepositoryImpl initialized")

    def create(self, data: CreateCondominiumData) -> CondominiumEntity:
        logger.info(f"Creating condominium with code={data.code}")
        try:
            with session_scope() as session:
                db_condominium = DBCondominiums(
                    uuid=str(uuid_lib.uuid4()),
                    code=data.code,
                    name=data.name,
                    description=data.description,
                    size=data.size,
                    percentage=data.percentage,
                )
                session.add(db_condominium)
                session.flush()
                session.refresh(db_condominium)
                logger.info(f"Condominium created with id={db_condominium.id}")
                return CondominiumMapper.to_domain(db_condominium)
        except IntegrityError as e:
            logger.warning(f"IntegrityError: duplicate code={data.code} — {e}")
            raise RepeatedCondominiumCode()
        except Exception as e:
            logger.error(f"Unexpected error creating condominium: {e}")
            raise

    def update(self, id: int, data: UpdateCondominiumData) -> Optional[CondominiumEntity]:
        logger.info(f"Updating condominium id={id}")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(DBCondominiums.id == id).first()
            if not db_condominium:
                logger.warning(f"Condominium not found for update id={id}")
                return None
            if data.name is not None:
                db_condominium.name = data.name
            if data.description is not None:
                db_condominium.description = data.description
            if data.size is not None:
                db_condominium.size = data.size
            if data.percentage is not None:
                db_condominium.percentage = data.percentage
            if data.status is not None:
                db_condominium.status = data.status
            session.flush()
            session.refresh(db_condominium)
            logger.info(f"Condominium updated id={id}")
            return CondominiumMapper.to_domain(db_condominium)

    def delete(self, id: int) -> bool:
        logger.info(f"Deleting condominium id={id}")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(DBCondominiums.id == id).first()
            if not db_condominium:
                logger.warning(f"Condominium not found for delete id={id}")
                return False
            session.delete(db_condominium)
            session.flush()
            logger.info(f"Condominium deleted id={id}")
            return True