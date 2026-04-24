"""
Seed financial module permissions — charges, AR, payments, receipts, ledger.

Revision ID: 033_seed_financial_permissions
Revises: 032_create_core_ledger_entries
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '033_seed_financial_permissions'
down_revision: Union[str, None] = '032_create_core_ledger_entries'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


FINANCIAL_PERMISSIONS_SEED = [
    # Charge types
    ("charge_type.read",   "charge_type",   "read",   "condominium", "Ver tipos de cargo del catálogo"),
    ("charge_type.write",  "charge_type",   "write",  "condominium", "Crear/editar tipos de cargo"),

    # Charges
    ("charge.read",        "charge",         "read",   "condominium", "Ver cargos del condominio"),
    ("charge.write",       "charge",         "write",  "condominium", "Registrar y editar cargos"),
    ("charge.delete",      "charge",         "delete", "condominium", "Eliminar cargos"),

    # Accounts receivable
    ("ar.read",           "ar",             "read",   "condominium", "Ver cuentas por cobrar"),
    ("ar.write",          "ar",             "write",  "condominium", "Crear/editar cuentas por cobrar"),
    ("ar.delete",         "ar",             "delete", "condominium", "Eliminar cuentas por cobrar"),

    # Payments
    ("payment.read",       "payment",        "read",   "condominium", "Ver pagos registrados"),
    ("payment.write",      "payment",        "write",  "condominium", "Registrar pagos"),
    ("payment.delete",     "payment",        "delete", "condominium", "Eliminar/anular pagos"),

    # Receipts
    ("receipt.read",       "receipt",        "read",   "condominium", "Ver recibos emitidos"),
    ("receipt.write",      "receipt",        "write",  "condominium", "Emitir recibos"),

    # Ledger
    ("ledger.read",        "ledger",         "read",   "condominium", "Ver libro mayor por unidad"),
    ("ledger.export",      "ledger",         "export", "condominium", "Exportar libro mayor"),

    # Announcements
    ("announcement.read",   "announcement",   "read",   "condominium", "Ver anuncios del condominio"),
    ("announcement.write",  "announcement",   "write",  "condominium", "Publicar y editar anuncios"),
    ("announcement.delete", "announcement",   "delete", "condominium", "Eliminar anuncios"),

    # Documents
    ("document.read",       "document",       "read",   "condominium", "Ver documentos del condominio"),
    ("document.write",      "document",       "write",  "condominium", "Subir y editar documentos"),
    ("document.delete",     "document",       "delete", "condominium", "Eliminar documentos"),
]


def upgrade() -> None:
    for code, resource, action, scope_default, description in FINANCIAL_PERMISSIONS_SEED:
        op.execute(
            f"""
            INSERT INTO core_permissions (code, resource, action, scope_default, description)
            SELECT * FROM (
                SELECT :code AS code, :resource AS resource, :action AS action,
                       :scope_default AS scope_default, :description AS description
            ) AS tmp
            WHERE NOT EXISTS (
                SELECT 1 FROM core_permissions WHERE code = :code
            )
            """
        )


def downgrade() -> None:
    for code, _, _, _, _ in FINANCIAL_PERMISSIONS_SEED:
        op.execute(f"DELETE FROM core_permissions WHERE code = '{code}'")
