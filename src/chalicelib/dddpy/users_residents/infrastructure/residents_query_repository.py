from typing import Optional, List
from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
from chalicelib.dddpy.users_residents.domain.residents_repository import UsersResidentsQueryRepository
from chalicelib.dddpy.users_residents.infrastructure.residents import DBUsersResidents
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("residents_query_repository")


class UsersResidentsQueryRepositoryImpl(UsersResidentsQueryRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("UsersResidentsQueryRepositoryImpl initialized")
    
    def get_by_id(self, id: int) -> Optional[UsersResidents]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting resident by id: {id}")
        
        with session_scope() as session:
            db_resident = session.query(DBUsersResidents).filter(DBUsersResidents.id == id).first()
            if db_resident:
                return UsersResidents.from_db(db_resident)
            return None
    
    def get_by_user_id(self, user_id: int) -> Optional[UsersResidents]:
        logging.add_inside_method("get_by_user_id")
        logging.info(f"Getting resident by user_id: {user_id}")
        
        with session_scope() as session:
            db_resident = session.query(DBUsersResidents).filter(DBUsersResidents.user_id == user_id).first()
            if db_resident:
                return UsersResidents.from_db(db_resident)
            return None
    
    def get_all(self) -> List[UsersResidents]:
        logging.add_inside_method("get_all")
        logging.info("Getting all residents")
        
        with session_scope() as session:
            db_residents = session.query(DBUsersResidents).all()
            return [UsersResidents.from_db(db) for db in db_residents]
    
    def get_by_unity_id(self, unity_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_unity_id")
        logging.info(f"Getting residents by unity_id: {unity_id}")
        
        with session_scope() as session:
            db_residents = session.query(DBUsersResidents).filter(
                DBUsersResidents.unity_id == unity_id
            ).all()
            return [UsersResidents.from_db(db) for db in db_residents]
    
    def get_by_building_id(self, building_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_building_id")
        logging.info(f"Getting residents by building_id: {building_id}")
        
        with session_scope() as session:
            db_residents = session.query(DBUsersResidents).filter(
                DBUsersResidents.building_id == building_id
            ).all()
            return [UsersResidents.from_db(db) for db in db_residents]
    
    def get_by_condominium_id(self, condominium_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_condominium_id")
        logging.info(f"Getting residents by condominium_id: {condominium_id}")
        
        with session_scope() as session:
            db_residents = session.query(DBUsersResidents).filter(
                DBUsersResidents.condominium_id == condominium_id
            ).all()
            return [UsersResidents.from_db(db) for db in db_residents]
    
    def get_by_status(self, status: str) -> List[UsersResidents]:
        logging.add_inside_method("get_by_status")
        logging.info(f"Getting residents by status: {status}")
        
        with session_scope() as session:
            db_residents = session.query(DBUsersResidents).filter(
                DBUsersResidents.status == status
            ).all()
            return [UsersResidents.from_db(db) for db in db_residents]
