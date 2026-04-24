"""Visitor query repository ABC — read operations."""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from library.dddpy.core_visitors.domain.visitor_entity import VisitorEntity


class VisitorQueryRepository(ABC):
    """Interfaz de lectura para consultas de visitors."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[VisitorEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[VisitorEntity]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        pass

    @abstractmethod
    def list_by_host(
        self,
        host_user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        pass

    @abstractmethod
    def list_by_date(
        self,
        condominium_id: int,
        expected_date: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        pass

    @abstractmethod
    def list_active(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
    ) -> Tuple[List[VisitorEntity], int]:
        pass

    @abstractmethod
    def get_by_access_code(
        self,
        access_code: str,
        condominium_id: Optional[int] = None,
    ) -> Optional[VisitorEntity]:
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[VisitorEntity]:
        """Re-fetch entity ignoring soft-delete filter."""
        pass