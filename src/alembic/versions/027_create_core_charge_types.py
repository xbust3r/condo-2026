"""
Create core_charge_types — catálogo de tipos de cargos del condominio.

Seed: 5 tipos base:
  monthly_fee      — Cuota Mensual ordinaria
  special_assessment — Cargo Extraordinario aprobado por asamblea
  reserve_fund     — Aportación al fondo de reserva
  penalty          — Multa por mora o incumplimiento
  utility          — Servicio común (agua, gas, mantenimiento)

Revision ID: 027_create_core_charge_types
Revises: 026_migrate_unit_occupancies
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '027_create_core_charge_types'
down_revision: Union[str, None] = '026_migrate_unit_occupancies'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CHARGE_TYPES_SEED = [
    {
        "code": "monthly_fee",
        "name": "Cuota Mensual",
        "description": "Cuota ordinaria mensual del condominio para gastos operativos.",
        "is_global": True,
        "is_active": True,
        "sort_order": 1,
    },
    {
        "code": "special_assessment",
        "name": "Cargo Extraordinario",
        "description": "Cargo aprobado por asamblea de propietarios para obras o gastos excepcionales.",
        "is_global": False,
        "is_active": True,
        "sort_order": 2,
    },
    {
        "code": "reserve_fund",
        "name": "Fondo de Reserva",
        "description": "Aportación mensual al fondo de reserva para imprevistos y mantenimiento mayor.",
        "is_global": True,
        "is_active": True,
        "sort_order": 3,
    },
    {
        "code": "penalty",
        "name": "Multa",
        "description": "Multa por mora en el pago de cuotas o incumplimiento del reglamento.",
        "is_global": False,
        "is_active": True,
        "sort_order": 4,
    },
    {
        "code": "utility",
        "name": "Servicio Común",
        "description": "Cargo por servicios comunes como agua, gas, mantenimiento de áreas.",
        "is_global": True,
        "is_active": True,
        "sort_order": 5,
    },
]


def upgrade() -> None:
    op.create_table(
        'core_charge_types',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_global', sa.SmallInteger(), nullable=False, server_default='1'),
        sa.Column('is_active', sa.SmallInteger(), nullable=False, server_default='1'),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_charge_types_code', 'core_charge_types', ['code'], unique=True)

    # Seed base system types
    conn = op.get_bind()
    for t in CHARGE_TYPES_SEED:
        conn.execute(
            text("""
                INSERT INTO core_charge_types
                    (uuid, code, name, description, is_global, is_active, sort_order)
                VALUES
                    (UUID(), :code, :name, :description, :is_global, :is_active, :sort_order)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    description = VALUES(description),
                    is_global = VALUES(is_global),
                    is_active = VALUES(is_active),
                    sort_order = VALUES(sort_order)
            """),
            {
                "code": t["code"],
                "name": t["name"],
                "description": t["description"],
                "is_global": 1 if t["is_global"] else 0,
                "is_active": 1 if t["is_active"] else 0,
                "sort_order": t["sort_order"],
            }
        )


def downgrade() -> None:
    op.drop_index('ix_charge_types_code', table_name='core_charge_types')
    op.drop_table('core_charge_types')
