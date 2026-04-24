"""
from typing import Optional
Incident query repository ABC — read operations.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from library.dddpy.core_incidents.domain.incident_entity import IncidentEntity


class IncidentQueryRepository(ABC):
    """Interfaz de lectura para consultas de incidents."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[IncidentEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[IncidentEntity]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        pass

    @abstractmethod
    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        pass

    @abstractmethod
    def list_by_assigned_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        pass

    @abstractmethod
    def list_active(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
    ) -> Tuple[List[IncidentEntity], int]:
        pass
