"""
Create core_occupancy_types — catálogo de tipos de ocupación de unidades.

Reemplaza el enum hardcodeado en frontend:
  resident_owner, tenant, family_member, office_user, occasional_user

Agrega además el flag requires_authorization para validaciones de negocio.

Seed: 5 tipos base con requires_authorization flag.

Revision ID: 025_create_core_occupancy_types
Revises: 024_add_theme_id_to_condominiums
Create Date: 2026-04-23
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '025_create_core_occupancy_types'
down_revision: Union[str, None] = '024_add_theme_id_to_condominiums'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


OCCUPANCY_TYPES_SEED = [
    {
        "code": "resident_owner",
        "name": "Propietario Residente",
        "description": "Persona que es propietaria de la unidad y reside en ella.",
        "requires_authorization": False,
        "allows_primary": True,
        "is_active": True,
        "sort_order": 1,
    },
    {
        "code": "tenant",
        "name": "Inquilino",
        "description": "Persona que ocupa la unidad bajo contrato de arrendamiento. "
                       "Requiere autorización del propietario.",
        "requires_authorization": True,
        "allows_primary": True,
        "is_active": True,
        "sort_order": 2,
    },
    {
        "code": "family_member",
        "name": "Familiar",
        "description": "Miembro de la familia del propietario o inquilino que habita la unidad. "
                       "Puede requerir autorización según políticas del condominio.",
        "requires_authorization": True,
        "allows_primary": False,
        "is_active": True,
        "sort_order": 3,
    },
    {
        "code": "office_user",
        "name": "Usuario de Oficina",
        "description": "Persona que utiliza la unidad con fines comerciales o de oficina. "
                       "No es residente.",
        "requires_authorization": True,
        "allows_primary": False,
        "is_active": True,
        "sort_order": 4,
    },
    {
        "code": "occasional_user",
        "name": "Usuario Ocasional",
        "description": "Persona con acceso ocasional o temporal a la unidad (Airbnb, "
                       "préstamo temporal, etc.).",
        "requires_authorization": True,
        "allows_primary": False,
        "is_active": True,
        "sort_order": 5,
    },
]


def upgrade() -> None:
    # Create table with new fields: scope, condominium_id, allows_primary
    op.create_table(
        'core_occupancy_types',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('scope', sa.String(20), nullable=False, server_default='system'),
        sa.Column('condominium_id', sa.BigInteger(), nullable=True, index=True),
        sa.Column('requires_authorization', sa.SmallInteger(), nullable=False, server_default='0'),
        sa.Column('allows_primary', sa.SmallInteger(), nullable=False, server_default='1'),
        sa.Column('is_active', sa.SmallInteger(), nullable=False, server_default='1'),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    # Unique code scoped to (scope, condominium_id)
    op.create_index('ix_occupancy_types_code', 'core_occupancy_types',
                   ['scope', 'condominium_id', 'code'], unique=True)

    # Seed base system types
    for t in OCCUPANCY_TYPES_SEED:
        op.execute(
            text("""
                INSERT INTO core_occupancy_types
                    (uuid, code, name, description, scope, condominium_id,
                     requires_authorization, allows_primary, is_active, sort_order)
                VALUES
                    (UUID(), :code, :name, :description, 'system', NULL,
                     :requires_authorization, :allows_primary, :is_active, :sort_order)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    description = VALUES(description),
                    requires_authorization = VALUES(requires_authorization),
                    allows_primary = VALUES(allows_primary),
                    is_active = VALUES(is_active),
                    sort_order = VALUES(sort_order)
            """),
            {
                "code": t["code"],
                "name": t["name"],
                "description": t["description"],
                "requires_authorization": 1 if t["requires_authorization"] else 0,
                "allows_primary": 1 if t["allows_primary"] else 0,
                "is_active": 1 if t["is_active"] else 0,
                "sort_order": t["sort_order"],
            }
        )


def downgrade() -> None:
    op.drop_index('ix_occupancy_types_code', table_name='core_occupancy_types')
    op.drop_table('core_occupancy_types')