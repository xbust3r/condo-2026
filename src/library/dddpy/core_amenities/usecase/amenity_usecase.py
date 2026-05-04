"""
Amenity Use Case — business logic for amenities.

Now scope-aware:
- CONDOMINIUM amenities are visible to all buildings
- BUILDING amenities are exclusive to a specific building
- Cross-condominium building_id is rejected
"""
import uuid as uuid_lib
from datetime import datetime, timezone
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
    VALID_SCOPES = {'CONDOMINIUM', 'BUILDING'}

    def __init__(self):
        self._cmd_repo = AmenityCmdRepositoryImpl()
        self._query_repo = AmenityQueryRepositoryImpl()

    # ------------------------------------------------------------------
    # Cross-validation helpers
    # ------------------------------------------------------------------

    def _validate_scope_consistency(
        self,
        scope: str,
        building_id: Optional[int],
    ) -> None:
        if scope not in self.VALID_SCOPES:
            raise AmenityValidationError(
                f"Invalid scope '{scope}'. Must be one of: {self.VALID_SCOPES}"
            )
        if scope == 'CONDOMINIUM' and building_id is not None:
            raise AmenityValidationError(
                "scope=CONDOMINIUM requires building_id=None"
            )
        if scope == 'BUILDING' and building_id is None:
            raise AmenityValidationError(
                "scope=BUILDING requires building_id"
            )

    def _validate_building_belongs_to_condominium(
        self,
        condominium_id: int,
        building_id: int,
    ) -> None:
        """Ensure building belongs to the same condominium."""
        from library.dddpy.shared.mysql.session_manager import session_scope
        with session_scope() as session:
            from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
            building = session.query(DBBuildings).filter(
                DBBuildings.id == building_id,
                DBBuildings.deleted_at.is_(None),
            ).first()
            if not building:
                raise AmenityValidationError(
                    f"Building id={building_id} not found"
                )
            if building.condominium_id != condominium_id:
                raise AmenityValidationError(
                    f"Building id={building_id} does not belong to "
                    f"condominium id={condominium_id}"
                )

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create(
        self,
        condominium_id: int,
        name: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        max_capacity: int = 1,
        booking_duration_min: int = 60,
        requires_approval: bool = False,
        scope: str = 'CONDOMINIUM',
        building_id: Optional[int] = None,
        booking_price: float = 0.0,
        security_deposit_amount: float = 0.0,
        is_reservable: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        if not name or len(name.strip()) < 3:
            raise AmenityValidationError("Name must be at least 3 characters")

        self._validate_scope_consistency(scope, building_id)
        if scope == 'BUILDING' and building_id is not None:
            self._validate_building_belongs_to_condominium(condominium_id, building_id)

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
            scope=scope,
            building_id=building_id,
            booking_price=booking_price,
            security_deposit_amount=security_deposit_amount,
            is_reservable=is_reservable,
            status='active',
            created_at=datetime.now(timezone.utc),
        )
        entity_id = self._cmd_repo.create(entity)
        entity.id = entity_id
        logger.info(f"Amenity created id={entity_id} scope={scope} building_id={building_id}")

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
        building_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        """List amenities with optional scope-aware filters.

        Semantics:
        - condominium_id only → amenities with scope=CONDOMINIUM
        - condominium_id + building_id → CONDOMINIUM amenities + BUILDING amenities for that building
        - building_id only → BUILDING amenities for that building + CONDOMINIUM amenities of its condominium
        """
        logger.add_inside_method("list_all")
        if status and status not in self.VALID_STATUSES:
            raise AmenityValidationError(f"Invalid status. Must be one of: {self.VALID_STATUSES}")

        entities, total = self._query_repo.list_all(
            condominium_id=condominium_id,
            building_id=building_id,
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
        building_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        """List active amenities for a condominium (and optionally a building).

        If building_id is provided:
            returns CONDOMINIUM amenities + that building's exclusive amenities.
        Otherwise:
            returns CONDOMINIUM amenities only.
        """
        logger.add_inside_method("list_active")
        entities, total = self._query_repo.list_active(
            condominium_id=condominium_id,
            building_id=building_id,
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

        new_scope = request.scope if request.scope is not None else existing.scope
        new_building_id = request.building_id if request.building_id is not None else existing.building_id

        # Validate scope consistency for the new state
        self._validate_scope_consistency(new_scope, new_building_id)

        # If building changed, validate it belongs to the correct condominium
        if new_scope == 'BUILDING' and new_building_id is not None:
            self._validate_building_belongs_to_condominium(
                existing.condominium_id, new_building_id
            )

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
            scope=new_scope,
            building_id=new_building_id,
            booking_price=request.booking_price if request.booking_price is not None else existing.booking_price,
            security_deposit_amount=request.security_deposit_amount if request.security_deposit_amount is not None else existing.security_deposit_amount,
            is_reservable=request.is_reservable if request.is_reservable is not None else existing.is_reservable,
            status=request.status if request.status is not None else existing.status,
            created_at=existing.created_at,
            updated_at=datetime.now(timezone.utc),
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
