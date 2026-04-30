# =============================================================================
# API Routes: core_documents
#
# Endpoints:
#   POST   /documents                       — upload  [RBAC: document.write]
#   GET    /documents                       — list    [RBAC: document.read]
#   GET    /documents/{id}                 — get     [RBAC: document.read]
#   GET    /documents/uuid/{uuid}          — get     [RBAC: document.read]
#   PUT    /documents/{id}                 — update  [RBAC: document.write]
#   DELETE /documents/{id}                — delete  [RBAC: document.delete]
#   DELETE /documents/{id}/hard           — hard    [RBAC: document.delete]
# =============================================================================

from fastapi import APIRouter, Depends, Query

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.core_documents.usecase.document_usecase import DocumentUseCase
from library.dddpy.core_documents.usecase.document_cmd_schema import (
    CreateDocumentSchema,
    UpdateDocumentSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.decorators.rbac_handler import rbac_required


PREFIX = "/documents"
document_routes = APIRouter(prefix=PREFIX)


@document_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_documents"}


@document_routes.post("")
@api_handler
def create_document(
    request: CreateDocumentSchema,
    user: UserIdentity = Depends(rbac_required("document", "write")),
) -> dict:
    """
    Register a new document (metadata only; file storage handled externally).
    RBAC: document.write on condominium_id.
    """
    response = DocumentUseCase().create(
        condominium_id=request.condominium_id,
        uploader_user_id=request.uploader_user_id,
        title=request.title,
        file_url=request.file_url,
        description=request.description,
        category=request.category,
        file_size_bytes=request.file_size_bytes,
        mime_type=request.mime_type,
    )
    return response.dict()


@document_routes.get("")
@api_handler
def list_documents(
    condominium_id: int = Query(None, description="Filter by condominium"),
    category: str = Query(None, description="Filter by category"),
    include_deleted: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: UserIdentity = Depends(rbac_required("document", "read")),
) -> dict:
    """List documents with optional filters."""
    response = DocumentUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        category=category,
        include_deleted=include_deleted,
    )
    return response.dict()


@document_routes.get("/{id}")
@api_handler
def get_document(
    id: int,
    user: UserIdentity = Depends(rbac_required("document", "read")),
) -> dict:
    """Get a document by id."""
    response = DocumentUseCase().get_by_id(id)
    return response.dict()


@document_routes.get("/uuid/{uuid}")
@api_handler
def get_document_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("document", "read")),
) -> dict:
    """Get a document by uuid."""
    response = DocumentUseCase().get_by_uuid(uuid)
    return response.dict()


@document_routes.put("/{id}")
@api_handler
def update_document(
    id: int,
    request: UpdateDocumentSchema,
    user: UserIdentity = Depends(rbac_required("document", "write")),
) -> dict:
    """Update document metadata (title, description, category)."""
    response = DocumentUseCase().update(id, request)
    return response.dict()


@document_routes.delete("/{id}")
@api_handler
def delete_document(
    id: int,
    user: UserIdentity = Depends(rbac_required("document", "delete")),
) -> dict:
    """Soft delete a document."""
    response = DocumentUseCase().soft_delete(id)
    return response.dict()


@document_routes.delete("/{id}/hard")
@api_handler
def hard_delete_document(
    id: int,
    user: UserIdentity = Depends(rbac_required("document", "delete")),
) -> dict:
    """Permanently delete a document."""
    response = DocumentUseCase().hard_delete(id)
    return response.dict()
