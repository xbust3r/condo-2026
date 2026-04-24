from typing import Optional, List

from library.dddpy.core_units.domain.unit_query_repository import UnitQueryRepository
from library.dddpy.core_units.domain.unit_entity import UnitEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitQueryUseCase")


class UnitQueryUseCase:

    def __init__(self, repository: UnitQueryRepository):
        self.repository = repository
        logger.info("UnitQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[UnitEntity]:
        logger.debug(f"Querying unit by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[UnitEntity]:
        logger.debug(f"Querying unit by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def get_by_unit_number_in_building(
        self, building_id: int, unit_number: str
    ) -> Optional[UnitEntity]:
        return self.repository.get_by_unit_number_in_building(building_id, unit_number)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unit_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnitEntity], int]:
        logger.debug(f"Listing units skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            building_id=building_id,
            unit_type_id=unit_type_id,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_building(
        self,
        building_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnitEntity], int]:
        logger.debug(f"Listing units for building_id={building_id}")
        return self.repository.list_by_building(
            building_id=building_id,
            skip=skip,
            limit=limit,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )

    def count_active_residents(self, unit_id: int) -> int:
        logger.debug(f"Counting active residents for unit_id={unit_id}")
        return self.repository.count_active_residents(unit_id)

    def _get_by_id_any_status(self, id: int) -> Optional[UnitEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Delegating unit fetch by id={id} (any status)")
        return self.repository._get_by_id_any_status(id)

    def get_consolidated_view(self, unit_id: int) -> dict:
        """
        Phase 1e: Get a consolidated view of a unit.

        Returns unit + active owners + active occupants + warnings.
        Warnings include:
          - ownership_percentage_sum: sum of all active ownership percentages
          - multiple_primary_occupancies: more than one primary occupant
        """
        unit = self.repository.get_by_id(unit_id)
        if not unit:
            from library.dddpy.core_units.domain.unit_exception import UnitNotFound
            raise UnitNotFound(f"Unit with id={unit_id} not found")

        result = {
            "unit": unit.to_dict(),
            "warnings": [],
        }

        # 1. Active ownerships
        from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import (
            UnitOwnershipQueryRepositoryImpl,
        )
        ownership_repo = UnitOwnershipQueryRepositoryImpl()
        ownerships, total_ownerships = ownership_repo.list_by_unit(
            unit_id=unit_id,
            status="active",
            include_deleted=False,
        )
        ownerships_data = [o.to_dict() for o in ownerships]
        result["ownerships"] = {
            "items": ownerships_data,
            "total": total_ownerships,
        }

        # Warning: sum of ownership percentages
        ownership_sum = sum(float(o.ownership_percentage) for o in ownerships)
        if ownerships:
            result["warnings"].append({
                "type": "ownership_percentage_sum",
                "value": round(ownership_sum, 2),
                "message": f"Active ownership sum: {ownership_sum}%"
            })

        # 2. Active occupancies
        from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_query_repository import (
            UnitOccupancyQueryRepositoryImpl,
        )
        occupancy_repo = UnitOccupancyQueryRepositoryImpl()
        occupancies, total_occupancies = occupancy_repo.list_by_unit(
            unit_id=unit_id,
            status="active",
            include_deleted=False,
        )
        result["occupancies"] = {
            "items": [o.to_dict() for o in occupancies],
            "total": total_occupancies,
        }

        # Warning: multiple primary occupants
        primary_count = sum(1 for o in occupancies if o.is_primary)
        if primary_count > 1:
            result["warnings"].append({
                "type": "multiple_primary_occupancies",
                "value": primary_count,
                "message": f"{primary_count} primary occupants found (expected: 1)"
            })

        return result

    def list_units_for_buildings(
        self,
        skip: int = 0,
        limit: int = 100,
        building_ids: Optional[List[int]] = None,
        building_id: Optional[int] = None,
        unit_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnitEntity], int]:
        logger.debug(f"Listing units for building_ids={building_ids}")
        return self.repository.list_units_for_buildings(
            skip=skip,
            limit=limit,
            building_ids=building_ids,
            building_id=building_id,
            unit_type_id=unit_type_id,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )
