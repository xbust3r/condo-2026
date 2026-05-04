"""
Payment Proof domain data transfer objects.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreatePaymentProofData:
    condominium_id: int
    unit_id: int
    ar_id: int
    submitted_by: int
    file_url: str
    original_filename: str
    file_size_bytes: int
    mime_type: str


@dataclass
class ApproveProofData:
    bank_name: str
    transaction_code: str
    notes: Optional[str] = None
    payment_method: str = "bank_transfer"


@dataclass
class RejectProofData:
    rejection_reason: str
