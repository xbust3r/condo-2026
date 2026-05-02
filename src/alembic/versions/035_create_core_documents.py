"""
Create core_documents — tabla de documentos (actas, reglamentos, archivos adjuntos).

Revision ID: 035_create_core_documents
Revises: 034_create_core_announcements
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '035_create_core_documents'
down_revision: Union[str, None] = '034_create_core_announcements'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DOCUMENT_CATEGORIES = ['bylaws', 'minutes', 'regulation', 'contract', 'invoice', 'other']


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
    if not _table_exists('core_documents'):
        op.create_table(
            'core_documents',
            sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, unique=True),
            sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('uploader_user_id', sa.BigInteger(), nullable=False),
            sa.Column('title', sa.String(200), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('file_url', sa.String(500), nullable=False),
            sa.Column('file_size_bytes', sa.BigInteger(), nullable=True),
            sa.Column('mime_type', sa.String(100), nullable=True),
            sa.Column('category', sa.String(30), nullable=False, server_default='other'),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
            sa.ForeignKeyConstraint(['uploader_user_id'], ['users.id']),
            sa.Index('ix_documents_condo_category', 'condominium_id', 'category'),
        )


def downgrade() -> None:
    op.drop_table('core_documents')
