# Buildings Command Repository Implementation
from typing import List
from library.dddpy.core_buildings.domain.buildings import Buildings
from library.dddpy.core_buildings.domain.buildings_repository import BuildingsRepository
from library.dddpy.core_buildings.domain.buildings_exception import (
    BuildingsNotFoundException,
    BuildingsAlreadyExistsException,
)
from library.dddpy.core_buildings.infrastructure.buildings import DBBuildings
from library.dddpy.core_buildings.infrastructure.buildings_mapper import BuildingsMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger

logger = Logger("BuildingsCmdRepository")


class BuildingsCmdRepositoryImpl(BuildingsRepository):
    
    def __init__(self):
        logger.info("BuildingsCmdRepositoryImpl initialized")

    def all(self) -> List[Buildings]:
        with session_scope() as session:
            db_buildings = session.query(DBBuildings).all()
            return [BuildingsMapper.to_domain(db) for db in db_buildings]

    def create(self, data: dict) -> Buildings:
        with session_scope() as session:
            existing = session.query(DBBuildings).filter(
                DBBuildings.code == data.get("code")
            ).first()
            if existing:
                raise BuildingsAlreadyExistsException(data.get("code"))
            
            db_building = DBBuildings(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                size=data.get("size"),
                percentage=data.get("percentage"),
                type=data.get("type"),
                condominium_id=data.get("condominium_id"),
                building_type_id=data.get("building_type_id"),
                status=data.get("status", 1),
            )
            session.add(db_building)
            session.flush()
            session.refresh(db_building)
            return BuildingsMapper.to_domain(db_building)

    def update(self, id: int, data: dict) -> Buildings:
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.id == id
            ).first()
            
            if not db_building:
                raise BuildingsNotFoundException(id)
            
            for key, value in data.items():
                if hasattr(db_building, key) and value is not None:
                    setattr(db_building, key, value)
            
            session.flush()
            session.refresh(db_building)
            return BuildingsMapper.to_domain(db_building)

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.id == id
            ).first()
            
            if not db_building:
                raise BuildingsNotFoundException(id)
            
            session.delete(db_building)
            return True

    def get_by_id(self, id: int) -> Buildings:
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.id == id
            ).first()
            
            if not db_building:
                raise BuildingsNotFoundException(id)
            
            return BuildingsMapper.to_domain(db_building)

    def get_by_code(self, code: str) -> Buildings:
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.code == code
            ).first()
            
            if not db_building:
                raise BuildingsNotFoundException()
            
            return BuildingsMapper.to_domain(db_building)

    def get_by_condominium(self, condominium_id: int) -> List[Buildings]:
        with session_scope() as session:
            db_buildings = session.query(DBBuildings).filter(
                DBBuildings.condominium_id == condominium_id
            ).all()
            return [BuildingsMapper.to_domain(db) for db in db_buildings]
