from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from chalicelib.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesCmdRepository
from chalicelib.dddpy.core_buildings_types.infrastructure.buildings_types import DBBuildingsTypes
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.timezone import Timezone

logging = Logger("buildings_types_cmd_repository")


class BuildingsTypesCmdRepositoryImpl(BuildingsTypesCmdRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("BuildingsTypesCmdRepositoryImpl initialized")
    
    def create(self, data: dict) -> BuildingsTypes:
        logging.add_inside_method("create")
        logging.info(f"Creating building type: {data.get('name')}")
        
        with session_scope() as session:
            today = Timezone.get_datetime()
            db_building_type = DBBuildingsTypes(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                created_at=today,
                updated_at=today
            )
            session.add(db_building_type)
            session.commit()
            session.refresh(db_building_type)
            logging.info(f"Building type created with id: {db_building_type.id}")
            return BuildingsTypes.from_db(db_building_type)
    
    def update(self, id: int, data: dict) -> BuildingsTypes:
        logging.add_inside_method("update")
        logging.info(f"Updating building type id: {id}")
        
        with session_scope() as session:
            db_building_type = session.query(DBBuildingsTypes).filter(DBBuildingsTypes.id == id).first()
            
            if not db_building_type:
                logging.error(f"Building type not found: {id}")
                raise Exception("Building type not found")
            
            for key, value in data.items():
                if hasattr(db_building_type, key) and value is not None:
                    setattr(db_building_type, key, value)
            
            db_building_type.updated_at = Timezone.get_datetime()
            session.commit()
            session.refresh(db_building_type)
            logging.info(f"Building type updated: {id}")
            return BuildingsTypes.from_db(db_building_type)
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting building type id: {id}")
        
        with session_scope() as session:
            db_building_type = session.query(DBBuildingsTypes).filter(DBBuildingsTypes.id == id).first()
            
            if not db_building_type:
                logging.error(f"Building type not found: {id}")
                return False
            
            session.delete(db_building_type)
            session.commit()
            logging.info(f"Building type deleted: {id}")
            return True
