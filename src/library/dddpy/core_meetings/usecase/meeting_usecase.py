"""
from typing import Optional
Meeting Use Case — business logic for condominium meetings.
"""
import uuid as uuid_lib
from datetime import datetime
from typing import Optional

from library.dddpy.core_meetings.domain.meeting_entity import MeetingEntity
from library.dddpy.core_meetings.domain.meeting_exception import (
    MeetingNotFound,
    MeetingValidationError,
)
from library.dddpy.core_meetings.domain.meeting_cmd_repository import (
    MeetingCmdRepository,
)
from library.dddpy.core_meetings.domain.meeting_query_repository import (
    MeetingQueryRepository,
)
from library.dddpy.core_meetings.infrastructure.meeting_cmd_repository import (
    MeetingCmdRepositoryImpl,
)
from library.dddpy.core_meetings.infrastructure.meeting_query_repository import (
    MeetingQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


logger = Logger("MeetingUseCase")


class MeetingUseCase:

    VALID_MEETING_TYPES = {'assembly', 'board', 'committee'}
    VALID_STATUSES = {'scheduled', 'confirmed', 'held', 'cancelled'}

    def __init__(self):
        self._cmd_repo = MeetingCmdRepositoryImpl()
        self._query_repo = MeetingQueryRepositoryImpl()

    def create(self, request) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        if not request.title or len(request.title.strip()) < 3:
            raise MeetingValidationError("Title must be at least 3 characters")
        if request.meeting_type not in self.VALID_MEETING_TYPES:
            raise MeetingValidationError(
                f"Invalid meeting_type. Must be one of: {self.VALID_MEETING_TYPES}"
            )

        entity = MeetingEntity(
            id=0,
            uuid=str(uuid_lib.uuid4()),
            condominium_id=request.condominium_id,
            meeting_type=request.meeting_type,
            title=request.title.strip(),
            description=request.description.strip() if request.description else None,
            meeting_date=request.meeting_date,
            location=request.location.strip() if request.location else None,
            status='scheduled',
            created_by_user_id=request.created_by_user_id,
            created_at=datetime.utcnow(),
        )
        entity_id = self._cmd_repo.create(entity)
        entity.id = entity_id
        logger.info(f"Meeting created id={entity_id}")

        # Re-fetch with enrichment
        created = self._query_repo.get_by_id(entity_id)

        return ResponseSuccessSchema(
            success=True,
            message="Meeting created",
            data=created.to_dict(),
        )

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_id")
        entity = self._query_repo.get_by_id(id)
        if not entity:
            raise MeetingNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Meeting found",
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_uuid")
        entity = self._query_repo.get_by_uuid(uuid)
        if not entity:
            raise MeetingNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Meeting found",
            data=entity.to_dict(),
        )

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        meeting_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if status and status not in self.VALID_STATUSES:
            raise MeetingValidationError(f"Invalid status: {status}")
        if meeting_type and meeting_type not in self.VALID_MEETING_TYPES:
            raise MeetingValidationError(f"Invalid meeting_type: {meeting_type}")

        entities, total = self._query_repo.list_all(
            condominium_id=condominium_id,
            status=status,
            meeting_type=meeting_type,
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Meetings retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def list_upcoming(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_upcoming")
        entities, total = self._query_repo.list_upcoming(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Upcoming meetings retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def update(self, id: int, request) -> ResponseSuccessSchema:
        logger.add_inside_method("update")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise MeetingNotFound()

        if request.status and request.status not in self.VALID_STATUSES:
            raise MeetingValidationError(f"Invalid status: {request.status}")

        entity = MeetingEntity(
            id=id,
            uuid=existing.uuid,
            condominium_id=existing.condominium_id,
            meeting_type=existing.meeting_type,
            title=request.title if request.title is not None else existing.title,
            description=request.description if request.description is not None else existing.description,
            meeting_date=request.meeting_date if request.meeting_date is not None else existing.meeting_date,
            location=request.location if request.location is not None else existing.location,
            status=request.status if request.status is not None else existing.status,
            approved_at=existing.approved_at,
            created_by_user_id=existing.created_by_user_id,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._cmd_repo.update(entity)

        # Re-fetch with enrichment
        updated = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Meeting updated",
            data=updated.to_dict(),
        )

    def approve(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("approve")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise MeetingNotFound()

        ok = self._cmd_repo.approve(id)
        if not ok:
            raise MeetingNotFound()

        approved = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Meeting approved",
            data=approved.to_dict(),
        )

    def cancel(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("cancel")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise MeetingNotFound()

        ok = self._cmd_repo.cancel(id)
        if not ok:
            raise MeetingNotFound()

        cancelled = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Meeting cancelled",
            data=cancelled.to_dict(),
        )

    def soft_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("soft_delete")
        ok = self._cmd_repo.soft_delete(id)
        if not ok:
            raise MeetingNotFound()
        return ResponseSuccessSchema(success=True, message="Meeting deleted", data=None)

    def hard_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("hard_delete")
        ok = self._cmd_repo.hard_delete(id)
        if not ok:
            raise MeetingNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Meeting permanently deleted",
            data=None,
        )
