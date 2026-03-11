from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
from chalicelib.dddpy.core_unittys_types.domain.unittys_types_repository import UnitysTypesCmdRepository
from chalicelib.dddpy.core_unittys_types.infrastructure.unittys_types import DBUnitysTypes
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.timezone import Timezone

logging = Logger("unittys_types_cmd_repository")


class UnitysTypesCmdRepositoryImpl(UnitysTypesCmdRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("UnitysTypesCmdRepositoryImpl initialized")
    
    def create(self, data: dict) -> UnitysTypes:
        logging.add_inside_method("create")
        logging.info(f"Creating unity type: {data.get('name')}")
        
        with session_scope() as session:
            today = Timezone.get_datetime()
            db_unity_type = DBUnitysTypes(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                created_at=today,
                updated_at=today
            )
            session.add(db_unity_type)
            session.commit()
            session.refresh(db_unity_type)
            logging.info(f"Unity type created with id: {db_unity_type.id}")
            return UnitysTypes.from_db(db_unity_type)
    
    def update(self, id: int, data: dict) -> UnitysTypes:
        logging.add_inside_method("update")
        logging.info(f"Updating unity type id: {id}")
        
        with session_scope() as session:
            db_unity_type = session.query(DBUnitysTypes).filter(DBUnitysTypes.id == id).first()
            
            if not db_unity_type:
                logging.error(f"Unity type not found: {id}")
                raise Exception("Unity type not found")
            
            for key, value in data.items():
                if hasattr(db_unity_type, key) and value is not None:
                    setattr(db_unity_type, key, value)
            
            db_unity_type.updated_at = Timezone.get_datetime()
            session.commit()
            session.refresh(db_unity_type)
            logging.info(f"Unity type updated: {id}")
            return UnitysTypes.from_db(db_unity_type)
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting unity type id: {id}")
        
        with session_scope() as session:
            db_unity_type = session.query(DBUnitysTypes).filter(DBUnitysTypes.id == id).first()
            
            if not db_unity_type:
                logging.error(f"Unity type not found: {id}")
                return False
            
            session.delete(db_unity_type)
            session.commit()
            logging.info(f"Unity type deleted: {id}")
            return True
