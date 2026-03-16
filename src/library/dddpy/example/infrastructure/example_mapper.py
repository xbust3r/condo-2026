"""
Example Mapper - Transforma entre DB y Domain.
"""
from chalicelib.dddpy.example.infrastructure.dbexample import DBExample
from chalicelib.dddpy.example.domain.example_entity import ExampleEntity


class ExampleMapper:
    """Mapper para convertir entre DBExample y ExampleEntity."""

    @staticmethod
    def to_domain(db_example: DBExample) -> ExampleEntity:
        """Convierte modelo DB a entidad de dominio."""
        return ExampleEntity(
            id=db_example.id,
            code=db_example.code,
            name=db_example.name,
            description=db_example.description,
            created_at=db_example.created_at,
            updated_at=db_example.updated_at,
        )

    @staticmethod
    def to_infrastructure(example: ExampleEntity) -> DBExample:
        """Convierte entidad de dominio a modelo DB."""
        return DBExample(
            id=example.id,
            code=example.code,
            name=example.name,
            description=example.description,
            created_at=example.created_at,
            updated_at=example.updated_at,
        )
