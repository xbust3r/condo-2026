from typing import Optional, List
from chalicelib.dddpy.users.domain.users import Users
from chalicelib.dddpy.users.domain.users_repository import UsersQueryRepository
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("users_query_usecase")


class UsersQueryUseCase:
    def __init__(self, repository: UsersQueryRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[Users]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting user by id: {id}")
        return self.repository.get_by_id(id)
    
    def get_by_email(self, email: str) -> Optional[Users]:
        logging.add_inside_method("get_by_email")
        logging.info(f"Getting user by email: {email}")
        return self.repository.get_by_email(email)
    
    def get_all(self) -> List[Users]:
        logging.add_inside_method("get_all")
        logging.info("Getting all users")
        return self.repository.get_all()
    
    def get_by_status(self, status: str) -> List[Users]:
        logging.add_inside_method("get_by_status")
        logging.info(f"Getting users by status: {status}")
        return self.repository.get_by_status(status)
