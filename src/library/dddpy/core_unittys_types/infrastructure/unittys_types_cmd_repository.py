# Mapper and Repository for Unity Types
from typing import List, Optional
from library.dddpy.core_unittys_types.domain.unittys_types import (
    UnittysTypes,
    UnittysTypesRepository,
    UnittysTypesNotFoundException,
    UnittysTypesAlreadyExistsException,
)
from library.dddpy.core_unittys_types.infrastructure.unittys_types import DBUnittysTypes
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger

logger = Logger("UnittysTypesRepository")


class UnittysTypesMapper:
    
    @staticmethod
    def to_domain(db_type: DBUnittysTypes) -> UnittysTypes:
        return UnittysTypes(
            id=db_type.id,
            name=db_type.name,
            code=db_type.code,
            description=db_type.description,
            status=db_type.status,
            created_at=db_type.created_at,
            updated_at=db_type.updated_at,
        )


class UnittysTypesCmdRepositoryImpl(UnittysTypesRepository):
    
    def all(self) -> List[UnittysTypes]:
        with session_scope() as session:
            db_types = session.query(DBUnittysTypes).all()
            return [UnittysTypesMapper.to_domain(db) for db in db_types]

    def create(self, data: dict) -> UnittysTypes:
        with session_scope() as session:
            existing = session.query(DBUnittysTypes).filter(
                DBUnittysTypes.code == data.get("code")
            ).first()
            if existing:
                raise UnittysTypesAlreadyExistsException(data.get("code"))
            
            db_type = DBUnittysTypes(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                status=data.get("status", 1),
            )
            session.add(db_type)
            session.flush()
            session.refresh(db_type)
            return UnittysTypesMapper.to_domain(db_type)

    def update(self, id: int, data: dict) -> UnittysTypes:
        with session_scope() as session:
            db_type = session.query(DBUnittysTypes).filter(
                DBUnittysTypes.id == id
            ).first()
            
            if not db_type:
                raise UnittysTypesNotFoundException(id)
            
            for key, value in data.items():
                if hasattr(db_type, key) and value is not None:
                    setattr(db_type, key, value)
            
            session.flush()
            session.refresh(db_type)
            return UnittysTypesMapper.to_domain(db_type)

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            db_type = session.query(DBUnittysTypes).filter(
                DBUnittysTypes.id == id
            ).first()
            
            if not db_type:
                raise UnittysTypesNotFoundException(id)
            
            session.delete(db_type)
            return True

    def get_by_id(self, id: int) -> UnittysTypes:
        with session_scope() as session:
            db_type = session.query(DBUnittysTypes).filter(
                DBUnittysTypes.id == id
            ).first()
            
            if not db_type:
                raise UnittysTypesNotFoundException(id)
            
            return UnittysTypesMapper.to_domain(db_type)

    def get_by_code(self, code: str) -> UnittysTypes:
        with session_scope() as session:
            db_type = session.query(DBUnittysTypes).filter(
                DBUnittysTypes.code == code
            ).first()
            
            if not db_type:
                raise UnittysTypesNotFoundException()
            
            return UnittysTypesMapper.to_domain(db_type)


class UnittysTypesQueryRepositoryImpl(UnittysTypesRepository):
    
    def all(self) -> List[UnittysTypes]:
        with session_scope() as session:
            db_types = session.query(DBUnittysTypes).all()
            return [UnittysTypesMapper.to_domain(db) for db in db_types]

    def create(self, data: dict):
        raise NotImplementedError("Use Command Repository")

    def update(self, id: int, data: dict):
        raise NotImplementedError("Use Command Repository")

    def delete(self, id: int):
        raise NotImplementedError("Use Command Repository")

    def get_by_id(self, id: int) -> Optional[UnittysTypes]:
        with session_scope() as session:
            db_type = session.query(DBUnittysTypes).filter(
                DBUnittysTypes.id == id
            ).first()
            return UnittysTypesMapper.to_domain(db_type) if db_type else None

    def get_by_code(self, code: str) -> Optional[UnittysTypes]:
        with session_scope() as session:
            db_type = session.query(DBUnittysTypes).filter(
                DBUnittysTypes.code == code
            ).first()
            return UnittysTypesMapper.to_domain(db_type) if db_type else None
