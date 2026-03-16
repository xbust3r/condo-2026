# Condominium Command Repository Implementation
from typing import List
from library.dddpy.core_condominiums.domain.condominiums import Condominium
from library.dddpy.core_condominiums.domain.condominiums_repository import CondominiumRepository
from library.dddpy.core_condominiums.domain.condominiums_exception import (
    CondominiumNotFoundException,
    CondominiumAlreadyExistsException,
)
from library.dddpy.core_condominiums.infrastructure.condominiums import DBCondominiums
from library.dddpy.core_condominiums.infrastructure.condominiums_mapper import CondominiumMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger

logger = Logger("CondominiumCmdRepository")


class CondominiumCmdRepositoryImpl(CondominiumRepository):
    
    def __init__(self):
        logger.info("CondominiumCmdRepositoryImpl initialized")

    def all(self) -> List[Condominium]:
        with session_scope() as session:
            db_condominiums = session.query(DBCondominiums).all()
            return [CondominiumMapper.to_domain(db) for db in db_condominiums]

    def create(self, data: dict) -> Condominium:
        with session_scope() as session:
            # Check if code already exists
            existing = session.query(DBCondominiums).filter(
                DBCondominiums.code == data.get("code")
            ).first()
            if existing:
                raise CondominiumAlreadyExistsException(data.get("code"))
            
            db_condominium = DBCondominiums(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                size=data.get("size"),
                percentage=data.get("percentage"),
                status=data.get("status", 1),
            )
            session.add(db_condominium)
            session.flush()
            session.refresh(db_condominium)
            return CondominiumMapper.to_domain(db_condominium)

    def update(self, id: int, data: dict) -> Condominium:
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.id == id
            ).first()
            
            if not db_condominium:
                raise CondominiumNotFoundException(id)
            
            # Check for duplicate code if changing
            if data.get("code") and data.get("code") != db_condominium.code:
                existing = session.query(DBCondominiums).filter(
                    DBCondominiums.code == data.get("code"),
                    DBCondominiums.id != id
                ).first()
                if existing:
                    raise CondominiumAlreadyExistsException(data.get("code"))
            
            for key, value in data.items():
                if hasattr(db_condominium, key) and value is not None:
                    setattr(db_condominium, key, value)
            
            session.flush()
            session.refresh(db_condominium)
            return CondominiumMapper.to_domain(db_condominium)

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.id == id
            ).first()
            
            if not db_condominium:
                raise CondominiumNotFoundException(id)
            
            session.delete(db_condominium)
            return True

    def get_by_id(self, id: int) -> Condominium:
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.id == id
            ).first()
            
            if not db_condominium:
                raise CondominiumNotFoundException(id)
            
            return CondominiumMapper.to_domain(db_condominium)

    def get_by_code(self, code: str) -> Condominium:
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.code == code
            ).first()
            
            if not db_condominium:
                raise CondominiumNotFoundException()
            
            return CondominiumMapper.to_domain(db_condominium)

    def get_by_status(self, status: int) -> List[Condominium]:
        with session_scope() as session:
            db_condominiums = session.query(DBCondominiums).filter(
                DBCondominiums.status == status
            ).all()
            return [CondominiumMapper.to_domain(db) for db in db_condominiums]
