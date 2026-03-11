from typing import Optional
from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
from chalicelib.dddpy.core_condominiums.domain.condominiums_repository import CondominiumsCmdRepository
from chalicelib.dddpy.core_condominiums.infrastructure.condominiums import DBCondominiums
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.timezone import Timezone

logging = Logger("condominiums_cmd_repository")


class CondominiumsCmdRepositoryImpl(CondominiumsCmdRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("CondominiumsCmdRepositoryImpl initialized")
    
    def create(self, data: dict) -> Condominiums:
        logging.add_inside_method("create")
        logging.info(f"Creating condominium: {data.get('name')}")
        
        with session_scope() as session:
            today = Timezone.get_datetime()
            db_condominium = DBCondominiums(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                size=data.get("size"),
                percentage=data.get("percentage"),
                created_at=today,
                updated_at=today
            )
            session.add(db_condominium)
            session.commit()
            session.refresh(db_condominium)
            logging.info(f"Condominium created with id: {db_condominium.id}")
            return Condominiums.from_db(db_condominium)
    
    def update(self, id: int, data: dict) -> Condominiums:
        logging.add_inside_method("update")
        logging.info(f"Updating condominium id: {id}")
        
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(DBCondominiums.id == id).first()
            
            if not db_condominium:
                logging.error(f"Condominium not found: {id}")
                raise Exception("Condominium not found")
            
            for key, value in data.items():
                if hasattr(db_condominium, key) and value is not None:
                    setattr(db_condominium, key, value)
            
            db_condominium.updated_at = Timezone.get_datetime()
            session.commit()
            session.refresh(db_condominium)
            logging.info(f"Condominium updated: {id}")
            return Condominiums.from_db(db_condominium)
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting condominium id: {id}")
        
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(DBCondominiums.id == id).first()
            
            if not db_condominium:
                logging.error(f"Condominium not found: {id}")
                return False
            
            session.delete(db_condominium)
            session.commit()
            logging.info(f"Condominium deleted: {id}")
            return True
