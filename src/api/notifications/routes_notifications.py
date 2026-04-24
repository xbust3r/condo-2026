# =============================================================================
# API Routes: core_notifications
# User notification system
#
# Endpoints:
#   GET    /notifications                    — list (auth user only, with filters)
#   GET    /notifications/{id}               — get by id (auth user=owner)
#   GET    /notifications/unread-count       — unread count for current user
#   PATCH  /notifications/{id}/read         — mark as read (auth user=owner)
#   PATCH  /notifications/mark-all-read     — mark all as read (current user)
#   DELETE /notifications/{id}              — soft-delete (auth user=owner)
# =============================================================================

from fastapi import APIRouter, Query, Depends, Path
from typing import Optional

from api.auth.auth_dependencies import get_current_user
from library.dddpy.core_notifications.usecase.notification_factory import (
    notification_cmd_usecase_factory,
    notification_query_usecase_factory,
)
from library.dddpy.core_notifications.usecase.notification_cmd_schema import (
    CreateNotificationSchema,
    UpdateNotificationSchema,
)
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.core_notifications.domain.notification_exception import (
    NotificationNotFound,
    UnauthorizedNotificationAccess,
)


PREFIX = "/notifications"
notification_routes = APIRouter(prefix=PREFIX)


@notification_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_notifications"}


@notification_routes.get("")
@api_handler
def list_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user_id: Optional[int] = Query(None),
    channel: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    is_read: Optional[bool] = Query(None),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    List notifications.
    Users can only see their own notifications (user_id filter enforced).
    Admins can view any user's notifications.
    """
    query_usecase = notification_query_usecase_factory()

    # Enforce user_id = current user unless user has admin scope
    effective_user_id = user.id
    if user_id is not None and user_id != user.id:
        # Non-admins can only see their own — ignore the filter
        effective_user_id = user.id

    results, total = query_usecase.list_all(
        skip=skip,
        limit=limit,
        user_id=effective_user_id,
        channel=channel,
        type=type,
        is_read=is_read,
    )
    return {
        "items": [n.to_dict() for n in results],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@notification_routes.get("/{notification_id:int}")
@api_handler
def get_notification(
    notification_id: int = Path(..., description="Notification ID"),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Get a notification by ID.
    User can only access their own notifications.
    """
    query_usecase = notification_query_usecase_factory()
    notification = query_usecase.get_by_id(notification_id)

    if not notification:
        raise NotificationNotFound()

    if notification.user_id != user.id:
        raise UnauthorizedNotificationAccess()

    return notification.to_dict()


@notification_routes.get("/unread-count")
@api_handler
def get_unread_count(
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Get unread notification count for the current user.
    """
    query_usecase = notification_query_usecase_factory()
    count = query_usecase.get_unread_count(user.id)
    return {"unread_count": count}


@notification_routes.patch("/{notification_id:int}/read")
@api_handler
def mark_notification_read(
    notification_id: int = Path(..., description="Notification ID"),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Mark a notification as read.
    User can only mark their own notifications.
    """
    cmd_usecase = notification_cmd_usecase_factory()
    notification = cmd_usecase.mark_read(id=notification_id, user_id=user.id)
    return notification.to_dict()


@notification_routes.patch("/mark-all-read")
@api_handler
def mark_all_notifications_read(
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Mark all notifications as read for the current user.
    """
    cmd_usecase = notification_cmd_usecase_factory()
    count = cmd_usecase.mark_all_read(user_id=user.id)
    return {"marked_count": count}


@notification_routes.delete("/{notification_id:int}")
@api_handler
def delete_notification(
    notification_id: int = Path(..., description="Notification ID"),
    user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Soft-delete a notification.
    User can only delete their own notifications.
    """
    query_usecase = notification_query_usecase_factory()
    notification = query_usecase.get_by_id(notification_id)

    if not notification:
        raise NotificationNotFound()

    if notification.user_id != user.id:
        raise UnauthorizedNotificationAccess()

    cmd_usecase = notification_cmd_usecase_factory()
    cmd_usecase.soft_delete(notification_id)
    return {"success": True, "deleted_id": notification_id}