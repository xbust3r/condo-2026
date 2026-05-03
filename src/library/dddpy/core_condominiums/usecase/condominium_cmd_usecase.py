from typing import Optional
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
            land_area=Decimal(str(schema.land_area)) if schema.land_area else None,
            built_area=Decimal(str(schema.built_area)) if schema.built_area else None,
            area_unit=schema.area_unit or 'm2',
            legal_name=schema.legal_name,
            document_number=schema.document_number,
            address=schema.address,
            city=schema.city,
            country=schema.country,
            contact_email=schema.contact_email,
            contact_phone=schema.contact_phone,
            theme_id=schema.theme_id,
            amenity_settings=schema.amenity_settings,
        )
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateCondominiumSchema) -> Optional[CondominiumEntity]:
        logger.info(f"Delegating condominium update for id={id}")
        data = UpdateCondominiumData(
            name=schema.name,
            description=schema.description,
            land_area=Decimal(str(schema.land_area)) if schema.land_area else None,
            built_area=Decimal(str(schema.built_area)) if schema.built_area else None,
            area_unit=schema.area_unit,
            legal_name=schema.legal_name,
            document_number=schema.document_number,
            address=schema.address,
            city=schema.city,
            country=schema.country,
            contact_email=schema.contact_email,
            contact_phone=schema.contact_phone,
            status=schema.status,
            theme_id=schema.theme_id,
            amenity_settings=schema.amenity_settings,
        )
        return self.repository.update(id, data)

    def delete(self, id: int) -> bool:
        logger.info(f"Delegating condominium delete (soft) for id={id}")
        return self.repository.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Delegating condominium restore for id={id}")
        return self.repository.restore(id)
