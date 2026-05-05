"""
from typing import Optional
Announcement domain entity — DDD for condominium announcements/posts.
"""
from datetime import datetime, date
from typing import Dict, Any, Optional


class AnnouncementEntity:
    """Entidad de dominio para anuncios/comunicados."""

    VALID_CATEGORIES = {'info', 'warning', 'urgent', 'event', 'balance', 'assembly', 'maintenance', 'vote', 'rule', 'general'}
    VALID_VISIBILITY_SCOPES = {'public', 'owners_only', 'residents_only'}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        author_user_id: int,
        title: str,
        content: str,
        category: str = 'info',
        visibility: str = 'public',
        is_pinned: bool = False,
        published_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        tower_id: Optional[int] = None,
        # Enriched
        author_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
        tower_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.author_user_id = author_user_id
        self.title = title
        self.content = content
        self.category = category
        self.visibility = visibility
        self.is_pinned = is_pinned
        self.published_at = published_at
        self.expires_at = expires_at
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.tower_id = tower_id
        self.author_name = author_name
        self.condominium_name = condominium_name
        self.tower_name = tower_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'condominium_id': self.condominium_id,
            'author_user_id': self.author_user_id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'visibility': self.visibility,
            'is_pinned': self.is_pinned,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tower_id': self.tower_id,
            'author_name': self.author_name,
            'condominium_name': self.condominium_name,
            'tower_name': self.tower_name,
        }
