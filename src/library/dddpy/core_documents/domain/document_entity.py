"""
from typing import Optional
Document domain entity.
"""
from datetime import datetime
from typing import Dict, Any, Optional


class DocumentEntity:
    """Entidad de dominio para documentos."""

    VALID_CATEGORIES = {'bylaws', 'minutes', 'regulation', 'contract', 'invoice', 'other'}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        uploader_user_id: int,
        title: str,
        description: Optional[str] = None,
        file_url: str = '',
        file_size_bytes: Optional[int] = None,
        mime_type: Optional[str] = None,
        category: str = 'other',
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched
        uploader_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.uploader_user_id = uploader_user_id
        self.title = title
        self.description = description
        self.file_url = file_url
        self.file_size_bytes = file_size_bytes
        self.mime_type = mime_type
        self.category = category
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.uploader_name = uploader_name
        self.condominium_name = condominium_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'condominium_id': self.condominium_id,
            'uploader_user_id': self.uploader_user_id,
            'title': self.title,
            'description': self.description,
            'file_url': self.file_url,
            'file_size_bytes': self.file_size_bytes,
            'mime_type': self.mime_type,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'uploader_name': self.uploader_name,
            'condominium_name': self.condominium_name,
        }
