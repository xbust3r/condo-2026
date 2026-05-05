"""
from typing import Optional
Announcement Use Case — business logic for announcements.
"""
import uuid as uuid_lib
from datetime import datetime
from typing import Optional

from library.dddpy.core_announcements.domain.announcement_entity import AnnouncementEntity
from library.dddpy.core_announcements.domain.announcement_exception import (
    AnnouncementNotFound,
    AnnouncementValidationError,
)
from library.dddpy.core_announcements.domain.announcement_cmd_repository import (
    AnnouncementCmdRepository,
)
from library.dddpy.core_announcements.domain.announcement_query_repository import (
    AnnouncementQueryRepository,
)
from library.dddpy.core_announcements.infrastructure.announcement_cmd_repository import (
    AnnouncementCmdRepositoryImpl,
)
from library.dddpy.core_announcements.infrastructure.announcement_query_repository import (
    AnnouncementQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


logger = Logger("AnnouncementUseCase")


class AnnouncementUseCase:

    VALID_CATEGORIES = {'info', 'warning', 'urgent', 'event', 'balance', 'assembly', 'maintenance', 'vote', 'rule', 'general'}
    VALID_VISIBILITY_SCOPES = {'public', 'owners_only', 'residents_only'}

    def __init__(self):
        self._cmd_repo = AnnouncementCmdRepositoryImpl()
        self._query_repo = AnnouncementQueryRepositoryImpl()

    def create(
        self,
        condominium_id: int,
        author_user_id: int,
        title: str,
        content: str,
        category: str = 'info',
        visibility: str = 'public',
        is_pinned: bool = False,
        tower_id: Optional[int] = None,
        published_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        if not title or len(title.strip()) < 3:
            raise AnnouncementValidationError("Title must be at least 3 characters")
        if not content or len(content.strip()) < 10:
            raise AnnouncementValidationError("Content must be at least 10 characters")
        if category not in self.VALID_CATEGORIES:
            raise AnnouncementValidationError(f"Invalid category. Must be one of: {self.VALID_CATEGORIES}")
        if visibility not in self.VALID_VISIBILITY_SCOPES:
            raise AnnouncementValidationError(f"Invalid visibility. Must be one of: {self.VALID_VISIBILITY_SCOPES}")

        entity = AnnouncementEntity(
            id=0,
            uuid=str(uuid_lib.uuid4()),
            condominium_id=condominium_id,
            author_user_id=author_user_id,
            title=title.strip(),
            content=content.strip(),
            category=category,
            visibility=visibility,
            is_pinned=is_pinned,
            tower_id=tower_id,
            published_at=published_at,
            expires_at=expires_at,
            created_at=datetime.utcnow(),
        )
        entity_id = self._cmd_repo.create(entity)
        entity.id = entity_id
        logger.info(f"Announcement created id={entity_id}")
        # Re-fetch with enrichment (author_name, condominium_name, tower_name)
        enriched = self._query_repo.get_by_id(entity_id)

        # ── Notification integration (Sprint 9 hotfix) ──────────────────────
        # Notify author with confirmation of publication
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
                    user_id=author_user_id,
                    channel="in_app",
                    type="announcement_published",
                    resource_type="announcement",
                    resource_id=entity_id,
                    title=f"Anuncio publicado: {title.strip()}",
                    body=content.strip()[:200] if len(content.strip()) > 200 else content.strip(),
                    metadata={
                        "condominium_id": condominium_id,
                        "author_user_id": author_user_id,
                    },
                )
            )
        except Exception:
            logger.warning("Failed to create notification for announcement_id={entity_id}")

        return ResponseSuccessSchema(
            success=True,
            message="Announcement created",
            data=enriched.to_dict() if enriched else entity.to_dict(),
        )

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_id")
        entity = self._query_repo.get_by_id(id)
        if not entity:
            raise AnnouncementNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Announcement found",
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_uuid")
        entity = self._query_repo.get_by_uuid(uuid)
        if not entity:
            raise AnnouncementNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Announcement found",
            data=entity.to_dict(),
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
        tower_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if category and category not in self.VALID_CATEGORIES:
            raise AnnouncementValidationError(f"Invalid category: {category}")
        if visibility and visibility not in self.VALID_VISIBILITY_SCOPES:
            raise AnnouncementValidationError(f"Invalid visibility: {visibility}")

        entities, total = self._query_repo.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            category=category,
            visibility=visibility,
            tower_id=tower_id,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Announcements retrieved",
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
        tower_id: Optional[int] = None,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_active")
        entities, total = self._query_repo.list_active(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            tower_id=tower_id,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Active announcements retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def soft_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("soft_delete")
        ok = self._cmd_repo.soft_delete(id)
        if not ok:
            raise AnnouncementNotFound()
        return ResponseSuccessSchema(success=True, message="Announcement deleted", data=None)

    def hard_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("hard_delete")
        ok = self._cmd_repo.hard_delete(id)
        if not ok:
            raise AnnouncementNotFound()
        return ResponseSuccessSchema(success=True, message="Announcement permanently deleted", data=None)

    def restore(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("restore")
        ok = self._cmd_repo.restore(id)
        if not ok:
            raise AnnouncementNotFound()
        return ResponseSuccessSchema(success=True, message="Announcement restored", data=None)

    def update(self, id: int, request) -> ResponseSuccessSchema:
        logger.add_inside_method("update")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise AnnouncementNotFound()

        entity = AnnouncementEntity(
            id=id,
            uuid=existing.uuid,
            condominium_id=existing.condominium_id,
            author_user_id=existing.author_user_id,
            title=request.title if request.title is not None else existing.title,
            content=request.content if request.content is not None else existing.content,
            category=request.category if request.category is not None else existing.category,
            visibility=request.visibility if request.visibility is not None else existing.visibility,
            is_pinned=request.is_pinned if request.is_pinned is not None else existing.is_pinned,
            tower_id=request.tower_id if request.tower_id is not None else existing.tower_id,
            published_at=request.published_at if request.published_at is not None else existing.published_at,
            expires_at=request.expires_at if request.expires_at is not None else existing.expires_at,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._cmd_repo.update(entity)
        # Re-fetch with enrichment
        updated = self._query_repo.get_by_id(id)

        # ── Notification integration (Sprint 9 hotfix) ──────────────────────
        # Notify author that their announcement was updated
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
                    user_id=existing.author_user_id,
                    channel="in_app",
                    type="announcement_updated",
                    resource_type="announcement",
                    resource_id=id,
                    title=f"Tu anuncio fue actualizado: {updated.title}",
                    body=updated.content[:200] if len(updated.content) > 200 else updated.content,
                    metadata={"condominium_id": updated.condominium_id},
                )
            )
        except Exception:
            logger.warning(f"Failed to create notification for announcement_id={id}")

        return ResponseSuccessSchema(
            success=True,
            message="Announcement updated",
            data=updated.to_dict(),
        )
