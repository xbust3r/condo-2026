"""
B2 cascade support — make override-eligible fields nullable.

For the cascade CONDOMINIUM → AMENITY_TYPE → AMENITY to work correctly,
lower levels must be able to signal "inherit from above" with NULL.

Fields made nullable:
- eligibility_mode  (AMENITY_TYPE/AMENITY can inherit from CONDOMINIUM)
- priority_policy   (AMENITY can inherit from AMENITY_TYPE)
- waitlist_mode     (AMENITY_TYPE/AMENITY can inherit from CONDOMINIUM)
- approval_mode     (AMENITY_TYPE/AMENITY can inherit from CONDOMINIUM)

CONDOMINIUM rows must still have values (enforced at application layer).

Revision ID: 062_nullable_policy_override_fields
Revises: 061_fix_b1_policy_idempotency
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '062_nullable_policy_override_fields'
down_revision: Union[str, None] = '061_fix_b1_policy_idempotency'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'core_amenity_policies', 'eligibility_mode',
        existing_type=sa.String(30),
        nullable=True,
        existing_server_default=None,
    )
    op.alter_column(
        'core_amenity_policies', 'priority_policy',
        existing_type=sa.String(30),
        nullable=True,
        existing_server_default=None,
    )
    op.alter_column(
        'core_amenity_policies', 'waitlist_mode',
        existing_type=sa.String(30),
        nullable=True,
        existing_server_default=None,
    )
    op.alter_column(
        'core_amenity_policies', 'approval_mode',
        existing_type=sa.String(30),
        nullable=True,
        existing_server_default=None,
    )


def downgrade() -> None:
    # Restore NOT NULL — fill any NULLs with sensible defaults first
    op.execute("""
        UPDATE core_amenity_policies SET eligibility_mode = 'all_residents'
        WHERE eligibility_mode IS NULL
    """)
    op.execute("""
        UPDATE core_amenity_policies SET priority_policy = 'fifo'
        WHERE priority_policy IS NULL
    """)
    op.execute("""
        UPDATE core_amenity_policies SET waitlist_mode = 'notify_and_confirm'
        WHERE waitlist_mode IS NULL
    """)
    op.execute("""
        UPDATE core_amenity_policies SET approval_mode = 'auto'
        WHERE approval_mode IS NULL
    """)

    op.alter_column(
        'core_amenity_policies', 'eligibility_mode',
        existing_type=op.VARCHAR(30),
        nullable=False,
        existing_server_default='all_residents',
    )
    op.alter_column(
        'core_amenity_policies', 'priority_policy',
        existing_type=op.VARCHAR(30),
        nullable=False,
        existing_server_default='fifo',
    )
    op.alter_column(
        'core_amenity_policies', 'waitlist_mode',
        existing_type=op.VARCHAR(30),
        nullable=False,
        existing_server_default='notify_and_confirm',
    )
    op.alter_column(
        'core_amenity_policies', 'approval_mode',
        existing_type=op.VARCHAR(30),
        nullable=False,
        existing_server_default='auto',
    )
