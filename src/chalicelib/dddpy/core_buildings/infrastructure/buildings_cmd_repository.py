from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
from chalicelib.dddpy.core_buildings.domain.buildings_repository import BuildingsCmdRepository
from chalicelib.dddpy.core_buildings.infrastructure.buildings import DBBuildings
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.timezone import Timezone

logging = Logger("buildings_cmd_repository")


class BuildingsCmdRepositoryImpl(BuildingsCmdRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("BuildingsCmdRepositoryImpl initialized")
    
    def create(self, data: dict) -> Buildings:
        logging.add_inside_method("create")
        logging.info(f"Creating building: {data.get('name')}")
        
        with session_scope() as session:
            today = Timezone.get_datetime()
            db_building = DBBuildings(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                size=data.get("size"),
                percentage=data.get("percentage"),
                type=data.get("type"),
                condominium_id=data.get("condominium_id"),
                building_type_id=data.get("building_type_id"),
                created_at=today,
                updated_at=today
            )
            session.add(db_building)
            session.commit()
            session.refresh(db_building)
            logging.info(f"Building created with id: {db_building.id}")
            return Buildings.from_db(db_building)
    
    def update(self, id: int, data: dict) -> Buildings:
        logging.add_inside_method("update")
        logging.info(f"Updating building id: {id}")
        
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.id == id).first()
            
            if not db_building:
                logging.error(f"Building not found: {id}")
                raise Exception("Building not found")
            
            for key, value in data.items():
                if hasattr(db_building, key) and value is not None:
                    setattr(db_building, key, value)
            
            db_building.updated_at = Timezone.get_datetime()
            session.commit()
            session.refresh(db_building)
            logging.info(f"Building updated: {id}")
            return Buildings.from_db(db_building)
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting building id: {id}")
        
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.id == id).first()
            
            if not db_building:
                logging.error(f"Building not found: {id}")
                return False
            
            session.delete(db_building)
            session.commit()
            logging.info(f"Building deleted: {id}")
            return True
