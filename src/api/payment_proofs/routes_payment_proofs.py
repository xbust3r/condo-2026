# =============================================================================
# API Routes: payment_proofs
# Módulo de comprobantes de pago
#
# Endpoints:
#   POST   /payment-proofs              — upload proof  [RBAC: payment_proof.write]
#   GET    /payment-proofs              — list          [RBAC: payment_proof.read]
#   GET    /payment-proofs/{id}         — get           [RBAC: payment_proof.read]
#   GET    /payment-proofs/uuid/{uuid}  — get           [RBAC: payment_proof.read]
#   POST   /payment-proofs/{id}/approve — approve       [RBAC: payment_proof.review]
#   POST   /payment-proofs/{id}/reject  — reject        [RBAC: payment_proof.review]
# =============================================================================

import os
import uuid as uuid_lib
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.core_payment_proofs.usecase.payment_proof_usecase import (
    PaymentProofUseCase,
)
from library.dddpy.core_payment_proofs.usecase.payment_proof_cmd_schema import (
    ApproveProofSchema,
    RejectProofSchema,
)
from library.dddpy.core_payment_proofs.domain.payment_proof_data import (
    ApproveProofData,
)
from library.dddpy.core_payment_proofs.domain.payment_proof_entity import (
    PaymentProofEntity,
)
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.decorators.rbac_handler import rbac_required
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PaymentProofRoutes")

PREFIX = "/payment-proofs"

payment_proof_routes = APIRouter(prefix=PREFIX)

# Configurable upload directory (env or default)
UPLOAD_DIR = os.environ.get(
    "PAYMENT_PROOF_UPLOAD_DIR",
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads", "payment_proofs"),
)


def _is_admin(user: UserIdentity, condominium_id: int) -> bool:
    """
    Determine if the user has admin/contador role in the given condominium.
    Uses permission check via has_permission for payment_proof.review.
    """
    from library.dddpy.shared.decorators.rbac_handler import _user_has_permission

    return _user_has_permission(
        user_id=user.id,
        permission_code="payment_proof.review",
        scope_type="condominium",
        scope_value=condominium_id,
    )


def _save_upload(upload: UploadFile) -> dict:
    """Save an uploaded file to disk and return metadata."""
    ext = os.path.splitext(upload.filename or "file")[1].lower()
    safe_name = f"{uuid_lib.uuid4().hex}{ext}"

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, safe_name)
    content = upload.file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Determine MIME from extension if content_type is generic
    mime = upload.content_type or "application/octet-stream"
    ext_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".pdf": "application/pdf",
    }
    if mime == "application/octet-stream" and ext in ext_map:
        mime = ext_map[ext]

    file_size = os.path.getsize(file_path) if file_path and os.path.exists(file_path) else 0

    return {
        "file_url": file_path,
        "original_filename": upload.filename or "file",
        "file_size_bytes": file_size,
        "mime_type": mime,
    }


@payment_proof_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "payment_proofs"}


@payment_proof_routes.post("")
@api_handler
def upload_proof(
    ar_id: int = Form(..., description="Accounts receivable ID"),
    condominium_id: int = Form(..., description="Condominium ID"),
    unit_id: int = Form(..., description="Unit ID"),
    file: UploadFile = File(..., description="Comprobante (imagen o PDF)"),
    user: UserIdentity = Depends(rbac_required("payment_proof", "write")),
) -> dict:
    """
    Upload a payment proof (image or PDF).

    Validates:
      - MIME type: only image/jpeg, image/png, image/webp, application/pdf
      - File size: max 10 MB

    The proof enters pending_review status.
    """
    logger.add_inside_method("upload_proof") if hasattr(logger, "add_inside_method") else None

    # Quick client-side validation before reading the file
    content_type = file.content_type or ""
    if content_type and content_type not in PaymentProofEntity.ALLOWED_MIME_TYPES:
        # Try extension-based fallback
        ext = os.path.splitext(file.filename or "")[1].lower()
        ext_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".pdf": "application/pdf",
        }
        if ext not in ext_map:
            from library.dddpy.core_payment_proofs.domain.payment_proof_exception import (
                PaymentProofInvalidFileType,
            )
            raise PaymentProofInvalidFileType(content_type)

    # Save file
    file_meta = _save_upload(file)

    response = PaymentProofUseCase().upload(
        condominium_id=condominium_id,
        unit_id=unit_id,
        ar_id=ar_id,
        submitted_by=user.id,
        file_url=file_meta["file_url"],
        original_filename=file_meta["original_filename"],
        file_size_bytes=file_meta["file_size_bytes"],
        mime_type=file_meta["mime_type"],
    )
    return response.dict()


@payment_proof_routes.get("")
@api_handler
def list_proofs(
    condominium_id: Optional[int] = Query(None, description="Filter by condominium"),
    unit_id: Optional[int] = Query(None, description="Filter by unit"),
    ar_id: Optional[int] = Query(None, description="Filter by AR"),
    status: Optional[str] = Query(None, description="Filter by status"),
    submitted_by: Optional[int] = Query(None, description="Filter by submitter"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: UserIdentity = Depends(rbac_required("payment_proof", "read")),
) -> dict:
    """
    List payment proofs with optional filters.

    Visibility:
      - Admin/contador: sees all fields (bank_name, transaction_code, notes, reviewer)
      - Resident: sees limited fields (no admin-only data)
    """
    admin = _is_admin(user, condominium_id) if condominium_id else False
    response = PaymentProofUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        unit_id=unit_id,
        ar_id=ar_id,
        status=status,
        submitted_by=submitted_by,
        is_admin=admin,
    )
    return response.dict()


@payment_proof_routes.get("/{id}")
@api_handler
def get_proof(
    id: int,
    condominium_id: Optional[int] = Query(None, description="Condominium for admin check"),
    user: UserIdentity = Depends(rbac_required("payment_proof", "read")),
) -> dict:
    """Get a payment proof by id."""
    admin = _is_admin(user, condominium_id) if condominium_id else False
    response = PaymentProofUseCase().get_by_id(id, is_admin=admin)
    return response.dict()


@payment_proof_routes.get("/uuid/{uuid}")
@api_handler
def get_proof_by_uuid(
    uuid: str,
    condominium_id: Optional[int] = Query(None, description="Condominium for admin check"),
    user: UserIdentity = Depends(rbac_required("payment_proof", "read")),
) -> dict:
    """Get a payment proof by uuid."""
    admin = _is_admin(user, condominium_id) if condominium_id else False
    response = PaymentProofUseCase().get_by_uuid(uuid, is_admin=admin)
    return response.dict()


@payment_proof_routes.post("/{id}/approve")
@api_handler
def approve_proof(
    id: int,
    request: ApproveProofSchema,
    user: UserIdentity = Depends(rbac_required("payment_proof", "review")),
) -> dict:
    """
    Approve a payment proof.

    Creates the payment + receipt and updates AR status.
    Requires bank_name and transaction_code.
    """
    logger.add_inside_method("approve_proof") if hasattr(logger, "add_inside_method") else None

    review_data = ApproveProofData(
        bank_name=request.bank_name,
        transaction_code=request.transaction_code,
        notes=request.notes,
        payment_method=request.payment_method,
    )
    response = PaymentProofUseCase().approve(
        id=id,
        review_data=review_data,
        reviewed_by=user.id,
    )
    return response.dict()


@payment_proof_routes.post("/{id}/reject")
@api_handler
def reject_proof(
    id: int,
    request: RejectProofSchema,
    user: UserIdentity = Depends(rbac_required("payment_proof", "review")),
) -> dict:
    """
    Reject a payment proof.

    Requires rejection_reason. Does NOT create any payment.
    """
    logger.add_inside_method("reject_proof") if hasattr(logger, "add_inside_method") else None

    response = PaymentProofUseCase().reject(
        id=id,
        rejection_reason=request.rejection_reason,
        reviewed_by=user.id,
    )
    return response.dict()
