"""
Document Command Repository Implementation.
"""
from datetime import datetime
from typing import Optional

from library.dddpy.core_documents.domain.document_cmd_repository import DocumentCmdRepository
from library.dddpy.core_documents.domain.document_entity import DocumentEntity
from library.dddpy.core_documents.infrastructure.dbdocument import DBDocument
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("DocumentCmdRepository")


class DocumentCmdRepositoryImpl(DocumentCmdRepository):

    def create(self, entity: DocumentEntity) -> int:
        logger.info(f"Creating document condominium_id={entity.condominium_id}")
        with session_scope() as session:
            db_d = DBDocument(
                uuid=entity.uuid,
                condominium_id=entity.condominium_id,
                uploader_user_id=entity.uploader_user_id,
                title=entity.title,
                description=entity.description,
                file_url=entity.file_url,
                file_size_bytes=entity.file_size_bytes,
                mime_type=entity.mime_type,
                category=entity.category,
            )
            session.add(db_d)
            session.flush()
            session.refresh(db_d)
            logger.info(f"Document created id={db_d.id}")
            return db_d.id

    def update(self, entity: DocumentEntity) -> bool:
        logger.info(f"Updating document id={entity.id}")
        with session_scope() as session:
            db_d = session.query(DBDocument).filter(
                DBDocument.id == entity.id,
                DBDocument.deleted_at.is_(None),
            ).first()
            if not db_d:
                return False
            db_d.title = entity.title
            db_d.description = entity.description
            db_d.category = entity.category
            db_d.updated_at = datetime.utcnow()
            session.flush()
            logger.info(f"Document updated id={entity.id}")
            return True

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft-deleting document id={id}")
        with session_scope() as session:
            db_d = session.query(DBDocument).filter(
                DBDocument.id == id,
                DBDocument.deleted_at.is_(None),
            ).first()
            if not db_d:
                return False
            db_d.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Document soft-deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard-deleting document id={id}")
        with session_scope() as session:
            db_d = session.query(DBDocument).filter(
                DBDocument.id == id,
            ).first()
            if not db_d:
                return False
            session.delete(db_d)
            session.flush()
            logger.info(f"Document hard-deleted id={id}")
            return True
