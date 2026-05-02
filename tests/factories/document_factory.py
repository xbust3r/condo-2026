"""
Factory: Document.

Creates test document records directly in the DB via SQLAlchemy.
"""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_documents.infrastructure.dbdocument import DBDocument


class DocumentFactory:
    """Factory for creating test Document records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        uploader_user_id: int,
        title: str = None,
        file_url: str = None,
        category: str = "other",
        description: str = None,
        file_size_bytes: int = None,
        mime_type: str = None,
        **kwargs,
    ) -> DBDocument:
        db_doc = DBDocument(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            uploader_user_id=uploader_user_id,
            title=title or "Factory Document",
            description=description,
            file_url=file_url or f"https://test.local/docs/{uuid.uuid4().hex}.pdf",
            file_size_bytes=file_size_bytes or 1024,
            mime_type=mime_type or "application/pdf",
            category=category,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_doc)
        session.flush()
        session.refresh(db_doc)
        return db_doc
