"""
Payment Proof DB model — SQLAlchemy for payment_proofs table.
"""
from sqlalchemy import (
    Column, BigInteger, String, Text, DateTime, Numeric, func, ForeignKey,
)
from library.dddpy.shared.mysql.base import Base


class DBPaymentProof(Base):
    __tablename__ = "payment_proofs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(
        BigInteger,
        ForeignKey("core_condominiums.id", name="fk_payment_proofs_condominium"),
        nullable=False,
        index=True,
    )
    unit_id = Column(
        BigInteger,
        ForeignKey("core_units.id", name="fk_payment_proofs_unit"),
        nullable=False,
        index=True,
    )
    ar_id = Column(
        BigInteger,
        ForeignKey("core_accounts_receivable.id", name="fk_payment_proofs_ar"),
        nullable=False,
        index=True,
    )
    submitted_by = Column(
        BigInteger,
        ForeignKey("users.id", name="fk_payment_proofs_submitted_by"),
        nullable=False,
        index=True,
    )

    # Archivo
    file_url = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    mime_type = Column(String(100), nullable=False)

    # Datos administrativos (llenados por admin/contador al revisar)
    bank_name = Column(String(100), nullable=True)
    transaction_code = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    # Revisión
    status = Column(
        String(30), nullable=False, server_default="pending_review", index=True
    )
    reviewed_by = Column(
        BigInteger,
        ForeignKey("users.id", name="fk_payment_proofs_reviewed_by"),
        nullable=True,
    )
    reviewed_at = Column(DateTime, nullable=True)
    rejection_reason = Column(String(500), nullable=True)

    # Resultado de la aprobación
    payment_id = Column(
        BigInteger,
        ForeignKey("core_payments.id", name="fk_payment_proofs_payment"),
        nullable=True,
    )
    receipt_id = Column(
        BigInteger,
        ForeignKey("core_receipts.id", name="fk_payment_proofs_receipt"),
        nullable=True,
    )

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(DateTime, nullable=True)
