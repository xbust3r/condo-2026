"""
from typing import Optional
Amenity Use Case — business logic for amenities.
"""
import uuid as uuid_lib
from datetime import datetime
from typing import Optional

from library.dddpy.core_amenities.domain.amenity_entity import AmenityEntity
from library.dddpy.core_amenities.domain.amenity_exception import (
    AmenityNotFound,
    AmenityValidationError,
)
from library.dddpy.core_amenities.domain.amenity_cmd_repository import (
    AmenityCmdRepository,
)
from library.dddpy.core_amenities.domain.amenity_query_repository import (
    AmenityQueryRepository,
)
from library.dddpy.core_amenities.infrastructure.amenity_cmd_repository import (
    AmenityCmdRepositoryImpl,
)
from library.dddpy.core_amenities.infrastructure.amenity_query_repository import (
    AmenityQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


logger = Logger("AmenityUseCase")


class AmenityUseCase:

    VALID_STATUSES = {'active', 'inactive'}

    def __init__(self):
        self._cmd_repo = AmenityCmdRepositoryImpl()
        self._query_repo = AmenityQueryRepositoryImpl()

    def create(
        self,
        condominium_id: int,
        name: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        max_capacity: int = 1,
        booking_duration_min: int = 60,
        requires_approval: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        if not name or len(name.strip()) < 3:
            raise AmenityValidationError("Name must be at least 3 characters")

        entity = AmenityEntity(
            id=0,
            uuid=str(uuid_lib.uuid4()),
            condominium_id=condominium_id,
            name=name.strip(),
            description=description.strip() if description else None,
            location=location.strip() if location else None,
            max_capacity=max_capacity,
            booking_duration_min=booking_duration_min,
            requires_approval=requires_approval,
            status='active',
            created_at=datetime.utcnow(),
        )
        entity_id = self._cmd_repo.create(entity)
        entity.id = entity_id
        logger.info(f"Amenity created id={entity_id}")

        return ResponseSuccessSchema(
            success=True,
            message="Amenity created",
            data=entity.to_dict(),
        )

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_id")
        entity = self._query_repo.get_by_id(id)
        if not entity:
            raise AmenityNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Amenity found",
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_uuid")
        entity = self._query_repo.get_by_uuid(uuid)
        if not entity:
            raise AmenityNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Amenity found",
            data=entity.to_dict(),
        )

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if status and status not in self.VALID_STATUSES:
            raise AmenityValidationError(f"Invalid status. Must be one of: {self.VALID_STATUSES}")

        entities, total = self._query_repo.list_all(
            condominium_id=condominium_id,
            status=status,
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Amenities retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def list_active(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_active")
        entities, total = self._query_repo.list_active(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Active amenities retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def update(self, id: int, request) -> ResponseSuccessSchema:
        logger.add_inside_method("update")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise AmenityNotFound()

        entity = AmenityEntity(
            id=id,
            uuid=existing.uuid,
            condominium_id=existing.condominium_id,
            name=request.name if request.name is not None else existing.name,
            description=request.description if request.description is not None else existing.description,
            location=request.location if request.location is not None else existing.location,
            max_capacity=request.max_capacity if request.max_capacity is not None else existing.max_capacity,
            booking_duration_min=request.booking_duration_min if request.booking_duration_min is not None else existing.booking_duration_min,
            requires_approval=request.requires_approval if request.requires_approval is not None else existing.requires_approval,
            status=request.status if request.status is not None else existing.status,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._cmd_repo.update(entity)
        updated = self._query_repo.get_by_id(id)

        return ResponseSuccessSchema(
            success=True,
            message="Amenity updated",
            data=updated.to_dict(),
        )

    def soft_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("soft_delete")
        ok = self._cmd_repo.soft_delete(id)
        if not ok:
            raise AmenityNotFound()
        return ResponseSuccessSchema(success=True, message="Amenity deleted", data=None)

    def hard_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("hard_delete")
        ok = self._cmd_repo.hard_delete(id)
        if not ok:
            raise AmenityNotFound()
        return ResponseSuccessSchema(success=True, message="Amenity permanently deleted", data=None)
