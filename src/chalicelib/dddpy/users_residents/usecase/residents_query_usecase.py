from typing import Optional, List
from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
from chalicelib.dddpy.users_residents.domain.residents_repository import UsersResidentsQueryRepository
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("residents_query_usecase")


class UsersResidentsQueryUseCase:
    def __init__(self, repository: UsersResidentsQueryRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[UsersResidents]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting resident by id: {id}")
        return self.repository.get_by_id(id)
    
    def get_by_user_id(self, user_id: int) -> Optional[UsersResidents]:
        logging.add_inside_method("get_by_user_id")
        logging.info(f"Getting resident by user_id: {user_id}")
        return self.repository.get_by_user_id(user_id)
    
    def get_all(self) -> List[UsersResidents]:
        logging.add_inside_method("get_all")
        logging.info("Getting all residents")
        return self.repository.get_all()
    
    def get_by_unity_id(self, unity_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_unity_id")
        logging.info(f"Getting residents by unity_id: {unity_id}")
        return self.repository.get_by_unity_id(unity_id)
    
    def get_by_building_id(self, building_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_building_id")
        logging.info(f"Getting residents by building_id: {building_id}")
        return self.repository.get_by_building_id(building_id)
    
    def get_by_condominium_id(self, condominium_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_condominium_id")
        logging.info(f"Getting residents by condominium_id: {condominium_id}")
        return self.repository.get_by_condominium_id(condominium_id)
    
    def get_by_status(self, status: str) -> List[UsersResidents]:
        logging.add_inside_method("get_by_status")
        logging.info(f"Getting residents by status: {status}")
        return self.repository.get_by_status(status)
