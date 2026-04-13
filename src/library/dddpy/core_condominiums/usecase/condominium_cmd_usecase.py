from typing import Optional
from decimal import Decimal

from library.dddpy.core_condominiums.usecase.condominium_cmd_schema import CreateCondominiumSchema, UpdateCondominiumSchema
from library.dddpy.core_condominiums.domain.condominium_cmd_repository import CondominiumCmdRepository
from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity
from library.dddpy.core_condominiums.domain.condominium_data import CreateCondominiumData, UpdateCondominiumData
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumCmdUseCase")


class CondominiumCmdUseCase:

    def __init__(self, repository: CondominiumCmdRepository):
        self.repository = repository
        logger.info("CondominiumCmdUseCase initialized")

    def create(self, schema: CreateCondominiumSchema) -> CondominiumEntity:
        logger.info(f"Delegating condominium creation for code={schema.code}")
        data = CreateCondominiumData(
            code=schema.code,
            name=schema.name,
            description=schema.description,
            size=Decimal(str(schema.size)) if schema.size else None,
            percentage=Decimal(str(schema.percentage)) if schema.percentage else None,
        )
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateCondominiumSchema) -> Optional[CondominiumEntity]:
        logger.info(f"Delegating condominium update for id={id}")
        data = UpdateCondominiumData(
            name=schema.name,
            description=schema.description,
            size=Decimal(str(schema.size)) if schema.size else None,
            percentage=Decimal(str(schema.percentage)) if schema.percentage else None,
            status=schema.status,
        )
        return self.repository.update(id, data)

    def delete(self, id: int) -> bool:
        logger.info(f"Delegating condominium delete for id={id}")
        return self.repository.delete(id)