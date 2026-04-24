"""
OccupancyType command use case — handles write operations.
"""
from library.dddpy.core_occupancy_types.domain.occupancy_type_data import (
    CreateOccupancyTypeData,
    UpdateOccupancyTypeData,
)
from library.dddpy.core_occupancy_types.domain.occupancy_type_entity import OccupancyTypeEntity
from library.dddpy.core_occupancy_types.domain.occupancy_type_cmd_repository import (
    OccupancyTypeCmdRepository,
)
from library.dddpy.core_occupancy_types.infrastructure.occupancy_type_cmd_repository import (
    OccupancyTypeCmdRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("OccupancyTypeCmdUseCase")


class OccupancyTypeCmdUseCase:
    def __init__(self):
        self._repository: OccupancyTypeCmdRepository = OccupancyTypeCmdRepositoryImpl()

    def create(self, data: CreateOccupancyTypeData) -> OccupancyTypeEntity:
        logger.info(f"OccupancyTypeCmdUseCase.create code={data.code}")
        entity = self._repository.create(data)
        logger.info(f"OccupancyType created id={entity.id}")
        return entity

    def update(self, id: int, data: UpdateOccupancyTypeData) -> OccupancyTypeEntity:
        logger.info(f"OccupancyTypeCmdUseCase.update id={id}")
        entity = self._repository.update(id, data)
        if not entity:
            raise ValueError(f"OccupancyType id={id} not found")
        logger.info(f"OccupancyType updated id={id}")
        return entity

    def soft_delete(self, id: int) -> bool:
        logger.info(f"OccupancyTypeCmdUseCase.soft_delete id={id}")
        return self._repository.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"OccupancyTypeCmdUseCase.restore id={id}")
        return self._repository.restore(id)

    def hard_delete(self, id: int) -> bool:
        logger.info(f"OccupancyTypeCmdUseCase.hard_delete id={id}")
        return self._repository.hard_delete(id)


_occupancy_type_cmd_instance: OccupancyTypeCmdUseCase | None = None


def occupancy_type_cmd_usecase_factory() -> OccupancyTypeCmdUseCase:
    global _occupancy_type_cmd_instance
    if _occupancy_type_cmd_instance is None:
        _occupancy_type_cmd_instance = OccupancyTypeCmdUseCase()
    return _occupancy_type_cmd_instance