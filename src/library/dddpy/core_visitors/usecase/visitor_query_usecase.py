"""
Visitor query use case — read operations.
"""
from typing import Optional, List, Tuple

from library.dddpy.core_visitors.domain.visitor_entity import VisitorEntity
from library.dddpy.core_visitors.domain.visitor_query_repository import VisitorQueryRepository
from library.dddpy.shared.logging.logging import Logger


logger = Logger("VisitorQueryUseCase")


class VisitorQueryUseCase:

    def __init__(self, repository: VisitorQueryRepository):
        self.repository = repository
        logger.info("VisitorQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[VisitorEntity]:
        logger.debug(f"Querying visitor by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[VisitorEntity]:
        logger.debug(f"Querying visitor by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        host_user_id: Optional[int] = None,
        status: Optional[str] = None,
        expected_date: Optional[str] = None,
        visit_purpose: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            building_id=building_id,
            unit_id=unit_id,
            host_user_id=host_user_id,
            status=status,
            expected_date=expected_date,
            visit_purpose=visit_purpose,
            include_deleted=include_deleted,
        )

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        expected_date: Optional[str] = None,
        visit_purpose: Optional[str] = None,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors for condominium_id={condominium_id}")
        return self.repository.list_by_condominium(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            status=status,
            expected_date=expected_date,
            visit_purpose=visit_purpose,
            building_id=building_id,
            unit_id=unit_id,
            include_deleted=include_deleted,
        )

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors for unit_id={unit_id}")
        return self.repository.list_by_unit(
            unit_id=unit_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_host(
        self,
        host_user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors for host_user_id={host_user_id}")
        return self.repository.list_by_host(
            host_user_id=host_user_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_date(
        self,
        condominium_id: int,
        expected_date: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors for date={expected_date}, condo={condominium_id}")
        return self.repository.list_by_date(
            condominium_id=condominium_id,
            expected_date=expected_date,
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
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing active visitors skip={skip} limit={limit}")
        return self.repository.list_active(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
        )

    def get_by_access_code(
        self,
        access_code: str,
        condominium_id: Optional[int] = None,
    ) -> Optional[VisitorEntity]:
        logger.debug(f"Querying visitor by access_code={access_code}")
        return self.repository.get_by_access_code(access_code, condominium_id)