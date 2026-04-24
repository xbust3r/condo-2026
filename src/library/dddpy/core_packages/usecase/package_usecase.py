"""Package Use Case — business logic for package delivery management."""
from typing import Optional
import random
import uuid as uuid_lib
from datetime import datetime
from typing import Optional

from library.dddpy.core_packages.domain.package_entity import PackageEntity, PackageStatus
from library.dddpy.core_packages.domain.package_exception import (
    PackageNotFound,
    PackageValidationError,
)
from library.dddpy.core_packages.domain.package_cmd_repository import PackageCmdRepository
from library.dddpy.core_packages.domain.package_query_repository import PackageQueryRepository
from library.dddpy.core_packages.infrastructure.package_cmd_repository import (
    PackageCmdRepositoryImpl,
)
from library.dddpy.core_packages.infrastructure.package_query_repository import (
    PackageQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


logger = Logger("PackageUseCase")


class PackageUseCase:

    VALID_STATUSES = PackageStatus.ALL

    def __init__(self):
        self._cmd_repo = PackageCmdRepositoryImpl()
        self._query_repo = PackageQueryRepositoryImpl()

    def _generate_pickup_code(self) -> str:
        return str(random.randint(1000, 9999))

    def create(
        self,
        condominium_id: int,
        unit_id: int,
        recipient_user_id: int,
        carrier: Optional[str] = None,
        tracking_number: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        if not condominium_id or condominium_id <= 0:
            raise PackageValidationError("condominium_id is required")
        if not unit_id or unit_id <= 0:
            raise PackageValidationError("unit_id is required")
        if not recipient_user_id or recipient_user_id <= 0:
            raise PackageValidationError("recipient_user_id is required")

        now = datetime.utcnow()
        pickup_code = self._generate_pickup_code()

        entity = PackageEntity(
            id=0,
            uuid=str(uuid_lib.uuid4()),
            condominium_id=condominium_id,
            unit_id=unit_id,
            recipient_user_id=recipient_user_id,
            carrier=carrier,
            tracking_number=tracking_number,
            description=description,
            status=PackageStatus.PENDING,
            received_at=now,
            delivered_at=None,
            pickup_code=pickup_code,
            created_at=now,
        )
        entity_id = self._cmd_repo.create(entity)
        entity.id = entity_id
        logger.info(f"Package created id={entity_id}, pickup_code={pickup_code}")
        return ResponseSuccessSchema(
            success=True,
            message="Package registered",
            data=entity.to_dict(),
        )

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_id")
        entity = self._query_repo.get_by_id(id)
        if not entity:
            raise PackageNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Package found",
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_uuid")
        entity = self._query_repo.get_by_uuid(uuid)
        if not entity:
            raise PackageNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Package found",
            data=entity.to_dict(),
        )

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        recipient_user_id: Optional[int] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if status and status not in self.VALID_STATUSES:
            raise PackageValidationError(f"Invalid status: {status}")

        entities, total = self._query_repo.list_all(
            condominium_id=condominium_id,
            unit_id=unit_id,
            recipient_user_id=recipient_user_id,
            status=status,
            include_deleted=include_deleted,
            skip=skip,
            limit=limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Packages retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def list_pending(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_pending")
        entities, total = self._query_repo.list_pending(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Pending packages retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def list_by_unit(
        self,
        unit_id: int,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_by_unit")
        if status and status not in self.VALID_STATUSES:
            raise PackageValidationError(f"Invalid status: {status}")

        entities, total = self._query_repo.list_by_unit(
            unit_id=unit_id,
            status=status,
            skip=skip,
            limit=limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Packages retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def update(
        self,
        id: int,
        status: Optional[str] = None,
        carrier: Optional[str] = None,
        tracking_number: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("update")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise PackageNotFound()

        if status is not None and status not in self.VALID_STATUSES:
            raise PackageValidationError(f"Invalid status: {status}")

        entity = PackageEntity(
            id=id,
            uuid=existing.uuid,
            condominium_id=existing.condominium_id,
            unit_id=existing.unit_id,
            recipient_user_id=existing.recipient_user_id,
            carrier=carrier if carrier is not None else existing.carrier,
            tracking_number=tracking_number if tracking_number is not None else existing.tracking_number,
            description=description if description is not None else existing.description,
            status=status if status is not None else existing.status,
            received_at=existing.received_at,
            delivered_at=existing.delivered_at,
            pickup_code=existing.pickup_code,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._cmd_repo.update(entity)
        updated = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Package updated",
            data=updated.to_dict(),
        )

    def mark_delivered(self, id: int, pickup_code: str) -> ResponseSuccessSchema:
        logger.add_inside_method("mark_delivered")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise PackageNotFound()

        if existing.pickup_code != pickup_code:
            raise PackageValidationError("Invalid pickup code")

        if existing.status == PackageStatus.DELIVERED:
            raise PackageValidationError("Package already delivered")

        entity = PackageEntity(
            id=id,
            uuid=existing.uuid,
            condominium_id=existing.condominium_id,
            unit_id=existing.unit_id,
            recipient_user_id=existing.recipient_user_id,
            carrier=existing.carrier,
            tracking_number=existing.tracking_number,
            description=existing.description,
            status=PackageStatus.DELIVERED,
            received_at=existing.received_at,
            delivered_at=datetime.utcnow(),
            pickup_code=None,  # clear after delivery
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._cmd_repo.update(entity)
        updated = self._query_repo.get_by_id(id)
        logger.info(f"Package delivered id={id}")
        return ResponseSuccessSchema(
            success=True,
            message="Package delivered",
            data=updated.to_dict(),
        )

    def cancel(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("cancel")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise PackageNotFound()

        if existing.status == PackageStatus.DELIVERED:
            raise PackageValidationError("Cannot cancel a delivered package")
        if existing.status == PackageStatus.CANCELLED:
            raise PackageValidationError("Package already cancelled")

        entity = PackageEntity(
            id=id,
            uuid=existing.uuid,
            condominium_id=existing.condominium_id,
            unit_id=existing.unit_id,
            recipient_user_id=existing.recipient_user_id,
            carrier=existing.carrier,
            tracking_number=existing.tracking_number,
            description=existing.description,
            status=PackageStatus.CANCELLED,
            received_at=existing.received_at,
            delivered_at=existing.delivered_at,
            pickup_code=existing.pickup_code,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._cmd_repo.update(entity)
        updated = self._query_repo.get_by_id(id)
        logger.info(f"Package cancelled id={id}")
        return ResponseSuccessSchema(
            success=True,
            message="Package cancelled",
            data=updated.to_dict(),
        )

    def soft_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("soft_delete")
        ok = self._cmd_repo.soft_delete(id)
        if not ok:
            raise PackageNotFound()
        return ResponseSuccessSchema(
            success=True, message="Package deleted", data=None
        )

    def hard_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("hard_delete")
        ok = self._cmd_repo.hard_delete(id)
        if not ok:
            raise PackageNotFound()
        return ResponseSuccessSchema(
            success=True, message="Package permanently deleted", data=None
        )
