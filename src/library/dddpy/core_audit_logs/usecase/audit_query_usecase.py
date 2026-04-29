"""
from typing import Optional
Audit log query use case — read-only access to audit trail.
"""
from datetime import date
from typing import Optional

from library.dddpy.core_audit_logs.domain.audit_exception import AuditLogNotFound
from library.dddpy.core_audit_logs.domain.audit_query_repository import AuditLogQueryRepository
from library.dddpy.core_audit_logs.infrastructure.audit_query_repository import AuditQueryRepositoryImpl
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


logger = Logger("AuditQueryUseCase")


class AuditQueryUseCase:

    def __init__(self):
        self._repo: AuditLogQueryRepository = AuditQueryRepositoryImpl()

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_id")
        entity = self._repo.get_by_id(id)
        if not entity:
            raise AuditLogNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Audit log found",
            data=entity.to_dict(),
        )

    def list_by_resource(
        self,
        resource_type: str,
        resource_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_by_resource")
        entities, total = self._repo.list_by_resource(
            resource_type=resource_type,
            resource_id=resource_id,
            skip=skip,
            limit=limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Audit trail retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_by_user")
        entities, total = self._repo.list_by_user(user_id=user_id, skip=skip, limit=limit)
        return ResponseSuccessSchema(
            success=True,
            message="Audit trail retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def list_all(
        self,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        user_id: Optional[int] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        entities, total = self._repo.list_all(
            action=action,
            resource_type=resource_type,
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            skip=skip,
            limit=limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Audit trail retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )