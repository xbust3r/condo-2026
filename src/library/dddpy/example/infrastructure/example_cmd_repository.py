from typing import Optional

from chalicelib.dddpy.example.domain.example_entity import ExampleEntity
from chalicelib.dddpy.example.domain.example_data import CreateExampleData, UpdateExampleData
from chalicelib.dddpy.example.domain.example_cmd_repository import ExampleCmdRepository
from chalicelib.dddpy.example.infrastructure.dbexample import DBExample
from chalicelib.dddpy.example.infrastructure.example_mapper import ExampleMapper
from chalicelib.dddpy.shared.postgresql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger


logger = Logger("ExampleCmdRepository")


class ExampleCmdRepositoryImpl(ExampleCmdRepository):

    def __init__(self):
        logger.info("ExampleCmdRepositoryImpl initialized")

    def create(self, data: CreateExampleData) -> ExampleEntity:
        logger.info(f"Creating example with code={data.code}")
        with session_scope() as session:
            db_example = DBExample(
                code=data.code,
                name=data.name,
                description=data.description,
            )
            session.add(db_example)
            session.flush()
            session.refresh(db_example)
            logger.info(f"Example created with id={db_example.id}")
            return ExampleMapper.to_domain(db_example)

    def update(self, id: int, data: UpdateExampleData) -> Optional[ExampleEntity]:
        logger.info(f"Updating example id={id}")
        with session_scope() as session:
            db_example = session.query(DBExample).filter(DBExample.id == id).first()
            if not db_example:
                logger.warning(f"Example not found for update id={id}")
                return None
            if data.name is not None:
                db_example.name = data.name
            if data.description is not None:
                db_example.description = data.description
            session.flush()
            session.refresh(db_example)
            logger.info(f"Example updated id={id}")
            return ExampleMapper.to_domain(db_example)

    def delete(self, id: int) -> bool:
        logger.info(f"Deleting example id={id}")
        with session_scope() as session:
            db_example = session.query(DBExample).filter(DBExample.id == id).first()
            if not db_example:
                logger.warning(f"Example not found for delete id={id}")
                return False
            session.delete(db_example)
            session.flush()
            logger.info(f"Example deleted id={id}")
            return True
