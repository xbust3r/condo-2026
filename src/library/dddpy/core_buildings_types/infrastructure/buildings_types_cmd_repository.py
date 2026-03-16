# Buildings Types Command Repository Implementation
from typing import List
from library.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from library.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesRepository
from library.dddpy.core_buildings_types.domain.buildings_types_exception import (
    BuildingsTypesNotFoundException,
    BuildingsTypesAlreadyExistsException,
)
from library.dddpy.core_buildings_types.infrastructure.buildings_types import DBBuildingsTypes
from library.dddpy.core_buildings_types.infrastructure.buildings_types_mapper import BuildingsTypesMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger

logger = Logger("BuildingsTypesCmdRepository")


class BuildingsTypesCmdRepositoryImpl(BuildingsTypesRepository):
    
    def __init__(self):
        logger.info("BuildingsTypesCmdRepositoryImpl initialized")

    def all(self) -> List[BuildingsTypes]:
        with session_scope() as session:
            db_types = session.query(DBBuildingsTypes).all()
            return [BuildingsTypesMapper.to_domain(db) for db in db_types]

    def create(self, data: dict) -> BuildingsTypes:
        with session_scope() as session:
            existing = session.query(DBBuildingsTypes).filter(
                DBBuildingsTypes.code == data.get("code")
            ).first()
            if existing:
                raise BuildingsTypesAlreadyExistsException(data.get("code"))
            
            db_type = DBBuildingsTypes(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                status=data.get("status", 1),
            )
            session.add(db_type)
            session.flush()
            session.refresh(db_type)
            return BuildingsTypesMapper.to_domain(db_type)

    def update(self, id: int, data: dict) -> BuildingsTypes:
        with session_scope() as session:
            db_type = session.query(DBBuildingsTypes).filter(
                DBBuildingsTypes.id == id
            ).first()
            
            if not db_type:
                raise BuildingsTypesNotFoundException(id)
            
            for key, value in data.items():
                if hasattr(db_type, key) and value is not None:
                    setattr(db_type, key, value)
            
            session.flush()
            session.refresh(db_type)
            return BuildingsTypesMapper.to_domain(db_type)

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            db_type = session.query(DBBuildingsTypes).filter(
                DBBuildingsTypes.id == id
            ).first()
            
            if not db_type:
                raise BuildingsTypesNotFoundException(id)
            
            session.delete(db_type)
            return True

    def get_by_id(self, id: int) -> BuildingsTypes:
        with session_scope() as session:
            db_type = session.query(DBBuildingsTypes).filter(
                DBBuildingsTypes.id == id
            ).first()
            
            if not db_type:
                raise BuildingsTypesNotFoundException(id)
            
            return BuildingsTypesMapper.to_domain(db_type)

    def get_by_code(self, code: str) -> BuildingsTypes:
        with session_scope() as session:
            db_type = session.query(DBBuildingsTypes).filter(
                DBBuildingsTypes.code == code
            ).first()
            
            if not db_type:
                raise BuildingsTypesNotFoundException()
            
            return BuildingsTypesMapper.to_domain(db_type)
