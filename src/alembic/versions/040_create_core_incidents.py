"""
Create core_incidents — maintenance ticketing / incident report system.

Revision ID: 040_create_core_incidents
Revises: 035_create_core_documents
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '040_create_core_incidents'
down_revision: Union[str, None] = '035_create_core_documents'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


INCIDENT_CATEGORIES = [
    'plumbing', 'electrical', 'structural', 'common_areas',
    'elevator', 'painting', 'cleaning', 'pest_control', 'security', 'other',
]
INCIDENT_PRIORITIES = ['low', 'medium', 'high', 'urgent']
INCIDENT_STATUSES = ['pending', 'open', 'in_progress', 'resolved', 'closed', 'cancelled']


def _table_exists(table: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*) FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :table
        """),
        {"table": table},
    )
    return result.scalar() > 0


def upgrade() -> None:
    if not _table_exists('core_incidents'):
        op.create_table(
            'core_incidents',
            sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, unique=True),
            sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('building_id', sa.BigInteger(), nullable=True, index=True),
            sa.Column('unit_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('reported_by_user_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('assigned_to_user_id', sa.BigInteger(), nullable=True, index=True),
            sa.Column('category', sa.String(40), nullable=False, server_default='other'),
            sa.Column('priority', sa.String(20), nullable=False, server_default='medium'),
            sa.Column('status', sa.String(30), nullable=False, server_default='pending'),
            sa.Column('title', sa.String(150), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('photos', sa.Text(), nullable=True),
            sa.Column('internal_notes', sa.Text(), nullable=True),
            sa.Column('resolution_notes', sa.Text(), nullable=True),
            sa.Column('scheduled_date', sa.Date(), nullable=True),
            sa.Column('completed_date', sa.Date(), nullable=True),
            sa.Column('is_escalated', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
            sa.ForeignKeyConstraint(['building_id'], ['core_buildings.id']),
            sa.ForeignKeyConstraint(['unit_id'], ['core_units.id']),
            sa.ForeignKeyConstraint(['reported_by_user_id'], ['users.id']),
            sa.ForeignKeyConstraint(['assigned_to_user_id'], ['users.id']),
            sa.Index('ix_incidents_condo_status', 'condominium_id', 'status'),
            sa.Index('ix_incidents_unit', 'unit_id'),
            sa.Index('ix_incidents_assigned', 'assigned_to_user_id'),
            sa.Index('ix_incidents_reported_by', 'reported_by_user_id'),
        )
        # MariaDB 10.5 workaround: ensure AUTO_INCREMENT is set on PK
        op.execute(sa.text(
            "ALTER TABLE core_incidents MODIFY id BIGINT NOT NULL AUTO_INCREMENT"
        ))


def downgrade() -> None:
    op.drop_table('core_incidents')
