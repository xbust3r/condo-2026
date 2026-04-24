"""
from typing import Optional
Incident query use case — read operations.
"""
from typing import Optional, List, Tuple

from library.dddpy.core_incidents.domain.incident_entity import IncidentEntity
from library.dddpy.core_incidents.domain.incident_query_repository import IncidentQueryRepository
from library.dddpy.shared.logging.logging import Logger


logger = Logger("IncidentQueryUseCase")


class IncidentQueryUseCase:

    def __init__(self, repository: IncidentQueryRepository):
        self.repository = repository
        logger.info("IncidentQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[IncidentEntity]:
        logger.debug(f"Querying incident by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[IncidentEntity]:
        logger.debug(f"Querying incident by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        reported_by_user_id: Optional[int] = None,
        assigned_to_user_id: Optional[int] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        is_escalated: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            building_id=building_id,
            unit_id=unit_id,
            reported_by_user_id=reported_by_user_id,
            assigned_to_user_id=assigned_to_user_id,
            category=category,
            priority=priority,
            status=status,
            is_escalated=is_escalated,
            include_deleted=include_deleted,
        )

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        assigned_to_user_id: Optional[int] = None,
        is_escalated: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents for condominium_id={condominium_id}")
        return self.repository.list_by_condominium(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            status=status,
            priority=priority,
            category=category,
            building_id=building_id,
            unit_id=unit_id,
            assigned_to_user_id=assigned_to_user_id,
            is_escalated=is_escalated,
            include_deleted=include_deleted,
        )

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents for user_id={user_id}")
        return self.repository.list_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents for unit_id={unit_id}")
        return self.repository.list_by_unit(
            unit_id=unit_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_assigned_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents assigned to user_id={user_id}")
        return self.repository.list_by_assigned_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def list_active(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing active incidents skip={skip} limit={limit}")
        return self.repository.list_active(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
        )
