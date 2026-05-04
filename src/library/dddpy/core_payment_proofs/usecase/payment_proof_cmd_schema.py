"""
Payment Proof command schemas — Pydantic models for API request bodies.
"""
from typing import Optional

from pydantic import BaseModel, Field


class ApproveProofSchema(BaseModel):
    bank_name: str = Field(
        ..., min_length=1, max_length=100, description="Nombre del banco"
    )
    transaction_code: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Código de transacción / número de operación",
    )
    notes: Optional[str] = Field(
        None, max_length=2000, description="Observaciones (opcional)"
    )
    payment_method: str = Field(
        "bank_transfer",
        description="Método de pago (default: bank_transfer)",
    )


class RejectProofSchema(BaseModel):
    rejection_reason: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Motivo del rechazo",
    )
