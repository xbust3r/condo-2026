"""
Document Use Case.
"""
import uuid as uuid_lib
from datetime import datetime
from typing import Optional

from library.dddpy.core_documents.domain.document_entity import DocumentEntity
from library.dddpy.core_documents.domain.document_exception import (
    DocumentNotFound,
    DocumentValidationError,
)
from library.dddpy.core_documents.domain.document_cmd_repository import DocumentCmdRepository
from library.dddpy.core_documents.domain.document_query_repository import DocumentQueryRepository
from library.dddpy.core_documents.infrastructure.document_cmd_repository import (
    DocumentCmdRepositoryImpl,
)
from library.dddpy.core_documents.infrastructure.document_query_repository import (
    DocumentQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


logger = Logger("DocumentUseCase")


class DocumentUseCase:

    VALID_CATEGORIES = {'bylaws', 'minutes', 'regulation', 'contract', 'invoice', 'other'}

    def __init__(self):
        self._cmd_repo = DocumentCmdRepositoryImpl()
        self._query_repo = DocumentQueryRepositoryImpl()

    def create(
        self,
        condominium_id: int,
        uploader_user_id: int,
        title: str,
        file_url: str,
        description: Optional[str] = None,
        category: str = 'other',
        file_size_bytes: Optional[int] = None,
        mime_type: Optional[str] = None,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        if not title or len(title.strip()) < 3:
            raise DocumentValidationError("Title must be at least 3 characters")
        if not file_url or len(file_url.strip()) < 5:
            raise DocumentValidationError("File URL is required")
        if category not in self.VALID_CATEGORIES:
            raise DocumentValidationError(
                f"Invalid category. Must be one of: {self.VALID_CATEGORIES}"
            )

        entity = DocumentEntity(
            id=0,
            uuid=str(uuid_lib.uuid4()),
            condominium_id=condominium_id,
            uploader_user_id=uploader_user_id,
            title=title.strip(),
            description=description,
            file_url=file_url.strip(),
            file_size_bytes=file_size_bytes,
            mime_type=mime_type,
            category=category,
            created_at=datetime.utcnow(),
        )
        entity_id = self._cmd_repo.create(entity)
        entity.id = entity_id
        logger.info(f"Document created id={entity_id}")
        return ResponseSuccessSchema(
            success=True,
            message="Document created",
            data=entity.to_dict(),
        )

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_id")
        entity = self._query_repo.get_by_id(id)
        if not entity:
            raise DocumentNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Document found",
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_uuid")
        entity = self._query_repo.get_by_uuid(uuid)
        if not entity:
            raise DocumentNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Document found",
            data=entity.to_dict(),
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        category: Optional[str] = None,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if category and category not in self.VALID_CATEGORIES:
            raise DocumentValidationError(f"Invalid category: {category}")

        entities, total = self._query_repo.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            category=category,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Documents retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def update(self, id: int, request) -> ResponseSuccessSchema:
        logger.add_inside_method("update")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise DocumentNotFound()

        entity = DocumentEntity(
            id=id,
            uuid=existing.uuid,
            condominium_id=existing.condominium_id,
            uploader_user_id=existing.uploader_user_id,
            title=request.title if request.title is not None else existing.title,
            description=request.description if request.description is not None else existing.description,
            category=request.category if request.category is not None else existing.category,
            file_url=existing.file_url,
            file_size_bytes=existing.file_size_bytes,
            mime_type=existing.mime_type,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._cmd_repo.update(entity)
        updated = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Document updated",
            data=updated.to_dict(),
        )

    def soft_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("soft_delete")
        ok = self._cmd_repo.soft_delete(id)
        if not ok:
            raise DocumentNotFound()
        return ResponseSuccessSchema(
            success=True, message="Document deleted", data=None
        )

    def hard_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("hard_delete")
        ok = self._cmd_repo.hard_delete(id)
        if not ok:
            raise DocumentNotFound()
        return ResponseSuccessSchema(
            success=True, message="Document permanently deleted", data=None
        )
