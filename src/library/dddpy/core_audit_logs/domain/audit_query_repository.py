"""
from typing import Optional
Audit log query repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from library.dddpy.core_audit_logs.domain.audit_log_entity import AuditLogEntity


class AuditLogQueryRepository(ABC):
    """Abstract read repository for audit logs."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[AuditLogEntity]:
        pass

    @abstractmethod
    def list_by_resource(
        self,
        resource_type: str,
        resource_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AuditLogEntity], int]:
        pass

    @abstractmethod
    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AuditLogEntity], int]:
        pass

    @abstractmethod
    def list_all(
        self,
        filters: dict,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[AuditLogEntity], int]:
        pass