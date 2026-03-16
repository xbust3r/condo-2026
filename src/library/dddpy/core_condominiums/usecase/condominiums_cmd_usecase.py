# Condominium Command Use Case
from library.dddpy.core_condominiums.domain.condominiums import Condominium
from library.dddpy.core_condominiums.domain.condominiums_repository import CondominiumRepository
from library.dddpy.core_condominiums.usecase.condominiums_cmd_schema import (
    CreateCondominiumSchema,
    UpdateCondominiumSchema,
)
from library.dddpy.shared.logging.logging import Logger

logger = Logger("CondominiumCmdUseCase")


class CondominiumCmdUseCase:
    
    def __init__(self, repository: CondominiumRepository):
        self.repository = repository

    def create(self, schema: CreateCondominiumSchema) -> Condominium:
        logger.info(f"Creating condominium with code: {schema.code}")
        data = schema.model_dump()
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateCondominiumSchema) -> Condominium:
        logger.info(f"Updating condominium with id: {id}")
        data = schema.model_dump(exclude_unset=True)
        return self.repository.update(id, data)

    def delete(self, id: int) -> bool:
        logger.info(f"Deleting condominium with id: {id}")
        return self.repository.delete(id)
