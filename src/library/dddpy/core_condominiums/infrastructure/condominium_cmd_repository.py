from typing import Optional
from typing import Optional
from datetime import datetime
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
                    land_area=data.land_area,
                    built_area=data.built_area,
                    area_unit=data.area_unit,
                    legal_name=data.legal_name,
                    document_number=data.document_number,
                    address=data.address,
                    city=data.city,
                    country=data.country,
                    contact_email=data.contact_email,
                    contact_phone=data.contact_phone,
                    theme_id=data.theme_id,
                    amenity_settings=data.amenity_settings,
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
            if data.land_area is not None:
                db_condominium.land_area = data.land_area
            if data.built_area is not None:
                db_condominium.built_area = data.built_area
            if data.area_unit is not None:
                db_condominium.area_unit = data.area_unit
            if data.legal_name is not None:
                db_condominium.legal_name = data.legal_name
            if data.document_number is not None:
                db_condominium.document_number = data.document_number
            if data.address is not None:
                db_condominium.address = data.address
            if data.city is not None:
                db_condominium.city = data.city
            if data.country is not None:
                db_condominium.country = data.country
            if data.contact_email is not None:
                db_condominium.contact_email = data.contact_email
            if data.contact_phone is not None:
                db_condominium.contact_phone = data.contact_phone
            if data.status is not None:
                db_condominium.status = data.status
            if data.theme_id is not None:
                db_condominium.theme_id = data.theme_id
            if data.amenity_settings is not None:
                db_condominium.amenity_settings = data.amenity_settings
            session.flush()
            session.refresh(db_condominium)
            logger.info(f"Condominium updated id={id}")
            return CondominiumMapper.to_domain(db_condominium)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting condominium id={id}")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(DBCondominiums.id == id).first()
            if not db_condominium:
                logger.warning(f"Condominium not found for soft delete id={id}")
                return False
            db_condominium.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Condominium soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring condominium id={id}")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(DBCondominiums.id == id).first()
            if not db_condominium:
                logger.warning(f"Condominium not found for restore id={id}")
                return False
            db_condominium.deleted_at = None
            session.flush()
            logger.info(f"Condominium restored id={id}")
            return True
