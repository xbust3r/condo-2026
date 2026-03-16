# Condominium Query Repository Implementation
from typing import List, Optional
from library.dddpy.core_condominiums.domain.condominiums import Condominium
from library.dddpy.core_condominiums.domain.condominiums_repository import CondominiumRepository
from library.dddpy.core_condominiums.infrastructure.condominiums import DBCondominiums
from library.dddpy.core_condominiums.infrastructure.condominiums_mapper import CondominiumMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger

logger = Logger("CondominiumQueryRepository")


class CondominiumQueryRepositoryImpl(CondominiumRepository):
    
    def __init__(self):
        logger.info("CondominiumQueryRepositoryImpl initialized")

    def all(self) -> List[Condominium]:
        with session_scope() as session:
            db_condominiums = session.query(DBCondominiums).all()
            return [CondominiumMapper.to_domain(db) for db in db_condominiums]

    def create(self, data: dict):
        raise NotImplementedError("Use Command Repository for create")

    def update(self, id: int, data: dict):
        raise NotImplementedError("Use Command Repository for update")

    def delete(self, id: int):
        raise NotImplementedError("Use Command Repository for delete")

    def get_by_id(self, id: int) -> Optional[Condominium]:
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.id == id
            ).first()
            
            if not db_condominium:
                return None
            
            return CondominiumMapper.to_domain(db_condominium)

    def get_by_code(self, code: str) -> Optional[Condominium]:
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.code == code
            ).first()
            
            if not db_condominium:
                return None
            
            return CondominiumMapper.to_domain(db_condominium)

    def get_by_status(self, status: int) -> List[Condominium]:
        with session_scope() as session:
            db_condominiums = session.query(DBCondominiums).filter(
                DBCondominiums.status == status
            ).all()
            return [CondominiumMapper.to_domain(db) for db in db_condominiums]
