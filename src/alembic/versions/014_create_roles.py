"""
Create core_condominium_roles — roles administrativos por condominio.

¿Qué responde?: ¿Qué puede administrar un usuario dentro de un condominio?
¿Qué NO responde?: Propiedad, ocupación — solo permisos operativos.

Roles disponibles:
  super_admin         — administrador global del sistema
  condominium_admin    — administrador del condominio
  building_manager     — encargado de torre/edificio
  security_staff       — personal de seguridad
  maintenance_staff    — personal de mantenimiento
  support_staff        — personal de soporte general

Reglas:
  - Un admin no necesita vivir en el condominio
  - Un usuario puede administrar múltiples condominios
  - Los permisos son contextuales (por condominio), no globales

Revision ID: 014_create_roles
Revises: 013_create_core_unit_occupancies
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '014_create_roles'
down_revision: Union[str, None] = '013_create_core_unit_occupancies'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(table: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
        """),
        {"table": table},
    )
    return result.scalar() > 0


def upgrade() -> None:
    if not _table_exists('core_condominium_roles'):
        op.create_table(
            'core_condominium_roles',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
            sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('user_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column(
                'role',
                sa.String(40),
                nullable=False,
                server_default='condominium_admin',
            ),
            sa.Column(
                'status',
                sa.String(30),
                nullable=False,
                server_default='active',
            ),
            sa.Column('start_date', sa.Date(), nullable=True),
            sa.Column('end_date', sa.Date(), nullable=True),
            sa.Column(
                'created_at',
                sa.DateTime(),
                nullable=False,
                server_default=sa.text('CURRENT_TIMESTAMP'),
            ),
            sa.Column(
                'updated_at',
                sa.DateTime(),
                nullable=False,
                server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
            ),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('uuid'),
            sa.ForeignKeyConstraint(
                ['condominium_id'],
                ['core_condominiums.id'],
                name='fk_condominium_roles_condominium',
                ondelete='CASCADE',
            ),
            sa.ForeignKeyConstraint(
                ['user_id'],
                ['users.id'],
                name='fk_condominium_roles_user',
                ondelete='CASCADE',
            ),
            sa.Index('ix_condominium_roles_condo_user', 'condominium_id', 'user_id'),
            sa.Index('ix_condominium_roles_role', 'role'),
            sa.Index('ix_condominium_roles_status', 'status'),
        )


def downgrade() -> None:
    op.drop_table('core_condominium_roles')