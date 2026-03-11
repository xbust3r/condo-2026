from chalicelib.dddpy.core_unitys.domain.unitys import Unitys
from chalicelib.dddpy.core_unitys.domain.unitys_repository import UnitysCmdRepository
from chalicelib.dddpy.core_unitys.infrastructure.unitys import DBUnitys
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.timezone import Timezone

logging = Logger("unitys_cmd_repository")


class UnitysCmdRepositoryImpl(UnitysCmdRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("UnitysCmdRepositoryImpl initialized")
    
    def create(self, data: dict) -> Unitys:
        logging.add_inside_method("create")
        logging.info(f"Creating unity: {data.get('name')}")
        
        with session_scope() as session:
            today = Timezone.get_datetime()
            db_unity = DBUnitys(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                size=data.get("size"),
                percentage=data.get("percentage"),
                type=data.get("type"),
                floor=data.get("floor"),
                unit=data.get("unit"),
                building_id=data.get("building_id"),
                unity_type_id=data.get("unity_type_id"),
                created_at=today,
                updated_at=today
            )
            session.add(db_unity)
            session.commit()
            session.refresh(db_unity)
            logging.info(f"Unity created with id: {db_unity.id}")
            return Unitys.from_db(db_unity)
    
    def update(self, id: int, data: dict) -> Unitys:
        logging.add_inside_method("update")
        logging.info(f"Updating unity id: {id}")
        
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(DBUnitys.id == id).first()
            
            if not db_unity:
                logging.error(f"Unity not found: {id}")
                raise Exception("Unity not found")
            
            for key, value in data.items():
                if hasattr(db_unity, key) and value is not None:
                    setattr(db_unity, key, value)
            
            db_unity.updated_at = Timezone.get_datetime()
            session.commit()
            session.refresh(db_unity)
            logging.info(f"Unity updated: {id}")
            return Unitys.from_db(db_unity)
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting unity id: {id}")
        
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(DBUnitys.id == id).first()
            
            if not db_unity:
                logging.error(f"Unity not found: {id}")
                return False
            
            session.delete(db_unity)
            session.commit()
            logging.info(f"Unity deleted: {id}")
            return True
