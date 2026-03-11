from typing import Optional, List
from chalicelib.dddpy.users.domain.users import Users
from chalicelib.dddpy.users.domain.users_repository import UsersQueryRepository
from chalicelib.dddpy.users.infrastructure.users import DBUsers
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("users_query_repository")


class UsersQueryRepositoryImpl(UsersQueryRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("UsersQueryRepositoryImpl initialized")
    
    def get_by_id(self, id: int) -> Optional[Users]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting user by id: {id}")
        
        with session_scope() as session:
            db_user = session.query(DBUsers).filter(DBUsers.id == id).first()
            if db_user:
                return Users.from_db(db_user)
            return None
    
    def get_by_email(self, email: str) -> Optional[Users]:
        logging.add_inside_method("get_by_email")
        logging.info(f"Getting user by email: {email}")
        
        with session_scope() as session:
            db_user = session.query(DBUsers).filter(DBUsers.email == email).first()
            if db_user:
                return Users.from_db(db_user)
            return None
    
    def get_all(self) -> List[Users]:
        logging.add_inside_method("get_all")
        logging.info("Getting all users")
        
        with session_scope() as session:
            db_users = session.query(DBUsers).all()
            return [Users.from_db(db) for db in db_users]
    
    def get_by_status(self, status: str) -> List[Users]:
        logging.add_inside_method("get_by_status")
        logging.info(f"Getting users by status: {status}")
        
        with session_scope() as session:
            db_users = session.query(DBUsers).filter(DBUsers.status == status).all()
            return [Users.from_db(db) for db in db_users]
