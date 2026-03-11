from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
from chalicelib.dddpy.users_residents.domain.residents_repository import UsersResidentsCmdRepository
from chalicelib.dddpy.users_residents.infrastructure.residents import DBUsersResidents
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.timezone import Timezone

logging = Logger("residents_cmd_repository")


class UsersResidentsCmdRepositoryImpl(UsersResidentsCmdRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("UsersResidentsCmdRepositoryImpl initialized")
    
    def create(self, data: dict) -> UsersResidents:
        logging.add_inside_method("create")
        logging.info(f"Creating resident for user_id: {data.get('user_id')}")
        
        with session_scope() as session:
            today = Timezone.get_datetime()
            db_resident = DBUsersResidents(
                condominium_id=data.get("condominium_id"),
                building_id=data.get("building_id"),
                unity_id=data.get("unity_id"),
                type=data.get("type"),
                status=data.get("status", "active"),
                user_id=data.get("user_id"),
                created_at=today,
                updated_at=today
            )
            session.add(db_resident)
            session.commit()
            session.refresh(db_resident)
            logging.info(f"Resident created with id: {db_resident.id}")
            return UsersResidents.from_db(db_resident)
    
    def update(self, id: int, data: dict) -> UsersResidents:
        logging.add_inside_method("update")
        logging.info(f"Updating resident id: {id}")
        
        with session_scope() as session:
            db_resident = session.query(DBUsersResidents).filter(DBUsersResidents.id == id).first()
            
            if not db_resident:
                logging.error(f"Resident not found: {id}")
                raise Exception("Resident not found")
            
            for key, value in data.items():
                if hasattr(db_resident, key) and value is not None:
                    setattr(db_resident, key, value)
            
            db_resident.updated_at = Timezone.get_datetime()
            session.commit()
            session.refresh(db_resident)
            logging.info(f"Resident updated: {id}")
            return UsersResidents.from_db(db_resident)
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting resident id: {id}")
        
        with session_scope() as session:
            db_resident = session.query(DBUsersResidents).filter(DBUsersResidents.id == id).first()
            
            if not db_resident:
                logging.error(f"Resident not found: {id}")
                return False
            
            session.delete(db_resident)
            session.commit()
            logging.info(f"Resident deleted: {id}")
            return True
