# Buildings Types Query Repository Implementation
from typing import List, Optional
from library.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from library.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesRepository
from library.dddpy.core_buildings_types.infrastructure.buildings_types import DBBuildingsTypes
from library.dddpy.core_buildings_types.infrastructure.buildings_types_mapper import BuildingsTypesMapper
from library.dddpy.shared.mysql.session_manager import session_scope


class BuildingsTypesQueryRepositoryImpl(BuildingsTypesRepository):
    
    def all(self) -> List[BuildingsTypes]:
        with session_scope() as session:
            db_types = session.query(DBBuildingsTypes).all()
            return [BuildingsTypesMapper.to_domain(db) for db in db_types]

    def create(self, data: dict):
        raise NotImplementedError("Use Command Repository for create")

    def update(self, id: int, data: dict):
        raise NotImplementedError("Use Command Repository for update")

    def delete(self, id: int):
        raise NotImplementedError("Use Command Repository for delete")

    def get_by_id(self, id: int) -> Optional[BuildingsTypes]:
        with session_scope() as session:
            db_type = session.query(DBBuildingsTypes).filter(
                DBBuildingsTypes.id == id
            ).first()
            if not db_type:
                return None
            return BuildingsTypesMapper.to_domain(db_type)

    def get_by_code(self, code: str) -> Optional[BuildingsTypes]:
        with session_scope() as session:
            db_type = session.query(DBBuildingsTypes).filter(
                DBBuildingsTypes.code == code
            ).first()
            if not db_type:
                return None
            return BuildingsTypesMapper.to_domain(db_type)
