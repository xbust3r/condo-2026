"""
Payment Proof domain entity — comprobante de pago subido por residente,
revisado por admin/contador.
"""
from datetime import datetime
from typing import Optional, Dict, Any


class PaymentProofEntity:
    """Entidad de dominio para un comprobante de pago."""

    VALID_STATUSES = {"pending_review", "approved", "rejected"}
    ALLOWED_MIME_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "application/pdf",
    }
    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        unit_id: int,
        ar_id: int,
        submitted_by: int,
        file_url: str = "",
        original_filename: str = "",
        file_size_bytes: int = 0,
        mime_type: str = "",
        bank_name: Optional[str] = None,
        transaction_code: Optional[str] = None,
        notes: Optional[str] = None,
        status: str = "pending_review",
        reviewed_by: Optional[int] = None,
        reviewed_at: Optional[datetime] = None,
        rejection_reason: Optional[str] = None,
        payment_id: Optional[int] = None,
        receipt_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched
        submitted_by_name: Optional[str] = None,
        reviewed_by_name: Optional[str] = None,
        unit_code: Optional[str] = None,
        condominium_name: Optional[str] = None,
        ar_reference: Optional[str] = None,
        ar_amount: Optional[float] = None,
        receipt_number: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.unit_id = unit_id
        self.ar_id = ar_id
        self.submitted_by = submitted_by
        self.file_url = file_url
        self.original_filename = original_filename
        self.file_size_bytes = file_size_bytes
        self.mime_type = mime_type
        self.bank_name = bank_name
        self.transaction_code = transaction_code
        self.notes = notes
        self.status = status
        self.reviewed_by = reviewed_by
        self.reviewed_at = reviewed_at
        self.rejection_reason = rejection_reason
        self.payment_id = payment_id
        self.receipt_id = receipt_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enriched
        self.submitted_by_name = submitted_by_name
        self.reviewed_by_name = reviewed_by_name
        self.unit_code = unit_code
        self.condominium_name = condominium_name
        self.ar_reference = ar_reference
        self.ar_amount = ar_amount
        self.receipt_number = receipt_number

    def is_pending(self) -> bool:
        return self.status == "pending_review"

    def is_reviewed(self) -> bool:
        return self.status in ("approved", "rejected")

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def to_dict(self, is_admin: bool = False) -> Dict[str, Any]:
        """Serialize to dict. Admin sees all fields; resident sees limited fields."""
        base = {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "unit_id": self.unit_id,
            "ar_id": self.ar_id,
            "submitted_by": self.submitted_by,
            "file_url": self.file_url,
            "original_filename": self.original_filename,
            "file_size_bytes": self.file_size_bytes,
            "mime_type": self.mime_type,
            "status": self.status,
            "rejection_reason": self.rejection_reason if self.status == "rejected" else None,
            "payment_id": self.payment_id,
            "receipt_id": self.receipt_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # Enriched (public)
            "submitted_by_name": self.submitted_by_name,
            "unit_code": self.unit_code,
            "condominium_name": self.condominium_name,
            "ar_reference": self.ar_reference,
            "ar_amount": self.ar_amount,
            "receipt_number": self.receipt_number,
        }

        if is_admin:
            base.update({
                "bank_name": self.bank_name,
                "transaction_code": self.transaction_code,
                "notes": self.notes,
                "reviewed_by": self.reviewed_by,
                "reviewed_by_name": self.reviewed_by_name,
                "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            })

        return base
