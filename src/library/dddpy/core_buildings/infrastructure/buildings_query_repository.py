# Buildings Query Repository Implementation
from typing import List, Optional
from library.dddpy.core_buildings.domain.buildings import Buildings
from library.dddpy.core_buildings.domain.buildings_repository import BuildingsRepository
from library.dddpy.core_buildings.infrastructure.buildings import DBBuildings
from library.dddpy.core_buildings.infrastructure.buildings_mapper import BuildingsMapper
from library.dddpy.shared.mysql.session_manager import session_scope


class BuildingsQueryRepositoryImpl(BuildingsRepository):
    
    def all(self) -> List[Buildings]:
        with session_scope() as session:
            db_buildings = session.query(DBBuildings).all()
            return [BuildingsMapper.to_domain(db) for db in db_buildings]

    def create(self, data: dict):
        raise NotImplementedError("Use Command Repository for create")

    def update(self, id: int, data: dict):
        raise NotImplementedError("Use Command Repository for update")

    def delete(self, id: int):
        raise NotImplementedError("Use Command Repository for delete")

    def get_by_id(self, id: int) -> Optional[Buildings]:
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.id == id
            ).first()
            if not db_building:
                return None
            return BuildingsMapper.to_domain(db_building)

    def get_by_code(self, code: str) -> Optional[Buildings]:
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(
                DBBuildings.code == code
            ).first()
            if not db_building:
                return None
            return BuildingsMapper.to_domain(db_building)

    def get_by_condominium(self, condominium_id: int) -> List[Buildings]:
        with session_scope() as session:
            db_buildings = session.query(DBBuildings).filter(
                DBBuildings.condominium_id == condominium_id
            ).all()
            return [BuildingsMapper.to_domain(db) for db in db_buildings]
