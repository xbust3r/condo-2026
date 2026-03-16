from typing import Optional, List

from chalicelib.dddpy.example.domain.example_entity import ExampleEntity
from chalicelib.dddpy.example.domain.example_query_repository import ExampleQueryRepository
from chalicelib.dddpy.example.infrastructure.dbexample import DBExample
from chalicelib.dddpy.example.infrastructure.example_mapper import ExampleMapper
from chalicelib.dddpy.shared.postgresql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger


logger = Logger("ExampleQueryRepository")


class ExampleQueryRepositoryImpl(ExampleQueryRepository):

    def __init__(self):
        logger.info("ExampleQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[ExampleEntity]:
        logger.info(f"Fetching example by id={id}")
        with session_scope() as session:
            db_example = session.query(DBExample).filter(DBExample.id == id).first()
            if not db_example:
                logger.warning(f"Example not found by id={id}")
                return None
            return ExampleMapper.to_domain(db_example)

    def get_by_code(self, code: str) -> Optional[ExampleEntity]:
        logger.info(f"Fetching example by code={code}")
        with session_scope() as session:
            db_example = session.query(DBExample).filter(DBExample.code == code).first()
            if not db_example:
                logger.warning(f"Example not found by code={code}")
                return None
            return ExampleMapper.to_domain(db_example)

    def get_by_name(self, name: str) -> Optional[ExampleEntity]:
        logger.info(f"Fetching example by name={name}")
        with session_scope() as session:
            db_example = session.query(DBExample).filter(DBExample.name == name).first()
            if not db_example:
                logger.warning(f"Example not found by name={name}")
                return None
            return ExampleMapper.to_domain(db_example)

    def list_all(self) -> List[ExampleEntity]:
        logger.info("Listing all examples")
        with session_scope() as session:
            db_examples = session.query(DBExample).all()
            logger.info(f"Found {len(db_examples)} examples")
            return [ExampleMapper.to_domain(db) for db in db_examples]
