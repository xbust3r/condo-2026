"""
Incident command use case — write operations with INC-01 validation.
"""
from typing import Optional

from library.dddpy.core_incidents.domain.incident_entity import (
    IncidentEntity,
    IncidentStatus,
    IncidentPriority,
    IncidentCategory,
)
from library.dddpy.core_incidents.domain.incident_repository import IncidentRepository
from library.dddpy.core_incidents.usecase.incident_cmd_schema import (
    CreateIncidentSchema,
    UpdateIncidentSchema,
)
from library.dddpy.core_incidents.domain.incident_exception import (
    IncidentNotFound,
    UnauthorizedIncidentAccess,
    IncidentValidationError,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("IncidentCmdUseCase")


class IncidentCmdUseCase:

    def __init__(self, repository: IncidentRepository):
        self.repository = repository
        logger.info("IncidentCmdUseCase initialized")

    def _has_active_occupancy_or_ownership(self, user_id: int, unit_id: int) -> bool:
        """
        INC-01: Verify user has an active occupancy OR active ownership in the unit.
        Returns True if at least one is found.
        """
        # Check occupancy
        from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_query_repository import (
            UnitOccupancyQueryRepositoryImpl,
        )
        try:
            occ_repo = UnitOccupancyQueryRepositoryImpl()
            active_occs, _ = occ_repo.list_all(
                unit_id=unit_id,
                user_id=user_id,
                status="active",
                include_deleted=False,
            )
            if active_occs:
                return True
        except Exception:
            pass

        # Check ownership
        from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import (
            UnitOwnershipQueryRepositoryImpl,
        )
        try:
            own_repo = UnitOwnershipQueryRepositoryImpl()
            active_owns, _ = own_repo.list_all(
                unit_id=unit_id,
                user_id=user_id,
                status="active",
                include_deleted=False,
            )
            if active_owns:
                return True
        except Exception:
            pass

        return False

    def create(self, data: CreateIncidentSchema, reported_by_user_id: int) -> IncidentEntity:
        """
        Create a new incident.

        INC-01 validation: reporter must have active occupancy OR ownership in the unit.
        INC-03: If priority=urgent, set is_escalated=True automatically.
        """
        logger.info(
            f"Creating incident title='{data.title}', "
            f"unit_id={data.unit_id}, reported_by_user_id={reported_by_user_id}"
        )

        # INC-01 validation
        if not self._has_active_occupancy_or_ownership(reported_by_user_id, data.unit_id):
            logger.warning(
                f"INC-01 violation: user_id={reported_by_user_id} has no active "
                f"occupancy or ownership in unit_id={data.unit_id}"
            )
            raise UnauthorizedIncidentAccess()

        # Validate category
        if data.category not in IncidentCategory.ALL:
            raise IncidentValidationError(
                f"Invalid category '{data.category}'. Valid: {', '.join(sorted(IncidentCategory.ALL))}"
            )

        # Validate priority
        if data.priority not in IncidentPriority.ALL:
            raise IncidentValidationError(
                f"Invalid priority '{data.priority}'. Valid: {', '.join(sorted(IncidentPriority.ALL))}"
            )

        # INC-03: auto-escalate urgent
        is_escalated = data.priority == IncidentPriority.URGENT

        entity = IncidentEntity(
            id=0,
            uuid="",
            condominium_id=data.condominium_id,
            building_id=data.building_id,
            unit_id=data.unit_id,
            reported_by_user_id=reported_by_user_id,
            assigned_to_user_id=None,
            category=data.category,
            priority=data.priority,
            status=IncidentStatus.PENDING,
            title=data.title,
            description=data.description,
            photos=data.photos or [],
            internal_notes=None,
            resolution_notes=None,
            scheduled_date=None,
            completed_date=None,
            is_escalated=is_escalated,
        )

        try:
            entity._validate_invariants()
        except ValueError as e:
            raise IncidentValidationError(str(e))

        result_entity = self.repository.create(entity)
        result_entity.id = entity.id  # ensure id is set on returned entity
        logger.info(f"Incident created id={result_entity.id}")

        # ── Notification integration (Sprint 9 hotfix) ──────────────────────
        # Notify reporter that their incident was created
        try:
            from library.dddpy.core_notifications.usecase.notification_cmd_schema import (
                CreateNotificationSchema,
            )
            from library.dddpy.core_notifications.usecase.notification_factory import (
                notification_cmd_usecase_factory,
            )
            notif_cmd = notification_cmd_usecase_factory()
            notif_cmd.create(
                CreateNotificationSchema(
                    user_id=reported_by_user_id,
                    channel="in_app",
                    type="incident_created",
                    resource_type="incident",
                    resource_id=result_entity.id,
                    title=f"Incidencia creada: {data.title}",
                    body=f"Tu incidencia ha sido registrada con estado 'pending'. ID #{result_entity.id}",
                    metadata={
                        "condominium_id": data.condominium_id,
                        "unit_id": data.unit_id,
                        "priority": data.priority,
                    },
                )
            )
        except Exception:
            logger.warning(f"Failed to create notification for incident, user_id={reported_by_user_id}")

        return result_entity
    def update(self, id: int, data: UpdateIncidentSchema, requesting_user_id: int) -> IncidentEntity:
        """
        Update an existing incident.
        Note: caller is responsible for RBAC permission check.
        """
        logger.info(f"Updating incident id={id}, requesting_user_id={requesting_user_id}")

        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise IncidentNotFound()

        # Apply partial updates
        if data.category is not None:
            if data.category not in IncidentCategory.ALL:
                raise IncidentValidationError(f"Invalid category '{data.category}'")
            existing.category = data.category
        if data.priority is not None:
            if data.priority not in IncidentPriority.ALL:
                raise IncidentValidationError(f"Invalid priority '{data.priority}'")
            existing.priority = data.priority
            # INC-03: auto-escalate if priority becomes urgent
            if data.priority == IncidentPriority.URGENT and not existing.is_escalated:
                existing.is_escalated = True
        if data.status is not None:
            if data.status not in IncidentStatus.ALL:
                raise IncidentValidationError(f"Invalid status '{data.status}'")
            # INC-04: can only close with completed_date
            if data.status == IncidentStatus.CLOSED and existing.completed_date is None and data.completed_date is None:
                raise IncidentValidationError("Cannot close incident without completed_date")
            existing.status = data.status
        if data.title is not None:
            existing.title = data.title
        if data.description is not None:
            existing.description = data.description
        if data.photos is not None:
            existing.photos = data.photos
        if data.internal_notes is not None:
            existing.internal_notes = data.internal_notes
        if data.resolution_notes is not None:
            existing.resolution_notes = data.resolution_notes
        if data.assigned_to_user_id is not None:
            existing.assigned_to_user_id = data.assigned_to_user_id
        if data.scheduled_date is not None:
            existing.scheduled_date = data.scheduled_date
        if data.completed_date is not None:
            existing.completed_date = data.completed_date

        try:
            existing._validate_invariants()
        except ValueError as e:
            raise IncidentValidationError(str(e))

        result = self.repository.update(id, existing)
        if result is None:
            raise IncidentNotFound()
        return result

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting incident id={id}")
        return self.repository.delete(id)

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting incident id={id}")
        return self.repository.hard_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring incident id={id}")
        return self.repository.restore(id)

    def assign(self, id: int, assigned_to_user_id: int) -> IncidentEntity:
        """Assign incident to a staff/contractor user."""
        logger.info(f"Assigning incident id={id} to user_id={assigned_to_user_id}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise IncidentNotFound()

        previous_assignee = existing.assigned_to_user_id
        existing.assigned_to_user_id = assigned_to_user_id
        # Optionally set status to open if still pending
        if existing.status == IncidentStatus.PENDING:
            existing.status = IncidentStatus.OPEN

        result = self.repository.update(id, existing)
        if result is None:
            raise IncidentNotFound()


        # ── Notification integration (Sprint 9 hotfix) ──────────────────────
        try:
            from library.dddpy.core_notifications.usecase.notification_cmd_schema import (
                CreateNotificationSchema,
            )
            from library.dddpy.core_notifications.usecase.notification_factory import (
                notification_cmd_usecase_factory,
            )
            notif_cmd = notification_cmd_usecase_factory()
            notif_cmd.create(
                CreateNotificationSchema(
                    user_id=assigned_to_user_id,
                    channel="in_app",
                    type="incident_assigned",
                    resource_type="incident",
                    resource_id=id,
                    title=f"Incidencia asignada: {existing.title}",
                    body=f"Se te ha asignado la incidencia #{id} (prioridad: {existing.priority})",
                    metadata={"condominium_id": existing.condominium_id},
                )
            )
        except Exception:
            logger.warning(f"Failed to notify assignee user_id={assigned_to_user_id}")

        return result

    def escalate(self, id: int) -> IncidentEntity:
        """Mark incident as escalated."""
        logger.info(f"Escalating incident id={id}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise IncidentNotFound()

        existing.is_escalated = True
        result = self.repository.update(id, existing)
        if result is None:
            raise IncidentNotFound()
        return result

    def complete(self, id: int, resolution_notes: Optional[str] = None) -> IncidentEntity:
        """Mark incident as completed (status=resolved, set completed_date)."""
        logger.info(f"Completing incident id={id}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise IncidentNotFound()

        from datetime import date
        existing.status = IncidentStatus.RESOLVED
        existing.completed_date = date.today()
        if resolution_notes:
            existing.resolution_notes = resolution_notes

        try:
            existing._validate_invariants()
        except ValueError as e:
            raise IncidentValidationError(str(e))

        result = self.repository.update(id, existing)
        if result is None:
            raise IncidentNotFound()


        # ── Notification integration (Sprint 9 hotfix) ──────────────────────
        # Notify reporter that their incident was resolved
        try:
            from library.dddpy.core_notifications.usecase.notification_cmd_schema import (
                CreateNotificationSchema,
            )
            from library.dddpy.core_notifications.usecase.notification_factory import (
                notification_cmd_usecase_factory,
            )
            notif_cmd = notification_cmd_usecase_factory()
            notif_cmd.create(
                CreateNotificationSchema(
                    user_id=existing.reported_by_user_id,
                    channel="in_app",
                    type="incident_completed",
                    resource_type="incident",
                    resource_id=id,
                    title=f"Incidencia #{id} resuelta",
                    body=f"Tu incidencia '{existing.title}' ha sido marcada como resuelta.",
                    metadata={"condominium_id": existing.condominium_id},
                )
            )
        except Exception:
            logger.warning(f"Failed to notify reporter user_id={existing.reported_by_user_id}")

        return result

    def close(self, id: int) -> IncidentEntity:
        """Close an incident (admin action). Requires completed_date."""
        logger.info(f"Closing incident id={id}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise IncidentNotFound()


        # INC-04: must have completed_date
        if existing.completed_date is None:
            raise IncidentValidationError("Cannot close incident without completed_date (mark as complete first)")


        existing.status = IncidentStatus.CLOSED
        result = self.repository.update(id, existing)
        if result is None:
            raise IncidentNotFound()

        # ── Notification integration (Sprint 9 hotfix) ──────────────────────
        # Notify reporter that their incident was closed
        try:
            from library.dddpy.core_notifications.usecase.notification_cmd_schema import (
                CreateNotificationSchema,
            )
            from library.dddpy.core_notifications.usecase.notification_factory import (
                notification_cmd_usecase_factory,
            )
            notif_cmd = notification_cmd_usecase_factory()
            notif_cmd.create(
                CreateNotificationSchema(
                    user_id=existing.reported_by_user_id,
                    channel="in_app",
                    type="incident_closed",
                    resource_type="incident",
                    resource_id=id,
                    title=f"Incidencia #{id} cerrada",
                    body=f"Tu incidencia '{existing.title}' ha sido cerrada.",
                    metadata={
                        "condominium_id": existing.condominium_id,
                        "resolved_by": "admin",
                    },
                )
            )
        except Exception:
            logger.warning(f"Failed to notify close for incident id={id}")


        return result

    def cancel(self, id: int) -> IncidentEntity:
        """Cancel an incident (admin action)."""
        logger.info(f"Cancelling incident id={id}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise IncidentNotFound()

        existing.status = IncidentStatus.CANCELLED
        result = self.repository.update(id, existing)
        if result is None:
            raise IncidentNotFound()
        return result
