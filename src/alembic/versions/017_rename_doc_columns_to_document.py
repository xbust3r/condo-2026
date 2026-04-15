"""
Rename columns in user_profiles for semantic consistency:
  doc_type        → document_type
  doc_identity    → document_number

Revision ID: 017_rename_doc_columns_to_document
Revises: 016_add_token_version_to_users
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '017_rename_doc_columns_to_document'
down_revision: Union[str, None] = '016_add_token_version_to_users'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
        """),
        {"table": table, "column": column},
    )
    return result.scalar() > 0


def upgrade() -> None:
    # doc_type → document_type
    if _column_exists('user_profiles', 'doc_type') and not _column_exists('user_profiles', 'document_type'):
        op.execute("ALTER TABLE `user_profiles` CHANGE COLUMN `doc_type` `document_type` VARCHAR(20) NULL")

    # doc_identity → document_number
    if _column_exists('user_profiles', 'doc_identity') and not _column_exists('user_profiles', 'document_number'):
        op.execute("ALTER TABLE `user_profiles` CHANGE COLUMN `doc_identity` `document_number` VARCHAR(50) NULL")


def downgrade() -> None:
    if _column_exists('user_profiles', 'document_type') and not _column_exists('user_profiles', 'doc_type'):
        op.execute("ALTER TABLE `user_profiles` CHANGE COLUMN `document_type` `doc_type` VARCHAR(20) NULL")

    if _column_exists('user_profiles', 'document_number') and not _column_exists('user_profiles', 'doc_identity'):
        op.execute("ALTER TABLE `user_profiles` CHANGE COLUMN `document_number` `doc_identity` VARCHAR(50) NULL")
