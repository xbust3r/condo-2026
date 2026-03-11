from chalicelib.dddpy.users.domain.users import Users
from chalicelib.dddpy.users.domain.users_repository import UsersCmdRepository
from chalicelib.dddpy.users.infrastructure.users import DBUsers
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.timezone import Timezone

logging = Logger("users_cmd_repository")


class UsersCmdRepositoryImpl(UsersCmdRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("UsersCmdRepositoryImpl initialized")
    
    def create(self, data: dict) -> Users:
        logging.add_inside_method("create")
        logging.info(f"Creating user: {data.get('email')}")
        
        with session_scope() as session:
            today = Timezone.get_datetime()
            db_user = DBUsers(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                password=data.get("password"),
                doc_identity=data.get("doc_identity"),
                phone=data.get("phone"),
                status=data.get("status", "active"),
                created_at=today,
                updated_at=today
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            logging.info(f"User created with id: {db_user.id}")
            return Users.from_db(db_user)
    
    def update(self, id: int, data: dict) -> Users:
        logging.add_inside_method("update")
        logging.info(f"Updating user id: {id}")
        
        with session_scope() as session:
            db_user = session.query(DBUsers).filter(DBUsers.id == id).first()
            
            if not db_user:
                logging.error(f"User not found: {id}")
                raise Exception("User not found")
            
            for key, value in data.items():
                if hasattr(db_user, key) and value is not None:
                    setattr(db_user, key, value)
            
            db_user.updated_at = Timezone.get_datetime()
            session.commit()
            session.refresh(db_user)
            logging.info(f"User updated: {id}")
            return Users.from_db(db_user)
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting user id: {id}")
        
        with session_scope() as session:
            db_user = session.query(DBUsers).filter(DBUsers.id == id).first()
            
            if not db_user:
                logging.error(f"User not found: {id}")
                return False
            
            session.delete(db_user)
            session.commit()
            logging.info(f"User deleted: {id}")
            return True
